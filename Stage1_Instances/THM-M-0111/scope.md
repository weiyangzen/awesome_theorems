# Scope map

## Included claim

The target is the analytic Kodaira embedding theorem: for a compact,
finite-dimensional complex manifold `X`, the existence of a Kahler form with
integral de Rham class implies the existence of a holomorphic embedding of `X`
into `CP^n` for some finite `n`.

The statement phase must expose the manifold structure, compactness, Kahler
form, comparison map from integral to real/de Rham cohomology, dimension, and
holomorphic embedding. Universes and typeclass binders must be explicit. It
must also decide connectedness and the conventional `2*pi` normalization.

## Exclusions

- The converse (a projective manifold is Kahler/Hodge).
- Chow's theorem and the assertion that a closed analytic subspace of
  projective space is algebraic.
- The algebraic-scheme ample-line-bundle criterion unless checked transports
  connect it to the analytic claim.
- Abstract predicates such as `compactComplexManifold : Prop` or
  `ambientIsProjectiveSpace : Prop` as substitutes for native structures.
- A supplied embedding package, wrapper implication, or statement equality as
  proof of the existence theorem.

## Required transports

Later work may use the positive holomorphic line-bundle formulation, but must
check both bridges: integral Kahler class to a positive line bundle, and enough
sections of a tensor power to a holomorphic projective embedding. Any algebraic
projectivity formulation needs a checked analytic/algebraic comparison.

## Mutation obligations for the statement node

Reject variants dropping compactness, complex structure, Kahler positivity,
or integrality. Reject a conclusion giving only a continuous map, holomorphic
map, immersion, or non-closed injection. Test zero-dimensional and disconnected
inputs rather than silently strengthening the domain.
