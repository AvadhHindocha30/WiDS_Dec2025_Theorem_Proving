def dpll(clauses, assignment=None):
    """
    clauses: list of sets (e.g. {{'P', '~Q'}, {'Q'}})
    assignment: dict mapping variable -> bool
    Returns: (sat: bool, assignment)
    """
    if assignment is None:
        assignment = {}
    assignment = dict(assignment)

    def lit_var(lit: str) -> str:
        return lit[1:] if lit.startswith("~") else lit

    def lit_val(lit: str) -> bool:
        return not lit.startswith("~")

    def simplify(curr, var: str, val: bool):
        pos = var
        neg = "~" + var
        sat_l = pos if val else neg
        bad_l = neg if val else pos

        out = []
        for cl in curr:
            if sat_l in cl:
                continue
            if bad_l in cl:
                nc = set(cl)
                nc.discard(bad_l)
                out.append(nc)
            else:
                out.append(set(cl))
        return out

    if not clauses:
        return True, assignment

    for cl in clauses:
        if len(cl) == 0:
            return False, {}

    while True:
        progressed = False

        unit = None
        for cl in clauses:
            if len(cl) == 1:
                unit = next(iter(cl))
                break

        if unit is not None:
            v = lit_var(unit)
            val = lit_val(unit)
            if v in assignment and assignment[v] != val:
                return False, {}
            assignment[v] = val
            clauses = simplify(clauses, v, val)
            for cl in clauses:
                if len(cl) == 0:
                    return False, {}
            if not clauses:
                return True, assignment
            progressed = True

        if not progressed:
            pos = set()
            neg = set()
            for cl in clauses:
                for lit in cl:
                    v = lit_var(lit)
                    if v in assignment:
                        continue
                    if lit_val(lit):
                        pos.add(v)
                    else:
                        neg.add(v)

            only_pos = pos - neg
            only_neg = neg - pos
            if only_pos or only_neg:
                if only_pos:
                    v = next(iter(only_pos))
                    val = True
                else:
                    v = next(iter(only_neg))
                    val = False

                if v in assignment and assignment[v] != val:
                    return False, {}
                assignment[v] = val
                clauses = simplify(clauses, v, val)
                for cl in clauses:
                    if len(cl) == 0:
                        return False, {}
                if not clauses:
                    return True, assignment
                progressed = True

        if not progressed:
            break

    pick = None
    for cl in clauses:
        for lit in cl:
            v = lit_var(lit)
            if v not in assignment:
                pick = v
                break
        if pick is not None:
            break

    if pick is None:
        return True, assignment

    for val in (True, False):
        next_assign = dict(assignment)
        next_assign[pick] = val
        sat, sol = dpll(simplify(clauses, pick, val), next_assign)
        if sat:
            return True, sol

    return False, {}
