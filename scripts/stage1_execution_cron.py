#!/usr/bin/env python3
"""Run the Stage1 rev-5.6 Lean 4 execution queue safely.

The requirements source is ``Docs/Stage1_Blueprint_rev-5.6.md``.  Its generated
execution appendix is a rendering of the typed execution-state DAG in
``Docs/Stage1_Execution_DAG_rev-5.6.json``.  The JSON is deliberately kept in
the repository, rather than in `.cron`, so worker state, dependencies, and
acceptance history are reviewable and reproducible.

This program owns scheduler-only state below `.cron/stage1-rev56/`, which is
gitignored.  A worker never writes an accepted state: it produces a self-test
manifest and its isolated clone is queued for the integration owner.
"""

from __future__ import annotations

import argparse
import datetime as dt
import errno
import fcntl
import functools
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter, deque
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "Docs"
BLUEPRINT = DOCS / "Stage1_Blueprint_rev-5.6.md"
TARGETS = DOCS / "Stage1_Targets_rev-5.6.json"
DAG = DOCS / "Stage1_Execution_DAG_rev-5.6.json"
THEOREM_DAG_V2 = DOCS / "Stage1_Theorem_DAG_v2.json"
RUNTIME = ROOT / ".cron" / "stage1-rev56"
CHECKLIST_BEGIN = "<!-- STAGE1-EXECUTION-CHECKLIST:BEGIN -->"
CHECKLIST_END = "<!-- STAGE1-EXECUTION-CHECKLIST:END -->"
PHASES = (
    ("intake", "Create the theorem dossier, scope map, and source-statement crosswalk."),
    ("statement", "Elaborate the exact Lean 4 target with the minimal pinned imports."),
    ("anchor_audit", "Audit mathlib and external Lean 4 candidates at immutable revisions."),
    ("obligation_tree", "Freeze the obligation registry and typed proof/provenance/workflow graphs."),
    ("proof", "Implement or pin/import the required proof bodies without placeholders."),
    ("validation", "Run hermetic kernel, trust, provenance, and independent validation gates."),
    ("release", "Reconcile evidence and decide the exact theorem-completion verdict."),
)
PHASE_NAMES = {phase for phase, _ in PHASES}
VALID_STATES = {"[ ]", "[_]", "[x]"}
DEPENDENCY_LEDGER_SCHEMA = "stage1-dependency-reuse-ledger/1.1"
REUSE_DECISIONS = {
    "reused_exact",
    "reused_with_transport",
    "candidate_only",
    "rejected_mismatch",
    "blocked_missing_acceptance",
    "not_applicable",
}
COMPATIBILITY_STATES = {"exact", "checked_transport", "candidate_only", "mismatch", "not_checked", "blocked"}
REUSE_RELATIONSHIPS = {"exact", "checked_transport", "implication", "candidate_only", "mismatch"}
ACCEPTED_REUSE_DECISIONS = {"reused_exact", "reused_with_transport"}
RECEIPT_REFERENCE_FIELDS = {"path", "receipt_id", "sha256"}
ARTIFACT_REFERENCE_FIELDS = {"path", "sha256"}
# This is both the lane-concurrency ceiling and the per-tick integration/refill ceiling.
# The operator requested three-minute saturation at 80 lanes. The target set
# remains frozen, but unfinished phases of the existing 1546 targets refill.
MAX_WORKERS = 80
DEFAULT_WORKERS = 80
DEFAULT_INTEGRATION_LIMIT = 80
STARTED_TARGETS_ONLY = False
CODEX_MODEL = "gpt-5.6-sol"
CODEX_REASONING_EFFORT = "ultra"
CODEX_SERVICE_TIER = "default"
ALLOWED_REASONING_EFFORTS = {"low", "medium", "high", "xhigh", "ultra"}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"stage1_execution_cron: {message}")


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
    timeout: int | None = None,
) -> subprocess.CompletedProcess[str]:
    if cwd is None:
        cwd = ROOT
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout)
    if check and result.returncode:
        detail = (result.stderr or result.stdout).strip()
        fail(f"command failed ({' '.join(command)}): {detail}")
    return result


def git_object_bytes(object_name: str, *, cwd: Path | None = None) -> bytes:
    """Read one Git blob without text decoding or worktree filters."""
    if cwd is None:
        cwd = ROOT
    result = subprocess.run(
        ["git", "show", object_name],
        cwd=cwd,
        capture_output=True,
    )
    if result.returncode:
        detail = (result.stderr or result.stdout).decode("utf-8", errors="replace").strip()
        fail(f"command failed (git show {object_name}): {detail}")
    return result.stdout


def durable_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        temporary.unlink(missing_ok=True)


def atomic_write(path: Path, text: str) -> None:
    durable_write_bytes(path, text.encode("utf-8"))


def durable_unlink(path: Path) -> None:
    """Remove a journal and persist the directory entry transition."""
    path.unlink(missing_ok=True)
    if path.parent.exists():
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)


def validate_runtime_root() -> None:
    """Reject scheduler storage reached through symlinks or outside the repo."""
    root_resolved = ROOT.resolve()
    current = RUNTIME
    lineage: list[Path] = []
    while current != ROOT and current.is_relative_to(ROOT):
        lineage.append(current)
        current = current.parent
    if current != ROOT or any(path.is_symlink() for path in lineage):
        fail("scheduler runtime path contains a symlink or escapes the repository")
    if RUNTIME.exists() and not RUNTIME.resolve().is_relative_to(root_resolved):
        fail("scheduler runtime path escapes the repository")
    for name in ("workers", "prompts", "logs", "blocked-reports"):
        path = RUNTIME / name
        if path.is_symlink() or (path.exists() and (not path.is_dir() or not path.resolve().is_relative_to(root_resolved))):
            fail(f"scheduler runtime subdirectory is unsafe: {name}")


class FileTransaction:
    """Restore authoritative and scheduler files if an integration tick aborts."""

    def __init__(
        self,
        journal_path: Path | None = None,
        wal_parent: "FileTransaction | None" = None,
    ) -> None:
        self._files: dict[Path, tuple[str, bytes | str | None, int | None]] = {}
        self._order: list[Path] = []
        self._created_dirs: list[Path] = []
        self._journal_path = journal_path
        self._wal_parent = wal_parent

    def commit(self) -> None:
        """Discard the rollback journal after a pending checkpoint is durable."""
        if self._journal_path is not None:
            durable_unlink(self._journal_path)
            self._journal_path = None

    def _persist_journal(self) -> None:
        if self._journal_path is None:
            return
        rows: list[dict[str, Any]] = []
        for path in self._order:
            kind, payload, mode = self._files[path]
            if not path.is_relative_to(ROOT):
                raise ValueError("integration journal path escapes repository root")
            row: dict[str, Any] = {
                "path": path.relative_to(ROOT).as_posix(),
                "kind": kind,
                "mode": mode,
            }
            if kind == "file":
                row["payload_hex"] = (payload if isinstance(payload, bytes) else b"").hex()
            elif kind == "symlink":
                row["target"] = str(payload)
            rows.append(row)
        journal = {
            "schema_version": "stage1-integration-wal/1.0",
            "state": "prepared",
            "base_revision": run(["git", "rev-parse", "HEAD"]).stdout.strip(),
            "files": rows,
            "created_dirs": [
                path.relative_to(ROOT).as_posix()
                for path in self._created_dirs
                if path.is_relative_to(ROOT)
            ],
        }
        atomic_write(self._journal_path, json.dumps(journal, indent=2) + "\n")

    def snapshot(self, path: Path) -> None:
        path = path.absolute()
        if path in self._files:
            return
        if path.is_symlink():
            raise ValueError(f"integration destination is a symlink: {path}")
        if path.exists():
            if not path.is_file():
                raise ValueError(f"integration destination is not a regular file: {path}")
            state = ("file", path.read_bytes(), path.stat().st_mode & 0o7777)
        else:
            state = ("missing", None, None)
        self._files[path] = state
        self._order.append(path)
        if self._wal_parent is not None:
            self._wal_parent.snapshot(path)
        self._persist_journal()

    def ensure_parent(self, path: Path) -> None:
        missing: list[Path] = []
        parent = path.absolute().parent
        while not parent.exists():
            missing.append(parent)
            parent = parent.parent
        for directory in reversed(missing):
            if directory not in self._created_dirs:
                self._created_dirs.append(directory)
            if self._wal_parent is not None and directory not in self._wal_parent._created_dirs:
                self._wal_parent._created_dirs.append(directory)
        if missing:
            if self._wal_parent is not None:
                self._wal_parent._persist_journal()
            self._persist_journal()
        path.parent.mkdir(parents=True, exist_ok=True)

    def absorb(self, other: "FileTransaction") -> None:
        """Adopt another successful subtransaction for later global rollback."""
        for path in other._order:
            if path not in self._files:
                self._files[path] = other._files[path]
                self._order.append(path)
        for directory in other._created_dirs:
            if directory not in self._created_dirs:
                self._created_dirs.append(directory)
        self._persist_journal()

    def rollback(self) -> None:
        errors: list[str] = []
        for path in reversed(self._order):
            kind, payload, mode = self._files[path]
            try:
                if path.is_symlink() or path.is_file():
                    path.unlink()
                elif path.exists():
                    raise OSError(f"rollback destination became a directory: {path}")
                if kind == "file":
                    durable_write_bytes(path, payload if isinstance(payload, bytes) else b"")
                    if mode is not None:
                        path.chmod(mode)
            except OSError as exc:
                errors.append(str(exc))
        for directory in reversed(self._created_dirs):
            try:
                directory.rmdir()
            except OSError:
                pass
        if errors:
            raise RuntimeError("integration rollback failed: " + "; ".join(errors))
        if self._journal_path is not None:
            durable_unlink(self._journal_path)


def recover_integration_wal() -> None:
    """Roll back a process-killed integration before any new scheduler work."""
    wal_path = runtime_path("integration_wal.json")
    if not wal_path.exists():
        return
    wal = read_json(wal_path)
    if wal.get("schema_version") != "stage1-integration-wal/1.0" or wal.get("state") != "prepared":
        fail("integration recovery journal is malformed")
    base = wal.get("base_revision")
    head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    if not isinstance(base, str) or head != base:
        fail("integration recovery journal base no longer matches HEAD")
    rows = wal.get("files")
    if not isinstance(rows, list):
        fail("integration recovery journal has no file snapshots")
    allowed_runtime = {
        ".cron/stage1-rev56/claims.json",
        ".cron/stage1-rev56/integration_queue.json",
        ".cron/stage1-rev56/pending_checkpoint.json",
    }

    def recovery_target(relative: str) -> Path:
        path = Path(relative)
        if (
            path.is_absolute()
            or ".." in path.parts
            or (
                relative not in allowed_runtime
                and relative not in {
                    "Docs/Stage1_Blueprint_rev-5.6.md",
                    "Docs/Stage1_Execution_DAG_rev-5.6.json",
                    "Docs/Stage1_Theorem_DAG_v2.json",
                }
                and re.fullmatch(r"Docs/todos_[0-9]{8}\.md", relative) is None
                and not relative.startswith("Stage1_Instances/THM-M-")
            )
        ):
            fail("integration recovery journal contains an unsafe path")
        target = ROOT / path
        parent = target.parent
        while parent != ROOT:
            if parent.is_symlink():
                fail("integration recovery path contains a symlink parent")
            parent = parent.parent
        if target.exists() and not target.resolve().is_relative_to(ROOT.resolve()):
            fail("integration recovery path escapes repository root")
        return target

    for row in reversed(rows):
        if not isinstance(row, dict):
            fail("integration recovery journal contains a malformed snapshot")
        relative = row.get("path")
        kind = row.get("kind")
        mode = row.get("mode")
        if (
            not isinstance(relative, str)
            or kind not in {"file", "missing"}
        ):
            fail("integration recovery journal contains an unsafe path")
        target = recovery_target(relative)
        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.exists():
            fail(f"integration recovery destination became a directory: {relative}")
        if kind == "file":
            payload_hex = row.get("payload_hex")
            if not isinstance(payload_hex, str):
                fail("integration recovery journal file payload is missing")
            try:
                payload = bytes.fromhex(payload_hex)
            except ValueError:
                fail("integration recovery journal file payload is malformed")
            durable_write_bytes(target, payload)
            if isinstance(mode, int):
                target.chmod(mode)
    created_dirs = wal.get("created_dirs", [])
    if not isinstance(created_dirs, list):
        fail("integration recovery directory list is malformed")
    for relative in reversed(created_dirs):
        if isinstance(relative, str):
            directory = recovery_target(relative)
            try:
                directory.rmdir()
            except OSError:
                pass
    durable_unlink(wal_path)
    theorem_dag_v2.cache_clear()
    print("recovery: rolled back interrupted Stage1 integration")


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path.relative_to(ROOT)}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def target_rows() -> list[dict[str, Any]]:
    manifest = read_json(TARGETS)
    targets = manifest.get("targets")
    if not isinstance(targets, list) or len(targets) != 1546:
        fail("target manifest must contain exactly 1546 targets")
    if [target.get("execution_rank") for target in targets] != list(range(1, 1547)):
        fail("target manifest execution ranks are not contiguous")
    return targets


@functools.lru_cache(maxsize=1)
def theorem_dag_v2() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    """Load the v2 theorem-order overlay without replacing rev-5.6 task state."""
    data = read_json(THEOREM_DAG_V2)
    nodes = data.get("theorems")
    if not isinstance(nodes, list) or len(nodes) != 1546:
        fail("v2 theorem DAG must contain exactly 1546 nodes")
    by_id = {node.get("theorem_id"): node for node in nodes if isinstance(node, dict)}
    if len(by_id) != 1546 or None in by_id:
        fail("v2 theorem DAG has duplicate or missing theorem IDs")
    targets = target_rows()
    if set(by_id) != {target["theorem_id"] for target in targets}:
        fail("v2 theorem DAG target set disagrees with rev-5.6 manifest")
    ranks = [node.get("v2_execution_rank") for node in nodes]
    if sorted(ranks) != list(range(1, 1547)):
        fail("v2 theorem DAG execution ranks are not contiguous")
    rank_by_id = {theorem_id: node["v2_execution_rank"] for theorem_id, node in by_id.items()}
    hard_edges = data.get("hard_edges")
    if not isinstance(hard_edges, list):
        fail("v2 theorem DAG hard_edges must be a list")
    for edge in hard_edges:
        if not isinstance(edge, dict) or edge.get("blocking") is not True:
            fail("v2 theorem DAG has malformed hard edge")
        parent = edge.get("parent_theorem_id")
        child = edge.get("child_theorem_id")
        if parent not in by_id or child not in by_id or rank_by_id[parent] >= rank_by_id[child]:
            fail("v2 theorem DAG hard edge violates parent-first order")
        contract = edge.get("material_contract")
        if (
            not isinstance(contract, dict)
            or not isinstance(contract.get("provider_sources"), list)
            or not contract["provider_sources"]
            or not isinstance(contract.get("consumer_sources"), list)
            or not contract["consumer_sources"]
        ):
            fail("v2 theorem DAG hard edge lacks a material contract")
    return data, by_id


