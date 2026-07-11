# THM-M-1042 rev-5.6 intake

This is the `planned` rev-5.6 instance for Dynkin's formula. The blueprint's short gloss,
"generator of a Markov process," does not specify one of the several formulas carrying this name.
The intake freezes the intended family at the standard stopped continuous-time identity, while
leaving the exact source hypotheses to the dependent statement and source-audit phases.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | The stopped expectation identity `E_x f(X_tau) = f(x) + E_x integral_0^tau A f(X_s) ds` | Exact process regularity, generator domain, and stopping-time conditions require a pinned source variant |
| Objects | Measurable state space, continuous-time Markov process, initial law/state, generator, stopping time, integrable observable | No Lean object model or universe choices are credited |
| Analytic layer | Measurability, generator-domain membership, Bochner/Lebesgue integral, integrability and localization | All interfaces remain open obligations |
| Probabilistic layer | Markov property, filtration/adaptedness, martingale construction, optional stopping | No theorem anchor or proof closure is claimed |
| Specializations | Deterministic time and bounded stopping times | Useful tests, never substitutes for the root |
| Exclusions | Discrete-time sum identity, Ito's formula, Feynman-Kac, and a semigroup derivative alone | Related results do not discharge this target |

The statement phase must select a primary-source formulation without silently dropping its domain,
regularity, boundedness, or integrability assumptions. It must then elaborate an exact Lean target
and test `tau = 0`, deterministic `tau = t`, constant `f`, and an unbounded stopping-time mutation.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed theorem gate is
the exact-statement gate: the available repository source gives only a name and gloss, and no Lean
declaration, environment fingerprint, or checked transport exists. The theorem is not complete.

Validation evidence is recorded in `validation.md` and establishes only manifest membership,
standard consistency, JSON syntax, and dossier-local integrity.
