# THM-M-0593 proof-phase validation

Item: `S56-M-0593-PROOF`
Validation date: `2026-07-15` (`Asia/Shanghai`)
Base revision: `718e166c56e53c552ebb861ee01427f9a606fc72`

## Implemented bodies

`Proof.lean` supplies unconditional, placeholder-free bodies for the two
elementary dimension branches of the frozen architecture.

For `M0593-B-ZERO`, every continuous linear map into
`EuclideanSpace Real (Fin 0)` is surjective, so `criticalPointsOn f R` is
empty and its image has zero volume. For `M0593-L-DIMENSION-IMAGE` and
`M0593-B-LOWDIM`, smoothness on the open region makes `f` locally Lipschitz
at every critical point. Mathlib's Hausdorff-dimension image bound gives
`dimH (f '' criticalPointsOn f R) <= m < n`; the definition of Euclidean
Hausdorff measure and its equality with Euclidean `volume` then give the
required nullity.

`sardTarget_of_hardDimensionBranch` checks the exact branch composition
again, now with the zero and low-dimensional bodies inserted. Its sole
premise is the still-open `HardDimensionBranch`. This supports provisional
machine state `M2`, not root closure: the remaining root cut is
`M0593-L-RANK-REDUCTION` and `M0593-L-TAYLOR` inside the hard Morse-Sard
argument. The accepted registry and graph files remain unchanged for master
reconciliation.

## Commands and results

All Lean commands reused the existing canonical pinned `.lake` artifacts.
No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation
was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-0593/check_proof.sh` | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated in an isolated temporary directory; all three proof declarations were sorry-free; each axiom report was exactly `[propext, Classical.choice, Quot.sound]`; the structural receipt checker passed |
| `python3 Stage1_Instances/THM-M-0593/check_obligation_tree.py` | 0 | `PASS THM-M-0593 obligation tree: 22 obligations, 43 typed edges`; frozen registry still truthfully reports its pre-proof open M4 boundary |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0593` | 0 | rank 633, planned, legacy artifacts unaccepted, theorem incomplete |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe\|extern)\b\|implemented_by\|native_decide' Stage1_Instances/THM-M-0593/Proof.lean` | 1, expected | empty output; no prohibited proof device |
| `python3 -m json.tool Stage1_Instances/THM-M-0593/proof-receipt.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0593/proof-blocker.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool .stage1-worker-selftest.json >/dev/null` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0593 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The environment is Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; the mathlib worktree is clean.

This is self-tested partial proof execution. The hard branch, H0/R0,
foundation and provenance closure, downstream validation/release, hermetic
replay, independent verification, master acceptance, and theorem completion
remain open.
