# Stage5.1 Theorem and Conjecture Organization Design

> Document role: project-specific design contract for the Stage5.1 organization
> release and its two execution Blueprints. This document is not an activated
> controller, a catalog release, a mathematical-dependency claim, or an
> acceptance receipt.
>
> Display revision: `Stage5.1`
>
> Catalog parent: Stage5 catalog release `5.6`
>
> Organization release namespace: `stage5_1_organization`

## 1. Version-name boundary

`Stage5.1` in this design is the display revision of the theorem/conjecture
organization and execution surfaces. It is **not** the historical Stage5
catalog release `5.1`. The source identities and source bytes remain pinned by
the current parent catalog release `5.6`; this design neither rolls the catalog
back to `5.1` nor republishes historical `5.1` records.

Every generated manifest must therefore carry separate, closed fields for:

- `blueprint_display_revision = "Stage5.1"`;
- `catalog_parent_release = "5.6"` and its exact authority digest;
- `organization_release = "1.0"` (or a later append-only organization
  release); and
- the historical catalog `5.1` namespace as a non-parent predecessor only
  where an original record actually came from that release.

No tool may abbreviate these three version axes to one ambiguous `version`
field.

### 1.1 Stage6 draft boundary

Stage5.1 is the current project SSOT. No Stage6 catalog, renumbering,
qualification, candidate, migration, or execution draft is a current input or
an execution surface. The former `Docs/catalog/v6/` draft tree has therefore
been retired and is intentionally empty. A future Stage6 publication, if ever
authorized, must be a separately reviewed append-only successor rooted in a
published Stage5.1 release; it must not be reconstructed from stale Stage5
blueprint prose or from a draft alias registry. The Stage5 predecessor
blueprints retain their Stage6 paths only as historical, digest-bound evidence
for the migration that produced Stage5.1 and must not be used to launch work or
allocate identities.

## 2. Frozen scope and honest completion boundary

The Stage5.1 organization covers the frozen sets currently supplied by the
Stage5 `5.6` authorities:

- 3,500 theorem identities;
- 1,425 strict-conjecture identities; and
- 14,865 source-occurrence intake identities.

The resulting 19,790 organization members preserve category boundaries. A
source occurrence is not silently promoted to a strict conjecture, and a
strict conjecture is not silently reclassified as a theorem. An identity
review may later relate several occurrences to one mathematical identity, but
it never deletes or reuses their occurrence IDs.

"Complete organization" means every frozen member has exactly one reversible
identity mapping, exactly one subject-assignment record (which may honestly use
a sentinel), exactly one dependency-assessment record, and exactly one
member-kind-specific Stage5.1 execution row. It does not mean every member has
a confident fine subject or an admitted dependency edge. Unknown evidence must
remain visible.

The generated authority is rooted at
`Docs/catalog/stage5_1_organization/Current_Release.json`; its immutable release
files, source bindings, schemas and set digests—not this prose—decide the exact
bytes accepted by a Blueprint BOOT.

The read-only query surface follows that pointer rather than hard-coding an
organization release. It fails closed unless the pointer seal, selected
manifest path/release/hash/authority binding, and every queried artifact digest
agree. Member output keeps assignment coordinates, relations, dependency
assessment, hard-DAG/closure, and execution dependencies separate; candidate
cross-root hints are explicitly non-scheduling.

## 3. Four layers that must never be collapsed

Stage5.1 has four separately versioned and validated layers:

1. **Identity and crosswalk.** Says which immutable Stage5/Stage5-pool object a
   Stage5.1 member names. It does not encode a subject, proof state or
   dependency.
2. **Subject taxonomy and assignment.** Gives a navigable discipline tree,
   multi-label memberships and evidence state. Reclassification changes an
   assignment, not the member identity.
3. **Mathematical relations and dependency assessment.** Records only typed,
   directed, evidence-bound relationships. It distinguishes hard proof/artifact
   prerequisites from semantic relations, identity/source links and reuse
   hints.
4. **Execution DAG.** Uses Blueprint `depends_on` solely for scheduling and
   material availability. A mathematical edge affects this DAG only through an
   explicit reviewed hard-edge projection; presentation order and subject
   proximity never do so.

In particular:

- the same subject is not a dependency;
- a shared module, title, family, keyword, source collection or AMS/MSC code is
  not a dependency;
- `equivalent_to`, `special_case_of`, `generalizes` or `reduces_to` does not by
  itself grant reusable artifacts or scheduler blocking;
