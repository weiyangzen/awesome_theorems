---
name: execute-stage1-rev56
description: Execute, audit, validate, or release one of the 1546 covered Lean 4 theorem targets under the repository's Stage1 rev-5.6 assurance standard and v2 theorem-dependency/reuse overlay. Use when asked to expand a target such as THM-M-0387, create or improve its theorem dossier, inspect direct or transitive parent results, reuse accepted theorem or shared-lemma artifacts, implement proof obligations, run Lean validation, classify H/M/R debt, or decide audit/theorem completion without overstating machine closure.
metadata:
  short-description: Execute rev-5.6 Lean theorem dossiers
---

# Execute Stage1 rev-5.6

Operate one covered theorem as a fail-closed execution workflow. Never treat the generated target
list, source status, an existing `.lean` file, or prose as proof completion.

## Inputs

Require a theorem ID and infer one intent: `intake`, `audit`, `prove`, `validate`, or `release`.
Default to `audit` when the request asks to inspect status and to `prove` when it asks to complete or
improve proof work. Do not ask for information discoverable from the repository.

Read, in order:

1. `Docs/Stage1_Targets_rev-5.6.json` for membership, execution rank, lane, and the uniform L0 rework baseline.
2. `Docs/Stage1_Blueprint_v2.md` for global theorem ordering, dependency inspection, and reuse rules.
3. The target node in `Docs/Stage1_Theorem_DAG_v2.json`, including every direct parent and the complete transitive-ancestor closure.
4. The generated checklist in `Docs/Stage1_Blueprint_v2.md` for the current seven-phase dual-cursor
   state. It is the task-state SSOT; `Docs/Stage1_Execution_DAG_rev-5.6.json` is its read-only JSON
   projection.
5. `Docs/Stage1_Blueprint_rev-5.6.md` for normative assurance gates, especially sections 0, 3, 5-11, and 14.
6. `Docs/Blueprint_Guidelines.md` for repository publication and debt rules.
7. Existing theorem dossier, Lean modules, dependency pins, validation scripts, and dependency-reuse ledger for the target and its ancestors.
8. `THM-M-0387` only as a quality floor and conformance fixture, never as status to copy.

If the ID is absent from the 1546-target manifest, stop with `rejected`. Do not create a Stage1
dossier, slot, lane, or conformance claim for it.

The v2 overlay does not reset or manufacture progress. Preserve every existing rev-5.6 item state by
stable item ID. Never redo a current `[x]` phase; leave a current `[_]` phase for master review unless
an explicit invalidation receipt proves it stale. Resume at the first relevant `[ ]` phase. The
uniform `L0 / rework_required` rule applies to evidence predating the current rev-5.6 task state: a
legacy slot remains only a discovery hint and cannot confer elevated assurance, proof credit, or a
gate exemption.

## Phase 1: Preflight

Run:

