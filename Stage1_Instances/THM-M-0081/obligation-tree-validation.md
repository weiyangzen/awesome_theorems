# THM-M-0081 obligation-tree validation

Date: 2026-07-12. Base revision: `f9413ba75c44c7b473fce84209ab02c65afd10cd`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0081/build_obligation_artifacts.py` | 0 | Wrote 11 obligations; frozen denominator `f38e8efb...bbf69d`. |
| `python3 Stage1_Instances/THM-M-0081/check_obligation_tree.py` | 0 | PASS: 11 obligations, 21 typed edges; root open at M4. |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0081/ObligationTree.lean)` | 0 | `root_compose` elaborated; axioms reported as `propext`, `Classical.choice`, `Quot.sound`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard valid: 15 groups, 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546. |
| `python3 scripts/stage1_target.py show THM-M-0081` | 0 | Rank 138, L0/rework required, theorem incomplete. |
| `git diff --check -- Stage1_Instances/THM-M-0081` | 0 | No whitespace errors. |

One initial path invocation from `Formalizations/Lean` used a repository-relative Python path and
failed with exit 2 because that working directory was wrong. It was corrected by running the Python
checks from the repository root; no validation claim relies on the failed invocation.

The existing untracked `Formalizations/Lean/.lake` link/artifact was present at preflight and was not
modified. Validation reused the pinned environment and did not run update, build, clone, or fetch.
This is scoped, dirty-worker evidence, not hermetic release or independent verification evidence.
