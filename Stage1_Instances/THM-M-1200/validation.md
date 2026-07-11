# Intake validation record

- Base revision: `7a8e792e568c85805fef02f4071bcc4b5ac9e09d`
- Scope: `S56-M-1200-INTAKE` only
- Result: self-tested planned intake; master acceptance remains pending

Commands run from the repository root on 2026-07-12 (Asia/Shanghai):

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | Rank 394, planned, L0/rework required, theorem incomplete |
| `jq -e '<intake invariants>' Stage1_Instances/THM-M-1200/intake.json` | 0 | Printed `true`; schema, item, lifecycle, ID, open statement gate, and incomplete status match |
| `test -s` on the four dossier deliverables | 0 | All files nonempty |
| `git diff --check -- Stage1_Instances/THM-M-1200` | 0 | No whitespace errors |

No Lean command is claimed for this intake phase: the selected target intentionally has no Lean
module or declaration until the dependent statement phase chooses a faithful weak-formulation API.
Thus this record validates dossier structure and honest open-state boundaries, not elaboration,
kernel closure, source fidelity, or theorem completion.
