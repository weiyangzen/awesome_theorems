# Intake validation

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

Commands were run from the repository root on 2026-07-12 (Asia/Shanghai):

| Command | Exit | Result and scope |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1139` | 0 | rank 344, planned, L0/rework_required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1139/intake.json` | 0 | Intake JSON parsed successfully |
| dossier reference check recorded below | 0 | Required files and expected identifiers/boundary strings were present |
| `git diff --check -- Stage1_Instances/THM-M-1139` | 0 | No whitespace errors |

The dossier reference check used:

```bash
python3 - <<'PY'
import json
from pathlib import Path
p = Path("Stage1_Instances/THM-M-1139")
d = json.loads((p / "intake.json").read_text())
assert d["item_id"] == "S56-M-1139-INTAKE"
assert d["theorem_id"] == "THM-M-1139"
assert d["lifecycle_mode"] == "planned"
assert d["canonical_formal_target"]["gate_state"] == "open_source_statement_ambiguity"
assert d["theorem_complete"] is False
for name in ("README.md", "source_statement_crosswalk.md", "validation.md"):
    text = (p / name).read_text()
    assert text.strip()
assert "The theorem is not complete" in (p / "README.md").read_text()
print("THM-M-1139 intake references: ok")
PY
```

No Lean build was run: this intake truthfully has no exact Lean expression or module to elaborate.
That is the recorded `M4` blocker, not proof evidence. These checks self-test only the assigned
intake artifact; master acceptance and every dependent theorem gate remain open.
