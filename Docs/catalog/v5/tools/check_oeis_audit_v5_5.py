#!/usr/bin/env python3
"""Independently replay the repository-owned OEIS v5.5 candidate audit."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile
from typing import Any, Iterable


DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_DIR = PurePosixPath("Docs/catalog/v5/sources")
CURATION_DIR = PurePosixPath("Docs/catalog/v5/curation/oeis_v5_5")
PARENT_DIR = PurePosixPath("Docs/catalog/v5/releases/5.4")
HISTORICAL_PARENT_DIR = PurePosixPath("Docs/catalog/v5/releases/5.3")
TOOLS_DIR = PurePosixPath("Docs/catalog/v5/tools")
CURRENT_RELEASE = PurePosixPath("Docs/catalog/v5/Current_Release.json")

SOURCE_ARCHIVE = SOURCE_DIR / "oeis-conjectures-4c866362-source.tar.gz"
V1_SOURCE = SOURCE_DIR / "oeis-conjectures-4c866362-candidates.jsonl"
V2_SOURCE = SOURCE_DIR / "oeis-conjectures-4c866362-all-conjectur-v2.jsonl"
SOURCE_RECEIPT = SOURCE_DIR / "oeis-conjectures-4c866362-receipt.json"
AUDIT_RECEIPT = CURATION_DIR / "audit-receipt.json"
COMBINED = CURATION_DIR / "combined-survivors.jsonl"
V1_LEGACY = CURATION_DIR / "v1/legacy-candidates.jsonl"
V1_AUDIT = CURATION_DIR / "v1/cross-dedupe-audit.json"
V1_INTERNAL = CURATION_DIR / "v1/internal-semantic-dedupe.json"
V1_SUPPLEMENT = CURATION_DIR / "v1/internal-semantic-dedupe-tier-supplement.json"
V1_PARENT_A = CURATION_DIR / "v1/parent-match-a.json"
V1_PARENT_B = CURATION_DIR / "v1/parent-match-b.json"
V2_MASTER = CURATION_DIR / "v2/source-v2-only-499.jsonl"
V2_ANNOTATIONS = CURATION_DIR / "v2/manual-annotations.json"
V2_AUDIT = CURATION_DIR / "v2/consolidation-audit.json"
V2_SURVIVORS = CURATION_DIR / "v2/survivors.jsonl"

PARENT_FILES = {
    "claim_catalog": PARENT_DIR / "Claim_Catalog.json",
    "claim_id_registry": PARENT_DIR / "Claim_ID_Registry.json",
    "coverage_ledger": PARENT_DIR / "Coverage_Ledger.json",
    "migration_v4_to_v5": PARENT_DIR / "Migration_v4_to_v5.json",
    "open_claim_list": PARENT_DIR / "Open_Claim_List.json",
    "release_manifest": PARENT_DIR / "Release_Manifest.json",
    "stage5_claim_id_registry": PARENT_DIR / "Stage5_Claim_ID_Registry.json",
    "strict_ledger": PARENT_DIR / "Strict_Conjecture_Ledger.json",
    "theorem_list": PARENT_DIR / "Theorem_List.json",
}
PARENT_ROWS: dict[str, int | None] = {
    "claim_catalog": 4100,
    "claim_id_registry": 7584,
    "coverage_ledger": 5961,
    "migration_v4_to_v5": 7584,
    "open_claim_list": 1600,
    "release_manifest": None,
    "stage5_claim_id_registry": 7584,
    "strict_ledger": 1001,
    "theorem_list": 2500,
}
HISTORICAL_PARENT_FILES = {
    "claim_catalog": HISTORICAL_PARENT_DIR / "Claim_Catalog.json",
    "strict_ledger": HISTORICAL_PARENT_DIR / "Strict_Conjecture_Ledger.json",
}
TOOL_FILES = {
    "migration": TOOLS_DIR / "migrate_oeis_audit_v5_5.py",
    "checker": TOOLS_DIR / "check_oeis_audit_v5_5.py",
}
EXTRACTOR_FILES = {
    "v1_extractor": PurePosixPath("Docs/tools/extract_oeis_conjectures_v5.py"),
    "v2_extractor": PurePosixPath("Docs/tools/extract_oeis_conjectures_v5_v2.py"),
}

# This is deliberately repeated here instead of imported from the migration
# utility: the checker must retain an independent, closed inventory contract.
EXPECTED_ARTIFACT_ROWS: dict[str, int | None] = {
    "combined-survivors.jsonl": 268,
    "v1/legacy-candidates.jsonl": 602,
    **{f"v1/batches/batch-{index:02d}.jsonl": 76 if index < 7 else 70
       for index in range(8)},
    **{f"v1/reviews/review-{index:02d}.jsonl": 76 if index < 7 else 70
       for index in range(8)},
    "v1/cross-dedupe-audit.json": None,
    "v1/internal-semantic-dedupe.json": None,
    "v1/internal-semantic-dedupe-tier-supplement.json": None,
    "v1/parent-match-a.json": None,
    "v1/parent-match-b.json": None,
    "v1/support/parent-match-retrieval.jsonl": 420,
    "v1/support/parent-strict-compact.tsv": None,
    "v1/support/accepted-compact.tsv": None,
    "v2/source-v2-only-499.jsonl": 499,
    **{f"v2/batches/batch-{index:02d}.jsonl": 63 if index < 7 else 58
       for index in range(8)},
    **{f"v2/reviews/review-v2-{index:02d}.jsonl": 63 if index < 7 else 58
       for index in range(8)},
    "v2/manual-annotations.json": None,
    "v2/consolidation-audit.json": None,
    "v2/survivors.jsonl": 69,
}

FIXED_SHA256 = {
    SOURCE_ARCHIVE.as_posix(): "85ac265ad3c7ab294a18a3874e33a139fa9afdba8b6dfba86ea03aefd7ab3a1e",
    V1_SOURCE.as_posix(): "7b426d78bcbd05389e129553ba2030690fd5b5309666a9819db0c6f9ae1cf3b3",
    V2_SOURCE.as_posix(): "18da1f5881f0410f2c38dc8362271b536db11c4509d58812942a11981181ec3d",
    (PARENT_DIR / "Claim_Catalog.json").as_posix(): "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709",
    (PARENT_DIR / "Claim_ID_Registry.json").as_posix(): "0c8047aaa05800e5ec3a004cfdb628a163c4c18e3dfb4905ac5635787dde9dc5",
    (PARENT_DIR / "Coverage_Ledger.json").as_posix(): "af1735648fd758b8cde367cc5a5beb5f5f4adc649fb50c763a9c4c0655eb001e",
    (PARENT_DIR / "Migration_v4_to_v5.json").as_posix(): "50be591db91ba6e610c2234f1e60e6b4a7448b1d6e9fdd385b7dac2a9685b875",
    (PARENT_DIR / "Open_Claim_List.json").as_posix(): "aa8acc2cfe859b7ce108863e51b69da6cbe9f5ab63a0b908ba7b811d82a165b4",
    (PARENT_DIR / "Release_Manifest.json").as_posix(): "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9",
    (PARENT_DIR / "Stage5_Claim_ID_Registry.json").as_posix(): "2c66b9220401db2372c9c92335f857e6c51dcc06cf4f0a1407f2e7332de74314",
    (PARENT_DIR / "Strict_Conjecture_Ledger.json").as_posix(): "52ba1ccf06462741bcc48028fb121e5e30d1e7b56128cfeb910dc56a2e1a83a3",
    (PARENT_DIR / "Theorem_List.json").as_posix(): "238644155db7e5941b0b5f95f7244aa695e8ba2ea9d0659bd8a6d111ce860784",
    (HISTORICAL_PARENT_DIR / "Claim_Catalog.json").as_posix(): "957da23fbd1e50244912fb6dbb76fbf663e7970ace3f6da8b19407929211a8bb",
    (HISTORICAL_PARENT_DIR / "Strict_Conjecture_Ledger.json").as_posix(): "91106334947a4406b75f7e87b400dd9966e25fb0441b6b78eb1047b4bb5a88dc",
    CURRENT_RELEASE.as_posix(): "261f27d39f379a879ea0fcacbab9e3c43dc5be8d83ea56473b2e8b4e6c384795",
}
V1_KEY_ORDER_SHA256 = "814a921549ccee4ffd03005959499cf111f96faebcd64386f88486514819c9c8"
V2_KEY_ORDER_SHA256 = "62301fa5b0a172c35c96d536241c14f0c6d95696881d65610107eae04c2b3be0"
COMBINED_KEY_ORDER_SHA256 = "9acf0f6ef66b5188d6e50e9a052f68248b81f832cde102cc5f7e5b4c195a63c1"
V1_KEY_TIER_ORDER_SHA256 = "9eee76f0f0c5c052422a2538f58d03946cb8fd72beef10ab3dc80aefcb1806ee"
V2_KEY_TIER_ORDER_SHA256 = "947d69e22d84bed371318f0391d88b8e3de4b5dacf4c660f9ecbe08fc0f151ef"
COMBINED_KEY_TIER_ORDER_SHA256 = "b74772b58282a939a55116411d6a2fc53bcd910cd807fd3fb8f315f047708bf4"

ARCHIVE_ROOT = "oeis-conjectures-4c866362-source"
PINNED_COMMIT = "4c8663620c66525a0c92654a4a9c4703b3d98921"
PINNED_TREE = "7e0ed547bdc22e34ec578307fed26572bbd58b1e"
README_SHA256 = "68138ef6cb982ff6029579b4e1a1407ad80d08fcaece8d2fbf40092d04a1baaa"
PAX_HEADERS = {
    "awesome-theorems.source_id": "SRC-MATH-V5-OEIS-4C866362",
    "awesome-theorems.repository": "https://github.com/oeis/oeisdata",
    "awesome-theorems.commit": PINNED_COMMIT,
    "awesome-theorems.commit_timestamp": "2026-08-10T03:05:07-04:00",
    "awesome-theorems.tree_sha1": PINNED_TREE,
    "awesome-theorems.export_time": "2026-08-10T03:00:14-04:00",
    "awesome-theorems.license_spdx": "CC-BY-SA-4.0",
}

FIELD_RE = re.compile(r"^%([A-Za-z])\s+(A[0-9]{6})\s?(.*)$")
SEQ_RE = re.compile(r"^seq/(A[0-9]{3})/(A[0-9]{6})\.seq$")
HTML_RE = re.compile(r"<[^>]*>")
V1_MARKER_RE = re.compile(
    r"(?:we\s+conjecture|i\s+conjecture|conjectures?\s+that|"
    r"it\s+is\s+conjectured|is\s+conjectured\s+to|"
    r"are\s+conjectured\s+to|the\s+conjecture\s+is)", re.IGNORECASE,
)
RESOLUTION_RE = re.compile(
    r"(?:proved|disproved|refuted|counterexample|resolved|settled|"
    r"is\s+false|was\s+false|no\s+longer\s+open)", re.IGNORECASE,
)
V2_MARKER_RE = re.compile(r"conjectur", re.IGNORECASE | re.ASCII)
KEY_RE = re.compile(r"^oeis-normalized/[0-9a-f]{64}$")
REVIEW_FIELDS = {
    "candidate_key", "decision", "reason_code", "exact_claim_text", "a_numbers",
    "truth_apt", "context_complete", "source_asserted_open_as_of_commit",
    "importance_tier", "importance_basis", "semantic_summary", "possible_duplicate_keys",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def require_true(value: Any, message: str) -> None:
    require(type(value) is bool and value is True, message)


def require_false(value: Any, message: str) -> None:
    require(type(value) is bool and value is False, message)


def require_zero(value: Any, message: str) -> None:
    require(type(value) is int and value == 0, message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_blob_sha1(value: bytes) -> str:
    return hashlib.sha1(f"blob {len(value)}\0".encode("ascii") + value).hexdigest()


def key_order_sha256(keys: Iterable[str]) -> str:
    return sha256_bytes(("\n".join(keys) + "\n").encode("utf-8"))


def key_tier_order_sha256(rows: Iterable[tuple[str, str]]) -> str:
    return sha256_bytes("".join(f"{key}\t{tier}\n" for key, tier in rows).encode("utf-8"))


def safe_repo_file(repo_root: Path, relative: PurePosixPath | str, label: str) -> Path:
    raw = relative.as_posix() if isinstance(relative, PurePosixPath) else relative
    require(isinstance(raw, str) and raw and "\\" not in raw,
            f"{label}: invalid repository path")
    rel = PurePosixPath(raw)
    require(not rel.is_absolute() and ".." not in rel.parts and rel.as_posix() == raw,
            f"{label}: absolute, escaping, or noncanonical repository path")
    lexical = repo_root.joinpath(*rel.parts)
    try:
        resolved = lexical.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"{label}: missing repository file {raw}") from exc
    try:
        resolved.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(f"{label}: path escapes repository root") from exc
    require(resolved == lexical, f"{label}: symlinked repository path is not allowed")
    require(resolved.is_file(), f"{label}: not a regular file")
    return resolved


def strict_json_loads(payload: str | bytes, label: str) -> Any:
    def object_from_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"{label}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    def reject_constant(value: str) -> None:
        raise ValueError(f"{label}: non-finite JSON number {value}")

    return json.loads(
        payload,
        object_pairs_hook=object_from_pairs,
        parse_constant=reject_constant,
    )


def load_json(path: Path, label: str) -> dict[str, Any]:
    value = strict_json_loads(path.read_text(encoding="utf-8"), label)
    require(isinstance(value, dict), f"{label}: JSON is not an object")
    return value


def load_jsonl(path: Path, label: str) -> list[dict[str, Any]]:
    raw = path.read_bytes()
    require(raw.endswith(b"\n"), f"{label}: missing final newline")
    output = []
    for number, line in enumerate(raw.splitlines(), 1):
        require(bool(line.strip()), f"{label}:{number}: blank row")
        value = strict_json_loads(line, f"{label}:{number}")
        require(isinstance(value, dict), f"{label}:{number}: row is not an object")
        output.append(value)
    return output


def expected_binding(path: Path, repo_root: Path, rows: int | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "path": path.relative_to(repo_root).as_posix(),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }
    if rows is not None:
        value["rows"] = rows
    return value


def validate_binding(
    value: Any, path: Path, repo_root: Path, label: str, rows: int | None = None,
) -> None:
    require(value == expected_binding(path, repo_root, rows), f"{label}: binding mismatch")
    safe_repo_file(repo_root, value["path"], label)


def validate_nested_binding(
    value: Any,
    relative: PurePosixPath,
    path: Path,
    repo_root: Path,
    label: str,
    *,
    rows: int | None = None,
    rows_key: str = "rows",
) -> None:
    require(isinstance(value, dict), f"{label}: nested binding is not an object")
    require(value.get("path") == relative.as_posix(), f"{label}: nested path mismatch")
    require(value.get("sha256") == sha256_file(path), f"{label}: nested SHA-256 mismatch")
    if rows is not None:
        require(value.get(rows_key) == rows, f"{label}: nested row count mismatch")
    if "size_bytes" in value:
        require(value.get("size_bytes") == path.stat().st_size,
                f"{label}: nested size mismatch")
    safe_repo_file(repo_root, relative, label)


def require_no_ephemeral_strings(value: Any, label: str) -> None:
    if isinstance(value, str):
        require(value not in {"/tmp", "/home"}
                and "/tmp/" not in value and "/home/" not in value and "file://" not in value,
                f"{label}: ephemeral absolute provenance path leaked")
    elif isinstance(value, list):
        for item in value:
            require_no_ephemeral_strings(item, label)
    elif isinstance(value, dict):
        for key, item in value.items():
            require_no_ephemeral_strings(key, label)
            require_no_ephemeral_strings(item, label)


def normalize_text(text: str) -> str:
    value = HTML_RE.sub("", text)
    value = "".join(chr(ord(char) + 32) if "A" <= char <= "Z" else char for char in value)
    value = "".join(char if char.isalnum() else " " for char in value)
    return " ".join(value.split())


def safe_tar_name(name: str) -> str:
    require(isinstance(name, str) and name and "\\" not in name and "\x00" not in name,
            "unsafe OEIS archive member name")
    parts = name.split("/")
    require(not name.startswith("/") and not name.endswith("/")
            and all(part not in {"", ".", ".."} for part in parts),
            f"unsafe OEIS archive member path {name!r}")
    prefix = ARCHIVE_ROOT + "/"
    require(name.startswith(prefix), f"OEIS archive member outside root {name!r}")
    return name[len(prefix):]


def replay_source(archive_path: Path) -> tuple[dict[tuple[str, int], dict[str, Any]], list[str], list[str]]:
    require(sha256_file(archive_path) == FIXED_SHA256[SOURCE_ARCHIVE.as_posix()],
            "frozen OEIS source archive SHA-256 changed")
    files: dict[str, bytes] = {}
    with tarfile.open(archive_path, "r:gz") as archive:
        require(dict(archive.pax_headers) == PAX_HEADERS, "OEIS archive PAX provenance changed")
        members = archive.getmembers()
        require(len(members) == 624, "OEIS archive member count changed")
        for member in members:
            relative = safe_tar_name(member.name)
            require(member.isfile() and not member.issym() and not member.islnk(),
                    f"OEIS archive member is not regular: {member.name}")
            require(relative not in files, f"duplicate OEIS archive member: {relative}")
            require({key: member.pax_headers.get(key) for key in PAX_HEADERS} == PAX_HEADERS,
                    f"OEIS archive member provenance changed: {relative}")
            handle = archive.extractfile(member)
            require(handle is not None, f"unreadable OEIS archive member: {relative}")
            data = handle.read()
            require(len(data) == member.size, f"OEIS archive member size mismatch: {relative}")
            files[relative] = data
    require(set(files).issuperset({"README.md", "time.txt"}), "OEIS license/time evidence missing")
    require(sha256_bytes(files["README.md"]) == README_SHA256, "OEIS README license evidence drift")
    require("Creative Commons Attribution Share Alike 4.0 license"
            in files["README.md"].decode("utf-8"), "OEIS license text missing")
    require(files["time.txt"].decode("utf-8").strip() == "2026-08-10T03:00:14-04:00",
            "OEIS export time changed")

    source_lines: dict[tuple[str, int], dict[str, Any]] = {}
    v1_normalized: list[str] = []
    v2_normalized: list[str] = []
    marker_count = resolution_count = v2_occurrences = 0
    seq_count = 0
    for relative, data in sorted(files.items()):
        if relative in {"README.md", "time.txt"}:
            continue
        match = SEQ_RE.fullmatch(relative)
        require(match is not None and match.group(1) == match.group(2)[:4],
                f"invalid OEIS sequence member path: {relative}")
        a_number = match.group(2)
        seq_count += 1
        text = data.decode("utf-8")
        require("\r" not in text, f"noncanonical CR in {relative}")
        file_sha = sha256_bytes(data)
        blob_sha = git_blob_sha1(data)
        seen_name = False
        for number, line in enumerate(text.splitlines(), 1):
            if not line:
                continue
            field_match = FIELD_RE.fullmatch(line)
            require(field_match is not None and field_match.group(2) == a_number,
                    f"invalid OEIS field line {relative}:{number}")
            field = "%" + field_match.group(1).upper()
            value = field_match.group(3)
            seen_name |= field == "%N"
            source_lines[(relative, number)] = {
                "a_number": a_number, "field": field, "original_text": value,
                "file_sha256": file_sha, "blob_sha1": blob_sha,
            }
            if field not in {"%N", "%C", "%F"}:
                continue
            if V1_MARKER_RE.search(value):
                marker_count += 1
                if RESOLUTION_RE.search(value):
                    resolution_count += 1
                else:
                    v1_normalized.append(normalize_text(value))
            if V2_MARKER_RE.search(value):
                v2_occurrences += 1
                v2_normalized.append(normalize_text(value))
        require(seen_name, f"OEIS sequence lacks %N field: {relative}")
    require(seq_count == 622, "OEIS sequence-entry count changed")
    require((marker_count, resolution_count, len(v1_normalized), v2_occurrences)
            == (665, 39, 626, 1141), "OEIS source discovery counts changed")
    v1_keys = [f"oeis-normalized/{sha256_bytes(value.encode())}"
               for value in sorted(set(v1_normalized))]
    v2_keys = [f"oeis-normalized/{sha256_bytes(value.encode())}"
               for value in sorted(set(v2_normalized))]
    require(len(v1_keys) == 602 and len(v2_keys) == 1101,
            "OEIS independently reconstructed candidate counts changed")
    return source_lines, v1_keys, v2_keys


def validate_source_rows(
    rows: list[dict[str, Any]], expected_keys: list[str], source_lines: dict[tuple[str, int], dict[str, Any]],
    label: str,
) -> dict[str, dict[str, Any]]:
    keys = [row.get("candidate_key") for row in rows]
    require(keys == expected_keys, f"{label}: candidate key coverage/order differs from source replay")
    result: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows, 1):
        key = row["candidate_key"]
        normalized = row.get("normalized_text")
        require(isinstance(normalized, str) and key == f"oeis-normalized/{sha256_bytes(normalized.encode())}",
                f"{label} {index}: normalized candidate key mismatch")
        require_true(row.get("candidate_only"), f"{label} {index}: candidate-only boundary missing")
        require_false(row.get("grants_catalog_entry"), f"{label} {index}: catalog credit granted")
        require_false(row.get("grants_strict_conjecture_credit"),
                      f"{label} {index}: strict credit granted")
        require(row.get("license_spdx") == "CC-BY-SA-4.0", f"{label} {index}: license changed")
        locations = row.get("locations")
        require(isinstance(locations, list) and locations,
                f"{label} {index}: source locations missing")
        require(row.get("occurrence_count") == len(locations)
                and row.get("a_number_count") == len({item.get("a_number") for item in locations}),
                f"{label} {index}: occurrence/A-number counts mismatch")
        for location in locations:
            path = location.get("path")
            line_number = location.get("line_number")
            require(isinstance(path, str) and type(line_number) is int,
                    f"{label} {index}: malformed source location")
            source = source_lines.get((path, line_number))
            require(source is not None, f"{label} {index}: source location absent from archive")
            for field in ("a_number", "field", "original_text", "file_sha256", "blob_sha1"):
                require(location.get(field) == source[field],
                        f"{label} {index}: frozen source {field} mismatch")
            require(normalize_text(source["original_text"]) == normalized,
                    f"{label} {index}: normalized text differs from frozen source")
        result[key] = row
    require(len(result) == len(rows), f"{label}: duplicate candidate key")
    return result


def validate_reviews(
    reviews: list[dict[str, Any]], source_rows: list[dict[str, Any]], label: str,
) -> tuple[dict[str, dict[str, Any]], Counter[str], Counter[str]]:
    require(len(reviews) == len(source_rows), f"{label}: review coverage count mismatch")
    require([row.get("candidate_key") for row in reviews]
            == [row.get("candidate_key") for row in source_rows],
            f"{label}: review key order differs from candidate batches")
    review_map: dict[str, dict[str, Any]] = {}
    decisions: Counter[str] = Counter()
    tiers: Counter[str] = Counter()
    for index, (review, source) in enumerate(zip(reviews, source_rows), 1):
        require(set(review) == REVIEW_FIELDS, f"{label} {index}: review field set changed")
        key = review.get("candidate_key")
        require(isinstance(key, str) and KEY_RE.fullmatch(key), f"{label} {index}: malformed key")
        require(review.get("a_numbers") == sorted({loc["a_number"] for loc in source["locations"]}),
                f"{label} {index}: reviewed A-number set differs from source")
        decision = review.get("decision")
        require(decision in {"accept", "reject"}, f"{label} {index}: invalid decision")
        require(isinstance(review.get("reason_code"), str) and review["reason_code"],
                f"{label} {index}: missing reason")
        require(isinstance(review.get("importance_basis"), str) and review["importance_basis"],
                f"{label} {index}: missing importance basis")
        require(isinstance(review.get("semantic_summary"), str) and review["semantic_summary"],
                f"{label} {index}: missing semantic summary")
        require(isinstance(review.get("possible_duplicate_keys"), list),
                f"{label} {index}: duplicate hints are not a list")
        if decision == "accept":
            require(review.get("importance_tier") in {"high", "medium", "low"},
                    f"{label} {index}: accepted tier invalid")
            for field in ("truth_apt", "context_complete", "source_asserted_open_as_of_commit"):
                require_true(review.get(field), f"{label} {index}: accepted gate {field} is not true")
            require(isinstance(review.get("exact_claim_text"), str) and review["exact_claim_text"],
                    f"{label} {index}: accepted exact claim missing")
            tiers[review["importance_tier"]] += 1
        else:
            require(review.get("exact_claim_text") is None,
                    f"{label} {index}: rejected row carries exact claim")
            require(review.get("importance_tier") in {"none", "low"},
                    f"{label} {index}: rejected tier invalid")
        decisions[decision] += 1
        review_map[key] = review
    require(len(review_map) == len(reviews), f"{label}: duplicate review key")
    return review_map, decisions, tiers


def literal_claim(review: dict[str, Any], source: dict[str, Any]) -> bool:
    claim = review.get("exact_claim_text")
    return isinstance(claim, str) and any(claim in loc["original_text"] for loc in source["locations"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=DEFAULT_REPO_ROOT)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve(strict=True)
    require(repo_root.is_dir(), "repository root is not a directory")

    required_relatives = [
        SOURCE_ARCHIVE, V1_SOURCE, V2_SOURCE, SOURCE_RECEIPT, AUDIT_RECEIPT, COMBINED,
        V1_LEGACY, V1_AUDIT, V1_INTERNAL, V1_SUPPLEMENT, V1_PARENT_A, V1_PARENT_B,
        V2_MASTER, V2_ANNOTATIONS, V2_AUDIT, V2_SURVIVORS,
        *PARENT_FILES.values(), *HISTORICAL_PARENT_FILES.values(), CURRENT_RELEASE,
        *TOOL_FILES.values(), *EXTRACTOR_FILES.values(),
        *[CURATION_DIR / name for name in EXPECTED_ARTIFACT_ROWS],
        *[CURATION_DIR / f"v1/batches/batch-{index:02d}.jsonl" for index in range(8)],
        *[CURATION_DIR / f"v1/reviews/review-{index:02d}.jsonl" for index in range(8)],
        *[CURATION_DIR / f"v2/batches/batch-{index:02d}.jsonl" for index in range(8)],
        *[CURATION_DIR / f"v2/reviews/review-v2-{index:02d}.jsonl" for index in range(8)],
        CURATION_DIR / "v1/support/parent-match-retrieval.jsonl",
        CURATION_DIR / "v1/support/parent-strict-compact.tsv",
        CURATION_DIR / "v1/support/accepted-compact.tsv",
    ]
    paths = {relative.as_posix(): safe_repo_file(repo_root, relative, relative.name)
             for relative in required_relatives}
    curation_root = repo_root.joinpath(*CURATION_DIR.parts).resolve(strict=True)
    require(curation_root.is_dir(), "OEIS curation root is not a directory")
    try:
        curation_root.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError("OEIS curation root escapes repository root") from exc
    actual_curation_files = {
        path.relative_to(curation_root).as_posix()
        for path in curation_root.rglob("*")
        if path.is_file()
    }
    require(actual_curation_files == set(EXPECTED_ARTIFACT_ROWS) | {"audit-receipt.json"},
            "OEIS curation directory has missing or unsealed extra files")
    for relative, expected in FIXED_SHA256.items():
        require(sha256_file(paths[relative]) == expected, f"pinned input drift: {relative}")

    source_lines, replay_v1_keys, replay_v2_keys = replay_source(paths[SOURCE_ARCHIVE.as_posix()])
    v1_source_rows = load_jsonl(paths[V1_SOURCE.as_posix()], "v1 source candidates")
    v2_source_rows = load_jsonl(paths[V2_SOURCE.as_posix()], "v2 source candidates")
    v1_source_map = validate_source_rows(
        v1_source_rows, replay_v1_keys, source_lines, "v1 source candidate",
    )
    v2_source_map = validate_source_rows(
        v2_source_rows, replay_v2_keys, source_lines, "v2 source candidate",
    )
    require(set(v1_source_map).issubset(v2_source_map), "v1 candidate keys are not a v2 subset")
    require(len(set(v2_source_map) - set(v1_source_map)) == 499, "v2-only key count changed")

    v1_legacy_rows = load_jsonl(paths[V1_LEGACY.as_posix()], "v1 legacy candidates")
    require([row.get("candidate_key") for row in v1_legacy_rows] == replay_v1_keys,
            "v1 legacy candidate coverage/order changed")
    v1_batch_rows: list[dict[str, Any]] = []
    v1_review_rows: list[dict[str, Any]] = []
    v1_batch_groups: list[list[dict[str, Any]]] = []
    v1_review_groups: list[list[dict[str, Any]]] = []
    for index in range(8):
        batch_group = load_jsonl(
            paths[(CURATION_DIR / f"v1/batches/batch-{index:02d}.jsonl").as_posix()],
            f"v1 batch {index:02d}",
        )
        review_group = load_jsonl(
            paths[(CURATION_DIR / f"v1/reviews/review-{index:02d}.jsonl").as_posix()],
            f"v1 review {index:02d}",
        )
        v1_batch_groups.append(batch_group)
        v1_review_groups.append(review_group)
        v1_batch_rows.extend(batch_group)
        v1_review_rows.extend(review_group)
    require(v1_batch_rows == v1_legacy_rows, "v1 candidate batches do not reconstruct legacy source")
    for legacy, rich in zip(v1_legacy_rows, v1_source_rows):
        require(legacy.get("candidate_key") == rich.get("candidate_key")
                and legacy.get("normalized_text") == rich.get("normalized_text")
                and legacy.get("locations") == rich.get("locations"),
                "v1 legacy source does not join exactly to frozen repository source")
    v1_reviews, v1_decisions, v1_tiers = validate_reviews(
        v1_review_rows, v1_batch_rows, "v1 review",
    )
    require(v1_decisions == {"accept": 420, "reject": 182}
            and v1_tiers == {"high": 66, "medium": 201, "low": 153},
            "v1 provisional review counts changed")

    v1_internal = load_json(paths[V1_INTERNAL.as_posix()], "v1 internal semantic audit")
    require(v1_internal.get("schema_version") == "oeis-accepted-internal-semantic-audit-v1",
            "v1 internal semantic audit schema changed")
    internal_scope = v1_internal.get("scope", {})
    require(internal_scope.get("candidate_file") == V1_LEGACY.as_posix()
            and internal_scope.get("candidate_file_sha256") == sha256_file(
                paths[V1_LEGACY.as_posix()]
            ), "v1 internal audit candidate binding changed")
    internal_review_refs = internal_scope.get("review_files")
    require(isinstance(internal_review_refs, list) and len(internal_review_refs) == 8,
            "v1 internal audit review inventory changed")
    for index, (reference, rows) in enumerate(zip(internal_review_refs, v1_review_groups)):
        relative = CURATION_DIR / f"v1/reviews/review-{index:02d}.jsonl"
        require(set(reference) == {"path", "row_count", "sha256"},
                f"v1 internal review {index:02d}: field set changed")
        validate_nested_binding(
            reference, relative, paths[relative.as_posix()], repo_root,
            f"v1 internal review {index:02d}", rows=len(rows), rows_key="row_count",
        )
    require(internal_scope.get("physical_review_row_count") == 602
            and internal_scope.get("physical_accepted_row_count") == 420
            and internal_scope.get("unique_accepted_candidate_key_count") == 420
            and internal_scope.get("physical_duplicate_accepted_candidate_keys") == {},
            "v1 internal audit scope counts changed")

    v1_supplement = load_json(paths[V1_SUPPLEMENT.as_posix()], "v1 tier supplement")
    require(v1_supplement.get("schema_version")
            == "oeis-internal-semantic-dedupe-tier-supplement-v1",
            "v1 tier supplement schema changed")
    require(set(v1_supplement.get("source_audit", {})) == {"path", "sha256"},
            "v1 tier supplement source binding fields changed")
    validate_nested_binding(
        v1_supplement.get("source_audit"), V1_INTERNAL, paths[V1_INTERNAL.as_posix()],
        repo_root, "v1 tier supplement source audit",
    )

    parent_match_documents: dict[str, dict[str, Any]] = {}
    for label, relative, selected in (
        ("a", V1_PARENT_A, range(0, 3)),
        ("b", V1_PARENT_B, range(3, 8)),
    ):
        document = load_json(paths[relative.as_posix()], f"v1 parent match {label}")
        parent_match_documents[label] = document
        require(document.get("schema_version") == "oeis-parent-semantic-match-audit/1.0",
                f"v1 parent match {label}: schema changed")
        scope = document.get("scope", {})
        review_refs = scope.get("review_files")
        selected_indexes = list(selected)
        require(isinstance(review_refs, list) and len(review_refs) == len(selected_indexes),
                f"v1 parent match {label}: review inventory changed")
        accepted_scope = 0
        accepted_tiers: Counter[str] = Counter()
        for reference, index in zip(review_refs, selected_indexes):
            rows = v1_review_groups[index]
            relative_review = CURATION_DIR / f"v1/reviews/review-{index:02d}.jsonl"
            accepted = sum(row["decision"] == "accept" for row in rows)
            accepted_scope += accepted
            accepted_tiers.update(
                row["importance_tier"] for row in rows if row["decision"] == "accept"
            )
            require(set(reference) == {"accepted", "path", "rows", "sha256"}
                    and reference.get("accepted") == accepted,
                    f"v1 parent match {label}: review metadata changed")
            validate_nested_binding(
                reference, relative_review, paths[relative_review.as_posix()], repo_root,
                f"v1 parent match {label} review {index:02d}", rows=len(rows),
            )
        require(scope.get("parent_release") == "5.3"
                and scope.get("parent_strict_credit_count") == 1000
                and scope.get("accepted_scope_count") == accepted_scope
                and scope.get("accepted_tier_counts") == dict(accepted_tiers),
                f"v1 parent match {label}: scope counts changed")
        inputs = document.get("inputs", {})
        expected_input_keys = {
            "claim_catalog", "parent_match_retrieval", "parent_strict_compact",
            "strict_ledger",
        } | ({"accepted_compact"} if label == "a" else set())
        require(set(inputs) == expected_input_keys,
                f"v1 parent match {label}: input inventory changed")
        require(inputs.get("claim_catalog")
                == HISTORICAL_PARENT_FILES["claim_catalog"].as_posix()
                and inputs.get("strict_ledger")
                == HISTORICAL_PARENT_FILES["strict_ledger"].as_posix(),
                f"v1 parent match {label}: historical parent path changed")
        support_inputs = {
            "parent_match_retrieval": CURATION_DIR / "v1/support/parent-match-retrieval.jsonl",
            "parent_strict_compact": CURATION_DIR / "v1/support/parent-strict-compact.tsv",
        }
        if label == "a":
            support_inputs["accepted_compact"] = (
                CURATION_DIR / "v1/support/accepted-compact.tsv"
            )
        for name, support_relative in support_inputs.items():
            require(set(inputs.get(name, {})) == {"path", "sha256"},
                    f"v1 parent match {label}: {name} binding fields changed")
            validate_nested_binding(
                inputs.get(name), support_relative, paths[support_relative.as_posix()],
                repo_root, f"v1 parent match {label}: {name}",
            )

    v2_master_rows = load_jsonl(paths[V2_MASTER.as_posix()], "v2-only master")
    expected_v2_only = [row for row in v2_source_rows if row["candidate_key"] not in v1_source_map]
    require(v2_master_rows == expected_v2_only, "v2-only master is not exact frozen-source projection")
    v2_batch_rows: list[dict[str, Any]] = []
    v2_review_rows: list[dict[str, Any]] = []
    v2_batch_groups: list[list[dict[str, Any]]] = []
    v2_review_groups: list[list[dict[str, Any]]] = []
    v2_review_file_sha: dict[str, str] = {}
    for index in range(8):
        batch_group = load_jsonl(
            paths[(CURATION_DIR / f"v2/batches/batch-{index:02d}.jsonl").as_posix()],
            f"v2 batch {index:02d}",
        )
        v2_batch_groups.append(batch_group)
        v2_batch_rows.extend(batch_group)
        review_path = paths[
            (CURATION_DIR / f"v2/reviews/review-v2-{index:02d}.jsonl").as_posix()
        ]
        review_rows = load_jsonl(review_path, f"v2 review {index:02d}")
        v2_review_groups.append(review_rows)
        v2_review_rows.extend(review_rows)
        review_sha = sha256_file(review_path)
        for row in review_rows:
            require(row.get("candidate_key") not in v2_review_file_sha,
                    "v2 review hash map has duplicate candidate key")
            v2_review_file_sha[row["candidate_key"]] = review_sha
    require(v2_batch_rows == v2_master_rows, "v2 batches do not reconstruct v2-only master")
    v2_reviews, v2_decisions, v2_tiers = validate_reviews(
        v2_review_rows, v2_batch_rows, "v2 review",
    )
    require(v2_decisions == {"accept": 89, "reject": 410}
            and v2_tiers == {"high": 35, "medium": 54},
            "v2 review counts changed")

    parent_catalog = load_json(paths[(PARENT_DIR / "Claim_Catalog.json").as_posix()], "parent catalog")
    parent_open = load_json(paths[(PARENT_DIR / "Open_Claim_List.json").as_posix()], "parent open list")
    parent_theorems = load_json(paths[(PARENT_DIR / "Theorem_List.json").as_posix()], "parent theorem list")
    parent_ledger = load_json(paths[(PARENT_DIR / "Strict_Conjecture_Ledger.json").as_posix()], "parent strict ledger")
    parent_manifest = load_json(paths[(PARENT_DIR / "Release_Manifest.json").as_posix()], "parent manifest")
    require(parent_manifest.get("release") == "5.4" and parent_manifest.get("counts", {}) == {
        "catalog_records": 4100, "cumulative_open_claims": 1600,
        "cumulative_theorems": 2500, "effective_strict_conjecture_credits": 1000,
        "non_manifest_artifacts": 8, "origin_open_claims": 0, "origin_theorems": 500,
    }, "parent 5.4 manifest/counts changed")
    manifest_artifact_names = [
        "Claim_Catalog.json", "Claim_ID_Registry.json", "Coverage_Ledger.json",
        "Migration_v4_to_v5.json", "Open_Claim_List.json",
        "Stage5_Claim_ID_Registry.json", "Strict_Conjecture_Ledger.json",
        "Theorem_List.json",
    ]
    manifest_artifacts = parent_manifest.get("artifacts")
    require(isinstance(manifest_artifacts, list)
            and [row.get("path") for row in manifest_artifacts] == manifest_artifact_names,
            "parent 5.4 manifest artifact inventory changed")
    expected_manifest_rows = {
        relative.name: PARENT_ROWS[name]
        for name, relative in PARENT_FILES.items()
        if name != "release_manifest"
    }
    for row in manifest_artifacts:
        relative = PARENT_DIR / row["path"]
        path = paths[relative.as_posix()]
        require(row == {
            "path": relative.name,
            "row_count": expected_manifest_rows[relative.name],
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        }, f"parent 5.4 manifest binding changed: {relative.name}")
    current_release = load_json(paths[CURRENT_RELEASE.as_posix()], "current release pointer")
    require(current_release.get("release") == "5.4"
            and current_release.get("manifest_path") == "releases/5.4/Release_Manifest.json"
            and current_release.get("manifest_sha256") == sha256_file(
                paths[(PARENT_DIR / "Release_Manifest.json").as_posix()]
            ), "current release pointer no longer authenticates 5.4")
    parent_records = parent_catalog.get("records")
    require(isinstance(parent_records, list) and len(parent_records) == 4100,
            "parent 5.4 catalog count changed")
    parent_by_id = {row.get("stage_claim_id"): row for row in parent_records}
    require(len(parent_by_id) == 4100, "parent 5.4 IDs are not unique")
    open_ids = set(parent_open.get("stage_claim_ids", []))
    theorem_ids = set(parent_theorems.get("stage_claim_ids", []))
    strict_ids = {row.get("stage_claim_id") for row in parent_ledger.get("strict_credits", [])}
    require(len(open_ids) == 1600 and len(theorem_ids) == 2500 and len(strict_ids) == 1000,
            "parent 5.4 partition counts changed")
    require(open_ids | theorem_ids == set(parent_by_id) and not (open_ids & theorem_ids),
            "parent 5.4 open/proved partition changed")
    require(strict_ids.issubset(open_ids), "parent strict IDs are not an open subset")

    v1_audit = load_json(paths[V1_AUDIT.as_posix()], "v1 final audit")
    require(v1_audit.get("schema_version") == "oeis-cross-dedupe-audit-v2-final",
            "v1 audit schema changed")
    require_true(v1_audit.get("audit_integrity_pass"), "v1 audit integrity flag is not true")
    cross_inputs = v1_audit.get("inputs", {})
    require(set(cross_inputs) == {
        "batch_files", "candidate_file", "internal_semantic_dedupe",
        "internal_tier_supplement", "parent_catalog", "parent_ledger",
        "parent_match_a", "parent_match_b", "parent_match_retrieval",
        "parent_strict_compact", "review_files",
    }, "v1 final audit input inventory changed")
    require(set(cross_inputs.get("candidate_file", {})) == {"path", "rows", "sha256"},
            "v1 final audit candidate binding fields changed")
    validate_nested_binding(
        cross_inputs.get("candidate_file"), V1_LEGACY, paths[V1_LEGACY.as_posix()],
        repo_root, "v1 final audit candidate file", rows=602,
    )
    batch_refs = cross_inputs.get("batch_files")
    review_refs = cross_inputs.get("review_files")
    require(isinstance(batch_refs, list) and len(batch_refs) == 8
            and isinstance(review_refs, list) and len(review_refs) == 8,
            "v1 final audit batch/review inventory changed")
    for index in range(8):
        batch_relative = CURATION_DIR / f"v1/batches/batch-{index:02d}.jsonl"
        review_relative = CURATION_DIR / f"v1/reviews/review-{index:02d}.jsonl"
        require(set(batch_refs[index]) == {"path", "rows", "sha256"},
                f"v1 final audit batch {index:02d}: fields changed")
        validate_nested_binding(
            batch_refs[index], batch_relative, paths[batch_relative.as_posix()], repo_root,
            f"v1 final audit batch {index:02d}", rows=len(v1_batch_groups[index]),
        )
        decisions = Counter(row["decision"] for row in v1_review_groups[index])
        require(set(review_refs[index]) == {
            "accepted", "path", "rejected", "rows", "sha256",
        } and review_refs[index].get("accepted") == decisions["accept"]
            and review_refs[index].get("rejected") == decisions["reject"],
            f"v1 final audit review {index:02d}: metadata changed")
        validate_nested_binding(
            review_refs[index], review_relative, paths[review_relative.as_posix()], repo_root,
            f"v1 final audit review {index:02d}", rows=len(v1_review_groups[index]),
        )
    cross_single_inputs = {
        "internal_semantic_dedupe": V1_INTERNAL,
        "internal_tier_supplement": V1_SUPPLEMENT,
        "parent_match_a": V1_PARENT_A,
        "parent_match_b": V1_PARENT_B,
        "parent_match_retrieval": CURATION_DIR / "v1/support/parent-match-retrieval.jsonl",
        "parent_strict_compact": CURATION_DIR / "v1/support/parent-strict-compact.tsv",
        "parent_catalog": HISTORICAL_PARENT_FILES["claim_catalog"],
        "parent_ledger": HISTORICAL_PARENT_FILES["strict_ledger"],
    }
    for name, relative in cross_single_inputs.items():
        require(set(cross_inputs.get(name, {})) == {"path", "sha256"},
                f"v1 final audit {name}: binding fields changed")
        validate_nested_binding(
            cross_inputs.get(name), relative, paths[relative.as_posix()], repo_root,
            f"v1 final audit {name}",
        )
    v1_survivor_keys = v1_audit.get("high_medium_survivor_keys")
    require(isinstance(v1_survivor_keys, list) and len(v1_survivor_keys) == 199
            and len(set(v1_survivor_keys)) == 199,
            "v1 survivor key coverage changed")
    require(key_order_sha256(v1_survivor_keys) == V1_KEY_ORDER_SHA256,
            "v1 authoritative survivor identity/order changed")
    require(v1_audit.get("high_medium_survivor_count") == 199
            and v1_audit.get("high_medium_survivor_tier_counts") == {"high": 41, "medium": 158},
            "v1 survivor count/tier declaration changed")
    all_tier_rows = v1_audit.get("all_tier_survivors")
    require(isinstance(all_tier_rows, list) and len(all_tier_rows) == 329,
            "v1 all-tier survivor rows changed")
    require(all(set(row) == {
        "candidate_key", "a_numbers", "importance_tier", "semantic_summary",
    } for row in all_tier_rows), "v1 all-tier survivor field set changed")
    all_tier_keys = [row.get("candidate_key") for row in all_tier_rows]
    require(len(set(all_tier_keys)) == 329
            and all_tier_keys == v1_audit.get("all_tier_survivor_keys")
            and v1_audit.get("all_tier_survivor_count") == 329,
            "v1 all-tier survivor identity/order changed")
    require(Counter(row.get("importance_tier") for row in all_tier_rows)
            == v1_audit.get("all_tier_survivor_tier_counts")
            == {"high": 41, "medium": 158, "low": 130},
            "v1 all-tier survivor tier counts changed")
    require([row["candidate_key"] for row in all_tier_rows
             if row["importance_tier"] in {"high", "medium"}] == v1_survivor_keys,
            "v1 high/medium projection differs from all-tier survivors")
    all_tier = {row["candidate_key"]: row for row in all_tier_rows}
    for key in v1_survivor_keys:
        require(key in v1_reviews and key in v1_source_map and key in all_tier,
                "v1 survivor does not join review/source/final projection")
        review = v1_reviews[key]
        final = all_tier[key]
        require(review["decision"] == "accept" and review["importance_tier"] in {"high", "medium"},
                "v1 survivor is not an accepted high/medium review")
        require(literal_claim(review, v1_source_map[key]),
                "v1 survivor exact claim is not a literal frozen source substring")
        require(final.get("importance_tier") == review["importance_tier"]
                and final.get("semantic_summary") == review["semantic_summary"]
                and final.get("a_numbers") == review["a_numbers"],
                "v1 survivor projection differs from review")
    require(key_tier_order_sha256(
        (key, all_tier[key]["importance_tier"]) for key in v1_survivor_keys
    ) == V1_KEY_TIER_ORDER_SHA256, "v1 authoritative survivor tier assignment changed")
    require(v1_audit.get("selection_threshold_met") is False
            and v1_audit.get("at_least_401") is False,
            "v1 audit threshold result changed")

    annotations = load_json(paths[V2_ANNOTATIONS.as_posix()], "v2 manual annotations")
    require(set(annotations) == {
        "schema_version", "review_boundary", "remove", "reviewed_retain_keys",
    } and annotations.get("schema_version")
        == "oeis-v2-consolidation-manual-annotations-v1",
            "v2 manual annotation schema/field inventory changed")
    review_boundary = annotations.get("review_boundary", {})
    require_true(review_boundary.get("pending_batches_must_be_annotated_after_arrival"),
                 "v2 manual annotation pending-batch gate changed")
    require_true(review_boundary.get("no_target_count_used"),
                 "v2 manual annotation target-count boundary changed")
    remove_rows = annotations.get("remove")
    retain_keys = annotations.get("reviewed_retain_keys")
    require(isinstance(remove_rows, list) and len(remove_rows) == 20,
            "v2 manual removal count changed")
    require(isinstance(retain_keys, list) and len(retain_keys) == 69
            and len(set(retain_keys)) == 69, "v2 manual retain set changed")
    high_medium_pool = [
        row["candidate_key"] for row in v2_review_rows
        if row["decision"] == "accept" and row["importance_tier"] in {"high", "medium"}
    ]
    remove_keys = [row.get("candidate_key") for row in remove_rows]
    require(len(set(remove_keys)) == 20 and not (set(remove_keys) & set(retain_keys)),
            "v2 manual remove/retain partition overlaps or duplicates")
    require(set(remove_keys) | set(retain_keys) == set(high_medium_pool),
            "v2 manual annotations do not partition all 89 high/medium accepts")
    allowed_reasons = {
        "non_atomic_grouped_referents", "semantic_duplicate_parent_5_4_strict",
        "semantic_duplicate_parent_5_4_broad_open_non_strict",
        "semantic_duplicate_parent_5_4_proved_or_status_exclusion",
        "semantic_duplicate_v1", "semantic_duplicate_v2", "subsumed_by_v1",
        "subsumed_by_v2", "subsumed_by_parent_5_4",
    }
    for row in remove_rows:
        require(set(row) == {"candidate_key", "reason_code", "target_keys", "basis", "reviewer"},
                "v2 manual removal field set changed")
        require(row.get("reason_code") in allowed_reasons,
                "v2 manual annotation reason is outside closed vocabulary")
        require(isinstance(row.get("basis"), str) and row["basis"],
                "v2 manual annotation basis missing")
        require(isinstance(row.get("reviewer"), str) and row["reviewer"],
                "v2 manual annotation reviewer missing")
        targets = row.get("target_keys")
        require(isinstance(targets, list), "v2 manual annotation targets malformed")
        for target in targets:
            if isinstance(target, str) and target.startswith("S5-CLM-"):
                require(target in parent_by_id, "v2 annotation references unknown parent claim")
                reason = row["reason_code"]
                if reason == "semantic_duplicate_parent_5_4_strict":
                    require(target in strict_ids, "v2 strict-duplicate target is not parent strict")
                elif reason == "semantic_duplicate_parent_5_4_broad_open_non_strict":
                    require(target in open_ids - strict_ids,
                            "v2 broad-open target is not parent non-strict open")
                elif reason == "semantic_duplicate_parent_5_4_proved_or_status_exclusion":
                    require(target in theorem_ids, "v2 proved target is not parent theorem")
            else:
                require(target in v1_source_map or target in v2_reviews,
                        "v2 annotation references unknown OEIS candidate")

    v2_survivors = load_jsonl(paths[V2_SURVIVORS.as_posix()], "v2 survivors")
    v2_keys = [row.get("candidate_key") for row in v2_survivors]
    require(set(v2_keys) == set(retain_keys)
            and key_order_sha256(v2_keys) == V2_KEY_ORDER_SHA256,
            "v2 authoritative survivor identity/order changed")
    require(not (set(v1_survivor_keys) & set(v2_keys)), "v1/v2 survivor sets overlap")
    v2_tier_counts = Counter(row.get("importance_tier") for row in v2_survivors)
    require(v2_tier_counts == {"high": 18, "medium": 51}, "v2 survivor tier counts changed")
    require(key_tier_order_sha256(
        (row["candidate_key"], row["importance_tier"]) for row in v2_survivors
    ) == V2_KEY_TIER_ORDER_SHA256, "v2 authoritative survivor tier assignment changed")
    expected_v2_fields = {
        "candidate_key", "a_numbers", "importance_tier", "exact_claim_text",
        "semantic_summary", "source_review_sha256",
    }
    for row in v2_survivors:
        key = row["candidate_key"]
        require(set(row) == expected_v2_fields, "v2 survivor field set changed")
        review = v2_reviews.get(key)
        require(review is not None and review["decision"] == "accept"
                and review["importance_tier"] in {"high", "medium"},
                "v2 survivor is not accepted high/medium review")
        require(row["a_numbers"] == review["a_numbers"]
                and row["importance_tier"] == review["importance_tier"]
                and row["exact_claim_text"] == review["exact_claim_text"]
                and row["semantic_summary"] == review["semantic_summary"],
                "v2 survivor projection differs from review")
        require(literal_claim(review, v2_source_map[key]),
                "v2 survivor exact claim is not a literal frozen source substring")
        require(row["source_review_sha256"] == v2_review_file_sha[key],
                "v2 survivor review hash binding mismatch")

    v2_audit = load_json(paths[V2_AUDIT.as_posix()], "v2 consolidation audit")
    require(v2_audit.get("schema_version") == "oeis-v2-consolidation-audit-v2"
            and v2_audit.get("audit_state") == "final_ready"
            and v2_audit.get("final_ready") is True, "v2 final-ready state changed")
    v2_inputs = v2_audit.get("inputs", {})
    require(set(v2_inputs) == {
        "available_reviews", "consolidator", "git_head", "manual_annotations",
        "parent_5_4", "release_path_git_status", "repo", "v1_final_audit",
        "v2_batch_inputs", "v2_master", "workspace",
    }, "v2 audit input inventory changed")
    require(v2_inputs.get("repo") == "."
            and v2_inputs.get("workspace") == CURATION_DIR.as_posix()
            and v2_inputs.get("git_head") == "9c299dbabd34878a420db46ca66d687886fe2b04"
            and v2_inputs.get("release_path_git_status")
            == "?? Docs/catalog/v5/releases/5.4/",
            "v2 audit repository/workspace boundary changed")
    available_review_refs = v2_inputs.get("available_reviews")
    batch_input_refs = v2_inputs.get("v2_batch_inputs")
    require(isinstance(available_review_refs, list) and len(available_review_refs) == 8
            and isinstance(batch_input_refs, list) and len(batch_input_refs) == 8,
            "v2 audit review/batch input inventory changed")
    for index in range(8):
        review_relative = CURATION_DIR / f"v2/reviews/review-v2-{index:02d}.jsonl"
        batch_relative = CURATION_DIR / f"v2/batches/batch-{index:02d}.jsonl"
        reviews = v2_review_groups[index]
        accepted = sum(row["decision"] == "accept" for row in reviews)
        high_medium = sum(
            row["decision"] == "accept" and row["importance_tier"] in {"high", "medium"}
            for row in reviews
        )
        reference = available_review_refs[index]
        require(set(reference) == {
            "accepted", "batch", "high_medium_accepted", "path", "rows", "sha256",
            "validation_errors",
        } and reference.get("batch") == f"{index:02d}"
            and reference.get("accepted") == accepted
            and reference.get("high_medium_accepted") == high_medium
            and reference.get("validation_errors") == 0,
            f"v2 audit review {index:02d}: metadata changed")
        validate_nested_binding(
            reference, review_relative, paths[review_relative.as_posix()], repo_root,
            f"v2 audit review {index:02d}", rows=len(reviews),
        )
        batch_reference = batch_input_refs[index]
        require(set(batch_reference) == {"batch", "path", "rows", "sha256"}
                and batch_reference.get("batch") == f"{index:02d}",
                f"v2 audit batch {index:02d}: metadata changed")
        validate_nested_binding(
            batch_reference, batch_relative, paths[batch_relative.as_posix()], repo_root,
            f"v2 audit batch {index:02d}", rows=len(v2_batch_groups[index]),
        )
    require(set(v2_inputs.get("v2_master", {})) == {"path", "rows", "sha256"},
            "v2 audit master binding fields changed")
    validate_nested_binding(
        v2_inputs.get("v2_master"), V2_MASTER, paths[V2_MASTER.as_posix()], repo_root,
        "v2 audit master", rows=499,
    )
    for name, relative in (
        ("manual_annotations", V2_ANNOTATIONS),
        ("v1_final_audit", V1_AUDIT),
    ):
        require(set(v2_inputs.get(name, {})) == {"path", "sha256"},
                f"v2 audit {name}: binding fields changed")
        validate_nested_binding(
            v2_inputs.get(name), relative, paths[relative.as_posix()], repo_root,
            f"v2 audit {name}",
        )
    consolidator = v2_inputs.get("consolidator", {})
    require(set(consolidator) == {
        "historical_generator_sha256", "path", "role", "sha256", "size_bytes",
    } and consolidator.get("historical_generator_sha256")
        == "de94c4759d49817014989a2c6cab799bedadbc1c5ae85fbb531234a867b8fc22"
        and consolidator.get("role")
        == "repository migration and receipt sealing; final validity is replayed by the independent checker",
            "v2 audit consolidator provenance changed")
    validate_nested_binding(
        consolidator, TOOL_FILES["migration"], paths[TOOL_FILES["migration"].as_posix()],
        repo_root, "v2 audit consolidator",
    )
    parent_input_map = {
        "catalog": "claim_catalog", "manifest": "release_manifest",
        "open_claim_list": "open_claim_list", "strict_ledger": "strict_ledger",
        "theorem_list": "theorem_list",
    }
    parent_inputs = v2_inputs.get("parent_5_4", {})
    require(set(parent_inputs) == set(parent_input_map),
            "v2 audit parent 5.4 input inventory changed")
    for input_name, parent_name in parent_input_map.items():
        relative = PARENT_FILES[parent_name]
        require(set(parent_inputs.get(input_name, {})) == {"path", "sha256"},
                f"v2 audit parent {input_name}: binding fields changed")
        validate_nested_binding(
            parent_inputs.get(input_name), relative, paths[relative.as_posix()], repo_root,
            f"v2 audit parent {input_name}",
        )
    require(v2_audit.get("coverage", {}).get("full_499_coverage_pass") is True
            and v2_audit.get("coverage", {}).get("pending_candidate_count") == 0,
            "v2 review coverage gate changed")
    layers = v2_audit.get("v2_layers", {})
    require(layers.get("high_medium_accept_pool", {}).get("candidate_keys") == high_medium_pool,
            "v2 audit high/medium pool differs from reviews")
    require(layers.get("manual_exclusion_count") == 20
            and layers.get("adjudicated_survivor_count") == 69
            and layers.get("adjudicated_survivor_tier_counts") == {"high": 18, "medium": 51}
            and layers.get("combined_v1_plus_adjudicated_v2_count") == 268,
            "v2 adjudication counts changed")
    dedupe = v2_audit.get("dedupe", {})
    dedupe_remove_keys = [
        row.get("candidate_key") for row in dedupe.get("manual_exclusions", [])
    ]
    require(dedupe.get("adjudicated_survivor_keys") == v2_keys
            and len(dedupe_remove_keys) == len(set(dedupe_remove_keys)) == 20
            and set(dedupe_remove_keys) == set(remove_keys),
            "v2 dedupe projection differs from survivors/manual annotations")
    gate = v2_audit.get("final_gate", {})
    require_true(gate.get("candidate_audit_only"), "v2 audit candidate-only boundary changed")
    require_true(gate.get("ready"), "v2 final gate not ready")
    require_false(gate.get("release_published"), "v2 audit claims release publication")
    require_zero(gate.get("formal_release_additions_counted"),
                 "v2 audit counts formal release additions")

    combined = load_jsonl(paths[COMBINED.as_posix()], "combined survivors")
    combined_keys = [row.get("candidate_key") for row in combined]
    require(len(combined) == 268 and combined_keys == [*v1_survivor_keys, *v2_keys]
            and key_order_sha256(combined_keys) == COMBINED_KEY_ORDER_SHA256,
            "combined authoritative survivor identity/order changed")
    expected_combined = []
    for key in v1_survivor_keys:
        row = all_tier[key]
        expected_combined.append({
            "candidate_key": key, "a_numbers": row["a_numbers"],
            "importance_tier": row["importance_tier"],
            "semantic_summary": row["semantic_summary"],
            "audit_layer": "v1_narrow_marker", "candidate_only": True,
            "grants_catalog_entry": False, "grants_strict_conjecture_credit": False,
        })
    expected_combined.extend({
        **row, "audit_layer": "v2_literal_stem_extension", "candidate_only": True,
        "grants_catalog_entry": False, "grants_strict_conjecture_credit": False,
    } for row in v2_survivors)
    require(combined == expected_combined, "combined survivor projection differs from v1/v2 audits")
    require(Counter(row["importance_tier"] for row in combined) == {"high": 59, "medium": 209},
            "combined survivor tier counts changed")
    require(key_tier_order_sha256(
        (row["candidate_key"], row["importance_tier"]) for row in combined
    ) == COMBINED_KEY_TIER_ORDER_SHA256,
            "combined authoritative survivor tier assignment changed")

    source_receipt = load_json(paths[SOURCE_RECEIPT.as_posix()], "OEIS source receipt")
    require(set(source_receipt) == {
        "schema_version", "artifact", "source", "artifacts", "extractors", "counts",
        "candidate_only", "grants_catalog_entry", "grants_strict_conjecture_credit",
    }, "OEIS source receipt field inventory changed")
    require(source_receipt.get("schema_version") == "awesome-theorems/oeis-frozen-source-receipt/5.5",
            "OEIS source receipt schema changed")
    require(source_receipt.get("artifact") == SOURCE_RECEIPT.as_posix(),
            "OEIS source receipt path changed")
    require(source_receipt.get("source") == {
        "repository": "https://github.com/oeis/oeisdata",
        "commit": PINNED_COMMIT,
        "tree_sha1": PINNED_TREE,
        "license_spdx": "CC-BY-SA-4.0",
    }, "OEIS source receipt provenance changed")
    require(source_receipt.get("counts") == {
        "frozen_sequence_entries": 622, "v1_candidate_rows": 602,
        "v2_candidate_rows": 1101, "v2_only_candidate_rows": 499,
    }, "OEIS source receipt counts changed")
    require_true(source_receipt.get("candidate_only"), "OEIS source receipt candidate boundary missing")
    require_false(source_receipt.get("grants_catalog_entry"), "OEIS source receipt grants catalog entry")
    require_false(source_receipt.get("grants_strict_conjecture_credit"),
                  "OEIS source receipt grants strict credit")
    source_artifacts = source_receipt.get("artifacts", {})
    require(set(source_artifacts) == {"source_archive", "v1_candidates", "v2_candidates"},
            "OEIS source receipt artifact inventory changed")
    validate_binding(source_artifacts.get("source_archive"), paths[SOURCE_ARCHIVE.as_posix()], repo_root,
                     "source receipt archive")
    validate_binding(source_artifacts.get("v1_candidates"), paths[V1_SOURCE.as_posix()], repo_root,
                     "source receipt v1 candidates", 602)
    validate_binding(source_artifacts.get("v2_candidates"), paths[V2_SOURCE.as_posix()], repo_root,
                     "source receipt v2 candidates", 1101)
    source_extractors = source_receipt.get("extractors", {})
    require(set(source_extractors) == set(EXTRACTOR_FILES),
            "OEIS source receipt extractor inventory changed")
    for name, relative in EXTRACTOR_FILES.items():
        validate_binding(source_extractors.get(name), paths[relative.as_posix()], repo_root,
                         f"source receipt extractor {name}")

    receipt = load_json(paths[AUDIT_RECEIPT.as_posix()], "OEIS audit receipt")
    require(set(receipt) == {
        "schema_version", "artifact", "audit_date", "source", "parent_release_5_4",
        "publication_boundary", "artifacts", "counts", "candidate_only",
        "formal_release_modified", "release_published", "tools",
    }, "OEIS audit receipt field inventory changed")
    require(receipt.get("schema_version") == "awesome-theorems/oeis-candidate-audit-receipt/5.5",
            "OEIS audit receipt schema changed")
    require(receipt.get("artifact") == AUDIT_RECEIPT.as_posix(),
            "OEIS audit receipt path changed")
    require(receipt.get("audit_date") == "2026-08-10", "OEIS audit date changed")
    require(receipt.get("counts") == {
        "v1_candidates_reviewed": 602, "v1_high_survivors": 41,
        "v1_medium_survivors": 158, "v1_high_medium_survivors": 199,
        "v2_only_candidates_reviewed": 499, "v2_high_survivors": 18,
        "v2_medium_survivors": 51, "v2_high_medium_survivors": 69,
        "combined_candidate_survivors": 268, "formal_release_additions": 0,
        "strict_credits_granted": 0,
    }, "OEIS audit receipt counts changed")
    require_true(receipt.get("candidate_only"), "OEIS audit candidate-only boundary missing")
    require_false(receipt.get("formal_release_modified"), "OEIS audit claims release modification")
    require_false(receipt.get("release_published"), "OEIS audit claims release publication")
    require_zero(receipt["counts"].get("formal_release_additions"),
                 "OEIS audit formal-addition count not integer zero")
    require_zero(receipt["counts"].get("strict_credits_granted"),
                 "OEIS audit strict-credit count not integer zero")

    receipt_source = receipt.get("source", {})
    require(set(receipt_source) == {
        "source_archive", "v1_candidates", "v2_candidates", "source_receipt",
    }, "OEIS audit receipt source inventory changed")
    validate_binding(receipt_source.get("source_archive"), paths[SOURCE_ARCHIVE.as_posix()], repo_root,
                     "audit receipt source archive")
    validate_binding(receipt_source.get("v1_candidates"), paths[V1_SOURCE.as_posix()], repo_root,
                     "audit receipt v1 source", 602)
    validate_binding(receipt_source.get("v2_candidates"), paths[V2_SOURCE.as_posix()], repo_root,
                     "audit receipt v2 source", 1101)
    validate_binding(receipt_source.get("source_receipt"), paths[SOURCE_RECEIPT.as_posix()], repo_root,
                     "audit receipt source receipt")
    receipt_parent = receipt.get("parent_release_5_4", {})
    require(set(receipt_parent) == set(PARENT_FILES),
            "OEIS audit receipt parent inventory changed")
    for name, relative in PARENT_FILES.items():
        validate_binding(receipt_parent.get(name), paths[relative.as_posix()], repo_root,
                         f"audit receipt parent {name}", PARENT_ROWS[name])
    publication_boundary = receipt.get("publication_boundary", {})
    require(set(publication_boundary) == {"current_release"},
            "OEIS audit publication-boundary inventory changed")
    validate_binding(
        publication_boundary.get("current_release"), paths[CURRENT_RELEASE.as_posix()],
        repo_root, "audit receipt current release boundary",
    )
    artifacts = receipt.get("artifacts", {})
    require(set(artifacts) == set(EXPECTED_ARTIFACT_ROWS),
            "OEIS audit receipt artifact inventory changed")
    for name, expected_rows in EXPECTED_ARTIFACT_ROWS.items():
        artifact_path = paths[(CURATION_DIR / name).as_posix()]
        if expected_rows is not None:
            require(len(load_jsonl(artifact_path, f"audit artifact {name}")) == expected_rows,
                    f"audit artifact {name}: actual JSONL row count changed")
        validate_binding(artifacts.get(name), artifact_path, repo_root,
                         f"audit artifact {name}", expected_rows)
    tools = receipt.get("tools", {})
    require(set(tools) == set(TOOL_FILES), "OEIS audit tool inventory changed")
    for name, relative in TOOL_FILES.items():
        validate_binding(tools.get(name), paths[relative.as_posix()], repo_root,
                         f"audit tool {name}")

    for name in [*EXPECTED_ARTIFACT_ROWS, "audit-receipt.json"]:
        relative = CURATION_DIR / name
        path = paths[relative.as_posix()]
        if path.suffix == ".json":
            require_no_ephemeral_strings(load_json(path, f"provenance {name}"), name)
        elif path.suffix == ".jsonl":
            require_no_ephemeral_strings(load_jsonl(path, f"provenance {name}"), name)
        else:
            require_no_ephemeral_strings(path.read_text(encoding="utf-8"), name)
    require_no_ephemeral_strings(source_receipt, "OEIS source receipt")

    print(
        "PASS independent OEIS audit check: source=622 v1=199 "
        "v2=69 combined=268 formal_additions=0 strict_credit=0"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL independent OEIS audit check: {exc}", file=sys.stderr)
        raise SystemExit(1)
