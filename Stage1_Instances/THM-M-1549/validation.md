# Intake validation

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. No canonical Lean expression exists at this phase, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1549/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1549/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1549` | exit 0; rank 208, L0/rework_required, planned, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-1549` | exit 0; no output |

Known downstream failures: exact rigorous source theorem/page and errata inspection, analytic and
normalization decisions, canonical Lean elaboration, anchor audit, obligation expansion, proof,
hermetic replay, and independent review remain open. They prevent theorem completion but do not
invalidate this fail-closed planned intake.
