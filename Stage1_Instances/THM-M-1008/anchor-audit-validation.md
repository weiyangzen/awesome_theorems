# THM-M-1008 anchor-audit validation

Item: `S56-M-1008-ANCHOR_AUDIT`  
Base revision: `73ef7b942ea9b981648b4c8bc90d810d9a5340a5`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The pinned mathlib revision has useful kernel-checked route anchors: iid laws are preserved under
coordinate reindexing, path laws can be assembled with `IdentDistrib.pi`, measurable preimages then
have equal measures, and a self-independent event has measure zero or one. Mathlib also proves
Kolmogorov's tail zero-one law. None of these declarations turns finite-permutation invariance into
self-independence or tail measurability, so none closes the frozen Hewitt-Savage root.

The historical repo-local module is statement and architecture discovery input. It has related
checked lemmas but no inhabitant of its `StatementShape`, and it is not accepted as a proof of the
new canonical target. A bounded immutable-archive survey of the five external Lean 4 probability
repositories recorded in that module found no terminal Hewitt-Savage candidate. The root therefore
remains `M2`; this audit is self-tested but the theorem is not complete.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-1008` | 0 | rank 288, planned, rework required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `lake env lean ../../Stage1_Instances/THM-M-1008/AnchorAudit.lean` from `Formalizations/Lean` | 0 | all six route declarations elaborated; audited endpoints reported only `propext`, `Classical.choice`, and `Quot.sound` |
| immutable codeload archive search at the five commits in `anchor-audit.json` | 0 | each archive had zero normalized terminal hits; placeholder-file counts were `1,1,0,1,2`; temporary archives were deleted |
| immutable raw `lean-toolchain` reads for those five commits | 0 | toolchains matched `v4.24.0`, `v4.27.0-rc1`, `v4.24.0`, `v4.29.1`, and `v4.29.0-rc3` |
| `python3 Stage1_Instances/THM-M-1008/check_anchor_audit.py` | 0 | pending final run; verifies the clean pin, exact source declarations, negative rows, and `M2` root |
| `python3 -m json.tool Stage1_Instances/THM-M-1008/anchor-audit.json` | 0 | pending final run; structured ledger parses |
| `git diff --check -- Stage1_Instances/THM-M-1008 .stage1-worker-selftest.json` | 0 | pending final run; no whitespace errors |

No `lake update`, build, dependency clone/fetch, or `.lake` mutation was performed. External
archives were inspection-only inputs at explicit commits, not added dependencies. Negative search
evidence is scoped to the listed repositories and revisions and is not a universal nonexistence
claim.
