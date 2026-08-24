#!/usr/bin/env python3
"""Digest-checked, read-only query surface for the current Stage5.1 release."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CATALOG_ROOT = Path("Docs/catalog/stage5_1_organization")
RELEASE_FILES = (
    "Subject_Taxonomy.json",
    "Subject_Nodes.jsonl",
    "Object_Index.jsonl",
    "Legacy_Checklist_Row_Crosswalk.jsonl",
    "Subject_Assignments.jsonl",
    "Dependency_Assessments.jsonl",
    "Relation_Edges.jsonl",
    "Execution_Hard_DAG.json",
    "Dependency_Closure.jsonl",
    "programs/theorems/Organization_Workset.jsonl",
    "programs/conjectures/Organization_Workset.jsonl",
)


class QueryError(RuntimeError):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _regular(path: Path) -> None:
    if not path.is_file() or path.is_symlink():
        raise QueryError(f"missing regular release file: {path}")


def read_json(path: Path) -> dict[str, Any]:
    _regular(path)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise QueryError(f"{path}: expected object")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    _regular(path)
    raw = path.read_bytes()
    if raw and not raw.endswith(b"\n"):
        raise QueryError(f"{path}: JSONL lacks final LF")
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(raw.splitlines(), 1):
        if not line:
            raise QueryError(f"{path}:{number}: blank row")
        value = json.loads(line)
        if not isinstance(value, dict):
            raise QueryError(f"{path}:{number}: expected object")
        rows.append(value)
    return rows


def verify_seal(value: dict[str, Any], field: str, label: str) -> None:
    observed = value.get(field)
    body = dict(value)
    body.pop(field, None)
    if not isinstance(observed, str) or observed != hashlib.sha256(canonical_json(body)).hexdigest():
        raise QueryError(f"{label} {field} differs")


def _repo_file(root: Path, relative: Any, label: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise QueryError(f"{label}: invalid repository-relative path")
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise QueryError(f"{label}: path escapes repository") from exc
    return path


def _unique(rows: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        identity = row.get(key)
        if not isinstance(identity, str) or identity in result:
            raise QueryError(f"{label}: missing or duplicate {key}: {identity}")
        result[identity] = row
    return result


def load(root: Path) -> dict[str, Any]:
    current_path = root / CATALOG_ROOT / "Current_Release.json"
    current = read_json(current_path)
    verify_seal(current, "authority_sha256", "Current_Release")
    release = current.get("organization_release")
    if not isinstance(release, str) or not release:
        raise QueryError("Current_Release lacks organization_release")
    manifest_binding = current.get("manifest")
    if not isinstance(manifest_binding, dict):
        raise QueryError("Current_Release lacks manifest binding")
    manifest_path = _repo_file(root, manifest_binding.get("path"), "manifest binding")
    expected_manifest = root / CATALOG_ROOT / "releases" / release / "Organization_Manifest.json"
    if manifest_path != expected_manifest.resolve():
        raise QueryError("Current_Release manifest path does not select its release")
    manifest = read_json(manifest_path)
    if sha256(manifest_path) != manifest_binding.get("sha256"):
        raise QueryError("Current_Release manifest SHA-256 differs")
    verify_seal(manifest, "authority_sha256", "Organization_Manifest")
    if (manifest.get("authority_sha256") != manifest_binding.get("authority_sha256")
            or manifest.get("organization_release") != release):
        raise QueryError("Current_Release manifest authority/release differs")

    artifact_bindings: dict[str, dict[str, Any]] = {}
    for binding in manifest.get("artifacts", []):
        if not isinstance(binding, dict) or not isinstance(binding.get("path"), str):
            raise QueryError("Organization_Manifest has malformed artifact binding")
        if binding["path"] in artifact_bindings:
            raise QueryError(f"Organization_Manifest duplicates {binding['path']}")
        artifact_bindings[binding["path"]] = binding

    base_relative = CATALOG_ROOT / "releases" / release
    loaded: dict[str, Any] = {}
    json_files = {"Subject_Taxonomy.json", "Execution_Hard_DAG.json"}
    for suffix in RELEASE_FILES:
        relative = (base_relative / suffix).as_posix()
        binding = artifact_bindings.get(relative)
        if binding is None:
            raise QueryError(f"manifest lacks queried artifact binding: {relative}")
        path = _repo_file(root, relative, "artifact binding")
        _regular(path)
        if sha256(path) != binding.get("sha256"):
            raise QueryError(f"manifest artifact SHA-256 differs: {relative}")
        loaded[suffix] = read_json(path) if suffix in json_files else read_jsonl(path)

    objects = _unique(loaded["Object_Index.jsonl"], "object_id", "Object_Index")
    assignments = _unique(loaded["Subject_Assignments.jsonl"], "object_id", "Subject_Assignments")
    nodes = _unique(loaded["Subject_Nodes.jsonl"], "subject_id", "Subject_Nodes")
    assessments = _unique(loaded["Dependency_Assessments.jsonl"], "object_id", "Dependency_Assessments")
    closures = _unique(loaded["Dependency_Closure.jsonl"], "item_id", "Dependency_Closure")
    by_any: dict[str, str] = {}
    for object_id, row in objects.items():
        for key in ("object_id", "stage51_item_id", "legacy_item_id", "stage5_claim_id", "variant_id", "pool_id"):
            value = row.get(key)
            if isinstance(value, str):
                if value in by_any and by_any[value] != object_id:
                    raise QueryError(f"ambiguous member identity: {value}")
                by_any[value] = object_id

    checklist_by_any: dict[str, list[dict[str, Any]]] = {}
    for row in loaded["Legacy_Checklist_Row_Crosswalk.jsonl"]:
        identities = [row.get("legacy_item_id"), *row.get("new_item_ids", [])]
        for identity in identities:
            if not isinstance(identity, str):
                raise QueryError("checklist crosswalk has malformed identity")
            checklist_by_any.setdefault(identity, []).append(row)

    worksets: dict[str, dict[str, Any]] = {}
    for program in ("theorems", "conjectures"):
        for row in loaded[f"programs/{program}/Organization_Workset.jsonl"]:
            object_id = row.get("object_id")
            if not isinstance(object_id, str) or object_id in worksets:
                raise QueryError(f"worksets have missing or duplicate object_id: {object_id}")
            worksets[object_id] = row

    return {
        "release": release,
        "current": current,
        "manifest": manifest,
        "manifest_sha256": manifest_binding["sha256"],
        "objects": objects,
        "by_any": by_any,
        "assignments": assignments,
        "nodes": nodes,
        "taxonomy": loaded["Subject_Taxonomy.json"],
        "relations": loaded["Relation_Edges.jsonl"],
        "assessments": assessments,
        "closures": closures,
        "hard_dag": loaded["Execution_Hard_DAG.json"],
        "checklist": checklist_by_any,
        "worksets": worksets,
    }


def breadcrumb(node_id: str, nodes: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    cursor: str | None = node_id
    while cursor is not None:
        if cursor in seen or cursor not in nodes:
            raise QueryError(f"invalid subject parent chain at {cursor}")
        seen.add(cursor)
        node = nodes[cursor]
        result.append({
            "subject_id": cursor, "notation": node.get("notation"),
            "label": node["label"]["en"], "rank": node.get("rank"),
        })
        cursor = node.get("parent_subject_id")
    return list(reversed(result))


def subject_granularity(node: dict[str, Any]) -> str:
    notation = str(node.get("notation") or "")
    if node.get("rank") in {"root", "sentinel"}:
        return node["rank"]
    if node.get("scheme") == "MSC" and len(notation) == 5 and not notation.endswith(("xx", "-XX")):
        return "fine"
    if node.get("scheme") == "MSC" and notation.endswith("xx"):
        return "intermediate"
    return "broad" if node.get("rank") == "branch" else "fine"


def top_branch(node_id: str, data: dict[str, Any]) -> str | None:
    nodes = data["nodes"]
    root = data["taxonomy"].get("root_subject_id")
    if node_id == root or node_id not in nodes or nodes[node_id].get("rank") == "sentinel":
        return None
    cursor = node_id
    seen: set[str] = set()
    while nodes[cursor].get("parent_subject_id") != root:
        if cursor in seen or nodes[cursor].get("parent_subject_id") not in nodes:
            raise QueryError(f"invalid subject root chain at {cursor}")
        seen.add(cursor)
        cursor = nodes[cursor]["parent_subject_id"]
    return cursor


def coordinate(data: dict[str, Any], node_id: str, role: str,
               assignment: dict[str, Any]) -> dict[str, Any]:
    node = data["nodes"][node_id]
    primary = assignment["primary"]
    if role == "primary":
        granularity = primary["granularity"]
        status = primary["assertion_state"]
        evidence_tier = primary["evidence_tier"]
        evidence = primary["evidence"]
    else:
        granularity = subject_granularity(node)
        status = assignment["classification_status"]
        evidence_tier = None
        evidence = []
    return {
        "role": role, "subject_id": node_id,
        "breadcrumb": breadcrumb(node_id, data["nodes"]),
        "granularity": granularity, "status": status,
        "review_state": assignment["review"]["state"],
        "evidence_tier": evidence_tier, "evidence": evidence,
        "root_subject_id": top_branch(node_id, data),
    }


def show_member(data: dict[str, Any], identity: str,
                plane: str | None, direction: str | None) -> dict[str, Any]:
    object_id = data["by_any"].get(identity)
    checklist_matches = data["checklist"].get(identity, [])
    if object_id is None:
        if checklist_matches:
            return {
                "query_identity": identity, "checklist_crosswalks": checklist_matches,
                "mathematical_member": None,
            }
        raise QueryError(f"unknown Stage5/Stage5.1 identity: {identity}")
    obj = data["objects"][object_id]
    assignment = data["assignments"][object_id]
    primary = coordinate(data, assignment["primary"]["subject_id"], "primary", assignment)
    secondary = [coordinate(data, value, "secondary", assignment) for value in assignment["secondary_subject_ids"]]
    candidates = [coordinate(data, value, "candidate", assignment) for value in assignment["candidate_subject_ids"]]
    candidate_roots = sorted({row["root_subject_id"] for row in candidates if row["root_subject_id"]})
    coordinate_roots = sorted({
        row["root_subject_id"]
        for row in [primary, *secondary, *candidates]
        if row["root_subject_id"]
    })
    assignment_accepted = assignment["classification_status"] == "accepted"

    relations = []
    for row in data["relations"]:
        if row["consumer_member_id"] == object_id:
            relation_direction, counterpart = "requires", row["provider_member_id"]
        elif row["provider_member_id"] == object_id:
            relation_direction, counterpart = "used_by", row["consumer_member_id"]
        else:
            continue
        if plane is not None and row["plane"] != plane:
            continue
        if direction is not None and relation_direction != direction:
            continue
        counterpart_object = data["objects"].get(counterpart)
        relations.append({
            "edge_id": row["edge_id"], "plane": row["plane"],
            "type": row["relation_type"], "direction": relation_direction,
            "counterpart": counterpart,
            "counterpart_item_id": counterpart_object.get("stage51_item_id") if counterpart_object else None,
            "review_state": row["review_state"], "evidence_tier": row["evidence_tier"],
            "evidence": row["evidence"], "blocking": row["blocking"],
            "scheduler_effect": row["scheduler_effect"],
        })
    relations.sort(key=lambda row: row["edge_id"])

    item_id = obj["stage51_item_id"]
    hard_edges = []
    for edge in data["hard_dag"].get("edges", []):
        if edge["consumer_member_id"] == object_id:
            edge_direction, counterpart = "requires", edge["provider_member_id"]
        elif edge["provider_member_id"] == object_id:
            edge_direction, counterpart = "used_by", edge["consumer_member_id"]
        else:
            continue
        hard_edges.append({**edge, "direction": edge_direction, "counterpart": counterpart})

    member_checklists = checklist_matches
    if not member_checklists:
        member_checklists = data["checklist"].get(obj["legacy_item_id"], [])
    return {
        "query_identity": identity,
        "release": {
            "organization_release": data["release"],
            "current_authority_sha256": data["current"]["authority_sha256"],
            "manifest_sha256": data["manifest_sha256"],
            "manifest_authority_sha256": data["manifest"]["authority_sha256"],
        },
        "object": obj,
        "checklist_crosswalks": member_checklists,
        "classification": {
            "status": assignment["classification_status"],
            "review": assignment["review"],
            "primary": primary, "secondary": secondary, "candidates": candidates,
            "cross_domain": assignment["cross_domain"],
            "candidate_cross_root_hint": {
                # A hint exposes a non-accepted review queue only.  It never
                # promotes coordinate multiplicity to an accepted relation or
                # to a scheduler dependency.
                "value": not assignment_accepted and len(coordinate_roots) > 1,
                "candidate_root_subject_ids": candidate_roots,
                "assignment_coordinate_root_subject_ids": coordinate_roots,
                "accepted_cross_domain_assertion": bool(
                    assignment_accepted and assignment["cross_domain"]["value"]
                ),
                "scheduler_effect": "none",
            },
        },
        "relations": relations,
        "dependency_assessment": data["assessments"][object_id],
        "hard_dag": {
            "authority_sha256": data["hard_dag"].get("authority_sha256"),
            "incident_edges": sorted(hard_edges, key=lambda row: row["edge_id"]),
        },
        "hard_dependency_closure": data["closures"][item_id],
        "execution_dependencies": data["worksets"][object_id]["execution_dependency_item_ids"],
    }


def list_subject(data: dict[str, Any], subject_id: str, limit: int) -> dict[str, Any]:
    if subject_id not in data["nodes"]:
        raise QueryError(f"unknown subject: {subject_id}")
    members = []
    for object_id, assignment in data["assignments"].items():
        roles = []
        if assignment["primary"]["subject_id"] == subject_id:
            roles.append("primary")
        if subject_id in assignment["secondary_subject_ids"]:
            roles.append("secondary")
        if subject_id in assignment["candidate_subject_ids"]:
            roles.append("candidate")
        if roles:
            members.append({"object_id": object_id, "roles": roles})
    members.sort(key=lambda row: row["object_id"])
    return {
        "subject": breadcrumb(subject_id, data["nodes"]),
        "member_count": len(members), "members": members[:limit],
        "truncated": len(members) > limit,
    }


def summary(data: dict[str, Any]) -> dict[str, Any]:
    assignments = list(data["assignments"].values())
    return {
        "organization_release": data["release"],
        "current_authority_sha256": data["current"]["authority_sha256"],
        "manifest_sha256": data["manifest_sha256"],
        "manifest_authority_sha256": data["manifest"]["authority_sha256"],
        "members": len(data["objects"]), "subject_nodes": len(data["nodes"]),
        "relations": len(data["relations"]),
        "classification_status": dict(sorted(Counter(row["classification_status"] for row in assignments).items())),
        "relation_planes": dict(sorted(Counter(row["plane"] for row in data["relations"]).items())),
        "relation_review_states": dict(sorted(Counter(row["review_state"] for row in data["relations"]).items())),
        "dependency_assessment_states": dict(sorted(Counter(row["audit_status"] for row in data["assessments"].values()).items())),
        "hard_edges": len(data["hard_dag"].get("edges", [])),
    }


def find_subject(data: dict[str, Any], query: str, limit: int) -> dict[str, Any]:
    folded = query.casefold()
    rows = [
        {"subject_id": identity, "notation": row.get("notation"), "label": row["label"]["en"],
         "granularity": subject_granularity(row), "breadcrumb": breadcrumb(identity, data["nodes"])}
        for identity, row in data["nodes"].items()
        if folded in identity.casefold() or folded in str(row.get("notation") or "").casefold()
        or folded in row["label"]["en"].casefold()
    ]
    rows.sort(key=lambda row: row["subject_id"])
    return {"query": query, "match_count": len(rows), "matches": rows[:limit], "truncated": len(rows) > limit}


def children(data: dict[str, Any], subject_id: str, limit: int) -> dict[str, Any]:
    if subject_id not in data["nodes"]:
        raise QueryError(f"unknown subject: {subject_id}")
    rows = [
        {"subject_id": identity, "notation": row.get("notation"), "label": row["label"]["en"],
         "granularity": subject_granularity(row)}
        for identity, row in data["nodes"].items() if row.get("parent_subject_id") == subject_id
    ]
    rows.sort(key=lambda row: row["subject_id"])
    return {"subject": breadcrumb(subject_id, data["nodes"]), "child_count": len(rows),
            "children": rows[:limit], "truncated": len(rows) > limit}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--summary", action="store_true")
    group.add_argument("--member")
    group.add_argument("--subject")
    group.add_argument("--find-subject")
    group.add_argument("--children")
    parser.add_argument("--plane")
    parser.add_argument("--direction", choices=("requires", "used_by"))
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    try:
        if args.limit < 1:
            raise QueryError("--limit must be positive")
        if (args.plane or args.direction) and not args.member:
            raise QueryError("--plane/--direction require --member")
        data = load(args.root.resolve())
        if args.summary:
            result = summary(data)
        elif args.member:
            result = show_member(data, args.member, args.plane, args.direction)
        elif args.subject:
            result = list_subject(data, args.subject, args.limit)
        elif args.find_subject:
            result = find_subject(data, args.find_subject, args.limit)
        else:
            result = children(data, args.children, args.limit)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except (OSError, json.JSONDecodeError, KeyError, TypeError, QueryError) as exc:
        print(f"Stage5.1 query failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
