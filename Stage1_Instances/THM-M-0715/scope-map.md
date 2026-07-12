# Scope map

## Repository claim

`Docs/researches/math_theorems.md` gives only the title `可计算性理论`, collective attribution,
the period "20th century", and the gloss `可计算函数的理论` ("the theory of computable
functions"). Stage0 repeats those fields while leaving definitions, premises, proof route,
equivalent formulations, axioms, and formal artifacts open. The manifest preserves `已验证` only
as untrusted source metadata.

## Candidate claim families

- closure properties of primitive-recursive or partial-recursive functions;
- equivalence of partial-recursive functions with a specified Turing-machine model;
- existence of a universal partial-recursive function or program enumeration;
- undecidability of the halting predicate or Rice-style extensional properties;
- equivalence among lambda calculus, recursive functions, register machines, and Turing machines.

These are distinct propositions with different domains and assumptions. The repository's broader
computer-science survey lists them separately, and several have adjacent or independent manifest
IDs. None is adopted as this root at intake.

## Decisions required before statement elaboration

The statement phase must first obtain and independently review a source that selects one theorem.
It must then freeze the computation model; total or partial functions; input and output types;
coding and decoding functions; operational semantics and divergence; extensional equality;
ordered binders and hypotheses; the exact conclusion; boundary cases; alternate-model transports;
minimal imports; and foundation, TCB, and computation profiles.

## Explicit exclusions

- A definition of `Computable`, `Partrec`, or a Turing machine presented as the missing theorem.
- A conjunction of many famous computability results invented to make "theory" truth-valued.
- Halting undecidability, Rice's theorem, Church-Turing, recursive functions, or universal machines
  silently substituted for this record when those subjects have separate repository entries.
- Native Lean computability or executable evaluation confused with the encoded mathematical model.
- The `已验证` label, an available mathlib API, or a successful `#check` used as proof credit.

No canonical human or Lean proposition is frozen at intake.

