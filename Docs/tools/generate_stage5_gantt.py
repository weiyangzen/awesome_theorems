#!/usr/bin/env python3
"""Generate and validate the same-name Stage5 mathematics Gantt projection."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT = ROOT / "Docs" / "Stage5_Math_Expansion_Blueprint.md"
VERSION = "stage5-math-expansion/1.0"
GANTT_SCHEMA = "stage5-math-gantt/1.0"

CHECKLIST_BEGIN = "<!-- STAGE5-MATH-EXECUTION-CHECKLIST:BEGIN -->"
CHECKLIST_END = "<!-- STAGE5-MATH-EXECUTION-CHECKLIST:END -->"
METADATA_BEGIN = "<!-- STAGE5-MATH-GANTT-METADATA:BEGIN -->"
METADATA_END = "<!-- STAGE5-MATH-GANTT-METADATA:END -->"

ID_PATTERN = r"S5M-[A-Z]+-[0-9]{3}"
TASK_RE = re.compile(
    rf"^- \[(?P<state>[ _x])\] `(?P<id>{ID_PATTERN})` "
    r"(?P<title>[^|]+?) \| depends_on=(?P<depends>[^|]+?) "
    r"\| delivers=(?P<delivers>[^|]+?) \| acceptance=(?P<acceptance>.+)$"
)
ROW_ID_RE = re.compile(rf"^\| `(?P<id>{ID_PATTERN})` \|", re.MULTILINE)
CHECKBOX_RE = re.compile(r"\[[ _x]\]")
RFC3339_UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")


class Stage5GanttError(RuntimeError):
    """Fail-closed Blueprint or projection error."""


@dataclass(frozen=True)
class Task:
    state: str
    item_id: str
    title: str
    dependencies: tuple[str, ...]
    deliverables: tuple[str, ...]
    acceptance: str


def companion_path(blueprint: Path) -> Path:
    suffix = "_Blueprint.md"
    if not blueprint.name.endswith(suffix):
        raise Stage5GanttError(f"Blueprint does not have the required same-name suffix: {blueprint}")
    return blueprint.with_name(blueprint.name[: -len(suffix)] + "_Gantt.md")


GANTT = companion_path(BLUEPRINT)


def _split_csv(value: str, field: str, item_id: str) -> tuple[str, ...]:
    values = tuple(part.strip() for part in value.split(","))
    if not values or any(not part for part in values):
        raise Stage5GanttError(f"{item_id} has an empty {field} value")
    if len(set(values)) != len(values):
        raise Stage5GanttError(f"{item_id} repeats a {field} value")
    return values


def _validate_deliverable(path_text: str, item_id: str) -> None:
    path = PurePosixPath(path_text)
    if any(character in path_text for character in "|`<>\\"):
        raise Stage5GanttError(f"{item_id} has an unsafe Markdown path: {path_text}")
    if path.is_absolute() or ".." in path.parts or path_text != path.as_posix():
        raise Stage5GanttError(f"{item_id} has a non-canonical repository path: {path_text}")
    if not path.parts or path.parts[0] in {".git", ".ops"}:
        raise Stage5GanttError(f"{item_id} has a forbidden deliverable path: {path_text}")


def _validate_dag(tasks: tuple[Task, ...]) -> None:
    by_id = {task.item_id: task for task in tasks}
    for task in tasks:
        for dependency in task.dependencies:
            if dependency not in by_id:
                raise Stage5GanttError(f"{task.item_id} has unknown dependency {dependency}")
            if dependency == task.item_id:
                raise Stage5GanttError(f"{task.item_id} depends on itself")
        if task.state in {"_", "x"}:
            unfinished = [dep for dep in task.dependencies if by_id[dep].state != "x"]
            if unfinished:
                raise Stage5GanttError(
                    f"{task.item_id} has advanced state before accepted dependencies: {unfinished}"
                )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(item_id: str) -> None:
        if item_id in visiting:
            raise Stage5GanttError(f"dependency cycle reaches {item_id}")
        if item_id in visited:
            return
        visiting.add(item_id)
        for dependency in by_id[item_id].dependencies:
            visit(dependency)
        visiting.remove(item_id)
        visited.add(item_id)

    for item_id in by_id:
        visit(item_id)


def parse_blueprint(raw: bytes) -> tuple[Task, ...]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Stage5GanttError("Blueprint must be UTF-8") from exc

    if text.count(f"> Blueprint version: `{VERSION}`") != 1:
        raise Stage5GanttError("Blueprint version does not match the generator contract")
    expected_authority = f"> Authoritative path: `{BLUEPRINT.relative_to(ROOT).as_posix()}`"
    expected_companion = f"> Same-name generated monitor: `{GANTT.relative_to(ROOT).as_posix()}`"
    if text.count(expected_authority) != 1 or text.count(expected_companion) != 1:
        raise Stage5GanttError("Blueprint authority or same-name companion declaration drifted")

    if text.count(CHECKLIST_BEGIN) != 1 or text.count(CHECKLIST_END) != 1:
        raise Stage5GanttError("Blueprint must contain exactly one checklist marker pair")
    before, remainder = text.split(CHECKLIST_BEGIN, 1)
    region, after = remainder.split(CHECKLIST_END, 1)
    if CHECKLIST_END in before or CHECKLIST_BEGIN in after:
        raise Stage5GanttError("Blueprint checklist markers are out of order")

    tasks: list[Task] = []
    for line_number, line in enumerate(region.splitlines(), start=1):
        if not line.strip():
            continue
        match = TASK_RE.fullmatch(line)
        if match is None:
            raise Stage5GanttError(f"invalid checklist line {line_number}: {line}")
        item_id = match.group("id")
        depends_text = match.group("depends").strip()
        dependencies = () if depends_text == "-" else _split_csv(depends_text, "dependency", item_id)
        deliverables = _split_csv(match.group("delivers").strip(), "deliverable", item_id)
        for deliverable in deliverables:
            _validate_deliverable(deliverable, item_id)
        acceptance = match.group("acceptance").strip()
        if len(acceptance) < 40:
            raise Stage5GanttError(f"{item_id} acceptance clause is not independently verifiable")
        tasks.append(
            Task(
                state=match.group("state"),
                item_id=item_id,
                title=match.group("title").strip(),
                dependencies=dependencies,
                deliverables=deliverables,
                acceptance=acceptance,
            )
        )

    if not tasks:
        raise Stage5GanttError("Blueprint checklist is empty")
    ids = [task.item_id for task in tasks]
    if len(ids) != len(set(ids)):
        duplicates = sorted(item_id for item_id, count in Counter(ids).items() if count > 1)
        raise Stage5GanttError(f"duplicate checklist IDs: {duplicates}")
    all_deliverables = [path for task in tasks for path in task.deliverables]
    duplicate_paths = sorted(path for path, count in Counter(all_deliverables).items() if count > 1)
    if duplicate_paths:
        raise Stage5GanttError(f"deliverable paths have multiple owners: {duplicate_paths}")
    _validate_dag(tuple(tasks))
    return tuple(tasks)


def _validate_generated_at(value: str) -> str:
    if not RFC3339_UTC_RE.fullmatch(value):
        raise Stage5GanttError("generated_at must be a whole-second RFC3339 UTC timestamp")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise Stage5GanttError("generated_at is not a real UTC timestamp") from exc
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise Stage5GanttError("generated_at is not canonical")
    return value


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def _state_name(state: str) -> str:
    return {" ": "not_started", "_": "awaiting_acceptance", "x": "accepted"}[state]


def _code(value: str) -> str:
    return "`" + value.replace("`", "\\`").replace("|", "\\|") + "`"


def _list_cell(values: tuple[str, ...]) -> str:
    if not values:
        return "—"
    return "<br>".join(_code(value) for value in values)


def _planning(task: Task, by_id: dict[str, Task]) -> tuple[str, tuple[str, ...]]:
    if task.state == "x":
        return "accepted", ()
    if task.state == "_":
        return "awaiting_independent_acceptance", ()
    blockers = tuple(dep for dep in task.dependencies if by_id[dep].state != "x")
    return ("dependency_blocked", blockers) if blockers else ("ready", ())


def _render_table(
    tasks: tuple[Task, ...], *, all_tasks: dict[str, Task], timing: str
) -> list[str]:
    if not tasks:
        return ["_None._"]
    lines = [
        "| Item | State | Depends on | Planning | Blocking dependencies | Deliverables | Timing |",
        "|---|---|---|---|---|---|---|",
    ]
    for task in tasks:
        planning, blockers = _planning(task, all_tasks)
        lines.append(
            "| "
            + " | ".join(
                (
                    _code(task.item_id),
                    _code(_state_name(task.state)),
                    _list_cell(task.dependencies),
                    _code(planning),
                    _list_cell(blockers),
                    _list_cell(task.deliverables),
                    _code(timing),
                )
            )
            + " |"
        )
    return lines


def render_gantt(tasks: tuple[Task, ...], raw_blueprint: bytes, generated_at: str) -> str:
    generated_at = _validate_generated_at(generated_at)
    source_digest = hashlib.sha256(raw_blueprint).hexdigest()
    counts = Counter(_state_name(task.state) for task in tasks)
    metadata = {
        "schema_version": GANTT_SCHEMA,
        "blueprint_version": VERSION,
        "blueprint_path": BLUEPRINT.relative_to(ROOT).as_posix(),
        "gantt_path": GANTT.relative_to(ROOT).as_posix(),
        "blueprint_source_sha256": source_digest,
        "generated_at": generated_at,
        "item_count": len(tasks),
        "state_counts": {
            "not_started": counts["not_started"],
            "awaiting_acceptance": counts["awaiting_acceptance"],
            "accepted": counts["accepted"],
        },
        "schedule_basis": "no_authoritative_task_dates",
    }
    unfinished = tuple(task for task in tasks if task.state == " ")
    progressed = tuple(task for task in tasks if task.state != " ")
    all_tasks = {task.item_id: task for task in tasks}
    lines = [
        "# Stage5 Mathematics Expansion Gantt and Monitor",
        "",
        f"> Generated read-only planning projection for `{VERSION}`.",
        "> The Blueprint is the sole task-state authority; regenerate this file instead of editing it.",
        "",
        METADATA_BEGIN,
        "```json",
        *json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=False).splitlines(),
        "```",
        METADATA_END,
        "",
        "## Timing boundary",
        "",
        "No task start, end, duration, or operator-frozen estimate is recorded in the Blueprint. "
        "The generation timestamp above describes this projection only and is not a task date. "
        "Document order and dependency depth are never converted into calendar claims.",
        "",
        "## Recorded progress without schedule timing",
        "",
        *_render_table(progressed, all_tasks=all_tasks, timing="not_recorded"),
        "",
        "## Unscheduled items",
        "",
        "Every unfinished item without accepted timing evidence appears here exactly once as a task row.",
        "",
        *_render_table(unfinished, all_tasks=all_tasks, timing="unscheduled"),
        "",
    ]
    return "\n".join(lines)


def _extract_metadata(text: str) -> dict[str, object]:
    if text.count(METADATA_BEGIN) != 1 or text.count(METADATA_END) != 1:
        raise Stage5GanttError("Gantt must contain exactly one metadata marker pair")
    payload = text.split(METADATA_BEGIN, 1)[1].split(METADATA_END, 1)[0].strip()
    if not payload.startswith("```json\n") or not payload.endswith("\n```"):
        raise Stage5GanttError("Gantt metadata must be one fenced JSON object")
    try:
        value = json.loads(payload[len("```json\n") : -len("\n```")])
    except json.JSONDecodeError as exc:
        raise Stage5GanttError("Gantt metadata is invalid JSON") from exc
    if not isinstance(value, dict):
        raise Stage5GanttError("Gantt metadata must be an object")
    return value


def validate_projection(text: str, tasks: tuple[Task, ...], raw_blueprint: bytes) -> None:
    if CHECKBOX_RE.search(text):
        raise Stage5GanttError("Gantt contains forbidden checkbox syntax")
    metadata = _extract_metadata(text)
    expected_digest = hashlib.sha256(raw_blueprint).hexdigest()
    if metadata.get("blueprint_source_sha256") != expected_digest:
        raise Stage5GanttError("Gantt source digest does not match the Blueprint bytes")
    if metadata.get("blueprint_path") != BLUEPRINT.relative_to(ROOT).as_posix():
        raise Stage5GanttError("Gantt metadata has the wrong Blueprint path")
    if metadata.get("gantt_path") != companion_path(BLUEPRINT).relative_to(ROOT).as_posix():
        raise Stage5GanttError("Gantt metadata violates same-name path derivation")
    if metadata.get("item_count") != len(tasks):
        raise Stage5GanttError("Gantt metadata item count does not match the Blueprint")
    expected_counts = Counter(_state_name(task.state) for task in tasks)
    if metadata.get("state_counts") != {
        "not_started": expected_counts["not_started"],
        "awaiting_acceptance": expected_counts["awaiting_acceptance"],
        "accepted": expected_counts["accepted"],
    }:
        raise Stage5GanttError("Gantt metadata state counts do not match the Blueprint")
    generated_at = metadata.get("generated_at")
    if not isinstance(generated_at, str):
        raise Stage5GanttError("Gantt metadata lacks generated_at")
    _validate_generated_at(generated_at)
    row_ids = ROW_ID_RE.findall(text)
    expected_ids = [task.item_id for task in tasks]
    if Counter(row_ids) != Counter(expected_ids) or len(row_ids) != len(expected_ids):
        raise Stage5GanttError("Gantt task rows do not cover every Blueprint ID exactly once")


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    output_mode = path.stat().st_mode & 0o777 if path.exists() else 0o664
    file_descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(file_descriptor, "wb") as handle:
            os.fchmod(handle.fileno(), output_mode)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate without writing")
    parser.add_argument("--generated-at", help="explicit whole-second RFC3339 UTC projection time")
    args = parser.parse_args(argv)

    try:
        raw_blueprint = BLUEPRINT.read_bytes()
        tasks = parse_blueprint(raw_blueprint)
        if args.check:
            if not GANTT.exists():
                raise Stage5GanttError(f"missing generated Gantt: {GANTT}")
            current = GANTT.read_text(encoding="utf-8")
            current_metadata = _extract_metadata(current)
            recorded_time = current_metadata.get("generated_at")
            if not isinstance(recorded_time, str):
                raise Stage5GanttError("generated Gantt lacks a valid generation time")
            generated_at = args.generated_at or recorded_time
            expected = render_gantt(tasks, raw_blueprint, generated_at)
            validate_projection(current, tasks, raw_blueprint)
            if current != expected:
                raise Stage5GanttError("generated Gantt is stale or hand-edited")
            print(
                f"PASS Stage5 Gantt check: items={len(tasks)} "
                f"blueprint_sha256={hashlib.sha256(raw_blueprint).hexdigest()}"
            )
            return 0

        generated_at = _validate_generated_at(args.generated_at) if args.generated_at else _utc_now()
        rendered = render_gantt(tasks, raw_blueprint, generated_at)
        validate_projection(rendered, tasks, raw_blueprint)
        if BLUEPRINT.read_bytes() != raw_blueprint:
            raise Stage5GanttError("Blueprint changed during generation")
        _atomic_write(GANTT, rendered.encode("utf-8"))
        if BLUEPRINT.read_bytes() != raw_blueprint:
            raise Stage5GanttError("Blueprint changed during publication; regenerate the Gantt")
        if GANTT.read_text(encoding="utf-8") != rendered:
            raise Stage5GanttError("published Gantt bytes do not match the validated projection")
        unfinished_count = sum(task.state == " " for task in tasks)
        print(f"WROTE {GANTT.relative_to(ROOT)} with {unfinished_count} unscheduled items")
        return 0
    except (OSError, UnicodeError, Stage5GanttError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
