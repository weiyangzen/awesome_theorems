# Source-statement crosswalk

## Available repository source

`Docs/researches/math_theorems.md` supplies the Chinese title `陈示性类`, attributes it to
Shiing-Shen Chern in 1946, and gives only `复向量丛的示性类` ("characteristic classes of complex
vector bundles"). The generated Stage0 and rev-5.6 manifest entries repeat this subject and an
untrusted `已验证` status. They provide no publication, theorem number, page, ordered assumptions,
conclusion, proof boundary, or errata record.

Chern's historical papers and modern treatments such as Milnor and Stasheff's *Characteristic
Classes* are discovery directions only. No edition or theorem/page anchor was inspected and pinned
in this intake, so none receives `H0` credit.

## Crosswalk

| Repository phrase | Mathematical information supported | Required Lean component | Intake status |
|---|---|---|---|
| "complex vector bundles" | intended input objects | bundle model, base category, finite rank, pullback and direct sum | domain family identified; hypotheses open |
| "characteristic classes" | intended outputs are natural cohomological invariants | a fixed graded cohomology target and classes `c_i(E)` | family identified; theorem conclusion open |
| "Chern" | conventional name and attribution for the family | no proof term or unique formal statement | historical metadata only |
| 1946 | discovery metadata | no formal component | primary publication and exact date claim unaudited |
| `已验证` | source-dataset status label | no human or machine evidence | explicitly untrusted by rev-5.6 |

## Candidate exact claims requiring source selection

Plausible roots include existence of the class family, uniqueness from stated axioms, a combined
existence-and-uniqueness characterization, naturality, the Whitney sum formula, normalization on a
universal line bundle, rank vanishing, or a Chern-Weil comparison. These are not interchangeable.
The statement phase must choose only a claim warranted by a pinned source and must record why other
candidates are outside the root.

Before `H0`, an independent reviewer must verify a stable primary edition, exact theorem/page and
definitions, every assumption and conclusion, proof boundaries, attribution, and errata. Before
statement credit, those components must map row by row to a kernel-elaborated Lean expression.
Anchor audit must separately inspect pinned mathlib and credible external Lean 4 projects; the lack
of a local theorem artifact at intake is not evidence that no formalization exists.
