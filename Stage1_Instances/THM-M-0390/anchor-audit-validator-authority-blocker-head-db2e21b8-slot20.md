# THM-M-0390 anchor-audit validator-authority blocker

## Scope and authority

This is the target-scoped fail-closed result for
`S56-M-0390-ANCHOR_AUDIT` at worker base
`db2e21b8fec263c5b65014acb1ee2039566e35a3` (tree
`815414c57391f2c12871c05a6e3d2944b0f2fef2`). It changes no theorem
source, phase receipt, validator candidate, task-state authority, theorem-DAG
projection, lifecycle, debt vector, or acceptance state.

The authoritative claim tuple is
`(v2_execution_rank=4, phase_layer=2,
phase_item_id=S56-M-0390-ANCHOR_AUDIT)`. The task-state authority reports
both this item and `S56-M-0390-STATEMENT` as `[_]`; neither mark is master
acceptance. The theorem-DAG SHA-256 is
`91ea782c662e40b9608f8900ad586114c5ef8e8e5d2d2f13316185bd8f205067`,
and the stable dependency-context SHA-256 is
`a615cea5c684a96055d1d5bb30bdcfccbc499a62f7fcfac3490551cb836c1598`.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_candidate_stale` is the first worker-
unrepairable gate. The HEAD phase contract declares the scheduler-owned
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
acceptance. Command success alone would not suffice, and the worker may not
substitute an undeclared adapter.

The only phase receipt is also stale. It binds the obsolete base and tree,
and its receipt-bound discovery rows contain `binding_boundary`, outside the
HEAD role resolver's closed binding schema. A current-base role map therefore
cannot resolve it. No new receipt is truthful until the protected validator
is refreshed by its scheduler owner and then appears unchanged in a fresh
worker base.

## Dependency and reuse audit

The supplied `parent_inspection_order`, direct hard-parent list, transitive
hard-ancestor list, hard-edge list, and reuse-hint list are exactly empty. The
complete empty order was traversed once, in order, before proof work. No proof
work was performed.

The only nonblocking context is weak shared-module group
`SHARED-MODULE-32f9c9eb1b52d871`, which co-mentions
`Mathlib.NumberTheory.FLT.Polynomial` for `THM-M-0133` and this target. The
provider's seven phases are all `[_]`. Its tracked statement, anchor audit,
proof source, and validation receipt still match the hashes recorded in the
historical ledger. `Polynomial.flt_catalan` is over `k[X]` and concludes that
three polynomial degrees are zero; it is not an exact body or checked
transport for the natural-number consecutive-power target. The decision is
`not_applicable`. No declaration, receipt, checkbox state, body, evidence
credit, or acceptance transfers.

The tracked `stage1-dependency-reuse-ledger/1.1` has empty inspections, one
weak-group decision, and no unresolved compatibility obligations. It is
historical because it records graph digest `fb17743f...` and revision
`c5037228...`. Refreshing it alone would violate the protected validator's
pinned ledger hash and would not establish the phase predicate. This report
binds the current mismatch instead of manufacturing a partial phase packet.

Inspected hard-parent IDs: none. Reused declaration IDs: none. Accepted
receipt IDs: none.

## Stale anchor evidence

The canonical pinned read-only cache now contains
`Mathlib/NumberTheory/FLT/Polynomial.olean`, SHA-256
`7a4c5f1b836d00bc79700cda1c80f91710be2253934e4fcb5d4bbfcbc211337e`,
size 48088 bytes. A scratch import probe checks `Polynomial.flt_catalan`
successfully. The existing inventory, discovery evidence, receipt, and
validation prose instead say this olean is unavailable. The observation
changes dependency feasibility only: the declaration's carrier, equation,
hypotheses, and conclusion remain materially incompatible, so it still earns
no root proof credit.

`discovery-evidence.json` also binds `anchor-audit-validation.md` with the
correct current SHA-256
`001442492b5a891d966bd8ab4b4521dd63ec6f5a49c9e500217c9705fd379fd1`
but the predecessor Git blob `7ed460ebac078396d4fd1cc3651664f4a0afdde7`;
the current HEAD blob is `f992749b880f998ffe8908af57709fd77ae894ae`.

The bounded six-candidate, seven-lane result otherwise keeps its negative
boundary: no placeholder-free exact Lean terminal body or checked transport
closes `Stage1.THM_M_0390.CatalanStatement`; the Formal Conjectures near-
statement contains `by sorry`; public discovery was access-limited and not
saturated; and the primary publication still lacks pinpoint source/errata
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
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0390/Statement.lean` | 0 | exact Init-only statement and four mutation surfaces elaborate |
| `cd Formalizations/Lean && lake env lean --trust=0 /tmp/thm_m_0390_polynomial_import_probe.lean` | 0 | pinned polynomial module imports and the materially mismatched declaration type prints |
| JSON parsing and `git diff --check -- Stage1_Instances/THM-M-0390` | 0 | target evidence parses and this owned report has no whitespace errors |

The automation-provided untracked `.lake` symlink is outside the assigned
owned path and excluded from the handoff.

## Retry condition and status boundary

The scheduler/master authority-maintenance lane must publish one corrected
declared validator together with a refreshed current-base ledger, inventory,
discovery evidence, validation record, and sole phase receipt. It must repair
the role bindings and stale olean/blob claims while preserving the negative
classifications and zero proof credit. A fresh claim must start from a base
already containing that unchanged validator blob. Only a positive semantic
replay may support `.stage1-worker-selftest.json`; master acceptance also
waits for the statement predecessor to reach `[x]`.

Because the assigned phase is not genuinely self-tested, this handoff
deliberately contains no `.stage1-worker-selftest.json` and no replacement
phase receipt. It grants no state transition, phase acceptance, parent or
provider acceptance transfer, proof credit, audit completion, theorem
completion, or master acceptance.
