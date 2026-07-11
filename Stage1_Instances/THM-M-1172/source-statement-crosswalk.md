# Source-statement crosswalk

## Candidate primary sources

- David Gilbarg and Neil S. Trudinger, *Elliptic Partial Differential Equations of Second Order*,
  Springer, Classics in Mathematics (2001 reprint of the 1998 edition), Chapter 9 on strong
  solutions. This is the leading source candidate for linear elliptic `W^{2,p}` estimates and the
  Dirichlet problem; the exact theorem/page, printing, hypotheses, and errata remain to be inspected.
- Lawrence C. Evans, *Partial Differential Equations*, second edition, AMS Graduate Studies in
  Mathematics 19 (2010), Chapter 6. This is a supporting source candidate for elliptic regularity,
  but it must not be used unless an exact theorem matches the selected `W^{2,p}` claim.

These are discovery anchors, not `H0` evidence. The statement phase must inspect the actual text and
choose one theorem rather than synthesize a stronger claim from the chapter titles.

## Crosswalk

| Repository phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| `W^{2,p}` regularity | weak derivatives through order two in `L^p` | concrete Sobolev membership | included; API open |
| elliptic equation | specified second-order operator and `Lu = f` | coefficient/operator structure and solution predicate | included; form open |
| ellipticity | quantitative uniform ellipticity | ordered quadratic-form bound with constants | included; conventions open |
| source `f` | forcing term in the source theorem's `L^p` space | `MemLp`/`Lp` on the selected domain | included; exponent open |
| regularity conclusion | local or global `W^{2,p}` membership | weak second-derivative conclusion | included; variant open |
| a priori estimate | source-accurate norm inequality | normed Sobolev estimate | included; constants open |
| boundary hypotheses | domain regularity and trace/Dirichlet data | domain and boundary-condition API | conditional on global variant |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_147.lean` checks first-derivative Sobolev wrappers
and inventories useful `MemLp`, distribution, and Fréchet-derivative APIs. Its
`W2pRegularityData` takes both second-derivative membership and the estimate as fields, while its
equation and ellipticity fields are abstract propositions. It is therefore statement-shape and
audit discovery only, not the source theorem or a proof of it. Its upstream searches must be
repeated under the rev-5.6 anchor-audit gate.

Before `H0`, an independent reviewer must verify edition, theorem/page, every assumption and
constant dependency, notation definitions, nearby qualifications, and published errata, then
approve a row-by-row source-to-Lean mapping.
