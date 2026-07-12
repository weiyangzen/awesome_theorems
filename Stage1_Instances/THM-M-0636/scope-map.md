# Scope map

## Preserved catalog scope

The intake preserves the Brouwer fixed-point family indicated jointly by the catalog's attribution
to Brouwer, year 1910, compact-convex wording, and point-set-topology placement. A later statement
phase may freeze a proposition only after an immutable authoritative source is selected and its
assumptions are independently reviewed.

The likely mathematical components, none yet credited as the exact theorem, are:

- a finite-dimensional real Euclidean or normed vector space;
- a nonempty compact convex subset `K`;
- a continuous self-map of `K`, represented on the subtype or by an ambient function with a
  preservation condition; and
- existence of an actual `x` in `K` satisfying the fixed-point equation.

## Proposition-changing decisions

The statement phase must freeze all of the following from an approved source rather than from a
textbook convention:

1. The exact edition, theorem/page, incorporated definitions, proof boundary, correction history,
   and independent review.
2. Whether the ambient domain is `R^n`, a finite-dimensional real normed space, a simplex, a closed
   ball, or a general compact convex subset, plus every checked transport between formulations.
3. The dimension encoding and whether dimension zero is included.
4. Whether `K` is explicitly nonempty and how compactness and convexity are expressed.
5. Whether the map is a function on the subtype `K` or an ambient function with `MapsTo f K K`.
6. Whether continuity is global, on `K`, or bundled into a continuous self-map of the subtype.
7. The ordered binders, universe and typeclass assumptions, equality orientation, and the exact
   existential conclusion.
8. The selected foundation, classical-choice, TCB, and computation policies.

These decisions distinguish Brouwer's finite-dimensional theorem from stronger infinite-
dimensional or locally convex fixed-point theorems. They are a resolution ledger, not a canonical
statement.

## Degenerate and mutation cases

Source review must explicitly dispose of empty `K`, singleton `K`, dimension zero, a map that does
not preserve `K`, continuity only on the wrong domain, and replacement of compactness or convexity
by weaker assumptions. It must also distinguish existence from uniqueness, approximation,
computable selection, and convergence of an iteration. No case is silently excluded at intake.

## Duplicate and substitution exclusions

- `THM-M-0319` is a separate Brouwer target in the functional-analysis catalog whose intake chooses
  a finite-dimensional compact-convex formulation. Its scope decision and evidence are not inherited.
- `THM-M-0640` is a separate point-set-topology target whose catalog gloss is the closed-ball form.
  A ball-to-compact-convex transport may later be relevant, but its status and proof credit are not
  shared.
- `THM-M-0637` (Schauder) and `THM-M-0638` (Tychonoff) are stronger neighboring fixed-point
  families and cannot fill the missing ambient assumptions.
- Banach's contraction theorem, Kakutani's set-valued theorem, interval-only fixed-point facts,
  order-theoretic fixed-point theorems, and Kleene's recursion-theoretic theorem are not substitutes.
- A structure or hypothesis containing the desired fixed point, or the catalog label `已验证`,
  supplies no proof credit.

## Formal boundary

No canonical Lean proposition is frozen. Pinned mathlib exposes the component vocabulary checked by
`IntakeProbe.lean`, but availability of those interfaces neither selects the source statement nor
proves a compact-convex fixed-point theorem. Minimal imports, exact expression elaboration,
statement fingerprint, checked alternate encodings, and mutation tests belong to
`S56-M-0636-STATEMENT`.
