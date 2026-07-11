# THM-M-1044 rev-5.6 intake

This is the `planned` dossier for Girsanov's theorem. The repository source supplies only the phrase
"change of measure and martingales". That denotes a theorem family, not an exact proposition, so
this intake deliberately does not manufacture a Lean target.

## Scope map

| Surface | Candidate scope | Intake boundary |
|---|---|---|
| Probability space | filtered probability space satisfying the conditions required by the selected source | filtration and completeness/right-continuity assumptions are unfrozen |
| Time | finite interval, nonnegative real time, or a discrete index | no time domain is selected |
| Integrator | Brownian motion, continuous local martingale, or general semimartingale | no process class is selected |
| Measure change | density random variable or density process, with absolute continuity or equivalence | direction and positivity conditions are unfrozen |
| Conclusion | drift-shifted Brownian motion, corrected local martingale, or transformed characteristics | no conclusion is selected |
| Integrability | true-martingale density as a hypothesis; sufficient criteria may be separate results | Novikov/Kazamaki are separate targets and are not imported into this root |
| Lean surface | probability/filtration/martingale/Radon-Nikodym/stochastic-integral APIs | exact modules, declaration, and environment fingerprint remain open |

The statement phase must first obtain a source-authoritative formulation or an explicit project
scope decision. It must preserve ordered binders, horizon, filtration conditions, density
orientation, integrability assumptions, and the exact martingale conclusion. The candidate families
above are alternatives, not conjuncts and not credited formal targets.

## Intake verdict

Lifecycle is `planned`; root vector is `[H3, M4, R3]`. The first failed gate is exact source scope:
the available record cannot distinguish materially different standard forms. Consequently no
canonical Lean expression can yet be elaborated. This is formalization/scope debt, not evidence that
the mathematical theorem is open. The theorem is not complete.

## Validation

The commands and exact outcomes in `validation.md` establish manifest membership, repository
consistency, JSON syntax, and dossier hygiene only. Master acceptance and all dependent phases remain
outstanding.
