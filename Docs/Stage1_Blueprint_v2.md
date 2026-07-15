# Stage1 v2 Theorem Dependency and Reuse Blueprint

> Document type: global orchestration overlay
> Version: `stage1-orchestration/2.0`
> Assurance authority: `Docs/Stage1_Blueprint_rev-5.6.md`
> Target authority: `Docs/Stage1_Targets_rev-5.6.json`
> Phase-state authority: `Docs/Stage1_Execution_DAG_rev-5.6.json`
> Theorem-DAG projection: `Docs/Stage1_Theorem_DAG_v2.json`
> Structural validator: `Docs/tools/check_stage1_theorem_dag_v2.py`
> Covered target set: exactly `1546` theorem IDs
> Canonical target-ID digest: `e07deabaab3463cc1f92cdf5c0cf50ad9f8270d35554529c375d20a8512d8f1a`

## 0. Purpose and Non-Goals

This blueprint adds a repository-wide theorem dependency and reuse order over the existing Stage1
rev-5.6 work. It has three purposes:

1. represent every one of the `1546` covered theorems exactly once in a typed theorem DAG;
2. schedule proved parent results and reusable lemma bodies before consumers while keeping unrelated
   or merely hinted work parallelizable; and
3. require every new pure proof run to inspect its complete direct and transitive parent context
   before implementing another proof of material that is already available.

This is an orchestration overlay, not a replacement assurance standard and not a second task-state
database. It does not weaken, duplicate, or relabel rev-5.6 evidence. In particular, v2:

- does not copy the 2.9 MB generated `1546 x 7` checklist into this file;
- does not create a second set of phase item IDs or a second execution-state cursor;
- does not turn a theorem name, topic similarity, citation, or historical source status into a proof
  dependency or machine-checked result;
- does not promote an existing `[ ]` or `[_]` item merely because its theorem moved earlier; and
- does not require work already represented by valid current evidence to be repeated.

The complete graph is the JSON projection named above. Diagrams and summaries in Markdown are only
readable views; they never override the structured authorities.

## 1. Authority and Compatibility

Authority remains deliberately separated:

| Concern | Authority | v2 rule |
|---|---|---|
| theorem assurance, H/M/R debt, exact statement, trust, receipts, `AUDIT-Z`, `THEOREM-Z` | `Docs/Stage1_Blueprint_rev-5.6.md` | unchanged |
| membership and original execution rank | `Docs/Stage1_Targets_rev-5.6.json` | all 1546 IDs and the digest are preserved |
| seven phase items and `[ ]` / `[_]` / `[x]` state | `Docs/Stage1_Execution_DAG_rev-5.6.json` | unchanged and snapshotted, never inferred from v2 order |
| cross-theorem order and reusable-context discovery | `Docs/Stage1_Theorem_DAG_v2.json` | new v2 projection |
| per-theorem scope and obligations | versioned theorem instance artifacts | unchanged |
| validation claims | content-addressed receipts and accepted evidence packets | unchanged |

`Docs/Stage1_Blueprint.md` remains a legacy generated 300-slot discovery queue. It is neither the v2
order nor live state. `Docs/Stage1_Blueprint_Applicable_Theorems.md` remains a readable target-set
projection. The other 55 Stage0 mathematical records remain outside this blueprint.

The repository skill at `skills/execute-stage1-rev56/SKILL.md` remains the compatible theorem
executor. It MUST continue to enforce rev-5.6 assurance and MUST use this v2 overlay only for parent
inspection, context reuse, and scheduling. The execution cron may treat this file as its single
global orchestration blueprint, but the structured rev-5.6 DAG remains the only phase-state
authority. There is no independently editable Markdown checklist in v2.

## 2. Migration Without Rework

The v2 migration is deterministic and state-preserving.

1. Import all and only the theorem IDs from `Docs/Stage1_Targets_rev-5.6.json`.
2. Import every theorem's seven phase states from `Docs/Stage1_Execution_DAG_rev-5.6.json` by the
   existing stable phase item ID.
