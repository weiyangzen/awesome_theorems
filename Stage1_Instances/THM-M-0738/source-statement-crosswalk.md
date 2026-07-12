# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records only the Chinese title `扩展Frege系统`, Stephen Cook,
the year 1975, and the gloss `扩展Frege系统的性质` ("properties of Extended Frege systems").
`Docs/Stage0_Blueprint.md` repeats these fields and leaves the exact definitions, premises, proof
route, axioms, and formal artifact open. The rev-5.6 manifest preserves `已验证` solely as the
untrusted field `source_status_untrusted`.

The metadata supplies no bibliographic work, immutable edition, theorem/page, exact definition of
Extended Frege, hypotheses, quantified conclusion, proof, errata record, or Lean artifact. The
author and year are discovery hints only; this intake does not infer a theorem from them.

## Source-statement crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Frege system" | a finitely presented propositional calculus | formulas, valuations, rules/axioms, derivations | presentation absent |
| "extended" | abbreviations introduced by fresh extension variables | freshness, defining equivalences, dependency order | convention absent |
| "system" | encoded proofs with a checker and size | proof datatype/predicate, end formula, encoding and measure | representation absent |
| "properties" | soundness, completeness, simulation, lower bounds, or automatability | one exact proposition with ordered quantifiers | conclusion absent |
| Stephen Cook, 1975 | historical locator | immutable source, theorem/page, assumptions, errata | incomplete citation |
| `已验证` | untrusted inventory label | no proposition or proof credit | rejected as evidence |

## Required source work

The next phase needs an immutable, independently inspected primary-source proposition. It must
record bibliographic edition/revision, pinpoint theorem and definition pages, the exact calculus and
extension convention, proof encoding and size measure, all assumptions and quantifiers, proof
boundary, and errata. If a later textbook or survey formulation is selected, it must be crosswalked
to the primary result rather than silently substituted.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded
`IntakeProbe.lean` checks finite Boolean-function/cardinality types and polynomial-time Turing
machine vocabulary. These are only potential encoding ingredients. The bounded repository/mathlib
text search found no Extended Frege declaration; that observation is not the later immutable anchor
audit and does not establish nonexistence.

