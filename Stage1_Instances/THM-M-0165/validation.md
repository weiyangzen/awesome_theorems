# Intake validation record

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0165` | 0 | rank 126, `planned`, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0165/intake.json` | 0 | valid JSON |
| `rg -n "THM-M-0165\|S56-M-0165-INTAKE" Stage1_Instances/THM-M-0165` | 0 | item and theorem identifiers found in the owned dossier |
| `git diff --check -- Stage1_Instances/THM-M-0165` | 0 | no whitespace errors |

These are intake-only structural checks. No Lean declaration exists in this phase, so no kernel
proof, exact-type check, or theorem completion is claimed. Known open gates are the exact statement,
source pin and review, anchor audit, obligation registry, proof, and rev-5.6 validation/release gates.