```bash
python3 Docs/tools/check_stage1_standard.py
python3 Docs/tools/check_stage1_theorem_dag_v2.py
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
- target manifest, v2 theorem DAG, rev-5.6 task state, Markdown projection, or a standard validator disagrees;
- the target's declared ancestor closure cannot be reproduced from the typed v2 edges;
- source statement cannot be identified without inventing missing mathematics;
- another change makes scoped editing impossible without overwriting user work.

## Phase 2: Freeze The Target

Before proof search or implementation, create or verify the theorem intake record required by
section 5. Freeze the exact human claim, domains, universes, ordered binders, hypotheses, conclusion,
degenerate cases, foundation/TCB/computation profiles, Lean module and declaration/expression, and
environment fingerprint.

Elaborate the canonical Lean target. Add checked transports for alternate encodings. Mutation-test
removed hypotheses, changed domains, binder scope, and boundary cases. Do not inspect or credit proof
closure before the statement and eligibility registry are frozen.

If exact elaboration is not yet possible, keep `M3` or `M4`, record a concrete blocker, and continue
only with audit work that does not claim exact statement or proof closure.

## Phase 3: Audit Sources And Formal Candidates

Use primary mathematical sources for H status. Record edition, theorem/page, assumptions, errata,
and node crosswalk; a citation alone is not H0.

Search repo-local Lean, pinned mathlib, then credible external Lean 4 projects. For every candidate,
record exact module, declaration, type, revision, toolchain, dependency feasibility, placeholders,
axioms, unsafe/oracle boundaries, and terminal proof-body provenance.

Classify debt independently:

- `H0..H5`: human proof and source fidelity.
- `M0-L/M0-W/M0-P/M1..M5`: exact kernel closure and integration state.
- `R0..R4`: readable reconstruction and review state.

Never turn an anchor-only external theorem into M0. If an exact external closure exists, pin/import/
check it or report an explicit integration blocker.

## Phase 4: Freeze And Expand The Proof Architecture

Freeze the canonical obligation registry before observing closure metrics. Build separate typed
proof, refinement, provenance, evidence, trust, documentation, and workflow graphs. Every root-
relevant import, bridge, case split, construction invariant, computation, and source boundary must
own a stable obligation ID.

Expand until every semantic leaf has a substantive ledger and at most 100 proof steps. The number
100 is only a split threshold. A short invocation of a deep theorem remains a bridge obligation.
Require checked child-to-parent composition for every nonleaf. Deduplicate aliases, wrappers,
transports, and shared terminal bodies in all coverage metrics.

## Dependency Context And Reuse Gate

Before changing a `proof` phase, load the target's complete v2 dependency context. Traverse all
direct parents and transitive ancestors recorded in `Docs/Stage1_Theorem_DAG_v2.json`; do not stop at
the first layer or silently discard an unresolved parent. Inspect that exact closure in ascending
`v2_execution_rank`, so every provider is visited before any dependent descendant. Do not replace
this order with filesystem order, theorem ID order, or whichever parent is easiest. For each
ancestor inspect:

- its current seven rev-5.6 phase states and blockers;
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
Provider receipts must use the rev-5.6 node-receipt schema and bind item, base revision, inputs, and
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
compatibility work. A checked transport is consumer-owned proof work: it must content-bind the
provider source, bind both statement fingerprints, identify the target-owned import/wrapper, and
obtain the consumer's own validation receipt. Provider `[x]`, a provider receipt, or a passing
provider replay cannot substitute for any consumer binding. The ledger revision, current validation
receipt, and worker handoff packet must all bind the scheduler claim's base revision and exact
nonempty validation commands.
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
proof search but confers no accepted proof credit. Do not count an alias, wrapper, transport, or the
same terminal body twice. A parent blocker is informative unless an evidence-audited hard edge makes
the result logically necessary; hard dependencies gate master closure, while provisional worker
exploration may continue without claiming closure.

## Phase 5: Execute The Requested Intent

For `intake`, create only a valid `planned` instance and its open task DAG.

For `audit`, complete inventories and classifications without requiring proof closure. Audit may
reach `AUDIT-Z` with an open root and must then return `accepted_audit_only`.

For `prove`, first pass the dependency context and reuse gate, then select dependency-legal open
obligations from the frozen DAG. Prefer checked ancestor declarations and canonical shared terminal
bodies over duplicate proof work. Implement exact Lean proof bodies, checked wrappers, or pinned
external integration. Do not weaken the target. Run node-scoped exact-type, axiom, placeholder,
provenance, and composition checks after every material change. Split an obligation after five
unresolved execution ticks.

For `validate`, re-run recorded structured recipes against the claimed declarations. Do not add
proof content merely to make validation agree with an old status.

For `release`, require immutable clean input, cold empty-cache build, offline replay, SBOM/license
checks, deterministic evidence bundle, a second independent runner, and an independently implemented
minimal verifier. Decide `AUDIT-Z` and `THEOREM-Z` separately.

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

Batch execution is opt-in. Process targets by `v2_execution_rank`, which is a deterministic overlay;
never rewrite the retained rev-5.6 `execution_rank` or stable phase IDs. Saturate independent roots
and nonblocking branches, but keep master closure ordered by audited hard dependencies. A failure
blocks only hard dependents, not truthful auditing or provisional work on independent targets.
Within one claim frontier, use `(v2_execution_rank, phase_layer, phase_item_id)` exactly; do not let a
later theorem jump ahead because its phase is shallower or cheaper to launch.
Immutable accepted declarations and canonical shared lemma bodies may be reused, but every consumer
must own its import/transport/composition/validation receipt. Never share checkbox state, mutable
build output, or receipt identity between targets. Aggregate counts and JSON/todo state are derived
from the authoritative v2 checklist, never manually edited.
