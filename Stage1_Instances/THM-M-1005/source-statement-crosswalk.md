# Source-statement crosswalk

## Candidate primary sources

Joseph L. Doob, *Stochastic Processes*, Wiley, 1953, is the historical primary-source candidate
for the named theorem family. A stable copy must still be inspected to identify the exact chapter,
theorem/page, notation, hypotheses, and relevant corrections. Bibliographic identification alone
is not H0.

For statement disambiguation, a modern primary textbook edition may be selected and recorded if it
states the intended weak or strong form more explicitly, but it must not be used to manufacture a
hybrid claim. The repository gloss "moment estimate for a martingale maximum" suggests the strong
`Lp` form, yet does not specify `p`, constants, or whether absolute values are used.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "Doob inequality" | one exact maximal-inequality variant | one exact theorem expression | family identified; variant and theorem anchor open |
| martingale maximum | running finite-time maximum/supremum | finite index set and measurable maximum | included; convention open |
| moment estimate | strong `Lp` norm/moment bound, likely `p > 1` | integrability predicate, `Lp` norm or integral, exact constant | intended by gloss; formula open |
| martingale hypotheses | source filtration, adaptedness, and conditional-expectation relation | concrete filtered probability-space/process predicates | included; encoding open |
| weak maximal bound | level-crossing estimate used directly or in the strong proof | measurable event and probability/integral inequality | conditional on selected source variant |

## Evidence boundary

The repository supplies no accepted source excerpt or Lean declaration for this target. Before H0,
an independent reviewer must verify an immutable edition, exact theorem/page, referenced definitions,
all integrability and exponent assumptions, boundary cases, and errata, then approve the row-by-row
source-to-Lean map. Before M-credit, the exact Lean target must elaborate; later anchor work must
inspect actual declarations and terminal proof bodies at immutable revisions.
