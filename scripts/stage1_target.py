#!/usr/bin/env python3
"""Inspect and verify the immutable Stage1 rev-5.6 target population."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "Docs" / "Stage1_Targets_rev-5.6.json"


def fail(message: str) -> NoReturn:
    raise SystemExit(f"stage1_target: {message}")


def load_manifest() -> dict[str, Any]:
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except OSError as exc:
        fail(f"cannot read {MANIFEST.relative_to(ROOT)}: {exc}")
    except json.JSONDecodeError as exc:
        fail(f"invalid target manifest JSON: {exc}")
    if not isinstance(data, dict):
        fail("target manifest must be a JSON object")
    return data


def checked_targets(data: dict[str, Any]) -> list[dict[str, Any]]:
    if data.get("schema_version") != "stage1-target-set/5.6.2":
        fail("unsupported or stale manifest schema")
    targets = data.get("targets")
    if not isinstance(targets, list) or len(targets) != 1546:
        fail("manifest must contain exactly 1546 target objects")
    if not all(isinstance(target, dict) for target in targets):
        fail("every target must be a JSON object")
    ranks = [target.get("execution_rank") for target in targets]
    if ranks != list(range(1, 1547)):
        fail("execution ranks must be contiguous from 1 through 1546")
    theorem_ids = [target.get("theorem_id") for target in targets]
    if not all(isinstance(theorem_id, str) for theorem_id in theorem_ids):
        fail("every target must have a string theorem_id")
    if len(set(theorem_ids)) != 1546:
        fail("target theorem IDs are not unique")
    payload = "\n".join(sorted(theorem_ids)) + "\n"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    scope = data.get("scope")
    if not isinstance(scope, dict):
        fail("manifest scope must be an object")
    if scope.get("canonical_sorted_target_id_set_sha256") != digest:
        fail("target ID-set digest mismatch")
    if scope.get("covered_targets") != 1546 or scope.get("excluded_mathematics_records") != 55:
        fail("manifest scope counts are stale")
    if any(target.get("theorem_complete") is not False for target in targets):
        fail("generated intake manifest must set theorem_complete=false for every target")
    if any(
        target.get("baseline") != "L0"
        or target.get("rework_required") is not True
        or target.get("legacy_artifacts_accepted") is not False
        or "assurance_level" in target
        or "priority_slot" in target
        for target in targets
    ):
        fail("every target must use the uniform L0 rework baseline")
    return targets


def command_check(targets: list[dict[str, Any]]) -> None:
    l0 = sum(target.get("baseline") == "L0" for target in targets)
    if l0 != 1546:
        fail(f"uniform baseline count is stale: L0={l0}")
    print("stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)")


def command_show(targets: list[dict[str, Any]], theorem_id: str) -> None:
    target = next((item for item in targets if item.get("theorem_id") == theorem_id), None)
    if target is None:
        fail(f"{theorem_id} is not covered by Stage1 rev-5.6")
    print(json.dumps(target, ensure_ascii=False, indent=2))


def command_next(targets: list[dict[str, Any]], start_rank: int, limit: int) -> None:
    matches = [target for target in targets if target.get("execution_rank", 0) >= start_rank]
    for target in matches[:limit]:
        print(
            f"{target['execution_rank']:04d}\t{target['theorem_id']}\t"
            f"{target['baseline']}\t{target['target_lane']}\t{target['name']}"
        )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subparsers = result.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check", help="verify target count, ordering, digest, and assurance totals")
    show = subparsers.add_parser("show", help="print one covered target as JSON")
    show.add_argument("theorem_id")
    next_parser = subparsers.add_parser("next", help="list targets from an execution rank")
    next_parser.add_argument("--from-rank", type=int, default=1)
    next_parser.add_argument("--limit", type=int, default=20)
    return result


def main() -> None:
    args = parser().parse_args()
    if getattr(args, "limit", 1) < 1 or getattr(args, "from_rank", 1) < 1:
        fail("--limit and --from-rank must be positive")
    targets = checked_targets(load_manifest())
    if args.command == "check":
        command_check(targets)
    elif args.command == "show":
        command_show(targets, args.theorem_id)
    elif args.command == "next":
        command_next(targets, args.from_rank, args.limit)
    else:
        fail(f"unsupported command: {args.command}")


if __name__ == "__main__":
    main()
