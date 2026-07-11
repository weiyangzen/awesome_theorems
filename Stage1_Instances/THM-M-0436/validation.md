# Intake validation

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

Commands are run from the repository root. Results below are for the final owned artifacts.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0436` | 0 | rank 85, planned, L0/rework_required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0436/intake.json >/dev/null` | 0 | intake JSON parses |
| owned-path reference and proof-artifact check recorded in the worker receipt | 0 | all referenced owned files exist and the intake adds no Lean proof artifact |
| `git diff --check -- Stage1_Instances/THM-M-0436` | 0 | no whitespace errors |

No Lean proof is introduced by the intake phase. Consequently a Lean build would not validate the
new dossier's outstanding exact-statement gate and is not presented as node evidence.
