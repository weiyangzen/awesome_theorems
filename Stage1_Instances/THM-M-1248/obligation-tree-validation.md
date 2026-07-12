# Obligation-tree validation receipt

Node: `S56-M-1248-OBLIGATION_TREE`. Base revision:
`3d70df6fcb9b415d87ecf4a29d431ea67cd23b3f`. Date: 2026-07-12. The pre-existing
untracked `Formalizations/Lean/.lake` link was reused as the canonical pinned dependency surface
and was not modified.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1248/build_obligation_artifacts.py` | 0 | generated 18 obligations; denominator `a0c3a82c3c3655d323873c8e3dc1164bbe6021d60d32521261f7d82cdcceaa11` |
| `python3 Stage1_Instances/THM-M-1248/check_obligation_tree.py` | 0 | PASS: 18 obligations and 43 typed edges; root open M3; weighted analytic package M4 |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets with ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1248` | 0 | rank 428; planned; L0/rework-required; theorem incomplete |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); LP="$(cd Formalizations/Lean && lake env printenv LEAN_PATH):Stage1_Instances/THM-M-1248"; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1248 Stage1_Instances/THM-M-1248/Statement.lean -o Stage1_Instances/THM-M-1248/Statement.olean; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1248 Stage1_Instances/THM-M-1248/ObligationTree.lean; rm -f Stage1_Instances/THM-M-1248/Statement.olean Stage1_Instances/THM-M-1248/Statement.ilean` | 0 | pinned Lean 4.29.0 elaborated the frozen statement and exact conditional composition; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`; temporary local interface artifacts were removed |
| `python3 -m json.tool Stage1_Instances/THM-M-1248/obligation-registry.json >/dev/null` and the corresponding `typed-graphs.json` command | 0 | both structured artifacts parse as JSON |
| `rg -n '(^\|[[:space:]])(sorry\|admit)([[:space:]]\|$)\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-1248/ObligationTree.lean` followed by `test $? -eq 1` | 0 | no forbidden proof device or axiom declaration |
| `git diff --check -- Stage1_Instances/THM-M-1248` | 0 | no scoped whitespace errors |

The Lean recipe obtains both the executable and `LEAN_PATH` from `lake env`; it performs no Lake
update, build, fetch, or dependency mutation.

## Result boundary

The frozen projection hash, denominator lists, node fields, typed-edge endpoints and reciprocity,
proof acyclicity/reachability, semantic-step ceilings, and honest open-root cut are self-tested.
Lean checks the exact conditional child-to-root interface. It does not construct
`CKNAnalyticPackage`, so the weighted inequality and exact root remain unproved. H0/R0, complete
provenance and trust closure, hermetic replay, independent validation, audit completion, master
acceptance, and theorem completion remain open.
