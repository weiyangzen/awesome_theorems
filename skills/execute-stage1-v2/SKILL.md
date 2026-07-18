---
name: execute-stage1-v2
description: Locate, pin, match, import, replay, validate, and organize an exact existing machine proof under the sole Stage1 v2 blueprint. Use for targets with a complete human proof and exact external or pinned kernel proof that this repository has not accepted, or for a scheduler-owned independently reviewed bounded frontier exception with completion probability at least 0.70.
metadata:
  short-description: Integrate existing machine proofs
---

# Execute Stage1 v2 Integration

Operate one covered theorem as a fail-closed integration workflow. The default job is not to invent
a new proof. Locate, content-bind, match, import, replay, validate, and organize a machine proof that
already exists outside this repository's accepted closure. Never treat the generated target list,
source status, an existing `.lean` file, or prose as proof completion.

## Inputs

Require a theorem ID and infer one intent: `intake`, `audit`, `integrate`, `frontier_prove`,
`validate`, or `release`. Default to `audit` when the request asks to inspect status and to
`integrate` when it asks to complete or improve ordinary proof-phase work. Never infer
`frontier_prove` from the user's wording alone: that intent is available only when the current
receipt has disposition `frontier_exception` and its reviewed lease and limits remain active. Do not
ask for information discoverable from the repository.

Read, in order:

1. `Docs/Stage1_Blueprint_v2.md` for the sole current requirements, global theorem ordering,
   focus policy, dependency inspection, reuse rules, and task state.
2. The target's `focus_eligibility` projection in `Docs/Stage1_Theorem_DAG_v2.json` and its
   content-bound `Stage1_Instances/<THEOREM-ID>/focus-eligibility.json` receipt when present.
3. `Docs/Stage1_Target_Membership_v2.json` as a read-only membership projection. Its discovery labels do
   not authorize proof-frontier work or determine current scheduling.
4. The target node in `Docs/Stage1_Theorem_DAG_v2.json`, including every direct parent and the complete transitive-ancestor closure.
5. The generated checklist in `Docs/Stage1_Blueprint_v2.md` for the current seven-phase dual-cursor
   state. It is the requirements and task-state SSOT; `Docs/Stage1_Phase_DAG_v2.json` is its
   read-only JSON projection.
6. `Docs/Stage1_Focus_Eligibility_Schema.json` and `scripts/stage1_focus_eligibility.py` for receipt
   syntax and fail-closed phase permission checks.
7. Existing theorem dossier, formal-system sources, dependency pins, validation scripts, and
   dependency-reuse ledger for the target and its ancestors.

Superseded assurance material exists only in Git history. Do not restore or read it during current
execution. Only requirements stated in the v2 blueprint and enforced by a current v2 validator apply.

If the ID is absent from the 1546-target manifest, stop with `rejected`. Do not create a Stage1
dossier, slot, lane, or conformance claim for it.

Before executing a phase, run the focus validator for that exact phase. A missing receipt projects to
`research_required` and may authorize only bounded intake, statement, and anchor research; a present
but malformed, stale, or expired receipt authorizes no phase until repaired. `obligation_tree`, `proof`,
`validation`, and `release` require a fresh valid receipt whose disposition is
`organize_or_integrate` or `frontier_exception`. A frontier exception is valid only when a
scheduler-owned estimator assigns probability `>= 0.70`, an independent reviewer approves it, and
the receipt declares a positive budget and stop conditions. Worker self-assessment never authorizes
the exception.

The v2 overlay does not reset or manufacture progress. Preserve every current v2 checklist state by
its stable `S56-*` item ID. Never redo a current `[x]` phase; leave a current `[_]` phase for master
review unless an explicit invalidation receipt proves it stale. Resume at the first relevant `[ ]`
phase. The uniform `L0 / rework_required` rule applies to evidence predating the migrated v2 cursor: a
legacy slot remains only a discovery hint and cannot confer elevated assurance, proof credit, or a
gate exemption.

## Phase 1: Preflight

Run:

```bash
python3 Docs/tools/check_stage1_standard.py
python3 Docs/tools/check_stage1_theorem_dag_v2.py
python3 scripts/stage1_focus_eligibility.py <THEOREM-ID> --phase <PHASE>
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show <THEOREM-ID>
git status --short
```

Confirm the target-set digest, v2 graph coverage/acyclicity, state-preservation digest, and ordered
manifest pass. Inspect the worktree and preserve unrelated changes. Identify the target's existing
files and validation surface. Record the base commit and, for a dirty tree, the relevant
diff/untracked hashes; a dirty run is nonrelease evidence.

