# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Kazamaki criterion | N. Kazamaki, "On a problem of Girsanov," *Tohoku Mathematical Journal* 29 (1977), 597-600 | future exact root | Primary source identified bibliographically; theorem/page, assumptions, scan hash, and errata still require audit, so no H0 claim |
| Continuous local martingale starting at zero | Same primary paper; exact theorem wording to be transcribed | no pinned mathlib declaration identified at intake | The legacy `localMartingaleProxy : Nat -> ...` is not the source domain |
| Half exponential condition | Standard formulation using `exp(M/2)` as a uniformly integrable submartingale or class-D process | legacy `halfExponentialSubmartingale` plus an opaque `kazamakiCondition` | Ordinary submartingale alone is too weak; exact quantification over stopping times/time horizon must be frozen |
| Stochastic exponential | `E(M)_t = exp(M_t - <M>_t/2)` for continuous `M` | legacy proxy formula | Requires genuine quadratic variation and stochastic-exponential definitions, not arbitrary functions connected by a field |
| Uniformly integrable martingale conclusion | Same root theorem | `Martingale ...` and `UniformIntegrable ...` are available predicates | The legacy conclusion is stored as input data and only projected, hence supplies no proof credit |

A commonly cited later source is N. Kazamaki, *Continuous Exponential Martingales and BMO*,
Lecture Notes in Mathematics 1579, Springer (1994). It is useful for terminology and variants but
does not replace the original-source premise audit.

Open source work: acquire immutable copies, verify the 1977 page range and exact theorem number,
transcribe ordered assumptions and horizon, check corrections/errata, distinguish class-D from
uniform-integrability formulations, and obtain independent review. Until then the human status is
`H1`, and the wording in `intake.json` is deliberately provisional where variants differ.
