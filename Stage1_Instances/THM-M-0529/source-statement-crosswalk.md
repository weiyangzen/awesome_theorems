# Source-statement crosswalk

## Repository sources inspected

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` give the Chinese phrase
`拓扑空间的同调不变量` ("homological invariants of topological spaces"), attribute the item to
Henri Poincare and 1895, and label it `已验证`. They give no definition, quantified theorem,
hypotheses, coefficient convention, citation, or proof. These fields are discovery metadata and do
not establish H0 or any machine status.

## Candidate primary sources

- Henri Poincare, "Analysis Situs," *Journal de l'Ecole Polytechnique*, second series, volume 1
  (1895), pages 1-121, is the historical source candidate behind the repository attribution. Its
  exact relevant section, terminology, correction supplements, and relationship to modern homology
  groups have not been inspected.
- Samuel Eilenberg and Norman Steenrod, *Foundations of Algebraic Topology*, Princeton University
  Press (1952), is a primary modern axiomatic source candidate for functorial topological
  invariance. The exact theorem/page, coefficient conventions, and errata remain to be inspected.

The historical paper's invariants must not be silently rewritten as modern singular homology. The
statement phase must select an exact theorem source or explicitly document a checked historical-to-
modern bridge. These citations are candidate anchors only, not source acceptance or proof credit.

## Crosswalk

| Repository component | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "topological space" | all topological spaces, including empty spaces | `X Y : TopCat` | exact formal encoding frozen |
| "homology groups" | ordinary unreduced absolute singular homology, integral coefficients, `n : ℕ` | `((singularHomologyFunctor AddCommGrpCat n).obj (AddCommGrpCat.of ℤ)).obj X` | exact formal encoding frozen |
| "invariant" | a homeomorphism induces an invertible homology morphism | `IsIso (...map (TopCat.isoOfHomeo e).hom)` | exact formal encoding frozen |
| Poincare / 1895 | historical invariant and definitions | source-to-modern transport, if credited | unverified metadata |
| `已验证` | repository source-status label | no Lean component and no proof credit | explicitly untrusted |

Before H0, an independent reviewer must verify the selected immutable edition, exact theorem/page,
definitions, all hypotheses and conclusions, historical corrections or errata, and a row-by-row
source-to-Lean map. Before any M0 status, a separate anchor audit must identify and validate the
exact terminal Lean body and its transitive trust closure.
