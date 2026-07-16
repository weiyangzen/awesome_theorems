# THM-M-0412 Anchor-Audit Revalidation: Blocked

Item `S56-M-0412-ANCHOR_AUDIT` was rechecked at base
`f545339546bf410d5110d7fe44e70bdcf5d8b48e` (tree
`6dc924134293b2674df7324ff98b6fdaf660159e`) in exact claim order
`(v2 rank 259, phase layer 2, S56-M-0412-ANCHOR_AUDIT)`.

## Verdict

`blocked`. The integrated six-candidate inventory still gives useful bounded
negative classifications, but the mandatory scheduler-owned validator cannot
prove the phase predicate at this claim base. Its exact contract argv exits `1`
and emits exactly one `stage1-validator-semantic-result/1.0` JSON object with
`verdict=repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, and `message="repository revision drift"`.

The contract selects exactly one candidate:
`Stage1_Instances/THM-M-0412/check_anchor_audit.py`. Its SHA-256 is
`c3e639d6...d810a0`, its HEAD/base Git blob is
`482afc5d...4801`, and the scheduler selector accepts the immutable candidate
at this base. The failure is semantic freshness, not validator absence or
ambiguity. The validator freezes base `307c34d3...`, graph `8be71ef1...`, an
anchor ledger hash later replaced by obligation-tree work, and the old `[ ]`
phase state. This worker did not change or add any declared validator candidate.

The sole `anchor-audit-receipt.json` cannot repair this. It is also bound to
base `307c34d3...`; current-base role resolution fails with `phase receipt
base_revision disagrees with worker base`. Historical-base role resolution
rejects `inputs.discovery_evidence[0].tracking_state`, and later rows also use
other fields outside the closed role-binding schema. Its ledger, graph, and
tracking-state claims no longer describe HEAD. There is therefore no truthful
current-base receipt and positive immutable-validator replay for a self-test
handoff.

## Dependency And Reuse Boundary

The authoritative direct/transitive hard-parent inspection closure, hard-edge
set, reuse-hint set, and shared-group set are all exactly empty. The supplied
empty `parent_inspection_order` was traversed exactly once before any possible
proof work. No proof work was performed, and no declaration, receipt, checkbox,
provider acceptance, or proof credit was reused.

The tracked schema-1.1 ledger was later refreshed for
`S56-M-0412-OBLIGATION_TREE`; it now binds phase layer 3, graph `d5b27da9...`,
and base `a103f2e1...`. The assigned anchor phase instead requires layer 2,
graph `39dc7ce5...`, and base `f5453395...`. Updating only the ledger would fail
the protected validator's pinned digest and invalidate the inventory and
receipt hashes, so this worker records the mismatch rather than manufacturing a
partial packet.

## Inventory Boundary

The frozen inventory remains a useful negative audit:

- Repo-local `S1_M_021.lean` is an abstract Nagell-Lutz-shaped interface, not a
  concrete source-faithful proposition or terminal proof. Its local
  `native_decide` budget lemma is not root proof evidence.
- Pinned mathlib still lists Nagell-Lutz in `docs/1000.yaml` without `decl` or
  `decls`. The checked Weierstrass, discriminant, two-torsion, and affine-point
  declarations are support APIs only.
- The content-bound public-project observations identify no immutable external
  Lean 4 terminal source. This is bounded negative evidence, not a global
  absence or saturation result.
- The Cassels/OpenAlex/Crossref evidence leaves the Pierce label, Nagell
  attribution, 1948 date, and cubic gloss conflicted. Choosing Nagell-Lutz,
  Ramanujan-Nagell, or another cubic theorem would substitute mathematics.

All six frozen candidates remain classified across the seven prescribed lanes,
with no exact terminal candidate and no root proof credit. The root remains
`H5 / M4 / R4`; `audit_complete=false` and `theorem_complete=false`.

## Narrow Validation

All dependency use was read-only. No network request, Lake update/build,
dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0412/check_anchor_audit.py` | 1 | one typed JSON result; `repair_required`, `phase_accepted=false`, `phase_predicate_proven=false`, repository revision drift |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/AnchorAudit.lean` | 0 | six adjacent pinned APIs elaborated; three nonfatal sandbox stream-fd warnings; no target or proof credit |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | 7 phases, 12 common gates, 23 source references |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all structural authorities passed before this blocker file was added |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 nodes, 10822 states, 2 hard edges, 5 hints, 311 groups, acyclic, before this blocker file was added |
| `python3 Docs/tools/check_stage1_standard.py` (post-edit) | 1 | expected integration boundary: fresh generation inventories the new blocker while this worker cannot edit the derived DAG |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` (post-edit) | 1 | same expected target evidence-inventory projection drift; master must regenerate the read-only projection |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranked uniform-L0 targets |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | rank 21, planned, legacy evidence unaccepted, theorem incomplete |
| read-only legacy inventory and required-item revalidation plan under `/tmp` | 0 | current HEAD selects this `[_]` item at rank 259/layer 2 and marks role ambiguity plus validator-base mismatch blocked; no validator or state transition executed |

## Retry Condition

An authority-maintenance/master action must land one corrected declared
validator together with a refreshed anchor-layer ledger, inventory, discovery
evidence, validation record, and sole node receipt against one current graph and
base. It must remove non-schema role-binding prose while preserving the honest
negative classifications and zero proof credit. A fresh claim must then start
from a base already containing that unchanged validator blob. Only then can a
worker produce the required positive semantic replay and the master resolve
HEAD roles, perform independent review, and apply dependency-ordered CAS after
the statement predecessor is accepted `[x]`.

This is target-scoped blocker evidence only. It does not satisfy the assigned
phase, propose `[_]`, replace the phase receipt or validator, claim audit or
theorem completion, change task state, or claim master acceptance. Because the
assigned phase is not genuinely self-tested, `.stage1-worker-selftest.json` is
deliberately absent.
