# THM-M-0927 obligation-tree validation

Item: `S56-M-0927-OBLIGATION_TREE`

Base revision: `ff3db6d51326417873f49c410421f8f3e13be993`

Base tree: `9160a80a3e3588fd96fcd79323230668cc7d3df1`

Validation date: `2026-07-15` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 26 semantic obligations and 47 directed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. Its denominator
SHA-256 is `96eb539e67048140003ad8ed68e84ef0fd1daa215803f7915908af2999c373de`.

The architecture expands the pinned recurrence proof through the recurrence definition and
characteristic polynomial, Fibonacci and two geometric solution witnesses, the scaled-difference
construction, exhaustive zero/one initial cases, recurrence uniqueness, the function and
pointwise Binet declarations, and the final source-radical transport. `Real.coe_fib_eq` is
deduplicated as a wrapper over the unique terminal body `Real.coe_fib_eq'`.

The proof graph contains only the exact abstract-child root harness. Eight internal relations
remain explicit `logical_decomposition` plans pending proof-phase exact child interfaces and
consuming composition certificates. No obligation is accepted closed. The root remains
`H1/M3/R4`, `audit_complete=false`, and `theorem_complete=false`.

## Commands and exact results

The worker clone's pre-existing `Formalizations/Lean/.lake` symlink was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout, or `.lake` mutation was performed.

| Command | Exit | Exact result and boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0927` | 0 | rank 1546, planned, L0/rework-required, theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0927/build_obligation_artifacts.py --write` | 0 | deterministically wrote 26 obligations and 47 typed edges; denominator `96eb539e...373de` |
| `python3 -B Stage1_Instances/THM-M-0927/build_obligation_artifacts.py --check` | 0 | generated registry, graph, validation, and readable artifacts exactly match deterministic regeneration |
| `python3 -B Stage1_Instances/THM-M-0927/check_obligation_tree.py` | 0 | statement/anchor hashes, manifest/DAG identity, 26 records and ledgers, mandatory layers, seven graphs, reciprocal proof edges, decomposition plans, recipes, pinned source blobs, Lean harness, and open closure passed |
| checker-managed temporary `Statement.olean` compilation and pinned Lean elaboration of `ObligationTree.lean` | 0 | exact transports and abstract-child root composition elaborated; six declarations reported `[propext, Classical.choice, Quot.sound]` and sorry-free; stdout SHA-256 `0c8860a4...1a242` |
| `python3 -m json.tool` on every structured obligation artifact and the worker packet | 0 | every JSON artifact parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0927-obligation-pycache python3 -m py_compile ...` | 0 | builder and checker compiled without cache output in the owned path |
| comment-aware prohibited-construct scan of `ObligationTree.lean` | expected no match | no `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/opaque body, oracle, external implementation, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0927 .stage1-worker-selftest.json` plus no-index checks | 0 | no whitespace diagnostics |

## Evidence boundary

`functionToPointwiseTransport_checked`, `namedRootToRadicalTransport_checked`, and
`root_of_terminal_packages` check the exact composition boundary. The substantive
`FunctionNamedRootPackage` remains an explicit premise. The module inspects the pinned
`Real.coe_fib_eq'` and `Real.coe_fib_eq` declarations and their axiom/sorry reports, but does not
install either as an accepted proof-phase child.

The integrated intake, statement, and anchor-audit nodes remain provisional `[_]` inputs. This
phase binds their current statement and anchor hashes and directly re-elaborates `Statement.lean`;
it does not falsely claim dependency-ordered master acceptance or replay an older phase's
worker-packet contract after later dossier files were added.

## Status boundary

The minimal open machine-proof cut is `M0927-T-FUNCTION-BINET`, which has an exact pinned candidate
but no proof-phase adoption or master acceptance. Primary-source H0 and independent review,
readable R0 and independent review, full provenance/evidence/TCB closure, hermetic replay,
independent verification, deterministic release, master acceptance, `AUDIT-Z`, and `THEOREM-Z`
remain open. This receipt proposes only `[_]`; it does not claim theorem completion.
