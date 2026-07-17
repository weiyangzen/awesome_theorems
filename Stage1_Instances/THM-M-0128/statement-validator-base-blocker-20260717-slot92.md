# THM-M-0128 statement current-base blocker

## Scope

This is the target-scoped fail-closed result for
`S56-M-0128-STATEMENT` at worker base
`c09fec56b723330b06490622768353922c42475f` (tree
`0d742d5018bc3b55b0352c28cca02f5d961018fb`). It changes no Lean
source, phase receipt, dependency ledger, scheduler-owned validator, task-state
authority, theorem-DAG projection, lifecycle, debt vector, or item state.

The sole task-state authority records the assigned item as `[_]` with one
attempt. This run is therefore a current-base revalidation of unfinished worker
evidence, not a new `[ ] -> [_]` transition and not master acceptance. The
exact claim tuple is `(v2_execution_rank=280, phase_layer=1,
phase_item_id=S56-M-0128-STATEMENT)`.

## Dependency And Reuse Audit

The authoritative theorem DAG has SHA-256
`c5d478054cf32914251001d24d128b3b21ba29414965d64947d78768329660bd`.
The target dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The direct-parent, transitive-ancestor, hard-edge, reuse-hint, shared-group, and
`parent_inspection_order` lists are all empty. The complete ordered closure was
therefore traversed exactly once before any proof work by inspecting zero
providers. There are no parent phase states, receipts, declaration bodies,
reusable artifacts, imports, copies, or transports to inspect or consume. No
proof work was performed, no reuse was accepted, and no provider checkbox
state, acceptance, or proof credit was transferred. The empty graph context is
not a mathematical independence claim.

The tracked `dependency-reuse-ledger.json` has schema
`stage1-dependency-reuse-ledger/1.1` and truthful empty `inspections`,
`reuse_decisions`, and `unresolved_compatibility_obligations`. It is historical
anchor-audit evidence bound to repository revision
`74d4c272070069bc62df15798895293b4795940a`, graph digest
`cb4b83c4c4a5474fce51f98098f1421315fe7f1bd8cd52205932e57eced9f675`,
and phase layer 2, not this statement claim. Current-base ledger validation
fails closed with `dependency reuse ledger does not match the graph supplied
to its worker`.

The ledger is deliberately not refreshed in this blocked run. Its new bytes
would make the immutable scheduler-owned validator's hard-coded ledger hash
stale, while that validator is already hard-coded to an obsolete base, tree,
graph, statement packet, and handoff. A ledger-only rewrite cannot produce a
truthful receipt or self-test packet and would overwrite prior evidence
without repairing scheduler authority.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_current_base_binding_stale` is the first
worker gate that cannot be repaired within this assignment. The mandatory
HEAD phase contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`
and declares these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0128/check_statement.py`
- `Stage1_Instances/THM-M-0128/check_statement_artifacts.py`

Exactly one exists at the worker base: `check_statement.py`, SHA-256
`212251f3154a8b8ca6747e983655e279ca754e875de6e23cdca50aa644db42b1`,
Git blob `25b60d1e6f3216c53e5015d53eea953d9bcc0c79`. Its HEAD and
worktree bytes are identical, so candidate selection is unambiguous and the
candidate was not modified.

The immutable candidate hard-codes repository revision
`dae1951609072752d49d111bf00e78e4512f2d14`, tree
`9d8cc27cc0e09489c78b0bdbdeb57b15c5840f13`, theorem-DAG digest
`3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa`,
and the historical statement ledger and handoff. The current claim has a later
base and graph. The worker is expressly forbidden to refresh, replace, rename,
create, or delete a validator candidate.

The exact contract-selected command was run without shell interpolation:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0128/check_statement.py
```

