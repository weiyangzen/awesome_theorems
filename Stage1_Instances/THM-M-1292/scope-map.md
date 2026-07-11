# Scope map

## Preserved source scope

- Named subject: a compactness lemma associated with Michael Struwe.
- Date metadata: 1984.
- Variational context: it is described as an alternative to the Palais-Smale condition.
- Broad repository category: differential equations / partial differential equations.

Nothing in the available source inventory fixes whether the intended result is the monotonicity
trick for parameterized min-max functionals, a bounded Palais-Smale sequence result for almost every
parameter, a PDE-specific entropy compactness result, or a later specialization.

## Decisions required before statement freeze

The statement phase must identify a primary publication and freeze its edition, theorem/page,
definitions, and errata. It must then fix the ambient Banach/Hilbert space, differentiability class
of the functionals, parameter interval and exceptional set, monotonicity convention, min-max family
and level, geometric and coercivity/boundedness hypotheses, the precise Palais-Smale sequence or
compactness conclusion, quantifier order, and endpoint/degenerate cases. Foundation, TCB,
computation profile, Lean imports, declaration type, and checked transports also remain open.

## Explicit exclusions

- Treating an assumed `PSCompactnessAt` predicate as proof of a Struwe compactness theorem.
- Substituting a generic sequential compactness or Bolzano-Weierstrass theorem.
- Choosing the legacy module's abstract monotonicity-trick variant without primary-source fidelity.
- Treating proposition-valued structure fields as discharged deformation, differentiability,
  boundedness, entropy, or compactness obligations.
- Treating the repository label `已验证` or the historical Lean file as H0/M0 evidence.
