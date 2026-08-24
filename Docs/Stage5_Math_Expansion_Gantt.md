# Stage5 Mathematics Expansion Gantt and Monitor

> Generated read-only planning projection for `stage5-math-expansion/1.0`.
> Historical read-only projection; the current task-state SSOT is Stage5.1.

<!-- STAGE5-MATH-GANTT-METADATA:BEGIN -->
```json
{
  "schema_version": "stage5-math-gantt/1.0",
  "blueprint_version": "stage5-math-expansion/1.0",
  "blueprint_path": "Docs/Stage5_Math_Expansion_Blueprint.md",
  "gantt_path": "Docs/Stage5_Math_Expansion_Gantt.md",
  "blueprint_source_sha256": "de219c48de7e4989a1c295701eea1ffff73871b0d4869073847c828d4cc85ce8",
  "generated_at": "2026-08-13T14:27:17Z",
  "item_count": 12,
  "state_counts": {
    "not_started": 0,
    "awaiting_acceptance": 0,
    "accepted": 12
  },
  "schedule_basis": "no_authoritative_task_dates"
}
```
<!-- STAGE5-MATH-GANTT-METADATA:END -->

## Timing boundary

No task start, end, duration, or operator-frozen estimate is recorded in the Blueprint. The generation timestamp above describes this projection only and is not a task date. Document order and dependency depth are never converted into calendar claims.

## Recorded progress without schedule timing

| Item | State | Depends on | Planning | Blocking dependencies | Deliverables | Timing |
|---|---|---|---|---|---|---|
| `S5M-AUTH-001` | `accepted` | — | `accepted` | — | `Docs/catalog/v5/Stage5_Math_Expansion_Contract_v5.json` | `not_recorded` |
| `S5M-SCH-001` | `accepted` | `S5M-AUTH-001` | `accepted` | — | `Docs/catalog/v5/Math_Claim_Record_Schema_v5.json` | `not_recorded` |
| `S5M-BASE-001` | `accepted` | — | `accepted` | — | `Docs/tools/build_v4_import_receipt_v5.py`<br>`Docs/catalog/v5/V4_Import_Receipt_v5.json`<br>`scripts/test_v4_import_receipt_v5.py` | `not_recorded` |
| `S5M-ASSET-001` | `accepted` | `S5M-AUTH-001` | `accepted` | — | `Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz` | `not_recorded` |
| `S5M-EXT-001` | `accepted` | `S5M-ASSET-001` | `accepted` | — | `Docs/tools/extract_formal_conjectures_v5.py`<br>`scripts/test_extract_formal_conjectures_v5.py` | `not_recorded` |
| `S5M-SRC-001` | `accepted` | `S5M-AUTH-001`<br>`S5M-SCH-001`<br>`S5M-EXT-001` | `accepted` | — | `Docs/catalog/v5/Math_Source_Registry_v5.json` | `not_recorded` |
| `S5M-GEN-001` | `accepted` | `S5M-BASE-001`<br>`S5M-SCH-001`<br>`S5M-SRC-001` | `accepted` | — | `Docs/tools/generate_math_catalog_v5.py` | `not_recorded` |
| `S5M-REL-500` | `accepted` | `S5M-GEN-001` | `accepted` | — | `Docs/catalog/v5/releases/5.0` | `not_recorded` |
| `S5M-REL-510` | `accepted` | `S5M-REL-500` | `accepted` | — | `Docs/catalog/v5/releases/5.1` | `not_recorded` |
| `S5M-QA-001` | `accepted` | `S5M-REL-500`<br>`S5M-REL-510` | `accepted` | — | `scripts/check_math_catalog_v5.py`<br>`scripts/test_math_catalog_v5.py` | `not_recorded` |
| `S5M-READ-001` | `accepted` | `S5M-QA-001` | `accepted` | — | `Docs/catalog/v5/readable/5.0`<br>`Docs/catalog/v5/readable/5.1` | `not_recorded` |
| `S5M-REV-001` | `accepted` | `S5M-QA-001`<br>`S5M-READ-001` | `accepted` | — | `Docs/reviews/Stage5_Math_Expansion_Release_Review.md` | `not_recorded` |

## Unscheduled items

Every unfinished item without accepted timing evidence appears here exactly once as a task row.

_None._
