# THM-M-1046 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Novikov's condition. The Stage0 label
`已验证` and the generated Stage1 description are discovery inputs only; neither supplies proof
credit or an accepted machine state.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | finite-horizon continuous-local-martingale form of Novikov's sufficient condition | Exact Lean binders and expression fingerprint belong to the statement phase |
| Data | filtered probability space, finite horizon `T`, real continuous local martingale `M` with `M₀ = 0`, quadratic variation `⟪M⟫` | Lean object model and measurability/usual-condition assumptions remain to be selected |
| Hypothesis | `E[exp((1/2) ⟪M⟫_T)] < infinity` | Extended-real versus Bochner-integrability encoding remains open |
| Conclusion | the stochastic exponential `exp(M_t - (1/2) ⟪M⟫_t)` is a martingale on `[0,T]` (and hence has expectation one) | Whether to state uniform integrability of the stopped family is an alternate/strengthened form requiring checked transport |
| Alternate scope | Brownian stochastic-integral/Girsanov integrand formulation | Candidate corollary only; it cannot substitute for the canonical root |
| Degenerate cases | `T = 0`, zero martingale, finite quadratic variation forced by exponential integrability | Boundary behavior must be mutation-tested later |
| Foundations | Lean 4 kernel, pinned mathlib, classical/choice policy, stochastic-integration dependencies | Exact TCB and dependency closure are open |

The initial architecture is: probability/filtration objects; continuous local martingale and
quadratic variation; stochastic exponential; exponential-integrability hypothesis; localization
and uniform-integrability argument; martingale conclusion. This is scope, not a frozen obligation
registry and not a proof tree.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the Lean statement gate: no canonical declaration has been elaborated, and the available repository
metadata does not identify a Lean API for continuous local martingales, quadratic variation, or the
stochastic exponential. The theorem is not complete.

The structured claim is in `intake.json`, its human-source mapping is in
`source_statement_crosswalk.md`, and the self-test evidence is in `validation.md`.
