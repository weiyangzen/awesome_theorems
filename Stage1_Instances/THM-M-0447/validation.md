# Intake validation

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

Commands are run from the repository root. Exit codes and summaries below are evidence for the
intake dossier only; they do not establish statement exactness or theorem closure.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0447` | 0 | rank 65, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0447/intake.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0447 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Known open gates: exact source statement, Lean elaboration and fingerprint, concrete object model,
source audit, frozen obligation registry, proof closure, trust/provenance, hermetic replay, and
independent acceptance.