- an execution edge never transfers proof credit or checkbox state; and
- no admitted edge means "no admitted edge under the present evidence," not
  "the objects are mathematically independent."

The Gantt projections must expose these layers in different fields. They may
display a subject path and mathematical prerequisites beside execution
`depends_on`, but must not render them as one graph or one concurrency count.

## 4. Stable member IDs and exact legacy mapping

Subject codes are deliberately absent from stable member IDs. The following
grammars preserve the legacy eight-digit ordinal exactly:

| Kind | Frozen source identity | Legacy execution row | Stage5.1 member locator | Stage5.1 execution row |
|---|---|---|---|---|
| theorem | `S5-CLM-NNNNNNNN` | `S5THM-NNNNNNNN-TARGET` | `S51-THM-NNNNNNNN` | `S51THM-NNNNNNNN-TARGET` |
| strict conjecture | `S5-CLM-NNNNNNNN` | `S5CON-NNNNNNNN-TARGET` | `S51-CON-NNNNNNNN` | `S51CON-NNNNNNNN-TARGET` |
| source occurrence | `S5POOL-NNNNNNNN` | `S5CON-POOL-NNNNNNNN-INTAKE` | `S51-OCC-NNNNNNNN` | `S51CON-POOL-NNNNNNNN-INTAKE` |

Here `NNNNNNNN` is the literal eight digits from the frozen predecessor; it is
not reallocated, left-padded again, sorted by subject, or inferred from row
position. The kind prefix disambiguates the theorem and conjecture spaces.
There is exactly one Stage5.1 member and exactly one Stage5.1 member row for
each frozen member.

`Mathematical_ID_Crosswalk.jsonl` carries this member bijection. It must bind
both predecessor and successor IDs, source-record hashes, member kind and the
exact parent release. `Legacy_Checklist_Row_Crosswalk.jsonl` separately accounts
for every old checklist row, including BOOT, shard, aggregate, QA and release
rows. Control-row dispositions may be predecessor-only or mapped to a new
control row; they may never be mistaken for mathematical identities.

Future identity review, split/merge evidence or canonical-equivalence grouping
is represented in `Object_Index.jsonl` and typed relations. It does not rewrite
this ordinal-preserving crosswalk.

## 5. Subject-tree contract

### 5.1 Stable nodes and external notation

Internal subject nodes use append-only stable IDs such as
`S51-SUB-NNNNNNNN`. Human labels, translations, MSC revisions and parentage are
attributes, not identities. An external coordinate such as `MSC2020:05Cxx` is
stored as a scheme/code crosswalk; it is never spliced into a theorem,
conjecture or occurrence ID.

`Subject_Node_ID_Registry.jsonl` is the sealed allocation authority. Its stable
key canonically binds `scheme`, `edition`, `notation`, and the source identity
(`subject_key`). Release 1.0 bootstraps the registry from its generated node
IDs. Every successor release must reuse the exact predecessor mapping, reject
duplicate or stale rows, and allocate unseen keys strictly after the greatest
previous numeric `S51-SUB` ID. Therefore source reordering and insertion do not
renumber existing nodes.

Each normal subject node records at least:

- one stable `subject_id`;
- an English display label and a `zh` display field whose release-1.0 value is
  a source-label fallback when no reviewed Chinese translation is available
  (field equality therefore does not assert that a human translation exists);
- `scheme` and nullable external `notation`;
- one `parent_subject_id` for the deterministic browsing tree;
- zero or more `broader_subject_ids` for honest multi-parent/cross-domain
  placement;
- a closed structural `rank`, lifecycle status and selection policy; and
- content-addressed provenance for externally sourced codes or labels.

Root reachability is derived and checked from the parent graph rather than
duplicated in every node. Supersession is a release-to-release migration event,
not an optional mutable field on a release-1.0 node. A later release may add a
reviewed translation ledger without rewriting these frozen source labels.

The primary-parent projection must be rooted and acyclic. The broader-subject
graph may have multiple parents but must also be acyclic. Cross-domain
membership is expressed through assignments and broader roots, not by inventing
an artificial "interdisciplinary" identity.

### 5.2 Required sentinel nodes

Coverage is total because uncertainty is represented, not guessed. The closed
reserved sentinels are:

- `S51-SUB-UNCLASSIFIED`: evidence is insufficient even for a useful branch;
- `S51-SUB-REVIEW-PENDING`: evidence exists but has not passed the required
  review;
