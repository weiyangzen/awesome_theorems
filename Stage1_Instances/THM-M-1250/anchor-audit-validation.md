# THM-M-1250 anchor-audit validation

Item: `S56-M-1250-ANCHOR_AUDIT`  
Base revision: `950964e64a8a340a562abdc58bb0987c439a6f11`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The manifest-pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact semantic anchor. `SchwartzMap` is a structure whose `smooth'` and `decay'`
fields match the two conjuncts of the frozen target. `SchwartzMap.smooth` and
`SchwartzMap.decay` are checked forward projections; `le_seminorm` and
`seminorm_le_bound` connect the bounds to mathlib's topology-facing API.

Public repository metadata searches found no separate relevant Lean 4 project. The similarly named
Schwartz-Zippel repository concerns polynomial identity testing and is not a candidate for Schwartz
function space. This negative discovery result is explicitly non-exhaustive.

The audit classifies the root `M1`: the exact proof route is available at a clean immutable pin, but
this phase does not implement the root wrapper. Thus the anchor audit is self-tested while the
theorem remains incomplete.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1250` | 0 | rank 430, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned dependency worktree clean |
| `lake env lean ../../Stage1_Instances/THM-M-1250/AnchorAudit.lean` from `Formalizations/Lean` | 0 | constructor, smoothness, decay, and seminorm candidates elaborated; axiom sets printed |
| `python3 Stage1_Instances/THM-M-1250/check_anchor_audit.py` | 0 | pin, manifest, clean worktree, exact source declarations, and fail-closed root classification matched |
| GitHub repository API queries for `SchwartzMap`, `Schwartz space`, and `rapidly decreasing` with `language:Lean` | 0 | zero relevant repositories returned; broader result was the unrelated Schwartz-Zippel lemma |
| `python3 -m json.tool Stage1_Instances/THM-M-1250/anchor-audit.json` | 0 | structured ledger is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1250 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, build, clone, fetch, or `.lake` mutation was performed. This evidence advances
only the audit node pending master acceptance; proof, validation, and release remain open.
