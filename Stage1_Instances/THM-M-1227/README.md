# THM-M-1227 rev-5.6 dossier

This directory contains the planned dossier and elaborated canonical target for the Leray-Hopf
weak-solution existence theorem for the incompressible Navier-Stokes equations. `Statement.lean`
chooses the unforced three-dimensional whole-space Leray formulation and explicitly represents the
weak equation, incompressibility, initial trace, and energy inequality.

The repository's Chinese phrase is too short to determine that choice, so source fidelity remains
`H2` pending exact primary-source review. The root vector remains `[H2, M4, R4]`: the exact Lean
expression elaborates, but it has no proof body and receives no proof, audit-completion, or
theorem-completion credit.

`statement.md` freezes the decisions and fidelity boundary. `obligation-registry.json` and
`typed-graphs.json` freeze the pre-proof denominator and separate proof, refinement, provenance,
evidence, trust, documentation, and workflow semantics. `obligation-tree.md` records their readable
projection. The root remains open at `M4`.
