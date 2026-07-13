# Scope map

## Preserved theorem family

The target is the undecidability of the halting problem. A later source and statement freeze must
retain all of these material components:

- a concrete, effectively encoded class of programs or machines;
- an input domain and an initialization/encoding convention;
- operational or partial-function semantics that distinguish termination from divergence;
- a halting predicate over every program/input pair in the selected valid domain;
- one total effective decision procedure, not a noncomputable Boolean function or a collection of
  pointwise `Decidable` instances; and
- the conclusion that no such sound-and-complete uniform decider exists.

This scope identifies a theorem family. It is not yet an exact source statement, Lean target, or
proof architecture.

## Decisions required at statement freeze

1. Inspect and independently review an immutable primary or authoritative source passage, with
   exact edition, page or section, definitions, assumptions, conclusion, proof boundary,
   translation, corrections, and errata.
2. Select the formal computation model: Turing machines, partial-recursive codes, another universal
   model, or one model plus a checked equivalence to the source wording.
3. Fix program and input encodings, valid versus malformed codes, configurations, transition or
   evaluation semantics, initial and halting states, and the treatment of divergence.
4. Define effective decidability precisely, including totality and both correctness directions;
   distinguish it from semidecidability and Lean's unrestricted propositional `Decidable`.
5. Freeze ordered binders and decide whether the root quantifies over arbitrary `(program, input)`
   pairs, a fixed input, diagonal self-input, or uses checked reductions among these formulations.
6. Resolve boundary cases: initially halted machines, empty input, invalid codes, programs that
   return without output, infinite execution, and any zero-code or indexing convention.
7. Freeze the foundation, TCB, computation, minimal-import, expression-fingerprint, alternate-
   encoding, and four statement-mutation profiles required by rev-5.6.

## Explicit exclusions

- Termination of one fixed program, termination checking for a restricted language, bounded-step
  simulation, or an empirical timeout.
- The false stronger claim that halting is not recursively enumerable.
- Fixed-input or self-input undecidability presented as the arbitrary-input root without a checked
  reduction in the required direction.
- `Not (Decidable p)` used as a synonym for absence of a uniform effective decider.
- A classical Boolean characteristic function with no computability or machine-realizability
  requirement.
- A structure, hypothesis, axiom, or oracle that assumes the desired undecidability conclusion.
- Reusing `THM-M-0707`, `ComputablePred.halting_problem`, or a matching theorem name as proof credit
  before exact statement identity and provenance are checked for this target.
- Treating the catalog label `已验证` as human-source, kernel, or theorem-completion evidence.

No canonical statement, formal expression, alternate transport, obligation registry, discovery
protocol, accepted proof state, or completion claim is frozen at intake.
