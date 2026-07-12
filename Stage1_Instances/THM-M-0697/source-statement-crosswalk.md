# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `一阶逻辑完备性`, attributes it to Kurt
Gödel, gives 1929, and states only `一阶逻辑的完备性` ("completeness of first-order logic"). Stage0
repeats this metadata while leaving exact definitions, premises, axioms, machine artifact, and proof
route open. The rev-5.6 manifest deliberately preserves `已验证` only as
`source_status_untrusted`. These records identify a famous theorem family, not an exact statement.

## Primary-source discovery lead

Gödel's 1929 dissertation and the 1930 publication *Die Vollständigkeit der Axiome des logischen
Funktionenkalküls* are the natural primary-source leads. No immutable scan, exact edition,
numbered theorem, page, incorporated definitions, assumptions, or errata were inspected and
accepted in this intake. The leads are therefore `E5` discovery inputs, not an `E4`/`H0` source
packet. The repository's year must not be used to guess which wording is authoritative.

## Source-to-statement crosswalk

| Repository phrase | Expected mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| first-order logic | a fixed first-order signature, syntax, and semantics | `FirstOrder.Language`, sentences, structures, realization | pinned ingredients probed; conventions open |
| semantic validity/consequence | all models, or all models of `T`, satisfy `phi` | `Theory.Models` / `ModelsBoundedFormula` and sentence satisfaction | pinned semantic API probed |
| completeness | semantic consequence implies a formal proof | a derivability judgment plus the implication theorem | derivability calculus not located or selected |
| provable | finite formal derivation in a named calculus | proof objects/rules and a terminal derivability predicate | absent from catalog; open |
| consistent theory has a model | equivalent-style formulation under fixed conventions | syntactic consistency plus `Theory.IsSatisfiable` | satisfiability exists; syntactic bridge open |
| 1929 / Gödel | historical attribution | immutable primary locator and reviewed mapping | metadata only |
| verified | untrusted inventory label | accepted kernel/source receipts | explicitly no credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.ModelTheory.Satisfiability` exposes first-order theory satisfiability, semantic consequence,
and the compactness theorem `FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable`.
`IntakeProbe.lean` checks these exact ingredients using the pinned executable.

A bounded name/text search of pinned `Mathlib/ModelTheory` found no proof-system derivability API
or theorem expressing semantic consequence implies derivability. This is only intake discovery,
not the later exhaustive immutable anchor audit. In particular, the available compactness theorem
must not be renamed or broadened into proof-theoretic completeness.

## Required source crosswalk

An `H0` packet requires an independently reviewed immutable edition and pinpoint theorem, mapping
its language, formation rules, logical axioms/rules, model convention, semantic premise, syntactic
conclusion, finiteness assumptions, equality treatment, dependencies, and corrections. Until that
work is complete the root remains `H1`, not `H0`.
