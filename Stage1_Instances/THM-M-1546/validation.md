# Intake validation

Validation was run from the repository root at base revision
`594dbb735284e7b81f51ce813a9c3200fd55f610`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, contiguous ranks, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1546` | exit 0; rank 205, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1546/intake.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1546/task-dag.json` | exit 0 |
| dossier reference and forbidden-claim scan using `rg` | exit 0; identifiers present and no `sorry`, `axiom`, placeholder, or completion claim found |
| `git diff --check -- Stage1_Instances/THM-M-1546` | exit 0 |

These checks self-test only the planned intake dossier and open task DAG. This phase creates no Lean
declaration, so it claims no elaboration or kernel evidence. Exact statement, source audit, proof,
and master acceptance remain later gates.
