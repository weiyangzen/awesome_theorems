# Obligation-tree validation receipt

Item: `S56-M-1146-OBLIGATION_TREE`. Base revision:
`1bea763d2294c2f3b725fe6eef9c769e0736c1eb`. Date: 2026-07-12. The pre-existing
`Formalizations/Lean/.lake` symlink is untracked in this worker clone and was neither created nor
modified by this phase.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1146/build_obligation_artifacts.py` | 0 | generated 18 obligations; denominator `59b6b2bd91ba7322a290e336203b2793f6c9a21cf216407b03cda9b8ae4207fe` |
| `python3 Stage1_Instances/THM-M-1146/check_obligation_tree.py` | 0 | PASS: 18 obligations and 40 typed edges; root open M3; reflected harmonic package M4 |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); LP="$(cd Formalizations/Lean && lake env printenv LEAN_PATH):Stage1_Instances/THM-M-1146"; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1146 Stage1_Instances/THM-M-1146/Statement.lean -o Stage1_Instances/THM-M-1146/Statement.olean; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1146 Stage1_Instances/THM-M-1146/ObligationTree.lean; rm -f Stage1_Instances/THM-M-1146/Statement.{o,i}lean` | 0 | pinned Lean 4.29.0 elaborated the exact statement and conditional composition; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`; temporary local interface artifacts were removed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets at ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1146` | 0 | rank 351; planned; L0/rework-required; theorem incomplete |
| `python3 -m json.tool` on both generated JSON artifacts | 0 | registry and typed graph bundle are valid JSON |
| scoped Lean scan for `sorry`, `admit`, `axiom`, and `sorryAx` | 1 | clean no-match result, converted to a successful shell assertion |
| `git diff --check -- Stage1_Instances/THM-M-1146 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

The Lean recipe uses only the executable and `LEAN_PATH` emitted by `lake env`; it performs no Lake
update/build, dependency fetch, or `.lake` mutation.

## Result boundary

The denominator projection, mandatory node fields, step budgets, typed graph separation, reciprocal
proof edges, endpoint indexes, proof acyclicity, required-node reachability, readable anchors, and
open closure boundary are self-tested. Lean checks only the exact conditional child-to-root
composition. It does not construct `ReflectedHarmonicPackage`; conjugation-precomposition and
harmonic gluing across the real axis remain open. Audit completion, H0/R0, trust closure, hermetic
replay, independent verification, proof/release phases, master acceptance, and theorem completion
are not claimed.
