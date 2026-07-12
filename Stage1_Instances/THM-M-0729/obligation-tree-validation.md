# THM-M-0729 obligation-tree validation

Item: `S56-M-0729-OBLIGATION_TREE`  
Base revision: `3159849a5319960dea505779c7c20894ea30487c`  
Validation date: 2026-07-12 (`Asia/Shanghai`)

Existing pinned Lake artifacts were reused. No update, build, dependency clone,
or fetch command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0729/build_obligation_artifacts.py` | 0 | regenerated registry and graph bundle; denominator `66be2951...a2e854` |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | 19 obligations and 76 typed edges; hashes, eligibility projections, adjacency, reciprocal proof edges, acyclicity, node schema, budgets, recipes, and placeholder hygiene passed |
| Lake-derived `LEAN_BIN`/`LEAN_PATH`; compile `Statement.lean` to a temporary owned `Statement.olean`, then elaborate `ObligationTree.lean`, then remove the olean | 0 | exact directional-to-root composition elaborated; axiom report was `[propext, Classical.choice, Quot.sound]` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | rank 766, planned, theorem incomplete |
| `python3 -m json.tool` on all three generated JSON artifacts | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0729` | 0 | no whitespace errors |

A direct `lake env lean ../../Stage1_Instances/THM-M-0729/ObligationTree.lean`
attempt failed because the target module imports sibling `Statement`, which is
not a Lake package module. The successful narrow recipe obtains the pinned Lean
executable and `LEAN_PATH` from Lake, emits the temporary olean only inside the
owned directory, and deletes it. This failed attempt is recorded rather than
hidden.

The validation establishes the registry freeze and conditional composition
interface only. Both PCP inclusions, primary-source proof mapping, foundation
closure, proof bodies, and master acceptance remain open. Root status is `M3`;
theorem completion is false.
