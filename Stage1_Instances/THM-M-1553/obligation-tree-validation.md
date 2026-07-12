# Obligation-tree validation receipt

Node: `S56-M-1553-OBLIGATION_TREE`. Base revision:
`c05c0fd312ac67c73431151907f2a4e8f6269664`. Date: 2026-07-12. The pre-existing
untracked `Formalizations/Lean/.lake` link was reused and was not modified.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1553/build_obligation_artifacts.py` | 0 | generated 14 obligations; denominator `553f66664b7a640a7e299ac12a65bfcf668173fbfb556f179614ae1dd4fbfed1` |
| `python3 Stage1_Instances/THM-M-1553/check_obligation_tree.py` | 0 | PASS: 14 obligations, 33 typed edges; root open M3; logarithmic-derivative bridge M4 |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets with ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1553` | 0 | rank 212; planned; L0/rework-required; theorem incomplete |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); LP="$(cd Formalizations/Lean && lake env printenv LEAN_PATH):Stage1_Instances/THM-M-1553"; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1553 Stage1_Instances/THM-M-1553/Statement.lean -o Stage1_Instances/THM-M-1553/Statement.olean; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1553 Stage1_Instances/THM-M-1553/ObligationTree.lean; rm -f Stage1_Instances/THM-M-1553/Statement.olean Stage1_Instances/THM-M-1553/Statement.ilean` | 0 | pinned Lean 4.29.0 elaborated the conditional composition; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`; temporary interface artifacts removed |
| `rg -n '(^\|[[:space:]])(sorry\|admit)([[:space:]]\|$)\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-1553` with failure on a match | 0 | no forbidden proof devices or axiom declarations |
| `git diff --check -- Stage1_Instances/THM-M-1553 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

The Lean recipe uses only the executable and `LEAN_PATH` supplied by `lake env`; it performs no
Lake update, build, fetch, or dependency mutation.

## Result boundary

The frozen projection hash, denominator lists, node ledgers and budgets, typed-edge endpoints,
reciprocity, proof acyclicity/reachability, and open closure boundary are self-tested. Lean checks
the exact conditional child-to-root composition. It does not construct `LogDerivativeBridge`, so
this is not root proof evidence. Source review, trust closure, H0/R0, hermetic replay, independent
review, master acceptance, and theorem completion remain open.
