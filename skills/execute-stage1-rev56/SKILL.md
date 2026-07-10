---
name: execute-stage1-rev56
description: Execute, audit, validate, or release one of the 1546 covered Lean 4 theorem targets under the repository's Stage1 rev-5.6 assurance standard. Use when asked to expand a target such as THM-M-0387, create or improve its theorem dossier, implement proof obligations, run Lean validation, classify H/M/R debt, or decide audit/theorem completion without overstating machine closure.
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
2. `Docs/Stage1_Blueprint_rev-5.6.md` for normative gates, especially sections 0, 3, 5-11, and 14.
3. `Docs/Blueprint_Guidelines.md` for repository publication and debt rules.
4. Existing theorem dossier, Lean modules, dependency pins, and validation scripts for the target.
5. `THM-M-0387` only as a quality floor and conformance fixture, never as status to copy.

If the ID is absent from the 1546-target manifest, stop with `rejected`. Do not create a Stage1
dossier, slot, lane, or conformance claim for it.

Treat every covered target as `L0 / rework_required`, including targets with historical Stage1
files and `THM-M-0387`. A legacy slot is only a file-discovery hint. Re-audit any old artifact from
the exact statement gate onward; never inherit elevated assurance, accepted state, proof credit, or
a gate exemption.

## Phase 1: Preflight

Run:

```bash
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show <THEOREM-ID>
git status --short
```

Confirm the target-set digest and ordered manifest pass. Inspect the worktree and preserve unrelated
changes. Identify the target's existing files and validation surface. Record the base commit and,
for a dirty tree, the relevant diff/untracked hashes; a dirty run is nonrelease evidence.

Hard stop conditions:

- target is outside the manifest;
- target manifest, Markdown projection, or standard validator disagrees;
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

## Phase 5: Execute The Requested Intent

For `intake`, create only a valid `planned` instance and its open task DAG.

For `audit`, complete inventories and classifications without requiring proof closure. Audit may
reach `AUDIT-Z` with an open root and must then return `accepted_audit_only`.

For `prove`, select dependency-legal open obligations from the frozen DAG. Implement exact Lean
proof bodies, checked wrappers, or pinned external integration. Do not weaken the target. Run
node-scoped exact-type, axiom, placeholder, provenance, and composition checks after every material
change. Split an obligation after five unresolved execution ticks.

For `validate`, re-run recorded structured recipes against the claimed declarations. Do not add
proof content merely to make validation agree with an old status.

For `release`, require immutable clean input, cold empty-cache build, offline replay, SBOM/license
checks, deterministic evidence bundle, a second independent runner, and an independently implemented
minimal verifier. Decide `AUDIT-Z` and `THEOREM-Z` separately.

## Phase 6: Reconcile Public State

Treat structured instance/state/evidence files as authority. Generate or reconcile README, metadata,
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
first_failed_gate
remaining_root_cut_set
status_boundary
```

Use `accepted` only for the exact requested state transition supported by accepted receipts. Use
`no_state_change` when checks pass but no authoritative state changes. Use `blocked` for an honest,
actionable gate failure. Never report theorem completion unless the exact root is M0, composition,
trust, source, readability, hermetic, freshness, and independent-verification gates all pass.

## Batch Mode

Batch execution is opt-in. Process targets in manifest execution order with isolated per-target
state and receipts. A failure blocks only dependent work for that theorem, not truthful auditing of
later independent targets. Never share proof credit, status, mutable build output, or evidence IDs
between targets. Aggregate counts are derived from accepted per-target state, never manually edited.
