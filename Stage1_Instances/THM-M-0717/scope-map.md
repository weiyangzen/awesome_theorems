# Scope map

## Included topic boundary

- A discrete machine with internal control states and a tape or an explicitly source-equivalent
  storage representation.
- A transition rule, configurations, initial configuration, halting convention, and partial
  evaluation semantics.
- Finiteness or effective-finiteness conditions required by the selected model.
- Input/output encodings and the exact behavioral property named by a later selected proposition.

## Decisions required at statement freeze

The repository record does not say whether its target is:

1. the definition and well-defined deterministic semantics of a classical single-tape machine;
2. a simulation or equivalence theorem between `TM0`, `TM1`, `TM2`, or another formulation;
3. existence of a machine computing a particular function;
4. a general characterization of the functions computable by Turing machines; or
5. merely an expository topic, in which case it is not itself a theorem target.

An immutable source must select one proposition. It must decide the alphabet and blank symbol,
state and halting conventions, one- versus multi-tape/storage representation, determinism,
finiteness conditions, input/output representation, treatment of divergence, ordered binders,
hypotheses, conclusion, and degenerate cases.

## Explicit exclusions

- The universal Turing machine theorem, owned separately by `THM-M-0718`.
- Undecidability of the halting problem, Church-Turing thesis, lambda-calculus equivalence,
  register-machine equivalence, complexity bounds, or language-recognition results as substitutes.
- A theorem about one mathlib machine variant presented as the classical source claim without a
  checked representation transport.
- A structure that carries the desired behavior as assumed data and a projection of that field.
- The inventory label `已验证`, existence of definitions, or successful API elaboration as proof.

No canonical Lean target is frozen at intake because the source record contains no proposition.
