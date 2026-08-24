#!/usr/bin/env python3
"""Validate non-TARGET Stage5 theorem preparation artifacts in isolation.

This is deliberately a structural gate before canonical Master validation. It
never advances a Blueprint row and never trusts worker-supplied acceptance.
The Master replays the exact mode-specific semantics against authoritative
dependency rows and current repository bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any


SHA = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN = re.compile(r"(?m)^\s*(?:sorry|admit|axiom|unsafe\s+(?:def|theorem)|opaque)\b")


class ProgramItemError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(value if isinstance(value, bytes) else canonical(value)).hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise ProgramItemError(f"missing regular JSON artifact: {path}")
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in rows:
            if key in result:
                raise ProgramItemError(f"duplicate JSON key {key!r}: {path}")
            result[key] = value
        return result
    try:
        value = json.loads(path.read_bytes(), object_pairs_hook=pairs,
                           parse_constant=lambda value: (_ for _ in ()).throw(
                               ProgramItemError(f"non-finite JSON number {value}: {path}")))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProgramItemError(f"invalid strict JSON: {path}") from exc
    if not isinstance(value, dict):
        raise ProgramItemError(f"JSON artifact is not an object: {path}")
    return value


def safe_relative(value: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or path.as_posix() != value or "." in path.parts or ".." in path.parts:
        raise ProgramItemError(f"unsafe artifact path {value!r}")
    return value


def sealed(value: dict[str, Any], label: str) -> None:
    authority = value.get("authority_sha256")
    body = dict(value)
    body.pop("authority_sha256", None)
    if not isinstance(authority, str) or not SHA.fullmatch(authority) or digest(body) != authority:
        raise ProgramItemError(f"{label}: authority seal differs")


def nonempty(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ProgramItemError(f"{label}: missing regular file")
    raw = path.read_bytes()
    if not raw.strip():
        raise ProgramItemError(f"{label}: empty")
    if path.suffix == ".lean" and FORBIDDEN.search(raw.decode("utf-8", "replace")):
        raise ProgramItemError(f"{label}: forbidden proof placeholder")
    return raw


def validate_claim(claim: dict[str, Any], claim_path: Path, work: Path) -> dict[str, Any]:
    if claim.get("program") != "stage5-theorem-proof-debt/2.0":
        raise ProgramItemError("claim program differs")
    item_id = claim.get("item_id")
    mode = claim.get("mode")
    if not isinstance(item_id, str) or not isinstance(mode, str):
        raise ProgramItemError("claim mode identity is malformed")
    expected_mode = (
        "SHARD" if item_id.startswith("S5THM-SHARD-") else
        "AGG" if item_id == "S5THM-AGG-001" else
        "QA" if item_id == "S5THM-QA-001" else
        "PROGRAM-RELEASE" if item_id == "S5THM-PROGRAM-RELEASE" else None
    )
    if expected_mode != mode:
        raise ProgramItemError(f"claim mode differs: expected {expected_mode}, observed {mode}")
    owned = claim.get("writable_paths")
    if not isinstance(owned, list) or not owned or len(set(owned)) != len(owned):
        raise ProgramItemError("claim ownership is malformed")
    for relative in owned:
        safe_relative(relative)
        nonempty(work / relative, f"owned artifact {relative}")
    if mode == "SHARD":
        if len(owned) != 1 or not owned[0].startswith("Docs/evidence/stage5_theorems/shards/"):
            raise ProgramItemError("SHARD ownership differs")
        value = strict_json(work / owned[0])
        sealed(value, "SHARD artifact")
        if value.get("item_id") != item_id or value.get("program") != claim["program"]:
            raise ProgramItemError("SHARD identity differs")
        dependencies = claim.get("dependencies")
        members = value.get("members")
        if not isinstance(dependencies, list) or not isinstance(members, list) or len(members) != len(dependencies):
            raise ProgramItemError("SHARD member cardinality differs")
        ids = [row.get("item_id") for row in members if isinstance(row, dict)]
        if len(ids) != len(members) or len(set(ids)) != len(ids) or set(ids) != set(dependencies):
            raise ProgramItemError("SHARD member ID set differs")
        if value.get("member_count") != len(members):
            raise ProgramItemError("SHARD member_count differs")
    elif mode == "AGG":
        if len(owned) != 2 or not any(path.endswith("Theorems.lean") for path in owned):
            raise ProgramItemError("AGG ownership differs")
        json_paths = [path for path in owned if path.endswith(".json")]
        if len(json_paths) != 1:
            raise ProgramItemError("AGG manifest is missing")
        value = strict_json(work / json_paths[0]); sealed(value, "aggregate artifact")
        if value.get("item_id") != item_id or value.get("program") != claim["program"]:
            raise ProgramItemError("aggregate identity differs")
    elif mode == "QA":
        if len(owned) != 3 or not any(path.endswith("program-acceptance.json") for path in owned):
            raise ProgramItemError("QA ownership differs")
        value = strict_json(work / next(path for path in owned if path.endswith("program-acceptance.json")))
        sealed(value, "QA artifact")
        if value.get("item_id") != item_id or value.get("program") != claim["program"]:
            raise ProgramItemError("QA identity differs")
    else:
        if len(owned) != 2 or not any(path.endswith("Proof_Debt_Final_Review.md") for path in owned):
            raise ProgramItemError("PROGRAM-RELEASE ownership differs")
        value = strict_json(work / next(path for path in owned if path.endswith("program-release-acceptance.json")))
        sealed(value, "program-release artifact")
        if value.get("item_id") != item_id or value.get("program") != claim["program"]:
            raise ProgramItemError("program-release identity differs")
    return {"valid": True, "item_id": item_id, "mode": mode}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim-card", required=True, type=Path)
    parser.add_argument("--work-root", required=True, type=Path)
    args = parser.parse_args()
    try:
        claim = strict_json(args.claim_card)
        validate_claim(claim, args.claim_card, args.work_root)
    except (OSError, ProgramItemError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps({"valid": True, "item_id": claim["item_id"], "mode": claim["mode"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
