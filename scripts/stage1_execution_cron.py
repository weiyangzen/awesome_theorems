#!/usr/bin/env python3
"""Run the Stage1 v2 Lean 4 execution queue safely.

``Docs/Stage1_Blueprint_v2.md`` is the single writable requirements and task-
state authority.  Its generated checklist is projected into the typed
``Docs/Stage1_Execution_DAG_rev-5.6.json`` and the daily todo snapshot; neither
projection may feed state back into the blueprint.

This program owns its app-server state below `.cron/stage1-v2-app-server/`,
which is gitignored.  The historical `.cron/stage1-rev56/` runtime is retained
as read-only audit evidence.  A worker never writes an accepted state: it
produces a self-test manifest and its isolated clone is queued for the
integration owner.
"""

from __future__ import annotations

import argparse
import base64
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
import stat
import subprocess
import sys
import tempfile
import time
from collections import Counter, deque
from typing import Any, NoReturn

try:
    import stage1_acceptance_evidence as acceptance_evidence
except ModuleNotFoundError:  # Support importlib-based focused tests from repo root.
    import importlib.util

    _EVIDENCE_PATH = Path(__file__).with_name("stage1_acceptance_evidence.py")
    _EVIDENCE_SPEC = importlib.util.spec_from_file_location(
        "stage1_acceptance_evidence", _EVIDENCE_PATH
    )
    if _EVIDENCE_SPEC is None or _EVIDENCE_SPEC.loader is None:
        raise
    acceptance_evidence = importlib.util.module_from_spec(_EVIDENCE_SPEC)
    sys.modules[_EVIDENCE_SPEC.name] = acceptance_evidence
    _EVIDENCE_SPEC.loader.exec_module(acceptance_evidence)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "Docs"
BLUEPRINT = DOCS / "Stage1_Blueprint_v2.md"
ASSURANCE_BLUEPRINT = DOCS / "Stage1_Blueprint_rev-5.6.md"
TARGETS = DOCS / "Stage1_Targets_rev-5.6.json"
DAG = DOCS / "Stage1_Execution_DAG_rev-5.6.json"
THEOREM_DAG_V2 = DOCS / "Stage1_Theorem_DAG_v2.json"
PHASE_ACCEPTANCE_CONTRACTS = DOCS / "Stage1_Phase_Acceptance_Contracts.json"
PHASE_ACCEPTANCE_CONTRACT_SHA256 = (
    "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
)
LEGACY_RUNTIME = ROOT / ".cron" / "stage1-rev56"
RUNTIME = ROOT / ".cron" / "stage1-v2-app-server"
CHECKLIST_BEGIN = "<!-- STAGE1-EXECUTION-CHECKLIST:BEGIN -->"
CHECKLIST_END = "<!-- STAGE1-EXECUTION-CHECKLIST:END -->"
CHECKLIST_ROW_RE = re.compile(
    r"^- (?P<state>\[[_x ]\]) `(?P<id>S56-M-\d{4}-(?:INTAKE|STATEMENT|ANCHOR_AUDIT|OBLIGATION_TREE|PROOF|VALIDATION|RELEASE))`"
    r" / `(?P<theorem>THM-M-\d{4})` / `(?P<phase>intake|statement|anchor_audit|obligation_tree|proof|validation|release)`"
    r": (?P<deliverable>.+?) \{attempts=(?P<attempts>\d+)\}$",
    re.MULTILINE,
)
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
EXECUTION_CONTRACT = {
    "claim_order": ["v2_execution_rank", "phase_layer", "phase_item_id"],
    "proof_parent_inspection": {
        "scope": ["direct_hard_parents", "transitive_hard_ancestors"],
        "order": "ascending_v2_execution_rank_parent_before_child",
        "complete_closure_required": True,
    },
    "accepted_reuse_relationships": ["exact", "checked_transport"],
    "checked_transport_requires": [
        "content_bound_provider_source",
        "provider_and_consumer_statement_fingerprints",
        "consumer_owned_import_or_wrapper",
        "consumer_validation_receipt",
    ],
    "provider_checkbox_state_is_observation_only": True,
    "provider_acceptance_inherited": False,
    "consumer_acceptance_required": True,
}
# App-server workers are deliberately bounded to one 50-thread cohort.  The
# integration budget is independent because a refill may drain older evidence.
MAX_WORKERS = 50
DEFAULT_WORKERS = 50
MAX_INTEGRATION_LIMIT = 80
DEFAULT_INTEGRATION_LIMIT = 20
MAX_SLOT_ID = 1546 * len(PHASES)
CLAIM_ID_RE = re.compile(r"[0-9]{8}T[0-9]{6}Z-[0-9a-f]{12}")
GOAL_HANDSHAKE_TIMEOUT_SECONDS = 30.0
GOAL_HANDSHAKE_POLL_SECONDS = 0.1
GOAL_HANDSHAKE_RECOVERY_GRACE_SECONDS = 120.0
STARTED_TARGETS_ONLY = False
CODEX_MODEL = "gpt-5.6-sol"
CODEX_REASONING_EFFORT = "ultra"
CODEX_SERVICE_TIER = "default"
REQUIRED_RUNTIME_CONFIG = {
    "model": "gpt-5.6-sol",
    "reasoning_effort": "ultra",
    "service_tier": "default",
}
IMPLEMENTATION_LANE = "implementation"
REVIEW_LANE = "review"
LANES = {IMPLEMENTATION_LANE, REVIEW_LANE}
REVIEW_BINDING_SCHEMA = "stage1-app-server-review-binding/1.0"
REVIEW_OUTPUT_SCHEMA = "stage1-master-review-output/1.0"
ROLE_MAP_SCHEMA = "stage1-phase-artifact-role-map/1.0"
MASTER_ACCEPTANCE_RECEIPT_SCHEMA = "stage1-master-phase-acceptance/1.0"
WORKER_PROVENANCE_SCHEMA = "stage1-worker-review-provenance/1.0"
REVIEW_INPUT_SCHEMA = "stage1-scheduler-review-input/1.0"
LEGACY_REVALIDATION_PLAN_SCHEMA = "stage1-legacy-revalidation-plan/1.0"
LEGACY_REVALIDATION_LANE_SCHEMA = "stage1-legacy-revalidation-lane/1.0"
LEGACY_REVALIDATION_PLAN_BINDING_SCHEMA = (
    "stage1-legacy-revalidation-plan-binding/1.0"
)
LEGACY_REVALIDATION_INTEGRATION_SCHEMA = (
    "stage1-legacy-revalidation-integration/1.0"
)
LEGACY_REVALIDATION_REQUIRED_STEPS = [
    "fresh_self_test",
    "new_contract_receipt",
    "new_provenance",
    "independent_review",
    "master_replay",
]
LEGACY_INVENTORY_CLASSIFICATIONS = {
    "missing_receipt",
    "legacy_receipt",
    "phase_mismatch",
    "missing_or_ambiguous_role",
    "validator_base_mismatch",
    "validator_stdout_mismatch",
    "sandbox_incompatible",
}
LEGACY_REVALIDATION_CLAIM_FIELDS = {
    "legacy_revalidation_lane",
    "legacy_revalidation_lane_sha256",
    "legacy_revalidation_plan_sha256",
    "legacy_revalidation_plan_file_sha256",
    "legacy_revalidation_plan_binding",
    "legacy_revalidation_plan_binding_sha256",
}
LEGACY_REVALIDATION_INTEGRATION_FIELDS = {
    "legacy_revalidation_integration",
    "legacy_revalidation_integration_sha256",
}
REPLAY_TIMEOUT_SECONDS = 3600.0
WORKER_VERDICTS = {
    "accepted", "accepted_audit_only", "no_state_change", "blocked", "rejected",
}
REVIEW_VERDICTS = {"phase_accepted", "repair_required", "rejected"}
REVIEW_OUTPUT_FIELDS = {
    "schema_version", "claim_id", "item_id", "theorem_id", "phase",
    "worker_verdict", "review_verdict", "audit_complete", "theorem_complete",
    "root_state", "first_failed_gate", "retry_condition", "status_boundary",
    "artifact_findings", "reviewed_artifact_sha256s",
    "validator_recipe_sha256s",
}
REQUIRED_APP_SERVER_ARGV = [
    "app-server",
    "--stdio",
    "--enable",
    "goals",
    "--disable",
    "code_mode",
    "--disable",
    "code_mode_host",
    "--disable",
    "code_mode_only",
]
REQUIRED_IMPLEMENTATION_SANDBOX_CONTRACT = {
    "type": "workspaceWrite",
    "writableRoots": [],
    "networkAccess": False,
    "excludeTmpdirEnvVar": False,
    "excludeSlashTmp": False,
}
REQUIRED_REVIEW_SANDBOX_CONTRACT = {"type": "readOnly", "networkAccess": False}
# Compatibility name retained for implementation-lane callers and tests.
REQUIRED_SANDBOX_CONTRACT = REQUIRED_IMPLEMENTATION_SANDBOX_CONTRACT
PAUSE_FILE = RUNTIME / "PAUSED"
LEGACY_PAUSE_FILE = LEGACY_RUNTIME / "PAUSED"
APP_SERVER_CLIENT = ROOT / "scripts" / "stage1_app_server_client.py"
PROC_ROOT = Path("/proc")
RUNTIME_PROTOCOL = "codex-app-server-jsonl"
LEGACY_RUNTIME_PROTOCOL = "tmux-codex-exec"


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
    for name in (
        "workers", "prompts", "logs", "goals", "app-server", "blocked-reports",
        "worker-handoffs", "role-maps", "review-inputs", "review-bindings",
        "review-workspaces", "worker-provenance", "review-manifests",
        "replay-results", "semantic-decisions",
    ):
        path = RUNTIME / name
        if path.is_symlink() or (path.exists() and (not path.is_dir() or not path.resolve().is_relative_to(root_resolved))):
            fail(f"scheduler runtime subdirectory is unsafe: {name}")


def pause_markers() -> tuple[Path, ...]:
    """Return the current marker plus the retired marker during migration."""
    current = RUNTIME / "PAUSED"
    legacy = LEGACY_PAUSE_FILE
    # Focused tests and callers may override PAUSE_FILE to isolate the stop
    # boundary. In that case the explicit override is the complete boundary.
    if PAUSE_FILE != current:
        return (PAUSE_FILE,)
    return (current,) if current == legacy else (current, legacy)


def execution_is_paused() -> bool:
    return any(path.exists() for path in pause_markers())


