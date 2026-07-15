# Obligation-tree validation record

Item: `S56-M-0110-OBLIGATION_TREE`  
Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

## Frozen result

Registry v1 contains 23 canonical obligations with denominator
`153eb5eb51ad4419b8eed1a637a24ff66c7690442339b4fefebb327dc20c2cba`.
The seven typed graph families contain 56 edges. Only two conditional
composition declarations are kernel-checked; their combined statement and
obligation output SHA-256 is
`19639f76068cb7b9327620974bcb2ae8806ced0cc3671266dc09da80eaf954f4`.

The dependency ledger reproduces an empty hard-parent/ancestor/hint closure
and rejects the sole weak shared-module co-mention as non-reusable. It is bound
to theorem-DAG digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`
and context digest
`4f60e4c0e01ec4cc069fbe1a7601aabdc8f2acf1df3e4c917e09e4235cec640b`.

## Commands and results

| Working directory | Command | Exit | Result |
|---|---|---:|---|
| repository root | `python3 Docs/tools/check_stage1_standard.py` | 1 | Expected worker-scope freshness failure: the immutable checked-in v2 DAG does not yet inventory the new target artifacts; the worker is forbidden to regenerate it |
| repository root | `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ordered manifest passed |
| repository root | `python3 scripts/stage1_target.py show THM-M-0110` | 0 | Rank 34, planned, L0/rework-required, theorem incomplete |
| repository root | `python3 -B Stage1_Instances/THM-M-0110/build_obligation_artifacts.py` | 0 | Deterministically generated 23 obligations, 56 edges, and the denominator above |
| repository root | `python3 -B Stage1_Instances/THM-M-0110/check_obligation_tree.py` | 0 | Frozen inputs, registry, ledgers, graphs, recipes, dependency context, and pinned Lean replay passed |
| temporary directory plus target directory | pinned Lean executable from `lake env which lean`; compile `Statement.lean` to a temporary `Statement.olean`, prepend that directory to pinned `LEAN_PATH`, then elaborate `ObligationTree.lean` | 0 | Exact target and two conditional composition declarations elaborated; only standard axioms reported |
| repository root | `python3 -m json.tool` over all new JSON artifacts and the worker packet | 0 | Every structured artifact parsed |
| repository root | `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0110-obligation-pycache python3 -m py_compile ...` | 0 | Builder and checker compiled outside the repository |
| repository root | comment-aware prohibited-construct scan of `ObligationTree.lean` | 0 | No proof gap, axiom declaration, unsafe/opaque body, oracle, native evaluator, or external implementation |
| repository root | `git diff --check -- Stage1_Instances/THM-M-0110 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics |

The checker uses the existing canonical pinned `.lake` symlink read-only. It
runs no update, build, clone, fetch, checkout, or dependency mutation. The
symlink is pre-existing untracked automation state, so this is warm nonrelease
worker evidence.

The global standard validator's one failure is not a theorem-node failure.
Its nested v2 check compares the immutable checked-in discovery inventory to a
fresh inventory that sees this worker's new target files. Updating that global
projection is reserved for integration. The authoritative DAG bytes remain
unchanged and retain the required SHA-256; manifest membership and target
inspection pass independently.

## Status boundary

The architecture and conditional composition self-test, but no native
semantic witness or substantive Kodaira proof exists. The root remains
`H1/M3/R3`, the accepted closed-obligation set is empty, and source,
provenance, trust, readable review, hermetic validation, independent replay,
release, `AUDIT-Z`, and `THEOREM-Z` remain open.
