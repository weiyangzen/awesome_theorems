# THM-M-0420 Obligation-Tree Validation

Item: `S56-M-0420-OBLIGATION_TREE`  
Base revision: `ccc0b68fd3d7429e00f96b36fe6fa9deb8a7dea1`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The registry freezes 16 unique semantic obligations with denominator SHA-256
`48ca1cdd4926354cbf6593e34e77d6394a81f2405ea1067be9111d3c60632383`. The structural validator
checked its statement and anchor-audit bindings, complete node schema, eligibility denominators,
seven separate typed graphs, reciprocal proof/composition edges, indexes, proof-graph acyclicity and
root reachability, structured recipes, and the open-root boundary. The bundle contains 54 typed
edges.

The Lean harness checks `root_composition`: one coherent candidate plus exact abelian-Galois,
finite-prime-unramifiedness, reciprocity, and maximality hypotheses compose to the exact canonical
target. It asserts none of those five premises. Only the two prior statement transports and this
conditional composition are `M0-L`; every substantive input remains `M4`, and the root remains
`M3`.

## Commands And Exact Outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets/ranks; all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0420` | 0 | rank 75, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0420/build_obligation_artifacts.py` | 0 | deterministically generated registry, typed graphs, and validation specs |
| `python3 Stage1_Instances/THM-M-0420/check_obligation_tree.py` | 0 | `PASS THM-M-0420 obligation tree: 16 obligations, 54 typed edges`; root open M3 |
| `cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0420/check_composition.sh` | 0 | exact statement elaborated; `root_composition ... : HilbertClassFieldTarget K` printed |
| `python3 -m json.tool` on all three generated JSON files | 0 | all parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0420 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

Generated artifact hashes:

```text
ce872985846b4565ef1973d2021c36cbb66a6fe01338633e2799d5eab71970a9  obligation-registry.json
1ccae2101ed73c52d6d1dc7fdda738abac232df189d793e9b5b72eec0de81aed  typed-graphs.json
2c5936c8ef9ed9fec1077ef7731cf769073b5251f7d14868ea2b8ab737e57841  validation-specs.json
```

An initial command invoked the artifact builder from `Formalizations/Lean` with a root-relative
path and exited 2 because that path did not exist from that working directory. The command was not
a validation recipe and changed nothing. It was corrected by running the builder and structural
validator from the repository root, then the recorded Lean recipe from `Formalizations/Lean`.

The pre-existing untracked `Formalizations/Lean/.lake` link reuses canonical pinned artifacts. The
composition script creates a temporary `Statement.olean` under the owned target path and removes it
on exit. No update, build, clone, fetch, network access, or dependency mutation occurred.

## Status Boundary

This self-tests only the frozen obligation registry and typed architecture. Planned signatures are
not declarations. Human-source pinpoint review, the construction, all four substantive properties,
an unconditional terminal proof, trust/provenance closure, readable review, hermetic replay,
independent verification, theorem completion, and master acceptance remain open. Accepted receipt
IDs are empty.
