# Source-statement crosswalk

## Candidate primary sources

- George D. Birkhoff, "Proof of the Ergodic Theorem," *Proceedings of the National Academy of
  Sciences* 17 (1931), 656-660, DOI `10.1073/pnas.17.12.656`. This is the historical primary-paper
  candidate. Its exact theorem wording, notation, assumptions, and any corrections remain to be
  inspected against a stable scan.
- Peter Walters, *An Introduction to Ergodic Theory*, Graduate Texts in Mathematics 79, Springer
  (1982), the pointwise ergodic theorem treatment. This is a modern interpretation candidate, not a
  substitute for auditing the primary claim; exact theorem/page and edition errata remain open.

These are discovery anchors, not `H0` evidence.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Birkhoff ergodic theorem" | pointwise almost-sure/time-average theorem | `Tendsto` under an `∀ᵐ` quantifier | included; exact expression open |
| probability space | normalized measure space | `Measure Ω` and `IsProbabilityMeasure μ` | included |
| measure-preserving transformation | measurable dynamics preserving `μ` | concrete `MeasurePreserving T μ μ` or justified equivalent | included; binder/API open |
| ergodic | invariant measurable sets are trivial | mathlib `Ergodic T μ` plus checked assumption crosswalk | included; source match open |
| integrable observable | real `L1` function | `MeasureTheory.Integrable f μ` | included |
| space mean | integral of `f`, without normalization on a probability space | `∫ x, f x ∂μ` | included |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_247.lean` is discovery evidence. It defines
`StatementNormalizationBoundary`, `BirkhoffLimitPackage`, and `ErgodicBirkhoffConclusion`, and
records historical mathlib/external audits. Because the conclusion is supplied as structure data,
the file does not establish its existence. Its imports, pinned revisions, candidate declarations,
and statement equivalence must be re-audited in later nodes; none is accepted by this intake.

Before `H0`, an independent reviewer must verify the primary edition and stable page image, exact
assumptions and conclusion, terminology drift, errata, and every row of the source-to-Lean mapping.
