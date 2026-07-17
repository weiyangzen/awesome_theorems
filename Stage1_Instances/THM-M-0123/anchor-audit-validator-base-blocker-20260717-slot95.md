# THM-M-0123 anchor-audit validator-base blocker

## Scope

This is the target-scoped fail-closed result for
`S56-M-0123-ANCHOR_AUDIT` at worker base
`db2e21b8fec263c5b65014acb1ee2039566e35a3` (tree
`815414c57391f2c12871c05a6e3d2944b0f2fef2`). It changes no Lean source,
prior phase receipt, task-state authority, theorem-DAG projection, lifecycle,
debt vector, item state, or scheduler-owned validator candidate.

The sole task-state authority records the item as `[_]` with one attempt, so
this run is a current-base revalidation of unfinished worker evidence, not a
new `[ ] -> [_]` transition and not master acceptance. The exact claim tuple is
`(v2_execution_rank=276, phase_layer=2,
phase_item_id=S56-M-0123-ANCHOR_AUDIT)`. The current theorem-DAG SHA-256 is
`91ea782c662e40b9608f8900ad586114c5ef8e8e5d2d2f13316185bd8f205067`;
the target dependency-context SHA-256 is
`0c0f6d1bed857aeaad7b4656db6ae6fe5c9c6bde39f7c9fb9ec2f8938eb4a484`.

## Dependency And Reuse Audit

The authoritative `parent_inspection_order`, direct-hard-parent,
transitive-hard-ancestor, hard-edge, and reuse-hint lists are empty. The
complete hard-parent closure was therefore traversed exactly once, in the
supplied empty order, before any proof work. There were zero parent phase
states, receipts, declaration bodies, or reusable artifacts to inspect. No
proof work was performed, and no parent checkbox, receipt, body, acceptance,
or proof credit was consumed or transferred.

The graph does declare the nonblocking weak group
`SHARED-MODULE-dff4d00d3b45e946`, whose only other member is
`THM-M-0122`. The current `THM-M-0122` node was inspected together with its
tracked anchor inventory and immutable public-source snapshot. Its phase
states are intake/statement/anchor-audit/obligation-tree/proof `[_]`, then
validation/release `[ ]`; those marks are observations only. The shared
identity is merely the co-mentioned module
`Atlas.ArithmeticGeometry.code.FaltingsTheorem`. The recorded Atlas source at
revision `34ffed396f376454c1a9b297f3fd74c5c801fb50` has a Q-only custom curve
statement, a free `Nat` genus, no checked transport to the target's
all-number-field scheme/cohomology statement, and a terminal `by sorry` body.
It is not a common lemma or valid proof body. No import, copy, transport,
consumer validation receipt, or provider acceptance is reused.

The tracked target ledger uses
`stage1-dependency-reuse-ledger/1.1`, but it is historical worker evidence:
it binds repository revision `307c34d30fc3763c82a944a142ae922b48ff18aa`,
graph digest `8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`,
context digest `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`,
and an empty shared-group list. It cannot support a current-base handoff. It is
deliberately not refreshed in this blocked run: changing target evidence
cannot repair the immutable validator, and no current receipt or self-test
packet may truthfully cite a failed semantic replay. A future eligible run must
refresh it with the current graph/context, the shared-group decision above,
empty `inspections`, and truthful `unresolved_compatibility_obligations`.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_base_binding_stale` is the first worker gate
that cannot be repaired within this assignment. The mandatory HEAD phase
contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`
and declares these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0123/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0123/check_anchor.py`

Exactly one exists at the worker base: `check_anchor_audit.py`, with SHA-256
`6166d1c2d444d4523ca76551c35f43807d6ce7d4b92411b0f3a4fd7e4a7c62dd`
and Git blob `67ed038b2fd206f92705cef5b7846780059d03de`. Its HEAD and
worker-base bytes are identical, so selection is unambiguous. The worker did
not create, edit, refresh, rename, replace, or delete either candidate.

However, the immutable candidate hard-codes the obsolete repository revision
`307c34d30fc3763c82a944a142ae922b48ff18aa`, tree
`ef45ba442c71959db78ad146a023bcf32946a53f`, theorem-DAG digest
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`,
context digest `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`,
and the former `[ ]`/zero-attempt anchor state with no shared group. The
current authority correctly records `[_]`, one attempt, and the shared group
above.

