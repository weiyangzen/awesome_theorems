# THM-M-0390 anchor-audit scheduler blocker

## Scope

This is the target-scoped fail-closed result for
`S56-M-0390-ANCHOR_AUDIT` at worker base
`d25efdf450b6236f4750b2eea2cd4f545944d084` (tree
`4674db99ea873d6879a1fa73110c7af3f0884937`). It changes no theorem
source, phase receipt, validator candidate, task-state authority, theorem-DAG
projection, lifecycle, debt vector, or acceptance state.

The authoritative claim tuple is
`(v2_execution_rank=4, phase_layer=2,
phase_item_id=S56-M-0390-ANCHOR_AUDIT)`. The sole task-state authority reports
this item `[_]` with two attempts and its statement predecessor `[_]`; both
remain unfinished and neither state is master acceptance. The current
theorem-DAG SHA-256 is
`441c96e3905667f769f2377a70cff6cfd78835d6a92c3862ce6ccbc3bcf505fe`,
and the stable dependency-context SHA-256 is
`a615cea5c684a96055d1d5bb30bdcfccbc499a62f7fcfac3490551cb836c1598`.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_candidate_stale` is the first
worker-unrepairable gate. The HEAD phase contract declares the scheduler-owned
candidates `check_anchor_audit.py` and `check_anchor.py`. Exactly one exists:
`Stage1_Instances/THM-M-0390/check_anchor_audit.py`, SHA-256
`36b8d075f9a09ecd598ad0a69696265644dee6b984c83b87a0c89537126bad08`,
Git blob `50c2541e90f0f01795bb51b18b25a13bf9660137`. Selection is unambiguous.
This worker did not create, refresh, rename, replace, or delete either
protected candidate.

The selected validator is internally bound to obsolete repository revision
`c5037228977a81948bbd6119e1728b4b65b9924e`, tree
`78b2627e717156dffe240bea12d14205af667d2a`, and theorem-DAG SHA-256
`fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518`.
The exact contract-selected invocation at the current base was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py
```

It exited `1`, wrote no stderr, and emitted exactly one 463-byte JSON object
(including the final LF), SHA-256
`e737f1c1abc68113dc377db8293ce83a978ff3bca827fa90e80206a7cb518abe`:

```json
{"audit_complete": false, "blocked": false, "first_failed_gate": "ANCHOR-AUDIT-SEMANTIC-CHECK", "item_id": "S56-M-0390-ANCHOR_AUDIT", "message": "repository revision drift", "open_obligations": 1, "phase": "anchor_audit", "phase_accepted": false, "phase_predicate_proven": false, "schema_version": "stage1-validator-semantic-result/1.0", "stale_inputs": [], "status": "failed", "theorem_complete": false, "theorem_id": "THM-M-0390", "verdict": "repair_required"}
```

The typed result expressly proves neither the phase predicate nor phase
acceptance. Exit status alone is not semantic acceptance, and the worker may
not substitute an undeclared adapter.

The sole phase receipt is also stale. It binds the obsolete base and tree, and
its receipt-bound discovery rows contain `binding_boundary` and
`base_git_blob`, outside the HEAD role resolver's closed binding schema. It
also contains null Git-blob bindings. No current-base role map can resolve it,
and no replacement receipt is truthful without a positive replay of the
unchanged scheduler-owned validator.

## Dependency and reuse audit

The supplied `parent_inspection_order`, direct hard-parent list, transitive
hard-ancestor list, hard-edge list, and reuse-hint list are exactly empty. The
complete empty order was traversed once, in order, before any possible proof
work. No proof work was performed.

The only nonblocking context is weak shared-module group
`SHARED-MODULE-32f9c9eb1b52d871`, which co-mentions
`Mathlib.NumberTheory.FLT.Polynomial` for `THM-M-0133` and this target. The
provider's seven authoritative phases are all `[_]`. Its tracked anchor
inventory, statement, proof source, and validation receipt have SHA-256/Git
blob pairs respectively:

- `98dd1ebb992bcd54fe4158551f2d98a09d8e95e783e31cb5c0135ed8426a72ca` /
  `6af0e07140527db641e033952e42e45913775a8f`
- `01ea9240ac0d33b11938232c382812ca369b21aeeda4b2bd24cae960996421e1` /
  `311e541f15eb5a99e37103fba3cfa9d5fc472a05`
