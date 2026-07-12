# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` records "differential algebra", attributes it to Joseph
Ritt/Ellis Kolchin in the 1950s, and describes it as "the algebraic theory of differential
equations". It labels the formalization status `已验证`, but supplies no bibliography, edition,
theorem number, page, quotation, assumptions, errata, or machine artifact. The target manifest
explicitly treats that status as untrusted and starts this target at `L0 / rework_required`.

Ritt's *Differential Algebra* (1950) and Kolchin's later books are plausible source families to
inspect, not accepted citations for an exact theorem. Intake does not infer a theorem from their
titles. Edition, locator, wording, assumptions, and errata remain open.

## Crosswalk

| Source element | Information fixed | Information still required | Intake result |
|---|---|---|---|
| "differential algebra" | a mathematical field is intended | a unique theorem and its exact scope | unresolved |
| "algebraic theory" | algebraic structures/methods are involved | ambient structures, characteristic, binders, hypotheses | unresolved |
| "differential equations" | derivations or differential equations are involved | ordinary/partial derivations, equation objects, solution notion | unresolved |
| Ritt/Kolchin, 1950s | historical attribution metadata | primary edition, theorem/page, quotation, division of attribution | unverified |
| `已验证` | metadata-screening label only | inspectable human proof and kernel receipts | no credit |

## Formal vocabulary crosswalk

Pinned mathlib contains `Differential`, `DifferentialAlgebra`, `Differential.ContainConstants`, and
the differential-field modules `Mathlib.FieldTheory.Differential.Basic` and
`Mathlib.FieldTheory.Differential.Liouville`. These are relevant discovery anchors only. Their
presence neither identifies the source proposition nor proves that mathlib contains an exact root
declaration.

The first downstream gate is selection of one primary-source theorem. A source reviewer must map
its domains, ordered quantifiers, hypotheses, conclusion, conventions, and boundary cases to the
canonical Lean proposition row by row. Until then the statement gate remains blocked and H0/M0
credit is impossible.
