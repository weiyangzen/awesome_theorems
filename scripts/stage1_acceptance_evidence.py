#!/usr/bin/env python3
"""Fail-closed evidence binding and hermetic replay for Stage1 acceptance.

This module deliberately does not mutate the Stage1 SSOT.  It turns one
worker-self-tested item into immutable inputs which the scheduler can give to
an independent reviewer and, later, to the master acceptance transaction.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tempfile
import time
from typing import Any, Mapping, NoReturn, Sequence


CONTRACT_PATH = "Docs/Stage1_Phase_Acceptance_Contracts.json"
CONTRACT_SCHEMA = "stage1-phase-acceptance-contracts/1.0"
ROLE_MAP_SCHEMA = "stage1-phase-artifact-role-map/1.0"
REVIEW_MANIFEST_SCHEMA = "stage1-master-review-input/1.0"
REPLAY_RESULT_SCHEMA = "stage1-authority-replay-result/1.0"
SEMANTIC_RESULT_SCHEMA = "stage1-replay-semantic-decision/1.0"
VALIDATOR_SEMANTIC_SCHEMA = "stage1-validator-semantic-result/1.0"
ITEM_RE = re.compile(r"^S56-M-[0-9]{4}-[A-Z_]+$")
THEOREM_RE = re.compile(r"^THM-M-[0-9]{4}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_OID_RE = re.compile(r"^[0-9a-f]{40,64}$")
WORKER_VERDICTS = {
    "accepted",
    "accepted_audit_only",
    "no_state_change",
    "blocked",
    "rejected",
}
REVIEW_VERDICTS = {"phase_accepted", "repair_required", "rejected"}
PHASES = {
    "intake",
    "statement",
    "anchor_audit",
    "obligation_tree",
    "proof",
    "validation",
    "release",
}
NEGATIVE_SEMANTIC_TOKENS = {
    "blocked",
    "blocking",
    "failed",
    "failure",
    "open",
    "rejected",
    "stale",
    "superseded",
    "revoked",
    "timeout",
    "timed_out",
}
POSITIVE_SEMANTIC_STATUSES = {"passed", "accepted", "phase_accepted"}
POSITIVE_SEMANTIC_VERDICTS = {"phase_accepted"}
VALIDATOR_SEMANTIC_STATUSES = POSITIVE_SEMANTIC_STATUSES | {
    "blocked",
    "failed",
    "open",
    "rejected",
    "stale",
}
VALIDATOR_SEMANTIC_VERDICTS = POSITIVE_SEMANTIC_VERDICTS | {
    "blocked",
    "repair_required",
    "rejected",
}
MAX_REPLAY_OUTPUT_BYTES = 16 * 1024 * 1024
RUNTIME_MOUNTS = ("/usr/bin", "/usr/lib", "/usr/lib64", "/usr/share")
RUNTIME_EXECUTABLES = ("/usr/bin/python3", "/usr/bin/bash")


class EvidenceError(RuntimeError):
    """The supplied evidence does not prove the requested binding."""


def _fail(message: str) -> NoReturn:
    raise EvidenceError(message)


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _run_git(
    repo: Path, argv: Sequence[str], *, check: bool = True, input_bytes: bytes | None = None
) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *argv],
        cwd=repo,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        _fail(f"git {' '.join(argv)} failed: {detail}")
    return result


def _git_text(repo: Path, *argv: str) -> str:
    return _run_git(repo, argv).stdout.decode("utf-8", "strict").strip()


def _require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(f"{label} must be a JSON object")
    return value


def _json_object(data: bytes, label: str) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                _fail(f"{label} contains duplicate key {key!r}")
            result[key] = value
        return result

    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"{label} is not valid UTF-8 JSON") from exc
    return _require_object(value, label)


def _repository_root(repo: Path | str) -> Path:
    """Return an absolute repository path whose entire path is symlink-free."""

    raw = Path(os.path.abspath(os.fspath(repo)))
    descriptor = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for component in raw.parts[1:]:
            try:
                child = os.open(
                    component,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=descriptor,
                )
            except OSError as exc:
                raise EvidenceError(
                    "repository path contains a missing, non-directory, or symlink component"
                ) from exc
            os.close(descriptor)
            descriptor = child
        metadata = os.fstat(descriptor)
        if not stat.S_ISDIR(metadata.st_mode):
            _fail("repository root is not a directory")
    finally:
        os.close(descriptor)
    return raw


def _read_regular_at(root: Path, relative: str, label: str) -> bytes:
    """Read a regular file while rejecting symlinks in every path component."""

    relative = _safe_relative(relative, label)
    components = PurePosixPath(relative).parts
    descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in components[:-1]:
            try:
                child = os.open(
                    component,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=descriptor,
                )
            except OSError as exc:
                raise EvidenceError(f"{label} has an unsafe parent path") from exc
            os.close(descriptor)
            descriptor = child
        try:
            opened = os.open(
                components[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=descriptor
            )
        except OSError as exc:
            raise EvidenceError(f"{label} is missing or unsafe") from exc
        try:
            before = os.fstat(opened)
            if not stat.S_ISREG(before.st_mode):
                _fail(f"{label} is not a regular file")
            chunks: list[bytes] = []
            while True:
                chunk = os.read(opened, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            after = os.fstat(opened)
            if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            ):
                _fail(f"{label} changed while it was being read")
            return b"".join(chunks)
        finally:
            os.close(opened)
    finally:
        os.close(descriptor)


def _safe_relative(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        _fail(f"{label} is not a safe repository-relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or value != path.as_posix() or any(
        part in {"", ".", ".."} for part in path.parts
    ):
        _fail(f"{label} is not a canonical repository-relative path")
    return value


def _render_theorem_path(pattern: str, theorem_id: str, label: str) -> str:
    rendered = pattern.replace("{theorem_id}", theorem_id)
    if "{" in rendered or "}" in rendered:
        _fail(f"{label} contains an unresolved placeholder")
    return _safe_relative(rendered, label)


def _require_item_identity(item_id: str, theorem_id: str, phase_row: Mapping[str, Any]) -> None:
    if not ITEM_RE.fullmatch(item_id) or not THEOREM_RE.fullmatch(theorem_id):
        _fail("item or theorem identity is malformed")
    suffix = phase_row.get("item_suffix")
    expected = f"{theorem_id.replace('THM-', 'S56-')}-{suffix}"
    if not isinstance(suffix, str) or item_id != expected:
        _fail("item identity does not match theorem and phase contract")


def _require_ancestor(repo: Path, ancestor: str, descendant: str, label: str) -> None:
    result = _run_git(
        repo, ["merge-base", "--is-ancestor", ancestor, descendant], check=False
    )
    if result.returncode != 0:
        _fail(f"{label} is not an ancestor of authoritative HEAD")


def _require_embedded_digest(value: Mapping[str, Any], field: str, label: str) -> None:
    claimed = value.get(field)
    if not isinstance(claimed, str) or not SHA256_RE.fullmatch(claimed):
        _fail(f"{label} lacks a canonical {field}")
    unhashed = dict(value)
    del unhashed[field]
    if sha256_bytes(canonical_json(unhashed)) != claimed:
        _fail(f"{label} {field} does not bind its content")


def _head_bytes(repo: Path, revision: str, relative: str, label: str) -> bytes:
    relative = _safe_relative(relative, label)
    result = _run_git(repo, ["show", f"{revision}:{relative}"], check=False)
    if result.returncode:
        _fail(f"{label} is not tracked at {revision}")
    return result.stdout


def _blob_oid(repo: Path, revision: str, relative: str, label: str) -> str:
    relative = _safe_relative(relative, label)
    result = _run_git(repo, ["rev-parse", "--verify", f"{revision}:{relative}"], check=False)
    if result.returncode:
        _fail(f"{label} is not tracked at {revision}")
    oid = result.stdout.decode("ascii", "strict").strip()
    if not GIT_OID_RE.fullmatch(oid):
        _fail(f"{label} does not resolve to a Git object")
    kind = _git_text(repo, "cat-file", "-t", oid)
    if kind != "blob":
        _fail(f"{label} is not a regular Git blob")
    return oid


def _head_mode(repo: Path, revision: str, relative: str, label: str) -> str:
    result = _run_git(repo, ["ls-tree", revision, "--", relative], check=False)
    if result.returncode or not result.stdout:
        _fail(f"{label} is not tracked at {revision}")
    rows = result.stdout.decode("utf-8", "strict").splitlines()
    exact = [row for row in rows if row.split("\t", 1)[-1] == relative]
    if len(exact) != 1:
        _fail(f"{label} has ambiguous Git tree identity")
    fields = exact[0].split("\t", 1)[0].split()
    if len(fields) != 3 or fields[1] != "blob":
        _fail(f"{label} is not a Git blob")
    if fields[0] == "120000":
        _fail(f"{label} is a symlink")
    if fields[0] not in {"100644", "100755"}:
        _fail(f"{label} has unsafe Git mode {fields[0]}")
    return fields[0]


def _require_worktree_matches_head(
    repo: Path, relative: str, expected: bytes, label: str
) -> None:
    actual = _read_regular_at(repo, relative, f"{label} in the scheduler checkout")
    if actual != expected:
        _fail(f"{label} differs from authoritative HEAD")


def load_head_contract(
    repo: Path | str,
    expected_sha256: str,
    *,
    revision: str = "HEAD",
) -> dict[str, Any]:
    """Load the contract strictly from Git HEAD and verify its pinned digest.

    The worktree copy is also required to equal HEAD so the scheduler cannot
    accidentally review against a dirty or untracked replacement.
    """

    root = _repository_root(repo)
    if not SHA256_RE.fullmatch(expected_sha256):
        _fail("expected contract digest must be a lowercase SHA-256")
    head = _git_text(root, "rev-parse", "--verify", f"{revision}^{{commit}}")
    symbolic = _run_git(root, ["symbolic-ref", "-q", "HEAD"], check=False)
    if revision == "HEAD" and symbolic.returncode != 0:
        # A scheduler checkout is expected to be branch-owned.  Immutable
        # replay checkouts are loaded by explicit commit instead.
        _fail("authoritative scheduler HEAD is detached")
    data = _head_bytes(root, head, CONTRACT_PATH, "phase acceptance contract")
    if sha256_bytes(data) != expected_sha256:
        _fail("HEAD phase acceptance contract digest mismatch")
    _head_mode(root, head, CONTRACT_PATH, "phase acceptance contract")
    if revision == "HEAD":
        _require_worktree_matches_head(root, CONTRACT_PATH, data, "phase acceptance contract")
    contract = _json_object(data, "phase acceptance contract")
    if contract.get("schema_version") != CONTRACT_SCHEMA:
        _fail("phase acceptance contract schema is unsupported")
    phases = contract.get("phases")
    order = contract.get("phase_order")
    if not isinstance(phases, list) or not isinstance(order, list):
        _fail("phase acceptance contract is missing its phase order")
    names = [row.get("phase") if isinstance(row, dict) else None for row in phases]
    if names != order or len(set(names)) != len(names):
        _fail("phase acceptance contract phase rows are missing or ambiguous")
    artifact_policy = _require_object(contract.get("artifact_resolution"), "artifact policy")
    validator_policy = _require_object(contract.get("validator_selection"), "validator policy")
    if (
        artifact_policy.get("per_item_role_map_owner") != "scheduler_master_lane"
        or artifact_policy.get("selected_files_must_be_head_tracked") is not True
        or artifact_policy.get("selected_files_must_not_be_symlinks") is not True
        or validator_policy.get("owner") != "scheduler_master_lane"
        or validator_policy.get("worker_or_reviewer_may_select_argv") is not False
        or validator_policy.get("require_exactly_one_candidate") is not True
        or validator_policy.get("shell_interpolation") is not False
        or validator_policy.get("network_policy") != "denied"
    ):
        _fail("phase acceptance contract weakens scheduler-owned evidence selection")
    return {
        "revision": head,
        "git_tree": _git_text(root, "rev-parse", f"{head}^{{tree}}"),
        "path": CONTRACT_PATH,
        "sha256": expected_sha256,
        "git_blob": _blob_oid(root, head, CONTRACT_PATH, "phase acceptance contract"),
        "contract": contract,
    }


def _phase_contract(contract_record: Mapping[str, Any], phase: str) -> dict[str, Any]:
    contract = _require_object(contract_record.get("contract"), "contract record")
    rows = [
        row
        for row in contract.get("phases", [])
        if isinstance(row, dict) and row.get("phase") == phase
    ]
    if len(rows) != 1:
        _fail(f"phase {phase!r} is missing or ambiguous in the HEAD contract")
    return rows[0]


def _pointer_value(document: Mapping[str, Any], pointer: Any, label: str) -> Any:
    if not isinstance(pointer, str) or not pointer.startswith("/") or pointer == "/":
        _fail(f"{label} is not a valid JSON pointer")
    value: Any = document
    for raw in pointer[1:].split("/"):
        component = raw.replace("~1", "/").replace("~0", "~")
        if "~" in re.sub(r"~[01]", "", raw):
            _fail(f"{label} contains an invalid JSON pointer escape")
        if isinstance(value, dict):
            if component not in value:
                _fail(f"{label} is missing from the phase receipt")
            value = value[component]
        elif isinstance(value, list) and component.isdecimal():
            index = int(component)
            if index >= len(value):
                _fail(f"{label} is outside the phase receipt")
            value = value[index]
        else:
            _fail(f"{label} cannot be traversed in the phase receipt")
    return value


def _receipt_binding_rows(value: Any, label: str) -> list[dict[str, str | None]]:
    rows = value if isinstance(value, list) else [value]
    if not rows:
        _fail(f"{label} is empty")
    result: list[dict[str, str | None]] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            _fail(f"{label}[{index}] must be an object binding path and digest")
        allowed = {"path", "sha256", "git_blob", "role", "kind", "artifact_kind"}
        if set(row) - allowed:
            _fail(f"{label}[{index}] has unrecognized binding fields")
        relative = _safe_relative(row.get("path"), f"{label}[{index}].path")
        digest = row.get("sha256")
        blob = row.get("git_blob")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            _fail(f"{label}[{index}] lacks a complete sha256 binding")
        if blob is not None and (not isinstance(blob, str) or not GIT_OID_RE.fullmatch(blob)):
            _fail(f"{label}[{index}] has an invalid git_blob binding")
        result.append({"path": relative, "sha256": digest, "git_blob": blob})
    if len({row["path"] for row in result}) != len(result):
        _fail(f"{label} contains duplicate or ambiguous paths")
    return result


def _receipt_candidate(
    repo: Path, revision: str, phase_row: Mapping[str, Any], theorem_id: str
) -> tuple[str, bytes]:
    receipt_roles = [
        row
        for row in phase_row.get("required_artifact_roles", [])
        if isinstance(row, dict) and row.get("role") == "phase_receipt"
    ]
    if len(receipt_roles) != 1:
        _fail("phase contract does not define exactly one phase_receipt role")
    role = receipt_roles[0]
    if role.get("resolution") != "path_candidates":
        _fail("phase_receipt must be scheduler-selected from path candidates")
    matches: list[tuple[str, bytes]] = []
    for pattern in role.get("path_candidates", []):
        if not isinstance(pattern, str):
            _fail("phase_receipt contains a non-string path candidate")
        relative = _render_theorem_path(pattern, theorem_id, "phase receipt candidate")
        result = _run_git(repo, ["show", f"{revision}:{relative}"], check=False)
        if result.returncode == 0:
            _head_mode(repo, revision, relative, "phase receipt candidate")
            matches.append((relative, result.stdout))
    if len(matches) != 1:
        _fail(f"phase_receipt requires exactly one HEAD candidate, found {len(matches)}")
    return matches[0]


def resolve_role_map(
    repo: Path | str,
    contract_record: Mapping[str, Any],
    *,
    item_id: str,
    theorem_id: str,
    phase: str,
    base_revision: str,
) -> dict[str, Any]:
    """Resolve one scheduler-owned, content-bound role map from HEAD."""

    root = _repository_root(repo)
    head = _git_text(root, "rev-parse", "--verify", "HEAD^{commit}")
    if contract_record.get("revision") != head:
        _fail("contract record is not bound to current authoritative HEAD")
    base = _git_text(root, "rev-parse", "--verify", f"{base_revision}^{{commit}}")
    phase_row = _phase_contract(contract_record, phase)
    _require_item_identity(item_id, theorem_id, phase_row)
    _require_ancestor(root, base, head, "worker base")

    receipt_path, receipt_bytes = _receipt_candidate(root, head, phase_row, theorem_id)
    _require_worktree_matches_head(root, receipt_path, receipt_bytes, "phase receipt")
    receipt = _json_object(receipt_bytes, "phase receipt")
    for field, expected in (("item_id", item_id), ("theorem_id", theorem_id), ("phase", phase)):
        if receipt.get(field) != expected:
            _fail(f"phase receipt {field} does not match the selected item")
    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        _fail("phase receipt schema is not stage1-node-receipt/1.0")
    for pointer in phase_row.get("phase_receipt_required_fields", []):
        _pointer_value(receipt, pointer, f"required phase receipt field {pointer}")
    if "base_revision" in receipt and receipt.get("base_revision") != base:
        _fail("phase receipt base_revision disagrees with worker base")
    if "base_tree" in receipt:
        base_tree = _git_text(root, "rev-parse", f"{base}^{{tree}}")
        if receipt.get("base_tree") != base_tree:
            _fail("phase receipt base_tree disagrees with worker base")

    artifacts: list[dict[str, str]] = []
    seen_roles: set[str] = set()
    for raw_role in phase_row.get("required_artifact_roles", []):
        role = _require_object(raw_role, "artifact role")
        name = role.get("role")
        if not isinstance(name, str) or not name or name in seen_roles:
            _fail("artifact roles are missing or ambiguous")
        seen_roles.add(name)
        requirement = role.get("requirement")
        if requirement == "conditional":
            # Conditional presence cannot be inferred by filenames.  The
            # phase semantic gate decides applicability and must reject a
            # missing applicable role later; any present candidate is bound.
            optional = True
        elif requirement == "required":
            optional = False
        else:
            _fail(f"role {name} has unsupported requirement semantics")
        cardinality = role.get("cardinality")
        if cardinality not in {"exactly_one", "one_or_more"}:
            _fail(f"role {name} has unsupported cardinality")

        selected: list[dict[str, str | None]] = []
        resolution = role.get("resolution")
        if resolution == "path_candidates":
            for pattern in role.get("path_candidates", []):
                if not isinstance(pattern, str):
                    _fail(f"role {name} has a non-string candidate")
                relative = _render_theorem_path(pattern, theorem_id, f"role {name} candidate")
                result = _run_git(root, ["show", f"{head}:{relative}"], check=False)
                if result.returncode == 0:
                    selected.append(
                        {
                            "path": relative,
                            "sha256": sha256_bytes(result.stdout),
                            "git_blob": _blob_oid(root, head, relative, f"role {name}"),
                        }
                    )
                elif (root / relative).exists() or (root / relative).is_symlink():
                    _fail(f"role {name} has an untracked or non-HEAD candidate")
        elif resolution == "receipt_bound_paths":
            pointer = role.get("binding_pointer")
            value = _pointer_value(receipt, pointer, f"role {name} binding pointer")
            selected = _receipt_binding_rows(value, f"role {name} receipt binding")
        else:
            _fail(f"role {name} has unsupported resolution semantics")

        if optional and not selected:
            continue
        if cardinality == "exactly_one" and len(selected) != 1:
            _fail(f"role {name} requires exactly one artifact, found {len(selected)}")
        if cardinality == "one_or_more" and len(selected) < 1:
            _fail(f"role {name} requires one or more artifacts")
        if len({row["path"] for row in selected}) != len(selected):
            _fail(f"role {name} resolves ambiguously")

        for binding in selected:
            relative = str(binding["path"])
            head_bytes = _head_bytes(root, head, relative, f"role {name}")
            _head_mode(root, head, relative, f"role {name}")
            blob = _blob_oid(root, head, relative, f"role {name}")
            digest = sha256_bytes(head_bytes)
            if binding.get("sha256") != digest:
                _fail(f"role {name} receipt sha256 disagrees with HEAD")
            if binding.get("git_blob") not in {None, blob}:
                _fail(f"role {name} receipt Git blob disagrees with HEAD")
            _require_worktree_matches_head(root, relative, head_bytes, f"role {name}")
            artifacts.append(
                {"role": name, "path": relative, "sha256": digest, "git_blob": blob}
            )

    if not artifacts or len({(row["role"], row["path"]) for row in artifacts}) != len(artifacts):
        _fail("resolved role map is empty or ambiguous")
    role_map = {
        "schema_version": ROLE_MAP_SCHEMA,
        "item_id": item_id,
        "theorem_id": theorem_id,
        "phase": phase,
        "base_revision": base,
        "authority_revision": head,
        "contract_sha256": contract_record.get("sha256"),
        "contract_git_blob": contract_record.get("git_blob"),
        "phase_receipt_path": receipt_path,
        "phase_receipt_sha256": sha256_bytes(receipt_bytes),
        "artifacts": sorted(artifacts, key=lambda row: (row["role"], row["path"])),
    }
    role_map["manifest_sha256"] = sha256_bytes(canonical_json(role_map))
    return role_map


def select_validator_recipe(
    repo: Path | str,
    contract_record: Mapping[str, Any],
    *,
    item_id: str,
    theorem_id: str,
    phase: str,
    base_revision: str,
    require_base_blob_match: bool = True,
) -> dict[str, Any]:
    """Select exactly one validator and derive argv only from HEAD contract.

    ``require_base_blob_match=False`` is reserved for rechecking whether a
    completed review still names the unchanged current-HEAD recipe. Review
    allocation keeps the strict default and binds the validator to its worker
    base.
    """

    root = _repository_root(repo)
    head = _git_text(root, "rev-parse", "--verify", "HEAD^{commit}")
    if contract_record.get("revision") != head:
        _fail("validator contract is not bound to current authoritative HEAD")
    base = _git_text(root, "rev-parse", "--verify", f"{base_revision}^{{commit}}")
    phase_row = _phase_contract(contract_record, phase)
    _require_item_identity(item_id, theorem_id, phase_row)
    _require_ancestor(root, base, head, "worker base")
    matches: list[tuple[dict[str, Any], str, bytes, str]] = []
    for raw in phase_row.get("validator_candidates", []):
        candidate = _require_object(raw, "validator candidate")
        pattern = candidate.get("path_pattern")
        if not isinstance(pattern, str):
            _fail("validator candidate path pattern is malformed")
        relative = _render_theorem_path(pattern, theorem_id, "validator candidate")
        result = _run_git(root, ["show", f"{head}:{relative}"], check=False)
        if result.returncode == 0:
            mode = _head_mode(root, head, relative, "validator")
            matches.append((candidate, relative, result.stdout, mode))
        elif (root / relative).exists() or (root / relative).is_symlink():
            _fail("validator candidate exists in the worktree but is not HEAD-owned")
    if len(matches) != 1:
        _fail(f"validator requires exactly one HEAD candidate, found {len(matches)}")
    candidate, relative, data, mode = matches[0]
    head_blob = _blob_oid(root, head, relative, "validator")
    if require_base_blob_match:
        base_result = _run_git(
            root, ["rev-parse", "--verify", f"{base}:{relative}"], check=False
        )
        if base_result.returncode:
            _fail("selected validator did not exist at the worker base")
        base_blob = base_result.stdout.decode("ascii", "strict").strip()
        if base_blob != head_blob:
            _fail("selected validator HEAD blob differs from worker-base blob")
    _require_worktree_matches_head(root, relative, data, "validator")

    template = candidate.get("argv_template")
    if (
        not isinstance(template, list)
        or not template
        or any(not isinstance(part, str) or "\x00" in part for part in template)
        or sum(part.count("{validator_path}") for part in template) != 1
    ):
        _fail("validator argv template is malformed or not path-bound exactly once")
    argv = [part.replace("{validator_path}", relative) for part in template]
    if any("{" in part or "}" in part for part in argv):
        _fail("validator argv contains an unresolved contract placeholder")
    policy = _require_object(
        _require_object(contract_record.get("contract"), "contract").get("validator_selection"),
        "validator policy",
    )
    language = candidate.get("language")
    expected_template = _require_object(policy.get("argv_templates"), "argv templates").get(language)
    if template != expected_template:
        _fail("phase validator argv differs from the scheduler authority template")
    if argv[0] not in set(RUNTIME_EXECUTABLES):
        _fail("validator executable is outside the closed authority allowlist")
    recipe = {
        "item_id": item_id,
        "theorem_id": theorem_id,
        "phase": phase,
        "base_revision": base,
        "authority_revision": head,
        "contract_sha256": contract_record.get("sha256"),
        "validator_path": relative,
        "validator_sha256": sha256_bytes(data),
        "validator_git_blob": head_blob,
        "validator_git_mode": mode,
        "argv": argv,
        "cwd": policy.get("cwd"),
        "network_policy": policy.get("network_policy"),
        "repo_write_access": policy.get("repo_write_access"),
        "isolated_scratch_write_access": policy.get("isolated_scratch_write_access"),
        "shell_interpolation": policy.get("shell_interpolation"),
    }
    if (
        recipe["cwd"] != "."
        or recipe["network_policy"] != "denied"
        or recipe["repo_write_access"] is not False
        or recipe["isolated_scratch_write_access"] is not True
        or recipe["shell_interpolation"] is not False
    ):
        _fail("validator recipe weakens the authority replay sandbox")
    recipe["recipe_sha256"] = sha256_bytes(canonical_json(recipe))
    return recipe


def build_review_manifest(
    contract_record: Mapping[str, Any],
    role_map: Mapping[str, Any],
    validator_recipe: Mapping[str, Any],
    *,
    blueprint_sha256: str,
    theorem_dag_sha256: str,
    worker_claim_sha256: str,
    worker_status_sha256: str,
    worker_prompt_sha256: str,
    worker_goal_sha256: str,
    worker_handoff_sha256: str,
) -> dict[str, Any]:
    """Build the immutable content manifest consumed by a read-only review."""

    digests = {
        "blueprint_sha256": blueprint_sha256,
        "theorem_dag_sha256": theorem_dag_sha256,
        "worker_claim_sha256": worker_claim_sha256,
        "worker_status_sha256": worker_status_sha256,
        "worker_prompt_sha256": worker_prompt_sha256,
        "worker_goal_sha256": worker_goal_sha256,
        "worker_handoff_sha256": worker_handoff_sha256,
    }
    if any(not SHA256_RE.fullmatch(value) for value in digests.values()):
        _fail("review manifest contains a malformed input digest")
    identity = (role_map.get("item_id"), role_map.get("theorem_id"), role_map.get("phase"))
    if identity != (
        validator_recipe.get("item_id"),
        validator_recipe.get("theorem_id"),
        validator_recipe.get("phase"),
    ):
        _fail("role map and validator recipe identify different items")
    _require_embedded_digest(role_map, "manifest_sha256", "role map")
    _require_embedded_digest(validator_recipe, "recipe_sha256", "validator recipe")
    if role_map.get("base_revision") != validator_recipe.get("base_revision"):
        _fail("role map and validator recipe use different worker bases")
    if (
        role_map.get("authority_revision") != contract_record.get("revision")
        or validator_recipe.get("authority_revision") != contract_record.get("revision")
        or role_map.get("contract_sha256") != contract_record.get("sha256")
        or validator_recipe.get("contract_sha256") != contract_record.get("sha256")
    ):
        _fail("review evidence is not bound to one contract authority")
    manifest = {
        "schema_version": REVIEW_MANIFEST_SCHEMA,
        "item_id": identity[0],
        "theorem_id": identity[1],
        "phase": identity[2],
        "authority_revision": contract_record.get("revision"),
        "authority_tree": contract_record.get("git_tree"),
        "base_revision": role_map.get("base_revision"),
        "contract": {
            "path": contract_record.get("path"),
            "sha256": contract_record.get("sha256"),
            "git_blob": contract_record.get("git_blob"),
        },
        "role_map_sha256": role_map.get("manifest_sha256"),
        "validator_recipe_sha256": validator_recipe.get("recipe_sha256"),
        "artifact_bindings": role_map.get("artifacts"),
        **digests,
    }
    manifest["manifest_sha256"] = sha256_bytes(canonical_json(manifest))
    return manifest


def _require_review_manifest_bindings(
    review_manifest: Mapping[str, Any],
    role_map: Mapping[str, Any],
    validator_recipe: Mapping[str, Any],
) -> tuple[str, str, str]:
    manifest = _require_object(dict(review_manifest), "review manifest")
    roles = _require_object(dict(role_map), "role map")
    recipe = _require_object(dict(validator_recipe), "validator recipe")
    _require_embedded_digest(manifest, "manifest_sha256", "review manifest")
    _require_embedded_digest(roles, "manifest_sha256", "role map")
    _require_embedded_digest(recipe, "recipe_sha256", "validator recipe")
    identity = (manifest.get("item_id"), manifest.get("theorem_id"), manifest.get("phase"))
    if identity != (roles.get("item_id"), roles.get("theorem_id"), roles.get("phase")):
        _fail("review manifest and role map identify different items")
    if identity != (recipe.get("item_id"), recipe.get("theorem_id"), recipe.get("phase")):
        _fail("review manifest and validator recipe identify different items")
    if manifest.get("schema_version") != REVIEW_MANIFEST_SCHEMA:
        _fail("review manifest schema is unsupported")
    if manifest.get("role_map_sha256") != roles.get("manifest_sha256"):
        _fail("review manifest does not bind the role map")
    if manifest.get("validator_recipe_sha256") != recipe.get("recipe_sha256"):
        _fail("review manifest does not bind the validator recipe")
    if manifest.get("artifact_bindings") != roles.get("artifacts"):
        _fail("review manifest does not bind the selected artifacts")
    if (
        manifest.get("authority_revision") != roles.get("authority_revision")
        or manifest.get("authority_revision") != recipe.get("authority_revision")
        or manifest.get("base_revision") != roles.get("base_revision")
        or manifest.get("base_revision") != recipe.get("base_revision")
    ):
        _fail("review evidence does not share one authority and worker base")
    if not all(isinstance(value, str) for value in identity):
        _fail("review manifest identity is malformed")
    return str(identity[0]), str(identity[1]), str(identity[2])


@dataclass(frozen=True)
class ReplayResult:
    schema_version: str
    item_id: str
    theorem_id: str
    phase: str
    authority_revision: str
    authority_tree: str
    validator_path: str
    validator_sha256: str
    validator_git_blob: str
    recipe_sha256: str
    review_manifest_sha256: str
    role_map_sha256: str
    artifact_bindings_sha256: str
    argv: list[str]
    bwrap_argv: list[str]
    cwd: str
    network_policy: str
    repo_access: str
    scratch_access: str
    scratch_was_isolated: bool
    shell: bool
    started_at_unix_ns: int
    duration_ms: int
    exit_code: int | None
    timed_out: bool
    stdout: str
    stderr: str
    stdout_base64: str
    stderr_base64: str
    stdout_sha256: str
    stderr_sha256: str
    stdout_complete: bool
    stderr_complete: bool
    semantic_result: dict[str, Any] | None
    semantic_result_sha256: str | None

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["result_sha256"] = sha256_bytes(canonical_json(value))
        return value


def _parse_validator_semantic_stdout(stdout: bytes) -> dict[str, Any]:
    if len(stdout) > MAX_REPLAY_OUTPUT_BYTES:
        _fail("validator stdout exceeds the complete-output limit")
    try:
        text = stdout.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise EvidenceError("validator stdout is not UTF-8 JSON") from exc

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            if key in value:
                _fail(f"validator stdout contains duplicate key {key!r}")
            value[key] = child
        return value

    try:
        semantic_raw, end = json.JSONDecoder(
            object_pairs_hook=reject_duplicates
        ).raw_decode(text)
    except json.JSONDecodeError as exc:
        raise EvidenceError("validator stdout is not one JSON object") from exc
    # A single final LF from print() is tolerated.  Leading whitespace,
    # blank lines, a second value, and all other trailing bytes are rejected.
    if text[end:] not in {"", "\n"}:
        _fail("validator stdout has trailing content")
    semantic = _require_object(semantic_raw, "validator stdout semantic result")
    allowed = {
        "schema_version",
        "item_id",
        "theorem_id",
        "phase",
        "status",
        "verdict",
        "phase_accepted",
        "audit_complete",
        "theorem_complete",
        "phase_predicate_proven",
        "first_failed_gate",
        "open_obligations",
        "stale_inputs",
        "blocked",
        "message",
    }
    required = {
        "schema_version",
        "item_id",
        "theorem_id",
        "phase",
        "status",
        "verdict",
        "phase_accepted",
        "audit_complete",
        "theorem_complete",
        "phase_predicate_proven",
        "first_failed_gate",
        "open_obligations",
        "stale_inputs",
        "blocked",
    }
    if set(semantic) != required and not (
        set(semantic) == required | {"message"}
    ):
        missing = sorted(required - set(semantic))
        unknown = sorted(set(semantic) - allowed)
        _fail(
            "validator stdout semantic schema is not exact"
            f" (missing={missing}, unknown={unknown})"
        )
    if semantic.get("schema_version") != VALIDATOR_SEMANTIC_SCHEMA:
        _fail("validator stdout semantic schema version is unsupported")
    if (
        not ITEM_RE.fullmatch(str(semantic.get("item_id", "")))
        or not THEOREM_RE.fullmatch(str(semantic.get("theorem_id", "")))
        or semantic.get("phase") not in PHASES
        or semantic.get("status") not in VALIDATOR_SEMANTIC_STATUSES
        or semantic.get("verdict") not in VALIDATOR_SEMANTIC_VERDICTS
    ):
        _fail("validator stdout semantic identity or enum is malformed")
    for field in (
        "phase_accepted",
        "audit_complete",
        "theorem_complete",
        "phase_predicate_proven",
        "blocked",
    ):
        if not isinstance(semantic.get(field), bool):
            _fail(f"validator stdout {field} must be boolean")
    failed_gate = semantic.get("first_failed_gate")
    if failed_gate is not None and (not isinstance(failed_gate, str) or not failed_gate):
        _fail("validator stdout first_failed_gate is malformed")
    open_obligations = semantic.get("open_obligations")
    if (
        not isinstance(open_obligations, int)
        or isinstance(open_obligations, bool)
        or open_obligations < 0
    ):
        _fail("validator stdout open_obligations must be a nonnegative integer")
    stale_inputs = semantic.get("stale_inputs")
    if (
        not isinstance(stale_inputs, list)
        or any(not isinstance(row, str) or not row for row in stale_inputs)
        or len(stale_inputs) != len(set(stale_inputs))
    ):
        _fail("validator stdout stale_inputs must be unique nonempty strings")
    if "message" in semantic and not isinstance(semantic["message"], str):
        _fail("validator stdout message must be a string")
    return semantic


def replay_validator(
    repo: Path | str,
    validator_recipe: Mapping[str, Any],
    *,
    review_manifest: Mapping[str, Any],
    role_map: Mapping[str, Any],
    timeout_seconds: float,
    bwrap_path: str = "/usr/bin/bwrap",
) -> dict[str, Any]:
    """Replay argv in a detached checkout, read-only repo and private scratch.

    Bubblewrap is mandatory.  If namespaces are unavailable the call fails
    closed; there is deliberately no bare-subprocess fallback.
    """

    root = _repository_root(repo)
    if not isinstance(timeout_seconds, (int, float)) or not (0 < timeout_seconds <= 86400):
        _fail("replay timeout must be within (0, 86400] seconds")
    bwrap = Path(bwrap_path)
    canonical_bwrap = Path("/usr/bin/bwrap").resolve()
    if not bwrap.is_absolute() or bwrap.resolve() != canonical_bwrap or not bwrap.is_file():
        _fail("bubblewrap executable is unavailable")
    bwrap_stat = canonical_bwrap.stat()
    if bwrap_stat.st_uid != 0 or bwrap_stat.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        _fail("bubblewrap executable ownership or permissions are unsafe")
    if validator_recipe.get("shell_interpolation") is not False:
        _fail("shell-based validator replay is forbidden")
    argv = validator_recipe.get("argv")
    if (
        not isinstance(argv, list)
        or not argv
        or any(not isinstance(part, str) or "\x00" in part for part in argv)
    ):
        _fail("validator argv is malformed")
    if argv[0] not in set(RUNTIME_EXECUTABLES):
        _fail("validator executable is not scheduler-authorized")
    _require_embedded_digest(validator_recipe, "recipe_sha256", "validator recipe")
    authority = validator_recipe.get("authority_revision")
    if not isinstance(authority, str) or not GIT_OID_RE.fullmatch(authority):
        _fail("validator recipe lacks an immutable authority revision")
    if _git_text(root, "rev-parse", "--verify", f"{authority}^{{commit}}") != authority:
        _fail("validator authority revision does not exist")
    if validator_recipe.get("network_policy") != "denied":
        _fail("validator recipe does not deny network access")
    if validator_recipe.get("repo_write_access") is not False:
        _fail("validator recipe permits repository writes")
    if validator_recipe.get("cwd") != ".":
        _fail("validator recipe cwd is not repository root")
    item_id, theorem_id, phase = _require_review_manifest_bindings(
        review_manifest, role_map, validator_recipe
    )
    relative = _safe_relative(validator_recipe.get("validator_path"), "validator path")
    expected_argv = (
        ["/usr/bin/python3", "-I", "-B", relative]
        if argv[0] == "/usr/bin/python3"
        else ["/usr/bin/bash", relative]
    )
    if argv != expected_argv:
        _fail("validator argv was not derived from the closed scheduler template")
    data = _head_bytes(root, authority, relative, "validator")
    blob = _blob_oid(root, authority, relative, "validator")
    if (
        sha256_bytes(data) != validator_recipe.get("validator_sha256")
        or blob != validator_recipe.get("validator_git_blob")
    ):
        _fail("validator recipe content binding is stale")

    with tempfile.TemporaryDirectory(prefix="stage1-acceptance-checkout-") as checkout_raw, tempfile.TemporaryDirectory(
        prefix="stage1-acceptance-scratch-"
    ) as scratch_raw:
        checkout = Path(checkout_raw)
        scratch = Path(scratch_raw)
        _run_git(root, ["worktree", "add", "--detach", "--no-checkout", str(checkout), authority])
        try:
            _run_git(checkout, ["checkout", "--detach", "--force", authority])
            if _git_text(checkout, "rev-parse", "HEAD") != authority:
                _fail("immutable checkout revision disagrees with replay authority")
            if _git_text(checkout, "status", "--porcelain", "--untracked-files=all"):
                _fail("immutable checkout is dirty before replay")
            if _read_regular_at(checkout, relative, "immutable checkout validator") != data:
                _fail("immutable checkout validator differs from the selected blob")

            # Start from an empty tmpfs root. Runtime directories are mounted
            # read-only and every executable is from the closed scheduler
            # allowlist.  No canonical worker .lake symlink, host /home, /root,
            # credentials, sockets, or environment config is visible.
            sandbox_repo = "/repo"
            sandbox_scratch = "/scratch"
            bwrap_argv = [
                bwrap_path,
                "--die-with-parent",
                "--new-session",
                "--unshare-all",
                "--tmpfs",
                "/",
                "--dir",
                "/usr",
            ]
            for runtime_mount in RUNTIME_MOUNTS:
                mount_path = Path(runtime_mount)
                if (
                    not mount_path.is_dir()
                    or mount_path.is_symlink()
                    or not mount_path.resolve().is_dir()
                ):
                    _fail(f"required replay runtime mount {runtime_mount} is unavailable")
                bwrap_argv.extend(
                    ["--dir", runtime_mount, "--ro-bind", runtime_mount, runtime_mount]
                )
            bwrap_argv.extend([
                "--symlink",
                "usr/bin",
                "/bin",
                "--symlink",
                "usr/lib",
                "/lib",
                "--symlink",
                "usr/lib64",
                "/lib64",
                "--proc",
                "/proc",
                "--dev",
                "/dev",
                "--dir",
                sandbox_repo,
                "--ro-bind",
                str(checkout),
                sandbox_repo,
                "--dir",
                sandbox_scratch,
                "--bind",
                str(scratch),
                sandbox_scratch,
                "--tmpfs",
                "/tmp",
                "--chdir",
                sandbox_repo,
                "--clearenv",
                "--setenv",
                "PATH",
                "/usr/bin:/bin",
                "--setenv",
                "HOME",
                sandbox_scratch,
                "--setenv",
                "TMPDIR",
                "/tmp",
                "--setenv",
                "TMP",
                "/tmp",
                "--setenv",
                "TEMP",
                "/tmp",
                "--setenv",
                "XDG_CACHE_HOME",
                f"{sandbox_scratch}/cache",
                "--setenv",
                "XDG_CONFIG_HOME",
                f"{sandbox_scratch}/config",
                "--setenv",
                "XDG_DATA_HOME",
                f"{sandbox_scratch}/data",
                "--setenv",
                "PYTHONDONTWRITEBYTECODE",
                "1",
                "--",
                *argv,
            ])
            if argv[0] not in RUNTIME_EXECUTABLES:
                _fail("validator executable is outside the replay toolchain allowlist")
            started_ns = time.time_ns()
            monotonic = time.monotonic_ns()
            timed_out = False
            exit_code: int | None
            try:
                result = subprocess.run(
                    bwrap_argv,
                    cwd=checkout,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=float(timeout_seconds),
                    check=False,
                    shell=False,
                    start_new_session=True,
                )
                stdout = result.stdout
                stderr = result.stderr
                exit_code = result.returncode
            except subprocess.TimeoutExpired as exc:
                timed_out = True
                exit_code = None
                stdout = exc.stdout or b""
                stderr = exc.stderr or b""
            duration_ms = (time.monotonic_ns() - monotonic) // 1_000_000
            if len(stderr) > MAX_REPLAY_OUTPUT_BYTES:
                _fail("validator stderr exceeds the complete-output limit")
            post_status = _git_text(checkout, "status", "--porcelain", "--untracked-files=all")
            if post_status:
                _fail("validator changed the supposedly read-only immutable checkout")
            if not timed_out and exit_code != 0 and stderr.lstrip().startswith(b"bwrap:"):
                _fail("bubblewrap sandbox could not be established")
            semantic_result = (
                _parse_validator_semantic_stdout(stdout)
                if not timed_out and exit_code == 0
                else None
            )
            semantic_sha256 = (
                sha256_bytes(canonical_json(semantic_result))
                if semantic_result is not None
                else None
            )
            replay = ReplayResult(
                schema_version=REPLAY_RESULT_SCHEMA,
                item_id=item_id,
                theorem_id=theorem_id,
                phase=phase,
                authority_revision=authority,
                authority_tree=_git_text(root, "rev-parse", f"{authority}^{{tree}}"),
                validator_path=relative,
                validator_sha256=sha256_bytes(data),
                validator_git_blob=blob,
                recipe_sha256=str(validator_recipe.get("recipe_sha256")),
                review_manifest_sha256=str(review_manifest.get("manifest_sha256")),
                role_map_sha256=str(role_map.get("manifest_sha256")),
                artifact_bindings_sha256=sha256_bytes(
                    canonical_json(role_map.get("artifacts"))
                ),
                argv=list(argv),
                bwrap_argv=bwrap_argv,
                cwd=sandbox_repo,
                network_policy="denied",
                repo_access="read_only",
                scratch_access="isolated_writable",
                scratch_was_isolated=True,
                shell=False,
                started_at_unix_ns=started_ns,
                duration_ms=duration_ms,
                exit_code=exit_code,
                timed_out=timed_out,
                stdout=stdout.decode("utf-8", "replace"),
                stderr=stderr.decode("utf-8", "replace"),
                stdout_base64=base64.b64encode(stdout).decode("ascii"),
                stderr_base64=base64.b64encode(stderr).decode("ascii"),
                stdout_sha256=sha256_bytes(stdout),
                stderr_sha256=sha256_bytes(stderr),
                stdout_complete=True,
                stderr_complete=True,
                semantic_result=semantic_result,
                semantic_result_sha256=semantic_sha256,
            )
            return replay.to_dict()
        finally:
            _run_git(root, ["worktree", "remove", "--force", str(checkout)], check=False)


def _semantic_tokens(value: Any) -> set[str]:
    tokens: set[str] = set()
    if isinstance(value, str):
        lowered = value.lower()
        tokens.update(re.findall(r"[a-z][a-z0-9_\-]*", lowered))
        for line in lowered.splitlines():
            prefix = re.match(r"\s*([a-z][a-z0-9_\-]*)\s*:", line)
            if prefix:
                tokens.add(prefix.group(1))
    elif isinstance(value, dict):
        for _key, child in value.items():
            tokens.update(_semantic_tokens(child))
    elif isinstance(value, list):
        for child in value:
            tokens.update(_semantic_tokens(child))
    return tokens


def evaluate_replay_semantics(
    replay_result: Mapping[str, Any],
    *,
    contract_record: Mapping[str, Any],
    review_manifest: Mapping[str, Any],
    role_map: Mapping[str, Any],
    validator_recipe: Mapping[str, Any],
    worker_verdict: str,
    review_verdict: str,
    audit_complete: bool,
    theorem_complete: bool,
) -> dict[str, Any]:
    """Evaluate only replay-owned semantics against the pinned HEAD contract."""

    if worker_verdict not in WORKER_VERDICTS:
        _fail("worker verdict is outside the closed vocabulary")
    if review_verdict not in REVIEW_VERDICTS:
        _fail("review verdict is outside the closed vocabulary")
    if not isinstance(audit_complete, bool) or not isinstance(theorem_complete, bool):
        _fail("terminal flags must be booleans")
    item_id, theorem_id, phase = _require_review_manifest_bindings(
        review_manifest, role_map, validator_recipe
    )
    replay_value = dict(replay_result)
    replay_digest = replay_value.pop("result_sha256", None)
    if (
        not isinstance(replay_digest, str)
        or not SHA256_RE.fullmatch(replay_digest)
        or sha256_bytes(canonical_json(replay_value)) != replay_digest
    ):
        _fail("replay result digest does not bind its content")
    phase_row = _phase_contract(contract_record, phase)
    _require_item_identity(item_id, theorem_id, phase_row)
    contract = _require_object(contract_record.get("contract"), "contract record")
    if (
        contract_record.get("revision") != review_manifest.get("authority_revision")
        or contract_record.get("sha256")
        != _require_object(review_manifest.get("contract"), "manifest contract").get("sha256")
        or contract_record.get("git_blob") != review_manifest.get("contract", {}).get("git_blob")
        or contract_record.get("git_tree") != review_manifest.get("authority_tree")
    ):
        _fail("review manifest is not bound to the supplied HEAD contract")
    if (
        replay_result.get("item_id") != item_id
        or replay_result.get("theorem_id") != theorem_id
        or replay_result.get("phase") != phase
        or replay_result.get("authority_revision") != contract_record.get("revision")
        or replay_result.get("authority_tree") != contract_record.get("git_tree")
        or replay_result.get("recipe_sha256") != validator_recipe.get("recipe_sha256")
        or replay_result.get("review_manifest_sha256")
        != review_manifest.get("manifest_sha256")
        or replay_result.get("role_map_sha256") != role_map.get("manifest_sha256")
        or replay_result.get("artifact_bindings_sha256")
        != sha256_bytes(canonical_json(role_map.get("artifacts")))
    ):
        _fail("replay result is not bound to the review manifest, role map, or artifacts")
    semantic_raw = replay_result.get("semantic_result")
    if semantic_raw is None:
        semantic: dict[str, Any] = {}
    else:
        semantic = _require_object(dict(semantic_raw), "replay-owned semantic result")
        # Re-run the exact stdout schema over the embedded object.  Otherwise
        # a caller could preserve the digest while smuggling extra semantic
        # members that the replay parser itself would have rejected.
        semantic = _parse_validator_semantic_stdout(canonical_json(semantic))
        if replay_result.get("semantic_result_sha256") != sha256_bytes(
            canonical_json(semantic)
        ):
            _fail("replay semantic digest does not bind stdout semantics")
        try:
            stdout_bytes = base64.b64decode(
                str(replay_result.get("stdout_base64")), validate=True
            )
        except (ValueError, TypeError) as exc:
            raise EvidenceError("replay stdout binding is malformed") from exc
        if (
            sha256_bytes(stdout_bytes) != replay_result.get("stdout_sha256")
            or semantic != _parse_validator_semantic_stdout(stdout_bytes)
        ):
            _fail("embedded semantics differ from complete replay stdout")
    status = semantic.get("status")
    verdict = semantic.get("verdict")
    phase_accepted = semantic.get("phase_accepted")
    tokens = _semantic_tokens(semantic)
    negative_tokens = sorted(tokens & NEGATIVE_SEMANTIC_TOKENS)
    reasons: list[str] = []
    if replay_result.get("schema_version") != REPLAY_RESULT_SCHEMA:
        reasons.append("unbound_replay_schema")
    if replay_result.get("timed_out") is not False:
        reasons.append("replay_timeout")
    if replay_result.get("exit_code") != 0:
        reasons.append("replay_nonzero")
    if replay_result.get("shell") is not False:
        reasons.append("shell_replay_forbidden")
    if replay_result.get("network_policy") != "denied":
        reasons.append("network_not_denied")
    if replay_result.get("repo_access") != "read_only":
        reasons.append("repo_not_read_only")
    if replay_result.get("scratch_access") != "isolated_writable":
        reasons.append("scratch_not_isolated")
    if replay_result.get("stdout_complete") is not True or replay_result.get(
        "stderr_complete"
    ) is not True:
        reasons.append("replay_output_incomplete")
    eligible = phase_row.get("worker_verdicts_eligible_for_review")
    if not isinstance(eligible, list) or worker_verdict not in eligible:
        reasons.append(f"worker_verdict_ineligible:{worker_verdict}")
    if worker_verdict == "blocked" or (
        phase_row.get("raw_blocked_can_close_phase") is not False
    ):
        reasons.append("raw_blocked_cannot_close")
    if review_verdict != "phase_accepted":
        reasons.append(f"review_{review_verdict}")
    if status not in POSITIVE_SEMANTIC_STATUSES:
        reasons.append(f"semantic_status_{status}")
    if verdict not in POSITIVE_SEMANTIC_VERDICTS:
        reasons.append(f"semantic_verdict_{verdict}")
    if phase_accepted is not True:
        reasons.append("semantic_phase_not_accepted")
    if semantic.get("blocked") not in {None, False}:
        reasons.append("semantic_blocked")
    if semantic.get("first_failed_gate") not in {None, ""}:
        reasons.append("semantic_failed_gate")
    if semantic.get("open_obligations") not in (None, 0, False, []):
        reasons.append("semantic_open_obligations")
    if semantic.get("stale_inputs") not in (None, 0, False, []):
        reasons.append("semantic_stale_inputs")
    if negative_tokens:
        reasons.append("negative_semantics:" + ",".join(negative_tokens))
    audit_boundary = _require_object(phase_row.get("audit_boundary"), "audit boundary")
    theorem_boundary = _require_object(
        phase_row.get("theorem_boundary"), "theorem boundary"
    )
    if audit_complete not in audit_boundary.get("allowed_audit_complete_values", []):
        reasons.append("audit_complete_outside_phase_contract")
    if theorem_complete not in theorem_boundary.get(
        "allowed_theorem_complete_values", []
    ):
        reasons.append("theorem_complete_outside_phase_contract")
    if semantic.get("audit_complete") is not audit_complete:
        reasons.append("semantic_audit_complete_mismatch")
    if semantic.get("theorem_complete") is not theorem_complete:
        reasons.append("semantic_theorem_complete_mismatch")
    if theorem_complete and (phase != "release" or not audit_complete):
        reasons.append("invalid_theorem_complete_boundary")
    if worker_verdict == "accepted_audit_only" and not (
        phase == "release" and audit_complete and not theorem_complete
    ):
        reasons.append("invalid_accepted_audit_only_boundary")
    verdict_protocol = _require_object(contract.get("verdict_protocol"), "verdict protocol")
    no_change_policy = _require_object(
        verdict_protocol.get("no_state_change_policy"), "no_state_change policy"
    )
    if worker_verdict == "no_state_change" and (
        no_change_policy.get("phase_closure_condition")
        != "master_independently_proves_the_phase_completion_predicate"
        or semantic.get("phase_predicate_proven") is not True
    ):
        reasons.append("no_state_change_predicate_not_independently_proven")
    if semantic.get("phase_predicate_proven") is not True:
        reasons.append("phase_predicate_not_proven")
    accepted = not reasons
    decision = {
        "schema_version": SEMANTIC_RESULT_SCHEMA,
        "phase": phase,
        "item_id": item_id,
        "theorem_id": theorem_id,
        "worker_verdict": worker_verdict,
        "review_verdict": review_verdict,
        "audit_complete": audit_complete,
        "theorem_complete": theorem_complete,
        "replay_result_sha256": replay_digest,
        "review_manifest_sha256": review_manifest.get("manifest_sha256"),
        "role_map_sha256": role_map.get("manifest_sha256"),
        "contract_sha256": contract_record.get("sha256"),
        "semantic_result_sha256": sha256_bytes(canonical_json(semantic)),
        "phase_evidence_accepted": accepted,
        "decision": "phase_accepted" if accepted else "remain_[_]",
        "negative_reasons": reasons,
    }
    decision["decision_sha256"] = sha256_bytes(canonical_json(decision))
    return decision