def order_by_v2(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Use v2 theorem priority while preserving each theorem's seven phases."""
    _, nodes = theorem_dag_v2()
    return sorted(
        items,
        key=lambda item: (
            nodes[item["theorem_id"]]["v2_execution_rank"],
            item["layer"],
            item["id"],
        ),
    )


def hard_parent_ids(theorem_id: str) -> list[str]:
    """Return audited theorem parents for context; reuse hints never gate."""
    _, nodes = theorem_dag_v2()
    parents = nodes[theorem_id].get("direct_hard_parents")
    if not isinstance(parents, list) or any(parent not in nodes for parent in parents):
        fail(f"{theorem_id} has invalid v2 hard-parent metadata")
    return parents


def graph_sha256() -> str:
    return hashlib.sha256(THEOREM_DAG_V2.read_bytes()).hexdigest()


def safe_evidence_path(root: Path, relative: Any, *, owner: str | None = None) -> Path:
    """Resolve one repo-relative evidence path inside the requested ownership scope."""
    if not isinstance(relative, str) or not relative:
        raise ValueError("dependency reuse evidence path must be a nonempty string")
    pure = Path(relative)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError("dependency reuse evidence path is unsafe")
    if owner is not None and (not pure.parts or pure.parts[:2] != ("Stage1_Instances", owner)):
        raise ValueError("dependency reuse receipt escapes the consumer target")
    root_resolved = root.resolve()
    path = root / pure
    if not path.is_file():
        raise ValueError("dependency reuse evidence file is missing")
    resolved = path.resolve()
    if not resolved.is_relative_to(root_resolved):
        raise ValueError("dependency reuse evidence path escapes through a symlink")
    if owner is not None:
        owner_root = (root / "Stage1_Instances" / owner).resolve()
        if not resolved.is_relative_to(owner_root):
            raise ValueError("dependency reuse receipt escapes the consumer target through a symlink")
    return resolved


def require_authoritative_match(
    relative: Any,
    candidate: Path,
    *,
    authoritative_root: Path,
    owner: str | None = None,
) -> None:
    """Reject worker-local rewrites of provider or ancestor evidence."""
    authoritative = safe_evidence_path(authoritative_root, relative, owner=owner)
    if hashlib.sha256(candidate.read_bytes()).digest() != hashlib.sha256(authoritative.read_bytes()).digest():
        raise ValueError("dependency reuse provider evidence differs from the authoritative checkout")


def validate_receipt_references(
    references: Any,
    *,
    evidence_root: Path,
    theorem_id: str,
    phases: set[str],
    require_accepted: bool,
    accepted_phase_states: dict[str, str] | None = None,
    authoritative_root: Path | None = None,
    require_successful_selftest: bool = False,
) -> None:
    """Bind receipt references to target-owned JSON bytes and their asserted authority."""
    if not isinstance(references, list) or not references:
        raise ValueError("dependency reuse decision lacks receipt references")
    seen: set[str] = set()
    for reference in references:
        if not isinstance(reference, dict) or set(reference) != RECEIPT_REFERENCE_FIELDS:
            raise ValueError("dependency reuse receipt reference has invalid fields")
        receipt_id = reference.get("receipt_id")
        digest = reference.get("sha256")
        if (
            not isinstance(receipt_id, str)
            or not receipt_id
            or receipt_id in seen
            or not isinstance(digest, str)
            or re.fullmatch(r"[0-9a-f]{64}", digest) is None
        ):
            raise ValueError("dependency reuse receipt reference has invalid identity or digest")
        path = safe_evidence_path(evidence_root, reference.get("path"), owner=theorem_id)
        if authoritative_root is not None:
            require_authoritative_match(reference.get("path"), path, authoritative_root=authoritative_root)
        try:
            receipt = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"dependency reuse receipt is invalid JSON: {exc}") from exc
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError("dependency reuse receipt digest is stale")
        if (
            not isinstance(receipt, dict)
            or receipt.get("schema_version") != "stage1-node-receipt/1.0"
            or receipt.get("receipt_id") != receipt_id
            or receipt.get("theorem_id") != theorem_id
            or receipt.get("phase") not in phases
            or receipt.get("item_id") != task_id(theorem_id, receipt.get("phase"))
            or not isinstance(receipt.get("base_revision"), str)
            or not receipt["base_revision"]
            or not isinstance(receipt.get("inputs"), dict)
            or not receipt["inputs"]
        ):
            raise ValueError("dependency reuse receipt identity, owner, or phase mismatch")
        if require_accepted:
            authoritative_receipt: dict[str, Any] | None = None
            if authoritative_root is not None:
                authoritative_path = safe_evidence_path(
                    authoritative_root,
                    reference.get("path"),
                    owner=theorem_id,
                )
                authoritative_receipt = json.loads(authoritative_path.read_text(encoding="utf-8"))
            if (
                authoritative_receipt is None
                or receipt != authoritative_receipt
                or authoritative_receipt.get("accepted") is not True
                or authoritative_receipt.get("support_state") not in {"master_accepted", "accepted"}
                or authoritative_receipt.get("verdict") in {"blocked", "rejected"}
                or accepted_phase_states is None
                or accepted_phase_states.get(authoritative_receipt.get("phase")) != "[x]"
            ):
                raise ValueError("dependency reuse consumer validation receipt is not authoritative master accepted evidence")
        if require_successful_selftest:
            accepted_evidence = (
                receipt.get("accepted") is True
                and receipt.get("support_state") in {"master_accepted", "accepted"}
                and receipt.get("verdict") in {"accepted", "passed", "no_state_change"}
                and accepted_phase_states is not None
                and accepted_phase_states.get(receipt.get("phase")) == "[x]"
                and receipt.get("selftest_status") == "passed"
                and isinstance(receipt.get("selftest_result"), dict)
                and receipt["selftest_result"].get("exit_code") == 0
                and isinstance(receipt["selftest_result"].get("commands"), list)
                and bool(receipt["selftest_result"]["commands"])
            )
            provisional_evidence = (
                receipt.get("accepted") is False
                and receipt.get("support_state") == "provisional_worker_selftest"
                and receipt.get("proposed_state") == "[_]"
                and receipt.get("selftest_status") == "passed"
                and isinstance(receipt.get("selftest_result"), dict)
                and receipt["selftest_result"].get("exit_code") == 0
                and isinstance(receipt["selftest_result"].get("commands"), list)
                and bool(receipt["selftest_result"]["commands"])
            )
            if not (accepted_evidence or provisional_evidence):
                raise ValueError("dependency reuse receipt is not successful accepted or worker-self-tested evidence")
        seen.add(receipt_id)


def validate_worker_selftest_receipt(
    references: Any,
    *,
    evidence_root: Path,
    theorem_id: str,
    expected_base_revision: str | None = None,
) -> None:
    """Bind the current worker's validation receipt without requiring it on master yet."""
    validate_receipt_references(
        references,
        evidence_root=evidence_root,
        theorem_id=theorem_id,
        phases={"validation"},
        require_accepted=False,
        require_successful_selftest=True,
    )
    for reference in references:
        receipt_path = safe_evidence_path(evidence_root, reference["path"], owner=theorem_id)
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        expected_item_id = task_id(theorem_id, "validation")
        if (
            receipt.get("schema_version") != "stage1-node-receipt/1.0"
            or receipt.get("item_id") != expected_item_id
            or receipt.get("intent") != "validate"
            or not isinstance(receipt.get("base_revision"), str)
            or not receipt["base_revision"]
            or (expected_base_revision is not None and receipt["base_revision"] != expected_base_revision)
            or not isinstance(receipt.get("inputs"), dict)
            or not receipt["inputs"]
        ):
            raise ValueError("dependency reuse consumer validation receipt lacks bound node evidence")


def validate_material_reference(
    reference: Any,
    *,
    evidence_root: Path,
    authoritative_root: Path,
    owner: str,
    declaration: Any,
    expected_fingerprint: Any,
) -> None:
    """Bind a claimed proof body/import declaration to one authoritative source file."""
    if not isinstance(reference, dict) or set(reference) != ARTIFACT_REFERENCE_FIELDS:
        raise ValueError("accepted dependency reuse material reference has invalid fields")
    if not isinstance(declaration, str) or not declaration or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_'.]*", declaration) is None:
        raise ValueError("accepted dependency reuse material declaration is invalid")
    path = safe_evidence_path(evidence_root, reference.get("path"), owner=owner)
    if path.suffix != ".lean":
        raise ValueError("accepted dependency reuse material must be a Lean source")
    require_authoritative_match(
        reference.get("path"),
        path,
        authoritative_root=authoritative_root,
        owner=owner,
    )
    digest = reference.get("sha256")
    if (
        not isinstance(digest, str)
        or re.fullmatch(r"[0-9a-f]{64}", digest) is None
        or hashlib.sha256(path.read_bytes()).hexdigest() != digest
    ):
        raise ValueError("accepted dependency reuse material digest is stale")
    declaration_tail = declaration.rsplit(".", 1)[-1]
    text = path.read_text(encoding="utf-8", errors="replace")
    stripped = re.sub(r"(?s)/-.*?-/|--[^\n]*|\"(?:\\.|[^\"\\])*\"", "", text)
    if re.search(rf"\b(?:theorem|lemma|def|abbrev)\s+{re.escape(declaration_tail)}\b", stripped) is None:
        raise ValueError("accepted dependency reuse declaration is not present in its bound source")
    namespace_parts = re.findall(r"(?m)^\s*namespace\s+([A-Za-z_][A-Za-z0-9_'.]*)\s*$", stripped)
    if "." in declaration:
        prefix = declaration.rsplit(".", 1)[0]
        if prefix not in namespace_parts:
            raise ValueError("accepted dependency reuse declaration namespace is not bound by its source")
    declaration_match = re.search(
        rf"(?ms)^\s*(?:theorem|lemma|def|abbrev)\s+{re.escape(declaration_tail)}\b(.*?)\s*:=",
        stripped,
    )
    if declaration_match is None or not isinstance(expected_fingerprint, str):
        raise ValueError("accepted dependency reuse declaration signature is not bound")
    signature = " ".join(declaration_match.group(1).split())
    signature = signature.split(":", 1)[-1].strip() if ":" in signature else signature
    signature_digest = hashlib.sha256(signature.encode("utf-8")).hexdigest()
    if signature_digest != expected_fingerprint:
        raise ValueError("accepted dependency reuse statement fingerprint does not match its source")


def validate_hard_edge_material_contract(
    edge: dict[str, Any],
    *,
    provider_reference: Any,
    provider_declaration: Any,
    consumer_reference: Any,
    consumer_declaration: Any,
) -> None:
    """Require accepted hard-edge reuse to use the exact admitted source bytes."""
    contract = edge.get("material_contract")
    if not isinstance(contract, dict):
        raise ValueError("accepted hard-edge reuse lacks an admitted material contract")
    expected_kind = (
        "cross_target_import_and_proof_receipt_input"
        if edge.get("edge_type") == "proof_dependency"
        else "source_manifest_and_consumer_adapter"
    )
    if contract.get("contract_kind") != expected_kind:
        raise ValueError("accepted hard-edge reuse has the wrong material contract kind")

    def require_admitted(reference: Any, declaration: Any, field: str) -> None:
        if not isinstance(reference, dict):
            raise ValueError(f"accepted hard-edge {field} is not a material reference")
        sources = contract.get(field)
        if not isinstance(sources, list):
            raise ValueError(f"accepted hard-edge lacks a {field} allowlist")
        admitted = next(
            (
                source
                for source in sources
                if isinstance(source, dict)
                and source.get("path") == reference.get("path")
                and source.get("sha256") == reference.get("sha256")
            ),
            None,
        )
        if admitted is None:
            raise ValueError(f"accepted hard-edge {field} is outside its content-bound allowlist")
        declarations = admitted.get("declarations")
        if not isinstance(declarations, list) or declaration not in declarations:
            raise ValueError(f"accepted hard-edge {field} declaration is not admitted for that source")

    require_admitted(provider_reference, provider_declaration, "provider_sources")
    require_admitted(consumer_reference, consumer_declaration, "consumer_sources")


def normalized_command_argv(command: Any, *, require_success: bool = False) -> tuple[str, ...] | None:
    """Normalize receipt/packet command records without invoking a shell."""
    if isinstance(command, str):
        if not command.strip():
            return None
        try:
            argv = shlex.split(command)
        except ValueError:
            return None
    elif isinstance(command, dict):
        if require_success and command.get("exit_code") != 0:
            return None
        argv = command.get("argv")
        if not isinstance(argv, list) or any(not isinstance(token, str) or not token for token in argv):
            return None
    else:
        return None
    if not argv or any(token in {"&&", "||", ";", "|", ">", ">>", "<"} for token in argv):
        return None
    return tuple(argv)


def require_head_tracked_file(root: Path, relative: str) -> Path:
    """Return an authority file only when its bytes are exactly the current HEAD blob."""
    path = safe_evidence_path(root, relative)
    blob = run(["git", "rev-parse", f"HEAD:{relative}"], cwd=root, check=False)
    if blob.returncode:
        raise ValueError(f"authoritative validation asset is not tracked at HEAD: {relative}")
    current = run(["git", "hash-object", str(path)], cwd=root, check=False)
    if current.returncode or current.stdout.strip() != blob.stdout.strip():
        raise ValueError(f"authoritative validation asset differs from HEAD: {relative}")
    return path


def authoritative_validation_recipe(
    *,
    theorem_id: str,
    evidence_root: Path,
    authoritative_root: Path,
    receipt_commands: list[Any],
) -> tuple[list[str], int]:
    """Select a committed integration-owned validator matching the receipt exactly."""
    receipt_argvs = {
        argv
        for command in receipt_commands
        if (argv := normalized_command_argv(command)) is not None
    }
    if not receipt_argvs:
        raise ValueError("dependency reuse consumer validation receipt lacks normalized replay commands")

    owner_prefix = f"Stage1_Instances/{theorem_id}/"
    errors: list[str] = []
    matches: list[tuple[list[str], int, str]] = []
    for name in ("validation-phase-spec.json", "validation-spec.json"):
        relative = f"{owner_prefix}{name}"
        try:
            authority_spec_path = require_head_tracked_file(authoritative_root, relative)
            worker_spec_path = safe_evidence_path(evidence_root, relative, owner=theorem_id)
            require_authoritative_match(
                relative,
                worker_spec_path,
                authoritative_root=authoritative_root,
                owner=theorem_id,
            )
            spec = json.loads(authority_spec_path.read_text(encoding="utf-8"))
            argv = spec.get("argv") if isinstance(spec, dict) else None
            if (
                not isinstance(spec, dict)
                or spec.get("schema_version")
                not in {"stage1-validation-recipe/1.0", "stage1-validation-spec/1.0"}
                or spec.get("item_id") != task_id(theorem_id, "validation")
                or spec.get("theorem_id") != theorem_id
                or spec.get("cwd") != "."
                or spec.get("expected_exit") != 0
                or spec.get("network_policy") != "denied"
                or not isinstance(argv, list)
                or not argv
                or any(not isinstance(token, str) or not token for token in argv)
            ):
                raise ValueError(f"authoritative validation recipe is malformed: {relative}")

            validator_tokens = [
                token
                for token in argv
                if token.startswith(owner_prefix)
                and Path(token).name in {"check_validation.py", "check_validation.sh"}
            ]
            if len(validator_tokens) != 1:
                raise ValueError(f"authoritative recipe does not bind exactly one target validator: {relative}")
            validator_relative = validator_tokens[0]
            require_head_tracked_file(authoritative_root, validator_relative)
            worker_validator = safe_evidence_path(evidence_root, validator_relative, owner=theorem_id)
            require_authoritative_match(
                validator_relative,
                worker_validator,
                authoritative_root=authoritative_root,
                owner=theorem_id,
            )
            timeout = spec.get("timeout_seconds")
            if not isinstance(timeout, int) or timeout <= 0:
                raise ValueError(f"authoritative validation recipe lacks a positive timeout: {relative}")
            matches.append((list(argv), timeout, relative))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
    unique = {tuple(argv) for argv, _, _ in matches}
    if len(unique) > 1:
        raise ValueError("dependency reuse has ambiguous authoritative validation recipes")
    if len(unique) == 1:
        argv, timeout, relative = matches[0]
        if tuple(argv) not in receipt_argvs:
            raise ValueError(f"consumer receipt does not name authoritative recipe: {relative}")
        return argv, timeout
    detail = "; ".join(errors) if errors else "no committed validation recipe"
    raise ValueError(f"dependency reuse has no matching authoritative validation recipe: {detail}")


