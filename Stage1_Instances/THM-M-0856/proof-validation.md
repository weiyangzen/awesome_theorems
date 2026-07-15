# THM-M-0856 proof-phase validation

Item: `S56-M-0856-PROOF`. Base revision:
`29a69c34f06bf3444399287853ea7806767d0944`.

## Implemented proof

`Proof.lean` adopts `SimpleGraph.tutte` from the manifest-pinned mathlib dependency. It installs the
declaration at the frozen `MathlibTerminal` interface, consumes both children of the checked root
composition, and proves the exact `TutteOneFactorTarget`. A separately written direct wrapper
rechecks the same canonical target by unfolding `OddComponentCondition`, `IsTutteViolator`, and
`not_lt`. The two root wrappers deduplicate to one upstream proof body.

Lean reports `SimpleGraph.tutte`, the installed terminal, and both exact roots sorry-free. Their
axiom closures are exactly `propext`, `Classical.choice`, and `Quot.sound`. The proof module contains
no placeholder, custom axiom, opaque or unsafe declaration, oracle, native evaluation, external
implementation, or substituted target.

This is provisional proof-phase evidence for an `M0-W` root proposal. This packet does not claim theorem completion or accepted closure. Exact declaration evidence covers the root, terminal, and adapter;
the upstream body maps to all 44 proof-reachable required-machine IDs. The 16 internal source-body
decomposition plans lack abstract-child composition certificates and receive no individual closure
credit. Accepted state remains `[H1, M3, R4]` with no accepted obligation or receipt.

## Commands and results

Commands ran in this worker clone on 2026-07-15 (Asia/Shanghai). The Lean runner copied only the
three target modules into a fresh temporary directory, compiled temporary `Statement.olean` and
`ObligationTree.olean` files, placed that directory before the pinned `LEAN_PATH`, used
`--trust=0`, and removed the directory on exit. Existing canonical pinned `.lake` artifacts were
reused read-only. No `lake update`, `lake build`, dependency clone/fetch, network access, or `.lake`
mutation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets at ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0856
  exit 0: rank 1410, planned, L0/rework_required, theorem_complete=false

bash Stage1_Instances/THM-M-0856/check_proof.sh
  exit 0: temporary trust-zero Statement and ObligationTree oleans compiled;
  the terminal, installed terminal, frozen-composition root, and direct exact
  root elaborated; four sorry checks passed and all four axiom reports were
  exactly [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-0856/build_obligation_artifacts.py --check
  exit 1: the deterministic obligation generator now emits typed-graphs.json
  with the current authoritative execution-DAG hash; the integrated frozen
  artifact intentionally retains its predecessor-phase hash

python3 -B Stage1_Instances/THM-M-0856/check_obligation_tree.py
  exit 1: the immutable predecessor checker reaches its stale execution-DAG
  fingerprint assertion; the proof checker separately rechecks the unchanged
  statement, registry, graph structure, denominator, composition, and hashes

python3 -B Stage1_Instances/THM-M-0856/check_proof.py
  exit 0: exact source markers, frozen target and graph, receipt/input hashes,
  mathlib revision/tree/source/blob/body/olean, worker packet, placeholder
  policy, and dirty-scope boundary passed

PYTHONPYCACHEPREFIX=/tmp/stage1-m0856-proof-pycache python3 -m py_compile \
  Stage1_Instances/THM-M-0856/check_proof.py
  exit 0: checker syntax compiled outside the repository

python3 -m json.tool Stage1_Instances/THM-M-0856/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both structured artifacts parsed

git diff --check -- Stage1_Instances/THM-M-0856 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The prerequisite receipts and this proof receipt remain provisional until dependency-ordered
master acceptance. Human-source H0, readable R0, complete transitive provenance and trust, cold
hermetic replay, independent verification, validation, release, `AUDIT-Z`, `THEOREM-Z`, and theorem
completion remain open.