3. Preserve each original execution rank as `original_execution_rank`.
4. Inventory existing dossiers, Lean declarations, obligation IDs, terminal proof-body identities,
   receipts, source crosswalks, blockers, and public artifacts without changing acceptance.
5. Derive a theorem completion bucket from the seven authoritative marks.
6. Add typed dependency and reuse records with evidence and explicit boundaries.
7. Compute the v2 topological order. Reordering changes only scheduling metadata.
8. Record the imported state digest in `legacy_state_snapshot` so regeneration cannot silently
   reset, upgrade, or lose work.

Existing work is handled as follows:

- `[x]` remains master accepted and is never reissued unless rev-5.6 invalidation or revocation
  evidence explicitly reopens it.
- `[_]` remains worker self-tested and goes to the master integration frontier, not back to the
  worker claim frontier.
- `[ ]` remains unfinished and may be claimed when its phase and theorem dependencies permit.
- Existing artifacts remain evidence candidates at their current strength. Reindexing an artifact
  into `evidence_inventory` or `reusable_artifacts` does not strengthen it.
- A changed path, rank, graph layer, or inferred relationship is not a reason to rerun a phase whose
  accepted receipt still binds the exact current inputs.
- Ambiguous legacy data is recorded as `needs_review`; migration never manufactures acceptance.

The theorem-level buckets use this closed vocabulary:

| Bucket | Exact meaning |
|---|---|
| `master_complete` | all seven authoritative phase items are `[x]` |
| `fully_self_tested` | all seven authoritative phase items are `[_]` |
| `partial` | at least one phase is started, but neither complete condition above holds |
| `unstarted` | all seven authoritative phase items are `[ ]` |

These are scheduling summaries only. Even `master_complete` does not replace the rev-5.6 terminal
receipt and `THEOREM-Z` decision from which the marks must have been accepted.

## 3. Theorem DAG Contract

`Docs/Stage1_Theorem_DAG_v2.json` uses schema `stage1-theorem-dag/2.0`. Its top-level record includes:

```text
schema_version
generated_by
requirements_source
target_manifest
legacy_execution_dag
target_id_set_sha256
legacy_state_snapshot
edge_policy
state_protocol
completion_bucket_order
graph_summary
hard_edges
reuse_hints
shared_lemma_groups
theorems
```

There MUST be exactly 1546 theorem records and no record outside the frozen target set. Each record
contains at least:

```text
theorem_id
name
category
original_execution_rank
v2_execution_rank
completion_bucket
phase_states
direct_hard_parents
direct_hard_children
direct_reuse_hint_ids
shared_lemma_group_ids
transitive_hard_ancestors
topological_layer
dependency_audit_status
evidence_inventory
reusable_artifacts
dependency_context_sha256
```

The `phase_states` projection MUST name the same seven stable tasks already present in the rev-5.6
execution DAG:

```text
INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE
```

No v2 theorem edge replaces this intra-theorem chain. Cross-theorem edges add prerequisites or
context to the relevant existing phase; they do not create an eighth phase.

### 3.1 Hard Dependencies

A hard edge means that an exact provider result or content-bound artifact is consumed by the
consumer's machine proof. It uses `edge_type: proof_dependency | artifact_dependency`,
`blocking: true`, and the fields:

```text
edge_id
edge_type
parent_theorem_id
child_theorem_id
blocking
evidence_strength
evidence
material_contract
state_semantics
```

A relationship may be hard only when evidence identifies the exact cross-target Lean import,
declaration dependency, or content-addressed provider artifact actually read by the consumer's
replay validator and binds it to statement/proof-body provenance and receipts. Name
similarity, textbook convention, a natural historical order, shared vocabulary, an LLM judgment, or
an unpinned citation is insufficient. Unknown exactness fails closed as a reuse hint or an unaudited
relationship, never as a fabricated blocking edge.

