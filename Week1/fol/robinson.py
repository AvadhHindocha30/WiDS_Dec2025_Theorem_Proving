"""
First-Order Logic - Robinson's Resolution Algorithm
Implement the Robinson resolution algorithm for FOL theorem proving.
"""

from typing import List, Tuple

def unify() -> dict:
    """
    Unification algorithm - find most general unifier (MGU).
    
    Returns:
        Substitution dictionary if unifiable, None otherwise
    """
    pair = globals().get("_UNIFY_PAIR", None)
    if not isinstance(pair, tuple) or len(pair) != 2:
        return None

    left_lit, right_lit = pair[0], pair[1]

    def split_args(s: str) -> List[str]:
        out = []
        depth = 0
        buf = []
        for ch in s:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if ch == "," and depth == 0:
                out.append("".join(buf).strip())
                buf = []
            else:
                buf.append(ch)
        out.append("".join(buf).strip())
        return out

    def parse_lit(l: str):
        l = l.strip()
        neg = False
        if l.startswith("~"):
            neg = True
            l = l[1:].strip()
        if "(" not in l:
            return neg, l, []
        name = l[: l.find("(")].strip()
        inside = l[l.find("(") + 1 : -1].strip()
        args = [] if inside == "" else split_args(inside)
        return neg, name, args

    def is_var_term(t: str) -> bool:
        t = t.strip()
        return t != "" and t[0].islower() and "(" not in t

    def is_func_term(t: str) -> bool:
        t = t.strip()
        return "(" in t and t.endswith(")")

    def func_parts(t: str):
        t = t.strip()
        nm = t[: t.find("(")].strip()
        inside = t[t.find("(") + 1 : -1].strip()
        args = [] if inside == "" else split_args(inside)
        return nm, args

    def apply_sub_term(t: str, sub: dict) -> str:
        t = t.strip()
        if is_func_term(t):
            nm, args = func_parts(t)
            new_args = [apply_sub_term(a, sub) for a in args]
            return nm + "(" + ",".join(new_args) + ")"
        seen = set()
        while is_var_term(t) and t in sub and t not in seen:
            seen.add(t)
            t = str(sub[t]).strip()
        if is_func_term(t):
            return apply_sub_term(t, sub)
        return t

    def occurs(v: str, term: str, sub: dict) -> bool:
        term = apply_sub_term(term, sub)
        if term == v:
            return True
        if is_func_term(term):
            _, args = func_parts(term)
            for a in args:
                if occurs(v, a, sub):
                    return True
        return False

    def unify_terms(a: str, b: str, sub: dict):
        a = apply_sub_term(a, sub)
        b = apply_sub_term(b, sub)

        if a == b:
            return sub

        if is_var_term(a):
            if occurs(a, b, sub):
                return None
            sub[a] = b
            for k in list(sub.keys()):
                if k != a:
                    sub[k] = apply_sub_term(sub[k], {a: b})
            return sub

        if is_var_term(b):
            if occurs(b, a, sub):
                return None
            sub[b] = a
            for k in list(sub.keys()):
                if k != b:
                    sub[k] = apply_sub_term(sub[k], {b: a})
            return sub

        if is_func_term(a) and is_func_term(b):
            na, aa = func_parts(a)
            nb, ab = func_parts(b)
            if na != nb or len(aa) != len(ab):
                return None
            for x, y in zip(aa, ab):
                sub = unify_terms(x, y, sub)
                if sub is None:
                    return None
            return sub

        return None

    n1, p1, a1 = parse_lit(left_lit)
    n2, p2, a2 = parse_lit(right_lit)

    if p1 != p2 or n1 == n2 or len(a1) != len(a2):
        return None

    theta = {}
    for x, y in zip(a1, a2):
        theta = unify_terms(x, y, theta)
        if theta is None:
            return None

    return theta


