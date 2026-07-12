# THM-M-1270 obligation-tree validation

Item: `S56-M-1270-OBLIGATION_TREE`  
Base revision: `a1b16ca3ed65db2ec65e3d478d1680d9c1f5489d`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 17 obligations and 41 directed typed edges across distinct proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Fourteen obligations
are root-relevant machine obligations and three are informational overlays. The frozen denominator
SHA-256 is `6f9c178b5c1e9de09200f57a3ac40b419e29abcc079899e208ae7c88e8a16156`.

The Lean harness checks the child-to-root composition: an explicit hard-core function producing
the witness package yields the exact root shape. It does not produce that function. All obligations
remain uncredited, the root remains `M3`, and the frozen hard-core cut set is `M1270-C-SEQUENCE`,
`M1270-C-INVARIANTS`, `M1270-L-CAUCHY`, `M1270-L-LIMIT`, `M1270-L-LOCALIZE`, and
`M1270-L-MAXIMAL`.

## Commands and exact results

Commands ran from the repository root unless a working directory is named. The pre-existing pinned
`.lake` closure was reused; no update, build, clone, fetch, or dependency mutation was performed.

| command | exit | result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1270` | 0 | rank 163, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1270/build_obligation_artifacts.py` | 0 | wrote 17 obligations and 41 typed edges; emitted the denominator digest above |
| `python3 Stage1_Instances/THM-M-1270/check_obligation_tree.py` | 0 | source hashes, denominator, node schema, seven graph classes, reciprocal proof edges, acyclicity, recipes, budgets, prohibited tokens, and open-root boundary passed |
| `python3 -m json.tool Stage1_Instances/THM-M-1270/obligation-registry.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1270/typed-graphs.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1270/validation-specs.json` | 0 | valid JSON |
| `lake env lean ../../Stage1_Instances/THM-M-1270/ObligationTree.lean` from `Formalizations/Lean` | 0 | composition elaborated; anchor probes passed; axioms were `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx` |
| `git diff --check -- Stage1_Instances/THM-M-1270 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The pre-existing untracked `Formalizations/Lean/.lake` link makes these nonrelease worker results.

## Status boundary

This receipt supports only the registry freeze, typed graphs, executable structural validation,
readable tree, and conditional composition harness, pending master acceptance. It closes no proof
obligation and does not claim primary-source review, readable reconstruction review, transitive
trust, independent replay, `AUDIT-Z`, `THEOREM-Z`, validation, release, or theorem completion.
