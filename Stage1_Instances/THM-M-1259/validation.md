# Intake validation record

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1259` | 0 | rank 161; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1259/intake.json >/dev/null` | 0 | JSON syntax valid |
| dossier-local reference check (see command below) | 0 | every relative dossier-file reference exists |
| `git diff --check -- Stage1_Instances/THM-M-1259` | 0 | no whitespace errors |

Reference-check command:

```bash
python3 - <<'PY'
import pathlib, re
root = pathlib.Path('.')
docs = pathlib.Path('Stage1_Instances/THM-M-1259')
refs = set()
for p in docs.iterdir():
    if p.suffix in {'.md', '.json'}:
        refs.update(re.findall(r'Stage1_Instances/THM-M-1259/[A-Za-z0-9_.-]+', p.read_text()))
missing = [ref for ref in sorted(refs) if not (root / ref).exists()]
assert not missing, missing
print(f'reference check: ok ({len(refs)} relative references)')
PY
```

These checks validate the intake structure only. No Lean build is applicable because this phase
truthfully leaves the exact formal target open; consequently they provide no theorem proof credit.
