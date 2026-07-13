# THM-M-0063 obligation-tree validation

Item: `S56-M-0063-OBLIGATION_TREE`. Base revision:
`cea7a197878ce23e819b006b2780b0bb1702fbbe`, tree
`079dc70c0b48278054700d1b4d45efee14a3bd04`.

Validation ran in the isolated worker clone on 2026-07-13. The initial worktree difference was only
the automation-provided untracked `Formalizations/Lean/.lake` symlink to the canonical pinned
environment. The symlink and packages were used read-only. No `lake update`, `lake build`, clone,
fetch, dependency write, or network-dependent validation was run. This dirty worker packet is
nonrelease evidence.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0063` | 0 | rank 1094; planned; theorem_complete false |
| `python3 -B Stage1_Instances/THM-M-0063/build_obligation_artifacts.py --write` | 0 | wrote 22 obligations and 61 typed edges; denominator `384a00c490054109773a2b786763af466971bd50c093a6facd39b614133b74a1` |
| `python3 -B Stage1_Instances/THM-M-0063/build_obligation_artifacts.py --check` | 0 | deterministic registry, graph, and validation-spec bytes match the generator |
| `python3 -B Stage1_Instances/THM-M-0063/check_obligation_tree.py` | 0 | 22 unique obligations; 61 legal typed edges; master DAG-bound workflow; reciprocal proof edges; open M3 root; empty accepted closure; temporary Statement olean and ObligationTree check; Lean output SHA-256 `dee26ca1...3b82` |
| `python3 -m json.tool` on `instance.json`, registry, graph bundle, validation specs, and receipt | 0 | all structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0063-obligation-pycache python3 -m py_compile Stage1_Instances/THM-M-0063/build_obligation_artifacts.py Stage1_Instances/THM-M-0063/check_obligation_tree.py` | 0 | both Python tools compile outside the repository |
| `if rg -n -i '\b(sorry\|admit\|sorryax\|axiom\|unsafe\|oracle\|placeholder)\b' Stage1_Instances/THM-M-0063/ObligationTree.lean; then exit 1; else echo PASS; fi` | 0 | no prohibited proof marker matched |
| `git diff --check -- Stage1_Instances/THM-M-0063 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Checked boundary

The structural validator recomputes the canonical denominator, binds the exact `Statement.lean`
and `anchor-audit.json` byte hashes, checks every required node field and substantive `<=100` step
ledger, verifies all seven graph classes and reciprocal proof edges, rejects proof-graph cycles,
checks root reachability and conditional certificate child sets, validates the three structured
recipes, and enforces the open-root receipt boundary.

The checker first compiles `Statement.lean` to a temporary olean, then checks the obligation module
with that directory first in `LEAN_PATH`; the root composition therefore returns the actual
`Stage1Instances.THM_M_0063.CayleyTheoremTarget`, not an unlinked copy. The Lean module proves only
composition from explicit interfaces. It never imports the proof-bearing Cayley module, invokes
`Equiv.Perm.subgroupOfMulAction`, or supplies the generalized package. The
root remains `[H1, M3, R4]`, `accepted_closed_obligations=[]`, `audit_complete=false`, and
`theorem_complete=false`. The first failed gate is integration-lane acceptance of the provisional
anchor prerequisite and this receipt. Proof integration, H0, R0, complete provenance/trust,
hermetic replay, independent validation, release, and master acceptance remain open.
