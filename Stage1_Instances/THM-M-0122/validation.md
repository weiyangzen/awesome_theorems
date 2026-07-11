# Intake validation record

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

Commands run from the repository root on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0122` | 0 | rank 41, `planned`, `L0`, rework required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0122/intake.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0122/task-dag.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0122` | 0 | no whitespace errors |

No Lean build is claimed. Intake does not accept or modify the legacy
provisional statement; exact native elaboration is owned by the dependent
statement node. The smallest real validation for this phase is manifest and
standard conformance, structured dossier parsing, and diff hygiene.
