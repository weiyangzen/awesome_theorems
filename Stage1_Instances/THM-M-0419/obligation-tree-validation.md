# THM-M-0419 obligation-tree validation

Item: `S56-M-0419-OBLIGATION_TREE`

Base revision: `80f0191c83a1bb4026c2d490be957cf109464de1`

Validation date: `2026-07-15` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 25 canonical obligations, 195 substantive ledger
steps, and 65 directed typed edges across separate proof, refinement,
provenance, evidence, trust, documentation, and workflow graphs. The denominator
SHA-256 is
`84b22238b8c01210c72a112261776db3e96002fde700709d0336a2d07d799f71`.

The proof graph checks only conditional interfaces. Three branch packages yield
the cyclic prime-power package; the cyclic package and an open induction engine
yield local containment; positive transport, local containment, and an open
globalization package yield the exact root through an explicit assembly
interface. None of those declarations proves a substantive premise.

The immutable Atlas candidate is retained as a zero-credit provenance boundary.
Its source hash and revision match `anchor-audit.json`, and the audited source has
22 proof gaps, including conductor and inertia/embedding bridges. No external
candidate, wrapper, source map, or support edge closes an obligation.

No obligation is accepted closed. The root remains `H1/M3/R3`,
`audit_complete=false`, and `theorem_complete=false`.

## Commands and results

Commands ran in this worker clone. The automation-provided `.lake` symlink was
reused read-only; no update, build, clone, fetch, checkout, or other dependency
mutation command ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, the execution skill, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0419` | 0 | rank 74; planned; L0/rework-required; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0419/build_obligation_artifacts.py` | 0 | generated 25 obligations, 65 typed edges, and denominator `84b22238...99f71` |
| `python3 -B Stage1_Instances/THM-M-0419/check_obligation_tree.py` | 0 | deterministic generation, frozen input hashes, denominator, 195 ledgers, seven graphs, reciprocal proof edges, workflow, recipes, pinned Lean replay, and open H1/M3/R3 boundary passed |
| compile `Statement.lean` to a temporary `Statement.olean` with pinned `lake env which lean`, then elaborate `ObligationTree.lean` with that directory prepended to `lake env LEAN_PATH` | 0 | exact root and five transport/conditional declarations elaborated; only `propext`, `Classical.choice`, and `Quot.sound` reported; combined output SHA-256 `152b9cfc...94175` |
| `python3 -m json.tool` on registry, graphs, specs, receipt, and root packet | 0 | all structured artifacts parsed successfully |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0419-obligation-pycache python3 -m py_compile Stage1_Instances/THM-M-0419/build_obligation_artifacts.py Stage1_Instances/THM-M-0419/check_obligation_tree.py` | 0 | both Python modules compiled outside the repository tree |
| comment-aware prohibited-construct validation over `ObligationTree.lean` | 0 | no proof gap, axiom declaration, unsafe/opaque body, external/native/oracle implementation, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0419 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

Generated machine artifacts:

```text
860e52d35f41f870858a3d2d1b230b7a2418bcf17c374efa618d62f93bd1dd7b  obligation-registry.json
a4385d65ac70f1d772b4e8d1d3f06607a5ba893534c555d70488d1c7f78f85ae  typed-graphs.json
8baa49ab69d0fdc1e1038aa7e9289c905e6cd1326246ff387c57ecc651a8e574  validation-specs.json
```

## Status boundary

This is provisional worker evidence pending dependency-ordered master
acceptance. The local induction engine, tame/odd-wild/2-adic-wild branches,
completion and conductor construction, inertia/Minkowski embedding, exact
cyclotomic identification, pinpoint `H0`, independently reviewed `R0`, full
provenance/trust, hermetic replay, independent verification, deterministic
release evidence, `AUDIT-Z`, and `THEOREM-Z` remain open.
