# Scope map

## Preserved catalog scope

The intake preserves the catalog's finite-dimensional Euclidean Heine-Borel family: for subsets
of real `n`-space, compactness is equivalent to being closed and bounded. A conventional candidate,
not yet credited as the canonical statement, quantifies over `n : Nat` and
`s : Set (EuclideanSpace Real (Fin n))` and concludes
`IsCompact s <-> IsClosed s and Bornology.IsBounded s`.

## Proposition-changing decisions

The statement phase must freeze all of the following from an admitted source rather than silently
choosing a convenient library generalization:

1. Whether `n` ranges over all natural numbers, only positive integers, or is fixed in advance.
2. Whether `R^n` is encoded as `EuclideanSpace Real (Fin n)`, `Fin n -> Real`, a product, or an
   arbitrary finite-dimensional real normed space connected by a checked specialization.
3. Whether boundedness means metric/bornological boundedness, coordinatewise two-sided bounds, or
   containment in a ball, and which checked transports connect credited alternatives.
4. The exact order of the equivalence and conjunction, ordered binders, universes, implicit
   topology and norm structures, and any nonemptiness assumptions.
5. Whether the source says "closed and bounded implies compact," the full equivalence, or both via
   separately incorporated general facts that compact subsets of Euclidean space are closed and
   bounded.
6. The source edition, theorem/page, incorporated definitions, proof boundary, historical
   attribution, translation, correction or errata record, and independent review.
7. The foundation, classical-choice, TCB, computation, and freshness profiles for the selected
   expression and minimal imports.

## Boundary and mutation cases

The empty set, singleton sets, finite sets, unbounded closed sets, bounded nonclosed sets, open and
closed balls, and all of `R^n` must be handled by the selected statement rather than excluded for
proof convenience. The `n = 0` space is a proposition-critical boundary: it is valid under the
usual all-natural-numbers formulation but may lie outside a source convention that assumes
positive dimension.

Statement mutations must reject a missing closedness or boundedness premise in the reverse
direction, a changed carrier such as an infinite-dimensional normed space, a binder that fixes only
one subset or one dimension, and replacements of compactness by sequential compactness without a
checked equivalence.

## Explicit exclusions

- The generalized proper-space theorem cannot silently replace the literal `R^n` root; it is a
  candidate source of a checked specialization.
- The one-way `Metric.isCompact_of_isClosed_isBounded` cannot replace the catalog's equivalence.
- Sequential compactness, total boundedness plus completeness, local compactness, compact closure
  of a bounded set, and Bolzano-Weierstrass may be dependencies or checked transports, not
  substitute targets.
- A theorem only for intervals, boxes, balls, `R`, a fixed positive dimension, or finite sets does
  not close the universal catalog family unless the accepted source selects that scope.
- A `ProperSpace` instance, theorem name, successful `#check`, or hypothesis already containing
  compactness supplies no root proof credit.
- The untrusted `已验证` catalog label supplies neither human-source nor kernel evidence.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.MetricSpace.Bounded` explicitly documents
`Metric.isCompact_iff_isClosed_bounded` as Heine-Borel in proper Hausdorff spaces, while
`Mathlib.Analysis.Normed.Module.FiniteDimension` provides `FiniteDimensional.proper`. The direct
interface warrants provisional `M3`, not M0. Source-approved carrier selection, minimal imports,
the exact expression and environment fingerprints, checked specialization, mutation tests,
terminal proof-body provenance, transitive dependencies, axiom policy, and trust closure remain
downstream.
