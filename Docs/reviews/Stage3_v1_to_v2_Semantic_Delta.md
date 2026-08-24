# Stage3 v1 to v2 Semantic Delta

> Date: `2026-08-10`
>
> From: `stage3-list-completion/1.0`
>
> To: `stage3-list-completion/2.0`
>
> Reason: breaking correction against the locally installed
> `b3ehive/1.5.0+codex.20260809210355` execution contract.
>
> Repository-addressable v1 Blueprint: unavailable; v1 was never committed or stored as a tracked
> content-addressed artifact. A best-effort reconstruction from local ephemeral Codex session patch
> history produced SHA-256 `d5a9bb21c1413610b20c051fd956eab0ec06346b8b903a74f93d7080989770df`,
> but that reconstruction is contextual evidence only and is not an accepted predecessor snapshot.

This delta is a migration note, not a byte-for-byte independently reproducible v1 receipt or a second
checklist. The former reported digest
`d5a9bb216743e29b1d89a094ad72981f01282a0199621860e759628c9770df` was unsupported and is retained
here only as a rejected historical value. `Docs/Stage3_Blueprint.md` remains the only authoritative
Stage3 cursor.

## Breaking corrections

1. The same-name Gantt changes from a schedule-only dependency projection to the required read-only
   schedule plus complete Kanban monitoring projection. It covers every stable ID exactly once and
   binds checklist, dependency, ownership, worker-lifecycle, blocked and timing state.
2. Status changes from `stage3-execution-status/1.0` to `/2.0`. Planning-DAG blockers and observed
   runtime blockers are separate namespaces; eligible, requested, host-admissible and effective
   targets plus binding underfill reasons are explicit; an absent runtime ledger is
   `null/unavailable`, not a fabricated zero.
3. Projection freshness is content-bound by Blueprint, execution-specification and runtime-snapshot
   digests plus an optional validated terminal-cleanup receipt digest, one shared snapshot ID and UTC
   generation time. Items without recorded timing are explicitly unscheduled. Status and Kanban are
   atomically replaced before the final Gantt surface.
4. The controller and transport are explicit canonical-Master bootstrap work. The cron activates
   immediately after controller acceptance; later environment, catalog, benchmark and M0387 roots
   require that activation. Completion cleanup becomes a mandatory lifecycle postcondition after the
   final checklist item, avoiding a self-blocking final row.
5. Scientific review identities now distinguish the primary six-task audit from supplemental
   second-pass and reused nested inputs. No transcript is relabeled as a signed attestation.
6. Catalog bootstrap freezes baseline occurrences and known candidate seeds without pretending that
   future splits or newly discovered candidates are already dispositioned. `CAT-009` is a draft
   allocator; `CAT-010` reaches a relation/allocation fixed point over frozen identity fingerprints;
   and `CAT-013` reruns discovery against the curated final catalog. Included blocked, unknown,
   unreviewed or deferred records prevent list completion, and only external out-of-manifest
   candidates may receive policy exclusion.
7. M0387 post-repair review now depends on the accepted receipt checker and fixtures. Cold replay
   consumes the isolated environment policies and a frozen clean tree; legacy receipt bytes and raw
   plus canonical hashes are preserved; final M0387 acceptance consumes the environment terminal.
   The current validator is noncircular, six reviews bind a stable finding-ID denominator and the
   reviewed pre-replay candidate, and Stage3-local replay remains distinct from historical Stage1
   phase acceptance.
8. Benchmark record families are provisional until tasks exist. A post-task family overlay closes
   shared-answer, proof-template, premise and data edges before splitting; generated assets receive a
   final rights closure; task IDs do not depend on the future benchmark release; and the outer release
   envelope avoids manifest self-hashing.

## State migration

`S3-AUTH-002` was reopened because its v1 acceptance gate required the now-invalid schedule-only
Gantt. Its v2 implementation may return to `[x]` only after the new generator, checker, generated
surfaces and adversarial tests pass together. Other preserved `[x]` rows retain only their narrow
input-observation boundaries and do not inherit any new completion claim.

No runtime claim, worker reservation, catalog completion, conjecture resolution, benchmark release,
M0387 closure or cleanup success is inferred from this migration.

## Exact authority migration summary

- The reconstructed local-history view and current v2 both contain the same 168 checklist IDs with no
  intended renumbering; because the v1 bytes are not repository-addressable, this is migration
  context rather than an independently accepted repository invariant.
- `S3-AUTH-002` changes `[x] -> [ ]` until v2 projection acceptance, and adds this semantic-delta
  document to its owned paths.
- `S3-REL-004` moves from the release tail to the bootstrap/execution bridge and depends on the
  accepted controller plus frozen environment/audit inputs. `S3-ENV-003`, `S3-CAT-001`,
  `S3-BEN-001` and `S3-M38-001` consume its activation receipt.
- `S3-REL-001` consumes `S3-REL-004` instead of `S3-EXE-015`; `S3-REL-003` explicitly consumes
  `S3-AUD-004`; `S3-REL-005` becomes cleanup readiness, while cleanup success moves to the mandatory
  post-checklist lifecycle receipt.
- `S3-CAT-001` changes ownership from the premature final disposition ledger to a pending-review
  queue. `S3-CAT-009` owns draft allocation, `S3-CAT-010` owns final registry/migration and relation
  convergence, final disposition-ledger ownership moves to `S3-CAT-011`, and `S3-CAT-008` becomes an
  initial baseline/seed partition.
- `S3-M38-030` freezes the pre-replay candidate and immutable public status surfaces before the six
  reviews; `S3-M38-029` adds `S3-AUD-004`, `S3-M38-023` and `030`; `S3-M38-033` adds
  `S3-ENV-006/007`; `S3-M38-034` adds `S3-M38-066` and `S3-ENV-008`. The final public M0387 pointer
  ownership moves from warm replay `032` to final acceptance `034`, while replay outputs are excluded
  from semantic inputs and checked for non-feedback.
- `S3-BEN-009` consumes final `S3-M38-034` rather than pre-replay `031`.
