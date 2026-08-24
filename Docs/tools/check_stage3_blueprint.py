#!/usr/bin/env python3
"""Validate the Stage3 v3 authority and its generated monitoring surfaces."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import argparse
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT = ROOT / "Docs" / "Stage3_Blueprint.md"
STATUS = ROOT / "Docs" / "Stage3_Status.json"
KANBAN = ROOT / "Docs" / "Stage3_Kanban.md"
CLEANUP_RECEIPT = ROOT / "Docs" / "evidence" / "stage3_cleanup.json"
RELEASE_VALIDATION = ROOT / "Docs" / "evidence" / "stage3_release_validation.json"
RUNTIME_SNAPSHOT = ROOT / ".ops" / "stage3-execution-v1" / "status" / "runtime-snapshot.json"
CLEANUP_VERIFIER_SCRIPT = ROOT / "scripts" / "stage3_execution_cleanup.py"
PRE_CLEANUP_RECEIPT = ROOT / "Docs" / "evidence" / "stage3_pre_cleanup.json"
GAP_REVIEW = ROOT / "Docs" / "reviews" / "Stage3_Blueprint_Gap_Review_2026-08-10.md"
BOUND_SOURCE_REPORTS = (
    "Docs/reviews/THM-M-0387_Critical_Audit_2026-08-10.md",
    "Docs/reviews/THM_List_Benchmark_Audit_2026-08-10.md",
    "Docs/reviews/THM_Catalog_and_ID_Audit_2026-08-10.md",
)
V3_BOUND_REPORTS = (
    "Docs/reviews/Stage3_v3_18_Agent_Critical_Audit_2026-08-10.md",
    "Docs/reviews/Stage3_v2_to_v3_Semantic_Delta.md",
)

BEGIN = "<!-- STAGE3-EXECUTION-CHECKLIST:BEGIN -->"
END = "<!-- STAGE3-EXECUTION-CHECKLIST:END -->"
SPEC_BEGIN = "<!-- STAGE3-EXECUTION-SPEC:BEGIN -->"
SPEC_END = "<!-- STAGE3-EXECUTION-SPEC:END -->"
METADATA_BEGIN = "<!-- STAGE3-PROJECTION-METADATA:BEGIN -->"
METADATA_END = "<!-- STAGE3-PROJECTION-METADATA:END -->"
GANTT_MONITOR_BEGIN = "<!-- STAGE3-GANTT-MONITORING:BEGIN -->"
GANTT_MONITOR_END = "<!-- STAGE3-GANTT-MONITORING:END -->"

VERSION = "stage3-list-completion/3.0"
STATUS_SCHEMA = "stage3-execution-status/3.0"
PROJECTION_SCHEMA = "stage3-projection-metadata/3.0"
RUNTIME_SCHEMA = "stage3-runtime-snapshot/1.0"
CLEANUP_RECEIPT_SCHEMA = "stage3-cleanup-receipt/1.0"
PRE_CLEANUP_RECEIPT_SCHEMA = "stage3-pre-cleanup/1.0"
RELEASE_VALIDATION_SCHEMA = "stage3-release-validation/3.0"
EXECUTION_CONTRACT = "b3ehive-execution/1.5.0"

# The marked specification is executable input, not prose that may silently drift
# away from the controller/checker constants.  Keep the complete table closed and
# independently parse the operational subset into ``ExecutionSpec`` below.
EXPECTED_EXECUTION_SPEC_ROWS = {
    "canonical repository root": "runtime `git rev-parse --show-toplevel`; no absolute path is frozen in tracked files",
    "authoritative blueprint": "`Docs/Stage3_Blueprint.md`",
    "checklist markers": "`STAGE3-EXECUTION-CHECKLIST:BEGIN/END`",
    "stable item grammar": "`S3-(AUTH|ENV|AUD|CAT|MATH|PHY|CS|BEN|M38|EXE|REL)-[0-9]{3}`",
    "dependency source": "explicit checklist `depends_on=` only",
    "runtime root": "`.ops/stage3-execution-v1/`",
    "canonical runtime snapshot": "`.ops/stage3-execution-v1/status/runtime-snapshot.json`; authority and generator CLIs auto-read it when present and use runtime-unavailable only when absent",
    "task root": "`.ops/stage3-execution-v1/tasks/<claim-id>/<run-id>/`",
    "immutable handoff queue": "`.ops/stage3-execution-v1/queue/`",
    "durable claim launch release and retirement ledgers": "`.ops/stage3-execution-v1/ledgers/claims.json`, `.ops/stage3-execution-v1/ledgers/launch-attempts.json`, `.ops/stage3-execution-v1/ledgers/released-claims.json`, `.ops/stage3-execution-v1/ledgers/retired-process-identities.json`",
    "durable integration and repair ledgers": "`.ops/stage3-execution-v1/ledgers/integration.json`, `.ops/stage3-execution-v1/ledgers/repair.json`",
    "durable admission cursor and cleanup ledgers": "`.ops/stage3-execution-v1/ledgers/admission.json`, `.ops/stage3-execution-v1/ledgers/cursor.json`, `Docs/evidence/stage3_pre_cleanup.json`, `Docs/evidence/stage3_cleanup.json`",
    "durable ledger contract": "every controller ledger is schema-versioned and atomically replaced under its repository-local lock; every identity binds schema version, claim ID, run ID, task root, state, timestamps and specification digest, while Codex process identities additionally bind tmux socket/session, pane PID/start time, private CODEX_HOME, thread ID and goal ID",
    "selected agent": "interactive Codex TUI",
    "resolved route": "installed Codex default unless operator explicitly freezes model, effort or tier",
    "canonical writer": "Master only",
    "commit and push policy": "disabled unless both repository policy and explicit operator authorization require them; implicit commit, push, reset, stash or checkout is forbidden",
    "path conflict budget": "zero overlapping writable paths among admitted or integrating claims",
    "result schema": "`stage3-worker-result/1.0`",
    "Master receipt schema": "`stage3-master-acceptance/1.0`",
    "status schema": "`stage3-execution-status/3.0`",
    "same-name Gantt companion and rendering policy": "`Docs/Stage3_Gantt.md`; render recorded timestamps or operator-frozen estimates only and expose all other items as `Unscheduled`",
    "validation profiles": "authority, Lean environment, catalog/domain lists, benchmark release, M0387, controller portability, hygiene and deterministic regeneration gates defined in section 7 and checklist terminals",
    "artifact policy": "exact checklist ownership only; generated, test, evidence and release artifacts are permitted when their owning gate requires them; the sole post-checklist exception is controller-lifecycle output `Docs/evidence/stage3_cleanup.json`, written only from the accepted `S3-REL-005` arm by the frozen cleanup path and externally verified before projection; no other undeclared canonical writes",
    "completion surfaces": "Blueprint, Status, Kanban, Gantt, pre-cleanup arm and externally verified cleanup receipt",
    "execution skill build": "`b3ehive/1.5.0+codex.20260809210355`",
    "execution skill SHA256": "`0a69713f2e5432e62f7d49b5ae21846b0ae59b75b57e5081d8858bf7af8e3d2b`",
    "execution pattern SHA256": "`cdc52c9a36392270e61a3ea6bb81f10c55be918fc9d499e20d856c43ebcdf085`",
    "gate rules SHA256": "`604d9a8bb20f8485a556eea16c4a555acbcc57e38dc1c7fd29a0443ab76e1711`",
    "cadence": "two minutes only after explicit operator-authorized installation",
    "cron marker": "`# BEGIN AWESOME_THEOREMS_STAGE3_EXECUTION_V1` and matching END",
    "scheduler lease": "`.ops/stage3-execution-v1/locks/scheduler.lock`; short transactions only",
    "requested logical-claim ceiling": "six active logical claims; never permission to exceed measured headroom",
    "startup reservations": "four",
    "launch fanout": "two per wave, with repeated waves in one invocation",
    "authenticated-live and running-turn ceilings": "six each, counted independently from logical claims",
    "Master integrations": "one",
    "CPU validator leases": "four",
    "accelerator leases": "zero",
    "PID and process headroom": "admission requires at least 512 unused cgroup-or-host PID slots and records the measured limit, usage and source; `AT_STAGE3_MIN_PID_HEADROOM` may only raise the requirement without a Blueprint revision",
    "external-rate admission": "every configured provider or service limit has a fresh observed allow-or-block decision; missing required evidence blocks admission rather than silently shrinking the target",
    "startup hard deadline": "15 minutes, reducible by `AT_STAGE3_STARTUP_DEADLINE_SECONDS`",
    "authentication deadline": "10 minutes, reducible by `AT_STAGE3_AUTH_DEADLINE_SECONDS`",
    "admission-pump budget": "90 seconds, reducible by `AT_STAGE3_PUMP_BUDGET_SECONDS`",
    "no-progress guard": "three reconciliation iterations, reducible by `AT_STAGE3_NO_PROGRESS_ITERATIONS`",
}

CATEGORIES = ("AUTH", "ENV", "AUD", "CAT", "MATH", "PHY", "CS", "BEN", "M38", "EXE", "REL")
ITEM_PATTERN = rf"S3-(?:{'|'.join(CATEGORIES)})-[0-9]{{3}}"
ITEM_RE = re.compile(rf"^{ITEM_PATTERN}$")
ITEM_REF_RE = re.compile(ITEM_PATTERN)
ROW_RE = re.compile(
    rf"^- \[(?P<state>[ _x])\] `(?P<item>{ITEM_PATTERN})` "
    r"(?P<title>[^|]+?) \| depends_on=(?P<deps>[^|]+?) "
    r"\| owned_paths=(?P<paths>[^|]+?) \| gate=(?P<gate>.+)$"
)
HEX_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
RFC3339_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SAFE_RUNTIME_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}$")
SAFE_PATH_COMPONENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")

MONITOR_COLUMNS = (
    "Item",
    "State",
    "Depends on",
    "Owned paths",
    "Claim",
    "Run",
    "Owner",
    "Startup",
    "Live",
    "Running",
    "Handoff",
    "Integration",
    "Repair",
    "Planning blockers",
    "Runtime block",
    "Timing",
)
MONITOR_HEADER = "| " + " | ".join(MONITOR_COLUMNS) + " |"
MONITOR_SEPARATOR = "|" + "|".join("---" for _ in MONITOR_COLUMNS) + "|"

PROJECTION_METADATA_KEYS = {
    "schema_version",
    "blueprint_path",
    "blueprint_version",
    "gantt_path",
    "status_path",
    "kanban_path",
    "raw_blueprint_sha256",
    "execution_spec_region_sha256",
    "runtime_snapshot_sha256",
    "runtime_snapshot_id",
    "runtime_snapshot_path",
    "cleanup_receipt_path",
    "cleanup_receipt_sha256",
    "cleanup_receipt_id",
    "projection_input_sha256",
    "snapshot_id",
    "generated_at",
}
STATUS_TOP_LEVEL_KEYS = {
    "schema_version",
    "authority_note",
    "metadata",
    "counts",
    "planning",
    "runtime",
    "items",
}
STATUS_ITEM_KEYS = {
    "id",
    "state",
    "depends_on",
    "owned_paths",
    "claim",
    "run",
    "owner",
    "startup",
    "live",
    "running",
    "handoff",
    "integration",
    "repair",
    "planning_blockers",
    "runtime_block",
    "timing",
}
RUNTIME_TOP_LEVEL_KEYS = {
    "schema_version",
    "snapshot_id",
    "blueprint_version",
    "raw_blueprint_sha256",
    "execution_spec_region_sha256",
    "observed_at",
    "last_progress",
    "cleanup_state",
    "cleanup_arm",
    "admission",
    "items",
}
CLEANUP_RECEIPT_KEYS = {
    "schema_version",
    "receipt_id",
    "teardown_completed_at",
    "verified_at",
    "issued_at",
    "required_cadence_seconds",
    "blueprint_path",
    "blueprint_version",
    "raw_blueprint_sha256",
    "execution_spec_region_sha256",
    "all_checklist_items_master_accepted",
    "controller_identity",
    "verifier",
    "pre_cleanup",
    "unfinished",
    "queues_empty",
    "absence_recheck",
}
CLEANUP_PRE_REF_KEYS = {"path", "receipt_id", "sha256"}
PRE_CLEANUP_KEYS = {
    "schema_version",
    "receipt_id",
    "state",
    "armed_at",
    "blueprint_path",
    "blueprint_version",
    "raw_blueprint_sha256",
    "execution_spec_region_sha256",
    "rel005_state",
    "all_other_items_master_accepted",
    "unfinished",
    "queues_empty",
    "final_pre_teardown_projection",
    "teardown_inventory",
    "teardown_inventory_sha256",
}
PRE_CLEANUP_PROJECTION_KEYS = {
    "snapshot_id",
    "projection_input_sha256",
    "generated_at",
    "surfaces",
    "runtime_snapshot",
}
RELEASE_VALIDATION_KEYS = {
    "schema_version",
    "receipt_id",
    "blueprint_version",
    "raw_blueprint_sha256",
    "execution_spec_region_sha256",
    "acceptance_contract_sha256",
    "accepted_repository_merkle",
    "item_master_receipts",
    "matrix_runs",
    "all_passed",
}
REPOSITORY_MERKLE_KEYS = {"algorithm", "entry_count", "sha256"}
MATRIX_RUN_KEYS = {
    "runner_id",
    "network",
    "cache",
    "argv_sha256",
    "inputs_sha256",
    "outputs_sha256",
    "raw_log_sha256",
    "exit_code",
    "passed",
}
PRE_CLEANUP_SURFACE_NAMES = {"gantt", "status", "kanban"}
PRE_CLEANUP_SURFACE_KEYS = {"path", "sha256", "text"}
PRE_CLEANUP_RUNTIME_KEYS = {"path", "snapshot_id", "sha256", "text"}
CLEANUP_UNFINISHED_KEYS = {"not_done", "self_tested"}
CLEANUP_QUEUE_KEYS = {"handoff", "integration", "repair", "checkpoint"}
CLEANUP_ABSENCE_KEYS = {
    "cron",
    "scheduler",
    "task_processes",
    "tmux_sockets",
    "locks",
    "runtime_root",
}
CLEANUP_CONTROLLER_KEYS = {"runtime_root", "cron_begin_marker", "cron_end_marker"}
CLEANUP_VERIFIER_KEYS = {
    "identity",
    "independent_of_controller",
    "script_path",
    "script_sha256",
    "commands",
}
CLEANUP_COMMAND_KEYS = {
    "argv",
    "cwd",
    "started_at",
    "finished_at",
    "exit_code",
    "stdout",
    "stdout_sha256",
    "stdout_payload_sha256",
    "stderr",
    "stderr_sha256",
}
CLEANUP_ABSENCE_EVIDENCE_KEYS = {"query", "targets", "raw_result", "absent"}
CLEANUP_VERIFIER_OUTPUT_KEYS = {
    "schema_version", "controller_identity", "observed_at", "inventory_sha256", "queries"
}
CLEANUP_QUERY_NAMES = {
    "cron": "exact_cron_marker_entries",
    "scheduler": "recorded_scheduler_processes",
    "task_processes": "recorded_task_processes",
    "tmux_sockets": "controller_tmux_sockets",
    "locks": "controller_lock_paths",
    "runtime_root": "runtime_root_lstat",
}
ADMISSION_KEYS = {
    "logical_claim_target",
    "startup_reservation_target",
    "authenticated_live_target",
    "running_turn_target",
    "admitted_target",
    "eligible_ready_count",
    "requested_target",
    "host_admissible_target",
    "master_integration_target",
    "cpu_validator_lease_target",
    "active_cpu_validator_leases",
    "effective_target_bindings",
    "underfill_stop_reason",
    "occupancy_underfill_reason",
}
EFFECTIVE_BINDING_KEYS = {"kind", "limit", "reason", "evidence"}
EFFECTIVE_BINDING_EVIDENCE_KEYS = {"source", "payload", "sha256"}
EFFECTIVE_BINDING_KINDS = {
    "logical_cap",
    "logical_available",
    "authenticated_live_cap",
    "running_turn_cap",
    "eligible",
    "requested",
    "host_resource",
    "conflict",
    "external_limit",
    "route",
    "validator",
    "budget",
}
RUNTIME_ITEM_KEYS = {
    "id",
    "claim_id",
    "run_id",
    "owner",
    "observation_evidence",
    "startup",
    "startup_evidence",
    "live",
    "live_evidence",
    "running",
    "handoff",
    "integration",
    "repair",
    "runtime_block",
    "timing",
}
OBSERVATION_EVIDENCE_KEYS = {"source", "sha256", "observed_at", "payload"}
STARTUP_EVIDENCE_KEYS = {
    "state_entered_at",
    "deadline_at",
    "identity_evidence_sha256",
    "process_identity",
}
STARTUP_PROCESS_KEYS = {
    "tmux_socket",
    "session",
    "pane_pid",
    "process_start_ticks",
    "cwd",
    "codex_home",
    "observed_at",
    "alive",
}
LIVE_EVIDENCE_KEYS = {
    "authenticated_at",
    "identity_evidence_sha256",
    "tmux_socket",
    "session",
    "pane_pid",
    "process_start_ticks",
    "cwd",
    "codex_home",
    "thread_id",
    "goal_id",
    "goal_status",
    "goal_item_id",
    "goal_claim_id",
    "goal_objective",
    "route",
    "route_sha256",
    "process_observed_at",
    "process_alive",
}
LIVE_ROUTE_KEYS = {"provider", "model", "reasoning_effort", "service_tier"}
TIMING_KEYS = {"status", "start", "end", "duration_seconds", "source"}
TIMING_SOURCE_KEYS = {"path", "payload", "sha256"}
TIMING_SOURCE_PAYLOAD_KEYS = {"start", "end", "duration_seconds"}

STARTUP_STATES = {"reserved", "materialized", "tmux_started", "goal_pasted", "goal_submitted"}
HANDOFF_STATES = {"handoff_ready", "harvested", "finished"}
INTEGRATION_STATES = {"queued", "integrating", "accepted", "failed"}
REPAIR_STATES = {"queued", "active", "resolved", "exhausted"}
RUNTIME_BLOCK_KINDS = {
    "dependency",
    "conflict",
    "startup",
    "resource",
    "external_limit",
    "route",
    "validator",
    "budget",
}
UNDERFILL_KINDS = RUNTIME_BLOCK_KINDS | {"no_progress", "invocation_deadline"}
STOP_REASON_KEYS = {"kind", "reason", "evidence"}
STOP_REASON_EVIDENCE_KEYS = {"source", "payload", "sha256"}
RUNTIME_CLEANUP_STATES = {"not_started", "cleanup_pending", "teardown", "awaiting_absence_recheck"}
CLEANUP_ARM_KEYS = {"path", "receipt_id", "sha256"}
MUTABLE_CHECKBOX_RE = re.compile(r"^ {0,3}(?:[-+*]|\d+[.)])\s+\[[ _xX]\](?:\s|$)", re.MULTILINE)
ANY_INDENT_CHECKBOX_RE = re.compile(
    r"^[ \t]*(?:>[ \t]*)*(?:[-+*]|\d+[.)])\s+\[[ _xX]\](?:\s|$)"
)
KANBAN_RUNTIME_FIELDS = (
    "logical_claims",
    "reserved",
    "starting",
    "authenticated_live_goals",
    "running_turns",
    "finished_handoffs",
    "dependency_blocked",
    "conflict_blocked",
    "startup_blocked",
    "resource_blocked",
    "external_limit_blocked",
    "route_blocked",
    "validator_blocked",
    "budget_blocked",
    "integration_backlog",
    "repair_backlog",
    "logical_claim_target",
    "startup_reservation_target",
    "authenticated_live_target",
    "running_turn_target",
    "admitted_target",
    "eligible_ready_count",
    "requested_target",
    "host_admissible_target",
    "master_integration_target",
    "cpu_validator_lease_target",
    "active_cpu_validator_leases",
    "effective_target_bindings",
    "logical_saturation",
    "admitted_saturation",
    "underfill_stop_reason",
    "occupancy_underfill_reason",
)

REQUIRED_BLUEPRINT_PHRASES = (
    "sole current Stage3 execution blueprint and checklist authority",
    "Blueprint version: `stage3-list-completion/3.0`",
    "Execution contract: `b3ehive-execution/1.5.0`",
    "status schema | `stage3-execution-status/3.0`",
    "complete_relative_to_manifest",
    "ATO  Awesome Theorems Occurrence",
    "ATF  Awesome Theorems Family",
    "ATS  Awesome Theorems Sense",
    "ATV  Awesome Theorems Variant",
    "ATR  Awesome Theorems Relation",
    "ATL  Awesome Theorems Leakage",
    "The Gantt is a read-only schedule plus Kanban monitoring projection",
    "raw Blueprint SHA256",
    "runtime snapshot SHA256 or explicit absence",
    "all current items remain",
    "visible `Unscheduled` state",
    "Status and Kanban are replaced first and",
    "Gantt last through same-directory atomic replacement",
    "WORKER_TRANSPORT=tmux_codex_tui",
    "WORKER_GOAL_COMMAND=/goal",
    "APP_SERVER_WORKERS=forbidden",
    "CODEX_PROCESS_ISOLATION=one_process_tree_per_claim",
    "CODEX_STATE_ISOLATION=one_writable_home_per_claim",
    "exactly one authenticated active\n`/goal` per claim",
    ".ops/stage3-execution-v1/tasks/<claim-id>/<run-id>/",
    "Harvest a checksum-valid per-item result and patch into immutable queue storage before stale pruning",
    "zero `[ ]`, zero `[_]`",
    "root_machine_closed=false",
    "theorem_complete=false",
)

REQUIRED_TERMINALS = {
    "S3-ENV-009",
    "S3-ENV-008",
    "S3-CAT-016",
    "S3-CAT-013",
    "S3-MATH-020",
    "S3-PHY-019",
    "S3-CS-025",
    "S3-BEN-021",
    "S3-BEN-015",
    "S3-M38-039",
    "S3-M38-041",
    "S3-M38-034",
    "S3-M38-066",
    "S3-EXE-015",
    "S3-REL-006",
    "S3-REL-005",
}
BOOTSTRAP_ACCEPTED_IDS = {
    "S3-AUTH-001",
    "S3-ENV-001",
    "S3-ENV-002",
    "S3-AUD-001",
    "S3-AUD-002",
    "S3-AUD-003",
    "S3-AUD-004",
    "S3-AUD-005",
}

# A long sentence is not a semantic contract.  These closed clause tokens are
# deliberately redundant with the Blueprint so weakening one of the v3 P0
# gates cannot be hidden behind a self-consistent projection regeneration.
REQUIRED_ITEM_CONTRACTS = {
    "S3-AUTH-002": ("exact append-only item manifest", "item-to-validator-fixture-artifact", "current accepted-tree membership"),
    "S3-AUTH-004": ("repository owner explicitly chooses", "without inventing MIT Apache"),
    "S3-AUD-005": ("exactly three groups of six", "98-key denominator", "miniF2F"),
    "S3-CAT-001": ("all98 legacy review keys", "62 missing plus36 present-collision"),
    "S3-CAT-003": ("real locks atomic create fsync", "crash two-writer ABA", "no default or evidence inheritance"),
    "S3-CAT-004": ("identity ATR edges and leakage ATL components remain separate", "container co-residence", "giant-component percolation"),
    "S3-CAT-007": ("every material-status truth-apt current ATV", "role-specific exact-variant-applicable", "proved refuted open partial independent conditional or disputed"),
    "S3-CAT-010": ("pre-curation", "zero novel leakage candidate", "two consecutive identical"),
    "S3-CAT-012": ("exactly one current material-status ID set", "Historical_Claim_Name_Index_v3"),
    "S3-CAT-014": ("62 missing plus36 present-collision", "never by itself allocates a claim ID"),
    "S3-CAT-015": ("active redirect split and retired", "crash concurrent writer ABA"),
    "S3-CAT-016": ("post-curation", "zero owner gap or duplication", "accepted-candidate descendants"),
    "S3-PHY-001": ("210 source-category and208 survivor-category",),
    "S3-PHY-022": ("method device dataset framework definition aggregate or nonclaim",),
    "S3-PHY-025": ("final physics-owned current ID set", "every truth-apt member equals one current material-status bucket"),
    "S3-CS-026": ("all398 v2 proposals", "finite testing empirical performance bounded model checking"),
    "S3-BEN-016": ("exactly ingested training-only contamination-reference comparator-only or excluded", "unknown training visibility"),
    "S3-BEN-017": ("executable candidate ABI", "every benchmark-eligible domain record maps to tasks or typed exclusions"),
    "S3-BEN-018": ("equivalent non_equivalent or undecided", "affine and logarithmic scales", "near-zero tolerances"),
    "S3-BEN-019": ("special and interactive judge", "cannot upgrade universal correctness"),
    "S3-BEN-020": ("every prospective release byte maps exactly once", "physically separated"),
    "S3-BEN-021": ("candidate output decision scorer trace metric", "pack rebuild or scorer-only replay cannot substitute"),
    "S3-M38-012": ("StatementAndReductionPath.lean", "S1_M_001.lean", "S1_M_022.lean"),
    "S3-M38-035": ("propext Classical.choice and Quot.sound", "native_decide"),
    "S3-M38-036": ("complete module public-declaration and root census", "cannot shrink the denominator"),
    "S3-M38-038": ("deny-by-default descendant-process sandbox", "warm_shared warm_private cache_restored cold_compile"),
    "S3-M38-039": ("leanchecker", "trust-zero", "source-olean mismatch"),
    "S3-M38-040": ("dossier rev-5.6 Stage1 registry and Stage3 registry", "many-to-many spaces"),
    "S3-M38-041": ("exclusive-create fsync and CAS", "held-out-zero"),
    "S3-M38-042": ("two independent mathematical checks", "three-five-trick"),
    "S3-EXE-008": ("content-addressed Master receipt", "integrated tree membership Merkle", "direct checkbox edit"),
    "S3-EXE-013": ("item-to-clause-to-validator-to-fixture-to-artifact", "post-accept proof deletion and Prop mutation"),
    "S3-REL-002": ("exact REL-006 argv matrix", "accepted repository membership Merkle"),
    "S3-REL-006": ("exact argv cwd validator and fixture hashes", "deleted proofs changed Props", "rather than trusting all-x prose or cleanup alone"),
}


class ValidationError(ValueError):
    """The Stage3 authority or generated projection violates its contract."""


@dataclass(frozen=True)
class Task:
    item_id: str
    state: str
    title: str
    dependencies: tuple[str, ...]
    owned_paths: tuple[str, ...]
    gate: str
    line_number: int


@dataclass(frozen=True)
class ExecutionSpec:
    """Typed operational fields parsed from the closed marked specification."""

    rows: dict[str, str]
    authoritative_blueprint: str
    runtime_root: str
    runtime_snapshot: str
    task_root_template: str
    scheduler_lock: str
    pre_cleanup_receipt: str
    cleanup_receipt: str
    result_schema: str
    master_receipt_schema: str
    status_schema: str
    gantt_path: str
    skill_build: str
    skill_sha256: str
    pattern_sha256: str
    gate_rules_sha256: str
    cadence_seconds: int
    logical_claim_ceiling: int
    startup_reservations: int
    launch_fanout: int
    authenticated_live_ceiling: int
    running_turn_ceiling: int
    master_integrations: int
    cpu_validator_leases: int
    accelerator_leases: int
    startup_deadline_seconds: int
    authentication_deadline_seconds: int
    admission_pump_budget_seconds: int
    no_progress_iterations: int


_NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}


def _first_backtick(value: str, label: str) -> str:
    match = re.search(r"`([^`]+)`", value)
    if match is None:
        raise ValidationError(f"execution specification {label} lacks a code value")
    return match.group(1)


def _leading_word_number(value: str, label: str) -> int:
    word = value.split(None, 1)[0]
    if word not in _NUMBER_WORDS:
        raise ValidationError(f"execution specification {label} lacks a supported numeric value")
    return _NUMBER_WORDS[word]


def _leading_decimal(value: str, unit: str, label: str) -> int:
    match = re.fullmatch(rf"(?P<number>[0-9]+) {re.escape(unit)}(?:, .+)?", value)
    if match is None:
        raise ValidationError(f"execution specification {label} has malformed {unit}")
    return int(match.group("number"))


def parse_execution_spec(blueprint_text: str) -> ExecutionSpec:
    """Parse and freeze the exact-key Stage3 execution-specification table."""

    region = exact_marked_region(
        blueprint_text, SPEC_BEGIN, SPEC_END, "execution specification"
    ).splitlines()[1:-1]
    header = "| Field | Stage3 value |"
    if region.count(header) != 1:
        raise ValidationError("execution specification must contain one canonical field table")
    table_start = region.index(header)
    if table_start + 2 >= len(region) or region[table_start + 1] != "|---|---|":
        raise ValidationError("execution specification must be one canonical two-column table")
    table_lines: list[str] = []
    for line in region[table_start + 2 :]:
        if not line.startswith("|"):
            break
        table_lines.append(line)
    rows: dict[str, str] = {}
    for offset, line in enumerate(table_lines, start=1):
        match = re.fullmatch(r"\| (?P<field>[^|]+?) \| (?P<value>.*) \|", line)
        if match is None:
            raise ValidationError(f"execution specification row {offset} is malformed")
        field = match.group("field")
        if field in rows:
            raise ValidationError(f"execution specification repeats field {field}")
        rows[field] = match.group("value")
    if set(rows) != set(EXPECTED_EXECUTION_SPEC_ROWS):
        raise ValidationError(
            "execution specification fields differ: "
            f"missing={sorted(set(EXPECTED_EXECUTION_SPEC_ROWS) - set(rows))}, "
            f"extra={sorted(set(rows) - set(EXPECTED_EXECUTION_SPEC_ROWS))}"
        )
    for field, expected in EXPECTED_EXECUTION_SPEC_ROWS.items():
        if rows[field] != expected:
            raise ValidationError(f"execution specification value differs for {field}")

    cleanup_paths = re.findall(r"`([^`]+)`", rows["durable admission cursor and cleanup ledgers"])
    if len(cleanup_paths) != 4:
        raise ValidationError("execution specification cleanup ledger paths are malformed")
    live_running = rows["authenticated-live and running-turn ceilings"]
    live_word = live_running.split(None, 1)[0]
    live_ceiling = _NUMBER_WORDS.get(live_word)
    if live_ceiling is None or not live_running.startswith(f"{live_word} each"):
        raise ValidationError("execution specification live/running ceilings are malformed")
    skill_sha = _first_backtick(rows["execution skill SHA256"], "execution skill SHA256")
    pattern_sha = _first_backtick(rows["execution pattern SHA256"], "execution pattern SHA256")
    rules_sha = _first_backtick(rows["gate rules SHA256"], "gate rules SHA256")
    if any(not HEX_SHA256_RE.fullmatch(value) for value in (skill_sha, pattern_sha, rules_sha)):
        raise ValidationError("execution specification contains a malformed reference SHA256")
    return ExecutionSpec(
        rows=rows,
        authoritative_blueprint=_first_backtick(rows["authoritative blueprint"], "authoritative blueprint"),
        runtime_root=_first_backtick(rows["runtime root"], "runtime root"),
        runtime_snapshot=_first_backtick(rows["canonical runtime snapshot"], "canonical runtime snapshot"),
        task_root_template=_first_backtick(rows["task root"], "task root"),
        scheduler_lock=_first_backtick(rows["scheduler lease"], "scheduler lease"),
        pre_cleanup_receipt=cleanup_paths[2],
        cleanup_receipt=cleanup_paths[3],
        result_schema=_first_backtick(rows["result schema"], "result schema"),
        master_receipt_schema=_first_backtick(rows["Master receipt schema"], "Master receipt schema"),
        status_schema=_first_backtick(rows["status schema"], "status schema"),
        gantt_path=_first_backtick(
            rows["same-name Gantt companion and rendering policy"], "same-name Gantt companion"
        ),
        skill_build=_first_backtick(rows["execution skill build"], "execution skill build"),
        skill_sha256=skill_sha,
        pattern_sha256=pattern_sha,
        gate_rules_sha256=rules_sha,
        cadence_seconds=_leading_word_number(rows["cadence"], "cadence") * 60,
        logical_claim_ceiling=_leading_word_number(
            rows["requested logical-claim ceiling"], "requested logical-claim ceiling"
        ),
        startup_reservations=_leading_word_number(rows["startup reservations"], "startup reservations"),
        launch_fanout=_leading_word_number(rows["launch fanout"], "launch fanout"),
        authenticated_live_ceiling=live_ceiling,
        running_turn_ceiling=live_ceiling,
        master_integrations=_leading_word_number(rows["Master integrations"], "Master integrations"),
        cpu_validator_leases=_leading_word_number(rows["CPU validator leases"], "CPU validator leases"),
        accelerator_leases=_leading_word_number(rows["accelerator leases"], "accelerator leases"),
        startup_deadline_seconds=_leading_decimal(
            rows["startup hard deadline"], "minutes", "startup hard deadline"
        ) * 60,
        authentication_deadline_seconds=_leading_decimal(
            rows["authentication deadline"], "minutes", "authentication deadline"
        ) * 60,
        admission_pump_budget_seconds=_leading_decimal(
            rows["admission-pump budget"], "seconds", "admission-pump budget"
        ),
        no_progress_iterations=_leading_word_number(rows["no-progress guard"], "no-progress guard"),
    )


def gantt_companion_path(blueprint: Path) -> Path:
    """Apply the execution-skill terminal Blueprint -> Gantt naming rule."""

    stem = blueprint.stem
    if stem.endswith("Blueprint"):
        stem = stem[: -len("Blueprint")] + "Gantt"
    else:
        stem += "_Gantt"
    return blueprint.with_name(stem + blueprint.suffix)


GANTT = gantt_companion_path(BLUEPRINT)


def _parse_csv(value: str, label: str, item_id: str) -> tuple[str, ...]:
    value = value.strip()
    if value == "-":
        return ()
    parts = tuple(part.strip() for part in value.split(","))
    if not parts or any(not part for part in parts):
        raise ValidationError(f"{item_id}: malformed {label}")
    if len(parts) != len(set(parts)):
        raise ValidationError(f"{item_id}: duplicate value in {label}")
    return parts


def _validate_owned_path(path: str, item_id: str) -> None:
    if "\\" in path:
        raise ValidationError(f"{item_id}: owned path must use repository-relative POSIX syntax")
    candidate = PurePosixPath(path)
    if candidate.is_absolute() or not candidate.parts or ".." in candidate.parts:
        raise ValidationError(f"{item_id}: owned path escapes the repository: {path}")
    if candidate.as_posix() != path:
        raise ValidationError(f"{item_id}: owned path is not canonical repository-relative POSIX: {path}")
    if candidate.parts[0] in {".git", ".ops", ".cron"}:
        raise ValidationError(f"{item_id}: tracked deliverable may not use runtime storage: {path}")
    if any(part in {"*", "**"} or "<" in part or ">" in part for part in candidate.parts):
        raise ValidationError(f"{item_id}: owned path contains a glob or placeholder: {path}")


def _validate_runtime_path(path: Any, label: str) -> str:
    if not isinstance(path, str) or "\\" in path:
        raise ValidationError(f"{label} must be a canonical runtime-relative POSIX path")
    candidate = PurePosixPath(path)
    if (
        candidate.is_absolute()
        or candidate.as_posix() != path
        or ".." in candidate.parts
        or len(candidate.parts) < 2
        or candidate.parts[:2] != (".ops", "stage3-execution-v1")
    ):
        raise ValidationError(f"{label} escapes the frozen Stage3 runtime root")
    return path


def _one_region(text: str, begin_marker: str, end_marker: str, label: str) -> tuple[int, int, list[str]]:
    if text.count(begin_marker) != 1 or text.count(end_marker) != 1:
        raise ValidationError(f"{label} must contain exactly one marker pair")
    lines = text.splitlines()
    begin = next(index for index, line in enumerate(lines) if line == begin_marker)
    end = next(index for index, line in enumerate(lines) if line == end_marker)
    if end <= begin:
        raise ValidationError(f"{label} end marker precedes begin marker")
    return begin, end, lines


def exact_marked_region(text: str, begin_marker: str, end_marker: str, label: str) -> str:
    """Return the exact inclusive marker region used for content hashing."""

    if text.count(begin_marker) != 1 or text.count(end_marker) != 1:
        raise ValidationError(f"{label} must contain exactly one marker pair")
    begin = text.index(begin_marker)
    end = text.index(end_marker, begin) + len(end_marker)
    if end <= begin:
        raise ValidationError(f"{label} marker order is invalid")
    return text[begin:end]


def parse_tasks(blueprint_text: str) -> dict[str, Task]:
    begin, end, lines = _one_region(blueprint_text, BEGIN, END, "blueprint checklist")
    for index, line in enumerate(lines):
        in_region = begin < index < end
        competing = ANY_INDENT_CHECKBOX_RE.match(line)
        if competing and (not in_region or ROW_RE.fullmatch(line) is None):
            raise ValidationError(
                f"line {index + 1}: noncanonical or competing mutable checkbox outside the sole cursor grammar"
            )
    tasks: dict[str, Task] = {}
    for index in range(begin + 1, end):
        line = lines[index]
        if not line:
            continue
        match = ROW_RE.fullmatch(line)
        if match is None:
            raise ValidationError(f"line {index + 1}: malformed or unsupported checklist row")
        item_id = match.group("item")
        if item_id in tasks:
            raise ValidationError(f"duplicate checklist item ID: {item_id}")
        dependencies = _parse_csv(match.group("deps"), "depends_on", item_id)
        paths = _parse_csv(match.group("paths"), "owned_paths", item_id)
        for path in paths:
            _validate_owned_path(path, item_id)
        gate = match.group("gate").strip()
        if len(gate) < 40:
            raise ValidationError(f"{item_id}: acceptance gate is not concrete")
        tasks[item_id] = Task(
            item_id=item_id,
            state=match.group("state"),
            title=match.group("title").strip(),
            dependencies=dependencies,
            owned_paths=paths,
            gate=gate,
            line_number=index + 1,
        )
    if not tasks:
        raise ValidationError("authoritative checklist is empty")
    return tasks


def _ancestors(tasks: dict[str, Task], item_id: str) -> set[str]:
    result: set[str] = set()
    pending = list(tasks[item_id].dependencies)
    while pending:
        dependency = pending.pop()
        if dependency in result:
            continue
        result.add(dependency)
        pending.extend(tasks[dependency].dependencies)
    return result


def validate_graph(tasks: dict[str, Task]) -> None:
    categories = {item_id.split("-")[1] for item_id in tasks}
    if categories != set(CATEGORIES):
        raise ValidationError(f"checklist categories differ: expected={CATEGORIES}, got={sorted(categories)}")
    if not REQUIRED_TERMINALS.issubset(tasks):
        raise ValidationError(f"required terminal items missing: {sorted(REQUIRED_TERMINALS - set(tasks))}")
    expected_by_category = {
        "AUTH": {f"S3-AUTH-{number:03d}" for number in range(1, 5)},
        "ENV": {f"S3-ENV-{number:03d}" for number in range(1, 10)},
        "AUD": {f"S3-AUD-{number:03d}" for number in range(1, 6)},
        "CAT": {f"S3-CAT-{number:03d}" for number in range(1, 17)},
        "MATH": {f"S3-MATH-{number:03d}" for number in range(1, 23)},
        "PHY": {f"S3-PHY-{number:03d}" for number in range(1, 26)},
        "CS": {f"S3-CS-{number:03d}" for number in range(1, 27)},
        "BEN": {f"S3-BEN-{number:03d}" for number in range(1, 22)},
        "M38": {f"S3-M38-{number:03d}" for number in range(1, 43)}
        | {f"S3-M38-{number:03d}" for number in range(60, 67)},
        "EXE": {f"S3-EXE-{number:03d}" for number in range(1, 16)},
        "REL": {f"S3-REL-{number:03d}" for number in range(1, 7)},
    }
    expected_ids = set().union(*expected_by_category.values())
    if set(tasks) != expected_ids:
        raise ValidationError(
            "Stage3 v3 stable item manifest differs: "
            f"missing={sorted(expected_ids - set(tasks))}, extra={sorted(set(tasks) - expected_ids)}"
        )
    for task in tasks.values():
        for dependency in task.dependencies:
            if not ITEM_RE.fullmatch(dependency) or dependency not in tasks:
                raise ValidationError(f"{task.item_id}: missing or malformed dependency {dependency}")
            if dependency == task.item_id:
                raise ValidationError(f"{task.item_id}: self dependency")
        if task.state in {"_", "x"}:
            incomplete = [dependency for dependency in task.dependencies if tasks[dependency].state != "x"]
            if incomplete:
                raise ValidationError(f"{task.item_id}: advanced state has unfinished dependencies {incomplete}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(item_id: str, trail: tuple[str, ...]) -> None:
        if item_id in visiting:
            raise ValidationError("dependency cycle: " + " -> ".join((*trail, item_id)))
        if item_id in visited:
            return
        visiting.add(item_id)
        for dependency in tasks[item_id].dependencies:
            visit(dependency, (*trail, item_id))
        visiting.remove(item_id)
        visited.add(item_id)

    for item_id in sorted(tasks):
        visit(item_id, ())

    if tasks["S3-REL-004"].dependencies != ("S3-EXE-015", "S3-ENV-002", "S3-AUD-005"):
        raise ValidationError(
            "S3-REL-004 must depend exactly on S3-EXE-015, S3-ENV-002, and S3-AUD-005"
        )
    for item_id in ("S3-ENV-003", "S3-CAT-001", "S3-BEN-001", "S3-M38-001"):
        if "S3-REL-004" not in tasks[item_id].dependencies:
            raise ValidationError(f"{item_id} must directly depend on S3-REL-004")
    required_release_join = {"S3-CAT-013", "S3-BEN-015", "S3-M38-034", "S3-ENV-008", "S3-REL-004"}
    if not required_release_join.issubset(tasks["S3-REL-001"].dependencies):
        raise ValidationError("S3-REL-001 does not join every release terminal and activation gate")
    if tasks["S3-REL-002"].dependencies != ("S3-REL-006",):
        raise ValidationError("S3-REL-002 must depend exactly on the frozen terminal matrix")
    if not {"S3-AUTH-002", "S3-AUD-005", "S3-REL-001"}.issubset(tasks["S3-REL-006"].dependencies):
        raise ValidationError("S3-REL-006 must bind authority, the v3 audit, and the release join")
    if not {"S3-REL-002", "S3-AUD-005"}.issubset(tasks["S3-REL-003"].dependencies):
        raise ValidationError("S3-REL-003 must include release validation and the v3 audit input")
    if tasks["S3-REL-005"].dependencies != ("S3-REL-003",):
        raise ValidationError("S3-REL-005 must depend exactly on S3-REL-003")
    expected_ancestors = set(tasks) - {"S3-REL-005"}
    actual_ancestors = _ancestors(tasks, "S3-REL-005")
    if actual_ancestors != expected_ancestors:
        missing = sorted(expected_ancestors - actual_ancestors)
        extra = sorted(actual_ancestors - expected_ancestors)
        raise ValidationError(f"S3-REL-005 ancestry does not cover all other IDs: missing={missing}, extra={extra}")
    if not {"S3-AUD-004", "S3-AUD-005", "S3-M38-023"}.issubset(tasks["S3-M38-029"].dependencies):
        raise ValidationError("S3-M38-029 must directly include both audits and S3-M38-023")
    if not {"S3-ENV-006", "S3-ENV-007"}.issubset(tasks["S3-M38-033"].dependencies):
        raise ValidationError("S3-M38-033 must include both isolated environment gates")
    if not {"S3-M38-039", "S3-M38-041", "S3-M38-066", "S3-ENV-008"}.issubset(tasks["S3-M38-034"].dependencies):
        raise ValidationError("S3-M38-034 must include cold-kernel, rights, six-review, and environment acceptance")
    if not {"S3-M38-019", "S3-M38-021"}.issubset(tasks["S3-ENV-005"].dependencies):
        raise ValidationError("S3-ENV-005 must depend on the independent evidence and replay checkers")
    if not {"S3-CAT-010", "S3-MATH-016", "S3-PHY-015", "S3-CS-022"}.issubset(tasks["S3-CAT-016"].dependencies):
        raise ValidationError("S3-CAT-016 must be the post-curation fixed point")
    if "S3-CAT-016" not in tasks["S3-CAT-011"].dependencies:
        raise ValidationError("S3-CAT-011 must consume the post-curation registry")
    if "S3-BEN-021" not in tasks["S3-BEN-014"].dependencies:
        raise ValidationError("S3-BEN-014 must consume sealed evaluation-run replay")
    expected_reviews = {f"S3-M38-{number:03d}" for number in range(60, 66)}
    if set(tasks["S3-M38-066"].dependencies) != expected_reviews or len(tasks["S3-M38-066"].dependencies) != 6:
        raise ValidationError("M0387 Master review gate must depend on exactly six review receipts")
    pointer = "THM-M-0387/receipts/current-validation.json"
    pointer_owners = [task.item_id for task in tasks.values() if pointer in task.owned_paths]
    if pointer_owners != ["S3-M38-034"]:
        raise ValidationError(f"only S3-M38-034 may own the current-validation pointer: {pointer_owners}")
    for item_id, clauses in REQUIRED_ITEM_CONTRACTS.items():
        task = tasks[item_id]
        contract_text = " ".join((task.title, *task.owned_paths, task.gate))
        missing_clauses = [clause for clause in clauses if clause not in contract_text]
        if missing_clauses:
            raise ValidationError(f"{item_id}: v3 contract clauses missing: {missing_clauses}")


def validate_ownership(tasks: dict[str, Task]) -> None:
    owners: dict[str, str] = {}
    for task in tasks.values():
        for path in task.owned_paths:
            if path in owners:
                raise ValidationError(f"owned path repeated by {owners[path]} and {task.item_id}: {path}")
            owners[path] = task.item_id
    paths = sorted(owners)
    for index, parent in enumerate(paths):
        prefix = parent.rstrip("/") + "/"
        for child in paths[index + 1 :]:
            if child.startswith(prefix):
                raise ValidationError(
                    f"owned path prefix overlap: {owners[parent]} owns {parent}; "
                    f"{owners[child]} owns {child}"
                )


def validate_gap_review_source_reports(
    gap_review_text: str,
    source_report_bytes: dict[str, bytes],
) -> None:
    """Validate the AUD-004 synthesis' closed, content-addressed source table."""

    lines = gap_review_text.splitlines()
    header = "| Source report | SHA-256 |"
    if lines.count(header) != 1:
        raise ValidationError("AUD-004 gap review must contain exactly one source-report digest table")
    start = lines.index(header)
    if start + 1 >= len(lines) or lines[start + 1] != "|---|---|":
        raise ValidationError("AUD-004 source-report table separator differs")
    rows: list[tuple[str, str]] = []
    index = start + 2
    while index < len(lines) and lines[index].startswith("|"):
        match = re.fullmatch(r"\| `(?P<path>[^`]+)` \| `(?P<digest>[0-9a-f]{64})` \|", lines[index])
        if match is None:
            raise ValidationError("AUD-004 source-report table contains a malformed row")
        rows.append((match.group("path"), match.group("digest")))
        index += 1
    paths = [path for path, _digest in rows]
    if len(paths) != len(set(paths)):
        raise ValidationError("AUD-004 source-report table repeats a path")
    if tuple(paths) != BOUND_SOURCE_REPORTS:
        raise ValidationError("AUD-004 source-report table paths/order differ from the frozen inputs")
    if set(source_report_bytes) != set(BOUND_SOURCE_REPORTS):
        raise ValidationError("AUD-004 source-report byte inputs differ from the exact frozen path set")
    for path, recorded_digest in rows:
        actual_digest = sha256_bytes(source_report_bytes[path])
        if recorded_digest != actual_digest:
            raise ValidationError(f"AUD-004 source-report digest is stale for {path}")


