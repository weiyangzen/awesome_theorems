# Obligation-tree validation receipt

Node: `S56-M-1289-OBLIGATION_TREE`. Base revision:
`4d5664421bb1948968c9c993cd7de255dfcc33fc`. Date: 2026-07-12. The pre-existing
untracked `Formalizations/Lean/.lake` link was neither created nor modified by this phase.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1289/build_obligation_artifacts.py` | 0 | generated 20 obligations; denominator `a0edf48d3fe3642429924f7bbd9010cf1fe2d9cb9acad4568dcff79766bf0731` |
| `python3 Stage1_Instances/THM-M-1289/check_obligation_tree.py` | 0 | PASS: 20 obligations and 50 typed edges; root open M3; six analytic components M4 |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets with ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1289` | 0 | rank 460, planned, L0/rework-required, theorem incomplete |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); LP="$(cd Formalizations/Lean && lake env printenv LEAN_PATH):Stage1_Instances/THM-M-1289"; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1289 Stage1_Instances/THM-M-1289/Statement.lean -o Stage1_Instances/THM-M-1289/Statement.olean; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1289 Stage1_Instances/THM-M-1289/ObligationTree.lean; rm -f Stage1_Instances/THM-M-1289/Statement.olean Stage1_Instances/THM-M-1289/Statement.ilean` | 0 | pinned Lean 4.29.0 elaborated the exact statement and conditional composition; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`; temporary interface artifacts removed |
| forbidden-device `rg` scan of `ObligationTree.lean`, requiring no match | 0 | no `sorry`, `admit`, `axiom` declaration, or `sorryAx` |
| `python3 -m json.tool` on both generated JSON artifacts | 0 | both artifacts parse as JSON |
| `git diff --check -- Stage1_Instances/THM-M-1289 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

The Lean recipe uses the executable and dependency path emitted by the existing `lake env`. It
performs no Lake update, build, fetch, clone, or dependency mutation.

## Result boundary

The frozen denominator projection, eligibility lists, required node fields, typed graph names and
endpoints, proof-edge reciprocity, proof acyclicity and reachability, explicit root cut set, and open
closure verdict are self-tested. Lean checks only that six exact abstract component propositions
compose to the unchanged public target. No analytic premise is constructed. Human-source review,
proof closure, H0/R0, provenance and trust closure, hermetic replay, independent validation, master
acceptance, and theorem completion remain open.
