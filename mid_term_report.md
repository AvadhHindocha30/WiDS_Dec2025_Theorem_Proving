# WiDS5.0 — AI for Logical Thinking (Theorem Proving)

This project focuses on learning core ideas in **automated reasoning / theorem proving** and implementing classical proof procedures in code. The goal over these two weeks was to build a strong foundation in logic-based inference systems and understand how modern theorem provers organize search to derive contradictions or proofs efficiently.

---

## Week 1 — Foundations of Logic + Implementations

### What I learned
- **Propositional logic basics**: syntax/semantics of formulas, truth assignments, and the idea of satisfiability vs. unsatisfiability.
- **CNF (Conjunctive Normal Form)**: why CNF is the standard input format for many SAT solvers and proof procedures, and how logical equivalences can be used to transform an expression into CNF.
- **SAT solving with DPLL**: how the Davis–Putnam–Logemann–Loveland algorithm searches over assignments using:
  - **unit propagation**
  - **pure literal elimination**
  - **backtracking/branching**
- **First-Order Logic (FOL)**: predicates, variables, constants, function symbols, and why general satisfiability in FOL is **undecidable** (so provers typically aim to prove UNSAT or return TIMEOUT).
- **Robinson Resolution + Unification**: how resolution extends to FOL using **Most General Unifier (MGU)**, unification, and occurs-check style reasoning to combine clauses.

### Assignments completed
- **Propositional Logic — CNF conversion**
  - Implemented `to_cnf(expr)` which converts an expression tree containing `Var`, `Not`, `And`, `Or`, `Implies` into CNF as a list of clauses.
  - Steps used: implication elimination → pushing negations inward (De Morgan / double-negation) → distributing OR over AND → extracting clause sets.
- **Propositional Logic — DPLL SAT solver**
  - Implemented `dpll(clauses, assignment)` that returns whether the CNF is satisfiable and (if SAT) a satisfying assignment.
  - Focused on correctness with edge cases like empty clause sets, contradictory unit clauses, and formulas requiring branching.
- **First-Order Logic — Robinson’s resolution**
  - Implemented `robinson_resolution(clauses, max_iterations)` to attempt proving **UNSAT** by deriving the empty clause via resolution.
  - Implemented **unification (MGU)** to resolve complementary literals with matching predicates and compatible arguments.
  - Since FOL satisfiability is undecidable, the solver returns:
    - **UNSAT** if a contradiction is derived
    - **TIMEOUT** if it cannot derive a contradiction within the iteration limit

---

## Week 2 — Search Control in Theorem Proving (Reading + Concepts)

### What I learned
Week 2 was focused on how real theorem provers control the explosion of the search space during resolution.

- **Given-Clause Algorithm**
  - Learned how provers maintain an **active set** (processed clauses) and a **passive set** (unprocessed clauses).
  - Understood the “pick one clause, generate inferences, then move it to processed” workflow and why clause selection order heavily affects performance.
- **Set of Support (SoS) Strategy**
  - Learned how SoS restricts resolution so that at least one parent clause comes from a designated “support” set (often derived from the negated conjecture).
  - Understood why this is useful for focusing the proof search and avoiding irrelevant derivations.
- **Subsumption and redundancy control**
  - Studied how provers remove clauses that are logically weaker/less useful:
    - A clause can be removed if it is **subsumed** by a stronger clause.
  - Understood the motivation behind redundancy elimination: fewer clauses → fewer resolution pairs → faster search.
- **Clause weighting and selection heuristics**
  - Learned how provers prioritize clauses based on features like:
    - clause length / number of literals
    - term depth / nesting (weight)
    - symbol frequency, etc.
  - Understood that these heuristics are crucial because resolution can generate an extremely large number of clauses.

---

## Summary of work so far
- Built implementations for **CNF conversion**, **DPLL SAT solving**, and **FOL resolution with unification**, which cover the core mechanics behind many SAT/ATP systems.
- Studied practical theorem-prover strategies (Given-Clause, SoS, subsumption, clause weighting) to understand how modern provers remain efficient despite the combinatorial nature of proof search.

---

## Repository structure (high level)
- `Week1/prop_logic/` — CNF conversion + DPLL solver (with autograders and testcases)
- `Week1/fol/` — Robinson resolution for FOL (with autograder and testcases)
- `Week2/` — reading resources and notes on search-control strategies
