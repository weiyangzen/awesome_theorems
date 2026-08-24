#!/usr/bin/env python3
"""Read-only release checker for the Stage5.1 organization overlay.

This checker intentionally does not delegate acceptance to the builder's
``--check`` command.  It validates the bytes already on disk, independently
checks the release invariants, and then asks the deterministic builder for an
in-memory reconstruction to detect source-input drift.  It never writes a
release artifact.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any, Iterable, Mapping, Sequence

from jsonschema import Draft202012Validator, RefResolver


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RELEASE = "1.0"
CATALOG_ROOT = PurePosixPath("Docs/catalog/stage5_1_organization")
CURRENT_PATH = CATALOG_ROOT / "Current_Release.json"
RELEASE_FILES = (
    "Source_Input_Manifest.json",
    "Subject_Taxonomy.json",
    "Subject_Nodes.jsonl",
    "Subject_Node_ID_Registry.jsonl",
    "Object_Index.jsonl",
    "Mathematical_ID_Crosswalk.jsonl",
    "Legacy_Checklist_Row_Crosswalk.jsonl",
    "Subject_Assignments.jsonl",
    "Dependency_Assessments.jsonl",
    "Relation_Edges.jsonl",
    "Execution_Hard_DAG.json",
    "Dependency_Closure.jsonl",
    "Cross_Domain_Edges.jsonl",
    "programs/theorems/Organization_Workset.jsonl",
    "programs/conjectures/Organization_Workset.jsonl",
    "Organization_Manifest.json",
)
PROJECTION_FILES = (
    "Docs/Stage5_1_Theorems_Blueprint.md",
    "Docs/Stage5_1_Theorems_Gantt.md",
    "Docs/Stage5_1_Conjectures_Blueprint.md",
    "Docs/Stage5_1_Conjectures_Gantt.md",
)
EXPECTED_MEMBER_COUNT = 19_790
EXPECTED_LEGACY_ROW_COUNT = 20_197
EXPECTED_PROGRAM_COUNTS = {"theorems": 3_500, "conjectures": 16_290}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
BLUEPRINT_ROW_RE = re.compile(
    r"^- \[(?P<state>[ _x])\] `(?P<id>[A-Z0-9_.:-]+)`\s+"
    r"(?P<title>.+?)\s+\|\s*depends_on=(?P<depends>[^|]+?)\s+"
    r"\|\s*owned_paths=(?P<paths>[^|]+?)\s+\|\s*gate=(?P<gate>.+)$"
)
CHECKBOX_RE = re.compile(r"(?m)^\s*-\s*\[[ _xX]\]")
JSON_FENCE_RE = re.compile(r"```json\s*\n(?P<body>.*?)\n```", re.DOTALL)


class ReleaseCheckError(RuntimeError):
    """A fail-closed Stage5.1 release violation."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReleaseCheckError(message)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_json(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ReleaseCheckError("value is not canonical finite JSON") from exc


