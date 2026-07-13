# THM-M-0895 scope map

## Preserved theorem family

The catalog preserves a family of necessary relations among the parameters of a finite strongly
regular graph. It does not select one constraint. Candidate components below form a resolution
ledger and are not statements credited to this target:

- the elementary feasibility equation
  `k * (k - lambda - 1) = (v - k - 1) * mu`;
- the adjacency-matrix identity
  `A^2 = k I + lambda A + mu (J - I - A)`;
- the complement parameter transformation;
- the two restricted nontrivial adjacency eigenvalues and their quadratic equation;
- eigenvalue multiplicities and their integrality or divisibility consequences;
- absolute, Krein, or other feasibility bounds; and
- parameter relations arising specifically from partial geometries or partially balanced designs.

## Decisions required at statement freeze

1. Admit a lawful immutable primary or authoritative edition, select the exact result and locator,
   map all incorporated definitions and proof boundaries, audit corrections or errata, and obtain
   independent source approval.
2. Decide whether the root is one named parameter equation, a matrix or spectral theorem, an
   integrality condition, a bound, a partial-geometry relation, or a precisely delimited
   conjunction.
3. Fix the parameter order and notation. Common conventions use `(v,k,lambda,mu)` or
   `(n,k,lambda,mu)`, while pinned Lean uses `IsSRGWith n k l mu`.
4. Fix the graph model, finite vertex carrier, decidable adjacency, regularity convention, common
   neighbor counts, and whether nonadjacent pairs are required to be distinct.
5. Fix every nontriviality and positivity assumption. Pinned `param_eq` requires `0 < n`; empty
   and complete graphs make some common-neighbor clauses vacuous, and many sources exclude them
   from the definition of a strongly regular graph.
6. Fix arithmetic domains and subtraction semantics. Mathlib's candidate equation is in `Nat`
   with truncated subtraction; source algebra may instead be an integer equality under bounds.
7. Freeze ordered binders and decide whether parameters are derived from a graph, supplied as
   hypotheses, or existentially quantified.

## Degenerate and boundary cases

Source review must dispose explicitly of empty and singleton vertex types, the empty and complete
graphs, `n = 0`, `k = 0`, `k = n - 1`, `mu = 0`, and parameter tuples for which adjacent or
nonadjacent pair clauses are vacuous. It must also decide whether connectedness or coconnectedness
is assumed, whether `0 < k < n - 1` is part of the definition, and how natural subtraction is
related to ordinary integer algebra.

In pinned mathlib, `bot_strongly_regular` and `IsSRGWith.top` deliberately include empty and
complete graphs. Therefore a source that adopts the conventional nontrivial definition cannot be
identified with `IsSRGWith` without explicit side conditions and a checked transport.

## Substitution exclusions

- Do not select `IsSRGWith.param_eq` merely because it is the easiest close pinned theorem.
- Do not replace a spectral, integrality, or feasibility-bound claim with the elementary counting
  equation, or conversely, without a source-approved checked relationship.
- A definition or structure hypothesis storing the four parameters is not a proof of any requested
  constraint.
- A result about a single named graph or one numerical parameter tuple is not the generic target.
- A partial-geometry or association-scheme specialization cannot replace a generic strongly
  regular graph result.
- Numerical eigenvalue experiments, graph databases, and unchecked matrix calculations carry no
  theorem credit.
- The catalog's `verified` label, theorem names, and this API probe carry no source or proof credit.

No canonical Lean target, expression fingerprint, checked alternate encoding, mutation suite,
discovery protocol, obligation registry, or proof body is frozen at intake.
