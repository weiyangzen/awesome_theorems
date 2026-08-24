#!/usr/bin/env python3
"""Extract the pinned 1000+ Theorems archive into a closed identity asset.

This tool deliberately extracts theorem *identities and source mappings*, not
mathematical truth or universal importance.  The input is the repository's
content-pinned git archive; no network request or mutable checkout is used.
"""

from __future__ import annotations

import argparse
from collections import Counter
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import tarfile
from typing import Any, Iterable, Mapping
import unicodedata

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ARCHIVE = (
    REPO_ROOT
    / "Docs/catalog/v5/sources/1000-plus-theorems-8e04b97d.tar.gz"
)
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "Docs/catalog/v5/sources/1000-plus-theorems-8e04b97d.json"
)

SCHEMA_VERSION = "awesome-theorems/1000-plus-theorem-source/v5-intake-1"
SOURCE_ID = "SRC-MATH-V5-1000-PLUS-8E04B97D"
REPOSITORY = "https://github.com/1000-plus/1000-plus.github.io.git"
COMMIT = "8e04b97dd24adc6e931be78a884da7e935bc8780"
TREE = "c6bba9af8736f82b29ad6c947a20c245beb26263"
COMMIT_DATE = "2026-07-22T16:23:18+02:00"
ARCHIVE_SHA256 = "3338fac218b0124fd66c77e7a589bb002b653b2d7c0f87f789d6884a256719cf"
ARCHIVE_SIZE_BYTES = 82_748
ARCHIVE_MEMBERS = 1_224
ARCHIVE_REGULAR_MEMBERS = 1_216
THEOREM_MEMBERS = 1_200
ROOT_PREFIX = "1000-plus-8e04b97d/"
LICENSE = "Unlicense"
LICENSE_MEMBER = ROOT_PREFIX + "LICENSE"
LICENSE_SHA256 = "6b0382b16279f26ff69014300541967a356a666eb0b91b422f6862f6b7dad17e"

ASSISTANTS = ("hol_light", "isabelle", "lean", "metamath", "mizar", "rocq")
MAPPING_KEYS = {
    "authors",
    "comment",
    "date",
    "identifiers",
    "library",
    "status",
    "url",
}
TOP_LEVEL_KEYS = {
    "hol_light",
    "id_suffix",
    "isabelle",
    "lean",
    "metamath",
    "mizar",
    "msc_classification",
    "rocq",
    "wikidata",
    "wikipedia_links",
}
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
WIKIDATA_RE = re.compile(r"Q[1-9][0-9]*")
EXTERNAL_ID_RE = re.compile(r"Q[1-9][0-9]*(?:[A-Z])?")


class ExtractionError(RuntimeError):
    pass


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ExtractionError(f"value is not canonical-JSON serializable: {error}") from error


def encoded_document(value: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        + "\n"
    ).encode("utf-8")


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


def normalize_scalar(value: Any, label: str) -> str:
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, (str, int)) and not isinstance(value, bool):
        return str(value)
    raise ExtractionError(f"{label} must be a string, integer, or YAML date")


def normalize_string_list(value: Any, label: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ExtractionError(f"{label} must be a list")
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, (str, int)) or isinstance(item, bool):
            raise ExtractionError(f"{label}[{index}] must be a string or integer")
        text = str(item).strip()
        if not text:
            raise ExtractionError(f"{label}[{index}] is empty")
        result.append(text)
    return result


def wikipedia_target(raw: str) -> dict[str, Any]:
    match = WIKILINK_RE.search(raw)
    syntax = "wikilink" if match else "invalid_plain_text"
    inner = match.group(1) if match else raw
    if "|" in inner:
        target, display = inner.split("|", 1)
    else:
        target, display = inner, None
    if "#" in target:
        page_title, fragment = target.split("#", 1)
    else:
        page_title, fragment = target, None
    normalized_title = unicodedata.normalize(
        "NFC", " ".join(page_title.replace("_", " ").split())
    ).strip()
    if not normalized_title:
        raise ExtractionError(f"empty Wikipedia target in {raw!r}")
    requested_title = normalized_title if match else None
    return {
        "display_text": display.strip() if display and display.strip() else None,
        "fragment": fragment.strip() if fragment and fragment.strip() else None,
        "raw": raw,
        "requested_title": requested_title,
        "syntax": syntax,
    }


