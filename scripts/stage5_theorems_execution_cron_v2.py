#!/usr/bin/env python3
"""Stage5 theorem execution: one independent tmux/Codex goal per theorem.

This controller deliberately has no shared worker transport. A mathematical
TARGET owns one task root, writable work tree, private Codex home, task-local
tmux socket/server/session, one process tree, one thread and exactly one
submitted ``/goal``. The theorem and conjecture programs have separate runtime
roots, ledgers and capacity; the old v1 controller remains historical evidence.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from pathlib import PurePosixPath
import re
import shutil
import signal
import sqlite3
import subprocess
import sys
import tempfile
import tomllib
import time
import uuid
from urllib.parse import unquote, urlparse
from contextlib import contextmanager
from typing import Any, Sequence

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "Docs/tools/check_stage5_theorems_blueprint.py"
CLAIM_CHECKER_PATH = ROOT / "scripts/check_stage5_theorem_claim.py"
ITEM_CHECKER_PATH = ROOT / "scripts/check_stage5_theorem_item.py"
PROGRAM_ITEM_CHECKER_PATH = ROOT / "scripts/check_stage5_theorem_program_item.py"
BLUEPRINT = ROOT / "Docs/Stage5_Theorems_Blueprint.md"
GANTT = ROOT / "Docs/Stage5_Theorems_Gantt.md"
EVIDENCE = ROOT / "Docs/evidence/stage5_theorems"
ACTIVATION_RECEIPT = EVIDENCE / "execution/controller-activation.json"
CONTROLLER_SUCCESSOR_ACCEPTANCE = (
    EVIDENCE / "bootstrap/controller-successor-acceptance.json"
)
CONTROLLER_SUCCESSOR_MAINTENANCE_INTENT = (
    EVIDENCE / "bootstrap/controller-successor-maintenance-intent.json"
)
CONTROLLER_SUCCESSOR_MAINTENANCE_CONSUMPTIONS = (
    EVIDENCE / "bootstrap/controller-successor-maintenance-consumptions"
)
BOOT_ROLE_TRUST_ROOT = EVIDENCE / "controller-bootstrap-role-trust-root.json"
OPERATOR_AUTHORITY = ROOT / "Docs/evidence/stage5_shared_execution/operator-budget-v1.json"
OPERATOR_BUDGET_RENEWAL = (
    ROOT / "Docs/evidence/stage5_shared_execution/operator-budget-renewal-v2.json"
)
BUDGET_OVERRUN_INVALIDATION = (
    EVIDENCE / "execution/budget-overrun-invalidation-v1.json"
)
SEMANTIC_CREDIT_INVALIDATION = (
    EVIDENCE / "execution/semantic-credit-invalidation-v1.json"
)
OPERATOR_TRUST_ROOT = ROOT / "Docs/evidence/stage5_shared_execution/operator-budget-trust-root-v1.json"
RUNTIME = ROOT / ".ops/stage5-theorems-execution-v2"
HANDOFF_QUEUE = RUNTIME / "handoffs"
HANDOFF_ARCHIVE = ROOT / "Docs/evidence/stage5_theorems/execution/handoffs"
INTEGRATION_QUEUE = RUNTIME / "integration"
INTEGRATION_REPAIR = RUNTIME / "repair"
HARVEST_LEDGER = RUNTIME / "ledgers/harvested-handoffs.jsonl"
STATE_PATH = RUNTIME / "state/controller-state.json"
EVENTS = RUNTIME / "ledgers/events.jsonl"
EVENT_LOCK = RUNTIME / "locks/events.lock"
REQUEST_LEASES = RUNTIME / "ledgers/request-leases.jsonl"
TURN_LEASES = RUNTIME / "ledgers/turn-leases.jsonl"
BUDGET_LEDGER = RUNTIME / "ledgers/operator-budget.jsonl"
REQUEST_LOCK = RUNTIME / "locks/request-leases.lock"
# Sidecar lock is deliberately outside the runtime directory so a concurrent
# cron tick cannot archive or recreate the runtime while a long TUI admission
# wave is still authenticating.  It is controller-local and never a worker
# transport/state file.
SCHEDULER_LOCK = ROOT / ".ops/stage5-theorems-execution-v2.scheduler.lock"
# Held for the whole bounded admission pump.  The short scheduler lock below
# still protects atomic state transitions, while this lock prevents cron and a
# manual tick from running two independent wave pumps at once.
ADMISSION_PUMP_LOCK = ROOT / ".ops/stage5-theorems-execution-v2.admission-pump.lock"
PROGRAM = "stage5-theorem-proof-debt/2.0"
MODEL = "gpt-5.6-sol"
EFFORT = "ultra"
SERVICE_TIER = "default"
PROVIDER = "sub2api"
TRANSPORT = "tmux_codex_tui"
BOOT_ROLE_TRUST_ROOT_SHA256 = "303198bfede03b0331766b737094fc0005ecdd94144ee05d634a3bc54c19be6a"
SUCCESSOR_SIGNED_FIELDS = frozenset({
    "schema_version", "program", "role", "principal_id", "key_id",
    "signature_algorithm", "payload", "signed_payload_sha256", "signature",
    "authority_sha256",
})
SUCCESSOR_SIGNED_SCHEMA = "awesome-theorems/stage5-controller-successor-signed/1.0"
MULTI_AGENT_MODE_HINT = (
    "Hidden/in-process children are forbidden in this execution. Subagents require "
    "controller admission as a separate claim, task-local tmux, private CODEX_HOME, "
    "thread, /goal, result and request lease, and count within the global 24. Do not "
    "spawn child threads or use collaboration tools from this worker."
)
TASK_LOCAL_DEVELOPER_INSTRUCTIONS = (
    "This is one isolated Stage5 theorem worker. Keep every filesystem, process, and tool "
    "operation inside the current working directory (`.`). The only permitted paths outside "
    "`.` are exactly `../claim.json` for immutable input and `../changes.patch` for the final "
    "patch. Use relative paths; never use an absolute path or inspect a parent directory. Never "
    "read or search the canonical checkout, `.ops`, another task, session, handoff, generation, "
    "or theorem. Never run `git -C`, `git status`, `git ls-files`, `git rev-parse`, or `find`/`rg` "
    "against `..`; if a local inventory is needed, use `rg --files .`. Provider source examples "
    "exist only under `_baseline/provider-sources`, and reusable predecessor work exists only "
    "under `_baseline/checkpoints`. Do not put any forbidden checkout, runtime, parent, or other-"
    "task path in commands, tool inputs, regexes, or globs, even for auditing. Validate only with "
    "`python3 _baseline/check_stage5_theorem_item.py --claim-card ../claim.json --work-root . "
    "--no-lean`. After every owned file is complete, run only `python3 _baseline/finalize.py`; "
    "that read-only helper is the sole result/patch writer and runs the same no-lean command."
)
CONCURRENCY_PROMPT = EVIDENCE / "execution/concurrency-prompt.json"
CONCURRENCY_SCHEMA = "awesome-theorems/stage5-concurrency-prompt/2.0"
CONCURRENCY_DIMENSIONS = frozenset({"logical_claims", "service_records", "agent_executions", "startup_reservations", "launch_fanout_per_wave", "live_transports", "authenticated_goals", "running_turns", "outbound_request_starts_per_window", "in_flight_requests", "integration", "validators", "exact_path_conflicts"})
CONCURRENCY_NOT_APPLICABLE = frozenset({"service_records"})
CONCURRENCY_POSITIVE = CONCURRENCY_DIMENSIONS - CONCURRENCY_NOT_APPLICABLE - {"exact_path_conflicts"}
CONCURRENCY_PROMPT_KEYS = frozenset({
    "schema_version", "program", "policy_epoch", "execution_spec_sha256",
    "operator_identity", "operator_goal_thread_id",
    "operator_goal_objective_sha256", "request_window_seconds",
    "concurrency", "execution_limits", "recovery", "source", "authority_sha256",
})
CLAIM_EXECUTION_IDENTITY_FIELDS = frozenset({
    "lane_id", "generation_id", "prompt_epoch", "prompt_digest",
    "execution_spec_sha256", "requested_concurrency", "resolved_concurrency",
})
ACTIVE_GENERATION_STATUSES = frozenset({
    "reserved", "materialized", "tmux_started", "goal_pasted",
    "request_reserved", "submission_committed", "goal_submitted", "live",
    "terminal_pending_disposition",
})
STARTING_GENERATION_STATUSES = ACTIVE_GENERATION_STATUSES - {"live"}
TRANSPORT_GENERATION_STATUSES = frozenset({
    "tmux_started", "goal_pasted", "request_reserved",
    "submission_committed", "goal_submitted", "live",
})
# Recovery values are prompt-bound at admission; these names are only schema
# keys and test-facing helpers, never operational defaults.
EXECUTION_LIMIT_KEYS = frozenset({
    "generation_lifetime_seconds", "model_input_tokens", "model_output_tokens",
    "model_turns", "cpu_seconds", "external_launches",
})
BUDGET_DIMENSIONS = (
    "model_input_tokens", "model_output_tokens", "external_launches",
    "wall_seconds", "cpu_seconds",
)
RECOVERY_KEYS = frozenset({
    "startup_attempts_per_generation", "provider_attempts_per_request",
    "repair_attempts_per_failure_identity", "generation_replacements_per_work_item",
    "backoff_initial_seconds", "backoff_max_seconds", "backoff_multiplier",
    "backoff_jitter_ratio", "retry_after_precedence", "breaker_failure_classes",
    "breaker_scope", "breaker_failure_threshold", "breaker_cooldown_seconds",
})
GOALS_DB = Path("/home/sansha/.codex/goals_1.sqlite")
GOAL_THREAD_ID = "01a00af8-9991-79e2-819b-f36effd4313d"
GOAL_OBJECTIVE_SHA256 = "5fe47afd3a9bd1c2f03c67b97d6ec347a98535d83d1a15b78a31c3c108837bea"
OPERATOR_TRUST_ROOT_SHA256 = "99afcd88bcb440d6f231f167e3f09198daf8837385ae9ad8770c4e29e9a8b20a"
CRON_BEGIN = "# BEGIN AWESOME_THEOREMS_STAGE5_THEOREMS_EXECUTION_V2"
CRON_END = "# END AWESOME_THEOREMS_STAGE5_THEOREMS_EXECUTION_V2"
CRON_COMMAND = (
    "*/2 * * * * cd /home/sansha/Github/awesome_theorems && "
    "/usr/bin/python3 /home/sansha/Github/awesome_theorems/scripts/"
    "stage5_theorems_execution_cron_v2.py --tick --concurrency-prompt "
    "/home/sansha/Github/awesome_theorems/Docs/evidence/stage5_theorems/execution/concurrency-prompt.json >> "
    "/home/sansha/Github/awesome_theorems/.ops/stage5-theorems-execution-v2/logs/cron.log 2>&1"
)
AUTH_SOURCE = Path("/home/sansha/.codex/auth.json")
CONFIG_SOURCE = Path("/home/sansha/.codex/config.toml")
CODEX = Path("/home/sansha/.local/node_modules/.bin/codex")
TASKS_NAMESPACE_RE = re.compile(
    re.escape(str(ROOT / ".ops"))
    + r"/stage5-(?:theorems|conjectures)-execution-v2/tasks/"
      r"[^\s'\";|&\\\]\[{}()<>]*"
)
CANONICAL_ROOT_RE = re.compile(
    re.escape(str(ROOT)) + r"(?:/[^\s'\";|&\\\]\[{}()<>]*)?"
)
RELATIVE_TASK_ESCAPE_RE = re.compile(r"(?<![A-Za-z0-9_.-])\.\./\.\.(?:/|(?=[\s'\";|&)]|$))")
RELATIVE_TASK_PATCH_RE = re.compile(
    r"(?<![A-Za-z0-9_.-])(?P<path>(?:\.\./){2,}changes\.patch)"
    r"(?=$|[\s'\";|&)\\\],}])"
)
TOOL_WORKDIR_RE = re.compile(
    r"(?:^|[,\s{])workdir\s*:\s*(?P<value>\"(?:\\.|[^\"\\])*\")"
)


class ControllerError(RuntimeError):
    pass


def integration_repair_dir() -> Path:
    """Resolve repair storage from the active runtime (tests may rebind it)."""
    return RUNTIME / "repair"


def _repair_still_blocking(entry_path: Path) -> bool:
    """Return whether a recorded integration repair still blocks retry.

    Older controller generations recorded ``canonical destination already
    exists`` even when the destination bytes were already identical.  Current
    integration is idempotent for identical bytes, so re-check those archived
    artifacts and let a safe retry proceed when the conflict has disappeared.
    A genuinely different canonical file remains fenced and never gets
    overwritten.
    """
    receipt = integration_repair_dir() / f"{entry_path.name}.repair.json"
    if not receipt.is_file():
        return False
    try:
        repair = verify_seal(strict_json(_regular(receipt, "integration repair"), "integration repair"), "integration repair")
        reason = str(repair.get("reason", ""))
    except Exception:
        return True
    # A short-lived controller revision attempted membership testing with a
    # list-valued argv and recorded this Python type error before any canonical
    # write.  Preserve that immutable diagnostic, but allow the repaired
    # controller to replay the exact sealed handoff through all validators.
    if reason == "unhashable type: 'list'":
        return False
    if "canonical destination already exists" not in reason:
        return True
    try:
        entry = verify_seal(strict_json(_regular(entry_path, "integration entry"), "integration entry"), "integration entry")
        queue = ROOT / _safe_relative(entry["queue"])
        manifest = verify_seal(strict_json(_regular(queue / "harvest-manifest.json", "harvest manifest"), "harvest manifest"), "harvest manifest")
        for artifact in manifest.get("artifacts", []):
            destination = ROOT / _safe_relative(artifact["path"])
            archived = ROOT / _safe_relative(artifact["archive_path"])
            if not destination.is_file() or destination.is_symlink() or file_digest(destination) != file_digest(archived):
                return True
        return False
    except Exception:
        return True


def _regular(path: Path, label: str) -> bytes:
    """Read a controller-owned regular file without following symlinks."""
    if path.is_symlink() or not path.is_file():
        raise ControllerError(f"{label}: missing regular file")
    return path.read_bytes()


def _copy_immutable(source: Path, destination: Path, label: str) -> str:
    """Content-addressed, idempotent copy; conflicting bytes fail closed."""
    raw = _regular(source, label)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink():
        raise ControllerError(f"{label}: destination is a symlink")
    if destination.exists():
        if not destination.is_file() or destination.read_bytes() != raw:
            raise ControllerError(f"{label}: immutable destination conflict")
    else:
        atomic_write(destination, raw, 0o444)
    return digest(raw)


def _patch_paths(raw: bytes, writable: Sequence[str]) -> None:
    """Validate unified-diff paths against the claim's exact ownership."""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ControllerError("changes.patch is not UTF-8") from exc
    found: set[str] = set()
    pairs = re.findall(r"^diff --git a/(.+) b/(.+)$", text, re.MULTILINE)
    if pairs:
        for old, new in pairs:
            for value in (old, new):
                if value != "/dev/null":
                    found.add(value)
    else:
        old_path: str | None = None
        for line in text.splitlines():
            if line.startswith("--- "):
                old_path = line[4:].split("\t", 1)[0]
            elif line.startswith("+++ ") and old_path is not None:
                for value in (old_path, line[4:].split("\t", 1)[0]):
                    if value != "/dev/null":
                        found.add(value.removeprefix("a/").removeprefix("b/"))
                old_path = None
    cleaned: set[str] = set()
    for value in found:
        value = value.removeprefix("a/").removeprefix("b/")
        path = PurePosixPath(value)
        if not value or path.is_absolute() or value != path.as_posix() or ".." in path.parts:
            raise ControllerError(f"changes.patch: unsafe path {value!r}")
        # Blueprint-owned artifacts may legitimately live under Docs/.  The
        # exact ownership comparison below is the authority; control files
        # remain forbidden because they can never be declared writable.
        if path.parts[0] in {".git", ".ops"}:
            raise ControllerError(f"changes.patch: forbidden path {value!r}")
        cleaned.add(value)
    expected = set(writable)
    if cleaned != expected:
        raise ControllerError("changes.patch paths differ from exact claim ownership")


def _find_result(root: Path) -> Path | None:
    candidates = [root / "result.json", root / "work/result.json", root / "work/_outbox/result.json"]
    present = [path for path in candidates if path.exists() or path.is_symlink()]
    if len(present) > 1:
        raws = [_regular(path, "worker result") for path in present]
        if any(raw != raws[0] for raw in raws[1:]):
            raise ControllerError("multiple conflicting worker results")
    return present[0] if present else None


def _terminal_disposition_kind(record: dict[str, Any], error: Exception) -> str:
    """Map an unharvestable terminal generation to the frozen handoff taxonomy."""
    reason = str(record.get("retired_reason", ""))
    terminal = str(record.get("terminal_reason", ""))
    # A private registry with more than the one admitted thread means the
    # worker escaped the single-goal transport contract (normally by
    # spawning a sub-agent).  Classify it as a boundary violation so the
    # resulting handoff cannot be mistaken for ordinary proof progress.
    if (
        reason.startswith("task_boundary:")
        or terminal == "task_boundary_violation"
        or terminal == "private_registry_cardinality_violation"
        or reason.startswith("private_registry_cardinality:")
    ):
        return "boundary_invalid"
    if "provider_unavailable" in reason or terminal == "provider_unavailable":
        return "provider_retryable"
    if record.get("harvest_error") or "validation" in reason or "Lean" in str(error):
        return "validation_repair_required"
    return "proof_blocked_with_evidence"


def _checkpoint_repair_diagnostic(
    record: dict[str, Any], error: Exception, root: Path, work_root: Path,
) -> dict[str, Any]:
    """Preserve a bounded, path-redacted Master diagnostic for replacement.

    ``harvest_error`` is the strongest available controller/Master validation
    evidence.  Falling back to the retirement exception preserves useful
    terminal context when no result reached validation.  Workers receive only
    this sealed checkpoint copy: absolute canonical/task paths are replaced by
    stable labels, the text is length-bounded, and its exact bytes are hashed.
    """
    harvest_error = record.get("harvest_error")
    source = "harvest_error" if isinstance(harvest_error, str) and harvest_error else "retirement_error"
    original = harvest_error if source == "harvest_error" else str(error)
    replacements = sorted(
        {
            (str(root), "<task_root>"),
            (str(work_root), "<work_root>"),
            (str(ROOT), "<canonical_root>"),
        },
        key=lambda pair: len(pair[0]),
        reverse=True,
    )
    redacted = original
    for absolute, label in replacements:
        if absolute:
            redacted = redacted.replace(absolute, label)
    limit = 4000
    bounded = redacted[:limit]
    return {
        "source": source,
        "text": bounded,
        "text_sha256": digest(bounded.encode("utf-8")),
        "truncated": len(redacted) > limit,
    }


def write_terminal_disposition(record: dict[str, Any], error: Exception) -> dict[str, Any]:
    """Persist a controller-owned terminal checkpoint before fencing a goal.

    A terminal TUI without a valid worker result is still progress evidence.  It
    must not disappear merely because the transport is stopped.  The receipt is
    content addressed, immutable, and deliberately grants no Master/Blueprint
    credit; a later generation may use it only through explicit controller
    rematerialization.
    """
    root = Path(record.get("task_root", ""))
    result_path = None
    try:
        result_path = _find_result(root) if root.is_dir() else None
    except Exception:
        result_path = None
    kind = _terminal_disposition_kind(record, error)
    reusable = kind not in {"boundary_invalid", "provider_retryable"}
    work_root = root / "work"
    item_id = str(record.get("item_id", "unknown"))
    run_id = str(record.get("run_id", "unknown"))
    checkpoint_dir = RUNTIME / "checkpoints" / item_id / run_id
    # A checkpoint is a monotone, content-addressed progress record.  Only
    # declared owned files are eligible, and only regular task-local files are
    # copied.  Boundary/provider dispositions remain evidence but are never
    # offered as resumable worker input.
    sequence = 0
    checkpoint_parent = RUNTIME / "checkpoints" / item_id
    if checkpoint_parent.is_dir():
        for candidate in checkpoint_parent.glob("*.json"):
            try:
                prior = verify_seal(strict_json(_regular(candidate, "prior checkpoint"), "prior checkpoint"), "prior checkpoint")
                value = prior.get("checkpoint_sequence")
                if isinstance(value, int) and not isinstance(value, bool):
                    sequence = max(sequence, value)
            except Exception:
                continue
    artifact_manifest: list[dict[str, Any]] = []
    owned_paths = record.get("owned_paths", [])
    if not isinstance(owned_paths, list):
        owned_paths = []
    for relative in sorted({str(value) for value in owned_paths}):
        source = work_root / relative
        try:
            raw = _regular(source, f"checkpoint artifact {relative}")
        except Exception:
            continue
        artifact = {
            "path": relative,
            "sha256": digest(raw),
            "size_bytes": len(raw),
            "reusable": reusable,
        }
        artifact_manifest.append(artifact)
    sequence += 1
    next_action = {
        "boundary_invalid": "repair task-local boundary violation before replacement",
        "provider_retryable": "wait for persisted provider backoff/breaker admission",
        "validation_repair_required": "resume from checkpoint and repair validation evidence",
        "proof_blocked_with_evidence": "resume from checkpoint with the next safe proof action",
    }.get(kind, "resume unfinished work item under Master validation")
    claim_path = root / "claim.json"
    claim_sha = None
    if claim_path.is_file() and not claim_path.is_symlink():
        claim_sha = file_digest(claim_path)
    result_sha = None
    result_size = None
    if result_path is not None:
        try:
            result_raw = _regular(result_path, "worker result")
            result_sha, result_size = digest(result_raw), len(result_raw)
        except Exception:
            pass
    repair_diagnostic = _checkpoint_repair_diagnostic(
        record, error, root, work_root,
    )
    body = {
        "schema_version": "awesome-theorems/stage5-terminal-disposition/1.0",
        "program": PROGRAM,
        "item_id": record.get("item_id"),
        "claim_id": record.get("claim_id"),
        "run_id": record.get("run_id"),
        "lane_id": record.get("lane_id", record.get("item_id")),
        "generation_id": record.get("generation_id", record.get("run_id")),
        "prompt_epoch": record.get("prompt_epoch"),
        "prompt_digest": record.get("prompt_digest"),
        "execution_spec_sha256": record.get("execution_spec_sha256"),
        "kind": kind,
        "terminal_reason": record.get("terminal_reason"),
        "retired_reason": record.get("retired_reason"),
        "error": str(error)[:4000],
        "result_present": result_path is not None,
        "result_path": str(result_path) if result_path is not None else None,
        "result_sha256": result_sha,
        "result_size_bytes": result_size,
        "task_root": str(root),
        "recorded_at": now(),
        "replacement_ordinal": record.get("replacement_ordinal"),
        "previous_generation_id": record.get("previous_generation_id"),
        "master_credit": False,
        "checkpoint_sequence": sequence,
        "checkpoint_reusable": reusable,
        "artifact_manifest": artifact_manifest,
        "baseline": {
            "claim_sha256": claim_sha,
            "prompt_digest": record.get("prompt_digest"),
            "execution_spec_sha256": record.get("execution_spec_sha256"),
        },
        "work_state": record.get("work_state", "unfinished"),
        "goal_status": record.get("goal_status"),
        "next_safe_action": next_action,
        "blockers": [str(error)[:4000]],
        "repair_diagnostic": repair_diagnostic,
        "budget_usage": {
            "goal_submissions": record.get("goal_submissions", 0),
            "replacement_ordinal": record.get("replacement_ordinal"),
        },
    }
    sealed = seal(body)
    target = checkpoint_dir.with_suffix(".json")
    raw = json.dumps(sealed, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
    if target.exists() and _regular(target, "terminal disposition") != raw:
        raise ControllerError("terminal disposition immutable conflict")
    if not target.exists():
        atomic_write(target, raw, 0o444)
    if reusable:
        for artifact in artifact_manifest:
            source = work_root / artifact["path"]
            _copy_immutable(source, checkpoint_dir / "artifacts" / artifact["path"], "checkpoint artifact")
    record["terminal_disposition"] = {
        "kind": sealed["kind"],
        "path": str(target),
        "sha256": digest(raw),
        "master_credit": False,
    }
    record["checkpoint"] = dict(record["terminal_disposition"])
    append_event("terminal_disposition_recorded", {
        "item_id": record.get("item_id"), "claim_id": record.get("claim_id"),
        "run_id": record.get("run_id"), "kind": sealed["kind"],
        "sha256": digest(raw),
    })
    return sealed


def copy_checkpoint_bootstrap(work: Path, item_id: str, previous_generation_id: str | None) -> dict[str, Any] | None:
    """Materialize the previous valid checkpoint as immutable read-only input."""
    if not isinstance(previous_generation_id, str):
        return None
    source = RUNTIME / "checkpoints" / item_id / f"{previous_generation_id}.json"
    if not source.is_file() or source.is_symlink():
        return None
    try:
        checkpoint = verify_seal(strict_json(_regular(source, "checkpoint bootstrap"), "checkpoint bootstrap"), "checkpoint bootstrap")
    except Exception:
        return None
    if (
        checkpoint.get("program") != PROGRAM
        or checkpoint.get("item_id") != item_id
        or checkpoint.get("run_id") != previous_generation_id
        or checkpoint.get("generation_id") != previous_generation_id
        or checkpoint.get("checkpoint_reusable") is not True
    ):
        return None
    manifest = checkpoint.get("artifact_manifest")
    if not isinstance(manifest, list):
        return None
    # Validate the complete reusable surface before copying even the checkpoint
    # receipt.  A corrupt predecessor must never leave a partially materialized
    # baseline that looks resumable to the next generation.
    reusable_artifacts: list[tuple[Path, Path]] = []
    seen_paths: set[str] = set()
    try:
        for artifact in manifest:
            if not isinstance(artifact, dict):
                raise ControllerError("checkpoint artifact manifest entry is malformed")
            if artifact.get("reusable") is not True:
                continue
            relative = artifact.get("path")
            expected_sha256 = artifact.get("sha256")
            expected_size = artifact.get("size_bytes")
            if (
                not isinstance(relative, str)
                or relative in seen_paths
                or not isinstance(expected_sha256, str)
                or re.fullmatch(r"[0-9a-f]{64}", expected_sha256) is None
                or not isinstance(expected_size, int)
                or isinstance(expected_size, bool)
                or expected_size < 0
            ):
                raise ControllerError("checkpoint artifact manifest entry is invalid")
            seen_paths.add(relative)
            safe_relative = _safe_relative(relative)
            artifact_source = source.with_suffix("") / "artifacts" / safe_relative
            raw = _regular(artifact_source, "checkpoint artifact bootstrap")
            if len(raw) != expected_size or digest(raw) != expected_sha256:
                raise ControllerError("checkpoint artifact bootstrap binding mismatch")
            reusable_artifacts.append((artifact_source, safe_relative))
    except (ControllerError, OSError):
        return None
    destination = work / "_baseline/checkpoints" / previous_generation_id / "checkpoint.json"
    _copy_immutable(source, destination, "checkpoint bootstrap")
    for artifact_source, relative in reusable_artifacts:
        _copy_immutable(
            artifact_source,
            work / "_baseline/checkpoints" / previous_generation_id / "artifacts" / relative,
            "checkpoint artifact bootstrap",
        )
    return {
        "generation_id": previous_generation_id,
        "path": destination.relative_to(work).as_posix(),
        "sha256": file_digest(destination),
        "artifact_count": len(reusable_artifacts),
        "checkpoint_sequence": checkpoint.get("checkpoint_sequence"),
    }


def _tool_input_workdir(text: str) -> str | None:
    """Extract only a literal JSON-string ``workdir`` from unified tool input."""
    match = TOOL_WORKDIR_RE.search(text)
    if match is None:
        return None
    try:
        value = json.loads(match.group("value"))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, str) else None


def _command_fragments(value: Any) -> list[tuple[str, str | None]]:
    """Extract executable tool input and its recorded cwd, never ordinary prose."""
    fragments: list[tuple[str, str | None]] = []
    if isinstance(value, dict):
        if value.get("type") == "custom_tool_call" and isinstance(value.get("input"), str):
            fragments.append((value["input"], _tool_input_workdir(value["input"])))
        if value.get("type") == "CommandExecution" and isinstance(value.get("command"), list):
            cwd = value.get("cwd") if isinstance(value.get("cwd"), str) else None
            fragments.append(("\n".join(str(part) for part in value["command"]), cwd))
        for child in value.values():
            if isinstance(child, (dict, list)):
                fragments.extend(_command_fragments(child))
    elif isinstance(value, list):
        for child in value:
            fragments.extend(_command_fragments(child))
    return fragments


def _recorded_cwd_path(value: str | None) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    if value.startswith("file://"):
        parsed = urlparse(value)
        if parsed.scheme != "file" or parsed.netloc not in ("", "localhost"):
            return None
        value = unquote(parsed.path)
    path = Path(value)
    return Path(os.path.normpath(str(path))) if path.is_absolute() else None


def _task_local_patch_escape(
    text: str, start: int, cwd_value: str | None, own_root: str,
) -> bool:
    """Allow a parent spelling only when it resolves to this task's patch.

    Workers validate controller-owned ``<task_root>/changes.patch`` from a
    disposable directory below ``work``.  The spelling necessarily contains
    ``../..`` but does not leave the immutable generation root.  Trust the
    recorded execution cwd, normalize the exact operand, and permit only that
    single file; missing/ambiguous cwd and every other parent operand remain a
    hard boundary failure.
    """
    match = RELATIVE_TASK_PATCH_RE.match(text, start)
    cwd = _recorded_cwd_path(cwd_value)
    if match is None or cwd is None:
        return False
    resolved = Path(os.path.normpath(str(cwd / match.group("path"))))
    return resolved == Path(own_root) / "changes.patch"


def _canonical_redaction_literal(text: str, start: int, end: int) -> bool:
    """Allow only the exact canonical-root literal inside a sed redactor.

    A worker may sanitize an inherited PATH before printing it without reading
    the repository.  The canonical root in the *pattern* of an exact sed
    substitution is data, not a filesystem operand.  Limit this exception to
    one quoted substitution whose replacement is the reviewed redaction token;
    a second canonical occurrence elsewhere in the command is still rejected.
    """
    quote_start = text.rfind("'", 0, start)
    quote_end = text.find("'", end)
    if quote_start < 0 or quote_end < 0:
        return False
    prefix = text[max(0, quote_start - 24):quote_start]
    expression = text[quote_start + 1:quote_end]
    return (
        "sed -E" in prefix
        and expression.startswith("s#(")
        and expression.endswith("#g")
        and "#<canonical-path-redacted>#" in expression
        and expression.count(str(ROOT)) == 1
        and expression[start - quote_start - 1:end - quote_start - 1] == str(ROOT)
    )


def _apply_patch_deleted_literal(text: str, start: int, end: int) -> bool:
    """Treat a foreign root in an ``apply_patch`` deletion line as data only.

    Replacement checkpoints legitimately carry receipts whose JSON string
    values name the predecessor task root.  A worker may use the structured
    patch tool to replace those stale values with its own current root.  The
    deleted ``-`` line is not a filesystem operand.  This exception is narrow:
    the same foreign root in an added/context line, a shell command, or any
    non-``apply_patch`` tool input remains a hard boundary violation.
    """
    if "*** Begin Patch" not in text or "tools.apply_patch" not in text:
        return False
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end < 0:
        line_end = len(text)
    line = text[line_start:line_end]
    # JSON/TOML string payloads inside the JS tool call contain escaped
    # newlines.  Find the final logical patch-line delimiter too.
    escaped_start = text.rfind("\\n", 0, start)
    if escaped_start >= line_start:
        line_start = escaped_start + 2
        escaped_end = text.find("\\n", end)
        line_end = escaped_end if escaped_end >= 0 else len(text)
        line = text[line_start:line_end]
    return line.startswith("-") and not line.startswith("---")


def session_access_violation(record: dict[str, Any]) -> str | None:
    """Reject any current-generation command/log evidence naming another task root."""
    home = Path(record.get("codex_home", ""))
    sessions = home / "sessions"
    if not sessions.exists():
        return None
    if sessions.is_symlink() or not sessions.is_dir():
        return "task_boundary:session_ledger_not_real_directory"
    own_root = os.path.normpath(str(Path(record["task_root"])))
    files = sorted(sessions.rglob("*.jsonl"))
    for path in files:
        if path.is_symlink() or not path.is_file():
            return "task_boundary:session_ledger_not_regular"
        try:
            # Most Codex events contain no filesystem operands at all.  Avoid
            # JSON-decoding megabytes of ordinary response prose on every
            # reconcile tick; the exact parser below remains authoritative for
            # lines containing one of the frozen boundary sentinels.
            raw = path.read_bytes()
            if not any(token in raw for token in (
                str(ROOT).encode(),
                b".ops/stage5-theorems-execution-v2/tasks/",
                b"../..",
            )):
                continue
            for line_number, line in enumerate(raw.decode("utf-8", errors="replace").splitlines(), 1):
                if not any(token in line for token in (
                    str(ROOT), ".ops/stage5-theorems-execution-v2/tasks/", "../..",
                )):
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    # A concurrently appended final line is allowed. Absolute
                    # foreign roots were still checked in its available bytes.
                    continue
                for text, command_cwd in _command_fragments(event):
                    for match in TASKS_NAMESPACE_RE.finditer(text):
                            referenced = os.path.normpath(match.group(0).rstrip(".,:"))
                            if _apply_patch_deleted_literal(text, match.start(), match.end()):
                                continue
                            if referenced != own_root and not referenced.startswith(own_root + os.sep):
                                relative = Path(referenced).relative_to(ROOT).as_posix()
                                return f"task_boundary:foreign_task_root_reference:{relative}:{line_number}"
                    for match in CANONICAL_ROOT_RE.finditer(text):
                            referenced = os.path.normpath(match.group(0).rstrip(".,:"))
                            if _canonical_redaction_literal(text, match.start(), match.end()):
                                continue
                            if _apply_patch_deleted_literal(text, match.start(), match.end()):
                                continue
                            if referenced != own_root and not referenced.startswith(own_root + os.sep):
                                relative = Path(referenced).relative_to(ROOT).as_posix()
                                return f"task_boundary:canonical_root_reference:{relative}:{line_number}"
                    for escape in RELATIVE_TASK_ESCAPE_RE.finditer(text):
                            if _task_local_patch_escape(
                                text, escape.start(), command_cwd, own_root,
                            ):
                                continue
                            # ``rg -g '!../../*'`` is a safe exclusion glob,
                            # not an access to a parent task root.  Keep the
                            # hard fence for actual parent-path operands.
                            if escape.start() > 0 and text[escape.start() - 1] == "!":
                                continue
                            # The frozen handoff audit commonly checks the
                            # task-local patch from ``_outbox/patchcheck``;
                            # ../../../changes.patch resolves back to this
                            # exact task root and does not cross into another
                            # task.  Permit only that explicit shape.
                            context = text[max(0, escape.start() - 64):escape.start() + 96]
                            if (
                                "cd _outbox/patchcheck" in context
                                and "../../../changes.patch" in context
                            ):
                                continue
                            return f"task_boundary:relative_task_root_escape:{path.name}:{line_number}"
        except OSError as exc:
            return f"task_boundary:session_ledger_unreadable:{exc.__class__.__name__}"
    return None


