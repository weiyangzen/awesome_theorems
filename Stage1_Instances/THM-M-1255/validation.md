# Intake validation record

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1255` | 0 | rank 160, planned, L0/rework_required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1255/intake.json` | 0 | valid JSON |
| dossier-local integrity command recorded below | 0 | required files, IDs, planned lifecycle, and non-completion boundary present |
| `git diff --check -- Stage1_Instances/THM-M-1255 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The integrity command is:

```bash
python3 - <<'PY'
import json
from pathlib import Path
p = Path('Stage1_Instances/THM-M-1255')
d = json.loads((p / 'intake.json').read_text())
assert d['item_id'] == 'S56-M-1255-INTAKE'
assert d['theorem_id'] == 'THM-M-1255'
assert d['lifecycle_mode'] == 'planned'
assert d['theorem_complete'] is False
for name in ('README.md', 'source_statement_crosswalk.md', 'validation.md'):
    assert (p / name).is_file()
assert 'No theorem completion' in (p / 'README.md').read_text()
print('THM-M-1255 intake integrity: ok')
PY
```

This is structural intake validation, not Lean elaboration or kernel evidence. Lean validation is
correctly deferred because the assigned node is intake and the exact statement remains unresolved.
