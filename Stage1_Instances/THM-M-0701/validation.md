# Intake validation

Base revision: `74980872e6ba4cca3e08b1b728b5cf3695421b94`.

The preflight worktree contained the pre-existing untracked
`Formalizations/Lean/.lake` entry. This intake did not modify it. The run is
therefore worker evidence, not release evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0701` | 0 | Rank 742; lane `hard_statement_first_partial_verification`; lifecycle `planned`; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0701/intake.json >/dev/null` | 0 | Intake JSON is syntactically valid |
| dossier invariant check shown below | 0 | Identity, lifecycle, null exact target, M4 blocker, no completion claims, public targets, and required files agree |
| `git diff --check -- Stage1_Instances/THM-M-0701 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The dossier invariant check was:

```bash
python3 - <<'PY'
import json
from pathlib import Path

root = Path("Stage1_Instances/THM-M-0701")
d = json.loads((root / "intake.json").read_text())
assert d["item_id"] == "S56-M-0701-INTAKE"
assert d["theorem_id"] == "THM-M-0701"
assert d["execution_rank"] == 742
assert d["lifecycle"] == "planned"
assert d["statement_resolution"]["state"] == "blocked_source_is_not_a_proposition"
assert d["canonical_formal_target"]["declaration_or_expression"] is None
assert d["debt"]["machine"].startswith("M4:")
assert d["theorem_complete"] is False and d["audit_complete"] is False
for p in d["public_merge_targets"]:
    assert Path(p).is_file(), p
for name in ("README.md", "scope.md", "source_statement_crosswalk.md", "validation.md"):
    assert (root / name).is_file(), name
print("THM-M-0701 intake invariants: ok")
PY
```

No Lean elaboration command is applicable: the dossier deliberately contains
no Lean expression because the repository source does not identify a
proposition. Inventing an expression merely to run `lake env lean` would
violate the exact-statement gate. This is the first failed downstream gate.
