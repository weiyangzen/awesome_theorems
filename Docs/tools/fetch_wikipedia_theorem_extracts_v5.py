#!/usr/bin/env python3
"""Pin English-Wikipedia revisions, wikitext, and intro extracts for 1000+ identities.

The output is a gzip-compressed canonical JSON asset.  Each mutable title is
resolved through the MediaWiki action API and bound to a page id, revision id,
revision timestamp, MediaWiki SHA1, full revision wikitext, plaintext intro
extract bytes, and an attribution URL.
The asset is an input to later statement review; no extract is automatically
declared to be a complete theorem statement.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import time
from typing import Any, Iterable, Mapping
import urllib.error
import urllib.parse
import urllib.request


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = (
    REPO_ROOT / "Docs/catalog/v5/sources/1000-plus-theorems-8e04b97d.json"
)
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "Docs/catalog/v5/sources/wikipedia-en-1000-plus-revisions-20260810.json.gz"
)
API_ENDPOINT = "https://en.wikipedia.org/w/api.php"
SCHEMA_VERSION = "awesome-theorems/wikipedia-1000-plus-revision-extract/v5-intake-1"
SOURCE_SCHEMA = "awesome-theorems/1000-plus-theorem-source/v5-intake-1"
SOURCE_ASSET_SHA256 = "fe61d56e4ba4cc3a9846e2b153edee32dae6b1266b668e1a63dd3639d867bdad"
SOURCE_CONTENT_DIGEST = "17635bd3beefd7534fdd32df36be364f5540696fc424876c20296a59408eecd7"
EXPECTED_REQUESTED_TITLES = 1_205
EXPECTED_IDENTITY_ROWS = 1_200
USER_AGENT = (
    "awesome-theorems-source-audit/1.0 "
    "(https://github.com/sansha2000/awesome_theorems; source pinning)"
)


class FetchError(RuntimeError):
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


def chunks(values: list[str], size: int) -> Iterable[list[str]]:
    for start in range(0, len(values), size):
        yield values[start : start + size]


def load_source(path: Path) -> dict[str, Any]:
    if sha256_file(path) != SOURCE_ASSET_SHA256:
        raise FetchError("1000+ normalized source asset SHA-256 drifted")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise FetchError(f"cannot read {path}: {error}") from error
    if not isinstance(value, dict) or value.get("schema_version") != SOURCE_SCHEMA:
        raise FetchError("unexpected 1000+ normalized source schema")
    if value.get("content_digest_before_self_field") != SOURCE_CONTENT_DIGEST:
        raise FetchError("1000+ normalized source content digest drifted")
    rows = value.get("records")
    if not isinstance(rows, list) or len(rows) != EXPECTED_IDENTITY_ROWS:
        raise FetchError("1000+ normalized source must contain exactly 1,200 rows")
    return value


def request_batch(titles: list[str], retries: int, retry_delay: float) -> dict[str, Any]:
    parameters = {
        "action": "query",
        "explaintext": "1",
        "exintro": "1",
        "exlimit": "max",
        "exsectionformat": "plain",
        "format": "json",
        "formatversion": "2",
        "maxlag": "5",
        "prop": "revisions|extracts",
        "redirects": "1",
        "rvprop": "ids|timestamp|sha1|content",
        "rvslots": "main",
        "titles": "|".join(titles),
        "utf8": "1",
    }
    data = urllib.parse.urlencode(parameters).encode("utf-8")
    request = urllib.request.Request(
        API_ENDPOINT,
        data=data,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        method="POST",
    )
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                payload = response.read()
            value = json.loads(payload.decode("utf-8"))
            if not isinstance(value, dict):
                raise FetchError("MediaWiki response is not an object")
            if "error" in value:
                raise FetchError(f"MediaWiki API error: {value['error']!r}")
            if "continue" in value:
                raise FetchError("unexpected continuation from title/revision query")
            return value
        except (
            FetchError,
            OSError,
            UnicodeError,
            json.JSONDecodeError,
            urllib.error.URLError,
        ) as error:
            last_error = error
            if attempt == retries:
                break
            time.sleep(retry_delay * (attempt + 1))
    raise FetchError(f"MediaWiki request failed after {retries + 1} attempts: {last_error}")


def cache_path(cache_dir: Path, batch_index: int) -> Path:
    return cache_dir / f"batch-{batch_index:03d}.json"


def load_or_fetch_batch(
    titles: list[str],
    batch_index: int,
    cache_dir: Path | None,
    retries: int,
    retry_delay: float,
) -> dict[str, Any]:
    expected_digest = sha256_bytes(canonical_json_bytes(titles))
    if cache_dir is not None:
        path = cache_path(cache_dir, batch_index)
        if path.exists():
            try:
                envelope = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as error:
                raise FetchError(f"cannot load raw response cache {path}: {error}") from error
            if envelope.get("requested_titles_sha256") != expected_digest:
                raise FetchError(f"raw response cache title digest mismatch: {path}")
            response = envelope.get("response")
            if not isinstance(response, dict):
                raise FetchError(f"raw response cache lacks object response: {path}")
            return response
    response = request_batch(titles, retries, retry_delay)
    if cache_dir is not None:
        cache_dir.mkdir(parents=True, exist_ok=True)
        envelope = {
            "requested_titles": titles,
            "requested_titles_sha256": expected_digest,
            "response": response,
        }
        cache_path(cache_dir, batch_index).write_text(
            json.dumps(envelope, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return response


def response_resolution(
    response: Mapping[str, Any], requested_titles: list[str]
) -> tuple[list[dict[str, Any]], dict[int, dict[str, Any]]]:
    query = response.get("query")
    if not isinstance(query, dict):
        raise FetchError("MediaWiki response lacks query object")
    normalizations: dict[str, str] = {}
    for row in query.get("normalized", []):
        if not isinstance(row, dict) or not isinstance(row.get("from"), str) or not isinstance(
            row.get("to"), str
        ):
            raise FetchError("invalid MediaWiki normalization row")
        normalizations[row["from"]] = row["to"]
    redirects: dict[str, str] = {}
    for row in query.get("redirects", []):
        if not isinstance(row, dict) or not isinstance(row.get("from"), str) or not isinstance(
            row.get("to"), str
        ):
            raise FetchError("invalid MediaWiki redirect row")
        redirects[row["from"]] = row["to"]
    pages = query.get("pages")
    if not isinstance(pages, list):
        raise FetchError("MediaWiki response lacks pages list")
    by_title: dict[str, dict[str, Any]] = {}
    page_records: dict[int, dict[str, Any]] = {}
    for page in pages:
        if not isinstance(page, dict) or not isinstance(page.get("title"), str):
            raise FetchError("invalid MediaWiki page row")
        by_title[page["title"]] = page
        if page.get("missing") is not True and isinstance(page.get("pageid"), int):
            page_records[page["pageid"]] = page

    result: list[dict[str, Any]] = []
    for requested in requested_titles:
        normalized = normalizations.get(requested, requested)
        chain: list[str] = []
        resolved = normalized
        seen: set[str] = set()
        while resolved in redirects:
            if resolved in seen:
                raise FetchError(f"redirect cycle for {requested!r}")
            seen.add(resolved)
            chain.append(resolved)
            resolved = redirects[resolved]
        page = by_title.get(resolved)
        if page is None:
            raise FetchError(f"no page result for requested title {requested!r} -> {resolved!r}")
        if page.get("missing") is True or not isinstance(page.get("pageid"), int):
            row: dict[str, Any] = {
                "normalized_title": normalized,
                "requested_title": requested,
                "resolution_status": "missing",
                "resolved_title": resolved,
            }
        else:
            revisions = page.get("revisions")
            if not isinstance(revisions, list) or len(revisions) != 1:
                raise FetchError(f"page {resolved!r} lacks exactly one current revision")
            revision = revisions[0]
            extract = page.get("extract")
            required = ("revid", "parentid", "timestamp", "sha1")
            if not isinstance(revision, dict) or any(key not in revision for key in required):
                raise FetchError(f"page {resolved!r} has incomplete revision metadata")
            if not isinstance(extract, str):
                raise FetchError(f"page {resolved!r} lacks plaintext extract")
            row = {
                "normalized_title": normalized,
                "page_id": page["pageid"],
                "requested_title": requested,
                "resolution_status": "resolved",
                "resolved_title": page["title"],
                "revision_id": revision["revid"],
            }
        if chain:
            row["redirect_chain"] = chain + [resolved]
        else:
            row["redirect_chain"] = []
        row["row_sha256"] = hash_without(row, "row_sha256")
        result.append(row)
    return result, page_records


def build_artifact(
    source: Mapping[str, Any],
    cache_dir: Path | None,
    batch_size: int,
    retries: int,
    retry_delay: float,
) -> dict[str, Any]:
    rows = source["records"]
    requested_titles = sorted(
        {
            target["requested_title"]
            for row in rows
            for target in row["wikipedia_targets"]
            if target["requested_title"] is not None
        },
        key=lambda value: value.encode("utf-8"),
    )
    if len(requested_titles) != EXPECTED_REQUESTED_TITLES:
        raise FetchError(
            f"source exposes {len(requested_titles)} requested titles, expected 1,205"
        )
    all_resolutions: list[dict[str, Any]] = []
    raw_pages: dict[int, dict[str, Any]] = {}
    for batch_index, batch in enumerate(chunks(requested_titles, batch_size)):
        response = load_or_fetch_batch(
            batch, batch_index, cache_dir, retries, retry_delay
        )
        resolutions, pages = response_resolution(response, batch)
        all_resolutions.extend(resolutions)
        for page_id, page in pages.items():
            previous = raw_pages.get(page_id)
            if previous is not None and previous != page:
                raise FetchError(f"page {page_id} changed between batches")
            raw_pages[page_id] = page
    all_resolutions.sort(key=lambda row: row["requested_title"].encode("utf-8"))

    page_assets: list[dict[str, Any]] = []
    for page_id, raw in sorted(raw_pages.items()):
        revisions = raw["revisions"]
        revision = revisions[0]
        extract = raw["extract"]
        slots = revision.get("slots")
        main_slot = slots.get("main") if isinstance(slots, dict) else None
        wikitext = main_slot.get("content") if isinstance(main_slot, dict) else None
        if not isinstance(wikitext, str):
            raise FetchError(f"page {raw['title']!r} lacks pinned main-slot wikitext")
        extract_bytes = extract.encode("utf-8")
        wikitext_bytes = wikitext.encode("utf-8")
        page: dict[str, Any] = {
            "attribution_url": f"https://en.wikipedia.org/?oldid={revision['revid']}",
            "extract": extract,
            "extract_sha256": sha256_bytes(extract_bytes),
            "extract_size_bytes": len(extract_bytes),
            "mediawiki_revision_sha1": revision["sha1"],
            "page_id": page_id,
            "parent_revision_id": revision["parentid"],
            "resolved_title": raw["title"],
            "revision_id": revision["revid"],
            "revision_timestamp": revision["timestamp"],
            "wikitext": wikitext,
            "wikitext_sha256": sha256_bytes(wikitext_bytes),
            "wikitext_size_bytes": len(wikitext_bytes),
        }
        page["row_sha256"] = hash_without(page, "row_sha256")
        page_assets.append(page)
    page_by_id = {page["page_id"]: page for page in page_assets}
    resolution_by_title = {row["requested_title"]: row for row in all_resolutions}

    identity_resolution: list[dict[str, Any]] = []
    identities_with_resolved = 0
    identities_with_nonempty_extract = 0
    for source_row in rows:
        requested = sorted(
            {
                target["requested_title"]
                for target in source_row["wikipedia_targets"]
                if target["requested_title"] is not None
            },
            key=lambda value: value.encode("utf-8"),
        )
        resolution_rows = [resolution_by_title[title] for title in requested]
        resolved_ids = sorted(
            {
                row["page_id"]
                for row in resolution_rows
                if row["resolution_status"] == "resolved"
            }
        )
        if resolved_ids:
            identities_with_resolved += 1
        if any(page_by_id[page_id]["extract_size_bytes"] > 0 for page_id in resolved_ids):
            identities_with_nonempty_extract += 1
        identity: dict[str, Any] = {
            "external_id": source_row["external_id"],
            "resolved_page_ids": resolved_ids,
            "source_record_id": source_row["source_record_id"],
            "source_row_sha256": source_row["row_sha256"],
            "unresolved_requested_titles": [
                row["requested_title"]
                for row in resolution_rows
                if row["resolution_status"] != "resolved"
            ],
        }
        identity["row_sha256"] = hash_without(identity, "row_sha256")
        identity_resolution.append(identity)

    status_counts = Counter(row["resolution_status"] for row in all_resolutions)
    artifact: dict[str, Any] = {
        "api_snapshot": {
            "batch_size": batch_size,
            "endpoint": API_ENDPOINT,
            "parameters": {
                "explaintext": 1,
                "exintro": 1,
                "exlimit": "max",
                "exsectionformat": "plain",
                "formatversion": 2,
                "prop": "revisions|extracts",
                "redirects": 1,
                "rvprop": "ids|timestamp|sha1|content",
                "rvslots": "main",
            },
            "retrieval_date_utc": "2026-08-10",
            "user_agent": USER_AGENT,
        },
        "counts": {
            "identities": len(identity_resolution),
            "identities_with_nonempty_extract": identities_with_nonempty_extract,
            "identities_with_resolved_page": identities_with_resolved,
            "missing_requested_titles": status_counts["missing"],
            "requested_titles": len(all_resolutions),
            "resolved_requested_titles": status_counts["resolved"],
            "unique_resolved_pages": len(page_assets),
        },
        "identity_resolution": identity_resolution,
        "pages": page_assets,
        "policy": {
            "automatic_complete_statement_credit": False,
            "api_plaintext_extract_scope": "intro_only",
            "purpose": "revision_pinned_wikitext_and_intro_statement_review_candidate_pool",
            "review_requirement": (
                "A reviewer must bind an exact complete theorem statement and conditions; "
                "page or extract presence alone grants no theorem or importance credit."
            ),
        },
        "rights": {
            "attribution": "English Wikipedia contributors; per-page oldid URLs are retained",
            "catalog_relicenses_source": False,
            "license": "CC-BY-SA-4.0",
            "terms_url": "https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use",
            "use": "revision_pinned_wikitext_and_plaintext_intro_for_statement_review",
        },
        "schema_version": SCHEMA_VERSION,
        "source_asset": {
            "content_digest_before_self_field": SOURCE_CONTENT_DIGEST,
            "path": "Docs/catalog/v5/sources/1000-plus-theorems-8e04b97d.json",
            "schema_version": SOURCE_SCHEMA,
            "sha256": SOURCE_ASSET_SHA256,
        },
        "title_resolution": all_resolutions,
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
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--cache-dir", type=Path)
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--retries", type=int, default=4)
    parser.add_argument("--retry-delay", type=float, default=2.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 1 <= args.batch_size <= 20:
        print("Wikipedia pin failed: --batch-size must be in 1..20 (extracts API limit)")
        return 1
    try:
        source = load_source(args.source.resolve())
        artifact = build_artifact(
            source,
            args.cache_dir.resolve() if args.cache_dir else None,
            args.batch_size,
            args.retries,
            args.retry_delay,
        )
        raw = encoded_document(artifact)
        compressed = gzip_bytes(raw)
        atomic_write(args.output.resolve(), compressed)
        counts = artifact["counts"]
        print(
            f"wrote {args.output}: requested={counts['requested_titles']} "
            f"resolved={counts['resolved_requested_titles']} "
            f"identities={counts['identities_with_resolved_page']} "
            f"pages={counts['unique_resolved_pages']} "
            f"sha256={sha256_bytes(compressed)}"
        )
    except (FetchError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"Wikipedia pin failed: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
