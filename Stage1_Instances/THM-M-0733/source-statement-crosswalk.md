# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `自然证明`, authors Alexander Razborov and
Steven Rudich, year 1994, and only the gloss `证明复杂性下界的障碍`. The wording appears twice.
`Docs/Stage0_Blueprint.md` repeats those fields while leaving the exact definitions, premises,
proof route, axioms, and machine artifact open. `Docs/researches/cs_theorems.md` separately labels
the item `Natural Proofs障碍` and says only that natural-proof methods face a fundamental barrier.
The rev-5.6 manifest correctly retains `已验证` solely as `source_status_untrusted`.

The attribution suggests the primary-source family Razborov and Rudich, *Natural Proofs* (1994
conference version; later journal publication), but the repository supplies no immutable edition,
theorem/page, exact definition set, assumptions, or errata record. This intake does not claim to
have established an H0 source crosswalk from that suggestion.

## Source-statement crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "natural proof" | a property satisfying constructivity and largeness conditions | predicates on encoded truth tables plus explicit resource/density bounds | definitions absent |
| "complexity lower bound" | usefulness against a selected nonuniform circuit class | circuit semantics, size family, and asymptotic nonmembership predicate | class and bounds absent |
| "barrier" | conditional incompatibility with pseudorandom functions | exact implication/negation with ordered quantifiers | conclusion absent |
| Razborov/Rudich, 1994 | likely primary-source family | immutable edition, theorem/page, definitions, and errata | citation incomplete |
| `已验证` | untrusted inventory label | no proposition or proof credit | rejected as evidence |

## Required source work

The next phase needs an immutable, independently inspected primary-source theorem passage. It must
record the edition/revision, theorem and pages, definitions referenced by that theorem, all circuit
and density parameters, the exact cryptographic premise, proof boundaries, and known corrections.
It must also explain whether the repository means the conference statement, a journal theorem, or a
later standard corollary. Until then, assigning exact quantifiers or an `H0` human proof would be
invented provenance.

## Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` checks
finite Boolean-function, cardinality, and polynomial-time Turing-machine types. These provide only
possible encoding vocabulary. They do not define Boolean circuits, natural properties, usefulness,
or pseudorandom-function security, and they do not constitute a formal anchor audit.

