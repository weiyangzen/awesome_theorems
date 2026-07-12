# Formal anchor audit

Item: `S56-M-0161-ANCHOR_AUDIT`  
Base revision: `b33312e792c156f58e747a0f53dfa36691ee0658`

## Verdict

No exact Lean 4 proof candidate was found for the frozen declaration
`Stage1Instances.THM_M_0161.FundamentalTheoremOfSpaceCurvesTarget`. The target therefore remains
`M4`. Pinned mathlib supplies useful ODE existence and uniqueness results and the cross-product
definition, but each is only a future bridge ingredient. None establishes the required global
open-interval curve, its differentiability and invariant equations, or uniqueness under a
determinant-one rigid motion.

## Pinned mathlib inventory

The audited checkout is mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, recorded in the repository Lake manifest and also
confirmed by the dependency checkout's `HEAD`. Its toolchain is `leanprover/lean4:v4.29.0`.

| Candidate | Type-level role | Classification and exact gap |
|---|---|---|
| `IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt` | local ODE existence on `Icc` | Supporting anchor only. It requires an `IsPicardLindelof` package and does not provide global continuation, Frenet invariants, or rigid-motion uniqueness. |
| `ODE_solution_unique_of_mem_Ioo` / `ODE_solution_unique_univ` | uniqueness for Lipschitz ODE solutions | Supporting anchors only. A proof must still encode the Frenet system, discharge Lipschitz and regularity obligations, reconstruct the curve, and prove the determinant-one congruence. |
| `crossProduct` | oriented three-dimensional algebra | Definition anchor already used by `Statement.lean`; it supplies no theorem proof. |

The ODE declarations have ordinary theorem bodies at the pinned revision. The inspected Gronwall
source contains no `sorry` or `admit`, and the Picard-Lindelof existence declaration itself has a
body. This audit does not mistake those dependency bodies for closure of the root theorem.

## External Lean 4 inventory

Sourcegraph searches of public indexed Lean source were run for the exact theorem names, `signed
torsion`, joint `torsion`/`curvature`, and `Frenet`. Exact theorem and torsion searches returned no
matches even when archived repositories and forks were included. The broader Frenet search found
one relevant project:

- `facebookresearch/atlas-lean`, immutable commit
  `34ffed396f376454c1a9b297f3fd74c5c801fb50`, file
  `Atlas/DifferentialGeometry/code/SpaceCurves.lean`, SHA-256
  `ebe6f9de7a951d944a56c348d428ef13e45e934be611fc1e4aeb673fed6bbb2f`.
- The file defines Frenet frames and proves portions of the Frenet-Serret theory, but it contains no
  prescribed-invariants existence theorem or uniqueness under a proper rigid motion.
- It is unusable as proof evidence because the immutable source has explicit `sorry` bodies,
  including `frenetFrame_differentiableAt`, `frenetFrame_orthogonal_higher_iteratedDeriv`, and
  `frenet_frame_det_one`. Other later declarations depend on this incomplete development.
- The project records the same Lean toolchain and mathlib revision as this repository. That makes it
  dependency-compatible in principle, not proof-complete. It was not cloned, fetched, vendored, or
  imported.

Public-code indexing is not exhaustive of private or unindexed projects. The claim here is limited
to the recorded search surfaces and immutable candidates, not universal nonexistence.

## Validation

All commands ran in this worker clone. Existing pinned Lake artifacts were reused without update,
fetch, or dependency mutation.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0161/Statement.lean` | 0 | canonical target still elaborates |
| `lake env lean ../../Stage1_Instances/THM-M-0161/AnchorCandidates.lean` | 0 | all four pinned mathlib candidate names and types elaborate |
| `python3 ../../Stage1_Instances/THM-M-0161/check_statement.py` | 0 | target hash remains `c140d1...f82`; four statement mutations distinguished |
| `python3 -m json.tool Stage1_Instances/THM-M-0161/anchor-audit.json` | 0 | valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard and 1546-target set valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets valid |
| `git diff --check -- Stage1_Instances/THM-M-0161` | 0 | no whitespace errors |

The initial worktree contained the pre-existing untracked `Formalizations/Lean/.lake` link used to
reach canonical pinned artifacts. The audit did not create or modify its dependency contents, but
this remains nonrelease worker evidence.

This is a self-tested anchor-audit proposal pending master acceptance. It does not alter task state,
close the proof, or claim full theorem audit/release.
