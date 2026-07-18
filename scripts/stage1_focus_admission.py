#!/usr/bin/env python3
"""Scheduler-owned issuance for Stage1 focus-admission receipts.

Workers may commit one theorem-owned proposal containing research facts.  This
module keeps authority in a separate scheduler pipeline:

1. read the proposal and every evidence byte exactly from authoritative HEAD;
2. build an immutable scheduler candidate and independently verify any claimed
   external Lean proof and kernel replay;
3. repeat verification under a distinct read-only reviewer principal; and
4. publish the derived focus receipt and regenerated theorem DAG as one
   rollback-journaled transaction.

The proposal is never itself an admission receipt.  In particular, it cannot
name the admission reviewer, scheduler owner, generated time, or final review
decision.
"""

from __future__ import annotations

import base64
import datetime as dt
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import tarfile
import tempfile
from typing import Any, Callable, Mapping, NoReturn, Sequence
from urllib.parse import unquote, urlparse

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


try:
    import stage1_focus_eligibility as focus_eligibility
except ModuleNotFoundError:
    _FOCUS_PATH = Path(__file__).with_name("stage1_focus_eligibility.py")
    _FOCUS_SPEC = importlib.util.spec_from_file_location(
        "stage1_focus_eligibility", _FOCUS_PATH
    )
    if _FOCUS_SPEC is None or _FOCUS_SPEC.loader is None:
        raise
    focus_eligibility = importlib.util.module_from_spec(_FOCUS_SPEC)
    _FOCUS_SPEC.loader.exec_module(focus_eligibility)

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


PROPOSAL_SCHEMA = "stage1-focus-admission-proposal/1.0"
DECISION_SCHEMA = "stage1-focus-admission-scheduler-decision/1.0"
CANDIDATE_SCHEMA = "stage1-focus-admission-candidate/1.0"
VERIFICATION_SCHEMA = "stage1-focus-admission-verification/1.0"
REVIEW_SCHEMA = "stage1-focus-admission-review/1.0"
ISSUANCE_SCHEMA = "stage1-focus-admission-issuance/2.0"
ISSUANCE_AUTHORITY_SCHEMA = "stage1-focus-admission-authority/2.0"
SIGNATURE_PAYLOAD_SCHEMA = "stage1-focus-admission-signature-payload/1.0"
DEFAULT_SCHEDULER_SIGNING_KEY = (
    Path.home() / ".config/awesome_theorems/stage1-focus-keys/scheduler.pem"
)
DEFAULT_REVIEWER_SIGNING_KEY = (
    Path.home() / ".config/awesome_theorems/stage1-focus-keys/reviewer.pem"
)
WAL_SCHEMA = "stage1-focus-admission-wal/1.0"
WAL_FIELDS = {"schema_version", "authority_revision", "snapshots"}
WAL_SNAPSHOT_FIELDS = {"path", "existed", "mode", "content_base64"}
PROPOSAL_NAME = "focus-admission-proposal.json"
THEOREM_RE = re.compile(r"^THM-M-[0-9]{4}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_OID_RE = re.compile(r"^[0-9a-f]{40,64}$")
ACTOR_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@-]{0,199}$")
UTC_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T.*Z$")
ALLOWED_ADMISSION_DECISIONS = {
    "organize_or_integrate": "admit_integration",
    "frontier_exception": "admit_frontier_exception",
    "research_required": "research_only",
    "defer_frontier": "defer",
    "exclude_scope": "exclude",
}
PROPOSAL_FIELDS = {
    "schema_version",
    "proposal_id",
    "theorem_id",
    "author",
    "submitted_at",
    "repository_base_revision",
    "evidence_as_of",
    "machine_evidence_class",
    "execution_disposition",
    "human_proof",
    "target_binding",
    "statement_binding",
    "machine_proof",
    "repository_gap",
    "evidence_bindings",
    "frontier_request",
    "invalidation_conditions",
}
DECISION_FIELDS = {
    "schema_version",
    "theorem_id",
    "authority_revision",
    "proposal_sha256",
    "issuer",
    "reviewer",
    "admission_decision",
    "expires_at",
    "human_source_authorization",
    "frontier_authorization",
}
HUMAN_SOURCE_AUTHORIZATION_FIELDS = {
    "path",
    "sha256",
    "review_sha256",
    "reviewer",
    "decision",
}
FRONTIER_REQUEST_FIELDS = {"root_obligation", "evidence"}
FRONTIER_AUTHORIZATION_FIELDS = {
    "assigned_worker",
    "estimator",
    "estimated_at",
    "estimation_method",
    "completion_probability",
    "budget",
    "milestones",
    "validator",
    "stop_conditions",
    "attempt_limit",
    "lease_expires_at",
}
REVIEW_FIELDS = {
    "schema_version",
    "candidate_sha256",
    "proposal_sha256",
    "receipt_facts_sha256",
    "theorem_id",
    "reviewer",
    "reviewed_at",
    "decision",
    "repository_access",
    "candidate_verification_sha256",
    "review_verification",
    "evidence_sha256s",
    "findings",
    "frontier_review_input",
    "receipt_generated_at",
    "unsigned_review_sha256",
    "receipt_payload_sha256",
    "reviewer_key_id",
    "reviewer_signature",
    "review_sha256",
}
FRONTIER_REVIEW_INPUT_SCHEMA = "stage1-frontier-independent-review-input/1.0"
FRONTIER_REVIEW_INPUT_FIELDS = {
    "schema_version", "candidate_sha256", "theorem_id", "reviewer",
    "authored_at", "decision", "assessed_completion_probability",
    "estimation_method_assessment", "comparables", "budget_assessment",
    "milestone_assessment", "validator_assessment", "stop_condition_assessment",
    "findings", "review_input_sha256",
}
PROHIBITED_LEAN_TOKENS = re.compile(
    r"(?m)(?:\bsorry\b|\badmit\b|\bsorryAx\b|^\s*axiom\b|^\s*unsafe\b)"
)
FOUNDATION_PROFILE_ID = "lean4-standard-foundation/1.0"
PERMITTED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
MAX_PROPOSAL_BYTES = 4 * 1024 * 1024
MAX_REVIEW_OUTPUT_BYTES = 16 * 1024 * 1024
MAX_WAL_BYTES = 32 * 1024 * 1024
CANONICAL_RUNTIME_RELATIVE = PurePosixPath(".cron/stage1-v2-app-server")
KERNEL_REPLAY_TIMEOUT_SECONDS = 3600
AUTHORITY_RESULT_SCHEMA = "stage1-focus-kernel-authority-result/1.0"
LOCAL_TARGET_RESULT_SCHEMA = "stage1-focus-local-target-authority-result/1.0"
TRANSPORT_AUTHORITY_RESULT_SCHEMA = (
    "stage1-focus-machine-transport-authority-result/1.0"
)
TRANSPORT_PROVIDER_MODULE = "Stage1FocusTransportProvider"
TRANSPORT_PROVIDER_SOURCE = f"{TRANSPORT_PROVIDER_MODULE}.lean"
TRANSPORT_PROVIDER_OLEAN = f"{TRANSPORT_PROVIDER_MODULE}.olean"
TRANSPORT_REPLAY_SOURCE = "Stage1FocusMachineTransport.lean"
TRANSPORT_DEPENDENCY_PREFIX = "STAGE1_TRANSPORT_PROVIDER_DEPENDENCY:"
TRANSPORT_VALIDATOR_SOURCE = b'''#!/usr/bin/env python3
"""Scheduler-owned deterministic Stage1 transport artifact validator."""
import argparse
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--transport-artifact", required=True)
args = parser.parse_args()
path = Path(args.transport_artifact)
data = path.read_bytes()
print(json.dumps({
    "artifact_sha256": hashlib.sha256(data).hexdigest(),
    "status": "transport_artifact_bound",
}, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
'''
HUMAN_SOURCE_REVIEW_SCHEMA = "stage1-human-source-review/1.0"
HUMAN_SOURCE_REVIEW_FIELDS = {
    "schema_version",
    "theorem_id",
    "source",
    "publication_timestamp",
    "statement_fingerprint",
    "statement_boundary",
    "statement_crosswalk",
    "hypotheses",
    "publication_status",
    "license",
    "reviewer",
    "reviewed_at",
    "decision",
    "review_sha256",
}
EXTERNAL_PROVENANCE_SCHEMA = "stage1-external-proof-provenance/1.0"
EXTERNAL_PROVENANCE_ROLE = "pre_stage1_machine_provenance"
TIMESTAMP_TOKEN_SCHEMA = "stage1-independent-publication-timestamp/1.0"
TIMESTAMP_SIGNATURE_PAYLOAD_SCHEMA = (
    "stage1-independent-publication-timestamp-signature-payload/1.0"
)
# The first committed Stage1 v2 authority is the latest instant at which an
# unintegrated artifact can have existed independently of this program.
STAGE1_PROVENANCE_CUTOFF = dt.datetime(
    2026, 7, 15, 20, 32, 21, tzinfo=dt.timezone.utc
)
EXTERNAL_PROVENANCE_FIELDS = {
    "schema_version",
    "theorem_id",
    "source",
    "publication",
    "reviewer",
    "reviewed_at",
    "decision",
    "provenance_sha256",
}
AUTHORITY_RESULT_FIELDS = {
    "schema_version",
    "formal_system",
    "toolchain",
    "dependency_lock_sha256",
    "file_path",
    "file_sha256",
    "module",
    "declaration",
    "declaration_type_sha256",
    "terminal_proof_body_sha256",
    "kernel_exit_code",
    "placeholder_free",
    "unsafe_free",
    "oracle_free",
    "undeclared_axioms_free",
    "permitted_axioms",
    "trust_audit_output_sha256",
    "replay_authority",
}
LOCAL_TARGET_RESULT_FIELDS = {
    "schema_version",
    "formal_system",
    "repository_revision",
    "file_path",
    "file_sha256",
    "declaration",
    "declaration_type_sha256",
    "toolchain",
    "dependency_lock_sha256",
    "kernel_exit_code",
    "permitted_axioms",
    "trust_audit_output_sha256",
    "replay_authority",
}


class AdmissionError(RuntimeError):
    """The requested admission transition is not proven."""