Hard stop conditions:

- target is outside the manifest;
- frozen target manifest, v2 theorem DAG, v2 checklist state, read-only projection, or a current v2 validator disagrees;
- the target's declared ancestor closure cannot be reproduced from the typed v2 edges;
- source statement cannot be identified without inventing missing mathematics;
- another change makes scoped editing impossible without overwriting user work.
- the current focus projection denies the requested phase;
- ordinary integration discovers that the purported exact machine proof is partial, mismatched,
  placeholder-bearing, unreplayable, or requires substantive new root-proof mathematics.

## Phase 2: Freeze The Target

Before candidate inspection or integration planning, create or verify the theorem intake record
required by the v2 blueprint and current v2 phase contract. Freeze the exact human claim,
domains, universes, ordered binders, hypotheses, conclusion,
degenerate cases, foundation/TCB/computation profiles, Lean module and declaration/expression, and
environment fingerprint.

Elaborate the canonical Lean target. Add checked transports for alternate encodings. Mutation-test
removed hypotheses, changed domains, binder scope, and boundary cases. Do not inspect or credit proof
closure before the statement and eligibility registry are frozen.

If exact elaboration is not yet possible, keep `M3` or `M4`, record a concrete blocker, and continue
only with audit work that does not claim exact statement or proof closure.

A missing eligibility receipt has disposition `research_required`: only `intake`, `statement`, and
`anchor_audit` are permitted until independently reviewed evidence changes that classification.

## Phase 3: Audit Sources And Formal Candidates

Use primary mathematical sources for H status. Record edition, theorem/page, assumptions, errata,
and node crosswalk; a citation alone is not H0.

Search repo-local Lean, pinned mathlib, then credible external Lean 4 projects. For every candidate,
record exact module, declaration, type, revision, toolchain, dependency feasibility, placeholders,
axioms, unsafe/oracle boundaries, and terminal proof-body provenance.

The audit's primary question is whether the exact machine proof already exists. Search, in order,
the accepted local closure, pinned dependencies, established formalization projects in their native
provers, and immutable external revisions. A negative result means only "no usable artifact located
as of the recorded date and query set". It never establishes global nonexistence.

Classify debt independently:

- `H0..H5`: human proof and source fidelity.
- `M0-L/M0-W/M0-P/M1..M5`: exact kernel closure and integration state.
- `R0..R4`: readable reconstruction and review state.

Never turn an anchor-only external theorem into machine closure. If an exact external closure exists,
pin/import/check it or report an explicit integration blocker. If none is content-bound, stop after
research unless the scheduler has issued a valid independently reviewed frontier exception.

## Phase 4: Freeze The Integration Architecture

This phase is forbidden without focus eligibility. For admitted integration work, freeze the exact
source-to-target match, dependency pin, import or checked transport, terminal body provenance,
kernel replay, trust/placeholder audit, compatibility work, license boundary, and acceptance plan.
Every root-relevant import, bridge, computation, and source boundary owns a stable obligation ID.

Do not expand a new proof tree merely because the old checklist contains an open proof phase. For an
ordinary admission, the terminal proof body already exists and the remaining tree describes only
integration and acceptance work. A frontier exception may expand proof obligations only within its
declared budget and must stop at the receipt's stop conditions.

## Dependency Context And Reuse Gate

Before changing a `proof` phase, load the target's complete v2 dependency context. Traverse all
direct parents and transitive ancestors recorded in `Docs/Stage1_Theorem_DAG_v2.json`; do not stop at
the first layer or silently discard an unresolved parent. Inspect that exact closure in ascending
`v2_execution_rank`, so every provider is visited before any dependent descendant. Do not replace
this order with filesystem order, theorem ID order, or whichever parent is easiest. For each
ancestor inspect:

- its current seven v2 checklist phase states and blockers;
- exact statement/declaration types and checked transports;
- obligation registry and typed proof, composition, provenance, trust, and workflow graphs;
- proof, validation, and release receipts, including revisions and content digests;
- terminal proof-body identity, reusable Lean declarations/modules, axiom/TCB boundary, and status.