def migrate_pause_marker() -> bool:
    """Copy a retired stop intent into current runtime without unfreezing it."""
    if PAUSE_FILE != RUNTIME / "PAUSED" or not LEGACY_PAUSE_FILE.exists():
        return False
    if PAUSE_FILE.exists():
        return False
    try:
        marker = LEGACY_PAUSE_FILE.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        fail(f"legacy PAUSED marker is unreadable: {exc}")
    PAUSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(PAUSE_FILE, marker)
    return True


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
    runtime_relative = RUNTIME.relative_to(ROOT).as_posix()
    allowed_runtime = {
        f"{runtime_relative}/claims.json",
        f"{runtime_relative}/integration_queue.json",
        f"{runtime_relative}/pending_checkpoint.json",
    }

    def allowed_runtime_evidence(relative: str) -> bool:
        """Admit only the two canonical per-review acceptance byproducts."""
        return any(
            re.fullmatch(
                rf"{re.escape(runtime_relative)}/{directory}/"
                rf"{CLAIM_ID_RE.pattern}\.json",
                relative,
            )
            is not None
            for directory in ("replay-results", "semantic-decisions")
        )

    def recovery_target(relative: str, *, directory: bool = False) -> Path:
        path = Path(relative)
        canonical_runtime_directory = relative in {
            f"{runtime_relative}/replay-results",
            f"{runtime_relative}/semantic-decisions",
        }
        canonical_receipt_directory = re.fullmatch(
            r"Stage1_Instances(?:/THM-M-[0-9]{4}"
            r"(?:/master-acceptance"
            r"(?:/(?:intake|statement|anchor_audit|obligation_tree|proof|validation|release))?"
            r")?"
            r")?",
            relative,
        ) is not None
        canonical_instance_file = re.fullmatch(
            r"Stage1_Instances/THM-M-[0-9]{4}/.+",
            relative,
        ) is not None
        reserved_receipt_file = "/master-acceptance/" in relative
        canonical_receipt_file = re.fullmatch(
            r"Stage1_Instances/THM-M-[0-9]{4}/master-acceptance/"
            r"(?:intake|statement|anchor_audit|obligation_tree|proof|validation|release)/"
            r"[0-9a-f]{64}\.json",
            relative,
        ) is not None
        if (
            path.is_absolute()
            or ".." in path.parts
            or (
                directory
                and not canonical_runtime_directory
                and not canonical_receipt_directory
            )
            or (
                not directory
                and
                relative not in allowed_runtime
                and not allowed_runtime_evidence(relative)
                and relative not in {
                    "Docs/Stage1_Blueprint_v2.md",
                    "Docs/Stage1_Blueprint_rev-5.6.md",
                    "Docs/Stage1_Execution_DAG_rev-5.6.json",
                    "Docs/Stage1_Theorem_DAG_v2.json",
                }
                and re.fullmatch(r"Docs/todos_[0-9]{8}\.md", relative) is None
                and not canonical_instance_file
            )
            or (not directory and reserved_receipt_file and not canonical_receipt_file)
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

    # Validate the complete recovery plan before changing the first byte. A
    # corrupt late row must never leave an otherwise valid prefix rolled back.
    recovery_rows: list[tuple[Path, str, bytes | None, int | None]] = []
    for row in rows:
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
        payload: bytes | None = None
        if kind == "file":
            payload_hex = row.get("payload_hex")
            if not isinstance(payload_hex, str):
                fail("integration recovery journal file payload is missing")
            try:
                payload = bytes.fromhex(payload_hex)
            except ValueError:
                fail("integration recovery journal file payload is malformed")
        if mode is not None and (
            not isinstance(mode, int) or mode < 0 or mode > 0o7777
        ):
            fail("integration recovery journal file mode is malformed")
        recovery_rows.append((target, kind, payload, mode))
    created_dirs = wal.get("created_dirs", [])
    if not isinstance(created_dirs, list):
        fail("integration recovery directory list is malformed")
    recovery_dirs: list[Path] = []
    for relative in created_dirs:
        if not isinstance(relative, str):
            fail("integration recovery directory list is malformed")
        recovery_dirs.append(recovery_target(relative, directory=True))

    for target, kind, payload, mode in reversed(recovery_rows):
        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.exists():
            fail(
                "integration recovery destination became a directory: "
                f"{target.relative_to(ROOT)}"
            )
        if kind == "file":
            durable_write_bytes(target, payload if payload is not None else b"")
            if isinstance(mode, int):
                target.chmod(mode)
    for directory in reversed(recovery_dirs):
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
    if data.get("execution_contract") != EXECUTION_CONTRACT:
        fail("v2 theorem DAG execution contract is incomplete or stale")
    ranks = [node.get("v2_execution_rank") for node in nodes]
    if sorted(ranks) != list(range(1, 1547)):
        fail("v2 theorem DAG execution ranks are not contiguous")
    rank_by_id = {theorem_id: node["v2_execution_rank"] for theorem_id, node in by_id.items()}
    hard_edges = data.get("hard_edges")
    if not isinstance(hard_edges, list):
        fail("v2 theorem DAG hard_edges must be a list")
    parents_by_id: dict[str, set[str]] = {theorem_id: set() for theorem_id in by_id}
    for edge in hard_edges:
        if not isinstance(edge, dict) or edge.get("blocking") is not True:
            fail("v2 theorem DAG has malformed hard edge")
        parent = edge.get("parent_theorem_id")
        child = edge.get("child_theorem_id")
        if parent not in by_id or child not in by_id or rank_by_id[parent] >= rank_by_id[child]:
            fail("v2 theorem DAG hard edge violates parent-first order")
        parents_by_id[child].add(parent)
        contract = edge.get("material_contract")
        if (
            not isinstance(contract, dict)
            or not isinstance(contract.get("provider_sources"), list)
            or not contract["provider_sources"]
            or not isinstance(contract.get("consumer_sources"), list)
            or not contract["consumer_sources"]
        ):
            fail("v2 theorem DAG hard edge lacks a material contract")
    closure_by_id: dict[str, set[str]] = {}
    for theorem_id in sorted(by_id, key=rank_by_id.__getitem__):
        direct = by_id[theorem_id].get("direct_hard_parents")
        ancestors = by_id[theorem_id].get("transitive_hard_ancestors")
        expected_direct = parents_by_id[theorem_id]
        expected_closure = set(expected_direct)
        for parent in expected_direct:
            expected_closure.update(closure_by_id[parent])
        expected_ancestors = sorted(expected_closure, key=rank_by_id.__getitem__)
        if (
            not isinstance(direct, list)
            or len(direct) != len(set(direct))
            or set(direct) != expected_direct
            or ancestors != expected_ancestors
        ):
            fail(f"v2 theorem DAG parent closure is incomplete or stale: {theorem_id}")
        closure_by_id[theorem_id] = expected_closure
    return data, by_id


def order_by_v2(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Use v2 theorem priority while preserving each theorem's seven phases."""
    _, nodes = theorem_dag_v2()
    return sorted(items, key=lambda item: claim_order_key(item, nodes))


def claim_order_key(
    item: dict[str, Any],
    theorem_nodes: dict[str, dict[str, Any]],
) -> tuple[int, int, str]:
    """Return the sole scheduler key declared by the theorem DAG contract."""
    return (
        theorem_nodes[item["theorem_id"]]["v2_execution_rank"],
        item["layer"],
        item["id"],
    )


def parent_inspection_order(
    theorem_id: str,
    theorem_nodes: dict[str, dict[str, Any]],
) -> list[str]:
    """Return the complete hard-parent closure in deterministic provider-first order."""
    node = theorem_nodes[theorem_id]
    direct = node.get("direct_hard_parents")
    ancestors = node.get("transitive_hard_ancestors")
    if not isinstance(direct, list) or not isinstance(ancestors, list):
        fail(f"{theorem_id} has malformed v2 parent metadata")
    closure = set(direct) | set(ancestors)
    if any(parent not in theorem_nodes for parent in closure):
        fail(f"{theorem_id} has an unknown v2 parent")
    child_rank = node.get("v2_execution_rank")
    ordered = sorted(closure, key=lambda parent: theorem_nodes[parent]["v2_execution_rank"])
    if not isinstance(child_rank, int) or any(
        theorem_nodes[parent].get("v2_execution_rank", child_rank) >= child_rank
        for parent in ordered
    ):
        fail(f"{theorem_id} has a hard parent that is not ranked before its consumer")
    return ordered


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
    rank = lambda parent: nodes[parent]["v2_execution_rank"]
    return {
        "direct_parent_ids": sorted(direct, key=rank),
        "transitive_ancestor_ids": sorted(ancestors, key=rank),
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
        if not isinstance(actual, list) or actual != values or len(actual) != len(set(actual)):
            raise ValueError(f"dependency reuse ledger has incomplete {field}")
    inspections = ledger.get("inspections")
    required_inspections = set(expected["direct_parent_ids"] + expected["transitive_ancestor_ids"])
    if not isinstance(inspections, list):
        raise ValueError("dependency reuse ledger inspections must be a list")
    inspected_ids = {row.get("theorem_id") for row in inspections if isinstance(row, dict)}
    if inspected_ids != required_inspections or len(inspections) != len(required_inspections):
        raise ValueError("dependency reuse ledger does not inspect every hard parent/ancestor exactly once")
    if [row.get("theorem_id") for row in inspections] != parent_inspection_order(theorem_id, nodes):
        raise ValueError("dependency reuse ledger inspections are not in v2 parent rank order")
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
            for item in authoritative_state_items(authoritative_root)
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
        for item in authoritative_state_items(authoritative_root)
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


def master_acceptance_receipt_path(
    theorem_id: str, phase: str, receipt_sha256: str
) -> str:
    if (
        not re.fullmatch(r"THM-M-[0-9]{4}", theorem_id)
        or phase not in PHASE_NAMES
        or re.fullmatch(r"[0-9a-f]{64}", receipt_sha256) is None
    ):
        raise ValueError("master acceptance receipt identity is malformed")
    return (
        f"Stage1_Instances/{theorem_id}/master-acceptance/"
        f"{phase}/{receipt_sha256}.json"
    )


def canonical_master_acceptance_receipt(
    item: dict[str, Any], claim: dict[str, Any], review_output: dict[str, Any],
    review_manifest: dict[str, Any], role_map: dict[str, Any],
    validator: dict[str, Any], replay: dict[str, Any], decision: dict[str, Any],
) -> tuple[dict[str, Any], bytes, str]:
    """Build a content-addressed scheduler-only phase receipt."""
    receipt = {
        "schema_version": MASTER_ACCEPTANCE_RECEIPT_SCHEMA,
        "item_id": item["id"],
        "theorem_id": item["theorem_id"],
        "phase": item["phase"],
        "authority_revision": review_manifest.get("authority_revision"),
        "authority_tree": review_manifest.get("authority_tree"),
        "worker_verdict": review_output["worker_verdict"],
        "review_verdict": review_output["review_verdict"],
        "phase_evidence_accepted": decision.get("phase_evidence_accepted"),
        "audit_complete": review_output["audit_complete"],
        "theorem_complete": review_output["theorem_complete"],
        "status_boundary": review_output["status_boundary"],
        "review_claim_id": claim["claim_id"],
        "review_binding_sha256": claim["review_binding_sha256"],
        "review_manifest_sha256": review_manifest["manifest_sha256"],
        "role_map_sha256": role_map["manifest_sha256"],
        "validator_recipe_sha256": validator["recipe_sha256"],
        "artifact_bindings": role_map["artifacts"],
        "replay_result_sha256": replay["result_sha256"],
        "replay_result": replay,
        "semantic_decision_sha256": decision["decision_sha256"],
        "semantic_decision": decision,
        "review_manifest": review_manifest,
        "role_map": role_map,
        "validator_recipe": validator,
    }
    payload = acceptance_evidence.canonical_json(receipt) + b"\n"
    digest = hashlib.sha256(payload).hexdigest()
    return receipt, payload, digest


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
        "requirements_source": "Docs/Stage1_Blueprint_v2.md",
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
    if data.get("requirements_source") != "Docs/Stage1_Blueprint_v2.md":
        fail("execution DAG requirements source is not the v2 blueprint")
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
    counts = Counter(item["state"] for item in items)
    worker_pct = 100 * counts["[_]"] / len(items) if items else 0.0
    lines = [
        CHECKLIST_BEGIN,
        "## 13. Generated 1546-Target Execution Checklist",
        "",
        "This appendix is the single writable task-state authority. The execution DAG and daily todo are",
        "generated, read-only projections of these stable rows; they never override this checklist.",
        "",
        "Authoritative progress summary (derived and validated from the rows below):",
        f"- `[_]` {counts['[_]']} ({worker_pct:.2f}% worker self-tested)",
        f"- `[ ]` {counts['[ ]']}",
        f"- `[x]` {counts['[x]']}",
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
            f"- {item['state']} `{item['id']}` / `{item['theorem_id']}` / `{item['phase']}`: "
            f"{item['deliverable']} {{attempts={item.get('attempts', 0)}}}"
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


def checklist_body(text: str) -> str:
    """Return the unique authoritative checklist body, failing closed."""
    if text.count(CHECKLIST_BEGIN) != 1 or text.count(CHECKLIST_END) != 1:
        fail("v2 blueprint must contain exactly one execution checklist marker pair")
    begin = text.index(CHECKLIST_BEGIN) + len(CHECKLIST_BEGIN)
    end = text.index(CHECKLIST_END, begin)
    return text[begin:end]


def load_blueprint_items() -> list[dict[str, Any]]:
    """Parse all task state and attempts from the v2 blueprint SSOT."""
    body = checklist_body(BLUEPRINT.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for match in CHECKLIST_ROW_RE.finditer(body):
        theorem_id = match["theorem"]
        phase = match["phase"]
        phase_index = next(index for index, row in enumerate(PHASES) if row[0] == phase)
        item = make_item(
            {"theorem_id": theorem_id, "execution_rank": 0}, phase_index
        )
        item.update(
            id=match["id"],
            state=match["state"],
            deliverable=match["deliverable"],
            attempts=int(match["attempts"]),
        )
        rows.append(item)
    expected = 1546 * len(PHASES)
    if len(rows) != expected:
        fail(f"v2 blueprint checklist must contain exactly {expected} machine-readable rows")
    ranks = {row["theorem_id"]: row["execution_rank"] for row in target_rows()}
    for item in rows:
        item["execution_rank"] = ranks[item["theorem_id"]]
    expected_render = render_checklist(rows)
    actual_render = CHECKLIST_BEGIN + body + CHECKLIST_END + "\n"
    if actual_render != expected_render:
        fail("v2 blueprint checklist has malformed, duplicate, reordered, or noncanonical rows")
    return rows


def authoritative_state_items(authoritative_root: Path = ROOT) -> list[dict[str, Any]]:
    """Load the SSOT under the selected authority root, including test clones."""
    if authoritative_root.resolve() == ROOT.resolve():
        return load_blueprint_items()
    blueprint = authoritative_root / "Docs" / "Stage1_Blueprint_v2.md"
    if blueprint.is_file():
        original = BLUEPRINT
        try:
            globals()["BLUEPRINT"] = blueprint
            return load_blueprint_items()
        finally:
            globals()["BLUEPRINT"] = original
    # Test-clone and one-time migration compatibility only. Production ROOT
    # must always possess the blueprint SSOT and never reaches this fallback.
    dag = authoritative_root / "Docs" / "Stage1_Execution_DAG_rev-5.6.json"
    if dag.is_file():
        items = read_json(dag).get("items")
        if isinstance(items, list):
            return items
    raise ValueError("authoritative Stage1 state source is missing")


def project_dag(items: list[dict[str, Any]]) -> dict[str, Any]:
    """Build the read-only execution-DAG projection from blueprint state."""
    data = new_dag()
    data["items"] = items
    return data


def write_derived_surfaces(data: dict[str, Any]) -> None:
    """Project the authoritative checklist to JSON after the blueprint write."""
    items = load_blueprint_items()
    projection = project_dag(items)
    validate_dag(projection)
    if data.get("items") != items:
        fail("authoritative blueprint write did not preserve the requested task state")
    atomic_write(DAG, json.dumps(projection, ensure_ascii=False, indent=2) + "\n")


def retire_assurance_checklist() -> None:
    """Remove the obsolete second checkbox surface after SSOT migration."""
    text = ASSURANCE_BLUEPRINT.read_text(encoding="utf-8")
    begin_count = text.count(CHECKLIST_BEGIN)
    end_count = text.count(CHECKLIST_END)
    if begin_count == end_count == 0:
        return
    if begin_count != 1 or end_count != 1:
        fail("assurance blueprint has malformed legacy checklist markers")
    replacement = (
        "## 13. Stage1 v2 Execution State\n\n"
        "The former generated phase checklist was migrated without state loss to "
        "`Docs/Stage1_Blueprint_v2.md`. That v2 checklist is the only writable task-state "
        "authority; the execution DAG and daily todo are derived projections.\n"
    )
    pattern = re.escape(CHECKLIST_BEGIN) + r".*?" + re.escape(CHECKLIST_END) + r"\n?"
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.DOTALL)
    if count != 1:
        fail("assurance blueprint legacy checklist markers are ambiguous")
    atomic_write(ASSURANCE_BLUEPRINT, updated)


def bootstrap() -> None:
    if CHECKLIST_BEGIN in BLUEPRINT.read_text(encoding="utf-8"):
        data = project_dag(load_blueprint_items())
    else:
        # One-time migration only: preserve the old projection byte-semantics,
        # then make the v2 checklist the sole source for every later run.
        data = read_json(DAG) if DAG.exists() else new_dag()
        data["requirements_source"] = "Docs/Stage1_Blueprint_v2.md"
    validate_dag(data)
    write_projection(data)
    write_derived_surfaces(data)
    retire_assurance_checklist()
    run(["python3", "Docs/tools/generate_stage1_theorem_dag_v2.py"])
    theorem_dag_v2.cache_clear()
    run(["python3", "Docs/tools/check_stage1_theorem_dag_v2.py"])
    print(f"bootstrapped {len(data['items'])} phase items for 1546 targets")


def load_dag() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    items = load_blueprint_items()
    data = project_dag(items)
    ordered = validate_dag(data)
    if not DAG.exists() or read_json(DAG) != data:
        fail("derived execution DAG disagrees with the v2 blueprint SSOT; run --bootstrap")
    return data, ordered


def runtime_path(name: str) -> Path:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    return RUNTIME / name


def load_claims() -> list[dict[str, Any]]:
    # Reading scheduler state must not create the runtime tree.  In particular,
    # validate-only uses this path and is required to leave an absent runtime
    # directory absent.
    path = RUNTIME / "claims.json"
    if not path.exists():
        return []
    if path.is_symlink() or not path.is_file():
        fail("claim ledger is not a regular scheduler-owned file")
    claims = read_json(path).get("claims", [])
    if not isinstance(claims, list):
        fail("claim ledger is malformed")
    return [claim for claim in claims if isinstance(claim, dict)]


def save_claims(claims: list[dict[str, Any]]) -> None:
    atomic_write(runtime_path("claims.json"), json.dumps({"claims": claims}, indent=2) + "\n")


def pid_alive(pid: Any) -> bool:
    return isinstance(pid, int) and pid > 0 and (PROC_ROOT / str(pid)).exists()


def process_command(pid: Any) -> list[str]:
    if not pid_alive(pid):
        return []
    try:
        raw = (PROC_ROOT / str(pid) / "cmdline").read_bytes()
    except OSError:
        return []
    return [part.decode("utf-8", errors="replace") for part in raw.split(b"\0") if part]


def process_start_ticks(pid: Any) -> int | None:
    """Return Linux /proc start ticks so a reused PID cannot inherit a lease."""
    if not pid_alive(pid):
        return None
    try:
        data = (PROC_ROOT / str(pid) / "stat").read_text(encoding="utf-8")
        closing = data.rfind(")")
        if closing < 0:
            return None
        fields_after_comm = data[closing + 2 :].split()
        return int(fields_after_comm[19])
    except (OSError, ValueError, IndexError):
        return None


def exact_option_values(command: list[str]) -> dict[str, str] | None:
    """Parse the closed client argv grammar without accepting duplicate flags."""
    if len(command) < 2 or Path(command[1]).absolute() != APP_SERVER_CLIENT.absolute():
        return None
    options: dict[str, str] = {}
    index = 2
    while index < len(command):
        flag = command[index]
        if flag not in {
            "--workspace", "--prompt", "--objective", "--status", "--log",
            "--lane", "--model", "--effort", "--service-tier", "--binding",
            "--thread-id", "--codex", "--timeout",
        } or flag in options or index + 1 >= len(command):
            return None
        options[flag] = command[index + 1]
        index += 2
    required = {
        "--workspace", "--prompt", "--objective", "--status", "--log",
        "--lane", "--model", "--effort", "--service-tier",
    }
    return options if required.issubset(options) else None


def canonical_client_identity(command: list[str]) -> dict[str, Any] | None:
    """Recognize only a scheduler-owned client invocation for this repository."""
    options = exact_option_values(command)
    if options is None:
        return None
    lane = options["--lane"]
    workspace_root = "review-workspaces" if lane == REVIEW_LANE else "workers"
    workspace_match = re.fullmatch(
        rf"{re.escape(str(RUNTIME / workspace_root))}/slot([1-9][0-9]*)",
        options["--workspace"],
    )
    status_match = re.fullmatch(
        rf"{re.escape(str(RUNTIME / 'app-server'))}/({CLAIM_ID_RE.pattern})\.json",
        options["--status"],
    )
    if lane not in LANES or workspace_match is None or status_match is None:
        return None
    slot = int(workspace_match.group(1))
    claim_id = status_match.group(1)
    expected = {
        "--prompt": RUNTIME / "prompts" / f"{claim_id}.txt",
        "--objective": RUNTIME / "goals" / f"{claim_id}.txt",
        "--log": RUNTIME / "logs" / f"{claim_id}.out",
    }
    if (
        slot > MAX_SLOT_ID
        or options["--model"] != CODEX_MODEL
        or options["--effort"] != CODEX_REASONING_EFFORT
        or options["--service-tier"] != CODEX_SERVICE_TIER
        or any(Path(options[flag]).absolute() != path.absolute() for flag, path in expected.items())
        or (lane == REVIEW_LANE) != ("--binding" in options)
        or (
            lane == REVIEW_LANE
            and Path(options["--binding"]).absolute()
            != (RUNTIME / "review-bindings" / f"{claim_id}.json").absolute()
        )
    ):
        return None
    return {
        "claim_id": claim_id,
        "lane": lane,
        "slot": slot,
        "workspace": options["--workspace"],
        "prompt": options["--prompt"],
        "objective": options["--objective"],
        "status": options["--status"],
        "log": options["--log"],
        "binding": options.get("--binding"),
        "thread_id": options.get("--thread-id"),
    }


def proc_parent_pid(pid: int) -> int | None:
    try:
        data = (PROC_ROOT / str(pid) / "stat").read_text(encoding="utf-8")
        closing = data.rfind(")")
        fields_after_comm = data[closing + 2 :].split() if closing >= 0 else []
        return int(fields_after_comm[1])
    except (OSError, ValueError, IndexError):
        return None


def stage1_process_inventory() -> tuple[list[dict[str, Any]], list[int]]:
    """Inventory canonical clients and every exact app-server child candidate."""
    clients: list[dict[str, Any]] = []
    processes: dict[int, tuple[int | None, list[str]]] = {}
    try:
        entries = list(PROC_ROOT.iterdir())
    except OSError:
        fail("cannot inspect process inventory; refuse lane allocation")
    for entry in entries:
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        command = process_command(pid)
        if not command:
            continue
        processes[pid] = (proc_parent_pid(pid), command)
        identity = canonical_client_identity(command)
        if (
            len(command) >= 2
            and Path(command[1]).absolute() == APP_SERVER_CLIENT.absolute()
            and identity is None
        ):
            fail("noncanonical Stage1 app-server client; refuse lane allocation")
        if identity is not None:
            start = process_start_ticks(pid)
            if start is None:
                fail("cannot bind a Stage1 client process identity; refuse lane allocation")
            clients.append({**identity, "pid": pid, "start_ticks": start})
    client_pids = {row["pid"] for row in clients}
    status_child_pids = set(runtime_status_child_identities())
    child_pids = sorted(
        pid
        for pid, (parent, command) in processes.items()
        if command[1:] == REQUIRED_APP_SERVER_ARGV
        and (
            parent in client_pids
            or pid in status_child_pids
        )
    )
    return clients, child_pids


def runtime_status_child_identities() -> dict[int, tuple[str, int]]:
    """Read only canonical status filenames and exact child identity fields."""
    status_root = RUNTIME / "app-server"
    if not status_root.exists():
        return {}
    if status_root.is_symlink() or not status_root.resolve().is_relative_to(RUNTIME.resolve()):
        fail("scheduler app-server status storage is unsafe; refuse lane allocation")
    identities: dict[int, tuple[str, int]] = {}
    try:
        entries = list(status_root.iterdir())
    except OSError:
        fail("cannot inspect app-server status inventory; refuse lane allocation")
    for path in entries:
        match = re.fullmatch(rf"({CLAIM_ID_RE.pattern})\.json", path.name)
        if match is None or path.is_symlink() or not path.is_file():
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(value, dict):
            continue
        child_pid = value.get("app_server_pid")
        child_start = value.get("app_server_start_ticks")
        if not isinstance(child_pid, int) or not isinstance(child_start, int):
            continue
        if child_pid in identities and identities[child_pid] != (match.group(1), child_start):
            fail("ambiguous Stage1 app-server child status; refuse lane allocation")
        identities[child_pid] = (match.group(1), child_start)
    return identities


def reconcile_process_inventory(claims: list[dict[str, Any]]) -> bool:
    """Recover uniquely-owned clients and reject every unledgered identity."""
    clients, child_pids = stage1_process_inventory()
    by_claim_id: dict[str, list[dict[str, Any]]] = {}
    for claim in claims:
        claim_id = claim.get("claim_id")
        if isinstance(claim_id, str):
            by_claim_id.setdefault(claim_id, []).append(claim)
    changed = False
    matched_clients: set[int] = set()
    for client in clients:
        matches = by_claim_id.get(client["claim_id"], [])
        if len(matches) != 1:
            fail("unledgered or ambiguous Stage1 app-server client; refuse lane allocation")
        claim = matches[0]
        expected_prompt = RUNTIME / "prompts" / f"{client['claim_id']}.txt"
        if (
            claim.get("runtime_protocol") != RUNTIME_PROTOCOL
            or claim.get("status") not in {"preparing", "launch_failed", "live", "draining"}
            or claim.get("lane", IMPLEMENTATION_LANE) != client["lane"]
            or claim.get("slot") != client["slot"]
            or str(claim.get("workspace", "")) != client["workspace"]
            or str(claim.get("app_server_status", "")) != client["status"]
            or str(claim.get("goal_objective_path", "")) != client["objective"]
            or str(claim.get("output_log", "")) != client["log"]
            or client["prompt"] != str(expected_prompt)
            or (
                client["lane"] == REVIEW_LANE
                and str(claim.get("review_binding_path", "")) != client["binding"]
            )
        ):
            fail("Stage1 app-server client disagrees with its canonical claim; refuse lane allocation")
        recorded = (claim.get("pid"), claim.get("pid_start_ticks"))
        observed = (client["pid"], client["start_ticks"])
        if recorded != observed:
            if claim.get("status") not in {"preparing", "launch_failed"} or (
                isinstance(recorded[0], int) and pid_alive(recorded[0])
            ):
                fail("Stage1 app-server client has an ambiguous process lease; refuse lane allocation")
            claim["pid"], claim["pid_start_ticks"] = observed
            claim["process_identity_recovered_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            changed = True
        matched_clients.add(client["pid"])
    status_children = runtime_status_child_identities()
    for child_pid in child_pids:
        status_identity = status_children.get(child_pid)
        if status_identity is None or process_start_ticks(child_pid) != status_identity[1]:
            fail("unledgered Stage1 app-server child; refuse lane allocation")
        claim_rows = by_claim_id.get(status_identity[0], [])
        if len(claim_rows) != 1 or claim_rows[0].get("runtime_protocol") != RUNTIME_PROTOCOL:
            fail("unledgered Stage1 app-server child; refuse lane allocation")
    return changed


def app_server_worker_is_live(claim: dict[str, Any]) -> bool:
    """Prove that the recorded PID is this claim's app-server client."""
    pid = claim.get("pid")
    command = process_command(pid)
    if not command:
        return False
    workspace = str(claim.get("workspace", ""))
    status_path = str(claim.get("app_server_status", ""))
    objective_path = str(claim.get("goal_objective_path", ""))
    output_path = str(claim.get("output_log", ""))
    expected_start = claim.get("pid_start_ticks")
    config = claim.get("runtime_config")
    lane = claim.get("lane", IMPLEMENTATION_LANE)
    if not isinstance(config, dict):
        return False
    return (
        claim.get("runtime_protocol") == RUNTIME_PROTOCOL
        and isinstance(expected_start, int)
        and process_start_ticks(pid) == expected_start
        and str(APP_SERVER_CLIENT) in command
        and "--workspace" in command
        and workspace in command
        and "--status" in command
        and status_path in command
        and "--objective" in command
        and objective_path in command
        and "--log" in command
        and output_path in command
        and "--model" in command
        and config.get("model") in command
        and "--effort" in command
        and config.get("reasoning_effort") in command
        and "--service-tier" in command
        and config.get("service_tier") in command
        and lane in LANES
        and "--lane" in command
        and lane in command
        and (
            lane != REVIEW_LANE
            or (
                "--binding" in command
                and str(claim.get("review_binding_path", "")) in command
            )
        )
    )


def app_server_child_is_live(claim: dict[str, Any]) -> bool:
    """Verify the exact app-server child argv independently of its client."""
    status = worker_status(claim)
    if not isinstance(status, dict):
        return False
    pid = status.get("app_server_pid")
    start = status.get("app_server_start_ticks")
    command = process_command(pid)
    return (
        isinstance(pid, int)
        and isinstance(start, int)
        and process_start_ticks(pid) == start
        and command[1:] == REQUIRED_APP_SERVER_ARGV
    )


def terminate_app_server_worker(claim: dict[str, Any]) -> bool:
    """Stop both independently grouped client and app-server processes."""
    client_live = app_server_worker_is_live(claim)
    child_live = app_server_child_is_live(claim)
    if not client_live and not child_live:
        return False
    client_pid = claim.get("pid") if client_live else None
    status = worker_status(claim)
    child_pid = status.get("app_server_pid") if isinstance(status, dict) else None
    if child_live and isinstance(child_pid, int):
        try:
            os.killpg(child_pid, 15)
        except ProcessLookupError:
            pass
    if client_live:
        assert isinstance(client_pid, int)
        try:
            os.killpg(client_pid, 15)
        except ProcessLookupError:
            pass
    for _ in range(50):
        client_stopped = not isinstance(client_pid, int) or not pid_alive(client_pid)
        child_stopped = not isinstance(child_pid, int) or not pid_alive(child_pid)
        if client_stopped and child_stopped:
            return True
        time.sleep(0.1)
    client_stopped = not isinstance(client_pid, int) or not pid_alive(client_pid)
    child_stopped = not isinstance(child_pid, int) or not pid_alive(child_pid)
    return client_stopped and child_stopped


def worker_status(claim: dict[str, Any]) -> dict[str, Any] | None:
    value = claim.get("app_server_status")
    if not isinstance(value, str):
        return None
    path = Path(value)
    expected = RUNTIME / "app-server" / f"{claim.get('claim_id')}.json"
    status_root = RUNTIME / "app-server"
    if (
        RUNTIME.is_symlink()
        or status_root.is_symlink()
        or (status_root.exists() and not status_root.resolve().is_relative_to(RUNTIME.resolve()))
        or path.absolute() != expected.absolute()
        or path.is_symlink()
        or not path.is_file()
    ):
        return None
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return result if isinstance(result, dict) else None


def recover_claim_process_identity(claim: dict[str, Any]) -> bool:
    """Recover a crash-window client identity from its content-bound status."""
    status = worker_status(claim)
    if not isinstance(status, dict):
        return False
    client_pid = status.get("client_pid")
    client_start = status.get("client_start_ticks")
    if not isinstance(client_pid, int) or not isinstance(client_start, int):
        return False
    original_pid = claim.get("pid")
    original_start = claim.get("pid_start_ticks")
    claim["pid"] = client_pid
    claim["pid_start_ticks"] = client_start
    if app_server_worker_is_live(claim):
        return True
    claim["pid"] = original_pid
    claim["pid_start_ticks"] = original_start
    return False


def claim_handshake_timed_out(claim: dict[str, Any]) -> bool:
    stamp = claim.get("client_started_at") or claim.get("claimed_at")
    if not isinstance(stamp, str):
        return True
    try:
        if stamp.endswith("Z") and "-" not in stamp[:8]:
            started = dt.datetime.strptime(stamp, "%Y%m%dT%H%M%SZ").replace(tzinfo=dt.timezone.utc)
        else:
            started = dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return True
    return (dt.datetime.now(dt.timezone.utc) - started).total_seconds() >= GOAL_HANDSHAKE_RECOVERY_GRACE_SECONDS


def goal_runtime_is_verified(claim: dict[str, Any]) -> bool:
    status = worker_status(claim)
    goal = status.get("goal") if isinstance(status, dict) else None
    contract = status.get("runtime_contract") if isinstance(status, dict) else None
    expected = claim.get("runtime_config")
    child_pid = status.get("app_server_pid") if isinstance(status, dict) else None
    child_start = status.get("app_server_start_ticks") if isinstance(status, dict) else None
    objective_path = claim.get("goal_objective_path")
    lane = claim.get("lane", IMPLEMENTATION_LANE)
    expected_sandbox = (
        REQUIRED_REVIEW_SANDBOX_CONTRACT
        if lane == REVIEW_LANE
        else REQUIRED_IMPLEMENTATION_SANDBOX_CONTRACT
    )
    objective_matches = False
    if isinstance(objective_path, str):
        path = Path(objective_path)
        expected_path = RUNTIME / "goals" / f"{claim.get('claim_id')}.txt"
        try:
            objective_matches = (
                path.absolute() == expected_path.absolute()
                and not path.is_symlink()
                and path.is_file()
                and path.read_text(encoding="utf-8").strip() == claim.get("goal_objective")
            )
        except OSError:
            objective_matches = False
    return (
        isinstance(status, dict)
        and status.get("state") in {"live", "finished"}
        and status.get("protocol") == RUNTIME_PROTOCOL
        and status.get("client_pid") == claim.get("pid")
        and status.get("client_start_ticks") == claim.get("pid_start_ticks")
        and isinstance(child_pid, int)
        and isinstance(child_start, int)
        and (status.get("state") == "finished" or process_start_ticks(child_pid) == child_start)
        and isinstance(status.get("thread_id"), str)
        and isinstance(goal, dict)
        and goal.get("threadId") == status.get("thread_id")
        and goal.get("objective") == claim.get("goal_objective")
        and objective_matches
        and goal.get("status") in {"active", "blocked", "usageLimited", "budgetLimited", "complete"}
        and isinstance(contract, dict)
        and isinstance(expected, dict)
        and contract.get("model") == expected.get("model")
        and contract.get("reasoning_effort") == expected.get("reasoning_effort")
        and contract.get("service_tier") == expected.get("service_tier")
        and contract.get("cwd") == claim.get("workspace")
        and status.get("lane", IMPLEMENTATION_LANE) == lane
        and contract.get("sandbox") == expected_sandbox
        and contract.get("network_access") is False
        and contract.get("app_server_argv") == REQUIRED_APP_SERVER_ARGV
        and (
            lane != REVIEW_LANE
            or (
                isinstance(status.get("binding_sha256"), str)
                and status.get("binding_sha256") == claim.get("review_binding_sha256")
            )
        )
    )


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
    # Recover or reject process identities before refresh can release, rewrite,
    # drain, or otherwise mutate a claim that still owns a live process. An
    # injected non-/proc root is required for focused unit calls so tests cannot
    # accidentally inspect or couple to host processes.
    if PROC_ROOT != Path("/proc") or ROOT.resolve() == Path(__file__).resolve().parents[1]:
        if reconcile_process_inventory(raw_claims):
            save_claims(raw_claims)
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
        if claim.get("status") not in active_statuses or claim.get("runtime_protocol") != RUNTIME_PROTOCOL:
            continue
        # One item may have one implementation handoff and one independent
        # review claim. Runtime identities remain globally unique.
        for field in ("worker_id", "slot", "workspace"):
            value = claim.get(field)
            if value is not None:
                identity_counts[(field, value)] += 1
        identity_counts[("item_lane", (claim.get("item_id"), claim.get("lane", IMPLEMENTATION_LANE)))] += 1
    current_revision = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    kept: list[dict[str, Any]] = []
    released: list[dict[str, Any]] = []
    for claim in raw_claims:
        item = item_by_id.get(claim.get("item_id"))
        if item is None:
            # Runtime state is not an authority surface. Preserve malformed or
            # obsolete rows for audit, but never derive runtime/filesystem side
            # effects from an identity absent from the validated DAG.
            claim["status"] = "quarantined"
            claim["quarantined_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["quarantine_reason"] = "claim item is absent from the authoritative DAG"
            kept.append(claim)
            continue
        lane = claim.get("lane", IMPLEMENTATION_LANE)
        if claim.get("theorem_id") != item["theorem_id"] or claim.get("owned_paths") != item["owned_paths"]:
            claim["status"] = "quarantined"
            claim["quarantined_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["quarantine_reason"] = "claim authority metadata disagrees with the validated DAG"
            kept.append(claim)
            continue
        slot = claim.get("slot")
        workspace_value = claim.get("workspace")
        output_value = claim.get("output_log")
        expected_rank = theorem_nodes[item["theorem_id"]]["v2_execution_rank"]
        claim_id = claim.get("claim_id")
        lane_tag = "impl" if lane == IMPLEMENTATION_LANE else "review"
        expected_worker_id = (
            (
                f"stage1app-{slot}-{expected_rank:04d}-{claim_id[-12:]}"
                if "lane" not in claim
                else f"stage1app-{lane_tag}-{slot}-{expected_rank:04d}-{claim_id[-12:]}"
            )
            if isinstance(slot, int) and isinstance(claim_id, str) and len(claim_id) >= 12
            else None
        )
        expected_workspace = (
            RUNTIME / "review-workspaces" / f"slot{slot}" if lane == REVIEW_LANE and isinstance(slot, int)
            else RUNTIME / "workers" / f"slot{slot}" if isinstance(slot, int)
            else None
        )
        expected_output = RUNTIME / "logs" / f"{claim_id}.out"
        expected_status = RUNTIME / "app-server" / f"{claim_id}.json"
        expected_goal = RUNTIME / "goals" / f"{claim_id}.txt"
        runtime_bound = claim.get("status") in active_statuses | {"blocked"}
        active_runtime = claim.get("status") in active_statuses
        protocol = claim.get("runtime_protocol", LEGACY_RUNTIME_PROTOCOL)
        legacy_runtime = protocol == LEGACY_RUNTIME_PROTOCOL
        # Historical tmux claims and quarantines belong to the retired runtime.
        # The new ledger never adopts, rewrites, or derives side effects from them.
        if legacy_runtime:
            claim["status"] = "quarantined"
            claim["quarantined_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["quarantine_reason"] = "legacy runtime claim is not reusable by the app-server scheduler"
            kept.append(claim)
            continue
        if runtime_bound and (
            (
                active_runtime
                and (
                    any(identity_counts[(field, claim.get(field))] > 1 for field in ("worker_id", "slot", "workspace"))
                    or identity_counts[("item_lane", (claim.get("item_id"), lane))] > 1
                )
            )
            or (
            not isinstance(slot, int)
            or isinstance(slot, bool)
            or slot < 1
            or slot > MAX_SLOT_ID
            or not isinstance(claim_id, str)
            or CLAIM_ID_RE.fullmatch(claim_id) is None
            or not isinstance(workspace_value, str)
            or Path(workspace_value).absolute() != expected_workspace.absolute()
            or Path(workspace_value).is_symlink()
            or (
                Path(workspace_value).exists()
                and not Path(workspace_value).resolve().is_relative_to(runtime_resolved)
            )
            or not isinstance(output_value, str)
            or Path(output_value).absolute() != expected_output.absolute()
            or claim.get("worker_id") != expected_worker_id
            or claim.get("runtime_protocol") != RUNTIME_PROTOCOL
            or not isinstance(claim.get("app_server_status"), str)
            or Path(str(claim.get("app_server_status"))).absolute() != expected_status.absolute()
            or not isinstance(claim.get("goal_objective_path"), str)
            or Path(str(claim.get("goal_objective_path"))).absolute() != expected_goal.absolute()
            or not isinstance(claim.get("goal_objective"), str)
            or not claim.get("goal_objective")
            or not isinstance(claim.get("runtime_config"), dict)
            or set(claim["runtime_config"]) != {"model", "reasoning_effort", "service_tier"}
            or claim["runtime_config"] != REQUIRED_RUNTIME_CONFIG
            or lane not in LANES
            or (
                lane == REVIEW_LANE
                and (
                    not isinstance(claim.get("review_binding_path"), str)
                    or Path(str(claim.get("review_binding_path"))).absolute()
                    != (RUNTIME / "review-bindings" / f"{claim_id}.json").absolute()
                    or not isinstance(claim.get("review_binding_sha256"), str)
                    or not isinstance(claim.get("review_binding_file_sha256"), str)
                    or not isinstance(claim.get("review_input_path"), str)
                    or Path(str(claim.get("review_input_path"))).absolute()
                    != (RUNTIME / "review-inputs" / f"{claim_id}.json").absolute()
                    or not isinstance(claim.get("review_input_sha256"), str)
                    or not isinstance(claim.get("review_manifest_path"), str)
                    or Path(str(claim.get("review_manifest_path"))).absolute()
                    != (RUNTIME / "review-manifests" / f"{claim_id}.json").absolute()
                    or not isinstance(claim.get("review_manifest_file_sha256"), str)
                    or not isinstance(claim.get("review_manifest_sha256"), str)
                    or not isinstance(claim.get("review_provenance_path"), str)
                    or not isinstance(claim.get("review_provenance_sha256"), str)
                )
            )
            )
        ):
            claim["status"] = "quarantined"
            claim["quarantined_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["quarantine_reason"] = "claim runtime identity is not scheduler-canonical"
            kept.append(claim)
            continue
        if (
            lane == IMPLEMENTATION_LANE
            and claim.get("fresh_revalidation") is True
            and claim.get("status")
            in {"live", "preparing", "launch_failed", "draining", "finished"}
        ):
            try:
                current_claim_legacy_revalidation_lane(claim, item)
            except (ValueError, SystemExit) as exc:
                if app_server_worker_is_live(claim) or app_server_child_is_live(claim):
                    terminate_app_server_worker(claim)
                claim["status"] = "quarantined"
                claim["quarantined_at"] = dt.datetime.now(
                    dt.timezone.utc
                ).isoformat()
                claim["quarantine_reason"] = (
                    "historical revalidation authority was revoked: " + str(exc)
                )
                kept.append(claim)
                continue
        if states[item["id"]] == "[x]":
            if claim.get("status") == "master_accepted":
                kept.append(claim)
                continue
            if (
                claim.get("status") in {"live", "preparing", "launch_failed", "draining"}
                and (app_server_worker_is_live(claim) or app_server_child_is_live(claim))
            ):
                terminate_app_server_worker(claim)
                if app_server_worker_is_live(claim) or app_server_child_is_live(claim):
                    claim["status"] = "draining"
                    claim["drain_reason"] = "master accepted but app-server worker did not stop"
                    kept.append(claim)
                    continue
            claim["released_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["release_reason"] = "master_accepted"
            released.append(claim)
            continue
        if claim.get("status") in {"review_finished", "review_failed"}:
            if lane != REVIEW_LANE:
                claim["status"] = "quarantined"
                claim["quarantined_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                claim["quarantine_reason"] = "review terminal status appeared on implementation lane"
            if claim.get("status") == "review_finished":
                try:
                    status = worker_status(claim)
                    binding = claimed_runtime_json(
                        claim, "review_binding_path", "review-bindings", "review binding"
                    )
                    if not isinstance(status, dict):
                        raise ValueError("review finished status is missing")
                    claim["review_output"] = require_review_output(claim, status, binding)
                except ValueError as exc:
                    claim["status"] = "review_failed"
                    claim["review_failed_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                    claim["review_retry_after"] = (
                        dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15)
                    ).isoformat()
                    claim["review_failure_reason"] = str(exc)
            kept.append(claim)
            continue
        if lane == REVIEW_LANE and states[item["id"]] != "[_]":
            if (
                claim.get("status") in {"live", "preparing", "launch_failed", "draining"}
                and (app_server_worker_is_live(claim) or app_server_child_is_live(claim))
            ):
                terminate_app_server_worker(claim)
                if app_server_worker_is_live(claim) or app_server_child_is_live(claim):
                    claim["status"] = "draining"
                    claim["drain_reason"] = "review authority item is no longer worker-self-tested"
                    kept.append(claim)
                    continue
            claim["released_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["release_reason"] = "review authority item is no longer worker-self-tested"
            released.append(claim)
            continue
        if claim.get("status") == "draining":
            if app_server_worker_is_live(claim) or app_server_child_is_live(claim):
                terminate_app_server_worker(claim)
            if app_server_worker_is_live(claim) or app_server_child_is_live(claim):
                claim["drain_retried_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                kept.append(claim)
            else:
                claim["released_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                claim["release_reason"] = "draining app-server worker stopped"
                released.append(claim)
            continue
        if claim.get("status") in {"preparing", "launch_failed"}:
            workspace = Path(str(claim.get("workspace", "")))
            manifest = workspace / ".stage1-worker-selftest.json"
            if not app_server_worker_is_live(claim):
                recover_claim_process_identity(claim)
            if app_server_worker_is_live(claim):
                if not goal_runtime_is_verified(claim):
                    status = worker_status(claim)
                    failed = isinstance(status, dict) and status.get("state") == "failed"
                    if not failed and not claim_handshake_timed_out(claim):
                        claim["status"] = "preparing"
                        claim["handshake_pending_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                        kept.append(claim)
                        continue
                    claim["status"] = "draining"
                    claim["drain_reason"] = (
                        "app-server reported failed /goal handshake"
                        if failed else "app-server /goal handshake exceeded recovery grace"
                    )
                    terminate_app_server_worker(claim)
                    kept.append(claim)
                    continue
                claim["status"] = "live"
                claim["recovered_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                kept.append(claim)
            elif app_server_child_is_live(claim):
                status = worker_status(claim)
                failed = isinstance(status, dict) and status.get("state") == "failed"
                if not failed and not claim_handshake_timed_out(claim):
                    claim["status"] = "preparing"
                    claim["handshake_pending_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                    kept.append(claim)
                    continue
                claim["status"] = "draining"
                claim["drain_reason"] = (
                    "orphan app-server reported failed /goal handshake"
                    if failed else "orphan app-server /goal handshake exceeded recovery grace"
                )
                terminate_app_server_worker(claim)
                kept.append(claim)
            elif lane == REVIEW_LANE:
                status = worker_status(claim)
                if isinstance(status, dict) and status.get("state") == "finished" and goal_runtime_is_verified(claim):
                    try:
                        binding = claimed_runtime_json(
                            claim, "review_binding_path", "review-bindings", "review binding"
                        )
                        claim["review_output"] = require_review_output(claim, status, binding)
                        claim["status"] = "review_finished"
                        claim["review_finished_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                    except ValueError as exc:
                        claim["status"] = "review_failed"
                        claim["review_failure_reason"] = str(exc)
                    kept.append(claim)
                else:
                    claim["released_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                    claim["release_reason"] = "incomplete review launch reservation"
                    released.append(claim)
            elif manifest.is_file() and not manifest.is_symlink():
                if not goal_runtime_is_verified(claim):
                    claim["status"] = "quarantined"
                    claim["quarantined_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                    claim["quarantine_reason"] = "recovered handoff lacks a verified app-server /goal runtime contract"
                    kept.append(claim)
                    continue
                claim["status"] = "finished"
                claim["selftest_manifest"] = (
                    str(manifest.relative_to(ROOT)) if manifest.is_relative_to(ROOT) else str(manifest)
                )
                claim["recovered_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                kept.append(claim)
            else:
                claim["released_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                claim["release_reason"] = "incomplete worker launch reservation"
                released.append(claim)
            continue
        if claim.get("status") == "live" and not app_server_worker_is_live(claim):
            if lane == REVIEW_LANE:
                status = worker_status(claim)
                if isinstance(status, dict) and status.get("state") == "finished" and goal_runtime_is_verified(claim):
                    try:
                        binding = claimed_runtime_json(
                            claim, "review_binding_path", "review-bindings", "review binding"
                        )
                        claim["review_output"] = require_review_output(claim, status, binding)
                        claim["status"] = "review_finished"
                        claim["review_finished_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                    except ValueError as exc:
                        claim["status"] = "review_failed"
                        claim["review_failure_reason"] = str(exc)
                else:
                    claim["status"] = "review_failed"
                    claim["review_failed_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                    claim["review_retry_after"] = (
                        dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15)
                    ).isoformat()
                    claim["review_failure_reason"] = (
                        status.get("error", "review exited without a verified structured output")
                        if isinstance(status, dict)
                        else "review exited without a verified structured output"
                    )
                kept.append(claim)
                continue
            manifest = Path(claim.get("workspace", "")) / ".stage1-worker-selftest.json"
            if manifest.exists():
                if not goal_runtime_is_verified(claim):
                    claim["status"] = "quarantined"
                    claim["quarantined_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                    claim["quarantine_reason"] = "worker handoff lacks a verified app-server /goal runtime contract"
                    kept.append(claim)
                    continue
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
        elif claim.get("status") == "live" and not goal_runtime_is_verified(claim):
            claim["status"] = "draining"
            claim["drain_reason"] = "live worker lacks a verified app-server /goal runtime contract"
            terminate_app_server_worker(claim)
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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()


def read_bound_runtime_file(path: Path, label: str) -> tuple[bytes, str]:
    """Read one scheduler-owned regular file without following the leaf symlink."""
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise ValueError(f"{label} is missing or unsafe") from exc
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError(f"{label} is not a regular file")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        data = b"".join(chunks)
    finally:
        os.close(descriptor)
    return data, hashlib.sha256(data).hexdigest()


@functools.lru_cache(maxsize=1)
def phase_acceptance_contract() -> dict[str, Any]:
    try:
        return acceptance_evidence.load_head_contract(
            ROOT, PHASE_ACCEPTANCE_CONTRACT_SHA256
        )["contract"]
    except acceptance_evidence.EvidenceError as exc:
        fail(str(exc))


@functools.lru_cache(maxsize=1)
def phase_acceptance_contract_record() -> dict[str, Any]:
    try:
        return acceptance_evidence.load_head_contract(
            ROOT, PHASE_ACCEPTANCE_CONTRACT_SHA256
        )
    except acceptance_evidence.EvidenceError as exc:
        fail(str(exc))


def phase_contract(item: dict[str, Any]) -> dict[str, Any]:
    rows = [
        row for row in phase_acceptance_contract().get("phases", [])
        if isinstance(row, dict) and row.get("phase") == item.get("phase")
    ]
    if len(rows) != 1:
        fail(f"phase acceptance contract is missing exactly one {item.get('phase')} row")
    return rows[0]


def scheduler_head_path(relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        fail(f"unsafe scheduler review path: {relative!r}")
    path = ROOT / relative
    if path.is_symlink() or not path.is_file():
        fail(f"scheduler review input is missing or unsafe: {relative}")
    tracked = run(["git", "ls-files", "--error-unmatch", "--", relative], check=False)
    if tracked.returncode:
        fail(f"scheduler review input is not HEAD tracked: {relative}")
    head_bytes = git_object_bytes(f"HEAD:{relative}")
    if path.read_bytes() != head_bytes:
        fail(f"scheduler review input worktree bytes disagree with HEAD: {relative}")
    return path


def _receipt_bound_paths(receipt: dict[str, Any], pointer: str) -> list[str]:
    value: Any = receipt
    for component in pointer.removeprefix("/").split("/"):
        if not component or not isinstance(value, dict) or component not in value:
            return []
        value = value[component]
    if isinstance(value, str):
        value = [value]
    if isinstance(value, dict):
        value = [value]
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for row in value:
        if isinstance(row, str):
            result.append(row)
        elif isinstance(row, dict) and isinstance(row.get("path"), str):
            result.append(row["path"])
    return result


def build_review_role_map(item: dict[str, Any], base_revision: str) -> dict[str, Any]:
    """Resolve exact HEAD-owned artifacts before allocating an independent review."""
    try:
        return acceptance_evidence.resolve_role_map(
            ROOT,
            phase_acceptance_contract_record(),
            item_id=item["id"],
            theorem_id=item["theorem_id"],
            phase=item["phase"],
            base_revision=base_revision,
        )
    except acceptance_evidence.EvidenceError as exc:
        fail(str(exc))


def select_review_validator(item: dict[str, Any], base_revision: str) -> dict[str, Any]:
    try:
        return acceptance_evidence.select_validator_recipe(
            ROOT,
            phase_acceptance_contract_record(),
            item_id=item["id"],
            theorem_id=item["theorem_id"],
            phase=item["phase"],
            base_revision=base_revision,
        )
    except acceptance_evidence.EvidenceError as exc:
        fail(str(exc))


def task_prompt(item: dict[str, Any], workspace: Path) -> str:
    item_json = json.dumps(item, ensure_ascii=False, indent=2)
    _, theorem_nodes = theorem_dag_v2()
    theorem_node = theorem_nodes[item["theorem_id"]]
    inspection_order = parent_inspection_order(item["theorem_id"], theorem_nodes)
    dependency_context = json.dumps(
        {
            "graph_sha256": graph_sha256(),
            "dependency_context_sha256": theorem_node.get("dependency_context_sha256"),
            "theorem_node": theorem_node,
            "parent_inspection_order": inspection_order,
            "required_ledger_context": expected_dependency_context(item["theorem_id"]),
            "ledger_schema": DEPENDENCY_LEDGER_SCHEMA,
            "execution_contract": EXECUTION_CONTRACT,
        },
        ensure_ascii=False,
        indent=2,
    )
    return f"""You are Stage1 rev-5.6 worker for exactly one Lean 4 theorem execution task.

Repository root: {workspace}
Work only inside this worker automation clone: {workspace}
Do not edit the scheduler's authoritative checkout directly: {ROOT}

This thread has a real persisted Codex `/goal`, created through app-server
`thread/goal/set`, for exactly the assigned item below. `Docs/Stage1_Blueprint_v2.md`
is the sole task-state authority. `Docs/Stage1_Blueprint_rev-5.6.md` is assurance
authority only. Do not claim theorem completion without every rev-5.6 gate and
kernel evidence.

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
   Before proof work, traverse every ID in `parent_inspection_order` exactly once and in that order; it is the complete direct/transitive closure in ascending v2 rank, not only the nearest parents. Inspect each parent's authoritative phase state, receipts, declaration bodies, and reusable artifacts. Accepted reuse is only `reused_exact` or `reused_with_transport`. Prefer an exact already-proved body over reproving it: import it when possible; otherwise copy only the minimal proof term/declaration into the consumer-owned path and record both the original provider bytes and the consumer copy/checked transport. A checked transport must bind both statement fingerprints, the provider source bytes, the consumer-owned import/wrapper bytes, and the consumer's own validation receipt. Re-elaborate the consumer and bind both byte hashes. Provider checkbox/receipt state is observation only: copying never transfers parent acceptance or evidence credit, and a `[_]` parent is guidance only unless the hard edge's material contract permits provisional consumption.
   Create or refresh the target-owned dependency-reuse-ledger.json required by the execution skill. Use schema {DEPENDENCY_LEDGER_SCHEMA} and exactly the graph digest/context IDs above. The ledger must include inspections, reuse_decisions, and unresolved_compatibility_obligations as specified by the skill. Empty parent/hint/group closure still requires an empty audited ledger. A reuse_hint or [_] ancestor is informative only and cannot transfer proof credit.
3. The HEAD phase contract at `Docs/Stage1_Phase_Acceptance_Contracts.json` is
   mandatory for new evidence. Produce exactly one phase receipt with schema
   `stage1-node-receipt/1.0`, every contract-required field, and complete
   path/SHA-256/Git-blob bindings for every role the contract selects. Produce
   exactly one HEAD-tracked validator at one of the phase's declared candidate
   paths. Its stdout must be exactly one JSON object with schema
   `stage1-validator-semantic-result/1.0` and the exact fields required by the
   scheduler; legacy prose stdout, exit code zero alone, or an undeclared
   adapter cannot support master acceptance. The worker may report a truthful
   negative result, but must never infer `phase_accepted` from command success.
4. Run the smallest real validation available and record exact commands/results in the owned artifact.
   The worker clone reuses the canonical pinned Lean `.lake` artifacts when available. Do not run
   `lake update`, `lake build`, dependency `git clone`/`git fetch`, or otherwise mutate `.lake`;
   those actions are neither a pinned validation nor valid worker evidence. Use the existing
   toolchain with `lake env lean` for narrowly scoped elaboration checks, and record a missing
   artifact as a blocker rather than fetching a moving dependency.
5. Do not edit Docs/Stage1_Execution_DAG_rev-5.6.json, Docs/Stage1_Theorem_DAG_v2.json, either blueprint, the generated checklist, or any item state. You are a worker, never the master.
6. If and only if your assigned phase is genuinely self-tested, write `.stage1-worker-selftest.json` at the workspace root with item_id, changed_paths, commands, output_summary, base_revision, known_failures, and `state: "[_]"`. Otherwise leave no self-test manifest and explain the blocker in an owned artifact.
7. Do not commit, push, launch tmux, launch `codex exec`, create nested agents, or modify unrelated targets. The app-server integration lane will inspect this clone.
"""


def worker_goal_objective(item: dict[str, Any]) -> str:
    return (
        f"Execute {item['id']} for {item['theorem_id']} from the sole task-state authority "
        "Docs/Stage1_Blueprint_v2.md. Preserve rev-5.6 assurance, follow the exact DAG claim order, "
        "inspect every direct and transitive parent before proof work, and reuse compatible "
        "already-proved parent bodies by exact import or checked consumer-owned copy/transport "
        "without transferring acceptance. Finish only with truthful owned-path evidence and the "
        "required worker self-test handoff, or a target-scoped blocker."
    )


def review_goal_objective(item: dict[str, Any]) -> str:
    return (
        f"Independently review {item['id']} for {item['theorem_id']} against the exact "
        "scheduler-owned Stage1 phase acceptance contract and content binding. Preserve the "
        "worker verdict, report only phase_accepted, repair_required, or rejected, and finish "
        "with one schema-valid JSON result without changing any repository file."
    )


def review_prompt(
    item: dict[str, Any],
    review_input: dict[str, Any],
    review_claim_id: str,
    workspace: Path,
) -> str:
    return f"""You are the independent read-only Stage1 master phase reviewer.

Repository root: {workspace}
You have no writable repository root and no network access. Never modify files,
run a worker, select a replacement validator, or treat exit code zero alone as
acceptance. Inspect every bound artifact. The scheduler, not you, selected the
validator argv from the HEAD-owned contract. You may inspect and reason about
the selected recipe, but this review does not replace the scheduler's later
immutable replay and master CAS gate.

Review input (content-bound by the adjacent binding JSON):
{json.dumps(review_input, ensure_ascii=False, indent=2)}

Return exactly one JSON object matching the supplied output schema. Preserve the
worker verdict verbatim. `review_verdict` is exactly `phase_accepted`,
`repair_required`, or `rejected`. Raw blocked/open/stale semantics cannot be
phase_accepted even when a command exited zero. `theorem_complete=true` requires
`audit_complete=true`; phase acceptance normally accepts only this phase's typed
deliverable and does not imply theorem completion. Set the persisted /goal to
complete only after emitting that single JSON object.
"""


def build_review_binding(
    claim_id: str,
    item: dict[str, Any],
    base_revision: str,
    prompt_text: str,
    objective: str,
    role_map: dict[str, Any],
    validator: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": REVIEW_BINDING_SCHEMA,
        "claim_id": claim_id,
        "item_id": item["id"],
        "theorem_id": item["theorem_id"],
        "phase": item["phase"],
        "base_revision": base_revision,
        "blueprint_sha256": sha256_file(BLUEPRINT),
        "theorem_dag_sha256": sha256_file(THEOREM_DAG_V2),
        "prompt_sha256": hashlib.sha256(prompt_text.encode()).hexdigest(),
        "objective_sha256": hashlib.sha256(objective.encode()).hexdigest(),
        "artifact_digests": {
            row["path"]: row["sha256"] for row in role_map["artifacts"]
        },
        "validator_recipe_sha256s": [validator["recipe_sha256"]],
        "output_schema": REVIEW_OUTPUT_SCHEMA,
    }


def worker_argv(
    workspace: Path,
    prompt_path: Path,
    output_path: Path,
    status_path: Path,
    objective_path: Path,
    *,
    lane: str = IMPLEMENTATION_LANE,
    binding_path: Path | None = None,
    thread_id: str | None = None,
) -> list[str]:
    configured = {
        "model": CODEX_MODEL,
        "reasoning_effort": CODEX_REASONING_EFFORT,
        "service_tier": CODEX_SERVICE_TIER,
    }
    if configured != REQUIRED_RUNTIME_CONFIG:
        fail(
            "worker runtime fallback is forbidden: expected "
            f"{REQUIRED_RUNTIME_CONFIG}, got {configured}"
        )
    if lane not in LANES:
        fail(f"unsupported app-server lane: {lane}")
    if lane == REVIEW_LANE and binding_path is None:
        fail("review app-server lane requires a scheduler-owned binding")
    if lane == IMPLEMENTATION_LANE and binding_path is not None:
        fail("implementation app-server lane cannot receive a review binding")
    if thread_id is not None and (
        not isinstance(thread_id, str)
        or not thread_id
        or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,199}", thread_id) is None
    ):
        fail("resume thread id is malformed")
    argv = [
        sys.executable,
        str(APP_SERVER_CLIENT),
        "--workspace", str(workspace),
        "--prompt", str(prompt_path),
        "--objective", str(objective_path),
        "--status", str(status_path),
        "--log", str(output_path),
        "--lane", lane,
        "--model", CODEX_MODEL,
        "--effort", CODEX_REASONING_EFFORT,
        "--service-tier", CODEX_SERVICE_TIER,
    ]
    if binding_path is not None:
        argv.extend(["--binding", str(binding_path)])
    if thread_id is not None:
        argv.extend(["--thread-id", thread_id])
    return argv


def launch_app_server_worker(argv: list[str]) -> int:
    """Launch without tmux/nohup/shell and return the process-group leader."""
    process = subprocess.Popen(
        argv,
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True,
    )
    return process.pid


def confirm_goal_handshakes(
    claims: list[dict[str, Any]],
    cohort: list[dict[str, Any]],
    *,
    timeout_seconds: float = GOAL_HANDSHAKE_TIMEOUT_SECONDS,
) -> int:
    """Promote preparing clients only after app-server proves the exact /goal."""
    pending = list(cohort)
    deadline = time.monotonic() + timeout_seconds
    while pending and time.monotonic() < deadline:
        for claim in list(pending):
            if goal_runtime_is_verified(claim):
                claim["status"] = "live"
                claim["goal_verified_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                pending.remove(claim)
                save_claims(claims)
                continue
            status = worker_status(claim)
            if isinstance(status, dict) and status.get("state") == "failed":
                claim["status"] = "launch_failed"
                claim["launch_failed_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                claim["launch_error"] = str(status.get("error", "app-server /goal handshake failed"))
                if app_server_worker_is_live(claim) or app_server_child_is_live(claim):
                    terminated = terminate_app_server_worker(claim)
                    claim["process_terminated_after_handshake_failure"] = terminated
                    if not terminated:
                        claim["status"] = "draining"
                        claim["drain_reason"] = "failed /goal app-server process did not stop"
                pending.remove(claim)
                save_claims(claims)
        if pending:
            time.sleep(GOAL_HANDSHAKE_POLL_SECONDS)
    for claim in pending:
        claim["status"] = "launch_failed"
        claim["launch_failed_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        claim["launch_error"] = "timed out waiting for verified app-server /goal handshake"
        if app_server_worker_is_live(claim) or app_server_child_is_live(claim):
            terminated = terminate_app_server_worker(claim)
            claim["process_terminated_after_handshake_timeout"] = terminated
            if not terminated:
                claim["status"] = "draining"
                claim["drain_reason"] = "timed-out /goal client did not stop"
    if pending:
        save_claims(claims)
    return sum(claim.get("status") == "live" for claim in cohort)


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
    # Lean worker clones are source-only to keep 50 lanes practical. The host
    # symlink is only a convenience for implementation-time self-tests; it is
    # not acceptance evidence. Master replay never follows it and instead uses
    # the scheduler-owned bubblewrap runtime/mount policy.
    canonical_lean = ROOT / "Formalizations" / "Lean"
    worker_lean = workspace / "Formalizations" / "Lean"
    canonical_lake = canonical_lean / ".lake"
    worker_lake = worker_lean / ".lake"
    if canonical_lake.is_dir() and worker_lean.is_dir() and not worker_lake.exists():
        worker_lake.symlink_to(canonical_lake)
    return workspace


def prepare_review_workspace(slot: int, base_revision: str) -> Path:
    """Create a detached, clean, scheduler-owned checkout for read-only review."""
    workspace = RUNTIME / "review-workspaces" / f"slot{slot}"
    validate_runtime_root()
    if workspace.is_symlink():
        fail(f"review slot path is a symlink: {workspace}")
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.parent.mkdir(parents=True, exist_ok=True)
    run([
        "git", "clone", "--no-checkout", "--filter=blob:none", "--reference-if-able", str(ROOT),
        str(ROOT), str(workspace),
    ])
    run(["git", "checkout", "--detach", base_revision], cwd=workspace)
    if (
        workspace.is_symlink()
        or not workspace.resolve().is_relative_to(RUNTIME.resolve())
        or run(["git", "rev-parse", "HEAD"], cwd=workspace).stdout.strip() != base_revision
        or run(["git", "status", "--porcelain"], cwd=workspace).stdout.strip()
    ):
        fail("prepared review workspace is not the exact clean detached authority revision")
    return workspace


def render_todo(
    data: dict[str, Any],
    ordered: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    *,
    destination: Path | None = None,
) -> tuple[Path, str]:
    """Validate and render the canonical daily projection without writing it."""
    authoritative = load_blueprint_items()
    if data.get("items") != authoritative:
        fail("todo input disagrees with the v2 blueprint SSOT")
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
        claim_state = "unclaimed" if claim is None else f"{claim.get('status')}:{claim.get('worker_id', 'unknown')}"
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
    path = destination or DOCS / f"todos_{dt.date.today():%Y%m%d}.md"
    if (
        path.parent != DOCS
        or re.fullmatch(r"todos_[0-9]{8}\.md", path.name) is None
    ):
        fail("todo destination is not the canonical daily projection path")
    blueprint_sha256 = hashlib.sha256(BLUEPRINT.read_bytes()).hexdigest()
    state_records = [
        {"id": item["id"], "state": item["state"], "attempts": item.get("attempts", 0)}
        for item in sorted(authoritative, key=lambda row: row["id"])
    ]
    state_sha256 = hashlib.sha256(
        json.dumps(state_records, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    lines = [
        "# Stage1 rev-5.6 Execution Todo",
        "",
        "SSOT: `Docs/Stage1_Blueprint_v2.md`; this file is today's derived task snapshot. Assurance: `Docs/Stage1_Blueprint_rev-5.6.md`; derived DAG/order: `Docs/Stage1_Execution_DAG_rev-5.6.json`, `Docs/Stage1_Theorem_DAG_v2.json`.",
        f"SSOT blueprint SHA-256: `{blueprint_sha256}`",
        f"Phase state/attempts SHA-256: `{state_sha256}`",
        f"Not done: {counts['[ ]']}",
        f"Worker self-tested: {counts['[_]']}",
        f"Master accepted: {counts['[x]']}",
        f"Unfinished: {counts['[ ]'] + counts['[_]']}",
        f"Theorems master-complete [x] x7: {theorem_counts['completed']}",
        f"Theorems fully self-tested [_] x7: {theorem_counts['fully_self_tested']}",
        f"Theorems partial [_]/[ ]: {theorem_counts['partial']}",
        f"Theorems unstarted [ ] x7: {theorem_counts['unstarted']}",
        "DAG cycle check: passed.",
        f"Claim ledger: `{RUNTIME.relative_to(ROOT) / 'claims.json'}`; live worker claims: {sum(c.get('status') == 'live' for c in claims)}.",
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
    return path, "\n".join(lines)


def write_todo(
    data: dict[str, Any],
    ordered: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    *,
    destination: Path | None = None,
) -> Path:
    path, projection = render_todo(
        data, ordered, claims, destination=destination
    )
    atomic_write(path, projection)
    return path


def validate_only() -> None:
    validate_runtime_root()
    run(["python3", "-B", "Docs/tools/check_stage1_theorem_dag_v2.py"])
    data, ordered = load_dag()
    theorem_graph, _ = theorem_dag_v2()
    # A dry gate must not stop workers, snapshot workspaces, rewrite ledgers,
    # trim logs, or otherwise reconcile mutable scheduler state.
    claims = load_claims()
    todo, todo_projection = render_todo(data, ordered, claims)
    todo_status = "absent_projection_validated"
    if todo.exists():
        if todo.is_symlink() or not todo.is_file():
            fail("daily todo projection is not a regular file")
        if todo.read_text(encoding="utf-8") != todo_projection:
            fail("daily todo projection is stale relative to the v2 blueprint SSOT")
        todo_status = "current"
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
    print(f"todo={todo.relative_to(ROOT)} status={todo_status}")


def integrate(limit: int) -> int:
    """Run one all-or-none integration transaction."""
    if limit < 0 or limit > MAX_INTEGRATION_LIMIT:
        fail(f"--limit must be in 0..{MAX_INTEGRATION_LIMIT}")
    if execution_is_paused():
        fail("integration refused: Stage1 execution is paused")
    recover_integration_wal()
    if runtime_path("pending_checkpoint.json").exists():
        fail("pending checkpoint must be resumed before another integration pass")
    data, ordered = load_dag()
    ordered = order_by_v2(ordered)
    # Lease reconciliation is its own durable preflight. A later integration
    # rollback restores this post-refresh state rather than resurrecting dead
    # workers or discarding their scheduler-owned blocker snapshots.
    claims = refresh_claims(ordered)
    transaction = FileTransaction(runtime_path("integration_wal.json"))
    todo_path = DOCS / f"todos_{dt.date.today():%Y%m%d}.md"
    try:
        integrated = _integrate(
            limit, transaction, data, ordered, claims, todo_path=todo_path
        )
        if execution_is_paused():
            fail("integration rolled back: Stage1 execution was paused during this pass")
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
    *,
    todo_path: Path,
) -> int:
    """Verify worker handoffs and preserve bounded fail-closed reports."""
    # These projections and scheduler surfaces can be rewritten after worker
    # files land. Snapshot them before any copy so integration is all-or-none.
    for path in (
        BLUEPRINT,
        DAG,
        THEOREM_DAG_V2,
        runtime_path("claims.json"),
        runtime_path("integration_queue.json"),
        runtime_path("pending_checkpoint.json"),
        todo_path,
    ):
        transaction.snapshot(path)
    by_id = {item["id"]: item for item in data["items"]}
    master_accepted, review_rejected = consume_review_finished(
        data, ordered, claims, transaction, limit=limit
    )
    _, theorem_nodes = theorem_dag_v2()
    integration_key = lambda claim: (
        claim_order_key(by_id[str(claim.get("item_id"))], theorem_nodes)
        if claim.get("item_id") in by_id
        else (sys.maxsize, sys.maxsize, "")
    )
    ready = sorted(
        (claim for claim in claims if claim.get("status") == "finished"),
        key=integration_key,
    )[:limit]
    remaining = max(0, limit - len(master_accepted) - len(ready))
    blocked_ready = sorted((
        claim
        for claim in claims
        if claim.get("status") == "blocked"
        and not claim.get("blocked_artifacts_merged_at")
        and not claim.get("blocked_artifact_rejection_reason")
    ), key=integration_key)[:remaining]
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
            revalidation_lane = current_claim_legacy_revalidation_lane(claim, item)
            revalidating_historical = (
                item["state"] == "[_]"
                and claim.get("fresh_revalidation") is True
                and revalidation_lane is not None
            )
            if item["state"] != "[ ]" and not revalidating_historical:
                raise ValueError(
                    "finished claim no longer targets a not-done or planned historical item"
                )
            if claim.get("runtime_protocol") != RUNTIME_PROTOCOL or not goal_runtime_is_verified(claim):
                raise ValueError("worker handoff lacks a verified app-server /goal runtime contract")
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
            pre_attempts = int(item.get("attempts", 0))
            item["state"] = "[_]"
            item["attempts"] = pre_attempts + 1
            claim["status"] = "finished_integrated"
            claim["integrated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["fresh_revalidation"] = revalidating_historical
            if revalidating_historical:
                closure = {
                    "schema_version": LEGACY_REVALIDATION_INTEGRATION_SCHEMA,
                    "item_id": item["id"],
                    "theorem_id": item["theorem_id"],
                    "phase": item["phase"],
                    "plan_sha256": claim["legacy_revalidation_plan_sha256"],
                    "plan_file_sha256": claim[
                        "legacy_revalidation_plan_file_sha256"
                    ],
                    "plan_binding_sha256": claim[
                        "legacy_revalidation_plan_binding_sha256"
                    ],
                    "lane_sha256": claim["legacy_revalidation_lane_sha256"],
                    "base_revision": claim["base_revision"],
                    "pre_attempts": pre_attempts,
                    "post_attempts": item["attempts"],
                    "integrated_at": claim["integrated_at"],
                }
                claim["legacy_revalidation_integration"] = closure
                claim["legacy_revalidation_integration_sha256"] = (
                    canonical_json_sha256(closure)
                )
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
    if accepted or preserved_blockers or master_accepted:
        # Write the sole authority first, then regenerate every state-bearing
        # projection from it inside the same rollback transaction.
        if accepted or master_accepted:
            if execution_is_paused():
                fail("integration publication refused: Stage1 execution is paused")
            write_projection(data)
            if execution_is_paused():
                fail("derived publication refused: Stage1 execution is paused")
            write_derived_surfaces(data)
        # The v2 inventory includes target-owned blocker artifacts as well as
        # phase-state projections, so every copied batch must regenerate it.
        if execution_is_paused():
            fail("theorem DAG regeneration refused: Stage1 execution is paused")
        run(["python3", "Docs/tools/generate_stage1_theorem_dag_v2.py"])
        theorem_dag_v2.cache_clear()
        if execution_is_paused():
            fail("integration validation refused: Stage1 execution is paused")
        run(["python3", "Docs/tools/check_stage1_theorem_dag_v2.py"])
        run(["python3", "Docs/tools/check_stage1_standard.py"])
        run(["python3", "scripts/stage1_target.py", "check"])
    if execution_is_paused():
        fail("integration ledger publication refused: Stage1 execution is paused")
    save_claims(claims)
    integration_queue = {
        "master_accepted": master_accepted,
        "review_rejected": review_rejected,
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
    if execution_is_paused():
        fail("integration queue publication refused: Stage1 execution is paused")
    atomic_write(
        runtime_path("integration_queue.json"),
        json.dumps(integration_queue, ensure_ascii=False, indent=2) + "\n",
    )
    if execution_is_paused():
        fail("todo publication refused: Stage1 execution is paused")
    todo = write_todo(data, validate_dag(data), claims, destination=todo_path)
    checkpoint_paths = sorted({
        path
        for row in queue
        for path in row.get("changed_paths", [])
        if isinstance(path, str) and path != ".stage1-worker-selftest.json"
    } | set(integration_queue["blocked_paths"]))
    if accepted or preserved_blockers or master_accepted:
        checkpoint_files = sorted({
            *checkpoint_paths,
            *(
                str(claim["master_receipt_path"])
                for claim in claims
                if claim.get("item_id") in set(master_accepted)
                and isinstance(claim.get("master_receipt_path"), str)
            ),
            *(
                path
                for path in (
                    "Docs/Stage1_Blueprint_v2.md",
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
        if execution_is_paused():
            fail("checkpoint publication refused: Stage1 execution is paused")
        atomic_write(
            runtime_path("pending_checkpoint.json"),
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        )
    print(
        f"integrate: master-accepted={len(master_accepted)} worker-self-tested={len(accepted)} "
        f"blocked-reports={len(preserved_blockers)} rejected={len(rejected) + len(review_rejected)} "
        f"todo={todo.relative_to(ROOT)}"
    )
    return len(master_accepted) + len(accepted) + len(preserved_blockers)


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
    claim = next(
        (row for row in reversed(load_claims()) if row.get("item_id") == item_id and isinstance(row.get("output_log"), str)),
        None,
    )
    log = Path(str(claim["output_log"])) if claim is not None else None
    if log is None or not log.exists() or log.is_symlink():
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
        relative_to_owner = value.removeprefix(normalized_owner + "/")
        if relative_to_owner == "master-acceptance" or relative_to_owner.startswith(
            "master-acceptance/"
        ):
            raise ValueError("worker handoff targets the scheduler-reserved master-acceptance namespace")
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
    if execution_is_paused():
        fail("checkpoint push refused: Stage1 execution is paused")
    run(["git", "fetch", "--prune", "origin"])
    upstream = run(["git", "rev-parse", "@{u}"]).stdout.strip()
    if upstream != commit_revision:
        if upstream != base_revision:
            fail("checkpoint upstream moved away from the checkpoint base")
        if execution_is_paused():
            fail("checkpoint push refused: Stage1 execution is paused")
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
    if execution_is_paused():
        fail("checkpoint refused: Stage1 execution is paused")
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
        "Docs/Stage1_Blueprint_v2.md",
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
        if "/master-acceptance/" in path:
            parts = Path(path).parts
            if (
                len(parts) != 5
                or parts[0] != "Stage1_Instances"
                or re.fullmatch(r"THM-M-[0-9]{4}", parts[1]) is None
                or parts[2] != "master-acceptance"
                or parts[3] not in PHASE_NAMES
                or parts[4] != f"{digest}.json"
            ):
                fail("pending checkpoint contains a malformed master acceptance receipt path")
        target = ROOT / path
        if target.is_symlink() or not target.is_file():
            fail(f"pending checkpoint path is missing or unsafe: {path}")
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            fail(f"pending checkpoint source changed after validation: {path}")
        selected.append(path)
        expected_hashes[path] = digest
        expected_modes[path] = mode

    state_surfaces = {
        "Docs/Stage1_Blueprint_v2.md",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "Docs/Stage1_Theorem_DAG_v2.json",
    }
    selected_state_surfaces = state_surfaces.intersection(selected)
    if selected_state_surfaces.intersection({
        "Docs/Stage1_Blueprint_v2.md",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
    }) and selected_state_surfaces != state_surfaces:
        fail("task-state checkpoint must bind the blueprint SSOT and both state projections together")
    if "Docs/Stage1_Theorem_DAG_v2.json" in selected_state_surfaces:
        # Content binding alone would allow three mutually consistent-looking
        # but semantically forged state files. Re-run the independent SSOT and
        # projection validators immediately before staging or recovery.
        load_dag()
        run(["python3", "Docs/tools/check_stage1_theorem_dag_v2.py"])

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

    if execution_is_paused():
        fail("checkpoint staging refused: Stage1 execution is paused")
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
    if execution_is_paused():
        fail("checkpoint commit refused: Stage1 execution is paused")
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
    if execution_is_paused():
        fail("checkpoint push refused: Stage1 execution is paused")
    finish_checkpoint_push(pending_path, base_revision, commit_revision)


def active_lane_leases(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Count implementation and review processes against one total budget."""
    return [
        claim
        for claim in claims
        if claim.get("runtime_protocol") == RUNTIME_PROTOCOL
        and (app_server_worker_is_live(claim) or app_server_child_is_live(claim))
    ]


def _head_blob_binding(relative: str) -> dict[str, Any]:
    """Return the exact regular-file binding for one authoritative HEAD blob."""
    if Path(relative).is_absolute() or ".." in Path(relative).parts:
        fail("legacy revalidation plan names an unsafe authority path")
    listing = run(["git", "ls-tree", "HEAD", "--", relative]).stdout.strip()
    match = re.fullmatch(r"(100644|100755) blob ([0-9a-f]{40,64})\t(.+)", listing)
    if match is None or match.group(3) != relative:
        fail(f"legacy revalidation authority is not one exact HEAD blob: {relative}")
    data = git_object_bytes(f"HEAD:{relative}")
    return {
        "path": relative,
        "git_blob": match.group(2),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
        "git_mode": match.group(1),
    }


def _legacy_plan_binding(
    value: dict[str, Any], *, file_sha256: str
) -> dict[str, Any]:
    lanes = value.get("lanes")
    if not isinstance(lanes, list):
        raise ValueError("legacy revalidation plan lacks lanes")
    return {
        "schema_version": LEGACY_REVALIDATION_PLAN_BINDING_SCHEMA,
        "plan_sha256": value.get("plan_sha256"),
        "plan_file_sha256": file_sha256,
        "generated_from_revision": value.get("generated_from_revision"),
        "generated_from_tree": value.get("generated_from_tree"),
        "source_bindings": value.get("source_bindings"),
        "lane_sha256s": [
            lane.get("lane_sha256") if isinstance(lane, dict) else None
            for lane in lanes
        ],
    }


def _valid_legacy_plan_binding_shape(binding: Any) -> bool:
    if not isinstance(binding, dict):
        return False
    expected_fields = {
        "schema_version", "plan_sha256", "plan_file_sha256",
        "generated_from_revision", "generated_from_tree", "source_bindings",
        "lane_sha256s",
    }
    lane_sha256s = binding.get("lane_sha256s")
    return (
        set(binding) == expected_fields
        and binding.get("schema_version") == LEGACY_REVALIDATION_PLAN_BINDING_SCHEMA
        and re.fullmatch(r"[0-9a-f]{64}", str(binding.get("plan_sha256"))) is not None
        and re.fullmatch(r"[0-9a-f]{64}", str(binding.get("plan_file_sha256"))) is not None
        and re.fullmatch(r"[0-9a-f]{40,64}", str(binding.get("generated_from_revision")))
        is not None
        and re.fullmatch(r"[0-9a-f]{40,64}", str(binding.get("generated_from_tree")))
        is not None
        and isinstance(binding.get("source_bindings"), dict)
        and isinstance(lane_sha256s, list)
        and 1 <= len(lane_sha256s) <= 50
        and len(lane_sha256s) == len(set(lane_sha256s))
        and all(re.fullmatch(r"[0-9a-f]{64}", str(value)) for value in lane_sha256s)
    )


def _validate_legacy_revalidation_lane(
    lane: Any,
    *,
    item: dict[str, Any],
    plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(lane, dict):
        raise ValueError("historical revalidation claim lane is malformed")
    lane_digest = lane.get("lane_sha256")
    lane_unhashed = dict(lane)
    lane_unhashed.pop("lane_sha256", None)
    phase = item.get("phase")
    phase_layer = next(
        (index for index, row in enumerate(PHASES) if row[0] == phase), None
    )
    classifications = lane.get("legacy_classification_statuses")
    bindings = lane.get("bindings")
    expected_bindings = None
    expected_tree = None
    expected_rank = None
    if plan is not None:
        source = plan.get("source_bindings")
        if isinstance(source, dict):
            expected_bindings = {
                "blueprint_sha256": source.get("blueprint", {}).get("sha256")
                if isinstance(source.get("blueprint"), dict) else None,
                "theorem_dag_sha256": source.get("theorem_dag", {}).get("sha256")
                if isinstance(source.get("theorem_dag"), dict) else None,
                "contract_sha256": source.get("contract", {}).get("sha256")
                if isinstance(source.get("contract"), dict) else None,
                "inventory_sha256": source.get("inventory", {}).get("inventory_sha256")
                if isinstance(source.get("inventory"), dict) else None,
            }
        expected_tree = plan.get("generated_from_tree")
        try:
            _, nodes = theorem_dag_v2()
            expected_rank = nodes[str(item.get("theorem_id"))]["v2_execution_rank"]
        except (KeyError, TypeError):
            expected_rank = None
    binding_prefix_matches = (
        isinstance(bindings, dict)
        and expected_bindings is not None
        and all(bindings.get(field) == digest for field, digest in expected_bindings.items())
    ) if plan is not None else isinstance(bindings, dict)
    if (
        lane.get("schema_version") != LEGACY_REVALIDATION_LANE_SCHEMA
        or lane.get("item_id") != item.get("id")
        or lane.get("theorem_id") != item.get("theorem_id")
        or lane.get("phase") != phase
        or lane.get("phase_layer") != phase_layer
        or lane.get("attempts_at_plan_base") != item.get("attempts")
        or lane.get("authoritative_state") != "[_]"
        or lane.get("required_steps") != LEGACY_REVALIDATION_REQUIRED_STEPS
        or lane.get("step_outcomes")
        != {step: "unknown" for step in LEGACY_REVALIDATION_REQUIRED_STEPS}
        or lane.get("state_transition") != "none"
        or lane.get("acceptance_claimed") is not False
        or lane.get("promotes_to_master_accepted") is not False
        or lane.get("executes_validators") is not False
        or lane.get("launches_workers") is not False
        or lane.get("mutates_repository") is not False
        or not isinstance(lane.get("legacy_migration_ready_observation"), bool)
        or not isinstance(classifications, dict)
        or set(classifications) != LEGACY_INVENTORY_CLASSIFICATIONS
        or any(value not in {"blocked", "clear", "unknown"} for value in classifications.values())
        or lane_digest != canonical_json_sha256(lane_unhashed)
        or not binding_prefix_matches
        or not isinstance(bindings.get("inventory_item_sha256") if isinstance(bindings, dict) else None, str)
        or re.fullmatch(r"[0-9a-f]{64}", str(bindings.get("inventory_item_sha256"))) is None
        or not isinstance(bindings.get("dependency_context_sha256") if isinstance(bindings, dict) else None, str)
        or re.fullmatch(r"[0-9a-f]{64}", str(bindings.get("dependency_context_sha256"))) is None
        or (plan is not None and lane.get("authority_revision") != plan.get("generated_from_revision"))
        or (plan is not None and lane.get("authority_tree") != expected_tree)
        or (plan is not None and lane.get("v2_execution_rank") != expected_rank)
    ):
        raise ValueError("legacy revalidation plan lane is not content-bound and authoritative")
    return lane


def legacy_revalidation_plan() -> tuple[
    dict[str, dict[str, Any]], dict[str, Any] | None
]:
    """Load the optional HEAD plan; a genuinely stale plan expires harmlessly."""
    path = RUNTIME / "legacy-revalidation-plan.json"
    if not path.exists():
        return {}, None
    if (
        path.is_symlink()
        or path.absolute() != (RUNTIME / "legacy-revalidation-plan.json").absolute()
        or not path.resolve().is_relative_to(RUNTIME.resolve())
    ):
        fail("legacy revalidation plan storage is unsafe")
    try:
        value, data = read_exact_json_file(path, "legacy revalidation plan")
    except ValueError as exc:
        fail(str(exc))
    current_revision = run(["git", "rev-parse", "HEAD^{commit}"]).stdout.strip()
    current_tree = run(["git", "rev-parse", "HEAD^{tree}"]).stdout.strip()
    generated_revision = value.get("generated_from_revision")
    generated_tree = value.get("generated_from_tree")
    # A previously valid plan naturally expires after any checkpoint commit.
    # It must never starve the independent queue of ordinary [ ] work.
    if generated_revision != current_revision or generated_tree != current_tree:
        return {}, None
    embedded = value.get("plan_sha256")
    unhashed = dict(value)
    unhashed.pop("plan_sha256", None)
    lanes = value.get("lanes")
    source = value.get("source_bindings")
    selection = value.get("selection_policy")
    phases = [phase for phase, _ in PHASES]
    if (
        value.get("schema_version") != LEGACY_REVALIDATION_PLAN_SCHEMA
        or value.get("authority_mode") != "authoritative_head"
        or value.get("head_owned_contract") is not True
        or value.get("planning_only") is not True
        or value.get("authoritative_for_acceptance") is not False
        or value.get("mutates_repository") is not False
        or value.get("state_transition") != "none"
        or value.get("acceptance_claimed") is not False
        or value.get("writes_ssot") is not False
        or value.get("writes_todo") is not False
        or value.get("writes_claims") is not False
        or value.get("writes_paused_state") is not False
        or value.get("executes_validators") is not False
        or value.get("launches_workers") is not False
        or embedded != canonical_json_sha256(unhashed)
        or not isinstance(lanes, list)
        or not 1 <= len(lanes) <= 50
        or value.get("selected_item_count") != len(lanes)
        or value.get("required_steps") != LEGACY_REVALIDATION_REQUIRED_STEPS
        or not isinstance(source, dict)
        or not isinstance(selection, dict)
        or selection.get("hard_max_samples") != 50
        or selection.get("authoritative_state_filter") != "[_]"
        or selection.get("phase_order") != phases
        or selection.get("phase_layers") != {phase: index for index, phase in enumerate(phases)}
        or selection.get("within_phase_order") != ["v2_execution_rank", "item_id"]
        or selection.get("output_order") != ["phase_layer", "v2_execution_rank", "item_id"]
    ):
        fail("legacy revalidation plan is non-authoritative or malformed")
    expected_sources = {
        "blueprint": _head_blob_binding("Docs/Stage1_Blueprint_v2.md"),
        "theorem_dag": _head_blob_binding("Docs/Stage1_Theorem_DAG_v2.json"),
        "contract": _head_blob_binding("Docs/Stage1_Phase_Acceptance_Contracts.json"),
    }
    if any(source.get(name) != binding for name, binding in expected_sources.items()):
        fail("legacy revalidation plan source binding disagrees with authoritative HEAD")
    inventory = source.get("inventory")
    if (
        not isinstance(inventory, dict)
        or inventory.get("schema_version") != "stage1-legacy-migration-inventory/1.0"
        or re.fullmatch(r"[0-9a-f]{64}", str(inventory.get("inventory_sha256"))) is None
        or re.fullmatch(r"[0-9a-f]{64}", str(inventory.get("json_bytes_sha256"))) is None
        or isinstance(inventory.get("size"), bool)
        or not isinstance(inventory.get("size"), int)
        or inventory.get("size", 0) <= 0
    ):
        fail("legacy revalidation inventory source binding is malformed")
    inventory_path = RUNTIME / "legacy-migration-inventory.json"
    try:
        inventory_value, inventory_bytes = read_exact_json_file(
            inventory_path,
            "legacy migration inventory",
            expected_sha256=str(inventory["json_bytes_sha256"]),
        )
    except ValueError as exc:
        fail(str(exc))
    inventory_unhashed = dict(inventory_value)
    inventory_embedded = inventory_unhashed.pop("inventory_sha256", None)
    if (
        len(inventory_bytes) != inventory["size"]
        or inventory_value.get("schema_version") != inventory["schema_version"]
        or inventory_embedded != inventory["inventory_sha256"]
        or inventory_embedded != canonical_json_sha256(inventory_unhashed)
        or inventory_value.get("generated_from_revision") != current_revision
        or inventory_value.get("generated_from_tree") != current_tree
        or inventory_value.get("authority_mode") != "authoritative_head"
        or inventory_value.get("authoritative_for_acceptance") is not False
        or inventory_value.get("mutates_repository") is not False
        or inventory_value.get("executes_validators") is not False
        or inventory_value.get("blueprint") != source.get("blueprint")
        or inventory_value.get("contract") != source.get("contract")
    ):
        fail("legacy migration inventory binding is stale or malformed")
    authoritative = {item["id"]: item for item in load_blueprint_items()}
    result: dict[str, dict[str, Any]] = {}
    for lane in lanes:
        item_id = lane.get("item_id") if isinstance(lane, dict) else None
        item = authoritative.get(item_id)
        if item is None or item.get("state") != "[_]":
            fail("legacy revalidation plan lane no longer targets authoritative [_]")
        try:
            validated = _validate_legacy_revalidation_lane(lane, item=item, plan=value)
        except ValueError as exc:
            fail(str(exc))
        if item_id in result:
            fail("legacy revalidation plan duplicates an item")
        result[str(item_id)] = validated
    binding = _legacy_plan_binding(value, file_sha256=hashlib.sha256(data).hexdigest())
    if not _valid_legacy_plan_binding_shape(binding):
        fail("legacy revalidation plan binding is malformed")
    return result, binding


def legacy_revalidation_lanes() -> dict[str, dict[str, Any]]:
    """Return only current, content-bound historical implementation lanes."""
    return legacy_revalidation_plan()[0]


def optional_legacy_revalidation_lanes() -> dict[str, dict[str, Any]]:
    """Keep a bad optional plan from starving the ordinary [ ] frontier."""
    try:
        return legacy_revalidation_lanes()
    except SystemExit as exc:
        print(
            "warning: ignored invalid optional legacy revalidation plan; "
            f"ordinary work remains eligible ({exc})",
            file=sys.stderr,
        )
        return {}


def legacy_revalidation_item_ids() -> set[str]:
    return set(legacy_revalidation_lanes())


def claim_legacy_revalidation_lane(
    claim: dict[str, Any], item: dict[str, Any]
) -> dict[str, Any] | None:
    """Verify the fresh-source mode and immutable historical plan closure."""
    fresh = claim.get("fresh_revalidation")
    present = LEGACY_REVALIDATION_CLAIM_FIELDS.intersection(claim)
    if not isinstance(fresh, bool):
        raise ValueError("implementation claim lacks boolean fresh_revalidation provenance")
    if fresh is False:
        if present:
            raise ValueError("normal fresh implementation claim carries legacy revalidation bindings")
        return None
    if present != LEGACY_REVALIDATION_CLAIM_FIELDS:
        raise ValueError("historical revalidation claim lacks its complete plan binding")
    lane = claim.get("legacy_revalidation_lane")
    binding = claim.get("legacy_revalidation_plan_binding")
    try:
        lane = _validate_legacy_revalidation_lane(lane, item=item)
    except ValueError as exc:
        raise ValueError("historical revalidation claim is stale or not content-bound") from exc
    lane_digest = lane.get("lane_sha256")
    if (
        not _valid_legacy_plan_binding_shape(binding)
        or binding.get("generated_from_revision") != claim.get("base_revision")
        or lane.get("authority_revision") != claim.get("base_revision")
        or lane.get("authority_tree") != binding.get("generated_from_tree")
        or lane_digest not in binding.get("lane_sha256s", [])
        or claim.get("legacy_revalidation_lane_sha256") != lane_digest
        or claim.get("legacy_revalidation_plan_sha256") != binding.get("plan_sha256")
        or claim.get("legacy_revalidation_plan_file_sha256")
        != binding.get("plan_file_sha256")
        or claim.get("legacy_revalidation_plan_binding_sha256")
        != canonical_json_sha256(binding)
    ):
        raise ValueError("historical revalidation claim plan binding is not exact")
    source = binding.get("source_bindings")
    lane_bindings = lane.get("bindings")
    if (
        not isinstance(source, dict)
        or not isinstance(lane_bindings, dict)
        or lane_bindings.get("blueprint_sha256")
        != source.get("blueprint", {}).get("sha256")
        or lane_bindings.get("theorem_dag_sha256")
        != source.get("theorem_dag", {}).get("sha256")
        or lane_bindings.get("contract_sha256")
        != source.get("contract", {}).get("sha256")
        or lane_bindings.get("inventory_sha256")
        != source.get("inventory", {}).get("inventory_sha256")
    ):
        raise ValueError("historical revalidation claim source binding is not exact")
    return lane


def current_claim_legacy_revalidation_lane(
    claim: dict[str, Any], item: dict[str, Any]
) -> dict[str, Any] | None:
    """Verify a historical lease against the current HEAD-owned plan file."""
    lane = claim_legacy_revalidation_lane(claim, item)
    if lane is None:
        return None
    current_revision = run(["git", "rev-parse", "HEAD^{commit}"]).stdout.strip()
    current_tree = run(["git", "rev-parse", "HEAD^{tree}"]).stdout.strip()
    binding = claim["legacy_revalidation_plan_binding"]
    if (
        claim.get("base_revision") != current_revision
        or binding.get("generated_from_revision") != current_revision
        or binding.get("generated_from_tree") != current_tree
    ):
        raise ValueError("historical revalidation claim authority is no longer current HEAD")
    lanes, current_binding = legacy_revalidation_plan()
    current_lane = lanes.get(str(item.get("id")))
    if (
        current_binding is None
        or current_binding != binding
        or current_lane != lane
    ):
        raise ValueError("historical revalidation claim no longer matches the HEAD-owned plan")
    return lane


def post_integration_legacy_revalidation_lane(
    claim: dict[str, Any], item: dict[str, Any]
) -> dict[str, Any] | None:
    """Verify the scheduler-owned N -> N+1 historical integration closure."""
    if claim.get("fresh_revalidation") is False:
        if LEGACY_REVALIDATION_INTEGRATION_FIELDS.intersection(claim):
            raise ValueError("normal implementation claim carries historical integration data")
        return claim_legacy_revalidation_lane(claim, item)
    closure = claim.get("legacy_revalidation_integration")
    digest = claim.get("legacy_revalidation_integration_sha256")
    lane = claim.get("legacy_revalidation_lane")
    binding = claim.get("legacy_revalidation_plan_binding")
    if (
        claim.get("status") != "finished_integrated"
        or not isinstance(claim.get("integrated_at"), str)
        or not claim.get("integrated_at")
        or not isinstance(closure, dict)
        or set(closure) != {
            "schema_version", "item_id", "theorem_id", "phase",
            "plan_sha256", "plan_file_sha256", "plan_binding_sha256",
            "lane_sha256", "base_revision", "pre_attempts", "post_attempts",
            "integrated_at",
        }
        or closure.get("schema_version") != LEGACY_REVALIDATION_INTEGRATION_SCHEMA
        or closure.get("item_id") != item.get("id")
        or closure.get("theorem_id") != item.get("theorem_id")
        or closure.get("phase") != item.get("phase")
        or closure.get("plan_sha256") != claim.get("legacy_revalidation_plan_sha256")
        or closure.get("plan_file_sha256")
        != claim.get("legacy_revalidation_plan_file_sha256")
        or closure.get("plan_binding_sha256")
        != claim.get("legacy_revalidation_plan_binding_sha256")
        or closure.get("lane_sha256") != claim.get("legacy_revalidation_lane_sha256")
        or closure.get("base_revision") != claim.get("base_revision")
        or closure.get("integrated_at") != claim.get("integrated_at")
        or not isinstance(lane, dict)
        or not isinstance(binding, dict)
        or closure.get("pre_attempts") != lane.get("attempts_at_plan_base")
        or closure.get("post_attempts") != item.get("attempts")
        or closure.get("post_attempts") != int(closure.get("pre_attempts", -2)) + 1
        or digest != canonical_json_sha256(closure)
    ):
        raise ValueError("historical revalidation integration closure is not exact")
    # Validate the immutable plan/lane fields against their pre-integration
    # attempts without requiring the naturally advanced plan file to remain current.
    plan_base_item = dict(item)
    plan_base_item["attempts"] = closure["pre_attempts"]
    verified = claim_legacy_revalidation_lane(claim, plan_base_item)
    if verified != lane:
        raise ValueError("historical revalidation integration lane changed after merge")
    return verified


def refuse_unsafe_live_identities(claims: list[dict[str, Any]]) -> None:
    unsafe = [
        claim
        for claim in claims
        if claim.get("status") == "quarantined"
        and (app_server_worker_is_live(claim) or app_server_child_is_live(claim))
    ]
    if unsafe:
        fail("claim ledger contains a quarantined live app-server identity; refuse lane allocation")


def review_candidates(
    ordered: list[dict[str, Any]], claims: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    now = dt.datetime.now(dt.timezone.utc)
    reviewed_or_claimed: set[Any] = set()
    for claim in claims:
        item_id = claim.get("item_id")
        lane = claim.get("lane", IMPLEMENTATION_LANE)
        status = claim.get("status")
        if lane == IMPLEMENTATION_LANE and status in {"live", "preparing", "draining"}:
            reviewed_or_claimed.add(item_id)
        if lane != REVIEW_LANE:
            continue
        if status in {"preparing", "live", "draining", "review_finished", "quarantined"}:
            reviewed_or_claimed.add(item_id)
            continue
        retry_after = claim.get("review_retry_after")
        if status == "review_failed" and isinstance(retry_after, str):
            try:
                if dt.datetime.fromisoformat(retry_after.replace("Z", "+00:00")) > now:
                    reviewed_or_claimed.add(item_id)
            except ValueError:
                reviewed_or_claimed.add(item_id)
    states = {item.get("id"): item.get("state") for item in ordered}
    fresh_sources = {
        claim.get("item_id")
        for claim in claims
        if claim.get("lane", IMPLEMENTATION_LANE) == IMPLEMENTATION_LANE
        and claim.get("status") == "finished_integrated"
        and claim.get("runtime_protocol") == RUNTIME_PROTOCOL
        and isinstance(claim.get("fresh_revalidation"), bool)
    }
    source_claims_by_item: dict[Any, list[dict[str, Any]]] = {}
    for claim in claims:
        if (
            claim.get("lane", IMPLEMENTATION_LANE) == IMPLEMENTATION_LANE
            and claim.get("status") == "finished_integrated"
            and claim.get("runtime_protocol") == RUNTIME_PROTOCOL
            and isinstance(claim.get("fresh_revalidation"), bool)
        ):
            source_claims_by_item.setdefault(claim.get("item_id"), []).append(claim)
    candidates = [
        item for item in ordered
        if item.get("state") == "[_]"
        and item.get("id") in fresh_sources
        and len(source_claims_by_item.get(item.get("id"), [])) == 1
        and item.get("id") not in reviewed_or_claimed
        and all(states.get(dependency) == "[x]" for dependency in item.get("depends_on", []))
        and (
            item.get("phase") not in {"proof", "validation", "release"}
            or hard_edge_gate_status(
                str(item.get("theorem_id")), str(item.get("phase"))
            )[0] in {"not_applicable", "satisfied"}
        )
    ]
    _, nodes = theorem_dag_v2()
    return sorted(candidates, key=lambda item: claim_order_key(item, nodes))


def implementation_candidates(
    ordered: list[dict[str, Any]], claims: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Return implementation-eligible items without assigning lane priority."""
    claimed_ids = {
        claim.get("item_id")
        for claim in claims
        if claim.get("runtime_protocol") == RUNTIME_PROTOCOL
        and claim.get("status")
        in {"live", "finished", "preparing", "launch_failed", "draining", "quarantined"}
    }
    claimed_ids.update(
        claim.get("item_id")
        for claim in claims
        if claim.get("runtime_protocol") == RUNTIME_PROTOCOL
        and claim.get("lane", IMPLEMENTATION_LANE) == IMPLEMENTATION_LANE
        and claim.get("status") in {
            "finished_integrated", "master_accepted", "review_finished", "review_failed"
        }
    )
    states_by_id = {item["id"]: item["state"] for item in ordered}
    started_targets = {
        item["theorem_id"]
        for item in ordered
        if item["state"] in {"[_]", "[x]"}
    }
    # The historical plan is an optional lane, never a prerequisite for the
    # ordinary [ ] frontier. Load it only when the SSOT actually has [_] work
    # that is otherwise unclaimed.
    needs_historical_plan = any(
        item.get("state") == "[_]" and item.get("id") not in claimed_ids
        for item in ordered
    )
    historical_revalidation = (
        optional_legacy_revalidation_lanes() if needs_historical_plan else {}
    )
    candidates = [
        item
        for item in ordered
        if item["state"] in {"[ ]", "[_]"}
        and (item["state"] == "[ ]" or item["id"] in historical_revalidation)
        and item["id"] not in claimed_ids
        and (not STARTED_TARGETS_ONLY or item["theorem_id"] in started_targets)
        and all(
            states_by_id.get(dependency) in {"[_]", "[x]"}
            for dependency in item["depends_on"]
        )
    ]
    _, nodes = theorem_dag_v2()
    return sorted(candidates, key=lambda item: claim_order_key(item, nodes))


def unified_lane_candidates(
    ordered: list[dict[str, Any]], claims: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Merge both lane frontiers under the one authoritative claim order."""
    records = [
        {"lane": REVIEW_LANE, "item": item}
        for item in review_candidates(ordered, claims)
    ] + [
        {"lane": IMPLEMENTATION_LANE, "item": item}
        for item in implementation_candidates(ordered, claims)
    ]
    item_ids = [record["item"]["id"] for record in records]
    if len(item_ids) != len(set(item_ids)):
        fail("one item is simultaneously eligible for implementation and review")
    _, nodes = theorem_dag_v2()
    return sorted(records, key=lambda record: claim_order_key(record["item"], nodes))


def review_source_claim(
    item: dict[str, Any], claims: list[dict[str, Any]]
) -> dict[str, Any] | None:
    """Return the unique, complete implementation provenance for one review."""
    candidates = [
        claim
        for claim in claims
        if claim.get("lane", IMPLEMENTATION_LANE) == IMPLEMENTATION_LANE
        and claim.get("item_id") == item.get("id")
        and claim.get("status") == "finished_integrated"
        and claim.get("runtime_protocol") == RUNTIME_PROTOCOL
        and isinstance(claim.get("fresh_revalidation"), bool)
    ]
    if len(candidates) != 1:
        return None
    claim = candidates[0]
    required = {
        "claim_id",
        "base_revision",
        "goal_objective",
        "goal_objective_path",
        "app_server_status",
        "output_log",
        "workspace",
        "selftest_manifest",
        "fresh_revalidation",
    }
    string_required = required - {"fresh_revalidation"}
    if (
        any(not isinstance(claim.get(field), str) or not claim.get(field) for field in string_required)
        or not isinstance(claim.get("fresh_revalidation"), bool)
    ):
        return None
    return claim


def snapshot_review_provenance(
    item: dict[str, Any], claim: dict[str, Any]
) -> dict[str, Any]:
    """Freeze the exact worker claim/status/prompt/goal/handoff before review."""
    if review_source_claim(item, [claim]) is None:
        raise ValueError("implementation provenance is incomplete")
    status = worker_status(claim)
    if not isinstance(status, dict) or status.get("state") != "finished":
        raise ValueError("implementation status is not a finished app-server record")
    claim_value = json.loads(json.dumps(claim, ensure_ascii=False))
    claim_sha256 = canonical_json_sha256(claim_value)
    status_sha256 = canonical_json_sha256(status)
    files: dict[str, dict[str, str]] = {}
    field_labels = {
        "goal_objective_path": "worker goal",
        "app_server_status": "worker status",
        "output_log": "worker output log",
        "selftest_manifest": "worker handoff",
    }
    for field, label in field_labels.items():
        path = Path(str(claim[field]))
        if not path.is_absolute():
            path = ROOT / path
        data, digest = read_bound_runtime_file(path, label)
        files[field] = {
            "path": str(path),
            "sha256": digest,
            "size": len(data),
            "content_base64": base64.b64encode(data).decode("ascii"),
        }
        if field == "goal_objective_path" and data.decode("utf-8").strip() != claim["goal_objective"]:
            raise ValueError("worker goal bytes disagree with its claim")
    prompt_path = RUNTIME / "prompts" / f"{claim['claim_id']}.txt"
    prompt_data, prompt_sha256 = read_bound_runtime_file(prompt_path, "worker prompt")
    files["prompt"] = {
        "path": str(prompt_path),
        "sha256": prompt_sha256,
        "size": len(prompt_data),
        "content_base64": base64.b64encode(prompt_data).decode("ascii"),
    }
    snapshot = {
        "schema_version": WORKER_PROVENANCE_SCHEMA,
        "item_id": item["id"],
        "theorem_id": item["theorem_id"],
        "phase": item["phase"],
        "claim": claim_value,
        "claim_sha256": claim_sha256,
        "status": status,
        "status_sha256": status_sha256,
        "files": files,
    }
    snapshot["snapshot_sha256"] = canonical_json_sha256(snapshot)
    return snapshot


def persist_review_provenance(
    implementation_claim: dict[str, Any], snapshot: dict[str, Any]
) -> tuple[Path, str]:
    """Persist one immutable scheduler copy and reject conflicting reuse."""
    claim_id = implementation_claim.get("claim_id")
    if not isinstance(claim_id, str) or CLAIM_ID_RE.fullmatch(claim_id) is None:
        raise ValueError("implementation provenance claim id is malformed")
    path = RUNTIME / "worker-provenance" / f"{claim_id}.json"
    payload = acceptance_evidence.canonical_json(snapshot) + b"\n"
    digest = hashlib.sha256(payload).hexdigest()
    if path.exists() or path.is_symlink():
        existing, existing_digest = read_bound_runtime_file(path, "worker provenance snapshot")
        if existing != payload or existing_digest != digest:
            raise ValueError("immutable worker provenance snapshot conflicts with existing bytes")
    else:
        durable_write_bytes(path, payload)
    return path, digest


def build_scheduler_review_manifest(
    provenance: dict[str, Any],
    role_map: dict[str, Any],
    validator: dict[str, Any],
) -> dict[str, Any]:
    """Bind the exact SSOT/DAG and frozen worker five-tuple for review."""
    scheduler_head_path(BLUEPRINT.relative_to(ROOT).as_posix())
    scheduler_head_path(THEOREM_DAG_V2.relative_to(ROOT).as_posix())
    files = provenance.get("files")
    if not isinstance(files, dict):
        raise ValueError("worker provenance has no bound files")
    required = {"app_server_status", "prompt", "goal_objective_path", "selftest_manifest"}
    if not required.issubset(files) or any(
        not isinstance(files.get(name), dict)
        or re.fullmatch(r"[0-9a-f]{64}", str(files[name].get("sha256", ""))) is None
        for name in required
    ):
        raise ValueError("worker provenance five-tuple is incomplete")
    try:
        return acceptance_evidence.build_review_manifest(
            phase_acceptance_contract_record(),
            role_map,
            validator,
            blueprint_sha256=sha256_file(BLUEPRINT),
            theorem_dag_sha256=sha256_file(THEOREM_DAG_V2),
            worker_claim_sha256=str(provenance.get("claim_sha256")),
            worker_status_sha256=str(provenance.get("status_sha256")),
            worker_prompt_sha256=str(files["prompt"]["sha256"]),
            worker_goal_sha256=str(files["goal_objective_path"]["sha256"]),
            worker_handoff_sha256=str(files["selftest_manifest"]["sha256"]),
        )
    except acceptance_evidence.EvidenceError as exc:
        raise ValueError(str(exc)) from exc


def persist_review_manifest(
    review_claim_id: str, manifest: dict[str, Any]
) -> tuple[Path, str]:
    if CLAIM_ID_RE.fullmatch(review_claim_id) is None:
        raise ValueError("review manifest claim id is malformed")
    embedded = manifest.get("manifest_sha256")
    unhashed = dict(manifest)
    unhashed.pop("manifest_sha256", None)
    if embedded != canonical_json_sha256(unhashed):
        raise ValueError("review manifest embedded digest is not content-bound")
    path = RUNTIME / "review-manifests" / f"{review_claim_id}.json"
    payload = acceptance_evidence.canonical_json(manifest) + b"\n"
    file_digest = hashlib.sha256(payload).hexdigest()
    if path.exists() or path.is_symlink():
        existing, existing_digest = read_bound_runtime_file(path, "review manifest")
        if existing != payload or existing_digest != file_digest:
            raise ValueError("immutable review manifest conflicts with existing bytes")
    else:
        durable_write_bytes(path, payload)
    return path, file_digest


def read_exact_json_file(
    path: Path, label: str, *, expected_sha256: str | None = None
) -> tuple[dict[str, Any], bytes]:
    data, digest = read_bound_runtime_file(path, label)
    if expected_sha256 is not None and digest != expected_sha256:
        raise ValueError(f"{label} digest disagrees with its claim")

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{label} contains duplicate key {key!r}")
            result[key] = value
        return result

    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} is not canonical UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value, data


def claimed_runtime_json(
    claim: dict[str, Any], field: str, directory: str, label: str
) -> dict[str, Any]:
    path_value = claim.get(field)
    claim_id = claim.get("claim_id")
    expected = RUNTIME / directory / f"{claim_id}.json"
    if not isinstance(path_value, str) or Path(path_value).absolute() != expected.absolute():
        raise ValueError(f"{label} path is not scheduler-canonical")
    digest_field = {
        "review_input_path": "review_input_sha256",
        "review_manifest_path": "review_manifest_file_sha256",
        "review_binding_path": "review_binding_file_sha256",
    }.get(field)
    expected_digest = claim.get(digest_field) if digest_field else None
    value, _ = read_exact_json_file(
        Path(path_value), label,
        expected_sha256=expected_digest if isinstance(expected_digest, str) else None,
    )
    return value


def require_review_output(
    claim: dict[str, Any], status: dict[str, Any], binding: dict[str, Any]
) -> dict[str, Any]:
    """Recheck the client's typed output without trusting its status summary."""
    output = status.get("review_output")
    text = status.get("review_output_text")
    if not isinstance(output, dict) or set(output) != REVIEW_OUTPUT_FIELDS:
        raise ValueError("review output fields are not exact")
    if not isinstance(text, str):
        raise ValueError("review output lacks its exact final text")
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("review output text is not JSON") from exc
    if parsed != output:
        raise ValueError("review output differs from its exact final text")
    canonical_digest = canonical_json_sha256(output)
    if (
        hashlib.sha256(text.encode("utf-8")).hexdigest()
        != status.get("review_output_sha256")
        or canonical_digest != status.get("review_output_canonical_sha256")
        or output.get("schema_version") != REVIEW_OUTPUT_SCHEMA
        or output.get("claim_id") != claim.get("claim_id")
        or output.get("item_id") != claim.get("item_id")
        or output.get("theorem_id") != claim.get("theorem_id")
        or output.get("phase") != binding.get("phase")
        or output.get("worker_verdict") not in WORKER_VERDICTS
        or output.get("review_verdict") not in REVIEW_VERDICTS
        or not isinstance(output.get("audit_complete"), bool)
        or not isinstance(output.get("theorem_complete"), bool)
        or not isinstance(output.get("status_boundary"), str)
        or not output.get("status_boundary")
        or output.get("reviewed_artifact_sha256s") != binding.get("artifact_digests")
        or output.get("validator_recipe_sha256s")
        != binding.get("validator_recipe_sha256s")
    ):
        raise ValueError("review output identity, digest, or typed verdict is invalid")
    findings = output.get("artifact_findings")
    if not isinstance(findings, list) or any(
        not isinstance(row, str) or not row for row in findings
    ):
        raise ValueError("review output findings are malformed")
    if output["theorem_complete"] and not output["audit_complete"]:
        raise ValueError("review output has an impossible theorem boundary")
    return output


def verify_review_evidence_bundle(
    item: dict[str, Any], claim: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Reload every scheduler snapshot and verify the prompt/binding closure."""
    review_input = claimed_runtime_json(
        claim, "review_input_path", "review-inputs", "review input"
    )
    manifest = claimed_runtime_json(
        claim, "review_manifest_path", "review-manifests", "review manifest"
    )
    binding = claimed_runtime_json(
        claim, "review_binding_path", "review-bindings", "review binding"
    )
    provenance_path = claim.get("review_provenance_path")
    if not isinstance(provenance_path, str):
        raise ValueError("review provenance path is missing")
    provenance, _ = read_exact_json_file(
        Path(provenance_path), "review provenance",
        expected_sha256=str(claim.get("review_provenance_sha256")),
    )
    if (
        review_input.get("schema_version") != REVIEW_INPUT_SCHEMA
        or review_input.get("review_claim_id") != claim.get("claim_id")
        or review_input.get("item") != item
        or review_input.get("implementation_provenance") != provenance
        or review_input.get("implementation_provenance_path") != provenance_path
        or review_input.get("implementation_provenance_file_sha256")
        != claim.get("review_provenance_sha256")
        or review_input.get("review_manifest") != manifest
        or review_input.get("review_manifest_path") != claim.get("review_manifest_path")
        or review_input.get("review_manifest_file_sha256")
        != claim.get("review_manifest_file_sha256")
        or manifest.get("manifest_sha256") != claim.get("review_manifest_sha256")
    ):
        raise ValueError("review input does not bind its provenance and manifest")
    role_map = review_input.get("role_map")
    validator = review_input.get("validator_recipe")
    if not isinstance(role_map, dict) or not isinstance(validator, dict):
        raise ValueError("review input lacks its role map or validator recipe")
    objective = review_goal_objective(item)
    prompt = review_prompt(
        item, review_input, str(claim.get("claim_id")), Path(str(claim.get("workspace")))
    )
    if (
        binding.get("schema_version") != REVIEW_BINDING_SCHEMA
        or binding.get("claim_id") != claim.get("claim_id")
        or binding.get("item_id") != item.get("id")
        or binding.get("theorem_id") != item.get("theorem_id")
        or binding.get("phase") != item.get("phase")
        or binding.get("prompt_sha256") != hashlib.sha256(prompt.encode()).hexdigest()
        or binding.get("objective_sha256") != hashlib.sha256(objective.encode()).hexdigest()
    ):
        raise ValueError("review binding does not close over the exact prompt and objective")
    prompt_path = RUNTIME / "prompts" / f"{claim.get('claim_id')}.txt"
    prompt_bytes, prompt_digest = read_bound_runtime_file(prompt_path, "review prompt")
    if prompt_bytes != prompt.encode() or prompt_digest != binding["prompt_sha256"]:
        raise ValueError("persisted review prompt differs from the binding closure")
    if (
        binding.get("base_revision") != manifest.get("base_revision")
        or binding.get("blueprint_sha256") != manifest.get("blueprint_sha256")
        or binding.get("theorem_dag_sha256") != manifest.get("theorem_dag_sha256")
        or binding.get("artifact_digests")
        != {row["path"]: row["sha256"] for row in role_map.get("artifacts", [])}
        or binding.get("validator_recipe_sha256s") != [validator.get("recipe_sha256")]
    ):
        raise ValueError("review binding does not bind the manifest authority inputs")
    status = worker_status(claim)
    if not isinstance(status, dict) or status.get("state") != "finished":
        raise ValueError("review status is not a finished app-server record")
    output = require_review_output(claim, status, binding)
    phase_receipt = next(
        (
            row for row in role_map.get("artifacts", [])
            if isinstance(row, dict) and row.get("role") == "phase_receipt"
        ),
        None,
    )
    if not isinstance(phase_receipt, dict) or not isinstance(phase_receipt.get("path"), str):
        raise ValueError("review role map lacks exactly one phase receipt")
    receipt_path = ROOT / str(phase_receipt["path"])
    receipt, receipt_bytes = read_exact_json_file(receipt_path, "worker phase receipt")
    receipt_verdict = receipt.get("worker_verdict", receipt.get("verdict"))
    handoff_record = provenance.get("files", {}).get("selftest_manifest")
    if not isinstance(handoff_record, dict):
        raise ValueError("review provenance lacks the worker handoff")
    handoff_encoded = handoff_record.get("content_base64")
    try:
        handoff_bytes = base64.b64decode(handoff_encoded, validate=True)
        handoff = json.loads(handoff_bytes)
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("review provenance handoff snapshot is malformed") from exc
    handoff_verdict = handoff.get("worker_verdict", handoff.get("verdict"))
    if handoff_verdict is None:
        handoff_verdict = receipt_verdict
    if (
        not isinstance(receipt_verdict, str)
        or receipt_verdict not in WORKER_VERDICTS
        or output.get("worker_verdict") != receipt_verdict
        or handoff_verdict != receipt_verdict
        or hashlib.sha256(receipt_bytes).hexdigest() != phase_receipt.get("sha256")
    ):
        raise ValueError("reviewer worker_verdict differs from immutable worker provenance")
    return output, manifest, role_map, validator, provenance


def consume_review_finished(
    data: dict[str, Any], ordered: list[dict[str, Any]], claims: list[dict[str, Any]],
    transaction: FileTransaction, *, limit: int,
) -> tuple[list[str], list[str]]:
    """Replay, decide, receipt, and CAS a bounded prefix of finished reviews."""
    by_id = {item["id"]: item for item in ordered}
    _, theorem_nodes = theorem_dag_v2()
    candidates = sorted(
        (
            claim for claim in claims
            if claim.get("lane") == REVIEW_LANE and claim.get("status") == "review_finished"
        ),
        key=lambda claim: claim_order_key(by_id.get(str(claim.get("item_id")), {}), theorem_nodes)
        if claim.get("item_id") in by_id else (sys.maxsize, sys.maxsize, ""),
    )[:limit]
    blueprint_sha256_at_start = sha256_file(BLUEPRINT)
    accepted: list[str] = []
    rejected: list[str] = []
    for claim in candidates:
        claim_transaction = FileTransaction(wal_parent=transaction)
        item = by_id.get(claim.get("item_id"))
        try:
            if item is None or item.get("state") != "[_]":
                raise ValueError("review CAS source is not the exact [_] item")
            states = {row["id"]: row["state"] for row in ordered}
            if any(states.get(dependency) != "[x]" for dependency in item.get("depends_on", [])):
                raise ValueError("master acceptance predecessor is not [x]")
            if execution_is_paused():
                fail("master acceptance refused: operator pause before replay")
            hard_status, hard_blockers = hard_edge_gate_status(
                str(item.get("theorem_id")), str(item.get("phase"))
            )
            if hard_status == "legacy_evidence_present":
                raise ValueError("legacy hard-edge evidence cannot satisfy G08 master acceptance")
            if hard_status not in {"not_applicable", "satisfied"}:
                detail = ": " + "; ".join(hard_blockers) if hard_blockers else ""
                raise ValueError(f"hard-edge master gate is not satisfied ({hard_status}){detail}")
            output, manifest, role_map, validator, _provenance = verify_review_evidence_bundle(
                item, claim
            )
            if output.get("review_verdict") != "phase_accepted":
                raise ValueError("independent review did not return typed phase_accepted")
            if execution_is_paused():
                fail("master acceptance refused: operator pause before authority replay")
            replay = acceptance_evidence.replay_validator(
                ROOT, validator, review_manifest=manifest, role_map=role_map,
                timeout_seconds=REPLAY_TIMEOUT_SECONDS,
            )
            if execution_is_paused():
                fail("master acceptance refused: operator pause after authority replay")
            decision = acceptance_evidence.evaluate_replay_semantics(
                replay,
                contract_record=phase_acceptance_contract_record(),
                review_manifest=manifest,
                role_map=role_map,
                validator_recipe=validator,
                worker_verdict=str(output["worker_verdict"]),
                review_verdict=str(output["review_verdict"]),
                audit_complete=bool(output["audit_complete"]),
                theorem_complete=bool(output["theorem_complete"]),
            )
            if execution_is_paused():
                fail("master acceptance refused: operator pause before replay publication")
            replay_path = RUNTIME / "replay-results" / f"{claim['claim_id']}.json"
            decision_path = RUNTIME / "semantic-decisions" / f"{claim['claim_id']}.json"
            replay_bytes = acceptance_evidence.canonical_json(replay) + b"\n"
            decision_bytes = acceptance_evidence.canonical_json(decision) + b"\n"
            claim_transaction.snapshot(replay_path)
            claim_transaction.snapshot(decision_path)
            claim_transaction.ensure_parent(replay_path)
            claim_transaction.ensure_parent(decision_path)
            durable_write_bytes(replay_path, replay_bytes)
            durable_write_bytes(decision_path, decision_bytes)
            claim["replay_result_path"] = str(replay_path)
            claim["replay_result_file_sha256"] = hashlib.sha256(replay_bytes).hexdigest()
            claim["semantic_decision_path"] = str(decision_path)
            claim["semantic_decision_file_sha256"] = hashlib.sha256(decision_bytes).hexdigest()
            if (
                decision.get("decision") != "phase_accepted"
                or decision.get("phase_evidence_accepted") is not True
            ):
                raise ValueError("authority replay semantics did not accept this phase")
            _receipt, receipt_bytes, receipt_sha256 = canonical_master_acceptance_receipt(
                item, claim, output, manifest, role_map, validator, replay, decision
            )
            receipt_relative = master_acceptance_receipt_path(
                item["theorem_id"], item["phase"], receipt_sha256
            )
            receipt_path = ROOT / receipt_relative
            if execution_is_paused():
                fail("master acceptance refused: operator pause before receipt publication")
            claim_transaction.snapshot(receipt_path)
            claim_transaction.ensure_parent(receipt_path)
            if receipt_path.exists() or receipt_path.is_symlink():
                existing = receipt_path.read_bytes() if receipt_path.is_file() and not receipt_path.is_symlink() else None
                if existing != receipt_bytes:
                    raise ValueError("content-addressed master receipt path conflicts")
            else:
                durable_write_bytes(receipt_path, receipt_bytes)
            if execution_is_paused():
                fail("master acceptance refused: operator pause after receipt publication")
            # Re-read the sole authority immediately before its CAS write. No
            # stale review may close an item that changed while replay ran.
            if execution_is_paused():
                fail("master acceptance refused: operator pause before SSOT CAS")
            authoritative = {row["id"]: row for row in load_blueprint_items()}
            current = authoritative.get(item["id"])
            if (
                current is None
                or current.get("state") != "[_]"
                or current.get("attempts") != item.get("attempts")
                or any(
                    authoritative.get(dependency, {}).get("state") != "[x]"
                    for dependency in item.get("depends_on", [])
                )
                or manifest.get("blueprint_sha256") != blueprint_sha256_at_start
                or sha256_file(BLUEPRINT) != blueprint_sha256_at_start
            ):
                raise ValueError("SSOT CAS source changed during master acceptance")
            item["state"] = "[x]"
            claim["status"] = "master_accepted"
            claim["master_accepted_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["master_receipt_path"] = receipt_relative
            claim["master_receipt_sha256"] = receipt_sha256
            accepted.append(item["id"])
            transaction.absorb(claim_transaction)
        except (ValueError, OSError, acceptance_evidence.EvidenceError) as exc:
            claim_transaction.rollback()
            claim["status"] = "review_failed"
            claim["review_rejected_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["review_rejection_reason"] = str(exc)
            claim["review_retry_after"] = (
                dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15)
            ).isoformat()
            rejected.append(str(claim.get("item_id")))
    if accepted:
        if execution_is_paused():
            fail("master acceptance refused: operator pause before SSOT publication")
        write_projection(data)
        write_derived_surfaces(data)
    return accepted, rejected


def refill_reviews(
    max_workers: int,
    *,
    data: dict[str, Any] | None = None,
    ordered: list[dict[str, Any]] | None = None,
    claims: list[dict[str, Any]] | None = None,
    selected_items: list[dict[str, Any]] | None = None,
    selected_slots: list[int] | None = None,
) -> int:
    """Allocate read-only scheduler-owned review /goal lanes without accepting SSOT state."""
    if data is None or ordered is None:
        data, ordered = load_dag()
    if claims is None:
        claims = refresh_claims(ordered)
    if execution_is_paused():
        return 0
    refuse_unsafe_live_identities(claims)
    active = active_lane_leases(claims)
    capacity = max(0, max_workers - len(active))
    if not capacity:
        return 0
    candidates = (
        list(selected_items)
        if selected_items is not None
        else review_candidates(ordered, claims)
    )
    if not candidates:
        return 0
    occupied_slots = {
        claim.get("slot") for claim in claims
        if isinstance(claim.get("slot"), int)
        and claim.get("status") in {
            "live", "preparing", "launch_failed", "draining", "finished", "review_finished", "quarantined",
        }
    }
    slots = (
        list(selected_slots)
        if selected_slots is not None
        else [
            slot for slot in range(1, MAX_SLOT_ID + 1) if slot not in occupied_slots
        ][: min(len(candidates), capacity)]
    )
    if (
        len(slots) != len(candidates)
        or len(slots) > capacity
        or len(slots) != len(set(slots))
        or any(slot in occupied_slots or slot < 1 or slot > MAX_SLOT_ID for slot in slots)
    ):
        fail("preselected review lanes exceed capacity or use occupied slots")
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base_revision = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    _, nodes = theorem_dag_v2()
    reservations: list[dict[str, Any]] = []
    for slot, item in zip(slots, candidates):
        if execution_is_paused():
            break
        claim_id = f"{timestamp}-{os.urandom(6).hex()}"
        implementation_claim = review_source_claim(item, claims)
        if implementation_claim is None:
            claims.append({
                "lane": REVIEW_LANE,
                "item_id": item["id"],
                "theorem_id": item["theorem_id"],
                "depends_on": item["depends_on"],
                "owned_paths": item["owned_paths"],
                "claim_id": claim_id,
                "worker_id": f"stage1app-review-{slot}-{nodes[item['theorem_id']]['v2_execution_rank']:04d}-{claim_id[-12:]}",
                "slot": slot,
                "workspace": str(RUNTIME / "review-workspaces" / f"slot{slot}"),
                "status": "review_failed",
                "claimed_at": timestamp,
                "base_revision": base_revision,
                "runtime_protocol": RUNTIME_PROTOCOL,
                "review_failure_reason": "missing or ambiguous immutable implementation provenance",
                "review_retry_after": (
                    dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15)
                ).isoformat(),
            })
            continue
        try:
            revalidation_lane = (
                post_integration_legacy_revalidation_lane(implementation_claim, item)
                if implementation_claim.get("fresh_revalidation") is True
                else claim_legacy_revalidation_lane(implementation_claim, item)
            )
            if (
                implementation_claim.get("fresh_revalidation") is True
                and revalidation_lane is None
            ):
                raise ValueError("historical review source lacks a fresh revalidation lane")
        except ValueError as exc:
            claims.append({
                    "lane": REVIEW_LANE,
                    "item_id": item["id"],
                    "theorem_id": item["theorem_id"],
                    "depends_on": item["depends_on"],
                    "owned_paths": item["owned_paths"],
                    "claim_id": claim_id,
                    "worker_id": f"stage1app-review-{slot}-{nodes[item['theorem_id']]['v2_execution_rank']:04d}-{claim_id[-12:]}",
                    "slot": slot,
                    "workspace": str(RUNTIME / "review-workspaces" / f"slot{slot}"),
                    "status": "review_failed",
                    "claimed_at": timestamp,
                    "base_revision": base_revision,
                    "runtime_protocol": RUNTIME_PROTOCOL,
                    "review_failure_reason": str(exc),
                    "review_retry_after": (
                        dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15)
                    ).isoformat(),
            })
            continue
        try:
            role_map = build_review_role_map(item, base_revision)
            validator = select_review_validator(item, base_revision)
            provenance = snapshot_review_provenance(item, implementation_claim)
            provenance_path, provenance_file_sha256 = persist_review_provenance(
                implementation_claim, provenance
            )
            review_manifest = build_scheduler_review_manifest(
                provenance, role_map, validator
            )
            review_manifest_path, review_manifest_file_sha256 = persist_review_manifest(
                claim_id, review_manifest
            )
        except (SystemExit, ValueError) as exc:
            # A malformed historical `[_]` must not stop all other reviews or
            # manufacture acceptance. Preserve a scheduler-owned negative row.
            claims.append({
                "lane": REVIEW_LANE,
                "item_id": item["id"],
                "theorem_id": item["theorem_id"],
                "depends_on": item["depends_on"],
                "owned_paths": item["owned_paths"],
                "claim_id": claim_id,
                "worker_id": f"stage1app-review-{slot}-{nodes[item['theorem_id']]['v2_execution_rank']:04d}-{claim_id[-12:]}",
                "slot": slot,
                "workspace": str(RUNTIME / "review-workspaces" / f"slot{slot}"),
                "status": "review_failed",
                "claimed_at": timestamp,
                "base_revision": base_revision,
                "runtime_protocol": RUNTIME_PROTOCOL,
                "review_failure_reason": str(exc),
                "review_retry_after": (
                    dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15)
                ).isoformat(),
            })
            continue
        objective = review_goal_objective(item)
        workspace = RUNTIME / "review-workspaces" / f"slot{slot}"
        review_input = {
            "schema_version": REVIEW_INPUT_SCHEMA,
            "review_claim_id": claim_id,
            "item": item,
            "phase_contract": phase_contract(item),
            "implementation_provenance": provenance,
            "implementation_provenance_path": str(provenance_path),
            "implementation_provenance_file_sha256": provenance_file_sha256,
            "review_manifest": review_manifest,
            "review_manifest_path": str(review_manifest_path),
            "review_manifest_file_sha256": review_manifest_file_sha256,
            "role_map": role_map,
            "validator_recipe": validator,
        }
        prompt_text = review_prompt(
            item, review_input, claim_id, workspace
        )
        binding = build_review_binding(
            claim_id, item, base_revision, prompt_text, objective, role_map, validator
        )
        prompt_path = RUNTIME / "prompts" / f"{claim_id}.txt"
        objective_path = RUNTIME / "goals" / f"{claim_id}.txt"
        output_path = RUNTIME / "logs" / f"{claim_id}.out"
        status_path = RUNTIME / "app-server" / f"{claim_id}.json"
        role_map_path = RUNTIME / "role-maps" / f"{item['id']}.json"
        review_input_path = RUNTIME / "review-inputs" / f"{claim_id}.json"
        binding_path = RUNTIME / "review-bindings" / f"{claim_id}.json"
        atomic_write(role_map_path, json.dumps(role_map, ensure_ascii=False, indent=2) + "\n")
        atomic_write(review_input_path, json.dumps(review_input, ensure_ascii=False, indent=2) + "\n")
        atomic_write(prompt_path, prompt_text)
        atomic_write(objective_path, objective + "\n")
        atomic_write(binding_path, json.dumps(binding, ensure_ascii=False, indent=2) + "\n")
        durable_unlink(status_path)
        claim = {
            "lane": REVIEW_LANE,
            "item_id": item["id"],
            "theorem_id": item["theorem_id"],
            "depends_on": item["depends_on"],
            "owned_paths": item["owned_paths"],
            "claim_id": claim_id,
            "worker_id": f"stage1app-review-{slot}-{nodes[item['theorem_id']]['v2_execution_rank']:04d}-{claim_id[-12:]}",
            "slot": slot,
            "workspace": str(workspace),
            "status": "preparing",
            "pid": None,
            "claimed_at": timestamp,
            "base_revision": base_revision,
            "output_log": str(output_path),
            "runtime_protocol": RUNTIME_PROTOCOL,
            "app_server_status": str(status_path),
            "goal_objective_path": str(objective_path),
            "goal_objective": objective,
            "runtime_config": dict(REQUIRED_RUNTIME_CONFIG),
            "review_role_map_path": str(role_map_path),
            "review_input_path": str(review_input_path),
            "review_input_sha256": sha256_file(review_input_path),
            "review_provenance_path": str(provenance_path),
            "review_provenance_sha256": provenance_file_sha256,
            "review_manifest_path": str(review_manifest_path),
            "review_manifest_file_sha256": review_manifest_file_sha256,
            "review_manifest_sha256": review_manifest["manifest_sha256"],
            "review_binding_path": str(binding_path),
            "review_binding_file_sha256": sha256_file(binding_path),
            "review_binding_sha256": hashlib.sha256(
                json.dumps(binding, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
            ).hexdigest(),
            "validator_recipe": validator,
        }
        claims.append(claim)
        reservations.append(claim)
        if len(reservations) >= capacity:
            break
    save_claims(claims)
    started: list[dict[str, Any]] = []
    def cancel_reviews_for_pause(start_index: int) -> None:
        now = dt.datetime.now(dt.timezone.utc).isoformat()
        for pending in reservations[start_index:]:
            if pending.get("status") == "preparing":
                pending["status"] = "cancelled"
                pending["cancelled_at"] = now
                pending["cancel_reason"] = "operator pause observed before review launch"
        save_claims(claims)

    for index, claim in enumerate(reservations):
        if execution_is_paused():
            cancel_reviews_for_pause(index)
            break
        try:
            workspace = prepare_review_workspace(int(claim["slot"]), str(claim["base_revision"]))
            prompt_path = RUNTIME / "prompts" / f"{claim['claim_id']}.txt"
            if execution_is_paused():
                cancel_reviews_for_pause(index)
                break
            claim["pid"] = launch_app_server_worker(
                worker_argv(
                    workspace,
                    prompt_path,
                    Path(str(claim["output_log"])),
                    Path(str(claim["app_server_status"])),
                    Path(str(claim["goal_objective_path"])),
                    lane=REVIEW_LANE,
                    binding_path=Path(str(claim["review_binding_path"])),
                )
            )
            claim["pid_start_ticks"] = process_start_ticks(claim["pid"])
            if claim["pid_start_ticks"] is None:
                raise RuntimeError("launched review client lacks a stable /proc identity")
            claim["client_started_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            started.append(claim)
        except BaseException as exc:
            claim["status"] = "launch_failed"
            claim["launch_error"] = str(exc)
        save_claims(claims)
    return confirm_goal_handshakes(claims, started) if started else 0


def refill_workers(max_workers: int) -> int:
    """Reconcile and refill lanes without running heavyweight integration."""
    data, ordered = load_dag()
    claims = refresh_claims(ordered)
    claims = enforce_worker_cap(claims, max_workers)
    space_guard(claims)
    if execution_is_paused():
        print("tick: Stage1 execution paused during this tick; refill skipped")
        write_todo(data, ordered, claims)
        return 0
    refuse_unsafe_live_identities(claims)
    active_leases = active_lane_leases(claims)
    # Finished handoffs retain their clones until integration, but they do not
    # consume live-worker capacity. Their occupied slot numbers are skipped
    # while fresh, otherwise-unused slot numbers refill the requested lanes.
    slot_reservations = [
        claim
        for claim in claims
        if claim.get("runtime_protocol") == RUNTIME_PROTOCOL
        and claim.get("status") in {
            "live", "finished", "review_finished", "preparing", "launch_failed",
            "draining", "quarantined",
        }
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
    capacity = max(0, max_workers - len(active_leases))
    available_slots = [
        slot
        for slot in range(1, MAX_SLOT_ID + 1)
        if slot not in occupied_slots
    ][:capacity]
    if capacity <= 0:
        print(
            f"tick: saturated ({len(active_leases)} active/{max_workers} slots, "
            f"{len(slot_reservations) - len(active_leases)} handoff pending)"
        )
        write_todo(data, ordered, claims)
        return 0
    # Both lane types share one ordered frontier; truncate only after sorting.
    _, theorem_nodes = theorem_dag_v2()
    selected_records = unified_lane_candidates(ordered, claims)[:capacity]
    allocated = [
        {**record, "slot": slot}
        for record, slot in zip(selected_records, available_slots)
    ]
    if not allocated:
        print("tick: no unclaimed implementation or review work")
        write_todo(data, ordered, claims)
        return 0
    review_allocations = [record for record in allocated if record["lane"] == REVIEW_LANE]
    implementation_allocations = [
        record for record in allocated if record["lane"] == IMPLEMENTATION_LANE
    ]
    launched_reviews = refill_reviews(
        max_workers,
        data=data,
        ordered=ordered,
        claims=claims,
        selected_items=[record["item"] for record in review_allocations],
        selected_slots=[record["slot"] for record in review_allocations],
    )
    if execution_is_paused():
        write_todo(data, ordered, claims)
        return launched_reviews
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    claim_graph_sha256 = graph_sha256()
    base_revision = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    needs_revalidation_binding = any(
        allocation["item"].get("state") == "[_]"
        for allocation in implementation_allocations
    )
    revalidation_lanes, revalidation_plan_binding = (
        legacy_revalidation_plan() if needs_revalidation_binding else ({}, None)
    )
    reservations: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for allocation in implementation_allocations:
        slot = int(allocation["slot"])
        item = allocation["item"]
        claim_id = f"{timestamp}-{os.urandom(6).hex()}"
        workspace = RUNTIME / "workers" / f"slot{slot}"
        prompt = RUNTIME / "prompts" / f"{claim_id}.txt"
        output = RUNTIME / "logs" / f"{claim_id}.out"
        worker_id = f"stage1app-impl-{slot}-{theorem_nodes[item['theorem_id']]['v2_execution_rank']:04d}-{claim_id[-12:]}"
        status_path = RUNTIME / "app-server" / f"{claim_id}.json"
        objective_path = RUNTIME / "goals" / f"{claim_id}.txt"
        objective = worker_goal_objective(item)
        claim = {
            "lane": IMPLEMENTATION_LANE,
            "item_id": item["id"], "theorem_id": item["theorem_id"], "depends_on": item["depends_on"],
            "owned_paths": item["owned_paths"], "claim_id": claim_id, "worker_id": worker_id,
            "slot": slot, "workspace": str(workspace),
            "status": "preparing", "pid": None, "claimed_at": timestamp,
            "retry_count": sum(1 for claim in claims if claim.get("item_id") == item["id"]),
            "base_revision": base_revision, "output_log": str(output),
            "runtime_protocol": RUNTIME_PROTOCOL,
            "app_server_status": str(status_path),
            "goal_objective_path": str(objective_path),
            "goal_objective": objective,
            "runtime_config": {
                "model": CODEX_MODEL,
                "reasoning_effort": CODEX_REASONING_EFFORT,
                "service_tier": CODEX_SERVICE_TIER,
            },
            "theorem_dag_sha256": claim_graph_sha256,
            "dependency_context_sha256": theorem_nodes[item["theorem_id"]].get("dependency_context_sha256"),
            "fresh_revalidation": item["state"] == "[_]",
        }
        if item["state"] == "[_]":
            lane = revalidation_lanes.get(item["id"])
            if lane is None or revalidation_plan_binding is None:
                fail("historical item allocation lacks its content-bound revalidation plan")
            claim["legacy_revalidation_lane"] = lane
            claim["legacy_revalidation_lane_sha256"] = lane["lane_sha256"]
            claim["legacy_revalidation_plan_sha256"] = revalidation_plan_binding[
                "plan_sha256"
            ]
            claim["legacy_revalidation_plan_file_sha256"] = revalidation_plan_binding[
                "plan_file_sha256"
            ]
            claim["legacy_revalidation_plan_binding"] = revalidation_plan_binding
            claim["legacy_revalidation_plan_binding_sha256"] = canonical_json_sha256(
                revalidation_plan_binding
            )
        claims.append(claim)
        reservations.append((claim, item))
    # Persist all leases before creating or replacing a clone/process. A crash
    # can now leave only a recoverable preparing row, never an unowned worker.
    save_claims(claims)
    started: list[dict[str, Any]] = []

    def cancel_unstarted_for_pause() -> None:
        now = dt.datetime.now(dt.timezone.utc).isoformat()
        started_ids = {started_claim.get("claim_id") for started_claim in started}
        for pending_claim, _ in reservations:
            if (
                pending_claim.get("status") == "preparing"
                and pending_claim.get("claim_id") not in started_ids
            ):
                pending_claim["status"] = "cancelled"
                pending_claim["cancelled_at"] = now
                pending_claim["cancel_reason"] = "operator pause observed before launch"
        save_claims(claims)

    for claim, item in reservations:
        if execution_is_paused():
            cancel_unstarted_for_pause()
            break
        workspace = Path(claim["workspace"])
        prompt = RUNTIME / "prompts" / f"{claim['claim_id']}.txt"
        output = Path(claim["output_log"])
        status_path = Path(str(claim["app_server_status"]))
        objective_path = Path(str(claim["goal_objective_path"]))
        try:
            prepare_workspace(int(claim["slot"]))
            prompt.parent.mkdir(parents=True, exist_ok=True)
            output.parent.mkdir(parents=True, exist_ok=True)
            atomic_write(prompt, task_prompt(item, workspace))
            atomic_write(objective_path, str(claim["goal_objective"]) + "\n")
            durable_unlink(status_path)
            if execution_is_paused():
                cancel_unstarted_for_pause()
                break
            claim["pid"] = launch_app_server_worker(
                worker_argv(workspace, prompt, output, status_path, objective_path)
            )
            claim["pid_start_ticks"] = process_start_ticks(claim["pid"])
            if claim["pid_start_ticks"] is None:
                raise RuntimeError("launched app-server client lacks a stable /proc identity")
            claim["client_started_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            started.append(claim)
        except BaseException as exc:
            # Persist a failed reservation before propagating. On the next
            # tick it cannot be mistaken for a free slot or live worker.
            claim["status"] = "launch_failed"
            claim["launch_failed_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["launch_error"] = str(exc)
            save_claims(claims)
            continue
        save_claims(claims)
    launched = confirm_goal_handshakes(claims, started) if started else 0
    todo = write_todo(data, ordered, claims)
    failed = sum(claim.get("status") == "launch_failed" for claim, _ in reservations)
    print(
        f"tick: verified {launched} implementation and {launched_reviews} review app-server /goal lane(s), "
        f"failed={failed}, active={len(active_leases) + launched}/{max_workers}, todo={todo.relative_to(ROOT)}"
    )
    return launched + launched_reviews


def launch(max_workers: int, integration_limit: int = DEFAULT_INTEGRATION_LIMIT) -> None:
    """Run one bounded tick with independent refill and integration budgets."""
    if max_workers < 0 or max_workers > MAX_WORKERS:
        fail(f"--workers must be in 0..{MAX_WORKERS}")
    if integration_limit < 0 or integration_limit > MAX_INTEGRATION_LIMIT:
        fail(f"--limit must be in 0..{MAX_INTEGRATION_LIMIT}")
    if execution_is_paused():
        print("tick: Stage1 execution is paused; no sync, integration, or refill performed")
        return
    # Sync and crash recovery are safety prerequisites. Refill comes before the
    # heavyweight integration/checkpoint cursor so every five-minute tick can
    # restore live capacity without waiting for validation, commit, or push.
    recover_integration_wal()
    pending = runtime_path("pending_checkpoint.json")
    if pending.exists():
        checkpoint_sync_guard()
        # The authoritative worktree may contain integrated bytes that are not
        # yet in HEAD.  Commit/push that exact manifest before cloning a worker;
        # otherwise a refill clone could silently receive stale task state.
        checkpoint_integration()
        if execution_is_paused():
            print("tick: Stage1 execution paused after checkpoint; refill skipped")
            return
    else:
        sync_guard()
    refill_workers(max_workers)
    if execution_is_paused():
        print("tick: Stage1 execution paused after refill; integration skipped")
        return
    integrated = integrate(integration_limit)
    if integrated:
        checkpoint_integration()


def restart_live_workers(max_workers: int) -> None:
    """Restart live claims in place after a scheduler runtime-policy change.

    A worker clone can contain useful, uncommitted progress.  Reusing the same
    clone keeps that progress available to the restarted Codex process while
    changing only the runtime configuration.  Finished handoffs are left for
    the normal integration path and are never restarted.
    """
    if max_workers < 0 or max_workers > MAX_WORKERS:
        fail(f"--workers must be in 0..{MAX_WORKERS}")
    if execution_is_paused():
        fail("restart refused: Stage1 execution is paused")
    sync_guard()
    data, ordered = load_dag()
    claims = refresh_claims(ordered)
    by_id = {item["id"]: item for item in ordered}
    live = [
        claim
        for claim in claims
        if claim.get("runtime_protocol") == RUNTIME_PROTOCOL
        and claim.get("status") == "live"
        and int(claim.get("slot", 0)) <= max_workers
    ]
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    restarted = 0
    _, theorem_nodes = theorem_dag_v2()
    for claim in live:
        item = by_id.get(claim.get("item_id"))
        workspace = Path(str(claim.get("workspace", "")))
        slot = claim.get("slot")
        if item is None or not isinstance(slot, int) or not workspace.is_dir():
            fail(f"cannot safely restart malformed live claim: {claim.get('item_id')}")
        previous_status = worker_status(claim)
        thread_id = previous_status.get("thread_id") if isinstance(previous_status, dict) else None
        previous_goal = previous_status.get("goal") if isinstance(previous_status, dict) else None
        objective = claim.get("goal_objective")
        if (
            not isinstance(thread_id, str)
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,199}", thread_id) is None
            or not isinstance(previous_goal, dict)
            or previous_goal.get("threadId") != thread_id
            or previous_goal.get("objective") != objective
            or previous_goal.get("status") != "active"
            or not isinstance(objective, str)
            or not objective
        ):
            fail(f"cannot resume live claim without its exact active thread/goal: {claim.get('item_id')}")
        if not app_server_worker_is_live(claim) or not terminate_app_server_worker(claim):
            fail(f"cannot safely stop live app-server claim: {claim.get('item_id')}")
        claim_id = f"{timestamp}-{os.urandom(6).hex()}"
        worker_id = f"stage1app-impl-{slot}-{theorem_nodes[item['theorem_id']]['v2_execution_rank']:04d}-{claim_id[-12:]}"
        prompt = RUNTIME / "prompts" / f"{claim_id}.txt"
        output = RUNTIME / "logs" / f"{claim_id}.out"
        status_path = RUNTIME / "app-server" / f"{claim_id}.json"
        objective_path = RUNTIME / "goals" / f"{claim_id}.txt"
        atomic_write(prompt, task_prompt(item, workspace))
        atomic_write(objective_path, objective + "\n")
        durable_unlink(status_path)
        previous = {
            "claim_id": claim.get("claim_id"),
            "worker_id": claim.get("worker_id"),
            "pid": claim.get("pid"),
            "pid_start_ticks": claim.get("pid_start_ticks"),
            "app_server_status": claim.get("app_server_status"),
            "thread_id": thread_id,
            "goal": previous_goal,
        }
        claim.update(
            claim_id=claim_id,
            worker_id=worker_id,
            output_log=str(output),
            app_server_status=str(status_path),
            goal_objective_path=str(objective_path),
            goal_objective=objective,
            status="preparing",
            previous_runtime=previous,
        )
        save_claims(claims)
        claim["pid"] = launch_app_server_worker(
            worker_argv(
                workspace, prompt, output, status_path, objective_path,
                thread_id=thread_id,
            )
        )
        claim["pid_start_ticks"] = process_start_ticks(claim["pid"])
        if claim["pid_start_ticks"] is None:
            claim["status"] = "launch_failed"
            save_claims(claims)
            fail(f"restarted app-server client lacks a stable /proc identity: {claim.get('item_id')}")
        claim["client_started_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        claim["runtime_config"] = {
            "model": CODEX_MODEL,
            "reasoning_effort": CODEX_REASONING_EFFORT,
            "service_tier": CODEX_SERVICE_TIER,
        }
        claim["theorem_dag_sha256"] = graph_sha256()
        claim["dependency_context_sha256"] = theorem_nodes[item["theorem_id"]].get("dependency_context_sha256")
        save_claims(claims)
        if confirm_goal_handshakes(claims, [claim]) != 1:
            fail(f"restarted app-server client failed its /goal handshake: {claim.get('item_id')}")
        claim["restarted_at"] = timestamp
        restarted += 1
        save_claims(claims)
    save_claims(claims)
    write_todo(data, ordered, claims)
    print(f"restart: restarted {restarted} app-server /goal worker(s) with service_tier={CODEX_SERVICE_TIER}")


def cleanup() -> None:
    data, ordered = load_dag()
    claims = refresh_claims(ordered)
    counts = Counter(item["state"] for item in ordered)
    todo = DOCS / f"todos_{dt.date.today():%Y%m%d}.md"
    unfinished_zero = todo.exists() and "Unfinished: 0" in todo.read_text(encoding="utf-8")
    runtime_claims = [
        claim
        for claim in claims
        if claim.get("runtime_protocol") == RUNTIME_PROTOCOL
        and claim.get("status") in {"live", "preparing", "launch_failed", "draining", "finished", "blocked", "quarantined"}
    ]
    if counts["[ ]"] or counts["[_]"] or runtime_claims or not unfinished_zero:
        fail("cleanup refused: unfinished work, active/pending claims, or stale todo remains")
    cron = run(["crontab", "-l"], check=False)
    lines = [line for line in cron.stdout.splitlines() if "stage1_execution_cron.py" not in line]
    subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", text=True, check=True)
    atomic_write(runtime_path("cleanup.json"), json.dumps({"state": "completed", "at": dt.datetime.now(dt.timezone.utc).isoformat()}, indent=2) + "\n")
    print("cleanup: removed Stage1 execution cron entry")


def install(schedule: str) -> None:
    if execution_is_paused():
        fail("install refused: Stage1 execution is paused; use --resume explicitly first")
    if not re.fullmatch(r"[^\n]+", schedule):
        fail("schedule must be one crontab line prefix")
    command = (
        f"{schedule} cd {ROOT} && "
        f"{sys.executable} {ROOT / 'scripts' / 'stage1_execution_cron.py'} "
        f"--tick --workers {DEFAULT_WORKERS} --limit {DEFAULT_INTEGRATION_LIMIT} "
        f">> {RUNTIME / 'keepalive.log'} 2>&1 # stage1_execution_cron.py"
    )
    current = run(["crontab", "-l"], check=False).stdout.splitlines()
    current = [line for line in current if "stage1_execution_cron.py" not in line]
    subprocess.run(["crontab", "-"], input="\n".join(current + [command]) + "\n", text=True, check=True)
    print("install: cron entry installed")


def pause() -> None:
    """Persistently stop scheduling before any future tick can mutate state."""
    validate_runtime_root()
    marker = dt.datetime.now(dt.timezone.utc).isoformat() + "\n"
    for path in pause_markers():
        path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(path, marker)
    cron = run(["crontab", "-l"], check=False)
    lines = [line for line in cron.stdout.splitlines() if "stage1_execution_cron.py" not in line]
    subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", text=True, check=True)
    # Wait for any in-flight tick to observe PAUSED and finish (or roll its WAL
    # back) before confirming the stop to the operator.
    with runtime_path("scheduler.lock").open("w", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
    print("pause: persisted PAUSED state and removed the Stage1 cron entry; live app-server workers were left to stop naturally")


def resume() -> None:
    """Clear the persistent pause without implicitly installing a cron."""
    validate_runtime_root()
    cron = run(["crontab", "-l"], check=False)
    if any("stage1_execution_cron.py" in line for line in cron.stdout.splitlines()):
        fail("resume refused: a Stage1 cron entry already exists")
    for path in pause_markers():
        durable_unlink(path)
    print("resume: cleared current and legacy PAUSED state; cron remains uninstalled")


def main() -> None:
    validate_only_requested = "--validate-only" in sys.argv[1:]
    # A paused tick must be a true no-op, including no runtime directory or
    # lock-file mutation. Check it before constructing the scheduler lock.
    # The one allowed migration is copying the retired stop marker into the
    # current runtime; this preserves rather than relaxes the operator freeze.
    if not validate_only_requested:
        migrate_pause_marker()
    if "--tick" in sys.argv[1:] and execution_is_paused():
        print("tick: Stage1 execution is paused; no sync, integration, or refill performed")
        return
    # A pause request must never be dropped behind an active scheduler lock.
    # Persist the stop intent and remove the refill entry immediately; any
    # in-flight tick observes PAUSED before launching a new worker below.
    if "--pause" in sys.argv[1:]:
        pause()
        return
    paused_mutating_modes = {"--bootstrap", "--integrate", "--cleanup", "--restart-live", "--install"}
    requested_paused_modes = paused_mutating_modes.intersection(sys.argv[1:])
    if execution_is_paused() and requested_paused_modes:
        fail(f"Stage1 execution is paused; refused {sorted(requested_paused_modes)[0]}")
    lock = None
    if not validate_only_requested:
        # A refill can take longer than its five-minute cadence. Serialize all
        # mutating scheduler invocations so overlapping ticks cannot allocate
        # the same slot or orphan an unrecorded app-server worker. Validate-only
        # deliberately avoids creating or touching this lock.
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
    modes.add_argument("--validate-only", action="store_true", help="read-only validation of DAG, state, runtime configuration, and the daily todo projection")
    modes.add_argument("--integrate", action="store_true", help="verify completed worker handoffs and advance them to worker-self-tested")
    modes.add_argument("--tick", action="store_true", help="sync, refill the app-server /goal worker lanes, and refresh todo")
    modes.add_argument("--cleanup", action="store_true", help="remove the cron entry only after every completion gate is true")
    modes.add_argument("--restart-live", action="store_true", help="restart live workers in place using the current scheduler runtime policy")
    modes.add_argument("--install", action="store_true", help="install a bounded scheduler cron entry")
    modes.add_argument("--pause", action="store_true", help="persistently disable ticks and remove the cron entry")
    modes.add_argument("--resume", action="store_true", help="clear the persistent pause without installing cron")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help=f"concurrent-worker refill budget (0..{MAX_WORKERS}; default {DEFAULT_WORKERS})")
    parser.add_argument("--limit", type=int, default=DEFAULT_INTEGRATION_LIMIT, help=f"handoff integration budget (0..{MAX_INTEGRATION_LIMIT}; default {DEFAULT_INTEGRATION_LIMIT})")
    parser.add_argument("--schedule", default="*/5 * * * *", help="crontab schedule used by --install")
    args = parser.parse_args()
    if args.bootstrap:
        bootstrap()
    elif args.validate_only:
        validate_only()
    elif args.integrate:
        integrate(args.limit)
    elif args.tick:
        launch(args.workers, args.limit)
    elif args.cleanup:
        cleanup()
    elif args.restart_live:
        restart_live_workers(args.workers)
    elif args.pause:
        pause()
    elif args.resume:
        resume()
    else:
        install(args.schedule)
    if lock is not None:
        lock.close()


if __name__ == "__main__":
    main()
