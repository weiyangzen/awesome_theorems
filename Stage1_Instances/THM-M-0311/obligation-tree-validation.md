# THM-M-0311 obligation-tree validation

Item: `S56-M-0311-OBLIGATION_TREE`  
Base revision: `8014740e5a37eff82745f6fd2bc69f0ee45e67c9`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The deterministic builder froze 17 semantic obligations and 33 typed edges in seven graphs. The
validator recomputed denominator digest
`50da280705bd60f82bd5542af670b42225813e40e3c016d0d24cd977f7890c53`, required the complete node
schema, checked reciprocal proof/composition indexes, rejected duplicate edges, checked proof-graph
acyclicity and root reachability, enforced leaf budgets, and retained the shared mathlib body as one
canonical obligation for both scalar branches.

The pinned Lean executable elaborated `ObligationTree.lean`. The checked composition theorem has
axioms `[propext, Classical.choice, Quot.sound]`; its real and complex completeness inputs remain
explicit premises. No dependency fetch, update, build, or `.lake` mutation was performed.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0311` | 0 | rank 813, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0311/check_statement.py` | 0 | exact expression, four mutations, toolchain, and mathlib pin passed |
| `python3 Stage1_Instances/THM-M-0311/check_anchor_audit.py` | 0 | immutable pin, source body, hygiene, exact wrapper, and fail-closed status passed |
| `python3 Stage1_Instances/THM-M-0311/build_obligation_artifacts.py` | 0 | deterministically wrote 17 obligations and 33 typed edges |
| `python3 Stage1_Instances/THM-M-0311/check_obligation_tree.py` | 0 | registry/node/graph/reachability/budget/hygiene gates passed; root remained M3 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0311/ObligationTree.lean)` | 0 | typed branches and conditional composition elaborated; exact upstream declarations resolved |
| `python3 -m json.tool` on both structured artifacts | 0 | both files are valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0311 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Content hashes after deterministic regeneration:

```text
48ca2b525149cebe6067eb371ec0f04dcef8bc5b86ba62acc04103e3708d2be0  obligation-registry.json
3d03d5d21d167a7d4007f0fee6c276ef5dcce482924cb5f7d18c7bf0c208d8a6  typed-graphs.json
```

## Status boundary

This self-test covers only the architecture freeze. The root remains `[H1, M3, R4]`; pinned scalar
bodies are candidates, not accepted proof state. Full proof admission, transitive trust and
provenance, pinpoint human-source review, readable reconstruction, hermetic validation, independent
review, audit completion, and theorem completion remain open. Master acceptance is required.
