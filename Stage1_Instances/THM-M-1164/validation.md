# Intake validation record

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard consistent: 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1164` | 0 | Rank 367, planned, L0/rework_required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1164/intake.json` | 0 | Valid JSON |
| dossier reference check (recorded below) | 0 | Required files and referenced public merge targets exist |
| `git diff --check -- Stage1_Instances/THM-M-1164 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The reference check is:

```bash
python3 -c 'import json,pathlib; p=pathlib.Path("Stage1_Instances/THM-M-1164"); d=json.loads((p/"intake.json").read_text()); assert d["item_id"]=="S56-M-1164-INTAKE"; assert d["theorem_id"]=="THM-M-1164"; assert d["lifecycle_mode"]=="planned"; assert d["theorem_complete"] is False; assert all(pathlib.Path(x).is_file() for x in d["public_merge_targets"]); assert all((p/x).is_file() for x in ("README.md","source_statement_crosswalk.md","validation.md"))'
```

No Lean build is claimed: intake deliberately leaves the formal expression and module unset for the
dependent statement phase.
