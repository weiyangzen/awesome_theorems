# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Historical normal approximation for sums | A. de Moivre, *The Doctrine of Chances*, 2nd ed. (1738), pp. 235-243, binomial approximation section | no exact candidate claimed | Primary historical lineage candidate; edition scan, exact proposition, and assumptions still require audit |
| General historical development | P.-S. Laplace, *Theorie analytique des probabilites*, 2nd ed. (1814), Book II, Ch. IV | no exact candidate claimed | Broad historical anchor only; it does not by itself freeze a modern measure-theoretic root |
| Modern i.i.d. finite-variance branch | Historical repository wording: `independent random-variable sums converge normally`; no theorem/page was supplied by the target manifest | `ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub` in `Mathlib.Probability.CentralLimitTheorem` | Plausible scoped formal target found in the legacy artifact; exact type, pin, and scope equivalence are deferred |
| Centering and scaling | Not specified in the source record | inverse square-root scaling of the centered finite sum | Necessary candidate detail, not licensed as an exact source crosswalk yet |
| Broader CLT family | Not distinguished in the source record | no single declaration selected | Multivariate, triangular-array, martingale, functional, and quantitative forms remain outside the candidate branch |

The repository source record (`Docs/researches/math_theorems.md`) gives only the attribution,
dates, and phrase "normal convergence of sums of independent random variables." Independence alone
is insufficient for an unrestricted CLT, so that phrase cannot truthfully be translated into a
Lean proposition without adding hypotheses. The statement phase must select and source a precise
version, then mutation-test independence, identical distribution, moment assumptions, centering,
scaling, and degenerate variance.

No `H0` or immutable-source receipt is claimed. Required follow-up: obtain stable scans or critical
editions, record file hashes and exact page propositions, add a modern primary theorem source for
the chosen version, check errata/translation issues, and obtain independent review.
