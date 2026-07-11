# THM-M-0166 anchor-audit validation

Item: `S56-M-0166-ANCHOR_AUDIT`  
Base revision: `291aeb20bea9e3684c8de5cfca9373fcec398835`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

At immutable mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the closest
checked anchors define Riemannian extended distance, bound it by every `C^1` path, and construct
paths arbitrarily close to its infimum. The metric constructors identify that distance with
`edist`. Proper-space results give compact closed balls and the reverse implication from properness
to completeness. None proves that completeness attains the infimum, much less that one smooth path
minimizes every subsegment.

The legacy repo module is statement and audit scaffolding, not the rev-5.6 root proof. Public
GitHub repository searches and grep.app Lean-index searches found no concrete external Hopf-Rinow
repository candidate. GitHub's code-search endpoint was unavailable without authentication, so the
negative discovery result is explicitly bounded rather than presented as exhaustive.

The exact root remains `M2` and is not kernel-closed. This completes candidate classification for
this phase only and makes no proof, theorem-completion, or master-acceptance claim.

## Commands and exact outcomes

All Lean commands ran from `Formalizations/Lean` using the existing pinned artifacts.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard passed: 15 groups, 41 legacy rows, 300 slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-0166` | 0 | rank 122, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `lake env lean ../../Stage1_Instances/THM-M-0166/Statement.lean` | 0 | frozen exact root elaborated and printed |
| `lake env lean ../../Stage1_Instances/THM-M-0166/AnchorAudit.lean` | 0 | nine adjacent declarations elaborated; three upstream trust reports printed |
| `python3 ../../Stage1_Instances/THM-M-0166/check_anchor_audit.py` | 0 | pin, cleanliness, exact source declarations, negative manifold-source terms, and fail-closed `M2` decision matched |
| GitHub repository API queries for quoted Hopf-Rinow/Lean, Hopf-Rinow/Lean4, and Riemannian geometry/Lean4 | 0 | each returned total count 0 |
| grep.app Lean code-index queries for `HopfRinow` and `Hopf-Rinow` | 0 | each returned zero hits |
| `python3 -m json.tool ../../Stage1_Instances/THM-M-0166/anchor-audit.json >/dev/null` | 0 | structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0166 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, build, dependency network operation, or mutation of `.lake` was performed.
