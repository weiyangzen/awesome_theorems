# THM-M-1032 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Ito formula. Historical Stage0 prose and
the legacy `S1_M_225.lean` module are discovery inputs only; neither supplies accepted proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact human root | finite-dimensional continuous-semimartingale Ito formula for a scalar `C^2` function | The terse source record does not choose a unique variant; the statement phase must freeze time interval, regularity, and integral conventions |
| Processes | an `R^d`-valued continuous semimartingale `X`, its coordinates, and quadratic covariations | Brownian, one-dimensional, stopped, and time-dependent versions are specializations or later transports, not substitutes |
| Identity | `f(X_t)-f(X_0)` equals first-order stochastic integrals plus one half of the Hessian integrated against coordinate quadratic covariations | Every stochastic-integral and covariation object remains an uncredited candidate interface |
| Degenerate cases | `t = 0`, constant/affine `f`, dimension zero or one, and finite-variation paths | Required mutation and boundary probes; none is excluded silently |
| Lean surface | candidate declarations in `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_225.lean` | Legacy interfaces are not canonical and have no rev-5.6 statement credit |
| Foundations | Lean 4 kernel and pinned mathlib with an explicit classical/choice/quotient policy | Exact toolchain, imports, dependency closure, and TCB fingerprint remain open |

The scope intentionally does not broaden the theorem to a generic phrase such as "chain rule for
stochastic processes": arbitrary stochastic processes do not satisfy this formula. The structured
claim and its unresolved choices are recorded in `intake.json`; the source relationship is recorded
in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The source statement is too
underspecified to identify one exact Lean proposition without mathematical choices, so the first
failed gate is exact-statement identification. This is an actionable statement-phase blocker, not a
claim that the Ito formula is unformalizable. The theorem is not complete.

## Validation

The commands and exact intake-level results are in `validation.md`. They establish target
membership, repository-standard consistency, JSON syntax, and dossier integrity only. No Lean
declaration was added or kernel proof claimed.
