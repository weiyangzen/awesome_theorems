#!/usr/bin/env python3
"""Validate and project the Stage1 v2 focus-eligibility receipt.

The blueprint owns policy and checklist state.  A per-target receipt owns only
content-bound facts used to decide which phases may run.  A missing receipt may
bootstrap the three research phases; stale or malformed evidence opens none.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
import tarfile
import io
import shutil
import importlib.util
from typing import Any, Mapping, NoReturn
from urllib.parse import unquote, urlparse

from jsonschema import Draft202012Validator, FormatChecker
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


try:
    import stage1_lean_authority
except ModuleNotFoundError:
    _LEAN_AUTHORITY_PATH = Path(__file__).with_name("stage1_lean_authority.py")
    _LEAN_AUTHORITY_SPEC = importlib.util.spec_from_file_location(
        "stage1_lean_authority", _LEAN_AUTHORITY_PATH
    )
    if _LEAN_AUTHORITY_SPEC is None or _LEAN_AUTHORITY_SPEC.loader is None:
        raise
    stage1_lean_authority = importlib.util.module_from_spec(_LEAN_AUTHORITY_SPEC)
    _LEAN_AUTHORITY_SPEC.loader.exec_module(stage1_lean_authority)


SCHEMA_VERSION = "stage1-focus-eligibility/1.0"
REQUIREMENTS_AUTHORITY = "Docs/Stage1_Blueprint_v2.md"
TARGET_MEMBERSHIP_RELATIVE_PATH = "Docs/Stage1_Target_Membership_v2.json"
TARGET_MEMBERSHIP_SCHEMA = "stage1-target-membership/2.0"
TARGET_MEMBERSHIP_COUNT = 1546
TARGET_MEMBERSHIP_SHA256 = (
    "64a8fcba92d0a32fab0ede8514ed91919e8ea2e273955b9a130747d8f6a3bef8"
)
TARGET_MEMBERSHIP_ID_SET_SHA256 = (
    "e07deabaab3463cc1f92cdf5c0cf50ad9f8270d35554529c375d20a8512d8f1a"
)
SCHEMA_RELATIVE_PATH = "Docs/Stage1_Focus_Eligibility_Schema.json"
TRUST_ANCHORS_RELATIVE_PATH = "Docs/Stage1_Focus_Trust_Anchors.json"
TRUST_ANCHORS_SHA256 = "d482cc8ac1fd0362f9a5c96ddfbc2df5e5b5399b0a50fa5935c17536f874182f"
FOCUS_SCHEMA_SHA256 = "1082484487f994b111f33ab84faa58b1dca842348b802ab3d1ec6209928dad48"
RECEIPT_NAME = "focus-eligibility.json"
THEOREM_RE = re.compile(r"^THM-M-[0-9]{4}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
CHECKLIST_BEGIN = "<!-- STAGE1-EXECUTION-CHECKLIST:BEGIN -->"
CHECKLIST_END = "<!-- STAGE1-EXECUTION-CHECKLIST:END -->"
MASTER_ACCEPTANCE_RECEIPT_SCHEMA = "stage1-master-phase-acceptance/1.0"
PHASES = (
    "intake",
    "statement",
    "anchor_audit",
    "obligation_tree",
    "proof",
    "validation",
    "release",
)
RESEARCH_PHASES = frozenset(PHASES[:3])
FULL_PHASES = frozenset(PHASES)
MACHINE_EVIDENCE_CLASSES = {
    "exact_pinned_closure",
    "exact_external_unintegrated",
    "no_exact_candidate_as_of",
    "unknown",
}
EXECUTION_DISPOSITIONS = {
    "organize_or_integrate",
    "frontier_exception",
    "defer_frontier",
    "research_required",
    "exclude_scope",
}
REQUIRED_INVALIDATIONS = {
    "human_statement_or_source_changes",
    "lean_target_or_fingerprint_changes",
    "machine_source_or_revision_changes",
    "kernel_replay_or_trust_audit_changes",
    "toolchain_or_dependency_lock_changes",
    "license_or_integration_status_changes",
    "eligibility_receipt_expires",
}
REQUIRED_FRONTIER_STOP_CONDITIONS = {
    "lease_expired",
    "any_resource_budget_exhausted",
    "attempt_limit_reached",
    "statement_or_source_mismatch",
    "validator_failure",
    "milestone_deadline_missed",
    "probability_below_threshold",
    "scheduler_revoked",
}
FRONTIER_DEFER_REASONS = {
    "no_current_frontier_exception",
    "frontier_probability_below_threshold",
    "frontier_exception_rejected",
    "frontier_exception_expired",
    "frontier_exception_exhausted",
}
SCOPE_EXCLUSION_REASONS = {
    "human_claim_unproved_or_conjectural",
    "non_exact_umbrella",
    "already_locally_accepted_root",
    "unusable_legal_boundary",
    "unusable_technical_boundary",
}
MAX_FRONTIER_BUDGET = {
    # A frontier exception is an escape hatch, not an unbounded research lane.
    # These are hard per-receipt ceilings; the scheduler may admit less.
    "wall_clock_seconds": 30 * 24 * 60 * 60,
    "token_limit": 50_000_000,
    "compute_seconds": 30 * 24 * 60 * 60,
    "disk_bytes": 1 * 1024**4,
    "concurrency_limit": 100,
}
MAX_FRONTIER_ATTEMPTS = 100
MAX_FRONTIER_LEASE_SECONDS = 30 * 24 * 60 * 60
PROHIBITED_LEAN_TOKENS = re.compile(
    r"(?m)(?:\bsorry\b|\badmit\b|\bsorryAx\b|^\s*axiom\b|^\s*unsafe\b)"
)
AUTHORITY_RESULT_SCHEMA = "stage1-focus-kernel-authority-result/1.0"
LOCAL_TARGET_RESULT_SCHEMA = "stage1-focus-local-target-authority-result/1.0"
TRANSPORT_AUTHORITY_RESULT_SCHEMA = (
    "stage1-focus-machine-transport-authority-result/1.0"
)
TRANSPORT_PROVIDER_MODULE = "Stage1FocusTransportProvider"
TRANSPORT_PROVIDER_SOURCE = f"{TRANSPORT_PROVIDER_MODULE}.lean"
TRANSPORT_PROVIDER_OLEAN = f"{TRANSPORT_PROVIDER_MODULE}.olean"
TRANSPORT_REPLAY_SOURCE = "Stage1FocusMachineTransport.lean"
EXTERNAL_PROVENANCE_SCHEMA = "stage1-external-proof-provenance/1.0"
EXTERNAL_PROVENANCE_ROLE = "pre_stage1_machine_provenance"
FRONTIER_REVIEW_INPUT_SCHEMA = "stage1-frontier-independent-review-input/1.0"
TIMESTAMP_TOKEN_SCHEMA = "stage1-independent-publication-timestamp/1.0"
TIMESTAMP_SIGNATURE_PAYLOAD_SCHEMA = (
    "stage1-independent-publication-timestamp-signature-payload/1.0"
)
STAGE1_PROVENANCE_CUTOFF = datetime(
    2026, 7, 15, 20, 32, 21, tzinfo=timezone.utc
)
EXTERNAL_PROVENANCE_FIELDS = {
    "schema_version", "theorem_id", "source", "publication", "reviewer",
    "reviewed_at", "decision", "provenance_sha256",
}
ISSUANCE_SCHEMA = "stage1-focus-admission-issuance/2.0"
ISSUANCE_AUTHORITY_SCHEMA = "stage1-focus-admission-authority/2.0"
TRUST_ANCHORS_SCHEMA = "stage1-focus-trust-anchors/1.0"
FOUNDATION_PROFILE_ID = "lean4-standard-foundation/1.0"
PERMITTED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
SIGNATURE_ALGORITHM = "Ed25519"


class EligibilityError(RuntimeError):
    """A target is not admitted to the requested phase."""


def _fail(message: str) -> NoReturn:
    raise EligibilityError(message)


def _repo_root(repo_root: Path | str) -> Path:
    raw = Path(repo_root).absolute()
    current = Path(raw.anchor or "/")
    for part in raw.parts[1:]:
        current = current / part
        if current.is_symlink():
            _fail("repository root traverses a symlink")
    if not current.is_dir():
        _fail("repository root is not a directory")
    return current


def receipt_relative_path(theorem_id: str) -> str:
    if not isinstance(theorem_id, str) or not THEOREM_RE.fullmatch(theorem_id):
        _fail("theorem_id is malformed")
    return f"Stage1_Instances/{theorem_id}/{RECEIPT_NAME}"


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _git(
    root: Path, argv: list[str], *, input_bytes: bytes | None = None
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *argv],
        cwd=root,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _git_text(root: Path, argv: list[str], label: str) -> str:
    result = _git(root, argv)
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        _fail(f"{label} cannot be resolved by Git: {detail or 'unknown Git error'}")
    try:
        return result.stdout.decode("ascii", "strict").strip()
    except UnicodeDecodeError as exc:
        raise EligibilityError(f"{label} has a non-ASCII Git identity") from exc


def _resolve_base_revision(root: Path, claimed: Any) -> str:
    if not isinstance(claimed, str) or not re.fullmatch(r"[0-9a-f]{40,64}", claimed):
        _fail("receipt repository base revision is malformed")
    top = _git_text(root, ["rev-parse", "--show-toplevel"], "repository root")
    if Path(top).absolute() != root.absolute():
        _fail("repository root is not the current Git worktree root")
    head = _git_text(root, ["rev-parse", "--verify", "HEAD^{commit}"], "current HEAD")
    revision = _git_text(
        root,
        ["rev-parse", "--verify", f"{claimed}^{{commit}}"],
        "repository base revision",
    )
    if revision != claimed:
        _fail("repository base revision is not a full canonical commit identity")
    ancestor = _git(root, ["merge-base", "--is-ancestor", revision, head])
    if ancestor.returncode != 0:
        _fail("repository base revision is not reachable from current HEAD")
    return revision


def _safe_repository_file(root: Path, relative: str, label: str) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or not pure.parts:
        _fail(f"{label} is not a safe repository-relative path")
    path = root
    for component in pure.parts:
        path = path / component
        if path.is_symlink():
            _fail(f"{label} traverses a symlink: {relative}")
    if not path.is_file():
        _fail(f"{label} is missing or unsafe: {relative}")
    return path


def _git_blob_bytes(root: Path, revision: str, relative: str, label: str) -> bytes:
    tree = _git(root, ["ls-tree", "-z", revision, "--", relative])
    if tree.returncode or not tree.stdout:
        _fail(f"{label} is not tracked at the repository base revision")
    rows = [row for row in tree.stdout.split(b"\0") if row]
    if len(rows) != 1:
        _fail(f"{label} is ambiguous at the repository base revision")
    try:
        metadata, tracked_path = rows[0].split(b"\t", 1)
        mode, object_type, object_id = metadata.decode("ascii").split()
        decoded_path = tracked_path.decode("utf-8")
    except (UnicodeDecodeError, ValueError) as exc:
        raise EligibilityError(f"{label} has malformed Git tree metadata") from exc
    if (
        decoded_path != relative
        or object_type != "blob"
        or mode not in {"100644", "100755"}
        or not re.fullmatch(r"[0-9a-f]{40,64}", object_id)
    ):
        _fail(f"{label} is not a regular tracked blob at the repository base revision")
    blob = _git(root, ["cat-file", "blob", object_id])
    if blob.returncode:
        _fail(f"{label} blob cannot be read at the repository base revision")
    return blob.stdout


def _require_file_at_revision(
    root: Path,
    revision: str,
    relative: str,
    label: str,
    *,
    claimed_sha256: str | None = None,
) -> None:
    path = _safe_repository_file(root, relative, label)
    current = path.read_bytes()
    if claimed_sha256 is not None:
        if not SHA256_RE.fullmatch(claimed_sha256):
            _fail(f"{label} digest is malformed")
        if _sha256_bytes(current) != claimed_sha256:
            _fail(f"{label} digest is stale: {relative}")
    if current != _git_blob_bytes(root, revision, relative, label):
        _fail(f"{label} differs from the repository base revision: {relative}")


def _parse_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        _fail(f"{label} must be a UTC date-time ending in Z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise EligibilityError(f"{label} is not a valid date-time") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        _fail(f"{label} must be UTC")
    return parsed


def _canonical_as_of(as_of: datetime | None) -> datetime:
    if as_of is None:
        return datetime.now(timezone.utc)
    if not isinstance(as_of, datetime) or as_of.tzinfo is None:
        _fail("as_of must be timezone-aware")
    return as_of.astimezone(timezone.utc)


def _actor(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail(f"{label} is missing")
    actor_id = value.get("id")
    role = value.get("role")
    if not isinstance(actor_id, str) or not actor_id or not isinstance(role, str) or not role:
        _fail(f"{label} is malformed")
    return value


def _is_worker_actor(actor: Mapping[str, Any]) -> bool:
    return "worker" in str(actor.get("role", "")).lower()


def _require_distinct_actors(first: Mapping[str, Any], second: Mapping[str, Any], label: str) -> None:
    if first.get("id") == second.get("id"):
        _fail(f"{label} must be independent")


def _safe_bound_file(
    root: Path,
    theorem_id: str,
    row: Mapping[str, Any],
    label: str,
    *,
    base_revision: str,
) -> None:
    raw_path = row.get("path")
    claimed_sha = row.get("sha256")
    if not isinstance(raw_path, str) or not isinstance(claimed_sha, str):
        _fail(f"{label} path or digest is missing")
    pure = PurePosixPath(raw_path)
    owner = PurePosixPath("Stage1_Instances", theorem_id)
    if (
        pure.is_absolute()
        or ".." in pure.parts
        or tuple(pure.parts[:2]) != tuple(owner.parts)
        or not SHA256_RE.fullmatch(claimed_sha)
    ):
        _fail(f"{label} is not a safe theorem-owned binding")
    _require_file_at_revision(
        root,
        base_revision,
        raw_path,
        label,
        claimed_sha256=claimed_sha,
    )


def _embedded_digest(value: Mapping[str, Any], field: str, label: str) -> None:
    claimed = value.get(field)
    if not isinstance(claimed, str) or not SHA256_RE.fullmatch(claimed):
        _fail(f"{label} lacks a canonical {field}")
    unhashed = dict(value)
    del unhashed[field]
    payload = json.dumps(
        unhashed, ensure_ascii=True, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    if _sha256_bytes(payload) != claimed:
        _fail(f"{label} {field} does not bind its content")


def _canonical_git_identity(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        return None
    raw = value.strip()
    if raw.startswith("file://"):
        parsed = urlparse(raw)
        if parsed.netloc not in {"", "localhost"}:
            return None
        raw = unquote(parsed.path)
    if raw.startswith("/") or raw.startswith("./") or raw.startswith("../"):
        try:
            normalized = Path(raw).expanduser().resolve(strict=False).as_posix()
        except OSError:
            return None
        normalized = normalized.rstrip("/")
        return normalized[:-4] if normalized.endswith(".git") else normalized
    scp = re.fullmatch(r"(?:[^@/:]+@)?([^:/]+):(.+)", raw)
    if scp and "://" not in raw:
        host, path = scp.groups()
        normalized = f"{host.lower()}/{path.lstrip('/')}"
    else:
        parsed = urlparse(raw if "://" in raw else f"https://{raw}")
        if not parsed.hostname:
            return None
        port = f":{parsed.port}" if parsed.port else ""
        normalized = f"{parsed.hostname.lower()}{port}/{parsed.path.lstrip('/')}"
    normalized = normalized.rstrip("/")
    return normalized[:-4] if normalized.endswith(".git") else normalized


def _authoritative_repository_identities(root: Path) -> set[str]:
    identities = {_canonical_git_identity(str(root.resolve()))}
    remotes = _git(root, ["remote", "-v"])
    if remotes.returncode == 0:
        for row in remotes.stdout.decode("utf-8", "replace").splitlines():
            fields = row.split()
            if len(fields) >= 2:
                identities.add(_canonical_git_identity(fields[1]))
    return {identity for identity in identities if identity is not None}


def _git_history_identity(
    root: Path, revisions: list[str]
) -> tuple[set[str], set[str]]:
    result = _git(root, ["rev-list", "--objects", *revisions])
    if result.returncode:
        _fail("Git object history cannot be inspected")
    commits: set[str] = set()
    trees: set[str] = set()
    try:
        rows = result.stdout.decode("ascii", "strict").splitlines()
    except UnicodeDecodeError as exc:
        raise EligibilityError("Git object history is not canonical ASCII") from exc
    for row in rows:
        oid = row.split(" ", 1)[0]
        if not re.fullmatch(r"[0-9a-f]{40,64}", oid):
            _fail("Git object history contains a malformed identity")
        kind = _git(root, ["cat-file", "-t", oid])
        if kind.returncode:
            _fail("Git object type cannot be inspected")
        object_type = kind.stdout.decode("ascii", "strict").strip()
        if object_type == "commit":
            commits.add(oid)
        elif object_type == "tree":
            trees.add(oid)
    return commits, trees


def _reject_authoritative_external_identity(
    root: Path,
    repository: Any,
    checkout: Path | None = None,
    *,
    revision: str | None = None,
    source_path: str | None = None,
) -> None:
    authoritative = _authoritative_repository_identities(root)
    candidate = _canonical_git_identity(repository)
    if candidate is None:
        _fail("external source repository identity is not canonical")
    candidates = {candidate}
    if checkout is not None:
        remotes = _git(checkout, ["remote", "-v"])
        if remotes.returncode:
            _fail("external source remotes cannot be inspected")
        for row in remotes.stdout.decode("utf-8", "replace").splitlines():
            fields = row.split()
            if len(fields) >= 2:
                identity = _canonical_git_identity(fields[1])
                if identity is not None:
                    candidates.add(identity)
    if authoritative & candidates:
        _fail(
            "exact external source is the authoritative repository or a remote alias/mirror"
        )
    if checkout is None:
        return
    candidate_revision = revision or _git_text(
        checkout, ["rev-parse", "HEAD^{commit}"], "external source revision"
    )
    if not re.fullmatch(r"[0-9a-f]{40,64}", candidate_revision):
        _fail("external source revision is not a canonical Git object identity")
    authoritative_commits, authoritative_trees = _git_history_identity(root, ["--all"])
    candidate_commits, candidate_trees = _git_history_identity(checkout, [candidate_revision])
    if (authoritative_commits & candidate_commits) or (
        authoritative_trees & candidate_trees
    ):
        _fail(
            "exact external source shares Git commit/history/object identity with "
            "the authoritative repository"
        )
    if source_path is not None:
        pure = PurePosixPath(source_path)
        if pure.is_absolute() or ".." in pure.parts or not pure.parts:
            _fail("external machine source path is unsafe")
        rows = _git(
            checkout,
            ["ls-tree", "-r", candidate_revision, "--", source_path],
        ).stdout.decode("ascii", "strict").splitlines()
        if len(rows) != 1:
            _fail("external machine source object identity cannot be inspected")
        try:
            metadata, tracked = rows[0].split("\t", 1)
            _mode, kind, source_oid = metadata.split()
        except ValueError as exc:
            raise EligibilityError("external machine source tree identity is malformed") from exc
        authoritative_rows = _git(
            root, ["rev-list", "--objects", "--all"]
        ).stdout.decode("ascii", "strict").splitlines()
        authoritative_proof_blobs = {
            row.split(" ", 1)[0]
            for row in authoritative_rows
            if " " in row and row.split(" ", 1)[1].endswith(".lean")
        }
        if tracked != source_path or kind != "blob" or source_oid in authoritative_proof_blobs:
            _fail("external machine proof source blob is part of the authoritative history")


def _validate_machine_pre_stage1_provenance(
    root: Path, receipt: Mapping[str, Any], source: Mapping[str, Any]
) -> None:
    theorem_id = str(receipt.get("theorem_id", ""))
    rows = [
        row for row in receipt.get("evidence_bindings", [])
        if isinstance(row, Mapping) and row.get("role") == EXTERNAL_PROVENANCE_ROLE
    ]
    if len(rows) != 1:
        _fail("exact machine source requires one typed pre-Stage1 provenance report")
    binding = rows[0]
    base = _resolve_base_revision(root, receipt.get("repository_base_revision"))
    _safe_bound_file(
        root, theorem_id, binding, "external proof provenance", base_revision=base
    )
    data = _git_blob_bytes(
        root, base, str(binding.get("path", "")), "external proof provenance"
    )
    report = _strict_json_object(data, "external proof provenance")
    if data != (json.dumps(report, ensure_ascii=True, indent=2, allow_nan=False) + "\n").encode():
        _fail("external proof provenance is not canonical pretty JSON")
    if (
        set(report) != EXTERNAL_PROVENANCE_FIELDS
        or report.get("schema_version") != EXTERNAL_PROVENANCE_SCHEMA
        or report.get("theorem_id") != theorem_id
        or report.get("decision") != "accepted"
    ):
        _fail("external proof provenance fields, schema, or decision are invalid")
    _embedded_digest(report, "provenance_sha256", "external proof provenance")
    reviewer = _actor(report.get("reviewer"), "external proof provenance reviewer")
    if reviewer.get("role") != "independent_reviewer" or _is_worker_actor(reviewer):
        _fail("external proof provenance review is not independent")
    admission_reviewer = _actor(
        receipt.get("admission_review", {}).get("reviewer"), "admission reviewer"
    )
    _require_distinct_actors(reviewer, admission_reviewer, "external proof provenance reviewer")
    publication = report.get("publication")
    if not isinstance(publication, Mapping) or set(publication) != {
        "immutable_id", "timestamp"
    }:
        _fail("external proof provenance publication binding is malformed")
    reviewed_at = _parse_timestamp(report.get("reviewed_at"), "proof provenance reviewed_at")
    evidence_as_of = _parse_timestamp(receipt.get("evidence_as_of"), "evidence_as_of")
    terminal = source.get("terminal_proof_body", {})
    expected_source = {
        "repository": source.get("repository"),
        "revision": source.get("revision"),
        "tree_or_archive_sha256": source.get("tree_or_archive_sha256"),
        "file_path": source.get("file_path"),
        "file_sha256": source.get("file_sha256"),
        "declaration": source.get("declaration"),
        "declaration_type_sha256": source.get("declaration_type_sha256"),
        "terminal_proof_body_sha256": terminal.get("sha256"),
    }
    pointer = source.get("pre_stage1_provenance")
    if (
        report.get("source") != expected_source
        or pointer != {
            "path": binding.get("path"),
            "sha256": binding.get("sha256"),
            "provenance_sha256": report.get("provenance_sha256"),
        }
        or not str(publication.get("immutable_id", "")).strip()
        or reviewed_at > evidence_as_of
    ):
        _fail(
            "external proof provenance is not content-bound, independently reviewed, and pre-Stage1"
        )
    timestamp_subject = {
        "kind": "external_machine_proof",
        "immutable_id": publication["immutable_id"],
        **expected_source,
    }
    author = _actor(receipt.get("admission_review", {}).get("author"), "admission author")
    timestamp = _validate_independent_timestamp(
        root,
        publication.get("timestamp"),
        expected_subject=timestamp_subject,
        cutoff=STAGE1_PROVENANCE_CUTOFF,
        forbidden_principals={
            str(reviewer.get("id")),
            str(admission_reviewer.get("id")),
            str(author.get("id")),
        },
        label="external proof publication timestamp",
    )
    if reviewed_at < _parse_timestamp(
        timestamp["issued_at"], "publication timestamp issued_at"
    ):
        _fail("external proof provenance review predates its independent timestamp")


def _transport_authority_support(
    authority: Mapping[str, Any], label: str
) -> Mapping[str, Any] | None:
    support = authority.get("human_source_review")
    if not isinstance(support, Mapping) or set(support) != {
        "human_source_review",
        "machine_transport_authority",
    }:
        return None
    transport = support.get("machine_transport_authority")
    if not isinstance(transport, Mapping):
        _fail(f"{label} machine transport authority is malformed")
    _embedded_digest(
        transport,
        "transport_verification_sha256",
        f"{label} machine transport authority",
    )
    return transport


def _strict_json_object(payload: bytes, label: str) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                _fail(f"{label} contains duplicate key {key!r}")
            result[key] = value
        return result

    def reject_nonfinite(value: str) -> NoReturn:
        _fail(f"{label} contains non-finite number {value}")

    try:
        value = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=reject_duplicates,
            parse_constant=reject_nonfinite,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EligibilityError(f"{label} is not canonical UTF-8 JSON") from exc
    if not isinstance(value, dict):
        _fail(f"{label} is not a JSON object")
    return value


def _target_membership_ids(root: Path) -> frozenset[str]:
    """Load the exact frozen Stage1 membership from current repository bytes."""

    path = _safe_repository_file(
        root, TARGET_MEMBERSHIP_RELATIVE_PATH, "Stage1 target membership"
    )
    head = _git_text(
        root, ["rev-parse", "--verify", "HEAD^{commit}"], "current HEAD"
    )
    _require_file_at_revision(
        root,
        head,
        TARGET_MEMBERSHIP_RELATIVE_PATH,
        "Stage1 target membership",
    )
    payload = path.read_bytes()
    manifest = _strict_json_object(payload, "Stage1 target membership")
    canonical = (
        json.dumps(manifest, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")
    targets = manifest.get("targets")
    if (
        _sha256_bytes(payload) != TARGET_MEMBERSHIP_SHA256
        or payload != canonical
        or manifest.get("schema_version") != TARGET_MEMBERSHIP_SCHEMA
        or manifest.get("task_state_authority") != REQUIREMENTS_AUTHORITY
        or not isinstance(targets, list)
        or len(targets) != TARGET_MEMBERSHIP_COUNT
    ):
        _fail("Stage1 target membership is malformed or stale")
    theorem_ids = [
        row.get("theorem_id") if isinstance(row, Mapping) else None
        for row in targets
    ]
    if (
        any(
            not isinstance(theorem_id, str)
            or THEOREM_RE.fullmatch(theorem_id) is None
            for theorem_id in theorem_ids
        )
        or len(set(theorem_ids)) != TARGET_MEMBERSHIP_COUNT
    ):
        _fail("Stage1 target membership theorem IDs are malformed or duplicated")
    id_set_sha256 = _sha256_bytes(
        ("\n".join(sorted(theorem_ids)) + "\n").encode("ascii")
    )
    scope = manifest.get("scope")
    if (
        id_set_sha256 != TARGET_MEMBERSHIP_ID_SET_SHA256
        or not isinstance(scope, Mapping)
        or scope.get("covered_targets") != TARGET_MEMBERSHIP_COUNT
        or scope.get("canonical_sorted_target_id_set_sha256") != id_set_sha256
    ):
        _fail("Stage1 target membership ID-set binding is stale")
    return frozenset(theorem_ids)


def _focus_schema(root: Path) -> dict[str, Any]:
    """Load the validator-pinned schema from the exact current HEAD blob."""

    path = _safe_repository_file(root, SCHEMA_RELATIVE_PATH, "focus eligibility schema")
    head = _git_text(
        root, ["rev-parse", "--verify", "HEAD^{commit}"], "current HEAD"
    )
    head_payload = _git_blob_bytes(
        root, head, SCHEMA_RELATIVE_PATH, "focus eligibility schema"
    )
    payload = path.read_bytes()
    if payload != head_payload:
        _fail("focus eligibility schema differs from the current HEAD authority")
    if _sha256_bytes(payload) != FOCUS_SCHEMA_SHA256:
        _fail("focus eligibility schema differs from the validator-pinned contract")
    schema = _strict_json_object(payload, "focus eligibility schema")
    canonical = (
        json.dumps(schema, ensure_ascii=True, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")
    if payload != canonical:
        _fail("focus eligibility schema is not canonical pretty JSON")
    return schema


def require_frozen_target_member(repo_root: Path | str, theorem_id: str) -> None:
    """Reject any theorem outside the sole frozen Stage1 target population."""

    if not isinstance(theorem_id, str) or THEOREM_RE.fullmatch(theorem_id) is None:
        _fail("theorem_id is malformed")
    root = _repo_root(repo_root)
    if (
        not isinstance(theorem_id, str)
        or THEOREM_RE.fullmatch(theorem_id) is None
        or theorem_id not in _target_membership_ids(root)
    ):
        _fail("theorem_id is outside frozen Stage1 target membership")


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _canonical_digest(value: Any, field: str, label: str) -> str:
    if not isinstance(value, Mapping):
        _fail(f"{label} is malformed")
    expected = value.get(field)
    unhashed = dict(value)
    unhashed.pop(field, None)
    observed = _sha256_bytes(_master_canonical_json(unhashed))
    if not isinstance(expected, str) or expected != observed:
        _fail(f"{label} {field} is stale or malformed")
    return expected


def _master_canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _current_release_state(root: Path, theorem_id: str) -> str:
    """Read the unique RELEASE cursor from the current v2 Blueprint SSOT."""

    blueprint = _safe_repository_file(
        root, REQUIREMENTS_AUTHORITY, "Stage1 v2 Blueprint SSOT"
    )
    head = _git_text(root, ["rev-parse", "--verify", "HEAD^{commit}"], "current HEAD")
    _require_file_at_revision(
        root, head, REQUIREMENTS_AUTHORITY, "Stage1 v2 Blueprint SSOT"
    )
    try:
        text = blueprint.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise EligibilityError("Stage1 v2 Blueprint SSOT is unreadable") from exc
    if text.count(CHECKLIST_BEGIN) != 1 or text.count(CHECKLIST_END) != 1:
        _fail("Stage1 v2 Blueprint SSOT lacks one checklist boundary")
    begin = text.index(CHECKLIST_BEGIN) + len(CHECKLIST_BEGIN)
    end = text.index(CHECKLIST_END, begin)
    item_id = f"S56-{theorem_id.removeprefix('THM-')}-RELEASE"
    pattern = re.compile(
        rf"^- (?P<state>\[[_x ]\]) `{re.escape(item_id)}` / "
        rf"`{re.escape(theorem_id)}` / `release`: .+ \{{attempts=\d+\}}$",
        re.MULTILINE,
    )
    matches = list(pattern.finditer(text[begin:end]))
    if len(matches) != 1:
        _fail("Stage1 v2 Blueprint SSOT lacks one canonical target RELEASE row")
    return matches[0]["state"]


def _content_bound_release_decision(
    root: Path, theorem_id: str, receipt: Mapping[str, Any]
) -> Mapping[str, Any]:
    bindings = [
        row
        for row in receipt.get("artifact_bindings", [])
        if isinstance(row, Mapping) and row.get("role") == "release_decision"
    ]
    if len(bindings) != 1:
        _fail("master RELEASE receipt lacks one content-bound release decision")
    binding = bindings[0]
    relative = binding.get("path")
    expected = binding.get("sha256")
    if (
        not isinstance(relative, str)
        or not relative.startswith(f"Stage1_Instances/{theorem_id}/")
        or not isinstance(expected, str)
        or SHA256_RE.fullmatch(expected) is None
    ):
        _fail("master RELEASE decision binding is malformed or outside theorem ownership")
    path = _safe_repository_file(root, relative, "master RELEASE decision")
    head = _git_text(root, ["rev-parse", "--verify", "HEAD^{commit}"], "current HEAD")
    _require_file_at_revision(root, head, relative, "master RELEASE decision")
    payload = path.read_bytes()
    if _sha256_bytes(payload) != expected:
        _fail("master RELEASE decision binding is stale")
    decision = _strict_json_object(payload, "master RELEASE decision")
    if (
        decision.get("theorem_id") != theorem_id
        or decision.get("item_id") != f"S56-{theorem_id.removeprefix('THM-')}-RELEASE"
        or decision.get("verdict") != "accepted"
        or decision.get("remaining_root_cut_set") != []
        or not isinstance(decision.get("terminal_decisions"), Mapping)
        or decision["terminal_decisions"].get("audit_complete") is not True
        or decision["terminal_decisions"].get("theorem_complete") is not True
        or not isinstance(decision.get("root_vector"), Mapping)
        or decision["root_vector"].get("M") not in {"M0-L", "M0-W", "M0-P"}
    ):
        _fail("master RELEASE decision does not prove exact terminal root closure")
    return decision


def _validate_master_release_receipt(
    root: Path, theorem_id: str, path: Path
) -> None:
    payload = path.read_bytes()
    digest = _sha256_bytes(payload)
    if path.name != f"{digest}.json":
        _fail("master RELEASE receipt path is not content-addressed by its bytes")
    relative = path.relative_to(root).as_posix()
    head = _git_text(root, ["rev-parse", "--verify", "HEAD^{commit}"], "current HEAD")
    _require_file_at_revision(root, head, relative, "master RELEASE receipt")
    receipt = _strict_json_object(payload, "master RELEASE receipt")
    if payload != _master_canonical_json(receipt) + b"\n":
        _fail("master RELEASE receipt is not canonical JSON")
    item_id = f"S56-{theorem_id.removeprefix('THM-')}-RELEASE"
    semantic_decision = receipt.get("semantic_decision")
    replay = receipt.get("replay_result")
    semantic_result = replay.get("semantic_result") if isinstance(replay, Mapping) else None
    if not isinstance(semantic_decision, Mapping) or not isinstance(semantic_result, Mapping):
        _fail("master RELEASE receipt lacks semantic acceptance evidence")
    _canonical_digest(semantic_decision, "decision_sha256", "master RELEASE decision")
    _canonical_digest(replay, "result_sha256", "master RELEASE replay")
    if (
        receipt.get("schema_version") != MASTER_ACCEPTANCE_RECEIPT_SCHEMA
        or receipt.get("item_id") != item_id
        or receipt.get("theorem_id") != theorem_id
        or receipt.get("phase") != "release"
        or receipt.get("phase_evidence_accepted") is not True
        or receipt.get("worker_verdict") != "accepted"
        or receipt.get("review_verdict") != "phase_accepted"
        or receipt.get("audit_complete") is not True
        or receipt.get("theorem_complete") is not True
        or semantic_decision.get("decision") != "phase_accepted"
        or semantic_decision.get("phase_evidence_accepted") is not True
        or semantic_decision.get("audit_complete") is not True
        or semantic_decision.get("theorem_complete") is not True
        or receipt.get("semantic_decision_sha256")
        != semantic_decision.get("decision_sha256")
        or receipt.get("replay_result_sha256") != replay.get("result_sha256")
        or semantic_result.get("verdict") != "accepted"
        or semantic_result.get("audit_complete") is not True
        or semantic_result.get("theorem_complete") is not True
        or replay.get("semantic_result_sha256")
        != _sha256_bytes(_master_canonical_json(semantic_result))
    ):
        _fail("master RELEASE receipt does not prove exact terminal root acceptance")
    _content_bound_release_decision(root, theorem_id, receipt)


def current_master_release_acceptance(
    repo_root: Path | str, theorem_id: str
) -> bool:
    """Return current master acceptance, failing closed on an invalid `[x]`."""

    if not isinstance(theorem_id, str) or THEOREM_RE.fullmatch(theorem_id) is None:
        _fail("theorem_id is malformed")
    root = _repo_root(repo_root)
    state = _current_release_state(root, theorem_id)
    if state != "[x]":
        return False
    directory = root / "Stage1_Instances" / theorem_id / "master-acceptance" / "release"
    if directory.is_symlink() or not directory.is_dir():
        _fail("master-accepted RELEASE lacks its content-addressed receipt directory")
    paths = list(directory.iterdir())
    if (
        len(paths) != 1
        or paths[0].is_symlink()
        or not paths[0].is_file()
        or re.fullmatch(r"[0-9a-f]{64}\.json", paths[0].name) is None
    ):
        _fail("master-accepted RELEASE lacks one canonical master receipt")
    _validate_master_release_receipt(root, theorem_id, paths[0])
    return True


def require_integration_root_unaccepted(
    repo_root: Path | str, theorem_id: str
) -> None:
    """Reject ordinary integration once the current SSOT root is accepted."""

    if current_master_release_acceptance(repo_root, theorem_id):
        _fail("already master-accepted root is outside ordinary integration focus")


def _receipt_signature_payload(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Return the complete final receipt except its signature envelope."""
    payload = json.loads(json.dumps(receipt, ensure_ascii=True, allow_nan=False))
    payload["issuance_authority"] = None
    return payload


