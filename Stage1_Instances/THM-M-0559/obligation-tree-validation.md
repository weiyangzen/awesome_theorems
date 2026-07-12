# Obligation-tree validation

Item: `S56-M-0559-OBLIGATION_TREE`

Validation ran in the worker clone at base revision
`b2c56f8eef5ebd746710a17dcbf9055a53957262`. The pre-existing
`Formalizations/Lean/.lake` symlink was used without update, build, fetch, or mutation.

| Command | Exact result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0559` | exit 0; rank 607, planned, L0/rework_required, theorem_complete false |
| `python3 Stage1_Instances/THM-M-0559/build_obligation_artifacts.py` | exit 0; built 18 obligations and 88 typed edges; denominator `040c9f0d06a8432b0cf5768d43391f143d820754686514252ce484f53d3446fc` |
| `python3 Stage1_Instances/THM-M-0559/check_obligation_tree.py` | exit 0; fingerprints, denominators, required fields, reciprocal proof edges, graph indexes, reachability, acyclicity, and open-root boundary passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0559/obligation-registry.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0559/typed-graphs.json` | exit 0; valid JSON |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0559/ObligationTree.lean)` | exit 0; conditional exact-root composition elaborated; axioms `[propext, Classical.choice, Quot.sound]` |
| scoped declaration-token scan over `Stage1_Instances/THM-M-0559/*.lean` | exit 0; no `sorry`, `admit`, assumed declaration, `sorryAx`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0559 .stage1-worker-selftest.json` | exit 0; no whitespace errors |

The Lean harness independently repeats the frozen definitions because the dossier is outside the
Lake source tree; the statement and registry hashes bind the architecture to `Statement.lean`.
`root_of_directWhiteheadCore` checks only child-to-parent composition. Its premise remains open, so
this receipt grants no proof-phase, audit-completion, or theorem-completion credit.
