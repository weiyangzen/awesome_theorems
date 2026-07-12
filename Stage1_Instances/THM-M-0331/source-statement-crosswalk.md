# Source-statement crosswalk

## Repository sources

`Docs/researches/math_theorems.md` records `斯通定理`, attributes it to Marshall Stone, dates it to
1932, and gives only `单参数酉群与自伴算子` ("one-parameter unitary groups and self-adjoint
operators"). `Docs/researches/physics_theorems.md` contains a separate Stage0 record with the gloss
`酉群与自伴算符的指数关系` ("the exponential relation between unitary groups and self-adjoint
operators"). Stage0 explicitly leaves exact definitions, hypotheses, equivalent formulations,
axioms, and existing artifacts open. The rev-5.6 manifest selects the mathematical record as
`THM-M-0331` and preserves `已验证` only as `source_status_untrusted`.

These are secondary inventory descriptions, not theorem statements. They provide no edition,
theorem/page, ordered binders, proof passage, assumptions, errata, or formal declaration.

## Candidate source work

The statement phase must inspect an immutable primary publication or an authoritative modern
source that states the intended version. It must record edition, theorem and page, definitions of
strong continuity and generator, all hypotheses, direction(s), uniqueness, sign convention, proof
boundary, and errata, followed by independent review. The historical attribution and date in the
inventory are discovery metadata only and do not establish `H0`.

## Crosswalk

| Repository phrase | Expected mathematical component | Candidate Lean component | Intake status |
|---|---|---|---|
| "one-parameter" | action/homomorphism of `(ℝ, +)` | a bundled or explicit homomorphism `ℝ → unitary (H →L[ℂ] H)` | encoding open |
| "unitary group" | unitary operators with group law | `unitary (H →L[ℂ] H)` and `Unitary.linearIsometryEquiv` | pinned API probed |
| "strongly continuous" | continuity of `t ↦ U(t)x` for every `x` | `Continuous` applied pointwise | convention absent from source |
| "self-adjoint operator" | generally unbounded, densely defined operator | `H →ₗ.[ℂ] H`, `IsSelfAdjoint`, `IsSelfAdjoint.dense_domain` | pinned API probed |
| "exponential relation" | `U(t)` represented by functional calculus of the generator | exact exponential/functional-calculus expression | direction and sign open |
| implicit generator | strong derivative at zero on its domain | derivative predicate plus `LinearPMap.domain` | absent from source |
| `已验证` | untrusted inventory label | no proposition and no proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports the inner-product-space adjoint and partial-linear-map modules and checks the types of
partial operators, their domains and closedness, self-adjointness and dense domain, unitary
operators, their linear-isometry equivalence, and continuity. These are only encoding ingredients.
A bounded name/text search found other theorems bearing Stone's name but no declaration identified
as this one-parameter unitary-group theorem; that negative search is not the later anchor audit.