def validate_v3_bound_reports(
    blueprint_text: str,
    report_bytes: dict[str, bytes],
) -> None:
    """Bind the eighteen-agent audit and its semantic delta into the authority."""

    lines = blueprint_text.splitlines()
    header = "| V3 bound review input | SHA-256 |"
    if lines.count(header) != 1:
        raise ValidationError("Blueprint must contain exactly one v3 bound-review digest table")
    start = lines.index(header)
    if start + 1 >= len(lines) or lines[start + 1] != "|---|---|":
        raise ValidationError("v3 bound-review table separator differs")
    rows: list[tuple[str, str]] = []
    index = start + 2
    while index < len(lines) and lines[index].startswith("|"):
        match = re.fullmatch(
            r"\| `(?P<path>[^`]+)` \| `(?P<digest>[0-9a-f]{64})` \|",
            lines[index],
        )
        if match is None:
            raise ValidationError("v3 bound-review table contains a malformed row")
        rows.append((match.group("path"), match.group("digest")))
        index += 1
    if tuple(path for path, _digest in rows) != V3_BOUND_REPORTS:
        raise ValidationError("v3 bound-review paths/order differ from the exact manifest")
    if set(report_bytes) != set(V3_BOUND_REPORTS):
        raise ValidationError("v3 bound-review byte inputs differ from the exact manifest")
    for path, digest in rows:
        if digest != sha256_bytes(report_bytes[path]):
            raise ValidationError(f"v3 bound-review digest is stale for {path}")


