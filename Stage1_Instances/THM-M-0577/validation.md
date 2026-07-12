# Intake validation

Base revision: `1794fae27ddcf6d19b6984502e27a9233890d8d1`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, and whitespace. No unique mathematical proposition or canonical Lean expression can
be selected from the source metadata, so no `lake env lean` elaboration or kernel-proof result is
applicable or claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0577` | exit 0; rank 689, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0577/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0577/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0577` | exit 0; no output |

Known downstream failures: theorem identity and a pinpoint primary source, independent source
review, canonical Lean statement and elaboration, anchor audit, obligation registry, proof,
hermetic replay, and release validation remain open. They prevent theorem completion but do not
invalidate a truthful fail-closed planned intake.
