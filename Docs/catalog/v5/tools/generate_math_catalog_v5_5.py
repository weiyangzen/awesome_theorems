#!/usr/bin/env python3
"""Build the qualified Stage5 release 5.5.

Release 5.5 is deliberately narrow in quantity and broad in qualification:

* it preserves release 5.4 byte-semantically and appends only independently
  curated strict conjectures;
* it binds, but does not duplicate, the separately checked 1,000-row important
  theorem inventory and the 500--1,000-row frontier-theorem qualification;
* it requires 401--1,000 new strict conjectures, so the effective strict count
  is 1,401--2,000 and the net increase over the 401-credit 5.0 baseline is at
  least 1,000;
* it never turns a question, pending review, or candidate-only row into credit.

The generator is standard-library-only.  ``--check`` is read-only. ``--write``
materializes the immutable release directory but leaves Current_Release at 5.4.
``--publish-current`` performs a compare-and-swap from the authenticated 5.4
pointer after the release directory has been written and re-read.
"""

from __future__ import annotations

import argparse
import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from typing import Any, Iterable, Iterator, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[4]
V5_ROOT = REPO_ROOT / "Docs/catalog/v5"
PARENT_DIR = V5_ROOT / "releases/5.4"
RELEASE_DIR = V5_ROOT / "releases/5.5"
CURRENT_PATH = V5_ROOT / "Current_Release.json"
LOCK_PATH = V5_ROOT / ".Current_Release.lock"
CURATION_PATH = V5_ROOT / "curation/Strict_Conjecture_Curation_v5_5.json"
IMPORTANT_PATH = (
    V5_ROOT / "curation/theorem_quality_v5_5/mathlib-important-inventory-1000.json"
)
FRONTIER_PATH = V5_ROOT / "curation/Frontier_Theorem_Qualification_v5_5.json"
FRONTIER_ACCEPTANCE_PATH = (
    V5_ROOT / "curation/Frontier_Theorem_Qualification_Acceptance_v5_5.json"
)
FRONTIER_SPECIALIZED_CHECKER_PATH = (
    V5_ROOT / "tools/check_frontier_theorem_qualification_v5_5.py"
)
CONTRACT_PATH = V5_ROOT / "Stage5_Math_Expansion_Contract_v5_5.json"
CHECKER_PATH = V5_ROOT / "tools/check_math_catalog_v5_5.py"
INDEPENDENT_RECEIPT_PATH = (
    V5_ROOT / "receipts/V5_5_Independent_Acceptance_Receipt.json"
)

RELEASE = "5.5"
PARENT_RELEASE = "5.4"
REVIEW_DATE = "2026-08-10"
PARENT_RELEASE_ROOT = "c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813"
PARENT_MANIFEST_SHA256 = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
PARENT_CATALOG_SHA256 = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
PARENT_STRICT_SHA256 = "52ba1ccf06462741bcc48028fb121e5e30d1e7b56128cfeb910dc56a2e1a83a3"
PARENT_CURRENT_SHA256 = "261f27d39f379a879ea0fcacbab9e3c43dc5be8d83ea56473b2e8b4e6c384795"
FRONTIER_FILE_SHA256 = "7e59381dee0d3364ae4ed75b7128e7fa86085a55141f756de11046f7c036b4b0"
FRONTIER_AUTHORITY_SHA256 = "d221170ac0a23a4134bf19457b124277b779eda0e0ef2180c283720223bac903"
FRONTIER_SPECIALIZED_CHECKER_SHA256 = "3f4b27bd5b67cda31e1cd392c55d928cb5693a14389c5a63829bb9bf8dfae222"
FRONTIER_ACCEPTANCE_FILE_SHA256 = "b602a39d349664d0eb1bbf035062aacb2b0fadebb53f76ef7efc879d88ea1659"
FRONTIER_ACCEPTANCE_AUTHORITY_SHA256 = "304a8404a5a8626a2863f2c98925533ad3b9b70a37820c9c6787bdc37984312d"
FRONTIER_REVIEW_MANIFEST_SHA256 = "b863b7b7a3b50020367afdbc1baab9700cf6c52f6dd27d4078d7360289aa3c1d"
FRONTIER_REVIEW_FILE_SET_SHA256 = "86ad73a13a81f51012df9f302a1682b6da6c74bba7ae0ec00305c8c181dfec8d"
PARENT_ATV_HIGH = 7_584
PARENT_ATF_HIGH = 7_354
MIN_NEW_STRICT = 401
MAX_NEW_STRICT = 1_000
BASELINE_5_0_STRICT = 401
MIN_NET_STRICT_AFTER_5_0 = 1_000
MIN_EFFECTIVE_STRICT = BASELINE_5_0_STRICT + MIN_NET_STRICT_AFTER_5_0
MAX_EFFECTIVE_STRICT = 2_000
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
ALL_PARENT_FILES = frozenset((*RELEASE_FILES, MANIFEST_NAME))

SHA_RE = re.compile(r"^[0-9a-f]{64}$")
S5_RE = re.compile(r"^S5-CLM-([0-9]{8})$")
ATF_RE = re.compile(r"^ATF-([0-9]{8})$")
ATV_RE = re.compile(r"^ATV-([0-9]{8})$")
SOURCE_KIND_RE = re.compile(r"^[a-z][a-z0-9_]{1,63}$")
MSC_RE = re.compile(r"^(?P<root>[0-9]{2})(?:[A-Z][0-9]{2})?$")
ALLOWED_SOURCE_KINDS = {
    "oeis",
    "aimpl",
    "open_logic",
    "open_problem_garden",
}

# A source kind is only syntactically known until an immutable review authority
# is pinned here.
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

ORIGIN_5_5_RECORD_KEYS = frozenset(
    {
        "schema_version", "record_role", "release_id", "origin_stage",
        "origin_release", "stage_claim_id", "family_id", "sense_id",
        "variant_id", "occurrence_id", "owner_domain", "membership_domains",
        "category", "claim_kind", "current_claim_kind", "historical_kind",
        "material_status", "lifecycle", "truth_apt", "atomicity",
        "display_name", "aliases", "curation_key", "semantic_key",
        "semantic_payload_sha256", "mathematical_statement", "classification",
        "importance", "frontier", "status_detail", "source_id",
        "source_locator", "source_record_key", "rights", "dedupe",
        "curator_disposition", "allocation", "provenance", "lineage",
        "content_payload_sha256", "catalog_record_sha256",
    }
)

ORIGIN_5_5_STRICT_CREDIT_KEYS = frozenset(
    {
        "stage_claim_id", "variant_id", "semantic_key", "origin_release",
        "credit_source_branch", "evidence_sha256", "catalog_record_sha256",
        "statement_sha256", "curation_row_sha256", "source_row_sha256",
        "source_authority_file_sha256", "allocation_request_sha256",
        "grants_strict_conjecture_credit", "row_sha256",
    }
)

INDEPENDENT_RECEIPT_KEYS = frozenset(
    {
        "schema_version", "release", "release_root_sha256",
        "manifest_file_sha256", "manifest_authority_sha256",
        "curation_authority_sha256", "important_authority_sha256",
        "frontier_authority_sha256", "counts", "findings",
        "checker_file_sha256", "authority_sha256",
    }
)

SOURCE_BINDING_KEYS = frozenset(
    {
        "path", "file_sha256", "line_number", "source_row_sha256",
        "source_record_key_json_pointer", "exact_claim_json_pointer",
        "exact_context_json_pointer",
    }
)


class GenerationError(RuntimeError):
    """An authenticated input or generated invariant failed closed."""


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise GenerationError(f"not canonical JSON: {error}") from error


def encoded(value: Any) -> bytes:
    return canonical(value) + b"\n"


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha_file(path: Path) -> str:
    hasher = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                hasher.update(chunk)
    except OSError as error:
        raise GenerationError(f"cannot hash {path}: {error}") from error
    return hasher.hexdigest()


def without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return digest(canonical({key: item for key, item in value.items() if key not in omitted}))


