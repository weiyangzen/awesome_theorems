# Anchor-audit validation record

Validation date: 2026-07-12 (Asia/Shanghai)  
Base revision: `3f994388953e417edafd54b069ab45d648619698`

All commands were run from the worker-clone root. No dependency update, fetch, or clone was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1333` | 0 | Rank 874; baseline `L0`; lifecycle `planned`; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1333/AnchorAudit.lean)` | 0 | All four candidate probes elaborated; both kernel dependency reports were `[propext, Classical.choice, Quot.sound]`; the checked theorem exposing `IsPicardLindelof.lipschitzOnWith` elaborated |
| `jq empty Stage1_Instances/THM-M-1333/anchor-audit.json` | 0 | Structured audit parses as JSON |
| `jq -e '.item_id == "S56-M-1333-ANCHOR_AUDIT" and .root_machine_debt == "M4" and .theorem_proved == false and .theorem_complete == false and .gate_state == "self_tested_pending_master_acceptance"' Stage1_Instances/THM-M-1333/anchor-audit.json` | 0 | `true` |
| `git diff --check -- Stage1_Instances/THM-M-1333` | 0 | No output |
| `rg -n '\b(s[o]rry\|a[x]iom\|a[d]mit)\b' Stage1_Instances/THM-M-1333` | 1 | No matches; expected clean-search exit |

## Search receipts

Repo-local and pinned-mathlib searches inspected Lean declarations and the complete pinned
`Mathlib/Analysis/ODE` directory. The mathlib source file hash was
`84f6cd4fe5fef3dd4c8e30f6db137f5be80c12678b0bafeaf0bc927181499863`.

Four anonymous GitHub repository-search queries returned valid empty result bodies with SHA-256
`08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2`. The two grep.app code-search
queries failed with HTTP 429 and empty response SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; they are access failures,
not negative evidence.

The phase is self-tested as a bounded, fail-closed anchor audit. It makes no exhaustive-discovery,
proof, `M0-*`, or theorem-completion claim and awaits master acceptance.