def parse_front_matter(payload: bytes, member: str) -> tuple[dict[str, Any], str]:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ExtractionError(f"{member} is not UTF-8: {error}") from error
    parts = re.split(r"^---\s*$", text, flags=re.MULTILINE)
    if len(parts) != 3 or parts[0].strip() or parts[2].strip():
        raise ExtractionError(f"{member} must contain exactly one bounded front-matter block")
    title_match = TITLE_RE.search(parts[1])
    if title_match is None:
        raise ExtractionError(f"{member} lacks a '# title' line")
    title = unicodedata.normalize("NFC", title_match.group(1).strip())
    try:
        value = yaml.safe_load(parts[1])
    except yaml.YAMLError as error:
        raise ExtractionError(f"invalid YAML in {member}: {error}") from error
    if not isinstance(value, dict):
        raise ExtractionError(f"{member} front matter must decode to an object")
    unknown = set(value) - TOP_LEVEL_KEYS
    if unknown:
        raise ExtractionError(f"{member} has unknown fields: {sorted(unknown)}")
    return value, title


def normalize_mapping(raw: Any, assistant: str, member: str, ordinal: int) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ExtractionError(f"{member} {assistant}[{ordinal}] must be an object")
    unknown = set(raw) - MAPPING_KEYS
    if unknown:
        raise ExtractionError(
            f"{member} {assistant}[{ordinal}] has unknown fields: {sorted(unknown)}"
        )
    status = raw.get("status")
    library = raw.get("library")
    url = raw.get("url")
    if status not in {"formalized", "statement"}:
        raise ExtractionError(f"{member} {assistant}[{ordinal}] has invalid status")
    if library not in {"L", "S", "X"}:
        raise ExtractionError(f"{member} {assistant}[{ordinal}] has invalid library")
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        raise ExtractionError(f"{member} {assistant}[{ordinal}] has invalid URL")
    result = {
        "assistant": assistant,
        "authors": normalize_string_list(raw.get("authors"), "authors"),
        "comment": str(raw["comment"]) if raw.get("comment") is not None else None,
        "date": normalize_scalar(raw["date"], "date") if raw.get("date") is not None else None,
        "identifiers": normalize_string_list(raw.get("identifiers"), "identifiers"),
        "library": library,
        "status": status,
        "url": url,
    }
    return result


def regular_member_manifest(archive: tarfile.TarFile) -> tuple[list[dict[str, Any]], dict[str, bytes]]:
    manifest: list[dict[str, Any]] = []
    payloads: dict[str, bytes] = {}
    members = archive.getmembers()
    if len(members) != ARCHIVE_MEMBERS:
        raise ExtractionError(
            f"archive has {len(members)} members, expected {ARCHIVE_MEMBERS}"
        )
    names: set[str] = set()
    for member in members:
        path = PurePosixPath(member.name)
        if member.name in names:
            raise ExtractionError(f"duplicate archive member {member.name}")
        names.add(member.name)
        in_root = member.name == ROOT_PREFIX.rstrip("/") or member.name.startswith(ROOT_PREFIX)
        if path.is_absolute() or ".." in path.parts or not in_root:
            raise ExtractionError(f"unsafe archive member {member.name}")
        if member.isfile():
            stream = archive.extractfile(member)
            if stream is None:
                raise ExtractionError(f"cannot read archive member {member.name}")
            payload = stream.read()
            if len(payload) != member.size:
                raise ExtractionError(f"short read for archive member {member.name}")
            payloads[member.name] = payload
            manifest.append(
                {
                    "member": member.name,
                    "sha256": sha256_bytes(payload),
                    "size_bytes": len(payload),
                }
            )
        elif not member.isdir():
            raise ExtractionError(f"archive member {member.name} is not a regular file/directory")
    manifest.sort(key=lambda row: row["member"].encode("utf-8"))
    if len(manifest) != ARCHIVE_REGULAR_MEMBERS:
        raise ExtractionError(
            f"archive has {len(manifest)} regular members, expected {ARCHIVE_REGULAR_MEMBERS}"
        )
    return manifest, payloads


