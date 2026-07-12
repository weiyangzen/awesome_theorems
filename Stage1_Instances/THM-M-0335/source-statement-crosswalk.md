# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the title `琼斯指标定理`, Vaughan Jones, 1983, and only the
gloss `子因子的指标值` ("index values of subfactors"). Stage0 repeats it. The manifest deliberately
stores `已验证` as `source_status_untrusted`; it supplies no exact proposition or proof credit.

## Primary source candidate

V. F. R. Jones, "Index for subfactors", *Inventiones Mathematicae* **72** (1983), issue 1,
pages 1-25, DOI `10.1007/BF01389127`. Publisher metadata and Crossref agree on the author, title,
journal, volume, issue, date, and page span. This identifies an immutable original-paper candidate,
but the article's exact numbered theorem/page, local definitions, hypotheses, proof boundary, and
errata were not inspected and independently reviewed in this intake. It is therefore `H1`, not
`H0`, evidence.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "subfactor" | inclusion of type `II_1` factors | factor predicates plus admissible inclusion | intended; exact source conventions open |
| "index" | Jones index `[M:N]` | source-faithful exact-valued index definition | missing from located pinned API |
| "index values" | discrete values below `4` and continuous range at least `4` | set membership or equivalent implication | intended; restriction/realization boundary open |
| `4 cos^2(pi/n)` | exact discrete family, `n >= 3` | exact real cosine, natural/integer binder, equality | mathematical scope frozen; formal expression open |
| `已验证` | untrusted inventory label | no proposition or evidence | rejected as proof evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe imports
`Mathlib.Analysis.VonNeumannAlgebra.Basic` and checks `WStarAlgebra`, `VonNeumannAlgebra`, its
underlying `StarSubalgebra`, and its commutant. A bounded case-insensitive search of mathlib Lean
sources found the von Neumann algebra base but no relevant `subfactor`, `Jones index`, `finite
factor`, or trace-index declaration. The unrelated polynomial identifier `evalSubFactor` was
excluded. This bounded search is not the later immutable anchor audit.

Before `H0`, an independent reviewer must pinpoint the primary theorem and verify every assumption,
definition, endpoint, restriction/realization direction, and erratum row against the canonical
human and Lean statements.

