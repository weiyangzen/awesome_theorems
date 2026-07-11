# THM-M-1157 rev-5.6 intake

This directory is the `planned` intake for **Newton potential**. The repository source calls it
`gravitational potential`, but gives no mathematical proposition. A potential is an object or
construction, not by itself a theorem. Consequently the exact claim cannot be frozen without
choosing mathematics absent from the source record.

## Scope map

| Surface | Candidate scope | Intake boundary |
|---|---|---|
| Point-mass potential | `Phi(x) = -Gm / dist x x0` away from the source | A definition; no requested conclusion is recorded |
| Distributed mass | Newtonian kernel convolved with a density or measure | Domain, dimension, integrability, normalization, and conclusion are absent |
| Poisson equation | A distributional or classical identity such as `Delta Phi = c * rho` | Sign and constant depend on conventions; regularity and boundary hypotheses are absent |
| Shell theorem | Exterior field equals that of a point mass; interior field vanishes | Requires spherical symmetry and is a distinct theorem not named by the record |
| Analytic properties | Harmonicity off support, decay, regularity, or uniqueness | Each is a different theorem with different hypotheses |
| Lean foundation | Euclidean geometry, measure/integration, convolution, derivatives, or distributions | No module or expression may be selected before the claim is disambiguated |

The statement phase must select one proposition by a pinpoint source anchor and preserve its domain,
constants, hypotheses, conclusion, and boundary cases. It must not silently substitute the shell
theorem, Poisson equation, or harmonicity merely because one is easier to encode.

## Intake verdict

Lifecycle is `planned`; root vector is `[H5, M4, R4]`. The first failed gate is exact source
statement identification. This intake is nevertheless self-tested as an honest scope dossier: it
freezes the ambiguity and the permitted candidate surfaces without claiming theorem completion.

## Open task DAG

1. `S56-M-1157-STATEMENT`: identify a primary-source proposition and elaborate its exact Lean target.
2. `S56-M-1157-ANCHOR_AUDIT`: audit mathlib and external candidates only after statement identity.
3. `S56-M-1157-OBLIGATION_TREE`: freeze typed obligations and graphs before observing closure.
4. `S56-M-1157-PROOF`: implement or integrate exact proof bodies.
5. `S56-M-1157-VALIDATION`: run kernel, trust, provenance, and independent checks.
6. `S56-M-1157-RELEASE`: independently decide audit and theorem completion.

Exact commands and results for the smallest intake validation appear in `validation.md`.
