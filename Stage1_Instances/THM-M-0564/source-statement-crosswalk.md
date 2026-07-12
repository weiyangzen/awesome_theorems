# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` supplies the Chinese name `示性类`, attributes the subject to
"many mathematicians" in the twentieth century, and gives the statement `向量丛的示性类理论`
("the theory of characteristic classes of vector bundles"). `Docs/Stage0_Blueprint.md` repeats
that wording but leaves definitions, assumptions, proof process, axioms, and artifacts open. Its
`已验证` label is untrusted metadata under rev-5.6.

The wording names a field of theory rather than a truth-valued claim. Consequently there is no
source theorem whose hypotheses and conclusion can yet be crosswalked exactly.

## Discovery-only source candidates

- John W. Milnor and James D. Stasheff, *Characteristic Classes*, Annals of Mathematics Studies 76,
  Princeton University Press (1974). This is a standard monograph candidate for definitions,
  universal constructions, and the individual class families.
- Dale Husemoller, *Fibre Bundles*, Graduate Texts in Mathematics 20, Springer. This is a secondary
  source candidate for vector bundles and characteristic-class constructions.

Neither candidate is an `H0` anchor here. No edition-specific theorem/page, exact statement,
assumption list, proof boundary, or errata record has been selected or independently reviewed.

## Crosswalk

| Repository phrase | Mathematical possibilities | Required Lean component | Intake status |
|---|---|---|---|
| "vector bundles" | real, complex, oriented, stable, or other bundles | concrete bundle category, rank, and base-space hypotheses | unresolved |
| "characteristic classes" | Stiefel-Whitney, Chern, Pontryagin, Euler, or a generic natural assignment | coefficient-graded cohomology classes and pullback action | unresolved |
| "theory" | definition, existence, uniqueness, classification, sum formula, or a collection of results | one exact `Prop` with ordered binders | blocking ambiguity |
| "many mathematicians / twentieth century" | historical subject attribution | edition, theorem, page, assumptions, and errata | no pinpoint source |
| `已验证` | repository status label | no proof term or source receipt | no credit |

## Existing Lean boundary

A repository search found historical modules mentioning characteristic-class APIs only as
dependencies or blockers, not a theorem-specific artifact for `THM-M-0564`. A filename search of
the pinned mathlib tree found characteristic-function and Euler-characteristic files, but no file
named for vector-bundle characteristic classes, Chern classes, or Stiefel-Whitney classes. These
are bounded intake observations, not the immutable candidate audit required by the later
`ANCHOR_AUDIT` phase and not evidence of global absence.

Before `H0`, an independent reviewer must approve a primary-source edition, exact theorem/page,
definitions, hypotheses, conclusion, proof boundary, and errata. Before statement credit, that
approved proposition must map row by row to an elaborated canonical Lean expression.
