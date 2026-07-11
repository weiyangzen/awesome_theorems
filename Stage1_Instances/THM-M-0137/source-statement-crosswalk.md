# Source-statement crosswalk

## Candidate primary sources

- V. G. Kac, *Infinite-Dimensional Lie Algebras*, 3rd ed., Cambridge University Press, 1990,
  Chapter 10. This is the standard book location for the Weyl-Kac character formula; exact theorem
  number, wording, and edition-page anchor still require inspection.
- V. G. Kac and D. H. Peterson, "Infinite-dimensional Lie algebras, theta functions and modular
  forms", *Advances in Mathematics* **53** (1984), 125-264, DOI
  `10.1016/0001-8708(84)90032-X`. This is a primary candidate for the named Kac-Peterson modular
  results; the exact character theorem and assumptions still require inspection.

These citations are discovery anchors, not immutable evidence receipts and not an `H0` claim.

## Crosswalk

| Metadata component | Candidate source meaning | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "Kac-Peterson" | likely the joint modularity work | normalized characters, theta functions, and modular action may be essential | unresolved |
| "character formula" | may instead mean Weyl-Kac formula | alternating affine-Weyl numerator and root-product denominator | unresolved |
| "affine Lie algebra characters" | common subject of both candidates | affine algebra and highest-weight representation objects are required | included subject only |
| no stated hypotheses | affine type, integrability, dominance, level, and completion unknown | no exact Lean binders can yet be frozen | blocking |

## Existing Lean discovery boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_053.lean` imports mathlib loop-algebra, Lie
character, weight, Weyl-group, and Hahn-series APIs. Its own header says it is not a proof of the
Kac-Peterson formula, and its interfaces do not identify a unique source theorem. It is therefore
discovery input only and receives no statement or proof credit.

Before `H0`, a reviewer must inspect a stable scan, record the exact theorem label/pages and all
definitions it invokes, check errata, map every assumption and conclusion to the chosen canonical
claim, and independently approve the mapping.
