#!/usr/bin/env python3
"""Generate the complete same-prefix Stage5 theorem runtime projection."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "Docs/tools/check_stage5_theorems_blueprint.py"
MANAGER_PATH = ROOT / "Docs/tools/manage_stage5_proof_debt_blueprints.py"
BLUEPRINT = ROOT / "Docs/Stage5_Theorems_Blueprint.md"
GANTT = ROOT / "Docs/Stage5_Theorems_Gantt.md"
RUNTIME_SNAPSHOT = ROOT / ".ops/stage5-theorems-execution-v2/status/runtime-snapshot.json"
META_BEGIN = "<!-- STAGE5-PROOF-DEBT-GANTT-METADATA:BEGIN -->"
META_END = "<!-- STAGE5-PROOF-DEBT-GANTT-METADATA:END -->"
INDEX_BEGIN = "<!-- STAGE5-PROOF-DEBT-GANTT-INDEX:BEGIN -->"
INDEX_END = "<!-- STAGE5-PROOF-DEBT-GANTT-INDEX:END -->"


class GanttError(RuntimeError):
    pass


def load_checker() -> Any:
    spec = importlib.util.spec_from_file_location("stage5_theorem_checker_for_gantt", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise GanttError("cannot load Stage5 theorem checker")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_manager() -> Any:
    spec = importlib.util.spec_from_file_location(
        "stage5_proof_debt_manager_for_theorem_gantt", MANAGER_PATH
    )
    if spec is None or spec.loader is None:
        raise GanttError("cannot load Stage5 proof-debt manager")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def json_cell(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def load_runtime(checker: Any, item_ids: set[str]) -> tuple[dict[str, Any], str | None]:
    if not RUNTIME_SNAPSHOT.exists():
        return {}, None
    if RUNTIME_SNAPSHOT.is_symlink() or not RUNTIME_SNAPSHOT.is_file():
        raise GanttError("runtime snapshot is not a regular file")
    raw = RUNTIME_SNAPSHOT.read_bytes()
    value = checker.strict_json(raw, "runtime snapshot")
    checker.verify_seal(value, "runtime snapshot")
    if value.get("schema_version") != "awesome-theorems/stage5-runtime-snapshot/1.0":
        raise GanttError("runtime snapshot schema differs")
    if value.get("program") != checker.PROGRAM:
        raise GanttError("runtime snapshot program differs")
    items = value.get("items")
    if not isinstance(items, dict) or set(items) - item_ids:
        raise GanttError("runtime snapshot item mapping is malformed or contains unknown IDs")
    return value, digest(raw)


def worker_summary(runtime_item: dict[str, Any]) -> dict[str, Any]:
    worker = runtime_item.get("worker", {}) if isinstance(runtime_item, dict) else {}
    if not isinstance(worker, dict):
        worker = {}
    summary = {
        field: worker.get(field)
        for field in (
            "claim_id", "run_id", "owner", "status", "startup", "live", "running",
            "tmux_socket", "tmux_session", "codex_home", "thread_id", "goal_id",
            "provider", "model", "reasoning_effort", "service_tier", "budget", "handoff",
        )
    }
    summary.update({
        "theorem_work_state": runtime_item.get("theorem_work_state"),
        "lane_state": runtime_item.get("lane_state"),
        "generation_state": runtime_item.get("generation_state", worker.get("status")),
        "goal_state": runtime_item.get("goal_state"),
        "handoff_kind": runtime_item.get("handoff_kind"),
        "checkpoint": runtime_item.get("checkpoint"),
        "terminal_disposition": runtime_item.get("terminal_disposition"),
        "replacement_lineage": runtime_item.get("replacement_lineage"),
    })
    return summary


def render(*, generated_at: str | None = None, blueprint_path: Path = BLUEPRINT) -> bytes:
    checker = load_checker()
    specification, rows, blueprint_raw = checker.parse_blueprint(blueprint_path)
    checker.validate_spec(specification)
    # During an activated controller run, the immutable BOOT receipt is the
    # predecessor authority and the ongoing controller owns signed
    # blank/underscore/x transitions.  Requiring the pristine BOOT post-bytes
    # for every runtime projection would reject every legitimate handoff.
    if checker.MIGRATION_RECEIPT.exists() and not RUNTIME_SNAPSHOT.exists():
        checker.validate_migration_receipt(rows, blueprint_raw)
        if blueprint_path == BLUEPRINT and not RUNTIME_SNAPSHOT.exists():
            manager = load_manager()
            tasks = manager.expected_tasks(manager.THEOREM)
            parsed = manager.parse_blueprint(
                manager.THEOREM, blueprint_raw, tasks
            )
            return manager.render_gantt(
                manager.THEOREM, blueprint_raw, parsed, generated_at or now()
            )
    item_ids = {row["item_id"] for row in rows}
    runtime, runtime_sha = load_runtime(checker, item_ids)
    runtime_items = runtime.get("items", {}) if runtime else {}
    counts = Counter(row["state"] for row in rows)
    by_id = {row["item_id"]: row for row in rows}
    ready = [
        row["item_id"] for row in rows
        if row["state"] == " " and all(by_id[dep]["state"] == "x" for dep in row["dependencies"])
    ]
    integration = [
        row["item_id"] for row in rows
        if row["state"] == "_" and all(by_id[dep]["state"] == "x" for dep in row["dependencies"])
    ]
    generated_at = generated_at or now()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", generated_at):
        raise GanttError("generation time is not whole-second RFC3339 UTC")
    observed = runtime.get("observed_usage", {}) if runtime else {}
    live = int(observed.get("authenticated_live_goals", 0))
    prompt_contract = specification["concurrency_prompt_contract"]
    requested = runtime.get("requested_concurrency") if runtime else None
    underfill = runtime.get("underfill", {}) if runtime else {
        "authenticated_live_goal_slots": None,
        "binding_reasons": ["BOOT_not_accepted", "controller_not_activated", "concurrency_prompt_required"],
    }
    metadata = {
        "schema_version": "awesome-theorems/stage5-proof-debt-gantt/1.1",
        "program": checker.PROGRAM,
        "blueprint_path": BLUEPRINT.relative_to(ROOT).as_posix(),
        "gantt_path": GANTT.relative_to(ROOT).as_posix(),
        "blueprint_sha256": digest(blueprint_raw),
        "execution_specification_sha256": digest(canonical(specification)),
        "checklist_dag_sha256": digest(canonical(checker.dag_object(rows))),
        "checklist_state_sha256": digest(canonical([
            [row["item_id"], {" ": "not_done", "_": "handoff_waiting_master", "x": "master_accepted"}[row["state"]]]
            for row in rows
        ])),
        "runtime_snapshot_path": RUNTIME_SNAPSHOT.relative_to(ROOT).as_posix(),
        "runtime_snapshot_sha256": runtime_sha,
        "runtime_snapshot_id": runtime.get("snapshot_id") if runtime else None,
        "generated_at": generated_at,
        "item_count": len(rows),
        "target_count": 3500,
        "program_complete": all(row["state"] == "x" for row in rows),
        "state_counts": {
            "not_done": counts[" "],
            "handoff_waiting_master": counts["_"],
            "master_accepted": counts["x"],
        },
        "frontiers": {"implementation": ready, "integration": integration},
        "capacity_saturation_underfill": {
            "concurrency_prompt_contract": prompt_contract,
            "requested_vector": requested,
            "observed_usage": observed or {
                "logical_claims": 0, "starting_lanes": 0,
                "authenticated_live_goals": 0, "running_turns": 0,
                "canonical_integrations": 0, "lean_build_validators": 0,
                "external_launches_this_wave": 0,
            },
            "saturated_dimensions": runtime.get("saturated_dimensions", []) if runtime else [],
            "underfill": underfill,
        },
        "schedule_basis": "recorded runtime timestamps only; all others unscheduled",
    }
    mermaid_at = generated_at.removesuffix("Z")
    lines = [
        "# Stage5 Theorems Proof-Debt Gantt and Complete Monitor",
        "",
        "> Generated read-only projection; `Docs/Stage5_Theorems_Blueprint.md` is the sole checklist authority.",
        "",
        META_BEGIN,
        "```json",
        json.dumps(metadata, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False),
        "```",
        META_END,
        "",
        "## Renderable recorded timing",
        "",
        "Unknown timing remains unscheduled. The projection timestamp is not a task estimate.",
        "",
        "```mermaid",
        "gantt",
        "    title Stage5 Theorems recorded projection timing",
        "    dateFormat YYYY-MM-DDTHH:mm:ss",
        "    axisFormat %Y-%m-%d %H:%M",
        "    section Projection",
        f"    Projection generated UTC :milestone, projection, {mermaid_at}, 0s",
        "```",
        "",
        "## Complete monitoring index",
        "",
        INDEX_BEGIN,
        "| Item | State | Depends on | Owned paths | Sole worker | Planning blockers | Runtime block | Timing |",
        "|---|---|---|---|---|---|---|---|",
    ]
    names = {" ": "not_done", "_": "handoff_waiting_master", "x": "master_accepted"}
    for row in rows:
        runtime_item = runtime_items.get(row["item_id"], {})
        if not isinstance(runtime_item, dict):
            raise GanttError(f"{row['item_id']}: runtime item is not an object")
        blockers = [dep for dep in row["dependencies"] if by_id[dep]["state"] != "x"]
        timing = runtime_item.get("timing") or {
            "status": "unscheduled", "start": None, "end": None,
            "duration_seconds": None, "source": None,
        }
        cells = [
            row["item_id"], names[row["state"]], list(row["dependencies"]),
            list(row["owned_paths"]), worker_summary(runtime_item), blockers,
            runtime_item.get("block"), timing,
        ]
        lines.append("| " + " | ".join(json_cell(cell) for cell in cells) + " |")
    lines.extend([INDEX_END, ""])
    return "\n".join(lines).encode("utf-8")


def atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    parser.add_argument("--generated-at")
    arguments = parser.parse_args(argv)
    try:
        if not arguments.write and not arguments.check:
            # BOOT command: validate that the current projection is complete
            # without attempting a write into the read-only snapshot.
            checker = load_checker()
            result = checker.check(require_boot_data=True, require_gantt=True)
            print(json.dumps({"valid": True, "mode": "read_only_boot_check", "items": result["items"]}, sort_keys=True))
            return 0
        expected = render(generated_at=arguments.generated_at)
        if arguments.check:
            if not GANTT.is_file() or GANTT.read_bytes() != expected:
                raise GanttError("Gantt bytes are stale or noncanonical for the requested generation time")
        else:
            atomic_write(GANTT, expected)
        print(json.dumps({"valid": True, "items": 3575, "targets": 3500, "sha256": digest(expected), "written": arguments.write}, sort_keys=True))
    except (GanttError, OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
