# Intake validation

Validation is limited to target membership, repository-standard consistency, JSON syntax, owned dossier invariants, and whitespace. This intake contains no Lean declaration, so it claims no elaboration or kernel result.

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

Exact commands and results are recorded after execution.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets validated |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0117` | exit 0; rank 37, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0117/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0117/task-dag.json` | exit 0 |
| scoped Python assertions over both JSON files and the exact owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0117` | exit 0; no output |

Known open gates: primary-source identification and disambiguation, exact Lean elaboration, obligation audit, proof, and release evidence. These are downstream gates and do not represent completion of the theorem.
