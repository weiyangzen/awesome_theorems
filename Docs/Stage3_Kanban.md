# Stage3 Worker Kanban

> Generated read-only view for `stage3-list-completion/3.0`; this is not a second checklist or completion authority.
> Planning blockers are derived from the Blueprint DAG. Runtime blocks come only from a validated runtime snapshot.

<!-- STAGE3-PROJECTION-METADATA:BEGIN -->
```json
{
  "schema_version": "stage3-projection-metadata/3.0",
  "blueprint_path": "Docs/Stage3_Blueprint.md",
  "blueprint_version": "stage3-list-completion/3.0",
  "gantt_path": "Docs/Stage3_Gantt.md",
  "status_path": "Docs/Stage3_Status.json",
  "kanban_path": "Docs/Stage3_Kanban.md",
  "raw_blueprint_sha256": "e6642cefa91dd618c1ded1887e676367964d1ba2c0df3192256379d2683b56e6",
  "execution_spec_region_sha256": "315cb1cc074df3fbe42ea55bbe81c7674bc68f2adc19d714e174d0ab69bf7e42",
  "runtime_snapshot_sha256": null,
  "runtime_snapshot_id": null,
  "runtime_snapshot_path": ".ops/stage3-execution-v1/status/runtime-snapshot.json",
  "cleanup_receipt_path": "Docs/evidence/stage3_cleanup.json",
  "cleanup_receipt_sha256": null,
  "cleanup_receipt_id": null,
  "projection_input_sha256": "9fd4312cc971238d43eb8fe98441cf2ff98404105a9712819ebfae0a2f9fdd28",
  "snapshot_id": "stage3-projection/9fd4312cc971238d43eb8fe98441cf2ff98404105a9712819ebfae0a2f9fdd28",
  "generated_at": "2026-08-09T23:58:05Z"
}
```
<!-- STAGE3-PROJECTION-METADATA:END -->

## Runtime snapshot

`runtime_unavailable`; every worker runtime count and lifecycle value is `null`, never an invented zero. Terminal `cleanup_state` is `not_started` from the optional durable cleanup receipt.

| Runtime field | Value |
|---|---:|
| `logical_claims` | `null` |
| `reserved` | `null` |
| `starting` | `null` |
| `authenticated_live_goals` | `null` |
| `running_turns` | `null` |
| `finished_handoffs` | `null` |
| `dependency_blocked` | `null` |
| `conflict_blocked` | `null` |
| `startup_blocked` | `null` |
| `resource_blocked` | `null` |
| `external_limit_blocked` | `null` |
| `route_blocked` | `null` |
| `validator_blocked` | `null` |
| `budget_blocked` | `null` |
| `integration_backlog` | `null` |
| `repair_backlog` | `null` |
| `logical_claim_target` | `null` |
| `startup_reservation_target` | `null` |
| `authenticated_live_target` | `null` |
| `running_turn_target` | `null` |
| `admitted_target` | `null` |
| `eligible_ready_count` | `null` |
| `requested_target` | `null` |
| `host_admissible_target` | `null` |
| `master_integration_target` | `null` |
| `cpu_validator_lease_target` | `null` |
| `active_cpu_validator_leases` | `null` |
| `effective_target_bindings` | `null` |
| `logical_saturation` | `null` |
| `admitted_saturation` | `null` |
| `underfill_stop_reason` | `null` |
| `occupancy_underfill_reason` | `null` |
| `cleanup_state` | `"not_started"` |

## Implementation-ready

- `S3-AUTH-002`
- `S3-AUTH-003`
- `S3-AUTH-004`

## Validation-preparation

_None._

## Starting

_None._

## Live

_None._

## Handoff

_None._

## Integration

_None._

## Repair

_None._

## Planning-blocked

