# Intake validation

Validation is limited to manifest membership, repository-standard consistency, JSON syntax, dossier invariants, and whitespace. No new Lean declaration belongs to this intake, so no kernel result is claimed.

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets accepted |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0124` | exit 0; rank 43, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0124/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0124/task-dag.json` | exit 0 |
| scoped Python assertions over both JSON files and the exact owned artifact set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0124` | exit 0; no output |

Known open downstream gates are canonical Lean elaboration, page-level primary-source audit, independent review, proof closure, and release evidence. They are not failures of this intake phase.
