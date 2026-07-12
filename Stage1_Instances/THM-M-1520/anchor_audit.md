# Immutable Lean anchor audit

Audit node: `S56-M-1520-ANCHOR_AUDIT`. Base repository revision:
`b8bb5ebb0eca5910e5a7efdde68c8e8a85f36f7e`. The exact target is
`Stage1.THM_M_1520.LiouvilleStatement` in `Statement.lean`; no candidate below is credited unless it
has that target type or a checked transport to it.

## Pinned mathlib inventory

The worker's existing Lake manifest pins mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with Lean `4.29.0`. A source-tree search at that commit
found no Hamiltonian-mechanics Liouville theorem, Hamiltonian vector-field/flow API, or theorem
turning the selected Hamilton equations into `MeasurePreserving (Phi t) volume volume`.

| Module and declaration | Kernel-checked role | Fit to exact root |
|---|---|---|
| `Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace`; `volume` | selected Lebesgue/Haar measure on finite-dimensional real inner-product spaces | exact conclusion object only |
| `Mathlib.Dynamics.Ergodic.MeasurePreserving`; `MeasurePreserving`, `.map_eq`, `.measure_preimage`, `.comp`, `.id` | target predicate and consequences/composition | substrate; none derives it from Hamilton equations |
| `Mathlib.Analysis.Calculus.Gradient.Basic`; `gradient` | defines the coordinate Hamiltonian vector field used by `Statement.lean` | statement substrate only |
| `Mathlib.LinearAlgebra.SymplecticGroup`; `Matrix.symplecticGroup`, `SymplecticGroup.J_mem`, `.symplectic_det` | linear symplectic matrices; `.symplectic_det` proves `IsUnit A.det` | not a nonlinear flow theorem; the module explicitly leaves determinant exactly one as a TODO |

`AnchorAudit.lean` re-elaborates these declarations and two small type-directed uses. This is anchor
evidence, not a proof of `LiouvilleStatement`. Mathlib files named `Analysis/Complex/Liouville`,
`FieldTheory/Differential/Liouville`, and `NumberTheory/Transcendental/Liouville/*` concern different
theorems and are excluded rather than substituted.

## External Lean candidates

Public GitHub discovery was frozen to the following full commit hashes on 2026-07-12. Tarballs were
read for audit only; no dependency was cloned, fetched, or added to `.lake`.

| Candidate | Immutable revision and environment | Audit result | Dependency feasibility |
|---|---|---|---|
| `velvetmonkey/hamiltonian-lean`, `HamiltonianLean.Liouville.liouville_theorem` | `0c77e2bd3c8bfa2488f14ec7122597eb6bc0a20e`; Lean `v4.28.0`; mathlib `8f9d9cff6bd728b17a24e163c9402775d9e6a365`; MIT | proves `L.jacobian t z = 1` for one degree of freedom. Its `LiouvilleSetup` assumes an abstract `jacobian`, `jacobian_zero`, and the decisive `jacobian_deriv` equation. It neither concludes `MeasurePreserving` nor connects its flow/Jacobian to the derivative of a map. It is a narrower, assumption-heavy surrogate, not an exact closure or usable wrapper. | revision is pin-able in principle, but toolchain/mathlib differ and importing it would not close any exact-root bridge; integration is rejected as no proof credit |
| `hrmacbeth/symplectic` | `acc509702046aaae6a3c9be4546d5735ad7450cf`; Lean `v4.19.0-rc3`; mathlib `ff99cdaecce8cab2fcc3d3828ab7f79717fbf77a` | supplies manifold symplectic-form definitions, standard form, pullback, and symplectic maps. Commit-wide Lean search found no Liouville, Hamiltonian-flow, or measure-preservation theorem. Useful object-model research only. | old incompatible toolchain and no terminal theorem; do not add dependency |
| `mpenciak/symplectic_groups` | `ed323cbbc75ee24e86312c470e7d1e5a1cb344db`; Lean 3 source | linear symplectic matrices and determinant invertibility; this work is already represented by the stronger maintained mathlib module above. No Hamiltonian flow or measure theorem. | Lean 3 and redundant with pinned mathlib; not dependency-feasible |

The apparent external `liouville_theorem` is therefore not imported: doing so would broaden the TCB
without proving the selected proposition and would risk falsely equating an assumed scalar Jacobian
law with phase-volume measure preservation.

## Search and validation receipt

Commands were run from the repository root unless a directory is shown.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1520` | 0 | rank 189, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'liouville\|hamiltonian\|symplectic.*(flow\|volume)\|volume.*symplectic' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | only unrelated Liouville families, graph-theoretic Hamiltonian names, and linear/form-level symplectic material; no exact terminal candidate |
| immutable GitHub tarball searches for the three external revisions above | 0 | results classified in the external table; tarballs were streamed and not installed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1520/AnchorAudit.lean` | 0 | all credited declarations and examples elaborated against the pinned environment |
| `rg -n '(^\|[[:space:]])(sorry\|admit)([[:space:]]\|$)\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-1520` followed by `test $? -eq 1` | 0 | no forbidden proof devices or axiom declarations in the owned artifacts |
| `git diff --check -- Stage1_Instances/THM-M-1520 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

## Verdict and boundary

The anchor inventory is complete for this node and is suitable input to the obligation-tree phase.
It finds no exact pinned mathlib or external Lean 4 closure. The first machine cut is still the
analytic bridge from the stated Hamilton ODE hypotheses to a genuine flow Jacobian/symplectic or
divergence-free theorem, followed by a checked change-of-variables bridge to `MeasurePreserving`.

Lifecycle remains `planned`; root vector remains `[H2, M3, R3]`. This audit does not finish the
primary human-source pinpoint/errata review, prove the root, accept any receipt, or make the theorem
complete. Master acceptance of this provisional node remains required.
