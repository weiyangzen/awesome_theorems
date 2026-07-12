# Anchor-audit validation record

Item: `S56-M-0708-ANCHOR_AUDIT`  
Base revision: `136ebf643dcdcbc42cef34e415177189578060ef`  
Date: `2026-07-12` (`Asia/Shanghai`)

The pinned mathlib tree at revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains `ComputablePred.rice` in `Mathlib.Computability.Halting`. Its conclusion says that a
computable semantic code predicate containing a represented `f` must contain every represented
`g`. The wrapper in `AnchorAudit.lean` checks that contradiction with the frozen negative witness
has exactly the strength needed by THM-M-0708.

## Validation

| Command | Exit | Result |
|---|---:|---|
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0708/AnchorAudit.lean)` | 0 | wrapper elaborated; `ComputablePred.rice` and wrapper both report only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0708/check_anchor_audit.py` | 0 | receipt, manifest revision, pinned source, and wrapper checks pass |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0708` | 0 | rank 749, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0708` | 0 | no whitespace errors |

The cache link/materialization `Formalizations/Lean/.lake` pre-existed this task and was not
modified. No dependency update, fetch, clone, or build was run. This is nonrelease worker evidence.
The proof phase has not adopted the wrapper, and theorem completion is not claimed.
