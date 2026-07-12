# THM-M-1091 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the Chapman-Kolmogorov equation,
glossed by the repository as the semigroup property of transition probabilities. The
intake preserves the common claim that transition from an earlier time to a later time
factors through every intermediate time. The repository source does not say whether time
is discrete or continuous, whether the kernels are homogeneous, or which measurable-space
regularity assumptions are intended, so those choices are not silently resolved here.

Pinned mathlib contains an unusually close candidate: `ProbabilityTheory.Kernel.pow_add`
and its integral form `ProbabilityTheory.Kernel.pow_add_apply_eq_lintegral` in
`Mathlib.Probability.Kernel.Composition.Comp`. They encode the discrete-time homogeneous
case using powers of one endokernel. This is candidate discovery at intake, not an accepted
identification with the source claim and not proof credit.

The provisional root vector is `[H1, M3, R3]`. A named book reference appears in the
mathlib declaration, but its edition, exact statement, assumptions, and errata have not
been independently audited. The Lean candidate is pinned and available, but the dependent
statement phase has not frozen an exact expression, checked the source transport, or run
the required mutation suite. No audit or theorem completion is claimed.

The dossier consists of `intake.json`, `scope-map.md`,
`source-statement-crosswalk.md`, the open `task-dag.json`, and the exact intake checks in
`validation.md`. `IntakeProbe.lean` checks only that the candidate declarations elaborate.

## Intake verdict

Lifecycle is `planned`. The intake deliverable is self-tested, while master acceptance is
still required. The first downstream gate is exact statement identity: an accountable
source review must choose the general time-indexed formulation or justify the homogeneous
discrete-time specialization before the Lean statement can receive credit.
