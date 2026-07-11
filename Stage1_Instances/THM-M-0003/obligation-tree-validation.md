# Obligation-tree validation record

Item: `S56-M-0003-OBLIGATION_TREE`  
Base revision: `b7719b39b5595e187b4d2ecf832d3922a916d38b`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The frozen registry contains 19 unique semantic obligations and separates the
proof, refinement, provenance, evidence, trust, documentation, and workflow
graphs. Proof edges are reciprocal and acyclic, all root proof leaves are
reachable, every semantic budget is at most 100, and all denominators are bound
to a canonical SHA-256 digest plus the exact statement and anchor-audit files.

`ObligationTree.lean` kernel-checks composition of four explicit exactness
premises into the exact pointwise six-term target without invoking
`SnakeInput.snake_lemma`. Lean reports `propext`, `Classical.choice`, and
`Quot.sound` for this local conditional composition. No obligation is recorded closed: upstream `M1` candidates are
availability evidence, not node-specific accepted receipts. The root remains
`M1`, `audit_complete=false`, and `theorem_complete=false`.

## Commands and results

All commands ran in this worker clone. Lean used the existing pinned Lake
environment; no update, build, clone, fetch, or other `.lake` mutation command
was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0003/build_obligation_artifacts.py` | 0 | wrote 19 obligations and 52 typed edges; denominator `239fd7f9...3424` printed |
| `python3 Stage1_Instances/THM-M-0003/check_obligation_tree.py` | 0 | registry hashes/denominators, typed graphs, reciprocal proof edges, acyclicity, reachability, budgets, recipes, and open closure boundary passed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0003/ObligationTree.lean` | 0 | four segment types checked; conditional exact composition elaborated; axioms: `propext`, `Classical.choice`, `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0003/Statement.lean` | 0 | exact frozen target and statement transport re-elaborated |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered uniform-L0 targets valid |
| `python3 scripts/stage1_target.py show THM-M-0003` | 0 | rank 98, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0003 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The first later gate still open is proof-phase node-specific provenance, trust,
and kernel evidence for the frozen obligations. Master acceptance is separate.
