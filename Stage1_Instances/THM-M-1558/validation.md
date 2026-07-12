# Intake validation

Base revision: `955bd0889d93d62c132eb6ec63d2d1572479357b`.

Validation is limited to target membership, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. No canonical Lean expression exists yet, so a `lake env lean` elaboration
would not cover any claimed declaration and no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1558` | exit 0; rank 570, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1558/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1558/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1558` | exit 0; no output |

Known downstream failures: a unique source proposition, primary-source equation/theorem/page and
errata inspection, exact AKNS conventions and boundary cases, canonical Lean elaboration, anchor
audit, obligation registry, proof, hermetic replay, and independent review remain open. They block
theorem completion but do not invalidate this fail-closed planned intake.
