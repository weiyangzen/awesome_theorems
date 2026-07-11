# Intake validation

Base revision: `7ea3aa8c0960c44b00d62639e9ddf1321848e342`.

| Command | Result | Scope |
|---|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0: standard and 1546-target coverage OK | repository structure |
| `python3 scripts/stage1_target.py check` | exit 0: 1546 unique targets, ranks 1..1546, uniform L0 | manifest integrity |
| `python3 scripts/stage1_target.py show THM-M-1330` | exit 0: rank 492, planned, L0/rework_required | membership and metadata |
| `python3 -m json.tool Stage1_Instances/THM-M-1330/intake.json >/dev/null` | exit 0 | dossier JSON syntax |
| `git diff --check -- Stage1_Instances/THM-M-1330` | exit 0 | whitespace integrity |

These checks self-test the intake artifact only. No Lean build, source-fidelity acceptance, machine
proof, or theorem completion is claimed.