def validate_blueprint_contract(blueprint_text: str, tasks: dict[str, Task]) -> None:
    for phrase in REQUIRED_BLUEPRINT_PHRASES:
        if phrase not in blueprint_text:
            raise ValidationError(f"blueprint missing required contract phrase: {phrase}")
    if blueprint_text.count("Authoritative path: `Docs/Stage3_Blueprint.md`") != 1:
        raise ValidationError("blueprint must name its authority exactly once")
    spec = parse_execution_spec(blueprint_text)
    expected_paths = {
        "authoritative blueprint": (spec.authoritative_blueprint, BLUEPRINT),
        "canonical runtime snapshot": (spec.runtime_snapshot, RUNTIME_SNAPSHOT),
        "pre-cleanup receipt": (spec.pre_cleanup_receipt, PRE_CLEANUP_RECEIPT),
        "cleanup receipt": (spec.cleanup_receipt, CLEANUP_RECEIPT),
        "same-name Gantt companion": (spec.gantt_path, GANTT),
    }
    for label, (recorded, path) in expected_paths.items():
        if recorded != path.relative_to(ROOT).as_posix():
            raise ValidationError(f"execution specification {label} differs from checker path")
    if spec.status_schema != STATUS_SCHEMA:
        raise ValidationError("execution specification status schema differs from checker schema")
    if spec.runtime_root.rstrip("/") != RUNTIME_SNAPSHOT.relative_to(ROOT).parts[0] + "/" + RUNTIME_SNAPSHOT.relative_to(ROOT).parts[1]:
        raise ValidationError("execution specification runtime root differs from checker runtime root")
    if not spec.skill_build.startswith("b3ehive/1.5.0+") or EXECUTION_CONTRACT != "b3ehive-execution/1.5.0":
        raise ValidationError("execution specification skill build/contract differs from checker contract")
    if str(ROOT) in blueprint_text:
        raise ValidationError("blueprint leaks this machine's absolute repository path")
    if len(tasks) > 200:
        raise ValidationError("Stage3 checklist exceeds the bounded 200-item authority limit")
    try:
        gap_review_text = GAP_REVIEW.read_bytes().decode("utf-8")
        source_report_bytes = {
            path: (ROOT / path).read_bytes() for path in BOUND_SOURCE_REPORTS
        }
        v3_report_bytes = {path: (ROOT / path).read_bytes() for path in V3_BOUND_REPORTS}
    except (OSError, UnicodeDecodeError) as exc:
        raise ValidationError("bound review bytes are unavailable") from exc
    validate_gap_review_source_reports(gap_review_text, source_report_bytes)
    validate_v3_bound_reports(blueprint_text, v3_report_bytes)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_json_sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json_bytes(value)).hexdigest()


def content_addressed_id(prefix: str, value: dict[str, Any], identity_key: str) -> str:
    payload = {key: field for key, field in value.items() if key != identity_key}
    return f"{prefix}/{canonical_json_sha256(payload)}"


def runtime_observation_payload(item: dict[str, Any]) -> dict[str, Any]:
    """Canonical embedded evidence payload, excluding its own digest fields."""

    startup_evidence = item.get("startup_evidence")
    if isinstance(startup_evidence, dict):
        startup_evidence = {
            key: value for key, value in startup_evidence.items() if key != "identity_evidence_sha256"
        }
    live_evidence = item.get("live_evidence")
    if isinstance(live_evidence, dict):
        live_evidence = {
            key: value for key, value in live_evidence.items() if key != "identity_evidence_sha256"
        }
    return {
        "schema_version": "stage3-runtime-observation/1.0",
        "id": item["id"],
        "claim_id": item["claim_id"],
        "run_id": item["run_id"],
        "owner": item["owner"],
        "startup": item["startup"],
        "startup_evidence": startup_evidence,
        "live": item["live"],
        "live_evidence": live_evidence,
        "running": item["running"],
        "handoff": item["handoff"],
        "integration": item["integration"],
        "repair": item["repair"],
        "runtime_block": item["runtime_block"],
        "timing": item["timing"],
    }


def runtime_item_root(item: dict[str, Any]) -> str | None:
    if item.get("claim_id") is None or item.get("run_id") is None:
        return None
    return f".ops/stage3-execution-v1/tasks/{item['claim_id']}/{item['run_id']}"


def runtime_observation_source(item: dict[str, Any]) -> str:
    root = runtime_item_root(item)
    if root is None:
        return f".ops/stage3-execution-v1/status/items/{item['id']}.json"
    return f"{root}/status/runtime-observation.json"