Every hard edge must satisfy all of the following:

1. both endpoints are in the 1546-target manifest;
2. parent and child roles are explicit and directionally correct;
3. the exact consumed declaration, statement fingerprint, checked transport, or hashed replay input
   is identifiable;
4. the terminal body and import provenance are not confused with a wrapper name, and an artifact
   edge states whether it orders proof preparation or only requires provider bytes at replay time;
5. the evidence boundary states what is and is not proved; and
6. the hard-edge subgraph is acyclic.

`material_contract` is an edge-local allowlist, not an owner-directory allowlist. It content-binds
each admitted provider and consumer Lean source as `{path, sha256, declarations}`. For a proof edge,
the provider hashes must also occur under the named proof-receipt `/inputs/...` binding and the
consumer source must be the cross-target import/use route admitted by that evidence. For an artifact
edge, every provider source must be derived from the structured manifest's `source_path_sha256`, and
the contract binds the target-owned adapter and replay script that consume it. An unrelated theorem
or wrapper in the same provider/consumer directory cannot satisfy the hard edge. This restriction is
only for accepted hard-edge reuse; it does not turn hints or weak shared groups into blockers.

If candidate hard edges form a cycle, the generator MUST NOT break it by arbitrary rank. It must
re-audit direction and exact declarations. A genuinely mutually defined package must be modeled by
an explicit shared package/lemma artifact under rev-5.6 and then exposed through acyclic consumption
edges. Until that occurs, the disputed edges remain nonblocking review records.

### 3.2 Reuse Hints

A reuse hint points to likely useful mathematics, APIs, proof patterns, source crosswalks, or common
lemma bodies without claiming logical necessity. It uses `blocking: false` and the fields:

```text
hint_id
hint_type
provider_theorem_id
consumer_theorem_id
blocking
confidence
evidence
reuse_boundary
```

Hints may be derived from exact imports that are not root-critical, common canonical obligation or
proof-body identities, named theorem references, shared source structure, or conservative
domain/lemma matching. The evidence MUST say which case applies. Hints may be revised as audits
improve and MUST NOT:

- block a consumer from being scheduled;
- make a parent master accepted;
- clear a child obligation;
- count as proof coverage; or
- be described publicly as a proved dependency.

The absence of a hard edge makes two nodes operationally parallelizable; it is not a mathematical
claim that their proofs are independent. This distinction lets the scheduler exploit concurrency
without turning an approximate graph into false certainty.

### 3.3 Dependency Audit Status

Each theorem has exactly one dependency-audit value:

| Value | Meaning |
|---|---|
| `audited_hard_dependency_found` | at least one exact hard parent passed the hard-edge evidence gate |
| `audited_reuse_only` | the inspected evidence supports hints but no hard parent |
| `unknown_not_independent_proof_claim` | the current inventory is insufficient; no independence claim is made |

This field reports graph knowledge, not theorem completion. A later exact Lean dependency may add a
hard edge, invalidate the old order for affected open work, and require a new deterministic DAG
revision. It does not erase previously valid receipts unrelated to that change.

The current repository inventory is conservative: it contains no preexisting cross-theorem edges,
some targets have no instance directory, and only a subset has typed proof graphs. Therefore every
node still appears in v2, but `unknown_not_independent_proof_claim` is the required default when
evidence does not establish a relationship. `no confirmed hard parent` never means `mathematically
independent proof`.

### 3.4 Shared Lemma and Module Groups

The top-level `shared_lemma_groups` array records an exact structured identity seen in at least two
theorem dossiers. Every nonblocking group contains:

```text
group_id
group_type
identity_kind
canonical_identity
member_theorem_ids
evidence_paths
confidence
blocking
reuse_boundary
```

