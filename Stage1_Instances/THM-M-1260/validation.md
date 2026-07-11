# Intake validation record

Base revision: `056367be3b1cb2e101200085ec5a5fdff670d16b`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure passed: 1546 uniform-L0 targets and execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1260` | 0 | Rank 437, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1260/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| dossier-local Python assertions for identity, lifecycle, null statement, false completion flags, and public-file references | 0 | All assertions passed |
| `! rg -n '\b(sorry\|axiom)\b\|placeholder\|fake result' Stage1_Instances/THM-M-1260` | 0 | No prohibited proof tokens found |
| `git diff --check -- Stage1_Instances/THM-M-1260 .stage1-worker-selftest.json` | 0 | No whitespace errors |

This is intake-only validation. No Lean declaration exists because the source metadata does not yet
identify a proposition; consequently no elaboration or kernel result is claimed.
