# Intake validation

Base revision: `68bccb854a8ce9bdd5fbdfdda203abe0bb3819eb`.

Validation is limited to target membership, repository consistency, dossier structure, scoped
intake invariants, and whitespace. No canonical Lean expression exists in this planned phase, so no
kernel elaboration or proof result is claimed. The pre-existing untracked `Formalizations/Lean/.lake`
link/artifact makes this dirty-worktree evidence and was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0186` | exit 0; rank 673, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0186/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0186/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0186` | exit 0; no output |

Known downstream failures: exact source pinpoint and independent review, a canonical Lean target and
environment fingerprint, mutation tests, obligation registry, anchor audit, proof, hermetic replay,
and independent validation remain open. They prevent audit and theorem completion but do not
invalidate this fail-closed planned intake.
