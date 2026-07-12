# Scope map

## Included root

- The first/absolute Hurewicz theorem in degree `n >= 2`.
- A pointed, path-connected space `X` with `pi_i(X) = 0` for `1 <= i < n`, equivalently an
  `(n-1)`-connected space once the exact convention is fixed.
- Vanishing reduced integral homology below `n`.
- The canonical Hurewicz homomorphism `pi_n(X) -> H_n(X; Z)` being an isomorphism.

The conjunction of lower-homology vanishing and the degree-`n` isomorphism is intentional. A Lean
target proving only one half is narrower than this intake.

## Statement-phase decisions

The source audit must decide whether the exact theorem assumes a CW complex, an arbitrary space,
or a space with an implicit local niceness condition; whether connectivity is stated by vanishing
homotopy groups or sphere extension; and whether `H_n` is reduced or unreduced in the displayed
map. It must also freeze basepoint handling, the `n = 2` nonabelian-to-abelian interface, all degree
binders, universe levels, and the concrete coefficient object `Z`.

## Explicit exclusions

- The `n = 1` result that `pi_1(X) -> H_1(X; Z)` is abelianization. It may later be a separately
  represented boundary node, but cannot replace the selected root.
- Relative Hurewicz, generalized-homology, rational, stable, or homology-equivalence theorems.
- Whitehead's theorem or the statement that weak equivalences induce homology isomorphisms.
- A mere existence of some isomorphism rather than the canonical Hurewicz map.
- An abstract package or hypothesis containing the desired vanishing/isomorphism conclusion.

## Known formal surface

The pinned mathlib source search found the word `Hurewicz` only in
`Mathlib/Topology/Homotopy/Lifting.lean`, where it refers to Hurewicz fibrations, not the homotopy-
to-homology theorem. This is an intake observation, not a complete anchor audit or proof of API
absence. The statement phase must locate concrete homotopy-group, singular-homology, and map APIs
before it can claim elaboration.
