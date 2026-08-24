# Stage5 Mathematics Expansion Blueprint

> Document type: historical bounded Stage5 5.0/5.1 mathematics-expansion checklist
>
> Blueprint version: `stage5-math-expansion/1.0`
>
> Historical source path: `Docs/Stage5_Math_Expansion_Blueprint.md`
>
> Same-name generated monitor: `Docs/Stage5_Math_Expansion_Gantt.md`
>
> Generator and validator: `Docs/tools/generate_stage5_gantt.py`
>
> State protocol: blank means not started, underscore means durable self-check evidence awaits acceptance, and `x` means independently accepted
>
> Historical initial scheduling state: every execution item was unscheduled

## 1. Mission and completion boundary

This checklist is the bounded historical `5.0`/`5.1` tranche. All twelve
items are now independently accepted; the current Stage5.1 organization release
and its execution Blueprints supersede this closed tranche as project SSOT.

Stage5 is the concrete mathematics expansion after the bounded Stage4 gap supplement. Release `5.0`
must add exactly 1,000 distinct proved mathematics claims and exactly 1,000 distinct open mathematics
claims. Release `5.1` must preserve `5.0` byte-bound as its parent and add at least 500 further distinct
proved mathematics claims. These are new Stage5 records; the 3,484 inherited Stage4 variants never
count toward those quotas.

Completion is relative to the two release contracts and their pinned source assets. It does not mean
“all mathematics,” that every inherited Stage4 row has received semantic review, or that a human-
proved statement has a proof checked in this repository. Source category, formal syntax, importance,
material truth status, machine-proof status, identity, rights, and quota eligibility remain separate
axes.

This release uses only the pinned Formal Conjectures source. Its Lean declarations and source
categories are intake evidence: `research open`, `research solved`, `textbook`, `answer(sorry)`, and
source variants require distinct mappings, and “solved” does not claim that this repository contains
a machine-checked proof. For this historical 5.0/5.1 tranche, mathlib and
Metamath extractors were non-authoritative source-diversification tools and
could not satisfy either quota. Later versioned contracts separately admitted
mathlib without rewriting this denominator.

No candidate, archive member, declaration, or extractor output grants release credit before the
generator produces a schema-valid, source-bound, identity-reviewed record and the independent checker
recomputes its eligibility.

## 2. Predecessor boundary, not Stage5 progress

At the start of this tranche, Stage4 contained 3,484 numbered variants, including 146 structured additions, with 83 proved
claims and 39 open/conditional claims in its generated projections. Stage5 must import all 3,484 ATVs,
3,262 historical `THM-*` aliases, eight redirects, and four splits without rebinding identity or
inheriting evidence across an inapplicable edge. The Stage4 manifest explicitly leaves inherited
baseline semantic review incomplete.

Existing Stage4 files and any in-progress Stage5 files are inputs or unaccepted work. Their mere
presence does not occupy a checklist row and does not advance one. In particular, an archive download,
extractor script, schema draft, seeded registry, generated JSON, or passing local command becomes
progress only through the state protocol below.

## 3. Authority, state, and dependency rules

Only the checklist region between the exact markers below is authoritative task state. The Gantt is
a generated read-only projection and contains no checkbox syntax. Every checklist row owns a concrete
repository artifact, implementation, generated release, readable projection, or review.

- Blank is unfinished work with no accepted self-check handoff.
- Underscore is unfinished work with durable, checksum-verifiable self-check evidence awaiting
  independent acceptance. All dependencies must already be accepted.
- `x` is accepted only after its acceptance clause and dependencies have been independently checked
  on the integrated tree. No item begins in this state.

`depends_on=-` means the item has no Stage5 predecessor. All other dependencies are explicit stable
IDs and form a directed acyclic graph. Document order is explanatory only. A delivered directory root
owns the files below that root for that item. No inventory total is a task.

## 4. Sole execution checklist

