#!/usr/bin/env python3
"""Replay the repository-local Open Problem Garden v5.5 eligibility audit.

The validator is deliberately independent of the scripts and temporary capture
tree used to produce the curation artifacts.  It reads only this repository's
portable OPG interface and the five frozen, repository-local dedupe authorities.
By default it is read-only.  Pass ``--write-report`` to write the optional,
self-sealed ``eligibility-validation.json`` beside this file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


CURATION_REL = PurePosixPath(
    "Docs/catalog/v5/curation/openproblemgarden_v5_5"
)
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]

CUTOFF = "2026-08-10"
INITIAL_DECISIONS = {"accept": 140, "pending": 73, "reject": 191}
RELEASE_OTHER_SOURCE_ADMISSIONS = 315
RELEASE_TOTAL_MINIMUM = 401
RELEASE_OPG_MINIMUM = RELEASE_TOTAL_MINIMUM - RELEASE_OTHER_SOURCE_ADMISSIONS

LOCAL_NAMES = {
    "manifest": "manifest.json",
    "review_queue": "review-queue.jsonl",
    "review": "review.jsonl",
    "status_evidence": "status-evidence.jsonl",
    "cross_dedupe_retrieval": "cross-dedupe-retrieval.jsonl",
    "dedupe_review": "dedupe-review.jsonl",
    "ledger": "eligibility-ledger.jsonl",
    "receipt": "eligibility-receipt.json",
}

AUTHORITY_SPECS = {
    "parent_5_4": {
        "path": "Docs/catalog/v5/releases/5.4/Claim_Catalog.json",
        "sha256": "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709",
        "rows": None,
    },
    "oeis_268": {
        "path": "Docs/catalog/v5/curation/oeis_v5_5/combined-survivors.jsonl",
        "sha256": "d9928d3d61a05e618df7a044c98d966b6f4d8fe63925ea4e95bb2cd5e4de4e5a",
        "rows": 268,
    },
    "aimpl_43": {
        "path": "Docs/catalog/v5/curation/aimpl_v5_5/review-ledger.jsonl",
        "sha256": "8f6c129a07c948b1712d9ce855fb25c69329b42e12a2148597dab8bcaad9343b",
        "rows": 59,
    },
    "open_logic_4": {
        "path": "Docs/catalog/v5/curation/open_logic_v5_5/open-logic-review.jsonl",
        "sha256": "65fe1f6cafd939ab9604d860838b56488f32d321230ce759cf2b243724d4f1a2",
        "rows": 17,
    },
    "conjecturebench_302": {
        "path": (
            "Docs/catalog/v5/curation/conjecturebench_v5_5/"
            "strict-review-ledger-302.jsonl"
        ),
        "sha256": "4d13d77513ee7064fbe7bfa0cbd996cb491363afa17297a2a185cb1927407600",
        "rows": 302,
    },
}

# These are frozen capture-level commitments.  The portable projections do not
# redistribute raw OPG pages, fetched response bodies, query text, or excerpts.
ORIGINAL_CAPTURE_SHA = {
    "source_manifest": "fc1f885a0488b221eedfd43b6e46bc025ea428c0bec704304059645d228d1f7e",
    "review_queue": "f0472beafa46bd6cdbf477693e9d942c5d5f0314386b013415d483266f63db2b",
    "review": "1a4625c2b190344c5db5b6301f6a11e95f7e9d286dfdac5727bbf866d7968458",
    "status_evidence": "957ede724a462dc3df02c4d058ec9af89970a28f86ce8512b37e27b858bf86eb",
    "cross_dedupe_retrieval": "5a23770d3c991309caa888b0fe5c0d3fc21f45c2d7ef0683a5f284367fdd0c95",
}

CORPORA = {
    "parent_5_4",
    "oeis_accepted",
    "aimpl_accepted",
    "open_logic_accepted",
    "conjecturebench_full",
    "opg_batch",
}
BLOCKING_CORPORA = {
    "parent_5_4",
    "oeis_accepted",
    "aimpl_accepted",
    "open_logic_accepted",
    "opg_batch",
}
EVIDENCE_ONLY_CORPORA = {"conjecturebench_full"}
DEDUPE_POLICY = {
    "credit_blocking_corpora": [
        "aimpl_accepted",
        "oeis_accepted",
        "open_logic_accepted",
        "opg_batch",
        "parent_5_4",
    ],
    "conjecturebench_accepted_credit": 0,
    "evidence_only_corpora": ["conjecturebench_full"],
    "fixed_parent_open_target_identity_blocks": True,
    "fixed_parent_open_target_polarity_does_not_create_a_new_identity": True,
    "related_stronger_or_weaker_targets_are_not_equivalent": True,
    "retrieval_is_not_review_boundary": True,
    "schema_version": "awesome-theorems/openproblemgarden-dedupe-policy/2",
    "supplemental_targets_must_resolve_in_fixed_authority": True,
}
VERDICTS = {
    "unique",
    "canonical_opg",
    "duplicate_parent",
    "duplicate_oeis",
    "duplicate_aimpl",
    "duplicate_open_logic",
    "duplicate_opg",
}
VERDICT_CORPUS = {
    "duplicate_parent": "parent_5_4",
    "duplicate_oeis": "oeis_accepted",
    "duplicate_aimpl": "aimpl_accepted",
    "duplicate_open_logic": "open_logic_accepted",
    "duplicate_opg": "opg_batch",
}

SHA_RE = re.compile(r"[0-9a-f]{64}")
URL_RE = re.compile(r"https?://\S+")
REASON_RE = re.compile(r"[a-z0-9]+(?:_[a-z0-9]+)*")
WINDOWS_ABS_RE = re.compile(r"^[A-Za-z]:[\\/]")
HOST_ABS_RE = re.compile(
    r"(?:^|[\s\"'=:])/(?:home|Users|root|var|private|mnt|opt|usr|etc|"
    r"workspace|workspaces|srv|run|dev|proc|sys)(?:/|$)"
)
TEXT_KEYS = {
    "title",
    "name",
    "display_name",
    "aliases",
    "exact_claim_text",
    "exact_statement",
    "source_statement",
    "semantic_summary",
    "normalized_text",
    "original_text",
    "natural_language",
    "plain_text",
    "body_tex",
    "formal_type",
    "statement",
    "mathematical_statement",
    "formal_statement",
    "problem_text",
}


class ValidationError(RuntimeError):
    """An actionable failure in the authoritative curation interface."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_line(value: Any) -> bytes:
    return canonical(value) + b"\n"


def reject_constant(value: str) -> None:
    raise ValidationError(f"non-finite JSON number {value!r}")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def parse_json(raw: bytes, where: str) -> Any:
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"{where}: invalid UTF-8: {exc}") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    except ValidationError:
        raise
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValidationError(f"{where}: invalid JSON: {exc}") from exc
    validate_numbers(value, where)
    return value