def seal(value: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    result.pop("authority_sha256", None)
    result["authority_sha256"] = without(result, "authority_sha256")
    return result


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GenerationError(message)


def require_exact_keys(value: Mapping[str, Any], expected: Iterable[str], label: str) -> None:
    expected_set = set(expected)
    observed = set(value)
    require(
        observed == expected_set,
        f"{label} is not closed-schema: missing={sorted(expected_set - observed)} "
        f"extra={sorted(observed - expected_set)}",
    )


def reject_duplicate_pairs(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GenerationError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def reject_nonfinite_constant(value: str) -> Any:
    raise GenerationError(f"non-finite JSON number is forbidden: {value}")


def parse_json(payload: bytes, label: str) -> Any:
    try:
        return json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=reject_duplicate_pairs,
            parse_constant=reject_nonfinite_constant,
        )
    except (UnicodeError, json.JSONDecodeError, GenerationError) as error:
        raise GenerationError(f"cannot parse {label}: {error}") from error


def require_str(value: Any, label: str, pattern: re.Pattern[str] | None = None) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{label} must be a nonempty string")
    if pattern is not None:
        require(pattern.fullmatch(value) is not None, f"{label} has invalid syntax: {value!r}")
    return value


def require_int(value: Any, label: str, minimum: int | None = None) -> int:
    require(isinstance(value, int) and not isinstance(value, bool), f"{label} must be an integer")
    if minimum is not None:
        require(value >= minimum, f"{label} must be at least {minimum}")
    return value


def load_json(path: Path, label: str | None = None) -> dict[str, Any]:
    try:
        lexical_relative = path.absolute().relative_to(REPO_ROOT.absolute())
    except ValueError as error:
        raise GenerationError(f"cannot load path outside repository: {path}") from error
    checked = safe_repo_file(lexical_relative.as_posix(), str(label or path))
    require(checked == path.resolve(), f"{label or path} path resolution drifted")
    try:
        payload = checked.read_bytes()
    except OSError as error:
        raise GenerationError(f"cannot load {label or path}: {error}") from error
    value = parse_json(payload, str(label or path))
    require(isinstance(value, dict), f"{label or path} must contain one object")
    return value


def verify_seal(value: Mapping[str, Any], label: str) -> None:
    declared = require_str(value.get("authority_sha256"), f"{label}.authority_sha256", SHA_RE)
    require(declared == without(value, "authority_sha256"), f"{label} has stale authority")


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError as error:
        raise GenerationError(f"path is outside repository: {path}") from error


def safe_repo_file(relative: Any, label: str) -> Path:
    text = require_str(relative, label)
    candidate = Path(text)
    require(not candidate.is_absolute() and ".." not in candidate.parts, f"unsafe {label}")
    unresolved = REPO_ROOT / candidate
    cursor = REPO_ROOT
    for part in candidate.parts:
        cursor /= part
        require(not cursor.is_symlink(), f"{label} traverses a symlink: {text}")
    resolved = unresolved.resolve()
    try:
        resolved.relative_to(REPO_ROOT.resolve())
    except ValueError as error:
        raise GenerationError(f"{label} escapes repository") from error
    require(resolved.is_file(), f"{label} is missing: {text}")
    return resolved


def replay_review_artifact(
    row: Mapping[str, Any], label: str, *, expected_path: str | None = None
) -> dict[str, Any]:
    require(isinstance(row, dict), f"{label} binding malformed")
    path_text = require_str(row.get("path"), f"{label}.path")
    if expected_path is not None:
        require(path_text == expected_path, f"{label} path differs from receipt inventory")
    file_sha = require_str(row.get("sha256"), f"{label}.sha256", SHA_RE)
    path = safe_repo_file(path_text, f"{label}.path")
    require(sha_file(path) == file_sha, f"{label} file hash drifted")
    size = row.get("size_bytes")
    if size is not None:
        require_int(size, f"{label}.size_bytes", 0)
        require(path.stat().st_size == size, f"{label} file size drifted")
    rows = row.get("rows")
    if rows is not None:
        require_int(rows, f"{label}.rows", 0)
        require(len(path.read_bytes().splitlines()) == rows, f"{label} row count drifted")
    return {
        "path": path_text,
        "file_sha256": file_sha,
        "size_bytes": path.stat().st_size,
        "row_count": len(path.read_bytes().splitlines()),
    }


def load_source_authority_allowlist() -> dict[str, dict[str, Any]]:
    """Replay pinned receipts into the only first-class review files we trust."""
    result: dict[str, dict[str, Any]] = {}
    for source_kind, specification in PINNED_SOURCE_AUTHORITY_RECEIPTS.items():
        receipt_path = safe_repo_file(
            specification["path"], f"{source_kind} authority receipt path"
        )
        require(
            sha_file(receipt_path) == specification["file_sha256"],
            f"{source_kind} authority receipt drifted",
        )
        receipt = load_json(receipt_path, f"{source_kind} authority receipt")
        require(
            receipt.get("schema_version") == specification["schema_version"],
            f"{source_kind} authority receipt schema drifted",
        )
        if "authority_sha256" in specification:
            verify_seal(receipt, f"{source_kind} authority receipt")
            require(
                receipt.get("authority_sha256") == specification["authority_sha256"],
                f"{source_kind} authority receipt seal differs from the pinned authority",
            )
        reviews: list[dict[str, Any]] = []
        qualification_artifact: dict[str, Any] | None = None
        qualified_candidates: list[dict[str, str]] | None = None
        if source_kind == "oeis":
            artifacts = receipt.get("artifacts")
            require(isinstance(artifacts, dict), "OEIS authority lacks artifact inventory")
            for key in sorted(artifacts):
                if OEIS_REVIEW_KEY_RE.fullmatch(key):
                    expected = f"Docs/catalog/v5/curation/oeis_v5_5/{key}"
                    reviews.append(
                        replay_review_artifact(
                            artifacts[key], f"OEIS authority {key}", expected_path=expected
                        )
                    )
            require(len(reviews) == 16, "OEIS authority must expose exactly 16 review ledgers")
            qualification_artifact = replay_review_artifact(
                artifacts.get("combined-survivors.jsonl"),
                "OEIS combined survivor authority",
                expected_path="Docs/catalog/v5/curation/oeis_v5_5/combined-survivors.jsonl",
            )
            require(
                qualification_artifact["file_sha256"]
                == "d9928d3d61a05e618df7a044c98d966b6f4d8fe63925ea4e95bb2cd5e4de4e5a",
                "OEIS combined survivor authority is not the pinned 268-row set",
            )
            survivor_path = safe_repo_file(
                qualification_artifact["path"], "OEIS combined survivor authority"
            )
            qualified_candidates = []
            seen_candidates: set[str] = set()
            for line_index, payload in enumerate(survivor_path.read_bytes().splitlines(), start=1):
                survivor = parse_json(payload, f"OEIS combined survivor row {line_index}")
                require(isinstance(survivor, dict), f"OEIS combined survivor row {line_index} malformed")
                candidate = require_str(survivor.get("candidate_key"), f"OEIS survivor {line_index} candidate_key")
                require(candidate not in seen_candidates, f"duplicate OEIS survivor candidate: {candidate}")
                tier = require_str(survivor.get("importance_tier"), f"OEIS survivor {line_index} tier")
                summary = require_str(survivor.get("semantic_summary"), f"OEIS survivor {line_index} summary")
                require(tier in {"high", "medium"}, f"OEIS survivor {line_index} tier is ineligible")
                require(
                    survivor.get("candidate_only") is True
                    and survivor.get("grants_catalog_entry") is False
                    and survivor.get("grants_strict_conjecture_credit") is False,
                    f"OEIS survivor {line_index} credit boundary drifted",
                )
                seen_candidates.add(candidate)
                qualified_candidates.append(
                    {"candidate_key": candidate, "importance_tier": tier, "semantic_summary": summary}
                )
            qualified_candidates.sort(key=lambda row: row["candidate_key"])
            require(len(qualified_candidates) == 268, "OEIS survivor denominator is not 268")
        elif source_kind == "aimpl":
            artifacts = receipt.get("artifacts")
            require(isinstance(artifacts, dict), "AimPL authority lacks artifact inventory")
            reviews.append(
                replay_review_artifact(
                    artifacts.get("review_ledger"), "AimPL authority review_ledger",
                    expected_path="Docs/catalog/v5/curation/aimpl_v5_5/review-ledger.jsonl",
                )
            )
        elif source_kind == "open_logic":
            artifact_name = require_str(receipt.get("artifact"), "Open Logic artifact")
            require(artifact_name == "open-logic-review.jsonl", "Open Logic artifact name drifted")
            artifact_path = (
                "Docs/catalog/v5/curation/open_logic_v5_5/open-logic-review.jsonl"
            )
            reviews.append(
                replay_review_artifact(
                    {
                        "path": artifact_path,
                        "sha256": receipt.get("artifact_sha256"),
                    },
                    "Open Logic authority review",
                    expected_path=artifact_path,
                )
            )
        elif source_kind == "open_problem_garden":
            output = receipt.get("output")
            require(isinstance(output, dict), "Open Problem Garden authority lacks output binding")
            expected = (
                "Docs/catalog/v5/curation/openproblemgarden_v5_5/eligibility-ledger.jsonl"
            )
            review = replay_review_artifact(
                {
                    "path": output.get("path"),
                    "sha256": output.get("sha256"),
                    "rows": output.get("rows"),
                },
                "Open Problem Garden eligibility authority",
                expected_path=expected,
            )
            require(
                review["file_sha256"]
                == "912f07198a7df439d7c398b41713908654d1b03b6380a61856a785a03a4fe021"
                and review["row_count"] == 404,
                "Open Problem Garden eligibility ledger differs from the pinned 404-row audit",
            )
            reviews.append(review)
        else:  # pragma: no cover - a new kind requires an explicit replay branch.
            raise GenerationError(f"no authority replay policy for {source_kind}")
        require(reviews, f"{source_kind} authority has no first-class review ledgers")
        require(
            len({row["path"] for row in reviews}) == len(reviews),
            f"{source_kind} authority repeats a review path",
        )
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


def source_review_disposition(
    source_kind: str, row: Mapping[str, Any], authority: Mapping[str, Any]
) -> str:
    if source_kind == "oeis":
        decision = row.get("decision")
        require(decision in {"accept", "reject"}, "OEIS review disposition malformed")
        survivors = authority.get("qualified_candidates")
        require(isinstance(survivors, list), "OEIS survivor authority missing")
        survivor_keys = {
            item["candidate_key"] for item in survivors if isinstance(item, dict)
        }
        if decision == "accept" and row.get("candidate_key") in survivor_keys:
            return "accepted_eligible"
        return "rejected"
    if source_kind == "aimpl":
        decision = row.get("final_decision")
    else:
        decision = row.get("decision")
    require(
        decision in {"accept", "eligible", "pending", "reject"},
        f"{source_kind} review disposition malformed",
    )
    if decision in {"accept", "eligible"}:
        return "accepted_eligible"
    return "pending" if decision == "pending" else "rejected"


def expected_coverage_bindings(
    authorities: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    expected: list[dict[str, Any]] = []
    for source_kind in sorted(authorities):
        authority = authorities[source_kind]
        receipt = authority.get("receipt")
        reviews = authority.get("review_artifacts")
        require(isinstance(receipt, dict), f"{source_kind} receipt binding malformed")
        require(isinstance(reviews, list), f"{source_kind} review inventory malformed")
        for review_index, review in enumerate(reviews):
            require(isinstance(review, dict), f"{source_kind} review binding {review_index} malformed")
            path = safe_repo_file(review.get("path"), f"{source_kind} review binding {review_index}")
            counts = {"accepted_eligible": 0, "pending": 0, "rejected": 0}
            for line_index, payload in enumerate(path.read_bytes().splitlines(), start=1):
                source_row = parse_json(payload, f"{source_kind} review {review_index} row {line_index}")
                require(isinstance(source_row, dict), f"{source_kind} review row {line_index} malformed")
                counts[source_review_disposition(source_kind, source_row, authority)] += 1
            require(sum(counts.values()) == review["row_count"], f"{source_kind} review coverage count drifted")
            expected.append(
                {
                    "source_kind": source_kind,
                    "path": review["path"],
                    "file_sha256": review["file_sha256"],
                    "size_bytes": review["size_bytes"],
                    "rows": review["row_count"],
                    **counts,
                    "audit_receipt": copy.deepcopy(receipt),
                }
            )
    return sorted(expected, key=lambda row: (row["source_kind"], row["path"]))


def binding(path: Path, value: Mapping[str, Any] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": repo_relative(path),
        "file_sha256": sha_file(path),
        "size_bytes": path.stat().st_size,
    }
    if value is not None and isinstance(value.get("authority_sha256"), str):
        result["authority_sha256"] = value["authority_sha256"]
    return result


def set_digest(values: Iterable[str]) -> str:
    return digest(canonical(sorted(values)))


def primary_rows(document: Mapping[str, Any]) -> int:
    for key in (
        "records",
        "variants",
        "mappings",
        "migrations",
        "candidate_dispositions",
        "strict_credits",
    ):
        rows = document.get(key)
        if isinstance(rows, list):
            if key == "candidate_dispositions" and isinstance(document.get("msc_coverage"), list):
                return len(rows) + len(document["msc_coverage"])
            if key == "strict_credits" and isinstance(document.get("credit_corrections"), list):
                return len(rows) + len(document["credit_corrections"])
            return len(rows)
    return 0


def release_root(inventory: Sequence[Mapping[str, Any]]) -> str:
    normalized = [
        {"path": row["path"], "sha256": row["sha256"], "size_bytes": row["size_bytes"]}
        for row in inventory
    ]
    return digest(canonical(sorted(normalized, key=lambda row: str(row["path"]))))


def verify_parent() -> dict[str, dict[str, Any]]:
    require(PARENT_DIR.is_dir(), "release 5.4 parent directory is missing")
    names = {path.name for path in PARENT_DIR.iterdir() if path.is_file()}
    require(names == ALL_PARENT_FILES, "release 5.4 artifact inventory drifted")
    require(sha_file(PARENT_DIR / MANIFEST_NAME) == PARENT_MANIFEST_SHA256, "parent manifest drifted")
    require(sha_file(PARENT_DIR / "Claim_Catalog.json") == PARENT_CATALOG_SHA256, "parent catalog drifted")
    require(sha_file(PARENT_DIR / "Strict_Conjecture_Ledger.json") == PARENT_STRICT_SHA256, "parent strict ledger drifted")
    documents = {name: load_json(PARENT_DIR / name, f"parent {name}") for name in names}
    for name, document in documents.items():
        verify_seal(document, f"parent {name}")
    manifest = documents[MANIFEST_NAME]
    require(manifest.get("release") == PARENT_RELEASE, "wrong parent release")
    require(manifest.get("release_root_sha256") == PARENT_RELEASE_ROOT, "parent release root drifted")
    inventory = manifest.get("artifacts")
    require(isinstance(inventory, list), "parent manifest inventory malformed")
    require(release_root(inventory) == PARENT_RELEASE_ROOT, "parent release root does not recompute")
    for row in inventory:
        require(isinstance(row, dict), "parent manifest row malformed")
        path = PARENT_DIR / require_str(row.get("path"), "parent artifact path")
        require(path.is_file(), f"parent artifact missing: {path.name}")
        require(sha_file(path) == row.get("sha256"), f"parent artifact hash drifted: {path.name}")
        require(path.stat().st_size == row.get("size_bytes"), f"parent artifact size drifted: {path.name}")
    catalog = documents["Claim_Catalog.json"]
    strict = documents["Strict_Conjecture_Ledger.json"]
    require(len(catalog.get("records", [])) == 4_100, "parent catalog denominator drifted")
    require(len(strict.get("strict_credits", [])) == 1_000, "parent strict denominator drifted")
    return documents


def row_hash(row: Mapping[str, Any], field: str = "row_sha256") -> str:
    return without(row, field)


def record_semantic_keys(row: Mapping[str, Any]) -> set[str]:
    result: set[str] = set()
    direct = row.get("semantic_key")
    if isinstance(direct, str) and direct:
        result.add(direct)
    dedupe = row.get("dedupe")
    if isinstance(dedupe, dict):
        nested = dedupe.get("semantic_key")
        if isinstance(nested, str) and nested:
            result.add(nested)
        normalized = dedupe.get("normalized_statement_sha256")
        if isinstance(normalized, str) and SHA_RE.fullmatch(normalized):
            result.add(f"normalized-statement-sha256/{normalized}")
        identity = dedupe.get("identity_payload_sha256")
        if isinstance(identity, str) and SHA_RE.fullmatch(identity):
            result.add(f"formal-conjectures-parent-identity/{identity}")
    return result


def verify_important(
    document: Mapping[str, Any], parent_theorems: Mapping[str, Mapping[str, Any]]
) -> list[dict[str, Any]]:
    verify_seal(document, "important theorem inventory")
    require(document.get("schema_version") == "awesome-theorems/mathlib-important-inventory/5.5", "wrong important schema")
    rows = document.get("records")
    require(isinstance(rows, list) and len(rows) == IMPORTANT_COUNT, "important inventory is not exactly 1,000 rows")
    ids: set[str] = set()
    semantic: set[str] = set()
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"important row {index} malformed")
        require(row.get("row_sha256") == row_hash(row), f"important row {index} hash stale")
        sid = require_str(row.get("stage_claim_id"), f"important[{index}].stage_claim_id", S5_RE)
        key = require_str(row.get("semantic_key"), f"important[{index}].semantic_key")
        require(sid in parent_theorems and sid not in ids, f"important row {index} identity invalid")
        parent = parent_theorems[sid]
        require(row.get("variant_id") == parent.get("variant_id"), f"important row {index} variant binding invalid")
        require(key in record_semantic_keys(parent), f"important row {index} semantic binding invalid")
        evidence = row.get("formal_evidence")
        require(
            isinstance(evidence, dict)
            and evidence.get("formal_proof_state") == "kernel_checked_sorry_free"
            and evidence.get("uses_sorry") is False,
            f"important row {index} formal evidence gate failed",
        )
        importance = row.get("importance_evidence")
        require(
            isinstance(importance, dict)
            and importance.get("operational_importance_credit") is True
            and importance.get("human_editorial_basis"),
            f"important row {index} human importance gate failed",
        )
        require(key not in semantic, f"important row {index} semantic duplicate")
        require(row.get("grants_existing_important_theorem_credit") is True, f"important row {index} lacks credit")
        ids.add(sid)
        semantic.add(key)
    return list(rows)


def verify_frontier_acceptance(document: Mapping[str, Any]) -> None:
    """Replay the pinned independent frontier checker and its durable receipt."""
    frontier_path = safe_repo_file(
        repo_relative(FRONTIER_PATH), "frontier theorem qualification"
    )
    checker_path = safe_repo_file(
        repo_relative(FRONTIER_SPECIALIZED_CHECKER_PATH),
        "frontier specialized checker",
    )
    acceptance_path = safe_repo_file(
        repo_relative(FRONTIER_ACCEPTANCE_PATH),
        "frontier independent acceptance receipt",
    )
    hashes_before = {
        "qualification": sha_file(frontier_path),
        "checker": sha_file(checker_path),
        "receipt": sha_file(acceptance_path),
    }
    require(
        hashes_before
        == {
            "qualification": FRONTIER_FILE_SHA256,
            "checker": FRONTIER_SPECIALIZED_CHECKER_SHA256,
            "receipt": FRONTIER_ACCEPTANCE_FILE_SHA256,
        },
        "frontier qualification, specialized checker, or acceptance receipt drifted",
    )

    acceptance_payload = acceptance_path.read_bytes()
    acceptance = load_json(
        acceptance_path, "frontier independent acceptance receipt"
    )
    require(
        acceptance_payload == encoded(acceptance),
        "frontier independent acceptance receipt is not canonical",
    )
    verify_seal(acceptance, "frontier independent acceptance receipt")
    require(
        acceptance.get("authority_sha256") == FRONTIER_ACCEPTANCE_AUTHORITY_SHA256,
        "frontier independent acceptance receipt authority drifted",
    )

    inputs = document.get("inputs")
    require(isinstance(inputs, dict), "frontier qualification inputs malformed")
    reviews = inputs.get("review_ledgers")
    require(isinstance(reviews, list) and reviews, "frontier review bindings missing")
    for index, review in enumerate(reviews):
        require(isinstance(review, dict), f"frontier review binding {index} malformed")
        require_exact_keys(
            review,
            {"path", "file_sha256", "size_bytes", "rows"},
            f"frontier review binding {index}",
        )
        require_str(review.get("path"), f"frontier review binding {index}.path")
        require_str(
            review.get("file_sha256"),
            f"frontier review binding {index}.file_sha256",
            SHA_RE,
        )
        require_int(
            review.get("size_bytes"), f"frontier review binding {index}.size_bytes", 0
        )
        require_int(review.get("rows"), f"frontier review binding {index}.rows", 0)
    review_manifest = {
        "files": len(reviews),
        "rows": sum(int(review["rows"]) for review in reviews),
        "manifest_sha256": digest(canonical(reviews)),
        "file_sha256_set_sha256": set_digest(
            str(review["file_sha256"]) for review in reviews
        ),
        "entries": copy.deepcopy(reviews),
    }
    require(
        review_manifest["manifest_sha256"] == FRONTIER_REVIEW_MANIFEST_SHA256
        and review_manifest["file_sha256_set_sha256"]
        == FRONTIER_REVIEW_FILE_SET_SHA256,
        "frontier review universe differs from the independently accepted manifest",
    )
    counts = document.get("counts")
    require(isinstance(counts, dict), "frontier qualification counts malformed")
    expected_acceptance = seal(
        {
            "schema_version": (
                "awesome-theorems/frontier-theorem-qualification-acceptance-receipt/5.5"
            ),
            "review_as_of": REVIEW_DATE,
            "qualification": {
                "path": repo_relative(FRONTIER_PATH),
                "file_sha256": FRONTIER_FILE_SHA256,
                "authority_sha256": FRONTIER_AUTHORITY_SHA256,
            },
            "checker": {
                "path": repo_relative(FRONTIER_SPECIALIZED_CHECKER_PATH),
                "file_sha256": FRONTIER_SPECIALIZED_CHECKER_SHA256,
                "independent_from_builder": True,
                "read_only": True,
            },
            "review_manifest": review_manifest,
            "counts": copy.deepcopy(counts),
            "findings": [],
        }
    )
    require(
        acceptance == expected_acceptance,
        "frontier independent acceptance receipt does not bind the exact review replay",
    )

    try:
        completed = subprocess.run(
            [
                sys.executable,
                str(checker_path),
                "--repo-root",
                str(REPO_ROOT),
                "--qualification",
                repo_relative(FRONTIER_PATH),
                "--receipt-json",
            ],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            timeout=300,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise GenerationError(
            f"frontier specialized checker could not run: {error}"
        ) from error
    require(
        completed.returncode == 0,
        "frontier specialized checker rejected the qualification: "
        f"stdout={completed.stdout[-2000:].decode('utf-8', errors='replace')!r} "
        f"stderr={completed.stderr[-2000:].decode('utf-8', errors='replace')!r}",
    )
    require(
        completed.stdout == acceptance_payload,
        "frontier specialized checker output differs from the durable acceptance receipt",
    )
    require(
        {
            "qualification": sha_file(frontier_path),
            "checker": sha_file(checker_path),
            "receipt": sha_file(acceptance_path),
        }
        == hashes_before,
        "frontier qualification trust chain changed during live replay",
    )


def verify_frontier(
    document: Mapping[str, Any], parent_theorems: Mapping[str, Mapping[str, Any]], important_ids: set[str]
) -> list[dict[str, Any]]:
    verify_seal(document, "frontier theorem qualification")
    require(
        document.get("authority_sha256") == FRONTIER_AUTHORITY_SHA256,
        "frontier qualification authority differs from the independently accepted artifact",
    )
    verify_frontier_acceptance(document)
    require(
        document.get("schema_version") == "awesome-theorems/frontier-theorem-qualification/5.5",
        "wrong frontier qualification schema",
    )
    parent = document.get("parent")
    require(
        isinstance(parent, dict)
        and parent.get("release") == PARENT_RELEASE
        and parent.get("release_root_sha256") == PARENT_RELEASE_ROOT,
        "frontier qualification parent drifted",
    )
    rows = document.get("accepted_credits")
    require(isinstance(rows, list), "frontier accepted_credits malformed")
    require(MIN_FRONTIER <= len(rows) <= MAX_FRONTIER, "frontier qualification misses 500--1,000 gate")
    ids: set[str] = set()
    semantics: set[str] = set()
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"frontier row {index} malformed")
        require(row.get("row_sha256") == row_hash(row), f"frontier row {index} hash stale")
        sid = require_str(row.get("stage_claim_id"), f"frontier[{index}].stage_claim_id", S5_RE)
        semantic = require_str(row.get("semantic_key"), f"frontier[{index}].semantic_key")
        require(sid in parent_theorems and sid not in ids, f"frontier row {index} identity invalid")
        parent_record = parent_theorems[sid]
        require(row.get("variant_id") == parent_record.get("variant_id"), f"frontier row {index} variant binding invalid")
        require(semantic in record_semantic_keys(parent_record), f"frontier row {index} semantic binding invalid")
        require(sid not in important_ids, f"frontier row {index} double-counts important quota")
        require(semantic not in semantics, f"frontier row {index} semantic duplicate")
        require(row.get("decision") == "accept" and row.get("all_gates_pass") is True, f"frontier row {index} not accepted")
        require(row.get("grants_frontier_theorem_credit") is True, f"frontier row {index} lacks formal credit")
        require(row.get("grants_new_theorem_identity_credit") is False, f"frontier row {index} invents theorem identity")
        ids.add(sid)
        semantics.add(semantic)
    counts = document.get("counts")
    require(
        isinstance(counts, dict)
        and counts.get("accepted_additional_frontier_theorems") == len(rows)
        and counts.get("unsupported_importance_or_frontier_credit") == 0,
        "frontier counters drifted",
    )
    return list(rows)


def parent_semantic_keys(records: Sequence[Mapping[str, Any]]) -> set[str]:
    result: set[str] = set()
    for row in records:
        result.update(record_semantic_keys(row))
    return result


def json_pointer(value: Any, pointer: str, label: str) -> Any:
    require(pointer.startswith("/"), f"{label} must be an RFC6901 absolute pointer")
    current = value
    for raw in pointer.split("/")[1:]:
        require(
            re.search(r"~(?:[^01]|$)", raw) is None,
            f"{label} has an invalid RFC6901 escape",
        )
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            require(token in current, f"{label} does not resolve")
            current = current[token]
        elif isinstance(current, list):
            require(
                token == "0" or (token.isdigit() and not token.startswith("0")),
                f"{label} list index is noncanonical",
            )
            require(int(token) < len(current), f"{label} list index invalid")
            current = current[int(token)]
        else:
            raise GenerationError(f"{label} traverses a scalar")
    return current


def verify_source_review_eligibility(
    source_kind: str, source_row: Mapping[str, Any], curation_row: Mapping[str, Any], index: int
) -> None:
    """Require a positive, complete decision in the pinned first-class review row."""
    if source_kind == "oeis":
        require(source_row.get("decision") == "accept", f"curation row {index} OEIS review is not accepted")
        require(
            source_row.get("truth_apt") is True
            and source_row.get("context_complete") is True
            and source_row.get("source_asserted_open_as_of_commit") is True,
            f"curation row {index} OEIS review gates failed",
        )
        require(source_row.get("importance_tier") in {"high", "medium"}, f"curation row {index} OEIS tier failed")
        require(
            source_row.get("importance_tier") == curation_row.get("importance_tier")
            and source_row.get("semantic_summary") == curation_row.get("semantic_summary"),
            f"curation row {index} OEIS tier or summary differs from reviewed row",
        )
    elif source_kind == "aimpl":
        initial = source_row.get("initial_review")
        require(
            source_row.get("final_decision") == "accept" and isinstance(initial, dict),
            f"curation row {index} AimPL review is not accepted",
        )
        require(
            initial.get("decision") == "accept"
            and initial.get("truth_apt") is True
            and initial.get("context_complete") is True
            and initial.get("source_asserted_open") is True
            and source_row.get("final_tier") in {"high", "medium"},
            f"curation row {index} AimPL review gates failed",
        )
        require(
            initial.get("tier") == curation_row.get("importance_tier")
            and initial.get("semantic_summary") == curation_row.get("semantic_summary"),
            f"curation row {index} AimPL tier or summary differs from reviewed row",
        )
    elif source_kind == "open_logic":
        require(
            source_row.get("decision") == "accept"
            and source_row.get("acceptance_evidence_complete") is True
            and source_row.get("grants_strict_conjecture_credit") is True,
            f"curation row {index} Open Logic review is not accepted",
        )
        require(
            source_row.get("truth_apt") is True
            and source_row.get("context_complete") is True
            and source_row.get("importance_tier") in {"high", "medium"}
            and source_row.get("question_to_assertion_promotion_permitted") is False,
            f"curation row {index} Open Logic review gates failed",
        )
        require(
            source_row.get("importance_tier") == curation_row.get("importance_tier"),
            f"curation row {index} Open Logic tier differs from reviewed row",
        )
    elif source_kind == "open_problem_garden":
        source = curation_row.get("source_binding")
        global_dedupe = source_row.get("global_dedupe")
        require(isinstance(source, dict), f"curation row {index} OPG source binding malformed")
        require(
            source_row.get("decision") == "accept"
            and source_row.get("formal_acceptance_eligible_for_5_5") is True
            and source_row.get("candidate_only") is True
            and source_row.get("grants_catalog_entry") is False
            and source_row.get("grants_strict_conjecture_credit") is False
            and isinstance(global_dedupe, dict)
            and global_dedupe.get("semantic_unique") is True,
            f"curation row {index} OPG eligibility transition source is invalid",
        )
        require(
            source_row.get("truth_apt") is True
            and source_row.get("context_complete") is True
            and source_row.get("current_open_as_of") == REVIEW_DATE
            and source_row.get("importance_tier") in {"high", "medium"}
            and source_row.get("source_wording_usage") == "evidence_only_not_release_payload",
            f"curation row {index} OPG truth/status/rights gates failed",
        )
        require(
            source.get("exact_claim_json_pointer") == "/semantic_summary",
            f"curation row {index} OPG release text must bind the independent semantic summary",
        )
        require(
            curation_row.get("statement_representation") == "independently_written_reviewed_summary",
            f"curation row {index} OPG statement representation is unsafe",
        )
        require(
            source_row.get("semantic_summary") == curation_row.get("exact_claim_text")
            == curation_row.get("semantic_summary")
            and source_row.get("semantic_key") == curation_row.get("semantic_key")
            and source_row.get("importance_tier") == curation_row.get("importance_tier"),
            f"curation row {index} OPG release summary binding drifted",
        )
    else:
        raise GenerationError(f"source kind {source_kind} lacks a source-review gate")


def verify_source_binding(
    row: Mapping[str, Any], index: int, source_kind: str,
    authorities: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    source = row.get("source_binding")
    require(isinstance(source, dict), f"curation row {index} source binding malformed")
    require_exact_keys(source, SOURCE_BINDING_KEYS, f"curation row {index} source binding")
    authority = authorities.get(source_kind)
    require(authority is not None, f"curation row {index} source kind lacks a pinned authority")
    reviews = authority.get("review_artifacts")
    require(isinstance(reviews, list), f"curation row {index} source authority malformed")
    allowed_paths = {
        review["path"]: review["file_sha256"]
        for review in reviews
        if isinstance(review, dict)
    }
    path_text = require_str(source.get("path"), f"curation[{index}].source_binding.path")
    require(path_text in allowed_paths, f"curation row {index} source path is not first-class reviewed authority")
    path = safe_repo_file(source.get("path"), f"curation[{index}].source_binding.path")
    observed = sha_file(path)
    require(observed == require_str(source.get("file_sha256"), f"curation[{index}].source file hash", SHA_RE), f"curation row {index} source drifted")
    require(observed == allowed_paths[path_text], f"curation row {index} source is outside the pinned receipt")
    line = require_int(source.get("line_number"), f"curation[{index}].source line", 1)
    source_row_sha = require_str(source.get("source_row_sha256"), f"curation[{index}].source row hash", SHA_RE)
    raw_lines = path.read_bytes().splitlines()
    require(line <= len(raw_lines), f"curation row {index} source line is out of range")
    source_row = parse_json(raw_lines[line - 1], f"curation row {index} bound source row")
    require(isinstance(source_row, dict), f"curation row {index} bound source row is not an object")
    require(digest(canonical(source_row)) == source_row_sha, f"curation row {index} source row hash mismatch")
    source_record_pointer = require_str(
        source.get("source_record_key_json_pointer"),
        f"curation[{index}].source record key pointer",
    )
    require(
        str(json_pointer(source_row, source_record_pointer, f"curation[{index}].source record key pointer"))
        == row.get("source_record_key"),
        f"curation row {index} source record key differs from reviewed source row",
    )
    if source_kind == "oeis":
        qualified = authority.get("qualified_candidates")
        require(isinstance(qualified, list), f"curation row {index} OEIS survivor authority missing")
        qualified_by_key = {
            candidate["candidate_key"]: candidate
            for candidate in qualified
            if isinstance(candidate, dict)
        }
        survivor = qualified_by_key.get(str(source_row.get("candidate_key")))
        require(survivor is not None, f"curation row {index} OEIS candidate is not in the 268-row survivor set")
        require(
            survivor.get("importance_tier") == source_row.get("importance_tier")
            and survivor.get("semantic_summary") == source_row.get("semantic_summary"),
            f"curation row {index} OEIS survivor tier or summary drifted",
        )
    claim_pointer = require_str(source.get("exact_claim_json_pointer"), f"curation[{index}].exact claim pointer")
    require(
        json_pointer(source_row, claim_pointer, f"curation[{index}].exact claim pointer")
        == row.get("exact_claim_text"),
        f"curation row {index} exact claim differs from bound reviewed source row",
    )
    context_pointer = source.get("exact_context_json_pointer")
    if context_pointer is not None:
        require_str(context_pointer, f"curation[{index}].exact context pointer")
        require(
            json_pointer(source_row, context_pointer, f"curation[{index}].exact context pointer")
            == row.get("exact_claim_context"),
            f"curation row {index} exact context differs from bound reviewed source row",
        )
    else:
        require(
            row.get("exact_claim_context") is None,
            f"curation row {index} has non-null context without a reviewed pointer",
        )
    verify_source_review_eligibility(source_kind, source_row, row, index)
    normalized = copy.deepcopy(source)
    normalized["authority_receipt"] = copy.deepcopy(authority["receipt"])
    return normalized


def normalize_classification(row: Mapping[str, Any], index: int) -> dict[str, Any]:
    raw = row.get("classification")
    if raw is None:
        raw = {
            "status": "review_metadata_unassigned",
            "msc_codes": [],
            "primary_msc_top_class": None,
        }
    require(isinstance(raw, dict), f"curation row {index} classification malformed")
    result = copy.deepcopy(raw)
    codes = result.get("msc_codes", [])
    require(isinstance(codes, list), f"curation row {index} msc_codes malformed")
    normalized_codes: list[str] = []
    roots: list[str] = []
    for code_index, code in enumerate(codes):
        text = require_str(code, f"curation[{index}].msc_codes[{code_index}]")
        match = MSC_RE.fullmatch(text)
        require(match is not None, f"curation row {index} has invalid MSC code: {text}")
        require(text not in normalized_codes, f"curation row {index} repeats MSC code: {text}")
        normalized_codes.append(text)
        root = match.group("root")
        if root not in roots:
            roots.append(root)
    primary = result.get("primary_msc_top_class")
    if not roots:
        require(primary is None, f"curation row {index} assigns primary MSC without an MSC code")
    else:
        primary = require_str(primary, f"curation[{index}].primary_msc_top_class")
        require(primary in roots, f"curation row {index} primary MSC is not represented in msc_codes")
    result["msc_codes"] = normalized_codes
    result["primary_msc_top_class"] = primary
    return result


def verify_curation(
    document: Mapping[str, Any], parent_records: Sequence[Mapping[str, Any]],
    authorities: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    verify_seal(document, "strict conjecture curation")
    require(
        document.get("schema_version") == "awesome-theorems/strict-conjecture-curation/5.5",
        "wrong strict curation schema",
    )
    parent = document.get("parent")
    require(
        isinstance(parent, dict)
        and parent.get("release") == PARENT_RELEASE
        and parent.get("release_root_sha256") == PARENT_RELEASE_ROOT
        and parent.get("claim_catalog_sha256") == PARENT_CATALOG_SHA256
        and parent.get("strict_ledger_sha256") == PARENT_STRICT_SHA256,
        "strict curation parent binding drifted",
    )
    declared_coverage = document.get("coverage_bindings")
    require(isinstance(declared_coverage, list), "strict curation coverage_bindings malformed")
    coverage_keys = {
        "source_kind", "path", "file_sha256", "size_bytes", "rows",
        "accepted_eligible", "pending", "rejected", "audit_receipt",
    }
    normalized_coverage: list[dict[str, Any]] = []
    for coverage_index, coverage_row in enumerate(declared_coverage):
        require(isinstance(coverage_row, dict), f"coverage binding {coverage_index} malformed")
        require_exact_keys(coverage_row, coverage_keys, f"coverage binding {coverage_index}")
        for count_field in ("size_bytes", "rows", "accepted_eligible", "pending", "rejected"):
            require_int(coverage_row.get(count_field), f"coverage[{coverage_index}].{count_field}", 0)
        require(
            coverage_row["accepted_eligible"] + coverage_row["pending"] + coverage_row["rejected"]
            == coverage_row["rows"],
            f"coverage binding {coverage_index} disposition counts do not close",
        )
        normalized_coverage.append(copy.deepcopy(coverage_row))
    normalized_coverage.sort(key=lambda row: (row["source_kind"], row["path"]))
    require(
        normalized_coverage == expected_coverage_bindings(authorities),
        "strict curation coverage_bindings do not exactly replay the pinned review universe",
    )
    rows = document.get("candidate_dispositions")
    require(isinstance(rows, list) and rows, "strict curation has no rows")
    existing_semantics = parent_semantic_keys(parent_records)
    accepted: list[dict[str, Any]] = []
    all_keys: set[str] = set()
    accepted_semantics: set[str] = set()
    accepted_source_records: set[tuple[str, str]] = set()
    accepted_source_paths: set[str] = set()
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"curation row {index} malformed")
        require(row.get("row_sha256") == row_hash(row), f"curation row {index} hash stale")
        candidate_key = require_str(row.get("candidate_key"), f"curation[{index}].candidate_key")
        require(candidate_key not in all_keys, f"duplicate curation candidate key: {candidate_key}")
        all_keys.add(candidate_key)
        decision = row.get("decision")
        require(decision in {"accept", "reject", "pending"}, f"curation row {index} decision invalid")
        grants = row.get("grants_catalog_entry") is True or row.get("grants_strict_conjecture_credit") is True
        if decision != "accept":
            require(not grants and row.get("accepted_rank") is None, f"nonaccepted curation row {index} grants credit")
            continue
        require(row.get("grants_catalog_entry") is True, f"accepted row {index} lacks catalog grant")
        require(row.get("grants_strict_conjecture_credit") is True, f"accepted row {index} lacks strict grant")
        rank = require_int(row.get("accepted_rank"), f"curation[{index}].accepted_rank", 1)
        source_kind = require_str(row.get("source_kind"), f"curation[{index}].source_kind", SOURCE_KIND_RE)
        require(source_kind in ALLOWED_SOURCE_KINDS, f"curation row {index} source kind is unapproved")
        source_record = require_str(row.get("source_record_key"), f"curation[{index}].source_record_key")
        require((source_kind, source_record) not in accepted_source_records, f"duplicate accepted source record at row {index}")
        source_binding = verify_source_binding(row, index, source_kind, authorities)
        statement = require_str(row.get("exact_claim_text"), f"curation[{index}].exact_claim_text")
        require("?" not in statement.strip()[-1:], f"curation row {index} appears interrogative")
        context = row.get("exact_claim_context")
        require(context is None or isinstance(context, str), f"curation row {index} context malformed")
        summary = require_str(row.get("semantic_summary"), f"curation[{index}].semantic_summary")
        semantic = require_str(row.get("semantic_key"), f"curation[{index}].semantic_key")
        require(semantic not in existing_semantics, f"curation row {index} exact semantic duplicate of parent")
        require(semantic not in accepted_semantics, f"curation row {index} accepted semantic duplicate")
        require(row.get("importance_tier") in {"high", "medium"}, f"curation row {index} importance below gate")
        require(row.get("truth_apt") is True and row.get("context_complete") is True, f"curation row {index} statement gate failed")
        require(row.get("current_open_as_of_review") is True, f"curation row {index} is not current-open")
        require(row.get("question_to_assertion_promotion_performed") is False, f"curation row {index} promotes a question")
        require(row.get("atomicity") in {"single", "source_named_compound"}, f"curation row {index} atomicity invalid")
        representation = row.get("statement_representation", "reviewed_release_assertion")
        require(
            representation in {
                "reviewed_release_assertion",
                "reviewed_exact_source_assertion",
                "independently_written_reviewed_summary",
            },
            f"curation row {index} statement representation invalid",
        )
        status = row.get("current_status_evidence")
        rights = row.get("rights")
        dedupe = row.get("dedupe")
        require(isinstance(status, dict) and bool(status), f"curation row {index} lacks status evidence")
        require(isinstance(rights, dict) and rights.get("cleared_for_catalog_metadata_and_statement") is True, f"curation row {index} rights gate failed")
        require(isinstance(rights.get("attribution"), str) and rights["attribution"].strip(), f"curation row {index} attribution missing")
        require(isinstance(dedupe, dict), f"curation row {index} dedupe malformed")
        require(dedupe.get("parent_semantic_unique") is True and dedupe.get("cross_source_semantic_unique") is True, f"curation row {index} semantic dedupe gate failed")
        if source_kind == "open_problem_garden":
            require(
                representation == "independently_written_reviewed_summary"
                and rights.get("statement_origin") == "independently_written_reviewed_summary"
                and rights.get("exact_source_wording_excluded_from_release") is True
                and rights.get("source_wording_redistributed") is False,
                f"curation row {index} OPG rights boundary failed",
            )
        normalized = copy.deepcopy(row)
        normalized["source_binding"] = source_binding
        normalized["statement_representation"] = representation
        normalized["classification"] = normalize_classification(row, index)
        normalized["_statement"] = statement
        normalized["_summary"] = summary
        accepted.append(normalized)
        accepted_semantics.add(semantic)
        accepted_source_records.add((source_kind, source_record))
        accepted_source_paths.add(source_binding["path"])
        require(rank <= MAX_NEW_STRICT, f"curation row {index} rank exceeds maximum")
    accepted.sort(key=lambda row: int(row["accepted_rank"]))
    require([row["accepted_rank"] for row in accepted] == list(range(1, len(accepted) + 1)), "accepted ranks are not dense 1..N")
    require(MIN_NEW_STRICT <= len(accepted) <= MAX_NEW_STRICT, "strict curation misses 401--1,000 addition gate")
    covered_paths = {row["path"] for row in normalized_coverage}
    require(
        accepted_source_paths <= covered_paths,
        "an accepted curation row uses a review path absent from coverage_bindings",
    )
    oeis_authority = authorities.get("oeis")
    require(isinstance(oeis_authority, dict), "pinned OEIS authority missing")
    oeis_survivors = oeis_authority.get("qualified_candidates")
    require(isinstance(oeis_survivors, list), "pinned OEIS survivor set missing")
    survivor_by_key = {
        row["candidate_key"]: row for row in oeis_survivors if isinstance(row, dict)
    }
    admitted_oeis = {
        row["candidate_key"]: row for row in accepted if row["source_kind"] == "oeis"
    }
    require(
        set(admitted_oeis) == set(survivor_by_key),
        "strict curation must admit exactly the pinned 268-row OEIS survivor set",
    )
    for candidate_key, admitted in admitted_oeis.items():
        survivor = survivor_by_key[candidate_key]
        require(
            admitted["importance_tier"] == survivor["importance_tier"]
            and admitted["semantic_summary"] == survivor["semantic_summary"],
            f"OEIS survivor metadata drifted: {candidate_key}",
        )
    counts = document.get("counts")
    require(
        isinstance(counts, dict)
        and counts.get("accepted_new_strict_conjectures") == len(accepted)
        and counts.get("pending_not_credited") == sum(row.get("decision") == "pending" for row in rows)
        and counts.get("rejected_not_credited") == sum(row.get("decision") == "reject" for row in rows),
        "strict curation counters drifted",
    )
    digests = document.get("set_digests")
    require(isinstance(digests, dict), "strict curation set digests missing")
    require(
        digests.get("accepted_semantic_key_set_sha256") == set_digest(row["semantic_key"] for row in accepted)
        and digests.get("accepted_candidate_key_set_sha256") == set_digest(row["candidate_key"] for row in accepted),
        "strict curation accepted set digests drifted",
    )
    return accepted


def expected_contract(
    curation: Mapping[str, Any], important: Mapping[str, Any], frontier: Mapping[str, Any],
    source_authorities: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    return seal(
        {
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
                "effective_strict_conjectures_min": MIN_EFFECTIVE_STRICT,
                "effective_strict_conjectures_max": MAX_EFFECTIVE_STRICT,
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
                "strict_conjecture_curation": binding(CURATION_PATH, curation),
                "important_theorem_inventory": binding(IMPORTANT_PATH, important),
                "frontier_theorem_qualification": binding(FRONTIER_PATH, frontier),
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
                "root": "Docs/catalog/v5/releases/5.5",
                "manifest_name": MANIFEST_NAME,
                "non_manifest_artifacts": list(RELEASE_FILES),
                "manifest_excluded_from_release_root": True,
            },
            "publication": {
                "compare_and_swap_parent_pointer_sha256": PARENT_CURRENT_SHA256,
                "write_does_not_publish": True,
                "publish_current_requires_authenticated_5_4_or_idempotent_5_5": True,
                "independent_checker_path": repo_relative(CHECKER_PATH),
                "independent_acceptance_receipt_path": repo_relative(INDEPENDENT_RECEIPT_PATH),
                "independent_receipt_and_live_prepublish_replay_required": True,
            },
        }
    )


def verify_or_write_contract(expected: Mapping[str, Any], *, write: bool) -> None:
    payload = encoded(expected)
    if write:
        CONTRACT_PATH.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(CONTRACT_PATH, payload)
        return
    require(CONTRACT_PATH.is_file(), "5.5 contract is missing")
    require(CONTRACT_PATH.read_bytes() == payload, "5.5 contract is stale")


def allocation_sha(row: Mapping[str, Any], ordinal: int) -> str:
    return digest(
        canonical(
            {
                "release": RELEASE,
                "ordinal": ordinal,
                "candidate_key": row["candidate_key"],
                "semantic_key": row["semantic_key"],
                "source_kind": row["source_kind"],
                "source_record_key": row["source_record_key"],
                "curation_row_sha256": row["row_sha256"],
            }
        )
    )


def statement_payload(row: Mapping[str, Any]) -> dict[str, Any]:
    statement = row["_statement"]
    context = row.get("exact_claim_context")
    summary = row["_summary"]
    result = {
        "language": row.get("statement_language", "en_or_mathematical_notation"),
        "representation": row["statement_representation"],
        "exact_claim_text": statement,
        "exact_claim_context": context,
        "semantic_summary": summary,
        "statement_sha256": digest(canonical({"claim": statement, "context": context})),
        "summary_sha256": digest(summary.encode("utf-8")),
        "completeness": "reviewed_context_complete",
    }
    return result


def build_claim(row: Mapping[str, Any], rank: int, curation: Mapping[str, Any]) -> dict[str, Any]:
    ordinal = PARENT_ATV_HIGH + rank
    family_ordinal = PARENT_ATF_HIGH + rank
    atv = f"ATV-{ordinal:08d}"
    ato = f"ATO-{ordinal:08d}"
    ats = f"ATS-{ordinal:08d}"
    atf = f"ATF-{family_ordinal:08d}"
    sid = f"S5-CLM-{ordinal:08d}"
    request = allocation_sha(row, ordinal)
    statement = statement_payload(row)
    semantic_payload = digest(
        canonical(
            {
                "semantic_key": row["semantic_key"],
                "statement_sha256": statement["statement_sha256"],
                "source_kind": row["source_kind"],
            }
        )
    )
    display = row.get("display_name") or row["semantic_summary"]
    require_str(display, f"accepted rank {rank} display name")
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
            "ledger_path": repo_relative(CURATION_PATH),
            "ledger_file_sha256": sha_file(CURATION_PATH),
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
            "curation_path": repo_relative(CURATION_PATH),
            "curation_authority_sha256": curation["authority_sha256"],
            "curation_row_sha256": row["row_sha256"],
            "question_to_assertion_promotion_performed": False,
        },
        "lineage": [],
    }
    result["content_payload_sha256"] = digest(
        canonical(
            {
                "statement": statement,
                "status": result["status_detail"],
                "rights": result["rights"],
                "dedupe": result["dedupe"],
            }
        )
    )
    result["catalog_record_sha256"] = row_hash(result, "catalog_record_sha256")
    require(set(result) == set(ORIGIN_5_5_RECORD_KEYS), "origin 5.5 catalog record schema drifted")
    return result


