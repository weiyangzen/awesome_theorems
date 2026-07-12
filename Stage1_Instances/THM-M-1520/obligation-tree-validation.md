# Obligation-tree validation receipt

Node: `S56-M-1520-OBLIGATION_TREE`. Base revision:
`6d7db94bb24d91df72f83fd7a393db356a7bb93b`. Date: 2026-07-12. The pre-existing
`Formalizations/Lean/.lake` symlink is untracked in this worker clone and was neither created nor
modified by this phase.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1520/build_obligation_artifacts.py` | 0 | generated 16 obligations; denominator `3e5ecbc29279547f4e05323bfea6cdbda08b8e69545cffba35df81df8b460e4c` |
| `python3 Stage1_Instances/THM-M-1520/check_obligation_tree.py` | 0 | PASS: 16 obligations, 32 typed edges; root open M3; analytic package M4 |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets with ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1520` | 0 | rank 189; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1520/ObligationTree.lean` | 1 | expected module-path setup failure: the source import was outside Lake's package search root; this attempt supplies no validation credit |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); LP="$(cd Formalizations/Lean && lake env printenv LEAN_PATH):Stage1_Instances/THM-M-1520"; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1520 Stage1_Instances/THM-M-1520/Statement.lean -o Stage1_Instances/THM-M-1520/Statement.olean; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1520 Stage1_Instances/THM-M-1520/ObligationTree.lean; rm -f Stage1_Instances/THM-M-1520/Statement.olean Stage1_Instances/THM-M-1520/Statement.ilean` | 0 | pinned Lean 4.29.0 elaborated the statement and conditional composition; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`; temporary local interface artifacts were removed |
| `rg -n '(^\|[[:space:]])(sorry\|admit)([[:space:]]\|$)\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-1520` followed by `test $? -eq 1` | 0 | no forbidden proof devices or axiom declarations |
| `git diff --check -- Stage1_Instances/THM-M-1520 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

The successful Lean recipe uses the executable and `LEAN_PATH` emitted by `lake env`, and only
creates the local `Statement.olean` needed to resolve `import Statement`; it performs no Lake
update, build, fetch, or dependency mutation.

## Result boundary

The registry projection hash, denominator lists, required node fields, typed-edge endpoints,
reciprocity, proof acyclicity/reachability, and open closure boundary are self-tested. Lean checks
the exact conditional child-to-root interface. The analytic premise is not constructed, so this is
not root proof evidence. Audit completion, source review, trust closure, hermetic replay, H0/R0,
master acceptance, and theorem completion remain open.
