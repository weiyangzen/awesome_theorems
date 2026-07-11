# Source-statement crosswalk

| Claim component | Human/source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Identity of the target | `Docs/researches/math_theorems.md` names Chebyshev, 1867, and “an upper bound on the probability that a random variable deviates from its expectation” | No declaration selected | This fixes the probabilistic theorem, but the repository row is metadata rather than primary proof evidence |
| Two-sided tail bound | P. L. Chebyshev, *Des valeurs moyennes*, Journal de Mathématiques Pures et Appliquées, 2e série 12 (1867), 177-184, is the historical candidate named by standard bibliographies | Candidate expression over `Measure`, expectation, and variance APIs | Bibliographic candidate only: scan/page-to-premise mapping, edition hash, translation, and errata search remain open, so no `H0` claim |
| Modern formula | For `r > 0`, `P(|X - E[X]| >= r) <= Var(X)/r^2` | Exact event and codomain coercions unresolved | Frozen as the intended root; exact Lean elaboration belongs to the dependent statement phase |
| Moment assumptions | A finite second moment supplies finite expectation and variance in the real-valued setting | Candidate `MemLp X 2 mu` or explicit integrability/measurability package | Alternatives must not be interchanged until their exact implications are checked in the pinned environment |
| Markov reduction | Apply Markov's inequality to the nonnegative variable `(X - E[X])^2` | Future bridge to a pinned mathlib theorem or local proof body | Proof architecture only; anchor name, exact type, revision, axioms, and terminal-body provenance are unaudited |
| Standard-deviation form | `P(|X-E[X]| >= k sigma) <= 1/k^2` | Future checked transport | Requires separate treatment of zero variance and the square-root normalization |

The deterministic inequality for similarly sorted finite sequences, also commonly called
Chebyshev's inequality and represented separately by `THM-M-0282`, is explicitly out of scope.
Strict-tail (`>`) and closed-tail (`>=`) versions are not presumed interchangeable: the canonical
root uses the closed event, and any alternate version needs a checked event inclusion or equality.

Discovery references are not evidence receipts. The statement and anchor-audit phases must obtain
immutable copies or hashes, pinpoint the historical assumptions and notation, search corrections,
inspect the actual pinned Lean declarations, and obtain independent review. Current human status is
therefore `H1`, not source-complete `H0`.
