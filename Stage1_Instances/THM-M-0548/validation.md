# Intake validation record

- Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`
- Scope: `S56-M-0548-INTAKE` only
- Network: not required

## Commands and results

The following commands were run from the repository root on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0548` | 0 | rank 120; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; theorem complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0548/intake.json` | 0 | valid JSON |
| dossier-local reference check shown below | 0 | all required files and referenced repo-local paths exist; IDs and planned/noncomplete state agree |
| `git diff --check -- Stage1_Instances/THM-M-0548` | 0 | no whitespace errors |

The dossier-local check is:

```bash
python3 - <<'PY'
import json
from pathlib import Path
p = Path('Stage1_Instances/THM-M-0548')
d = json.loads((p / 'intake.json').read_text())
assert d['item_id'] == 'S56-M-0548-INTAKE'
assert d['theorem_id'] == 'THM-M-0548'
assert d['lifecycle_mode'] == 'planned' and d['theorem_complete'] is False
for name in ('README.md', 'intake.json', 'source_statement_crosswalk.md', 'validation.md'):
    assert (p / name).is_file(), name
assert Path('Docs/Stage1_Blueprint_rev-5.6.md').is_file()
assert Path('Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_120.lean').is_file()
print('THM-M-0548 intake references: ok')
PY
```

These are structural intake checks, not Lean elaboration, source acceptance, proof, or theorem
completion evidence. The dependent statement phase remains open.
