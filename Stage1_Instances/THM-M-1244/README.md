# THM-M-1244 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the logarithmic Sobolev inequality. The
metadata phrase "an upper bound for entropy" does not identify a unique theorem, so the intake
selects Gross's Gaussian inequality as the canonical scope. `Statement.lean` now freezes and
elaborates that exact selected target. The source label `已验证` supplies no proof or machine credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Gaussian log-Sobolev inequality with sharp constant `2` | Frozen as `Stage1Instances.THM_M_1244.GaussianLogSobolevTarget` |
| Ambient space | `(Fin n -> Real)` under the product of `gaussianReal 0 1` | Gross's abstract Wiener-space generality is a later transport, not silently part of the root |
| Functions | `ContDiff Real 1`, with explicit integrability of every displayed integrand | No Sobolev-completion extension is credited at this phase |
| Entropy | `Ent_gamma(f^2) = integral f^2 log(f^2) dgamma - m log m`, `m = integral f^2 dgamma` | Conventions at zero and integrability side conditions remain statement obligations |
| Energy | Gaussian integral of the squared Euclidean gradient | Weak-gradient and Dirichlet-form variants are candidate transports only |
| Constant | `Ent_gamma(f^2) <= 2 * integral ||grad f||^2 dgamma` | Normalization depends on standard covariance and must be mutation-tested |
| Out of scope | manifold, discrete, modified, defective, and general-measure LSI families | No result from those families may close this target without checked equivalence |

## Intake verdict

Lifecycle remains `planned`; the statement node is self-tested pending master acceptance. The exact
Lean expression, environment fingerprint, definitional expansion, and four structural mutations
are recorded in `statement.json` and `statement_validation.md`. The human theorem family and a
primary paper are identified, but the original theorem/page assumptions and errata have not been
independently audited. Candidate audit and every proof/release gate remain open; the theorem is not
complete.

The structured claim is in `intake.json`, the source relationship and ambiguity resolution are in
`source_statement_crosswalk.md`, and reproducible intake checks are in `validation.md`.