<!-- STAGE5-MATH-EXECUTION-CHECKLIST:BEGIN -->
- [x] `S5M-AUTH-001` Seal the two-release expansion and curation contract | depends_on=- | delivers=Docs/catalog/v5/Stage5_Math_Expansion_Contract_v5.json | acceptance=The sealed authority fixes the exact 5.0 quota and 5.1 minimum, category and status mappings, importance and dedupe keys, source-route policy, record-level rights boundary, parent high-watermark 3484, append-only identity rules, no-inventory-credit rule, and bounded completion wording without self-reported count credit
- [x] `S5M-SCH-001` Seal the accepted mathematics claim-record schema | depends_on=S5M-AUTH-001 | delivers=Docs/catalog/v5/Math_Claim_Record_Schema_v5.json | acceptance=Draft 2020-12 validation closes all accepted record fields and source-language variants selected by the contract, separates formal and natural-language statements, status and machine-proof evidence, identity, classification, provenance, rights, importance and lifecycle, and rejects unknown fields stale digests or internally inconsistent theorem and open records
- [x] `S5M-BASE-001` Build and verify the immutable Stage4 import receipt | depends_on=- | delivers=Docs/tools/build_v4_import_receipt_v5.py,Docs/catalog/v5/V4_Import_Receipt_v5.json,scripts/test_v4_import_receipt_v5.py | acceptance=An independent rebuild authenticates all 13 Stage4 outputs and 17 authority inputs, conserves 3,484 ATV and S4 pairs 3,262 aliases eight redirects four splits and their no-inheritance boundary, binds the complete Stage4 checker result, passes mutation tests, and explicitly grants no inherited semantic truth proof or rights upgrade
- [x] `S5M-ASSET-001` Pin the Formal Conjectures release-source asset | depends_on=S5M-AUTH-001 | delivers=Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz | acceptance=The exact Formal Conjectures revision is present as locally replayable archive bytes with SHA-256 size root prefix safe member inventory toolchain and manifest hashes plus license and embedded third-party-rights evidence; a download archive member count or repository license alone grants no record credit
- [x] `S5M-EXT-001` Implement and test Formal Conjectures extraction | depends_on=S5M-ASSET-001 | delivers=Docs/tools/extract_formal_conjectures_v5.py,scripts/test_extract_formal_conjectures_v5.py | acceptance=The pinned archive is parsed without proof bodies into deterministic exact qualified declaration docstring category AMS and byte-range source blocks, malformed scopes missing metadata duplicate payloads and unsafe archives fail closed, source variants remain visible, and tests prevent research-solved or answer-sorry labels from being mistaken for repo-local proof
- [x] `S5M-SRC-001` Seal the role-bound mathematics source registry | depends_on=S5M-AUTH-001,S5M-SCH-001,S5M-EXT-001 | delivers=Docs/catalog/v5/Math_Source_Registry_v5.json | acceptance=The Formal Conjectures release source has one unique source ID pinned asset and revision, field-level source roles, exact locator rules, license and third-party rights axes and release eligibility; the canonical authority hash and counts recompute, non-authoritative diversification sources are excluded from release credit, and no seeded placeholder archive count or source name grants acceptance
- [x] `S5M-GEN-001` Implement deterministic atomic Stage5 release generation | depends_on=S5M-BASE-001,S5M-SCH-001,S5M-SRC-001 | delivers=Docs/tools/generate_math_catalog_v5.py | acceptance=The generator authenticates contract schema registry assets and predecessor receipt before allocation, independently normalizes and deduplicates quota candidates, creates exact source-bound records, appends ATO ATF ATS ATV and S5 IDs without rebinding Stage4 identities, derives all seven JSON surfaces, seals manifests, publishes atomically, and reproduces byte-identical outputs in check mode
- [x] `S5M-REL-500` Materialize and seal release 5.0 | depends_on=S5M-GEN-001 | delivers=Docs/catalog/v5/releases/5.0 | acceptance=The directory contains one Release_Manifest and exactly the seven Claim_Catalog Claim_ID_Registry Stage5_Claim_ID_Registry Migration_v4_to_v5 Theorem_List Open_Claim_List and Coverage_Ledger JSON artifacts, conserves the full Stage4 parent, and independently contains exactly 1,000 distinct eligible origin theorems plus exactly 1,000 distinct eligible origin open claims with no duplicate quota credit
- [x] `S5M-REL-510` Materialize and seal immutable-child release 5.1 | depends_on=S5M-REL-500 | delivers=Docs/catalog/v5/releases/5.1 | acceptance=The directory contains one Release_Manifest and the same seven JSON artifacts, binds the exact 5.0 manifest and release-root digests, preserves every 5.0 record and identity, appends at least 500 distinct eligible origin theorems with no quota duplication, preserves the open-claim surface, and allocates a contiguous collision-free ATV and S5 suffix
- [x] `S5M-QA-001` Independently verify both releases with adversarial tests | depends_on=S5M-REL-500,S5M-REL-510 | delivers=scripts/check_math_catalog_v5.py,scripts/test_math_catalog_v5.py | acceptance=The checker imports no generator or extractor and recomputes schema validity raw source slices semantic hashes category and status mappings rights identity migration parent roots exact or minimum quotas projections and release manifests; positive determinism read-only and mutation tests reject loss duplication spoofed counts stale hashes alias rebinding source drift status inflation and hand-edited projections
- [x] `S5M-READ-001` Generate the two readable Markdown release surfaces | depends_on=S5M-QA-001 | delivers=Docs/catalog/v5/readable/5.0,Docs/catalog/v5/readable/5.1 | acceptance=Each directory is generated only from its accepted JSON release, exposes theorem open coverage source and migration views with exactly matching ID sets and counts, names the release and source digests, contains no independent task-state cursor, and adds no truth proof importance or completeness claim absent from the authorities
- [x] `S5M-REV-001` Perform the terminal independent Stage5 release review | depends_on=S5M-QA-001,S5M-READ-001 | delivers=Docs/reviews/Stage5_Math_Expansion_Release_Review.md | acceptance=The review reruns the complete command matrix on the integrated tree, records exact input tool release and readable-surface digests, traces both quota denominators and all migration invariants to independent evidence, resolves every P0 and P1 finding, and states the source-relative catalog boundary without claiming all mathematics or inherited semantic completion
<!-- STAGE5-MATH-EXECUTION-CHECKLIST:END -->

