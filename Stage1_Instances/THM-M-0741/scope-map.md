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

The statement phase freezes these components in mathlib's universal partial-recursive-code model.
This is an exact conventional Lean target, but it is not yet an accepted source-exact translation,
proof architecture, or proof.

## Frozen statement decisions

1. Programs are `Nat.Partrec.Code`; inputs are `Nat`; both are concrete universe-0 types.
2. Every code constructor is valid, so no malformed-code premise is introduced.
3. Execution is `Code.eval`; halting is its `Part.Dom` proposition, including every returned value.
4. Effective decision is `ComputablePred`, not semidecidability or unrestricted `Decidable`.
5. The root is one predicate on arbitrary `(program, input)` pairs. Fixed-input, existentially
   fixed-input, and diagonal self-input variants are explicit uncredited mutations.
6. `Code.zero` authenticates termination on every input; `Code.rfind' Code.succ` authenticates
   divergence on every input.
7. The sole direct import, expression and environment fingerprints, checked expanded-form iff,
   foundation/TCB/computation profiles, and four required mutation classes are recorded.

## Open source decision

An accountable review must still inspect and independently approve an immutable primary passage,
including its edition, definitions, assumptions, proof boundary, historical-to-modern translation,
correction, and errata. A concrete Turing-machine formulation may receive alternate-encoding
credit only after a checked transport to the frozen root. These source tasks keep `H1`; they do not
undo exact elaboration of the conventional machine target.

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

No obligation registry, discovery protocol, proof body, accepted execution state, audit completion,
or theorem completion is claimed by the statement freeze.
