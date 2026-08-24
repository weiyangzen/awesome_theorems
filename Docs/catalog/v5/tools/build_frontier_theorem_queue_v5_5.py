#!/usr/bin/env python3
"""Build the non-Erdős frontier-theorem human-review queue for Stage5.5.

Every output row is an existing release-5.4 theorem identity whose pinned
Formal Conjectures source labels it ``research solved``.  This queue excludes
Erdős rows (they have a separate current-status join), admits at most two
distinct source declarations per file, and grants no frontier or new-theorem
credit.  Primary resolution references, theorem scope, status, importance and
semantic equivalence remain human-review gates.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping


REPO_ROOT = Path(__file__).resolve().parents[4]
CATALOG = REPO_ROOT / "Docs/catalog/v5/releases/5.4/Claim_Catalog.json"
MANIFEST = REPO_ROOT / "Docs/catalog/v5/releases/5.4/Release_Manifest.json"
OUTPUT = REPO_ROOT / "Docs/catalog/v5/curation/Frontier_Theorem_Candidate_Queue_v5_5.json"
CATALOG_SHA256 = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
MANIFEST_SHA256 = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
RELEASE_ROOT = "c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813"
FORMAL_CONJECTURES_COMMIT = "2270d31e8dd611521f979de6d86da364930b7669"
URL_RE = re.compile(r"https?://[^\s)\]}>,]+", re.IGNORECASE)
DOI_RE = re.compile(r"\b10\.[0-9]{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
ARXIV_RE = re.compile(
    r"(?<![0-9])(?:[0-9]{4}\.[0-9]{4,5}|(?:math|alg-geom|astro-ph|cond-mat|gr-qc|hep-ex|hep-lat|hep-ph|hep-th|math-ph|nlin|nucl-ex|nucl-th|physics|quant-ph)/[0-9]{7})(?:v[0-9]+)?",
    re.IGNORECASE,
)
YEAR_RE = re.compile(r"\b(?:18|19|20)[0-9]{2}\b")
RESOLUTION_RE = re.compile(r"\b(?:proved|proof|resolved|solved|disproved|refuted|counterexample)\b", re.IGNORECASE)


class QueueError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
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


def stable_semantic_key(row: Mapping[str, Any]) -> str:
    key = row.get("semantic_key")
    if isinstance(key, str) and key:
        return key
    normalized = row.get("dedupe", {}).get("normalized_statement_sha256")
    if isinstance(normalized, str) and normalized:
        return f"normalized-statement-sha256/{normalized}"
    raise QueueError(f"missing semantic key for {row.get('stage_claim_id')}")


def source_text(row: Mapping[str, Any]) -> str:
    return "\n".join(
        value
        for value in (
            row.get("formal_docstring"),
            row.get("mathematical_statement", {}).get("natural_language"),
        )
        if isinstance(value, str) and value
    )


def evidence_score(row: Mapping[str, Any]) -> tuple[int, int, int, int, int, int]:
    text = source_text(row)
    return (
        int(bool(DOI_RE.search(text))),
        int(bool(URL_RE.search(text))),
        int(bool(ARXIV_RE.search(text))),
        int(bool(RESOLUTION_RE.search(text))),
        int(bool(YEAR_RE.search(text))),
        len(text),
    )


def validate_candidate(row: Mapping[str, Any]) -> None:
    sid = row.get("stage_claim_id")
    if row.get("current_claim_kind") != "theorem" or row.get("material_status") != "proved":
        raise QueueError(f"non-proved theorem candidate: {sid}")
    if row.get("raw_category") != "research solved":
        raise QueueError(f"candidate is not source-labelled research solved: {sid}")
    if row.get("formal_statement", {}).get("declaration_kind") != "theorem":
        raise QueueError(f"candidate is not literal theorem syntax: {sid}")
    path = row.get("locator", {}).get("member_path")
    if not isinstance(path, str) or not path.startswith("FormalConjectures/"):
        raise QueueError(f"candidate lacks Formal Conjectures locator: {sid}")
    if "/ErdosProblems/" in path:
        raise QueueError(f"Erdős row leaked into non-Erdős queue: {sid}")
    statement = row.get("mathematical_statement", {})
    if not statement.get("formal_type") or not statement.get("natural_language"):
        raise QueueError(f"candidate lacks complete source representations: {sid}")


def build() -> dict[str, Any]:
    if sha_file(CATALOG) != CATALOG_SHA256 or sha_file(MANIFEST) != MANIFEST_SHA256:
        raise QueueError("release 5.4 input hash drifted")
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("release_root_sha256") != RELEASE_ROOT:
        raise QueueError("release root drifted")
    source_rows = [
        row
        for row in catalog.get("records", [])
        if row.get("current_claim_kind") == "theorem"
        and row.get("raw_category") == "research solved"
        and "/ErdosProblems/" not in str(row.get("locator", {}).get("member_path", ""))
    ]
    if len(source_rows) != 371:
        raise QueueError(f"non-Erdős denominator drifted: {len(source_rows)}")
    by_file: defaultdict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in source_rows:
        validate_candidate(row)
        by_file[str(row["locator"]["member_path"])].append(row)

    selected: list[Mapping[str, Any]] = []
    for path, values in sorted(by_file.items()):
        values.sort(
            key=lambda row: (
                tuple(-value for value in evidence_score(row)),
                stable_semantic_key(row),
                str(row["stage_claim_id"]),
            )
        )
        selected.extend(values[:2])
    if len(by_file) != 177 or len(selected) != 254:
        raise QueueError(f"file/capacity drifted: files={len(by_file)} selected={len(selected)}")

    selected.sort(
        key=lambda row: (
            tuple(-value for value in evidence_score(row)),
            str(row["locator"]["member_path"]).split("/")[1],
            str(row["locator"]["member_path"]),
            str(row["stage_claim_id"]),
        )
    )
    records: list[dict[str, Any]] = []
    per_file_rank: Counter[str] = Counter()
    for rank, row in enumerate(selected, start=1):
        path = str(row["locator"]["member_path"])
        per_file_rank[path] += 1
        text = source_text(row)
        urls = sorted(set(URL_RE.findall(text)))
        dois = sorted(set(match.group(0).rstrip(".,;)") for match in DOI_RE.finditer(text)))
        arxiv_ids = sorted(set(match.group(0) for match in ARXIV_RE.finditer(text)))
        years = sorted(set(YEAR_RE.findall(text)))
        item: dict[str, Any] = {
            "candidate_rank": rank,
            "source_file_rank": per_file_rank[path],
            "stage_claim_id": row["stage_claim_id"],
            "variant_id": row["variant_id"],
            "family_id": row["family_id"],
            "semantic_key": stable_semantic_key(row),
            "display_name": row["display_name"],
            "primary_ams_class": row.get("primary_ams_class"),
            "source_collection": path.split("/")[1],
            "source_member_path": path,
            "source_locator": row["locator"],
            "source_id": row["source_id"],
            "source_commit": FORMAL_CONJECTURES_COMMIT,
            "source_record_id": row["curation_key"],
            "formal_type": row["mathematical_statement"]["formal_type"],
            "formal_type_sha256": row.get("formal_type_sha256") or row.get("dedupe", {}).get("formal_type_sha256"),
            "natural_language": row["mathematical_statement"]["natural_language"],
            "statement_sha256": row["mathematical_statement"]["statement_sha256"],
            "source_status": {
                "parent_material_status": row["material_status"],
                "parent_raw_category": row["raw_category"],
                "parent_frontier": row.get("frontier"),
                "source_assertion_not_independent_resolution_review": True,
            },
            "discovery_evidence": {
                "resolution_language_present": bool(RESOLUTION_RE.search(text)),
                "urls": urls,
                "dois": dois,
                "arxiv_ids": arxiv_ids,
                "years": years,
                "score": list(evidence_score(row)),
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
        item["row_sha256"] = hash_without(item, "row_sha256")
        records.append(item)

    result: dict[str, Any] = {
        "schema_version": "awesome-theorems/frontier-theorem-review-queue/5.5",
        "review_as_of": "2026-08-10",
        "scope": "non-Erdos existing-theorem frontier review candidates; no automatic credit",
        "inputs": {
            "parent_release": "5.4",
            "parent_release_root_sha256": RELEASE_ROOT,
            "parent_catalog_sha256": CATALOG_SHA256,
            "parent_manifest_sha256": MANIFEST_SHA256,
            "formal_conjectures_commit": FORMAL_CONJECTURES_COMMIT,
        },
        "selection_policy": {
            "source_category": "research solved",
            "excluded_collection": "ErdosProblems",
            "maximum_rows_per_source_file": 2,
            "ranking": ["DOI", "URL", "arXiv identifier", "resolution language", "year", "source text length"],
            "automatic_credit": False,
        },
        "counts": {
            "source_rows": len(source_rows),
            "distinct_source_files": len(by_file),
            "review_queue_rows": len(records),
            "rows_with_url": sum(bool(row["discovery_evidence"]["urls"]) for row in records),
            "rows_with_doi": sum(bool(row["discovery_evidence"]["dois"]) for row in records),
            "rows_with_arxiv_id": sum(bool(row["discovery_evidence"]["arxiv_ids"]) for row in records),
            "rows_with_resolution_language": sum(row["discovery_evidence"]["resolution_language_present"] for row in records),
            "accepted_frontier_credits": 0,
            "new_theorem_credits": 0,
            "by_collection": dict(sorted(Counter(row["source_collection"] for row in records).items())),
        },
        "set_digests": {
            "s5_id_set_sha256": set_digest(row["stage_claim_id"] for row in records),
            "semantic_key_set_sha256": set_digest(row["semantic_key"] for row in records),
            "row_sha256_set_sha256": set_digest(row["row_sha256"] for row in records),
        },
        "records": records,
    }
    result["authority_sha256"] = hash_without(result, "authority_sha256")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    document = build()
    payload = canonical(document) + b"\n"
    if args.check:
        if not args.output.is_file() or args.output.read_bytes() != payload:
            raise QueueError(f"missing or stale queue: {args.output}")
        print(f"PASS frontier theorem queue rows={len(document['records'])} authority={document['authority_sha256']}")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    print(f"wrote {args.output} rows={len(document['records'])} authority={document['authority_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
