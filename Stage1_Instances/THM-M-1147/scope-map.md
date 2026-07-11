# Scope map

## Preserved source scope

- Named family: Kelvin transform.
- Subject: harmonic functions.
- Operation: inversion.
- Attribution/date metadata: William Thomson (Lord Kelvin), 1847.

This is all the mathematical scope fixed by the repository record. The attribution and date have
not been checked against a primary edition and receive no source-fidelity credit.

## Decisions required before statement freeze

The statement phase must identify a primary theorem and freeze: dimension (including treatment of
dimensions one and two), ambient field and Euclidean space, open domain and exclusion of the
inversion center, inversion center/radius, the exact weight and normalization, the meaning of
harmonicity and differentiability assumptions, and whether the conclusion is pointwise harmonicity
on the inverted domain or a Laplacian covariance identity. It must state behavior at zero, empty
domains, disconnected domains, constant/zero functions, and any extension across infinity.

## Candidate shape, not adopted

For dimension `n >= 3`, a standard unit-centered candidate maps `u` to
`x |-> |x|^(2-n) * u (x / |x|^2)` away from zero and asserts preservation of harmonicity on the
inverted domain. Dimension two has weight one; other radii and centers alter the formula. These
inequivalent choices demonstrate why the metadata phrase alone cannot freeze the target.

## Explicit exclusions

- Choosing the unit-centered `n >= 3` formula merely because it is familiar.
- Substituting geometric inversion alone, a fundamental-solution identity, conformal invariance in
  dimension two, or a harmonic-polynomial transform for the source theorem.
- Treating `已验证`, the attribution, or a future mathlib name as proof/source evidence.
