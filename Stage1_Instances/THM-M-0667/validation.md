# Intake validation record

Base revision: `16187d91397de4edab8cb93140166f634baa0c02`.

This record covers dossier structure, target identity, pinned-environment
availability, and scope hygiene only. Intake intentionally adds no Lean
declaration, so the Lean command checks the pinned executable rather than
claiming target elaboration or kernel proof evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0667` | 0 | rank 711, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-0667/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0667/intake-receipt.json >/dev/null` | 0 | worker receipt is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0667` | 0 | no whitespace errors |

The canonical Lean statement, expression fingerprint, mutation tests, source
audit, obligation registry, proof, axiom report, hermetic replay, and master
acceptance remain dependent-phase work.

