# THM-M-0123 anchor-audit current-HEAD blocker

Item: `S56-M-0123-ANCHOR_AUDIT`

Worker base revision: `6cff7bae0e4547cf9ad8b7abaae20d1abb9fe049`

Worker base tree: `28c148dbd84fbd549c749f060c92c9a3f00b16d0`

Claim order: `(v2_execution_rank=276, phase_layer=2,
phase_item_id=S56-M-0123-ANCHOR_AUDIT)`

Worker verdict: `blocked`; no phase receipt or self-test handoff is emitted.

## First Failed Gate

`G05-AUTHORITY-REPLAY.immutable_HEAD_validator_is_stale_for_worker_base`

The mandatory HEAD phase contract declares these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0123/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0123/check_anchor.py`

Exactly the first path exists. It is unchanged from HEAD, with Git blob
`67ed038b2fd206f92705cef5b7846780059d03de` and SHA-256
`6166d1c2d444d4523ca76551c35f43807d6ce7d4b92411b0f3a4fd7e4a7c62dd`.
The exact contract argv is:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0123/check_anchor_audit.py
```

It exits `1`, writes no stderr, and emits exactly one 463-byte JSON object on
stdout. The stdout SHA-256, including its final LF, is
`e7f1123863358d53eb51cab3c9035465c0c7a8a73ff2b2d2df8433001ebb8d1a`:

```json
{"audit_complete": false, "blocked": false, "first_failed_gate": "ANCHOR-AUDIT-SEMANTIC-CHECK", "item_id": "S56-M-0123-ANCHOR_AUDIT", "message": "repository revision drift", "open_obligations": 1, "phase": "anchor_audit", "phase_accepted": false, "phase_predicate_proven": false, "schema_version": "stage1-validator-semantic-result/1.0", "stale_inputs": [], "status": "failed", "theorem_complete": false, "theorem_id": "THM-M-0123", "verdict": "repair_required"}
```