Create or refresh `Stage1_Instances/<THEOREM-ID>/dependency-reuse-ledger.json` before proof edits.
Use schema `stage1-dependency-reuse-ledger/1.1`. The ledger must identify the observed v2 graph
digest, the target node's stable `dependency_context_sha256`, and repository revision; list the exact
`direct_parent_ids`, `transitive_ancestor_ids`, `hard_edge_ids`, `reuse_hint_ids`, and
`shared_group_ids`; include one inspection for every hard parent/ancestor with phase states, artifact
digests, and compatibility; include one reuse decision for every edge, hint, and shared group; and
record every unresolved compatibility obligation. A target with no known context still records an
empty, successfully inspected closure. Never satisfy this gate with only theorem names, categories,
source status prose, or a copied parent summary.

Every provider or consumer receipt reference is an object with `path`, `receipt_id`, and `sha256`,
not a bare identifier. The path must remain under the referenced theorem's owned directory and the
receipt JSON must agree on identity, owner, phase, acceptance, and exact bytes. During `proof`, record
the complete inspection and decision without fabricating a future consumer-validation receipt.
Record the provider's current authoritative proof mark as `provider_proof_state`; it must agree with
the inspection and never transfers checkbox credit. Do not impose blanket provider `[x]`: follow the
hard edge's exact artifact/import/hash and consumer-replay `state_semantics`.
Provider and ancestor evidence must match the authoritative checkout byte-for-byte; a worker-local
rewrite outside the assigned consumer path is invalid. A provisional consumer validation receipt
must set `selftest_status: passed` and record `selftest_result.exit_code: 0` plus a nonempty exact
`selftest_result.commands` list; missing or prose-only success claims do not pass. Those commands
must each match a successful command record in the worker handoff packet and the committed,
authority-bound validation specification. The integration lane replays that authoritative recipe
before merge; a worker-created or worker-modified validator cannot satisfy the gate.
Every phase-validator candidate declared by
`Docs/Stage1_Phase_Acceptance_Contracts.json` is scheduler-owned and immutable in
worker handoffs. Workers use the unique candidate already present at their HEAD;
they never create, refresh, rename, replace, or delete a candidate. A missing or
ambiguous candidate is a scheduler-ownership blocker, not permission for a worker
to manufacture one.
Provider receipts must use the retained `stage1-node-receipt/1.0` schema and bind item, base revision, inputs, and
successful accepted or normalized worker-self-tested evidence.
During `validation`, refresh the ledger and attach the target-owned, content-bound self-test receipt
for every accepted hard-edge reuse; it is still provisional while that phase advances to `[_]`.
During `release`, the referenced validation receipt and authoritative validation phase must be
master accepted `[x]`; blocked, stale, or cross-target receipts fail closed.
The detailed obligation/body/fingerprint/import fields are mandatory for accepted reuse and for a
material candidate comparison. A weak shared-group decision recorded as `not_applicable` instead
names an actual inspected member theorem, the current context digest, and a non-reuse reason; do not
fabricate declaration identities or fingerprints for a mere module co-mention.
`reused_exact` requires exact inspection/relationship, equal 64-hex statement fingerprints, and no
unresolved compatibility work. `reused_with_transport` requires checked-transport
inspection/relationship, explicit 64-hex fingerprints, the consumer wrapper, and no unresolved
compatibility work. A checked transport is consumer-owned integration work: it must content-bind the
provider source, bind both statement fingerprints, identify and replay the target-owned
import/wrapper, and record no unresolved compatibility obligation. During `proof`, the ledger must
not invent a future consumer-validation receipt. That receipt becomes mandatory only at
`validation`, where the ledger, receipt, and worker handoff packet must bind the scheduler claim's
base revision and exact nonempty validation commands. Provider `[x]`, a provider receipt, or a
passing provider replay cannot substitute for any consumer binding.
Bind `terminal_proof_body_id` through `provider_body_source: {path, sha256}` and bind
`consumer_import_or_wrapper` through `consumer_import_source: {path, sha256}`. Each declaration must
actually occur in that owner-scoped Lean source and the source must match the authoritative checkout.
For accepted hard-edge reuse, both references and declarations must also be exact entries in that
edge's `material_contract` allowlists. Same-owner but unlisted Lean material is not evidence: proof
edges must use the cross-target import plus proof-receipt input binding, while artifact edges must use
provider bytes derived from `source_path_sha256` and the admitted consumer adapter/replay path. Do not
apply this hard-edge-only restriction to nonblocking hints or weak shared groups.
Accepted reuse also requires a successful accepted or normalized worker-self-tested provider receipt;
an explicitly blocked provider receipt is not reuse evidence.

