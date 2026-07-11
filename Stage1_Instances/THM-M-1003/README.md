# THM-M-1003 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the discrete-time real-valued
`L^p` martingale convergence theorem. Historical Stage1 material is discovery input only.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Root | `1 < p < infinity`, `L^p`-bounded real martingale converges a.s. and in `L^p` | Exact Lean expression is not yet elaborated or fingerprinted |
| Model | Discrete time `Nat`, finite probability/measure space, filtration, real-valued process | Probability-measure versus finite-measure normalization needs statement review |
| Limit | An `L^p` random variable; the legacy candidate selects `Filtration.limitProcess` | Existence and selected-limit formulations need a checked transport |
| Endpoint | `p = 1` only with uniform integrability | Separate theorem; excluded from the root |
| Generalizations | Continuous time and Banach-valued martingales | Explicitly out of scope |
| Legacy Lean | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_283.lean` | Candidate only; no rev-5.6 proof or statement credit |

The future proof architecture must expose at least the martingale-to-submartingale bridge,
almost-sure limit, limit `MemLp`, uniform-integrability or domination step, and terminal
`L^p`-norm convergence composition. No obligation is closed or counted at intake.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M3, R3]`. The human-source debt is
`H3` because the repository supplies only a slogan and no verified primary-source edition,
pinpoint, assumptions, or errata record. The first failed theorem gate is the statement gate:
the exponent restriction in the frozen human claim is not enforced by the legacy full statement
shape, and there is no normalized-expression hash, environment fingerprint, checked transport,
or mutation evidence. `theorem_complete` is false.

## Validation

Exact commands and results for this dossier are recorded in `validation.md`. They validate
manifest membership, repository structure, JSON syntax, and dossier consistency only.