The current group types are `shared_module_cluster` and `shared_terminal_body`. Module clusters are
weak co-mention/search clusters, not claims of a common lemma or proof body. A terminal group is
admitted only for a global canonical declaration/body identity; target-local and path-based names
are namespaced and cannot merge across theorem owners. Invalid/prose/path module strings are
excluded. These groups provide broad reuse discovery without inventing an arbitrary
provider-to-consumer direction. A node's `shared_lemma_group_ids` is its complete membership
projection. Group membership requires a worker to inspect exact declarations and types before
duplicate work, but `blocking` remains false until a consumer-specific import or checked transport
earns an audited hard edge.

## 4. Deterministic Ordering and Parallel Waves

The v2 rank is computed over the hard-edge DAG using Kahn topological sorting. At each ready
frontier, choose the next theorem using this stable key:

```text
(
  completion_bucket_order,
  topological_layer,
  original_execution_rank,
  theorem_id
)
```

where the bucket order is:

```text
master_complete = 0
fully_self_tested = 1
partial = 2
unstarted = 3
```

Hard parent precedence always wins. Bucket priority applies only among nodes currently ready in the
hard DAG. Thus completed and already-invested work is surfaced early without moving a consumer in
front of an actual parent. `v2_execution_rank` is total, contiguous from 1 through 1546, and does
not overwrite `original_execution_rank`.

`topological_layer` describes hard-dependency depth and supports parallel waves:

- all hard parents of a node are in earlier layers;
- nodes in the same layer may run concurrently when their owned paths and runtime resources
  permit; and
- reuse hints may influence which context is prefetched, but never serialize the wave.

The scheduler should prefer the earliest v2-ranked theorem with useful unfinished work, while still
honoring the existing phase DAG and dual-cursor rules. A theorem with a `[_]` handoff is integration
work, not a reason to issue a duplicate worker. A theorem whose remaining phase is blocked by a hard
parent yields its slot to another ready theorem rather than idling unrelated work.

## 5. Mandatory Parent and Ancestor Inspection

Before a newly claimed `PROOF` phase may implement proof content, the executor MUST build a
content-addressed dependency context for the consumer. This is a hard preflight gate for pure proof
work, not optional reading advice.

The context closure includes:

1. every `direct_hard_parent`;
2. every `transitive_hard_ancestor` in parent-before-child order;
3. every direct reuse provider selected by the run; and
4. the accepted hard ancestors of a selected reuse provider when they explain the reusable body.

For every theorem in that closure, inspect and record:

- all seven authoritative phase states and the theorem completion bucket;
- canonical statement and environment fingerprints, alternate transports, and boundary cases;
- lifecycle, `AUDIT-Z`, `THEOREM-Z`, and current H/M/R vectors;
- canonical obligation IDs, proof-tree nodes, root cut set, and open blockers;
- accepted receipt IDs, input digests, validity/freshness, and revocation state;
- exact Lean module/declaration, pinned revision, axiom/TCB result, and terminal proof-body identity;
- reusable lemmas, APIs, construction invariants, composition certificates, source crosswalks, and
  human-readable anchors; and
- any mismatch in foundations, universes, domains, assumptions, imports, toolchain, license, or
  source boundary that prevents reuse.

The run MUST bind the resulting context digest in its worker evidence packet. If the graph or an
inspected parent changes before master integration, the context is stale and must be regenerated or
explicitly shown unaffected.

State semantics are strict:

- an `[x]` parent artifact may be consumed within the exact scope of its accepted receipt;
- a `[_]` artifact may guide search and avoid exploratory duplication, but remains provisional and
  cannot transfer parent theorem acceptance; a consumer may close only after its own exact
  content/hash, import/transport, trust, composition, and replay receipt passes;
- a `[ ]` result is open context only; and
- a theorem-level source label such as `verified` supplies no proof credit.