The scheduler parser accepts that object under the exact
`stage1-validator-semantic-result/1.0` schema. Its negative semantics are
authoritative for this attempt. The validator freezes repository revision
`307c34d30fc3763c82a944a142ae922b48ff18aa`, tree
`ef45ba442c71959db78ad146a023bcf32946a53f`, theorem-DAG SHA-256
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`,
and the earlier empty reuse context. Current HEAD instead has the base and tree
above, theorem-DAG SHA-256
`80cf05109d5b3776b7defe95fdb591b216894a57ecbb7180a59f315a67d487d5`,
and dependency-context SHA-256
`0c0f6d1bed857aeaad7b4656db6ae6fe5c9c6bde39f7c9fb9ec2f8938eb4a484`.
Worker policy forbids refreshing, replacing, renaming, deleting, or wrapping
either declared candidate.

The tracked `anchor-audit-receipt.json` is historical evidence, not a
current-base receipt. It binds the old base and tree, says `accepted=false`,
and predates the current shared-group context. Rewriting it without a passing
unchanged scheduler-owned validator would manufacture a phase packet and
violate the exactly-one-receipt rule. Therefore this attempt leaves that
receipt unchanged and produces no `.stage1-worker-selftest.json`.

`G02-TOPOLOGY` is independently pending. The authoritative v2 task state has
both `S56-M-0123-STATEMENT` and this item at `[_]`, not master-accepted `[x]`.
No predecessor checkbox or receipt transfers acceptance.

## Dependency And Reuse Audit

The complete `parent_inspection_order`, direct-hard-parent closure,
transitive-hard-ancestor closure, hard-edge list, and reuse-hint list are all
exactly empty. The prescribed parent traversal was therefore the empty
sequence, traversed exactly once before any possible proof work. No proof work
was performed, and no parent declaration, terminal proof body, receipt,
checkbox, acceptance, or evidence credit was consumed.

The current graph adds one nonblocking weak group:
`SHARED-MODULE-dff4d00d3b45e946`, canonical identity
`Atlas.ArithmeticGeometry.code.FaltingsTheorem`, with members `THM-M-0122`
and `THM-M-0123`. The group expressly records module co-mention only, not a
common lemma or proof body.

`THM-M-0122` was inspected read-only at current HEAD. Its authoritative phase
states are intake `[_]`, statement `[_]`, anchor audit `[_]`, obligation tree
`[_]`, proof `[_]`, validation `[ ]`, and release `[ ]`. Material inspected
bytes were:

| Provider artifact | SHA-256 | HEAD Git blob |
|---|---|---|
| `Stage1_Instances/THM-M-0122/Statement.lean` | `824c2d9410bbf3117fa6340e4259f9a3a7df6ff892c4b7cc6dad94a03ab437e8` | `b3831f8318cb743c2987c52f7042c1c9ad1b4ff9` |
| `Stage1_Instances/THM-M-0122/AnchorAudit.lean` | `15039aefbdd9a98db43a4583bbd19971edd5817a9c969bae344a8575073ad779` | `7f53945e3ead93ca4746fac05fdee940c736b0ff` |
| `Stage1_Instances/THM-M-0122/ObligationTree.lean` | `c081ee9e08e5bf5aeb3060605ebc9c7f7926d08d04632380e105e8ff1c783c69` | `965138b260061d124440ec5508cb7788197a207c` |
| `Stage1_Instances/THM-M-0122/Proof.lean` | `07c9c730d01964dc4aeea81b2af34a8fc59a105301751e78ea0eccfa1a521e1a` | `b53a6e7f174841587c65d95f421eddcac144db70` |
| `Stage1_Instances/THM-M-0122/anchor-audit.json` | `3da3f5c769e138a1c623eea5395483982e068a1d23c7f06fd69842f13524ac16` | `847fdae9c48b6e2a8bb51e62de6920a7aeff3687` |
| `Stage1_Instances/THM-M-0122/anchor-audit-receipt.json` | `78ca0f4099b681ddbff6f90148d0380763510e915788fa628cddf1d6b82bcaff` | `1e7183e56ba024df87f8984d05037718a9e0193e` |
| `Stage1_Instances/THM-M-0122/proof-blocker.json` | `3b5183c462e84be52662958fb014d72a47088f0d002ca59d96bf14ed086b369e` | `de487ea11c19109e9bfea9624173d531314bba8e` |
| `Stage1_Instances/THM-M-0122/proof-receipt.json` | `934c4795e4baebe5feb838e8e2cbdb78b0bfc3b71c2c45c62fcb76aa1f7b78d3` | `a1f7270f77e4ec95cb75e8f78d037dac61924f99` |

The reuse decision is `not_applicable`. The provider statement uses a
concrete projectivity predicate while the consumer freezes properness, so the
statements are not definitionally identical and no checked cross-target
transport exists. More importantly, the provider has no premise-free Faltings
body: `Proof.lean` proves generic injection transports and a conditional root
composer that still requires explicit normalization, Abel-Jacobi, and
Mordell-Lang packages. Its proof receipt is `accepted=false` and records an
open six-obligation arithmetic-geometric cut set. Both targets merely audit
the same Atlas declaration whose body is directly `by sorry`. No provider
source is imported or copied, no consumer wrapper is created, no validation
receipt is claimed, and provider provisional state or acceptance is not
inherited.

The integrated schema-1.1 `dependency-reuse-ledger.json` is now stale: it
binds the old graph, repository revision, empty `shared_group_ids`, and empty
`reuse_decisions`. A worker-authored ledger refresh cannot make the immutable
validator pass because the validator pins the old ledger hash and rejects the
current repository before evaluating it. This blocked attempt therefore
records the current group decision here without creating a partial or
misleading receipt/ledger pair. A fresh eligible run must refresh the ledger
and bind this exact `not_applicable` decision.

## Anchor Boundary

The integrated bounded ten-candidate inventory remains useful discovery
guidance. It covers all seven required lanes in order. The repo-local exact
target is statement-only (`M3`); pinned mathlib provides geometry,
cohomology, Northcott, and descent substrate but no terminal Mordell/Faltings
theorem; the official documentation row has no declaration; the immutable
Atlas candidate is materially mismatched and directly `by sorry` (`M5`); and
the Formal Conjectures observation found no matching path. Public discovery
was access-limited and does not establish saturation. The primary Faltings
source still lacks an exact locator, corrections and assumption crosswalk,
and independent H0 review.

No new exact terminal candidate appeared in this read-only replay. The root
remains `H4/M3/R3`; `audit_complete=false` and `theorem_complete=false`.

## Checks Run

No `lake update`, `lake build`, dependency clone/fetch, checkout, or `.lake`
mutation was performed. The automation-provided canonical `.lake` symlink was
used read-only.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, v2 DAG, contract, and skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 phase states, 2 hard edges, 5 hints, and 311 shared groups passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and twenty-three source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranked L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0123` | 0 | Rank 42, planned, rework required, theorem incomplete. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0123/check_anchor_audit.py` | 1 | Exactly one schema-valid typed negative JSON object; `repair_required`, message `repository revision drift`. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0123/Statement.lean` | 0 | Exact target and checked transports re-elaborated; expected `#check_failure` diagnostics confirm mutation separation. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0123/AnchorAudit.lean` | 0 | Pinned support declarations elaborated; the Northcott wrapper reports no axioms. |
| scheduler semantic-result parser on exact validator stdout | 0 | The one-object closed schema parses; its negative phase result is preserved. |
| provider/current-HEAD byte comparison | 0 | All inspected `THM-M-0122` bytes match HEAD; no provider path was modified. |

## Retry Condition

The scheduler must publish a refreshed sole `check_anchor_audit.py` at a new
authoritative commit, then issue a fresh claim whose base contains that
identical validator blob. The fresh worker must refresh the schema-1.1 ledger
against graph digest
`80cf05109d5b3776b7defe95fdb591b216894a57ecbb7180a59f315a67d487d5`
and context digest
`0c0f6d1bed857aeaad7b4656db6ae6fe5c9c6bde39f7c9fb9ec2f8938eb4a484`,
bind the weak-group `not_applicable` decision, refresh exactly one phase
receipt with complete current-HEAD role bindings, and replay the unchanged
validator. A self-test handoff may be emitted only if that typed result proves
the phase predicate. Master acceptance additionally waits for the statement
predecessor to reach `[x]`, independent review, final authority-owned role
bindings, regenerated projections, and SSOT compare-and-swap.

This target-scoped blocker changes no task state, ledger, phase receipt,
validator, theorem source, lifecycle, debt vector, or acceptance. It grants no
proof credit, `AUDIT-Z`, `THEOREM-Z`, or master acceptance.
