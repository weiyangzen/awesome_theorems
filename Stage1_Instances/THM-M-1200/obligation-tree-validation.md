# Obligation-tree validation receipt

Item: `S56-M-1200-OBLIGATION_TREE`. Base revision:
`f4b142975b0cf41e1c092e006544346545ed8b8c`. Date: 2026-07-12. The pre-existing
untracked `Formalizations/Lean/.lake` link was reused and not modified.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1200/build_obligation_artifacts.py` | 0 | generated 14 obligations; frozen registry projection denominator `9915c4444fa19015a1a5aa3413871c87dafe1aeafb0ef4ab8540cacc01c54931` |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | PASS: 14 obligations and 54 typed edges; root open at M4; nonzero-trace construction open at M4 |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets with ranks 1 through 1546 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1200/ObligationTree.lean` | 1 | expected module-path setup failure: `Statement` was outside the Lake package search root; this attempt receives no validation credit |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); LP="$(cd Formalizations/Lean && lake env printenv LEAN_PATH):Stage1_Instances/THM-M-1200"; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1200 Stage1_Instances/THM-M-1200/Statement.lean -o Stage1_Instances/THM-M-1200/Statement.olean; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1200 Stage1_Instances/THM-M-1200/ObligationTree.lean; rm -f Stage1_Instances/THM-M-1200/Statement.olean Stage1_Instances/THM-M-1200/Statement.ilean` | 0 | pinned Lean 4.29.0 elaborated the statement and exact conditional composition; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`; temporary interface artifacts were removed |
| `rg -n '(^\|[[:space:]])(sorry\|admit)([[:space:]]\|$)\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-1200` followed by `test $? -eq 1` | 0 | no forbidden proof devices or axiom declarations |
| `git diff --check -- Stage1_Instances/THM-M-1200 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

The successful Lean recipe uses only the executable and search path supplied by `lake env`. Its
temporary local interface artifacts are removed; it performs no Lake update, build, fetch, clone,
or dependency mutation.

## Result boundary

The receipt self-tests the frozen denominator, complete node schema, typed endpoints and reciprocal
proof edges, graph acyclicity and root reachability, and the honest open closure boundary. Lean
checks that the explicitly named nonzero-trace construction package is sufficient for the exact
frozen root. It does not construct that package. Human-source pinpoint review, proof bodies,
transitive trust/provenance closure, H0/R0, hermetic and independent validation, master acceptance,
and theorem completion remain open.
