# Intake validation record

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

The preflight commands were run before dossier creation:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0446` | 0 | rank 64; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `git status --short` | 0 | clean output before dossier creation |
| `git rev-parse HEAD` | 0 | `5997161aebf527e8a1e05724d4fbd4ce07dfd815` |

Post-creation validation is appended below after running the checks. This intake introduces no Lean
declaration, so JSON, reference, forbidden-token, and whitespace checks are the smallest real
validation surface. Master acceptance and every dependent phase remain outstanding.

| Command | Exit | Result |
|---|---:|---|
| `python3 -m json.tool Stage1_Instances/THM-M-0446/intake.json >/dev/null` | 0 | intake is valid JSON |
| `rg -n 'sorry\|axiom\|placeholder\|fake result' Stage1_Instances/THM-M-0446` | 1 | no forbidden proof mechanisms or fake-result wording found; exit 1 is ripgrep's no-match result |
| `rg -n 'THM-M-0446\|S56-M-0446-INTAKE' Stage1_Instances/THM-M-0446` | 0 | dossier identity and owned-path references found in the structured intake, README, and validation record |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard remains valid with 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | ordered 1546-target manifest remains valid |
| `git diff --check` | 0 | no whitespace errors |
| `git status --short` | 0 | only the untracked owned directory `Stage1_Instances/THM-M-0446/` is reported |
