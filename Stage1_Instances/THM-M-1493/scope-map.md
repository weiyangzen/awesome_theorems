# THM-M-1493 scope map

## Preserved repository scope

- Target identity: `THM-M-1493`, named `单纯形法` (simplex method).
- Literal gloss: `线性规划的算法` (an algorithm for linear programming).
- Catalog attribution and date: George Dantzig, 1947.
- Recognizable boundary: a simplex-family procedure for finite-dimensional linear programs.

This identifies a method family, not one proposition. Intake preserves that ambiguity rather than
silently adopting a modern textbook formulation or the behavior of mathlib's certificate oracle.

## Proposition-changing decisions

An accountable source correction must select one immutable proposition and freeze:

1. The linear-program representation: equality or inequality form, minimization or maximization,
   slack variables, homogeneous or affine formulation, and primal, dual, or phase-I problem.
2. The coefficient domain and dimensions: rationals, reals, an ordered field, finite index types,
   matrix/vector orientation, encodings, and universe/typeclass context.
3. Input assumptions: feasibility, existence of an initial basis, boundedness, full rank,
   nondegeneracy, exact arithmetic, and any regularity or finiteness conditions.
4. The algorithm: tableau or revised simplex state, initialization, entering and leaving rules,
   ratio-test and tie conventions, basis updates, phase transitions, and stopping conditions.
5. The conclusion: preservation of feasibility, strict objective improvement, finite termination,
   optimality, infeasibility or unboundedness certification, completeness, or complexity.
6. Degeneracy and cycling policy: exclusion, symbolic perturbation, Bland's rule, lexicographic
   pivoting, or another source-defined strategy and its exact termination theorem.
7. The execution semantics: mathematical relation versus executable code, exact versus
   floating-point arithmetic, resource cancellation, failure behavior, and certificate checking.
8. Ordered binders, hypotheses, alternate encodings and transport directions, boundary cases,
   source corrections, and foundation/TCB/computation/freshness profiles.

Each choice changes truth conditions and proof obligations. This list is a resolution ledger, not a
candidate statement.

## Candidate theorem families not credited

- Existence of a basic feasible solution when a feasible solution exists.
- A reduced-cost or supporting-hyperplane criterion proving that a feasible basis is optimal.
- A pivot lemma preserving feasibility while improving or not decreasing the objective.
- Finite termination for nondegenerate inputs or under Bland/lexicographic anti-cycling rules.
- Correct detection of infeasibility or unboundedness.
- End-to-end soundness and completeness of a specified phase-I/phase-II algorithm.
- Exponential lower bounds, smoothed complexity, or a bound for a particular pivot rule.

No candidate is selected, combined, or credited at intake.

## Boundary cases to resolve

- zero variables or constraints, empty feasible sets, and inconsistent equalities;
- feasible but unbounded objectives, bounded objectives whose maximum is not attained under an
  alternate infinite-domain encoding, and multiple optima;
- rank-deficient constraints, redundant rows or columns, zero columns, and nonunique bases;
- degenerate basic feasible solutions, zero-length pivots, ties, cycling, and repeated bases;
- already optimal input, absent initial feasible basis, phase-I failure, and artificial variables;
- strict versus non-strict inequalities and sign-unrestricted variables;
- rational exactness versus real existence and floating-point roundoff; and
- cancellation, iteration limits, or implementation exceptions.

No case is excluded before a proposition is selected.

## Neighbor ownership and exclusions

| Target | Boundary |
|---|---|
| `THM-M-1492` linear programming | owns the broader optimization problem and its existence/duality questions; no algorithm theorem is inherited |
| `THM-M-1494` interior-point method | distinct LP algorithm family and complexity/correctness contracts |
| `THM-M-1495` ellipsoid method | distinct separation-oracle algorithm and polynomial-time theorem family |
| `THM-M-1496` semidefinite programming | broader conic optimization target, not a simplex-method result |
| `THM-M-1506` KKT conditions | optimality conditions may be substrate but do not identify simplex iteration |

Also excluded are a single worked numerical example, a `linarith` proof of one linear-arithmetic
goal, generic LP duality alone, an assumed solver result, or a structure field that stores desired
correctness as a premise.

## Formal and execution boundary

Pinned mathlib's `Mathlib.Tactic.Linarith.SimplexAlgorithm` namespace implements a rational,
meta-level certificate search for `linarith`. Its internal problem asks for a nonnegative vector
`v` with `A v = 0` and a positive strict coordinate. It is adjacent to the topic, but it neither
selects the catalog root nor exposes an inspected theorem proving a general LP solver correct,
complete, terminating under the catalog's intended assumptions, or faithful to Dantzig's 1947
method. The canonical statement, obligation registry, and discovery protocol remain open.