def strict_json(raw: bytes, label: str) -> Any:
    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"{label}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    def reject_constant(value: str) -> Any:
        raise ReleaseCheckError(f"{label}: non-finite number {value}")

    try:
        return json.loads(
            raw,
            object_pairs_hook=pairs_hook,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReleaseCheckError(f"{label}: invalid strict UTF-8 JSON") from exc


def strict_jsonl(raw: bytes, label: str) -> list[dict[str, Any]]:
    if raw == b"":
        return []
    require(raw.endswith(b"\n"), f"{label}: JSONL must end with LF")
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(raw.splitlines(), 1):
        require(bool(line), f"{label}:{number}: blank JSONL row")
        value = strict_json(line, f"{label}:{number}")
        require(isinstance(value, dict), f"{label}:{number}: row must be an object")
        require(canonical_json(value) == line,
                f"{label}:{number}: row is not canonical compact JSON")
        rows.append(value)
    return rows


def _safe_repo_path(root: Path, relative: str, label: str) -> Path:
    posix = PurePosixPath(relative)
    require(
        not posix.is_absolute() and ".." not in posix.parts,
        f"{label}: path is not repository-relative: {relative!r}",
    )
    path = root.joinpath(*posix.parts)
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise ReleaseCheckError(f"{label}: path escapes repository root") from exc
    return path


def _load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ReleaseCheckError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # pragma: no cover - normalized at the CLI boundary
        raise ReleaseCheckError(f"cannot import {path}: {exc}") from exc
    return module


def _first_string(row: Mapping[str, Any], names: Sequence[str], label: str) -> str:
    present = [row[name] for name in names if isinstance(row.get(name), str)]
    require(bool(present), f"{label}: missing one of {', '.join(names)}")
    require(len(set(present)) == 1, f"{label}: conflicting identity aliases")
    return present[0]


def _optional_string(row: Mapping[str, Any], names: Sequence[str]) -> str | None:
    present = [row[name] for name in names if isinstance(row.get(name), str)]
    if not present:
        return None
    require(len(set(present)) == 1, "conflicting string aliases")
    return present[0]


def member_id(row: Mapping[str, Any], label: str = "row") -> str:
    return _first_string(row, ("object_id",), label)


def subject_id(row: Mapping[str, Any], label: str = "subject") -> str:
    return _first_string(row, ("subject_id",), label)


def _record_id(row: Mapping[str, Any]) -> str | None:
    for name in ("edge_id", "object_id", "stage51_item_id", "legacy_item_id", "subject_id"):
        if isinstance(row.get(name), str):
            return row[name]
    return None


def _verify_inline_record_seal(row: Mapping[str, Any], label: str) -> None:
    """Verify common seal spellings without requiring every row to be sealed."""

    for seal_key in ("authority_sha256", "record_sha256"):
        seal = row.get(seal_key)
        if seal is None:
            continue
        require(isinstance(seal, str) and SHA256_RE.fullmatch(seal) is not None,
                f"{label}: malformed {seal_key}")
        body = dict(row)
        body.pop(seal_key)
        require(sha256_bytes(canonical_json(body)) == seal,
                f"{label}: {seal_key} mismatch")


@dataclass(frozen=True)
class ReleaseSnapshot:
    root: Path
    release: str
    release_prefix: PurePosixPath
    raw: dict[str, bytes]
    documents: dict[str, Any]

    def rows(self, name: str) -> list[dict[str, Any]]:
        value = self.documents[name]
        require(isinstance(value, list), f"{name}: expected JSONL rows")
        return value

    def obj(self, name: str) -> dict[str, Any]:
        value = self.documents[name]
        require(isinstance(value, dict), f"{name}: expected JSON object")
        return value


def load_snapshot(root: Path, release: str) -> ReleaseSnapshot:
    release_prefix = CATALOG_ROOT / "releases" / release
    paths = [str(release_prefix / name) for name in RELEASE_FILES]
    paths.extend(PROJECTION_FILES)
    paths.append(str(CURRENT_PATH))
    paths.append(str(CATALOG_ROOT / "migrations" / f"stage5-v2_to_stage5_1-{release}.json"))
    raw: dict[str, bytes] = {}
    documents: dict[str, Any] = {}
    for relative in paths:
        path = _safe_repo_path(root, relative, relative)
        require(path.is_file() and not path.is_symlink(), f"missing regular release file: {relative}")
        payload = path.read_bytes()
        raw[relative] = payload
        if relative.endswith(".jsonl"):
            documents[relative] = strict_jsonl(payload, relative)
        elif relative.endswith(".json"):
            documents[relative] = strict_json(payload, relative)
        else:
            try:
                documents[relative] = payload.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ReleaseCheckError(f"{relative}: invalid UTF-8 Markdown") from exc
    return ReleaseSnapshot(root, release, release_prefix, raw, documents)


def _doc_name(snapshot: ReleaseSnapshot, suffix: str) -> str:
    name = str(snapshot.release_prefix / suffix)
    require(name in snapshot.documents, f"release document not loaded: {name}")
    return name


def _walk_path_hashes(value: Any) -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        yielded: set[tuple[str, str]] = set()
        path = next(
            (value.get(key) for key in ("path", "artifact_path", "file_path", "relative_path")
             if isinstance(value.get(key), str)),
            None,
        )
        digest = next(
            (value.get(key) for key in ("sha256", "file_sha256", "artifact_sha256", "input_sha256")
             if isinstance(value.get(key), str)),
            None,
        )
        if path is not None and digest is not None:
            yielded.add((path, digest))
        for key, candidate_path in value.items():
            if not key.endswith("_path") or not isinstance(candidate_path, str):
                continue
            candidate_digest = value.get(key[:-5] + "_sha256")
            if isinstance(candidate_digest, str):
                yielded.add((candidate_path, candidate_digest))
        yield from sorted(yielded)
        for child in value.values():
            yield from _walk_path_hashes(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_path_hashes(child)


def _verify_path_hashes(
    root: Path,
    value: Any,
    label: str,
    *,
    captured_raw: Mapping[str, bytes] | None = None,
) -> set[str]:
    seen: set[str] = set()
    for relative, digest in _walk_path_hashes(value):
        require(SHA256_RE.fullmatch(digest) is not None, f"{label}: malformed digest for {relative}")
        if captured_raw is not None and relative in captured_raw:
            raw = captured_raw[relative]
        else:
            path = _safe_repo_path(root, relative, label)
            require(path.is_file() and not path.is_symlink(),
                    f"{label}: missing hashed input/output {relative}")
            raw = path.read_bytes()
        require(sha256_bytes(raw) == digest, f"{label}: hash drift for {relative}")
        seen.add(relative)
    return seen


SCHEMA_BINDINGS: dict[str, str] = {
    "Source_Input_Manifest.json": "source-input.schema.json",
    "Subject_Taxonomy.json": "taxonomy.schema.json",
    "Subject_Nodes.jsonl": "subject-node.schema.json",
    "Subject_Node_ID_Registry.jsonl": "subject-node-id-registry.schema.json",
    "Object_Index.jsonl": "object-index.schema.json",
    "Mathematical_ID_Crosswalk.jsonl": "id-crosswalk.schema.json",
    "Legacy_Checklist_Row_Crosswalk.jsonl": "checklist-crosswalk.schema.json",
    "Subject_Assignments.jsonl": "subject-assignment.schema.json",
    "Dependency_Assessments.jsonl": "dependency-assessment.schema.json",
    "Relation_Edges.jsonl": "relation-edge.schema.json",
    "Execution_Hard_DAG.json": "execution-hard-dag.schema.json",
    "Dependency_Closure.jsonl": "dependency-closure.schema.json",
    "Cross_Domain_Edges.jsonl": "cross-domain-edge.schema.json",
    "programs/theorems/Organization_Workset.jsonl": "organization-workset.schema.json",
    "programs/conjectures/Organization_Workset.jsonl": "organization-workset.schema.json",
    "Organization_Manifest.json": "organization-manifest.schema.json",
}


def validate_json_schemas(snapshot: ReleaseSnapshot) -> None:
    schema_root = snapshot.root / "Docs/catalog/stage5_1_organization/schemas"
    require(schema_root.is_dir(), "Stage5.1 JSON schema directory missing")
    schemas: dict[str, dict[str, Any]] = {}
    store: dict[str, dict[str, Any]] = {}
    for path in sorted(schema_root.glob("*.schema.json")):
        value = strict_json(path.read_bytes(), path.relative_to(snapshot.root).as_posix())
        require(isinstance(value, dict) and isinstance(value.get("$id"), str),
                f"{path.name}: schema lacks an absolute $id")
        try:
            Draft202012Validator.check_schema(value)
        except Exception as exc:
            raise ReleaseCheckError(f"{path.name}: invalid Draft 2020-12 schema: {exc}") from exc
        schemas[path.name] = value
        store[value["$id"]] = value

    def check(value: Any, schema_name: str, label: str) -> None:
        require(schema_name in schemas, f"missing release schema {schema_name}")
        schema = schemas[schema_name]
        validator = Draft202012Validator(
            schema,
            resolver=RefResolver.from_schema(schema, store=store),
        )
        errors = sorted(validator.iter_errors(value), key=lambda error: list(error.absolute_path))
        if errors:
            error = errors[0]
            locator = "/" + "/".join(str(part) for part in error.absolute_path)
            raise ReleaseCheckError(f"{label}{locator}: schema violation: {error.message}")

    for suffix, schema_name in SCHEMA_BINDINGS.items():
        name = _doc_name(snapshot, suffix)
        value = snapshot.documents[name]
        if isinstance(value, list):
            for index, row in enumerate(value):
                check(row, schema_name, f"{name}:{index + 1}")
        else:
            check(value, schema_name, name)
    current_name = str(CURRENT_PATH)
    check(snapshot.documents[current_name], "current-release.schema.json", current_name)
    migration_name = str(
        CATALOG_ROOT / "migrations" / f"stage5-v2_to_stage5_1-{snapshot.release}.json"
    )
    check(snapshot.documents[migration_name], "migration.schema.json", migration_name)


def validate_current_manifest_and_inputs(snapshot: ReleaseSnapshot) -> None:
    current_name = str(CURRENT_PATH)
    current = snapshot.obj(current_name)
    _verify_inline_record_seal(current, current_name)
    release_value = _optional_string(
        current, ("organization_release", "release", "current_release", "release_id"),
    )
    require(release_value == snapshot.release, "Current_Release does not select the checked release")

    manifest_name = _doc_name(snapshot, "Organization_Manifest.json")
    manifest = snapshot.obj(manifest_name)
    _verify_inline_record_seal(manifest, manifest_name)
    input_name = _doc_name(snapshot, "Source_Input_Manifest.json")
    inputs = snapshot.obj(input_name)
    _verify_inline_record_seal(inputs, input_name)
    migration_name = str(
        CATALOG_ROOT / "migrations" / f"stage5-v2_to_stage5_1-{snapshot.release}.json"
    )
    migration = snapshot.obj(migration_name)
    _verify_inline_record_seal(migration, migration_name)

    manifest_paths = _verify_path_hashes(
        snapshot.root, manifest, manifest_name, captured_raw=snapshot.raw,
    )
    input_paths = _verify_path_hashes(
        snapshot.root, inputs, input_name, captured_raw=snapshot.raw,
    )
    required_release_paths = {
        str(snapshot.release_prefix / name) for name in RELEASE_FILES
        if name != "Organization_Manifest.json"
    }
    required_release_paths.update(PROJECTION_FILES)
    require(required_release_paths <= manifest_paths,
            "Organization_Manifest does not hash every declared release projection")
    require(bool(input_paths), "Source_Input_Manifest contains no content-bound inputs")
    input_entries = inputs.get("inputs")
    require(isinstance(input_entries, list) and
            inputs.get("input_root_sha256") == sha256_bytes(canonical_json(input_entries)),
            "Source_Input_Manifest input_root_sha256 differs")
    for entry in input_entries:
        require(isinstance(entry, dict) and isinstance(entry.get("path"), str),
                "Source_Input_Manifest input row malformed")
        path = _safe_repo_path(snapshot.root, entry["path"], "source input")
        require(path.stat().st_size == entry.get("size_bytes"),
                f"Source_Input_Manifest size drift for {entry['path']}")

    artifacts = manifest.get("artifacts")
    require(isinstance(artifacts, list), "Organization_Manifest artifacts malformed")
    candidate_entries: list[dict[str, Any]] = []
    for artifact in artifacts:
        require(isinstance(artifact, dict), "Organization_Manifest artifact row malformed")
        path_value = artifact.get("path")
        require(isinstance(path_value, str), "Organization_Manifest artifact path malformed")
        raw = snapshot.raw.get(path_value)
        if raw is None:
            path = _safe_repo_path(snapshot.root, path_value, "manifest artifact")
            require(path.is_file() and not path.is_symlink(),
                    f"Organization_Manifest artifact missing: {path_value}")
            raw = path.read_bytes()
        require(len(raw) == artifact.get("size_bytes"),
                f"Organization_Manifest size drift for {path_value}")
        if isinstance(artifact.get("rows"), int):
            require(len(raw.splitlines()) == artifact["rows"],
                    f"Organization_Manifest row count drift for {path_value}")
        candidate_entries.append({
            "path": path_value,
            "sha256": artifact.get("sha256"),
            "size_bytes": artifact.get("size_bytes"),
        })
    candidate_entries.sort(key=lambda row: str(row["path"]))
    require(manifest.get("candidate_output_root_sha256") ==
            sha256_bytes(canonical_json(candidate_entries)),
            "Organization_Manifest candidate output root differs")

    # Current must bind the exact manifest, not merely name the release.
    manifest_digest = sha256_bytes(snapshot.raw[manifest_name])
    current_manifest = current.get("manifest")
    require(isinstance(current_manifest, dict) and
            current_manifest.get("path") == manifest_name and
            current_manifest.get("sha256") == manifest_digest and
            current_manifest.get("authority_sha256") == manifest.get("authority_sha256"),
            "Current_Release is not bound to the exact Organization_Manifest bytes")
    current_blueprints = current.get("blueprints")
    require(isinstance(current_blueprints, dict) and set(current_blueprints) == {"theorems", "conjectures"},
            "Current_Release Blueprint bindings malformed")
    for binding in current_blueprints.values():
        require(isinstance(binding, dict), "Current_Release Blueprint binding malformed")
        for path_key, sha_key in (
            ("path", "sha256"),
            ("gantt_path", "gantt_sha256"),
        ):
            relative = binding.get(path_key)
            digest = binding.get(sha_key)
            require(isinstance(relative, str) and isinstance(digest, str),
                    "Current_Release projection binding malformed")
            raw = snapshot.raw.get(relative)
            require(raw is not None and sha256_bytes(raw) == digest,
                    f"Current_Release projection drift: {relative}")


def _unique_rows(rows: Sequence[Mapping[str, Any]], getter: Any, label: str) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for number, row in enumerate(rows, 1):
        identity = getter(row, f"{label}:{number}")
        require(identity not in result, f"{label}: duplicate identity {identity}")
        result[identity] = row
        _verify_inline_record_seal(row, f"{label}:{identity}")
    return result


def _workset_program(row: Mapping[str, Any], fallback: str) -> str:
    value = _optional_string(row, ("program", "program_id", "object_program"))
    if value is None:
        return fallback
    lowered = value.lower()
    if "theorem" in lowered:
        return "theorems"
    if "conjecture" in lowered:
        return "conjectures"
    raise ReleaseCheckError(f"workset: unknown program {value!r}")


def validate_member_bijections(snapshot: ReleaseSnapshot) -> dict[str, Any]:
    objects = _unique_rows(
        snapshot.rows(_doc_name(snapshot, "Object_Index.jsonl")), member_id, "Object_Index",
    )
    math_crosswalk = _unique_rows(
        snapshot.rows(_doc_name(snapshot, "Mathematical_ID_Crosswalk.jsonl")),
        member_id,
        "Mathematical_ID_Crosswalk",
    )
    legacy_rows = snapshot.rows(_doc_name(snapshot, "Legacy_Checklist_Row_Crosswalk.jsonl"))
    legacy = _unique_rows(
        legacy_rows,
        lambda row, label: _first_string(row, ("legacy_item_id",), label),
        "Legacy_Checklist_Row_Crosswalk",
    )
    assignments = _unique_rows(
        snapshot.rows(_doc_name(snapshot, "Subject_Assignments.jsonl")),
        member_id,
        "Subject_Assignments",
    )
    assessments = _unique_rows(
        snapshot.rows(_doc_name(snapshot, "Dependency_Assessments.jsonl")),
        member_id,
        "Dependency_Assessments",
    )
    require(len(objects) == EXPECTED_MEMBER_COUNT,
            f"Object_Index count differs: expected {EXPECTED_MEMBER_COUNT}, got {len(objects)}")
    require(len(legacy) == EXPECTED_LEGACY_ROW_COUNT,
            f"legacy checklist row count differs: expected {EXPECTED_LEGACY_ROW_COUNT}, got {len(legacy)}")
    for name, observed in (
        ("Mathematical_ID_Crosswalk", set(math_crosswalk)),
        ("Subject_Assignments", set(assignments)),
        ("Dependency_Assessments", set(assessments)),
    ):
        require(observed == set(objects), f"{name} is not a bijection over the 19,790 members")

    worksets: dict[str, dict[str, Mapping[str, Any]]] = {}
    for program in ("theorems", "conjectures"):
        rows = snapshot.rows(_doc_name(snapshot, f"programs/{program}/Organization_Workset.jsonl"))
        indexed = _unique_rows(rows, member_id, f"{program} Organization_Workset")
        require(len(indexed) == EXPECTED_PROGRAM_COUNTS[program],
                f"{program} workset count differs")
        require(all(_workset_program(row, program) == program for row in indexed.values()),
                f"{program} workset contains a foreign program member")
        worksets[program] = indexed
    theorem_ids = set(worksets["theorems"])
    conjecture_ids = set(worksets["conjectures"])
    require(theorem_ids.isdisjoint(conjecture_ids), "program worksets overlap")
    require(theorem_ids | conjecture_ids == set(objects),
            "program worksets do not partition Object_Index")

    # Prove the 20,197-row predecessor bijection against the predecessor
    # Blueprints, not against ordering or ordinal assumptions.
    predecessor_rows: dict[str, Mapping[str, Any]] = {}
    for relative in ("Docs/Stage5_Theorems_Blueprint.md", "Docs/Stage5_Conjectures_Blueprint.md"):
        text = _safe_repo_path(snapshot.root, relative, relative).read_text(encoding="utf-8")
        rows = parse_blueprint_rows(text, relative)
        ids = {row["item_id"] for row in rows}
        require(len(ids) == len(rows), f"{relative}: duplicate predecessor checklist ID")
        require(set(predecessor_rows).isdisjoint(ids), "predecessor theorem/conjecture IDs overlap")
        predecessor_rows.update({row["item_id"]: row for row in rows})
    require(set(legacy) == set(predecessor_rows),
            "Legacy_Checklist_Row_Crosswalk is not a bijection over 20,197 predecessor rows")

    objects_by_legacy: dict[str, tuple[str, Mapping[str, Any]]] = {}
    for object_identity, row in objects.items():
        legacy_id = _first_string(row, ("legacy_item_id",), f"object {object_identity}")
        require(legacy_id not in objects_by_legacy, f"two members share legacy item {legacy_id}")
        objects_by_legacy[legacy_id] = (object_identity, row)
        crosswalk_row = math_crosswalk[object_identity]
        for key in ("legacy_item_id", "stage51_item_id", "identity_sha256"):
            require(crosswalk_row.get(key) == row.get(key),
                    f"mathematical crosswalk {object_identity} disagrees with Object_Index on {key}")
        require(crosswalk_row.get("stage51_initial_state") == "not_done" and
                crosswalk_row.get("state_transfer") == "evidence_only_revalidation_required",
                f"mathematical crosswalk {object_identity} inherits legacy state")
        require(assignments[object_identity].get("assignment_id") == row.get("subject_assignment_id"),
                f"object {object_identity} assignment binding differs")
        require(assessments[object_identity].get("assessment_id") == row.get("dependency_assessment_id"),
                f"object {object_identity} assessment binding differs")

        def ordinal(value: Any, label: str) -> str:
            require(isinstance(value, str), f"object {object_identity} lacks {label}")
            match = re.search(r"([0-9]{8})", value)
            require(match is not None, f"object {object_identity} malformed {label}")
            return match.group(1)

        expected_ordinal = ordinal(object_identity, "object_id")
        ordinal_fields = [
            (row.get("stage51_item_id"), "stage51_item_id"),
            (legacy_id, "legacy_item_id"),
            (row.get("subject_assignment_id"), "subject_assignment_id"),
            (row.get("dependency_assessment_id"), "dependency_assessment_id"),
        ]
        if row.get("object_kind") == "source_occurrence":
            ordinal_fields.append((row.get("pool_id"), "pool_id"))
        else:
            ordinal_fields.extend([
                (row.get("stage5_claim_id"), "stage5_claim_id"),
                (row.get("variant_id"), "variant_id"),
            ])
        require(all(ordinal(value, label) == expected_ordinal
                    for value, label in ordinal_fields),
                f"object {object_identity} ordinal-preserving ID crosswalk differs")

    for legacy_id, row in legacy.items():
        predecessor = predecessor_rows[legacy_id]
        expected_state = {
            " ": "not_done", "_": "handoff_waiting_master", "x": "master_accepted",
        }[predecessor["state"]]
        require(row.get("legacy_state") == expected_state,
                f"legacy crosswalk {legacy_id} predecessor state differs")
        expected_row_sha = sha256_bytes(canonical_json({
            "item_id": legacy_id,
            "title": predecessor["title"],
            "dependencies": list(predecessor["dependencies"]),
            "owned_paths": list(predecessor["owned_paths"]),
            "gate": predecessor["gate"],
        }))
        require(row.get("legacy_row_sha256") == expected_row_sha,
                f"legacy crosswalk {legacy_id} predecessor row receipt differs")
        require(row.get("stage51_initial_state") == "not_done",
                f"legacy crosswalk {legacy_id} steals predecessor completion state")
        new_ids = row.get("new_item_ids")
        require(isinstance(new_ids, list) and all(isinstance(value, str) for value in new_ids),
                f"legacy crosswalk {legacy_id} new_item_ids malformed")
        require(len(new_ids) == len(set(new_ids)),
                f"legacy crosswalk {legacy_id} repeats a successor ID")
        if legacy_id in objects_by_legacy:
            object_identity, object_row = objects_by_legacy[legacy_id]
            require(row.get("relationship") == "exact_member_successor" and
                    new_ids == [object_row.get("stage51_item_id")],
                    f"member legacy row {legacy_id} is not an exact one-to-one successor")
            require(math_crosswalk[object_identity].get("legacy_state") == expected_state,
                    f"mathematical crosswalk {object_identity} predecessor state differs")
    return {
        "objects": objects,
        "math_crosswalk": math_crosswalk,
        "legacy": legacy,
        "assignments": assignments,
        "assessments": assessments,
        "worksets": worksets,
    }


def _parent_subject(row: Mapping[str, Any]) -> str | None:
    value = row.get("parent_subject_id")
    require(value is None or isinstance(value, str), "taxonomy parent must be null or a subject ID")
    return value


def validate_taxonomy(snapshot: ReleaseSnapshot, state: Mapping[str, Any]) -> dict[str, Any]:
    taxonomy = snapshot.obj(_doc_name(snapshot, "Subject_Taxonomy.json"))
    _verify_inline_record_seal(taxonomy, "Subject_Taxonomy")
    node_rows = snapshot.rows(_doc_name(snapshot, "Subject_Nodes.jsonl"))
    nodes = _unique_rows(node_rows, subject_id, "Subject_Nodes")
    require(bool(nodes), "taxonomy contains no subject nodes")
    registry_name = _doc_name(snapshot, "Subject_Node_ID_Registry.jsonl")
    registry_rows = snapshot.rows(registry_name)
    registry_by_id = _unique_rows(registry_rows, subject_id, "Subject_Node_ID_Registry")
    registry_by_key: dict[str, Mapping[str, Any]] = {}
    for number, row in enumerate(registry_rows, 1):
        _verify_inline_record_seal(row, f"Subject_Node_ID_Registry:{number}")
        stable_key = row.get("stable_key")
        require(isinstance(stable_key, str) and stable_key not in registry_by_key,
                "Subject_Node_ID_Registry has duplicate or missing stable key")
        registry_by_key[stable_key] = row
    require(set(registry_by_id) == set(nodes),
            "Subject_Node_ID_Registry and Subject_Nodes are not an exact ID bijection")
    for identity, node in nodes.items():
        expected_key = "s51-subject:" + sha256_bytes(canonical_json({
            "scheme": node.get("scheme"), "edition": node.get("edition"),
            "notation": node.get("notation"), "source_identity": node.get("subject_key"),
        }))
        row = registry_by_id[identity]
        require(row.get("stable_key") == expected_key and
                row.get("scheme") == node.get("scheme") and
                row.get("edition") == node.get("edition") and
                row.get("notation") == node.get("notation") and
                row.get("source_identity") == node.get("subject_key"),
                f"Subject_Node_ID_Registry stable key differs for {identity}")
    evidence_digest_cache: dict[str, str] = {}

    def evidence_digest(relative: str, label: str) -> str:
        if relative not in evidence_digest_cache:
            path = _safe_repo_path(snapshot.root, relative, label)
            require(path.is_file() and not path.is_symlink(), f"{label}: evidence is not a regular file")
            evidence_digest_cache[relative] = sha256_bytes(path.read_bytes())
        return evidence_digest_cache[relative]

    for identity, node in nodes.items():
        refs = node.get("source_refs")
        require(isinstance(refs, list), f"subject {identity} source_refs malformed")
        for ref in refs:
            require(isinstance(ref, dict) and isinstance(ref.get("path"), str) and
                    isinstance(ref.get("sha256"), str),
                    f"subject {identity} source reference malformed")
            require(evidence_digest(ref["path"], f"subject {identity} source") == ref["sha256"],
                    f"subject {identity} source reference drift")
    parents = {identity: _parent_subject(row) for identity, row in nodes.items()}
    roots = [identity for identity, parent in parents.items() if parent is None]
    require(len(roots) == 1, f"taxonomy must have exactly one root, found {len(roots)}")
    root = roots[0]
    for identity, parent in parents.items():
        require(parent is None or parent in nodes,
                f"taxonomy orphan: {identity} -> {parent}")
        require(parent != identity, f"taxonomy self-cycle at {identity}")
    colors: dict[str, int] = {}

    def visit(identity: str) -> None:
        color = colors.get(identity, 0)
        require(color != 1, f"taxonomy cycle at {identity}")
        if color == 2:
            return
        colors[identity] = 1
        parent = parents[identity]
        if parent is not None:
            visit(parent)
        colors[identity] = 2

    for identity in nodes:
        visit(identity)
    require(len(colors) == len(nodes), "taxonomy contains unreachable nodes")

    broader: dict[str, tuple[str, ...]] = {}
    for identity, row in nodes.items():
        values = row.get("broader_subject_ids", [])
        require(isinstance(values, list) and all(isinstance(value, str) for value in values),
                f"subject {identity} broader_subject_ids malformed")
        require(len(values) == len(set(values)),
                f"subject {identity} repeats broader subjects")
        require(all(value in nodes and value != identity for value in values),
                f"subject {identity} has unknown/self broader subject")
        broader[identity] = tuple(values)
    broader_visiting: set[str] = set()
    broader_visited: set[str] = set()

    def visit_broader(identity: str) -> None:
        require(identity not in broader_visiting,
                f"broader-subject projection cycle at {identity}")
        if identity in broader_visited:
            return
        broader_visiting.add(identity)
        for parent in broader[identity]:
            visit_broader(parent)
        broader_visiting.remove(identity)
        broader_visited.add(identity)

    for identity in nodes:
        visit_broader(identity)

    assignments = state["assignments"]
    for identity, row in assignments.items():
        obj = state["objects"][identity]
        require(row.get("stage51_item_id") == obj.get("stage51_item_id"),
                f"assignment {identity} item binding differs")
        legacy_binding = row.get("legacy_binding")
        require(isinstance(legacy_binding, dict) and
                legacy_binding.get("legacy_item_id") == obj.get("legacy_item_id") and
                legacy_binding.get("identity_sha256") == obj.get("identity_sha256") and
                legacy_binding.get("source_record_sha256") == obj.get("source_record_sha256"),
                f"assignment {identity} legacy identity binding differs")
        primary_value = row.get("primary")
        require(isinstance(primary_value, dict), f"assignment {identity} primary is malformed")
        primary = _first_string(primary_value, ("subject_id",), f"assignment {identity}.primary")
        require(primary in nodes, f"assignment {identity} has unknown primary subject")
        require(nodes[primary].get("selectable_as_primary") is True,
                f"assignment {identity} uses a non-selectable primary subject")
        secondary = row.get("secondary_subject_ids", [])
        require(isinstance(secondary, list) and all(isinstance(value, str) for value in secondary),
                f"assignment {identity} secondary subjects are malformed")
        require(len(secondary) == len(set(secondary)),
                f"assignment {identity} repeats a secondary subject")
        require(all(value in nodes for value in secondary),
                f"assignment {identity} has an unknown secondary subject")
        require(all(nodes[value].get("selectable_as_secondary") is True for value in secondary),
                f"assignment {identity} uses a non-selectable secondary subject")
        require(primary not in secondary,
                f"assignment {identity} repeats its primary as secondary")
        candidates = row.get("candidate_subject_ids")
        require(isinstance(candidates, list) and len(candidates) == len(set(candidates)) and
                all(value in nodes for value in candidates),
                f"assignment {identity} candidate subjects malformed")
        status = row.get("classification_status")
        require(isinstance(status, str), f"assignment {identity} lacks classification state")
        assertion = primary_value.get("assertion_state")
        evidence_tier = primary_value.get("evidence_tier")
        require(assertion is not None and evidence_tier is not None,
                f"assignment {identity} primary lacks assertion/evidence state")
        if assertion == "accepted":
            require(evidence_tier == "independent_review",
                    f"assignment {identity} accepts classification without independent review")
        primary_evidence = primary_value.get("evidence")
        require(isinstance(primary_evidence, list),
                f"assignment {identity} primary evidence malformed")
        for ref in primary_evidence:
            require(isinstance(ref, dict) and isinstance(ref.get("path"), str) and
                    isinstance(ref.get("sha256"), str),
                    f"assignment {identity} primary evidence reference malformed")
            require(evidence_digest(ref["path"], f"assignment {identity} evidence") == ref["sha256"],
                    f"assignment {identity} primary evidence hash drift")
        sentinels = {
            "S51-SUB-UNCLASSIFIED", "S51-SUB-REVIEW-PENDING",
            "S51-SUB-AMBIGUOUS", "S51-SUB-OUT-OF-SCOPE",
        }
        coordinate_subjects = [primary] + list(secondary)
        coordinate_roots = (
            sorted({
                _top_branch(value, {"parents": parents, "root": root})
                for value in coordinate_subjects if value not in sentinels
            })
            if status == "accepted" and assertion == "accepted"
            else []
        )
        cross = row.get("cross_domain")
        require(isinstance(cross, dict) and
                cross.get("root_subject_ids") == coordinate_roots and
                cross.get("value") is (status == "accepted" and len(coordinate_roots) > 1),
                f"assignment {identity} cross_domain projection differs")
        if primary in sentinels or status != "accepted":
            require(cross.get("value") is False,
                    f"assignment {identity} sentinel/candidate may not assert cross-domain")
        if primary in sentinels or status != "accepted":
            require(cross.get("root_subject_ids") == [],
                    f"assignment {identity} non-accepted classification may not be a domain root")
        review = row.get("review")
        require(isinstance(review, dict), f"assignment {identity} review malformed")
        if assertion == "accepted":
            require(review.get("state") == "accepted" and
                    isinstance(review.get("reviewer_id"), str) and
                    isinstance(review.get("receipt_sha256"), str),
                    f"assignment {identity} accepted classification lacks review receipt")
            primary_evidence = primary_value.get("evidence")
            require(isinstance(primary_evidence, list) and any(
                isinstance(ref, dict) and ref.get("sha256") == review.get("receipt_sha256")
                for ref in primary_evidence
            ), f"assignment {identity} review receipt is not content-bound in primary evidence")
    declared_root = taxonomy.get("root_subject_id")
    require(declared_root == root, "Subject_Taxonomy root differs from Subject_Nodes")
    require(taxonomy.get("node_count") == len(nodes),
            "Subject_Taxonomy node_count differs from Subject_Nodes")
    require(taxonomy.get("node_id_set_sha256") ==
            sha256_bytes(canonical_json(sorted(nodes))),
            "Subject_Taxonomy node ID set digest differs")
    nodes_name = _doc_name(snapshot, "Subject_Nodes.jsonl")
    require(taxonomy.get("nodes_path") == nodes_name and
            taxonomy.get("nodes_sha256") == sha256_bytes(snapshot.raw[nodes_name]),
            "Subject_Taxonomy does not bind exact Subject_Nodes bytes")
    registry_binding = snapshot.obj(_doc_name(snapshot, "Organization_Manifest.json")).get("subject_id_registry")
    current_binding = snapshot.obj(str(CURRENT_PATH)).get("subject_id_registry")
    migration_name = str(CATALOG_ROOT / "migrations" / f"stage5-v2_to_stage5_1-{snapshot.release}.json")
    migration_binding = snapshot.obj(migration_name).get("subject_id_registry")
    expected_binding = {"path": registry_name, "sha256": sha256_bytes(snapshot.raw[registry_name]),
                        "rows": len(registry_rows)}
    require(registry_binding == expected_binding and current_binding == expected_binding,
            "manifest/current subject ID registry binding differs")
    require(isinstance(migration_binding, dict) and
            {key: migration_binding.get(key) for key in expected_binding} == expected_binding and
            migration_binding.get("policy") == "reuse_predecessor_and_append_after_max",
            "migration subject ID registry binding differs")
    return {"nodes": nodes, "parents": parents, "root": root}


def _endpoint(row: Mapping[str, Any], side: str) -> tuple[str, str]:
    key = "consumer_member_id" if side == "source" else "provider_member_id"
    identity = row.get(key)
    require(isinstance(identity, str), f"relation edge lacks exact {key}")
    return "item", identity


def _top_branch(subject: str, taxonomy: Mapping[str, Any]) -> str:
    parents = taxonomy["parents"]
    root = taxonomy["root"]
    require(subject in parents, f"unknown subject endpoint {subject}")
    current = subject
    while parents[current] is not None and parents[current] != root:
        current = parents[current]
    return current


def _endpoint_branches(
    endpoint: tuple[str, str],
    taxonomy: Mapping[str, Any],
    assignments: Mapping[str, Mapping[str, Any]],
) -> set[str]:
    kind, identity = endpoint
    normalized = kind.lower()
    if "subject" in normalized:
        return {_top_branch(identity, taxonomy)}
    require(identity in assignments, f"relation endpoint is not a known member: {identity}")
    assignment = assignments[identity]
    primary_value = assignment.get("primary")
    require(isinstance(primary_value, dict), f"assignment {identity} primary malformed")
    # `cross_domain` is an accepted-evidence projection. Candidate coordinates
    # remain useful browsing hints but may not assert a cross-domain relation.
    if (assignment.get("classification_status") != "accepted" or
            primary_value.get("assertion_state") != "accepted"):
        return set()
    primary = _first_string(primary_value, ("subject_id",), f"assignment {identity}.primary")
    sentinels = {
        "S51-SUB-UNCLASSIFIED", "S51-SUB-REVIEW-PENDING",
        "S51-SUB-AMBIGUOUS", "S51-SUB-OUT-OF-SCOPE",
    }
    values = [] if primary in sentinels else [primary]
    secondary = assignment.get("secondary_subject_ids", [])
    if isinstance(secondary, list):
        values.extend(
            value for value in secondary
            if isinstance(value, str) and value not in sentinels
        )
    return {_top_branch(value, taxonomy) for value in values}


def _is_verified(row: Mapping[str, Any]) -> bool:
    return row.get("review_state") == "verified"


def _is_target_owned(row: Mapping[str, Any]) -> bool:
    binding = row.get("provider_binding")
    if not isinstance(binding, dict):
        return False
    return binding.get("binding_kind") == "target_owned_exact_replay"


def _is_hard_relation(row: Mapping[str, Any]) -> bool:
    return row.get("blocking") is True or row.get("scheduler_effect") == "block_until_accepted"


def _dag_edges(value: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    for key in ("edges", "hard_edges", "execution_edges"):
        rows = value.get(key)
        if isinstance(rows, list):
            require(all(isinstance(row, dict) for row in rows), "Execution_Hard_DAG edges malformed")
            return rows
    raise ReleaseCheckError("Execution_Hard_DAG has no edge array")


RELATION_TYPE_PLANE: dict[str, str] = {
    "proof_prerequisite": "mathematical_prerequisite",
    "artifact_dependency": "proof",
    "checked_formal_import": "proof",
    "implies": "mathematical_semantic",
    "reduces_to": "mathematical_semantic",
    "generalizes": "mathematical_semantic",
    "special_case_of": "mathematical_semantic",
    "equivalent_to": "mathematical_semantic",
    "reuse_hint": "reuse_hint",
    "shared_lemma_group": "reuse_hint",
    "method_adaptation": "reuse_hint",
    "same_parameter_family": "association",
    "parameter_neighbor": "association",
    "source_crosswalk": "identity",
    "related_source": "association",
    "identity_candidate": "identity",
}
HARD_CAPABLE_RELATION_TYPES = {
    "proof_prerequisite", "artifact_dependency", "checked_formal_import",
}
DEPENDENCY_RECEIPT_SCHEMA = (
    "awesome-theorems/stage5-1-organization/dependency-binding-receipt/1.0"
)
DEPENDENCY_RECEIPT_KINDS = {
    "provider_acceptance_receipt": "provider_acceptance",
    "independent_review_receipt": "independent_review",
    "consumer_replay_receipt": "consumer_replay",
}
DEPENDENCY_EVIDENCE_KINDS = {
    "provider_artifact": "provider_accepted_artifact",
    "provider_acceptance_receipt": "provider_acceptance_receipt",
    "independent_review_receipt": "independent_review_receipt",
    "consumer_replay_receipt": "consumer_replay_receipt",
}


def _blueprint_owned_paths(snapshot: ReleaseSnapshot) -> dict[str, tuple[str, ...]]:
    """Return the exact owned-path authority for every current checklist ID."""

    result: dict[str, tuple[str, ...]] = {}
    for relative in (
        "Docs/Stage5_1_Theorems_Blueprint.md",
        "Docs/Stage5_1_Conjectures_Blueprint.md",
    ):
        value = snapshot.documents.get(relative)
        require(isinstance(value, str), f"{relative}: missing owned-path authority")
        for row in parse_blueprint_rows(value, relative):
            require(row["item_id"] not in result,
                    f"Blueprint owned-path authority repeats {row['item_id']}")
            result[row["item_id"]] = tuple(row["owned_paths"])
    return result


def _path_is_owned(relative: str, owned_paths: Sequence[str]) -> bool:
    candidate = PurePosixPath(relative)
    for owned_text in owned_paths:
        owned = PurePosixPath(owned_text)
        if candidate == owned:
            return True
        # A suffixless owned path is a tree authority.  File-looking paths are
        # exact authorities and cannot be widened by a string prefix.
        if not owned.suffix and len(candidate.parts) > len(owned.parts):
            if candidate.parts[:len(owned.parts)] == owned.parts:
                return True
    return False


def _binding_ref(
    snapshot: ReleaseSnapshot,
    edge_id: str,
    binding: Mapping[str, Any],
    name: str,
) -> tuple[dict[str, Any], Path, bytes]:
    ref = binding.get(name)
    require(isinstance(ref, dict) and set(ref) == {"path", "sha256", "evidence_kind"},
            f"hard edge {edge_id} {name} reference is not closed")
    require(ref.get("evidence_kind") == DEPENDENCY_EVIDENCE_KINDS[name],
            f"hard edge {edge_id} {name} evidence kind differs")
    relative = ref.get("path")
    digest = ref.get("sha256")
    require(isinstance(relative, str) and isinstance(digest, str) and
            SHA256_RE.fullmatch(digest) is not None,
            f"hard edge {edge_id} {name} reference is malformed")
    path = _safe_repo_path(snapshot.root, relative, f"hard edge {edge_id} {name}")
    require(path.is_file() and not path.is_symlink(),
            f"hard edge {edge_id} {name} is not a regular file")
    raw = path.read_bytes()
    require(sha256_bytes(raw) == digest,
            f"hard edge {edge_id} {name} hash drift")
    return dict(ref), path, raw


def _validate_dependency_receipt(
    edge: Mapping[str, Any],
    name: str,
    raw: bytes,
    artifact_ref: Mapping[str, Any],
) -> Mapping[str, Any]:
    edge_id = str(edge["edge_id"])
    value = strict_json(raw, f"hard edge {edge_id} {name}")
    require(isinstance(value, dict), f"hard edge {edge_id} {name} is not an object")
    common = {
        "schema_version", "receipt_kind", "edge_id", "consumer_member_id",
        "provider_member_id", "direction_semantics", "provider_artifact",
        "authority_sha256",
    }
    authority_keys = {
        "provider_acceptance_receipt": {"producer_actor_id", "acceptance_issuer_id"},
        "independent_review_receipt": {"reviewer_id", "issuer_authority_id"},
        "consumer_replay_receipt": {"consumer_owner_id", "acceptance_issuer_id"},
    }
    replay_keys = {
        "outcome", "consumption_verified", "replay_command_digest",
        "observed_output_digest", "consumed_provider_artifact_sha256",
        "consumer_owned_result_path", "consumer_owned_result_sha256",
    }
    expected_keys = common | authority_keys[name] | (
        replay_keys if name == "consumer_replay_receipt" else {"decision"}
    )
    require(set(value) == expected_keys,
            f"hard edge {edge_id} {name} receipt shape differs")
    _verify_inline_record_seal(value, f"hard edge {edge_id} {name}")
    require(value.get("schema_version") == DEPENDENCY_RECEIPT_SCHEMA and
            value.get("receipt_kind") == DEPENDENCY_RECEIPT_KINDS[name] and
            value.get("edge_id") == edge_id and
            value.get("consumer_member_id") == edge.get("consumer_member_id") and
            value.get("provider_member_id") == edge.get("provider_member_id") and
            value.get("direction_semantics") == "consumer_requires_provider" and
            value.get("provider_artifact") == artifact_ref,
            f"hard edge {edge_id} {name} receipt binding differs")
    for field in authority_keys[name]:
        require(isinstance(value.get(field), str) and bool(value[field].strip()),
                f"hard edge {edge_id} {name} {field} authority is missing")
    if name == "consumer_replay_receipt":
        require(value.get("outcome") == "accepted" and
                value.get("consumption_verified") is True,
                f"hard edge {edge_id} consumer replay was not accepted and consumed")
        for field in (
            "replay_command_digest", "observed_output_digest",
            "consumed_provider_artifact_sha256", "consumer_owned_result_sha256",
        ):
            require(isinstance(value.get(field), str) and
                    SHA256_RE.fullmatch(value[field]) is not None,
                    f"hard edge {edge_id} consumer replay {field} is malformed")
        require(value.get("consumed_provider_artifact_sha256") == artifact_ref.get("sha256"),
                f"hard edge {edge_id} consumer replay consumed artifact differs")
        require(isinstance(value.get("consumer_owned_result_path"), str),
                f"hard edge {edge_id} consumer replay result path is malformed")
    else:
        require(value.get("decision") == "accepted",
                f"hard edge {edge_id} {name} was not accepted")
    return value


def _validate_target_owned_binding(
    snapshot: ReleaseSnapshot,
    state: Mapping[str, Any],
    edge: Mapping[str, Any],
    owned_paths: Mapping[str, Sequence[str]],
) -> None:
    edge_id = str(edge["edge_id"])
    binding = edge.get("provider_binding")
    require(isinstance(binding, dict) and set(binding) == {
        "binding_kind", "provider_artifact", "provider_acceptance_receipt",
        "independent_review_receipt", "consumer_replay_receipt",
    }, f"hard edge {edge_id} target-owned binding shape differs")
    refs: dict[str, dict[str, Any]] = {}
    raws: dict[str, bytes] = {}
    for name in DEPENDENCY_EVIDENCE_KINDS:
        ref, _path, raw = _binding_ref(snapshot, edge_id, binding, name)
        refs[name] = ref
        raws[name] = raw
    binding_paths = [refs[name]["path"] for name in DEPENDENCY_EVIDENCE_KINDS]
    require(len(binding_paths) == len(set(binding_paths)),
            f"hard edge {edge_id} artifact/receipt paths are not distinct")

    provider = str(edge["provider_member_id"])
    consumer = str(edge["consumer_member_id"])
    provider_item = state["objects"][provider]["stage51_item_id"]
    consumer_item = state["objects"][consumer]["stage51_item_id"]
    require(provider_item in owned_paths and consumer_item in owned_paths,
            f"hard edge {edge_id} endpoint lacks Blueprint owned-path authority")
    require(_path_is_owned(refs["provider_artifact"]["path"], owned_paths[provider_item]),
            f"hard edge {edge_id} provider artifact is not provider-target-owned")
    require(_path_is_owned(refs["consumer_replay_receipt"]["path"], owned_paths[consumer_item]),
            f"hard edge {edge_id} consumer replay receipt is not consumer-target-owned")
    artifact_ref = refs["provider_artifact"]
    receipts: dict[str, Mapping[str, Any]] = {}
    for name in DEPENDENCY_RECEIPT_KINDS:
        receipts[name] = _validate_dependency_receipt(
            edge, name, raws[name], artifact_ref,
        )
    provider_acceptance = receipts["provider_acceptance_receipt"]
    independent_review = receipts["independent_review_receipt"]
    consumer_replay = receipts["consumer_replay_receipt"]
    reviewer_id = independent_review["reviewer_id"]
    conflicting_authorities = {
        provider_acceptance["producer_actor_id"],
        provider_acceptance["acceptance_issuer_id"],
        consumer_replay["consumer_owner_id"],
        consumer_replay["acceptance_issuer_id"],
    }
    require(reviewer_id not in conflicting_authorities,
            f"hard edge {edge_id} independent reviewer conflicts with producer, consumer owner, or acceptance issuer authority")

    result_relative = str(consumer_replay["consumer_owned_result_path"])
    require(_path_is_owned(result_relative, owned_paths[consumer_item]),
            f"hard edge {edge_id} consumer replay result is not consumer-target-owned")
    result_path = _safe_repo_path(
        snapshot.root, result_relative, f"hard edge {edge_id} consumer replay result",
    )
    require(result_path.is_file() and not result_path.is_symlink() and
            sha256_bytes(result_path.read_bytes()) ==
            consumer_replay["consumer_owned_result_sha256"],
            f"hard edge {edge_id} consumer replay result hash drift")

    evidence_pairs = {
        (ref.get("path"), ref.get("sha256"))
        for ref in edge.get("evidence", []) if isinstance(ref, dict)
    }
    binding_pairs = {(ref["path"], ref["sha256"]) for ref in refs.values()}
    require(binding_pairs <= evidence_pairs,
            f"hard edge {edge_id} binding files lack relation evidence references")


def validate_relations_and_hard_dag(
    snapshot: ReleaseSnapshot,
    state: Mapping[str, Any],
    taxonomy: Mapping[str, Any],
) -> dict[str, Any]:
    relation_rows = snapshot.rows(_doc_name(snapshot, "Relation_Edges.jsonl"))
    relations = _unique_rows(relation_rows, lambda row, label: _first_string(row, ("edge_id",), label),
                             "Relation_Edges")
    assignments = state["assignments"]
    node_ids = set(state["objects"]) | set(taxonomy["nodes"])
    owned_paths = _blueprint_owned_paths(snapshot)
    hard_relation_ids: set[str] = set()
    cross_ids: set[str] = set()
    for edge_id, row in relations.items():
        source = _endpoint(row, "source")
        target = _endpoint(row, "target")
        require(source[1] in node_ids and target[1] in node_ids,
                f"relation {edge_id} has an unknown endpoint")
        require(source != target, f"relation {edge_id} is a self edge")
        consumer_object = state["objects"][source[1]]
        provider_object = state["objects"][target[1]]
        require(row.get("consumer_identity_sha256") == consumer_object.get("identity_sha256") and
                row.get("provider_identity_sha256") == provider_object.get("identity_sha256") and
                row.get("consumer_object_record_sha256") == consumer_object.get("record_sha256") and
                row.get("provider_object_record_sha256") == provider_object.get("record_sha256"),
                f"relation {edge_id} endpoint identity/object receipts differ")
        relation_type = row.get("relation_type")
        plane = row.get("plane")
        require(relation_type in RELATION_TYPE_PLANE and
                plane == RELATION_TYPE_PLANE[relation_type],
                f"relation {edge_id} relation_type/plane mapping differs")
        require(row.get("direction_semantics") == "consumer_requires_provider",
                f"relation {edge_id} direction semantics differ")
        consumer_roots = _endpoint_branches(source, taxonomy, assignments)
        provider_roots = _endpoint_branches(target, taxonomy, assignments)
        recomputed_cross = bool(consumer_roots and provider_roots and consumer_roots != provider_roots)
        require(row.get("cross_domain") is recomputed_cross,
                f"relation {edge_id} cross_domain differs from taxonomy assignments")
        if recomputed_cross:
            cross_ids.add(edge_id)
        if _is_hard_relation(row):
            hard_relation_ids.add(edge_id)
            require(relation_type in HARD_CAPABLE_RELATION_TYPES,
                    f"hard edge {edge_id} relation type cannot block")
            require(_is_verified(row), f"hard edge {edge_id} is not verified")
            require(_is_target_owned(row), f"hard edge {edge_id} is not target-owned")
            tier = _optional_string(row, ("evidence_tier", "evidence_strength"))
            require(tier in {"A2_target_owned_replay", "B_content_bound_artifact"},
                    f"hard edge {edge_id} lacks A/B evidence")
            require(row.get("scheduler_effect") == "block_until_accepted" and
                    row.get("blocking") is True,
                    f"hard edge {edge_id} lacks exact scheduler semantics")
            require(source[0].lower().find("subject") < 0 and target[0].lower().find("subject") < 0,
                    f"hard edge {edge_id} must connect item endpoints")
            require(state["objects"][source[1]].get("stage51_item_id", "").endswith("-TARGET") and
                    state["objects"][target[1]].get("stage51_item_id", "").endswith("-TARGET"),
                    f"hard edge {edge_id} must connect target-owned mathematical items")
            require(row.get("state_inheritance", False) is False and
                    row.get("status_inheritance", False) is False and
                    row.get("credit_inheritance", False) is False,
                    f"hard edge {edge_id} illegally inherits provider state/credit")
        else:
            require(row.get("scheduler_effect") == "none" and row.get("blocking") is False,
                    f"non-hard relation {edge_id} leaks into the execution plane")
        if relation_type in {
            "same_parameter_family", "parameter_neighbor", "source_crosswalk",
            "related_source", "identity_candidate",
        }:
            require(row.get("blocking") is False and row.get("scheduler_effect") == "none",
                    f"association/identity edge {edge_id} may not block execution")
        evidence = row.get("evidence")
        require(isinstance(evidence, list) and len(evidence) >= 1,
                f"relation {edge_id} evidence must be nonempty")
        for ref in evidence:
            require(isinstance(ref, dict), f"relation {edge_id} evidence row is malformed")
            path = ref.get("path")
            digest = ref.get("sha256")
            require(isinstance(path, str) and isinstance(digest, str) and
                    SHA256_RE.fullmatch(digest) is not None,
                    f"relation {edge_id} evidence reference is malformed")
            evidence_path = _safe_repo_path(snapshot.root, path, f"relation {edge_id} evidence")
            require(evidence_path.is_file() and not evidence_path.is_symlink() and
                    sha256_bytes(evidence_path.read_bytes()) == digest,
                    f"relation {edge_id} evidence hash drift")
        if edge_id in hard_relation_ids:
            _validate_target_owned_binding(snapshot, state, row, owned_paths)

    cross_rows = snapshot.rows(_doc_name(snapshot, "Cross_Domain_Edges.jsonl"))
    cross_projection = _unique_rows(
        cross_rows,
        lambda row, label: _first_string(row, ("edge_id",), label),
        "Cross_Domain_Edges",
    )
    require(set(cross_projection) == cross_ids,
            "Cross_Domain_Edges is not the exact recomputed relation projection")
    for edge_id, projection in cross_projection.items():
        relation = relations[edge_id]
        consumer = _endpoint(relation, "source")[1]
        provider = _endpoint(relation, "target")[1]
        consumer_roots = sorted(_endpoint_branches(("item", consumer), taxonomy, assignments))
        provider_roots = sorted(_endpoint_branches(("item", provider), taxonomy, assignments))
        require(projection.get("consumer_member_id") == consumer and
                projection.get("provider_member_id") == provider and
                projection.get("consumer_root_subject_ids") == consumer_roots and
                projection.get("provider_root_subject_ids") == provider_roots and
                projection.get("consumer_assignment_sha256") == assignments[consumer].get("record_sha256") and
                projection.get("provider_assignment_sha256") == assignments[provider].get("record_sha256") and
                projection.get("relation_record_sha256") == relation.get("record_sha256"),
                f"Cross_Domain_Edges projection differs for {edge_id}")

    dag = snapshot.obj(_doc_name(snapshot, "Execution_Hard_DAG.json"))
    _verify_inline_record_seal(dag, "Execution_Hard_DAG")
    dag_rows = _dag_edges(dag)
    dag_ids: set[str] = set()
    object_to_item = {
        identity: _first_string(row, ("stage51_item_id",), f"object {identity}")
        for identity, row in state["objects"].items()
    }
    item_ids = set(object_to_item.values())
    require(set(dag.get("nodes", [])) == item_ids,
            "Execution_Hard_DAG node projection differs from Object_Index")
    adjacency: dict[str, set[str]] = defaultdict(set)
    indegree: dict[str, int] = {identity: 0 for identity in item_ids}
    for number, row in enumerate(dag_rows, 1):
        edge_id = _first_string(row, ("edge_id",), f"hard DAG edge {number}")
        require(edge_id not in dag_ids, f"Execution_Hard_DAG repeats {edge_id}")
        dag_ids.add(edge_id)
        require(edge_id in hard_relation_ids, f"Execution_Hard_DAG contains non-admitted edge {edge_id}")
        relation = relations[edge_id]
        dependent = row.get("consumer_member_id")
        prerequisite = row.get("provider_member_id")
        rel_source = _endpoint(relation, "source")[1]
        rel_target = _endpoint(relation, "target")[1]
        require(dependent == rel_source and prerequisite == rel_target,
                f"Execution_Hard_DAG reverses or changes relation {edge_id}")
        require(dependent in object_to_item and prerequisite in object_to_item and dependent != prerequisite,
                f"Execution_Hard_DAG has invalid endpoints for {edge_id}")
        require(row.get("relation_record_sha256") == relation.get("record_sha256"),
                f"Execution_Hard_DAG relation receipt differs for {edge_id}")
        provider_item = object_to_item[prerequisite]
        consumer_item = object_to_item[dependent]
        if consumer_item not in adjacency[provider_item]:
            adjacency[provider_item].add(consumer_item)
            indegree[consumer_item] += 1
    require(dag_ids == hard_relation_ids,
            "Execution_Hard_DAG is not the exact verified target-owned hard-edge projection")
    root_count = sum(1 for degree in indegree.values() if degree == 0)
    queue = deque(sorted(identity for identity, degree in indegree.items() if degree == 0))
    visited = 0
    while queue:
        identity = queue.popleft()
        visited += 1
        for child in sorted(adjacency.get(identity, ())):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    require(visited == len(indegree), "Execution_Hard_DAG contains a cycle")
    topological_order = dag.get("topological_order")
    require(isinstance(topological_order, list) and set(topological_order) == item_ids and
            len(topological_order) == len(item_ids),
            "Execution_Hard_DAG topological_order is not a node permutation")
    position = {identity: index for index, identity in enumerate(topological_order)}
    require(all(position[parent] < position[child]
                for parent, children in adjacency.items() for child in children),
            "Execution_Hard_DAG topological_order violates an edge")
    counts = dag.get("counts")
    require(isinstance(counts, dict) and counts.get("node_count") == len(item_ids) and
            counts.get("edge_count") == len(dag_ids) and
            counts.get("root_count") == root_count,
            "Execution_Hard_DAG counts differ")

    expected_outgoing: dict[str, set[str]] = defaultdict(set)
    expected_incoming: dict[str, set[str]] = defaultdict(set)
    expected_hard_items: dict[str, set[str]] = defaultdict(set)
    for edge_id, relation in relations.items():
        consumer = _endpoint(relation, "source")[1]
        provider = _endpoint(relation, "target")[1]
        expected_outgoing[consumer].add(edge_id)
        expected_incoming[provider].add(edge_id)
        if edge_id in hard_relation_ids:
            expected_hard_items[consumer].add(object_to_item[provider])

    for identity, assessment in state["assessments"].items():
        status = assessment.get("audit_status")
        require(isinstance(status, str), f"dependency assessment {identity} has no audit status")
        for key in ("outgoing_edge_ids", "incoming_edge_ids"):
            listed = assessment.get(key)
            if listed is None:
                continue
            require(isinstance(listed, list) and all(isinstance(value, str) for value in listed),
                    f"dependency assessment {identity} {key} malformed")
            require(all(value in relations for value in listed),
                    f"dependency assessment {identity} references an unknown edge")
        require("independent" not in status or status == "unknown_not_independent_proof_claim",
                f"dependency assessment {identity} overclaims independence")
        require(set(assessment.get("outgoing_edge_ids", [])) == expected_outgoing[identity] and
                set(assessment.get("incoming_edge_ids", [])) == expected_incoming[identity],
                f"dependency assessment {identity} is not the exact relation projection")
        require(set(assessment.get("hard_prerequisite_item_ids", [])) == expected_hard_items[identity],
                f"dependency assessment {identity} hard prerequisite projection differs")
        incident = [relations[edge_id] for edge_id in
                    expected_outgoing[identity] | expected_incoming[identity]]
        if incident:
            expected_status = (
                "audited_edges_present"
                if any(edge.get("review_state") == "verified" for edge in incident)
                else "source_edges_present_pending_review"
            )
            require(status == expected_status,
                    f"dependency assessment {identity} relation review status differs")
    return {
        "relations": relations,
        "hard_relation_ids": hard_relation_ids,
        "dag": dag,
        "object_to_item": object_to_item,
        "adjacency": adjacency,
        "topological_order": topological_order,
    }


def validate_dependency_closure_and_worksets(
    snapshot: ReleaseSnapshot,
    state: Mapping[str, Any],
    relation_state: Mapping[str, Any],
) -> None:
    dag = relation_state["dag"]
    relations = relation_state["relations"]
    hard_ids = relation_state["hard_relation_ids"]
    object_to_item = relation_state["object_to_item"]
    item_to_object = {item: obj for obj, item in object_to_item.items()}
    require(len(item_to_object) == len(object_to_item), "two members share a Stage5.1 item ID")
    topological_order = relation_state["topological_order"]

    direct_items: dict[str, set[str]] = defaultdict(set)
    direct_edges: dict[str, set[str]] = defaultdict(set)
    for edge_id in hard_ids:
        relation = relations[edge_id]
        consumer_object = _endpoint(relation, "source")[1]
        provider_object = _endpoint(relation, "target")[1]
        consumer_item = object_to_item[consumer_object]
        provider_item = object_to_item[provider_object]
        direct_items[consumer_item].add(provider_item)
        direct_edges[consumer_item].add(edge_id)

    transitive: dict[str, set[str]] = {item: set() for item in item_to_object}
    ranks: dict[str, int] = {item: 0 for item in item_to_object}
    for item in topological_order:
        for provider in direct_items[item]:
            transitive[item].add(provider)
            transitive[item].update(transitive[provider])
            ranks[item] = max(ranks[item], ranks[provider] + 1)

    closure_rows = snapshot.rows(_doc_name(snapshot, "Dependency_Closure.jsonl"))
    closure = _unique_rows(
        closure_rows,
        lambda row, label: _first_string(row, ("item_id",), label),
        "Dependency_Closure",
    )
    require(set(closure) == set(item_to_object),
            "Dependency_Closure does not exactly cover the hard-DAG nodes")
    hard_authorities = {
        dag.get("authority_sha256"),
        sha256_bytes(snapshot.raw[_doc_name(snapshot, "Execution_Hard_DAG.json")]),
    }
    for item, row in closure.items():
        object_identity = item_to_object[item]
        assessment = state["assessments"][object_identity]
        require(row.get("assessment_id") == assessment.get("assessment_id"),
                f"Dependency_Closure {item} assessment binding differs")
        require(set(row.get("direct_prerequisite_item_ids", [])) == direct_items[item] and
                set(row.get("transitive_prerequisite_item_ids", [])) == transitive[item] and
                set(row.get("direct_edge_ids", [])) == direct_edges[item],
                f"Dependency_Closure {item} is not the exact transitive projection")
        require(row.get("topological_rank") == ranks[item],
                f"Dependency_Closure {item} topological rank differs")
        require(row.get("hard_dag_sha256") in hard_authorities,
                f"Dependency_Closure {item} hard-DAG binding differs")

    all_workset_ids: set[str] = set()
    for program, indexed in state["worksets"].items():
        for object_identity, row in indexed.items():
            require(object_identity not in all_workset_ids, "Organization_Worksets overlap")
            all_workset_ids.add(object_identity)
            obj = state["objects"][object_identity]
            assignment = state["assignments"][object_identity]
            assessment = state["assessments"][object_identity]
            item = object_to_item[object_identity]
            require(row.get("item_id") == item and row.get("legacy_item_id") == obj.get("legacy_item_id"),
                    f"{program} workset {object_identity} identity binding differs")
            require(row.get("program") == obj.get("program") and
                    row.get("object_kind") == obj.get("object_kind") and
                    row.get("id_crosswalk_record_sha256") ==
                    state["math_crosswalk"][object_identity].get("record_sha256"),
                    f"{program} workset {object_identity} program/kind/crosswalk binding differs")
            require(row.get("object_index_record_sha256") == obj.get("record_sha256") and
                    row.get("subject_assignment_id") == assignment.get("assignment_id") and
                    row.get("subject_assignment_record_sha256") == assignment.get("record_sha256") and
                    row.get("dependency_assessment_id") == assessment.get("assessment_id") and
                    row.get("dependency_assessment_record_sha256") == assessment.get("record_sha256") and
                    row.get("dependency_closure_record_sha256") == closure[item].get("record_sha256"),
                    f"{program} workset {object_identity} content receipt differs")
            require(set(row.get("execution_dependency_item_ids", [])) == direct_items[item],
                    f"{program} workset {object_identity} execution dependency differs")
            require(row.get("initial_state") == "not_done",
                    f"{program} workset {object_identity} inherits predecessor state")
    require(all_workset_ids == set(state["objects"]),
            "Organization_Worksets do not cover every object exactly once")


def parse_blueprint_rows(text: str, label: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(text.splitlines(), 1):
        if not line.startswith("- ["):
            continue
        match = BLUEPRINT_ROW_RE.fullmatch(line)
        require(match is not None, f"{label}:{number}: malformed checklist row")
        depends_raw = match.group("depends").strip()
        dependencies = () if depends_raw.lower() in {"none", "-", ""} else tuple(
            value.strip() for value in depends_raw.split(",") if value.strip()
        )
        rows.append({
            "state": match.group("state"),
            "item_id": match.group("id"),
            "title": match.group("title"),
            "dependencies": dependencies,
            "owned_paths": tuple(
                value.strip() for value in match.group("paths").split(",") if value.strip()
            ),
            "gate": match.group("gate"),
            "line": number,
        })
    require(bool(rows), f"{label}: no checklist rows")
    return rows


def _walk_objects(value: Any) -> Iterable[Mapping[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_objects(child)


REQUIRED_CONCURRENCY_DIMENSIONS = {
    "logical_claims",
    "desired_live_target",
    "hard_cap",
    "service_records",
    "agent_executions",
    "startup_reservations",
    "launch_fanout_per_wave",
    "live_transports",
    "authenticated_goals",
    "running_turns",
    "outbound_request_starts_per_window",
    "in_flight_requests",
    "max_outstanding_requests_per_execution",
    "integration",
    "validators",
    "exact_path_conflicts",
}
REQUIRED_CONCURRENCY_POLICY_FIELDS = {
    "request_window_seconds", "lifecycle_mode", "replacement_policy",
}
REQUIRED_REPLACEMENT_POLICY_FIELDS = {
    "replacement_limit", "startup_deadline_seconds", "tick_time_budget_seconds",
}
REQUIRED_PROMPT_FIELDS = {
    "schema_version", "program", "policy_epoch", "source", "concurrency",
    "request_window_seconds", "lifecycle_mode", "replacement_policy", "route",
    "model", "reasoning_effort", "service_tier", "authority_sha256",
}
REQUIRED_AUTHORITY_FIELDS = {"program", "policy_epoch", "source", "authority_sha256"}
REQUIRED_ROUTE_FIELDS = {"route", "model", "reasoning_effort", "service_tier"}


def _contains_number(value: Any) -> bool:
    if isinstance(value, bool) or value is None:
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, dict):
        return any(_contains_number(child) for child in value.values())
    if isinstance(value, list):
        return any(_contains_number(child) for child in value)
    return False


def validate_concurrency_prompt(text: str, label: str) -> None:
    parsed: list[Any] = []
    for match in JSON_FENCE_RE.finditer(text):
        parsed.append(strict_json(match.group("body").encode("utf-8"), f"{label} JSON fence"))
    contracts: list[Mapping[str, Any]] = []
    for value in parsed:
        for obj in _walk_objects(value):
            contract = obj.get("concurrency_prompt_contract")
            if isinstance(contract, dict):
                contracts.append(contract)
    require(len(contracts) == 1,
            f"{label}: expected exactly one concurrency_prompt_contract")
    contract = contracts[0]
    require(set(contract) == {
        "value_source", "missing_policy", "defaults_forbidden", "required_dimensions",
        "required_policy_fields", "required_replacement_policy_fields",
        "required_prompt_fields", "required_authority_fields", "required_route_fields",
        "prompt_path",
    }, f"{label}: concurrency prompt contract fields differ")
    required = contract.get("required_dimensions")
    require(isinstance(required, list) and all(isinstance(value, str) for value in required),
            f"{label}: prompt concurrency required fields are missing")
    require(set(required) == REQUIRED_CONCURRENCY_DIMENSIONS and len(required) == len(set(required)),
            f"{label}: prompt concurrency dimension set differs")
    for key, expected in (
        ("required_policy_fields", REQUIRED_CONCURRENCY_POLICY_FIELDS),
        ("required_replacement_policy_fields", REQUIRED_REPLACEMENT_POLICY_FIELDS),
        ("required_prompt_fields", REQUIRED_PROMPT_FIELDS),
        ("required_authority_fields", REQUIRED_AUTHORITY_FIELDS),
        ("required_route_fields", REQUIRED_ROUTE_FIELDS),
    ):
        value = contract.get(key)
        require(isinstance(value, list) and len(value) == len(set(value)) and set(value) == expected,
                f"{label}: {key} differs")
    require(isinstance(contract.get("prompt_path"), str) and
            contract["prompt_path"].startswith("Docs/evidence/stage5_1_") and
            contract["prompt_path"].endswith("/operator-concurrency-prompt.json"),
            f"{label}: prompt_path differs")
    require(contract.get("value_source") == "explicit_execution_prompt_only",
            f"{label}: concurrency values must come only from the execution prompt")
    missing = contract.get("missing_policy")
    require(isinstance(missing, str) and missing.startswith("fail_closed"),
            f"{label}: missing concurrency prompt must fail closed")
    require(contract.get("defaults_forbidden") is True,
            f"{label}: concurrency defaults must be explicitly forbidden")
    require(not _contains_number(contract),
            f"{label}: concurrency prompt contract contains a hard-coded numeric value")
    for obj in _walk_objects(contract):
        for key, value in obj.items():
            lowered = key.lower()
            if lowered == "defaults_forbidden" and value is True:
                continue
            require("default" not in lowered,
                    f"{label}: concurrency defaults are forbidden ({key})")
    # Also reject the common prose form used to smuggle a cap around the JSON
    # contract.  Stage/release version numbers are intentionally outside this
    # narrow line-oriented check.
    prose = JSON_FENCE_RE.sub("", text)
    for line in prose.splitlines():
        lowered = line.lower()
        if "concurr" in lowered or "并发" in line:
            require(re.search(r"\b\d+\b", line) is None,
                    f"{label}: hard-coded numeric concurrency in prose")


def validate_blueprint_spec(
    snapshot: ReleaseSnapshot,
    text: str,
    label: str,
    program: str,
) -> None:
    blocks = [
        strict_json(match.group("body").encode("utf-8"), f"{label} execution specification")
        for match in JSON_FENCE_RE.finditer(text)
    ]
    require(len(blocks) == 1 and isinstance(blocks[0], dict),
            f"{label}: expected one execution specification")
    spec = blocks[0]
    hard_name = _doc_name(snapshot, "Execution_Hard_DAG.json")
    hard_binding = spec.get("execution_hard_dag")
    require(spec.get("program") == program and
            spec.get("blueprint_revision") == "Stage5.1" and
            spec.get("base_catalog_release") == "5.6" and
            spec.get("not_catalog_release_5_1") is True and
            spec.get("authoritative_blueprint") == label and
            spec.get("same_prefix_gantt") == label.replace("_Blueprint.md", "_Gantt.md") and
            spec.get("organization_release_manifest") == _doc_name(snapshot, "Organization_Manifest.json") and
            spec.get("activation_status") == "blocked",
            f"{label}: frozen execution identity differs")
    require(isinstance(hard_binding, dict) and hard_binding.get("path") == hard_name and
            hard_binding.get("sha256") == sha256_bytes(snapshot.raw[hard_name]),
            f"{label}: Execution_Hard_DAG binding differs")
    activation = spec.get("activation_contract")
    require(isinstance(activation, dict), f"{label}: activation contract missing")
    require(set(activation.get("required_side_effect_absence", [])) == {
        "runtime_root", "claims", "reservations", "task_roots", "tmux_sockets",
        "processes", "request_leases", "turn_leases", "requests", "cron_marker",
    }, f"{label}: activation side-effect absence contract differs")
    require(spec.get("concurrency_values") is None or "concurrency_values" not in spec,
            f"{label}: release embeds concurrency values")


def _validate_master_non_tui(
    text: str,
    rows: Sequence[Mapping[str, Any]],
    member_item_ids: set[str],
    label: str,
) -> None:
    lowered = text.lower()
    require("master" in lowered and ("non-tui" in lowered or "non_tui" in lowered),
            f"{label}: Master control must be declared non-TUI")
    master_contracts: list[Mapping[str, Any]] = []
    for match in JSON_FENCE_RE.finditer(text):
        value = strict_json(match.group("body").encode("utf-8"), f"{label} JSON fence")
        for obj in _walk_objects(value):
            candidate = obj.get("master_control")
            if isinstance(candidate, dict):
                master_contracts.append(candidate)
    require(len(master_contracts) == 1, f"{label}: expected one Master control contract")
    require(master_contracts[0] == {
        "transport": "non_tui_controller",
        "worker_transport": "forbidden",
        "goal_submission": "forbidden",
    },
            f"{label}: Master control contract is not non-TUI")
    for row in rows:
        haystack = f"{row['item_id']} {row['title']} {row['gate']}".lower()
        if row["item_id"] in member_item_ids:
            continue
        require("canonical master deterministic control operation" in haystack and
                "without launching a tui worker" in haystack and
                "tmux" not in haystack and "codex tui" not in haystack and "/goal" not in haystack,
                f"{label}: Master control row is incorrectly assigned to a TUI worker")


def _validate_blueprint_graph(rows: Sequence[Mapping[str, Any]], label: str) -> dict[str, Mapping[str, Any]]:
    indexed: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        identity = row["item_id"]
        require(identity not in indexed, f"{label}: duplicate checklist ID {identity}")
        indexed[identity] = row
        require(row["state"] == " ",
                f"{label}: new Stage5.1 release must be all blank; state inheritance at {identity}")
    indegree = {identity: 0 for identity in indexed}
    children: dict[str, set[str]] = defaultdict(set)
    for identity, row in indexed.items():
        for parent in row["dependencies"]:
            require(parent in indexed, f"{label}: {identity} depends on missing {parent}")
            require(parent != identity, f"{label}: self dependency at {identity}")
            if identity not in children[parent]:
                children[parent].add(identity)
                indegree[identity] += 1
    roots = sorted(identity for identity, degree in indegree.items() if degree == 0)
    require(bool(roots), f"{label}: no reachable root")
    queue = deque(roots)
    visited: set[str] = set()
    while queue:
        identity = queue.popleft()
        if identity in visited:
            continue
        visited.add(identity)
        for child in sorted(children.get(identity, ())):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    require(visited == set(indexed), f"{label}: checklist DAG is cyclic or unreachable")
    return indexed


def _gantt_ids(text: str, known_ids: set[str]) -> list[str]:
    found: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") or stripped.startswith("- ")):
            continue
        for identity in re.findall(r"[A-Z][A-Z0-9_.:-]*", stripped):
            if identity in known_ids:
                found.append(identity)
                break
    return found


def validate_gantt(
    snapshot: ReleaseSnapshot,
    blueprint_name: str,
    gantt_name: str,
    blueprint_text: str,
    rows: Sequence[Mapping[str, Any]],
    gantt_text: str,
    state: Mapping[str, Any],
    taxonomy: Mapping[str, Any],
) -> None:
    expected = blueprint_name.replace("_Blueprint.md", "_Gantt.md")
    require(gantt_name == expected,
            f"{gantt_name}: Gantt is not the same-name Blueprint projection")
    require(CHECKBOX_RE.search(gantt_text) is None,
            f"{gantt_name}: Gantt must not contain checklist boxes")
    known = {row["item_id"] for row in rows}
    observed = _gantt_ids(gantt_text, known)
    require(observed == [row["item_id"] for row in rows],
            f"{gantt_name}: Gantt monitoring rows do not exactly match Blueprint order")
    expected_header = (
        "| Item | Legacy/member mapping | State | Execution depends on | "
        "Owner / claim | Startup | Live | Handoff | Integration | Repair | Block | "
        "Subject code/path/label | Classification/review | Assignment SHA-256 | "
        "Assessment SHA-256 | Dependency assessment | "
        "Mathematical prerequisite consumer-required edge IDs | "
        "Mathematical prerequisite provider-used-by edge IDs | Semantic relation edge IDs | "
        "Reuse hint edge IDs | Hard edge review | Scheduler effect | Cross-domain | Timing |"
    )
    require(expected_header in gantt_text,
            f"{gantt_name}: execution/math/subject/cross-domain columns are not separate")
    table_rows: dict[str, list[str]] = {}
    for line in gantt_text.splitlines():
        match = re.fullmatch(r"\| `(?P<id>[A-Z0-9-]+)` \|(?P<body>.*)\|", line)
        if match is None or match.group("id") not in known:
            continue
        cells = [cell.strip() for cell in match.group("body").split("|")]
        require(len(cells) == 23, f"{gantt_name}: malformed 24-column monitoring row")
        table_rows[match.group("id")] = cells
    require(set(table_rows) == known, f"{gantt_name}: Gantt omits checklist table rows")
    object_by_item = {
        obj["stage51_item_id"]: identity for identity, obj in state["objects"].items()
    }
    relations = snapshot.rows(_doc_name(snapshot, "Relation_Edges.jsonl"))
    outgoing: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    incoming: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for relation in relations:
        outgoing[relation["consumer_member_id"]].append(relation)
        incoming[relation["provider_member_id"]].append(relation)

    def decode_ids(cell: str) -> set[str]:
        raw = cell[1:-1] if cell.startswith("`") and cell.endswith("`") else cell
        if raw == "[]":
            return set()
        values = raw.split(",")
        require(all(values) and len(values) == len(set(values)),
                f"{gantt_name}: malformed relation edge ID cell")
        return set(values)

    for row in rows:
        (
            mapping_cell, row_state, execution, owner_claim, startup, live,
            handoff, integration, repair, blocked, subject_cell, classification_cell,
            assignment_sha_cell, assessment_sha_cell, audit_cell, math_cell,
            math_used_by_cell, semantic_cell, reuse_cell, hard_review_cell, scheduler_cell,
            cross_cell, timing,
        ) = table_rows[row["item_id"]]
        expected_execution = "`" + (",".join(row["dependencies"]) or "-") + "`"
        math_ids = decode_ids(math_cell)
        math_used_by_ids = decode_ids(math_used_by_cell)
        semantic_ids = decode_ids(semantic_cell)
        reuse_ids = decode_ids(reuse_cell)
        hard_review_ids = decode_ids(hard_review_cell)
        cross_raw = cross_cell[1:-1] if cross_cell.startswith("`") and cross_cell.endswith("`") else cross_cell
        require(cross_raw in {"true", "false"}, f"{gantt_name}: malformed cross-domain cell")
        object_identity = object_by_item.get(row["item_id"])
        if object_identity is None:
            require(mapping_cell == "control successor" and subject_cell == "-" and
                    classification_cell == "not_applicable" and
                    assignment_sha_cell == "-" and assessment_sha_cell == "-" and
                    audit_cell == "control_not_member" and not math_ids and
                    not math_used_by_ids and
                    not semantic_ids and not reuse_ids and not hard_review_ids,
                    f"{gantt_name}: control projection differs at {row['item_id']}")
            expected_cross, expected_scheduler = False, {"none"}
        else:
            obj = state["objects"][object_identity]
            assignment = state["assignments"][object_identity]
            assessment = state["assessments"][object_identity]
            subject = taxonomy["nodes"][assignment["primary"]["subject_id"]]
            subject_path: list[str] = []
            cursor: str | None = subject["subject_id"]
            while cursor is not None:
                subject_path.append(cursor)
                cursor = taxonomy["parents"][cursor]
            subject_path.reverse()
            expected_subject = (
                f"`{subject.get('notation') or '-'}` / `{'/'.join(subject_path)}` / "
                f"{str(subject['label']['en']).replace('|', '/')}"
            )
            consumer_incident = outgoing[object_identity]
            provider_incident = incoming[object_identity]
            associated = consumer_incident + provider_incident
            expected_math = {
                edge["edge_id"] for edge in consumer_incident
                if edge["plane"] in {"proof", "mathematical_prerequisite"}
            }
            expected_math_used_by = {
                edge["edge_id"] for edge in provider_incident
                if edge["plane"] in {"proof", "mathematical_prerequisite"}
            }
            expected_semantic = {
                edge["edge_id"] for edge in associated
                if edge["plane"] in {"mathematical_semantic", "association", "identity"}
            }
            expected_reuse = {
                edge["edge_id"] for edge in associated if edge["plane"] == "reuse_hint"
            }
            expected_hard = {
                f"{edge['edge_id']}:{edge['review_state']}"
                for edge in associated if edge["blocking"] is True
            }
            consumer_hard = [edge for edge in consumer_incident if edge["blocking"] is True]
            expected_scheduler = (
                {f"{edge['edge_id']}:{edge['scheduler_effect']}" for edge in consumer_hard}
                if consumer_hard else {"none"}
            )
            require(mapping_cell == f"`{obj['legacy_item_id']}→{object_identity}`" and
                    subject_cell == expected_subject and
                    classification_cell ==
                    f"`{assignment['classification_status']}/{assignment['review']['state']}`" and
                    assignment_sha_cell == f"`{assignment['record_sha256']}`" and
                    assessment_sha_cell == f"`{assessment['record_sha256']}`" and
                    audit_cell == f"`{assessment['audit_status']}`" and
                    math_ids == expected_math and math_used_by_ids == expected_math_used_by and
                    semantic_ids == expected_semantic and
                    reuse_ids == expected_reuse and hard_review_ids == expected_hard,
                    f"{gantt_name}: member graph/evidence projection differs at {row['item_id']}")
            expected_cross = assignment["cross_domain"]["value"]
        scheduler_raw = (
            scheduler_cell[1:-1]
            if scheduler_cell.startswith("`") and scheduler_cell.endswith("`")
            else scheduler_cell
        )
        scheduler_values = set(scheduler_raw.split(","))
        require(row_state == "not_done" and execution == expected_execution and
                owner_claim == "unclaimed" and startup == "not_started" and
                live == "not_live" and handoff == "no_handoff" and
                integration == "no_integration" and repair == "no_repair" and
                blocked == "blocked_activation" and
                scheduler_values == expected_scheduler and
                (cross_raw == "true") is expected_cross and timing == "unscheduled",
                f"{gantt_name}: monitoring projection differs at {row['item_id']}")

    metadata_blocks = [
        strict_json(match.group("body").encode("utf-8"), f"{gantt_name} metadata")
        for match in JSON_FENCE_RE.finditer(gantt_text)
    ]
    require(len(metadata_blocks) == 1 and isinstance(metadata_blocks[0], dict),
            f"{gantt_name}: expected one projection metadata object")
    metadata = metadata_blocks[0]
    program = "theorems" if "_Theorems_" in blueprint_name else "conjectures"
    program_objects = {
        identity for identity, obj in state["objects"].items()
        if obj["program"] == program
    }
    program_relations = {
        row["edge_id"]: row for row in relations
        if (row["consumer_member_id"] in program_objects or
            row["provider_member_id"] in program_objects)
    }
    consumer_incident_count = sum(len(outgoing[identity]) for identity in program_objects)
    provider_incident_count = sum(len(incoming[identity]) for identity in program_objects)
    manifest = snapshot.obj(_doc_name(snapshot, "Organization_Manifest.json"))
    expected_metadata = {
        "schema_version": "awesome-theorems/stage5-1-organization/gantt/1.0",
        "program": program,
        "blueprint_path": blueprint_name,
        "blueprint_sha256": sha256_bytes(blueprint_text.encode("utf-8")),
        "generated_at": manifest["generated_at"],
        "item_count": len(rows),
        "all_timing_unknown": True,
        "activation_status": "blocked",
        "taxonomy_sha256": sha256_bytes(snapshot.raw[_doc_name(snapshot, "Subject_Taxonomy.json")]),
        "subject_assignments_sha256": sha256_bytes(snapshot.raw[_doc_name(snapshot, "Subject_Assignments.jsonl")]),
        "dependency_assessments_sha256": sha256_bytes(snapshot.raw[_doc_name(snapshot, "Dependency_Assessments.jsonl")]),
        "relation_edges_sha256": sha256_bytes(snapshot.raw[_doc_name(snapshot, "Relation_Edges.jsonl")]),
        "execution_hard_dag_sha256": sha256_bytes(snapshot.raw[_doc_name(snapshot, "Execution_Hard_DAG.json")]),
        "assessment_status_counts": dict(sorted(Counter(
            state["assessments"][identity]["audit_status"]
            for identity in program_objects
        ).items())),
        "relation_type_counts": dict(sorted(Counter(
            row["relation_type"] for row in program_relations.values()
        ).items())),
        "relation_plane_counts": dict(sorted(Counter(
            row["plane"] for row in program_relations.values()
        ).items())),
        "relation_review_state_counts": dict(sorted(Counter(
            row["review_state"] for row in program_relations.values()
        ).items())),
        "relation_scheduler_effect_counts": dict(sorted(Counter(
            row["scheduler_effect"] for row in program_relations.values()
        ).items())),
        "relation_incident_counts": {
            "consumer_required": consumer_incident_count,
            "provider_used_by": provider_incident_count,
            "total_endpoint_incidents": consumer_incident_count + provider_incident_count,
            "unique_relations": len(program_relations),
            "members_with_incident": sum(
                bool(outgoing[identity] or incoming[identity])
                for identity in program_objects
            ),
        },
        "cross_domain_assignment_count": sum(
            state["assignments"][identity]["cross_domain"]["value"] is True
            for identity in program_objects
        ),
        "cross_domain_relation_count": sum(
            row["cross_domain"] is True for row in program_relations.values()
        ),
        "hard_edge_count": sum(
            row["blocking"] is True for row in program_relations.values()
        ),
    }
    require(metadata == expected_metadata,
            f"{gantt_name}: projection metadata differs from independent recomputation")


def validate_blueprints_and_gantts(
    snapshot: ReleaseSnapshot,
    state: Mapping[str, Any],
    taxonomy: Mapping[str, Any],
) -> None:
    expected_all: set[str] = set()
    for legacy_id, row in state["legacy"].items():
        new_ids = row.get("new_item_ids")
        require(isinstance(new_ids, list) and all(isinstance(value, str) for value in new_ids),
                f"legacy crosswalk {legacy_id} new_item_ids malformed")
        expected_all.update(new_ids)
    object_by_item = {
        obj["stage51_item_id"]: identity for identity, obj in state["objects"].items()
    }
    observed_all: set[str] = set()
    for program_title in ("Theorems", "Conjectures"):
        blueprint_name = f"Docs/Stage5_1_{program_title}_Blueprint.md"
        gantt_name = f"Docs/Stage5_1_{program_title}_Gantt.md"
        blueprint = snapshot.documents[blueprint_name]
        gantt = snapshot.documents[gantt_name]
        require(isinstance(blueprint, str) and isinstance(gantt, str), "Markdown projection malformed")
        rows = parse_blueprint_rows(blueprint, blueprint_name)
        indexed = _validate_blueprint_graph(rows, blueprint_name)
        predecessor_name = (
            "Docs/Stage5_Theorems_Blueprint.md"
            if program_title == "Theorems"
            else "Docs/Stage5_Conjectures_Blueprint.md"
        )
        predecessor_rows = parse_blueprint_rows(
            _safe_repo_path(snapshot.root, predecessor_name, predecessor_name).read_text(encoding="utf-8"),
            predecessor_name,
        )
        predecessor_by_id = {row["item_id"]: row for row in predecessor_rows}
        successor_by_legacy = {
            legacy_id: tuple(row["new_item_ids"])
            for legacy_id, row in state["legacy"].items()
            if row.get("legacy_program") == program_title.lower()
        }
        for legacy_id, predecessor in predecessor_by_id.items():
            require(legacy_id in successor_by_legacy,
                    f"{blueprint_name}: predecessor {legacy_id} has no successor")
            control_dependencies = {
                successor
                for dependency in predecessor["dependencies"]
                for successor in successor_by_legacy[dependency]
            }
            crosswalk = state["legacy"][legacy_id]
            for successor in successor_by_legacy[legacy_id]:
                require(successor in indexed,
                        f"{blueprint_name}: crosswalk successor {successor} missing")
                expected_dependencies = set(control_dependencies)
                if crosswalk.get("relationship") == "exact_member_successor":
                    object_identity = object_by_item.get(successor)
                    require(object_identity is not None,
                            f"{blueprint_name}: member successor {successor} lacks object")
                    expected_dependencies.update(
                        state["assessments"][object_identity].get("hard_prerequisite_item_ids", [])
                    )
                require(set(indexed[successor]["dependencies"]) == expected_dependencies,
                        f"{blueprint_name}: {successor} execution dependencies differ from control readiness plus admitted hard providers")
        require(observed_all.isdisjoint(indexed), "theorem/conjecture Blueprint IDs overlap")
        observed_all.update(indexed)
        validate_concurrency_prompt(blueprint, blueprint_name)
        validate_blueprint_spec(
            snapshot, blueprint, blueprint_name, program_title.lower(),
        )
        _validate_master_non_tui(blueprint, rows, set(object_by_item), blueprint_name)
        validate_gantt(
            snapshot, blueprint_name, gantt_name, blueprint, rows, gantt, state,
            taxonomy,
        )
    require(observed_all == expected_all,
            "the two Blueprints are not a complete projection of 20,197 legacy rows")


def _find_generated_at(value: Any) -> str | None:
    if isinstance(value, dict):
        generated = value.get("generated_at")
        if isinstance(generated, str):
            return generated
        for child in value.values():
            found = _find_generated_at(child)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _find_generated_at(child)
            if found is not None:
                return found
    return None


def _reconstruct_initial_bundle(snapshot: ReleaseSnapshot) -> dict[str, bytes]:
    common_path = snapshot.root / "Docs/tools/stage5_1_common.py"
    builder_path = snapshot.root / "Docs/tools/build_stage5_1_organization_release.py"
    require(common_path.is_file() and builder_path.is_file(), "Stage5.1 common/builder interface missing")
    builder = _load_module(builder_path, f"stage5_1_builder_release_check_{id(snapshot)}")
    manifest = snapshot.obj(_doc_name(snapshot, "Organization_Manifest.json"))
    generated_at = _find_generated_at(manifest)
    require(generated_at is not None, "Organization_Manifest lacks generated_at")
    try:
        expected = builder.build_bundle(snapshot.root, snapshot.release, generated_at)
    except Exception as exc:
        raise ReleaseCheckError(f"in-memory release reconstruction failed: {exc}") from exc
    require(isinstance(expected, dict) and
            all(isinstance(path, str) and isinstance(raw, bytes) for path, raw in expected.items()),
            "builder build_bundle interface differs")
    return expected


def validate_common_and_rebuild(
    snapshot: ReleaseSnapshot,
    *,
    expected_bundle: Mapping[str, bytes] | None = None,
    disk_exceptions: Iterable[str] = (),
) -> dict[str, bytes]:
    common_path = snapshot.root / "Docs/tools/stage5_1_common.py"
    require(common_path.is_file(), "Stage5.1 common interface missing")
    common = _load_module(common_path, f"stage5_1_common_release_check_{id(snapshot)}")
    expected = (dict(expected_bundle) if expected_bundle is not None
                else _reconstruct_initial_bundle(snapshot))

    # Validate reconstructed initial bytes, not a potentially advanced cursor.
    # This is an independent shared structural pass over the immutable release.
    try:
        common.validate_release_bundle(snapshot.root, expected)
    except Exception as exc:
        raise ReleaseCheckError(f"shared release-bundle validation failed: {exc}") from exc

    excluded = set(disk_exceptions)
    for relative, expected_raw in expected.items():
        if relative in excluded:
            continue
        path = _safe_repo_path(snapshot.root, relative, "reconstructed bundle")
        require(path.is_file() and not path.is_symlink(),
                f"reconstructed output is missing: {relative}")
        require(path.read_bytes() == expected_raw,
                f"source/input drift changes reconstructed output: {relative}")
    return expected


def _document_from_raw(relative: str, raw: bytes) -> Any:
    if relative.endswith(".jsonl"):
        return strict_jsonl(raw, relative)
    if relative.endswith(".json"):
        return strict_json(raw, relative)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ReleaseCheckError(f"{relative}: invalid UTF-8 Markdown") from exc


def _initial_snapshot(
    observed: ReleaseSnapshot,
    expected: Mapping[str, bytes],
) -> ReleaseSnapshot:
    raw: dict[str, bytes] = {}
    documents: dict[str, Any] = {}
    for relative in observed.raw:
        require(relative in expected,
                f"reconstructed initial bundle omits loaded authority {relative}")
        payload = expected[relative]
        raw[relative] = payload
        documents[relative] = _document_from_raw(relative, payload)
    # Manifest hashing may name builder outputs not selected by load_snapshot;
    # include them as captured initial bytes so validation never falls through
    # to an advanced on-disk Blueprint/Gantt cursor.
    for relative, payload in expected.items():
        raw.setdefault(relative, payload)
    return ReleaseSnapshot(
        observed.root, observed.release, observed.release_prefix, raw, documents,
    )


def _activation_receipt_value(
    root: Path,
    receipt: Mapping[str, Any] | str | Path | None,
    release: str,
) -> dict[str, Any]:
    require(receipt is not None,
            "boot_accepted_overlay requires an activation_receipt object or path")
    if isinstance(receipt, Mapping):
        value: Any = dict(receipt)
    else:
        path_value = Path(receipt)
        if path_value.is_absolute():
            try:
                relative = path_value.resolve().relative_to(root.resolve()).as_posix()
            except ValueError as exc:
                raise ReleaseCheckError("activation receipt path escapes repository root") from exc
        else:
            relative = PurePosixPath(path_value.as_posix()).as_posix()
        path = _safe_repo_path(root, relative, "activation receipt")
        require(path.is_file() and not path.is_symlink(),
                "activation receipt is not a regular file")
        value = strict_json(path.read_bytes(), "activation receipt")
    require(isinstance(value, dict), "activation receipt must be an object")

    schema_root = root / "Docs/catalog/stage5_1_organization/schemas"
    activation_schema = strict_json(
        (schema_root / "activation-fence.schema.json").read_bytes(),
        "activation-fence.schema.json",
    )
    common_schema = strict_json(
        (schema_root / "common.schema.json").read_bytes(), "common.schema.json",
    )
    store = {
        activation_schema["$id"]: activation_schema,
        common_schema["$id"]: common_schema,
    }
    validator = Draft202012Validator(
        activation_schema,
        resolver=RefResolver.from_schema(activation_schema, store=store),
    )
    errors = sorted(validator.iter_errors(value), key=lambda error: list(error.absolute_path))
    require(not errors, f"activation receipt schema violation: {errors[0].message}" if errors else "")
    _verify_inline_record_seal(value, "activation receipt")
    require(value.get("organization_release") == release,
            "activation receipt organization release differs")
    return value


def _accepted_blueprint(
    initial_raw: bytes,
    current_raw: bytes,
    boot_item_id: str,
    label: str,
) -> None:
    initial = initial_raw.decode("utf-8")
    marker = f"- [ ] `{boot_item_id}`"
    accepted = f"- [x] `{boot_item_id}`"
    require(initial.count(marker) == 1 and accepted not in initial,
            f"{label}: reconstructed initial BOOT row differs")
    expected = initial.replace(marker, accepted, 1).encode("utf-8")
    require(current_raw == expected,
            f"{label}: cursor transition is not exactly BOOT blank-to-accepted")


def _rerender_accepted_gantt(
    initial_raw: bytes,
    boot_item_id: str,
    post_blueprint_sha256: str,
    label: str,
) -> bytes:
    text = initial_raw.decode("utf-8")
    lines = text.splitlines()
    changed = 0
    for index, line in enumerate(lines):
        cells = line.split("|")
        if len(cells) < 5 or cells[1].strip() != f"`{boot_item_id}`":
            continue
        require(cells[3].strip() == "not_done",
                f"{label}: initial BOOT Gantt state differs")
        cells[3] = " master_accepted "
        lines[index] = "|".join(cells)
        changed += 1
    require(changed == 1, f"{label}: BOOT Gantt row is not unique")
    rendered = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    matches = list(JSON_FENCE_RE.finditer(rendered))
    require(len(matches) == 1, f"{label}: projection metadata is not unique")
    metadata = strict_json(matches[0].group("body").encode("utf-8"), f"{label} metadata")
    require(isinstance(metadata, dict), f"{label}: projection metadata malformed")
    metadata["blueprint_sha256"] = post_blueprint_sha256
    body = json.dumps(metadata, ensure_ascii=False, sort_keys=True, indent=2)
    match = matches[0]
    rendered = rendered[:match.start("body")] + body + rendered[match.end("body"):]
    return rendered.encode("utf-8")


def _validate_boot_accepted_overlay(
    observed: ReleaseSnapshot,
    initial: ReleaseSnapshot,
    receipt: Mapping[str, Any],
) -> int:
    boots = receipt.get("boot_acceptance")
    require(isinstance(boots, dict) and set(boots) == {"theorems", "conjectures"},
            "activation receipt BOOT acceptance is incomplete")
    accepted = 0
    for program, title, boot_item_id in (
        ("theorems", "Theorems", "S51THM-BOOT-001"),
        ("conjectures", "Conjectures", "S51CON-BOOT-001"),
    ):
        blueprint = f"Docs/Stage5_1_{title}_Blueprint.md"
        gantt = f"Docs/Stage5_1_{title}_Gantt.md"
        binding = boots[program]
        require(isinstance(binding, dict) and binding.get("item_id") == boot_item_id,
                f"activation receipt {program} BOOT item differs")
        initial_blueprint = initial.raw[blueprint]
        current_blueprint = observed.raw[blueprint]
        current_gantt = observed.raw[gantt]
        require(binding.get("pre_blueprint_sha256") == sha256_bytes(initial_blueprint) and
                binding.get("post_blueprint_sha256") == sha256_bytes(current_blueprint) and
                binding.get("post_gantt_sha256") == sha256_bytes(current_gantt),
                f"activation receipt {program} post-cursor digests differ")
        _accepted_blueprint(initial_blueprint, current_blueprint, boot_item_id, blueprint)
        rerendered = _rerender_accepted_gantt(
            initial.raw[gantt], boot_item_id, sha256_bytes(current_blueprint), gantt,
        )
        require(current_gantt == rerendered,
                f"{gantt}: current bytes are not the independent BOOT-accepted projection")
        accepted += 1
    return accepted


def audit_release(
    root: Path = ROOT,
    release: str = DEFAULT_RELEASE,
    *,
    rebuild: bool = True,
    cursor_mode: str = "initial_blank",
    activation_receipt: Mapping[str, Any] | str | Path | None = None,
) -> dict[str, int]:
    require(cursor_mode in {"initial_blank", "boot_accepted_overlay"},
            "cursor_mode must be initial_blank or boot_accepted_overlay")
    require(cursor_mode == "boot_accepted_overlay" or activation_receipt is None,
            "activation_receipt is only valid with boot_accepted_overlay")
    require(cursor_mode != "boot_accepted_overlay" or activation_receipt is not None,
            "boot_accepted_overlay requires an activation_receipt object or path")
    root = root.resolve()
    observed = load_snapshot(root, release)
    overlay_receipt: dict[str, Any] | None = None
    if cursor_mode == "boot_accepted_overlay":
        overlay_receipt = _activation_receipt_value(root, activation_receipt, release)
        expected = _reconstruct_initial_bundle(observed)
        snapshot = _initial_snapshot(observed, expected)
        # Overlay validation may never waive reconstruction: immutable release
        # artifacts and Current remain byte-identical to the initial bundle.
        validate_common_and_rebuild(
            snapshot, expected_bundle=expected, disk_exceptions=PROJECTION_FILES,
        )
    else:
        snapshot = observed
    validate_json_schemas(snapshot)
    validate_current_manifest_and_inputs(snapshot)
    state = validate_member_bijections(snapshot)
    taxonomy = validate_taxonomy(snapshot, state)
    relation_state = validate_relations_and_hard_dag(snapshot, state, taxonomy)
    validate_dependency_closure_and_worksets(snapshot, state, relation_state)
    validate_blueprints_and_gantts(snapshot, state, taxonomy)
    if cursor_mode == "initial_blank" and rebuild:
        validate_common_and_rebuild(snapshot)
    counts = {
        "members": len(state["objects"]),
        "legacy_rows": len(state["legacy"]),
        "subjects": len(taxonomy["nodes"]),
        "relations": len(relation_state["relations"]),
        "hard_edges": len(relation_state["hard_relation_ids"]),
    }
    if cursor_mode == "boot_accepted_overlay":
        require(overlay_receipt is not None, "activation receipt unexpectedly absent")
        counts["boot_accepted_rows"] = _validate_boot_accepted_overlay(
            observed, snapshot, overlay_receipt,
        )
    return counts


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--release", default=DEFAULT_RELEASE)
    parser.add_argument(
        "--cursor-mode",
        choices=("initial_blank", "boot_accepted_overlay"),
        default="initial_blank",
    )
    parser.add_argument(
        "--activation-receipt",
        help="repository-relative receipt path required by boot_accepted_overlay",
    )
    parser.add_argument(
        "--no-rebuild",
        action="store_true",
        help="skip only the deterministic in-memory input-drift reconstruction",
    )
    args = parser.parse_args(argv)
    try:
        counts = audit_release(
            args.root,
            args.release,
            rebuild=not args.no_rebuild,
            cursor_mode=args.cursor_mode,
            activation_receipt=args.activation_receipt,
        )
    except (OSError, ReleaseCheckError) as exc:
        print(f"stage5.1 organization release check failed: {exc}", file=sys.stderr)
        return 1
    print(
        "stage5.1 organization release check passed "
        f"({counts['members']} members, {counts['legacy_rows']} legacy rows, "
        f"{counts['subjects']} subjects, {counts['relations']} relations, "
        f"{counts['hard_edges']} hard edges)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