It exited `1` and emitted exactly one JSON object on stdout:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"S01-ARTIFACTS.negative_evidence_validation","item_id":"S56-M-0128-STATEMENT","message":"theorem DAG changed","open_obligations":5,"phase":"statement","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0128","verdict":"repair_required"}
```

This typed negative result does not prove the phase predicate. It cannot
support a current-base phase receipt or worker self-test handoff. Creating the
handoff first would be circular because the unchanged validator requires the
historical receipt's exact old-base packet, and the graph and ledger checks
would still fail.

The topology gate is independently open for master acceptance:
`S56-M-0128-INTAKE` remains `[_]`, not `[x]`. Its state and receipts are
observation only and do not supply an accepted statement predecessor.

## Positive Statement Gate Remains Open

The tracked negative evidence still identifies only a CM-special-point family,
not one source-authorized proposition. No immutable admitted theorem passage
fixes the CM type and reflex construction, idelic quotient, arithmetic versus
geometric Artin normalization, canonical model and level, action variance,
equality notion, ordered binders, hypotheses, or boundary cases. Those choices
can narrow, broaden, or reverse the requested claim; choosing convenient ones
would substitute a different theorem.

The pinned environment exposes `NumberField.IsCMField` and
`NumberField.AdeleRing`. The unchanged `Statement.lean` has exactly those two
minimal substrate imports and deliberately declares no canonical proposition.
Its trust-zero elaboration succeeds, but that proves only the availability of
the substrate types. There is no canonical expression or environment
fingerprint, credited transport, canonical-target import-minimality result, or
meaningful removed-hypothesis, changed-domain, changed-binder-scope, or
boundary-case mutation. Thus `S02-EXACT-TARGET` and `S03-MUTATIONS` remain
open independently of validator freshness.

## Checks Run

All commands ran in this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided untracked `Formalizations/Lean/.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout,
network action, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Fifteen assurance groups, 1546 uniform-L0 targets, the v2 DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 blueprint states, typed relations, deterministic order, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and twenty-three source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered 1546-target L0/rework-required manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0128` | 0 | Rank 46, planned lifecycle, legacy artifacts unaccepted, theorem incomplete. |
| Declared candidate enumeration and HEAD/worktree blob comparison | 0 | Exactly one statement candidate exists and its bytes are unchanged. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0128/check_statement.py` | 1 | Exactly one typed `failed` / `repair_required` object reported `theorem DAG changed`; `phase_accepted=false`. |
| Current-base `validate_dependency_reuse_ledger(...)` | 1 | The historical ledger truthfully failed its stale graph/base binding. |
| From `Formalizations/Lean`: `env LEAN_NUM_THREADS=1 LC_ALL=C TZ=UTC timeout --foreground --kill-after=5s 300s lake env lean --trust=0 ../../Stage1_Instances/THM-M-0128/Statement.lean` | 0 | Both substrate anchors elaborated; no canonical target declaration was checked. |
| Prohibited-construct scan of `Statement.lean` | 1, expected no matches | No `sorry`, axiom, placeholder, unsafe, or native-oracle construct was present. |
| `git diff --check -- Stage1_Instances/THM-M-0128 .stage1-worker-selftest.json` | 0 | No whitespace errors in the target-scoped delta. |

The structural checks and narrow Lean elaboration do not override the
validator's semantic failure or the mathematical exact-target blocker.
Because this phase is not genuinely self-tested at the current base, this run
creates no replacement `stage1-node-receipt/1.0` and no root
`.stage1-worker-selftest.json`. The sole historical phase receipt remains
bound to its old claim and is not rewritten.

## Retry Condition And Status Boundary

The scheduler/master lane must commit a refreshed validator at exactly one
declared path and issue a fresh claim whose base already contains that
identical blob. The authority packet must coherently bind the current
base/tree, task state, graph, empty schema-1.1 statement ledger, selected role
artifacts, and exactly one phase receipt. A worker may emit
`.stage1-worker-selftest.json` only if the contract argv then proves the
positive phase predicate.

Positive statement acceptance separately requires intake master acceptance,
an independently approved immutable source theorem/page with incorporated
definitions, assumptions, corrections, errata, translation, and all
reciprocity/action conventions, plus a pinned concrete CM/reflex/Shimura object
model. Only then can a worker encode the exact target, minimize imports, bind
the elaborated expression and environment fingerprints, compile credited
transports, and execute all four mutation classes.

This artifact is a target-scoped scheduler-ownership and exact-statement
blocker only. It grants no state transition, phase acceptance, accepted
receipt, reuse, proof credit, audit completion, theorem completion, provider
acceptance, or master acceptance. The authoritative item remains unfinished
at `[_]`.

## Persisted-Goal Continuation Audit

The first automatic continuation re-read the same base/tree, `[_]` cursor with
one attempt, graph and contract digests, empty ordered parent closure, historical
ledger, and unique unchanged validator blob. The exact contract-selected replay
again exited `1` and emitted the same single typed `failed` /
`repair_required` result with message `theorem DAG changed` and
`phase_accepted=false`. No scheduler-owned validator/base repair or admitted
exact source statement has appeared. A lawful current-base receipt and worker
self-test handoff therefore remain impossible; `.stage1-worker-selftest.json`
is still intentionally absent.

The second automatic continuation performed the same audit against the same
immutable base and obtained the identical typed semantic failure. The
scheduler-owned validator/base mismatch has now repeated across the original
worker turn and two consecutive continuations. No worker-permitted edit can
repair it: changing the validator is forbidden, and changing only the ledger,
receipt, or packet cannot satisfy the validator's obsolete graph/base bindings.
The exact source-statement gate also remains independently open. This is an
external-state impasse rather than incomplete worker investigation.
