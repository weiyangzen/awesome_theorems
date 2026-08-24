#!/usr/bin/env python3
"""Independent checker for the pinned Erdős Problems status snapshot."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import tarfile
from typing import Any, Mapping

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_ARCHIVE = REPO_ROOT / "Docs/catalog/v5/sources/erdosproblems-af90db96-source.tar.gz"
DEFAULT_SNAPSHOT = REPO_ROOT / "Docs/catalog/v5/sources/erdosproblems-status-af90db96.json"
EXPECTED = {
    "archive_sha256": "a9125786b0ccf2da2c5411b0eb9c80f6b2cd2717d140606e136314e76bc0be58",
    "problems_sha256": "14007c54a9ad0a9560966bd782f3303db898c6387df02754219dc585ef8b989d",
    "license_sha256": "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4",
    "commit": "af90db960021ff3247f0374e015dae97b5125ff6",
    "tree": "931fc5b8a230485d49f095b59bbd30e6a0466455",
    "timestamp": "2026-08-09T21:27:45+00:00",
}
HEX64 = re.compile(r"[0-9a-f]{64}")


class CheckError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def without_hash(value: Mapping[str, Any], field: str) -> str:
    return sha(canonical({key: item for key, item in value.items() if key != field}))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def read_archive(path: Path) -> dict[str, bytes]:
    require(path.is_file(), f"missing archive: {path}")
    require(sha_file(path) == EXPECTED["archive_sha256"], "archive digest mismatch")
    output: dict[str, bytes] = {}
    with tarfile.open(path, "r:gz") as stream:
        members = stream.getmembers()
        require([member.name for member in members] == ["LICENSE", "data", "data/problems.yaml"], "archive inventory mismatch")
        for member in members:
            if member.isdir():
                continue
            require(member.isfile(), f"non-file archive member: {member.name}")
            require(not member.name.startswith("/") and ".." not in Path(member.name).parts, f"unsafe archive member: {member.name}")
            handle = stream.extractfile(member)
            require(handle is not None, f"cannot extract {member.name}")
            output[member.name] = handle.read()
    require(sha(output["data/problems.yaml"]) == EXPECTED["problems_sha256"], "raw problem digest mismatch")
    require(sha(output["LICENSE"]) == EXPECTED["license_sha256"], "raw license digest mismatch")
    return output


def status(value: Any, label: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{label} is not an object")
    state = value.get("state")
    require(isinstance(state, str) and bool(state.strip()), f"{label}.state missing")
    result: dict[str, Any] = {"state": state.strip()}
    if value.get("last_update") is not None:
        raw = value["last_update"]
        text = raw.isoformat() if hasattr(raw, "isoformat") else str(raw)
        require(bool(re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", text)), f"{label}.last_update invalid")
        result["last_update"] = text
    return result


def expected_records(raw: Any) -> list[dict[str, Any]]:
    require(isinstance(raw, list) and len(raw) == 1_217, "raw problem cardinality mismatch")
    rows: list[dict[str, Any]] = []
    numbers: set[int] = set()
    for index, item in enumerate(raw):
        require(isinstance(item, dict), f"raw row {index} malformed")
        try:
            number = int(item["number"])
        except (KeyError, TypeError, ValueError) as error:
            raise CheckError(f"raw row {index} has invalid number") from error
        require(number > 0 and number not in numbers, f"duplicate/nonpositive problem number {number}")
        numbers.add(number)
        tags = item.get("tags", [])
        oeis = item.get("oeis", [])
        require(isinstance(tags, list) and all(isinstance(value, str) and value for value in tags), f"problem {number} tags malformed")
        require(isinstance(oeis, list) and all(isinstance(value, str) and value for value in oeis), f"problem {number} OEIS malformed")
        row: dict[str, Any] = {
            "problem_number": number,
            "source_index": index,
            "status": status(item.get("status"), f"{number}.status"),
            "informal_status": status(item.get("informal_status"), f"{number}.informal_status"),
            "formal_status": status(item.get("formal_status"), f"{number}.formal_status"),
            "formalized": status(item.get("formalized"), f"{number}.formalized"),
            "prize": item.get("prize"),
            "tags": tags,
            "oeis_raw": oeis,
            "oeis_a_numbers": sorted({value for value in oeis if re.fullmatch(r"A[0-9]{6}", value)}),
            "upstream_page": f"https://www.erdosproblems.com/{number}",
        }
        row["row_sha256"] = without_hash(row, "row_sha256")
        rows.append(row)
    return sorted(rows, key=lambda row: row["problem_number"])


def check(snapshot_path: Path, archive_path: Path) -> dict[str, Any]:
    members = read_archive(archive_path)
    raw = yaml.safe_load(members["data/problems.yaml"].decode("utf-8"))
    expected_rows = expected_records(raw)
    try:
        document = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CheckError(f"cannot read snapshot: {error}") from error
    require(isinstance(document, dict), "snapshot must be an object")
    require(document.get("schema_version") == "awesome-theorems/erdosproblems-status-snapshot/1.0", "schema version mismatch")
    source = document.get("source")
    require(isinstance(source, dict), "source block missing")
    require(source.get("repository") == "https://github.com/teorth/erdosproblems", "repository mismatch")
    require(source.get("commit") == EXPECTED["commit"] and source.get("tree") == EXPECTED["tree"], "commit/tree mismatch")
    require(source.get("commit_timestamp") == EXPECTED["timestamp"], "commit timestamp mismatch")
    require(source.get("archive_path") == "Docs/catalog/v5/sources/erdosproblems-af90db96-source.tar.gz", "archive path mismatch")
    require(source.get("archive_sha256") == EXPECTED["archive_sha256"], "bound archive digest mismatch")
    require(source.get("problems_sha256") == EXPECTED["problems_sha256"], "bound problems digest mismatch")
    require(source.get("license_sha256") == EXPECTED["license_sha256"] and source.get("license") == "Apache-2.0", "license binding mismatch")
    boundary = document.get("evidence_boundary")
    require(isinstance(boundary, dict), "evidence boundary missing")
    require(boundary.get("problem_existence_grants_catalog_credit") is False, "problem existence grants credit")
    require(boundary.get("status_metadata_alone_grants_theorem_or_conjecture_credit") is False, "status metadata grants credit")
    require(document.get("records") == expected_rows, "normalized record replay mismatch")
    expected_counts = {
        "records": len(expected_rows),
        "by_status": dict(sorted(Counter(row["status"]["state"] for row in expected_rows).items())),
        "records_with_prize": sum(row["prize"] not in (None, "", "no") for row in expected_rows),
        "records_with_oeis_a_number": sum(bool(row["oeis_a_numbers"]) for row in expected_rows),
        "records_with_oeis_metadata": sum(bool(row["oeis_raw"]) for row in expected_rows),
    }
    require(document.get("counts") == expected_counts, "count block mismatch")
    expected_sets = {
        "problem_number_set_sha256": sha(canonical(sorted(row["problem_number"] for row in expected_rows))),
        "row_sha256_set_sha256": sha(canonical(sorted(row["row_sha256"] for row in expected_rows))),
    }
    require(document.get("set_digests") == expected_sets, "set digest mismatch")
    authority = document.get("authority_sha256")
    require(isinstance(authority, str) and bool(HEX64.fullmatch(authority)), "authority malformed")
    require(authority == without_hash(document, "authority_sha256"), "authority mismatch")
    return {"records": len(expected_rows), "authority_sha256": authority}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    args = parser.parse_args()
    result = check(args.snapshot.resolve(), args.archive.resolve())
    print(f"PASS independent Erdős status snapshot records={result['records']} authority={result['authority_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
