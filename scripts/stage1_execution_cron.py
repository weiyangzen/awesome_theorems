#!/usr/bin/env python3
"""Run the Stage1 v2 Lean 4 execution queue safely.

``Docs/Stage1_Blueprint_v2.md`` is the single writable requirements and task-
state authority. Its generated checklist is projected into the typed
``Docs/Stage1_Phase_DAG_v2.json`` and the daily todo snapshot; neither
projection may feed state back into the blueprint.

This program owns its app-server state below `.cron/stage1-v2-app-server/`,
which is gitignored. A worker never writes an accepted state: it produces a
self-test manifest and its isolated clone is queued for the integration owner.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import datetime as dt
import errno
import fcntl
import functools
import hashlib
import json
import math
import os
import pwd
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import uuid
from collections import Counter, deque
from typing import Any, Callable, NoReturn

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

try:
    import stage1_focus_eligibility as focus_eligibility
except ModuleNotFoundError:  # Support importlib-based focused tests from repo root.
    import importlib.util

    _FOCUS_PATH = Path(__file__).with_name("stage1_focus_eligibility.py")
    _FOCUS_SPEC = importlib.util.spec_from_file_location(
        "stage1_focus_eligibility", _FOCUS_PATH
    )
    if _FOCUS_SPEC is None or _FOCUS_SPEC.loader is None:
        raise
    focus_eligibility = importlib.util.module_from_spec(_FOCUS_SPEC)
    sys.modules[_FOCUS_SPEC.name] = focus_eligibility
    _FOCUS_SPEC.loader.exec_module(focus_eligibility)

try:
    import stage1_focus_admission as focus_admission
except ModuleNotFoundError:  # Support importlib-based focused tests from repo root.
    import importlib.util

    _ADMISSION_PATH = Path(__file__).with_name("stage1_focus_admission.py")
    _ADMISSION_SPEC = importlib.util.spec_from_file_location(
        "stage1_focus_admission", _ADMISSION_PATH
    )
    if _ADMISSION_SPEC is None or _ADMISSION_SPEC.loader is None:
        raise
    focus_admission = importlib.util.module_from_spec(_ADMISSION_SPEC)
    sys.modules[_ADMISSION_SPEC.name] = focus_admission
    _ADMISSION_SPEC.loader.exec_module(focus_admission)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "Docs"
BLUEPRINT = DOCS / "Stage1_Blueprint_v2.md"
TARGETS = DOCS / "Stage1_Target_Membership_v2.json"
DAG = DOCS / "Stage1_Phase_DAG_v2.json"
THEOREM_DAG_V2 = DOCS / "Stage1_Theorem_DAG_v2.json"
FOCUS_ELIGIBILITY_SCHEMA = DOCS / "Stage1_Focus_Eligibility_Schema.json"
PHASE_ACCEPTANCE_CONTRACTS = DOCS / "Stage1_Phase_Acceptance_Contracts.json"
PHASE_ACCEPTANCE_CONTRACT_SHA256 = (
    "d7fdb80f50d87b7a3c2dd570c0dd8a269fae951751ab8f5ea5ec448431d57e72"
)
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
    (
        "proof",
        "Integrate and replay the admitted exact machine proof; new root proof content requires an active frontier exception.",
    ),
    ("validation", "Run hermetic kernel, trust, provenance, and independent validation gates."),
    ("release", "Reconcile evidence and decide the exact theorem-completion verdict."),
)
FOCUS_DELIVERABLES = {
    "organize_or_integrate": {
        "intake": "Bind the exact human theorem and its already-existing machine proof candidate.",
        "statement": "Elaborate the exact repository target needed to match the existing machine proof.",
        "anchor_audit": "Content-bind and independently replay the exact external or pinned machine proof.",
        "obligation_tree": "Freeze only the repository-local integration, transport, provenance, and acceptance obligations.",
        "proof": "Pin, import, wrap, or checked-transport the admitted existing machine proof without inventing root mathematics.",
        "validation": "Replay the integrated existing proof under the pinned kernel, trust, provenance, and independence gates.",
        "release": "Reconcile the accepted integration evidence and exact theorem-completion verdict.",
    },
    "frontier_exception": {
        "intake": "Bind the exact human theorem and the bounded negative machine-proof search.",
        "statement": "Elaborate the exact repository target authorized by the frontier lease.",
        "anchor_audit": "Confirm the bounded negative search and every frontier-admission input.",
        "obligation_tree": "Freeze only the root obligations and milestones authorized by the active frontier lease.",
        "proof": "Attempt the exact new root proof only within the active reviewed frontier lease, budget, and stop conditions.",
        "validation": "Validate the leased frontier result without widening its target or resource authority.",
        "release": "Reconcile the bounded frontier evidence and exact theorem-completion verdict.",
    },
    "research_required": {
        "intake": "Audit the exact human claim, source boundary, and formal-proof discovery scope.",
        "statement": "Elaborate the exact target for evidence matching without constructing its proof.",
        "anchor_audit": "Search and content-bind exact existing machine-proof candidates without constructing a proof.",
    },
}
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
        "consumer_kernel_replay",
    ],
    "provider_checkbox_state_is_observation_only": True,
    "provider_acceptance_inherited": False,
    "consumer_acceptance_required": True,
}
# The operator-facing lane/refill/concurrency setting is currently zero.
# Existing process-backed workers are grandfathered and may finish naturally.
MAX_WORKERS = 0
DEFAULT_WORKERS = 0
MAX_INTEGRATION_LIMIT = 0
DEFAULT_INTEGRATION_LIMIT = 0
MAX_SLOT_ID = 1546 * len(PHASES)
CLAIM_ID_RE = re.compile(r"[0-9]{8}T[0-9]{6}Z-[0-9a-f]{12}")
GOAL_HANDSHAKE_TIMEOUT_SECONDS = 30.0
FOCUS_REVIEW_TIMEOUT_SECONDS = 3600.0
GOAL_HANDSHAKE_POLL_SECONDS = 0.1
GOAL_HANDSHAKE_RECOVERY_GRACE_SECONDS = 120.0
# Concurrent app-server processes share Codex's ~/.codex SQLite state. When
# allocation is enabled, start each bounded cohort at a controlled cadence.
APP_SERVER_LAUNCH_STAGGER_SECONDS = 0.2
# A five-minute scheduler cadence must not turn one refill into an unbounded
# retry loop.  The pre-integration cohort gets three measured attempts within
# three minutes; the post-integration tail gets one attempt before exit.
PRE_INTEGRATION_REFILL_ROUNDS = 3
PRE_INTEGRATION_REFILL_DEADLINE_SECONDS = 180.0
TAIL_REFILL_DEADLINE_SECONDS = 60.0
REFILL_RETRY_SETTLE_SECONDS = 1.0
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
REVIEW_BINDING_SCHEMA = "stage1-app-server-review-binding/1.2"
REVIEW_OUTPUT_SCHEMA = "stage1-master-review-output/1.1"
ROLE_MAP_SCHEMA = "stage1-phase-artifact-role-map/1.0"
MASTER_ACCEPTANCE_RECEIPT_SCHEMA = "stage1-master-phase-acceptance/1.0"
WORKER_PROVENANCE_SCHEMA = "stage1-worker-review-provenance/1.0"
WORKER_HANDOFF_ARCHIVE_SCHEMA = "stage1-worker-handoff-archive/1.0"
MAX_WORKER_HANDOFF_BYTES = 4 * 1024 * 1024
REVIEW_INPUT_SCHEMA = "stage1-scheduler-review-input/1.0"
FOCUS_REVIEW_JOB_SCHEMA = "stage1-focus-review-job/1.0"
FOCUS_REVIEW_RESULT_SCHEMA = "stage1-focus-review-result/1.0"
REVIEW_ACL_SNAPSHOT_SCHEMA = "stage1-review-acl-snapshot/1.0"
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
    "validator_recipe_sha256s", "focus_review",
}
FOCUS_EXECUTION_FIELDS = {
    "focus_contract_sha256", "execution_disposition", "receipt_sha256",
}
INTEGRATION_ONLY_FOCUS_EXECUTION_FIELDS = FOCUS_EXECUTION_FIELDS | {
    "machine_evidence_class", "exact_machine_source", "exact_machine_source_used",
    "introduced_root_critical_proof",
}
FRONTIER_RUNTIME_LEDGER_SCHEMA = "stage1-frontier-runtime-ledger/1.0"
FRONTIER_SCRATCH_DIRECTORY = "frontier-scratch"
FRONTIER_VALIDATOR_TIMEOUT_SECONDS = 60.0
FRONTIER_VALIDATOR_MAX_OUTPUT_BYTES = 256 * 1024
FRONTIER_VALIDATOR_RESULT_SCHEMA = "stage1-frontier-validator-result/1.0"


class FrontierPolicyStop(ValueError):
    def __init__(self, condition: str, message: str) -> None:
        super().__init__(message)
        self.condition = condition
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
REQUIRED_FRONTIER_TURN_SANDBOX_BASE = {
    "type": "workspaceWrite",
    "networkAccess": False,
    "excludeTmpdirEnvVar": False,
    # A frontier process may write only its clone and scheduler-owned TMPDIR.
    # Generic /tmp would be outside resource accounting and is therefore denied.
    "excludeSlashTmp": True,
}
REQUIRED_REVIEW_SANDBOX_CONTRACT = {"type": "readOnly", "networkAccess": False}
# Compatibility name retained for implementation-lane callers and tests.
REQUIRED_SANDBOX_CONTRACT = REQUIRED_IMPLEMENTATION_SANDBOX_CONTRACT
PAUSE_FILE = RUNTIME / "PAUSED"
APP_SERVER_CLIENT = ROOT / "scripts" / "stage1_app_server_client.py"
PROC_ROOT = Path("/proc")
RUNTIME_PROTOCOL = "codex-app-server-jsonl"
UNSUPPORTED_RUNTIME_CLAIM_FIELDS = frozenset({
    "fresh_revalidation",
    "legacy_revalidation_lane",
    "legacy_revalidation_lane_sha256",
    "legacy_revalidation_plan_binding",
    "legacy_revalidation_plan_binding_sha256",
    "legacy_revalidation_plan_file_sha256",
    "legacy_revalidation_plan_sha256",
})


def focus_decision_for_item(
    item: dict[str, Any],
    theorem_nodes: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Reload and compare the scheduler's read-only focus projection.

    The theorem DAG is not an admission authority.  It is a content-bound
    projection of the target-owned receipt, so both views must agree exactly.
    A missing receipt is the one policy-defined bootstrap state and can admit
    only intake through anchor audit; malformed or stale evidence admits no
    phase.
    """
    theorem_id = item.get("theorem_id")
    phase = item.get("phase")
    if not isinstance(theorem_id, str) or phase not in PHASE_NAMES:
        raise ValueError("focus eligibility item identity is malformed")
    if theorem_nodes is None:
        _, theorem_nodes = theorem_dag_v2()
    node = theorem_nodes.get(theorem_id)
    projection = node.get("focus_eligibility") if isinstance(node, dict) else None
    if not isinstance(projection, dict):
        raise ValueError("focus eligibility DAG projection is missing or malformed")
    expected_digest = projection.get("receipt_sha256")
    if expected_digest is not None and (
        not isinstance(expected_digest, str)
        or re.fullmatch(r"[0-9a-f]{64}", expected_digest) is None
    ):
        raise ValueError("focus eligibility DAG receipt digest is malformed")
    decision = focus_eligibility.load_focus_eligibility(
        ROOT,
        theorem_id,
        expected_projection_sha256=expected_digest,
    )
    if decision != projection:
        raise ValueError("focus eligibility DAG projection is stale or disagrees with receipt")
    return decision


def item_focus_phase_allowed(
    item: dict[str, Any],
    theorem_nodes: dict[str, dict[str, Any]] | None = None,
) -> bool:
    """Return False, never optimistic, for any eligibility validation error."""
    try:
        decision = focus_decision_for_item(item, theorem_nodes)
    except (OSError, ValueError, focus_eligibility.EligibilityError):
        return False
    return focus_eligibility.phase_allowed(decision, str(item.get("phase", "")))


