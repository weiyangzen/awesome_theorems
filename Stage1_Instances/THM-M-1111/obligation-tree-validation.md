# Obligation-tree validation receipt

Node: `S56-M-1111-OBLIGATION_TREE`. Base revision:
`f7de69c04a9761094e2b361e94121e5395124106`. Date: 2026-07-12. The pre-existing untracked
`Formalizations/Lean/.lake` link was reused and was neither created nor modified by this phase.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1111/build_obligation_artifacts.py` | 0 | generated 19 obligations; denominator `cf7ead856983378eda1c59efa35309d1a3e5b78599dc0e4f535df33469f36d54` |
| `python3 Stage1_Instances/THM-M-1111/check_obligation_tree.py` | 0 | PASS: 19 obligations and 46 typed edges; root open M3; comparison package M4 |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets with ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1111` | 0 | rank 551; planned; L0/rework-required; theorem incomplete |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); LP="$(cd Formalizations/Lean && lake env printenv LEAN_PATH):Stage1_Instances/THM-M-1111"; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1111 Stage1_Instances/THM-M-1111/Statement.lean -o Stage1_Instances/THM-M-1111/Statement.olean; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1111 Stage1_Instances/THM-M-1111/ObligationTree.lean; rm -f Stage1_Instances/THM-M-1111/Statement.olean Stage1_Instances/THM-M-1111/Statement.ilean` | 0 | pinned Lean 4.29.0 elaborated the statement and exact conditional composition; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`; temporary local interface artifacts were removed |
| `rg -n '(^\|[[:space:]])(sorry\|admit)([[:space:]]\|$)\|^[[:space:]]*axiom[[:space:]]'` on the new Lean and validator sources, followed by `test $? -eq 1` | 0 | no forbidden proof devices or axiom declarations |
| `git diff --check -- Stage1_Instances/THM-M-1111 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

The successful Lean recipe uses only the executable and `LEAN_PATH` emitted by `lake env`; it runs
no Lake update, build, fetch, or dependency mutation. The generated registry and graph SHA-256
digests are `b43d60cebbb4681637a67f9dea64e11c524c622c99a3188a9438fe5a39bccee5` and
`a223815a23b3bd8d370a474de41536f3096ec7ca9f9f73cd6f13628c8436df02` respectively.

## Result boundary

The frozen denominator projection, eligibility lists, required node fields, typed-edge endpoints,
proof reciprocity, acyclicity, reachability, and open closure boundary are self-tested. Lean checks
only the exact conditional child-to-root transport. `FourMomentComparisonPackage S` is definitionally
the root and remains an explicit premise; no analytic result is smuggled into the composition.
The source-faithful semantic implementation, replacement proof, source review, trust closure,
hermetic replay, independent review, audit completion, H0/R0, and theorem completion remain open.
