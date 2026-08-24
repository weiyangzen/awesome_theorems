#!/usr/bin/env python3
"""Build the release-5.5 strict-conjecture admission ledger.

The input reviews remain candidate-only.  This builder is the explicit
transition from those reviews to a release admission decision.  It accepts
only the final OEIS survivor set, accepted AimPL and Open Logic reviews, and
the globally deduplicated Open Problem Garden eligibility set.  Every output
row points at one exact reviewed JSONL row and the complete upstream review
universes are bound separately in ``coverage_bindings``.

The script is deterministic and standard-library-only.  Without ``--write``
it compares the checked result with the existing output and never mutates the
repository.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from typing import Any, Iterable, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[4]
V5_ROOT = REPO_ROOT / "Docs/catalog/v5"
OUTPUT = V5_ROOT / "curation/Strict_Conjecture_Curation_v5_5.json"
PARENT_CATALOG = V5_ROOT / "releases/5.4/Claim_Catalog.json"
PARENT_STRICT = V5_ROOT / "releases/5.4/Strict_Conjecture_Ledger.json"

OEIS_ROOT = V5_ROOT / "curation/oeis_v5_5"
OEIS_RECEIPT = OEIS_ROOT / "audit-receipt.json"
OEIS_SURVIVORS = OEIS_ROOT / "combined-survivors.jsonl"
OEIS_SOURCE_RECEIPT = V5_ROOT / "sources/oeis-conjectures-4c866362-receipt.json"
OEIS_REVIEWS = tuple(
    [OEIS_ROOT / f"v1/reviews/review-{index:02d}.jsonl" for index in range(8)]
    + [OEIS_ROOT / f"v2/reviews/review-v2-{index:02d}.jsonl" for index in range(8)]
)

AIMPL_ROOT = V5_ROOT / "curation/aimpl_v5_5"
AIMPL_RECEIPT = AIMPL_ROOT / "audit-receipt.json"
AIMPL_REVIEW = AIMPL_ROOT / "review-ledger.jsonl"
AIMPL_CANDIDATES = V5_ROOT / "sources/aimpl/candidates.jsonl"

OPEN_LOGIC_ROOT = V5_ROOT / "curation/open_logic_v5_5"
OPEN_LOGIC_RECEIPT = OPEN_LOGIC_ROOT / "open-logic-review.count.json"
OPEN_LOGIC_REVIEW = OPEN_LOGIC_ROOT / "open-logic-review.jsonl"

OPG_ROOT = V5_ROOT / "curation/openproblemgarden_v5_5"
OPG_RECEIPT = OPG_ROOT / "eligibility-receipt.json"
OPG_REVIEW = OPG_ROOT / "eligibility-ledger.jsonl"

PARENT_RELEASE_ROOT = "c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813"
PARENT_CATALOG_SHA256 = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
PARENT_STRICT_SHA256 = "52ba1ccf06462741bcc48028fb121e5e30d1e7b56128cfeb910dc56a2e1a83a3"

# These three completed audits are immutable inputs.  OPG is pinned through
# its sealed receipt because that receipt is produced only after global
# proposition-level deduplication and may not exist while this script is
# being reviewed.
OEIS_RECEIPT_SHA256 = "6a05b9ca89540e3e51b42869410fa1e3607a88f9c7a7c14e4ae0125ae1043f20"
OEIS_SURVIVORS_SHA256 = "d9928d3d61a05e618df7a044c98d966b6f4d8fe63925ea4e95bb2cd5e4de4e5a"
AIMPL_RECEIPT_SHA256 = "01acc230256829ed50010731dd419e17c4b630f4f64651c09600debede741a83"
AIMPL_REVIEW_SHA256 = "8f6c129a07c948b1712d9ce855fb25c69329b42e12a2148597dab8bcaad9343b"
OPEN_LOGIC_RECEIPT_SHA256 = "08f2f925bddf8fd0e4042d90e1687f9a976a2d91ca75af139bc32cb0aaacc27e"
OPEN_LOGIC_REVIEW_SHA256 = "65fe1f6cafd939ab9604d860838b56488f32d321230ce759cf2b243724d4f1a2"

MIN_ACCEPTED = 401
MAX_ACCEPTED = 1_000
REVIEW_DATE = "2026-08-10"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


class BuildError(RuntimeError):
    """A frozen input or admission invariant failed closed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


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
        raise BuildError(f"value is not canonical JSON: {error}") from error


