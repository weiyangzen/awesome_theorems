#!/usr/bin/env python3
"""Independent, read-only acceptance checker for Stage5 mathematics release 5.5.

The checker intentionally imports no catalog generator.  It authenticates the
5.4 parent, replays JSONL source bindings and review decisions, independently
derives the 1,000 important-theorem and 500--1,000 frontier-theorem sets,
rebuilds every 5.5 append and projection, and verifies the manifest, release
root, Stage6 parent interface, and Current_Release publication boundary.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable, Mapping, Sequence


V5_REL = Path("Docs/catalog/v5")
PARENT_REL = V5_REL / "releases/5.4"
RELEASE_REL = V5_REL / "releases/5.5"
CURRENT_REL = V5_REL / "Current_Release.json"
CURATION_REL = V5_REL / "curation/Strict_Conjecture_Curation_v5_5.json"
IMPORTANT_REL = V5_REL / "curation/theorem_quality_v5_5/mathlib-important-inventory-1000.json"
FRONTIER_REL = V5_REL / "curation/Frontier_Theorem_Qualification_v5_5.json"
FRONTIER_ACCEPTANCE_REL = V5_REL / "curation/Frontier_Theorem_Qualification_Acceptance_v5_5.json"
FRONTIER_SPECIALIZED_CHECKER_REL = V5_REL / "tools/check_frontier_theorem_qualification_v5_5.py"
CONTRACT_REL = V5_REL / "Stage5_Math_Expansion_Contract_v5_5.json"
MATHLIB_SOURCE_REL = V5_REL / "sources/mathlib-theorems-8a178386.json"
MATHLIB_CURATION_RELS = (
    V5_REL / "curation/Mathlib_Theorem_Curation_v5_3.json",
    V5_REL / "curation/Mathlib_Theorem_Curation_v5_4.json",
)
FRONTIER_REVIEW_REL = V5_REL / "curation/frontier_theorem_reviews_v5_5"

RELEASE = "5.5"
PARENT_RELEASE = "5.4"
REVIEW_DATE = "2026-08-10"
PARENT_RELEASE_ROOT = "c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813"
PARENT_MANIFEST_SHA256 = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
PARENT_CATALOG_SHA256 = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
PARENT_STRICT_SHA256 = "52ba1ccf06462741bcc48028fb121e5e30d1e7b56128cfeb910dc56a2e1a83a3"
PARENT_CURRENT_SHA256 = "261f27d39f379a879ea0fcacbab9e3c43dc5be8d83ea56473b2e8b4e6c384795"
MATHLIB_SOURCE_SHA256 = "236b9f6ac192eaf87215663bfd7fadb80c439b452049cef1747ea804c458637a"
MATHLIB_CURATION_SHA256 = (
    "379e165ae52ffd911e383fdb351fc602d36ec585e40bade54612c1512a7a1905",
    "0057a36999422726d6d490dbf59eca69824bc29a02f5117f9a02ebdd601dd386",
)
MATHLIB_COMMIT = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
IMPORTANT_FILE_SHA256 = "a3db9bcd31feb8f2ea4ac07c0b60076446af25b3e4045c2938851440fb974f92"
IMPORTANT_AUTHORITY_SHA256 = "0b4d7c43f91e3c57104665c579fabf7b8a27282b10d95670dea9ccb3bbaf11d2"
FRONTIER_FILE_SHA256 = "7e59381dee0d3364ae4ed75b7128e7fa86085a55141f756de11046f7c036b4b0"
FRONTIER_AUTHORITY_SHA256 = "d221170ac0a23a4134bf19457b124277b779eda0e0ef2180c283720223bac903"
FRONTIER_SPECIALIZED_CHECKER_SHA256 = "3f4b27bd5b67cda31e1cd392c55d928cb5693a14389c5a63829bb9bf8dfae222"
FRONTIER_ACCEPTANCE_FILE_SHA256 = "b602a39d349664d0eb1bbf035062aacb2b0fadebb53f76ef7efc879d88ea1659"
FRONTIER_ACCEPTANCE_AUTHORITY_SHA256 = "304a8404a5a8626a2863f2c98925533ad3b9b70a37820c9c6787bdc37984312d"
FRONTIER_REVIEW_MANIFEST_SHA256 = "b863b7b7a3b50020367afdbc1baab9700cf6c52f6dd27d4078d7360289aa3c1d"
FRONTIER_REVIEW_FILE_SET_SHA256 = "86ad73a13a81f51012df9f302a1682b6da6c74bba7ae0ec00305c8c181dfec8d"
OEIS_SURVIVORS_SHA256 = "d9928d3d61a05e618df7a044c98d966b6f4d8fe63925ea4e95bb2cd5e4de4e5a"
OEIS_SURVIVORS_REL = V5_REL / "curation/oeis_v5_5/combined-survivors.jsonl"
STRICT_CURATION_AUTHORITY_SHA256 = "e3b1bd28502783e4f505f654ed9b46e78b550bd16c409854276cedfcd336a1c0"
PARENT_ATV_HIGH = 7_584
PARENT_ATF_HIGH = 7_354
MIN_NEW_STRICT = 401
MAX_NEW_STRICT = 1_000
BASELINE_5_0_STRICT = 401
MIN_NET_STRICT_AFTER_5_0 = 1_000
MIN_FRONTIER = 500
MAX_FRONTIER = 1_000
IMPORTANT_COUNT = 1_000

RELEASE_FILES = (
    "Claim_Catalog.json",
    "Claim_ID_Registry.json",
    "Stage5_Claim_ID_Registry.json",
    "Migration_v4_to_v5.json",
    "Theorem_List.json",
    "Open_Claim_List.json",
    "Coverage_Ledger.json",
    "Strict_Conjecture_Ledger.json",
)
MANIFEST_NAME = "Release_Manifest.json"
ALL_RELEASE_FILES = frozenset((*RELEASE_FILES, MANIFEST_NAME))

SHA_RE = re.compile(r"^[0-9a-f]{64}$")
S5_RE = re.compile(r"^S5-CLM-([0-9]{8})$")
ATF_RE = re.compile(r"^ATF-([0-9]{8})$")
ATS_RE = re.compile(r"^ATS-([0-9]{8})$")
ATV_RE = re.compile(r"^ATV-([0-9]{8})$")
ATO_RE = re.compile(r"^ATO-([0-9]{8})$")
SOURCE_KIND_RE = re.compile(r"^[a-z][a-z0-9_]{1,63}$")
ALLOWED_SOURCE_KINDS = {
    "oeis", "aimpl", "open_logic", "open_problem_garden"
}
PINNED_SOURCE_AUTHORITY_RECEIPTS: dict[str, dict[str, str]] = {
    "oeis": {
        "path": "Docs/catalog/v5/curation/oeis_v5_5/audit-receipt.json",
        "file_sha256": "6a05b9ca89540e3e51b42869410fa1e3607a88f9c7a7c14e4ae0125ae1043f20",
        "schema_version": "awesome-theorems/oeis-candidate-audit-receipt/5.5",
    },
    "aimpl": {
        "path": "Docs/catalog/v5/curation/aimpl_v5_5/audit-receipt.json",
        "file_sha256": "01acc230256829ed50010731dd419e17c4b630f4f64651c09600debede741a83",
        "schema_version": "awesome-theorems/aimpl-strict-conjecture-review/1",
    },
    "open_logic": {
        "path": "Docs/catalog/v5/curation/open_logic_v5_5/open-logic-review.count.json",
        "file_sha256": "08f2f925bddf8fd0e4042d90e1687f9a976a2d91ca75af139bc32cb0aaacc27e",
        "schema_version": "awesome-theorems/open-logic-strict-source-review-count/1.0",
    },
    "open_problem_garden": {
        "path": "Docs/catalog/v5/curation/openproblemgarden_v5_5/eligibility-receipt.json",
        "file_sha256": "a51164d2f8976927e88076964c031ca1c7f2c490ead3e036b4f5978f1a5d8d30",
        "schema_version": "awesome-theorems/openproblemgarden-eligibility-receipt/1",
        "authority_sha256": "fc5eea0a063ee501d016a9fba910fa733b5a808344f5b78f3bc7eeab2da7fb15",
    },
}
OEIS_REVIEW_KEY_RE = re.compile(
    r"^(?:v1/reviews/review-[0-9]{2}|v2/reviews/review-v2-[0-9]{2})\.jsonl$"
)


class CheckError(RuntimeError):
    """An authenticated or semantic release invariant failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def reject_constant(token: str) -> None:
    raise CheckError(f"non-finite JSON token is forbidden: {token}")


def closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise CheckError(f"value is not canonical JSON: {error}") from error


def encoded(value: Any) -> bytes:
    return canonical(value) + b"\n"


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def file_sha(path: Path) -> str:
    hasher = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                hasher.update(chunk)
    except OSError as error:
        raise CheckError(f"cannot hash {path}: {error}") from error
    return hasher.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return digest(canonical({key: item for key, item in value.items() if key not in omitted}))