## 5. Terminal acceptance and publication boundary

This historical tranche is complete because all 12 rows are independently
accepted, both release manifests and the terminal review agree, and the Gantt
is regenerated from the final Blueprint bytes. A current-release pointer was
introduced by later append-only releases and now authenticates 5.6, but it is
not this checklist's task-state authority.

No historical schedule dates or duration estimates were recorded. The final
Gantt therefore reports all 12 accepted items with timing `not_recorded` and
has no unfinished or unscheduled item. This Blueprint and its generator do not
implement a controller, create a cron entry, or authorize installation of one.

## 5A. Harness execution contract (when this closed tranche is replayed)

The harness is repository-agnostic and receives concurrency only from an explicit
operator prompt. There is no Blueprint, skill, environment-variable or host
headroom concurrency default: the prompt must provide the complete vector
(`logical_claims`, `service_records` or `not_applicable`, `agent_executions`,
`startup_reservations`, `launch_fanout_per_wave`, `live_transports`,
`authenticated_goals`, `running_turns`, `outbound_request_starts_per_window`,
`in_flight_requests`, `integration`, `validators`, and `exact_path_conflicts`),
with missing/unknown/stale values rejected before side effects.

The execution mapping is lane-based: one durable lane represents one checklist
object, while every retry or replacement is a fresh generation with a new task
root, private tmux server/socket/session, private `CODEX_HOME`, thread and one
`/goal`. The old generation is harvested and fenced before its lane is reused.
Independent admissions run in concurrent waves using the prompt fanout outside
the scheduler lock; sibling failures are isolated, and the ledger/Gantt records
the prompt epoch/digest, requested and effective vectors, lane/generation
lineage, request-rate/in-flight usage and every scale-down reason. This section
is a project-specific activation boundary only; the reusable execution skill
defines the generic strategy.

## 6. Non-blocking source-diversification assets

These tools are not checklist items, do not affect Stage5 completion, and contribute zero `5.0` or
`5.1` quota credit. Their presence is recorded only to prevent them from being confused with the
Formal Conjectures release route.

| Path | Role in this release | Release authority |
|---|---|---|
| `Docs/tools/extract_mathlib_theorems_v5.py` | noncredit diversification candidate for 5.0/5.1; later contracts use separately pinned mathlib routes | none in this tranche |
| `Docs/tools/extract_metamath_theorems_v5.py` | noncredit source-diversification candidate | none |

## 7. Projection commands

```bash
python3 Docs/tools/generate_stage5_gantt.py
python3 Docs/tools/generate_stage5_gantt.py --check
```