def require_item_focus_phase_allowed(
    item: dict[str, Any],
    theorem_nodes: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Enforce eligibility again at an irreversible scheduler boundary."""
    try:
        decision = focus_decision_for_item(item, theorem_nodes)
        focus_eligibility.require_phase_allowed(decision, str(item.get("phase", "")))
    except (OSError, ValueError, focus_eligibility.EligibilityError) as exc:
        raise ValueError(f"focus eligibility gate refused {item.get('id')}: {exc}") from exc
    return decision


def focus_contract_sha256(decision: dict[str, Any]) -> str:
    """Return the canonical digest used at every focus handoff boundary."""
    return hashlib.sha256(
        json.dumps(
            decision, ensure_ascii=True, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def _focus_receipt(decision: dict[str, Any]) -> dict[str, Any]:
    """Reload the validated receipt bytes without trusting a projected summary."""
    relative = decision.get("receipt_path")
    expected = decision.get("receipt_sha256")
    if (
        decision.get("valid") is not True
        or not isinstance(relative, str)
        or Path(relative).is_absolute()
        or ".." in Path(relative).parts
        or not isinstance(expected, str)
        or re.fullmatch(r"[0-9a-f]{64}", expected) is None
    ):
        raise ValueError("focus execution contract lacks a valid receipt binding")
    path = ROOT / relative
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise ValueError("focus receipt is missing or unsafe") from exc
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size <= 0:
            raise ValueError("focus receipt is not a regular nonempty file")
        payload = b""
        while len(payload) < metadata.st_size:
            block = os.read(descriptor, min(1024 * 1024, metadata.st_size - len(payload)))
            if not block:
                raise ValueError("focus receipt was truncated while reading")
            payload += block
        if os.read(descriptor, 1):
            raise ValueError("focus receipt grew while reading")
    finally:
        os.close(descriptor)
    if hashlib.sha256(payload).hexdigest() != expected:
        raise ValueError("focus receipt changed after eligibility validation")
    try:
        receipt = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("focus receipt is not UTF-8 JSON") from exc
    if not isinstance(receipt, dict):
        raise ValueError("focus receipt is not a JSON object")
    return receipt


def focus_execution_contract(
    item: dict[str, Any],
    theorem_nodes: dict[str, dict[str, Any]] | None = None,
    *,
    decision: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the typed focus contract a worker and reviewer must preserve."""
    current = decision or require_item_focus_phase_allowed(item, theorem_nodes)
    focus_eligibility.require_phase_allowed(current, str(item.get("phase", "")))
    contract: dict[str, Any] = {
        "focus_contract_sha256": focus_contract_sha256(current),
        "execution_disposition": current.get("execution_disposition"),
        "receipt_sha256": current.get("receipt_sha256"),
    }
    if current.get("execution_disposition") == "organize_or_integrate":
        receipt = _focus_receipt(current)
        source = receipt.get("machine_proof", {}).get("source")
        if not isinstance(source, dict):
            raise ValueError("integration-only focus lacks an exact machine proof source")
        required = {
            "formal_system", "repository", "revision", "tree_or_archive_sha256", "file_path",
            "file_sha256", "module", "declaration", "declaration_type_sha256",
            "match_kind", "transport_evidence", "terminal_proof_body",
        }
        if any(key not in source for key in required):
            raise ValueError("integration-only focus source identity is incomplete")
        contract.update({
            "machine_evidence_class": current.get("machine_evidence_class"),
            "exact_machine_source": {key: source[key] for key in sorted(required)},
            "exact_machine_source_used": True,
            "introduced_root_critical_proof": False,
        })
    return contract


def require_phase_receipt_focus_semantics(
    item: dict[str, Any],
    focus_contract: dict[str, Any],
    role_map: dict[str, Any],
    *,
    evidence_root: Path | None = None,
) -> dict[str, Any]:
    """Bind the worker's typed intent and exact-source claim to current focus."""
    phase_receipts = [
        row for row in role_map.get("artifacts", [])
        if isinstance(row, dict) and row.get("role") == "phase_receipt"
    ]
    if len(phase_receipts) != 1 or not isinstance(phase_receipts[0].get("path"), str):
        raise ValueError("focus semantic gate requires exactly one phase receipt")
    receipt, _ = read_exact_json_file(
        (evidence_root or ROOT) / phase_receipts[0]["path"],
        "worker phase receipt",
    )
    if (
        receipt.get("item_id") != item.get("id")
        or receipt.get("theorem_id") != item.get("theorem_id")
        or receipt.get("phase") != item.get("phase")
    ):
        raise ValueError("phase receipt identity disagrees with focus contract")
    disposition = focus_contract.get("execution_disposition")
    expected_intent: Any = phase_contract(item).get("intent")
    if isinstance(expected_intent, dict):
        expected_intent = expected_intent.get(disposition)
    if not isinstance(expected_intent, str) or receipt.get("intent") != expected_intent:
        raise ValueError("phase receipt intent is not permitted by current focus disposition")
    if disposition == "organize_or_integrate":
        worker_focus = receipt.get("focus_execution")
        if worker_focus != focus_contract:
            raise ValueError("integration phase receipt does not bind the exact focus proof source")
    return receipt


def require_integration_only_source_evidence(
    item: dict[str, Any],
    focus_contract: dict[str, Any],
    role_map: dict[str, Any],
    *,
    changed_paths: list[str] | None = None,
    evidence_root: Path | None = None,
) -> dict[str, Any]:
    """Check provisional worker source bindings without granting proof credit."""
    if focus_contract.get("execution_disposition") != "organize_or_integrate":
        if any(key in focus_contract for key in INTEGRATION_ONLY_FOCUS_EXECUTION_FIELDS - FOCUS_EXECUTION_FIELDS):
            raise ValueError("non-integration focus carries integration-only assertions")
        return {}
    if set(focus_contract) != INTEGRATION_ONLY_FOCUS_EXECUTION_FIELDS:
        raise ValueError("integration-only focus execution fields are not exact")
    expected = focus_contract.get("exact_machine_source")
    if (
        focus_contract.get("exact_machine_source_used") is not True
        or focus_contract.get("introduced_root_critical_proof") is not False
        or not isinstance(expected, dict)
    ):
        raise ValueError("integration-only focus assertions are not fail-closed")
    phase_receipt = require_phase_receipt_focus_semantics(
        item, focus_contract, role_map, evidence_root=evidence_root
    )
    consumes_source = acceptance_evidence.phase_consumes_exact_machine_source(
        str(item.get("phase", "")), role_map
    )
    if not consumes_source:
        return phase_receipt
    worker_assertion = phase_receipt.get("integration_source_evidence")
    proof_sources = phase_receipt.get("inputs", {}).get("proof_sources")
    if (
        not isinstance(worker_assertion, dict)
        or set(worker_assertion)
        != {
            "exact_machine_source", "exact_machine_source_used",
            "introduced_root_critical_proof", "local_proof_source",
        }
        or worker_assertion.get("exact_machine_source") != expected
        or worker_assertion.get("exact_machine_source_used") is not True
        or worker_assertion.get("introduced_root_critical_proof") is not False
        or not isinstance(proof_sources, list)
        or not proof_sources
    ):
        raise ValueError("integration receipt lacks independent exact-source evidence")
    body = expected.get("terminal_proof_body")
    local_binding = worker_assertion.get("local_proof_source")
    if (
        not isinstance(local_binding, dict)
        or set(local_binding) != {"path", "sha256"}
        or re.fullmatch(r"[0-9a-f]{64}", str(local_binding.get("sha256", "")))
        is None
    ):
        raise ValueError("integration receipt lacks a local exact-source binding")
    matches = [
        row for row in proof_sources
        if isinstance(row, dict)
        and row.get("path") == local_binding.get("path")
        and row.get("sha256") == local_binding.get("sha256")
    ]
    if len(matches) != 1:
        raise ValueError("proof sources do not consume the receipt-bound exact source")
    local_path = str(local_binding["path"])
    local = (evidence_root or ROOT) / local_path
    if (
        Path(local_path).is_absolute()
        or ".." in Path(local_path).parts
        or local.is_symlink()
        or not local.is_file()
        or hashlib.sha256(local.read_bytes()).hexdigest() != matches[0]["sha256"]
    ):
        raise ValueError("exact-source local integration artifact is missing or stale")
    if changed_paths is not None:
        lean_changes = [path for path in changed_paths if Path(path).suffix == ".lean"]
        if set(lean_changes) - {local_path}:
            raise ValueError("integration delta contains undeclared root-critical proof content")
    return phase_receipt


def require_claim_focus_current(
    item: dict[str, Any],
    claim: dict[str, Any],
    theorem_nodes: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Reject a lease when its exact admission changed after allocation."""
    decision = require_item_focus_phase_allowed(item, theorem_nodes)
    if claim.get("focus_eligibility") != decision:
        raise ValueError("claim focus eligibility is missing, stale, or changed")
    expected_contract = focus_execution_contract(
        item, theorem_nodes, decision=decision
    )
    recorded_contract = claim.get("focus_execution")
    if recorded_contract != expected_contract:
        raise ValueError("claim focus execution contract is missing or changed after allocation")
    return decision


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
        "replay-results", "semantic-decisions", "review-acl-snapshots",
    ):
        path = RUNTIME / name
        if path.is_symlink() or (path.exists() and (not path.is_dir() or not path.resolve().is_relative_to(root_resolved))):
            fail(f"scheduler runtime subdirectory is unsafe: {name}")


def execution_is_paused() -> bool:
    return PAUSE_FILE.exists()


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
                    "Docs/Stage1_Phase_DAG_v2.json",
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
    """Load the blueprint-derived v2 theorem-order projection."""
    data = read_json(THEOREM_DAG_V2)
    if data.get("schema_version") != "stage1-theorem-dag/2.1":
        fail("v2 theorem DAG schema version is unsupported")
    if data.get("requirements_source") != "Docs/Stage1_Blueprint_v2.md":
        fail("v2 theorem DAG requirements source is stale")
    if data.get("execution_dag_projection") != "Docs/Stage1_Phase_DAG_v2.json":
        fail("v2 theorem DAG execution projection path is stale")
    snapshot = data.get("blueprint_state_snapshot")
    if (
        not isinstance(snapshot, dict)
        or snapshot.get("authoritative_blueprint") != "Docs/Stage1_Blueprint_v2.md"
        or snapshot.get("authoritative_blueprint_sha256") != sha256_file(BLUEPRINT)
    ):
        fail("v2 theorem DAG blueprint state snapshot is stale")
    nodes = data.get("theorems")
    if not isinstance(nodes, list) or len(nodes) != 1546:
        fail("v2 theorem DAG must contain exactly 1546 nodes")
    by_id = {node.get("theorem_id"): node for node in nodes if isinstance(node, dict)}
    if len(by_id) != 1546 or None in by_id:
        fail("v2 theorem DAG has duplicate or missing theorem IDs")
    targets = target_rows()
    if set(by_id) != {target["theorem_id"] for target in targets}:
        fail("v2 theorem DAG target set disagrees with the v2 membership projection")
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
        projection = by_id[theorem_id].get("focus_eligibility")
        if not isinstance(projection, dict):
            fail(f"v2 theorem DAG focus eligibility projection is missing: {theorem_id}")
        expected_digest = projection.get("receipt_sha256")
        if expected_digest is not None and (
            not isinstance(expected_digest, str)
            or re.fullmatch(r"[0-9a-f]{64}", expected_digest) is None
        ):
            fail(f"v2 theorem DAG focus eligibility digest is malformed: {theorem_id}")
        decision = focus_eligibility.load_focus_eligibility(
            ROOT,
            theorem_id,
            expected_projection_sha256=expected_digest,
        )
        if decision != projection:
            fail(f"v2 theorem DAG focus eligibility projection is stale: {theorem_id}")
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
            if decision == "reused_with_transport":
                provider_import_module = row.get("provider_import_module")
                if (
                    not isinstance(provider_import_module, str)
                    or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_'.]*", provider_import_module)
                    is None
                ):
                    raise ValueError(
                        "checked transport decision lacks a canonical provider import module"
                    )
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
    focus = require_item_focus_phase_allowed(item)
    receipt = {
        "schema_version": MASTER_ACCEPTANCE_RECEIPT_SCHEMA,
        "item_id": item["id"],
        "theorem_id": item["theorem_id"],
        "phase": item["phase"],
        "focus_eligibility": focus,
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
        "completion_gate": "current v2 focus permission, replayed phase evidence, and master acceptance",
        "attempts": 0,
        "children": [],
    }


def new_dag() -> dict[str, Any]:
    targets = target_rows()
    items = [make_item(target, phase) for target in targets for phase in range(len(PHASES))]
    ids = "\n".join(sorted(target["theorem_id"] for target in targets)) + "\n"
    return {
        "schema_version": "stage1-phase-dag/2.0",
        "requirements_source": "Docs/Stage1_Blueprint_v2.md",
        "target_manifest": "Docs/Stage1_Target_Membership_v2.json",
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
    if data.get("schema_version") != "stage1-phase-dag/2.0":
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
        "## 18. Generated 1546-Target Execution Checklist",
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
        "integration lane may render `[x]` only after current v2 focus, replay, and acceptance gates pass.",
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
    """Load the v2 SSOT under the selected authority root, including test clones."""
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
    raise ValueError("authoritative Stage1 v2 blueprint is missing")


def project_dag(items: list[dict[str, Any]]) -> dict[str, Any]:
    """Build the read-only execution-DAG projection from blueprint state."""
    data = new_dag()
    data["items"] = items
    return data


def write_derived_surfaces(data: dict[str, Any]) -> None:
    """Project the authoritative checklist to JSON without changing the SSOT."""
    items = load_blueprint_items()
    projection = project_dag(items)
    validate_dag(projection)
    if data.get("items") != items:
        fail("authoritative blueprint write did not preserve the requested task state")
    atomic_write(DAG, json.dumps(projection, ensure_ascii=False, indent=2) + "\n")


def bootstrap() -> None:
    # The v2 checklist is already the sole task-state authority.  A missing or
    # malformed checklist is corruption, never permission to recover state
    # from a derived DAG.
    data = project_dag(load_blueprint_items())
    validate_dag(data)
    write_derived_surfaces(data)
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


def process_effective_uid(pid: Any) -> int | None:
    """Return the effective UID from proc status for a live process."""
    if not pid_alive(pid):
        return None
    try:
        for line in (PROC_ROOT / str(pid) / "status").read_text(
            encoding="ascii"
        ).splitlines():
            if line.startswith("Uid:"):
                values = line.split()[1:]
                return int(values[1]) if len(values) == 4 else None
    except (OSError, ValueError):
        return None
    return None


def require_process_effective_uid(pid: Any, expected_uid: int, label: str) -> None:
    """Fail closed unless a live process is the configured OS principal."""
    observed = process_effective_uid(pid)
    if observed != expected_uid:
        fail(
            f"{label} effective UID mismatch: expected {expected_uid}, "
            f"observed {observed if observed is not None else 'unavailable'}"
        )


def exact_option_values(command: list[str]) -> dict[str, str] | None:
    """Parse the closed client argv grammar without accepting duplicate flags."""
    if len(command) >= 2 and Path(command[1]).absolute() == APP_SERVER_CLIENT.absolute():
        option_start = 2
    elif "--" in command:
        separator = command.index("--")
        if (
            separator + 2 >= len(command)
            or Path(command[separator + 2]).absolute()
            != APP_SERVER_CLIENT.absolute()
        ):
            return None
        option_start = separator + 3
    else:
        return None
    options: dict[str, str] = {}
    index = option_start
    while index < len(command):
        flag = command[index]
        if flag not in {
            "--workspace", "--prompt", "--objective", "--status", "--log",
            "--lane", "--model", "--effort", "--service-tier", "--binding",
            "--thread-id", "--worker-principal", "--codex", "--timeout",
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
        "worker_principal": options.get("--worker-principal"),
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
            observed_uid = process_effective_uid(pid)
            if observed_uid is None:
                fail("cannot bind a Stage1 client OS identity; refuse lane allocation")
            if identity["lane"] == REVIEW_LANE:
                raw_uid = os.environ.get("STAGE1_REVIEWER_UID")
                if raw_uid is None or not raw_uid.isdecimal() or observed_uid != int(raw_uid):
                    fail("Stage1 review client is not the configured independent OS principal")
            elif observed_uid != os.geteuid():
                fail("Stage1 implementation client OS principal is unexpected")
            clients.append({
                **identity, "pid": pid, "start_ticks": start,
                "effective_uid": observed_uid,
            })
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
        if (
            claim.get("runtime_protocol") != RUNTIME_PROTOCOL
            or UNSUPPORTED_RUNTIME_CLAIM_FIELDS.intersection(claim)
        ):
            fail(
                "unsupported Stage1 claim owns a live app-server client; "
                "refuse v2 runtime migration"
            )
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
            or client.get("worker_principal")
            != claim.get("runtime_principal_id")
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
        if (
            len(claim_rows) != 1
            or claim_rows[0].get("runtime_protocol") != RUNTIME_PROTOCOL
            or UNSUPPORTED_RUNTIME_CLAIM_FIELDS.intersection(claim_rows[0])
        ):
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
    expected_uid = (
        claim.get("runtime_principal_uid")
        if lane == REVIEW_LANE
        else os.geteuid()
    )
    if not isinstance(config, dict):
        return False
    return (
        claim.get("runtime_protocol") == RUNTIME_PROTOCOL
        and isinstance(expected_start, int)
        and process_start_ticks(pid) == expected_start
        and isinstance(expected_uid, int)
        and process_effective_uid(pid) == expected_uid
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
        and "--worker-principal" in command
        and str(claim.get("runtime_principal_id", "")) in command
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
    expected_client_uid = (
        claim.get("runtime_principal_uid")
        if lane == REVIEW_LANE
        else os.geteuid()
    )
    expected_sandbox = (
        REQUIRED_REVIEW_SANDBOX_CONTRACT
        if lane == REVIEW_LANE
        else REQUIRED_IMPLEMENTATION_SANDBOX_CONTRACT
    )
    expected_turn_sandbox = (
        {
            **REQUIRED_FRONTIER_TURN_SANDBOX_BASE,
            "writableRoots": [claim.get("workspace"), claim.get("frontier_scratch")],
        }
        if claim.get("frontier_policy_sha256") is not None
        else None
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
        and isinstance(expected_client_uid, int)
        and (
            status.get("state") == "finished"
            or process_effective_uid(status.get("client_pid")) == expected_client_uid
        )
        and isinstance(child_pid, int)
        and isinstance(child_start, int)
        and (status.get("state") == "finished" or process_start_ticks(child_pid) == child_start)
        and isinstance(status.get("thread_id"), str)
        and status.get("worker_principal") == claim.get("runtime_principal_id")
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
        and contract.get("worker_principal") == claim.get("runtime_principal_id")
        and (
            expected_turn_sandbox is None
            or (
                status.get("frontier_scratch") == claim.get("frontier_scratch")
                and contract.get("turn_sandbox") == expected_turn_sandbox
            )
        )
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
        if (
            claim.get("status") not in active_statuses
            or claim.get("runtime_protocol") != RUNTIME_PROTOCOL
            or UNSUPPORTED_RUNTIME_CLAIM_FIELDS.intersection(claim)
        ):
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
        if (
            claim.get("runtime_protocol") != RUNTIME_PROTOCOL
            or UNSUPPORTED_RUNTIME_CLAIM_FIELDS.intersection(claim)
        ):
            # Unsupported rows are audit data, never operational authority. Do
            # not trust their paths or lane metadata enough to perform cleanup.
            claim["status"] = "quarantined"
            claim["quarantined_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["quarantine_reason"] = (
                "claim is not current Stage1 v2 runtime state"
            )
            kept.append(claim)
            continue
        item = item_by_id.get(claim.get("item_id"))
        if item is None:
            # Runtime state is not an authority surface. Preserve malformed or
            # obsolete rows for audit, but never derive runtime/filesystem side
            # effects from an identity absent from the validated DAG.
            claim["status"] = "quarantined"
            claim["quarantined_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["quarantine_reason"] = "claim item is absent from the authoritative DAG"
            restore_stopped_review_acl(claim)
            kept.append(claim)
            continue
        lane = claim.get("lane", IMPLEMENTATION_LANE)
        if claim.get("theorem_id") != item["theorem_id"] or claim.get("owned_paths") != item["owned_paths"]:
            claim["status"] = "quarantined"
            claim["quarantined_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["quarantine_reason"] = "claim authority metadata disagrees with the validated DAG"
            restore_stopped_review_acl(claim)
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
        expected_frontier_scratch = (
            RUNTIME / FRONTIER_SCRATCH_DIRECTORY / str(claim_id)
        )
        runtime_bound = claim.get("status") in active_statuses | {"blocked"}
        active_runtime = claim.get("status") in active_statuses
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
                claim.get("frontier_policy_sha256") is not None
                and (
                    not isinstance(claim.get("frontier_scratch"), str)
                    or Path(str(claim.get("frontier_scratch"))).absolute()
                    != expected_frontier_scratch.absolute()
                    or Path(str(claim.get("frontier_scratch"))).is_symlink()
                )
            )
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
            restore_stopped_review_acl(claim)
            kept.append(claim)
            continue
        if claim.get("status") in active_statuses | {
            "finished_integrated", "review_finished"
        }:
            try:
                require_claim_focus_runtime_current(
                    item, claim, theorem_nodes, boundary="runtime_refresh"
                )
            except (OSError, ValueError, focus_eligibility.EligibilityError) as exc:
                try:
                    recorded = claim.get("focus_eligibility")
                    policy = (
                        _frontier_policy(recorded)
                        if isinstance(recorded, dict)
                        else None
                    )
                    ledger = _read_frontier_runtime(str(item.get("theorem_id", "")))
                    if policy is not None and ledger is not None:
                        _frontier_stop(
                            str(item["theorem_id"]), ledger,
                            "frontier scheduler authority was revoked: " + str(exc),
                            condition="scheduler_revoked",
                        )
                except (OSError, ValueError, focus_eligibility.EligibilityError):
                    pass
                was_live = app_server_worker_is_live(claim) or app_server_child_is_live(claim)
                if was_live:
                    terminated = terminate_app_server_worker(claim)
                    if not terminated and (
                        app_server_worker_is_live(claim) or app_server_child_is_live(claim)
                    ):
                        claim["status"] = "draining"
                        claim["drain_reason"] = "focus authority revoked: " + str(exc)
                        kept.append(claim)
                        continue
                try:
                    settle_frontier_claim(item, claim, reason="focus authority revoked")
                except ValueError:
                    pass
                claim["status"] = "quarantined"
                claim["quarantined_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                claim["quarantine_reason"] = "focus authority revoked: " + str(exc)
                restore_stopped_review_acl(claim)
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
            if lane == IMPLEMENTATION_LANE:
                settle_frontier_claim(item, claim, reason="master_accepted")
            restore_stopped_review_acl(claim)
            quarantine_review_acl_restore_failure(claim)
            claim["released_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["release_reason"] = "master_accepted"
            (kept if claim.get("status") == "quarantined" else released).append(claim)
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
            restore_stopped_review_acl(claim)
            quarantine_review_acl_restore_failure(claim)
            kept.append(claim)
            continue
        if lane == REVIEW_LANE and claim.get("status") in {
            "quarantined", "released", "cancelled", "master_accepted", "superseded"
        }:
            restore_stopped_review_acl(claim)
            quarantine_review_acl_restore_failure(claim)
            kept.append(claim)
            continue
        if (
            lane == REVIEW_LANE
            and claim.get("review_acl_snapshot_state") == "active"
            and not app_server_worker_is_live(claim)
            and not app_server_child_is_live(claim)
        ):
            # Covers scheduler crashes after process exit but before a status
            # transition, including non-active terminal rows retained for audit.
            restore_stopped_review_acl(claim)
            quarantine_review_acl_restore_failure(claim)
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
            restore_stopped_review_acl(claim)
            quarantine_review_acl_restore_failure(claim)
            (kept if claim.get("status") == "quarantined" else released).append(claim)
            continue
        if claim.get("status") == "draining":
            if app_server_worker_is_live(claim) or app_server_child_is_live(claim):
                terminate_app_server_worker(claim)
            if app_server_worker_is_live(claim) or app_server_child_is_live(claim):
                claim["drain_retried_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                kept.append(claim)
            else:
                if lane == IMPLEMENTATION_LANE:
                    settle_frontier_claim(item, claim, reason="draining worker stopped")
                restore_stopped_review_acl(claim)
                quarantine_review_acl_restore_failure(claim)
                claim["released_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                claim["release_reason"] = "draining app-server worker stopped"
                (kept if claim.get("status") == "quarantined" else released).append(claim)
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
                    if (
                        not app_server_worker_is_live(claim)
                        and not app_server_child_is_live(claim)
                    ):
                        restore_stopped_review_acl(claim)
                        quarantine_review_acl_restore_failure(claim)
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
                if (
                    not app_server_worker_is_live(claim)
                    and not app_server_child_is_live(claim)
                ):
                    restore_stopped_review_acl(claim)
                    quarantine_review_acl_restore_failure(claim)
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
                    restore_stopped_review_acl(claim)
                    quarantine_review_acl_restore_failure(claim)
                    kept.append(claim)
                else:
                    restore_stopped_review_acl(claim)
                    quarantine_review_acl_restore_failure(claim)
                    claim["released_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                    claim["release_reason"] = "incomplete review launch reservation"
                    (kept if claim.get("status") == "quarantined" else released).append(claim)
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
                settle_frontier_claim(item, claim, reason="incomplete worker launch")
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
                restore_stopped_review_acl(claim)
                quarantine_review_acl_restore_failure(claim)
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
                settle_frontier_claim(item, claim, reason="worker finished")
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
                settle_frontier_claim(item, claim, reason="worker blocked")
                kept.append(claim)
        elif claim.get("status") == "live" and not goal_runtime_is_verified(claim):
            claim["status"] = "draining"
            claim["drain_reason"] = "live worker lacks a verified app-server /goal runtime contract"
            terminate_app_server_worker(claim)
            if (
                not app_server_worker_is_live(claim)
                and not app_server_child_is_live(claim)
            ):
                restore_stopped_review_acl(claim)
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


def _frontier_runtime_path(theorem_id: str) -> Path:
    if re.fullmatch(r"THM-M-[0-9]{4}", theorem_id) is None:
        raise ValueError("frontier runtime theorem identity is malformed")
    return RUNTIME / "frontier-runtime" / f"{theorem_id}.json"


def scheduler_worker_principal_id() -> str:
    """Return the stable, scheduler-authenticated proof-worker principal."""
    override = os.environ.get("STAGE1_PROOF_WORKER_ID")
    if override is not None:
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:@-]{0,199}", override) is None:
            raise ValueError("configured proof-worker principal is malformed")
        return override
    # The OS account and machine id are runtime facts, unlike a copied receipt
    # label or a random per-attempt claim id. Hash the host fact so the receipt
    # need not expose a private machine identifier.
    machine_id = Path("/etc/machine-id")
    try:
        host_fact = machine_id.read_text(encoding="ascii").strip()
    except OSError:
        host_fact = f"node-{uuid.getnode():012x}"
    if not host_fact:
        raise ValueError("scheduler cannot authenticate its proof-worker host")
    host_digest = hashlib.sha256(host_fact.encode("ascii")).hexdigest()[:16]
    return f"{os.environ.get('USER', 'unknown')}@{host_digest}"


def scheduler_review_principal_id() -> str:
    """Return the configured, OS-authenticated read-only review principal."""
    raw_uid = os.environ.get("STAGE1_REVIEWER_UID")
    if raw_uid is None or not raw_uid.isdecimal():
        raise ValueError("independent review service-account UID is not configured")
    uid = int(raw_uid)
    if uid < 1 or uid == os.geteuid():
        raise ValueError("independent reviewer must use a distinct non-root OS UID")
    try:
        account = pwd.getpwuid(uid)
    except KeyError as exc:
        raise ValueError("configured independent reviewer UID does not exist") from exc
    if not account.pw_name or account.pw_uid != uid:
        raise ValueError("configured independent reviewer account is malformed")
    machine_id = Path("/etc/machine-id")
    try:
        host_fact = machine_id.read_text(encoding="ascii").strip()
    except OSError:
        host_fact = f"node-{uuid.getnode():012x}"
    if not host_fact:
        raise ValueError("scheduler cannot authenticate its review host")
    host_digest = hashlib.sha256(host_fact.encode("ascii")).hexdigest()[:16]
    principal = f"uid:{uid}:{account.pw_name}@{host_digest}"
    configured = os.environ.get("STAGE1_REVIEWER_PRINCIPAL_ID")
    if configured is None:
        raise ValueError("independent review trust principal is not configured")
    try:
        _key_id, trust_principal, _key = focus_eligibility._trust_anchor(
            ROOT, "independent_review", active_only=True
        )
    except focus_eligibility.EligibilityError as exc:
        raise ValueError("independent review trust anchor is unavailable") from exc
    if configured != trust_principal:
        raise ValueError(
            "configured review principal does not match the active trust anchor"
        )
    if principal == scheduler_worker_principal_id():
        raise ValueError("review and implementation principals are not distinct")
    # The UID/account/host tuple above authenticates the execution boundary;
    # the stable trust-anchor principal is the identity signed into receipts.
    return configured


def scheduler_review_principal() -> tuple[str, int]:
    """Return one validated principal tuple without reparsing caller text."""
    principal = scheduler_review_principal_id()
    raw_uid = os.environ.get("STAGE1_REVIEWER_UID")
    if raw_uid is None or not raw_uid.isdecimal():
        raise ValueError("authenticated review principal has a malformed identity")
    uid = int(raw_uid)
    if uid == os.geteuid():
        raise ValueError("independent reviewer must use a distinct non-root OS UID")
    return principal, uid


def _parse_runtime_timestamp(value: Any, label: str) -> dt.datetime:
    if not isinstance(value, str):
        raise ValueError(f"frontier {label} is missing")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"frontier {label} is malformed") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"frontier {label} is not timezone-aware")
    return parsed.astimezone(dt.timezone.utc)


def _frontier_policy(decision: dict[str, Any]) -> dict[str, Any] | None:
    policy = decision.get("frontier_policy")
    if decision.get("execution_disposition") != "frontier_exception":
        return None
    if not isinstance(policy, dict):
        raise ValueError("frontier focus lacks a runtime policy")
    unhashed = dict(policy)
    embedded = unhashed.pop("policy_sha256", None)
    if (
        policy.get("schema_version") != "stage1-frontier-runtime-policy/1.0"
        or embedded != hashlib.sha256(
            json.dumps(
                unhashed, ensure_ascii=True, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest()
        or not isinstance(policy.get("assigned_worker_id"), str)
        or not policy["assigned_worker_id"]
        or not isinstance(policy.get("completion_probability"), (int, float))
        or isinstance(policy.get("completion_probability"), bool)
        or not 0.70 <= float(policy["completion_probability"]) <= 1.0
        or set(policy.get("stop_conditions", []))
        != focus_eligibility.REQUIRED_FRONTIER_STOP_CONDITIONS
        or not isinstance(policy.get("validator"), dict)
    ):
        raise ValueError("frontier runtime policy is malformed or unbound")
    return policy


def _frontier_validator_input(
    item: dict[str, Any],
    decision: dict[str, Any],
    policy: dict[str, Any],
    ledger: dict[str, Any] | None,
    boundary: str,
) -> bytes:
    payload = {
        "schema_version": "stage1-frontier-validator-input/1.0",
        "boundary": boundary,
        "theorem_id": item.get("theorem_id"),
        "item_id": item.get("id"),
        "phase": item.get("phase"),
        "receipt_sha256": decision.get("receipt_sha256"),
        "policy_sha256": policy.get("policy_sha256"),
        "completion_probability": policy.get("completion_probability"),
        "runtime_ledger": ledger,
    }
    return (
        json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _run_frontier_validator(
    item: dict[str, Any],
    decision: dict[str, Any],
    policy: dict[str, Any],
    ledger: dict[str, Any] | None,
    *,
    boundary: str,
) -> dict[str, Any]:
    """Run the receipt-bound validator in a read-only, networkless sandbox."""

    validator = policy.get("validator")
    if not isinstance(validator, dict) or set(validator) != {"path", "sha256", "command"}:
        raise ValueError("frontier validator policy is malformed")
    relative = validator.get("path")
    digest = validator.get("sha256")
    command = validator.get("command")
    owner = f"Stage1_Instances/{item.get('theorem_id')}/"
    if (
        not isinstance(relative, str)
        or not relative.startswith(owner)
        or Path(relative).is_absolute()
        or ".." in Path(relative).parts
        or not isinstance(digest, str)
        or re.fullmatch(r"[0-9a-f]{64}", digest) is None
        or command != ["python3", relative]
    ):
        raise ValueError("frontier validator path, digest, or command is not canonical")
    path = safe_evidence_path(ROOT, relative, owner=str(item.get("theorem_id")))
    if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise ValueError("frontier validator is missing, unsafe, or stale")
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3")
    if not bwrap.is_file() or not python.is_file():
        raise ValueError("frontier validator sandbox runtime is unavailable")
    argv = [
        str(bwrap), "--die-with-parent", "--new-session", "--unshare-all",
        "--ro-bind", "/usr", "/usr", "--symlink", "usr/bin", "/bin",
        "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib64", "/lib64",
        "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
        "--ro-bind", str(ROOT.resolve()), "/repo", "--chdir", "/repo",
        "--clearenv", "--setenv", "PATH", "/usr/bin:/bin", "--setenv", "HOME", "/tmp",
        "--", str(python), "-I", "-B", f"/repo/{relative}",
    ]
    try:
        result = subprocess.run(
            argv,
            input=_frontier_validator_input(item, decision, policy, ledger, boundary),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=FRONTIER_VALIDATOR_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValueError("frontier validator timed out") from exc
    if (
        len(result.stdout) > FRONTIER_VALIDATOR_MAX_OUTPUT_BYTES
        or len(result.stderr) > FRONTIER_VALIDATOR_MAX_OUTPUT_BYTES
    ):
        raise ValueError("frontier validator output exceeds its scheduler limit")
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise ValueError(f"frontier validator failed: {detail or 'nonzero exit'}")
    try:
        output = json.loads(result.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("frontier validator output is not one JSON object") from exc
    if (
        not isinstance(output, dict)
        or set(output) != {
            "schema_version", "theorem_id", "item_id", "phase", "boundary",
            "policy_sha256", "valid", "completion_probability",
            "statement_source_match", "scheduler_revoked", "reason_codes",
        }
        or output.get("schema_version") != FRONTIER_VALIDATOR_RESULT_SCHEMA
        or output.get("theorem_id") != item.get("theorem_id")
        or output.get("item_id") != item.get("id")
        or output.get("phase") != item.get("phase")
        or output.get("boundary") != boundary
        or output.get("policy_sha256") != policy.get("policy_sha256")
        or not isinstance(output.get("completion_probability"), (int, float))
        or isinstance(output.get("completion_probability"), bool)
        or not isinstance(output.get("reason_codes"), list)
        or any(not isinstance(reason, str) or not reason for reason in output["reason_codes"])
    ):
        raise FrontierPolicyStop(
            "validator_failure",
            "frontier validator returned a malformed or mismatched decision",
        )
    if output.get("scheduler_revoked") is not False:
        raise FrontierPolicyStop("scheduler_revoked", "frontier exception is scheduler-revoked")
    if output.get("statement_source_match") is not True:
        raise FrontierPolicyStop(
            "statement_or_source_mismatch",
            "frontier statement or source no longer matches",
        )
    probability = float(output["completion_probability"])
    if probability < 0.70 or probability != float(policy["completion_probability"]):
        raise FrontierPolicyStop(
            "probability_below_threshold",
            "frontier completion probability is below or differs from the reviewed threshold",
        )
    if output.get("valid") is not True:
        raise FrontierPolicyStop("validator_failure", "frontier validator rejected the attempt")
    return output


def _require_frontier_validator(
    item: dict[str, Any],
    decision: dict[str, Any],
    policy: dict[str, Any],
    ledger: dict[str, Any] | None,
    *,
    boundary: str,
) -> dict[str, Any]:
    theorem_id = str(item.get("theorem_id", ""))
    try:
        return _run_frontier_validator(
            item, decision, policy, ledger, boundary=boundary
        )
    except ValueError as exc:
        condition = (
            exc.condition if isinstance(exc, FrontierPolicyStop) else "validator_failure"
        )
        if ledger is not None:
            _frontier_stop(
                theorem_id,
                ledger,
                f"frontier validator failure at {boundary}: {exc}",
                condition=condition,
            )
        raise


def _read_frontier_runtime(theorem_id: str) -> dict[str, Any] | None:
    path = _frontier_runtime_path(theorem_id)
    if not path.exists():
        return None
    if path.is_symlink() or not path.is_file():
        raise ValueError("frontier runtime ledger is unsafe")
    value = read_json(path)
    if value.get("schema_version") != FRONTIER_RUNTIME_LEDGER_SCHEMA:
        raise ValueError("frontier runtime ledger schema is unsupported")
    return value


def _frontier_claim_scratch_path(claim: dict[str, Any]) -> Path:
    """Resolve the only scheduler-owned temporary directory for a frontier claim."""

    claim_id = claim.get("claim_id")
    configured = claim.get("frontier_scratch")
    if not isinstance(claim_id, str) or CLAIM_ID_RE.fullmatch(claim_id) is None:
        raise ValueError("frontier scratch claim identity is malformed")
    expected = RUNTIME / FRONTIER_SCRATCH_DIRECTORY / claim_id
    if (
        not isinstance(configured, str)
        or Path(configured).absolute() != expected.absolute()
        or Path(configured).is_symlink()
    ):
        raise ValueError("frontier scratch path is not scheduler-canonical")
    try:
        runtime_resolved = RUNTIME.resolve()
        parent_resolved = expected.parent.resolve()
    except OSError as exc:
        raise ValueError("frontier scratch parent is unavailable") from exc
    if (
        RUNTIME.is_symlink()
        or expected.parent.is_symlink()
        or not parent_resolved.is_relative_to(runtime_resolved)
    ):
        raise ValueError("frontier scratch escapes scheduler-owned storage")
    if expected.exists() and (
        not expected.is_dir()
        or expected.is_symlink()
        or not expected.resolve().is_relative_to(runtime_resolved)
    ):
        raise ValueError("frontier scratch is unsafe")
    return expected


def prepare_frontier_scratch(claim: dict[str, Any]) -> Path:
    """Create an empty, claim-scoped TMPDIR without following stale links."""

    scratch = _frontier_claim_scratch_path(claim)
    scratch.parent.mkdir(parents=True, exist_ok=True)
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(mode=0o700)
    return scratch


def ensure_frontier_scratch(claim: dict[str, Any]) -> Path:
    """Require an existing scratch on restart without erasing uncommitted usage."""

    scratch = _frontier_claim_scratch_path(claim)
    if not scratch.is_dir() or scratch.is_symlink():
        raise ValueError("frontier restart scratch is missing or unsafe")
    return scratch


def cleanup_frontier_scratch(claim: dict[str, Any]) -> None:
    """Remove a settled claim's scratch only after usage has been committed."""

    if claim.get("frontier_scratch") is None:
        return
    scratch = _frontier_claim_scratch_path(claim)
    if scratch.exists():
        shutil.rmtree(scratch)


def _regular_tree_bytes(path: Path, label: str) -> int:
    if not path.exists():
        return 0
    if path.is_symlink() or not path.is_dir():
        raise ValueError(f"frontier {label} usage root is unsafe")
    total = 0
    try:
        for child in path.rglob("*"):
            if child.is_file() and not child.is_symlink():
                total += child.stat().st_size
    except OSError as exc:
        raise ValueError(f"frontier {label} usage is unreadable") from exc
    return total


def _proc_process_tree_usage(pid: int, start_ticks: int) -> float | None:
    """Return cumulative CPU seconds for the claim and every live descendant."""

    if PROC_ROOT != Path("/proc"):
        return None
    if process_start_ticks(pid) != start_ticks:
        return None
    try:
        clock_ticks = os.sysconf("SC_CLK_TCK")
    except (OSError, ValueError):
        return None
    if not isinstance(clock_ticks, int) or clock_ticks <= 0:
        return None
    processes: dict[int, tuple[int, int]] = {}
    try:
        rows = list(PROC_ROOT.iterdir())
    except OSError:
        return None
    for row in rows:
        if not row.name.isdecimal():
            continue
        try:
            data = (row / "stat").read_text(encoding="utf-8")
            closing = data.rfind(")")
            fields = data[closing + 2 :].split()
            # Fields after comm begin at proc field 3: ppid=4, utime=14,
            # stime=15, cutime=16, cstime=17. Child times retain already-reaped
            # descendants; live descendants contribute their own rows.
            process_pid = int(row.name)
            processes[process_pid] = (
                int(fields[1]),
                sum(int(fields[index]) for index in (11, 12, 13, 14)),
            )
        except (OSError, ValueError, IndexError):
            continue
    descendants = {pid}
    changed = True
    while changed:
        changed = False
        for process_pid, (parent_pid, _ticks) in processes.items():
            if process_pid not in descendants and parent_pid in descendants:
                descendants.add(process_pid)
                changed = True
    total_ticks = sum(
        processes[process_pid][1]
        for process_pid in descendants
        if process_pid in processes
    )
    return total_ticks / clock_ticks


def _frontier_observed_usage(claim: dict[str, Any]) -> dict[str, int]:
    status = worker_status(claim)
    goal = status.get("goal") if isinstance(status, dict) else None
    launched = isinstance(claim.get("pid"), int) or isinstance(
        claim.get("client_started_at"), str
    )
    if launched and not isinstance(goal, dict):
        raise ValueError("launched frontier attempt lacks runtime usage accounting")
    tokens = goal.get("tokensUsed", 0) if isinstance(goal, dict) else 0
    goal_elapsed = goal.get("timeUsedSeconds", 0) if isinstance(goal, dict) else 0
    started_at = claim.get("frontier_attempt_started_at")
    if started_at is None:
        raise ValueError("frontier attempt lacks a scheduler start time")
    lease_started = _parse_runtime_timestamp(started_at, "attempt start time")
    now = dt.datetime.now(dt.timezone.utc)
    elapsed = max(0, int((now - lease_started).total_seconds()))
    workspace = Path(str(claim.get("workspace", "")))
    disk = _regular_tree_bytes(workspace, "workspace")
    scratch = _frontier_claim_scratch_path(claim)
    launched = isinstance(claim.get("pid"), int) or isinstance(
        claim.get("client_started_at"), str
    )
    if launched and not scratch.exists():
        raise ValueError("launched frontier attempt lacks its scheduler-owned scratch")
    scratch_disk = _regular_tree_bytes(scratch, "scratch")
    baseline = claim.get("frontier_disk_baseline_bytes")
    for label, value in (
        ("tokens", tokens), ("goal elapsed", goal_elapsed),
        ("elapsed", elapsed), ("disk", disk), ("scratch disk", scratch_disk),
        ("disk baseline", baseline),
    ):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"frontier {label} usage is malformed")
    cpu_seconds: float | None = None
    pid = claim.get("pid")
    pid_start = claim.get("pid_start_ticks")
    if isinstance(pid, int) and isinstance(pid_start, int):
        cpu_seconds = _proc_process_tree_usage(pid, pid_start)
    # Goal accounting is retained for durable post-exit accounting. While the
    # process tree is live, charge the greater of goal and whole-tree CPU usage.
    # Elapsed time remains the conservative upper bound so detached or very
    # short-lived descendants cannot make compute usage disappear.
    compute = max(goal_elapsed, math.ceil(cpu_seconds or 0), elapsed)
    return {
        "wall_clock_seconds": elapsed,
        "token_count": tokens,
        "compute_seconds": compute,
        # Charge only bytes created above the scheduler-prepared clean clone.
        # The immutable source checkout itself is not exception work.
        "disk_bytes": max(0, disk - baseline) + scratch_disk,
    }


def _persist_frontier_runtime(theorem_id: str, ledger: dict[str, Any]) -> None:
    ledger["updated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    atomic_write(
        _frontier_runtime_path(theorem_id),
        json.dumps(ledger, ensure_ascii=True, indent=2) + "\n",
    )


def _frontier_stop(
    theorem_id: str,
    ledger: dict[str, Any],
    reason: str,
    *,
    condition: str | None = None,
) -> NoReturn:
    triggered = ledger.setdefault("triggered_stop_conditions", [])
    if not isinstance(triggered, list):
        raise ValueError("frontier stop-condition ledger is malformed")
    if reason not in triggered:
        triggered.append(reason)
    if condition is not None:
        if condition not in focus_eligibility.REQUIRED_FRONTIER_STOP_CONDITIONS:
            raise ValueError("frontier stop condition code is not policy-declared")
        codes = ledger.setdefault("triggered_stop_condition_codes", [])
        if not isinstance(codes, list):
            raise ValueError("frontier stop-condition code ledger is malformed")
        if condition not in codes:
            codes.append(condition)
    _persist_frontier_runtime(theorem_id, ledger)
    raise ValueError(reason)


def settle_frontier_claim(
    item: dict[str, Any], claim: dict[str, Any], *, reason: str
) -> None:
    """Commit one attempt's measured usage before releasing its logical principal."""
    decision = claim.get("focus_eligibility")
    if not isinstance(decision, dict) or decision.get("execution_disposition") != "frontier_exception":
        return
    policy = _frontier_policy(decision)
    ledger = _read_frontier_runtime(str(item.get("theorem_id", "")))
    if policy is None or ledger is None or ledger.get("active_claim_id") != claim.get("claim_id"):
        return
    committed = ledger.get("committed_usage")
    if not isinstance(committed, dict):
        raise ValueError("frontier committed usage is malformed")
    observed = _frontier_observed_usage(claim)
    saved_attempt = ledger.get("attempt_usage")
    if not isinstance(saved_attempt, dict):
        raise ValueError("frontier attempt usage is malformed")
    for key, value in observed.items():
        saved = saved_attempt.get(key)
        if not isinstance(saved, int) or isinstance(saved, bool) or saved < 0:
            raise ValueError("frontier attempt usage is malformed")
        committed[key] = int(committed.get(key, 0)) + max(saved, value)
    ledger["attempt_usage"] = {key: 0 for key in committed}
    ledger["active_claim_id"] = None
    ledger["last_settled_claim_id"] = claim.get("claim_id")
    ledger["last_settlement_reason"] = reason
    _persist_frontier_runtime(str(item["theorem_id"]), ledger)
    cleanup_frontier_scratch(claim)


FRONTIER_MILESTONE_PHASES = {
    "statement_closure": "statement",
    "root_proof_closure": "proof",
    "kernel_replay": "validation",
    "trust_audit": "validation",
}


def record_frontier_milestone_completion(
    item: dict[str, Any],
    review_claim: dict[str, Any],
    *,
    evidence_path: str,
    evidence_sha256: str,
) -> list[str]:
    """Append only policy-declared milestones proven by master acceptance."""

    decision = require_item_focus_phase_allowed(item)
    policy = _frontier_policy(decision)
    if policy is None:
        return []
    theorem_id = str(item.get("theorem_id", ""))
    ledger = _read_frontier_runtime(theorem_id)
    if ledger is None:
        raise ValueError("frontier runtime ledger is missing")
    if (
        review_claim.get("lane") != REVIEW_LANE
        or review_claim.get("status") != "master_accepted"
        or review_claim.get("item_id") != item.get("id")
        or review_claim.get("master_receipt_path") != evidence_path
        or review_claim.get("master_receipt_sha256") != evidence_sha256
        or not isinstance(evidence_path, str)
        or Path(evidence_path).is_absolute()
        or ".." in Path(evidence_path).parts
        or re.fullmatch(r"[0-9a-f]{64}", str(evidence_sha256)) is None
    ):
        raise ValueError("frontier milestone write lacks master-owned acceptance evidence")
    evidence = ROOT / evidence_path
    if (
        evidence.is_symlink()
        or not evidence.is_file()
        or hashlib.sha256(evidence.read_bytes()).hexdigest() != evidence_sha256
    ):
        raise ValueError("frontier milestone master receipt is missing or stale")
    if (
        ledger.get("policy_sha256") != policy.get("policy_sha256")
        or ledger.get("theorem_id") != theorem_id
    ):
        raise ValueError("frontier milestone ledger disagrees with current policy")
    completed = ledger.get("completed_milestones")
    milestones = policy.get("milestones")
    if not isinstance(completed, list) or not isinstance(milestones, list):
        raise ValueError("frontier milestone ledger or policy is malformed")
    existing = {
        row.get("milestone_id")
        for row in completed
        if isinstance(row, dict) and isinstance(row.get("milestone_id"), str)
    }
    eligible = [
        row
        for row in milestones
        if isinstance(row, dict)
        and FRONTIER_MILESTONE_PHASES.get(str(row.get("evidence_role")))
        == item.get("phase")
    ]
    added: list[str] = []
    for milestone in eligible:
        milestone_id = milestone.get("id")
        if not isinstance(milestone_id, str):
            raise ValueError("frontier milestone policy identity is malformed")
        if milestone_id in existing:
            prior = next(
                row for row in completed
                if isinstance(row, dict) and row.get("milestone_id") == milestone_id
            )
            if (
                prior.get("evidence_path") != evidence_path
                or prior.get("evidence_sha256") != evidence_sha256
                or prior.get("review_claim_id") != review_claim.get("claim_id")
            ):
                raise ValueError("frontier milestone already has different evidence")
            continue
        completed.append({
            "milestone_id": milestone_id,
            "evidence_role": milestone["evidence_role"],
            "evidence_path": evidence_path,
            "evidence_sha256": evidence_sha256,
            "review_claim_id": review_claim.get("claim_id"),
            "reviewed_by": "scheduler_master_lane",
            "reviewed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        })
        existing.add(milestone_id)
        added.append(milestone_id)
    if added:
        _persist_frontier_runtime(theorem_id, ledger)
    return added


def _require_frontier_runtime(
    item: dict[str, Any],
    decision: dict[str, Any],
    *,
    claim: dict[str, Any] | None,
    create: bool = False,
    boundary: str = "runtime_refresh",
) -> dict[str, Any] | None:
    policy = _frontier_policy(decision)
    if policy is None:
        return None
    theorem_id = str(item.get("theorem_id", ""))
    ledger = _read_frontier_runtime(theorem_id)
    if ledger is not None and ledger.get("triggered_stop_conditions"):
        raise ValueError(
            "frontier stop condition has already been triggered: "
            + ", ".join(str(row) for row in ledger["triggered_stop_conditions"])
        )
    now = dt.datetime.now(dt.timezone.utc)
    try:
        lease_expires_at = _parse_runtime_timestamp(
            policy.get("lease_expires_at"), "policy lease expiry"
        )
    except ValueError:
        if ledger is None:
            raise
        _frontier_stop(
            theorem_id, ledger, "frontier policy lease expiry is malformed",
            condition="lease_expired",
        )
    if now >= lease_expires_at:
        if ledger is None:
            raise ValueError("frontier policy lease is expired")
        _frontier_stop(
            theorem_id, ledger, "frontier policy lease is expired",
            condition="lease_expired",
        )
    if create:
        if claim is None:
            raise ValueError("frontier allocation lacks its scheduler claim")
        if ledger is None:
            ledger = {
                "schema_version": FRONTIER_RUNTIME_LEDGER_SCHEMA,
                "theorem_id": theorem_id,
                "assigned_worker_id": policy["assigned_worker_id"],
                "policy_sha256": policy["policy_sha256"],
                "attempts_started": 1,
                "active_claim_id": claim.get("claim_id"),
                "completed_milestones": [],
                "triggered_stop_conditions": [],
                "triggered_stop_condition_codes": [],
                "committed_usage": {
                    "wall_clock_seconds": 0, "token_count": 0,
                    "compute_seconds": 0, "disk_bytes": 0,
                },
                "attempt_usage": {
                    "wall_clock_seconds": 0, "token_count": 0,
                    "compute_seconds": 0, "disk_bytes": 0,
                },
                "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            }
        elif ledger.get("active_claim_id") != claim.get("claim_id"):
            if ledger.get("active_claim_id") is not None:
                raise ValueError("frontier logical principal already has an active claim")
            ledger["attempts_started"] = int(ledger.get("attempts_started", 0)) + 1
            ledger["active_claim_id"] = claim.get("claim_id")
            ledger["attempt_usage"] = {
                "wall_clock_seconds": 0, "token_count": 0,
                "compute_seconds": 0, "disk_bytes": 0,
            }
        _persist_frontier_runtime(theorem_id, ledger)
    if ledger is None:
        raise ValueError("frontier runtime ledger is missing")
    committed_usage = ledger.get("committed_usage")
    attempt_usage = ledger.get("attempt_usage")
    budget = policy.get("budget")
    milestones = policy.get("milestones")
    completed = ledger.get("completed_milestones")
    stopped = ledger.get("triggered_stop_conditions")
    stopped_codes = ledger.get("triggered_stop_condition_codes", [])
    if (
        ledger.get("theorem_id") != theorem_id
        or ledger.get("assigned_worker_id") != policy.get("assigned_worker_id")
        or ledger.get("policy_sha256") != policy.get("policy_sha256")
        or not isinstance(ledger.get("attempts_started"), int)
        or not isinstance(committed_usage, dict)
        or not isinstance(attempt_usage, dict)
        or not isinstance(budget, dict)
        or not isinstance(milestones, list)
        or not isinstance(completed, list)
        or not isinstance(stopped, list)
        or not isinstance(stopped_codes, list)
        or any(
            code not in focus_eligibility.REQUIRED_FRONTIER_STOP_CONDITIONS
            for code in stopped_codes
        )
    ):
        raise ValueError("frontier runtime ledger disagrees with its policy")
    if claim is not None:
        expected_principal = scheduler_worker_principal_id()
        terminal_implementation = (
            claim.get("lane", IMPLEMENTATION_LANE) == IMPLEMENTATION_LANE
            and claim.get("status") in {"finished", "finished_integrated", "blocked"}
            and ledger.get("last_settled_claim_id") == claim.get("claim_id")
        )
        active_implementation = (
            claim.get("lane", IMPLEMENTATION_LANE) == IMPLEMENTATION_LANE
            and ledger.get("active_claim_id") == claim.get("claim_id")
        )
        if (
            claim.get("frontier_assigned_worker_id") != policy.get("assigned_worker_id")
            or policy.get("assigned_worker_id") != expected_principal
            or claim.get("runtime_principal_id") != expected_principal
            or claim.get("frontier_policy_sha256") != policy.get("policy_sha256")
            or not (active_implementation or terminal_implementation)
        ):
            raise ValueError("frontier claim is not mapped to its logical principal")
        if active_implementation:
            attempt_usage.update(_frontier_observed_usage(claim))
    _require_frontier_validator(
        item, decision, policy, ledger, boundary=boundary
    )
    if ledger["attempts_started"] > policy.get("attempt_limit", 0):
        _frontier_stop(
            theorem_id, ledger, "frontier attempt limit is exhausted",
            condition="attempt_limit_reached",
        )
    limits = {
        "wall_clock_seconds": "wall_clock_seconds",
        "token_count": "token_limit",
        "compute_seconds": "compute_seconds",
        "disk_bytes": "disk_bytes",
    }
    total_usage: dict[str, int] = {}
    for key, limit in limits.items():
        committed_value = committed_usage.get(key)
        attempt_value = attempt_usage.get(key)
        if (
            not isinstance(committed_value, int)
            or isinstance(committed_value, bool)
            or committed_value < 0
            or not isinstance(attempt_value, int)
            or isinstance(attempt_value, bool)
            or attempt_value < 0
            or not isinstance(budget.get(limit), int)
        ):
            _frontier_stop(
                theorem_id, ledger, "frontier resource usage is malformed",
                condition="any_resource_budget_exhausted",
            )
        total_usage[key] = committed_value + attempt_value
        if total_usage[key] >= budget[limit]:
            _frontier_stop(
                theorem_id, ledger, f"frontier {limit} budget is exhausted",
                condition="any_resource_budget_exhausted",
            )
    if stopped:
        raise ValueError("frontier stop condition has been triggered: " + ", ".join(stopped))
    completed_ids: set[str] = set()
    policy_by_id = {
        row.get("id"): row
        for row in milestones
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    for record in completed:
        evidence_path = record.get("evidence_path") if isinstance(record, dict) else None
        evidence_sha = record.get("evidence_sha256") if isinstance(record, dict) else None
        review_claim_id = record.get("review_claim_id") if isinstance(record, dict) else None
        if (
            not isinstance(record, dict)
            or not isinstance(record.get("milestone_id"), str)
            or not isinstance(evidence_path, str)
            or Path(evidence_path).is_absolute()
            or ".." in Path(evidence_path).parts
            or not isinstance(evidence_sha, str)
            or re.fullmatch(r"[0-9a-f]{64}", evidence_sha) is None
            or not isinstance(review_claim_id, str)
            or record.get("milestone_id") not in policy_by_id
            or record.get("evidence_role")
            != policy_by_id.get(record.get("milestone_id"), {}).get("evidence_role")
            or record.get("reviewed_by") != "scheduler_master_lane"
            or not isinstance(record.get("reviewed_at"), str)
        ):
            _frontier_stop(
                theorem_id, ledger,
                "frontier milestone completion is not scheduler-reviewed",
                condition="validator_failure",
            )
        evidence = ROOT / evidence_path
        matching_reviews = [
            row for row in load_claims()
            if row.get("claim_id") == review_claim_id
            and row.get("lane") == REVIEW_LANE
            and row.get("status") == "master_accepted"
            and row.get("master_receipt_path") == evidence_path
            and row.get("master_receipt_sha256") == evidence_sha
        ]
        expected_phase = FRONTIER_MILESTONE_PHASES.get(str(record.get("evidence_role")))
        if (
            evidence.is_symlink()
            or not evidence.is_file()
            or hashlib.sha256(evidence.read_bytes()).hexdigest() != evidence_sha
            or len(matching_reviews) != 1
            or matching_reviews[0].get("theorem_id") != theorem_id
            or matching_reviews[0].get("item_id")
            != task_id(theorem_id, str(expected_phase))
        ):
            _frontier_stop(
                theorem_id, ledger, "frontier milestone evidence is forged or stale",
                condition="validator_failure",
            )
        completed_ids.add(record["milestone_id"])
    for milestone in milestones:
        if not isinstance(milestone, dict):
            raise ValueError("frontier milestone policy is malformed")
        deadline = milestone.get("deadline_at")
        milestone_id = milestone.get("id")
        if (
            isinstance(deadline, str)
            and isinstance(milestone_id, str)
            and _parse_runtime_timestamp(deadline, "milestone deadline") <= now
            and milestone_id not in completed_ids
        ):
            _frontier_stop(
                theorem_id, ledger,
                f"frontier milestone deadline missed: {milestone_id}",
                condition="milestone_deadline_missed",
            )
    # The ledger admits one active dynamic claim for this policy. Also reject
    # any independently injected active claim rows mapped to the same policy.
    if claim is not None:
        active_for_policy = {
            row.get("claim_id")
            for row in load_claims()
            if row.get("runtime_protocol") == RUNTIME_PROTOCOL
            and row.get("lane", IMPLEMENTATION_LANE) == IMPLEMENTATION_LANE
            and row.get("frontier_policy_sha256") == policy.get("policy_sha256")
            and row.get("status") in {"preparing", "live", "draining", "finished"}
            and (app_server_worker_is_live(row) or app_server_child_is_live(row))
        }
        active_for_policy.add(claim.get("claim_id"))
        concurrency_limit = budget.get("concurrency_limit")
        if not isinstance(concurrency_limit, int) or len(active_for_policy) > concurrency_limit:
            _frontier_stop(
                theorem_id, ledger, "frontier concurrency limit is exceeded",
                condition="any_resource_budget_exhausted",
            )
    if claim is not None:
        _persist_frontier_runtime(theorem_id, ledger)
    return ledger


def require_claim_focus_runtime_current(
    item: dict[str, Any],
    claim: dict[str, Any],
    theorem_nodes: dict[str, dict[str, Any]] | None = None,
    *,
    boundary: str = "runtime_refresh",
) -> dict[str, Any]:
    decision = require_claim_focus_current(item, claim, theorem_nodes)
    # Exception resources belong to the assigned proof implementation
    # principal. Independent read-only review consumes the frozen ledger but
    # cannot impersonate that principal or spend its proof budget.
    runtime_claim = (
        claim if claim.get("lane", IMPLEMENTATION_LANE) == IMPLEMENTATION_LANE
        else None
    )
    _require_frontier_runtime(
        item, decision, claim=runtime_claim, boundary=boundary
    )
    return decision


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


def read_bounded_runtime_file(
    path: Path, label: str, *, max_bytes: int
) -> tuple[bytes, str]:
    """Read a scheduler-bound regular file only when its size is bounded."""
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise ValueError(f"{label} is missing or unsafe") from exc
    try:
        metadata = os.fstat(descriptor)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or metadata.st_size <= 0
            or metadata.st_size > max_bytes
        ):
            raise ValueError(f"{label} size is outside the scheduler limit")
        chunks: list[bytes] = []
        remaining = metadata.st_size
        while remaining:
            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
            if not chunk:
                raise ValueError(f"{label} was truncated while reading")
            chunks.append(chunk)
            remaining -= len(chunk)
        if os.read(descriptor, 1):
            raise ValueError(f"{label} grew while reading")
        data = b"".join(chunks)
    finally:
        os.close(descriptor)
    return data, hashlib.sha256(data).hexdigest()


def worker_handoff_archive_path(claim: dict[str, Any]) -> Path:
    """Return the immutable scheduler-owned handoff path for one worker claim."""
    claim_id = claim.get("claim_id")
    if not isinstance(claim_id, str) or CLAIM_ID_RE.fullmatch(claim_id) is None:
        raise ValueError("implementation claim id is malformed")
    return RUNTIME / "worker-handoffs" / f"{claim_id}.json"


def parse_worker_handoff(payload: bytes, claim: dict[str, Any]) -> dict[str, Any]:
    """Parse one bounded handoff while rejecting duplicate JSON fields."""
    if not payload or len(payload) > MAX_WORKER_HANDOFF_BYTES:
        raise ValueError("worker handoff size is outside the scheduler limit")

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"worker handoff contains duplicate key {key!r}")
            result[key] = value
        return result

    try:
        packet = json.loads(
            payload.decode("utf-8"), object_pairs_hook=reject_duplicates
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("worker handoff is not UTF-8 JSON") from exc
    if (
        not isinstance(packet, dict)
        or packet.get("item_id") != claim.get("item_id")
        or packet.get("state") != "[_]"
        or packet.get("base_revision") != claim.get("base_revision")
    ):
        raise ValueError("worker handoff identity is invalid")
    return packet


def require_safe_handoff_archive_parent(*, create: bool) -> Path:
    """Return the canonical archive directory after rechecking its ancestry."""
    validate_runtime_root()
    directory = RUNTIME / "worker-handoffs"
    if create:
        directory.mkdir(parents=True, exist_ok=True)
    validate_runtime_root()
    if (
        directory.is_symlink()
        or not directory.is_dir()
        or not directory.resolve().is_relative_to(RUNTIME.resolve())
    ):
        raise ValueError("worker handoff archive directory is unsafe")
    return directory


def read_handoff_archive_bytes(directory: Path, name: str) -> bytes:
    """Read one archive leaf through a no-follow directory descriptor."""
    directory_fd = os.open(
        directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    )
    try:
        descriptor = os.open(
            name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory_fd
        )
        try:
            metadata = os.fstat(descriptor)
            if (
                not stat.S_ISREG(metadata.st_mode)
                or metadata.st_size <= 0
                or metadata.st_size > MAX_WORKER_HANDOFF_BYTES
            ):
                raise ValueError("persisted worker handoff is not a bounded regular file")
            chunks: list[bytes] = []
            remaining = metadata.st_size
            while remaining:
                chunk = os.read(descriptor, min(remaining, 1024 * 1024))
                if not chunk:
                    raise ValueError("persisted worker handoff was truncated while reading")
                chunks.append(chunk)
                remaining -= len(chunk)
            if os.read(descriptor, 1):
                raise ValueError("persisted worker handoff grew while reading")
            return b"".join(chunks)
        finally:
            os.close(descriptor)
    finally:
        os.close(directory_fd)


def create_handoff_archive_bytes(directory: Path, name: str, payload: bytes) -> None:
    """Create one immutable archive leaf without replacing an existing name."""
    directory_fd = os.open(
        directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    )
    descriptor: int | None = None
    created = False
    complete = False
    try:
        descriptor = os.open(
            name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
            dir_fd=directory_fd,
        )
        created = True
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise OSError("short write while persisting worker handoff")
            view = view[written:]
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = None
        os.fsync(directory_fd)
        complete = True
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if created and not complete:
            try:
                os.unlink(name, dir_fd=directory_fd)
                os.fsync(directory_fd)
            except FileNotFoundError:
                pass
        os.close(directory_fd)


def persist_worker_handoff(
    claim: dict[str, Any], payload: bytes
) -> tuple[Path, str, int]:
    """Freeze exact validated worker bytes before its recyclable slot is released."""
    directory = require_safe_handoff_archive_parent(create=True)
    path = worker_handoff_archive_path(claim)
    if path.parent.absolute() != directory.absolute():
        raise ValueError("worker handoff archive path is not scheduler-canonical")
    parse_worker_handoff(payload, claim)
    digest = hashlib.sha256(payload).hexdigest()
    try:
        create_handoff_archive_bytes(directory, path.name, payload)
    except FileExistsError:
        existing = read_handoff_archive_bytes(directory, path.name)
        if existing != payload or hashlib.sha256(existing).hexdigest() != digest:
            raise ValueError(
                "immutable worker handoff conflicts with existing scheduler bytes"
            )
    return path, digest, len(payload)


def read_persisted_worker_handoff(
    claim: dict[str, Any]
) -> tuple[bytes, str, Path]:
    """Reload one exact handoff without trusting a reused worker workspace."""
    directory = require_safe_handoff_archive_parent(create=False)
    expected = worker_handoff_archive_path(claim)
    value = claim.get("worker_handoff_path")
    if not isinstance(value, str) or not value:
        raise ValueError("implementation claim lacks its persisted worker handoff")
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    if path.absolute() != expected.absolute():
        raise ValueError("worker handoff path is not scheduler-canonical")
    expected_digest = claim.get("worker_handoff_sha256")
    expected_size = claim.get("worker_handoff_size")
    if (
        claim.get("worker_handoff_archive_schema")
        != WORKER_HANDOFF_ARCHIVE_SCHEMA
        or path.parent.absolute() != directory.absolute()
        or not isinstance(expected_digest, str)
        or re.fullmatch(r"[0-9a-f]{64}", expected_digest) is None
        or not isinstance(expected_size, int)
        or isinstance(expected_size, bool)
        or expected_size <= 0
    ):
        raise ValueError("implementation claim lacks a complete worker handoff binding")
    try:
        data = read_handoff_archive_bytes(directory, path.name)
    except OSError as exc:
        raise ValueError("persisted worker handoff is missing or unsafe") from exc
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected_digest or len(data) != expected_size:
        raise ValueError("persisted worker handoff disagrees with its claim binding")
    parse_worker_handoff(data, claim)
    return data, digest, path


def authoritative_head_revision() -> str:
    """Return the commit currently owned by the scheduler checkout."""
    return run(["git", "rev-parse", "--verify", "HEAD^{commit}"]).stdout.strip()


@functools.lru_cache(maxsize=2)
def _phase_acceptance_contract_record_at(revision: str) -> dict[str, Any]:
    try:
        record = acceptance_evidence.load_head_contract(
            ROOT, PHASE_ACCEPTANCE_CONTRACT_SHA256
        )
    except acceptance_evidence.EvidenceError as exc:
        fail(str(exc))
    if (
        record.get("revision") != revision
        or authoritative_head_revision() != revision
    ):
        fail("authoritative HEAD changed while loading the phase acceptance contract")
    return record


def phase_acceptance_contract_record() -> dict[str, Any]:
    # One tick may checkpoint and advance HEAD before allocating its review
    # tail. Key the cache by commit so that evidence selection never carries a
    # pre-checkpoint authority record into the new HEAD.
    return _phase_acceptance_contract_record_at(authoritative_head_revision())


def review_authority_contract_record(review_manifest: dict[str, Any]) -> dict[str, Any]:
    """Reload the immutable contract snapshot bound by one completed review."""
    authority = review_manifest.get("authority_revision")
    manifest_contract = review_manifest.get("contract")
    if (
        not isinstance(authority, str)
        or re.fullmatch(r"[0-9a-f]{40}", authority) is None
        or not isinstance(manifest_contract, dict)
        or manifest_contract.get("path")
        != PHASE_ACCEPTANCE_CONTRACTS.relative_to(ROOT).as_posix()
        or manifest_contract.get("sha256") != PHASE_ACCEPTANCE_CONTRACT_SHA256
    ):
        raise ValueError("review manifest lacks an exact contract authority binding")
    try:
        record = acceptance_evidence.load_head_contract(
            ROOT, PHASE_ACCEPTANCE_CONTRACT_SHA256, revision=authority
        )
    except acceptance_evidence.EvidenceError as exc:
        raise ValueError(str(exc)) from exc
    if (
        record.get("revision") != authority
        or record.get("git_tree") != review_manifest.get("authority_tree")
        or record.get("path") != manifest_contract.get("path")
        or record.get("sha256") != manifest_contract.get("sha256")
        or record.get("git_blob") != manifest_contract.get("git_blob")
    ):
        raise ValueError("review manifest contract authority snapshot is stale")
    return record


def require_review_compatible_with_current_head(
    item: dict[str, Any],
    review_manifest: dict[str, Any],
    role_map: dict[str, Any],
    validator: dict[str, Any],
) -> str:
    """Permit unrelated commits while rejecting every target-relevant drift."""
    compatible_head = authoritative_head_revision()
    current_contract = phase_acceptance_contract_record()
    manifest_contract = review_manifest.get("contract")
    manifest_blueprint = review_manifest.get("blueprint")
    blueprint_relative = BLUEPRINT.relative_to(ROOT).as_posix()
    current_blueprint_bytes = git_object_bytes(
        f"{compatible_head}:{blueprint_relative}"
    )
    current_blueprint_blob = hashlib.sha1(
        f"blob {len(current_blueprint_bytes)}\0".encode() + current_blueprint_bytes
    ).hexdigest()
    if (
        current_contract.get("revision") != compatible_head
        or not isinstance(manifest_contract, dict)
        or current_contract.get("path") != manifest_contract.get("path")
        or current_contract.get("sha256") != manifest_contract.get("sha256")
        or current_contract.get("git_blob") != manifest_contract.get("git_blob")
        or not isinstance(manifest_blueprint, dict)
        or manifest_blueprint.get("path") != blueprint_relative
        or manifest_blueprint.get("sha256")
        != hashlib.sha256(current_blueprint_bytes).hexdigest()
        or manifest_blueprint.get("git_blob") != current_blueprint_blob
        or review_manifest.get("blueprint_sha256")
        != manifest_blueprint.get("sha256")
    ):
        raise ValueError("review authority contract or v2 blueprint changed after review allocation")
    current_role_map = build_review_role_map(item, str(review_manifest.get("base_revision", "")))
    current_validator = select_review_validator(
        item,
        str(review_manifest.get("base_revision", "")),
        require_base_blob_match=False,
    )
    role_fields = {
        "schema_version", "item_id", "theorem_id", "phase", "base_revision",
        "contract_sha256", "contract_git_blob", "phase_receipt_path",
        "phase_receipt_sha256", "artifacts",
    }
    validator_fields = {
        "item_id", "theorem_id", "phase", "base_revision", "contract_sha256",
        "validator_path", "validator_sha256", "validator_git_blob",
        "validator_git_mode", "argv", "cwd", "network_policy",
        "repo_write_access", "isolated_scratch_write_access", "shell_interpolation",
    }
    if (
        {field: current_role_map.get(field) for field in role_fields}
        != {field: role_map.get(field) for field in role_fields}
        or {field: current_validator.get(field) for field in validator_fields}
        != {field: validator.get(field) for field in validator_fields}
    ):
        raise ValueError("review target artifacts or validator changed after review allocation")
    try:
        current_graph = json.loads(
            git_object_bytes(
                f"{compatible_head}:{THEOREM_DAG_V2.relative_to(ROOT).as_posix()}"
            )
        )
    except json.JSONDecodeError as exc:
        raise ValueError("current authoritative theorem DAG is malformed") from exc
    if not isinstance(current_graph, dict):
        raise ValueError("current authoritative theorem DAG is malformed")
    current_nodes = {
        node.get("theorem_id"): node
        for node in current_graph.get("theorems", [])
        if isinstance(node, dict)
    }
    current_node = current_nodes.get(item.get("theorem_id"))
    authority_dag = json.loads(
        git_object_bytes(
            f"{review_manifest.get('authority_revision')}:{THEOREM_DAG_V2.relative_to(ROOT).as_posix()}"
        )
    )
    authority_nodes = {
        node.get("theorem_id"): node
        for node in authority_dag.get("theorems", [])
        if isinstance(node, dict)
    }
    node_fields = {
        "theorem_id", "v2_execution_rank", "topological_layer",
        "direct_hard_parents", "transitive_hard_ancestors",
        "direct_reuse_hint_ids", "shared_lemma_group_ids",
        "dependency_context_sha256", "focus_eligibility",
    }
    authority_node = authority_nodes.get(item.get("theorem_id"))
    if (
        not isinstance(current_node, dict)
        or not isinstance(authority_node, dict)
        or {key: current_node.get(key) for key in node_fields}
        != {key: authority_node.get(key) for key in node_fields}
    ):
        raise ValueError("review target DAG node changed after review allocation")
    theorem_id = item.get("theorem_id")
    related_specs = (
        ("hard_edges", "edge_id", ("parent_theorem_id", "child_theorem_id")),
        ("reuse_hints", "hint_id", ("provider_theorem_id", "consumer_theorem_id")),
        ("shared_lemma_groups", "group_id", ("member_theorem_ids",)),
    )
    for table, identity, relation_fields in related_specs:
        current_rows = current_graph.get(table, [])
        authority_rows = authority_dag.get(table, [])
        if not isinstance(current_rows, list) or not isinstance(authority_rows, list):
            raise ValueError(f"review target DAG {table} table is malformed")

        def related(row: Any) -> bool:
            if not isinstance(row, dict):
                return False
            return any(
                theorem_id in row.get(field, [])
                if isinstance(row.get(field), list)
                else row.get(field) == theorem_id
                for field in relation_fields
            )

        current_related = {
            row.get(identity): row for row in current_rows if related(row)
        }
        authority_related = {
            row.get(identity): row for row in authority_rows if related(row)
        }
        if (
            None in current_related
            or None in authority_related
            or current_related != authority_related
        ):
            raise ValueError(f"review target DAG {table} changed after review allocation")
    if authoritative_head_revision() != compatible_head:
        raise ValueError("authoritative HEAD changed during review compatibility check")
    return compatible_head


def phase_acceptance_contract() -> dict[str, Any]:
    return phase_acceptance_contract_record()["contract"]


def phase_contract(item: dict[str, Any]) -> dict[str, Any]:
    rows = [
        row for row in phase_acceptance_contract().get("phases", [])
        if isinstance(row, dict) and row.get("phase") == item.get("phase")
    ]
    if len(rows) != 1:
        fail(f"phase acceptance contract is missing exactly one {item.get('phase')} row")
    return rows[0]


def phase_validator_candidate_paths(item: dict[str, Any]) -> set[str]:
    """Resolve current and superseded validator paths protected by the contract."""
    row = phase_contract(item)
    current = row.get("validator_authorities")
    superseded = row.get("superseded_validator_sources")
    if not isinstance(current, list) or not isinstance(superseded, list):
        raise ValueError("phase contract lacks validator authority registries")
    candidates = [*current, *superseded]
    if not candidates:
        raise ValueError("phase contract has no protected validator sources")
    paths: set[str] = set()
    for candidate in candidates:
        pattern = candidate.get("path_pattern") if isinstance(candidate, dict) else None
        if not isinstance(pattern, str) or not pattern:
            raise ValueError("phase contract contains a malformed validator candidate")
        relative = pattern.replace("{theorem_id}", str(item.get("theorem_id", "")))
        path = Path(relative)
        if (
            "{" in relative
            or "}" in relative
            or path.is_absolute()
            or ".." in path.parts
            or path.as_posix() != relative
            or not (
                relative.startswith(str(item["owned_paths"][0]).rstrip("/") + "/")
                or relative.startswith("scripts/stage1_phase_validators/")
            )
        ):
            raise ValueError("phase contract validator source escapes protected namespaces")
        paths.add(relative)
    if len(paths) != len(candidates):
        raise ValueError("phase contract contains duplicate validator sources")
    return paths


def reject_worker_validator_changes(item: dict[str, Any], changed_paths: list[str]) -> None:
    """Keep scheduler-selected validators immutable across worker handoffs."""
    changed_candidates = sorted(
        phase_validator_candidate_paths(item).intersection(changed_paths)
    )
    if changed_candidates:
        raise ValueError(
            "worker handoff changes scheduler-owned validator candidate(s): "
            + ", ".join(changed_candidates)
        )


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


def build_staged_worker_role_map(
    item: dict[str, Any],
    base_revision: str,
    workspace: Path,
    changed_paths: list[str],
) -> dict[str, Any]:
    """Resolve the scheduler-owned contract against one unmerged worker delta."""
    try:
        return acceptance_evidence.resolve_staged_role_map(
            ROOT,
            phase_acceptance_contract_record(),
            workspace=workspace,
            declared_delta_paths=changed_paths,
            item_id=item["id"],
            theorem_id=item["theorem_id"],
            phase=item["phase"],
            base_revision=base_revision,
        )
    except acceptance_evidence.EvidenceError as exc:
        raise ValueError(str(exc)) from exc


def reject_research_only_proof_delta(
    item: dict[str, Any], focus: dict[str, Any], role_map: dict[str, Any],
    workspace: Path,
) -> None:
    """Reject proof-bearing Lean bytes before a research-only handoff is copied."""

    if focus.get("execution_disposition") != "research_required":
        return
    validator_path = ROOT / "scripts/stage1_phase_validators/current.py"
    spec = importlib.util.spec_from_file_location(
        "stage1_phase_validator_research_gate", validator_path
    )
    if spec is None or spec.loader is None:
        raise ValueError("current Stage1 phase validator is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    artifacts = role_map.get("artifacts", [])
    artifact_bytes: dict[str, bytes] = {}
    for path in role_map.get("staged_delta_paths", []):
        if not isinstance(path, str) or not path.endswith(".lean"):
            continue
        rows = [
            row for row in artifacts
            if isinstance(row, dict) and row.get("path") == path
        ]
        if len(rows) != 1:
            raise ValueError(
                "research-only changed Lean path is not a bound phase artifact"
            )
        artifact_bytes[path] = contained_regular_file(
            workspace, path, str(item["owned_paths"][0]) + "/"
        ).read_bytes()
    try:
        module.reject_research_proof_construction(
            str(item["phase"]), focus, role_map, artifact_bytes
        )
    except module.ValidationError as exc:
        raise ValueError(str(exc)) from exc


def select_review_validator(
    item: dict[str, Any], base_revision: str, *, require_base_blob_match: bool = True
) -> dict[str, Any]:
    try:
        return acceptance_evidence.select_validator_recipe(
            ROOT,
            phase_acceptance_contract_record(),
            item_id=item["id"],
            theorem_id=item["theorem_id"],
            phase=item["phase"],
            base_revision=base_revision,
            require_base_blob_match=require_base_blob_match,
        )
    except acceptance_evidence.EvidenceError as exc:
        fail(str(exc))


def task_prompt(item: dict[str, Any], workspace: Path) -> str:
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
    focus_decision = focus_decision_for_item(item, theorem_nodes)
    disposition = str(focus_decision.get("execution_disposition", ""))
    prompt_item = dict(item)
    prompt_deliverable = FOCUS_DELIVERABLES.get(disposition, {}).get(
        str(item.get("phase", ""))
    )
    if not isinstance(prompt_deliverable, str):
        fail("current focus disposition has no safe prompt deliverable for this phase")
    prompt_item["deliverable"] = prompt_deliverable
    prompt_item["authoritative_checklist_deliverable"] = item.get("deliverable")
    prompt_item["deliverable_interpretation"] = "current_v2_focus_policy_override"
    item_json = json.dumps(prompt_item, ensure_ascii=False, indent=2)
    focus_context = json.dumps(focus_decision, ensure_ascii=False, indent=2)
    return f"""You are a Stage1 v2 worker for exactly one Lean 4 theorem execution task.

Repository root: {workspace}
Work only inside this worker automation clone: {workspace}
Do not edit the scheduler's authoritative checkout directly: {ROOT}

This thread has a real persisted Codex `/goal`, created through app-server
`thread/goal/set`, for exactly the assigned item below. `Docs/Stage1_Blueprint_v2.md`
is the sole requirements and task-state authority. Do not claim theorem completion
without every gate and kernel evidence defined there.

Resume the active `/goal` now. If your current context has reached capacity,
write the required target-scoped artifact or self-test handoff immediately and
exit cleanly so the scheduler can integrate it and continue the goal in a
fresh worker context. Do not wait for an interactive operator message.

Your assigned item is the only item you may claim:
{item_json}

The authoritative v2 dependency/reuse context for this theorem is:
{dependency_context}

The scheduler-validated focus admission for this exact phase is:
{focus_context}

Required work:
1. Read Docs/Stage1_Blueprint_v2.md, skills/execute-stage1-v2/SKILL.md, the target manifest entry, and the target node in Docs/Stage1_Theorem_DAG_v2.json.
2. Stay inside the focus admission above. Missing eligibility and `research_required` permit discovery only through anchor audit, never proof, validation, release, or theorem-completion claims. `organize_or_integrate` means locate, pin, match, import or transport, replay, and validate an existing exact machine proof rather than inventing one. Frontier proof work requires a valid scheduler-owned, independently reviewed `frontier_exception`; worker-authored probability never authorizes it.
3. Complete the assigned phase with real source, Lean, and/or evidence artifacts under the item's owned path. You may inspect shared read-only sources, but never modify another target's owned path. Never use sorry, axiom, placeholder, fake results, or a broadened/substituted theorem.
   Before proof work, traverse every ID in `parent_inspection_order` exactly once and in that order; it is the complete direct/transitive closure in ascending v2 rank, not only the nearest parents. Inspect each parent's authoritative phase state, receipts, declaration bodies, and reusable artifacts. Accepted reuse is only `reused_exact` or `reused_with_transport`. Prefer an exact already-proved body over reproving it: import it when possible; otherwise copy only the minimal proof term/declaration into the consumer-owned path and record both the original provider bytes and the consumer copy/checked transport. A checked transport must bind both statement fingerprints, the provider source bytes, and the consumer-owned import/wrapper bytes, then re-elaborate the consumer under the pinned kernel and bind both byte hashes. A proof worker must not invent the later consumer-validation receipt; that receipt becomes mandatory when the `validation` phase performs its own replay. Provider checkbox/receipt state is observation only: copying never transfers parent acceptance or evidence credit, and a `[_]` parent is guidance only unless the hard edge's material contract permits provisional consumption.
   Create or refresh the target-owned dependency-reuse-ledger.json required by the execution skill. Use schema {DEPENDENCY_LEDGER_SCHEMA} and exactly the graph digest/context IDs above. The ledger must include inspections, reuse_decisions, and unresolved_compatibility_obligations as specified by the skill. Empty parent/hint/group closure still requires an empty audited ledger. A reuse_hint or [_] ancestor is informative only and cannot transfer proof credit.
4. The HEAD phase contract at `Docs/Stage1_Phase_Acceptance_Contracts.json` is
   mandatory for new evidence. Produce exactly one phase receipt with schema
   `stage1-node-receipt/1.0`, every contract-required field, and complete
   path/SHA-256/Git-blob bindings for every role the contract selects. The
   scheduler owns every declared validator candidate: use the one already
   present in HEAD, but never create, refresh, rename, replace, or delete any
   validator candidate. Record its exact argv/result in the receipt and handoff.
   Its stdout must be exactly one JSON object with schema
   `stage1-validator-semantic-result/1.0` and the exact fields required by the
   scheduler; legacy prose stdout, exit code zero alone, or an undeclared
   adapter cannot support master acceptance. If HEAD has zero or multiple
   validator candidates, leave no self-test handoff and report the scheduler
   ownership blocker instead of manufacturing a candidate. The worker may
   report a truthful negative result, but must never infer `phase_accepted`
   from command success.
5. Run the smallest real validation available and record exact commands/results in the owned artifact.
   The worker clone reuses the canonical pinned Lean `.lake` artifacts when available. Do not run
   `lake update`, `lake build`, dependency `git clone`/`git fetch`, or otherwise mutate `.lake`;
   those actions are neither a pinned validation nor valid worker evidence. Use the existing
   toolchain with `lake env lean` for narrowly scoped elaboration checks, and record a missing
   artifact as a blocker rather than fetching a moving dependency.
6. Do not edit focus-eligibility.json, Docs/Stage1_Phase_DAG_v2.json, Docs/Stage1_Theorem_DAG_v2.json, the blueprint, the generated checklist, or any item state. Focus admission is scheduler/master-owned; you are a worker, never the master.
7. If and only if your assigned phase is genuinely self-tested, write `.stage1-worker-selftest.json` at the workspace root with item_id, changed_paths, commands, output_summary, base_revision, known_failures, and `state: "[_]"`. Otherwise leave no self-test manifest and explain the blocker in an owned artifact.
8. Do not commit, push, launch tmux, launch `codex exec`, create nested agents, or modify unrelated targets. The app-server integration lane will inspect this clone.
"""


def worker_goal_objective(item: dict[str, Any]) -> str:
    return (
        f"Execute {item['id']} for {item['theorem_id']} from the sole task-state authority "
        "Docs/Stage1_Blueprint_v2.md. Obey its scheduler-owned focus admission, follow the exact DAG claim order, "
        "prefer locating, pinning, importing, replaying, and validating existing exact machine proofs, "
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
    focus_contract: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": REVIEW_BINDING_SCHEMA,
        "claim_id": claim_id,
        "item_id": item["id"],
        "theorem_id": item["theorem_id"],
        "phase": item["phase"],
        "base_revision": base_revision,
        "blueprint_sha256": sha256_file(BLUEPRINT),
        "blueprint_git_blob": run(
            ["git", "rev-parse", f"HEAD:{BLUEPRINT.relative_to(ROOT).as_posix()}"]
        ).stdout.strip(),
        "theorem_dag_sha256": sha256_file(THEOREM_DAG_V2),
        "prompt_sha256": hashlib.sha256(prompt_text.encode()).hexdigest(),
        "objective_sha256": hashlib.sha256(objective.encode()).hexdigest(),
        "artifact_digests": {
            row["path"]: row["sha256"] for row in role_map["artifacts"]
        },
        "validator_recipe_sha256s": [validator["recipe_sha256"]],
        "focus_execution": focus_contract,
        "focus_contract_sha256": canonical_json_sha256(focus_contract),
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
    worker_principal: str | None = None,
    frontier_scratch: Path | None = None,
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
    if lane != IMPLEMENTATION_LANE and frontier_scratch is not None:
        fail("frontier scratch is restricted to the implementation lane")
    if thread_id is not None and (
        not isinstance(thread_id, str)
        or not thread_id
        or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,199}", thread_id) is None
    ):
        fail("resume thread id is malformed")
    if worker_principal is None:
        worker_principal = scheduler_worker_principal_id()
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:@-]{0,199}", worker_principal) is None:
        fail("worker principal is malformed")
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
        "--worker-principal", worker_principal,
    ]
    if binding_path is not None:
        argv.extend(["--binding", str(binding_path)])
    if thread_id is not None:
        argv.extend(["--thread-id", thread_id])
    if frontier_scratch is not None:
        if (
            frontier_scratch.is_symlink()
            or not frontier_scratch.is_dir()
            or not frontier_scratch.resolve().is_relative_to(RUNTIME.resolve())
        ):
            fail("frontier scratch is unavailable or outside scheduler storage")
        argv.extend(["--scratch", str(frontier_scratch)])
    return argv


def launch_app_server_worker(
    argv: list[str], *, delay_seconds: float = 0.0, scratch: Path | None = None
) -> int:
    """Launch without tmux/nohup/shell and return the process-group leader."""
    if delay_seconds < 0 or delay_seconds > APP_SERVER_LAUNCH_STAGGER_SECONDS:
        fail("app-server launch delay is outside the bounded cohort cadence")
    if delay_seconds:
        time.sleep(delay_seconds)
    environment = None
    if scratch is not None:
        if scratch.is_symlink() or not scratch.is_dir():
            fail("frontier launch scratch is unavailable or unsafe")
        environment = os.environ.copy()
        environment["TMPDIR"] = str(scratch)
        environment["TMP"] = str(scratch)
        environment["TEMP"] = str(scratch)
    process = subprocess.Popen(
        argv,
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True,
        env=environment,
    )
    return process.pid


def launch_review_app_server_worker(
    argv: list[str],
    *,
    reviewer_uid: int,
    workspace: Path,
    read_paths: list[Path],
    write_paths: list[Path],
    delay_seconds: float = 0.0,
    claim: dict[str, Any] | None = None,
    claims: list[dict[str, Any]] | None = None,
) -> int:
    """Launch a review client as the configured distinct service account."""
    if reviewer_uid < 1 or reviewer_uid == os.geteuid():
        fail("review launch requires a distinct non-root OS UID")
    if delay_seconds < 0 or delay_seconds > APP_SERVER_LAUNCH_STAGGER_SECONDS:
        fail("app-server launch delay is outside the bounded cohort cadence")
    if delay_seconds:
        time.sleep(delay_seconds)
    if os.geteuid() != 0:
        fail(
            "review service-account launch requires a root-owned supervisor; "
            "same-UID review fallback is forbidden"
        )
    try:
        if claim is None or claims is None:
            fail("review ACL provisioning requires its durable scheduler claim")

        def bind_snapshot_before_grant(snapshots: dict[Path, bytes]) -> None:
            persist_review_acl_snapshot(
                claim, snapshots, reviewer_uid=reviewer_uid
            )
            save_claims(claims)

        access_snapshots = provision_review_access(
            reviewer_uid=reviewer_uid,
            workspace=workspace,
            read_paths=read_paths,
            write_paths=write_paths,
            snapshot_callback=bind_snapshot_before_grant,
        )
        if (
            not access_snapshots
            or claim.get("review_acl_snapshot_state") != "active"
        ):
            fail("review access provisioning lacks durable authenticated ACL evidence")
        if not Path("/usr/bin/setpriv").is_file():
            fail("root-owned review supervisor lacks /usr/bin/setpriv")
        process = subprocess.Popen(
            [
                "/usr/bin/setpriv",
                f"--reuid={reviewer_uid}",
                f"--regid={reviewer_uid}",
                "--clear-groups",
                "--no-new-privs",
                "--",
                *argv,
            ],
            cwd=workspace,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            close_fds=True,
        )
        claim["pid"] = process.pid
        claim["pid_start_ticks"] = process_start_ticks(process.pid)
        claim["client_started_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        save_claims(claims)
        try:
            require_process_effective_uid(process.pid, reviewer_uid, "review client")
        except BaseException:
            try:
                os.killpg(process.pid, 15)
            except ProcessLookupError:
                pass
            raise
        return process.pid
    except BaseException:
        # No process was returned to the caller. Restore through the same
        # durable lifecycle path used after scheduler crash recovery.
        if claim is not None:
            if claim.get("review_acl_snapshot_state") == "active":
                restore_stopped_review_acl(claim)
            if claims is not None:
                save_claims(claims)
        raise


def launch_stagger_delay(started_count: int) -> float:
    if started_count < 0:
        fail("app-server launch sequence is negative")
    return APP_SERVER_LAUNCH_STAGGER_SECONDS if started_count else 0.0


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
                if (
                    not app_server_worker_is_live(claim)
                    and not app_server_child_is_live(claim)
                ):
                    restore_stopped_review_acl(claim)
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
        if (
            not app_server_worker_is_live(claim)
            and not app_server_child_is_live(claim)
        ):
            restore_stopped_review_acl(claim)
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
        "Docs/Stage1_Phase_DAG_v2.json",
        "Docs/Stage1_Target_Membership_v2.json", "Docs/Stage1_Focus_Eligibility_Schema.json",
        "scripts/stage1_focus_eligibility.py", "skills/execute-stage1-v2/SKILL.md",
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
    """Create a detached, clean checkout; access is provisioned at launch."""
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


def _acl_snapshot(path: Path) -> bytes:
    result = subprocess.run(
        ["/usr/bin/getfacl", "-cpn", "--", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        fail(f"cannot snapshot review ACL for {path}: {detail or 'unknown error'}")
    return result.stdout


def _restore_acl(path: Path, snapshot: bytes) -> None:
    result = subprocess.run(
        ["/usr/bin/setfacl", "--restore=-"],
        cwd=Path("/"),
        input=(f"# file: {path.as_posix().lstrip('/')}\n".encode() + snapshot),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        fail(f"cannot restore review ACL for {path}: {detail or 'unknown error'}")


def provision_review_access(
    *,
    reviewer_uid: int,
    workspace: Path,
    read_paths: list[Path],
    write_paths: list[Path],
    snapshot_callback: Callable[[dict[Path, bytes]], None] | None = None,
) -> dict[Path, bytes]:
    """Grant only traversal/read plus claim-scoped writable endpoint ACLs.

    The repository and runtime deliberately remain 0700.  A root-owned
    supervisor must install narrow POSIX ACL entries immediately before it
    drops privileges; chmod/world-write fallbacks are forbidden.
    """
    if os.geteuid() != 0:
        fail(
            "review access provisioning requires a root-owned supervisor; "
            "same-UID review fallback is forbidden"
        )
    if reviewer_uid < 1 or reviewer_uid == os.geteuid():
        fail("review access requires a distinct non-root OS UID")
    if shutil.which("setfacl") != "/usr/bin/setfacl" or shutil.which("getfacl") != "/usr/bin/getfacl":
        fail("review access requires root-owned /usr/bin POSIX ACL tools")
    root = ROOT.absolute()
    runtime = RUNTIME.absolute()
    workspace = workspace.absolute()
    if (
        workspace.is_symlink()
        or not workspace.is_dir()
        or not workspace.resolve().is_relative_to(runtime.resolve())
    ):
        fail("review workspace is not a detached scheduler-owned directory")
    allowed_reads = {workspace, *(path.absolute() for path in read_paths)}
    allowed_writes = {path.absolute() for path in write_paths}
    if not allowed_reads or not allowed_writes:
        fail("review access plan is empty")
    for path in allowed_reads | allowed_writes:
        if path.is_symlink():
            fail(f"review access path is a symlink: {path}")
    for path in allowed_writes:
        if not path.parent.resolve().is_relative_to(runtime.resolve()):
            fail("review writable endpoint escapes scheduler runtime")

    access: dict[Path, str] = {}

    def merge(path: Path, permissions: str) -> None:
        current = access.get(path, "---")
        access[path] = "".join(
            flag if flag in current or flag in permissions else "-" for flag in "rwx"
        )

    # Traverse only the absolute ancestors needed to reach the detached copy
    # and claim-scoped endpoints.  No ancestor receives read or write access.
    for leaf in allowed_reads | allowed_writes:
        current = leaf.parent
        while current != current.parent:
            merge(current, "--x")
            current = current.parent
    for path in allowed_reads:
        if not path.exists():
            fail(f"review read input is missing: {path}")
        if path.is_dir():
            for descendant in [path, *path.rglob("*")]:
                if descendant.is_symlink():
                    target = descendant.resolve(strict=True)
                    if not target.is_relative_to(path.resolve()):
                        fail(f"review detached workspace symlink escapes its copy: {descendant}")
                    # setfacl follows a symlink on Linux. Bind and restore the
                    # actual in-workspace inode rather than recording an
                    # ambiguous symlink pathname.
                    merge(target, "r-x" if target.is_dir() else "r--")
                    continue
                merge(descendant, "r-x" if descendant.is_dir() else "r--")
        else:
            merge(path, "r--")
    for path in allowed_writes:
        path.parent.mkdir(parents=True, exist_ok=True)
        merge(path.parent, "-wx")
        if path.exists():
            if not path.is_file():
                fail(f"review writable endpoint is not a regular file: {path}")
            merge(path, "rw-")

    snapshots = {path: _acl_snapshot(path) for path in access if path.exists()}
    if snapshot_callback is not None:
        snapshot_callback(snapshots)
    applied: list[Path] = []
    try:
        for path, permissions in sorted(access.items(), key=lambda row: len(row[0].parts)):
            if not path.exists():
                continue
            result = subprocess.run(
                ["/usr/bin/setfacl", "-m", f"u:{reviewer_uid}:{permissions}", "--", str(path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if result.returncode:
                detail = result.stderr.decode("utf-8", "replace").strip()
                fail(f"cannot provision review ACL for {path}: {detail or 'unknown error'}")
            applied.append(path)
    except BaseException:
        for path in reversed(applied):
            _restore_acl(path, snapshots[path])
        raise
    return snapshots


def restore_review_access(snapshots: dict[Path, bytes]) -> None:
    """Remove claim-scoped reviewer ACLs by restoring exact prior entries."""
    for path in sorted(snapshots, key=lambda row: len(row.parts), reverse=True):
        if path.exists() and not path.is_symlink():
            _restore_acl(path, snapshots[path])


def _review_acl_snapshot_path(claim_id: Any) -> Path:
    if not isinstance(claim_id, str) or CLAIM_ID_RE.fullmatch(claim_id) is None:
        raise ValueError("review ACL snapshot claim identity is malformed")
    return RUNTIME / "review-acl-snapshots" / f"{claim_id}.json"


def _review_acl_snapshot_payload(
    claim: dict[str, Any], snapshots: dict[Path, bytes], *, reviewer_uid: int
) -> dict[str, Any]:
    if claim.get("lane") != REVIEW_LANE:
        raise ValueError("review ACL snapshot cannot bind a non-review claim")
    if reviewer_uid < 1 or claim.get("runtime_principal_uid") != reviewer_uid:
        raise ValueError("review ACL snapshot principal disagrees with its claim")
    rows: list[dict[str, str]] = []
    for path, snapshot in sorted(snapshots.items(), key=lambda row: str(row[0])):
        absolute = path.absolute()
        if path.is_symlink() or not path.exists() or absolute != path:
            raise ValueError("review ACL snapshot path is missing or unsafe")
        rows.append({
            "path": str(absolute),
            "acl_base64": base64.b64encode(snapshot).decode("ascii"),
        })
    if not rows:
        raise ValueError("review ACL snapshot is empty")
    body: dict[str, Any] = {
        "schema_version": REVIEW_ACL_SNAPSHOT_SCHEMA,
        "claim_id": claim.get("claim_id"),
        "item_id": claim.get("item_id"),
        "reviewer_principal": claim.get("runtime_principal_id"),
        "reviewer_uid": reviewer_uid,
        "paths": rows,
    }
    return {**body, "payload_sha256": canonical_json_sha256(body)}


def persist_review_acl_snapshot(
    claim: dict[str, Any], snapshots: dict[Path, bytes], *, reviewer_uid: int
) -> Path:
    """Durably bind the pre-provision ACLs to one scheduler-owned claim."""
    validate_runtime_root()
    path = _review_acl_snapshot_path(claim.get("claim_id"))
    if path.is_symlink() or path.parent.is_symlink():
        raise ValueError("review ACL snapshot storage is unsafe")
    payload = _review_acl_snapshot_payload(
        claim, snapshots, reviewer_uid=reviewer_uid
    )
    encoded = (
        json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    if path.exists():
        if not path.is_file() or path.read_bytes() != encoded:
            raise ValueError("review ACL snapshot conflicts with durable state")
    else:
        durable_write_bytes(path, encoded)
        path.chmod(0o600)
    metadata = path.stat()
    if (
        path.is_symlink()
        or not stat.S_ISREG(metadata.st_mode)
        or stat.S_IMODE(metadata.st_mode) != 0o600
        or metadata.st_uid != os.geteuid()
    ):
        raise ValueError("review ACL snapshot is not scheduler-owned mode 0600")
    claim["review_acl_snapshot_path"] = str(path)
    claim["review_acl_snapshot_sha256"] = hashlib.sha256(encoded).hexdigest()
    claim["review_acl_payload_sha256"] = payload["payload_sha256"]
    claim["review_acl_snapshot_state"] = "active"
    claim["review_acl_snapshot_persisted_at"] = dt.datetime.now(
        dt.timezone.utc
    ).isoformat()
    return path


def _load_review_acl_snapshot(claim: dict[str, Any]) -> tuple[Path, dict[Path, bytes]]:
    expected_path = _review_acl_snapshot_path(claim.get("claim_id"))
    value = claim.get("review_acl_snapshot_path")
    expected_file_sha = claim.get("review_acl_snapshot_sha256")
    expected_payload_sha = claim.get("review_acl_payload_sha256")
    if (
        claim.get("lane") != REVIEW_LANE
        or claim.get("review_acl_snapshot_state") != "active"
        or not isinstance(value, str)
        or Path(value).absolute() != expected_path.absolute()
        or expected_path.is_symlink()
        or expected_path.parent.is_symlink()
        or not expected_path.is_file()
        or not expected_path.resolve().is_relative_to(RUNTIME.resolve())
        or not isinstance(expected_file_sha, str)
        or re.fullmatch(r"[0-9a-f]{64}", expected_file_sha) is None
        or not isinstance(expected_payload_sha, str)
        or re.fullmatch(r"[0-9a-f]{64}", expected_payload_sha) is None
    ):
        raise ValueError("review ACL snapshot binding is missing or unsafe")
    metadata = expected_path.stat()
    if (
        stat.S_IMODE(metadata.st_mode) != 0o600
        or metadata.st_uid != os.geteuid()
    ):
        raise ValueError("review ACL snapshot ownership or mode changed")
    encoded = expected_path.read_bytes()
    if hashlib.sha256(encoded).hexdigest() != expected_file_sha:
        raise ValueError("review ACL snapshot bytes were tampered")
    try:
        payload = json.loads(encoded.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("review ACL snapshot is not canonical JSON") from exc
    if (
        not isinstance(payload, dict)
        or encoded
        != (
            json.dumps(
                payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")
            )
            + "\n"
        ).encode("utf-8")
        or canonical_json_sha256(
            {key: value for key, value in payload.items() if key != "payload_sha256"}
        ) != expected_payload_sha
        or payload.get("payload_sha256") != expected_payload_sha
        or payload.get("schema_version") != REVIEW_ACL_SNAPSHOT_SCHEMA
        or payload.get("claim_id") != claim.get("claim_id")
        or payload.get("item_id") != claim.get("item_id")
        or payload.get("reviewer_principal") != claim.get("runtime_principal_id")
        or payload.get("reviewer_uid") != claim.get("runtime_principal_uid")
        or set(payload) != {
            "schema_version", "claim_id", "item_id", "reviewer_principal",
            "reviewer_uid", "paths", "payload_sha256",
        }
    ):
        raise ValueError("review ACL snapshot payload disagrees with its claim")
    rows = payload.get("paths")
    if not isinstance(rows, list) or not rows:
        raise ValueError("review ACL snapshot path list is malformed")
    snapshots: dict[Path, bytes] = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "acl_base64"}:
            raise ValueError("review ACL snapshot row is malformed")
        raw_path, encoded_acl = row.get("path"), row.get("acl_base64")
        if not isinstance(raw_path, str) or not isinstance(encoded_acl, str):
            raise ValueError("review ACL snapshot row is malformed")
        path = Path(raw_path)
        root = ROOT.absolute()
        allowed_root_lineage = (
            path == root
            or path.is_relative_to(root)
            or root.is_relative_to(path)
        )
        if (
            not path.is_absolute()
            or path != path.absolute()
            or path in snapshots
            or path.is_symlink()
            or not allowed_root_lineage
        ):
            raise ValueError("review ACL restore path is unsafe")
        try:
            snapshots[path] = base64.b64decode(encoded_acl, validate=True)
        except (ValueError, binascii.Error) as exc:
            raise ValueError("review ACL snapshot bytes are malformed") from exc
    return expected_path, snapshots


def review_claim_processes_are_dead(claim: dict[str, Any]) -> bool:
    """Require both recorded review process identities to have disappeared."""
    identities: list[tuple[Any, Any]] = [
        (claim.get("pid"), claim.get("pid_start_ticks"))
    ]
    status = worker_status(claim)
    if isinstance(status, dict):
        identities.append(
            (status.get("app_server_pid"), status.get("app_server_start_ticks"))
        )
    for pid, expected_start in identities:
        if not isinstance(pid, int) or isinstance(pid, bool) or pid < 1:
            continue
        observed_start = process_start_ticks(pid)
        if isinstance(expected_start, int) and observed_start == expected_start:
            return False
        if not isinstance(expected_start, int) and pid_alive(pid):
            return False
    return not app_server_worker_is_live(claim) and not app_server_child_is_live(claim)


def restore_review_acl_for_claim(claim: dict[str, Any]) -> bool:
    """Idempotently restore ACLs only after both review processes are dead."""
    if claim.get("lane") != REVIEW_LANE:
        return False
    if claim.get("review_acl_snapshot_state") == "restored":
        return False
    if claim.get("review_acl_snapshot_state") != "active":
        return False
    if not review_claim_processes_are_dead(claim):
        raise ValueError("refuse to restore review ACL while review process is live")
    path, snapshots = _load_review_acl_snapshot(claim)
    restore_review_access(snapshots)
    claim["review_acl_snapshot_state"] = "restored"
    claim["review_acl_snapshot_consumed_sha256"] = claim[
        "review_acl_snapshot_sha256"
    ]
    claim["review_acl_restored_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    return True


def restore_stopped_review_acl(claim: dict[str, Any]) -> bool:
    """Restore a review lease when possible and retain failures for recovery."""
    try:
        changed = restore_review_acl_for_claim(claim)
    except (OSError, ValueError, SystemExit) as exc:
        claim["review_acl_restore_error"] = str(exc)
        return False
    if changed:
        claim.pop("review_acl_restore_error", None)
    return changed


def quarantine_review_acl_restore_failure(claim: dict[str, Any]) -> None:
    """Keep an unrestored review claim visible and non-releasable."""
    if claim.get("lane") != REVIEW_LANE or not claim.get("review_acl_restore_error"):
        return
    claim["status"] = "quarantined"
    claim.setdefault(
        "quarantined_at", dt.datetime.now(dt.timezone.utc).isoformat()
    )
    claim["quarantine_reason"] = (
        "review ACL restoration failed closed: "
        + str(claim["review_acl_restore_error"])
    )


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
    _, focus_nodes = theorem_dag_v2()
    actionable_unfinished = sum(
        item["state"] != "[x]"
        and isinstance(focus_nodes.get(item["theorem_id"]), dict)
        and isinstance(focus_nodes[item["theorem_id"]].get("focus_eligibility"), dict)
        and focus_nodes[item["theorem_id"]]["focus_eligibility"].get(
            "execution_disposition"
        )
        not in {"defer_frontier", "exclude_scope"}
        for item in ordered
    )
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
    # The claim ledger is append-only attempt history. Pick the newest attempt
    # explicitly instead of depending on incidental JSON array order.
    claim_by_item: dict[str, dict[str, Any]] = {}
    for claim in claims:
        item_id = claim.get("item_id")
        claim_id = claim.get("claim_id")
        if not isinstance(item_id, str) or not isinstance(claim_id, str):
            continue
        current = claim_by_item.get(item_id)
        if current is None or claim_id > str(current.get("claim_id", "")):
            claim_by_item[item_id] = claim
    ready = []
    workers = []
    for item in ordered:
        claim = claim_by_item.get(item["id"])
        claim_state = "unclaimed" if claim is None else f"{claim.get('status')}:{claim.get('worker_id', 'unknown')}"
        phase_deps_done = all(next(row for row in ordered if row["id"] == dependency)["state"] == "[x]" for dependency in item["depends_on"])
        focus_allowed = item_focus_phase_allowed(item, focus_nodes)
        focus_node = focus_nodes.get(item["theorem_id"], {})
        focus_projection = (
            focus_node.get("focus_eligibility")
            if isinstance(focus_node, dict)
            else {}
        )
        if not isinstance(focus_projection, dict):
            focus_projection = {}
        focus_disposition = str(focus_projection.get("execution_disposition", "invalid"))
        if item["phase"] in {"proof", "validation", "release"}:
            hard_gate, hard_blockers = hard_edge_gate_status(item["theorem_id"], item["phase"])
        else:
            hard_gate, hard_blockers = "not_applicable_for_phase", []
        deps_done = phase_deps_done and hard_gate != "blocked" and focus_allowed
        if item["state"] == "[_]":
            ready.append((item, claim_state, phase_deps_done, deps_done, hard_gate, hard_blockers, focus_allowed, focus_disposition))
        elif item["state"] == "[ ]" and claim is None:
            workers.append((item, claim_state, phase_deps_done, deps_done, hard_gate, hard_blockers, focus_allowed, focus_disposition))
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
    live_claim_count = sum(
        claim.get("status") == "live"
        and (app_server_worker_is_live(claim) or app_server_child_is_live(claim))
        for claim in claims
    )
    lines = [
        "# Stage1 v2 Execution Todo",
        "",
        "SSOT: `Docs/Stage1_Blueprint_v2.md`; this file is today's derived task snapshot. Derived DAG/order: `Docs/Stage1_Phase_DAG_v2.json`, `Docs/Stage1_Theorem_DAG_v2.json`.",
        f"SSOT blueprint SHA-256: `{blueprint_sha256}`",
        f"Phase state/attempts SHA-256: `{state_sha256}`",
        f"Not done: {counts['[ ]']}",
        f"Worker self-tested: {counts['[_]']}",
        f"Master accepted: {counts['[x]']}",
        f"Unfinished: {counts['[ ]'] + counts['[_]']}",
        f"Actionable unfinished: {actionable_unfinished}",
        f"Theorems master-complete [x] x7: {theorem_counts['completed']}",
        f"Theorems fully self-tested [_] x7: {theorem_counts['fully_self_tested']}",
        f"Theorems partial [_]/[ ]: {theorem_counts['partial']}",
        f"Theorems unstarted [ ] x7: {theorem_counts['unstarted']}",
        "DAG cycle check: passed.",
        f"Claim ledger: `{RUNTIME.relative_to(ROOT) / 'claims.json'}`; process-backed live worker claims: {live_claim_count}.",
        "",
        "## Worker Claim Frontier",
        "",
        "| Item | Target | Phase | Focus gate | Phase deps accepted | Hard-edge gate | Claim | Owned path |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item, claim_state, phase_deps_done, deps_done, hard_gate, hard_blockers, focus_allowed, focus_disposition in workers:
        hard_display = hard_gate if not hard_blockers else f"{hard_gate}: {len(hard_blockers)} blocker(s); see target ledger"
        focus_display = f"{focus_disposition}:{focus_allowed}"
        lines.append(f"| `{item['id']}` | `{item['theorem_id']}` | {item['phase']} | {focus_display} | {phase_deps_done} | {hard_display} | {claim_state} | `{item['owned_paths'][0]}` |")
    lines.extend(["", "## Master Integration Frontier", "", "| Item | Focus gate | Phase deps accepted | Hard-edge gate | Claim |", "| --- | --- | --- | --- | --- |"])
    for item, claim_state, phase_deps_done, deps_done, hard_gate, hard_blockers, focus_allowed, focus_disposition in ready:
        hard_display = hard_gate if not hard_blockers else f"{hard_gate}: {len(hard_blockers)} blocker(s); see target ledger"
        focus_display = f"{focus_disposition}:{focus_allowed}"
        lines.append(f"| `{item['id']}` | {focus_display} | {phase_deps_done} | {hard_display} | {claim_state} |")
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
    reconciled = reconcile_finished_implementation_handoffs(ordered, claims)
    if reconciled:
        save_claims(claims)
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
            # Claims are leases, not admission authority. Re-evaluate the
            # current content-bound focus receipt before copying any worker
            # bytes so a revoked, expired, malformed, or downgraded target
            # cannot cross the integration boundary.
            require_claim_focus_runtime_current(
                item, claim, theorem_nodes, boundary="integration"
            )
            unsupported_fields = UNSUPPORTED_RUNTIME_CLAIM_FIELDS.intersection(claim)
            if unsupported_fields:
                raise ValueError(
                    "worker claim contains unsupported runtime fields: "
                    + ", ".join(sorted(unsupported_fields))
                )
            if item["state"] != "[ ]":
                raise ValueError("finished claim no longer targets a not-done v2 item")
            if claim.get("runtime_protocol") != RUNTIME_PROTOCOL or not goal_runtime_is_verified(claim):
                raise ValueError("worker handoff lacks a verified app-server /goal runtime contract")
            claim_focus = claim.get("focus_eligibility")
            current_focus = focus_decision_for_item(item, theorem_nodes)
            if not isinstance(claim_focus, dict) or claim_focus != current_focus:
                raise ValueError(
                    "worker claim focus eligibility is missing, stale, or changed since allocation"
                )
            handoff_data, _ = read_bounded_runtime_file(
                handoff,
                "worker handoff",
                max_bytes=MAX_WORKER_HANDOFF_BYTES,
            )
            packet = parse_worker_handoff(handoff_data, claim)
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
            protected_validator_paths = phase_validator_candidate_paths(item)
            changed = worker_changed_paths(
                workspace, owner, protected_paths=protected_validator_paths
            )
            if not changed:
                raise ValueError("worker made no owned-path changes")
            if any(not packet_path_covers(path, changed_paths, owner) for path in changed):
                raise ValueError("worker packet does not declare every changed owned path")
            # Resolve the complete candidate set, not merely the currently
            # selected validator. A worker may neither replace an existing
            # candidate nor introduce an alternate that makes selection
            # ambiguous after the copy.
            reject_worker_validator_changes(item, changed)
            worker_role_map = build_staged_worker_role_map(
                item,
                str(claim.get("base_revision", "")),
                workspace,
                changed,
            )
            reject_research_only_proof_delta(
                item, current_focus, worker_role_map, workspace
            )
            if current_focus.get("execution_disposition") == "organize_or_integrate":
                require_integration_only_source_evidence(
                    item,
                    claim["focus_execution"],
                    worker_role_map,
                    changed_paths=changed,
                    evidence_root=workspace,
                )
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
            archive_path, archive_digest, archive_size = persist_worker_handoff(
                claim, handoff_data
            )
            pre_attempts = int(item.get("attempts", 0))
            item["state"] = "[_]"
            item["attempts"] = pre_attempts + 1
            claim["status"] = "finished_integrated"
            claim["integrated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["worker_handoff_archive_schema"] = (
                WORKER_HANDOFF_ARCHIVE_SCHEMA
            )
            claim["worker_handoff_path"] = str(archive_path)
            claim["worker_handoff_sha256"] = archive_digest
            claim["worker_handoff_size"] = archive_size
            claim["staged_role_map"] = worker_role_map
            claim["staged_role_map_sha256"] = worker_role_map["manifest_sha256"]
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
            # Runtime blocker snapshots remain available for audit, but only a
            # claim whose exact focus lease is still current may copy bytes into
            # the authoritative worktree.
            require_claim_focus_runtime_current(
                item, claim, theorem_nodes, boundary="integration_blocker"
            )
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
            focus_receipt = (
                f"{owner.rstrip('/')}/{focus_eligibility.RECEIPT_NAME}"
            )
            if focus_receipt in changed:
                raise ValueError(
                    "blocked handoff changes scheduler/master-owned focus eligibility receipt"
                )
            reject_worker_validator_changes(item, changed)
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
                    "Docs/Stage1_Phase_DAG_v2.json",
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


def worker_changed_paths(
    workspace: Path,
    owner: str,
    *,
    protected_paths: set[str] | None = None,
) -> list[str]:
    """Return the worker's owned file changes and reject deletions.

    A later phase starts from a clone which already contains its target's intake
    dossier.  Copying the whole directory would therefore either reject valid
    work or overwrite independently changed master evidence.  The integration
    surface is instead the worker's actual Git delta, merged one owned file at
    a time with a base-content conflict check.
    """
    status = run(["git", "diff", "--name-status", "HEAD", "--", owner], cwd=workspace).stdout.splitlines()
    status_paths = {
        path
        for line in status
        for path in line.split("\t")[1:]
        if path
    }
    tracked = run(["git", "diff", "--name-only", "HEAD", "--", owner], cwd=workspace).stdout.splitlines()
    untracked = run(["git", "ls-files", "--others", "--exclude-standard", "--", owner], cwd=workspace).stdout.splitlines()
    paths = sorted(set(tracked + untracked))
    all_changed_paths = status_paths | set(paths)
    if any(
        not path.startswith(owner) or ".." in Path(path).parts
        for path in all_changed_paths
    ):
        raise ValueError("worker Git delta escapes the assigned ownership scope")
    focus_receipt = f"{owner.rstrip('/')}/{focus_eligibility.RECEIPT_NAME}"
    if focus_receipt in all_changed_paths:
        raise ValueError(
            "worker handoff changes scheduler/master-owned focus eligibility receipt"
        )
    protected_changes = sorted((protected_paths or set()) & all_changed_paths)
    if protected_changes:
        raise ValueError(
            "worker handoff changes scheduler-owned validator candidate(s): "
            + ", ".join(protected_changes)
        )
    deleted = [line for line in status if line.startswith("D\t")]
    if deleted:
        raise ValueError(f"worker deletion is not an admissible handoff: {deleted}")
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
        "Docs/Stage1_Phase_DAG_v2.json",
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
        "Docs/Stage1_Phase_DAG_v2.json",
        "Docs/Stage1_Theorem_DAG_v2.json",
    }
    selected_state_surfaces = state_surfaces.intersection(selected)
    if selected_state_surfaces.intersection({
        "Docs/Stage1_Blueprint_v2.md",
        "Docs/Stage1_Phase_DAG_v2.json",
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



def reconcile_finished_implementation_handoffs(
    items: list[dict[str, Any]], claims: list[dict[str, Any]], *, limit: int = 50
) -> bool:
    """Park finished sources whose immutable handoff is no longer available."""
    if limit < 0 or limit > 50:
        raise ValueError("handoff reconciliation limit must be in 0..50")
    item_by_id = {item.get("id"): item for item in items}
    _, nodes = theorem_dag_v2()
    sources = sorted(
        (
            source
            for source in claims
            if source.get("lane", IMPLEMENTATION_LANE) == IMPLEMENTATION_LANE
            and source.get("status") == "finished_integrated"
            and isinstance(item_by_id.get(source.get("item_id")), dict)
            and item_by_id[source.get("item_id")].get("state") == "[_]"
        ),
        key=lambda source: claim_order_key(
            item_by_id[source.get("item_id")], nodes
        ),
    )
    changed = False
    for source in sources:
        item = item_by_id.get(source.get("item_id"))
        try:
            read_persisted_worker_handoff(source)
        except (OSError, ValueError) as exc:
            source["status"] = "quarantined"
            source["quarantined_at"] = dt.datetime.now(
                dt.timezone.utc
            ).isoformat()
            source["quarantine_reason"] = (
                "immutable worker handoff is unavailable and v2 does not rerun historical work: "
                + str(exc)
            )
            changed = True
    return changed


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
    ordered_by_id = {item.get("id"): item for item in ordered}
    source_claims_by_item: dict[Any, list[dict[str, Any]]] = {}
    for claim in claims:
        if (
            claim.get("lane", IMPLEMENTATION_LANE) == IMPLEMENTATION_LANE
            and claim.get("status") == "finished_integrated"
            and claim.get("runtime_protocol") == RUNTIME_PROTOCOL
            and not UNSUPPORTED_RUNTIME_CLAIM_FIELDS.intersection(claim)
        ):
            item = ordered_by_id.get(claim.get("item_id"))
            if (
                isinstance(item, dict)
                and item.get("state") == "[_]"
                and review_source_claim(item, [claim]) is not None
            ):
                source_claims_by_item.setdefault(claim.get("item_id"), []).append(claim)
    _, nodes = theorem_dag_v2()
    candidates = [
        item for item in ordered
        if item.get("state") == "[_]"
        and len(source_claims_by_item.get(item.get("id"), [])) == 1
        and item.get("id") not in reviewed_or_claimed
        and all(states.get(dependency) == "[x]" for dependency in item.get("depends_on", []))
        and (
            item.get("phase") not in {"proof", "validation", "release"}
            or hard_edge_gate_status(
                str(item.get("theorem_id")), str(item.get("phase"))
            )[0] in {"not_applicable", "satisfied"}
        )
        and item_focus_phase_allowed(item, nodes)
    ]
    return sorted(candidates, key=lambda item: claim_order_key(item, nodes))


def implementation_candidates(
    ordered: list[dict[str, Any]], claims: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Return only fresh v2 ``[ ]`` work without reviving historical ``[_]``."""
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
    _, nodes = theorem_dag_v2()
    candidates = [
        item
        for item in ordered
        if item["state"] == "[ ]"
        and item["id"] not in claimed_ids
        and (not STARTED_TARGETS_ONLY or item["theorem_id"] in started_targets)
        and all(
            states_by_id.get(dependency) in {"[_]", "[x]"}
            for dependency in item["depends_on"]
        )
        and item_focus_phase_allowed(item, nodes)
    ]
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
    disposition_priority = {
        "organize_or_integrate": 0,
        "frontier_exception": 1,
        "research_required": 2,
    }
    return sorted(
        records,
        key=lambda record: (
            disposition_priority.get(
                nodes.get(record["item"]["theorem_id"], {})
                .get("focus_eligibility", {})
                .get("execution_disposition"),
                sys.maxsize,
            ),
            claim_order_key(record["item"], nodes),
        ),
    )


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
        and not UNSUPPORTED_RUNTIME_CLAIM_FIELDS.intersection(claim)
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
        "worker_handoff_archive_schema",
        "worker_handoff_path",
        "worker_handoff_sha256",
        "worker_handoff_size",
        "focus_eligibility",
        "focus_execution",
    }
    string_required = required - {
        "worker_handoff_size", "focus_eligibility",
        "focus_execution",
    }
    if (
        any(not isinstance(claim.get(field), str) or not claim.get(field) for field in string_required)
        or not isinstance(claim.get("focus_eligibility"), dict)
        or not isinstance(claim.get("focus_execution"), dict)
        or bool(UNSUPPORTED_RUNTIME_CLAIM_FIELDS.intersection(claim))
        or not isinstance(claim.get("worker_handoff_size"), int)
        or isinstance(claim.get("worker_handoff_size"), bool)
        or int(claim["worker_handoff_size"]) <= 0
        or claim.get("worker_handoff_archive_schema")
        != WORKER_HANDOFF_ARCHIVE_SCHEMA
        or re.fullmatch(
            r"[0-9a-f]{64}", str(claim.get("worker_handoff_sha256", ""))
        )
        is None
    ):
        return None
    try:
        read_persisted_worker_handoff(claim)
        require_claim_focus_runtime_current(item, claim, boundary="review_selection")
    except (OSError, ValueError):
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
        if field == "selftest_manifest":
            data, digest, path = read_persisted_worker_handoff(claim)
        else:
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


def validate_review_provenance_handoff(
    item: dict[str, Any], provenance: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Verify the embedded source claim and durable handoff metadata closure."""
    provenance_unhashed = dict(provenance)
    embedded_snapshot_sha256 = provenance_unhashed.pop("snapshot_sha256", None)
    implementation_claim = provenance.get("claim")
    files = provenance.get("files")
    handoff_record = (
        files.get("selftest_manifest") if isinstance(files, dict) else None
    )
    if (
        provenance.get("schema_version") != WORKER_PROVENANCE_SCHEMA
        or embedded_snapshot_sha256 != canonical_json_sha256(provenance_unhashed)
        or not isinstance(implementation_claim, dict)
        or not isinstance(handoff_record, dict)
        or review_source_claim(item, [implementation_claim]) is None
        or handoff_record.get("path")
        != implementation_claim.get("worker_handoff_path")
        or handoff_record.get("sha256")
        != implementation_claim.get("worker_handoff_sha256")
        or handoff_record.get("size")
        != implementation_claim.get("worker_handoff_size")
    ):
        raise ValueError("review provenance lacks a valid durable worker handoff binding")
    return implementation_claim, handoff_record


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
    focus_contract: dict[str, Any],
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
        manifest = acceptance_evidence.build_review_manifest(
            phase_acceptance_contract_record(),
            role_map,
            validator,
            blueprint_sha256=sha256_file(BLUEPRINT),
            blueprint_git_blob=run(
                ["git", "rev-parse", f"HEAD:{BLUEPRINT.relative_to(ROOT).as_posix()}"]
            ).stdout.strip(),
            theorem_dag_sha256=sha256_file(THEOREM_DAG_V2),
            worker_claim_sha256=str(provenance.get("claim_sha256")),
            worker_status_sha256=str(provenance.get("status_sha256")),
            worker_prompt_sha256=str(files["prompt"]["sha256"]),
            worker_goal_sha256=str(files["goal_objective_path"]["sha256"]),
            worker_handoff_sha256=str(files["selftest_manifest"]["sha256"]),
        )
        manifest["focus_execution"] = focus_contract
        manifest["focus_contract_sha256"] = canonical_json_sha256(focus_contract)
        manifest["manifest_sha256"] = canonical_json_sha256(
            {key: value for key, value in manifest.items() if key != "manifest_sha256"}
        )
        return manifest
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
    reviewer_uid = claim.get("runtime_principal_uid")
    client_pid = status.get("client_pid")
    client_start = status.get("client_start_ticks")
    process_is_live = (
        isinstance(client_pid, int)
        and isinstance(client_start, int)
        and process_start_ticks(client_pid) == client_start
    )
    if process_is_live and process_effective_uid(client_pid) != reviewer_uid:
        raise ValueError("live review output process changed its authenticated UID")
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
        or output.get("focus_review") != binding.get("focus_execution")
        or not isinstance(reviewer_uid, int)
        or reviewer_uid < 1
        or reviewer_uid == os.geteuid()
        or status.get("worker_principal") != claim.get("runtime_principal_id")
        or not isinstance(client_pid, int)
        or not isinstance(client_start, int)
        or claim.get("pid") != client_pid
        or claim.get("pid_start_ticks") != client_start
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
    implementation_claim, handoff_record = validate_review_provenance_handoff(
        item, provenance
    )
    current_focus = require_item_focus_phase_allowed(item)
    current_focus_contract = focus_execution_contract(
        item, decision=current_focus
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
        or implementation_claim.get("focus_eligibility") != current_focus
        or implementation_claim.get("focus_execution") != current_focus_contract
        or review_input.get("focus_eligibility") != current_focus
        or review_input.get("focus_execution") != current_focus_contract
        or claim.get("focus_eligibility") != current_focus
        or claim.get("focus_execution") != current_focus_contract
        or manifest.get("focus_execution") != current_focus_contract
        or manifest.get("focus_contract_sha256")
        != canonical_json_sha256(current_focus_contract)
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
        or binding.get("focus_execution") != current_focus_contract
        or binding.get("focus_contract_sha256")
        != canonical_json_sha256(current_focus_contract)
    ):
        raise ValueError("review binding does not close over the exact prompt and objective")
    prompt_path = RUNTIME / "prompts" / f"{claim.get('claim_id')}.txt"
    prompt_bytes, prompt_digest = read_bound_runtime_file(prompt_path, "review prompt")
    if prompt_bytes != prompt.encode() or prompt_digest != binding["prompt_sha256"]:
        raise ValueError("persisted review prompt differs from the binding closure")
    if (
        binding.get("base_revision") != manifest.get("base_revision")
        or binding.get("blueprint_sha256") != manifest.get("blueprint_sha256")
        or binding.get("blueprint_git_blob")
        != manifest.get("blueprint", {}).get("git_blob")
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
    require_phase_receipt_focus_semantics(item, current_focus_contract, role_map)
    require_integration_only_source_evidence(item, current_focus_contract, role_map)
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
    handoff_encoded = handoff_record.get("content_base64")
    try:
        handoff_bytes = base64.b64decode(handoff_encoded, validate=True)
        handoff = json.loads(handoff_bytes)
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("review provenance handoff snapshot is malformed") from exc
    if (
        len(handoff_bytes) != handoff_record.get("size")
        or hashlib.sha256(handoff_bytes).hexdigest()
        != handoff_record.get("sha256")
    ):
        raise ValueError("review provenance handoff bytes disagree with their binding")
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
            # Review output cannot authorize scope. Recheck current scheduler-
            # owned admission immediately before replay and the SSOT CAS.
            acceptance_focus = require_item_focus_phase_allowed(item, theorem_nodes)
            _require_frontier_runtime(
                item, acceptance_focus, claim=None, boundary="master_acceptance_preflight"
            )
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
            compatible_head = require_review_compatible_with_current_head(
                item, manifest, role_map, validator
            )
            review_contract = review_authority_contract_record(manifest)
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
                ROOT,
                contract_record=review_contract,
                review_manifest=manifest,
                role_map=role_map,
                validator_recipe=validator,
                worker_verdict=str(output["worker_verdict"]),
                review_verdict=str(output["review_verdict"]),
                audit_complete=bool(output["audit_complete"]),
                theorem_complete=bool(output["theorem_complete"]),
            )
            replay_focus_contract = focus_execution_contract(
                item, decision=require_item_focus_phase_allowed(item, theorem_nodes)
            )
            integration_semantics = (
                acceptance_evidence.require_replayed_integration_source_semantics(
                    replay, replay_focus_contract, role_map
                )
            )
            if integration_semantics:
                decision = dict(decision)
                decision["integration_source_semantics"] = integration_semantics
                decision["decision_sha256"] = canonical_json_sha256(
                    {key: value for key, value in decision.items() if key != "decision_sha256"}
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
            if item.get("phase") == "release" and (
                output.get("worker_verdict") != "accepted"
                or output.get("audit_complete") is not True
                or output.get("theorem_complete") is not True
                or decision.get("audit_complete") is not True
                or decision.get("theorem_complete") is not True
            ):
                raise ValueError(
                    "release CAS requires accepted with AUDIT-Z and THEOREM-Z"
                )
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
            final_focus = require_item_focus_phase_allowed(item)
            _require_frontier_runtime(
                item, final_focus, claim=None, boundary="master_acceptance_cas"
            )
            if (
                authoritative_head_revision() != compatible_head
                or current is None
                or current.get("state") != "[_]"
                or current.get("attempts") != item.get("attempts")
                or any(
                    authoritative.get(dependency, {}).get("state") != "[x]"
                    for dependency in item.get("depends_on", [])
                )
                or sha256_file(BLUEPRINT) != blueprint_sha256_at_start
            ):
                raise ValueError("SSOT CAS source changed during master acceptance")
            item["state"] = "[x]"
            claim["status"] = "master_accepted"
            claim["master_accepted_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["master_receipt_path"] = receipt_relative
            claim["master_receipt_sha256"] = receipt_sha256
            record_frontier_milestone_completion(
                item,
                claim,
                evidence_path=receipt_relative,
                evidence_sha256=receipt_sha256,
            )
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
    authority_revision = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    _, nodes = theorem_dag_v2()
    reservations: list[dict[str, Any]] = []
    try:
        review_principal, reviewer_uid = scheduler_review_principal()
    except ValueError as exc:
        fail(f"independent review principal is unavailable: {exc}")

    def record_review_preflight_failure(
        item: dict[str, Any],
        *,
        slot: int,
        claim_id: str,
        reason: str,
        implementation_claim: dict[str, Any] | None = None,
    ) -> None:
        """Persist a fail-closed review row without crashing the scheduler tick."""
        claims.append({
            "lane": REVIEW_LANE,
            "item_id": item["id"],
            "theorem_id": item["theorem_id"],
            "depends_on": item["depends_on"],
            "owned_paths": item["owned_paths"],
            "claim_id": claim_id,
            "worker_id": (
                f"stage1app-review-{slot}-"
                f"{nodes[item['theorem_id']]['v2_execution_rank']:04d}-{claim_id[-12:]}"
            ),
            "slot": slot,
            "workspace": str(RUNTIME / "review-workspaces" / f"slot{slot}"),
            "status": "review_failed",
            "claimed_at": timestamp,
            "base_revision": str(
                implementation_claim.get("base_revision", "")
                if isinstance(implementation_claim, dict)
                else authority_revision
            ),
            "authority_revision": authority_revision,
            "runtime_protocol": RUNTIME_PROTOCOL,
            "review_failure_reason": reason,
            "review_retry_after": (
                dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15)
            ).isoformat(),
        })

    for slot, item in zip(slots, candidates):
        if execution_is_paused():
            break
        claim_id = f"{timestamp}-{os.urandom(6).hex()}"
        try:
            focus_decision = require_item_focus_phase_allowed(item, nodes)
            focus_contract = focus_execution_contract(
                item, nodes, decision=focus_decision
            )
        except ValueError as exc:
            record_review_preflight_failure(
                item,
                slot=slot,
                claim_id=claim_id,
                reason=str(exc),
            )
            continue
        implementation_claim = review_source_claim(item, claims)
        if implementation_claim is None:
            record_review_preflight_failure(
                item,
                slot=slot,
                claim_id=claim_id,
                reason="missing or ambiguous immutable implementation provenance",
            )
            continue
        try:
            worker_base_revision = str(implementation_claim.get("base_revision", ""))
            role_map = build_review_role_map(item, worker_base_revision)
            staged_role_map = implementation_claim.get("staged_role_map")
            if (
                focus_decision.get("execution_disposition") == "research_required"
                and isinstance(staged_role_map, dict)
            ):
                staged_paths = staged_role_map.get("staged_delta_paths")
                if not isinstance(staged_paths, list):
                    raise ValueError(
                        "research-only review lacks its scheduler-bound changed-path inventory"
                    )
                role_map = dict(role_map)
                role_map["staged_delta_paths"] = staged_paths
                role_map["manifest_sha256"] = canonical_json_sha256(
                    {
                        key: value for key, value in role_map.items()
                        if key != "manifest_sha256"
                    }
                )
            validator = select_review_validator(item, worker_base_revision)
            provenance = snapshot_review_provenance(item, implementation_claim)
            provenance_path, provenance_file_sha256 = persist_review_provenance(
                implementation_claim, provenance
            )
            review_manifest = build_scheduler_review_manifest(
                provenance, role_map, validator, focus_contract
            )
            review_manifest_path, review_manifest_file_sha256 = persist_review_manifest(
                claim_id, review_manifest
            )
        except (SystemExit, ValueError) as exc:
            # A malformed historical `[_]` must not stop all other reviews or
            # manufacture acceptance. Preserve a scheduler-owned negative row.
            record_review_preflight_failure(
                item,
                slot=slot,
                claim_id=claim_id,
                reason=str(exc),
                implementation_claim=implementation_claim,
            )
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
            "focus_eligibility": focus_decision,
            "focus_execution": focus_contract,
            "runtime_principal_id": review_principal,
            "runtime_principal_uid": reviewer_uid,
        }
        prompt_text = review_prompt(
            item, review_input, claim_id, workspace
        )
        binding = build_review_binding(
            claim_id, item, worker_base_revision, prompt_text, objective, role_map,
            validator, focus_contract,
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
            "base_revision": worker_base_revision,
            "authority_revision": authority_revision,
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
            "focus_eligibility": focus_decision,
            "focus_execution": focus_contract,
            "runtime_principal_id": review_principal,
            "runtime_principal_uid": reviewer_uid,
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
            workspace = prepare_review_workspace(
                int(claim["slot"]), str(claim["authority_revision"])
            )
            prompt_path = RUNTIME / "prompts" / f"{claim['claim_id']}.txt"
            if execution_is_paused():
                cancel_reviews_for_pause(index)
                break
            item = next(
                row for row in ordered if row.get("id") == claim.get("item_id")
            )
            require_claim_focus_runtime_current(
                item, claim, nodes, boundary="review_launch"
            )
            claim["pid"] = launch_review_app_server_worker(
                worker_argv(
                    workspace,
                    prompt_path,
                    Path(str(claim["output_log"])),
                    Path(str(claim["app_server_status"])),
                    Path(str(claim["goal_objective_path"])),
                    lane=REVIEW_LANE,
                    binding_path=Path(str(claim["review_binding_path"])),
                    worker_principal=str(claim["runtime_principal_id"]),
                ),
                reviewer_uid=int(claim["runtime_principal_uid"]),
                workspace=workspace,
                read_paths=[
                    prompt_path,
                    Path(str(claim["goal_objective_path"])),
                    Path(str(claim["review_binding_path"])),
                ],
                write_paths=[
                    Path(str(claim["output_log"])),
                    Path(str(claim["app_server_status"])),
                ],
                delay_seconds=launch_stagger_delay(len(started)),
                claim=claim,
                claims=claims,
            )
            claim["pid_start_ticks"] = process_start_ticks(claim["pid"])
            if claim["pid_start_ticks"] is None:
                raise RuntimeError("launched review client lacks a stable /proc identity")
            claim["client_started_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            started.append(claim)
        except BaseException as exc:
            if app_server_worker_is_live(claim) or app_server_child_is_live(claim):
                terminate_app_server_worker(claim)
            restore_stopped_review_acl(claim)
            claim["status"] = "launch_failed"
            claim["launch_error"] = str(exc)
            quarantine_review_acl_restore_failure(claim)
        save_claims(claims)
    return confirm_goal_handshakes(claims, started) if started else 0


def refill_workers(max_workers: int) -> int:
    """Reconcile and refill lanes without running heavyweight integration."""
    data, ordered = load_dag()
    claims = refresh_claims(ordered)
    reconciled = reconcile_finished_implementation_handoffs(ordered, claims)
    if reconciled:
        save_claims(claims)
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
    reservations: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for allocation in implementation_allocations:
        slot = int(allocation["slot"])
        item = allocation["item"]
        focus_decision = require_item_focus_phase_allowed(item, theorem_nodes)
        focus_contract = focus_execution_contract(
            item, theorem_nodes, decision=focus_decision
        )
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
            "focus_eligibility": focus_decision,
            "focus_execution": focus_contract,
            "runtime_principal_id": scheduler_worker_principal_id(),
        }
        frontier_policy = _frontier_policy(focus_decision)
        if frontier_policy is not None:
            runtime_principal = scheduler_worker_principal_id()
            if frontier_policy["assigned_worker_id"] != runtime_principal:
                fail(
                    "frontier receipt assignee does not match the authenticated "
                    f"runtime principal: {frontier_policy['assigned_worker_id']} != "
                    f"{runtime_principal}"
                )
            claim["frontier_assigned_worker_id"] = frontier_policy[
                "assigned_worker_id"
            ]
            claim["frontier_policy_sha256"] = frontier_policy["policy_sha256"]
            claim["runtime_principal_id"] = runtime_principal
            claim["frontier_scratch"] = str(
                RUNTIME / FRONTIER_SCRATCH_DIRECTORY / claim_id
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
            if claim.get("frontier_policy_sha256") is not None:
                scratch = prepare_frontier_scratch(claim)
                claim["frontier_attempt_started_at"] = dt.datetime.now(
                    dt.timezone.utc
                ).isoformat()
                claim["frontier_disk_baseline_bytes"] = sum(
                    path.stat().st_size
                    for path in workspace.rglob("*")
                    if path.is_file() and not path.is_symlink()
                )
                _require_frontier_runtime(
                    item, claim["focus_eligibility"], claim=claim, create=True,
                    boundary="implementation_launch",
                )
                save_claims(claims)
            if execution_is_paused():
                cancel_unstarted_for_pause()
                break
            require_claim_focus_runtime_current(
                item, claim, theorem_nodes, boundary="implementation_launch_postcheck"
            )
            claim["pid"] = launch_app_server_worker(
                worker_argv(
                    workspace, prompt, output, status_path, objective_path,
                    worker_principal=str(claim["runtime_principal_id"]),
                    frontier_scratch=(
                        _frontier_claim_scratch_path(claim)
                        if claim.get("frontier_policy_sha256") is not None
                        else None
                    ),
                ),
                delay_seconds=launch_stagger_delay(len(started)),
                scratch=(
                    _frontier_claim_scratch_path(claim)
                    if claim.get("frontier_policy_sha256") is not None
                    else None
                ),
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
            if (
                isinstance(claim.get("pid"), int)
                and (app_server_worker_is_live(claim) or app_server_child_is_live(claim))
            ):
                terminate_app_server_worker(claim)
            try:
                settle_frontier_claim(item, claim, reason="implementation launch failed")
            except ValueError as settlement_exc:
                claim["frontier_settlement_error"] = str(settlement_exc)
            save_claims(claims)
            continue
        save_claims(claims)
    launched = confirm_goal_handshakes(claims, started) if started else 0
    todo = write_todo(data, ordered, claims)
    failed = sum(claim.get("status") == "launch_failed" for claim, _ in reservations)
    print(
        f"tick: verified {launched} implementation and {launched_reviews} review app-server /goal lane(s), "
        f"failed={failed}, todo={todo.relative_to(ROOT)}"
    )
    return launched + launched_reviews


def audited_active_worker_count() -> int:
    """Refresh the claim ledger, then count only process-backed live leases."""
    _data, ordered = load_dag()
    claims = refresh_claims(ordered)
    refuse_unsafe_live_identities(claims)
    return len(active_lane_leases(claims))


def stable_refill(
    max_workers: int,
    *,
    phase: str,
    max_rounds: int,
    deadline_seconds: float,
) -> int:
    """Refill from fresh PID audits, bounded by both attempts and wall time."""
    if max_rounds < 1 or max_rounds > PRE_INTEGRATION_REFILL_ROUNDS:
        fail("stable refill rounds must be in 1..3")
    if deadline_seconds <= 0:
        fail("stable refill deadline must be positive")
    deadline = time.monotonic() + deadline_seconds
    rounds = 0
    verified = 0
    active = 0
    stop_reason = "round_limit"
    while rounds < max_rounds:
        if execution_is_paused():
            active = len(active_lane_leases(load_claims()))
            stop_reason = "paused"
            break
        # refresh_claims performs the canonical PID/start-tick and /goal
        # reconciliation.  Capacity is never inferred from the prior round's
        # launch count or from a stale claim-status snapshot.
        active = audited_active_worker_count()
        if active >= max_workers:
            stop_reason = "cap_reached" if active == max_workers else "downscale_draining"
            break
        if time.monotonic() >= deadline:
            stop_reason = "deadline"
            break
        verified += refill_workers(max_workers)
        rounds += 1
        # Report and decide from a second real process audit.  A client that
        # verified its handshake and then exited does not occupy capacity.
        active = audited_active_worker_count()
        if active >= max_workers:
            stop_reason = "cap_reached" if active == max_workers else "downscale_draining"
            break
        if execution_is_paused():
            stop_reason = "paused"
            break
        if time.monotonic() >= deadline:
            stop_reason = "deadline"
            break
        if rounds < max_rounds:
            time.sleep(
                min(REFILL_RETRY_SETTLE_SECONDS, max(0.0, deadline - time.monotonic()))
            )
    # The value in this line is always a PID-backed audit, never
    # len(starting_claims) + launches.  Existing over-cap workers after a
    # downscale are observed but left to finish naturally.
    print(
        f"refill[{phase}]: rounds={rounds}/{max_rounds}, verified={verified}, "
        f"active={active}/{max_workers}, stop={stop_reason}"
    )
    return active


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
    stable_refill(
        max_workers,
        phase="pre-integration",
        max_rounds=PRE_INTEGRATION_REFILL_ROUNDS,
        deadline_seconds=PRE_INTEGRATION_REFILL_DEADLINE_SECONDS,
    )
    if execution_is_paused():
        print("tick: Stage1 execution paused after refill; integration skipped")
        return
    integrated = integrate(integration_limit)
    if integrated:
        checkpoint_integration()
    if execution_is_paused():
        print("tick: Stage1 execution paused after integration; tail refill skipped")
        return
    stable_refill(
        max_workers,
        phase="tail",
        max_rounds=1,
        deadline_seconds=TAIL_REFILL_DEADLINE_SECONDS,
    )


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
        # A revoked lease must be refused before the old, useful process is
        # disturbed. This also validates the frontier ledger and budget.
        try:
            require_claim_focus_runtime_current(
                item, claim, theorem_nodes, boundary="restart_preflight"
            )
        except (OSError, ValueError, focus_eligibility.EligibilityError) as exc:
            fail(f"cannot restart claim with revoked focus authority: {claim.get('item_id')}: {exc}")
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
        settle_frontier_claim(item, claim, reason="scheduler runtime restart")
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
        focus_decision = require_item_focus_phase_allowed(item, theorem_nodes)
        focus_contract = focus_execution_contract(
            item, theorem_nodes, decision=focus_decision
        )
        claim["focus_eligibility"] = focus_decision
        claim["focus_execution"] = focus_contract
        claim["runtime_principal_id"] = scheduler_worker_principal_id()
        frontier_policy = _frontier_policy(focus_decision)
        if frontier_policy is not None:
            runtime_principal = scheduler_worker_principal_id()
            if frontier_policy["assigned_worker_id"] != runtime_principal:
                fail(
                    "frontier receipt assignee does not match the authenticated "
                    f"runtime principal: {frontier_policy['assigned_worker_id']} != "
                    f"{runtime_principal}"
                )
            claim["frontier_assigned_worker_id"] = frontier_policy[
                "assigned_worker_id"
            ]
            claim["frontier_policy_sha256"] = frontier_policy["policy_sha256"]
            claim["runtime_principal_id"] = runtime_principal
            claim["frontier_scratch"] = str(
                RUNTIME / FRONTIER_SCRATCH_DIRECTORY / claim_id
            )
            ensure_frontier_scratch(claim)
            claim["frontier_attempt_started_at"] = dt.datetime.now(
                dt.timezone.utc
            ).isoformat()
            claim["frontier_disk_baseline_bytes"] = sum(
                path.stat().st_size
                for path in workspace.rglob("*")
                if path.is_file() and not path.is_symlink()
            )
            _require_frontier_runtime(
                item, focus_decision, claim=claim, create=True,
                boundary="restart_allocation",
            )
        save_claims(claims)
        try:
            require_claim_focus_runtime_current(
                item, claim, theorem_nodes, boundary="restart_launch"
            )
            claim["pid"] = launch_app_server_worker(
                worker_argv(
                    workspace, prompt, output, status_path, objective_path,
                    thread_id=thread_id,
                    worker_principal=str(claim["runtime_principal_id"]),
                    frontier_scratch=(
                        _frontier_claim_scratch_path(claim)
                        if frontier_policy is not None
                        else None
                    ),
                ),
                delay_seconds=launch_stagger_delay(restarted),
                scratch=(
                    _frontier_claim_scratch_path(claim)
                    if frontier_policy is not None
                    else None
                ),
            )
            claim["pid_start_ticks"] = process_start_ticks(claim["pid"])
            if claim["pid_start_ticks"] is None:
                raise RuntimeError(
                    "restarted app-server client lacks a stable /proc identity"
                )
        except BaseException as exc:
            if app_server_worker_is_live(claim) or app_server_child_is_live(claim):
                terminate_app_server_worker(claim)
            claim["status"] = "launch_failed"
            claim["launch_error"] = str(exc)
            try:
                settle_frontier_claim(item, claim, reason="restart launch failed")
            except ValueError as settlement_exc:
                claim["frontier_settlement_error"] = str(settlement_exc)
            save_claims(claims)
            fail(f"restarted app-server client failed: {claim.get('item_id')}: {exc}")
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


CRON_MARKER = "# awesome-theorems-stage1-v2"


def _cleanup_embedded_digest(
    value: dict[str, Any], field: str, label: str
) -> str:
    """Verify one canonical embedded digest used by cleanup revalidation."""
    expected = value.get(field)
    unhashed = dict(value)
    unhashed.pop(field, None)
    if (
        not isinstance(expected, str)
        or re.fullmatch(r"[0-9a-f]{64}", expected) is None
        or expected != canonical_json_sha256(unhashed)
    ):
        raise ValueError(f"{label} {field} is stale or malformed")
    return expected


def _cleanup_normalized_blueprint(data: bytes) -> bytes:
    """Ignore checkbox cursors while preserving every normative/checklist byte."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("cleanup blueprint authority is not UTF-8") from exc
    if text.count(CHECKLIST_BEGIN) != 1 or text.count(CHECKLIST_END) != 1:
        raise ValueError("cleanup blueprint authority lacks one checklist boundary")
    normalized = re.sub(
        r"(?m)^- \[[_x ]\] "
        r"(`S56-M-\d{4}-(?:INTAKE|STATEMENT|ANCHOR_AUDIT|OBLIGATION_TREE|PROOF|VALIDATION|RELEASE)`"
        r".*) \{attempts=\d+\}$",
        r"- [STATE] \1 {attempts=N}",
        text,
    )
    return normalized.encode("utf-8")


def _require_cleanup_contract_source_ranges(
    contract_record: dict[str, Any], blueprint_bytes: bytes
) -> None:
    """Recheck every contract source range against the current v2 SSOT bytes."""
    contract = contract_record.get("contract")
    references = contract.get("source_references") if isinstance(contract, dict) else None
    if not isinstance(references, list) or not references:
        raise ValueError("current release contract has no source-reference authority")
    try:
        lines = blueprint_bytes.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise ValueError("current v2 blueprint source is not UTF-8") from exc
    by_id: dict[str, dict[str, Any]] = {}
    blueprint_relative = BLUEPRINT.relative_to(ROOT).as_posix()
    for reference in references:
        if not isinstance(reference, dict):
            raise ValueError("current release contract source reference is malformed")
        reference_id = reference.get("reference_id")
        start = reference.get("line_start")
        end = reference.get("line_end")
        phrases = reference.get("required_phrases")
        if (
            not isinstance(reference_id, str)
            or not reference_id
            or reference_id in by_id
            or reference.get("path") != blueprint_relative
            or not isinstance(start, int)
            or isinstance(start, bool)
            or not isinstance(end, int)
            or isinstance(end, bool)
            or start < 1
            or end < start
            or end > len(lines)
            or not isinstance(phrases, list)
            or not phrases
            or any(not isinstance(phrase, str) or not phrase for phrase in phrases)
        ):
            raise ValueError("current release contract source range is stale or malformed")
        excerpt = "\n".join(lines[start - 1:end])
        if any(phrase not in excerpt for phrase in phrases):
            raise ValueError(
                f"current release contract source range is stale: {reference_id}"
            )
        by_id[reference_id] = reference
    referenced: set[str] = set()
    for row in [
        *contract.get("common_master_gates", []),
        *contract.get("phases", []),
    ]:
        if not isinstance(row, dict):
            raise ValueError("current release contract source-reference use is malformed")
        row_references = row.get("source_reference_ids")
        if not isinstance(row_references, list) or any(
            not isinstance(value, str) or value not in by_id
            for value in row_references
        ):
            raise ValueError("current release contract source-reference use is malformed")
        referenced.update(row_references)
    if referenced != set(by_id):
        raise ValueError("current release contract source-reference coverage is stale")


def _cleanup_blueprint_and_dag_authority(
    item: dict[str, Any], historical_manifest: dict[str, Any], current_head: str,
    current_contract: dict[str, Any],
) -> tuple[str, str, str]:
    """Allow cursor-only SSOT drift while rejecting material blueprint/DAG drift."""
    blueprint_relative = BLUEPRINT.relative_to(ROOT).as_posix()
    historical_revision = historical_manifest.get("authority_revision")
    historical_blueprint = historical_manifest.get("blueprint")
    if (
        not isinstance(historical_revision, str)
        or re.fullmatch(r"[0-9a-f]{40}", historical_revision) is None
        or not isinstance(historical_blueprint, dict)
        or historical_blueprint.get("path") != blueprint_relative
    ):
        raise ValueError("release receipt lacks an immutable blueprint authority")
    historical_blueprint_bytes = git_object_bytes(
        f"{historical_revision}:{blueprint_relative}"
    )
    current_blueprint_bytes = git_object_bytes(f"{current_head}:{blueprint_relative}")
    if (
        hashlib.sha256(historical_blueprint_bytes).hexdigest()
        != historical_blueprint.get("sha256")
        or historical_manifest.get("blueprint_sha256")
        != historical_blueprint.get("sha256")
        or hashlib.sha1(
            f"blob {len(historical_blueprint_bytes)}\0".encode()
            + historical_blueprint_bytes
        ).hexdigest()
        != historical_blueprint.get("git_blob")
        or BLUEPRINT.read_bytes() != current_blueprint_bytes
    ):
        raise ValueError("release blueprint authority binding is stale")
    if _cleanup_normalized_blueprint(
        historical_blueprint_bytes
    ) != _cleanup_normalized_blueprint(current_blueprint_bytes):
        raise ValueError(
            "release blueprint changed beyond expected post-acceptance checkbox cursors"
        )
    _require_cleanup_contract_source_ranges(current_contract, current_blueprint_bytes)

    dag_relative = THEOREM_DAG_V2.relative_to(ROOT).as_posix()
    historical_dag_bytes = git_object_bytes(f"{historical_revision}:{dag_relative}")
    current_dag_bytes = git_object_bytes(f"{current_head}:{dag_relative}")
    if (
        hashlib.sha256(historical_dag_bytes).hexdigest()
        != historical_manifest.get("theorem_dag_sha256")
        or THEOREM_DAG_V2.read_bytes() != current_dag_bytes
    ):
        raise ValueError("release theorem DAG authority binding is stale")
    try:
        historical_dag = json.loads(historical_dag_bytes)
        current_dag = json.loads(current_dag_bytes)
    except json.JSONDecodeError as exc:
        raise ValueError("release theorem DAG authority is malformed") from exc
    if not isinstance(historical_dag, dict) or not isinstance(current_dag, dict):
        raise ValueError("release theorem DAG authority is malformed")
    global_fields = {
        "schema_version", "requirements_source", "target_manifest",
        "target_id_set_sha256", "execution_contract", "focus_policy", "edge_policy",
    }
    if (
        {key: current_dag.get(key) for key in global_fields}
        != {key: historical_dag.get(key) for key in global_fields}
    ):
        raise ValueError("release theorem DAG global authority changed")
    theorem_id = item.get("theorem_id")
    historical_nodes = {
        row.get("theorem_id"): row
        for row in historical_dag.get("theorems", [])
        if isinstance(row, dict)
    }
    current_nodes = {
        row.get("theorem_id"): row
        for row in current_dag.get("theorems", [])
        if isinstance(row, dict)
    }
    node_fields = {
        "theorem_id", "v2_execution_rank", "topological_layer",
        "direct_hard_parents", "transitive_hard_ancestors",
        "direct_reuse_hint_ids", "shared_lemma_group_ids",
        "dependency_context_sha256", "focus_eligibility",
    }
    historical_node = historical_nodes.get(theorem_id)
    current_node = current_nodes.get(theorem_id)
    if (
        not isinstance(historical_node, dict)
        or not isinstance(current_node, dict)
        or {key: current_node.get(key) for key in node_fields}
        != {key: historical_node.get(key) for key in node_fields}
    ):
        raise ValueError("release target DAG authority changed after acceptance")
    related_specs = (
        ("hard_edges", "edge_id", ("parent_theorem_id", "child_theorem_id")),
        ("reuse_hints", "hint_id", ("provider_theorem_id", "consumer_theorem_id")),
        ("shared_lemma_groups", "group_id", ("member_theorem_ids",)),
    )
    for table, identity, relation_fields in related_specs:
        def related(row: Any) -> bool:
            if not isinstance(row, dict):
                return False
            return any(
                theorem_id in row.get(field, [])
                if isinstance(row.get(field), list)
                else row.get(field) == theorem_id
                for field in relation_fields
            )

        old_rows = historical_dag.get(table, [])
        new_rows = current_dag.get(table, [])
        if not isinstance(old_rows, list) or not isinstance(new_rows, list):
            raise ValueError(f"release target DAG {table} authority is malformed")
        old_related = {row.get(identity): row for row in old_rows if related(row)}
        new_related = {row.get(identity): row for row in new_rows if related(row)}
        if None in old_related or None in new_related or old_related != new_related:
            raise ValueError(f"release target DAG {table} authority changed")
    current_blueprint_blob = hashlib.sha1(
        f"blob {len(current_blueprint_bytes)}\0".encode() + current_blueprint_bytes
    ).hexdigest()
    return (
        hashlib.sha256(current_blueprint_bytes).hexdigest(),
        current_blueprint_blob,
        hashlib.sha256(current_dag_bytes).hexdigest(),
    )


def _cleanup_material_fields_equal(
    historical: dict[str, Any], current: dict[str, Any], fields: set[str]
) -> bool:
    return (
        {field: historical.get(field) for field in fields}
        == {field: current.get(field) for field in fields}
    )


CLEANUP_REPLAY_VOLATILE_FIELDS = {
    "authority_revision", "authority_tree", "recipe_sha256",
    "review_manifest_sha256", "role_map_sha256", "validator_input_sha256",
    "bwrap_argv", "started_at_unix_ns", "duration_ms", "result_sha256",
}
CLEANUP_DECISION_VOLATILE_FIELDS = {
    "replay_result_sha256", "review_manifest_sha256", "role_map_sha256",
    "decision_sha256",
}


def _cleanup_replay_invariants(replay: dict[str, Any]) -> dict[str, Any]:
    if set(replay) != set(acceptance_evidence.ReplayResult.__dataclass_fields__) | {
        "result_sha256"
    }:
        raise ValueError("cleanup release replay schema changed or is incomplete")
    return {
        key: value for key, value in replay.items()
        if key not in CLEANUP_REPLAY_VOLATILE_FIELDS
    }


def _cleanup_decision_invariants(decision: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "schema_version", "phase", "item_id", "theorem_id", "worker_verdict",
        "review_verdict", "audit_complete", "theorem_complete",
        "replay_result_sha256", "review_manifest_sha256", "role_map_sha256",
        "contract_sha256", "semantic_result_sha256", "phase_evidence_accepted",
        "decision", "negative_reasons", "decision_sha256",
        "integration_source_semantics",
    }
    if not (
        set(decision) == expected
        or set(decision) == expected - {"integration_source_semantics"}
    ):
        raise ValueError("cleanup release semantic decision schema changed or is incomplete")
    return {
        key: value for key, value in decision.items()
        if key not in CLEANUP_DECISION_VOLATILE_FIELDS
    }


def revalidate_cleanup_release_acceptance(
    item: dict[str, Any],
    claim: dict[str, Any],
    receipt: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Re-run the current release authority immediately before final cleanup.

    A historical master receipt proves what was accepted then. Cleanup needs a
    current fact: the release permission, contract, target artifacts, validator,
    toolchain closure, replay result, and semantic decision must all still agree.
    """

    focus = require_item_focus_phase_allowed(item)
    _require_frontier_runtime(
        item, focus, claim=None, boundary="cleanup_release_revalidation"
    )
    embedded_focus = receipt.get("focus_eligibility")
    if embedded_focus != focus:
        raise ValueError("release focus authority changed after master acceptance")
    manifest = receipt.get("review_manifest")
    role_map = receipt.get("role_map")
    validator = receipt.get("validator_recipe")
    historical_replay = receipt.get("replay_result")
    historical_decision = receipt.get("semantic_decision")
    if (
        not isinstance(manifest, dict)
        or not isinstance(role_map, dict)
        or not isinstance(validator, dict)
        or not isinstance(historical_replay, dict)
        or not isinstance(historical_decision, dict)
    ):
        raise ValueError("release receipt lacks replayable authority inputs")
    manifest_sha = _cleanup_embedded_digest(
        manifest, "manifest_sha256", "historical release manifest"
    )
    role_map_sha = _cleanup_embedded_digest(
        role_map, "manifest_sha256", "historical release role map"
    )
    validator_sha = _cleanup_embedded_digest(
        validator, "recipe_sha256", "historical release validator"
    )
    replay_sha = _cleanup_embedded_digest(
        historical_replay, "result_sha256", "historical release replay"
    )
    decision_sha = _cleanup_embedded_digest(
        historical_decision, "decision_sha256", "historical release decision"
    )
    if (
        receipt.get("review_manifest_sha256") != manifest_sha
        or receipt.get("role_map_sha256") != role_map_sha
        or receipt.get("validator_recipe_sha256") != validator_sha
        or receipt.get("replay_result_sha256") != replay_sha
        or receipt.get("semantic_decision_sha256") != decision_sha
    ):
        raise ValueError("release receipt authority digests are inconsistent")

    current_head = authoritative_head_revision()
    current_contract = phase_acceptance_contract_record()
    manifest_contract = manifest.get("contract")
    if (
        current_contract.get("revision") != current_head
        or not isinstance(manifest_contract, dict)
        or current_contract.get("path") != manifest_contract.get("path")
        or current_contract.get("sha256") != manifest_contract.get("sha256")
        or current_contract.get("git_blob") != manifest_contract.get("git_blob")
    ):
        raise ValueError("release acceptance contract is no longer current")
    blueprint_sha, blueprint_blob, theorem_dag_sha = (
        _cleanup_blueprint_and_dag_authority(
            item, manifest, current_head, current_contract
        )
    )
    base_revision = manifest.get("base_revision")
    if not isinstance(base_revision, str) or re.fullmatch(r"[0-9a-f]{40}", base_revision) is None:
        raise ValueError("release receipt lacks its immutable worker base")
    try:
        current_role_map = build_review_role_map(item, base_revision)
        current_validator = select_review_validator(
            item, base_revision, require_base_blob_match=False
        )
    except SystemExit as exc:
        raise ValueError(str(exc)) from exc
    role_fields = {
        "schema_version", "item_id", "theorem_id", "phase", "base_revision",
        "contract_sha256", "contract_git_blob", "phase_receipt_path",
        "phase_receipt_sha256", "artifacts",
    }
    validator_fields = {
        "item_id", "theorem_id", "phase", "base_revision", "contract_sha256",
        "validator_authority_generation", "requirements_authority",
        "positive_acceptance_capable", "validator_path", "validator_sha256",
        "validator_git_blob", "validator_git_mode", "argv", "cwd",
        "network_policy", "repo_write_access", "isolated_scratch_write_access",
        "shell_interpolation",
    }
    if not _cleanup_material_fields_equal(role_map, current_role_map, role_fields):
        raise ValueError("release target artifacts changed after master acceptance")
    if not _cleanup_material_fields_equal(
        validator, current_validator, validator_fields
    ):
        raise ValueError("release validator changed after master acceptance")
    current_focus_contract = focus_execution_contract(item, decision=focus)
    if (
        manifest.get("focus_execution") != current_focus_contract
        or manifest.get("focus_contract_sha256")
        != canonical_json_sha256(current_focus_contract)
    ):
        raise ValueError("release exact-source focus contract changed after acceptance")
    provenance_fields = {
        name: manifest.get(name)
        for name in (
            "worker_claim_sha256", "worker_status_sha256", "worker_prompt_sha256",
            "worker_goal_sha256", "worker_handoff_sha256",
        )
    }
    try:
        current_manifest = acceptance_evidence.build_review_manifest(
            current_contract,
            current_role_map,
            current_validator,
            blueprint_sha256=blueprint_sha,
            blueprint_git_blob=blueprint_blob,
            theorem_dag_sha256=theorem_dag_sha,
            **provenance_fields,
        )
    except acceptance_evidence.EvidenceError as exc:
        raise ValueError(str(exc)) from exc
    current_manifest["focus_execution"] = current_focus_contract
    current_manifest["focus_contract_sha256"] = canonical_json_sha256(
        current_focus_contract
    )
    current_manifest["manifest_sha256"] = canonical_json_sha256(
        {
            key: value for key, value in current_manifest.items()
            if key != "manifest_sha256"
        }
    )
    replay = acceptance_evidence.replay_validator(
        ROOT,
        current_validator,
        review_manifest=current_manifest,
        role_map=current_role_map,
        timeout_seconds=REPLAY_TIMEOUT_SECONDS,
    )
    decision = acceptance_evidence.evaluate_replay_semantics(
        replay,
        ROOT,
        contract_record=current_contract,
        review_manifest=current_manifest,
        role_map=current_role_map,
        validator_recipe=current_validator,
        worker_verdict=str(receipt.get("worker_verdict", "")),
        review_verdict=str(receipt.get("review_verdict", "")),
        audit_complete=receipt.get("audit_complete"),
        theorem_complete=receipt.get("theorem_complete"),
    )
    replay_focus_contract = focus_execution_contract(item, decision=focus)
    integration_semantics = (
        acceptance_evidence.require_replayed_integration_source_semantics(
            replay, replay_focus_contract, current_role_map
        )
    )
    if integration_semantics:
        decision = dict(decision)
        decision["integration_source_semantics"] = integration_semantics
        decision["decision_sha256"] = canonical_json_sha256(
            {key: value for key, value in decision.items() if key != "decision_sha256"}
        )
    _cleanup_embedded_digest(replay, "result_sha256", "current release replay")
    _cleanup_embedded_digest(decision, "decision_sha256", "current release decision")
    if (
        decision.get("decision") != "phase_accepted"
        or decision.get("phase_evidence_accepted") is not True
        or decision.get("audit_complete") is not True
        or decision.get("theorem_complete") is not True
    ):
        raise ValueError(
            "current release validator replay or semantic decision differs from acceptance"
        )
    if _cleanup_replay_invariants(replay) != _cleanup_replay_invariants(
        historical_replay
    ):
        raise ValueError(
            "current release replay changed material validator, target, toolchain, or semantics"
        )
    if _cleanup_decision_invariants(decision) != _cleanup_decision_invariants(
        historical_decision
    ):
        raise ValueError("current release semantic acceptance properties changed")
    if authoritative_head_revision() != current_head:
        raise ValueError("authoritative HEAD changed during cleanup release revalidation")
    return replay, decision


def require_cleanup_completion(
    data: dict[str, Any],
    ordered: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> None:
    """Enforce all six Blueprint cleanup conditions before touching crontab."""
    graph, nodes = theorem_dag_v2()
    phase_states = {
        theorem_id: [item["state"] for item in ordered if item["theorem_id"] == theorem_id]
        for theorem_id in nodes
    }
    for theorem_id, node in nodes.items():
        focus = node.get("focus_eligibility") if isinstance(node, dict) else None
        if not isinstance(focus, dict):
            fail(f"cleanup refused: target lacks current disposition: {theorem_id}")
        disposition = focus.get("execution_disposition")
        if disposition in {"organize_or_integrate", "frontier_exception"}:
            if node.get("completion_bucket") != "master_complete" or any(
                state != "[x]" for state in phase_states[theorem_id]
            ):
                fail(f"cleanup refused: eligible target is not master_complete: {theorem_id}")
        elif disposition == "research_required":
            fail(
                f"cleanup refused: research-required target is nonterminal: {theorem_id}"
            )
        elif disposition in {"defer_frontier", "exclude_scope"}:
            if focus.get("valid") is not True or focus.get("present") is not True:
                fail(f"cleanup refused: target lacks accepted terminal disposition: {theorem_id}")
            decision = _focus_receipt(focus).get("admission_review", {}).get("decision")
            expected = {
                "defer_frontier": "defer",
                "exclude_scope": "exclude",
            }[str(disposition)]
            if decision != expected:
                fail(f"cleanup refused: target disposition lacks accepted reason: {theorem_id}")
        else:
            fail(f"cleanup refused: target disposition is nonterminal: {theorem_id}")
    if graph.get("focus_eligibility_summary", {}).get("receipt_valid_count") != len(nodes):
        fail("cleanup refused: not every target has a valid terminal receipt")
    todo = DOCS / f"todos_{dt.date.today():%Y%m%d}.md"
    if todo.is_symlink() or not todo.is_file():
        fail("cleanup refused: daily todo is missing or unsafe")
    expected_todo, expected_projection = render_todo(
        data, ordered, claims, destination=todo
    )
    if expected_todo != todo or todo.read_text(encoding="utf-8") != expected_projection:
        fail("cleanup refused: daily todo is not the current content-bound projection")
    if "Actionable unfinished: 0\n" not in expected_projection:
        fail("cleanup refused: actionable unfinished work remains")
    pending_statuses = {
        "preparing", "live", "launch_failed", "draining", "finished", "blocked",
        "quarantined", "finished_integrated", "review_finished", "review_failed",
        "revalidation_required",
    }
    if any(
        claim.get("runtime_protocol") == RUNTIME_PROTOCOL
        and claim.get("status") in pending_statuses
        for claim in claims
    ):
        fail("cleanup refused: a runtime claim or handoff remains pending")
    for name in ("pending_checkpoint.json", "integration_wal.json"):
        if runtime_path(name).exists() or runtime_path(name).is_symlink():
            fail(f"cleanup refused: {name} remains")
    queue_path = runtime_path("integration_queue.json")
    if queue_path.exists():
        queue = read_json(queue_path)
        if any(queue.get(key) for key in ("queued", "blocked_reports", "rejected", "review_rejected")):
            fail("cleanup refused: integration queue is not empty")
    run(["python3", "Docs/tools/check_stage1_standard.py"])
    run(["python3", "scripts/stage1_target.py", "check"])
    run(["python3", "Docs/tools/check_stage1_theorem_dag_v2.py"])
    release_claims = {
        claim.get("item_id"): claim
        for claim in claims
        if claim.get("status") == "master_accepted"
    }
    for item in ordered:
        node = nodes.get(str(item.get("theorem_id")), {})
        focus = node.get("focus_eligibility") if isinstance(node, dict) else {}
        if (
            item.get("phase") == "release"
            and isinstance(focus, dict)
            and focus.get("execution_disposition")
            in {"organize_or_integrate", "frontier_exception"}
        ):
            claim = release_claims.get(item.get("id"))
            if not isinstance(claim, dict):
                fail(f"cleanup refused: release lacks master acceptance: {item.get('id')}")
            receipt_path = claim.get("master_receipt_path")
            receipt_sha = claim.get("master_receipt_sha256")
            if (
                not isinstance(receipt_path, str)
                or Path(receipt_path).is_absolute()
                or ".." in Path(receipt_path).parts
                or not isinstance(receipt_sha, str)
                or not (ROOT / receipt_path).is_file()
                or hashlib.sha256((ROOT / receipt_path).read_bytes()).hexdigest()
                != receipt_sha
            ):
                fail(f"cleanup refused: release gate receipt is missing or stale: {item.get('id')}")
            try:
                receipt, receipt_bytes = read_exact_json_file(
                    ROOT / receipt_path,
                    "master release acceptance receipt",
                    expected_sha256=receipt_sha,
                )
            except (OSError, ValueError) as exc:
                fail(
                    f"cleanup refused: release gate receipt cannot be replayed: "
                    f"{item.get('id')}: {exc}"
                )
            decision = receipt.get("semantic_decision")
            semantic = receipt.get("replay_result", {}).get("semantic_result")
            try:
                replayed, replayed_decision = revalidate_cleanup_release_acceptance(
                    item, claim, receipt
                )
            except (
                OSError,
                ValueError,
                SystemExit,
                acceptance_evidence.EvidenceError,
                focus_eligibility.EligibilityError,
            ) as exc:
                fail(
                    "cleanup refused: release currentness revalidation failed: "
                    f"{item.get('id')}: {exc}"
                )
            release_decisions = [
                row
                for row in receipt.get("artifact_bindings", [])
                if isinstance(row, dict) and row.get("role") == "release_decision"
            ]
            release_decision: dict[str, Any] | None = None
            if len(release_decisions) == 1:
                relative = release_decisions[0].get("path")
                expected = release_decisions[0].get("sha256")
                if (
                    isinstance(relative, str)
                    and not Path(relative).is_absolute()
                    and ".." not in Path(relative).parts
                    and isinstance(expected, str)
                ):
                    try:
                        release_decision, _ = read_exact_json_file(
                            ROOT / relative,
                            "release terminal decision",
                            expected_sha256=expected,
                        )
                    except (OSError, ValueError):
                        release_decision = None
            terminal = (
                release_decision.get("terminal_decisions")
                if isinstance(release_decision, dict)
                else None
            )
            root_vector = (
                release_decision.get("root_vector")
                if isinstance(release_decision, dict)
                else None
            )
            if (
                receipt.get("schema_version") != MASTER_ACCEPTANCE_RECEIPT_SCHEMA
                or receipt.get("item_id") != item.get("id")
                or receipt.get("theorem_id") != item.get("theorem_id")
                or receipt.get("phase") != "release"
                or receipt.get("phase_evidence_accepted") is not True
                or receipt.get("worker_verdict") != "accepted"
                or receipt.get("review_verdict") != "phase_accepted"
                or receipt.get("audit_complete") is not True
                or receipt.get("theorem_complete") is not True
                or not isinstance(decision, dict)
                or decision.get("decision") != "phase_accepted"
                or decision.get("phase_evidence_accepted") is not True
                or decision.get("audit_complete") is not True
                or decision.get("theorem_complete") is not True
                or receipt.get("semantic_decision_sha256")
                != canonical_json_sha256(
                    {key: value for key, value in decision.items() if key != "decision_sha256"}
                )
                or decision.get("decision_sha256")
                != receipt.get("semantic_decision_sha256")
                or not isinstance(semantic, dict)
                or semantic.get("verdict") != "accepted"
                or semantic.get("audit_complete") is not True
                or semantic.get("theorem_complete") is not True
                or not isinstance(release_decision, dict)
                or release_decision.get("verdict") != "accepted"
                or not isinstance(terminal, dict)
                or terminal.get("audit_complete") is not True
                or terminal.get("theorem_complete") is not True
                or release_decision.get("remaining_root_cut_set") not in (None, [])
                or not isinstance(root_vector, dict)
                or root_vector.get("M")
                not in {"M0-L", "M0-W", "M0-P"}
                or hashlib.sha256(receipt_bytes).hexdigest() != receipt_sha
                or replayed_decision.get("decision") != "phase_accepted"
                or replayed_decision.get("phase_evidence_accepted") is not True
                or replayed_decision.get("audit_complete") is not True
                or replayed_decision.get("theorem_complete") is not True
            ):
                fail(
                    "cleanup refused: eligible release does not establish exact "
                    f"THEOREM-Z/M0 closure: {item.get('id')}"
                )


def cleanup() -> None:
    data, ordered = load_dag()
    claims = refresh_claims(ordered)
    require_cleanup_completion(data, ordered, claims)
    cron = run(["crontab", "-l"], check=False)
    lines = [line for line in cron.stdout.splitlines() if CRON_MARKER not in line]
    subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", text=True, check=True)
    after = run(["crontab", "-l"], check=False)
    if any(CRON_MARKER in line for line in after.stdout.splitlines()):
        fail("cleanup refused: exact Stage1 cron entry remains installed")
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
        f">> {RUNTIME / 'keepalive.log'} 2>&1 {CRON_MARKER}"
    )
    current = run(["crontab", "-l"], check=False).stdout.splitlines()
    current = [line for line in current if "stage1_execution_cron.py" not in line]
    subprocess.run(["crontab", "-"], input="\n".join(current + [command]) + "\n", text=True, check=True)
    print("install: cron entry installed")


def pause() -> None:
    """Persistently stop scheduling before any future tick can mutate state."""
    validate_runtime_root()
    marker = dt.datetime.now(dt.timezone.utc).isoformat() + "\n"
    PAUSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(PAUSE_FILE, marker)
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
    durable_unlink(PAUSE_FILE)
    print("resume: cleared Stage1 v2 PAUSED state; cron remains uninstalled")


def _write_focus_review_job(
    candidate: Path,
    reviewer_id: str,
    reviewer_uid: int,
    reject: bool,
    *,
    frontier_review_input: Path | None = None,
) -> tuple[Path, Path]:
    candidate_sha256 = sha256_file(candidate)
    nonce = os.urandom(16).hex()
    job_root = RUNTIME / "focus-admission" / "review-jobs" / nonce
    result_root = RUNTIME / "focus-admission" / "review-results" / nonce
    job = {
        "schema_version": FOCUS_REVIEW_JOB_SCHEMA,
        "candidate_path": str(candidate),
        "candidate_file_sha256": candidate_sha256,
        "reviewer": {"id": reviewer_id, "role": "independent_reviewer"},
        "reviewer_uid": reviewer_uid,
        "approve": not reject,
        "nonce": nonce,
    }
    candidate_value = focus_admission._load_runtime_record(
        candidate,
        RUNTIME / "focus-admission" / "candidates",
        "focus candidate",
        root=ROOT,
    )
    frontier = candidate_value.get("receipt_facts", {}).get("frontier_exception")
    if isinstance(frontier, dict):
        if frontier_review_input is None:
            fail(
                "frontier focus review requires a separately authored reviewer input; "
                "boolean approval is forbidden"
            )
        review_input = focus_admission._load_runtime_record(
            frontier_review_input.absolute(),
            RUNTIME / "focus-admission" / "frontier-review-staging",
            "staged frontier independent review input",
            root=ROOT,
        )
        if (
            review_input.get("candidate_sha256") != candidate_value["candidate_sha256"]
            or review_input.get("reviewer")
            != {"id": reviewer_id, "role": "independent_reviewer"}
        ):
            fail("staged frontier review input targets another candidate or reviewer")
        review_path = focus_admission._frontier_review_input_path(
            RUNTIME, candidate_value["candidate_sha256"]
        )
        durable_write_bytes(
            review_path,
            (json.dumps(review_input, ensure_ascii=True, indent=2) + "\n").encode("utf-8"),
        )
    job["job_sha256"] = canonical_json_sha256(job)
    job_path = job_root / "job.json"
    result_path = result_root / "result.json"
    durable_write_bytes(
        job_path,
        (json.dumps(job, ensure_ascii=True, indent=2) + "\n").encode("utf-8"),
    )
    return job_path, result_path


def _run_focus_review_job_as_principal(
    job_path: Path, result_path: Path, reviewer_uid: int
) -> None:
    """Run the focus verifier in a distinct OS process or refuse issuance."""
    if os.geteuid() != 0:
        fail(
            "independent focus review requires a root-owned supervisor; "
            "synchronous scheduler-UID review is forbidden"
        )
    if reviewer_uid < 1 or reviewer_uid == os.geteuid():
        fail("independent focus review requires a distinct non-root OS UID")
    reviewer_key_value = os.environ.get("STAGE1_FOCUS_REVIEWER_SIGNING_KEY")
    if reviewer_key_value is None:
        reviewer_key_value = str(focus_admission.DEFAULT_REVIEWER_SIGNING_KEY)
    reviewer_key = Path(reviewer_key_value).absolute()
    if (
        reviewer_key.is_symlink()
        or not reviewer_key.is_file()
        or reviewer_key.stat().st_mode & 0o777 != 0o600
        or reviewer_key.stat().st_uid != os.geteuid()
    ):
        fail(
            "independent focus reviewer signing key must be a "
            "scheduler-owned regular file with mode 0600"
        )
    review_root = result_path.parent
    review_root.mkdir(parents=True, exist_ok=True)
    access_snapshots = provision_review_access(
        reviewer_uid=reviewer_uid,
        workspace=job_path.parent,
        read_paths=[
            job_path,
            Path(__file__).resolve(),
            Path(focus_admission.__file__).resolve(),
            Path(focus_eligibility.__file__).resolve(),
            reviewer_key,
        ],
        write_paths=[result_path],
    )
    helper = """
import hashlib
import importlib.util
import json
import os
import pathlib
import sys

module_path = pathlib.Path(sys.argv[5])
spec = importlib.util.spec_from_file_location("stage1_focus_admission", module_path)
if spec is None or spec.loader is None:
    raise RuntimeError("focus review module is unavailable")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
job = json.loads(pathlib.Path(sys.argv[1]).read_text())
candidate = pathlib.Path(job["candidate_path"])
if hashlib.sha256(candidate.read_bytes()).hexdigest() != job["candidate_file_sha256"]:
    raise RuntimeError("focus candidate changed before independent review")
review = module.review_focus_admission(
    sys.argv[3], sys.argv[4], candidate, job["reviewer"],
    approve=job["approve"], reviewer_signing_key_path=sys.argv[6]
)
result = {
    "schema_version": "stage1-focus-review-result/1.0",
    "job_sha256": job["job_sha256"],
    "review_path": str(review),
    "review_file_sha256": hashlib.sha256(review.read_bytes()).hexdigest(),
    "reviewer_uid": os.geteuid(),
    "nonce": job["nonce"],
}
result["result_sha256"] = hashlib.sha256(
    json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()
pathlib.Path(sys.argv[2]).write_text(json.dumps(result, indent=2) + "\n")
"""
    command = [
        "/usr/bin/setpriv", f"--reuid={reviewer_uid}", f"--regid={reviewer_uid}",
        "--clear-groups", "--no-new-privs", "--", sys.executable, "-I", "-B", "-c", helper,
        str(job_path), str(result_path), str(ROOT), str(RUNTIME),
        str(Path(focus_admission.__file__).resolve()), str(reviewer_key),
    ]
    process: subprocess.Popen[bytes] | None = None
    try:
        process = subprocess.Popen(
            command,
            cwd=job_path.parent,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
            close_fds=True,
        )
        try:
            require_process_effective_uid(process.pid, reviewer_uid, "focus reviewer")
            stdout, stderr = process.communicate(timeout=FOCUS_REVIEW_TIMEOUT_SECONDS)
        except BaseException:
            try:
                os.killpg(process.pid, 15)
            except ProcessLookupError:
                pass
            raise
        if process.returncode:
            detail = (stderr or stdout).decode("utf-8", "replace").strip()
            fail(f"independent focus reviewer failed: {detail or 'no diagnostic'}")
    finally:
        # The key remains scheduler-owned. The reviewer gets a narrow,
        # claim-scoped read ACL only while producing this signed review.
        restore_review_access(access_snapshots)


def _load_focus_review_result(
    job_path: Path, result_path: Path, reviewer_uid: int
) -> Path:
    try:
        job = json.loads(job_path.read_text(encoding="utf-8"))
        result = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"independent focus reviewer produced no canonical result: {exc}")
    unhashed = dict(result)
    result_sha256 = unhashed.pop("result_sha256", None)
    review_path = Path(str(result.get("review_path", "")))
    if (
        result.get("schema_version") != FOCUS_REVIEW_RESULT_SCHEMA
        or set(result) != {
            "schema_version", "job_sha256", "review_path", "review_file_sha256",
            "reviewer_uid", "nonce", "result_sha256",
        }
        or result_sha256 != canonical_json_sha256(unhashed)
        or result.get("job_sha256") != job.get("job_sha256")
        or result.get("nonce") != job.get("nonce")
        or result.get("reviewer_uid") != reviewer_uid
        or not review_path.is_file()
        or sha256_file(review_path) != result.get("review_file_sha256")
    ):
        fail("independent focus review result is stale, forged, or incomplete")
    return review_path


def issue_focus_admission(
    proposal: Path,
    decision: Path,
    *,
    reject: bool,
    frontier_review_input: Path | None = None,
) -> None:
    """Prepare as scheduler, but review only under a distinct OS principal."""
    try:
        reviewer_id, reviewer_uid = scheduler_review_principal()
        scheduler_decision = focus_admission.load_scheduler_decision(RUNTIME, decision)
        expected_reviewer = {
            "id": reviewer_id,
            "role": "independent_reviewer",
        }
        if scheduler_decision.get("reviewer") != expected_reviewer:
            fail(
                "scheduler decision reviewer does not match the configured "
                "authenticated review principal"
            )
        candidate = focus_admission.prepare_focus_admission(
            ROOT,
            RUNTIME,
            proposal,
            scheduler_decision,
        )
        job_path, result_path = _write_focus_review_job(
            candidate,
            reviewer_id,
            reviewer_uid,
            reject,
            frontier_review_input=frontier_review_input,
        )
        _run_focus_review_job_as_principal(job_path, result_path, reviewer_uid)
        review = _load_focus_review_result(job_path, result_path, reviewer_uid)
        if reject:
            print(f"focus-admission: rejected review={review}")
            return
        issuance = focus_admission.publish_focus_admission(
            ROOT,
            RUNTIME,
            candidate,
            review,
        )
    except (focus_admission.AdmissionError, ValueError) as exc:
        fail(str(exc))
    print(f"focus-admission: published issuance={issuance}")


def main() -> None:
    validate_only_requested = "--validate-only" in sys.argv[1:]
    # A paused tick must be a true no-op, including no runtime directory or
    # lock-file mutation. Check it before constructing the scheduler lock.
    if "--tick" in sys.argv[1:] and execution_is_paused():
        print("tick: Stage1 execution is paused; no sync, integration, or refill performed")
        return
    # A pause request must never be dropped behind an active scheduler lock.
    # Persist the stop intent and remove the refill entry immediately; any
    # in-flight tick observes PAUSED before launching a new worker below.
    if "--pause" in sys.argv[1:]:
        pause()
        return
    paused_mutating_modes = {
        "--bootstrap", "--integrate", "--cleanup", "--restart-live", "--install",
    }
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
    modes.add_argument("--issue-focus", action="store_true", help="review and publish one scheduler-owned focus admission")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help=f"concurrent-worker refill budget (0..{MAX_WORKERS}; default {DEFAULT_WORKERS})")
    parser.add_argument("--limit", type=int, default=DEFAULT_INTEGRATION_LIMIT, help=f"handoff integration budget (0..{MAX_INTEGRATION_LIMIT}; default {DEFAULT_INTEGRATION_LIMIT})")
    parser.add_argument("--schedule", default="*/5 * * * *", help="crontab schedule used by --install")
    parser.add_argument("--focus-proposal", type=Path, help="HEAD-tracked theorem-owned focus proposal")
    parser.add_argument("--focus-decision", type=Path, help="scheduler-staged focus admission decision")
    parser.add_argument(
        "--frontier-review-input",
        type=Path,
        help="separately authored reviewer decision staged under focus-admission/frontier-review-staging",
    )
    parser.add_argument("--focus-reject", action="store_true", help="persist a typed rejected focus review without publishing")
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
    elif args.issue_focus:
        if (
            args.focus_proposal is None
            or args.focus_decision is None
        ):
            fail("--issue-focus requires proposal and scheduler decision")
        issue_focus_admission(
            args.focus_proposal,
            args.focus_decision,
            reject=args.focus_reject,
            frontier_review_input=args.frontier_review_input,
        )
    else:
        install(args.schedule)
    if lock is not None:
        lock.close()


if __name__ == "__main__":
    main()
