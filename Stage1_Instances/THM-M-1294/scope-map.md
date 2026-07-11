# Scope map

## Included theorem family

- A critical-growth elliptic or variational PDE fixed by the selected primary theorem.
- A bounded solution, approximate-solution, or Palais-Smale sequence satisfying every source
  equation, boundary, energy, and residual hypothesis.
- Subsequence extraction, a weak/background limit, and concentration profiles or bubbles.
- The source's precise convergence away from concentration points, parameter separation,
  quantization, norm splitting, and energy identity conclusions.

## Decisions required before statement freeze

The statement phase must inspect a stable primary source and fix the author/theorem intended by
"global compactness"; the PDE and sign convention; ambient domain or manifold and dimension;
boundary conditions; critical exponent; function and dual spaces; sequence and boundedness
hypotheses; weak-solution and Palais-Smale predicates; profile equations; translation/dilation
parameters; finite versus countable profile indexing; convergence topologies; and the exact energy
or norm splitting. It must map zero profiles, vanishing remainders, boundary concentration, and
noncompact symmetry cases. Universe and binder order follow those choices.

## Explicit exclusions

- One-point compactification, compact-operator closed-ball compactness, Arzela-Ascoli, weak-star
  compactness, Prokhorov tightness, Rellich-Kondrachov, or Aubin-Lions as the terminal theorem.
- A generic compact profile space whose fields assume extraction, the PDE, energy splitting, or
  convergence.
- A concentration-compactness slogan without the selected source's equation and conclusions.
- A theorem for a neighboring critical PDE or different domain substituted for the source result.

The formal statement must expose the concrete PDE and decomposition quantifiers, or record a
precise unavailable Lean API as a blocker.