def _trust_anchor_records(root: Path) -> list[Mapping[str, Any]]:
    path = _safe_repository_file(
        root, TRUST_ANCHORS_RELATIVE_PATH, "focus trust anchors"
    )
    data = path.read_bytes()
    if _sha256_bytes(data) != TRUST_ANCHORS_SHA256:
        _fail("focus trust anchors differ from the validator-pinned trust root")
    anchors = _strict_json_object(data, "focus trust anchors")
    canonical = (
        json.dumps(anchors, ensure_ascii=True, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")
    if (
        data != canonical
        or anchors.get("schema_version") != TRUST_ANCHORS_SCHEMA
        or anchors.get("signature_algorithm") != SIGNATURE_ALGORITHM
        or set(anchors) != {"schema_version", "signature_algorithm", "keys"}
        or not isinstance(anchors.get("keys"), list)
        or not anchors["keys"]
    ):
        _fail("focus trust anchors are malformed")
    records: list[Mapping[str, Any]] = []
    identities: set[str] = set()
    public_keys: set[str] = set()
    active_roles: set[str] = set()
    for record in anchors["keys"]:
        if (
            not isinstance(record, Mapping)
            or set(record) != {
                "key_id", "role", "principal_id", "public_key_hex", "status",
                "not_before", "not_after",
            }
            or record.get("role") not in {
                "scheduler_issuance",
                "independent_review",
                "publication_timestamp",
            }
            or record.get("status") not in {"active", "retired", "revoked"}
            or not isinstance(record.get("key_id"), str)
            or not re.fullmatch(
                r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", record["key_id"]
            )
            or not isinstance(record.get("public_key_hex"), str)
            or not isinstance(record.get("principal_id"), str)
            or not re.fullmatch(
                r"[A-Za-z0-9][A-Za-z0-9._:@-]{0,199}", record["principal_id"]
            )
            or not re.fullmatch(r"[0-9a-f]{64}", record["public_key_hex"])
            or record["key_id"] in identities
            or record["public_key_hex"] in public_keys
        ):
            _fail("focus trust anchor key record is malformed or duplicated")
        not_before = _parse_timestamp(
            record.get("not_before"), "focus trust anchor not_before"
        )
        raw_not_after = record.get("not_after")
        not_after = (
            _parse_timestamp(raw_not_after, "focus trust anchor not_after")
            if raw_not_after is not None
            else None
        )
        if not_after is not None and not_after <= not_before:
            _fail("focus trust anchor validity interval is empty")
        if record["status"] == "retired" and not_after is None:
            _fail("retired focus trust anchor lacks a finite not_after")
        if record["status"] == "active":
            if record["role"] in active_roles or not_after is not None:
                _fail("focus trust anchors do not have one unexpired active key per role")
            active_roles.add(str(record["role"]))
        identities.add(str(record["key_id"]))
        public_keys.add(str(record["public_key_hex"]))
        records.append(record)
    if active_roles != {
        "scheduler_issuance",
        "independent_review",
        "publication_timestamp",
    }:
        _fail("focus trust anchors lack one active key for each authority role")
    return records


def _trust_anchor(
    root: Path,
    role: str,
    *,
    key_id: str | None = None,
    issued_at: datetime | None = None,
    active_only: bool = False,
) -> tuple[str, str, Ed25519PublicKey]:
    matches = [
        record
        for record in _trust_anchor_records(root)
        if record.get("role") == role
        and (key_id is None or record.get("key_id") == key_id)
        and (not active_only or record.get("status") == "active")
    ]
    if len(matches) != 1:
        _fail("focus trust anchor key identity is unknown or ambiguous")
    record = matches[0]
    if record.get("status") == "revoked":
        _fail("focus trust anchor key is revoked")
    if issued_at is not None:
        not_before = _parse_timestamp(
            record.get("not_before"), "focus trust anchor not_before"
        )
        raw_not_after = record.get("not_after")
        not_after = (
            _parse_timestamp(raw_not_after, "focus trust anchor not_after")
            if raw_not_after is not None
            else None
        )
        if issued_at < not_before or (not_after is not None and issued_at >= not_after):
            _fail("focus issuance was signed outside the key validity interval")
    try:
        key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(record["public_key_hex"]))
    except ValueError as exc:
        raise EligibilityError("focus trust anchor public key is invalid") from exc
    return str(record["key_id"]), str(record["principal_id"]), key


def _timestamp_signature_payload(
    *, token_id: str, issued_at: str, subject_sha256: str
) -> bytes:
    return _canonical_json(
        {
            "schema_version": TIMESTAMP_SIGNATURE_PAYLOAD_SCHEMA,
            "token_id": token_id,
            "issued_at": issued_at,
            "subject_sha256": subject_sha256,
        }
    )


def _validate_independent_timestamp(
    root: Path,
    token: Any,
    *,
    expected_subject: Mapping[str, Any],
    cutoff: datetime | None,
    forbidden_principals: set[str],
    label: str,
) -> dict[str, Any]:
    """Verify an externally issued, trust-anchored, content-bound timestamp."""

    fields = {
        "schema_version",
        "token_id",
        "issued_at",
        "subject",
        "subject_sha256",
        "authority",
        "key_id",
        "signature_algorithm",
        "signature",
    }
    if (
        not isinstance(token, Mapping)
        or set(token) != fields
        or token.get("schema_version") != TIMESTAMP_TOKEN_SCHEMA
        or token.get("signature_algorithm") != SIGNATURE_ALGORITHM
    ):
        _fail(f"{label} is malformed")
    token_id = token.get("token_id")
    subject_sha = token.get("subject_sha256")
    signature = token.get("signature")
    if (
        not isinstance(token_id, str)
        or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:@-]{0,199}", token_id)
        or not isinstance(subject_sha, str)
        or not SHA256_RE.fullmatch(subject_sha)
        or not isinstance(signature, str)
        or not re.fullmatch(r"[0-9a-f]{128}", signature)
        or token.get("subject") != dict(expected_subject)
        or _sha256_bytes(_canonical_json(token.get("subject"))) != subject_sha
    ):
        _fail(f"{label} does not bind the exact published bytes")
    issued_at_text = token.get("issued_at")
    issued_at = _parse_timestamp(issued_at_text, f"{label} issued_at")
    if cutoff is not None and issued_at > cutoff:
        _fail(f"{label} was issued after the Stage1 provenance cutoff")
    authority = _actor(token.get("authority"), f"{label} authority")
    if (
        authority.get("role") != "publication_timestamp_authority"
        or authority.get("id") in forbidden_principals
    ):
        _fail(f"{label} authority is not independent")
    key_id, principal_id, public_key = _trust_anchor(
        root,
        "publication_timestamp",
        key_id=str(token.get("key_id", "")),
        issued_at=issued_at,
    )
    if authority.get("id") != principal_id:
        _fail(f"{label} authority is not authorized by its trust anchor")
    signed = _timestamp_signature_payload(
        token_id=token_id,
        issued_at=str(issued_at_text),
        subject_sha256=subject_sha,
    )
    try:
        public_key.verify(bytes.fromhex(signature), signed)
    except (ValueError, InvalidSignature) as exc:
        raise EligibilityError(f"{label} signature is invalid") from exc
    return {
        "token_id": token_id,
        "issued_at": str(issued_at_text),
        "subject_sha256": subject_sha,
        "authority": dict(authority),
        "key_id": key_id,
    }


