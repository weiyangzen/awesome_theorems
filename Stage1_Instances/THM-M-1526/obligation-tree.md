# THM-M-1526 frozen obligation architecture

Item: `S56-M-1526-OBLIGATION_TREE`. Registry version: 1. Freeze date: 2026-07-12.

The denominator contains 17 canonical obligations fixed from the elaborated statement and bounded
anchor audit before proof execution. Fifteen are machine-required, twelve require human-source
mapping, and all seventeen require readable accounts. The exact root remains `M3` because no
terminal factorization proof body exists locally or in the audited external candidates.

<a id="m1526-root"></a>
## M1526-ROOT

The root is exactly `FreeDiracFactorizationTarget`: for every finite constant-coefficient family
satisfying the frozen Clifford and commutation hypotheses, the two conjugate first-order factors
compose to `kleinGordon D - D.mass ^ 2`, and every vector killed by the right factor is killed by
that second-order operator.

## Statement layer

<a id="m1526-s-definitions"></a> `M1526-S-DEFINITIONS` owns `slash` and `kleinGordon`.
<a id="m1526-s-domain"></a> `M1526-S-DOMAIN` owns the finite index, complex module, universe, and
endomorphism context. <a id="m1526-s-boundary"></a> `M1526-S-BOUNDARY` retains zero mass, empty
index types, and zero spinor spaces. <a id="m1526-s-transport"></a> `M1526-S-TRANSPORT` is the
checked equivalence to `DirectConsequenceShape`. <a id="m1526-s-foundation"></a>
`M1526-S-FOUNDATION` keeps the transitive axiom and TCB audit open.

## Algebraic core

<a id="m1526-n-product"></a> `M1526-N-PRODUCT` cancels scalar cross terms in the product of the
conjugate factors. <a id="m1526-c-pair-split"></a> `M1526-C-PAIR-SPLIT` owns a duplicate-free
partition of the double sum into diagonal terms and unordered off-diagonal pairs.

<a id="m1526-l-slash-square"></a> `M1526-L-SLASH-SQUARE` is the central identity
`slash D * slash D = kleinGordon D`. It is split-required rather than hidden behind ring or sum
automation. <a id="m1526-l-diagonal"></a> `M1526-L-DIAGONAL` applies the diagonal Clifford law.
<a id="m1526-l-offdiagonal"></a> `M1526-L-OFFDIAGONAL` moves the constant gamma maps past the
commuting derivatives, pairs swapped indices, and applies the polarized Clifford law.

## Terminal composition

<a id="m1526-t-factor"></a> `M1526-T-FACTOR` combines product normalization with slash-square
identification. <a id="m1526-t-consequence"></a> `M1526-T-CONSEQUENCE` applies that equality to a
vector killed by the right factor. <a id="m1526-t-assemble"></a> `M1526-T-ASSEMBLE` is checked in
`ObligationTree.lean`: `root_of_factorization` consumes the exact open `FactorizationPackage`,
derives the consequence by application and `map_zero`, and returns the canonical conjunction.
The premise remains open, so the declaration provides composition evidence only.

## Boundaries

<a id="m1526-x-mathlib"></a> `M1526-X-MATHLIB` owns the pinned finite-sum, endomorphism, matrix,
and Clifford support boundary. It cannot earn terminal proof credit. <a id="m1526-x-source"></a>
`M1526-X-SOURCE` owns the open pinpoint historical-source crosswalk. <a id="m1526-x-provenance"></a>
`M1526-X-PROVENANCE` owns wrapper/body provenance and is informational rather than an independent
proof obligation.

## Closure boundary

The minimal root cut set is `M1526-N-PRODUCT` plus `M1526-L-SLASH-SQUARE`; the latter expands into
the pair partition and diagonal/off-diagonal lemmas. The registry and separate proof, refinement,
provenance, evidence, trust, documentation, and workflow graphs are frozen and self-tested. No
factorization proof, source-fidelity promotion, validation release, or theorem completion is claimed.