If a blocking hard parent lacks either accepted closure for the exact consumed result or the
content-bound artifact plus successful consumer replay required by that edge's `state_semantics`,
the consumer proof run may prepare a transport, interface, or conditional skeleton, but it must
report the proof phase as dependency-blocked. A hard edge never implies that all seven parent phases
must be `[x]`; its exact artifact gate controls. It may not replace the premise with an axiom or
silently prove a weaker theorem.

## 6. Reuse Ledger and Common Lemma Policy

Every `PROOF` run produces or updates
`Stage1_Instances/<THEOREM-ID>/dependency-reuse-ledger.json`. This derived ledger is excluded from
the theorem-DAG discovery inventory so it cannot change its own context hash. Each material
candidate records:

```yaml
schema_version: stage1-dependency-reuse-ledger/1.1
consumer_theorem_id: <THM-M-ID>
observed_theorem_dag_sha256: <full observed graph digest>
dependency_context_sha256: <stable target context digest>
repository_revision: <worker base revision>
direct_parent_ids: [<all direct hard parents>]
transitive_ancestor_ids: [<all hard ancestors>]
hard_edge_ids: [<all incoming hard edges>]
reuse_hint_ids: [<all direct reuse hints>]
shared_group_ids: [<all shared module/body groups>]
inspections: [<one phase-state/artifact/compatibility record per hard parent or ancestor>]
reuse_decisions: [<one decision per hard edge, hint, or shared group>]
consumer_obligation_id: <stable obligation id>
provider_theorem_id: <THM-M-ID or shared package id>
provider_obligation_id: <stable obligation id>
terminal_proof_body_id: <canonical body identity>
provider_body_source: {path: <provider-owned Lean source>, sha256: <digest>}
provider_statement_fingerprint: <hash>
consumer_required_fingerprint: <hash>
relationship: exact | checked_transport | implication | candidate_only | mismatch
provider_proof_state: "[ ]" | "[_]" | "[x]"
provider_receipts: [{path: <repo-relative provider receipt>, receipt_id: <id>, sha256: <digest>}]
decision: reused_exact | reused_with_transport | candidate_only |
          rejected_mismatch | blocked_missing_acceptance | not_applicable
consumer_import_or_wrapper: <repo-relative declaration/path or none>
consumer_import_source: {path: <consumer-owned Lean source>, sha256: <digest>}
consumer_validation_receipts: [{path: <repo-relative consumer validation receipt>, receipt_id: <id>, sha256: <digest>}]
non_reuse_reason: <required unless reuse is accepted>
context_digest: <dependency-context digest>
unresolved_compatibility_obligations: [<open exact compatibility work>]
```

Receipt references are structured and content-bound, never bare IDs. Each path must stay inside the
referenced theorem's owned directory; the referenced JSON must agree on receipt ID, theorem ID, and
phase, and its bytes must match `sha256`. `provider_proof_state` must equal the provider inspection's
current authoritative proof mark; it is observation, never inherited credit. An accepted reuse
decision requires exact content-bound provider evidence, but does not require a blanket provider
`[x]`: each hard edge follows its own artifact/import/hash and consumer-replay `state_semantics`.
Provider and ancestor files are always compared byte-for-byte with the authoritative checkout; a
worker-local rewrite outside the consumer's owned path cannot satisfy the gate.
A proof-phase ledger records the complete inspection and reuse decision but cannot invent
the later consumer-validation receipt. A target-owned, content-bound consumer receipt becomes
mandatory at the `VALIDATION` worker-handoff gate; it remains provisional there because that phase
is only advancing to `[_]`, but it must declare a successful worker self-test rather than a blocked,
failed, or rejected verdict. At `RELEASE`, the same validation receipt and its authoritative phase
must be master accepted `[x]`; a blocked, missing, stale, or cross-target receipt fails closed.

