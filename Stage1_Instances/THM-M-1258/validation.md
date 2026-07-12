# Intake validation

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

Validation covers manifest consistency, structured dossier syntax, scoped intake invariants, and
whitespace only. No Lean target exists yet, so this phase records no kernel evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1258` | exit 0; rank 436, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1258/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1258/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1258` | exit 0; no output |

This is the historical intake receipt. `statement-receipt.md` supersedes its former "no Lean target"
boundary for the statement node only. Stable primary-source inspection, anchor audit, obligation
expansion, proof, hermetic replay, and independent review remain open.