def seal(value: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    result.pop("authority_sha256", None)
    result["authority_sha256"] = hash_without(result, "authority_sha256")
    return result


def set_digest(values: Iterable[str]) -> str:
    return digest(canonical(sorted(values)))


def safe_path(root: Path, relative: Path | str, *, file: bool = True) -> Path:
    raw = Path(relative)
    require(not raw.is_absolute() and raw.parts and ".." not in raw.parts, f"unsafe path: {relative}")
    lexical = root / raw
    cursor = root
    for component in raw.parts:
        cursor = cursor / component
        require(not cursor.is_symlink(), f"symlinked authoritative path is forbidden: {relative}")
    candidate = lexical.resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise CheckError(f"path escapes repository root: {relative}") from error
    if file:
        require(candidate.is_file(), f"required file is missing: {relative}")
    else:
        require(candidate.is_dir(), f"required directory is missing: {relative}")
    return candidate


def repo_root(value: Path) -> Path:
    absolute = value.absolute()
    require(not absolute.is_symlink() and absolute == absolute.resolve(),
            f"symlinked/aliased repository root is forbidden: {value}")
    try:
        root = value.resolve(strict=True)
    except OSError as error:
        raise CheckError(f"repository root does not exist: {value}") from error
    require(root.is_dir(), f"repository root is not a directory: {root}")
    return root


def relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError as error:
        raise CheckError(f"path is outside repository root: {path}") from error


def load_json(root: Path, relative_path: Path | str, *, canonical_file: bool = True) -> dict[str, Any]:
    path = safe_path(root, relative_path)
    raw = path.read_bytes()
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=closed_object, parse_constant=reject_constant
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise CheckError(f"invalid JSON in {relative_path}: {error}") from error
    require(isinstance(value, dict), f"{relative_path} must contain one object")
    if canonical_file:
        require(raw == encoded(value), f"{relative_path} is not canonical JSON plus one LF")
    return value


def parse_document_bytes(raw: bytes, label: str, *, canonical_file: bool = True) -> dict[str, Any]:
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=closed_object, parse_constant=reject_constant
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise CheckError(f"invalid JSON in {label}: {error}") from error
    require(isinstance(value, dict), f"{label} must contain one object")
    if canonical_file:
        require(raw == encoded(value), f"{label} is not canonical JSON plus one LF")
    return value


def verify_seal(document: Mapping[str, Any], label: str) -> None:
    authority = document.get("authority_sha256")
    require(isinstance(authority, str) and SHA_RE.fullmatch(authority) is not None,
            f"{label} authority is malformed")
    require(authority == hash_without(document, "authority_sha256"), f"{label} authority is stale")


def require_string(value: Any, label: str, pattern: re.Pattern[str] | None = None) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{label} must be a nonempty string")
    if pattern is not None:
        require(pattern.fullmatch(value) is not None, f"{label} syntax is invalid: {value!r}")
    return value


def require_integer(value: Any, label: str, minimum: int | None = None) -> int:
    require(isinstance(value, int) and not isinstance(value, bool), f"{label} must be an integer")
    if minimum is not None:
        require(value >= minimum, f"{label} must be at least {minimum}")
    return value


def row_hash(row: Mapping[str, Any], field: str = "row_sha256") -> str:
    return hash_without(row, field)


def primary_rows(document: Mapping[str, Any]) -> int:
    if isinstance(document.get("candidate_dispositions"), list):
        candidates = document["candidate_dispositions"]
        msc = document.get("msc_coverage")
        return len(candidates) + (len(msc) if isinstance(msc, list) else 0)
    if isinstance(document.get("strict_credits"), list):
        credits = document["strict_credits"]
        corrections = document.get("credit_corrections")
        return len(credits) + (len(corrections) if isinstance(corrections, list) else 0)
    for key in ("records", "variants", "mappings", "migrations"):
        rows = document.get(key)
        if isinstance(rows, list):
            return len(rows)
    return 0


def release_root(inventory: Sequence[Mapping[str, Any]]) -> str:
    normalized = [
        {"path": row["path"], "sha256": row["sha256"], "size_bytes": row["size_bytes"]}
        for row in inventory
    ]
    return digest(canonical(sorted(normalized, key=lambda row: str(row["path"]))))


def record_semantic_keys(row: Mapping[str, Any]) -> set[str]:
    result: set[str] = set()
    if isinstance(row.get("semantic_key"), str) and row["semantic_key"]:
        result.add(row["semantic_key"])
    dedupe = row.get("dedupe")
    if isinstance(dedupe, dict):
        if isinstance(dedupe.get("semantic_key"), str) and dedupe["semantic_key"]:
            result.add(dedupe["semantic_key"])
        if isinstance(dedupe.get("normalized_statement_sha256"), str) and SHA_RE.fullmatch(dedupe["normalized_statement_sha256"]):
            result.add(f"normalized-statement-sha256/{dedupe['normalized_statement_sha256']}")
        if isinstance(dedupe.get("identity_payload_sha256"), str) and SHA_RE.fullmatch(dedupe["identity_payload_sha256"]):
            result.add(f"formal-conjectures-parent-identity/{dedupe['identity_payload_sha256']}")
    return result


def theorem_predicate(row: Mapping[str, Any]) -> bool:
    return bool(
        row.get("record_role") == "claim" and row.get("lifecycle") == "active"
        and row.get("truth_apt") is True and row.get("current_claim_kind") == "theorem"
        and row.get("material_status") == "proved"
    )


def open_predicate(row: Mapping[str, Any]) -> bool:
    return bool(
        row.get("record_role") == "claim" and row.get("lifecycle") == "active"
        and row.get("truth_apt") is True and row.get("category") == "open_claim"
        and row.get("current_claim_kind") in {"conjecture", "hypothesis", "open_problem"}
        and row.get("material_status") in {"open", "partial", "independent", "disputed"}
    )


def check_parent(root: Path) -> dict[str, dict[str, Any]]:
    directory = safe_path(root, PARENT_REL, file=False)
    entries = list(directory.iterdir())
    require(all(path.is_file() and not path.is_symlink() for path in entries),
            "5.4 parent contains a non-regular/symlink entry")
    observed = {path.name for path in entries}
    require(observed == ALL_RELEASE_FILES, f"5.4 parent artifact set drifted: {sorted(observed)}")
    require(file_sha(directory / MANIFEST_NAME) == PARENT_MANIFEST_SHA256, "5.4 manifest bytes drifted")
    require(file_sha(directory / "Claim_Catalog.json") == PARENT_CATALOG_SHA256, "5.4 catalog bytes drifted")
    require(file_sha(directory / "Strict_Conjecture_Ledger.json") == PARENT_STRICT_SHA256, "5.4 strict ledger bytes drifted")
    documents = {name: load_json(root, PARENT_REL / name) for name in ALL_RELEASE_FILES}
    for name, document in documents.items():
        verify_seal(document, f"parent {name}")
    manifest = documents[MANIFEST_NAME]
    require(manifest.get("release") == PARENT_RELEASE, "wrong parent release")
    require(manifest.get("release_root_sha256") == PARENT_RELEASE_ROOT, "parent root drifted")
    inventory = manifest.get("artifacts")
    require(isinstance(inventory, list) and len(inventory) == len(RELEASE_FILES), "parent inventory malformed")
    require({row.get("path") for row in inventory if isinstance(row, dict)} == set(RELEASE_FILES), "parent inventory set drifted")
    require(release_root(inventory) == PARENT_RELEASE_ROOT, "parent root does not recompute")
    for row in inventory:
        require(isinstance(row, dict), "parent artifact row malformed")
        name = require_string(row.get("path"), "parent artifact path")
        require(Path(name).name == name, f"unsafe parent artifact path: {name}")
        path = directory / name
        require(file_sha(path) == row.get("sha256"), f"parent artifact hash drifted: {name}")
        require(path.stat().st_size == row.get("size_bytes"), f"parent artifact size drifted: {name}")
        require(primary_rows(documents[name]) == row.get("row_count"), f"parent artifact row count drifted: {name}")
    catalog = documents["Claim_Catalog.json"]
    theorem = documents["Theorem_List.json"]
    opened = documents["Open_Claim_List.json"]
    strict = documents["Strict_Conjecture_Ledger.json"]
    require(len(catalog.get("records", [])) == 4_100, "parent catalog denominator drifted")
    require(len(theorem.get("records", [])) == 2_500, "parent theorem denominator drifted")
    require(len(opened.get("records", [])) == 1_600, "parent open denominator drifted")
    require(len(strict.get("strict_credits", [])) == 1_000, "parent strict denominator drifted")
    return documents


def json_pointer(value: Any, pointer: str, label: str) -> Any:
    require(isinstance(pointer, str) and pointer.startswith("/"), f"{label} must be an absolute RFC6901 pointer")
    current = value
    for encoded_token in pointer.split("/")[1:]:
        # RFC6901 permits only ~0 and ~1 escapes.  Reject invalid escape spellings.
        require(re.search(r"~(?:[^01]|$)", encoded_token) is None, f"{label} has an invalid RFC6901 escape")
        token = encoded_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            require(token in current, f"{label} does not resolve at {token!r}")
            current = current[token]
        elif isinstance(current, list):
            require(token == "0" or (token.isdigit() and not token.startswith("0")), f"{label} has a noncanonical list index")
            index = int(token)
            require(index < len(current), f"{label} list index is out of range")
            current = current[index]
        else:
            raise CheckError(f"{label} traverses a scalar")
    return current


def source_path_is_allowed(source_kind: str, path: str) -> bool:
    patterns = {
        "oeis": (
            r"Docs/catalog/v5/curation/oeis_v5_5/v1/reviews/review-[0-9]{2}\.jsonl",
            r"Docs/catalog/v5/curation/oeis_v5_5/v2/reviews/review-v2-[0-9]{2}\.jsonl",
        ),
        "aimpl": (r"Docs/catalog/v5/curation/aimpl_v5_5/review-ledger\.jsonl",),
        "open_logic": (r"Docs/catalog/v5/curation/open_logic_v5_5/open-logic-review\.jsonl",),
        "open_problem_garden": (
            r"Docs/catalog/v5/curation/openproblemgarden_v5_5/eligibility-ledger\.jsonl",
        ),
    }
    return source_kind in patterns and any(re.fullmatch(pattern, path) for pattern in patterns[source_kind])


def replay_authority_artifact(
    root: Path, row: Any, label: str, *, expected_path: str
) -> dict[str, Any]:
    require(isinstance(row, dict), f"{label} binding malformed")
    require(row.get("path") == expected_path, f"{label} path differs from pinned receipt")
    expected_sha = require_string(row.get("sha256"), f"{label}.sha256", SHA_RE)
    path = safe_path(root, expected_path)
    require(file_sha(path) == expected_sha, f"{label} file hash drifted")
    if row.get("size_bytes") is not None:
        require(row.get("size_bytes") == path.stat().st_size, f"{label} size drifted")
    row_count = len(path.read_bytes().splitlines())
    if row.get("rows") is not None:
        require(row.get("rows") == row_count, f"{label} row count drifted")
    return {
        "path": expected_path, "file_sha256": expected_sha,
        "size_bytes": path.stat().st_size, "row_count": row_count,
    }


def load_source_authorities(root: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for source_kind, specification in PINNED_SOURCE_AUTHORITY_RECEIPTS.items():
        receipt_path = safe_path(root, specification["path"])
        require(file_sha(receipt_path) == specification["file_sha256"],
                f"{source_kind} authority receipt drifted")
        receipt = load_json(root, specification["path"], canonical_file=False)
        require(receipt.get("schema_version") == specification["schema_version"],
                f"{source_kind} authority receipt schema drifted")
        if "authority_sha256" in specification:
            verify_seal(receipt, f"{source_kind} authority receipt")
            require(receipt.get("authority_sha256") == specification["authority_sha256"],
                    f"{source_kind} authority receipt seal differs from the pinned authority")
        reviews: list[dict[str, Any]] = []
        qualification_artifact: dict[str, Any] | None = None
        qualified_candidates: list[dict[str, str]] | None = None
        if source_kind == "oeis":
            artifacts = receipt.get("artifacts")
            require(isinstance(artifacts, dict), "OEIS authority artifact inventory missing")
            for key in sorted(artifacts):
                if OEIS_REVIEW_KEY_RE.fullmatch(key):
                    reviews.append(replay_authority_artifact(
                        root, artifacts[key], f"OEIS authority {key}",
                        expected_path=f"Docs/catalog/v5/curation/oeis_v5_5/{key}",
                    ))
            require(len(reviews) == 16, "OEIS authority must expose exactly 16 review ledgers")
            qualification_artifact = replay_authority_artifact(
                root, artifacts.get("combined-survivors.jsonl"), "OEIS combined survivor authority",
                expected_path=OEIS_SURVIVORS_REL.as_posix(),
            )
            require(qualification_artifact["file_sha256"] == OEIS_SURVIVORS_SHA256,
                    "OEIS qualification artifact is not the pinned survivor set")
            qualified_candidates = []
            seen_candidates: set[str] = set()
            for line_index, survivor in enumerate(load_jsonl(
                safe_path(root, OEIS_SURVIVORS_REL), OEIS_SURVIVORS_REL.as_posix()
            ), start=1):
                candidate = require_string(survivor.get("candidate_key"), f"OEIS survivor[{line_index}] key")
                tier = require_string(survivor.get("importance_tier"), f"OEIS survivor[{line_index}] tier")
                summary = require_string(survivor.get("semantic_summary"), f"OEIS survivor[{line_index}] summary")
                require(candidate not in seen_candidates and tier in {"high", "medium"},
                        f"OEIS survivor[{line_index}] duplicate/ineligible")
                require(survivor.get("candidate_only") is True
                        and survivor.get("grants_catalog_entry") is False
                        and survivor.get("grants_strict_conjecture_credit") is False,
                        f"OEIS survivor[{line_index}] candidate-only boundary drifted")
                seen_candidates.add(candidate)
                qualified_candidates.append({
                    "candidate_key": candidate, "importance_tier": tier, "semantic_summary": summary,
                })
            qualified_candidates.sort(key=lambda row: row["candidate_key"])
            require(len(qualified_candidates) == 268, "OEIS survivor denominator is not 268")
        elif source_kind == "aimpl":
            artifacts = receipt.get("artifacts")
            require(isinstance(artifacts, dict), "AimPL authority artifact inventory missing")
            reviews.append(replay_authority_artifact(
                root, artifacts.get("review_ledger"), "AimPL authority review ledger",
                expected_path="Docs/catalog/v5/curation/aimpl_v5_5/review-ledger.jsonl",
            ))
        elif source_kind == "open_logic":
            require(receipt.get("artifact") == "open-logic-review.jsonl", "Open Logic authority artifact drifted")
            path = "Docs/catalog/v5/curation/open_logic_v5_5/open-logic-review.jsonl"
            reviews.append(replay_authority_artifact(
                root, {"path": path, "sha256": receipt.get("artifact_sha256")},
                "Open Logic authority review", expected_path=path,
            ))
        elif source_kind == "open_problem_garden":
            reviews.append(replay_authority_artifact(
                root, receipt.get("output"), "OPG eligibility authority",
                expected_path="Docs/catalog/v5/curation/openproblemgarden_v5_5/eligibility-ledger.jsonl",
            ))
        else:  # pragma: no cover - adding a source requires a versioned branch.
            raise CheckError(f"no independent authority replay for {source_kind}")
        require(reviews and len({row["path"] for row in reviews}) == len(reviews),
                f"{source_kind} authority review set malformed")
        result[source_kind] = {
            "receipt": {
                "path": specification["path"],
                "file_sha256": specification["file_sha256"],
                "schema_version": specification["schema_version"],
            },
            "review_artifacts": reviews,
        }
        if qualification_artifact is not None:
            result[source_kind]["qualification_artifact"] = qualification_artifact
        if qualified_candidates is not None:
            result[source_kind]["qualified_candidates"] = qualified_candidates
            result[source_kind]["qualified_candidate_key_set_sha256"] = set_digest(
                row["candidate_key"] for row in qualified_candidates
            )
    return result


def replay_jsonl_binding(
    root: Path, row: Mapping[str, Any], index: int,
    authorities: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    binding = row.get("source_binding")
    require(isinstance(binding, dict), f"curation[{index}] source_binding malformed")
    allowed = {
        "path", "file_sha256", "line_number", "source_row_sha256",
        "source_record_key_json_pointer", "exact_claim_json_pointer", "exact_context_json_pointer",
    }
    require(set(binding) == allowed,
            f"curation[{index}] source binding field closure drifted")
    path_text = require_string(binding.get("path"), f"curation[{index}] source path")
    source_kind = require_string(row.get("source_kind"), f"curation[{index}] source_kind", SOURCE_KIND_RE)
    require(source_kind in ALLOWED_SOURCE_KINDS and source_path_is_allowed(source_kind, path_text),
            f"curation[{index}] source path/kind is outside the closed allowlist")
    authority = authorities.get(source_kind)
    require(isinstance(authority, dict), f"curation[{index}] source kind lacks pinned authority")
    reviews = authority.get("review_artifacts")
    require(isinstance(reviews, list), f"curation[{index}] authority review inventory malformed")
    allowed_paths = {item["path"]: item["file_sha256"] for item in reviews if isinstance(item, dict)}
    require(path_text in allowed_paths, f"curation[{index}] source path is not receipt-authorized")
    path = safe_path(root, path_text)
    require(path.suffix == ".jsonl", f"curation[{index}] source is not JSONL")
    require(file_sha(path) == require_string(binding.get("file_sha256"), f"curation[{index}] file SHA", SHA_RE),
            f"curation[{index}] source file drifted")
    require(file_sha(path) == allowed_paths[path_text], f"curation[{index}] source differs from receipt authority")
    line_number = require_integer(binding.get("line_number"), f"curation[{index}] line", 1)
    raw_lines = path.read_bytes().splitlines()
    require(line_number <= len(raw_lines), f"curation[{index}] line is out of range")
    raw_line = raw_lines[line_number - 1]
    try:
        source = json.loads(
            raw_line.decode("utf-8"), object_pairs_hook=closed_object, parse_constant=reject_constant
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise CheckError(f"curation[{index}] bound line is invalid JSON: {error}") from error
    require(isinstance(source, dict), f"curation[{index}] bound row is not an object")
    # Several frozen OEIS v1 review ledgers predate sort-key canonical JSONL.
    # Their exact file bytes are pinned; row identity is nevertheless the
    # canonical parsed-object digest, while duplicate keys/NaN remain fatal.
    require(digest(canonical(source)) == require_string(binding.get("source_row_sha256"), f"curation[{index}] row SHA", SHA_RE),
            f"curation[{index}] source row hash mismatch")
    record_pointer = require_string(binding.get("source_record_key_json_pointer"), f"curation[{index}] record pointer")
    require(str(json_pointer(source, record_pointer, f"curation[{index}] record pointer")) == row.get("source_record_key"),
            f"curation[{index}] source record key differs from reviewed row")
    claim = json_pointer(source, require_string(binding.get("exact_claim_json_pointer"), f"curation[{index}] claim pointer"), f"curation[{index}] claim pointer")
    require(isinstance(claim, str) and claim == row.get("exact_claim_text"),
            f"curation[{index}] exact claim is not the bound reviewed source text")
    context_pointer = binding.get("exact_context_json_pointer")
    if context_pointer is None:
        require(row.get("exact_claim_context") is None, f"curation[{index}] unbound context is non-null")
    else:
        context = json_pointer(source, require_string(context_pointer, f"curation[{index}] context pointer"), f"curation[{index}] context pointer")
        require(isinstance(context, str) and context == row.get("exact_claim_context"),
                f"curation[{index}] exact context differs from source")
    if source_kind == "open_problem_garden":
        require(binding.get("exact_claim_json_pointer") == "/semantic_summary",
                f"curation[{index}] OPG release must bind the independently written summary")
        require(source.get("source_wording_usage") == "evidence_only_not_release_payload",
                f"curation[{index}] OPG source-wording boundary missing")
        require(isinstance(source.get("exact_claim_text"), str)
                and source["exact_claim_text"] != row.get("exact_claim_text"),
                f"curation[{index}] OPG source wording was copied into release payload")
    normalized = copy.deepcopy(binding)
    normalized["authority_receipt"] = copy.deepcopy(authority["receipt"])
    return normalized, source


def nested_values(source: Mapping[str, Any], paths: Sequence[tuple[str, ...]]) -> list[Any]:
    values: list[Any] = []
    for path in paths:
        current: Any = source
        for part in path:
            if not isinstance(current, dict) or part not in current:
                break
            current = current[part]
        else:
            values.append(current)
    return values


def check_source_review_gate(source: Mapping[str, Any], row: Mapping[str, Any], index: int) -> None:
    source_kind = row.get("source_kind")
    if source_kind == "oeis":
        require(source.get("decision") == "accept", f"curation[{index}] OEIS review is not accepted")
        require(source.get("truth_apt") is True and source.get("context_complete") is True
                and source.get("source_asserted_open_as_of_commit") is True
                and source.get("importance_tier") == row.get("importance_tier") in {"high", "medium"},
                f"curation[{index}] OEIS source-review gates failed")
        require(source.get("semantic_summary") == row.get("semantic_summary"),
                f"curation[{index}] OEIS summary differs from reviewed row")
        return
    elif source_kind == "aimpl":
        initial = source.get("initial_review")
        require(source.get("final_decision") == "accept" and isinstance(initial, dict)
                and initial.get("decision") == "accept" and initial.get("truth_apt") is True
                and initial.get("context_complete") is True and initial.get("source_asserted_open") is True
                and source.get("final_tier") == row.get("importance_tier") in {"high", "medium"},
                f"curation[{index}] AimPL source-review gates failed")
        require(initial.get("tier") == row.get("importance_tier")
                and initial.get("semantic_summary") == row.get("semantic_summary"),
                f"curation[{index}] AimPL tier/summary differs from reviewed row")
        return
    elif source_kind == "open_logic":
        require(source.get("decision") == "accept" and source.get("acceptance_evidence_complete") is True
                and source.get("grants_strict_conjecture_credit") is True
                and source.get("truth_apt") is True and source.get("context_complete") is True
                and source.get("importance_tier") == row.get("importance_tier") in {"high", "medium"}
                and source.get("question_to_assertion_promotion_permitted") is False,
                f"curation[{index}] Open Logic source-review gates failed")
        return
    elif source_kind == "open_problem_garden":
        global_dedupe = source.get("global_dedupe")
        require(source.get("formal_acceptance_eligible_for_5_5") is True
                and source.get("decision") == "accept"
                and source.get("candidate_only") is True
                and source.get("grants_catalog_entry") is False
                and source.get("grants_strict_conjecture_credit") is False
                and source.get("truth_apt") is True and source.get("context_complete") is True
                and source.get("importance_tier") == row.get("importance_tier") in {"high", "medium"}
                and source.get("current_open_as_of") == REVIEW_DATE
                and isinstance(global_dedupe, dict) and global_dedupe.get("semantic_unique") is True
                and source.get("source_wording_usage") == "evidence_only_not_release_payload",
                f"curation[{index}] OPG source-review gates failed")
        require(source.get("semantic_summary") == row.get("exact_claim_text") == row.get("semantic_summary")
                and source.get("semantic_key") == row.get("semantic_key")
                and str(source.get("source_record_key")) == row.get("source_record_key"),
                f"curation[{index}] OPG summary/semantic/source identity drifted")
        return
    decisions = nested_values(source, (("decision",), ("final_decision",), ("initial_review", "decision")))
    require(decisions, f"curation[{index}] source review has no independent decision")
    require(any(value in {"accept", "eligible_existing_strict_credit", "eligible"} for value in decisions),
            f"curation[{index}] source review is not accepted")
    require(not any(value in {"pending", "reject", "rejected"} for value in decisions if value is not None),
            f"curation[{index}] promotes a pending/rejected source review")
    truth_values = nested_values(source, (("truth_apt",), ("initial_review", "truth_apt")))
    context_values = nested_values(source, (("context_complete",), ("initial_review", "context_complete")))
    require(True in truth_values, f"curation[{index}] source truth-apt gate is absent/false")
    require(True in context_values, f"curation[{index}] source context gate is absent/false")
    tiers = nested_values(source, (("importance_tier",), ("final_tier",), ("tier",), ("initial_review", "tier")))
    require(row.get("importance_tier") in tiers and row.get("importance_tier") in {"high", "medium"},
            f"curation[{index}] importance tier is not source-reviewed")
    open_values = nested_values(
        source,
        (
            ("current_open_as_of_review",), ("current_open_as_of_2026_08_10",),
            ("source_asserted_open",), ("source_asserted_open_as_of_commit",),
            ("source_status", "current_open_as_of_review"),
            ("initial_review", "source_asserted_open"),
        ),
    )
    require(True in open_values, f"curation[{index}] source current-open gate is absent/false")
    require(source.get("question_to_assertion_promotion_permitted") is not True,
            f"curation[{index}] source permits question promotion")


def normalize_classification(row: Mapping[str, Any], index: int) -> dict[str, Any]:
    raw = row.get("classification")
    if raw is None:
        raw = {"status": "review_metadata_unassigned", "msc_codes": [], "primary_msc_top_class": None}
    require(isinstance(raw, dict), f"curation[{index}] classification malformed")
    result = copy.deepcopy(raw)
    codes = result.get("msc_codes", [])
    require(isinstance(codes, list), f"curation[{index}] msc_codes malformed")
    normalized_codes: list[str] = []
    roots: list[str] = []
    for code_index, code in enumerate(codes):
        text = require_string(code, f"curation[{index}] msc_codes[{code_index}]")
        match = re.fullmatch(r"(?P<root>[0-9]{2})(?:[A-Z][0-9]{2})?", text)
        require(match is not None and text not in normalized_codes, f"curation[{index}] invalid/duplicate MSC code")
        normalized_codes.append(text)
        if match.group("root") not in roots:
            roots.append(match.group("root"))
    primary = result.get("primary_msc_top_class")
    if roots:
        primary = require_string(primary, f"curation[{index}] primary MSC")
        require(primary in roots, f"curation[{index}] primary MSC not represented")
    else:
        require(primary is None, f"curation[{index}] primary MSC exists without a code")
    result["msc_codes"] = normalized_codes
    result["primary_msc_top_class"] = primary
    return result


def parse_jsonl_rows_loose(path: Path, label: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, raw in enumerate(path.read_bytes().splitlines(), start=1):
        try:
            row = json.loads(raw.decode("utf-8"), object_pairs_hook=closed_object, parse_constant=reject_constant)
        except (UnicodeError, json.JSONDecodeError) as error:
            raise CheckError(f"{label}:{index}: invalid JSON: {error}") from error
        require(isinstance(row, dict), f"{label}:{index} is not an object")
        rows.append(row)
    return rows


def source_review_disposition(
    source_kind: str, row: Mapping[str, Any], authority: Mapping[str, Any]
) -> str:
    if source_kind == "oeis":
        decision = row.get("decision")
        require(decision in {"accept", "reject"}, "OEIS review disposition malformed")
        survivors = authority.get("qualified_candidates")
        require(isinstance(survivors, list), "OEIS survivor authority missing")
        survivor_keys = {item["candidate_key"] for item in survivors if isinstance(item, dict)}
        return "accepted_eligible" if decision == "accept" and row.get("candidate_key") in survivor_keys else "rejected"
    decision = row.get("final_decision") if source_kind == "aimpl" else row.get("decision")
    if source_kind == "open_problem_garden" and decision is None:
        return "accepted_eligible" if row.get("formal_acceptance_eligible_for_5_5") is True else "rejected"
    require(decision in {"accept", "eligible", "pending", "reject"}, f"{source_kind} review disposition malformed")
    if decision in {"accept", "eligible"}:
        return "accepted_eligible"
    return "pending" if decision == "pending" else "rejected"


def expected_coverage_bindings(
    root: Path, authorities: Mapping[str, Mapping[str, Any]]
) -> list[dict[str, Any]]:
    expected: list[dict[str, Any]] = []
    for source_kind in sorted(authorities):
        authority = authorities[source_kind]
        receipt = authority.get("receipt")
        reviews = authority.get("review_artifacts")
        require(isinstance(receipt, dict) and isinstance(reviews, list), f"{source_kind} authority malformed")
        for review_index, review in enumerate(reviews):
            require(isinstance(review, dict), f"{source_kind} review binding[{review_index}] malformed")
            path = safe_path(root, review["path"])
            counts = {"accepted_eligible": 0, "pending": 0, "rejected": 0}
            for row in parse_jsonl_rows_loose(path, str(review["path"])):
                counts[source_review_disposition(source_kind, row, authority)] += 1
            require(sum(counts.values()) == review["row_count"], f"{source_kind} review coverage count drifted")
            expected.append({
                "source_kind": source_kind, "path": review["path"],
                "file_sha256": review["file_sha256"], "size_bytes": review["size_bytes"],
                "rows": review["row_count"], **counts,
                "audit_receipt": copy.deepcopy(receipt),
            })
    return sorted(expected, key=lambda row: (row["source_kind"], row["path"]))


def check_curation(
    root: Path, parent_records: Sequence[Mapping[str, Any]],
    authorities: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    document = load_json(root, CURATION_REL)
    verify_seal(document, "strict curation")
    require(document.get("authority_sha256") == STRICT_CURATION_AUTHORITY_SHA256,
            "strict curation authority differs from the independently pinned review result")
    require(set(document) == {
        "schema_version", "review_as_of", "parent", "coverage_bindings",
        "candidate_dispositions", "counts", "set_digests", "authority_sha256",
    }, "strict curation top-level field closure drifted")
    require(document.get("schema_version") == "awesome-theorems/strict-conjecture-curation/5.5", "strict curation schema drifted")
    require(document.get("review_as_of") == REVIEW_DATE, "strict curation review date drifted")
    parent = document.get("parent")
    require(isinstance(parent, dict) and parent == {
        "release": PARENT_RELEASE,
        "release_root_sha256": PARENT_RELEASE_ROOT,
        "claim_catalog_sha256": PARENT_CATALOG_SHA256,
        "strict_ledger_sha256": PARENT_STRICT_SHA256,
    }, "strict curation parent binding drifted")
    coverage = document.get("coverage_bindings")
    require(isinstance(coverage, list), "strict curation coverage_bindings malformed")
    coverage_keys = {
        "source_kind", "path", "file_sha256", "size_bytes", "rows",
        "accepted_eligible", "pending", "rejected", "audit_receipt",
    }
    normalized_coverage: list[dict[str, Any]] = []
    for index, item in enumerate(coverage):
        require(isinstance(item, dict) and set(item) == coverage_keys, f"coverage binding[{index}] closure drifted")
        for field in ("size_bytes", "rows", "accepted_eligible", "pending", "rejected"):
            require_integer(item.get(field), f"coverage[{index}].{field}", 0)
        require(item["accepted_eligible"] + item["pending"] + item["rejected"] == item["rows"],
                f"coverage binding[{index}] disposition partition does not close")
        normalized_coverage.append(copy.deepcopy(item))
    normalized_coverage.sort(key=lambda item: (item["source_kind"], item["path"]))
    require(normalized_coverage == expected_coverage_bindings(root, authorities),
            "strict curation coverage bindings do not replay the pinned review universe")
    rows = document.get("candidate_dispositions")
    require(isinstance(rows, list) and rows, "strict curation candidate rows missing")
    parent_semantics = set().union(*(record_semantic_keys(row) for row in parent_records))
    all_keys: set[str] = set()
    accepted_semantics: set[str] = set()
    accepted_sources: set[tuple[str, str]] = set()
    accepted_source_paths: set[str] = set()
    accepted: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"curation[{index}] is not an object")
        require(row.get("row_sha256") == row_hash(row), f"curation[{index}] row hash is stale")
        key = require_string(row.get("candidate_key"), f"curation[{index}] candidate_key")
        require(key not in all_keys, f"duplicate curation candidate key: {key}")
        all_keys.add(key)
        decision = row.get("decision")
        require(decision in {"accept", "reject", "pending"}, f"curation[{index}] decision invalid")
        grants = row.get("grants_catalog_entry") is True or row.get("grants_strict_conjecture_credit") is True
        if decision != "accept":
            require(not grants and row.get("accepted_rank") is None, f"curation[{index}] nonaccept row grants credit")
            continue
        binding, source = replay_jsonl_binding(root, row, index, authorities)
        check_source_review_gate(source, row, index)
        require(row.get("grants_catalog_entry") is True and row.get("grants_strict_conjecture_credit") is True,
                f"curation[{index}] accepted row lacks both grants")
        rank = require_integer(row.get("accepted_rank"), f"curation[{index}] accepted_rank", 1)
        source_kind = require_string(row.get("source_kind"), f"curation[{index}] source_kind", SOURCE_KIND_RE)
        require(source_kind in ALLOWED_SOURCE_KINDS, f"curation[{index}] source kind is not approved")
        source_record = require_string(row.get("source_record_key"), f"curation[{index}] source_record_key")
        require((source_kind, source_record) not in accepted_sources, f"curation[{index}] duplicate source record")
        statement = require_string(row.get("exact_claim_text"), f"curation[{index}] exact_claim_text")
        require(not statement.rstrip().endswith("?"), f"curation[{index}] exact claim is interrogative")
        require(row.get("question_to_assertion_promotion_performed") is False, f"curation[{index}] performs question promotion")
        require(row.get("truth_apt") is True and row.get("context_complete") is True,
                f"curation[{index}] statement gate failed")
        require(row.get("current_open_as_of_review") is True, f"curation[{index}] is not current-open")
        require(row.get("importance_tier") in {"high", "medium"}, f"curation[{index}] importance gate failed")
        require(row.get("atomicity") in {"single", "source_named_compound"}, f"curation[{index}] atomicity invalid")
        representation = row.get("statement_representation", "reviewed_release_assertion")
        require(representation in {
            "reviewed_release_assertion", "reviewed_exact_source_assertion",
            "independently_written_reviewed_summary",
        }, f"curation[{index}] statement representation invalid")
        require(isinstance(row.get("current_status_evidence"), dict) and bool(row["current_status_evidence"]),
                f"curation[{index}] status evidence missing")
        rights = row.get("rights")
        require(isinstance(rights, dict) and rights.get("cleared_for_catalog_metadata_and_statement") is True,
                f"curation[{index}] rights gate failed")
        require(isinstance(rights.get("attribution"), str) and rights["attribution"].strip(),
                f"curation[{index}] attribution missing")
        if source_kind == "open_problem_garden":
            require(rights.get("exact_source_wording_excluded_from_release") is True
                    and rights.get("source_wording_redistributed") is False,
                    f"curation[{index}] OPG rights boundary failed")
            require(representation == "independently_written_reviewed_summary"
                    and rights.get("statement_origin") == "independently_written_reviewed_summary",
                    f"curation[{index}] OPG statement origin is not independent")
        dedupe = row.get("dedupe")
        require(isinstance(dedupe, dict) and dedupe.get("parent_semantic_unique") is True
                and dedupe.get("cross_source_semantic_unique") is True,
                f"curation[{index}] semantic dedupe gate failed")
        semantic = require_string(row.get("semantic_key"), f"curation[{index}] semantic_key")
        require(semantic not in parent_semantics, f"curation[{index}] duplicates parent semantic identity")
        require(semantic not in accepted_semantics, f"curation[{index}] duplicates accepted semantic identity")
        normalized = copy.deepcopy(row)
        normalized["source_binding"] = binding
        normalized["statement_representation"] = representation
        normalized["classification"] = normalize_classification(row, index)
        normalized["_statement"] = statement
        normalized["_summary"] = require_string(row.get("semantic_summary"), f"curation[{index}] semantic_summary")
        accepted.append(normalized)
        accepted_semantics.add(semantic)
        accepted_sources.add((source_kind, source_record))
        accepted_source_paths.add(binding["path"])
        require(rank <= MAX_NEW_STRICT, f"curation[{index}] rank exceeds release maximum")
    accepted.sort(key=lambda row: int(row["accepted_rank"]))
    require([row["accepted_rank"] for row in accepted] == list(range(1, len(accepted) + 1)), "accepted ranks are not dense")
    require(MIN_NEW_STRICT <= len(accepted) <= MAX_NEW_STRICT, "strict curation misses 401--1,000 gate")
    require(accepted_source_paths <= {item["path"] for item in normalized_coverage},
            "an accepted row uses a source absent from coverage bindings")
    survivors_path = safe_path(root, OEIS_SURVIVORS_REL)
    require(file_sha(survivors_path) == OEIS_SURVIVORS_SHA256, "OEIS final survivor set drifted")
    survivor_rows = load_jsonl(survivors_path, OEIS_SURVIVORS_REL.as_posix())
    require(len(survivor_rows) == 268, "OEIS final survivor denominator drifted")
    survivor_by_key = {row.get("candidate_key"): row for row in survivor_rows}
    require(len(survivor_by_key) == 268 and None not in survivor_by_key, "OEIS survivor keys are not unique")
    admitted_oeis = {row["candidate_key"]: row for row in accepted if row["source_kind"] == "oeis"}
    require(set(admitted_oeis) == set(survivor_by_key), "curation OEIS admissions differ from final 268 survivors")
    for key, row in admitted_oeis.items():
        survivor = survivor_by_key[key]
        require(row["importance_tier"] == survivor.get("importance_tier")
                and row["semantic_summary"] == survivor.get("semantic_summary"),
                f"curation OEIS survivor metadata drifted: {key}")
    counts = document.get("counts")
    expected_counts = {
        "admissible_pool_rows": len(rows),
        "accepted_new_strict_conjectures": len(accepted),
        "pending_not_credited": sum(row.get("decision") == "pending" for row in rows),
        "rejected_not_credited": sum(row.get("decision") == "reject" for row in rows),
        "by_source": dict(sorted(Counter(row["source_kind"] for row in accepted).items())),
    }
    require(counts == expected_counts, "strict curation counts do not match the independently replayed pool")
    require(document.get("set_digests") == {
        "accepted_candidate_key_set_sha256": set_digest(row["candidate_key"] for row in accepted),
        "accepted_semantic_key_set_sha256": set_digest(row["semantic_key"] for row in accepted),
    }, "strict curation accepted-set digests drifted")
    return document, accepted


def check_important(root: Path, parent: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    source_path = safe_path(root, MATHLIB_SOURCE_REL)
    require(file_sha(source_path) == MATHLIB_SOURCE_SHA256, "mathlib source asset drifted")
    source = load_json(root, MATHLIB_SOURCE_REL, canonical_file=False)
    source_rows = source.get("records")
    require(isinstance(source_rows, list) and len(source_rows) == 1_500, "mathlib source denominator drifted")
    source_by_id = {row.get("source_record_id"): row for row in source_rows if isinstance(row, dict)}
    require(len(source_by_id) == 1_500 and None not in source_by_id, "mathlib source IDs are not unique")
    accepted_by_stage: dict[str, tuple[str, dict[str, Any]]] = {}
    for relative_path, expected_sha in zip(MATHLIB_CURATION_RELS, MATHLIB_CURATION_SHA256, strict=True):
        require(file_sha(safe_path(root, relative_path)) == expected_sha, f"mathlib curation drifted: {relative_path}")
        curation = load_json(root, relative_path)
        verify_seal(curation, f"important source curation {relative_path}")
        rows = [row for row in curation.get("candidate_dispositions", [])
                if isinstance(row, dict) and row.get("disposition") == "accepted_new_kernel_checked_theorem"]
        require(len(rows) == 500, f"important source curation denominator drifted: {relative_path}")
        for row in rows:
            require(row.get("row_sha256") == row_hash(row), "important source curation row hash stale")
            sid = require_string(row.get("target_s5_id"), "important source target", S5_RE)
            require(sid not in accepted_by_stage, f"duplicate important source target: {sid}")
            accepted_by_stage[sid] = (relative_path.as_posix(), row)
    require(len(accepted_by_stage) == IMPORTANT_COUNT, "important source union is not 1,000")
    document = load_json(root, IMPORTANT_REL)
    require(file_sha(safe_path(root, IMPORTANT_REL)) == IMPORTANT_FILE_SHA256,
            "important theorem inventory file pin drifted")
    verify_seal(document, "important theorem inventory")
    require(document.get("authority_sha256") == IMPORTANT_AUTHORITY_SHA256,
            "important theorem inventory authority pin drifted")
    require(document.get("schema_version") == "awesome-theorems/mathlib-important-inventory/5.5", "important schema drifted")
    require(document.get("review_as_of") == REVIEW_DATE, "important review date drifted")
    rows = document.get("records")
    require(isinstance(rows, list) and len(rows) == IMPORTANT_COUNT, "important inventory is not exactly 1,000")
    require([row.get("stage_claim_id") for row in rows] == sorted(accepted_by_stage), "important inventory order/set differs from source curations")
    catalog_by_id = {row["stage_claim_id"]: row for row in parent["Claim_Catalog.json"]["records"]}
    tiers: Counter[str] = Counter()
    origins: Counter[str] = Counter()
    source_ids: list[str] = []
    semantic_keys: list[str] = []
    row_hashes: list[str] = []
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"important[{index}] malformed")
        sid = require_string(row.get("stage_claim_id"), f"important[{index}] stage ID", S5_RE)
        curation_path, curation_row = accepted_by_stage[sid]
        source_id = curation_row["source_record_id"]
        source_row = source_by_id[source_id]
        claim = catalog_by_id[sid]
        require(row.get("row_sha256") == row_hash(row), f"important[{index}] row hash stale")
        require(row.get("curation_path") == curation_path and row.get("curation_row_sha256") == curation_row["row_sha256"], f"important[{index}] curation binding drifted")
        require(row.get("source_record_id") == source_id and row.get("source_record_sha256") == digest(canonical(source_row)), f"important[{index}] source binding drifted")
        require(row.get("variant_id") == claim.get("variant_id") and row.get("family_id") == claim.get("family_id"), f"important[{index}] identity binding drifted")
        require(row.get("semantic_key") in record_semantic_keys(claim) and row.get("semantic_key") == curation_row.get("semantic_key"), f"important[{index}] semantic binding drifted")
        require(theorem_predicate(claim), f"important[{index}] does not bind a proved parent theorem")
        require(source_row.get("formal_proof_state") == "kernel_checked_sorry_free"
                and source_row.get("proof_evidence", {}).get("uses_sorry") is False,
                f"important[{index}] kernel proof gate failed")
        require(source_row.get("material_status", {}).get("as_of_commit") == MATHLIB_COMMIT,
                f"important[{index}] source commit drifted")
        signals = source_row.get("importance_signals")
        require(isinstance(signals, list) and signals, f"important[{index}] importance signals missing")
        kinds = sorted({signal.get("kind") for signal in signals if isinstance(signal, dict)})
        expected_tier = ("human_curated_mathlib_1000_named_theorem"
                         if "mathlib_1000_theorems" in kinds
                         else "human_documented_mathlib_module_main_result")
        require("mathlib_1000_theorems" in kinds or "mathlib_module_main_result" in kinds,
                f"important[{index}] lacks human editorial signal")
        evidence = row.get("importance_evidence")
        require(isinstance(evidence, dict) and evidence.get("signals") == signals
                and evidence.get("signal_kinds") == kinds
                and evidence.get("operational_importance_credit") is True,
                f"important[{index}] importance evidence drifted")
        require(row.get("quality_tier") == expected_tier, f"important[{index}] quality tier drifted")
        require(row.get("grants_existing_important_theorem_credit") is True
                and row.get("grants_new_theorem_identity_credit") is False
                and row.get("grants_new_proof_credit") is False,
                f"important[{index}] credit boundary drifted")
        require(row.get("rights") == source_row.get("rights"), f"important[{index}] rights binding drifted")
        tiers[expected_tier] += 1
        origins[str(row.get("origin_release"))] += 1
        source_ids.append(source_id)
        semantic_keys.append(row["semantic_key"])
        row_hashes.append(row["row_sha256"])
    require(len(set(source_ids)) == len(set(semantic_keys)) == IMPORTANT_COUNT, "important source/semantic duplicate")
    require(document.get("counts") == {
        "by_origin_release": dict(sorted(origins.items())),
        "by_quality_tier": dict(sorted(tiers.items())),
        "existing_important_theorem_credits": IMPORTANT_COUNT,
        "new_proof_credits": 0,
        "new_theorem_identity_credits": 0,
    }, "important inventory counters drifted")
    require(document.get("set_digests") == {
        "row_sha256_set_sha256": set_digest(row_hashes),
        "semantic_keys_sha256": set_digest(semantic_keys),
        "source_record_ids_sha256": set_digest(source_ids),
        "stage_claim_ids_sha256": set_digest(accepted_by_stage),
    }, "important inventory set digests drifted")
    return document


def load_jsonl(path: Path, label: str) -> list[dict[str, Any]]:
    payload = path.read_bytes()
    require(payload.endswith(b"\n"), f"{label} lacks terminal LF")
    rows: list[dict[str, Any]] = []
    for index, raw_line in enumerate(payload.splitlines()):
        try:
            row = json.loads(
                raw_line.decode("utf-8"), object_pairs_hook=closed_object,
                parse_constant=reject_constant,
            )
        except (UnicodeError, json.JSONDecodeError) as error:
            raise CheckError(f"{label}:{index + 1}: invalid JSON: {error}") from error
        require(isinstance(row, dict), f"{label}:{index + 1} is not an object")
        # Review evidence is byte-pinned as a whole.  Row identity is the
        # canonical parsed-object hash; legacy key ordering is not rewritten.
        rows.append(row)
    return rows


def all_review_gates_pass(gates: Any) -> bool:
    if not isinstance(gates, dict) or not gates:
        return False
    for value in gates.values():
        if isinstance(value, bool):
            if value is not True:
                return False
        elif isinstance(value, dict):
            if value.get("pass") is True or value.get("verdict") == "pass":
                continue
            return False
        else:
            return False
    return True


def normalize_frontier_review(
    root: Path, path: Path, line_index: int, row: Mapping[str, Any]
) -> dict[str, Any]:
    label = f"{relative(root, path)}:{line_index + 1}"
    erdos = path.name.startswith("erdos_")
    if erdos:
        identity = row.get("identity")
        source = row.get("source_binding")
        require(isinstance(identity, dict) and isinstance(source, dict), f"{label} malformed")
        candidate_index = source.get("zero_based_row")
        stage_id = identity.get("stage_claim_id")
        variant_id = identity.get("variant_id")
        semantic = identity.get("semantic_identity_key")
        decision = row.get("decision")
        accepted = decision == "accept" and row.get("all_gates_pass") is True and all_review_gates_pass(row.get("gates"))
        lane = "erdos_supplemental" if "supplemental" in path.name else "erdos_primary"
        if lane == "erdos_supplemental":
            candidate_index = row.get("supplemental_index", row.get("supplemental_rank", candidate_index))
        rights = row.get("rights_boundary")
        references = [
            value.get("evidence")
            for key, value in row.get("gates", {}).items()
            if key == "primary_resolution" and isinstance(value, dict)
        ]
    else:
        candidate_index = row.get("candidate_rank")
        stage_id = row.get("stage_claim_id")
        variant_id = row.get("variant_id")
        semantic = row.get("semantic_key")
        decision = row.get("decision")
        accepted = decision == "eligible_existing_frontier_credit" and all_review_gates_pass(row.get("gates"))
        lane = "nonerdos_supplemental" if "supplemental" in path.name else "nonerdos_primary"
        rights = {"review_finding": row.get("rights_finding"), "gate": row.get("gates", {}).get("rights")}
        references = row.get("primary_references", row.get("primary_resolution_references", []))
    require(isinstance(candidate_index, int) and not isinstance(candidate_index, bool), f"{label} candidate index malformed")
    require_string(stage_id, f"{label} stage ID", S5_RE)
    require_string(variant_id, f"{label} variant ID", ATV_RE)
    require_string(semantic, f"{label} semantic key")
    declared = row.get("row_sha256", row.get("review_row_sha256"))
    if declared is not None:
        field = "row_sha256" if "row_sha256" in row else "review_row_sha256"
        require(declared == row_hash(row, field), f"{label} declared row hash stale")
    return {
        "lane": lane,
        "candidate_index": candidate_index,
        "stage_claim_id": stage_id,
        "variant_id": variant_id,
        "semantic_key": semantic,
        "decision": decision,
        "accepted": accepted,
        "all_gates_pass": all_review_gates_pass(row.get("gates")) and row.get("all_gates_pass", True) is True,
        "rights_evidence": copy.deepcopy(rights),
        "primary_references": copy.deepcopy(references),
        "review_binding": {
            "path": relative(root, path),
            "file_sha256": file_sha(path),
            "line_number": line_index + 1,
            "review_row_sha256": digest(canonical(row)),
        },
    }


def check_frontier_coverage(rows: Sequence[Mapping[str, Any]]) -> None:
    by_lane: dict[str, list[int]] = {}
    for row in rows:
        by_lane.setdefault(str(row["lane"]), []).append(int(row["candidate_index"]))
    expected = {
        "erdos_primary": set(range(379)),
        "erdos_supplemental": set(range(167)),
        "nonerdos_primary": set(range(1, 255)),
        "nonerdos_supplemental": set(range(255, 372)),
    }
    require(set(by_lane) == set(expected), f"frontier review lanes incomplete: {sorted(by_lane)}")
    for lane, wanted in expected.items():
        observed = by_lane[lane]
        if lane == "erdos_supplemental" and set(observed) == set(range(1, 168)) and len(observed) == 167:
            continue
        require(set(observed) == wanted and len(observed) == len(wanted), f"frontier {lane} coverage differs")


def check_frontier(
    root: Path, parent: Mapping[str, Mapping[str, Any]], important: Mapping[str, Any]
) -> dict[str, Any]:
    require(file_sha(safe_path(root, FRONTIER_REL)) == FRONTIER_FILE_SHA256,
            "frontier qualification file differs from the independently accepted artifact")
    document = load_json(root, FRONTIER_REL)
    verify_seal(document, "frontier theorem qualification")
    require(document.get("authority_sha256") == FRONTIER_AUTHORITY_SHA256,
            "frontier qualification authority differs from the independently accepted artifact")
    require(document.get("schema_version") == "awesome-theorems/frontier-theorem-qualification/5.5", "frontier schema drifted")
    require(document.get("review_as_of") == REVIEW_DATE, "frontier review date drifted")
    require(document.get("parent") == {
        "release": PARENT_RELEASE,
        "release_root_sha256": PARENT_RELEASE_ROOT,
        "claim_catalog_sha256": PARENT_CATALOG_SHA256,
        "release_manifest_sha256": PARENT_MANIFEST_SHA256,
    }, "frontier parent binding drifted")
    inputs = document.get("inputs")
    require(isinstance(inputs, dict), "frontier inputs malformed")
    declared_reviews = inputs.get("review_ledgers")
    require(isinstance(declared_reviews, list) and declared_reviews, "frontier review bindings missing")
    specialized_checker_path = safe_path(root, FRONTIER_SPECIALIZED_CHECKER_REL)
    require(file_sha(specialized_checker_path) == FRONTIER_SPECIALIZED_CHECKER_SHA256,
            "frontier specialized checker differs from its accepted trust root")
    acceptance_path = safe_path(root, FRONTIER_ACCEPTANCE_REL)
    require(file_sha(acceptance_path) == FRONTIER_ACCEPTANCE_FILE_SHA256,
            "frontier independent acceptance receipt file drifted")
    acceptance = load_json(root, FRONTIER_ACCEPTANCE_REL)
    verify_seal(acceptance, "frontier independent acceptance receipt")
    require(acceptance.get("authority_sha256") == FRONTIER_ACCEPTANCE_AUTHORITY_SHA256,
            "frontier independent acceptance receipt authority drifted")
    expected_review_manifest = {
        "files": len(declared_reviews),
        "rows": sum(
            require_integer(item.get("rows"), f"frontier receipt review[{index}].rows", 0)
            for index, item in enumerate(declared_reviews)
            if isinstance(item, dict)
        ),
        "manifest_sha256": digest(canonical(declared_reviews)),
        "file_sha256_set_sha256": set_digest(
            require_string(item.get("file_sha256"), f"frontier receipt review[{index}].file_sha256", SHA_RE)
            for index, item in enumerate(declared_reviews)
            if isinstance(item, dict)
        ),
        "entries": copy.deepcopy(declared_reviews),
    }
    require(len(expected_review_manifest["entries"]) == len(declared_reviews)
            and all(isinstance(item, dict) for item in declared_reviews),
            "frontier receipt review manifest contains a non-object")
    require(expected_review_manifest["manifest_sha256"] == FRONTIER_REVIEW_MANIFEST_SHA256
            and expected_review_manifest["file_sha256_set_sha256"] == FRONTIER_REVIEW_FILE_SET_SHA256,
            "frontier review universe differs from the independently accepted manifest")
    expected_acceptance = {
        "schema_version": "awesome-theorems/frontier-theorem-qualification-acceptance-receipt/5.5",
        "review_as_of": REVIEW_DATE,
        "qualification": {
            "path": FRONTIER_REL.as_posix(),
            "file_sha256": FRONTIER_FILE_SHA256,
            "authority_sha256": FRONTIER_AUTHORITY_SHA256,
        },
        "checker": {
            "path": FRONTIER_SPECIALIZED_CHECKER_REL.as_posix(),
            "file_sha256": FRONTIER_SPECIALIZED_CHECKER_SHA256,
            "independent_from_builder": True,
            "read_only": True,
        },
        "review_manifest": expected_review_manifest,
        "counts": copy.deepcopy(document.get("counts")),
        "findings": [],
    }
    expected_acceptance["authority_sha256"] = hash_without(expected_acceptance, "authority_sha256")
    require(acceptance == expected_acceptance,
            "frontier independent acceptance receipt does not bind the exact replayed artifact set")
    review_directory = safe_path(root, FRONTIER_REVIEW_REL, file=False)
    actual_paths = sorted(review_directory.glob("*.jsonl"), key=lambda path: path.name.encode("utf-8"))
    declared_paths: list[Path] = []
    normalized: list[dict[str, Any]] = []
    for index, binding in enumerate(declared_reviews):
        require(isinstance(binding, dict), f"frontier review binding[{index}] malformed")
        require(set(binding) == {"path", "file_sha256", "size_bytes", "rows"}, f"frontier review binding[{index}] closure drifted")
        text_path = require_string(binding.get("path"), f"frontier review binding[{index}].path")
        path = safe_path(root, text_path)
        require(path.parent == review_directory and path.suffix == ".jsonl"
                and path.name.startswith(("erdos_", "nonerdos_")),
                f"frontier review binding[{index}] path is outside frozen review universe")
        require(path not in declared_paths, f"duplicate frontier review binding: {text_path}")
        require(file_sha(path) == binding.get("file_sha256"), f"frontier review hash drifted: {text_path}")
        require(path.stat().st_size == binding.get("size_bytes"), f"frontier review size drifted: {text_path}")
        rows = load_jsonl(path, text_path)
        require(len(rows) == binding.get("rows"), f"frontier review row count drifted: {text_path}")
        normalized.extend(normalize_frontier_review(root, path, row_index, row) for row_index, row in enumerate(rows))
        declared_paths.append(path)
    require(declared_paths == actual_paths, "frontier qualification omits or reorders a review ledger")
    check_frontier_coverage(normalized)
    important_binding = inputs.get("important_inventory")
    important_path = safe_path(root, IMPORTANT_REL)
    require(important_binding == {
        "path": IMPORTANT_REL.as_posix(),
        "file_sha256": file_sha(important_path),
        "authority_sha256": important["authority_sha256"],
        "rows": IMPORTANT_COUNT,
    }, "frontier important-inventory binding drifted")
    parent_theorems = {
        row["stage_claim_id"]: row for row in parent["Claim_Catalog.json"]["records"]
        if theorem_predicate(row)
    }
    require(len(parent_theorems) == 2_500, "frontier parent theorem denominator drifted")
    important_ids = {row["stage_claim_id"] for row in important["records"]}
    accepted = [row for row in normalized if row["accepted"]]
    accepted.sort(key=lambda row: (
        {"erdos_primary": 0, "erdos_supplemental": 1, "nonerdos_primary": 2, "nonerdos_supplemental": 3}[str(row["lane"])],
        int(row["candidate_index"]), str(row["stage_claim_id"]),
    ))
    seen_stage: set[str] = set()
    seen_variant: set[str] = set()
    seen_semantic: set[str] = set()
    expected_credits: list[dict[str, Any]] = []
    for source in accepted:
        sid = str(source["stage_claim_id"])
        atv = str(source["variant_id"])
        semantic = str(source["semantic_key"])
        require(sid in parent_theorems, f"frontier accepted identity is not a parent theorem: {sid}")
        claim = parent_theorems[sid]
        require(atv == claim.get("variant_id"), f"frontier accepted variant does not bind theorem: {sid}")
        require(semantic in record_semantic_keys(claim), f"frontier accepted semantic does not bind theorem: {sid}")
        require(sid not in important_ids, f"frontier double-counts important quota: {sid}")
        require(sid not in seen_stage and atv not in seen_variant, f"frontier identity duplicate: {sid}")
        require(semantic not in seen_semantic, f"frontier semantic duplicate: {semantic}")
        credit = {
            "accepted_rank": len(expected_credits) + 1,
            "stage_claim_id": sid,
            "variant_id": atv,
            "semantic_key": semantic,
            "source_lane": source["lane"],
            "source_candidate_index": source["candidate_index"],
            "decision": "accept",
            "all_gates_pass": True,
            "rights_evidence": source["rights_evidence"],
            "primary_references": source["primary_references"],
            "review_binding": source["review_binding"],
            "grants_frontier_theorem_credit": True,
            "grants_new_theorem_identity_credit": False,
        }
        credit["row_sha256"] = row_hash(credit)
        expected_credits.append(credit)
        seen_stage.add(sid)
        seen_variant.add(atv)
        seen_semantic.add(semantic)
    require(MIN_FRONTIER <= len(expected_credits) <= MAX_FRONTIER, "frontier qualification misses 500--1,000 gate")
    require(document.get("accepted_credits") == expected_credits, "frontier credits are not the independent review replay")
    pending = sum(row["decision"] == "pending" for row in normalized)
    rejected = sum(row["decision"] == "reject" for row in normalized)
    counts = document.get("counts")
    require(isinstance(counts, dict), "frontier counts malformed")
    require(counts.get("review_rows") == len(normalized), "frontier review-row count drifted")
    require(counts.get("review_accepted_before_global_dedupe") == len(accepted), "frontier pre-dedupe count drifted")
    require(counts.get("accepted_additional_frontier_theorems") == len(expected_credits), "frontier accepted count drifted")
    require(counts.get("accepted_distinct_important_landmarks") == IMPORTANT_COUNT, "frontier important count drifted")
    require(counts.get("new_theorem_identity_credits") == 0 and counts.get("unsupported_importance_or_frontier_credit") == 0,
            "frontier unsupported/new identity credit is nonzero")
    require(counts.get("pending_not_credited") == pending, "frontier pending count drifted")
    require(counts.get("rejected_not_credited") == rejected, "frontier rejected count drifted")
    require(document.get("set_digests") == {
        "accepted_stage_claim_id_set_sha256": set_digest(row["stage_claim_id"] for row in expected_credits),
        "accepted_variant_id_set_sha256": set_digest(row["variant_id"] for row in expected_credits),
        "accepted_semantic_key_set_sha256": set_digest(row["semantic_key"] for row in expected_credits),
        "accepted_row_sha256_set_sha256": set_digest(row["row_sha256"] for row in expected_credits),
    }, "frontier accepted-set digests drifted")
    return document


def binding(root: Path, relative_path: Path, document: Mapping[str, Any] | None = None) -> dict[str, Any]:
    path = safe_path(root, relative_path)
    result: dict[str, Any] = {
        "path": relative_path.as_posix(),
        "file_sha256": file_sha(path),
        "size_bytes": path.stat().st_size,
    }
    if document is not None:
        authority = document.get("authority_sha256")
        if isinstance(authority, str):
            result["authority_sha256"] = authority
    return result


def expected_contract(
    root: Path, curation: Mapping[str, Any], important: Mapping[str, Any], frontier: Mapping[str, Any],
    source_authorities: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    return seal({
        "schema_version": "awesome-theorems/stage5-math-expansion-contract/5.5",
        "contract_status": "normative_qualified_strict_conjecture_append_and_quality_binding",
        "stage": "Stage5",
        "release": RELEASE,
        "review_date": REVIEW_DATE,
        "parent": {
            "release": PARENT_RELEASE,
            "release_root_sha256": PARENT_RELEASE_ROOT,
            "manifest_file_sha256": PARENT_MANIFEST_SHA256,
            "claim_catalog_file_sha256": PARENT_CATALOG_SHA256,
            "strict_ledger_file_sha256": PARENT_STRICT_SHA256,
            "catalog_records": 4_100,
            "theorem_records": 2_500,
            "open_claim_records": 1_600,
            "effective_strict_conjecture_credits": 1_000,
            "variant_high_watermark": PARENT_ATV_HIGH,
            "family_high_watermark": PARENT_ATF_HIGH,
        },
        "quantity_gates": {
            "new_strict_conjectures_min": MIN_NEW_STRICT,
            "new_strict_conjectures_max": MAX_NEW_STRICT,
            "effective_strict_conjectures_min": BASELINE_5_0_STRICT + MIN_NET_STRICT_AFTER_5_0,
            "effective_strict_conjectures_max": 2_000,
            "stage5_5_0_baseline_strict_credits": BASELINE_5_0_STRICT,
            "net_strict_increase_after_5_0_min": MIN_NET_STRICT_AFTER_5_0,
            "theorem_status_conserved": 2_500,
        },
        "quality_gates": {
            "important_theorems_exact": IMPORTANT_COUNT,
            "additional_frontier_theorems_min": MIN_FRONTIER,
            "additional_frontier_theorems_max": MAX_FRONTIER,
            "important_and_frontier_quota_sets_disjoint": True,
            "unsupported_importance_or_frontier_credit": 0,
        },
        "strict_admission_gates": [
            "complete truth-apt declarative proposition",
            "high or medium importance",
            "current-open evidence as of review",
            "source-specific rights and attribution",
            "parent and cross-source proposition-level semantic deduplication",
            "no question-to-assertion promotion",
            "accepted dense rank and immutable source binding",
        ],
        "versioned_authorities": {
            "strict_conjecture_curation": binding(root, CURATION_REL, curation),
            "important_theorem_inventory": binding(root, IMPORTANT_REL, important),
            "frontier_theorem_qualification": binding(root, FRONTIER_REL, frontier),
            "first_class_source_review_allowlist": copy.deepcopy(source_authorities),
        },
        "identity_allocation": {
            "append_only": True,
            "one_new_family_sense_variant_occurrence_per_new_strict_identity": True,
            "first_new_ATF": PARENT_ATF_HIGH + 1,
            "first_new_ATV_ATS_ATO_S5": PARENT_ATV_HIGH + 1,
            "parent_prefix_rewrite_forbidden": True,
        },
        "release_layout": {
            "root": RELEASE_REL.as_posix(),
            "manifest_name": MANIFEST_NAME,
            "non_manifest_artifacts": list(RELEASE_FILES),
            "manifest_excluded_from_release_root": True,
        },
        "publication": {
            "compare_and_swap_parent_pointer_sha256": PARENT_CURRENT_SHA256,
            "write_does_not_publish": True,
            "publish_current_requires_authenticated_5_4_or_idempotent_5_5": True,
            "independent_checker_path": "Docs/catalog/v5/tools/check_math_catalog_v5_5.py",
            "independent_acceptance_receipt_path": "Docs/catalog/v5/receipts/V5_5_Independent_Acceptance_Receipt.json",
            "independent_receipt_and_live_prepublish_replay_required": True,
        },
    })


def check_contract(
    root: Path, curation: Mapping[str, Any], important: Mapping[str, Any], frontier: Mapping[str, Any],
    source_authorities: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    observed = load_json(root, CONTRACT_REL)
    verify_seal(observed, "5.5 contract")
    expected = expected_contract(root, curation, important, frontier, source_authorities)
    require(observed == expected, "5.5 contract is not the independently reconstructed contract")
    return observed


def allocation_sha(row: Mapping[str, Any], ordinal: int) -> str:
    return digest(canonical({
        "release": RELEASE,
        "ordinal": ordinal,
        "candidate_key": row["candidate_key"],
        "semantic_key": row["semantic_key"],
        "source_kind": row["source_kind"],
        "source_record_key": row["source_record_key"],
        "curation_row_sha256": row["row_sha256"],
    }))


def statement_payload(row: Mapping[str, Any]) -> dict[str, Any]:
    statement = row["_statement"]
    context = row.get("exact_claim_context")
    summary = row["_summary"]
    return {
        "language": row.get("statement_language", "en_or_mathematical_notation"),
        "representation": row["statement_representation"],
        "exact_claim_text": statement,
        "exact_claim_context": context,
        "semantic_summary": summary,
        "statement_sha256": digest(canonical({"claim": statement, "context": context})),
        "summary_sha256": digest(summary.encode("utf-8")),
        "completeness": "reviewed_context_complete",
    }


ORIGIN_CLAIM_FIELDS = frozenset({
    "schema_version", "record_role", "release_id", "origin_stage", "origin_release",
    "stage_claim_id", "family_id", "sense_id", "variant_id", "occurrence_id",
    "owner_domain", "membership_domains", "category", "claim_kind", "current_claim_kind",
    "historical_kind", "material_status", "lifecycle", "truth_apt", "atomicity",
    "display_name", "aliases", "curation_key", "semantic_key", "semantic_payload_sha256",
    "mathematical_statement", "classification", "importance", "frontier", "status_detail",
    "source_id", "source_locator", "source_record_key", "rights", "dedupe",
    "curator_disposition", "allocation", "provenance", "lineage", "content_payload_sha256",
    "catalog_record_sha256",
})

ORIGIN_STRICT_CREDIT_FIELDS = frozenset({
    "stage_claim_id", "variant_id", "semantic_key", "origin_release",
    "credit_source_branch", "evidence_sha256", "catalog_record_sha256",
    "statement_sha256", "curation_row_sha256", "source_row_sha256",
    "source_authority_file_sha256", "allocation_request_sha256",
    "grants_strict_conjecture_credit", "row_sha256",
})


def expected_claim(root: Path, row: Mapping[str, Any], rank: int, curation: Mapping[str, Any]) -> dict[str, Any]:
    ordinal = PARENT_ATV_HIGH + rank
    family_ordinal = PARENT_ATF_HIGH + rank
    atv = f"ATV-{ordinal:08d}"
    ato = f"ATO-{ordinal:08d}"
    ats = f"ATS-{ordinal:08d}"
    atf = f"ATF-{family_ordinal:08d}"
    sid = f"S5-CLM-{ordinal:08d}"
    request = allocation_sha(row, ordinal)
    statement = statement_payload(row)
    semantic_payload = digest(canonical({
        "semantic_key": row["semantic_key"],
        "statement_sha256": statement["statement_sha256"],
        "source_kind": row["source_kind"],
    }))
    display = row.get("display_name") or row["semantic_summary"]
    require_string(display, f"accepted rank {rank} display name")
    source_id = f"SRC-MATH-V5-5-{str(row['source_kind']).upper().replace('_', '-')}"
    result: dict[str, Any] = {
        "schema_version": "awesome-theorems/stage5-math-claim-record/5.5",
        "record_role": "claim",
        "release_id": RELEASE,
        "origin_stage": "Stage5",
        "origin_release": RELEASE,
        "stage_claim_id": sid,
        "family_id": atf,
        "sense_id": ats,
        "variant_id": atv,
        "occurrence_id": ato,
        "owner_domain": "mathematics",
        "membership_domains": ["mathematics"],
        "category": "open_claim",
        "claim_kind": "conjecture",
        "current_claim_kind": "conjecture",
        "historical_kind": "conjecture",
        "material_status": "open",
        "lifecycle": "active",
        "truth_apt": True,
        "atomicity": "atomic" if row["atomicity"] == "single" else "source_named_compound",
        "display_name": display,
        "aliases": list(row.get("aliases", [])) if isinstance(row.get("aliases", []), list) else [],
        "curation_key": f"strict-v5.5/{row['source_kind']}/{row['candidate_key']}",
        "semantic_key": row["semantic_key"],
        "semantic_payload_sha256": semantic_payload,
        "mathematical_statement": statement,
        "classification": copy.deepcopy(row["classification"]),
        "importance": {
            "tier": row["importance_tier"],
            "basis": row.get("importance_basis", "source-specific human review"),
            "independently_reviewed": True,
        },
        "frontier": {
            "class": "current_open_research_conjecture",
            "as_of": REVIEW_DATE,
            "evidence": copy.deepcopy(row["current_status_evidence"]),
            "independently_reviewed": True,
        },
        "status_detail": {
            "status_as_of": REVIEW_DATE,
            "basis": "curation accepted current-open evidence",
            "resolution_criterion": "prove or refute the exact reviewed proposition",
            "evidence": copy.deepcopy(row["current_status_evidence"]),
        },
        "source_id": source_id,
        "source_locator": copy.deepcopy(row["source_binding"]),
        "source_record_key": row["source_record_key"],
        "rights": copy.deepcopy(row["rights"]),
        "dedupe": {
            "semantic_key": row["semantic_key"],
            "parent_semantic_unique": True,
            "cross_source_semantic_unique": True,
            "duplicate_grants_quota": False,
            "candidate_atv_ids": [],
            "no_evidence_or_status_inheritance": True,
            "curation_finding": copy.deepcopy(row["dedupe"]),
        },
        "curator_disposition": {
            "disposition": "accepted_new_strict_open_claim",
            "accepted_rank": rank,
            "candidate_key": row["candidate_key"],
            "source_kind": row["source_kind"],
            "source_record_key": row["source_record_key"],
            "grants_release_entry": True,
            "grants_strict_conjecture_credit": True,
            "target_s5_id": sid,
            "target_variant_id": atv,
            "ledger_path": CURATION_REL.as_posix(),
            "ledger_file_sha256": file_sha(safe_path(root, CURATION_REL)),
            "ledger_authority_sha256": curation["authority_sha256"],
            "ledger_row_sha256": row["row_sha256"],
            "source_review_path": row["source_binding"]["path"],
            "source_review_file_sha256": row["source_binding"]["file_sha256"],
            "source_review_row_sha256": row["source_binding"]["source_row_sha256"],
            "source_authority_file_sha256": row["source_binding"]["authority_receipt"]["file_sha256"],
        },
        "allocation": {
            "transaction_id": f"S5-ALLOC-{ordinal:08d}",
            "allocation_request_sha256": request,
            "append_only": True,
            "family_action": "new_family",
            "parent_release_root_sha256": PARENT_RELEASE_ROOT,
        },
        "provenance": {
            "source_kind": row["source_kind"],
            "source_record_key": row["source_record_key"],
            "source_binding": copy.deepcopy(row["source_binding"]),
            "curation_path": CURATION_REL.as_posix(),
            "curation_authority_sha256": curation["authority_sha256"],
            "curation_row_sha256": row["row_sha256"],
            "question_to_assertion_promotion_performed": False,
        },
        "lineage": [],
    }
    result["content_payload_sha256"] = digest(canonical({
        "statement": statement,
        "status": result["status_detail"],
        "rights": result["rights"],
        "dedupe": result["dedupe"],
    }))
    result["catalog_record_sha256"] = hash_without(result, "catalog_record_sha256")
    require(set(result) == ORIGIN_CLAIM_FIELDS, "independent origin claim schema is not closed")
    return result


def authoritative_inputs(
    root: Path, contract: Mapping[str, Any], curation: Mapping[str, Any],
    important: Mapping[str, Any], frontier: Mapping[str, Any],
    parent: Mapping[str, Mapping[str, Any]], source_authorities: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "contract": binding(root, CONTRACT_REL, contract),
        "strict_conjecture_curation": binding(root, CURATION_REL, curation),
        "important_theorem_inventory": binding(root, IMPORTANT_REL, important),
        "frontier_theorem_qualification": binding(root, FRONTIER_REL, frontier),
        "first_class_source_review_allowlist": copy.deepcopy(source_authorities),
        "parent_release": {
            "release": PARENT_RELEASE,
            "release_root_sha256": PARENT_RELEASE_ROOT,
            "manifest_file_sha256": PARENT_MANIFEST_SHA256,
            "manifest_authority_sha256": parent[MANIFEST_NAME]["authority_sha256"],
            "catalog_file_sha256": PARENT_CATALOG_SHA256,
            "strict_ledger_file_sha256": PARENT_STRICT_SHA256,
        },
    }


def registry_additions(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    families: list[dict[str, Any]] = []
    senses: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    for row in rows:
        request = row["allocation"]["allocation_request_sha256"]
        families.append({
            "family_id": row["family_id"],
            "curation_key": row["curation_key"],
            "display_titles": list(dict.fromkeys([row["display_name"], *row["aliases"]])),
            "member_occurrence_ids": [row["occurrence_id"]],
            "historical_member_occurrence_ids": [row["occurrence_id"]],
            "idempotency_request_sha256": request,
            "identity_state": "stage5_reviewed_strict_conjecture_family",
            "lifecycle": "current",
            "semantic_equivalence_asserted": True,
        })
        senses.append({
            "sense_id": row["sense_id"], "family_id": row["family_id"],
            "bootstrap_occurrence_id": row["occurrence_id"], "curation_key": row["curation_key"],
            "idempotency_request_sha256": request,
            "identity_state": "stage5_reviewed_strict_conjecture_sense", "lifecycle": "current",
        })
        variants.append({
            "variant_id": row["variant_id"], "sense_id": row["sense_id"],
            "bootstrap_occurrence_id": row["occurrence_id"], "curation_key": row["curation_key"],
            "idempotency_request_sha256": request,
            "semantic_payload_sha256": row["semantic_payload_sha256"],
            "identity_state": "stage5_reviewed_strict_conjecture_variant", "lifecycle": "current",
        })
    return families, senses, variants


def strict_credit(row: Mapping[str, Any]) -> dict[str, Any]:
    credit = {
        "stage_claim_id": row["stage_claim_id"], "variant_id": row["variant_id"],
        "semantic_key": row["semantic_key"], "origin_release": RELEASE,
        "credit_source_branch": f"origin_5_5_{row['provenance']['source_kind']}_reviewed_assertion",
        "evidence_sha256": row["content_payload_sha256"],
        "catalog_record_sha256": row["catalog_record_sha256"],
        "statement_sha256": row["mathematical_statement"]["statement_sha256"],
        "curation_row_sha256": row["curator_disposition"]["ledger_row_sha256"],
        "source_row_sha256": row["source_locator"]["source_row_sha256"],
        "source_authority_file_sha256": row["source_locator"]["authority_receipt"]["file_sha256"],
        "allocation_request_sha256": row["allocation"]["allocation_request_sha256"],
        "grants_strict_conjecture_credit": True,
    }
    credit["row_sha256"] = row_hash(credit)
    require(set(credit) == ORIGIN_STRICT_CREDIT_FIELDS, "independent strict credit schema is not closed")
    return credit


def expected_artifacts(
    parent: Mapping[str, Mapping[str, Any]], rows: Sequence[dict[str, Any]],
    inputs: Mapping[str, Any], frontier: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    count = len(rows)
    parent_catalog = parent["Claim_Catalog.json"]
    records = copy.deepcopy(parent_catalog["records"]) + copy.deepcopy(list(rows))
    catalog = seal({
        "schema_version": "awesome-theorems/stage5-claim-catalog/5.5",
        "artifact": "Claim_Catalog.json", "release": RELEASE,
        "catalog_scope": parent_catalog["catalog_scope"],
        "authoritative_inputs": copy.deepcopy(inputs),
        "quality_qualification": {
            "important_theorems": IMPORTANT_COUNT,
            "additional_frontier_theorems": len(frontier["accepted_credits"]),
            "unsupported_credit": 0,
        },
        "origin_5_5_closed_schema": {
            "closed": True,
            "record_keys": sorted(ORIGIN_CLAIM_FIELDS),
            "record_hash_field": "catalog_record_sha256",
            "record_hash_rule": "SHA-256 of canonical JSON after omitting catalog_record_sha256",
            "origin_records": count,
        },
        "counts": {
            "records": 4_100 + count, "origin_theorems": 0,
            "origin_open_claims": count, "origin_strict_conjectures": count,
            "cumulative_theorems": 2_500, "cumulative_open_claims": 1_600 + count,
            "effective_strict_conjectures": 1_000 + count,
        },
        "records": records,
    })
    parent_registry = parent["Claim_ID_Registry.json"]
    families, senses, variants = registry_additions(rows)
    allocation_policy = copy.deepcopy(parent_registry["allocation_policy"])
    allocation_policy.update({
        "release_5_5_first_new_atv_ordinal": PARENT_ATV_HIGH + 1,
        "release_5_5_new_family_first_atf_ordinal": PARENT_ATF_HIGH + 1,
    })
    registry = seal({
        "schema_version": "awesome-theorems/claim-id-registry/5.5",
        "artifact": "Claim_ID_Registry.json", "release": RELEASE,
        "parent_registry_authority_sha256": parent_registry["authority_sha256"],
        "baseline_registry_authority_sha256": parent_registry["baseline_registry_authority_sha256"],
        "authoritative_inputs": copy.deepcopy(inputs), "allocation_policy": allocation_policy,
        "namespace_high_watermarks": {
            "ATF": PARENT_ATF_HIGH + count, "ATO": PARENT_ATV_HIGH + count,
            "ATS": PARENT_ATV_HIGH + count, "ATV": PARENT_ATV_HIGH + count,
        },
        "families": copy.deepcopy(parent_registry["families"]) + families,
        "senses": copy.deepcopy(parent_registry["senses"]) + senses,
        "variants": copy.deepcopy(parent_registry["variants"]) + variants,
        "legacy_aliases": copy.deepcopy(parent_registry["legacy_aliases"]),
        "redirects": copy.deepcopy(parent_registry["redirects"]),
        "splits": copy.deepcopy(parent_registry["splits"]),
        "family_membership_extensions": copy.deepcopy(parent_registry["family_membership_extensions"]),
        "counts": {
            "families": len(parent_registry["families"]) + count,
            "senses": len(parent_registry["senses"]) + count,
            "variants": len(parent_registry["variants"]) + count,
            "stage4_variants": parent_registry["counts"]["stage4_variants"],
            "stage5_additions": parent_registry["counts"]["stage5_additions"] + count,
            "legacy_aliases": len(parent_registry["legacy_aliases"]),
            "redirects": len(parent_registry["redirects"]), "splits": len(parent_registry["splits"]),
        },
    })
    parent_stage = parent["Stage5_Claim_ID_Registry.json"]
    mappings = copy.deepcopy(parent_stage["mappings"]) + [{
        "ordinal": int(ATV_RE.fullmatch(row["variant_id"]).group(1)),
        "variant_id": row["variant_id"], "predecessor_stage_claim_id": None,
        "stage_claim_id": row["stage_claim_id"], "lifecycle": "current",
    } for row in rows]
    stage_registry = seal({
        "schema_version": "awesome-theorems/stage5-claim-id-registry/5.5",
        "artifact": "Stage5_Claim_ID_Registry.json", "release": RELEASE,
        "authoritative_inputs": copy.deepcopy(inputs),
        "numbering_policy": parent_stage["numbering_policy"],
        "counts": {"mappings": len(mappings)}, "mappings": mappings,
    })
    parent_migration = parent["Migration_v4_to_v5.json"]
    migrations = copy.deepcopy(parent_migration["migrations"]) + [{
        "ordinal": int(ATV_RE.fullmatch(row["variant_id"]).group(1)),
        "variant_id": row["variant_id"], "v4_variant_id": None, "s4_claim_id": None,
        "stage_claim_id": row["stage_claim_id"], "migration_action": "new_stage5_allocation",
        "predecessor_record_sha256": None,
        "current_resolution": {
            "kind": "current", "terminal_atv_ids": [row["variant_id"]],
            "terminal_s5_ids": [row["stage_claim_id"]], "default_child": None,
            "evidence_inherited": False,
        },
    } for row in rows]
    migration = seal({
        "schema_version": "awesome-theorems/migration-v4-to-v5/5.5",
        "artifact": "Migration_v4_to_v5.json", "release": RELEASE,
        "authoritative_inputs": copy.deepcopy(inputs),
        "v4_import_receipt": copy.deepcopy(parent_migration["v4_import_receipt"]),
        "counts": {
            "historical_bindings": parent_migration["counts"]["historical_bindings"],
            "new_allocations": parent_migration["counts"]["new_allocations"] + count,
            "migrations": len(migrations),
        }, "migrations": migrations,
    })
    theorem_rows = [row for row in records if theorem_predicate(row)]
    open_rows = [row for row in records if open_predicate(row)]
    theorem = seal({
        "schema_version": "awesome-theorems/stage5-query-projection/5.5",
        "artifact": "Theorem_List.json", "release": RELEASE,
        "authoritative_inputs": copy.deepcopy(inputs),
        "query": "pure predicate over Claim_Catalog.json; records copied byte-semantically",
        "stage_claim_ids": [row["stage_claim_id"] for row in theorem_rows],
        "counts": {"records": len(theorem_rows)}, "records": theorem_rows,
    })
    open_list = seal({
        "schema_version": "awesome-theorems/stage5-query-projection/5.5",
        "artifact": "Open_Claim_List.json", "release": RELEASE,
        "authoritative_inputs": copy.deepcopy(inputs),
        "query": "pure predicate over Claim_Catalog.json; records copied byte-semantically",
        "stage_claim_ids": [row["stage_claim_id"] for row in open_rows],
        "counts": {"records": len(open_rows)}, "records": open_rows,
    })
    parent_coverage = parent["Coverage_Ledger.json"]
    additions = [{
        "candidate_key": f"strict-v5.5:{row['curator_disposition']['candidate_key']}",
        "source_id": row["source_id"], "source_record_id": row["source_record_key"],
        "semantic_key": row["semantic_key"], "disposition": "accepted_new_strict_open_claim",
        "reason_code": "all_strict_release_gates_pass",
        "accepted_rank": row["curator_disposition"]["accepted_rank"],
        "target_variant_id": row["variant_id"], "target_s5_id": row["stage_claim_id"],
        "catalog_record_sha256": row["catalog_record_sha256"],
        "grants_catalog_entry": True, "grants_strict_conjecture_credit": True,
        "origin_release": RELEASE,
        "curation_row_sha256": row["curator_disposition"]["ledger_row_sha256"],
        "source_review_row_sha256": row["source_locator"]["source_row_sha256"],
        "source_authority_file_sha256": row["source_locator"]["authority_receipt"]["file_sha256"],
        "supersedes_candidate_key": None, "transition_from_disposition": "new_source_candidate",
    } for row in rows]
    coverage_rows = copy.deepcopy(parent_coverage["candidate_dispositions"]) + additions
    by_msc: dict[str, list[Mapping[str, Any]]] = {}
    unassigned_msc: list[Mapping[str, Any]] = []
    for claim in rows:
        primary = claim["classification"]["primary_msc_top_class"]
        if primary is None:
            unassigned_msc.append(claim)
        else:
            by_msc.setdefault(primary, []).append(claim)
    msc_rows: list[dict[str, Any]] = []
    for parent_row in parent_coverage["msc_coverage"]:
        projected = copy.deepcopy(parent_row)
        code = str(projected["msc_top_class"])
        classified_additions = by_msc.pop(code, [])
        new_ids = sorted(claim["stage_claim_id"] for claim in classified_additions)
        projected["current_open_s5_ids"] = sorted([*projected["current_open_s5_ids"], *new_ids])
        projected["origin_open_s5_ids"] = new_ids
        projected["origin_theorem_s5_ids"] = []
        if classified_additions:
            projected["source_ids"] = sorted(set(projected["source_ids"]) | {
                claim["source_id"] for claim in classified_additions
            })
        projected["classification_basis_counts"]["independent_review"] += len(classified_additions)
        projected["counts"]["current_theorems"] = len(projected["current_theorem_s5_ids"])
        projected["counts"]["current_open"] = len(projected["current_open_s5_ids"])
        projected["counts"]["origin_theorems"] = 0
        projected["counts"]["origin_open"] = len(new_ids)
        projected["counts"]["open_reserve"] = len(projected["open_reserve_candidate_keys"])
        classified = sum(projected["counts"][key] for key in ("current_theorems", "current_open", "open_reserve"))
        if classified == 0:
            projected["scarcity"] = "zero"
            projected["scarcity_reason"] = "No current or open-reserve member has this primary source annotation."
        elif classified < 10:
            projected["scarcity"] = "thin"
            projected["scarcity_reason"] = "Fewer than ten current-plus-reserve members have this primary class."
        else:
            projected["scarcity"] = "adequate_in_source_inventory"
            projected["scarcity_reason"] = "At least ten current-plus-reserve members have this primary class."
        msc_rows.append(projected)
    require(not by_msc, f"origin claims use unknown MSC roots: {sorted(by_msc)}")
    coverage = seal({
        "schema_version": "awesome-theorems/stage5-coverage-ledger/5.5", "release": RELEASE,
        "authoritative_inputs": copy.deepcopy(inputs),
        "effective_state_policy": {
            "identity_fields": ["source_id", "source_record_id"],
            "supersession_field": "supersedes_candidate_key",
            "effective_rule": "A candidate row is effective exactly when no later appended row names its candidate_key in supersedes_candidate_key.",
            "historical_parent_rows_are_immutable": True,
            "release_5_4_rows_supersede_exact_5_3_residual_rows": True,
            "release_5_5_rows_are_new_identities_without_supersession": True,
        },
        "msc_projection_policy": {
            "primary_field": "classification.primary_msc_top_class",
            "assigned_rows_project_into_exactly_one_top_class": True,
            "unassigned_rows_are_counted_but_not_fabricated_into_a_class": True,
            "origin_open_ids_are_release_local": True,
        },
        "candidate_dispositions": coverage_rows,
        "msc_coverage": msc_rows,
        "counts": {
            "candidate_dispositions": len(coverage_rows),
            "msc_coverage": len(msc_rows),
            "origin_5_5_candidates": count,
            "origin_5_5_accepted_new_strict_conjectures": count,
            "origin_5_5_pending_or_rejected_release_rows": 0,
            "origin_5_5_msc_assigned": count - len(unassigned_msc),
            "origin_5_5_msc_unassigned": len(unassigned_msc),
        },
    })
    parent_strict = parent["Strict_Conjecture_Ledger.json"]
    new_credits = [strict_credit(row) for row in rows]
    credits = copy.deepcopy(parent_strict["strict_credits"]) + new_credits
    strict = seal({
        "schema_version": "awesome-theorems/stage5-strict-conjecture-ledger/5.5", "release": RELEASE,
        "parent_release_root_sha256": PARENT_RELEASE_ROOT,
        "parent_strict_ledger_file_sha256": PARENT_STRICT_SHA256,
        "parent_strict_ledger_authority_sha256": parent_strict["authority_sha256"],
        "origin_5_5_closed_credit_schema": {
            "closed": True,
            "credit_keys": sorted(ORIGIN_STRICT_CREDIT_FIELDS),
            "row_hash_field": "row_sha256",
            "row_hash_rule": "SHA-256 of canonical JSON after omitting row_sha256",
            "origin_credits": len(new_credits),
        },
        "strict_credits": credits,
        "credit_corrections": copy.deepcopy(parent_strict["credit_corrections"]),
        "counts": {
            "credit_corrections": len(parent_strict["credit_corrections"]),
            "effective_parent_credits": 1_000, "origin_5_2_credits": 600,
            "origin_5_5_credits": len(new_credits), "effective_strict_credits": len(credits),
            "stage5_5_0_baseline_strict_credits": BASELINE_5_0_STRICT,
            "net_strict_increase_after_5_0": len(credits) - BASELINE_5_0_STRICT,
        },
        "set_digests": {
            "effective_s5_id_set_sha256": set_digest(row["stage_claim_id"] for row in credits),
            "effective_variant_id_set_sha256": set_digest(row["variant_id"] for row in credits),
            "origin_5_5_s5_id_set_sha256": set_digest(row["stage_claim_id"] for row in new_credits),
            "origin_5_5_semantic_key_set_sha256": set_digest(row["semantic_key"] for row in new_credits),
        },
    })
    return {
        "Claim_Catalog.json": catalog, "Claim_ID_Registry.json": registry,
        "Stage5_Claim_ID_Registry.json": stage_registry, "Migration_v4_to_v5.json": migration,
        "Theorem_List.json": theorem, "Open_Claim_List.json": open_list,
        "Coverage_Ledger.json": coverage, "Strict_Conjecture_Ledger.json": strict,
    }


def validate_origin_rows(rows: Sequence[Mapping[str, Any]], expected: Sequence[Mapping[str, Any]]) -> None:
    require(len(rows) == len(expected), "origin 5.5 row denominator differs")
    for index, (observed, wanted) in enumerate(zip(rows, expected, strict=True)):
        require(set(observed) == ORIGIN_CLAIM_FIELDS, f"origin claim[{index}] top-level schema is not closed")
        require(observed == wanted, f"origin claim[{index}] differs from independent source replay")


def validate_parent_prefix(child: Sequence[Mapping[str, Any]], parent: Sequence[Mapping[str, Any]], label: str) -> None:
    require(len(child) >= len(parent) and list(child[:len(parent)]) == list(parent), f"{label} parent prefix changed")


def validate_dense_origin_ids(new_rows: Sequence[Mapping[str, Any]]) -> None:
    expected_atv = [f"ATV-{value:08d}" for value in range(PARENT_ATV_HIGH + 1, PARENT_ATV_HIGH + len(new_rows) + 1)]
    expected_atf = [f"ATF-{value:08d}" for value in range(PARENT_ATF_HIGH + 1, PARENT_ATF_HIGH + len(new_rows) + 1)]
    expected_s5 = [value.replace("ATV-", "S5-CLM-") for value in expected_atv]
    require([row.get("variant_id") for row in new_rows] == expected_atv, "origin ATV IDs contain a gap/reorder")
    require([row.get("family_id") for row in new_rows] == expected_atf, "origin ATF IDs contain a gap/reorder")
    require([row.get("stage_claim_id") for row in new_rows] == expected_s5, "origin S5 IDs contain a gap/reorder")


def validate_strict_catalog_symmetry(documents: Mapping[str, Mapping[str, Any]], new_count: int) -> None:
    catalog_rows = documents["Claim_Catalog.json"]["records"][4_100:]
    strict_rows = documents["Strict_Conjecture_Ledger.json"]["strict_credits"]
    origin_strict = strict_rows[1_000:]
    open_ids = documents["Open_Claim_List.json"]["stage_claim_ids"][1_600:]
    catalog_ids = [row["stage_claim_id"] for row in catalog_rows]
    strict_ids = [row["stage_claim_id"] for row in origin_strict]
    require(len(catalog_ids) == len(strict_ids) == len(open_ids) == new_count,
            "strict/catalog/open origin-5.5 denominators are asymmetric")
    require(set(catalog_ids) == set(strict_ids) == set(open_ids) and len(set(catalog_ids)) == new_count,
            "strict/catalog/open origin-5.5 identity sets are asymmetric")
    for field in ("stage_claim_id", "variant_id", "semantic_key"):
        values = [row.get(field) for row in strict_rows]
        require(len(values) == len(set(values)), f"strict ledger duplicates {field}")


def validate_manifest_inventory_shape(manifest: Mapping[str, Any]) -> None:
    rows = manifest.get("artifacts")
    require(isinstance(rows, list) and len(rows) == len(RELEASE_FILES), "manifest artifact denominator drifted")
    require(all(isinstance(row, dict) and set(row) == {"path", "sha256", "size_bytes", "row_count"} for row in rows),
            "manifest artifact row closure drifted")
    require([row["path"] for row in rows] == sorted(RELEASE_FILES), "manifest artifact set/order drifted")


def validate_stage6_parent_interface(documents: Mapping[str, Mapping[str, Any]]) -> None:
    catalog = documents["Claim_Catalog.json"]
    registry = documents["Claim_ID_Registry.json"]
    stage = documents["Stage5_Claim_ID_Registry.json"]
    migration = documents["Migration_v4_to_v5.json"]
    manifest = documents[MANIFEST_NAME]
    expected_schemas = {
        "Claim_Catalog.json": "awesome-theorems/stage5-claim-catalog/5.5",
        "Claim_ID_Registry.json": "awesome-theorems/claim-id-registry/5.5",
        "Stage5_Claim_ID_Registry.json": "awesome-theorems/stage5-claim-id-registry/5.5",
        "Migration_v4_to_v5.json": "awesome-theorems/migration-v4-to-v5/5.5",
        MANIFEST_NAME: "awesome-theorems/stage5-release-manifest/5.5",
    }
    for name, schema in expected_schemas.items():
        require(documents[name].get("schema_version") == schema, f"Stage6 adapter schema mismatch: {name}")
        require(documents[name].get("release") == RELEASE, f"Stage6 adapter release mismatch: {name}")
    for name in ("Claim_Catalog.json", "Claim_ID_Registry.json", "Stage5_Claim_ID_Registry.json", "Migration_v4_to_v5.json"):
        require(documents[name].get("artifact") == name, f"Stage6 adapter artifact mismatch: {name}")
    families = registry.get("families")
    senses = registry.get("senses")
    variants = registry.get("variants")
    mappings = stage.get("mappings")
    migrations = migration.get("migrations")
    require(all(isinstance(value, list) for value in (families, senses, variants, mappings, migrations)), "Stage6 identity arrays malformed")

    def unique(
        rows: Sequence[Mapping[str, Any]], key: str, pattern: re.Pattern[str], label: str,
        *, require_request: bool = False,
    ) -> dict[str, Mapping[str, Any]]:
        result: dict[str, Mapping[str, Any]] = {}
        requests: set[str] = set()
        for index, row in enumerate(rows):
            require(isinstance(row, dict), f"{label}[{index}] malformed")
            identifier = require_string(row.get(key), f"{label}[{index}].{key}", pattern)
            require(identifier not in result, f"{label} duplicates {identifier}")
            result[identifier] = row
            if require_request:
                request = require_string(row.get("idempotency_request_sha256"), f"{label}[{index}] idempotency", SHA_RE)
                require(request not in requests, f"{label} duplicates canonical identity request")
                requests.add(request)
        return result

    family_by_id = unique(families, "family_id", ATF_RE, "families", require_request=True)
    sense_by_id = unique(senses, "sense_id", ATS_RE, "senses", require_request=True)
    variant_by_id = unique(variants, "variant_id", ATV_RE, "variants", require_request=True)
    mapping_by_variant = unique(mappings, "variant_id", ATV_RE, "stage mappings")
    migration_by_variant = unique(migrations, "variant_id", ATV_RE, "migrations")
    require(set(mapping_by_variant) == set(variant_by_id) == set(migration_by_variant), "Stage6 adapter does not cover every variant")
    stage_ids: set[str] = set()
    occurrences: set[str] = set()
    for sense_id, row in sense_by_id.items():
        require(row.get("family_id") in family_by_id, f"sense {sense_id} references unknown family")
    for variant_id, row in variant_by_id.items():
        require(row.get("sense_id") in sense_by_id, f"variant {variant_id} references unknown sense")
        occurrence = require_string(row.get("bootstrap_occurrence_id"), f"variant {variant_id} occurrence", ATO_RE)
        require(occurrence not in occurrences, f"duplicate bootstrap occurrence: {occurrence}")
        occurrences.add(occurrence)
        mapping = mapping_by_variant[variant_id]
        sid = require_string(mapping.get("stage_claim_id"), f"mapping {variant_id} S5", S5_RE)
        require(sid not in stage_ids, f"duplicate Stage5 claim ID: {sid}")
        stage_ids.add(sid)
        migrated = migration_by_variant[variant_id]
        require(migrated.get("stage_claim_id") == sid, f"migration/mapping S5 mismatch: {variant_id}")
        require(migrated.get("s4_claim_id") == mapping.get("predecessor_stage_claim_id"), f"migration/mapping S4 mismatch: {variant_id}")
        resolution = migrated.get("current_resolution")
        require(isinstance(resolution, dict) and resolution.get("kind") in {"current", "redirect", "split"}, f"migration resolution malformed: {variant_id}")
        terminal_atv = resolution.get("terminal_atv_ids")
        terminal_s5 = resolution.get("terminal_s5_ids")
        require(isinstance(terminal_atv, list) and isinstance(terminal_s5, list)
                and terminal_atv and len(terminal_atv) == len(terminal_s5),
                f"migration terminal resolution malformed: {variant_id}")
        for terminal_variant, terminal_stage in zip(terminal_atv, terminal_s5, strict=True):
            require(terminal_variant in variant_by_id and terminal_stage in stage_ids | {
                mapping_by_variant[value].get("stage_claim_id") for value in variant_by_id
            }, f"migration terminal target unknown: {variant_id}")
        require(resolution.get("evidence_inherited") is False and resolution.get("default_child") is None,
                f"migration inherits evidence/default child: {variant_id}")
    high = registry.get("namespace_high_watermarks")
    require(isinstance(high, dict), "namespace high-watermarks missing")
    for namespace, index, rows in (
        ("ATF", 4, family_by_id), ("ATS", 4, sense_by_id), ("ATV", 4, variant_by_id)
    ):
        observed = max(int(identifier[index:]) for identifier in rows)
        require(high.get(namespace) == observed, f"{namespace} high-watermark drifted")
    require(high.get("ATO") == max(int(identifier[4:]) for identifier in occurrences), "ATO high-watermark drifted")
    catalog_variants: set[str] = set()
    catalog_occurrences: set[str] = set()
    mapping_by_stage = {row["stage_claim_id"]: row for row in mappings}
    require(len(mapping_by_stage) == len(mappings), "stage mapping IDs not unique")
    for index, row in enumerate(catalog.get("records", [])):
        atv = require_string(row.get("variant_id"), f"catalog[{index}] variant", ATV_RE)
        ato = require_string(row.get("occurrence_id"), f"catalog[{index}] occurrence", ATO_RE)
        sid = require_string(row.get("stage_claim_id"), f"catalog[{index}] stage", S5_RE)
        require(atv in variant_by_id and variant_by_id[atv].get("bootstrap_occurrence_id") == ato,
                f"catalog[{index}] occurrence/variant graph mismatch")
        require(sid in mapping_by_stage and mapping_by_stage[sid].get("variant_id") == atv,
                f"catalog[{index}] stage/variant graph mismatch")
        require(atv not in catalog_variants and ato not in catalog_occurrences,
                f"catalog[{index}] variant/occurrence duplicate")
        catalog_variants.add(atv)
        catalog_occurrences.add(ato)
    manifest_paths = {row.get("path") for row in manifest.get("artifacts", []) if isinstance(row, dict)}
    require(manifest_paths == set(RELEASE_FILES), "Stage6 adapter manifest is not the complete 5.5 interface")


def expected_manifest(
    root: Path, artifacts: Mapping[str, Mapping[str, Any]], inputs: Mapping[str, Any],
    curation: Mapping[str, Any], important: Mapping[str, Any], frontier: Mapping[str, Any],
) -> dict[str, Any]:
    inventory = []
    for name in sorted(RELEASE_FILES):
        payload = encoded(artifacts[name])
        inventory.append({
            "path": name, "sha256": digest(payload), "size_bytes": len(payload),
            "row_count": primary_rows(artifacts[name]),
        })
    root_sha = release_root(inventory)
    strict = artifacts["Strict_Conjecture_Ledger.json"]
    accepted_count = sum(row.get("decision") == "accept" for row in curation["candidate_dispositions"])
    return seal({
        "schema_version": "awesome-theorems/stage5-release-manifest/5.5",
        "release": RELEASE, "parent_release": PARENT_RELEASE,
        "parent_release_root_sha256": PARENT_RELEASE_ROOT,
        "release_root_sha256": root_sha,
        "authoritative_inputs": copy.deepcopy(inputs),
        "quality_qualification": {
            "important_theorem_inventory_authority_sha256": important["authority_sha256"],
            "accepted_distinct_important_landmarks": IMPORTANT_COUNT,
            "frontier_theorem_qualification_authority_sha256": frontier["authority_sha256"],
            "accepted_additional_frontier_theorems": len(frontier["accepted_credits"]),
            "unsupported_importance_or_frontier_credit": 0,
        },
        "strict_credit_binding": {
            "path": "Strict_Conjecture_Ledger.json",
            "file_sha256": digest(encoded(strict)), "authority_sha256": strict["authority_sha256"],
            "effective_s5_id_set_sha256": strict["set_digests"]["effective_s5_id_set_sha256"],
            "effective_variant_id_set_sha256": strict["set_digests"]["effective_variant_id_set_sha256"],
        },
        "accepted_set_digests": {
            "new_candidate_key_set_sha256": curation["set_digests"]["accepted_candidate_key_set_sha256"],
            "new_semantic_key_set_sha256": curation["set_digests"]["accepted_semantic_key_set_sha256"],
            "new_catalog_record_set_sha256": set_digest(
                row["catalog_record_sha256"] for row in artifacts["Claim_Catalog.json"]["records"]
                if row.get("origin_release") == RELEASE
            ),
            "new_strict_credit_row_set_sha256": set_digest(
                row["row_sha256"] for row in strict["strict_credits"]
                if row.get("origin_release") == RELEASE
            ),
        },
        "artifacts": inventory,
        "counts": {
            "non_manifest_artifacts": len(inventory),
            "catalog_records": artifacts["Claim_Catalog.json"]["counts"]["records"],
            "origin_theorems": 0, "origin_open_claims": accepted_count,
            "origin_strict_conjectures": strict["counts"]["origin_5_5_credits"],
            "cumulative_theorems": 2_500,
            "cumulative_open_claims": artifacts["Open_Claim_List.json"]["counts"]["records"],
            "effective_strict_conjecture_credits": strict["counts"]["effective_strict_credits"],
            "net_strict_increase_after_5_0": strict["counts"]["net_strict_increase_after_5_0"],
        },
    })


def validate_release_documents(
    documents: Mapping[str, Mapping[str, Any]], expected: Mapping[str, Mapping[str, Any]],
    parent: Mapping[str, Mapping[str, Any]], new_rows: Sequence[Mapping[str, Any]],
) -> None:
    require(set(documents) == ALL_RELEASE_FILES, "release document set drifted")
    require(set(expected) == set(RELEASE_FILES), "independent artifact set drifted")
    for name in RELEASE_FILES:
        verify_seal(documents[name], name)
        require(documents[name] == expected[name], f"{name} differs from independent reconstruction")
    validate_origin_rows(documents["Claim_Catalog.json"]["records"][4_100:], new_rows)
    validate_strict_catalog_symmetry(documents, len(new_rows))
    validate_dense_origin_ids(new_rows)
    validate_parent_prefix(documents["Claim_Catalog.json"]["records"], parent["Claim_Catalog.json"]["records"], "catalog")


def check_release(
    root: Path, parent: Mapping[str, Mapping[str, Any]], curation: Mapping[str, Any],
    accepted: Sequence[Mapping[str, Any]], important: Mapping[str, Any],
    frontier: Mapping[str, Any], contract: Mapping[str, Any],
    source_authorities: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    directory = safe_path(root, RELEASE_REL, file=False)
    entries = list(directory.iterdir())
    require(all(path.is_file() and not path.is_symlink() for path in entries),
            "5.5 release contains a non-regular/symlink entry")
    observed_names = {path.name for path in entries}
    require(observed_names == ALL_RELEASE_FILES, f"5.5 release has missing/extra files: {sorted(observed_names)}")
    documents = {name: load_json(root, RELEASE_REL / name) for name in ALL_RELEASE_FILES}
    inputs = authoritative_inputs(root, contract, curation, important, frontier, parent, source_authorities)
    new_rows = [expected_claim(root, row, rank, curation) for rank, row in enumerate(accepted, start=1)]
    expected = expected_artifacts(parent, new_rows, inputs, frontier)
    validate_release_documents(documents, expected, parent, new_rows)
    manifest = documents[MANIFEST_NAME]
    verify_seal(manifest, MANIFEST_NAME)
    validate_manifest_inventory_shape(manifest)
    wanted_manifest = expected_manifest(root, expected, inputs, curation, important, frontier)
    require(manifest == wanted_manifest, "Release_Manifest.json differs from independent reconstruction")
    inventory = manifest["artifacts"]
    require(release_root(inventory) == manifest["release_root_sha256"], "5.5 release root does not recompute")
    for row in inventory:
        name = row["path"]
        path = directory / name
        require(file_sha(path) == row["sha256"] and path.stat().st_size == row["size_bytes"],
                f"manifest file binding drifted: {name}")
        require(primary_rows(documents[name]) == row["row_count"], f"manifest row count drifted: {name}")
    validate_stage6_parent_interface(documents)
    return documents, manifest, new_rows, inputs


def authenticated_parent_pointer() -> dict[str, Any]:
    return {
        "authority_sha256": "d31142a2ad65035bb88201e23d9a0329ee2a9948e65d5070e9d24685e28dde80",
        "manifest_path": "releases/5.4/Release_Manifest.json",
        "manifest_sha256": PARENT_MANIFEST_SHA256,
        "release": PARENT_RELEASE,
        "release_root_sha256": PARENT_RELEASE_ROOT,
        "schema_version": "awesome-theorems/stage5-current-release/5.4",
    }


def expected_target_pointer(root: Path, manifest: Mapping[str, Any]) -> dict[str, Any]:
    return seal({
        "schema_version": "awesome-theorems/stage5-current-release/5.5",
        "release": RELEASE,
        "manifest_path": "releases/5.5/Release_Manifest.json",
        "manifest_sha256": file_sha(safe_path(root, RELEASE_REL / MANIFEST_NAME)),
        "release_root_sha256": manifest["release_root_sha256"],
    })


def validate_current_pointer(
    root: Path, current: Mapping[str, Any], manifest: Mapping[str, Any], boundary: str
) -> str:
    verify_seal(current, "Current_Release.json")
    parent = authenticated_parent_pointer()
    target = expected_target_pointer(root, manifest)
    require(boundary in {"auto", "prepublish", "published"}, "invalid publication boundary")
    if boundary == "prepublish":
        require(current == parent, "prepublish gate requires exact authenticated 5.4 Current_Release")
        return "prepublish"
    if boundary == "published":
        require(current == target, "published gate requires exact accepted 5.5 Current_Release")
        return "published"
    if current == parent:
        return "prepublish"
    if current == target:
        return "published"
    raise CheckError("auto publication boundary found neither exact 5.4 parent nor exact 5.5 target pointer")


def acceptance_receipt(
    root: Path, manifest: Mapping[str, Any], curation: Mapping[str, Any],
    important: Mapping[str, Any], frontier: Mapping[str, Any], new_count: int,
) -> dict[str, Any]:
    checker_relative = Path("Docs/catalog/v5/tools/check_math_catalog_v5_5.py")
    return seal({
        "schema_version": "awesome-theorems/stage5-independent-release-acceptance/5.5",
        "release": RELEASE,
        "release_root_sha256": manifest["release_root_sha256"],
        "manifest_file_sha256": file_sha(safe_path(root, RELEASE_REL / MANIFEST_NAME)),
        "manifest_authority_sha256": manifest["authority_sha256"],
        "curation_authority_sha256": curation["authority_sha256"],
        "important_authority_sha256": important["authority_sha256"],
        "frontier_authority_sha256": frontier["authority_sha256"],
        "checker_file_sha256": file_sha(safe_path(root, checker_relative)),
        "counts": copy.deepcopy(manifest["counts"]),
        "findings": [],
    })


def verify(repo: Path, *, boundary: str = "auto") -> dict[str, Any]:
    root = repo_root(repo)
    current_path = safe_path(root, CURRENT_REL)
    current_before = current_path.read_bytes()
    parent = check_parent(root)
    source_authorities = load_source_authorities(root)
    important = check_important(root, parent)
    frontier = check_frontier(root, parent, important)
    curation, accepted = check_curation(root, parent["Claim_Catalog.json"]["records"], source_authorities)
    contract = check_contract(root, curation, important, frontier, source_authorities)
    documents, manifest, new_rows, _inputs = check_release(
        root, parent, curation, accepted, important, frontier, contract, source_authorities
    )
    current = parse_document_bytes(current_before, CURRENT_REL.as_posix())
    require(current_path.read_bytes() == current_before, "Current_Release changed during independent acceptance")
    observed_boundary = validate_current_pointer(root, current, manifest, boundary)
    # Re-read every release byte after semantic validation to close the publication race window.
    manifest_by_name = {row["path"]: row for row in manifest["artifacts"]}
    for name in RELEASE_FILES:
        path = safe_path(root, RELEASE_REL / name)
        require(file_sha(path) == manifest_by_name[name]["sha256"], f"release changed during acceptance: {name}")
    require(file_sha(safe_path(root, RELEASE_REL / MANIFEST_NAME)) == digest(encoded(manifest)),
            "manifest changed during acceptance")
    receipt = acceptance_receipt(root, manifest, curation, important, frontier, len(new_rows))
    return {
        "root": root,
        "boundary": observed_boundary,
        "parent": parent,
        "important": important,
        "frontier": frontier,
        "curation": curation,
        "accepted": accepted,
        "contract": contract,
        "source_authorities": source_authorities,
        "documents": documents,
        "manifest": manifest,
        "new_rows": new_rows,
        "receipt": receipt,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[4])
    boundary = parser.add_mutually_exclusive_group()
    boundary.add_argument("--auto-boundary", dest="boundary", action="store_const", const="auto",
                          help="accept exact prepublish 5.4 or published 5.5 pointer (default)")
    boundary.add_argument("--prepublish", dest="boundary", action="store_const", const="prepublish",
                          help="require Current_Release to remain exact authenticated 5.4")
    boundary.add_argument("--published", dest="boundary", action="store_const", const="published",
                          help="require Current_Release to be exact accepted 5.5")
    parser.set_defaults(boundary="auto")
    parser.add_argument("--receipt-json", action="store_true",
                        help="print only the canonical independent acceptance receipt")
    parser.add_argument("--quiet", action="store_true", help="suppress the human PASS line")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = verify(args.repo_root, boundary=args.boundary)
    except (CheckError, OSError, KeyError, TypeError, ValueError, IndexError) as error:
        print(f"FAIL independent math catalog 5.5: {error}", file=sys.stderr)
        return 1
    if args.receipt_json:
        sys.stdout.buffer.write(encoded(result["receipt"]))
    elif not args.quiet:
        manifest = result["manifest"]
        print(
            "PASS independent math catalog 5.5 "
            f"mode={result['boundary']} root={manifest['release_root_sha256']} "
            f"catalog={manifest['counts']['catalog_records']} "
            f"theorem={manifest['counts']['cumulative_theorems']} "
            f"open={manifest['counts']['cumulative_open_claims']} "
            f"strict={manifest['counts']['effective_strict_conjecture_credits']} "
            f"important={IMPORTANT_COUNT} "
            f"frontier={manifest['quality_qualification']['accepted_additional_frontier_theorems']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
