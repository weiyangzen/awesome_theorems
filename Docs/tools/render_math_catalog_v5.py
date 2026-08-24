#!/usr/bin/env python3
"""Render the user-readable Stage5 mathematics projections.

The immutable release directory contains JSON authorities only.  This tool
joins the ``Theorem_List.json`` and ``Open_Claim_List.json`` member projections
to ``Claim_Catalog.json`` and streams deterministic Markdown to the sibling
``Docs/catalog/v5/readable/<release>/`` directory.  Release 5.2 also joins its
credit authority to generate ``Strict_Conjecture_List.md``; that list is the
effective strict-credit set, not a spelling-based projection of open claims.

Only Python's standard library is used.  ``--check`` performs no writes: it
validates the release root and compares the expected Markdown byte-for-byte
with every readable projection already on disk.
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable, Iterator, Mapping
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
V5_DIR = ROOT / "Docs" / "catalog" / "v5"
RELEASES_DIR = V5_DIR / "releases"
READABLE_DIR = V5_DIR / "readable"

MANIFEST_NAME = "Release_Manifest.json"
CATALOG_NAME = "Claim_Catalog.json"
THEOREM_JSON_NAME = "Theorem_List.json"
OPEN_JSON_NAME = "Open_Claim_List.json"
STRICT_JSON_NAME = "Strict_Conjecture_Ledger.json"
COVERAGE_JSON_NAME = "Coverage_Ledger.json"
THEOREM_MD_NAME = "Theorem_List.md"
OPEN_MD_NAME = "Open_Claim_List.md"
STRICT_MD_NAME = "Strict_Conjecture_List.md"

OFFICIAL_NON_MANIFEST_FILES = frozenset(
    {
        CATALOG_NAME,
        "Claim_ID_Registry.json",
        "Stage5_Claim_ID_Registry.json",
        "Migration_v4_to_v5.json",
        THEOREM_JSON_NAME,
        OPEN_JSON_NAME,
        "Coverage_Ledger.json",
    }
)
OFFICIAL_RELEASE_FILES = OFFICIAL_NON_MANIFEST_FILES | {MANIFEST_NAME}

OFFICIAL_NON_MANIFEST_FILES_V5_2 = OFFICIAL_NON_MANIFEST_FILES | {STRICT_JSON_NAME}
OFFICIAL_RELEASE_FILES_V5_2 = OFFICIAL_NON_MANIFEST_FILES_V5_2 | {MANIFEST_NAME}

RECORD_SCHEMA = "awesome-theorems/stage5-math-claim-record/5.0"
S5_ID_RE = re.compile(r"^S5-CLM-([0-9]{8})$")
ATV_ID_RE = re.compile(r"^ATV-([0-9]{8})$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
SOURCE_ID_RE = re.compile(r"^SRC-MATH-V5-[A-Z0-9][A-Z0-9._-]*$")

SCHEMA_THEOREM_KINDS = frozenset({"theorem", "lemma", "corollary", "proposition"})
SCHEMA_OPEN_KINDS = frozenset({"conjecture", "hypothesis", "open_problem"})
SCHEMA_OPEN_STATUSES = frozenset({"open", "partial", "independent", "disputed"})


class RenderError(RuntimeError):
    """The release or one of its readable projections is invalid."""


def _canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise RenderError(f"value is not canonical-JSON serializable: {exc}") from exc


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _sha256_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def _reject_constant(value: str) -> None:
    raise RenderError(f"non-finite JSON number is forbidden: {value}")


def _object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise RenderError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _strict_json_bytes(payload: bytes, label: str) -> dict[str, Any]:
    try:
        text = payload.decode("utf-8")
        value = json.loads(
            text,
            object_pairs_hook=_object_without_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise RenderError(f"invalid JSON in {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise RenderError(f"{label} must contain one JSON object")
    return value


def _require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RenderError(f"{label} must be an object")
    return value


def _require_rows(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise RenderError(f"{label} must be an array of objects")
    return value


def _require_string(
    value: Any,
    label: str,
    pattern: re.Pattern[str] | None = None,
    *,
    allow_empty: bool = False,
) -> str:
    if not isinstance(value, str) or (not value and not allow_empty):
        qualifier = "a string" if allow_empty else "a non-empty string"
        raise RenderError(f"{label} must be {qualifier}")
    if pattern is not None and pattern.fullmatch(value) is None:
        raise RenderError(f"{label} has invalid syntax: {value!r}")
    return value


def _require_nonnegative_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise RenderError(f"{label} must be a non-negative integer")
    return value


def _require_string_array(
    value: Any,
    label: str,
    *,
    pattern: re.Pattern[str] | None = None,
    nonempty: bool = False,
) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise RenderError(f"{label} must be an array of strings")
    if nonempty and not value:
        raise RenderError(f"{label} must not be empty")
    if len(value) != len(set(value)):
        raise RenderError(f"{label} must not contain duplicates")
    if pattern is not None:
        for index, item in enumerate(value):
            _require_string(item, f"{label}[{index}]", pattern)
    return value


def _validate_counts_tree(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str) or not key:
                raise RenderError(f"{label} has an invalid metric name")
            _validate_counts_tree(child, f"{label}.{key}")
        return
    _require_nonnegative_int(value, label)


def _safe_release_file(release_root: Path, relative: str) -> Path:
    pure = Path(relative)
    if pure.is_absolute() or len(pure.parts) != 1 or pure.name != relative:
        raise RenderError(f"unsafe release artifact path: {relative!r}")
    resolved_root = release_root.resolve()
    resolved = (resolved_root / pure).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise RenderError(f"release artifact escapes its root: {relative!r}") from exc
    if not resolved.is_file():
        raise RenderError(f"release artifact is missing: {relative}")
    return resolved


def _artifact_root_payload(artifacts: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    bindings = [
        {
            "path": artifact["path"],
            "sha256": artifact["sha256"],
            "size_bytes": artifact["size_bytes"],
        }
        for artifact in artifacts
    ]
    return sorted(bindings, key=lambda row: row["path"])


class ReleaseBundle:
    """Validated JSON authorities needed by the renderer."""

    def __init__(
        self,
        *,
        release: str,
        release_root: Path,
        manifest_bytes: bytes,
        manifest: dict[str, Any],
        artifact_bindings: dict[str, dict[str, Any]],
        catalog: dict[str, Any],
        theorem: dict[str, Any],
        open_claim: dict[str, Any],
        strict_conjecture: dict[str, Any] | None,
        catalog_index: dict[str, dict[str, Any]],
    ) -> None:
        self.release = release
        self.release_root = release_root
        self.manifest_bytes = manifest_bytes
        self.manifest = manifest
        self.artifact_bindings = artifact_bindings
        self.catalog = catalog
        self.theorem = theorem
        self.open_claim = open_claim
        self.strict_conjecture = strict_conjecture
        self.catalog_index = catalog_index


def _validate_manifest_v5_2(
    release_root: Path,
    manifest: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Validate the wider 5.2 manifest without weakening the 5.0/5.1 path."""

    expected_fields = {
        "schema_version",
        "release",
        "parent_release",
        "parent_release_root_sha256",
        "release_root_sha256",
        "authoritative_inputs",
        "accepted_set_digests",
        "strict_credit_binding",
        "artifacts",
        "counts",
        "authority_sha256",
    }
    if set(manifest) != expected_fields:
        missing = sorted(expected_fields - set(manifest))
        extra = sorted(set(manifest) - expected_fields)
        raise RenderError(
            f"5.2 manifest field set mismatch: missing={missing}, extra={extra}"
        )
    if manifest.get("schema_version") != "awesome-theorems/stage5-release-manifest/5.2":
        raise RenderError("5.2 manifest has the wrong schema_version")
    if manifest.get("release") != "5.2" or manifest.get("parent_release") != "5.1":
        raise RenderError("5.2 manifest release/parent_release binding is invalid")
    parent_root = _require_string(
        manifest.get("parent_release_root_sha256"),
        "manifest.parent_release_root_sha256",
        SHA256_RE,
    )
    declared_root = _require_string(
        manifest.get("release_root_sha256"),
        "manifest.release_root_sha256",
        SHA256_RE,
    )
    _require_object(manifest.get("authoritative_inputs"), "manifest.authoritative_inputs")
    accepted_digests = _require_object(
        manifest.get("accepted_set_digests"), "manifest.accepted_set_digests"
    )
    for key in ("content_hash_set_sha256", "semantic_key_set_sha256", "s5_id_set_sha256"):
        _require_string(
            accepted_digests.get(key), f"manifest.accepted_set_digests.{key}", SHA256_RE
        )
    if set(accepted_digests) != {
        "content_hash_set_sha256",
        "semantic_key_set_sha256",
        "s5_id_set_sha256",
    }:
        raise RenderError("5.2 manifest accepted_set_digests field set is invalid")

    strict_binding = _require_object(
        manifest.get("strict_credit_binding"), "manifest.strict_credit_binding"
    )
    if set(strict_binding) != {
        "path",
        "file_sha256",
        "authority_sha256",
        "effective_s5_id_set_sha256",
        "effective_variant_id_set_sha256",
    } or strict_binding.get("path") != STRICT_JSON_NAME:
        raise RenderError("5.2 manifest strict_credit_binding is invalid")
    for key in (
        "file_sha256",
        "authority_sha256",
        "effective_s5_id_set_sha256",
        "effective_variant_id_set_sha256",
    ):
        _require_string(strict_binding.get(key), f"manifest.strict_credit_binding.{key}", SHA256_RE)

    counts = _require_object(manifest.get("counts"), "manifest.counts")
    expected_count_keys = {
        "non_manifest_artifacts",
        "catalog_records",
        "origin_theorems",
        "origin_open_claims",
        "cumulative_theorems",
        "cumulative_open_claims",
        "effective_strict_conjecture_credits",
    }
    if set(counts) != expected_count_keys:
        raise RenderError("5.2 manifest count field set is invalid")
    for key in sorted(expected_count_keys):
        _require_nonnegative_int(counts.get(key), f"manifest.counts.{key}")

    authority = _require_string(
        manifest.get("authority_sha256"), "manifest.authority_sha256", SHA256_RE
    )
    observed_authority = _sha256_bytes(
        _canonical_json_bytes(
            {key: value for key, value in manifest.items() if key != "authority_sha256"}
        )
    )
    if authority != observed_authority:
        raise RenderError(
            f"5.2 manifest authority mismatch: declared={authority}, "
            f"observed={observed_authority}"
        )

    artifacts = _require_rows(manifest.get("artifacts"), "manifest.artifacts")
    if len(artifacts) != len(OFFICIAL_NON_MANIFEST_FILES_V5_2):
        raise RenderError("5.2 manifest must bind exactly eight non-manifest artifacts")
    bindings: dict[str, dict[str, Any]] = {}
    for index, artifact in enumerate(artifacts):
        if set(artifact) != {"path", "sha256", "size_bytes", "row_count"}:
            raise RenderError(f"manifest.artifacts[{index}] field set is invalid")
        path = _require_string(artifact.get("path"), f"manifest.artifacts[{index}].path")
        if path in bindings:
            raise RenderError(f"manifest.artifacts duplicates path={path!r}")
        digest = _require_string(
            artifact.get("sha256"), f"manifest.artifacts[{index}].sha256", SHA256_RE
        )
        size = _require_nonnegative_int(
            artifact.get("size_bytes"), f"manifest.artifacts[{index}].size_bytes"
        )
        row_count = _require_nonnegative_int(
            artifact.get("row_count"), f"manifest.artifacts[{index}].row_count"
        )
        bindings[path] = {
            "path": path,
            "sha256": digest,
            "size_bytes": size,
            "row_count": row_count,
        }
    if set(bindings) != OFFICIAL_NON_MANIFEST_FILES_V5_2:
        missing = sorted(OFFICIAL_NON_MANIFEST_FILES_V5_2 - set(bindings))
        extra = sorted(set(bindings) - OFFICIAL_NON_MANIFEST_FILES_V5_2)
        raise RenderError(
            f"5.2 manifest artifact set mismatch: missing={missing}, extra={extra}"
        )

    actual_entries = {path.name: path for path in release_root.iterdir()}
    if set(actual_entries) != OFFICIAL_RELEASE_FILES_V5_2 or not all(
        path.is_file() and not path.is_symlink() for path in actual_entries.values()
    ):
        missing = sorted(OFFICIAL_RELEASE_FILES_V5_2 - set(actual_entries))
        extra = sorted(set(actual_entries) - OFFICIAL_RELEASE_FILES_V5_2)
        raise RenderError(
            "immutable 5.2 release directory must contain exactly nine files: "
            f"missing={missing}, extra={extra}"
        )
    for path, binding in bindings.items():
        actual_digest, actual_size = _sha256_file(_safe_release_file(release_root, path))
        if actual_digest != binding["sha256"] or actual_size != binding["size_bytes"]:
            raise RenderError(
                f"5.2 artifact binding mismatch for {path}: "
                f"expected sha256={binding['sha256']} bytes={binding['size_bytes']}, "
                f"observed sha256={actual_digest} bytes={actual_size}"
            )
    computed_root = _sha256_bytes(_canonical_json_bytes(_artifact_root_payload(artifacts)))
    if computed_root != declared_root:
        raise RenderError(
            f"5.2 release root mismatch: declared={declared_root}, computed={computed_root}"
        )
    if counts["non_manifest_artifacts"] != len(artifacts):
        raise RenderError("5.2 manifest non_manifest_artifacts count is stale")

    parent_dir = RELEASES_DIR / "5.1"
    parent_manifest_path = parent_dir / MANIFEST_NAME
    if not parent_manifest_path.is_file():
        raise RenderError("release 5.2 cannot resolve its immutable 5.1 parent manifest")
    parent_manifest = _strict_json_bytes(
        parent_manifest_path.read_bytes(), "5.1/Release_Manifest.json"
    )
    _validate_manifest("5.1", parent_dir, parent_manifest)
    if parent_root != parent_manifest["release_root_sha256"]:
        raise RenderError("release 5.2 parent root does not match recomputed release 5.1")
    return bindings


def _validate_manifest_v5_3(
    release_root: Path,
    manifest: dict[str, Any],
    *,
    release: str = "5.3",
    parent_release: str = "5.2",
) -> dict[str, dict[str, Any]]:
    """Validate a mathlib-expansion manifest and its immutable parent."""

    expected_fields = {
        "schema_version",
        "release",
        "parent_release",
        "parent_release_root_sha256",
        "release_root_sha256",
        "authoritative_inputs",
        "accepted_set_digests",
        "strict_credit_binding",
        "artifacts",
        "counts",
        "authority_sha256",
    }
    if set(manifest) != expected_fields:
        missing = sorted(expected_fields - set(manifest))
        extra = sorted(set(manifest) - expected_fields)
        raise RenderError(
            f"{release} manifest field set mismatch: missing={missing}, extra={extra}"
        )
    if manifest.get("schema_version") != f"awesome-theorems/stage5-release-manifest/{release}":
        raise RenderError(f"{release} manifest has the wrong schema_version")
    if manifest.get("release") != release or manifest.get("parent_release") != parent_release:
        raise RenderError(f"{release} manifest release/parent_release binding is invalid")
    parent_root = _require_string(
        manifest.get("parent_release_root_sha256"),
        "manifest.parent_release_root_sha256",
        SHA256_RE,
    )
    declared_root = _require_string(
        manifest.get("release_root_sha256"),
        "manifest.release_root_sha256",
        SHA256_RE,
    )
    _require_object(manifest.get("authoritative_inputs"), "manifest.authoritative_inputs")
    accepted_digests = _require_object(
        manifest.get("accepted_set_digests"), "manifest.accepted_set_digests"
    )
    expected_digest_keys = {
        "source_record_id_set_sha256",
        "declaration_set_sha256",
        "formal_type_sha256_set_sha256",
        "semantic_key_set_sha256",
        "variant_id_set_sha256",
        "s5_id_set_sha256",
    }
    if set(accepted_digests) != expected_digest_keys:
        raise RenderError(f"{release} manifest accepted_set_digests field set is invalid")
    for key in sorted(expected_digest_keys):
        _require_string(
            accepted_digests.get(key), f"manifest.accepted_set_digests.{key}", SHA256_RE
        )

    strict_binding = _require_object(
        manifest.get("strict_credit_binding"), "manifest.strict_credit_binding"
    )
    if set(strict_binding) != {
        "path",
        "file_sha256",
        "authority_sha256",
        "effective_s5_id_set_sha256",
        "effective_variant_id_set_sha256",
    } or strict_binding.get("path") != STRICT_JSON_NAME:
        raise RenderError(f"{release} manifest strict_credit_binding is invalid")
    for key in (
        "file_sha256",
        "authority_sha256",
        "effective_s5_id_set_sha256",
        "effective_variant_id_set_sha256",
    ):
        _require_string(
            strict_binding.get(key), f"manifest.strict_credit_binding.{key}", SHA256_RE
        )

    counts = _require_object(manifest.get("counts"), "manifest.counts")
    expected_count_keys = {
        "non_manifest_artifacts",
        "catalog_records",
        "origin_theorems",
        "origin_open_claims",
        "cumulative_theorems",
        "cumulative_open_claims",
        "effective_strict_conjecture_credits",
    }
    if set(counts) != expected_count_keys:
        raise RenderError(f"{release} manifest count field set is invalid")
    for key in sorted(expected_count_keys):
        _require_nonnegative_int(counts.get(key), f"manifest.counts.{key}")

    authority = _require_string(
        manifest.get("authority_sha256"), "manifest.authority_sha256", SHA256_RE
    )
    observed_authority = _sha256_bytes(
        _canonical_json_bytes(
            {key: value for key, value in manifest.items() if key != "authority_sha256"}
        )
    )
    if authority != observed_authority:
        raise RenderError(
            f"{release} manifest authority mismatch: declared={authority}, "
            f"observed={observed_authority}"
        )

    artifacts = _require_rows(manifest.get("artifacts"), "manifest.artifacts")
    if len(artifacts) != len(OFFICIAL_NON_MANIFEST_FILES_V5_2):
        raise RenderError(f"{release} manifest must bind exactly eight non-manifest artifacts")
    bindings: dict[str, dict[str, Any]] = {}
    for index, artifact in enumerate(artifacts):
        if set(artifact) != {"path", "sha256", "size_bytes", "row_count"}:
            raise RenderError(f"manifest.artifacts[{index}] field set is invalid")
        path = _require_string(artifact.get("path"), f"manifest.artifacts[{index}].path")
        if path in bindings:
            raise RenderError(f"manifest.artifacts duplicates path={path!r}")
        digest = _require_string(
            artifact.get("sha256"), f"manifest.artifacts[{index}].sha256", SHA256_RE
        )
        size = _require_nonnegative_int(
            artifact.get("size_bytes"), f"manifest.artifacts[{index}].size_bytes"
        )
        row_count = _require_nonnegative_int(
            artifact.get("row_count"), f"manifest.artifacts[{index}].row_count"
        )
        bindings[path] = {
            "path": path,
            "sha256": digest,
            "size_bytes": size,
            "row_count": row_count,
        }
    if set(bindings) != OFFICIAL_NON_MANIFEST_FILES_V5_2:
        missing = sorted(OFFICIAL_NON_MANIFEST_FILES_V5_2 - set(bindings))
        extra = sorted(set(bindings) - OFFICIAL_NON_MANIFEST_FILES_V5_2)
        raise RenderError(
            f"{release} manifest artifact set mismatch: missing={missing}, extra={extra}"
        )

    actual_entries = {path.name: path for path in release_root.iterdir()}
    if set(actual_entries) != OFFICIAL_RELEASE_FILES_V5_2 or not all(
        path.is_file() and not path.is_symlink() for path in actual_entries.values()
    ):
        missing = sorted(OFFICIAL_RELEASE_FILES_V5_2 - set(actual_entries))
        extra = sorted(set(actual_entries) - OFFICIAL_RELEASE_FILES_V5_2)
        raise RenderError(
            f"immutable {release} release directory must contain exactly nine files: "
            f"missing={missing}, extra={extra}"
        )
    for path, binding in bindings.items():
        actual_digest, actual_size = _sha256_file(_safe_release_file(release_root, path))
        if actual_digest != binding["sha256"] or actual_size != binding["size_bytes"]:
            raise RenderError(
                f"{release} artifact binding mismatch for {path}: "
                f"expected sha256={binding['sha256']} bytes={binding['size_bytes']}, "
                f"observed sha256={actual_digest} bytes={actual_size}"
            )
    computed_root = _sha256_bytes(_canonical_json_bytes(_artifact_root_payload(artifacts)))
    if computed_root != declared_root:
        raise RenderError(
            f"{release} release root mismatch: declared={declared_root}, computed={computed_root}"
        )
    if counts["non_manifest_artifacts"] != len(artifacts):
        raise RenderError(f"{release} manifest non_manifest_artifacts count is stale")

    parent_dir = RELEASES_DIR / parent_release
    parent_manifest_path = parent_dir / MANIFEST_NAME
    if not parent_manifest_path.is_file():
        raise RenderError(
            f"release {release} cannot resolve its immutable {parent_release} parent manifest"
        )
    parent_manifest = _strict_json_bytes(
        parent_manifest_path.read_bytes(), f"{parent_release}/Release_Manifest.json"
    )
    _validate_manifest(parent_release, parent_dir, parent_manifest)
    if parent_root != parent_manifest["release_root_sha256"]:
        raise RenderError(
            f"release {release} parent root does not match recomputed release {parent_release}"
        )
    return bindings


