#!/usr/bin/env python3
"""Freeze and validate the full ConjectureBench Stage5 occurrence pool.

This builder deliberately creates a source-occurrence intake authority, not a
Stage5 catalog release and not a strict-conjecture ledger.  Every source record
keeps its own status and review boundary; no S5-CLM or Stage6 identity is
allocated here.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tarfile
import tempfile
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[4]
CATALOG = ROOT / "Docs/catalog/v5"
SOURCE_ARCHIVE = CATALOG / "sources/conjecturebench-357bcb1a-full-source.tar.gz"
POOL_ROOT = CATALOG / "pools/conjecturebench-357bcb1a"
OCCURRENCES = POOL_ROOT / "Source_Occurrence_Pool.jsonl"
IDENTITIES = POOL_ROOT / "Identity_Registry.jsonl"
MANIFEST = POOL_ROOT / "Pool_Manifest.json"
CURRENT = CATALOG / "pools/Current_Pool_Release.json"

REPOSITORY = "https://github.com/bespokelabsai/conjecture-bench"
COMMIT = "357bcb1a1daf93917d42e8206ceaa55645729a09"
TREE_SHA1 = "ce1e057720604415124e20cf4c24486a4fd8cd30"
ARCHIVE_SHA256 = "9e0493e5b67767f6636c5518d6bca7326b971dda54a6df237084c51151da2ead"
ARCHIVE_SIZE_BYTES = 1_801_907
TOP_LEVEL = f"conjecture-bench-{COMMIT}"
EXPECTED_COUNTS = {"curated": 302, "family": 9_342, "catalog": 5_221}
EXPECTED_STATUS_COUNTS = {
    "open": 12_427,
    "listed-unsolved": 1_227,
    "research open": 1_031,
    "listed-open": 94,
    "reported-answered-by-source": 80,
    "partially-open": 3,
    "status-contested": 1,
    "conflicting-status-categories": 1,
    "unclear": 1,
}
ACTIVE_STATUS = frozenset({"open", "listed-unsolved", "research open", "listed-open", "partially-open"})
SOURCE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,191}$")


class PoolError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def seal(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "authority_sha256": sha256(canonical(body))}


def strict_json(raw: bytes, label: str) -> Any:
    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise PoolError(f"{label}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    def reject(value: str) -> Any:
        raise PoolError(f"{label}: non-finite JSON number {value}")

    try:
        return json.loads(raw, object_pairs_hook=pairs_hook, parse_constant=reject)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PoolError(f"{label}: invalid strict UTF-8 JSON") from exc


def jsonl_bytes(rows: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(canonical(row) + b"\n" for row in rows)


def atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix=f".{path.name}.", dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(raw)
        stream.flush()
    try:
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def safe_members(archive: tarfile.TarFile) -> dict[str, tarfile.TarInfo]:
    members: dict[str, tarfile.TarInfo] = {}
    for member in archive.getmembers():
        path = PurePosixPath(member.name)
        if path.is_absolute() or ".." in path.parts or member.issym() or member.islnk():
            raise PoolError(f"unsafe archive member: {member.name}")
        if member.isfile():
            if member.name in members:
                raise PoolError(f"duplicate archive member: {member.name}")
            members[member.name] = member
        elif not member.isdir():
            raise PoolError(f"unsupported archive member type: {member.name}")
    return members


def member_bytes(archive: tarfile.TarFile, members: dict[str, tarfile.TarInfo], relative: str) -> bytes:
    name = f"{TOP_LEVEL}/{relative}"
    member = members.get(name)
    if member is None:
        raise PoolError(f"missing archive member: {relative}")
    stream = archive.extractfile(member)
    if stream is None:
        raise PoolError(f"unreadable archive member: {relative}")
    return stream.read()


def statement_metadata(kind: str, record: dict[str, Any]) -> tuple[str, str | None, bool | None]:
    statement = record.get("statement")
    if kind in {"curated", "family"}:
        text = statement if isinstance(statement, str) else None
        return ("text" if text is not None else "missing", sha256(text.encode("utf-8")) if text is not None else None, False if text is not None else None)
    if isinstance(statement, dict):
        text = statement.get("text")
        representation = statement.get("representation")
        return (str(representation or "text") if isinstance(text, str) else "pointer", sha256(text.encode("utf-8")) if isinstance(text, str) else None, statement.get("contains_placeholder") if isinstance(statement.get("contains_placeholder"), bool) else None)
    return "pointer", None, None


def rights_class(kind: str, source: str | None) -> str:
    if kind == "family":
        return (
            "cc_by_4_0_source_attribution_required"
            if source == "ljcr-difference-sets"
            else "no_formal_upstream_license_metadata_only_or_pointer_required"
        )
    if kind == "catalog":
        return {
            "unsolvedmath-1.1.0": "cc_by_4_0_source_attribution_required",
            "egres-open": "cc_by_3_0_source_attribution_required",
            "formal-conjectures-bench-v1": "apache_2_0_source_attribution_required",
            "erdos-problems": "apache_2_0_metadata_status_pointer_only",
            "kourovka-notebook": "copyrighted_no_general_license_pointer_or_individual_review_required",
            "open-problems-project": "no_stated_text_license_pointer_or_individual_review_required",
        }.get(str(source), "source_specific_notice_or_pointer_boundary")
    return "bespoke_record_layer_cc_by_4_0_upstream_rights_not_inherited"


def occurrence(
    ordinal: int,
    *,
    kind: str,
    record: dict[str, Any],
    record_path: str,
    container_index: int | None,
) -> dict[str, Any]:
    source_id = record.get("id")
    if not isinstance(source_id, str) or not SOURCE_ID_RE.fullmatch(source_id):
        raise PoolError(f"{record_path}: invalid source ID")
    if kind == "curated":
        status_obj = record.get("status_observation") or {}
        source = (record.get("provenance") or {}).get("collection")
        related = [record["duplicate_of"]] if isinstance(record.get("duplicate_of"), str) else []
        review_flags: list[str] = []
    elif kind == "family":
        status_obj = record.get("status") or {}
        source = record_path.split("/")[2]
        related = []
        review_flags = []
    else:
        status_obj = record.get("status_observation") or {}
        source = record.get("source_registry")
        related = record.get("related_conjecture_ids") or []
        review_flags = record.get("review_flags") or []
    if not isinstance(status_obj, dict) or not isinstance(status_obj.get("state"), str):
        raise PoolError(f"{record_path}: status observation is missing")
    if not isinstance(related, list) or any(not isinstance(item, str) for item in related):
        raise PoolError(f"{record_path}: related IDs are malformed")
    if not isinstance(review_flags, list) or any(not isinstance(item, str) for item in review_flags):
        raise PoolError(f"{record_path}: review flags are malformed")
    representation, statement_sha, contains_placeholder = statement_metadata(kind, record)
    body = {
        "schema_version": "awesome-theorems/stage5-conjecture-source-occurrence/1.0",
        "pool_id": f"S5POOL-{ordinal:08d}",
        # This is the cross-snapshot logical source identity.  The immutable
        # occurrence version is bound separately by source_commit/path/hash;
        # a new upstream snapshot must not manufacture a new logical key.
        "stable_source_key": f"conjecturebench/{kind}/{source_id}",
        "source_repository": REPOSITORY,
        "source_commit": COMMIT,
        "kind": kind,
        "source_native_id": source_id,
        "title": record.get("title"),
        "source_collection": source,
        "record_path": record_path,
        "family_container_index": container_index,
        "canonical_record_sha256": sha256(canonical(record)),
        "source_status": status_obj.get("state"),
        "status_as_of": status_obj.get("as_of"),
        "source_observed_active_candidate": status_obj.get("state") in ACTIVE_STATUS,
        "statement_presence": representation,
        "statement_sha256": statement_sha,
        "contains_placeholder": contains_placeholder,
        "review_flags": review_flags,
        "related_source_ids": related,
        "rights_class": rights_class(kind, source if isinstance(source, str) else None),
        "strict_credit": False,
        "independent_current_open_verified": False,
        "stage5_claim_id": None,
        "stage6_alias": None,
        "execution_admission": "intake_status_rights_dedupe_only",
    }
    return seal(body)


def build_rows(path: Path) -> tuple[list[dict[str, Any]], str, int]:
    if path.is_symlink() or not path.is_file():
        raise PoolError(f"missing regular source archive: {path}")
    if path.stat().st_size != ARCHIVE_SIZE_BYTES or file_sha256(path) != ARCHIVE_SHA256:
        raise PoolError("full ConjectureBench archive size/SHA-256 differs")
    rows: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    with tarfile.open(path, "r:gz") as archive:
        members = safe_members(archive)
        table_raw = member_bytes(archive, members, "problems/tables/all.csv")
        reader = csv.DictReader(io.StringIO(table_raw.decode("utf-8")))
        table_rows = list(reader)
        if len(table_rows) != 14_865 or reader.fieldnames != ["id", "kind", "title", "source", "family", "status"]:
            raise PoolError("all.csv schema/cardinality differs")

        curated_paths = sorted(
            name.removeprefix(f"{TOP_LEVEL}/")
            for name in members
            if re.fullmatch(re.escape(TOP_LEVEL) + r"/problems/conjectures/cb-[0-9]{4}\.json", name)
        )
        family_paths = sorted(
            name.removeprefix(f"{TOP_LEVEL}/")
            for name in members
            if re.fullmatch(re.escape(TOP_LEVEL) + r"/problems/families/[^/]+/records\.json", name)
        )
        catalog_paths = sorted(
            name.removeprefix(f"{TOP_LEVEL}/")
            for name in members
            if re.fullmatch(re.escape(TOP_LEVEL) + r"/problems/extended-catalog/[^/]+/[^/]+\.json", name)
        )
        records: list[tuple[str, dict[str, Any], str, int | None]] = []
        for relative in curated_paths:
            value = strict_json(member_bytes(archive, members, relative), relative)
            if not isinstance(value, dict):
                raise PoolError(f"{relative}: expected object")
            records.append(("curated", value, relative, None))
        for relative in family_paths:
            payload = strict_json(member_bytes(archive, members, relative), relative)
            if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
                raise PoolError(f"{relative}: expected family record array")
            for index, value in enumerate(payload["records"]):
                if not isinstance(value, dict):
                    raise PoolError(f"{relative}#{index}: expected object")
                records.append(("family", value, relative, index))
        for relative in catalog_paths:
            value = strict_json(member_bytes(archive, members, relative), relative)
            if not isinstance(value, dict):
                raise PoolError(f"{relative}: expected object")
            records.append(("catalog", value, relative, None))

        records.sort(key=lambda item: ({"curated": 0, "family": 1, "catalog": 2}[item[0]], str(item[1].get("id"))))
        for ordinal, (kind, record, relative, index) in enumerate(records, 1):
            source_id = record.get("id")
            if source_id in seen_ids:
                raise PoolError(f"duplicate source ID: {source_id}")
            seen_ids.add(source_id)
            rows.append(occurrence(ordinal, kind=kind, record=record, record_path=relative, container_index=index))
        if set(seen_ids) != {row["id"] for row in table_rows}:
            raise PoolError("independent archive traversal differs from all.csv ID set")
        for required in ("README.md", "LICENSE-DATA", "NOTICE", "problems/schemas/README.md", "scripts/export_records.py"):
            member_bytes(archive, members, required)
        return rows, sha256(table_raw), len(members)


def build_outputs(archive_path: Path) -> dict[Path, bytes]:
    rows, table_sha, archive_file_members = build_rows(archive_path)
    kind_counts = Counter(row["kind"] for row in rows)
    status_counts = Counter(row["source_status"] for row in rows)
    if len(rows) != 14_865 or dict(kind_counts) != EXPECTED_COUNTS or dict(status_counts) != EXPECTED_STATUS_COUNTS:
        raise PoolError(f"full pool counts differ: kinds={dict(kind_counts)} statuses={dict(status_counts)}")
    pool_ids = [row["pool_id"] for row in rows]
    occurrence_raw = jsonl_bytes(rows)
    identities = [seal({
        "schema_version": "awesome-theorems/stage5-conjecture-identity-relation/1.0",
        "pool_id": row["pool_id"],
        "stable_source_key": row["stable_source_key"],
        "relation_state": "pending_independent_identity_review",
        "relation_kind": None,
        "canonical_identity_id": None,
        "related_stage5_claim_ids": [],
        "evidence_sha256": None,
        "strict_promotion_authorized": False,
    }) for row in rows]
    identity_raw = jsonl_bytes(identities)
    status_observed_upper = sum(row["source_status"] != "reported-answered-by-source" for row in rows)
    active_upper = sum(row["source_observed_active_candidate"] for row in rows)
    manifest_body = {
        "schema_version": "awesome-theorems/stage5-conjecture-pool-manifest/1.0",
        "pool_release": "conjecturebench-357bcb1a-occurrences-v1",
        "ordering_rule": "kind_order(curated,family,catalog), then source_native_id by Unicode code-point order; pool ordinal is one-based and immutable within this pinned commit",
        "stable_source_key_rule": "conjecturebench/<kind>/<source_native_id>; commit/path/container-index/record-hash identify the frozen occurrence version and never alter the logical key",
        "semantic_boundary": {
            "denominator_kind": "source_occurrence_candidate_pool",
            "not_a_stage5_catalog_release": True,
            "not_a_strict_conjecture_ledger": True,
            "not_independently_current_open_verified": True,
            "no_stage5_or_stage6_identity_allocation": True,
            "proof_target_admission": "forbidden_until_independent_statement_status_rights_importance_and_semantic_dedupe_acceptance",
        },
        "source": {
            "repository": REPOSITORY,
            "commit": COMMIT,
            "tree_sha1": TREE_SHA1,
            "archive_path": SOURCE_ARCHIVE.relative_to(ROOT).as_posix(),
            "archive_sha256": ARCHIVE_SHA256,
            "archive_size_bytes": ARCHIVE_SIZE_BYTES,
            "archive_file_members": archive_file_members,
            "all_csv_sha256": table_sha,
        },
        "base_stage5_release": {
            "release": "5.6",
            "current_path": "Docs/catalog/v5/Current_Release.json",
            "release_root_sha256": "ce490ed958240ae1cabc26c3f704ad20b4103e30ad8abfd44e9c3b722fa17877",
            "strict_conjecture_credits": 1_425,
            "immutable": True,
        },
        "counts": {
            "source_occurrences": len(rows),
            "by_kind": dict(kind_counts),
            "by_source_status": dict(status_counts),
            "source_observed_not_answered_upper_bound": status_observed_upper,
            "source_observed_active_candidate_upper_bound": active_upper,
            "independently_verified_new_strict_identities": 0,
            "strict_credits_granted": 0,
        },
        "artifacts": {
            "occurrences": {"path": OCCURRENCES.relative_to(ROOT).as_posix(), "rows": len(rows), "sha256": sha256(occurrence_raw)},
            "identity_registry": {"path": IDENTITIES.relative_to(ROOT).as_posix(), "rows": len(identities), "sha256": sha256(identity_raw)},
            "pool_id_set_sha256": sha256(canonical(sorted(pool_ids))),
            "source_record_set_sha256": sha256(canonical(sorted(row["canonical_record_sha256"] for row in rows))),
        },
        "rights": {
            "record_layer": "CC-BY-4.0",
            "code_layer": "Apache-2.0",
            "upstream_problem_content_rights_not_inherited": True,
            "notice_member": f"{TOP_LEVEL}/NOTICE",
            "worker_rule": "preserve source attribution and obey each occurrence rights_class; use a pointer where reproduction rights are unclear",
        },
    }
    manifest = seal(manifest_body)
    manifest_raw = json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    current = seal({
        "schema_version": "awesome-theorems/stage5-current-conjecture-pool/1.0",
        "pool_release": manifest["pool_release"],
        "manifest_path": MANIFEST.relative_to(CATALOG / "pools").as_posix(),
        "manifest_sha256": sha256(manifest_raw),
        "source_occurrence_denominator": 14_865,
        "base_stage5_release": "5.6",
        "base_stage5_release_immutable": True,
    })
    current_raw = json.dumps(current, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    return {OCCURRENCES: occurrence_raw, IDENTITIES: identity_raw, MANIFEST: manifest_raw, CURRENT: current_raw}


def validate_outputs(outputs: dict[Path, bytes]) -> dict[str, Any]:
    missing = [path.relative_to(ROOT).as_posix() for path in outputs if path.is_symlink() or not path.is_file()]
    if missing:
        raise PoolError(f"missing generated pool artifacts: {missing}")
    drift = [path.relative_to(ROOT).as_posix() for path, expected in outputs.items() if path.read_bytes() != expected]
    if drift:
        raise PoolError(f"generated pool artifact drift: {drift}")
    manifest = strict_json(MANIFEST.read_bytes(), "pool manifest")
    current = strict_json(CURRENT.read_bytes(), "current pool")
    for value, label in ((manifest, "pool manifest"), (current, "current pool")):
        if not isinstance(value, dict) or not isinstance(value.get("authority_sha256"), str):
            raise PoolError(f"{label}: malformed authority")
        body = dict(value); authority = body.pop("authority_sha256")
        if sha256(canonical(body)) != authority:
            raise PoolError(f"{label}: authority mismatch")
    if current.get("manifest_sha256") != file_sha256(MANIFEST):
        raise PoolError("current pool manifest binding differs")
    return {
        "valid": True,
        "source_occurrences": manifest["counts"]["source_occurrences"],
        "source_observed_not_answered_upper_bound": manifest["counts"]["source_observed_not_answered_upper_bound"],
        "source_observed_active_candidate_upper_bound": manifest["counts"]["source_observed_active_candidate_upper_bound"],
        "strict_credits_granted": manifest["counts"]["strict_credits_granted"],
        "manifest_sha256": file_sha256(MANIFEST),
        "occurrences_sha256": file_sha256(OCCURRENCES),
        "identity_registry_sha256": file_sha256(IDENTITIES),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-archive", type=Path, default=SOURCE_ARCHIVE)
    parser.add_argument("--freeze-source", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        source = args.source_archive.resolve()
        if args.freeze_source:
            if source == SOURCE_ARCHIVE.resolve():
                raise PoolError("--freeze-source needs a distinct reviewed input archive")
            if source.is_symlink() or not source.is_file() or source.stat().st_size != ARCHIVE_SIZE_BYTES or file_sha256(source) != ARCHIVE_SHA256:
                raise PoolError("reviewed input archive size/SHA-256 differs")
            SOURCE_ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
            with source.open("rb") as input_stream, tempfile.NamedTemporaryFile(prefix=f".{SOURCE_ARCHIVE.name}.", dir=SOURCE_ARCHIVE.parent, delete=False) as output_stream:
                temporary = Path(output_stream.name)
                shutil.copyfileobj(input_stream, output_stream)
            temporary.chmod(0o644)
            temporary.replace(SOURCE_ARCHIVE)
            source = SOURCE_ARCHIVE
        outputs = build_outputs(source)
        if args.write:
            for path, raw in outputs.items():
                atomic_write(path, raw)
        if args.check or args.write:
            print(json.dumps(validate_outputs(outputs), ensure_ascii=False, sort_keys=True))
        else:
            print(json.dumps({"valid": True, "would_write": [path.relative_to(ROOT).as_posix() for path in outputs]}, sort_keys=True))
        return 0
    except (OSError, PoolError, tarfile.TarError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
