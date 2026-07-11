# Intake validation

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

The following checks were run from the repository root after creating the dossier. They validate
only this intake artifact, not the mathematical theorem or a Lean statement.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0024` | 0 | rank 296; baseline L0; `rework_required: true`; lifecycle `planned`; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0024/intake.json >/dev/null` | 0 | intake JSON parses |
| dossier-local integrity command recorded below | 0 | required files, item/theorem IDs, lifecycle, false completion flag, and local Markdown references agree |
| `git diff --check -- Stage1_Instances/THM-M-0024` | 0 | no whitespace errors |

Integrity command:

```bash
python3 - <<'PY'
import json
from pathlib import Path
p = Path("Stage1_Instances/THM-M-0024")
d = json.loads((p / "intake.json").read_text())
assert d["item_id"] == "S56-M-0024-INTAKE"
assert d["theorem_id"] == "THM-M-0024"
assert d["lifecycle_mode"] == "planned"
assert d["theorem_complete"] is False
for name in ("README.md", "source_statement_crosswalk.md", "validation.md"):
    assert (p / name).is_file()
for target in d["public_merge_targets"]:
    assert Path(target).is_file()
print("THM-M-0024 intake integrity: ok")
PY
```

Known open gates: immutable source receipt and pinpoint crosswalk; exact formal signature; Lean
elaboration and mutation tests; environment fingerprint; obligation registry; proof, trust,
provenance, readability, hermetic replay, and independent acceptance.