def _validate_content_evidence(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    evidence = _require_exact_keys(value, keys, label)
    if not isinstance(evidence["source"], str) or not evidence["source"].strip():
        raise ValidationError(f"{label}.source must be a nonempty identity")
    if not isinstance(evidence["payload"], dict):
        raise ValidationError(f"{label}.payload must be an object")
    digest = evidence["sha256"]
    if not isinstance(digest, str) or not HEX_SHA256_RE.fullmatch(digest):
        raise ValidationError(f"{label}.sha256 is malformed")
    if digest != canonical_json_sha256(evidence["payload"]):
        raise ValidationError(f"{label}.sha256 does not bind its canonical payload")
    return evidence


def _validate_stop_reason(value: Any, label: str) -> dict[str, Any]:
    reason = _require_exact_keys(value, STOP_REASON_KEYS, label)
    if reason["kind"] not in UNDERFILL_KINDS:
        raise ValidationError(f"{label} has an unsupported kind")
    if not isinstance(reason["reason"], str) or not reason["reason"].strip():
        raise ValidationError(f"{label} requires a concrete reason")
    evidence = _validate_content_evidence(
        reason["evidence"], STOP_REASON_EVIDENCE_KEYS, f"{label}.evidence"
    )
    payload = evidence["payload"]
    if payload.get("kind") != reason["kind"] or payload.get("reason") != reason["reason"]:
        raise ValidationError(f"{label} evidence does not bind the exact kind/reason")
    return reason


def _validate_process_identity(
    value: Any,
    *,
    item: dict[str, Any],
    observed_at: datetime,
    label: str,
) -> dict[str, Any]:
    process = _require_exact_keys(value, STARTUP_PROCESS_KEYS, label)
    for key in ("pane_pid", "process_start_ticks"):
        if not isinstance(process[key], int) or isinstance(process[key], bool) or process[key] <= 0:
            raise ValidationError(f"{label}.{key} must be a positive integer")
    if not isinstance(process["session"], str) or not SAFE_PATH_COMPONENT_RE.fullmatch(process["session"]):
        raise ValidationError(f"{label}.session has unsafe identity syntax")
    if process["alive"] is not True:
        raise ValidationError(f"{label} does not attest a live process")
    _validate_rfc3339_utc(process["observed_at"], f"{label}.observed_at")
    process_observed = datetime.strptime(process["observed_at"], "%Y-%m-%dT%H:%M:%SZ")
    if process_observed != observed_at:
        raise ValidationError(f"{label} is not fresh at the reconciled snapshot time")
    task_root = runtime_item_root(item)
    if task_root is None:
        raise ValidationError(f"{label} lacks claim/run identity")
    expected_paths = {
        "tmux_socket": f"{task_root}/tmux.sock",
        "cwd": f"{task_root}/work",
        "codex_home": f"{task_root}/codex-home",
    }
    for key, expected in expected_paths.items():
        _validate_runtime_path(process[key], f"{label}.{key}")
        if process[key] != expected:
            raise ValidationError(f"{label}.{key} differs from the exact claim root")
    return process


def _validate_rfc3339_utc(value: Any, label: str, *, nullable: bool = False) -> None:
    if value is None and nullable:
        return
    if not isinstance(value, str) or not RFC3339_UTC_RE.fullmatch(value):
        raise ValidationError(f"{label} must be an RFC3339 UTC second timestamp")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise ValidationError(f"{label} is not a real RFC3339 timestamp") from exc
    if parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ValidationError(f"{label} is not UTC")


def build_projection_metadata(
    blueprint_text: str,
    generated_at: str,
    *,
    runtime_snapshot_sha256: str | None = None,
    runtime_snapshot_id: str | None = None,
    cleanup_receipt_sha256: str | None = None,
    cleanup_receipt_id: str | None = None,
) -> dict[str, Any]:
    _validate_rfc3339_utc(generated_at, "generated_at")
    generated = datetime.strptime(generated_at, "%Y-%m-%dT%H:%M:%SZ")
    if generated > datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(seconds=5):
        raise ValidationError("projection generated_at is in the future")
    if runtime_snapshot_sha256 is not None and cleanup_receipt_sha256 is not None:
        raise ValidationError(
            "terminal cleanup receipt and live controller runtime snapshot are mutually exclusive"
        )
    if (runtime_snapshot_sha256 is None) != (runtime_snapshot_id is None):
        raise ValidationError("runtime snapshot digest and ID must both be present or both be null")
    if runtime_snapshot_sha256 is not None and not HEX_SHA256_RE.fullmatch(runtime_snapshot_sha256):
        raise ValidationError("runtime snapshot SHA256 is malformed")
    if (cleanup_receipt_sha256 is None) != (cleanup_receipt_id is None):
        raise ValidationError("cleanup receipt digest and ID must both be present or both be null")
    if cleanup_receipt_sha256 is not None and not HEX_SHA256_RE.fullmatch(cleanup_receipt_sha256):
        raise ValidationError("cleanup receipt SHA256 is malformed")
    raw_blueprint_sha256 = sha256_text(blueprint_text)
    spec_region = exact_marked_region(blueprint_text, SPEC_BEGIN, SPEC_END, "execution specification")
    execution_spec_region_sha256 = sha256_text(spec_region)
    projection_input = {
        "projection_contract": PROJECTION_SCHEMA,
        "blueprint_path": BLUEPRINT.relative_to(ROOT).as_posix(),
        "blueprint_version": VERSION,
        "raw_blueprint_sha256": raw_blueprint_sha256,
        "execution_spec_region_sha256": execution_spec_region_sha256,
        "runtime_snapshot_sha256": runtime_snapshot_sha256,
        "runtime_snapshot_id": runtime_snapshot_id,
        "runtime_snapshot_path": RUNTIME_SNAPSHOT.relative_to(ROOT).as_posix(),
        "cleanup_receipt_path": CLEANUP_RECEIPT.relative_to(ROOT).as_posix(),
        "cleanup_receipt_sha256": cleanup_receipt_sha256,
        "cleanup_receipt_id": cleanup_receipt_id,
    }
    projection_input_sha256 = hashlib.sha256(_canonical_json_bytes(projection_input)).hexdigest()
    return {
        "schema_version": PROJECTION_SCHEMA,
        "blueprint_path": BLUEPRINT.relative_to(ROOT).as_posix(),
        "blueprint_version": VERSION,
        "gantt_path": GANTT.relative_to(ROOT).as_posix(),
        "status_path": STATUS.relative_to(ROOT).as_posix(),
        "kanban_path": KANBAN.relative_to(ROOT).as_posix(),
        "raw_blueprint_sha256": raw_blueprint_sha256,
        "execution_spec_region_sha256": execution_spec_region_sha256,
        "runtime_snapshot_sha256": runtime_snapshot_sha256,
        "runtime_snapshot_id": runtime_snapshot_id,
        "runtime_snapshot_path": RUNTIME_SNAPSHOT.relative_to(ROOT).as_posix(),
        "cleanup_receipt_path": CLEANUP_RECEIPT.relative_to(ROOT).as_posix(),
        "cleanup_receipt_sha256": cleanup_receipt_sha256,
        "cleanup_receipt_id": cleanup_receipt_id,
        "projection_input_sha256": projection_input_sha256,
        "snapshot_id": f"stage3-projection/{projection_input_sha256}",
        "generated_at": generated_at,
    }


def _reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def parse_json_strict(text: str, label: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_json_keys)
    except ValidationError:
        raise
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{label} is invalid JSON: {exc}") from exc


def _require_exact_keys(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    actual = set(value)
    if actual != keys:
        raise ValidationError(f"{label} fields differ: missing={sorted(keys - actual)}, extra={sorted(actual - keys)}")
    return value


def parse_surface_metadata(text: str, label: str) -> dict[str, Any]:
    begin, end, lines = _one_region(text, METADATA_BEGIN, METADATA_END, f"{label} metadata")
    region = lines[begin + 1 : end]
    if len(region) < 3 or region[0] != "```json" or region[-1] != "```":
        raise ValidationError(f"{label} metadata must be one fenced JSON object")
    metadata = parse_json_strict("\n".join(region[1:-1]), f"{label} metadata")
    metadata = _require_exact_keys(metadata, PROJECTION_METADATA_KEYS, f"{label} metadata")
    if region[1:-1] != json.dumps(
        metadata, ensure_ascii=False, indent=2, sort_keys=False
    ).splitlines():
        raise ValidationError(f"{label} metadata is not canonically encoded")
    return metadata


def _validate_nullable_string(value: Any, label: str) -> None:
    if value is not None and (not isinstance(value, str) or not value.strip()):
        raise ValidationError(f"{label} must be null or a nonempty string")


def _validate_timing(value: Any, label: str) -> dict[str, Any]:
    timing = _require_exact_keys(value, TIMING_KEYS, label)
    status = timing["status"]
    if status == "unscheduled":
        if any(timing[key] is not None for key in ("start", "end", "duration_seconds", "source")):
            raise ValidationError(f"{label}: unscheduled timing may not invent dates, duration, or source")
        return timing
    if status != "recorded":
        raise ValidationError(f"{label}: timing status must be unscheduled or recorded")
    _validate_rfc3339_utc(timing["start"], f"{label}.start")
    _validate_rfc3339_utc(timing["end"], f"{label}.end", nullable=True)
    source = _require_exact_keys(timing["source"], TIMING_SOURCE_KEYS, f"{label}.source")
    _validate_runtime_path(source["path"], f"{label}.source.path")
    source_payload = _require_exact_keys(
        source["payload"], TIMING_SOURCE_PAYLOAD_KEYS, f"{label}.source.payload"
    )
    expected_source_payload = {
        "start": timing["start"],
        "end": timing["end"],
        "duration_seconds": timing["duration_seconds"],
    }
    if source_payload != expected_source_payload or source["sha256"] != canonical_json_sha256(
        source_payload
    ):
        raise ValidationError(f"{label}: recorded timing source does not bind exact endpoints")
    duration = timing["duration_seconds"]
    if duration is not None and (not isinstance(duration, int) or isinstance(duration, bool) or duration < 0):
        raise ValidationError(f"{label}: duration_seconds must be null or a nonnegative integer")
    if timing["end"] is not None:
        start = datetime.strptime(timing["start"], "%Y-%m-%dT%H:%M:%SZ")
        end = datetime.strptime(timing["end"], "%Y-%m-%dT%H:%M:%SZ")
        if end < start:
            raise ValidationError(f"{label}: recorded end precedes start")
        actual_duration = int((end - start).total_seconds())
        if duration is not None and duration != actual_duration:
            raise ValidationError(f"{label}: duration does not match recorded endpoints")
    return timing


def parse_runtime_snapshot(
    runtime_snapshot_text: str,
    tasks: dict[str, Task],
    blueprint_text: str | None = None,
    *,
    pre_cleanup_receipt_text: str | None = None,
) -> dict[str, Any]:
    if blueprint_text is None:
        blueprint_text = BLUEPRINT.read_bytes().decode("utf-8")
    snapshot = parse_json_strict(runtime_snapshot_text, "runtime snapshot")
    snapshot = _require_exact_keys(snapshot, RUNTIME_TOP_LEVEL_KEYS, "runtime snapshot")
    if snapshot["schema_version"] != RUNTIME_SCHEMA:
        raise ValidationError("runtime snapshot schema differs")
    if snapshot["blueprint_version"] != VERSION:
        raise ValidationError("runtime snapshot blueprint version differs")
    if snapshot["raw_blueprint_sha256"] != sha256_text(blueprint_text):
        raise ValidationError("runtime snapshot raw Blueprint digest is stale")
    spec_region = exact_marked_region(blueprint_text, SPEC_BEGIN, SPEC_END, "execution specification")
    if snapshot["execution_spec_region_sha256"] != sha256_text(spec_region):
        raise ValidationError("runtime snapshot execution specification digest is stale")
    execution_spec = parse_execution_spec(blueprint_text)
    _validate_nullable_string(snapshot["snapshot_id"], "runtime snapshot ID")
    if snapshot["snapshot_id"] is None or not SAFE_RUNTIME_ID_RE.fullmatch(snapshot["snapshot_id"]):
        raise ValidationError("runtime snapshot ID must use the stable safe-ID grammar")
    _validate_rfc3339_utc(snapshot["observed_at"], "runtime observed_at")
    _validate_rfc3339_utc(snapshot["last_progress"], "runtime last_progress", nullable=True)
    observed_at = datetime.strptime(snapshot["observed_at"], "%Y-%m-%dT%H:%M:%SZ")
    current_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    if observed_at > current_utc + timedelta(seconds=5):
        raise ValidationError("runtime observed_at is in the future")
    if snapshot["last_progress"] is not None:
        last_progress = datetime.strptime(snapshot["last_progress"], "%Y-%m-%dT%H:%M:%SZ")
        if last_progress > observed_at:
            raise ValidationError("runtime last_progress is later than snapshot observed_at")
    _validate_nullable_string(snapshot["cleanup_state"], "runtime cleanup_state")
    if snapshot["cleanup_state"] is not None and snapshot["cleanup_state"] not in RUNTIME_CLEANUP_STATES:
        raise ValidationError("runtime cleanup_state is unsupported; complete requires a durable cleanup receipt")
    cleanup_arm = snapshot["cleanup_arm"]
    if snapshot["cleanup_state"] in {None, "not_started"}:
        if cleanup_arm is not None:
            raise ValidationError("runtime names a cleanup arm before cleanup_pending")
    else:
        cleanup_arm = _require_exact_keys(cleanup_arm, CLEANUP_ARM_KEYS, "runtime cleanup_arm")
        if pre_cleanup_receipt_text is None:
            raise ValidationError("runtime cleanup transition lacks the canonical pre-cleanup receipt bytes")
    admission = _require_exact_keys(snapshot["admission"], ADMISSION_KEYS, "runtime admission")
    for key in (
        "logical_claim_target",
        "startup_reservation_target",
        "authenticated_live_target",
        "running_turn_target",
        "admitted_target",
        "eligible_ready_count",
        "requested_target",
        "host_admissible_target",
        "master_integration_target",
        "cpu_validator_lease_target",
        "active_cpu_validator_leases",
    ):
        value = admission[key]
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValidationError(f"runtime admission {key} must be a nonnegative integer")
    configured_targets = {
        "logical_claim_target": execution_spec.logical_claim_ceiling,
        "startup_reservation_target": execution_spec.startup_reservations,
        "authenticated_live_target": execution_spec.authenticated_live_ceiling,
        "running_turn_target": execution_spec.running_turn_ceiling,
        "master_integration_target": execution_spec.master_integrations,
        "cpu_validator_lease_target": execution_spec.cpu_validator_leases,
    }
    for key, configured in configured_targets.items():
        if admission[key] != configured:
            raise ValidationError(f"runtime admission {key} differs from the frozen execution specification")
    if admission["requested_target"] != execution_spec.logical_claim_ceiling:
        raise ValidationError("runtime requested_target differs from the operator-requested ceiling")
    if admission["active_cpu_validator_leases"] > admission["cpu_validator_lease_target"]:
        raise ValidationError("runtime active CPU validator leases exceed the frozen target")
    ready_ids = planning_projection(tasks)["frontiers"]["implementation_ready"]
    if admission["eligible_ready_count"] != len(ready_ids):
        raise ValidationError("runtime eligible_ready_count differs from the authoritative DAG frontier")
    if not isinstance(admission["effective_target_bindings"], list):
        raise ValidationError("runtime effective_target_bindings must be an array")
    bindings: dict[str, dict[str, Any]] = {}
    for index, raw_binding in enumerate(admission["effective_target_bindings"]):
        binding = _require_exact_keys(raw_binding, EFFECTIVE_BINDING_KEYS, f"effective target binding {index}")
        kind = binding["kind"]
        if kind not in EFFECTIVE_BINDING_KINDS:
            raise ValidationError(f"effective target binding {index} has an unsupported kind")
        if kind in bindings:
            raise ValidationError(f"runtime repeats effective target binding {kind}")
        limit = binding["limit"]
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
            raise ValidationError(f"effective target binding {kind} has an invalid limit")
        _validate_nullable_string(binding["reason"], f"effective target binding {kind} reason")
        evidence = _validate_content_evidence(
            binding["evidence"], EFFECTIVE_BINDING_EVIDENCE_KEYS,
            f"effective target binding {kind} evidence",
        )
        if evidence["payload"].get("limit") != limit:
            raise ValidationError(f"effective target binding {kind} limit is not derived from its payload")
        bindings[kind] = binding
    if set(bindings) != EFFECTIVE_BINDING_KINDS:
        raise ValidationError(
            "runtime effective target binding kinds differ: "
            f"missing={sorted(EFFECTIVE_BINDING_KINDS - set(bindings))}, "
            f"extra={sorted(set(bindings) - EFFECTIVE_BINDING_KINDS)}"
        )
    spec_digest = snapshot["execution_spec_region_sha256"]
    fixed_binding_limits = {
        "logical_cap": admission["logical_claim_target"],
        "authenticated_live_cap": admission["authenticated_live_target"],
        "running_turn_cap": admission["running_turn_target"],
        "requested": admission["requested_target"],
        "eligible": admission["eligible_ready_count"],
        "host_resource": admission["host_admissible_target"],
    }
    for kind, limit in fixed_binding_limits.items():
        if bindings[kind]["limit"] != limit:
            raise ValidationError(f"runtime effective target binding {kind} differs from its source field")
    spec_fields = {
        "logical_cap": "requested logical-claim ceiling",
        "authenticated_live_cap": "authenticated-live and running-turn ceilings",
        "running_turn_cap": "authenticated-live and running-turn ceilings",
        "requested": "requested logical-claim ceiling",
    }
    for kind, field in spec_fields.items():
        expected_evidence = {
            "source": "Docs/Stage3_Blueprint.md#STAGE3-EXECUTION-SPEC",
            "payload": {
                "field": field,
                "limit": bindings[kind]["limit"],
                "execution_spec_region_sha256": spec_digest,
            },
        }
        expected_evidence["sha256"] = canonical_json_sha256(expected_evidence["payload"])
        if bindings[kind]["evidence"] != expected_evidence or not bindings[kind]["reason"]:
            raise ValidationError(f"runtime effective target binding {kind} is not specification-bound")
    eligible_payload = {
        "ids": ready_ids,
        "limit": len(ready_ids),
        "raw_blueprint_sha256": snapshot["raw_blueprint_sha256"],
    }
    eligible_evidence = {
        "source": "Docs/Stage3_Blueprint.md#STAGE3-EXECUTION-CHECKLIST",
        "payload": eligible_payload,
        "sha256": canonical_json_sha256(eligible_payload),
    }
    if bindings["eligible"]["evidence"] != eligible_evidence or not bindings["eligible"]["reason"]:
        raise ValidationError("runtime eligible target binding is not bound to the exact ready-ID frontier")
    for kind in EFFECTIVE_BINDING_KINDS - set(spec_fields) - {"eligible"}:
        evidence = bindings[kind]["evidence"]
        _validate_runtime_path(evidence["source"], f"effective target binding {kind} evidence source")
        expected_source = f".ops/stage3-execution-v1/status/admission/{kind}.json"
        if evidence["source"] != expected_source:
            raise ValidationError(f"runtime effective target binding {kind} evidence source differs")
        common_fields = {"limit", "observed_at", "basis"}
        extra_fields = {
            "logical_available": set(),
            "host_resource": {
                "available_ram_bytes", "free_disk_bytes", "load_1m", "swap_exhausted",
                "pid_limit", "pid_usage", "pid_source",
            },
            "conflict": {"conflicting_pairs"},
            "external_limit": {"decisions"},
            "route": {"routes"},
            "validator": {"lease_target", "active_leases"},
            "budget": {"pump_started_at", "pump_deadline_at", "remaining_seconds"},
        }[kind]
        if set(evidence["payload"]) != common_fields | extra_fields:
            raise ValidationError(f"runtime effective target binding {kind} evidence payload fields differ")
        if evidence["payload"]["observed_at"] != snapshot["observed_at"]:
            raise ValidationError(f"runtime effective target binding {kind} is stale")
        if not isinstance(evidence["payload"]["basis"], str) or not evidence["payload"]["basis"].strip():
            raise ValidationError(f"runtime effective target binding {kind} lacks a concrete basis")
        payload = evidence["payload"]
        derived_limit = payload["limit"]
        if kind == "host_resource":
            integer_metrics = ("available_ram_bytes", "free_disk_bytes", "pid_limit", "pid_usage")
            if any(
                not isinstance(payload[key], int) or isinstance(payload[key], bool) or payload[key] < 0
                for key in integer_metrics
            ):
                raise ValidationError("runtime host-resource evidence has invalid integer metrics")
            if (
                not isinstance(payload["load_1m"], (int, float))
                or isinstance(payload["load_1m"], bool)
                or payload["load_1m"] < 0
                or not isinstance(payload["swap_exhausted"], bool)
                or not isinstance(payload["pid_source"], str)
                or not payload["pid_source"].strip()
                or payload["pid_usage"] > payload["pid_limit"]
            ):
                raise ValidationError("runtime host-resource evidence is malformed")
            host_ok = (
                payload["available_ram_bytes"] >= 16 * 1024**3
                and payload["free_disk_bytes"] >= 100 * 1024**3
                and payload["load_1m"] < 24
                and payload["swap_exhausted"] is False
                and payload["pid_limit"] - payload["pid_usage"] >= 512
            )
            derived_limit = admission["requested_target"] if host_ok else 0
        elif kind == "conflict":
            if not isinstance(payload["conflicting_pairs"], list) or any(
                not isinstance(pair, list)
                or len(pair) != 2
                or any(not isinstance(value, str) or not value for value in pair)
                for pair in payload["conflicting_pairs"]
            ):
                raise ValidationError("runtime conflict evidence is malformed")
            derived_limit = max(0, admission["requested_target"] - len(payload["conflicting_pairs"]))
        elif kind == "external_limit":
            if not isinstance(payload["decisions"], list) or not payload["decisions"]:
                raise ValidationError("runtime external-limit evidence lacks provider decisions")
            limits: list[int] = []
            for decision in payload["decisions"]:
                decision = _require_exact_keys(
                    decision, {"name", "decision", "limit", "observed_at"},
                    "runtime external-limit decision",
                )
                if (
                    not isinstance(decision["name"], str)
                    or not decision["name"].strip()
                    or decision["decision"] not in {"allow", "block"}
                    or not isinstance(decision["limit"], int)
                    or isinstance(decision["limit"], bool)
                    or decision["limit"] < 0
                    or decision["observed_at"] != snapshot["observed_at"]
                ):
                    raise ValidationError("runtime external-limit decision is malformed or stale")
                limits.append(decision["limit"] if decision["decision"] == "allow" else 0)
            derived_limit = min(limits)
        elif kind == "route":
            if not isinstance(payload["routes"], list) or not payload["routes"]:
                raise ValidationError("runtime route evidence lacks route observations")
            route_limits: list[int] = []
            for route_observation in payload["routes"]:
                route_observation = _require_exact_keys(
                    route_observation, {"route_id", "available", "limit", "observed_at"},
                    "runtime route observation",
                )
                if (
                    not isinstance(route_observation["route_id"], str)
                    or not route_observation["route_id"].strip()
                    or not isinstance(route_observation["available"], bool)
                    or not isinstance(route_observation["limit"], int)
                    or isinstance(route_observation["limit"], bool)
                    or route_observation["limit"] < 0
                    or route_observation["observed_at"] != snapshot["observed_at"]
                ):
                    raise ValidationError("runtime route observation is malformed or stale")
                route_limits.append(
                    route_observation["limit"] if route_observation["available"] else 0
                )
            derived_limit = min(route_limits)
        elif kind == "validator":
            if (
                payload["lease_target"] != admission["cpu_validator_lease_target"]
                or payload["active_leases"] != admission["active_cpu_validator_leases"]
            ):
                raise ValidationError("runtime validator binding differs from observed lease occupancy")
            derived_limit = (
                admission["requested_target"]
                if payload["active_leases"] < payload["lease_target"]
                else 0
            )
        elif kind == "budget":
            _validate_rfc3339_utc(payload["pump_started_at"], "runtime pump_started_at")
            _validate_rfc3339_utc(payload["pump_deadline_at"], "runtime pump_deadline_at")
            pump_started = datetime.strptime(payload["pump_started_at"], "%Y-%m-%dT%H:%M:%SZ")
            pump_deadline = datetime.strptime(payload["pump_deadline_at"], "%Y-%m-%dT%H:%M:%SZ")
            if (
                not isinstance(payload["remaining_seconds"], int)
                or isinstance(payload["remaining_seconds"], bool)
                or payload["remaining_seconds"] < 0
                or pump_deadline < observed_at
                or int((pump_deadline - pump_started).total_seconds())
                > execution_spec.admission_pump_budget_seconds
                or payload["remaining_seconds"] != int((pump_deadline - observed_at).total_seconds())
            ):
                raise ValidationError("runtime budget binding is temporally inconsistent")
            derived_limit = admission["requested_target"] if payload["remaining_seconds"] > 0 else 0
        if derived_limit != bindings[kind]["limit"]:
            raise ValidationError(f"runtime effective target binding {kind} limit is not independently derived")
    if not bindings["host_resource"]["reason"]:
        raise ValidationError("runtime host admissible target lacks an observation reason")
    for kind in ("conflict", "external_limit", "route", "validator", "budget"):
        if bindings[kind]["limit"] > admission["requested_target"]:
            raise ValidationError(f"runtime effective target binding {kind} exceeds requested capacity")
        if bindings[kind]["limit"] < admission["requested_target"] and (
            not bindings[kind]["reason"]
        ):
            raise ValidationError(f"runtime reducing binding {kind} lacks a reason")
    recomputed_target = min(binding["limit"] for binding in bindings.values())
    if admission["admitted_target"] != recomputed_target:
        raise ValidationError("runtime admitted_target does not equal the minimum effective target binding")
    if admission["admitted_target"] > min(
        admission["logical_claim_target"],
        admission["authenticated_live_target"],
        admission["running_turn_target"],
    ):
        raise ValidationError("runtime admitted_target exceeds a logical/live/running ceiling")
    underfill = admission["underfill_stop_reason"]
    if underfill is not None:
        underfill = _validate_stop_reason(underfill, "runtime underfill_stop_reason")
    occupancy_underfill = admission["occupancy_underfill_reason"]
    if occupancy_underfill is not None:
        occupancy_underfill = _validate_stop_reason(
            occupancy_underfill, "runtime occupancy_underfill_reason"
        )
    if not isinstance(snapshot["items"], list):
        raise ValidationError("runtime snapshot items must be an array")
    items: dict[str, dict[str, Any]] = {}
    claim_ids: set[str] = set()
    run_ids: set[str] = set()
    active_sessions: set[str] = set()
    active_processes: set[tuple[int, int]] = set()
    active_threads: set[str] = set()
    active_goals: set[str] = set()
    active_sockets: set[str] = set()
    active_homes: set[str] = set()
    active_task_roots: set[str] = set()
    for index, raw_item in enumerate(snapshot["items"]):
        item = _require_exact_keys(raw_item, RUNTIME_ITEM_KEYS, f"runtime item {index}")
        item_id = item["id"]
        if not isinstance(item_id, str) or item_id not in tasks:
            raise ValidationError(f"runtime item {index} has an unknown ID")
        if item_id in items:
            raise ValidationError(f"runtime snapshot repeats item {item_id}")
        for key in ("claim_id", "run_id", "owner"):
            _validate_nullable_string(item[key], f"{item_id}.{key}")
        for key in ("claim_id", "run_id"):
            if item[key] is not None and not SAFE_PATH_COMPONENT_RE.fullmatch(item[key]):
                raise ValidationError(f"{item_id}.{key} must be one safe task-root path component")
        observation = _require_exact_keys(
            item["observation_evidence"], OBSERVATION_EVIDENCE_KEYS, f"{item_id}.observation_evidence"
        )
        _validate_runtime_path(observation["source"], f"{item_id}.observation_evidence.source")
        if not isinstance(observation["sha256"], str) or not HEX_SHA256_RE.fullmatch(observation["sha256"]):
            raise ValidationError(f"{item_id}: observation evidence digest is malformed")
        _validate_rfc3339_utc(observation["observed_at"], f"{item_id}.observation_evidence.observed_at")
        if observation["observed_at"] != snapshot["observed_at"]:
            raise ValidationError(f"{item_id}: observation evidence is from a different reconciliation time")
        if item["startup"] is not None and item["startup"] not in STARTUP_STATES:
            raise ValidationError(f"{item_id}: unsupported startup state")
        startup_evidence = item["startup_evidence"]
        if item["startup"] is None:
            if startup_evidence is not None:
                raise ValidationError(f"{item_id}: startup evidence exists without a startup state")
        else:
            startup_evidence = _require_exact_keys(
                startup_evidence, STARTUP_EVIDENCE_KEYS, f"{item_id}.startup_evidence"
            )
            _validate_rfc3339_utc(startup_evidence["state_entered_at"], f"{item_id}.startup state_entered_at")
            _validate_rfc3339_utc(startup_evidence["deadline_at"], f"{item_id}.startup deadline_at")
            entered = datetime.strptime(startup_evidence["state_entered_at"], "%Y-%m-%dT%H:%M:%SZ")
            deadline = datetime.strptime(startup_evidence["deadline_at"], "%Y-%m-%dT%H:%M:%SZ")
            if entered > observed_at or deadline < observed_at or deadline < entered:
                raise ValidationError(f"{item_id}: startup evidence is stale or temporally inconsistent")
            deadline_limit = (
                execution_spec.authentication_deadline_seconds
                if item["startup"] == "goal_submitted"
                else execution_spec.startup_deadline_seconds
            )
            if int((deadline - entered).total_seconds()) > deadline_limit:
                raise ValidationError(f"{item_id}: startup deadline exceeds the frozen state limit")
            if not isinstance(startup_evidence["identity_evidence_sha256"], str) or not HEX_SHA256_RE.fullmatch(
                startup_evidence["identity_evidence_sha256"]
            ):
                raise ValidationError(f"{item_id}: startup identity evidence digest is malformed")
            requires_process = item["startup"] in {"tmux_started", "goal_pasted", "goal_submitted"}
            if requires_process:
                _validate_process_identity(
                    startup_evidence["process_identity"],
                    item=item,
                    observed_at=observed_at,
                    label=f"{item_id}.startup.process_identity",
                )
            elif startup_evidence["process_identity"] is not None:
                raise ValidationError(f"{item_id}: pre-process startup state invents process identity")
        for key in ("live", "running"):
            if not isinstance(item[key], bool):
                raise ValidationError(f"{item_id}.{key} must be boolean in an observed runtime snapshot")
        if item["running"] is True and item["live"] is not True:
            raise ValidationError(f"{item_id}: a running turn must be authenticated live")
        live_evidence = item["live_evidence"]
        if item["live"] is not True:
            if live_evidence is not None:
                raise ValidationError(f"{item_id}: live evidence exists for a non-live lane")
        else:
            live_evidence = _require_exact_keys(live_evidence, LIVE_EVIDENCE_KEYS, f"{item_id}.live_evidence")
            _validate_rfc3339_utc(live_evidence["authenticated_at"], f"{item_id}.live authenticated_at")
            authenticated = datetime.strptime(live_evidence["authenticated_at"], "%Y-%m-%dT%H:%M:%SZ")
            if authenticated > observed_at:
                raise ValidationError(f"{item_id}: live authentication is later than the snapshot")
            for digest_key in ("identity_evidence_sha256", "route_sha256"):
                if not isinstance(live_evidence[digest_key], str) or not HEX_SHA256_RE.fullmatch(
                    live_evidence[digest_key]
                ):
                    raise ValidationError(f"{item_id}: live {digest_key} is malformed")
            for component_key in ("session", "thread_id", "goal_id"):
                if not isinstance(live_evidence[component_key], str) or not SAFE_PATH_COMPONENT_RE.fullmatch(
                    live_evidence[component_key]
                ):
                    raise ValidationError(f"{item_id}: live {component_key} has unsafe identity syntax")
            for integer_key in ("pane_pid", "process_start_ticks"):
                if (
                    not isinstance(live_evidence[integer_key], int)
                    or isinstance(live_evidence[integer_key], bool)
                    or live_evidence[integer_key] <= 0
                ):
                    raise ValidationError(f"{item_id}: live {integer_key} must be a positive integer")
            if live_evidence["process_alive"] is not True:
                raise ValidationError(f"{item_id}: live process evidence is not alive")
            _validate_rfc3339_utc(
                live_evidence["process_observed_at"], f"{item_id}.live process_observed_at"
            )
            if live_evidence["process_observed_at"] != snapshot["observed_at"]:
                raise ValidationError(f"{item_id}: live process evidence is stale")
            if item["claim_id"] is None or item["run_id"] is None:
                raise ValidationError(f"{item_id}: live evidence lacks claim/run identity")
            task_root = f".ops/stage3-execution-v1/tasks/{item['claim_id']}/{item['run_id']}"
            expected_paths = {
                "tmux_socket": f"{task_root}/tmux.sock",
                "cwd": f"{task_root}/work",
                "codex_home": f"{task_root}/codex-home",
            }
            for path_key, expected_path in expected_paths.items():
                _validate_runtime_path(live_evidence[path_key], f"{item_id}.live {path_key}")
                if live_evidence[path_key] != expected_path:
                    raise ValidationError(f"{item_id}: live {path_key} differs from the exact claim root")
            route = _require_exact_keys(live_evidence["route"], LIVE_ROUTE_KEYS, f"{item_id}.live route")
            for route_key, route_value in route.items():
                if route_value is not None and (
                    not isinstance(route_value, str) or not route_value.strip()
                ):
                    raise ValidationError(f"{item_id}: live route {route_key} must be null or nonempty")
            if not isinstance(route["provider"], str) or not route["provider"].strip():
                raise ValidationError(f"{item_id}: live route lacks a provider")
            if not isinstance(route["model"], str) or not route["model"].strip():
                raise ValidationError(f"{item_id}: live route lacks a model")
            if live_evidence["route_sha256"] != canonical_json_sha256(route):
                raise ValidationError(f"{item_id}: live route digest does not bind the route payload")
            if live_evidence["goal_status"] != "active":
                raise ValidationError(f"{item_id}: live goal status is not active")
            if live_evidence["goal_item_id"] != item_id:
                raise ValidationError(f"{item_id}: live goal item binding differs")
            if live_evidence["goal_claim_id"] != item["claim_id"]:
                raise ValidationError(f"{item_id}: live goal claim binding differs")
            objective = live_evidence["goal_objective"]
            if (
                not isinstance(objective, str)
                or item_id not in objective
                or item["claim_id"] not in objective
            ):
                raise ValidationError(f"{item_id}: live goal objective does not name the item and claim")
        if item["handoff"] is not None and item["handoff"] not in HANDOFF_STATES:
            raise ValidationError(f"{item_id}: unsupported handoff state")
        if item["integration"] is not None and item["integration"] not in INTEGRATION_STATES:
            raise ValidationError(f"{item_id}: unsupported integration state")
        if item["repair"] is not None and item["repair"] not in REPAIR_STATES:
            raise ValidationError(f"{item_id}: unsupported repair state")
        runtime_block = item["runtime_block"]
        if runtime_block is not None:
            runtime_block = _require_exact_keys(runtime_block, {"kind", "reason"}, f"{item_id}.runtime_block")
            if runtime_block["kind"] not in RUNTIME_BLOCK_KINDS:
                raise ValidationError(f"{item_id}: unsupported runtime block kind")
            if not isinstance(runtime_block["reason"], str) or not runtime_block["reason"].strip():
                raise ValidationError(f"{item_id}: runtime block requires a reason")
        timing = _validate_timing(item["timing"], f"{item_id}.timing")
        if timing["status"] == "recorded":
            start = datetime.strptime(timing["start"], "%Y-%m-%dT%H:%M:%SZ")
            end = None if timing["end"] is None else datetime.strptime(timing["end"], "%Y-%m-%dT%H:%M:%SZ")
            if start > observed_at or (end is not None and end > observed_at):
                raise ValidationError(f"{item_id}: recorded timing is later than runtime observed_at")
        lifecycle_present = (
            item["startup"] is not None
            or item["live"] is True
            or item["running"] is True
            or any(item[key] is not None for key in ("handoff", "integration", "repair"))
        )
        if lifecycle_present and any(item[key] is None for key in ("claim_id", "run_id", "owner")):
            raise ValidationError(f"{item_id}: observed lifecycle state requires claim, run, and owner identity")
        identity_present = [item[key] is not None for key in ("claim_id", "run_id", "owner")]
        if any(identity_present) and not all(identity_present):
            raise ValidationError(f"{item_id}: claim, run, and owner identity must be all present or all null")
        if all(identity_present) and not lifecycle_present:
            raise ValidationError(f"{item_id}: claim identity exists without an explicit lifecycle state")
        if item["claim_id"] is not None:
            if item["claim_id"] in claim_ids:
                raise ValidationError(f"runtime snapshot reuses claim identity {item['claim_id']}")
            if item["run_id"] in run_ids:
                raise ValidationError(f"runtime snapshot reuses run identity {item['run_id']}")
            claim_ids.add(item["claim_id"])
            run_ids.add(item["run_id"])
        expected_observation_payload = runtime_observation_payload(item)
        if observation["payload"] != expected_observation_payload:
            raise ValidationError(f"{item_id}: observation evidence payload differs from the item lifecycle")
        observation_digest = canonical_json_sha256(expected_observation_payload)
        if observation["sha256"] != observation_digest:
            raise ValidationError(f"{item_id}: observation evidence digest does not bind its payload")
        if observation["source"] != runtime_observation_source(item):
            raise ValidationError(f"{item_id}: observation source differs from its canonical claim/run identity")
        if startup_evidence is not None and startup_evidence["identity_evidence_sha256"] != observation_digest:
            raise ValidationError(f"{item_id}: startup identity evidence is not bound to the observation")
        if live_evidence is not None and live_evidence["identity_evidence_sha256"] != observation_digest:
            raise ValidationError(f"{item_id}: live identity evidence is not bound to the observation")
        if item["startup"] is not None and (
            item["live"] is True
            or item["running"] is True
            or any(item[key] is not None for key in ("handoff", "integration", "repair"))
        ):
            raise ValidationError(f"{item_id}: startup state cannot coexist with downstream lifecycle state")
        if item["handoff"] is not None and (item["live"] is True or item["running"] is True):
            raise ValidationError(f"{item_id}: handoff state must have released live/running capacity")
        if item["integration"] is not None and item["handoff"] not in {"harvested", "finished"}:
            raise ValidationError(f"{item_id}: integration requires a harvested or finished handoff")
        if item["repair"] is not None and item["handoff"] not in {"harvested", "finished"}:
            raise ValidationError(f"{item_id}: repair requires a harvested or finished handoff")
        if item["repair"] in {"queued", "active", "exhausted"} and item["integration"] != "failed":
            raise ValidationError(f"{item_id}: unresolved repair requires failed integration")
        if item["repair"] == "resolved" and item["integration"] != "accepted":
            raise ValidationError(f"{item_id}: resolved repair requires accepted integration")
        if item["integration"] == "failed" and item["repair"] not in {"queued", "active", "exhausted"}:
            raise ValidationError(f"{item_id}: failed integration requires an explicit repair disposition")
        if item["integration"] == "accepted" and item["repair"] not in {None, "resolved"}:
            raise ValidationError(f"{item_id}: accepted integration contradicts unresolved repair")
        if tasks[item_id].state == "x":
            accepted_terminal = (
                item["claim_id"] is None
                and item["run_id"] is None
                and item["owner"] is None
                and item["startup"] is None
                and item["live"] is False
                and item["running"] is False
                and item["runtime_block"] is None
                and item["integration"] not in {"queued", "integrating", "failed"}
                and item["repair"] not in {"queued", "active", "exhausted"}
            )
            if not accepted_terminal:
                raise ValidationError(f"{item_id}: Master-accepted item contains active, blocked, or backlog state")
            if any(item[key] is not None for key in ("handoff", "integration", "repair")):
                raise ValidationError(f"{item_id}: accepted lifecycle history belongs only in immutable ledgers")
        elif tasks[item_id].state == " ":
            if item["handoff"] in {"harvested", "finished"} or item["integration"] is not None or item["repair"] is not None:
                raise ValidationError(f"{item_id}: durable handoff/integration state requires self-tested cursor")
        elif tasks[item_id].state == "_" and item["integration"] == "accepted":
            raise ValidationError(f"{item_id}: accepted integration requires an atomic Master-accepted cursor")
        planning_blockers = [dependency for dependency in tasks[item_id].dependencies if tasks[dependency].state != "x"]
        if planning_blockers and (
            item["claim_id"] is not None
            or item["startup"] is not None
            or item["live"] is True
            or item["running"] is True
            or any(item[key] is not None for key in ("handoff", "integration", "repair"))
        ):
            raise ValidationError(
                f"{item_id}: planning-dependency-blocked item occupies runtime lifecycle state"
            )
        active_process: dict[str, Any] | None = None
        if startup_evidence is not None and startup_evidence["process_identity"] is not None:
            active_process = startup_evidence["process_identity"]
        elif live_evidence is not None:
            active_process = live_evidence
        if active_process is not None:
            task_root = runtime_item_root(item)
            assert task_root is not None
            unique_values = (
                (active_sessions, active_process["session"], "session"),
                (active_processes, (active_process["pane_pid"], active_process["process_start_ticks"]), "process"),
                (active_sockets, active_process["tmux_socket"], "tmux socket"),
                (active_homes, active_process["codex_home"], "Codex home"),
                (active_task_roots, task_root, "task root"),
            )
            for seen_values, value, identity_label in unique_values:
                if value in seen_values:
                    raise ValidationError(f"runtime simultaneously reuses active {identity_label} identity")
                seen_values.add(value)
        if live_evidence is not None:
            for seen_values, value, identity_label in (
                (active_threads, live_evidence["thread_id"], "thread"),
                (active_goals, live_evidence["goal_id"], "goal"),
            ):
                if value in seen_values:
                    raise ValidationError(f"runtime simultaneously reuses active {identity_label} identity")
                seen_values.add(value)
        items[item_id] = item
    if set(items) != set(tasks):
        raise ValidationError(
            "runtime snapshot item coverage differs: "
            f"missing={sorted(set(tasks) - set(items))}, extra={sorted(set(items) - set(tasks))}"
        )
    logical_claims = len({item["claim_id"] for item in items.values() if item["claim_id"] is not None})
    authenticated_live = sum(item["live"] is True for item in items.values())
    running_turns = sum(item["running"] is True for item in items.values())
    startup_reservations = sum(item["startup"] is not None for item in items.values())
    if logical_claims > admission["logical_claim_target"]:
        raise ValidationError("runtime logical claims exceed their frozen target")
    if authenticated_live > admission["authenticated_live_target"]:
        raise ValidationError("runtime authenticated live goals exceed their frozen target")
    if running_turns > admission["running_turn_target"]:
        raise ValidationError("runtime running turns exceed their frozen target")
    if startup_reservations > admission["startup_reservation_target"]:
        raise ValidationError("runtime startup reservations exceed their frozen target")
    integrating = sum(item["integration"] == "integrating" for item in items.values())
    if integrating > admission["master_integration_target"]:
        raise ValidationError("runtime integrating claims exceed the frozen Master integration target")
    actively_starting = sum(
        item["startup"] in (STARTUP_STATES - {"reserved"}) for item in items.values()
    )
    occupancy = authenticated_live + actively_starting
    nonoccupancy_claims = sum(
        item["claim_id"] is not None
        and item["live"] is not True
        and item["startup"] not in (STARTUP_STATES - {"reserved"})
        for item in items.values()
    )
    logical_availability = max(0, admission["logical_claim_target"] - nonoccupancy_claims)
    if bindings["logical_available"]["limit"] != logical_availability:
        raise ValidationError("runtime logical availability does not subtract nonoccupancy active claims")
    if admission["admitted_target"] + nonoccupancy_claims > admission["logical_claim_target"]:
        raise ValidationError("runtime admitted target plus nonoccupancy claims exceeds the logical cap")
    if occupancy > admission["admitted_target"]:
        raise ValidationError("runtime live plus starting lanes exceed the recomputed admitted target")
    target_reduced = admission["admitted_target"] < admission["requested_target"]
    occupancy_underfilled = occupancy < admission["admitted_target"]
    if target_reduced != (underfill is not None):
        raise ValidationError("runtime target reduction reason presence differs from effective target reduction")
    if occupancy_underfilled != (occupancy_underfill is not None):
        raise ValidationError("runtime occupancy underfill requires a separate stop reason")
    if underfill is not None:
        limiter_kind_map = {
            "eligible": "dependency",
            "logical_available": "resource",
            "host_resource": "resource",
            "conflict": "conflict",
            "external_limit": "external_limit",
            "route": "route",
            "validator": "validator",
            "budget": "budget",
        }
        minimum = admission["admitted_target"]
        allowed_underfill_kinds = {
            limiter_kind_map[kind]
            for kind, binding in bindings.items()
            if binding["limit"] == minimum and kind in limiter_kind_map
        }
        if underfill["kind"] not in allowed_underfill_kinds:
            raise ValidationError(
                "runtime underfill reason kind does not match the recomputed binding limiter"
            )
        target_evidence = underfill["evidence"]
        _validate_runtime_path(target_evidence["source"], "runtime underfill evidence source")
        expected_fields = {"kind", "reason", "observed_at", "admitted_target", "requested_target"}
        if set(target_evidence["payload"]) != expected_fields:
            raise ValidationError("runtime target-reduction evidence fields differ")
        if (
            target_evidence["payload"]["observed_at"] != snapshot["observed_at"]
            or target_evidence["payload"]["admitted_target"] != admission["admitted_target"]
            or target_evidence["payload"]["requested_target"] != admission["requested_target"]
        ):
            raise ValidationError("runtime target-reduction evidence is stale or mismatched")
    if occupancy_underfill is not None:
        if occupancy_underfill["kind"] not in {"startup", "no_progress", "invocation_deadline"}:
            raise ValidationError("runtime occupancy underfill reason is not a startup/progress/deadline reason")
        occupancy_evidence = occupancy_underfill["evidence"]
        _validate_runtime_path(
            occupancy_evidence["source"], "runtime occupancy-underfill evidence source"
        )
        expected_fields = {
            "kind", "reason", "observed_at", "occupancy", "admitted_target",
            "pump_started_at", "pump_deadline_at", "reconciliation_iteration",
            "no_progress_limit",
        }
        if set(occupancy_evidence["payload"]) != expected_fields:
            raise ValidationError("runtime occupancy-underfill evidence fields differ")
        if (
            occupancy_evidence["payload"]["observed_at"] != snapshot["observed_at"]
            or occupancy_evidence["payload"]["occupancy"] != occupancy
            or occupancy_evidence["payload"]["admitted_target"] != admission["admitted_target"]
        ):
            raise ValidationError("runtime occupancy-underfill evidence is stale or mismatched")
        occupancy_payload = occupancy_evidence["payload"]
        _validate_rfc3339_utc(occupancy_payload["pump_started_at"], "occupancy pump_started_at")
        _validate_rfc3339_utc(occupancy_payload["pump_deadline_at"], "occupancy pump_deadline_at")
        pump_started = datetime.strptime(occupancy_payload["pump_started_at"], "%Y-%m-%dT%H:%M:%SZ")
        pump_deadline = datetime.strptime(occupancy_payload["pump_deadline_at"], "%Y-%m-%dT%H:%M:%SZ")
        if (
            not isinstance(occupancy_payload["reconciliation_iteration"], int)
            or isinstance(occupancy_payload["reconciliation_iteration"], bool)
            or occupancy_payload["reconciliation_iteration"] < 0
            or occupancy_payload["no_progress_limit"] != execution_spec.no_progress_iterations
            or pump_started > observed_at
            or int((pump_deadline - pump_started).total_seconds())
            > execution_spec.admission_pump_budget_seconds
        ):
            raise ValidationError("runtime occupancy-underfill pump evidence is inconsistent")
        if (
            occupancy_underfill["kind"] == "no_progress"
            and occupancy_payload["reconciliation_iteration"]
            < occupancy_payload["no_progress_limit"]
        ):
            raise ValidationError("runtime no-progress stop predates the frozen iteration guard")
        if (
            occupancy_underfill["kind"] == "invocation_deadline"
            and observed_at < pump_deadline
        ):
            raise ValidationError("runtime invocation-deadline stop predates its deadline")
        if (
            occupancy_underfill["kind"] == "startup"
            and not any(item["startup"] is not None for item in items.values())
        ):
            raise ValidationError("runtime startup underfill reason has no observed startup lane")
    if snapshot["cleanup_state"] not in {None, "not_started"}:
        if any(task.state != "x" for task in tasks.values()):
            raise ValidationError("runtime cleanup transition exists before all rows are Master accepted")
        if any(
            item["claim_id"] is not None
            or item["startup"] is not None
            or item["live"] is True
            or item["running"] is True
            or item["handoff"] is not None
            or item["integration"] is not None
            or item["repair"] is not None
            or item["runtime_block"] is not None
            for item in items.values()
        ):
            raise ValidationError("runtime cleanup transition coexists with worker or queue lifecycle state")
        assert pre_cleanup_receipt_text is not None
        pre_cleanup = parse_pre_cleanup_receipt(pre_cleanup_receipt_text, blueprint_text, tasks)
        expected_cleanup_arm = {
            "path": PRE_CLEANUP_RECEIPT.relative_to(ROOT).as_posix(),
            "receipt_id": pre_cleanup["receipt_id"],
            "sha256": sha256_text(pre_cleanup_receipt_text),
        }
        if cleanup_arm != expected_cleanup_arm:
            raise ValidationError("runtime cleanup arm reference is stale or mismatched")
    for item_id, task in tasks.items():
        if task.state == "_" and items[item_id]["handoff"] not in {"harvested", "finished"}:
            raise ValidationError(f"{item_id}: self-tested cursor lacks a durable harvested handoff")
    expected_snapshot_id = content_addressed_id("stage3-runtime", snapshot, "snapshot_id")
    if snapshot["snapshot_id"] != expected_snapshot_id:
        raise ValidationError("runtime snapshot ID is not its canonical content digest")
    snapshot["items_by_id"] = items
    return snapshot


def parse_pre_cleanup_receipt(
    pre_cleanup_text: str,
    blueprint_text: str,
    tasks: dict[str, Task],
) -> dict[str, Any]:
    receipt = parse_json_strict(pre_cleanup_text, "pre-cleanup receipt")
    receipt = _require_exact_keys(receipt, PRE_CLEANUP_KEYS, "pre-cleanup receipt")
    if receipt["schema_version"] != PRE_CLEANUP_RECEIPT_SCHEMA:
        raise ValidationError("pre-cleanup receipt schema differs")
    if receipt["state"] != "cleanup_pending":
        raise ValidationError("pre-cleanup receipt is not armed in cleanup_pending state")
    _validate_rfc3339_utc(receipt["armed_at"], "pre-cleanup armed_at")
    if receipt["blueprint_path"] != BLUEPRINT.relative_to(ROOT).as_posix():
        raise ValidationError("pre-cleanup receipt blueprint path differs")
    if receipt["blueprint_version"] != VERSION:
        raise ValidationError("pre-cleanup receipt blueprint version differs")
    if receipt["raw_blueprint_sha256"] != sha256_text(blueprint_text):
        raise ValidationError("pre-cleanup receipt raw Blueprint digest is stale")
    spec_region = exact_marked_region(blueprint_text, SPEC_BEGIN, SPEC_END, "execution specification")
    if receipt["execution_spec_region_sha256"] != sha256_text(spec_region):
        raise ValidationError("pre-cleanup receipt execution specification digest is stale")
    if receipt["rel005_state"] != "master_accepted" or tasks["S3-REL-005"].state != "x":
        raise ValidationError("pre-cleanup receipt does not bind accepted S3-REL-005")
    if receipt["all_other_items_master_accepted"] is not True or any(
        task.state != "x" for item_id, task in tasks.items() if item_id != "S3-REL-005"
    ):
        raise ValidationError("pre-cleanup receipt does not bind acceptance of every other item")
    unfinished = _require_exact_keys(
        receipt["unfinished"], CLEANUP_UNFINISHED_KEYS, "pre-cleanup unfinished"
    )
    if unfinished != {"not_done": 0, "self_tested": 0}:
        raise ValidationError("pre-cleanup receipt reports unfinished checklist work")
    queues = _require_exact_keys(receipt["queues_empty"], CLEANUP_QUEUE_KEYS, "pre-cleanup queues_empty")
    if any(value is not True for value in queues.values()):
        raise ValidationError("pre-cleanup receipt reports a nonempty durable queue")
    inventory = _require_exact_keys(
        receipt["teardown_inventory"], CLEANUP_ABSENCE_KEYS, "pre-cleanup teardown inventory"
    )
    if receipt["teardown_inventory_sha256"] != canonical_json_sha256(inventory):
        raise ValidationError("pre-cleanup teardown inventory digest differs")
    if inventory["cron"] != [{
        "begin_marker": "# BEGIN AWESOME_THEOREMS_STAGE3_EXECUTION_V1",
        "end_marker": "# END AWESOME_THEOREMS_STAGE3_EXECUTION_V1",
    }]:
        raise ValidationError("pre-cleanup teardown inventory cron identity differs")
    if not isinstance(inventory["scheduler"], list) or len(inventory["scheduler"]) != 1:
        raise ValidationError("pre-cleanup teardown inventory lacks the exact scheduler identity")
    scheduler_identity = _require_exact_keys(
        inventory["scheduler"][0],
        {"pid", "process_start_ticks", "cwd", "argv"},
        "pre-cleanup scheduler identity",
    )
    if (
        not isinstance(scheduler_identity["pid"], int)
        or isinstance(scheduler_identity["pid"], bool)
        or scheduler_identity["pid"] <= 0
        or not isinstance(scheduler_identity["process_start_ticks"], int)
        or isinstance(scheduler_identity["process_start_ticks"], bool)
        or scheduler_identity["process_start_ticks"] <= 0
        or scheduler_identity["cwd"] != "."
        or scheduler_identity["argv"] != ["python3", "scripts/stage3_execution_scheduler.py"]
    ):
        raise ValidationError("pre-cleanup scheduler identity is malformed")
    if inventory["task_processes"] != [] or inventory["tmux_sockets"] != []:
        raise ValidationError("pre-cleanup all-accepted inventory still contains task/Tmux identities")
    if inventory["locks"] != [".ops/stage3-execution-v1/locks/scheduler.lock"]:
        raise ValidationError("pre-cleanup teardown lock inventory differs")
    if inventory["runtime_root"] != [".ops/stage3-execution-v1/"]:
        raise ValidationError("pre-cleanup runtime-root inventory differs")
    projection = _require_exact_keys(
        receipt["final_pre_teardown_projection"],
        PRE_CLEANUP_PROJECTION_KEYS,
        "pre-cleanup final projection",
    )
    if not isinstance(projection["projection_input_sha256"], str) or not HEX_SHA256_RE.fullmatch(
        projection["projection_input_sha256"]
    ):
        raise ValidationError("pre-cleanup final projection has malformed projection_input_sha256")
    if projection["snapshot_id"] != f"stage3-projection/{projection['projection_input_sha256']}":
        raise ValidationError("pre-cleanup final projection snapshot ID/digest differ")
    _validate_rfc3339_utc(projection["generated_at"], "pre-cleanup final projection generated_at")
    armed = datetime.strptime(receipt["armed_at"], "%Y-%m-%dT%H:%M:%SZ")
    projected = datetime.strptime(projection["generated_at"], "%Y-%m-%dT%H:%M:%SZ")
    if projected > armed:
        raise ValidationError("pre-cleanup final projection was generated after cleanup was armed")
    surfaces = _require_exact_keys(
        projection["surfaces"], PRE_CLEANUP_SURFACE_NAMES, "pre-cleanup archived surfaces"
    )
    expected_surface_paths = {
        "gantt": GANTT.relative_to(ROOT).as_posix(),
        "status": STATUS.relative_to(ROOT).as_posix(),
        "kanban": KANBAN.relative_to(ROOT).as_posix(),
    }
    archived_texts: dict[str, str] = {}
    for name in sorted(PRE_CLEANUP_SURFACE_NAMES):
        surface = _require_exact_keys(
            surfaces[name], PRE_CLEANUP_SURFACE_KEYS, f"pre-cleanup archived {name}"
        )
        if surface["path"] != expected_surface_paths[name]:
            raise ValidationError(f"pre-cleanup archived {name} path differs")
        if not isinstance(surface["text"], str):
            raise ValidationError(f"pre-cleanup archived {name} bytes are not UTF-8 text")
        if surface["sha256"] != sha256_text(surface["text"]):
            raise ValidationError(f"pre-cleanup archived {name} digest differs from exact bytes")
        archived_texts[name] = surface["text"]
    runtime_ref = _require_exact_keys(
        projection["runtime_snapshot"], PRE_CLEANUP_RUNTIME_KEYS,
        "pre-cleanup archived runtime snapshot",
    )
    if runtime_ref["path"] != RUNTIME_SNAPSHOT.relative_to(ROOT).as_posix():
        raise ValidationError("pre-cleanup archived runtime snapshot path differs")
    if not isinstance(runtime_ref["text"], str) or runtime_ref["sha256"] != sha256_text(runtime_ref["text"]):
        raise ValidationError("pre-cleanup archived runtime snapshot digest differs from exact bytes")
    archived_runtime = parse_runtime_snapshot(runtime_ref["text"], tasks, blueprint_text)
    if runtime_ref["snapshot_id"] != archived_runtime["snapshot_id"]:
        raise ValidationError("pre-cleanup archived runtime snapshot ID differs")
    validate_texts(
        blueprint_text,
        archived_texts["gantt"],
        archived_texts["status"],
        archived_texts["kanban"],
        runtime_ref["text"],
    )
    archived_metadata = parse_surface_metadata(archived_texts["gantt"], "pre-cleanup Gantt")
    if (
        archived_metadata["snapshot_id"] != projection["snapshot_id"]
        or archived_metadata["projection_input_sha256"] != projection["projection_input_sha256"]
        or archived_metadata["generated_at"] != projection["generated_at"]
    ):
        raise ValidationError("pre-cleanup archived projection metadata differs from its receipt summary")
    expected_id = content_addressed_id("stage3-pre-cleanup", receipt, "receipt_id")
    if receipt["receipt_id"] != expected_id:
        raise ValidationError("pre-cleanup receipt ID is not its canonical content digest")
    return receipt


def validate_runtime_fresh_now(
    runtime_snapshot: dict[str, Any],
    blueprint_text: str,
    *,
    now: datetime | None = None,
) -> None:
    """Enforce wall-clock freshness only for canonical active-runtime entrypoints."""

    if not any(
        item["startup"] is not None or item["live"] is True or item["running"] is True
        for item in runtime_snapshot["items_by_id"].values()
    ):
        return
    if now is None:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
    elif now.tzinfo is not None:
        now = now.astimezone(timezone.utc).replace(tzinfo=None)
    observed = datetime.strptime(runtime_snapshot["observed_at"], "%Y-%m-%dT%H:%M:%SZ")
    maximum_age = parse_execution_spec(blueprint_text).cadence_seconds * 2
    if observed > now + timedelta(seconds=5) or now - observed > timedelta(seconds=maximum_age):
        raise ValidationError("active runtime snapshot is stale or future relative to current validation")


def parse_cleanup_receipt(
    cleanup_receipt_text: str,
    blueprint_text: str,
    tasks: dict[str, Task],
    *,
    pre_cleanup_receipt_text: str | None = None,
    verifier_script_bytes: bytes | None = None,
) -> dict[str, Any]:
    receipt = parse_json_strict(cleanup_receipt_text, "cleanup receipt")
    receipt = _require_exact_keys(receipt, CLEANUP_RECEIPT_KEYS, "cleanup receipt")
    if receipt["schema_version"] != CLEANUP_RECEIPT_SCHEMA:
        raise ValidationError("cleanup receipt schema differs")
    _validate_nullable_string(receipt["receipt_id"], "cleanup receipt ID")
    if receipt["receipt_id"] is None or not SAFE_RUNTIME_ID_RE.fullmatch(receipt["receipt_id"]):
        raise ValidationError("cleanup receipt ID must use the stable safe-ID grammar")
    for key in ("teardown_completed_at", "verified_at", "issued_at"):
        _validate_rfc3339_utc(receipt[key], f"cleanup {key}")
    teardown = datetime.strptime(receipt["teardown_completed_at"], "%Y-%m-%dT%H:%M:%SZ")
    verified = datetime.strptime(receipt["verified_at"], "%Y-%m-%dT%H:%M:%SZ")
    issued = datetime.strptime(receipt["issued_at"], "%Y-%m-%dT%H:%M:%SZ")
    if receipt["required_cadence_seconds"] != 120:
        raise ValidationError("cleanup receipt does not bind the frozen 120-second scheduler cadence")
    if (verified - teardown).total_seconds() < receipt["required_cadence_seconds"]:
        raise ValidationError("cleanup absence verification did not wait one frozen scheduler cadence")
    if issued < verified:
        raise ValidationError("cleanup receipt was issued before external absence verification")
    if receipt["blueprint_path"] != BLUEPRINT.relative_to(ROOT).as_posix():
        raise ValidationError("cleanup receipt blueprint path differs")
    if receipt["blueprint_version"] != VERSION:
        raise ValidationError("cleanup receipt blueprint version differs")
    if receipt["raw_blueprint_sha256"] != sha256_text(blueprint_text):
        raise ValidationError("cleanup receipt raw Blueprint digest is stale")
    spec_region = exact_marked_region(blueprint_text, SPEC_BEGIN, SPEC_END, "execution specification")
    if receipt["execution_spec_region_sha256"] != sha256_text(spec_region):
        raise ValidationError("cleanup receipt execution specification digest is stale")
    if receipt["all_checklist_items_master_accepted"] is not True:
        raise ValidationError("cleanup receipt does not attest all checklist items accepted")
    if any(task.state != "x" for task in tasks.values()):
        raise ValidationError("cleanup receipt exists before every checklist item is Master accepted")
    if pre_cleanup_receipt_text is None:
        try:
            pre_cleanup_receipt_text = PRE_CLEANUP_RECEIPT.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise ValidationError("canonical pre-cleanup cleanup_pending receipt is absent") from exc
    pre_cleanup = parse_pre_cleanup_receipt(pre_cleanup_receipt_text, blueprint_text, tasks)
    pre_ref = _require_exact_keys(receipt["pre_cleanup"], CLEANUP_PRE_REF_KEYS, "cleanup pre_cleanup")
    expected_pre_ref = {
        "path": PRE_CLEANUP_RECEIPT.relative_to(ROOT).as_posix(),
        "receipt_id": pre_cleanup["receipt_id"],
        "sha256": sha256_text(pre_cleanup_receipt_text),
    }
    if pre_ref != expected_pre_ref:
        raise ValidationError("cleanup receipt pre-cleanup reference is missing, stale, or mismatched")
    pre_armed = datetime.strptime(pre_cleanup["armed_at"], "%Y-%m-%dT%H:%M:%SZ")
    if teardown < pre_armed:
        raise ValidationError("cleanup teardown predates the canonical cleanup_pending arm")
    controller = _require_exact_keys(
        receipt["controller_identity"], CLEANUP_CONTROLLER_KEYS, "cleanup controller_identity"
    )
    if controller != {
        "runtime_root": ".ops/stage3-execution-v1/",
        "cron_begin_marker": "# BEGIN AWESOME_THEOREMS_STAGE3_EXECUTION_V1",
        "cron_end_marker": "# END AWESOME_THEOREMS_STAGE3_EXECUTION_V1",
    }:
        raise ValidationError("cleanup receipt controller identity differs from the frozen specification")
    verifier = _require_exact_keys(receipt["verifier"], CLEANUP_VERIFIER_KEYS, "cleanup verifier")
    if not isinstance(verifier["identity"], str) or not verifier["identity"].strip():
        raise ValidationError("cleanup receipt lacks an external verifier identity")
    if verifier["independent_of_controller"] is not True:
        raise ValidationError("cleanup receipt verifier is not independent of the controller")
    expected_script_path = CLEANUP_VERIFIER_SCRIPT.relative_to(ROOT).as_posix()
    if verifier["script_path"] != expected_script_path:
        raise ValidationError("cleanup receipt names a noncanonical verifier script")
    if verifier_script_bytes is None:
        try:
            verifier_script_bytes = CLEANUP_VERIFIER_SCRIPT.read_bytes()
        except OSError as exc:
            raise ValidationError("cleanup verifier script is absent at its frozen repository path") from exc
    if verifier["script_sha256"] != sha256_bytes(verifier_script_bytes):
        raise ValidationError("cleanup verifier script digest differs from the frozen repository bytes")
    if not isinstance(verifier["commands"], list) or len(verifier["commands"]) != 1:
        raise ValidationError("cleanup receipt must contain exactly one canonical verifier command outcome")
    command = _require_exact_keys(verifier["commands"][0], CLEANUP_COMMAND_KEYS, "cleanup verifier command")
    expected_argv = [
        "python3",
        expected_script_path,
        "--verify-absence",
        "--format=json",
    ]
    if command["argv"] != expected_argv or command["cwd"] != ".":
        raise ValidationError("cleanup verifier command argv/cwd differs from the frozen side-effect-free route")
    if command["exit_code"] != 0:
        raise ValidationError("cleanup verifier command failed")
    if not isinstance(command["stdout"], str) or not isinstance(command["stderr"], str):
        raise ValidationError("cleanup verifier stdout/stderr must be exact UTF-8 strings")
    if command["stdout_sha256"] != sha256_text(command["stdout"]):
        raise ValidationError("cleanup verifier stdout byte digest differs")
    if command["stderr"] != "" or command["stderr_sha256"] != sha256_text(""):
        raise ValidationError("cleanup verifier produced unbound stderr")
    stdout_payload = parse_json_strict(command["stdout"], "cleanup verifier stdout")
    stdout_payload = _require_exact_keys(
        stdout_payload, CLEANUP_VERIFIER_OUTPUT_KEYS, "cleanup verifier stdout"
    )
    canonical_stdout = _canonical_json_bytes(stdout_payload).decode("utf-8") + "\n"
    if command["stdout"] != canonical_stdout:
        raise ValidationError("cleanup verifier stdout is not canonical JSON plus one newline")
    if command["stdout_payload_sha256"] != canonical_json_sha256(stdout_payload):
        raise ValidationError("cleanup verifier stdout payload digest differs")
    if stdout_payload["schema_version"] != "stage3-cleanup-absence/1.0":
        raise ValidationError("cleanup verifier stdout schema differs")
    if stdout_payload["controller_identity"] != controller:
        raise ValidationError("cleanup verifier stdout controller identity differs")
    if stdout_payload["inventory_sha256"] != pre_cleanup["teardown_inventory_sha256"]:
        raise ValidationError("cleanup verifier stdout does not bind the pre-cleanup identity inventory")
    _validate_rfc3339_utc(stdout_payload["observed_at"], "cleanup verifier stdout observed_at")
    if stdout_payload["observed_at"] != receipt["verified_at"]:
        raise ValidationError("cleanup verifier stdout observation time differs from the receipt")
    queries = _require_exact_keys(
        stdout_payload["queries"], CLEANUP_ABSENCE_KEYS, "cleanup verifier stdout queries"
    )
    for key, raw_query in queries.items():
        query = _require_exact_keys(
            raw_query, CLEANUP_ABSENCE_EVIDENCE_KEYS, f"cleanup verifier stdout query {key}"
        )
        if query["query"] != CLEANUP_QUERY_NAMES[key]:
            raise ValidationError(f"cleanup verifier stdout query identity differs: {key}")
        if query["targets"] != pre_cleanup["teardown_inventory"][key]:
            raise ValidationError(f"cleanup verifier stdout query targets differ: {key}")
        if not isinstance(query["raw_result"], list):
            raise ValidationError(f"cleanup verifier stdout raw query result is not an array: {key}")
        if query["absent"] is not True or query["raw_result"]:
            raise ValidationError(f"cleanup verifier stdout found surviving controller state: {key}")
    _validate_rfc3339_utc(command["started_at"], "cleanup verifier command started_at")
    _validate_rfc3339_utc(command["finished_at"], "cleanup verifier command finished_at")
    started = datetime.strptime(command["started_at"], "%Y-%m-%dT%H:%M:%SZ")
    finished = datetime.strptime(command["finished_at"], "%Y-%m-%dT%H:%M:%SZ")
    verifier_observed = datetime.strptime(stdout_payload["observed_at"], "%Y-%m-%dT%H:%M:%SZ")
    earliest_verification = teardown + timedelta(seconds=receipt["required_cadence_seconds"])
    if (
        started < earliest_verification
        or finished < started
        or not (started <= verifier_observed <= finished)
        or finished != verified
    ):
        raise ValidationError("cleanup verifier command timing is inconsistent")
    unfinished = _require_exact_keys(receipt["unfinished"], CLEANUP_UNFINISHED_KEYS, "cleanup unfinished")
    if unfinished != {"not_done": 0, "self_tested": 0}:
        raise ValidationError("cleanup receipt reports unfinished checklist work")
    queues = _require_exact_keys(receipt["queues_empty"], CLEANUP_QUEUE_KEYS, "cleanup queues_empty")
    if any(value is not True for value in queues.values()):
        raise ValidationError("cleanup receipt reports a nonempty durable queue")
    absence = _require_exact_keys(receipt["absence_recheck"], CLEANUP_ABSENCE_KEYS, "cleanup absence_recheck")
    if absence != queries:
        raise ValidationError("cleanup absence_recheck differs from parsed canonical verifier stdout")
    expected_receipt_id = content_addressed_id("stage3-cleanup", receipt, "receipt_id")
    if receipt["receipt_id"] != expected_receipt_id:
        raise ValidationError("cleanup receipt ID is not its canonical content digest")
    return receipt


def parse_release_validation(
    release_validation_text: str,
    blueprint_text: str,
    tasks: dict[str, Task],
) -> dict[str, Any]:
    """Validate the terminal fixed-matrix/current-repository receipt."""

    receipt = _require_exact_keys(
        parse_json_strict(release_validation_text, "release validation"),
        RELEASE_VALIDATION_KEYS,
        "release validation",
    )
    if receipt["schema_version"] != RELEASE_VALIDATION_SCHEMA:
        raise ValidationError("release validation schema differs")
    if receipt["blueprint_version"] != VERSION:
        raise ValidationError("release validation Blueprint version differs")
    if receipt["raw_blueprint_sha256"] != sha256_text(blueprint_text):
        raise ValidationError("release validation does not bind the accepted Blueprint bytes")
    spec_region = exact_marked_region(
        blueprint_text, SPEC_BEGIN, SPEC_END, "execution specification"
    )
    if receipt["execution_spec_region_sha256"] != sha256_text(spec_region):
        raise ValidationError("release validation execution-specification digest is stale")
    for key in ("acceptance_contract_sha256",):
        if not isinstance(receipt[key], str) or not HEX_SHA256_RE.fullmatch(receipt[key]):
            raise ValidationError(f"release validation {key} is malformed")
    merkle = _require_exact_keys(
        receipt["accepted_repository_merkle"],
        REPOSITORY_MERKLE_KEYS,
        "accepted repository Merkle",
    )
    if (
        merkle["algorithm"] != "sha256-framed-path-mode-bytes-v1"
        or not isinstance(merkle["entry_count"], int)
        or isinstance(merkle["entry_count"], bool)
        or merkle["entry_count"] <= 0
        or not isinstance(merkle["sha256"], str)
        or not HEX_SHA256_RE.fullmatch(merkle["sha256"])
    ):
        raise ValidationError("accepted repository Merkle is malformed")
    item_receipts = receipt["item_master_receipts"]
    if not isinstance(item_receipts, dict) or set(item_receipts) != set(tasks):
        raise ValidationError("release validation Master-receipt index does not cover every item exactly")
    if any(not isinstance(value, str) or not HEX_SHA256_RE.fullmatch(value) for value in item_receipts.values()):
        raise ValidationError("release validation Master-receipt index contains a malformed digest")
    runs = receipt["matrix_runs"]
    if not isinstance(runs, list) or len(runs) != 2:
        raise ValidationError("release validation requires exactly two fixed-matrix runs")
    runner_ids: set[str] = set()
    output_digests: set[str] = set()
    for index, raw_run in enumerate(runs):
        run = _require_exact_keys(raw_run, MATRIX_RUN_KEYS, f"release validation run {index}")
        if not isinstance(run["runner_id"], str) or not run["runner_id"].strip():
            raise ValidationError("release validation runner ID is empty")
        runner_ids.add(run["runner_id"])
        if run["network"] != "denied" or run["cache"] != "private_empty":
            raise ValidationError("release validation run is not clean and network-denied")
        for key in ("argv_sha256", "inputs_sha256", "outputs_sha256", "raw_log_sha256"):
            if not isinstance(run[key], str) or not HEX_SHA256_RE.fullmatch(run[key]):
                raise ValidationError(f"release validation run {index} has malformed {key}")
        output_digests.add(run["outputs_sha256"])
        if run["exit_code"] != 0 or run["passed"] is not True:
            raise ValidationError("release validation matrix run did not pass")
    if len(runner_ids) != 2 or len(output_digests) != 1:
        raise ValidationError("release validation lacks two distinct runners with matching outputs")
    if receipt["all_passed"] is not True:
        raise ValidationError("release validation does not report terminal success")
    expected_id = content_addressed_id("stage3-release-validation", receipt, "receipt_id")
    if receipt["receipt_id"] != expected_id:
        raise ValidationError("release validation receipt ID is not its canonical content digest")
    return receipt


def _state_name(state: str) -> str:
    return {" ": "not_done", "_": "self_tested", "x": "master_accepted"}[state]


def planning_projection(tasks: dict[str, Task]) -> dict[str, Any]:
    implementation_ready: list[str] = []
    validation_preparation: list[str] = []
    integration_ready: list[str] = []
    dependency_blocked: list[dict[str, Any]] = []
    accepted: list[str] = []
    for task in sorted(tasks.values(), key=lambda value: value.item_id):
        blockers = [dependency for dependency in task.dependencies if tasks[dependency].state != "x"]
        if task.state == "x":
            accepted.append(task.item_id)
        elif task.state == "_":
            integration_ready.append(task.item_id)
        elif not blockers:
            implementation_ready.append(task.item_id)
        if task.state == " " and blockers and all(tasks[dependency].state in {"_", "x"} for dependency in task.dependencies):
            validation_preparation.append(task.item_id)
        if task.state != "x" and blockers:
            dependency_blocked.append({"id": task.item_id, "blockers": blockers})
    return {
        "frontiers": {
            "implementation_ready": implementation_ready,
            "validation_preparation": validation_preparation,
            "integration_ready": integration_ready,
        },
        "dependency_blocked": dependency_blocked,
        "accepted": accepted,
    }


def unavailable_timing() -> dict[str, Any]:
    return {
        "status": "unscheduled",
        "start": None,
        "end": None,
        "duration_seconds": None,
        "source": None,
    }


def expected_status_items(
    tasks: dict[str, Task], runtime_snapshot: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    runtime_items = runtime_snapshot["items_by_id"] if runtime_snapshot is not None else {}
    result: list[dict[str, Any]] = []
    for task in sorted(tasks.values(), key=lambda value: value.item_id):
        runtime = runtime_items.get(task.item_id)
        blockers = [dependency for dependency in task.dependencies if tasks[dependency].state != "x"]
        result.append(
            {
                "id": task.item_id,
                "state": _state_name(task.state),
                "depends_on": list(task.dependencies),
                "owned_paths": list(task.owned_paths),
                "claim": None if runtime is None else runtime["claim_id"],
                "run": None if runtime is None else runtime["run_id"],
                "owner": None if runtime is None else runtime["owner"],
                "startup": None if runtime is None else runtime["startup"],
                "live": None if runtime is None else runtime["live"],
                "running": None if runtime is None else runtime["running"],
                "handoff": None if runtime is None else runtime["handoff"],
                "integration": None if runtime is None else runtime["integration"],
                "repair": None if runtime is None else runtime["repair"],
                "planning_blockers": blockers,
                "runtime_block": None if runtime is None else runtime["runtime_block"],
                "timing": unavailable_timing() if runtime is None else runtime["timing"],
            }
        )
    return result


def expected_runtime_projection(
    runtime_snapshot: dict[str, Any] | None = None,
    cleanup_receipt: dict[str, Any] | None = None,
) -> dict[str, Any]:
    count_keys = (
        "logical_claims",
        "reserved",
        "starting",
        "authenticated_live_goals",
        "running_turns",
        "finished_handoffs",
        "dependency_blocked",
        "conflict_blocked",
        "startup_blocked",
        "resource_blocked",
        "external_limit_blocked",
        "route_blocked",
        "validator_blocked",
        "budget_blocked",
        "integration_backlog",
        "repair_backlog",
    )
    admission_keys = (
        "logical_claim_target",
        "startup_reservation_target",
        "authenticated_live_target",
        "running_turn_target",
        "admitted_target",
        "eligible_ready_count",
        "requested_target",
        "host_admissible_target",
        "master_integration_target",
        "cpu_validator_lease_target",
        "active_cpu_validator_leases",
        "effective_target_bindings",
        "logical_saturation",
        "admitted_saturation",
        "underfill_stop_reason",
        "occupancy_underfill_reason",
    )
    if runtime_snapshot is None:
        return {
            "availability": "runtime_unavailable",
            "snapshot_id": None,
            "observed_at": None,
            **{key: None for key in count_keys},
            **{key: None for key in admission_keys},
            "last_progress": None,
            "cleanup_state": "complete" if cleanup_receipt is not None else "not_started",
        }
    items = list(runtime_snapshot["items_by_id"].values())
    blocks = Counter(
        item["runtime_block"]["kind"]
        for item in items
        if item["runtime_block"] is not None
    )
    admission = runtime_snapshot["admission"]
    logical_claims = len({item["claim_id"] for item in items if item["claim_id"] is not None})
    authenticated_live = sum(item["live"] is True for item in items)
    logical_target = admission["logical_claim_target"]
    admitted_target = admission["admitted_target"]
    return {
        "availability": "observed",
        "snapshot_id": runtime_snapshot["snapshot_id"],
        "observed_at": runtime_snapshot["observed_at"],
        "logical_claims": logical_claims,
        "reserved": sum(item["startup"] == "reserved" for item in items),
        "starting": sum(item["startup"] in (STARTUP_STATES - {"reserved"}) for item in items),
        "authenticated_live_goals": sum(item["live"] is True for item in items),
        "running_turns": sum(item["running"] is True for item in items),
        "finished_handoffs": sum(item["handoff"] in {"harvested", "finished"} for item in items),
        "dependency_blocked": blocks["dependency"],
        "conflict_blocked": blocks["conflict"],
        "startup_blocked": blocks["startup"],
        "resource_blocked": blocks["resource"],
        "external_limit_blocked": blocks["external_limit"],
        "route_blocked": blocks["route"],
        "validator_blocked": blocks["validator"],
        "budget_blocked": blocks["budget"],
        "integration_backlog": sum(item["integration"] in {"queued", "integrating", "failed"} for item in items),
        "repair_backlog": sum(item["repair"] in {"queued", "active", "exhausted"} for item in items),
        "logical_claim_target": logical_target,
        "startup_reservation_target": admission["startup_reservation_target"],
        "authenticated_live_target": admission["authenticated_live_target"],
        "running_turn_target": admission["running_turn_target"],
        "admitted_target": admitted_target,
        "eligible_ready_count": admission["eligible_ready_count"],
        "requested_target": admission["requested_target"],
        "host_admissible_target": admission["host_admissible_target"],
        "master_integration_target": admission["master_integration_target"],
        "cpu_validator_lease_target": admission["cpu_validator_lease_target"],
        "active_cpu_validator_leases": admission["active_cpu_validator_leases"],
        "effective_target_bindings": admission["effective_target_bindings"],
        "logical_saturation": None if logical_target == 0 else logical_claims / logical_target,
        "admitted_saturation": None if admitted_target == 0 else authenticated_live / admitted_target,
        "underfill_stop_reason": admission["underfill_stop_reason"],
        "occupancy_underfill_reason": admission["occupancy_underfill_reason"],
        "last_progress": runtime_snapshot["last_progress"],
        "cleanup_state": "complete" if cleanup_receipt is not None else runtime_snapshot["cleanup_state"],
    }


def _expected_counts(tasks: dict[str, Task]) -> dict[str, int]:
    counts = Counter(task.state for task in tasks.values())
    return {
        "not_done": counts[" "],
        "self_tested": counts["_"],
        "master_accepted": counts["x"],
        "total": len(tasks),
    }


def validate_projection_metadata(
    metadata: dict[str, Any],
    blueprint_text: str,
    *,
    runtime_snapshot_text: str | None = None,
    runtime_snapshot: dict[str, Any] | None = None,
    cleanup_receipt_text: str | None = None,
    cleanup_receipt: dict[str, Any] | None = None,
) -> None:
    _require_exact_keys(metadata, PROJECTION_METADATA_KEYS, "projection metadata")
    _validate_rfc3339_utc(metadata["generated_at"], "projection generated_at")
    if runtime_snapshot_text is None:
        if metadata["runtime_snapshot_sha256"] is not None or metadata["runtime_snapshot_id"] is not None:
            raise ValidationError("projection names a runtime snapshot that was not supplied for validation")
        runtime_sha = None
        runtime_id = None
    else:
        if runtime_snapshot is None:
            raise ValidationError("parsed runtime snapshot is missing")
        runtime_sha = sha256_text(runtime_snapshot_text)
        runtime_id = runtime_snapshot["snapshot_id"]
        generated_at = datetime.strptime(metadata["generated_at"], "%Y-%m-%dT%H:%M:%SZ")
        observed_at = datetime.strptime(runtime_snapshot["observed_at"], "%Y-%m-%dT%H:%M:%SZ")
        if observed_at > generated_at:
            raise ValidationError("runtime snapshot observed_at is later than projection generated_at")
        has_active_lane = any(
            item["startup"] is not None or item["live"] is True or item["running"] is True
            for item in runtime_snapshot["items_by_id"].values()
        )
        execution_spec = parse_execution_spec(blueprint_text)
        if has_active_lane and generated_at - observed_at > timedelta(
            seconds=execution_spec.cadence_seconds * 2
        ):
            raise ValidationError("active runtime snapshot is stale relative to projection generation")
    if cleanup_receipt_text is None:
        if metadata["cleanup_receipt_sha256"] is not None or metadata["cleanup_receipt_id"] is not None:
            raise ValidationError("projection names a cleanup receipt that was not supplied for validation")
        cleanup_sha = None
        cleanup_id = None
    else:
        if cleanup_receipt is None:
            raise ValidationError("parsed cleanup receipt is missing")
        cleanup_sha = sha256_text(cleanup_receipt_text)
        cleanup_id = cleanup_receipt["receipt_id"]
        generated_at = datetime.strptime(metadata["generated_at"], "%Y-%m-%dT%H:%M:%SZ")
        issued_at = datetime.strptime(cleanup_receipt["issued_at"], "%Y-%m-%dT%H:%M:%SZ")
        if issued_at > generated_at:
            raise ValidationError("cleanup receipt issued_at is later than projection generated_at")
    expected = build_projection_metadata(
        blueprint_text,
        metadata["generated_at"],
        runtime_snapshot_sha256=runtime_sha,
        runtime_snapshot_id=runtime_id,
        cleanup_receipt_sha256=cleanup_sha,
        cleanup_receipt_id=cleanup_id,
    )
    if metadata != expected:
        raise ValidationError("projection metadata is stale or does not bind the exact inputs")


def validate_status(
    status_text: str,
    tasks: dict[str, Task],
    metadata: dict[str, Any],
    runtime_snapshot: dict[str, Any] | None,
    cleanup_receipt: dict[str, Any] | None,
) -> dict[str, Any]:
    status = parse_json_strict(status_text, "Status")
    status = _require_exact_keys(status, STATUS_TOP_LEVEL_KEYS, "Status")
    canonical_status = json.dumps(status, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    if status_text != canonical_status:
        raise ValidationError("Status is not the canonical UTF-8 pretty-JSON projection")
    if status["schema_version"] != STATUS_SCHEMA:
        raise ValidationError("Status schema version differs")
    if status["authority_note"] != "Generated read-only projection; Docs/Stage3_Blueprint.md is the only checklist authority.":
        raise ValidationError("Status authority boundary differs")
    if _canonical_json_bytes(status["metadata"]) != _canonical_json_bytes(metadata):
        raise ValidationError("Status metadata differs from the shared projection snapshot")
    if _canonical_json_bytes(status["counts"]) != _canonical_json_bytes(_expected_counts(tasks)):
        raise ValidationError("Status checklist counts differ")
    if _canonical_json_bytes(status["planning"]) != _canonical_json_bytes(planning_projection(tasks)):
        raise ValidationError("Status planning DAG projection differs")
    if _canonical_json_bytes(status["runtime"]) != _canonical_json_bytes(
        expected_runtime_projection(runtime_snapshot, cleanup_receipt)
    ):
        raise ValidationError("Status runtime projection invents, omits, or merges runtime state")
    if not isinstance(status["items"], list):
        raise ValidationError("Status items must be an array")
    for index, item in enumerate(status["items"]):
        _require_exact_keys(item, STATUS_ITEM_KEYS, f"Status item {index}")
    expected_items = expected_status_items(tasks, runtime_snapshot)
    if _canonical_json_bytes(status["items"]) != _canonical_json_bytes(expected_items):
        raise ValidationError("Status item monitoring projection differs")
    return status


def _decode_monitor_cell(cell: str, label: str) -> Any:
    if len(cell) < 2 or not cell.startswith("`") or not cell.endswith("`"):
        raise ValidationError(f"{label} must be a code-wrapped JSON scalar")
    encoded = cell[1:-1]
    try:
        return json.loads(encoded)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{label} contains malformed JSON") from exc


def _markdown_json_cell(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    encoded = encoded.replace("|", "\\u007c").replace("`", "\\u0060")
    return f"`{encoded}`"


def expected_gantt_mermaid_lines(
    metadata: dict[str, Any], expected_items: list[dict[str, Any]]
) -> list[str]:
    """Independently derive the only allowed Mermaid timing program."""

    lines = [
        "```mermaid",
        "gantt",
        "    title Stage3 recorded projection and task timing",
        "    dateFormat YYYY-MM-DDTHH:mm:ss",
        "    axisFormat %Y-%m-%d %H:%M",
        "    section Projection",
        "    Projection snapshot generated :milestone, projection, "
        + metadata["generated_at"].removesuffix("Z")
        + ", 0s",
    ]
    recorded = [item for item in expected_items if item["timing"]["status"] == "recorded"]
    if recorded:
        lines.append("    section Recorded task timing")
    for item in recorded:
        timing = item["timing"]
        mermaid_id = "timing_" + item["id"].lower().replace("-", "_")
        start = timing["start"].removesuffix("Z")
        if timing["end"] is not None:
            lines.append(
                f"    {item['id']} :{mermaid_id}, {start}, {timing['end'].removesuffix('Z')}"
            )
        elif timing["duration_seconds"] is not None:
            lines.append(
                f"    {item['id']} :{mermaid_id}, {start}, {timing['duration_seconds']}s"
            )
        else:
            lines.append(
                f"    {item['id']} start observed :milestone, {mermaid_id}, {start}, 0s"
            )
    lines.append("```")
    return lines


def _extract_exact_fenced_block(text: str, opener: str, label: str) -> list[str]:
    lines = text.splitlines()
    if lines.count(opener) != 1:
        raise ValidationError(f"{label} must contain exactly one {opener} fence")
    start = lines.index(opener)
    try:
        end = lines.index("```", start + 1)
    except ValueError as exc:
        raise ValidationError(f"{label} fence is unterminated") from exc
    return lines[start : end + 1]


def parse_gantt_monitor(gantt_text: str) -> list[dict[str, Any]]:
    begin, end, lines = _one_region(
        gantt_text, GANTT_MONITOR_BEGIN, GANTT_MONITOR_END, "Gantt monitoring index"
    )
    body = lines[begin + 1 : end]
    if len(body) < 2 or body[0] != MONITOR_HEADER or body[1] != MONITOR_SEPARATOR:
        raise ValidationError("Gantt monitoring index has missing or duplicate fields")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for offset, line in enumerate(body[2:], start=begin + 4):
        if not line:
            continue
        if not line.startswith("| ") or not line.endswith(" |"):
            raise ValidationError(f"Gantt line {offset}: malformed monitoring row")
        cells = line[2:-2].split(" | ")
        if len(cells) != len(MONITOR_COLUMNS):
            raise ValidationError(f"Gantt line {offset}: missing or duplicate monitoring fields")
        values = []
        for cell, column in zip(cells, MONITOR_COLUMNS):
            value = _decode_monitor_cell(cell, f"Gantt line {offset} field {column}")
            if cell != _markdown_json_cell(value):
                raise ValidationError(f"Gantt line {offset} field {column} is not canonically encoded")
            values.append(value)
        row = dict(zip(
            (
                "id", "state", "depends_on", "owned_paths", "claim", "run", "owner", "startup",
                "live", "running", "handoff", "integration", "repair", "planning_blockers",
                "runtime_block", "timing",
            ),
            values,
        ))
        item_id = row["id"]
        if not isinstance(item_id, str) or not ITEM_RE.fullmatch(item_id):
            raise ValidationError(f"Gantt line {offset}: invalid item ID")
        if item_id in seen:
            raise ValidationError(f"Gantt repeats monitoring row {item_id}")
        seen.add(item_id)
        _require_exact_keys(row, STATUS_ITEM_KEYS, f"Gantt row {item_id}")
        result.append(row)
    return result


def validate_gantt(gantt_text: str, metadata: dict[str, Any], expected_items: list[dict[str, Any]]) -> None:
    lines = gantt_text.splitlines()
    if not lines or lines[0] != "# Stage3 Full Claim-List Completion and Isolated Execution Gantt":
        raise ValidationError("Gantt heading differs from Stage3")
    if any(ANY_INDENT_CHECKBOX_RE.match(line) for line in gantt_text.splitlines()):
        raise ValidationError("Gantt contains a competing mutable checkbox")
    expected_headings = [
        "# Stage3 Full Claim-List Completion and Isolated Execution Gantt",
        "## Renderable generation milestone",
        "## Unscheduled task timing",
        "## Complete monitoring index",
    ]
    if [line for line in lines if line.startswith("#")] != expected_headings:
        raise ValidationError("Gantt heading set/order differs from the closed projection grammar")
    for phrase in (
        VERSION,
        "read-only schedule and complete worker Kanban monitoring projection",
        "## Renderable generation milestone",
        "## Unscheduled task timing",
    ):
        if phrase not in gantt_text:
            raise ValidationError(f"Gantt missing monitoring phrase: {phrase}")
    mermaid_block = _extract_exact_fenced_block(gantt_text, "```mermaid", "Gantt")
    expected_mermaid = expected_gantt_mermaid_lines(metadata, expected_items)
    if mermaid_block != expected_mermaid:
        raise ValidationError("Gantt Mermaid rows differ from the exact recorded timing projection")
    if sum(line.strip() == "```mermaid" for line in lines) != 1:
        raise ValidationError("Gantt contains an extra or disguised Mermaid block")
    if parse_surface_metadata(gantt_text, "Gantt") != metadata:
        raise ValidationError("Gantt metadata differs from the shared projection snapshot")
    rows = parse_gantt_monitor(gantt_text)
    if _canonical_json_bytes(rows) != _canonical_json_bytes(expected_items):
        raise ValidationError("Gantt monitoring index is incomplete, duplicated, stale, or field-inexact")
    unscheduled_count = sum(item["timing"]["status"] == "unscheduled" for item in expected_items)
    if unscheduled_count == len(expected_items):
        expected_timing_summary = (
            f"Every task is `unscheduled` in this {len(expected_items)}-item snapshot because neither the Blueprint "
            "nor a runtime ledger records a trustworthy task date or operator-frozen estimate."
        )
    else:
        expected_timing_summary = (
            f"{unscheduled_count} tasks are `unscheduled`; {len(expected_items) - unscheduled_count} tasks carry only "
            "recorded timing from the bound runtime snapshot."
        )
    if gantt_text.count(expected_timing_summary) != 1:
        raise ValidationError("Gantt timing narrative count/state differs from its monitoring rows")
    metadata_begin, metadata_end, _ = _one_region(
        gantt_text, METADATA_BEGIN, METADATA_END, "Gantt metadata"
    )
    mermaid_begin = lines.index("```mermaid")
    mermaid_end = mermaid_begin + len(expected_mermaid) - 1
    monitor_begin, monitor_end, _ = _one_region(
        gantt_text, GANTT_MONITOR_BEGIN, GANTT_MONITOR_END, "Gantt monitoring index"
    )
    expected_prefix = [
        "# Stage3 Full Claim-List Completion and Isolated Execution Gantt",
        "",
        f"> Mandatory same-name read-only schedule and complete worker Kanban monitoring projection for `{VERSION}`.",
        "> `Docs/Stage3_Blueprint.md` is the only mutable checklist authority; regenerate this file instead of editing it.",
        "",
    ]
    if lines[:metadata_begin] != expected_prefix:
        raise ValidationError("Gantt introduction differs from the closed projection grammar")
    if lines[metadata_end + 1 : mermaid_begin] != [
        "",
        "## Renderable generation milestone",
        "",
        "Every renderable row below comes from the projection timestamp or an exact recorded runtime timing object; it is never an inferred task estimate.",
        "",
    ]:
        raise ValidationError("Gantt pre-Mermaid structure differs")
    if lines[mermaid_end + 1 : monitor_begin] != [
        "",
        "## Unscheduled task timing",
        "",
        expected_timing_summary,
        "The complete timing object remains visible in each monitoring row; no calendar interval is inferred from document order, category, dependency depth, or generation time.",
        "",
        "## Complete monitoring index",
        "",
        "Each stable checklist ID has exactly one row. `Planning blockers` are unresolved Blueprint dependencies; `Runtime block` is independent and remains `null` when runtime is unavailable.",
        "",
    ]:
        raise ValidationError("Gantt timing/monitor skeleton contains extra or missing prose")
    if monitor_end != len(lines) - 1:
        raise ValidationError("Gantt contains trailing content after the monitoring commit surface")
    for row in rows:
        timing = _validate_timing(row["timing"], f"Gantt {row['id']}.timing")
        if metadata["runtime_snapshot_sha256"] is None and timing["status"] != "unscheduled":
            raise ValidationError("Gantt invents timing while runtime evidence is unavailable")
    if metadata["runtime_snapshot_sha256"] is None and "Every task is `unscheduled`" not in gantt_text:
        raise ValidationError("Gantt does not visibly classify every no-runtime item as unscheduled")
    if str(ROOT) in gantt_text:
        raise ValidationError("Gantt leaks this machine's absolute repository path")


def _kanban_primary_ids(kanban_text: str) -> list[str]:
    result: list[str] = []
    for line in kanban_text.splitlines():
        match = re.match(rf"^- `(?P<item>{ITEM_PATTERN})`(?:\s|$)", line)
        if match:
            result.append(match.group("item"))
    return result


def _kanban_section_ids(kanban_text: str, heading: str) -> list[str]:
    lines = kanban_text.splitlines()
    marker = f"## {heading}"
    if lines.count(marker) != 1:
        raise ValidationError(f"Kanban must contain exactly one {heading} column")
    begin = lines.index(marker) + 1
    end = next((index for index in range(begin, len(lines)) if lines[index].startswith("## ")), len(lines))
    ids: list[str] = []
    for line in lines[begin:end]:
        match = re.match(rf"^- `(?P<item>{ITEM_PATTERN})`(?:\s|$)", line)
        if match:
            ids.append(match.group("item"))
    if len(ids) != len(set(ids)):
        raise ValidationError(f"Kanban {heading} column repeats an item")
    return ids


def _kanban_section_content(kanban_text: str, heading: str) -> list[str]:
    lines = kanban_text.splitlines()
    marker = f"## {heading}"
    if lines.count(marker) != 1:
        raise ValidationError(f"Kanban must contain exactly one {heading} column")
    begin = lines.index(marker) + 1
    end = next((index for index in range(begin, len(lines)) if lines[index].startswith("## ")), len(lines))
    return [line for line in lines[begin:end] if line]


def _parse_kanban_runtime_table(kanban_text: str) -> dict[str, Any]:
    lines = kanban_text.splitlines()
    header = "| Runtime field | Value |"
    if lines.count(header) != 1:
        raise ValidationError("Kanban must contain exactly one runtime table")
    index = lines.index(header)
    if index + 1 >= len(lines) or lines[index + 1] != "|---|---:|":
        raise ValidationError("Kanban runtime table separator differs")
    result: dict[str, Any] = {}
    for line in lines[index + 2 :]:
        if not line.startswith("| "):
            break
        match = re.fullmatch(r"\| `(?P<key>[a-z_]+)` \| (?P<value>`.*`) \|", line)
        if match is None:
            raise ValidationError("Kanban runtime table contains a malformed row")
        key = match.group("key")
        if key in result:
            raise ValidationError(f"Kanban runtime table repeats {key}")
        raw_value = match.group("value")
        value = _decode_monitor_cell(raw_value, f"Kanban runtime {key}")
        if raw_value != _markdown_json_cell(value):
            raise ValidationError(f"Kanban runtime {key} is not canonically encoded")
        result[key] = value
    expected_keys = set(KANBAN_RUNTIME_FIELDS) | {"cleanup_state"}
    if set(result) != expected_keys:
        raise ValidationError(
            "Kanban runtime fields differ: "
            f"missing={sorted(expected_keys - set(result))}, extra={sorted(set(result) - expected_keys)}"
        )
    return result


def validate_kanban(
    kanban_text: str,
    tasks: dict[str, Task],
    metadata: dict[str, Any],
    runtime_snapshot: dict[str, Any] | None,
    cleanup_receipt: dict[str, Any] | None,
) -> None:
    lines = kanban_text.splitlines()
    if not lines or lines[0] != "# Stage3 Worker Kanban":
        raise ValidationError("Kanban heading differs")
    if any(ANY_INDENT_CHECKBOX_RE.match(line) for line in kanban_text.splitlines()):
        raise ValidationError("Kanban contains a competing mutable checkbox")
    expected_headings = [
        "# Stage3 Worker Kanban",
        "## Runtime snapshot",
        "## Implementation-ready",
        "## Validation-preparation",
        "## Starting",
        "## Live",
        "## Handoff",
        "## Integration",
        "## Repair",
        "## Planning-blocked",
        "## Runtime-blocked",
        "## Accepted",
        "## Lifecycle vocabulary",
    ]
    if [line for line in lines if line.startswith("#")] != expected_headings:
        raise ValidationError("Kanban heading set/order differs from the closed projection grammar")
    for phrase in (
        VERSION,
        "not a second checklist or completion authority",
        "Planning blockers are derived from the Blueprint DAG",
        "## Implementation-ready",
        "## Validation-preparation",
        "## Starting",
        "## Live",
        "## Handoff",
        "## Integration",
        "## Repair",
        "## Planning-blocked",
        "## Runtime-blocked",
        "## Accepted",
    ):
        if phrase not in kanban_text:
            raise ValidationError(f"Kanban missing required monitor field: {phrase}")
    if metadata["runtime_snapshot_sha256"] is None:
        phrase = "`runtime_unavailable`; every worker runtime count and lifecycle value is `null`, never an invented zero."
        if phrase not in kanban_text:
            raise ValidationError("Kanban merges unavailable runtime with an observed zero")
    if parse_surface_metadata(kanban_text, "Kanban") != metadata:
        raise ValidationError("Kanban metadata differs from the shared projection snapshot")
    primary_ids = _kanban_primary_ids(kanban_text)
    if set(primary_ids) != set(tasks):
        raise ValidationError("Kanban item coverage differs from the authority")
    if any(item_id not in tasks for item_id in ITEM_REF_RE.findall(kanban_text)):
        raise ValidationError("Kanban references an unknown item")
    runtime = expected_runtime_projection(runtime_snapshot, cleanup_receipt)
    if runtime_snapshot is None:
        expected_runtime_narrative = (
            "`runtime_unavailable`; every worker runtime count and lifecycle value is `null`, never an invented zero. "
            f"Terminal `cleanup_state` is `{runtime['cleanup_state']}` from the optional durable cleanup receipt."
        )
    else:
        expected_runtime_narrative = (
            f"Observed runtime snapshot {_markdown_json_cell(runtime['snapshot_id'])} "
            f"at {_markdown_json_cell(runtime['observed_at'])}."
        )
    if kanban_text.count(expected_runtime_narrative) != 1:
        raise ValidationError("Kanban runtime/cleanup narrative differs from the reconciled snapshot")
    runtime_table = _parse_kanban_runtime_table(kanban_text)
    expected_runtime_table = {key: runtime[key] for key in KANBAN_RUNTIME_FIELDS}
    expected_runtime_table["cleanup_state"] = runtime["cleanup_state"]
    if _canonical_json_bytes(runtime_table) != _canonical_json_bytes(expected_runtime_table):
        raise ValidationError("Kanban runtime table differs from the reconciled Status snapshot")
    metadata_begin, metadata_end, _ = _one_region(
        kanban_text, METADATA_BEGIN, METADATA_END, "Kanban metadata"
    )
    expected_prefix = [
        "# Stage3 Worker Kanban",
        "",
        f"> Generated read-only view for `{VERSION}`; this is not a second checklist or completion authority.",
        "> Planning blockers are derived from the Blueprint DAG. Runtime blocks come only from a validated runtime snapshot.",
        "",
    ]
    if lines[:metadata_begin] != expected_prefix:
        raise ValidationError("Kanban introduction differs from the closed projection grammar")
    runtime_heading_index = lines.index("## Runtime snapshot")
    if lines[metadata_end + 1 : runtime_heading_index] != [""]:
        raise ValidationError("Kanban contains extra prose before the runtime column")
    expected_runtime_section = [
        expected_runtime_narrative,
        "| Runtime field | Value |",
        "|---|---:|",
        *[
            f"| `{key}` | {_markdown_json_cell(runtime[key])} |"
            for key in KANBAN_RUNTIME_FIELDS
        ],
        f"| `cleanup_state` | {_markdown_json_cell(runtime['cleanup_state'])} |",
    ]
    if _kanban_section_content(kanban_text, "Runtime snapshot") != expected_runtime_section:
        raise ValidationError("Kanban runtime column contains extra, missing, or reordered content")
    planning = planning_projection(tasks)
    items = expected_status_items(tasks, runtime_snapshot)
    item_by_id = {item["id"]: item for item in items}

    def plain_lines(ids: list[str]) -> list[str]:
        return [f"- `{item_id}`" for item_id in ids] if ids else ["_None._"]

    integration_ids = list(
        dict.fromkeys(
            planning["frontiers"]["integration_ready"]
            + [item["id"] for item in items if item["integration"] is not None]
        )
    )
    integration_lines: list[str] = []
    for item_id in integration_ids:
        labels: list[str] = []
        if item_id in planning["frontiers"]["integration_ready"]:
            labels.append("planning integration-ready")
        if item_by_id[item_id]["integration"] is not None:
            labels.append("runtime " + _markdown_json_cell(item_by_id[item_id]["integration"]))
        integration_lines.append(f"- `{item_id}` — " + "; ".join(labels))
    if not integration_lines:
        integration_lines = ["_None._"]
    planning_blocked_lines = [
        f"- `{entry['id']}` — blockers: "
        + ", ".join(f"`{dependency}`" for dependency in entry["blockers"])
        for entry in planning["dependency_blocked"]
    ] or ["_None._"]
    runtime_blocked_lines = [
        f"- `{item['id']}` — {_markdown_json_cell(item['runtime_block'])}"
        for item in items
        if item["runtime_block"] is not None
    ] or ["_None._"]
    expected_columns = {
        "Implementation-ready": plain_lines(planning["frontiers"]["implementation_ready"]),
        "Validation-preparation": plain_lines(planning["frontiers"]["validation_preparation"]),
        "Starting": plain_lines(
            [item["id"] for item in items if item["startup"] is not None and item["live"] is not True]
        ),
        "Live": plain_lines([item["id"] for item in items if item["live"] is True]),
        "Handoff": plain_lines([item["id"] for item in items if item["handoff"] is not None]),
        "Integration": integration_lines,
        "Repair": plain_lines([item["id"] for item in items if item["repair"] is not None]),
        "Planning-blocked": planning_blocked_lines,
        "Runtime-blocked": runtime_blocked_lines,
        "Accepted": plain_lines(planning["accepted"]),
    }
    for heading, expected_lines in expected_columns.items():
        if _kanban_section_content(kanban_text, heading) != expected_lines:
            raise ValidationError(f"Kanban {heading} column differs from the reconciled snapshot")
    expected_vocabulary = [
        "`reserved -> materialized -> tmux_started -> goal_pasted -> goal_submitted -> live -> handoff_ready -> finished`"
    ]
    if _kanban_section_content(kanban_text, "Lifecycle vocabulary") != expected_vocabulary:
        raise ValidationError("Kanban lifecycle vocabulary/trailing structure differs")


def validate_texts(
    blueprint_text: str,
    gantt_text: str,
    status_text: str,
    kanban_text: str,
    runtime_snapshot_text: str | None = None,
    cleanup_receipt_text: str | None = None,
    pre_cleanup_receipt_text: str | None = None,
    cleanup_verifier_script_bytes: bytes | None = None,
    release_validation_text: str | None = None,
    *,
    require_complete: bool = False,
    enforce_current_runtime: bool = False,
    validation_now: datetime | None = None,
) -> dict[str, int]:
    if runtime_snapshot_text is not None and cleanup_receipt_text is not None:
        raise ValidationError(
            "terminal cleanup receipt requires the canonical controller runtime snapshot to be absent"
        )
    tasks = parse_tasks(blueprint_text)
    validate_graph(tasks)
    validate_ownership(tasks)
    validate_blueprint_contract(blueprint_text, tasks)
    runtime_snapshot = None
    if runtime_snapshot_text is not None:
        runtime_snapshot = parse_runtime_snapshot(
            runtime_snapshot_text,
            tasks,
            blueprint_text,
            pre_cleanup_receipt_text=pre_cleanup_receipt_text,
        )
        if enforce_current_runtime:
            validate_runtime_fresh_now(
                runtime_snapshot, blueprint_text, now=validation_now
            )
    elif any(task.state == "_" for task in tasks.values()):
        raise ValidationError("a self-tested cursor requires a bound runtime handoff snapshot")
    cleanup_receipt = None
    if cleanup_receipt_text is not None:
        cleanup_receipt = parse_cleanup_receipt(
            cleanup_receipt_text,
            blueprint_text,
            tasks,
            pre_cleanup_receipt_text=pre_cleanup_receipt_text,
            verifier_script_bytes=cleanup_verifier_script_bytes,
        )
    if runtime_snapshot is None and cleanup_receipt is None:
        accepted_ids = {item_id for item_id, task in tasks.items() if task.state == "x"}
        if accepted_ids != BOOTSTRAP_ACCEPTED_IDS:
            raise ValidationError(
                "Master-accepted cursor differs without a raw runtime/Master-receipt or terminal cleanup binding"
            )
    gantt_metadata = parse_surface_metadata(gantt_text, "Gantt")
    status_raw = parse_json_strict(status_text, "Status")
    if not isinstance(status_raw, dict) or not isinstance(status_raw.get("metadata"), dict):
        raise ValidationError("Status lacks projection metadata")
    status_metadata = status_raw["metadata"]
    kanban_metadata = parse_surface_metadata(kanban_text, "Kanban")
    if not (gantt_metadata == status_metadata == kanban_metadata):
        raise ValidationError("Gantt, Status, and Kanban metadata do not describe one snapshot")
    validate_projection_metadata(
        gantt_metadata,
        blueprint_text,
        runtime_snapshot_text=runtime_snapshot_text,
        runtime_snapshot=runtime_snapshot,
        cleanup_receipt_text=cleanup_receipt_text,
        cleanup_receipt=cleanup_receipt,
    )
    status = validate_status(status_text, tasks, gantt_metadata, runtime_snapshot, cleanup_receipt)
    validate_gantt(gantt_text, gantt_metadata, status["items"])
    validate_kanban(
        kanban_text, tasks, gantt_metadata, runtime_snapshot, cleanup_receipt
    )
    if require_complete:
        if any(task.state != "x" for task in tasks.values()):
            raise ValidationError("terminal completion profile requires every checklist item Master accepted")
        if cleanup_receipt is None:
            raise ValidationError("terminal completion profile requires the externally verified cleanup receipt")
        if status["runtime"]["cleanup_state"] != "complete":
            raise ValidationError("terminal completion profile lacks the projected complete cleanup state")
        if release_validation_text is None:
            raise ValidationError("terminal completion profile requires the fixed-matrix release receipt")
        parse_release_validation(release_validation_text, blueprint_text, tasks)
    return _expected_counts(tasks)


def resolve_runtime_snapshot_path(explicit: Path | None) -> Path | None:
    """Use an explicit fixture/override, otherwise discover the frozen controller snapshot."""

    if explicit is not None:
        return explicit
    return RUNTIME_SNAPSHOT if RUNTIME_SNAPSHOT.is_file() else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--runtime-snapshot",
        type=Path,
        help=f"optional strict {RUNTIME_SCHEMA} input used to validate runtime-backed projections",
    )
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="enforce all Master receipts, the fixed matrix, current repository Merkle, and cleanup receipt",
    )
    parser.add_argument(
        "--acceptance-receipt",
        type=Path,
        help=f"terminal {RELEASE_VALIDATION_SCHEMA} receipt; defaults to {RELEASE_VALIDATION.relative_to(ROOT)}",
    )
    args = parser.parse_args()
    lock_fd: int | None = None
    try:
        lock_fd = os.open(
            ROOT,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
        except OSError as exc:
            if exc.errno not in {errno.EACCES, errno.EAGAIN}:
                raise
            raise ValidationError("a Stage3 projection writer is active; retry validation") from exc
        runtime_path = resolve_runtime_snapshot_path(args.runtime_snapshot)
        captured_bytes: dict[Path, bytes | None] = {
            BLUEPRINT: BLUEPRINT.read_bytes(),
            GANTT: GANTT.read_bytes(),
            STATUS: STATUS.read_bytes(),
            KANBAN: KANBAN.read_bytes(),
            RUNTIME_SNAPSHOT if runtime_path is None else runtime_path: (
                None if runtime_path is None else runtime_path.read_bytes()
            ),
            CLEANUP_RECEIPT: CLEANUP_RECEIPT.read_bytes() if CLEANUP_RECEIPT.exists() else None,
            PRE_CLEANUP_RECEIPT: (
                PRE_CLEANUP_RECEIPT.read_bytes() if PRE_CLEANUP_RECEIPT.exists() else None
            ),
        }
        release_path = args.acceptance_receipt or RELEASE_VALIDATION
        if args.require_complete:
            captured_bytes[release_path] = release_path.read_bytes()
        cleanup_receipt_bytes = captured_bytes[CLEANUP_RECEIPT]
        pre_cleanup_bytes = captured_bytes[PRE_CLEANUP_RECEIPT]
        verifier_bytes = None
        if cleanup_receipt_bytes is not None:
            if pre_cleanup_bytes is None:
                raise ValidationError("cleanup receipt exists without the canonical pre-cleanup arm")
            verifier_bytes = CLEANUP_VERIFIER_SCRIPT.read_bytes()
            captured_bytes[CLEANUP_VERIFIER_SCRIPT] = verifier_bytes
        blueprint_text = captured_bytes[BLUEPRINT].decode("utf-8")
        runtime_snapshot_bytes = captured_bytes[RUNTIME_SNAPSHOT if runtime_path is None else runtime_path]
        runtime_snapshot_text = (
            None if runtime_snapshot_bytes is None else runtime_snapshot_bytes.decode("utf-8")
        )
        cleanup_receipt_text = (
            None if cleanup_receipt_bytes is None else cleanup_receipt_bytes.decode("utf-8")
        )
        summary = validate_texts(
            blueprint_text,
            captured_bytes[GANTT].decode("utf-8"),
            captured_bytes[STATUS].decode("utf-8"),
            captured_bytes[KANBAN].decode("utf-8"),
            runtime_snapshot_text,
            cleanup_receipt_text,
            None if pre_cleanup_bytes is None else pre_cleanup_bytes.decode("utf-8"),
            verifier_bytes,
            None if not args.require_complete else captured_bytes[release_path].decode("utf-8"),
            require_complete=args.require_complete,
            enforce_current_runtime=True,
        )
        for path, expected in captured_bytes.items():
            actual = path.read_bytes() if path.exists() else None
            if actual != expected:
                raise ValidationError(f"validation input changed during checker run: {path.relative_to(ROOT)}")
    except (OSError, UnicodeDecodeError, ValidationError) as exc:
        print(f"check_stage3_blueprint: ERROR: {exc}", file=sys.stderr)
        return 1
    finally:
        if lock_fd is not None:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            finally:
                os.close(lock_fd)
    print(
        "check_stage3_blueprint: ok "
        f"({summary['total']} items; [ ]={summary['not_done']}, "
        f"[_]={summary['self_tested']}, [x]={summary['master_accepted']}; "
        "DAG/ownership and v3 clause manifest exact; shared snapshot fresh; Gantt all-ID monitor; runtime unavailable is null)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
