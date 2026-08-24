#!/usr/bin/env python3
"""Pin the Erdős Problems status database used by theorem/conjecture review.

The asset is metadata evidence, not a theorem or conjecture inventory credit.
It deliberately preserves every upstream row so independent checkers can join
problem numbers and detect status drift without trusting a filtered export.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import tarfile
from typing import Any, Mapping

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ARCHIVE = REPO_ROOT / "Docs/catalog/v5/sources/erdosproblems-af90db96-source.tar.gz"
DEFAULT_OUTPUT = REPO_ROOT / "Docs/catalog/v5/sources/erdosproblems-status-af90db96.json"
PINNED_COMMIT = "af90db960021ff3247f0374e015dae97b5125ff6"
PINNED_TREE = "931fc5b8a230485d49f095b59bbd30e6a0466455"
PINNED_COMMIT_TIMESTAMP = "2026-08-09T21:27:45+00:00"
PINNED_ARCHIVE_SHA256 = "a9125786b0ccf2da2c5411b0eb9c80f6b2cd2717d140606e136314e76bc0be58"
PINNED_PROBLEMS_SHA256 = "14007c54a9ad0a9560966bd782f3303db898c6387df02754219dc585ef8b989d"
PINNED_LICENSE_SHA256 = "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"
HEX64 = re.compile(r"[0-9a-f]{64}")


class PinError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def encoded(value: Mapping[str, Any]) -> bytes:
    return canonical(value) + b"\n"


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    ignored = set(fields)
    return digest_bytes(canonical({key: item for key, item in value.items() if key not in ignored}))


def normalized_status(value: Any, *, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PinError(f"{field} must be an object")
    state = value.get("state")
    if not isinstance(state, str) or not state.strip():
        raise PinError(f"{field}.state must be nonempty")
    result: dict[str, Any] = {"state": state.strip()}
    last_update = value.get("last_update")
    if last_update is not None:
        text = last_update.isoformat() if hasattr(last_update, "isoformat") else str(last_update)
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", text):
            raise PinError(f"invalid {field}.last_update: {text}")
        result["last_update"] = text
    return result


def archive_members(archive: Path) -> dict[str, bytes]:
    if digest_file(archive) != PINNED_ARCHIVE_SHA256:
        raise PinError("Erdős Problems archive digest drifted")
    result: dict[str, bytes] = {}
    with tarfile.open(archive, "r:gz") as stream:
        names = [member.name for member in stream.getmembers()]
        if names != ["LICENSE", "data", "data/problems.yaml"]:
            raise PinError(f"unexpected archive member inventory: {names}")
        for member in stream.getmembers():
            if member.isdir():
                continue
            if not member.isfile() or member.name.startswith("/") or ".." in Path(member.name).parts:
                raise PinError(f"unsafe archive member: {member.name}")
            extracted = stream.extractfile(member)
            if extracted is None:
                raise PinError(f"cannot read archive member: {member.name}")
            result[member.name] = extracted.read()
    return result


def build(archive: Path) -> dict[str, Any]:
    members = archive_members(archive)
    problems_bytes = members["data/problems.yaml"]
    license_bytes = members["LICENSE"]
    if digest_bytes(problems_bytes) != PINNED_PROBLEMS_SHA256:
        raise PinError("problems.yaml digest drifted")
    if digest_bytes(license_bytes) != PINNED_LICENSE_SHA256:
        raise PinError("LICENSE digest drifted")
    raw = yaml.safe_load(problems_bytes.decode("utf-8"))
    if not isinstance(raw, list):
        raise PinError("problems.yaml must be a list")

    records: list[dict[str, Any]] = []
    seen: set[int] = set()
    for source_index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise PinError(f"problem row {source_index} is not an object")
        try:
            number = int(item["number"])
        except (KeyError, TypeError, ValueError) as error:
            raise PinError(f"invalid problem number at row {source_index}") from error
        if number <= 0 or number in seen:
            raise PinError(f"duplicate/nonpositive problem number {number}")
        seen.add(number)
        tags = item.get("tags", [])
        oeis = item.get("oeis", [])
        if not isinstance(tags, list) or not all(isinstance(value, str) and value for value in tags):
            raise PinError(f"malformed tags for problem {number}")
        if not isinstance(oeis, list) or not all(isinstance(value, str) and value for value in oeis):
            raise PinError(f"malformed OEIS references for problem {number}")
        oeis_a_numbers = sorted({value for value in oeis if re.fullmatch(r"A[0-9]{6}", value)})
        record: dict[str, Any] = {
            "problem_number": number,
            "source_index": source_index,
            "status": normalized_status(item.get("status"), field=f"{number}.status"),
            "informal_status": normalized_status(item.get("informal_status"), field=f"{number}.informal_status"),
            "formal_status": normalized_status(item.get("formal_status"), field=f"{number}.formal_status"),
            "formalized": normalized_status(item.get("formalized"), field=f"{number}.formalized"),
            "prize": item.get("prize"),
            "tags": tags,
            "oeis_raw": oeis,
            "oeis_a_numbers": oeis_a_numbers,
            "upstream_page": f"https://www.erdosproblems.com/{number}",
        }
        record["row_sha256"] = hash_without(record, "row_sha256")
        records.append(record)
    records.sort(key=lambda row: int(row["problem_number"]))
    if len(records) != 1_217:
        raise PinError(f"expected 1217 rows, found {len(records)}")

    result: dict[str, Any] = {
        "schema_version": "awesome-theorems/erdosproblems-status-snapshot/1.0",
        "source": {
            "repository": "https://github.com/teorth/erdosproblems",
            "commit": PINNED_COMMIT,
            "tree": PINNED_TREE,
            "commit_timestamp": PINNED_COMMIT_TIMESTAMP,
            "archive_path": archive.relative_to(REPO_ROOT).as_posix(),
            "archive_sha256": PINNED_ARCHIVE_SHA256,
            "problems_path": "data/problems.yaml",
            "problems_sha256": PINNED_PROBLEMS_SHA256,
            "license_path": "LICENSE",
            "license_sha256": PINNED_LICENSE_SHA256,
            "license": "Apache-2.0",
        },
        "evidence_boundary": {
            "role": "current_status_importance_and_classification_metadata_join",
            "problem_existence_grants_catalog_credit": False,
            "status_metadata_alone_grants_theorem_or_conjecture_credit": False,
            "status_disclaimer": "The upstream website states that open status reflects its owner's current belief and may miss literature; qualifying release rows still require independent status and statement review.",
        },
        "counts": {
            "records": len(records),
            "by_status": dict(sorted(__import__("collections").Counter(row["status"]["state"] for row in records).items())),
            "records_with_prize": sum(row["prize"] not in (None, "", "no") for row in records),
            "records_with_oeis_a_number": sum(bool(row["oeis_a_numbers"]) for row in records),
            "records_with_oeis_metadata": sum(bool(row["oeis_raw"]) for row in records),
        },
        "set_digests": {
            "problem_number_set_sha256": digest_bytes(canonical(sorted(seen))),
            "row_sha256_set_sha256": digest_bytes(canonical(sorted(row["row_sha256"] for row in records))),
        },
        "records": records,
    }
    result["authority_sha256"] = hash_without(result, "authority_sha256")
    if not HEX64.fullmatch(result["authority_sha256"]):
        raise PinError("invalid authority digest")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    document = build(args.archive.resolve())
    payload = encoded(document)
    if args.check:
        if not args.output.is_file() or args.output.read_bytes() != payload:
            raise PinError(f"missing or stale snapshot: {args.output}")
        print(f"PASS Erdős status snapshot rows={len(document['records'])} authority={document['authority_sha256']}")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    print(f"wrote {args.output} rows={len(document['records'])} authority={document['authority_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
