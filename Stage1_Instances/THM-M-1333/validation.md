# Intake validation record

Validation date: 2026-07-12 (Asia/Shanghai)  
Base revision: `6f601f70dc531aafc2c0e73ea51db67cebeb3ad9`

All commands below were run from the worker-clone root unless a subshell is shown.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1333` | 0 | Rank 874; `THM-M-1333`; baseline `L0`; `rework_required: true`; lane `hard_statement_first_partial_verification`; lifecycle `planned`; theorem incomplete |
| `jq empty Stage1_Instances/THM-M-1333/intake.json Stage1_Instances/THM-M-1333/task-dag.json` | 0 | Both structured artifacts parse as JSON |
| `jq -e '.item_id == "S56-M-1333-INTAKE" and .theorem_id == "THM-M-1333" and .lifecycle_mode == "planned" and .theorem_complete == false and .canonical_formal_target.gate_state == "blocked_pending_exact_statement_and_source_pin"' Stage1_Instances/THM-M-1333/intake.json` | 0 | `true` |
| `jq -e '.theorem_id == "THM-M-1333" and .lifecycle == "planned" and (.accepted_states \| length == 0) and (.tasks \| length == 6) and ([.tasks[].state] \| all(. == "open"))' Stage1_Instances/THM-M-1333/task-dag.json` | 0 | `true` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | `Lean (version 4.29.0, x86_64-unknown-linux-gnu, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release)` |
| `git diff --check -- Stage1_Instances/THM-M-1333` | 0 | No output |
| `rg -n '\b(s[o]rry\|a[x]iom\|a[d]mit)\b' Stage1_Instances/THM-M-1333` | 1 | No matches; expected clean-search exit |

The worker clone exposes the canonical pinned `.lake` artifacts as an existing untracked link; this
task did not mutate or fetch dependencies. Because intake deliberately has no exact formal target,
`lake env lean` was used only to verify availability and identity of the pinned executable. No Lean
elaboration or proof result is claimed.

## Gate boundary

The intake deliverable is self-tested structurally. The statement gate remains open because there is
no independently inspected exact source proposition, normalized expression, environment fingerprint,
or mutation suite. Human source fidelity remains `H2`, machine status remains `M4`, and readability
remains `R3`. Master acceptance is still required before the intake checklist item can be promoted.
