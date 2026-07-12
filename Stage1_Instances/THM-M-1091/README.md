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

## Statement phase handoff

The dependent statement phase now proposes
`Stage1Instances.THM_M_1091.ChapmanKolmogorovTarget` in `Statement.lean`. It selects the
homogeneous discrete-time Markov-kernel reading as the narrowest direct formal expansion of the
repository's "semigroup property of transition probabilities" gloss. `statement.json` freezes
the explicit expression and environment hashes, while `target_iff_integralTarget` checks the
measurable-set integral form. Four structural mutations and both zero-step boundaries are tested
by the recipes in `statement-validation.md`.

This is statement-only evidence pending master acceptance. The general inhomogeneous three-time
family and continuous-time semigroup remain uncredited alternate scopes, and primary-source
fidelity remains an anchor-audit obligation. No theorem proof or completion is claimed.

## Anchor-audit handoff

The anchor audit now freezes the pinned mathlib candidates and an exact checked bridge in
`AnchorAudit.lean`. `Kernel.pow_add` closes the frozen kernel expression after swapping the named
step counts and normalizing addition; `Kernel.pow_add_apply_eq_lintegral` directly closes the
checked integral encoding. Exact source bodies and transitive axioms were inspected at mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. Repo-local legacy wrappers are duplicates,
and the external search found no separately admissible exact candidate.

This is a self-tested anchor inventory pending master acceptance. The exact bridge is only an
`M0-P` candidate until the dependent obligation-tree and proof phases adopt it. Human-source debt
remains `H1`, all later validation and release gates remain open, and theorem completion is false.

## Obligation-tree handoff

Registry version 1 freezes twelve canonical obligations and seven separate typed graph classes
before proof-phase closure credit is observed. `ObligationTree.lean` checks the exact conditional
composition: a named power-add child is instantiated at swapped indices and `add_comm` yields the
frozen chronological root. Both zero-step boundaries also elaborate. The pinned
`Kernel.pow_add` body is the unique central bridge identity; wrappers receive no duplicate credit.

This architecture is self-tested pending master acceptance. The root stays open at
`M1091-L-POWADD` until the proof phase adopts the audited anchor. H0/R0 review, transitive trust,
hermetic and independent validation, release, and theorem completion remain open.