A provisional consumer validation receipt referenced by schema 1.1 must expose the normalized fields
`selftest_status: passed` and `selftest_result: {exit_code: 0, commands: [<nonempty exact command
records>]}`. Missing status, arbitrary verdict prose, an empty command record, or a nonzero exit code
cannot satisfy the worker-handoff gate. Each receipt command must match a successful command record
in the worker handoff packet and the committed, authority-bound validation specification. The
integration lane replays that authoritative recipe itself before merging; a worker-created or
worker-modified validator cannot satisfy the gate. Provider
receipts use the rev-5.6 node-receipt schema, stable item ID, base revision, input bindings, and
successful accepted or normalized self-test evidence; schema-less or blocked provider JSON is not a
receipt.

Material fields are decision-sensitive. `reused_exact` and `reused_with_transport` require the full
obligation, body, statement-fingerprint, provider-receipt, and consumer import/transport record.
Candidate, mismatch, and blocked decisions retain the compared material plus a non-reuse reason.
For a weak shared-module co-mention that was inspected and found irrelevant, `not_applicable` needs
only the source/group ID, an actual member theorem used for the inspection, the context digest, and
a non-reuse reason; workers must not invent an obligation, body, or fingerprint to fill the ledger.
For `reused_exact`, inspection compatibility and relationship are both `exact`, both statement
fingerprints are equal 64-hex digests, and no compatibility obligation remains unresolved. For
`reused_with_transport`, compatibility and relationship are both `checked_transport`, fingerprints
remain explicit 64-hex digests, and the consumer wrapper/transport is recorded. Mismatch and open
compatibility work can never be labeled accepted reuse.
The terminal body and consumer import/wrapper declaration must occur in their respective bound Lean
source files, whose bytes match both the worker view and authoritative checkout. A nonempty invented
name is not evidence. Provider receipts used for accepted reuse must themselves be successful
accepted or normalized worker-self-tested evidence; an explicitly blocked provider receipt cannot
support `reused_exact` or `reused_with_transport`.
For an accepted hard-edge decision, `provider_body_source` and its declaration and
`consumer_import_source` and its declaration must additionally be exact members of that edge's
content-bound `material_contract`. Owner-scoped but unlisted material is rejected. Hint/shared-group
decisions remain governed by their own evidence and are not forced into a hard-edge contract.

The reuse policy is:

1. Compare canonical statement fingerprints, contexts, foundations, and proof-body provenance before
   implementing a duplicate lemma.
2. When an accepted exact body already exists, import it rather than reproving it.
3. When a checked transport is required, implement and validate the transport in the consumer.
4. Reuse proof content, not acceptance. The consumer still needs its own import, composition,
   provenance, trust, and validation receipts.
5. Shared aliases, wrappers, and copied evidence rows do not create new semantic coverage.
6. One canonical terminal body may serve many consumers, but its credit is deduplicated by body ID.
7. A rejected candidate remains in the ledger with its mismatch so later workers do not repeat the
   same failed search.
8. A new local proof is justified only after the ledger shows that no compatible accepted body or
   transport is available for that exact obligation.

Common lemmas that are not themselves one of the 1546 theorem roots are first-class reusable
artifacts, not invented theorem targets. They receive stable obligation/body identities, provenance,
owners, validation, and consumer links under the relevant theorem or shared formalization package.
They do not change the 1546 denominator. Frequently shared mathlib declarations may define a lemma
cluster or reuse hint, but do not by themselves establish a directed hard theorem edge. Existing
`neighbor_target_boundaries` are exclusions unless exact evidence proves otherwise.

## 7. Execution and Dual-Cursor Rules

The existing seven phases retain their rev-5.6 meanings. V2 changes their work order and proof
preflight as follows:

| Phase | v2 addition |
|---|---|
| `INTAKE` | attach the theorem node and dependency-audit status; do not infer proof credit |
| `STATEMENT` | expose exact fingerprints needed for edge and reuse comparison |
| `ANCHOR_AUDIT` | inventory cross-target imports, formal candidates, and likely common bodies |
| `OBLIGATION_TREE` | type all root-critical parent uses and canonical shared obligations |
| `PROOF` | require the parent/ancestor context digest and reuse ledger before new proof content |
| `VALIDATION` | validate imported bodies, transports, composition, trust, and consumer receipts |
| `RELEASE` | recheck hard-parent closure and context freshness before terminal decisions |