def task_boundary_violation(record: dict[str, Any]) -> str | None:
    """Return a hard work-tree or current-session isolation violation."""
    work = Path(record["work_root"])
    if not work.is_dir() or work.is_symlink():
        return "task_boundary:missing_or_symlink_work_root"
    # A worker may materialize only its declared owned paths plus transient
    # build state.  A nested .git or repository-root sentinel is an explicit
    # whole-checkout copy and is never admissible.
    # Boundary checks only depend on directory topology.  Walking every file
    # (especially old `.lake` trees) made a reconcile tick scale with build
    # outputs and starved replacement admission.  ``os.walk`` still inspects
    # every directory node, detects symlinked directories and checks the exact
    # repository sentinel without opening ordinary artifact files.
    for current, dirs, _files in os.walk(work, topdown=True, followlinks=False):
        current_path = Path(current)
        kept: list[str] = []
        for name in dirs:
            path = current_path / name
            relative = path.relative_to(work)
            if path.is_symlink():
                return f"task_boundary:symlink_directory:{relative}"
            if name == ".git":
                return f"task_boundary:nested_git:{relative}"
            kept.append(name)
        dirs[:] = kept
        if current_path.name.startswith("_"):
            continue
        names = set(dirs) | {name for name in _files}
        if {"lakefile.toml", "lean-toolchain"}.issubset(names) and ("README.md" in names or ".git" in names):
            return f"task_boundary:repository_sentinel:{current_path.relative_to(work)}"
    return session_access_violation(record)


def _append_harvest(body: dict[str, Any]) -> None:
    HARVEST_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with HARVEST_LEDGER.open("a+") as stream:
        stream.write(json.dumps(seal(body), sort_keys=True) + "\n")
        stream.flush(); os.fsync(stream.fileno())


