# Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Exact root | Markov property for the solution family of a well-posed time-homogeneous Itô SDE | Exact coefficient class, uniqueness notion, and conditional identity await source audit |
| State equation | `dX_t = b(X_t) dt + sigma(X_t) dW_t`, initially finite dimensional and nonexplosive | General manifolds, jumps, SPDEs, and path-dependent coefficients are excluded from the root |
| Well-posedness | existence from every initial state plus the uniqueness strength required to restart the equation | Lipschitz/linear-growth assumptions are a sufficient candidate, not yet frozen as the only formulation |
| Markov conclusion | deterministic-time conditional law/expectation depends only on `X_s`; transition semigroup/kernel formulation | Strong Markov at stopping times is not credited as equivalent without a checked derivation and filtration hypotheses |
| Filtration | filtration supporting Brownian motion and the adapted solution, with conditioning convention explicit | natural versus augmented filtration and completion/right-continuity must be reconciled |
| Boundary branches | deterministic noise, random initial condition, `s = t`, killed/explosive processes | nonunique weak solutions require a selected Markov family and do not follow from the provisional root |
| Formal system | Lean 4 and pinned mathlib measure/probability APIs | no existing exact declaration or local Lean wrapper has been identified or credited |

Future statement work must choose one exact conditional-expectation or kernel
identity, freeze all binders and measurability assumptions, and provide checked
transports to any alternate formulation. Future proof architecture must expose
the restart/shifted-Brownian argument, uniqueness step, filtration independence,
measurability of the solution map, and child-to-root composition. Nothing in
this map closes those obligations.

