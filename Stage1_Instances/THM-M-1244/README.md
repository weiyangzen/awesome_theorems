# THM-M-1244 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the logarithmic Sobolev inequality. The
metadata phrase "an upper bound for entropy" does not identify a unique theorem, so this intake
selects Gross's Gaussian inequality as the canonical scope and records the remaining statement
work explicitly. The source label `已验证` supplies no proof or machine credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Gaussian log-Sobolev inequality with sharp constant `2` | The precise Lean representation and elaborated expression belong to the statement phase |
| Ambient space | finite-dimensional standard Gaussian probability space as the first formal target | Gross's abstract Wiener-space generality is a later transport, not silently part of the root |
| Functions | sufficiently regular real functions with square-integrable gradient and entropy | The exact measurable/Sobolev predicate must be frozen in Lean |
| Entropy | `Ent_gamma(f^2) = integral f^2 log(f^2) dgamma - m log m`, `m = integral f^2 dgamma` | Conventions at zero and integrability side conditions remain statement obligations |
| Energy | Gaussian integral of the squared Euclidean gradient | Weak-gradient and Dirichlet-form variants are candidate transports only |
| Constant | `Ent_gamma(f^2) <= 2 * integral ||grad f||^2 dgamma` | Normalization depends on standard covariance and must be mutation-tested |
| Out of scope | manifold, discrete, modified, defective, and general-measure LSI families | No result from those families may close this target without checked equivalence |

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The human theorem family and a
primary paper are identified, but the original theorem/page assumptions and errata have not been
independently audited. The first failed theorem gate is exact-statement elaboration: no Lean module,
declaration, normalized expression hash, checked transports, or mutation evidence exists. This
intake is complete as an intake node only; the theorem is not complete.

The structured claim is in `intake.json`, the source relationship and ambiguity resolution are in
`source_statement_crosswalk.md`, and reproducible intake checks are in `validation.md`.
