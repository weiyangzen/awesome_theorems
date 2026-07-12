# Scope map

## Included theorem family

- A topological space `X` equipped with a CW-complex structure and skeletal filtration `X^n`.
- Cellular chain groups constructed from consecutive skeleta, classically
  `C_n(X; R) = H_n(X^n, X^(n-1); R)`.
- Differentials induced by the connecting morphisms for triples of skeleta, with the usual
  inclusion/identification maps.
- A chain-complex comparison whose induced homology is naturally isomorphic to singular homology
  of `X` with the same coefficients.
- The free-module basis indexed by `n`-cells and the attaching-map degree formula only if they are
  present in the selected source theorem or are registered as separate refinement obligations.

This is the standard mathematical interpretation of the repository phrase "CW complex homology
computation". It freezes a theorem family, not an exact formal proposition.

## Statement-phase decisions

The next phase must inspect a stable source and freeze: absolute or relative CW complexes; arbitrary
or finite-type complexes; coefficient group or commutative ring; reduced or unreduced theory;
natural-number or integer grading; definitions of the negative and degree-zero skeleta; the exact
cellular differential; whether the conclusion is a group/module isomorphism in each degree or a
natural isomorphism of graded objects; and the hypotheses needed for an infinite CW complex.

It must also decide whether "cellular homology" names the construction, the cellular-versus-singular
comparison theorem, or the stronger calculation package including free generators and incidence
numbers. These forms are related but cannot share one proof claim without checked transports.

## Explicit exclusions

- Defining a chain complex and then assuming that its homology is singular homology.
- Proving only that cellular chains form a complex (`d^2 = 0`).
- Substituting simplicial homology, singular homology, or the homology of one example.
- Replacing the comparison isomorphism by an equality of ranks or Euler characteristics.
- Treating mathlib's CW-complex definitions and singular-homology functor as a terminal theorem.
- Treating the manifest's untrusted `已验证` label as source or kernel evidence.

No obligation denominator or proof architecture is frozen at intake. Those require the exact source
statement and a formal-candidate audit.
