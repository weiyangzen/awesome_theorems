# THM-M-1277 obligation-tree validation

Item: `S56-M-1277-OBLIGATION_TREE`  
Base revision: `d16846c4969f0161ce4deb072fd4ba49becebb56`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The frozen registry contains 24 unique obligations and the seven required
typed graphs contain 48 unique edges. The validator recomputed denominator
digest `e17739e989327c1dcc2a43ec26c2d83e43a62bdf8448246f530a84f65af60575`,
checked eligibility projections, full node schemas, reciprocal proof edges,
edge indexes, graph acyclicity, and root reachability for every required
machine obligation. JSON parsing and whitespace checks passed.

The exact statement and the conditional branch composition both elaborated
with the pinned Lean executable. `#print axioms statement_of_branches` reported
only `propext`, `Classical.choice`, and `Quot.sound`; it reported no `sorryAx`.
The existing canonical `.lake` artifact was reused without update, build,
clone, fetch, or other dependency mutation.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-1277` | 0 | rank 328, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1277/build_obligation_artifacts.py` | 0 | wrote 24 obligations and 48 typed edges; printed the frozen digest above |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | `PASS THM-M-1277 obligation tree: 24 obligations, 48 typed edges`; root open M3 |
| `python3 -m json.tool Stage1_Instances/THM-M-1277/obligation-registry.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1277/typed-graphs.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1277/validation-specs.json` | 0 | valid JSON |
| `(cd Formalizations/Lean && lake env lean --root=../.. ../../Stage1_Instances/THM-M-1277/Statement.lean)` | 0 | exact statement elaborated; printed `Stage1Rev56.THMM1277.Statement : Prop` |
| `(cd Formalizations/Lean && lake env lean --root=../.. ../../Stage1_Instances/THM-M-1277/ObligationTree.lean)` | 0 | conditional composition elaborated; axioms were `propext`, `Classical.choice`, `Quot.sound` |
| `git diff --check -- Stage1_Instances/THM-M-1277` | 0 | no whitespace errors |

Validated content hashes:

```text
aa8ec448e49d03b87ea9afe610a3285318b2c377e68c0dd77ab854a4813abeec  obligation-registry.json
fdcc8a995fc5cbc5b20d14d8fa3d4b6bb657d3d57ca40c0ddc6271cbc00e53f0  typed-graphs.json
6491fb5a1bd8c99752c35f731a02581e7f788146bf0b59f6b4c75da0757652f7  ObligationTree.lean
```

## Status boundary

This self-test covers only the architecture freeze and exact conditional
composition. Neither the endpoint nor sharpness branch has a proof body; both
remain the root cut set. No source acceptance, audit completion, proof-phase
acceptance, release evidence, or theorem completion is claimed. Integration-
lane master acceptance remains required for the assigned scheduler item.
