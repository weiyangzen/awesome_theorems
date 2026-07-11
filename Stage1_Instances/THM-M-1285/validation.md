# Intake validation record

Base revision: `ef0dd4cd5367b81a98b8906e3325b55fe5263491`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1285` | 0 | rank 456; planned; `hard_mathlib_anchor_and_wrapper`; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1285/intake.json >/dev/null` | 0 | intake record is valid JSON |
| `test "$(find Stage1_Instances/THM-M-1285 -maxdepth 1 -type f \| wc -l)" -eq 4` | 0 | all four intended dossier files exist |
| `rg -n 'S56-M-1285-INTAKE\|THM-M-1285\|Schwarz\|equimeasur' Stage1_Instances/THM-M-1285` | 0 | item identity, corrected terminology, and root property occur in the dossier |
| `git diff --check -- Stage1_Instances/THM-M-1285` | 0 | no whitespace errors |

These are preflight checks, not Lean theorem validation. Dossier JSON parsing, reference checks, and
whitespace validation are recorded by the worker self-test after the files are created. No Lean
command is appropriate in intake because there is intentionally no frozen Lean declaration yet.
