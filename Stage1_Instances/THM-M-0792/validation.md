# Intake validation record

Base revision: `32404187d6cee70b44ae90adf8d0d765752e5149`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard consistent: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0792` | 0 | Rank 797; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0792/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| dossier integrity check recorded below | 0 | Required identity, lifecycle, state boundary, and public merge targets are consistent |
| prohibited proof-construct scan recorded below | 1 | No `sorry`, `axiom`, or copied fixture ID; exit 1 means no match |
| `git diff --check -- Stage1_Instances/THM-M-0792 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The dossier integrity check is:

```bash
python3 -c 'import json,pathlib; p=pathlib.Path("Stage1_Instances/THM-M-0792"); d=json.loads((p/"intake.json").read_text()); assert d["item_id"]=="S56-M-0792-INTAKE"; assert d["theorem_id"]=="THM-M-0792"; assert d["lifecycle_mode"]=="planned"; assert d["canonical_statement"] is None; assert d["canonical_formal_target"]["gate_state"]=="blocked_pending_source_disambiguation"; assert d["theorem_complete"] is False; assert all(pathlib.Path(x).is_file() for x in d["public_merge_targets"])'
```

The prohibited proof-construct scan is:

```bash
rg -n 'sorry|axiom|THM-M-0387' Stage1_Instances/THM-M-0792
```

No Lean file or declaration is introduced: the intake's exact target is deliberately unresolved,
so running `lake env lean` would not validate a proposition and no kernel result is claimed.
