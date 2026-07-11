# Intake validation record

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

Commands run from the repository root on 2026-07-12 are recorded below after
execution. Intake does not claim a Lean build: exact elaboration belongs to the
dependent statement node.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets with ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0108` | 0 | rank 32, planned, L0, rework required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0108/intake.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0108` | 0 | no whitespace errors |

These are the smallest real checks for the intake phase: repository standard
conformance, exact manifest membership, structured dossier parsing, and patch
hygiene. No historical Lean artifact is accepted by these results.
