#!/usr/bin/env python3
"""Build the 117-row non-Erdos supplemental frontier-review queue.

This is the exact set difference between the 371 release-5.4 non-Erdos
``research solved`` theorem rows and the frozen 254-row primary queue.  Every
row remains candidate-only and receives no frontier or new-theorem credit.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import re
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[4]
CATALOG = ROOT / "Docs/catalog/v5/releases/5.4/Claim_Catalog.json"
MANIFEST = ROOT / "Docs/catalog/v5/releases/5.4/Release_Manifest.json"
PRIMARY = ROOT / "Docs/catalog/v5/curation/Frontier_Theorem_Candidate_Queue_v5_5.json"
OUTPUT = ROOT / "Docs/catalog/v5/curation/Frontier_Theorem_Supplemental_Candidate_Queue_v5_5.json"
CATALOG_SHA = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
MANIFEST_SHA = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
RELEASE_ROOT = "c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813"
PRIMARY_SHA = "b3b28b81cfcd9fe4dbf002d2bb8d9bedaa8094656396e224abb5c6221530b2fc"
PRIMARY_AUTHORITY = "375ca73546293f74fdc966209d4be0d184ad5e28273c70aecc7a12a601548133"
SOURCE_COMMIT = "2270d31e8dd611521f979de6d86da364930b7669"

URL_RE = re.compile(r"https?://[^\s)\]}>,]+", re.I)
DOI_RE = re.compile(r"\b10\.[0-9]{4,9}/[-._;()/:A-Z0-9]+", re.I)
ARXIV_RE = re.compile(r"(?<![0-9])(?:[0-9]{4}\.[0-9]{4,5}|(?:math|alg-geom|astro-ph|cond-mat|gr-qc|hep-ex|hep-lat|hep-ph|hep-th|math-ph|nlin|nucl-ex|nucl-th|physics|quant-ph)/[0-9]{7})(?:v[0-9]+)?", re.I)
YEAR_RE = re.compile(r"\b(?:18|19|20)[0-9]{2}\b")
RESOLUTION_RE = re.compile(r"\b(?:proved|proof|resolved|solved|disproved|refuted|counterexample)\b", re.I)


class QueueError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    return sha(path.read_bytes())


def hash_without(value: Mapping[str, Any], field: str) -> str:
    return sha(canonical({key: item for key, item in value.items() if key != field}))


def set_digest(values: Iterable[str]) -> str:
    return sha(canonical(sorted(values)))


def semantic(row: Mapping[str, Any]) -> str:
    value = row.get("semantic_key")
    if isinstance(value, str) and value:
        return value
    value = row.get("dedupe", {}).get("normalized_statement_sha256")
    if isinstance(value, str) and value:
        return "normalized-statement-sha256/" + value
    raise QueueError(f"missing semantic key for {row.get('stage_claim_id')}")


def source_text(row: Mapping[str, Any]) -> str:
    return "\n".join(value for value in (
        row.get("formal_docstring"),
        row.get("mathematical_statement", {}).get("natural_language"),
    ) if isinstance(value, str) and value)


def score(row: Mapping[str, Any]) -> tuple[int, int, int, int, int, int]:
    text = source_text(row)
    return (
        int(bool(DOI_RE.search(text))), int(bool(URL_RE.search(text))),
        int(bool(ARXIV_RE.search(text))), int(bool(RESOLUTION_RE.search(text))),
        int(bool(YEAR_RE.search(text))), len(text),
    )


def validate(row: Mapping[str, Any]) -> None:
    sid = row.get("stage_claim_id")
    if row.get("current_claim_kind") != "theorem" or row.get("material_status") != "proved":
        raise QueueError(f"non-proved theorem: {sid}")
    if row.get("raw_category") != "research solved" or row.get("formal_statement", {}).get("declaration_kind") != "theorem":
        raise QueueError(f"wrong category/declaration: {sid}")
    path = row.get("locator", {}).get("member_path")
    if not isinstance(path, str) or not path.startswith("FormalConjectures/") or "/ErdosProblems/" in path:
        raise QueueError(f"bad non-Erdos source path: {sid}")
    statement = row.get("mathematical_statement", {})
    if not statement.get("formal_type") or not statement.get("natural_language"):
        raise QueueError(f"incomplete source representations: {sid}")


def build() -> dict[str, Any]:
    if file_sha(CATALOG) != CATALOG_SHA or file_sha(MANIFEST) != MANIFEST_SHA:
        raise QueueError("release 5.4 input hash drifted")
    if file_sha(PRIMARY) != PRIMARY_SHA:
        raise QueueError("primary queue hash drifted")
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    primary = json.loads(PRIMARY.read_text(encoding="utf-8"))
    if manifest.get("release_root_sha256") != RELEASE_ROOT or primary.get("authority_sha256") != PRIMARY_AUTHORITY:
        raise QueueError("release or primary authority drifted")
    source_rows = [row for row in catalog["records"]
                   if row.get("current_claim_kind") == "theorem"
                   and row.get("raw_category") == "research solved"
                   and "/ErdosProblems/" not in str(row.get("locator", {}).get("member_path", ""))]
    if len(source_rows) != 371:
        raise QueueError(f"non-Erdos denominator drifted: {len(source_rows)}")
    groups: defaultdict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in source_rows:
        validate(row)
        groups[str(row["locator"]["member_path"])].append(row)
    if len(groups) != 177:
        raise QueueError(f"source-file denominator drifted: {len(groups)}")

    expected_primary: list[Mapping[str, Any]] = []
    supplemental: list[Mapping[str, Any]] = []
    file_rank: dict[str, int] = {}
    for path in sorted(groups):
        values = sorted(groups[path], key=lambda row: (
            tuple(-item for item in score(row)), semantic(row), str(row["stage_claim_id"]),
        ))
        expected_primary.extend(values[:2])
        supplemental.extend(values[2:])
        for index, row in enumerate(values, start=1):
            file_rank[str(row["stage_claim_id"])] = index
    expected_primary.sort(key=lambda row: (
        tuple(-item for item in score(row)), str(row["locator"]["member_path"]).split("/")[1],
        str(row["locator"]["member_path"]), str(row["stage_claim_id"]),
    ))
    primary_ids = [row["stage_claim_id"] for row in primary["records"]]
    if primary_ids != [row["stage_claim_id"] for row in expected_primary]:
        raise QueueError("primary queue is not the exact top-two-per-file set")
    if len(primary_ids) != 254 or len(supplemental) != 117:
        raise QueueError(f"set-difference drifted: primary={len(primary_ids)} supplemental={len(supplemental)}")
    supplemental.sort(key=lambda row: (
        tuple(-item for item in score(row)), str(row["locator"]["member_path"]).split("/")[1],
        str(row["locator"]["member_path"]), str(row["stage_claim_id"]),
    ))
    primary_semantics = {row["semantic_key"] for row in primary["records"]}
    primary_formals = {row["formal_type_sha256"] for row in primary["records"]}

    records = []
    for supplemental_rank, row in enumerate(supplemental, start=1):
        path = str(row["locator"]["member_path"])
        text = source_text(row)
        item: dict[str, Any] = {
            "candidate_rank": 254 + supplemental_rank,
            "supplemental_rank": supplemental_rank,
            "source_file_rank": file_rank[str(row["stage_claim_id"])],
            "stage_claim_id": row["stage_claim_id"],
            "variant_id": row["variant_id"],
            "family_id": row["family_id"],
            "semantic_key": semantic(row),
            "display_name": row["display_name"],
            "primary_ams_class": row.get("primary_ams_class"),
            "source_collection": path.split("/")[1],
            "source_member_path": path,
            "source_locator": row["locator"],
            "source_id": row["source_id"],
            "source_commit": SOURCE_COMMIT,
            "source_record_id": row["curation_key"],
            "formal_type": row["mathematical_statement"]["formal_type"],
            "formal_type_sha256": row.get("formal_type_sha256") or row.get("dedupe", {}).get("formal_type_sha256"),
            "natural_language": row["mathematical_statement"]["natural_language"],
            "statement_sha256": row["mathematical_statement"]["statement_sha256"],
            "primary_queue_exclusion": {
                "reason": "source_file_capacity_after_top_two",
                "maximum_primary_rows_per_source_file": 2,
                "source_file_rank": file_rank[str(row["stage_claim_id"])],
                "primary_queue_sha256": PRIMARY_SHA,
            },
            "exact_cross_queue_dedupe": {
                "semantic_key_in_primary_queue": semantic(row) in primary_semantics,
                "formal_type_sha256_in_primary_queue": row["formal_type_sha256"] in primary_formals,
                "manual_logical_subsumption_pending": True,
            },
            "source_status": {
                "parent_material_status": row["material_status"],
                "parent_raw_category": row["raw_category"],
                "parent_frontier": row.get("frontier"),
                "source_assertion_not_independent_resolution_review": True,
            },
            "discovery_evidence": {
                "resolution_language_present": bool(RESOLUTION_RE.search(text)),
                "urls": sorted(set(URL_RE.findall(text))),
                "dois": sorted(set(match.group(0).rstrip(".,;)") for match in DOI_RE.finditer(text))),
                "arxiv_ids": sorted(set(match.group(0) for match in ARXIV_RE.finditer(text))),
                "years": sorted(set(YEAR_RE.findall(text))),
                "score": list(score(row)),
            },
            "rights": row.get("rights"),
            "review_state": {
                "disposition": "pending_human_frontier_review",
                "primary_resolution_reference_verified": False,
                "theorem_scope_matches_resolution": False,
                "current_proved_status_independently_verified": False,
                "importance_verified": False,
                "semantic_dedupe_complete": False,
                "grants_frontier_credit": False,
                "grants_new_theorem_credit": False,
            },
        }
        if item["source_file_rank"] <= 2:
            raise QueueError(f"supplemental row did not exceed file cap: {row['stage_claim_id']}")
        item["row_sha256"] = hash_without(item, "row_sha256")
        records.append(item)

    if any(row["exact_cross_queue_dedupe"]["semantic_key_in_primary_queue"] or
           row["exact_cross_queue_dedupe"]["formal_type_sha256_in_primary_queue"] for row in records):
        raise QueueError("unexpected exact primary/supplemental duplicate")
    result: dict[str, Any] = {
        "schema_version": "awesome-theorems/frontier-theorem-supplemental-review-queue/5.5",
        "review_as_of": "2026-08-10",
        "scope": "complete non-Erdos research-solved remainder after the frozen 254-row primary queue; candidate-only",
        "inputs": {
            "parent_release": "5.4",
            "parent_release_root_sha256": RELEASE_ROOT,
            "parent_catalog_sha256": CATALOG_SHA,
            "parent_manifest_sha256": MANIFEST_SHA,
            "primary_queue_path": PRIMARY.relative_to(ROOT).as_posix(),
            "primary_queue_sha256": PRIMARY_SHA,
            "primary_queue_authority_sha256": PRIMARY_AUTHORITY,
            "formal_conjectures_commit": SOURCE_COMMIT,
        },
        "selection_policy": {
            "source_category": "research solved",
            "excluded_collection": "ErdosProblems",
            "set_operation": "all_371_nonerdos_rows minus exact_254_primary_stage_claim_ids",
            "primary_queue_maximum_rows_per_source_file": 2,
            "supplemental_source_file_rank_minimum": 3,
            "ranking": ["DOI", "URL", "arXiv identifier", "resolution language", "year", "source text length"],
            "automatic_credit": False,
        },
        "counts": {
            "source_rows": 371,
            "distinct_source_files": 177,
            "primary_queue_rows": 254,
            "supplemental_queue_rows": len(records),
            "supplemental_distinct_source_files": len({row["source_member_path"] for row in records}),
            "exact_semantic_overlaps_with_primary": sum(row["exact_cross_queue_dedupe"]["semantic_key_in_primary_queue"] for row in records),
            "exact_formal_type_overlaps_with_primary": sum(row["exact_cross_queue_dedupe"]["formal_type_sha256_in_primary_queue"] for row in records),
            "rows_with_url": sum(bool(row["discovery_evidence"]["urls"]) for row in records),
            "rows_with_doi": sum(bool(row["discovery_evidence"]["dois"]) for row in records),
            "rows_with_arxiv_id": sum(bool(row["discovery_evidence"]["arxiv_ids"]) for row in records),
            "rows_with_resolution_language": sum(row["discovery_evidence"]["resolution_language_present"] for row in records),
            "accepted_frontier_credits": 0,
            "new_theorem_credits": 0,
            "by_collection": dict(sorted(Counter(row["source_collection"] for row in records).items())),
        },
        "set_digests": {
            "primary_s5_id_set_sha256": set_digest(primary_ids),
            "supplemental_s5_id_set_sha256": set_digest(row["stage_claim_id"] for row in records),
            "combined_s5_id_set_sha256": set_digest(primary_ids + [row["stage_claim_id"] for row in records]),
            "semantic_key_set_sha256": set_digest(row["semantic_key"] for row in records),
            "formal_type_sha256_set_sha256": set_digest(row["formal_type_sha256"] for row in records),
            "row_sha256_set_sha256": set_digest(row["row_sha256"] for row in records),
        },
        "records": records,
    }
    result["authority_sha256"] = hash_without(result, "authority_sha256")
    return result


def main() -> None:
    document = build()
    OUTPUT.write_bytes(canonical(document) + b"\n")
    print(f"wrote {OUTPUT} rows={len(document['records'])} authority={document['authority_sha256']}")


if __name__ == "__main__":
    main()
