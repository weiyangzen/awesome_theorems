# Intake validation

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

Validation is limited to target-set consistency, dossier syntax/invariants, owned-file scope, and
whitespace. No exact theorem has been selected, so this intake makes no Lean kernel claim.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0435` | exit 0; rank 84, L0/rework required, planned, theorem complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0435/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0435/task-dag.json` | exit 0 |
| scoped Python assertions over instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0435` | exit 0; no output |

Known downstream failures: exact source theorem/variant, hypotheses, and conclusion remain
unselected; no canonical Lean expression, source review, anchor audit, obligation registry, proof,
hermetic replay, or independent review exists. These fail-closed boundaries do not invalidate the
planned intake but prohibit any theorem-completion claim.
