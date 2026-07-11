# THM-M-0394 Obligation-Tree Validation

Item: `S56-M-0394-OBLIGATION_TREE`  
Base revision: `63ffe6d6785bf79248c8559737f408834081b07e`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The registry freezes 17 unique semantic obligations with denominator SHA-256
`5d036d97b1e182b399dd6f5b770b17a6d5506fdf54d8aa409513e3b354fc472a`.
The structural validator checked the statement and anchor-audit bindings, required
node fields, eligibility denominators, seven separate typed graphs, reciprocal
proof/composition edges, indexes, acyclicity and root reachability, validation
recipe references, and the open-root boundary. The graph bundle contains 47 edges.

The Lean harness checks `branch_composition`: abstract proofs of the exact
positive-genus and genus-zero branches compose to the exact canonical statement.
It asserts neither premise. Only the two definition transports and this conditional
composition are classified `M0-L`; every substantive Siegel branch remains `M4`,
and the root remains `M3`.

## Commands And Exact Outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets/ranks; all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0394` | 0 | rank 7, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0394/build_obligation_artifacts.py` | 0 | deterministically generated registry, typed graphs, and validation specs |
| `python3 Stage1_Instances/THM-M-0394/check_obligation_tree.py` | 0 | `PASS THM-M-0394 obligation tree: 17 obligations, 47 typed edges`; root open M3 |
| `cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0394/check_composition.sh` | 0 | statement elaborated and `branch_composition (positive) (genusZero) : Statement` printed |
| `python3 -m json.tool` on all three generated JSON files | 0 | all parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0394 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Generated artifact hashes:

```text
62e1d333dc8d1537643609c6820d3f3c3d478b2d302c609f4bdb7f33b53f0378  obligation-registry.json
e2ec6dc22e909aee78b509f11ce5389ef1082f32bb97dac630085d464221a9d5  typed-graphs.json
06ae548affaa92a596d0abae5cbf132edb1c56eeea01ab3897bc75cfeea3afff  validation-specs.json
```

The pre-existing untracked `Formalizations/Lean/.lake` link reuses canonical
pinned artifacts. The composition script creates a temporary `Statement.olean`
inside the owned target directory and removes it on exit. No update, build,
clone, fetch, network access, or dependency mutation was performed.

## Status Boundary

This evidence self-tests only the frozen obligation registry and typed
architecture. Planned signatures are not declarations. Human-source pinpointing,
both substantive branches, terminal root proof, trust/provenance closure, readable
review, hermetic replay, independent verification, theorem completion, and master
acceptance remain open. Accepted receipt IDs are empty.
