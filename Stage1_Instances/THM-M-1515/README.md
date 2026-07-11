# THM-M-1515 rev-5.6 intake

This directory is the `planned` intake dossier for Noether's theorem. The repository's short
description, "correspondence between symmetries and conserved quantities", names a theorem family,
not one proposition: it can mean the finite-dimensional variational theorem, its field-theoretic
generalization, or a converse. This intake selects the classical first theorem for a regular
finite-dimensional Lagrangian system as the canonical scope and explicitly excludes the converse
and field-theory variants. Exact conventions still require source and statement review.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Model | A smooth finite-dimensional configuration manifold, time-dependent Lagrangian on its tangent bundle, and smooth one-parameter transformations | Lean object model and regularity classes remain to be chosen |
| Symmetry | Infinitesimal invariance of the action, allowing invariance up to a total time derivative | Sign conventions and boundary term are not yet frozen |
| Dynamics | Twice differentiable curves satisfying the Euler-Lagrange equations | Coordinate-free versus chart-local encoding remains open |
| Conclusion | The Noether charge obtained from momentum paired with the infinitesimal generator, minus the boundary term, is constant along each solution | No exact Lean expression or checked derivative calculation exists yet |
| Exclusions | Noether's second theorem, gauge identities, converse Noether theorems, quantum anomalies, PDE field theory, and empirical conservation claims | Separate targets would be required |
| Foundations | Lean 4 kernel and pinned mathlib, with an explicit classical/choice policy | Toolchain, imports, TCB, and axiom profile remain open |

The structured scope is in `intake.json`, source ambiguity and premise mapping are in
`source_statement_crosswalk.md`, and downstream work is frozen in `task-dag.json`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. `H1` records identified primary
historical sources without an accepted edition/page/errata review. `M4` is deliberate: the broad
repository label does not identify an exact Lean proposition, and no candidate expression has been
elaborated. The first failed theorem gate is exact statement identity. This intake is self-tested
as a scope artifact only; it makes no audit-completion or theorem-completion claim.

