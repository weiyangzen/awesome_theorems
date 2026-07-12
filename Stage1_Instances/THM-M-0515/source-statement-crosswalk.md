# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `克罗内克青春之梦`, attributes it to
Leopold Kronecker, dates it to 1880, and gives only `虚二次域的类域的生成` ("generation of class
fields of imaginary quadratic fields"). Stage0 repeats this and leaves exact definitions,
assumptions, equivalent statements, axioms, and machine artifacts open. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted`.

No primary source, modern edition, theorem number, page, exact special function, conductor range,
hypotheses, conclusion, proof boundary, or errata record is supplied. The nearby repository entries
for complex multiplication and Hilbert's twelfth problem are distinct targets and cannot fill the
missing statement by adjacency.

## Candidate source work

A later source audit must choose an immutable authoritative formulation of one theorem in the
Jugendtraum family. It must record edition, theorem and page, every assumption and exceptional
case, the exact field equality, proof boundary, errata, and independent review. Historical slogans
and unsourced textbook paraphrases are useful search terms but cannot establish `H0`.

## Crosswalk

| Repository phrase | Mathematical component needing a source | Lean component | Intake status |
|---|---|---|---|
| "imaginary quadratic field" | exact number-field and embedding predicate | number field, quadratic/CM structure | prerequisite API probed; exact domain open |
| "class fields" | Hilbert, ring, ray, or other class field; order/conductor | abelian extensions, class/ray groups, class-field construction | family unspecified; no target selected |
| "generation" | equality of a named extension with a field adjoined by values | field adjunction and exact extension equality | base and generators absent |
| implied CM values | `j`, Weber, or another modular function at specified CM points | modular function and special-value infrastructure | absent from repository claim |
| `已验证` | untrusted inventory label | no Lean proposition or proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.NumberTheory.NumberField.CMField` and
`Mathlib.NumberTheory.NumberField.ClassNumber`. It checks the CM-field predicate, ring of integers,
class group, and class number. A bounded name search found no Jugendtraum, imaginary-quadratic
class-field, Hilbert-class-field, or ring-class-field declaration. This records available
prerequisites and a gap only; it is not the later immutable anchor audit and gives no proof credit.

