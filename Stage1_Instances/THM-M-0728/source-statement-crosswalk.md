# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` records `IP=PSPACE`, Adi Shamir, 1990, and the gloss
`interactive proofs equal PSPACE`. `Docs/Stage0_Blueprint.md` repeats it while leaving exact
definitions, assumptions, proof route, dependencies, axioms, and formal artifacts open. The
rev-5.6 manifest preserves `verified` only as `source_status_untrusted`.

The clear bibliographic discovery lead is Adi Shamir, *IP = PSPACE*, Journal of the ACM 39(4),
1992, pages 869-877, DOI `10.1145/146585.146609`, following a 1990 conference version. This intake
does not claim `H0`: the primary text, referenced definitions, edition relationship, and errata
have not been independently inspected and crosswalked by an assigned reviewer.

## Claim crosswalk

| Repository/source component | Required mathematical content | Required Lean content | Intake status |
|---|---|---|---|
| `IP` | interactive verifier/prover model, polynomial bounds, randomness, completeness and soundness | languages, transcript/protocol types, verifier cost, probability and acceptance predicates | model and binder order open |
| `PSPACE` | deterministic polynomial-space decision model | machine/configuration encoding, space measure, language-decision predicate, polynomial bound | no pinned declaration identified |
| `=` | both class inclusions under the same encoding conventions | equality of language classes or checked pair of inclusions | representation open |
| `IP subseteq PSPACE` | deterministic polynomial-space evaluation of an optimal interaction/acceptance condition | simulation obligation with probability and strategy semantics | proof branch only; no credit |
| `PSPACE subseteq IP` | arithmetization-based interactive protocol for polynomial-space computation | reductions, finite-field polynomial identities, sum-check/protocol soundness | proof branch only; no credit |
| Adi Shamir / 1990 | attribution and preliminary-publication lead | no machine proof credit | exact conference record open |
| `verified` | alleged historical status | accepted receipts and terminal proof-body provenance would be required | explicitly untrusted |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Computability.Language` provides `Language`, and
`Mathlib.Computability.TuringMachine.Computable` provides deterministic polynomial-time
vocabulary. `IntakeProbe.lean` checks those exact APIs. A scoped text search found no occurrence of
`PSPACE` or `interactive proof` in pinned mathlib's Lean sources. This is a reproducible intake
inventory observation, not the later immutable formal-candidate audit and not proof that no
external formalization exists.

Before `H0`, an assigned independent reviewer must verify a stable primary edition's exact
statement, referenced definitions, assumptions, pages, proof boundary, conference/journal delta,
and errata. Before statement credit, each verified component must map to an elaborated Lean target,
including domains, ordered binders, thresholds, encodings, and boundary cases.
