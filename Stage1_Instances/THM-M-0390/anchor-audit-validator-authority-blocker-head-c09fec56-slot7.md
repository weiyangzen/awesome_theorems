# THM-M-0390 anchor-audit validator-authority blocker

## Scope and claim order

This is the target-scoped fail-closed result for
`S56-M-0390-ANCHOR_AUDIT` at worker base
`c09fec56b723330b06490622768353922c42475f` (tree
`0d742d5018bc3b55b0352c28cca02f5d961018fb`). It changes no theorem
source, phase receipt, validator candidate, task-state authority, theorem-DAG
projection, lifecycle, debt vector, or acceptance state.

The authoritative claim tuple is
`(v2_execution_rank=4, phase_layer=2,
phase_item_id=S56-M-0390-ANCHOR_AUDIT)`. The sole task-state authority reports
the assigned item `[_]` with two attempts and its statement predecessor `[_]`;
both states remain unfinished. The current theorem-DAG SHA-256 is
`c5d478054cf32914251001d24d128b3b21ba29414965d64947d78768329660bd`,
and the stable dependency-context SHA-256 is
`a615cea5c684a96055d1d5bb30bdcfccbc499a62f7fcfac3490551cb836c1598`.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_candidate_stale` is the first
worker-unrepairable gate. The HEAD anchor-audit contract declares two
scheduler-owned candidates:

- `Stage1_Instances/THM-M-0390/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0390/check_anchor.py`

Exactly one exists at this base: `check_anchor_audit.py`, SHA-256
`36b8d075f9a09ecd598ad0a69696265644dee6b984c83b87a0c89537126bad08`,
Git blob `50c2541e90f0f01795bb51b18b25a13bf9660137`, mode `100644`.
Selection is unambiguous. This worker did not create, refresh, rename,
replace, or delete either protected candidate.

The selected validator is internally bound to obsolete repository revision
`c5037228977a81948bbd6119e1728b4b65b9924e`, tree
`78b2627e717156dffe240bea12d14205af667d2a`, and theorem-DAG SHA-256
`fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518`.
The exact contract-selected invocation was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py
```

It exited `1`, wrote no stderr, and emitted exactly one 463-byte JSON object
including its final line feed, SHA-256
`e737f1c1abc68113dc377db8293ce83a978ff3bca827fa90e80206a7cb518abe`:

```json
{"audit_complete": false, "blocked": false, "first_failed_gate": "ANCHOR-AUDIT-SEMANTIC-CHECK", "item_id": "S56-M-0390-ANCHOR_AUDIT", "message": "repository revision drift", "open_obligations": 1, "phase": "anchor_audit", "phase_accepted": false, "phase_predicate_proven": false, "schema_version": "stage1-validator-semantic-result/1.0", "stale_inputs": [], "status": "failed", "theorem_complete": false, "theorem_id": "THM-M-0390", "verdict": "repair_required"}
```

The stdout protocol is structurally correct, but the typed result expressly
proves neither the phase predicate nor phase acceptance. Exit status alone
cannot override it, and an undeclared adapter is not admissible.

The sole phase receipt is also stale. It records the obsolete base and tree,
and its receipt-bound discovery rows include `binding_boundary`, outside the
HEAD resolver's closed binding schema. Consequently it cannot resolve a
current-base authority-owned role map. A replacement receipt would not be
truthful while the immutable selected validator still returns
`repair_required`.

## Dependency and reuse audit

The supplied direct hard-parent, transitive hard-ancestor, hard-edge,
reuse-hint, and `parent_inspection_order` lists are exactly empty. The complete
empty inspection order was traversed once, in order, before any proof work. No
proof work was performed.

The only nonblocking context is weak shared-module group
`SHARED-MODULE-32f9c9eb1b52d871`, which co-mentions
`Mathlib.NumberTheory.FLT.Polynomial` for `THM-M-0133` and this target. The
provider's seven phase states remain `[_]`. Its tracked statement, anchor
inventory, proof source, and validation receipt still have the exact hashes
recorded in the historical ledger. Inspection of its declaration bodies,
obligation registry, typed proof/provenance/trust/workflow graphs, and sole
validation receipt confirms that its root is Fermat's Last Theorem and remains
conditional on the all-odd-prime family. `Polynomial.flt_catalan` is a theorem
over `k[X]` concluding constant polynomial degrees; it is neither an exact
body nor a checked transport for the natural-number consecutive-power target.
The weak-group decision remains `not_applicable`. No declaration, receipt,
checkbox state, terminal body, evidence credit, or acceptance transfers.

