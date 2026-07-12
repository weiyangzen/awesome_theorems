# THM-M-1058 obligation-tree validation

Item: `S56-M-1058-OBLIGATION_TREE`  
Base revision: `a73eeda2e13e2eac063df01faf369a96820fa249`  
Validation date: 2026-07-12 (`Asia/Shanghai`)

## Result

The generator deterministically produced a 16-node registry and seven typed
graphs. The validator recomputed the frozen denominator digest, checked unique
registry and graph identities, reciprocal edge indexes, all mandatory node
fields and debt domains, leaf step budgets, proof/refinement acyclicity, and
root reachability of all 12 mathematical obligations. It found 26 typed edges.
All closure fields remain explicitly open.

The exact statement re-elaborated under the pinned toolchain. The pre-existing
untracked `Formalizations/Lean/.lake` link/artifact was reused without update,
build, clone, fetch, or dependency mutation.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1058` | 0 | rank 250, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1058/build_obligation_artifacts.py` | 0 | registry and graph bundle regenerated deterministically |
| `python3 Stage1_Instances/THM-M-1058/check_obligation_tree.py` | 0 | `PASS THM-M-1058 obligation tree: 16 obligations, 26 typed edges`; denominator `603b6a62...73f2`; root open M3 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1058/Statement.lean)` | 0 | frozen target and direct-expansion transport elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-1058/obligation-registry.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1058/typed-graphs.json >/dev/null` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1058 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Validated artifact hashes:

```text
4e9784a73d5370fd9ea35e3fb251436ecd12c71b833a54dd9c0fb9afe1e7fc38  obligation-registry.json
a60333cb73165c2f2a2b587147c882f8d5a2b2f9f37c11c3c039628f77a28060  typed-graphs.json
```

## Status boundary

This is node-scoped architecture evidence only. It does not prove either LDP
bound for any data, and it claims no audit or theorem completion. Integration
and master acceptance remain pending.
