#!/usr/bin/env python3
"""Independent replay of the 1,000-row strict research-conjecture inventory."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile
from typing import Any, Iterable, Mapping


CATALOG = Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json")
STRICT = Path("Docs/catalog/v5/releases/5.4/Strict_Conjecture_Ledger.json")
MANIFEST = Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json")
FORMAL_ARCHIVE = Path("Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz")
OPEN_SOURCE = Path("Docs/catalog/v5/sources/openconjecture-fa03d85-cc-by-real-conf090.jsonl")
OPEN_CURATION = Path("Docs/catalog/v5/curation/OpenConjecture_Curation_v5_2.json")
LEDGER = Path("Docs/catalog/v5/curation/conjecture_quality_v5_5/strict-research-inventory-1000.json")
EXPECTED_SHA = {
    CATALOG: "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709",
    STRICT: "52ba1ccf06462741bcc48028fb121e5e30d1e7b56128cfeb910dc56a2e1a83a3",
    MANIFEST: "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9",
    FORMAL_ARCHIVE: "51535f4755574d97672515a75b8b076065aba2c0d79631e99fa57719f484dcc8",
    OPEN_SOURCE: "8a698e3af53ca0605a2a8ecd2e3a9944ad84157440a86f3c319effaf9792c6ce",
    OPEN_CURATION: "9bd937d4f0949d001869b5ed69387350078f42d042847251daa6b7f170dc25a7",
    LEDGER: "9a76a5632d8b99a5034adb8a0f2e481f2bb642903edea475049e9d477796d80c",
}
AUTHORITY = "0bc736749dbf9d823bd2b2c66066171c71e0f7369cd1c25d75a653f3f715a1f8"
FORMAL_SOURCE_ID = "SRC-MATH-V5-FORMAL-CONJECTURES-2270D31E"
OPEN_SOURCE_ID = "SRC-MATH-V5-OPENCONJECTURE-FA03D85"
REVISION = "2270d31e8dd611521f979de6d86da364930b7669"


class AuditError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def digest_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def without(value: Mapping[str, Any], field: str) -> str:
    return digest(canonical({key: item for key, item in value.items() if key != field}))


def digest_set(values: Iterable[str]) -> str:
    return digest(canonical(sorted(values)))


def reject_constant(token: str) -> None:
    raise AuditError(f"non-finite JSON token: {token}")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json(payload: bytes, label: str) -> Any:
    try:
        return json.loads(payload, object_pairs_hook=reject_duplicate_keys, parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditError(f"invalid {label}: {error}") from error


def resolved(root: Path, relative: Path) -> Path:
    path = (root / relative).resolve(strict=True)
    require(path.is_relative_to(root), f"path escapes repository: {relative}")
    require(path.is_file() and not path.is_symlink(), f"input is not a regular repository file: {relative}")
    require(digest_file(path) == EXPECTED_SHA[relative], f"input digest drifted: {relative}")
    return path


def load_object(root: Path, relative: Path) -> dict[str, Any]:
    document = strict_json(resolved(root, relative).read_bytes(), relative.as_posix())
    require(isinstance(document, dict), f"root is not object: {relative}")
    return document


def open_rows(root: Path) -> list[dict[str, Any]]:
    payload = resolved(root, OPEN_SOURCE).read_bytes()
    require(payload.endswith(b"\n"), "OpenConjecture JSONL lacks final newline")
    result = [strict_json(line, "OpenConjecture JSONL row") for line in payload.splitlines()]
    require(len(result) == 889 and all(isinstance(row, dict) for row in result), "OpenConjecture source denominator drifted")
    return result


def formal_member_map(root: Path) -> dict[str, bytes]:
    prefix = f"formal-conjectures-{REVISION}/"
    result: dict[str, bytes] = {}
    names: set[str] = set()
    with tarfile.open(resolved(root, FORMAL_ARCHIVE), "r:gz") as archive:
        for member in archive.getmembers():
            pure = PurePosixPath(member.name)
            require(member.name not in names and not pure.is_absolute() and ".." not in pure.parts, "unsafe or duplicate Formal Conjectures member")
            names.add(member.name)
            require(not member.issym() and not member.islnk(), "Formal Conjectures link member")
            if not member.isfile():
                continue
            require(member.name.startswith(prefix), "Formal Conjectures prefix drifted")
            handle = archive.extractfile(member)
            require(handle is not None, "Formal Conjectures member extraction failed")
            data = handle.read()
            require(len(data) == member.size, "Formal Conjectures member size mismatch")
            result[member.name[len(prefix) :]] = data
    require(len(result) > 1_000, "Formal Conjectures member denominator implausible")
    return result


def exact_integer(value: Any, expected: int, label: str) -> None:
    require(type(value) is int and value == expected, f"{label} must be integer {expected}")


def verify(repo_root: Path) -> dict[str, int]:
    root = repo_root.resolve(strict=True)
    catalog = load_object(root, CATALOG)
    strict = load_object(root, STRICT)
    manifest = load_object(root, MANIFEST)
    curation = load_object(root, OPEN_CURATION)
    ledger_path = resolved(root, LEDGER)
    ledger_payload = ledger_path.read_bytes()
    ledger = strict_json(ledger_payload, "strict research inventory")
    require(isinstance(ledger, dict), "strict research inventory root is not object")
    require(ledger_payload == canonical(ledger) + b"\n", "strict research inventory is not canonical JSON")
    require(ledger.get("authority_sha256") == AUTHORITY == without(ledger, "authority_sha256"), "strict research inventory authority mismatch")
    require(ledger.get("schema_version") == "awesome-theorems/strict-conjecture-research-inventory/5.5", "strict research inventory schema mismatch")
    require(ledger.get("review_as_of") == "2026-08-10", "strict research inventory date mismatch")
    scope = ledger.get("scope")
    require(
        scope
        == {
            "kind": "quality qualification of the 1,000 effective strict conjecture identities in release 5.4",
            "qualification_union": "important_or_frontier_research_conjecture under explicit source-qualified operational gates",
            "not_an_independent_current_literature_status_survey": True,
            "not_a_universal_importance_ranking": True,
            "not_a_release_append": True,
        },
        "strict research inventory scope drifted",
    )
    require(
        ledger.get("inputs")
        == {relative.as_posix(): {"sha256": EXPECTED_SHA[relative]} for relative in sorted(EXPECTED_SHA, key=lambda path: path.as_posix()) if relative != LEDGER},
        "strict research inventory input bindings drifted",
    )

    require(manifest.get("release") == "5.4", "release binding drifted")
    exact_integer(manifest.get("counts", {}).get("effective_strict_conjecture_credits"), 1_000, "manifest strict credits")
    exact_integer(manifest.get("counts", {}).get("cumulative_theorems"), 2_500, "manifest theorems")
    require(strict.get("authority_sha256") == without(strict, "authority_sha256"), "parent strict ledger seal mismatch")
    strict_credits = strict.get("strict_credits")
    require(isinstance(strict_credits, list) and len(strict_credits) == 1_000, "parent strict credit denominator drifted")
    strict_by_id: dict[str, dict[str, Any]] = {}
    for item in strict_credits:
        require(isinstance(item, dict) and item.get("row_sha256") == without(item, "row_sha256"), "parent strict row hash mismatch")
        require(item.get("grants_strict_conjecture_credit") is True, "parent strict row does not grant credit")
        stage_id = item.get("stage_claim_id")
        require(isinstance(stage_id, str) and stage_id not in strict_by_id, "parent strict stage id collision")
        strict_by_id[stage_id] = item

    catalog_rows = catalog.get("records")
    require(isinstance(catalog_rows, list) and len(catalog_rows) == 4_100, "catalog denominator drifted")
    catalog_by_id = {item.get("stage_claim_id"): item for item in catalog_rows if isinstance(item, dict)}
    require(len(catalog_by_id) == 4_100 and None not in catalog_by_id, "catalog stage id collision")
    require(curation.get("authority_sha256") == without(curation, "authority_sha256"), "OpenConjecture curation seal mismatch")
    accepted = [item for item in curation.get("candidate_dispositions", []) if isinstance(item, dict) and item.get("disposition") == "accepted_new_strict_open_claim"]
    require(len(accepted) == 600, "OpenConjecture accepted denominator drifted")
    accepted_by_id = {item.get("target_s5_id"): item for item in accepted}
    require(len(accepted_by_id) == 600 and None not in accepted_by_id, "OpenConjecture accepted target collision")
    source_rows = open_rows(root)
    formal_files = formal_member_map(root)

    rows = ledger.get("records")
    require(isinstance(rows, list) and len(rows) == 1_000, "quality ledger denominator drifted")
    require([row.get("stage_claim_id") for row in rows] == sorted(strict_by_id), "quality ledger ID coverage/order mismatch")
    sources: Counter[str] = Counter()
    tiers: Counter[str] = Counter()
    semantics: list[str] = []
    row_hashes: list[str] = []
    for row in rows:
        require(isinstance(row, dict) and row.get("row_sha256") == without(row, "row_sha256"), "quality row hash mismatch")
        stage_id = row["stage_claim_id"]
        strict_row = strict_by_id[stage_id]
        claim = catalog_by_id.get(stage_id)
        require(claim is not None, f"catalog claim missing: {stage_id}")
        require(row.get("strict_credit_row_sha256") == strict_row.get("row_sha256"), f"strict row binding mismatch: {stage_id}")
        require(row.get("variant_id") == strict_row.get("variant_id") == claim.get("variant_id"), f"variant binding mismatch: {stage_id}")
        require(row.get("family_id") == claim.get("family_id") and row.get("origin_release") == claim.get("origin_release"), f"identity binding mismatch: {stage_id}")
        require(claim.get("claim_kind") == claim.get("current_claim_kind") == "conjecture", f"claim kind mismatch: {stage_id}")
        require(claim.get("material_status") == "open" and claim.get("truth_apt") is True and claim.get("atomicity") == "atomic", f"claim status/truth/atomicity mismatch: {stage_id}")
        require(row.get("statement_sha256") == claim.get("mathematical_statement", {}).get("statement_sha256"), f"statement binding mismatch: {stage_id}")
        require(row.get("grants_existing_important_or_frontier_research_conjecture_credit") is True, f"research quality credit absent: {stage_id}")
        require(row.get("grants_new_conjecture_identity_credit") is False, f"new conjecture credit escalation: {stage_id}")
        require(row.get("independent_current_literature_status_reviewed") is False, f"independent status overclaim: {stage_id}")
        require(row.get("status_boundary") == "source-curated open status at pinned source; not an independent current-literature survey", f"status boundary drifted: {stage_id}")
        source_id = row.get("source_id")
        require(source_id == claim.get("source_id"), f"source ID mismatch: {stage_id}")
        evidence = row.get("quality_evidence")
        require(isinstance(evidence, dict), f"quality evidence missing: {stage_id}")
        if source_id == FORMAL_SOURCE_ID:
            semantic = f"formal-conjectures-semantic/{claim.get('semantic_payload_sha256')}"
            require(row.get("source_class") == "formal_conjectures_research_open", f"Formal source class mismatch: {stage_id}")
            require(row.get("quality_tier") == "source_curated_formal_conjectures_open_frontier", f"Formal quality tier mismatch: {stage_id}")
            require(claim.get("origin_release") == strict_row.get("origin_release") == "5.0", f"Formal origin mismatch: {stage_id}")
            require(claim.get("raw_category") == claim.get("raw_status") == "research open", f"Formal category mismatch: {stage_id}")
            require(claim.get("frontier", {}).get("class") == "source_asserted_open_frontier", f"Formal frontier mismatch: {stage_id}")
            require(claim.get("importance", {}).get("tier") == "unranked_research_level", f"Formal importance boundary mismatch: {stage_id}")
            locator = claim.get("locator")
            require(isinstance(locator, dict) and locator.get("revision") == REVISION, f"Formal locator mismatch: {stage_id}")
            member = formal_files.get(locator.get("member_path"))
            require(member is not None and digest(member) == locator.get("file_sha256"), f"Formal member mismatch: {stage_id}")
            start, end = locator.get("byte_start"), locator.get("byte_end_exclusive")
            require(type(start) is int and type(end) is int and 0 <= start < end <= len(member), f"Formal byte range mismatch: {stage_id}")
            require(digest(member[start:end]) == locator.get("raw_block_sha256"), f"Formal raw block mismatch: {stage_id}")
            require(claim.get("formal_declaration", "").encode("utf-8") in member[start:end], f"Formal declaration missing from block: {stage_id}")
            require(
                evidence
                == {
                    "exact_formal_type_sha256": claim["formal_type_sha256"],
                    "source_member_path": locator["member_path"],
                    "source_member_sha256": locator["file_sha256"],
                    "raw_block_sha256": locator["raw_block_sha256"],
                    "source_category": "research open",
                    "status_evidence_level": "source_asserted_as_of",
                    "rights_status": claim.get("rights", {}).get("status"),
                },
                f"Formal quality evidence drifted: {stage_id}",
            )
        elif source_id == OPEN_SOURCE_ID:
            semantic = claim.get("semantic_key")
            curation_row = accepted_by_id.get(stage_id)
            require(curation_row is not None and curation_row.get("row_sha256") == without(curation_row, "row_sha256"), f"OpenConjecture curation binding missing: {stage_id}")
            importance = curation_row.get("importance_assessment")
            require(importance in {"high", "medium"}, f"OpenConjecture importance invalid: {stage_id}")
            require(row.get("source_class") == "openconjecture_author_labeled_research", f"OpenConjecture source class mismatch: {stage_id}")
            require(row.get("quality_tier") == f"source_curated_{importance}_research_conjecture", f"OpenConjecture tier mismatch: {stage_id}")
            review_codes = curation_row.get("review_reason_codes")
            require(isinstance(review_codes, list) and "truth_apt" in review_codes and any(code.startswith("author_") or code.startswith("current_author_") for code in review_codes), f"OpenConjecture author/truth review missing: {stage_id}")
            line = claim.get("source_locator", {}).get("eligible_pool_line_number")
            require(type(line) is int and 1 <= line <= 889, f"OpenConjecture source line invalid: {stage_id}")
            source = source_rows[line - 1]
            source_hash = digest(canonical(source))
            require(source_hash == curation_row.get("source_record_sha256") == claim.get("provenance", {}).get("source_record_sha256"), f"OpenConjecture source hash mismatch: {stage_id}")
            require(source.get("body_tex") == claim.get("mathematical_statement", {}).get("body_tex"), f"OpenConjecture exact body mismatch: {stage_id}")
            require(source.get("latest_label") == "real_open_conjecture" and source.get("latest_label_confidence", 0) >= 0.9, f"OpenConjecture open-label gate failed: {stage_id}")
            require(source.get("publication_text_allowed") is True and source.get("normalized_license_url") == "https://creativecommons.org/licenses/by/4.0/", f"OpenConjecture rights gate failed: {stage_id}")
            require(
                evidence
                == {
                    "curation_row_sha256": curation_row["row_sha256"],
                    "eligible_pool_line_number": line,
                    "source_record_sha256": source_hash,
                    "body_tex_sha256": curation_row["body_tex_sha256"],
                    "author_labeled_conjecture_reviewed": True,
                    "curation_review_reason_codes": review_codes,
                    "source_open_label": "real_open_conjecture",
                    "source_open_label_confidence": source["latest_label_confidence"],
                    "interestingness_score": curation_row["interestingness_score"],
                    "importance_assessment": importance,
                    "rights_spdx": "CC-BY-4.0",
                },
                f"OpenConjecture quality evidence drifted: {stage_id}",
            )
        else:
            raise AuditError(f"unexpected strict source: {stage_id} / {source_id}")
        require(row.get("semantic_key") == semantic == strict_row.get("semantic_key"), f"semantic binding mismatch: {stage_id}")
        sources[row["source_class"]] += 1
        tiers[row["quality_tier"]] += 1
        semantics.append(semantic)
        row_hashes.append(row["row_sha256"])

    require(sources == Counter({"formal_conjectures_research_open": 400, "openconjecture_author_labeled_research": 600}), "source class counts drifted")
    counts = ledger.get("counts")
    require(isinstance(counts, dict), "quality ledger counts missing")
    exact_integer(counts.get("existing_strict_research_conjecture_credits"), 1_000, "existing research credits")
    exact_integer(counts.get("new_conjecture_identity_credits"), 0, "new conjecture credits")
    exact_integer(counts.get("independent_current_literature_status_reviews"), 0, "independent current status reviews")
    require(counts.get("by_source_class") == dict(sorted(sources.items())), "source class summary drifted")
    require(counts.get("by_quality_tier") == dict(sorted(tiers.items())), "quality tier summary drifted")
    require(
        ledger.get("set_digests")
        == {
            "stage_claim_ids_sha256": digest_set(strict_by_id),
            "semantic_keys_sha256": digest_set(semantics),
            "row_sha256_set_sha256": digest_set(row_hashes),
        },
        "quality ledger set digests drifted",
    )
    return {"formal_frontier": sources["formal_conjectures_research_open"], "openconjecture": sources["openconjecture_author_labeled_research"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[4])
    args = parser.parse_args()
    try:
        result = verify(args.repo_root)
    except (AuditError, OSError, tarfile.TarError, KeyError, TypeError) as error:
        print(f"FAIL strict conjecture research inventory: {error}")
        return 1
    print(
        "PASS strict conjecture research inventory strict_research=1000 "
        f"formal_frontier={result['formal_frontier']} openconjecture={result['openconjecture']} "
        f"new=0 independent_current_status=0 authority={AUTHORITY}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
