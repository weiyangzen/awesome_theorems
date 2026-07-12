# Statement validation record

Item: `S56-M-1119-STATEMENT`  
Base revision: `c0764cd5ac368a420421893aa0f4c34cd8009ebf`

## Frozen target

`Stage1Instances.THM_M_1119.KestenTarget` states that the critical probability of independent bond
percolation on the nearest-neighbor square lattice `Z x Z` is `1/2`. Bonds are the unoriented edges
of an explicit `SimpleGraph`; configurations are Boolean functions on those bonds; their law is an
infinite product of Bernoulli measures. The order parameter is the measure of configurations in
which the origin can reach a vertex outside every finite vertex set through open bonds. The critical
probability is the `NNReal` infimum of parameters in `[0,1]` where this measure is positive.

The selected human claim is the equality in Kesten's paper title, *The critical probability of bond
percolation on the square lattice equals 1/2*, CMP 74(1) (1980), 41-59, DOI
`10.1007/BF01197577`. This statement phase does not claim pinpoint definition review, errata review,
or `H0`; those remain source-audit work. It also does not add the stronger critical-endpoint claim.

## Commands and results

All commands ran inside this worker clone. Lean ran from `Formalizations/Lean` with the existing
pinned Lake environment; no dependency update, fetch, build, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1119/Statement.lean` | 0 | square lattice, bond product measure, infinite-cluster predicate, threshold, exact target, expanded-target iff, and four mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-1119/check_statement.py` | 0 | expression SHA-256 `c457bb8081bc2dc5dfdaca2c724ea34eab89491a80e87e78ab2a31fa16c5cf6e`; all four mutations distinguished; mathlib revision `8a178386...95` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1119/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `f020e5...b86`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1119` | 0 | rank 559, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool` on `statement.json`, `instance.json`, and `task-dag.json` | 0 | all JSON parsed |
| `rg -n '\b(sorry\|axiom\|admit)\b' Statement.lean check_statement.py` | 1 | no prohibited token found; `rg` exit 1 means no match |
| `git diff --check -- Stage1_Instances/THM-M-1119 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Mutation and status boundary

The validator separately elaborates and compares mutations that use site rather than bond
configurations, remove the infinite-cluster event, change binder scope by requiring positive
probability at `p = 1/2`, and add absence of an infinite cluster at the endpoint. None serializes to
the canonical expression. `kestenTarget_iff_expandedTarget` kernel-checks direct expansion of the
factored definitions.

This is statement-only evidence pending master acceptance. It contains no Kesten proof and claims
no anchor audit, obligation tree, machine closure, audit completion, or theorem completion.
