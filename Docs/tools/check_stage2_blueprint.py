#!/usr/bin/env python3
"""Validate the frozen historical Stage2 checklist and its read-only Gantt projection."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT = ROOT / "Docs" / "Stage2_Blueprint.md"
GANTT = ROOT / "Docs" / "Stage2_Gantt.md"
BEGIN = "<!-- STAGE2-EXECUTION-CHECKLIST:BEGIN -->"
END = "<!-- STAGE2-EXECUTION-CHECKLIST:END -->"
GANTT_DEP_BEGIN = "<!-- STAGE2-GANTT-DEPENDENCIES:BEGIN -->"
GANTT_DEP_END = "<!-- STAGE2-GANTT-DEPENDENCIES:END -->"
VERSION = "stage2-catalog-integrity/1.0"
GANTT_HEADING = "# Stage2 Catalog Integrity and Isolated Execution Gantt"
GANTT_MERMAID_TITLE = "title Stage2 Catalog Integrity and Isolated Execution"

ITEM_PATTERN = r"S2-(?:AUTH|ENV|AUD|CAT|M38|EXE|REL)-[0-9]{3}"
ITEM_RE = re.compile(rf"^{ITEM_PATTERN}$")
ITEM_REF_RE = re.compile(ITEM_PATTERN)
ROW_RE = re.compile(
    rf"^- \[(?P<state>[ _x])\] `(?P<item>{ITEM_PATTERN})` "
    r"(?P<title>[^|]+?) \| depends_on=(?P<deps>[^|]+?) "
    r"\| owned_paths=(?P<paths>[^|]+?) \| gate=(?P<gate>.+)$"
)
GANTT_DEP_ROW_RE = re.compile(
    rf"^\| `(?P<item>{ITEM_PATTERN})` \| `(?P<deps>[^`]+)` \|$"
)

REQUIRED_BLUEPRINT_PHRASES = (
    "SUPERSEDED / HISTORICAL — DO NOT EXECUTE",
    "sole current cross-stage execution\n> authority is `Docs/Stage3_Blueprint.md`",
    "WORKER_TRANSPORT=tmux_codex_tui",
    "WORKER_GOAL_COMMAND=/goal",
    "APP_SERVER_WORKERS=forbidden",
    "CODEX_PROCESS_ISOLATION=one_process_tree_per_claim",
    "CODEX_STATE_ISOLATION=one_writable_home_per_claim",
    "exactly one authenticated active `/goal` per claim",
    ".ops/stage2-execution-v1/tasks/<claim-id>/<run-id>/",
    "Harvest always precedes stale pruning",
    "zero `[ ]`, zero `[_]`",
)

REQUIRED_CATEGORIES = {"AUTH", "ENV", "AUD", "CAT", "M38", "EXE", "REL"}


class ValidationError(ValueError):
    """The Stage2 authority or projection violates its frozen contract."""


@dataclass(frozen=True)
class Task:
    item_id: str
    state: str
    title: str
    dependencies: tuple[str, ...]
    owned_paths: tuple[str, ...]
    gate: str
    line_number: int


def _one_region(text: str) -> tuple[int, int, list[str]]:
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValidationError("blueprint must contain exactly one checklist marker pair")
    lines = text.splitlines()
    begin_index = next(index for index, line in enumerate(lines) if line == BEGIN)
    end_index = next(index for index, line in enumerate(lines) if line == END)
    if end_index <= begin_index:
        raise ValidationError("checklist end marker precedes its begin marker")
    return begin_index, end_index, lines


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
    if candidate.parts[0] in {".git", ".ops", ".cron"}:
        raise ValidationError(f"{item_id}: tracked deliverable may not live in runtime/control storage: {path}")


def parse_tasks(blueprint_text: str) -> dict[str, Task]:
    begin_index, end_index, lines = _one_region(blueprint_text)
    tasks: dict[str, Task] = {}

    for index in range(begin_index + 1, end_index):
        line = lines[index]
        if not line.startswith("- ["):
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
        if len(gate) < 20:
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


def validate_graph(tasks: dict[str, Task]) -> None:
    categories = {item_id.split("-")[1] for item_id in tasks}
    if categories != REQUIRED_CATEGORIES:
        raise ValidationError(
            f"checklist categories differ: expected {sorted(REQUIRED_CATEGORIES)}, got {sorted(categories)}"
        )

    for task in tasks.values():
        for dependency in task.dependencies:
            if not ITEM_RE.fullmatch(dependency):
                raise ValidationError(f"{task.item_id}: malformed dependency {dependency}")
            if dependency not in tasks:
                raise ValidationError(f"{task.item_id}: missing dependency {dependency}")
            if dependency == task.item_id:
                raise ValidationError(f"{task.item_id}: self dependency")
        if task.state in {"_", "x"}:
            incomplete = [dep for dep in task.dependencies if tasks[dep].state != "x"]
            if incomplete:
                raise ValidationError(
                    f"{task.item_id}: advanced item has unfinished dependencies {incomplete}"
                )

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


def validate_blueprint_contract(blueprint_text: str) -> None:
    for phrase in REQUIRED_BLUEPRINT_PHRASES:
        if phrase not in blueprint_text:
            raise ValidationError(f"blueprint is missing required contract phrase: {phrase}")
    if blueprint_text.count("Authoritative path: `Docs/Stage2_Blueprint.md`") != 1:
        raise ValidationError("blueprint must name its authoritative path exactly once")
    if f"Blueprint version: `{VERSION}`" not in blueprint_text:
        raise ValidationError("blueprint version is missing or changed")
    if str(ROOT) in blueprint_text:
        raise ValidationError("blueprint leaks the current machine's absolute repository path")


def parse_gantt_dependencies(gantt_text: str) -> dict[str, tuple[str, ...]]:
    if gantt_text.count(GANTT_DEP_BEGIN) != 1 or gantt_text.count(GANTT_DEP_END) != 1:
        raise ValidationError("Gantt must contain exactly one exact-dependency projection")
    lines = gantt_text.splitlines()
    begin = next(index for index, line in enumerate(lines) if line == GANTT_DEP_BEGIN)
    end = next(index for index, line in enumerate(lines) if line == GANTT_DEP_END)
    if end <= begin:
        raise ValidationError("Gantt dependency projection markers are reversed")

    projected: dict[str, tuple[str, ...]] = {}
    for index in range(begin + 1, end):
        line = lines[index]
        if not line.startswith("| `S2-"):
            continue
        match = GANTT_DEP_ROW_RE.fullmatch(line)
        if match is None:
            raise ValidationError(f"Gantt line {index + 1}: malformed dependency projection row")
        item_id = match.group("item")
        if item_id in projected:
            raise ValidationError(f"Gantt dependency projection repeats {item_id}")
        dependencies = _parse_csv(match.group("deps"), "Gantt depends_on", item_id)
        projected[item_id] = dependencies
    return projected


def validate_gantt(gantt_text: str, tasks: dict[str, Task]) -> None:
    if "Docs/Stage2_Blueprint.md" not in gantt_text or VERSION not in gantt_text:
        raise ValidationError("Gantt does not bind the authoritative blueprint and version")
    if gantt_text.splitlines()[0] != GANTT_HEADING:
        raise ValidationError("Gantt heading does not match the Stage2 blueprint")
    if gantt_text.count(GANTT_MERMAID_TITLE) != 1:
        raise ValidationError("Gantt Mermaid title is missing or ambiguous")
    if re.search(r"^- \[[ _xX]\]", gantt_text, flags=re.MULTILINE):
        raise ValidationError("Gantt contains a competing checkbox cursor")
    gantt_ids = set(ITEM_REF_RE.findall(gantt_text))
    task_ids = set(tasks)
    if gantt_ids != task_ids:
        missing = sorted(task_ids - gantt_ids)
        extra = sorted(gantt_ids - task_ids)
        raise ValidationError(f"Gantt item projection differs: missing={missing}, extra={extra}")
    projected = parse_gantt_dependencies(gantt_text)
    if set(projected) != task_ids:
        missing = sorted(task_ids - set(projected))
        extra = sorted(set(projected) - task_ids)
        raise ValidationError(
            f"Gantt exact-dependency rows differ: missing={missing}, extra={extra}"
        )
    for item_id, task in tasks.items():
        if projected[item_id] != task.dependencies:
            raise ValidationError(
                f"Gantt dependency drift for {item_id}: "
                f"expected={task.dependencies}, projected={projected[item_id]}"
            )
    if str(ROOT) in gantt_text:
        raise ValidationError("Gantt leaks the current machine's absolute repository path")


def validate_texts(blueprint_text: str, gantt_text: str) -> dict[str, int]:
    validate_blueprint_contract(blueprint_text)
    tasks = parse_tasks(blueprint_text)
    validate_graph(tasks)
    validate_gantt(gantt_text, tasks)
    counts = Counter(task.state for task in tasks.values())
    return {
        "items": len(tasks),
        "open": counts[" "],
        "self_tested": counts["_"],
        "master_accepted": counts["x"],
    }


def main() -> int:
    try:
        summary = validate_texts(BLUEPRINT.read_text(), GANTT.read_text())
    except (OSError, ValidationError) as exc:
        print(f"check_stage2_blueprint: ERROR: {exc}", file=sys.stderr)
        return 1
    print(
        "check_stage2_blueprint: ok "
        f"({summary['items']} items; [ ]={summary['open']}, "
        f"[_]={summary['self_tested']}, [x]={summary['master_accepted']}; DAG acyclic; Gantt exact)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
