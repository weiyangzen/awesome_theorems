# Stage5.1 Organization Catalog

This directory contains the generated, content-addressed organization overlay
for the Stage5.1 theorem and conjecture Blueprints. It does not replace the
Stage5 catalog, the strict-conjecture ledger or the ConjectureBench occurrence
pool.

## Namespace and parentage

- `Stage5.1` is the Blueprint display revision.
- Stage5 catalog release `5.6` is the catalog parent.
- Historical Stage5 catalog release `5.1` is a different namespace and is not
  republished or rolled back here.
- `1.0`, `1.1`, and later numbers below are organization-release versions.

The full policy and ID rules are in
`Docs/Stage5_1_Organization_Design.md`.

## Stable population

The organization overlay accounts for 19,790 frozen members:

- 3,500 theorems;
- 1,425 strict conjectures; and
- 14,865 source-occurrence intake records.

Every member retains its predecessor identity. Stage5.1 locators preserve the
literal eight-digit ordinal:

- `S5-CLM-NNNNNNNN` theorem -> `S51-THM-NNNNNNNN`;
- `S5-CLM-NNNNNNNN` strict conjecture -> `S51-CON-NNNNNNNN`;
- `S5POOL-NNNNNNNN` occurrence -> `S51-OCC-NNNNNNNN`.

The corresponding execution rows are `S51THM-NNNNNNNN-TARGET`,
`S51CON-NNNNNNNN-TARGET`, and
`S51CON-POOL-NNNNNNNN-INTAKE`. Subject reassignment never changes these IDs.

## File layout

`Current_Release.json` is the sole small pointer to one exact immutable
organization release. It is updated atomically only after the selected release
passes all checks.

Release `1.0` uses these generated paths:

| Path below `releases/1.0/` | Role |
|---|---|
| `Organization_Manifest.json` | Release schema, counts, set digests and authority root |
| `Source_Input_Manifest.json` | Exact Stage5 5.6, pool, Blueprint and predecessor-evidence input bindings |
| `Subject_Taxonomy.json` | Root/sentinel policy plus an exact hash binding to the external node table |
| `Subject_Nodes.jsonl` | Stable subject nodes, primary browsing tree and broader-subject DAG |
| `Subject_Node_ID_Registry.jsonl` | Sealed append-only stable-key to `S51-SUB` allocation authority |
| `Object_Index.jsonl` | One immutable object locator per Stage5.1 member |
| `Mathematical_ID_Crosswalk.jsonl` | Exact predecessor-member to Stage5.1-member bijection |
| `Legacy_Checklist_Row_Crosswalk.jsonl` | Explicit disposition of every predecessor checklist row |
| `Subject_Assignments.jsonl` | Exactly one primary/secondary/evidence assignment record per member |
| `Dependency_Assessments.jsonl` | Exactly one audited-or-unknown dependency assessment per member |
| `Relation_Edges.jsonl` | Typed identity, source, semantic, reuse and hard-material relation records |
| `Execution_Hard_DAG.json` | Only independently admitted, acyclic hard material prerequisites |
| `Dependency_Closure.jsonl` | Deterministic direct/transitive hard-DAG projection per member |
| `Cross_Domain_Edges.jsonl` | Recomputable projection of reviewed relations whose accepted endpoint subjects cross roots |
| `programs/theorems/Organization_Workset.jsonl` | Theorem Blueprint's sealed member projection |
| `programs/conjectures/Organization_Workset.jsonl` | Strict-conjecture plus occurrence-intake sealed member projection |

The migration receipt is outside the immutable release directory at
`migrations/stage5-v2_to_stage5_1-1.0.json`. It binds predecessor and successor
surfaces and records that old execution state is evidence-only.

Related generated execution surfaces are:

- `Docs/Stage5_1_Theorems_Blueprint.md`;
- `Docs/Stage5_1_Theorems_Gantt.md`;
- `Docs/Stage5_1_Conjectures_Blueprint.md`;
- `Docs/Stage5_1_Conjectures_Gantt.md`.

The complete Gantts are machine-complete monitoring projections and can be
large. Human navigation uses the deterministic read-only organization query
tool to resolve an old/new ID, print a subject breadcrumb, list a subject's
members, and filter typed relations by plane and direction; it never owns a
checkbox or mutates the release.

The owning tools are:

- `Docs/tools/build_stage5_1_organization_release.py`;
- `Docs/tools/classify_stage5_1_subjects.py`;
- `Docs/tools/query_stage5_1_organization.py`;
- `Docs/tools/check_stage5_1_organization_release.py`; and
- `Docs/tools/check_stage5_1_activation_fence.py`.

The generated artifacts, their manifest-reported hashes and the tools' actual
CLI contracts are authoritative. This README intentionally does not invent
hashes or undocumented command-line flags.

Before answering any query, the navigation tool verifies the current pointer's
own authority seal, the selected manifest path/release/hash/authority binding,
and the manifest SHA-256 of every release artifact it reads. Its mutually
exclusive modes are `--summary`, `--member ID`, `--subject SUBJECT_ID`,
`--children SUBJECT_ID`, and `--find-subject TEXT`; `--plane` and
`--direction requires|used_by` further filter member relations. Member lookup
accepts every old/new mathematical identity and every legacy/current checklist
control ID represented by the release crosswalk.

