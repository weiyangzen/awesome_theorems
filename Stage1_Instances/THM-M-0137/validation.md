# Intake validation

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

Validation is limited to manifest/standard consistency, dossier JSON syntax and scoped invariants,
and whitespace. No exact Lean target was selected, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0137` | exit 0; rank 53, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0137/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0137/task-dag.json` | exit 0 |
| scoped Python assertions over the instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0137` | exit 0; no output |

Known downstream failures: the source wording is ambiguous; the canonical human claim and Lean
expression are not frozen; primary-source page/theorem inspection, exact elaboration, proof,
hermetic replay, and independent review remain open. These prevent theorem progress but do not
invalidate this fail-closed intake.
