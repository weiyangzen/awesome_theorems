# THM-M-1093 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Fokker-Planck equation. The source label
`已验证` and the historical `S1_M_217.lean` module are discovery inputs only. Neither supplies
accepted source fidelity or proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | A one-dimensional diffusion-density evolution theorem with drift `b`, variance `a`, and equation `partial_t rho = -partial_x (b rho) + (1/2) partial_xx (a rho)` | Precise coefficient spaces, regularity, time interval, boundary behavior, and existence/uniqueness class remain statement obligations |
| Classical form | Pointwise PDE on an explicit time-space domain | Derivative meaning and boundary conditions are not yet source-justified or elaboration-frozen |
| Weak form | Test-function identity `d/dt integral phi rho = integral (L phi) rho` | Test class, integrability, differentiation under the integral, and two integration-by-parts steps remain open |
| Probabilistic bridge | Initial probability law, SDE generator, density/law evolution, mass preservation | No SDE-to-forward-equation theorem is credited |
| Alternatives | Measure-valued forward equation, higher dimensions, manifolds, jumps, bounded domains | Out of canonical scope unless later source audit deliberately revises the intake |
| Foundations | Lean 4 kernel and pinned mathlib analysis/measure/probability APIs | Toolchain, import closure, axioms, and TCB fingerprint remain open |

The proposed formal target is the historical declaration
`AwesomeTheorems.Stage1.S1_M_217.StatementShape`. Its bundled `Prop` fields and existence claim may
be too weak, too strong, or circular relative to a primary source, so the dependent statement phase
must re-elaborate and mutation-test it before it receives any credit.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The initial proof architecture is: source/scope choice; analytic coefficient and initial-data model;
classical PDE or weak formulation; differentiation under the integral; drift and diffusion
integration by parts; probability-law/generator bridge; existence; mass/nonnegativity; uniqueness;
and exact child-to-parent composition. This is architecture, not a frozen obligation registry.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M3, R3]`. The source statement is only a
short repository gloss, and primary-source pinpoints have not been checked. The first failed theorem
gate is therefore source-statement fidelity, followed independently by the Lean statement gate.
The theorem is not complete.

## Validation

The exact intake-only checks and their results are recorded in `validation.md`. They establish
manifest membership, standard consistency, JSON syntax, local cross-reference integrity, and the
absence of forbidden proof declarations in this dossier. They do not validate a Lean target.
