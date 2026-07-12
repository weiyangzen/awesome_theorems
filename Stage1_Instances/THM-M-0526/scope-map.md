# Scope map

## Included claim

- A topological space `X` with two open subspaces `U` and `V` satisfying `X = U union V`.
- A basepoint `x0` lying in `U intersection V`.
- Path-connectedness of `U`, `V`, and `U intersection V`, so all four based fundamental groups
  and inclusion-induced homomorphisms use the same basepoint without change-of-basepoint choices.
- The commuting square induced by the inclusions of `U intersection V` into `U` and `V`.
- The universal conclusion that this square is a pushout in groups, with apex
  `pi_1(X, x0)`.
- As a checked alternate encoding only: the canonical map from the free product
  `pi_1(U,x0) * pi_1(V,x0)` onto `pi_1(X,x0)` is surjective and has kernel the normal closure of
  the relations identifying the two images of every element of `pi_1(U intersection V,x0)`.

## Statement-phase decisions

The next phase must select and inspect one exact source statement and then freeze its ordered
binders and hypotheses. It must decide whether `U` and `V` are represented as sets, subspaces, or
open embeddings; how `X = U union V` is encoded; which path-connected predicate is used; the
fundamental-group and categorical-pushout APIs; and whether the source states the universal
property or the free-product quotient. It must also test the empty-space boundary (excluded by the
basepoint), `U = X`, `V = X`, trivial intersection group, and coincident cover members.

The formal target must map the inclusion-induced arrows and their equality after composition to
the literal source diagram. A group isomorphism without the commuting maps and universal property
does not by itself express the pushout claim.

## Explicit exclusions

- The fundamental groupoid theorem for a cover with disconnected intersection as a broadened
  replacement; it may later be a proof dependency only if a checked specialization is provided.
- A version for an arbitrary family of open sets, a CW-complex cell-attachment corollary, or a
  computation of the fundamental group of one example.
- The weaker assertion that the inclusion maps merely generate `pi_1(X,x0)`.
- An abstract structure or hypothesis that already contains the desired pushout/isomorphism.
- Any unbased formulation unless a checked bridge proves it is the selected based source claim.

No Lean declaration is selected or credited at intake. Absence or presence of a suitable pinned
mathlib theorem must be established by the later anchor audit, not inferred from theorem names.
