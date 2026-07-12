# THM-M-1515 rev-5.6 intake

This directory is the `planned` dossier for Noether's theorem. The repository's short
description, "correspondence between symmetries and conserved quantities", names a theorem family,
not one proposition: it can mean the finite-dimensional variational theorem, its field-theoretic
generalization, or a converse. This intake selects the classical first theorem for a regular
finite-dimensional Lagrangian system as the canonical scope and explicitly excludes the converse
and field-theory variants. `Statement.lean` now freezes one exact vector-space proposition; its
historical-source fidelity still requires independent review.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Model | A finite-dimensional real normed vector space and a time-independent differentiable Lagrangian `E -> E -> Real` | Manifold-local and explicitly time-dependent variants are excluded |
| Symmetry | A differentiable vertical infinitesimal generator, with quasi-invariance up to the total derivative of `boundary : E -> Real` | Time transformations are excluded; the sign convention is frozen in `IsVariationalSymmetry` |
| Dynamics | `ContDiff Real 2` curves satisfying the covector-valued Euler-Lagrange equation | The equation is global on `Real`, not chart-local |
| Conclusion | `HasDerivAt` zero for momentum paired with the generator minus the boundary term | This is a statement claim only, not a proof of the derivative identity |
| Exclusions | Noether's second theorem, gauge identities, converse Noether theorems, quantum anomalies, PDE field theory, and empirical conservation claims | Separate targets would be required |
| Foundations | Lean 4 kernel and pinned mathlib, with an explicit classical/choice policy | Toolchain, imports, TCB, and axiom profile remain open |

The structured scope is in `intake.json`, source ambiguity and premise mapping are in
`source_statement_crosswalk.md`, and downstream work is frozen in `task-dag.json`. The obligation
phase freezes 12 semantic obligations in `obligation-registry.json` and keeps proof, refinement,
provenance, evidence, trust, documentation, and workflow edges separate in `typed-graphs.json`.

## Current verdict

Lifecycle remains `planned`; provisional root vector is `[H1, M3, R3]`. `H1` records identified
primary historical sources without an accepted edition/page/errata review. `M3` records that the
exact target elaborates but has no credited proof body. The statement, anchor audit, and obligation-
tree nodes are self-tested pending master acceptance. The minimal open proof cut is the momentum-
pairing derivative package plus the boundary-along-curve derivative package. Proof, validation, and
release remain open; there is no audit-completion or theorem-completion claim.
