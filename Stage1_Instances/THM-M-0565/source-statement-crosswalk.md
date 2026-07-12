# Source-statement crosswalk

## Available repository source

`Docs/researches/math_theorems.md` and the generated Stage0 entry supply the Chinese title
`斯蒂菲尔-惠特尼示性类`, the names Eduard Stiefel and Hassler Whitney, the year 1935, and the
phrase `实向量丛的模2示性类` ("mod-2 characteristic classes of real vector bundles"). They supply
no publication, theorem number, page, ordered hypotheses, conclusion, proof boundary, or errata.
The generated `已验证` status is explicitly untrusted under rev-5.6.

Historical work of Stiefel and Whitney and the modern monograph *Characteristic Classes* by John
Milnor and James Stasheff are source-discovery directions only. Exact editions, theorem/page
anchors, assumptions, and errata have not been inspected here, so they provide no `H0` credit.

## Crosswalk

| Repository phrase | Mathematical information supported | Required Lean component | Intake status |
|---|---|---|---|
| "real vector bundles" | intended objects are real bundles | bundle category, rank, base hypotheses, pullback and direct sum | domain identified only |
| "mod-2" | coefficients should be `F_2` | a fixed cohomology theory and coefficient-ring model | coefficient intent identified; model open |
| "characteristic classes" | a graded family of natural invariants is intended | classes `w_i(E)` in degree `i`, or an exact equivalent encoding | family identified; construction open |
| "Stiefel-Whitney" | historical name of that family | no proof credit and no unique conclusion | exact theorem unresolved |
| 1935 / named authors | bibliographic discovery metadata | no formal component | primary anchor unresolved |

## Candidate exact claims requiring source selection

The most plausible statement candidates are: existence of the classes; uniqueness from specified
axioms; a combined existence-and-uniqueness characterization; naturality under pullback; the
Whitney product formula; or a named obstruction theorem. These are not interchangeable. The
statement phase must choose only the candidate warranted by an inspected primary theorem and must
record why the other candidates are excluded.

Before `H0`, an independent reviewer must verify a stable edition, exact theorem/page, definitions,
all assumptions, conclusion, proof boundaries, historical attribution, and errata. Before statement
credit, each verified source component must map row by row to a kernel-elaborated Lean expression.
Anchor audit must separately examine pinned mathlib and credible external Lean 4 projects; the
absence of a theorem-specific repository artifact at intake is not an external negative result.