- `edf992203932c7a16827e75bc0954ecddfcc4ce966778b40d1a9c090cac43a6d` /
  `9012882bef420155c1c7040f3b74593c70e5d2fe`
- `c8f42b62d303e0eb882427837db87a3f475cb5eded737f359f26815336b2d2f9` /
  `ac06c36f993cfa6919413b4494e44bd35e2b47b0`

`Polynomial.flt_catalan` is over `k[X]` and concludes that three polynomial
degrees are zero. It is neither an exact body nor a checked transport for the
natural-number consecutive-perfect-power target. The decision remains
`not_applicable`; no declaration, receipt, checkbox state, proof body,
evidence credit, or acceptance transfers.

The tracked `stage1-dependency-reuse-ledger/1.1` has empty inspections, the
one weak-group decision, and no unresolved compatibility obligations. It is
historical because it records graph digest `fb17743f...` and revision
`c5037228...`, rather than this run's graph and base. Refreshing it alone would
contradict the protected validator's pinned ledger hash and would not establish
the phase predicate. This blocker therefore binds the current mismatch instead
of manufacturing a partial phase packet.

Inspected hard-parent IDs: none. Reused declaration IDs: none. Accepted
receipt IDs: none.

## Stale anchor evidence

The canonical pinned read-only cache contains
`Mathlib/NumberTheory/FLT/Polynomial.olean`, SHA-256
`7a4c5f1b836d00bc79700cda1c80f91710be2253934e4fcb5d4bbfcbc211337e`,
size 48088 bytes. The existing inventory, discovery evidence, receipt, and
validation prose instead say this olean is unavailable. This changes only
dependency-feasibility evidence: the candidate remains materially
incompatible and receives no root proof credit.

`discovery-evidence.json` also binds `anchor-audit-validation.md` with its
current SHA-256
`001442492b5a891d966bd8ab4b4521dd63ec6f5a49c9e500217c9705fd379fd1`
but the predecessor Git blob `7ed460ebac078396d4fd1cc3651664f4a0afdde7`;
the current HEAD blob is `f992749b880f998ffe8908af57709fd77ae894ae`.

The bounded six-candidate, seven-lane result otherwise retains its negative
boundary: no placeholder-free exact Lean terminal body or checked transport
closes `Stage1.THM_M_0390.CatalanStatement`; the Formal Conjectures
near-statement contains `by sorry`; public discovery was access-limited and
not saturated; and the primary publication still lacks pinpoint source/errata
review. Root proof credit, H0, R0, AUDIT-Z, THEOREM-Z, hermetic release, and
independent verification remain open.

## Checks run

No network request, `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py` | 1 | one typed negative JSON result: `repair_required`, message `repository revision drift` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard, target set, v2 DAG, phase contract, and execution skill pass |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 nodes, 10822 states, two hard edges, five hints, 311 groups, acyclic |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phases, twelve common gates, and 23 source references pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets |
| `python3 scripts/stage1_target.py show THM-M-0390` | 0 | rank 4, planned lifecycle, theorem incomplete |
| `cd Formalizations/Lean && PATH="$HOME/.elan/bin:$PATH" lake env lean --trust=0 ../../Stage1_Instances/THM-M-0390/Statement.lean` | 0 | exact Init-only target and four mutation surfaces elaborate |
| JSON parsing and `git diff --check -- Stage1_Instances/THM-M-0390` | 0 | target evidence parses and the owned report has no whitespace errors |

The automation-provided untracked `.lake` symlink is outside the assigned
owned path and excluded from the handoff.

## Retry condition and status boundary

The scheduler/master authority-maintenance lane must publish one corrected
declared validator together with a refreshed current-base ledger, inventory,
discovery evidence, validation record, and sole phase receipt. It must repair
the role bindings and stale olean/blob claims while preserving the negative
classifications and zero proof credit. A fresh claim must start from a base
already containing that unchanged validator blob. Only a positive semantic
replay may support `.stage1-worker-selftest.json`; master acceptance also waits
for the statement predecessor to reach `[x]`.

Because the assigned phase is not genuinely self-tested, this handoff
deliberately contains no `.stage1-worker-selftest.json` and no replacement
phase receipt. It grants no state transition, phase acceptance, parent or
provider acceptance transfer, proof credit, audit completion, theorem
completion, or master acceptance.