def theorem_predicate(row: Mapping[str, Any]) -> bool:
    return bool(
        row.get("record_role") == "claim"
        and row.get("lifecycle") == "active"
        and row.get("truth_apt") is True
        and row.get("current_claim_kind") == "theorem"
        and row.get("material_status") == "proved"
    )


def open_predicate(row: Mapping[str, Any]) -> bool:
    return bool(
        row.get("record_role") == "claim"
        and row.get("lifecycle") == "active"
        and row.get("truth_apt") is True
        and row.get("category") == "open_claim"
        and row.get("current_claim_kind") in {"conjecture", "hypothesis", "open_problem"}
        and row.get("material_status") in {"open", "partial", "independent", "disputed"}
    )


def authoritative_inputs(
    contract: Mapping[str, Any], curation: Mapping[str, Any], important: Mapping[str, Any],
    frontier: Mapping[str, Any], parent: Mapping[str, Mapping[str, Any]],
    source_authorities: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "contract": binding(CONTRACT_PATH, contract),
        "strict_conjecture_curation": binding(CURATION_PATH, curation),
        "important_theorem_inventory": binding(IMPORTANT_PATH, important),
        "frontier_theorem_qualification": binding(FRONTIER_PATH, frontier),
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


def registry_rows(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    families: list[dict[str, Any]] = []
    senses: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    for row in rows:
        request = row["allocation"]["allocation_request_sha256"]
        families.append(
            {
                "family_id": row["family_id"],
                "curation_key": row["curation_key"],
                "display_titles": list(dict.fromkeys([row["display_name"], *row["aliases"]])),
                "member_occurrence_ids": [row["occurrence_id"]],
                "historical_member_occurrence_ids": [row["occurrence_id"]],
                "idempotency_request_sha256": request,
                "identity_state": "stage5_reviewed_strict_conjecture_family",
                "lifecycle": "current",
                "semantic_equivalence_asserted": True,
            }
        )
        senses.append(
            {
                "sense_id": row["sense_id"],
                "family_id": row["family_id"],
                "bootstrap_occurrence_id": row["occurrence_id"],
                "curation_key": row["curation_key"],
                "idempotency_request_sha256": request,
                "identity_state": "stage5_reviewed_strict_conjecture_sense",
                "lifecycle": "current",
            }
        )
        variants.append(
            {
                "variant_id": row["variant_id"],
                "sense_id": row["sense_id"],
                "bootstrap_occurrence_id": row["occurrence_id"],
                "curation_key": row["curation_key"],
                "idempotency_request_sha256": request,
                "semantic_payload_sha256": row["semantic_payload_sha256"],
                "identity_state": "stage5_reviewed_strict_conjecture_variant",
                "lifecycle": "current",
            }
        )
    return families, senses, variants


def strict_credit(row: Mapping[str, Any]) -> dict[str, Any]:
    credit = {
        "stage_claim_id": row["stage_claim_id"],
        "variant_id": row["variant_id"],
        "semantic_key": row["semantic_key"],
        "origin_release": RELEASE,
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
    require(set(credit) == set(ORIGIN_5_5_STRICT_CREDIT_KEYS), "origin 5.5 strict credit schema drifted")
    return credit


def build_artifacts(
    parent: Mapping[str, Mapping[str, Any]], rows: Sequence[dict[str, Any]], inputs: Mapping[str, Any],
    curation: Mapping[str, Any], important: Mapping[str, Any], frontier: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    parent_catalog = parent["Claim_Catalog.json"]
    records = copy.deepcopy(parent_catalog["records"]) + copy.deepcopy(list(rows))
    catalog = seal(
        {
            "schema_version": "awesome-theorems/stage5-claim-catalog/5.5",
            "artifact": "Claim_Catalog.json",
            "release": RELEASE,
            "catalog_scope": parent_catalog["catalog_scope"],
            "authoritative_inputs": copy.deepcopy(inputs),
            "quality_qualification": {
                "important_theorems": IMPORTANT_COUNT,
                "additional_frontier_theorems": len(frontier["accepted_credits"]),
                "unsupported_credit": 0,
            },
            "origin_5_5_closed_schema": {
                "closed": True,
                "record_keys": sorted(ORIGIN_5_5_RECORD_KEYS),
                "record_hash_field": "catalog_record_sha256",
                "record_hash_rule": (
                    "SHA-256 of canonical JSON after omitting catalog_record_sha256"
                ),
                "origin_records": len(rows),
            },
            "counts": {
                "records": len(records),
                "origin_theorems": 0,
                "origin_open_claims": len(rows),
                "origin_strict_conjectures": len(rows),
                "cumulative_theorems": sum(theorem_predicate(row) for row in records),
                "cumulative_open_claims": sum(open_predicate(row) for row in records),
                "effective_strict_conjectures": 1_000 + len(rows),
            },
            "records": records,
        }
    )

    parent_registry = parent["Claim_ID_Registry.json"]
    families, senses, variants = registry_rows(rows)
    allocation_policy = copy.deepcopy(parent_registry["allocation_policy"])
    allocation_policy.update(
        {
            "release_5_5_first_new_atv_ordinal": PARENT_ATV_HIGH + 1,
            "release_5_5_new_family_first_atf_ordinal": PARENT_ATF_HIGH + 1,
        }
    )
    registry = seal(
        {
            "schema_version": "awesome-theorems/claim-id-registry/5.5",
            "artifact": "Claim_ID_Registry.json",
            "release": RELEASE,
            "parent_registry_authority_sha256": parent_registry["authority_sha256"],
            "baseline_registry_authority_sha256": parent_registry["baseline_registry_authority_sha256"],
            "authoritative_inputs": copy.deepcopy(inputs),
            "allocation_policy": allocation_policy,
            "namespace_high_watermarks": {
                "ATF": PARENT_ATF_HIGH + len(rows),
                "ATO": PARENT_ATV_HIGH + len(rows),
                "ATS": PARENT_ATV_HIGH + len(rows),
                "ATV": PARENT_ATV_HIGH + len(rows),
            },
            "families": copy.deepcopy(parent_registry["families"]) + families,
            "senses": copy.deepcopy(parent_registry["senses"]) + senses,
            "variants": copy.deepcopy(parent_registry["variants"]) + variants,
            "legacy_aliases": copy.deepcopy(parent_registry["legacy_aliases"]),
            "redirects": copy.deepcopy(parent_registry["redirects"]),
            "splits": copy.deepcopy(parent_registry["splits"]),
            "family_membership_extensions": copy.deepcopy(parent_registry["family_membership_extensions"]),
            "counts": {
                "families": len(parent_registry["families"]) + len(rows),
                "senses": len(parent_registry["senses"]) + len(rows),
                "variants": len(parent_registry["variants"]) + len(rows),
                "stage4_variants": parent_registry["counts"]["stage4_variants"],
                "stage5_additions": parent_registry["counts"]["stage5_additions"] + len(rows),
                "legacy_aliases": len(parent_registry["legacy_aliases"]),
                "redirects": len(parent_registry["redirects"]),
                "splits": len(parent_registry["splits"]),
            },
        }
    )

    parent_stage = parent["Stage5_Claim_ID_Registry.json"]
    mappings = copy.deepcopy(parent_stage["mappings"]) + [
        {
            "ordinal": int(ATV_RE.fullmatch(row["variant_id"]).group(1)),
            "variant_id": row["variant_id"],
            "predecessor_stage_claim_id": None,
            "stage_claim_id": row["stage_claim_id"],
            "lifecycle": "current",
        }
        for row in rows
    ]
    stage_registry = seal(
        {
            "schema_version": "awesome-theorems/stage5-claim-id-registry/5.5",
            "artifact": "Stage5_Claim_ID_Registry.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "numbering_policy": parent_stage["numbering_policy"],
            "counts": {"mappings": len(mappings)},
            "mappings": mappings,
        }
    )

    parent_migration = parent["Migration_v4_to_v5.json"]
    migrations = copy.deepcopy(parent_migration["migrations"]) + [
        {
            "ordinal": int(ATV_RE.fullmatch(row["variant_id"]).group(1)),
            "variant_id": row["variant_id"],
            "v4_variant_id": None,
            "s4_claim_id": None,
            "stage_claim_id": row["stage_claim_id"],
            "migration_action": "new_stage5_allocation",
            "predecessor_record_sha256": None,
            "current_resolution": {
                "kind": "current",
                "terminal_atv_ids": [row["variant_id"]],
                "terminal_s5_ids": [row["stage_claim_id"]],
                "default_child": None,
                "evidence_inherited": False,
            },
        }
        for row in rows
    ]
    migration = seal(
        {
            "schema_version": "awesome-theorems/migration-v4-to-v5/5.5",
            "artifact": "Migration_v4_to_v5.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "v4_import_receipt": copy.deepcopy(parent_migration["v4_import_receipt"]),
            "counts": {
                "historical_bindings": parent_migration["counts"]["historical_bindings"],
                "new_allocations": parent_migration["counts"]["new_allocations"] + len(rows),
                "migrations": len(migrations),
            },
            "migrations": migrations,
        }
    )

    theorem_rows = [row for row in records if theorem_predicate(row)]
    open_rows = [row for row in records if open_predicate(row)]
    theorem = seal(
        {
            "schema_version": "awesome-theorems/stage5-query-projection/5.5",
            "artifact": "Theorem_List.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "query": "pure predicate over Claim_Catalog.json; records copied byte-semantically",
            "stage_claim_ids": [row["stage_claim_id"] for row in theorem_rows],
            "counts": {"records": len(theorem_rows)},
            "records": theorem_rows,
        }
    )
    open_list = seal(
        {
            "schema_version": "awesome-theorems/stage5-query-projection/5.5",
            "artifact": "Open_Claim_List.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "query": "pure predicate over Claim_Catalog.json; records copied byte-semantically",
            "stage_claim_ids": [row["stage_claim_id"] for row in open_rows],
            "counts": {"records": len(open_rows)},
            "records": open_rows,
        }
    )

    parent_coverage = parent["Coverage_Ledger.json"]
    additions = [
        {
            "candidate_key": f"strict-v5.5:{row['curator_disposition']['candidate_key']}",
            "source_id": row["source_id"],
            "source_record_id": row["source_record_key"],
            "semantic_key": row["semantic_key"],
            "disposition": "accepted_new_strict_open_claim",
            "reason_code": "all_strict_release_gates_pass",
            "accepted_rank": row["curator_disposition"]["accepted_rank"],
            "target_variant_id": row["variant_id"],
            "target_s5_id": row["stage_claim_id"],
            "catalog_record_sha256": row["catalog_record_sha256"],
            "grants_catalog_entry": True,
            "grants_strict_conjecture_credit": True,
            "origin_release": RELEASE,
            "curation_row_sha256": row["curator_disposition"]["ledger_row_sha256"],
            "source_review_row_sha256": row["source_locator"]["source_row_sha256"],
            "source_authority_file_sha256": row["source_locator"]["authority_receipt"]["file_sha256"],
            "supersedes_candidate_key": None,
            "transition_from_disposition": "new_source_candidate",
        }
        for row in rows
    ]
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
        projected["current_open_s5_ids"] = sorted(
            [*projected["current_open_s5_ids"], *new_ids]
        )
        projected["origin_open_s5_ids"] = new_ids
        projected["origin_theorem_s5_ids"] = []
        if classified_additions:
            projected["source_ids"] = sorted(
                set(projected["source_ids"])
                | {claim["source_id"] for claim in classified_additions}
            )
        projected["classification_basis_counts"]["independent_review"] += len(
            classified_additions
        )
        projected["counts"]["current_theorems"] = len(
            projected["current_theorem_s5_ids"]
        )
        projected["counts"]["current_open"] = len(projected["current_open_s5_ids"])
        projected["counts"]["origin_theorems"] = 0
        projected["counts"]["origin_open"] = len(new_ids)
        projected["counts"]["open_reserve"] = len(
            projected["open_reserve_candidate_keys"]
        )
        classified = (
            projected["counts"]["current_theorems"]
            + projected["counts"]["current_open"]
            + projected["counts"]["open_reserve"]
        )
        if classified == 0:
            projected["scarcity"] = "zero"
            projected["scarcity_reason"] = (
                "No current or open-reserve member has this primary source annotation."
            )
        elif classified < 10:
            projected["scarcity"] = "thin"
            projected["scarcity_reason"] = (
                "Fewer than ten current-plus-reserve members have this primary class."
            )
        else:
            projected["scarcity"] = "adequate_in_source_inventory"
            projected["scarcity_reason"] = (
                "At least ten current-plus-reserve members have this primary class."
            )
        msc_rows.append(projected)
    require(not by_msc, f"new rows use unknown MSC roots: {sorted(by_msc)}")
    coverage = seal(
        {
            "schema_version": "awesome-theorems/stage5-coverage-ledger/5.5",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "effective_state_policy": {
                "identity_fields": ["source_id", "source_record_id"],
                "supersession_field": "supersedes_candidate_key",
                "effective_rule": (
                    "A candidate row is effective exactly when no later appended row "
                    "names its candidate_key in supersedes_candidate_key."
                ),
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
                "origin_5_5_candidates": len(rows),
                "origin_5_5_accepted_new_strict_conjectures": len(rows),
                "origin_5_5_pending_or_rejected_release_rows": 0,
                "origin_5_5_msc_assigned": len(rows) - len(unassigned_msc),
                "origin_5_5_msc_unassigned": len(unassigned_msc),
            },
        }
    )

    parent_strict = parent["Strict_Conjecture_Ledger.json"]
    new_credits = [strict_credit(row) for row in rows]
    credits = copy.deepcopy(parent_strict["strict_credits"]) + new_credits
    strict = seal(
        {
            "schema_version": "awesome-theorems/stage5-strict-conjecture-ledger/5.5",
            "release": RELEASE,
            "parent_release_root_sha256": PARENT_RELEASE_ROOT,
            "parent_strict_ledger_file_sha256": PARENT_STRICT_SHA256,
            "parent_strict_ledger_authority_sha256": parent_strict["authority_sha256"],
            "origin_5_5_closed_credit_schema": {
                "closed": True,
                "credit_keys": sorted(ORIGIN_5_5_STRICT_CREDIT_KEYS),
                "row_hash_field": "row_sha256",
                "row_hash_rule": "SHA-256 of canonical JSON after omitting row_sha256",
                "origin_credits": len(new_credits),
            },
            "strict_credits": credits,
            "credit_corrections": copy.deepcopy(parent_strict["credit_corrections"]),
            "counts": {
                "credit_corrections": len(parent_strict["credit_corrections"]),
                "effective_parent_credits": 1_000,
                "origin_5_2_credits": 600,
                "origin_5_5_credits": len(new_credits),
                "effective_strict_credits": len(credits),
                "stage5_5_0_baseline_strict_credits": BASELINE_5_0_STRICT,
                "net_strict_increase_after_5_0": len(credits) - BASELINE_5_0_STRICT,
            },
            "set_digests": {
                "effective_s5_id_set_sha256": set_digest(row["stage_claim_id"] for row in credits),
                "effective_variant_id_set_sha256": set_digest(row["variant_id"] for row in credits),
                "origin_5_5_s5_id_set_sha256": set_digest(row["stage_claim_id"] for row in new_credits),
                "origin_5_5_semantic_key_set_sha256": set_digest(row["semantic_key"] for row in new_credits),
            },
        }
    )
    artifacts = {
        "Claim_Catalog.json": catalog,
        "Claim_ID_Registry.json": registry,
        "Stage5_Claim_ID_Registry.json": stage_registry,
        "Migration_v4_to_v5.json": migration,
        "Theorem_List.json": theorem,
        "Open_Claim_List.json": open_list,
        "Coverage_Ledger.json": coverage,
        "Strict_Conjecture_Ledger.json": strict,
    }
    validate_artifacts(artifacts, parent, rows, important, frontier)
    return artifacts


def validate_artifacts(
    artifacts: Mapping[str, Mapping[str, Any]], parent: Mapping[str, Mapping[str, Any]],
    rows: Sequence[Mapping[str, Any]], important: Mapping[str, Any], frontier: Mapping[str, Any],
) -> None:
    require(set(artifacts) == set(RELEASE_FILES), "5.5 artifact set drifted")
    for name, document in artifacts.items():
        verify_seal(document, name)
    count = len(rows)
    catalog = artifacts["Claim_Catalog.json"]
    require(catalog["records"][:4_100] == parent["Claim_Catalog.json"]["records"], "catalog parent prefix changed")
    require(catalog["records"][4_100:] == list(rows), "catalog append differs from curation")
    require(
        catalog["origin_5_5_closed_schema"]["record_keys"]
        == sorted(ORIGIN_5_5_RECORD_KEYS),
        "catalog origin 5.5 closed schema drifted",
    )
    for index, row in enumerate(rows, start=1):
        require_exact_keys(row, ORIGIN_5_5_RECORD_KEYS, f"origin 5.5 record {index}")
        require(row.get("origin_release") == RELEASE, f"origin 5.5 record {index} release drifted")
        require(
            row.get("catalog_record_sha256") == row_hash(row, "catalog_record_sha256"),
            f"origin 5.5 record {index} catalog hash drifted",
        )
        require(
            row["allocation"]["allocation_request_sha256"]
            == digest(
                canonical(
                    {
                        "release": RELEASE,
                        "ordinal": PARENT_ATV_HIGH + index,
                        "candidate_key": row["curator_disposition"]["candidate_key"],
                        "semantic_key": row["semantic_key"],
                        "source_kind": row["provenance"]["source_kind"],
                        "source_record_key": row["source_record_key"],
                        "curation_row_sha256": row["curator_disposition"]["ledger_row_sha256"],
                    }
                )
            ),
            f"origin 5.5 record {index} allocation request drifted",
        )
    require(catalog["counts"] == {
        "records": 4_100 + count,
        "origin_theorems": 0,
        "origin_open_claims": count,
        "origin_strict_conjectures": count,
        "cumulative_theorems": 2_500,
        "cumulative_open_claims": 1_600 + count,
        "effective_strict_conjectures": 1_000 + count,
    }, "catalog counts drifted")
    require(artifacts["Theorem_List.json"]["records"] == parent["Theorem_List.json"]["records"], "theorem projection changed")
    require(artifacts["Open_Claim_List.json"]["records"][:1_600] == parent["Open_Claim_List.json"]["records"], "open parent prefix changed")
    require(
        artifacts["Open_Claim_List.json"]["records"][1_600:] == list(rows),
        "open projection does not contain the complete catalog append",
    )
    require(
        artifacts["Theorem_List.json"]["stage_claim_ids"]
        == [row["stage_claim_id"] for row in artifacts["Theorem_List.json"]["records"]]
        and artifacts["Open_Claim_List.json"]["stage_claim_ids"]
        == [row["stage_claim_id"] for row in artifacts["Open_Claim_List.json"]["records"]],
        "projection ID arrays drifted",
    )
    for artifact, key in (
        ("Claim_ID_Registry.json", "families"),
        ("Claim_ID_Registry.json", "senses"),
        ("Claim_ID_Registry.json", "variants"),
        ("Stage5_Claim_ID_Registry.json", "mappings"),
        ("Migration_v4_to_v5.json", "migrations"),
        ("Coverage_Ledger.json", "candidate_dispositions"),
    ):
        parent_rows = parent[artifact][key]
        require(artifacts[artifact][key][: len(parent_rows)] == parent_rows, f"{artifact}.{key} parent prefix changed")
    registry = artifacts["Claim_ID_Registry.json"]
    parent_registry = parent["Claim_ID_Registry.json"]
    require(
        registry["baseline_registry_authority_sha256"]
        == parent_registry["baseline_registry_authority_sha256"]
        and registry["parent_registry_authority_sha256"]
        == parent_registry["authority_sha256"],
        "Claim_ID_Registry ancestry drifted",
    )
    for key in ("legacy_aliases", "redirects", "splits", "family_membership_extensions"):
        require(registry[key] == parent_registry[key], f"Claim_ID_Registry.{key} changed")
    require(
        artifacts["Stage5_Claim_ID_Registry.json"]["numbering_policy"]
        == parent["Stage5_Claim_ID_Registry.json"]["numbering_policy"],
        "Stage5 numbering policy changed",
    )
    require(
        artifacts["Migration_v4_to_v5.json"]["v4_import_receipt"]
        == parent["Migration_v4_to_v5.json"]["v4_import_receipt"],
        "v4 import receipt changed",
    )
    expected_atv = [f"ATV-{value:08d}" for value in range(PARENT_ATV_HIGH + 1, PARENT_ATV_HIGH + count + 1)]
    expected_atf = [f"ATF-{value:08d}" for value in range(PARENT_ATF_HIGH + 1, PARENT_ATF_HIGH + count + 1)]
    require([row["variant_id"] for row in rows] == expected_atv, "new ATV allocation drifted")
    require([row["family_id"] for row in rows] == expected_atf, "new ATF allocation drifted")
    require([row["stage_claim_id"] for row in rows] == [value.replace("ATV-", "S5-CLM-") for value in expected_atv], "new S5 allocation drifted")
    require(
        registry["namespace_high_watermarks"] == {
            "ATF": PARENT_ATF_HIGH + count,
            "ATO": PARENT_ATV_HIGH + count,
            "ATS": PARENT_ATV_HIGH + count,
            "ATV": PARENT_ATV_HIGH + count,
        },
        "registry high-watermarks drifted",
    )
    new_families = registry["families"][len(parent_registry["families"]) :]
    new_senses = registry["senses"][len(parent_registry["senses"]) :]
    new_variants = registry["variants"][len(parent_registry["variants"]) :]
    for index, (claim, family, sense, variant) in enumerate(
        zip(rows, new_families, new_senses, new_variants, strict=True), start=1
    ):
        request = claim["allocation"]["allocation_request_sha256"]
        require(
            family["idempotency_request_sha256"]
            == sense["idempotency_request_sha256"]
            == variant["idempotency_request_sha256"]
            == request,
            f"origin 5.5 registry request {index} drifted",
        )
    strict = artifacts["Strict_Conjecture_Ledger.json"]
    require(strict["strict_credits"][:1_000] == parent["Strict_Conjecture_Ledger.json"]["strict_credits"], "strict parent prefix changed")
    require(strict["credit_corrections"] == parent["Strict_Conjecture_Ledger.json"]["credit_corrections"], "strict corrections changed")
    new_credits = strict["strict_credits"][1_000:]
    require(len(new_credits) == count, "strict credit append count drifted")
    for index, (claim, credit) in enumerate(zip(rows, new_credits, strict=True), start=1):
        require_exact_keys(credit, ORIGIN_5_5_STRICT_CREDIT_KEYS, f"origin 5.5 strict credit {index}")
        require(credit["row_sha256"] == row_hash(credit), f"origin 5.5 strict credit {index} hash drifted")
        require(
            credit["stage_claim_id"] == claim["stage_claim_id"]
            and credit["variant_id"] == claim["variant_id"]
            and credit["semantic_key"] == claim["semantic_key"]
            and credit["catalog_record_sha256"] == claim["catalog_record_sha256"]
            and credit["statement_sha256"] == claim["mathematical_statement"]["statement_sha256"]
            and credit["curation_row_sha256"] == claim["curator_disposition"]["ledger_row_sha256"]
            and credit["source_row_sha256"] == claim["source_locator"]["source_row_sha256"]
            and credit["source_authority_file_sha256"]
            == claim["source_locator"]["authority_receipt"]["file_sha256"]
            and credit["allocation_request_sha256"]
            == claim["allocation"]["allocation_request_sha256"],
            f"origin 5.5 strict credit {index} is not fully bound to its catalog record",
        )
    require(MIN_EFFECTIVE_STRICT <= len(strict["strict_credits"]) <= MAX_EFFECTIVE_STRICT, "effective strict range failed")
    require(strict["counts"]["net_strict_increase_after_5_0"] >= MIN_NET_STRICT_AFTER_5_0, "net strict increase gate failed")
    require(len(important["records"]) == IMPORTANT_COUNT, "important count drifted during build")
    require(MIN_FRONTIER <= len(frontier["accepted_credits"]) <= MAX_FRONTIER, "frontier count drifted during build")
    require(len({row["stage_claim_id"] for row in catalog["records"]}) == len(catalog["records"]), "catalog S5 IDs collide")
    require(len({row["variant_id"] for row in catalog["records"]}) == len(catalog["records"]), "catalog ATV IDs collide")
    coverage = artifacts["Coverage_Ledger.json"]
    coverage_candidate_keys = [
        row.get("candidate_key") for row in coverage["candidate_dispositions"]
    ]
    require(
        all(isinstance(value, str) and value for value in coverage_candidate_keys)
        and len(coverage_candidate_keys) == len(set(coverage_candidate_keys)),
        "coverage candidate keys are missing or duplicated",
    )
    require(
        coverage["counts"]["origin_5_5_msc_assigned"]
        + coverage["counts"]["origin_5_5_msc_unassigned"]
        == count,
        "coverage MSC accounting drifted",
    )
    projected_origin_ids = [
        stage_id
        for coverage_row in coverage["msc_coverage"]
        for stage_id in coverage_row["origin_open_s5_ids"]
    ]
    expected_projected_ids = [
        row["stage_claim_id"]
        for row in rows
        if row["classification"]["primary_msc_top_class"] is not None
    ]
    require(
        sorted(projected_origin_ids) == sorted(expected_projected_ids)
        and len(projected_origin_ids) == len(set(projected_origin_ids)),
        "coverage MSC projection is incomplete or duplicated",
    )


def package_release(
    artifacts: Mapping[str, Mapping[str, Any]], inputs: Mapping[str, Any], curation: Mapping[str, Any],
    important: Mapping[str, Any], frontier: Mapping[str, Any],
) -> tuple[dict[str, bytes], str, dict[str, Any]]:
    package = {name: encoded(artifacts[name]) for name in RELEASE_FILES}
    inventory = [
        {
            "path": name,
            "sha256": digest(package[name]),
            "size_bytes": len(package[name]),
            "row_count": primary_rows(artifacts[name]),
        }
        for name in sorted(RELEASE_FILES)
    ]
    root = release_root(inventory)
    strict = artifacts["Strict_Conjecture_Ledger.json"]
    manifest = seal(
        {
            "schema_version": "awesome-theorems/stage5-release-manifest/5.5",
            "release": RELEASE,
            "parent_release": PARENT_RELEASE,
            "parent_release_root_sha256": PARENT_RELEASE_ROOT,
            "release_root_sha256": root,
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
                "file_sha256": digest(package["Strict_Conjecture_Ledger.json"]),
                "authority_sha256": strict["authority_sha256"],
                "effective_s5_id_set_sha256": strict["set_digests"]["effective_s5_id_set_sha256"],
                "effective_variant_id_set_sha256": strict["set_digests"]["effective_variant_id_set_sha256"],
            },
            "accepted_set_digests": {
                "new_candidate_key_set_sha256": curation["set_digests"]["accepted_candidate_key_set_sha256"],
                "new_semantic_key_set_sha256": curation["set_digests"]["accepted_semantic_key_set_sha256"],
                "new_catalog_record_set_sha256": set_digest(
                    row["catalog_record_sha256"]
                    for row in artifacts["Claim_Catalog.json"]["records"]
                    if row.get("origin_release") == RELEASE
                ),
                "new_strict_credit_row_set_sha256": set_digest(
                    row["row_sha256"]
                    for row in strict["strict_credits"]
                    if row.get("origin_release") == RELEASE
                ),
            },
            "artifacts": inventory,
            "counts": {
                "non_manifest_artifacts": len(inventory),
                "catalog_records": artifacts["Claim_Catalog.json"]["counts"]["records"],
                "origin_theorems": 0,
                "origin_open_claims": sum(
                    row.get("decision") == "accept"
                    for row in curation["candidate_dispositions"]
                ),
                "origin_strict_conjectures": strict["counts"]["origin_5_5_credits"],
                "cumulative_theorems": 2_500,
                "cumulative_open_claims": artifacts["Open_Claim_List.json"]["counts"]["records"],
                "effective_strict_conjecture_credits": strict["counts"]["effective_strict_credits"],
                "net_strict_increase_after_5_0": strict["counts"]["net_strict_increase_after_5_0"],
            },
        }
    )
    require(manifest["counts"]["origin_open_claims"] == strict["counts"]["origin_5_5_credits"], "manifest origin count mismatch")
    package[MANIFEST_NAME] = encoded(manifest)
    return package, root, manifest


def build_all(*, write_contract: bool) -> tuple[dict[str, bytes], str, dict[str, Any]]:
    parent = verify_parent()
    source_authorities = load_source_authority_allowlist()
    curation = load_json(CURATION_PATH, "strict conjecture curation")
    important = load_json(IMPORTANT_PATH, "important theorem inventory")
    frontier = load_json(FRONTIER_PATH, "frontier theorem qualification")
    parent_theorems = {
        row["stage_claim_id"]: row for row in parent["Theorem_List.json"]["records"]
    }
    important_rows = verify_important(important, parent_theorems)
    verify_frontier(frontier, parent_theorems, {row["stage_claim_id"] for row in important_rows})
    accepted = verify_curation(
        curation, parent["Claim_Catalog.json"]["records"], source_authorities
    )
    contract = expected_contract(curation, important, frontier, source_authorities)
    verify_or_write_contract(contract, write=write_contract)
    inputs = authoritative_inputs(
        contract, curation, important, frontier, parent, source_authorities
    )
    rows = [build_claim(row, index, curation) for index, row in enumerate(accepted, start=1)]
    artifacts = build_artifacts(parent, rows, inputs, curation, important, frontier)
    return package_release(artifacts, inputs, curation, important, frontier)


def compare_package(package: Mapping[str, bytes]) -> None:
    require(RELEASE_DIR.is_dir(), "release 5.5 directory is missing")
    names = {path.name for path in RELEASE_DIR.iterdir() if path.is_file()}
    require(names == set(package), "release 5.5 artifact inventory differs")
    for name, payload in package.items():
        require((RELEASE_DIR / name).read_bytes() == payload, f"release 5.5 byte drift: {name}")


def verify_independent_acceptance(
    package: Mapping[str, bytes], root: str, manifest: Mapping[str, Any],
    *, checker_boundary: str | None,
) -> None:
    checker = safe_repo_file(
        "Docs/catalog/v5/tools/check_math_catalog_v5_5.py",
        "independent 5.5 checker",
    )
    receipt_path = safe_repo_file(
        "Docs/catalog/v5/receipts/V5_5_Independent_Acceptance_Receipt.json",
        "independent 5.5 acceptance receipt",
    )
    checker_sha_before = sha_file(checker)
    receipt_sha_before = sha_file(receipt_path)
    receipt = load_json(receipt_path, "independent 5.5 acceptance receipt")
    require_exact_keys(receipt, INDEPENDENT_RECEIPT_KEYS, "independent 5.5 acceptance receipt")
    verify_seal(receipt, "independent 5.5 acceptance receipt")
    inputs = manifest.get("authoritative_inputs")
    require(isinstance(inputs, dict), "5.5 manifest authoritative inputs malformed")
    expected = {
        "schema_version": "awesome-theorems/stage5-independent-release-acceptance/5.5",
        "release": RELEASE,
        "release_root_sha256": root,
        "manifest_file_sha256": digest(package[MANIFEST_NAME]),
        "manifest_authority_sha256": manifest["authority_sha256"],
        "curation_authority_sha256": inputs["strict_conjecture_curation"]["authority_sha256"],
        "important_authority_sha256": inputs["important_theorem_inventory"]["authority_sha256"],
        "frontier_authority_sha256": inputs["frontier_theorem_qualification"]["authority_sha256"],
        "counts": manifest["counts"],
        "findings": [],
        "checker_file_sha256": checker_sha_before,
    }
    for key, value in expected.items():
        require(receipt.get(key) == value, f"independent acceptance receipt {key} drifted")
    if checker_boundary is None:
        return
    require(
        checker_boundary in {"prepublish", "published"},
        "invalid independent checker publication boundary",
    )
    try:
        completed = subprocess.run(
            [
                sys.executable,
                str(checker),
                "--repo-root",
                str(REPO_ROOT),
                f"--{checker_boundary}",
                "--quiet",
            ],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise GenerationError(f"independent 5.5 checker could not run: {error}") from error
    require(
        completed.returncode == 0,
        f"independent 5.5 checker rejected {checker_boundary} validation: "
        f"stdout={completed.stdout[-2000:]!r} stderr={completed.stderr[-2000:]!r}",
    )
    require(
        sha_file(checker) == checker_sha_before,
        "independent 5.5 checker changed during live prepublication replay",
    )
    require(
        sha_file(receipt_path) == receipt_sha_before,
        "independent 5.5 acceptance receipt changed during live replay",
    )


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def write_release(package: Mapping[str, bytes]) -> None:
    RELEASE_DIR.parent.mkdir(parents=True, exist_ok=True)
    if RELEASE_DIR.exists():
        compare_package(package)
        return
    temporary = Path(tempfile.mkdtemp(prefix=".5.5.tmp-", dir=RELEASE_DIR.parent))
    try:
        for name, payload in package.items():
            atomic_write(temporary / name, payload)
        os.replace(temporary, RELEASE_DIR)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    compare_package(package)


def expected_current(root: str, manifest_payload: bytes) -> dict[str, Any]:
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-current-release/5.5",
            "release": RELEASE,
            "manifest_path": "releases/5.5/Release_Manifest.json",
            "manifest_sha256": digest(manifest_payload),
            "release_root_sha256": root,
        }
    )


@contextmanager
def writer_lock() -> Iterator[None]:
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOCK_PATH.open("a+b") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        yield


def publish_current(
    package: Mapping[str, bytes], root: str, manifest: Mapping[str, Any]
) -> None:
    target = expected_current(root, package[MANIFEST_NAME])
    target_payload = encoded(target)
    with writer_lock():
        current_bytes = CURRENT_PATH.read_bytes()
        current = load_json(CURRENT_PATH, "Current_Release")
        verify_seal(current, "Current_Release")
        if current.get("release") == RELEASE:
            require(current_bytes == target_payload, "existing 5.5 pointer differs")
            compare_package(package)
            verify_independent_acceptance(
                package, root, manifest, checker_boundary="published"
            )
            require(
                CURRENT_PATH.read_bytes() == current_bytes,
                "Current_Release changed during published-state validation",
            )
            compare_package(package)
            return
        require(current.get("release") == PARENT_RELEASE, "Current_Release is not 5.4")
        require(digest(current_bytes) == PARENT_CURRENT_SHA256, "5.4 Current_Release pointer drifted")
        compare_package(package)
        verify_independent_acceptance(
            package, root, manifest, checker_boundary="prepublish"
        )
        require(
            CURRENT_PATH.read_bytes() == current_bytes,
            "Current_Release changed during independent prepublication validation",
        )
        compare_package(package)
        atomic_write(CURRENT_PATH, target_payload)
    require(CURRENT_PATH.read_bytes() == target_payload, "5.5 Current_Release publication failed")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--publish-current", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    package, root, manifest = build_all(write_contract=args.write)
    if args.check:
        compare_package(package)
    else:
        write_release(package)
        if args.publish_current:
            publish_current(package, root, manifest)
    print(
        "PASS generate_math_catalog_v5_5 "
        f"mode={'check' if args.check else 'publish-current' if args.publish_current else 'write'} "
        f"root={root} catalog={manifest['counts']['catalog_records']} "
        f"theorem={manifest['counts']['cumulative_theorems']} "
        f"open={manifest['counts']['cumulative_open_claims']} "
        f"strict={manifest['counts']['effective_strict_conjecture_credits']} "
        f"frontier={manifest['quality_qualification']['accepted_additional_frontier_theorems']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
