# Intake validation

Base revision: `f1411d9611fd9a140123ade3316fdecb3a0b3f25`.

The preflight worktree contained the pre-existing untracked `Formalizations/Lean/.lake` link. This
intake did not modify or fetch dependencies under `.lake`.

## Commands and results

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0590` | 0 | Target found at execution rank 630, `L0`, `rework_required: true`, lane `hard_statement_first_partial_verification`, lifecycle `planned`, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0590/intake.json >/dev/null` | 0 | Intake JSON parsed successfully |
| dossier-local integrity check recorded below | 0 | Required files, IDs, lifecycle, root vector, incomplete status, DAG order, and public merge targets agree |
| `git diff --check -- Stage1_Instances/THM-M-0590` | 0 | No whitespace errors |

The dossier-local check used Python's standard JSON parser and asserted:

```text
item_id == S56-M-0590-INTAKE
theorem_id == THM-M-0590
execution_rank == 630
lifecycle_mode == planned
root_vector == {human: H1, machine: M3, readability: R3}
theorem_complete is false
open_task_dag is the seven manifest phases in dependency order
every public_merge_target exists
README.md and source_statement_crosswalk.md exist
```

No `lake env lean` command is applicable to this intake phase: it intentionally creates no Lean
module or declaration, and the exact formal expression is an explicit output of the dependent
statement phase. Consequently this receipt is structural evidence for a planned dossier, not
kernel evidence for the theorem or its statement.
