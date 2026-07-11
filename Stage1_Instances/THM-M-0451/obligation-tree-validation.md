# Obligation-tree validation

Item: `S56-M-0451-OBLIGATION_TREE`  
Base revision: `0bc6e1901fa105d8a56626039132f99d3441ef3b`

The registry and seven graph families freeze 17 obligations. The Lean module
checks a binder- and normalization-preserving conditional composition from an
explicit, uninhabited engine into the exact target. It proves none of the open
mathematical fields. Root closure, audit completion, and theorem completion all
remain false.

## Commands and exact results

All commands ran in this worker clone. Lean reused the existing pinned `.lake`
artifacts; no update, fetch, clone, dependency build, or `.lake` mutation was
performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard passed: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0451` | 0 | rank 93, planned, rework-required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean -R ../.. -o /tmp/thm-m-0451-olean/Statement.olean ../../Stage1_Instances/THM-M-0451/Statement.lean` | 0 | exact statement elaborated to a temporary module artifact outside `.lake` |
| `cd Formalizations/Lean && LEAN_PATH=/tmp/thm-m-0451-olean lake env lean -R ../.. ../../Stage1_Instances/THM-M-0451/ObligationTree.lean` | 0 | engine and exact conditional composition elaborated; `#print axioms` reported only pinned foundational `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0451/check_obligation_tree.py` | 0 | 17 obligations and 44 typed edges passed; root open |
| `python3 -m json.tool Stage1_Instances/THM-M-0451/obligation-registry.json >/dev/null` | 0 | registry parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0451/typed-graphs.json >/dev/null` | 0 | graph bundle parsed |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)' Stage1_Instances/THM-M-0451 -g '*.lean'` | 1 | expected no-match result; no prohibited Lean declaration |
| `git diff --check -- Stage1_Instances/THM-M-0451 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The minimal mathematical cut remains the approximate-height estimate together
with the construction/property leaves. Source, provenance, trust, replay,
readability, and independent acceptance are also open release gates.
