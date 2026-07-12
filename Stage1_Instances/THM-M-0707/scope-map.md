# Scope map

## Repository claim

`Docs/researches/cs_theorems.md` states that no Turing machine can decide whether an arbitrary
Turing machine halts on a given input. Stage0 shortens this to "the halting problem is
undecidable." The manifest's `source_status_untrusted` value supplies no proof credit.

## Included claim family

- A concrete, effectively encoded program or Turing-machine type and input type.
- An operational semantics defining finite execution and halting rather than observing a timeout.
- A halting predicate on every program/input pair in the selected domain.
- A purported total effective Boolean decider that is sound and complete for that predicate.
- The negation of the existence of such a decider, normally established through a universal
  evaluator plus diagonal self-application.

This is a scope boundary, not a frozen Lean proposition or proof architecture.

## Decisions required at statement freeze

1. Select an immutable primary-source theorem and decide whether the canonical object is a Turing
   machine, another equivalent machine, or a partial-recursive code.
2. Fix encodings, validity of codes, the input convention, configurations, step relation, halting
   states, and existential finite-step semantics.
3. Define "decides" as a total effective Boolean function with both directions of correctness;
   distinguish this from semidecidability and from Lean's `Decidable` typeclass alone.
4. Fix the exact binder order and whether the root uses arbitrary `(machine, input)` pairs,
   diagonal self-input, or a checked reduction between them.
5. Map any partial-recursive-code formulation to the repository's Turing-machine wording by a
   kernel-checked transport or retain it only as an uncredited alternate target.
6. Freeze malformed-code, initially halted, divergent, empty-input, and other boundary behavior,
   plus foundation, TCB, computation, minimal-import, and mutation-test profiles.

## Explicit exclusions

- Termination of a single fixed program, a bounded-step simulator, or empirical timeout behavior.
- The claim that halting is not semidecidable; the standard halting set is semidecidable.
- Undecidability of only self-input halting presented as the arbitrary-input theorem without a
  checked reduction.
- `Not (Decidable P)` as a substitute for absence of an effective uniform decider unless its
  computational interpretation is fixed and crosswalked.
- A diagonal contradiction whose hypotheses already assume the required universal evaluator or
  encode the conclusion as a structure field.
- The repository label `已验证` or the intake API probe as proof evidence.

No canonical Lean target is frozen during intake, so statement fingerprinting and the four
required mutation classes remain dependency-ordered work for `S56-M-0707-STATEMENT`.
