# Intake validation

Base revision: `6d9732600c7da75d9b55873adc3303cf64bd77f2`.

The intake was checked with:

```text
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1133
python3 -m json.tool Stage1_Instances/THM-M-1133/intake.json
python3 -c "import json, pathlib; p=pathlib.Path('Stage1_Instances/THM-M-1133'); d=json.loads((p/'intake.json').read_text()); assert d['item_id']=='S56-M-1133-INTAKE'; assert d['theorem_id']=='THM-M-1133'; assert d['lifecycle_mode']=='planned'; assert d['theorem_complete'] is False; assert all((pathlib.Path(x)).is_file() for x in d['public_merge_targets']); print('THM-M-1133 intake references: ok')"
git diff --check -- Stage1_Instances/THM-M-1133
```

All commands exited `0`. The repository validators reported 15 assurance groups, 41 legacy rows,
300 legacy slots, 1546 uniform-L0 targets, unique ranks 1 through 1546, and confirmed this target at
execution rank 338 in `planned` mode. JSON parsing and dossier-local assertions passed, and
`git diff --check` produced no output.

These are intake checks, not Lean/kernel checks. No `.lean` target exists in this dossier, so the
statement, proof, axiom, provenance, and hermetic gates remain open.
