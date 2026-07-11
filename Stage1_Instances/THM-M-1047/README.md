# THM-M-1047 rev-5.6 intake

This is the `planned` dossier for Kazamaki's criterion. Historical source labels and the legacy
Lean module are discovery inputs only and receive no rev-5.6 proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Kazamaki's sufficient condition for uniform integrability of a stochastic exponential | Exact source variant and time horizon require primary-source pinning |
| Ambient objects | Filtered probability space; real continuous local martingale starting at zero | Lean universes, filtration conditions, and completion/usual conditions remain open |
| Hypothesis | The exponential-submartingale/class-D condition on `exp(M/2)` | Equivalent stopping-time formulations are candidates, not credited transports |
| Construction | Quadratic variation and Doleans-Dade exponential `exp(M - <M>/2)` | No suitable pinned repo-local stochastic-calculus API has yet been established |
| Conclusion | A true uniformly integrable martingale, including the martingale property | Not merely positivity, adaptedness, or a supplied conclusion field |
| Exclusions | Discrete proxies, finite-state special cases, and assumptions containing the conclusion | Such results may become leaves but cannot replace the root |

The legacy `S1_M_240.lean` declaration carries proposition fields for missing infrastructure and a
`terminalKazamakiConclusion` data field. Its projection theorem is therefore not a proof of the
root and is explicitly excluded from machine closure.

## Intake verdict

Lifecycle is `planned`; provisional vector is `[H1, M3, R3]`. The first failed theorem gate is the
exact statement gate: no pinned source edition, normalized Lean expression, environment fingerprint,
checked transport, or mutation suite exists. The theorem is not complete.

Validation commands and their exact outcomes are recorded in `validation.md`.
