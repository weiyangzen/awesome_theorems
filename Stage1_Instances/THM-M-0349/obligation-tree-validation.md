# Obligation-tree validation record

Item: `S56-M-0349-OBLIGATION_TREE`  
Base revision: `7780ee2963f599a6bf06f39a12c6fddb7eafc914`

The registry freezes 15 semantic obligations and seven separate typed graphs. The proof graph is acyclic and reaches exactly 11 proof-relevant nodes. Its conditional Lean composition depends on the explicit existence and uniform-bound packages; it does not close either package or the root.

## Commands and results

All commands ran in this worker clone against the existing pinned Lake environment. No update, build, clone, fetch, or other `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0349/build_obligation_artifacts.py` | 0 | generated registry and graphs; denominator `559befd6...3185d` |
| `cd Formalizations/Lean && lake env lean -R ../../Stage1_Instances/THM-M-0349 ../../Stage1_Instances/THM-M-0349/Statement.lean -o ../../Stage1_Instances/THM-M-0349/Statement.olean && LEAN_PATH=../../Stage1_Instances/THM-M-0349 lake env lean -R ../../Stage1_Instances/THM-M-0349 ../../Stage1_Instances/THM-M-0349/ObligationTree.lean` | 0 | exact conditional composition elaborated; axioms were `propext`, `Classical.choice`, `Quot.sound`; temporary olean removed |
| `python3 Stage1_Instances/THM-M-0349/check_obligation_tree.py` | 0 | 15 obligations and all typed edges passed; root reported open M3 |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0349` | 0 | rank 842, planned, theorem incomplete |
| placeholder/axiom scan of target Lean files | 1, expected | no `sorry`, `admit`, declared `axiom`, or `sorryAx` found |
| `git diff --check -- Stage1_Instances/THM-M-0349 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This phase freezes architecture only. Human-source mapping is still H3, the exact root remains M3, readability remains R4, and theorem completion is false.
