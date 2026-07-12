# Statement validation record

Validation date: 2026-07-12 (Asia/Shanghai)  
Base revision: `562c428c3d520ab42bba305174b7cad9409d7c0b`

All commands below were run from the worker-clone root.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1333` | 0 | Rank 874; target is uniform `L0 / rework_required`, lifecycle `planned`, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1333/check_statement.py` | 0 | Expression SHA-256 `4ecb0c59750f3a7df0ec655cc4e7527dde459d3c8a186811c37c1b0b8120f78e`; all four named mutations killed; toolchain `leanprover/lean4:v4.29.0`; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `jq empty Stage1_Instances/THM-M-1333/statement.json` | 0 | Structured statement certificate parses as JSON |
| `jq -e '.item_id == "S56-M-1333-STATEMENT" and .statement_elaborated == true and .theorem_proved == false and .theorem_complete == false and .gate_state == "self_tested_pending_master_acceptance"' Stage1_Instances/THM-M-1333/statement.json` | 0 | `true` |
| `git diff --check -- Stage1_Instances/THM-M-1333` | 0 | No output |
| `rg -n '\b(s[o]rry\|a[x]iom\|a[d]mit)\b' Stage1_Instances/THM-M-1333` | 1 | No matches; expected clean-search exit |

The checker invokes `lake env lean` narrowly on `Statement.lean` and temporary print variants. It
does not update, fetch, or mutate dependencies. The existing `.lake` link points at the canonical
pinned artifacts.

## Gate boundary

The statement deliverable is self-tested and awaits master acceptance. It establishes exact
elaboration, not a proof of the proposition. Source acceptance, anchor audit, obligation-tree,
proof, hermetic validation, and release remain open; theorem completion remains false.
