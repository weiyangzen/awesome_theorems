# Intake validation

Base revision: `b893e6c58267baaf373a26b8975e44ef203629da`.

Validation is limited to target membership, repository/manifest consistency, dossier structure,
scoped planned-state invariants, and whitespace. No canonical Lean expression has been selected,
so a Lean elaboration command would validate a substituted statement and is intentionally not
claimed for this intake.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0536` | exit 0; rank 593, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0536/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0536/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0536` | exit 0; no output |

Known downstream failures are explicit: primary-source pinpoint review, coefficient and grading
conventions, canonical Lean elaboration and expression hash, mutation tests, anchor audit,
obligation registry, proof, hermetic replay, and independent review remain open. They prevent audit
and theorem completion but do not invalidate this fail-closed planned intake.
