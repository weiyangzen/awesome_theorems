# Intake validation

Base revision: `73a92b5e63e8eb3c93a5c95d5aead1658ca24c79`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. There is no canonical Lean expression at intake, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1279` | exit 0; rank 450, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1279/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1279/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1279` | exit 0; no output |

Known downstream failures: primary-source page/theorem inspection and errata review, exact formula
and normalization, Lean elaboration, anchor audit, obligation registry, proof, hermetic replay, and
independent review remain open. These prevent theorem completion but do not invalidate a truthful
planned intake.
