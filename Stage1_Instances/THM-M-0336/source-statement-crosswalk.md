# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `康内斯分类定理`, attributes it to Alain
Connes, dates it to 1976, and gives only `注入冯·诺依曼代数的分类` ("classification of injective von
Neumann algebras"). Stage0 repeats this metadata while leaving exact definitions, assumptions,
equivalent formulations, axioms, and machine artifacts open. The rev-5.6 manifest retains
`已验证` solely as `source_status_untrusted`.

The attribution makes a published human result credible, so intake uses `H1` rather than treating
the topic as an open problem. The metadata does not identify an edition, theorem, page, assumptions,
exact conclusion, proof boundary, or errata. It therefore supports neither `H0` nor a canonical
formal target.

## Candidate primary-source work

Connes' article *Classification of Injective Factors. Cases II1, II-infinity, III-lambda,
lambda != 1* in *Annals of Mathematics* 104 (1976) is the candidate primary locator suggested by
the repository title, year, and gloss. Intake records it only as a locator, not as a verified
pinpoint or a decision that the entire paper is one theorem. The source phase must inspect an
immutable copy, identify exact numbered results and pages, record every factor, separability, type,
and equivalence assumption, distinguish the paper's covered cases from later classification
results, audit errata, and obtain independent review.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "von Neumann algebra" | abstract W-star algebra or concrete operator algebra | `WStarAlgebra` or `VonNeumannAlgebra` | both structures probed; intended presentation open |
| "injective" | extension/retraction property for the algebra as an operator system | source-matched injectivity predicate and morphism categories | no matching API identified in bounded probe |
| "classification" | isomorphism to a canonical hyperfinite/injective factor | factor and type predicates, canonical model, star-isomorphism | mathematical candidate only |
| "classification" | one result for each covered factor type | explicit type parameter, branch hypotheses, exhaustiveness and uniqueness | exact branch range open |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.Analysis.VonNeumannAlgebra.Basic` and checks abstract/concrete von Neumann
algebra structures, the concrete commutant, and star projections. A scoped content search found no
operator-algebra declarations for injective or amenable factors, hyperfinite factors, or the Connes
classification in that module tree. This is an intake observation, not an exhaustive anchor audit.
The available APIs are encoding ingredients only and receive no statement or proof credit.
