# Source-statement crosswalk

## Candidate primary sources

- Luis A. Caffarelli, "A localization property of viscosity solutions to the Monge-Ampere
  equation and their strict convexity," *Annals of Mathematics* 131 (1990), 129-134.
- Luis A. Caffarelli, "Interior `W^{2,p}` estimates for solutions of the Monge-Ampere equation,"
  *Annals of Mathematics* 131 (1990), 135-150.

These bibliographic records identify two primary candidates, not an exact theorem. Exact theorem
number/page span, wording, definitions, assumptions, cited prerequisites, and errata have not been
inspected in this intake and therefore provide neither `H0` nor a canonical formal statement.

## Crosswalk

| Repository phrase | Mathematical component to disambiguate | Required Lean component | Intake status |
|---|---|---|---|
| "Caffarelli regularity theory" | localization/strict convexity or a named interior regularity theorem | one exact proposition, not a family label | source selection open |
| "Monge-Ampere equation" | classical determinant equation or Alexandrov/viscosity formulation | Hessian determinant or Monge-Ampere measure | encoding open |
| convex solution | convex function on a specified domain | convexity plus domain restriction | included, binders open |
| density `f` | positivity/boundedness/continuity hypotheses | measurable or regular real-valued function and bounds | exact assumptions open |
| regularity | local `C^{1,alpha}`, `C^{2,alpha}`, or `W^{2,p}` conclusion | concrete function-space membership/estimate | exact conclusion open |
| sections/localization | normalized sublevel-set geometry | affine sections and quantitative inclusions | required only if selected source uses it |

## Existing repository boundary

The generated Stage1 entry contributes only the phrase "regularity of the Monge-Ampere equation"
and a proof-package seed. It does not identify a source theorem. No legacy target file was present
under this theorem's owned path at intake. A later anchor audit must separately search the pinned
mathlib revision and credible Lean 4 projects; bibliographic knowledge cannot be converted into
machine closure.

Before `H0`, an independent reviewer must approve the selected edition/article, exact theorem and
page, definitions, every hypothesis and conclusion, dependency/errata review, and a row-by-row
source-to-Lean mapping.
