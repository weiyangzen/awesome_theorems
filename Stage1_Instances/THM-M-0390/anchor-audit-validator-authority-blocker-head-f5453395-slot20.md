# THM-M-0390 anchor-audit validator-authority blocker

## Scope

This is the target-scoped fail-closed result for
`S56-M-0390-ANCHOR_AUDIT` at worker base
`f545339546bf410d5110d7fe44e70bdcf5d8b48e` (tree
`6dc924134293b2674df7324ff98b6fdaf660159e`). It changes no theorem
source, prior phase receipt, task-state authority, theorem-DAG projection,
lifecycle, debt vector, or acceptance state.

The authoritative claim tuple is
`(v2_execution_rank=4, phase_layer=2,
phase_item_id=S56-M-0390-ANCHOR_AUDIT)`. The theorem-DAG SHA-256 is
`39dc7ce5f668c527de899e74c99840aef50e6be4c576aaf146abed1b6749275c`,
and the stable dependency-context SHA-256 is
`a615cea5c684a96055d1d5bb30bdcfccbc499a62f7fcfac3490551cb836c1598`.
The sole task-state authority reports this item `[_]` with two attempts and
its statement predecessor `[_]`; neither state is master acceptance.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_candidate_stale` is the first
mechanically unrepairable worker gate. The HEAD anchor-audit contract declares
these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0390/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0390/check_anchor.py`

Exactly one exists: `check_anchor_audit.py`, SHA-256
`36b8d075f9a09ecd598ad0a69696265644dee6b984c83b87a0c89537126bad08`,
Git blob `50c2541e90f0f01795bb51b18b25a13bf9660137`. Candidate selection is
therefore unambiguous, and this worker did not create, refresh, rename,
replace, or delete either protected path.