The exact contract-selected argv was run without shell interpolation:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0123/check_anchor_audit.py
```

It exited `1` and emitted exactly one JSON object on stdout:

```json
{"audit_complete": false, "blocked": false, "first_failed_gate": "ANCHOR-AUDIT-SEMANTIC-CHECK", "item_id": "S56-M-0123-ANCHOR_AUDIT", "message": "repository revision drift", "open_obligations": 1, "phase": "anchor_audit", "phase_accepted": false, "phase_predicate_proven": false, "schema_version": "stage1-validator-semantic-result/1.0", "stale_inputs": [], "status": "failed", "theorem_complete": false, "theorem_id": "THM-M-0123", "verdict": "repair_required"}
```

This typed negative result cannot prove the phase predicate. Exit zero from a
different check cannot override `phase_accepted=false`. Because every declared
candidate is scheduler-owned and immutable to workers, this run cannot produce
a truthful new `stage1-node-receipt/1.0` or self-test handoff. The existing
tracked receipt remains historical observation bound to the old base; it is
not refreshed, replaced, or presented as current evidence.

`G02-TOPOLOGY` is independently open for master acceptance:
`S56-M-0123-STATEMENT` is still `[_]`, not `[x]`. That does not prevent a
bounded audit, but it prevents dependency-ordered master closure and transfers
no statement acceptance.

## Existing Audit Boundary

The historical inventory remains useful discovery guidance. It records all
seven prescribed lanes and classifies ten candidates at immutable local or
external revisions, while expressly declining discovery saturation. Its
mathematical boundary remains unchanged:

- the exact repo-local target is statement-only;
- pinned mathlib supplies scheme/cohomology, Northcott, and descent substrate,
  but no terminal Mordell/Faltings declaration;
- the Atlas declaration is materially mismatched and directly uses `sorry`;
- public discovery was bounded, and an anonymous code-search access failure is
  not a global negative result; and
- the primary-source wording, conventions, corrections, derivation, and
  independent H review remain open.

The root therefore remains `H4/M3/R3`. This run grants no `H0`, `M0`, `M1`,
`R0`, accepted reuse, proof credit, discovery-saturation claim, `AUDIT-Z`,
`THEOREM-Z`, phase acceptance, or master acceptance.

## Checks Run

All commands ran in this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided `.lake` symlink was reused read-only; no `lake update`,
`lake build`, dependency clone/fetch, checkout, or cache mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structure, 1546-target manifest, v2 DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 phase states, typed relationships, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and scheduler-owned validator rules passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered 1546-target `L0/rework_required` manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0123` | 0 | Rank 42, planned lifecycle, legacy artifacts unaccepted, theorem incomplete. |
| declared candidate enumeration and HEAD/base blob comparison | 0 | Exactly one declared candidate exists and is unchanged at this worker base. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0123/check_anchor_audit.py` | 1 | One typed semantic JSON object reported `repair_required` because of repository revision drift. |
| `LC_ALL=C TZ=UTC LEAN_NUM_THREADS=1 lake env lean --trust=0 ../../Stage1_Instances/THM-M-0123/Statement.lean` from `Formalizations/Lean` | 0 | The exact statement, checked transports, axiom observations, and four expected negative mutation probes elaborated. |
| `LC_ALL=C TZ=UTC LEAN_NUM_THREADS=1 lake env lean --trust=0 ../../Stage1_Instances/THM-M-0123/AnchorAudit.lean` from `Formalizations/Lean` | 0 | The pinned support declarations elaborated; the Northcott wrapper reported no axioms. |
| `git diff --check -- Stage1_Instances/THM-M-0123 .stage1-worker-selftest.json` | 0 | No whitespace errors were found before this blocker was added. |

Structural checks and Lean elaboration do not override the validator's typed
negative result. Because this phase is not genuinely self-tested at the
current base, this run emits no `.stage1-worker-selftest.json`.

## Retry Condition And Status Boundary

The scheduler/master lane must commit a refreshed validator at exactly one
declared candidate path, then issue a fresh claim whose worker base contains
that identical blob. The validator must bind the fresh base, current graph and
context digests, current `[_]` task state, current target evidence, and the weak
shared-group decision. A fresh worker can then refresh the target ledger and
receipt and may write the self-test handoff only if the unchanged selected argv
emits a typed positive semantic result. Master acceptance additionally requires
the statement predecessor `[x]`, authority-owned artifact-role mapping, final
HEAD SHA-256/Git-blob bindings, independent review, replay, and SSOT CAS.

This artifact is a target-scoped scheduler-ownership blocker only. It grants
no state transition, phase acceptance, provider acceptance transfer, proof
credit, audit completion, theorem completion, or master acceptance.
