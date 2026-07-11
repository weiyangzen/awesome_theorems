# THM-M-0583 anchor-audit validation

Item: `S56-M-0583-ANCHOR_AUDIT`  
Base revision: `27314f63340f00cfc0abe5e57d8bfb9eb2331fd7`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The pinned mathlib module has the generalized topological Poincare type as a source-level
`proof_wanted` marker. It is not an importable proof constant. The retained repo-local
`S1_M_116` module likewise contains statement and audit wrappers, not a terminal proof.

At immutable revision `540da9...f61`, `lean-dojo/LeanMillenniumPrizeProblems` states the
generalized theorem but proves only dimension zero. At immutable revision `686d32...146`,
`google-deepmind/formal-conjectures` has an exact dimension-four declaration whose body is
`by sorry`. Its Lean 4.27.0/mathlib `a3a10d...900` pins also differ from this repository.

The exact root therefore remains `M2`, not kernel-closed. This completes candidate classification
for this anchor-audit phase only and makes no theorem-completion claim.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0583` | 0 | rank 116, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0583/AnchorAudit.lean` | 0 | exact candidate type and self-homeomorphism sanity endpoint elaborated; endpoint axioms printed |
| `python3 Stage1_Instances/THM-M-0583/check_anchor_audit.py` | 0 | local pins/source gates and both immutable external classifications matched; root remained `M2` |
| `python3 -m json.tool Stage1_Instances/THM-M-0583/anchor-audit.json` | 0 | structured audit ledger is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0583 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The external verifier reads raw files by immutable commit URL; it does not clone, fetch, add, or
build either dependency. No `lake update`, `lake build`, or `.lake` mutation was performed.

## Status boundary

Anchor discovery and classification are self-tested pending master acceptance. The missing
placeholder-free four-dimensional proof and pinned exact transport are the remaining root cut set.
H0 source review, the obligation tree, proof, hermetic validation, independent review, release,
and theorem completion remain open.
