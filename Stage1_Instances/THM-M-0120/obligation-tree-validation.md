# THM-M-0120 obligation-tree validation

Item: `S56-M-0120-OBLIGATION_TREE`  
Date: `2026-07-12` (Asia/Shanghai)  
Base revision: `5f9b9aa5be620b78a09a5b1b2fd877e0c9051251`

## Frozen result

Registry version 1 freezes 25 root-relevant obligations and 62 edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. All 25 obligations are
eligible for machine, human-source, and readable coverage. The canonical denominator digest is
`69152b161a10b5ce6099fb09c48320330d6d35f63a11411ad14ccb84963081b1`.

The root and already elaborated statement/interface nodes remain `M3`; all substantive
birational-geometry and theorem nodes remain `M4`. No obligation is closed. The explicit root cut
set records missing klt/numerical-intersection foundations, cone decomposition and rational
generator arguments, local finiteness, and contraction construction/universality.

## Commands and results

All commands ran in this worker clone. Lean reused the existing pinned `.lake` artifacts. No update,
build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0120/build_obligation_artifacts.py` | 0 | deterministically wrote 25 obligations and 62 typed edges; emitted the denominator digest above |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | schemas, frozen input hashes, denominator, seven graph classes, reciprocal indices, acyclicity, full root reachability, budgets, recipes, and open closure boundary passed |
| `python3 -m json.tool` on the registry, graph bundle, and validation specs | 0 | all three structured artifacts are valid JSON |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0120/ObligationTree.lean` | 0 | conditional four-package composition elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0120 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This evidence self-tests only the obligation freeze, graph invariants, and conditional logical
assembly. It supplies no missing geometric premise or proof body. H0, R0, transitive trust review,
independent replay, `AUDIT-Z`, `THEOREM-Z`, theorem completion, release, and master acceptance remain
open. The pre-existing untracked `Formalizations/Lean/.lake` worker artifact makes this nonrelease
evidence.