def validate_numbers(value: Any, where: str) -> None:
    if isinstance(value, float):
        require(math.isfinite(value), f"{where}: non-finite JSON number")
    elif isinstance(value, dict):
        for key, child in value.items():
            validate_numbers(child, f"{where}/{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            validate_numbers(child, f"{where}/{index}")


def validate_no_host_paths(value: Any, where: str, key: str | None = None) -> None:
    if isinstance(value, str):
        lowered = value.casefold()
        require("/tmp" not in lowered, f"{where}: forbidden /tmp authority")
        require("file://" not in lowered, f"{where}: forbidden file URI")
        require(not WINDOWS_ABS_RE.match(value), f"{where}: Windows absolute path")
        require(not value.startswith("\\\\"), f"{where}: UNC absolute path")
        require(not HOST_ABS_RE.search(value), f"{where}: host absolute path")
        require(str(REPO) not in value, f"{where}: repository host path leaked")
        if key and (key == "path" or key.endswith("_path")) and value.startswith("/"):
            require(
                value.startswith(("/op/", "/category/", "/node/", "/files/")),
                f"{where}: absolute filesystem-like path",
            )
    elif isinstance(value, dict):
        for child_key, child in value.items():
            validate_no_host_paths(child, f"{where}/{child_key}", child_key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            validate_no_host_paths(child, f"{where}/{index}", key)


def load_canonical_json(path: Path, *, scan_paths: bool = True) -> dict[str, Any]:
    raw = path.read_bytes()
    value = parse_json(raw, str(path))
    require(isinstance(value, dict), f"{path}: top level must be an object")
    require(raw == canonical_line(value), f"{path}: JSON is not canonical one-line + LF")
    if scan_paths:
        validate_no_host_paths(value, path.name)
    return value


def load_canonical_jsonl(
    path: Path, *, scan_paths: bool = True
) -> tuple[list[dict[str, Any]], list[bytes]]:
    raw = path.read_bytes()
    require(bool(raw), f"{path}: empty JSONL")
    lines = raw.splitlines(keepends=True)
    require(all(line.endswith(b"\n") for line in lines), f"{path}: missing final LF")
    rows: list[dict[str, Any]] = []
    payloads: list[bytes] = []
    for number, line in enumerate(lines, 1):
        require(line != b"\n", f"{path}:{number}: blank JSONL line")
        payload = line[:-1]
        value = parse_json(payload, f"{path}:{number}")
        require(isinstance(value, dict), f"{path}:{number}: row must be an object")
        require(line == canonical_line(value), f"{path}:{number}: noncanonical JSONL row")
        if scan_paths:
            validate_no_host_paths(value, f"{path.name}:{number}")
        rows.append(value)
        payloads.append(payload)
    return rows, payloads


def assert_keys(value: Any, required: set[str], where: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{where}: expected object")
    missing = required - set(value)
    require(not missing, f"{where}: missing keys {sorted(missing)}")
    return value


def assert_exact_keys(value: Any, expected: set[str], where: str) -> dict[str, Any]:
    result = assert_keys(value, expected, where)
    require(set(result) == expected, f"{where}: unexpected keys {sorted(set(result)-expected)}")
    return result


def require_sha(value: Any, where: str) -> str:
    require(isinstance(value, str) and SHA_RE.fullmatch(value) is not None, where)
    return value


def require_url(value: Any, where: str) -> str:
    require(isinstance(value, str) and URL_RE.fullmatch(value) is not None, where)
    return value


def normalized_source_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalized_semantic(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"\s+", " ", normalized).strip()


def semantic_key(summary: str) -> str:
    return "semantic-summary-nfkc-v1/" + sha256_bytes(
        normalized_semantic(summary).encode("utf-8")
    )


def relative_path(name: str) -> str:
    return str(CURATION_REL / name)


def binding_for_row(
    name: str,
    path: Path,
    row_number: int,
    payload: bytes,
    row: dict[str, Any],
) -> dict[str, Any]:
    return {
        "path": relative_path(name),
        "file_sha256": sha256_file(path),
        "row_number": row_number,
        "candidate_index": row["candidate_index"],
        "candidate_key": row["candidate_key"],
        "row_sha256": sha256_bytes(payload),
    }


def validate_row_binding(
    actual: Any,
    expected: dict[str, Any],
    where: str,
    *,
    allow_extra: bool = False,
) -> None:
    require(isinstance(actual, dict), f"{where}: binding must be an object")
    if not allow_extra:
        require(set(actual) == set(expected), f"{where}: binding fields drifted")
    for key, value in expected.items():
        require(actual.get(key) == value, f"{where}/{key}: binding mismatch")


def artifact_binding(name: str, path: Path, rows: int | None) -> dict[str, Any]:
    return {
        "path": relative_path(name),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
        "rows": rows,
    }


def validate_self_seal(value: dict[str, Any], where: str) -> None:
    require_sha(value.get("authority_sha256"), f"{where}: invalid authority_sha256")
    projection = {key: child for key, child in value.items() if key != "authority_sha256"}
    require(
        value["authority_sha256"] == sha256_bytes(canonical(projection)),
        f"{where}: stale self-seal",
    )


def all_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [text for child in value.values() for text in all_strings(child)]
    if isinstance(value, list):
        return [text for child in value for text in all_strings(child)]
    return []


def selected_strings(value: Any, keys: set[str]) -> list[str]:
    result: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in keys:
                result.extend(all_strings(child))
            elif isinstance(child, (dict, list)):
                result.extend(selected_strings(child, keys))
    elif isinstance(value, list):
        for child in value:
            result.extend(selected_strings(child, keys))
    return result


def retrieval_document(
    label: str,
    text: str,
    material_status: str,
    preexisting: bool,
    source: str,
) -> dict[str, Any]:
    excerpt = re.sub(r"\s+", " ", text).strip()[:1000]
    return {
        "label_sha256": sha256_bytes(label.encode("utf-8")),
        "text_excerpt_sha256": sha256_bytes(excerpt.encode("utf-8")),
        "material_status": material_status,
        "preexisting_strict_or_accepted_candidate": preexisting,
        "source": source,
    }


def query_text(candidate: dict[str, Any], review: dict[str, Any]) -> str:
    return "\n".join(
        filter(
            None,
            [
                candidate["source"]["title"],
                review["exact_claim_context"],
                review["exact_claim_text"],
                review["semantic_summary"],
                " ".join(item["name"] for item in candidate["context"]["subjects"]),
                " ".join(item["name"] for item in candidate["context"]["keywords"]),
            ],
        )
    )


def validate_capture_binding(
    value: Any, artifact_sha: str, row_number: int, where: str
) -> None:
    binding = assert_exact_keys(
        value, {"artifact_sha256", "row_number", "row_sha256"}, where
    )
    require(binding["artifact_sha256"] == artifact_sha, f"{where}: artifact SHA drift")
    require(binding["row_number"] == row_number, f"{where}: source row drift")
    require_sha(binding["row_sha256"], f"{where}: invalid source row SHA")


def load_authorities() -> tuple[
    dict[str, dict[str, Any]],
    dict[str, set[str]],
    dict[str, dict[str, dict[str, Any]]],
    dict[str, str],
]:
    authority_set: dict[str, dict[str, Any]] = {}
    loaded: dict[str, Any] = {}
    for name, spec in AUTHORITY_SPECS.items():
        path = REPO / spec["path"]
        require(path.is_file(), f"missing frozen authority {spec['path']}")
        require(sha256_file(path) == spec["sha256"], f"{name}: authority SHA drift")
        if path.suffix == ".jsonl":
            rows, _ = load_canonical_jsonl(path)
            require(len(rows) == spec["rows"], f"{name}: physical row count drift")
            loaded[name] = rows
        else:
            document = load_canonical_json(path)
            records = document.get("records")
            require(isinstance(records, list) and len(records) == 4100, "parent row drift")
            loaded[name] = records
        authority_set[name] = {
            "path": spec["path"],
            "sha256": spec["sha256"],
            "size_bytes": path.stat().st_size,
            "rows": spec["rows"],
        }

    parent = loaded["parent_5_4"]
    oeis = loaded["oeis_268"]
    aimpl = loaded["aimpl_43"]
    open_logic = loaded["open_logic_4"]
    cb = loaded["conjecturebench_302"]

    parent_by_id = {row["variant_id"]: row for row in parent}
    require(len(parent_by_id) == 4100, "parent authority IDs are not unique")
    oeis_by_id = {"oeis/" + row["candidate_key"]: row for row in oeis}
    require(len(oeis_by_id) == 268, "OEIS authority IDs are not unique")
    aimpl_by_id = {
        row["candidate_key"]: row for row in aimpl if row.get("final_decision") == "accept"
    }
    require(len(aimpl_by_id) == 43, "AIMPL accepted authority denominator drifted")
    open_logic_by_id = {
        f"openlogic/{row['problem_id']}": row
        for row in open_logic
        if row.get("decision") == "accept"
    }
    require(len(open_logic_by_id) == 4, "Open Logic accepted denominator drifted")
    cb_by_id = {row["cb_id"]: row for row in cb}
    require(len(cb_by_id) == 302, "ConjectureBench IDs are not unique")

    namespaces = {
        "parent_5_4": set(parent_by_id),
        "oeis_accepted": set(oeis_by_id),
        "aimpl_accepted": set(aimpl_by_id),
        "open_logic_accepted": set(open_logic_by_id),
        "conjecturebench_full": set(cb_by_id),
    }
    docs: dict[str, dict[str, dict[str, Any]]] = {name: {} for name in CORPORA}
    for doc_id, row in parent_by_id.items():
        docs["parent_5_4"][doc_id] = retrieval_document(
            str(row["display_name"]),
            "\n".join(selected_strings(row, TEXT_KEYS)),
            str(row.get("material_status")),
            True,
            "parent_5_4",
        )
    for doc_id, row in oeis_by_id.items():
        label = (
            row.get("a_number")
            or ",".join(row.get("a_numbers") or [])
            or row.get("sequence")
            or row.get("title")
            or row["candidate_key"]
        )
        docs["oeis_accepted"][doc_id] = retrieval_document(
            str(label),
            "\n".join(selected_strings(row, TEXT_KEYS)),
            "accepted_candidate_survivor",
            True,
            f"oeis_{row.get('audit_layer') or 'combined'}",
        )
    for doc_id, row in aimpl_by_id.items():
        docs["aimpl_accepted"][doc_id] = retrieval_document(
            str(row.get("source_record_key", doc_id)),
            "\n".join(selected_strings(row, TEXT_KEYS)),
            "accepted_candidate",
            True,
            "aimpl",
        )
    for doc_id, row in open_logic_by_id.items():
        docs["open_logic_accepted"][doc_id] = retrieval_document(
            str(row.get("name", row["problem_id"])),
            "\n".join(selected_strings(row, TEXT_KEYS)),
            "accepted_candidate",
            True,
            "open_logic",
        )
    for doc_id, row in cb_by_id.items():
        docs["conjecturebench_full"][doc_id] = retrieval_document(
            str(row.get("exact_claim_text") or doc_id),
            "\n".join(selected_strings(row, TEXT_KEYS)),
            str(row.get("decision")),
            row.get("decision") == "accept",
            "conjecturebench",
        )
    parent_kinds = {
        doc_id: str(row.get("current_claim_kind")) for doc_id, row in parent_by_id.items()
    }
    return authority_set, namespaces, docs, parent_kinds


def validate_manifest(
    manifest: dict[str, Any],
    paths: dict[str, Path],
    row_counts: dict[str, int],
    authority_set: dict[str, dict[str, Any]],
) -> tuple[str, str]:
    required = {
        "schema_version",
        "cutoff",
        "candidate_only",
        "raw_source_bodies_redistributed",
        "artifacts",
        "upstream_provenance",
        "authority_set",
        "authority_set_sha256",
        "dedupe_policy",
        "dedupe_scope_sha256",
        "authority_sha256",
    }
    assert_keys(manifest, required, "manifest")
    require(
        manifest["schema_version"]
        == "awesome-theorems/openproblemgarden-portable-manifest/1",
        "manifest: wrong schema",
    )
    require(manifest["cutoff"] == CUTOFF, "manifest: cutoff drift")
    require(manifest["candidate_only"] is True, "manifest: candidate boundary")
    require(
        manifest["raw_source_bodies_redistributed"] is False,
        "manifest: raw body redistribution claimed",
    )
    validate_self_seal(manifest, "manifest")

    expected_authority_sha = sha256_bytes(canonical(authority_set))
    require(manifest["authority_set"] == authority_set, "manifest: authority set drift")
    require(
        manifest["authority_set_sha256"] == expected_authority_sha,
        "manifest: authority-set digest drift",
    )
    require(manifest["dedupe_policy"] == DEDUPE_POLICY, "manifest: dedupe policy drift")

    artifacts = assert_keys(manifest["artifacts"], set(), "manifest/artifacts")
    expected_artifact_names = {
        "review_queue",
        "review",
        "status_evidence",
        "cross_dedupe_retrieval",
        "dedupe_review",
    }
    require(set(artifacts) == expected_artifact_names, "manifest: artifact set drift")
    for logical_name in sorted(expected_artifact_names):
        expected = artifact_binding(
            LOCAL_NAMES[logical_name], paths[logical_name], row_counts[logical_name]
        )
        require(
            artifacts[logical_name] == expected,
            f"manifest/artifacts/{logical_name}: stale binding",
        )

    upstream = manifest["upstream_provenance"]
    require(isinstance(upstream, dict) and upstream, "manifest: upstream provenance missing")
    frozen_values = set(ORIGINAL_CAPTURE_SHA.values())
    observed_values = {
        text
        for text in all_strings(manifest)
        if isinstance(text, str) and SHA_RE.fullmatch(text)
    }
    require(
        frozen_values <= observed_values,
        "manifest: one or more frozen capture SHAs are missing",
    )
    scope_projection = {
        "authority_set_sha256": expected_authority_sha,
        "initial_review_sha256": sha256_file(paths["review"]),
        "original_retrieval_sha256": ORIGINAL_CAPTURE_SHA["cross_dedupe_retrieval"],
        "policy": DEDUPE_POLICY,
    }
    dedupe_scope_sha = sha256_bytes(canonical(scope_projection))
    require(
        manifest["dedupe_scope_sha256"] == dedupe_scope_sha,
        "manifest: dedupe-scope digest drift",
    )
    return expected_authority_sha, dedupe_scope_sha


def validate_queue_and_reviews(
    queue_rows: list[dict[str, Any]],
    review_rows: list[dict[str, Any]],
) -> tuple[dict[int, dict[str, Any]], dict[int, dict[str, Any]], set[int]]:
    require(len(queue_rows) == len(review_rows) == 404, "review universe is not 404")
    require(
        sha256_file(HERE / LOCAL_NAMES["review"]) == ORIGINAL_CAPTURE_SHA["review"],
        "review.jsonl differs from the frozen independently validated review",
    )
    queue: dict[int, dict[str, Any]] = {}
    reviews: dict[int, dict[str, Any]] = {}
    candidate_keys: set[str] = set()
    source_keys: set[str] = set()
    review_required = {
        "schema_version",
        "candidate_index",
        "candidate_key",
        "source_record_key",
        "source_url",
        "snapshot_sha256",
        "candidate_only",
        "strict_credit_granted",
        "release_mutation_authorized_or_performed",
        "decision",
        "reason_code",
        "review_basis",
        "source_form",
        "exact_claim_text",
        "exact_claim_context",
        "truth_apt",
        "context_complete",
        "question_to_assertion_promotion_performed",
        "source_asserted_open",
        "full_discussion_reviewed",
        "current_open_as_of_2026_08_10",
        "current_status_evidence",
        "importance_tier",
        "semantic_summary",
        "atomicity",
        "duplicate_hints",
        "rights_handling",
    }
    queue_required = {
        "schema_version",
        "candidate_index",
        "candidate_key",
        "candidate_only",
        "source_record_key",
        "source",
        "context",
        "importance",
        "mechanical_screen",
        "admission_boundary",
        "source_status_evidence",
        "exact_source_commitments",
        "rights",
        "original_capture_binding",
        "raw_source_body_redistributed",
    }
    banned_queue_keys = {
        "problem_div_html",
        "discussion_div_html",
        "problem_text",
        "discussion_text",
        "snapshot_path",
        "html_path",
        "body",
        "body_path",
    }

    def check_banned(value: Any, where: str) -> None:
        if isinstance(value, dict):
            found = banned_queue_keys & set(value)
            require(not found, f"{where}: raw/body fields present: {sorted(found)}")
            for key, child in value.items():
                check_banned(child, f"{where}/{key}")
        elif isinstance(value, list):
            for number, child in enumerate(value):
                check_banned(child, f"{where}/{number}")

    for expected_index, (candidate, review) in enumerate(
        zip(queue_rows, review_rows, strict=True), 1
    ):
        where = f"candidate {expected_index}"
        assert_exact_keys(candidate, queue_required, f"{where}/source")
        assert_keys(review, review_required, f"{where}/review")
        check_banned(candidate, f"{where}/source")
        require(
            candidate["schema_version"]
            == "awesome-theorems/openproblemgarden-portable-source-evidence/1",
            f"{where}: source schema drift",
        )
        require(
            candidate["candidate_only"] is True
            and candidate["raw_source_body_redistributed"] is False,
            f"{where}: portable candidate/body boundary drift",
        )
        require(
            review["schema_version"]
            == "awesome-theorems/openproblemgarden-strict-review/1",
            f"{where}: review schema drift",
        )
        require(
            candidate["candidate_index"] == review["candidate_index"] == expected_index,
            f"{where}: index/order mismatch",
        )
        key = candidate["candidate_key"]
        source_key = candidate["source_record_key"]
        require(
            isinstance(key, str) and key not in candidate_keys,
            f"{where}: duplicate/invalid candidate key",
        )
        require(
            isinstance(source_key, str) and source_key not in source_keys,
            f"{where}: duplicate/invalid source key",
        )
        candidate_keys.add(key)
        source_keys.add(source_key)
        require(review["candidate_key"] == key, f"{where}: review candidate binding")
        require(review["source_record_key"] == source_key, f"{where}: review source binding")

        commitments = assert_keys(
            candidate["exact_source_commitments"],
            {
                "problem_div_html_sha256",
                "discussion_div_html_sha256",
                "problem_text_sha256",
                "discussion_text_sha256",
                "problem_text_size_bytes",
                "discussion_text_size_bytes",
                "exact_claim_binding",
                "discussion_passage_bindings",
            },
            f"{where}/commitments",
        )
        for field in (
            "problem_div_html_sha256",
            "discussion_div_html_sha256",
            "problem_text_sha256",
            "discussion_text_sha256",
        ):
            require_sha(commitments[field], f"{where}/{field}: invalid SHA")
        for field in ("problem_text_size_bytes", "discussion_text_size_bytes"):
            require(
                is_int(commitments[field]) and commitments[field] >= 0,
                f"{where}/{field}: invalid size",
            )
        expected_key = sha256_bytes(
            (source_key + "\0" + commitments["problem_div_html_sha256"]).encode("utf-8")
        )[:20]
        require(key == expected_key, f"{where}: candidate-key formula mismatch")
        validate_capture_binding(
            candidate["original_capture_binding"],
            ORIGINAL_CAPTURE_SHA["review_queue"],
            expected_index,
            f"{where}/original_capture_binding",
        )

        source = assert_keys(
            candidate["source"],
            {"collection", "url", "node_id", "title", "snapshot_sha256"},
            f"{where}/source",
        )
        require(source["collection"] == "Open Problem Garden", f"{where}: source collection")
        require_url(source["url"], f"{where}: invalid OPG URL")
        require_sha(source["snapshot_sha256"], f"{where}: invalid snapshot SHA")
        require(review["source_url"] == source["url"], f"{where}: review URL binding")
        require(
            review["snapshot_sha256"] == source["snapshot_sha256"],
            f"{where}: review snapshot binding",
        )
        importance = assert_keys(
            candidate["importance"], {"stars", "eligible_tier"}, f"{where}/importance"
        )
        require(
            is_int(importance["stars"]) and importance["stars"] in {2, 3, 4},
            f"{where}: invalid OPG stars",
        )
        require(
            importance["eligible_tier"]
            == ("high" if importance["stars"] >= 3 else "medium"),
            f"{where}: importance mapping drift",
        )
        admission = assert_keys(
            candidate["admission_boundary"],
            {
                "candidate_only",
                "strict_credit_granted",
                "question_to_assertion_promotion_permitted",
                "accept_only_complete_truth_apt_source_assertions",
                "accept_only_current_open_as_of",
                "semantic_uniqueness_requires_later_cross_dedupe",
            },
            f"{where}/admission",
        )
        require(admission["candidate_only"] is True, f"{where}: candidate boundary")
        require(admission["strict_credit_granted"] is False, f"{where}: strict credit")
        require(
            admission["question_to_assertion_promotion_permitted"] is False,
            f"{where}: question promotion permitted",
        )
        require(
            admission["accept_only_complete_truth_apt_source_assertions"] is True
            and admission["accept_only_current_open_as_of"] == CUTOFF
            and admission["semantic_uniqueness_requires_later_cross_dedupe"] is True,
            f"{where}: admission gate drift",
        )
        rights = assert_keys(
            candidate["rights"],
            {
                "license_ref",
                "spdx_expression",
                "full_source_text_is_evidence_only_pending_release_compliance",
                "release_handling",
            },
            f"{where}/rights",
        )
        require(
            rights["license_ref"] == "LicenseRef-GNU-FDL-version-unspecified"
            and rights["spdx_expression"] == "NOASSERTION"
            and rights["full_source_text_is_evidence_only_pending_release_compliance"]
            is True,
            f"{where}: source rights boundary drift",
        )

        require(review["candidate_only"] is True, f"{where}: review candidate boundary")
        require(review["strict_credit_granted"] is False, f"{where}: review strict credit")
        require(
            review["release_mutation_authorized_or_performed"] is False,
            f"{where}: review release mutation",
        )
        require(
            review["question_to_assertion_promotion_performed"] is False,
            f"{where}: question promoted",
        )
        require(review["decision"] in INITIAL_DECISIONS, f"{where}: bad review decision")
        require(
            isinstance(review["reason_code"], str)
            and REASON_RE.fullmatch(review["reason_code"]) is not None,
            f"{where}: invalid reason code",
        )
        require(
            isinstance(review["review_basis"], str) and len(review["review_basis"]) >= 25,
            f"{where}: review basis too short",
        )
        require(
            review["source_form"]
            in {"declarative_assertion", "explicit_conjecture_component", "question_only", "other"},
            f"{where}: invalid source form",
        )
        require(review["importance_tier"] in {"high", "medium", "none"}, where)
        require(
            review["atomicity"] in {"single", "source_named_compound", "not_applicable"},
            f"{where}: invalid atomicity",
        )
        require(isinstance(review["duplicate_hints"], list), f"{where}: duplicate hints")

        claim = review["exact_claim_text"]
        claim_binding = commitments["exact_claim_binding"]
        if claim is None:
            require(claim_binding is None, f"{where}: unexpected exact-claim binding")
        else:
            require(isinstance(claim, str) and claim.strip(), f"{where}: invalid exact claim")
            binding = assert_exact_keys(
                claim_binding,
                {
                    "text_sha256",
                    "normalized_text_sha256",
                    "normalized_occurrences_in_problem_text",
                },
                f"{where}/exact_claim_binding",
            )
            require(
                binding["text_sha256"] == sha256_bytes(claim.encode("utf-8")),
                f"{where}: exact-claim text commitment mismatch",
            )
            require(
                binding["normalized_text_sha256"]
                == sha256_bytes(normalized_source_text(claim).encode("utf-8")),
                f"{where}: normalized exact-claim commitment mismatch",
            )
            require(
                is_int(binding["normalized_occurrences_in_problem_text"])
                and binding["normalized_occurrences_in_problem_text"] >= 1,
                f"{where}: exact claim is not committed inside problem text",
            )

        status = assert_exact_keys(
            review["current_status_evidence"],
            {
                "opg_listing_and_page",
                "discussion_passages",
                "independent_sources",
                "resolution_risk_review",
            },
            f"{where}/current_status_evidence",
        )
        passages = status["discussion_passages"]
        passage_bindings = commitments["discussion_passage_bindings"]
        require(
            isinstance(passages, list)
            and isinstance(passage_bindings, list)
            and len(passages) == len(passage_bindings),
            f"{where}: discussion-passage coverage mismatch",
        )
        for passage_index, (passage, binding_value) in enumerate(
            zip(passages, passage_bindings, strict=True), 1
        ):
            require(isinstance(passage, str) and passage.strip(), f"{where}: empty passage")
            binding = assert_exact_keys(
                binding_value,
                {
                    "passage_sha256",
                    "normalized_passage_sha256",
                    "normalized_occurrences_in_problem_text",
                    "normalized_occurrences_in_discussion_text",
                },
                f"{where}/passage_binding/{passage_index}",
            )
            require(
                binding["passage_sha256"] == sha256_bytes(passage.encode("utf-8")),
                f"{where}: passage commitment mismatch",
            )
            require(
                binding["normalized_passage_sha256"]
                == sha256_bytes(normalized_source_text(passage).encode("utf-8")),
                f"{where}: normalized passage commitment mismatch",
            )
            counts = (
                binding["normalized_occurrences_in_problem_text"],
                binding["normalized_occurrences_in_discussion_text"],
            )
            require(
                all(is_int(count) and count >= 0 for count in counts) and sum(counts) >= 1,
                f"{where}: passage is not committed to source text",
            )
        require(isinstance(status["independent_sources"], list), f"{where}: source URLs")
        for url in status["independent_sources"]:
            require_url(url, f"{where}: invalid independent status URL")

        if review["decision"] == "accept":
            require(
                review["importance_tier"] == importance["eligible_tier"],
                f"{where}: accepted tier drift",
            )
            require(
                review["source_form"] in {"declarative_assertion", "explicit_conjecture_component"},
                f"{where}: accepted non-assertion",
            )
            require(isinstance(claim, str) and "?" not in claim, f"{where}: question accepted")
            require(
                review["truth_apt"] is True
                and review["context_complete"] is True
                and review["source_asserted_open"] is True
                and review["full_discussion_reviewed"] is True
                and review["current_open_as_of_2026_08_10"] is True,
                f"{where}: accepted strict gate failed",
            )
            require(
                review["atomicity"] in {"single", "source_named_compound"},
                f"{where}: accepted atomicity failed",
            )
            summary = review["semantic_summary"]
            require(
                isinstance(summary, str) and len(summary) >= 15,
                f"{where}: accepted summary missing",
            )
            require(
                normalized_semantic(summary) != normalized_semantic(claim),
                f"{where}: release summary copies exact claim",
            )
            require(
                isinstance(status["opg_listing_and_page"], str)
                and len(status["opg_listing_and_page"]) >= 15
                and isinstance(status["resolution_risk_review"], str)
                and len(status["resolution_risk_review"]) >= 15
                and bool(passages or status["independent_sources"]),
                f"{where}: accepted current-open evidence insufficient",
            )

        queue[expected_index] = candidate
        reviews[expected_index] = review

    decisions = Counter(row["decision"] for row in review_rows)
    require(dict(decisions) == INITIAL_DECISIONS, "initial review decision counts drifted")
    accepted = {index for index, row in reviews.items() if row["decision"] == "accept"}
    require(len(accepted) == 140, "initial accepted denominator drifted")
    return queue, reviews, accepted


def validate_status_evidence(
    rows: list[dict[str, Any]], reviews: dict[int, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    expected: dict[str, list[dict[str, Any]]] = {}
    for index, review in reviews.items():
        for url in review["current_status_evidence"]["independent_sources"]:
            expected.setdefault(url, []).append(
                {
                    "candidate_index": index,
                    "candidate_key": review["candidate_key"],
                    "decision": review["decision"],
                }
            )
    for citations in expected.values():
        citations.sort(key=lambda item: item["candidate_index"])
    require(len(rows) == len(expected), "status URL coverage count drifted")
    evidence: dict[str, dict[str, Any]] = {}
    banned = {"body", "body_path", "sha256", "size_bytes"}
    required = {
        "schema_version",
        "original_capture_binding",
        "requested_url",
        "final_url",
        "status_code",
        "successful_status_evidence_transport",
        "observed_at",
        "content_type",
        "etag",
        "last_modified",
        "response_body_sha256",
        "response_body_size_bytes",
        "response_body_redistributed",
        "cited_by",
    }
    previous_url: str | None = None
    for row_number, row in enumerate(rows, 1):
        where = f"status-evidence:{row_number}"
        assert_exact_keys(row, required, where)
        require(not (banned & set(row)), f"{where}: raw response field present")
        require(
            row["schema_version"]
            == "awesome-theorems/openproblemgarden-portable-status-evidence/1",
            f"{where}: schema drift",
        )
        validate_capture_binding(
            row["original_capture_binding"],
            ORIGINAL_CAPTURE_SHA["status_evidence"],
            row_number,
            f"{where}/original_capture_binding",
        )
        url = require_url(row["requested_url"], f"{where}: invalid requested URL")
        require_url(row["final_url"], f"{where}: invalid final URL")
        require(url not in evidence, f"{where}: duplicate requested URL")
        require(previous_url is None or previous_url < url, f"{where}: URL order drift")
        previous_url = url
        require(
            is_int(row["status_code"]) and 100 <= row["status_code"] <= 599,
            f"{where}: invalid status code",
        )
        success = 200 <= row["status_code"] < 400
        require(
            row["successful_status_evidence_transport"] is success,
            f"{where}: transport-success flag drift",
        )
        require_sha(row["response_body_sha256"], f"{where}: body SHA malformed")
        require(
            row["response_body_redistributed"] is False,
            f"{where}: response body redistribution claimed",
        )
        require(
            is_int(row["response_body_size_bytes"])
            and row["response_body_size_bytes"] >= 0,
            f"{where}: body size malformed",
        )
        require(row["cited_by"] == expected.get(url), f"{where}: citation binding drift")
        evidence[url] = row
    require(set(evidence) == set(expected), "status URL coverage is incomplete")
    for url, row in evidence.items():
        if any(citation["decision"] == "accept" for citation in row["cited_by"]):
            require(
                row["successful_status_evidence_transport"] is True,
                f"accepted status citation transport failed: {url}",
            )
    return evidence


def validate_retrieval(
    rows: list[dict[str, Any]],
    queue: dict[int, dict[str, Any]],
    reviews: dict[int, dict[str, Any]],
    initially_accepted: set[int],
    namespaces: dict[str, set[str]],
    docs: dict[str, dict[str, dict[str, Any]]],
) -> dict[int, dict[str, Any]]:
    require(len(rows) == 140, "retrieval query count drifted")
    retrieval: dict[int, dict[str, Any]] = {}
    expected_lengths = {
        "parent_5_4": 12,
        "oeis_accepted": 12,
        "aimpl_accepted": 12,
        "open_logic_accepted": 4,
        "conjecturebench_full": 12,
        "opg_batch": 12,
    }
    accepted_queries = {
        f"opg/{index}": query_text(queue[index], reviews[index])
        for index in initially_accepted
    }
    namespaces["opg_batch"] = set(accepted_queries)
    docs["opg_batch"] = {
        doc_id: retrieval_document(
            doc_id, text, "same_review_batch", False, "openproblemgarden"
        )
        for doc_id, text in accepted_queries.items()
    }
    banned = {"query_text", "text_excerpt", "label"}
    for row_number, row in enumerate(rows, 1):
        where = f"retrieval:{row_number}"
        assert_exact_keys(
            row,
            {
                "schema_version",
                "candidate_index",
                "candidate_key",
                "query_sha256",
                "original_capture_binding",
                "retrieval_only_not_a_semantic_verdict",
                "top_matches",
            },
            where,
        )
        require(not (banned & set(row)), f"{where}: raw retrieval text present")
        require(
            row["schema_version"]
            == "awesome-theorems/openproblemgarden-portable-dedupe-retrieval/1",
            f"{where}: schema drift",
        )
        validate_capture_binding(
            row["original_capture_binding"],
            ORIGINAL_CAPTURE_SHA["cross_dedupe_retrieval"],
            row_number,
            f"{where}/original_capture_binding",
        )
        index = row["candidate_index"]
        require(index in initially_accepted and index not in retrieval, f"{where}: bad index")
        require(row["candidate_key"] == reviews[index]["candidate_key"], f"{where}: key")
        require(
            row["query_sha256"]
            == sha256_bytes(query_text(queue[index], reviews[index]).encode("utf-8")),
            f"{where}: query commitment drift",
        )
        require(
            row["retrieval_only_not_a_semantic_verdict"] is True,
            f"{where}: retrieval treated as verdict",
        )
        matches_by_corpus = assert_exact_keys(row["top_matches"], CORPORA, where + "/top")
        for corpus in DEDUPE_POLICY["credit_blocking_corpora"] + DEDUPE_POLICY[
            "evidence_only_corpora"
        ]:
            matches = matches_by_corpus[corpus]
            require(
                isinstance(matches, list) and len(matches) == expected_lengths[corpus],
                f"{where}/{corpus}: retrieval depth drift",
            )
            seen_ids: set[str] = set()
            for rank, match in enumerate(matches, 1):
                match_where = f"{where}/{corpus}/{rank}"
                assert_exact_keys(
                    match,
                    {
                        "id",
                        "retrieval_rank",
                        "score",
                        "source",
                        "material_status",
                        "preexisting_strict_or_accepted_candidate",
                        "label_sha256",
                        "text_excerpt_sha256",
                    },
                    match_where,
                )
                doc_id = match["id"]
                require(
                    isinstance(doc_id, str)
                    and doc_id in namespaces[corpus]
                    and doc_id not in seen_ids,
                    f"{match_where}: unresolved/duplicate ID",
                )
                require(
                    not (corpus == "opg_batch" and doc_id == f"opg/{index}"),
                    f"{match_where}: self retrieval",
                )
                seen_ids.add(doc_id)
                require(match["retrieval_rank"] == rank, f"{match_where}: rank drift")
                require(
                    isinstance(match["score"], (int, float))
                    and not isinstance(match["score"], bool)
                    and math.isfinite(match["score"])
                    and match["score"] >= 0,
                    f"{match_where}: invalid advisory score",
                )
                expected_doc = docs[corpus][doc_id]
                for field, expected_value in expected_doc.items():
                    require(
                        match[field] == expected_value,
                        f"{match_where}/{field}: authority projection mismatch",
                    )
        retrieval[index] = row
    require(set(retrieval) == initially_accepted, "retrieval coverage is not initial accepts")
    require(list(retrieval) == sorted(retrieval), "retrieval rows are not candidate-sorted")
    return retrieval


def validate_dedupe(
    rows: list[dict[str, Any]],
    retrieval: dict[int, dict[str, Any]],
    namespaces: dict[str, set[str]],
    parent_kinds: dict[str, str],
) -> dict[int, dict[str, Any]]:
    require(len(rows) == 140, "dedupe review count drifted")
    dedupe: dict[int, dict[str, Any]] = {}
    required = {
        "schema_version",
        "candidate_index",
        "candidate_key",
        "candidate_only",
        "strict_credit_granted",
        "release_mutation_authorized_or_performed",
        "retrieval_only_not_a_verdict",
        "corpus_reviews",
        "additional_search_terms",
        "within_opg_canonical_candidate_key",
        "semantic_unique_across_credit_blocking_inputs",
        "manual_verdict",
        "duplicate_targets",
        "evidence_only_duplicate_targets",
        "dedupe_basis",
    }
    opg_key_by_id = {
        f"opg/{index}": row["candidate_key"] for index, row in retrieval.items()
    }
    for row_number, row in enumerate(rows, 1):
        where = f"dedupe-review:{row_number}"
        assert_exact_keys(row, required, where)
        index = row["candidate_index"]
        require(index in retrieval and index not in dedupe, f"{where}: bad/duplicate index")
        source = retrieval[index]
        require(
            row["schema_version"]
            == "awesome-theorems/openproblemgarden-semantic-dedupe-review/2",
            f"{where}: schema is not dedupe /2",
        )
        require(row["candidate_key"] == source["candidate_key"], f"{where}: key binding")
        require(row["candidate_only"] is True, f"{where}: candidate boundary")
        require(row["strict_credit_granted"] is False, f"{where}: strict credit")
        require(
            row["release_mutation_authorized_or_performed"] is False,
            f"{where}: release mutation",
        )
        require(
            row["retrieval_only_not_a_verdict"] is True,
            f"{where}: retrieval treated as verdict",
        )
        corpus_reviews = assert_exact_keys(row["corpus_reviews"], CORPORA, where)
        blocking_targets: list[str] = []
        evidence_targets: list[str] = []
        supplemental: list[tuple[str, str]] = []
        for corpus in DEDUPE_POLICY["credit_blocking_corpora"] + DEDUPE_POLICY[
            "evidence_only_corpora"
        ]:
            audit = assert_exact_keys(
                corpus_reviews[corpus],
                {"reviewed_match_ids", "semantic_duplicate_targets", "notes"},
                f"{where}/{corpus}",
            )
            expected_ids = [match["id"] for match in source["top_matches"][corpus]]
            require(
                audit["reviewed_match_ids"] == expected_ids,
                f"{where}/{corpus}: not every retrieved ID was reviewed in order",
            )
            targets = audit["semantic_duplicate_targets"]
            require(
                isinstance(targets, list)
                and all(isinstance(target, str) for target in targets)
                and len(targets) == len(set(targets)),
                f"{where}/{corpus}: malformed semantic targets",
            )
            require(
                set(targets) <= namespaces[corpus],
                f"{where}/{corpus}: target outside fixed authority",
            )
            require(
                isinstance(audit["notes"], str) and len(audit["notes"]) >= 10,
                f"{where}/{corpus}: notes too short",
            )
            supplemental.extend(
                (corpus, target) for target in targets if target not in expected_ids
            )
            if corpus in EVIDENCE_ONLY_CORPORA:
                evidence_targets.extend(targets)
            else:
                blocking_targets.extend(targets)

        terms = row["additional_search_terms"]
        require(
            isinstance(terms, list)
            and all(isinstance(term, str) and term.strip() for term in terms),
            f"{where}: malformed additional search terms",
        )
        if supplemental:
            require(bool(terms), f"{where}: supplemental targets without search terms")
            for corpus, target in supplemental:
                require(
                    target in corpus_reviews[corpus]["notes"] or target in row["dedupe_basis"],
                    f"{where}/{corpus}: supplemental target is not explained",
                )
        require(row["manual_verdict"] in VERDICTS, f"{where}: invalid verdict")
        require(
            isinstance(row["duplicate_targets"], list)
            and len(row["duplicate_targets"]) == len(set(row["duplicate_targets"]))
            and sorted(row["duplicate_targets"]) == sorted(blocking_targets),
            f"{where}: credit-blocking targets drift",
        )
        require(
            isinstance(row["evidence_only_duplicate_targets"], list)
            and len(row["evidence_only_duplicate_targets"])
            == len(set(row["evidence_only_duplicate_targets"]))
            and sorted(row["evidence_only_duplicate_targets"])
            == sorted(evidence_targets),
            f"{where}: evidence-only targets drift",
        )
        require(
            isinstance(row["dedupe_basis"], str) and len(row["dedupe_basis"]) >= 30,
            f"{where}: dedupe basis too short",
        )
        open_parent_targets = [
            target
            for target in corpus_reviews["parent_5_4"]["semantic_duplicate_targets"]
            if parent_kinds[target] == "open_problem"
        ]
        if open_parent_targets:
            explanation = (
                corpus_reviews["parent_5_4"]["notes"] + " " + row["dedupe_basis"]
            )
            require(
                "duplicate_fixed_parent_open_target" in explanation,
                f"{where}: fixed-parent open-target policy marker missing",
            )

        unique = row["semantic_unique_across_credit_blocking_inputs"]
        require(isinstance(unique, bool), f"{where}: semantic-unique flag malformed")
        verdict = row["manual_verdict"]
        canonical_key = row["within_opg_canonical_candidate_key"]
        if unique:
            require(canonical_key == row["candidate_key"], f"{where}: canonical key drift")
            if verdict == "unique":
                require(not blocking_targets, f"{where}: unique verdict has blocker")
            else:
                require(verdict == "canonical_opg", f"{where}: unique verdict mismatch")
                require(
                    bool(corpus_reviews["opg_batch"]["semantic_duplicate_targets"]),
                    f"{where}: canonical OPG row has no siblings",
                )
                require(
                    not any(
                        corpus_reviews[corpus]["semantic_duplicate_targets"]
                        for corpus in BLOCKING_CORPORA - {"opg_batch"}
                    ),
                    f"{where}: canonical OPG row has external blocker",
                )
        else:
            require(
                verdict in VERDICT_CORPUS and bool(blocking_targets),
                f"{where}: nonunique row lacks blocking verdict/target",
            )
            verdict_corpus = VERDICT_CORPUS[verdict]
            require(
                bool(corpus_reviews[verdict_corpus]["semantic_duplicate_targets"]),
                f"{where}: verdict has no target in its corpus",
            )
            if verdict == "duplicate_opg":
                require(
                    canonical_key
                    in {
                        opg_key_by_id[target]
                        for target in corpus_reviews["opg_batch"][
                            "semantic_duplicate_targets"
                        ]
                    },
                    f"{where}: OPG canonical key does not resolve to a target",
                )
            else:
                require(canonical_key == row["candidate_key"], f"{where}: external canonical")
        dedupe[index] = row

    require(set(dedupe) == set(retrieval), "dedupe does not cover all 140 retrieval rows")
    require(list(dedupe) == sorted(dedupe), "dedupe rows are not candidate-sorted")
    by_key = {row["candidate_key"]: row for row in rows}
    require(len(by_key) == len(rows), "dedupe candidate keys are not unique")

    adjacency: dict[str, set[str]] = {key: set() for key in by_key}
    for row in rows:
        key = row["candidate_key"]
        for target in row["corpus_reviews"]["opg_batch"]["semantic_duplicate_targets"]:
            other_key = opg_key_by_id[target]
            require(other_key != key, f"dedupe {key}: self OPG duplicate")
            adjacency[key].add(other_key)
            require(
                f"opg/{row['candidate_index']}"
                in by_key[other_key]["corpus_reviews"]["opg_batch"][
                    "semantic_duplicate_targets"
                ],
                f"dedupe {key}<->{other_key}: OPG relation is not reciprocal",
            )

    unseen = set(by_key)
    while unseen:
        seed = next(iter(unseen))
        stack = [seed]
        component: set[str] = set()
        while stack:
            key = stack.pop()
            if key in component:
                continue
            component.add(key)
            stack.extend(adjacency[key] - component)
        unseen -= component
        if len(component) == 1 and not adjacency[seed]:
            require(
                by_key[seed]["within_opg_canonical_candidate_key"] == seed,
                f"dedupe {seed}: singleton points outside itself",
            )
            continue
        roots = {
            by_key[key]["within_opg_canonical_candidate_key"] for key in component
        }
        require(len(roots) == 1, f"OPG class {sorted(component)} has multiple canonicals")
        root = next(iter(roots))
        require(root in component, f"OPG class {sorted(component)} canonical is outside class")
        require(
            by_key[root]["within_opg_canonical_candidate_key"] == root,
            f"OPG class {root}: canonical is not self-canonical",
        )
        require(
            adjacency[root] == component - {root},
            f"OPG class {root}: canonical does not enumerate the full class",
        )
        require(
            by_key[root]["manual_verdict"]
            in {
                "canonical_opg",
                "duplicate_parent",
                "duplicate_oeis",
                "duplicate_aimpl",
                "duplicate_open_logic",
            },
            f"OPG class {root}: invalid canonical verdict",
        )
        for key in component - {root}:
            require(
                by_key[key]["manual_verdict"] == "duplicate_opg"
                and by_key[key]["semantic_unique_across_credit_blocking_inputs"] is False
                and root in adjacency[key],
                f"OPG class {root}: invalid noncanonical member {key}",
            )
    return dedupe


def validate_ledger(
    rows: list[dict[str, Any]],
    payloads: list[bytes],
    queue: dict[int, dict[str, Any]],
    reviews: dict[int, dict[str, Any]],
    dedupe: dict[int, dict[str, Any]],
    evidence: dict[str, dict[str, Any]],
    paths: dict[str, Path],
    queue_payloads: list[bytes],
    review_payloads: list[bytes],
    dedupe_payloads: list[bytes],
    authority_set_sha: str,
    dedupe_scope_sha: str,
) -> tuple[Counter[str], Counter[str], int]:
    require(len(rows) == len(payloads) == 404, "eligibility ledger is not 404 rows")
    dedupe_row_number = {
        row["candidate_index"]: number for number, row in enumerate(dedupe.values(), 1)
    }
    dedupe_payload_by_index = {
        row["candidate_index"]: payload
        for row, payload in zip(dedupe.values(), dedupe_payloads, strict=True)
    }
    decisions: Counter[str] = Counter()
    tiers: Counter[str] = Counter()
    accepted_rank = 0
    semantic_keys: set[str] = set()
    ledger_keys: set[str] = set()
    required = {
        "schema_version",
        "candidate_index",
        "candidate_key",
        "source_kind",
        "source_record_key",
        "source_artifact",
        "review_artifact",
        "dedupe_artifact",
        "decision",
        "reason_code",
        "decision_basis",
        "accepted_rank",
        "exact_claim_text",
        "exact_claim_context",
        "source_wording_usage",
        "semantic_summary",
        "semantic_key",
        "importance_tier",
        "current_open_as_of",
        "current_open_evidence",
        "truth_apt",
        "context_complete",
        "question_to_assertion_promotion_performed",
        "atomicity",
        "global_dedupe",
        "rights",
        "attribution",
        "candidate_only",
        "formal_acceptance_eligible_for_5_5",
        "grants_catalog_entry",
        "grants_strict_conjecture_credit",
        "release_mutation_authorized_or_performed",
        "row_sha256",
    }
    for expected_index, (row, raw_payload) in enumerate(
        zip(rows, payloads, strict=True), 1
    ):
        where = f"eligibility-ledger:{expected_index}"
        assert_exact_keys(row, required, where)
        require(
            row["schema_version"] == "awesome-theorems/openproblemgarden-eligibility/1",
            f"{where}: schema drift",
        )
        require(row["candidate_index"] == expected_index, f"{where}: index/order drift")
        unsealed = {key: value for key, value in row.items() if key != "row_sha256"}
        require(
            row["row_sha256"] == sha256_bytes(canonical(unsealed)),
            f"{where}: stale row seal",
        )
        require(raw_payload == canonical(row), f"{where}: raw row differs from sealed object")
        candidate = queue[expected_index]
        review = reviews[expected_index]
        dedupe_row = dedupe.get(expected_index)
        key = candidate["candidate_key"]
        require(
            row["candidate_key"] == review["candidate_key"] == key
            and key not in ledger_keys,
            f"{where}: candidate key binding/uniqueness",
        )
        ledger_keys.add(key)
        require(row["source_kind"] == "open_problem_garden", f"{where}: source kind")
        require(
            row["source_record_key"] == review["source_record_key"]
            == candidate["source_record_key"],
            f"{where}: source-record binding",
        )
        expected_source_binding = binding_for_row(
            LOCAL_NAMES["review_queue"],
            paths["review_queue"],
            expected_index,
            queue_payloads[expected_index - 1],
            candidate,
        )
        validate_row_binding(
            row["source_artifact"], expected_source_binding, where + "/source_artifact", allow_extra=True
        )
        source_artifact = row["source_artifact"]
        require(
            source_artifact.get("snapshot_url") == candidate["source"]["url"]
            and source_artifact.get("snapshot_sha256")
            == candidate["source"]["snapshot_sha256"]
            and source_artifact.get("problem_div_html_sha256")
            == candidate["exact_source_commitments"]["problem_div_html_sha256"],
            f"{where}: source commitment binding drift",
        )
        expected_review_binding = binding_for_row(
            LOCAL_NAMES["review"],
            paths["review"],
            expected_index,
            review_payloads[expected_index - 1],
            review,
        )
        validate_row_binding(
            row["review_artifact"], expected_review_binding, where + "/review_artifact"
        )
        if dedupe_row is None:
            require(row["dedupe_artifact"] is None, f"{where}: unexpected dedupe binding")
        else:
            number = dedupe_row_number[expected_index]
            expected_dedupe_binding = binding_for_row(
                LOCAL_NAMES["dedupe_review"],
                paths["dedupe_review"],
                number,
                dedupe_payload_by_index[expected_index],
                dedupe_row,
            )
            validate_row_binding(
                row["dedupe_artifact"], expected_dedupe_binding, where + "/dedupe_artifact"
            )

        initial_decision = review["decision"]
        if initial_decision == "accept":
            require(dedupe_row is not None, f"{where}: accepted review lacks dedupe")
            semantic_unique = dedupe_row[
                "semantic_unique_across_credit_blocking_inputs"
            ]
            expected_decision = "accept" if semantic_unique else "reject"
        else:
            require(dedupe_row is None, f"{where}: nonaccept was sent to dedupe")
            expected_decision = initial_decision
        require(row["decision"] == expected_decision, f"{where}: final decision replay drift")
        require(
            not (initial_decision == "pending" and expected_decision != "pending"),
            f"{where}: pending review was promoted",
        )
        decisions[expected_decision] += 1
        require(
            row["candidate_only"] is True
            and row["grants_catalog_entry"] is False
            and row["grants_strict_conjecture_credit"] is False
            and row["release_mutation_authorized_or_performed"] is False,
            f"{where}: candidate-only boundary crossed",
        )
        require(
            row["question_to_assertion_promotion_performed"] is False
            and row["question_to_assertion_promotion_performed"]
            == review["question_to_assertion_promotion_performed"],
            f"{where}: question promotion drift",
        )

        global_dedupe = assert_keys(
            row["global_dedupe"],
            {
                "verdict",
                "semantic_unique",
                "relation",
                "duplicate_targets",
                "blocking_duplicate_targets",
                "evidence_only_duplicate_targets",
                "within_opg_canonical_candidate_key",
                "scope",
                "dedupe_scope_sha256",
                "authority_set_sha256",
            },
            where + "/global_dedupe",
        )
        require(
            global_dedupe["authority_set_sha256"] == authority_set_sha
            and global_dedupe["dedupe_scope_sha256"] == dedupe_scope_sha
            and global_dedupe["scope"] == "credit_blocking_authorities_v2",
            f"{where}: global dedupe authority/scope drift",
        )
        if dedupe_row:
            blocking = dedupe_row["duplicate_targets"]
            evidence_only = dedupe_row["evidence_only_duplicate_targets"]
            require(
                global_dedupe["verdict"] == dedupe_row["manual_verdict"]
                and global_dedupe["semantic_unique"]
                == dedupe_row["semantic_unique_across_credit_blocking_inputs"]
                and global_dedupe["duplicate_targets"] == blocking
                and global_dedupe["blocking_duplicate_targets"] == blocking
                and global_dedupe["evidence_only_duplicate_targets"] == evidence_only
                and global_dedupe["within_opg_canonical_candidate_key"]
                == dedupe_row["within_opg_canonical_candidate_key"],
                f"{where}: dedupe payload does not replay /2 review",
            )
            relation = global_dedupe["relation"]
            require(isinstance(relation, str) and relation, f"{where}: dedupe relation")
            if (
                evidence_only
                and global_dedupe["semantic_unique"]
                and dedupe_row["manual_verdict"] == "unique"
            ):
                require(
                    (
                        "evidence_only" in relation
                        or relation
                        == "semantically_distinct_from_all_credit_blocking_authorities"
                    )
                    and relation != "semantically_distinct_from_all_fixed_authorities",
                    f"{where}: evidence-only CB relation was mislabeled as globally distinct",
                )
            open_parent_targets = [
                target
                for target in dedupe_row["corpus_reviews"]["parent_5_4"][
                    "semantic_duplicate_targets"
                ]
                if target
                and "duplicate_fixed_parent_open_target"
                in (
                    dedupe_row["corpus_reviews"]["parent_5_4"]["notes"]
                    + " "
                    + dedupe_row["dedupe_basis"]
                )
            ]
            if open_parent_targets:
                require(
                    row["reason_code"] == "duplicate_fixed_parent_open_target",
                    f"{where}: fixed-parent open-target reason code missing",
                )
        else:
            require(
                global_dedupe["verdict"] == "not_applicable_review_not_accepted"
                and global_dedupe["semantic_unique"] is False
                and global_dedupe["relation"] == "not_sent_to_global_dedupe"
                and global_dedupe["duplicate_targets"] == []
                and global_dedupe["blocking_duplicate_targets"] == []
                and global_dedupe["evidence_only_duplicate_targets"] == []
                and global_dedupe["within_opg_canonical_candidate_key"] is None,
                f"{where}: non-dedupe payload drift",
            )

        rights = assert_keys(
            row["rights"],
            {
                "license_ref",
                "spdx_expression",
                "release_rights_gate",
                "exact_source_wording_excluded_from_release",
                "raw_source_bodies_not_redistributed_in_repo_curation",
            },
            where + "/rights",
        )
        for field, value in candidate["rights"].items():
            require(rights.get(field) == value, f"{where}/rights/{field}: source rights drift")
        require(
            rights["license_ref"] == "LicenseRef-GNU-FDL-version-unspecified"
            and rights["spdx_expression"] == "NOASSERTION"
            and rights["exact_source_wording_excluded_from_release"] is True
            and rights["raw_source_bodies_not_redistributed_in_repo_curation"] is True,
            f"{where}: rights boundary failed",
        )
        attribution = assert_keys(
            row["attribution"],
            {"collection", "title", "url", "authors_as_displayed", "posted_by"},
            where + "/attribution",
        )
        require(
            attribution["collection"] == "Open Problem Garden"
            and attribution["title"] == candidate["source"]["title"]
            and attribution["url"] == candidate["source"]["url"]
            and attribution["authors_as_displayed"] == candidate["context"]["authors"]
            and attribution["posted_by"] == candidate["context"]["posted_by"],
            f"{where}: attribution drift",
        )

        if expected_decision == "accept":
            accepted_rank += 1
            require(row["accepted_rank"] == accepted_rank, f"{where}: accepted rank drift")
            require(
                row["formal_acceptance_eligible_for_5_5"] is True,
                f"{where}: accepted eligibility false",
            )
            require(
                row["reason_code"] == "strict_gates_and_global_semantic_uniqueness_pass",
                f"{where}: accepted reason code drift",
            )
            require(
                row["decision_basis"]
                == review["review_basis"]
                + " Global credit-blocking proposition-level review: "
                + dedupe_row["dedupe_basis"],
                f"{where}: accepted decision basis drift",
            )
            require(
                row["exact_claim_text"] == review["exact_claim_text"]
                and row["exact_claim_context"] == review["exact_claim_context"]
                and isinstance(row["exact_claim_text"], str)
                and "?" not in row["exact_claim_text"],
                f"{where}: accepted exact claim drift/question",
            )
            require(
                row["source_wording_usage"] == "evidence_only_not_release_payload",
                f"{where}: source wording leaked to release payload",
            )
            require(row["semantic_summary"] == review["semantic_summary"], where)
            expected_semantic_key = semantic_key(row["semantic_summary"])
            require(row["semantic_key"] == expected_semantic_key, f"{where}: semantic key")
            require(
                expected_semantic_key not in semantic_keys,
                f"{where}: duplicate accepted semantic key",
            )
            semantic_keys.add(expected_semantic_key)
            require(
                row["importance_tier"] == review["importance_tier"]
                and row["importance_tier"] in {"high", "medium"},
                f"{where}: accepted tier drift",
            )
            tiers[row["importance_tier"]] += 1
            require(row["current_open_as_of"] == CUTOFF, f"{where}: open cutoff")
            require(
                row["current_open_evidence"] == review["current_status_evidence"],
                f"{where}: status evidence drift",
            )
            for url in row["current_open_evidence"]["independent_sources"]:
                require(
                    url in evidence
                    and evidence[url]["successful_status_evidence_transport"] is True,
                    f"{where}: accepted status URL lacks successful transport",
                )
            require(
                row["truth_apt"] is True
                and row["context_complete"] is True
                and row["atomicity"] in {"single", "source_named_compound"},
                f"{where}: accepted statement gate drift",
            )
            require(
                rights["release_rights_gate"]
                == "pass_independent_summary_pointer_attribution_only",
                f"{where}: accepted rights gate drift",
            )
        else:
            require(row["accepted_rank"] is None, f"{where}: nonaccept rank")
            require(
                row["formal_acceptance_eligible_for_5_5"] is False,
                f"{where}: nonaccept formally eligible",
            )
            require(
                row["exact_claim_text"] is None
                and row["exact_claim_context"] is None
                and row["semantic_summary"] is None
                and row["semantic_key"] is None
                and row["importance_tier"] == "none"
                and row["current_open_as_of"] is None
                and row["current_open_evidence"] is None
                and row["atomicity"] == "not_applicable",
                f"{where}: nonaccept retained release payload",
            )
            require(
                row["source_wording_usage"] == "not_in_eligibility_payload"
                and rights["release_rights_gate"] == "not_applicable",
                f"{where}: nonaccept release boundary drift",
            )
            require(
                row["truth_apt"] == review["truth_apt"]
                and row["context_complete"] == review["context_complete"],
                f"{where}: nonaccept review gate drift",
            )
            if initial_decision == "accept":
                expected_reason = {
                    "duplicate_parent": (
                        "duplicate_fixed_parent_open_target"
                        if any(
                            target
                            for target in dedupe_row["corpus_reviews"]["parent_5_4"][
                                "semantic_duplicate_targets"
                            ]
                            if "duplicate_fixed_parent_open_target"
                            in (
                                dedupe_row["corpus_reviews"]["parent_5_4"]["notes"]
                                + " "
                                + dedupe_row["dedupe_basis"]
                            )
                        )
                        else "duplicate_fixed_parent_authority"
                    ),
                    "duplicate_oeis": "duplicate_fixed_oeis_authority",
                    "duplicate_aimpl": "duplicate_fixed_aimpl_authority",
                    "duplicate_open_logic": "duplicate_fixed_open_logic_authority",
                    "duplicate_opg": "duplicate_within_openproblemgarden",
                }[dedupe_row["manual_verdict"]]
                require(row["reason_code"] == expected_reason, f"{where}: duplicate reason")
                require(
                    row["decision_basis"] == dedupe_row["dedupe_basis"],
                    f"{where}: duplicate decision basis drift",
                )
            else:
                require(
                    row["reason_code"] == review["reason_code"]
                    and row["decision_basis"] == review["review_basis"],
                    f"{where}: preserved decision payload drift",
                )
    require(accepted_rank == decisions["accept"], "accepted rank count drift")
    return decisions, tiers, accepted_rank


def validate_receipt(
    receipt: dict[str, Any],
    paths: dict[str, Path],
    row_counts: dict[str, int],
    authority_set: dict[str, dict[str, Any]],
    authority_set_sha: str,
    dedupe_scope_sha: str,
    decisions: Counter[str],
    tiers: Counter[str],
    dedupe: dict[int, dict[str, Any]],
) -> None:
    required = {
        "schema_version",
        "cutoff",
        "target_minimum",
        "target_met",
        "release_5_5_required_opg_minimum",
        "release_5_5_other_source_admissions",
        "release_5_5_total_minimum",
        "release_5_5_total_candidate_admissions",
        "candidate_only",
        "formal_additions",
        "strict_credits_granted",
        "release_mutation_authorized_or_performed",
        "raw_source_bodies_redistributed",
        "raw_source_bodies_not_redistributed_in_repo_curation",
        "authority_set",
        "authority_set_sha256",
        "dedupe_scope_sha256",
        "inputs",
        "output",
        "counts",
        "checks",
        "authority_sha256",
    }
    assert_keys(receipt, required, "receipt")
    require(
        receipt["schema_version"]
        == "awesome-theorems/openproblemgarden-eligibility-receipt/1",
        "receipt: schema drift",
    )
    validate_self_seal(receipt, "receipt")
    require(receipt["cutoff"] == CUTOFF, "receipt: cutoff drift")
    require(receipt["target_minimum"] == RELEASE_OPG_MINIMUM, "receipt: target drift")
    accepted = decisions["accept"]
    expected_target = (
        accepted >= RELEASE_OPG_MINIMUM
        and RELEASE_OTHER_SOURCE_ADMISSIONS + accepted >= RELEASE_TOTAL_MINIMUM
    )
    require(receipt["target_met"] is expected_target, "receipt: target flag drift")
    require(expected_target, "release 5.5 OPG minimum was not met")
    require(
        receipt["release_5_5_required_opg_minimum"] == RELEASE_OPG_MINIMUM
        and receipt["release_5_5_other_source_admissions"]
        == RELEASE_OTHER_SOURCE_ADMISSIONS
        and receipt["release_5_5_total_minimum"] == RELEASE_TOTAL_MINIMUM
        and receipt["release_5_5_total_candidate_admissions"]
        == RELEASE_OTHER_SOURCE_ADMISSIONS + accepted,
        "receipt: release candidate-admission arithmetic drift",
    )
    require(
        receipt["candidate_only"] is True
        and receipt["formal_additions"] == 0
        and receipt["strict_credits_granted"] == 0
        and receipt["release_mutation_authorized_or_performed"] is False
        and receipt["raw_source_bodies_redistributed"] is False,
        "receipt: candidate/credit/release boundary crossed",
    )
    require(
        receipt["raw_source_bodies_not_redistributed_in_repo_curation"] is True,
        "receipt: raw-source nonredistribution boundary drift",
    )
    require(receipt["authority_set"] == authority_set, "receipt: authority set drift")
    require(
        receipt["authority_set_sha256"] == authority_set_sha,
        "receipt: authority-set digest drift",
    )
    require(
        receipt["dedupe_scope_sha256"] == dedupe_scope_sha,
        "receipt: dedupe-scope digest drift",
    )
    inputs = assert_exact_keys(
        receipt["inputs"],
        {
            "manifest",
            "review_queue",
            "review",
            "status_evidence",
            "cross_dedupe_retrieval",
            "dedupe_review",
        },
        "receipt/inputs",
    )
    for logical_name in inputs:
        require(
            inputs[logical_name]
            == artifact_binding(
                LOCAL_NAMES[logical_name], paths[logical_name], row_counts[logical_name]
            ),
            f"receipt/inputs/{logical_name}: stale binding",
        )
    require(
        receipt["output"]
        == artifact_binding(LOCAL_NAMES["ledger"], paths["ledger"], 404),
        "receipt: output binding drift",
    )
    counts = assert_exact_keys(
        receipt["counts"],
        {
            "reviewed_candidates",
            "initial_review_decisions",
            "decisions",
            "accepted_tiers",
            "dedupe",
        },
        "receipt/counts",
    )
    require(counts["reviewed_candidates"] == 404, "receipt: reviewed count")
    require(
        counts["initial_review_decisions"] == INITIAL_DECISIONS,
        "receipt: initial review counts drift",
    )
    require(counts["decisions"] == dict(sorted(decisions.items())), "receipt: decisions")
    require(counts["accepted_tiers"] == dict(sorted(tiers.items())), "receipt: tiers")
    dedupe_counts = {
        "reviewed": len(dedupe),
        "semantic_unique": sum(
            row["semantic_unique_across_credit_blocking_inputs"] for row in dedupe.values()
        ),
        "blocked": sum(
            not row["semantic_unique_across_credit_blocking_inputs"]
            for row in dedupe.values()
        ),
        "evidence_only_relations": sum(
            len(row["evidence_only_duplicate_targets"]) for row in dedupe.values()
        ),
        "evidence_only_rows": sum(
            bool(row["evidence_only_duplicate_targets"]) for row in dedupe.values()
        ),
    }
    require(counts["dedupe"] == dedupe_counts, "receipt: dedupe counts drift")
    checks = receipt["checks"]
    require(
        isinstance(checks, dict)
        and bool(checks)
        and all(value is True for value in checks.values()),
        "receipt: one or more declared checks are not true",
    )


def write_report(
    paths: dict[str, Path],
    authority_set_sha: str,
    dedupe_scope_sha: str,
    decisions: Counter[str],
    tiers: Counter[str],
) -> Path:
    report_path = HERE / "eligibility-validation.json"
    report: dict[str, Any] = {
        "schema_version": "awesome-theorems/openproblemgarden-eligibility-validation/1",
        "overall_pass": True,
        "validator": {
            "path": relative_path("validate.py"),
            "sha256": sha256_file(Path(__file__).resolve()),
            "size_bytes": Path(__file__).resolve().stat().st_size,
        },
        "ledger": artifact_binding(LOCAL_NAMES["ledger"], paths["ledger"], 404),
        "receipt": artifact_binding(LOCAL_NAMES["receipt"], paths["receipt"], 1),
        "authority_set_sha256": authority_set_sha,
        "dedupe_scope_sha256": dedupe_scope_sha,
        "counts": {
            "rows": 404,
            "decisions": dict(sorted(decisions.items())),
            "accepted_tiers": dict(sorted(tiers.items())),
        },
        "target_met": decisions["accept"] >= RELEASE_OPG_MINIMUM,
        "formal_additions": 0,
        "strict_credits_granted": 0,
        "checks": {
            "canonical_repository_local_authorities": True,
            "source_review_status_and_dedupe_replayed": True,
            "all_hashes_bindings_and_seals_replayed": True,
            "candidate_only_no_credit_or_release_mutation": True,
        },
    }
    report["authority_sha256"] = sha256_bytes(canonical(report))
    validate_no_host_paths(report, "eligibility-validation")
    temporary = HERE / ".eligibility-validation.json.new"
    temporary.write_bytes(canonical_line(report))
    os.replace(temporary, report_path)
    return report_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="write the optional canonical, self-sealed eligibility-validation.json",
    )
    args = parser.parse_args(argv)
    require(
        HERE == REPO.joinpath(*CURATION_REL.parts).resolve(),
        "validator is not located at its repository-authoritative path",
    )
    paths = {key: HERE / name for key, name in LOCAL_NAMES.items()}
    for key, path in paths.items():
        require(path.is_file(), f"missing local OPG artifact {key}: {path.name}")

    manifest = load_canonical_json(paths["manifest"])
    receipt = load_canonical_json(paths["receipt"])
    queue_rows, queue_payloads = load_canonical_jsonl(paths["review_queue"])
    review_rows, review_payloads = load_canonical_jsonl(paths["review"])
    status_rows, _ = load_canonical_jsonl(paths["status_evidence"])
    retrieval_rows, _ = load_canonical_jsonl(paths["cross_dedupe_retrieval"])
    dedupe_rows, dedupe_payloads = load_canonical_jsonl(paths["dedupe_review"])
    ledger_rows, ledger_payloads = load_canonical_jsonl(paths["ledger"])
    row_counts = {
        "manifest": 1,
        "review_queue": len(queue_rows),
        "review": len(review_rows),
        "status_evidence": len(status_rows),
        "cross_dedupe_retrieval": len(retrieval_rows),
        "dedupe_review": len(dedupe_rows),
        "ledger": len(ledger_rows),
        "receipt": 1,
    }

    authority_set, namespaces, docs, parent_kinds = load_authorities()
    authority_set_sha, dedupe_scope_sha = validate_manifest(
        manifest, paths, row_counts, authority_set
    )
    queue, reviews, initially_accepted = validate_queue_and_reviews(
        queue_rows, review_rows
    )
    evidence = validate_status_evidence(status_rows, reviews)
    retrieval = validate_retrieval(
        retrieval_rows,
        queue,
        reviews,
        initially_accepted,
        namespaces,
        docs,
    )
    dedupe = validate_dedupe(dedupe_rows, retrieval, namespaces, parent_kinds)
    decisions, tiers, _ = validate_ledger(
        ledger_rows,
        ledger_payloads,
        queue,
        reviews,
        dedupe,
        evidence,
        paths,
        queue_payloads,
        review_payloads,
        dedupe_payloads,
        authority_set_sha,
        dedupe_scope_sha,
    )
    validate_receipt(
        receipt,
        paths,
        row_counts,
        authority_set,
        authority_set_sha,
        dedupe_scope_sha,
        decisions,
        tiers,
        dedupe,
    )
    report = write_report(paths, authority_set_sha, dedupe_scope_sha, decisions, tiers) \
        if args.write_report else None
    result = {
        "overall_pass": True,
        "rows": 404,
        "decisions": dict(sorted(decisions.items())),
        "accepted_tiers": dict(sorted(tiers.items())),
        "target_met": decisions["accept"] >= RELEASE_OPG_MINIMUM,
        "ledger_sha256": sha256_file(paths["ledger"]),
        "receipt_sha256": sha256_file(paths["receipt"]),
    }
    if report is not None:
        result["report"] = str(CURATION_REL / report.name)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationError, OSError) as exc:
        print(f"OPG eligibility validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