- `S51-SUB-AMBIGUOUS`: competing primary assignments remain unresolved; and
- `S51-SUB-OUT-OF-SCOPE`: the object is bound correctly but the current
  taxonomy does not claim a suitable subject.

A sentinel is a truthful primary assignment, not a missing record. Sentinels
cannot appear as secondary labels, cannot be counted as fine-classified, and
cannot be used to infer mathematical or execution edges.

### 5.3 Primary, secondary and method facets

Every member has exactly one `primary_subject_id`, including a sentinel when
necessary. `secondary_subject_ids` is a unique, ordered set of additional
mathematical homes and may cross any root. Proof techniques, formalization
technology and source-provider categories belong in `method_facets` or
`source_labels`; they do not silently replace the subject of the statement.

`cross_domain=true` is derived only when accepted non-sentinel primary and
secondary assignments reach different root subjects. The record carries the
root IDs that justify the derived value. A source cross-list or model guess can
produce a cross-domain candidate, but not an accepted cross-domain claim.

### 5.4 Evidence levels and assignment state

Evidence level and review state are independent closed fields. Recommended
evidence levels, from strongest direct authority to no supporting evidence,
are:

| Evidence level | Meaning | Maximum unreviewed use |
|---|---|---|
| `independent_review` | identity-distinct reviewer accepted the exact assignment against bound statement bytes | eligible for Master acceptance |
| `source_exact` | a per-object source supplies an exact subject/code | source-exact candidate; preserve source semantics |
| `source_category` | source field, category or cross-list supplies a broader signal | provisional branch candidate |
| `machine_crosswalk` | deterministic module/root or controlled-vocabulary crosswalk | coarse candidate only |
| `statement_candidate` | statement/title/rule/model analysis proposes a label | review queue only |
| `none` | no admissible classification evidence | sentinel required |

Assignment state is one of `accepted`, `candidate`, `review_pending`,
`ambiguous`, `unclassified`, `out_of_scope` or `rejected`. Only the canonical
Master can write `accepted`, and it must cite an independent review receipt.
Lower evidence must not be upgraded merely to fill a leaf-level denominator.
If evidence supports only a two-digit MSC class, the assignment stops there;
the builder must not fabricate a three- or five-character class.

Every evidence entry names the repository-relative path, exact locator,
evidence kind and SHA-256 of the bytes inspected. Source collection, module
root, same title and classification adjacency remain provenance or candidates,
never self-authenticating fine labels.

## 6. Mathematical relation and prerequisite contract

### 6.1 Direction and typed relations

Edges use explicit endpoint roles rather than the overloaded words “source”
and “target”. `consumer_member_id -> provider_member_id` has the frozen
direction semantics `consumer_requires_provider`: the consumer requires or
consumes material supplied by the provider. Every edge records endpoint
identity hashes, relation kind, this direction convention, evidence, review
state, cross-domain derivation and scheduler effect.

Relation kinds are separated into at least these families:

- hard material relations: `proof_prerequisite`, `artifact_dependency`,
  `checked_formal_import`;
- mathematical semantics: `implies`, `reduces_to`, `generalizes`,
  `special_case_of`, `equivalent_to`;
- nonblocking reuse: `reuse_hint`, `shared_lemma_group`, `method_adaptation`;
- parameter/source/identity context: `same_parameter_family`,
  `parameter_neighbor`, `source_crosswalk`, `related_source`,
  `identity_candidate`.

The last three families are nonblocking unless a later, separately reviewed
hard material edge proves exact consumption. Equivalence and other semantic
relations may contain cycles. `Execution_Hard_DAG.json` contains only admitted
hard edges and must be acyclic; it must never be obtained by treating every
relation as a prerequisite.

### 6.2 Hard-edge admission

A hard edge is admitted only when all of the following are content-bound:

1. both endpoint members and exact statements resolve in the current immutable
   organization release;
2. the consumer's checked artifact, import or replay validator demonstrably
   consumes a named provider artifact;
3. provider and consumer paths, declarations and SHA-256 values are recorded in
   a material contract;
4. an identity-distinct review accepts the direction and relation kind;
5. the proposed hard graph remains acyclic; and
6. `execution_blocking` and its precise material-availability semantics are
   explicit.

Shared topics, modules, names, proof ideas or parameter families fail this gate.
An independently reviewed semantic reduction without a consumable artifact may
be valuable, but remains nonblocking.

