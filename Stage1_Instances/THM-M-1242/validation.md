# Intake validation

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

This phase validates only target membership, dossier structure, scoped invariants, and formatting.
No Lean declaration is introduced, so no elaboration or kernel-proof result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1242` | 0 | rank 423, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1242/instance.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1242/task-dag.json >/dev/null` | 0 | valid JSON |
| scoped Python assertions over the six owned artifacts | 0 | `intake invariant check: ok`; planned lifecycle and six open downstream tasks |
| `git diff --check -- Stage1_Instances/THM-M-1242` | 0 | no whitespace errors |

Known downstream failures are source inspection and independent review, exact Lean elaboration and
mutation tests, immutable anchor audit, obligation composition, proof closure, hermetic replay, and
release review. They prevent theorem completion but do not invalidate this planned intake.
