#!/usr/bin/env python3
"""Shared deterministic primitives for the Stage5.1 organization release.

This module deliberately contains no repository inventory, taxonomy decision,
concurrency value, worker count, or agent route.  The release builder supplies
those project-specific facts.  It provides canonical serialization, sealed
records, Blueprint parsing, structural validation, and a replayable multi-file
install transaction.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
from typing import Any, Iterable, Mapping, Sequence


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
RFC3339_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
ROW_RE = re.compile(
    r"^- \[(?P<state>[ _x])\] `(?P<item_id>[A-Z0-9-]+)` "
    r"(?P<title>.+?) \| depends_on=(?P<depends>[^|]+?) "
    r"\| owned_paths=(?P<paths>[^|]+?) \| gate=(?P<gate>.+)$"
)


class Stage51Error(RuntimeError):
    """Fail-closed Stage5.1 generation or validation error."""


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_json(value: Any) -> bytes:
    """Return canonical JSON bytes without a trailing newline."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_json_pretty(value: Any) -> bytes:
    """Return stable human-readable JSON bytes with one final LF."""

    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def canonical_jsonl(records: Iterable[Mapping[str, Any]]) -> bytes:
    rows = [canonical_json(dict(record)) for record in records]
    return b"\n".join(rows) + (b"\n" if rows else b"")


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise Stage51Error(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json(raw: bytes, label: str) -> Any:
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_strict_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Stage51Error(f"{label}: invalid strict UTF-8 JSON: {exc}") from exc


def strict_jsonl(raw: bytes, label: str) -> list[dict[str, Any]]:
    # The canonical serialization of an empty sequence is zero bytes.  A
    # single LF would be an empty JSON row and is therefore invalid.
    if raw == b"":
        return []
    if raw and not raw.endswith(b"\n"):
        raise Stage51Error(f"{label}: JSONL lacks final LF")
    rows: list[dict[str, Any]] = []
    for index, line in enumerate(raw.splitlines(), start=1):
        value = strict_json(line, f"{label}:{index}")
        if not isinstance(value, dict):
            raise Stage51Error(f"{label}:{index}: row is not an object")
        if canonical_json(value) != line:
            raise Stage51Error(f"{label}:{index}: row is not canonical JSON")
        rows.append(value)
    return rows


def seal_object(value: Mapping[str, Any], field: str = "authority_sha256") -> dict[str, Any]:
    body = dict(value)
    if field in body:
        raise Stage51Error(f"cannot seal object already containing {field}")
    body[field] = sha256_bytes(canonical_json(body))
    return body


def seal_record(value: Mapping[str, Any]) -> dict[str, Any]:
    return seal_object(value, "record_sha256")


def verify_seal(value: Mapping[str, Any], label: str, field: str = "authority_sha256") -> None:
    observed = value.get(field)
    if not isinstance(observed, str) or not SHA256_RE.fullmatch(observed):
        raise Stage51Error(f"{label}: missing or malformed {field}")
    body = dict(value)
    del body[field]
    expected = sha256_bytes(canonical_json(body))
    if observed != expected:
        raise Stage51Error(f"{label}: {field} mismatch")


def validate_timestamp(value: str) -> str:
    if not RFC3339_RE.fullmatch(value):
        raise Stage51Error("--generated-at must be whole-second RFC3339 UTC")
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise Stage51Error("--generated-at is not a real UTC instant") from exc
    return value


def validate_relative_path(value: str, label: str = "path") -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise Stage51Error(f"{label}: invalid repository-relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise Stage51Error(f"{label}: path escapes or is not normalized: {value}")
    return value


def set_digest(values: Iterable[str]) -> str:
    ordered = sorted(values)
    if len(ordered) != len(set(ordered)):
        raise Stage51Error("cannot compute set digest over duplicate values")
    return sha256_bytes(canonical_json(ordered))


_NUMERIC_SUBJECT_ID = re.compile(r"^S51-SUB-([0-9]{8})$")


def subject_stable_key(node: Mapping[str, Any]) -> str:
    """Return the immutable scheme/edition/notation/source node identity."""

    payload = {
        "scheme": node.get("scheme"),
        "edition": node.get("edition"),
        "notation": node.get("notation"),
        "source_identity": node.get("subject_key"),
    }
    if not isinstance(payload["scheme"], str) or not isinstance(payload["source_identity"], str):
        raise Stage51Error("subject stable key lacks scheme or source identity")
    return "s51-subject:" + sha256_bytes(canonical_json(payload))


def assign_subject_node_ids(
    nodes: Sequence[Mapping[str, Any]],
    predecessor_registry: Sequence[Mapping[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Reuse predecessor IDs and allocate new numeric IDs above its maximum."""

    previous = list(predecessor_registry or ())
    by_key: dict[str, str] = {}
    by_id: dict[str, str] = {}
    max_ordinal = -1
    for row in previous:
        key, subject_id = row.get("stable_key"), row.get("subject_id")
        if not isinstance(key, str) or not isinstance(subject_id, str):
            raise Stage51Error("subject ID registry row lacks stable_key or subject_id")
        if key in by_key or subject_id in by_id:
            raise Stage51Error("subject ID registry has duplicate stable key or subject ID")
        by_key[key], by_id[subject_id] = subject_id, key
        match = _NUMERIC_SUBJECT_ID.fullmatch(subject_id)
        if match:
            max_ordinal = max(max_ordinal, int(match.group(1)))

    current_keys: dict[str, Mapping[str, Any]] = {}
    for node in nodes:
        key = subject_stable_key(node)
        if key in current_keys:
            raise Stage51Error("subject nodes have duplicate stable keys")
        current_keys[key] = node

    if not previous:
        for key, node in current_keys.items():
            subject_id = node.get("subject_id")
            if not isinstance(subject_id, str) or subject_id in by_id:
                raise Stage51Error("release 1.0 subject nodes have duplicate or missing IDs")
            by_key[key], by_id[subject_id] = subject_id, key
    else:
        if set(by_key) - set(current_keys):
            raise Stage51Error("subject ID registry contains stale predecessor stable keys")
        for key in sorted(set(current_keys) - set(by_key)):
            max_ordinal += 1
            subject_id = f"S51-SUB-{max_ordinal:08d}"
            if subject_id in by_id:
                raise Stage51Error("subject ID append allocation collides with predecessor")
            by_key[key], by_id[subject_id] = subject_id, key

    rewritten: list[dict[str, Any]] = []
    registry: list[dict[str, Any]] = []
    for key, node in current_keys.items():
        subject_id = by_key[key]
        value = dict(node)
        value["subject_id"] = subject_id
        rewritten.append(value)
        registry.append(seal_record({
            "schema_version": "awesome-theorems/stage5-1-organization/subject-node-id-registry/1.0",
            "stable_key": key, "subject_id": subject_id,
            "scheme": node.get("scheme"), "edition": node.get("edition"),
            "notation": node.get("notation"), "source_identity": node.get("subject_key"),
        }))
    rewritten.sort(key=lambda row: str(row["subject_id"]))
    registry.sort(key=lambda row: str(row["subject_id"]))
    return rewritten, registry


@dataclass(frozen=True)
class BlueprintRow:
    item_id: str
    title: str
    dependencies: tuple[str, ...]
    owned_paths: tuple[str, ...]
    gate: str
    state: str = " "

    def render(self) -> str:
        dependencies = ",".join(self.dependencies) if self.dependencies else "-"
        paths = ",".join(self.owned_paths) if self.owned_paths else "-"
        return (
            f"- [{self.state}] `{self.item_id}` {self.title} "
            f"| depends_on={dependencies} | owned_paths={paths} | gate={self.gate}"
        )


def _split_cell(value: str) -> tuple[str, ...]:
    return () if value == "-" else tuple(value.split(","))


def parse_blueprint_rows(raw: bytes, begin: str, end: str, label: str) -> list[BlueprintRow]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Stage51Error(f"{label}: Blueprint is not UTF-8") from exc
    if text.count(begin) != 1 or text.count(end) != 1 or text.index(begin) >= text.index(end):
        raise Stage51Error(f"{label}: checklist markers missing, duplicated, or reversed")
    region = text.split(begin, 1)[1].split(end, 1)[0]
    rows: list[BlueprintRow] = []
    # Checklist gates can be several kilobytes.  Python 3.12's regex engine
    # exhibits pathological backtracking for the previous monolithic pattern;
    # parse the fixed delimiters linearly, then validate each component.
    row_prefix = re.compile(r"^- \[(?P<state>[ _x])\] `(?P<item_id>[A-Z0-9-]+)` (?P<body>.*)$")
    for line_number, line in enumerate(region.splitlines(), start=1):
        if not line:
            continue
        match = row_prefix.fullmatch(line)
        if match is None:
            raise Stage51Error(f"{label}: malformed checklist line {line_number}")
        body = match.group("body")
        marker_depends = " | depends_on="
        marker_paths = " | owned_paths="
        marker_gate = " | gate="
        if (body.count(marker_depends) != 1 or body.count(marker_paths) != 1
                or body.count(marker_gate) != 1):
            raise Stage51Error(f"{label}: malformed checklist cells at line {line_number}")
        title, tail = body.split(marker_depends, 1)
        depends, tail = tail.split(marker_paths, 1)
        paths, gate = tail.split(marker_gate, 1)
        if not title or not depends or not paths or not gate:
            raise Stage51Error(f"{label}: empty checklist cell at line {line_number}")
        rows.append(
            BlueprintRow(
                item_id=match.group("item_id"),
                title=title,
                dependencies=_split_cell(depends),
                owned_paths=_split_cell(paths),
                gate=gate,
                state=match.group("state"),
            )
        )
    ids = [row.item_id for row in rows]
    if len(ids) != len(set(ids)):
        raise Stage51Error(f"{label}: duplicate checklist ID")
    return rows


def expected_gantt_path(blueprint_path: str) -> str:
    path = PurePosixPath(validate_relative_path(blueprint_path, "Blueprint path"))
    if path.stem.endswith("Blueprint"):
        stem = path.stem[: -len("Blueprint")] + "Gantt"
    else:
        stem = path.stem + "_Gantt"
    return (path.parent / (stem + path.suffix)).as_posix()


def validate_dag(rows: Sequence[BlueprintRow], label: str) -> None:
    by_id = {row.item_id: row for row in rows}
    if len(by_id) != len(rows):
        raise Stage51Error(f"{label}: duplicate item ID")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(item_id: str) -> None:
        if item_id in visiting:
            raise Stage51Error(f"{label}: dependency cycle at {item_id}")
        if item_id in visited:
            return
        visiting.add(item_id)
        for dependency in by_id[item_id].dependencies:
            if dependency not in by_id:
                raise Stage51Error(f"{label}: unknown dependency {dependency}")
            visit(dependency)
        visiting.remove(item_id)
        visited.add(item_id)

    for item_id in by_id:
        visit(item_id)


def validate_subject_tree(nodes: Sequence[Mapping[str, Any]], root_subject_id: str) -> None:
    by_id = {node.get("subject_id"): node for node in nodes}
    if len(by_id) != len(nodes) or None in by_id:
        raise Stage51Error("subject taxonomy has duplicate or missing IDs")
    if root_subject_id not in by_id or by_id[root_subject_id].get("parent_subject_id") is not None:
        raise Stage51Error("subject taxonomy root missing or has a parent")
    for subject_id, node in by_id.items():
        parent = node.get("parent_subject_id")
        if subject_id != root_subject_id and parent not in by_id:
            raise Stage51Error(f"subject {subject_id} has unknown parent {parent}")
    for subject_id in by_id:
        seen: set[str] = set()
        cursor: str | None = subject_id
        while cursor is not None:
            if cursor in seen:
                raise Stage51Error(f"subject taxonomy cycle at {cursor}")
            seen.add(cursor)
            cursor = by_id[cursor].get("parent_subject_id")
        if root_subject_id not in seen:
            raise Stage51Error(f"subject {subject_id} is disconnected from root")


def _json_at(bundle: Mapping[str, bytes], path: str) -> dict[str, Any]:
    if path not in bundle:
        raise Stage51Error(f"bundle lacks {path}")
    value = strict_json(bundle[path], path)
    if not isinstance(value, dict):
        raise Stage51Error(f"{path}: expected JSON object")
    return value


def validate_release_bundle(root: Path, bundle: Mapping[str, bytes]) -> None:
    """Validate cross-artifact invariants independent of project heuristics."""

    for path, raw in bundle.items():
        validate_relative_path(path, "bundle path")
        if path.endswith((".json", ".jsonl", ".md")) and raw and not raw.endswith(b"\n"):
            raise Stage51Error(f"{path}: generated text lacks final LF")

    object_path = next((p for p in bundle if p.endswith("/Object_Index.jsonl")), None)
    crosswalk_path = next((p for p in bundle if p.endswith("/Mathematical_ID_Crosswalk.jsonl")), None)
    assignment_path = next((p for p in bundle if p.endswith("/Subject_Assignments.jsonl")), None)
    assessment_path = next((p for p in bundle if p.endswith("/Dependency_Assessments.jsonl")), None)
    taxonomy_path = next((p for p in bundle if p.endswith("/Subject_Taxonomy.json")), None)
    hard_path = next((p for p in bundle if p.endswith("/Execution_Hard_DAG.json")), None)
    required = [object_path, crosswalk_path, assignment_path, assessment_path, taxonomy_path, hard_path]
    if any(path is None for path in required):
        raise Stage51Error("bundle is missing a core organization artifact")

    objects = strict_jsonl(bundle[object_path], object_path)  # type: ignore[index]
    crosswalk = strict_jsonl(bundle[crosswalk_path], crosswalk_path)  # type: ignore[index]
    assignments = strict_jsonl(bundle[assignment_path], assignment_path)  # type: ignore[index]
    assessments = strict_jsonl(bundle[assessment_path], assessment_path)  # type: ignore[index]
    taxonomy = _json_at(bundle, taxonomy_path)  # type: ignore[arg-type]
    nodes_path = taxonomy.get("nodes_path")
    if not isinstance(nodes_path, str) or nodes_path not in bundle:
        raise Stage51Error("subject taxonomy lacks its external node authority")
    nodes = strict_jsonl(bundle[nodes_path], nodes_path)
    if taxonomy.get("nodes_sha256") != sha256_bytes(bundle[nodes_path]):
        raise Stage51Error("subject taxonomy node authority digest mismatch")
    hard = _json_at(bundle, hard_path)  # type: ignore[arg-type]
    for index, record in enumerate(objects):
        verify_seal(record, f"object:{index}", "record_sha256")
    for label, records in (("crosswalk", crosswalk), ("assignment", assignments), ("assessment", assessments), ("subject", nodes)):
        for index, record in enumerate(records):
            verify_seal(record, f"{label}:{index}", "record_sha256")
    object_ids = [row.get("object_id") for row in objects]
    if len(objects) != 19790 or len(object_ids) != len(set(object_ids)):
        raise Stage51Error("object index must contain exactly 19,790 unique members")
    if {row.get("object_id") for row in crosswalk} != set(object_ids):
        raise Stage51Error("mathematical ID crosswalk does not exactly cover object index")
    if {row.get("object_id") for row in assignments} != set(object_ids):
        raise Stage51Error("subject assignments do not exactly cover object index")
    if {row.get("object_id") for row in assessments} != set(object_ids):
        raise Stage51Error("dependency assessments do not exactly cover object index")
    validate_subject_tree(nodes, taxonomy.get("root_subject_id"))
    verify_seal(taxonomy, "subject taxonomy")
    verify_seal(hard, "execution hard DAG")
    item_ids = {row.get("stage51_item_id") for row in objects}
    if set(hard.get("nodes", [])) != item_ids:
        raise Stage51Error("hard DAG node set differs from member item set")
    for edge in hard.get("edges", []):
        if not isinstance(edge, dict) or edge.get("consumer_member_id") not in set(object_ids) or edge.get("provider_member_id") not in set(object_ids):
            raise Stage51Error("hard DAG contains malformed or unknown endpoint")
        if edge.get("evidence_tier") not in {"A2_target_owned_replay", "B_content_bound_artifact"} or edge.get("blocking") is not True:
            raise Stage51Error("hard DAG contains an inadmissible edge")

    legacy_path = next((p for p in bundle if p.endswith("/Legacy_Checklist_Row_Crosswalk.jsonl")), None)
    if legacy_path is None or len(strict_jsonl(bundle[legacy_path], legacy_path)) != 20197:
        raise Stage51Error("legacy checklist crosswalk must contain exactly 20,197 rows")

    for blueprint_path in (
        "Docs/Stage5_1_Theorems_Blueprint.md",
        "Docs/Stage5_1_Conjectures_Blueprint.md",
    ):
        gantt_path = expected_gantt_path(blueprint_path)
        if blueprint_path not in bundle or gantt_path not in bundle:
            raise Stage51Error(f"bundle lacks same-prefix pair for {blueprint_path}")
        rows = parse_blueprint_rows(
            bundle[blueprint_path],
            "<!-- STAGE5-1-EXECUTION-CHECKLIST:BEGIN -->",
            "<!-- STAGE5-1-EXECUTION-CHECKLIST:END -->",
            blueprint_path,
        )
        if any(row.state != " " for row in rows):
            raise Stage51Error(f"{blueprint_path}: initial cursor is not all blank")
        validate_dag(rows, blueprint_path)
        gantt_text = bundle[gantt_path].decode("utf-8")
        monitored = re.findall(r'^\| `([A-Z0-9-]+)` \|', gantt_text, re.MULTILINE)
        if monitored != [row.item_id for row in rows]:
            raise Stage51Error(f"{gantt_path}: monitoring rows do not exactly cover Blueprint order")
        if re.search(r"^- \[[ _x]\]", gantt_text, re.MULTILINE):
            raise Stage51Error(f"{gantt_path}: generated Gantt contains mutable checkbox syntax")
        lower = bundle[blueprint_path].lower()
        forbidden = (b"concurrency_default", b"default_concurrency", b"worker_count_default")
        if any(token in lower for token in forbidden):
            raise Stage51Error(f"{blueprint_path}: concurrency default token present")


def bundle_digest(bundle: Mapping[str, bytes], paths: Iterable[str] | None = None) -> str:
    selected = sorted(paths if paths is not None else bundle)
    return sha256_bytes(
        canonical_json(
            [
                {"path": path, "sha256": sha256_bytes(bundle[path]), "size_bytes": len(bundle[path])}
                for path in selected
            ]
        )
    )


def compare_bundle(root: Path, bundle: Mapping[str, bytes]) -> list[str]:
    differences: list[str] = []
    for relative, expected in sorted(bundle.items()):
        path = root / relative
        if not path.is_file() or path.is_symlink():
            differences.append(f"missing_or_nonregular:{relative}")
            continue
        observed = path.read_bytes()
        if observed != expected:
            differences.append(
                f"byte_drift:{relative}:expected={sha256_bytes(expected)}:observed={sha256_bytes(observed)}"
            )
    release_directories = {
        (root / relative).parent
        for relative in bundle
        if "/releases/" in relative and relative.endswith((".json", ".jsonl"))
    }
    expected_paths = {(root / relative).resolve() for relative in bundle}
    for directory in sorted(release_directories):
        if not directory.is_dir():
            continue
        for candidate in directory.iterdir():
            if candidate.is_file() and candidate.resolve() not in expected_paths:
                differences.append(f"unexpected_release_file:{candidate.relative_to(root).as_posix()}")
    return differences


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_bundle_transaction(root: Path, bundle: Mapping[str, bytes]) -> str:
    """Install a bundle with a durable replay journal and Current pointer last.

    Existing differing destinations are rejected.  Therefore an immutable
    release can be replayed byte-for-byte but never silently rewritten.
    """

    transaction_root = root / "Docs/catalog/stage5_1_organization/.transactions"
    transaction_root.mkdir(parents=True, exist_ok=True)
    lock_path = root / "Docs/catalog/stage5_1_organization/.build.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as lock_stream:
        fcntl.flock(lock_stream.fileno(), fcntl.LOCK_EX)
        digest = bundle_digest(bundle)
        transaction = transaction_root / digest
        stage = transaction / "stage"
        manifest_path = transaction / "transaction.json"
        if transaction.exists() and manifest_path.is_file():
            manifest = strict_json(manifest_path.read_bytes(), "transaction manifest")
            if not isinstance(manifest, dict) or manifest.get("bundle_sha256") != digest:
                raise Stage51Error("stale transaction identity collision")
        else:
            if transaction.exists():
                shutil.rmtree(transaction)
            stage.mkdir(parents=True)
            for relative, raw in sorted(bundle.items()):
                destination = root / relative
                if destination.exists():
                    if destination.is_symlink() or not destination.is_file():
                        raise Stage51Error(f"destination is not a regular file: {relative}")
                    if destination.read_bytes() != raw:
                        raise Stage51Error(f"append-only destination already has different bytes: {relative}")
                staged = stage / relative
                staged.parent.mkdir(parents=True, exist_ok=True)
                with staged.open("wb") as stream:
                    stream.write(raw)
                    stream.flush()
                    os.fsync(stream.fileno())
            manifest = seal_object(
                {
                    "schema_version": "awesome-theorems/stage5.1-build-transaction/1.0",
                    "bundle_sha256": digest,
                    "outputs": [
                        {"path": path, "sha256": sha256_bytes(bundle[path]), "size_bytes": len(bundle[path])}
                        for path in sorted(bundle)
                    ],
                    "current_pointer_last": "Docs/catalog/stage5_1_organization/Current_Release.json",
                }
            )
            with manifest_path.open("wb") as stream:
                stream.write(canonical_json_pretty(manifest))
                stream.flush()
                os.fsync(stream.fileno())
            _fsync_directory(transaction)

        current = "Docs/catalog/stage5_1_organization/Current_Release.json"
        order = [path for path in sorted(bundle) if path != current] + ([current] if current in bundle else [])
        for relative in order:
            destination = root / relative
            expected = bundle[relative]
            if destination.is_file() and not destination.is_symlink() and destination.read_bytes() == expected:
                continue
            staged = stage / relative
            if not staged.is_file():
                staged.parent.mkdir(parents=True, exist_ok=True)
                with staged.open("wb") as stream:
                    stream.write(expected)
                    stream.flush()
                    os.fsync(stream.fileno())
            if sha256_bytes(staged.read_bytes()) != sha256_bytes(expected):
                raise Stage51Error(f"transaction staging drift for {relative}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staged, destination)
            _fsync_directory(destination.parent)
        differences = compare_bundle(root, bundle)
        if differences:
            raise Stage51Error(f"post-install bundle verification failed: {differences[:3]}")
        shutil.rmtree(transaction)
        try:
            transaction_root.rmdir()
        except OSError:
            pass
        return digest


__all__ = [
    "BlueprintRow",
    "Stage51Error",
    "bundle_digest",
    "canonical_json",
    "canonical_json_pretty",
    "canonical_jsonl",
    "compare_bundle",
    "expected_gantt_path",
    "parse_blueprint_rows",
    "seal_object",
    "seal_record",
    "assign_subject_node_ids",
    "set_digest",
    "sha256_bytes",
    "strict_json",
    "strict_jsonl",
    "subject_stable_key",
    "validate_dag",
    "validate_relative_path",
    "validate_release_bundle",
    "validate_subject_tree",
    "validate_timestamp",
    "verify_seal",
    "write_bundle_transaction",
]
