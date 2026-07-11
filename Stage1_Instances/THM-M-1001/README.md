# THM-M-1001 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the martingale convergence theorem
(`鞅收敛定理`). It inherits no proof credit from the Stage0 status label `已验证`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | A discrete-time real-valued martingale convergence theorem with an almost-sure conclusion | The source record omits the indispensable boundedness/integrability hypothesis and the mode and codomain of the limit |
| Candidate classical readings | an `L¹`-bounded submartingale converges almost surely to an integrable finite limit; a nonnegative supermartingale converges almost surely | These are distinct standard theorems, not interchangeable restatements |
| Process objects | probability space, filtration, adapted measurable integrable random variables indexed by `Nat` | Exact Lean object model belongs to the dependent statement phase |
| Conclusion | pointwise convergence on an almost-everywhere set, with the limit's measurability/integrability specified | No convergence mode beyond the source phrase "almost surely" may be added silently |
| Exclusions | continuous-time variants, `Lᵖ` convergence, uniform-integrability equivalences, stopping-time and stochastic-integral theorems | Each requires a separately sourced statement or checked transport |
| Foundations | Lean 4 kernel and pinned mathlib, with classical/choice and measure-theory dependencies audited | Environment and TCB fingerprints remain open |

The canonical source statement cannot yet be frozen without inventing missing mathematics. The
crosswalk therefore preserves the ambiguity and records the exact source work needed to select one
root. No downstream statement, anchor, proof, or theorem-completion credit is claimed.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M4, R3]`. The first failed gate is exact
source-statement identification. The dossier, scope map, and crosswalk are complete for intake, but
the theorem is not complete and the dependent statement phase must remain fail-closed until the
integration lane selects a primary-source theorem with all assumptions.

