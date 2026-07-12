# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `计算复杂性`, attributes the field to many
mathematicians in the twentieth century, and gives only `计算资源复杂度的理论` (the theory of
computational-resource complexity). `Docs/Stage0_Blueprint.md` repeats that gloss while leaving
exact definitions, premises, proof path, dependencies, axioms, and formal artifacts open. The
rev-5.6 manifest carries `已验证` only as `source_status_untrusted`.

This is not a proposition: it contains no computation model, resource measure, bound, ordered
quantifiers, hypotheses, or conclusion.

## Primary-source discovery boundary

Hartmanis and Stearns, *On the Computational Complexity of Algorithms*, Transactions of the
American Mathematical Society **117** (1965), 285-306, DOI `10.2307/1994208`, is a plausible
primary historical source for machine-based time complexity and complexity classes. It contains
multiple definitions and results, however; its title and bibliographic identity do not select one
as this repository target. Cobham's and Edmonds's early polynomial-time work, hierarchy theorems,
and later completeness theory likewise yield different propositions. None is accepted as the
canonical source without an accountable scope decision and independent inspection of an immutable
edition, pinpoint statement, referenced definitions, proof boundary, and errata.

| Repository phrase | Possible mathematical component | Lean discovery candidate | Intake status |
|---|---|---|---|
| computational complexity | resource use by computations | `Turing.TM2ComputableInTime` | exact resource-bounded predicate exists; not a selected theorem |
| computational resources | a time/space/other cost measure | `Turing.TM2OutputsInTime` and a bound function | metadata does not select the measure or semantics |
| complexity theory | classes, closure, hierarchy, separation, or completeness | no single declaration | subject area, not a conclusion |
| polynomial time | polynomial upper bound relative to an encoding | `Turing.TM2ComputableInPolyTime` | API anchor only; the repository gloss does not specifically select P |
| verified | alleged prior formal status | none | explicitly untrusted and gives no proof credit |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Computability.TuringMachine.Computable` defines multi-tape Turing-machine computation,
time-bounded computation, and polynomial-time computation. `IntakeProbe.lean` checks those exact
types and the forgetful conversion from polynomial-time to time-bounded computation. This confirms
that a later exact statement may have relevant local vocabulary. It does not select a source claim,
establish equivalence across computation models, define a complete complexity class, or prove a
root theorem. The formal-candidate audit remains a dependent phase with its own precommitted search.

No `H0`, `M0`, source-proof closure, or statement-equivalence credit is claimed.

