#!/usr/bin/env python3
"""Build the pinned NaturalProofs ProofWiki ↔ 1000+ title join asset.

Only exact equality after a documented Unicode/title normalization is joined.
The joined NaturalProofs rows are statement-review candidates; title equality
alone never grants theorem identity, truth, importance, or release credit.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import gzip
import hashlib
import html
import json
from pathlib import Path
import re
from typing import Any, Mapping
import unicodedata


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = REPO_ROOT / "Docs/catalog/v5/sources/1000-plus-theorems-8e04b97d.json"
DEFAULT_NATURALPROOFS = (
    REPO_ROOT / "Docs/catalog/v5/sources/naturalproofs-proofwiki-v2.0.0.json.gz"
)
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "Docs/catalog/v5/sources/naturalproofs-proofwiki-1000-plus-title-join-v2.0.0.json.gz"
)

SCHEMA_VERSION = "awesome-theorems/naturalproofs-1000-plus-title-join/v5-intake-1"
SOURCE_SCHEMA = "awesome-theorems/1000-plus-theorem-source/v5-intake-1"
SOURCE_SHA256 = "fe61d56e4ba4cc3a9846e2b153edee32dae6b1266b668e1a63dd3639d867bdad"
SOURCE_CONTENT_DIGEST = "17635bd3beefd7534fdd32df36be364f5540696fc424876c20296a59408eecd7"
NATURALPROOFS_FILENAME = "naturalproofs_proofwiki.json"
NATURALPROOFS_SIZE_BYTES = 116_780_142
NATURALPROOFS_MD5 = "f6d0cfcbfa91b47c9390ca654351fa46"
NATURALPROOFS_SHA256 = "5ecbad2ad0078aa679d48d219148a96bca2c9bc2a3c04d8476b7eb725602f5a5"
NATURALPROOFS_ARCHIVE_SHA256 = "17abb6eb24f7dc278b49d5d84d750bdead0ae54e1ee13d8de248ba03893a08c6"
NATURALPROOFS_ARCHIVE_SIZE_BYTES = 10_855_454
NATURALPROOFS_THEOREMS = 19_734
ZENODO_RECORD = "https://doi.org/10.5281/zenodo.4902289"
ZENODO_FILE_URL = (
    "https://zenodo.org/api/records/4902289/files/naturalproofs_proofwiki.json/content"
)
ZENODO_LICENSE_URL = "https://zenodo.org/api/records/4902289/files/LICENSE/content"
ZENODO_LICENSE_SHA256 = "5eb8b61e7f35ef20cbd875a889b085a7819f7d02165c9a54b3c03c127e07f420"
EXPECTED_MATCHED_IDENTITIES = 136
EXPECTED_MATCHED_TITLE_KEYS = 135
EXPECTED_UNAMBIGUOUS_IDENTITIES = 134


class JoinError(RuntimeError):
    pass


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def encoded_document(value: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def digest_file(path: Path, algorithm: str) -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    excluded = set(fields)
    return sha256_bytes(
        canonical_json_bytes({key: item for key, item in value.items() if key not in excluded})
    )


def normalize_title(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", html.unescape(value)).casefold()
    normalized = (
        normalized.replace("–", "-")
        .replace("—", "-")
        .replace("−", "-")
        .replace("_", " ")
    )
    return " ".join(re.findall(r"[\w]+", normalized, flags=re.UNICODE))


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise JoinError(f"cannot read {label} {path}: {error}") from error
    if not isinstance(value, dict):
        raise JoinError(f"{label} must contain one JSON object")
    return value


def validate_inputs(source_path: Path, naturalproofs_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if digest_file(source_path, "sha256") != SOURCE_SHA256:
        raise JoinError("1000+ normalized source SHA-256 drifted")
    source = load_json(source_path, "1000+ source")
    if source.get("schema_version") != SOURCE_SCHEMA or source.get(
        "content_digest_before_self_field"
    ) != SOURCE_CONTENT_DIGEST:
        raise JoinError("1000+ normalized source authority drifted")
    if naturalproofs_path.suffix == ".gz":
        if naturalproofs_path.stat().st_size != NATURALPROOFS_ARCHIVE_SIZE_BYTES:
            raise JoinError("NaturalProofs deterministic archive size drifted")
        if digest_file(naturalproofs_path, "sha256") != NATURALPROOFS_ARCHIVE_SHA256:
            raise JoinError("NaturalProofs deterministic archive SHA-256 drifted")
        try:
            raw_payload = gzip.decompress(naturalproofs_path.read_bytes())
        except (OSError, gzip.BadGzipFile) as error:
            raise JoinError(f"cannot decompress {naturalproofs_path}: {error}") from error
    else:
        raw_payload = naturalproofs_path.read_bytes()
    if len(raw_payload) != NATURALPROOFS_SIZE_BYTES:
        raise JoinError("NaturalProofs ProofWiki raw size drifted")
    if hashlib.md5(raw_payload).hexdigest() != NATURALPROOFS_MD5:
        raise JoinError("NaturalProofs ProofWiki MD5 drifted from Zenodo metadata")
    if sha256_bytes(raw_payload) != NATURALPROOFS_SHA256:
        raise JoinError("NaturalProofs ProofWiki raw SHA-256 drifted")
    try:
        natural = json.loads(raw_payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise JoinError(f"cannot parse NaturalProofs ProofWiki: {error}") from error
    if not isinstance(natural, dict):
        raise JoinError("NaturalProofs ProofWiki must contain one object")
    dataset = natural.get("dataset")
    rows = dataset.get("theorems") if isinstance(dataset, dict) else None
    if not isinstance(rows, list) or len(rows) != NATURALPROOFS_THEOREMS or not all(
        isinstance(row, dict) for row in rows
    ):
        raise JoinError("NaturalProofs ProofWiki theorem denominator drifted")
    return source, rows


def validate_natural_row(row: Mapping[str, Any], index: int) -> None:
    required = {
        "categories",
        "contents",
        "id",
        "label",
        "proofs",
        "recursive_categories",
        "ref_ids",
        "refs",
        "title",
        "toplevel_categories",
        "type",
    }
    if set(row) != required:
        raise JoinError(f"NaturalProofs theorem row {index} has unexpected keys")
    if row.get("id") != index or row.get("type") != "theorem":
        raise JoinError(f"NaturalProofs theorem row {index} identity/type drifted")
    for field in ("label", "title"):
        if not isinstance(row.get(field), str) or not row[field].strip():
            raise JoinError(f"NaturalProofs theorem row {index} has invalid {field}")
    for field in (
        "categories",
        "contents",
        "proofs",
        "recursive_categories",
        "ref_ids",
        "refs",
        "toplevel_categories",
    ):
        if not isinstance(row.get(field), list):
            raise JoinError(f"NaturalProofs theorem row {index} has invalid {field}")


def build_artifact(source: Mapping[str, Any], natural_rows: list[dict[str, Any]]) -> dict[str, Any]:
    source_rows = source.get("records")
    if not isinstance(source_rows, list) or len(source_rows) != 1_200:
        raise JoinError("1000+ source denominator changed")
    natural_by_title: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, row in enumerate(natural_rows):
        validate_natural_row(row, index)
        natural_by_title[normalize_title(row["title"])].append(row)
    source_by_title: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, row in enumerate(source_rows):
        if row.get("selection_rank") != index + 1:
            raise JoinError("1000+ source ordering drifted")
        source_by_title[normalize_title(row["title"])].append(row)

    matches: list[dict[str, Any]] = []
    for source_row in source_rows:
        normalized = normalize_title(source_row["title"])
        candidates = natural_by_title.get(normalized, [])
        if not candidates:
            continue
        source_collision_ids = sorted(
            (row["source_record_id"] for row in source_by_title[normalized]),
            key=lambda value: value.encode("utf-8"),
        )
        natural_collision_ids = sorted(row["id"] for row in candidates)
        unambiguous = len(source_collision_ids) == 1 and len(natural_collision_ids) == 1
        candidate_payloads: list[dict[str, Any]] = []
        for natural_row in candidates:
            statement = "\n".join(natural_row["contents"])
            payload: dict[str, Any] = {
                "naturalproofs_record": natural_row,
                "naturalproofs_row_sha256": sha256_bytes(canonical_json_bytes(natural_row)),
                "proof_count": len(natural_row["proofs"]),
                "statement_candidate": statement,
                "statement_candidate_sha256": sha256_bytes(statement.encode("utf-8")),
                "statement_completeness_reviewed": False,
            }
            payload["row_sha256"] = hash_without(payload, "row_sha256")
            candidate_payloads.append(payload)
        match: dict[str, Any] = {
            "automatic_identity_or_theorem_credit": False,
            "candidates": candidate_payloads,
            "external_id": source_row["external_id"],
            "match_class": "unicode_normalized_title_exact",
            "naturalproofs_collision_ids": natural_collision_ids,
            "normalized_title": normalized,
            "review_disposition": (
                "candidate_unambiguous_title_join_pending_statement_review"
                if unambiguous
                else "pending_source_identity_collision_review"
            ),
            "selection_rank": source_row["selection_rank"],
            "source_collision_ids": source_collision_ids,
            "source_record_id": source_row["source_record_id"],
            "source_row_sha256": source_row["row_sha256"],
            "source_title": source_row["title"],
        }
        match["row_sha256"] = hash_without(match, "row_sha256")
        matches.append(match)

    matches.sort(key=lambda row: row["selection_rank"])
    unique_keys = {row["normalized_title"] for row in matches}
    unambiguous_count = sum(
        row["review_disposition"]
        == "candidate_unambiguous_title_join_pending_statement_review"
        for row in matches
    )
    if (
        len(matches) != EXPECTED_MATCHED_IDENTITIES
        or len(unique_keys) != EXPECTED_MATCHED_TITLE_KEYS
        or unambiguous_count != EXPECTED_UNAMBIGUOUS_IDENTITIES
    ):
        raise JoinError(
            "NaturalProofs/1000+ exact-title join counts drifted: "
            f"identities={len(matches)} keys={len(unique_keys)} unambiguous={unambiguous_count}"
        )
    artifact: dict[str, Any] = {
        "counts": {
            "ambiguous_source_identities": len(matches) - unambiguous_count,
            "matched_1000_plus_identities": len(matches),
            "matched_normalized_title_keys": len(unique_keys),
            "naturalproofs_theorem_denominator": len(natural_rows),
            "unambiguous_title_join_identities": unambiguous_count,
            "unmatched_1000_plus_identities": len(source_rows) - len(matches),
        },
        "generator": {
            "path": "Docs/tools/extract_naturalproofs_1000_plus_join_v5.py",
            "version": "1.0.0",
        },
        "join_policy": {
            "automatic_credit": False,
            "normalization": (
                "HTML-unescape; Unicode NFKC; casefold; normalize dash variants; replace "
                "underscore with space; retain Unicode word runs; join with one ASCII space"
            ),
            "relation": "exact equality of normalized title",
            "review_requirement": (
                "A reviewer must resolve identity collisions and verify that contents are a "
                "complete statement with hypotheses, scope, and conclusion."
            ),
        },
        "matches": matches,
        "naturalproofs_snapshot": {
            "dataset_version": "2.0.0",
            "doi": ZENODO_RECORD,
            "download_url": ZENODO_FILE_URL,
            "filename": NATURALPROOFS_FILENAME,
            "local_archive_path": "Docs/catalog/v5/sources/naturalproofs-proofwiki-v2.0.0.json.gz",
            "local_archive_sha256": NATURALPROOFS_ARCHIVE_SHA256,
            "local_archive_size_bytes": NATURALPROOFS_ARCHIVE_SIZE_BYTES,
            "md5": NATURALPROOFS_MD5,
            "sha256": NATURALPROOFS_SHA256,
            "size_bytes": NATURALPROOFS_SIZE_BYTES,
            "theorem_records": NATURALPROOFS_THEOREMS,
        },
        "rights": {
            "attribution": "NaturalProofs authors and ProofWiki contributors",
            "catalog_relicenses_source": False,
            "license": "CC-BY-SA-4.0",
            "license_evidence_sha256": ZENODO_LICENSE_SHA256,
            "license_evidence_text": (
                "naturalproofs_proofwiki.json: Creative Commons "
                "Attribution-ShareAlike 4.0 International"
            ),
            "license_evidence_url": ZENODO_LICENSE_URL,
            "use": "exact_title_joined_statement_and_proof_review_candidates",
        },
        "schema_version": SCHEMA_VERSION,
        "source_asset": {
            "content_digest_before_self_field": SOURCE_CONTENT_DIGEST,
            "path": "Docs/catalog/v5/sources/1000-plus-theorems-8e04b97d.json",
            "schema_version": SOURCE_SCHEMA,
            "sha256": SOURCE_SHA256,
        },
    }
    artifact["content_digest_before_self_field"] = hash_without(
        artifact, "content_digest_before_self_field"
    )
    return artifact


def gzip_bytes(payload: bytes) -> bytes:
    return gzip.compress(payload, compresslevel=9, mtime=0)


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(payload)
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--naturalproofs", type=Path, default=DEFAULT_NATURALPROOFS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        source, natural_rows = validate_inputs(
            args.source.resolve(), args.naturalproofs.resolve()
        )
        artifact = build_artifact(source, natural_rows)
        compressed = gzip_bytes(encoded_document(artifact))
        if args.check:
            if args.output.resolve().read_bytes() != compressed:
                raise JoinError(f"{args.output} differs from deterministic rebuild")
            print(
                f"NaturalProofs join PASS: identities={len(artifact['matches'])} "
                f"sha256={sha256_bytes(compressed)}"
            )
        else:
            atomic_write(args.output.resolve(), compressed)
            print(
                f"wrote {args.output}: identities={len(artifact['matches'])} "
                f"sha256={sha256_bytes(compressed)}"
            )
    except (JoinError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"NaturalProofs join failed: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
