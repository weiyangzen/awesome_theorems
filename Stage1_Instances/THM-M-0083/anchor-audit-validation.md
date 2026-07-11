# THM-M-0083 anchor-audit validation

Item: `S56-M-0083-ANCHOR_AUDIT`  
Date: 2026-07-12 (Asia/Shanghai)  
Base revision: `45225aadff56e3948bc75a950e5287a960a002b5`

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact terminal family in `Mathlib.CategoryTheory.RepresentedBy`.
`IsRepresentable.iff_exists_isRepresentedBy` supplies the existential
representation criterion and `isRepresentedBy_iff` expands its witness to the
same every-object bijectivity map frozen in `Statement.lean`. The independently
restated adapter elaborates and its axiom probe reports only mathlib's expected
`propext`, `Classical.choice`, and `Quot.sound` foundation profile.

The repository-local `S1_M_139` theorem is a duplicate wrapper over that same
terminal family, not an independent proof body. Searches found no additional
credible external Lean 4 candidate, but public code search was unavailable, so
the external inventory is explicitly bounded rather than claimed exhaustive.

## Commands

All commands ran from the repository root unless a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets |
| `python3 scripts/stage1_target.py show THM-M-0083` | 0 | rank 139, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned mathlib worktree clean |
| `python3 Stage1_Instances/THM-M-0083/check_anchor_audit.py` | 0 | immutable pins, hashes, exact wrapper markers, and status boundary verified |
| `lake env lean ../../Stage1_Instances/THM-M-0083/AnchorAudit.lean` (`cwd=Formalizations/Lean`) | 0 | exact adapter elaborated; upstream and wrapper axiom probes agree |
| `lake env lean ../../Stage1_Instances/THM-M-0083/Statement.lean` (`cwd=Formalizations/Lean`) | 0 | predecessor's frozen exact target still elaborates |
| `python3 -m json.tool Stage1_Instances/THM-M-0083/anchor-audit.json >/dev/null` | 0 | structured audit is valid JSON |
| `rg -n '\b(sorry|axiom|admit)\b' Stage1_Instances/THM-M-0083/AnchorAudit.lean Stage1_Instances/THM-M-0083/check_anchor_audit.py` | 1 (expected) | no prohibited declaration or placeholder in executable audit artifacts |
| `git diff --check -- Stage1_Instances/THM-M-0083 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Boundary

This self-test supports the anchor-audit node only, pending master acceptance.
The candidate root classification is `M0-W`; it does not establish theorem
completion. Human-source H0, frozen obligations and typed graphs, transitive
provenance/trust closure, readable reconstruction, hermetic/offline replay,
independent verification, and release receipts remain later gates.
