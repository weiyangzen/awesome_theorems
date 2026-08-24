#!/usr/bin/env python3
"""Build the 1,000-row important-or-frontier strict conjecture ledger."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[4]
CATALOG_REL = Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json")
STRICT_REL = Path("Docs/catalog/v5/releases/5.4/Strict_Conjecture_Ledger.json")
MANIFEST_REL = Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json")
FORMAL_ARCHIVE_REL = Path("Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz")
OPEN_SOURCE_REL = Path("Docs/catalog/v5/sources/openconjecture-fa03d85-cc-by-real-conf090.jsonl")
OPEN_CURATION_REL = Path("Docs/catalog/v5/curation/OpenConjecture_Curation_v5_2.json")
OUTPUT_REL = Path("Docs/catalog/v5/curation/conjecture_quality_v5_5/strict-research-inventory-1000.json")
EXPECTED_SHA256 = {
    CATALOG_REL: "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709",
    STRICT_REL: "52ba1ccf06462741bcc48028fb121e5e30d1e7b56128cfeb910dc56a2e1a83a3",
    MANIFEST_REL: "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9",
    FORMAL_ARCHIVE_REL: "51535f4755574d97672515a75b8b076065aba2c0d79631e99fa57719f484dcc8",
    OPEN_SOURCE_REL: "8a698e3af53ca0605a2a8ecd2e3a9944ad84157440a86f3c319effaf9792c6ce",
    OPEN_CURATION_REL: "9bd937d4f0949d001869b5ed69387350078f42d042847251daa6b7f170dc25a7",
}
FORMAL_SOURCE_ID = "SRC-MATH-V5-FORMAL-CONJECTURES-2270D31E"
OPEN_SOURCE_ID = "SRC-MATH-V5-OPENCONJECTURE-FA03D85"
FORMAL_REVISION = "2270d31e8dd611521f979de6d86da364930b7669"


class BuildError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    ignored = set(fields)
    return sha(canonical({key: item for key, item in value.items() if key not in ignored}))


def set_digest(values: Iterable[str]) -> str:
    return sha(canonical(sorted(values)))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


def load_json(relative: Path) -> dict[str, Any]:
    path = ROOT / relative
    require(file_sha(path) == EXPECTED_SHA256[relative], f"input digest drifted: {relative}")
    result = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(result, dict), f"input root is not an object: {relative}")
    return result


def load_open_source() -> list[dict[str, Any]]:
    path = ROOT / OPEN_SOURCE_REL
    require(file_sha(path) == EXPECTED_SHA256[OPEN_SOURCE_REL], "OpenConjecture source digest drifted")
    payload = path.read_bytes()
    require(payload.endswith(b"\n"), "OpenConjecture source lacks final newline")
    rows = [json.loads(line) for line in payload.decode("utf-8").splitlines()]
    require(len(rows) == 889 and all(isinstance(row, dict) for row in rows), "OpenConjecture source denominator drifted")
    return rows


def safe_tar_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and ".." not in path.parts


def load_formal_files() -> dict[str, bytes]:
    archive_path = ROOT / FORMAL_ARCHIVE_REL
    require(file_sha(archive_path) == EXPECTED_SHA256[FORMAL_ARCHIVE_REL], "Formal Conjectures archive digest drifted")
    files: dict[str, bytes] = {}
    prefix = f"formal-conjectures-{FORMAL_REVISION}/"
    with tarfile.open(archive_path, "r:gz") as archive:
        names: set[str] = set()
        for member in archive.getmembers():
            require(member.name not in names and safe_tar_member(member.name), "unsafe or duplicate Formal Conjectures tar member")
            names.add(member.name)
            require(not member.issym() and not member.islnk(), "linked Formal Conjectures tar member")
            if not member.isfile():
                continue
            stream = archive.extractfile(member)
            require(stream is not None, f"cannot extract tar member: {member.name}")
            data = stream.read()
            require(len(data) == member.size, f"tar member size mismatch: {member.name}")
            require(member.name.startswith(prefix), f"unexpected archive prefix: {member.name}")
            files[member.name[len(prefix) :]] = data
    require(len(files) > 1_000, "Formal Conjectures archive file denominator implausible")
    return files


def build() -> dict[str, Any]:
    catalog = load_json(CATALOG_REL)
    strict = load_json(STRICT_REL)
    manifest = load_json(MANIFEST_REL)
    curation = load_json(OPEN_CURATION_REL)
    open_source = load_open_source()
    formal_files = load_formal_files()

    require(manifest.get("release") == "5.4", "manifest release drifted")
    require(manifest.get("counts", {}).get("cumulative_theorems") == 2_500, "manifest theorem count drifted")
    require(manifest.get("counts", {}).get("effective_strict_conjecture_credits") == 1_000, "manifest strict count drifted")
    require(strict.get("authority_sha256") == hash_without(strict, "authority_sha256"), "strict ledger seal drifted")
    require(curation.get("authority_sha256") == hash_without(curation, "authority_sha256"), "OpenConjecture curation seal drifted")

    catalog_rows = catalog.get("records")
    require(isinstance(catalog_rows, list) and len(catalog_rows) == 4_100, "catalog denominator drifted")
    catalog_by_id = {row.get("stage_claim_id"): row for row in catalog_rows if isinstance(row, dict)}
    require(len(catalog_by_id) == 4_100 and None not in catalog_by_id, "catalog identity collision")
    strict_rows = strict.get("strict_credits")
    require(isinstance(strict_rows, list) and len(strict_rows) == 1_000, "strict credit denominator drifted")
    require(len({row.get("stage_claim_id") for row in strict_rows}) == 1_000, "strict identity collision")
    require(all(row.get("row_sha256") == hash_without(row, "row_sha256") for row in strict_rows), "strict row digest mismatch")
    require(all(row.get("grants_strict_conjecture_credit") is True for row in strict_rows), "strict row lacks credit")

    curation_rows = curation.get("candidate_dispositions")
    require(isinstance(curation_rows, list), "OpenConjecture curation rows missing")
    accepted = [row for row in curation_rows if row.get("disposition") == "accepted_new_strict_open_claim"]
    require(len(accepted) == 600, "OpenConjecture accepted denominator drifted")
    accepted_by_stage = {row.get("target_s5_id"): row for row in accepted}
    require(len(accepted_by_stage) == 600 and None not in accepted_by_stage, "OpenConjecture target collision")
    require(all(row.get("row_sha256") == hash_without(row, "row_sha256") for row in accepted), "OpenConjecture curation row digest mismatch")

    output_rows: list[dict[str, Any]] = []
    source_classes: Counter[str] = Counter()
    tiers: Counter[str] = Counter()
    for strict_row in strict_rows:
        stage_id = strict_row["stage_claim_id"]
        claim = catalog_by_id.get(stage_id)
        require(claim is not None, f"strict claim absent from catalog: {stage_id}")
        require(claim.get("variant_id") == strict_row.get("variant_id"), f"strict variant mismatch: {stage_id}")
        if claim.get("source_id") == FORMAL_SOURCE_ID:
            claim_semantic_key = f"formal-conjectures-semantic/{claim.get('semantic_payload_sha256')}"
        else:
            claim_semantic_key = claim.get("semantic_key")
        require(claim_semantic_key == strict_row.get("semantic_key"), f"strict semantic mismatch: {stage_id}")
        require(claim.get("claim_kind") == "conjecture" and claim.get("current_claim_kind") == "conjecture", f"strict claim kind mismatch: {stage_id}")
        require(claim.get("material_status") == "open" and claim.get("lifecycle") == "active", f"strict material status mismatch: {stage_id}")
        require(claim.get("truth_apt") is True and claim.get("atomicity") == "atomic", f"strict truth/atomicity mismatch: {stage_id}")
        require(claim.get("mathematical_statement", {}).get("statement_sha256") == claim.get("statement_sha256", claim.get("mathematical_statement", {}).get("statement_sha256")), f"statement digest field mismatch: {stage_id}")

        source_id = claim.get("source_id")
        evidence: dict[str, Any]
        if source_id == FORMAL_SOURCE_ID:
            require(claim.get("origin_release") == "5.0" and strict_row.get("origin_release") == "5.0", f"Formal origin mismatch: {stage_id}")
            require(claim.get("raw_category") == "research open" and claim.get("raw_status") == "research open", f"Formal source category mismatch: {stage_id}")
            require(claim.get("frontier", {}).get("class") == "source_asserted_open_frontier", f"Formal frontier class mismatch: {stage_id}")
            require(claim.get("importance", {}).get("tier") == "unranked_research_level", f"Formal importance boundary mismatch: {stage_id}")
            require(claim.get("formal_shape") == "direct_prop" and claim.get("formal_type_sha256") == sha(claim["formal_type"].encode("utf-8")), f"Formal exact proposition mismatch: {stage_id}")
            locator = claim.get("locator")
            require(isinstance(locator, dict) and locator.get("revision") == FORMAL_REVISION, f"Formal locator mismatch: {stage_id}")
            member_path = locator.get("member_path")
            require(isinstance(member_path, str) and member_path in formal_files, f"Formal member missing: {stage_id}")
            member_bytes = formal_files[member_path]
            require(sha(member_bytes) == locator.get("file_sha256"), f"Formal member digest mismatch: {stage_id}")
            start = locator.get("byte_start")
            end = locator.get("byte_end_exclusive")
            require(type(start) is int and type(end) is int and 0 <= start < end <= len(member_bytes), f"Formal byte range invalid: {stage_id}")
            block = member_bytes[start:end]
            require(sha(block) == locator.get("raw_block_sha256"), f"Formal block digest mismatch: {stage_id}")
            require(claim.get("formal_declaration", "").encode("utf-8") in block, f"Formal declaration absent from block: {stage_id}")
            quality_tier = "source_curated_formal_conjectures_open_frontier"
            source_class = "formal_conjectures_research_open"
            evidence = {
                "exact_formal_type_sha256": claim["formal_type_sha256"],
                "source_member_path": member_path,
                "source_member_sha256": locator["file_sha256"],
                "raw_block_sha256": locator["raw_block_sha256"],
                "source_category": "research open",
                "status_evidence_level": "source_asserted_as_of",
                "rights_status": claim.get("rights", {}).get("status"),
            }
        elif source_id == OPEN_SOURCE_ID:
            require(claim.get("origin_release") == "5.2" and strict_row.get("origin_release") == "5.2", f"OpenConjecture origin mismatch: {stage_id}")
            curation_row = accepted_by_stage.get(stage_id)
            require(curation_row is not None, f"OpenConjecture curation row missing: {stage_id}")
            require(curation_row.get("target_variant_id") == claim.get("variant_id"), f"OpenConjecture variant mismatch: {stage_id}")
            require(curation_row.get("semantic_key") == claim.get("semantic_key"), f"OpenConjecture semantic mismatch: {stage_id}")
            require(curation_row.get("grants_catalog_entry") is True and curation_row.get("grants_strict_conjecture_credit") is True, f"OpenConjecture curation credit absent: {stage_id}")
            require(curation_row.get("importance_assessment") in {"high", "medium"}, f"OpenConjecture importance tier invalid: {stage_id}")
            review_codes = curation_row.get("review_reason_codes", [])
            require(
                isinstance(review_codes, list)
                and "truth_apt" in review_codes
                and any(code.startswith("author_") or code.startswith("current_author_") for code in review_codes),
                f"OpenConjecture author/truth review gates drifted: {stage_id}",
            )
            locator = claim.get("source_locator")
            line_number = locator.get("eligible_pool_line_number") if isinstance(locator, dict) else None
            require(type(line_number) is int and 1 <= line_number <= len(open_source), f"OpenConjecture line locator invalid: {stage_id}")
            source_row = open_source[line_number - 1]
            source_record_sha = sha(canonical(source_row))
            require(source_record_sha == claim.get("provenance", {}).get("source_record_sha256") == curation_row.get("source_record_sha256"), f"OpenConjecture source row binding mismatch: {stage_id}")
            require(source_row.get("content_hash") == claim.get("source_block", {}).get("content_hash") == curation_row.get("content_hash"), f"OpenConjecture content identity mismatch: {stage_id}")
            require(source_row.get("body_tex") == claim.get("mathematical_statement", {}).get("body_tex"), f"OpenConjecture exact body mismatch: {stage_id}")
            require(sha(source_row["body_tex"].encode("utf-8")) == curation_row.get("body_tex_sha256"), f"OpenConjecture body digest mismatch: {stage_id}")
            require(source_row.get("latest_label") == "real_open_conjecture" and source_row.get("latest_label_confidence", 0) >= 0.9, f"OpenConjecture source label gate failed: {stage_id}")
            require(source_row.get("publication_text_allowed") is True and source_row.get("normalized_license_url") == "https://creativecommons.org/licenses/by/4.0/", f"OpenConjecture rights gate failed: {stage_id}")
            importance = curation_row["importance_assessment"]
            quality_tier = f"source_curated_{importance}_research_conjecture"
            source_class = "openconjecture_author_labeled_research"
            evidence = {
                "curation_row_sha256": curation_row["row_sha256"],
                "eligible_pool_line_number": line_number,
                "source_record_sha256": source_record_sha,
                "body_tex_sha256": curation_row["body_tex_sha256"],
                "author_labeled_conjecture_reviewed": True,
                "curation_review_reason_codes": review_codes,
                "source_open_label": "real_open_conjecture",
                "source_open_label_confidence": source_row["latest_label_confidence"],
                "interestingness_score": curation_row["interestingness_score"],
                "importance_assessment": importance,
                "rights_spdx": "CC-BY-4.0",
            }
        else:
            raise BuildError(f"unexpected strict source: {stage_id} / {source_id}")

        source_classes[source_class] += 1
        tiers[quality_tier] += 1
        row: dict[str, Any] = {
            "stage_claim_id": stage_id,
            "variant_id": claim["variant_id"],
            "family_id": claim["family_id"],
            "origin_release": claim["origin_release"],
            "source_id": source_id,
            "source_class": source_class,
            "semantic_key": claim_semantic_key,
            "statement_sha256": claim["mathematical_statement"]["statement_sha256"],
            "strict_credit_row_sha256": strict_row["row_sha256"],
            "quality_tier": quality_tier,
            "quality_evidence": evidence,
            "grants_existing_important_or_frontier_research_conjecture_credit": True,
            "grants_new_conjecture_identity_credit": False,
            "independent_current_literature_status_reviewed": False,
            "status_boundary": "source-curated open status at pinned source; not an independent current-literature survey",
        }
        row["row_sha256"] = hash_without(row, "row_sha256")
        output_rows.append(row)

    output_rows.sort(key=lambda row: row["stage_claim_id"])
    require(source_classes == Counter({"formal_conjectures_research_open": 400, "openconjecture_author_labeled_research": 600}), "strict source partition drifted")
    result: dict[str, Any] = {
        "schema_version": "awesome-theorems/strict-conjecture-research-inventory/5.5",
        "review_as_of": "2026-08-10",
        "scope": {
            "kind": "quality qualification of the 1,000 effective strict conjecture identities in release 5.4",
            "qualification_union": "important_or_frontier_research_conjecture under explicit source-qualified operational gates",
            "not_an_independent_current_literature_status_survey": True,
            "not_a_universal_importance_ranking": True,
            "not_a_release_append": True,
        },
        "inputs": {
            relative.as_posix(): {"sha256": expected}
            for relative, expected in sorted(EXPECTED_SHA256.items(), key=lambda item: item[0].as_posix())
        },
        "counts": {
            "existing_strict_research_conjecture_credits": len(output_rows),
            "new_conjecture_identity_credits": 0,
            "independent_current_literature_status_reviews": 0,
            "by_source_class": dict(sorted(source_classes.items())),
            "by_quality_tier": dict(sorted(tiers.items())),
        },
        "set_digests": {
            "stage_claim_ids_sha256": set_digest(row["stage_claim_id"] for row in output_rows),
            "semantic_keys_sha256": set_digest(row["semantic_key"] for row in output_rows),
            "row_sha256_set_sha256": set_digest(row["row_sha256"] for row in output_rows),
        },
        "records": output_rows,
    }
    result["authority_sha256"] = hash_without(result, "authority_sha256")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    document = build()
    output = ROOT / OUTPUT_REL
    payload = canonical(document) + b"\n"
    if args.write:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(payload)
        print(f"wrote {OUTPUT_REL} strict_research=1000 new=0 authority={document['authority_sha256']}")
        return 0
    require(output.is_file() and output.read_bytes() == payload, "output is not a deterministic rebuild")
    print(f"PASS strict conjecture research inventory strict_research=1000 new=0 authority={document['authority_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
