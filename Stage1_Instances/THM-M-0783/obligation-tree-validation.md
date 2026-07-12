# Obligation-tree validation

Validated on 2026-07-12 in the worker clone at base revision
`32404187d6cee70b44ae90adf8d0d765752e5149`. Existing canonical pinned `.lake` artifacts were used
read-only. No update, build, clone, fetch, or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0783/build_obligation_artifacts.py` | 0 | Reproduced denominator `0581a4ed...25532c9` |
| `cd Formalizations/Lean && lake env lean -R ../.. -o /tmp/thm-m-0783-lean/Statement.olean ../../Stage1_Instances/THM-M-0783/Statement.lean` | 0 | Re-elaborated exact statement into an isolated temporary olean |
| `cd Formalizations/Lean && LEAN_PATH=/tmp/thm-m-0783-lean lake env lean -R ../.. ../../Stage1_Instances/THM-M-0783/ObligationTree.lean` | 0 | Conditional composition elaborated; axiom report was `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0783/check_obligation_tree.py` | 0 | Twelve obligations, 28 reciprocal/typed edges, exact hashes, DAG reachability, ledgers, recipes, and open-root boundary passed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and projection passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets passed |
| `python3 scripts/stage1_target.py show THM-M-0783` | 0 | Rank 788, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0783 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The axiom report belongs only to the checked conditional transport and is not evidence for an
inhabitant of `DenseFamilySolver`. The root remains `M4`, with no proof or theorem-completion claim.
