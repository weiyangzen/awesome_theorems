# Intake validation record

Base revision: `73a92b5e63e8eb3c93a5c95d5aead1658ca24c79`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard OK; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1264` | 0 | rank 441, planned, L0/rework required, not complete |
| `python3 -m json.tool Stage1_Instances/THM-M-1264/intake.json` | 0 | valid JSON |
| dossier assertion command recorded below | 0 | ID/schema agree; canonical target is deliberately null; theorem_complete is false |
| `git diff --check -- Stage1_Instances/THM-M-1264 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The dossier assertion command is:

```bash
python3 -c 'import json; p="Stage1_Instances/THM-M-1264/intake.json"; d=json.load(open(p)); assert d["schema_version"] == "stage1-instance/5.6.0"; assert d["item_id"] == "S56-M-1264-INTAKE"; assert d["theorem_id"] == "THM-M-1264"; assert d["canonical_statement"] is None; assert d["canonical_formal_target"]["gate_state"] == "blocked_missing_exact_human_statement"; assert d["theorem_complete"] is False'
```

This is the smallest real validation for an intake whose exact proposition is unavailable. No Lean
elaboration was run because there is no eligible expression to elaborate.
