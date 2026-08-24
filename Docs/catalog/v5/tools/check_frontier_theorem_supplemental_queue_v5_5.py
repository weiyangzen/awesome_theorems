#!/usr/bin/env python3
"""Independent checker for the 117-row non-Erdos supplemental queue."""

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
QUEUE = ROOT / "Docs/catalog/v5/curation/Frontier_Theorem_Supplemental_Candidate_Queue_v5_5.json"
CATALOG_SHA = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
MANIFEST_SHA = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
RELEASE_ROOT = "c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813"
PRIMARY_SHA = "b3b28b81cfcd9fe4dbf002d2bb8d9bedaa8094656396e224abb5c6221530b2fc"
PRIMARY_AUTHORITY = "375ca73546293f74fdc966209d4be0d184ad5e28273c70aecc7a12a601548133"
URL_RE = re.compile(r"https?://[^\s)\]}>,]+", re.I)
DOI_RE = re.compile(r"\b10\.[0-9]{4,9}/[-._;()/:A-Z0-9]+", re.I)
ARXIV_RE = re.compile(r"(?<![0-9])(?:[0-9]{4}\.[0-9]{4,5}|(?:math|alg-geom|astro-ph|cond-mat|gr-qc|hep-ex|hep-lat|hep-ph|hep-th|math-ph|nlin|nucl-ex|nucl-th|physics|quant-ph)/[0-9]{7})(?:v[0-9]+)?", re.I)
YEAR_RE = re.compile(r"\b(?:18|19|20)[0-9]{2}\b")
RESOLUTION_RE = re.compile(r"\b(?:proved|proof|resolved|solved|disproved|refuted|counterexample)\b", re.I)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_without(value: Mapping[str, Any], field: str) -> str:
    return sha(canonical({key: item for key, item in value.items() if key != field}))


def set_digest(values: Iterable[str]) -> str:
    return sha(canonical(sorted(values)))


def semantic(row: Mapping[str, Any]) -> str:
    value = row.get("semantic_key") or row.get("dedupe", {}).get("normalized_statement_sha256")
    assert isinstance(value, str) and value
    return value if value.startswith("normalized-statement-sha256/") else "normalized-statement-sha256/" + value


def text(row: Mapping[str, Any]) -> str:
    return "\n".join(value for value in (row.get("formal_docstring"), row.get("mathematical_statement", {}).get("natural_language")) if isinstance(value, str) and value)


def score(row: Mapping[str, Any]) -> tuple[int, int, int, int, int, int]:
    value = text(row)
    return (int(bool(DOI_RE.search(value))), int(bool(URL_RE.search(value))), int(bool(ARXIV_RE.search(value))), int(bool(RESOLUTION_RE.search(value))), int(bool(YEAR_RE.search(value))), len(value))


