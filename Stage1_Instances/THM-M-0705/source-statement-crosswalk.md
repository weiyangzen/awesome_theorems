# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `Church-Rosser定理`, attributes it to
Alonzo Church and J. Barkley Rosser, dates it to 1936, and gives only `lambda calculus confluence`
as its statement. `Docs/Stage0_Blueprint.md` repeats this gloss while leaving the precise definitions,
assumptions, equivalent formulations, axioms, proof route, and formal artifacts open. The manifest
preserves `已验证` only as `source_status_untrusted`.

A historical primary-source candidate is Alonzo Church and J. Barkley Rosser, *Some Properties of
Conversion*, Transactions of the American Mathematical Society 39 (1936), 472-482. This intake has
not independently inspected an immutable scan, exact theorem/page, notation, assumptions, later
corrections, or errata. The citation is therefore a discovery locator, not `H0` evidence.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "lambda calculus" | untyped terms with variables, abstraction, application, and substitution | concrete inductive/quotient term representation and capture-avoiding substitution | family included; encoding open |
| "beta reduction" | compatible closure of beta contraction | one-step relation on the selected term type | expected, exact source variant open |
| "reduces" | zero or more reduction steps | `Relation.ReflTransGen` or a checked equivalent | pinned generic API probed |
| "confluence" | two reducts of one term have a common reduct | quantified join of the many-step relation | provisional claim frozen; canonical expression open |
| conversion formulation | convertible terms admit a common reduct | symmetric-transitive closure plus checked equivalence to confluence | alternate encoding; source selection open |
| `已验证` | untrusted inventory label | no Lean proposition or proof evidence | explicitly rejected as credit |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Logic.Relation` exposes `Relation.ReflTransGen`, `Relation.Join`, and the generic theorem
`Relation.church_rosser`. Its theorem derives global joinability from a stated local condition for
an arbitrary relation. It neither defines untyped lambda terms nor proves that beta reduction meets
that condition. The intake probe checks only these types and closure APIs.

The statement phase must first inspect and independently review the selected source passage, then
map every domain, binder, reduction rule, closure, and boundary case to an elaborated Lean target.
The later anchor audit must separately search repo-local, pinned mathlib, and credible immutable
external Lean 4 formalizations; this bounded intake observation is not that audit.