def robinson_resolution(clauses: List[List[str]], max_iterations: int = 1000) -> Tuple[str, List]:
    """
    Robinson's resolution algorithm for FOL.
    
    Args:
        clauses: List of clauses in CNF (each clause is list of literals)
        max_iterations: Maximum resolution steps before timeout
        
    Returns:
        ("UNSAT", proof) if empty clause derived (contradiction found)
        ("TIMEOUT", []) if max_iterations reached or no new clauses
    """
    def split_args(s: str) -> List[str]:
        out = []
        depth = 0
        buf = []
        for ch in s:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if ch == "," and depth == 0:
                out.append("".join(buf).strip())
                buf = []
            else:
                buf.append(ch)
        out.append("".join(buf).strip())
        return out

    def parse_lit(l: str):
        l = l.strip()
        neg = False
        if l.startswith("~"):
            neg = True
            l = l[1:].strip()
        if "(" not in l:
            return neg, l, []
        name = l[: l.find("(")].strip()
        inside = l[l.find("(") + 1 : -1].strip()
        args = [] if inside == "" else split_args(inside)
        return neg, name, args

    def is_var_term(t: str) -> bool:
        t = t.strip()
        return t != "" and t[0].islower() and "(" not in t

    def is_func_term(t: str) -> bool:
        t = t.strip()
        return "(" in t and t.endswith(")")

    def func_parts(t: str):
        t = t.strip()
        nm = t[: t.find("(")].strip()
        inside = t[t.find("(") + 1 : -1].strip()
        args = [] if inside == "" else split_args(inside)
        return nm, args

    def apply_sub_term(t: str, sub: dict) -> str:
        t = t.strip()
        if is_func_term(t):
            nm, args = func_parts(t)
            new_args = [apply_sub_term(a, sub) for a in args]
            return nm + "(" + ",".join(new_args) + ")"
        seen = set()
        while is_var_term(t) and t in sub and t not in seen:
            seen.add(t)
            t = str(sub[t]).strip()
        if is_func_term(t):
            return apply_sub_term(t, sub)
        return t

    def apply_sub_lit(l: str, sub: dict) -> str:
        neg, pred, args = parse_lit(l)
        new_args = [apply_sub_term(a, sub) for a in args]
        body = pred + "(" + ",".join(new_args) + ")"
        return ("~" + body) if neg else body

    def vars_in_term(t: str) -> List[str]:
        t = t.strip()
        if is_var_term(t):
            return [t]
        if is_func_term(t):
            _, args = func_parts(t)
            acc = []
            for a in args:
                acc.extend(vars_in_term(a))
            return acc
        return []

    def vars_in_lit(l: str) -> List[str]:
        _, _, args = parse_lit(l)
        acc = []
        for a in args:
            acc.extend(vars_in_term(a))
        return acc

    def fresh_name(k: int) -> str:
        return "v" + str(k)

    counter = {"k": 0}

    def standardize_clause(cl: List[str]) -> List[str]:
        seen = set()
        for lit in cl:
            for v in vars_in_lit(lit):
                seen.add(v)
        mapping = {}
        for v in sorted(seen):
            mapping[v] = fresh_name(counter["k"])
            counter["k"] += 1
        if not mapping:
            return list(cl)
        return [apply_sub_lit(l, mapping) for l in cl]

    def standardize_pair(c1: List[str], c2: List[str]):
        return standardize_clause(c1), standardize_clause(c2)

    def canonicalize(clset: set) -> frozenset:
        allv = set()
        for lit in clset:
            for v in vars_in_lit(lit):
                allv.add(v)
        mapping = {}
        i = 0
        for v in sorted(allv):
            mapping[v] = "x" + str(i)
            i += 1
        if not mapping:
            return frozenset(clset)
        return frozenset(apply_sub_lit(l, mapping) for l in clset)

    if any(len(c) == 0 for c in clauses):
        return "UNSAT", []

    kb = set()
    for c in clauses:
        c0 = standardize_clause(list(c))
        kb.add(canonicalize(set(c0)))

    for _ in range(max_iterations):
        kb_list = list(kb)
        produced = set()

        for i in range(len(kb_list)):
            for j in range(i + 1, len(kb_list)):
                a = list(kb_list[i])
                b = list(kb_list[j])

                a2, b2 = standardize_pair(a, b)

                for l1 in a2:
                    for l2 in b2:
                        globals()["_UNIFY_PAIR"] = (l1, l2)
                        sub = unify()
                        if sub is None:
                            continue

                        res = set()
                        for t in a2:
                            if t != l1:
                                res.add(apply_sub_lit(t, sub))
                        for t in b2:
                            if t != l2:
                                res.add(apply_sub_lit(t, sub))

                        if not res:
                            return "UNSAT", []

                        fz = canonicalize(res)
                        if fz not in kb and fz not in produced:
                            produced.add(fz)

        if not produced:
            return "TIMEOUT", []

        kb |= produced

    return "TIMEOUT", []
