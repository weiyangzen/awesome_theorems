# Intake validation

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. The legacy Lean file was inspected but not revalidated or credited in this intake.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0994` | exit 0; rank 274, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0994/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0994/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0994` | exit 0; no output |

Known downstream failures: primary-source text and errata review, canonical Lean elaboration,
anchor/provenance audit, frozen obligation graphs, proof acceptance, hermetic replay, and independent
review remain open. They prevent theorem completion but do not invalidate this planned intake.
