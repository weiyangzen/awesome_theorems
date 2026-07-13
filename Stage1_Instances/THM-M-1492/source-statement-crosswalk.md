# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10903-10908` records the title `线性规划`, George Dantzig, the
year 1947, and the complete gloss `线性目标函数的优化`. It supplies no bibliography, formula,
definitions, quantifiers, hypotheses, conclusion, proof, corrections, errata, or formal artifact.
All six catalog lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; this is repository provenance, not a primary
mathematical source. The attribution and date remain unaudited metadata.

`Docs/Stage0_Blueprint.md:40567-40592` repeats the gloss while explicitly leaving the target formal
system, foundation, exact definitions and premises, proof route, dependency graph, equivalent
forms, axioms, machine status, and artifact links open. The rev-5.6 target manifest retains
`已验证` only in the field `source_status_untrusted`.

## Crosswalk

| Catalog component | Missing mathematical component | Prospective Lean surface | Intake status |
|---|---|---|---|
| `线性` objective | coefficient domain, decision carrier, objective orientation and value codomain | scalar/typeclass binders and a linear functional or matrix-vector expression | absent; no binders accepted |
| `规划` | constraints, standard form, signs, feasibility and boundary conventions | matrices or linear maps, relations, feasible predicate | absent; no model accepted |
| `优化` | infimum/supremum, attainment, optimizer, alternative, duality, or algorithm result | an exact `Prop` and any witness types | absent; no conclusion accepted |
| implicit theorem status | all hypotheses and proof boundary | ordered binders and assumptions | absent; topic family only |
| attribution and 1947 | primary edition and exact result identity | immutable source revision and crosswalk | untrusted metadata only |
| `已验证` | proof body, formal system, declaration, revision, trust and build evidence | exact module/declaration plus kernel receipt | no credit |

The literal gloss cannot be translated to Lean without adding a conclusion: optimization is a
problem or operation, not by itself a proposition. Plausible LP theorems have materially different
assumptions and conclusions, so no one of them is privileged at intake.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.Convex.Cone.Dual` provides proper-cone duality and Farkas-style separation
infrastructure. Its imported `Mathlib.Analysis.Convex.Cone.Basic` explicitly lists as TODOs the
definitions of primal and dual cone programs, weak and strong cone-program duality, and definitions
of linear programs with LP duality.

`Mathlib.Tactic.Linarith.Oracle.SimplexAlgorithm.PositiveVector` defines a meta-level reduction of
`linarith` certificate search to a bounded linear program and calls a simplex implementation. Its
`stateLP` and `findPositiveVector` declarations are computation used by a tactic oracle, not a
source-mapped, kernel-level statement or proof of an LP root. Algorithm ownership also belongs to
the separate target `THM-M-1493` unless an approved cross-target bridge later says otherwise.

A bounded repository and pinned-mathlib search found those adjacent surfaces but no
source-selected declaration for this target. This observation is intake discovery only, not the
later exhaustive immutable anchor audit and not a claim about all external Lean projects.

## Retry condition

The statement phase may proceed only after an accountable reviewer corrects or selects one
immutable primary-source proposition, maps every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, correction and degenerate case, and independently approves
why that proposition is the repository target. The phase must then encode exactly that claim with
minimal pinned imports, preserve its elaborated expression and environment fingerprints, compile
any credited transports, and execute the required domain, hypothesis, binder-scope, and boundary
mutations.
