#!/usr/bin/env python3
"""Independent checker for the Stage5.5 non-Erdős frontier review queue."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[4]
CATALOG = ROOT / "Docs/catalog/v5/releases/5.4/Claim_Catalog.json"
MANIFEST = ROOT / "Docs/catalog/v5/releases/5.4/Release_Manifest.json"
QUEUE = ROOT / "Docs/catalog/v5/curation/Frontier_Theorem_Candidate_Queue_v5_5.json"
CATALOG_SHA = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
MANIFEST_SHA = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
ROOT_SHA = "c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813"
URL = re.compile(r"https?://[^\s)\]}>,]+", re.I)
DOI = re.compile(r"\b10\.[0-9]{4,9}/[-._;()/:A-Z0-9]+", re.I)
ARXIV = re.compile(r"(?<![0-9])(?:[0-9]{4}\.[0-9]{4,5}|(?:math|alg-geom|astro-ph|cond-mat|gr-qc|hep-ex|hep-lat|hep-ph|hep-th|math-ph|nlin|nucl-ex|nucl-th|physics|quant-ph)/[0-9]{7})(?:v[0-9]+)?", re.I)
YEAR = re.compile(r"\b(?:18|19|20)[0-9]{2}\b")
RESOLUTION = re.compile(r"\b(?:proved|proof|resolved|solved|disproved|refuted|counterexample)\b", re.I)


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], field: str) -> str:
    return sha(canonical({key: item for key, item in value.items() if key != field}))


def set_digest(values: Iterable[str]) -> str:
    return sha(canonical(sorted(values)))


def semantic(row: Mapping[str, Any]) -> str:
    value = row.get("semantic_key")
    if isinstance(value, str) and value:
        return value
    value = row.get("dedupe", {}).get("normalized_statement_sha256")
    require(isinstance(value, str) and bool(value), f"missing semantic key: {row.get('stage_claim_id')}")
    return f"normalized-statement-sha256/{value}"


def text(row: Mapping[str, Any]) -> str:
    return "\n".join(
        value
        for value in (row.get("formal_docstring"), row.get("mathematical_statement", {}).get("natural_language"))
        if isinstance(value, str) and value
    )


def score(row: Mapping[str, Any]) -> tuple[int, int, int, int, int, int]:
    value = text(row)
    return (
        int(bool(DOI.search(value))),
        int(bool(URL.search(value))),
        int(bool(ARXIV.search(value))),
        int(bool(RESOLUTION.search(value))),
        int(bool(YEAR.search(value))),
        len(value),
    )


def selected_parent_rows(parent: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    candidates = [
        row
        for row in parent
        if row.get("current_claim_kind") == "theorem"
        and row.get("raw_category") == "research solved"
        and "/ErdosProblems/" not in str(row.get("locator", {}).get("member_path", ""))
    ]
    require(len(candidates) == 371, "source denominator mismatch")
    groups: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in candidates:
        sid = row.get("stage_claim_id")
        require(row.get("material_status") == "proved", f"non-proved candidate {sid}")
        require(row.get("formal_statement", {}).get("declaration_kind") == "theorem", f"non-theorem syntax {sid}")
        path = row.get("locator", {}).get("member_path")
        require(isinstance(path, str) and path.startswith("FormalConjectures/"), f"bad source path {sid}")
        require(row.get("mathematical_statement", {}).get("formal_type") and row.get("mathematical_statement", {}).get("natural_language"), f"incomplete source row {sid}")
        groups[path].append(row)
    selected: list[dict[str, Any]] = []
    for path in sorted(groups):
        values = groups[path]
        values.sort(key=lambda row: (tuple(-item for item in score(row)), semantic(row), row["stage_claim_id"]))
        selected.extend(values[:2])
    require(len(groups) == 177 and len(selected) == 254, "file cap mismatch")
    selected.sort(
        key=lambda row: (
            tuple(-item for item in score(row)),
            row["locator"]["member_path"].split("/")[1],
            row["locator"]["member_path"],
            row["stage_claim_id"],
        )
    )
    return selected, len(groups)


def check(queue_path: Path = QUEUE) -> dict[str, Any]:
    require(file_sha(CATALOG) == CATALOG_SHA and file_sha(MANIFEST) == MANIFEST_SHA, "parent input hash mismatch")
    parent_doc = json.loads(CATALOG.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(manifest.get("release_root_sha256") == ROOT_SHA, "parent root mismatch")
    selected, file_count = selected_parent_rows(parent_doc["records"])
    by_id = {row["stage_claim_id"]: row for row in selected}
    try:
        document = json.loads(queue_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CheckError(f"cannot read queue: {error}") from error
    require(document.get("schema_version") == "awesome-theorems/frontier-theorem-review-queue/5.5", "schema mismatch")
    require(document.get("inputs", {}).get("parent_release_root_sha256") == ROOT_SHA, "input root binding mismatch")
    policy = document.get("selection_policy", {})
    require(policy.get("maximum_rows_per_source_file") == 2 and policy.get("automatic_credit") is False, "selection policy mismatch")
    records = document.get("records")
    require(isinstance(records, list) and len(records) == 254, "queue cardinality mismatch")
    expected_order = [row["stage_claim_id"] for row in selected]
    require([row.get("stage_claim_id") for row in records] == expected_order, "queue selection/order mismatch")
    ranks: Counter[str] = Counter()
    for index, item in enumerate(records, start=1):
        sid = item["stage_claim_id"]
        parent = by_id[sid]
        path = parent["locator"]["member_path"]
        ranks[path] += 1
        require(item.get("candidate_rank") == index and item.get("source_file_rank") == ranks[path], f"rank mismatch {sid}")
        require(item.get("variant_id") == parent["variant_id"] and item.get("family_id") == parent["family_id"], f"identity mismatch {sid}")
        require(item.get("semantic_key") == semantic(parent), f"semantic mismatch {sid}")
        require(item.get("source_member_path") == path and item.get("source_locator") == parent["locator"], f"source mismatch {sid}")
        require(item.get("formal_type") == parent["mathematical_statement"]["formal_type"], f"formal statement mismatch {sid}")
        require(item.get("natural_language") == parent["mathematical_statement"]["natural_language"], f"natural statement mismatch {sid}")
        discovery = item.get("discovery_evidence", {})
        source = text(parent)
        require(discovery.get("score") == list(score(parent)), f"score mismatch {sid}")
        require(discovery.get("urls") == sorted(set(URL.findall(source))), f"URL evidence mismatch {sid}")
        require(discovery.get("dois") == sorted(set(match.group(0).rstrip(".,;)") for match in DOI.finditer(source))), f"DOI evidence mismatch {sid}")
        require(discovery.get("arxiv_ids") == sorted(set(match.group(0) for match in ARXIV.finditer(source))), f"arXiv evidence mismatch {sid}")
        review = item.get("review_state", {})
        require(review.get("disposition") == "pending_human_frontier_review", f"non-pending candidate {sid}")
        for field in ("primary_resolution_reference_verified", "theorem_scope_matches_resolution", "current_proved_status_independently_verified", "importance_verified", "semantic_dedupe_complete", "grants_frontier_credit", "grants_new_theorem_credit"):
            require(review.get(field) is False, f"unsupported {field} for {sid}")
        require(item.get("row_sha256") == hash_without(item, "row_sha256"), f"row hash mismatch {sid}")
    counts = document.get("counts", {})
    require(counts.get("source_rows") == 371 and counts.get("distinct_source_files") == file_count and counts.get("review_queue_rows") == 254, "count denominator mismatch")
    require(counts.get("accepted_frontier_credits") == 0 and counts.get("new_theorem_credits") == 0, "unsupported count credit")
    require(counts.get("by_collection") == dict(sorted(Counter(row["source_collection"] for row in records).items())), "collection counts mismatch")
    sets = document.get("set_digests", {})
    require(sets.get("s5_id_set_sha256") == set_digest(row["stage_claim_id"] for row in records), "ID set digest mismatch")
    require(sets.get("semantic_key_set_sha256") == set_digest(row["semantic_key"] for row in records), "semantic set digest mismatch")
    require(sets.get("row_sha256_set_sha256") == set_digest(row["row_sha256"] for row in records), "row set digest mismatch")
    require(document.get("authority_sha256") == hash_without(document, "authority_sha256"), "authority mismatch")
    return {"rows": len(records), "authority": document["authority_sha256"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=QUEUE)
    args = parser.parse_args()
    result = check(args.queue.resolve())
    print(f"PASS independent frontier theorem queue rows={result['rows']} authority={result['authority']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
