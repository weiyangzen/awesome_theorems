# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Definition from elementary step integrands | K. Ito, "Stochastic Integral," *Proceedings of the Imperial Academy* 20 (1944), 519-524, DOI `10.3792/pia/1195572786` | finite adapted sums, provisionally related to `S1_M_227.discreteStochasticIntegral` | Primary paper identified, but a scan/hash and line-by-line notation audit are still required |
| Isometry controlling completion | Ito (1944), same article; the second-moment identity is the construction's analytic bridge | a future elementary-integral isometry lemma | Exact equation/page mapping and assumptions are not yet accepted |
| Extension to square-integrable integrands | Ito (1944), same article, approximation construction | a future continuous extension from elementary predictable processes into an `L2` random-variable space | Density, representative independence, and uniqueness must be explicit proof obligations |
| Modern Brownian formulation and filtration conventions | B. Oksendal, *Stochastic Differential Equations*, 6th ed., Springer, 2003, Chapter 3, section on the Ito integral | future normalized wrapper over pinned mathlib probability APIs | Secondary clarification only; edition-page and convention audit remain open |
| Existing repository artifact | No human source is cited by the legacy file | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_227.lean` | Discovery only: finite sums compile historically, while `StatementShape` assumes essential construction conclusions and cannot represent closure |

## Scope correspondence

The phrase "definition of the stochastic integral" in the generated blueprint is too short to be
an exact theorem. The intake resolves it conservatively as the classical Brownian Ito construction:
elementary adapted sums, isometry, completion, agreement, and uniqueness. This does not broaden the
claim to general semimartingales. Conversely, merely defining a finite discrete sum would substitute
a strictly weaker theorem and is excluded.

The statement phase must inspect the pinned mathlib object model before fixing whether predictability
is encoded directly, through an `L2` completion, or through progressively measurable representatives.
It must also mutation-test removal of predictability and square integrability, replacement of
Brownian motion by an arbitrary process, `T = 0`, the zero integrand, and equality of almost-everywhere
representatives.

No `H0` claim is made. `H1` records that a primary source is identified but not yet immutably pinned,
fully crosswalked (edition/pages/equations/assumptions/errata), or independently reviewed.
