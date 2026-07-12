# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9845-9850` supplies exactly the title `指标理论`, Henri Poincare,
1885, the gloss `闭曲线的指标`, importance `high`, and status `已验证`. Git history places this
uncited record in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It contains no
bibliography, theorem or page locator, definitions, binders, hypotheses, conclusion, proof route,
errata, or formal artifact.

`Docs/Stage0_Blueprint.md:36723-36748` repeats the metadata but explicitly leaves the exact
definitions and premises, proof process, dependencies, equivalent forms, axiom policy,
machine-checked status, and artifact links open. The rev-5.6 target manifest preserves `已验证` only
as untrusted metadata and resets this target to `L0 / rework_required`.

No primary mathematical source is cited or selected. The attribution and date are discovery hints,
not a pinpoint source crosswalk. Consequently this intake makes no H0 or source-genealogy claim.

## Component crosswalk

| Catalog component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `闭曲线` / closed curve | loop as a path, periodic parametrization, Jordan curve, piecewise smooth contour, boundary of a planar domain | `Path`, continuous maps, periodic functions, or a future curve structure | representation and regularity open |
| `指标` / index | curve winding number about a point, vector-field index along a curve, or boundary/local-index sum theorem | lift through an exponential cover, degree/homotopy class, contour integral, or future vector-field index | mathematical object and theorem conclusion open |
| omitted datum | excluded point, nonzero boundary field, enclosed isolated zeros, or source-specific phase portrait | explicit binder and avoidance/nonvanishing/isolation hypotheses | absent; hard statement blocker |
| Poincare, 1885 | historical attribution to an index-theory family | provenance only after a pinpoint primary source is frozen | unverified discovery metadata |
| ODE category | possible planar-vector-field interpretation | a future ODE/vector-field encoding | contextual clue, not statement identity |
| `已验证` | untrusted inventory label | no proposition or proof object | no H or M credit |

## Formal crosswalk boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe checks `Path`, path homotopy, covering-map path lifting, the complex exponential covering, and
complex circle parametrization. A bounded lexical search over repo-local Lean and pinned mathlib
found no declaration named as a winding number, Poincare index, vector-field index, or closed-curve
index. This does not constitute the later exhaustive formal anchor audit and does not establish
absence from external Lean projects.

Before statement work, accountable reviewers must preserve an immutable primary or authoritative
source, record an exact theorem/page and incorporated definitions, select one truth-valued claim,
transcribe every ordered binder and hypothesis, fix its index and orientation convention, map the
conclusion and boundary cases, inspect corrections and errata, and independently approve the
crosswalk. Only that corrected target may receive a canonical Lean expression, minimal imports,
checked alternate-form transports, expression/environment fingerprints, and statement mutations.
