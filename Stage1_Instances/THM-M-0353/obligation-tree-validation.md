# Obligation-tree validation record

Item: `S56-M-0353-OBLIGATION_TREE`  
Base revision: `ded29702119d0d4880db9fcf1d0a6560a89058fd`

The registry freezes 16 semantic obligations and seven separate typed graphs. The proof graph is
acyclic and reaches exactly 13 proof-relevant nodes. Its conditional Lean composition depends on
the explicit `MemLp` and `HilbertBasis` packages; it closes neither package nor the theorem root.

## Commands and results

All commands ran in this worker clone against the existing pinned Lake environment. No update,
build, clone, fetch, or other `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0353/build_obligation_artifacts.py` | 0 | generated registry and typed graphs; denominator `4516c92f...d0f0` |
| `cd Formalizations/Lean && lake env lean -R ../../Stage1_Instances/THM-M-0353 ../../Stage1_Instances/THM-M-0353/Statement.lean -o ../../Stage1_Instances/THM-M-0353/Statement.olean && LEAN_PATH=../../Stage1_Instances/THM-M-0353 lake env lean -R ../../Stage1_Instances/THM-M-0353 ../../Stage1_Instances/THM-M-0353/ObligationTree.lean` | 0 | exact conditional composition elaborated; axioms were `propext`, `Classical.choice`, and `Quot.sound`; temporary olean removed |
| `python3 Stage1_Instances/THM-M-0353/check_obligation_tree.py` | 0 | 16 obligations and 76 typed edges passed; root reported open M3 |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0353` | 0 | rank 846, planned, theorem incomplete |
| placeholder/declared-axiom scan over target Lean files | 1, expected | no `sorry`, `admit`, declared `axiom`, or `sorryAx` found |
| `python3 -m json.tool` on both generated JSON artifacts | 0 | both structured artifacts parsed |
| `git diff --check -- Stage1_Instances/THM-M-0353 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This phase freezes architecture only. Human-source status remains H1, the exact root remains M3,
readability remains R4, and theorem completion is false.
