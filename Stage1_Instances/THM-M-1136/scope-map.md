# Scope map

## Preserved source scope

- Subject: a function described as harmonic.
- Governing relation: it is a solution of Laplace's equation, conventionally expressed as a
  vanishing Laplacian.
- Historical scope: eighteenth century and attributed only to "many mathematicians".
- Logical character: the wording is a characterization or definition, not a specified consequence.

Nothing in the repository source fixes a theorem beyond this scope.

## Decisions required before statement freeze

The statement phase must identify a primary mathematical source and determine whether the intended
claim is a definition, an `iff`, or one implication. It must freeze the ambient dimension and scalar
field, open domain, function codomain, differentiability class, classical/weak/distributional
solution notion, Laplacian convention, pointwise or setwise quantification, and boundary behavior.
It must also account for empty domains, dimension zero, disconnected domains, and constant
functions where those cases are admitted.

## Explicit exclusions

- Mean-value, maximum-principle, analyticity, Liouville, Harnack, or Poisson results merely because
  they concern harmonic functions; those are distinct neighboring targets.
- A tautology produced by defining `IsHarmonic u` to be the desired equation and proving it by
  reflexivity without establishing that this is the sourced claim.
- Complex harmonicity, manifolds and the Laplace-Beltrami operator unless a source selects them.
- The untrusted metadata label `已验证` as source or kernel evidence.