The tracked `stage1-dependency-reuse-ledger/1.1` correctly has no hard-parent
inspections, exactly one weak-group decision, no accepted reuse, and no
unresolved compatibility obligations. It is nevertheless historical: it
records graph digest `fb17743f...` and repository revision `c5037228...`, not
the required current digest and base. Refreshing the ledger alone would break
the protected validator's pinned ledger hash and still could not prove the
phase predicate. This report therefore records the current mismatch without
manufacturing a partial phase packet.

Inspected hard-parent IDs: none. Reused declaration IDs: none. Accepted
receipt IDs: none.

## Stale anchor evidence

The canonical pinned read-only cache contains
`Mathlib/NumberTheory/FLT/Polynomial.olean`, SHA-256
`7a4c5f1b836d00bc79700cda1c80f91710be2253934e4fcb5d4bbfcbc211337e`,
size 48088 bytes. A trust-zero scratch probe imports the module and elaborates
`Polynomial.flt_catalan`. A second trust-zero probe imports the pinned support
modules and elaborates `IsPrimePow`, `isPrimePow_nat_iff`, both recorded
power-equality declarations, and `Nat.factorization_pow`. The existing anchor
inventory, discovery evidence, phase receipt, and validation record instead
claim that these oleans or import probes are unavailable. This changes
dependency-feasibility evidence only: all declarations remain nonterminal or
materially mismatched and give no Catalan root proof credit.

`discovery-evidence.json` also binds `anchor-audit-validation.md` with its
current SHA-256
`001442492b5a891d966bd8ab4b4521dd63ec6f5a49c9e500217c9705fd379fd1`
but predecessor Git blob `7ed460ebac078396d4fd1cc3651664f4a0afdde7` rather than the current
HEAD blob `f992749b880f998ffe8908af57709fd77ae894ae`.

The bounded six-candidate, seven-lane result otherwise preserves its truthful
negative boundary. No placeholder-free exact Lean terminal body or checked
transport closes `Stage1.THM_M_0390.CatalanStatement`; the Formal Conjectures
near-statement contains `by sorry`; public discovery was access-limited and is
not saturated; and the primary publication still lacks pinpoint
source/assumption/errata review. Root proof credit, H0, R0, AUDIT-Z,
THEOREM-Z, hermetic release, and independent verification remain open.

## Checks run

No network request, `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py` | 1 | exactly one typed negative result: `repair_required`, message `repository revision drift` |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0390/Statement.lean` | 0 | exact Init-only target and mutation surfaces elaborate |
| `cd Formalizations/Lean && lake env lean --trust=0 /tmp/thm_m_0390_polynomial_import_probe.lean` | 0 | pinned polynomial module imports and the materially mismatched declaration type prints |
| `cd Formalizations/Lean && lake env lean --trust=0 /tmp/thm_m_0390_support_import_probe.lean` | 0 | all five pinned support declarations elaborate at their actual types |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 targets, v2 DAG, phase contract, and execution skill pass |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 nodes, 10822 states, two hard edges, five hints, 311 groups, and acyclicity pass |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phases, twelve common gates, and 23 source references pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets pass |
| `python3 scripts/stage1_target.py show THM-M-0390` | 0 | rank 4, planned lifecycle, theorem incomplete |

The automation-provided untracked `.lake` symlink is outside the assigned
owned path and excluded from this handoff.

## Retry condition and status boundary

The scheduler or authority-maintenance lane must publish one corrected
declared validator together with one coherent current-base packet: refreshed
schema-1.1 ledger, anchor inventory, discovery evidence, validation record,
and sole phase receipt. It must repair the role bindings and both stale-evidence
findings while preserving the negative candidate classifications and zero
proof credit. A fresh claim must begin from a base that already contains that
unchanged corrected validator. Only its positive typed replay may support
`.stage1-worker-selftest.json`; master acceptance additionally waits for the
statement predecessor to reach `[x]`.

Because the assigned phase is not genuinely self-tested, this handoff
deliberately contains no `.stage1-worker-selftest.json` and no replacement
phase receipt. It grants no state transition, phase acceptance, parent or
provider acceptance transfer, proof credit, audit completion, theorem
completion, or master acceptance.