def _fail(message: str) -> NoReturn:
    raise AdmissionError(message)


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _pretty_json(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=True, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")


def _load_signing_key(path: Path | str, label: str) -> Ed25519PrivateKey:
    value = Path(path).absolute()
    if (
        value.is_symlink()
        or not value.is_file()
        or value.stat().st_mode & 0o777 != 0o600
        or (
            value.stat().st_uid != os.geteuid()
            and not (
                label == "independent reviewer focus signing key"
                and os.geteuid() != 0
                and value.stat().st_uid == 0
            )
        )
    ):
        _fail(f"{label} must be an owner-controlled regular file with mode 0600")
    try:
        key = serialization.load_pem_private_key(value.read_bytes(), password=None)
    except (OSError, ValueError, TypeError) as exc:
        raise AdmissionError(f"{label} is unreadable or invalid") from exc
    if not isinstance(key, Ed25519PrivateKey):
        _fail(f"{label} is not an Ed25519 private key")
    return key


def _signing_key_path(
    explicit: Path | str | None, env_name: str, default: Path
) -> Path:
    raw = explicit if explicit is not None else os.environ.get(env_name, str(default))
    if not isinstance(raw, (str, os.PathLike)) or not os.fspath(raw):
        _fail(f"{env_name} does not name a signing key file")
    return Path(os.fspath(raw)).absolute()


def _digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _embedded_digest(value: Mapping[str, Any], field: str, label: str) -> str:
    claimed = value.get(field)
    if not isinstance(claimed, str) or SHA256_RE.fullmatch(claimed) is None:
        _fail(f"{label} lacks a canonical {field}")
    unhashed = dict(value)
    del unhashed[field]
    if _digest(_canonical_json(unhashed)) != claimed:
        _fail(f"{label} {field} does not bind its content")
    return claimed


def _with_digest(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result[field] = _digest(_canonical_json(result))
    return result


def _parse_json(data: bytes, label: str) -> dict[str, Any]:
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
            data.decode("utf-8"),
            object_pairs_hook=reject_duplicates,
            parse_constant=reject_nonfinite,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AdmissionError(f"{label} is not canonical UTF-8 JSON") from exc
    if not isinstance(value, dict):
        _fail(f"{label} must be a JSON object")
    return value


def _safe_relative(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        _fail(f"{label} is not a safe repository-relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or path.as_posix() != value or any(
        component in {"", ".", ".."} for component in path.parts
    ):
        _fail(f"{label} is not a canonical repository-relative path")
    return value


def _actor(value: Any, label: str, *, role: str | None = None) -> dict[str, str]:
    if not isinstance(value, dict) or set(value) != {"id", "role"}:
        _fail(f"{label} is malformed")
    actor_id = value.get("id")
    actor_role = value.get("role")
    if (
        not isinstance(actor_id, str)
        or ACTOR_ID_RE.fullmatch(actor_id) is None
        or not isinstance(actor_role, str)
        or not actor_role
        or (role is not None and actor_role != role)
    ):
        _fail(f"{label} is malformed")
    return {"id": actor_id, "role": actor_role}


def _distinct(first: Mapping[str, Any], second: Mapping[str, Any], label: str) -> None:
    if first.get("id") == second.get("id"):
        _fail(f"{label} must be independent")


def _timestamp(value: Any, label: str) -> dt.datetime:
    if not isinstance(value, str) or UTC_TIMESTAMP_RE.fullmatch(value) is None:
        _fail(f"{label} must be a UTC timestamp ending in Z")
    try:
        parsed = dt.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise AdmissionError(f"{label} is malformed") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != dt.timedelta(0):
        _fail(f"{label} is not UTC")
    return parsed.astimezone(dt.timezone.utc)


def _utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _utc_text(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z"
    )


def _run_git(
    root: Path,
    argv: Sequence[str],
    *,
    input_bytes: bytes | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *argv],
        cwd=root,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        _fail(f"git {' '.join(argv)} failed: {detail or 'unknown Git error'}")
    return result


def _git_text(root: Path, *argv: str) -> str:
    try:
        return _run_git(root, argv).stdout.decode("ascii", "strict").strip()
    except UnicodeDecodeError as exc:
        raise AdmissionError("Git returned a non-ASCII identity") from exc


def _root(root: Path | str) -> Path:
    result = Path(root).absolute()
    current = Path(result.anchor or "/")
    for component in result.parts[1:]:
        current /= component
        if current.is_symlink():
            _fail("repository root traverses a symlink")
    if not result.is_dir():
        _fail("repository root is missing")
    top = Path(_git_text(result, "rev-parse", "--show-toplevel")).absolute()
    if top != result:
        _fail("repository root is not the current Git worktree root")
    return result


def _repo_owner(root: Path) -> int:
    metadata = os.stat(root, follow_symlinks=False)
    if not stat.S_ISDIR(metadata.st_mode):
        _fail("repository root is not a directory")
    return metadata.st_uid


def _canonical_runtime(
    root: Path,
    runtime_root: Path | str,
    *,
    required_descendants: Sequence[PurePosixPath | str] = (),
    allowed_caller_uids: set[int] | None = None,
) -> Path:
    """Bind authority-bearing runtime input to the repository's fixed store."""
    runtime = Path(runtime_root).absolute()
    expected = root.joinpath(*CANONICAL_RUNTIME_RELATIVE.parts)
    if runtime != expected:
        _fail("focus admission runtime is not the canonical repository runtime")
    owner = _repo_owner(root)
    callers = {owner} if allowed_caller_uids is None else set(allowed_caller_uids)
    if os.geteuid() not in callers:
        _fail("focus admission caller is not an authorized runtime principal")

    # Walk from the already no-symlink-validated repository root.  lstat each
    # component instead of resolve(), which would silently follow an attacker.
    requested = {
        PurePosixPath(".cron"),
        CANONICAL_RUNTIME_RELATIVE,
        *(
            CANONICAL_RUNTIME_RELATIVE / PurePosixPath(value)
            for value in required_descendants
        ),
    }
    for relative in sorted(requested, key=lambda value: len(value.parts)):
        if relative.is_absolute() or ".." in relative.parts:
            _fail("focus admission runtime lineage is malformed")
        current = root
        for component in relative.parts:
            current /= component
            try:
                metadata = os.stat(current, follow_symlinks=False)
            except OSError as exc:
                raise AdmissionError("focus admission runtime lineage is missing") from exc
            if (
                not stat.S_ISDIR(metadata.st_mode)
                or metadata.st_uid != owner
                or stat.S_IMODE(metadata.st_mode) & 0o022
            ):
                _fail("focus admission runtime lineage is not owner-controlled")
    return runtime


def _runtime_relative(path: Path, runtime: Path, label: str) -> PurePosixPath:
    absolute = path.absolute()
    try:
        relative = absolute.relative_to(runtime)
    except ValueError as exc:
        raise AdmissionError(f"{label} path is not scheduler-canonical") from exc
    result = PurePosixPath(relative.as_posix())
    if not result.parts or any(component in {"", ".", ".."} for component in result.parts):
        _fail(f"{label} path is not scheduler-canonical")
    return result


def _runtime_parent_relative(value: PurePosixPath | str) -> PurePosixPath:
    result = PurePosixPath(value)
    if result.as_posix() in {"", "."}:
        return PurePosixPath()
    return result


def _read_secure_runtime_file(
    root: Path,
    runtime: Path,
    path: Path,
    *,
    expected_parent: PurePosixPath | str,
    label: str,
    max_bytes: int,
    allowed_owner_uids: set[int] | None = None,
    allowed_caller_uids: set[int] | None = None,
) -> bytes:
    """Read one runtime leaf through nofollow directory/file descriptors."""
    parent_relative = _runtime_parent_relative(expected_parent)
    relative = _runtime_relative(path, runtime, label)
    if PurePosixPath(*relative.parts[:-1]) != parent_relative:
        _fail(f"{label} path is not scheduler-canonical")
    descendants: tuple[PurePosixPath, ...] = (
        () if not parent_relative.parts else (parent_relative,)
    )
    _canonical_runtime(
        root,
        runtime,
        required_descendants=descendants,
        allowed_caller_uids=allowed_caller_uids,
    )
    owner = _repo_owner(root)
    permitted = {owner} if allowed_owner_uids is None else set(allowed_owner_uids)
    if not permitted or any(not isinstance(uid, int) or uid < 0 for uid in permitted):
        _fail(f"{label} owner policy is malformed")

    directory = os.open(runtime, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    descriptor: int | None = None
    try:
        for component in relative.parts[:-1]:
            try:
                child = os.open(
                    component,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=directory,
                )
            except OSError as exc:
                raise AdmissionError(f"{label} has an unsafe runtime ancestor") from exc
            metadata = os.fstat(child)
            if (
                not stat.S_ISDIR(metadata.st_mode)
                or metadata.st_uid != owner
                or stat.S_IMODE(metadata.st_mode) & 0o022
            ):
                os.close(child)
                _fail(f"{label} runtime lineage is not owner-controlled")
            os.close(directory)
            directory = child
        try:
            descriptor = os.open(
                relative.parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory
            )
        except OSError as exc:
            raise AdmissionError(f"{label} is missing or unsafe") from exc
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_uid not in permitted
            or stat.S_IMODE(before.st_mode) != 0o600
            or before.st_nlink != 1
            or before.st_size > max_bytes
        ):
            _fail(f"{label} is not an owner-controlled mode 0600 regular file")
        chunks: list[bytes] = []
        remaining = max_bytes + 1
        while remaining > 0:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        if remaining == 0 and os.read(descriptor, 1):
            _fail(f"{label} exceeds its byte limit")
        after = os.fstat(descriptor)
        if (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
            before.st_ctime_ns,
        ) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        ):
            _fail(f"{label} changed while being read")
        return b"".join(chunks)
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(directory)


def _read_regular(root: Path, relative: str, label: str) -> bytes:
    relative = _safe_relative(relative, label)
    components = PurePosixPath(relative).parts
    directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in components[:-1]:
            try:
                child = os.open(
                    component,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=directory,
                )
            except OSError as exc:
                raise AdmissionError(f"{label} has an unsafe parent") from exc
            os.close(directory)
            directory = child
        try:
            descriptor = os.open(
                components[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory
            )
        except OSError as exc:
            raise AdmissionError(f"{label} is missing or unsafe") from exc
        try:
            before = os.fstat(descriptor)
            if not stat.S_ISREG(before.st_mode) or before.st_size > MAX_PROPOSAL_BYTES:
                _fail(f"{label} is not a bounded regular file")
            chunks: list[bytes] = []
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            after = os.fstat(descriptor)
            if (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            ) != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            ):
                _fail(f"{label} changed while being read")
            return b"".join(chunks)
        finally:
            os.close(descriptor)
    finally:
        os.close(directory)


def _head_blob(root: Path, head: str, relative: str, label: str) -> tuple[bytes, str]:
    relative = _safe_relative(relative, label)
    rows = [
        row
        for row in _run_git(root, ["ls-tree", "-z", head, "--", relative]).stdout.split(
            b"\0"
        )
        if row
    ]
    if len(rows) != 1:
        _fail(f"{label} is not exactly one authoritative HEAD path")
    try:
        metadata, raw_path = rows[0].split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split()
        tracked_path = raw_path.decode("utf-8")
    except (UnicodeDecodeError, ValueError) as exc:
        raise AdmissionError(f"{label} has malformed Git metadata") from exc
    if (
        tracked_path != relative
        or kind != "blob"
        or mode not in {"100644", "100755"}
        or GIT_OID_RE.fullmatch(oid) is None
    ):
        _fail(f"{label} is not a regular nonsymlink HEAD blob")
    data = _run_git(root, ["cat-file", "blob", oid]).stdout
    if _read_regular(root, relative, label) != data:
        _fail(f"{label} worktree bytes disagree with authoritative HEAD")
    return data, oid


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        temporary.unlink(missing_ok=True)


def _immutable_write(
    path: Path,
    value: Mapping[str, Any],
    label: str,
    *,
    owner_uid: int | None = None,
) -> None:
    payload = _pretty_json(value)
    if path.exists() or path.is_symlink():
        if path.is_symlink() or not path.is_file() or path.read_bytes() != payload:
            _fail(f"immutable {label} conflicts with existing bytes")
        return
    _atomic_write(path, payload)
    path.chmod(0o600)
    if owner_uid is not None and path.stat(follow_symlinks=False).st_uid != owner_uid:
        try:
            os.chown(path, owner_uid, -1, follow_symlinks=False)
        except OSError as exc:
            raise AdmissionError(f"immutable {label} has the wrong owner") from exc


def proposal_relative_path(theorem_id: str) -> str:
    if not isinstance(theorem_id, str) or THEOREM_RE.fullmatch(theorem_id) is None:
        _fail("proposal theorem_id is malformed")
    return f"Stage1_Instances/{theorem_id}/{PROPOSAL_NAME}"


def _load_proposal(root: Path, proposal_path: Path | str) -> tuple[dict[str, Any], str, str]:
    path = Path(proposal_path)
    try:
        relative = path.relative_to(root).as_posix() if path.is_absolute() else path.as_posix()
    except ValueError as exc:
        raise AdmissionError("proposal path escapes the repository") from exc
    relative = _safe_relative(relative, "focus proposal")
    data, _ = _head_blob(root, _git_text(root, "rev-parse", "HEAD^{commit}"), relative, "focus proposal")
    proposal = _parse_json(data, "focus proposal")
    if data != _pretty_json(proposal):
        _fail("focus proposal is not canonical pretty JSON")
    if set(proposal) != PROPOSAL_FIELDS or proposal.get("schema_version") != PROPOSAL_SCHEMA:
        _fail("focus proposal fields or schema are not canonical")
    theorem_id = proposal.get("theorem_id")
    if relative != proposal_relative_path(str(theorem_id)):
        _fail("focus proposal path does not match its theorem owner")
    author = _actor(proposal.get("author"), "proposal author", role="research_worker")
    if author["id"] == "scheduler_master_lane":
        _fail("worker proposal impersonates the scheduler")
    proposal_id = proposal.get("proposal_id")
    if not isinstance(proposal_id, str) or ACTOR_ID_RE.fullmatch(proposal_id) is None:
        _fail("focus proposal id is malformed")
    base = proposal.get("repository_base_revision")
    if not isinstance(base, str) or GIT_OID_RE.fullmatch(base) is None:
        _fail("focus proposal repository base is malformed")
    resolved = _git_text(root, "rev-parse", "--verify", f"{base}^{{commit}}")
    if resolved != base or _run_git(
        root, ["merge-base", "--is-ancestor", base, "HEAD"], check=False
    ).returncode:
        _fail("focus proposal repository base is not an authoritative ancestor")
    submitted = _timestamp(proposal.get("submitted_at"), "proposal submitted_at")
    evidence_as_of = _timestamp(proposal.get("evidence_as_of"), "proposal evidence_as_of")
    if evidence_as_of > submitted or submitted > _utc_now():
        _fail("focus proposal timestamps are future-dated or out of order")
    if proposal.get("execution_disposition") not in ALLOWED_ADMISSION_DECISIONS:
        _fail("focus proposal disposition is unsupported")
    return proposal, _digest(data), relative


def _verify_bound_evidence(
    root: Path, head: str, theorem_id: str, bindings: Any
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    if not isinstance(bindings, list):
        _fail("proposal evidence bindings are missing")
    verified: list[dict[str, Any]] = []
    digests: dict[str, str] = {}
    seen: set[tuple[str, str]] = set()
    owner = f"Stage1_Instances/{theorem_id}/"
    forbidden = f"{owner}{focus_eligibility.RECEIPT_NAME}"
    for index, raw in enumerate(bindings):
        if not isinstance(raw, dict):
            _fail(f"proposal evidence binding {index} is malformed")
        path = _safe_relative(raw.get("path"), f"proposal evidence binding {index}")
        digest = raw.get("sha256")
        role = raw.get("role")
        if (
            not path.startswith(owner)
            or path == forbidden
            or not isinstance(digest, str)
            or SHA256_RE.fullmatch(digest) is None
            or not isinstance(role, str)
            or not role
        ):
            _fail("proposal evidence is not a theorem-owned content binding")
        data, oid = _head_blob(root, head, path, f"proposal evidence {index}")
        if _digest(data) != digest:
            _fail(f"proposal evidence digest is stale: {path}")
        key = (role, path)
        if key in seen:
            _fail("proposal evidence contains a duplicate role/path binding")
        seen.add(key)
        verified.append({**raw, "git_blob": oid})
        if path in digests and digests[path] != digest:
            _fail("proposal evidence binds one path to conflicting digests")
        digests[path] = digest
    return verified, dict(sorted(digests.items()))


def _human_source_review(
    root: Path,
    head: str,
    receipt_facts: Mapping[str, Any],
    *,
    proposal_author: Mapping[str, Any],
    scheduler_issuer: Mapping[str, Any],
    admission_reviewer: Mapping[str, Any],
    authorization: Any,
) -> dict[str, Any] | None:
    """Load a typed independent source review instead of trusting proposal labels."""
    if receipt_facts.get("execution_disposition") not in {
        "organize_or_integrate",
        "frontier_exception",
    }:
        if authorization is not None:
            _fail("non-exact admission carries human source authority")
        return None
    if (
        not isinstance(authorization, Mapping)
        or set(authorization) != HUMAN_SOURCE_AUTHORIZATION_FIELDS
        or authorization.get("decision") != "accepted"
    ):
        _fail("exact admission lacks scheduler-bound human source authority")
    theorem_id = str(receipt_facts.get("theorem_id"))
    bindings = [
        row
        for row in receipt_facts.get("evidence_bindings", [])
        if isinstance(row, Mapping) and row.get("role") == "human_source_review"
    ]
    if len(bindings) != 1:
        _fail("admission requires exactly one typed human source review")
    binding = bindings[0]
    path = _safe_relative(binding.get("path"), "human source review")
    data, _ = _head_blob(root, head, path, "human source review")
    if _digest(data) != binding.get("sha256"):
        _fail("human source review digest is stale")
    review = _parse_json(data, "human source review")
    if data != _pretty_json(review):
        _fail("human source review is not canonical pretty JSON")
    if (
        set(review) != HUMAN_SOURCE_REVIEW_FIELDS
        or review.get("schema_version") != HUMAN_SOURCE_REVIEW_SCHEMA
        or review.get("theorem_id") != theorem_id
    ):
        _fail("human source review fields, schema, or theorem binding are invalid")
    _embedded_digest(review, "review_sha256", "human source review")
    reviewer = _actor(
        review.get("reviewer"), "human source reviewer", role="independent_reviewer"
    )
    _distinct(reviewer, proposal_author, "human source reviewer")
    _distinct(reviewer, scheduler_issuer, "human source reviewer")
    _distinct(reviewer, admission_reviewer, "human source reviewer")
    human = receipt_facts.get("human_proof")
    source = human.get("source") if isinstance(human, Mapping) else None
    if not isinstance(source, Mapping):
        _fail("human source review lacks an enclosing accepted source")
    reviewed_at = _timestamp(review.get("reviewed_at"), "human source reviewed_at")
    evidence_as_of = _timestamp(
        receipt_facts.get("evidence_as_of"), "evidence_as_of"
    )
    if reviewed_at > evidence_as_of:
        _fail("human source review postdates the evidence snapshot")
    reviewed_source = review.get("source")
    if not isinstance(reviewed_source, Mapping) or set(reviewed_source) != {
        "citation",
        "locator",
        "immutable_id",
        "artifact_path",
        "content_sha256",
    }:
        _fail("human source review lacks a canonical immutable source binding")
    artifact_path = _safe_relative(
        reviewed_source.get("artifact_path"), "reviewed human source"
    )
    if not artifact_path.startswith(f"Stage1_Instances/{theorem_id}/"):
        _fail("reviewed human source is not theorem-owned")
    source_data, _ = _head_blob(root, head, artifact_path, "reviewed human source")
    if _digest(source_data) != reviewed_source.get("content_sha256"):
        _fail("reviewed human source bytes do not match their immutable identity")
    statement_crosswalk = review.get("statement_crosswalk")
    statement_fingerprint = review.get("statement_fingerprint")
    if (
        not isinstance(statement_crosswalk, Mapping)
        or set(statement_crosswalk) != {
            "source_artifact_sha256",
            "locator",
            "boundary",
            "hypotheses",
            "statement_fingerprint",
            "target_declaration_type_sha256",
            "relation",
        }
        or statement_crosswalk.get("source_artifact_sha256") != _digest(source_data)
        or statement_crosswalk.get("locator") != reviewed_source.get("locator")
        or statement_crosswalk.get("boundary") != review.get("statement_boundary")
        or statement_crosswalk.get("hypotheses") != review.get("hypotheses")
        or statement_crosswalk.get("statement_fingerprint") != statement_fingerprint
        or statement_crosswalk.get("target_declaration_type_sha256")
        != receipt_facts.get("target_binding", {}).get("declaration_type_sha256")
        or statement_crosswalk.get("relation") != "exact"
    ):
        _fail("human source review lacks an exact structured statement crosswalk")
    timestamp_subject = {
        "kind": "human_proof_source",
        "immutable_id": reviewed_source.get("immutable_id"),
        "citation": reviewed_source.get("citation"),
        "locator": reviewed_source.get("locator"),
        "artifact_sha256": _digest(source_data),
        "statement_fingerprint": statement_fingerprint,
        "statement_boundary": review.get("statement_boundary"),
        "hypotheses": review.get("hypotheses"),
    }
    timestamp = focus_eligibility._validate_independent_timestamp(
        root,
        review.get("publication_timestamp"),
        expected_subject=timestamp_subject,
        cutoff=None,
        forbidden_principals={
            str(proposal_author.get("id")),
            str(scheduler_issuer.get("id")),
            str(admission_reviewer.get("id")),
            str(reviewer.get("id")),
        },
        label="human proof publication timestamp",
    )
    if reviewed_at < _timestamp(timestamp["issued_at"], "human publication timestamp"):
        _fail("human source review predates its independently timestamped publication")
    source_identity = {
        key: source.get(key)
        for key in ("citation", "locator", "immutable_id", "content_sha256")
    }
    reviewed_identity = {
        key: reviewed_source.get(key)
        for key in ("citation", "locator", "immutable_id", "content_sha256")
    }
    expected_license = source.get("license")
    if (
        review.get("decision") != "accepted"
        or reviewed_identity != source_identity
        or review.get("statement_fingerprint") != human.get("statement_fingerprint")
        or review.get("statement_fingerprint")
        != receipt_facts.get("statement_binding", {}).get(
            "human_statement_fingerprint"
        )
        or review.get("statement_boundary") != source.get("proof_scope")
        or review.get("hypotheses") != source.get("hypotheses")
        or review.get("publication_status") != source.get("publication_status")
        or review.get("license") != expected_license
        or source.get("accepted_by") != reviewer
        or source.get("accepted_at") != review.get("reviewed_at")
        or authorization.get("path") != path
        or authorization.get("sha256") != binding.get("sha256")
        or authorization.get("review_sha256") != review.get("review_sha256")
        or authorization.get("reviewer") != reviewer
        or not isinstance(expected_license, Mapping)
        or expected_license.get("reviewed_for_use") is not True
        or not str(expected_license.get("identifier", "")).strip()
    ):
        _fail(
            "human source review does not independently bind the immutable source, "
            "exact statement boundary, accepted status, and license"
        )
    return {
        "path": path,
        "sha256": binding["sha256"],
        "review_sha256": review["review_sha256"],
        "source_artifact_path": artifact_path,
        "source_content_sha256": reviewed_source["content_sha256"],
        "publication_timestamp": timestamp,
        "statement_crosswalk": dict(statement_crosswalk),
        "reviewer": reviewer,
        "reviewed_at": review["reviewed_at"],
        "decision": review["decision"],
    }


def _require_existing_receipt_issued(
    root: Path, runtime: Path, head: str, theorem_id: str
) -> None:
    """Reject a receipt introduced outside a completed scheduler transaction."""
    relative = focus_eligibility.receipt_relative_path(theorem_id)
    receipt_path = root / relative
    tracked = bool(
        _run_git(root, ["ls-tree", "-z", head, "--", relative]).stdout
    )
    if not tracked:
        if receipt_path.exists() or receipt_path.is_symlink():
            _fail("existing focus receipt is not backed by a scheduler issuance")
        return
    data, _ = _head_blob(root, head, relative, "existing focus receipt")
    try:
        receipt = _parse_json(data, "existing focus receipt")
        focus_eligibility.validate_receipt(
            root,
            theorem_id,
            receipt,
            runtime_root=runtime,
            require_issuance=True,
        )
    except (AdmissionError, focus_eligibility.EligibilityError) as exc:
        raise AdmissionError(
            "existing focus receipt is not backed by a scheduler issuance; "
            "durable embedded authority is missing or invalid"
        ) from exc


def _decision(
    value: Mapping[str, Any],
    *,
    theorem_id: str,
    authority_revision: str,
    proposal_sha256: str,
    proposal_author: Mapping[str, Any],
) -> dict[str, Any]:
    decision = dict(value)
    if set(decision) != DECISION_FIELDS or decision.get("schema_version") != DECISION_SCHEMA:
        _fail("scheduler admission decision fields or schema are not canonical")
    if (
        decision.get("theorem_id") != theorem_id
        or decision.get("authority_revision") != authority_revision
        or decision.get("proposal_sha256") != proposal_sha256
    ):
        _fail("scheduler admission decision is stale or targets another proposal")
    issuer = _actor(decision.get("issuer"), "admission issuer", role="scheduler_master_lane")
    reviewer = _actor(
        decision.get("reviewer"), "designated admission reviewer", role="independent_reviewer"
    )
    _distinct(proposal_author, reviewer, "proposal reviewer")
    _distinct(issuer, reviewer, "admission reviewer")
    expires = _timestamp(decision.get("expires_at"), "admission expires_at")
    if expires <= _utc_now():
        _fail("scheduler admission decision is expired")
    return decision


def _declaration_region(data: bytes, declaration: str) -> tuple[str, str]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AdmissionError("external Lean source is not UTF-8") from exc
    short = declaration.rsplit(".", 1)[-1]
    start = re.search(
        rf"(?m)^\s*(?:theorem|lemma|opaque|def)\s+{re.escape(short)}\b", text
    )
    if start is None:
        _fail("external source does not contain the claimed declaration")
    tail = text[start.start() :]
    next_declaration = re.search(
        r"(?m)^\s*(?:theorem|lemma|opaque|def|namespace|end)\s+", tail[start.end() - start.start() :]
    )
    end = len(tail)
    if next_declaration is not None:
        end = start.end() - start.start() + next_declaration.start()
    region = tail[:end].encode("utf-8")
    return _digest(region), text


def _dependency_identity(checkout: Path) -> tuple[str, str]:
    toolchain_path = checkout / "lean-toolchain"
    if not toolchain_path.is_file() or toolchain_path.is_symlink():
        _fail("Lean source lacks a regular pinned lean-toolchain")
    toolchain = toolchain_path.read_text(encoding="utf-8").strip()
    if not toolchain:
        _fail("Lean source toolchain pin is empty")
    lock = checkout / "lake-manifest.json"
    dependency = lock if lock.is_file() and not lock.is_symlink() else toolchain_path
    return toolchain, _digest(dependency.read_bytes())


def _repository_replay_authority(root: Path, revision: str) -> dict[str, Any]:
    """Build the same full Lean authority snapshot used at master acceptance."""

    try:
        authority, _toolchain, _cache = (
            stage1_lean_authority.build_repository_lean_authority(
                root, authority_revision=revision
            )
        )
    except Exception as exc:
        # Do not leak an acceptance-module exception type through this API.
        raise AdmissionError(f"pinned Lean replay authority is invalid: {exc}") from exc
    if not isinstance(authority, dict):
        _fail("pinned Lean replay authority is malformed")
    return authority


def _pinned_manifest_provider(
    root: Path,
    authority_revision: str,
    source: Mapping[str, Any],
) -> dict[str, str]:
    """Resolve one machine source to the exact repository Lake lock entry."""

    manifest_path = "Formalizations/Lean/lake-manifest.json"
    manifest_bytes = _head_blob(
        root, authority_revision, manifest_path, "repository Lake manifest"
    )[0]
    manifest = _parse_json(manifest_bytes, "repository Lake manifest")
    packages = manifest.get("packages")
    repository = source.get("repository")
    revision = source.get("revision")
    if not isinstance(packages, list):
        _fail("repository Lake manifest package list is malformed")

    def canonical_remote(value: Any) -> str | None:
        if not isinstance(value, str) or not value:
            return None
        normalized = value.rstrip("/")
        if normalized.endswith(".git"):
            normalized = normalized[:-4]
        return normalized

    expected_remote = canonical_remote(repository)
    matches = [
        row
        for row in packages
        if isinstance(row, Mapping)
        and canonical_remote(row.get("url")) == expected_remote
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
        "repository": str(repository),
        "revision": str(revision),
        "manifest_sha256": _digest(manifest_bytes),
    }


def _require_root_lake_declaration(
    root: Path, authority_revision: str, provider: Mapping[str, str]
) -> None:
    """Bind the selected manifest row to the tracked root Lake dependency."""

    relative = "Formalizations/Lean/lakefile.lean"
    data = _head_blob(root, authority_revision, relative, "repository Lakefile")[0]
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AdmissionError("repository Lakefile is not UTF-8") from exc
    name = re.escape(provider["package_name"])
    repository = re.escape(provider["repository"])
    revision = re.escape(provider["revision"])
    declaration = re.compile(
        rf"(?m)^require[ \t]+{name}[ \t]+from[ \t]+git[ \t]*\n"
        rf"[ \t]+\"{repository}\"[ \t]+@[ \t]+\"{revision}\"[ \t]*$"
    )
    if len(declaration.findall(text)) != 1:
        _fail("pinned provider is not declared exactly in the tracked root Lakefile")


def _canonical_git_remote(value: Any) -> str | None:
    """Canonicalize common local, file, HTTPS, SSH and scp Git identities."""

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
        return normalized[:-4] if normalized.endswith(".git") else normalized.rstrip("/")
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
    identities = {_canonical_git_remote(str(root.resolve()))}
    result = _run_git(root, ["remote", "-v"], check=False)
    if result.returncode == 0:
        for row in result.stdout.decode("utf-8", "replace").splitlines():
            fields = row.split()
            if len(fields) >= 2:
                identities.add(_canonical_git_remote(fields[1]))
    return {identity for identity in identities if identity is not None}


def _git_history_identity(root: Path, *revisions: str) -> tuple[set[str], set[str]]:
    result = _run_git(root, ["rev-list", "--objects", *revisions], check=False)
    if result.returncode:
        _fail("Git object history cannot be inspected")
    commits: set[str] = set()
    trees: set[str] = set()
    for row in result.stdout.decode("ascii", "strict").splitlines():
        oid = row.split(" ", 1)[0]
        if GIT_OID_RE.fullmatch(oid) is None:
            _fail("Git object history contains a malformed identity")
        kind = _run_git(root, ["cat-file", "-t", oid], check=False)
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
    candidate = _canonical_git_remote(repository)
    if candidate is None:
        _fail("external source repository identity is not canonical")
    candidates = {candidate}
    if checkout is not None:
        remotes = _run_git(checkout, ["remote", "-v"], check=False)
        if remotes.returncode:
            _fail("external source remotes cannot be inspected")
        for row in remotes.stdout.decode("utf-8", "replace").splitlines():
            fields = row.split()
            if len(fields) >= 2:
                identity = _canonical_git_remote(fields[1])
                if identity is not None:
                    candidates.add(identity)
    if authoritative & candidates:
        _fail(
            "exact external source is the authoritative repository or a remote alias/mirror"
        )
    if checkout is None:
        return
    candidate_revision = revision or _git_text(checkout, "rev-parse", "HEAD^{commit}")
    if GIT_OID_RE.fullmatch(candidate_revision) is None:
        _fail("external source revision is not a canonical Git object identity")
    authoritative_commits, authoritative_trees = _git_history_identity(root, "--all")
    candidate_commits, candidate_trees = _git_history_identity(checkout, candidate_revision)
    shared = (authoritative_commits & candidate_commits) | (
        authoritative_trees & candidate_trees
    )
    if shared:
        _fail(
            "exact external source shares Git commit/history/object identity with "
            "the authoritative repository"
        )
    if source_path is not None:
        source_path = _safe_relative(source_path, "external machine source")
        source_rows = _run_git(
            checkout,
            ["ls-tree", "-r", candidate_revision, "--", source_path],
            check=False,
        ).stdout.decode("ascii", "strict").splitlines()
        if len(source_rows) != 1:
            _fail("external machine source object identity cannot be inspected")
        try:
            metadata, tracked = source_rows[0].split("\t", 1)
            _mode, kind, source_oid = metadata.split()
        except ValueError as exc:
            raise AdmissionError("external machine source tree identity is malformed") from exc
        blob_occurrences = _run_git(
            root,
            ["rev-list", "--objects", "--all"],
            check=False,
        ).stdout.decode("ascii", "strict").splitlines()
        authoritative_proof_blobs = {
            row.split(" ", 1)[0]
            for row in blob_occurrences
            if " " in row and row.split(" ", 1)[1].endswith(".lean")
        }
        if tracked != source_path or kind != "blob" or source_oid in authoritative_proof_blobs:
            _fail(
                "external machine proof source blob is part of the authoritative history"
            )


def _verify_machine_pre_stage1_provenance(
    root: Path,
    receipt_facts: Mapping[str, Any],
    source: Mapping[str, Any],
    *,
    proposal_author: Mapping[str, Any] | None = None,
    verifier: Mapping[str, Any] | None = None,
    authority_revision: str | None = None,
) -> dict[str, Any]:
    """Revalidate immutable, independent provenance for exact proof bytes."""

    theorem_id = str(receipt_facts.get("theorem_id", ""))
    rows = [
        row
        for row in receipt_facts.get("evidence_bindings", [])
        if isinstance(row, Mapping) and row.get("role") == EXTERNAL_PROVENANCE_ROLE
    ]
    if len(rows) != 1:
        _fail("exact machine source requires one typed pre-Stage1 provenance report")
    binding = rows[0]
    path = _safe_relative(binding.get("path"), "external proof provenance")
    if not path.startswith(f"Stage1_Instances/{theorem_id}/"):
        _fail("external proof provenance is not theorem-owned")
    revision = authority_revision or str(
        receipt_facts.get("repository_base_revision", "")
    )
    data, _ = _head_blob(root, revision, path, "external proof provenance")
    if _digest(data) != binding.get("sha256"):
        _fail("external proof provenance digest is stale")
    report = _parse_json(data, "external proof provenance")
    if data != _pretty_json(report):
        _fail("external proof provenance is not canonical pretty JSON")
    if (
        set(report) != EXTERNAL_PROVENANCE_FIELDS
        or report.get("schema_version") != EXTERNAL_PROVENANCE_SCHEMA
        or report.get("theorem_id") != theorem_id
        or report.get("decision") != "accepted"
    ):
        _fail("external proof provenance fields, schema, or decision are invalid")
    _embedded_digest(report, "provenance_sha256", "external proof provenance")
    reviewer = _actor(
        report.get("reviewer"),
        "external proof provenance reviewer",
        role="independent_reviewer",
    )
    if proposal_author is not None:
        _distinct(reviewer, proposal_author, "external proof provenance reviewer")
    if verifier is not None:
        _distinct(reviewer, verifier, "external proof provenance reviewer")
    publication = report.get("publication")
    reviewed_at = _timestamp(report.get("reviewed_at"), "external proof provenance reviewed_at")
    evidence_as_of = _timestamp(receipt_facts.get("evidence_as_of"), "evidence_as_of")
    source_identity = report.get("source")
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
    if (
        not isinstance(publication, Mapping)
        or set(publication) != {"immutable_id", "timestamp"}
        or not str(publication.get("immutable_id", "")).strip()
        or source_identity != expected_source
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
    forbidden = {
        str(actor.get("id"))
        for actor in (proposal_author, verifier, reviewer)
        if isinstance(actor, Mapping)
    }
    timestamp = focus_eligibility._validate_independent_timestamp(
        root,
        publication.get("timestamp"),
        expected_subject=timestamp_subject,
        cutoff=STAGE1_PROVENANCE_CUTOFF,
        forbidden_principals=forbidden,
        label="external proof publication timestamp",
    )
    if reviewed_at < _timestamp(timestamp["issued_at"], "publication timestamp issued_at"):
        _fail("external proof provenance review predates its independent timestamp")
    pointer = source.get("pre_stage1_provenance")
    if pointer != {
        "path": path,
        "sha256": binding.get("sha256"),
        "provenance_sha256": report.get("provenance_sha256"),
    }:
        _fail("exact machine source does not bind the typed provenance report")
    return {
        "path": path,
        "sha256": str(binding.get("sha256")),
        "provenance_sha256": str(report.get("provenance_sha256")),
        "publication_subject_sha256": timestamp["subject_sha256"],
        "published_at": timestamp["issued_at"],
        "timestamp_authority": timestamp["authority"],
        "timestamp_key_id": timestamp["key_id"],
        "reviewer": reviewer,
        "reviewed_at": str(report.get("reviewed_at")),
        "decision": "accepted",
    }


def _lean_probe(
    checkout: Path,
    *,
    source_path: Path,
    declaration: str,
    command_runner: Callable[..., subprocess.CompletedProcess[bytes]],
    lean_path: Path | None = None,
) -> tuple[str, list[str], str]:
    probe = checkout / "Stage1FocusAuthorityProbe.lean"
    if probe.exists() or probe.is_symlink():
        _fail("external source conflicts with scheduler probe path")
    try:
        source = source_path.read_bytes()
    except OSError as exc:
        raise AdmissionError("scheduler Lean probe source is unavailable") from exc
    probe.write_bytes(
        source
        + (b"" if source.endswith(b"\n") else b"\n")
        + f"#check {declaration}\n#print axioms {declaration}\n".encode("utf-8")
    )
    try:
        # An explicit import path means the caller has already materialized the
        # exact module closure to probe (notably the transport provider olean).
        # Invoke the pinned Lean binary directly in that case: starting Lake in
        # a read-only revision snapshot may try to create `.lake` before Lean
        # runs, even though no package resolution is needed.
        if lean_path is not None:
            command = ["lean", probe.name]
        elif (checkout / "lakefile.lean").is_file() or (checkout / "lakefile.toml").is_file():
            command = ["lake", "env", "lean", probe.name]
        else:
            command = ["lean", probe.name]
        result = _run_lean_replay(
            command_runner,
            checkout,
            command,
            timeout=KERNEL_REPLAY_TIMEOUT_SECONDS,
            lean_path=lean_path,
        )
    finally:
        probe.unlink(missing_ok=True)
    if result.returncode != 0:
        _fail("scheduler declaration/type/trust probe failed")
    try:
        output = result.stdout.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AdmissionError("scheduler Lean probe output is not UTF-8") from exc
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    check_prefix = f"{declaration} :"
    check_rows = [line for line in lines if line.startswith(check_prefix)]
    if len(check_rows) != 1:
        _fail("scheduler Lean probe did not identify exactly one declaration type")
    type_text = " ".join(check_rows[0].split(":", 1)[1].split())
    if not type_text:
        _fail("scheduler Lean probe produced an empty declaration type")
    quoted_declaration = re.escape(declaration)
    no_axiom_pattern = re.compile(
        rf"^['\"]?{quoted_declaration}['\"]? does not depend on any axioms$"
    )
    axiom_pattern = re.compile(
        rf"^['\"]?{quoted_declaration}['\"]? depends on axioms: (\[.*\])$"
    )
    no_axiom_rows = [line for line in lines if no_axiom_pattern.fullmatch(line)]
    axiom_rows = [match for line in lines if (match := axiom_pattern.fullmatch(line))]
    if len(no_axiom_rows) + len(axiom_rows) != 1:
        _fail("scheduler Lean probe did not report the declaration axiom closure")
    axioms: list[str] = []
    if axiom_rows:
        raw_axioms = axiom_rows[0].group(1)
        axioms = sorted(
            value.strip().strip("'\"")
            for value in raw_axioms[1:-1].split(",")
            if value.strip()
        )
    return _digest(type_text.encode("utf-8")), axioms, _digest(result.stdout)


def _lean_import_probe(
    checkout: Path,
    *,
    package: Path,
    module: str,
    declaration: str,
    command_runner: Callable[..., subprocess.CompletedProcess[bytes]],
) -> tuple[str, list[str], str]:
    """Import a provider through Lake, then inspect its exact declaration."""

    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*", module) is None:
        _fail("pinned provider module is not a canonical Lean module name")
    try:
        package.relative_to(checkout)
    except ValueError as exc:
        raise AdmissionError("pinned provider package escapes the Lean closure") from exc
    probe = package / "Stage1FocusPinnedProviderProbe.lean"
    if probe.exists() or probe.is_symlink():
        _fail("local Lean closure conflicts with the pinned provider probe path")
    probe.write_text(
        f"import {module}\n#check {declaration}\n#print axioms {declaration}\n",
        encoding="utf-8",
    )
    try:
        result = _run_lean_replay(
            command_runner,
            package,
            ["lake", "env", "lean", probe.name],
            timeout=KERNEL_REPLAY_TIMEOUT_SECONDS,
        )
    finally:
        probe.unlink(missing_ok=True)
    if result.returncode != 0:
        _fail("local pinned provider Lake import probe failed")
    try:
        output = result.stdout.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AdmissionError("local pinned provider probe output is not UTF-8") from exc
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    check_rows = [line for line in lines if line.startswith(f"{declaration} ")]
    if len(check_rows) != 1:
        _fail("local pinned provider import did not identify one declaration type")
    declaration_tail = check_rows[0][len(declaration) :].strip()
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
    return _digest(type_text.encode("utf-8")), axioms, _digest(result.stdout)


def _fresh_root_provider_replay(
    lean_root: Path,
    source_path: Path,
    *,
    module: str,
    declaration: str,
    command_runner: Callable[..., subprocess.CompletedProcess[bytes]],
) -> tuple[subprocess.CompletedProcess[bytes], str, list[str], str]:
    """Compile exact source afresh, then probe only that fresh root-bound module."""

    with tempfile.TemporaryDirectory(
        prefix=".stage1-focus-provider-", dir=lean_root
    ) as directory:
        replay_root = Path(directory)
        module_path = PurePosixPath(*module.split("."))
        olean_path = replay_root / module_path.with_suffix(".olean")
        probe_path = replay_root / "Stage1FocusPinnedProviderProbe.lean"
        olean_path.parent.mkdir(parents=True, exist_ok=True)
        replay = _run_lean_replay(
            command_runner,
            lean_root,
            [
                "lake",
                "env",
                "lean",
                "-o",
                olean_path.relative_to(lean_root).as_posix(),
                source_path.relative_to(lean_root).as_posix(),
            ],
            timeout=KERNEL_REPLAY_TIMEOUT_SECONDS,
            writable_path=replay_root,
        )
        if replay.returncode != 0 or not olean_path.is_file():
            _fail("local pinned provider Lake replay failed")
        probe_path.write_text(
            f"import {module}\n"
            f"#check {declaration}\n#print axioms {declaration}\n",
            encoding="utf-8",
        )
        probe = _run_lean_replay(
            command_runner,
            lean_root,
            ["lake", "env", "lean", probe_path.relative_to(lean_root).as_posix()],
            timeout=KERNEL_REPLAY_TIMEOUT_SECONDS,
            lean_path=replay_root,
        )
        if probe.returncode != 0:
            _fail("local pinned provider Lake import probe failed")
        try:
            output = probe.stdout.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise AdmissionError("local pinned provider probe output is not UTF-8") from exc
        lines = [line.strip() for line in output.splitlines() if line.strip()]
        check_rows = [line for line in lines if line.startswith(f"{declaration} ")]
        if len(check_rows) != 1:
            _fail("local pinned provider import did not identify one declaration type")
        tail = check_rows[0][len(declaration) :].strip()
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
        return replay, _digest(type_text.encode("utf-8")), axioms, _digest(probe.stdout)


def _verify_local_pinned_provider(
    root: Path,
    authority_revision: str,
    source: Mapping[str, Any],
    provider: Mapping[str, str],
    *,
    command_runner: Callable[..., subprocess.CompletedProcess[bytes]],
) -> dict[str, Any]:
    """Replay the exact provider from the scheduler-owned live Lake closure.

    `.lake` is intentionally untracked, so a Git archive cannot establish that
    the package available to local acceptance is the manifest package.  Bind
    the tracked lock at ``authority_revision`` to the live lock bytes, then
    inspect and replay the live package without network or repository writes.
    """

    lean_root = root / "Formalizations" / "Lean"
    manifest = lean_root / "lake-manifest.json"
    if manifest.is_symlink() or not manifest.is_file():
        _fail("scheduler-owned Lake manifest is absent or unsafe")
    if _digest(manifest.read_bytes()) != provider.get("manifest_sha256"):
        _fail("live scheduler-owned Lake manifest differs from the authority revision")
    _require_root_lake_declaration(root, authority_revision, provider)
    packages = lean_root / ".lake" / "packages"
    package = packages / provider["cache_name"]
    if packages.is_symlink() or not packages.is_dir() or package.is_symlink() or not package.is_dir():
        _fail("pinned provider package is absent from the scheduler-owned Lake closure")
    if _git_text(package, "rev-parse", "--is-inside-work-tree") != "true":
        _fail("local pinned provider is not a Git worktree")
    remotes = [
        row
        for row in _git_text(package, "remote", "-v").splitlines()
        if row.strip()
    ]
    fetch_urls = []
    for row in remotes:
        fields = row.split()
        if len(fields) == 3 and fields[2] == "(fetch)":
            fetch_urls.append(fields[1])
    expected_remote = _canonical_git_remote(provider.get("repository"))
    if (
        expected_remote is None
        or len(fetch_urls) != 1
        or _canonical_git_remote(fetch_urls[0]) != expected_remote
    ):
        _fail("local pinned provider origin URL disagrees with the Lake manifest")
    if _git_text(package, "rev-parse", "--verify", "HEAD^{commit}") != provider[
        "revision"
    ]:
        _fail("local pinned provider revision disagrees with the Lake manifest")
    if _git_text(package, "status", "--porcelain", "--untracked-files=all"):
        _fail("local pinned provider is not a clean exact checkout")
    file_path = _safe_relative(source.get("file_path"), "pinned provider source")
    source_path = package
    for component in PurePosixPath(file_path).parts:
        source_path /= component
        if source_path.is_symlink():
            _fail("pinned provider source path traverses a symlink")
    if not source_path.is_file():
        _fail("pinned provider source is absent from its manifest package")
    source_bytes = source_path.read_bytes()
    if _digest(source_bytes) != source.get("file_sha256"):
        _fail("local pinned provider source differs from the admitted proof")
    body_sha, text = _declaration_region(
        source_bytes, str(source.get("declaration", ""))
    )
    terminal = source.get("terminal_proof_body")
    if (
        not isinstance(terminal, Mapping)
        or terminal.get("locator") != source.get("declaration")
        or terminal.get("sha256") != body_sha
    ):
        _fail("local pinned provider proof body differs from the admitted proof")
    if PROHIBITED_LEAN_TOKENS.search(text):
        _fail("local pinned provider source contains a prohibited construct")
    # Compile the exact provider source through the repository's manifest-bound
    # closure.  Starting Lake in the provider package would resolve a different
    # package-local cache, which need not exist even when the authoritative root
    # closure is complete.
    replay, type_sha, axioms, output_sha = _fresh_root_provider_replay(
        lean_root,
        source_path,
        module=str(source.get("module", "")),
        declaration=str(source.get("declaration", "")),
        command_runner=command_runner,
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
    return {
        **dict(provider),
        "file_sha256": _digest(source_bytes),
        "terminal_proof_body_sha256": body_sha,
        "declaration_type_sha256": type_sha,
        "permitted_axioms": axioms,
        "kernel_stdout_sha256": _digest(replay.stdout),
        "kernel_stderr_sha256": _digest(replay.stderr),
        "trust_audit_output_sha256": output_sha,
    }


def _lean_name_literal(name: str, label: str) -> str:
    """Return an exact Lean name literal for a replay-generated command."""

    if (
        not isinstance(name, str)
        or not name
        or "\x00" in name
        or "`" in name
        or "\n" in name
        or "\r" in name
    ):
        _fail(f"{label} is not a canonical Lean declaration name")
    return "`" + name


def _transport_replay_source(
    artifact_bytes: bytes,
    *,
    target_declaration: str,
    provider_declaration: str,
) -> bytes:
    """Build the consumer-owned transport plus its kernel-level dependency check."""

    target_name = _lean_name_literal(target_declaration, "transport target declaration")
    provider_name = _lean_name_literal(
        provider_declaration, "transport provider declaration"
    )
    suffix = f'''\n
open Lean Elab Command in
elab "#stage1_verify_transport_provider_dependency" : command => liftTermElabM do
  let targetInfo ← getConstInfo {target_name}
  let targetValue ← match targetInfo.value? (allowOpaque := true) with
    | some value => pure value
    | none => throwError "transport target declaration has no inspectable proof body"
  let directConstants := targetValue.getUsedConstantsAsSet
  if !directConstants.contains {provider_name} then
    throwError "transport target proof body does not directly depend on provider declaration"
  logInfo "{TRANSPORT_DEPENDENCY_PREFIX} target={target_declaration} provider={provider_declaration} status=direct-proof-body-dependency"

#stage1_verify_transport_provider_dependency
'''.encode("utf-8")
    return (
        f"import Lean\nimport {TRANSPORT_PROVIDER_MODULE}\n".encode("utf-8")
        + artifact_bytes
        + (b"" if artifact_bytes.endswith(b"\n") else b"\n")
        + suffix
    )


def _materialize_head_checkout(root: Path, revision: str, destination: Path) -> None:
    """Materialize exactly one tracked repository revision without worker bytes."""
    archive = _run_git(root, ["archive", "--format=tar", revision]).stdout
    try:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as stream:
            for member in stream.getmembers():
                pure = PurePosixPath(member.name)
                if (
                    pure.is_absolute()
                    or ".." in pure.parts
                    or member.issym()
                    or member.islnk()
                    or not (member.isdir() or member.isfile())
                ):
                    _fail("repository archive contains an unsafe target entry")
            stream.extractall(destination, filter="data")
    except (tarfile.TarError, OSError) as exc:
        raise AdmissionError("repository target snapshot cannot be materialized") from exc


def verify_local_lean_target(
    root: Path,
    receipt_facts: Mapping[str, Any],
    *,
    verifier: Mapping[str, Any],
    command_runner: Callable[..., subprocess.CompletedProcess[bytes]] | None = None,
) -> dict[str, Any]:
    """Probe the actual HEAD target declaration, never its proposed fingerprint."""
    actor = _actor(verifier, "local target verifier")
    if command_runner is None:
        command_runner = _readonly_kernel_command
    if actor["role"] not in {"scheduler_focus_verifier", "independent_reviewer"}:
        _fail("local target verifier role is not authoritative")
    target = receipt_facts.get("target_binding")
    if not isinstance(target, Mapping) or target.get("formal_system") != "Lean 4":
        _fail("exact admission lacks a Lean 4 local target")
    revision = receipt_facts.get("repository_base_revision")
    if not isinstance(revision, str) or GIT_OID_RE.fullmatch(revision) is None:
        _fail("local target repository revision is malformed")
    resolved = _git_text(root, "rev-parse", "--verify", f"{revision}^{{commit}}")
    if resolved != revision:
        _fail("local target repository revision is not canonical")
    relative = _safe_relative(target.get("path"), "local Lean target")
    if not relative.startswith(f"Stage1_Instances/{receipt_facts.get('theorem_id')}/"):
        _fail("local Lean target is not theorem-owned")
    source_data, _ = _head_blob(root, revision, relative, "local Lean target")
    file_sha = _digest(source_data)
    if file_sha != target.get("file_sha256"):
        _fail("local Lean target file digest is stale")
    declaration = target.get("declaration")
    if not isinstance(declaration, str) or not declaration:
        _fail("local Lean target declaration is missing")
    if PROHIBITED_LEAN_TOKENS.search(source_data.decode("utf-8", "replace")):
        _fail("local Lean target contains a prohibited construct")

    replay_authority = _repository_replay_authority(root, revision)
    with tempfile.TemporaryDirectory(prefix="stage1-focus-target-") as directory:
        checkout = Path(directory) / "repository"
        checkout.mkdir()
        _materialize_head_checkout(root, revision, checkout)
        source_path = checkout / relative
        lean_root = checkout / "Formalizations" / "Lean"
        if not lean_root.is_dir():
            _fail("repository target snapshot lacks its Lean project")
        toolchain, dependency_lock_sha = _dependency_identity(lean_root)
        # The theorem-owned source is outside the Lake root.  Copy it into the
        # exact project snapshot so `lake env lean` uses only the pinned closure.
        probe_source = lean_root / "Stage1FocusLocalTarget.lean"
        if probe_source.exists():
            _fail("local target conflicts with scheduler probe path")
        probe_source.write_bytes(source_path.read_bytes())
        try:
            type_sha, axioms, output_sha = _lean_probe(
                lean_root,
                source_path=probe_source,
                declaration=declaration,
                command_runner=command_runner,
            )
        except AdmissionError as exc:
            # A root Lake project with an intentionally absent writable cache
            # may not start under the read-only sandbox.  The target source
            # itself has no imports, so replay it with the exact pinned Lean
            # binary while root closure authority remains separately bound.
            if "scheduler declaration/type/trust probe failed" not in str(exc):
                raise
            fallback = Path(directory) / "standalone-target"
            fallback.mkdir()
            (fallback / "lean-toolchain").write_bytes(
                (lean_root / "lean-toolchain").read_bytes()
            )
            fallback_source = fallback / "Stage1FocusLocalTarget.lean"
            fallback_source.write_bytes(source_data)
            type_sha, axioms, output_sha = _lean_probe(
                fallback,
                source_path=fallback_source,
                declaration=declaration,
                command_runner=command_runner,
            )
        finally:
            probe_source.unlink(missing_ok=True)
    observed = {
        "schema_version": LOCAL_TARGET_RESULT_SCHEMA,
        "formal_system": "Lean 4",
        "repository_revision": revision,
        "file_path": relative,
        "file_sha256": file_sha,
        "declaration": declaration,
        "declaration_type_sha256": type_sha,
        "toolchain": toolchain,
        "dependency_lock_sha256": dependency_lock_sha,
        "kernel_exit_code": 0,
        "permitted_axioms": axioms,
        "trust_audit_output_sha256": output_sha,
        "replay_authority": replay_authority,
    }
    if set(axioms) - PERMITTED_AXIOMS:
        _fail("local target uses axioms outside the foundation policy")
    if set(observed) != LOCAL_TARGET_RESULT_FIELDS:
        _fail("local target authority result schema is inconsistent")
    return observed


def _authority_result(
    *,
    source: Mapping[str, Any],
    file_path: str,
    file_sha: str,
    body_sha: str,
    type_sha: str,
    axioms: list[str],
    trust_output_sha: str,
    toolchain: str,
    dependency_lock_sha: str,
    replay_authority: Mapping[str, Any],
) -> dict[str, Any]:
    trust = source.get("trust_audit")
    if not isinstance(trust, Mapping):
        _fail("machine source lacks trust audit facts")
    claimed_axioms = sorted(str(value) for value in trust.get("permitted_axioms", []))
    if set(claimed_axioms) - PERMITTED_AXIOMS:
        _fail("machine source claims axioms outside the foundation policy")
    if set(axioms) - PERMITTED_AXIOMS:
        _fail("machine source uses axioms outside the foundation policy")
    if claimed_axioms != sorted(axioms):
        _fail("machine source axiom inventory is not exact")
    result = {
        "schema_version": AUTHORITY_RESULT_SCHEMA,
        "formal_system": source.get("formal_system"),
        "toolchain": toolchain,
        "dependency_lock_sha256": dependency_lock_sha,
        "file_path": file_path,
        "file_sha256": file_sha,
        "module": source.get("module"),
        "declaration": source.get("declaration"),
        "declaration_type_sha256": type_sha,
        "terminal_proof_body_sha256": body_sha,
        "kernel_exit_code": 0,
        "placeholder_free": True,
        "unsafe_free": True,
        "oracle_free": True,
        "undeclared_axioms_free": set(axioms) <= PERMITTED_AXIOMS,
        "permitted_axioms": axioms,
        "trust_audit_output_sha256": trust_output_sha,
        "replay_authority": dict(replay_authority),
    }
    expected = {
        "formal_system": source.get("formal_system"),
        "toolchain": source.get("kernel_replay", {}).get("toolchain"),
        "dependency_lock_sha256": source.get("kernel_replay", {}).get(
            "dependency_lock_sha256"
        ),
        "file_path": source.get("file_path"),
        "file_sha256": source.get("file_sha256"),
        "module": source.get("module"),
        "declaration": source.get("declaration"),
        "declaration_type_sha256": source.get("declaration_type_sha256"),
        "terminal_proof_body_sha256": source.get("terminal_proof_body", {}).get(
            "sha256"
        ),
        "placeholder_free": trust.get("placeholder_free"),
        "unsafe_free": trust.get("unsafe_free"),
        "oracle_free": trust.get("oracle_free"),
        "undeclared_axioms_free": trust.get("undeclared_axioms_free"),
        "permitted_axioms": claimed_axioms,
        "trust_audit_output_sha256": trust.get("output_sha256"),
        "replay_authority": dict(replay_authority),
    }
    observed = {key: result.get(key) for key in expected}
    if observed != expected:
        _fail(
            "kernel authority result does not bind declaration type, body, "
            "toolchain, dependency lock, and trust facts"
        )
    return result


def _readonly_kernel_command(
    checkout: Path,
    command: list[str],
    *,
    timeout: int,
    lean_path: Path | None = None,
    writable: bool = False,
    writable_path: Path | None = None,
) -> subprocess.CompletedProcess[bytes]:
    if not Path("/usr/bin/bwrap").is_file():
        _fail("bubblewrap is required for independent kernel replay")
    executable_name = Path(command[0]).name
    if executable_name not in {"lean", "lake"} or command[0] != executable_name:
        _fail("kernel replay executable is not a canonical Lean authority command")
    toolchain_file = checkout / "lean-toolchain"
    if toolchain_file.is_symlink() or not toolchain_file.is_file():
        _fail("kernel replay lacks a regular pinned lean-toolchain")
    toolchain_name = toolchain_file.read_text(encoding="utf-8").strip()
    match = re.fullmatch(r"leanprover/lean4:v([0-9]+\.[0-9]+\.[0-9]+)", toolchain_name)
    if match is None:
        _fail("kernel replay Lean toolchain pin is noncanonical")
    tool_root = Path.home() / ".elan" / "toolchains" / (
        "leanprover--lean4---v" + match.group(1)
    )
    executable_path = tool_root / "bin" / executable_name
    if executable_path.is_symlink() or not executable_path.is_file():
        _fail("pinned Lean toolchain executable is unavailable")
    expected_binary_sha = hashlib.sha256(executable_path.read_bytes()).hexdigest()
    bwrap = [
        "/usr/bin/bwrap",
        "--die-with-parent",
        "--new-session",
        "--unshare-all",
        "--tmpfs",
        "/",
    ]
    for host in (Path("/usr"), Path("/lib"), Path("/lib64")):
        if host.exists():
            bwrap.extend(["--dir", host.as_posix(), "--ro-bind", host.as_posix(), host.as_posix()])
    bwrap.extend(["--symlink", "usr/bin", "/bin", "--proc", "/proc", "--dev", "/dev"])
    current = Path("/")
    for component in tool_root.parts[1:]:
        current /= component
        bwrap.extend(["--dir", current.as_posix()])
    bwrap.extend(["--ro-bind", tool_root.as_posix(), tool_root.as_posix()])
    path_value = f"{tool_root / 'bin'}:/usr/bin:/bin"
    lean_path_value: str | None = None
    if lean_path is not None:
        try:
            relative_lean_path = lean_path.resolve().relative_to(checkout.resolve())
        except (OSError, ValueError) as exc:
            raise AdmissionError("Lean replay import path escapes its checkout") from exc
        lean_path_value = (Path("/repo") / relative_lean_path).as_posix()
    argv = [executable_path.as_posix(), *command[1:]]
    bwrap.extend(["--dir", "/repo"])
    if writable and writable_path is not None:
        _fail("kernel replay writable boundary is ambiguous")
    bwrap.extend(["--bind" if writable else "--ro-bind", checkout.as_posix(), "/repo"])
    if writable_path is not None:
        try:
            relative_writable = writable_path.resolve().relative_to(checkout.resolve())
        except (OSError, ValueError) as exc:
            raise AdmissionError("kernel replay writable path escapes its checkout") from exc
        if relative_writable == Path(".") or not writable_path.is_dir() or writable_path.is_symlink():
            _fail("kernel replay writable path is unsafe")
        bwrap.extend(
            ["--bind", writable_path.as_posix(), (Path("/repo") / relative_writable).as_posix()]
        )
    bwrap.extend(
        [
            "--dir",
            "/scratch",
            "--tmpfs",
            "/tmp",
            "--chdir",
            "/repo",
            "--clearenv",
            "--setenv",
            "PATH",
            path_value,
            "--setenv",
            "HOME",
            "/scratch",
            "--setenv",
            "ELAN_HOME",
            "/scratch/.elan",
            "--setenv",
            "TMPDIR",
            "/tmp",
            "--setenv",
            "PYTHONDONTWRITEBYTECODE",
            "1",
        ]
    )
    if lean_path_value is not None:
        bwrap.extend(["--setenv", "LEAN_PATH", lean_path_value])
    bwrap.extend(["--", *argv])
    try:
        result = subprocess.run(
            bwrap,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        if hashlib.sha256(executable_path.read_bytes()).hexdigest() != expected_binary_sha:
            _fail("pinned Lean executable changed during replay")
        return result
    except subprocess.TimeoutExpired as exc:
        raise AdmissionError("independent kernel replay timed out") from exc


def _run_lean_replay(
    command_runner: Callable[..., subprocess.CompletedProcess[bytes]],
    checkout: Path,
    command: list[str],
    *,
    timeout: int,
    lean_path: Path | None = None,
    writable: bool = False,
    writable_path: Path | None = None,
) -> subprocess.CompletedProcess[bytes]:
    """Call a replay runner while preserving compatibility with simple test doubles."""

    if lean_path is None and not writable and writable_path is None:
        return command_runner(checkout, command, timeout=timeout)
    try:
        return command_runner(
            checkout,
            command,
            timeout=timeout,
            lean_path=lean_path,
            writable=writable,
            writable_path=writable_path,
        )
    except TypeError as exc:
        if (
            "lean_path" not in str(exc)
            and "writable" not in str(exc)
            and "writable_path" not in str(exc)
        ):
            raise
        return command_runner(checkout, command, timeout=timeout)


def _canonical_kernel_command(command: Any, *, file_path: str, module: Any) -> list[str]:
    """Accept only a compiling Lean invocation of the bound source.

    Lean/Lake informational switches such as `--version` exit successfully
    without checking a source.  Requiring one exact grammar also prevents a
    source-looking operand after an option terminator from lending authority to
    an unrelated no-op command.
    """

    if (
        not isinstance(command, list)
        or any(not isinstance(part, str) or not part or "\x00" in part for part in command)
    ):
        _fail("external kernel replay command is malformed")
    executable = Path(command[0]).name if command else ""
    if executable == "lean" and command == ["lean", file_path]:
        return list(command)
    if executable == "lake" and command == ["lake", "env", "lean", file_path]:
        return list(command)
    _fail("external kernel replay command is not the canonical Lean compilation of the bound source")


def _canonical_transport_command(
    command: Any, *, validator_path: str, artifact_path: str
) -> list[str]:
    """Accept one non-ambiguous invocation of the content-bound validator."""

    expected = [
        "python3",
        validator_path,
        "--transport-artifact",
        artifact_path,
    ]
    if command != expected:
        _fail(
            "machine transport replay command is not the canonical bound validator invocation"
        )
    return expected


def _readonly_transport_command(
    checkout: Path, command: list[str], *, timeout: int
) -> subprocess.CompletedProcess[bytes]:
    """Run a transport validator without network or writable repository access."""

    if not Path("/usr/bin/bwrap").is_file() or not Path("/usr/bin/python3").is_file():
        _fail("bubblewrap and the system Python are required for transport replay")
    bwrap = [
        "/usr/bin/bwrap",
        "--die-with-parent",
        "--new-session",
        "--unshare-all",
        "--tmpfs",
        "/",
    ]
    for host in (Path("/usr"), Path("/lib"), Path("/lib64")):
        if host.exists():
            bwrap.extend(
                ["--dir", host.as_posix(), "--ro-bind", host.as_posix(), host.as_posix()]
            )
    bwrap.extend(
        [
            "--symlink",
            "usr/bin",
            "/bin",
            "--proc",
            "/proc",
            "--dev",
            "/dev",
            "--dir",
            "/repo",
            "--ro-bind",
            checkout.as_posix(),
            "/repo",
            "--dir",
            "/scratch",
            "--tmpfs",
            "/tmp",
            "--chdir",
            "/repo",
            "--clearenv",
            "--setenv",
            "PATH",
            "/usr/bin:/bin",
            "--setenv",
            "HOME",
            "/scratch",
            "--setenv",
            "TMPDIR",
            "/tmp",
            "--setenv",
            "PYTHONDONTWRITEBYTECODE",
            "1",
            "--",
            "/usr/bin/python3",
            "-I",
            *command[1:],
        ]
    )
    try:
        return subprocess.run(
            bwrap,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise AdmissionError("independent machine transport replay timed out") from exc


def _transport_binding_bytes(
    root: Path,
    revision: str,
    theorem_id: str,
    binding: Mapping[str, Any],
    label: str,
) -> tuple[str, bytes]:
    path = _safe_relative(binding.get("path"), label)
    if not path.startswith(f"Stage1_Instances/{theorem_id}/"):
        _fail(f"{label} is not theorem-owned")
    digest = binding.get("sha256")
    if not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None:
        _fail(f"{label} lacks a canonical content digest")
    data, _ = _head_blob(root, revision, path, label)
    if _digest(data) != digest:
        _fail(f"{label} digest is stale")
    return path, data


def _verify_machine_transport_replay(
    root: Path,
    receipt_facts: Mapping[str, Any],
    *,
    actor: Mapping[str, Any],
    external_result: Mapping[str, Any],
    local_target_result: Mapping[str, Any],
    transport_command_runner: Callable[..., subprocess.CompletedProcess[bytes]] = (
        _readonly_transport_command
    ),
    lean_command_runner: Callable[..., subprocess.CompletedProcess[bytes]] = (
        _readonly_kernel_command
    ),
    external_checkout: Path | None = None,
    external_source_path: Path | None = None,
) -> dict[str, Any]:
    """Replay one canonical Lean-to-Lean transport under scheduler authority."""

    source = receipt_facts.get("machine_proof", {}).get("source")
    target = receipt_facts.get("target_binding")
    if not isinstance(source, Mapping) or not isinstance(target, Mapping):
        _fail("checked transport lacks source or local target facts")
    if source.get("formal_system") != "Lean 4" or target.get("formal_system") != "Lean 4":
        _fail(
            "cross-formal-system checked transport requires a generic provider replay "
            "authority and is not yet supported"
        )
    if (
        external_checkout is None
        or external_source_path is None
        or not external_source_path.is_file()
        or not external_source_path.is_relative_to(external_checkout)
    ):
        _fail("checked transport lacks the materialized provider source checkout")
    evidence = source.get("transport_evidence")
    if not isinstance(evidence, list) or len(evidence) != 1:
        _fail("checked transport requires exactly one canonical replay receipt")
    row = evidence[0]
    if not isinstance(row, Mapping):
        _fail("checked transport evidence is malformed")
    theorem_id = str(receipt_facts.get("theorem_id"))
    revision = str(receipt_facts.get("repository_base_revision"))
    receipt_path, receipt_bytes = _transport_binding_bytes(
        root, revision, theorem_id, row, "machine transport replay receipt"
    )
    receipt_sha = _digest(receipt_bytes)
    top_level_rows = [
        binding
        for binding in receipt_facts.get("evidence_bindings", [])
        if isinstance(binding, Mapping)
        and binding.get("path") == receipt_path
        and binding.get("sha256") == receipt_sha
    ]
    if (
        row.get("role") != "statement_match"
        or row.get("evidence_kind") != "machine_checked_statement_transport"
        or row.get("replay_receipt_sha256") != receipt_sha
        or len(top_level_rows) != 1
        or top_level_rows[0].get("role") != "statement_match"
        or top_level_rows[0].get("evidence_kind")
        != "machine_checked_statement_transport"
    ):
        _fail("machine transport replay receipt is not top-level content-bound")
    replay_receipt = _parse_json(receipt_bytes, "machine transport replay receipt")
    if receipt_bytes != _pretty_json(replay_receipt):
        _fail("machine transport replay receipt is not canonical pretty JSON")
    if focus_eligibility._schema_definition_errors(
        root, replay_receipt, "machineTransportReplayReceipt"
    ):
        _fail("machine transport replay receipt schema is invalid")
    if replay_receipt.get("theorem_id") != theorem_id:
        _fail("machine transport replay receipt targets another theorem")

    observed_source = {
        "formal_system": external_result.get("formal_system"),
        "declaration": external_result.get("declaration"),
        "declaration_type_sha256": external_result.get("declaration_type_sha256"),
    }
    observed_target = {
        "formal_system": local_target_result.get("formal_system"),
        "declaration": local_target_result.get("declaration"),
        "declaration_type_sha256": local_target_result.get(
            "declaration_type_sha256"
        ),
    }
    claimed_row_identity = {
        "source_formal_system": observed_source["formal_system"],
        "source_declaration": observed_source["declaration"],
        "source_declaration_type_sha256": observed_source[
            "declaration_type_sha256"
        ],
        "target_formal_system": observed_target["formal_system"],
        "target_declaration": observed_target["declaration"],
        "target_declaration_type_sha256": observed_target[
            "declaration_type_sha256"
        ],
    }
    if (
        replay_receipt.get("source") != observed_source
        or replay_receipt.get("target") != observed_target
        or any(row.get(key) != value for key, value in claimed_row_identity.items())
    ):
        _fail("machine transport replay does not bind the observed source and local target")
    if observed_source == observed_target:
        _fail("checked transport is redundant for identical observed proof types")

    artifact = replay_receipt["transport_artifact"]
    validator = replay_receipt["validator"]
    replay = replay_receipt["replay"]
    trust = replay_receipt["trust_audit"]
    artifact_path, artifact_bytes = _transport_binding_bytes(
        root, revision, theorem_id, artifact, "machine transport artifact"
    )
    validator_path, validator_bytes = _transport_binding_bytes(
        root, revision, theorem_id, validator, "machine transport validator"
    )
    output_path, output_bytes = _transport_binding_bytes(
        root, revision, theorem_id, replay["output"], "machine transport replay output"
    )
    trust_output_path, _trust_output_bytes = _transport_binding_bytes(
        root, revision, theorem_id, trust["output"], "machine transport trust output"
    )
    if validator.get("authority") != "scheduler_master_lane":
        _fail("machine transport validator is not scheduler-owned")
    if validator_bytes != TRANSPORT_VALIDATOR_SOURCE:
        _fail("machine transport validator bytes are not scheduler-owned")
    command = _canonical_transport_command(
        replay.get("command"),
        validator_path=validator_path,
        artifact_path=artifact_path,
    )
    terminal_sha, artifact_text = _declaration_region(
        artifact_bytes, str(artifact.get("declaration", ""))
    )
    terminal = artifact.get("terminal_proof_body")
    if (
        artifact.get("formal_system") != "Lean 4"
        or artifact.get("declaration") != observed_target["declaration"]
        or artifact.get("declaration_type_sha256")
        != observed_target["declaration_type_sha256"]
        or not isinstance(terminal, Mapping)
        or terminal.get("locator") != artifact.get("declaration")
        or terminal.get("sha256") != terminal_sha
    ):
        _fail("machine transport artifact does not implement the observed local target")
    if PROHIBITED_LEAN_TOKENS.search(artifact_text):
        _fail("machine transport artifact contains a prohibited construct")

    with tempfile.TemporaryDirectory(prefix="stage1-focus-transport-") as directory:
        checkout = Path(directory) / "repository"
        checkout.mkdir()
        _materialize_head_checkout(root, revision, checkout)
        lean_root = checkout / "Formalizations" / "Lean"
        if not lean_root.is_dir():
            _fail("repository transport snapshot lacks its Lean project")
        toolchain, dependency_sha = _dependency_identity(lean_root)
        provider_source = lean_root / TRANSPORT_PROVIDER_SOURCE
        provider_olean = lean_root / TRANSPORT_PROVIDER_OLEAN
        probe_source = lean_root / TRANSPORT_REPLAY_SOURCE
        if any(
            path.exists() or path.is_symlink()
            for path in (provider_source, provider_olean, probe_source)
        ):
            _fail("machine transport conflicts with the scheduler probe path")
        provider_bytes = external_source_path.read_bytes()
        provider_source.write_bytes(provider_bytes)
        try:
            provider_compile = _run_lean_replay(
                lean_command_runner,
                lean_root,
                [
                    "lean",
                    "-o",
                    TRANSPORT_PROVIDER_OLEAN,
                    TRANSPORT_PROVIDER_SOURCE,
                ],
                timeout=KERNEL_REPLAY_TIMEOUT_SECONDS,
                writable=True,
            )
            if provider_compile.returncode != 0:
                _fail("checked transport could not compile the materialized provider")
            probe_source.write_bytes(
                _transport_replay_source(
                    artifact_bytes,
                    target_declaration=str(artifact["declaration"]),
                    provider_declaration=str(source.get("declaration", "")),
                )
            )
            joint_replay = _run_lean_replay(
                lean_command_runner,
                lean_root,
                ["lean", TRANSPORT_REPLAY_SOURCE],
                timeout=KERNEL_REPLAY_TIMEOUT_SECONDS,
                lean_path=lean_root,
            )
            if joint_replay.returncode != 0:
                _fail(
                    "checked transport joint Lean replay failed or target proof body "
                    "does not depend on the provider declaration"
                )
            type_sha, axioms, trust_output_sha = _lean_probe(
                lean_root,
                source_path=probe_source,
                declaration=str(artifact["declaration"]),
                command_runner=lean_command_runner,
                lean_path=lean_root,
            )
        finally:
            probe_source.unlink(missing_ok=True)
            provider_olean.unlink(missing_ok=True)
            provider_source.unlink(missing_ok=True)
        replay_result = transport_command_runner(
            checkout, list(command), timeout=KERNEL_REPLAY_TIMEOUT_SECONDS
        )
    if replay_result.returncode != 0:
        _fail("independent machine transport validator replay failed")
    if replay_result.stderr:
        _fail("independent machine transport validator emitted unbound diagnostics")
    if replay_result.stdout != output_bytes:
        _fail("machine transport validator output differs from its content binding")
    if (
        replay.get("exit_code") != 0
        or replay.get("toolchain") != toolchain
        or replay.get("dependency_lock_sha256") != dependency_sha
        or type_sha != observed_target["declaration_type_sha256"]
        or sorted(trust.get("permitted_axioms", [])) != axioms
        or set(axioms) - PERMITTED_AXIOMS
    ):
        _fail(
            "independent machine transport kernel replay disagrees with its type, "
            "environment, or trust audit"
        )
    checked_at = _timestamp(replay.get("checked_at"), "transport replay checked_at")
    independent_review = replay_receipt.get("independent_review")
    reviewer = _actor(
        independent_review.get("reviewer") if isinstance(independent_review, Mapping) else None,
        "machine transport reviewer",
        role="independent_reviewer",
    )
    _distinct(reviewer, actor, "machine transport replay verifier")
    reviewed_at = _timestamp(
        independent_review.get("reviewed_at"), "transport replay reviewed_at"
    )
    evidence_as_of = _timestamp(receipt_facts.get("evidence_as_of"), "evidence_as_of")
    if (
        independent_review.get("decision") != "approved"
        or not checked_at <= reviewed_at <= evidence_as_of
    ):
        _fail("machine transport replay lacks a timely independent approval")

    result = {
        "schema_version": TRANSPORT_AUTHORITY_RESULT_SCHEMA,
        "theorem_id": theorem_id,
        "replay_receipt": {"path": receipt_path, "sha256": receipt_sha},
        "source": observed_source,
        "local_target": observed_target,
        "transport_artifact": {
            "path": artifact_path,
            "sha256": _digest(artifact_bytes),
            "declaration": artifact["declaration"],
            "declaration_type_sha256": type_sha,
            "terminal_proof_body_sha256": terminal_sha,
        },
        "provider_materialization": {
            "source_file_sha256": _digest(provider_bytes),
            "module": TRANSPORT_PROVIDER_MODULE,
            "declaration": observed_source["declaration"],
            "compiled_exit_code": provider_compile.returncode,
        },
        "semantic_dependency": {
            "target_declaration": observed_target["declaration"],
            "provider_declaration": observed_source["declaration"],
            "relation": "direct_proof_body_constant_dependency",
            "joint_kernel_exit_code": joint_replay.returncode,
            "joint_kernel_stdout_sha256": _digest(joint_replay.stdout),
            "joint_kernel_stderr_sha256": _digest(joint_replay.stderr),
        },
        "validator": {
            "path": validator_path,
            "sha256": validator["sha256"],
            "authority": validator["authority"],
        },
        "replay": {
            "command": command,
            "exit_code": replay_result.returncode,
            "stdout_sha256": _digest(replay_result.stdout),
            "stderr_sha256": _digest(replay_result.stderr),
            "output": {"path": output_path, "sha256": _digest(output_bytes)},
            "toolchain": toolchain,
            "dependency_lock_sha256": dependency_sha,
        },
        "trust_audit": {
            "permitted_axioms": axioms,
            "output": {"path": trust_output_path, "sha256": trust_output_sha},
            "placeholder_free": True,
            "unsafe_free": True,
            "oracle_free": True,
            "undeclared_axioms_free": True,
        },
        "prior_independent_review": {
            "reviewer": reviewer,
            "reviewed_at": independent_review["reviewed_at"],
            "decision": "approved",
        },
        "repository_revision": revision,
        "repository_access": "temporary_read_only_replay",
        "network_during_replay": False,
    }
    return _with_digest(result, "transport_verification_sha256")


def verify_external_machine_source(
    receipt_facts: Mapping[str, Any],
    *,
    repo_root: Path,
    verifier: Mapping[str, Any],
    command_runner: Callable[..., subprocess.CompletedProcess[bytes]] = _readonly_kernel_command,
    local_target_verifier: Callable[..., dict[str, Any]] = verify_local_lean_target,
    transport_command_runner: Callable[..., subprocess.CompletedProcess[bytes]] = (
        _readonly_transport_command
    ),
) -> dict[str, Any]:
    """Fetch an immutable revision and repeat its Lean kernel replay read-only."""
    actor = _actor(verifier, "focus verifier")
    if actor["role"] not in {"scheduler_focus_verifier", "independent_reviewer"}:
        _fail("focus verifier role is not authoritative")
    local_target_result = local_target_verifier(
        repo_root, receipt_facts, verifier=actor, command_runner=command_runner
    )
    machine = receipt_facts.get("machine_proof")
    source = machine.get("source") if isinstance(machine, Mapping) else None
    if not isinstance(source, Mapping):
        _fail("exact admission lacks an external machine source")
    evidence_class = receipt_facts.get("machine_evidence_class")
    pinned_provider: dict[str, str] | None = None
    pinned_authority_result: dict[str, Any] | None = None
    if evidence_class in {"exact_pinned_closure", "exact_external_unintegrated"}:
        _verify_machine_pre_stage1_provenance(
            repo_root,
            receipt_facts,
            source,
            verifier=actor,
            authority_revision=_git_text(repo_root, "rev-parse", "HEAD^{commit}"),
        )
    if evidence_class == "exact_pinned_closure":
        pinned_provider = _pinned_manifest_provider(
            repo_root,
            str(receipt_facts.get("repository_base_revision", "")),
            source,
        )
        pinned_authority_result = _verify_local_pinned_provider(
            repo_root,
            str(receipt_facts.get("repository_base_revision", "")),
            source,
            pinned_provider,
            command_runner=command_runner,
        )
    elif evidence_class == "exact_external_unintegrated":
        if source.get("match_kind") == "checked_transport":
            _fail(
                "checked transport is not admissible for an unintegrated external source; "
                "pin the provider into the authoritative root closure first"
            )
        _reject_authoritative_external_identity(repo_root, source.get("repository"))
    if source.get("formal_system") != "Lean 4":
        _fail("automatic focus admission supports only independently replayed Lean 4 sources")
    repository = source.get("repository")
    revision = source.get("revision")
    if (
        not isinstance(repository, str)
        or not repository
        or "\x00" in repository
        or not isinstance(revision, str)
        or GIT_OID_RE.fullmatch(revision) is None
    ):
        _fail("external source repository or revision is not immutable")
    file_path = _safe_relative(source.get("file_path"), "external machine source")
    command = _canonical_kernel_command(
        source.get("kernel_replay", {}).get("command"),
        file_path=file_path,
        module=source.get("module"),
    )
    with tempfile.TemporaryDirectory(prefix="stage1-focus-source-") as directory:
        checkout = Path(directory) / "source"
        clone = subprocess.run(
            ["git", "clone", "--no-checkout", "--", repository, str(checkout)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if clone.returncode:
            _fail("external immutable source cannot be cloned")
        resolved = _git_text(checkout, "rev-parse", "--verify", f"{revision}^{{commit}}")
        if resolved != revision:
            _fail("external source revision is not a full canonical commit")
        if evidence_class == "exact_external_unintegrated":
            _reject_authoritative_external_identity(
                repo_root,
                repository,
                checkout,
                revision=resolved,
                source_path=file_path,
            )
        _run_git(checkout, ["checkout", "--detach", revision])
        if _git_text(checkout, "status", "--porcelain"):
            _fail("external source checkout is not clean")
        archive = _run_git(checkout, ["archive", "--format=tar", revision]).stdout
        tree = _git_text(checkout, "rev-parse", f"{revision}^{{tree}}")
        archive_sha = _digest(archive)
        source_identity = source.get("tree_or_archive_sha256")
        if archive_sha != source.get("tree_or_archive_sha256"):
            if _digest(tree.encode("ascii")) != source_identity:
                _fail("external source tree/archive digest is stale")
        path = checkout / file_path
        current = checkout
        for component in PurePosixPath(file_path).parts:
            current /= component
            if current.is_symlink():
                _fail("external source path traverses a symlink")
        if not path.is_file():
            _fail("external source file is missing")
        data = path.read_bytes()
        file_sha = _digest(data)
        if file_sha != source.get("file_sha256"):
            _fail("external source file digest is stale")
        body_sha, text = _declaration_region(data, str(source.get("declaration", "")))
        terminal = source.get("terminal_proof_body")
        if (
            not isinstance(terminal, Mapping)
            or terminal.get("locator") != source.get("declaration")
            or terminal.get("sha256") != body_sha
        ):
            _fail("terminal proof body identity does not bind the external declaration bytes")
        if PROHIBITED_LEAN_TOKENS.search(text):
            _fail("external proof source contains a prohibited construct")
        target = receipt_facts.get("target_binding")
        match_kind = source.get("match_kind")
        if not isinstance(target, Mapping) or target.get("status") != "verified":
            _fail("external source lacks a verified bound local target")
        if match_kind not in {"exact", "checked_transport"}:
            _fail("external source lacks an exact or checked-transport match kind")
        if source.get("formal_system") != target.get("formal_system"):
            _fail(
                "cross-formal-system checked transport requires a generic provider replay "
                "authority and is not yet supported"
            )
        toolchain, dependency_lock_sha = _dependency_identity(checkout)
        if evidence_class == "exact_pinned_closure":
            # A pinned proof's authority is the repository root manifest and
            # live cache.  A provider-local Lake project is never an authority.
            replay_authority = _repository_replay_authority(
                repo_root, str(receipt_facts.get("repository_base_revision", ""))
            )
            if (
                replay_authority.get("dependency_packages_sha256") is None
                or replay_authority.get("compiled_cache_sha256") is None
                or replay_authority.get("compiled_cache_file_count", 0) < 1
            ):
                _fail(
                    "exact pinned closure lacks a verified Lake manifest/package closure"
                )
            local_authority = local_target_result.get("replay_authority", {})
            if (
                not isinstance(pinned_provider, Mapping)
                or local_authority.get("dependency_lock_sha256")
                != pinned_provider.get("manifest_sha256")
                or local_authority.get("dependency_packages_sha256") is None
                or local_authority.get("compiled_cache_sha256") is None
            ):
                _fail(
                    "exact pinned closure is not in the local manifest-bound replay authority"
                )
            if not isinstance(pinned_authority_result, Mapping):
                _fail("exact pinned closure lacks a root-manifest provider replay")
            toolchain = str(local_target_result.get("toolchain", toolchain))
            dependency_lock_sha = str(pinned_provider.get("manifest_sha256"))
        else:
            try:
                replay_authority, _external_toolchain, _external_cache = (
                    stage1_lean_authority.build_project_lean_authority(checkout)
                )
            except Exception as exc:
                raise AdmissionError(
                    f"external pinned Lean replay authority is invalid: {exc}"
                ) from exc
        replay = command_runner(
            checkout, list(command), timeout=KERNEL_REPLAY_TIMEOUT_SECONDS
        )
        if replay.returncode != 0:
            _fail("independent external kernel replay failed")
        if evidence_class == "exact_pinned_closure":
            if not isinstance(pinned_authority_result, Mapping):
                _fail("exact pinned closure lacks a root-manifest provider replay")
            type_sha = str(pinned_authority_result["declaration_type_sha256"])
            axioms = list(pinned_authority_result["permitted_axioms"])
            trust_output_sha = str(
                pinned_authority_result["trust_audit_output_sha256"]
            )
        else:
            type_sha, axioms, trust_output_sha = _lean_probe(
                checkout,
                source_path=path,
                declaration=str(source.get("declaration", "")),
                command_runner=command_runner,
            )
        authority_result = _authority_result(
            source=source,
            file_path=file_path,
            file_sha=file_sha,
            body_sha=body_sha,
            type_sha=type_sha,
            axioms=axioms,
            trust_output_sha=trust_output_sha,
            toolchain=toolchain,
            dependency_lock_sha=dependency_lock_sha,
            replay_authority=replay_authority,
        )
        stdout_sha = _digest(replay.stdout)
        compatibility = source.get("compatibility")
        if (
            not isinstance(compatibility, Mapping)
            or compatibility.get("toolchain") != authority_result["toolchain"]
            or compatibility.get("dependency_lock_sha256")
            != authority_result["dependency_lock_sha256"]
        ):
            _fail("kernel authority result disagrees with compatibility facts")
        if stdout_sha != source.get("kernel_replay", {}).get("output_sha256"):
            _fail("independent kernel replay output digest changed")
        observed_source_sha = authority_result["declaration_type_sha256"]
        observed_target_sha = local_target_result["declaration_type_sha256"]
        statement_target_sha = receipt_facts.get("statement_binding", {}).get(
            "target_declaration_type_sha256"
        )
        if statement_target_sha != observed_target_sha:
            _fail("statement binding does not name the observed local target type")
        transport_result: dict[str, Any] | None = None
        if match_kind == "exact":
            if source.get("transport_evidence"):
                _fail("exact external source must not claim transport evidence")
            if observed_source_sha != observed_target_sha:
                _fail("external source declaration type is not exact for the bound local target")
        else:
            if observed_source_sha == observed_target_sha:
                _fail("checked transport is redundant for identical observed proof types")
            transport_result = _verify_machine_transport_replay(
                repo_root,
                receipt_facts,
                actor=actor,
                external_result=authority_result,
                local_target_result=local_target_result,
                transport_command_runner=transport_command_runner,
                lean_command_runner=command_runner,
                external_checkout=checkout,
                external_source_path=path,
            )
        observed = {
            "schema_version": VERIFICATION_SCHEMA,
            "theorem_id": receipt_facts.get("theorem_id"),
            "verification_kind": "external_lean_kernel_replay",
            "verifier": actor,
            "repository": repository,
            "resolved_revision": resolved,
            "archive_sha256": archive_sha,
            "resolved_tree": tree,
            "file_path": file_path,
            "file_sha256": file_sha,
            "terminal_proof_body_sha256": body_sha,
            "kernel_command": list(command),
            "kernel_exit_code": replay.returncode,
            "kernel_stdout_sha256": stdout_sha,
            "kernel_authority_result": authority_result,
            "local_target_authority_result": local_target_result,
            "kernel_stderr_sha256": _digest(replay.stderr),
            "repository_access": "temporary_read_only_replay",
            "network_during_replay": False,
        }
        if transport_result is not None:
            observed["transport_authority_result"] = transport_result
    return _with_digest(observed, "verification_sha256")


def _facts_verification(
    receipt_facts: Mapping[str, Any],
    *,
    verifier: Mapping[str, Any],
    human_source_review: Mapping[str, Any] | None,
) -> dict[str, Any]:
    actor = _actor(verifier, "focus verifier")
    return _with_digest(
        {
            "schema_version": VERIFICATION_SCHEMA,
            "theorem_id": receipt_facts.get("theorem_id"),
            "verification_kind": "head_bound_research_facts",
            "verifier": actor,
            "evidence_bindings_sha256": _digest(
                _canonical_json(receipt_facts.get("evidence_bindings"))
            ),
            "human_source_review": human_source_review,
            "repository_access": "authoritative_head_read_only",
            "network_during_replay": False,
        },
        "verification_sha256",
    )


def _verify_receipt_facts(
    root: Path,
    receipt_facts: Mapping[str, Any],
    *,
    verifier: Mapping[str, Any],
    human_source_review: Mapping[str, Any] | None,
    external_verifier: Callable[..., dict[str, Any]] = verify_external_machine_source,
) -> dict[str, Any]:
    if receipt_facts.get("execution_disposition") == "organize_or_integrate":
        result = external_verifier(receipt_facts, repo_root=root, verifier=verifier)
    else:
        result = _facts_verification(
            receipt_facts,
            verifier=verifier,
            human_source_review=human_source_review,
        )
    if not isinstance(result, dict) or result.get("schema_version") != VERIFICATION_SCHEMA:
        _fail("focus verification result schema is unsupported")
    _embedded_digest(result, "verification_sha256", "focus verification")
    if result.get("theorem_id") != receipt_facts.get("theorem_id"):
        _fail("focus verification targets another theorem")
    if result.get("verifier") != dict(verifier):
        _fail("focus verification principal is stale")
    transport_authority = result.pop("transport_authority_result", None)
    source = receipt_facts.get("machine_proof", {}).get("source")
    match_kind = source.get("match_kind") if isinstance(source, Mapping) else None
    verification_support: Any = human_source_review
    if match_kind == "checked_transport":
        if not isinstance(transport_authority, Mapping):
            _fail("checked transport verification lacks replayed transport authority")
        _embedded_digest(
            transport_authority,
            "transport_verification_sha256",
            "machine transport authority",
        )
        # `authorityVerification` predates checked transports and deliberately
        # leaves this evidence envelope untyped.  Keep the full replay result,
        # not a label or digest-only escape, inside each independently signed
        # authority record while preserving the v1 receipt schema.
        verification_support = {
            "human_source_review": human_source_review,
            "machine_transport_authority": dict(transport_authority),
        }
    elif transport_authority is not None:
        _fail("non-transport verification unexpectedly carries transport authority")
    result = _with_digest(
        {
            key: value
            for key, value in result.items()
            if key != "verification_sha256"
        }
        | {"human_source_review": verification_support},
        "verification_sha256",
    )
    return result


def _transport_authority_from_verification(
    verification: Mapping[str, Any],
) -> Mapping[str, Any] | None:
    support = verification.get("human_source_review")
    if not isinstance(support, Mapping) or set(support) != {
        "human_source_review",
        "machine_transport_authority",
    }:
        return None
    result = support.get("machine_transport_authority")
    if not isinstance(result, Mapping):
        return None
    _embedded_digest(
        result,
        "transport_verification_sha256",
        "machine transport authority",
    )
    return result


def _receipt_facts(
    proposal: Mapping[str, Any], decision: Mapping[str, Any]
) -> dict[str, Any]:
    disposition = str(proposal["execution_disposition"])
    frontier_request = proposal.get("frontier_request")
    authorization = decision.get("frontier_authorization")
    frontier: dict[str, Any] | None = None
    if disposition == "frontier_exception":
        if (
            not isinstance(frontier_request, dict)
            or set(frontier_request) != FRONTIER_REQUEST_FIELDS
            or not isinstance(authorization, dict)
            or set(authorization) != FRONTIER_AUTHORIZATION_FIELDS
        ):
            _fail("frontier admission lacks separate worker facts and scheduler authorization")
        probability = authorization.get("completion_probability")
        if (
            not isinstance(probability, (int, float))
            or isinstance(probability, bool)
            or probability < 0.70
            or probability > 1.0
        ):
            _fail("frontier admission probability is below 0.70")
        validator = authorization.get("validator")
        if (
            not isinstance(validator, Mapping)
            or not isinstance(validator.get("path"), str)
            or validator.get("command") != ["python3", validator.get("path")]
        ):
            _fail(
                "frontier validator command must be exactly ['python3', validator.path]"
            )
        frontier = {
            "scheduler_owner": "scheduler_master_lane",
            "root_obligation": frontier_request["root_obligation"],
            "assigned_worker": authorization["assigned_worker"],
            "estimator": authorization["estimator"],
            "estimated_at": authorization["estimated_at"],
            "estimation_method": authorization["estimation_method"],
            "completion_probability": probability,
            "evidence": frontier_request["evidence"],
            "budget": authorization["budget"],
            "milestones": authorization["milestones"],
            "validator": authorization["validator"],
            "stop_conditions": authorization["stop_conditions"],
            "attempt_limit": authorization["attempt_limit"],
            "lease_expires_at": authorization["lease_expires_at"],
            "revocation_route": "scheduler_master_lane",
            # Added only after the independent review binds the candidate.
            "independent_review": None,
        }
    elif frontier_request is not None or authorization is not None:
        _fail("non-frontier admission carries frontier authority")
    return {
        "schema_version": focus_eligibility.SCHEMA_VERSION,
        "theorem_id": proposal["theorem_id"],
        "requirements_authority": focus_eligibility.REQUIREMENTS_AUTHORITY,
        "repository_base_revision": proposal["repository_base_revision"],
        "scheduler_owner": "scheduler_master_lane",
        "evidence_as_of": proposal["evidence_as_of"],
        "expires_at": decision["expires_at"],
        "machine_evidence_class": proposal["machine_evidence_class"],
        "execution_disposition": disposition,
        "human_proof": proposal["human_proof"],
        "target_binding": proposal["target_binding"],
        "statement_binding": proposal["statement_binding"],
        "machine_proof": proposal["machine_proof"],
        "repository_gap": proposal["repository_gap"],
        "evidence_bindings": proposal["evidence_bindings"],
        "disposition_basis": None,
        "frontier_exception": frontier,
        "invalidation_conditions": proposal["invalidation_conditions"],
    }


def _candidate_path(runtime: Path, theorem_id: str, proposal_sha256: str) -> Path:
    return runtime / "focus-admission" / "candidates" / f"{theorem_id}-{proposal_sha256}.json"


def _review_path(runtime: Path, candidate_sha256: str) -> Path:
    return runtime / "focus-admission" / "reviews" / f"{candidate_sha256}.json"


def _frontier_review_input_path(runtime: Path, candidate_sha256: str) -> Path:
    return (
        runtime / "focus-admission" / "frontier-review-inputs"
        / f"{candidate_sha256}.json"
    )


def _load_frontier_review_input(
    root: Path,
    runtime: Path,
    candidate: Mapping[str, Any],
    reviewer: Mapping[str, Any],
) -> dict[str, Any]:
    """Load the reviewer's separately authored substantive frontier decision."""
    path = _frontier_review_input_path(runtime, str(candidate["candidate_sha256"]))
    if not path.exists() and not path.is_symlink():
        _fail("frontier independent review input path is not scheduler-canonical")
    value = _load_runtime_record(
        path,
        runtime / "focus-admission" / "frontier-review-inputs",
        "frontier independent review input",
        root=root,
        allowed_owner_uids=_reviewer_owner_uids(root),
        allowed_caller_uids=_reviewer_owner_uids(root),
    )
    if set(value) != FRONTIER_REVIEW_INPUT_FIELDS:
        _fail("frontier independent review input fields are not canonical")
    _embedded_digest(value, "review_input_sha256", "frontier independent review input")
    facts = candidate.get("receipt_facts", {})
    frontier = facts.get("frontier_exception") if isinstance(facts, Mapping) else None
    if not isinstance(frontier, Mapping):
        _fail("non-frontier candidate has a frontier independent review input")
    probability = value.get("assessed_completion_probability")
    comparables = value.get("comparables")
    findings = value.get("findings")
    authored_at = _timestamp(value.get("authored_at"), "frontier review authored_at")
    estimated_at = _timestamp(frontier.get("estimated_at"), "frontier estimated_at")
    if (
        value.get("schema_version") != FRONTIER_REVIEW_INPUT_SCHEMA
        or value.get("candidate_sha256") != candidate.get("candidate_sha256")
        or value.get("theorem_id") != candidate.get("theorem_id")
        or value.get("reviewer") != reviewer
        or value.get("decision") not in {"approved", "rejected"}
        or not isinstance(probability, (int, float))
        or isinstance(probability, bool)
        or not 0.0 <= float(probability) <= 1.0
        or not isinstance(value.get("estimation_method_assessment"), str)
        or not value["estimation_method_assessment"].strip()
        or not isinstance(comparables, list)
        or not comparables
        or any(not isinstance(row, str) or not row.strip() for row in comparables)
        or not isinstance(findings, list)
        or not findings
        or any(not isinstance(row, str) or not row.strip() for row in findings)
        or authored_at < estimated_at
        or authored_at > _utc_now()
    ):
        _fail("frontier independent review input is not substantive or timely")
    expected_assessments = {
        "budget_assessment": frontier.get("budget"),
        "milestone_assessment": frontier.get("milestones"),
        "validator_assessment": frontier.get("validator"),
        "stop_condition_assessment": frontier.get("stop_conditions"),
    }
    if any(value.get(key) != expected for key, expected in expected_assessments.items()):
        _fail("frontier independent review does not bind the authorized controls")
    if value.get("decision") == "approved" and float(probability) < 0.70:
        _fail("frontier independent review probability is below 0.70")
    return value


def _durable_frontier_review(
    review_input: Mapping[str, Any], *, reviewed_at: str
) -> dict[str, Any]:
    """Embed the complete substantive review in the signed theorem receipt."""
    durable = json.loads(json.dumps(review_input, ensure_ascii=True, allow_nan=False))
    durable["reviewed_at"] = reviewed_at
    return durable


def _issuance_path(runtime: Path, candidate_sha256: str) -> Path:
    return runtime / "focus-admission" / "issuances" / f"{candidate_sha256}.json"


def _prepare_runtime_directory(root: Path, runtime: Path, relative: str) -> Path:
    """Create one canonical scheduler directory and verify its secure lineage."""
    _canonical_runtime(root, runtime)
    owner = _repo_owner(root)
    clean_relative = PurePosixPath(relative)
    if clean_relative.is_absolute() or any(
        component in {"", ".", ".."} for component in clean_relative.parts
    ):
        _fail("focus admission runtime directory is malformed")
    directory = os.open(runtime, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in clean_relative.parts:
            try:
                child = os.open(
                    component,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=directory,
                )
            except FileNotFoundError:
                os.mkdir(component, mode=0o700, dir_fd=directory)
                child = os.open(
                    component,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=directory,
                )
            except OSError as exc:
                raise AdmissionError("focus admission runtime directory is unsafe") from exc
            metadata = os.fstat(child)
            if (
                not stat.S_ISDIR(metadata.st_mode)
                or metadata.st_uid != owner
                or stat.S_IMODE(metadata.st_mode) & 0o022
            ):
                os.close(child)
                _fail("focus admission runtime lineage is not owner-controlled")
            os.close(directory)
            directory = child
    finally:
        os.close(directory)
    _canonical_runtime(
        root,
        runtime,
        required_descendants=(clean_relative,),
    )
    return runtime.joinpath(*clean_relative.parts)


def prepare_focus_admission(
    repo_root: Path | str,
    runtime_root: Path | str,
    proposal_path: Path | str,
    scheduler_decision: Mapping[str, Any],
    *,
    external_verifier: Callable[..., dict[str, Any]] = verify_external_machine_source,
) -> Path:
    """Create one immutable scheduler candidate from HEAD worker facts.

    Focus admission is scheduler maintenance, not execution.  The caller must
    serialize it with the scheduler lock, but an operator PAUSED marker does
    not block evidence verification or publication.
    """
    root = _root(repo_root)
    runtime = Path(runtime_root).absolute()
    _prepare_runtime_directory(root, runtime, "focus-admission/candidates")
    authority = _git_text(root, "rev-parse", "HEAD^{commit}")
    proposal, proposal_sha, relative = _load_proposal(root, proposal_path)
    try:
        focus_eligibility.require_frozen_target_member(
            root, str(proposal["theorem_id"])
        )
    except focus_eligibility.EligibilityError as exc:
        raise AdmissionError(f"focus proposal is not a frozen Stage1 target: {exc}") from exc
    _require_existing_receipt_issued(
        root, runtime, authority, str(proposal["theorem_id"])
    )
    decision = _decision(
        scheduler_decision,
        theorem_id=str(proposal["theorem_id"]),
        authority_revision=authority,
        proposal_sha256=proposal_sha,
        proposal_author=proposal["author"],
    )
    expected_decision = ALLOWED_ADMISSION_DECISIONS[str(proposal["execution_disposition"])]
    if decision.get("admission_decision") != expected_decision:
        _fail("scheduler decision does not match the proposed disposition")
    if proposal.get("execution_disposition") == "organize_or_integrate":
        try:
            focus_eligibility.require_integration_root_unaccepted(
                root, str(proposal["theorem_id"])
            )
        except focus_eligibility.EligibilityError as exc:
            raise AdmissionError(f"ordinary integration is no longer admissible: {exc}") from exc
    verified_bindings, evidence_digests = _verify_bound_evidence(
        root, authority, str(proposal["theorem_id"]), proposal["evidence_bindings"]
    )
    # Git blob identities are candidate metadata. The receipt schema retains
    # only the proposal's path/SHA/role triples.
    facts = _receipt_facts(proposal, decision)
    source = facts.get("machine_proof", {}).get("source")
    if (
        facts.get("machine_evidence_class")
        in {"exact_pinned_closure", "exact_external_unintegrated"}
        and isinstance(source, Mapping)
    ):
        _verify_machine_pre_stage1_provenance(
            root,
            facts,
            source,
            proposal_author=proposal["author"],
            verifier=decision["issuer"],
            authority_revision=authority,
        )
    human_source_review = _human_source_review(
        root,
        authority,
        facts,
        proposal_author=proposal["author"],
        scheduler_issuer=decision["issuer"],
        admission_reviewer=decision["reviewer"],
        authorization=decision.get("human_source_authorization"),
    )
    verifier = {
        "id": f"scheduler-focus-verifier@{authority[:12]}",
        "role": "scheduler_focus_verifier",
    }
    verification = _verify_receipt_facts(
        root,
        facts,
        verifier=verifier,
        human_source_review=human_source_review,
        external_verifier=external_verifier,
    )
    candidate = _with_digest(
        {
            "schema_version": CANDIDATE_SCHEMA,
            "theorem_id": proposal["theorem_id"],
            "authority_revision": authority,
            "proposal": {
                "path": relative,
                "sha256": proposal_sha,
                "author": proposal["author"],
                "submitted_at": proposal["submitted_at"],
            },
            "scheduler_issuer": decision["issuer"],
            "designated_reviewer": decision["reviewer"],
            "admission_decision": decision["admission_decision"],
            "receipt_facts": facts,
            "receipt_facts_sha256": _digest(_canonical_json(facts)),
            "verified_evidence_bindings": verified_bindings,
            "evidence_sha256s": evidence_digests,
            "human_source_authorization": decision.get(
                "human_source_authorization"
            ),
            "verified_human_source_review": human_source_review,
            "candidate_verification": verification,
            "prepared_at": _utc_text(_utc_now()),
        },
        "candidate_sha256",
    )
    if _git_text(root, "rev-parse", "HEAD^{commit}") != authority:
        _fail("authoritative HEAD changed during focus candidate preparation")
    path = _candidate_path(runtime, str(proposal["theorem_id"]), proposal_sha)
    _immutable_write(path, candidate, "focus candidate", owner_uid=_repo_owner(root))
    return path


def _reviewer_owner_uids(root: Path) -> set[int]:
    owners = {_repo_owner(root)}
    configured = os.environ.get("STAGE1_REVIEWER_UID")
    if configured is not None:
        if not configured.isdecimal() or int(configured) < 1:
            _fail("configured independent reviewer UID is malformed")
        owners.add(int(configured))
    return owners


def _load_runtime_record(
    path: Path,
    expected_parent: Path,
    label: str,
    *,
    root: Path | None = None,
    allowed_owner_uids: set[int] | None = None,
    allowed_caller_uids: set[int] | None = None,
) -> dict[str, Any]:
    expected_parent = expected_parent.absolute()
    if root is None:
        try:
            root = expected_parent.parents[3]
        except IndexError as exc:
            raise AdmissionError(f"{label} path is not scheduler-canonical") from exc
        root = _root(root)
    runtime = root.joinpath(*CANONICAL_RUNTIME_RELATIVE.parts)
    try:
        parent_relative = expected_parent.relative_to(runtime).as_posix()
    except ValueError as exc:
        raise AdmissionError(f"{label} path is not scheduler-canonical") from exc
    data = _read_secure_runtime_file(
        root,
        runtime,
        path,
        expected_parent=parent_relative,
        label=label,
        max_bytes=MAX_REVIEW_OUTPUT_BYTES,
        allowed_owner_uids=allowed_owner_uids,
        allowed_caller_uids=allowed_caller_uids,
    )
    value = _parse_json(data, label)
    if data != _pretty_json(value):
        _fail(f"{label} is not canonical pretty JSON")
    return value


def _reload_candidate(
    root: Path,
    runtime: Path,
    path: Path,
    *,
    allowed_caller_uids: set[int] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate = _load_runtime_record(
        path,
        runtime / "focus-admission" / "candidates",
        "focus candidate",
        root=root,
        allowed_owner_uids={_repo_owner(root)},
        allowed_caller_uids=allowed_caller_uids,
    )
    if candidate.get("schema_version") != CANDIDATE_SCHEMA:
        _fail("focus candidate schema is unsupported")
    candidate_sha = _embedded_digest(candidate, "candidate_sha256", "focus candidate")
    proposal_binding = candidate.get("proposal")
    if not isinstance(proposal_binding, dict):
        _fail("focus candidate lacks its proposal binding")
    proposal, proposal_sha, relative = _load_proposal(root, str(proposal_binding.get("path")))
    if (
        proposal_sha != proposal_binding.get("sha256")
        or relative != proposal_binding.get("path")
        or proposal.get("author") != proposal_binding.get("author")
        or candidate.get("authority_revision") != _git_text(root, "rev-parse", "HEAD^{commit}")
        or candidate.get("theorem_id") != proposal.get("theorem_id")
        or candidate.get("receipt_facts_sha256")
        != _digest(_canonical_json(candidate.get("receipt_facts")))
    ):
        _fail("focus candidate proposal, authority, or receipt facts are stale")
    expected_name = f"{candidate['theorem_id']}-{proposal_sha}.json"
    if path.name != expected_name or candidate_sha != candidate["candidate_sha256"]:
        _fail("focus candidate path does not bind its identity")
    _, evidence_digests = _verify_bound_evidence(
        root,
        str(candidate["authority_revision"]),
        str(candidate["theorem_id"]),
        candidate.get("receipt_facts", {}).get("evidence_bindings"),
    )
    if evidence_digests != candidate.get("evidence_sha256s"):
        _fail("focus candidate evidence changed after preparation")
    verification = candidate.get("candidate_verification")
    if not isinstance(verification, dict):
        _fail("focus candidate lacks scheduler verification")
    _embedded_digest(verification, "verification_sha256", "candidate verification")
    return candidate, proposal


def review_focus_admission(
    repo_root: Path | str,
    runtime_root: Path | str,
    candidate_path: Path | str,
    reviewer: Mapping[str, Any],
    *,
    approve: bool = True,
    external_verifier: Callable[..., dict[str, Any]] = verify_external_machine_source,
    reviewer_signing_key_path: Path | str | None = None,
) -> Path:
    """Repeat candidate verification as a distinct repository-read-only actor."""
    root = _root(repo_root)
    reviewer_uids = _reviewer_owner_uids(root)
    if os.geteuid() != _repo_owner(root) and os.geteuid() not in reviewer_uids:
        _fail("focus admission caller is not the configured independent reviewer")
    runtime = _canonical_runtime(
        root,
        runtime_root,
        required_descendants=(PurePosixPath("focus-admission/candidates"),),
        allowed_caller_uids=reviewer_uids,
    )
    candidate, proposal = _reload_candidate(
        root,
        runtime,
        Path(candidate_path),
        allowed_caller_uids=reviewer_uids,
    )
    actor = _actor(reviewer, "focus admission reviewer", role="independent_reviewer")
    if actor != candidate.get("designated_reviewer"):
        _fail("focus review principal is not the designated independent reviewer")
    _distinct(actor, proposal["author"], "proposal reviewer")
    _distinct(actor, candidate["scheduler_issuer"], "admission reviewer")
    facts = candidate["receipt_facts"]
    if facts.get("execution_disposition") == "organize_or_integrate":
        try:
            focus_eligibility.require_integration_root_unaccepted(
                root, str(candidate["theorem_id"])
            )
        except focus_eligibility.EligibilityError as exc:
            raise AdmissionError(f"ordinary integration is no longer admissible: {exc}") from exc
    human_source_review = _human_source_review(
        root,
        str(candidate["authority_revision"]),
        facts,
        proposal_author=proposal["author"],
        scheduler_issuer=candidate["scheduler_issuer"],
        admission_reviewer=candidate["designated_reviewer"],
        authorization=candidate.get("human_source_authorization"),
    )
    if human_source_review != candidate.get("verified_human_source_review"):
        _fail("candidate human source review binding is stale")
    frontier = facts.get("frontier_exception")
    frontier_review_input: dict[str, Any] | None = None
    if isinstance(frontier, dict):
        assigned = _actor(frontier.get("assigned_worker"), "assigned frontier worker")
        estimator = _actor(frontier.get("estimator"), "frontier estimator")
        _distinct(actor, assigned, "frontier reviewer")
        _distinct(actor, estimator, "frontier reviewer")
        _distinct(proposal["author"], estimator, "frontier estimator")
        frontier_review_input = _load_frontier_review_input(
            root, runtime, candidate, actor
        )
    reviewed_at = _utc_now()
    findings: list[str] = []
    review_verification: dict[str, Any] | None = None
    decision = "rejected"
    if approve and (
        frontier_review_input is None
        or frontier_review_input.get("decision") == "approved"
    ):
        try:
            review_verification = _verify_receipt_facts(
                root,
                facts,
                verifier=actor,
                human_source_review=human_source_review,
                external_verifier=external_verifier,
            )
            decision = "approved"
        except (AdmissionError, focus_eligibility.EligibilityError) as exc:
            findings.append(str(exc))
    else:
        findings.extend(
            frontier_review_input.get("findings", [])
            if frontier_review_input is not None
            else ["independent reviewer rejected the candidate"]
        )
    if decision == "approved" and not isinstance(review_verification, dict):
        _fail("approved focus review lacks independent verification")
    review_body = {
            "schema_version": REVIEW_SCHEMA,
            "candidate_sha256": candidate["candidate_sha256"],
            "proposal_sha256": candidate["proposal"]["sha256"],
            "receipt_facts_sha256": candidate["receipt_facts_sha256"],
            "theorem_id": candidate["theorem_id"],
            "reviewer": actor,
            "reviewed_at": _utc_text(reviewed_at),
            "decision": decision,
            "repository_access": "read_only",
            "candidate_verification_sha256": candidate["candidate_verification"][
                "verification_sha256"
            ],
            "review_verification": review_verification,
            "evidence_sha256s": candidate["evidence_sha256s"],
            "findings": findings,
            "frontier_review_input": frontier_review_input,
            "unsigned_review_sha256": None,
            "receipt_payload_sha256": None,
            "reviewer_key_id": None,
            "reviewer_signature": None,
    }
    if decision == "approved":
        review_body["receipt_generated_at"] = _utc_text(
            max(_utc_now(), reviewed_at)
        )
        unsigned_review = dict(review_body)
        for field in (
            "unsigned_review_sha256", "receipt_payload_sha256",
            "reviewer_key_id", "reviewer_signature",
        ):
            unsigned_review.pop(field)
        unsigned_review_sha = _digest(_canonical_json(unsigned_review))
        # The signed payload contains review_sha256. Use the immutable digest
        # of the unsigned review body, avoiding a signature/hash recursion.
        review_for_payload = dict(review_body)
        review_for_payload["review_sha256"] = unsigned_review_sha
        review_for_payload["unsigned_review_sha256"] = unsigned_review_sha
        receipt_payload = _final_receipt_payload(candidate, review_for_payload)
        signing_key_path = _signing_key_path(
            reviewer_signing_key_path,
            "STAGE1_FOCUS_REVIEWER_SIGNING_KEY",
            DEFAULT_REVIEWER_SIGNING_KEY,
        )
        reviewer_key = _load_signing_key(
            signing_key_path, "independent reviewer focus signing key"
        )
        reviewer_key_id, reviewer_principal_id, reviewer_public = focus_eligibility._trust_anchor(
            root, "independent_review", active_only=True
        )
        if actor["id"] != reviewer_principal_id:
            _fail("focus reviewer identity is not authorized by the active trust anchor")
        if reviewer_key.public_key().public_bytes_raw() != reviewer_public.public_bytes_raw():
            _fail("reviewer signing key does not match the active trust anchor")
        review_body.update(
            unsigned_review_sha256=unsigned_review_sha,
            receipt_payload_sha256=_digest(_canonical_json(receipt_payload)),
            reviewer_key_id=reviewer_key_id,
            reviewer_signature=reviewer_key.sign(
                _signature_payload(receipt_payload, candidate, review_for_payload)
            ).hex(),
        )
    review = _with_digest(review_body, "review_sha256")
    if _git_text(root, "rev-parse", "HEAD^{commit}") != candidate["authority_revision"]:
        _fail("authoritative HEAD changed during independent focus review")
    path = _review_path(runtime, str(candidate["candidate_sha256"]))
    if os.geteuid() == _repo_owner(root):
        _prepare_runtime_directory(root, runtime, "focus-admission/reviews")
    else:
        _canonical_runtime(
            root,
            runtime,
            required_descendants=(PurePosixPath("focus-admission/reviews"),),
            allowed_caller_uids=reviewer_uids,
        )
    _immutable_write(path, review, "focus review", owner_uid=os.geteuid())
    return path


def _final_receipt_payload(
    candidate: Mapping[str, Any], review: Mapping[str, Any]
) -> dict[str, Any]:
    """Derive the complete receipt facts before adding the signature envelope."""
    facts = json.loads(json.dumps(candidate["receipt_facts"]))
    scheduler_verification = candidate.get("candidate_verification")
    reviewer_verification = review.get("review_verification")
    if facts.get("execution_disposition") == "organize_or_integrate":
        if not isinstance(scheduler_verification, Mapping) or not isinstance(
            reviewer_verification, Mapping
        ):
            _fail("exact admission lacks both authority verification results")
        scheduler_external = scheduler_verification.get("kernel_authority_result")
        reviewer_external = reviewer_verification.get("kernel_authority_result")
        scheduler_local = scheduler_verification.get("local_target_authority_result")
        reviewer_local = reviewer_verification.get("local_target_authority_result")
        scheduler_transport = _transport_authority_from_verification(
            scheduler_verification
        )
        reviewer_transport = _transport_authority_from_verification(
            reviewer_verification
        )
        if (
            scheduler_external != reviewer_external
            or scheduler_local != reviewer_local
            or not isinstance(scheduler_external, Mapping)
            or not isinstance(scheduler_local, Mapping)
        ):
            _fail("scheduler and reviewer observed different exact proof facts")
        # Replace worker-asserted semantic fingerprints with independently
        # observed kernel facts before any receipt can become authoritative.
        observed_target_sha = scheduler_local.get("declaration_type_sha256")
        observed_source_sha = scheduler_external.get("declaration_type_sha256")
        source = facts["machine_proof"]["source"]
        match_kind = source.get("match_kind")
        if match_kind == "exact":
            if observed_target_sha != observed_source_sha:
                _fail("observed local target and external proof types are not exact")
            if scheduler_transport is not None or reviewer_transport is not None:
                _fail("exact admission unexpectedly carries transport authority")
        elif match_kind == "checked_transport":
            if observed_target_sha == observed_source_sha:
                _fail("checked transport is redundant for identical observed proof types")
            if (
                not isinstance(scheduler_transport, Mapping)
                or scheduler_transport != reviewer_transport
                or scheduler_transport.get("source", {}).get(
                    "declaration_type_sha256"
                )
                != observed_source_sha
                or scheduler_transport.get("local_target", {}).get(
                    "declaration_type_sha256"
                )
                != observed_target_sha
                or scheduler_transport.get("transport_artifact", {}).get(
                    "declaration_type_sha256"
                )
                != observed_target_sha
            ):
                _fail(
                    "scheduler and reviewer did not independently replay the exact "
                    "source-to-local-target transport"
                )
        else:
            _fail("external proof has an unsupported statement match kind")
        facts["target_binding"]["declaration_type_sha256"] = observed_target_sha
        facts["statement_binding"]["target_declaration_type_sha256"] = observed_target_sha
        source["declaration_type_sha256"] = observed_source_sha
        source["file_sha256"] = scheduler_external["file_sha256"]
        source["terminal_proof_body"]["sha256"] = (
            scheduler_external["terminal_proof_body_sha256"]
        )
        facts["admission_authority"] = {
            "scheduler_verification": scheduler_verification,
            "reviewer_verification": reviewer_verification,
            "observed_facts_sha256": _digest(
                _canonical_json(
                    {
                        "external": scheduler_external,
                        "local_target": scheduler_local,
                    }
                )
            ),
        }
    else:
        facts["admission_authority"] = None
    # Review envelope hashes/signatures are intentionally not semantic receipt
    # inputs. Only the independently observed facts and timestamp are.
    review = dict(review)
    if review.get("unsigned_review_sha256") is not None:
        review["review_sha256"] = review["unsigned_review_sha256"]
    reviewed_at = review["reviewed_at"]
    generated_at = review.get("receipt_generated_at")
    if generated_at is None:
        generated_at = _utc_text(
            max(_utc_now(), _timestamp(reviewed_at, "reviewed_at"))
        )
    elif _timestamp(generated_at, "receipt generated_at") < _timestamp(
        reviewed_at, "reviewed_at"
    ):
        _fail("receipt generated_at predates its independent review")
    facts["generated_at"] = generated_at
    facts["admission_review"] = {
        "author": candidate["scheduler_issuer"],
        "reviewer": review["reviewer"],
        "reviewed_at": reviewed_at,
        "decision": candidate["admission_decision"],
    }
    facts["issuance_authority"] = None
    if facts.get("execution_disposition") == "frontier_exception":
        review_input = review.get("frontier_review_input")
        if not isinstance(review_input, Mapping):
            _fail("frontier receipt lacks its substantive independent review")
        durable_review = _durable_frontier_review(
            review_input, reviewed_at=reviewed_at
        )
        if (
            durable_review.get("reviewer") != review.get("reviewer")
            or durable_review.get("decision") != "approved"
            or _timestamp(
                durable_review.get("authored_at"), "frontier review authored_at"
            )
            > _timestamp(reviewed_at, "frontier reviewed_at")
        ):
            _fail("frontier review envelope and substantive review disagree")
        facts["frontier_exception"]["independent_review"] = durable_review
    return facts


def _signature_payload(
    receipt_payload: Mapping[str, Any],
    candidate: Mapping[str, Any],
    review: Mapping[str, Any],
) -> bytes:
    review_binding = review.get("unsigned_review_sha256")
    if review_binding is None:
        review_binding = review.get("review_sha256")
    return _canonical_json(
        {
            "schema_version": SIGNATURE_PAYLOAD_SCHEMA,
            "theorem_id": candidate["theorem_id"],
            "receipt_path": focus_eligibility.receipt_relative_path(
                str(candidate["theorem_id"])
            ),
            "receipt_payload_sha256": _digest(_canonical_json(receipt_payload)),
            "authority_revision": candidate["authority_revision"],
            "candidate_sha256": candidate["candidate_sha256"],
            "review_sha256": review_binding,
        }
    )


def _final_receipt(
    root: Path,
    candidate: Mapping[str, Any],
    review: Mapping[str, Any],
    *,
    scheduler_signing_key_path: Path | str,
) -> dict[str, Any]:
    facts = _final_receipt_payload(candidate, review)
    receipt_payload_sha = _digest(_canonical_json(facts))
    if (
        review.get("receipt_payload_sha256") != receipt_payload_sha
        or not isinstance(review.get("reviewer_signature"), str)
        or re.fullmatch(r"[0-9a-f]{128}", review["reviewer_signature"]) is None
    ):
        _fail("independent review did not sign the exact final receipt payload")
    signed = _signature_payload(facts, candidate, review)
    reviewer_key_id, reviewer_principal_id, reviewer_key = focus_eligibility._trust_anchor(
        root,
        "independent_review",
        key_id=str(review.get("reviewer_key_id", "")),
        issued_at=_timestamp(review["reviewed_at"], "reviewed_at"),
    )
    if review.get("reviewer", {}).get("id") != reviewer_principal_id:
        _fail("independent review identity is not authorized by its trust anchor")
    try:
        reviewer_key.verify(bytes.fromhex(review["reviewer_signature"]), signed)
    except (ValueError, focus_eligibility.InvalidSignature) as exc:
        raise AdmissionError("independent review signature is invalid") from exc
    scheduler_key_id, scheduler_principal_id, scheduler_public_key = focus_eligibility._trust_anchor(
        root, "scheduler_issuance", active_only=True
    )
    if candidate.get("scheduler_issuer", {}).get("id") != scheduler_principal_id:
        _fail("scheduler issuer identity is not authorized by the active trust anchor")
    scheduler_key = _load_signing_key(
        scheduler_signing_key_path, "scheduler focus signing key"
    )
    if scheduler_key.public_key().public_bytes_raw() != scheduler_public_key.public_bytes_raw():
        _fail("scheduler signing key does not match the active trust anchor")
    scheduler_signature = scheduler_key.sign(signed).hex()
    generated_at = str(facts["generated_at"])
    issuance = _with_digest(
        {
            "schema_version": ISSUANCE_SCHEMA,
            "theorem_id": candidate["theorem_id"],
            "authority_revision": candidate["authority_revision"],
            "candidate_sha256": candidate["candidate_sha256"],
            "review_sha256": review["review_sha256"],
            "unsigned_review_sha256": review["unsigned_review_sha256"],
            "proposal_sha256": candidate["proposal"]["sha256"],
            "receipt_facts_sha256": candidate["receipt_facts_sha256"],
            "scheduler_issuer": candidate["scheduler_issuer"],
            "reviewer": review["reviewer"],
            "candidate_verification_sha256": candidate["candidate_verification"][
                "verification_sha256"
            ],
            "review_verification_sha256": review["review_verification"][
                "verification_sha256"
            ],
            "receipt_path": focus_eligibility.receipt_relative_path(
                str(candidate["theorem_id"])
            ),
            "published_at": generated_at,
            "state": "published",
            "receipt_payload_sha256": receipt_payload_sha,
            "scheduler_key_id": scheduler_key_id,
            "reviewer_key_id": reviewer_key_id,
            "scheduler_signature": scheduler_signature,
            "reviewer_signature": review["reviewer_signature"],
        },
        "issuance_sha256",
    )
    facts["issuance_authority"] = {
        "schema_version": ISSUANCE_AUTHORITY_SCHEMA,
        "authority_revision": candidate["authority_revision"],
        "candidate_sha256": candidate["candidate_sha256"],
        "proposal_sha256": candidate["proposal"]["sha256"],
        "receipt_facts_sha256": candidate["receipt_facts_sha256"],
        "scheduler_issuer": candidate["scheduler_issuer"],
        "review_sha256": review["review_sha256"],
        "unsigned_review_sha256": review["unsigned_review_sha256"],
        "reviewer": review["reviewer"],
        "candidate_verification_sha256": candidate["candidate_verification"][
            "verification_sha256"
        ],
        "review_verification_sha256": review["review_verification"][
            "verification_sha256"
        ],
        "issuance": issuance,
    }
    return facts


class _PublicationTransaction:
    def __init__(self, root: Path, wal: Path, authority_revision: str) -> None:
        self.root = root
        self.wal = wal
        self.authority_revision = authority_revision
        self.snapshots: dict[Path, tuple[bytes | None, int | None]] = {}

    def _persist(self) -> None:
        rows = []
        for path, (data, mode) in self.snapshots.items():
            if not path.absolute().is_relative_to(self.root):
                _fail("focus admission transaction path escapes repository")
            rows.append(
                {
                    "path": path.absolute().relative_to(self.root).as_posix(),
                    "existed": data is not None,
                    "mode": mode,
                    "content_base64": base64.b64encode(data or b"").decode("ascii"),
                }
            )
        _atomic_write(
            self.wal,
            _pretty_json(
                {
                    "schema_version": WAL_SCHEMA,
                    "authority_revision": self.authority_revision,
                    "snapshots": rows,
                }
            ),
        )
        self.wal.chmod(0o600)
        if self.wal.stat(follow_symlinks=False).st_uid != _repo_owner(self.root):
            _fail("focus admission recovery journal has the wrong owner")

    def snapshot(self, path: Path) -> None:
        path = path.absolute()
        if path in self.snapshots:
            return
        if path.is_symlink() or (path.exists() and not path.is_file()):
            _fail("focus admission transaction destination is unsafe")
        self.snapshots[path] = (
            path.read_bytes() if path.is_file() else None,
            path.stat().st_mode & 0o7777 if path.is_file() else None,
        )
        self._persist()

    def rollback(self) -> None:
        errors: list[str] = []
        for path, (data, mode) in reversed(list(self.snapshots.items())):
            try:
                if path.is_symlink() or path.is_file():
                    path.unlink()
                elif path.exists():
                    raise OSError(f"rollback destination became a directory: {path}")
                if data is not None:
                    _atomic_write(path, data)
                    if mode is not None:
                        path.chmod(mode)
            except OSError as exc:
                errors.append(str(exc))
        self.wal.unlink(missing_ok=True)
        if errors:
            raise AdmissionError("focus admission rollback failed: " + "; ".join(errors))

    def commit(self) -> None:
        self.wal.unlink(missing_ok=True)


def recover_focus_admission_wal(repo_root: Path | str, runtime_root: Path | str) -> bool:
    root = _root(repo_root)
    runtime = _canonical_runtime(root, runtime_root)
    wal = runtime / "focus-admission-wal.json"
    try:
        os.stat(wal, follow_symlinks=False)
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise AdmissionError("focus admission recovery journal is unsafe") from exc
    record = _parse_json(
        _read_secure_runtime_file(
            root,
            runtime,
            wal,
            expected_parent=PurePosixPath("."),
            label="focus admission recovery journal",
            max_bytes=MAX_WAL_BYTES,
            allowed_owner_uids={_repo_owner(root)},
        ),
        "focus admission recovery journal",
    )
    if set(record) != WAL_FIELDS or record.get("schema_version") != WAL_SCHEMA:
        _fail("focus admission recovery journal fields or schema are unsupported")
    if record.get("authority_revision") != _git_text(root, "rev-parse", "HEAD^{commit}"):
        _fail("focus admission recovery authority changed")
    rows = record.get("snapshots")
    if not isinstance(rows, list) or not rows or len(rows) > 4:
        _fail("focus admission recovery snapshots are malformed")
    plan: list[tuple[Path, bytes | None, int | None]] = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != WAL_SNAPSHOT_FIELDS:
            _fail("focus admission recovery row is malformed")
        relative = _safe_relative(row.get("path"), "focus admission recovery path")
        if relative in seen:
            _fail("focus admission recovery path is duplicated")
        seen.add(relative)
        allowed = (
            re.fullmatch(r"Stage1_Instances/THM-M-[0-9]{4}/focus-eligibility\.json", relative)
            is not None
            or relative == "Docs/Stage1_Theorem_DAG_v2.json"
            or relative == "Docs/Stage1_Blueprint_v2.md"
            or re.fullmatch(
                re.escape(runtime.relative_to(root).as_posix())
                + r"/focus-admission/issuances/[0-9a-f]{64}\.json",
                relative,
            )
            is not None
        )
        if not allowed:
            _fail("focus admission recovery journal contains an unsafe path")
        if relative == "Docs/Stage1_Blueprint_v2.md":
            authoritative_blueprint = _run_git(
                root,
                ["show", f"{record['authority_revision']}:{relative}"],
            ).stdout
        existed = row.get("existed")
        encoded = row.get("content_base64")
        mode = row.get("mode")
        if (
            not isinstance(existed, bool)
            or not isinstance(encoded, str)
            or (existed and (not isinstance(mode, int) or isinstance(mode, bool)))
            or (not existed and mode is not None)
            or (isinstance(mode, int) and (mode < 0 or mode > 0o777))
        ):
            _fail("focus admission recovery row is incomplete")
        try:
            data = base64.b64decode(encoded, validate=True)
        except (ValueError, TypeError) as exc:
            raise AdmissionError("focus admission recovery payload is malformed") from exc
        if len(data) > MAX_WAL_BYTES or (not existed and data):
            _fail("focus admission recovery missing file carries bytes")
        if relative == "Docs/Stage1_Blueprint_v2.md" and (
            not existed or data != authoritative_blueprint
        ):
            _fail("focus admission recovery blueprint bytes are not authoritative")
        plan.append((root / relative, data if existed else None, mode))
    for path, data, mode in reversed(plan):
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.exists():
            _fail("focus admission recovery destination became a directory")
        if data is not None:
            _atomic_write(path, data)
            if isinstance(mode, int):
                path.chmod(mode)
    wal.unlink()
    return True


def _default_regenerate(root: Path) -> None:
    result = subprocess.run(
        ["python3", "Docs/tools/generate_stage1_theorem_dag_v2.py"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        _fail(f"focus theorem DAG regeneration failed: {(result.stderr or result.stdout).strip()}")


def _default_validate_graph(root: Path) -> None:
    result = subprocess.run(
        ["python3", "Docs/tools/check_stage1_theorem_dag_v2.py"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        _fail(f"focus theorem DAG validation failed: {(result.stderr or result.stdout).strip()}")


def publish_focus_admission(
    repo_root: Path | str,
    runtime_root: Path | str,
    candidate_path: Path | str,
    review_path: Path | str,
    *,
    regenerate: Callable[[Path], None] = _default_regenerate,
    validate_graph: Callable[[Path], None] = _default_validate_graph,
    scheduler_signing_key_path: Path | str | None = None,
) -> Path:
    """Validate, publish, regenerate, and verify one admission atomically.

    This maintenance transaction may run while execution is PAUSED.  It only
    publishes admission evidence and its read-only DAG projection; it never
    claims work, launches workers, integrates handoffs, or advances the SSOT.
    """
    root = _root(repo_root)
    runtime = _canonical_runtime(root, runtime_root)
    recover_focus_admission_wal(root, runtime)
    candidate, proposal = _reload_candidate(root, runtime, Path(candidate_path))
    if candidate.get("receipt_facts", {}).get("execution_disposition") == "organize_or_integrate":
        try:
            focus_eligibility.require_integration_root_unaccepted(
                root, str(candidate["theorem_id"])
            )
        except focus_eligibility.EligibilityError as exc:
            raise AdmissionError(f"ordinary integration is no longer admissible: {exc}") from exc
    try:
        focus_eligibility.require_frozen_target_member(
            root, str(candidate["theorem_id"])
        )
    except focus_eligibility.EligibilityError as exc:
        raise AdmissionError(f"focus candidate is not a frozen Stage1 target: {exc}") from exc
    review = _load_runtime_record(
        Path(review_path),
        runtime / "focus-admission" / "reviews",
        "focus review",
        root=root,
        allowed_owner_uids={_repo_owner(root), *_reviewer_owner_uids(root)},
    )
    if set(review) != REVIEW_FIELDS or review.get("schema_version") != REVIEW_SCHEMA:
        _fail("focus review fields or schema are not canonical")
    _embedded_digest(review, "review_sha256", "focus review")
    verification = review.get("review_verification")
    if (
        review.get("decision") != "approved"
        or review.get("candidate_sha256") != candidate["candidate_sha256"]
        or review.get("proposal_sha256") != candidate["proposal"]["sha256"]
        or review.get("receipt_facts_sha256") != candidate["receipt_facts_sha256"]
        or review.get("theorem_id") != candidate["theorem_id"]
        or review.get("reviewer") != candidate["designated_reviewer"]
        or review.get("repository_access") != "read_only"
        or review.get("candidate_verification_sha256")
        != candidate["candidate_verification"]["verification_sha256"]
        or review.get("evidence_sha256s") != candidate["evidence_sha256s"]
        or review.get("findings") != []
        or not isinstance(verification, dict)
    ):
        _fail("focus review did not approve the exact current candidate and evidence")
    _embedded_digest(verification, "verification_sha256", "review verification")
    if verification.get("verifier") != review["reviewer"]:
        _fail("focus review verification was not performed by the reviewer")
    _distinct(review["reviewer"], proposal["author"], "proposal reviewer")
    _distinct(review["reviewer"], candidate["scheduler_issuer"], "admission reviewer")
    receipt = _final_receipt(
        root,
        candidate,
        review,
        scheduler_signing_key_path=_signing_key_path(
            scheduler_signing_key_path,
            "STAGE1_FOCUS_SCHEDULER_SIGNING_KEY",
            DEFAULT_SCHEDULER_SIGNING_KEY,
        ),
    )
    now = _utc_now()
    try:
        # Structural validation precedes publication; the external issuance
        # anchor is created atomically with the receipt below.
        focus_eligibility.validate_receipt(
            root,
            str(candidate["theorem_id"]),
            receipt,
            as_of=now,
            runtime_root=runtime,
            require_issuance=True,
        )
    except focus_eligibility.EligibilityError as exc:
        raise AdmissionError(f"final focus receipt is invalid: {exc}") from exc
    authority = str(candidate["authority_revision"])
    if _git_text(root, "rev-parse", "HEAD^{commit}") != authority:
        _fail("authoritative HEAD changed before focus publication")
    receipt_relative = focus_eligibility.receipt_relative_path(str(candidate["theorem_id"]))
    receipt_path = root / receipt_relative
    graph = root / "Docs" / "Stage1_Theorem_DAG_v2.json"
    blueprint = root / focus_eligibility.REQUIREMENTS_AUTHORITY
    status_path = _issuance_path(runtime, str(candidate["candidate_sha256"]))
    _prepare_runtime_directory(root, runtime, "focus-admission/issuances")
    blueprint_before = blueprint.read_bytes()
    transaction = _PublicationTransaction(
        root, runtime / "focus-admission-wal.json", authority
    )
    for path in (receipt_path, graph, blueprint, status_path):
        transaction.snapshot(path)
    try:
        _atomic_write(receipt_path, _pretty_json(receipt))
        receipt_sha = _digest(receipt_path.read_bytes())
        # The signed receipt was validated before publication from identical
        # canonical bytes. Its envelope cannot include this byte digest without
        # introducing an impossible self-reference.
        # Runtime status is only a cache of the durable issuance embedded in
        # the theorem-owned receipt. Deleting `.cron` cannot revoke admission.
        issuance = receipt["issuance_authority"]["issuance"]
        _atomic_write(status_path, _pretty_json(issuance))
        status_path.chmod(0o600)
        projection = focus_eligibility.evaluate_target(
            root,
            str(candidate["theorem_id"]),
            as_of=now,
            expected_receipt_sha256=receipt_sha,
        )
        if projection.get("valid") is not True:
            _fail(
                "published focus receipt does not produce a valid projection: "
                + ",".join(str(value) for value in projection.get("reason_codes", []))
            )
        regenerate(root)
        if blueprint.read_bytes() != blueprint_before:
            _fail("focus publication changed frozen blueprint checklist bytes")
        validate_graph(root)
        try:
            graph_value = json.loads(graph.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise AdmissionError("regenerated theorem DAG is malformed") from exc
        rows = [
            row
            for row in graph_value.get("theorems", [])
            if isinstance(row, dict) and row.get("theorem_id") == candidate["theorem_id"]
        ]
        if len(rows) != 1 or rows[0].get("focus_eligibility") != projection:
            _fail("regenerated theorem DAG does not project the exact published receipt")
        if _git_text(root, "rev-parse", "HEAD^{commit}") != authority:
            _fail("authoritative HEAD changed during focus publication")
        transaction.commit()
    except BaseException:
        transaction.rollback()
        raise
    return status_path


def load_scheduler_decision(
    runtime_root: Path | str,
    path: Path | str,
    *,
    repo_root: Path | str | None = None,
) -> dict[str, Any]:
    runtime = Path(runtime_root).absolute()
    if repo_root is None:
        try:
            repo_root = runtime.parents[1]
        except IndexError as exc:
            raise AdmissionError("scheduler runtime path is not canonical") from exc
    root = _root(repo_root)
    _canonical_runtime(
        root,
        runtime,
        required_descendants=(PurePosixPath("focus-admission/decisions"),),
    )
    data = _read_secure_runtime_file(
        root,
        runtime,
        Path(path),
        expected_parent=PurePosixPath("focus-admission/decisions"),
        label="scheduler-owned staging decision",
        max_bytes=MAX_REVIEW_OUTPUT_BYTES,
        allowed_owner_uids={_repo_owner(root)},
    )
    result = _parse_json(data, "scheduler focus decision")
    if data != _pretty_json(result):
        _fail("scheduler focus decision is not canonical pretty JSON")
    return result
