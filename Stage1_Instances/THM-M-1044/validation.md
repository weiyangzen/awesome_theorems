# Intake validation record

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1044` | 0 | rank 237; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1044/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorry\|axiom\|placeholder\|THM-M-0387' README.md intake.json source_statement_crosswalk.md` (from target directory) | 1 | no prohibited proof tokens or copied fixture ID (`rg` exit 1 means no matches) |
| `test "$(find Stage1_Instances/THM-M-1044 -maxdepth 1 -type f \| wc -l)" -eq 4` | 0 | all four intended intake artifacts exist |
| `git diff --check` | 0 | no whitespace errors |

The dossier-local JSON, prohibited-token scan, reference check, and whitespace check are recorded
after artifact creation. This is intake-only validation: no Lean declaration is introduced and no
kernel result is claimed.
