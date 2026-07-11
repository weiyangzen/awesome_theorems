# THM-M-1516 rev-5.6 intake

This directory is the `planned` intake dossier for **Hamiltonian mechanics**. The upstream wording,
"the Hamiltonian form of classical mechanics," names a theory rather than a uniquely quantified
theorem. Consequently this intake deliberately records `M4`: selecting the legacy proposition would
invent a stronger and more specific source statement.

## Scope map

| Surface | In scope for discovery | Intake boundary |
|---|---|---|
| Source claim | Hamiltonian formulation of classical mechanics | No exact theorem, edition, hypotheses, or conclusion supplied |
| Canonical finite-dimensional model | phase coordinates `(q,p)`, Hamiltonian `H`, canonical `J`, equation `x' = J grad H` | Coordinate-free and constrained variants are not silently identified with it |
| Legendre correspondence | equivalence with Euler-Lagrange equations under a regular Legendre transform | Regularity, smoothness, and local/global domain must be made explicit |
| Conservation | constancy of `H` along autonomous Hamiltonian trajectories | Requires differentiability, chain rule, and skew-symmetry; time-dependent Hamiltonians differ |
| Symplectic dynamics | Hamiltonian flow preserves the symplectic form | Existence interval and differentiability of the flow must be fixed |
| Existing Lean surface | `AwesomeTheorems.Stage1.S1_M_185.StatementShape` and matrix/ODE anchors | Legacy artifact is discovery-only; proposition-valued structure fields make it an axiomatized schema, not closure |
| Foundations | Lean 4 kernel and pinned mathlib | Exact pin, imports, axioms, and computation profile remain open |

The dependent statement phase must choose one literal source-backed root, freeze its ordered binders
and boundary cases, elaborate it with minimal imports, and mutation-test its assumptions. Plausible
roots are not interchangeable: Legendre equivalence, energy conservation, and symplectic-flow
preservation are separate theorems.

## Intake verdict

Lifecycle is `planned`; provisional vector is `[H3, M4, R3]`. The first failed gate is exact source
identification. This intake is self-tested structurally but the theorem is not complete.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The next node is blocked until a primary-source theorem is selected without broadening the label.

## Validation

Commands and exact results are recorded in `validation.md` against base revision
`61369637c5db864082a624c34c62a91e6741f9da`.
