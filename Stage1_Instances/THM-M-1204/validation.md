# Intake validation record

Base revision: `7a8e792e568c85805fef02f4071bcc4b5ac9e09d`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1204` | 0 | rank 398, planned, theorem incomplete, hard anchor/wrapper lane |
| `python3 -m json.tool Stage1_Instances/THM-M-1204/intake.json` | 0 | valid JSON |
| `rg -n "sorry\|axiom\|placeholder\|theorem_complete.*true" Stage1_Instances/THM-M-1204 \|\| test $? -eq 1` | 0 | no forbidden proof placeholder or false completion marker found |
| `git diff --check -- Stage1_Instances/THM-M-1204` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only, deliberately unelaborated dossier. No Lean
kernel result is claimed. Known open gates are primary-source pinpointing, exact statement selection,
Lean elaboration and environment fingerprinting, proof, trust/provenance, and independent review.
