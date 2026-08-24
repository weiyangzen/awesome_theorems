#!/usr/bin/env python3
"""Independent, fail-closed verifier for the Stage5 mathematics release 5.2.

The verifier deliberately imports none of the production extractor, curation
builder, or release generator modules.  It starts from the pinned public
OpenConjecture JSONL bytes, independently reapplies the source gates, rebuilds
the canonical eligible pool, replays the durable human-review and semantic
dedupe evidence, and derives the complete release package from those inputs.

This proves inventory integrity and release credit.  It does not turn a source
model label or a curator decision into an independent mathematical status
survey, proof, refutation, Lean formalization, or importance ranking.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable, Mapping, Sequence

try:
    import jsonschema
except ImportError:  # pragma: no cover - repository CI installs jsonschema.
    jsonschema = None


RELEASE = "5.2"
PARENT_RELEASE = "5.1"
IMMEDIATE_SUCCESSOR_RELEASE = "5.3"
REVIEW_DATE = "2026-08-10"
SOURCE_ID = "SRC-MATH-V5-OPENCONJECTURE-FA03D85"

CATALOG_ROOT = Path("Docs/catalog/v5")
CONTRACT_PATH = CATALOG_ROOT / "Stage5_Math_Expansion_Contract_v5_2.json"
SCHEMA_PATH = CATALOG_ROOT / "Math_Claim_Record_Schema_v5_2.json"
SOURCE_REGISTRY_PATH = CATALOG_ROOT / "Math_Source_Registry_v5_2.json"
STRICT_RECEIPT_PATH = CATALOG_ROOT / "V5_1_Strict_Conjecture_Receipt_v5_2.json"
CURATION_PATH = CATALOG_ROOT / "curation/OpenConjecture_Curation_v5_2.json"
CROSS_DEDUPE_PATH = CATALOG_ROOT / "curation/reviews/cross-dedupe.json"
REVIEW_PATHS = tuple(
    CATALOG_ROOT / f"curation/reviews/review-{letter}.jsonl"
    for letter in "abcd"
)
UPSTREAM_PATH = CATALOG_ROOT / "sources/openconjecture-fa03d85-public.jsonl"
POOL_PATH = CATALOG_ROOT / "sources/openconjecture-fa03d85-cc-by-real-conf090.jsonl"
PARENT_DIR = CATALOG_ROOT / "releases" / PARENT_RELEASE
RELEASE_DIR = CATALOG_ROOT / "releases" / RELEASE
IMMEDIATE_SUCCESSOR_DIR = CATALOG_ROOT / "releases" / IMMEDIATE_SUCCESSOR_RELEASE
CURRENT_PATH = CATALOG_ROOT / "Current_Release.json"

BASE_RELEASE_FILES = (
    "Claim_Catalog.json",
    "Claim_ID_Registry.json",
    "Stage5_Claim_ID_Registry.json",
    "Migration_v4_to_v5.json",
    "Theorem_List.json",
    "Open_Claim_List.json",
    "Coverage_Ledger.json",
)
STRICT_LEDGER_NAME = "Strict_Conjecture_Ledger.json"
RELEASE_FILES = BASE_RELEASE_FILES + (STRICT_LEDGER_NAME,)
MANIFEST_NAME = "Release_Manifest.json"

SUCCESSOR_MANIFEST_FIELDS = {
    "schema_version",
    "release",
    "parent_release",
    "parent_release_root_sha256",
    "release_root_sha256",
    "authoritative_inputs",
    "accepted_set_digests",
    "strict_credit_binding",
    "artifacts",
    "counts",
    "authority_sha256",
}

UPSTREAM_SHA256 = "8cf0a7ce4baff47769fe1ca0c40b11eed0767480c858c208a7beae8f5829dd14"
UPSTREAM_SIZE_BYTES = 9_695_990
UPSTREAM_ROWS = 4_415
POOL_SHA256 = "8a698e3af53ca0605a2a8ecd2e3a9944ad84157440a86f3c319effaf9792c6ce"
POOL_SIZE_BYTES = 2_490_006
POOL_ROWS = 889
BEFORE_VERSION_GATE_ROWS = 931
INTEREST_FLOOR_ROWS = 742
NEW_ROWS = 600
PARENT_CATALOG_ROWS = 2_500
PARENT_ATV_HIGH_WATERMARK = 5_984
PARENT_ATF_HIGH_WATERMARK = 5_754
LAST_ATV_ORDINAL = 6_584
LAST_ATF_ORDINAL = 6_354
GITHUB_COMMIT = "d2e3afe62098611fabd7236998acc73f64e4b3b7"
HUGGINGFACE_COMMIT = "fa03d85db95e6edad4ff751b490704fa8a0d9358"

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ARXIV_RE = re.compile(
    r"^(?P<base>[0-9]{4}\.[0-9]{4,5})v(?P<version>[1-9][0-9]*)$"
)
ATV_RE = re.compile(r"^ATV-([0-9]{8})$")
SEMANTIC_KEY_RE = re.compile(r"^openconjecture-semantic/[0-9a-f]{64}$")

REVIEW_FIELDS = {
    "id",
    "content_hash",
    "decision",
    "importance_assessment",
    "reason_codes",
    "notes",
    "semantic_key",
    "atomic_statement_summary",
}
LEDGER_REVIEW_FIELDS = {
    "atomic_statement_summary",
    "importance_assessment",
    "review_reason_codes",
    "review_notes",
    "review_fragment_sha256",
}
NONCLAIM_REASON_MARKERS = {
    "not_truth_apt",
    "not_strictly_truth_apt",
    "not_stably_truth_apt",
    "non_truth_apt_approximation",
    "pure_question",
    "pure_questions",
    "question_only",
    "question_form",
    "not_proposition",
    "not_author_asserted_conjecture",
}
STATUS_REASON_MARKERS = {
    "solved",
    "proved",
    "refuted",
    "proved_lemma_bundle",
    "outdated_overlap",
    "not_in_published_text",
    "not_presented_in_paper",
    "commented_out_source",
}
FORBIDDEN_LATEX_FIELDS = {
    "qualified_name",
    "module",
    "namespace",
    "declaration_kind",
    "formal_shape",
    "formal_proof_state",
    "formal_declaration",
    "formal_type",
    "formal_docstring",
    "formal_statement",
}


class CheckFailure(RuntimeError):
    """An authenticated input or release invariant failed closed."""


class Checker:
    """Repository-root-aware checker state exposed for focused tests."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.errors: list[str] = []
        self.notes: list[str] = []

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)

    def path(self, relative: str | Path) -> Path:
        item = Path(relative)
        if item.is_absolute() or ".." in item.parts:
            raise CheckFailure(f"unsafe repository path: {relative!r}")
        # Keep the lexical path so read-only per-file symlink mirrors can be
        # verified in tests and archival mounts.  The caller-controlled path
        # itself is still closed against absolute paths and ``..`` traversal.
        resolved = self.root / item
        try:
            resolved.relative_to(self.root)
        except ValueError as error:
            raise CheckFailure(f"path escapes repository: {relative!r}") from error
        return resolved

    def load_json(self, relative: str | Path) -> dict[str, Any]:
        path = self.path(relative)
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise CheckFailure(f"cannot load JSON object {relative}: {error}") from error
        if not isinstance(value, dict):
            raise CheckFailure(f"JSON authority must be an object: {relative}")
        return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def encoded_document(value: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as error:
        raise CheckFailure(f"cannot hash {path}: {error}") from error
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    excluded = set(fields)
    return sha256_bytes(
        canonical_json_bytes({key: item for key, item in value.items() if key not in excluded})
    )


def seal(value: Mapping[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result.pop("authority_sha256", None)
    result["authority_sha256"] = hash_without(result, "authority_sha256")
    return result


def seal_field(value: Mapping[str, Any], field: str, *also_omit: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    result[field] = hash_without(result, field, *also_omit)
    return result


def verify_seal(value: Mapping[str, Any], label: str) -> str:
    observed = value.get("authority_sha256")
    require(
        isinstance(observed, str) and SHA256_RE.fullmatch(observed) is not None,
        f"{label} has no valid authority_sha256",
    )
    require(observed == hash_without(value, "authority_sha256"), f"{label} seal drifted")
    return observed


def set_digest(values: Iterable[str]) -> str:
    return sha256_bytes(canonical_json_bytes(sorted(values)))


def ordinal(identifier: str, pattern: re.Pattern[str] = ATV_RE) -> int:
    match = pattern.fullmatch(identifier)
    if match is None:
        raise CheckFailure(f"invalid identifier: {identifier!r}")
    return int(match.group(1))


def relative_path(path: Path) -> str:
    return path.as_posix()


def authority_binding(checker: Checker, path: Path, value: Mapping[str, Any]) -> dict[str, Any]:
    absolute = checker.path(path)
    return {
        "path": relative_path(path),
        "file_sha256": sha256_file(absolute),
        "size_bytes": absolute.stat().st_size,
        "authority_sha256": value["authority_sha256"],
    }


def primary_row_count(document: Mapping[str, Any]) -> int:
    candidates = document.get("candidate_dispositions")
    coverage = document.get("msc_coverage")
    if isinstance(candidates, list) and isinstance(coverage, list):
        return len(candidates) + len(coverage)
    strict = document.get("strict_credits")
    corrections = document.get("credit_corrections")
    if isinstance(strict, list) and isinstance(corrections, list):
        return len(strict) + len(corrections)
    for key in ("records", "variants", "mappings", "migrations", "entries", "rows"):
        rows = document.get(key)
        if isinstance(rows, list):
            return len(rows)
    return 0


def release_root(inventory: Sequence[Mapping[str, Any]]) -> str:
    payload = [
        {"path": row["path"], "sha256": row["sha256"], "size_bytes": row["size_bytes"]}
        for row in sorted(inventory, key=lambda row: str(row["path"]))
    ]
    return sha256_bytes(canonical_json_bytes(payload))


def parse_jsonl(
    checker: Checker,
    relative: Path,
    *,
    expected_sha256: str,
    expected_size: int,
    expected_rows: int,
    canonical_lines: bool,
) -> tuple[list[dict[str, Any]], bytes]:
    path = checker.path(relative)
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise CheckFailure(f"cannot read JSONL asset {relative}: {error}") from error
    require(len(payload) == expected_size, f"{relative} byte size drifted")
    require(sha256_bytes(payload) == expected_sha256, f"{relative} SHA-256 drifted")
    require(payload.endswith(b"\n"), f"{relative} lacks its final LF")
    raw_lines = payload[:-1].split(b"\n")
    require(len(raw_lines) == expected_rows, f"{relative} row count drifted")
    require(all(raw_lines), f"{relative} contains a blank JSONL row")
    result: list[dict[str, Any]] = []
    for line_number, raw in enumerate(raw_lines, start=1):
        try:
            row = json.loads(raw.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise CheckFailure(f"{relative}:{line_number}: invalid JSON: {error}") from error
        require(isinstance(row, dict), f"{relative}:{line_number}: row is not an object")
        if canonical_lines:
            require(raw == canonical_json_bytes(row), f"{relative}:{line_number}: noncanonical JSON")
        result.append(row)
    return result, payload


def source_gate(row: Mapping[str, Any], include_version: bool = True) -> bool:
    number = row.get("latest_label_confidence")
    admitted = bool(
        row.get("latest_label") == "real_open_conjecture"
        and row.get("latest_label_model") == "gpt-5-mini"
        and row.get("latest_assessment_version") == "gpt5mini-v5-open-exact-v1"
        and isinstance(number, (int, float))
        and not isinstance(number, bool)
        and float(number) >= 0.9
        and isinstance(row.get("body_tex"), str)
        and bool(str(row["body_tex"]).strip())
        and row.get("license_family") == "cc_by"
        and row.get("license_url") == "http://creativecommons.org/licenses/by/4.0/"
        and row.get("normalized_license_url") == "https://creativecommons.org/licenses/by/4.0/"
        and row.get("publication_decision") == "publish_text"
        and row.get("publication_text_allowed") is True
        and row.get("publication_text_reason") == "creativecommons_license_treated_as_publishable"
        and row.get("publication_policy_version") == "hf-publication-v2"
        and row.get("text_withheld") is False
    )
    if not admitted or not include_version:
        return admitted
    arxiv_id = row.get("arxiv_id")
    return bool(
        isinstance(arxiv_id, str)
        and ARXIV_RE.fullmatch(arxiv_id)
        and isinstance(row.get("source_url"), str)
        and str(row["source_url"]).endswith(arxiv_id)
    )


def version_key(row: Mapping[str, Any]) -> tuple[str, int, str, int]:
    arxiv_id = str(row.get("arxiv_id", ""))
    match = ARXIV_RE.fullmatch(arxiv_id)
    require(match is not None, f"unversioned arXiv ID reached winner resolution: {arxiv_id!r}")
    record_id = row.get("id")
    require(isinstance(record_id, int) and not isinstance(record_id, bool), "invalid source id")
    return (match.group("base"), int(match.group("version")), str(row.get("updated_at", "")), record_id)


def verify_authorities(checker: Checker) -> tuple[dict[str, Any], ...]:
    contract = checker.load_json(CONTRACT_PATH)
    schema = checker.load_json(SCHEMA_PATH)
    registry = checker.load_json(SOURCE_REGISTRY_PATH)
    receipt = checker.load_json(STRICT_RECEIPT_PATH)
    curation = checker.load_json(CURATION_PATH)
    for label, value in (
        (str(CONTRACT_PATH), contract),
        (str(SCHEMA_PATH), schema),
        (str(SOURCE_REGISTRY_PATH), registry),
        (str(STRICT_RECEIPT_PATH), receipt),
        (str(CURATION_PATH), curation),
    ):
        verify_seal(value, label)
    require(contract.get("release") == RELEASE, "5.2 contract release drifted")
    bindings = contract.get("versioned_authorities")
    require(isinstance(bindings, dict), "contract versioned_authorities is malformed")
    for key, path, value in (
        ("record_schema", SCHEMA_PATH, schema),
        ("source_registry", SOURCE_REGISTRY_PATH, registry),
        ("parent_strict_receipt", STRICT_RECEIPT_PATH, receipt),
    ):
        binding = bindings.get(key)
        require(isinstance(binding, dict), f"missing authority binding: {key}")
        absolute = checker.path(path)
        require(binding.get("path") == relative_path(path), f"{key} path binding drifted")
        require(binding.get("file_sha256") == sha256_file(absolute), f"{key} file binding drifted")
        require(binding.get("authority_sha256") == value["authority_sha256"], f"{key} authority binding drifted")
    required_curation_top = set(contract["curation_ledger_contract"]["required_top_level_fields"])
    require(set(curation) == required_curation_top, "curation top-level field closure drifted")
    curation_binding = contract["curation_ledger_contract"]
    require(curation_binding.get("path") == relative_path(CURATION_PATH), "curation path drifted")
    if curation_binding.get("authority_sha256") is not None:
        require(curation_binding["authority_sha256"] == curation["authority_sha256"], "contract curation authority binding drifted")
    if curation_binding.get("file_sha256") is not None:
        require(curation_binding["file_sha256"] == sha256_file(checker.path(CURATION_PATH)), "contract curation file binding drifted")
    require(schema.get("schema_version", schema.get("$id")) is not None, "record schema identity missing")
    require(registry.get("schema_version") == "awesome-theorems/stage5-math-source-registry/5.2", "source registry schema drifted")
    sources = registry.get("sources")
    require(isinstance(sources, list) and len(sources) == 1, "5.2 registry must add exactly one source")
    require(sources[0].get("source_id") == SOURCE_ID, "OpenConjecture source ID drifted")
    require(receipt.get("parent_release", {}).get("release") == PARENT_RELEASE, "strict receipt parent drifted")
    require(curation.get("source_id") == SOURCE_ID, "curation source ID drifted")
    return contract, schema, registry, receipt, curation


def rebuild_source_pool(
    checker: Checker, contract: Mapping[str, Any], registry: Mapping[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, tuple[int, int]], dict[str, str]]:
    assets = contract["source_assets"]
    upstream_spec = assets["upstream_public_jsonl"]
    pool_spec = assets["eligible_pool_jsonl"]
    require(
        upstream_spec == {
            "path": relative_path(UPSTREAM_PATH),
            "sha256": UPSTREAM_SHA256,
            "size_bytes": UPSTREAM_SIZE_BYTES,
            "record_count": UPSTREAM_ROWS,
        },
        "contract upstream source pin drifted",
    )
    require(pool_spec.get("path") == relative_path(POOL_PATH), "contract pool path drifted")
    require(pool_spec.get("sha256") == POOL_SHA256, "contract pool SHA drifted")
    require(pool_spec.get("size_bytes") == POOL_SIZE_BYTES, "contract pool size drifted")
    require(pool_spec.get("record_count") == POOL_ROWS, "contract pool count drifted")
    require(assets["pins"].get("github_commit") == GITHUB_COMMIT, "GitHub commit pin drifted")
    require(assets["pins"].get("huggingface_commit") == HUGGINGFACE_COMMIT, "Hugging Face commit pin drifted")

    source = registry["sources"][0]
    registry_assets = source["assets"]
    for key, expected_sha, expected_size, expected_count in (
        ("upstream_public_jsonl", UPSTREAM_SHA256, UPSTREAM_SIZE_BYTES, UPSTREAM_ROWS),
        ("eligible_pool_jsonl", POOL_SHA256, POOL_SIZE_BYTES, POOL_ROWS),
    ):
        spec = registry_assets[key]
        require(spec.get("sha256") == expected_sha, f"source-registry {key} SHA drifted")
        require(spec.get("size_bytes") == expected_size, f"source-registry {key} size drifted")
        require(spec.get("record_count") == expected_count, f"source-registry {key} count drifted")
    require(source["pin"].get("github_commit") == GITHUB_COMMIT, "registry GitHub commit drifted")
    require(source["pin"].get("huggingface_commit") == HUGGINGFACE_COMMIT, "registry Hugging Face commit drifted")

    upstream, _ = parse_jsonl(
        checker,
        UPSTREAM_PATH,
        expected_sha256=UPSTREAM_SHA256,
        expected_size=UPSTREAM_SIZE_BYTES,
        expected_rows=UPSTREAM_ROWS,
        canonical_lines=False,
    )
    pool, _ = parse_jsonl(
        checker,
        POOL_PATH,
        expected_sha256=POOL_SHA256,
        expected_size=POOL_SIZE_BYTES,
        expected_rows=POOL_ROWS,
        canonical_lines=True,
    )
    upstream_by_id: dict[int, tuple[int, dict[str, Any]]] = {}
    for line_number, row in enumerate(upstream, start=1):
        record_id = row.get("id")
        require(isinstance(record_id, int) and not isinstance(record_id, bool) and record_id > 0, f"upstream line {line_number}: invalid id")
        require(record_id not in upstream_by_id, f"duplicate upstream source id {record_id}")
        upstream_by_id[record_id] = (line_number, row)

    before_version = [row for row in upstream if source_gate(row, include_version=False)]
    require(len(before_version) == BEFORE_VERSION_GATE_ROWS, "source gate did not rebuild 931 pre-locator candidates")
    winners: dict[str, dict[str, Any]] = {}
    for row in before_version:
        if not source_gate(row, include_version=True):
            continue
        content_hash = row.get("content_hash")
        require(isinstance(content_hash, str) and SHA256_RE.fullmatch(content_hash) is not None, "eligible source has invalid content_hash")
        previous = winners.get(content_hash)
        if previous is None or version_key(previous) < version_key(row):
            winners[content_hash] = row
    rebuilt = sorted(winners.values(), key=lambda row: str(row["content_hash"]))
    require(len(rebuilt) == POOL_ROWS, "source gates/dedupe did not rebuild 889 rows")
    require(rebuilt == pool, "eligible pool is not the exact independent upstream rebuild")
    content_hashes = [str(row["content_hash"]) for row in pool]
    require(content_hashes == sorted(content_hashes), "eligible pool is not content-hash sorted")
    require(len(set(content_hashes)) == POOL_ROWS, "eligible pool repeats content hashes")
    require(set_digest(content_hashes) == pool_spec["content_hash_set_sha256"], "eligible content-hash set digest drifted")
    require(sum(float(row["latest_interestingness_score"]) >= 0.5 for row in pool) == INTEREST_FLOOR_ROWS, "eligible score-floor count drifted")

    locators: dict[str, tuple[int, int]] = {}
    source_hashes: dict[str, str] = {}
    for pool_line, row in enumerate(pool, start=1):
        record_id = int(row["id"])
        require(record_id in upstream_by_id, f"pool source id {record_id} is absent upstream")
        upstream_line, upstream_row = upstream_by_id[record_id]
        require(row == upstream_row, f"pool line {pool_line} differs from upstream line {upstream_line}")
        content_hash = str(row["content_hash"])
        locators[content_hash] = (upstream_line, pool_line)
        source_hashes[content_hash] = sha256_bytes(canonical_json_bytes(row))
    return pool, locators, source_hashes


def paper_object(source: Mapping[str, Any]) -> dict[str, Any]:
    return seal_field(
        {
            "arxiv_id": source["arxiv_id"],
            "title": source["title"],
            "authors": list(source["authors"]),
            "published_at": source["published_at"],
            "updated_at": source["updated_at"],
            "categories": list(source["categories"]),
            "primary_category": source["primary_category"],
            "doi": source["doi"],
            "journal_ref": source["journal_ref"],
            "comments": source["comments"],
            "abs_url": source["abs_url"],
            "pdf_url": source["pdf_url"],
            "source_url": source["source_url"],
        },
        "metadata_payload_sha256",
    )


def model_label_object(source: Mapping[str, Any]) -> dict[str, Any]:
    return seal_field(
        {
            "label_model": source["latest_label_model"],
            "label": source["latest_label"],
            "label_confidence": source["latest_label_confidence"],
            "assessment_version": source["latest_assessment_version"],
            "label_rationale": source["latest_label_rationale"],
            "evidence_snippet": source["latest_evidence_snippet"],
            "labeled_at": source["latest_labeled_at"],
            "interestingness_score": source["latest_interestingness_score"],
            "interestingness_confidence": source["latest_interestingness_confidence"],
            "interestingness_rationale": source["latest_interestingness_rationale"],
            "viability_score": source["latest_viability_score"],
            "viability_confidence": source["latest_viability_confidence"],
            "viability_rationale": source["latest_viability_rationale"],
            "source_model_assertion_not_independent_status_review": True,
            "source_model_assertion_not_proof": True,
        },
        "model_label_payload_sha256",
    )


def rights_object(source: Mapping[str, Any]) -> dict[str, Any]:
    attribution = {
        "attribution_authors": list(source["authors"]),
        "attribution_title": source["title"],
        "attribution_arxiv_id": source["arxiv_id"],
    }
    return seal_field(
        {
            "spdx_expression": "CC-BY-4.0",
            "license_family": source["license_family"],
            "license_url": source["license_url"],
            "normalized_license_url": source["normalized_license_url"],
            "publication_decision": source["publication_decision"],
            "publication_text_allowed": source["publication_text_allowed"],
            "publication_text_reason": source["publication_text_reason"],
            "publication_policy_version": source["publication_policy_version"],
            "text_withheld": source["text_withheld"],
            **attribution,
            "attribution_payload_sha256": sha256_bytes(canonical_json_bytes(attribution)),
            "redistribution_mode": "verbatim_cc_by_4_0_with_per_record_attribution",
            "catalog_relicenses_source": False,
            "source_refs": [SOURCE_ID],
        },
        "rights_payload_sha256",
    )


def final_semantic_key(review: Mapping[str, Any]) -> str:
    payload = {
        "review_semantic_key": review["semantic_key"],
        "atomic_statement_summary": review["atomic_statement_summary"],
    }
    return "openconjecture-semantic/" + sha256_bytes(canonical_json_bytes(payload))


def semantic_key_payload_sha256(review: Mapping[str, Any]) -> str:
    return sha256_bytes(
        canonical_json_bytes(
            {
                "semantic_key": final_semantic_key(review),
                "atomic_statement_summary": review["atomic_statement_summary"],
            }
        )
    )


def load_reviews(
    checker: Checker, pool: Sequence[Mapping[str, Any]]
) -> tuple[dict[int, dict[str, Any]], dict[int, str], dict[int, str]]:
    pool_by_id = {int(row["id"]): row for row in pool}
    reviews: dict[int, dict[str, Any]] = {}
    fragment_hashes: dict[int, str] = {}
    shards: dict[int, str] = {}
    for path in REVIEW_PATHS:
        absolute = checker.path(path)
        try:
            payload = absolute.read_bytes()
        except OSError as error:
            raise CheckFailure(f"cannot read review shard {path}: {error}") from error
        require(payload.endswith(b"\n"), f"review shard {path} lacks final LF")
        fragment_hash = sha256_bytes(payload)
        shard = path.stem.removeprefix("review-")
        for line_number, raw in enumerate(payload[:-1].split(b"\n"), start=1):
            require(bool(raw), f"{path}:{line_number}: blank review row")
            try:
                value = json.loads(raw.decode("utf-8"))
            except (UnicodeError, json.JSONDecodeError) as error:
                raise CheckFailure(f"{path}:{line_number}: invalid JSON: {error}") from error
            require(isinstance(value, dict), f"{path}:{line_number}: review is not an object")
            require(set(value) == REVIEW_FIELDS, f"{path}:{line_number}: review field closure drifted")
            row = dict(value)
            record_id = row.get("id")
            require(isinstance(record_id, int) and not isinstance(record_id, bool) and record_id > 0, f"{path}:{line_number}: invalid source id")
            require(record_id not in reviews, f"review shards repeat source id {record_id}")
            source = pool_by_id.get(record_id)
            require(source is not None, f"review source id {record_id} is outside eligible pool")
            require(row.get("content_hash") == source["content_hash"], f"review/source content hash mismatch for {record_id}")
            require(row.get("decision") in {"accept", "reject", "needs_split"}, f"invalid review decision for {record_id}")
            require(row.get("importance_assessment") in {"high", "medium", "low"}, f"invalid review importance for {record_id}")
            codes = row.get("reason_codes")
            require(
                isinstance(codes, list)
                and bool(codes)
                and all(isinstance(code, str) and bool(code.strip()) for code in codes)
                and len(codes) == len(set(codes)),
                f"invalid review reason codes for {record_id}",
            )
            require(isinstance(row.get("notes"), str) and bool(str(row["notes"]).strip()), f"invalid review notes for {record_id}")
            if row.get("semantic_key") is None or row.get("atomic_statement_summary") is None:
                require(
                    row["decision"] == "reject"
                    and row.get("semantic_key") is None
                    and row.get("atomic_statement_summary") is None,
                    f"review {record_id} partially omits its semantic payload",
                )
                row["semantic_key"] = f"nonclaim/{source['content_hash']}"
                row["atomic_statement_summary"] = row["notes"]
            else:
                require(isinstance(row["semantic_key"], str) and bool(row["semantic_key"].strip()), f"invalid review semantic key for {record_id}")
                require(isinstance(row["atomic_statement_summary"], str) and bool(row["atomic_statement_summary"].strip()), f"invalid atomic summary for {record_id}")
            reviews[record_id] = row
            fragment_hashes[record_id] = fragment_hash
            shards[record_id] = shard
    require(len(reviews) == POOL_ROWS, "review shards do not contain exactly 889 rows")
    require(set(reviews) == set(pool_by_id), "review shards are not an exact eligible-pool partition")
    return reviews, fragment_hashes, shards


def base_review_eligible(review: Mapping[str, Any], source: Mapping[str, Any]) -> bool:
    return bool(
        review.get("decision") == "accept"
        and review.get("importance_assessment") in {"high", "medium"}
        and float(source["latest_interestingness_score"]) >= 0.5
    )


def load_cross_dedupe(
    checker: Checker,
    reviews: Mapping[int, Mapping[str, Any]],
    pool: Sequence[Mapping[str, Any]],
    shards: Mapping[int, str],
    parent_rows: Sequence[Mapping[str, Any]],
) -> tuple[dict[int, tuple[str | None, str | None]], set[int]]:
    cross = checker.load_json(CROSS_DEDUPE_PATH)
    require(cross.get("schema_version") == "openconjecture-cross-dedupe-v1", "cross-dedupe schema drifted")
    pool_by_id = {int(row["id"]): row for row in pool}
    base_ids = {
        record_id
        for record_id, review in reviews.items()
        if base_review_eligible(review, pool_by_id[record_id])
    }
    require(cross.get("eligible_count") == len(base_ids) == 671, "cross-dedupe eligible count drifted")
    expected_shards = dict(sorted(Counter(shards[item] for item in base_ids).items()))
    require(cross.get("eligible_counts_by_shard") == expected_shards, "cross-dedupe shard counts drifted")
    missing_categories = {
        item for item in base_ids if not str(pool_by_id[item].get("primary_category", ""))
    }
    raw_missing_categories = cross.get("missing_category_ids")
    require(
        isinstance(raw_missing_categories, list)
        and all(isinstance(item, int) and not isinstance(item, bool) for item in raw_missing_categories)
        and len(raw_missing_categories) == len(set(raw_missing_categories))
        and set(raw_missing_categories) == missing_categories,
        "cross-dedupe missing-category inventory drifted",
    )
    raw_missing_context = cross.get("missing_context_ids")
    require(
        isinstance(raw_missing_context, list)
        and all(isinstance(item, int) and not isinstance(item, bool) for item in raw_missing_context)
        and len(raw_missing_context) == len(set(raw_missing_context)),
        "cross-dedupe missing-context inventory is invalid",
    )
    missing_context = set(raw_missing_context)
    require(missing_context <= base_ids and len(missing_context) == 49, "cross-dedupe missing-context set drifted")

    parent_by_variant: dict[str, Mapping[str, Any]] = {}
    for row in parent_rows:
        variant_id = row.get("variant_id")
        require(isinstance(variant_id, str) and ATV_RE.fullmatch(variant_id) is not None, "parent catalog has invalid ATV ID")
        require(variant_id not in parent_by_variant, f"parent catalog repeats {variant_id}")
        parent_by_variant[variant_id] = row
    require(max(ordinal(item) for item in parent_by_variant) == PARENT_ATV_HIGH_WATERMARK, "parent ATV high-watermark drifted")

    groups = cross.get("groups")
    require(isinstance(groups, list), "cross-dedupe groups is not an array")
    links: dict[int, tuple[str | None, str | None]] = {}
    canonical_ids: set[int] = set()
    parent_ids: set[str] = set()
    internal_removed: set[int] = set()
    parent_removed: set[int] = set()
    for index, group in enumerate(groups):
        require(isinstance(group, dict), f"cross-dedupe group {index} is not an object")
        candidate_mode = "canonical_candidate_id" in group
        parent_mode = "parent_variant_id" in group
        require(candidate_mode != parent_mode, f"cross-dedupe group {index} has ambiguous canonical target")
        duplicates = group.get("duplicate_candidate_ids")
        require(
            isinstance(duplicates, list)
            and bool(duplicates)
            and all(isinstance(item, int) and not isinstance(item, bool) for item in duplicates)
            and len(duplicates) == len(set(duplicates)),
            f"cross-dedupe group {index} has invalid duplicates",
        )
        require(isinstance(group.get("rationale"), str) and bool(group["rationale"].strip()), f"cross-dedupe group {index} lacks rationale")
        confidence = group.get("confidence")
        require(
            (isinstance(confidence, str) and bool(confidence.strip()))
            or (isinstance(confidence, (int, float)) and not isinstance(confidence, bool) and 0 <= float(confidence) <= 1),
            f"cross-dedupe group {index} has invalid confidence",
        )
        canonical_semantic: str | None = None
        parent_variant: str | None = None
        if candidate_mode:
            canonical = group.get("canonical_candidate_id")
            require(isinstance(canonical, int) and not isinstance(canonical, bool) and canonical in base_ids, f"cross-dedupe group {index} canonical is ineligible")
            require(canonical not in duplicates and canonical not in canonical_ids, f"cross-dedupe group {index} repeats its canonical")
            canonical_ids.add(canonical)
            canonical_semantic = final_semantic_key(reviews[canonical])
            internal_removed.update(duplicates)
        else:
            parent_variant = group.get("parent_variant_id")
            require(isinstance(parent_variant, str) and parent_variant in parent_by_variant, f"cross-dedupe group {index} cites an unknown parent variant")
            require(parent_variant not in parent_ids, f"parent duplicate target {parent_variant} occurs twice")
            parent_ids.add(parent_variant)
            parent_removed.update(duplicates)
        for duplicate in duplicates:
            require(duplicate in base_ids, f"cross-dedupe candidate {duplicate} was not review-eligible")
            require(duplicate not in links, f"cross-dedupe candidate {duplicate} occurs in multiple groups")
            links[duplicate] = (canonical_semantic, parent_variant)
    require(not (canonical_ids & set(links)), "a cross-dedupe canonical is itself marked duplicate")
    require(not (internal_removed & parent_removed), "internal and parent duplicate sets overlap")
    expected_counts = {
        "internal_duplicate_group_count": len(canonical_ids),
        "internal_duplicate_rows_removed": len(internal_removed),
        "parent_duplicate_group_count": len(parent_ids),
        "parent_duplicate_rows_removed": len(parent_removed),
        "internal_unique_count": len(base_ids - internal_removed),
        "viable_unique_count": len(base_ids - set(links)),
    }
    for key, expected in expected_counts.items():
        require(cross.get(key) == expected, f"cross-dedupe {key} drifted")
    require(len(parent_ids) == 7 and len(parent_removed) == 7, "cross-parent dedupe is not exactly seven audited removals")
    return links, missing_context


def selection_key(review: Mapping[str, Any], source: Mapping[str, Any]) -> tuple[Any, ...]:
    return (
        0 if review["importance_assessment"] == "high" else 1,
        -float(source["latest_interestingness_score"]),
        -float(source["latest_interestingness_confidence"]),
        -float(source["latest_label_confidence"]),
        str(source["content_hash"]),
    )


def select_review_ids(
    reviews: Mapping[int, Mapping[str, Any]],
    pool_by_id: Mapping[int, Mapping[str, Any]],
    duplicate_ids: set[int],
    missing_context: set[int],
) -> tuple[list[int], set[int]]:
    eligible = [
        record_id
        for record_id, review in reviews.items()
        if base_review_eligible(review, pool_by_id[record_id])
        and record_id not in duplicate_ids
        and record_id not in missing_context
    ]
    semantic_keys = [final_semantic_key(reviews[item]) for item in eligible]
    require(len(semantic_keys) == len(set(semantic_keys)), "viable reviewed candidates repeat a semantic key")
    require(len(eligible) >= NEW_ROWS, "fewer than 600 candidates survive semantic/status gates")
    by_category: dict[str, list[int]] = defaultdict(list)
    for record_id in eligible:
        category = str(pool_by_id[record_id].get("primary_category", ""))
        if category:
            by_category[category].append(record_id)
    selected: list[int] = []
    selected_set: set[int] = set()
    seeded: set[int] = set()
    for category in sorted(by_category):
        ranked = sorted(by_category[category], key=lambda item: selection_key(reviews[item], pool_by_id[item]))
        for record_id in ranked[:3]:
            if record_id not in selected_set:
                selected.append(record_id)
                selected_set.add(record_id)
                seeded.add(record_id)
    ranked_all = sorted(eligible, key=lambda item: selection_key(reviews[item], pool_by_id[item]))
    for record_id in ranked_all:
        if len(selected) == NEW_ROWS:
            break
        if record_id not in selected_set:
            selected.append(record_id)
            selected_set.add(record_id)
    require(len(selected) == len(selected_set) == NEW_ROWS, "review replay did not select exactly 600 candidates")
    return selected, seeded


def review_rejection(review: Mapping[str, Any]) -> tuple[str, str]:
    reasons = set(review["reason_codes"])
    if "semantic_duplicate" in reasons:
        return "rejected_semantic_duplicate", "review_identified_semantic_duplicate"
    if reasons & STATUS_REASON_MARKERS:
        return "rejected_status_boundary", "review_failed_open_status_boundary"
    if reasons & NONCLAIM_REASON_MARKERS:
        return "rejected_nonclaim", "review_failed_truth_apt_claim_boundary"
    return "rejected_incoherent_source_block", "review_found_source_block_not_release_coherent"


def expected_disposition(
    record_id: int,
    review: Mapping[str, Any],
    source: Mapping[str, Any],
    selected_ranks: Mapping[int, int],
    seeded: set[int],
    duplicate_links: Mapping[int, tuple[str | None, str | None]],
    missing_context: set[int],
) -> tuple[str, str]:
    if record_id in missing_context:
        return "rejected_incoherent_source_block", "cross_audit_missing_context_for_whole_exact_source_block"
    if record_id in duplicate_links:
        if duplicate_links[record_id][1] is not None:
            return "rejected_semantic_duplicate", "semantic_duplicate_of_parent_variant"
        return "rejected_semantic_duplicate", "semantic_duplicate_of_curated_candidate"
    if review["decision"] == "needs_split":
        return "rejected_incoherent_source_block", "whole_exact_source_block_requires_split"
    if review["decision"] == "reject":
        return review_rejection(review)
    if float(source["latest_interestingness_score"]) < 0.5:
        return "rejected_below_interest_floor", "source_interestingness_below_0_50"
    if review["importance_assessment"] not in {"high", "medium"}:
        return "eligible_not_selected", "curator_importance_below_medium"
    if record_id in selected_ranks:
        if record_id in seeded:
            return "accepted_new_strict_open_claim", "selected_category_seed"
        return "accepted_new_strict_open_claim", "selected_global_rank_fill"
    return "eligible_not_selected", "ranked_beyond_exact_600"


def verify_curation(
    checker: Checker,
    contract: Mapping[str, Any],
    curation: Mapping[str, Any],
    pool: Sequence[dict[str, Any]],
    source_hashes: Mapping[str, str],
    parent_rows: Sequence[Mapping[str, Any]],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    reviews, fragment_hashes, shards = load_reviews(checker, pool)
    links, missing_context = load_cross_dedupe(checker, reviews, pool, shards, parent_rows)
    pool_by_id = {int(row["id"]): row for row in pool}
    selected, seeded = select_review_ids(reviews, pool_by_id, set(links), missing_context)
    selected_ranks = {record_id: rank for rank, record_id in enumerate(selected, start=1)}
    expected_rows: list[dict[str, Any]] = []
    accepted: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for source in pool:
        record_id = int(source["id"])
        review = reviews[record_id]
        disposition, reason_code = expected_disposition(
            record_id, review, source, selected_ranks, seeded, links, missing_context
        )
        is_accepted = disposition == "accepted_new_strict_open_claim"
        rank = selected_ranks.get(record_id) if is_accepted else None
        item_ordinal = PARENT_ATV_HIGH_WATERMARK + rank if rank is not None else None
        duplicate_semantic, duplicate_variant = links.get(record_id, (None, None))
        content_hash = str(source["content_hash"])
        row: dict[str, Any] = {
            "candidate_key": f"openconjecture:{content_hash}",
            "source_record_id": record_id,
            "source_record_sha256": source_hashes[content_hash],
            "content_hash": content_hash,
            "body_tex_sha256": sha256_bytes(str(source["body_tex"]).encode("utf-8")),
            "arxiv_id": source["arxiv_id"],
            "interestingness_score": source["latest_interestingness_score"],
            "semantic_key": final_semantic_key(review),
            "semantic_key_payload_sha256": semantic_key_payload_sha256(review),
            "disposition": disposition,
            "reason_code": reason_code,
            "selected_rank": rank,
            "target_variant_id": f"ATV-{item_ordinal:08d}" if item_ordinal is not None else None,
            "target_s5_id": f"S5-CLM-{item_ordinal:08d}" if item_ordinal is not None else None,
            "duplicate_of_semantic_key": duplicate_semantic,
            "duplicate_of_variant_id": duplicate_variant,
            "grants_catalog_entry": is_accepted,
            "grants_strict_conjecture_credit": is_accepted,
            "rights_payload_sha256": rights_object(source)["rights_payload_sha256"],
            "model_label_payload_sha256": model_label_object(source)["model_label_payload_sha256"],
            "atomic_statement_summary": review["atomic_statement_summary"],
            "importance_assessment": review["importance_assessment"],
            "review_reason_codes": list(review["reason_codes"]),
            "review_notes": review["notes"],
            "review_fragment_sha256": fragment_hashes[record_id],
        }
        row["row_sha256"] = hash_without(row, "row_sha256")
        expected_rows.append(row)
        if is_accepted:
            accepted.append((row, source))

    require(curation.get("schema_version") == "awesome-theorems/openconjecture-curation/5.2", "curation schema version drifted")
    require(curation.get("source_registry_authority_sha256") == contract["versioned_authorities"]["source_registry"]["authority_sha256"], "curation source-registry binding drifted")
    require(curation.get("eligible_pool_sha256") == POOL_SHA256, "curation pool binding drifted")
    actual_rows = curation.get("candidate_dispositions")
    require(isinstance(actual_rows, list) and actual_rows == expected_rows, "curation ledger does not exactly replay from reviews and cross-dedupe")
    required_fields = set(contract["curation_ledger_contract"]["required_candidate_fields"]) | LEDGER_REVIEW_FIELDS
    require(all(set(row) == required_fields for row in expected_rows), "curation row field closure drifted")
    accepted.sort(key=lambda pair: int(pair[0]["selected_rank"]))
    require(len(accepted) == NEW_ROWS, "curation does not accept exactly 600 rows")
    require([row["selected_rank"] for row, _ in accepted] == list(range(1, NEW_ROWS + 1)), "curation ranks are not 1..600")
    semantics = [str(row["semantic_key"]) for row, _ in accepted]
    require(all(SEMANTIC_KEY_RE.fullmatch(value) for value in semantics), "accepted semantic key format drifted")
    require(len(set(semantics)) == NEW_ROWS, "accepted curation rows repeat semantic keys")
    require(all(row["duplicate_of_variant_id"] is None and row["duplicate_of_semantic_key"] is None for row, _ in accepted), "an accepted row retains a duplicate link")
    dispositions = Counter(str(row["disposition"]) for row in expected_rows)
    expected_counts = {
        "candidates": POOL_ROWS,
        "accepted": NEW_ROWS,
        "nonaccepted": POOL_ROWS - NEW_ROWS,
        "by_disposition": dict(sorted(dispositions.items())),
        "by_review_decision": dict(sorted(Counter(str(row["decision"]) for row in reviews.values()).items())),
        "category_seeded": len(seeded),
        "global_rank_fill": NEW_ROWS - len(seeded),
        "cross_dedupe_groups": len(checker.load_json(CROSS_DEDUPE_PATH)["groups"]),
        "missing_context_rejections": len(missing_context),
        "review_fragments": len(REVIEW_PATHS),
    }
    require(curation.get("counts") == expected_counts, "curation counts do not independently recompute")
    expected_digests = {
        "eligible_content_hash_set_sha256": set_digest(str(row["content_hash"]) for row in pool),
        "accepted_content_hash_set_sha256": set_digest(str(row["content_hash"]) for row, _ in accepted),
        "accepted_semantic_key_set_sha256": set_digest(str(row["semantic_key"]) for row, _ in accepted),
        "accepted_s5_id_set_sha256": set_digest(str(row["target_s5_id"]) for row, _ in accepted),
    }
    require(curation.get("set_digests") == expected_digests, "curation set digests drifted")
    return accepted


def load_release_documents(
    checker: Checker, directory: Path, names: Sequence[str]
) -> tuple[dict[str, dict[str, Any]], dict[str, bytes]]:
    absolute = checker.path(directory)
    require(absolute.is_dir(), f"release directory is missing: {directory}")
    actual_files = {item.name for item in absolute.iterdir() if item.is_file()}
    non_files = [item.name for item in absolute.iterdir() if not item.is_file()]
    expected = set(names) | {MANIFEST_NAME}
    require(actual_files == expected and not non_files, f"{directory} is not the exact immutable artifact set")
    documents: dict[str, dict[str, Any]] = {}
    payloads: dict[str, bytes] = {}
    for name in sorted(expected):
        path = absolute / name
        try:
            raw = path.read_bytes()
            value = json.loads(raw.decode("utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise CheckFailure(f"cannot load release artifact {path}: {error}") from error
        require(isinstance(value, dict), f"release artifact {path} is not an object")
        require(raw == encoded_document(value), f"release artifact {path} is not canonical JSON plus LF")
        verify_seal(value, str(path))
        documents[name] = value
        payloads[name] = raw
    return documents, payloads


def verify_inventory(
    manifest: Mapping[str, Any],
    payloads: Mapping[str, bytes],
    documents: Mapping[str, Mapping[str, Any]],
    expected_names: Sequence[str],
    label: str,
) -> str:
    inventory = manifest.get("artifacts")
    require(isinstance(inventory, list), f"{label} manifest inventory is not an array")
    require([row.get("path") for row in inventory] == sorted(expected_names), f"{label} manifest artifact order/set drifted")
    rebuilt: list[dict[str, Any]] = []
    for entry in inventory:
        require(isinstance(entry, dict), f"{label} manifest inventory row is not an object")
        require(set(entry) == {"path", "sha256", "size_bytes", "row_count"}, f"{label} manifest inventory row closure drifted")
        name = entry["path"]
        raw = payloads[name]
        require(entry["sha256"] == sha256_bytes(raw), f"{label} artifact hash drifted: {name}")
        require(entry["size_bytes"] == len(raw), f"{label} artifact size drifted: {name}")
        require(entry["row_count"] == primary_row_count(documents[name]), f"{label} row count drifted: {name}")
        rebuilt.append(entry)
    root = release_root(rebuilt)
    require(manifest.get("release_root_sha256") == root, f"{label} release root does not recompute")
    return root


def verify_parent_release(
    checker: Checker, contract: Mapping[str, Any]
) -> tuple[dict[str, dict[str, Any]], dict[str, bytes]]:
    documents, payloads = load_release_documents(checker, PARENT_DIR, BASE_RELEASE_FILES)
    manifest = documents[MANIFEST_NAME]
    parent = contract["parent"]
    require(manifest.get("release") == PARENT_RELEASE, "parent manifest release drifted")
    root = verify_inventory(manifest, payloads, documents, BASE_RELEASE_FILES, "parent 5.1")
    require(parent.get("release") == PARENT_RELEASE, "contract parent name drifted")
    require(parent.get("manifest_path") == relative_path(PARENT_DIR / MANIFEST_NAME), "contract parent manifest path drifted")
    require(parent.get("manifest_file_sha256") == sha256_bytes(payloads[MANIFEST_NAME]), "contract parent manifest bytes drifted")
    require(parent.get("manifest_authority_sha256") == manifest["authority_sha256"], "contract parent manifest authority drifted")
    require(parent.get("release_root_sha256") == root, "contract parent release root drifted")
    catalog = documents["Claim_Catalog.json"]
    registry = documents["Claim_ID_Registry.json"]
    require(parent.get("claim_catalog_file_sha256") == sha256_bytes(payloads["Claim_Catalog.json"]), "contract parent catalog bytes drifted")
    require(parent.get("claim_catalog_authority_sha256") == catalog["authority_sha256"], "contract parent catalog authority drifted")
    require(parent.get("claim_id_registry_authority_sha256") == registry["authority_sha256"], "contract parent registry authority drifted")
    rows = catalog.get("records")
    require(isinstance(rows, list) and len(rows) == PARENT_CATALOG_ROWS, "parent catalog is not exactly 2,500 rows")
    require(registry.get("namespace_high_watermarks", {}).get("ATV") == PARENT_ATV_HIGH_WATERMARK, "parent registry ATV high-watermark drifted")
    require(registry.get("namespace_high_watermarks", {}).get("ATF") == PARENT_ATF_HIGH_WATERMARK, "parent registry ATF high-watermark drifted")
    return documents, payloads


def source_locator_object(
    source: Mapping[str, Any],
    upstream_line: int,
    pool_line: int,
    source_sha256: str,
) -> dict[str, Any]:
    return {
        "source_id": SOURCE_ID,
        "upstream_asset_path": relative_path(UPSTREAM_PATH),
        "upstream_asset_sha256": UPSTREAM_SHA256,
        "upstream_asset_size_bytes": UPSTREAM_SIZE_BYTES,
        "eligible_pool_path": relative_path(POOL_PATH),
        "eligible_pool_sha256": POOL_SHA256,
        "eligible_pool_size_bytes": POOL_SIZE_BYTES,
        "github_commit": GITHUB_COMMIT,
        "huggingface_commit": HUGGINGFACE_COMMIT,
        "upstream_line_number": upstream_line,
        "eligible_pool_line_number": pool_line,
        "source_record_id": source["id"],
        "source_record_sha256": source_sha256,
        "arxiv_id": source["arxiv_id"],
        "source_url": source["source_url"],
        "source_file": source["source_file"],
        "index_in_file": source["index_in_file"],
        "line_start": source["start_line"],
        "line_end": source["end_line"],
        "content_hash": source["content_hash"],
    }


def validate_record_schema(row: Mapping[str, Any], schema: Mapping[str, Any], label: str) -> None:
    require(jsonschema is not None, "jsonschema is required for independent schema validation")
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = sorted(validator.iter_errors(row), key=lambda error: list(error.absolute_path))
    if errors:
        first = errors[0]
        location = ".".join(str(item) for item in first.absolute_path) or "$"
        raise CheckFailure(f"{label} violates the closed 5.2 schema at {location}: {first.message}")


def expected_new_record(
    ledger_row: Mapping[str, Any],
    source: Mapping[str, Any],
    locators: Mapping[str, tuple[int, int]],
    source_hashes: Mapping[str, str],
    parent_registry_authority: str,
    parent_root: str,
    curation_authority: str,
) -> dict[str, Any]:
    content_hash = str(source["content_hash"])
    source_sha = source_hashes[content_hash]
    upstream_line, pool_line = locators[content_hash]
    rank = int(ledger_row["selected_rank"])
    atv_ordinal = PARENT_ATV_HIGH_WATERMARK + rank
    atf_ordinal = PARENT_ATF_HIGH_WATERMARK + rank
    semantic_key = str(ledger_row["semantic_key"])
    body_tex = str(source["body_tex"])
    plain_text = str(source["plain_text"])
    body_sha = sha256_bytes(body_tex.encode("utf-8"))
    plain_sha = sha256_bytes(plain_text.encode("utf-8"))
    locator = source_locator_object(source, upstream_line, pool_line, source_sha)
    source_block = {
        "language": "LaTeX",
        "block_kind": "source_conjecture_environment",
        "extraction_scope": "exact_upstream_body_tex_field",
        "body_tex": body_tex,
        "body_tex_sha256": body_sha,
        "plain_text": plain_text,
        "plain_text_sha256": plain_sha,
        "content_hash": content_hash,
        "source_record_sha256": source_sha,
    }
    paper = paper_object(source)
    model_label = model_label_object(source)
    rights = rights_object(source)
    curator = {
        "ledger_path": relative_path(CURATION_PATH),
        "ledger_authority_sha256": curation_authority,
        "ledger_row_sha256": ledger_row["row_sha256"],
        "candidate_key": ledger_row["candidate_key"],
        "selected_rank": rank,
        "disposition": "accepted_new_strict_open_claim",
        "basis": "curator_accepted_after_closed_source_semantic_nonclaim_and_rights_gates",
        "grants_release_entry": True,
        "grants_strict_conjecture_credit": True,
        "human_status_review_performed": False,
        "duplicate_of_variant_id": None,
        "reviewed_as_of": REVIEW_DATE,
    }
    curator["disposition_payload_sha256"] = hash_without(
        curator, "ledger_row_sha256", "disposition_payload_sha256"
    )
    statement = seal_field(
        {
            "language": "LaTeX",
            "representation": "verbatim_source_conjecture_block",
            "completeness": "exact_source_body_tex_plus_upstream_plain_text",
            "component_extraction_status": "not_separately_parsed",
            "body_tex": body_tex,
            "body_tex_sha256": body_sha,
            "plain_text": plain_text,
            "plain_text_sha256": plain_sha,
        },
        "statement_sha256",
    )
    statement_sha = statement["statement_sha256"]
    status_detail = seal_field(
        {
            "status_as_of": REVIEW_DATE,
            "basis": "pinned OpenConjecture source/model label preserved as a source assertion",
            "evidence_level": "source_dataset_model_assertion",
            "source_refs": [SOURCE_ID],
            "resolution_criterion": "prove or refute the exact source LaTeX conjecture block under its stated context",
            "independent_current_status_review": False,
        },
        "status_payload_sha256",
    )
    categories = list(source["categories"])
    primary_category = str(source["primary_category"])
    classification = seal_field(
        {
            "source_categories": categories,
            "source_primary_category": primary_category,
            "classification_system": "arXiv",
            "classification_status": "source_metadata_missing" if not categories and not primary_category else "source_metadata_only",
            "msc_codes": [],
            "msc_status": "unassigned",
        },
        "classification_payload_sha256",
    )
    provenance = seal_field(
        {
            "source_refs": [SOURCE_ID],
            "extraction_mode": "exact_jsonl_record_and_verbatim_latex_block",
            "extractor_version": "1.0.0",
            "extractor_schema_version": "awesome-theorems/openconjecture-eligible-pool/5.2",
            "source_record_sha256": source_sha,
            "eligible_pool_sha256": POOL_SHA256,
            "curation_ledger_path": relative_path(CURATION_PATH),
            "curation_ledger_authority_sha256": curation_authority,
            "curation_ledger_row_sha256": ledger_row["row_sha256"],
            "source_assertion_not_independent_truth_review": True,
            "no_formalization_claimed": True,
        },
        "provenance_payload_sha256",
    )
    allocation_request = {
        "origin_release": RELEASE,
        "source_id": SOURCE_ID,
        "content_hash": content_hash,
        "semantic_key": semantic_key,
        "statement_sha256": statement_sha,
        "family_action": "new_family",
    }
    allocation = {
        "parent_release_root_sha256": parent_root,
        "parent_registry_authority_sha256": parent_registry_authority,
        "allocation_request_sha256": sha256_bytes(canonical_json_bytes(allocation_request)),
        "transaction_id": f"S5-ALLOC-{atv_ordinal:08d}",
        "family_action": "new_family",
        "append_only": True,
    }
    identity_payload = {
        "semantic_key": semantic_key,
        "content_hash": content_hash,
        "statement_sha256": statement_sha,
        "source_record_sha256": source_sha,
    }
    normalized_latex = " ".join(body_tex.split())
    dedupe = {
        "identity_payload_sha256": sha256_bytes(canonical_json_bytes(identity_payload)),
        "semantic_key": semantic_key,
        "semantic_key_sha256": sha256_bytes(semantic_key.encode("utf-8")),
        "content_hash": content_hash,
        "body_tex_sha256": body_sha,
        "normalized_latex_sha256": sha256_bytes(normalized_latex.encode("utf-8")),
        "source_record_sha256": source_sha,
        "candidate_atv_ids": [],
        "verdict": "unique_new_claim",
        "validation_status": "independent_machine_validated_exact",
        "content_hash_unique_in_eligible_pool": True,
        "semantic_key_unique_in_release": True,
        "duplicate_grants_quota": False,
        "no_evidence_or_status_inheritance": True,
    }
    row: dict[str, Any] = {
        "schema_version": "awesome-theorems/stage5-math-claim-record/5.2",
        "release_id": RELEASE,
        "origin_stage": "Stage5",
        "origin_release": RELEASE,
        "curation_key": f"openconjecture/{content_hash}",
        "allocation": allocation,
        "occurrence_id": f"ATO-{atv_ordinal:08d}",
        "family_id": f"ATF-{atf_ordinal:08d}",
        "sense_id": f"ATS-{atv_ordinal:08d}",
        "variant_id": f"ATV-{atv_ordinal:08d}",
        "stage_claim_id": f"S5-CLM-{atv_ordinal:08d}",
        "display_name": str(ledger_row["atomic_statement_summary"]),
        "aliases": [str(source["title"])],
        "owner_domain": "mathematics",
        "membership_domains": ["mathematics"],
        "record_role": "claim",
        "claim_kind": "conjecture",
        "current_claim_kind": "conjecture",
        "historical_kind": "conjecture",
        "atomicity": "atomic",
        "atomicity_detail": {
            "allocation_unit": "one_exact_source_conjecture_environment",
            "whole_coherent_compound_block_allowed": True,
            "logical_irreducibility_asserted": False,
        },
        "truth_apt": True,
        "category": "open_claim",
        "material_status": "open",
        "source_id": SOURCE_ID,
        "source_locator": locator,
        "source_block": source_block,
        "paper": paper,
        "model_label": model_label,
        "curator_disposition": curator,
        "mathematical_statement": statement,
        "status_detail": status_detail,
        "classification": classification,
        "provenance": provenance,
        "rights": rights,
        "dedupe": dedupe,
        "frontier": {
            "class": "source_model_asserted_open_frontier",
            "as_of": REVIEW_DATE,
            "basis": "pinned OpenConjecture real_open_conjecture label",
            "source_refs": [SOURCE_ID],
            "evidence_level": "source_model_label",
            "independent_review": False,
        },
        "importance": {
            "tier": "source_scored_research_interest",
            "basis": "source_model_interestingness_signal_only",
            "source_score": source["latest_interestingness_score"],
            "source_score_confidence": source["latest_interestingness_confidence"],
            "rationale": source["latest_interestingness_rationale"],
            "independent_ranking": False,
        },
        "lifecycle": "active",
        "lineage": [],
        "semantic_key": semantic_key,
    }
    row["content_payload_sha256"] = sha256_bytes(
        canonical_json_bytes({"source_block": source_block, "mathematical_statement": statement})
    )
    row["source_payload_sha256"] = sha256_bytes(
        canonical_json_bytes({"source_locator": locator, "paper": paper, "model_label": model_label})
    )
    row["semantic_payload_sha256"] = sha256_bytes(
        canonical_json_bytes(
            {
                "record_role": row["record_role"],
                "atomicity": row["atomicity"],
                "truth_apt": row["truth_apt"],
                "category": row["category"],
                "current_claim_kind": row["current_claim_kind"],
                "semantic_key": semantic_key,
                "statement_sha256": statement_sha,
            }
        )
    )
    return row


def verify_new_record(
    actual: Mapping[str, Any], expected: Mapping[str, Any], schema: Mapping[str, Any], index: int
) -> None:
    label = f"origin-5.2 catalog row {index}"
    require(actual == expected, f"{label} does not exactly rebuild from its source and curation row")
    require(not (FORBIDDEN_LATEX_FIELDS & set(actual)), f"{label} fabricates Lean/formal fields")
    validate_record_schema(actual, schema, label)


def authoritative_inputs(
    checker: Checker,
    contract: Mapping[str, Any],
    schema: Mapping[str, Any],
    registry: Mapping[str, Any],
    receipt: Mapping[str, Any],
    curation: Mapping[str, Any],
    parent: Mapping[str, Mapping[str, Any]],
    parent_payloads: Mapping[str, bytes],
) -> dict[str, Any]:
    return {
        "contract": authority_binding(checker, CONTRACT_PATH, contract),
        "record_schema": authority_binding(checker, SCHEMA_PATH, schema),
        "source_registry": authority_binding(checker, SOURCE_REGISTRY_PATH, registry),
        "parent_strict_receipt": authority_binding(checker, STRICT_RECEIPT_PATH, receipt),
        "curation_ledger": authority_binding(checker, CURATION_PATH, curation),
        "upstream_asset": {
            "path": relative_path(UPSTREAM_PATH),
            "file_sha256": sha256_file(checker.path(UPSTREAM_PATH)),
            "size_bytes": checker.path(UPSTREAM_PATH).stat().st_size,
        },
        "eligible_pool": {
            "path": relative_path(POOL_PATH),
            "file_sha256": sha256_file(checker.path(POOL_PATH)),
            "size_bytes": checker.path(POOL_PATH).stat().st_size,
        },
        "parent_release": {
            "release": PARENT_RELEASE,
            "release_root_sha256": parent[MANIFEST_NAME]["release_root_sha256"],
            "manifest_file_sha256": sha256_bytes(parent_payloads[MANIFEST_NAME]),
            "manifest_authority_sha256": parent[MANIFEST_NAME]["authority_sha256"],
            "registry_authority_sha256": parent["Claim_ID_Registry.json"]["authority_sha256"],
        },
    }


def theorem_predicate(row: Mapping[str, Any]) -> bool:
    return bool(
        row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "theorem"
        and row.get("current_claim_kind") == "theorem"
        and row.get("material_status") == "proved"
        and row.get("declaration_kind") == "theorem"
    )


def open_predicate(row: Mapping[str, Any]) -> bool:
    admitted = bool(
        row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "open_claim"
        and row.get("current_claim_kind") in {"conjecture", "hypothesis", "open_problem"}
        and row.get("material_status") in {"open", "partial", "independent", "disputed"}
    )
    if not admitted:
        return False
    if row.get("origin_release") == RELEASE:
        block = row.get("source_block")
        return isinstance(block, dict) and block.get("language") == "LaTeX"
    return row.get("declaration_kind") == "theorem"


def parent_syntactic_strict(row: Mapping[str, Any]) -> bool:
    return bool(
        row.get("origin_stage") == "Stage5"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "open_claim"
        and row.get("claim_kind") == "conjecture"
        and row.get("current_claim_kind") == "conjecture"
        and row.get("declaration_kind") == "theorem"
        and row.get("formal_shape") == "direct_prop"
        and row.get("material_status") == "open"
        and row.get("lifecycle") == "active"
    )


def moving_sofa_projection(row: Mapping[str, Any]) -> dict[str, Any]:
    """Rebuild the receipt's strict-membership evidence projection."""
    fields = (
        "variant_id",
        "stage_claim_id",
        "record_role",
        "atomicity",
        "truth_apt",
        "category",
        "current_claim_kind",
        "declaration_kind",
        "formal_shape",
        "material_status",
        "lifecycle",
    )
    return {field: row.get(field) for field in fields}


def verify_parent_strict_receipt(
    checker: Checker,
    receipt: Mapping[str, Any],
    parent: Mapping[str, Mapping[str, Any]],
    parent_payloads: Mapping[str, bytes],
) -> tuple[list[Mapping[str, Any]], dict[str, Any]]:
    binding = receipt.get("parent_release")
    require(isinstance(binding, dict), "strict receipt parent binding is malformed")
    require(binding.get("release") == PARENT_RELEASE, "strict receipt parent release drifted")
    require(binding.get("release_root_sha256") == parent[MANIFEST_NAME]["release_root_sha256"], "strict receipt parent root drifted")
    require(binding.get("manifest_file_sha256") == sha256_bytes(parent_payloads[MANIFEST_NAME]), "strict receipt manifest binding drifted")
    require(binding.get("manifest_authority_sha256") == parent[MANIFEST_NAME]["authority_sha256"], "strict receipt manifest authority drifted")
    require(binding.get("claim_catalog_file_sha256") == sha256_bytes(parent_payloads["Claim_Catalog.json"]), "strict receipt catalog bytes drifted")
    require(binding.get("claim_catalog_authority_sha256") == parent["Claim_Catalog.json"]["authority_sha256"], "strict receipt catalog authority drifted")
    parent_rows = parent["Claim_Catalog.json"]["records"]
    strict_rows = sorted(
        (row for row in parent_rows if parent_syntactic_strict(row)),
        key=lambda row: str(row["stage_claim_id"]),
    )
    strict_s5 = [str(row["stage_claim_id"]) for row in strict_rows]
    strict_atv = [str(row["variant_id"]) for row in strict_rows]
    open_rows = [row for row in parent_rows if open_predicate(row)]
    non_strict_s5 = sorted(
        str(row["stage_claim_id"])
        for row in open_rows
        if not parent_syntactic_strict(row)
    )
    rebuild = receipt["rebuild"]
    require(len(strict_rows) == 401, "parent syntactic strict count is not 401")
    require(rebuild.get("syntactic_strict_count") == len(strict_rows), "strict receipt syntactic count drifted")
    require(rebuild.get("syntactic_strict_s5_id_set_sha256") == set_digest(strict_s5), "strict receipt S5 set digest drifted")
    require(rebuild.get("syntactic_strict_atv_id_set_sha256") == set_digest(strict_atv), "strict receipt ATV set digest drifted")
    require(len(open_rows) == 1_000 and len(non_strict_s5) == 599, "parent strict/non-strict open partition drifted")
    require(rebuild.get("non_strict_open_count") == len(non_strict_s5), "strict receipt non-strict count drifted")
    require(rebuild.get("non_strict_open_s5_id_set_sha256") == set_digest(non_strict_s5), "strict receipt non-strict digest drifted")
    require(rebuild.get("partition_count") == len(open_rows) and rebuild.get("partition_is_exact") is True, "strict receipt partition metadata drifted")

    corrections = receipt.get("effective_5_2_credit_corrections")
    require(isinstance(corrections, list) and len(corrections) == 1, "strict receipt must contain one correction")
    correction = corrections[0]
    require(isinstance(correction, dict), "strict receipt correction is not an object")
    require(correction.get("stage_claim_id") == "S5-CLM-00005311", "MovingSofa S5 correction drifted")
    require(correction.get("variant_id") == "ATV-00005311", "MovingSofa ATV correction drifted")
    require(correction.get("qualified_name") == "MovingSofa.sofaConstant_eq_volume_iff_eq_gerversSofa", "MovingSofa qualified name drifted")
    require(
        correction.get("effective_release") == RELEASE
        and correction.get("effective_strict_credit") is False
        and correction.get("disposition") == "strict_credit_revoked"
        and correction.get("identity_changed") is False
        and correction.get("parent_record_changed") is False
        and correction.get("material_status_change_asserted") is False
        and correction.get("proof_or_refutation_asserted") is False,
        "MovingSofa correction changes more than 5.2 strict release credit",
    )
    by_s5 = {str(row["stage_claim_id"]): row for row in strict_rows}
    target = by_s5.get("S5-CLM-00005311")
    require(target is not None, "MovingSofa is not in the parent syntactic strict set")
    require(sha256_bytes(canonical_json_bytes(target)) == correction.get("parent_record_sha256"), "MovingSofa parent-record hash drifted")
    require(sha256_bytes(canonical_json_bytes(moving_sofa_projection(target))) == correction.get("parent_strict_projection_sha256"), "MovingSofa strict projection hash drifted")
    require(correction.get("qualified_name") == target.get("qualified_name"), "MovingSofa correction targets the wrong declaration")
    effective = [row for row in strict_rows if row["stage_claim_id"] != correction["stage_claim_id"]]
    effective_s5 = [str(row["stage_claim_id"]) for row in effective]
    effective_meta = receipt["effective_parent_credit"]
    require(len(effective) == 400, "effective parent strict set is not 400")
    require(effective_meta.get("revoked_count") == 1, "strict receipt revoked count drifted")
    require(effective_meta.get("revoked_s5_id_set_sha256") == set_digest([str(correction["stage_claim_id"])]), "revoked S5 set digest drifted")
    require(effective_meta.get("effective_strict_count") == len(effective), "effective parent count drifted")
    require(effective_meta.get("effective_strict_s5_id_set_sha256") == set_digest(effective_s5), "effective parent strict digest drifted")
    return effective, correction


def record_evidence_components(row: Mapping[str, Any]) -> dict[str, str]:
    if row.get("origin_release") == RELEASE:
        content_hash = str(row["content_payload_sha256"])
        source_hash = str(row["source_payload_sha256"])
        rights_hash = str(row["rights"]["rights_payload_sha256"])
    else:
        content_hash = sha256_bytes(
            canonical_json_bytes(
                {
                    "formal_statement": row.get("formal_statement"),
                    "mathematical_statement": row.get("mathematical_statement"),
                }
            )
        )
        source_hash = sha256_bytes(
            canonical_json_bytes(
                {
                    "source_id": row.get("source_id"),
                    "locator": row.get("locator"),
                    "formal_statement": row.get("formal_statement"),
                    "provenance": row.get("provenance"),
                }
            )
        )
        rights_hash = sha256_bytes(canonical_json_bytes(row["rights"]))
    return {
        "record_sha256": sha256_bytes(canonical_json_bytes(row)),
        "content_payload_sha256": content_hash,
        "source_payload_sha256": source_hash,
        "rights_payload_sha256": rights_hash,
        "allocation_request_sha256": str(row["allocation"]["allocation_request_sha256"]),
    }


def strict_credit_row(row: Mapping[str, Any], branch: str) -> dict[str, Any]:
    semantic_key = row.get("semantic_key")
    if not isinstance(semantic_key, str):
        semantic_key = "formal-conjectures-semantic/" + str(row["semantic_payload_sha256"])
    value = {
        "stage_claim_id": row["stage_claim_id"],
        "variant_id": row["variant_id"],
        "origin_release": row["origin_release"],
        "credit_source_branch": branch,
        "semantic_key": semantic_key,
        "grants_strict_conjecture_credit": True,
        "evidence_sha256": sha256_bytes(canonical_json_bytes(record_evidence_components(row))),
    }
    return seal_field(value, "row_sha256")


def expected_strict_ledger(
    checker: Checker,
    receipt: Mapping[str, Any],
    curation: Mapping[str, Any],
    parent: Mapping[str, Mapping[str, Any]],
    parent_payloads: Mapping[str, bytes],
    new_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    effective_parent, receipt_correction = verify_parent_strict_receipt(
        checker, receipt, parent, parent_payloads
    )
    credits = [
        strict_credit_row(row, "effective_parent_5_1_direct_prop")
        for row in effective_parent
    ] + [
        strict_credit_row(row, "origin_5_2_curated_latex_environment")
        for row in new_rows
    ]
    credits.sort(key=lambda row: str(row["stage_claim_id"]))
    require(len(credits) == 1_000, "effective strict credit reconstruction is not 1,000")
    require(len({row["stage_claim_id"] for row in credits}) == 1_000, "strict ledger repeats S5 IDs")
    require(len({row["variant_id"] for row in credits}) == 1_000, "strict ledger repeats ATV IDs")
    correction = {
        "stage_claim_id": receipt_correction["stage_claim_id"],
        "variant_id": receipt_correction["variant_id"],
        "disposition": "strict_credit_revoked",
        "effective_release": RELEASE,
        "grants_strict_conjecture_credit": False,
        "parent_record_sha256": receipt_correction["parent_record_sha256"],
        "receipt_authority_sha256": receipt["authority_sha256"],
    }
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-strict-conjecture-ledger/5.2",
            "release": RELEASE,
            "parent_release_root_sha256": parent[MANIFEST_NAME]["release_root_sha256"],
            "parent_strict_receipt_authority_sha256": receipt["authority_sha256"],
            "curation_ledger_authority_sha256": curation["authority_sha256"],
            "strict_credits": credits,
            "credit_corrections": [correction],
            "counts": {
                "effective_strict_credits": len(credits),
                "effective_parent_credits": len(effective_parent),
                "origin_5_2_credits": len(new_rows),
                "credit_corrections": 1,
            },
            "set_digests": {
                "effective_s5_id_set_sha256": set_digest(str(row["stage_claim_id"]) for row in credits),
                "effective_variant_id_set_sha256": set_digest(str(row["variant_id"]) for row in credits),
                "effective_parent_s5_id_set_sha256": set_digest(
                    str(row["stage_claim_id"])
                    for row in credits
                    if row["credit_source_branch"] == "effective_parent_5_1_direct_prop"
                ),
                "origin_5_2_s5_id_set_sha256": set_digest(
                    str(row["stage_claim_id"])
                    for row in credits
                    if row["credit_source_branch"] == "origin_5_2_curated_latex_environment"
                ),
            },
        }
    )


def new_registry_rows(
    rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    families: list[dict[str, Any]] = []
    senses: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    for row in rows:
        request = row["allocation"]["allocation_request_sha256"]
        families.append(
            {
                "family_id": row["family_id"],
                "curation_key": row["curation_key"],
                "display_titles": [row["display_name"]] + list(row["aliases"]),
                "member_occurrence_ids": [row["occurrence_id"]],
                "historical_member_occurrence_ids": [row["occurrence_id"]],
                "idempotency_request_sha256": request,
                "identity_state": "stage5_curated_latex_exact_family",
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
                "identity_state": "stage5_curated_latex_exact_sense",
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
                "identity_state": "stage5_curated_latex_exact_variant",
                "lifecycle": "current",
            }
        )
    return families, senses, variants


def expected_release_artifacts(
    checker: Checker,
    inputs: Mapping[str, Any],
    parent: Mapping[str, Mapping[str, Any]],
    parent_payloads: Mapping[str, bytes],
    new_rows: Sequence[dict[str, Any]],
    curation: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    parent_catalog = parent["Claim_Catalog.json"]
    all_rows = copy.deepcopy(parent_catalog["records"]) + list(new_rows)
    catalog = seal(
        {
            "schema_version": "awesome-theorems/stage5-claim-catalog/5.2",
            "artifact": "Claim_Catalog.json",
            "release": RELEASE,
            "catalog_scope": parent_catalog["catalog_scope"],
            "authoritative_inputs": copy.deepcopy(inputs),
            "counts": {
                "records": len(all_rows),
                "origin_theorems": sum(theorem_predicate(row) for row in new_rows),
                "origin_open_claims": sum(open_predicate(row) for row in new_rows),
                "cumulative_theorems": sum(theorem_predicate(row) for row in all_rows),
                "cumulative_open_claims": sum(open_predicate(row) for row in all_rows),
            },
            "records": all_rows,
        }
    )
    require(catalog["counts"] == {
        "records": 3_100,
        "origin_theorems": 0,
        "origin_open_claims": 600,
        "cumulative_theorems": 1_500,
        "cumulative_open_claims": 1_600,
    }, "catalog predicates do not independently reproduce the 5.2 counts")

    parent_registry = parent["Claim_ID_Registry.json"]
    new_families, new_senses, new_variants = new_registry_rows(new_rows)
    registry = seal(
        {
            "schema_version": "awesome-theorems/claim-id-registry/5.2",
            "artifact": "Claim_ID_Registry.json",
            "release": RELEASE,
            "parent_registry_authority_sha256": parent_registry["authority_sha256"],
            "baseline_registry_authority_sha256": parent_registry["baseline_registry_authority_sha256"],
            "authoritative_inputs": copy.deepcopy(inputs),
            "allocation_policy": {
                **copy.deepcopy(parent_registry["allocation_policy"]),
                "release_5_2_first_new_atv_ordinal": PARENT_ATV_HIGH_WATERMARK + 1,
                "release_5_2_new_family_first_atf_ordinal": PARENT_ATF_HIGH_WATERMARK + 1,
            },
            "namespace_high_watermarks": {
                "ATF": LAST_ATF_ORDINAL,
                "ATO": LAST_ATV_ORDINAL,
                "ATS": LAST_ATV_ORDINAL,
                "ATV": LAST_ATV_ORDINAL,
            },
            "families": copy.deepcopy(parent_registry["families"]) + new_families,
            "senses": copy.deepcopy(parent_registry["senses"]) + new_senses,
            "variants": copy.deepcopy(parent_registry["variants"]) + new_variants,
            "legacy_aliases": copy.deepcopy(parent_registry.get("legacy_aliases", [])),
            "redirects": copy.deepcopy(parent_registry.get("redirects", [])),
            "splits": copy.deepcopy(parent_registry.get("splits", [])),
            "family_membership_extensions": copy.deepcopy(parent_registry.get("family_membership_extensions", [])),
            "counts": {
                "families": len(parent_registry["families"]) + NEW_ROWS,
                "senses": len(parent_registry["senses"]) + NEW_ROWS,
                "variants": len(parent_registry["variants"]) + NEW_ROWS,
                "stage4_variants": parent_registry["counts"]["stage4_variants"],
                "stage5_additions": parent_registry["counts"]["stage5_additions"] + NEW_ROWS,
                "legacy_aliases": len(parent_registry.get("legacy_aliases", [])),
                "redirects": len(parent_registry.get("redirects", [])),
                "splits": len(parent_registry.get("splits", [])),
            },
        }
    )

    parent_stage = parent["Stage5_Claim_ID_Registry.json"]
    stage_additions = [
        {
            "ordinal": ordinal(str(row["variant_id"])),
            "variant_id": row["variant_id"],
            "predecessor_stage_claim_id": None,
            "stage_claim_id": row["stage_claim_id"],
            "lifecycle": "current",
        }
        for row in new_rows
    ]
    stage_registry = seal(
        {
            "schema_version": "awesome-theorems/stage5-claim-id-registry/5.2",
            "artifact": "Stage5_Claim_ID_Registry.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "numbering_policy": parent_stage["numbering_policy"],
            "counts": {"mappings": len(parent_stage["mappings"]) + len(stage_additions)},
            "mappings": copy.deepcopy(parent_stage["mappings"]) + stage_additions,
        }
    )

    parent_migration = parent["Migration_v4_to_v5.json"]
    migration_additions = [
        {
            "ordinal": ordinal(str(row["variant_id"])),
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
        for row in new_rows
    ]
    migration = seal(
        {
            "schema_version": "awesome-theorems/migration-v4-to-v5/5.2",
            "artifact": "Migration_v4_to_v5.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "v4_import_receipt": copy.deepcopy(parent_migration["v4_import_receipt"]),
            "counts": {
                "historical_bindings": parent_migration["counts"]["historical_bindings"],
                "new_allocations": parent_migration["counts"]["new_allocations"] + NEW_ROWS,
                "migrations": len(parent_migration["migrations"]) + len(migration_additions),
            },
            "migrations": copy.deepcopy(parent_migration["migrations"]) + migration_additions,
        }
    )

    def projection(name: str, predicate: Any) -> dict[str, Any]:
        projected = [row for row in all_rows if predicate(row)]
        return seal(
            {
                "schema_version": "awesome-theorems/stage5-query-projection/5.2",
                "artifact": name,
                "release": RELEASE,
                "authoritative_inputs": copy.deepcopy(inputs),
                "query": "pure predicate over Claim_Catalog.json; records copied byte-semantically",
                "stage_claim_ids": [row["stage_claim_id"] for row in projected],
                "counts": {"records": len(projected)},
                "records": projected,
            }
        )

    parent_coverage = parent["Coverage_Ledger.json"]
    coverage_additions = [
        {
            "candidate_key": row["candidate_key"],
            "source_id": SOURCE_ID,
            "source_record_id": row["source_record_id"],
            "source_record_sha256": row["source_record_sha256"],
            "content_hash": row["content_hash"],
            "semantic_key": row["semantic_key"],
            "disposition": row["disposition"],
            "reason_code": row["reason_code"],
            "target_variant_id": row["target_variant_id"],
            "target_s5_id": row["target_s5_id"],
            "duplicate_of_variant_id": row["duplicate_of_variant_id"],
            "grants_catalog_entry": row["grants_catalog_entry"],
            "grants_strict_conjecture_credit": row["grants_strict_conjecture_credit"],
            "origin_release": RELEASE,
            "curation_row_sha256": row["row_sha256"],
        }
        for row in curation["candidate_dispositions"]
    ]
    disposition_counts = Counter(row["disposition"] for row in coverage_additions)
    coverage = seal(
        {
            "schema_version": "awesome-theorems/stage5-coverage-ledger/5.2",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "candidate_dispositions": copy.deepcopy(parent_coverage["candidate_dispositions"]) + coverage_additions,
            "msc_coverage": copy.deepcopy(parent_coverage["msc_coverage"]),
            "counts": {
                "candidate_dispositions": len(parent_coverage["candidate_dispositions"]) + len(coverage_additions),
                "msc_coverage": len(parent_coverage["msc_coverage"]),
                "origin_5_2_candidates": len(coverage_additions),
                "origin_5_2_accepted_new_claims": disposition_counts["accepted_new_strict_open_claim"],
                "origin_5_2_nonaccepted": len(coverage_additions) - disposition_counts["accepted_new_strict_open_claim"],
            },
        }
    )
    strict = expected_strict_ledger(
        checker, receipt, curation, parent, parent_payloads, new_rows
    )
    return {
        "Claim_Catalog.json": catalog,
        "Claim_ID_Registry.json": registry,
        "Stage5_Claim_ID_Registry.json": stage_registry,
        "Migration_v4_to_v5.json": migration,
        "Theorem_List.json": projection("Theorem_List.json", theorem_predicate),
        "Open_Claim_List.json": projection("Open_Claim_List.json", open_predicate),
        "Coverage_Ledger.json": coverage,
        STRICT_LEDGER_NAME: strict,
    }


def verify_release_artifacts(
    actual: Mapping[str, Mapping[str, Any]],
    actual_payloads: Mapping[str, bytes],
    expected: Mapping[str, Mapping[str, Any]],
    parent: Mapping[str, Mapping[str, Any]],
    new_rows: Sequence[Mapping[str, Any]],
) -> None:
    require(set(expected) == set(RELEASE_FILES), "independent expected artifact set drifted")
    for name in RELEASE_FILES:
        require(actual[name] == expected[name], f"release artifact does not independently rebuild: {name}")
        require(actual_payloads[name] == encoded_document(expected[name]), f"release artifact byte drift: {name}")
    catalog_rows = actual["Claim_Catalog.json"]["records"]
    require(catalog_rows[:PARENT_CATALOG_ROWS] == parent["Claim_Catalog.json"]["records"], "5.2 catalog mutates the 5.1 parent prefix")
    require(catalog_rows[PARENT_CATALOG_ROWS:] == list(new_rows), "5.2 catalog suffix differs from rebuilt records")
    registry = actual["Claim_ID_Registry.json"]
    parent_registry = parent["Claim_ID_Registry.json"]
    for field in ("families", "senses", "variants"):
        require(registry[field][: len(parent_registry[field])] == parent_registry[field], f"5.2 registry mutates parent {field} prefix")
    require(actual["Stage5_Claim_ID_Registry.json"]["mappings"][: len(parent["Stage5_Claim_ID_Registry.json"]["mappings"])] == parent["Stage5_Claim_ID_Registry.json"]["mappings"], "5.2 stage registry mutates its parent prefix")
    require(actual["Migration_v4_to_v5.json"]["migrations"][: len(parent["Migration_v4_to_v5.json"]["migrations"])] == parent["Migration_v4_to_v5.json"]["migrations"], "5.2 migration mutates its parent prefix")
    require(actual["Coverage_Ledger.json"]["candidate_dispositions"][: len(parent["Coverage_Ledger.json"]["candidate_dispositions"])] == parent["Coverage_Ledger.json"]["candidate_dispositions"], "5.2 coverage mutates its parent prefix")
    require(actual["Theorem_List.json"]["records"] == parent["Theorem_List.json"]["records"], "5.2 theorem projection changes parent theorem rows")
    require(actual["Open_Claim_List.json"]["records"][:1_000] == parent["Open_Claim_List.json"]["records"], "5.2 open projection mutates parent rows")
    expected_atv = [f"ATV-{value:08d}" for value in range(5_985, 6_585)]
    expected_atf = [f"ATF-{value:08d}" for value in range(5_755, 6_355)]
    require([row["variant_id"] for row in new_rows] == expected_atv, "new ATV allocation is not contiguous 5985..6584")
    require([row["family_id"] for row in new_rows] == expected_atf, "new ATF allocation is not contiguous 5755..6354")
    require([row["stage_claim_id"] for row in new_rows] == [f"S5-CLM-{value:08d}" for value in range(5_985, 6_585)], "new S5 allocation is not rank-aligned")


def expected_manifest(
    artifacts: Mapping[str, Mapping[str, Any]],
    inputs: Mapping[str, Any],
    curation: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, bytes], str]:
    payloads = {name: encoded_document(artifacts[name]) for name in RELEASE_FILES}
    inventory = [
        {
            "path": name,
            "sha256": sha256_bytes(payloads[name]),
            "size_bytes": len(payloads[name]),
            "row_count": primary_row_count(artifacts[name]),
        }
        for name in sorted(RELEASE_FILES)
    ]
    root = release_root(inventory)
    catalog_counts = artifacts["Claim_Catalog.json"]["counts"]
    strict = artifacts[STRICT_LEDGER_NAME]
    manifest = seal(
        {
            "schema_version": "awesome-theorems/stage5-release-manifest/5.2",
            "release": RELEASE,
            "parent_release": PARENT_RELEASE,
            "parent_release_root_sha256": inputs["parent_release"]["release_root_sha256"],
            "release_root_sha256": root,
            "authoritative_inputs": copy.deepcopy(inputs),
            "accepted_set_digests": {
                "content_hash_set_sha256": curation["set_digests"]["accepted_content_hash_set_sha256"],
                "semantic_key_set_sha256": curation["set_digests"]["accepted_semantic_key_set_sha256"],
                "s5_id_set_sha256": curation["set_digests"]["accepted_s5_id_set_sha256"],
            },
            "strict_credit_binding": {
                "path": STRICT_LEDGER_NAME,
                "file_sha256": sha256_bytes(payloads[STRICT_LEDGER_NAME]),
                "authority_sha256": strict["authority_sha256"],
                "effective_s5_id_set_sha256": strict["set_digests"]["effective_s5_id_set_sha256"],
                "effective_variant_id_set_sha256": strict["set_digests"]["effective_variant_id_set_sha256"],
            },
            "artifacts": inventory,
            "counts": {
                "non_manifest_artifacts": len(inventory),
                "catalog_records": catalog_counts["records"],
                "origin_theorems": catalog_counts["origin_theorems"],
                "origin_open_claims": catalog_counts["origin_open_claims"],
                "cumulative_theorems": catalog_counts["cumulative_theorems"],
                "cumulative_open_claims": catalog_counts["cumulative_open_claims"],
                "effective_strict_conjecture_credits": strict["counts"]["effective_strict_credits"],
            },
        }
    )
    payloads[MANIFEST_NAME] = encoded_document(manifest)
    return manifest, payloads, root


def verify_manifest(
    actual: Mapping[str, Any],
    actual_payloads: Mapping[str, bytes],
    expected: Mapping[str, Any],
    expected_payloads: Mapping[str, bytes],
    expected_root: str,
) -> None:
    require(actual == expected, "5.2 manifest does not independently rebuild")
    require(actual_payloads[MANIFEST_NAME] == expected_payloads[MANIFEST_NAME], "5.2 manifest bytes drifted")
    require(actual.get("release_root_sha256") == expected_root, "5.2 manifest release root drifted")
    verify_inventory(actual, actual_payloads, {name: json.loads(actual_payloads[name]) for name in RELEASE_FILES}, RELEASE_FILES, "release 5.2")


def verify_current_pointer(
    checker: Checker, manifest_payload: bytes, root: str
) -> None:
    current = checker.load_json(CURRENT_PATH)
    verify_seal(current, str(CURRENT_PATH))
    if current.get("release") == RELEASE:
        expected = seal(
            {
                "schema_version": "awesome-theorems/stage5-current-release/5.2",
                "release": RELEASE,
                "release_root_sha256": root,
                "manifest_sha256": sha256_bytes(manifest_payload),
                "manifest_path": f"releases/{RELEASE}/{MANIFEST_NAME}",
            }
        )
        require(
            current == expected,
            "Current_Release.json is not the exact post-CAS 5.2 pointer",
        )
        return

    require(
        current.get("release") == IMMEDIATE_SUCCESSOR_RELEASE,
        "Current_Release.json points neither to 5.2 nor its immediate 5.3 successor",
    )
    successor_manifest_relative = (
        f"releases/{IMMEDIATE_SUCCESSOR_RELEASE}/{MANIFEST_NAME}"
    )
    require(
        current.get("schema_version")
        == "awesome-theorems/stage5-current-release/5.3"
        and current.get("manifest_path") == successor_manifest_relative,
        "Current_Release.json is not the exact 5.3 successor pointer shape",
    )

    successor, successor_payloads = load_release_documents(
        checker, IMMEDIATE_SUCCESSOR_DIR, RELEASE_FILES
    )
    successor_manifest = successor[MANIFEST_NAME]
    successor_manifest_payload = successor_payloads[MANIFEST_NAME]
    require(
        set(successor_manifest) == SUCCESSOR_MANIFEST_FIELDS,
        "5.3 successor manifest field closure drifted",
    )
    require(
        successor_manifest.get("schema_version")
        == "awesome-theorems/stage5-release-manifest/5.3"
        and successor_manifest.get("release") == IMMEDIATE_SUCCESSOR_RELEASE,
        "5.3 successor manifest identity drifted",
    )
    successor_root = verify_inventory(
        successor_manifest,
        successor_payloads,
        successor,
        RELEASE_FILES,
        "immediate successor 5.3",
    )
    require(
        successor_manifest.get("parent_release") == RELEASE,
        "5.3 successor manifest parent_release is not 5.2",
    )
    require(
        successor_manifest.get("parent_release_root_sha256") == root,
        "5.3 successor manifest does not bind the verified 5.2 release root",
    )
    expected = seal(
        {
            "schema_version": "awesome-theorems/stage5-current-release/5.3",
            "release": IMMEDIATE_SUCCESSOR_RELEASE,
            "release_root_sha256": successor_root,
            "manifest_sha256": sha256_bytes(successor_manifest_payload),
            "manifest_path": successor_manifest_relative,
        }
    )
    require(
        current == expected,
        "Current_Release.json does not exactly bind the authenticated 5.3 successor",
    )


def _run(checker: Checker) -> None:
    contract, schema, source_registry, receipt, curation = verify_authorities(checker)
    require(tuple(contract["release_layout"]["non_manifest_artifacts"]) == RELEASE_FILES, "contract 5.2 artifact set/order drifted")
    parent, parent_payloads = verify_parent_release(checker, contract)
    pool, locators, source_hashes = rebuild_source_pool(checker, contract, source_registry)
    accepted = verify_curation(
        checker,
        contract,
        curation,
        pool,
        source_hashes,
        parent["Claim_Catalog.json"]["records"],
    )
    parent_root = parent[MANIFEST_NAME]["release_root_sha256"]
    parent_registry_authority = parent["Claim_ID_Registry.json"]["authority_sha256"]
    new_rows = [
        expected_new_record(
            ledger_row,
            source,
            locators,
            source_hashes,
            parent_registry_authority,
            parent_root,
            curation["authority_sha256"],
        )
        for ledger_row, source in accepted
    ]
    actual, actual_payloads = load_release_documents(checker, RELEASE_DIR, RELEASE_FILES)
    actual_catalog = actual["Claim_Catalog.json"]["records"]
    require(isinstance(actual_catalog, list) and len(actual_catalog) == 3_100, "5.2 catalog is not 3,100 rows")
    for index, (observed, expected) in enumerate(
        zip(actual_catalog[PARENT_CATALOG_ROWS:], new_rows), start=PARENT_CATALOG_ROWS + 1
    ):
        verify_new_record(observed, expected, schema, index)
    inputs = authoritative_inputs(
        checker,
        contract,
        schema,
        source_registry,
        receipt,
        curation,
        parent,
        parent_payloads,
    )
    artifacts = expected_release_artifacts(
        checker, inputs, parent, parent_payloads, new_rows, curation, receipt
    )
    verify_release_artifacts(actual, actual_payloads, artifacts, parent, new_rows)
    manifest, expected_payloads, root = expected_manifest(artifacts, inputs, curation)
    verify_manifest(actual[MANIFEST_NAME], actual_payloads, manifest, expected_payloads, root)
    verify_current_pointer(checker, actual_payloads[MANIFEST_NAME], root)
    checker.note(
        "upstream=4415; pre-locator=931; eligible=889; curated=600; "
        "cross-parent-duplicates=7; parent-strict=401-1; effective-strict=1000"
    )
    checker.note(
        f"release_root={root}; catalog=3100; theorem=1500; open=1600"
    )


def run(checker: Checker) -> None:
    """Run the complete check, recording a clean diagnostic instead of traceback."""
    try:
        _run(checker)
    except (CheckFailure, OSError, KeyError, IndexError, TypeError, ValueError) as error:
        checker.fail(str(error))


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (default: inferred from this script)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    checker = Checker(args.root)
    run(checker)
    if checker.errors:
        print(f"FAIL check_math_catalog_v5_2 ({len(checker.errors)} errors)")
        for error in checker.errors:
            print(f"- {error}")
        for note in checker.notes:
            print(f"NOTE {note}")
        return 1
    print("PASS check_math_catalog_v5_2")
    for note in checker.notes:
        print(f"NOTE {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
