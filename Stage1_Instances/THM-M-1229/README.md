# THM-M-1229 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the Serrin regularity
criterion for incompressible Navier-Stokes weak solutions. Historical Stage1
material is discovery input only and contributes no accepted proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Classical three-dimensional Prodi-Serrin velocity criterion | Primary-source wording and exact local/global variant remain open |
| PDE objects | weak solution, divergence-free condition, energy class, initial/boundary data | No canonical mathlib Navier-Stokes weak-solution object has been accepted |
| Integrability | mixed `L^q_t L^p_x` velocity membership | The legacy file stores this as an opaque proposition, so it is not the exact target |
| Exponents | `p > 3` and `2/q + 3/p <= 1` | Endpoint and infinity encodings require statement audit and mutation tests |
| Analytic bridge | convection estimate, energy estimate, bootstrap, weak-to-strong regularity | Architecture only; no closure is claimed |
| Conclusion | interior regularity on a nondegenerate spacetime region | Exact differentiability and pressure claims remain open |
| Foundations | Lean 4 kernel and pinned mathlib | Toolchain, imports, axioms, and TCB fingerprint remain open |

The canonical claim, unresolved choices, boundary probes, and initial scope
nodes are structured in `intake.json`. Source relationships and the distinction
between the historical scaffold and an exact formalization are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first
failed theorem gate is the exact Lean statement gate: no accepted source
pinpoint, normalized expression hash, environment fingerprint, checked
transport, or mutation suite exists. This intake is self-tested structurally,
but neither the audit nor the theorem is complete.

## Validation

Commands and exact outcomes are recorded in `validation.md`. They establish
manifest membership, standard consistency, JSON syntax, dossier references,
and diff hygiene only.
