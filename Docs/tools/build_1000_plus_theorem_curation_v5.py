#!/usr/bin/env python3
"""Build the 1,200-row 1000+ theorem identity/statement curation ledger.

This ledger is an intake-quality authority, not a release.  It grants a narrow
high-confidence binding only when one 1000+ identity maps by its own pinned
Lean identifier to exactly one literal, kernel-checked, sorry-free mathlib
theorem already present in release 5.4.  Multi-declaration families, mapping
drift, lemmas, Wikipedia pages, and NaturalProofs title joins remain pending.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping
import unicodedata


REPO_ROOT = Path(__file__).resolve().parents[2]
V5_ROOT = REPO_ROOT / "Docs/catalog/v5"
SOURCE_PATH = V5_ROOT / "sources/1000-plus-theorems-8e04b97d.json"
WIKIPEDIA_PATH = V5_ROOT / "sources/wikipedia-en-1000-plus-revisions-20260810.json.gz"
NATURALPROOFS_PATH = (
    V5_ROOT / "sources/naturalproofs-proofwiki-1000-plus-title-join-v2.0.0.json.gz"
)
MATHLIB_PATH = V5_ROOT / "sources/mathlib-theorems-8a178386.json"
CURATION_53_PATH = V5_ROOT / "curation/Mathlib_Theorem_Curation_v5_3.json"
CURATION_54_PATH = V5_ROOT / "curation/Mathlib_Theorem_Curation_v5_4.json"
CATALOG_PATH = V5_ROOT / "releases/5.4/Claim_Catalog.json"
MANIFEST_PATH = V5_ROOT / "releases/5.4/Release_Manifest.json"
OUTPUT_PATH = V5_ROOT / "curation/Thousand_Plus_Theorem_Curation_v5.json"

SCHEMA_VERSION = "awesome-theorems/1000-plus-theorem-curation/v5-intake-1"
SOURCE_SHA256 = "fe61d56e4ba4cc3a9846e2b153edee32dae6b1266b668e1a63dd3639d867bdad"
SOURCE_CONTENT_DIGEST = "17635bd3beefd7534fdd32df36be364f5540696fc424876c20296a59408eecd7"
WIKIPEDIA_SHA256 = "73341aebcc1d9d1c577881d2c6d59734ce102d7cc07b1f8ec6d21c9875076d33"
WIKIPEDIA_CONTENT_DIGEST = "4acc9a0c33c73bae8bc508f41b5fa1f21149e6d210008f0563fe0167cf05e357"
NATURALPROOFS_SHA256 = "3cb44f9f7ed62b402a892e0b485c38d3881b9a4e40c5f34135a57fbf1d8936b5"
NATURALPROOFS_CONTENT_DIGEST = "52fe3b23f5d18c0a3323e806d317663ac40455043676d4c80f85df454179d67c"
MATHLIB_SHA256 = "236b9f6ac192eaf87215663bfd7fadb80c439b452049cef1747ea804c458637a"
CURATION_53_SHA256 = "379e165ae52ffd911e383fdb351fc602d36ec585e40bade54612c1512a7a1905"
CURATION_54_SHA256 = "0057a36999422726d6d490dbf59eca69824bc29a02f5117f9a02ebdd601dd386"
CATALOG_SHA256 = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
MANIFEST_SHA256 = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
RELEASE_ROOT = "c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813"

EXPECTED_COUNTS = {
    "accepted_exact_single_literal_theorem_binding": 125,
    "pending_multiple_exact_formal_bindings": 25,
    "rejected_nonliteral_lemma_binding": 8,
    "pending_external_signal_identifier_drift": 1,
    "pending_no_packaged_exact_statement": 68,
    "pending_statement_only_mapping": 1,
    "pending_no_formalized_mapping": 972,
}


class CurationError(RuntimeError):
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    excluded = set(fields)
    return sha256_bytes(
        canonical_json_bytes({key: item for key, item in value.items() if key not in excluded})
    )


def set_digest(values: Iterable[str]) -> str:
    return sha256_bytes(canonical_json_bytes(sorted(values)))


def load_json(path: Path, expected_sha256: str) -> dict[str, Any]:
    if sha256_file(path) != expected_sha256:
        raise CurationError(f"input SHA-256 drifted: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CurationError(f"cannot read {path}: {error}") from error
    if not isinstance(value, dict):
        raise CurationError(f"{path} must contain one object")
    return value


def load_gzip_json(path: Path, expected_sha256: str) -> dict[str, Any]:
    if sha256_file(path) != expected_sha256:
        raise CurationError(f"input SHA-256 drifted: {path}")
    try:
        payload = gzip.decompress(path.read_bytes())
        value = json.loads(payload.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, gzip.BadGzipFile) as error:
        raise CurationError(f"cannot read {path}: {error}") from error
    if not isinstance(value, dict):
        raise CurationError(f"{path} must contain one object")
    return value


def normalized_formal_type(value: str) -> str:
    return " ".join(value.split())


def normalized_declaration(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold().strip()


def exact_signals(row: Mapping[str, Any], external_id: str) -> list[dict[str, Any]]:
    signals = row.get("importance_signals")
    if not isinstance(signals, list):
        return []
    return [
        signal
        for signal in signals
        if isinstance(signal, dict)
        and signal.get("kind") == "mathlib_1000_theorems"
        and signal.get("external_id") == external_id
    ]


def curation_index(document: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    rows = document.get("candidate_dispositions")
    if not isinstance(rows, list):
        raise CurationError("mathlib curation lacks candidate_dispositions")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("source_record_id"), str):
            raise CurationError("invalid mathlib curation row")
        source_id = row["source_record_id"]
        if source_id in result:
            raise CurationError(f"duplicate mathlib curation source id {source_id}")
        result[source_id] = row
    return result


def catalog_index(document: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    records = document.get("records")
    if not isinstance(records, list):
        raise CurationError("5.4 catalog lacks records")
    result: dict[str, dict[str, Any]] = {}
    for row in records:
        if not isinstance(row, dict):
            raise CurationError("invalid catalog row")
        provenance = row.get("provenance")
        source_id = provenance.get("source_record_id") if isinstance(provenance, dict) else None
        if not isinstance(source_id, str) or not source_id.startswith("ML4-"):
            continue
        if source_id in result:
            raise CurationError(f"duplicate catalog source record id {source_id}")
        result[source_id] = row
    return result


def binding_payload(
    asset_row: Mapping[str, Any],
    curation_53: Mapping[str, Mapping[str, Any]],
    curation_54: Mapping[str, Mapping[str, Any]],
    catalog: Mapping[str, Mapping[str, Any]],
    matched_identifier: bool,
    external_id: str,
) -> dict[str, Any]:
    source_id = asset_row.get("source_record_id")
    declaration = asset_row.get("declaration")
    formal_type = asset_row.get("formal_type")
    if not all(isinstance(value, str) for value in (source_id, declaration, formal_type)):
        raise CurationError("mathlib asset binding has incomplete identity")
    asset_row_sha = sha256_bytes(canonical_json_bytes(asset_row))
    cat = catalog.get(source_id)
    cat_statement = cat.get("formal_statement") if isinstance(cat, dict) else None
    catalog_matches = bool(
        isinstance(cat_statement, dict)
        and cat_statement.get("declaration") == declaration
        and cat_statement.get("formal_type") == formal_type
        and cat_statement.get("formal_type_sha256") == asset_row.get("formal_type_sha256")
    )
    row: dict[str, Any] = {
        "catalog_binding": (
            {
                "catalog_record_sha256": sha256_bytes(canonical_json_bytes(cat)),
                "formal_statement_exact_match": catalog_matches,
                "origin_release": cat.get("origin_release"),
                "stage_claim_id": cat.get("stage_claim_id"),
                "variant_id": cat.get("variant_id"),
            }
            if isinstance(cat, dict)
            else None
        ),
        "curation_5_3": (
            {
                "disposition": curation_53[source_id].get("disposition"),
                "row_sha256": curation_53[source_id].get("row_sha256"),
                "target_s5_id": curation_53[source_id].get("target_s5_id"),
                "target_variant_id": curation_53[source_id].get("target_variant_id"),
            }
            if source_id in curation_53
            else None
        ),
        "curation_5_4": (
            {
                "disposition": curation_54[source_id].get("disposition"),
                "row_sha256": curation_54[source_id].get("row_sha256"),
                "target_s5_id": curation_54[source_id].get("target_s5_id"),
                "target_variant_id": curation_54[source_id].get("target_variant_id"),
            }
            if source_id in curation_54
            else None
        ),
        "declaration": declaration,
        "declaration_kind": asset_row.get("declaration_kind"),
        "exact_1000_plus_signal": exact_signals(asset_row, external_id),
        "exact_source_formal_identifier_match": matched_identifier,
        "formal_proof_state": asset_row.get("formal_proof_state"),
        "formal_type": formal_type,
        "formal_type_sha256": asset_row.get("formal_type_sha256"),
        "mathlib_source_record_id": source_id,
        "mathlib_source_row_sha256": asset_row_sha,
        "normalized_declaration_sha256": sha256_bytes(
            normalized_declaration(declaration).encode("utf-8")
        ),
        "normalized_formal_type_sha256": sha256_bytes(
            normalized_formal_type(formal_type).encode("utf-8")
        ),
        "proof_evidence_sha256": sha256_bytes(
            canonical_json_bytes(asset_row.get("proof_evidence"))
        ),
        "rights_sha256": sha256_bytes(canonical_json_bytes(asset_row.get("rights"))),
        "source_locator": asset_row.get("source"),
        "source_syntax_kind": asset_row.get("source_syntax_kind"),
    }
    row["row_sha256"] = hash_without(row, "row_sha256")
    return row


def accepted_binding_is_valid(binding: Mapping[str, Any]) -> bool:
    catalog_binding = binding.get("catalog_binding")
    curation_53 = binding.get("curation_5_3")
    return bool(
        binding.get("exact_source_formal_identifier_match") is True
        and binding.get("exact_1000_plus_signal")
        and binding.get("declaration_kind") == "theorem"
        and binding.get("source_syntax_kind") == "theorem"
        and binding.get("formal_proof_state") == "kernel_checked_sorry_free"
        and isinstance(catalog_binding, dict)
        and catalog_binding.get("formal_statement_exact_match") is True
        and isinstance(curation_53, dict)
        and curation_53.get("disposition") == "accepted_new_kernel_checked_theorem"
    )


def build_artifact() -> dict[str, Any]:
    source = load_json(SOURCE_PATH, SOURCE_SHA256)
    wikipedia = load_gzip_json(WIKIPEDIA_PATH, WIKIPEDIA_SHA256)
    natural = load_gzip_json(NATURALPROOFS_PATH, NATURALPROOFS_SHA256)
    mathlib = load_json(MATHLIB_PATH, MATHLIB_SHA256)
    curation_53_doc = load_json(CURATION_53_PATH, CURATION_53_SHA256)
    curation_54_doc = load_json(CURATION_54_PATH, CURATION_54_SHA256)
    catalog_doc = load_json(CATALOG_PATH, CATALOG_SHA256)
    manifest = load_json(MANIFEST_PATH, MANIFEST_SHA256)
    if source.get("content_digest_before_self_field") != SOURCE_CONTENT_DIGEST:
        raise CurationError("1000+ source content digest drifted")
    if wikipedia.get("content_digest_before_self_field") != WIKIPEDIA_CONTENT_DIGEST:
        raise CurationError("Wikipedia content digest drifted")
    if natural.get("content_digest_before_self_field") != NATURALPROOFS_CONTENT_DIGEST:
        raise CurationError("NaturalProofs join content digest drifted")
    if manifest.get("release_root_sha256") != RELEASE_ROOT:
        raise CurationError("release 5.4 root drifted")

    source_rows = source.get("records")
    mathlib_rows = mathlib.get("records")
    if not isinstance(source_rows, list) or len(source_rows) != 1_200:
        raise CurationError("1000+ source denominator drifted")
    if not isinstance(mathlib_rows, list) or len(mathlib_rows) != 1_500:
        raise CurationError("mathlib source denominator drifted")
    mathlib_by_declaration: dict[str, list[dict[str, Any]]] = defaultdict(list)
    mathlib_by_external: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in mathlib_rows:
        if not isinstance(row, dict) or not isinstance(row.get("declaration"), str):
            raise CurationError("invalid mathlib source row")
        mathlib_by_declaration[row["declaration"]].append(row)
        for signal in row.get("importance_signals", []):
            if isinstance(signal, dict) and signal.get("kind") == "mathlib_1000_theorems":
                external = signal.get("external_id")
                if isinstance(external, str):
                    mathlib_by_external[external].append(row)
    curation_53 = curation_index(curation_53_doc)
    curation_54 = curation_index(curation_54_doc)
    catalog = catalog_index(catalog_doc)
    wiki_identity = {
        row["source_record_id"]: row for row in wikipedia.get("identity_resolution", [])
    }
    natural_identity = {row["source_record_id"]: row for row in natural.get("matches", [])}

    ledger_rows: list[dict[str, Any]] = []
    dispositions: Counter[str] = Counter()
    for index, source_row in enumerate(source_rows):
        if source_row.get("selection_rank") != index + 1:
            raise CurationError("1000+ source ordering drifted")
        external_id = source_row["external_id"]
        formalized_mappings = [
            mapping
            for mapping in source_row["proof_assistant_mappings"]
            if mapping["status"] == "formalized"
        ]
        lean_identifiers = sorted(
            {
                identifier
                for mapping in formalized_mappings
                if mapping["assistant"] == "lean"
                for identifier in mapping["identifiers"]
            },
            key=lambda value: value.encode("utf-8"),
        )
        exact_asset_rows: list[dict[str, Any]] = []
        for identifier in lean_identifiers:
            exact_asset_rows.extend(mathlib_by_declaration.get(identifier, []))
        exact_asset_rows = sorted(
            {row["source_record_id"]: row for row in exact_asset_rows}.values(),
            key=lambda row: row["selection_rank"],
        )
        signal_rows = sorted(
            mathlib_by_external.get(external_id, []), key=lambda row: row["selection_rank"]
        )
        exact_bindings = [
            binding_payload(
                row,
                curation_53,
                curation_54,
                catalog,
                True,
                external_id,
            )
            for row in exact_asset_rows
        ]
        signal_only_bindings = [
            binding_payload(
                row,
                curation_53,
                curation_54,
                catalog,
                False,
                external_id,
            )
            for row in signal_rows
            if row["source_record_id"] not in {item["source_record_id"] for item in exact_asset_rows}
        ]

        if not source_row["proof_assistant_mappings"]:
            disposition = "pending_no_formalized_mapping"
            reason = "The identity has no proof-assistant mapping in the pinned 1000+ source."
        elif not formalized_mappings:
            disposition = "pending_statement_only_mapping"
            reason = "The only pinned proof-assistant mapping is statement-only."
        elif not exact_bindings:
            if signal_only_bindings:
                disposition = "pending_external_signal_identifier_drift"
                reason = (
                    "The mathlib docs signal names this identity, but its declaration differs "
                    "from the pinned 1000+ formalized identifier."
                )
            else:
                disposition = "pending_no_packaged_exact_statement"
                reason = (
                    "No selected mathlib statement row exactly matches a pinned 1000+ Lean "
                    "formalized identifier."
                )
        elif len(exact_bindings) > 1:
            disposition = "pending_multiple_exact_formal_bindings"
            reason = (
                "Multiple exact formal declarations map to one named theorem identity; "
                "equivalence/component semantics require review."
            )
        elif exact_bindings[0]["declaration_kind"] != "theorem" or exact_bindings[0][
            "source_syntax_kind"
        ] != "theorem":
            disposition = "rejected_nonliteral_lemma_binding"
            reason = "The only exact packaged declaration is a literal Lean lemma, not a theorem."
        elif not accepted_binding_is_valid(exact_bindings[0]):
            disposition = "pending_exact_binding_failed_current_catalog_gate"
            reason = "The exact theorem binding failed proof, curation, or current-catalog replay."
        else:
            disposition = "accepted_exact_single_literal_theorem_binding"
            reason = (
                "One exact pinned 1000+ Lean identifier binds one literal kernel-checked "
                "sorry-free theorem with an exact statement in release 5.4."
            )
        dispositions[disposition] += 1
        wiki_row = wiki_identity.get(source_row["source_record_id"])
        natural_row = natural_identity.get(source_row["source_record_id"])
        row: dict[str, Any] = {
            "accepted_binding": (
                exact_bindings[0]
                if disposition == "accepted_exact_single_literal_theorem_binding"
                else None
            ),
            "candidate_key": f"1000-plus:{external_id}",
            "disposition": disposition,
            "exact_mathlib_bindings": exact_bindings,
            "external_id": external_id,
            "grants_new_release_credit": False,
            "grants_quality_binding_credit": disposition
            == "accepted_exact_single_literal_theorem_binding",
            "lean_formalized_identifiers": lean_identifiers,
            "naturalproofs_evidence": (
                {
                    "candidate_count": len(natural_row["candidates"]),
                    "join_row_sha256": natural_row["row_sha256"],
                    "match_class": natural_row["match_class"],
                    "review_disposition": natural_row["review_disposition"],
                }
                if natural_row
                else None
            ),
            "reason": reason,
            "selection_rank": source_row["selection_rank"],
            "signal_only_mathlib_bindings": signal_only_bindings,
            "source_member": source_row["source"]["archive_member"],
            "source_member_sha256": source_row["source"]["member_sha256"],
            "source_record_id": source_row["source_record_id"],
            "source_row_sha256": source_row["row_sha256"],
            "title": source_row["title"],
            "wikipedia_evidence": (
                {
                    "resolved_page_ids": wiki_row["resolved_page_ids"],
                    "resolution_row_sha256": wiki_row["row_sha256"],
                    "unresolved_requested_titles": wiki_row["unresolved_requested_titles"],
                }
                if wiki_row
                else None
            ),
        }
        row["row_sha256"] = hash_without(row, "row_sha256")
        ledger_rows.append(row)

    observed = dict(dispositions)
    if observed != EXPECTED_COUNTS:
        raise CurationError(f"terminal disposition counts drifted: {observed}")
    accepted = [row for row in ledger_rows if row["grants_quality_binding_credit"]]
    for field in (
        "formal_type_sha256",
        "normalized_formal_type_sha256",
        "normalized_declaration_sha256",
        "mathlib_source_record_id",
    ):
        values = [row["accepted_binding"][field] for row in accepted]
        if len(values) != len(set(values)):
            raise CurationError(f"accepted set is not unique by {field}")

    input_rows = [
        ("1000_plus_source", SOURCE_PATH, SOURCE_SHA256),
        ("wikipedia_revision_extract", WIKIPEDIA_PATH, WIKIPEDIA_SHA256),
        ("naturalproofs_title_join", NATURALPROOFS_PATH, NATURALPROOFS_SHA256),
        ("mathlib_source", MATHLIB_PATH, MATHLIB_SHA256),
        ("mathlib_curation_5_3", CURATION_53_PATH, CURATION_53_SHA256),
        ("mathlib_curation_5_4", CURATION_54_PATH, CURATION_54_SHA256),
        ("release_5_4_catalog", CATALOG_PATH, CATALOG_SHA256),
        ("release_5_4_manifest", MANIFEST_PATH, MANIFEST_SHA256),
    ]
    artifact: dict[str, Any] = {
        "counts": {
            "accepted_quality_bindings": len(accepted),
            "candidate_identities": len(ledger_rows),
            "dispositions": EXPECTED_COUNTS,
            "naturalproofs_join_candidates": sum(
                row["naturalproofs_evidence"] is not None for row in ledger_rows
            ),
            "wikipedia_resolved_identities": sum(
                bool(row["wikipedia_evidence"]["resolved_page_ids"])
                for row in ledger_rows
                if row["wikipedia_evidence"] is not None
            ),
        },
        "decision_boundary": {
            "accepted_meaning": (
                "high-confidence named-theorem identity to one exact current formal statement"
            ),
            "candidate_pool_not_accepted_inventory": True,
            "frontier_status_claimed": False,
            "new_release_or_quota_credit_granted": False,
            "universal_importance_claimed": False,
        },
        "inputs": [
            {
                "label": label,
                "path": path.relative_to(REPO_ROOT).as_posix(),
                "sha256": digest,
                "size_bytes": path.stat().st_size,
            }
            for label, path, digest in input_rows
        ],
        "policy": {
            "acceptance_gates": [
                "pinned 1000+ identity has a formalized Lean identifier",
                "exact declaration identifier occurs in the pinned mathlib asset",
                "exact 1000+ external-id signal agrees",
                "exactly one packaged binding exists for the named identity",
                "declaration and source syntax are literal theorem",
                "proof state is kernel_checked_sorry_free",
                "5.3 curation accepted the exact source row",
                "release 5.4 contains an exact declaration/formal-type statement binding",
                "accepted identities are unique by exact and normalized formal type and declaration",
            ],
            "fuzzy_title_join_grants_credit": False,
            "multiple_declaration_family_grants_credit": False,
            "naturalproofs_title_join_grants_credit": False,
            "wikipedia_page_presence_grants_credit": False,
        },
        "records": ledger_rows,
        "release_context": {
            "current_release": "5.4",
            "release_root_sha256": RELEASE_ROOT,
            "release_was_modified": False,
        },
        "schema_version": SCHEMA_VERSION,
        "set_digests": {
            "accepted_external_ids_sha256": set_digest(row["external_id"] for row in accepted),
            "accepted_formal_types_sha256": set_digest(
                row["accepted_binding"]["formal_type_sha256"] for row in accepted
            ),
            "accepted_mathlib_source_ids_sha256": set_digest(
                row["accepted_binding"]["mathlib_source_record_id"] for row in accepted
            ),
            "candidate_external_ids_sha256": set_digest(
                row["external_id"] for row in ledger_rows
            ),
        },
    }
    artifact["authority_sha256"] = hash_without(artifact, "authority_sha256")
    return artifact


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(payload)
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        artifact = build_artifact()
        payload = encoded_document(artifact)
        if args.check:
            if args.output.resolve().read_bytes() != payload:
                raise CurationError(f"{args.output} differs from deterministic rebuild")
            print(
                f"1000+ curation rebuild PASS: candidates=1200 accepted=125 "
                f"authority={artifact['authority_sha256']}"
            )
        else:
            atomic_write(args.output.resolve(), payload)
            print(
                f"wrote {args.output}: candidates=1200 accepted=125 "
                f"sha256={sha256_bytes(payload)} authority={artifact['authority_sha256']}"
            )
    except (CurationError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"1000+ curation build failed: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
