#!/usr/bin/env python3
"""Fetch and pin OpenAlex metadata for DOI review candidates.

OpenAlex metadata corroborates bibliographic identity and date only.  It never
proves that a work supports the exact theorem statement or grants quality
credit without human review.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import gzip
import hashlib
import json
from pathlib import Path
import time
from typing import Any, Iterable, Mapping
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[4]
INPUT = ROOT / "Docs/catalog/v5/curation/Thousand_Plus_Reference_Candidates_v5_5.json"
OUTPUT = ROOT / "Docs/catalog/v5/sources/openalex-thousand-plus-doi-metadata-20260810.json.gz"
INPUT_SHA256 = "f86b87afcffbf120d2f3cf0ff8860e7c925e8f9fa514db3714936e3cfa100435"
API = "https://api.openalex.org/works"
BATCH_SIZE = 40


class MetadataError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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


def chunks(values: list[str], size: int) -> list[list[str]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def fetch_batch(dois: list[str]) -> dict[str, Any]:
    filter_value = "|".join(f"https://doi.org/{doi}" for doi in dois)
    url = (
        f"{API}?filter=doi:{quote(filter_value, safe='|:/')}&per-page=100"
        "&select=id,doi,display_name,publication_year,publication_date,type,authorships,primary_location,open_access,updated_date,cited_by_count,ids"
        "&mailto=awesome-theorems@example.com"
    )
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            request = Request(url, headers={"User-Agent": "awesome-theorems-source-audit/5.5 (mailto:awesome-theorems@example.com)"})
            with urlopen(request, timeout=45) as response:
                payload = response.read()
            document = json.loads(payload)
            if not isinstance(document, dict) or not isinstance(document.get("results"), list):
                raise MetadataError("OpenAlex response shape mismatch")
            return document
        except Exception as error:  # network and JSON failures share bounded retry
            last_error = error
            if attempt < 3:
                time.sleep(0.5 * (2**attempt))
    raise MetadataError(f"OpenAlex batch failed after retries: {last_error}")


def compact_work(work: Mapping[str, Any]) -> dict[str, Any]:
    doi = work.get("doi")
    normalized = doi.removeprefix("https://doi.org/").lower() if isinstance(doi, str) else None
    authors = []
    for authorship in work.get("authorships") or []:
        if not isinstance(authorship, dict):
            continue
        author = authorship.get("author") or {}
        name = author.get("display_name") if isinstance(author, dict) else None
        if isinstance(name, str) and name:
            authors.append(name)
    location = work.get("primary_location") or {}
    source = location.get("source") or {} if isinstance(location, dict) else {}
    row: dict[str, Any] = {
        "normalized_doi": normalized,
        "openalex_id": work.get("id"),
        "title": work.get("display_name"),
        "publication_year": work.get("publication_year"),
        "publication_date": work.get("publication_date"),
        "type": work.get("type"),
        "authors": authors,
        "cited_by_count": work.get("cited_by_count"),
        "updated_date": work.get("updated_date"),
        "ids": work.get("ids"),
        "primary_location": {
            "landing_page_url": location.get("landing_page_url") if isinstance(location, dict) else None,
            "pdf_url": location.get("pdf_url") if isinstance(location, dict) else None,
            "is_oa": location.get("is_oa") if isinstance(location, dict) else None,
            "source_id": source.get("id") if isinstance(source, dict) else None,
            "source_name": source.get("display_name") if isinstance(source, dict) else None,
            "source_issn_l": source.get("issn_l") if isinstance(source, dict) else None,
        },
        "open_access": work.get("open_access"),
        "evidence_boundary": {
            "bibliographic_metadata_only": True,
            "supports_exact_theorem_statement_verified": False,
            "quality_credit_granted": False,
        },
    }
    row["row_sha256"] = hash_without(row, "row_sha256")
    return row


def build(*, network: bool) -> dict[str, Any]:
    if file_sha(INPUT) != INPUT_SHA256:
        raise MetadataError("reference-candidate input digest drifted")
    candidates = json.loads(INPUT.read_text(encoding="utf-8"))
    dois = sorted(
        {
            item["normalized_identifier"]
            for record in candidates.get("records", [])
            for item in record.get("reference_candidates", [])
            if item.get("kind") == "doi"
        }
    )
    if len(dois) != 2_655:
        raise MetadataError(f"DOI denominator drifted: {len(dois)}")
    if not network:
        if not OUTPUT.is_file():
            raise MetadataError("missing pinned OpenAlex output")
        with gzip.open(OUTPUT, "rt", encoding="utf-8") as stream:
            return json.load(stream)

    responses: list[dict[str, Any]] = []
    batches = chunks(dois, BATCH_SIZE)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(fetch_batch, batch): index for index, batch in enumerate(batches)}
        ordered: dict[int, dict[str, Any]] = {}
        for future in as_completed(futures):
            ordered[futures[future]] = future.result()
        responses = [ordered[index] for index in range(len(batches))]
    # OpenAlex can expose more than one work for the same DOI.  A concrete
    # example in this corpus is 10.1002/9783527617234, which currently maps to
    # both a book and an article record.  Do not silently choose whichever row
    # happens to be returned first: retain every distinct match and quarantine
    # the DOI as bibliographically ambiguous for human review.
    works: dict[str, dict[str, dict[str, Any]]] = {}
    for response in responses:
        for raw in response["results"]:
            row = compact_work(raw)
            doi = row["normalized_doi"]
            if not isinstance(doi, str) or doi not in dois:
                continue
            row_key = row.get("openalex_id")
            if not isinstance(row_key, str) or not row_key:
                row_key = row["row_sha256"]
            previous = works.setdefault(doi, {}).get(row_key)
            if previous is not None and previous != row:
                raise MetadataError(f"conflicting OpenAlex payloads for {doi} / {row_key}")
            works[doi][row_key] = row
    records = []
    for doi in dois:
        matches = sorted(works.get(doi, {}).values(), key=lambda row: (str(row.get("openalex_id")), row["row_sha256"]))
        if len(matches) == 1:
            records.append(matches[0])
        elif len(matches) > 1:
            row = {
                "normalized_doi": doi,
                "openalex_id": None,
                "ambiguous": True,
                "match_count": len(matches),
                "matches": matches,
                "evidence_boundary": {
                    "bibliographic_metadata_only": True,
                    "supports_exact_theorem_statement_verified": False,
                    "quality_credit_granted": False,
                    "human_disambiguation_required": True,
                },
            }
            row["row_sha256"] = hash_without(row, "row_sha256")
            records.append(row)
        else:
            row: dict[str, Any] = {
                "normalized_doi": doi,
                "openalex_id": None,
                "missing": True,
                "evidence_boundary": {
                    "bibliographic_metadata_only": True,
                    "supports_exact_theorem_statement_verified": False,
                    "quality_credit_granted": False,
                },
            }
            row["row_sha256"] = hash_without(row, "row_sha256")
            records.append(row)
    result: dict[str, Any] = {
        "schema_version": "awesome-theorems/openalex-theorem-reference-metadata/5.5",
        "observed_on": "2026-08-10",
        "source": {
            "api": API,
            "dataset_license": "CC0-1.0",
            "terms_url": "https://docs.openalex.org/download-all-data/openalex-snapshot",
        },
        "input": {
            "path": INPUT.relative_to(ROOT).as_posix(),
            "sha256": INPUT_SHA256,
            "doi_candidates": len(dois),
        },
        "policy": {
            "openalex_metadata_grants_theorem_support_credit": False,
            "human_exact_reference_and_scope_review_required": True,
        },
        "counts": {
            "requested_dois": len(dois),
            "resolved_dois": sum(record.get("openalex_id") is not None for record in records),
            "ambiguous_dois": sum(record.get("ambiguous") is True for record in records),
            "missing_dois": sum(record.get("missing") is True for record in records),
            "quality_credits": 0,
        },
        "set_digests": {
            "doi_set_sha256": set_digest(dois),
            "row_sha256_set_sha256": set_digest(record["row_sha256"] for record in records),
        },
        "records": records,
    }
    result["authority_sha256"] = hash_without(result, "authority_sha256")
    return result


def write_gzip(path: Path, document: Mapping[str, Any]) -> None:
    payload = canonical(document) + b"\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=9) as stream:
            stream.write(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="perform the bounded OpenAlex API fetch")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.fetch and args.check:
        raise MetadataError("--fetch and --check are mutually exclusive")
    if args.fetch:
        document = build(network=True)
        write_gzip(OUTPUT, document)
        print(
            f"wrote {OUTPUT} resolved={document['counts']['resolved_dois']} "
            f"ambiguous={document['counts']['ambiguous_dois']} "
            f"missing={document['counts']['missing_dois']} authority={document['authority_sha256']}"
        )
        return 0
    document = build(network=False)
    if document.get("input", {}).get("sha256") != INPUT_SHA256:
        raise MetadataError("pinned output input binding mismatch")
    if document.get("authority_sha256") != hash_without(document, "authority_sha256"):
        raise MetadataError("pinned output authority mismatch")
    records = document.get("records", [])
    if len(records) != 2_655 or any(record.get("row_sha256") != hash_without(record, "row_sha256") for record in records):
        raise MetadataError("pinned output record replay mismatch")
    counts = document.get("counts", {})
    partition = counts.get("resolved_dois", 0) + counts.get("ambiguous_dois", 0) + counts.get("missing_dois", 0)
    if partition != len(records) or counts.get("quality_credits") != 0:
        raise MetadataError("pinned output resolution partition mismatch")
    print(
        f"PASS OpenAlex metadata resolved={counts['resolved_dois']} "
        f"ambiguous={counts['ambiguous_dois']} missing={counts['missing_dois']} "
        f"authority={document['authority_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