Only a declaration backed by current accepted evidence and an exact or independently checked
transport may discharge a child obligation. A `[_]` parent or nonblocking `reuse_hint` may guide
candidate inspection or an admitted bounded frontier attempt but confers no accepted proof credit.
Do not count an alias, wrapper, transport, or the
same terminal body twice. A parent blocker is informative unless an evidence-audited hard edge makes
the result logically necessary; hard dependencies gate master closure, while provisional worker
exploration may continue without claiming closure.

## Phase 5: Execute The Requested Intent

For `intake`, create only a valid `planned` instance and its open task DAG.

For `audit`, complete inventories and classifications without requiring proof closure. Audit may
reach `AUDIT-Z` with an open root and must then return `accepted_audit_only`.

For `integrate`, first pass focus eligibility, dependency context, and reuse gates. Perform only the
import, pin, wrapper/transport, replay, provenance, trust, license, documentation, and acceptance
work required to integrate an already existing exact proof. Do not invent a replacement proof, even
when the target separately has a frontier admission.

For `frontier_prove`, require the current disposition to be `frontier_exception`, then recheck its
assigned worker, lease, attempt and resource limits, milestones, validator, and stop conditions.
Implement new root-proof content only inside those reviewed bounds. A missing, revoked, stale,
expired, or exhausted exception rejects this intent rather than falling back to ordinary
`integrate`. Do not weaken the target.

For `validate`, re-run recorded structured recipes against the claimed declarations. Do not add
proof content merely to make validation agree with an old status.

For `release`, require immutable clean input, cold empty-cache build, offline replay, SBOM/license
checks, deterministic evidence bundle, a second independent runner, and an independently implemented
minimal verifier. Decide `AUDIT-Z` and `THEOREM-Z` separately. An `accepted_audit_only` result records
`AUDIT-Z` evidence but cannot close RELEASE or advance its checklist row to `[x]`; positive release
requires `accepted` with `theorem_complete=true`.

## Phase 6: Reconcile Public State

Treat the v2 blueprint checklist plus structured instance/evidence files as authority. Generate or reconcile README, metadata,
proof outline, machine audit, process audit, readable reconstruction, and build record from accepted
state. Never edit generated target lists manually. Never expose private runtime ledgers or absolute
machine paths in public artifacts.

Only the integration lane may promote provisional `[_]` work to accepted `[x]`. A worker report,
docs-only change, passing unrelated build, or source label such as `已验证` cannot promote state.

## Phase 7: Validate And Report

Always run the structural validator and the narrowest relevant Lean checks. For a release candidate,
run every recorded recipe and the full hermetic protocol. Run `git diff --check` on touched files.

Return a structured summary with:

```text
theorem_id
intent
verdict: accepted | accepted_audit_only | no_state_change | blocked | rejected
lifecycle_before -> lifecycle_after
root_vector_before -> root_vector_after
audit_complete: true | false
theorem_complete: true | false
changed_paths
commands_and_exit_codes
accepted_receipt_ids
dependency_reuse_ledger
inspected_parent_ids
reused_declaration_ids
first_failed_gate
remaining_root_cut_set
status_boundary
```

Use `accepted` only for the exact requested state transition supported by accepted receipts. Use
`no_state_change` when checks pass but no authoritative state changes. Use `blocked` for an honest,
actionable gate failure. Never report theorem completion unless the exact root is M0, composition,
trust, source, readability, hermetic, freshness, and independent-verification gates all pass.

## Batch Mode

Batch execution is opt-in. Process only focus-permitted phases by `v2_execution_rank`, which is a deterministic overlay;
never rewrite the retained original discovery rank or stable phase IDs. Saturate independent roots
and nonblocking branches, but keep master closure ordered by audited hard dependencies. A failure
blocks only hard dependents, not truthful auditing or provisional work on independent targets.
Within one claim frontier, use `(v2_execution_rank, phase_layer, phase_item_id)` exactly; do not let a
later theorem jump ahead because its phase is shallower or cheaper to launch.
The old manifest `target_lane` values are inert historical metadata. They never override the focus
receipt or revive a `frontier_deep_formalization_debt` lane.
Immutable accepted declarations and canonical shared lemma bodies may be reused, but every consumer
must own its import/transport/composition/validation receipt. Never share checkbox state, mutable
build output, or receipt identity between targets. Aggregate counts and JSON/todo state are derived
from the authoritative v2 checklist, never manually edited.
