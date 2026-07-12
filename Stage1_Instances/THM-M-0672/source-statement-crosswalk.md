# Source-statement crosswalk

## Available record

`Docs/researches/math_theorems.md` contains the complete upstream repository record: `模型配方法`,
Abraham Robinson, 1966, and the gloss `非标准分析的基础`. `Docs/Stage0_Blueprint.md` repeats it and
leaves exact definitions, assumptions, proof route, axioms, and artifacts open. Under rev-5.6 the
`已验证` field is explicitly untrusted metadata and grants neither `H0` nor kernel credit.

## Primary-source candidates

- Abraham Robinson, *Non-standard Analysis*, North-Holland, 1966. The matching author, year, and
  gloss make this a bibliographic candidate, but the repository gives no chapter, theorem, or page.
  The book must be inspected before deciding whether transfer, enlargement/saturation, an
  elementary-extension construction, or another result is intended.
- The model-companion/model-completion literature associated with Robinson is a separate candidate
  family suggested by the Chinese title. No exact paper, edition, theorem, or year correspondence
  is present in the repository record.

These are discovery anchors only. Intake has not inspected or independently reviewed a pinpoint
statement, its definitions, assumptions, corrections, or errata.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `模型配方法` | model companions or model completions | first-order languages, theories, model classes, embeddings, model-completeness and companion predicates | translation and exact theorem open |
| `非标准分析的基础` | foundational nonstandard-analysis result | elementary extensions, transfer/realization, ultrapowers or saturation interfaces as source requires | historical gloss only; conclusion open |
| Abraham Robinson | author/source locator | no formal component and no proof credit | candidate attribution only |
| 1966 | possible locator for *Non-standard Analysis* | no formal component and no proof credit | exact edition/page open |
| `已验证` | repository status label | none | untrusted; excluded from H/M evidence |

## Lean discovery boundary

A narrow repository and pinned-mathlib text search found concrete neighboring APIs for elementary
embeddings, ultraproducts, and Los's theorem, but no declaration identified as a model-companion or
model-completion theorem. This is intake discovery, not the later immutable anchor audit. Nearby
APIs cannot resolve which proposition the source record means and receive no proof credit here.

Before `H0`, an independent model-theory reviewer must approve the selected edition/theorem/page,
terminology translation, all assumptions and definitions, source boundaries, and errata. Before
statement credit, those approved rows must map to one elaborated Lean expression, with checked
transports for any alternate formulation. The present metadata is too weak for either gate.
