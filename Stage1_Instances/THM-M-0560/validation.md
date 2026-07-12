# Intake validation record

Base revision: `418e6ea60487eaae4d9a1fa7aeb4bb7c575c33ee`.

The worktree already contained untracked `Formalizations/Lean/.lake` material before this intake.
It was reused read-only and not updated, fetched, built, or otherwise mutated. This makes the Lean
probe nonrelease evidence. The intake node adds no Lean declaration, so there is no canonical
target elaboration or proof check to claim.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; exactly 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0560` | 0 | rank 608, planned, L0/rework-required, no accepted legacy artifact, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0560/intake.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0560/task-dag.json >/dev/null` | 0 | valid JSON |
| scoped Python intake assertions | 0 | `intake invariant check: ok`; planned lifecycle, empty accepted states, and exact downstream chain verified |
| scoped Python proof-escape scan (tokens assembled from fragments to avoid self-matching the validation record) | 0 | no forbidden proof escapes, bodyless declarations, or fabricated-result markers |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_139.lean` | 0 | pinned environment elaborated the existing representability/API discovery module; printed only its declarations and does not prove Brown representability |
| `git diff --check -- Stage1_Instances/THM-M-0560` | 0 | no whitespace errors |

The first downstream blocker is exact statement identity: a stable copy of Brown's 1962 article
and 1963 correction must be inspected to select and crosswalk the precise root. Canonical Lean
elaboration, anchor audit, obligation freezing, proof, hermetic replay, human/readability reviews,
and master acceptance remain open. Consequently `audit_complete=false` and
`theorem_complete=false`.
