#!/usr/bin/env python3
"""Resolve one sealed Stage5 theorem integration conflict without data loss.

The normal Master integrator never overwrites a different canonical file.  An
operator may use this tool only after proving that every conflicting path is
either an older Master-accepted artifact or an unaccepted artifact from one
identified historical worker generation.  The tool content-addresses those
bytes under the durable ``superseded`` evidence tree, archives the original
repair receipt, removes only the proved conflicting paths, and writes sealed
intent/completion receipts.  The immutable handoff and integration entry stay
in place for an ordinary controller tick to validate and integrate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
from typing import Any

import stage5_theorems_execution_cron_v2 as controller


SCHEMA_INTENT = "awesome-theorems/stage5-canonical-conflict-resolution-intent/1.0"
SCHEMA_COMPLETION = "awesome-theorems/stage5-canonical-conflict-resolution/1.0"
SUPERSEDED_ROOT = (
    controller.ROOT
    / "Docs/evidence/stage5_theorems/execution/superseded/canonical-conflicts"
)


def _repo_path(value: str, label: str) -> Path:
    pure = PurePosixPath(value)
    if pure.is_absolute() or not pure.parts or any(part in {"", ".", ".."} for part in pure.parts):
        raise controller.ControllerError(f"{label}: expected a normalized repository-relative path")
    path = controller.ROOT.joinpath(*pure.parts)
    if not path.is_relative_to(controller.ROOT):
        raise controller.ControllerError(f"{label}: path escapes repository")
    return path


def _sealed(path: Path, label: str) -> dict[str, Any]:
    return controller.verify_seal(
        controller.strict_json(controller._regular(path, label), label), label
    )


def _fsync_parent(path: Path) -> None:
    descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _provenance_map(
    *, kind: str, source: Path, item_id: str, conflicts: list[dict[str, Any]]
) -> dict[str, str]:
    expected = {row["path"]: row["sha256"] for row in conflicts}
    if kind == "master_acceptance":
        acceptance = _sealed(source, "superseded Master acceptance")
        if acceptance.get("item_id") != item_id:
            raise controller.ControllerError("Master acceptance item differs")
        integrated = acceptance.get("integration", {}).get("integrated_files")
        if not isinstance(integrated, list):
            raise controller.ControllerError("Master acceptance integrated files are absent")
        observed = {
            row.get("path"): row.get("sha256")
            for row in integrated
            if isinstance(row, dict)
        }
    elif kind == "historical_generation":
        if source.is_symlink() or not source.is_dir():
            raise controller.ControllerError("historical generation root is not a real directory")
        claim = controller.strict_json(
            controller._regular(source / "claim.json", "historical claim"),
            "historical claim",
        )
        if not isinstance(claim, dict) or claim.get("item_id") != item_id:
            raise controller.ControllerError("historical generation claim item differs")
        if claim.get("run_id") != source.name:
            raise controller.ControllerError("historical generation run identity differs")
        observed: dict[str, str] = {}
        for relative in expected:
            artifact = source / "work" / controller._safe_relative(relative)
            observed[relative] = controller.file_digest(artifact)
    else:
        raise controller.ControllerError("unsupported provenance kind")
    if observed != expected:
        missing = sorted(set(expected) - set(observed))
        different = sorted(
            path for path in set(expected) & set(observed) if expected[path] != observed[path]
        )
        extra = sorted(set(observed) - set(expected))
        raise controller.ControllerError(
            f"provenance differs: missing={missing}, different={different}, extra={extra}"
        )
    return observed


def resolve(
    *, entry_path: Path, provenance_kind: str, provenance_path: Path, reason: str
) -> dict[str, Any]:
    integration_dir = controller.INTEGRATION_QUEUE.resolve()
    if entry_path.parent.resolve() != integration_dir or entry_path.suffix != ".json":
        raise controller.ControllerError("entry must be one active theorem integration JSON")
    entry = _sealed(entry_path, "integration entry")
    entry_sha = controller.file_digest(entry_path)
    item_id = entry.get("item_id")
    if not isinstance(item_id, str):
        raise controller.ControllerError("integration entry item is absent")
    resolution_root = SUPERSEDED_ROOT / item_id / entry_sha
    intent_path = resolution_root / "intent.json"
    completion_path = resolution_root / "completion.json"
    if completion_path.is_file():
        completion = _sealed(completion_path, "conflict resolution completion")
        if (
            completion.get("entry_sha256") != entry_sha
            or completion.get("item_id") != item_id
        ):
            raise controller.ControllerError("conflict resolution completion binding differs")
        return completion
    repair_path = controller.integration_repair_dir() / f"{entry_path.name}.repair.json"
    queue = _repo_path(str(entry.get("queue")), "handoff queue")
    manifest_path = queue / "harvest-manifest.json"
    manifest = _sealed(manifest_path, "harvest manifest")
    if manifest.get("item_id") != item_id or manifest.get("run_id") != entry.get("run_id"):
        raise controller.ControllerError("harvest manifest binding differs")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise controller.ControllerError("harvest artifacts are absent")

    if intent_path.is_file():
        intent = _sealed(intent_path, "conflict resolution intent")
        if (
            intent.get("entry_sha256") != entry_sha
            or intent.get("provenance", {}).get("kind") != provenance_kind
            or intent.get("provenance", {}).get("path")
            != provenance_path.relative_to(controller.ROOT).as_posix()
            or intent.get("manifest_sha256") != controller.file_digest(manifest_path)
        ):
            raise controller.ControllerError("existing resolution intent differs")
        conflicts = intent["conflicts"]
    else:
        repair = _sealed(repair_path, "integration repair")
        if repair.get("entry_sha256") != entry_sha or repair.get("item_id") != item_id:
            raise controller.ControllerError("repair receipt binding differs")
        if "canonical destination already exists" not in str(repair.get("reason", "")):
            raise controller.ControllerError("repair is not a canonical destination conflict")
        conflicts: list[dict[str, Any]] = []
        for artifact in artifacts:
            relative = artifact.get("path")
            if not isinstance(relative, str):
                raise controller.ControllerError("harvest artifact path is malformed")
            destination = controller.ROOT / controller._safe_relative(relative)
            if destination.is_symlink():
                raise controller.ControllerError(f"canonical conflict is a symlink: {relative}")
            if not destination.exists():
                continue
            if not destination.is_file():
                raise controller.ControllerError(f"canonical conflict is not a file: {relative}")
            current_sha = controller.file_digest(destination)
            if current_sha == artifact.get("sha256"):
                continue
            conflicts.append(
                {
                    "path": relative,
                    "sha256": current_sha,
                    "size_bytes": destination.stat().st_size,
                    "replacement_sha256": artifact.get("sha256"),
                }
            )
        if not conflicts:
            raise controller.ControllerError("integration entry has no different canonical conflicts")
        _provenance_map(
            kind=provenance_kind,
            source=provenance_path,
            item_id=item_id,
            conflicts=conflicts,
        )
        body = {
            "schema_version": SCHEMA_INTENT,
            "program": controller.PROGRAM,
            "item_id": item_id,
            "claim_id": entry.get("claim_id"),
            "run_id": entry.get("run_id"),
            "entry_path": entry_path.relative_to(controller.ROOT).as_posix(),
            "entry_sha256": entry_sha,
            "repair_path": repair_path.relative_to(controller.ROOT).as_posix(),
            "repair_sha256": controller.file_digest(repair_path),
            "manifest_path": manifest_path.relative_to(controller.ROOT).as_posix(),
            "manifest_sha256": controller.file_digest(manifest_path),
            "provenance": {
                "kind": provenance_kind,
                "path": provenance_path.relative_to(controller.ROOT).as_posix(),
                "sha256": (
                    controller.file_digest(provenance_path)
                    if provenance_path.is_file()
                    else controller.file_digest(provenance_path / "claim.json")
                ),
            },
            "reason": reason,
            "conflicts": conflicts,
            "prepared_at": controller.now(),
        }
        intent = controller.seal(body)
        controller.atomic_json(intent_path, intent, 0o444)

    # Revalidate provenance on every retry, including after an interrupted
    # removal, using the immutable intent rather than mutable canonical paths.
    _provenance_map(
        kind=provenance_kind,
        source=provenance_path,
        item_id=item_id,
        conflicts=conflicts,
    )
    archived: list[dict[str, Any]] = []
    for conflict in conflicts:
        relative = conflict["path"]
        source = controller.ROOT / controller._safe_relative(relative)
        archive = resolution_root / "artifacts" / controller._safe_relative(relative)
        if source.exists():
            if source.is_symlink() or not source.is_file():
                raise controller.ControllerError(f"canonical conflict changed type: {relative}")
            if controller.file_digest(source) != conflict["sha256"]:
                raise controller.ControllerError(f"canonical conflict changed bytes: {relative}")
            controller._copy_immutable(source, archive, "superseded canonical artifact")
        elif not archive.is_file() or controller.file_digest(archive) != conflict["sha256"]:
            raise controller.ControllerError(f"canonical conflict disappeared before archive: {relative}")
        archived.append(
            {
                **conflict,
                "archive_path": archive.relative_to(controller.ROOT).as_posix(),
            }
        )

    repair_archive = resolution_root / "integration-repair.json"
    if repair_path.exists():
        controller._copy_immutable(repair_path, repair_archive, "integration repair archive")
    elif not repair_archive.is_file() or controller.file_digest(repair_archive) != intent["repair_sha256"]:
        raise controller.ControllerError("integration repair disappeared before archive")

    # The complete immutable archive and intent exist before canonical bytes
    # are removed.  Each unlink is immediately preceded by an exact digest
    # check and followed by a directory fsync.
    for conflict in conflicts:
        source = controller.ROOT / controller._safe_relative(conflict["path"])
        if source.exists():
            if source.is_symlink() or not source.is_file() or controller.file_digest(source) != conflict["sha256"]:
                raise controller.ControllerError(f"canonical conflict changed before removal: {conflict['path']}")
            source.unlink()
            _fsync_parent(source)
    if repair_path.exists():
        if controller.file_digest(repair_path) != intent["repair_sha256"]:
            raise controller.ControllerError("integration repair changed before disposition")
        repair_path.unlink()
        _fsync_parent(repair_path)

    completion = controller.seal(
        {
            "schema_version": SCHEMA_COMPLETION,
            "program": controller.PROGRAM,
            "item_id": item_id,
            "claim_id": entry.get("claim_id"),
            "run_id": entry.get("run_id"),
            "entry_path": entry_path.relative_to(controller.ROOT).as_posix(),
            "entry_sha256": entry_sha,
            "intent_path": intent_path.relative_to(controller.ROOT).as_posix(),
            "intent_sha256": controller.file_digest(intent_path),
            "repair_archive_path": repair_archive.relative_to(controller.ROOT).as_posix(),
            "repair_archive_sha256": controller.file_digest(repair_archive),
            "archived_conflicts": archived,
            "next_action": "ordinary controller tick revalidates the immutable handoff",
            "completed_at": controller.now(),
        }
    )
    controller.atomic_json(completion_path, completion, 0o444)
    return completion


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--entry", required=True)
    parser.add_argument(
        "--provenance-kind",
        required=True,
        choices=("master_acceptance", "historical_generation"),
    )
    parser.add_argument("--provenance", required=True)
    parser.add_argument("--reason", required=True)
    args = parser.parse_args(argv)
    try:
        entry = _repo_path(args.entry, "entry")
        provenance = _repo_path(args.provenance, "provenance")
        # Match the controller's pump -> short scheduler lock order.  This
        # prevents a cron tick from observing a partial repair disposition.
        with controller.admission_pump_guard():
            with controller.scheduler_guard():
                result = resolve(
                    entry_path=entry,
                    provenance_kind=args.provenance_kind,
                    provenance_path=provenance,
                    reason=args.reason,
                )
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