The three checkbox states remain exact:

- `[ ]`: not done and potentially worker-claimable;
- `[_]`: worker implementation plus self-test exists, awaiting master integration; and
- `[x]`: master accepted after dependency-legal integration and validation.

Workers may only propose `[ ] -> [_]`. Only the master may accept `[_] -> [x]`. Both `[ ]` and `[_]`
are unfinished. Regeneration preserves marks by stable item ID. A v2 reorder never resets an item,
and neither a worker nor the theorem-DAG generator writes `[x]`.

Worker claims and master integration remain separate frontiers:

- worker capacity is consumed only by live claims;
- landed `[_]` work enters the integration queue and frees its worker slot;
- the claim frontier uses v2 theorem order plus existing phase eligibility;
- the integration frontier requires all intra-theorem dependencies to be `[x]`, every cross-theorem
  hard edge to satisfy its exact `state_semantics`, and conflict-free owned paths; an
  `artifact_dependency` never inherits or requires the provider's seven checkbox states unless its
  own evidence contract says so; and
- legacy pre-v2 edge receipts may be displayed as `legacy_evidence_present`, never as a satisfied
  new v2 ledger gate; exact v2 acceptance still requires the current consumer ledger/receipt checks;
- later provisional work may be prepared concurrently, but master acceptance remains topological.

After five unresolved attempts, split the open obligation into smaller stable child items under the
rev-5.6 instance model. Do not create duplicate theorem roots or bypass the parent context gate.

## 8. Master Acceptance

For a v2-scheduled item, the master performs every rev-5.6 acceptance check and additionally verifies:

1. the theorem ID, v2 rank, phase states, and dependency context agree with current authorities;
2. every consumed hard edge satisfies its exact declaration/content, receipt, replay, and
   `state_semantics` gate; no blanket provider checkbox rule substitutes for that evidence;
3. all transitive ancestors required by the imported dependency closure were inspected;
4. hint-only material was not counted as a premise or machine closure;
5. reused bodies and wrappers have correct body identity, provenance, trust, and source boundaries;
6. required transports and child-to-parent composition are kernel checked;
7. the consumer reuse ledger records accepted, rejected, and blocked candidates truthfully;
8. no existing accepted or still-valid self-tested work was duplicated or silently discarded; and
9. the context digest is fresh for the integrated snapshot.

If these checks fail, the item remains `[_]` and receives a repair child or explicit blocker. Master
acceptance follows typed dependency semantics, never merely the longest textual prefix or v2 rank.

## 9. Validation Contract

Run the v2 graph validator together with the existing assurance and state validators:

```bash
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 Docs/tools/check_stage1_theorem_dag_v2.py
python3 scripts/stage1_execution_cron.py --validate-only --workers 0
```

`Docs/tools/check_stage1_theorem_dag_v2.py` MUST fail on at least:

- target count, target-ID set, or digest mismatch;
- a missing, duplicate, or extra theorem node;
- a missing or changed snapshot of any of the 10,822 phase item states;
- an invalid completion bucket or dependency-audit value;
- a hard or hint endpoint outside the manifest;
- duplicate edge/hint IDs, self edges, malformed typed records, or wrong blocking semantics;
- a hard-edge cycle, incorrect transitive hard-ancestor closure, or parent-after-child v2 rank;
- noncontiguous or nondeterministic v2 ranks;
- a v2 ordering inconsistent with the documented Kahn frontier key;
- a hard edge lacking exact evidence or being derived only from a reuse hint;
- a reuse hint presented as acceptance or proof coverage; or
- a dependency-reuse ledger being consumed as graph-discovery input, which would make its own
  context self-invalidating;
- an absolute/private runtime path exposed as stable public evidence.

