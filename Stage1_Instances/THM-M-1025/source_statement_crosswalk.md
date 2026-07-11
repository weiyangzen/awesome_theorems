# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` attributes the item to Paul Levy, dates it to 1924, and gives
only the gloss "characteristics of stable distributions". It supplies no definition of stability,
formula, parameter ranges, theorem number, page, or cited publication. The same sparse record is
projected into `Docs/Stage0_Blueprint.md`. Its `已验证` field is untrusted intake metadata.

The gloss is convention-sensitive. Stable laws can be characterized probabilistically by affine
closure of sums of independent copies, or analytically by a characteristic-function family. Even
within the analytic form, standard parameterizations differ at `alpha = 1` and shift the location
parameter. Choosing one without a source pinpoint could change the theorem rather than formalize it.

## Claim map

| Claim component | Metadata anchor | Candidate formal surface | Intake assessment |
|---|---|---|---|
| stable law | "stable distributions" | predicate on `ProbabilityMeasure Real` defined by affine convolution closure | expected, exact quantifier form open |
| characteristic function | ambiguous word "characteristics" | Fourier transform of a probability law | plausible intended analytic side, not explicit enough for acceptance |
| stability index | classical stable-law classification | real `alpha` with `0 < alpha` and `alpha <= 2` | expected parameter, absent from metadata |
| skew/scale/location | classification family | bounded skew, positive scale, real location | parameterization and degeneracy policy open |
| exceptional branch | convention-dependent formula | separate `alpha = 1` logarithmic term | must be explicit in any analytic target |
| Gaussian endpoint | `alpha = 2` specialization | normal-law characteristic function | boundary branch, not a replacement for the root |
| converse | word "characteristics" may mean characterization | analytic family implies probabilistic stability | inclusion in the root is not determined by metadata |

## Source discovery leads

Two primary or standard monograph leads for the later source-audit phase are Paul Levy,
*Calcul des probabilites* (1925), and V. M. Zolotarev, *One-Dimensional Stable Distributions*
(1986 English translation). These are discovery leads only. This intake has not established that
the 1924 attribution points to a particular Levy paper or fixed an edition, theorem/page, scan
hash, translation relationship, or errata record. Neither lead receives `H0` or `H1` credit here.

The statement phase may proceed only after a reviewer selects and pinpoints the intended source
claim and freezes the stability definition, both implication directions, Fourier sign, all
parameter bounds, the `alpha = 1` location convention, and the degenerate-law policy. It must then
elaborate that exact proposition and mutation-test every one of those choices. Until then `H2` and
`M4` are the fail-closed classifications.
