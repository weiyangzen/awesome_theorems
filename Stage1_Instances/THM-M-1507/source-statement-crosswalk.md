# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` records the title `拉格朗日对偶`, Joseph Lagrange, the year
1762, and the complete gloss `约束优化的对偶问题`. It supplies no bibliography, formula,
quantifiers, hypotheses, conclusion, proof, errata, or formal artifact. All six catalog lines
originate at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; this is repository
provenance, not a primary mathematical source. The attribution and date themselves remain
unaudited.

`Docs/Stage0_Blueprint.md` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent formulations,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted`.

## Crosswalk

| Catalog component | Missing mathematical component | Prospective Lean surface | Intake status |
|---|---|---|---|
| `约束优化` | decision domain, objective, constraint families, feasibility | types, objective and constraint functions, feasible predicate | absent; no binders accepted |
| `拉格朗日` | multiplier types/signs and Lagrangian formula/convention | a function of decision variables and multipliers | absent; no definition accepted |
| `对偶问题` | dual function, feasible multipliers, objective direction, dual value | infimum over decisions and supremum over multipliers, or source-selected equivalent | absent; family only |
| implicit theorem status | weak inequality, zero gap, attainment, or another conclusion | an exact `Prop` with ordered binders | absent; no proposition accepted |
| catalog attribution/date | primary edition and historical/source identity | source revision and statement crosswalk | untrusted metadata only |
| `已验证` | proof body, formal system, declaration, revision and build evidence | exact module/declaration plus kernel receipt | no credit |

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.Convex.Cone.Dual` provides `ProperCone.dual`, double-dual inclusion/equality, and
Farkas-style hyperplane separation. Its imported `Mathlib.Analysis.Convex.Cone.Basic` explicitly
lists definitions of primal and dual cone programs and proofs of weak/strong cone-program duality
as TODO work. `Mathlib.Analysis.Calculus.LagrangeMultipliers` concerns constrained local extrema
and multipliers, not the Lagrangian dual problem selected by this catalog entry.

A bounded repo-local and pinned-mathlib search found a separate Kantorovich transport-duality
development and the cone TODO text, but no source-selected general Lagrangian-duality declaration.
The transport theorem is a different root and receives no credit. This is bounded intake discovery,
not the downstream exhaustive anchor audit or a claim about every external Lean project.

## Retry condition

The statement phase may proceed only after an accountable reviewer corrects or selects one
immutable primary-source proposition, freezes every semantic choice in `scope-map.md`, maps the
edition, theorem/definition locator, assumptions, conclusion, proof and errata, and independently
approves why that proposition is this repository target. It must then elaborate the exact Lean
target with minimal pinned imports and run the required domain, hypothesis, binder-scope and
boundary mutations.
