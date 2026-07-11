# THM-M-0989 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Lindeberg-Feller central limit theorem. It
does not inherit proof credit from the source label `已验证`. The source metadata only says
"central limit theorem for independent, non-identically distributed variables"; it does not select
one of the row, infinitesimal-array, or converse formulations commonly bearing this name.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | A triangular array of independent, centered real random variables whose row variances sum to one; the Lindeberg condition implies convergence in distribution of row sums to the standard Gaussian | Provisional canonical claim; exact Lean binders and normalization belong to the statement phase |
| Probability objects | probability space, measurable real random variables, expectation, variance, finite row sums, laws | No measurability or integrability obligation is credited here |
| Lindeberg hypothesis | for every positive epsilon, the sum of truncated second moments tends to zero | Encoding of truncation and convergence remains open |
| Conclusion | row-sum laws converge weakly/in distribution to `N(0,1)` | The exact mathlib convergence interface remains open |
| Converse | equivalence with the Lindeberg condition under a uniform-asymptotic-negligibility/Feller condition | Excluded from the provisional root until the source audit resolves which named form is authoritative |
| Foundations | Lean 4 kernel and pinned mathlib, with classical probability and integration dependencies audited | Toolchain, imports, trust dependencies, and TCB fingerprint remain open |

The future proof architecture must at least expose array independence, centering and square
integrability, variance normalization, Lindeberg truncation, characteristic-function or imported
CLT bridge, and weak-convergence composition. These are scope seeds, not frozen obligations.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. `H2` records that standard
pinpoint references have been located but the historical naming and converse variants have not been
audited. `M4` records that no exact Lean declaration or elaborated signature is identified. The
first failed theorem gate is the exact-statement gate. The theorem is not complete.
