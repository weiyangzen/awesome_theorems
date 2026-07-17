# THM-M-0390 anchor-audit validator-authority blocker

## Scope and authority

This is the target-scoped fail-closed result for
`S56-M-0390-ANCHOR_AUDIT` at worker base
`629a7ce266289b9ad49a37c0cc4d89b7b148cf36` (tree
`97daff5e375fca5b6781ccf0dede0d1c25648e19`). It changes no Lean
source, phase receipt, validator candidate, task-state authority, theorem-DAG
projection, lifecycle, debt vector, or acceptance state.

The exact claim tuple is `(v2_execution_rank=4, phase_layer=2,
phase_item_id=S56-M-0390-ANCHOR_AUDIT)`. The sole task-state authority reports
this item `[_]` with two attempts and its statement predecessor `[_]`; both
remain unfinished. The authoritative theorem-DAG SHA-256 is
`de71a3ca00b2ac64f96f4a0b7363cf56d09acb943716310332e693d9c9503c6a`,
and the stable dependency-context SHA-256 is
`a615cea5c684a96055d1d5bb30bdcfccbc499a62f7fcfac3490551cb836c1598`.

## Dependency and reuse audit

The supplied direct hard-parent, transitive hard-ancestor, hard-edge,
reuse-hint, and `parent_inspection_order` lists are exactly empty. The complete
empty order was traversed exactly once, in order, before any possible proof
work. No proof work was performed, so there is no provider body to import,
copy, or transport. Inspected hard-parent IDs, reused declaration IDs, and
accepted receipt IDs are all empty.

The sole nonblocking dependency context is weak shared-module group
`SHARED-MODULE-32f9c9eb1b52d871`, canonical identity
`Mathlib.NumberTheory.FLT.Polynomial`. Its other member, `THM-M-0133`, was
re-inspected as guidance only. Its authoritative seven phase states are all
`[_]`. Its statement, anchor inventory, proof source, and validation receipt
still have SHA-256 values `01ea9240ac0d33b11938232c382812ca369b21aeeda4b2bd24cae960996421e1`,
`98dd1ebb992bcd54fe4158551f2d98a09d8e95e783e31cb5c0135ed8426a72ca`,
`edf992203932c7a16827e75bc0954ecddfcc4ce966778b40d1a9c090cac43a6d`,
and `c8f42b62d303e0eb882427837db87a3f475cb5eded737f359f26815336b2d2f9`.
Its exact target is Fermat's Last Theorem, its root remains conditional on the
all-odd-prime family, and `Polynomial.flt_catalan` is a field-polynomial
theorem concluding three constant degrees. Neither is an exact body or checked
transport for the natural-number `CatalanStatement`. The decision remains
`not_applicable`; no declaration, terminal body, receipt, checkbox state,
evidence credit, or acceptance transfers.

The tracked `stage1-dependency-reuse-ledger/1.1` truthfully records the empty
hard closure, this one weak-group decision, and no unresolved compatibility
obligations. It is historical, however: it binds repository revision
`c5037228977a81948bbd6119e1728b4b65b9924e` and graph digest
`fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518`.
Refreshing it alone would violate the immutable validator's pinned ledger hash
and could not prove the phase predicate. This blocked run therefore does not
manufacture a partial ledger/receipt packet.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_candidate_stale` is the first
worker-unrepairable gate. The mandatory HEAD contract declares these
scheduler-owned candidates:

- `Stage1_Instances/THM-M-0390/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0390/check_anchor.py`

Exactly one exists: `check_anchor_audit.py`, SHA-256
`36b8d075f9a09ecd598ad0a69696265644dee6b984c83b87a0c89537126bad08`,
Git blob `50c2541e90f0f01795bb51b18b25a13bf9660137`. Candidate selection is
unambiguous. This worker did not create, refresh, rename, replace, or delete
either protected path.

The selected validator is internally bound to obsolete base
`c5037228977a81948bbd6119e1728b4b65b9924e`, tree
`78b2627e717156dffe240bea12d14205af667d2a`, and theorem-DAG SHA-256
`fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518`.
The exact contract-selected invocation was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py
```

It exited `1`, wrote no stderr, and emitted exactly one 463-byte JSON object,
including its final line feed, with SHA-256
`e737f1c1abc68113dc377db8293ce83a978ff3bca827fa90e80206a7cb518abe`:

```json
{"audit_complete": false, "blocked": false, "first_failed_gate": "ANCHOR-AUDIT-SEMANTIC-CHECK", "item_id": "S56-M-0390-ANCHOR_AUDIT", "message": "repository revision drift", "open_obligations": 1, "phase": "anchor_audit", "phase_accepted": false, "phase_predicate_proven": false, "schema_version": "stage1-validator-semantic-result/1.0", "stale_inputs": [], "status": "failed", "theorem_complete": false, "theorem_id": "THM-M-0390", "verdict": "repair_required"}
```

The stdout protocol is structurally correct, but its typed semantics expressly
prove neither the phase predicate nor phase acceptance. Exit status alone
cannot override that result, and an undeclared adapter is inadmissible.

The sole phase receipt is also stale: it binds the same obsolete base/tree,
and its receipt-bound discovery rows contain `binding_boundary`, outside the
HEAD role resolver's closed binding schema. Rewriting the receipt cannot be
truthful while the unchanged selected validator reports `repair_required`.
`G02-TOPOLOGY` is independently pending because `S56-M-0390-STATEMENT` is
`[_]`, not master-accepted `[x]`.

## Current anchor boundary

The bounded six-candidate, seven-lane classification preserves its negative
mathematical boundary, but several historical evidence assertions are stale.
The canonical pinned read-only cache currently contains
`Mathlib/NumberTheory/FLT/Polynomial.olean`, SHA-256
`7a4c5f1b836d00bc79700cda1c80f91710be2253934e4fcb5d4bbfcbc211337e`,
size 48088 bytes. A trust-zero scratch import probe elaborates
`Polynomial.flt_catalan` without a build, update, clone, or fetch. The existing
inventory, discovery evidence, receipt, and validation prose instead say the
olean or import probe is unavailable. This changes dependency feasibility,
not compatibility or root proof credit.

`discovery-evidence.json` also combines the current SHA-256
`001442492b5a891d966bd8ab4b4521dd63ec6f5a49c9e500217c9705fd379fd1`
of `anchor-audit-validation.md` with predecessor Git blob
`7ed460ebac078396d4fd1cc3651664f4a0afdde7`; the current HEAD blob is
`f992749b880f998ffe8908af57709fd77ae894ae`. That pair is not a valid
current content/blob binding.

The remaining classifications stay honest: repo-local material provides
statement shapes, transports, finite checks, and open architecture but no
terminal root body; pinned mathlib has documentation row `Q174955` without a
declaration; the materially mismatched polynomial theorem and support APIs do
not close the root; Formal Conjectures revision
`7871d8fc7a8164a1ac16c3765b40c25ce015b681` contains the near statement
with `by sorry`; public discovery is access-limited rather than saturated; and
the primary paper still lacks pinpoint source/assumption/errata review. The
strongest root boundary remains `M3/E4` formalization debt, with no H0, R0,
root proof credit, `AUDIT-Z`, or theorem completion.

## Checks run

No network request, `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation was performed. The automation-provided untracked `.lake`
symlink is outside the owned path and excluded from this handoff.

| Command | Exit | Result |
|---|---:|---|
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py` | 1 | exactly one typed negative JSON result: `repair_required`, message `repository revision drift` |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0390/Statement.lean` | 0 | exact Init-only statement and four mutation surfaces elaborate |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard, target set, v2 DAG, phase contract, and skill pass |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 nodes, 10822 states, two hard edges, five hints, 311 groups, and acyclicity pass |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phases, twelve common gates, and 23 source references pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets pass |
| `python3 scripts/stage1_target.py show THM-M-0390` | 0 | rank 4, planned lifecycle, theorem incomplete |

## Retry condition and status boundary

The scheduler or authority-maintenance lane must publish one corrected
declared validator together with one coherent current-base packet: refreshed
schema-1.1 ledger, anchor inventory, discovery evidence, validation record,
and sole phase receipt. It must repair the role bindings and stale olean/blob
observations while preserving the negative classifications and zero proof
credit. A fresh claim must begin from a base already containing that unchanged
validator. Only its positive typed replay may support
`.stage1-worker-selftest.json`; master acceptance additionally waits for the
statement predecessor to reach `[x]`.

Because the assigned phase is not genuinely self-tested, this handoff
deliberately contains no `.stage1-worker-selftest.json` and no replacement
phase receipt. It grants no state transition, phase acceptance, parent or
provider acceptance transfer, proof credit, audit completion, theorem
completion, or master acceptance.
