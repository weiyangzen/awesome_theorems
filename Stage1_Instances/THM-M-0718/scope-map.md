# Scope map

## Included topic boundary

- A source-specified theorem asserting universality of a Turing-machine computation model.
- A fixed universal machine/interpreter and a precise encoding of simulated programs and inputs.
- Partial computation semantics, including divergence and the halting/output convention.
- A correctness relation connecting the universal machine's behavior to the simulated program.
- Finiteness or effective-finiteness conditions required for the object to count as a Turing machine.

## Decisions required at statement freeze

1. Whether programs encode classical single-tape machines, multi-tape/stack machines, or partial
   recursive codes.
2. Whether the universal object is one fixed finite machine, a fixed transition function with
   program-dependent reachable finite support, or an indexed machine construction.
3. Whether simulation is equality of partial outputs, preservation of acceptance/halting, or a
   step-by-step refinement, and whether efficiency overhead is part of the claim.
4. The concrete encodings of programs, inputs, configurations, and outputs, including malformed
   encodings and the pairing convention.
5. The quantifier order: existence of one machine before quantification over programs and inputs is
   essential to the ordinary universality reading.

## Explicit exclusions

- Church-Turing equivalence, the halting problem, Rice's theorem, or undecidability as substitutes.
- A family of machines indexed by the simulated program when the source requires one universal
  interpreter; that can trivialize the existential quantifier.
- Merely proving that every partial recursive function has some Turing machine.
- Total-function-only evaluation that silently discards divergence.
- Complexity bounds unless the selected source statement explicitly includes them.
- The separate `THM-C-0003` inventory entry as authority for this target; it is only a discovery
  clue and cannot supply cross-target proof credit.
- The repository label `已验证` as source or machine evidence.

No canonical Lean target is frozen at intake because the source record does not resolve these
choices.
