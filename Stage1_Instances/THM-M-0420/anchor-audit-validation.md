# Anchor audit validation record

Item: `S56-M-0420-ANCHOR_AUDIT`  
Base revision: `d76396d014ed07f02b5e64944c3eafca7d453d40`

## Verdict

The bounded audit found no exact terminal Lean 4 proof. The root classification is `M4`:
mathlib supplies only class-group, finite-prime ramification, Galois, and equivalence
infrastructure. The two immutable external Lean 4 candidates are nonterminal and dependency-
incompatible; the latter is local rather than global class field theory. Negative search results
are explicitly bounded to the recorded trees.

## Immutable external evidence

GitHub recursive-tree API responses were resolved at
`kbuzzard/ClassFieldTheory@11f0a7f3874b6891e8e8290d1e645d61ed06e1aa` (109 Lean files) and
`mariainesdff/LocalClassFieldTheory@9ebdafa0b464df096037c10a2597c40f7e046602` (66 Lean files).
Both responses reported `truncated=false` and a root tree SHA equal to the requested commit.
Their pinned mathlib revisions are respectively
`3bd2603b817feffa4cc0ce9f5d6bad4094ca746e` and
`81a4b04c3ae8a45c367ee1664e82b618694462c4`, neither equal to this repository's pin.
No external dependency was fetched or installed.

## Commands and results

All commands ran in this worker clone. Lean used the existing canonical pinned `.lake` symlink.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0420/AnchorAudit.lean` | 0 | all 10 supporting mathlib declarations elaborated |
| `python3 ../../Stage1_Instances/THM-M-0420/check_anchor_audit.py` | 0 | target hash, pin, probes, bounded absence search, and four classifications agreed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard structure passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets passed |
| `python3 scripts/stage1_target.py show THM-M-0420` | 0 | rank 75, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0420 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

This self-tested node remains pending master acceptance. It does not advance the obligation-tree,
proof, validation, or release phases and does not claim theorem completion.