def validate_consumer_validation_commands(
    references: Any,
    *,
    evidence_root: Path,
    authoritative_root: Path,
    theorem_id: str,
    expected_commands: list[Any] | None = None,
) -> None:
    """Replay an integration-owned recipe, never a worker-selected validator."""
    for reference in references:
        receipt_path = safe_evidence_path(evidence_root, reference["path"], owner=theorem_id)
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        commands = receipt.get("selftest_result", {}).get("commands")
        if not isinstance(commands, list) or not commands:
            raise ValueError("dependency reuse consumer validation receipt lacks replay commands")
        argv, timeout = authoritative_validation_recipe(
            theorem_id=theorem_id,
            evidence_root=evidence_root,
            authoritative_root=authoritative_root,
            receipt_commands=commands,
        )
        if expected_commands is not None:
            packet_argvs = {
                normalized
                for command in expected_commands
                if (normalized := normalized_command_argv(command, require_success=isinstance(command, dict)))
                is not None
            }
            if tuple(argv) not in packet_argvs:
                raise ValueError("dependency reuse consumer validation recipe is absent from successful worker packet commands")
        try:
            result = run(argv, cwd=evidence_root, check=False, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            raise ValueError(
                f"dependency reuse authoritative validation replay timed out after {timeout}s"
            ) from exc
        if result.returncode:
            detail = (result.stderr or result.stdout).strip()
            raise ValueError(f"dependency reuse authoritative validation replay failed: {detail}")


def expected_dependency_context(theorem_id: str) -> dict[str, list[str]]:
    """Return the exact v2 context a proof ledger must account for."""
    graph, nodes = theorem_dag_v2()
    node = nodes[theorem_id]
    direct = node.get("direct_hard_parents")
    ancestors = node.get("transitive_hard_ancestors")
    hints = node.get("direct_reuse_hint_ids")
    groups = node.get("shared_lemma_group_ids")
    if not all(isinstance(value, list) for value in (direct, ancestors, hints, groups)):
        fail(f"{theorem_id} has malformed v2 dependency context")
    context_nodes = set(ancestors) | {theorem_id}
    hard_edges = [
        edge["edge_id"]
        for edge in graph.get("hard_edges", [])
        if edge.get("child_theorem_id") in context_nodes
        and edge.get("parent_theorem_id") in context_nodes
    ]
    return {
        "direct_parent_ids": sorted(direct),
        "transitive_ancestor_ids": sorted(ancestors),
        "hard_edge_ids": sorted(hard_edges),
        "reuse_hint_ids": sorted(hints),
        "shared_group_ids": sorted(groups),
    }


def validate_dependency_reuse_ledger(
    path: Path,
    theorem_id: str,
    *,
    expected_observed_graph_sha256: str | None = None,
    expected_repository_revision: str | None = None,
    evidence_root: Path = ROOT,
    authoritative_root: Path = ROOT,
) -> dict[str, Any]:
    """Fail closed unless a proof ledger covers the complete current v2 context."""
    try:
        ledger = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid dependency reuse ledger: {exc}") from exc
    if not isinstance(ledger, dict):
        raise ValueError("dependency reuse ledger must be an object")
    expected = expected_dependency_context(theorem_id)
    if ledger.get("schema_version") != DEPENDENCY_LEDGER_SCHEMA:
        raise ValueError("dependency reuse ledger schema mismatch")
    if ledger.get("consumer_theorem_id") != theorem_id:
        raise ValueError("dependency reuse ledger theorem mismatch")
    _, nodes = theorem_dag_v2()
    context_sha256 = nodes[theorem_id].get("dependency_context_sha256")
    observed_digest = ledger.get("observed_theorem_dag_sha256")
    if not isinstance(observed_digest, str) or re.fullmatch(r"[0-9a-f]{64}", observed_digest) is None:
        raise ValueError("dependency reuse ledger lacks observed theorem DAG digest")
    if expected_observed_graph_sha256 is not None and observed_digest != expected_observed_graph_sha256:
        raise ValueError("dependency reuse ledger does not match the graph supplied to its worker")
    if ledger.get("dependency_context_sha256") != context_sha256:
        raise ValueError("dependency reuse ledger is stale for the target dependency context")
    if not isinstance(ledger.get("repository_revision"), str) or not ledger["repository_revision"]:
        raise ValueError("dependency reuse ledger lacks repository revision")
    if expected_repository_revision is not None and ledger["repository_revision"] != expected_repository_revision:
        raise ValueError("dependency reuse ledger repository revision disagrees with its worker claim")
    for field, values in expected.items():
        actual = ledger.get(field)
        if not isinstance(actual, list) or sorted(actual) != values or len(actual) != len(set(actual)):
            raise ValueError(f"dependency reuse ledger has incomplete {field}")
    inspections = ledger.get("inspections")
    required_inspections = set(expected["direct_parent_ids"] + expected["transitive_ancestor_ids"])
    if not isinstance(inspections, list):
        raise ValueError("dependency reuse ledger inspections must be a list")
    inspected_ids = {row.get("theorem_id") for row in inspections if isinstance(row, dict)}
    if inspected_ids != required_inspections or len(inspections) != len(required_inspections):
        raise ValueError("dependency reuse ledger does not inspect every hard parent/ancestor exactly once")
    inspected_phase_states: dict[str, dict[str, str]] = {}
    for row in inspections:
        phase_states = row.get("phase_states")
        if (
            not isinstance(phase_states, dict)
            or set(phase_states) != PHASE_NAMES
            or set(phase_states.values()) - VALID_STATES
        ):
            raise ValueError("dependency reuse inspection lacks valid phase states")
        current_states = {
            item["phase"]: item["state"]
            for item in read_json(DAG).get("items", [])
            if item.get("theorem_id") == row["theorem_id"]
        }
        if phase_states != current_states:
            raise ValueError("dependency reuse inspection phase states are stale")
        inspected_phase_states[row["theorem_id"]] = phase_states
        artifact_digests = row.get("artifact_digests")
        if not isinstance(artifact_digests, dict) or not artifact_digests:
            raise ValueError("dependency reuse inspection lacks artifact digests")
        for relative, digest in artifact_digests.items():
            try:
                artifact = safe_evidence_path(evidence_root, relative, owner=row["theorem_id"])
                require_authoritative_match(
                    relative,
                    artifact,
                    authoritative_root=authoritative_root,
                    owner=row["theorem_id"],
                )
            except ValueError as exc:
                raise ValueError("dependency reuse inspection has a stale or unsafe artifact digest") from exc
            if not isinstance(digest, str) or hashlib.sha256(artifact.read_bytes()).hexdigest() != digest:
                raise ValueError("dependency reuse inspection has a stale or unsafe artifact digest")
        if row.get("compatibility") not in COMPATIBILITY_STATES:
            raise ValueError("dependency reuse inspection has invalid compatibility")
    decisions = ledger.get("reuse_decisions")
    if not isinstance(decisions, list):
        raise ValueError("dependency reuse ledger decisions must be a list")
    graph, _ = theorem_dag_v2()
    hard_edges_by_id = {edge["edge_id"]: edge for edge in graph.get("hard_edges", [])}
    hints_by_id = {hint["hint_id"]: hint for hint in graph.get("reuse_hints", [])}
    groups_by_id = {group["group_id"]: group for group in graph.get("shared_lemma_groups", [])}
    accounted = set()
    for row in decisions:
        if not isinstance(row, dict) or row.get("decision") not in REUSE_DECISIONS:
            raise ValueError("dependency reuse ledger has invalid reuse decision")
        source_id = row.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            raise ValueError("dependency reuse decision lacks source_id")
        provider_theorem_id = row.get("provider_theorem_id")
        if source_id in hard_edges_by_id:
            expected_provider = hard_edges_by_id[source_id]["parent_theorem_id"]
        elif source_id in hints_by_id:
            expected_provider = hints_by_id[source_id]["provider_theorem_id"]
        elif source_id in groups_by_id:
            expected_provider = row.get("provider_theorem_id")
            if expected_provider not in groups_by_id[source_id]["member_theorem_ids"]:
                raise ValueError("dependency reuse decision provider is not a member of its shared group")
        else:
            raise ValueError("dependency reuse decision has an unknown source_id")
        if provider_theorem_id != expected_provider:
            raise ValueError("dependency reuse decision provider does not match its source")
        context_digest = row.get("context_digest")
        if context_digest != context_sha256:
            raise ValueError("dependency reuse decision context digest is stale")
        decision = row["decision"]
        if decision != "not_applicable":
            if row.get("relationship") not in REUSE_RELATIONSHIPS or row.get("provider_proof_state") not in VALID_STATES:
                raise ValueError("dependency reuse decision has invalid relationship or provider state")
            provider_states = inspected_phase_states.get(expected_provider)
            if provider_states is not None and row["provider_proof_state"] != provider_states["proof"]:
                raise ValueError("dependency reuse decision provider proof state is stale")
            for field in ("consumer_obligation_id", "provider_obligation_id"):
                if not isinstance(row.get(field), str) or not row[field]:
                    raise ValueError(f"dependency reuse decision lacks {field}")
            for field in (
                "terminal_proof_body_id",
                "provider_statement_fingerprint",
                "consumer_required_fingerprint",
            ):
                value = row.get(field)
                if not isinstance(value, str) or not value:
                    raise ValueError(f"dependency reuse decision lacks {field}")
        if decision in ACCEPTED_REUSE_DECISIONS:
            required_relationship = "exact" if decision == "reused_exact" else "checked_transport"
            if row["relationship"] != required_relationship:
                raise ValueError("accepted dependency reuse decision has inconsistent relationship")
            inspection_compatibility = None
            if expected_provider in inspected_phase_states:
                inspection_compatibility = next(
                    inspection.get("compatibility")
                    for inspection in inspections
                    if inspection.get("theorem_id") == expected_provider
                )
            if inspection_compatibility is not None and inspection_compatibility != required_relationship:
                raise ValueError("accepted dependency reuse decision conflicts with provider inspection")
            provider_fingerprint = row["provider_statement_fingerprint"]
            consumer_fingerprint = row["consumer_required_fingerprint"]
            if (
                re.fullmatch(r"[0-9a-f]{64}", provider_fingerprint) is None
                or re.fullmatch(r"[0-9a-f]{64}", consumer_fingerprint) is None
                or (decision == "reused_exact" and provider_fingerprint != consumer_fingerprint)
            ):
                raise ValueError("accepted dependency reuse decision has invalid statement fingerprints")
            wrapper = row.get("consumer_import_or_wrapper")
            if not isinstance(wrapper, str) or not wrapper or wrapper == "none":
                raise ValueError("accepted dependency reuse decision lacks a consumer import or wrapper")
            validate_receipt_references(
                row.get("provider_receipts"),
                evidence_root=evidence_root,
                theorem_id=expected_provider,
                phases={"proof", "validation", "release"},
                # Hard-edge admission already pins the exact provider bytes.
                # Reuse never inherits provider checkbox or receipt authority;
                # the consumer must close its own replay receipt below.
                require_accepted=False,
                authoritative_root=authoritative_root,
                require_successful_selftest=True,
                accepted_phase_states=inspected_phase_states.get(expected_provider),
            )
            validate_material_reference(
                row.get("provider_body_source"),
                evidence_root=evidence_root,
                authoritative_root=authoritative_root,
                owner=expected_provider,
                declaration=row["terminal_proof_body_id"],
                expected_fingerprint=provider_fingerprint,
            )
            validate_material_reference(
                row.get("consumer_import_source"),
                evidence_root=evidence_root,
                authoritative_root=authoritative_root,
                owner=theorem_id,
                declaration=wrapper,
                expected_fingerprint=consumer_fingerprint,
            )
            if source_id in hard_edges_by_id:
                validate_hard_edge_material_contract(
                    hard_edges_by_id[source_id],
                    provider_reference=row.get("provider_body_source"),
                    provider_declaration=row["terminal_proof_body_id"],
                    consumer_reference=row.get("consumer_import_source"),
                    consumer_declaration=wrapper,
                )
        else:
            reason = row.get("non_reuse_reason")
            if not isinstance(reason, str) or not reason:
                raise ValueError("non-accepted dependency reuse decision lacks non_reuse_reason")
        accounted.add(source_id)
    expected_sources = set(expected["hard_edge_ids"] + expected["reuse_hint_ids"] + expected["shared_group_ids"])
    if accounted != expected_sources or len(decisions) != len(expected_sources):
        raise ValueError("dependency reuse ledger does not decide every hard edge, hint, and shared group")
    unresolved = ledger.get("unresolved_compatibility_obligations")
    if not isinstance(unresolved, list) or any(not isinstance(item, str) or not item for item in unresolved):
        raise ValueError("dependency reuse ledger unresolved obligations must be a string list")
    if unresolved and any(
        isinstance(row, dict) and row.get("decision") in ACCEPTED_REUSE_DECISIONS
        for row in decisions
    ):
        raise ValueError("accepted dependency reuse decision has unresolved compatibility obligations")
    return ledger


def hard_edge_decision_blockers(
    ledger: dict[str, Any],
    theorem_id: str,
    *,
    require_consumer_validation: bool = False,
    require_accepted_consumer_validation: bool = False,
    evidence_root: Path = ROOT,
    authoritative_root: Path = ROOT,
    expected_base_revision: str | None = None,
    expected_commands: list[Any] | None = None,
) -> list[str]:
    graph, _ = theorem_dag_v2()
    incoming = [edge for edge in graph.get("hard_edges", []) if edge.get("child_theorem_id") == theorem_id]
    decisions = {row.get("source_id"): row for row in ledger["reuse_decisions"] if isinstance(row, dict)}
    blockers: list[str] = []
    phase_states = {
        item["phase"]: item["state"]
        for item in read_json(DAG).get("items", [])
        if item.get("theorem_id") == theorem_id
    }
    for edge in incoming:
        decision = decisions.get(edge["edge_id"], {})
        if decision.get("decision") not in ACCEPTED_REUSE_DECISIONS:
            blockers.append(f"{edge['edge_id']}: no accepted reuse decision")
        if require_consumer_validation:
            try:
                if require_accepted_consumer_validation:
                    validate_receipt_references(
                        decision.get("consumer_validation_receipts"),
                        evidence_root=evidence_root,
                        theorem_id=theorem_id,
                        phases={"validation"},
                        require_accepted=True,
                        accepted_phase_states=phase_states,
                        authoritative_root=authoritative_root,
                    )
                else:
                    validate_worker_selftest_receipt(
                        decision.get("consumer_validation_receipts"),
                        evidence_root=evidence_root,
                        theorem_id=theorem_id,
                        expected_base_revision=expected_base_revision,
                    )
                    validate_consumer_validation_commands(
                        decision.get("consumer_validation_receipts"),
                        evidence_root=evidence_root,
                        authoritative_root=authoritative_root,
                        theorem_id=theorem_id,
                        expected_commands=expected_commands,
                    )
            except ValueError as exc:
                blockers.append(f"{edge['edge_id']}: {exc}")
    return blockers


def enforce_master_hard_edge_gate(
    item: dict[str, Any],
    ledger: dict[str, Any] | None = None,
    *,
    evidence_root: Path = ROOT,
    authoritative_root: Path = ROOT,
    expected_base_revision: str | None = None,
    expected_commands: list[Any] | None = None,
) -> None:
    """Reject closure-relevant handoffs whose exact hard-edge evidence is open."""
    if item["phase"] not in {"proof", "validation", "release"}:
        return
    if not hard_parent_ids(item["theorem_id"]):
        return
    if ledger is None:
        ledger_path = ROOT / item["owned_paths"][0] / "dependency-reuse-ledger.json"
        try:
            ledger = validate_dependency_reuse_ledger(
                ledger_path,
                item["theorem_id"],
                evidence_root=evidence_root,
                authoritative_root=ROOT,
            )
        except ValueError as exc:
            raise ValueError(f"hard-edge master gate failed: {exc}") from exc
    # A proof handoff can truthfully establish only the inspected dependency
    # and reuse decision.  The consumer validation receipt is produced later,
    # so require it only for the validation/release closure gates.
    blockers = hard_edge_decision_blockers(
        ledger,
        item["theorem_id"],
        require_consumer_validation=item["phase"] in {"validation", "release"},
        require_accepted_consumer_validation=item["phase"] == "release",
        evidence_root=evidence_root,
        authoritative_root=authoritative_root,
        expected_base_revision=expected_base_revision,
        expected_commands=expected_commands,
    )
    if blockers:
        raise ValueError("hard-edge master gate failed: " + "; ".join(blockers))


def hard_edge_gate_status(theorem_id: str, phase: str) -> tuple[str, list[str]]:
    """Classify the target-local evidence required by each incoming hard edge."""
    graph, _ = theorem_dag_v2()
    incoming = [edge for edge in graph.get("hard_edges", []) if edge.get("child_theorem_id") == theorem_id]
    if not incoming:
        return "not_applicable", []
    directory = ROOT / "Stage1_Instances" / theorem_id
    blockers: list[str] = []
    ledger_path = directory / "dependency-reuse-ledger.json"
    try:
        ledger = validate_dependency_reuse_ledger(
            ledger_path,
            theorem_id,
            evidence_root=ROOT,
            authoritative_root=ROOT,
        )
    except ValueError as exc:
        legacy = audited_legacy_hard_edge_status(theorem_id)
        if legacy is not None:
            return legacy
        return "blocked", [str(exc)]
    blockers.extend(
        hard_edge_decision_blockers(
            ledger,
            theorem_id,
            require_consumer_validation=phase in {"validation", "release"},
            require_accepted_consumer_validation=phase == "release",
            authoritative_root=ROOT,
        )
    )
    return ("satisfied", []) if not blockers else ("blocked", blockers)


def audited_legacy_hard_edge_status(theorem_id: str) -> tuple[str, list[str]] | None:
    """Recognize pre-v2 exact edge receipts without manufacturing a v2 ledger."""
    graph, _ = theorem_dag_v2()
    incoming = [edge for edge in graph.get("hard_edges", []) if edge.get("child_theorem_id") == theorem_id]
    if not incoming:
        return None
    blockers: list[str] = []
    for edge in incoming:
        for row in edge.get("evidence", []):
            relative = row.get("path")
            digest = row.get("sha256")
            path = ROOT / relative if isinstance(relative, str) else ROOT
            if not path.is_file() or not isinstance(digest, str) or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                blockers.append(f"{edge.get('edge_id')}: stale admitted evidence")
    return ("legacy_evidence_present", []) if not blockers else ("blocked", blockers)


def task_id(theorem_id: str, phase: str) -> str:
    return f"S56-{theorem_id.removeprefix('THM-')}-{phase.upper()}"


def make_item(target: dict[str, Any], phase_index: int) -> dict[str, Any]:
    theorem_id = target["theorem_id"]
    phase, description = PHASES[phase_index]
    dependencies = [] if phase_index == 0 else [task_id(theorem_id, PHASES[phase_index - 1][0])]
    instance_dir = f"Stage1_Instances/{theorem_id}"
    return {
        "id": task_id(theorem_id, phase),
        "theorem_id": theorem_id,
        "execution_rank": target["execution_rank"],
        "phase": phase,
        "layer": phase_index,
        "state": "[ ]",
        "depends_on": dependencies,
        "owned_paths": [instance_dir],
        "deliverable": description,
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }


def new_dag() -> dict[str, Any]:
    targets = target_rows()
    items = [make_item(target, phase) for target in targets for phase in range(len(PHASES))]
    ids = "\n".join(sorted(target["theorem_id"] for target in targets)) + "\n"
    return {
        "schema_version": "stage1-execution-dag/1.0",
        "requirements_source": "Docs/Stage1_Blueprint_rev-5.6.md",
        "target_manifest": "Docs/Stage1_Targets_rev-5.6.json",
        "target_id_set_sha256": hashlib.sha256(ids.encode()).hexdigest(),
        "state_protocol": {"not_done": "[ ]", "worker_self_tested": "[_]", "master_accepted": "[x]"},
        "items": items,
    }


def topological_order(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {item.get("id"): item for item in items}
    if len(by_id) != len(items) or None in by_id:
        fail("execution DAG has duplicate or missing item ids")
    indegree = {item_id: 0 for item_id in by_id}
    children: dict[str, list[str]] = {item_id: [] for item_id in by_id}
    for item in items:
        dependencies = item.get("depends_on")
        if not isinstance(dependencies, list):
            fail(f"{item['id']} has invalid dependency list")
        for dependency in dependencies:
            if dependency not in by_id:
                fail(f"{item['id']} depends on missing item {dependency}")
            indegree[item["id"]] += 1
            children[dependency].append(item["id"])
    ready = deque(sorted((item_id for item_id, degree in indegree.items() if degree == 0), key=lambda i: (by_id[i]["layer"], by_id[i]["execution_rank"], i)))
    ordered: list[dict[str, Any]] = []
    while ready:
        item_id = ready.popleft()
        ordered.append(by_id[item_id])
        for child in sorted(children[item_id], key=lambda i: (by_id[i]["layer"], by_id[i]["execution_rank"], i)):
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
    if len(ordered) != len(items):
        fail("execution DAG contains a cycle")
    return ordered


def validate_dag(data: dict[str, Any]) -> list[dict[str, Any]]:
    if data.get("schema_version") != "stage1-execution-dag/1.0":
        fail("unsupported execution DAG schema")
    if data.get("requirements_source") != "Docs/Stage1_Blueprint_rev-5.6.md":
        fail("execution DAG requirements source is not the rev-5.6 blueprint")
    items = data.get("items")
    if not isinstance(items, list) or len(items) != 1546 * len(PHASES):
        fail(f"execution DAG must contain exactly {1546 * len(PHASES)} phase items")
    targets = target_rows()
    target_ids = {target["theorem_id"] for target in targets}
    items_by_target: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        if not isinstance(item, dict) or item.get("state") not in VALID_STATES:
            fail("execution DAG contains an invalid item state")
        theorem_id = item.get("theorem_id")
        if theorem_id not in target_ids:
            fail(f"execution DAG item has unknown target {theorem_id}")
        if not isinstance(item.get("owned_paths"), list) or not item["owned_paths"]:
            fail(f"{item.get('id')} has no owned paths")
        attempts = item.get("attempts", 0)
        if isinstance(attempts, bool) or not isinstance(attempts, int) or attempts < 0:
            fail(f"{item.get('id')} has an invalid attempts count")
        items_by_target.setdefault(theorem_id, []).append(item)
    if set(items_by_target) != target_ids or any(len(group) != len(PHASES) for group in items_by_target.values()):
        fail("every target must have exactly one item per execution phase")
    for theorem_id, group in items_by_target.items():
        by_phase = {item.get("phase"): item for item in group}
        if set(by_phase) != {phase for phase, _ in PHASES}:
            fail(f"{theorem_id} has an invalid phase set")
        for index, (phase, _) in enumerate(PHASES):
            item = by_phase[phase]
            if item.get("id") != task_id(theorem_id, phase) or item.get("layer") != index:
                fail(f"{theorem_id}/{phase} has unstable identity or layer")
            expected = [] if index == 0 else [task_id(theorem_id, PHASES[index - 1][0])]
            if item.get("depends_on") != expected:
                fail(f"{theorem_id}/{phase} has invalid dependencies")
            if item["state"] == "[x]" and any(by_phase[prior]["state"] != "[x]" for prior, _ in PHASES[:index]):
                fail(f"{item['id']} is accepted before a dependency")
    return topological_order(items)


def render_checklist(items: list[dict[str, Any]]) -> str:
    lines = [
        CHECKLIST_BEGIN,
        "## 13. Generated 1546-Target Execution Checklist",
        "",
        "This appendix is generated by `scripts/stage1_execution_cron.py --bootstrap`. The typed DAG at",
        "`Docs/Stage1_Execution_DAG_rev-5.6.json` is the execution-state authority; this Markdown rendering",
        "is retained in the normative blueprint for inspection. Do not edit either surface by hand.",
        "",
        "Every target is expanded into seven dependency-ordered phases: intake, statement, anchor audit,",
        "obligation tree, proof, validation, and release. `[ ]` and `[_]` are unfinished; only the master",
        "integration lane may render `[x]` after all rev-5.6 receipts and gates pass.",
        "",
    ]
    for item in sorted(items, key=lambda row: (row["execution_rank"], row["layer"])):
        depends = ", ".join(f"`{dependency}`" for dependency in item["depends_on"]) or "none"
        paths = ", ".join(f"`{path}`" for path in item["owned_paths"])
        lines.append(
            f"- {item['state']} `{item['id']}` / `{item['theorem_id']}` / `{item['phase']}`: {item['deliverable']}"
        )
        lines.append(f"  Depends: {depends}. Owned paths: {paths}. Gate: {item['completion_gate']}.")
    lines.extend(["", CHECKLIST_END, ""])
    return "\n".join(lines)


def write_projection(data: dict[str, Any]) -> None:
    items = validate_dag(data)
    blueprint = BLUEPRINT.read_text(encoding="utf-8")
    rendered = render_checklist(items)
    if CHECKLIST_BEGIN in blueprint or CHECKLIST_END in blueprint:
        if CHECKLIST_BEGIN not in blueprint or CHECKLIST_END not in blueprint:
            fail("blueprint has malformed execution checklist markers")
        pattern = re.escape(CHECKLIST_BEGIN) + r".*?" + re.escape(CHECKLIST_END) + r"\n?"
        blueprint, count = re.subn(pattern, rendered, blueprint, count=1, flags=re.DOTALL)
        if count != 1:
            fail("blueprint execution checklist markers are ambiguous")
    else:
        blueprint = blueprint.rstrip() + "\n\n" + rendered
    atomic_write(BLUEPRINT, blueprint)


def bootstrap() -> None:
    data = read_json(DAG) if DAG.exists() else new_dag()
    validate_dag(data)
    atomic_write(DAG, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    run(["python3", "Docs/tools/generate_stage1_theorem_dag_v2.py"])
    theorem_dag_v2.cache_clear()
    run(["python3", "Docs/tools/check_stage1_theorem_dag_v2.py"])
    write_projection(data)
    print(f"bootstrapped {len(data['items'])} phase items for 1546 targets")


def load_dag() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not DAG.exists():
        fail("execution DAG is missing; run --bootstrap first")
    data = read_json(DAG)
    return data, validate_dag(data)


def runtime_path(name: str) -> Path:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    return RUNTIME / name


def load_claims() -> list[dict[str, Any]]:
    path = runtime_path("claims.json")
    if not path.exists():
        return []
    claims = read_json(path).get("claims", [])
    if not isinstance(claims, list):
        fail("claim ledger is malformed")
    return [claim for claim in claims if isinstance(claim, dict)]


def save_claims(claims: list[dict[str, Any]]) -> None:
    atomic_write(runtime_path("claims.json"), json.dumps({"claims": claims}, indent=2) + "\n")


def pid_alive(pid: Any) -> bool:
    return isinstance(pid, int) and pid > 0 and Path(f"/proc/{pid}").exists()


def session_is_live(session: Any) -> bool:
    if not isinstance(session, str):
        return False
    result = run(["tmux", "list-panes", "-t", session, "-F", "#{pane_dead}"], check=False)
    return result.returncode == 0 and any(line.strip() == "0" for line in result.stdout.splitlines())


def snapshot_blocked_worker(claim: dict[str, Any]) -> tuple[list[str], Path]:
    """Copy a fail-closed worker's owned delta before its reusable slot is reset."""
    item_id = claim.get("item_id")
    if not isinstance(item_id, str) or re.fullmatch(r"S56-M-[0-9]{4}-[A-Z_]+", item_id) is None:
        raise ValueError("blocked claim has an unsafe item id")
    workspace = Path(str(claim.get("workspace", "")))
    owned_paths = claim.get("owned_paths")
    if not isinstance(owned_paths, list) or len(owned_paths) != 1 or not isinstance(owned_paths[0], str):
        raise ValueError("blocked claim has invalid ownership metadata")
    owner = owned_paths[0] + "/"
    changed = validate_owned_relative_paths(worker_changed_paths(workspace, owner), owner)
    snapshot = runtime_path("blocked-reports") / item_id
    shutil.rmtree(snapshot, ignore_errors=True)
    for relative in changed:
        source = contained_regular_file(workspace, relative, owner)
        destination = snapshot / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    atomic_write(snapshot / "manifest.json", json.dumps({"changed_paths": changed}, indent=2) + "\n")
    return changed, snapshot


def validated_blocked_snapshot(item_id: str, value: Any) -> Path:
    """Accept only the scheduler-created snapshot directory for this item."""
    if not isinstance(value, str) or not value:
        raise ValueError("blocked snapshot path is missing")
    runtime_resolved = RUNTIME.resolve()
    if RUNTIME.is_symlink() or not runtime_resolved.is_relative_to(ROOT.resolve()):
        raise ValueError("scheduler runtime storage escapes the repository")
    blocked_root = RUNTIME / "blocked-reports"
    if blocked_root.is_symlink():
        raise ValueError("blocked snapshot storage is a symlink")
    expected = blocked_root / item_id
    snapshot = Path(value)
    if (
        not snapshot.is_absolute()
        or snapshot.is_symlink()
        or snapshot.absolute() != expected.absolute()
        or snapshot.resolve() != expected.resolve()
        or not snapshot.resolve().is_relative_to(runtime_resolved)
        or not snapshot.is_dir()
    ):
        raise ValueError("blocked snapshot is outside scheduler-owned storage")
    return snapshot


def refresh_claims(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    states = {item["id"]: item["state"] for item in items}
    item_by_id = {item["id"]: item for item in items}
    raw_claims = load_claims()
    active_statuses = {"live", "preparing", "launch_failed", "draining", "finished"}
    root_resolved = ROOT.resolve()
    runtime_resolved = RUNTIME.resolve()
    workers_root = RUNTIME / "workers"
    if (
        RUNTIME.is_symlink()
        or not runtime_resolved.is_relative_to(root_resolved)
        or workers_root.is_symlink()
        or (workers_root.exists() and not workers_root.resolve().is_relative_to(runtime_resolved))
    ):
        fail("scheduler worker storage escapes the repository or contains a symlink root")
    _, theorem_nodes = theorem_dag_v2()
    identity_counts: Counter[tuple[str, Any]] = Counter()
    for claim in raw_claims:
        if claim.get("status") not in active_statuses:
            continue
        for field in ("item_id", "session", "slot", "workspace"):
            value = claim.get(field)
            if value is not None:
                identity_counts[(field, value)] += 1
    current_revision = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    kept: list[dict[str, Any]] = []
    released: list[dict[str, Any]] = []
    for claim in raw_claims:
        item = item_by_id.get(claim.get("item_id"))
        if item is None:
            # Runtime state is not an authority surface. Preserve malformed or
            # obsolete rows for audit, but never derive tmux/filesystem side
            # effects from an identity absent from the validated DAG.
            claim["status"] = "quarantined"
            claim["quarantined_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["quarantine_reason"] = "claim item is absent from the authoritative DAG"
            kept.append(claim)
            continue
        if claim.get("theorem_id") != item["theorem_id"] or claim.get("owned_paths") != item["owned_paths"]:
            claim["status"] = "quarantined"
            claim["quarantined_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["quarantine_reason"] = "claim authority metadata disagrees with the validated DAG"
            kept.append(claim)
            continue
        slot = claim.get("slot")
        session = claim.get("session")
        workspace_value = claim.get("workspace")
        output_value = claim.get("output_log")
        expected_rank = theorem_nodes[item["theorem_id"]]["v2_execution_rank"]
        expected_session = f"stage1r56-{slot}-{expected_rank:04d}" if isinstance(slot, int) else None
        expected_workspace = RUNTIME / "workers" / f"slot{slot}" if isinstance(slot, int) else None
        expected_output = RUNTIME / "logs" / f"{item['id']}.out"
        runtime_bound = claim.get("status") in active_statuses | {"blocked"}
        active_runtime = claim.get("status") in active_statuses
        if runtime_bound and (
            (
                active_runtime
                and any(identity_counts[(field, claim.get(field))] > 1 for field in ("item_id", "session", "slot", "workspace"))
            )
            or (
            not isinstance(slot, int)
            or isinstance(slot, bool)
            or slot < 1
            or slot > MAX_WORKERS * 4
            or not isinstance(workspace_value, str)
            or Path(workspace_value).absolute() != expected_workspace.absolute()
            or Path(workspace_value).is_symlink()
            or (
                Path(workspace_value).exists()
                and not Path(workspace_value).resolve().is_relative_to(runtime_resolved)
            )
            or not isinstance(output_value, str)
            or Path(output_value).absolute() != expected_output.absolute()
            )
            or (active_runtime and session != expected_session)
        ):
            claim["status"] = "quarantined"
            claim["quarantined_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["quarantine_reason"] = "claim runtime identity is not scheduler-canonical"
            kept.append(claim)
            continue
        if states[item["id"]] == "[x]":
            if claim.get("status") in {"live", "preparing", "launch_failed", "draining"} and session_is_live(session):
                if isinstance(session, str):
                    run(["tmux", "kill-session", "-t", session], check=False)
                if session_is_live(session):
                    claim["status"] = "draining"
                    claim["drain_reason"] = "master accepted but worker session did not stop"
                    kept.append(claim)
                    continue
            claim["released_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["release_reason"] = "master_accepted"
            released.append(claim)
            continue
        if claim.get("status") == "draining":
            if session_is_live(session):
                run(["tmux", "kill-session", "-t", str(session)], check=False)
            if session_is_live(session):
                claim["drain_retried_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                kept.append(claim)
            else:
                claim["released_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                claim["release_reason"] = "draining worker session stopped"
                released.append(claim)
            continue
        if claim.get("status") in {"preparing", "launch_failed"}:
            session = claim.get("session")
            workspace = Path(str(claim.get("workspace", "")))
            manifest = workspace / ".stage1-worker-selftest.json"
            if session_is_live(session):
                pid_result = run(
                    ["tmux", "list-panes", "-t", str(session), "-F", "#{pane_pid}"],
                    check=False,
                )
                pid_text = pid_result.stdout.strip()
                claim["status"] = "live"
                claim["pid"] = int(pid_text) if pid_text.isdigit() else None
                claim["recovered_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                kept.append(claim)
            elif manifest.is_file() and not manifest.is_symlink():
                claim["status"] = "finished"
                claim["selftest_manifest"] = (
                    str(manifest.relative_to(ROOT)) if manifest.is_relative_to(ROOT) else str(manifest)
                )
                claim["recovered_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                kept.append(claim)
            else:
                if isinstance(session, str):
                    run(["tmux", "kill-session", "-t", session], check=False)
                claim["released_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                claim["release_reason"] = "incomplete worker launch reservation"
                released.append(claim)
            continue
        if claim.get("status") == "live" and not session_is_live(claim.get("session")):
            session = claim.get("session")
            if isinstance(session, str):
                run(["tmux", "kill-session", "-t", session], check=False)
            manifest = Path(claim.get("workspace", "")) / ".stage1-worker-selftest.json"
            if manifest.exists():
                claim["status"] = "finished"
                claim["selftest_manifest"] = str(manifest.relative_to(ROOT)) if manifest.is_relative_to(ROOT) else str(manifest)
                kept.append(claim)
            else:
                # A worker that deliberately fails closed must not be relaunched on
                # the same repository revision forever.  Keep its negative result
                # in the runtime ledger while freeing the slot for another DAG node.
                # Retry requires an explicit operator decision backed by new source
                # evidence, rather than incidental commits elsewhere in the queue.
                claim["status"] = "blocked"
                claim["blocked_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                claim["block_reason"] = "worker_exited_without_selftest"
                claim["base_revision"] = claim.get("base_revision", current_revision)
                try:
                    changed, snapshot = snapshot_blocked_worker(claim)
                    claim["blocked_snapshot"] = str(snapshot)
                    claim["blocked_snapshot_paths"] = changed
                except ValueError as exc:
                    claim["blocked_artifact_rejection_reason"] = str(exc)
                kept.append(claim)
        else:
            kept.append(claim)
    if released:
        audit = runtime_path("released_claims.jsonl")
        with audit.open("a", encoding="utf-8") as handle:
            for claim in released:
                handle.write(json.dumps(claim) + "\n")
    save_claims(kept)
    return kept


def enforce_worker_cap(claims: list[dict[str, Any]], max_workers: int) -> list[dict[str, Any]]:
    """Preserve existing lanes when the configured cap is lowered.

    The cap controls new allocation only. In-flight workers retain their
    worktree and finish naturally, preventing evidence loss on a downscale.
    """
    return claims


def trim_file(path: Path, max_bytes: int) -> None:
    if path.is_symlink():
        fail(f"refuse to trim symlinked scheduler log: {path}")
    if path.exists() and path.stat().st_size > max_bytes:
        with path.open("rb") as handle:
            handle.seek(-max_bytes, os.SEEK_END)
            tail = handle.read()
        durable_write_bytes(path, tail)


def space_guard(claims: list[dict[str, Any]]) -> None:
    # Keep enough room for the OS, but do not impose a scheduler-local quota
    # on an execution run explicitly authorized to use the available volume.
    min_free_gb = int(os.environ.get("MIN_FREE_GB", "1"))
    danger_free_gb = int(os.environ.get("DANGER_FREE_GB", "1"))
    max_log_mb = int(os.environ.get("MAX_LOG_MB", "1024"))
    max_keepalive_mb = int(os.environ.get("MAX_KEEPALIVE_MB", "256"))
    retention_days = int(os.environ.get("LOG_RETENTION_DAYS", "30"))
    RUNTIME.mkdir(parents=True, exist_ok=True)
    now = time.time()
    for path in RUNTIME.rglob("*"):
        if not path.is_file():
            continue
        if path.is_symlink():
            fail(f"scheduler runtime contains a symlinked log file: {path}")
        if path.name == "keepalive.log":
            trim_file(path, max_keepalive_mb * 1024 * 1024)
        elif path.suffix in {".log", ".out", ".err"}:
            if now - path.stat().st_mtime > retention_days * 86400:
                path.unlink(missing_ok=True)
            else:
                trim_file(path, max_log_mb * 1024 * 1024)
    usage = shutil.disk_usage(ROOT)
    free_gb = usage.free // (1024**3)
    # Do not recursively size active worker worktrees: at high concurrency it
    # is both a scheduler-local quota and slow enough to delay refills.
    state = {"free_gb": free_gb, "cron_root_gb": None, "checked_at": dt.datetime.now(dt.timezone.utc).isoformat()}
    atomic_write(runtime_path("space_guard.json"), json.dumps(state, indent=2) + "\n")
    if free_gb < danger_free_gb:
        fail(f"blocked_disk_space: only {free_gb} GiB free (danger threshold {danger_free_gb})")
    if free_gb < min_free_gb:
        fail(f"blocked_disk_space: only {free_gb} GiB free (minimum {min_free_gb})")


def sync_guard() -> None:
    status = run(["git", "status", "--porcelain"], check=True).stdout
    if status.strip():
        fail("blocked_sync: tracked or untracked local changes exist; refuse to stash user work automatically")
    run(["git", "fetch", "--prune", "origin"])
    upstream = run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"]).stdout.strip()
    head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    remote = run(["git", "rev-parse", upstream]).stdout.strip()
    if head != remote:
        run(["git", "merge", "--ff-only", upstream])
        head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    if head != remote:
        fail("blocked_sync: local HEAD does not match remote tracking HEAD")


def checkpoint_sync_guard() -> None:
    """Allow only the dirty paths already bound by a pending checkpoint."""
    pending = read_json(runtime_path("pending_checkpoint.json"))
    rows = pending.get("paths")
    allowed = {
        row.get("path")
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    } if isinstance(rows, list) else set()
    status = run(["git", "status", "--porcelain"]).stdout.splitlines()
    dirty = {line[3:] for line in status if len(line) >= 4}
    if dirty - allowed:
        fail(f"blocked_sync: changes outside pending checkpoint: {sorted(dirty - allowed)}")
    run(["git", "fetch", "--prune", "origin"])
    upstream = run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"]).stdout.strip()
    remote = run(["git", "rev-parse", upstream]).stdout.strip()
    base = pending.get("base_revision")
    state = pending.get("state")
    expected_head = pending.get("commit_revision") if state == "committed_unpushed" else base
    head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    if state == "integrated_uncommitted" and isinstance(base, str) and head != base:
        # A commit may have completed immediately before the journal state was
        # advanced. Permit only its direct child here; the checkpoint gate will
        # bind its exact paths and bytes before any push.
        ancestry = run(["git", "rev-list", "--parents", "-n", "1", head]).stdout.split()
        if len(ancestry) == 2 and ancestry[1] == base:
            expected_head = head
    if (
        not isinstance(base, str)
        or not isinstance(expected_head, str)
        or head != expected_head
        or remote not in {base, expected_head}
    ):
        fail("blocked_sync: pending checkpoint revision no longer matches its authority base")


def task_prompt(item: dict[str, Any], workspace: Path) -> str:
    item_json = json.dumps(item, ensure_ascii=False, indent=2)
    _, theorem_nodes = theorem_dag_v2()
    theorem_node = theorem_nodes[item["theorem_id"]]
    dependency_context = json.dumps(
        {
            "graph_sha256": graph_sha256(),
            "dependency_context_sha256": theorem_node.get("dependency_context_sha256"),
            "theorem_node": theorem_node,
            "required_ledger_context": expected_dependency_context(item["theorem_id"]),
            "ledger_schema": DEPENDENCY_LEDGER_SCHEMA,
        },
        ensure_ascii=False,
        indent=2,
    )
    return f"""You are Stage1 rev-5.6 worker for exactly one Lean 4 theorem execution task.

Repository root: {workspace}
Work only inside this worker automation clone: {workspace}
Do not edit the scheduler's authoritative checkout directly: {ROOT}

Active /goal: fully and truthfully expand and validate all 1546 metadata-screened Lean 4 targets under Docs/Stage1_Blueprint_rev-5.6.md. Do not claim theorem completion without every rev-5.6 gate and kernel evidence.

Resume the active `/goal` now. If your current context has reached capacity,
write the required target-scoped artifact or self-test handoff immediately and
exit cleanly so the scheduler can integrate it and continue the goal in a
fresh worker context. Do not wait for an interactive operator message.

Your assigned item is the only item you may claim:
{item_json}

The authoritative v2 dependency/reuse context for this theorem is:
{dependency_context}

Required work:
1. Read Docs/Stage1_Blueprint_v2.md, Docs/Stage1_Blueprint_rev-5.6.md, skills/execute-stage1-rev56/SKILL.md, the target manifest entry, and the target node in Docs/Stage1_Theorem_DAG_v2.json.
2. Complete the assigned phase with real source, Lean, and/or evidence artifacts under the item's owned path. You may inspect shared read-only sources, but never modify another target's owned path. Never use sorry, axiom, placeholder, fake results, or a broadened/substituted theorem.
   Before proof work, traverse every direct and transitive parent in the v2 node, inspect its current rev-5.6 phase state and exact reusable artifacts, and create or refresh the target-owned dependency-reuse-ledger.json required by the execution skill. Use schema {DEPENDENCY_LEDGER_SCHEMA} and exactly the graph digest/context IDs above. The ledger must include inspections, reuse_decisions, and unresolved_compatibility_obligations as specified by the skill. Empty parent/hint/group closure still requires an empty audited ledger. A reuse_hint or [_] ancestor is informative only and cannot transfer proof credit.
3. Run the smallest real validation available and record exact commands/results in the owned artifact.
   The worker clone reuses the canonical pinned Lean `.lake` artifacts when available. Do not run
   `lake update`, `lake build`, dependency `git clone`/`git fetch`, or otherwise mutate `.lake`;
   those actions are neither a pinned validation nor valid worker evidence. Use the existing
   toolchain with `lake env lean` for narrowly scoped elaboration checks, and record a missing
   artifact as a blocker rather than fetching a moving dependency.
4. Do not edit Docs/Stage1_Execution_DAG_rev-5.6.json, Docs/Stage1_Theorem_DAG_v2.json, either blueprint, the generated checklist, or any item state. You are a worker, never the master.
5. If and only if your assigned phase is genuinely self-tested, write `.stage1-worker-selftest.json` at the workspace root with item_id, changed_paths, commands, output_summary, base_revision, known_failures, and `state: "[_]"`. Otherwise leave no self-test manifest and explain the blocker in an owned artifact.
6. Do not commit, push, or modify unrelated targets. The integration lane will inspect this clone.
"""


def worker_command(workspace: Path, prompt_path: Path, output_path: Path) -> str:
    model = CODEX_MODEL
    effort = CODEX_REASONING_EFFORT
    if effort not in ALLOWED_REASONING_EFFORTS:
        fail(f"CODEX_REASONING_EFFORT must be one of {sorted(ALLOWED_REASONING_EFFORTS)}")
    # Stage1 workers must use the standard-priority lane.  Do not inherit a
    # caller's ``fast`` setting: the scheduler owns this execution policy.
    service_tier = CODEX_SERVICE_TIER
    return (
        f"cd {shlex_quote(str(workspace))} && "
        f"codex exec --cd {shlex_quote(str(workspace))} --model {shlex_quote(model)} "
        f"-c features.code_mode_host=false -c model_reasoning_effort={shlex_quote(effort)} "
        f"-c service_tier={shlex_quote(service_tier)} "
        f"--sandbox danger-full-access "
        f"< {shlex_quote(str(prompt_path))} > {shlex_quote(str(output_path))} 2>&1"
    )


def shlex_quote(value: str) -> str:
    import shlex

    return shlex.quote(value)


def prepare_workspace(slot: int) -> Path:
    workspace = RUNTIME / "workers" / f"slot{slot}"
    validate_runtime_root()
    if workspace.is_symlink():
        fail(f"worker slot path is a symlink: {workspace}")
    if workspace.exists():
        # A worker may have just released a clone while its final filesystem
        # cleanup is still in flight.  Retry ENOTEMPTY rather than aborting
        # the entire refill pass and leaving otherwise-free slots idle.
        for attempt in range(6):
            try:
                shutil.rmtree(workspace)
                break
            except FileNotFoundError:
                break
            except OSError as exc:
                if exc.errno != errno.ENOTEMPTY or attempt == 5:
                    raise
                time.sleep(0.2 * (attempt + 1))
    workspace.parent.mkdir(parents=True, exist_ok=True)
    # Shared clones would inherit the 7.5 GiB local Lean build tree.  Create a lightweight
    # source-only worktree instead and let workers inspect the canonical local toolchain read-only.
    run([
        "git", "clone", "--no-checkout", "--filter=blob:none", "--reference-if-able", str(ROOT),
        str(ROOT), str(workspace),
    ], cwd=ROOT)
    run(["git", "checkout", "--detach", "HEAD"], cwd=workspace)
    if workspace.is_symlink() or not workspace.resolve().is_relative_to(RUNTIME.resolve()):
        fail("prepared worker workspace escaped scheduler storage")
    for relative in (
        "Docs/Stage1_Blueprint_v2.md", "Docs/Stage1_Theorem_DAG_v2.json",
        "Docs/Stage1_Blueprint_rev-5.6.md", "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "Docs/Stage1_Targets_rev-5.6.json", "skills/execute-stage1-rev56/SKILL.md",
    ):
        source, destination = ROOT / relative, workspace / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    # Lean worker clones are source-only to keep 12 lanes practical.  Reuse the
    # canonical checkout's pinned build artifacts read-only rather than asking
    # every statement worker to run `lake update` and fetch dependencies again.
    canonical_lean = ROOT / "Formalizations" / "Lean"
    worker_lean = workspace / "Formalizations" / "Lean"
    canonical_lake = canonical_lean / ".lake"
    worker_lake = worker_lean / ".lake"
    if canonical_lake.is_dir() and worker_lean.is_dir() and not worker_lake.exists():
        worker_lake.symlink_to(canonical_lake)
    return workspace


def write_todo(data: dict[str, Any], ordered: list[dict[str, Any]], claims: list[dict[str, Any]]) -> Path:
    ordered = order_by_v2(ordered)
    counts = Counter(item["state"] for item in ordered)
    theorem_states: dict[str, list[str]] = {}
    for item in ordered:
        theorem_states.setdefault(item["theorem_id"], []).append(item["state"])
    theorem_counts = Counter()
    for states in theorem_states.values():
        if all(state == "[x]" for state in states):
            theorem_counts["completed"] += 1
        elif all(state == "[_]" for state in states):
            theorem_counts["fully_self_tested"] += 1
        elif all(state == "[ ]" for state in states):
            theorem_counts["unstarted"] += 1
        else:
            theorem_counts["partial"] += 1
    claim_by_item = {claim.get("item_id"): claim for claim in claims}
    ready = []
    workers = []
    for item in ordered:
        claim = claim_by_item.get(item["id"])
        claim_state = "unclaimed" if claim is None else f"{claim.get('status')}:{claim.get('session', 'unknown')}"
        phase_deps_done = all(next(row for row in ordered if row["id"] == dependency)["state"] == "[x]" for dependency in item["depends_on"])
        if item["phase"] in {"proof", "validation", "release"}:
            hard_gate, hard_blockers = hard_edge_gate_status(item["theorem_id"], item["phase"])
        else:
            hard_gate, hard_blockers = "not_applicable_for_phase", []
        deps_done = phase_deps_done and hard_gate != "blocked"
        if item["state"] == "[_]":
            ready.append((item, claim_state, phase_deps_done, deps_done, hard_gate, hard_blockers))
        elif item["state"] == "[ ]" and claim is None:
            workers.append((item, claim_state, phase_deps_done, deps_done, hard_gate, hard_blockers))
    today = dt.date.today().strftime("%Y%m%d")
    path = DOCS / f"todos_{today}.md"
    lines = [
        "# Stage1 rev-5.6 Execution Todo",
        "",
        "Source: `Docs/Stage1_Blueprint_v2.md`; assurance/state bases: `Docs/Stage1_Blueprint_rev-5.6.md` and `Docs/Stage1_Execution_DAG_rev-5.6.json`; theorem order: `Docs/Stage1_Theorem_DAG_v2.json`.",
        f"Not done: {counts['[ ]']}",
        f"Worker self-tested: {counts['[_]']}",
        f"Master accepted: {counts['[x]']}",
        f"Unfinished: {counts['[ ]'] + counts['[_]']}",
        f"Theorems master-complete [x] x7: {theorem_counts['completed']}",
        f"Theorems fully self-tested [_] x7: {theorem_counts['fully_self_tested']}",
        f"Theorems partial [_]/[ ]: {theorem_counts['partial']}",
        f"Theorems unstarted [ ] x7: {theorem_counts['unstarted']}",
        "DAG cycle check: passed.",
        f"Claim ledger: `.cron/stage1-rev56/claims.json`; live worker claims: {sum(c.get('status') == 'live' for c in claims)}.",
        "",
        "## Worker Claim Frontier",
        "",
        "| Item | Target | Phase | Phase deps accepted | Hard-edge gate | Claim | Owned path |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item, claim_state, phase_deps_done, deps_done, hard_gate, hard_blockers in workers:
        hard_display = hard_gate if not hard_blockers else f"{hard_gate}: {len(hard_blockers)} blocker(s); see target ledger"
        lines.append(f"| `{item['id']}` | `{item['theorem_id']}` | {item['phase']} | {phase_deps_done} | {hard_display} | {claim_state} | `{item['owned_paths'][0]}` |")
    lines.extend(["", "## Master Integration Frontier", "", "| Item | Phase deps accepted | Hard-edge gate | Claim |", "| --- | --- | --- | --- |"])
    for item, claim_state, phase_deps_done, deps_done, hard_gate, hard_blockers in ready:
        hard_display = hard_gate if not hard_blockers else f"{hard_gate}: {len(hard_blockers)} blocker(s); see target ledger"
        lines.append(f"| `{item['id']}` | {phase_deps_done} | {hard_display} | {claim_state} |")
    lines.append("")
    atomic_write(path, "\n".join(lines))
    return path


def validate_only() -> None:
    run(["python3", "Docs/tools/check_stage1_theorem_dag_v2.py"])
    data, ordered = load_dag()
    theorem_graph, _ = theorem_dag_v2()
    # A dry gate must not kill sessions, snapshot workspaces, rewrite ledgers,
    # trim logs, or otherwise reconcile mutable scheduler state.
    claims = load_claims()
    todo = write_todo(data, ordered, claims)
    print("validate-only: ok")
    print("requirements_source=Docs/Stage1_Blueprint_v2.md")
    print(
        "assurance_source=Docs/Stage1_Blueprint_rev-5.6.md "
        "theorem_dag=Docs/Stage1_Theorem_DAG_v2.json "
        f"hard_edges={len(theorem_graph.get('hard_edges', []))} "
        f"reuse_hints={len(theorem_graph.get('reuse_hints', []))}"
    )
    print(f"items={len(ordered)} targets=1546 states={dict(Counter(item['state'] for item in ordered))}")
    print(
        "platform=codex "
        f"model={CODEX_MODEL} "
        f"reasoning_effort={CODEX_REASONING_EFFORT} "
        f"service_tier={CODEX_SERVICE_TIER}"
    )
    print(f"todo={todo.relative_to(ROOT)}")


def integrate(limit: int) -> int:
    """Run one all-or-none integration transaction."""
    if limit < 0 or limit > MAX_WORKERS:
        fail(f"--limit must be in 0..{MAX_WORKERS}")
    recover_integration_wal()
    if runtime_path("pending_checkpoint.json").exists():
        fail("pending checkpoint must be resumed before another integration pass")
    data, ordered = load_dag()
    ordered = order_by_v2(ordered)
    # Lease reconciliation is its own durable preflight. A later integration
    # rollback restores this post-refresh state rather than resurrecting dead
    # sessions or discarding their scheduler-owned blocker snapshots.
    claims = refresh_claims(ordered)
    transaction = FileTransaction(runtime_path("integration_wal.json"))
    try:
        integrated = _integrate(limit, transaction, data, ordered, claims)
        # A successful integration is now guarded by the content-bound pending
        # checkpoint. Removing the rollback WAL is the final local transition.
        transaction.commit()
        return integrated
    except BaseException:
        transaction.rollback()
        theorem_dag_v2.cache_clear()
        raise


def _integrate(
    limit: int,
    transaction: FileTransaction,
    data: dict[str, Any],
    ordered: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> int:
    """Verify worker handoffs and preserve bounded fail-closed reports."""
    # These projections and scheduler surfaces can be rewritten after worker
    # files land. Snapshot them before any copy so integration is all-or-none.
    for path in (
        DAG,
        THEOREM_DAG_V2,
        BLUEPRINT,
        runtime_path("claims.json"),
        runtime_path("integration_queue.json"),
        runtime_path("pending_checkpoint.json"),
        DOCS / f"todos_{dt.date.today():%Y%m%d}.md",
    ):
        transaction.snapshot(path)
    by_id = {item["id"]: item for item in data["items"]}
    ready = [claim for claim in claims if claim.get("status") == "finished"][:limit]
    remaining = limit - len(ready)
    blocked_ready = [
        claim
        for claim in claims
        if claim.get("status") == "blocked"
        and not claim.get("blocked_artifacts_merged_at")
        and not claim.get("blocked_artifact_rejection_reason")
    ][:remaining]
    accepted: list[str] = []
    rejected: list[dict[str, str]] = []
    preserved_blockers: list[str] = []
    queue: list[dict[str, Any]] = []
    for claim in ready:
        claim_transaction = FileTransaction(wal_parent=transaction)
        item = by_id.get(claim.get("item_id"))
        workspace = Path(str(claim.get("workspace", "")))
        handoff = workspace / ".stage1-worker-selftest.json"
        try:
            if item is None:
                raise ValueError("claim refers to unknown item")
            if item["state"] != "[ ]":
                raise ValueError("finished claim no longer targets a not-done authoritative item")
            packet = json.loads(handoff.read_text(encoding="utf-8"))
            changed_paths = packet.get("changed_paths")
            owner = item["owned_paths"][0] + "/"
            if packet.get("item_id") != item["id"] or packet.get("state") != "[_]":
                raise ValueError("worker packet identity/state mismatch")
            if packet.get("base_revision") != claim.get("base_revision"):
                raise ValueError("worker packet base revision disagrees with its claim")
            packet_commands = packet.get("commands")
            if (
                not isinstance(packet_commands, list)
                or not packet_commands
                or any(not isinstance(command, (str, dict)) for command in packet_commands)
            ):
                raise ValueError("worker packet lacks exact validation commands")
            if not isinstance(changed_paths, list) or not changed_paths:
                raise ValueError("worker packet lacks changed paths")
            allowed_worker_metadata = {".stage1-worker-selftest.json"}
            if any(
                not isinstance(path, str)
                or (not path.startswith(owner) and path not in allowed_worker_metadata)
                or ".." in Path(path).parts
                for path in changed_paths
            ):
                raise ValueError("worker paths escape the assigned ownership scope")
            source = workspace / item["owned_paths"][0]
            destination = ROOT / item["owned_paths"][0]
            if not source.is_dir():
                raise ValueError("worker source missing")
            reject_mutable_dependency_operations(item["id"])
            changed = worker_changed_paths(workspace, owner)
            if not changed:
                raise ValueError("worker made no owned-path changes")
            if any(not packet_path_covers(path, changed_paths, owner) for path in changed):
                raise ValueError("worker packet does not declare every changed owned path")
            records = [*source.rglob("*.json"), *source.rglob("*.yaml"), *source.rglob("*.yml")]
            if not records or not any(item["theorem_id"] in record.read_text(encoding="utf-8", errors="ignore") for record in records):
                raise ValueError("no target-identifying structured evidence record")
            dependency_ledger = None
            needs_dependency_ledger = item["phase"] == "proof" or (
                item["phase"] in {"validation", "release"} and bool(hard_parent_ids(item["theorem_id"]))
            )
            if needs_dependency_ledger and item["state"] == "[ ]":
                ledger_path = source / "dependency-reuse-ledger.json"
                expected_worker_graph = claim.get("theorem_dag_sha256")
                if not isinstance(expected_worker_graph, str):
                    raise ValueError("proof claim lacks its theorem DAG digest")
                dependency_ledger = validate_dependency_reuse_ledger(
                    ledger_path,
                    item["theorem_id"],
                    expected_observed_graph_sha256=expected_worker_graph,
                    expected_repository_revision=claim.get("base_revision"),
                    evidence_root=workspace,
                    authoritative_root=ROOT,
                )
                ledger_relative = f"{item['owned_paths'][0]}/dependency-reuse-ledger.json"
                if item["phase"] == "proof" and ledger_relative not in changed:
                    raise ValueError("proof handoff did not change the required dependency reuse ledger")
            if item["state"] == "[ ]":
                enforce_master_hard_edge_gate(
                    item,
                    dependency_ledger,
                    evidence_root=workspace,
                    authoritative_root=ROOT,
                    expected_base_revision=claim.get("base_revision"),
                    expected_commands=packet_commands,
                )
            merge_worker_changes(workspace, changed, owner=owner, transaction=claim_transaction)
            item["state"] = "[_]"
            item["attempts"] = int(item.get("attempts", 0)) + 1
            claim["status"] = "finished_integrated"
            claim["integrated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            accepted.append(item["id"])
            queue.append({"item_id": item["id"], "theorem_id": item["theorem_id"], "state": "[_]", "owned_paths": item["owned_paths"], "changed_paths": changed, "commands": packet.get("commands", []), "known_failures": packet.get("known_failures", [])})
            transaction.absorb(claim_transaction)
        except BaseException as exc:
            claim_transaction.rollback()
            if not isinstance(exc, (OSError, ValueError, json.JSONDecodeError)):
                raise
            claim["status"] = "rejected"
            claim["rejected_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            # Preserve the reason in the durable claim ledger as well as the
            # per-tick queue, which is deliberately overwritten on each run.
            claim["rejection_reason"] = str(exc)
            rejected.append({"item_id": str(claim.get("item_id")), "reason": str(exc)})
    for claim in blocked_ready:
        claim_transaction = FileTransaction(wal_parent=transaction)
        item = by_id.get(claim.get("item_id"))
        workspace = Path(str(claim.get("workspace", "")))
        try:
            if item is None:
                raise ValueError("blocked claim refers to unknown item")
            owner = item["owned_paths"][0] + "/"
            reject_mutable_dependency_operations(item["id"])
            changed = claim.get("blocked_snapshot_paths")
            snapshot_text = claim.get("blocked_snapshot")
            source_root = workspace
            if isinstance(snapshot_text, str):
                snapshot = validated_blocked_snapshot(item["id"], snapshot_text)
                manifest = snapshot / "manifest.json"
                if manifest.is_symlink():
                    raise ValueError("blocked snapshot manifest is a symlink")
                if not isinstance(changed, list) and manifest.exists():
                    changed = json.loads(manifest.read_text(encoding="utf-8")).get("changed_paths")
                source_root = snapshot
            if not isinstance(changed, list):
                changed = worker_changed_paths(workspace, owner)
            changed = validate_owned_relative_paths(changed, owner)
            allowed_suffixes = {".json", ".md", ".txt", ".yaml", ".yml", ".lean"}
            if any(Path(path).suffix not in allowed_suffixes for path in changed):
                raise ValueError("blocked handoff contains an unsupported artifact type")
            report_text = "\n".join(
                contained_regular_file(source_root, path, owner).read_text(encoding="utf-8", errors="replace")
                for path in changed
                if Path(path).suffix in {".md", ".txt"}
            )
            if item["theorem_id"] not in report_text or "blocked" not in report_text.lower():
                raise ValueError("blocked handoff lacks a target-specific blocker report")
            run(["git", "diff", "--check", "--", owner], cwd=workspace)
            if source_root == workspace:
                merge_worker_changes(workspace, changed, owner=owner, transaction=claim_transaction)
            else:
                for relative in changed:
                    source = contained_regular_file(source_root, relative, owner)
                    destination = contained_destination_path(ROOT, relative, owner)
                    if destination.exists():
                        raise ValueError(f"blocked report conflicts with existing master file: {relative}")
                    claim_transaction.snapshot(destination)
                    claim_transaction.ensure_parent(destination)
                    shutil.copy2(source, destination)
            claim["blocked_artifacts"] = changed
            claim["blocked_artifacts_merged_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            preserved_blockers.append(item["id"])
            transaction.absorb(claim_transaction)
        except BaseException as exc:
            claim_transaction.rollback()
            if not isinstance(exc, (OSError, ValueError, json.JSONDecodeError)):
                raise
            claim["blocked_artifact_rejection_reason"] = str(exc)
    if accepted or preserved_blockers:
        # Phase state and v2 completion-bucket order are one transaction.
        # Write both projections when state changed, but validate every copied
        # artifact batch, including blocked-only evidence, before persistence.
        if accepted:
            atomic_write(DAG, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        # The v2 inventory includes target-owned blocker artifacts as well as
        # phase-state projections, so every copied batch must regenerate it.
        run(["python3", "Docs/tools/generate_stage1_theorem_dag_v2.py"])
        theorem_dag_v2.cache_clear()
        run(["python3", "Docs/tools/check_stage1_theorem_dag_v2.py"])
        run(["python3", "Docs/tools/check_stage1_standard.py"])
        run(["python3", "scripts/stage1_target.py", "check"])
        if accepted:
            write_projection(data)
    save_claims(claims)
    integration_queue = {
        "queued": queue,
        "blocked_reports": preserved_blockers,
        "blocked_paths": sorted({
            path
            for claim in claims
            if claim.get("item_id") in set(preserved_blockers)
            and claim.get("blocked_artifacts_merged_at")
            for path in claim.get("blocked_artifacts", [])
            if isinstance(path, str)
        }),
        "rejected": rejected,
    }
    atomic_write(
        runtime_path("integration_queue.json"),
        json.dumps(integration_queue, ensure_ascii=False, indent=2) + "\n",
    )
    todo = write_todo(data, validate_dag(data), claims)
    checkpoint_paths = sorted({
        path
        for row in queue
        for path in row.get("changed_paths", [])
        if isinstance(path, str) and path != ".stage1-worker-selftest.json"
    } | set(integration_queue["blocked_paths"]))
    if accepted or preserved_blockers:
        checkpoint_files = sorted({
            *checkpoint_paths,
            *(
                path
                for path in (
                    "Docs/Stage1_Blueprint_rev-5.6.md",
                    "Docs/Stage1_Execution_DAG_rev-5.6.json",
                    "Docs/Stage1_Theorem_DAG_v2.json",
                )
                if path_differs_from_head(path)
            ),
        })
        # A blocked snapshot may contain historical files already identical to
        # HEAD. Bind and stage only the actual checkpoint delta.
        checkpoint_files = [path for path in checkpoint_files if path_differs_from_head(path)]
        manifest = {
            "schema_version": "stage1-pending-checkpoint/1.0",
            "base_revision": run(["git", "rev-parse", "HEAD"]).stdout.strip(),
            "state": "integrated_uncommitted",
            "paths": [
                {
                    "path": path,
                    "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest(),
                    "mode": "100755" if (ROOT / path).stat().st_mode & 0o111 else "100644",
                }
                for path in checkpoint_files
            ],
            "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
        atomic_write(
            runtime_path("pending_checkpoint.json"),
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        )
    print(
        f"integrate: worker-self-tested={len(accepted)} blocked-reports={len(preserved_blockers)} "
        f"rejected={len(rejected)} todo={todo.relative_to(ROOT)}"
    )
    return len(accepted) + len(preserved_blockers)


def worker_changed_paths(workspace: Path, owner: str) -> list[str]:
    """Return the worker's owned file changes and reject deletions.

    A later phase starts from a clone which already contains its target's intake
    dossier.  Copying the whole directory would therefore either reject valid
    work or overwrite independently changed master evidence.  The integration
    surface is instead the worker's actual Git delta, merged one owned file at
    a time with a base-content conflict check.
    """
    status = run(["git", "diff", "--name-status", "HEAD", "--", owner], cwd=workspace).stdout.splitlines()
    deleted = [line for line in status if line.startswith("D\t")]
    if deleted:
        raise ValueError(f"worker deletion is not an admissible handoff: {deleted}")
    tracked = run(["git", "diff", "--name-only", "HEAD", "--", owner], cwd=workspace).stdout.splitlines()
    untracked = run(["git", "ls-files", "--others", "--exclude-standard", "--", owner], cwd=workspace).stdout.splitlines()
    paths = sorted(set(tracked + untracked))
    if any(not path.startswith(owner) or ".." in Path(path).parts for path in paths):
        raise ValueError("worker Git delta escapes the assigned ownership scope")
    return paths


def reject_mutable_dependency_operations(item_id: str) -> None:
    """Fail closed when a worker's recorded execution mutates Lean dependencies."""
    log = RUNTIME / "logs" / f"{item_id}.out"
    if not log.exists():
        return
    text = log.read_text(encoding="utf-8", errors="replace")
    # A worker prompt and repository search may legitimately quote forbidden
    # commands. Inspect only the command that follows an `exec` event, stopping
    # at the event result, so prose never becomes a false rejection.
    commands = re.findall(r"(?ms)^exec\n(.*?)(?=\n(?:succeeded|failed) in |\nexec\n|\Z)", text)
    forbidden = (
        r"(?:^|[;&|]\s*|(?:/bin/)?bash\s+-lc\s+['\"])lake\s+(?:update|build)\b",
        r"(?:^|[;&|]\s*|(?:/bin/)?bash\s+-lc\s+['\"])git\s+(?:clone|fetch|pull)\b.*?\.lake",
    )
    if any(re.search(pattern, command) for command in commands for pattern in forbidden):
        raise ValueError("worker ran a mutable Lean dependency operation; no pinned receipt is admissible")


def packet_path_covers(path: str, declared: list[Any], owner: str) -> bool:
    """Allow a packet to name an exact file or the complete owned directory."""
    for entry in declared:
        if not isinstance(entry, str) or entry == ".stage1-worker-selftest.json":
            continue
        normalized = entry.rstrip("/")
        if normalized == owner.rstrip("/") or path == normalized:
            return True
    return False


def validate_owned_relative_paths(paths: Any, owner: str) -> list[str]:
    """Reject absolute, traversing, duplicate, or cross-owner handoff paths."""
    if not isinstance(paths, list) or not paths:
        raise ValueError("blocked worker made no owned-path report")
    normalized_owner = owner.rstrip("/")
    accepted: list[str] = []
    for value in paths:
        if not isinstance(value, str) or not value:
            raise ValueError("blocked handoff path must be a nonempty string")
        path = Path(value)
        if (
            path.is_absolute()
            or ".." in path.parts
            or path.as_posix() != value
            or not value.startswith(normalized_owner + "/")
        ):
            raise ValueError("blocked handoff path escapes the assigned ownership scope")
        accepted.append(value)
    if len(accepted) != len(set(accepted)):
        raise ValueError("blocked handoff contains duplicate paths")
    return accepted


def contained_regular_file(root: Path, relative: str, owner: str) -> Path:
    """Resolve one handoff source without permitting symlink or root escape."""
    validate_owned_relative_paths([relative], owner)
    root_resolved = root.resolve()
    path = root / relative
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"blocked handoff path is not a regular file: {relative}")
    resolved = path.resolve()
    owner_root = (root / owner.rstrip("/")).resolve()
    if not resolved.is_relative_to(root_resolved) or not resolved.is_relative_to(owner_root):
        raise ValueError("blocked handoff source escapes through a symlink")
    return resolved


def contained_destination_path(root: Path, relative: str, owner: str) -> Path:
    """Resolve an owned destination without following a symlink outside root."""
    validate_owned_relative_paths([relative], owner)
    root_resolved = root.resolve()
    owner_path = root / owner.rstrip("/")
    if owner_path.is_symlink():
        raise ValueError("handoff owner path is a symlink")
    owner_resolved = owner_path.resolve()
    destination = root / relative
    if destination.is_symlink():
        raise ValueError("handoff destination is a symlink")
    resolved = destination.resolve()
    if not owner_resolved.is_relative_to(root_resolved) or not resolved.is_relative_to(owner_resolved):
        raise ValueError("handoff destination escapes the assigned ownership scope")
    return destination


def git_blob_oid(workspace: Path, revision_path: str) -> str | None:
    result = run(["git", "rev-parse", f"HEAD:{revision_path}"], cwd=workspace, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def path_differs_from_head(relative: str) -> bool:
    """Return whether one regular worktree file differs from the HEAD blob."""
    path = ROOT / relative
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"checkpoint path is missing or unsafe: {relative}")
    head_oid = run(["git", "rev-parse", f"HEAD:{relative}"], check=False)
    return head_oid.returncode != 0 or head_oid.stdout.strip() != file_oid(path)


def file_oid(path: Path) -> str:
    return run(["git", "hash-object", str(path)]).stdout.strip()


def git_tree_mode(revision_path: str, *, cwd: Path | None = None) -> str | None:
    result = run(["git", "ls-tree", revision_path.split(":", 1)[0], "--", revision_path.split(":", 1)[1]], cwd=cwd, check=False)
    if result.returncode or not result.stdout.strip():
        return None
    return result.stdout.split(None, 1)[0]


def merge_worker_changes(
    workspace: Path,
    changed: list[str],
    *,
    owner: str | None = None,
    transaction: FileTransaction | None = None,
) -> None:
    """Merge an isolated worker delta without overwriting a changed master file."""
    if owner is not None:
        changed = validate_owned_relative_paths(changed, owner)
    plan: list[tuple[Path, Path]] = []
    for relative in changed:
        source = (
            contained_regular_file(workspace, relative, owner)
            if owner is not None
            else workspace / relative
        )
        destination = (
            contained_destination_path(ROOT, relative, owner)
            if owner is not None
            else ROOT / relative
        )
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"worker changed path is not a regular file: {relative}")
        if destination.exists():
            base_oid = git_blob_oid(workspace, relative)
            if base_oid is None:
                raise ValueError(f"new worker file conflicts with existing master file: {relative}")
            if file_oid(destination) != base_oid and file_oid(destination) != file_oid(source):
                raise ValueError(f"master file changed since worker base: {relative}")
        plan.append((source, destination))
    for source, destination in plan:
        if transaction is not None:
            transaction.snapshot(destination)
            transaction.ensure_parent(destination)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def checkpoint_commit_error(
    commit_revision: str,
    base_revision: str,
    expected_hashes: dict[str, str],
    expected_modes: dict[str, str],
) -> str | None:
    """Return why a checkpoint commit is not the exact manifest child."""
    ancestry = run(
        ["git", "rev-list", "--parents", "-n", "1", commit_revision],
        check=False,
    )
    parents = ancestry.stdout.split() if ancestry.returncode == 0 else []
    if len(parents) != 2 or parents[0] != commit_revision or parents[1] != base_revision:
        return "commit is not the single direct child of the checkpoint base"
    changed = run(
        ["git", "diff", "--name-only", base_revision, commit_revision, "--"],
        check=False,
    )
    if changed.returncode or set(changed.stdout.splitlines()) != set(expected_hashes):
        return "commit paths do not exactly match the verified manifest"
    for path, digest in expected_hashes.items():
        if git_tree_mode(f"{commit_revision}:{path}") != expected_modes[path]:
            return f"committed file mode differs from the verified manifest: {path}"
        try:
            committed = git_object_bytes(f"{commit_revision}:{path}")
        except SystemExit:
            return f"commit is missing manifest path: {path}"
        if hashlib.sha256(committed).hexdigest() != digest:
            return f"committed bytes differ from the verified manifest: {path}"
    return None


def finish_checkpoint_push(
    pending_path: Path,
    base_revision: str,
    commit_revision: str,
) -> None:
    """Push once, or finish an already-pushed checkpoint idempotently."""
    run(["git", "fetch", "--prune", "origin"])
    upstream = run(["git", "rev-parse", "@{u}"]).stdout.strip()
    if upstream != commit_revision:
        if upstream != base_revision:
            fail("checkpoint upstream moved away from the checkpoint base")
        run([
            "git", "push",
            f"--force-with-lease=refs/heads/main:{base_revision}",
            "origin", f"{commit_revision}:refs/heads/main",
        ])
        run(["git", "fetch", "--prune", "origin"])
        upstream = run(["git", "rev-parse", "@{u}"]).stdout.strip()
    if upstream != commit_revision:
        fail("checkpoint push did not update the upstream head")
    durable_unlink(pending_path)


def checkpoint_integration() -> None:
    """Commit/push exactly one content-bound, retryable integration manifest."""
    pending_path = runtime_path("pending_checkpoint.json")
    pending = read_json(pending_path)
    if pending.get("schema_version") != "stage1-pending-checkpoint/1.0":
        fail("pending checkpoint manifest has an unsupported schema")
    rows = pending.get("paths")
    if not isinstance(rows, list) or not rows:
        fail("pending checkpoint manifest has no verified paths")
    selected: list[str] = []
    expected_hashes: dict[str, str] = {}
    expected_modes: dict[str, str] = {}
    allowed_generated = {
        "Docs/Stage1_Blueprint_rev-5.6.md",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "Docs/Stage1_Theorem_DAG_v2.json",
    }
    for row in rows:
        if not isinstance(row, dict) or set(row) not in ({"path", "sha256"}, {"path", "sha256", "mode"}):
            fail("pending checkpoint path record is malformed")
        path, digest, mode = row.get("path"), row.get("sha256"), row.get("mode", "100644")
        if (
            not isinstance(path, str)
            or not isinstance(digest, str)
            or re.fullmatch(r"[0-9a-f]{64}", digest) is None
            or mode not in {"100644", "100755"}
            or Path(path).is_absolute()
            or ".." in Path(path).parts
            or (path not in allowed_generated and not path.startswith("Stage1_Instances/"))
            or path in expected_hashes
        ):
            fail("pending checkpoint contains an invalid or duplicate path")
        target = ROOT / path
        if target.is_symlink() or not target.is_file():
            fail(f"pending checkpoint path is missing or unsafe: {path}")
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            fail(f"pending checkpoint source changed after validation: {path}")
        selected.append(path)
        expected_hashes[path] = digest
        expected_modes[path] = mode

    base_revision = pending.get("base_revision")
    if not isinstance(base_revision, str) or re.fullmatch(r"[0-9a-f]{40,64}", base_revision) is None:
        fail("pending checkpoint base revision is malformed")
    head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    state = pending.get("state")
    commit_revision = pending.get("commit_revision")
    if state == "committed_unpushed":
        if not isinstance(commit_revision, str) or head != commit_revision:
            fail("pending checkpoint commit does not match local HEAD")
        mismatch = checkpoint_commit_error(commit_revision, base_revision, expected_hashes, expected_modes)
        if mismatch is not None:
            fail(f"pending checkpoint commit is not content-bound: {mismatch}")
        finish_checkpoint_push(pending_path, base_revision, commit_revision)
        return
    if state != "integrated_uncommitted":
        fail("pending checkpoint has an unsupported state")
    if head != base_revision:
        mismatch = checkpoint_commit_error(head, base_revision, expected_hashes, expected_modes)
        if mismatch is not None:
            fail(f"pending checkpoint recovery commit is not content-bound: {mismatch}")
        pending["state"] = "committed_unpushed"
        pending["commit_revision"] = head
        atomic_write(pending_path, json.dumps(pending, ensure_ascii=False, indent=2) + "\n")
        finish_checkpoint_push(pending_path, base_revision, head)
        return
    if head != base_revision:
        fail("pending checkpoint base revision does not match local HEAD")

    run(["git", "add", "--", *selected])
    staged = run(["git", "diff", "--cached", "--name-only"]).stdout.splitlines()
    if set(staged) != set(selected):
        fail("checkpoint index does not exactly match the verified manifest")
    for path, digest in expected_hashes.items():
        if hashlib.sha256(git_object_bytes(f":{path}")).hexdigest() != digest:
            fail(f"checkpoint staged bytes differ from the validated manifest: {path}")
        staged_mode = run(["git", "ls-files", "-s", "--", path]).stdout.split(None, 1)[0]
        if staged_mode != expected_modes[path]:
            fail(f"checkpoint staged file mode differs from the validated manifest: {path}")
        target = ROOT / path
        if target.is_symlink() or not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            fail(f"checkpoint worktree changed after staging: {path}")
    run(["git", "commit", "-m", "Integrate Stage1 worker evidence batch"])
    commit_revision = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    mismatch = checkpoint_commit_error(commit_revision, base_revision, expected_hashes, expected_modes)
    if mismatch is not None:
        fail(f"new checkpoint commit is not content-bound: {mismatch}")
    for path, digest in expected_hashes.items():
        target = ROOT / path
        if target.is_symlink() or not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            fail(f"checkpoint worktree changed during commit: {path}")
    pending["state"] = "committed_unpushed"
    pending["commit_revision"] = commit_revision
    atomic_write(pending_path, json.dumps(pending, ensure_ascii=False, indent=2) + "\n")
    finish_checkpoint_push(pending_path, base_revision, commit_revision)


def launch(max_workers: int) -> None:
    if max_workers < 0 or max_workers > MAX_WORKERS:
        fail(f"--workers must be in 0..{MAX_WORKERS}")
    # A tick begins clean/synced, then drains handoffs, checkpoints them, and only then
    # refills worker capacity. This preserves the worker/master dual cursor across cron ticks.
    recover_integration_wal()
    pending = runtime_path("pending_checkpoint.json")
    if pending.exists():
        checkpoint_sync_guard()
        checkpoint_integration()
    else:
        sync_guard()
        integrated = integrate(max_workers)
        if integrated:
            checkpoint_integration()
    data, ordered = load_dag()
    claims = refresh_claims(ordered)
    claims = enforce_worker_cap(claims, max_workers)
    space_guard(claims)
    live = [claim for claim in claims if claim.get("status") in {"live", "draining"}]
    if any(claim.get("status") == "quarantined" for claim in claims):
        fail("claim ledger contains quarantined runtime identities; refuse worker refill")
    # Finished handoffs retain their clones until integration, but they do not
    # consume live-worker capacity. Their occupied slot numbers are skipped
    # while fresh, otherwise-unused slot numbers refill the requested lanes.
    slot_reservations = [
        claim
        for claim in claims
        if claim.get("status") in {"live", "finished", "preparing", "launch_failed", "draining", "quarantined"}
    ]
    # A slot owns its clone.  Never derive a slot from the count of live claims:
    # claims can finish out of order, leaving holes, and reusing an occupied slot
    # would make two Codex processes write the same worker checkout/manifest.
    occupied_slots = {
        claim.get("slot")
        for claim in slot_reservations
        if isinstance(claim.get("slot"), int) and claim["slot"] >= 1
    }
    # On a downscale, existing live workers are grandfathered until they
    # finish. Pending handoffs remain reserved only at the filesystem level.
    capacity = max(0, max_workers - len(live))
    available_slots = [slot for slot in range(1, max_workers + len(slot_reservations) + 1) if slot not in occupied_slots][:capacity]
    if capacity <= 0:
        print(f"tick: saturated ({len(live)} live/{max_workers} slots, {len(slot_reservations) - len(live)} handoff pending)")
        write_todo(data, ordered, claims)
        return
    # A blocked worker is a durable negative receipt, not a lease forever.
    # Keep only live workers and pending handoffs reserved so a three-minute
    # refill can retry eligible work and maintain the operator's lane target.
    claimed_ids = {
        claim.get("item_id")
        for claim in claims
        if claim.get("status") in {"live", "finished", "preparing", "launch_failed", "draining", "quarantined"}
    }
    states_by_id = {item["id"]: item["state"] for item in ordered}
    started_targets = {
        item["theorem_id"]
        for item in ordered
        if item["state"] in {"[_]", "[x]"}
    }
    # Phase artifacts are allowed to advance from a self-tested predecessor;
    # only master acceptance remains strictly `[x]`-ordered.  This lets
    # statement/anchor work begin from the concrete intake dossier while the
    # master reviews the preceding receipt, without treating `[_]` as closure.
    candidates = [
        item
        for item in ordered
        if item["state"] == "[ ]"
        and item["id"] not in claimed_ids
        and (not STARTED_TARGETS_ONLY or item["theorem_id"] in started_targets)
        and all(states_by_id.get(dependency) in {"[_]", "[x]"} for dependency in item["depends_on"])
        # Hard theorem parents block only accepted closure.  Workers may still
        # prepare a dependent proof provisionally after inspecting all parents.
    ]
    # Start a bounded *depth-first* pipeline. Once a target has a self-tested
    # predecessor, advancing its deepest ready phase is more useful than
    # launching another unrelated statement: it permits real statement ->
    # anchor -> obligation -> proof -> validation -> release progress rather
    # than filling all 1546 targets one phase at a time. Intake remains the
    # deterministic fallback when no successor phase is ready.
    _, theorem_nodes = theorem_dag_v2()
    candidates.sort(
        key=lambda item: (
            0 if item["depends_on"] else 1,
            -item["layer"],
            theorem_nodes[item["theorem_id"]]["v2_execution_rank"],
            item["id"],
        )
    )
    selected = candidates[:capacity]
    if not selected:
        print("tick: no unclaimed work")
        write_todo(data, ordered, claims)
        return
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    claim_graph_sha256 = graph_sha256()
    base_revision = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    reservations: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for slot, item in zip(available_slots, selected):
        workspace = RUNTIME / "workers" / f"slot{slot}"
        prompt = RUNTIME / "prompts" / f"{item['id']}.txt"
        output = RUNTIME / "logs" / f"{item['id']}.out"
        session = f"stage1r56-{slot}-{theorem_nodes[item['theorem_id']]['v2_execution_rank']:04d}"
        claim = {
            "item_id": item["id"], "theorem_id": item["theorem_id"], "depends_on": item["depends_on"],
            "owned_paths": item["owned_paths"], "session": session, "slot": slot, "workspace": str(workspace),
            "status": "preparing", "pid": None, "claimed_at": timestamp,
            "retry_count": sum(1 for claim in claims if claim.get("item_id") == item["id"]),
            "base_revision": base_revision, "output_log": str(output),
            "runtime_config": {
                "model": CODEX_MODEL,
                "reasoning_effort": CODEX_REASONING_EFFORT,
                "service_tier": CODEX_SERVICE_TIER,
            },
            "theorem_dag_sha256": claim_graph_sha256,
            "dependency_context_sha256": theorem_nodes[item["theorem_id"]].get("dependency_context_sha256"),
        }
        claims.append(claim)
        reservations.append((claim, item))
    # Persist all leases before creating or replacing a clone/session. A crash
    # can now leave only a recoverable preparing row, never an unowned worker.
    save_claims(claims)
    launched = 0
    for claim, item in reservations:
        workspace = Path(claim["workspace"])
        prompt = RUNTIME / "prompts" / f"{item['id']}.txt"
        output = Path(claim["output_log"])
        session = str(claim["session"])
        try:
            prepare_workspace(int(claim["slot"]))
            prompt.parent.mkdir(parents=True, exist_ok=True)
            output.parent.mkdir(parents=True, exist_ok=True)
            atomic_write(prompt, task_prompt(item, workspace))
            run(["tmux", "kill-session", "-t", session], check=False)
            command = worker_command(workspace, prompt, output)
            run(["tmux", "new-session", "-d", "-s", session, "bash", "-lc", command])
            pid_result = run(["tmux", "list-panes", "-t", session, "-F", "#{pane_pid}"], check=False)
            pid_text = pid_result.stdout.strip()
            claim["pid"] = int(pid_text) if pid_text.isdigit() else None
            claim["status"] = "live"
            claim["launched_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            launched += 1
        except BaseException as exc:
            # Persist a failed reservation before propagating. On the next
            # tick it cannot be mistaken for a free slot or live worker.
            claim["status"] = "launch_failed"
            claim["launch_failed_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["launch_error"] = str(exc)
            save_claims(claims)
            raise
        save_claims(claims)
    todo = write_todo(data, ordered, claims)
    print(f"tick: launched {launched} worker(s), live={len(live) + launched}/{max_workers}, todo={todo.relative_to(ROOT)}")


def restart_live_workers(max_workers: int) -> None:
    """Restart live claims in place after a scheduler runtime-policy change.

    A worker clone can contain useful, uncommitted progress.  Reusing the same
    clone keeps that progress available to the restarted Codex process while
    changing only the runtime configuration.  Finished handoffs are left for
    the normal integration path and are never restarted.
    """
    if max_workers < 0 or max_workers > MAX_WORKERS:
        fail(f"--workers must be in 0..{MAX_WORKERS}")
    sync_guard()
    data, ordered = load_dag()
    claims = refresh_claims(ordered)
    by_id = {item["id"]: item for item in ordered}
    live = [claim for claim in claims if claim.get("status") == "live" and int(claim.get("slot", 0)) <= max_workers]
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    restarted = 0
    for claim in live:
        item = by_id.get(claim.get("item_id"))
        workspace = Path(str(claim.get("workspace", "")))
        slot = claim.get("slot")
        session = claim.get("session")
        if item is None or not isinstance(slot, int) or not workspace.is_dir() or not isinstance(session, str):
            fail(f"cannot safely restart malformed live claim: {claim.get('item_id')}")
        run(["tmux", "kill-session", "-t", session], check=False)
        prompt = RUNTIME / "prompts" / f"{item['id']}.txt"
        output = RUNTIME / "logs" / f"{item['id']}.out"
        atomic_write(prompt, task_prompt(item, workspace))
        command = worker_command(workspace, prompt, output)
        run(["tmux", "new-session", "-d", "-s", session, "bash", "-lc", command])
        pid_result = run(["tmux", "list-panes", "-t", session, "-F", "#{pane_pid}"], check=False)
        pid_text = pid_result.stdout.strip()
        claim["pid"] = int(pid_text) if pid_text.isdigit() else None
        claim["restarted_at"] = timestamp
        claim["runtime_config"] = {
            "model": CODEX_MODEL,
            "reasoning_effort": CODEX_REASONING_EFFORT,
            "service_tier": CODEX_SERVICE_TIER,
        }
        claim["theorem_dag_sha256"] = graph_sha256()
        _, theorem_nodes = theorem_dag_v2()
        claim["dependency_context_sha256"] = theorem_nodes[item["theorem_id"]].get("dependency_context_sha256")
        restarted += 1
    save_claims(claims)
    write_todo(data, ordered, claims)
    print(f"restart: restarted {restarted} live worker(s) with service_tier={CODEX_SERVICE_TIER}")


def cleanup() -> None:
    data, ordered = load_dag()
    claims = refresh_claims(ordered)
    counts = Counter(item["state"] for item in ordered)
    todo = DOCS / f"todos_{dt.date.today():%Y%m%d}.md"
    unfinished_zero = todo.exists() and "Unfinished: 0" in todo.read_text(encoding="utf-8")
    if counts["[ ]"] or counts["[_]"] or claims or not unfinished_zero:
        fail("cleanup refused: unfinished work, active/pending claims, or stale todo remains")
    cron = run(["crontab", "-l"], check=False)
    lines = [line for line in cron.stdout.splitlines() if "stage1_execution_cron.py" not in line]
    subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", text=True, check=True)
    atomic_write(runtime_path("cleanup.json"), json.dumps({"state": "completed", "at": dt.datetime.now(dt.timezone.utc).isoformat()}, indent=2) + "\n")
    print("cleanup: removed Stage1 execution cron entry")


def install(schedule: str) -> None:
    if not re.fullmatch(r"[^\n]+", schedule):
        fail("schedule must be one crontab line prefix")
    command = f"{schedule} cd {ROOT} && {ROOT / 'scripts' / 'stage1_execution_cron.py'} --tick --workers {DEFAULT_WORKERS} --limit {DEFAULT_INTEGRATION_LIMIT} >> {RUNTIME / 'keepalive.log'} 2>&1 # stage1_execution_cron.py"
    current = run(["crontab", "-l"], check=False).stdout.splitlines()
    current = [line for line in current if "stage1_execution_cron.py" not in line]
    subprocess.run(["crontab", "-"], input="\n".join(current + [command]) + "\n", text=True, check=True)
    print("install: cron entry installed")


def main() -> None:
    # A refill can take longer than its three-minute cadence. Serialize all
    # scheduler invocations so overlapping ticks cannot allocate the same slot
    # or orphan an unrecorded tmux worker.
    validate_runtime_root()
    lock = runtime_path("scheduler.lock").open("w", encoding="utf-8")
    try:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("scheduler: another invocation is active; skipping overlapping run")
        lock.close()
        return
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--bootstrap", action="store_true", help="generate the typed 1546-target execution DAG and blueprint appendix")
    modes.add_argument("--validate-only", action="store_true", help="validate DAG, state, budgets, and todo without syncing or spawning workers")
    modes.add_argument("--integrate", action="store_true", help="verify completed worker handoffs and advance them to worker-self-tested")
    modes.add_argument("--tick", action="store_true", help="sync, refill the tmux Codex worker lanes, and refresh todo")
    modes.add_argument("--cleanup", action="store_true", help="remove the cron entry only after every completion gate is true")
    modes.add_argument("--restart-live", action="store_true", help="restart live workers in place using the current scheduler runtime policy")
    modes.add_argument("--install", action="store_true", help="install a bounded scheduler cron entry")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help=f"concurrent-worker refill budget (0..{MAX_WORKERS}; default {DEFAULT_WORKERS})")
    parser.add_argument("--limit", type=int, default=DEFAULT_INTEGRATION_LIMIT, help=f"handoff integration budget (0..{MAX_WORKERS}; default {DEFAULT_INTEGRATION_LIMIT})")
    parser.add_argument("--schedule", default="*/3 * * * *", help="crontab schedule used by --install")
    args = parser.parse_args()
    if args.bootstrap:
        bootstrap()
    elif args.validate_only:
        validate_only()
    elif args.integrate:
        integrate(args.limit)
    elif args.tick:
        launch(args.workers)
    elif args.cleanup:
        cleanup()
    elif args.restart_live:
        restart_live_workers(args.workers)
    else:
        install(args.schedule)
    lock.close()


if __name__ == "__main__":
    main()
