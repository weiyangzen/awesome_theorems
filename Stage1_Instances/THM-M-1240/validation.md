# Intake validation record

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1240` | 0 | rank 421, planned, L0/rework-required, historical status untrusted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1240/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `test $(find Stage1_Instances/THM-M-1240 -maxdepth 1 -type f \| wc -l) -eq 5` | 0 | the dossier has its five expected intake artifacts |
| `rg -o 'Stage1_Instances/THM-M-1240/[A-Za-z0-9_.-]+' Stage1_Instances/THM-M-1240/intake.json \| while read -r f; do test -f "$f" \|\| exit 1; done` | 0 | every dossier-local public merge target exists |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for the intake node. The two prose occurrences of `axiom`
describe an uncredited policy/deceptive-encoding boundary; no Lean declaration, proof term, or
kernel result is introduced. Master acceptance and all dependent phases remain outstanding.
