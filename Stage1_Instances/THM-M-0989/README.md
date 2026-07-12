# THM-M-0989 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Lindeberg-Feller central limit theorem. It
does not inherit proof credit from the source label `已验证`. The source metadata only says
"central limit theorem for independent, non-identically distributed variables"; it does not select
one of the row, infinitesimal-array, or converse formulations commonly bearing this name.

The statement phase freezes the forward variance-normalized triangular-array form in
`Statement.lean`. Row `n` has `n + 1` entries, its total variance is exactly one, and the summed
truncated second moments tend to zero for every positive threshold. The checked
`statement_iff` witness exposes the transparent binder form. This is kernel-checked statement
elaboration, not a proof of the Lindeberg-Feller theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | A triangular array of independent, centered real random variables whose row variances sum to one; the Lindeberg condition implies convergence in distribution of row sums to the standard Gaussian | Frozen as `Stage1Instances.THM_M_0989.Statement` |
| Probability objects | probability space, measurable real random variables, expectation, variance, finite row sums, laws | No measurability or integrability obligation is credited here |
| Lindeberg hypothesis | for every positive epsilon, the sum of truncated second moments tends to zero | Frozen using a real integral and `Tendsto ... atTop (nhds 0)` |
| Conclusion | row-sum laws converge weakly/in distribution to `N(0,1)` | Frozen with `TendstoInDistribution` and `gaussianReal 0 1` |
| Converse | equivalence with the Lindeberg condition under a uniform-asymptotic-negligibility/Feller condition | Excluded from the provisional root until the source audit resolves which named form is authoritative |
| Foundations | Lean 4 kernel and pinned mathlib, using classical probability and integration APIs | Toolchain/import fingerprints recorded for elaboration; transitive trust and TCB audit remain open |

The future proof architecture must at least expose array independence, centering and square
integrability, variance normalization, Lindeberg truncation, characteristic-function or imported
CLT bridge, and weak-convergence composition. These are scope seeds, not frozen obligations.

## Intake verdict

Lifecycle remains `planned`; provisional root vector is `[H2, M3, R3]`. `H2` records that standard
pinpoint references have been located but the historical naming and converse variants have not been
audited. `M3` records an exact elaborated statement without a proof body. The first failed theorem
gate is the source/anchor audit, followed by proof closure. The theorem is not complete.
