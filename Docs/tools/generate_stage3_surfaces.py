#!/usr/bin/env python3
"""Atomically generate the Stage3 v3 Status, Kanban, and same-name Gantt."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
import errno
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "Docs" / "tools" / "check_stage3_blueprint.py"
SPEC = importlib.util.spec_from_file_location("stage3_checker_for_generator", CHECKER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import Stage3 checker")
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)

BLUEPRINT = ROOT / "Docs" / "Stage3_Blueprint.md"
GANTT = CHECKER.gantt_companion_path(BLUEPRINT)
STATUS = ROOT / "Docs" / "Stage3_Status.json"
KANBAN = ROOT / "Docs" / "Stage3_Kanban.md"
CLEANUP_RECEIPT = CHECKER.CLEANUP_RECEIPT
OUTPUT_ORDER = (STATUS, KANBAN, GANTT)
PROJECTION_LOCK_TARGET = ROOT


@dataclass(frozen=True)
class ProjectionInputSnapshot:
    """Exact bytes whose validated state determines one projection commit."""

    runtime_path: Path | None
    blueprint_bytes: bytes
    runtime_snapshot_bytes: bytes | None
    cleanup_receipt_bytes: bytes | None
    pre_cleanup_receipt_bytes: bytes | None
    cleanup_verifier_script_bytes: bytes | None

    @property
    def blueprint_text(self) -> str:
        return self.blueprint_bytes.decode("utf-8")

    @property
    def runtime_snapshot_text(self) -> str | None:
        if self.runtime_snapshot_bytes is None:
            return None
        return self.runtime_snapshot_bytes.decode("utf-8")

    @property
    def cleanup_receipt_text(self) -> str | None:
        if self.cleanup_receipt_bytes is None:
            return None
        return self.cleanup_receipt_bytes.decode("utf-8")

    @property
    def pre_cleanup_receipt_text(self) -> str | None:
        if self.pre_cleanup_receipt_bytes is None:
            return None
        return self.pre_cleanup_receipt_bytes.decode("utf-8")


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _metadata_block(metadata: dict[str, Any]) -> list[str]:
    return [
        CHECKER.METADATA_BEGIN,
        "```json",
        *json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=False).splitlines(),
        "```",
        CHECKER.METADATA_END,
    ]


def _monitor_cell(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    # Keep Markdown table and code-span delimiters structural while preserving JSON value semantics.
    encoded = encoded.replace("|", "\\u007c").replace("`", "\\u0060")
    return f"`{encoded}`"


def _render_ids(values: list[str], *, suffixes: dict[str, str] | None = None) -> list[str]:
    if not values:
        return ["_None._"]
    suffixes = suffixes or {}
    return [f"- `{item_id}`{suffixes.get(item_id, '')}" for item_id in values]


def generate_status(
    tasks: dict[str, Any],
    metadata: dict[str, Any],
    runtime_snapshot: dict[str, Any] | None,
    cleanup_receipt: dict[str, Any] | None = None,
) -> str:
    payload = {
        "schema_version": CHECKER.STATUS_SCHEMA,
        "authority_note": "Generated read-only projection; Docs/Stage3_Blueprint.md is the only checklist authority.",
        "metadata": metadata,
        "counts": CHECKER._expected_counts(tasks),
        "planning": CHECKER.planning_projection(tasks),
        "runtime": CHECKER.expected_runtime_projection(runtime_snapshot, cleanup_receipt),
        "items": CHECKER.expected_status_items(tasks, runtime_snapshot),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def _runtime_item_groups(items: list[dict[str, Any]]) -> dict[str, list[str]]:
    return {
        "starting": [item["id"] for item in items if item["startup"] is not None and item["live"] is not True],
        "live": [item["id"] for item in items if item["live"] is True],
        "handoff": [item["id"] for item in items if item["handoff"] is not None],
        "integration": [item["id"] for item in items if item["integration"] is not None],
        "repair": [item["id"] for item in items if item["repair"] is not None],
        "runtime_blocked": [item["id"] for item in items if item["runtime_block"] is not None],
    }


def generate_kanban(
    tasks: dict[str, Any],
    metadata: dict[str, Any],
    runtime_snapshot: dict[str, Any] | None,
    cleanup_receipt: dict[str, Any] | None = None,
) -> str:
    planning = CHECKER.planning_projection(tasks)
    items = CHECKER.expected_status_items(tasks, runtime_snapshot)
    item_by_id = {item["id"]: item for item in items}
    runtime = CHECKER.expected_runtime_projection(runtime_snapshot, cleanup_receipt)
    groups = _runtime_item_groups(items)
    planning_blocked_ids = [entry["id"] for entry in planning["dependency_blocked"]]
    planning_suffixes = {
        entry["id"]: " — blockers: " + ", ".join(f"`{dependency}`" for dependency in entry["blockers"])
        for entry in planning["dependency_blocked"]
    }
    runtime_suffixes = {
        item_id: " — " + _monitor_cell(item_by_id[item_id]["runtime_block"])
        for item_id in groups["runtime_blocked"]
    }
    integration_ids = list(
        dict.fromkeys(planning["frontiers"]["integration_ready"] + groups["integration"])
    )
    integration_suffixes: dict[str, str] = {}
    for item_id in integration_ids:
        labels: list[str] = []
        if item_id in planning["frontiers"]["integration_ready"]:
            labels.append("planning integration-ready")
        if item_by_id[item_id]["integration"] is not None:
            labels.append("runtime " + _monitor_cell(item_by_id[item_id]["integration"]))
        integration_suffixes[item_id] = " — " + "; ".join(labels)
    lines = [
        "# Stage3 Worker Kanban",
        "",
        f"> Generated read-only view for `{CHECKER.VERSION}`; this is not a second checklist or completion authority.",
        "> Planning blockers are derived from the Blueprint DAG. Runtime blocks come only from a validated runtime snapshot.",
        "",
        *_metadata_block(metadata),
        "",
        "## Runtime snapshot",
        "",
    ]
    if runtime_snapshot is None:
        lines.append(
            "`runtime_unavailable`; every worker runtime count and lifecycle value is `null`, never an invented zero. "
            f"Terminal `cleanup_state` is `{runtime['cleanup_state']}` from the optional durable cleanup receipt."
        )
    else:
        lines.append(
            f"Observed runtime snapshot {_monitor_cell(runtime['snapshot_id'])} "
            f"at {_monitor_cell(runtime['observed_at'])}."
        )
    lines.extend(["", "| Runtime field | Value |", "|---|---:|"])
    for key in CHECKER.KANBAN_RUNTIME_FIELDS:
        lines.append(f"| `{key}` | {_monitor_cell(runtime[key])} |")
    lines.append(f"| `cleanup_state` | {_monitor_cell(runtime['cleanup_state'])} |")
    lines.extend(
        [
            "",
            "## Implementation-ready",
            "",
            *_render_ids(planning["frontiers"]["implementation_ready"]),
            "",
            "## Validation-preparation",
            "",
            *_render_ids(planning["frontiers"]["validation_preparation"]),
            "",
            "## Starting",
            "",
            *_render_ids(groups["starting"]),
            "",
            "## Live",
            "",
            *_render_ids(groups["live"]),
            "",
            "## Handoff",
            "",
            *_render_ids(groups["handoff"]),
            "",
            "## Integration",
            "",
            *_render_ids(integration_ids, suffixes=integration_suffixes),
            "",
            "## Repair",
            "",
            *_render_ids(groups["repair"]),
            "",
            "## Planning-blocked",
            "",
            *_render_ids(planning_blocked_ids, suffixes=planning_suffixes),
            "",
            "## Runtime-blocked",
            "",
            *_render_ids(groups["runtime_blocked"], suffixes=runtime_suffixes),
            "",
            "## Accepted",
            "",
            *_render_ids(planning["accepted"]),
            "",
            "## Lifecycle vocabulary",
            "",
            "`reserved -> materialized -> tmux_started -> goal_pasted -> goal_submitted -> live -> handoff_ready -> finished`",
            "",
        ]
    )
    return "\n".join(lines)


def generate_gantt(
    tasks: dict[str, Any],
    metadata: dict[str, Any],
    runtime_snapshot: dict[str, Any] | None,
) -> str:
    items = CHECKER.expected_status_items(tasks, runtime_snapshot)
    milestone_time = metadata["generated_at"].removesuffix("Z")
    recorded_items = [item for item in items if item["timing"]["status"] == "recorded"]
    unscheduled_count = sum(item["timing"]["status"] == "unscheduled" for item in items)
    if unscheduled_count == len(items):
        timing_summary = (
            f"Every task is `unscheduled` in this {len(items)}-item snapshot because neither the Blueprint "
            "nor a runtime ledger records a trustworthy task date or operator-frozen estimate."
        )
    else:
        timing_summary = (
            f"{unscheduled_count} tasks are `unscheduled`; {len(items) - unscheduled_count} tasks carry only "
            "recorded timing from the bound runtime snapshot."
        )
    mermaid_lines = [
        "```mermaid",
        "gantt",
        "    title Stage3 recorded projection and task timing",
        "    dateFormat YYYY-MM-DDTHH:mm:ss",
        "    axisFormat %Y-%m-%d %H:%M",
        "    section Projection",
        f"    Projection snapshot generated :milestone, projection, {milestone_time}, 0s",
    ]
    if recorded_items:
        mermaid_lines.append("    section Recorded task timing")
        for item in recorded_items:
            timing = item["timing"]
            mermaid_id = "timing_" + item["id"].lower().replace("-", "_")
            start = timing["start"].removesuffix("Z")
            if timing["end"] is not None:
                endpoint = timing["end"].removesuffix("Z")
                mermaid_lines.append(f"    {item['id']} :{mermaid_id}, {start}, {endpoint}")
            elif timing["duration_seconds"] is not None:
                mermaid_lines.append(
                    f"    {item['id']} :{mermaid_id}, {start}, {timing['duration_seconds']}s"
                )
            else:
                mermaid_lines.append(
                    f"    {item['id']} start observed :milestone, {mermaid_id}, {start}, 0s"
                )
    mermaid_lines.append("```")
    lines = [
        "# Stage3 Full Claim-List Completion and Isolated Execution Gantt",
        "",
        f"> Mandatory same-name read-only schedule and complete worker Kanban monitoring projection for `{CHECKER.VERSION}`.",
        "> `Docs/Stage3_Blueprint.md` is the only mutable checklist authority; regenerate this file instead of editing it.",
        "",
        *_metadata_block(metadata),
        "",
        "## Renderable generation milestone",
        "",
        "Every renderable row below comes from the projection timestamp or an exact recorded runtime timing object; it is never an inferred task estimate.",
        "",
        *mermaid_lines,
        "",
        "## Unscheduled task timing",
        "",
        timing_summary,
        "The complete timing object remains visible in each monitoring row; no calendar interval is inferred from document order, category, dependency depth, or generation time.",
        "",
        "## Complete monitoring index",
        "",
        "Each stable checklist ID has exactly one row. `Planning blockers` are unresolved Blueprint dependencies; `Runtime block` is independent and remains `null` when runtime is unavailable.",
        "",
        CHECKER.GANTT_MONITOR_BEGIN,
        CHECKER.MONITOR_HEADER,
        CHECKER.MONITOR_SEPARATOR,
    ]
    field_names = (
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
    )
    for item in items:
        lines.append("| " + " | ".join(_monitor_cell(item[field]) for field in field_names) + " |")
    lines.extend([CHECKER.GANTT_MONITOR_END, ""])
    return "\n".join(lines)


def _validated_inputs(
    runtime_snapshot_text: str | None,
    cleanup_receipt_text: str | None,
    *,
    blueprint_text: str | None = None,
    pre_cleanup_receipt_text: str | None = None,
    cleanup_verifier_script_bytes: bytes | None = None,
    enforce_current_runtime: bool = False,
) -> tuple[str, dict[str, Any], dict[str, Any] | None, dict[str, Any] | None]:
    if runtime_snapshot_text is not None and cleanup_receipt_text is not None:
        raise CHECKER.ValidationError(
            "terminal cleanup receipt requires the canonical controller runtime snapshot to be absent"
        )
    if blueprint_text is None:
        blueprint_text = BLUEPRINT.read_bytes().decode("utf-8")
    tasks = CHECKER.parse_tasks(blueprint_text)
    CHECKER.validate_graph(tasks)
    CHECKER.validate_ownership(tasks)
    CHECKER.validate_blueprint_contract(blueprint_text, tasks)
    runtime_snapshot = None
    if runtime_snapshot_text is not None:
        runtime_snapshot = CHECKER.parse_runtime_snapshot(
            runtime_snapshot_text,
            tasks,
            blueprint_text,
            pre_cleanup_receipt_text=pre_cleanup_receipt_text,
        )
        if enforce_current_runtime:
            CHECKER.validate_runtime_fresh_now(runtime_snapshot, blueprint_text)
    cleanup_receipt = None
    if cleanup_receipt_text is not None:
        cleanup_receipt = CHECKER.parse_cleanup_receipt(
            cleanup_receipt_text,
            blueprint_text,
            tasks,
            pre_cleanup_receipt_text=pre_cleanup_receipt_text,
            verifier_script_bytes=cleanup_verifier_script_bytes,
        )
    return blueprint_text, tasks, runtime_snapshot, cleanup_receipt


def expected_outputs(
    *,
    generated_at: str,
    runtime_snapshot_text: str | None = None,
    cleanup_receipt_text: str | None = None,
    blueprint_text: str | None = None,
    pre_cleanup_receipt_text: str | None = None,
    cleanup_verifier_script_bytes: bytes | None = None,
    enforce_current_runtime: bool = False,
) -> dict[Path, str]:
    blueprint_text, tasks, runtime_snapshot, cleanup_receipt = _validated_inputs(
        runtime_snapshot_text,
        cleanup_receipt_text,
        blueprint_text=blueprint_text,
        pre_cleanup_receipt_text=pre_cleanup_receipt_text,
        cleanup_verifier_script_bytes=cleanup_verifier_script_bytes,
        enforce_current_runtime=enforce_current_runtime,
    )
    runtime_sha = None if runtime_snapshot_text is None else CHECKER.sha256_text(runtime_snapshot_text)
    runtime_id = None if runtime_snapshot is None else runtime_snapshot["snapshot_id"]
    cleanup_sha = None if cleanup_receipt_text is None else CHECKER.sha256_text(cleanup_receipt_text)
    cleanup_id = None if cleanup_receipt is None else cleanup_receipt["receipt_id"]
    metadata = CHECKER.build_projection_metadata(
        blueprint_text,
        generated_at,
        runtime_snapshot_sha256=runtime_sha,
        runtime_snapshot_id=runtime_id,
        cleanup_receipt_sha256=cleanup_sha,
        cleanup_receipt_id=cleanup_id,
    )
    outputs = {
        STATUS: generate_status(tasks, metadata, runtime_snapshot, cleanup_receipt),
        KANBAN: generate_kanban(tasks, metadata, runtime_snapshot, cleanup_receipt),
        GANTT: generate_gantt(tasks, metadata, runtime_snapshot),
    }
    CHECKER.validate_texts(
        blueprint_text,
        outputs[GANTT],
        outputs[STATUS],
        outputs[KANBAN],
        runtime_snapshot_text,
        cleanup_receipt_text,
        pre_cleanup_receipt_text,
        cleanup_verifier_script_bytes,
    )
    return outputs


def _target_projection_digest(
    runtime_snapshot_text: str | None,
    cleanup_receipt_text: str | None,
    generated_at: str,
    *,
    blueprint_text: str | None = None,
    pre_cleanup_receipt_text: str | None = None,
    cleanup_verifier_script_bytes: bytes | None = None,
) -> str:
    blueprint_text, _tasks, runtime_snapshot, cleanup_receipt = _validated_inputs(
        runtime_snapshot_text,
        cleanup_receipt_text,
        blueprint_text=blueprint_text,
        pre_cleanup_receipt_text=pre_cleanup_receipt_text,
        cleanup_verifier_script_bytes=cleanup_verifier_script_bytes,
    )
    runtime_sha = None if runtime_snapshot_text is None else CHECKER.sha256_text(runtime_snapshot_text)
    runtime_id = None if runtime_snapshot is None else runtime_snapshot["snapshot_id"]
    cleanup_sha = None if cleanup_receipt_text is None else CHECKER.sha256_text(cleanup_receipt_text)
    cleanup_id = None if cleanup_receipt is None else cleanup_receipt["receipt_id"]
    return CHECKER.build_projection_metadata(
        blueprint_text,
        generated_at,
        runtime_snapshot_sha256=runtime_sha,
        runtime_snapshot_id=runtime_id,
        cleanup_receipt_sha256=cleanup_sha,
        cleanup_receipt_id=cleanup_id,
    )["projection_input_sha256"]


def _existing_gantt_metadata() -> dict[str, Any] | None:
    try:
        return CHECKER.parse_surface_metadata(GANTT.read_bytes().decode("utf-8"), "Gantt")
    except (OSError, UnicodeDecodeError, CHECKER.ValidationError):
        return None


def choose_generation_time(
    runtime_snapshot_text: str | None,
    cleanup_receipt_text: str | None = None,
    *,
    blueprint_text: str | None = None,
    pre_cleanup_receipt_text: str | None = None,
    cleanup_verifier_script_bytes: bytes | None = None,
) -> str:
    """Reuse the committed snapshot time when inputs are unchanged; otherwise use now."""

    existing = _existing_gantt_metadata()
    if existing is None:
        return _utc_now()
    try:
        existing_gantt = GANTT.read_bytes().decode("utf-8")
        existing_status = STATUS.read_bytes().decode("utf-8")
        existing_kanban = KANBAN.read_bytes().decode("utf-8")
        CHECKER.validate_texts(
            BLUEPRINT.read_bytes().decode("utf-8") if blueprint_text is None else blueprint_text,
            existing_gantt,
            existing_status,
            existing_kanban,
            runtime_snapshot_text,
            cleanup_receipt_text,
            pre_cleanup_receipt_text,
            cleanup_verifier_script_bytes,
        )
        target_digest = _target_projection_digest(
            runtime_snapshot_text,
            cleanup_receipt_text,
            existing["generated_at"],
            blueprint_text=blueprint_text,
            pre_cleanup_receipt_text=pre_cleanup_receipt_text,
            cleanup_verifier_script_bytes=cleanup_verifier_script_bytes,
        )
    except (OSError, UnicodeDecodeError, CHECKER.ValidationError):
        return _utc_now()
    if existing.get("projection_input_sha256") == target_digest:
        return existing["generated_at"]
    return _utc_now()


@contextmanager
def _projection_writer_lock():
    """Serialize projection writers without recreating runtime state after cleanup."""

    directory_flags = (
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_CLOEXEC", 0)
    )
    lock_fd = os.open(PROJECTION_LOCK_TARGET, directory_flags)
    acquired = False
    try:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            acquired = True
        except OSError as exc:
            if exc.errno not in {errno.EACCES, errno.EAGAIN}:
                raise
            raise CHECKER.ValidationError(
                "another Stage3 projection writer holds the repository-local advisory lock"
            ) from exc
        yield
    finally:
        if acquired:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            finally:
                os.close(lock_fd)
        else:
            os.close(lock_fd)


def _read_optional_bytes(path: Path) -> bytes | None:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        return None


def _capture_projection_inputs(explicit_runtime_path: Path | None) -> ProjectionInputSnapshot:
    """Read one exact source/runtime/cleanup snapshot while the writer lock is held."""

    runtime_path = CHECKER.resolve_runtime_snapshot_path(explicit_runtime_path)
    runtime_snapshot_bytes = None if runtime_path is None else runtime_path.read_bytes()
    cleanup_receipt_bytes = _read_optional_bytes(CLEANUP_RECEIPT)
    pre_cleanup_receipt_bytes = _read_optional_bytes(CHECKER.PRE_CLEANUP_RECEIPT)
    cleanup_verifier_script_bytes = (
        None if cleanup_receipt_bytes is None else CHECKER.CLEANUP_VERIFIER_SCRIPT.read_bytes()
    )
    return ProjectionInputSnapshot(
        runtime_path=runtime_path,
        blueprint_bytes=BLUEPRINT.read_bytes(),
        runtime_snapshot_bytes=runtime_snapshot_bytes,
        cleanup_receipt_bytes=cleanup_receipt_bytes,
        pre_cleanup_receipt_bytes=pre_cleanup_receipt_bytes,
        cleanup_verifier_script_bytes=cleanup_verifier_script_bytes,
    )


def _assert_projection_inputs_unchanged(
    expected: ProjectionInputSnapshot,
    explicit_runtime_path: Path | None,
) -> None:
    actual = _capture_projection_inputs(explicit_runtime_path)
    if actual == expected:
        return
    changed = [
        field
        for field in ProjectionInputSnapshot.__dataclass_fields__
        if getattr(actual, field) != getattr(expected, field)
    ]
    raise CHECKER.ValidationError(
        "projection inputs changed during generation: " + ", ".join(changed)
    )


def _atomic_replace(
    path: Path,
    content: str,
    *,
    replace_func: Callable[[str | os.PathLike[str], str | os.PathLike[str]], Any] | None = None,
) -> None:
    """Flush, fsync, and replace one surface using a temporary in its target directory."""

    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    replace = os.replace if replace_func is None else replace_func
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        replace(temporary, path)
        directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        directory_fd = os.open(path.parent, directory_flags)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def write_outputs(
    outputs: dict[Path, str],
    *,
    writer: Callable[[Path, str], None] | None = None,
) -> None:
    """Exercise frozen write order with an injected non-production test writer."""

    if set(outputs) != set(OUTPUT_ORDER):
        raise ValueError("output set differs from the frozen Stage3 projection surfaces")
    if writer is None:
        raise ValueError(
            "unlocked direct projection writes are forbidden; use the locked snapshot commit path"
        )
    write_one = writer
    for path in OUTPUT_ORDER:
        write_one(path, outputs[path])


def _read_optional_runtime(path: Path | None) -> str | None:
    if path is None:
        return None
    return path.read_bytes().decode("utf-8")


def _read_cleanup_receipt() -> str | None:
    if not CLEANUP_RECEIPT.exists():
        return None
    return CLEANUP_RECEIPT.read_bytes().decode("utf-8")


def _check_outputs(
    outputs: dict[Path, str],
    runtime_snapshot_text: str | None,
    cleanup_receipt_text: str | None,
    *,
    blueprint_text: str | None = None,
    pre_cleanup_receipt_text: str | None = None,
    cleanup_verifier_script_bytes: bytes | None = None,
) -> list[str]:
    drift: list[str] = []
    actual: dict[Path, str] = {}
    for path in OUTPUT_ORDER:
        try:
            actual[path] = path.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError):
            drift.append(path.relative_to(ROOT).as_posix())
            continue
        if actual[path] != outputs[path]:
            drift.append(path.relative_to(ROOT).as_posix())
    if not drift:
        try:
            CHECKER.validate_texts(
                BLUEPRINT.read_bytes().decode("utf-8") if blueprint_text is None else blueprint_text,
                actual[GANTT],
                actual[STATUS],
                actual[KANBAN],
                runtime_snapshot_text,
                cleanup_receipt_text,
                pre_cleanup_receipt_text,
                cleanup_verifier_script_bytes,
            )
        except (OSError, UnicodeDecodeError, CHECKER.ValidationError) as exc:
            raise CHECKER.ValidationError(f"generated surfaces are stale or invalid: {exc}") from exc
    return drift


def _commit_outputs(
    outputs: dict[Path, str],
    inputs: ProjectionInputSnapshot,
    explicit_runtime_path: Path | None,
) -> None:
    """Commit one input snapshot with Gantt last, then validate exact disk state."""

    if set(outputs) != set(OUTPUT_ORDER):
        raise ValueError("output set differs from the frozen Stage3 projection surfaces")
    _assert_projection_inputs_unchanged(inputs, explicit_runtime_path)
    _atomic_replace(STATUS, outputs[STATUS])
    _atomic_replace(KANBAN, outputs[KANBAN])
    # A changed authority/runtime input must not receive the Gantt commit marker.
    _assert_projection_inputs_unchanged(inputs, explicit_runtime_path)
    _atomic_replace(GANTT, outputs[GANTT])
    _assert_projection_inputs_unchanged(inputs, explicit_runtime_path)
    drift = _check_outputs(
        outputs,
        inputs.runtime_snapshot_text,
        inputs.cleanup_receipt_text,
        blueprint_text=inputs.blueprint_text,
        pre_cleanup_receipt_text=inputs.pre_cleanup_receipt_text,
        cleanup_verifier_script_bytes=inputs.cleanup_verifier_script_bytes,
    )
    _assert_projection_inputs_unchanged(inputs, explicit_runtime_path)
    if drift:
        raise CHECKER.ValidationError(
            "postcommit projection drift in "
            + ", ".join(drift)
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail on stale or byte-different projections")
    parser.add_argument(
        "--runtime-snapshot",
        type=Path,
        help=(
            f"explicit strict {CHECKER.RUNTIME_SCHEMA} snapshot override; omission auto-discovers "
            "the canonical controller snapshot and otherwise projects runtime_unavailable"
        ),
    )
    args = parser.parse_args()
    try:
        with _projection_writer_lock():
            inputs = _capture_projection_inputs(args.runtime_snapshot)
            runtime_snapshot_text = inputs.runtime_snapshot_text
            cleanup_receipt_text = inputs.cleanup_receipt_text
            if args.check:
                existing = _existing_gantt_metadata()
                if existing is None:
                    print(
                        "generate_stage3_surfaces: ERROR: Gantt metadata missing; projections are stale",
                        file=sys.stderr,
                    )
                    return 1
                outputs = expected_outputs(
                    generated_at=existing["generated_at"],
                    runtime_snapshot_text=runtime_snapshot_text,
                    cleanup_receipt_text=cleanup_receipt_text,
                    blueprint_text=inputs.blueprint_text,
                    pre_cleanup_receipt_text=inputs.pre_cleanup_receipt_text,
                    cleanup_verifier_script_bytes=inputs.cleanup_verifier_script_bytes,
                    enforce_current_runtime=True,
                )
                drift = _check_outputs(
                    outputs,
                    runtime_snapshot_text,
                    cleanup_receipt_text,
                    blueprint_text=inputs.blueprint_text,
                    pre_cleanup_receipt_text=inputs.pre_cleanup_receipt_text,
                    cleanup_verifier_script_bytes=inputs.cleanup_verifier_script_bytes,
                )
                _assert_projection_inputs_unchanged(inputs, args.runtime_snapshot)
                if drift:
                    print(
                        "generate_stage3_surfaces: ERROR: stale drift in " + ", ".join(drift),
                        file=sys.stderr,
                    )
                    return 1
                print("generate_stage3_surfaces: ok (shared timestamp reused; source/spec/runtime snapshot fresh)")
                return 0
            _validated_inputs(
                runtime_snapshot_text,
                cleanup_receipt_text,
                blueprint_text=inputs.blueprint_text,
                pre_cleanup_receipt_text=inputs.pre_cleanup_receipt_text,
                cleanup_verifier_script_bytes=inputs.cleanup_verifier_script_bytes,
                enforce_current_runtime=True,
            )
            generated_at = choose_generation_time(
                runtime_snapshot_text,
                cleanup_receipt_text,
                blueprint_text=inputs.blueprint_text,
                pre_cleanup_receipt_text=inputs.pre_cleanup_receipt_text,
                cleanup_verifier_script_bytes=inputs.cleanup_verifier_script_bytes,
            )
            outputs = expected_outputs(
                generated_at=generated_at,
                runtime_snapshot_text=runtime_snapshot_text,
                cleanup_receipt_text=cleanup_receipt_text,
                blueprint_text=inputs.blueprint_text,
                pre_cleanup_receipt_text=inputs.pre_cleanup_receipt_text,
                cleanup_verifier_script_bytes=inputs.cleanup_verifier_script_bytes,
                enforce_current_runtime=True,
            )
            _commit_outputs(outputs, inputs, args.runtime_snapshot)
    except (OSError, UnicodeDecodeError, CHECKER.ValidationError, ValueError) as exc:
        print(f"generate_stage3_surfaces: ERROR: {exc}", file=sys.stderr)
        return 1
    for path in OUTPUT_ORDER:
        print(f"generated {path.relative_to(ROOT)}")
    print(f"snapshot generated_at={generated_at}; Gantt replaced last")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