def _validate_issuance_authority(
    root: Path,
    theorem_id: str,
    receipt: Mapping[str, Any],
    *,
    runtime_root: Path | str | None,
) -> None:
    """Require the durable scheduler issuance embedded in the exact receipt."""

    authority = receipt.get("issuance_authority")
    if not isinstance(authority, Mapping):
        _fail("focus receipt lacks scheduler issuance authority")
    if authority.get("schema_version") != ISSUANCE_AUTHORITY_SCHEMA:
        _fail("focus receipt scheduler issuance authority is stale")
    candidate_sha = authority.get("candidate_sha256")
    if not isinstance(candidate_sha, str) or not SHA256_RE.fullmatch(candidate_sha):
        _fail("focus receipt scheduler candidate identity is malformed")
    issuance = authority.get("issuance")
    if not isinstance(issuance, Mapping):
        _fail("focus receipt is not backed by a durable scheduler issuance")
    expected_fields = {
        "schema_version", "theorem_id", "authority_revision", "candidate_sha256",
        "review_sha256", "proposal_sha256", "receipt_facts_sha256",
        "unsigned_review_sha256",
        "scheduler_issuer", "reviewer", "candidate_verification_sha256",
        "review_verification_sha256", "receipt_path",
        "published_at", "state", "receipt_payload_sha256",
        "scheduler_key_id", "reviewer_key_id", "scheduler_signature",
        "reviewer_signature", "issuance_sha256",
    }
    if set(issuance) != expected_fields or issuance.get("schema_version") != ISSUANCE_SCHEMA:
        _fail("focus issuance fields or schema are not canonical")
    _embedded_digest(issuance, "issuance_sha256", "focus issuance")
    authority_fields = {
        "authority_revision", "candidate_sha256", "proposal_sha256",
        "receipt_facts_sha256", "scheduler_issuer", "review_sha256", "reviewer",
        "unsigned_review_sha256", "candidate_verification_sha256",
        "review_verification_sha256",
    }
    expected_authority = {key: authority.get(key) for key in authority_fields}
    observed_authority = {key: issuance.get(key) for key in authority_fields}
    relative = receipt_relative_path(theorem_id)
    if (
        observed_authority != expected_authority
        or issuance.get("theorem_id") != theorem_id
        or issuance.get("receipt_path") != relative
        or issuance.get("state") != "published"
    ):
        _fail("focus issuance does not authorize the exact current receipt")
    payload = _canonical_json(_receipt_signature_payload(receipt))
    payload_sha = _sha256_bytes(payload)
    if (
        issuance.get("receipt_payload_sha256") != payload_sha
    ):
        _fail("focus issuance does not bind the exact final receipt payload")
    issued_at = _parse_timestamp(issuance.get("published_at"), "focus issuance published_at")
    generated_at = _parse_timestamp(receipt.get("generated_at"), "focus receipt generated_at")
    if issued_at != generated_at:
        _fail("focus issuance published_at differs from receipt generated_at")
    scheduler_key_id, scheduler_principal_id, scheduler_key = _trust_anchor(
        root,
        "scheduler_issuance",
        key_id=issuance.get("scheduler_key_id"),
        issued_at=issued_at,
    )
    reviewer_key_id, reviewer_principal_id, reviewer_key = _trust_anchor(
        root,
        "independent_review",
        key_id=issuance.get("reviewer_key_id"),
        issued_at=issued_at,
    )
    signature_review_sha = authority.get("unsigned_review_sha256")
    if signature_review_sha is None:
        signature_review_sha = authority.get("review_sha256")
    signed = _canonical_json(
        {
            "schema_version": "stage1-focus-admission-signature-payload/1.0",
            "theorem_id": theorem_id,
            "receipt_path": relative,
            "receipt_payload_sha256": payload_sha,
            "authority_revision": authority.get("authority_revision"),
            "candidate_sha256": authority.get("candidate_sha256"),
            "review_sha256": signature_review_sha,
        }
    )
    try:
        if (
            issuance.get("scheduler_key_id") != scheduler_key_id
            or issuance.get("reviewer_key_id") != reviewer_key_id
            or not isinstance(issuance.get("scheduler_signature"), str)
            or not re.fullmatch(r"[0-9a-f]{128}", issuance["scheduler_signature"])
            or not isinstance(issuance.get("reviewer_signature"), str)
            or not re.fullmatch(r"[0-9a-f]{128}", issuance["reviewer_signature"])
        ):
            _fail("focus issuance signatures are missing or name stale keys")
        scheduler_key.verify(bytes.fromhex(issuance["scheduler_signature"]), signed)
        reviewer_key.verify(bytes.fromhex(issuance["reviewer_signature"]), signed)
    except (InvalidSignature, ValueError) as exc:
        raise EligibilityError("focus issuance signature verification failed") from exc
    issuer = _actor(authority.get("scheduler_issuer"), "focus issuance scheduler")
    reviewer = _actor(authority.get("reviewer"), "focus issuance reviewer")
    if (
        issuer.get("role") != "scheduler_master_lane"
        or issuer.get("id") != scheduler_principal_id
    ):
        _fail("focus issuance was not issued by the scheduler master lane")
    if (
        reviewer.get("role") != "independent_reviewer"
        or reviewer.get("id") != reviewer_principal_id
        or _is_worker_actor(reviewer)
    ):
        _fail("focus issuance reviewer is not independent")
    _require_distinct_actors(issuer, reviewer, "focus issuance reviewer")
    authority_revision = authority.get("authority_revision")
    if (
        not isinstance(authority_revision, str)
        or not re.fullmatch(r"[0-9a-f]{40,64}", authority_revision)
        or _git_text(
            root,
            ["rev-parse", "--verify", f"{authority_revision}^{{commit}}"],
            "focus issuance authority revision",
        )
        != authority_revision
        or _git(
            root,
            [
                "merge-base",
                "--is-ancestor",
                str(receipt.get("repository_base_revision")),
                authority_revision,
            ],
        ).returncode
    ):
        _fail("focus issuance authority revision does not descend from the receipt base")
    review = receipt.get("admission_review", {})
    if review.get("author") != issuer or review.get("reviewer") != reviewer:
        _fail("focus receipt review principals differ from scheduler issuance")


def _dependency_identity(checkout: Path) -> tuple[str, str]:
    toolchain_path = checkout / "lean-toolchain"
    if not toolchain_path.is_file() or toolchain_path.is_symlink():
        _fail("Lean authority snapshot lacks a regular pinned lean-toolchain")
    toolchain = toolchain_path.read_text(encoding="utf-8").strip()
    lock = checkout / "lake-manifest.json"
    dependency = lock if lock.is_file() and not lock.is_symlink() else toolchain_path
    return toolchain, _sha256_bytes(dependency.read_bytes())


def _pinned_manifest_provider(
    root: Path,
    authority_revision: str,
    source: Mapping[str, Any],
) -> dict[str, str]:
    relative = "Formalizations/Lean/lake-manifest.json"
    data = _git_blob_bytes(root, authority_revision, relative, "repository Lake manifest")
    manifest = _strict_json_object(data, "repository Lake manifest")
    packages = manifest.get("packages")
    if not isinstance(packages, list):
        _fail("repository Lake manifest package list is malformed")

    def canonical_remote(value: Any) -> str | None:
        if not isinstance(value, str) or not value:
            return None
        normalized = value.rstrip("/")
        return normalized[:-4] if normalized.endswith(".git") else normalized

    remote = canonical_remote(source.get("repository"))
    revision = source.get("revision")
    matches = [
        row for row in packages
        if isinstance(row, Mapping)
        and canonical_remote(row.get("url")) == remote
        and row.get("rev") == revision
    ]
    if len(matches) != 1:
        _fail(
            "exact pinned closure source repository/revision is absent or ambiguous "
            "in the authoritative Lake manifest"
        )
    row = matches[0]
    if (
        set(row)
        != {
            "url",
            "type",
            "subDir",
            "scope",
            "rev",
            "name",
            "manifestFile",
            "inputRev",
            "inherited",
            "configFile",
        }
        or row.get("type") != "git"
        or row.get("subDir") is not None
        or row.get("manifestFile") != "lake-manifest.json"
        or row.get("configFile") not in {"lakefile.lean", "lakefile.toml"}
    ):
        _fail("pinned Lake provider manifest record is not a canonical Git package")
    raw_name = row.get("name")
    if not isinstance(raw_name, str) or not raw_name:
        _fail("pinned Lake provider has no canonical package name")
    cache_name = (
        raw_name[1:-1]
        if raw_name.startswith("«") and raw_name.endswith("»")
        else raw_name
    )
    if re.fullmatch(r"[A-Za-z0-9_.-]+", cache_name) is None:
        _fail("pinned Lake provider cache name is unsafe")
    return {
        "package_name": raw_name,
        "cache_name": cache_name,
        "repository": str(source.get("repository")),
        "revision": str(revision),
        "manifest_sha256": _sha256_bytes(data),
    }


def _require_root_lake_declaration(
    root: Path, authority_revision: str, provider: Mapping[str, str]
) -> None:
    relative = "Formalizations/Lean/lakefile.lean"
    data = _git_blob_bytes(root, authority_revision, relative, "repository Lakefile")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise EligibilityError("repository Lakefile is not UTF-8") from exc
    declaration = re.compile(
        rf"(?m)^require[ \t]+{re.escape(provider['package_name'])}[ \t]+from[ \t]+git[ \t]*\n"
        rf"[ \t]+\"{re.escape(provider['repository'])}\"[ \t]+@[ \t]+"
        rf"\"{re.escape(provider['revision'])}\"[ \t]*$"
    )
    if len(declaration.findall(text)) != 1:
        _fail("pinned provider is not declared exactly in the tracked root Lakefile")


def _canonical_kernel_command(command: Any, *, file_path: str) -> list[str]:
    if (
        not isinstance(command, list)
        or any(not isinstance(part, str) or not part or "\x00" in part for part in command)
    ):
        _fail("external authority command is malformed")
    executable = Path(command[0]).name if command else ""
    if executable == "lean" and command == ["lean", file_path]:
        return list(command)
    if executable == "lake" and command == ["lake", "env", "lean", file_path]:
        return list(command)
    _fail("external authority command is not the canonical Lean compilation of the bound source")


