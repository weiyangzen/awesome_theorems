# Scope map

## Candidate theorem family

The following boundary is a source-selection candidate, not the canonical claim:

- a nonempty closed bounded convex subset of a finite-dimensional real Euclidean space;
- a set-valued map whose values are contained in the domain;
- nonempty closed convex values;
- the source's upper-semicontinuity condition; and
- a conclusion of the form `exists x in K, x in F x`.

This is the natural reading of the catalog label and 1941 attribution, but the received record does
not contain these premises. The statement phase must admit and independently inspect an immutable
source passage before freezing them.

## Proposition-critical decisions

The exact statement must decide all of the following rather than inheriting a convenient modern
variant:

1. Euclidean space versus an abstract finite-dimensional real topological vector space.
2. Closed and bounded versus compact domain, and the exact nonemptiness premise.
3. Closed versus compact values and whether containment in the domain is part of the map's type or
   a separate hypothesis.
4. Kakutani's point-set-function semicontinuity definition versus mathlib's
   `UpperHemicontinuousOn`, including every hypothesis needed for a checked transport.
5. Ambient `F : E -> Set E` versus a subtype correspondence `K -> Set K`.
6. Ordered binders, universe and typeclass context, and whether dimension zero is included.
7. Empty domains or values, singleton domains, boundary points, and values escaping the domain.
8. Whether a closed-graph formulation is equivalent in the selected compact/Hausdorff setting or
   is only a distinct theorem candidate.

## Explicit exclusions

- Brouwer's single-valued theorem, Schauder's theorem, Tychonoff's theorem, and the
  Markov-Kakutani commuting-map theorem.
- Infinite-dimensional, locally convex, game-theoretic, or equilibrium generalizations absent an
  approved source selection.
- Approximate fixed points, a fixed point of a chosen continuous selection, or membership only in
  a convex hull.
- A structure or hypothesis containing a chosen fixed point or otherwise assuming the conclusion.
- Riesz-Markov-Kakutani representation theorems and Kakutani towers.
- Importing any assurance or proof credit from the duplicate-title target `THM-M-0320`.
- Treating the catalog's `verified` label as human-source or kernel evidence.

No exact formal target or degenerate-case exclusion is frozen by this intake.
