# Intake validation record

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0170` | 0 | rank 123, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0170/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0170/task-dag.json >/dev/null` | 0 | open task DAG is valid JSON |
| `rg -n '\\b(sorry|axiom)\\b|placeholder|theorem_complete[[:space:]]*:[[:space:]]*true' Stage1_Instances/THM-M-0170/{README.md,intake.json,source-statement-crosswalk.md,task-dag.json}` | 1 | no forbidden proof claims or placeholders (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-0170 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. It validates repository membership and
artifact structure, not the mathematical source crosswalk or any Lean theorem. Master acceptance
and all dependent phases remain outstanding.

## Statement validation (2026-07-12)

Base revision: `41a639c14626145f43eda7724d6a570cd710d688`.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0170/Statement.lean` | 0 | Exact target, `Iff.rfl` serialization, and four guarded negative mutations elaborate; printed declaration has no metavariables; `statement_iff` axioms are `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0170` | 0 | rank 123, planned, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0170/statement.json >/dev/null` | 0 | statement receipt is valid JSON |

The Lean command reuses the canonical pinned `.lake` artifacts and performs no dependency update.
This validates statement elaboration, not existence of an embedding or theorem closure.
