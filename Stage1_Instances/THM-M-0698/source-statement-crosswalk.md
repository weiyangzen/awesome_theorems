# Source-statement crosswalk

## Repository sources

The target-specific row in `Docs/researches/math_theorems.md` names `一阶逻辑紧致性`, attributes it
to Kurt Goedel and Anatoly Maltsev, dates it to 1930, and gives only the gloss "first-order logic
compactness". Stage0 repeats that gloss and explicitly leaves definitions, assumptions, proof,
axioms, and machine artifact links open. The rev-5.6 manifest retains `已验证` only as the untrusted
source label.

An earlier row in the model-theory section is titled `紧致性定理`, has the same attribution and
date, and states: "a theory has a model if and only if each finite subset has a model." This
uniquely corroborates the conventional semantic reading selected for intake. The repository does
not, however, give a source UID proving that the rows were intended as duplicates. It supplies no
primary source edition, theorem/page, exact language conventions, proof, or errata record. Thus it
supports human-scope selection but cannot clear `H0` or independent review.

## Crosswalk

| Repository phrase | Frozen mathematical component | Candidate Lean component | Intake status |
|---|---|---|---|
| "first-order logic" | arbitrary first-order language and its sentences | `FirstOrder.Language`, `L.Sentence` | pinned API checked |
| "theory" | set of closed formulas | `FirstOrder.Language.Theory` | pinned API checked |
| "has a model" | a nonempty structure satisfying all sentences | `Theory.IsSatisfiable` | definition type checked |
| "every finite subset has a model" | every finite subtheory contained in `T` is satisfiable | `Theory.IsFinitelySatisfiable` | definition type checked |
| "compactness" | equivalence of those two predicates | `Theory.isSatisfiable_iff_isFinitelySatisfiable` | candidate theorem type checked; no proof credit |
| `已验证` | untrusted inventory status | no proposition or receipt | explicitly rejected as evidence |

## Pinned formal candidate

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.ModelTheory.Satisfiability` documents and defines the two predicates and declares
`FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable`. The bounded intake probe
checks the exact displayed types and also checks `models_iff_finset_models`, an alternate
consequence form. This locates an unusually strong formal candidate, but terminal proof-body,
transitive dependency, axiom, placeholder, provenance, exact-expression, and source-fidelity audits
belong to later phases and remain open.

## Work required before source closure

The source audit must select an immutable primary or authoritative edition, record a theorem or
section/page locator, map its language/model/nonemptiness and finite-subtheory conventions, inspect
corrections or errata, and obtain independent review. It must also resolve the historical
attribution carefully rather than copying the repository's combined names into an `H0` claim.