def _readonly_lean(
    checkout: Path,
    command: list[str],
    *,
    timeout: int = 3600,
    lean_path: Path | None = None,
    writable: bool = False,
    writable_path: Path | None = None,
) -> subprocess.CompletedProcess[bytes]:
    bwrap = Path("/usr/bin/bwrap")
    if not bwrap.is_file():
        _fail("bubblewrap is required for focus authority replay")
    executable_name = Path(command[0]).name
    if executable_name not in {"lean", "lake"} or command[0] != executable_name:
        _fail("focus authority replay executable is not canonical")
    toolchain_file = checkout / "lean-toolchain"
    if toolchain_file.is_symlink() or not toolchain_file.is_file():
        _fail("focus replay lacks a regular pinned lean-toolchain")
    toolchain_name = toolchain_file.read_text(encoding="utf-8").strip()
    match = re.fullmatch(r"leanprover/lean4:v([0-9]+\.[0-9]+\.[0-9]+)", toolchain_name)
    if match is None:
        _fail("focus replay Lean toolchain pin is noncanonical")
    tool_root = Path.home() / ".elan" / "toolchains" / (
        "leanprover--lean4---v" + match.group(1)
    )
    executable_path = tool_root / "bin" / executable_name
    if executable_path.is_symlink() or not executable_path.is_file():
        _fail("pinned Lean toolchain executable is unavailable")
    expected_binary_sha = hashlib.sha256(executable_path.read_bytes()).hexdigest()
    args = [
        str(bwrap), "--die-with-parent", "--new-session", "--unshare-all",
        "--tmpfs", "/",
    ]
    for host in (Path("/usr"), Path("/lib"), Path("/lib64")):
        if host.exists():
            args += ["--dir", host.as_posix(), "--ro-bind", host.as_posix(), host.as_posix()]
    args += ["--symlink", "usr/bin", "/bin", "--proc", "/proc", "--dev", "/dev"]
    current = Path("/")
    for component in tool_root.parts[1:]:
        current /= component
        args += ["--dir", current.as_posix()]
    args += ["--ro-bind", tool_root.as_posix(), tool_root.as_posix()]
    path_value = f"{tool_root / 'bin'}:/usr/bin:/bin"
    args += ["--dir", "/repo"]
    if writable and writable_path is not None:
        _fail("focus replay writable boundary is ambiguous")
    args += ["--bind" if writable else "--ro-bind", checkout.as_posix(), "/repo"]
    if writable_path is not None:
        try:
            relative_writable = writable_path.resolve().relative_to(checkout.resolve())
        except (OSError, ValueError) as exc:
            raise EligibilityError("focus replay writable path escapes its checkout") from exc
        if relative_writable == Path(".") or not writable_path.is_dir() or writable_path.is_symlink():
            _fail("focus replay writable path is unsafe")
        args += [
            "--bind", writable_path.as_posix(),
            (Path("/repo") / relative_writable).as_posix(),
        ]
    args += [
        "--dir", "/scratch", "--tmpfs", "/tmp", "--chdir", "/repo",
        "--clearenv", "--setenv", "PATH", path_value,
        "--setenv", "HOME", "/scratch", "--setenv", "ELAN_HOME", "/scratch/.elan",
        "--setenv", "TMPDIR", "/tmp",
    ]
    if lean_path is not None:
        try:
            relative_lean_path = lean_path.resolve().relative_to(checkout.resolve())
        except (OSError, ValueError) as exc:
            raise EligibilityError("Lean replay import path escapes its checkout") from exc
        args += ["--setenv", "LEAN_PATH", (Path("/repo") / relative_lean_path).as_posix()]
    args += ["--", executable_path.as_posix(), *command[1:]]
    try:
        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=timeout, check=False)
        if hashlib.sha256(executable_path.read_bytes()).hexdigest() != expected_binary_sha:
            _fail("pinned Lean executable changed during replay")
        return result
    except subprocess.TimeoutExpired as exc:
        raise EligibilityError("focus authority replay timed out") from exc


def _lean_probe(checkout: Path, source: bytes, declaration: str) -> tuple[str, list[str], str]:
    probe = checkout / "Stage1FocusEligibilityProbe.lean"
    if probe.exists() or probe.is_symlink():
        _fail("focus target conflicts with authority probe path")
    probe.write_bytes(
        source + (b"" if source.endswith(b"\n") else b"\n")
        + f"#check {declaration}\n#print axioms {declaration}\n".encode()
    )
    try:
        command = ["lake", "env", "lean", probe.name] if (
            (checkout / "lakefile.lean").is_file() or (checkout / "lakefile.toml").is_file()
        ) else ["lean", probe.name]
        result = _readonly_lean(checkout, command)
    finally:
        probe.unlink(missing_ok=True)
    if result.returncode:
        _fail("focus declaration/type/trust authority probe failed")
    output = result.stdout.decode("utf-8", "strict")
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    rows = [line for line in lines if line.startswith(f"{declaration} :")]
    if len(rows) != 1:
        _fail("focus authority probe did not identify one declaration type")
    type_text = " ".join(rows[0].split(":", 1)[1].split())
    no_axiom = re.compile(rf"^['\"]?{re.escape(declaration)}['\"]? does not depend on any axioms$")
    with_axiom = re.compile(rf"^['\"]?{re.escape(declaration)}['\"]? depends on axioms: (\[.*\])$")
    none_rows = [line for line in lines if no_axiom.fullmatch(line)]
    axiom_rows = [m for line in lines if (m := with_axiom.fullmatch(line))]
    if len(none_rows) + len(axiom_rows) != 1:
        _fail("focus authority probe did not report the axiom closure")
    axioms: list[str] = []
    if axiom_rows:
        raw = axiom_rows[0].group(1)
        axioms = sorted(v.strip().strip("'\"") for v in raw[1:-1].split(",") if v.strip())
    return _sha256_bytes(type_text.encode()), axioms, _sha256_bytes(result.stdout)


def _lean_import_probe(
    checkout: Path, package: Path, module: str, declaration: str
) -> tuple[str, list[str], str]:
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*", module) is None:
        _fail("pinned provider module is not a canonical Lean module name")
    try:
        package.relative_to(checkout)
    except ValueError as exc:
        raise EligibilityError("pinned provider package escapes the Lean closure") from exc
    probe = package / "Stage1FocusPinnedProviderProbe.lean"
    if probe.exists() or probe.is_symlink():
        _fail("local Lean closure conflicts with the pinned provider probe path")
    probe.write_text(
        f"import {module}\n#check {declaration}\n#print axioms {declaration}\n",
        encoding="utf-8",
    )
    try:
        result = _readonly_lean(
            package,
            ["lake", "env", "lean", probe.name],
        )
    finally:
        probe.unlink(missing_ok=True)
    if result.returncode:
        _fail("local pinned provider Lake import probe failed")
    output = result.stdout.decode("utf-8", "strict")
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    rows = [line for line in lines if line.startswith(f"{declaration} ")]
    if len(rows) != 1:
        _fail("local pinned provider import did not identify one declaration type")
    declaration_tail = rows[0][len(declaration) :].strip()
    colon = declaration_tail.rfind(":")
    if colon < 0:
        _fail("local pinned provider import produced a malformed declaration type")
    type_text = " ".join(declaration_tail[colon + 1 :].split())
    no_axiom = re.compile(
        rf"^['\"]?{re.escape(declaration)}['\"]? does not depend on any axioms$"
    )
    with_axiom = re.compile(
        rf"^['\"]?{re.escape(declaration)}['\"]? depends on axioms: (\[.*\])$"
    )
    none_rows = [line for line in lines if no_axiom.fullmatch(line)]
    axiom_rows = [match for line in lines if (match := with_axiom.fullmatch(line))]
    if len(none_rows) + len(axiom_rows) != 1:
        _fail("local pinned provider import did not report the axiom closure")
    axioms: list[str] = []
    if axiom_rows:
        raw = axiom_rows[0].group(1)
        axioms = sorted(
            value.strip().strip("'\"")
            for value in raw[1:-1].split(",")
            if value.strip()
        )
    return _sha256_bytes(type_text.encode()), axioms, _sha256_bytes(result.stdout)


def _fresh_root_provider_replay(
    lean_root: Path, source_path: Path, module: str, declaration: str
) -> tuple[str, list[str]]:
    """Compile exact source afresh, then probe only that fresh root-bound module."""

    with tempfile.TemporaryDirectory(
        prefix=".stage1-focus-provider-", dir=lean_root
    ) as directory:
        replay_root = Path(directory)
        module_path = PurePosixPath(*module.split("."))
        olean_path = replay_root / module_path.with_suffix(".olean")
        probe_path = replay_root / "Stage1FocusPinnedProviderProbe.lean"
        olean_path.parent.mkdir(parents=True, exist_ok=True)
        replay = _readonly_lean(
            lean_root,
            [
                "lake", "env", "lean", "-o",
                olean_path.relative_to(lean_root).as_posix(),
                source_path.relative_to(lean_root).as_posix(),
            ],
            writable_path=replay_root,
        )
        if replay.returncode or not olean_path.is_file():
            _fail("local pinned provider Lake replay failed")
        probe_path.write_text(
            f"import {module}\n"
            f"#check {declaration}\n#print axioms {declaration}\n",
            encoding="utf-8",
        )
        probe = _readonly_lean(
            lean_root,
            ["lake", "env", "lean", probe_path.relative_to(lean_root).as_posix()],
            lean_path=replay_root,
        )
        if probe.returncode:
            _fail("local pinned provider Lake import probe failed")
        output = probe.stdout.decode("utf-8", "strict")
        lines = [line.strip() for line in output.splitlines() if line.strip()]
        rows = [line for line in lines if line.startswith(f"{declaration} ")]
        if len(rows) != 1:
            _fail("local pinned provider import did not identify one declaration type")
        tail = rows[0][len(declaration) :].strip()
        colon = tail.rfind(":")
        if colon < 0:
            _fail("local pinned provider import produced a malformed declaration type")
        type_text = " ".join(tail[colon + 1 :].split())
        no_axiom = re.compile(
            rf"^['\"]?{re.escape(declaration)}['\"]? does not depend on any axioms$"
        )
        with_axiom = re.compile(
            rf"^['\"]?{re.escape(declaration)}['\"]? depends on axioms: (\[.*\])$"
        )
        none_rows = [line for line in lines if no_axiom.fullmatch(line)]
        axiom_rows = [match for line in lines if (match := with_axiom.fullmatch(line))]
        if len(none_rows) + len(axiom_rows) != 1:
            _fail("local pinned provider import did not report the axiom closure")
        axioms: list[str] = []
        if axiom_rows:
            raw = axiom_rows[0].group(1)
            axioms = sorted(
                value.strip().strip("'\"")
                for value in raw[1:-1].split(",")
                if value.strip()
            )
        return _sha256_bytes(type_text.encode()), axioms


def _materialize_revision(root: Path, revision: str, destination: Path) -> None:
    archive = _git(root, ["archive", "--format=tar", revision]).stdout
    try:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as stream:
            for member in stream.getmembers():
                pure = PurePosixPath(member.name)
                if pure.is_absolute() or ".." in pure.parts or member.issym() or member.islnk():
                    _fail("repository archive contains an unsafe entry")
            stream.extractall(destination, filter="data")
    except (tarfile.TarError, OSError) as exc:
        raise EligibilityError("repository snapshot cannot be materialized") from exc


def _verify_local_pinned_provider(
    root: Path,
    authority_revision: str,
    source: Mapping[str, Any],
    provider: Mapping[str, str],
) -> None:
    lean_root = root / "Formalizations" / "Lean"
    manifest = lean_root / "lake-manifest.json"
    if manifest.is_symlink() or not manifest.is_file():
        _fail("scheduler-owned Lake manifest is absent or unsafe")
    if _sha256_bytes(manifest.read_bytes()) != provider.get("manifest_sha256"):
        _fail("live scheduler-owned Lake manifest differs from the authority revision")
    _require_root_lake_declaration(root, authority_revision, provider)
    packages = lean_root / ".lake" / "packages"
    package = packages / provider["cache_name"]
    if packages.is_symlink() or not packages.is_dir() or package.is_symlink() or not package.is_dir():
        _fail("pinned provider package is absent from the scheduler-owned Lake closure")
    if _git_text(
        package, ["rev-parse", "--is-inside-work-tree"], "local pinned provider"
    ) != "true":
        _fail("local pinned provider is not a Git worktree")
    remote_result = _git(package, ["remote", "-v"])
    if remote_result.returncode:
        _fail("local pinned provider remotes cannot be inspected")
    remotes = remote_result.stdout.decode("utf-8", "strict").splitlines()
    fetch_urls = []
    for row in remotes:
        fields = row.split()
        if len(fields) == 3 and fields[2] == "(fetch)":
            fetch_urls.append(fields[1])

    def canonical_remote(value: Any) -> str | None:
        if not isinstance(value, str) or not value or "\x00" in value:
            return None
        normalized = value.rstrip("/")
        return normalized[:-4] if normalized.endswith(".git") else normalized

    expected_remote = canonical_remote(provider.get("repository"))
    if (
        expected_remote is None
        or len(fetch_urls) != 1
        or canonical_remote(fetch_urls[0]) != expected_remote
    ):
        _fail("local pinned provider origin URL disagrees with the Lake manifest")
    revision = _git_text(
        package,
        ["rev-parse", "--verify", "HEAD^{commit}"],
        "local pinned provider revision",
    )
    if revision != provider["revision"]:
        _fail("local pinned provider revision disagrees with the Lake manifest")
    if _git(package, ["status", "--porcelain", "--untracked-files=all"]).stdout:
        _fail("local pinned provider is not a clean exact checkout")
    file_path = str(source.get("file_path", ""))
    pure_path = PurePosixPath(file_path)
    if pure_path.is_absolute() or not pure_path.parts or any(
        part in {"", ".", ".."} for part in pure_path.parts
    ):
        _fail("pinned provider source path is unsafe")
    source_path = package
    for component in pure_path.parts:
        source_path /= component
        if source_path.is_symlink():
            _fail("pinned provider source path traverses a symlink")
    if not source_path.is_file():
        _fail("pinned provider source is absent from its manifest package")
    data = source_path.read_bytes()
    if _sha256_bytes(data) != source.get("file_sha256"):
        _fail("local pinned provider source differs from the admitted proof")
    declaration = str(source.get("declaration", ""))
    body_sha = _declaration_region(data, declaration)
    terminal = source.get("terminal_proof_body", {})
    if terminal.get("locator") != declaration or terminal.get("sha256") != body_sha:
        _fail("local pinned provider proof body differs from the admitted proof")
    if PROHIBITED_LEAN_TOKENS.search(data.decode("utf-8", "replace")):
        _fail("local pinned provider source contains a prohibited construct")
    # Compile the exact provider source through the repository's manifest-bound
    # closure, not through a separate provider-local dependency cache.
    type_sha, axioms = _fresh_root_provider_replay(
        lean_root, source_path, str(source.get("module", "")), declaration
    )
    if type_sha != source.get("declaration_type_sha256"):
        _fail("local pinned provider declaration type differs from the admitted proof")
    claimed_axioms = source.get("trust_audit", {}).get("permitted_axioms", [])
    if set(claimed_axioms) - PERMITTED_AXIOMS:
        _fail("local pinned provider claims axioms outside the foundation policy")
    if set(axioms) - PERMITTED_AXIOMS:
        _fail("local pinned provider uses axioms outside the foundation policy")
    if sorted(claimed_axioms) != sorted(axioms):
        _fail("local pinned provider axiom inventory is not exact")


def _declaration_region(data: bytes, declaration: str) -> str:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise EligibilityError("external Lean source is not UTF-8") from exc
    short = declaration.rsplit(".", 1)[-1]
    start = re.search(
        rf"(?m)^\s*(?:theorem|lemma|opaque|def)\s+{re.escape(short)}\b", text
    )
    if start is None:
        _fail("external source does not contain the admitted declaration")
    tail = text[start.start():]
    next_decl = re.search(
        r"(?m)^\s*(?:theorem|lemma|opaque|def|namespace|end)\s+",
        tail[start.end() - start.start():],
    )
    end = len(tail) if next_decl is None else (
        start.end() - start.start() + next_decl.start()
    )
    return _sha256_bytes(tail[:end].encode("utf-8"))


def _lean_name_literal(name: str, label: str) -> str:
    if (
        not isinstance(name, str)
        or not name
        or any(character in name for character in ("\x00", "`", "\n", "\r"))
    ):
        _fail(f"{label} is not a canonical Lean declaration name")
    return "`" + name


def _transport_replay_source(
    artifact_bytes: bytes,
    *,
    target_declaration: str,
    provider_declaration: str,
) -> bytes:
    target_name = _lean_name_literal(target_declaration, "transport target declaration")
    provider_name = _lean_name_literal(
        provider_declaration, "transport provider declaration"
    )
    return (
        f"import Lean\nimport {TRANSPORT_PROVIDER_MODULE}\n".encode("utf-8")
        + artifact_bytes
        + (b"" if artifact_bytes.endswith(b"\n") else b"\n")
        + f'''\n
open Lean Elab Command in
elab "#stage1_verify_transport_provider_dependency" : command => liftTermElabM do
  let targetInfo ← getConstInfo {target_name}
  let targetValue ← match targetInfo.value? (allowOpaque := true) with
    | some value => pure value
    | none => throwError "transport target declaration has no inspectable proof body"
  if !targetValue.getUsedConstantsAsSet.contains {provider_name} then
    throwError "transport target proof body does not directly depend on provider declaration"

#stage1_verify_transport_provider_dependency
'''.encode("utf-8")
    )


