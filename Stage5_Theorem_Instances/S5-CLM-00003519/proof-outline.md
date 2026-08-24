# Proof outline — the diagonal copy of S₂ is cyclic

Let `τ` be the transposition of the two elements of `Fin 2`, and let
`g = (τ, τ)`. Its two coordinates have the same sign, so `g` belongs to
`gammaSubgroup 2 2`.

Every permutation of a two-element type is either the identity or `τ`. Thus a
pair of such permutations has four apparent forms. Membership in
`gammaSubgroup` says that the two signs agree; it rules out exactly the two
mixed forms `(1, τ)` and `(τ, 1)`. Every subgroup element is consequently either
the identity pair or `g`.

The closure of `{g}` contains the identity because it is a subgroup, and it
contains `g` by the defining inclusion into a generated closure. Hence it
contains every element of `gammaSubgroup 2 2`, so it is the top subgroup.