The target-owned material binding consists of one provider artifact plus three
closed typed receipts.  Provider acceptance identifies both the artifact
producer actor and its acceptance issuer; independent review identifies its
reviewer and issuing authority; consumer replay identifies the consumer
execution owner and its acceptance issuer.  The independent reviewer must be
different from the producer, consumer execution owner, and both acceptance
issuers.  Every receipt binds the exact edge ID, endpoint roles, frozen
direction and provider-artifact digest.  The replay receipt additionally binds
the command digest, observed-output digest, consumed provider digest, and a
hash-checked result under the consumer's Blueprint-owned paths.

Cross-domain hard edges are fully permitted. They pass the same evidence gate
as same-domain edges and additionally cite the accepted endpoint subject
assignments. `cross_domain` is derived from those roots; it is not selected to
make an edge look interdisciplinary.

### 6.3 Unknown is not independent

`Dependency_Assessments.jsonl` contains exactly one assessment for every one of
the 19,790 members, even when the member has no relation edge. Its closed states
include:

- `audited_edges_present`;
- `source_edges_present_pending_review`;
- `audited_no_admitted_edge`; and
- `unknown_not_independent_proof_claim`.

An empty edge list and `unknown_not_independent_proof_claim` are the normal
truthful result when the repository lacks exact proof-body or artifact evidence.
A release with `hard_edge_count = 0` is valid if that is what the admission gate
finds. It means zero currently admitted hard edges, not 19,790 independent
objects. The builder and Gantt must report the assessment-state denominator
alongside the edge count.

Source-occurrence relations remain occurrence-scoped and provisional while the
pool identity review is pending. They cannot target a strict claim or become a
blocking proof prerequisite merely because a title, source ID or statement hash
looks related.

## 7. Projection into the two execution Blueprints

The authoritative Stage5.1 execution surfaces are:

- `Docs/Stage5_1_Theorems_Blueprint.md` and
  `Docs/Stage5_1_Theorems_Gantt.md`;
- `Docs/Stage5_1_Conjectures_Blueprint.md` and
  `Docs/Stage5_1_Conjectures_Gantt.md`.

The theorem program binds
`releases/1.0/programs/theorems/Organization_Workset.jsonl`; the conjecture
program binds
`releases/1.0/programs/conjectures/Organization_Workset.jsonl`. Each member row
binds its object-index record, ID crosswalk, subject assignment, dependency
assessment and relevant relation/closure records by digest. These bindings are
immutable claim inputs, not extra phase rows or extra workers.

One object still owns one long-lived logical TARGET/INTAKE and at most one live
worker generation. Organization work does not introduce a second
`CLASSIFY`/`DEPENDENCY` worker, phase checklist identity, tmux session or
`/goal`. A generation completes the target-local organization and theorem or
conjecture gates under its one goal, with durable checkpoint/handoff before any
replacement.

The Blueprint row exposes separately:

- stable member and predecessor IDs;
- primary/secondary subject assignment references;
- mathematical prerequisite and assessment references;
- execution `depends_on`;
- exact owned paths and acceptance gate.

Only an admitted edge in `Execution_Hard_DAG.json` may be projected into
target-to-target execution `depends_on`, and the projection is exact and
reviewed. With zero admitted hard edges, member rows depend on BOOT rather than
on fabricated subject-order chains. Shard, aggregate, QA and release edges are
controller-owned execution aggregation, not mathematical relations.

## 8. Migration and proof-state semantics

The migration receipt is
`Docs/catalog/stage5_1_organization/migrations/stage5-v2_to_stage5_1-1.0.json`.
It binds the prior theorem/conjecture Blueprints and Gantts, parent catalog and
pool authorities, all crosswalk bytes, preserved artifacts, and the exact new
pristine projections.

Whatever proof, handoff, checkpoint, receipt, live, retired or stopped state
exists at the migration boundary is predecessor evidence only. It may be
content-addressed and replayed by a Stage5.1 claim, but it does not transfer an
old checkbox, worker generation, tmux server, thread, goal, claim lease or
request accounting into the new epoch.

Both Stage5.1 Blueprints are initially materialized with a completely blank
cursor. In particular:

- old `[x]` is recorded as `legacy_accepted` evidence, never copied to new
  `[x]`;
- old `[_]`, handoff or checkpoint remains replayable evidence, never copied to
  new `[_]`;
- old `[ ]` conveys no classification or dependency assessment; and
- every Stage5.1 `[x]` requires the new taxonomy, dependency, mapping and target
  gates to pass against integrated bytes.

