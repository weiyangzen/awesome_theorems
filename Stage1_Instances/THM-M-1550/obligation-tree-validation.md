# THM-M-1550 obligation-tree validation

Date: `2026-07-12`. Base revision: `e1aeca70d414df009dea3559577ea90aa9834089`.

All commands ran inside this worker clone. Lean reused the pinned canonical `.lake` artifacts; no
update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1550/build_obligation_artifacts.py` | 0 | Wrote 10 obligations; denominator `c5237144...79730`. |
| `python3 Stage1_Instances/THM-M-1550/check_obligation_tree.py` | 0 | PASS: 10 obligations, 19 reciprocal typed edges, required-node reachability, acyclicity, frozen denominators, zero closure, and root cut verified. |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1550/ObligationTree.lean)` | 0 | Conditional `root_compose` elaborated; reported axioms are `propext`, `Classical.choice`, and `Quot.sound`. |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1550/Statement.lean)` | 0 | Frozen canonical statement and mutations still elaborate. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard valid: 15 groups and 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1550` | 0 | Rank 209, planned, L0/rework-required, theorem incomplete. |
| `rg -n "\\bsorry\\b\|\\badmit\\b\|\\bunsafe\\b\|^axiom " Stage1_Instances/THM-M-1550/ObligationTree.lean` | 1 | No placeholder, unsafe declaration, or added axiom; exit 1 is ripgrep's no-match result. |
| `git diff --check -- Stage1_Instances/THM-M-1550` | 0 | No whitespace errors. |

One initial Python invocation was mistakenly issued from `Formalizations/Lean` with a root-relative
path and exited 2 because the file was not found. It was corrected from the repository root; no
validation claim relies on that failed invocation.

This is scoped dirty-worker evidence pending master acceptance, not a hermetic or independent
release receipt. The architecture freezes zero closed obligations and does not prove the theorem.
