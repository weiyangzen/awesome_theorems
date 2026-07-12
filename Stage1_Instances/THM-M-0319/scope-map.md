# Scope map

## Included root

- The ambient space is real and finite-dimensional, provisionally `R^n` for a natural number `n`.
- `K` is a nonempty, compact, convex subset of that space.
- The map is a continuous self-map of `K`, either encoded directly on the subtype or by an ambient
  function together with a checked `MapsTo` condition.
- The conclusion is existence of `x` in `K` satisfying the literal fixed-point equation.

The zero-dimensional case is intentionally not discarded: if the chosen encoding admits `n = 0`,
nonemptiness makes the claim valid. Empty `K` is excluded because it supplies an immediate
counterexample to the existential conclusion. No uniqueness, computable fixed-point selector, or
convergence rate is asserted.

## Statement-phase decisions

The next phase must freeze the concrete Euclidean representation (`EuclideanSpace R (Fin n)`, a
finite-dimensional real normed space, or a checked equivalent), subtype-versus-ambient function
encoding, binder order and universes, and the exact compactness/convexity predicates. It must also
check whether the selected primary source states the theorem for a simplex, closed ball, bounded
closed convex set, or general compact convex set and provide checked transports rather than
treating these formulations as definitionally equal.

## Explicit exclusions

- Banach's contraction mapping theorem or any extra contraction hypothesis.
- Schauder, Kakutani, Markov-Kakutani, Tychonoff, or Knaster-Tarski as a substituted root.
- The interval-only theorem, a simplex-only theorem, or the closed-ball formulation without the
  proof obligation transporting it to the frozen compact-convex claim.
- Infinite-dimensional compact-convex spaces, set-valued maps, approximate fixed points, or a
  statement that assumes a fixed point as structure data.
- The separate duplicate metadata target `THM-M-0640`; no evidence or status is shared with it.

## Profiles still open

The exact Lean imports, foundation/choice dependencies, terminal proof-body provenance, complete
TCB, source edition, theorem/page, errata, and readable proof architecture are deliberately open.
They belong to later statement, anchor-audit, obligation-tree, proof, validation, and release nodes.