Positive validation proves structural conformance only. It does not prove that every approximate
hint is mathematically complete, that an unaudited theorem is independent, or that any theorem has
reached `THEOREM-Z`.

## 10. Regeneration and Change Control

The generator and validator must make regeneration idempotent. With unchanged target, state, and
evidence inputs, byte-semantic graph content and v2 ranks remain stable. A change SHOULD emit an
explicit delta containing added/removed/changed hard edges, hint changes, affected transitive
ancestors, rank movement, context invalidations, and the reason/evidence for each change. Until a
separate durable delta artifact exists, Git's reviewable JSON diff is the change ledger and schema
validation remains mandatory.

Breaking field or edge semantics increment the schema major version. Existing JSON, receipts, and
status history remain available as immutable migration inputs. A generator must never rewrite a
historical receipt, delete a failed reuse decision to improve metrics, or downgrade an authoritative
state without rev-5.6 invalidation evidence.

Daily todo views are generated from the two structured DAGs:

- theorem order and parent context come from `Stage1_Theorem_DAG_v2.json`;
- phase state and stable task identity come from `Stage1_Execution_DAG_rev-5.6.json`; and
- the todo reports `[ ]`, `[_]`, and `[x]` separately, plus live claims, landed integration backlog,
  hard-parent blockers, and the v2 worker/integration frontiers.

There is one writable phase-state authority, not two independently editable completion surfaces.

## 11. Cron and Cleanup Boundary

This blueprint does not itself start a cron or workers. A future execution cron must first pass all
validators, use the v2 theorem frontier, preserve operator-selected model/effort/service-tier
settings, isolate worker workspaces, and keep the master as the only integration owner.

Cron cleanup is allowed only when all of the following are true:

1. the rev-5.6 execution DAG contains zero `[ ]` and zero `[_]` items;
2. every one of the 1546 theorem nodes is `master_complete` with valid rev-5.6 terminal evidence;
3. the latest todo reports unfinished zero;
4. both graph validators and all required release gates pass;
5. no live worker, finished handoff, pending integration, or checkpoint remains; and
6. the cleanup command removes the exact project cron line and verifies its absence.

An empty ready frontier caused by blockers is not completion and must not trigger cleanup.

## 12. Conceptual Graph

The full 1546-node graph is machine-readable JSON. Its semantics can be summarized as:

```text
rev-5.6 assurance and receipts
             |
             v
  accepted or content-bound provider body --hard dependency--> consumer theorem
             |                                             |
             +--------------- reuse_hint ------------------+
                                                           |
                direct + transitive context inspection -----+
                                                           |
                reuse ledger / checked transport -----------+
                                                           v
            existing 7-phase rev-5.6 state and master acceptance
```

Disconnected hard-DAG roots and nodes connected only by nonblocking hints can be worked in
parallel. Consumers wait only for evidenced hard prerequisites at closure time, while still reading
useful parent and common-lemma context before proof implementation.

## 13. Definition of v2 Blueprint Success

This blueprint is successfully instantiated only when:

- the theorem DAG contains all and only the 1546 frozen targets;
- the 10,822 existing phase states and all stable item identities are preserved exactly;
- hard proof dependencies and nonblocking reuse hints are typed and never conflated;
- the hard subgraph is acyclic and has a deterministic parent-first rank;
- completed, fully self-tested, and partial work is prioritized within each legal ready frontier;
- every new proof run has a hash-bound direct/transitive parent context and reuse ledger;
- accepted parent proofs and common lemmas are reused without duplicating proof credit;
- existing valid work is not repeated merely because the global order changed;
- workers and master continue to obey the rev-5.6 dual-cursor and evidence gates; and
- `Docs/tools/check_stage1_theorem_dag_v2.py` plus all existing validators pass.

V2 success is an orchestration result. It makes later proof work better ordered and better informed;
it does not, by itself, claim that any additional theorem has been proved.
