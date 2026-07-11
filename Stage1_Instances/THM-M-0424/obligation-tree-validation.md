# THM-M-0424 obligation-tree validation

Base revision: `23c9585c21005a4bdad02f551436a857923c438e`.

The frozen registry contains 18 unique obligations and the seven separately
typed graphs contain 35 reciprocal or support edges. The root remains open at
M3. The conditional Lean composition certificate elaborates but has an
uninhabited premise and is explicitly excluded from terminal-body credit.

## Commands and results

| Command | Exit/result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0; 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0; rank 78, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0424/build_obligation_artifacts.py` | 0; deterministically rebuilt 18 obligations, denominator `83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00` |
| `python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py` | 0; registry hashes, node schemas, typed reciprocity, proof reachability, recipes, and open-root boundary passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0424/obligation-registry.json` | 0; parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0424/typed-graphs.json` | 0; parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0424/validation-specs.json` | 0; parsed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0424/ObligationTree.lean` | 0; exact conditional composition and all LawData projections elaborated; reported axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0424/Statement.lean` | 0; frozen target still elaborated |
| `git diff --check -- Stage1_Instances/THM-M-0424 .stage1-worker-selftest.json` | 0; no whitespace errors |

No `lake update`, build, clone, fetch, or `.lake` mutation was performed. The
pre-existing untracked `.lake` link/artifact is outside the owned path and was
used read-only as instructed.
