# THM-M-1227 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 21 semantic obligations before proof execution. Eighteen are
root-relevant machine obligations; `X-SOURCE`, `X-TCB`, and `X-AUTOMATION` are non-proof overlays.
All require readable coverage. Root and statement fingerprints bind the checked `Statement.lean`;
planned fingerprints bind each precise human statement to its proposed formal signature. Any
correction, split, merge, target, eligibility, exclusion, weight, or risk change requires version 2
and an append-only delta.

The immutable anchor audit found no terminal theorem. Therefore no obligation is marked closed and
the root remains `M4`.

## Typed proof route

```text
M1227-ROOT [open M4]
`-- M1227-T-ASSEMBLE  checked conditional six-conjunct composition
    |-- M1227-L-GRADIENT  identify the distributional gradient
    |   `-- M1227-C-COMPACT  extract and identify limits
    |-- M1227-L-CLASS  limiting velocity/gradient energy class
    |   |-- M1227-C-BOUNDS  uniform energy/dissipation bounds
    |   `-- M1227-C-COMPACT
    |-- M1227-L-DIVERGENCE  pass solenoidality to the limit
    |   |-- M1227-C-GALERKIN  divergence-free approximants
    |   `-- M1227-C-COMPACT
    |-- M1227-L-MOMENTUM  pass the nonlinear weak identity
    |   |-- M1227-C-GALERKIN
    |   `-- M1227-C-COMPACT
    |-- M1227-L-TRACE  attain u0 strongly at time zero
    |   |-- M1227-N-DATA  smooth solenoidal datum approximation
    |   `-- M1227-C-COMPACT
    `-- M1227-L-ENERGY  global limiting energy inequality
        |-- M1227-C-BOUNDS
        `-- M1227-C-COMPACT
```

`C-GALERKIN` also requires `N-DATA`; `C-COMPACT` requires `C-BOUNDS` and `N-GLOBAL`. These explicit
shared nodes prevent duplicate proof credit for the same approximation, estimate, or compactness
body.

## Node ledger

### root

`M1227-ROOT` is exactly `lerayHopfExistenceTarget`, not smoothness, uniqueness, a finite-time
structure, or a Galerkin approximation.

### s-exact

`M1227-S-EXACT` owns the fixed order of viscosity, datum, positivity, energy and divergence
hypotheses, existential witnesses, and the six solution components.

### s-boundary

`M1227-S-BOUNDARY` retains zero data, excludes zero viscosity, fixes dimension three and `R^3`, and
requires all nonnegative times. The zero and general datum branches must be exhaustive.

### s-foundation

`M1227-S-FOUNDATION` owns classical choice, extensionality, integration, derivative, imported
declaration, axiom, and executable trust decisions. Those remain open.

### n-data

`M1227-N-DATA` is a substantive density theorem: approximate an arbitrary admissible `u0` by smooth
solenoidal data while preserving convergence strong enough for the initial trace.

### n-global

`M1227-N-GLOBAL` owns finite-time to global-time diagonal extraction and compatibility. A family of
unrelated finite-horizon witnesses cannot substitute for one global witness.

### b-zero

`M1227-B-ZERO` constructs the zero solution for zero datum and checks all six conjuncts.

### b-general

`M1227-B-GENERAL` owns nonzero input and branch recomposition. It prevents the degenerate branch
from being presented as general existence.

### c-galerkin

`M1227-C-GALERKIN` constructs finite-dimensional divergence-free solutions and proves their
projected weak equation; mere finite-dimensional existence is not root closure.

### c-bounds

`M1227-C-BOUNDS` derives dimension-uniform kinetic-energy and viscous-dissipation estimates.

### c-compact

`M1227-C-COMPACT` extracts limits with enough compactness for the nonlinear term and identifies the
gradient witness. This is kept below 100 ledger steps only as a project node; its eventual proof
must split further whenever an imported compactness theorem or hidden local-to-global step appears.

### l-gradient

`M1227-L-GRADIENT` passes the integration-by-parts identity to the limit, producing
`IsWeakGradient u g`.

### l-class

`M1227-L-CLASS` turns uniform estimates and lower semicontinuity into the almost-everywhere
integrability conjunct.

### l-divergence

`M1227-L-DIVERGENCE` passes divergence freedom to the limit and obtains the almost-everywhere
trace-free gradient statement.

### l-momentum

`M1227-L-MOMENTUM` passes the time derivative, viscosity, and especially quadratic convection term
to every frozen solenoidal test velocity, including the required integrability.

### l-trace

`M1227-L-TRACE` establishes the exact strong `L2` right trace encoded by `Tendsto`, not merely weak
attainment or almost-every-time convergence.

### l-energy

`M1227-L-ENERGY` proves the energy inequality for every nonnegative time in the chosen
representative. An almost-every-time inequality is not silently substituted.

### t-assemble

`M1227-T-ASSEMBLE` is checked by `isLerayHopfSolution_compose`. It consumes all six exact component
premises. It does not construct witnesses or close any premise, so it gives no unconditional proof.

### x-source

`M1227-X-SOURCE` remains `H2`: exact primary theorem/page, assumptions, original proof route,
translation choices, errata, and independent review are open.

### x-tcb

`M1227-X-TCB` owns the full transitive Lean, mathlib, compiled artifact, axiom, and reproducibility
boundary needed for release.

### x-automation

`M1227-X-AUTOMATION` will record terminal proof bodies and any tactic, simplifier, imported
compactness theorem, solver, or generated certificate. The anchor audit supplies no terminal body.

## Status boundary

Proof requirements have reciprocal `composes` edges. Refinement, provenance, evidence, trust,
documentation, and workflow edges live in separate graphs and cannot close proof nodes. Every node
budget is at most 100 substantive steps, but these estimates are neither proof evidence nor `R0`.

The frozen root cut set is `N-DATA`, `N-GLOBAL`, `C-GALERKIN`, `C-BOUNDS`, and `C-COMPACT`. This
phase claims no accepted proof obligation, H0 review, readable reconstruction, transitive trust
closure, audit completion, theorem completion, or master acceptance.
