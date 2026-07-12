# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `默里-冯·诺依曼分类`, attributes it to
Francis Murray and John von Neumann, dates it to 1936, and gives only `冯·诺依曼代数的分类`
("classification of von Neumann algebras"). Stage0 repeats this metadata while leaving exact
definitions, assumptions, equivalent formulations, axioms, and machine artifacts open. The
rev-5.6 manifest retains `已验证` solely as `source_status_untrusted`.

The historical coordinates make a published human result credible, so the intake uses `H1` rather
than treating this as an open mathematical problem. They do not identify an edition, article,
chapter, theorem, page, assumptions, exact conclusion, proof boundary, or errata. Consequently they
cannot support `H0` or a canonical formal target.

## Candidate primary-source work

Murray and von Neumann's 1936 paper *On Rings of Operators*, *Annals of Mathematics* 37(1), is a
candidate primary locator suggested by the repository's authors and year. Intake does not assert
that one particular theorem in that paper is the intended root. The source phase must inspect a
fixed copy, record its immutable identity and exact page/result, translate its historical
terminology, map every assumption and conclusion, audit corrections or later convention changes,
and obtain independent review.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "von Neumann algebra" | concrete operator algebra or abstract W-star algebra | `VonNeumannAlgebra` or `WStarAlgebra` | both APIs probed; intended presentation open |
| "classification" | exclusive and exhaustive factor types I/II/III | factor predicate, center, projections, comparison and type predicates | mathematical candidate only; classification APIs not identified |
| "classification" | refined factor types | dimension/finite/infinite projection predicates and refined type predicates | candidate only |
| "classification" | central decomposition of a general algebra | central projections or direct-integral/decomposition infrastructure | candidate only |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.Analysis.VonNeumannAlgebra.Basic` and checks the abstract and concrete
algebra structures, concrete commutant, and `IsStarProjection`. The module itself states that
substantial foundational work remains, including equivalence of its abstract and concrete notions.
These APIs are encoding ingredients only. No type-I/type-II/type-III factor classification
declaration was identified by the bounded local name/content search. That negative observation is
not an exhaustive anchor audit and receives no proof credit.