def theorem_members(payloads: Mapping[str, bytes]) -> list[str]:
    pattern = re.compile(
        "^" + re.escape(ROOT_PREFIX) + r"_thm/Q[1-9][0-9]*[A-Z]?\.md$"
    )
    result = sorted(
        (member for member in payloads if pattern.fullmatch(member)),
        key=lambda value: value.encode("utf-8"),
    )
    if len(result) != THEOREM_MEMBERS:
        raise ExtractionError(
            f"archive has {len(result)} theorem members, expected {THEOREM_MEMBERS}"
        )
    return result


def build_artifact(archive_path: Path) -> dict[str, Any]:
    if sha256_file(archive_path) != ARCHIVE_SHA256:
        raise ExtractionError("1000+ archive SHA-256 does not match the pinned source")
    if archive_path.stat().st_size != ARCHIVE_SIZE_BYTES:
        raise ExtractionError("1000+ archive size does not match the pinned source")
    try:
        with tarfile.open(archive_path, mode="r:gz") as archive:
            manifest, payloads = regular_member_manifest(archive)
    except (OSError, tarfile.TarError) as error:
        raise ExtractionError(f"cannot read {archive_path}: {error}") from error
    if sha256_bytes(payloads[LICENSE_MEMBER]) != LICENSE_SHA256:
        raise ExtractionError("pinned 1000+ license member hash changed")

    records: list[dict[str, Any]] = []
    external_ids: set[str] = set()
    mapping_counts: Counter[str] = Counter()
    requested_titles: set[str] = set()
    for rank, member in enumerate(theorem_members(payloads), start=1):
        raw = payloads[member]
        data, title = parse_front_matter(raw, member)
        wikidata = data.get("wikidata")
        suffix = data.get("id_suffix", "")
        msc = data.get("msc_classification")
        links = data.get("wikipedia_links")
        if not isinstance(wikidata, str) or not WIKIDATA_RE.fullmatch(wikidata):
            raise ExtractionError(f"{member} has invalid wikidata identity")
        if not isinstance(suffix, str) or suffix not in {"", "A", "B", "X"}:
            raise ExtractionError(f"{member} has invalid id_suffix")
        external_id = wikidata + suffix
        if not EXTERNAL_ID_RE.fullmatch(external_id) or external_id in external_ids:
            raise ExtractionError(f"{member} has duplicate/invalid external identity")
        external_ids.add(external_id)
        if PurePosixPath(member).stem != external_id:
            raise ExtractionError(f"{member} filename disagrees with {external_id}")
        if not isinstance(msc, str) or not re.fullmatch(r"[0-9]{2}", msc):
            raise ExtractionError(f"{member} has invalid MSC class")
        if not isinstance(links, list) or not links or not all(
            isinstance(link, str) and link.strip() for link in links
        ):
            raise ExtractionError(f"{member} has invalid wikipedia_links")
        wiki_targets = [wikipedia_target(link) for link in links]
        requested_titles.update(
            target["requested_title"]
            for target in wiki_targets
            if target["requested_title"] is not None
        )

        mappings: list[dict[str, Any]] = []
        for assistant in ASSISTANTS:
            raw_mappings = data.get(assistant, [])
            if not isinstance(raw_mappings, list):
                raise ExtractionError(f"{member} field {assistant} must be a list")
            for ordinal, raw_mapping in enumerate(raw_mappings):
                mapping = normalize_mapping(raw_mapping, assistant, member, ordinal)
                mappings.append(mapping)
                mapping_counts["entries"] += 1
                mapping_counts[f"assistant:{assistant}"] += 1
                mapping_counts[f"status:{mapping['status']}"] += 1
        mappings.sort(
            key=lambda row: canonical_json_bytes(row)
        )
        row: dict[str, Any] = {
            "external_id": external_id,
            "id_suffix": suffix or None,
            "identity_evidence": {
                "basis": "listed_in_1000_plus_snapshot_derived_from_wikipedia_list_of_theorems",
                "independent_universal_importance_ranking_claimed": False,
                "signal_level": "encyclopedic_named_theorem_identity",
            },
            "msc2020": msc,
            "proof_assistant_mappings": mappings,
            "selection_rank": rank,
            "source": {
                "archive_member": member,
                "member_sha256": sha256_bytes(raw),
                "member_size_bytes": len(raw),
            },
            "source_record_id": "TP1K-" + external_id,
            "title": title,
            "wikidata_id": wikidata,
            "wikipedia_targets": wiki_targets,
        }
        row["row_sha256"] = hash_without(row, "row_sha256")
        records.append(row)

    records_with_mappings = sum(bool(row["proof_assistant_mappings"]) for row in records)
    records_with_formalized = sum(
        any(mapping["status"] == "formalized" for mapping in row["proof_assistant_mappings"])
        for row in records
    )
    records_statement_only = sum(
        bool(row["proof_assistant_mappings"])
        and all(mapping["status"] == "statement" for mapping in row["proof_assistant_mappings"])
        for row in records
    )
    manifest_sha256 = sha256_bytes(canonical_json_bytes(manifest))
    artifact: dict[str, Any] = {
        "counts": {
            "formalized_mapping_entries": mapping_counts["status:formalized"],
            "mapping_entries": mapping_counts["entries"],
            "mapping_entries_by_assistant": {
                assistant: mapping_counts[f"assistant:{assistant}"] for assistant in ASSISTANTS
            },
            "records": len(records),
            "records_statement_only": records_statement_only,
            "records_with_formalized_mapping": records_with_formalized,
            "records_with_proof_assistant_mapping": records_with_mappings,
            "statement_mapping_entries": mapping_counts["status:statement"],
            "unique_requested_wikipedia_titles": len(requested_titles),
            "valid_wikipedia_link_entries": sum(
                target["requested_title"] is not None
                for row in records
                for target in row["wikipedia_targets"]
            ),
            "wikipedia_link_field_entries": sum(
                len(row["wikipedia_targets"]) for row in records
            ),
        },
        "extraction_policy": {
            "ordering": "UTF-8 bytewise archive member path",
            "scope": "identity_metadata_and_proof_assistant_mappings_only",
            "statement_or_truth_inferred": False,
            "title_source": "level-one Markdown heading inside YAML front matter",
            "wikipedia_target_normalization": (
                "parse first wikilink when present; drop display label and section fragment; "
                "replace underscores; collapse whitespace; NFC"
            ),
        },
        "generator": {
            "path": "Docs/tools/extract_1000_plus_theorems_v5.py",
            "version": "1.0.0",
        },
        "records": records,
        "rights": {
            "attribution": "1000+ Theorems contributors",
            "catalog_relicenses_source": False,
            "license": LICENSE,
            "license_member": LICENSE_MEMBER,
            "license_member_sha256": LICENSE_SHA256,
            "use": "source_identity_metadata_and_formalization_crosswalk",
        },
        "schema_version": SCHEMA_VERSION,
        "source_snapshot": {
            "archive_member_manifest_sha256": manifest_sha256,
            "archive_members": ARCHIVE_MEMBERS,
            "archive_path": "Docs/catalog/v5/sources/1000-plus-theorems-8e04b97d.tar.gz",
            "archive_regular_members": ARCHIVE_REGULAR_MEMBERS,
            "archive_sha256": ARCHIVE_SHA256,
            "archive_size_bytes": ARCHIVE_SIZE_BYTES,
            "commit": COMMIT,
            "commit_date": COMMIT_DATE,
            "repository": REPOSITORY,
            "root_prefix": ROOT_PREFIX,
            "source_id": SOURCE_ID,
            "theorem_members": THEOREM_MEMBERS,
            "tree": TREE,
        },
    }
    artifact["content_digest_before_self_field"] = hash_without(
        artifact, "content_digest_before_self_field"
    )
    return artifact


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(payload)
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="compare rebuilt bytes to --output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = encoded_document(build_artifact(args.archive.resolve()))
        if args.check:
            actual = args.output.resolve().read_bytes()
            if actual != payload:
                raise ExtractionError(f"{args.output} is stale; deterministic rebuild differs")
            print(
                f"1000+ source asset PASS: records={THEOREM_MEMBERS} "
                f"sha256={sha256_bytes(actual)}"
            )
        else:
            atomic_write(args.output.resolve(), payload)
            print(
                f"wrote {args.output}: records={THEOREM_MEMBERS} "
                f"sha256={sha256_bytes(payload)}"
            )
    except (ExtractionError, OSError, tarfile.TarError, yaml.YAMLError) as error:
        print(f"1000+ source extraction failed: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
