# THM-M-0110 proof validator-authority blocker

## Scope

This is the target-scoped fail-closed handoff for `S56-M-0110-PROOF` at
worker base `0c2274d4ca42a99c4281bd566d19f1db7530a87a` (tree
`d1b6ec259121c90799df53290217af4ee29444b3`). It changes no Lean source,
phase receipt, dependency ledger, task-state authority, theorem-DAG
projection, lifecycle, debt vector, or acceptance state.

The authoritative claim tuple is
`(v2_execution_rank=269, phase_layer=4, phase_item_id=S56-M-0110-PROOF)`.
The theorem-DAG SHA-256 is
`78e8063002c0e50e2b2d5de6f539073b0a91215542ff3ae241b5d03c0bf05e22`,
and the stable dependency-context SHA-256 is
`4f60e4c0e01ec4cc069fbe1a7601aabdc8f2acf1df3e4c917e09e4235cec640b`.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_base_binding_stale` is the first
mechanically unrepairable worker gate. The mandatory HEAD phase contract
(SHA-256
`1e7adf0f4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`)
declares these scheduler-owned proof-validator candidates:

- `Stage1_Instances/THM-M-0110/check_proof.py`
- `Stage1_Instances/THM-M-0110/check_proof.sh`

Exactly one candidate exists: `check_proof.py`, with SHA-256
`56981df1e84360fba842e48c3c0837a94e0b2776240a1d60752e81cc71d8c5d5`
and Git blob `d7f9f2d58a1b8e77ee441f504d8317836eeddfbe`. It is present unchanged at
the current worker base, so the scheduler-selected argv is exactly:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0110/check_proof.py
```

The command exits `1` and emits exactly one JSON object with schema
`stage1-validator-semantic-result/1.0`. Its typed result is `status=failed`,
`verdict=repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, `first_failed_gate=P01-ARTIFACTS`, and message
`proof evidence replay failed: repository HEAD differs from the claimed worker base`.
Stdout is 464 bytes with SHA-256
`48a03a4889d12a6a567c7eeec3b93c148c93d168fd890a1ec78c5ececb34c6b1`;
stderr is empty. A strict JSON parse confirmed that stdout is exactly one
canonical object plus one final LF, with no leading or trailing prose.
The validator hard-codes historical base
`307c34d30fc3763c82a944a142ae922b48ff18aa` and tree
`ef45ba442c71959db78ad146a023bcf32946a53f`; the current worker base is the
one recorded above.

The contract makes every candidate scheduler-owned and immutable in a worker
handoff. A worker must not refresh, replace, rename, or delete it. Therefore
this worker cannot repair the base binding, cannot produce a passing semantic
replay, and cannot truthfully refresh `proof-receipt.json`. Because the proof
phase is not genuinely self-tested on this base, `.stage1-worker-selftest.json`
is deliberately absent.

## DAG and reuse boundary

The complete `parent_inspection_order`, direct hard-parent list, transitive
hard-ancestor list, hard-edge list, and reuse-hint list are empty. The empty
sequence is the complete closure, so there are no parent receipts,
declarations, or reusable bodies to inspect or consume.

The sole contextual relationship is the nonblocking weak shared-module group
`SHARED-MODULE-735a79718fe89f59`. The target-owned
`dependency-reuse-ledger.json` uses schema
`stage1-dependency-reuse-ledger/1.1`, records the exact current context IDs,
and rejects reuse from `THM-M-0118`: sharing
`Mathlib.CategoryTheory.Sites.SheafCohomology.Basic` is not a common lemma,
checked transport, or terminal proof body. No provider acceptance, receipt,
or checkbox state is inherited.

The current theorem-DAG projection content-binds the existing ledger and proof
artifacts. Refreshing the ledger alone would change those scheduler-owned
projection bindings while still leaving the immutable validator stale, so it
would not make the requested phase self-testable and is not performed.

## Proof boundary

The existing target-owned declaration

```text
Stage1Instances.THMM0110.Proof.kodairaVanishingTarget_of_vanishing
```

is a real, placeholder-free conditional assembly body. It consumes an
explicit premise proving the entire substantive vanishing statement and then
returns the exact frozen root. It does not construct that premise and cannot
close the assigned proof phase. The current `proof-receipt.json` remains
truthfully `accepted=false`, `verdict=blocked`, and
`root_kernel_closed=false`; no accepted obligation ID exists.

The exact root cut remains:

- `M0110-S-SEMANTIC`: connect the independent projective, canonical,
  dualizing, invertible, rank-one, ample, and tensor-product proposition
  fields to faithful native objects.
- `M0110-T-VANISHING`: prove positive-degree vanishing for the concrete
  `Sheaf.H` carrier for every frozen datum.

The pinned zero-sheaf and injective-Ext anchors require stronger premises that
the frozen hypotheses do not imply. No exact compatible terminal Kodaira body
exists in the inspected repository or pinned closure. Thus
`audit_complete=false` and `theorem_complete=false`; no M0, validation,
release, AUDIT-Z, THEOREM-Z, or master-acceptance claim is supported.

## Bounded checks

All commands ran in this worker clone on 2026-07-17 (Asia/Shanghai). No
`lake update`, `lake build`, dependency clone/fetch, network access, or `.lake`
mutation was performed. The automation-provided untracked `.lake` symlink was
observed and reused read-only only by the immutable validator before its base
check failed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structure, 1546-target manifest, v2 theorem DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10822 blueprint states, typed relationships, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and scheduler-owned validator rules passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered 1546-target L0/rework-required manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0110` | 0 | Rank 34 target remains planned, legacy evidence unaccepted, and theorem incomplete. |
| Candidate enumeration at both HEAD-declared proof paths | 0 | Exactly one candidate exists: the HEAD-tracked `check_proof.py`. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0110/check_proof.py` | 1 | Exact typed JSON result: `repair_required`; the validator's historical base binding differs from current HEAD. |
| `git diff --check -- Stage1_Instances/THM-M-0110 .stage1-worker-selftest.json` | 0 | No whitespace errors in the target-scoped handoff. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The failed proof replay emitted no false completion handoff. |

## Retry condition

The scheduler/master lane must publish a refreshed `check_proof.py` in an
authoritative integration commit and issue a fresh proof claim whose worker
base contains that exact unchanged blob. The refreshed validator must bind the
current graph digest, task state, target-owned artifacts, and receipt bytes and
must still report the substantive open proof boundary unless an exact
placeholder-free Kodaira body and checked native semantic/cohomology
transports have also been integrated. A fresh worker may then replay the
unchanged scheduler-selected argv and emit a self-test handoff only if the
typed result supports it.

This artifact is a scheduler-ownership blocker. It grants no item-state
transition, proof-phase acceptance, provider acceptance transfer, root proof
credit, audit completion, theorem completion, or master acceptance.
