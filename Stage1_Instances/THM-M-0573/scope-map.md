# Scope map

## Included subject boundary

- A compact group `G` acting smoothly on a compact smooth manifold `M`.
- `G`-equivariant complex vector bundles over `M` and a `G`-equivariant elliptic operator between
  their section spaces.
- The analytic equivariant index, represented by the virtual `G`-representation
  `[ker D] - [coker D]`, once the functional-analytic hypotheses making these finite-dimensional
  representations are fixed.
- The topological equivariant index obtained from the equivariant symbol class and a topological
  pushforward, if this is the selected source theorem.
- Character evaluation at `g : G` and contributions from the fixed locus `M^g` only if the source
  statement selected for the root includes the fixed-point formula.

These bullets are a subject map, not a fully quantified theorem and not accepted proof obligations.

## Exact-statement decisions

"G-index theorem" is not a unique proposition. The statement phase must use an inspected primary
source to decide whether the root is:

1. equality of analytic and topological equivariant indices in the representation ring `R(G)`;
2. the corresponding equality of character values for every `g : G`; or
3. a fixed-point formula expressing a character value as local data on `M^g`.

It must also freeze the group category, operator class, smoothness and compactness hypotheses,
boundary convention, real/complex convention, symbol and pushforward model, fixed-locus regularity,
and all characteristic-class normalizations. These variants cannot receive mutual proof credit
without checked transports.

## Explicit exclusions

- The nonequivariant Atiyah-Singer theorem obtained by replacing `G` with the trivial group.
- The Atiyah-Bott fixed-point theorem as an automatic substitute for the representation-ring
  index equality.
- A numerical equality of dimensions that discards the `G`-representation or its character.
- An abstract structure carrying the desired analytic/topological equality as an assumed field.
- Generic mathlib group actions, manifolds, or Euler characteristics as evidence for the terminal
  equivariant index theorem.

The identity element, trivial action, empty fixed locus, free action, disconnected manifold, and
zero-dimensional cases remain mandatory statement mutations or boundary checks rather than
implicit exclusions.