The selected validator is internally pinned to obsolete repository revision
`c5037228977a81948bbd6119e1728b4b65b9924e`, tree
`78b2627e717156dffe240bea12d14205af667d2a`, and theorem-DAG SHA-256
`fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518`.
The exact contract-selected invocation at the current base is:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py
```

It exits `1`, writes no stderr, and emits exactly one 463-byte JSON object
(including the final LF), SHA-256
`e737f1c1abc68113dc377db8293ce83a978ff3bca827fa90e80206a7cb518abe`:

```json
{"audit_complete": false, "blocked": false, "first_failed_gate": "ANCHOR-AUDIT-SEMANTIC-CHECK", "item_id": "S56-M-0390-ANCHOR_AUDIT", "message": "repository revision drift", "open_obligations": 1, "phase": "anchor_audit", "phase_accepted": false, "phase_predicate_proven": false, "schema_version": "stage1-validator-semantic-result/1.0", "stale_inputs": [], "status": "failed", "theorem_complete": false, "theorem_id": "THM-M-0390", "verdict": "repair_required"}
```

Exit zero alone would not be sufficient, and this typed negative result
expressly proves neither the phase predicate nor phase acceptance. The worker
is forbidden to edit a declared validator candidate, so it cannot repair this
gate or substitute an adapter.

The only existing phase receipt is also stale. It binds the obsolete base and
tree above, and its `/inputs/discovery_evidence` rows contain the extra field
`binding_boundary`, which is outside the HEAD role resolver's closed binding
schema. It cannot support a current-base role map or master review.

## Dependency And Reuse Audit

The supplied `parent_inspection_order`, direct hard-parent list, transitive
hard-ancestor list, hard-edge list, and reuse-hint list are all exactly empty.
The complete empty order was traversed once, in order, before any proof work;
no proof work was performed.

The sole nonblocking context is shared-module group
`SHARED-MODULE-32f9c9eb1b52d871`, a weak co-mention of
`Mathlib.NumberTheory.FLT.Polynomial` by `THM-M-0133` and `THM-M-0390`.
The provider's authoritative seven phases are all `[_]`. Its statement,
anchor inventory, proof source, and validation receipt retain the exact hashes
recorded in the target ledger. `Polynomial.flt_catalan` is a theorem over
`k[X]` concluding constant polynomial degrees, not an exact body or checked
transport for the natural-number consecutive-perfect-power target. The
decision remains `not_applicable`; no declaration, receipt, checkbox state,
proof body, evidence credit, or acceptance transfers.

The tracked `stage1-dependency-reuse-ledger/1.1` truthfully contains empty
`inspections`, the one weak-group decision, and no unresolved compatibility
obligations. It is nevertheless historical: it records graph digest
`fb17743f...` and revision `c5037228...`, not the required current digest and
base. Refreshing it alone would violate the protected validator's pinned
ledger hash and could not make the phase predicate true. This blocker therefore
records the current mismatch without manufacturing a partial receipt packet.

Inspected hard-parent IDs: none. Reused declaration IDs: none. Accepted
receipt IDs: none.

## Stale Anchor Evidence

The canonical pinned cache currently contains
`Mathlib/NumberTheory/FLT/Polynomial.olean`, SHA-256
`7a4c5f1b836d00bc79700cda1c80f91710be2253934e4fcb5d4bbfcbc211337e`,
size 48088 bytes. A read-only scratch probe imports the module and checks
`Polynomial.flt_catalan` successfully. Existing inventory, discovery, receipt,
and validation prose instead say the olean is unavailable. This changes only
dependency-feasibility evidence: the candidate still has a different carrier,
equation, hypotheses, and conclusion and therefore remains `M5` for root
credit.

There is also a content/blob mismatch in `discovery-evidence.json` for
`anchor-audit-validation.md`: its recorded SHA-256
`001442492b5a891d966bd8ab4b4521dd63ec6f5a49c9e500217c9705fd379fd1`
matches the current file, but its recorded Git blob
`7ed460ebac078396d4fd1cc3651664f4a0afdde7` is the predecessor; the actual
HEAD blob is `f992749b880f998ffe8908af57709fd77ae894ae`.

The bounded six-candidate, seven-lane classification otherwise retains its
honest negative boundary: no placeholder-free exact Lean 4 terminal body or
checked transport closes `Stage1.THM_M_0390.CatalanStatement`; the Formal
Conjectures near-statement contains `by sorry`; public search was access-limited
and is not saturated; the primary publication lacks a completed pinpoint
source/errata review. Root proof credit remains false, and H0, R0, AUDIT-Z,
THEOREM-Z, hermetic release, and independent verification remain open.

## Checks Run

All dependency use was read-only. No network request, `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py` | 1 | exactly one typed negative JSON result; `repair_required`, message `repository revision drift` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 targets, the v2 DAG, phase contract, and execution skill passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 states, 2 hard edges, 5 hints, 311 groups, and acyclicity passed |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | 7 phases, 12 common gates, and 23 source references passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0390` | 0 | rank 4, planned lifecycle, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0390/Statement.lean` | 0 | exact Init-only target and four mutation surfaces elaborated |
| `cd Formalizations/Lean && lake env lean --trust=0 /tmp/thm_m_0390_polynomial_import_probe.lean` | 0 | imported the pinned module and printed the materially mismatched polynomial theorem type |
| JSON parsing, self-test-absence check, and `git diff --check -- Stage1_Instances/THM-M-0390` | 0 | blocker is structured and no whitespace error is present |

The automation-provided untracked `.lake` symlink is not an owned-path change
and is excluded from this handoff.

## Retry Condition

The scheduler/master authority-maintenance lane must publish a corrected
declared validator together with one refreshed current-base ledger, anchor
inventory, discovery evidence, validation record, and sole phase receipt. It
must repair the role bindings and both stale-evidence findings while preserving
the negative candidate classifications and zero proof credit. A fresh claim
must start from a base already containing that unchanged validator blob. The
worker can then replay the exact selected argv and emit
`.stage1-worker-selftest.json` only if its semantic result is positive. Master
acceptance additionally waits for `S56-M-0390-STATEMENT` to reach `[x]`.

Because the assigned phase is not genuinely self-tested, this handoff
deliberately contains no `.stage1-worker-selftest.json` and no replacement
phase receipt. It grants no state transition, phase acceptance, provider
acceptance transfer, proof credit, audit completion, theorem completion, or
master acceptance.