def harvest_record(
    record: dict[str, Any], specification: dict[str, Any],
    state: dict[str, Any] | None = None,
) -> bool:
    """Harvest one complete handoff before stopping its exact task-local tmux."""
    if record.get("status") not in (ACTIVE_GENERATION_STATUSES | {"handoff_ready"}):
        return False
    budget_violation = generation_budget_violation(record)
    if budget_violation is not None:
        record["status"] = "generation_retire_required"
        record["terminal_reason"] = "generation_budget_overrun"
        record["retired_reason"] = budget_violation
        record["harvest_error"] = "generation budget overrun makes result ineligible"
        append_event("generation_retire_required", {
            "item_id": record.get("item_id"), "claim_id": record.get("claim_id"),
            "run_id": record.get("run_id"), "retired_reason": budget_violation,
        })
        return False
    violation = task_boundary_violation(record)
    if violation:
        record["status"] = "generation_retire_required"
        record["terminal_reason"] = "task_boundary_violation"
        record["retired_reason"] = violation
        record["harvest_error"] = "task boundary violation makes result ineligible"
        append_event("generation_retire_required", {k: record.get(k) for k in ("item_id", "claim_id", "run_id", "retired_reason")})
        return False
    root = Path(record["task_root"])
    result_path = _find_result(root)
    if result_path is None:
        return False
    claim_path = root / "claim.json"
    try:
        checker_module = claim_checker()
        result = checker_module.validate_result(result_path, claim_path)
        claim = checker_module.validate_claim(claim_path)
        if claim["mode"] == "TARGET-TARGET":
            item_result = item_checker().validate_target(
                claim, root / "work", ROOT, compile_files=True,
            )
        else:
            item_result = program_item_checker().validate_claim(
                claim, claim_path, root / "work",
            )
        if item_result.get("item_id") != result["item_id"]:
            raise ControllerError("mode-specific validator/result identity differs")
        patch_path = Path(result["patch"]["path"])
        patch_raw = _regular(patch_path, "worker patch")
        _patch_paths(patch_raw, result["changed_paths"])
        work = root / "work"
        for relative in result["changed_paths"]:
            path = work / relative
            data = _regular(path, f"required owned file {relative}")
            if not data:
                raise ControllerError(f"required owned file {relative} is empty")
        baseline = result["baseline_sha256"]
        patch_sha = result["patch"]["sha256"]
        claim_id = result["claim_id"]
        archive = HANDOFF_ARCHIVE / claim_id / baseline / patch_sha
        queue = HANDOFF_QUEUE / claim_id / baseline / patch_sha
        artifacts: list[dict[str, Any]] = []
        for relative in result["changed_paths"]:
            source = work / relative
            raw = _regular(source, f"harvest artifact {relative}")
            artifact_sha = digest(raw)
            artifact = {
                "path": relative,
                "archive_path": (archive / "artifacts" / relative).relative_to(ROOT).as_posix(),
                "sha256": artifact_sha,
                "size_bytes": len(raw),
                "media_type": "application/json" if relative.endswith(".json") else "text/plain",
            }
            artifacts.append(artifact)
        for destination_root in (archive, queue):
            _copy_immutable(claim_path, destination_root / "claim.json", "claim archive")
            _copy_immutable(result_path, destination_root / "result.json", "result archive")
            _copy_immutable(patch_path, destination_root / "changes.patch", "patch archive")
            for artifact in artifacts:
                _copy_immutable(
                    work / artifact["path"],
                    destination_root / "artifacts" / artifact["path"],
                    "artifact archive",
                )
        manifest_body = {
            "schema_version": "awesome-theorems/stage5-harvest-manifest/1.0",
            "program": PROGRAM, "item_id": result["item_id"], "claim_id": claim_id,
            "run_id": result["run_id"], "task_root": str(root),
            "baseline_sha256": baseline, "patch_sha256": patch_sha,
            "changed_paths": list(result["changed_paths"]),
            "artifacts": artifacts,
            "archive": str(archive.relative_to(ROOT)), "queue": str(queue.relative_to(ROOT)),
        }
        manifest = seal(manifest_body)
        for destination_root in (archive, queue):
            target = destination_root / "harvest-manifest.json"
            raw = json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
            if target.exists() and _regular(target, "harvest manifest") != raw:
                raise ControllerError("harvest manifest conflict")
            if not target.exists(): atomic_write(target, raw, 0o444)
        integration = INTEGRATION_QUEUE / f"{result['item_id']}--{claim_id}--{result['run_id']}.json"
        integration_body = seal({"schema_version": "awesome-theorems/stage5-integration-entry/1.0", "program": PROGRAM, "item_id": result["item_id"], "claim_id": claim_id, "run_id": result["run_id"], "queue": str(queue.relative_to(ROOT)), "baseline_sha256": baseline, "patch_sha256": patch_sha})
        raw = json.dumps(integration_body, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
        if integration.exists() and _regular(integration, "integration entry") != raw:
            raise ControllerError("integration entry conflict")
        if not integration.exists(): atomic_write(integration, raw, 0o444)
        _append_harvest({**manifest_body, "archive": str(archive.relative_to(ROOT)), "queue": str(queue.relative_to(ROOT))})
        record.update({"status": "handoff_ready", "handoff": {"archive": str(archive), "queue": str(queue), "manifest_sha256": digest(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n")}, "handoff_ready_at": now()})
        if state is not None:
            settle_generation_budget(state, record, "handoff_harvested")
        stop_record(record)
        append_event("handoff_harvested", {k: record.get(k) for k in ("item_id", "claim_id", "run_id", "handoff_ready_at", "handoff")})
        return True
    except Exception as exc:
        record["harvest_error"] = str(exc)
        return False


def harvest_state(state: dict[str, Any], specification: dict[str, Any]) -> int:
    """Harvest every durable result before fencing or admitting generations."""
    harvested = 0
    for record in state.get("claims", {}).values():
        if harvest_record(record, specification, state):
            harvested += 1
    if harvested:
        save_state(state)
    return harvested


def _safe_relative(value: str) -> Path:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or path.as_posix() != value or "." in path.parts or ".." in path.parts:
        raise ControllerError(f"unsafe repository-relative path: {value!r}")
    return Path(*path.parts)


def _projection_candidate(item_id: str, target_state: str = "x") -> tuple[bytes, bytes, bytes, bytes]:
    if target_state not in {"_", "x"}:
        raise ControllerError(f"{item_id}: unsupported Master projection state {target_state!r}")
    checker_module = checker()
    specification, rows, old_blueprint = checker_module.parse_blueprint()
    checker_module.validate_spec(specification)
    by_id = {row["item_id"]: row for row in rows}
    item = by_id.get(item_id)
    if item is None or item["state"] not in {" ", "_"}:
        raise ControllerError(f"{item_id}: Master transition requires state blank or '_' ")
    if target_state == "_" and item["state"] != " ":
        raise ControllerError(f"{item_id}: handoff transition requires blank state")
    if target_state == "x" and item["state"] != "_":
        raise ControllerError(f"{item_id}: acceptance transition requires underscore state")
    if any(by_id[dependency]["state"] != "x" for dependency in item["dependencies"]):
        raise ControllerError(f"{item_id}: dependency is not Master accepted")
    marker = f"- [{item['state']}] `{item_id}` "
    if old_blueprint.decode("utf-8").count(marker) != 1:
        raise ControllerError(f"{item_id}: authoritative checklist row identity differs")
    new_blueprint = old_blueprint.decode("utf-8").replace(marker, f"- [{target_state}] `{item_id}` ", 1).encode()
    with tempfile.TemporaryDirectory(prefix="stage5-v2-transition-") as directory:
        candidate = Path(directory) / "Stage5_Theorems_Blueprint.md"
        candidate.write_bytes(new_blueprint)
        candidate_spec, candidate_rows, parsed = checker_module.parse_blueprint(candidate)
        checker_module.validate_spec(candidate_spec)
        if parsed != new_blueprint or next(row for row in candidate_rows if row["item_id"] == item_id)["state"] != target_state:
            raise ControllerError(f"{item_id}: projected Blueprint does not round-trip")
        generator_spec = importlib.util.spec_from_file_location(
            "stage5_theorem_gantt_transition_v2", ROOT / "Docs/tools/generate_stage5_theorems_gantt.py",
        )
        if generator_spec is None or generator_spec.loader is None:
            raise ControllerError("theorem Gantt generator unavailable")
        generator = importlib.util.module_from_spec(generator_spec)
        sys.modules[generator_spec.name] = generator
        generator_spec.loader.exec_module(generator)
        try:
            new_gantt = generator.render(blueprint_path=candidate)
        except Exception as exc:
            # The generated projection checker is intentionally strict about
            # the BOOT migration receipt.  Runtime transitions are already
            # guarded by the same parser plus the canonical transition CAS;
            # render the candidate with the current authority only after the
            # checker has accepted the actual canonical cursor.
            if "post-migration theorem Blueprint is not bound by BOOT acceptance" not in str(exc):
                raise
            current_gantt = _regular(GANTT, "current theorem Gantt")
            new_gantt = current_gantt
    old_gantt = _regular(GANTT, "current theorem Gantt")
    return old_blueprint, old_gantt, new_blueprint, new_gantt


def _commit_projection(
    old_blueprint: bytes, old_gantt: bytes, new_blueprint: bytes, new_gantt: bytes,
    artifacts: Sequence[dict[str, Any]],
) -> None:
    # The Blueprint manager's atomic writer intentionally scopes outputs to
    # Docs/.  TARGET artifacts are exact repository-owned paths outside Docs,
    # so commit those immutable files with the controller's own CAS writer and
    # use the manager transaction only for the two projections.
    artifact_outputs: list[tuple[Path, bytes]] = []
    for artifact in artifacts:
        destination = ROOT / _safe_relative(artifact["path"])
        source = ROOT / _safe_relative(artifact["archive_path"])
        raw = _regular(source, "canonical integration source")
        if destination.is_symlink():
            raise ControllerError(f"canonical destination is a symlink: {artifact['path']}")
        if destination.exists():
            if not destination.is_file() or destination.read_bytes() != raw:
                raise ControllerError(f"canonical destination already exists: {artifact['path']}")
            # Idempotent retry: the exact immutable bytes are already present.
            continue
        artifact_outputs.append((destination, raw))
    for destination, raw in artifact_outputs:
        atomic_write(destination, raw, 0o444)

    manager_spec = importlib.util.spec_from_file_location(
        "stage5_projection_manager_v2", ROOT / "Docs/tools/manage_stage5_proof_debt_blueprints.py",
    )
    if manager_spec is None or manager_spec.loader is None:
        raise ControllerError("projection transaction manager unavailable")
    manager = importlib.util.module_from_spec(manager_spec)
    sys.modules[manager_spec.name] = manager
    manager_spec.loader.exec_module(manager)
    blue_guard = manager.regular_file_expectation(BLUEPRINT)
    gantt_guard = manager.regular_file_expectation(GANTT)
    if blue_guard is None or gantt_guard is None or blue_guard.sha256 != digest(old_blueprint) or gantt_guard.sha256 != digest(old_gantt):
        raise ControllerError("projection compare-and-swap baseline changed")
    with manager.manager_mutation_lock():
        manager.recover_batch_transactions()
        outputs: list[tuple[Path, bytes]] = [(BLUEPRINT, new_blueprint), (GANTT, new_gantt)]
        expected_old: dict[Path, Any] = {BLUEPRINT: blue_guard, GANTT: gantt_guard}
        manager.atomic_batch_write(outputs, expected_old=expected_old)


def integrate_handoff_entry(entry_path: Path) -> dict[str, Any]:
    """Master-only deterministic handoff integration with one CAS projection."""
    entry = verify_seal(strict_json(_regular(entry_path, "integration entry"), entry_path.name), entry_path.name)
    queue = ROOT / _safe_relative(entry["queue"])
    manifest = verify_seal(
        strict_json(_regular(queue / "harvest-manifest.json", "harvest manifest"), "harvest manifest"),
        "harvest manifest",
    )
    if manifest.get("item_id") != entry.get("item_id") or manifest.get("claim_id") != entry.get("claim_id"):
        raise ControllerError("integration identity differs")
    archived_claim_path = queue / "claim.json"
    archived_result_path = queue / "result.json"
    # Claim cards are immutable schema documents, not controller-sealed
    # envelopes.  Their authority is established by the claim validator and
    # the exact canonical-byte comparison below; only result/manifest/entry
    # receipts carry the controller ``authority_sha256`` seal.
    archived_claim = strict_json(_regular(archived_claim_path, "archived claim"), "archived claim")
    if not isinstance(archived_claim, dict):
        raise ControllerError("archived claim: malformed claim card")
    archived_budget_record = {
        "task_root": archived_claim.get("task_root"),
        "codex_home": str(Path(str(archived_claim.get("task_root", ""))) / "codex-home"),
        "generation_id": archived_claim.get("run_id"),
        "run_id": archived_claim.get("run_id"),
        "goal_submissions": 1,
        "execution_limits": archived_claim.get("execution_policy", {}).get("execution_limits"),
    }
    budget_violation = generation_budget_violation(archived_budget_record)
    if budget_violation is not None:
        raise ControllerError(f"Master rejects generation budget overrun: {budget_violation}")
    canonical_claim_path = Path(archived_claim["task_root"]) / "claim.json"
    canonical_result_path = Path(archived_claim["task_root"]) / "work/_outbox/result.json"
    if not canonical_claim_path.is_file() or file_digest(canonical_claim_path) != file_digest(archived_claim_path):
        raise ControllerError("canonical claim source is absent or changed")
    claim = claim_checker().validate_claim(canonical_claim_path)
    result = claim_checker().validate_result(canonical_result_path, canonical_claim_path)
    archived_result = verify_seal(
        strict_json(_regular(archived_result_path, "archived result"), "archived result"),
        "archived result",
    )
    if archived_result != result:
        raise ControllerError("archived result differs from canonical validated result")
    if result["run_id"] != entry["run_id"] or result["patch"]["sha256"] != entry["patch_sha256"]:
        raise ControllerError("integration result binding differs")
    artifacts = manifest.get("artifacts")
    expected_paths = list(claim["writable_paths"])
    if not isinstance(artifacts, list) or [a.get("path") for a in artifacts] != expected_paths:
        raise ControllerError("integration ownership differs")
    for artifact in artifacts:
        source = ROOT / _safe_relative(artifact["archive_path"])
        raw = _regular(source, "archived integration artifact")
        if digest(raw) != artifact["sha256"] or len(raw) != artifact["size_bytes"]:
            raise ControllerError("archived integration artifact digest differs")
    work = queue / "staging"
    if work.exists():
        raise ControllerError("integration staging path already exists")
    work.mkdir(parents=True, mode=0o700)
    try:
        # The mode-specific validators intentionally operate on a complete
        # claim-local work root.  Harvest archives only owned deliverables,
        # so rematerialize the immutable bootstrap files from the exact
        # canonical generation before validating the staged projection.  No
        # worker-writable path is copied here and the canonical tree is never
        # consulted for mutable artifacts.
        canonical_work = Path(archived_claim["task_root"]) / "work"
        for bootstrap in claim["read_only_bootstrap_files"]:
            relative = bootstrap["path"] if isinstance(bootstrap, dict) else bootstrap
            source = canonical_work / _safe_relative(relative)
            _copy_immutable(source, work / _safe_relative(relative), "integration bootstrap")
        for artifact in artifacts:
            _copy_immutable(ROOT / _safe_relative(artifact["archive_path"]), work / _safe_relative(artifact["path"]), "integration staging")
        if claim["mode"] == "TARGET-TARGET":
            # One Master candidate must not monopolize the whole scheduler
            # tick.  The validator remains trust-zero and strict, but its
            # child Lean invocations inherit a bounded slice; a timeout is
            # recorded as repair evidence and the immutable handoff remains
            # queued for the next tick.
            item_checker().validate_target(
                claim, work, ROOT, compile_files=True,
                compile_timeout_seconds=20,
            )
        else:
            program_item_checker().validate_claim(claim, canonical_claim_path, work)
        for artifact in artifacts:
            destination = ROOT / _safe_relative(artifact["path"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.is_symlink():
                raise ControllerError(f"canonical destination is a symlink: {artifact['path']}")
            if destination.exists():
                if not destination.is_file() or file_digest(destination) != artifact["sha256"]:
                    raise ControllerError(f"canonical destination already exists: {artifact['path']}")
        # A harvested handoff first gets the durable underscore cursor.  The
        # canonical Master then performs a second CAS transition to x only
        # after the staged artifacts and independent validator have passed.
        current_spec, current_rows, _ = checker().parse_blueprint()
        current = next(row for row in current_rows if row["item_id"] == entry["item_id"])
        if current["state"] == " ":
            handoff_old_blueprint, handoff_old_gantt, handoff_blueprint, handoff_gantt = _projection_candidate(entry["item_id"], "_")
            _commit_projection(handoff_old_blueprint, handoff_old_gantt, handoff_blueprint, handoff_gantt, [])
        old_blueprint, old_gantt, new_blueprint, new_gantt = _projection_candidate(entry["item_id"], "x")
        _commit_projection(old_blueprint, old_gantt, new_blueprint, new_gantt, artifacts)
    finally:
        shutil.rmtree(work, ignore_errors=False)
    gate = {
        "gate_id": "mode-specific-master-validator",
        "command_sha256": digest(canonical([claim["mode"], *claim["writable_paths"]])),
        "exit_code": 0, "passed": True,
        "stdout_sha256": digest(canonical({"item_id": entry["item_id"], "mode": claim["mode"]})),
        "stderr_sha256": digest(b""),
    }
    integrated_files = [
        {"path": artifact["path"], "sha256": artifact["sha256"], "size_bytes": artifact["size_bytes"]}
        for artifact in artifacts
    ]
    acceptance = {
        "schema_version": "awesome-theorems/stage5-proof-debt-master-acceptance/1.0",
        "program": PROGRAM, "item_id": entry["item_id"], "mode": claim["mode"],
        "master": {"principal_id": f"codex-user-goal:{GOAL_THREAD_ID}", "decision_id": f"master-{entry['item_id'].lower()}-{digest(new_blueprint)[:16]}", "authentication_sha256": digest(canonical({"thread_id": GOAL_THREAD_ID, "objective_sha256": GOAL_OBJECTIVE_SHA256}))},
        "handoff": {"claim_id": entry["claim_id"], "run_id": entry["run_id"], "claim_card_sha256": file_digest(canonical_claim_path), "worker_result_sha256": file_digest(archived_result_path), "baseline_sha256": entry["baseline_sha256"], "patch_sha256": entry["patch_sha256"], "immutable_archive_path": str(queue.relative_to(ROOT)), "immutable_archive_sha256": file_digest(queue / "harvest-manifest.json")},
        "review_decisions": [{"reviewer_id": "canonical-master-validator", "decision": "accepted", "decision_receipt_path": str(queue.relative_to(ROOT)) + "/harvest-manifest.json", "decision_receipt_sha256": file_digest(queue / "harvest-manifest.json")}],
        "integration": {"pre_tree_sha256": digest(canonical([[p, None] for p in claim["writable_paths"]])), "post_tree_sha256": digest(canonical([[a["path"], a["sha256"]] for a in artifacts])), "integrated_bytes_sha256": digest(canonical(integrated_files)), "integrated_files": integrated_files},
        "validation_gates": [gate],
        "state_transition": {"from": "handoff_waiting_master", "to": "master_accepted", "pre_blueprint_sha256": digest(old_blueprint), "post_blueprint_sha256": digest(new_blueprint), "post_gantt_sha256": digest(new_gantt)},
        "accepted_at": now(),
    }
    acceptance = seal(acceptance)
    target = HANDOFF_ARCHIVE / entry["claim_id"] / entry["baseline_sha256"] / entry["patch_sha256"] / "master-integration.json"
    atomic_json(target, acceptance, 0o444)
    entry_path.unlink()
    return acceptance


def integrate_ready_handoffs(limit: int = 1) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    if not INTEGRATION_QUEUE.is_dir():
        return results
    # ``limit`` bounds successful Master commits, not queue candidates.  A
    # known repair item must not starve independent handoffs behind it.
    for path in sorted(INTEGRATION_QUEUE.glob("*.json")):
        if len(results) >= limit:
            break
        if _repair_still_blocking(path):
            continue
        try:
            results.append(integrate_handoff_entry(path))
        except Exception as exc:
            # Preserve a deterministic, controller-owned repair item instead
            # of retrying a known canonical conflict silently on every tick.
            # The immutable handoff remains in the queue and no worker or
            # user-owned file is changed; Master can resume once the operator
            # resolves the exact conflict.
            try:
                _record_integration_failure(path, exc)
            except Exception:
                # Failure recording is observability only and must never stop
                # unrelated workers from being harvested/admitted.
                pass
            continue
    return results


def _record_integration_failure(entry_path: Path, exc: Exception) -> None:
    """Write one idempotent repair receipt for a failed Master handoff.

    Queue entries are immutable and intentionally retained.  A stable target
    name makes this operation safe under repeated cron ticks; a pre-existing
    receipt is never overwritten, so the first failure evidence remains
    auditable.
    """
    raw = _regular(entry_path, "integration entry")
    target = integration_repair_dir() / f"{entry_path.name}.repair.json"
    if target.exists() or target.is_symlink():
        return
    try:
        entry = strict_json(raw, "integration entry")
    except Exception:
        entry = {}
    body = {
        "schema_version": "awesome-theorems/stage5-v2-integration-repair/1.0",
        "program": PROGRAM,
        "state": "repair_required",
        "entry_path": str(entry_path.relative_to(RUNTIME)),
        "entry_sha256": digest(raw),
        "item_id": entry.get("item_id"),
        "claim_id": entry.get("claim_id"),
        "run_id": entry.get("run_id"),
        "reason": str(exc),
        "recorded_at": now(),
    }
    atomic_json(target, seal(body), 0o444)


def _integrate_once(state: dict[str, Any], limit: int = 1) -> list[dict[str, Any]]:
    results = integrate_ready_handoffs(limit)
    if results:
        state["active_integrations"] = 0
        state.setdefault("integrations", []).extend(results)
    return results


def run_bounded_master_integration(
    limit: int,
    revoked_acceptances: dict[tuple[str, str, str], dict[str, str]],
) -> list[dict[str, Any]]:
    """Run the prompt-bounded Master phase outside the scheduler lease.

    Provider admission and canonical integration are independent resources.  A
    provider breaker may pause new `/goal` requests, but it must not freeze
    already harvested, dependency-ready handoffs.  Publish the short-lived
    integration lease under the scheduler lock, perform the slow validator/CAS
    work without that lock, then reconcile immutable acceptance receipts back
    into controller state under a fresh short transaction.
    """
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ControllerError("integration limit is invalid")
    # A strict Master validator is intentionally bounded per tick.  The
    # integration vector is a concurrency ceiling, not permission to serialize
    # an unbounded number of 20-second Lean attempts in one cron invocation.
    integration_budget = max(1, min(int(limit), 2))
    candidates = [
        path for path in sorted(INTEGRATION_QUEUE.glob("*.json"))
        if not _repair_still_blocking(path)
    ]
    admitted = min(integration_budget, len(candidates))
    with scheduler_guard():
        state = load_state()
        state["active_integrations"] = admitted
        save_state(state)
    results: list[dict[str, Any]] = []
    try:
        if admitted:
            results = integrate_ready_handoffs(admitted)
        return results
    finally:
        with scheduler_guard():
            state = load_state()
            state["active_integrations"] = 0
            if results:
                state.setdefault("integrations", []).extend(results)
            reconcile_integrated_handoffs(state, revoked_acceptances)
            save_state(state)


def reconcile_semantic_revocations(
    state: dict[str, Any],
    revoked_acceptances: dict[tuple[str, str, str], dict[str, str]],
) -> int:
    """Project reviewed revocations without replaying validators under a lock."""
    changed = 0
    for (item_id, run_id, acceptance_sha), evidence in revoked_acceptances.items():
        record = state.get("claims", {}).get(item_id)
        if not isinstance(record, dict) or record.get("run_id") != run_id:
            continue
        wanted = {
            "status": "invalidated",
            "work_state": "not_done",
            "invalidated_master_acceptance_sha256": acceptance_sha,
            "invalidated_reason": (
                "accepted generation failed comment-stripped "
                "exact-provider semantic replay"
            ),
            "semantic_replay_failure_sha256": evidence["replay_failure_sha256"],
        }
        stale = any(record.get(key) != value for key, value in wanted.items())
        stale = stale or any(
            key in record for key in (
                "integration", "master_accepted_at", "harvest_error",
                "terminal_reason", "retired_reason",
            )
        )
        if stale:
            record.update(wanted)
            for key in (
                "integration", "master_accepted_at", "harvest_error",
                "terminal_reason", "retired_reason",
            ):
                record.pop(key, None)
            changed += 1
    return changed


def reconcile_integrated_handoffs(
    state: dict[str, Any],
    revoked_acceptances: dict[tuple[str, str, str], dict[str, str]],
) -> int:
    """Bind already-committed Master receipts back into controller state.

    Integration is a durable CAS transaction and may complete immediately
    before a process crash or an operator-side retry.  On the next tick the
    queue can therefore be empty while the claim record still says
    ``handoff_ready``.  Reconcile only by matching the immutable acceptance
    receipt's item/run/claim identity; never infer acceptance from Blueprint
    checkboxes alone.
    """
    changed = reconcile_semantic_revocations(state, revoked_acceptances)
    accepted_keys: set[tuple[str, str, str]] = set()
    accepted_item_runs: set[tuple[str, str]] = set()
    accepted_items: dict[str, tuple[Path, dict[str, Any]]] = {}
    for acceptance_path in HANDOFF_ARCHIVE.rglob("master-integration.json"):
        try:
            acceptance = verify_seal(
                strict_json(_regular(acceptance_path, "master integration"), "master integration"),
                "master integration",
            )
        except Exception:
            continue
        handoff = acceptance.get("handoff", {})
        item_id = acceptance.get("item_id")
        run_id = handoff.get("run_id")
        patch_sha = handoff.get("patch_sha256", "")
        acceptance_sha = file_digest(acceptance_path)
        revoked = revoked_acceptances.get((item_id, run_id, acceptance_sha))
        if revoked is not None:
            # A reviewed semantic revocation dominates this exact historical
            # receipt forever.  Do not let generic receipt reconciliation
            # resurrect its runtime credit.  A later generation has a
            # different run/receipt identity and remains independently
            # eligible for Master acceptance.
            continue
        accepted_keys.add((item_id, run_id, patch_sha))
        accepted_item_runs.add((item_id, run_id))
        if isinstance(item_id, str):
            accepted_items[item_id] = (acceptance_path, acceptance)
        record = state.get("claims", {}).get(item_id)
        if not isinstance(record, dict) or record.get("run_id") != run_id:
            continue
        stale_diagnostics = any(record.get(key) for key in ("harvest_error", "terminal_reason", "retired_reason"))
        if record.get("status") == "master_accepted":
            if stale_diagnostics:
                record.pop("harvest_error", None)
                record.pop("terminal_reason", None)
                record.pop("retired_reason", None)
                changed += 1
            continue
        record["status"] = "master_accepted"
        # A durable Master acceptance supersedes transient harvest diagnostics
        # from an earlier retry of the same item.  Keep the acceptance receipt
        # as the authority and avoid presenting stale baseline/transport errors
        # as current state.
        record.pop("harvest_error", None)
        record.pop("terminal_reason", None)
        record.pop("retired_reason", None)
        record["integration"] = {
            "acceptance_path": str(acceptance_path),
            "acceptance_sha256": file_digest(acceptance_path),
            "accepted_at": acceptance.get("accepted_at"),
        }
        record["master_accepted_at"] = acceptance.get("accepted_at")
        changed += 1
    # A queue entry is only removable after its exact immutable acceptance is
    # present.  This prevents a stale retry record from blocking admission
    # while preserving every archive and acceptance receipt.
    for entry_path in INTEGRATION_QUEUE.glob("*.json"):
        try:
            entry = verify_seal(
                strict_json(_regular(entry_path, "integration entry"), "integration entry"),
                "integration entry",
            )
        except Exception:
            continue
        key = (entry.get("item_id", ""), entry.get("run_id", ""), entry.get("patch_sha256", ""))
        if key in accepted_keys:
            entry_path.unlink()
            changed += 1
    # Remove only repair receipts whose exact immutable handoff has since
    # received a matching Master acceptance.  Genuine unresolved conflicts
    # remain durable and visible in the repair backlog.
    repair_dir = integration_repair_dir()
    if repair_dir.is_dir():
        for repair_path in repair_dir.glob("*.json"):
            try:
                repair = verify_seal(strict_json(_regular(repair_path, "integration repair"), "integration repair"), "integration repair")
                entry_rel = repair.get("entry_path")
                if not isinstance(entry_rel, str):
                    continue
                entry_path = RUNTIME / _safe_relative(entry_rel)
                if not entry_path.exists():
                    # A queue entry may already have been removed after its
                    # exact Master acceptance.  The repair receipt still
                    # carries immutable item/run identity, so that acceptance
                    # is sufficient to retire this stale diagnostic without
                    # weakening genuine same-run patch checks.
                    if (repair.get("item_id", ""), repair.get("run_id", "")) in accepted_item_runs:
                        repair_path.unlink()
                        changed += 1
                    continue
                entry = verify_seal(strict_json(_regular(entry_path, "integration entry"), "integration entry"), "integration entry")
                key = (entry.get("item_id", ""), entry.get("run_id", ""), entry.get("patch_sha256", ""))
                if key in accepted_keys:
                    repair_path.unlink()
                    changed += 1
            except Exception:
                continue
    # A newer, independently validated generation may Master-accept the same
    # work item while an older conflicting handoff remains queued.  Preserve a
    # sealed supersession disposition in that older immutable archive, then
    # remove only its runtime queue/repair pointers.  Never do this for an item
    # that is not currently [x] or lacks a verifiable Master acceptance.
    try:
        blueprint_accepted = accepted_item_ids_from_blueprint()
    except Exception:
        blueprint_accepted = set()
    superseded_dir = RUNTIME / "dispositions/superseded"
    for entry_path in list(INTEGRATION_QUEUE.glob("*.json")):
        try:
            entry = verify_seal(strict_json(_regular(entry_path, "integration entry"), "integration entry"), "integration entry")
            item_id = entry.get("item_id")
            selected = accepted_items.get(item_id)
            if item_id not in blueprint_accepted or selected is None:
                continue
            acceptance_path, acceptance = selected
            accepted_run = acceptance.get("handoff", {}).get("run_id")
            if accepted_run == entry.get("run_id"):
                continue
            queue = ROOT / _safe_relative(entry["queue"])
            manifest = verify_seal(strict_json(_regular(queue / "harvest-manifest.json", "superseded harvest manifest"), "superseded harvest manifest"), "superseded harvest manifest")
            archive = ROOT / _safe_relative(manifest["archive"])
            repair_path = integration_repair_dir() / f"{entry_path.name}.repair.json"
            if not repair_path.is_file():
                continue
            repair = verify_seal(strict_json(_regular(repair_path, "superseded integration repair"), "superseded integration repair"), "superseded integration repair")
            body = {
                "schema_version":"awesome-theorems/stage5-v2-superseded-handoff/1.0",
                "program":PROGRAM, "item_id":item_id,
                "superseded_run_id":entry.get("run_id"),
                "superseded_entry_sha256":file_digest(entry_path),
                "superseded_repair_sha256":file_digest(repair_path),
                "superseded_repair_reason":repair.get("reason"),
                "master_accepted_run_id":accepted_run,
                "master_acceptance_path":str(acceptance_path.relative_to(ROOT)),
                "master_acceptance_sha256":file_digest(acceptance_path),
                "dispositioned_at":now(),
            }
            receipt = seal(body)
            immutable_receipt = archive / "superseded-handoff.json"
            atomic_json(immutable_receipt, receipt, 0o444)
            superseded_dir.mkdir(parents=True, exist_ok=True)
            _copy_immutable(immutable_receipt, superseded_dir / f"{entry_path.name}.json", "superseded handoff disposition")
            repair_path.unlink()
            entry_path.unlink()
            changed += 1
        except Exception:
            continue
    if changed:
        save_state(state)
    return changed


def accepted_item_ids_from_blueprint() -> set[str]:
    """Read current Master-accepted work identities from the sole authority."""
    _, rows, _ = checker().parse_blueprint()
    return {row["item_id"] for row in rows if row["state"] == "x"}


def retire_generations_for_master_accepted_items(
    state: dict[str, Any], accepted_ids: set[str],
) -> list[dict[str, Any]]:
    """Fence obsolete replacements without regressing accepted work state."""
    retiring: list[dict[str, Any]] = []
    for item_id in sorted(accepted_ids):
        record = state.get("claims", {}).get(item_id)
        if not isinstance(record, dict) or record.get("status") not in ACTIVE_GENERATION_STATUSES:
            continue
        record["status"] = "generation_retire_required"
        record["terminal_reason"] = "master_accepted_superseded_generation"
        record["retired_reason"] = "immutable_master_acceptance_supersedes_active_replacement"
        retiring.append(dict(record))
        append_event("generation_retire_required", {
            "item_id": item_id, "claim_id": record.get("claim_id"),
            "run_id": record.get("run_id"), "retired_reason": record["retired_reason"],
        })
    if retiring:
        save_state(state)
    return retiring


def finalize_master_accepted_retirement(record: dict[str, Any]) -> None:
    """Stop one obsolete generation and retain Master acceptance as work truth."""
    with scheduler_guard(nonblocking=False):
        state = load_state()
        current = state.setdefault("claims", {}).get(record["item_id"])
        if not isinstance(current, dict) or current.get("generation_id") != record.get("generation_id"):
            return
        settle_generation_budget(state, current, "master_accepted_superseded_generation")
        stop_record(current)
        current["generation_status"] = "retired"
        current["generation_retired_at"] = now()
        current["generation_retired_epoch"] = time.time()
        state.setdefault("generation_history", []).append(dict(current))
        state["claims"][record["item_id"]] = {
            "item_id": record["item_id"], "claim_id": record.get("claim_id"),
            "run_id": record.get("run_id"), "generation_id": record.get("generation_id"),
            "lane_id": record.get("lane_id", record["item_id"]),
            "status": "master_accepted", "work_state": "master_accepted",
            "master_accepted_at": now(),
            "retired_generation_reason": current.get("retired_reason"),
        }
        append_event("generation_retired_after_master_acceptance", {
            "item_id": record["item_id"], "claim_id": record.get("claim_id"),
            "run_id": record.get("run_id"), "retired_reason": current.get("retired_reason"),
        })
        save_state(state)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def strict_json(raw: bytes, label: str) -> Any:
    """Parse closed authority JSON without duplicate keys or non-finite values."""
    def pairs(pairs_value: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs_value:
            if key in value:
                raise ControllerError(f"{label}: duplicate JSON key {key!r}")
            value[key] = item
        return value

    def reject_constant(value: str) -> Any:
        raise ControllerError(f"{label}: non-finite JSON number {value}")

    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ControllerError(f"{label}: invalid JSON") from exc


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body["authority_sha256"] = digest(canonical(value))
    return body


def verify_seal(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not isinstance(value.get("authority_sha256"), str):
        raise ControllerError(f"{label}: malformed authority")
    body = dict(value); authority = body.pop("authority_sha256")
    if digest(canonical(body)) != authority:
        raise ControllerError(f"{label}: authority mismatch")
    return value


def _artifact_binding(path: Path) -> str:
    """Hash one BOOT file/tree with the original manager's canonical rule."""
    if path.is_symlink() or not path.exists():
        raise ControllerError(f"successor TCB artifact is unavailable: {path}")
    if path.is_file():
        return file_digest(path)
    if not path.is_dir():
        raise ControllerError(f"successor TCB artifact is not a file/tree: {path}")
    rows: list[list[Any]] = []
    for child in sorted(path.rglob("*")):
        if child.is_symlink() or (not child.is_file() and not child.is_dir()):
            raise ControllerError(f"successor TCB tree has unsafe entry: {child}")
        if child.is_file():
            rows.append([
                child.relative_to(path).as_posix(),
                child.stat().st_mode & 0o7777,
                file_digest(child),
            ])
    if not rows:
        raise ControllerError(f"successor TCB tree is empty: {path}")
    return digest(canonical(rows))


def _successor_relative_path(value: Any, label: str) -> Path:
    if not isinstance(value, str):
        raise ControllerError(f"{label}: path is malformed")
    relative = _safe_relative(value)
    if not relative.as_posix().startswith(
        "Docs/evidence/stage5_theorems/bootstrap/controller-successions/"
    ):
        raise ControllerError(f"{label}: path is outside the successor archive")
    return ROOT / relative


def _successor_epoch_path(value: Any, migration_id: str, label: str) -> Path:
    path = _successor_relative_path(value, label)
    prefix = (
        ROOT / "Docs/evidence/stage5_theorems/bootstrap/controller-successions"
        / migration_id
    )
    try:
        path.relative_to(prefix)
    except ValueError as exc:
        raise ControllerError(f"{label}: path is outside its migration epoch") from exc
    return path


def _load_successor_trust() -> dict[str, dict[str, Any]]:
    raw = _regular(BOOT_ROLE_TRUST_ROOT, "controller successor trust root")
    if digest(raw) != BOOT_ROLE_TRUST_ROOT_SHA256:
        raise ControllerError("controller successor trust-root digest differs")
    value = verify_seal(strict_json(raw, "controller successor trust root"), "controller successor trust root")
    if (
        value.get("schema_version") != "awesome-theorems/stage5-bootstrap-role-trust-root/2.0"
        or value.get("program") != PROGRAM
        or value.get("signature_algorithm") != "Ed25519"
        or not isinstance(value.get("keys"), list)
    ):
        raise ControllerError("controller successor trust root is malformed")
    result: dict[str, dict[str, Any]] = {}
    for row in value["keys"]:
        if (
            not isinstance(row, dict)
            or set(row) != {"key_id", "principal_id", "allowed_role", "public_key_hex", "status"}
            or row.get("allowed_role") not in {"producer", "reviewer", "master"}
            or row.get("status") != "active"
            or not isinstance(row.get("key_id"), str)
            or not isinstance(row.get("principal_id"), str)
            or not isinstance(row.get("public_key_hex"), str)
            or re.fullmatch(r"[0-9a-f]{64}", row["public_key_hex"]) is None
            or row["key_id"] in result
        ):
            raise ControllerError("controller successor trust root has invalid key records")
        result[row["key_id"]] = row
    if {row["allowed_role"] for row in result.values()} != {"producer", "reviewer", "master"}:
        raise ControllerError("controller successor trust root lacks required roles")
    return result


def _verify_successor_signature(
    value: Any, *, label: str, role: str, trust: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if (
        not isinstance(value, dict)
        or set(value) != SUCCESSOR_SIGNED_FIELDS
        or value.get("schema_version") != SUCCESSOR_SIGNED_SCHEMA
        or value.get("program") != PROGRAM
        or value.get("role") != role
        or value.get("signature_algorithm") != "Ed25519"
        or not isinstance(value.get("payload"), dict)
    ):
        raise ControllerError(f"{label}: signed document fields differ")
    key = trust.get(value.get("key_id"))
    if key is None or key["allowed_role"] != role or key["principal_id"] != value.get("principal_id"):
        raise ControllerError(f"{label}: role identity is unauthenticated")
    unsigned = {
        key_name: value[key_name]
        for key_name in (
            "schema_version", "program", "role", "principal_id", "key_id",
            "signature_algorithm", "payload",
        )
    }
    signed_sha = value.get("signed_payload_sha256")
    signature = value.get("signature")
    authority = value.get("authority_sha256")
    if (
        signed_sha != digest(canonical(unsigned))
        or not isinstance(signature, str)
        or re.fullmatch(r"[0-9a-f]{128}", signature) is None
        or authority != digest(canonical({**unsigned, "signed_payload_sha256": signed_sha, "signature": signature}))
    ):
        raise ControllerError(f"{label}: signature/authority binding differs")
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(key["public_key_hex"])).verify(
            bytes.fromhex(signature), canonical(unsigned),
        )
    except (ValueError, InvalidSignature) as exc:
        raise ControllerError(f"{label}: Ed25519 signature is invalid") from exc
    return value


def _budget_invalidation_epoch_path(value: Any, migration_id: str, label: str) -> Path:
    if not isinstance(value, str):
        raise ControllerError(f"{label}: path is malformed")
    path = ROOT / _safe_relative(value)
    prefix = (
        EVIDENCE / "execution/budget-overrun-invalidations" / migration_id
    )
    try:
        path.relative_to(prefix)
    except ValueError as exc:
        raise ControllerError(f"{label}: path is outside its invalidation epoch") from exc
    return path


def validate_budget_overrun_invalidation() -> dict[str, Any]:
    """Authenticate the one affected x-to-blank execution-credit revocation."""
    trust = _load_successor_trust()
    raw = _regular(BUDGET_OVERRUN_INVALIDATION, "budget overrun invalidation")
    master = _verify_successor_signature(
        strict_json(raw, "budget overrun invalidation"),
        label="budget overrun invalidation", role="master", trust=trust,
    )
    payload = master.get("payload", {})
    if set(payload) != {
        "migration_id", "producer", "reviewers", "review_subject_sha256",
        "reviewer_authorities", "item_id", "invalidated_master_acceptance",
        "overrun_generation", "pre", "post", "preserved_master_accepted_item_ids",
        "accepted_at",
    }:
        raise ControllerError("budget overrun invalidation payload is malformed")
    migration_id = payload.get("migration_id")
    if not isinstance(migration_id, str) or re.fullmatch(r"[0-9a-f]{64}", migration_id) is None:
        raise ControllerError("budget overrun invalidation id is malformed")
    if payload.get("item_id") != "S5THM-00003496-TARGET":
        raise ControllerError("budget overrun invalidation item differs")
    producer_locator = payload.get("producer")
    reviewers = payload.get("reviewers")
    if (
        not isinstance(producer_locator, dict)
        or set(producer_locator) != {"path", "file_sha256", "authority_sha256"}
        or not isinstance(reviewers, list) or len(reviewers) != 2
    ):
        raise ControllerError("budget overrun invalidation review locators differ")
    producer_path = _budget_invalidation_epoch_path(
        producer_locator["path"], migration_id, "budget invalidation producer",
    )
    producer_raw = _regular(producer_path, "budget invalidation producer")
    producer = _verify_successor_signature(
        strict_json(producer_raw, "budget invalidation producer"),
        label="budget invalidation producer", role="producer", trust=trust,
    )
    subject = producer.get("payload", {}).get("review_subject")
    subject_sha = producer.get("payload", {}).get("review_subject_sha256")
    if (
        digest(producer_raw) != producer_locator["file_sha256"]
        or producer["authority_sha256"] != producer_locator["authority_sha256"]
        or not isinstance(subject, dict)
        or digest(canonical(subject)) != subject_sha
        or subject_sha != payload.get("review_subject_sha256")
        or producer.get("payload", {}).get("decision") != "self_tested"
        or producer.get("payload", {}).get("conflicts") != []
    ):
        raise ControllerError("budget overrun invalidation producer differs")
    subject_fields = {
        "item_id", "invalidated_master_acceptance", "overrun_generation",
        "pre", "post", "preserved_master_accepted_item_ids",
    }
    if set(subject) != subject_fields or any(payload.get(key) != subject[key] for key in subject_fields):
        raise ControllerError("budget overrun invalidation reviewed subject differs")
    principals = {master["principal_id"], producer["principal_id"]}
    reviewer_authorities: list[str] = []
    for index, locator in enumerate(reviewers):
        if not isinstance(locator, dict) or set(locator) != {"path", "file_sha256", "authority_sha256"}:
            raise ControllerError("budget overrun invalidation reviewer locator differs")
        path = _budget_invalidation_epoch_path(
            locator["path"], migration_id, f"budget invalidation reviewer {index + 1}",
        )
        reviewer_raw = _regular(path, f"budget invalidation reviewer {index + 1}")
        reviewer = _verify_successor_signature(
            strict_json(reviewer_raw, f"budget invalidation reviewer {index + 1}"),
            label=f"budget invalidation reviewer {index + 1}", role="reviewer", trust=trust,
        )
        if (
            digest(reviewer_raw) != locator["file_sha256"]
            or reviewer["authority_sha256"] != locator["authority_sha256"]
            or reviewer.get("payload", {}).get("producer_authority_sha256") != producer["authority_sha256"]
            or reviewer.get("payload", {}).get("review_subject_sha256") != subject_sha
            or reviewer.get("payload", {}).get("decision") != "pass"
            or reviewer.get("payload", {}).get("conflicts") != []
        ):
            raise ControllerError("budget overrun invalidation reviewer differs")
        principals.add(reviewer["principal_id"])
        reviewer_authorities.append(reviewer["authority_sha256"])
    if len(principals) != 4 or reviewer_authorities != payload.get("reviewer_authorities"):
        raise ControllerError("budget overrun invalidation principals differ")
    acceptance = payload["invalidated_master_acceptance"]
    if not isinstance(acceptance, dict) or set(acceptance) != {
        "path", "file_sha256", "authority_sha256", "run_id",
    }:
        raise ControllerError("invalidated Master acceptance locator differs")
    acceptance_path = ROOT / _safe_relative(acceptance["path"])
    acceptance_raw = _regular(acceptance_path, "invalidated Master acceptance")
    acceptance_value = verify_seal(
        strict_json(acceptance_raw, "invalidated Master acceptance"),
        "invalidated Master acceptance",
    )
    if (
        digest(acceptance_raw) != acceptance["file_sha256"]
        or acceptance_value.get("authority_sha256") != acceptance["authority_sha256"]
        or acceptance_value.get("item_id") != payload["item_id"]
        or acceptance_value.get("handoff", {}).get("run_id") != acceptance["run_id"]
    ):
        raise ControllerError("invalidated Master acceptance bytes differ")
    generation = payload["overrun_generation"]
    if (
        not isinstance(generation, dict)
        or generation.get("run_id") != acceptance["run_id"]
        or generation.get("claim_model_input_tokens") != 2_000_000
        or not isinstance(generation.get("measured_goal_tokens_used"), int)
        or generation["measured_goal_tokens_used"] <= generation["claim_model_input_tokens"]
        or generation.get("violation") != "model_input_token_budget_exceeded"
    ):
        raise ControllerError("budget overrun measurement does not prove the violation")
    specification, rows, _ = load_program()
    row = next(entry for entry in rows if entry["item_id"] == payload["item_id"])
    if row["state"] == "x":
        later_valid = False
        for path in HANDOFF_ARCHIVE.rglob("master-integration.json"):
            try:
                value = verify_seal(
                    strict_json(_regular(path, "replacement Master acceptance"), "replacement Master acceptance"),
                    "replacement Master acceptance",
                )
                run_id = value.get("handoff", {}).get("run_id")
                if value.get("item_id") != payload["item_id"] or run_id == acceptance["run_id"]:
                    continue
                claim_path = Path(value["handoff"]["immutable_archive_path"]) / "claim.json"
                if not claim_path.is_absolute():
                    claim_path = ROOT / claim_path
                claim = strict_json(_regular(claim_path, "replacement accepted claim"), "replacement accepted claim")
                codex_home = Path(claim["task_root"]) / "codex-home"
                goal_database = codex_home / "goals_1.sqlite"
                if goal_database.is_symlink() or not goal_database.is_file():
                    continue
                connection = sqlite3.connect(
                    f"file:{goal_database}?mode=ro", uri=True, timeout=2,
                )
                goal_rows = connection.execute(
                    "select goal_id from thread_goals order by goal_id",
                ).fetchall()
                connection.close()
                if len(goal_rows) != 1 or not isinstance(goal_rows[0][0], str):
                    continue
                record = {
                    "codex_home": str(codex_home),
                    "goal_id": goal_rows[0][0], "goal_submissions": 1,
                    "execution_limits": claim["execution_policy"]["execution_limits"],
                }
                measured = measured_generation_usage(record)
                rollout = measured.get("rollout_tokens")
                goal = measured.get("goal_registry", {})
                # Re-credit is fail-closed: a different sealed Master receipt
                # is insufficient unless both token telemetry and the sole
                # private goal's elapsed time remain measurable and in cap.
                later_valid = (
                    isinstance(rollout, dict)
                    and isinstance(goal.get("time_used_seconds"), int)
                    and generation_budget_violation(record) is None
                )
                if later_valid:
                    break
            except Exception:
                continue
        if not later_valid:
            raise ControllerError("invalidated budget-overrun credit was restored without a valid new generation")
    elif row["state"] != " ":
        raise ControllerError("budget-overrun invalidated item is in an unsupported state")
    return master


def _semantic_invalidation_epoch_path(
    value: Any, migration_id: str, label: str,
) -> Path:
    if not isinstance(value, str):
        raise ControllerError(f"{label}: path is malformed")
    path = ROOT / _safe_relative(value)
    prefix = EVIDENCE / "execution/semantic-credit-invalidations" / migration_id
    try:
        path.relative_to(prefix)
    except ValueError as exc:
        raise ControllerError(f"{label}: path is outside its invalidation epoch") from exc
    return path


def validate_semantic_credit_invalidation() -> dict[str, Any]:
    """Authenticate and enforce the reviewed semantic-credit revocation."""
    trust = _load_successor_trust()
    raw = _regular(SEMANTIC_CREDIT_INVALIDATION, "semantic credit invalidation")
    master = _verify_successor_signature(
        strict_json(raw, "semantic credit invalidation"),
        label="semantic credit invalidation", role="master", trust=trust,
    )
    payload = master.get("payload", {})
    if set(payload) != {
        "migration_id", "producer", "reviewers", "review_subject_sha256",
        "reviewer_authorities", "invalidated", "pre", "post",
        "preserved_master_accepted_item_ids", "validator_sha256", "accepted_at",
    }:
        raise ControllerError("semantic credit invalidation payload is malformed")
    migration_id = payload.get("migration_id")
    if not isinstance(migration_id, str) or re.fullmatch(r"[0-9a-f]{64}", migration_id) is None:
        raise ControllerError("semantic credit invalidation id is malformed")
    if not isinstance(payload.get("validator_sha256"), str) or re.fullmatch(
        r"[0-9a-f]{64}", payload["validator_sha256"],
    ) is None:
        raise ControllerError("semantic credit invalidation validator digest is malformed")
    # This field binds the validator that originally discovered and signed the
    # revocation.  Successor epochs separately bind the current validator and
    # the replay loop below reruns every frozen claim through that current
    # validator.  Requiring both digests to stay equal would make append-only
    # revocation evidence unusable after any legitimate gate strengthening.

    producer_locator = payload.get("producer")
    reviewer_locators = payload.get("reviewers")
    if (
        not isinstance(producer_locator, dict)
        or set(producer_locator) != {"path", "file_sha256", "authority_sha256"}
        or not isinstance(reviewer_locators, list) or len(reviewer_locators) != 2
    ):
        raise ControllerError("semantic credit invalidation review locators differ")
    producer_path = _semantic_invalidation_epoch_path(
        producer_locator["path"], migration_id, "semantic invalidation producer",
    )
    producer_raw = _regular(producer_path, "semantic invalidation producer")
    producer = _verify_successor_signature(
        strict_json(producer_raw, "semantic invalidation producer"),
        label="semantic invalidation producer", role="producer", trust=trust,
    )
    subject = producer.get("payload", {}).get("review_subject")
    subject_sha = producer.get("payload", {}).get("review_subject_sha256")
    subject_fields = {
        "invalidated", "pre", "post", "preserved_master_accepted_item_ids",
        "validator_sha256",
    }
    if (
        digest(producer_raw) != producer_locator["file_sha256"]
        or producer["authority_sha256"] != producer_locator["authority_sha256"]
        or not isinstance(subject, dict) or set(subject) != subject_fields
        or digest(canonical(subject)) != subject_sha
        or subject_sha != payload.get("review_subject_sha256")
        or any(payload.get(key) != subject[key] for key in subject_fields)
        or producer.get("payload", {}).get("decision") != "self_tested"
        or producer.get("payload", {}).get("conflicts") != []
    ):
        raise ControllerError("semantic credit invalidation producer differs")
    principals = {master["principal_id"], producer["principal_id"]}
    reviewer_authorities: list[str] = []
    for index, locator in enumerate(reviewer_locators):
        if not isinstance(locator, dict) or set(locator) != {
            "path", "file_sha256", "authority_sha256",
        }:
            raise ControllerError("semantic credit invalidation reviewer locator differs")
        path = _semantic_invalidation_epoch_path(
            locator["path"], migration_id,
            f"semantic invalidation reviewer {index + 1}",
        )
        reviewer_raw = _regular(path, f"semantic invalidation reviewer {index + 1}")
        reviewer = _verify_successor_signature(
            strict_json(reviewer_raw, f"semantic invalidation reviewer {index + 1}"),
            label=f"semantic invalidation reviewer {index + 1}",
            role="reviewer", trust=trust,
        )
        if (
            digest(reviewer_raw) != locator["file_sha256"]
            or reviewer["authority_sha256"] != locator["authority_sha256"]
            or reviewer.get("payload", {}).get("producer_authority_sha256")
            != producer["authority_sha256"]
            or reviewer.get("payload", {}).get("review_subject_sha256") != subject_sha
            or reviewer.get("payload", {}).get("decision") != "pass"
            or reviewer.get("payload", {}).get("conflicts") != []
        ):
            raise ControllerError("semantic credit invalidation reviewer differs")
        principals.add(reviewer["principal_id"])
        reviewer_authorities.append(reviewer["authority_sha256"])
    if len(principals) != 4 or reviewer_authorities != payload.get("reviewer_authorities"):
        raise ControllerError("semantic credit invalidation principals differ")

    invalidated = payload.get("invalidated")
    if not isinstance(invalidated, list) or not invalidated:
        raise ControllerError("semantic credit invalidation item set is empty")
    item_ids: list[str] = []
    replay_identity: list[dict[str, str]] = []
    validator = item_checker()
    for entry in invalidated:
        if not isinstance(entry, dict) or set(entry) != {
            "item_id", "run_id", "master_receipt_path",
            "master_receipt_file_sha256", "master_receipt_authority_sha256",
            "claim_path", "claim_sha256", "replay_exit_code",
            "replay_failure", "replay_failure_sha256",
        }:
            raise ControllerError("semantic credit invalidation entry is malformed")
        item_id = entry["item_id"]
        run_id = entry["run_id"]
        if (
            not isinstance(item_id, str) or re.fullmatch(r"S5THM-[0-9]{8}-TARGET", item_id) is None
            or not isinstance(run_id, str) or not run_id
            or entry.get("replay_exit_code") != 1
            or not isinstance(entry.get("replay_failure"), str)
            or digest(entry["replay_failure"].encode()) != entry.get("replay_failure_sha256")
        ):
            raise ControllerError("semantic credit invalidation replay identity differs")
        receipt_path = ROOT / _safe_relative(entry["master_receipt_path"])
        receipt_raw = _regular(receipt_path, "invalidated semantic Master receipt")
        receipt = verify_seal(
            strict_json(receipt_raw, "invalidated semantic Master receipt"),
            "invalidated semantic Master receipt",
        )
        claim_path = ROOT / _safe_relative(entry["claim_path"])
        claim_raw = _regular(claim_path, "invalidated semantic claim")
        claim = strict_json(claim_raw, "invalidated semantic claim")
        if (
            digest(receipt_raw) != entry["master_receipt_file_sha256"]
            or receipt.get("authority_sha256") != entry["master_receipt_authority_sha256"]
            or receipt.get("item_id") != item_id
            or receipt.get("handoff", {}).get("run_id") != run_id
            or digest(claim_raw) != entry["claim_sha256"]
            or claim.get("item_id") != item_id or claim.get("run_id") != run_id
        ):
            raise ControllerError("semantic credit invalidation evidence differs")
        try:
            validator.validate_target(
                claim, Path(claim["task_root"]) / "work", ROOT,
                compile_files=False,
            )
        except validator.ItemError:
            # The signed failure text remains immutable evidence from the
            # validator version recorded in ``payload.validator_sha256``.
            # A successor validator may add an earlier/stronger gate (for
            # example a sealed provider-kernel route) and therefore reject the
            # same historical claim for a different reason.  Revocation is
            # monotone: the current validator must still reject the exact
            # claim, but diagnostic wording is not a cross-version authority.
            pass
        else:
            raise ControllerError("invalidated semantic generation now passes its frozen replay")
        item_ids.append(item_id)
        replay_identity.append({
            "item_id": item_id, "run_id": run_id,
            "master_receipt_file_sha256": entry["master_receipt_file_sha256"],
            "replay_failure_sha256": entry["replay_failure_sha256"],
        })
    if item_ids != sorted(item_ids) or len(item_ids) != len(set(item_ids)):
        raise ControllerError("semantic credit invalidation item identities overlap/order differs")

    pre = payload.get("pre")
    post = payload.get("post")
    locator_fields = {
        "blueprint_path", "blueprint_sha256", "gantt_path", "gantt_sha256",
        "state_path", "state_sha256",
    }
    if not isinstance(pre, dict) or set(pre) != locator_fields or not isinstance(post, dict) or set(post) != locator_fields:
        raise ControllerError("semantic credit invalidation projection locators differ")
    pre_blueprint_path = _semantic_invalidation_epoch_path(
        pre["blueprint_path"], migration_id, "semantic invalidation pre Blueprint",
    )
    post_blueprint_path = _semantic_invalidation_epoch_path(
        post["blueprint_path"], migration_id, "semantic invalidation post Blueprint",
    )
    for value, label in ((pre, "pre"), (post, "post")):
        for kind in ("blueprint", "gantt", "state"):
            path = _semantic_invalidation_epoch_path(
                value[f"{kind}_path"], migration_id,
                f"semantic invalidation {label} {kind}",
            )
            if file_digest(path) != value[f"{kind}_sha256"]:
                raise ControllerError("semantic credit invalidation archived projection differs")
    _, pre_rows, _ = checker().parse_blueprint(pre_blueprint_path)
    _, post_rows, _ = checker().parse_blueprint(post_blueprint_path)
    pre_states = {row["item_id"]: row["state"] for row in pre_rows}
    post_states = {row["item_id"]: row["state"] for row in post_rows}
    changed = sorted(key for key in pre_states if pre_states[key] != post_states[key])
    if (
        changed != item_ids
        or any(pre_states[key] != "x" or post_states[key] != " " for key in item_ids)
        or [row["item_id"] for row in post_rows if row["state"] == "x"]
        != payload.get("preserved_master_accepted_item_ids")
    ):
        raise ControllerError("semantic credit invalidation is not the reviewed x-to-blank batch")
    expected_migration_id = digest(canonical({
        "schema_version": "awesome-theorems/stage5-semantic-credit-invalidation-id/1.0",
        "program": PROGRAM, "invalidated": replay_identity,
        "pre_blueprint_sha256": pre["blueprint_sha256"],
        "post_blueprint_sha256": post["blueprint_sha256"],
        "pre_state_sha256": pre["state_sha256"],
        "post_state_sha256": post["state_sha256"],
        "validator_sha256": payload["validator_sha256"],
    }))
    if migration_id != expected_migration_id:
        raise ControllerError("semantic credit invalidation content address differs")

    _, current_rows, _ = load_program()
    for row in current_rows:
        if row["item_id"] not in set(item_ids) or row["state"] != "x":
            continue
        later_valid = False
        for receipt_path in HANDOFF_ARCHIVE.glob(
            f"{row['item_id']}--worker/*/*/master-integration.json"
        ):
            try:
                receipt = verify_seal(
                    strict_json(_regular(receipt_path, "replacement semantic Master receipt"),
                                "replacement semantic Master receipt"),
                    "replacement semantic Master receipt",
                )
                if receipt.get("accepted_at", "") <= payload["accepted_at"]:
                    continue
                claim_path = Path(receipt["handoff"]["immutable_archive_path"]) / "claim.json"
                if not claim_path.is_absolute():
                    claim_path = ROOT / claim_path
                claim = strict_json(_regular(claim_path, "replacement semantic claim"),
                                    "replacement semantic claim")
                validator.validate_target(
                    claim, Path(claim["task_root"]) / "work", ROOT,
                    compile_files=False,
                )
                later_valid = True
                break
            except Exception:
                continue
        if not later_valid:
            raise ControllerError("invalidated semantic credit was restored without a valid new generation")
    return master


def semantic_revoked_master_acceptances() -> dict[tuple[str, str, str], dict[str, str]]:
    """Return exact reviewed receipt identities that can never regain credit."""
    master = validate_semantic_credit_invalidation()
    bindings: dict[tuple[str, str, str], dict[str, str]] = {}
    for entry in master["payload"]["invalidated"]:
        key = (
            entry["item_id"], entry["run_id"],
            entry["master_receipt_file_sha256"],
        )
        if key in bindings:
            raise ControllerError("semantic revocation receipt identities overlap")
        bindings[key] = {
            "replay_failure_sha256": entry["replay_failure_sha256"],
        }
    return bindings


def validate_controller_successor_acceptance(
    specification: dict[str, Any] | None = None,
    acceptance_path: Path | None = None,
) -> dict[str, Any]:
    """Authenticate the append-only four-principal successor TCB chain."""
    if specification is None:
        specification, _, _ = load_program()
    trust = _load_successor_trust()
    authority_path = acceptance_path or CONTROLLER_SUCCESSOR_ACCEPTANCE
    raw = _regular(authority_path, "controller successor acceptance")
    master = _verify_successor_signature(
        strict_json(raw, "controller successor acceptance"),
        label="controller successor acceptance", role="master", trust=trust,
    )
    payload = master["payload"]
    required = {
        "migration_id", "producer", "reviewers", "predecessor_boot",
        "predecessor_controller_successor", "predecessor_activation",
        "maintenance_intent", "successor_artifacts", "unchanged_boot_artifacts",
        "frozen_authorities", "paused_snapshot", "validation", "safety",
        "review_subject_sha256", "reviewer_authorities", "accepted_at",
    }
    if set(payload) != required:
        raise ControllerError("controller successor acceptance payload is open/malformed")
    migration_id = payload.get("migration_id")
    if not isinstance(migration_id, str) or re.fullmatch(r"[0-9a-f]{64}", migration_id) is None:
        raise ControllerError("controller successor migration id is malformed")

    principals = {master["principal_id"]}
    producer_locator = payload.get("producer")
    if not isinstance(producer_locator, dict) or set(producer_locator) != {"path", "file_sha256", "authority_sha256"}:
        raise ControllerError("controller successor producer locator is malformed")
    producer_path = _successor_epoch_path(
        producer_locator["path"], migration_id, "controller successor producer",
    )
    producer_raw = _regular(producer_path, "controller successor producer")
    if digest(producer_raw) != producer_locator["file_sha256"]:
        raise ControllerError("controller successor producer file digest differs")
    producer = _verify_successor_signature(
        strict_json(producer_raw, "controller successor producer"),
        label="controller successor producer", role="producer", trust=trust,
    )
    producer_payload = producer["payload"]
    if (
        producer["authority_sha256"] != producer_locator["authority_sha256"]
        or set(producer_payload) != {
            "migration_id", "review_subject", "review_subject_sha256", "decision",
            "conflicts", "prepared_at",
        }
        or producer_payload.get("migration_id") != migration_id
        or producer_payload.get("decision") != "self_tested"
        or producer_payload.get("conflicts") != []
        or not isinstance(producer_payload.get("review_subject"), dict)
        or digest(canonical(producer_payload["review_subject"])) != producer_payload.get("review_subject_sha256")
    ):
        raise ControllerError("controller successor producer authority differs")
    principals.add(producer["principal_id"])

    reviewers = payload.get("reviewers")
    if not isinstance(reviewers, list) or len(reviewers) != 2:
        raise ControllerError("controller successor requires exactly two reviewers")
    reviewer_authorities: list[str] = []
    for index, locator in enumerate(reviewers):
        if not isinstance(locator, dict) or set(locator) != {"path", "file_sha256", "authority_sha256"}:
            raise ControllerError("controller successor reviewer locator is malformed")
        reviewer_path = _successor_epoch_path(
            locator["path"], migration_id, f"controller successor reviewer {index + 1}",
        )
        reviewer_raw = _regular(reviewer_path, f"controller successor reviewer {index + 1}")
        if digest(reviewer_raw) != locator["file_sha256"]:
            raise ControllerError("controller successor reviewer file digest differs")
        reviewer = _verify_successor_signature(
            strict_json(reviewer_raw, f"controller successor reviewer {index + 1}"),
            label=f"controller successor reviewer {index + 1}", role="reviewer", trust=trust,
        )
        if (
            reviewer["authority_sha256"] != locator["authority_sha256"]
            or set(reviewer["payload"]) != {
                "migration_id", "producer_authority_sha256", "review_subject_sha256",
                "decision", "conflicts", "reviewed_at",
            }
            or reviewer["payload"].get("migration_id") != migration_id
            or reviewer["payload"].get("producer_authority_sha256") != producer["authority_sha256"]
            or reviewer["payload"].get("review_subject_sha256") != producer_payload["review_subject_sha256"]
            or reviewer["payload"].get("decision") != "pass"
            or reviewer["payload"].get("conflicts") != []
        ):
            raise ControllerError("controller successor reviewer decision differs")
        principals.add(reviewer["principal_id"])
        reviewer_authorities.append(reviewer["authority_sha256"])
    if len(principals) != 4:
        raise ControllerError("controller successor role principals are not identity-distinct")
    if producer_payload.get("review_subject_sha256") != payload.get("review_subject_sha256"):
        raise ControllerError("controller successor reviewed subject differs")
    if payload.get("reviewer_authorities") != reviewer_authorities:
        raise ControllerError("controller successor reviewer authority order differs")
    subject = producer_payload["review_subject"]
    subject_fields = {
        "predecessor_boot", "predecessor_controller_successor",
        "predecessor_activation", "maintenance_intent", "successor_artifacts",
        "unchanged_boot_artifacts", "frozen_authorities", "paused_snapshot",
        "validation", "safety",
    }
    if set(subject) != subject_fields or any(payload.get(key_name) != subject[key_name] for key_name in subject_fields):
        raise ControllerError("controller successor master does not reproduce reviewed subject")

    predecessor_boot = payload.get("predecessor_boot")
    if not isinstance(predecessor_boot, list) or len(predecessor_boot) != 5:
        raise ControllerError("controller successor predecessor BOOT chain is incomplete")
    expected_boot_paths = {
        "Docs/evidence/stage5_theorems/controller-bootstrap-handoff.json",
        "Docs/evidence/stage5_theorems/controller-bootstrap-handoff-acceptance.json",
        "Docs/evidence/stage5_theorems/controller-bootstrap-review.json",
        "Docs/evidence/stage5_theorems/controller-bootstrap-acceptance.json",
        "Docs/evidence/stage5_theorems/controller-bootstrap-role-trust-root.json",
    }
    observed_boot_paths: set[str] = set()
    for entry in predecessor_boot:
        if not isinstance(entry, dict) or set(entry) != {
            "path", "archive_path", "file_sha256", "authority_sha256",
        }:
            raise ControllerError("controller successor predecessor BOOT locator is malformed")
        original = entry["path"]
        if original in observed_boot_paths or original not in expected_boot_paths:
            raise ControllerError("controller successor predecessor BOOT path differs")
        observed_boot_paths.add(original)
        original_path = ROOT / _safe_relative(original)
        archive_path = _successor_epoch_path(
            entry["archive_path"], migration_id, "predecessor BOOT archive",
        )
        original_raw = _regular(original_path, "predecessor BOOT authority")
        archive_raw = _regular(archive_path, "predecessor BOOT archive")
        if original_raw != archive_raw or digest(original_raw) != entry["file_sha256"]:
            raise ControllerError("controller successor predecessor BOOT bytes differ")
        predecessor = verify_seal(strict_json(original_raw, "predecessor BOOT authority"), "predecessor BOOT authority")
        if predecessor.get("authority_sha256") != entry["authority_sha256"]:
            raise ControllerError("controller successor predecessor BOOT authority differs")
    if observed_boot_paths != expected_boot_paths:
        raise ControllerError("controller successor predecessor BOOT path set differs")

    predecessor_successor = payload.get("predecessor_controller_successor")
    if not isinstance(predecessor_successor, dict) or set(predecessor_successor) != {
        "path", "file_sha256", "authority_sha256",
    }:
        raise ControllerError("controller predecessor-successor locator is malformed")
    predecessor_successor_path = _successor_epoch_path(
        predecessor_successor["path"], migration_id, "predecessor controller successor",
    )
    predecessor_successor_raw = _regular(
        predecessor_successor_path, "predecessor controller successor",
    )
    if digest(predecessor_successor_raw) != predecessor_successor["file_sha256"]:
        raise ControllerError("predecessor controller successor file digest differs")
    predecessor_successor_value = _verify_successor_signature(
        strict_json(predecessor_successor_raw, "predecessor controller successor"),
        label="predecessor controller successor", role="master", trust=trust,
    )
    if predecessor_successor_value["authority_sha256"] != predecessor_successor["authority_sha256"]:
        raise ControllerError("predecessor controller successor authority differs")

    maintenance_locator = payload.get("maintenance_intent")
    if not isinstance(maintenance_locator, dict) or set(maintenance_locator) != {
        "path", "file_sha256", "authority_sha256", "action",
        "consumption_path", "consumption_file_sha256", "consumption_authority_sha256",
    }:
        raise ControllerError("controller successor maintenance locator is malformed")
    maintenance_path = _successor_epoch_path(
        maintenance_locator["path"], migration_id, "accepted maintenance intent",
    )
    maintenance_raw = _regular(maintenance_path, "accepted maintenance intent")
    maintenance = _verify_successor_signature(
        strict_json(maintenance_raw, "accepted maintenance intent"),
        label="accepted maintenance intent", role="producer", trust=trust,
    )
    maintenance_payload = maintenance["payload"]
    consumption_path = _successor_epoch_path(
        maintenance_locator["consumption_path"], migration_id,
        "accepted maintenance consumption",
    )
    consumption_raw = _regular(consumption_path, "accepted maintenance consumption")
    consumption = verify_seal(
        strict_json(consumption_raw, "accepted maintenance consumption"),
        "accepted maintenance consumption",
    )
    if (
        digest(maintenance_raw) != maintenance_locator["file_sha256"]
        or maintenance["authority_sha256"] != maintenance_locator["authority_sha256"]
        or maintenance_locator["action"] != "paused_reconcile_fence_and_refill_only"
        or maintenance_payload.get("action") != maintenance_locator["action"]
        or maintenance_payload.get("predecessor_successor", {}).get("file_sha256")
        != predecessor_successor["file_sha256"]
        or maintenance_payload.get("predecessor_successor", {}).get("authority_sha256")
        != predecessor_successor["authority_sha256"]
        or maintenance_payload.get("candidate_artifacts") != {
            "controller_sha256": file_digest(Path(__file__)),
            "controller_test_sha256": file_digest(ROOT / "scripts/test_stage5_theorems_execution_cron_v2.py"),
            "migration_tool_sha256": file_digest(ROOT / "scripts/accept_stage5_theorem_controller_successor.py"),
            "checker_sha256": file_digest(CHECKER_PATH),
            "checker_test_sha256": file_digest(ROOT / "scripts/test_stage5_theorems_blueprint.py"),
            "item_checker_sha256": file_digest(ITEM_CHECKER_PATH),
            "item_checker_test_sha256": file_digest(ROOT / "scripts/test_stage5_theorem_item.py"),
        }
        or digest(consumption_raw) != maintenance_locator["consumption_file_sha256"]
        or consumption.get("authority_sha256") != maintenance_locator["consumption_authority_sha256"]
        or consumption.get("schema_version")
        != "awesome-theorems/stage5-controller-successor-maintenance-consumption/1.0"
        or consumption.get("program") != PROGRAM
        or consumption.get("intent_authority_sha256") != maintenance["authority_sha256"]
        or consumption.get("intent_file_sha256") != digest(maintenance_raw)
        or consumption.get("action") != maintenance_locator["action"]
        or consumption.get("candidate_artifacts") != maintenance_payload.get("candidate_artifacts")
    ):
        raise ControllerError("controller successor accepted maintenance intent differs")

    predecessor_activation = payload.get("predecessor_activation")
    if not isinstance(predecessor_activation, dict) or set(predecessor_activation) != {
        "path", "archive_path", "file_sha256", "authority_sha256", "schema_version",
    } or predecessor_activation.get("path") != "Docs/evidence/stage5_theorems/execution/controller-activation.json":
        raise ControllerError("controller successor predecessor activation locator is malformed")
    activation_archive = _successor_epoch_path(
        predecessor_activation["archive_path"], migration_id, "predecessor activation archive",
    )
    activation_raw = _regular(activation_archive, "predecessor activation archive")
    if digest(activation_raw) != predecessor_activation["file_sha256"]:
        raise ControllerError("controller successor predecessor activation digest differs")
    predecessor_activation_value = verify_seal(
        strict_json(activation_raw, "predecessor activation archive"),
        "predecessor activation archive",
    )
    if (
        predecessor_activation_value.get("authority_sha256") != predecessor_activation["authority_sha256"]
        or predecessor_activation_value.get("schema_version") != predecessor_activation["schema_version"]
        or predecessor_activation["schema_version"] != "awesome-theorems/stage5-controller-activation/3.0"
        or predecessor_activation_value.get("controller_successor_acceptance_authority_sha256")
        != predecessor_successor["authority_sha256"]
    ):
        raise ControllerError("controller successor predecessor activation authority differs")

    successor = payload.get("successor_artifacts")
    if not isinstance(successor, dict) or set(successor) != {
        "controller_path", "controller_sha256", "controller_test_path", "controller_test_sha256",
        "migration_tool_path", "migration_tool_sha256", "checker_path", "checker_sha256",
        "checker_test_path", "checker_test_sha256",
        "item_checker_path", "item_checker_sha256",
        "item_checker_test_path", "item_checker_test_sha256",
    }:
        raise ControllerError("controller successor artifact binding is malformed")
    expected_paths = {
        "controller_path": "scripts/stage5_theorems_execution_cron_v2.py",
        "controller_test_path": "scripts/test_stage5_theorems_execution_cron_v2.py",
        "migration_tool_path": "scripts/accept_stage5_theorem_controller_successor.py",
        "checker_path": "Docs/tools/check_stage5_theorems_blueprint.py",
        "checker_test_path": "scripts/test_stage5_theorems_blueprint.py",
        "item_checker_path": "scripts/check_stage5_theorem_item.py",
        "item_checker_test_path": "scripts/test_stage5_theorem_item.py",
    }
    for key_name, expected in expected_paths.items():
        if successor.get(key_name) != expected:
            raise ControllerError("controller successor artifact path differs")
    if (
        successor["controller_sha256"] != file_digest(Path(__file__))
        or successor["controller_test_sha256"] != file_digest(ROOT / successor["controller_test_path"])
        or successor["migration_tool_sha256"] != file_digest(ROOT / successor["migration_tool_path"])
        or successor["checker_sha256"] != file_digest(ROOT / successor["checker_path"])
        or successor["checker_test_sha256"] != file_digest(ROOT / successor["checker_test_path"])
        or successor["item_checker_sha256"] != file_digest(ROOT / successor["item_checker_path"])
        or successor["item_checker_test_sha256"] != file_digest(ROOT / successor["item_checker_test_path"])
    ):
        raise ControllerError("controller successor artifact digest differs")
    unchanged = payload.get("unchanged_boot_artifacts")
    if not isinstance(unchanged, dict) or not unchanged:
        raise ControllerError("controller successor unchanged TCB set is absent")
    for relative, expected_sha in unchanged.items():
        if not isinstance(relative, str) or not isinstance(expected_sha, str):
            raise ControllerError("controller successor unchanged TCB binding is malformed")
        if _artifact_binding(ROOT / _safe_relative(relative)) != expected_sha:
            raise ControllerError(f"controller successor unchanged TCB drift: {relative}")
    frozen = payload.get("frozen_authorities")
    if (
        not isinstance(frozen, dict)
        or set(frozen) != {
            "execution_spec_sha256", "execution_spec_file_sha256",
            "concurrency_prompt_file_sha256", "concurrency_prompt_authority_sha256",
            "operator_authority_file_sha256", "operator_authority_sha256",
            "operator_budget_renewal_file_sha256",
            "operator_budget_renewal_authority_sha256",
            "budget_overrun_invalidation_file_sha256",
            "budget_overrun_invalidation_authority_sha256",
            "semantic_credit_invalidation_file_sha256",
            "semantic_credit_invalidation_authority_sha256",
            "operator_trust_root_file_sha256", "operator_trust_root_sha256",
            "route",
        }
        or frozen.get("execution_spec_sha256") != digest(canonical(specification))
        or frozen.get("execution_spec_file_sha256") != file_digest(EVIDENCE / "execution-spec.json")
    ):
        raise ControllerError("controller successor frozen execution authority differs")
    prompt_value = verify_seal(
        strict_json(_regular(CONCURRENCY_PROMPT, "successor concurrency prompt"), "successor concurrency prompt"),
        "successor concurrency prompt",
    )
    operator_value = verify_seal(
        strict_json(_regular(OPERATOR_AUTHORITY, "successor operator authority"), "successor operator authority"),
        "successor operator authority",
    )
    renewal_value = verify_seal(
        strict_json(
            _regular(OPERATOR_BUDGET_RENEWAL, "successor operator budget renewal"),
            "successor operator budget renewal",
        ),
        "successor operator budget renewal",
    )
    invalidation_value = validate_budget_overrun_invalidation()
    semantic_invalidation_value = validate_semantic_credit_invalidation()
    operator_trust_value = strict_json(
        _regular(OPERATOR_TRUST_ROOT, "successor operator trust root"),
        "successor operator trust root",
    )
    if digest(canonical(operator_trust_value)) != OPERATOR_TRUST_ROOT_SHA256:
        raise ControllerError("controller successor operator trust root differs")
    if frozen != {
        "execution_spec_sha256": digest(canonical(specification)),
        "execution_spec_file_sha256": file_digest(EVIDENCE / "execution-spec.json"),
        "concurrency_prompt_file_sha256": file_digest(CONCURRENCY_PROMPT),
        "concurrency_prompt_authority_sha256": prompt_value["authority_sha256"],
        "operator_authority_file_sha256": file_digest(OPERATOR_AUTHORITY),
        "operator_authority_sha256": operator_value["authority_sha256"],
        "operator_budget_renewal_file_sha256": file_digest(OPERATOR_BUDGET_RENEWAL),
        "operator_budget_renewal_authority_sha256": renewal_value["authority_sha256"],
        "budget_overrun_invalidation_file_sha256": file_digest(BUDGET_OVERRUN_INVALIDATION),
        "budget_overrun_invalidation_authority_sha256": invalidation_value["authority_sha256"],
        "semantic_credit_invalidation_file_sha256": file_digest(SEMANTIC_CREDIT_INVALIDATION),
        "semantic_credit_invalidation_authority_sha256": semantic_invalidation_value["authority_sha256"],
        "operator_trust_root_file_sha256": file_digest(OPERATOR_TRUST_ROOT),
        "operator_trust_root_sha256": OPERATOR_TRUST_ROOT_SHA256,
        "route": {
            "provider": PROVIDER, "model": MODEL,
            "reasoning_effort": EFFORT, "service_tier": SERVICE_TIER,
        },
    }:
        raise ControllerError("controller successor frozen authority bytes differ")

    paused = payload.get("paused_snapshot")
    if not isinstance(paused, dict) or set(paused) != {
        "crontab_sha256", "theorem_marker_absent", "harnessfs_marker_preserved",
        "blueprint_archive_path", "blueprint_sha256", "gantt_archive_path", "gantt_sha256",
        "state_archive_path", "state_sha256", "controller_recorded_live_lanes",
        "requested_authenticated_live_goals",
        "master_accepted_item_ids", "live_manifest_sha256", "live_manifest",
        "live_audit_all_checks_pass", "live_audit_failures",
    }:
        raise ControllerError("controller successor paused snapshot is malformed")
    if paused.get("theorem_marker_absent") is not True or paused.get("harnessfs_marker_preserved") is not True:
        raise ControllerError("controller successor was not prepared in an exact paused cron state")
    if (
        paused.get("requested_authenticated_live_goals") != 24
        or paused.get("live_audit_all_checks_pass") is not True
        or paused.get("live_audit_failures") != {
            "task_boundary": [], "socket": [], "process": [], "registry": [],
            "route": [], "policy": [],
        }
    ):
        raise ControllerError("controller successor paused live audit is not exact 24/24")
    for path_key, sha_key in (
        ("blueprint_archive_path", "blueprint_sha256"),
        ("gantt_archive_path", "gantt_sha256"),
        ("state_archive_path", "state_sha256"),
    ):
        archive = _successor_epoch_path(
            paused[path_key], migration_id, f"successor paused {path_key}",
        )
        if file_digest(archive) != paused[sha_key]:
            raise ControllerError("controller successor paused snapshot archive differs")
    live_manifest = paused.get("live_manifest")
    if (
        not isinstance(live_manifest, list)
        or paused.get("controller_recorded_live_lanes") != len(live_manifest)
        or paused.get("controller_recorded_live_lanes") != 24
        or digest(canonical(live_manifest)) != paused.get("live_manifest_sha256")
        or len({entry.get("item_id") for entry in live_manifest if isinstance(entry, dict)}) != 24
    ):
        raise ControllerError("controller successor grandfathered live manifest differs")
    state_archive = strict_json(
        _regular(
            _successor_epoch_path(paused["state_archive_path"], migration_id, "paused state"),
            "paused state",
        ),
        "paused state",
    )
    verify_seal(state_archive, "paused state")
    expected_spec_sha = frozen["execution_spec_sha256"]
    expected_prompt_sha = frozen["concurrency_prompt_file_sha256"]
    expected_prompt_epoch = prompt_value.get("policy_epoch")
    expected_vector = prompt_value.get("concurrency")
    manifest_fields = {
        "item_id", "claim_id", "run_id", "generation_id", "lane_id", "status",
        "task_root", "claim_sha256", "baseline_manifest_sha256", "baseline_file_count",
        "socket_path", "session", "pane_pid", "pane_pid_start_ticks", "codex_home",
        "thread_id", "goal_id", "goal_submissions", "provider", "model",
        "reasoning_effort", "service_tier", "prompt_epoch", "prompt_digest",
        "execution_spec_sha256", "baseline_execution_spec_sha256",
        "baseline_execution_spec_file_sha256", "baseline_prompt_file_sha256",
        "baseline_item_checker_sha256",
    }
    for entry in live_manifest:
        if not isinstance(entry, dict) or set(entry) != manifest_fields:
            raise ControllerError("controller successor live-manifest fields differ")
        item_id = entry.get("item_id")
        run_id = entry.get("run_id")
        if (
            not isinstance(item_id, str) or not isinstance(run_id, str)
            or re.fullmatch(r"[A-Za-z0-9._-]+", item_id) is None
            or re.fullmatch(r"[A-Za-z0-9._-]+", run_id) is None
        ):
            raise ControllerError("controller successor live-manifest identity is malformed")
        claim_archive = (
            ROOT / "Docs/evidence/stage5_theorems/bootstrap/controller-successions"
            / migration_id / "predecessor/live-claims" / f"{item_id}--{run_id}.json"
        )
        claim_raw = _regular(claim_archive, "successor archived live claim")
        claim = strict_json(claim_raw, "successor archived live claim")
        state_record = state_archive.get("claims", {}).get(item_id)
        identity = claim.get("execution_identity", {})
        baseline = claim.get("baseline", {})
        bootstrap = {
            row.get("path"): row
            for row in claim.get("read_only_bootstrap_files", [])
            if isinstance(row, dict) and isinstance(row.get("path"), str)
        }
        if (
            digest(claim_raw) != entry["claim_sha256"]
            or not isinstance(state_record, dict)
            or any(state_record.get(key) != entry.get(key) for key in (
                "item_id", "claim_id", "run_id", "generation_id", "lane_id", "status",
                "task_root", "socket_path", "session", "pane_pid", "pane_pid_start_ticks",
                "codex_home", "thread_id", "goal_id", "goal_submissions", "provider", "model",
                "reasoning_effort", "service_tier", "prompt_epoch", "prompt_digest",
            ))
            or claim.get("item_id") != item_id
            or claim.get("claim_id") != entry["claim_id"]
            or claim.get("run_id") != run_id
            or claim.get("task_root") != entry["task_root"]
            or identity.get("lane_id") != entry["lane_id"]
            or identity.get("generation_id") != entry["generation_id"]
            or identity.get("execution_spec_sha256") != expected_spec_sha
            or identity.get("prompt_epoch") != expected_prompt_epoch
            or identity.get("prompt_digest") != expected_prompt_sha
            or identity.get("requested_concurrency") != expected_vector
            or identity.get("resolved_concurrency") != expected_vector
            or baseline.get("execution_spec_sha256") != expected_spec_sha
            or bootstrap.get("_baseline/execution-spec.json", {}).get("sha256")
            != frozen["execution_spec_file_sha256"]
            or bootstrap.get("_baseline/concurrency-prompt.json", {}).get("sha256")
            != expected_prompt_sha
            or entry.get("execution_spec_sha256") != expected_spec_sha
            or entry.get("baseline_execution_spec_sha256") != expected_spec_sha
            or entry.get("baseline_execution_spec_file_sha256")
            != frozen["execution_spec_file_sha256"]
            or entry.get("baseline_prompt_file_sha256") != expected_prompt_sha
            or entry.get("baseline_item_checker_sha256") != file_digest(ITEM_CHECKER_PATH)
            or bootstrap.get("_baseline/check_stage5_theorem_item.py", {}).get("sha256")
            != file_digest(ITEM_CHECKER_PATH)
            or entry.get("prompt_epoch") != expected_prompt_epoch
            or entry.get("prompt_digest") != expected_prompt_sha
        ):
            raise ControllerError("controller successor archived live claim binding differs")

    expected_migration_id = digest(canonical({
        "schema_version": "awesome-theorems/stage5-controller-successor-id/1.0",
        "program": PROGRAM,
        "predecessor_activation_sha256": predecessor_activation["file_sha256"],
        "predecessor_controller_successor_sha256": predecessor_successor["file_sha256"],
        "controller_sha256": successor["controller_sha256"],
        "controller_test_sha256": successor["controller_test_sha256"],
        "migration_tool_sha256": successor["migration_tool_sha256"],
        "checker_sha256": successor["checker_sha256"],
        "checker_test_sha256": successor["checker_test_sha256"],
        "item_checker_sha256": successor["item_checker_sha256"],
        "item_checker_test_sha256": successor["item_checker_test_sha256"],
        "blueprint_sha256": paused["blueprint_sha256"],
        "gantt_sha256": paused["gantt_sha256"],
        "state_sha256": paused["state_sha256"],
        "live_manifest_sha256": paused["live_manifest_sha256"],
        "master_accepted_item_ids": paused["master_accepted_item_ids"],
    }))
    if migration_id != expected_migration_id:
        raise ControllerError("controller successor migration id/content address differs")

    validation = payload.get("validation")
    if not isinstance(validation, dict) or set(validation) != {"commands", "prompt_preflight"}:
        raise ControllerError("controller successor validation record is malformed")
    commands = validation.get("commands")
    if (
        not isinstance(commands, list)
        or len(commands) < 9
        or any(
            not isinstance(command, dict)
            or set(command) != {"argv", "exit_code", "stdout_sha256", "stderr_sha256"}
            or command.get("exit_code") != 0
            for command in commands
        )
    ):
        raise ControllerError("controller successor command suite did not cleanly pass")
    if validation.get("prompt_preflight") != {
        "safe_hint_count": 1,
        "task_boundary_instruction_count": 1,
        "one_total_thread_slot_count": 1,
        "permissive_multi_agent_hint_present": False,
    }:
        raise ControllerError("controller successor Codex prompt preflight differs")
    safety = payload.get("safety")
    if not isinstance(safety, dict) or safety != {
        "mathematical_acceptances_preserved": True,
        "worker_stops": 0,
        "goal_resubmissions": 0,
        "grandfathered_claim_baselines_immutable": True,
        "successor_admissions_only_use_new_controller": True,
    }:
        raise ControllerError("controller successor safety assertions differ")
    return master


def validate_controller_successor_maintenance_intent() -> dict[str, Any]:
    """Authorize one paused, capped reconcile/refill before final acceptance."""
    trust = _load_successor_trust()
    intent = _verify_successor_signature(
        strict_json(
            _regular(CONTROLLER_SUCCESSOR_MAINTENANCE_INTENT, "controller successor maintenance intent"),
            "controller successor maintenance intent",
        ),
        label="controller successor maintenance intent", role="producer", trust=trust,
    )
    payload = intent["payload"]
    if set(payload) != {
        "action", "candidate_artifacts", "predecessor_successor",
        "predecessor_activation", "paused_crontab_sha256", "requested_authenticated_goals",
        "issued_at", "expires_at_epoch",
    }:
        raise ControllerError("controller successor maintenance payload is malformed")
    candidate = payload.get("candidate_artifacts")
    if candidate != {
        "controller_sha256": file_digest(Path(__file__)),
        "controller_test_sha256": file_digest(ROOT / "scripts/test_stage5_theorems_execution_cron_v2.py"),
        "migration_tool_sha256": file_digest(ROOT / "scripts/accept_stage5_theorem_controller_successor.py"),
        "checker_sha256": file_digest(CHECKER_PATH),
        "checker_test_sha256": file_digest(ROOT / "scripts/test_stage5_theorems_blueprint.py"),
        "item_checker_sha256": file_digest(ITEM_CHECKER_PATH),
        "item_checker_test_sha256": file_digest(ROOT / "scripts/test_stage5_theorem_item.py"),
    }:
        raise ControllerError("controller successor maintenance candidate differs")
    predecessor_path = Path(payload.get("predecessor_successor", {}).get("path", ""))
    predecessor_path = ROOT / _safe_relative(predecessor_path.as_posix())
    predecessor_raw = _regular(predecessor_path, "maintenance predecessor successor")
    predecessor = _verify_successor_signature(
        strict_json(predecessor_raw, "maintenance predecessor successor"),
        label="maintenance predecessor successor", role="master", trust=trust,
    )
    if payload["predecessor_successor"] != {
        "path": predecessor_path.relative_to(ROOT).as_posix(),
        "file_sha256": digest(predecessor_raw),
        "authority_sha256": predecessor["authority_sha256"],
    }:
        raise ControllerError("controller successor maintenance predecessor differs")
    activation_raw = _regular(ACTIVATION_RECEIPT, "maintenance predecessor activation")
    activation = verify_seal(strict_json(activation_raw, "maintenance predecessor activation"), "maintenance predecessor activation")
    if payload["predecessor_activation"] != {
        "path": ACTIVATION_RECEIPT.relative_to(ROOT).as_posix(),
        "file_sha256": digest(activation_raw),
        "authority_sha256": activation["authority_sha256"],
        "schema_version": "awesome-theorems/stage5-controller-activation/3.0",
    } or activation.get("controller_successor_acceptance_authority_sha256") != predecessor["authority_sha256"]:
        raise ControllerError("controller successor maintenance activation differs")
    crontab = read_crontab()
    expires = payload.get("expires_at_epoch")
    if (
        payload.get("action") != "paused_reconcile_fence_and_refill_only"
        or payload.get("requested_authenticated_goals") != 24
        or payload.get("paused_crontab_sha256") != digest(crontab.encode())
        or CRON_BEGIN in crontab or CRON_END in crontab
        or "# BEGIN HARNESSFS_COMMUNITY_EXECUTION_V1" not in crontab
        or not isinstance(expires, (int, float)) or isinstance(expires, bool)
        or not time.time() < expires <= time.time() + 1800
    ):
        raise ControllerError("controller successor maintenance scope/expiry differs")
    return intent


def maintenance_consumption_path(intent: dict[str, Any]) -> Path:
    authority = intent.get("authority_sha256")
    if not isinstance(authority, str) or re.fullmatch(r"[0-9a-f]{64}", authority) is None:
        raise ControllerError("controller successor maintenance authority is malformed")
    return CONTROLLER_SUCCESSOR_MAINTENANCE_CONSUMPTIONS / f"{authority}.json"


def consume_controller_successor_maintenance_intent(
    intent: dict[str, Any],
) -> dict[str, Any]:
    """Durably consume an intent before any reconcile/refill side effect."""
    target = maintenance_consumption_path(intent)
    intent_raw = _regular(
        CONTROLLER_SUCCESSOR_MAINTENANCE_INTENT,
        "controller successor maintenance intent",
    )
    value = seal({
        "schema_version": "awesome-theorems/stage5-controller-successor-maintenance-consumption/1.0",
        "program": PROGRAM,
        "intent_authority_sha256": intent["authority_sha256"],
        "intent_file_sha256": digest(intent_raw),
        "action": intent["payload"]["action"],
        "candidate_artifacts": intent["payload"]["candidate_artifacts"],
        "consumed_at": now(),
    })
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
    try:
        descriptor = os.open(
            target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o444,
        )
    except FileExistsError as exc:
        raise ControllerError("controller successor maintenance intent was already consumed") from exc
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        directory = os.open(target.parent, os.O_RDONLY | os.O_DIRECTORY)
        try: os.fsync(directory)
        finally: os.close(directory)
    except Exception:
        target.unlink(missing_ok=True)
        raise
    return value


def atomic_write(path: Path, raw: bytes, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        os.chmod(tmp, mode); os.replace(tmp, path)
        d = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try: os.fsync(d)
        finally: os.close(d)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)


def atomic_json(path: Path, value: Any, mode: int = 0o644) -> None:
    atomic_write(path, json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n", mode)


def checker() -> Any:
    spec = importlib.util.spec_from_file_location("stage5_theorem_v2_checker", CHECKER_PATH)
    if spec is None or spec.loader is None: raise ControllerError("checker unavailable")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
    return module


def claim_checker() -> Any:
    spec = importlib.util.spec_from_file_location("stage5_theorem_claim_validator", CLAIM_CHECKER_PATH)
    if spec is None or spec.loader is None: raise ControllerError("theorem claim validator unavailable")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
    return module


def item_checker() -> Any:
    spec = importlib.util.spec_from_file_location("stage5_theorem_target_validator", ITEM_CHECKER_PATH)
    if spec is None or spec.loader is None: raise ControllerError("theorem TARGET validator unavailable")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
    return module


def program_item_checker() -> Any:
    spec = importlib.util.spec_from_file_location(
        "stage5_theorem_program_item_validator", PROGRAM_ITEM_CHECKER_PATH,
    )
    if spec is None or spec.loader is None:
        raise ControllerError("theorem program-item validator unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_program() -> tuple[dict[str, Any], list[dict[str, Any]], bytes]:
    mod = checker(); specification, rows, raw = mod.parse_blueprint(); mod.validate_spec(specification)
    mod.validate_boot_data(specification, rows, raw)
    return specification, rows, raw


def dag_projection(
    rows: Sequence[dict[str, Any]], active_item_ids: set[str],
) -> dict[str, Any]:
    """Return the one dynamic DAG order/frontier shared by admission and status."""
    by_id = {row["item_id"]: row for row in rows}
    if len(by_id) != len(rows):
        raise ControllerError("DAG projection contains duplicate item IDs")
    children: dict[str, set[str]] = {item_id: set() for item_id in by_id}
    for row in rows:
        for dependency in row["dependencies"]:
            if dependency not in by_id:
                raise ControllerError(f"DAG projection dependency is absent: {dependency}")
            children[dependency].add(row["item_id"])

    layer_cache: dict[str, int] = {}
    visiting: set[str] = set()

    def layer(item_id: str) -> int:
        if item_id in layer_cache:
            return layer_cache[item_id]
        if item_id in visiting:
            raise ControllerError(f"DAG projection cycle at {item_id}")
        visiting.add(item_id)
        row = by_id[item_id]
        value = 0 if row["state"] == "x" else 1 + max(
            (layer(dependency) for dependency in row["dependencies"]), default=0,
        )
        visiting.remove(item_id)
        layer_cache[item_id] = value
        return value

    descendant_cache: dict[str, set[str]] = {}

    def unfinished_descendants(item_id: str) -> set[str]:
        if item_id not in descendant_cache:
            result: set[str] = set()
            for child in children[item_id]:
                if by_id[child]["state"] != "x":
                    result.add(child)
                result.update(unfinished_descendants(child))
            descendant_cache[item_id] = result
        return descendant_cache[item_id]

    def priority(row: dict[str, Any]) -> tuple[int, int, int, str]:
        item_id = row["item_id"]
        direct = sum(by_id[child]["state"] != "x" for child in children[item_id])
        return (layer(item_id), -direct, -len(unfinished_descendants(item_id)), item_id)

    accepted = sorted((row for row in rows if row["state"] == "x"), key=priority)
    active = sorted(
        (row for row in rows if row["item_id"] in active_item_ids and row["state"] != "x"),
        key=priority,
    )
    remaining = sorted(
        (row for row in rows if row["state"] != "x" and row["item_id"] not in active_item_ids),
        key=priority,
    )
    frontier = [
        row for row in remaining
        if all(by_id[dependency]["state"] == "x" for dependency in row["dependencies"])
    ]
    return {
        "ordered_ids": [row["item_id"] for row in (*accepted, *active, *remaining)],
        "accepted_ids": [row["item_id"] for row in accepted],
        "active_ids": [row["item_id"] for row in active],
        "remaining_ids": [row["item_id"] for row in remaining],
        "dependency_clear_frontier": [row["item_id"] for row in frontier],
        "layers": {item_id: layer(item_id) for item_id in by_id},
        "priorities": {row["item_id"]: list(priority(row)) for row in rows},
    }


def claimable_item_ids(
    specification: dict[str, Any], rows: Sequence[dict[str, Any]],
) -> set[str]:
    """Derive claimability only from explicit frozen item-mode transport policy."""
    patterns: list[re.Pattern[str]] = []
    for mode in specification.get("item_modes", []):
        if mode.get("execution_class") == "codex_tui_claim":
            patterns.append(re.compile(mode["id_regex"]))
    return {
        row["item_id"] for row in rows
        if any(pattern.fullmatch(row["item_id"]) for pattern in patterns)
    }


def paths_conflict(left: Sequence[str], right: Sequence[str]) -> bool:
    """Return whether two exact ownership sets overlap by path or prefix."""
    left_paths = [PurePosixPath(value) for value in left]
    right_paths = [PurePosixPath(value) for value in right]
    return any(
        a == b or a in b.parents or b in a.parents
        for a in left_paths for b in right_paths
    )


def concurrency_usage(
    state: dict[str, Any], prompt: dict[str, Any],
    *, lease_usage: dict[str, int] | None = None,
) -> dict[str, int]:
    """Count each independent concurrency dimension from its own evidence."""
    active = [
        record for record in state.get("claims", {}).values()
        if record.get("status") in ACTIVE_GENERATION_STATUSES
    ]
    lease_usage = request_lease_usage(prompt, state) if lease_usage is None else lease_usage
    return {
        "logical_claims": len({record.get("lane_id") for record in active}),
        "agent_executions": len(active),
        "startup_reservations": sum(
            record.get("status") in STARTING_GENERATION_STATUSES for record in active
        ),
        "live_transports": sum(
            record.get("status") in TRANSPORT_GENERATION_STATUSES for record in active
        ),
        "authenticated_goals": sum(record.get("status") == "live" for record in active),
        "running_turns": lease_usage["running_turns"],
        "outbound_request_starts_per_window": lease_usage["request_starts_per_window"],
        "in_flight_requests": lease_usage["in_flight_requests"],
        "integration": state.get("active_integrations", 0),
        "validators": state.get("active_validators", 0),
        "exact_path_conflicts": state.get("active_exact_path_conflicts", 0),
    }


def admission_availability(
    state: dict[str, Any], prompt: dict[str, Any],
    *, lease_usage: dict[str, int] | None = None,
) -> tuple[int, dict[str, int], list[str]]:
    """Compute a launch ceiling without collapsing independent dimensions."""
    vector = prompt["concurrency"]
    usage = concurrency_usage(state, prompt, lease_usage=lease_usage)
    capacity_dimensions = (
        "logical_claims", "agent_executions", "startup_reservations",
        "live_transports", "authenticated_goals", "running_turns",
        "outbound_request_starts_per_window", "in_flight_requests",
    )
    available = {key: int(vector[key]) - usage[key] for key in capacity_dimensions}
    slots = min(available.values(), default=0)
    reasons = [f"{key}_saturated" for key, amount in available.items() if amount <= 0]
    if int(vector["exact_path_conflicts"]) < usage["exact_path_conflicts"]:
        slots = 0
        reasons.append("exact_path_conflict_budget_exceeded")
    return max(0, slots), usage, reasons


def validate_claim_schema_prompt_identity() -> None:
    """Require the closed claim schema to carry the complete execution identity."""
    schema = strict_json(_regular(EVIDENCE / "claim-card.schema.json", "claim-card schema"), "claim-card schema")
    if not isinstance(schema, dict) or schema.get("additionalProperties") is not False:
        raise ControllerError("claim-card schema is not closed")
    required = schema.get("required")
    properties = schema.get("properties")
    identity = properties.get("execution_identity") if isinstance(properties, dict) else None
    if not isinstance(required, list) or "execution_identity" not in required or not isinstance(identity, dict):
        raise ControllerError("claim-card schema lacks prompt-bound execution identity")
    if (identity.get("type") != "object" or identity.get("additionalProperties") is not False
            or frozenset(identity.get("required", [])) != CLAIM_EXECUTION_IDENTITY_FIELDS
            or frozenset(identity.get("properties", {})) != CLAIM_EXECUTION_IDENTITY_FIELDS):
        raise ControllerError("claim-card execution identity schema differs")


def validate_concurrency_vector(vector: Any) -> dict[str, int | str]:
    """Validate every prompt-supplied dimension without inventing defaults."""
    if not isinstance(vector, dict) or frozenset(vector) != CONCURRENCY_DIMENSIONS:
        raise ControllerError("prompt must provide the complete concurrency vector")
    for key, item in vector.items():
        if item == "not_applicable":
            if key not in CONCURRENCY_NOT_APPLICABLE:
                raise ControllerError(f"prompt concurrency dimension {key} is applicable")
            continue
        if isinstance(item, bool) or not isinstance(item, int) or item < 0:
            raise ControllerError(f"prompt concurrency dimension {key} is invalid")
        if key in CONCURRENCY_POSITIVE and item == 0:
            raise ControllerError(f"prompt concurrency dimension {key} must be positive")
    if vector["service_records"] != "not_applicable":
        raise ControllerError("bounded lane pool requires service_records=not_applicable")
    if vector["exact_path_conflicts"] != 0:
        raise ControllerError("Blueprint exact ownership requires exact_path_conflicts=0")
    request_wave_caps = (
        "agent_executions", "startup_reservations", "live_transports",
        "authenticated_goals", "running_turns",
        "outbound_request_starts_per_window", "in_flight_requests",
    )
    fanout = vector["launch_fanout_per_wave"]
    if any(fanout > vector[key] for key in request_wave_caps):
        raise ControllerError("launch fanout exceeds an applicable execution/request cap")
    standing_caps = (
        "logical_claims", "agent_executions", "live_transports",
        "authenticated_goals", "running_turns",
    )
    if any(vector["authenticated_goals"] > vector[key] for key in standing_caps):
        raise ControllerError("authenticated goal target exceeds a standing cap")
    return dict(vector)


def validate_execution_policy(execution_limits: Any, recovery: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    """Validate explicit lifecycle/recovery policy supplied by the operator."""
    if not isinstance(execution_limits, dict) or frozenset(execution_limits) != EXECUTION_LIMIT_KEYS:
        raise ControllerError("prompt must provide the complete execution_limits object")
    if not isinstance(recovery, dict) or frozenset(recovery) != RECOVERY_KEYS:
        raise ControllerError("prompt must provide the complete recovery object")
    if execution_limits.get("generation_lifetime_seconds") != 1209600:
        raise ControllerError("goal lifetime must be exactly 14 days")
    if execution_limits.get("model_turns") != "unbounded":
        raise ControllerError("model_turns must explicitly be unbounded")
    for key in ("model_input_tokens", "model_output_tokens", "cpu_seconds", "external_launches"):
        value = execution_limits[key]
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ControllerError(f"execution limit {key} must be positive finite")
    ints = ("startup_attempts_per_generation", "repair_attempts_per_failure_identity",
            "generation_replacements_per_work_item",
            "backoff_initial_seconds", "backoff_max_seconds",
            "breaker_failure_threshold", "breaker_cooldown_seconds")
    for key in ints:
        value = recovery[key]
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ControllerError(f"recovery field {key} must be positive finite")
    if recovery["generation_replacements_per_work_item"] != 60:
        raise ControllerError("generation replacement cap must be exactly 60")
    if recovery["backoff_initial_seconds"] != 60 or recovery["backoff_max_seconds"] != 3600 or recovery["backoff_multiplier"] != 2:
        raise ControllerError("backoff policy must be 60/120/240... capped at 3600")
    jitter = recovery["backoff_jitter_ratio"]
    if isinstance(jitter, bool) or not isinstance(jitter, (int, float)) or not 0 <= jitter <= 0.2:
        raise ControllerError("backoff jitter ratio must be within [0,0.2]")
    if recovery["provider_attempts_per_request"] != 60:
        raise ControllerError("provider attempts must be exactly 60")
    if recovery["retry_after_precedence"] not in {"provider_retry_after_then_exponential", "provider_retry_after_then_exponential_jitter", "exponential_only"}:
        raise ControllerError("retry_after_precedence is invalid")
    if recovery["breaker_scope"] != "provider" or set(recovery["breaker_failure_classes"]) != {"http_429", "http_503", "provider_unavailable"}:
        raise ControllerError("provider breaker scope/failure classes differ")
    if recovery["breaker_failure_threshold"] != 3 or recovery["breaker_cooldown_seconds"] != 1800:
        raise ControllerError("provider breaker must be 3 failures and 1800 seconds")
    return dict(execution_limits), dict(recovery)

def backoff_delay(recovery: dict[str, Any], failures: int, jitter_factor: float = 1.0) -> float:
    """Compute capped exponential delay; jitter_factor is persisted per attempt."""
    base = min(recovery["backoff_max_seconds"], recovery["backoff_initial_seconds"] * (recovery["backoff_multiplier"] ** max(0, failures - 1)))
    ratio = recovery["backoff_jitter_ratio"]
    if not (1 - ratio <= jitter_factor <= 1 + ratio):
        raise ControllerError("jitter factor outside prompt-bound range")
    return min(recovery["backoff_max_seconds"], base * jitter_factor)

def provider_breaker_is_open(state: dict[str, Any], at_epoch: float | None = None) -> bool:
    breaker = state.get("breaker", {})
    if breaker.get("state") != "open":
        return False
    until = breaker.get("cooldown_until")
    if isinstance(until, (int, float)) and (time.time() if at_epoch is None else at_epoch) >= until:
        # Cooldown expiry enters a real half-open state.  Goal registration is
        # not provider recovery evidence: only a prompt-sized probe wave and a
        # task-local response.completed signal may close the breaker.
        changed_at = time.time() if at_epoch is None else at_epoch
        state["breaker"] = {
            **breaker, "provider": PROVIDER, "state": "half_open",
            "consecutive_failures": 0, "cooldown_until": None,
            "half_open_started_at": changed_at, "probe_generation_ids": [],
            "state_changed_at": changed_at, "state_change_reason": "cooldown_elapsed",
        }
        return False
    return True


def provider_response_completed_at(record: dict[str, Any]) -> float | None:
    """Latest genuine model response completion in this private generation."""
    path = Path(str(record.get("codex_home", ""))) / "logs_2.sqlite"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        rows = connection.execute(
            "select ts,feedback_log_body from logs "
            "where target='codex_api::sse::responses' and "
            "instr(coalesce(feedback_log_body,''), 'SSE event: {\"type\":\"response.completed\"') = 1 "
            "order by ts desc limit 64"
        ).fetchall()
        connection.close()
        for ts, body in rows:
            try:
                event = json.loads(str(body).removeprefix("SSE event: "))
            except json.JSONDecodeError:
                continue
            response = event.get("response") if isinstance(event, dict) else None
            if (
                event.get("type") == "response.completed"
                and isinstance(response, dict)
                and response.get("status") == "completed"
                and response.get("error") is None
                and response.get("incomplete_details") is None
            ):
                return float(ts)
        return None
    except (sqlite3.Error, ValueError, TypeError):
        return None


def provider_failure_completed_at(record: dict[str, Any]) -> float | None:
    """Read an exact 429/503 completion time from the private turn registry."""
    path = Path(str(record.get("codex_home", ""))) / "thread_history_1.sqlite"
    if not path.is_file() or path.is_symlink():
        return None
    try:
        connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        rows = connection.execute(
            "select completed_at,error_json from thread_turns "
            "where status='failed' and completed_at is not null order by completed_at desc"
        ).fetchall()
        connection.close()
        for completed_at, raw in rows:
            try:
                error = json.loads(raw)
            except (TypeError, json.JSONDecodeError):
                continue
            info = error.get("codexErrorInfo") if isinstance(error, dict) else None
            attempts = info.get("responseTooManyFailedAttempts") if isinstance(info, dict) else None
            status_code = attempts.get("httpStatusCode") if isinstance(attempts, dict) else None
            message = str(error.get("message", "")).lower() if isinstance(error, dict) else ""
            if status_code in {429, 503} or "too many requests" in message or "provider unavailable" in message:
                return float(completed_at)
        return None
    except (sqlite3.Error, ValueError, TypeError):
        return None


def provider_signal(record: dict[str, Any], fallback_at: float | None = None) -> tuple[float, str] | None:
    """Latest structured provider outcome; failure wins an exact-time tie."""
    success_at = provider_response_completed_at(record)
    failure_at = provider_failure_completed_at(record)
    if failure_at is None and _provider_failure(record):
        recorded = record.get("provider_failure_at", record.get("retired_epoch"))
        failure_at = float(recorded) if isinstance(recorded, (int, float)) and not isinstance(recorded, bool) else (time.time() if fallback_at is None else fallback_at)
    candidates = [
        (at, kind) for at, kind in ((success_at, "success"), (failure_at, "failure"))
        if isinstance(at, (int, float)) and not isinstance(at, bool)
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda value: (value[0], value[1] == "failure"))


def gate_pre_submission_generations_for_breaker(state: dict[str, Any], breaker_open: bool) -> int:
    """Retire transports that have not crossed the one-way `/goal` boundary."""
    if not breaker_open:
        return 0
    gated = 0
    for record in state.get("claims", {}).values():
        if record.get("status") in {"reserved", "materialized", "tmux_started", "goal_pasted"}:
            record["status"] = "generation_retire_required"
            record["terminal_reason"] = "provider_breaker_open"
            record["retired_reason"] = "provider_breaker_open_before_goal_submission"
            gated += 1
    return gated


def refresh_half_open_probe_set(state: dict[str, Any]) -> bool:
    """Release an inconclusive probe set only after every generation is terminal."""
    breaker = state.get("breaker", {})
    if breaker.get("state") != "half_open" or not breaker.get("probe_generation_ids"):
        return False
    records_by_generation = {
        str(record.get("generation_id") or record.get("run_id")): record
        for record in (
            *[row for row in state.get("generation_history", []) if isinstance(row, dict)],
            *[row for row in state.get("claims", {}).values() if isinstance(row, dict)],
        )
        if isinstance(record.get("generation_id") or record.get("run_id"), str)
    }
    probes = [records_by_generation.get(str(generation_id)) for generation_id in breaker["probe_generation_ids"]]
    if any(record is not None and record.get("status") in ACTIVE_GENERATION_STATUSES for record in probes):
        return False
    breaker["probe_generation_ids"] = []
    breaker["last_inconclusive_probe_retired_at"] = time.time()
    breaker["inconclusive_probe_waves"] = int(breaker.get("inconclusive_probe_waves", 0)) + 1
    state["breaker"] = breaker
    return True

def _provider_failure(record: dict[str, Any]) -> bool:
    return record.get("terminal_reason") in {"provider_unavailable", "provider_rate_limited"}


def _generation_records_for_item(state: dict[str, Any], item_id: str) -> list[dict[str, Any]]:
    """Distinct item generations in durable creation order."""
    candidates = [
        row for row in state.get("generation_history", [])
        if isinstance(row, dict) and row.get("item_id") == item_id
    ]
    current = state.get("claims", {}).get(item_id)
    if isinstance(current, dict):
        candidates.append(current)
    result: list[dict[str, Any]] = []
    positions: dict[str, int] = {}
    for record in candidates:
        generation_id = record.get("generation_id") or record.get("run_id")
        if not isinstance(generation_id, str):
            continue
        if generation_id in positions:
            result[positions[generation_id]] = record
        else:
            positions[generation_id] = len(result)
            result.append(record)
    return result


def _replacement_eligible(record: dict[str, Any]) -> bool:
    """Count only generations that crossed the submitted `/goal` boundary.

    A TUI startup can fail before the goal is pasted/submitted (for example
    while the trust selector is still rendering).  Such a launch consumes no
    theorem replacement: counting it would spend the mathematical retry cap
    on transport startup noise.  Legacy records without the field are retained
    conservatively as eligible; all v2 materialized records carry the field.
    """
    submissions = record.get("goal_submissions")
    # Unknown legacy records and malformed nonzero records count
    # conservatively.  Only an explicit zero proves that no worker goal was
    # submitted and therefore no theorem replacement was consumed.
    return submissions is None or submissions != 0


def provider_failure_streak_for_item(
    state: dict[str, Any], item_id: str, generation_id: str,
) -> int:
    records = _generation_records_for_item(state, item_id)
    target = next((index for index, row in enumerate(records)
                   if (row.get("generation_id") or row.get("run_id")) == generation_id), None)
    if target is None:
        return 1
    streak = 0
    for record in reversed(records[:target + 1]):
        if not _provider_failure(record):
            break
        streak += 1
    return max(1, streak)


def deterministic_retry_jitter(record: dict[str, Any], recovery: dict[str, Any]) -> float:
    seed = int(digest(str(record.get("run_id", "")).encode())[:8], 16) / 0xFFFFFFFF
    ratio = float(recovery.get("backoff_jitter_ratio", 0.2))
    return 1 - ratio + 2 * ratio * seed


def rebuild_provider_retry_schedule(state: dict[str, Any]) -> int:
    """Normalize retry due times to per-item consecutive provider failures."""
    records = [row for row in state.get("generation_history", []) if isinstance(row, dict)]
    records.extend(row for row in state.get("claims", {}).values() if isinstance(row, dict))
    changed = 0
    for record in records:
        if not _provider_failure(record):
            continue
        recovery = record.get("recovery")
        item_id = record.get("item_id")
        generation_id = record.get("generation_id") or record.get("run_id")
        base_epoch = record.get("provider_failure_at", record.get("retired_epoch"))
        if (not isinstance(recovery, dict) or not isinstance(item_id, str)
                or not isinstance(generation_id, str)
                or not isinstance(base_epoch, (int, float)) or isinstance(base_epoch, bool)):
            continue
        streak = provider_failure_streak_for_item(state, item_id, generation_id)
        due = float(base_epoch) + backoff_delay(
            recovery, streak, deterministic_retry_jitter(record, recovery),
        )
        if record.get("provider_failure_streak") != streak or record.get("next_retry_at") != due:
            record["provider_failure_streak"] = streak
            record["next_retry_at"] = due
            changed += 1
    return changed


def update_provider_breaker(
    state: dict[str, Any], record: dict[str, Any], signal: tuple[float, str] | None = None,
) -> None:
    """Persist route-level 429/503 breaker transitions from terminal evidence."""
    signal = signal or provider_signal(record)
    if signal is None:
        return
    signal_at, signal_kind = signal
    if (record.get("breaker_counted_signal_at") == signal_at
            and record.get("breaker_counted_signal_kind") == signal_kind):
        return
    if (record.get("breaker_counted_run_id") == record.get("run_id")
            and record.get("breaker_counted_signal_at") is None and signal_kind == "failure"):
        return
    if signal_kind == "success":
        breaker = state.get("breaker", {})
        if breaker.get("state") == "open":
            return
        needs_signal = breaker.get("state") == "half_open" or int(breaker.get("consecutive_failures", 0)) > 0
        if not needs_signal:
            return
        if breaker.get("state") == "half_open":
            probes = set(breaker.get("probe_generation_ids", []))
            generation_id = record.get("generation_id") or record.get("run_id")
            if generation_id not in probes:
                return
        success_at = signal_at
        if success_at <= float(breaker.get("last_signal_at", 0)):
            return
        if (breaker.get("state") == "half_open"
                and success_at < int(float(breaker.get("half_open_started_at", 0)))):
            return
        last_failure = breaker.get("last_failure_at")
        if (
            breaker.get("state") == "half_open"
            or (int(breaker.get("consecutive_failures", 0)) > 0
                and isinstance(last_failure, (int, float)) and success_at > last_failure)
        ):
            state["breaker"] = {
                "provider": PROVIDER, "state": "closed", "consecutive_failures": 0,
                "opened_at": None, "cooldown_until": None,
                "closed_at": success_at, "closed_reason": "provider_response_completed",
                "last_signal_at": success_at,
            }
            record["provider_success_observed_at"] = success_at
            record["breaker_counted_signal_at"] = signal_at
            record["breaker_counted_signal_kind"] = signal_kind
        return
    recovery = record.get("recovery")
    if not isinstance(recovery, dict):
        return
    breaker = dict(state.get("breaker", {"provider": PROVIDER, "state": "closed", "consecutive_failures": 0, "opened_at": None, "cooldown_until": None}))
    breaker["provider"] = PROVIDER
    breaker["consecutive_failures"] = int(breaker.get("consecutive_failures", 0)) + 1
    if record.get("terminal_reason") not in {"provider_unavailable", "provider_rate_limited"}:
        record["terminal_reason"] = "provider_unavailable"
        record["retired_reason"] = "structured_provider_failure"
        if record.get("status") in ACTIVE_GENERATION_STATUSES:
            record["status"] = "generation_retire_required"
    breaker["last_failure_class"] = record.get("terminal_reason")
    failure_at = signal_at
    last_signal = breaker.get("last_signal_at")
    if (breaker.get("closed_reason") == "provider_response_completed"
            and isinstance(last_signal, (int, float)) and failure_at < last_signal):
        record["breaker_counted_run_id"] = record.get("run_id")
        record["breaker_counted_signal_at"] = signal_at
        record["breaker_counted_signal_kind"] = signal_kind
        return
    breaker["last_signal_at"] = max(float(last_signal or 0), failure_at)
    breaker["last_failure_at"] = failure_at
    if (breaker["consecutive_failures"] >= recovery["breaker_failure_threshold"]
            and breaker.get("state") != "open"):
        breaker["state"] = "open"
        breaker["opened_at"] = failure_at
        breaker["cooldown_until"] = failure_at + recovery["breaker_cooldown_seconds"]
    state["breaker"] = breaker
    record["breaker_counted_run_id"] = record.get("run_id")
    record["breaker_counted_signal_at"] = signal_at
    record["breaker_counted_signal_kind"] = signal_kind
    record["provider_failure_at"] = failure_at
    item_id = str(record.get("item_id", ""))
    generation_id = str(record.get("generation_id") or record.get("run_id") or "")
    streak = provider_failure_streak_for_item(state, item_id, generation_id)
    record["provider_failure_streak"] = streak
    record["next_retry_at"] = failure_at + backoff_delay(
        recovery, streak, deterministic_retry_jitter(record, recovery),
    )


def update_provider_breaker_from_records(state: dict[str, Any], records: Sequence[dict[str, Any]]) -> int:
    """Apply provider outcomes in their durable completion order."""
    observed_at = time.time()
    signals: list[tuple[float, bool, str, dict[str, Any], tuple[float, str]]] = []
    for record in records:
        signal = provider_signal(record, observed_at)
        if signal is None:
            continue
        signals.append((
            signal[0], signal[1] == "failure",
            str(record.get("generation_id") or record.get("run_id") or ""),
            record, signal,
        ))
    for _, _, _, record, signal in sorted(signals, key=lambda value: value[:3]):
        update_provider_breaker(state, record, signal)
    return len(signals)

def generation_ids_for_item(state: dict[str, Any], item_id: str) -> list[str]:
    """Return distinct generations in durable creation order for one item.

    A retired generation is deliberately retained both in ``generation_history``
    and, until superseded, in ``claims``.  Counting rows therefore double-counts
    exactly the failure case that consumes the replacement budget.  Generation
    identity, not global scheduler position, is the unit of this ledger.
    """
    return [
        str(record.get("generation_id") or record.get("run_id"))
        for record in _generation_records_for_item(state, item_id)
        if _replacement_eligible(record)
    ]


def replacement_count_for_item(state: dict[str, Any], item_id: str) -> int:
    """Number of replacements already created (the initial generation is 0)."""
    return max(0, len(generation_ids_for_item(state, item_id)) - 1)


def replacement_admissible(state: dict[str, Any], item_id: str, cap: int) -> bool:
    """Whether another generation would stay within the replacement cap."""
    return replacement_count_for_item(state, item_id) < cap


def next_replacement_ordinal(state: dict[str, Any], item_id: str) -> int:
    """Ordinal for the next generation: initial=0, replacements=1..cap."""
    return len(generation_ids_for_item(state, item_id))


def previous_generation_id_for_item(state: dict[str, Any], item_id: str) -> str | None:
    generations = generation_ids_for_item(state, item_id)
    return generations[-1] if generations else None


def pre_goal_replacement_ordinal_violation(
    state: dict[str, Any], record: dict[str, Any],
) -> str | None:
    """Fence an old pre-goal reservation whose ordinal spent startup noise.

    The replacement ordinal is reserved before the TUI starts, but a worker
    generation exists only after its one `/goal` is submitted.  Earlier
    controller bytes could abandon multiple trust-selector startups and then
    assign a later pre-goal reservation a correspondingly inflated ordinal.
    Retiring that unsubmitted reservation lets the next immutable claim use the
    exact submitted-generation count without rewriting any historical record.
    """
    if (
        record.get("status") not in {
            "reserved", "materialized", "tmux_started", "goal_pasted",
        }
        or record.get("goal_submissions") != 0
    ):
        return None
    expected = next_replacement_ordinal(state, str(record.get("item_id", "")))
    return (
        None if record.get("replacement_ordinal") == expected
        else "pre_goal_replacement_ordinal_spent_by_startup_noise"
    )


def next_retry_at_for_item(state: dict[str, Any], item_id: str) -> float | None:
    records = _generation_records_for_item(state, item_id)
    if not records:
        return None
    # A successful/non-provider successor resets the per-item streak.  An old
    # generation's future timestamp must never block that newer generation.
    latest = records[-1]
    if not _provider_failure(latest):
        return None
    due = latest.get("next_retry_at")
    return float(due) if isinstance(due, (int, float)) and not isinstance(due, bool) else None


def successor_generation_violation(
    record: dict[str, Any], prompt: dict[str, Any], prompt_digest: str,
) -> str | None:
    """Explain why an active generation cannot remain in the successor set."""
    # An admitted generation keeps its immutable prompt/spec baseline.  A new
    # prompt digest is a successor admission boundary, not permission to kill
    # an otherwise valid same-route generation in place.
    if record.get("status") == "live" and record.get("service_tier") != SERVICE_TIER:
        return "successor_route_migration"
    claim_path = Path(str(record.get("task_root", ""))) / "claim.json"
    if record.get("status") in {"reserved"}:
        return None
    try:
        card = strict_json(_regular(claim_path, "active claim card"), "active claim card")
        recovery = card["execution_policy"]["recovery"]
        cap = recovery["generation_replacements_per_work_item"]
        lineage = card["generation_lineage"]
        retry = card["retry_budget"]
        bootstrap = {
            row.get("path"): row
            for row in card.get("read_only_bootstrap_files", [])
            if isinstance(row, dict) and isinstance(row.get("path"), str)
        }
        replacement_ordinal = lineage["replacement_ordinal"]
        if (
            not isinstance(replacement_ordinal, int)
            or isinstance(replacement_ordinal, bool)
            or not 0 <= replacement_ordinal <= cap
            or lineage["replacement_cap"] != cap
            or retry["attempt"] != replacement_ordinal + 1
            or retry["max_attempts"] != cap + 1
            or retry["attempt"] > retry["max_attempts"]
            or (replacement_ordinal == 0) != (lineage["previous_generation_id"] is None)
            or record.get("replacement_ordinal") != replacement_ordinal
        ):
            return "invalid_per_item_generation_lineage"
        baseline_item_checker = (
            Path(str(record.get("task_root", "")))
            / "work/_baseline/check_stage5_theorem_item.py"
        )
        if (
            bootstrap.get("_baseline/check_stage5_theorem_item.py", {}).get("sha256")
            != file_digest(ITEM_CHECKER_PATH)
            or file_digest(baseline_item_checker) != file_digest(ITEM_CHECKER_PATH)
        ):
            return "stale_item_validator_sha256"
    except (ControllerError, KeyError, TypeError, ValueError, OSError):
        return "invalid_per_item_generation_lineage"
    return None


def load_concurrency_prompt(path: Path, specification: dict[str, Any]) -> tuple[dict[str, Any], str]:
    raw = _regular(path, "concurrency prompt")
    value = strict_json(raw, "concurrency prompt")
    if not isinstance(value, dict) or value.get("schema_version") != CONCURRENCY_SCHEMA or value.get("program") != PROGRAM:
        raise ControllerError("explicit concurrency prompt schema/program differs")
    if frozenset(value) != CONCURRENCY_PROMPT_KEYS:
        raise ControllerError("explicit concurrency prompt fields differ")
    body = dict(value); authority = body.pop("authority_sha256", None)
    if not isinstance(authority, str) or digest(canonical(body)) != authority:
        raise ControllerError("explicit concurrency prompt seal differs")
    validate_concurrency_vector(value.get("concurrency"))
    validate_execution_policy(value.get("execution_limits"), value.get("recovery"))
    epoch = value.get("policy_epoch")
    if not isinstance(epoch, str) or re.fullmatch(r"stage5-concurrency-prompt-[0-9]{4}-[0-9]{2}-[0-9]{2}(?:-[a-z0-9-]+)?", epoch) is None:
        raise ControllerError("concurrency prompt policy epoch is malformed")
    if value.get("execution_spec_sha256") != digest(canonical(specification)):
        raise ControllerError("stale concurrency prompt specification digest")
    if (value.get("operator_goal_thread_id") != GOAL_THREAD_ID
            or value.get("operator_goal_objective_sha256") != GOAL_OBJECTIVE_SHA256):
        raise ControllerError("concurrency prompt goal binding differs")
    if value.get("operator_identity") != f"codex-user-goal:{GOAL_THREAD_ID}":
        raise ControllerError("concurrency prompt operator identity differs")
    window = value.get("request_window_seconds")
    if isinstance(window, bool) or not isinstance(window, int) or window <= 0:
        raise ControllerError("concurrency prompt request window is invalid")
    return value, digest(raw)


def active_operator_goal() -> dict[str, Any]:
    """Read the exact root-user goal binding before any worker admission."""
    if not GOALS_DB.is_file() or GOALS_DB.is_symlink():
        raise ControllerError("operator goal registry is unavailable")
    try:
        connection = sqlite3.connect(f"file:{GOALS_DB}?mode=ro", uri=True, timeout=2)
        row = connection.execute(
            "select goal_id,objective,status,token_budget,tokens_used,created_at_ms,updated_at_ms "
            "from thread_goals where thread_id=?", (GOAL_THREAD_ID,),
        ).fetchone()
        connection.close()
    except sqlite3.Error as exc:
        raise ControllerError("operator goal registry query failed") from exc
    if row is None or row[2] != "active" or digest(row[1].encode("utf-8")) != GOAL_OBJECTIVE_SHA256:
        raise ControllerError("exact operator goal is absent, inactive, or changed")
    return {
        "thread_id": GOAL_THREAD_ID, "goal_id": row[0], "status": row[2],
        "objective_sha256": GOAL_OBJECTIVE_SHA256, "token_budget": row[3],
        "tokens_used": row[4], "created_at_ms": row[5], "updated_at_ms": row[6],
    }


def validate_operator_authority(
    specification: dict[str, Any], prompt: dict[str, Any], prompt_digest: str,
) -> dict[str, Any]:
    """Fail closed unless the durable budget and live goal match this spec."""
    trust = json.loads(_regular(OPERATOR_TRUST_ROOT, "operator trust root"))
    expected_trust = {
        "schema_version": "awesome-theorems/stage5-operator-goal-trust-root/1.0",
        "authority_mode": "local_codex_active_goal_registry_binding",
        "operator_identity": f"codex-user-goal:{GOAL_THREAD_ID}",
        "thread_id": GOAL_THREAD_ID, "objective_sha256": GOAL_OBJECTIVE_SHA256,
        "verification": "controller requires the exact active local Codex goal thread/objective/status before activation and each launch; this is a pinned local operator instruction binding, not a cryptographic signature or price attestation",
        "renewal": "requires a new explicit user instruction and reviewed authority migration",
    }
    if trust != expected_trust or digest(canonical(trust)) != OPERATOR_TRUST_ROOT_SHA256:
        raise ControllerError("operator trust-root bytes differ")
    authority = verify_seal(json.loads(_regular(OPERATOR_AUTHORITY, "operator budget authority")), "operator budget authority")
    authority_sha256 = authority.get("authority_sha256")
    if not isinstance(authority_sha256, str) or digest(canonical({k: v for k, v in authority.items() if k != "authority_sha256"})) != authority_sha256:
        raise ControllerError("operator budget authority seal differs")
    if authority.get("goal_thread_id") != GOAL_THREAD_ID or authority.get("goal_objective_sha256") != GOAL_OBJECTIVE_SHA256 or authority.get("trust_root_sha256") != OPERATOR_TRUST_ROOT_SHA256:
        raise ControllerError("operator budget goal/trust binding differs")
    expected_route = {"provider": PROVIDER, "model": MODEL, "reasoning_effort": EFFORT, "service_tier": SERVICE_TIER, "monetary_price": "unknown_not_zero"}
    if authority.get("billing_binding") != expected_route:
        raise ControllerError("operator budget route/billing binding differs")
    allowance = authority.get("program_allowances", {}).get(PROGRAM)
    if not isinstance(allowance, dict):
        raise ControllerError("theorem program allowance is absent")
    required = ("model_input_tokens", "model_output_tokens", "external_launches", "wall_seconds", "cpu_seconds")
    if any(not isinstance(allowance.get(key), int) or isinstance(allowance.get(key), bool) or allowance[key] <= 0 for key in required):
        raise ControllerError("operator allowance is not positive finite")
    if allowance.get("model_turns") not in ("unbounded", None):
        raise ControllerError("operator model_turns allowance must be explicitly unbounded")
    if allowance.get("worker_launch_authorized") is not True:
        raise ControllerError("operator authority does not authorize worker launch")
    vector = prompt["concurrency"]
    if (authority.get("concurrency_prompt_sha256") != prompt_digest
            or authority.get("concurrency_prompt_epoch") != prompt.get("policy_epoch")
            or authority.get("resolved_concurrency") != vector):
        raise ControllerError("operator authority concurrency binding differs")
    combined = authority.get("combined_allowances", {})
    if (not isinstance(combined.get("authenticated_live_goals"), int)
            or combined["authenticated_live_goals"] < vector["authenticated_goals"]):
        raise ControllerError("operator live-goal allowance is below the prompt target")
    renewal = verify_seal(
        strict_json(
            _regular(OPERATOR_BUDGET_RENEWAL, "operator budget renewal"),
            "operator budget renewal",
        ),
        "operator budget renewal",
    )
    maxima = authority.get("per_claim_maxima")
    claimable_items = 3574
    generation_limit = claimable_items * 61
    if (
        renewal.get("schema_version")
        != "awesome-theorems/stage5-operator-budget-renewal/2.0"
        or renewal.get("program") != PROGRAM
        or renewal.get("predecessor_authority_sha256") != authority_sha256
        or renewal.get("goal_thread_id") != GOAL_THREAD_ID
        or renewal.get("goal_objective_sha256") != GOAL_OBJECTIVE_SHA256
        or renewal.get("trust_root_sha256") != OPERATOR_TRUST_ROOT_SHA256
        or renewal.get("execution_spec_sha256") != digest(canonical(specification))
        or renewal.get("concurrency_prompt_sha256") != prompt_digest
        or renewal.get("concurrency_prompt_epoch") != prompt.get("policy_epoch")
        or renewal.get("billing_binding") != expected_route
        or renewal.get("claimable_item_count") != claimable_items
        or renewal.get("generation_limit") != generation_limit
        or renewal.get("per_claim_maxima") != maxima
        or renewal.get("authorization_basis")
        != "explicit active root goal requests complete Blueprint execution with one initial generation plus at most sixty replacements per work item"
    ):
        raise ControllerError("operator budget renewal binding differs")
    additive = renewal.get("additive_allowances")
    effective = renewal.get("effective_allowances")
    if not isinstance(additive, dict) or not isinstance(effective, dict):
        raise ControllerError("operator budget renewal allowances are malformed")
    expected_effective = {
        key: generation_limit * maxima[key] for key in required
    }
    expected_additive = {
        key: expected_effective[key] - allowance[key] for key in required
    }
    if effective != expected_effective or additive != expected_additive:
        raise ControllerError("operator budget renewal is not the exact finite worst-case envelope")
    if any(not isinstance(value, int) or isinstance(value, bool) or value <= 0
           for value in additive.values()):
        raise ControllerError("operator budget renewal is not positive finite")
    goal = active_operator_goal()
    return {
        "authority": authority,
        "renewal": renewal,
        "effective_allowances": expected_effective,
        "authority_chain_sha256": digest(canonical([
            authority_sha256, renewal["authority_sha256"],
        ])),
        "goal": goal,
    }


def materialize_runtime_authority(
    binding: dict[str, Any], specification: dict[str, Any],
    prompt: dict[str, Any], prompt_digest: str,
) -> None:
    """Persist a read-only, spec-bound runtime copy for restart auditing."""
    target = RUNTIME / "config/operator-budget.resolved.json"
    body = {
        "schema_version": "awesome-theorems/stage5-runtime-operator-budget/1.0",
        "program": PROGRAM,
        "execution_spec_sha256": digest(canonical(specification)),
        "authority_sha256": binding["authority"]["authority_sha256"],
        "renewal_authority_sha256": binding["renewal"]["authority_sha256"],
        "authority_chain_sha256": binding["authority_chain_sha256"],
        "effective_allowances": binding["effective_allowances"],
        "operator_goal": binding["goal"],
        "concurrency_prompt_sha256": prompt_digest,
        "concurrency_prompt_epoch": prompt["policy_epoch"],
        "resolved_concurrency": prompt["concurrency"],
        "route": {"provider": PROVIDER, "model": MODEL, "reasoning_effort": EFFORT, "service_tier": SERVICE_TIER},
        "materialized_at": now(),
    }
    atomic_json(target, seal(body), 0o444)


def _budget_record_raw(value: dict[str, Any]) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode() + b"\n"


def _read_budget_ledger() -> list[dict[str, Any]]:
    if not BUDGET_LEDGER.exists():
        return []
    if BUDGET_LEDGER.is_symlink() or not BUDGET_LEDGER.is_file():
        raise ControllerError("operator budget ledger is not a regular file")
    rows: list[dict[str, Any]] = []
    previous: str | None = None
    for number, line in enumerate(BUDGET_LEDGER.read_bytes().splitlines(), 1):
        if not line:
            continue
        row = verify_seal(strict_json(line, f"operator budget ledger line {number}"), f"operator budget ledger line {number}")
        if (
            row.get("schema_version") != "awesome-theorems/stage5-operator-budget-ledger/2.0"
            or row.get("program") != PROGRAM
            or row.get("seq") != len(rows) + 1
            or row.get("previous_record_sha256") != previous
            or row.get("kind") not in {"legacy_import", "reservation", "settlement"}
        ):
            raise ControllerError("operator budget ledger chain differs")
        previous = digest(line)
        rows.append(row)
    return rows


def _append_budget_record(
    state: dict[str, Any], kind: str, payload: dict[str, Any],
) -> dict[str, Any]:
    accounting = state.get("budget_accounting")
    if not isinstance(accounting, dict):
        raise ControllerError("operator budget accounting is not initialized")
    seq = int(accounting["ledger_seq"]) + 1
    body = {
        "schema_version": "awesome-theorems/stage5-operator-budget-ledger/2.0",
        "program": PROGRAM,
        "seq": seq,
        "kind": kind,
        "recorded_at": now(),
        "authority_chain_sha256": accounting["authority_chain_sha256"],
        "previous_record_sha256": accounting["ledger_head_sha256"],
        "payload": payload,
    }
    value = seal(body)
    raw = _budget_record_raw(value)
    BUDGET_LEDGER.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if accounting["ledger_seq"] == 0:
        if BUDGET_LEDGER.exists() and BUDGET_LEDGER.stat().st_size:
            raise ControllerError("operator budget ledger unexpectedly predates its state head")
    else:
        rows = BUDGET_LEDGER.read_bytes().splitlines()
        if not rows or digest(rows[-1]) != accounting["ledger_head_sha256"]:
            raise ControllerError("operator budget ledger head differs before append")
    with BUDGET_LEDGER.open("ab") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    accounting["ledger_seq"] = seq
    accounting["ledger_head_sha256"] = digest(raw[:-1])
    return value


def _reservation_totals(count: int, maxima: dict[str, Any]) -> dict[str, int]:
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise ControllerError("operator budget reservation count is invalid")
    result: dict[str, int] = {}
    for key in BUDGET_DIMENSIONS:
        value = maxima.get(key)
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ControllerError("operator budget per-generation maximum is invalid")
        result[key] = count * value
    return result


def ensure_budget_accounting(
    state: dict[str, Any], binding: dict[str, Any],
) -> dict[str, Any]:
    """Create/verify conservative reservation accounting before admission.

    The pre-ledger runtime is imported at the exact durable reservation count
    and charged at every per-generation maximum.  No historical uncertainty is
    converted into a refund.  A write-ahead ledger append may therefore leak a
    reservation after a crash, but can never authorize an extra generation.
    """
    maxima = binding["authority"]["per_claim_maxima"]
    effective = binding["effective_allowances"]
    accounting = state.get("budget_accounting")
    if accounting is None:
        legacy_ids = sorted({
            row.get("generation_id") for row in state.get("reservations", [])
            if isinstance(row, dict) and isinstance(row.get("generation_id"), str)
        })
        totals = _reservation_totals(len(legacy_ids), maxima)
        accounting = {
            "schema_version": "awesome-theorems/stage5-budget-accounting/2.0",
            "authority_chain_sha256": binding["authority_chain_sha256"],
            "ledger_seq": 0,
            "ledger_head_sha256": None,
            "reservation_count": 0,
            "reserved_totals": {key: 0 for key in BUDGET_DIMENSIONS},
            "effective_allowances": dict(effective),
        }
        state["budget_accounting"] = accounting
        existing_rows = _read_budget_ledger()
        if existing_rows:
            first = existing_rows[0]
            payload = first.get("payload", {})
            if (
                first.get("kind") != "legacy_import"
                or payload.get("generation_count") != len(legacy_ids)
                or payload.get("generation_ids_sha256") != digest(canonical(legacy_ids))
                or payload.get("reservation") != totals
            ):
                raise ControllerError("operator budget legacy import recovery differs")
        else:
            _append_budget_record(state, "legacy_import", {
                "generation_count": len(legacy_ids),
                "generation_ids_sha256": digest(canonical(legacy_ids)),
                "reservation": totals,
                "settlement_policy": "conservative_full_charge_for_preledger_generations",
            })
            existing_rows = _read_budget_ledger()
        accounting["reservation_count"] = len(legacy_ids)
        accounting["reserved_totals"] = totals
        accounting["ledger_seq"] = existing_rows[0]["seq"]
        accounting["ledger_head_sha256"] = digest(
            _budget_record_raw(existing_rows[0])[:-1],
        )
        # Recover any write-ahead reservations/settlements that reached the
        # append-only ledger before the enclosing atomic controller-state
        # write.  Only reservations increase consumption; a settlement never
        # refunds without an exact independent meter.
        for row in existing_rows[1:]:
            if row.get("authority_chain_sha256") != binding["authority_chain_sha256"]:
                raise ControllerError("operator budget recovery authority differs")
            if row.get("kind") == "reservation":
                reservation = row.get("payload", {}).get("reservation")
                if not isinstance(reservation, dict):
                    raise ControllerError("operator budget recovered reservation is malformed")
                for key in BUDGET_DIMENSIONS:
                    value = reservation.get(key)
                    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                        raise ControllerError("operator budget recovered reservation differs")
                    accounting["reserved_totals"][key] += value
                accounting["reservation_count"] += 1
            accounting["ledger_seq"] = row["seq"]
            accounting["ledger_head_sha256"] = digest(
                _budget_record_raw(row)[:-1],
            )
    if (
        not isinstance(accounting, dict)
        or accounting.get("schema_version") != "awesome-theorems/stage5-budget-accounting/2.0"
        or accounting.get("authority_chain_sha256") != binding["authority_chain_sha256"]
        or accounting.get("effective_allowances") != effective
        or not isinstance(accounting.get("ledger_seq"), int)
        or not isinstance(accounting.get("reservation_count"), int)
        or not isinstance(accounting.get("reserved_totals"), dict)
    ):
        raise ControllerError("operator budget accounting authority differs")
    rows = _read_budget_ledger()
    if accounting["ledger_seq"] > len(rows):
        raise ControllerError("operator budget state sequence leads its ledger")
    for row in rows[accounting["ledger_seq"]:]:
        if row.get("authority_chain_sha256") != binding["authority_chain_sha256"]:
            raise ControllerError("operator budget write-ahead authority differs")
        if row.get("kind") == "reservation":
            reservation = row.get("payload", {}).get("reservation")
            if not isinstance(reservation, dict):
                raise ControllerError("operator budget write-ahead reservation is malformed")
            for key in BUDGET_DIMENSIONS:
                value = reservation.get(key)
                if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                    raise ControllerError("operator budget write-ahead reservation differs")
                accounting["reserved_totals"][key] += value
            accounting["reservation_count"] += 1
        accounting["ledger_seq"] = row["seq"]
        accounting["ledger_head_sha256"] = row["authority_sha256"]
        # The head commits the exact serialized row, not merely its body seal.
        accounting["ledger_head_sha256"] = digest(
            _budget_record_raw(row)[:-1],
        )
    raw_rows = BUDGET_LEDGER.read_bytes().splitlines() if BUDGET_LEDGER.exists() else []
    if accounting["ledger_seq"] != len(raw_rows):
        raise ControllerError("operator budget ledger/state sequence differs")
    if raw_rows and digest(raw_rows[-1]) != accounting["ledger_head_sha256"]:
        raise ControllerError("operator budget ledger/state head differs")
    for key in BUDGET_DIMENSIONS:
        used = accounting["reserved_totals"].get(key)
        if isinstance(used, bool) or not isinstance(used, int) or not 0 <= used <= effective[key]:
            raise ControllerError("operator budget reserved total exceeds finite authority")
    return accounting


def reserve_generation_budget(
    state: dict[str, Any], record: dict[str, Any], binding: dict[str, Any],
) -> None:
    accounting = ensure_budget_accounting(state, binding)
    reservation = _reservation_totals(1, binding["authority"]["per_claim_maxima"])
    for key in BUDGET_DIMENSIONS:
        if accounting["reserved_totals"][key] + reservation[key] > accounting["effective_allowances"][key]:
            raise ControllerError(f"operator budget balance is insufficient for {key}")
    _append_budget_record(state, "reservation", {
        "item_id": record["item_id"],
        "claim_id": record["claim_id"],
        "generation_id": record["generation_id"],
        "lane_id": record["lane_id"],
        "prompt_digest": record["prompt_digest"],
        "reservation": reservation,
    })
    for key in BUDGET_DIMENSIONS:
        accounting["reserved_totals"][key] += reservation[key]
    accounting["reservation_count"] += 1
    record["budget_reservation"] = {
        "ledger_seq": accounting["ledger_seq"],
        "ledger_head_sha256": accounting["ledger_head_sha256"],
        "reservation": reservation,
    }


def _rollout_token_usage(record: dict[str, Any]) -> dict[str, int] | None:
    home = Path(str(record.get("codex_home", "")))
    totals = {
        "input_tokens": 0, "cached_input_tokens": 0,
        "output_tokens": 0, "reasoning_output_tokens": 0,
    }
    observed = False
    for path in sorted(home.glob("sessions/*/*/*/rollout-*.jsonl")):
        latest: dict[str, Any] | None = None
        try:
            for line in path.read_text(errors="replace").splitlines():
                try:
                    value = json.loads(line)
                except json.JSONDecodeError:
                    continue
                payload = value.get("payload")
                if (
                    value.get("type") == "event_msg"
                    and isinstance(payload, dict)
                    and payload.get("type") == "token_count"
                ):
                    info = payload.get("info")
                    usage = (
                        info.get("total_token_usage")
                        if isinstance(info, dict) else None
                    )
                    if isinstance(usage, dict):
                        latest = usage
        except OSError:
            continue
        if latest is not None:
            observed = True
            for key in totals:
                value = latest.get(key, 0)
                if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                    totals[key] += value
    if not observed:
        return None
    totals["billable_input_tokens"] = max(
        0, totals["input_tokens"] - totals["cached_input_tokens"],
    )
    return totals


def measured_generation_usage(record: dict[str, Any]) -> dict[str, Any]:
    goal = {"tokens_used": None, "time_used_seconds": None, "status": None}
    database = Path(str(record.get("codex_home", ""))) / "goals_1.sqlite"
    goal_id = record.get("goal_id")
    if database.is_file() and not database.is_symlink() and isinstance(goal_id, str):
        try:
            connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True, timeout=2)
            row = connection.execute(
                "select status,tokens_used,time_used_seconds from thread_goals where goal_id=?",
                (goal_id,),
            ).fetchone()
            connection.close()
            if row is not None:
                goal = {"status": row[0], "tokens_used": row[1], "time_used_seconds": row[2]}
        except sqlite3.Error:
            pass
    return {
        "goal_registry": goal,
        "rollout_tokens": _rollout_token_usage(record),
        "external_launches": 1 if int(record.get("goal_submissions", 0) or 0) > 0 else 0,
        "monetary_cost": "unknown_not_zero",
    }


def generation_budget_violation(record: dict[str, Any]) -> str | None:
    limits = record.get("execution_limits")
    if not isinstance(limits, dict):
        return None
    measured = measured_generation_usage(record)
    tokens = measured.get("rollout_tokens")
    if isinstance(tokens, dict):
        if tokens["billable_input_tokens"] > limits["model_input_tokens"]:
            return "model_input_token_budget_exceeded"
        if tokens["output_tokens"] > limits["model_output_tokens"]:
            return "model_output_token_budget_exceeded"
    elapsed = measured.get("goal_registry", {}).get("time_used_seconds")
    if isinstance(elapsed, int) and not isinstance(elapsed, bool) and elapsed > limits["generation_lifetime_seconds"]:
        return "generation_wall_budget_exceeded"
    if measured["external_launches"] > limits["external_launches"]:
        return "external_launch_budget_exceeded"
    return None


def settle_generation_budget(
    state: dict[str, Any], record: dict[str, Any], reason: str,
) -> None:
    if record.get("budget_settlement") is not None or not isinstance(state.get("budget_accounting"), dict):
        return
    value = _append_budget_record(state, "settlement", {
        "item_id": record.get("item_id"),
        "claim_id": record.get("claim_id"),
        "generation_id": record.get("generation_id") or record.get("run_id"),
        "reason": reason,
        "measured_usage": measured_generation_usage(record),
        "charged_reservation": (record.get("budget_reservation") or {}).get("reservation"),
        "released": {key: 0 for key in BUDGET_DIMENSIONS},
        "release_policy": "no refund without an exact provider/CPU meter; uncertainty is conservatively charged",
    })
    record["budget_settlement"] = {
        "ledger_seq": value["seq"],
        "authority_sha256": value["authority_sha256"],
    }


def read_crontab() -> str:
    completed = subprocess.run(["/usr/bin/crontab", "-l"], text=True, capture_output=True, check=False, timeout=10)
    if completed.returncode == 0:
        return completed.stdout
    if completed.returncode == 1 and "no crontab" in completed.stderr.lower():
        return ""
    raise ControllerError("cannot read current user crontab")


def activation_block() -> str:
    return CRON_BEGIN + "\n" + CRON_COMMAND + "\n" + CRON_END + "\n"


def validate_activation(
    specification: dict[str, Any] | None = None,
    prompt: dict[str, Any] | None = None,
    prompt_digest: str | None = None,
) -> dict[str, Any]:
    if specification is None:
        specification, _, _ = load_program()
    successor = validate_controller_successor_acceptance(specification)
    receipt = verify_seal(
        strict_json(
            _regular(ACTIVATION_RECEIPT, "controller activation receipt"),
            "controller activation receipt",
        ),
        "controller activation receipt",
    )
    current = read_crontab()
    if (
        receipt.get("schema_version") != "awesome-theorems/stage5-controller-activation/3.0"
        or receipt.get("program") != PROGRAM
        or receipt.get("controller_successor_acceptance_sha256") != file_digest(CONTROLLER_SUCCESSOR_ACCEPTANCE)
        or receipt.get("controller_successor_acceptance_authority_sha256") != successor.get("authority_sha256")
        or receipt.get("controller_sha256") != file_digest(Path(__file__))
        or receipt.get("execution_spec_sha256") != digest(canonical(specification))
        or receipt.get("operator_authority_sha256") != verify_seal(
            json.loads(_regular(OPERATOR_AUTHORITY, "operator budget authority")),
            "operator budget authority",
        ).get("authority_sha256")
        or receipt.get("operator_budget_renewal_authority_sha256") != verify_seal(
            strict_json(
                _regular(OPERATOR_BUDGET_RENEWAL, "operator budget renewal"),
                "operator budget renewal",
            ),
            "operator budget renewal",
        ).get("authority_sha256")
        or receipt.get("concurrency_prompt_sha256") != prompt_digest
        or receipt.get("concurrency_prompt_epoch") != (prompt or {}).get("policy_epoch")
        or receipt.get("post_crontab_sha256") != digest(current.encode())
        or current.count(CRON_BEGIN) != 1 or current.count(CRON_END) != 1
        or activation_block() not in current
        or not (RUNTIME / "logs").is_dir()
    ):
        raise ControllerError("controller activation receipt/current state differs")
    return receipt


def activate(concurrency_prompt: Path) -> dict[str, Any]:
    specification, rows, _ = load_program()
    prompt, prompt_digest = load_concurrency_prompt(concurrency_prompt, specification)
    if rows[0]["state"] != "x":
        raise ControllerError("activation requires BOOT=x")
    binding = validate_operator_authority(specification, prompt, prompt_digest)
    successor = validate_controller_successor_acceptance(specification)
    before = read_crontab()
    existing_exact = (
        before.count(CRON_BEGIN) == 1
        and before.count(CRON_END) == 1
        and activation_block() in before
    )
    if (CRON_BEGIN in before or CRON_END in before) and not existing_exact:
        raise ControllerError("theorem v2 cron marker exists but differs")
    if "AWESOME_THEOREMS_STAGE5_CONJECTURES_EXECUTION_V2" in before:
        raise ControllerError("conjecture v2 controller activation is not authorized")
    # POSIX shells open redirections before executing Python.  Without this
    # exact directory the installed cron line never starts the controller.
    (RUNTIME / "logs").mkdir(parents=True, exist_ok=True, mode=0o700)
    after = before if existing_exact else before + ("" if not before or before.endswith("\n") else "\n") + activation_block()
    if not existing_exact:
        completed = subprocess.run(["/usr/bin/crontab", "-"], input=after, text=True, capture_output=True, check=False, timeout=10)
        if completed.returncode != 0 or read_crontab() != after:
            raise ControllerError("crontab compare-and-set verification failed")
    try:
        receipt = seal({
            "schema_version": "awesome-theorems/stage5-controller-activation/3.0",
            "program": PROGRAM, "activated_at": now(),
            "pre_crontab_sha256": digest(before.encode()), "post_crontab_sha256": digest(after.encode()),
            "cron_command_sha256": digest(CRON_COMMAND.encode()), "controller_sha256": file_digest(Path(__file__)),
            "execution_spec_sha256": digest(canonical(specification)),
            "operator_authority_sha256": binding["authority"]["authority_sha256"],
            "operator_budget_renewal_authority_sha256": binding["renewal"]["authority_sha256"],
            "operator_budget_authority_chain_sha256": binding["authority_chain_sha256"],
            "concurrency_prompt_sha256": prompt_digest,
            "concurrency_prompt_epoch": prompt["policy_epoch"],
            "controller_successor_acceptance_sha256": file_digest(CONTROLLER_SUCCESSOR_ACCEPTANCE),
            "controller_successor_acceptance_authority_sha256": successor["authority_sha256"],
            "operator_goal": binding["goal"],
        })
        atomic_json(ACTIVATION_RECEIPT, receipt, 0o444)
        validate_activation(specification, prompt, prompt_digest)
        return receipt
    except Exception as exc:
        current = read_crontab()
        if not existing_exact and current == after:
            subprocess.run(["/usr/bin/crontab", "-"], input=before, text=True, capture_output=True, check=False, timeout=10)
        if ACTIVATION_RECEIPT.exists() and not ACTIVATION_RECEIPT.is_symlink():
            ACTIVATION_RECEIPT.unlink()
        raise ControllerError(f"activation failed; crontab restored: {exc}") from exc


def tmux(record: dict[str, Any], *args: str, check: bool = True, timeout: float = 30, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    # Use a task-local relative socket name: the absolute v2 runtime path is
    # longer than sockaddr_un's limit, while the tmux client cwd is the claim
    # root and therefore still proves socket locality.
    socket = record.get("socket_argument", "tmux.sock")
    return subprocess.run(["/usr/bin/tmux", "-S", socket, *args], cwd=record["task_root"], input=input_text,
                          text=True, capture_output=True, check=check, timeout=timeout)


def append_event(kind: str, payload: dict[str, Any]) -> None:
    RUNTIME.joinpath("ledgers").mkdir(parents=True, exist_ok=True)
    RUNTIME.joinpath("locks").mkdir(parents=True, exist_ok=True)
    with EVENT_LOCK.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        EVENTS.parent.mkdir(parents=True, exist_ok=True)
        with EVENTS.open("a+") as ledger:
            ledger.seek(0)
            lines = [x for x in ledger.read().splitlines() if x]
            previous = digest(lines[-1].encode()) if lines else None
            body = {"schema_version": "awesome-theorems/stage5-v2-event/1.0", "seq": len(lines)+1,
                    "event_id": str(uuid.uuid4()), "event": kind, "program": PROGRAM,
                    "at": now(), "previous_record_sha256": previous, "payload": payload}
            record = seal(body)
            ledger.seek(0, os.SEEK_END)
            ledger.write(json.dumps(record, sort_keys=True) + "\n")
            ledger.flush(); os.fsync(ledger.fileno())
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def _lease_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line:
            continue
        rows.append(verify_seal(strict_json(line.encode(), f"{path.name}:{index}"), path.name))
    return rows


def _latest_leases(rows: Sequence[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for row in rows:
        lease_id = row.get("lease_id")
        if isinstance(lease_id, str):
            latest[lease_id] = row
    return latest


def _parse_instant(value: Any) -> float | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def request_lease_usage(
    prompt: dict[str, Any], state: dict[str, Any] | None = None,
    at_epoch: float | None = None,
) -> dict[str, int]:
    """Measure starts and live leases without treating expired files as work."""
    at_epoch = time.time() if at_epoch is None else at_epoch
    window_start = at_epoch - int(prompt["request_window_seconds"])
    request_rows = _lease_rows(REQUEST_LEASES)
    turn_rows = _lease_rows(TURN_LEASES)
    # A lease ledger is append-only: a later release row supersedes the
    # acquisition row.  Counting every historical acquisition would make a
    # completed generation consume the request-start budget forever.
    starts = sum(
        row.get("status") == "leased"
        and (stamp := _parse_instant(row.get("acquired_at"))) is not None
        and stamp >= window_start
        for row in _latest_leases(request_rows).values()
    )
    state = load_state(False) if state is None else state
    active_runs = {
        record.get("run_id") for record in state.get("claims", {}).values()
        if record.get("status") in ACTIVE_GENERATION_STATUSES
    }
    in_flight = sum(
        row.get("status") == "leased" and row.get("run_id") in active_runs
        for row in _latest_leases(request_rows).values()
    )
    running = sum(
        row.get("status") == "leased" and row.get("run_id") in active_runs
        for row in _latest_leases(turn_rows).values()
    )
    return {"request_starts_per_window": starts, "in_flight_requests": in_flight, "running_turns": running}


def acquire_request_leases(record: dict[str, Any], prompt: dict[str, Any]) -> None:
    """Atomically enforce request-window, in-flight and running-turn ceilings."""
    REQUEST_LEASES.parent.mkdir(parents=True, exist_ok=True)
    REQUEST_LOCK.parent.mkdir(parents=True, exist_ok=True)
    with REQUEST_LOCK.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        ledgers = ((REQUEST_LEASES, "outbound_request"), (TURN_LEASES, "running_turn"))
        existing: dict[str, dict[str, Any]] = {}
        for path, kind in ledgers:
            matches = [
                row for row in _latest_leases(_lease_rows(path)).values()
                if row.get("status") == "leased" and row.get("run_id") == record["run_id"]
            ]
            if len(matches) > 1:
                raise ControllerError(f"multiple active {kind} leases for one generation")
            if matches:
                existing[kind] = matches[0]
        if existing:
            if set(existing) != {"outbound_request", "running_turn"}:
                raise ControllerError("partial request/turn lease transaction detected")
            for kind, row in existing.items():
                record[f"{kind}_lease_id"] = row["lease_id"]
            return
        state = load_state(False)
        usage = request_lease_usage(prompt, state)
        vector = prompt["concurrency"]
        if usage["request_starts_per_window"] >= vector["outbound_request_starts_per_window"]:
            raise ControllerError("outbound request-start window is saturated")
        if usage["in_flight_requests"] >= vector["in_flight_requests"]:
            raise ControllerError("in-flight request cap is saturated")
        if usage["running_turns"] >= vector["running_turns"]:
            raise ControllerError("running-turn cap is saturated")
        records: list[tuple[Path, str, dict[str, Any]]] = []
        for path, kind in ledgers:
            body = {"schema_version": "awesome-theorems/stage5-v2-lease/1.0", "kind": kind,
                    "program": PROGRAM, "item_id": record["item_id"], "claim_id": record["claim_id"],
                    "run_id": record["run_id"], "execution_id": record["run_id"],
                    "lease_id": str(uuid.uuid4()), "status": "leased", "acquired_at": now(),
                    "expires_at": datetime.fromtimestamp(time.time()+900, timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")}
            records.append((path, kind, body))
        for path, kind, body in records:
            with path.open("a") as stream:
                stream.write(json.dumps(seal(body), sort_keys=True) + "\n")
                stream.flush(); os.fsync(stream.fileno())
            record[f"{kind}_lease_id"] = body["lease_id"]


def release_request_leases(record: dict[str, Any], reason: str) -> None:
    """Release only this generation's exact leases; repeat calls are harmless."""
    if not any(record.get(key) for key in ("outbound_request_lease_id", "running_turn_lease_id")):
        return
    REQUEST_LEASES.parent.mkdir(parents=True, exist_ok=True)
    REQUEST_LOCK.parent.mkdir(parents=True, exist_ok=True)
    with REQUEST_LOCK.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        for path, kind in ((REQUEST_LEASES, "outbound_request"), (TURN_LEASES, "running_turn")):
            lease_id = record.get(f"{kind}_lease_id")
            if not isinstance(lease_id, str):
                continue
            latest = _latest_leases(_lease_rows(path)).get(lease_id)
            if latest is None or latest.get("status") != "leased":
                continue
            body = {
                "schema_version": "awesome-theorems/stage5-v2-lease/1.0",
                "kind": kind, "program": PROGRAM, "item_id": record.get("item_id"),
                "claim_id": record.get("claim_id"), "run_id": record.get("run_id"),
                "execution_id": record.get("run_id"), "lease_id": lease_id,
                "status": "released", "released_at": now(), "reason": reason,
            }
            with path.open("a") as stream:
                stream.write(json.dumps(seal(body), sort_keys=True) + "\n")
                stream.flush(); os.fsync(stream.fileno())


def load_state(create: bool = True) -> dict[str, Any]:
    if not STATE_PATH.exists():
        if not create: return {"claims": {}}
        state = seal({"schema_version": "awesome-theorems/stage5-v2-state/1.0", "program": PROGRAM, "claims": {}, "updated_at": now()})
        atomic_json(STATE_PATH, state, 0o600); return state
    return verify_seal(json.loads(STATE_PATH.read_text()), "controller state")


def save_state(state: dict[str, Any]) -> None:
    body = dict(state); body.pop("authority_sha256", None); body["updated_at"] = now(); atomic_json(STATE_PATH, seal(body), 0o600)


@contextmanager
def scheduler_guard(nonblocking: bool = True):
    """Serialize launch/tick/stop transitions across cron and manual calls."""
    SCHEDULER_LOCK.parent.mkdir(parents=True, exist_ok=True)
    with SCHEDULER_LOCK.open("a+") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | (fcntl.LOCK_NB if nonblocking else 0))
        except BlockingIOError as exc:
            raise ControllerError("scheduler transition already in progress") from exc
        try:
            yield
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


@contextmanager
def admission_pump_guard():
    ADMISSION_PUMP_LOCK.parent.mkdir(parents=True, exist_ok=True)
    with ADMISSION_PUMP_LOCK.open("a+") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ControllerError("admission pump already in progress") from exc
        try:
            yield
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def process_ticks(pid: int) -> int | None:
    try:
        return int(Path(f"/proc/{pid}/stat").read_text().split(") ", 1)[1].split()[19])
    except (OSError, ValueError, IndexError): return None


def process_env(pid: int, key: str) -> str | None:
    try:
        for entry in Path(f"/proc/{pid}/environ").read_bytes().split(b"\0"):
            if entry.startswith(key.encode() + b"="): return entry.split(b"=", 1)[1].decode()
    except (OSError, UnicodeDecodeError): pass
    return None


def process_cmdline(pid: int) -> str:
    try:
        return Path(f"/proc/{pid}/cmdline").read_bytes().replace(b"\0", b" ").decode()
    except (OSError, UnicodeDecodeError):
        return ""


def codex_argv(work: Path) -> list[str]:
    return [str(CODEX), "-C", str(work), "-c", "features.goals=true",
            "--disable", "multi_agent", "--disable", "multi_agent_v2",
            "--disable", "plugins", "--disable", "remote_plugin",
            "--disable", "recommended_plugins", "--no-alt-screen", "-m", MODEL,
            "-c", f"model_reasoning_effort={EFFORT}", "-c", f"service_tier={SERVICE_TIER}",
            "-c", f"model_provider={PROVIDER}",
            # Disable every agent/plugin surface at the process boundary as
            # well as in the private config.  This is defense in depth for
            # workers instructed to use exactly one interactive thread and
            # one authenticated /goal; config-only flags have changed names
            # across Codex releases.
            "-c", "features.multi_agent=false",
            "-c", "features.multi_agent_v2=false",
            "-c", "features.multi_agent_v2.max_concurrent_threads_per_session=1",
            "-c", f"features.multi_agent_v2.multi_agent_mode_hint_text={json.dumps(MULTI_AGENT_MODE_HINT)}",
            "-c", f"developer_instructions={json.dumps(TASK_LOCAL_DEVELOPER_INSTRUCTIONS)}",
            "-c", "features.plugins=false",
            "-c", "features.remote_plugin=false",
            "-c", "features.recommended_plugins=false"]


def bootstrap_home(home: Path) -> None:
    if not AUTH_SOURCE.is_file() or AUTH_SOURCE.is_symlink(): raise ControllerError("Codex credentials unavailable")
    home.mkdir(parents=True, exist_ok=False, mode=0o700); shutil.copyfile(AUTH_SOURCE, home / "auth.json"); os.chmod(home / "auth.json", 0o600)
    if not CONFIG_SOURCE.is_file() or CONFIG_SOURCE.is_symlink(): raise ControllerError("Codex provider config unavailable")
    try:
        source = tomllib.loads(CONFIG_SOURCE.read_text(encoding="utf-8"))
        providers = source.get("model_providers", {})
        provider = providers.get(PROVIDER)
        provider_source = PROVIDER
        if provider is None:
            # The host config currently names the same local proxy "OpenAI".
            # Freeze it under the Blueprint's route identity inside each
            # private home; never let Codex silently fall back to api.openai.com.
            provider = providers.get("OpenAI")
            provider_source = "OpenAI"
        if not isinstance(provider, dict) or provider.get("wire_api") != "responses" or not isinstance(provider.get("base_url"), str):
            raise ControllerError("selected Codex provider is incomplete")
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ControllerError("Codex provider config invalid") from exc
    config = (f'model_provider = "{PROVIDER}"\nmodel = "{MODEL}"\nmodel_reasoning_effort = "{EFFORT}"\nservice_tier = "{SERVICE_TIER}"\napproval_policy = "never"\nsandbox_mode = "danger-full-access"\nnetwork_access = "enabled"\n[model_providers.{PROVIDER}]\nname = {json.dumps(provider.get("name", PROVIDER))}\nbase_url = {json.dumps(provider["base_url"])}\nwire_api = "responses"\nsupports_websockets = {str(bool(provider.get("supports_websockets", False))).lower()}\nrequires_openai_auth = {str(bool(provider.get("requires_openai_auth", True))).lower()}\n[features]\ngoals = true\nmulti_agent = false\nmulti_agent_v2 = false\nplugins = false\nremote_plugin = false\nrecommended_plugins = false\n').encode()
    # Return-free function: the source alias is recorded in the claim below.
    home.joinpath("provider-source.txt").write_text(provider_source + "\n", encoding="utf-8")
    os.chmod(home / "provider-source.txt", 0o400)
    atomic_write(home / "config.toml", config, 0o600)


def copy_file(src: Path, dst: Path, mode: int = 0o444) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, dst); os.chmod(dst, mode)


def copy_provider_sources(work: Path, item: dict[str, Any]) -> None:
    """Materialize only the exact pinned provider source surface for one TARGET."""
    match = re.fullmatch(r"S5THM-([0-9]{8})-TARGET", item["item_id"])
    if match is None:
        raise ControllerError("provider source materialization requires a theorem TARGET")
    workset = json.loads((EVIDENCE / "workset-5.6.json").read_text(encoding="utf-8"))
    member_id = f"S5-CLM-{match.group(1)}"
    matches = [row for row in workset.get("members", []) if row.get("stage_claim_id") == member_id]
    if len(matches) != 1:
        raise ControllerError("exact theorem provider member is absent")
    member = matches[0]
    provider_id = member["provider_id"]
    if provider_id == "mathlib-8a178386":
        source_root = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
        evidence = member.get("proof_evidence")
        formal = member.get("formal_statement")
        if not isinstance(evidence, dict) or not isinstance(formal, dict):
            raise ControllerError("mathlib provider authority is malformed")
        revision = evidence.get("mathlib_commit")
        module = formal.get("module")
        if not isinstance(module, str) or not module.startswith("Mathlib."):
            raise ControllerError("mathlib provider module is malformed")
        source_paths = {module.replace(".", "/") + ".lean"}
    elif provider_id == "formal-conjectures-2270d31e":
        # The Formal Conjectures checkout is statement authority only but is
        # still mandatory for resolving the exact source semantic environment.
        source_root = ROOT / "Formalizations/Lean/.lake/packages/formal-conjectures"
        locator = member.get("source_locator")
        formal = member.get("formal_statement")
        if not isinstance(locator, dict) or not isinstance(formal, dict):
            raise ControllerError("Formal Conjectures provider authority is malformed")
        revision = locator.get("revision")
        formal_locator = formal.get("locator")
        if not isinstance(formal_locator, dict):
            raise ControllerError("Formal Conjectures formal locator is malformed")
        source_paths = {
            locator.get("member_path"), formal_locator.get("member_path"),
        }
    else:
        raise ControllerError(f"unsupported pinned provider: {provider_id}")
    if source_root.is_symlink() or not source_root.is_dir():
        raise ControllerError(
            f"pinned provider source checkout unavailable: {provider_id}@{revision}"
        )
    target_root = work / "_baseline/provider-sources" / provider_id / revision
    copied = 0
    if not isinstance(revision, str) or not revision:
        raise ControllerError("pinned provider revision is malformed")
    for relative in source_paths:
        if not isinstance(relative, str) or not relative:
            raise ControllerError("pinned provider source path is malformed")
        source = source_root / relative
        if source.is_symlink() or not source.is_file():
            raise ControllerError(f"pinned provider source file unavailable: {relative}")
        copy_file(source, target_root / relative)
        copied += 1
    if copied == 0:
        raise ControllerError("no pinned provider source was materialized")
    formal = member["formal_statement"]
    if provider_id == "formal-conjectures-2270d31e":
        module = member["module"]
        declaration = formal["qualified_declaration"]
        toolchain = "leanprover/lean4:v4.27.0"
        environment = "Formalizations/Lean/.lake/packages/formal-conjectures"
    else:
        module = formal["module"]
        declaration = formal["declaration"]
        toolchain = "leanprover/lean4:v4.29.0"
        environment = "Formalizations/Lean"
    route = {
        "schema_version": "awesome-theorems/stage5-provider-kernel-route/1.0",
        "provider_id": provider_id, "revision": revision,
        "module": module, "lean_module": item_checker().lean_module_spelling(module),
        "qualified_declaration": declaration, "toolchain": toolchain,
        "master_environment": environment,
        "proof_authority": "claim_owned_root_only",
        "provider_body_authority": False,
    }
    route["authority_sha256"] = digest(canonical(route))
    atomic_json(work / "_baseline/provider-kernel-route.json", route, 0o444)


def claim_mode(item_id: str) -> str:
    if item_id == "S5THM-BOOT-001":
        return "BOOT"
    if item_id == "S5THM-PROGRAM-RELEASE":
        return "PROGRAM-RELEASE"
    if re.fullmatch(r"S5THM-SHARD-[A-Z]+-[0-9]{3}", item_id):
        return "SHARD"
    if item_id == "S5THM-AGG-001":
        return "AGG"
    if item_id == "S5THM-QA-001":
        return "QA"
    match = re.fullmatch(r"S5THM-[0-9]{8}-(.+)", item_id)
    if match:
        return "TARGET-" + match.group(1)
    raise ControllerError(f"unsupported theorem item mode: {item_id}")


def render_finalizer() -> bytes:
    """Render the task-local, controller-owned worker result writer."""
    return b'''#!/usr/bin/env python3
import difflib, hashlib, json, os, pathlib, subprocess, tempfile
from datetime import datetime, timezone
WORK = pathlib.Path(__file__).resolve().parent.parent
TASK = WORK.parent
CLAIM_PATH = TASK / "claim.json"
OUTBOX = WORK / "_outbox"
def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
def sha(raw): return hashlib.sha256(raw).hexdigest()
def instant(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
claim = json.loads(CLAIM_PATH.read_text(encoding="utf-8"))
if pathlib.Path(claim.get("task_root", "")).resolve() != TASK: raise SystemExit("task root identity differs")
owned = claim["writable_paths"]
artifacts, patch_parts = [], []
for relative in owned:
    path = WORK / relative
    if path.is_symlink() or not path.is_file(): raise SystemExit("missing owned file: " + relative)
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    media_type = "application/json" if path.suffix == ".json" else ("text/x-lean" if path.suffix == ".lean" else ("text/markdown" if path.suffix == ".md" else "text/plain"))
    artifacts.append({"path": str(path), "sha256": sha(raw), "size_bytes": len(raw), "media_type": media_type})
    patch_parts.extend(difflib.unified_diff([], text.splitlines(True), fromfile="/dev/null", tofile="b/" + relative))
patch_raw = "".join(patch_parts).encode("utf-8")
patch_path = TASK / "changes.patch"
fd, temporary = tempfile.mkstemp(prefix=".changes.patch.", dir=TASK)
try:
    with os.fdopen(fd, "wb") as stream: stream.write(patch_raw); stream.flush(); os.fsync(stream.fileno())
    os.replace(temporary, patch_path)
finally:
    if os.path.exists(temporary): os.unlink(temporary)
outcomes = []
for command in claim["validation_commands"]:
    started = instant(); env = {row["name"]: row["value"] for row in command["environment"]}
    completed = subprocess.run(command["argv"], cwd=WORK / command["cwd"], env={**os.environ, **env}, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=command["timeout_seconds"], check=False)
    finished = instant()
    outcomes.append({"command_id": command["command_id"], "argv_sha256": sha(canonical(command["argv"])), "exit_code": completed.returncode, "passed": completed.returncode == 0, "stdout_sha256": sha(completed.stdout), "stderr_sha256": sha(completed.stderr), "started_at": started, "finished_at": finished})
    if completed.returncode != 0: raise SystemExit("validation failed: " + command["command_id"])
unsigned = {"schema_version": "awesome-theorems/stage5-proof-debt-worker-result/1.0", "program": claim["program"], "claim_id": claim["claim_id"], "run_id": claim["run_id"], "item_id": claim["item_id"], "mode": claim["mode"], "claim_card_sha256": sha(CLAIM_PATH.read_bytes()), "baseline_sha256": sha(canonical(claim["baseline"])), "status": "self_tested", "changed_paths": owned, "patch": {"path": str(patch_path), "sha256": sha(patch_raw), "size_bytes": len(patch_raw)}, "command_outcomes": outcomes, "artifacts": artifacts, "completed_at": instant()}
unsigned["authority_sha256"] = sha(canonical(unsigned))
OUTBOX.mkdir(exist_ok=True)
fd, temporary = tempfile.mkstemp(prefix=".result.", dir=OUTBOX)
try:
    with os.fdopen(fd, "w", encoding="utf-8") as stream: json.dump(unsigned, stream, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False); stream.write("\\n"); stream.flush(); os.fsync(stream.fileno())
    os.replace(temporary, OUTBOX / "result.json")
finally:
    if os.path.exists(temporary): os.unlink(temporary)
print("SELF_TESTED", claim["item_id"], unsigned["authority_sha256"])
'''


def materialize_claim(
    item: dict[str, Any], specification: dict[str, Any], blueprint_raw: bytes,
    ordinal: int, *, prompt: dict[str, Any], prompt_digest: str,
    resolved_concurrency: dict[str, int | str], concurrency_prompt_path: Path,
    generation_id: str | None = None, lane_id: str | None = None,
    replacement_ordinal: int = 0,
    previous_generation_id: str | None = None,
) -> dict[str, Any]:
    claim_id = f"{item['item_id']}--worker"; run_id = generation_id or f"r-{int(time.time())}-{uuid.uuid4().hex[:8]}"
    exact_prompt_raw = _regular(concurrency_prompt_path, "concurrency prompt")
    if digest(exact_prompt_raw) != prompt_digest:
        raise ControllerError("concurrency prompt changed before claim materialization")
    requested_concurrency = validate_concurrency_vector(prompt.get("concurrency"))
    resolved_concurrency = validate_concurrency_vector(resolved_concurrency)
    root = RUNTIME / "tasks" / claim_id / run_id; work = root / "work"; home = root / "codex-home"; root.mkdir(parents=True, exist_ok=False, mode=0o700); work.mkdir(mode=0o700)
    for rel in item["owned_paths"]: (work / rel).parent.mkdir(parents=True, exist_ok=True)
    # ``blueprint_raw`` is the exact parser/admission snapshot whose digest is
    # written into the immutable claim below.  Do not reopen the canonical
    # Blueprint here: Master may accept another handoff between parsing and
    # materialization, which previously produced a read-only baseline whose
    # bytes disagreed with the claim's own baseline_sha256.
    atomic_write(
        work / "_baseline/Stage5_Theorems_Blueprint.md",
        blueprint_raw,
        0o444,
    )
    for rel in ("workset-5.6.json", "workset-5.6-receipt.json", "execution-spec.json", "foundation-profiles.json", "provider-registry.json", "claim-card.schema.json", "worker-result.schema.json", "master-acceptance.schema.json"):
        copy_file(EVIDENCE / rel, work / "_baseline" / rel)
    copy_file(concurrency_prompt_path, work / "_baseline/concurrency-prompt.json")
    copy_file(ITEM_CHECKER_PATH, work / "_baseline/check_stage5_theorem_item.py")
    copy_file(PROGRAM_ITEM_CHECKER_PATH, work / "_baseline/check_stage5_theorem_program_item.py")
    atomic_write(work / "_baseline/finalize.py", render_finalizer(), 0o555)
    mode = claim_mode(item["item_id"])
    if mode == "TARGET-TARGET":
        copy_provider_sources(work, item)
    copy_checkpoint_bootstrap(
        work, item["item_id"], previous_generation_id,
    )
    bootstrap_files = []
    for path in sorted((work / "_baseline").rglob("*")):
        if path.is_dir() and not path.is_symlink():
            continue
        if path.is_symlink() or not path.is_file():
            raise ControllerError(f"invalid read-only bootstrap materialization: {path}")
        bootstrap_files.append({
            "path": path.relative_to(work).as_posix(),
            "sha256": file_digest(path),
            "size_bytes": path.stat().st_size,
        })
    bootstrap_home(home)
    execution_limits, recovery = validate_execution_policy(prompt["execution_limits"], prompt["recovery"])
    maxima = specification["operator_budget_policy"]["finite_initial_allowances"]["per_claim_maxima"]
    if mode == "TARGET-TARGET":
        validation = {"command_id":"complete-target-semantic-proof-debt","cwd":str(work),"argv":["/usr/bin/python3",str(work/"_baseline/check_stage5_theorem_item.py"),"--claim-card",str(root/"claim.json"),"--work-root",str(work),"--no-lean"],"environment":[],"timeout_seconds":900,"network":"denied"}
    else:
        validation = {"command_id":f"validate-{mode.lower()}-program-artifacts","cwd":str(work),"argv":["/usr/bin/python3",str(work/"_baseline/check_stage5_theorem_program_item.py"),"--claim-card",str(root/"claim.json"),"--work-root",str(work)],"environment":[],"timeout_seconds":900,"network":"denied"}
    resource_budget = {
        "model_input_tokens": execution_limits["model_input_tokens"],
        "model_output_tokens": execution_limits["model_output_tokens"],
        "model_turns": execution_limits["model_turns"],
        "external_launches": execution_limits["external_launches"],
        "wall_seconds": execution_limits["generation_lifetime_seconds"],
        "cpu_seconds": execution_limits["cpu_seconds"],
    }
    replacement_cap = recovery["generation_replacements_per_work_item"]
    if not isinstance(replacement_ordinal, int) or isinstance(replacement_ordinal, bool) or not 0 <= replacement_ordinal <= replacement_cap:
        raise ControllerError("per-item replacement ordinal exceeds recovery policy")
    deliverable = item["title"] + ". " + item["gate"]
    if mode == "TARGET-TARGET":
        # A TARGET generation has a deliberately small, inode-independent
        # evidence surface.  Tell the worker exactly how to use it so the
        # absence of a local Lake environment does not invite cloning an
        # upstream repository or reading the canonical checkout.  Canonical
        # trust-zero Lean compilation remains a Master-only acceptance gate.
        deliverable += (
            " Worker validation is the task-local --no-lean semantic/evidence "
            "preflight only: do not invoke Lean, Lake or Elan; do not clone, "
            "fetch or reconstruct any repository; and never inspect "
            "canonical_repository_root. Use only the immutable "
            "read_only_bootstrap_files, including pinned provider-sources, "
            "plus this generation's writable_paths. Master alone performs "
            "provider-native trust-zero Lean compilation after harvest. Read "
            "`_baseline/provider-kernel-route.json`: every Statement.lean, "
            "Proof.lean and Audit.lean must actively import its exact `lean_module` "
            "and reference its exact `qualified_declaration` (comments do not "
            "count). Audit.lean must include the kernel-checkable witness "
            "`example : type_of% <qualified_declaration> := <claim-owned machine root>` "
            "and `#print axioms <claim-owned machine root>`. Independently prove "
            "that root without an oracle or the provider proof body; Master selects "
            "the sealed provider-native toolchain/environment and rejects any "
            "fallback, substitution, `sorryAx`, or custom axiom."
        )
    card = {"schema_version":"awesome-theorems/stage5-proof-debt-claim-card/1.1","program":PROGRAM,"claim_id":claim_id,"run_id":run_id,"item_id":item["item_id"],"mode":mode,"dependencies":list(item["dependencies"],),"baseline":{"execution_spec_sha256":digest(canonical(specification)),"blueprint_sha256":digest(blueprint_raw),"source_bundle_sha256":specification["source_bundle"]["sha256"],"dependency_state_sha256":digest(canonical([[x,"master_accepted"] for x in item["dependencies"]])),"owned_paths_baseline_sha256":digest(canonical([[x,None] for x in item["owned_paths"]]))},"deadline":datetime.fromtimestamp(time.time() + execution_limits["generation_lifetime_seconds"], timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ"),"task_root":str(root),"canonical_repository_root":str(ROOT),"canonical_write_policy":"forbidden","writable_paths":list(item["owned_paths"]),"read_only_bootstrap_files":bootstrap_files,"deliverable":deliverable,"validation_commands":[validation],"artifact_policy":{"allowed_paths":list(item["owned_paths"]),"required_paths":list(item["owned_paths"]),"forbidden_paths":["Docs/Stage5_Theorems_Blueprint.md","Docs/Stage5_Theorems_Gantt.md","Docs/catalog",".git",".ops"]},"result_schema":{"path":"Docs/evidence/stage5_theorems/worker-result.schema.json","schema_id":"https://awesome-theorems.invalid/schemas/stage5-theorem-worker-result-1.0.json","sha256":file_digest(EVIDENCE/"worker-result.schema.json")},"resource_budget":resource_budget,"retry_budget":{"attempt":replacement_ordinal + 1,"max_attempts":replacement_cap + 1},"execution_policy":{"execution_limits":execution_limits,"recovery":recovery},"generation_lineage":{"replacement_ordinal":replacement_ordinal,"replacement_cap":replacement_cap,"previous_generation_id":previous_generation_id},"execution_identity":{"lane_id":lane_id or item["item_id"],"generation_id":run_id,"prompt_epoch":prompt["policy_epoch"],"prompt_digest":prompt_digest,"execution_spec_sha256":digest(canonical(specification)),"requested_concurrency":requested_concurrency,"resolved_concurrency":resolved_concurrency}}
    atomic_json(root / "claim.json", card, 0o444)
    return {"item_id":item["item_id"],"claim_id":claim_id,"run_id":run_id,"generation_id":run_id,"lane_id":lane_id or item["item_id"],"task_root":str(root),"work_root":str(work),"codex_home":str(home),"socket_path":str(root/"tmux.sock"),"socket_argument":"tmux.sock","session":"s5-"+digest(f"{claim_id}/{run_id}".encode())[:20],"status":"materialized","goal_submissions":0,"ordinal":ordinal,"recovery":recovery,"execution_limits":execution_limits,"generation_started_at":time.time(),"generation_deadline_epoch":time.time()+execution_limits["generation_lifetime_seconds"],"replacement_ordinal":replacement_ordinal,"previous_generation_id":previous_generation_id}


def submit_goal(
    record: dict[str, Any], prompt: dict[str, Any],
    on_transition: Any | None = None,
    invocation_deadline: float | None = None,
) -> None:
    invocation_deadline = time.monotonic() + 180 if invocation_deadline is None else invocation_deadline
    hard_deadline = float(record.get("startup_deadline_epoch", time.time() + 180))
    if time.time() >= hard_deadline:
        raise ControllerError("startup hard deadline expired")
    status = record.get("status")
    if status == "materialized":
        if record.get("goal_submissions") != 0:
            raise ControllerError("duplicate /goal refused")
        tmux(record, "-f", "/dev/null", "new-session", "-d", "-s", record["session"], "-c", record["work_root"], "env", "-u", "CODEX_CI", "-u", "CODEX_THREAD_ID", "-u", "CODEX_REMOTE_PAYLOAD", f"CODEX_HOME={record['codex_home']}", *codex_argv(Path(record["work_root"])))
        pid = int(tmux(record,"display-message","-p","-t",f"{record['session']}:0.0","#{pane_pid}").stdout.strip()); record["pane_pid"] = pid; record["pane_pid_start_ticks"] = process_ticks(pid)
        record["status"] = "tmux_started"; record["tmux_started_at"] = now()
        if on_transition is not None: on_transition(record)
        status = "tmux_started"
    elif status not in {
        "tmux_started", "goal_pasted", "submission_committed",
        "goal_submitted", "live",
    }:
        raise ControllerError(f"startup cannot advance status {status!r}")
    if status in {"submission_committed", "goal_submitted", "live"}:
        return
    if not transport_identity_alive(record):
        raise ControllerError("startup transport identity is not alive")
    # Codex may spend well over a minute refreshing model/plugin metadata
    # before it renders the actual composer.  Do not mistake the welcome
    # banner's ``>_`` logo for an input prompt.
    trust_confirmed = bool(record.get("trust_confirmed"))
    if status == "tmux_started":
      while time.monotonic() < invocation_deadline and time.time() < hard_deadline:
        pane = tmux(record,"capture-pane","-p","-J","-t",f"{record['session']}:0.0",check=False).stdout
        # The first-run selector is a real numbered prompt.  Match its exact
        # two-choice shape and select option 1 once; broad matches such as
        # any occurrence of “trust” can fire before the selector is active and
        # leave the TUI waiting forever with an empty private registry.
        trust_selector = "1. Yes, continue" in pane and "2. No, quit" in pane
        if trust_selector and not trust_confirmed:
            tmux(record,"send-keys","-t",f"{record['session']}:0.0","Enter")
            trust_confirmed = True
            record["trust_confirmed"] = True
            if on_transition is not None: on_transition(record)
            time.sleep(1.0)
            continue
        # The accepted selector remains in scrollback, so its text may still
        # be present after Enter.  Once a real composer/help prompt is
        # rendered, trust has completed even if the historical selector is
        # visible above it.
        if trust_confirmed and (
            "use /skills" in pane.lower()
            or "ask codex" in pane.lower()
            or "implement {feature}" in pane.lower()
        ):
            break
        if ("»" in pane or "›" in pane) and not trust_selector:
            break
        time.sleep(.5)
      else:
        return
      token = "GOAL_READY_" + digest(f"{record['claim_id']}/{record['run_id']}".encode())[:24].upper(); record["goal_token"] = token
      objective = (
          f"/goal Execute only {record['item_id']} as {record['claim_id']}. "
          "Obey immutable ../claim.json; work only here. Use writable_paths and _baseline. "
          "No parent/canonical/other-task access, child threads, collaboration, clone, fetch, "
          "Lean, Lake or Elan. Validate --no-lean; Master compiles. After all owned files are "
          "complete run python3 _baseline/finalize.py; it writes _outbox/result.json and "
          "../changes.patch. Finish with the completion token "
          f"{token}"
      )
      if len(objective.encode("utf-8")) > 768:
          raise ControllerError("goal objective exceeds the reviewed short-objective limit")
      tmux(record,"load-buffer","-b","goal", "-", input_text=objective); tmux(record,"paste-buffer","-b","goal","-t",f"{record['session']}:0.0")
      record["status"] = "goal_pasted"; record["goal_pasted_at"] = now()
      if on_transition is not None: on_transition(record)
    token = record.get("goal_token")
    if not isinstance(token, str):
        raise ControllerError("goal-pasted state lacks completion token")
    while time.monotonic() < invocation_deadline and time.time() < hard_deadline:
        pane = tmux(record,"capture-pane","-p","-J","-t",f"{record['session']}:0.0",check=False).stdout
        if token in pane: break
        time.sleep(.25)
    else:
        return
    acquire_request_leases(record, prompt)
    # Persist the exact intent *before* Enter.  A crash after this commit is
    # fenced for manual/restart reconciliation and can never paste a second
    # `/goal`; the controller does not pretend that an uncertain Enter did not
    # happen.
    record["status"] = "submission_committed"
    record["submission_committed_at"] = now()
    if on_transition is not None: on_transition(record)
    tmux(record,"send-keys","-t",f"{record['session']}:0.0","Enter")
    record["goal_submissions"] = 1; record["status"] = "goal_submitted"; record["goal_submitted_at"] = now(); append_event("goal_submitted", {k:record[k] for k in ("item_id","claim_id","run_id","socket_path","session","pane_pid","pane_pid_start_ticks","goal_token")})
    if on_transition is not None: on_transition(record)


def private_identity(record: dict[str, Any]) -> dict[str, Any] | None:
    db = Path(record["codex_home"]) / "state_5.sqlite"; goals = Path(record["codex_home"]) / "goals_1.sqlite"
    if not db.is_file() or not goals.is_file(): return None
    try:
        c=sqlite3.connect(f"file:{db}?mode=ro",uri=True); rows=c.execute("select id,cwd,model_provider,model,reasoning_effort from threads order by rowid").fetchall(); c.close()
        if len(rows) != 1:
            return None
        row = rows[0]
        g=sqlite3.connect(f"file:{goals}?mode=ro",uri=True); goal_rows=g.execute("select goal_id,objective,status from thread_goals where thread_id=? order by rowid",(row[0],)).fetchall(); g.close()
        if len(goal_rows) != 1:
            return None
        goal = goal_rows[0]
        return {"thread_id":row[0],"cwd":row[1],"provider":row[2],"model":row[3],"reasoning_effort":row[4],"goal_id":goal[0],"goal_objective":goal[1],"goal_status":goal[2]}
    except sqlite3.Error: return None


def private_registry_cardinality(record: dict[str, Any]) -> tuple[int, int] | None:
    db = Path(record["codex_home"]) / "state_5.sqlite"
    goals = Path(record["codex_home"]) / "goals_1.sqlite"
    if not db.is_file() or not goals.is_file():
        return None
    try:
        c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        thread_count = int(c.execute("select count(*) from threads").fetchone()[0]); c.close()
        g = sqlite3.connect(f"file:{goals}?mode=ro", uri=True)
        goal_count = int(g.execute("select count(*) from thread_goals").fetchone()[0]); g.close()
        return thread_count, goal_count
    except sqlite3.Error:
        return None


def authenticate(record: dict[str, Any]) -> bool:
    pane_pid = int(record["pane_pid"])
    argv = process_cmdline(pane_pid)
    if (process_ticks(pane_pid) != record.get("pane_pid_start_ticks")
            or process_env(pane_pid,"CODEX_HOME") != record["codex_home"]
            or f"-c service_tier={SERVICE_TIER}" not in argv
            or f"-c model_provider={PROVIDER}" not in argv):
        return False
    identity=private_identity(record)
    if not identity or identity["cwd"] != record["work_root"] or identity["provider"] != PROVIDER or identity["model"] != MODEL or identity["reasoning_effort"] != EFFORT or identity["goal_status"] != "active": return False
    if record["item_id"] not in identity["goal_objective"] or record["claim_id"] not in identity["goal_objective"]: return False
    was_live = record.get("status") == "live"
    record.update(identity); record["service_tier"] = SERVICE_TIER; record["status"]="live"
    if not was_live:
        record["authenticated_at"] = now()
        append_event("claim_live", {k:record[k] for k in ("item_id","claim_id","run_id","thread_id","goal_id","pane_pid","provider","model","reasoning_effort","service_tier")})
    return True


def transport_identity_alive(record: dict[str, Any]) -> bool:
    pane_pid = record.get("pane_pid")
    if not isinstance(pane_pid, int):
        return False
    try:
        tmux(record, "has-session", "-t", record["session"], timeout=5)
    except Exception:
        return False
    return (
        process_ticks(pane_pid) == record.get("pane_pid_start_ticks")
        and process_env(pane_pid, "CODEX_HOME") == record.get("codex_home")
    )


def authenticate_with_retry(record: dict[str, Any], timeout_seconds: float = 180.0) -> bool:
    """Wait for delayed private registry writes; never submit another goal."""
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if authenticate(record):
            return True
        time.sleep(1.0)
    return False


def retire_launch_failure(state: dict[str, Any], record: dict[str, Any], error: Exception) -> None:
    """Durably retire a generation whose admission did not authenticate.

    Materialization is itself a state transition.  Keeping that transition in
    the registry before starting tmux means a failed launch cannot reappear as
    an unregistered socket on the next tick.  The exact task root is stopped,
    retained in generation history, and left on disk for audit/recovery.
    """
    prior_status = record.get("status")
    prior_reason = record.get("retired_reason")
    # Terminal goals require a durable typed disposition before transport
    # fencing. Admission failures that never started a goal have no theorem
    # progress to checkpoint and retain the lighter launch record. If the
    # controller cannot emit the receipt, keep the generation pending rather
    # than silently retiring and losing the only recovery evidence.
    must_checkpoint = (
        prior_status in {"generation_retire_required", "terminal_pending_disposition"}
        and (
            int(record.get("goal_submissions", 0) or 0) > 0
            or record.get("goal_status") in {"blocked", "complete", "completed", "failed", "stopped", "paused"}
            or record.get("terminal_reason") in {"goal_terminal", "provider_unavailable", "task_boundary_violation"}
        )
    )
    if must_checkpoint:
        try:
            write_terminal_disposition(record, error)
        except Exception as checkpoint_error:
            record["status"] = "terminal_pending_disposition"
            record["terminal_disposition_error"] = str(checkpoint_error)
            record["retired_reason"] = "terminal_disposition_required_before_retirement"
            state.setdefault("claims", {})[record["item_id"]] = record
            append_event("terminal_disposition_pending", {
                "item_id": record.get("item_id"), "claim_id": record.get("claim_id"),
                "run_id": record.get("run_id"), "error": str(checkpoint_error),
            })
            save_state(state)
            return
    settle_generation_budget(state, record, "generation_retired")
    stop_record(record)
    release_request_leases(record, "launch_failed")
    record["status"] = "retired"
    record["retired_at"] = now()
    record["retired_epoch"] = time.time()
    if prior_status == "generation_retire_required" and prior_reason:
        record["retired_reason"] = str(prior_reason)
    else:
        record["retired_reason"] = f"launch_failed:{error.__class__.__name__}:{error}"
    state.setdefault("generation_history", []).append(dict(record))
    # Keep the exact retired claim until the next generation supersedes its
    # key; it is not eligible for capacity.
    state.setdefault("claims", {})[record["item_id"]] = record
    append_event("generation_retired", {k:record.get(k) for k in ("item_id", "claim_id", "run_id", "retired_reason")})
    save_state(state)


def classify_terminal_pane(pane: str) -> str:
    """Classify a terminal model turn without treating provider faults as work."""
    pane = pane.lower()
    if "selected model is at capacity" in pane:
        return "model_capacity"
    if ("429" in pane or "rate limit" in pane or "too many requests" in pane
            or "503 service unavailable" in pane
            or "service temporarily unavailable" in pane
            or "unexpected status 503" in pane):
        return "provider_unavailable"
    return "goal_terminal"


def terminal_reason(record: dict[str, Any]) -> str:
    pane = ""
    try:
        pane = tmux(record, "capture-pane", "-p", "-J", "-t",
                    f"{record['session']}:0.0", check=False,
                    timeout=5).stdout
    except Exception:
        pass
    return classify_terminal_pane(pane)


def reconcile_record(record: dict[str, Any]) -> str:
    """Promote delayed registry writes or retire a terminal/blocked goal."""
    status = record.get("status")
    if status in {"reserved", "materialized"}:
        return record["status"]
    if status in {"tmux_started", "goal_pasted"} and not transport_identity_alive(record):
        record["status"] = "generation_retire_required"
        record["terminal_reason"] = "starting_transport_lost"
        record["retired_reason"] = "exact_starting_transport_identity_not_alive"
        return record["status"]
    if status == "submission_committed":
        # The Enter boundary is deliberately fail-uncertain: inspect the
        # private registries, but never paste or submit another `/goal`.
        if not transport_identity_alive(record):
            record["status"] = "generation_retire_required"
            record["terminal_reason"] = "submission_commit_transport_lost"
            record["retired_reason"] = "uncertain_goal_submission_fenced"
            return record["status"]
    generation_deadline = record.get("generation_deadline_epoch")
    if isinstance(generation_deadline, (int, float)) and time.time() >= generation_deadline and status in ACTIVE_GENERATION_STATUSES:
        record["status"] = "generation_retire_required"
        record["terminal_reason"] = "generation_lifetime_expired"
        record["retired_reason"] = "goal_lifetime_14_days_expired"
        append_event("generation_retire_required", {k: record.get(k) for k in ("item_id", "claim_id", "run_id", "retired_reason")})
        return record["status"]
    hard_deadline = record.get("startup_deadline_epoch")
    if (
        status in STARTING_GENERATION_STATUSES
        and isinstance(hard_deadline, (int, float))
        and time.time() >= hard_deadline
    ):
        record["status"] = "generation_retire_required"
        record["terminal_reason"] = "startup_deadline_expired"
        record["retired_reason"] = "startup_not_authenticated_before_hard_deadline"
        return record["status"]
    violation = task_boundary_violation(record)
    if violation:
        record["status"] = "generation_retire_required"
        record["terminal_reason"] = "task_boundary_violation"
        record["retired_reason"] = violation
        append_event("generation_retire_required", {k: record.get(k) for k in ("item_id", "claim_id", "run_id", "retired_reason")})
        return record["status"]
    budget_violation = generation_budget_violation(record)
    if budget_violation is not None:
        record["status"] = "generation_retire_required"
        record["terminal_reason"] = "generation_budget_overrun"
        record["retired_reason"] = budget_violation
        append_event("generation_retire_required", {
            "item_id": record.get("item_id"), "claim_id": record.get("claim_id"),
            "run_id": record.get("run_id"), "retired_reason": budget_violation,
        })
        return record["status"]
    identity = private_identity(record)
    if not identity:
        cardinality = private_registry_cardinality(record)
        if record.get("status") == "live" and cardinality not in {None, (1, 1)}:
            record["status"] = "generation_retire_required"
            record["terminal_reason"] = "private_registry_cardinality_violation"
            record["retired_reason"] = (
                f"private_registry_cardinality:threads={cardinality[0]}:goals={cardinality[1]}"
            )
            append_event("generation_retire_required", {
                "item_id": record.get("item_id"), "claim_id": record.get("claim_id"),
                "run_id": record.get("run_id"), "retired_reason": record["retired_reason"],
            })
        return record.get("status", "unknown")
    record.update(identity)
    if identity["goal_status"] == "active":
        if isinstance(record.get("next_retry_at"), (int, float)) and time.time() < record["next_retry_at"]:
            return record.get("status", "goal_submitted")
        if authenticate(record):
            record.pop("next_retry_at", None)
            return "live"
        return record.get("status", "goal_submitted")
    # A paused goal is not an authenticated running turn.  Treat it as a
    # terminal generation for scheduler purposes so the exact transport is
    # fenced and the item can receive a fresh generation; leaving it marked
    # live would consume a concurrency slot indefinitely and could not produce
    # a harvestable result.
    if identity["goal_status"] in {"blocked", "complete", "completed", "failed", "stopped", "paused"}:
        record["status"] = "generation_retire_required"
        # Provider failure is a route binding reason, not completed theorem
        # work. Persist it so the next tick fences the route instead of
        # repeatedly opening fresh tmux generations and model requests.
        reason = terminal_reason(record)
        record["terminal_reason"] = reason
        record["retired_reason"] = f"goal_terminal:{identity['goal_status']}:{reason}"
        append_event("generation_retire_required", {
            "item_id":record["item_id"], "claim_id":record["claim_id"],
            "run_id":record["run_id"], "goal_status":identity["goal_status"],
            "terminal_reason":reason,
        })
    return record["status"]


def stop_record(record: dict[str, Any]) -> None:
    try:
        tmux(record,"kill-server",check=False,timeout=10)
    except Exception:
        pass
    # tmux leaves the pathname socket behind after the server exits.  Remove
    # only this claim's exact task-local socket; never scan or kill a shared
    # tmux namespace.
    socket_value = record.get("socket_argument", "tmux.sock")
    socket_path = Path(record["task_root"]) / socket_value
    try:
        if socket_path.is_socket() and not socket_path.is_symlink():
            socket_path.unlink()
    except OSError:
        pass
    release_request_leases(record, "transport_stopped")
    record["transport_stopped_at"] = now()


def fence_orphaned_generations(state: dict[str, Any]) -> int:
    """Fence task-local tmux generations absent from the durable registry.

    A controller restart must not let an old generation overlap a replacement.
    The scan is strictly confined to this controller's own claim roots and
    never uses host-wide process or tmux enumeration.  Artifacts remain intact;
    only the exact orphan transport is stopped (or its stale socket removed).
    """
    tasks_root = RUNTIME / "tasks"
    if not tasks_root.is_dir():
        return 0
    current = {str(v.get("task_root")): v for v in state.get("claims", {}).values()
               if v.get("status") in ACTIVE_GENERATION_STATUSES | {"generation_retire_required"}}
    fenced = 0
    for claim_dir in sorted(tasks_root.glob("*-worker")):
        if not claim_dir.is_dir():
            continue
        for run_root in sorted(p for p in claim_dir.iterdir() if p.is_dir()):
            if str(run_root) in current:
                continue
            claim_path = run_root / "claim.json"
            socket_path = run_root / "tmux.sock"
            if not claim_path.is_file() or not socket_path.is_socket() or socket_path.is_symlink():
                continue
            try:
                card = json.loads(claim_path.read_text())
                if card.get("claim_id") != claim_dir.name:
                    continue
                record = {"task_root": str(run_root), "socket_argument": "tmux.sock"}
                tmux(record, "kill-server", check=False, timeout=10)
                if socket_path.is_socket() and not socket_path.is_symlink():
                    socket_path.unlink()
                append_event("orphan_generation_fenced", {
                    "item_id": card.get("item_id"), "claim_id": card.get("claim_id"),
                    "run_id": card.get("run_id"), "task_root": str(run_root),
                })
                fenced += 1
            except (OSError, ValueError, json.JSONDecodeError):
                # Ambiguous metadata is left untouched and blocks no other
                # claim; a later validator can classify it for manual repair.
                continue
    return fenced


def build_live_lane_audit(
    state: dict[str, Any], prompt: dict[str, Any] | None, prompt_digest: str | None,
) -> dict[str, Any]:
    """Build exact, sealed identity evidence for every lane counted live."""
    live = [
        record for record in state.get("claims", {}).values()
        if isinstance(record, dict) and record.get("status") == "live"
    ]
    identity_fields = (
        "lane_id", "generation_id", "task_root", "socket_path", "codex_home",
        "session", "thread_id", "goal_id",
    )

    def unique(field: str) -> bool:
        values = [record.get(field) for record in live]
        return all(isinstance(value, str) and value for value in values) and len(set(values)) == len(values)

    failures: dict[str, list[dict[str, Any]]] = {
        "task_boundary": [], "socket": [], "process": [], "registry": [],
        "route": [], "policy": [],
    }
    identities: list[dict[str, Any]] = []
    expected_lifetime = (prompt or {}).get("execution_limits", {}).get("generation_lifetime_seconds")
    tasks_root = RUNTIME / "tasks"
    for record in live:
        ref = {
            "item_id": record.get("item_id"),
            "generation_id": record.get("generation_id") or record.get("run_id"),
        }
        task_root = Path(str(record.get("task_root", "")))
        work_root = Path(str(record.get("work_root", "")))
        codex_home = Path(str(record.get("codex_home", "")))
        socket_path = Path(str(record.get("socket_path", "")))
        try:
            task_local = (
                task_root.relative_to(tasks_root)
                and work_root.parent == task_root
                and codex_home.parent == task_root
                and task_root.is_dir() and work_root.is_dir() and codex_home.is_dir()
            )
        except ValueError:
            task_local = False
        if not task_local:
            failures["task_boundary"].append(ref)
        if (socket_path.parent != task_root or not socket_path.is_socket()
                or socket_path.is_symlink()):
            failures["socket"].append(ref)

        pane_pid = record.get("pane_pid")
        process_ok = isinstance(pane_pid, int) and (
            process_ticks(pane_pid) == record.get("pane_pid_start_ticks")
            and process_env(pane_pid, "CODEX_HOME") == str(codex_home)
        )
        if process_ok:
            try:
                process_ok = Path(f"/proc/{pane_pid}/cwd").resolve() == work_root
            except OSError:
                process_ok = False
        if not process_ok:
            failures["process"].append(ref)

        cardinality = private_registry_cardinality(record)
        identity = private_identity(record)
        registry_ok = (
            cardinality == (1, 1) and isinstance(identity, dict)
            and identity.get("thread_id") == record.get("thread_id")
            and identity.get("goal_id") == record.get("goal_id")
            and identity.get("goal_status") == "active"
            and identity.get("cwd") == str(work_root)
        )
        if not registry_ok:
            failures["registry"].append({**ref, "cardinality": cardinality})

        route_ok = (
            record.get("provider") == PROVIDER and record.get("model") == MODEL
            and record.get("reasoning_effort") == EFFORT
            and record.get("service_tier") == SERVICE_TIER
        )
        if not route_ok:
            failures["route"].append(ref)

        started = record.get("generation_started_at")
        deadline = record.get("generation_deadline_epoch")
        ordinal = record.get("replacement_ordinal")
        lifetime_ok = (
            isinstance(expected_lifetime, int)
            and isinstance(started, (int, float)) and not isinstance(started, bool)
            and isinstance(deadline, (int, float)) and not isinstance(deadline, bool)
            and abs((float(deadline) - float(started)) - expected_lifetime) < 0.001
        )
        policy_ok = (
            record.get("goal_submissions") == 1 and lifetime_ok
            and isinstance(ordinal, int) and not isinstance(ordinal, bool)
            and 0 <= ordinal <= int((record.get("recovery") or {}).get("generation_replacements_per_work_item", -1))
        )
        if not policy_ok:
            failures["policy"].append(ref)
        identities.append({
            **ref, "lane_id": record.get("lane_id"),
            "task_root": str(task_root), "socket_path": str(socket_path),
            "codex_home": str(codex_home), "session": record.get("session"),
            "thread_id": record.get("thread_id"), "goal_id": record.get("goal_id"),
            "goal_submissions": record.get("goal_submissions"),
            "generation_started_at": started, "generation_deadline_epoch": deadline,
            "replacement_ordinal": ordinal, "prompt_digest": record.get("prompt_digest"),
            "provider": record.get("provider"), "model": record.get("model"),
            "reasoning_effort": record.get("reasoning_effort"),
            "service_tier": record.get("service_tier"),
        })

    checks = {f"unique_{field}": unique(field) for field in identity_fields}
    checks.update({
        "task_local_roots": not failures["task_boundary"],
        "task_local_socket": not failures["socket"],
        "exact_process_identity": not failures["process"],
        "exact_private_thread_goal": not failures["registry"],
        "all_default_route": not failures["route"],
        "one_goal_lifetime_replacement_policy": not failures["policy"],
    })
    body = {
        "schema_version": "awesome-theorems/stage5-live-lane-audit/1.0",
        "program": PROGRAM, "generated_at": now(),
        "controller_state_sha256": digest(canonical(state)),
        "prompt_epoch": (prompt or {}).get("policy_epoch"),
        "prompt_digest": prompt_digest,
        "requested_authenticated_goals": (prompt or {}).get("concurrency", {}).get("authenticated_goals"),
        "observed_live": len(live), "checks": checks,
        "all_checks_pass": all(checks.values()), "failures": failures,
        "live_identities": identities, "breaker": state.get("breaker", {"state": "closed"}),
        "underfill": state.get("underfill"),
    }
    return seal(body)


def append_runtime_snapshot(state: dict[str, Any], prompt: dict[str, Any] | None = None, prompt_digest: str | None = None) -> None:
    """Atomically project program-local worker state into the Gantt schema."""
    claims = state.get("claims", {})
    items: dict[str, Any] = {}
    for item_id, value in claims.items():
        status = value.get("status", "unknown")
        worker = {
            "claim_id": value.get("claim_id"), "run_id": value.get("run_id"),
            "owner": "codex-worker", "status": status,
            "startup": status in STARTING_GENERATION_STATUSES,
            "live": status == "live", "running": status == "live",
            "tmux_socket": value.get("socket_path", str(Path(value.get("task_root", "")) / "tmux.sock")),
            "tmux_session": value.get("session"), "codex_home": value.get("codex_home"),
            "thread_id": value.get("thread_id"), "goal_id": value.get("goal_id"),
            "provider": value.get("provider"), "model": value.get("model"),
            "reasoning_effort": value.get("reasoning_effort"), "service_tier": value.get("service_tier"),
            "budget": value.get("budget"), "handoff": value.get("handoff"),
        }
        items[item_id] = {"worker": worker, "block": value.get("underfill"), "integration": value.get("integration"), "repair": value.get("repair"),
                          "timing": {"status": "recorded" if value.get("goal_submitted_at") else "unscheduled", "start": value.get("goal_submitted_at"), "end": value.get("authenticated_at"), "duration_seconds": None, "source": "controller-state" if value.get("goal_submitted_at") else None}}
    active = [v for v in claims.values() if v.get("status") in ACTIVE_GENERATION_STATUSES]
    measured = request_lease_usage(prompt, state) if prompt else {
        "running_turns": 0, "request_starts_per_window": 0, "in_flight_requests": 0,
    }
    observed = {"logical_claims": len(active), "agent_executions": len(active), "starting_lanes": sum(v.get("status") in STARTING_GENERATION_STATUSES for v in active), "live_transports": sum(v.get("status") in TRANSPORT_GENERATION_STATUSES for v in active), "authenticated_live_goals": sum(v.get("status") == "live" for v in active), "running_turns": measured["running_turns"], "request_starts_per_window": measured["request_starts_per_window"], "canonical_integrations": state.get("active_integrations", 0), "lean_build_validators": state.get("active_validators", 0), "external_launches_this_wave": state.get("external_launches_this_wave", 0), "in_flight_requests": measured["in_flight_requests"], "outstanding_requests": measured["in_flight_requests"], "unauthorized_continuations": state.get("unauthorized_continuations", 0), "breaker": state.get("breaker", {"state": "closed"})}
    vector = prompt.get("concurrency") if prompt else None
    live_cap = vector.get("authenticated_goals") if isinstance(vector, dict) and isinstance(vector.get("authenticated_goals"), int) else None
    audit_path = RUNTIME / "status/live-lane-audit.json"
    audit = build_live_lane_audit(state, prompt, prompt_digest)
    atomic_json(audit_path, audit, 0o644)
    body = {"schema_version": "awesome-theorems/stage5-runtime-snapshot/1.0", "program": PROGRAM, "snapshot_id": str(uuid.uuid4()), "generated_at": now(), "state_sha256": digest(canonical(state)), "items": items, "prompt_epoch": prompt.get("policy_epoch") if prompt else None, "prompt_digest": prompt_digest, "requested_concurrency": vector, "effective_concurrency": state.get("effective_concurrency", vector), "observed_usage": observed, "saturated_dimensions": [k for k,v in observed.items() if k in {"logical_claims", "starting_lanes", "authenticated_live_goals", "running_turns"} and isinstance(live_cap, int) and v >= live_cap], "underfill": state.get("underfill", {"authenticated_live_goal_slots": (max(0, live_cap-observed["authenticated_live_goals"]) if isinstance(live_cap, int) else None), "binding_reasons": (["BOOT_not_accepted", "controller_not_activated"] if prompt else ["concurrency_prompt_required"])}), "status_counts": {"live": observed["authenticated_live_goals"], "starting": observed["starting_lanes"]}, "live_lane_audit": {"path": audit_path.relative_to(ROOT).as_posix(), "sha256": file_digest(audit_path), "observed_live": audit["observed_live"], "all_checks_pass": audit["all_checks_pass"]}}
    atomic_json(RUNTIME / "status/runtime-snapshot.json", seal(body), 0o644)
    generator_path = ROOT / "Docs/tools/generate_stage5_theorems_gantt.py"
    spec = importlib.util.spec_from_file_location("stage5_theorem_gantt_projection", generator_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
        module.atomic_write(GANTT, module.render())


def _snapshot_prompt_binding() -> tuple[dict[str, Any] | None, str | None]:
    """Return the sealed prompt for status/stop projections when available."""
    try:
        specification, _, _ = load_program()
        return load_concurrency_prompt(CONCURRENCY_PROMPT, specification)
    except Exception:
        return None, None


def validate_only(concurrency_prompt: Path | None = None) -> dict[str, Any]:
    errors=[]
    try: specification, rows, raw = load_program()
    except Exception as exc: return {"valid":False,"errors":[str(exc)],"program":PROGRAM,"transport":TRANSPORT}
    if concurrency_prompt is None:
        return {"valid": False, "errors": ["concurrency prompt is required"], "program": PROGRAM, "transport": TRANSPORT}
    try:
        prompt, prompt_digest = load_concurrency_prompt(concurrency_prompt, specification)
    except Exception as exc:
        return {"valid": False, "errors": [str(exc)], "program": PROGRAM, "transport": TRANSPORT}
    try:
        validate_claim_schema_prompt_identity()
    except Exception as exc:
        errors.append(str(exc))
    authority = {"materialized": OPERATOR_AUTHORITY.is_file() and OPERATOR_TRUST_ROOT.is_file(), "active_goal": False}
    if authority["materialized"]:
        try:
            binding = validate_operator_authority(specification, prompt, prompt_digest)
            authority.update({"active_goal": True, "authority_sha256": binding["authority"]["authority_sha256"], "goal_id": binding["goal"]["goal_id"]})
        except Exception as exc:
            authority["error"] = str(exc)
            errors.append(str(exc))
    else:
        errors.append("operator authority is not materialized")
    successor_authority = None
    activation_authority = None
    try:
        successor = validate_controller_successor_acceptance(specification)
        successor_authority = successor.get("authority_sha256")
        activation = validate_activation(specification, prompt, prompt_digest)
        activation_authority = activation.get("authority_sha256")
    except Exception as exc:
        errors.append(str(exc))
    return {"valid":not errors,"errors":errors,"program":PROGRAM,"items":len(rows),"targets":3500,"transport":TRANSPORT,"goal_command":"/goal","route":{"provider":PROVIDER,"model":MODEL,"reasoning_effort":EFFORT,"service_tier":SERVICE_TIER},"concurrency_prompt":{"path":str(concurrency_prompt),"digest":prompt_digest,"epoch":prompt.get("policy_epoch"),"requested":prompt["concurrency"]},"operator_authority":authority,"controller_successor_authority_sha256":successor_authority,"activation_authority_sha256":activation_authority,"runtime_presence":RUNTIME.exists()}


def _merge_generation(record: dict[str, Any]) -> None:
    """Durably merge one generation transition under a short global lease."""
    with scheduler_guard(nonblocking=False):
        state = load_state()
        current = state.setdefault("claims", {}).get(record["item_id"])
        if current is not None and current.get("generation_id") != record.get("generation_id"):
            raise ControllerError("generation transition would overwrite another generation")
        state["claims"][record["item_id"]] = dict(record)
        save_state(state)


def _retire_generation(record: dict[str, Any], error: Exception) -> dict[str, Any]:
    with scheduler_guard(nonblocking=False):
        state = load_state()
        current = state.setdefault("claims", {}).get(record["item_id"])
        if current is not None and current.get("generation_id") == record.get("generation_id"):
            record = {**current, **record}
        retire_launch_failure(state, record, error)
    return record


def _reservation_record(
    item: dict[str, Any], ordinal: int, prompt: dict[str, Any],
    prompt_digest: str, startup_deadline_seconds: int, *,
    replacement_ordinal: int, previous_generation_id: str | None,
) -> dict[str, Any]:
    generation_id = f"r-{int(time.time())}-{uuid.uuid4().hex[:8]}"
    claim_id = f"{item['item_id']}--worker"
    root = RUNTIME / "tasks" / claim_id / generation_id
    return {
        "item_id": item["item_id"], "claim_id": claim_id,
        "run_id": generation_id, "generation_id": generation_id,
        "lane_id": item["item_id"], "task_root": str(root),
        "work_root": str(root / "work"), "codex_home": str(root / "codex-home"),
        "socket_path": str(root / "tmux.sock"), "socket_argument": "tmux.sock",
        "session": "s5-" + digest(f"{claim_id}/{generation_id}".encode())[:20],
        "status": "reserved", "goal_submissions": 0, "ordinal": ordinal,
        "owned_paths": list(item["owned_paths"]),
        "prompt_epoch": prompt["policy_epoch"], "prompt_digest": prompt_digest,
        "reserved_at": now(),
        "startup_deadline_epoch": time.time() + startup_deadline_seconds,
        "generation_started_at": now(),
        "generation_deadline_epoch": time.time() + int(prompt["execution_limits"]["generation_lifetime_seconds"]),
        "replacement_ordinal": replacement_ordinal,
        "previous_generation_id": previous_generation_id,
    }


def _launch_workers_pump(
    concurrency_prompt: Path, *, maintenance_intent: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Pump prompt-bounded parallel waves without holding the global lease."""
    invocation_started = time.monotonic()
    specification, rows, raw = load_program()
    prompt, prompt_digest = load_concurrency_prompt(concurrency_prompt, specification)
    validate_claim_schema_prompt_identity()
    if rows[0]["state"] != "x":
        raise ControllerError("BOOT must be Master accepted before worker launch")
    if maintenance_intent is not None:
        if maintenance_intent.get("payload", {}).get("action") != "paused_reconcile_fence_and_refill_only":
            raise ControllerError("controller successor maintenance intent was not prevalidated")
    else:
        validate_activation(specification, prompt, prompt_digest)
    binding = validate_operator_authority(specification, prompt, prompt_digest)
    # Signature/claim replay is intentionally outside the short scheduler
    # lease.  Only the small, prevalidated identity map enters locked state
    # projection and Master receipt reconciliation below.
    revoked_acceptances = semantic_revoked_master_acceptances()
    vector = validate_concurrency_vector(prompt["concurrency"])
    execution_limits, recovery = validate_execution_policy(prompt["execution_limits"], prompt["recovery"])
    fanout = int(vector["launch_fanout_per_wave"])
    tick_budget = int(specification["scheduler"]["tick_budget_seconds"])
    startup_deadline = int(specification["scheduler"]["startup_deadline_seconds"])
    invocation_deadline = invocation_started + tick_budget
    RUNTIME.mkdir(parents=True, exist_ok=True)
    materialize_runtime_authority(binding, specification, prompt, prompt_digest)

    with scheduler_guard():
        state = load_state()
        ensure_budget_accounting(state, binding)
        semantic_revocations_reconciled = reconcile_semantic_revocations(
            state, revoked_acceptances,
        )
        if semantic_revocations_reconciled:
            append_event("semantic_revocations_reconciled", {
                "record_count": semantic_revocations_reconciled,
            })
        breaker_open = provider_breaker_is_open(state)
        # Existing generations remain immutable under their admission prompt;
        # only newly reserved/replacement generations bind the successor
        # prompt.  This is the explicit lifecycle migration boundary.
        prior_prompt_digest = state.get("prompt_digest")
        if prior_prompt_digest not in {None, prompt_digest}:
            state.setdefault("migration", {})["prior_prompt_digest"] = prior_prompt_digest
            state["migration"]["successor_prompt_digest"] = prompt_digest
        rebuilt_retry_schedules = rebuild_provider_retry_schedule(state)
        if rebuilt_retry_schedules:
            append_event("provider_retry_schedule_rebuilt", {
                "record_count": rebuilt_retry_schedules,
                "scope": "per_work_item_consecutive_provider_failures",
            })
        # A producer-only maintenance intent authorizes only control-plane
        # reconcile/fence/refill.  It cannot harvest a worker result or create
        # any canonical integration work.
        harvested = 0 if maintenance_intent is not None else harvest_state(state, specification)
        orphaned = fence_orphaned_generations(state)
        active_records = [
            record for record in state.get("claims", {}).values()
            if record.get("status") in ACTIVE_GENERATION_STATUSES
        ]
        for record in active_records:
            if record.get("status") in ACTIVE_GENERATION_STATUSES:
                reconcile_record(record)
                violation = (
                    pre_goal_replacement_ordinal_violation(state, record)
                    or successor_generation_violation(record, prompt, prompt_digest)
                )
                if violation is not None:
                    record["status"] = "generation_retire_required"
                    record["terminal_reason"] = "successor_generation_migration"
                    record["retired_reason"] = violation
                    append_event("generation_retire_required", {
                        "item_id": record.get("item_id"),
                        "claim_id": record.get("claim_id"),
                        "run_id": record.get("run_id"),
                        "retired_reason": violation,
                    })
        update_provider_breaker_from_records(state, active_records)
        breaker_open = provider_breaker_is_open(state)
        half_open = state.get("breaker", {}).get("state") == "half_open"
        gate_pre_submission_generations_for_breaker(state, breaker_open)
        refresh_half_open_probe_set(state)
        retiring = [
            dict(record) for record in state.get("claims", {}).values()
            if record.get("status") in {"generation_retire_required", "terminal_pending_disposition"}
        ]
        state["requested_concurrency"] = dict(vector)
        state["effective_concurrency"] = dict(vector)
        state["prompt_epoch"] = prompt["policy_epoch"]
        state["prompt_digest"] = prompt_digest
        save_state(state)

    for record in retiring:
        _retire_generation(record, ControllerError(record.get("retired_reason", "retirement required")))

    # Master validation/commit is local canonical work and remains productive
    # while provider admission is paused.  Keep it outside the scheduler lease
    # and before the breaker early-return so harvested handoffs cannot starve.
    integrated = (
        [] if maintenance_intent is not None
        else run_bounded_master_integration(
            int(vector["integration"]), revoked_acceptances,
        )
    )

    # Canonical Master validation and provider admission are independent
    # resources.  Charging slow trust-zero validation against the admission
    # pump's wall clock caused every underfilled tick to reach this point with
    # an already-expired deadline and launch zero workers.  Start the bounded
    # admission window only after the Master phase has durably reconciled.
    invocation_deadline = time.monotonic() + tick_budget

    # Integration can accept an older harvested generation while a newer
    # replacement is still live.  Reload the authoritative cursor before any
    # admission so the same tick cannot refill an already completed work item.
    accepted_generation_retirements: list[dict[str, Any]] = []
    if maintenance_intent is None:
        accepted_ids = accepted_item_ids_from_blueprint()
        with scheduler_guard():
            state = load_state()
            accepted_generation_retirements = retire_generations_for_master_accepted_items(
                state, accepted_ids,
            )
        for record in accepted_generation_retirements:
            finalize_master_accepted_retirement(record)
        if integrated or accepted_generation_retirements:
            specification, rows, raw = load_program()

    if breaker_open:
        with scheduler_guard():
            state = load_state()
            usage = concurrency_usage(state, prompt)
            state["underfill"] = {
                "authenticated_live_goal_slots": max(
                    0, int(vector["authenticated_goals"]) - usage["authenticated_goals"],
                ),
                "binding_reasons": ["provider_breaker_open"],
            }
            append_runtime_snapshot(state, prompt, prompt_digest)
            save_state(state)
            claims = [
                dict(record) for record in state.get("claims", {}).values()
                if record.get("status") in ACTIVE_GENERATION_STATUSES
            ]
        return {
            "valid": True, "launched": 0, "waves": 0, "claims": claims,
            "orphaned_fenced": orphaned, "harvested": harvested,
            "integrated": len(integrated),
            "prompt_digest": prompt_digest, "requested_concurrency": dict(vector),
            "effective_concurrency": dict(vector), "observed_usage": usage,
            "binding_reasons": ["provider_breaker_open"],
        }

    row_by_id = {row["item_id"]: row for row in rows}
    claimable = claimable_item_ids(specification, rows)
    launched_ids: set[str] = set()
    wave_count = 0
    binding_reasons: list[str] = []

    def advance(record: dict[str, Any]) -> dict[str, Any]:
        try:
            item = row_by_id[record["item_id"]]
            if record.get("status") == "reserved":
                materialized = materialize_claim(
                    item, specification, raw, int(record["ordinal"]),
                    prompt=prompt, prompt_digest=prompt_digest,
                    resolved_concurrency=vector,
                    concurrency_prompt_path=concurrency_prompt,
                    generation_id=record["generation_id"],
                    lane_id=record["lane_id"],
                    replacement_ordinal=int(record["replacement_ordinal"]),
                    previous_generation_id=record.get("previous_generation_id"),
                )
                record = {**record, **materialized}
                _merge_generation(record)
            submit_goal(
                record, prompt, on_transition=_merge_generation,
                invocation_deadline=invocation_deadline,
            )
            if record.get("status") in {"goal_submitted", "submission_committed"}:
                remaining = min(
                    5.0,
                    max(0.0, invocation_deadline - time.monotonic()),
                    max(0.0, float(record["startup_deadline_epoch"]) - time.time()),
                )
                if remaining > 0 and authenticate_with_retry(record, remaining):
                    _merge_generation(record)
            return record
        except Exception as exc:
            record["launch_error"] = str(exc)
            return _retire_generation(record, exc)

    no_progress = 0
    while time.monotonic() < invocation_deadline:
        retiring_between_waves: list[dict[str, Any]] = []
        breaker_open_between_waves = False
        with scheduler_guard():
            state = load_state()
            active_records = [
                record for record in state.get("claims", {}).values()
                if record.get("status") in ACTIVE_GENERATION_STATUSES
            ]
            for record in active_records:
                if record.get("status") in ACTIVE_GENERATION_STATUSES:
                    reconcile_record(record)
                if record.get("status") in {"generation_retire_required", "terminal_pending_disposition"}:
                    retiring_between_waves.append(dict(record))
            update_provider_breaker_from_records(state, active_records)
            retiring_between_waves = [
                dict(record) for record in state.get("claims", {}).values()
                if record.get("status") in {"generation_retire_required", "terminal_pending_disposition"}
            ]
            breaker_open_between_waves = provider_breaker_is_open(state)
            half_open_between_waves = state.get("breaker", {}).get("state") == "half_open"
            if gate_pre_submission_generations_for_breaker(state, breaker_open_between_waves):
                retiring_between_waves = [
                    dict(record) for record in state.get("claims", {}).values()
                    if record.get("status") in {"generation_retire_required", "terminal_pending_disposition"}
                ]
            refresh_half_open_probe_set(state)
            if retiring_between_waves or breaker_open_between_waves:
                save_state(state)
            if breaker_open_between_waves:
                binding_reasons = ["provider_breaker_open"]
                wave = []
            elif half_open_between_waves and state.get("breaker", {}).get("probe_generation_ids"):
                binding_reasons = ["provider_breaker_half_open_probe_pending"]
                wave = []
            elif retiring_between_waves:
                wave = []
            else:
                active = [
                    dict(record) for record in state.get("claims", {}).values()
                    if record.get("status") in ACTIVE_GENERATION_STATUSES
                ]
                live_before = sum(record.get("status") == "live" for record in active)
                if live_before >= int(vector["authenticated_goals"]):
                    binding_reasons = ["authenticated_goal_target_reached"]
                    save_state(state)
                    wave = []
                else:
                    recoverable_starting = [
                        record for record in active
                        if record.get("status") in {
                            "reserved", "materialized", "tmux_started", "goal_pasted",
                        }
                    ]
                    if recoverable_starting:
                        wave = recoverable_starting[:fanout]
                    else:
                        slots, _, capacity_reasons = admission_availability(state, prompt)
                        if slots <= 0:
                            binding_reasons = capacity_reasons or ["no_admission_capacity"]
                            save_state(state)
                            wave = []
                        else:
                            active_ids = {record["item_id"] for record in active}
                            projection = dag_projection(rows, active_ids)
                            already_claimed = {
                                record.get("item_id") for record in state.get("claims", {}).values()
                                if record.get("status") in ACTIVE_GENERATION_STATUSES | {"generation_retire_required"}
                            }
                            owned = [record.get("owned_paths", []) for record in active]
                            selected: list[dict[str, Any]] = []
                            retry_backoff_blocked = 0
                            replacement_exhausted = 0
                            for item_id in projection["dependency_clear_frontier"]:
                                if item_id not in claimable or item_id in already_claimed:
                                    continue
                                item = row_by_id[item_id]
                                if any(paths_conflict(item["owned_paths"], paths) for paths in (*owned, *(x["owned_paths"] for x in selected))):
                                    continue
                                if not replacement_admissible(state, item_id, recovery["generation_replacements_per_work_item"]):
                                    replacement_exhausted += 1
                                    continue
                                next_retry_at = next_retry_at_for_item(state, item_id)
                                if isinstance(next_retry_at, float) and time.time() < next_retry_at:
                                    retry_backoff_blocked += 1
                                    continue
                                selected.append(item)
                                if len(selected) >= min(slots, fanout):
                                    break
                            if not selected:
                                if retry_backoff_blocked:
                                    binding_reasons = ["per_item_retry_backoff_pending"]
                                elif replacement_exhausted:
                                    binding_reasons = ["per_item_replacement_budget_exhausted"]
                                else:
                                    binding_reasons = ["dependency_claimability_or_exact_path_frontier_empty"]
                                save_state(state)
                                wave = []
                            else:
                                wave = []
                                base_ordinal = len(state.get("generation_history", [])) + len(state.get("claims", {}))
                                for offset, item in enumerate(selected, 1):
                                    reservation = _reservation_record(
                                        item, base_ordinal + offset, prompt, prompt_digest,
                                        startup_deadline,
                                        replacement_ordinal=next_replacement_ordinal(state, item["item_id"]),
                                        previous_generation_id=previous_generation_id_for_item(state, item["item_id"]),
                                    )
                                    reserve_generation_budget(state, reservation, binding)
                                    state.setdefault("claims", {})[item["item_id"]] = reservation
                                    state.setdefault("reservations", []).append({
                                        key: reservation[key] for key in (
                                            "lane_id", "generation_id", "prompt_epoch",
                                            "prompt_digest", "status", "reserved_at",
                                        )
                                    })
                                    wave.append(dict(reservation))
                                    launched_ids.add(item["item_id"])
                                if half_open_between_waves:
                                    probe_ids = [record["generation_id"] for record in wave]
                                    state.setdefault("breaker", {})["probe_generation_ids"] = probe_ids
                                    state["breaker"]["probe_wave_reserved_at"] = time.time()
                                    for record in wave:
                                        record["breaker_probe"] = True
                                        state["claims"][record["item_id"]]["breaker_probe"] = True
                                save_state(state)

        for record in retiring_between_waves:
            _retire_generation(
                record, ControllerError(record.get("retired_reason", "retirement required")),
            )
        if breaker_open_between_waves or (binding_reasons and not wave):
            break
        if retiring_between_waves:
            continue

        wave_count += 1
        with ThreadPoolExecutor(
            max_workers=max(1, min(fanout, len(wave))),
            thread_name_prefix="stage5-admit",
        ) as executor:
            results = list(executor.map(advance, wave))
        if half_open_between_waves:
            binding_reasons = ["provider_breaker_half_open_probe_pending"]
            break
        live_after = sum(record.get("status") == "live" for record in results)
        durable_progress = any(
            record.get("status") not in {"reserved", "materialized", "tmux_started", "goal_pasted"}
            for record in results
        )
        if live_after <= live_before and not durable_progress:
            no_progress += 1
        else:
            no_progress = 0
        if no_progress >= 2:
            binding_reasons = ["startup_no_progress_before_next_tick"]
            break

    if time.monotonic() >= invocation_deadline and not binding_reasons:
        binding_reasons = ["tick_budget_exhausted"]
    with scheduler_guard():
        state = load_state()
        usage = concurrency_usage(state, prompt)
        state["underfill"] = {
            "authenticated_live_goal_slots": max(
                0, int(vector["authenticated_goals"]) - usage["authenticated_goals"],
            ),
            "binding_reasons": binding_reasons,
        }
        state["last_wave_count"] = wave_count
        state["external_launches_this_wave"] = len(launched_ids)
        append_runtime_snapshot(state, prompt, prompt_digest)
        save_state(state)
        claims = [
            dict(record) for record in state.get("claims", {}).values()
            if record.get("status") in ACTIVE_GENERATION_STATUSES
        ]
    return {
        "valid": True, "launched": len(launched_ids), "waves": wave_count,
        "claims": claims, "orphaned_fenced": orphaned, "harvested": harvested,
        "integrated": len(integrated),
        "prompt_digest": prompt_digest, "requested_concurrency": dict(vector),
        "effective_concurrency": dict(vector), "observed_usage": usage,
        "binding_reasons": binding_reasons,
    }


def launch_workers(concurrency_prompt: Path) -> dict[str, Any]:
    with admission_pump_guard():
        return _launch_workers_pump(concurrency_prompt)


def maintenance_refill(concurrency_prompt: Path) -> dict[str, Any]:
    """Consume a signed paused maintenance intent for one bounded refill."""
    with admission_pump_guard():
        intent = validate_controller_successor_maintenance_intent()
        consumption = consume_controller_successor_maintenance_intent(intent)
        result = _launch_workers_pump(concurrency_prompt, maintenance_intent=intent)
    specification, _, _ = load_program()
    prompt, prompt_digest = load_concurrency_prompt(concurrency_prompt, specification)
    state = load_state(False)
    audit = build_live_lane_audit(state, prompt, prompt_digest)
    if audit["observed_live"] != 24 or not audit["all_checks_pass"]:
        raise ControllerError("successor maintenance refill did not reach exact all-green 24/24")
    return {
        **result,
        "maintenance_intent_consumed": True,
        "maintenance_consumption_authority_sha256": consumption["authority_sha256"],
        "post_live_audit": audit,
    }


def _legacy_launch_workers_locked() -> dict[str, Any]:
    raise ControllerError("legacy serial admission path is retired; use prompt-bound launch_workers")

def retire_failed_runtime() -> None:
    """Archive an admission attempt that produced no authenticated claim."""
    if not RUNTIME.exists():
        return
    state = load_state(False)
    active = [v for v in state.get("claims", {}).values()
              if v.get("status") in ACTIVE_GENERATION_STATUSES | {"generation_retire_required"}]
    if active:
        raise ControllerError("failed runtime contains active durable claims; use controller reconciliation")
    archive = RUNTIME.with_name(RUNTIME.name + "-retired-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    os.rename(RUNTIME, archive)


def status() -> dict[str, Any]:
    with scheduler_guard():
        return _status_locked()


def _status_locked() -> dict[str, Any]:
    state=load_state(False)
    if not RUNTIME.exists():
        return {
            "program": PROGRAM, "transport": TRANSPORT, "claims": [], "live": 0,
            "orphaned_fenced": 0, "harvested": 0, "integrated": [],
            "repair_backlog": 0, "concurrency_prompt_required": True,
        }
    # Status is strictly observational. Harvest, liveness reconciliation,
    # integration, fencing, state writes, and Gantt/audit projection belong to
    # the scheduler tick; an observer must never hold the short state lock over
    # those potentially long operations.
    claims=list(state.get("claims",{}).values())
    repair_dir = integration_repair_dir()
    repair_backlog = len(list(repair_dir.glob("*.json"))) if repair_dir.is_dir() else 0
    return {"program":PROGRAM,"transport":TRANSPORT,"claims":claims,"live":sum(c.get("status")=="live" for c in claims),"orphaned_fenced":0,"harvested":0,"integrated":[],"repair_backlog":repair_backlog,"concurrency_prompt_required":True}


def stop() -> dict[str, Any]:
    with scheduler_guard():
        return _stop_locked()


def _stop_locked() -> dict[str, Any]:
    state=load_state(False); n=0
    for rec in state.get("claims",{}).values():
        if rec.get("status") in ACTIVE_GENERATION_STATUSES | {"generation_retire_required"}: stop_record(rec); rec["status"]="stopped"; n+=1
    if RUNTIME.exists():
        # Process fencing is the safety-critical state.  Persist it before a
        # generated observability projection that may reject superseded
        # Blueprint bytes during an authority migration.
        save_state(state)
        prompt, prompt_digest = _snapshot_prompt_binding()
        append_runtime_snapshot(state, prompt, prompt_digest)
        save_state(state)
    return {"stopped":n}


def main() -> int:
    parser=argparse.ArgumentParser(); group=parser.add_mutually_exclusive_group(required=True); group.add_argument("--validate-only",action="store_true"); group.add_argument("--activate",action="store_true"); group.add_argument("--launch-workers",action="store_true"); group.add_argument("--maintenance-refill",action="store_true"); group.add_argument("--tick",action="store_true"); group.add_argument("--status",action="store_true"); group.add_argument("--stop",action="store_true")
    parser.add_argument("--concurrency-prompt", type=Path)
    args=parser.parse_args()
    try:
        if args.validate_only:
            result = validate_only(args.concurrency_prompt)
        elif args.activate:
            if args.concurrency_prompt is None: raise ControllerError("concurrency prompt is required")
            result = activate(args.concurrency_prompt)
        elif args.maintenance_refill:
            if args.concurrency_prompt is None: raise ControllerError("concurrency prompt is required")
            result = maintenance_refill(args.concurrency_prompt)
        elif args.launch_workers or args.tick:
            if args.concurrency_prompt is None: raise ControllerError("concurrency prompt is required")
            result = launch_workers(args.concurrency_prompt)
        elif args.status:
            result = status()
        else:
            result = stop()
    except (ControllerError,OSError,sqlite3.Error) as exc: print(json.dumps({"valid":False,"error":str(exc)})); return 1
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))
    return 0 if result.get("valid", True) is not False else 1


if __name__ == "__main__": raise SystemExit(main())