## Four independent ledgers

Consumers must not flatten the release into one graph:

1. `Mathematical_ID_Crosswalk.jsonl` and `Object_Index.jsonl` answer identity.
2. `Subject_Taxonomy.json`, `Subject_Nodes.jsonl` and
   `Subject_Assignments.jsonl` answer subject placement, including multi-label
   and cross-domain placement. Keeping the large node table external makes the
   closed release stream-checkable; the taxonomy object binds its exact bytes,
   ID set and row count.
3. `Dependency_Assessments.jsonl` and `Relation_Edges.jsonl` answer what has
   actually been reviewed about mathematical relationships.
4. `Execution_Hard_DAG.json` and the two Blueprint `depends_on` fields answer
   what can block execution.

Only reviewed, content-bound hard material edges enter
`Execution_Hard_DAG.json`. Same subject, title, module, source, parameter family
or semantic similarity never does. Cross-domain hard edges are allowed under
the same evidence gate.

A hard-edge binding is authority-bearing rather than a set of anonymous hash
claims: provider acceptance names the producer and acceptance issuer,
independent review names its reviewer and issuer, and consumer replay names the
execution owner and acceptance issuer.  The reviewer is independent of the
producer, consumer owner, and both acceptance issuers.  Replay receipts bind
the command/output digests, exact consumed provider artifact, and a checked
consumer-owned result path and digest.

An empty hard DAG is valid. It says no hard edge is currently admitted; it does
not say the objects are independent. Every member still has a dependency
assessment, normally `unknown_not_independent_proof_claim` when evidence is
insufficient.

An object incident to a pinned source-reported relation uses
`source_edges_present_pending_review`; this means the source edge was
enumerated, not that an independent mathematical relation audit accepted it.
Only verified relations use `audited_edges_present`.

## Classification honesty

Each member has exactly one primary subject coordinate, using a sentinel
instead of a guess when necessary. Release 1.0 keeps every source-derived
coordinate in `candidate`/pending review state; it does not claim any
independently accepted assignment. Reserved sentinels are:

- `S51-SUB-UNCLASSIFIED`;
- `S51-SUB-REVIEW-PENDING`;
- `S51-SUB-AMBIGUOUS`; and
- `S51-SUB-OUT-OF-SCOPE`.

Secondary subjects may cross discipline roots. Evidence is recorded separately
as `independent_review`, `source_exact`, `source_category`,
`machine_crosswalk`, `statement_candidate` or `none`; review state is never
inferred from that label. A coarse source code remains coarse, and a model or
module-root result remains a candidate until accepted.

The current complete projection contains no accepted cross-domain assignment.
That is an evidence result, not a topology restriction: the schema, relation
ledger and Gantt all support cross-domain coordinates and reviewed edges, but
only an independent acceptance receipt may turn candidate roots into
`cross_domain=true`.

The read-only query surface exposes all secondary and candidate coordinates so
multi-root review candidates remain discoverable even while the accepted
cross-domain projection is empty. Candidate multi-root membership is never a
scheduler edge or mathematical-credit signal.

Release `1.0` persists content-addressed evidence for each primary assignment.
Secondary and candidate coordinate IDs are deliberately retained as review
queue projections, but their separate coordinate-level source locators are not
promoted into accepted evidence in this release; the query surface marks those
coordinates as review-only rather than fabricating evidence. A future release
may add independently reviewed per-coordinate evidence without changing any
member or subject IDs.

## Migration and activation

Stage5.1 starts with new blank Blueprint cursors. Old accepted rows, self-tested
handoffs, checkpoints and runtime state are immutable predecessor evidence; no
old checkbox, worker, tmux transport, thread, goal, lease or concurrency value
is copied into the new epoch.

Release construction and validation do not activate workers. Activation fails
closed until both BOOT review and the activation fence pass and the current
operator prompt supplies the complete concurrency vector. There is no default
or inherited concurrency value in this catalog or either Blueprint. With a
missing, partial, stale, unknown or ambiguous prompt, no reservation, tmux
server, Codex process, `/goal`, request or cron may be created.

"Complete" refers to every named field in the frozen Stage5.1 concurrency
schema, not merely a worker total. Prompt validation happens before any worker
lifecycle side effect.

## Immutability and release 1.1

Do not hand-edit files under `releases/1.0/`; rebuild deterministically and
publish a new append-only release. A future immutable `releases/1.1/` may carry
independently reviewed fine classifications and new evidence-backed relations.
It must reuse its predecessor `Subject_Node_ID_Registry.jsonl`: the canonical
`scheme + edition + notation + source_identity` stable key retains its ID, and
new keys receive numeric IDs only after the predecessor's maximum. Source-row
reordering or insertion never renumbers an existing subject.
It must preserve every member ID and predecessor mapping and cite `1.0` as its
ancestor. This README does not claim that `1.1` exists or that its hard-edge set
will be nonempty.

Once a release is published, corrections create successor records and a new
migration receipt. `Current_Release.json` changes only after complete
validation; old release bytes remain addressable and unchanged.
