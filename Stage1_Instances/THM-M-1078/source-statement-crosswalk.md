# Source-statement crosswalk

## Repository-source record

The repository's source row says only "martingale transform", attributes it to
"Burkholder/Davis/Gundy", gives 1972, and labels it verified. That row does not identify a theorem,
page, hypotheses, constant, or even whether it means a discrete transform or the related BDG
inequalities. It is therefore discovery evidence only.

## Candidate primary sources

- D. L. Burkholder, "Martingale transforms," *Annals of Mathematical Statistics* 37 (1966),
  1494-1504. This is the primary candidate for the discrete martingale-transform theorem family.
  The exact theorem number, page, multiplier convention, range of `p`, and constant must be checked
  directly before it can support `H0`.
- D. L. Burkholder, B. J. Davis, and R. F. Gundy, "Integral inequalities for convex functions of
  operators on martingales," in *Proceedings of the Sixth Berkeley Symposium on Mathematical
  Statistics and Probability*, Volume II (1972), 223-240. This is the candidate behind the
  repository attribution and date. Direct inspection must decide whether its relevant result is
  the transform inequality, a more general operator theorem, or only the adjacent maximal/square-
  function family.

These bibliographic anchors are not accepted source packets. Edition scans, exact theorem/page,
assumptions, definitions, and errata have not been independently reviewed in this intake.

## Crosswalk

| Repository phrase | Frozen interpretation | Required Lean component | Intake status |
|---|---|---|---|
| martingale | finite real `L^p` martingale on a filtration | probability space, filtration, adaptedness, conditional-expectation law, `MemLp` | included; encoding open |
| transform | predictable scalar transform of martingale differences | shifted measurability and finite sum of weighted increments | included; indexing open |
| bounded multipliers | `|v_k| <= 1` (pointwise or a.e. as selected source requires) | measurable multiplier plus bound and any a.e. transport | included; source convention open |
| boundedness | uniform terminal `L^p` estimate | `snorm`/`Lp` inequality with a constant depending only on `p` | included; normalization open |
| `1 < p < infinity` | strong-type non-endpoint range | real exponent assumptions accepted by the chosen norm API | included |
| 1972 / BDG | historical metadata needing disambiguation | no Lean component until source identity is resolved | unresolved; no proof credit |

## Evidence boundary

No repo-local or upstream Lean declaration has been accepted or inspected for this intake. The
statement and anchor-audit phases must search the pinned mathlib revision and credible Lean 4
projects, recording exact modules, declaration types, immutable revisions, trust dependencies,
placeholders, and terminal proof-body provenance. Before `H0`, an independent reviewer must approve
a pinpoint primary-source statement and a row-by-row map including all quantifiers, filtration and
measurability assumptions, integrability requirements, constants, endpoints, and indexing.
