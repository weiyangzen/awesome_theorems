# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `PSPACE完全性`, attributes it to
"many mathematicians", dates it only to the 1970s, and gives the statement `PSPACE完全问题`
("PSPACE-complete problems"). The duplicate inventory occurrence has the same wording. Stage0
repeats it and marks the exact definitions, assumptions, proof history, dependencies, axioms, and
formal artifacts as open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted`.

This metadata neither names a problem nor states the membership and hardness clauses. The nearby
`IP=PSPACE` record is a distinct target and cannot disambiguate this one.

## Candidate source work

The standard theorem that TQBF is PSPACE-complete is a plausible source target, but it is only a
candidate. A stable edition of a complexity-theory text can locate its exact modern formulation;
the source audit must then trace the claimed historical proof source rather than treating a
textbook paraphrase as primary evidence. Edition, theorem/page, formal-language syntax, machine
model, reduction class, assumptions, proof boundary, and errata all remain unverified. No source is
credited as H0 during intake.

If the intended problem is not TQBF, its exact name and primary theorem must be supplied. A list of
examples or a generic definition of completeness does not determine the repository target.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "problem" | a named decision language and concrete input syntax | `Language` plus an encoder/well-formedness predicate | absent from source |
| `PSPACE` | languages decided within polynomial work space | formal machine semantics, space usage, polynomial bound | API not identified in pinned mathlib |
| "hard" | every PSPACE language reduces to the named language | quantified resource-bounded reduction | reduction convention absent |
| "complete" | PSPACE membership and PSPACE hardness | conjunction/structure with both checked components | subject and definitions open |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.Computability.Language`,
`Mathlib.Computability.TuringMachine.Computable`, and `Mathlib.Computability.Reduce`. It checks
formal languages, a finite bundled Turing-machine model, time-bounded and polynomial-time machine
packages, and computable many-one reducibility. These declarations confirm useful substrate but do
not encode PSPACE completeness: `ManyOneReducible` guarantees only computability, and the bundled
resource API shown by the probe is time-based rather than space-based.

The bounded name/content search of pinned mathlib found no `PSPACE`, `SpaceComplexity`, or
polynomial-space declaration. This negative result is an intake blocker observation, not the later
immutable external-anchor audit and not proof that no suitable external Lean project exists.
