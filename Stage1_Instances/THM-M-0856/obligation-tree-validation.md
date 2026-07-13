# THM-M-0856 obligation-tree validation

Item: `S56-M-0856-OBLIGATION_TREE`.

Base revision: `f023dbc3411d83201065d1a1156d7406b81135d4`.

Base tree: `3b3a73ec19293a2a9b8d9c7e67f0d25da2a511b4`.

Validation date: 2026-07-14 (`Asia/Shanghai`).

## Result

Registry version 1 freezes 56 canonical obligations and the denominator SHA-256
`9d6a920afceb2d2c42ce432e12008329977aa733eecb42c28ed2c44686aca20c`. The 300
typed edges live in separate proof, refinement, provenance, evidence, trust, documentation, and
workflow graphs. Each obligation has a unique readable anchor and a substantive structured ledger
below the 100-step split threshold.

Every proof endpoint now carries either an exact declaration type or an elaborated planned Lean
signature with a deterministic fingerprint. The evidence-object registry and evidence graph are
empty: all current worker receipts explicitly remain mutable, unaccepted, and non-content-addressed.

The architecture follows the actual pinned `SimpleGraph.tutte` body. It expands necessity through
the injection from odd deleted components to deleted vertices; sufficiency through the odd/even
split; the even branch through an edge-maximal matching-free supergraph and deletion of universal
vertices; the clique branch through representative, component-local, and complement matchings; and
the nonclique branch through two edge augmentations, near-matchings, alternating cycles, and a
symmetric-difference toggle. The root terminal body is deduplicated from the local adapter and the
external Atlas wrapper.

`ObligationTree.lean` checks the literal pinned terminal proposition, its exact adapter to the
frozen deletion inequality, and a root harness that explicitly consumes both children. It reports
the terminal, wrapper, and adapter recursively sorry-free. The necessity theorem, even-order
existence theorem, terminal, adapter, wrapper, and root composition report only `propext`,
`Classical.choice`, and `Quot.sound`. The 16 internal source-body relations remain explicitly
unverified decomposition plans, not false composition certificates.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0856` | 0 | rank 1410, planned, L0/rework-required, theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0856/build_obligation_artifacts.py --check` | 0 | deterministic registry, graph, validation-spec, readable-tree, and signature-module bytes match |
| `python3 -B Stage1_Instances/THM-M-0856/check_obligation_tree.py --worker-packet .stage1-worker-selftest.json` | 0 | registry, graphs, task links, source hashes, all planned Lean signatures, root composition, receipt, packet, and open-root boundary passed |
| `python3 -m json.tool <path>` separately for `instance.json`, `task-dag.json`, `obligation-registry.json`, `typed-graphs.json`, `validation-specs.json`, `obligation-tree-receipt.json`, and `.stage1-worker-selftest.json` | 0 | each named executable argv parsed its artifact |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0856-obligation-pycache python3 -m py_compile Stage1_Instances/THM-M-0856/build_obligation_artifacts.py Stage1_Instances/THM-M-0856/check_obligation_tree.py Stage1_Instances/THM-M-0856/check_prohibited_constructs.py` | 0 | all three Python tools compiled outside the repository |
| `python3 -B Stage1_Instances/THM-M-0856/check_prohibited_constructs.py` | 0 | comment-aware scan of both owned Lean sources and pinned `Tutte.lean` passed; the main Lean harness also reports pinned `SimpleGraph.tutte` sorry-free |
| `env PYTHONOPTIMIZE=1 python3 -B Stage1_Instances/THM-M-0856/check_obligation_tree.py` | 1 expected | fail-closed guard rejected optimized Python before any assertion-based gate could be skipped |
| `git diff --check -- Stage1_Instances/THM-M-0856 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The existing canonical `.lake` symlink and pinned package checkout were reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout, or `.lake` mutation was performed.

## Status boundary

This is nonrelease worker evidence pending dependency-ordered master acceptance. The root remains
`[H1, M3, R4]`, `accepted_closed_obligations=[]`, `audit_complete=false`, and
`theorem_complete=false`. The exact pinned route remains below E1 until proof-phase adoption and
release-grade provenance/trust evidence are accepted. Primary-source H0, readable R0, internal
composition certificates, hermetic replay, independent validation, `AUDIT-Z`, release, and theorem
completion remain open.