def _validate_manifest_v5_4(
    release_root: Path,
    manifest: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Validate the 5.4 mathlib-expansion manifest and its 5.3 parent."""

    return _validate_manifest_v5_3(
        release_root,
        manifest,
        release="5.4",
        parent_release="5.3",
    )


def _validate_manifest(
    release: str,
    release_root: Path,
    manifest: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    if release == "5.4":
        return _validate_manifest_v5_4(release_root, manifest)
    if release == "5.3":
        return _validate_manifest_v5_3(release_root, manifest)
    if release == "5.2":
        return _validate_manifest_v5_2(release_root, manifest)
    expected_fields = {
        "schema_version",
        "release",
        "parent_release",
        "parent_release_root_sha256",
        "release_root_sha256",
        "artifacts",
        "counts",
        "authority_sha256",
    }
    if set(manifest) != expected_fields:
        missing = sorted(expected_fields - set(manifest))
        extra = sorted(set(manifest) - expected_fields)
        raise RenderError(f"manifest field set mismatch: missing={missing}, extra={extra}")
    _require_string(manifest.get("schema_version"), "manifest.schema_version")
    declared_release = _require_string(manifest.get("release"), "manifest.release")
    if declared_release != release:
        raise RenderError(
            f"manifest release {declared_release!r} does not match --release {release!r}"
        )

    declared_root = _require_string(
        manifest.get("release_root_sha256"),
        "manifest.release_root_sha256",
        SHA256_RE,
    )
    counts = _require_object(manifest.get("counts"), "manifest.counts")
    _validate_counts_tree(counts, "manifest.counts")
    if release == "5.0":
        if manifest.get("parent_release") is not None:
            raise RenderError("release 5.0 manifest.parent_release must be null")
        if manifest.get("parent_release_root_sha256") is not None:
            raise RenderError("release 5.0 manifest.parent_release_root_sha256 must be null")
    else:
        if manifest.get("parent_release") != "5.0":
            raise RenderError("release 5.1 manifest.parent_release must be 5.0")
        _require_string(
            manifest.get("parent_release_root_sha256"),
            "manifest.parent_release_root_sha256",
            SHA256_RE,
        )
    authority = _require_string(
        manifest.get("authority_sha256"), "manifest.authority_sha256", SHA256_RE
    )
    authority_body = {key: value for key, value in manifest.items() if key != "authority_sha256"}
    observed_authority = _sha256_bytes(_canonical_json_bytes(authority_body))
    if authority != observed_authority:
        raise RenderError(
            f"manifest authority mismatch: declared={authority}, observed={observed_authority}"
        )

    artifacts = _require_rows(manifest.get("artifacts"), "manifest.artifacts")
    if len(artifacts) != len(OFFICIAL_NON_MANIFEST_FILES):
        raise RenderError(
            "manifest.artifacts must bind exactly the seven non-manifest release files"
        )

    bindings: dict[str, dict[str, Any]] = {}
    for index, artifact in enumerate(artifacts):
        path = _require_string(artifact.get("path"), f"manifest.artifacts[{index}].path")
        if path in bindings:
            raise RenderError(f"manifest.artifacts duplicates path={path!r}")
        digest = _require_string(
            artifact.get("sha256"),
            f"manifest.artifacts[{index}].sha256",
            SHA256_RE,
        )
        size = _require_nonnegative_int(
            artifact.get("size_bytes"), f"manifest.artifacts[{index}].size_bytes"
        )
        _require_nonnegative_int(
            artifact.get("row_count"), f"manifest.artifacts[{index}].row_count"
        )
        bindings[path] = dict(artifact)
        bindings[path]["sha256"] = digest
        bindings[path]["size_bytes"] = size

    if set(bindings) != OFFICIAL_NON_MANIFEST_FILES:
        missing = sorted(OFFICIAL_NON_MANIFEST_FILES - set(bindings))
        extra = sorted(set(bindings) - OFFICIAL_NON_MANIFEST_FILES)
        raise RenderError(f"manifest artifact set mismatch: missing={missing}, extra={extra}")

    actual_entries = {path.name: path for path in release_root.iterdir()}
    if set(actual_entries) != OFFICIAL_RELEASE_FILES or not all(
        path.is_file() and not path.is_symlink() for path in actual_entries.values()
    ):
        missing = sorted(OFFICIAL_RELEASE_FILES - set(actual_entries))
        extra = sorted(set(actual_entries) - OFFICIAL_RELEASE_FILES)
        raise RenderError(
            f"immutable release directory must contain exactly eight files: "
            f"missing={missing}, extra={extra}"
        )

    for path, binding in bindings.items():
        actual_path = _safe_release_file(release_root, path)
        actual_digest, actual_size = _sha256_file(actual_path)
        if actual_digest != binding["sha256"] or actual_size != binding["size_bytes"]:
            raise RenderError(
                f"release artifact binding mismatch for {path}: "
                f"expected sha256={binding['sha256']} bytes={binding['size_bytes']}, "
                f"observed sha256={actual_digest} bytes={actual_size}"
            )

    computed_root = _sha256_bytes(_canonical_json_bytes(_artifact_root_payload(artifacts)))
    if computed_root != declared_root:
        raise RenderError(
            f"release root mismatch: declared={declared_root}, computed={computed_root}"
        )
    if release == "5.1":
        parent_root = RELEASES_DIR / "5.0"
        parent_manifest_path = parent_root / MANIFEST_NAME
        if not parent_manifest_path.is_file():
            raise RenderError("release 5.1 cannot resolve its immutable 5.0 parent manifest")
        parent_manifest = _strict_json_bytes(
            parent_manifest_path.read_bytes(), "5.0/Release_Manifest.json"
        )
        _validate_manifest("5.0", parent_root, parent_manifest)
        if manifest["parent_release_root_sha256"] != parent_manifest["release_root_sha256"]:
            raise RenderError("release 5.1 parent root does not match recomputed release 5.0")
    return bindings


def _validate_source_locator(value: Any, label: str) -> dict[str, Any]:
    locator = _require_object(value, label)
    _require_string(locator.get("source_id"), f"{label}.source_id", SOURCE_ID_RE)
    _require_string(locator.get("revision"), f"{label}.revision")
    _require_string(locator.get("member_path"), f"{label}.member_path")
    for key in ("file_sha256", "raw_block_sha256"):
        _require_string(locator.get(key), f"{label}.{key}", SHA256_RE)
    byte_start = _require_nonnegative_int(locator.get("byte_start"), f"{label}.byte_start")
    byte_end = _require_nonnegative_int(
        locator.get("byte_end_exclusive"), f"{label}.byte_end_exclusive"
    )
    line_start = _require_nonnegative_int(locator.get("line_start"), f"{label}.line_start")
    line_end = _require_nonnegative_int(locator.get("line_end"), f"{label}.line_end")
    if byte_end <= byte_start:
        raise RenderError(f"{label} byte range is empty or reversed")
    if line_start < 1 or line_end < line_start:
        raise RenderError(f"{label} line range is invalid")
    return locator


def _validate_formal_statement(value: Any, label: str) -> dict[str, Any]:
    formal = _require_object(value, label)
    if formal.get("language") != "Lean4":
        raise RenderError(f"{label}.language must be Lean4")
    for key in (
        "module",
        "declaration_name",
        "qualified_declaration",
        "declaration_kind",
        "declaration_text",
        "declaration_type",
        "docstring",
        "elaboration_status",
    ):
        _require_string(formal.get(key), f"{label}.{key}")
    _require_string(formal.get("namespace"), f"{label}.namespace", allow_empty=True)
    for text_key, digest_key in (
        ("declaration_text", "declaration_sha256"),
        ("declaration_type", "declaration_type_sha256"),
        ("docstring", "docstring_sha256"),
    ):
        declared = _require_string(formal.get(digest_key), f"{label}.{digest_key}", SHA256_RE)
        observed = _sha256_text(formal[text_key])
        if observed != declared:
            raise RenderError(
                f"{label}.{digest_key} does not match UTF-8 {text_key}: "
                f"declared={declared}, observed={observed}"
            )
    sorry_free = formal.get("sorry_free")
    if not (
        isinstance(sorry_free, bool) or sorry_free == "unknown" or sorry_free is None
    ):
        raise RenderError(f"{label}.sorry_free has an invalid value")
    _require_string_array(formal.get("axioms"), f"{label}.axioms")
    _validate_source_locator(formal.get("locator"), f"{label}.locator")
    return formal


def _validate_status_detail(value: Any, label: str) -> dict[str, Any]:
    detail = _require_object(value, label)
    _require_string(detail.get("status_as_of"), f"{label}.status_as_of", DATE_RE)
    _require_string(detail.get("basis"), f"{label}.basis")
    _require_string(detail.get("evidence_level"), f"{label}.evidence_level")
    _require_string_array(
        detail.get("source_refs"),
        f"{label}.source_refs",
        pattern=SOURCE_ID_RE,
        nonempty=True,
    )
    return detail


def _validate_provenance(value: Any, label: str) -> dict[str, Any]:
    provenance = _require_object(value, label)
    _require_string(
        provenance.get("formal_source_ref"), f"{label}.formal_source_ref", SOURCE_ID_RE
    )
    _require_string_array(
        provenance.get("source_refs"),
        f"{label}.source_refs",
        pattern=SOURCE_ID_RE,
        nonempty=True,
    )
    _require_string(provenance.get("extraction_mode"), f"{label}.extraction_mode")
    _require_string(provenance.get("extractor_version"), f"{label}.extractor_version")
    _require_string(
        provenance.get("extraction_receipt_sha256"),
        f"{label}.extraction_receipt_sha256",
        SHA256_RE,
    )
    if provenance.get("source_assertion_not_independent_truth_review") is not True:
        raise RenderError(
            f"{label}.source_assertion_not_independent_truth_review must be true"
        )
    return provenance


def _validate_statement_aliases(row: Mapping[str, Any], label: str) -> None:
    statement = _require_object(row.get("statement"), f"{label}.statement")
    nested = _require_object(
        row.get("mathematical_statement"), f"{label}.mathematical_statement"
    )
    nested_digest = _require_string(
        nested.get("statement_sha256"),
        f"{label}.mathematical_statement.statement_sha256",
        SHA256_RE,
    )
    flat_digest = _require_string(
        row.get("statement_sha256"), f"{label}.statement_sha256", SHA256_RE
    )
    nested_without_digest = {
        key: value for key, value in nested.items() if key != "statement_sha256"
    }
    if nested_without_digest != statement:
        raise RenderError(
            f"{label}.statement does not value-match mathematical_statement minus its self hash"
        )
    observed = _sha256_bytes(_canonical_json_bytes(statement))
    if not (observed == flat_digest == nested_digest):
        raise RenderError(
            f"{label} statement hashes differ: observed={observed}, "
            f"flat={flat_digest}, nested={nested_digest}"
        )
    if statement.get("formal_type") != row.get("formal_type"):
        raise RenderError(f"{label}.statement.formal_type does not match formal_type")


def _validate_rights(value: Any, label: str) -> dict[str, Any]:
    rights = _require_object(value, label)
    for key in ("formal_code_terms", "docstring_terms", "status"):
        _require_string(rights.get(key), f"{label}.{key}")
    if rights.get("redistribution_mode") != "source_terms_preserved_in_repository_inventory":
        raise RenderError(
            f"{label}.redistribution_mode does not permit readable declaration/docstring output"
        )
    _require_string_array(rights.get("attribution"), f"{label}.attribution")
    _require_string_array(
        rights.get("source_refs"),
        f"{label}.source_refs",
        pattern=SOURCE_ID_RE,
        nonempty=True,
    )
    if not isinstance(rights.get("not_independently_cleared"), bool):
        raise RenderError(f"{label}.not_independently_cleared must be a boolean")
    return rights


def _validate_catalog_record(row: dict[str, Any], index: int) -> str:
    label = f"catalog.records[{index}]"
    if row.get("schema_version") != RECORD_SCHEMA:
        raise RenderError(f"{label}.schema_version must be {RECORD_SCHEMA!r}")
    stage_id = _require_string(row.get("stage_claim_id"), f"{label}.stage_claim_id", S5_ID_RE)
    variant_id = _require_string(row.get("variant_id"), f"{label}.variant_id", ATV_ID_RE)
    if S5_ID_RE.fullmatch(stage_id).group(1) != ATV_ID_RE.fullmatch(variant_id).group(1):
        raise RenderError(f"{label} S5 and ATV ordinals differ")

    if row.get("origin_stage") != "Stage5":
        raise RenderError(f"{label}.origin_stage must be Stage5")
    if row.get("origin_release") not in {"5.0", "5.1"}:
        raise RenderError(f"{label}.origin_release is invalid")
    if row.get("release_id") not in {"5.0", "5.1"}:
        raise RenderError(f"{label}.release_id is invalid")

    _require_string(row.get("display_name"), f"{label}.display_name")
    if row.get("owner_domain") != "mathematics":
        raise RenderError(f"{label}.owner_domain must be mathematics")
    if row.get("record_role") != "claim" or row.get("atomicity") != "atomic":
        raise RenderError(f"{label} must be one atomic claim")
    if row.get("truth_apt") is not True:
        raise RenderError(f"{label}.truth_apt must be true")

    category = _require_string(row.get("category"), f"{label}.category")
    kind = _require_string(row.get("current_claim_kind"), f"{label}.current_claim_kind")
    formal = _validate_formal_statement(row.get("formal_statement"), f"{label}.formal_statement")
    locator = _validate_source_locator(row.get("locator"), f"{label}.locator")
    material_status = _require_string(row.get("material_status"), f"{label}.material_status")
    _validate_status_detail(row.get("status_detail"), f"{label}.status_detail")
    provenance = _validate_provenance(row.get("provenance"), f"{label}.provenance")

    source_id = _require_string(row.get("source_id"), f"{label}.source_id", SOURCE_ID_RE)
    if not (
        source_id
        == locator["source_id"]
        == formal["locator"]["source_id"]
        == provenance["formal_source_ref"]
    ):
        raise RenderError(f"{label} flat, nested, and provenance source IDs differ")
    if locator != formal["locator"]:
        raise RenderError(f"{label}.locator does not byte-match formal_statement.locator")

    flat_to_nested = {
        "qualified_name": "qualified_declaration",
        "module": "module",
        "namespace": "namespace",
        "declaration_kind": "declaration_kind",
        "formal_declaration": "declaration_text",
        "formal_declaration_sha256": "declaration_sha256",
        "formal_type": "declaration_type",
        "formal_type_sha256": "declaration_type_sha256",
        "formal_docstring": "docstring",
        "formal_docstring_sha256": "docstring_sha256",
    }
    for flat_key, nested_key in flat_to_nested.items():
        flat_value = row.get(flat_key)
        if flat_key.endswith("_sha256"):
            _require_string(flat_value, f"{label}.{flat_key}", SHA256_RE)
        else:
            _require_string(
                flat_value,
                f"{label}.{flat_key}",
                allow_empty=flat_key == "namespace",
            )
        if flat_value != formal[nested_key]:
            raise RenderError(
                f"{label}.{flat_key} does not byte-match formal_statement.{nested_key}"
            )

    proof_state = _require_string(row.get("formal_proof_state"), f"{label}.formal_proof_state")
    nested_proof_state = {
        "source_asserted_not_replayed": "source_repository_statement"
    }.get(proof_state, proof_state)
    if formal["elaboration_status"] != nested_proof_state:
        raise RenderError(f"{label} flat and nested formal proof states differ")
    _require_string(row.get("formal_shape"), f"{label}.formal_shape")

    ams = _require_string_array(row.get("ams"), f"{label}.ams", nonempty=True)
    for ams_index, code in enumerate(ams):
        if re.fullmatch(r"[0-9]{2}(?:[A-Z][0-9]{2})?", code) is None:
            raise RenderError(f"{label}.ams[{ams_index}] has invalid syntax: {code!r}")
    primary = _require_string(row.get("primary_ams_class"), f"{label}.primary_ams_class")
    if re.fullmatch(r"[0-9]{2}", primary) is None or not any(
        code.startswith(primary) for code in ams
    ):
        raise RenderError(f"{label}.primary_ams_class is not represented in ams")
    _require_string(row.get("classification_status"), f"{label}.classification_status")
    _require_string(row.get("raw_category"), f"{label}.raw_category")
    _require_string(row.get("raw_status"), f"{label}.raw_status")
    _validate_statement_aliases(row, label)
    _validate_rights(row.get("rights"), f"{label}.rights")

    if category == "theorem":
        if kind not in SCHEMA_THEOREM_KINDS or material_status != "proved":
            raise RenderError(f"{label} theorem category has incompatible kind/status")
    elif category == "open_claim":
        if kind not in SCHEMA_OPEN_KINDS or material_status not in SCHEMA_OPEN_STATUSES:
            raise RenderError(f"{label} open-claim category has incompatible kind/status")
    else:
        raise RenderError(f"{label}.category has unknown value {category!r}")

    if row.get("lifecycle") != "active":
        raise RenderError(f"{label}.lifecycle must be active")
    return stage_id


def _validate_catalog(
    release: str,
    document: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, int]]:
    if document.get("release") != release:
        raise RenderError(f"{CATALOG_NAME}.release does not match {release}")
    authority = _require_string(
        document.get("authority_sha256"), f"{CATALOG_NAME}.authority_sha256", SHA256_RE
    )
    authority_body = {key: value for key, value in document.items() if key != "authority_sha256"}
    observed_authority = _sha256_bytes(_canonical_json_bytes(authority_body))
    if authority != observed_authority:
        raise RenderError(
            f"{CATALOG_NAME} authority mismatch: declared={authority}, "
            f"observed={observed_authority}"
        )
    counts = _require_object(document.get("counts"), f"{CATALOG_NAME}.counts")
    for key in ("records", "origin_theorems", "origin_open_claims"):
        _require_nonnegative_int(counts.get(key), f"{CATALOG_NAME}.counts.{key}")
    for key in ("cumulative_theorems", "cumulative_open_claims"):
        _require_nonnegative_int(counts.get(key), f"{CATALOG_NAME}.counts.{key}")
    rows = _require_rows(document.get("records"), f"{CATALOG_NAME}.records")
    if counts["records"] != len(rows):
        raise RenderError(f"{CATALOG_NAME}.counts.records does not match records array")

    index: dict[str, dict[str, Any]] = {}
    previous_id: str | None = None
    for row_index, row in enumerate(rows):
        stage_id = _validate_catalog_record(row, row_index)
        if stage_id in index:
            raise RenderError(f"{CATALOG_NAME} duplicates {stage_id}")
        if previous_id is not None and stage_id <= previous_id:
            raise RenderError(f"{CATALOG_NAME}.records must be strictly sorted by S5 ID")
        previous_id = stage_id
        index[stage_id] = row

    predicate_counts = {
        "theorem": sum(
            row.get("origin_release") == release
            and _record_is_current_projection_member(row, "theorem")
            for row in index.values()
        ),
        "open_claim": sum(
            row.get("origin_release") == release
            and _record_is_current_projection_member(row, "open_claim")
            for row in index.values()
        ),
    }
    if counts["origin_theorems"] != predicate_counts["theorem"]:
        raise RenderError(f"{CATALOG_NAME}.counts.origin_theorems is stale")
    if counts["origin_open_claims"] != predicate_counts["open_claim"]:
        raise RenderError(f"{CATALOG_NAME}.counts.origin_open_claims is stale")
    cumulative_counts = {
        "theorem": sum(
            _record_is_current_projection_member(row, "theorem")
            for row in index.values()
        ),
        "open_claim": sum(
            _record_is_current_projection_member(row, "open_claim")
            for row in index.values()
        ),
    }
    if counts["cumulative_theorems"] != cumulative_counts["theorem"]:
        raise RenderError(f"{CATALOG_NAME}.counts.cumulative_theorems is stale")
    if counts["cumulative_open_claims"] != cumulative_counts["open_claim"]:
        raise RenderError(f"{CATALOG_NAME}.counts.cumulative_open_claims is stale")
    return index, predicate_counts


def _record_is_current_projection_member(row: Mapping[str, Any], bucket: str) -> bool:
    common = (
        row.get("origin_stage") == "Stage5"
        and row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("declaration_kind") == "theorem"
    )
    if bucket == "theorem":
        return (
            common
            and row.get("category") == "theorem"
            and row.get("current_claim_kind") == "theorem"
            and row.get("material_status") == "proved"
        )
    if bucket == "open_claim":
        return (
            common
            and row.get("category") == "open_claim"
            and row.get("current_claim_kind") in SCHEMA_OPEN_KINDS
            and row.get("material_status") in SCHEMA_OPEN_STATUSES
        )
    raise RenderError(f"unknown projection bucket: {bucket!r}")


def _validate_projection(
    release: str,
    name: str,
    document: dict[str, Any],
    catalog_index: Mapping[str, dict[str, Any]],
    bucket: str,
) -> list[str]:
    if document.get("release") != release:
        raise RenderError(f"{name}.release does not match {release}")
    counts = _require_object(document.get("counts"), f"{name}.counts")
    if set(counts) != {"records"}:
        raise RenderError(f"{name}.counts must contain only the checker records metric")
    declared_count = _require_nonnegative_int(counts.get("records"), f"{name}.counts.records")
    rows = _require_rows(document.get("records"), f"{name}.records")
    if declared_count != len(rows):
        raise RenderError(f"{name}.counts.records does not match records array")

    ids: list[str] = []
    for index, row in enumerate(rows):
        stage_id = _require_string(
            row.get("stage_claim_id"), f"{name}.records[{index}].stage_claim_id", S5_ID_RE
        )
        if stage_id not in catalog_index:
            raise RenderError(f"{name} references missing catalog record {stage_id}")
        if row != catalog_index[stage_id]:
            raise RenderError(
                f"{name}.records[{index}] is not an exact Claim_Catalog row copy for {stage_id}"
            )
        ids.append(stage_id)
    if ids != sorted(set(ids)):
        raise RenderError(f"{name}.records must be unique and strictly S5-ID sorted")
    projected_ids = _require_string_array(
        document.get("stage_claim_ids"),
        f"{name}.stage_claim_ids",
        pattern=S5_ID_RE,
    )
    if projected_ids != ids:
        raise RenderError(f"{name}.stage_claim_ids does not match its records")

    authority = _require_string(
        document.get("authority_sha256"), f"{name}.authority_sha256", SHA256_RE
    )
    authority_body = {key: value for key, value in document.items() if key != "authority_sha256"}
    observed_authority = _sha256_bytes(_canonical_json_bytes(authority_body))
    if authority != observed_authority:
        raise RenderError(
            f"{name} authority mismatch: declared={authority}, observed={observed_authority}"
        )

    expected = sorted(
        stage_id
        for stage_id, row in catalog_index.items()
        if _record_is_current_projection_member(row, bucket)
    )
    if ids != expected:
        missing = sorted(set(expected) - set(ids))
        extra = sorted(set(ids) - set(expected))
        raise RenderError(f"{name} is not the exact catalog predicate: missing={missing}, extra={extra}")
    return ids


def _validate_artifact_row_count(
    bindings: Mapping[str, Mapping[str, Any]], name: str, observed: int
) -> None:
    binding = bindings[name]
    if "row_count" not in binding:
        raise RenderError(f"manifest artifact {name} lacks row_count")
    declared = _require_nonnegative_int(binding["row_count"], f"manifest[{name}].row_count")
    if declared != observed:
        raise RenderError(
            f"manifest artifact {name} row_count mismatch: declared={declared}, observed={observed}"
        )


def _validate_document_authority(document: Mapping[str, Any], label: str) -> str:
    authority = _require_string(
        document.get("authority_sha256"), f"{label}.authority_sha256", SHA256_RE
    )
    observed = _sha256_bytes(
        _canonical_json_bytes(
            {key: value for key, value in document.items() if key != "authority_sha256"}
        )
    )
    if authority != observed:
        raise RenderError(
            f"{label} authority mismatch: declared={authority}, observed={observed}"
        )
    return authority


def _set_digest(values: Iterable[str]) -> str:
    return _sha256_bytes(_canonical_json_bytes(sorted(values)))


def _validate_catalog_record_v5_2(row: dict[str, Any], index: int) -> str:
    """Validate fields that the renderer consumes from one native 5.2 row."""

    label = f"catalog.records[{index}]"
    if row.get("schema_version") != "awesome-theorems/stage5-math-claim-record/5.2":
        raise RenderError(f"{label}.schema_version is not the 5.2 record schema")
    stage_id = _require_string(row.get("stage_claim_id"), f"{label}.stage_claim_id", S5_ID_RE)
    variant_id = _require_string(row.get("variant_id"), f"{label}.variant_id", ATV_ID_RE)
    ordinal_text = S5_ID_RE.fullmatch(stage_id).group(1)
    if ordinal_text != ATV_ID_RE.fullmatch(variant_id).group(1):
        raise RenderError(f"{label} S5 and ATV ordinals differ")
    if row.get("occurrence_id") != f"ATO-{ordinal_text}" or row.get("sense_id") != f"ATS-{ordinal_text}":
        raise RenderError(f"{label} ATO/ATS ordinals do not match the S5 ID")
    if not re.fullmatch(r"ATF-[0-9]{8}", str(row.get("family_id", ""))):
        raise RenderError(f"{label}.family_id is invalid")
    if row.get("release_id") != "5.2" or row.get("origin_release") != "5.2":
        raise RenderError(f"{label} release identity is invalid")
    if row.get("origin_stage") != "Stage5" or row.get("owner_domain") != "mathematics":
        raise RenderError(f"{label} stage/domain identity is invalid")
    if row.get("membership_domains") != ["mathematics"]:
        raise RenderError(f"{label}.membership_domains must be mathematics only")
    if not (
        row.get("record_role") == "claim"
        and row.get("claim_kind") == "conjecture"
        and row.get("current_claim_kind") == "conjecture"
        and row.get("historical_kind") == "conjecture"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "open_claim"
        and row.get("material_status") == "open"
        and row.get("lifecycle") == "active"
    ):
        raise RenderError(f"{label} is not one active atomic open conjecture")
    _require_string(row.get("display_name"), f"{label}.display_name")
    _require_string_array(row.get("aliases"), f"{label}.aliases")
    source_id = _require_string(row.get("source_id"), f"{label}.source_id", SOURCE_ID_RE)
    if source_id != "SRC-MATH-V5-OPENCONJECTURE-FA03D85":
        raise RenderError(f"{label}.source_id is not the pinned 5.2 source")

    statement = _require_object(row.get("mathematical_statement"), f"{label}.mathematical_statement")
    statement_sha = _require_string(
        statement.get("statement_sha256"),
        f"{label}.mathematical_statement.statement_sha256",
        SHA256_RE,
    )
    statement_without_hash = {
        key: value for key, value in statement.items() if key != "statement_sha256"
    }
    if _sha256_bytes(_canonical_json_bytes(statement_without_hash)) != statement_sha:
        raise RenderError(f"{label}.mathematical_statement hash is stale")
    body_tex = _require_string(statement.get("body_tex"), f"{label}.mathematical_statement.body_tex")
    plain_text = _require_string(
        statement.get("plain_text"), f"{label}.mathematical_statement.plain_text"
    )
    if _sha256_text(body_tex) != statement.get("body_tex_sha256"):
        raise RenderError(f"{label}.mathematical_statement.body_tex hash is stale")
    if _sha256_text(plain_text) != statement.get("plain_text_sha256"):
        raise RenderError(f"{label}.mathematical_statement.plain_text hash is stale")

    source_block = _require_object(row.get("source_block"), f"{label}.source_block")
    if source_block.get("body_tex") != body_tex or source_block.get("plain_text") != plain_text:
        raise RenderError(f"{label} source block and mathematical statement differ")
    source_locator = _require_object(row.get("source_locator"), f"{label}.source_locator")
    if source_locator.get("source_id") != source_id:
        raise RenderError(f"{label}.source_locator source ID differs")
    for key in (
        "content_hash",
        "source_record_sha256",
        "eligible_pool_sha256",
        "upstream_asset_sha256",
    ):
        _require_string(source_locator.get(key), f"{label}.source_locator.{key}", SHA256_RE)
    _require_string(source_locator.get("arxiv_id"), f"{label}.source_locator.arxiv_id")
    for key in ("eligible_pool_line_number", "upstream_line_number", "line_start", "line_end"):
        _require_nonnegative_int(source_locator.get(key), f"{label}.source_locator.{key}")

    status = _require_object(row.get("status_detail"), f"{label}.status_detail")
    _require_string(status.get("status_as_of"), f"{label}.status_detail.status_as_of", DATE_RE)
    if (
        status.get("evidence_level") != "source_dataset_model_assertion"
        or status.get("independent_current_status_review") is not False
    ):
        raise RenderError(f"{label} inflates the 5.2 source/model status assertion")
    model = _require_object(row.get("model_label"), f"{label}.model_label")
    if (
        model.get("label") != "real_open_conjecture"
        or model.get("source_model_assertion_not_independent_status_review") is not True
        or model.get("source_model_assertion_not_proof") is not True
    ):
        raise RenderError(f"{label}.model_label lacks the required limitations")
    disposition = _require_object(
        row.get("curator_disposition"), f"{label}.curator_disposition"
    )
    if not (
        disposition.get("grants_release_entry") is True
        and disposition.get("grants_strict_conjecture_credit") is True
        and disposition.get("human_status_review_performed") is False
    ):
        raise RenderError(f"{label}.curator_disposition is inconsistent")
    rights = _require_object(row.get("rights"), f"{label}.rights")
    if not (
        rights.get("spdx_expression") == "CC-BY-4.0"
        and rights.get("publication_text_allowed") is True
        and rights.get("text_withheld") is False
        and rights.get("catalog_relicenses_source") is False
    ):
        raise RenderError(f"{label}.rights does not permit this readable projection")
    paper = _require_object(row.get("paper"), f"{label}.paper")
    if paper.get("arxiv_id") != source_locator.get("arxiv_id"):
        raise RenderError(f"{label} paper and source locator arXiv IDs differ")
    _require_string(paper.get("title"), f"{label}.paper.title")
    _require_string_array(paper.get("authors"), f"{label}.paper.authors", nonempty=True)

    expected_content_hash = _sha256_bytes(
        _canonical_json_bytes(
            {"source_block": source_block, "mathematical_statement": statement}
        )
    )
    if row.get("content_payload_sha256") != expected_content_hash:
        raise RenderError(f"{label}.content_payload_sha256 is stale")
    expected_source_hash = _sha256_bytes(
        _canonical_json_bytes(
            {"source_locator": source_locator, "paper": paper, "model_label": model}
        )
    )
    if row.get("source_payload_sha256") != expected_source_hash:
        raise RenderError(f"{label}.source_payload_sha256 is stale")
    semantic_key = _require_string(row.get("semantic_key"), f"{label}.semantic_key")
    expected_semantic_hash = _sha256_bytes(
        _canonical_json_bytes(
            {
                "record_role": row["record_role"],
                "atomicity": row["atomicity"],
                "truth_apt": row["truth_apt"],
                "category": row["category"],
                "current_claim_kind": row["current_claim_kind"],
                "semantic_key": semantic_key,
                "statement_sha256": statement_sha,
            }
        )
    )
    if row.get("semantic_payload_sha256") != expected_semantic_hash:
        raise RenderError(f"{label}.semantic_payload_sha256 is stale")
    return stage_id


def _record_is_current_projection_member_v5_2(
    row: Mapping[str, Any], bucket: str
) -> bool:
    if row.get("origin_release") != "5.2":
        return _record_is_current_projection_member(row, bucket)
    common = (
        row.get("origin_stage") == "Stage5"
        and row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
    )
    if bucket == "theorem":
        return bool(
            common
            and row.get("category") == "theorem"
            and row.get("current_claim_kind") == "theorem"
            and row.get("material_status") == "proved"
        )
    if bucket == "open_claim":
        return bool(
            common
            and row.get("category") == "open_claim"
            and row.get("current_claim_kind") in SCHEMA_OPEN_KINDS
            and row.get("material_status") in SCHEMA_OPEN_STATUSES
        )
    raise RenderError(f"unknown projection bucket: {bucket!r}")


def _validate_catalog_record_v5_3(
    row: dict[str, Any],
    index: int,
    *,
    release: str = "5.3",
) -> str:
    """Validate the fields rendered from one native mathlib theorem row."""

    label = f"catalog.records[{index}]"
    if row.get("schema_version") != f"awesome-theorems/stage5-math-claim-record/{release}":
        raise RenderError(f"{label}.schema_version is not the {release} record schema")
    stage_id = _require_string(row.get("stage_claim_id"), f"{label}.stage_claim_id", S5_ID_RE)
    variant_id = _require_string(row.get("variant_id"), f"{label}.variant_id", ATV_ID_RE)
    ordinal_text = S5_ID_RE.fullmatch(stage_id).group(1)
    if ordinal_text != ATV_ID_RE.fullmatch(variant_id).group(1):
        raise RenderError(f"{label} S5 and ATV ordinals differ")
    if row.get("occurrence_id") != f"ATO-{ordinal_text}" or row.get("sense_id") != f"ATS-{ordinal_text}":
        raise RenderError(f"{label} ATO/ATS ordinals do not match the S5 ID")
    if not re.fullmatch(r"ATF-[0-9]{8}", str(row.get("family_id", ""))):
        raise RenderError(f"{label}.family_id is invalid")
    if row.get("release_id") != release or row.get("origin_release") != release:
        raise RenderError(f"{label} release identity is invalid")
    if row.get("origin_stage") != "Stage5" or row.get("owner_domain") != "mathematics":
        raise RenderError(f"{label} stage/domain identity is invalid")
    if row.get("membership_domains") != ["mathematics"]:
        raise RenderError(f"{label}.membership_domains must be mathematics only")
    if not (
        row.get("record_role") == "claim"
        and row.get("claim_kind") == "theorem"
        and row.get("current_claim_kind") == "theorem"
        and row.get("historical_kind") == "theorem"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "theorem"
        and row.get("material_status") == "proved"
        and row.get("lifecycle") == "active"
    ):
        raise RenderError(f"{label} is not one active atomic proved theorem")
    _require_string(row.get("display_name"), f"{label}.display_name")
    _require_string_array(row.get("aliases"), f"{label}.aliases")
    source_id = _require_string(row.get("source_id"), f"{label}.source_id", SOURCE_ID_RE)
    if source_id != "SRC-MATH-V5-MATHLIB-8A178386":
        raise RenderError(f"{label}.source_id is not the pinned mathlib source")

    locator = _require_object(row.get("source_locator"), f"{label}.source_locator")
    source_record_id = _require_string(
        locator.get("source_record_id"), f"{label}.source_locator.source_record_id"
    )
    if re.fullmatch(r"ML4-[A-F0-9]{20}", source_record_id) is None:
        raise RenderError(f"{label}.source_locator.source_record_id is invalid")
    if not (
        locator.get("source_id") == source_id
        and locator.get("artifact_path")
        == "Docs/catalog/v5/sources/mathlib-theorems-8a178386.json"
        and locator.get("artifact_sha256")
        == "236b9f6ac192eaf87215663bfd7fadb80c439b452049cef1747ea804c458637a"
        and locator.get("mathlib_commit")
        == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    ):
        raise RenderError(f"{label}.source_locator does not bind the pinned mathlib asset")
    _require_nonnegative_int(locator.get("record_index"), f"{label}.source_locator.record_index")
    _require_nonnegative_int(
        locator.get("artifact_size_bytes"), f"{label}.source_locator.artifact_size_bytes"
    )
    _require_string(locator.get("module"), f"{label}.source_locator.module")
    _require_string(locator.get("source_path"), f"{label}.source_locator.source_path")
    _require_string(locator.get("url"), f"{label}.source_locator.url")
    for key in ("source_record_sha256", "source_sha256"):
        _require_string(locator.get(key), f"{label}.source_locator.{key}", SHA256_RE)
    for range_name in ("source_range", "selection_range"):
        source_range = _require_object(
            locator.get(range_name), f"{label}.source_locator.{range_name}"
        )
        for key in (
            "line_start",
            "line_end",
            "column_start_zero_based",
            "column_end_zero_based",
        ):
            _require_nonnegative_int(
                source_range.get(key), f"{label}.source_locator.{range_name}.{key}"
            )
        if source_range["line_start"] < 1 or source_range["line_end"] < source_range["line_start"]:
            raise RenderError(f"{label}.source_locator.{range_name} is reversed")

    formal = _require_object(row.get("formal_statement"), f"{label}.formal_statement")
    if not (
        formal.get("language") == "Lean4"
        and formal.get("source_syntax_kind") == "theorem"
        and formal.get("declaration_kind") == "theorem"
        and formal.get("module") == locator.get("module")
    ):
        raise RenderError(f"{label}.formal_statement kind/module is invalid")
    declaration = _require_string(formal.get("declaration"), f"{label}.formal_statement.declaration")
    formal_type = _require_string(formal.get("formal_type"), f"{label}.formal_statement.formal_type")
    formal_type_sha = _require_string(
        formal.get("formal_type_sha256"), f"{label}.formal_statement.formal_type_sha256", SHA256_RE
    )
    docstring = _require_string(
        formal.get("formal_docstring"), f"{label}.formal_statement.formal_docstring"
    )
    if _sha256_text(formal_type) != formal_type_sha:
        raise RenderError(f"{label}.formal_statement.formal_type_sha256 is stale")
    if _sha256_text(docstring) != formal.get("formal_docstring_sha256"):
        raise RenderError(f"{label}.formal_statement.formal_docstring_sha256 is stale")

    statement = _require_object(row.get("mathematical_statement"), f"{label}.mathematical_statement")
    statement_sha = _require_string(
        statement.get("statement_sha256"), f"{label}.mathematical_statement.statement_sha256", SHA256_RE
    )
    if _sha256_bytes(
        _canonical_json_bytes(
            {key: value for key, value in statement.items() if key != "statement_sha256"}
        )
    ) != statement_sha:
        raise RenderError(f"{label}.mathematical_statement hash is stale")
    if not (
        statement.get("language") == "Lean4"
        and statement.get("formal_type") == formal_type
        and statement.get("formal_type_sha256") == formal_type_sha
    ):
        raise RenderError(f"{label} formal and mathematical statements differ")
    _require_string(
        statement.get("natural_language"), f"{label}.mathematical_statement.natural_language"
    )

    selection = _require_object(row.get("theorem_selection"), f"{label}.theorem_selection")
    if not (
        selection.get("source_record_id") == source_record_id
        and selection.get("display_label") == row.get("display_name")
    ):
        raise RenderError(f"{label}.theorem_selection identity differs")
    _require_string(selection.get("selection_phase"), f"{label}.theorem_selection.selection_phase")
    _require_string(selection.get("selection_cohort"), f"{label}.theorem_selection.selection_cohort")
    _require_string(selection.get("module_root"), f"{label}.theorem_selection.module_root")
    _require_nonnegative_int(selection.get("selection_rank"), f"{label}.theorem_selection.selection_rank")
    _require_nonnegative_int(selection.get("phase_rank"), f"{label}.theorem_selection.phase_rank")
    _require_rows(selection.get("importance_signals"), f"{label}.theorem_selection.importance_signals")

    disposition = _require_object(
        row.get("curator_disposition"), f"{label}.curator_disposition"
    )
    if not (
        disposition.get("source_record_id") == source_record_id
        and disposition.get("target_s5_id") == stage_id
        and disposition.get("target_variant_id") == variant_id
        and disposition.get("disposition") == "accepted_new_kernel_checked_theorem"
        and disposition.get("grants_catalog_entry") is True
        and disposition.get("grants_theorem_credit") is True
        and disposition.get("semantic_key") == row.get("semantic_key")
    ):
        raise RenderError(f"{label}.curator_disposition is inconsistent")

    status = _require_object(row.get("status_detail"), f"{label}.status_detail")
    if not (
        status.get("source_material_status") == "proved_formal"
        and status.get("evidence_level") == "kernel_checked_sorry_free_at_pinned_commit"
        and status.get("later_commit_status_not_inferred") is True
        and status.get("status_as_of_commit")
        == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    ):
        raise RenderError(f"{label}.status_detail inflates or weakens pinned proof evidence")

    proof = _require_object(row.get("proof_evidence"), f"{label}.proof_evidence")
    proof_sha = _require_string(
        proof.get("proof_payload_sha256"), f"{label}.proof_evidence.proof_payload_sha256", SHA256_RE
    )
    if _sha256_bytes(
        _canonical_json_bytes(
            {key: value for key, value in proof.items() if key != "proof_payload_sha256"}
        )
    ) != proof_sha or row.get("proof_payload_sha256") != proof_sha:
        raise RenderError(f"{label}.proof_payload_sha256 is stale")
    if not (
        proof.get("formal_proof_state") == "kernel_checked_sorry_free"
        and proof.get("uses_sorry") is False
        and proof.get("verification")
        == "lean_checked_environment_thmInfo_and_collectAxioms_without_sorryAx"
        and proof.get("compiled_module") == locator.get("module")
        and proof.get("mathlib_commit") == locator.get("mathlib_commit")
        and proof.get("axiom_evidence_scope")
        == "batch_union_not_per_declaration_exact_dependencies"
    ):
        raise RenderError(f"{label}.proof_evidence is inconsistent")
    for key in ("ilean_sha256", "olean_sha256"):
        _require_string(proof.get(key), f"{label}.proof_evidence.{key}", SHA256_RE)
    _require_string_array(
        proof.get("batch_axiom_dependency_union"),
        f"{label}.proof_evidence.batch_axiom_dependency_union",
    )

    classification = _require_object(row.get("classification"), f"{label}.classification")
    if not (
        re.fullmatch(r"[0-9]{2}", str(classification.get("msc2020_code", "")))
        and classification.get("module_root") == selection.get("module_root")
        and classification.get("status") in {"source_curated_exact", "machine_root_crosswalk"}
    ):
        raise RenderError(f"{label}.classification is invalid")
    importance = _require_object(row.get("importance"), f"{label}.importance")
    if importance.get("independent_universal_ranking_claimed") is not False:
        raise RenderError(f"{label}.importance claims an unsupported universal ranking")
    rights = _require_object(row.get("rights"), f"{label}.rights")
    rights_sha = _require_string(
        rights.get("rights_payload_sha256"), f"{label}.rights.rights_payload_sha256", SHA256_RE
    )
    if _sha256_bytes(
        _canonical_json_bytes(
            {key: value for key, value in rights.items() if key != "rights_payload_sha256"}
        )
    ) != rights_sha:
        raise RenderError(f"{label}.rights_payload_sha256 is stale")
    if not (
        rights.get("formal_code_terms") == "Apache-2.0"
        and rights.get("docstring_terms") == "Apache-2.0"
        and rights.get("redistribution_mode") == "apache_2_0_with_attribution"
        and rights.get("catalog_relicenses_source") is False
        and rights.get("attribution") == ["The mathlib Community"]
    ):
        raise RenderError(f"{label}.rights is inconsistent")
    provenance = _require_object(row.get("provenance"), f"{label}.provenance")
    if not (
        provenance.get("formal_source_ref") == source_id
        and provenance.get("source_record_id") == source_record_id
        and provenance.get("source_record_sha256") == locator.get("source_record_sha256")
        and provenance.get("mathlib_commit") == locator.get("mathlib_commit")
        and provenance.get("exact_source_replay_required") is True
    ):
        raise RenderError(f"{label}.provenance is inconsistent")

    if row.get("content_payload_sha256") != _sha256_bytes(
        _canonical_json_bytes(
            {"formal_statement": formal, "mathematical_statement": statement}
        )
    ):
        raise RenderError(f"{label}.content_payload_sha256 is stale")
    if row.get("source_payload_sha256") != _sha256_bytes(
        _canonical_json_bytes(
            {"source_locator": locator, "theorem_selection": selection, "provenance": provenance}
        )
    ):
        raise RenderError(f"{label}.source_payload_sha256 is stale")
    semantic_key = _require_string(row.get("semantic_key"), f"{label}.semantic_key")
    if semantic_key != "mathlib-theorem-semantic/" + formal_type_sha:
        raise RenderError(f"{label}.semantic_key does not bind the formal type")
    if row.get("semantic_payload_sha256") != _sha256_bytes(
        _canonical_json_bytes(
            {
                "record_role": row["record_role"],
                "atomicity": row["atomicity"],
                "truth_apt": row["truth_apt"],
                "category": row["category"],
                "current_claim_kind": row["current_claim_kind"],
                "semantic_key": semantic_key,
                "statement_sha256": statement_sha,
            }
        )
    ):
        raise RenderError(f"{label}.semantic_payload_sha256 is stale")
    if formal.get("declaration") != declaration:
        raise RenderError(f"{label}.formal_statement declaration drifted")
    return stage_id


def _record_is_current_projection_member_v5_3(
    row: Mapping[str, Any], bucket: str
) -> bool:
    if row.get("origin_release") != "5.3":
        return _record_is_current_projection_member_v5_2(row, bucket)
    common = (
        row.get("origin_stage") == "Stage5"
        and row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
    )
    if bucket == "theorem":
        return bool(
            common
            and row.get("category") == "theorem"
            and row.get("claim_kind") == "theorem"
            and row.get("current_claim_kind") == "theorem"
            and row.get("material_status") == "proved"
        )
    if bucket == "open_claim":
        return bool(
            common
            and row.get("category") == "open_claim"
            and row.get("current_claim_kind") in SCHEMA_OPEN_KINDS
            and row.get("material_status") in SCHEMA_OPEN_STATUSES
        )
    raise RenderError(f"unknown projection bucket: {bucket!r}")


def _validate_catalog_v5_2(
    document: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    if document.get("release") != "5.2":
        raise RenderError(f"{CATALOG_NAME}.release does not match 5.2")
    if document.get("schema_version") != "awesome-theorems/stage5-claim-catalog/5.2":
        raise RenderError(f"{CATALOG_NAME}.schema_version does not match 5.2")
    _validate_document_authority(document, CATALOG_NAME)
    counts = _require_object(document.get("counts"), f"{CATALOG_NAME}.counts")
    expected_counts = {
        "records": 3100,
        "origin_theorems": 0,
        "origin_open_claims": 600,
        "cumulative_theorems": 1500,
        "cumulative_open_claims": 1600,
    }
    if counts != expected_counts:
        raise RenderError(f"{CATALOG_NAME}.counts is not the accepted 5.2 count set")
    rows = _require_rows(document.get("records"), f"{CATALOG_NAME}.records")
    if len(rows) != counts["records"]:
        raise RenderError(f"{CATALOG_NAME}.records length is stale")
    index: dict[str, dict[str, Any]] = {}
    previous: str | None = None
    for row_index, row in enumerate(rows):
        if row.get("origin_release") == "5.2":
            stage_id = _validate_catalog_record_v5_2(row, row_index)
        else:
            stage_id = _validate_catalog_record(row, row_index)
        if stage_id in index or (previous is not None and stage_id <= previous):
            raise RenderError(f"{CATALOG_NAME}.records are not unique strict S5-ID order")
        previous = stage_id
        index[stage_id] = row
    theorem_count = sum(
        _record_is_current_projection_member_v5_2(row, "theorem") for row in rows
    )
    open_count = sum(
        _record_is_current_projection_member_v5_2(row, "open_claim") for row in rows
    )
    origin_theorems = sum(
        row.get("origin_release") == "5.2"
        and _record_is_current_projection_member_v5_2(row, "theorem")
        for row in rows
    )
    origin_open = sum(
        row.get("origin_release") == "5.2"
        and _record_is_current_projection_member_v5_2(row, "open_claim")
        for row in rows
    )
    if (theorem_count, open_count, origin_theorems, origin_open) != (1500, 1600, 0, 600):
        raise RenderError("5.2 catalog predicate counts do not match its declared counts")
    return index


def _validate_projection_v5_2(
    name: str,
    document: dict[str, Any],
    catalog_index: Mapping[str, dict[str, Any]],
    bucket: str,
) -> list[str]:
    if document.get("release") != "5.2":
        raise RenderError(f"{name}.release does not match 5.2")
    if document.get("schema_version") != "awesome-theorems/stage5-query-projection/5.2":
        raise RenderError(f"{name}.schema_version does not match 5.2")
    _validate_document_authority(document, name)
    counts = _require_object(document.get("counts"), f"{name}.counts")
    if set(counts) != {"records"}:
        raise RenderError(f"{name}.counts has an invalid field set")
    rows = _require_rows(document.get("records"), f"{name}.records")
    if counts.get("records") != len(rows):
        raise RenderError(f"{name}.counts.records does not match records")
    ids: list[str] = []
    for index, row in enumerate(rows):
        stage_id = _require_string(
            row.get("stage_claim_id"), f"{name}.records[{index}].stage_claim_id", S5_ID_RE
        )
        if stage_id not in catalog_index or row != catalog_index[stage_id]:
            raise RenderError(f"{name}.records[{index}] is not an exact catalog row")
        ids.append(stage_id)
    if ids != sorted(set(ids)) or document.get("stage_claim_ids") != ids:
        raise RenderError(f"{name} IDs are not one sorted exact projection")
    expected = sorted(
        stage_id
        for stage_id, row in catalog_index.items()
        if _record_is_current_projection_member_v5_2(row, bucket)
    )
    if ids != expected:
        raise RenderError(f"{name} is not the exact 5.2 catalog predicate")
    return ids


def _record_evidence_components_v5_2(row: Mapping[str, Any]) -> dict[str, str]:
    if row.get("origin_release") == "5.2":
        content_hash = str(row["content_payload_sha256"])
        source_hash = str(row["source_payload_sha256"])
        rights_hash = str(row["rights"]["rights_payload_sha256"])
    else:
        content_hash = _sha256_bytes(
            _canonical_json_bytes(
                {
                    "formal_statement": row.get("formal_statement"),
                    "mathematical_statement": row.get("mathematical_statement"),
                }
            )
        )
        source_hash = _sha256_bytes(
            _canonical_json_bytes(
                {
                    "source_id": row.get("source_id"),
                    "locator": row.get("locator"),
                    "formal_statement": row.get("formal_statement"),
                    "provenance": row.get("provenance"),
                }
            )
        )
        rights_hash = _sha256_bytes(_canonical_json_bytes(row["rights"]))
    return {
        "record_sha256": _sha256_bytes(_canonical_json_bytes(row)),
        "content_payload_sha256": content_hash,
        "source_payload_sha256": source_hash,
        "rights_payload_sha256": rights_hash,
        "allocation_request_sha256": str(row["allocation"]["allocation_request_sha256"]),
    }


def _validate_strict_ledger_v5_2(
    document: dict[str, Any],
    catalog_index: Mapping[str, dict[str, Any]],
    manifest: Mapping[str, Any],
) -> list[str]:
    if document.get("schema_version") != "awesome-theorems/stage5-strict-conjecture-ledger/5.2":
        raise RenderError(f"{STRICT_JSON_NAME}.schema_version does not match 5.2")
    if document.get("release") != "5.2":
        raise RenderError(f"{STRICT_JSON_NAME}.release does not match 5.2")
    authority = _validate_document_authority(document, STRICT_JSON_NAME)
    if document.get("parent_release_root_sha256") != manifest.get("parent_release_root_sha256"):
        raise RenderError(f"{STRICT_JSON_NAME} parent root differs from the manifest")
    credits = _require_rows(document.get("strict_credits"), f"{STRICT_JSON_NAME}.strict_credits")
    corrections = _require_rows(
        document.get("credit_corrections"), f"{STRICT_JSON_NAME}.credit_corrections"
    )
    counts = _require_object(document.get("counts"), f"{STRICT_JSON_NAME}.counts")
    if counts != {
        "effective_strict_credits": 1000,
        "effective_parent_credits": 400,
        "origin_5_2_credits": 600,
        "credit_corrections": 1,
    } or len(credits) != 1000 or len(corrections) != 1:
        raise RenderError(f"{STRICT_JSON_NAME} count set is invalid")
    ids: list[str] = []
    variants: list[str] = []
    parent_ids: list[str] = []
    origin_ids: list[str] = []
    for index, credit in enumerate(credits):
        expected_fields = {
            "stage_claim_id",
            "variant_id",
            "origin_release",
            "credit_source_branch",
            "semantic_key",
            "grants_strict_conjecture_credit",
            "evidence_sha256",
            "row_sha256",
        }
        if set(credit) != expected_fields:
            raise RenderError(f"strict_credits[{index}] field set is invalid")
        row_sha = _require_string(credit.get("row_sha256"), f"strict_credits[{index}].row_sha256", SHA256_RE)
        observed_row_sha = _sha256_bytes(
            _canonical_json_bytes(
                {key: value for key, value in credit.items() if key != "row_sha256"}
            )
        )
        if row_sha != observed_row_sha:
            raise RenderError(f"strict_credits[{index}].row_sha256 is stale")
        stage_id = _require_string(
            credit.get("stage_claim_id"), f"strict_credits[{index}].stage_claim_id", S5_ID_RE
        )
        variant_id = _require_string(
            credit.get("variant_id"), f"strict_credits[{index}].variant_id", ATV_ID_RE
        )
        if stage_id not in catalog_index:
            raise RenderError(f"strict_credits[{index}] references missing {stage_id}")
        row = catalog_index[stage_id]
        if variant_id != row.get("variant_id") or credit.get("origin_release") != row.get("origin_release"):
            raise RenderError(f"strict_credits[{index}] identity differs from the catalog")
        if not (
            credit.get("grants_strict_conjecture_credit") is True
            and row.get("category") == "open_claim"
            and row.get("current_claim_kind") == "conjecture"
            and row.get("material_status") == "open"
        ):
            raise RenderError(f"strict_credits[{index}] is not an effective open conjecture")
        expected_semantic_key = row.get("semantic_key")
        if not isinstance(expected_semantic_key, str):
            expected_semantic_key = "formal-conjectures-semantic/" + str(
                row["semantic_payload_sha256"]
            )
        if credit.get("semantic_key") != expected_semantic_key:
            raise RenderError(f"strict_credits[{index}] semantic key differs from the catalog")
        expected_evidence = _sha256_bytes(
            _canonical_json_bytes(_record_evidence_components_v5_2(row))
        )
        if credit.get("evidence_sha256") != expected_evidence:
            raise RenderError(f"strict_credits[{index}] evidence hash is stale")
        branch = credit.get("credit_source_branch")
        if branch == "effective_parent_5_1_direct_prop":
            if row.get("formal_shape") != "direct_prop" or row.get("origin_release") == "5.2":
                raise RenderError(f"strict_credits[{index}] has an invalid parent branch")
            parent_ids.append(stage_id)
        elif branch == "origin_5_2_curated_latex_environment":
            if row.get("origin_release") != "5.2":
                raise RenderError(f"strict_credits[{index}] has an invalid 5.2 branch")
            origin_ids.append(stage_id)
        else:
            raise RenderError(f"strict_credits[{index}] has an unknown source branch")
        ids.append(stage_id)
        variants.append(variant_id)
    if ids != sorted(set(ids)) or variants != sorted(set(variants)):
        raise RenderError(f"{STRICT_JSON_NAME}.strict_credits is not unique sorted order")
    if len(parent_ids) != 400 or len(origin_ids) != 600:
        raise RenderError(f"{STRICT_JSON_NAME} parent/origin partitions are invalid")

    correction = corrections[0]
    if not (
        correction.get("stage_claim_id") == "S5-CLM-00005311"
        and correction.get("variant_id") == "ATV-00005311"
        and correction.get("disposition") == "strict_credit_revoked"
        and correction.get("effective_release") == "5.2"
        and correction.get("grants_strict_conjecture_credit") is False
    ):
        raise RenderError("Moving Sofa strict-credit correction is invalid")
    corrected_row = catalog_index["S5-CLM-00005311"]
    if correction.get("parent_record_sha256") != _sha256_bytes(
        _canonical_json_bytes(corrected_row)
    ):
        raise RenderError("Moving Sofa correction record hash is stale")
    if correction["stage_claim_id"] in ids:
        raise RenderError("Moving Sofa remains in the effective strict-credit set")

    digests = _require_object(document.get("set_digests"), f"{STRICT_JSON_NAME}.set_digests")
    expected_digests = {
        "effective_s5_id_set_sha256": _set_digest(ids),
        "effective_variant_id_set_sha256": _set_digest(variants),
        "effective_parent_s5_id_set_sha256": _set_digest(parent_ids),
        "origin_5_2_s5_id_set_sha256": _set_digest(origin_ids),
    }
    if digests != expected_digests:
        raise RenderError(f"{STRICT_JSON_NAME}.set_digests is stale")
    binding = _require_object(
        manifest.get("strict_credit_binding"), "manifest.strict_credit_binding"
    )
    if not (
        binding.get("authority_sha256") == authority
        and binding.get("effective_s5_id_set_sha256")
        == digests["effective_s5_id_set_sha256"]
        and binding.get("effective_variant_id_set_sha256")
        == digests["effective_variant_id_set_sha256"]
    ):
        raise RenderError("manifest strict-credit binding differs from the ledger")
    return ids


def _load_release_v5_2(
    release_root: Path, manifest_bytes: bytes
) -> ReleaseBundle:
    manifest = _strict_json_bytes(manifest_bytes, MANIFEST_NAME)
    bindings = _validate_manifest("5.2", release_root, manifest)
    catalog = _strict_json_bytes(
        _safe_release_file(release_root, CATALOG_NAME).read_bytes(), CATALOG_NAME
    )
    theorem = _strict_json_bytes(
        _safe_release_file(release_root, THEOREM_JSON_NAME).read_bytes(), THEOREM_JSON_NAME
    )
    open_claim = _strict_json_bytes(
        _safe_release_file(release_root, OPEN_JSON_NAME).read_bytes(), OPEN_JSON_NAME
    )
    strict = _strict_json_bytes(
        _safe_release_file(release_root, STRICT_JSON_NAME).read_bytes(), STRICT_JSON_NAME
    )
    catalog_index = _validate_catalog_v5_2(catalog)
    theorem_ids = _validate_projection_v5_2(
        THEOREM_JSON_NAME, theorem, catalog_index, "theorem"
    )
    open_ids = _validate_projection_v5_2(
        OPEN_JSON_NAME, open_claim, catalog_index, "open_claim"
    )
    strict_ids = _validate_strict_ledger_v5_2(strict, catalog_index, manifest)
    if set(theorem_ids) & set(open_ids):
        raise RenderError("5.2 theorem and open-claim projections overlap")
    _validate_artifact_row_count(bindings, CATALOG_NAME, len(catalog_index))
    _validate_artifact_row_count(bindings, THEOREM_JSON_NAME, len(theorem_ids))
    _validate_artifact_row_count(bindings, OPEN_JSON_NAME, len(open_ids))
    _validate_artifact_row_count(
        bindings,
        STRICT_JSON_NAME,
        len(strict.get("strict_credits", [])) + len(strict.get("credit_corrections", [])),
    )
    manifest_counts = manifest["counts"]
    if not (
        manifest_counts["catalog_records"] == len(catalog_index)
        and manifest_counts["cumulative_theorems"] == len(theorem_ids)
        and manifest_counts["cumulative_open_claims"] == len(open_ids)
        and manifest_counts["effective_strict_conjecture_credits"] == len(strict_ids)
        and manifest_counts["origin_theorems"] == 0
        and manifest_counts["origin_open_claims"] == 600
    ):
        raise RenderError("5.2 manifest counts do not match explicit release rows")

    parent_manifest_bytes = (RELEASES_DIR / "5.1" / MANIFEST_NAME).read_bytes()
    parent = _load_release("5.1", RELEASES_DIR / "5.1", parent_manifest_bytes)
    parent_rows = parent.catalog["records"]
    if catalog["records"][: len(parent_rows)] != parent_rows:
        raise RenderError("5.2 catalog does not preserve the exact 5.1 parent prefix")
    if theorem["records"] != parent.theorem["records"]:
        raise RenderError("5.2 theorem projection changed its 5.1 parent")
    if open_claim["records"][: len(parent.open_claim["records"])] != parent.open_claim["records"]:
        raise RenderError("5.2 open projection does not preserve the 5.1 parent prefix")
    new_rows = catalog["records"][len(parent_rows) :]
    expected_new_ids = [f"S5-CLM-{value:08d}" for value in range(5985, 6585)]
    if [row["stage_claim_id"] for row in new_rows] != expected_new_ids:
        raise RenderError("5.2 new record IDs are not the fixed append-only suffix")
    accepted = manifest["accepted_set_digests"]
    if accepted != {
        "content_hash_set_sha256": _set_digest(
            str(row["source_locator"]["content_hash"]) for row in new_rows
        ),
        "semantic_key_set_sha256": _set_digest(str(row["semantic_key"]) for row in new_rows),
        "s5_id_set_sha256": _set_digest(str(row["stage_claim_id"]) for row in new_rows),
    }:
        raise RenderError("5.2 manifest accepted-set digests are stale")
    return ReleaseBundle(
        release="5.2",
        release_root=release_root,
        manifest_bytes=manifest_bytes,
        manifest=manifest,
        artifact_bindings=bindings,
        catalog=catalog,
        theorem=theorem,
        open_claim=open_claim,
        strict_conjecture=strict,
        catalog_index=catalog_index,
    )


def _validate_catalog_v5_3(
    document: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    if document.get("release") != "5.3":
        raise RenderError(f"{CATALOG_NAME}.release does not match 5.3")
    if document.get("schema_version") != "awesome-theorems/stage5-claim-catalog/5.3":
        raise RenderError(f"{CATALOG_NAME}.schema_version does not match 5.3")
    _validate_document_authority(document, CATALOG_NAME)
    counts = _require_object(document.get("counts"), f"{CATALOG_NAME}.counts")
    expected_counts = {
        "records": 3600,
        "origin_theorems": 500,
        "origin_open_claims": 0,
        "cumulative_theorems": 2000,
        "cumulative_open_claims": 1600,
    }
    if counts != expected_counts:
        raise RenderError(f"{CATALOG_NAME}.counts is not the accepted 5.3 count set")
    rows = _require_rows(document.get("records"), f"{CATALOG_NAME}.records")
    if len(rows) != counts["records"]:
        raise RenderError(f"{CATALOG_NAME}.records length is stale")
    index: dict[str, dict[str, Any]] = {}
    previous: str | None = None
    for row_index, row in enumerate(rows):
        if row.get("origin_release") == "5.3":
            stage_id = _validate_catalog_record_v5_3(row, row_index)
        elif row.get("origin_release") == "5.2":
            stage_id = _validate_catalog_record_v5_2(row, row_index)
        else:
            stage_id = _validate_catalog_record(row, row_index)
        if stage_id in index or (previous is not None and stage_id <= previous):
            raise RenderError(f"{CATALOG_NAME}.records are not unique strict S5-ID order")
        previous = stage_id
        index[stage_id] = row
    theorem_count = sum(
        _record_is_current_projection_member_v5_3(row, "theorem") for row in rows
    )
    open_count = sum(
        _record_is_current_projection_member_v5_3(row, "open_claim") for row in rows
    )
    origin_theorems = sum(
        row.get("origin_release") == "5.3"
        and _record_is_current_projection_member_v5_3(row, "theorem")
        for row in rows
    )
    origin_open = sum(
        row.get("origin_release") == "5.3"
        and _record_is_current_projection_member_v5_3(row, "open_claim")
        for row in rows
    )
    if (theorem_count, open_count, origin_theorems, origin_open) != (2000, 1600, 500, 0):
        raise RenderError("5.3 catalog predicate counts do not match its declared counts")
    return index


def _validate_projection_v5_3(
    name: str,
    document: dict[str, Any],
    catalog_index: Mapping[str, dict[str, Any]],
    bucket: str,
) -> list[str]:
    if document.get("release") != "5.3":
        raise RenderError(f"{name}.release does not match 5.3")
    if document.get("schema_version") != "awesome-theorems/stage5-query-projection/5.3":
        raise RenderError(f"{name}.schema_version does not match 5.3")
    _validate_document_authority(document, name)
    counts = _require_object(document.get("counts"), f"{name}.counts")
    if set(counts) != {"records"}:
        raise RenderError(f"{name}.counts has an invalid field set")
    rows = _require_rows(document.get("records"), f"{name}.records")
    if counts.get("records") != len(rows):
        raise RenderError(f"{name}.counts.records does not match records")
    ids: list[str] = []
    for index, row in enumerate(rows):
        stage_id = _require_string(
            row.get("stage_claim_id"), f"{name}.records[{index}].stage_claim_id", S5_ID_RE
        )
        if stage_id not in catalog_index or row != catalog_index[stage_id]:
            raise RenderError(f"{name}.records[{index}] is not an exact catalog row")
        ids.append(stage_id)
    if ids != sorted(set(ids)) or document.get("stage_claim_ids") != ids:
        raise RenderError(f"{name} IDs are not one sorted exact projection")
    expected = sorted(
        stage_id
        for stage_id, row in catalog_index.items()
        if _record_is_current_projection_member_v5_3(row, bucket)
    )
    if ids != expected:
        raise RenderError(f"{name} is not the exact 5.3 catalog predicate")
    return ids


def _record_is_current_projection_member_v5_4(
    row: Mapping[str, Any], bucket: str
) -> bool:
    if row.get("origin_release") != "5.4":
        return _record_is_current_projection_member_v5_3(row, bucket)
    common = (
        row.get("origin_stage") == "Stage5"
        and row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
    )
    if bucket == "theorem":
        return bool(
            common
            and row.get("category") == "theorem"
            and row.get("claim_kind") == "theorem"
            and row.get("current_claim_kind") == "theorem"
            and row.get("material_status") == "proved"
        )
    if bucket == "open_claim":
        return bool(
            common
            and row.get("category") == "open_claim"
            and row.get("current_claim_kind") in SCHEMA_OPEN_KINDS
            and row.get("material_status") in SCHEMA_OPEN_STATUSES
        )
    raise RenderError(f"unknown projection bucket: {bucket!r}")


def _validate_catalog_v5_4(
    document: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    if document.get("release") != "5.4":
        raise RenderError(f"{CATALOG_NAME}.release does not match 5.4")
    if document.get("schema_version") != "awesome-theorems/stage5-claim-catalog/5.4":
        raise RenderError(f"{CATALOG_NAME}.schema_version does not match 5.4")
    _validate_document_authority(document, CATALOG_NAME)
    counts = _require_object(document.get("counts"), f"{CATALOG_NAME}.counts")
    expected_counts = {
        "records": 4100,
        "origin_theorems": 500,
        "origin_open_claims": 0,
        "cumulative_theorems": 2500,
        "cumulative_open_claims": 1600,
    }
    if counts != expected_counts:
        raise RenderError(f"{CATALOG_NAME}.counts is not the accepted 5.4 count set")
    rows = _require_rows(document.get("records"), f"{CATALOG_NAME}.records")
    if len(rows) != counts["records"]:
        raise RenderError(f"{CATALOG_NAME}.records length is stale")
    index: dict[str, dict[str, Any]] = {}
    previous: str | None = None
    for row_index, row in enumerate(rows):
        if row.get("origin_release") == "5.4":
            stage_id = _validate_catalog_record_v5_3(
                row, row_index, release="5.4"
            )
        elif row.get("origin_release") == "5.3":
            stage_id = _validate_catalog_record_v5_3(row, row_index)
        elif row.get("origin_release") == "5.2":
            stage_id = _validate_catalog_record_v5_2(row, row_index)
        else:
            stage_id = _validate_catalog_record(row, row_index)
        if stage_id in index or (previous is not None and stage_id <= previous):
            raise RenderError(f"{CATALOG_NAME}.records are not unique strict S5-ID order")
        previous = stage_id
        index[stage_id] = row
    theorem_count = sum(
        _record_is_current_projection_member_v5_4(row, "theorem") for row in rows
    )
    open_count = sum(
        _record_is_current_projection_member_v5_4(row, "open_claim") for row in rows
    )
    origin_theorems = sum(
        row.get("origin_release") == "5.4"
        and _record_is_current_projection_member_v5_4(row, "theorem")
        for row in rows
    )
    origin_open = sum(
        row.get("origin_release") == "5.4"
        and _record_is_current_projection_member_v5_4(row, "open_claim")
        for row in rows
    )
    if (theorem_count, open_count, origin_theorems, origin_open) != (2500, 1600, 500, 0):
        raise RenderError("5.4 catalog predicate counts do not match its declared counts")
    return index


def _validate_projection_v5_4(
    name: str,
    document: dict[str, Any],
    catalog_index: Mapping[str, dict[str, Any]],
    bucket: str,
) -> list[str]:
    if document.get("release") != "5.4":
        raise RenderError(f"{name}.release does not match 5.4")
    if document.get("schema_version") != "awesome-theorems/stage5-query-projection/5.4":
        raise RenderError(f"{name}.schema_version does not match 5.4")
    _validate_document_authority(document, name)
    counts = _require_object(document.get("counts"), f"{name}.counts")
    if set(counts) != {"records"}:
        raise RenderError(f"{name}.counts has an invalid field set")
    rows = _require_rows(document.get("records"), f"{name}.records")
    if counts.get("records") != len(rows):
        raise RenderError(f"{name}.counts.records does not match records")
    ids: list[str] = []
    for index, row in enumerate(rows):
        stage_id = _require_string(
            row.get("stage_claim_id"), f"{name}.records[{index}].stage_claim_id", S5_ID_RE
        )
        if stage_id not in catalog_index or row != catalog_index[stage_id]:
            raise RenderError(f"{name}.records[{index}] is not an exact catalog row")
        ids.append(stage_id)
    if ids != sorted(set(ids)) or document.get("stage_claim_ids") != ids:
        raise RenderError(f"{name} IDs are not one sorted exact projection")
    expected = sorted(
        stage_id
        for stage_id, row in catalog_index.items()
        if _record_is_current_projection_member_v5_4(row, bucket)
    )
    if ids != expected:
        raise RenderError(f"{name} is not the exact 5.4 catalog predicate")
    return ids


def _validate_strict_ledger_v5_3(
    document: dict[str, Any],
    parent: ReleaseBundle,
    manifest: Mapping[str, Any],
    *,
    release: str = "5.3",
) -> list[str]:
    expected_fields = {
        "schema_version",
        "release",
        "parent_release_root_sha256",
        "parent_strict_ledger_file_sha256",
        "parent_strict_ledger_authority_sha256",
        "strict_credits",
        "credit_corrections",
        "counts",
        "set_digests",
        "authority_sha256",
    }
    if set(document) != expected_fields:
        raise RenderError(f"{STRICT_JSON_NAME} {release} field set is invalid")
    if document.get("schema_version") != (
        f"awesome-theorems/stage5-strict-conjecture-ledger/{release}"
    ):
        raise RenderError(f"{STRICT_JSON_NAME}.schema_version does not match {release}")
    if document.get("release") != release:
        raise RenderError(f"{STRICT_JSON_NAME}.release does not match {release}")
    authority = _validate_document_authority(document, STRICT_JSON_NAME)
    parent_strict = parent.strict_conjecture
    if parent_strict is None:
        raise RenderError(f"{release} parent has no strict-conjecture ledger")
    parent_strict_path = parent.release_root / STRICT_JSON_NAME
    if not (
        document.get("parent_release_root_sha256")
        == parent.manifest.get("release_root_sha256")
        == manifest.get("parent_release_root_sha256")
        and document.get("parent_strict_ledger_file_sha256")
        == _sha256_file(parent_strict_path)[0]
        and document.get("parent_strict_ledger_authority_sha256")
        == parent_strict.get("authority_sha256")
    ):
        raise RenderError(f"{STRICT_JSON_NAME} parent binding is invalid")
    for field in ("strict_credits", "credit_corrections", "counts", "set_digests"):
        if document.get(field) != parent_strict.get(field):
            raise RenderError(f"{STRICT_JSON_NAME} changed inherited {field}")
    credits = _require_rows(document.get("strict_credits"), f"{STRICT_JSON_NAME}.strict_credits")
    corrections = _require_rows(
        document.get("credit_corrections"), f"{STRICT_JSON_NAME}.credit_corrections"
    )
    counts = _require_object(document.get("counts"), f"{STRICT_JSON_NAME}.counts")
    if len(credits) != counts.get("effective_strict_credits") or len(corrections) != counts.get("credit_corrections"):
        raise RenderError(f"{STRICT_JSON_NAME} inherited cardinality is stale")
    ids = [str(row["stage_claim_id"]) for row in credits]
    variants = [str(row["variant_id"]) for row in credits]
    digests = _require_object(document.get("set_digests"), f"{STRICT_JSON_NAME}.set_digests")
    if not (
        _set_digest(ids) == digests.get("effective_s5_id_set_sha256")
        and _set_digest(variants) == digests.get("effective_variant_id_set_sha256")
    ):
        raise RenderError(f"{STRICT_JSON_NAME} inherited set digests are stale")
    binding = _require_object(
        manifest.get("strict_credit_binding"), "manifest.strict_credit_binding"
    )
    if not (
        binding.get("path") == STRICT_JSON_NAME
        and binding.get("file_sha256")
        == _sha256_file(RELEASES_DIR / release / STRICT_JSON_NAME)[0]
        and binding.get("authority_sha256") == authority
        and binding.get("effective_s5_id_set_sha256")
        == digests.get("effective_s5_id_set_sha256")
        and binding.get("effective_variant_id_set_sha256")
        == digests.get("effective_variant_id_set_sha256")
    ):
        raise RenderError(
            f"{release} manifest strict-credit binding differs from the ledger"
        )
    return ids


def _load_release_v5_3(
    release_root: Path, manifest_bytes: bytes
) -> ReleaseBundle:
    manifest = _strict_json_bytes(manifest_bytes, MANIFEST_NAME)
    bindings = _validate_manifest("5.3", release_root, manifest)
    parent_manifest_bytes = (RELEASES_DIR / "5.2" / MANIFEST_NAME).read_bytes()
    parent = _load_release("5.2", RELEASES_DIR / "5.2", parent_manifest_bytes)
    catalog = _strict_json_bytes(
        _safe_release_file(release_root, CATALOG_NAME).read_bytes(), CATALOG_NAME
    )
    theorem = _strict_json_bytes(
        _safe_release_file(release_root, THEOREM_JSON_NAME).read_bytes(), THEOREM_JSON_NAME
    )
    open_claim = _strict_json_bytes(
        _safe_release_file(release_root, OPEN_JSON_NAME).read_bytes(), OPEN_JSON_NAME
    )
    strict = _strict_json_bytes(
        _safe_release_file(release_root, STRICT_JSON_NAME).read_bytes(), STRICT_JSON_NAME
    )
    catalog_index = _validate_catalog_v5_3(catalog)
    theorem_ids = _validate_projection_v5_3(
        THEOREM_JSON_NAME, theorem, catalog_index, "theorem"
    )
    open_ids = _validate_projection_v5_3(
        OPEN_JSON_NAME, open_claim, catalog_index, "open_claim"
    )
    strict_ids = _validate_strict_ledger_v5_3(strict, parent, manifest)
    if set(theorem_ids) & set(open_ids):
        raise RenderError("5.3 theorem and open-claim projections overlap")
    _validate_artifact_row_count(bindings, CATALOG_NAME, len(catalog_index))
    _validate_artifact_row_count(bindings, THEOREM_JSON_NAME, len(theorem_ids))
    _validate_artifact_row_count(bindings, OPEN_JSON_NAME, len(open_ids))
    _validate_artifact_row_count(
        bindings,
        STRICT_JSON_NAME,
        len(strict.get("strict_credits", [])) + len(strict.get("credit_corrections", [])),
    )
    manifest_counts = manifest["counts"]
    if not (
        manifest_counts["catalog_records"] == len(catalog_index)
        and manifest_counts["cumulative_theorems"] == len(theorem_ids)
        and manifest_counts["cumulative_open_claims"] == len(open_ids)
        and manifest_counts["effective_strict_conjecture_credits"] == len(strict_ids)
        and manifest_counts["origin_theorems"] == 500
        and manifest_counts["origin_open_claims"] == 0
    ):
        raise RenderError("5.3 manifest counts do not match explicit release rows")

    parent_rows = parent.catalog["records"]
    if catalog["records"][: len(parent_rows)] != parent_rows:
        raise RenderError("5.3 catalog does not preserve the exact 5.2 parent prefix")
    if theorem["records"][: len(parent.theorem["records"])] != parent.theorem["records"]:
        raise RenderError("5.3 theorem projection does not preserve its 5.2 parent prefix")
    if open_claim["records"] != parent.open_claim["records"]:
        raise RenderError("5.3 changed the 5.2 open-claim projection")
    new_rows = catalog["records"][len(parent_rows) :]
    if theorem["records"][len(parent.theorem["records"]) :] != new_rows:
        raise RenderError("5.3 theorem suffix differs from its catalog additions")
    expected_new_ids = [f"S5-CLM-{value:08d}" for value in range(6585, 7085)]
    if [row["stage_claim_id"] for row in new_rows] != expected_new_ids:
        raise RenderError("5.3 new record IDs are not the fixed append-only suffix")
    accepted = manifest["accepted_set_digests"]
    expected_accepted = {
        "source_record_id_set_sha256": _set_digest(
            str(row["source_locator"]["source_record_id"]) for row in new_rows
        ),
        "declaration_set_sha256": _set_digest(
            str(row["formal_statement"]["declaration"]) for row in new_rows
        ),
        "formal_type_sha256_set_sha256": _set_digest(
            str(row["formal_statement"]["formal_type_sha256"]) for row in new_rows
        ),
        "semantic_key_set_sha256": _set_digest(str(row["semantic_key"]) for row in new_rows),
        "variant_id_set_sha256": _set_digest(str(row["variant_id"]) for row in new_rows),
        "s5_id_set_sha256": _set_digest(str(row["stage_claim_id"]) for row in new_rows),
    }
    if accepted != expected_accepted:
        raise RenderError("5.3 manifest accepted-set digests are stale")
    return ReleaseBundle(
        release="5.3",
        release_root=release_root,
        manifest_bytes=manifest_bytes,
        manifest=manifest,
        artifact_bindings=bindings,
        catalog=catalog,
        theorem=theorem,
        open_claim=open_claim,
        strict_conjecture=strict,
        catalog_index=catalog_index,
    )


def _validate_coverage_v5_4(
    document: dict[str, Any],
    parent: ReleaseBundle,
    new_catalog_rows: list[dict[str, Any]],
) -> tuple[int, int]:
    expected_fields = {
        "schema_version",
        "release",
        "authoritative_inputs",
        "candidate_dispositions",
        "effective_state_policy",
        "msc_coverage",
        "counts",
        "authority_sha256",
    }
    if set(document) != expected_fields:
        raise RenderError(f"{COVERAGE_JSON_NAME} 5.4 field set is invalid")
    if document.get("schema_version") != "awesome-theorems/stage5-coverage-ledger/5.4":
        raise RenderError(f"{COVERAGE_JSON_NAME}.schema_version does not match 5.4")
    if document.get("release") != "5.4":
        raise RenderError(f"{COVERAGE_JSON_NAME}.release does not match 5.4")
    _validate_document_authority(document, COVERAGE_JSON_NAME)
    counts = _require_object(document.get("counts"), f"{COVERAGE_JSON_NAME}.counts")
    expected_counts = {
        "candidate_dispositions": 5898,
        "msc_coverage": 63,
        "origin_5_4_accepted_new_theorems": 500,
        "origin_5_4_candidates": 731,
        "origin_5_4_eligible_not_selected": 231,
        "origin_5_4_literal_lemma_noncredit": 0,
    }
    if counts != expected_counts:
        raise RenderError(f"{COVERAGE_JSON_NAME}.counts is not the accepted 5.4 count set")
    dispositions = _require_rows(
        document.get("candidate_dispositions"),
        f"{COVERAGE_JSON_NAME}.candidate_dispositions",
    )
    msc_rows = _require_rows(
        document.get("msc_coverage"), f"{COVERAGE_JSON_NAME}.msc_coverage"
    )
    if len(dispositions) != counts["candidate_dispositions"]:
        raise RenderError(f"{COVERAGE_JSON_NAME}.candidate_dispositions length is stale")
    if len(msc_rows) != counts["msc_coverage"]:
        raise RenderError(f"{COVERAGE_JSON_NAME}.msc_coverage length is stale")

    parent_coverage = _strict_json_bytes(
        _safe_release_file(parent.release_root, COVERAGE_JSON_NAME).read_bytes(),
        f"5.3/{COVERAGE_JSON_NAME}",
    )
    parent_dispositions = _require_rows(
        parent_coverage.get("candidate_dispositions"),
        f"5.3/{COVERAGE_JSON_NAME}.candidate_dispositions",
    )
    if dispositions[: len(parent_dispositions)] != parent_dispositions:
        raise RenderError("5.4 coverage dispositions do not preserve the exact 5.3 prefix")
    new_dispositions = dispositions[len(parent_dispositions) :]
    if len(new_dispositions) != 731 or any(
        row.get("origin_release") != "5.4" for row in new_dispositions
    ):
        raise RenderError("5.4 coverage suffix is not the exact 731-row residual cohort")
    accepted = [
        row
        for row in new_dispositions
        if row.get("disposition") == "accepted_new_kernel_checked_theorem"
    ]
    remaining = [
        row
        for row in new_dispositions
        if row.get("disposition") == "eligible_not_selected_after_5_4"
    ]
    if len(accepted) != 500 or len(remaining) != 231:
        raise RenderError("5.4 coverage suffix disposition cardinalities are stale")
    if any(row.get("source_syntax_kind") != "theorem" for row in new_dispositions):
        raise RenderError("5.4 coverage grants or reports a literal lemma in theorem quota")
    expected_new_ids = [row["stage_claim_id"] for row in new_catalog_rows]
    accepted_ids = [row.get("target_s5_id") for row in accepted]
    if sorted(accepted_ids) != sorted(expected_new_ids):
        raise RenderError("5.4 coverage accepted targets differ from catalog additions")
    if any(
        row.get("target_s5_id") is not None
        or row.get("target_variant_id") is not None
        or row.get("grants_catalog_entry") is not False
        or row.get("grants_theorem_credit") is not False
        for row in remaining
    ):
        raise RenderError("5.4 unselected residual theorem grants an ID or quota")
    return len(dispositions), len(msc_rows)


def _load_release_v5_4(
    release_root: Path, manifest_bytes: bytes
) -> ReleaseBundle:
    manifest = _strict_json_bytes(manifest_bytes, MANIFEST_NAME)
    bindings = _validate_manifest("5.4", release_root, manifest)
    parent_manifest_bytes = (RELEASES_DIR / "5.3" / MANIFEST_NAME).read_bytes()
    parent = _load_release("5.3", RELEASES_DIR / "5.3", parent_manifest_bytes)
    catalog = _strict_json_bytes(
        _safe_release_file(release_root, CATALOG_NAME).read_bytes(), CATALOG_NAME
    )
    theorem = _strict_json_bytes(
        _safe_release_file(release_root, THEOREM_JSON_NAME).read_bytes(), THEOREM_JSON_NAME
    )
    open_claim = _strict_json_bytes(
        _safe_release_file(release_root, OPEN_JSON_NAME).read_bytes(), OPEN_JSON_NAME
    )
    strict = _strict_json_bytes(
        _safe_release_file(release_root, STRICT_JSON_NAME).read_bytes(), STRICT_JSON_NAME
    )
    coverage = _strict_json_bytes(
        _safe_release_file(release_root, COVERAGE_JSON_NAME).read_bytes(), COVERAGE_JSON_NAME
    )
    catalog_index = _validate_catalog_v5_4(catalog)
    theorem_ids = _validate_projection_v5_4(
        THEOREM_JSON_NAME, theorem, catalog_index, "theorem"
    )
    open_ids = _validate_projection_v5_4(
        OPEN_JSON_NAME, open_claim, catalog_index, "open_claim"
    )
    strict_ids = _validate_strict_ledger_v5_3(
        strict, parent, manifest, release="5.4"
    )
    if set(theorem_ids) & set(open_ids):
        raise RenderError("5.4 theorem and open-claim projections overlap")

    parent_rows = parent.catalog["records"]
    if catalog["records"][: len(parent_rows)] != parent_rows:
        raise RenderError("5.4 catalog does not preserve the exact 5.3 parent prefix")
    if theorem["records"][: len(parent.theorem["records"])] != parent.theorem["records"]:
        raise RenderError("5.4 theorem projection does not preserve its 5.3 parent prefix")
    # The projection wrapper is release-native, but both member arrays are inherited.
    if (
        open_claim.get("records") != parent.open_claim.get("records")
        or open_claim.get("stage_claim_ids") != parent.open_claim.get("stage_claim_ids")
    ):
        raise RenderError("5.4 changed the 5.3 open-claim projection members")
    new_rows = catalog["records"][len(parent_rows) :]
    if theorem["records"][len(parent.theorem["records"]) :] != new_rows:
        raise RenderError("5.4 theorem suffix differs from its catalog additions")
    expected_new_ids = [f"S5-CLM-{value:08d}" for value in range(7085, 7585)]
    if [row["stage_claim_id"] for row in new_rows] != expected_new_ids:
        raise RenderError("5.4 new record IDs are not the fixed append-only suffix")
    expected_family_ids = [f"ATF-{value:08d}" for value in range(6855, 7355)]
    if [row["family_id"] for row in new_rows] != expected_family_ids:
        raise RenderError("5.4 new family IDs are not the fixed append-only suffix")
    if any(
        row.get("formal_statement", {}).get("source_syntax_kind") != "theorem"
        or row.get("proof_evidence", {}).get("formal_proof_state")
        != "kernel_checked_sorry_free"
        or row.get("proof_evidence", {}).get("uses_sorry") is not False
        for row in new_rows
    ):
        raise RenderError("5.4 additions are not 500 literal kernel-checked theorems")

    coverage_dispositions, coverage_msc = _validate_coverage_v5_4(
        coverage, parent, new_rows
    )
    _validate_artifact_row_count(bindings, CATALOG_NAME, len(catalog_index))
    _validate_artifact_row_count(bindings, THEOREM_JSON_NAME, len(theorem_ids))
    _validate_artifact_row_count(bindings, OPEN_JSON_NAME, len(open_ids))
    _validate_artifact_row_count(
        bindings,
        STRICT_JSON_NAME,
        len(strict.get("strict_credits", [])) + len(strict.get("credit_corrections", [])),
    )
    _validate_artifact_row_count(
        bindings,
        COVERAGE_JSON_NAME,
        coverage_dispositions + coverage_msc,
    )
    manifest_counts = manifest["counts"]
    if manifest_counts != {
        "non_manifest_artifacts": 8,
        "catalog_records": 4100,
        "origin_theorems": 500,
        "origin_open_claims": 0,
        "cumulative_theorems": 2500,
        "cumulative_open_claims": 1600,
        "effective_strict_conjecture_credits": 1000,
    }:
        raise RenderError("5.4 manifest counts do not match explicit release rows")
    if not (
        len(catalog_index) == 4100
        and len(theorem_ids) == 2500
        and len(open_ids) == 1600
        and len(strict_ids) == 1000
    ):
        raise RenderError("5.4 release authority cardinalities are stale")

    accepted_digests = manifest["accepted_set_digests"]
    expected_accepted_digests = {
        "source_record_id_set_sha256": _set_digest(
            str(row["source_locator"]["source_record_id"]) for row in new_rows
        ),
        "declaration_set_sha256": _set_digest(
            str(row["formal_statement"]["declaration"]) for row in new_rows
        ),
        "formal_type_sha256_set_sha256": _set_digest(
            str(row["formal_statement"]["formal_type_sha256"]) for row in new_rows
        ),
        "semantic_key_set_sha256": _set_digest(
            str(row["semantic_key"]) for row in new_rows
        ),
        "variant_id_set_sha256": _set_digest(str(row["variant_id"]) for row in new_rows),
        "s5_id_set_sha256": _set_digest(str(row["stage_claim_id"]) for row in new_rows),
    }
    if accepted_digests != expected_accepted_digests:
        raise RenderError("5.4 manifest accepted-set digests are stale")
    return ReleaseBundle(
        release="5.4",
        release_root=release_root,
        manifest_bytes=manifest_bytes,
        manifest=manifest,
        artifact_bindings=bindings,
        catalog=catalog,
        theorem=theorem,
        open_claim=open_claim,
        strict_conjecture=strict,
        catalog_index=catalog_index,
    )


def _load_release(release: str, release_root: Path, manifest_bytes: bytes) -> ReleaseBundle:
    if release == "5.4":
        return _load_release_v5_4(release_root, manifest_bytes)
    if release == "5.3":
        return _load_release_v5_3(release_root, manifest_bytes)
    if release == "5.2":
        return _load_release_v5_2(release_root, manifest_bytes)
    manifest = _strict_json_bytes(manifest_bytes, MANIFEST_NAME)
    bindings = _validate_manifest(release, release_root, manifest)

    catalog = _strict_json_bytes(
        _safe_release_file(release_root, CATALOG_NAME).read_bytes(), CATALOG_NAME
    )
    theorem = _strict_json_bytes(
        _safe_release_file(release_root, THEOREM_JSON_NAME).read_bytes(), THEOREM_JSON_NAME
    )
    open_claim = _strict_json_bytes(
        _safe_release_file(release_root, OPEN_JSON_NAME).read_bytes(), OPEN_JSON_NAME
    )
    catalog_index, _bucket_counts = _validate_catalog(release, catalog)
    theorem_ids = _validate_projection(
        release, THEOREM_JSON_NAME, theorem, catalog_index, "theorem"
    )
    open_ids = _validate_projection(
        release, OPEN_JSON_NAME, open_claim, catalog_index, "open_claim"
    )
    if set(theorem_ids) & set(open_ids):
        raise RenderError("theorem and open-claim projections overlap")

    _validate_artifact_row_count(bindings, CATALOG_NAME, len(catalog_index))
    _validate_artifact_row_count(bindings, THEOREM_JSON_NAME, len(theorem_ids))
    _validate_artifact_row_count(bindings, OPEN_JSON_NAME, len(open_ids))
    return ReleaseBundle(
        release=release,
        release_root=release_root,
        manifest_bytes=manifest_bytes,
        manifest=manifest,
        artifact_bindings=bindings,
        catalog=catalog,
        theorem=theorem,
        open_claim=open_claim,
        strict_conjecture=None,
        catalog_index=catalog_index,
    )


def _flatten_counts(value: Mapping[str, Any], prefix: str) -> Iterator[tuple[str, int]]:
    for key in sorted(value):
        child = value[key]
        qualified = f"{prefix}.{key}"
        if isinstance(child, dict):
            yield from _flatten_counts(child, qualified)
        else:
            yield qualified, _require_nonnegative_int(child, qualified)


def _heading_text(value: str) -> str:
    single_line = " ".join(value.split())
    for character in ("\\", "`", "*", "_", "{", "}", "[", "]", "<", ">", "#"):
        single_line = single_line.replace(character, "\\" + character)
    return single_line


def _one_line(value: str) -> str:
    return " ".join(value.split())


def _inline_code(value: str) -> str:
    if "\n" in value or "\r" in value:
        raise RenderError("inline-code value unexpectedly contains a newline")
    longest = max((len(run) for run in re.findall(r"`+", value)), default=0)
    fence = "`" * max(1, longest + 1)
    padding = " " if value.startswith(("`", " ")) or value.endswith(("`", " ")) else ""
    return f"{fence}{padding}{value}{padding}{fence}"


def _fenced_block(value: str, language: str) -> Iterator[str]:
    longest = max((len(run) for run in re.findall(r"`+", value)), default=0)
    fence = "`" * max(3, longest + 1)
    yield f"{fence}{language}\n"
    yield value
    if not value.endswith("\n"):
        yield "\n"
    yield f"{fence}\n"


def _format_ams(record: Mapping[str, Any]) -> str:
    codes = _require_string_array(record["ams"], "record.ams", nonempty=True)
    return (
        f"primary={_inline_code(record['primary_ams_class'])}; "
        + ", ".join(_inline_code(code) for code in codes)
        + f"; review={_inline_code(record['classification_status'])}"
    )


def _format_locator(locator: Mapping[str, Any]) -> str:
    return (
        f"source={locator['source_id']}; revision={locator['revision']}; "
        f"member={locator['member_path']}; "
        f"file_sha256={locator['file_sha256']}; "
        f"lines={locator['line_start']}-{locator['line_end']}; "
        f"bytes=[{locator['byte_start']},{locator['byte_end_exclusive']}); "
        f"raw_block_sha256={locator['raw_block_sha256']}"
    )


def _all_source_refs(record: Mapping[str, Any]) -> list[str]:
    provenance = _require_object(record["provenance"], "record.provenance")
    status_detail = _require_object(record["status_detail"], "record.status_detail")
    rights = _require_object(record["rights"], "record.rights")
    values = [provenance["formal_source_ref"]]
    values.extend(provenance["source_refs"])
    values.extend(status_detail["source_refs"])
    values.extend(rights["source_refs"])
    return sorted(set(values))


def _iter_record_markdown(record: Mapping[str, Any]) -> Iterator[str]:
    stage_id = record["stage_claim_id"]
    label = record["display_name"]
    formal = _require_object(record["formal_statement"], f"{stage_id}.formal_statement")
    status_detail = _require_object(record["status_detail"], f"{stage_id}.status_detail")
    locator = _require_object(record["locator"], f"{stage_id}.locator")
    rights = _require_object(record["rights"], f"{stage_id}.rights")

    yield f"## {_heading_text(stage_id)} — {_heading_text(label)}\n"
    yield "\n"
    yield f"- S5 ID：{_inline_code(stage_id)}\n"
    yield f"- 标签 / Label：{_heading_text(label)}\n"
    yield (
        "- Lean 完整声明名 / Qualified declaration："
        f"{_inline_code(record['qualified_name'])}\n"
    )
    yield f"- 模块 / Module：{_inline_code(record['module'])}\n"
    yield (
        f"- 类型 / Kind：{_inline_code(record['current_claim_kind'])}; "
        f"Lean {_inline_code(record['declaration_kind'])}\n"
    )
    yield f"- AMS / MSC2020：{_format_ams(record)}\n"
    yield (
        f"- 状态 / Status：{_inline_code(record['material_status'])}，"
        f"截至 / as of {_inline_code(status_detail['status_as_of'])}，"
        f"证据级别 / evidence {_inline_code(status_detail['evidence_level'])}\n"
    )
    yield (
        "- 状态依据 / Status basis："
        f"{_heading_text(_one_line(status_detail['basis']))}\n"
    )
    yield (
        "- 形式化检查 / Formal check："
        f"{_inline_code(record['formal_proof_state'])}; "
        f"sorry_free={_inline_code(json.dumps(formal['sorry_free']))}\n"
    )
    yield f"- 来源定位 / Source locator：{_inline_code(_format_locator(locator))}\n"
    yield (
        "- 来源引用 / Source refs："
        + ", ".join(_inline_code(value) for value in _all_source_refs(record))
        + "\n"
    )
    yield (
        "- 权利 / Rights："
        f"{_inline_code(rights['status'])}; "
        f"formal={_inline_code(rights['formal_code_terms'])}; "
        f"docstring={_inline_code(rights['docstring_terms'])}; "
        f"not_independently_cleared="
        f"{_inline_code(str(rights['not_independently_cleared']).lower())}\n"
    )
    if rights["attribution"]:
        yield (
            "- 归属 / Attribution："
            + "; ".join(_heading_text(_one_line(value)) for value in rights["attribution"])
            + "\n"
        )
    yield "\n"
    yield "### 精确陈述 / Exact statement\n"
    yield "\n"
    yield (
        "#### 源文档字符串 / Source docstring "
        f"(SHA-256 {_inline_code(record['formal_docstring_sha256'])})\n"
    )
    yield "\n"
    yield from _fenced_block(record["formal_docstring"], "text")
    yield "\n"
    yield (
        "#### Lean 声明 / Lean declaration "
        f"(SHA-256 {_inline_code(record['formal_declaration_sha256'])})\n"
    )
    yield "\n"
    yield from _fenced_block(record["formal_declaration"], "lean")
    yield "\n"
    yield (
        "#### 精确声明类型 / Exact declaration type "
        f"(SHA-256 {_inline_code(record['formal_type_sha256'])})\n"
    )
    yield "\n"
    yield from _fenced_block(record["formal_type"], "lean")
    yield "\n"


def _iter_record_markdown_v5_2(record: Mapping[str, Any]) -> Iterator[str]:
    """Render one native OpenConjecture 5.2 record without implying proof review."""

    stage_id = str(record["stage_claim_id"])
    label = str(record["display_name"])
    statement = _require_object(
        record["mathematical_statement"], f"{stage_id}.mathematical_statement"
    )
    status = _require_object(record["status_detail"], f"{stage_id}.status_detail")
    locator = _require_object(record["source_locator"], f"{stage_id}.source_locator")
    paper = _require_object(record["paper"], f"{stage_id}.paper")
    model = _require_object(record["model_label"], f"{stage_id}.model_label")
    classification = _require_object(
        record["classification"], f"{stage_id}.classification"
    )
    rights = _require_object(record["rights"], f"{stage_id}.rights")
    disposition = _require_object(
        record["curator_disposition"], f"{stage_id}.curator_disposition"
    )

    yield f"## {_heading_text(stage_id)} — {_heading_text(label)}\n"
    yield "\n"
    yield f"- S5 ID：{_inline_code(stage_id)}\n"
    yield f"- ATV ID：{_inline_code(str(record['variant_id']))}\n"
    yield f"- 标签 / Label：{_heading_text(label)}\n"
    yield (
        f"- 类型 / Kind：{_inline_code(str(record['current_claim_kind']))}; "
        f"status={_inline_code(str(record['material_status']))}\n"
    )
    yield (
        "- 严格猜想额度 / Strict credit："
        f"{_inline_code(str(disposition['grants_strict_conjecture_credit']).lower())}; "
        f"curation rank={_inline_code(str(disposition['selected_rank']))}\n"
    )
    yield (
        "- 状态证据 / Status evidence："
        f"{_inline_code(str(status['evidence_level']))}; "
        f"independent_current_status_review="
        f"{_inline_code(str(status['independent_current_status_review']).lower())}; "
        f"as_of={_inline_code(str(status['status_as_of']))}\n"
    )
    yield f"- 状态依据 / Status basis：{_heading_text(_one_line(str(status['basis'])))}\n"
    yield (
        "- 来源模型标签 / Source model label："
        f"{_inline_code(str(model['label']))}; "
        f"model={_inline_code(str(model['label_model']))}; "
        f"confidence={_inline_code(str(model['label_confidence']))}\n"
    )
    yield (
        "- 论文 / Paper："
        f"{_heading_text(_one_line(str(paper['title'])))}; "
        f"arXiv={_inline_code(str(paper['arxiv_id']))}\n"
    )
    yield (
        "- 作者 / Authors："
        + "; ".join(
            _heading_text(_one_line(str(author))) for author in paper["authors"]
        )
        + "\n"
    )
    source_categories = [str(value) for value in classification["source_categories"]]
    source_primary = str(classification["source_primary_category"])
    category_text = ", ".join(_inline_code(value) for value in source_categories) or "none"
    yield (
        "- 分类 / Classification："
        f"source primary={_inline_code(source_primary or 'none')}; "
        f"source categories={category_text}; "
        f"MSC={_inline_code(str(classification['msc_status']))}\n"
    )
    yield (
        "- 来源定位 / Source locator："
        f"source={_inline_code(str(record['source_id']))}; "
        f"asset line={_inline_code(str(locator['upstream_line_number']))}; "
        f"eligible-pool line={_inline_code(str(locator['eligible_pool_line_number']))}; "
        f"source file={_inline_code(str(locator['source_file']))}; "
        f"source lines={_inline_code(str(locator['line_start']))}-"
        f"{_inline_code(str(locator['line_end']))}\n"
    )
    yield (
        "- 固定版本 / Pinned revisions："
        f"GitHub={_inline_code(str(locator['github_commit']))}; "
        f"Hugging Face={_inline_code(str(locator['huggingface_commit']))}\n"
    )
    yield (
        "- 权利 / Rights："
        f"{_inline_code(str(rights['spdx_expression']))}; "
        f"mode={_inline_code(str(rights['redistribution_mode']))}; "
        f"catalog_relicenses_source="
        f"{_inline_code(str(rights['catalog_relicenses_source']).lower())}\n"
    )
    yield (
        "- 归属 / Attribution："
        f"{_heading_text(_one_line(str(rights['attribution_title'])))} — "
        + "; ".join(
            _heading_text(_one_line(str(author)))
            for author in rights["attribution_authors"]
        )
        + f" ({_inline_code(str(rights['attribution_arxiv_id']))})\n"
    )
    yield "\n"
    yield "### 精确陈述 / Exact statement\n"
    yield "\n"
    yield (
        "#### 上游纯文本 / Upstream plain text "
        f"(SHA-256 {_inline_code(str(statement['plain_text_sha256']))})\n"
    )
    yield "\n"
    yield from _fenced_block(str(statement["plain_text"]), "text")
    yield "\n"
    yield (
        "#### 原始 LaTeX 猜想块 / Verbatim LaTeX conjecture block "
        f"(SHA-256 {_inline_code(str(statement['body_tex_sha256']))})\n"
    )
    yield "\n"
    yield from _fenced_block(str(statement["body_tex"]), "latex")
    yield "\n"
    yield "### 来源模型说明 / Source-model note\n"
    yield "\n"
    yield f"- 标签理由 / Label rationale：{_heading_text(_one_line(str(model['label_rationale'])))}\n"
    yield f"- 证据片段 / Evidence snippet：{_heading_text(_one_line(str(model['evidence_snippet'])))}\n"
    yield (
        "- 限制 / Limitation：这是一条固定数据集中的模型断言；本仓库没有对该命题"
        "逐条完成截至当前的独立文献状态调查，也没有据此声称证明或反证。\n"
    )
    yield "\n"


def _iter_record_markdown_v5_3(record: Mapping[str, Any]) -> Iterator[str]:
    """Render one native 5.3 mathlib theorem with its exact proof boundary."""

    stage_id = str(record["stage_claim_id"])
    label = str(record["display_name"])
    formal = _require_object(record["formal_statement"], f"{stage_id}.formal_statement")
    statement = _require_object(
        record["mathematical_statement"], f"{stage_id}.mathematical_statement"
    )
    status = _require_object(record["status_detail"], f"{stage_id}.status_detail")
    proof = _require_object(record["proof_evidence"], f"{stage_id}.proof_evidence")
    locator = _require_object(record["source_locator"], f"{stage_id}.source_locator")
    source_range = _require_object(locator["source_range"], f"{stage_id}.source_range")
    selection = _require_object(record["theorem_selection"], f"{stage_id}.theorem_selection")
    classification = _require_object(
        record["classification"], f"{stage_id}.classification"
    )
    importance = _require_object(record["importance"], f"{stage_id}.importance")
    rights = _require_object(record["rights"], f"{stage_id}.rights")
    disposition = _require_object(
        record["curator_disposition"], f"{stage_id}.curator_disposition"
    )

    yield f"## {_heading_text(stage_id)} — {_heading_text(label)}\n"
    yield "\n"
    yield f"- S5 ID：{_inline_code(stage_id)}\n"
    yield f"- ATV ID：{_inline_code(str(record['variant_id']))}\n"
    yield f"- 标签 / Label：{_heading_text(label)}\n"
    yield f"- Lean 声明 / Declaration：{_inline_code(str(formal['declaration']))}\n"
    yield f"- 模块 / Module：{_inline_code(str(formal['module']))}\n"
    yield (
        f"- 类型 / Kind：{_inline_code(str(record['current_claim_kind']))}; "
        f"Lean {_inline_code(str(formal['declaration_kind']))}; "
        f"status={_inline_code(str(record['material_status']))}\n"
    )
    yield (
        "- MSC2020："
        f"{_inline_code(str(classification['msc2020_code']))}; "
        f"status={_inline_code(str(classification['status']))}; "
        f"basis={_inline_code(str(classification['basis']))}; "
        f"module root={_inline_code(str(classification['module_root']))}\n"
    )
    yield (
        "- 证明状态 / Proof state："
        f"{_inline_code(str(proof['formal_proof_state']))}; "
        f"uses_sorry={_inline_code(str(proof['uses_sorry']).lower())}; "
        f"evidence={_inline_code(str(status['evidence_level']))}\n"
    )
    yield (
        "- 固定环境 / Pinned environment："
        f"mathlib={_inline_code(str(proof['mathlib_commit']))}; "
        f"module={_inline_code(str(proof['compiled_module']))}; "
        f"olean_sha256={_inline_code(str(proof['olean_sha256']))}; "
        f"ilean_sha256={_inline_code(str(proof['ilean_sha256']))}\n"
    )
    axiom_union = _require_string_array(
        proof["batch_axiom_dependency_union"], f"{stage_id}.batch_axiom_dependency_union"
    )
    yield (
        "- 公理证据范围 / Axiom evidence scope："
        f"{_inline_code(str(proof['axiom_evidence_scope']))}; batch union="
        + (", ".join(_inline_code(value) for value in axiom_union) or "none")
        + "\n"
    )
    yield (
        "- 证明证据限制 / Proof limitation：`kernel_checked_sorry_free` 绑定固定 commit "
        "的已编译声明；上列公理为 batch union，不冒充逐声明的精确依赖集合，也不外推后续 commit。\n"
    )
    yield (
        "- 选择 / Selection："
        f"{_inline_code(str(selection['selection_phase']))}; "
        f"cohort={_inline_code(str(selection['selection_cohort']))}; "
        f"accepted rank={_inline_code(str(disposition['accepted_rank']))}\n"
    )
    signal_kinds = [
        _inline_code(str(signal.get("kind")))
        for signal in _require_rows(
            selection["importance_signals"], f"{stage_id}.importance_signals"
        )
    ]
    yield (
        "- 重要性信号 / Importance signals："
        + (", ".join(signal_kinds) or "none")
        + f"; independent universal ranking="
        f"{_inline_code(str(importance['independent_universal_ranking_claimed']).lower())}\n"
    )
    yield (
        "- 来源定位 / Source locator："
        f"record={_inline_code(str(locator['source_record_id']))}; "
        f"path={_inline_code(str(locator['source_path']))}; "
        f"lines={_inline_code(str(source_range['line_start']))}-"
        f"{_inline_code(str(source_range['line_end']))}; "
        f"source_sha256={_inline_code(str(locator['source_sha256']))}\n"
    )
    yield f"- 固定源码 URL / Pinned source URL：{_inline_code(str(locator['url']))}\n"
    yield (
        "- 权利 / Rights："
        f"formal={_inline_code(str(rights['formal_code_terms']))}; "
        f"docstring={_inline_code(str(rights['docstring_terms']))}; "
        f"mode={_inline_code(str(rights['redistribution_mode']))}; "
        f"catalog_relicenses_source="
        f"{_inline_code(str(rights['catalog_relicenses_source']).lower())}\n"
    )
    yield (
        "- 归属 / Attribution："
        + "; ".join(_heading_text(_one_line(str(value))) for value in rights["attribution"])
        + "\n"
    )
    yield "\n"
    yield "### 精确陈述 / Exact statement\n"
    yield "\n"
    yield "#### 策展摘要 / Curated summary\n"
    yield "\n"
    yield from _fenced_block(str(statement["natural_language"]), "text")
    yield "\n"
    yield (
        "#### 上游文档字符串 / Source docstring "
        f"(SHA-256 {_inline_code(str(formal['formal_docstring_sha256']))})\n"
    )
    yield "\n"
    yield from _fenced_block(str(formal["formal_docstring"]), "text")
    yield "\n"
    yield (
        "#### 精确 Lean 类型 / Exact Lean type "
        f"(SHA-256 {_inline_code(str(formal['formal_type_sha256']))})\n"
    )
    yield "\n"
    yield from _fenced_block(str(formal["formal_type"]), "lean")
    yield "\n"


def _iter_any_record_markdown(record: Mapping[str, Any]) -> Iterator[str]:
    if record.get("origin_release") in {"5.3", "5.4"}:
        yield from _iter_record_markdown_v5_3(record)
    elif record.get("origin_release") == "5.2":
        yield from _iter_record_markdown_v5_2(record)
    else:
        yield from _iter_record_markdown(record)


def _iter_markdown(
    bundle: ReleaseBundle,
    *,
    projection_name: str,
    document: Mapping[str, Any],
    title_zh: str,
    title_en: str,
) -> Iterator[str]:
    counts = _require_object(document["counts"], f"{projection_name}.counts")
    rows = _require_rows(document["records"], f"{projection_name}.records")
    release_root = bundle.manifest["release_root_sha256"]

    yield f"# {title_zh} / {title_en}\n"
    yield "\n"
    yield (
        "> 由 `render_math_catalog_v5.py` 从不可变 JSON release 生成；请勿手工编辑。  \n"
    )
    yield (
        "> Generated from the immutable JSON release by `render_math_catalog_v5.py`; "
        "do not edit by hand.\n"
    )
    yield "\n"
    yield f"- 发布 / Release：{_inline_code(bundle.release)}\n"
    yield f"- 发布根 / Release root：{_inline_code('sha256:' + release_root)}\n"
    yield f"- 成员投影 / Membership projection：{_inline_code(projection_name)}\n"
    yield (
        "- 检查器口径记录数 / Checker-scope records："
        f"**{counts['records']}**\n"
    )
    yield "\n"
    yield "## 检查器计数 / Checker counts\n"
    yield "\n"
    yield "| Authority | Metric | Count |\n"
    yield "|---|---|---:|\n"
    manifest_counts = _require_object(bundle.manifest["counts"], "manifest.counts")
    for metric, value in _flatten_counts(manifest_counts, "counts"):
        yield f"| `Release_Manifest.json` | `{metric}` | {value} |\n"
    for metric, value in _flatten_counts(counts, "counts"):
        yield f"| `{projection_name}` | `{metric}` | {value} |\n"
    yield "\n"
    yield (
        "> 清单成员完全由 JSON 投影决定；详细字段按 S5 ID 从 "
        "`Claim_Catalog.json` 连接，不在此重新分类。  \n"
    )
    yield (
        "> Membership is defined entirely by the JSON projection. Detailed fields are "
        "joined from `Claim_Catalog.json` by S5 ID and are not reclassified here.\n"
    )
    yield (
        "> 正文仅在 record 声明保留上游条款并允许仓库内再分发时复制；source 状态不等于"
        "逐条独立真值或机器证明复核。  \n"
    )
    yield (
        "> Verbatim text is emitted only when the record preserves upstream terms and "
        "permits in-repository redistribution. Source status is not an independent "
        "truth or proof replay.\n"
    )
    if bundle.release in {"5.2", "5.3", "5.4"} and projection_name == THEOREM_JSON_NAME:
        raw_categories: dict[str, int] = {}
        proof_states: dict[str, int] = {}
        sorry_ax = 0
        for row in rows:
            raw = str(row.get("raw_category"))
            raw_categories[raw] = raw_categories.get(raw, 0) + 1
            proof = str(row.get("formal_proof_state"))
            proof_states[proof] = proof_states.get(proof, 0) + 1
            formal = row.get("formal_statement")
            if isinstance(formal, dict) and "sorryAx" in formal.get("axioms", []):
                sorry_ax += 1
        yield "\n"
        yield f"## {bundle.release} 定理质量边界 / Theorem-quality boundary\n"
        yield "\n"
        yield (
            f"- 固定来源类别 / Pinned source categories："
            f"`research solved`={raw_categories.get('research solved', 0)}; "
            f"`textbook`={raw_categories.get('textbook', 0)}。\n"
        )
        yield (
            f"- 形式证明状态 / Formal-proof state："
            f"`source_asserted_not_replayed`="
            f"{proof_states.get('source_asserted_not_replayed', 0)}; "
            f"records whose imported declaration reports `sorryAx`={sorry_ax}。\n"
        )
        if bundle.release == "5.2":
            yield (
                "- 这 1,500 条是 theorem-status/source-asserted inventory；它们不是 1,500 条"
                "逐条独立人审的重要定理，也不是 1,500 个在本仓库重放通过的无占位符证明。\n"
            )
        else:
            native_rows = [
                row for row in rows if row.get("origin_release") == bundle.release
            ]
            kernel_checked = sum(
                isinstance(row.get("proof_evidence"), dict)
                and row["proof_evidence"].get("formal_proof_state")
                == "kernel_checked_sorry_free"
                and row["proof_evidence"].get("uses_sorry") is False
                for row in native_rows
            )
            if bundle.release == "5.3":
                yield (
                    "- 继承的 1,500 条仍保持上述 source-asserted 质量边界；5.3 没有反向"
                    "抬高它们的证明证据。\n"
                )
            else:
                yield (
                    "- 继承的 1,500 条 source-asserted 记录仍保持原质量边界；另有 500 条"
                    "继承自 5.3 的固定 mathlib 环境 kernel-checked 定理。5.4 没有反向"
                    "抬高任何父记录的证明证据。\n"
                )
            yield (
                f"- {bundle.release} 新增 mathlib literal theorem records={len(native_rows)}；"
                f"`kernel_checked_sorry_free`={kernel_checked}。该证明状态严格绑定记录中的"
                "固定 mathlib commit 与已编译环境。\n"
            )
            if bundle.release == "5.3":
                yield (
                    "- 新 500 条的 importance 来自 mathlib 1000-theorems 或模块 Main-results "
                    "文档信号，不冒充一份独立、普适的数学重要性排名。\n"
                )
            else:
                yield (
                    "- 新 500 条的 importance 来自模块 Main-results 文档信号；"
                    "不冒充一份独立、普适的数学重要性排名。\n"
                )
    if bundle.release in {"5.2", "5.3", "5.4"} and projection_name == OPEN_JSON_NAME:
        kind_counts: dict[str, int] = {}
        for row in rows:
            kind = str(row.get("current_claim_kind"))
            kind_counts[kind] = kind_counts.get(kind, 0) + 1
        yield "\n"
        yield f"## {bundle.release} 开放命题口径 / Open-claim accounting\n"
        yield "\n"
        yield (
            f"- 语法 `conjecture` records：{kind_counts.get('conjecture', 0)}；"
            f"`open_problem` records：{kind_counts.get('open_problem', 0)}。\n"
        )
        yield (
            "- 语法 `conjecture` 数不是严格猜想额度。有效严格猜想由 "
            f"`Strict_Conjecture_Ledger.json` 决定，{bundle.release} 恰为 1,000；"
            "Moving Sofa 旧记录保留但 strict credit 已撤销。\n"
        )
        yield (
            "- 5.2 新增 600 条的 open 状态来自固定 OpenConjecture 数据集/模型标签，"
            "并非本仓库逐条完成的当前文献状态调查。\n"
        )
    yield "\n"
    for projection_row in rows:
        stage_id = projection_row["stage_claim_id"]
        yield from _iter_any_record_markdown(bundle.catalog_index[stage_id])


def _iter_strict_markdown(bundle: ReleaseBundle) -> Iterator[str]:
    document = bundle.strict_conjecture
    if document is None:
        raise RenderError("strict-conjecture rendering requested without a ledger")
    counts = _require_object(document["counts"], f"{STRICT_JSON_NAME}.counts")
    credits = _require_rows(document["strict_credits"], f"{STRICT_JSON_NAME}.strict_credits")
    corrections = _require_rows(
        document["credit_corrections"], f"{STRICT_JSON_NAME}.credit_corrections"
    )
    yield "# Stage5 数学严格猜想清单 / Stage5 Mathematics Strict Conjecture List\n"
    yield "\n"
    yield (
        "> 由 `render_math_catalog_v5.py` 从不可变 JSON release 的严格额度账本生成；"
        "请勿手工编辑。  \n"
    )
    yield (
        "> Generated from the immutable release strict-credit ledger by "
        "`render_math_catalog_v5.py`; do not edit by hand.\n"
    )
    yield "\n"
    yield f"- 发布 / Release：{_inline_code(bundle.release)}\n"
    yield (
        f"- 发布根 / Release root："
        f"{_inline_code('sha256:' + str(bundle.manifest['release_root_sha256']))}\n"
    )
    yield f"- 成员权威 / Membership authority：{_inline_code(STRICT_JSON_NAME)}\n"
    yield (
        "- 有效严格猜想额度 / Effective strict conjecture credits："
        f"**{counts['effective_strict_credits']}**\n"
    )
    yield "\n"
    yield "## 对账 / Reconciliation\n"
    yield "\n"
    yield "| Measure | Count | Meaning |\n"
    yield "|---|---:|---|\n"
    theorem_count = bundle.manifest["counts"]["cumulative_theorems"]
    if bundle.release == "5.3":
        yield (
            f"| theorem-status records | {theorem_count:,} | 1,500 条继承 "
            "source-asserted，加 500 条固定 mathlib 环境 kernel-checked；不属于本清单 |\n"
        )
    elif bundle.release == "5.4":
        yield (
            f"| theorem-status records | {theorem_count:,} | 1,500 条继承 "
            "source-asserted，加 1,000 条固定 mathlib 环境 kernel-checked；不属于本清单 |\n"
        )
    else:
        yield (
            f"| theorem-status records | {theorem_count:,} | "
            "单独的已解决/定理状态库存；不属于本清单 |\n"
        )
    yield "| syntactic `conjecture` records | 1,001 | `current_claim_kind=conjecture` 的原始记录口径 |\n"
    yield "| effective parent strict credits | 400 | 401 条父版本语法猜想减去 1 条撤销 |\n"
    yield "| origin 5.2 strict credits | 600 | 经 5.2 curation 接受的新记录 |\n"
    yield "| **effective strict conjecture credits** | **1,000** | 本文件的精确成员集 |\n"
    yield "| `open_problem` records | 599 | 开放问题，明确不冒充严格猜想 |\n"
    yield "\n"
    yield (
        "> 5.2 新增 600 条的“开放”来自固定 OpenConjecture 数据集中的模型标签。"
        "Curation 审查了命题性、原子性、重要性信号、权利和语义重复，但没有逐条完成"
        "截至当前的独立文献状态调查。  \n"
    )
    yield (
        "> The 600 new open-status assertions come from the pinned OpenConjecture "
        "dataset/model labels. Curation did not independently survey the current "
        "literature status of every item.\n"
    )
    yield "\n"
    yield "## 额度修正 / Credit correction\n"
    yield "\n"
    correction = corrections[0]
    if bundle.release in {"5.3", "5.4"}:
        correction_text = (
            "父记录和数学状态均未被改写；5.2 撤销的严格猜想额度在本 release 中继续继承，"
            "因此它不在下面 1,000 条有效成员中。"
        )
    else:
        correction_text = (
            "父 release 记录和数学状态均未被改写；5.2 只撤销其严格猜想额度，"
            "因此它不在下面 1,000 条有效成员中。"
        )
    yield (
        f"- {_inline_code(str(correction['stage_claim_id']))} / "
        f"{_inline_code(str(correction['variant_id']))} (Moving Sofa)："
        f"{correction_text}\n"
    )
    yield "\n"
    yield "## 精确成员 / Exact members\n"
    yield "\n"
    for credit in credits:
        stage_id = str(credit["stage_claim_id"])
        yield from _iter_any_record_markdown(bundle.catalog_index[stage_id])


def _encoded(chunks: Iterable[str]) -> Iterator[bytes]:
    for chunk in chunks:
        yield chunk.encode("utf-8")


def _stream_equal(path: Path, chunks: Iterable[str]) -> tuple[bool, int | None]:
    if not path.is_file():
        return False, 0
    offset = 0
    with path.open("rb") as current:
        for expected in _encoded(chunks):
            observed = current.read(len(expected))
            if observed != expected:
                mismatch = next(
                    (
                        index
                        for index, (left, right) in enumerate(zip(observed, expected))
                        if left != right
                    ),
                    min(len(observed), len(expected)),
                )
                return False, offset + mismatch
            offset += len(expected)
        if current.read(1):
            return False, offset
    return True, None


def _prepare_atomic(path: Path, chunks: Iterable[str]) -> Path:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            for chunk in _encoded(chunks):
                stream.write(chunk)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, 0o644)
        return temporary
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _assert_release_unchanged(bundle: ReleaseBundle) -> None:
    manifest_path = bundle.release_root / MANIFEST_NAME
    if manifest_path.read_bytes() != bundle.manifest_bytes:
        raise RenderError("release manifest changed while rendering")
    for name, binding in bundle.artifact_bindings.items():
        digest, size = _sha256_file(_safe_release_file(bundle.release_root, name))
        if digest != binding["sha256"] or size != binding["size_bytes"]:
            raise RenderError(f"release artifact changed while rendering: {name}")


def _projection_specs(
    bundle: ReleaseBundle,
) -> tuple[tuple[Path, str, Mapping[str, Any], str, str], ...]:
    output_root = READABLE_DIR / bundle.release
    return (
        (
            output_root / THEOREM_MD_NAME,
            THEOREM_JSON_NAME,
            bundle.theorem,
            "Stage5 数学定理清单",
            "Stage5 Mathematics Theorem List",
        ),
        (
            output_root / OPEN_MD_NAME,
            OPEN_JSON_NAME,
            bundle.open_claim,
            "Stage5 数学开放命题清单",
            "Stage5 Mathematics Open-Claim List",
        ),
    )


def _render_chunks(
    bundle: ReleaseBundle,
    projection_name: str,
    document: Mapping[str, Any],
    title_zh: str,
    title_en: str,
) -> Iterator[str]:
    return _iter_markdown(
        bundle,
        projection_name=projection_name,
        document=document,
        title_zh=title_zh,
        title_en=title_en,
    )


def check_readable_projections(bundle: ReleaseBundle) -> bool:
    all_current = True
    for path, projection_name, document, title_zh, title_en in _projection_specs(bundle):
        current, mismatch = _stream_equal(
            path,
            _render_chunks(bundle, projection_name, document, title_zh, title_en),
        )
        if not current:
            all_current = False
            location = "missing" if not path.exists() else f"first mismatch at byte {mismatch}"
            print(f"STALE {path.relative_to(ROOT)}: {location}", file=sys.stderr)
    if bundle.strict_conjecture is not None:
        strict_path = READABLE_DIR / bundle.release / STRICT_MD_NAME
        current, mismatch = _stream_equal(strict_path, _iter_strict_markdown(bundle))
        if not current:
            all_current = False
            location = (
                "missing" if not strict_path.exists() else f"first mismatch at byte {mismatch}"
            )
            print(f"STALE {strict_path.relative_to(ROOT)}: {location}", file=sys.stderr)
    return all_current


def write_readable_projections(bundle: ReleaseBundle) -> list[Path]:
    specs = _projection_specs(bundle)
    output_root = specs[0][0].parent
    output_root.mkdir(parents=True, exist_ok=True)

    stale: list[tuple[Path, str, Mapping[str, Any], str, str]] = []
    for spec in specs:
        path, projection_name, document, title_zh, title_en = spec
        current, _mismatch = _stream_equal(
            path,
            _render_chunks(bundle, projection_name, document, title_zh, title_en),
        )
        if not current:
            stale.append(spec)
    strict_path = output_root / STRICT_MD_NAME
    strict_stale = False
    if bundle.strict_conjecture is not None:
        strict_current, _strict_mismatch = _stream_equal(
            strict_path, _iter_strict_markdown(bundle)
        )
        strict_stale = not strict_current
    if not stale and not strict_stale:
        return []

    prepared: list[tuple[Path, Path]] = []
    try:
        for path, projection_name, document, title_zh, title_en in stale:
            temporary = _prepare_atomic(
                path,
                _render_chunks(bundle, projection_name, document, title_zh, title_en),
            )
            prepared.append((path, temporary))
        if strict_stale:
            strict_temporary = _prepare_atomic(
                strict_path, _iter_strict_markdown(bundle)
            )
            prepared.append((strict_path, strict_temporary))
        _assert_release_unchanged(bundle)
        for path, temporary in prepared:
            os.replace(temporary, path)
        _fsync_directory(output_root)
    finally:
        for _path, temporary in prepared:
            temporary.unlink(missing_ok=True)
    return [path for path, _temporary in prepared]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--release",
        required=True,
        choices=("5.0", "5.1", "5.2", "5.3", "5.4"),
        help="immutable Stage5 release whose JSON projections should be rendered",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate and compare expected Markdown without writing files",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    release_root = RELEASES_DIR / args.release
    manifest_path = release_root / MANIFEST_NAME
    if not release_root.is_dir():
        raise RenderError(f"release directory is missing: {release_root.relative_to(ROOT)}")
    if not manifest_path.is_file():
        raise RenderError(f"release manifest is missing: {manifest_path.relative_to(ROOT)}")

    with manifest_path.open("rb") as manifest_stream:
        fcntl.flock(
            manifest_stream.fileno(), fcntl.LOCK_SH if args.check else fcntl.LOCK_EX
        )
        manifest_bytes = manifest_stream.read()
        bundle = _load_release(args.release, release_root, manifest_bytes)
        if args.check:
            if not check_readable_projections(bundle):
                return 1
            print(
                f"PASS Stage5 readable projections --release {args.release} "
                f"root={bundle.manifest['release_root_sha256']}"
            )
            return 0

        written = write_readable_projections(bundle)
        if written:
            for path in written:
                print(f"WROTE {path.relative_to(ROOT)}")
        else:
            print(f"CURRENT Stage5 readable projections --release {args.release}")
        return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RenderError) as exc:
        print(f"ERROR render_math_catalog_v5: {exc}", file=sys.stderr)
        raise SystemExit(2)