def _replay_external_authority(
    source: Mapping[str, Any], *, authoritative_root: Path | None = None
) -> dict[str, Any]:
    repository = source.get("repository")
    revision = source.get("revision")
    if (
        not isinstance(repository, str) or not repository or "\x00" in repository
        or not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40,64}", revision)
    ):
        _fail("external authority source is not an immutable repository revision")
    file_path = str(source.get("file_path", ""))
    pure_path = PurePosixPath(file_path)
    if pure_path.is_absolute() or ".." in pure_path.parts or not pure_path.parts:
        _fail("external authority source path is unsafe")
    declaration = source.get("declaration")
    if not isinstance(declaration, str) or not declaration:
        _fail("external authority declaration is missing")
    command = _canonical_kernel_command(
        source.get("kernel_replay", {}).get("command"), file_path=file_path
    )
    with tempfile.TemporaryDirectory(prefix="stage1-focus-external-") as directory:
        checkout = Path(directory) / "source"
        clone = subprocess.run(
            ["git", "clone", "--no-checkout", "--", repository, str(checkout)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        if clone.returncode:
            _fail("external immutable source cannot be cloned for authority replay")
        resolved = _git_text(checkout, ["rev-parse", "--verify", f"{revision}^{{commit}}"],
                             "external source revision")
        if resolved != revision:
            _fail("external source revision is not a full canonical commit")
        if authoritative_root is not None:
            _reject_authoritative_external_identity(
                authoritative_root,
                repository,
                checkout,
                revision=resolved,
                source_path=file_path,
            )
        checkout_result = _git(checkout, ["checkout", "--detach", revision])
        if checkout_result.returncode:
            _fail("external immutable source cannot be checked out")
        archive = _git(checkout, ["archive", "--format=tar", revision]).stdout
        tree = _git_text(checkout, ["rev-parse", f"{revision}^{{tree}}"], "external tree")
        archive_sha = _sha256_bytes(archive)
        identity = source.get("tree_or_archive_sha256")
        if identity not in {archive_sha, _sha256_bytes(tree.encode("ascii"))}:
            _fail("external source tree/archive digest is stale")
        path = checkout / file_path
        current = checkout
        for component in pure_path.parts:
            current /= component
            if current.is_symlink():
                _fail("external source path traverses a symlink")
        if not path.is_file():
            _fail("external source file is missing")
        data = path.read_bytes()
        file_sha = _sha256_bytes(data)
        body_sha = _declaration_region(data, declaration)
        if file_sha != source.get("file_sha256"):
            _fail("external source file digest is stale")
        terminal = source.get("terminal_proof_body", {})
        if terminal.get("locator") != declaration or terminal.get("sha256") != body_sha:
            _fail("external terminal proof body identity is stale")
        if PROHIBITED_LEAN_TOKENS.search(data.decode("utf-8", "replace")):
            _fail("external proof source contains a prohibited construct")
        toolchain, dependency_sha = _dependency_identity(checkout)
        try:
            replay_authority, _external_toolchain, _external_cache = (
                stage1_lean_authority.build_project_lean_authority(checkout)
            )
        except Exception as exc:
            raise EligibilityError(
                f"external pinned Lean replay authority is invalid: {exc}"
            ) from exc
        replay = _readonly_lean(checkout, list(command))
        if replay.returncode:
            _fail("external immutable proof kernel replay failed")
        type_sha, axioms, trust_output_sha = _lean_probe(checkout, data, declaration)
    trust = source.get("trust_audit", {})
    return {
        "schema_version": AUTHORITY_RESULT_SCHEMA,
        "formal_system": source.get("formal_system"),
        "toolchain": toolchain,
        "dependency_lock_sha256": dependency_sha,
        "file_path": file_path,
        "file_sha256": file_sha,
        "module": source.get("module"),
        "declaration": declaration,
        "declaration_type_sha256": type_sha,
        "terminal_proof_body_sha256": body_sha,
        "kernel_exit_code": 0,
        "placeholder_free": True,
        "unsafe_free": True,
        "oracle_free": True,
        "undeclared_axioms_free": set(axioms) <= PERMITTED_AXIOMS,
        "permitted_axioms": axioms,
        "trust_audit_output_sha256": trust_output_sha,
        "replay_authority": replay_authority,
        "resolved_revision": resolved,
        "archive_sha256": archive_sha,
        "resolved_tree": tree,
        "kernel_stdout_sha256": _sha256_bytes(replay.stdout),
        "kernel_stderr_sha256": _sha256_bytes(replay.stderr),
    }


def _schema_errors(root: Path, receipt: Any) -> list[str]:
    try:
        schema = _focus_schema(root)
    except (OSError, EligibilityError):
        return ["schema_unavailable"]
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(
            validator.iter_errors(receipt), key=lambda error: list(error.absolute_path)
        )
    except Exception:  # jsonschema uses version-specific schema exception types
        return ["schema_unavailable"]
    return ["schema_invalid"] if errors else []


def _schema_definition_errors(
    root: Path, value: Any, definition: str
) -> list[str]:
    """Validate a nested evidence receipt against a definition in the focus schema."""

    try:
        schema = _focus_schema(root)
        definitions = schema["$defs"]
        if definition not in definitions:
            return ["schema_unavailable"]
        wrapper = {
            "$schema": schema["$schema"],
            "$defs": definitions,
            "$ref": f"#/$defs/{definition}",
        }
        Draft202012Validator.check_schema(wrapper)
        validator = Draft202012Validator(wrapper, format_checker=FormatChecker())
        errors = list(validator.iter_errors(value))
    except Exception:  # jsonschema uses version-specific schema exception types
        return ["schema_unavailable"]
    return ["schema_invalid"] if errors else []


def _validate_common(
    root: Path,
    theorem_id: str,
    receipt: Mapping[str, Any],
    *,
    as_of: datetime,
    runtime_root: Path | str | None,
    require_issuance: bool,
) -> None:
    if receipt.get("schema_version") != SCHEMA_VERSION:
        _fail("receipt schema_version is unsupported")
    if receipt.get("theorem_id") != theorem_id:
        _fail("receipt theorem_id does not match its owner")
    if receipt.get("requirements_authority") != REQUIREMENTS_AUTHORITY:
        _fail("receipt requirements authority is stale")
    if receipt.get("scheduler_owner") != "scheduler_master_lane":
        _fail("receipt is not owned by the scheduler master lane")
    if require_issuance:
        _validate_issuance_authority(
            root,
            theorem_id,
            receipt,
            runtime_root=runtime_root,
        )
    base_revision = _resolve_base_revision(root, receipt.get("repository_base_revision"))
    _require_file_at_revision(
        root,
        base_revision,
        REQUIREMENTS_AUTHORITY,
        "requirements authority",
    )
    _require_file_at_revision(
        root,
        base_revision,
        TARGET_MEMBERSHIP_RELATIVE_PATH,
        "Stage1 target membership",
    )
    _require_file_at_revision(
        root,
        base_revision,
        SCHEMA_RELATIVE_PATH,
        "focus eligibility schema",
    )

    generated_at = _parse_timestamp(receipt.get("generated_at"), "generated_at")
    evidence_as_of = _parse_timestamp(receipt.get("evidence_as_of"), "evidence_as_of")
    expires_at = _parse_timestamp(receipt.get("expires_at"), "expires_at")
    if not evidence_as_of <= generated_at <= as_of:
        _fail("receipt timestamps are future-dated or out of order")
    if expires_at <= generated_at or as_of >= expires_at:
        _fail("receipt has expired")

    invalidations = receipt.get("invalidation_conditions")
    if not isinstance(invalidations, list) or set(invalidations) != REQUIRED_INVALIDATIONS:
        _fail("receipt invalidation coverage is incomplete")

    author = _actor(receipt.get("admission_review", {}).get("author"), "admission author")
    reviewer = _actor(receipt.get("admission_review", {}).get("reviewer"), "admission reviewer")
    _require_distinct_actors(author, reviewer, "admission reviewer")
    if _is_worker_actor(reviewer):
        _fail("worker may not perform admission review")
    if reviewer.get("role") not in {"scheduler_master_lane", "independent_reviewer"}:
        _fail("admission reviewer is not scheduler-owned or independent")

    target = receipt.get("target_binding")
    if not isinstance(target, Mapping):
        _fail("target binding is missing")
    path = target.get("path")
    digest = target.get("file_sha256")
    if path is not None:
        _safe_bound_file(
            root,
            theorem_id,
            {"path": path, "sha256": digest},
            "Lean target",
            base_revision=base_revision,
        )

    bindings = receipt.get("evidence_bindings")
    if not isinstance(bindings, list):
        _fail("evidence bindings are missing")
    roles: set[str] = set()
    for index, row in enumerate(bindings):
        if not isinstance(row, Mapping):
            _fail(f"evidence binding {index} is malformed")
        _safe_bound_file(
            root,
            theorem_id,
            row,
            f"evidence binding {index}",
            base_revision=base_revision,
        )
        role = row.get("role")
        if isinstance(role, str):
            roles.add(role)

    evidence_class = receipt.get("machine_evidence_class")
    disposition = receipt.get("execution_disposition")
    if evidence_class not in MACHINE_EVIDENCE_CLASSES or disposition not in EXECUTION_DISPOSITIONS:
        _fail("receipt classification is invalid")

    review_time = _parse_timestamp(
        receipt.get("admission_review", {}).get("reviewed_at"), "admission reviewed_at"
    )
    if review_time < evidence_as_of or review_time > generated_at:
        _fail("admission review does not postdate the evidence or is future-dated")

    human_source = receipt.get("human_proof", {}).get("source")
    if isinstance(human_source, Mapping):
        source_reviewer = _actor(human_source.get("accepted_by"), "human-source reviewer")
        if _is_worker_actor(source_reviewer) or source_reviewer.get("role") not in {
            "scheduler_master_lane",
            "independent_reviewer",
        }:
            _fail("human-proof source was not accepted by an independent authority")
        if _parse_timestamp(human_source.get("accepted_at"), "human source accepted_at") > evidence_as_of:
            _fail("human-proof source acceptance postdates the evidence snapshot")

    machine = receipt.get("machine_proof", {})
    machine_status = machine.get("status") if isinstance(machine, Mapping) else None
    expected_status = {
        "exact_pinned_closure": "exact_kernel_checked",
        "exact_external_unintegrated": "exact_kernel_checked",
        "no_exact_candidate_as_of": "no_usable_exact_artifact_located",
        "unknown": "unknown",
    }[str(evidence_class)]
    if machine_status != expected_status:
        _fail("machine evidence class and proof status disagree")
    negative_inventory = machine.get("negative_search_inventory")
    if machine_status == "no_usable_exact_artifact_located":
        if not isinstance(negative_inventory, list) or not negative_inventory:
            _fail("negative search lacks its bounded inventory")
        for index, row in enumerate(negative_inventory):
            if not isinstance(row, Mapping):
                _fail(f"negative search inventory {index} is malformed")
            searched_at = _parse_timestamp(
                row.get("searched_at"), f"negative search inventory {index} searched_at"
            )
            if searched_at > evidence_as_of:
                _fail("negative search postdates the evidence snapshot")


def _validate_statement_binding(receipt: Mapping[str, Any]) -> None:
    human = receipt.get("human_proof", {})
    target = receipt.get("target_binding", {})
    binding = receipt.get("statement_binding")
    if not isinstance(binding, Mapping):
        _fail("accepted statement lacks a source-to-target binding")
    human_fingerprint = human.get("statement_fingerprint")
    target_fingerprint = target.get("declaration_type_sha256")
    if (
        binding.get("human_statement_fingerprint") != human_fingerprint
        or binding.get("target_declaration_type_sha256") != target_fingerprint
    ):
        _fail("statement binding does not bind the accepted human and target fingerprints")
    match_kind = binding.get("match_kind")
    evidence = binding.get("evidence")
    if match_kind == "exact":
        if human_fingerprint != target_fingerprint or evidence:
            _fail("exact human-to-target statement binding is not fingerprint-identical")
        return
    # Human prose has no kernel-level statement identity. Until a canonical,
    # independently replayed human-semantics transport exists, a typed blob is
    # evidence only and cannot authorize work on a nonidentical target.
    _fail("nonidentical human and target statements require unsupported semantic transport")


def _validate_human_source_authority(
    root: Path, receipt: Mapping[str, Any], scheduler_verification: Mapping[str, Any]
) -> None:
    support = scheduler_verification.get("human_source_review")
    if not isinstance(support, Mapping):
        _fail("exact admission lacks a replayable human source review")
    if set(support) == {"human_source_review", "machine_transport_authority"}:
        support = support.get("human_source_review")
    if not isinstance(support, Mapping):
        _fail("exact admission lacks a replayable human source review")
    required = {
        "path",
        "sha256",
        "review_sha256",
        "source_artifact_path",
        "source_content_sha256",
        "publication_timestamp",
        "statement_crosswalk",
        "reviewer",
        "reviewed_at",
        "decision",
    }
    if set(support) != required or support.get("decision") != "accepted":
        _fail("human source review authority is malformed")
    theorem_id = str(receipt.get("theorem_id", ""))
    base = _resolve_base_revision(root, receipt.get("repository_base_revision"))
    for label, path_key, sha_key in (
        ("human source review", "path", "sha256"),
        ("human proof source artifact", "source_artifact_path", "source_content_sha256"),
    ):
        _safe_bound_file(
            root,
            theorem_id,
            {"path": support.get(path_key), "sha256": support.get(sha_key)},
            label,
            base_revision=base,
        )
    review_data = _git_blob_bytes(root, base, str(support["path"]), "human source review")
    review = _strict_json_object(review_data, "human source review")
    canonical = (
        json.dumps(review, ensure_ascii=True, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")
    if review_data != canonical:
        _fail("human source review is not canonical pretty JSON")
    if review.get("review_sha256") != support.get("review_sha256"):
        _fail("human source review digest is stale")
    _embedded_digest(review, "review_sha256", "human source review")
    reviewer = _actor(review.get("reviewer"), "human source reviewer")
    admission = receipt.get("admission_review", {})
    admission_author = _actor(admission.get("author"), "admission author")
    admission_reviewer = _actor(admission.get("reviewer"), "admission reviewer")
    if (
        reviewer != support.get("reviewer")
        or reviewer.get("role") != "independent_reviewer"
        or _is_worker_actor(reviewer)
    ):
        _fail("human source review is not independent")
    _require_distinct_actors(reviewer, admission_author, "human source reviewer")
    _require_distinct_actors(reviewer, admission_reviewer, "human source reviewer")
    human = receipt.get("human_proof", {})
    source = human.get("source") if isinstance(human, Mapping) else None
    reviewed_source = review.get("source")
    if not isinstance(source, Mapping) or not isinstance(reviewed_source, Mapping):
        _fail("human source review lacks an immutable source")
    artifact = _git_blob_bytes(
        root, base, str(support["source_artifact_path"]), "human proof source artifact"
    )
    crosswalk = review.get("statement_crosswalk")
    expected_crosswalk = {
        "source_artifact_sha256": _sha256_bytes(artifact),
        "locator": reviewed_source.get("locator"),
        "boundary": review.get("statement_boundary"),
        "hypotheses": review.get("hypotheses"),
        "statement_fingerprint": review.get("statement_fingerprint"),
        "target_declaration_type_sha256": receipt.get("target_binding", {}).get(
            "declaration_type_sha256"
        ),
        "relation": "exact",
    }
    source_identity = {
        key: source.get(key)
        for key in ("citation", "locator", "immutable_id", "content_sha256")
    }
    reviewed_identity = {
        key: reviewed_source.get(key)
        for key in ("citation", "locator", "immutable_id", "content_sha256")
    }
    if (
        reviewed_identity != source_identity
        or _sha256_bytes(artifact) != reviewed_source.get("content_sha256")
        or crosswalk != expected_crosswalk
        or support.get("statement_crosswalk") != crosswalk
        or review.get("statement_fingerprint") != human.get("statement_fingerprint")
        or review.get("statement_boundary") != source.get("proof_scope")
        or review.get("hypotheses") != source.get("hypotheses")
        or review.get("publication_status") != source.get("publication_status")
        or review.get("license") != source.get("license")
        or source.get("accepted_by") != reviewer
        or source.get("accepted_at") != review.get("reviewed_at")
    ):
        _fail("human source bytes, theorem boundary, or exact statement crosswalk is stale")
    timestamp_subject = {
        "kind": "human_proof_source",
        "immutable_id": reviewed_source.get("immutable_id"),
        "citation": reviewed_source.get("citation"),
        "locator": reviewed_source.get("locator"),
        "artifact_sha256": _sha256_bytes(artifact),
        "statement_fingerprint": review.get("statement_fingerprint"),
        "statement_boundary": review.get("statement_boundary"),
        "hypotheses": review.get("hypotheses"),
    }
    timestamp = _validate_independent_timestamp(
        root,
        review.get("publication_timestamp"),
        expected_subject=timestamp_subject,
        cutoff=None,
        forbidden_principals={
            str(reviewer.get("id")),
            str(admission_author.get("id")),
            str(admission_reviewer.get("id")),
        },
        label="human proof publication timestamp",
    )
    if timestamp != support.get("publication_timestamp"):
        _fail("human proof publication timestamp authority is stale")
    if _parse_timestamp(review.get("reviewed_at"), "human source reviewed_at") < _parse_timestamp(
        timestamp["issued_at"], "human proof publication timestamp"
    ):
        _fail("human source review predates its independently timestamped publication")


def _authority_observed_facts(verification: Mapping[str, Any], label: str) -> dict[str, Any]:
    expected_keys = {
        "schema_version", "theorem_id", "verification_kind", "verifier",
        "repository", "resolved_revision", "archive_sha256", "resolved_tree",
        "file_path", "file_sha256", "terminal_proof_body_sha256",
        "kernel_command", "kernel_exit_code", "kernel_stdout_sha256",
        "kernel_authority_result", "local_target_authority_result",
        "kernel_stderr_sha256", "repository_access", "network_during_replay",
        "human_source_review", "verification_sha256",
    }
    transport_authority = _transport_authority_support(verification, label)
    if set(verification) != expected_keys:
        _fail(f"{label} fields are not canonical")
    _embedded_digest(verification, "verification_sha256", label)
    external = verification.get("kernel_authority_result")
    local = verification.get("local_target_authority_result")
    if (
        verification.get("schema_version") != "stage1-focus-admission-verification/1.0"
        or verification.get("verification_kind") != "external_lean_kernel_replay"
        or verification.get("kernel_exit_code") != 0
        or verification.get("network_during_replay") is not False
        or not isinstance(external, Mapping)
        or external.get("schema_version") != AUTHORITY_RESULT_SCHEMA
        or not isinstance(local, Mapping)
        or local.get("schema_version") != LOCAL_TARGET_RESULT_SCHEMA
    ):
        _fail(f"{label} lacks exact external and local kernel authority results")
    result = {"external": dict(external), "local_target": dict(local)}
    if transport_authority is not None:
        result["machine_transport_authority"] = dict(transport_authority)
    return result


def _validate_admission_authority(root: Path, receipt: Mapping[str, Any]) -> None:
    authority = receipt.get("admission_authority")
    if not isinstance(authority, Mapping):
        _fail("exact integration lacks scheduler/reviewer admission authority")
    scheduler = authority.get("scheduler_verification")
    reviewer = authority.get("reviewer_verification")
    if not isinstance(scheduler, Mapping) or not isinstance(reviewer, Mapping):
        _fail("exact integration lacks both authority verification records")
    scheduler_actor = _actor(scheduler.get("verifier"), "scheduler focus verifier")
    reviewer_actor = _actor(reviewer.get("verifier"), "independent focus verifier")
    if scheduler_actor.get("role") != "scheduler_focus_verifier":
        _fail("scheduler authority record has the wrong principal")
    if reviewer_actor.get("role") != "independent_reviewer" or _is_worker_actor(reviewer_actor):
        _fail("review authority record is not independent")
    _require_distinct_actors(scheduler_actor, reviewer_actor, "focus authority reviewer")
    scheduler_facts = _authority_observed_facts(scheduler, "scheduler verification")
    reviewer_facts = _authority_observed_facts(reviewer, "reviewer verification")
    if scheduler_facts != reviewer_facts:
        _fail("scheduler and reviewer observed different proof or target facts")
    _validate_human_source_authority(root, receipt, scheduler)
    _validate_human_source_authority(root, receipt, reviewer)
    observed_kernel_facts = {
        "external": scheduler_facts["external"],
        "local_target": scheduler_facts["local_target"],
    }
    facts_sha = _sha256_bytes(
        json.dumps(observed_kernel_facts, ensure_ascii=True, sort_keys=True,
                   separators=(",", ":"), allow_nan=False).encode()
    )
    if authority.get("observed_facts_sha256") != facts_sha:
        _fail("admission authority observed-facts digest is stale")

    external = scheduler_facts["external"]
    local = scheduler_facts["local_target"]
    target = receipt["target_binding"]
    source = receipt["machine_proof"]["source"]
    evidence_class = receipt.get("machine_evidence_class")
    expected_external = {
        "file_path": source.get("file_path"),
        "file_sha256": source.get("file_sha256"),
        "module": source.get("module"),
        "declaration": source.get("declaration"),
        "declaration_type_sha256": source.get("declaration_type_sha256"),
        "terminal_proof_body_sha256": source.get("terminal_proof_body", {}).get("sha256"),
        "toolchain": source.get("kernel_replay", {}).get("toolchain"),
        "dependency_lock_sha256": source.get("kernel_replay", {}).get("dependency_lock_sha256"),
    }
    if any(external.get(key) != value for key, value in expected_external.items()):
        _fail("receipt machine proof differs from observed external authority facts")
    if (
        scheduler.get("repository") != source.get("repository")
        or scheduler.get("resolved_revision") != source.get("revision")
        or scheduler.get("file_sha256") != source.get("file_sha256")
        or scheduler.get("terminal_proof_body_sha256")
        != source.get("terminal_proof_body", {}).get("sha256")
    ):
        _fail("external replay identity differs from the receipt source")
    _validate_machine_pre_stage1_provenance(root, receipt, source)
    if evidence_class == "exact_pinned_closure":
        pinned_provider = _pinned_manifest_provider(
            root,
            str(receipt.get("repository_base_revision", "")),
            source,
        )
        _verify_local_pinned_provider(
            root,
            str(receipt.get("repository_base_revision", "")),
            source,
            pinned_provider,
        )
        try:
            replay_authority, _toolchain_root, _cache_root = (
                stage1_lean_authority.build_repository_lean_authority(
                    root,
                    authority_revision=str(receipt.get("repository_base_revision", "")),
                )
            )
        except Exception as exc:
            raise EligibilityError(f"pinned Lean replay authority is invalid: {exc}") from exc
        local_replay_authority = local.get("replay_authority", {})
        if (
            replay_authority.get("dependency_packages_sha256") is None
            or replay_authority.get("compiled_cache_sha256") is None
            or replay_authority.get("compiled_cache_file_count", 0) < 1
            or local_replay_authority.get("dependency_lock_sha256")
            != pinned_provider.get("manifest_sha256")
            or local_replay_authority.get("dependency_packages_sha256") is None
            or local_replay_authority.get("compiled_cache_sha256") is None
        ):
            _fail("exact pinned closure lacks a verified Lake manifest/package closure")
        # For a pinned proof the embedded external identity remains provenance,
        # while current proof authority comes only from the root lock/cache.
        if external.get("replay_authority") != replay_authority:
            _fail("pinned provider authority is not the current root Lake closure")
    else:
        _reject_authoritative_external_identity(root, source.get("repository"))
        replayed_external = _replay_external_authority(
            source, authoritative_root=root
        )
        replay_comparison = {key: replayed_external.get(key) for key in external}
        if replay_comparison != external:
            _fail("current external proof replay differs from admitted authority facts")
        if (
            scheduler.get("resolved_revision") != replayed_external["resolved_revision"]
            or scheduler.get("archive_sha256") != replayed_external["archive_sha256"]
            or scheduler.get("resolved_tree") != replayed_external["resolved_tree"]
            or scheduler.get("kernel_stdout_sha256")
            != replayed_external["kernel_stdout_sha256"]
            or scheduler.get("kernel_stderr_sha256")
            != replayed_external["kernel_stderr_sha256"]
        ):
            _fail("current external replay provenance differs from admission")
    expected_local = {
        "repository_revision": receipt.get("repository_base_revision"),
        "file_path": target.get("path"),
        "file_sha256": target.get("file_sha256"),
        "declaration": target.get("declaration"),
        "declaration_type_sha256": target.get("declaration_type_sha256"),
    }
    if any(local.get(key) != value for key, value in expected_local.items()):
        _fail("receipt target differs from observed local authority facts")

    # Embedded records are provenance, not a trust root. Re-run the current
    # target from the exact Git revision before granting any phase permission.
    revision = _resolve_base_revision(root, receipt.get("repository_base_revision"))
    target_bytes = _git_blob_bytes(root, revision, str(target["path"]), "Lean target")
    if PROHIBITED_LEAN_TOKENS.search(target_bytes.decode("utf-8", "replace")):
        _fail("local Lean target contains a prohibited construct")
    try:
        current_replay_authority, _toolchain_root, _cache_root = (
            stage1_lean_authority.build_repository_lean_authority(
                root, authority_revision=revision
            )
        )
    except Exception as exc:
        raise EligibilityError(f"pinned Lean replay authority is invalid: {exc}") from exc
    if local.get("replay_authority") != current_replay_authority:
        _fail("current local replay authority differs from admitted authority facts")
    with tempfile.TemporaryDirectory(prefix="stage1-focus-eligibility-") as directory:
        checkout = Path(directory) / "repository"
        checkout.mkdir()
        _materialize_revision(root, revision, checkout)
        lean_root = checkout / "Formalizations" / "Lean"
        if not lean_root.is_dir():
            _fail("repository snapshot lacks its Lean project")
        toolchain, dependency_sha = _dependency_identity(lean_root)
        type_sha, axioms, output_sha = _lean_probe(
            lean_root, target_bytes, str(target["declaration"])
        )
    if (
        type_sha != local.get("declaration_type_sha256")
        or toolchain != local.get("toolchain")
        or dependency_sha != local.get("dependency_lock_sha256")
        or axioms != local.get("permitted_axioms")
        or output_sha != local.get("trust_audit_output_sha256")
    ):
        _fail("current local target replay differs from admitted authority facts")

    match_kind = source.get("match_kind")
    transport_authority = scheduler_facts.get("machine_transport_authority")
    if match_kind == "checked_transport":
        if evidence_class == "exact_external_unintegrated":
            _fail(
                "checked transport is not admissible until the provider is pinned "
                "into the authoritative root closure"
            )
        if not isinstance(transport_authority, Mapping):
            _fail("checked transport lacks embedded semantic replay authority")
        _replay_machine_transport_semantics(
            root,
            receipt,
            source,
            target,
            transport_authority,
            base_revision=revision,
        )
    elif transport_authority is not None:
        _fail("exact match unexpectedly carries machine transport authority")


def _validate_machine_transport_replay(
    root: Path,
    receipt: Mapping[str, Any],
    row: Mapping[str, Any],
    expected_identity: Mapping[str, Any],
) -> None:
    """Validate one content-bound, independently reviewed transport replay."""

    theorem_id = str(receipt["theorem_id"])
    if row.get("replay_receipt_sha256") != row.get("sha256"):
        _fail("machine transport evidence does not bind its replay receipt digest")
    base_revision = _resolve_base_revision(
        root, receipt.get("repository_base_revision")
    )
    _safe_bound_file(
        root,
        theorem_id,
        row,
        "machine transport replay receipt",
        base_revision=base_revision,
    )
    path = _safe_repository_file(
        root, str(row.get("path", "")), "machine transport replay receipt"
    )
    payload = path.read_bytes()

    def reject_nonfinite(value: str) -> NoReturn:
        raise ValueError(f"non-finite JSON number: {value}")

    try:
        replay_receipt = json.loads(
            payload.decode("utf-8"), parse_constant=reject_nonfinite
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        _fail("machine transport replay receipt is not canonical JSON")
    if not isinstance(replay_receipt, dict):
        _fail("machine transport replay receipt is not a JSON object")
    canonical = (
        json.dumps(replay_receipt, ensure_ascii=True, indent=2, allow_nan=False)
        + "\n"
    ).encode("utf-8")
    if payload != canonical:
        _fail("machine transport replay receipt is not canonical JSON")
    if _schema_definition_errors(
        root, replay_receipt, "machineTransportReplayReceipt"
    ):
        _fail("machine transport replay receipt schema is invalid")
    if replay_receipt.get("theorem_id") != theorem_id:
        _fail("machine transport replay receipt theorem identity is stale")

    expected_source = {
        "formal_system": expected_identity["source_formal_system"],
        "declaration": expected_identity["source_declaration"],
        "declaration_type_sha256": expected_identity[
            "source_declaration_type_sha256"
        ],
    }
    expected_target = {
        "formal_system": expected_identity["target_formal_system"],
        "declaration": expected_identity["target_declaration"],
        "declaration_type_sha256": expected_identity[
            "target_declaration_type_sha256"
        ],
    }
    if (
        replay_receipt.get("source") != expected_source
        or replay_receipt.get("target") != expected_target
    ):
        _fail("machine transport replay does not bind the admitted source and target")

    artifact = replay_receipt["transport_artifact"]
    validator = replay_receipt["validator"]
    replay = replay_receipt["replay"]
    trust = replay_receipt["trust_audit"]
    for binding, label in (
        (artifact, "machine transport artifact"),
        (validator, "machine transport validator"),
        (replay["output"], "machine transport replay output"),
        (trust["output"], "machine transport trust-audit output"),
    ):
        _safe_bound_file(
            root,
            theorem_id,
            binding,
            label,
            base_revision=base_revision,
        )
    if (
        artifact.get("formal_system") != expected_identity["target_formal_system"]
        or artifact.get("declaration") != expected_identity["target_declaration"]
        or artifact.get("declaration_type_sha256")
        != expected_identity["target_declaration_type_sha256"]
    ):
        _fail("machine transport artifact does not implement the admitted target")
    if validator.get("authority") != "scheduler_master_lane":
        _fail("machine transport replay validator is not scheduler-owned")
    command = replay.get("command", [])
    if validator.get("path") not in command or artifact.get("path") not in command:
        _fail("machine transport replay command does not bind its validator and artifact")

    checked_at = _parse_timestamp(replay.get("checked_at"), "transport replay checked_at")
    reviewed_at = _parse_timestamp(
        replay_receipt.get("independent_review", {}).get("reviewed_at"),
        "transport replay reviewed_at",
    )
    evidence_as_of = _parse_timestamp(receipt.get("evidence_as_of"), "evidence_as_of")
    if not checked_at <= reviewed_at <= evidence_as_of:
        _fail("machine transport replay review timestamps are out of order")
    reviewer = _actor(
        replay_receipt.get("independent_review", {}).get("reviewer"),
        "machine transport reviewer",
    )
    author = _actor(receipt.get("admission_review", {}).get("author"), "admission author")
    if _is_worker_actor(reviewer) or reviewer.get("role") != "independent_reviewer":
        _fail("machine transport replay was not independently reviewed")
    _require_distinct_actors(author, reviewer, "machine transport reviewer")


def _replay_machine_transport_semantics(
    root: Path,
    receipt: Mapping[str, Any],
    source: Mapping[str, Any],
    target: Mapping[str, Any],
    authority: Mapping[str, Any],
    *,
    base_revision: str,
) -> None:
    """Rebuild the admitted provider/consumer proof and recheck real dependence."""

    if authority.get("schema_version") != TRANSPORT_AUTHORITY_RESULT_SCHEMA:
        _fail("machine transport semantic authority schema is stale")
    _embedded_digest(
        authority,
        "transport_verification_sha256",
        "machine transport semantic authority",
    )
    materialization = authority.get("provider_materialization")
    semantic = authority.get("semantic_dependency")
    artifact = authority.get("transport_artifact")
    if (
        not isinstance(materialization, Mapping)
        or not isinstance(semantic, Mapping)
        or not isinstance(artifact, Mapping)
        or materialization.get("module") != TRANSPORT_PROVIDER_MODULE
        or materialization.get("declaration") != source.get("declaration")
        or materialization.get("source_file_sha256") != source.get("file_sha256")
        or materialization.get("compiled_exit_code") != 0
        or semantic.get("target_declaration") != target.get("declaration")
        or semantic.get("provider_declaration") != source.get("declaration")
        or semantic.get("relation") != "direct_proof_body_constant_dependency"
        or semantic.get("joint_kernel_exit_code") != 0
    ):
        _fail("machine transport authority does not bind provider materialization and semantics")
    artifact_path = str(artifact.get("path", ""))
    artifact_bytes = _git_blob_bytes(
        root, base_revision, artifact_path, "machine transport artifact"
    )
    if _sha256_bytes(artifact_bytes) != artifact.get("sha256"):
        _fail("machine transport artifact differs from embedded semantic authority")

    repository = source.get("repository")
    revision = source.get("revision")
    file_path = str(source.get("file_path", ""))
    with tempfile.TemporaryDirectory(prefix="stage1-focus-transport-recheck-") as directory:
        external = Path(directory) / "external"
        clone = subprocess.run(
            ["git", "clone", "--no-checkout", "--", str(repository), str(external)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if clone.returncode:
            _fail("transport provider cannot be cloned for semantic recheck")
        resolved = _git_text(
            external,
            ["rev-parse", "--verify", f"{revision}^{{commit}}"],
            "transport provider revision",
        )
        if resolved != revision or _git(external, ["checkout", "--detach", resolved]).returncode:
            _fail("transport provider revision cannot be materialized")
        provider_path = external / file_path
        if not provider_path.is_file() or provider_path.is_symlink():
            _fail("transport provider source is missing or unsafe")
        provider_bytes = provider_path.read_bytes()
        if _sha256_bytes(provider_bytes) != materialization.get("source_file_sha256"):
            _fail("materialized transport provider differs from embedded authority")

        checkout = Path(directory) / "repository"
        checkout.mkdir()
        _materialize_revision(root, base_revision, checkout)
        lean_root = checkout / "Formalizations" / "Lean"
        provider_source = lean_root / TRANSPORT_PROVIDER_SOURCE
        provider_olean = lean_root / TRANSPORT_PROVIDER_OLEAN
        replay_source = lean_root / TRANSPORT_REPLAY_SOURCE
        if any(path.exists() or path.is_symlink() for path in (
            provider_source, provider_olean, replay_source
        )):
            _fail("machine transport semantic replay paths conflict")
        provider_source.write_bytes(provider_bytes)
        replay_source.write_bytes(
            _transport_replay_source(
                artifact_bytes,
                target_declaration=str(target.get("declaration", "")),
                provider_declaration=str(source.get("declaration", "")),
            )
        )
        try:
            compiled = _readonly_lean(
                lean_root,
                ["lean", "-o", TRANSPORT_PROVIDER_OLEAN, TRANSPORT_PROVIDER_SOURCE],
                writable=True,
            )
            if compiled.returncode:
                _fail("materialized transport provider no longer compiles")
            replayed = _readonly_lean(
                lean_root,
                ["lean", TRANSPORT_REPLAY_SOURCE],
                lean_path=lean_root,
            )
        finally:
            provider_source.unlink(missing_ok=True)
            provider_olean.unlink(missing_ok=True)
            replay_source.unlink(missing_ok=True)
    if replayed.returncode:
        _fail("machine transport no longer has a provider-dependent consumer proof body")


def _validate_exact_integration(root: Path, receipt: Mapping[str, Any]) -> None:
    if receipt.get("machine_evidence_class") not in {
        "exact_pinned_closure",
        "exact_external_unintegrated",
    }:
        _fail("integration disposition lacks exact machine evidence")
    if receipt.get("frontier_exception") is not None:
        _fail("integration disposition must not carry a frontier exception")
    require_integration_root_unaccepted(root, str(receipt.get("theorem_id", "")))
    human = receipt.get("human_proof", {})
    target = receipt.get("target_binding", {})
    target_fingerprint = target.get("declaration_type_sha256")
    machine = receipt.get("machine_proof", {})
    gap = receipt.get("repository_gap", {})
    if human.get("status") != "complete_source_confirmed" or human.get("source") is None:
        _fail("integration admission lacks a confirmed complete human proof")
    if target.get("status") != "verified":
        _fail("integration admission lacks an exact verified Lean target")
    if machine.get("status") != "exact_kernel_checked" or machine.get("source") is None:
        _fail("integration admission lacks an exact kernel-checked machine proof")
    if machine.get("negative_search_boundary") is not None:
        _fail("exact machine proof must not carry a negative-search claim")
    _validate_statement_binding(receipt)
    if gap.get("acceptance_status") not in {
        "not_integrated",
        "present_unaccepted",
        "dependency_unaccepted",
    }:
        _fail("target has no unaccepted repository integration gap")
    if gap.get("local_presence") == "repository_accepted":
        _fail("already accepted theorem is outside Stage1 integration focus")
    if not gap.get("integration_plan"):
        _fail("integration admission lacks a concrete integration plan")
    owned_paths = gap.get("owned_paths")
    owner_root = f"Stage1_Instances/{receipt['theorem_id']}"
    if (
        not isinstance(owned_paths, list)
        or not owned_paths
        or any(
            not isinstance(path, str)
            or (path != owner_root and not path.startswith(owner_root + "/"))
            for path in owned_paths
        )
    ):
        _fail("integration admission lacks theorem-owned path boundaries")
    decision = receipt.get("admission_review", {}).get("decision")
    if decision != "admit_integration":
        _fail("admission review did not approve integration")

    _validate_admission_authority(root, receipt)

    source = machine["source"]
    match_kind = source.get("match_kind")
    transport = source.get("transport_evidence")
    if (
        receipt.get("machine_evidence_class") == "exact_external_unintegrated"
        and match_kind == "checked_transport"
    ):
        _fail(
            "checked transport cannot admit an unintegrated external provider; "
            "the provider must first enter the authoritative pinned closure"
        )
    if match_kind == "exact" and transport:
        _fail("exact match must not claim checked transport")
    if match_kind == "checked_transport" and not transport:
        _fail("checked transport lacks content-bound evidence")
    if transport:
        theorem_id = str(receipt["theorem_id"])
        expected_transport_identity = {
            "role": "statement_match",
            "evidence_kind": "machine_checked_statement_transport",
            "source_formal_system": source.get("formal_system"),
            "source_declaration": source.get("declaration"),
            "source_declaration_type_sha256": source.get("declaration_type_sha256"),
            "target_formal_system": target.get("formal_system"),
            "target_declaration": target.get("declaration"),
            "target_declaration_type_sha256": target.get("declaration_type_sha256"),
            "replay_receipt_sha256": None,
        }
        if any(
            not isinstance(row, Mapping)
            or any(
                row.get(key) != value
                for key, value in expected_transport_identity.items()
                if key != "replay_receipt_sha256"
            )
            or row.get("replay_receipt_sha256") != row.get("sha256")
            for row in transport
        ):
            _fail("checked machine transport does not bind the exact source and target types")
        transport_keys = {(row.get("path"), row.get("sha256")) for row in transport}
        bound_keys = {
            (row.get("path"), row.get("sha256"))
            for row in receipt.get("evidence_bindings", [])
            if isinstance(row, Mapping)
        }
        if not transport_keys <= bound_keys:
            _fail(f"{theorem_id} transport evidence is not top-level content-bound")
        for row in transport:
            _validate_machine_transport_replay(
                root, receipt, row, expected_transport_identity
            )
    if match_kind == "exact" and (
        source.get("formal_system") != target.get("formal_system")
        or source.get("declaration_type_sha256") != target.get("declaration_type_sha256")
    ):
        _fail("exact machine source does not match the bound target type")
    if match_kind == "checked_transport" and (
        source.get("formal_system") == target.get("formal_system")
        and source.get("declaration_type_sha256") == target_fingerprint
    ):
        _fail("checked transport is redundant and does not bind a nonidentical source type")
    replay = source.get("kernel_replay", {})
    compatibility = source.get("compatibility", {})
    if (
        replay.get("toolchain") != compatibility.get("toolchain")
        or replay.get("dependency_lock_sha256")
        != compatibility.get("dependency_lock_sha256")
    ):
        _fail("kernel replay and compatibility audit use different environments")
    checked_at = _parse_timestamp(replay.get("checked_at"), "kernel replay checked_at")
    if checked_at > _parse_timestamp(receipt.get("evidence_as_of"), "evidence_as_of"):
        _fail("kernel replay postdates the evidence snapshot")
    presence = gap.get("local_presence")
    evidence_class = receipt.get("machine_evidence_class")
    if evidence_class == "exact_pinned_closure" and presence != "pinned_dependency":
        _fail("pinned closure is not present in a pinned dependency")
    if evidence_class == "exact_external_unintegrated" and presence not in {
        "absent",
        "external_cache_only",
        "repository_unaccepted",
    }:
        _fail("external machine proof has an inconsistent local-presence status")

    roles = {
        row.get("role")
        for row in receipt.get("evidence_bindings", [])
        if isinstance(row, Mapping)
    }
    required_roles = {
        "human_source_review",
        "statement_match",
        "machine_source_pin",
        "kernel_replay",
        "trust_audit",
        "compatibility_audit",
        "license_review",
        "integration_plan",
    }
    if not required_roles <= roles:
        _fail("integration admission lacks one or more required evidence roles")


def _validate_frontier_exception(receipt: Mapping[str, Any], *, as_of: datetime) -> None:
    if receipt.get("admission_authority") is not None:
        _fail("frontier exception carries integration-only admission authority")
    if receipt.get("machine_evidence_class") != "no_exact_candidate_as_of":
        _fail("frontier exception requires a bounded negative candidate search")
    human = receipt.get("human_proof", {})
    target = receipt.get("target_binding", {})
    machine = receipt.get("machine_proof", {})
    exception = receipt.get("frontier_exception")
    if human.get("status") != "complete_source_confirmed" or human.get("source") is None:
        _fail("frontier exception lacks a confirmed complete human proof")
    if target.get("status") != "verified":
        _fail("frontier exception lacks an exact verified Lean target")
    _validate_statement_binding(receipt)
    if machine.get("status") != "no_usable_exact_artifact_located":
        _fail("frontier exception is inconsistent with machine-proof search status")
    boundary = machine.get("negative_search_boundary")
    if not isinstance(boundary, str) or not boundary.strip():
        _fail("negative search must name only its bounded as-of/query boundary")
    if not isinstance(exception, Mapping):
        _fail("frontier exception evidence is missing")
    if exception.get("scheduler_owner") != "scheduler_master_lane":
        _fail("frontier exception is not scheduler-owned")
    probability = exception.get("completion_probability")
    if (
        not isinstance(probability, (int, float))
        or isinstance(probability, bool)
        or not 0.70 <= probability <= 1.0
    ):
        _fail("frontier exception completion probability is below 0.70")

    author = _actor(receipt.get("admission_review", {}).get("author"), "admission author")
    assigned_worker = _actor(exception.get("assigned_worker"), "assigned frontier worker")
    estimator = _actor(exception.get("estimator"), "frontier estimator")
    review = exception.get("independent_review")
    if not isinstance(review, Mapping):
        _fail("frontier exception lacks durable independent review evidence")
    reviewer = _actor(review.get("reviewer"), "frontier exception reviewer")
    if assigned_worker.get("role") != "proof_worker":
        _fail("frontier exception lacks a canonical assigned proof worker")
    if _is_worker_actor(estimator) or estimator.get("role") != "scheduler_estimator":
        _fail("worker-authored probability cannot authorize a frontier exception")
    if _is_worker_actor(reviewer) or reviewer.get("role") != "independent_reviewer":
        _fail("frontier exception review is not independent")
    _require_distinct_actors(estimator, reviewer, "frontier exception reviewer")
    _require_distinct_actors(author, reviewer, "frontier exception reviewer")
    _require_distinct_actors(assigned_worker, estimator, "frontier estimator")
    _require_distinct_actors(assigned_worker, reviewer, "frontier exception reviewer")
    _require_distinct_actors(assigned_worker, author, "frontier admission author")

    if review.get("decision") != "approved":
        _fail("frontier exception was not approved")
    if receipt.get("admission_review", {}).get("decision") != "admit_frontier_exception":
        _fail("admission review did not admit the frontier exception")
    estimated_at = _parse_timestamp(exception.get("estimated_at"), "frontier estimated_at")
    authored_at = _parse_timestamp(
        review.get("authored_at"), "frontier review authored_at"
    )
    reviewed_at = _parse_timestamp(review.get("reviewed_at"), "frontier reviewed_at")
    evidence_as_of = _parse_timestamp(receipt.get("evidence_as_of"), "evidence_as_of")
    generated_at = _parse_timestamp(receipt.get("generated_at"), "generated_at")
    if (
        estimated_at < evidence_as_of
        or estimated_at > authored_at
        or authored_at > reviewed_at
        or reviewed_at > generated_at
    ):
        _fail("frontier estimate/review timestamps are out of order")
    review_input = {key: value for key, value in review.items() if key != "reviewed_at"}
    review_digest = review.get("review_input_sha256")
    if (
        review.get("schema_version") != FRONTIER_REVIEW_INPUT_SCHEMA
        or review.get("theorem_id") != receipt.get("theorem_id")
        or review.get("candidate_sha256")
        != receipt.get("issuance_authority", {}).get("candidate_sha256")
        or not isinstance(review_digest, str)
        or not SHA256_RE.fullmatch(review_digest)
    ):
        _fail("frontier independent review identity is malformed")
    _embedded_digest(
        review_input,
        "review_input_sha256",
        "frontier independent review input",
    )
    assessed_probability = review.get("assessed_completion_probability")
    comparables = review.get("comparables")
    findings = review.get("findings")
    if (
        not isinstance(assessed_probability, (int, float))
        or isinstance(assessed_probability, bool)
        or not 0.70 <= float(assessed_probability) <= 1.0
        or not isinstance(review.get("estimation_method_assessment"), str)
        or not review["estimation_method_assessment"].strip()
        or not isinstance(comparables, list)
        or not comparables
        or any(not isinstance(row, str) or not row.strip() for row in comparables)
        or not isinstance(findings, list)
        or not findings
        or any(not isinstance(row, str) or not row.strip() for row in findings)
    ):
        _fail("frontier independent review is not substantive or below 0.70")
    expected_control_assessments = {
        "budget_assessment": exception.get("budget"),
        "milestone_assessment": exception.get("milestones"),
        "validator_assessment": exception.get("validator"),
        "stop_condition_assessment": exception.get("stop_conditions"),
    }
    if any(
        review.get(key) != expected
        for key, expected in expected_control_assessments.items()
    ):
        _fail("frontier independent review does not bind the authorized controls")
    root_obligation = exception.get("root_obligation", {})
    if root_obligation.get("statement_fingerprint") != receipt.get("human_proof", {}).get(
        "statement_fingerprint"
    ):
        _fail("frontier root obligation does not bind the accepted human statement")
    if not str(exception.get("estimation_method", "")).strip():
        _fail("frontier exception lacks an estimation method")
    validator = exception.get("validator")
    if (
        not isinstance(validator, Mapping)
        or not isinstance(validator.get("path"), str)
        or validator.get("command") != ["python3", validator.get("path")]
    ):
        _fail(
            "frontier validator command must be exactly ['python3', validator.path]"
        )
    budget = exception.get("budget", {})
    resource_fields = {
        "wall_clock_seconds",
        "token_limit",
        "compute_seconds",
        "disk_bytes",
        "concurrency_limit",
    }
    if (
        not isinstance(budget, Mapping)
        or not str(budget.get("scope", "")).strip()
        or any(
            not isinstance(budget.get(field), int)
            or isinstance(budget.get(field), bool)
            or budget.get(field, 0) <= 0
            for field in resource_fields
        )
        or set(exception.get("stop_conditions", [])) != REQUIRED_FRONTIER_STOP_CONDITIONS
    ):
        _fail("frontier exception lacks finite multidimensional resources and stop conditions")
    if any(budget[field] > maximum for field, maximum in MAX_FRONTIER_BUDGET.items()):
        _fail("frontier exception resource budget exceeds the policy maximum")
    evidence = exception.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        _fail("frontier estimate lacks content-bound evidence")
    bound_keys = {
        (row.get("path"), row.get("sha256"))
        for row in receipt.get("evidence_bindings", [])
        if isinstance(row, Mapping)
    }
    estimate_keys = {
        (row.get("path"), row.get("sha256"))
        for row in evidence
        if isinstance(row, Mapping)
    }
    if not estimate_keys or not estimate_keys <= bound_keys:
        _fail("frontier estimate evidence is not top-level content-bound")
    validator = exception.get("validator", {})
    if not isinstance(validator, Mapping):
        _fail("frontier exception validator is missing")
    validator_key = (validator.get("path"), validator.get("sha256"))
    if validator_key not in bound_keys:
        _fail("frontier exception validator is not top-level content-bound")
    milestones = exception.get("milestones")
    if not isinstance(milestones, list) or not milestones:
        _fail("frontier exception lacks milestones")
    milestone_ids: set[str] = set()
    previous_deadline = reviewed_at
    for milestone in milestones:
        if not isinstance(milestone, Mapping):
            _fail("frontier exception milestone is malformed")
        milestone_id = milestone.get("id")
        if not isinstance(milestone_id, str) or milestone_id in milestone_ids:
            _fail("frontier exception milestone identities are missing or duplicated")
        milestone_ids.add(milestone_id)
        deadline = _parse_timestamp(
            milestone.get("deadline_at"), f"frontier milestone {milestone_id} deadline_at"
        )
        if deadline <= previous_deadline:
            _fail("frontier exception milestone deadlines are not strictly increasing")
        previous_deadline = deadline
    attempt_limit = exception.get("attempt_limit")
    if (
        not isinstance(attempt_limit, int)
        or isinstance(attempt_limit, bool)
        or not 1 <= attempt_limit <= MAX_FRONTIER_ATTEMPTS
    ):
        _fail("frontier exception attempt limit is invalid")
    lease_expires_at = _parse_timestamp(
        exception.get("lease_expires_at"), "frontier lease_expires_at"
    )
    if (
        lease_expires_at <= reviewed_at
        or as_of >= lease_expires_at
        or (lease_expires_at - reviewed_at).total_seconds() > MAX_FRONTIER_LEASE_SECONDS
        or lease_expires_at > _parse_timestamp(receipt.get("expires_at"), "expires_at")
    ):
        _fail("frontier exception lease is expired or exceeds receipt validity")
    if previous_deadline > lease_expires_at:
        _fail("frontier exception milestone exceeds its lease")
    if exception.get("revocation_route") != "scheduler_master_lane":
        _fail("frontier exception lacks scheduler-owned revocation")


def _validate_research_or_defer(
    root: Path, receipt: Mapping[str, Any]
) -> None:
    disposition = receipt.get("execution_disposition")
    if receipt.get("admission_authority") is not None:
        _fail("non-integration receipt carries exact admission authority")
    evidence_class = receipt.get("machine_evidence_class")
    machine = receipt.get("machine_proof", {})
    decision = receipt.get("admission_review", {}).get("decision")
    basis = receipt.get("disposition_basis")
    if receipt.get("frontier_exception") is not None:
        _fail("non-exception disposition must not carry a frontier exception")
    if disposition == "research_required":
        if decision != "research_only":
            _fail("research-required receipt lacks research-only admission")
        if evidence_class not in {"unknown", "no_exact_candidate_as_of"}:
            _fail("research-required receipt has an inconsistent evidence class")
        if basis is not None:
            _fail("research-required receipt must not claim a terminal disposition basis")
    elif disposition == "defer_frontier":
        if decision != "defer":
            _fail("deferred receipt lacks a defer decision")
        if evidence_class != "no_exact_candidate_as_of":
            _fail("deferred receipt lacks a bounded negative candidate search")
        _validate_terminal_disposition_basis(
            root, receipt, basis, FRONTIER_DEFER_REASONS, "frontier_defer_review"
        )
    elif disposition == "exclude_scope":
        if decision != "exclude":
            _fail("excluded receipt lacks an exclude decision")
        _validate_terminal_disposition_basis(
            root, receipt, basis, SCOPE_EXCLUSION_REASONS, "scope_exclusion_review"
        )
        reason = basis.get("reason_code") if isinstance(basis, Mapping) else None
        if (
            reason == "human_claim_unproved_or_conjectural"
            and receipt.get("human_proof", {}).get("status") != "partial_or_open"
        ):
            _fail("human-claim exclusion lacks positive open or conjectural evidence")
        if reason == "already_locally_accepted_root" and (
            receipt.get("repository_gap", {}).get("acceptance_status") != "master_accepted"
            or receipt.get("repository_gap", {}).get("local_presence")
            != "repository_accepted"
        ):
            _fail("accepted-root exclusion lacks repository acceptance evidence")
    if machine.get("status") == "no_usable_exact_artifact_located":
        boundary = machine.get("negative_search_boundary")
        if not isinstance(boundary, str) or not boundary.strip():
            _fail("negative candidate status lacks its bounded as-of/query boundary")
    gap = receipt.get("repository_gap", {})
    owned_paths = gap.get("owned_paths") if isinstance(gap, Mapping) else None
    owner_root = f"Stage1_Instances/{receipt['theorem_id']}"
    if isinstance(owned_paths, list) and any(
        not isinstance(path, str)
        or (path != owner_root and not path.startswith(owner_root + "/"))
        for path in owned_paths
    ):
        _fail("receipt owned paths escape the theorem owner")


def _validate_terminal_disposition_basis(
    root: Path,
    receipt: Mapping[str, Any],
    basis: Any,
    allowed_reasons: set[str],
    required_role: str,
) -> None:
    if (
        not isinstance(basis, Mapping)
        or basis.get("reason_code") not in allowed_reasons
        or not isinstance(basis.get("summary"), str)
        or not basis.get("summary", "").strip()
        or not isinstance(basis.get("evidence"), list)
        or not basis.get("evidence")
    ):
        _fail("terminal disposition lacks a structured positive evidence basis")
    bound = {
        (row.get("path"), row.get("sha256"), row.get("role"))
        for row in receipt.get("evidence_bindings", [])
        if isinstance(row, Mapping)
    }
    basis_rows = basis["evidence"]
    if any(
        not isinstance(row, Mapping)
        or row.get("role") != required_role
        or (row.get("path"), row.get("sha256"), row.get("role")) not in bound
        for row in basis_rows
    ):
        _fail("terminal disposition evidence is untyped or not top-level content-bound")
    if len(basis_rows) != 1:
        _fail("terminal disposition requires exactly one authoritative report")
    row = basis_rows[0]
    if basis.get("report_sha256") != row.get("sha256"):
        _fail("terminal disposition does not bind its report digest")
    theorem_id = str(receipt["theorem_id"])
    base_revision = _resolve_base_revision(
        root, receipt.get("repository_base_revision")
    )
    _safe_bound_file(
        root,
        theorem_id,
        row,
        "terminal disposition report",
        base_revision=base_revision,
    )
    path = _safe_repository_file(
        root, str(row.get("path", "")), "terminal disposition report"
    )
    payload = path.read_bytes()
    try:
        report = json.loads(
            payload.decode("utf-8"),
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError(f"non-finite JSON number: {value}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        _fail("terminal disposition report is not canonical JSON")
    canonical = (
        json.dumps(report, ensure_ascii=True, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")
    if payload != canonical or not isinstance(report, Mapping):
        _fail("terminal disposition report is not canonical JSON")
    if _schema_definition_errors(root, report, "terminalDispositionReport"):
        _fail("terminal disposition report schema is invalid")
    reason = basis["reason_code"]
    if report.get("theorem_id") != theorem_id or report.get("reason_code") != reason:
        _fail("terminal disposition report identity or reason is stale")
    reviewer = _actor(report.get("reviewer"), "terminal disposition reviewer")
    author = _actor(receipt.get("admission_review", {}).get("author"), "admission author")
    if _is_worker_actor(reviewer) or reviewer.get("role") != "independent_reviewer":
        _fail("terminal disposition report was not independently reviewed")
    _require_distinct_actors(author, reviewer, "terminal disposition reviewer")
    reviewed_at = _parse_timestamp(report.get("reviewed_at"), "terminal disposition reviewed_at")
    evidence_as_of = _parse_timestamp(receipt.get("evidence_as_of"), "evidence_as_of")
    if reviewed_at > evidence_as_of:
        _fail("terminal disposition review postdates the evidence snapshot")

    facts = report["facts"]
    expected_kind = {
        **{code: "frontier_exception_snapshot" for code in FRONTIER_DEFER_REASONS},
        "human_claim_unproved_or_conjectural": "open_claim_source_review",
        "non_exact_umbrella": "exact_boundary_comparison",
        "already_locally_accepted_root": "accepted_root_receipt",
        "unusable_legal_boundary": "license_review",
        "unusable_technical_boundary": "reproducible_incompatibility",
    }[reason]
    if facts.get("kind") != expected_kind:
        _fail("terminal disposition report fact kind does not match its reason")
    if reason in FRONTIER_DEFER_REASONS:
        boundary = str(receipt.get("machine_proof", {}).get("negative_search_boundary", ""))
        if facts.get("search_boundary_sha256") != _sha256_bytes(boundary.encode("utf-8")):
            _fail("frontier disposition report does not bind the negative search boundary")
        expected_state = {
            "no_current_frontier_exception": "absent",
            "frontier_probability_below_threshold": "below_threshold",
            "frontier_exception_rejected": "rejected",
            "frontier_exception_expired": "expired",
            "frontier_exception_exhausted": "exhausted",
        }[reason]
        if facts.get("exception_state") != expected_state:
            _fail("frontier disposition report state does not match its reason")
        _safe_bound_file(
            root,
            theorem_id,
            {"path": facts.get("snapshot_path"), "sha256": facts.get("snapshot_sha256")},
            "frontier exception snapshot",
            base_revision=base_revision,
        )
        snapshot_path = _safe_repository_file(
            root, str(facts.get("snapshot_path", "")), "frontier exception snapshot"
        )
        try:
            snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            _fail("frontier exception snapshot is not structured JSON")
        if _schema_definition_errors(root, snapshot, "frontierExceptionStateSnapshot"):
            _fail("frontier exception snapshot schema is invalid")
        expected_snapshot = {
            "theorem_id": theorem_id,
            "scheduler_owner": "scheduler_master_lane",
            "snapshot_id": facts.get("exception_snapshot_id"),
            "search_boundary_sha256": facts.get("search_boundary_sha256"),
            "exception_policy_sha256": facts.get("exception_policy_sha256"),
            "exception_state": facts.get("exception_state"),
        }
        if any(snapshot.get(key) != value for key, value in expected_snapshot.items()):
            _fail("frontier disposition facts disagree with the scheduler snapshot")
        if _parse_timestamp(snapshot.get("captured_at"), "frontier snapshot captured_at") > evidence_as_of:
            _fail("frontier exception snapshot postdates the evidence snapshot")
    elif reason == "human_claim_unproved_or_conjectural":
        if (
            facts.get("claim_status") != receipt.get("human_proof", {}).get("status")
            or not str(facts.get("source_immutable_id", "")).strip()
            or not SHA256_RE.fullmatch(str(facts.get("source_content_sha256", "")))
        ):
            _fail("open-claim report disagrees with the human-proof status")
        _safe_bound_file(
            root,
            theorem_id,
            {"path": facts.get("source_path"), "sha256": facts.get("source_content_sha256")},
            "open-claim immutable source",
            base_revision=base_revision,
        )
    elif reason == "non_exact_umbrella":
        fingerprint = receipt.get("human_proof", {}).get("statement_fingerprint")
        if (
            facts.get("catalogue_statement_sha256") != fingerprint
            or facts.get("candidate_statement_sha256") == fingerprint
        ):
            _fail("umbrella exclusion lacks an exact nonidentical boundary comparison")
    elif reason == "already_locally_accepted_root":
        if facts.get("root_statement_sha256") != receipt.get("target_binding", {}).get(
            "declaration_type_sha256"
        ):
            _fail("accepted-root report does not bind the repository target")
        _safe_bound_file(
            root,
            theorem_id,
            {
                "path": facts.get("master_receipt_path"),
                "sha256": facts.get("master_receipt_sha256"),
            },
            "accepted-root master receipt",
            base_revision=base_revision,
        )
        master_path = _safe_repository_file(
            root, str(facts.get("master_receipt_path", "")), "accepted-root master receipt"
        )
        try:
            master = json.loads(master_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            _fail("accepted-root master receipt is not structured JSON")
        if (
            master.get("schema_version") != "stage1-master-phase-acceptance/1.0"
            or master.get("theorem_id") != theorem_id
            or master.get("phase") != "release"
            or master.get("theorem_complete") is not True
            or master.get("phase_evidence_accepted") is not True
        ):
            _fail("accepted-root master receipt does not prove terminal root acceptance")
    elif reason == "unusable_legal_boundary":
        _safe_bound_file(
            root,
            theorem_id,
            {"path": facts.get("artifact_path"), "sha256": facts.get("artifact_sha256")},
            "license-blocked artifact",
            base_revision=base_revision,
        )
    elif reason == "unusable_technical_boundary":
        if (
            facts.get("exit_code") == 0
            or not facts.get("reproduction_command")
            or not SHA256_RE.fullmatch(str(facts.get("output_sha256", "")))
        ):
            _fail("technical exclusion lacks reproducible incompatibility evidence")
        _safe_bound_file(
            root,
            theorem_id,
            {"path": facts.get("output_path"), "sha256": facts.get("output_sha256")},
            "technical incompatibility output",
            base_revision=base_revision,
        )


def _semantic_validate(
    root: Path,
    theorem_id: str,
    receipt: Mapping[str, Any],
    *,
    as_of: datetime,
    runtime_root: Path | str | None,
    require_issuance: bool,
) -> None:
    if receipt.get("execution_disposition") == "organize_or_integrate":
        # Current acceptance outranks historical receipt facts and is checked
        # before their base-revision bindings can report a generic stale view.
        require_integration_root_unaccepted(root, theorem_id)
    _validate_common(
        root,
        theorem_id,
        receipt,
        as_of=as_of,
        runtime_root=runtime_root,
        require_issuance=require_issuance,
    )
    disposition = receipt["execution_disposition"]
    if disposition == "organize_or_integrate":
        _validate_exact_integration(root, receipt)
    elif disposition == "frontier_exception":
        _validate_frontier_exception(receipt, as_of=as_of)
    else:
        _validate_research_or_defer(root, receipt)


def validate_receipt(
    repo_root: Path | str,
    theorem_id: str,
    receipt: Mapping[str, Any],
    *,
    as_of: datetime | None = None,
    runtime_root: Path | str | None = None,
    require_issuance: bool = True,
) -> None:
    """Validate one already-parsed receipt and its bound repository evidence.

    This strict API raises ``EligibilityError`` and is intended for receipt
    producers and focused tests.  Scheduler/DAG callers should use
    ``evaluate_target`` so every failure becomes a JSON-safe fail-closed view.
    """

    root = _repo_root(repo_root)
    if theorem_id not in _target_membership_ids(root):
        _fail("theorem_id is outside frozen Stage1 target membership")
    schema_errors = _schema_errors(root, receipt)
    if schema_errors:
        _fail(",".join(schema_errors))
    payload = (
        json.dumps(receipt, ensure_ascii=True, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")
    _semantic_validate(
        root,
        theorem_id,
        receipt,
        as_of=_canonical_as_of(as_of),
        runtime_root=runtime_root,
        require_issuance=require_issuance,
    )


def _permissions(disposition: str, *, valid: bool) -> dict[str, bool]:
    if not valid:
        allowed: frozenset[str] = frozenset()
    elif disposition in {"organize_or_integrate", "frontier_exception"}:
        allowed = FULL_PHASES
    elif disposition == "research_required":
        allowed = RESEARCH_PHASES
    else:
        allowed = frozenset()
    return {phase: phase in allowed for phase in PHASES}


def _frontier_policy(exception: Mapping[str, Any]) -> dict[str, Any]:
    policy = {
        "schema_version": "stage1-frontier-runtime-policy/1.0",
        "assigned_worker_id": exception["assigned_worker"]["id"],
        "completion_probability": exception["completion_probability"],
        "attempt_limit": exception["attempt_limit"],
        "lease_expires_at": exception["lease_expires_at"],
        "budget": dict(exception["budget"]),
        "milestones": [dict(row) for row in exception["milestones"]],
        "validator": dict(exception["validator"]),
        "stop_conditions": list(exception["stop_conditions"]),
    }
    policy["policy_sha256"] = _sha256_bytes(
        json.dumps(
            policy, ensure_ascii=True, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    )
    return policy


def _invalid_projection(
    theorem_id: str,
    path: str,
    *,
    present: bool,
    receipt_sha256: str | None,
    reason_codes: list[str],
    receipt: Mapping[str, Any] | None = None,
    bootstrap_research: bool = False,
) -> dict[str, Any]:
    invalid_reason_codes = sorted(set(reason_codes))
    evidence_class = "unknown"
    disposition = "research_required"
    return {
        "receipt_path": path,
        "present": present,
        "valid": False,
        "theorem_id": theorem_id,
        "machine_evidence_class": evidence_class,
        "execution_disposition": disposition,
        # A genuinely absent receipt is the only synthesized bootstrap state:
        # discovery may create eligibility evidence, but proof work cannot run.
        # Once a receipt exists, malformed/stale evidence opens no phase at all.
        "phase_permissions": (
            {phase: phase in RESEARCH_PHASES for phase in PHASES}
            if bootstrap_research
            else _permissions(disposition, valid=False)
        ),
        "reason_codes": invalid_reason_codes,
        "receipt_sha256": receipt_sha256,
        "evidence_as_of": receipt.get("evidence_as_of") if receipt else None,
        "expires_at": receipt.get("expires_at") if receipt else None,
        "frontier_policy": None,
    }


def evaluate_target(
    repo_root: Path | str,
    theorem_id: str,
    *,
    as_of: datetime | None = None,
    expected_receipt_sha256: str | None = None,
    runtime_root: Path | str | None = None,
) -> dict[str, Any]:
    """Return a deterministic JSON-safe admission projection for one target.

    ``expected_receipt_sha256`` should be the receipt digest copied into the
    theorem-DAG projection.  Supplying it rejects a receipt changed since DAG
    generation without binding this evaluator to the DAG's own graph digest.
    """

    try:
        relative = receipt_relative_path(theorem_id)
    except EligibilityError:
        relative = f"Stage1_Instances/{theorem_id}/{RECEIPT_NAME}"
        return _invalid_projection(
            str(theorem_id), relative, present=False, receipt_sha256=None,
            reason_codes=["theorem_id_malformed"],
        )
    root = _repo_root(repo_root)
    try:
        is_member = theorem_id in _target_membership_ids(root)
    except EligibilityError as exc:
        return _invalid_projection(
            theorem_id, relative, present=False, receipt_sha256=None,
            reason_codes=[_reason_code(str(exc))],
        )
    if not is_member:
        return _invalid_projection(
            theorem_id, relative, present=False, receipt_sha256=None,
            reason_codes=["theorem_id_outside_frozen_stage1_target_membership"],
        )
    # Even receipt-free discovery is an authority-governed phase. A dirty,
    # missing, or independently rewritten schema must not leave a research
    # bootstrap lane open while the receipt validator itself is unavailable.
    try:
        _focus_schema(root)
    except EligibilityError as exc:
        return _invalid_projection(
            theorem_id, relative, present=False, receipt_sha256=None,
            reason_codes=[_reason_code(str(exc))],
        )
    path = root / relative
    if not path.is_file() or path.is_symlink():
        return _invalid_projection(
            theorem_id, relative, present=False, receipt_sha256=None,
            reason_codes=["receipt_missing"], bootstrap_research=True,
        )
    try:
        payload = path.read_bytes()
    except OSError:
        return _invalid_projection(
            theorem_id, relative, present=True, receipt_sha256=None,
            reason_codes=["receipt_unreadable"],
        )
    receipt_sha = _sha256_bytes(payload)
    if expected_receipt_sha256 is not None and (
        not SHA256_RE.fullmatch(expected_receipt_sha256)
        or receipt_sha != expected_receipt_sha256
    ):
        return _invalid_projection(
            theorem_id, relative, present=True, receipt_sha256=receipt_sha,
            reason_codes=["projection_receipt_digest_mismatch"],
        )
    def reject_nonfinite(value: str) -> NoReturn:
        raise ValueError(f"non-finite JSON number: {value}")

    try:
        receipt = json.loads(
            payload.decode("utf-8"), parse_constant=reject_nonfinite
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return _invalid_projection(
            theorem_id, relative, present=True, receipt_sha256=receipt_sha,
            reason_codes=["receipt_not_canonical_json"],
        )
    if not isinstance(receipt, dict):
        return _invalid_projection(
            theorem_id, relative, present=True, receipt_sha256=receipt_sha,
            reason_codes=["receipt_not_object"],
        )
    canonical = (
        json.dumps(receipt, ensure_ascii=True, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")
    reasons = [] if payload == canonical else ["receipt_not_canonical_json"]
    reasons.extend(_schema_errors(root, receipt))
    if reasons:
        return _invalid_projection(
            theorem_id, relative, present=True, receipt_sha256=receipt_sha,
            reason_codes=reasons, receipt=receipt,
        )
    try:
        _semantic_validate(
            root,
            theorem_id,
            receipt,
            as_of=_canonical_as_of(as_of),
            runtime_root=runtime_root,
            require_issuance=True,
        )
    except EligibilityError as exc:
        return _invalid_projection(
            theorem_id, relative, present=True, receipt_sha256=receipt_sha,
            reason_codes=[_reason_code(str(exc))], receipt=receipt,
        )

    disposition = str(receipt["execution_disposition"])
    return {
        "receipt_path": relative,
        "present": True,
        "valid": True,
        "theorem_id": theorem_id,
        "machine_evidence_class": receipt["machine_evidence_class"],
        "execution_disposition": disposition,
        "phase_permissions": _permissions(disposition, valid=True),
        "reason_codes": [f"admitted_{disposition}"],
        "receipt_sha256": receipt_sha,
        "evidence_as_of": receipt["evidence_as_of"],
        "expires_at": receipt["expires_at"],
        "frontier_policy": (
            _frontier_policy(receipt["frontier_exception"])
            if disposition == "frontier_exception"
            else None
        ),
    }


def _reason_code(message: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", message.lower()).strip("_")
    return value[:120] or "semantic_validation_failed"


def load_focus_eligibility(
    repo_root: Path | str,
    theorem_id: str,
    *,
    as_of: datetime | None = None,
    expected_projection_sha256: str | None = None,
    runtime_root: Path | str | None = None,
) -> dict[str, Any]:
    """Compatibility name for scheduler callers."""

    return evaluate_target(
        repo_root,
        theorem_id,
        as_of=as_of,
        expected_receipt_sha256=expected_projection_sha256,
        runtime_root=runtime_root,
    )


def phase_allowed(decision: Mapping[str, Any], phase: str) -> bool:
    if phase not in PHASES:
        return False
    permissions = decision.get("phase_permissions")
    allowed = isinstance(permissions, Mapping) and permissions.get(phase) is True
    if not allowed:
        return False
    if decision.get("valid") is True:
        return True
    return (
        decision.get("present") is False
        and decision.get("reason_codes") == ["receipt_missing"]
        and phase in RESEARCH_PHASES
    )


def require_phase_allowed(decision: Mapping[str, Any], phase: str) -> None:
    if not phase_allowed(decision, phase):
        theorem = decision.get("theorem_id", "unknown")
        reasons = ",".join(str(reason) for reason in decision.get("reason_codes", []))
        _fail(f"{theorem}/{phase} is not focus-eligible: {reasons or 'fail_closed'}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("theorem_id")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--phase", choices=PHASES)
    parser.add_argument("--expected-receipt-sha256")
    args = parser.parse_args()
    result = evaluate_target(
        args.repo_root,
        args.theorem_id,
        expected_receipt_sha256=args.expected_receipt_sha256,
    )
    print(json.dumps(result, ensure_ascii=True, indent=2))
    if args.phase and not phase_allowed(result, args.phase):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