def encoded(value: Any) -> bytes:
    return canonical(value) + b"\n"


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def file_sha(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        raise BuildError(f"cannot read {path}: {error}") from error


def without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return digest(canonical({key: item for key, item in value.items() if key not in omitted}))


def seal(value: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    result.pop("authority_sha256", None)
    result["authority_sha256"] = without(result, "authority_sha256")
    return result


def row_seal(value: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    result.pop("row_sha256", None)
    result["row_sha256"] = without(result, "row_sha256")
    return result


def set_digest(values: Iterable[str]) -> str:
    return digest(canonical(sorted(values)))


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError as error:
        raise BuildError(f"path is outside repository: {path}") from error


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def reject_nonfinite_constant(token: str) -> None:
    raise BuildError(f"non-finite JSON number is forbidden: {token}")


def parse_json(payload: bytes, label: str) -> Any:
    try:
        return json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=reject_duplicate_pairs,
            parse_constant=reject_nonfinite_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise BuildError(f"cannot parse {label}: {error}") from error


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise BuildError(f"cannot load {path}: {error}") from error
    value = parse_json(payload, str(path))
    require(isinstance(value, dict), f"{path} must contain one object")
    return value


def load_jsonl(path: Path) -> list[tuple[int, dict[str, Any]]]:
    try:
        lines = path.read_bytes().splitlines()
    except OSError as error:
        raise BuildError(f"cannot load {path}: {error}") from error
    output: list[tuple[int, dict[str, Any]]] = []
    for line_number, raw in enumerate(lines, 1):
        require(bool(raw.strip()), f"blank JSONL row in {path}:{line_number}")
        value = parse_json(raw, f"{path}:{line_number}")
        require(isinstance(value, dict), f"non-object JSONL row in {path}:{line_number}")
        output.append((line_number, value))
    return output


def require_pinned(path: Path, expected: str, label: str) -> None:
    require(path.is_file(), f"{label} is missing: {relative(path)}")
    require(file_sha(path) == expected, f"{label} hash drifted")


def verify_seal(value: Mapping[str, Any], label: str) -> None:
    authority = value.get("authority_sha256")
    require(
        isinstance(authority, str) and SHA_RE.fullmatch(authority) is not None,
        f"{label} authority is malformed",
    )
    require(authority == without(value, "authority_sha256"), f"{label} authority is stale")


def verify_artifact_binding(
    row: Any,
    path: Path,
    label: str,
    *,
    expected_rows: int | None = None,
) -> None:
    require(isinstance(row, dict), f"{label} binding is missing or malformed")
    require(row.get("path") == relative(path), f"{label} path drifted")
    require(row.get("sha256") == file_sha(path), f"{label} hash drifted")
    if row.get("size_bytes") is not None:
        require(row.get("size_bytes") == path.stat().st_size, f"{label} size drifted")
    if expected_rows is not None:
        require(row.get("rows") == expected_rows, f"{label} declared row count drifted")
        require(
            len(path.read_bytes().splitlines()) == expected_rows,
            f"{label} physical row count drifted",
        )


def binding(
    path: Path,
    line_number: int,
    row: Mapping[str, Any],
    pointer: str,
    source_record_key_pointer: str,
) -> dict[str, Any]:
    return {
        "path": relative(path),
        "file_sha256": file_sha(path),
        "line_number": line_number,
        "source_row_sha256": digest(canonical(row)),
        "source_record_key_json_pointer": source_record_key_pointer,
        "exact_claim_json_pointer": pointer,
        "exact_context_json_pointer": None,
    }


def audit_binding(path: Path) -> dict[str, Any]:
    document = load_json(path)
    return {
        "path": relative(path),
        "file_sha256": file_sha(path),
        "schema_version": document.get("schema_version"),
    }


def normalized_semantic(summary: str) -> str:
    text = unicodedata.normalize("NFKC", summary).casefold()
    text = re.sub(r"\s+", " ", text).strip()
    require(bool(text), "empty normalized semantic summary")
    return text


def semantic_key(summary: str) -> str:
    return f"semantic-summary-nfkc-v1/{digest(normalized_semantic(summary).encode('utf-8'))}"


def source_decision(row: Mapping[str, Any], source_kind: str) -> str:
    if source_kind == "aimpl":
        value = row.get("final_decision")
    else:
        value = row.get("decision")
    return value if isinstance(value, str) else "invalid"


def source_tier(row: Mapping[str, Any], source_kind: str) -> str:
    if source_kind == "aimpl":
        value = row.get("final_tier")
    else:
        value = row.get("importance_tier")
    return value if isinstance(value, str) else "none"


def coverage(
    source_kind: str,
    path: Path,
    rows: Sequence[tuple[int, Mapping[str, Any]]],
    receipt: Path,
    *,
    qualified_candidate_keys: set[str] | None = None,
) -> dict[str, Any]:
    decisions = [source_decision(row, source_kind) for _, row in rows]
    require(
        all(decision in {"accept", "pending", "reject"} for decision in decisions),
        f"{source_kind} coverage has an unknown review decision in {relative(path)}",
    )
    accepted_rows = [
        row
        for decision, (_, row) in zip(decisions, rows, strict=True)
        if decision == "accept"
    ]
    require(
        all(source_tier(row, source_kind) in {"high", "medium", "low", "none"}
            for row in accepted_rows),
        f"{source_kind} coverage has an unknown importance tier in {relative(path)}",
    )
    if source_kind == "oeis":
        require(qualified_candidate_keys is not None, "OEIS coverage lacks survivor authority")
        eligible = sum(
            decision == "accept" and row.get("candidate_key") in qualified_candidate_keys
            for decision, (_, row) in zip(decisions, rows, strict=True)
        )
    else:
        require(
            all(source_tier(row, source_kind) in {"high", "medium"} for row in accepted_rows),
            f"{source_kind} accepted coverage row is below the importance gate",
        )
        eligible = len(accepted_rows)
    pending = sum(decision == "pending" for decision in decisions)
    not_release_eligible = len(rows) - eligible - pending
    require(
        eligible + pending + not_release_eligible == len(rows),
        f"{source_kind} coverage counters do not partition {relative(path)}",
    )
    return {
        "source_kind": source_kind,
        "path": relative(path),
        "file_sha256": file_sha(path),
        "size_bytes": path.stat().st_size,
        "rows": len(rows),
        "accepted_eligible": eligible,
        "pending": pending,
        # In this admission schema, rejected means not release-eligible; it
        # therefore also includes source accepts below the importance floor.
        "rejected": not_release_eligible,
        "audit_receipt": audit_binding(receipt),
    }


def base_row(
    *,
    candidate_key: str,
    source_kind: str,
    source_record_key: str,
    source_binding: Mapping[str, Any],
    statement: str,
    summary: str,
    tier: str,
    status: Mapping[str, Any],
    rights: Mapping[str, Any],
    dedupe: Mapping[str, Any],
    atomicity: str = "single",
    display_name: str | None = None,
    importance_basis: str,
    classification: Mapping[str, Any] | None = None,
    statement_representation: str = "reviewed_exact_source_assertion",
) -> dict[str, Any]:
    require(isinstance(candidate_key, str) and candidate_key.strip(), "missing candidate key")
    require(
        isinstance(source_record_key, str) and source_record_key.strip(),
        f"{candidate_key}: missing source record key",
    )
    require(isinstance(source_binding, Mapping), f"{candidate_key}: malformed source binding")
    require(
        set(source_binding)
        == {
            "path",
            "file_sha256",
            "line_number",
            "source_row_sha256",
            "source_record_key_json_pointer",
            "exact_claim_json_pointer",
            "exact_context_json_pointer",
        },
        f"{candidate_key}: source binding schema drifted",
    )
    require(isinstance(statement, str) and statement.strip(), f"{candidate_key}: missing statement")
    require(not statement.rstrip().endswith("?"), f"{candidate_key}: interrogative statement")
    require(isinstance(summary, str) and summary.strip(), f"{candidate_key}: missing summary")
    require(tier in {"high", "medium"}, f"{candidate_key}: below importance gate")
    require(atomicity in {"single", "source_named_compound"}, f"{candidate_key}: invalid atomicity")
    require(isinstance(status, Mapping) and bool(status), f"{candidate_key}: missing status evidence")
    require(isinstance(rights, Mapping), f"{candidate_key}: malformed rights evidence")
    require(
        rights.get("cleared_for_catalog_metadata_and_statement") is True
        and isinstance(rights.get("attribution"), str)
        and bool(rights["attribution"].strip()),
        f"{candidate_key}: rights gate failed",
    )
    require(isinstance(dedupe, Mapping), f"{candidate_key}: malformed dedupe evidence")
    require(
        dedupe.get("parent_semantic_unique") is True
        and dedupe.get("cross_source_semantic_unique") is True,
        f"{candidate_key}: dedupe gate failed",
    )
    require(
        isinstance(importance_basis, str) and importance_basis.strip(),
        f"{candidate_key}: missing importance basis",
    )
    require(
        classification is None or isinstance(classification, Mapping),
        f"{candidate_key}: malformed classification",
    )
    row = {
        "candidate_key": candidate_key,
        "decision": "accept",
        "accepted_rank": None,
        "grants_catalog_entry": True,
        "grants_strict_conjecture_credit": True,
        "source_kind": source_kind,
        "source_record_key": source_record_key,
        "source_binding": copy.deepcopy(dict(source_binding)),
        "exact_claim_text": statement,
        "exact_claim_context": None,
        "semantic_summary": summary,
        "semantic_key": semantic_key(summary),
        "statement_representation": statement_representation,
        "display_name": display_name or summary,
        "aliases": [],
        "statement_language": "en_or_mathematical_notation",
        "importance_tier": tier,
        "importance_basis": importance_basis,
        "truth_apt": True,
        "context_complete": True,
        "current_open_as_of_review": True,
        "question_to_assertion_promotion_performed": False,
        "atomicity": atomicity,
        "current_status_evidence": copy.deepcopy(dict(status)),
        "rights": copy.deepcopy(dict(rights)),
        "dedupe": copy.deepcopy(dict(dedupe)),
        "classification": copy.deepcopy(
            dict(classification or {"status": "source_or_review_metadata", "msc_codes": []})
        ),
    }
    return row


def oeis_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    require_pinned(OEIS_RECEIPT, OEIS_RECEIPT_SHA256, "OEIS audit receipt")
    require_pinned(OEIS_SURVIVORS, OEIS_SURVIVORS_SHA256, "OEIS final survivor ledger")
    receipt = load_json(OEIS_RECEIPT)
    require(
        receipt.get("schema_version") == "awesome-theorems/oeis-candidate-audit-receipt/5.5",
        "wrong OEIS audit receipt schema",
    )
    require(
        receipt.get("candidate_only") is True
        and receipt.get("formal_release_modified") is False
        and receipt.get("release_published") is False,
        "OEIS audit crossed its candidate-only publication boundary",
    )
    artifacts = receipt.get("artifacts")
    counts = receipt.get("counts")
    require(isinstance(artifacts, dict) and isinstance(counts, dict), "OEIS receipt is incomplete")
    receipt_source = receipt.get("source")
    require(isinstance(receipt_source, dict), "OEIS frozen-source binding is missing")
    verify_artifact_binding(
        receipt_source.get("source_receipt"),
        OEIS_SOURCE_RECEIPT,
        "OEIS frozen-source receipt",
    )
    source_receipt = load_json(OEIS_SOURCE_RECEIPT)
    source_metadata = source_receipt.get("source")
    require(
        source_receipt.get("schema_version") == "awesome-theorems/oeis-frozen-source-receipt/5.5"
        and source_receipt.get("candidate_only") is True
        and source_receipt.get("grants_catalog_entry") is False
        and source_receipt.get("grants_strict_conjecture_credit") is False
        and isinstance(source_metadata, dict)
        and source_metadata.get("commit") == "4c8663620c66525a0c92654a4a9c4703b3d98921"
        and source_metadata.get("license_spdx") == "CC-BY-SA-4.0",
        "OEIS frozen-source rights/publication boundary failed",
    )
    verify_artifact_binding(
        artifacts.get("combined-survivors.jsonl"),
        OEIS_SURVIVORS,
        "OEIS survivor ledger",
        expected_rows=268,
    )
    require(counts.get("combined_candidate_survivors") == 268, "OEIS survivor count drifted")
    survivor_rows = load_jsonl(OEIS_SURVIVORS)
    require(len(survivor_rows) == 268, "OEIS survivor denominator drifted")
    survivors: dict[str, dict[str, Any]] = {}
    for _, survivor in survivor_rows:
        key = survivor.get("candidate_key")
        require(
            isinstance(key, str) and key and key not in survivors,
            f"OEIS survivor key is missing or duplicated: {key}",
        )
        require(
            survivor.get("candidate_only") is True
            and survivor.get("grants_catalog_entry") is False
            and survivor.get("grants_strict_conjecture_credit") is False,
            f"OEIS survivor crossed the candidate-only boundary: {key}",
        )
        survivors[key] = survivor
    review_index: dict[str, tuple[Path, int, dict[str, Any]]] = {}
    coverage_rows: list[dict[str, Any]] = []
    for path in OEIS_REVIEWS:
        rows = load_jsonl(path)
        artifact_key = path.relative_to(OEIS_ROOT).as_posix()
        verify_artifact_binding(
            artifacts.get(artifact_key),
            path,
            f"OEIS review {artifact_key}",
            expected_rows=len(rows),
        )
        coverage_rows.append(
            coverage(
                "oeis",
                path,
                rows,
                OEIS_RECEIPT,
                qualified_candidate_keys=set(survivors),
            )
        )
        for line_number, row in rows:
            key = row.get("candidate_key")
            require(isinstance(key, str) and key not in review_index, f"OEIS review key duplicate: {key}")
            review_index[key] = (path, line_number, row)
    require(sum(item["rows"] for item in coverage_rows) == 1_101, "OEIS review universe drifted")
    require(
        sum(item["accepted_eligible"] for item in coverage_rows) == 268,
        "OEIS receipt-authorized survivor coverage drifted",
    )
    require(set(survivors).issubset(review_index), "OEIS survivor lacks reviewed source row")

    output: list[dict[str, Any]] = []
    rights = {
        "cleared_for_catalog_metadata_and_statement": True,
        "attribution": "OEIS Foundation Inc. and OEIS contributors",
        "license_spdx": "CC-BY-SA-4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "share_alike_required": True,
        "source_pointer_required": True,
        "license_evidence_receipt_path": relative(OEIS_SOURCE_RECEIPT),
        "license_evidence_receipt_sha256": file_sha(OEIS_SOURCE_RECEIPT),
    }
    for key in sorted(survivors):
        survivor = survivors[key]
        path, line_number, review = review_index[key]
        require(review.get("decision") == "accept", f"OEIS survivor is not review-accepted: {key}")
        require(review.get("truth_apt") is True and review.get("context_complete") is True, f"OEIS statement gate failed: {key}")
        require(review.get("source_asserted_open_as_of_commit") is True, f"OEIS current-open gate failed: {key}")
        require(review.get("importance_tier") == survivor.get("importance_tier"), f"OEIS tier drifted: {key}")
        require(review.get("semantic_summary") == survivor.get("semantic_summary"), f"OEIS summary drifted: {key}")
        statement = review.get("exact_claim_text")
        summary = survivor.get("semantic_summary")
        a_numbers = survivor.get("a_numbers")
        require(isinstance(a_numbers, list) and a_numbers and all(isinstance(item, str) for item in a_numbers), f"OEIS A-number binding malformed: {key}")
        output.append(
            base_row(
                candidate_key=key,
                source_kind="oeis",
                source_record_key=key,
                source_binding=binding(
                    path, line_number, review, "/exact_claim_text", "/candidate_key"
                ),
                statement=statement,
                summary=summary,
                tier=survivor["importance_tier"],
                status={
                    "as_of": REVIEW_DATE,
                    "evidence_level": "pinned_oeis_source_and_independent_review",
                    "source_commit": "4c8663620c66525a0c92654a4a9c4703b3d98921",
                    "source_asserted_open_as_of_commit": True,
                    "review_row_sha256": digest(canonical(review)),
                    "a_numbers": a_numbers,
                },
                rights=rights,
                dedupe={
                    "parent_semantic_unique": True,
                    "cross_source_semantic_unique": True,
                    "basis": "OEIS final survivor audit plus later AimPL/OPG cross-source review",
                    "survivor_ledger_sha256": OEIS_SURVIVORS_SHA256,
                },
                importance_basis=review.get("importance_basis", "OEIS proposition-level human review"),
                classification={"status": "source_or_review_metadata", "msc_codes": [], "oeis_a_numbers": a_numbers},
            )
        )
    return output, coverage_rows


def aimpl_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    require_pinned(AIMPL_RECEIPT, AIMPL_RECEIPT_SHA256, "AimPL audit receipt")
    require_pinned(AIMPL_REVIEW, AIMPL_REVIEW_SHA256, "AimPL review ledger")
    receipt = load_json(AIMPL_RECEIPT)
    require(
        receipt.get("schema_version") == "awesome-theorems/aimpl-strict-conjecture-review/1",
        "wrong AimPL audit receipt schema",
    )
    require(
        receipt.get("formal_release_modified") is False
        and receipt.get("strict_credits_granted") == 0,
        "AimPL audit crossed its candidate-only publication boundary",
    )
    artifacts = receipt.get("artifacts")
    require(isinstance(artifacts, dict), "AimPL receipt artifact inventory is missing")
    verify_artifact_binding(
        artifacts.get("review_ledger"),
        AIMPL_REVIEW,
        "AimPL review ledger",
        expected_rows=59,
    )
    verify_artifact_binding(
        artifacts.get("candidates"),
        AIMPL_CANDIDATES,
        "AimPL candidate source ledger",
        expected_rows=59,
    )
    rows = load_jsonl(AIMPL_REVIEW)
    require(len(rows) == 59, "AimPL review universe drifted")
    candidate_rows = load_jsonl(AIMPL_CANDIDATES)
    candidates: dict[str, tuple[int, dict[str, Any]]] = {}
    for candidate_line, candidate in candidate_rows:
        key = candidate.get("candidate_key")
        require(
            isinstance(key, str) and key and key not in candidates,
            f"AimPL source candidate key is missing or duplicated: {key}",
        )
        candidates[key] = (candidate_line, candidate)
    require(len(candidates) == 59, "AimPL candidate source universe drifted")
    output: list[dict[str, Any]] = []
    for line_number, review in rows:
        require(
            review.get("candidate_only") is True
            and review.get("strict_credit_granted") is False,
            f"AimPL row {line_number} crossed the candidate-only boundary",
        )
        if review.get("final_decision") != "accept":
            continue
        initial = review.get("initial_review")
        require(isinstance(initial, dict) and initial.get("decision") == "accept", "AimPL final accept lacks accepted source review")
        require(initial.get("truth_apt") is True and initial.get("context_complete") is True, "AimPL statement gate failed")
        require(initial.get("source_asserted_open") is True, "AimPL current-open gate failed")
        require(initial.get("tier") == review.get("final_tier"), "AimPL accepted tier drifted")
        require(
            initial.get("reason_code")
            in {
                "complete_atomic_open_conjecture",
                "explicit_open_atomic_component",
                "explicit_open_atomic_conjecture",
                "explicit_open_atomic_conjecture_with_redundant_special_case",
                "atomic_affirmative_subclaim_selected",
                "atomic_numbered_subclaim_selected",
                "atomic_conjunct_selected",
            },
            "AimPL accepted row lacks an approved atomic-selection reason",
        )
        cross = review.get("cross_dedupe")
        require(
            isinstance(cross, dict)
            and cross.get("manual_verdict")
            in {
                "semantic_unique_with_any_listed_relations_non_equivalent",
                "component_overlap_present_no_duplicate_credit",
            },
            "AimPL semantic review gate failed",
        )
        raw_key = review.get("candidate_key")
        require(isinstance(raw_key, str) and raw_key, "AimPL candidate key missing")
        candidate_match = candidates.get(raw_key)
        require(candidate_match is not None, f"AimPL review lacks a source candidate: {raw_key}")
        candidate_line, candidate = candidate_match
        exact_source = candidate.get("exact_source")
        candidate_rights = candidate.get("rights")
        snapshot = candidate.get("source_snapshot")
        require(
            isinstance(exact_source, dict)
            and isinstance(candidate_rights, dict)
            and isinstance(snapshot, dict),
            f"AimPL source evidence is malformed: {raw_key}",
        )
        require(
            candidate.get("source_record_key") == review.get("source_record_key")
            and isinstance(exact_source.get("body_html"), str)
            and isinstance(initial.get("exact_claim_html"), str)
            and initial["exact_claim_html"] in exact_source["body_html"]
            and snapshot.get("source_sha256") == review.get("source_sha256")
            and snapshot.get("source_url") == review.get("source_url"),
            f"AimPL source/review binding drifted: {raw_key}",
        )
        require(
            candidate_rights.get("license_spdx") == "CC-BY-SA-3.0"
            and candidate_rights.get("license_url")
            == "http://creativecommons.org/licenses/by-sa/3.0/"
            and candidate_rights.get("share_alike_required_for_adapted_source_text") is True
            and isinstance(candidate_rights.get("attribution"), str)
            and bool(candidate_rights["attribution"].strip()),
            f"AimPL source rights gate failed: {raw_key}",
        )
        summary = initial.get("semantic_summary")
        output.append(
            base_row(
                candidate_key=f"aimpl/{raw_key}",
                source_kind="aimpl",
                source_record_key=str(review.get("source_record_key")),
                source_binding=binding(
                    AIMPL_REVIEW,
                    line_number,
                    review,
                    "/initial_review/exact_claim_html",
                    "/source_record_key",
                ),
                statement=initial.get("exact_claim_html"),
                summary=summary,
                tier=review.get("final_tier"),
                status={
                    "as_of": REVIEW_DATE,
                    "evidence_level": "pinned_aimpl_snapshot_and_independent_review",
                    "source_asserted_open": True,
                    "source_url": review.get("source_url"),
                    "source_sha256": review.get("source_sha256"),
                },
                rights={
                    "cleared_for_catalog_metadata_and_statement": True,
                    "attribution": candidate_rights["attribution"],
                    "license_spdx": candidate_rights["license_spdx"],
                    "license_url": candidate_rights["license_url"],
                    "share_alike_required": True,
                    "source_pointer_required": True,
                    "license_evidence_path": relative(AIMPL_CANDIDATES),
                    "license_evidence_file_sha256": file_sha(AIMPL_CANDIDATES),
                    "license_evidence_line_number": candidate_line,
                    "license_evidence_row_sha256": digest(canonical(candidate)),
                },
                dedupe={
                    "parent_semantic_unique": True,
                    "cross_source_semantic_unique": True,
                    "basis": cross.get("manual_verdict"),
                    "reviewed_relations": {
                        key: cross.get(key, []) for key in ("parent_5_4", "oeis", "aimpl_batch", "conjecturebench")
                    },
                },
                importance_basis=initial.get("basis", "AimPL proposition-level human review"),
            )
        )
    require(len(output) == 43, "AimPL accepted denominator drifted")
    return output, [coverage("aimpl", AIMPL_REVIEW, rows, AIMPL_RECEIPT)]


def open_logic_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    require_pinned(OPEN_LOGIC_RECEIPT, OPEN_LOGIC_RECEIPT_SHA256, "Open Logic audit receipt")
    require_pinned(OPEN_LOGIC_REVIEW, OPEN_LOGIC_REVIEW_SHA256, "Open Logic review ledger")
    receipt = load_json(OPEN_LOGIC_RECEIPT)
    require(
        receipt.get("schema_version")
        == "awesome-theorems/open-logic-strict-source-review-count/1.0",
        "wrong Open Logic audit receipt schema",
    )
    require(
        receipt.get("artifact") == OPEN_LOGIC_REVIEW.name
        and receipt.get("artifact_sha256") == file_sha(OPEN_LOGIC_REVIEW)
        and receipt.get("release_modified") is False,
        "Open Logic receipt does not authenticate the candidate-only review ledger",
    )
    rows = load_jsonl(OPEN_LOGIC_REVIEW)
    receipt_counts = receipt.get("counts")
    require(
        len(rows) == 17
        and isinstance(receipt_counts, dict)
        and receipt_counts.get("total") == 17,
        "Open Logic review universe drifted",
    )
    output: list[dict[str, Any]] = []
    for line_number, review in rows:
        if review.get("decision") != "accept":
            continue
        require(review.get("acceptance_evidence_complete") is True, "Open Logic acceptance evidence incomplete")
        require(
            review.get("grants_strict_conjecture_credit") is True
            and review.get("release_mutation_authorized_or_performed") is False
            and review.get("question_to_assertion_promotion_permitted") is False,
            "Open Logic acceptance/publication boundary failed",
        )
        require(review.get("truth_apt") is True and review.get("context_complete") is True, "Open Logic statement gate failed")
        status = review.get("source_status")
        require(isinstance(status, dict) and status.get("current_open_as_of_review") is True, "Open Logic current-open gate failed")
        source = review.get("source")
        rights_source = review.get("rights")
        dedupe_source = review.get("dedupe")
        require(isinstance(source, dict) and isinstance(rights_source, dict) and isinstance(dedupe_source, dict), "Open Logic evidence malformed")
        require(
            rights_source.get("status") == "cleared_cc_by_4_0_with_attribution"
            and rights_source.get("license") == "CC-BY-4.0"
            and isinstance(rights_source.get("attribution"), str)
            and bool(rights_source["attribution"].strip()),
            "Open Logic rights evidence failed",
        )
        require(
            dedupe_source.get("parent_5_4_catalog_sha256") == PARENT_CATALOG_SHA256
            and dedupe_source.get("within_batch") == "unique"
            and not dedupe_source.get("parent_duplicate_targets")
            and dedupe_source.get("other_overlap_grants_duplicate_credit") is False,
            "Open Logic semantic dedupe evidence failed",
        )
        problem_id = review.get("problem_id")
        require(isinstance(problem_id, int) and not isinstance(problem_id, bool), "Open Logic problem ID malformed")
        output.append(
            base_row(
                candidate_key=f"open_logic/{problem_id}",
                source_kind="open_logic",
                source_record_key=str(problem_id),
                source_binding=binding(
                    OPEN_LOGIC_REVIEW,
                    line_number,
                    review,
                    "/exact_claim_text",
                    "/problem_id",
                ),
                statement=review.get("exact_claim_text"),
                summary=review.get("exact_claim_text"),
                tier=review.get("importance_tier"),
                status=status,
                rights={
                    "cleared_for_catalog_metadata_and_statement": rights_source.get("status") == "cleared_cc_by_4_0_with_attribution",
                    "attribution": rights_source.get("attribution"),
                    "attribution_url": rights_source.get("attribution_url"),
                    "license_spdx": rights_source.get("license"),
                    "license_url": rights_source.get("license_url"),
                    "change_notice_required_if_adapted": rights_source.get("change_notice_required_if_adapted"),
                    "source_pointer_required": True,
                },
                dedupe={
                    "parent_semantic_unique": not bool(dedupe_source.get("parent_duplicate_targets")),
                    "cross_source_semantic_unique": dedupe_source.get("other_overlap_grants_duplicate_credit") is False,
                    "basis": dedupe_source.get("parent_semantic_review"),
                    "other_source_overlaps": dedupe_source.get("other_source_overlaps", []),
                },
                atomicity="source_named_compound" if review.get("target_component_count", 1) > 1 else "single",
                display_name=review.get("name"),
                importance_basis=review.get("importance_basis", "Open Logic impact review"),
                classification={"status": "source_or_review_metadata", "msc_codes": [], "source_areas": review.get("areas", [])},
            )
        )
    require(len(output) == 4, "Open Logic accepted denominator drifted")
    require(
        receipt_counts.get("accepted") == 4
        and receipt_counts.get("grants_strict_conjecture_credit") == 4
        and receipt.get("accepted_problem_ids")
        == [row.get("problem_id") for _, row in rows if row.get("decision") == "accept"],
        "Open Logic accepted receipt counts drifted",
    )
    return output, [coverage("open_logic", OPEN_LOGIC_REVIEW, rows, OPEN_LOGIC_RECEIPT)]


def opg_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    require(
        OPG_RECEIPT.is_file() and OPG_REVIEW.is_file(),
        "final OPG eligibility ledger/receipt is missing",
    )
    receipt = load_json(OPG_RECEIPT)
    require(
        receipt.get("schema_version")
        == "awesome-theorems/openproblemgarden-eligibility-receipt/1",
        "wrong OPG receipt schema",
    )
    require(
        OPG_RECEIPT.read_bytes() == encoded(receipt),
        "OPG receipt is not canonical JSON plus one LF",
    )
    verify_seal(receipt, "OPG eligibility receipt")
    output_binding = receipt.get("output")
    verify_artifact_binding(
        output_binding,
        OPG_REVIEW,
        "OPG eligibility ledger",
        expected_rows=404,
    )
    rows = load_jsonl(OPG_REVIEW)
    raw_rows = OPG_REVIEW.read_bytes().splitlines()
    require(
        all(raw == canonical(row) for raw, (_, row) in zip(raw_rows, rows, strict=True)),
        "OPG eligibility ledger is not canonical JSONL",
    )
    require(len(rows) == 404, "OPG review universe is not 404 rows")

    observed_decisions = {decision: 0 for decision in ("accept", "pending", "reject")}
    observed_tiers = {tier: 0 for tier in ("high", "medium")}
    candidate_keys: set[str] = set()
    source_records: set[str] = set()
    accepted_ranks: list[int] = []
    for expected_index, (_, review) in enumerate(rows, 1):
        require(
            review.get("schema_version")
            == "awesome-theorems/openproblemgarden-eligibility/1",
            f"OPG row {expected_index} schema drifted",
        )
        require(
            review.get("row_sha256") == without(review, "row_sha256"),
            f"OPG row {expected_index} seal is stale",
        )
        require(
            review.get("candidate_index") == expected_index,
            f"OPG row {expected_index} index drifted",
        )
        decision = review.get("decision")
        require(decision in observed_decisions, f"OPG row {expected_index} decision is invalid")
        observed_decisions[decision] += 1
        candidate_key = review.get("candidate_key")
        source_record = review.get("source_record_key")
        require(
            isinstance(candidate_key, str)
            and candidate_key
            and candidate_key not in candidate_keys,
            f"OPG row {expected_index} candidate key is missing or duplicated",
        )
        require(
            isinstance(source_record, str)
            and source_record
            and source_record not in source_records,
            f"OPG row {expected_index} source record is missing or duplicated",
        )
        candidate_keys.add(candidate_key)
        source_records.add(source_record)
        require(
            review.get("candidate_only") is True
            and review.get("grants_catalog_entry") is False
            and review.get("grants_strict_conjecture_credit") is False
            and review.get("release_mutation_authorized_or_performed") is False,
            f"OPG row {expected_index} crossed the candidate-only boundary",
        )
        if decision == "accept":
            rank = review.get("accepted_rank")
            require(
                isinstance(rank, int) and not isinstance(rank, bool),
                f"OPG row {expected_index} accepted rank malformed",
            )
            accepted_ranks.append(rank)
            tier = review.get("importance_tier")
            require(tier in observed_tiers, f"OPG row {expected_index} accepted tier is below gate")
            observed_tiers[tier] += 1
        else:
            require(
                review.get("accepted_rank") is None,
                f"OPG row {expected_index} nonaccept has a rank",
            )
            require(
                review.get("formal_acceptance_eligible_for_5_5") is False,
                f"OPG row {expected_index} nonaccept is marked formally eligible",
            )
    require(
        sorted(accepted_ranks) == list(range(1, len(accepted_ranks) + 1)),
        "OPG accepted ranks are not dense 1..N",
    )
    receipt_counts = receipt.get("counts")
    require(isinstance(receipt_counts, dict), "OPG receipt counts missing")
    decisions = receipt_counts.get("decisions")
    require(decisions == observed_decisions, "OPG receipt decision counts drifted")
    require(
        receipt_counts.get("accepted_tiers") == observed_tiers,
        "OPG receipt accepted-tier counts drifted",
    )

    output: list[dict[str, Any]] = []
    for line_number, review in rows:
        if review.get("decision") != "accept":
            continue
        require(
            review.get("formal_acceptance_eligible_for_5_5") is True,
            "OPG accept is not formally eligible",
        )
        require(review.get("source_kind") == "open_problem_garden", "OPG source kind drifted")
        require(
            review.get("truth_apt") is True and review.get("context_complete") is True,
            "OPG statement gate failed",
        )
        require(review.get("current_open_as_of") == REVIEW_DATE, "OPG current-open gate failed")
        status = review.get("current_open_evidence")
        require(isinstance(status, dict) and bool(status), "OPG current-open evidence missing")
        global_dedupe = review.get("global_dedupe")
        rights_source = review.get("rights")
        attribution = review.get("attribution")
        require(
            isinstance(global_dedupe, dict)
            and global_dedupe.get("semantic_unique") is True
            and isinstance(global_dedupe.get("authority_set_sha256"), str)
            and SHA_RE.fullmatch(global_dedupe["authority_set_sha256"]) is not None
            and global_dedupe.get("within_opg_canonical_candidate_key")
            == review.get("candidate_key"),
            "OPG global dedupe gate failed",
        )
        require(
            isinstance(rights_source, dict)
            and rights_source.get("exact_source_wording_excluded_from_release") is True,
            "OPG source-wording rights boundary failed",
        )
        require(
            isinstance(attribution, dict)
            and isinstance(attribution.get("url"), str)
            and bool(attribution["url"].strip())
            and isinstance(attribution.get("title"), str)
            and bool(attribution["title"].strip()),
            "OPG attribution missing",
        )
        # The independently authored semantic summary is the release statement.
        # The evidence-only exact source wording is deliberately not copied.
        summary = review.get("semantic_summary")
        source_wording = review.get("exact_claim_text")
        require(
            review.get("source_wording_usage") == "evidence_only_not_release_payload",
            "OPG source wording usage drifted",
        )
        require(
            isinstance(summary, str)
            and summary.strip()
            and isinstance(source_wording, str)
            and source_wording.strip()
            and normalized_semantic(summary) != normalized_semantic(source_wording),
            "OPG independent summary duplicates excluded source wording",
        )
        require(review.get("semantic_key") == semantic_key(summary), "OPG semantic key drifted")
        decision_basis = review.get("decision_basis")
        require(
            isinstance(decision_basis, str) and decision_basis.strip(),
            "OPG decision basis is missing",
        )
        output.append(
            base_row(
                candidate_key=f"opg/{review['candidate_key']}",
                source_kind="open_problem_garden",
                source_record_key=review["source_record_key"],
                source_binding=binding(
                    OPG_REVIEW,
                    line_number,
                    review,
                    "/semantic_summary",
                    "/source_record_key",
                ),
                statement=summary,
                summary=summary,
                tier=review.get("importance_tier"),
                status=status,
                rights={
                    "cleared_for_catalog_metadata_and_statement": True,
                    "attribution": "Open Problem Garden; " + attribution["title"],
                    "attribution_url": attribution["url"],
                    "release_payload": "independently_written_review_summary_plus_pointer",
                    "exact_source_wording_excluded_from_release": True,
                    "statement_origin": "independently_written_reviewed_summary",
                    "source_wording_redistributed": False,
                    "source_pointer_required": True,
                },
                dedupe={
                    "parent_semantic_unique": True,
                    "cross_source_semantic_unique": True,
                    "basis": decision_basis,
                    "authority_set_sha256": global_dedupe["authority_set_sha256"],
                    "duplicate_targets": global_dedupe.get("duplicate_targets", []),
                },
                atomicity=review.get("atomicity"),
                display_name=attribution["title"],
                importance_basis=decision_basis,
                statement_representation="independently_written_reviewed_summary",
            )
        )
    require(len(output) == decisions.get("accept"), "OPG accepted count differs from receipt")
    require(len(output) >= 86, "OPG survivor count is below the 401-total release requirement")
    return output, [coverage("open_problem_garden", OPG_REVIEW, rows, OPG_RECEIPT)]


def parent_semantics() -> set[str]:
    require_pinned(PARENT_CATALOG, PARENT_CATALOG_SHA256, "parent claim catalog")
    require_pinned(PARENT_STRICT, PARENT_STRICT_SHA256, "parent strict ledger")
    catalog = load_json(PARENT_CATALOG)
    records = catalog.get("records")
    require(isinstance(records, list) and len(records) == 4_100, "parent catalog denominator drifted")
    result: set[str] = set()
    for row in records:
        if not isinstance(row, dict):
            continue
        direct = row.get("semantic_key")
        if isinstance(direct, str):
            result.add(direct)
        dedupe = row.get("dedupe")
        if isinstance(dedupe, dict):
            nested = dedupe.get("semantic_key")
            if isinstance(nested, str):
                result.add(nested)
            normalized = dedupe.get("normalized_statement_sha256")
            if isinstance(normalized, str) and SHA_RE.fullmatch(normalized):
                result.add(f"normalized-statement-sha256/{normalized}")
            identity = dedupe.get("identity_payload_sha256")
            if isinstance(identity, str) and SHA_RE.fullmatch(identity):
                result.add(f"formal-conjectures-parent-identity/{identity}")
    return result


def build() -> dict[str, Any]:
    parent_keys = parent_semantics()
    groups = [oeis_rows(), aimpl_rows(), open_logic_rows(), opg_rows()]
    rows = [row for group, _ in groups for row in group]
    coverage_rows = [item for _, items in groups for item in items]
    require(MIN_ACCEPTED <= len(rows) <= MAX_ACCEPTED, "accepted strict-conjecture total misses 401--1,000 gate")
    require(len(coverage_rows) == 19, "review coverage must bind exactly 19 JSONL ledgers")
    require(
        len({item["path"] for item in coverage_rows}) == len(coverage_rows),
        "review coverage repeats a JSONL ledger",
    )
    require(
        {item["source_kind"] for item in coverage_rows}
        == {"oeis", "aimpl", "open_logic", "open_problem_garden"},
        "review coverage source-kind set drifted",
    )
    require(
        sum(item["rows"] for item in coverage_rows) == 1_581,
        "complete review universe must contain exactly 1,581 rows",
    )
    require(
        all(
            item["accepted_eligible"] + item["pending"] + item["rejected"]
            == item["rows"]
            for item in coverage_rows
        ),
        "review coverage dispositions do not close",
    )

    candidate_keys: set[str] = set()
    semantic_keys: set[str] = set()
    source_records: set[tuple[str, str]] = set()
    for rank, row in enumerate(rows, 1):
        key = row["candidate_key"]
        semantic = row["semantic_key"]
        source = (row["source_kind"], row["source_record_key"])
        require(key not in candidate_keys, f"duplicate candidate key: {key}")
        require(semantic not in semantic_keys, f"duplicate normalized semantic summary: {semantic}")
        require(semantic not in parent_keys, f"semantic key collides with parent: {semantic}")
        require(source not in source_records, f"duplicate source record: {source}")
        row["accepted_rank"] = rank
        candidate_keys.add(key)
        semantic_keys.add(semantic)
        source_records.add(source)
    accepted_by_source = {
        source: sum(row["source_kind"] == source for row in rows)
        for source in ("oeis", "aimpl", "open_logic", "open_problem_garden")
    }
    coverage_eligible_by_source = {
        source: sum(
            item["accepted_eligible"]
            for item in coverage_rows
            if item["source_kind"] == source
        )
        for source in accepted_by_source
    }
    require(
        accepted_by_source == coverage_eligible_by_source,
        "accepted rows differ from the receipt-replayed eligible coverage set",
    )
    coverage_rows.sort(key=lambda item: (item["source_kind"], item["path"]))
    sealed_rows = [row_seal(row) for row in rows]
    return seal(
        {
            "schema_version": "awesome-theorems/strict-conjecture-curation/5.5",
            "review_as_of": REVIEW_DATE,
            "parent": {
                "release": "5.4",
                "release_root_sha256": PARENT_RELEASE_ROOT,
                "claim_catalog_sha256": PARENT_CATALOG_SHA256,
                "strict_ledger_sha256": PARENT_STRICT_SHA256,
            },
            "coverage_bindings": coverage_rows,
            "candidate_dispositions": sealed_rows,
            "counts": {
                "admissible_pool_rows": len(sealed_rows),
                "accepted_new_strict_conjectures": len(sealed_rows),
                "pending_not_credited": 0,
                "rejected_not_credited": 0,
                "by_source": accepted_by_source,
            },
            "set_digests": {
                "accepted_candidate_key_set_sha256": set_digest(row["candidate_key"] for row in sealed_rows),
                "accepted_semantic_key_set_sha256": set_digest(row["semantic_key"] for row in sealed_rows),
            },
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the canonical sealed ledger")
    arguments = parser.parse_args()
    document = build()
    payload = encoded(document)
    if arguments.write:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        temporary = OUTPUT.with_suffix(OUTPUT.suffix + ".tmp")
        temporary.write_bytes(payload)
        temporary.replace(OUTPUT)
    else:
        require(OUTPUT.is_file(), f"output is missing (run with --write): {relative(OUTPUT)}")
        require(OUTPUT.read_bytes() == payload, "strict conjecture curation is stale")
    counts = document["counts"]
    print(
        "strict-curation-v5.5: "
        f"accepted={counts['accepted_new_strict_conjectures']} "
        f"by_source={json.dumps(counts['by_source'], sort_keys=True)} "
        f"authority={document['authority_sha256']}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as error:
        raise SystemExit(f"ERROR: {error}") from error