- `S3-BEN-001` — blockers: `S3-REL-004`
- `S3-BEN-002` — blockers: `S3-CAT-002`, `S3-BEN-001`
- `S3-BEN-003` — blockers: `S3-MATH-020`, `S3-BEN-001`, `S3-BEN-002`
- `S3-BEN-004` — blockers: `S3-PHY-019`, `S3-BEN-001`, `S3-BEN-002`
- `S3-BEN-005` — blockers: `S3-CS-025`, `S3-BEN-001`, `S3-BEN-002`
- `S3-BEN-006` — blockers: `S3-CAT-013`, `S3-BEN-003`, `S3-BEN-004`, `S3-BEN-005`
- `S3-BEN-007` — blockers: `S3-BEN-006`
- `S3-BEN-008` — blockers: `S3-BEN-001`, `S3-BEN-006`
- `S3-BEN-009` — blockers: `S3-BEN-002`, `S3-BEN-006`, `S3-BEN-007`, `S3-BEN-008`, `S3-BEN-017`, `S3-M38-034`
- `S3-BEN-010` — blockers: `S3-BEN-007`, `S3-BEN-009`
- `S3-BEN-011` — blockers: `S3-BEN-002`, `S3-BEN-009`, `S3-BEN-017`
- `S3-BEN-012` — blockers: `S3-BEN-008`, `S3-BEN-010`, `S3-BEN-011`, `S3-BEN-018`, `S3-BEN-019`, `S3-BEN-020`
- `S3-BEN-013` — blockers: `S3-BEN-010`, `S3-BEN-011`, `S3-BEN-012`
- `S3-BEN-014` — blockers: `S3-BEN-001`, `S3-BEN-002`, `S3-BEN-006`, `S3-BEN-008`, `S3-BEN-009`, `S3-BEN-010`, `S3-BEN-011`, `S3-BEN-012`, `S3-BEN-013`, `S3-BEN-021`
- `S3-BEN-015` — blockers: `S3-BEN-014`
- `S3-BEN-016` — blockers: `S3-AUTH-004`, `S3-REL-004`
- `S3-BEN-017` — blockers: `S3-BEN-002`, `S3-BEN-016`
- `S3-BEN-018` — blockers: `S3-BEN-004`, `S3-BEN-009`, `S3-BEN-011`, `S3-BEN-017`
- `S3-BEN-019` — blockers: `S3-BEN-005`, `S3-BEN-009`, `S3-BEN-011`, `S3-BEN-017`
- `S3-BEN-020` — blockers: `S3-BEN-008`, `S3-BEN-010`, `S3-BEN-016`
- `S3-BEN-021` — blockers: `S3-BEN-012`, `S3-BEN-013`, `S3-BEN-018`, `S3-BEN-019`, `S3-BEN-020`
- `S3-CAT-001` — blockers: `S3-REL-004`
- `S3-CAT-002` — blockers: `S3-CAT-001`
- `S3-CAT-003` — blockers: `S3-CAT-001`, `S3-CAT-002`, `S3-CAT-015`
- `S3-CAT-004` — blockers: `S3-CAT-001`, `S3-CAT-002`, `S3-CAT-003`, `S3-CAT-006`, `S3-CAT-014`, `S3-CAT-015`
- `S3-CAT-005` — blockers: `S3-CAT-004`
- `S3-CAT-006` — blockers: `S3-CAT-002`
- `S3-CAT-007` — blockers: `S3-CAT-002`, `S3-CAT-006`
- `S3-CAT-008` — blockers: `S3-CAT-001`, `S3-CAT-002`, `S3-CAT-004`, `S3-CAT-005`, `S3-CAT-014`
- `S3-CAT-009` — blockers: `S3-CAT-003`, `S3-CAT-005`, `S3-MATH-008`, `S3-PHY-008`, `S3-CS-016`
- `S3-CAT-010` — blockers: `S3-CAT-005`, `S3-CAT-009`
- `S3-CAT-011` — blockers: `S3-CAT-006`, `S3-CAT-007`, `S3-CAT-016`, `S3-MATH-020`, `S3-PHY-019`, `S3-CS-025`
- `S3-CAT-012` — blockers: `S3-CAT-011`
- `S3-CAT-013` — blockers: `S3-CAT-011`, `S3-CAT-012`, `S3-CAT-016`
- `S3-CAT-014` — blockers: `S3-CAT-001`
- `S3-CAT-015` — blockers: `S3-CAT-002`, `S3-CAT-014`
- `S3-CAT-016` — blockers: `S3-CAT-010`, `S3-CAT-014`, `S3-CAT-015`, `S3-MATH-016`, `S3-PHY-015`, `S3-CS-022`
- `S3-CS-001` — blockers: `S3-CAT-001`, `S3-CAT-008`
- `S3-CS-002` — blockers: `S3-CAT-002`, `S3-CS-001`
- `S3-CS-003` — blockers: `S3-CAT-006`, `S3-CS-001`
- `S3-CS-004` — blockers: `S3-CS-001`, `S3-CS-002`, `S3-CS-026`
- `S3-CS-005` — blockers: `S3-CS-001`, `S3-CS-002`, `S3-CS-026`
- `S3-CS-006` — blockers: `S3-CS-001`, `S3-CS-002`, `S3-CS-026`
- `S3-CS-007` — blockers: `S3-CS-001`, `S3-CS-002`, `S3-CS-026`
- `S3-CS-008` — blockers: `S3-CS-001`, `S3-CS-002`, `S3-CS-026`
- `S3-CS-009` — blockers: `S3-CS-001`, `S3-CS-002`, `S3-CS-026`
- `S3-CS-010` — blockers: `S3-CS-001`, `S3-CS-002`, `S3-CS-026`
- `S3-CS-011` — blockers: `S3-CS-001`, `S3-CS-002`, `S3-CS-026`
- `S3-CS-012` — blockers: `S3-CS-001`, `S3-CS-002`, `S3-CS-026`
- `S3-CS-013` — blockers: `S3-CS-001`, `S3-CS-002`, `S3-CS-026`
- `S3-CS-014` — blockers: `S3-CS-004`, `S3-CS-005`, `S3-CS-006`, `S3-CS-007`, `S3-CS-008`, `S3-CS-009`, `S3-CS-010`, `S3-CS-011`, `S3-CS-012`, `S3-CS-013`
- `S3-CS-015` — blockers: `S3-CS-003`, `S3-CS-014`
- `S3-CS-016` — blockers: `S3-CS-014`, `S3-CS-015`
- `S3-CS-017` — blockers: `S3-CAT-010`, `S3-CS-016`
- `S3-CS-018` — blockers: `S3-CAT-010`, `S3-CS-016`
- `S3-CS-019` — blockers: `S3-CAT-010`, `S3-CS-016`
- `S3-CS-020` — blockers: `S3-CAT-007`, `S3-CAT-010`, `S3-CS-016`
- `S3-CS-021` — blockers: `S3-CAT-006`, `S3-CAT-010`, `S3-CS-016`
- `S3-CS-022` — blockers: `S3-CS-017`, `S3-CS-018`, `S3-CS-019`, `S3-CS-020`, `S3-CS-021`
- `S3-CS-023` — blockers: `S3-CAT-016`, `S3-CS-002`, `S3-CS-022`, `S3-CS-026`
- `S3-CS-024` — blockers: `S3-CS-023`
- `S3-CS-025` — blockers: `S3-CS-024`
- `S3-CS-026` — blockers: `S3-CAT-015`, `S3-CS-002`, `S3-CS-003`, `S3-BEN-016`
- `S3-ENV-003` — blockers: `S3-REL-004`
- `S3-ENV-004` — blockers: `S3-ENV-003`
- `S3-ENV-005` — blockers: `S3-ENV-003`, `S3-ENV-004`, `S3-M38-019`, `S3-M38-021`
- `S3-ENV-006` — blockers: `S3-ENV-003`
- `S3-ENV-007` — blockers: `S3-ENV-004`, `S3-ENV-005`, `S3-M38-012`
- `S3-ENV-008` — blockers: `S3-ENV-006`, `S3-ENV-007`, `S3-ENV-009`, `S3-M38-033`
- `S3-ENV-009` — blockers: `S3-ENV-006`, `S3-ENV-007`, `S3-M38-039`
- `S3-EXE-001` — blockers: `S3-AUTH-002`, `S3-AUTH-003`
- `S3-EXE-002` — blockers: `S3-EXE-001`
- `S3-EXE-003` — blockers: `S3-EXE-002`
- `S3-EXE-004` — blockers: `S3-EXE-003`
- `S3-EXE-005` — blockers: `S3-EXE-004`
- `S3-EXE-006` — blockers: `S3-EXE-005`
- `S3-EXE-007` — blockers: `S3-EXE-002`, `S3-EXE-005`
- `S3-EXE-008` — blockers: `S3-EXE-006`, `S3-EXE-007`
- `S3-EXE-009` — blockers: `S3-EXE-008`
- `S3-EXE-010` — blockers: `S3-EXE-006`, `S3-EXE-007`, `S3-EXE-008`
- `S3-EXE-011` — blockers: `S3-AUTH-002`, `S3-EXE-010`
- `S3-EXE-012` — blockers: `S3-EXE-009`, `S3-EXE-010`, `S3-EXE-011`
- `S3-EXE-013` — blockers: `S3-EXE-012`
- `S3-EXE-014` — blockers: `S3-EXE-002`, `S3-EXE-003`, `S3-EXE-004`, `S3-EXE-005`, `S3-EXE-006`, `S3-EXE-007`, `S3-EXE-008`, `S3-EXE-009`, `S3-EXE-010`, `S3-EXE-011`, `S3-EXE-012`, `S3-EXE-013`
- `S3-EXE-015` — blockers: `S3-EXE-014`
- `S3-M38-001` — blockers: `S3-REL-004`
- `S3-M38-002` — blockers: `S3-M38-001`
- `S3-M38-003` — blockers: `S3-M38-002`
- `S3-M38-004` — blockers: `S3-M38-003`
- `S3-M38-005` — blockers: `S3-M38-002`
- `S3-M38-006` — blockers: `S3-M38-005`
- `S3-M38-007` — blockers: `S3-M38-003`, `S3-M38-004`, `S3-M38-005`, `S3-M38-006`
- `S3-M38-008` — blockers: `S3-M38-001`
- `S3-M38-009` — blockers: `S3-M38-001`
- `S3-M38-010` — blockers: `S3-M38-001`
- `S3-M38-011` — blockers: `S3-M38-001`
- `S3-M38-012` — blockers: `S3-ENV-004`, `S3-CAT-016`, `S3-M38-001`
- `S3-M38-013` — blockers: `S3-M38-001`
- `S3-M38-014` — blockers: `S3-M38-007`, `S3-M38-008`, `S3-M38-009`, `S3-M38-010`, `S3-M38-011`, `S3-M38-013`
- `S3-M38-015` — blockers: `S3-M38-012`, `S3-M38-014`, `S3-M38-040`
- `S3-M38-016` — blockers: `S3-M38-012`, `S3-M38-015`, `S3-M38-035`, `S3-M38-036`, `S3-M38-037`
- `S3-M38-017` — blockers: `S3-M38-016`
- `S3-M38-018` — blockers: `S3-M38-007`, `S3-M38-008`, `S3-M38-009`, `S3-M38-010`, `S3-M38-011`, `S3-M38-014`, `S3-M38-015`, `S3-M38-016`, `S3-M38-042`
- `S3-M38-019` — blockers: `S3-M38-017`, `S3-M38-018`
- `S3-M38-020` — blockers: `S3-M38-012`, `S3-M38-017`, `S3-M38-019`
- `S3-M38-021` — blockers: `S3-M38-020`
- `S3-M38-022` — blockers: `S3-ENV-005`, `S3-M38-019`, `S3-M38-021`, `S3-M38-024`, `S3-M38-038`, `S3-M38-041`
- `S3-M38-023` — blockers: `S3-M38-022`
- `S3-M38-024` — blockers: `S3-CAT-013`, `S3-M38-012`, `S3-M38-015`
- `S3-M38-025` — blockers: `S3-M38-017`, `S3-M38-021`, `S3-M38-024`, `S3-M38-038`
- `S3-M38-026` — blockers: `S3-BEN-002`, `S3-BEN-017`, `S3-M38-024`, `S3-M38-025`
- `S3-M38-027` — blockers: `S3-M38-021`, `S3-M38-026`
- `S3-M38-028` — blockers: `S3-M38-027`
- `S3-M38-029` — blockers: `S3-M38-018`, `S3-M38-021`, `S3-M38-023`, `S3-M38-028`, `S3-M38-030`
- `S3-M38-030` — blockers: `S3-M38-023`, `S3-M38-024`, `S3-M38-025`, `S3-M38-026`, `S3-M38-027`, `S3-M38-028`
- `S3-M38-031` — blockers: `S3-M38-019`, `S3-M38-021`, `S3-M38-023`, `S3-M38-029`, `S3-M38-030`, `S3-M38-066`
- `S3-M38-032` — blockers: `S3-M38-022`, `S3-M38-031`
- `S3-M38-033` — blockers: `S3-M38-032`, `S3-ENV-006`, `S3-ENV-007`
- `S3-M38-034` — blockers: `S3-M38-030`, `S3-M38-033`, `S3-M38-039`, `S3-M38-041`, `S3-M38-066`, `S3-ENV-008`
- `S3-M38-035` — blockers: `S3-ENV-004`, `S3-M38-001`
- `S3-M38-036` — blockers: `S3-CAT-016`, `S3-ENV-004`, `S3-M38-012`
- `S3-M38-037` — blockers: `S3-M38-012`, `S3-M38-036`
- `S3-M38-038` — blockers: `S3-ENV-005`, `S3-M38-021`
- `S3-M38-039` — blockers: `S3-M38-016`, `S3-M38-017`, `S3-M38-033`, `S3-M38-035`, `S3-M38-038`
- `S3-M38-040` — blockers: `S3-M38-012`, `S3-M38-013`, `S3-M38-014`
- `S3-M38-041` — blockers: `S3-AUTH-004`, `S3-M38-018`, `S3-M38-024`
- `S3-M38-042` — blockers: `S3-M38-002`, `S3-M38-004`, `S3-M38-005`, `S3-M38-006`, `S3-M38-007`
- `S3-M38-060` — blockers: `S3-M38-029`
- `S3-M38-061` — blockers: `S3-M38-029`
- `S3-M38-062` — blockers: `S3-M38-029`
- `S3-M38-063` — blockers: `S3-M38-029`
- `S3-M38-064` — blockers: `S3-M38-029`
- `S3-M38-065` — blockers: `S3-M38-029`
- `S3-M38-066` — blockers: `S3-M38-060`, `S3-M38-061`, `S3-M38-062`, `S3-M38-063`, `S3-M38-064`, `S3-M38-065`
- `S3-MATH-001` — blockers: `S3-CAT-001`, `S3-CAT-008`
- `S3-MATH-002` — blockers: `S3-MATH-001`
- `S3-MATH-003` — blockers: `S3-MATH-002`
- `S3-MATH-004` — blockers: `S3-MATH-002`
- `S3-MATH-005` — blockers: `S3-CAT-002`, `S3-CAT-006`, `S3-CAT-007`, `S3-CAT-015`, `S3-MATH-001`
- `S3-MATH-006` — blockers: `S3-MATH-003`, `S3-MATH-004`, `S3-MATH-005`
- `S3-MATH-007` — blockers: `S3-MATH-006`
- `S3-MATH-008` — blockers: `S3-MATH-005`, `S3-MATH-007`, `S3-MATH-021`, `S3-MATH-022`
- `S3-MATH-009` — blockers: `S3-CAT-010`, `S3-MATH-008`
- `S3-MATH-010` — blockers: `S3-MATH-009`
- `S3-MATH-011` — blockers: `S3-MATH-009`
- `S3-MATH-012` — blockers: `S3-MATH-009`
- `S3-MATH-013` — blockers: `S3-MATH-009`
- `S3-MATH-014` — blockers: `S3-MATH-009`
- `S3-MATH-015` — blockers: `S3-MATH-009`
- `S3-MATH-016` — blockers: `S3-MATH-010`, `S3-MATH-011`, `S3-MATH-012`, `S3-MATH-013`, `S3-MATH-014`, `S3-MATH-015`
- `S3-MATH-017` — blockers: `S3-MATH-016`
- `S3-MATH-018` — blockers: `S3-MATH-003`, `S3-MATH-016`
- `S3-MATH-019` — blockers: `S3-CAT-016`, `S3-MATH-006`, `S3-MATH-008`, `S3-MATH-016`, `S3-MATH-017`, `S3-MATH-018`
- `S3-MATH-020` — blockers: `S3-MATH-019`
- `S3-MATH-021` — blockers: `S3-MATH-005`, `S3-MATH-007`
- `S3-MATH-022` — blockers: `S3-CAT-007`, `S3-CAT-015`, `S3-MATH-005`
- `S3-PHY-001` — blockers: `S3-CAT-001`, `S3-CAT-008`
- `S3-PHY-002` — blockers: `S3-CAT-002`, `S3-PHY-001`
- `S3-PHY-003` — blockers: `S3-PHY-002`
- `S3-PHY-004` — blockers: `S3-PHY-001`
- `S3-PHY-005` — blockers: `S3-CAT-006`, `S3-PHY-001`
- `S3-PHY-006` — blockers: `S3-PHY-001`, `S3-PHY-005`
- `S3-PHY-007` — blockers: `S3-PHY-002`, `S3-PHY-003`, `S3-PHY-005`, `S3-PHY-006`, `S3-PHY-020`, `S3-PHY-021`
- `S3-PHY-008` — blockers: `S3-PHY-007`
- `S3-PHY-009` — blockers: `S3-CAT-010`, `S3-PHY-003`, `S3-PHY-004`, `S3-PHY-005`, `S3-PHY-007`, `S3-PHY-022`
- `S3-PHY-010` — blockers: `S3-CAT-010`, `S3-PHY-003`, `S3-PHY-004`, `S3-PHY-005`, `S3-PHY-007`, `S3-PHY-022`
- `S3-PHY-011` — blockers: `S3-CAT-010`, `S3-PHY-003`, `S3-PHY-004`, `S3-PHY-005`, `S3-PHY-007`, `S3-PHY-022`
- `S3-PHY-012` — blockers: `S3-CAT-010`, `S3-PHY-003`, `S3-PHY-004`, `S3-PHY-005`, `S3-PHY-007`, `S3-PHY-022`, `S3-PHY-024`
- `S3-PHY-013` — blockers: `S3-CAT-007`, `S3-CAT-010`, `S3-PHY-003`, `S3-PHY-005`, `S3-PHY-007`, `S3-PHY-022`
- `S3-PHY-014` — blockers: `S3-PHY-003`, `S3-PHY-004`
- `S3-PHY-015` — blockers: `S3-PHY-008`, `S3-PHY-009`, `S3-PHY-010`, `S3-PHY-011`, `S3-PHY-012`, `S3-PHY-013`, `S3-PHY-014`, `S3-PHY-023`, `S3-PHY-024`
- `S3-PHY-016` — blockers: `S3-PHY-015`
- `S3-PHY-017` — blockers: `S3-CAT-016`, `S3-PHY-015`, `S3-PHY-016`, `S3-PHY-025`
- `S3-PHY-018` — blockers: `S3-PHY-017`
- `S3-PHY-019` — blockers: `S3-PHY-018`
- `S3-PHY-020` — blockers: `S3-CAT-015`, `S3-PHY-006`
- `S3-PHY-021` — blockers: `S3-PHY-004`, `S3-PHY-005`, `S3-PHY-006`
- `S3-PHY-022` — blockers: `S3-CAT-010`, `S3-PHY-007`, `S3-PHY-008`
- `S3-PHY-023` — blockers: `S3-CAT-006`, `S3-PHY-022`
- `S3-PHY-024` — blockers: `S3-PHY-007`, `S3-PHY-021`
- `S3-PHY-025` — blockers: `S3-CAT-016`, `S3-PHY-015`
- `S3-REL-001` — blockers: `S3-CAT-013`, `S3-BEN-015`, `S3-M38-034`, `S3-ENV-008`, `S3-REL-004`
- `S3-REL-002` — blockers: `S3-REL-006`
- `S3-REL-003` — blockers: `S3-REL-002`
- `S3-REL-004` — blockers: `S3-EXE-015`
- `S3-REL-005` — blockers: `S3-REL-003`
- `S3-REL-006` — blockers: `S3-AUTH-002`, `S3-REL-001`

## Runtime-blocked

_None._

## Accepted

- `S3-AUD-001`
- `S3-AUD-002`
- `S3-AUD-003`
- `S3-AUD-004`
- `S3-AUD-005`
- `S3-AUTH-001`
- `S3-ENV-001`
- `S3-ENV-002`

## Lifecycle vocabulary

`reserved -> materialized -> tmux_started -> goal_pasted -> goal_submitted -> live -> handoff_ready -> finished`