This is a new execution epoch, not a destructive rewrite. Old Blueprints,
Gantts, runtime evidence and receipts remain immutable predecessor surfaces.
Any old live lane must be harvested or safely fenced and its exact transport
retired before a new mapped generation can start; generations may not overlap.

## 9. Activation fence and explicit concurrency

Generating release files or blank Blueprints does not activate execution. The
activation checker is `Docs/tools/check_stage5_1_activation_fence.py`. It must
fail closed unless, at minimum:

- `Current_Release.json` selects one exact immutable release and all manifest,
  input, crosswalk, taxonomy, assignment, assessment, relation, hard-DAG,
  closure and workset digests validate;
- all frozen predecessor members and checklist rows have the required exact
  crosswalk/disposition with no duplicate, omission or ordinal drift;
- the taxonomy and assignment invariants, dependency evidence gate and hard-DAG
  acyclicity pass;
- both new Blueprint/Gantt pairs are exact same-prefix projections of the
  selected release and start from the migration-authorized blank cursor;
- predecessor admission is fenced, live predecessor work is durably harvested,
  and no predecessor transport is being reinterpreted as a successor lane;
- Stage5.1 BOOT has been independently reviewed and accepted before ordinary
  member admission; and
- the current operator prompt supplies the complete concurrency vector required
  by the execution specification and its digest matches the activation request.

There is no concurrency default in this design, the release, either Blueprint,
the execution skill, environment variables, CPU discovery or an old runtime.
A missing, partial, unknown, stale, inherited or ambiguous concurrency prompt
means: no reservation, no tmux server, no Codex TUI, no `/goal`, no request and
no cron activation. Validation and release construction remain read-only with
respect to worker lifecycle.

The prompt must name every field in the frozen Stage5.1 concurrency schema,
including logical/service records, agent executions, startup reservations,
launch fanout, live transports, authenticated goals, running turns, outbound
request rate and window, in-flight requests, integration, validator and
exact-path-conflict limits, desired-live target and hard cap. An explicit
`not_applicable` is valid only where that closed schema permits it; omission is
not `not_applicable`.

Every admitted Codex generation continues to require an independent task-local
tmux server, private writable `CODEX_HOME`, interactive Codex TUI and exactly
one authenticated `/goal`, with all execution/turn/request/integration limits
charged to the explicit prompt.

## 10. Generated authorities and ownership

The builder `Docs/tools/build_stage5_1_organization_release.py` owns these
release files under `Docs/catalog/stage5_1_organization/releases/1.0/`:

- `Organization_Manifest.json`;
- `Source_Input_Manifest.json`;
- `Subject_Taxonomy.json`;
- `Subject_Nodes.jsonl`;
- `Subject_Node_ID_Registry.jsonl`;
- `Object_Index.jsonl`;
- `Mathematical_ID_Crosswalk.jsonl`;
- `Legacy_Checklist_Row_Crosswalk.jsonl`;
- `Subject_Assignments.jsonl`;
- `Dependency_Assessments.jsonl`;
- `Relation_Edges.jsonl`;
- `Execution_Hard_DAG.json`;
- `Dependency_Closure.jsonl`;
- `Cross_Domain_Edges.jsonl`;
- `programs/theorems/Organization_Workset.jsonl`; and
- `programs/conjectures/Organization_Workset.jsonl`.

`Docs/tools/check_stage5_1_organization_release.py` validates their schemas,
hashes, counts, set equality, crosswalks, subject graphs, assessments, relation
evidence and hard-DAG projection. Generated release files and Gantts are not
hand-edited; corrections create new deterministic bytes and an append-only
migration/release.

## 11. Future immutable organization release 1.1

Release `1.0` is the Stage5.1 migration baseline selected by exact digest. A
future `releases/1.1/` may promote independently reviewed fine classifications,
resolved sentinels and newly evidenced mathematical relations. This document
does not assert that release `1.1` already exists, that all candidates will be
accepted, or that it will contain a nonzero hard-edge set.

When published, `1.1` is a new immutable directory with its own source-input
manifest, schemas, set digests and migration receipt. It must preserve all
member IDs and eight-digit legacy mappings; changes to labels, parents,
assignments, assessments or edges are explicit supersessions with predecessor
digests. `Current_Release.json` is atomically advanced only after the complete
new release validates. No `1.0` byte is overwritten, and activation always
binds the exact selected release rather than an implicit "latest".