def main() -> None:
    assert sha(CATALOG.read_bytes()) == CATALOG_SHA
    assert sha(MANIFEST.read_bytes()) == MANIFEST_SHA
    assert sha(PRIMARY.read_bytes()) == PRIMARY_SHA
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    primary = json.loads(PRIMARY.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    assert manifest["release_root_sha256"] == RELEASE_ROOT
    assert primary["authority_sha256"] == PRIMARY_AUTHORITY
    rows = [row for row in catalog["records"] if row.get("current_claim_kind") == "theorem" and row.get("raw_category") == "research solved" and "/ErdosProblems/" not in str(row.get("locator", {}).get("member_path", ""))]
    assert len(rows) == 371
    groups: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        assert row["material_status"] == "proved" and row["formal_statement"]["declaration_kind"] == "theorem"
        assert row["mathematical_statement"]["formal_type"] and row["mathematical_statement"]["natural_language"]
        path = row["locator"]["member_path"]
        assert path.startswith("FormalConjectures/") and "/ErdosProblems/" not in path
        groups[path].append(row)
    assert len(groups) == 177
    expected_primary = []
    expected_supplemental = []
    file_rank = {}
    for path in sorted(groups):
        values = sorted(groups[path], key=lambda row: (tuple(-item for item in score(row)), semantic(row), row["stage_claim_id"]))
        expected_primary.extend(values[:2])
        expected_supplemental.extend(values[2:])
        for index, row in enumerate(values, start=1):
            file_rank[row["stage_claim_id"]] = index
    order_key = lambda row: (tuple(-item for item in score(row)), row["locator"]["member_path"].split("/")[1], row["locator"]["member_path"], row["stage_claim_id"])
    expected_primary.sort(key=order_key)
    expected_supplemental.sort(key=order_key)
    primary_ids = [row["stage_claim_id"] for row in primary["records"]]
    supplemental_ids = [row["stage_claim_id"] for row in expected_supplemental]
    assert primary_ids == [row["stage_claim_id"] for row in expected_primary]
    assert len(primary_ids) == 254 and len(supplemental_ids) == 117
    assert not set(primary_ids) & set(supplemental_ids)
    assert set(primary_ids) | set(supplemental_ids) == {row["stage_claim_id"] for row in rows}

    assert queue["schema_version"] == "awesome-theorems/frontier-theorem-supplemental-review-queue/5.5"
    assert queue["inputs"]["parent_catalog_sha256"] == CATALOG_SHA
    assert queue["inputs"]["parent_manifest_sha256"] == MANIFEST_SHA
    assert queue["inputs"]["parent_release_root_sha256"] == RELEASE_ROOT
    assert queue["inputs"]["primary_queue_sha256"] == PRIMARY_SHA
    assert queue["inputs"]["primary_queue_authority_sha256"] == PRIMARY_AUTHORITY
    records = queue["records"]
    assert len(records) == 117
    assert [row["stage_claim_id"] for row in records] == supplemental_ids
    parent_by_id = {row["stage_claim_id"]: row for row in expected_supplemental}
    primary_semantics = {row["semantic_key"] for row in primary["records"]}
    primary_formals = {row["formal_type_sha256"] for row in primary["records"]}
    for supplemental_rank, item in enumerate(records, start=1):
        parent = parent_by_id[item["stage_claim_id"]]
        assert item["candidate_rank"] == 254 + supplemental_rank
        assert item["supplemental_rank"] == supplemental_rank
        assert item["source_file_rank"] == file_rank[item["stage_claim_id"]] >= 3
        for field in ("variant_id", "family_id", "display_name"):
            assert item[field] == parent[field]
        assert item["semantic_key"] == semantic(parent)
        assert item["source_member_path"] == parent["locator"]["member_path"]
        assert item["source_locator"] == parent["locator"]
        assert item["formal_type"] == parent["mathematical_statement"]["formal_type"]
        assert item["natural_language"] == parent["mathematical_statement"]["natural_language"]
        assert item["primary_queue_exclusion"]["reason"] == "source_file_capacity_after_top_two"
        assert item["primary_queue_exclusion"]["source_file_rank"] == item["source_file_rank"]
        dedupe = item["exact_cross_queue_dedupe"]
        assert dedupe["semantic_key_in_primary_queue"] == (item["semantic_key"] in primary_semantics) is False
        assert dedupe["formal_type_sha256_in_primary_queue"] == (item["formal_type_sha256"] in primary_formals) is False
        assert dedupe["manual_logical_subsumption_pending"] is True
        discovery = item["discovery_evidence"]
        source = text(parent)
        assert discovery["score"] == list(score(parent))
        assert discovery["urls"] == sorted(set(URL_RE.findall(source)))
        assert discovery["dois"] == sorted(set(match.group(0).rstrip(".,;)") for match in DOI_RE.finditer(source)))
        assert discovery["arxiv_ids"] == sorted(set(match.group(0) for match in ARXIV_RE.finditer(source)))
        review = item["review_state"]
        assert review["disposition"] == "pending_human_frontier_review"
        assert all(review[field] is False for field in (
            "primary_resolution_reference_verified", "theorem_scope_matches_resolution",
            "current_proved_status_independently_verified", "importance_verified",
            "semantic_dedupe_complete", "grants_frontier_credit", "grants_new_theorem_credit",
        ))
        assert item["row_sha256"] == hash_without(item, "row_sha256")

    counts = queue["counts"]
    assert counts["source_rows"] == 371 and counts["primary_queue_rows"] == 254 and counts["supplemental_queue_rows"] == 117
    assert counts["distinct_source_files"] == 177 and counts["supplemental_distinct_source_files"] == 45
    assert counts["exact_semantic_overlaps_with_primary"] == 0 and counts["exact_formal_type_overlaps_with_primary"] == 0
    assert counts["accepted_frontier_credits"] == 0 and counts["new_theorem_credits"] == 0
    assert counts["by_collection"] == dict(sorted(Counter(row["source_collection"] for row in records).items()))
    digests = queue["set_digests"]
    assert digests["primary_s5_id_set_sha256"] == set_digest(primary_ids)
    assert digests["supplemental_s5_id_set_sha256"] == set_digest(supplemental_ids)
    assert digests["combined_s5_id_set_sha256"] == set_digest(primary_ids + supplemental_ids)
    assert digests["semantic_key_set_sha256"] == set_digest(row["semantic_key"] for row in records)
    assert digests["formal_type_sha256_set_sha256"] == set_digest(row["formal_type_sha256"] for row in records)
    assert digests["row_sha256_set_sha256"] == set_digest(row["row_sha256"] for row in records)
    assert queue["authority_sha256"] == hash_without(queue, "authority_sha256")
    print(f"PASS supplemental frontier queue rows=117 primary=254 union=371 authority={queue['authority_sha256']}")


if __name__ == "__main__":
    main()
