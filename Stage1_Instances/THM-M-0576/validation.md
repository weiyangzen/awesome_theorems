# Intake validation

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

Commands are run from the repository root. Results below concern the intake phase
only and are not Lean theorem evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0576` | 0 | rank 108; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0576/intake.json` | 0 | valid JSON |
| dossier-local required-file/reference check (see worker receipt) | 0 | required files and declared merge targets exist; this intake adds no Lean proof file |
| `git diff --check -- Stage1_Instances/THM-M-0576` | 0 | no whitespace errors |

Known open gates: exact source-version selection, source hashes and errata review,
canonical Lean elaboration, environment fingerprint, checked transports, mutations,
obligation registry, anchor audit, proof, and all release validation.
