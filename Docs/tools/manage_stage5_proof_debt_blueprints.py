#!/usr/bin/env python3
"""Create, migrate and validate the Stage5 proof-debt Blueprint authorities.

This one-time bootstrap validator derives the fixed all-blank v2 Blueprint rows
from sealed Stage5/Stage6 authorities and renders an all-unscheduled same-prefix
Gantt.  Its only state-changing exception is the closed, digest-bound BOOT
blank-to-underscore-to-x acceptance procedure; it never activates cron, creates
execution runtime, or authorizes worker launch.  After BOOT acceptance this
script is no longer an authority, parser, or generator for later transitions or
ordinary checklist transitions.  Its explicit reviewed v1-to-v2 action only
retires legacy phase rows into a digest-bound preservation receipt and installs
the all-blank one-mathematical-object/one-goal authorities; it launches nothing.
"""

from __future__ import annotations

import argparse
import ast
import base64
from collections import Counter
from contextlib import contextmanager
import ctypes
from dataclasses import dataclass
from datetime import datetime, timezone
import errno
from functools import lru_cache
import hashlib
import importlib.util
import json
import os
import fcntl
import importlib.util
from pathlib import Path, PurePosixPath
import re
import secrets
import stat
import subprocess
import tempfile
from typing import Any, Iterable, Iterator

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "Docs"
CANONICAL_ROOT = Path("/home/sansha/Github/awesome_theorems")
SHARED_RUNTIME_ROOT = ".ops/stage5-proof-debt-shared-v2"
ROOT_RELOCATION_POLICY = (
    "new reviewed specification and source-bundle authority; prior receipts remain "
    "bound to the old absolute root and cannot be reinterpreted"
)
CANONICAL_ROOT_AUTHORITY_SHA256 = "d1d94122caf8e062de148d9ef537052bbbb184b680d3e30504486cd156a3bc81"

STAGE5_CURRENT = DOCS / "catalog/v5/Current_Release.json"
STAGE5_MANIFEST = DOCS / "catalog/v5/releases/5.6/Release_Manifest.json"
THEOREM_SOURCE = DOCS / "catalog/v5/releases/5.6/Theorem_List.json"
STRICT_SOURCE = DOCS / "catalog/v5/releases/5.6/Strict_Conjecture_Ledger.json"
OPEN_SOURCE = DOCS / "catalog/v5/releases/5.6/Open_Claim_List.json"
CONJECTURE_POOL_CURRENT = DOCS / "catalog/v5/pools/Current_Pool_Release.json"
CONJECTURE_POOL_MANIFEST = DOCS / "catalog/v5/pools/conjecturebench-357bcb1a/Pool_Manifest.json"
CONJECTURE_POOL_OCCURRENCES = DOCS / "catalog/v5/pools/conjecturebench-357bcb1a/Source_Occurrence_Pool.jsonl"
CONJECTURE_POOL_IDENTITIES = DOCS / "catalog/v5/pools/conjecturebench-357bcb1a/Identity_Registry.jsonl"
STAGE6_CURRENT = DOCS / "catalog/v6/Current_Release.json"
STAGE6_MANIFEST = DOCS / "catalog/v6/releases/6.0/Migration_Manifest.json"
STAGE6_REGISTRY = DOCS / "catalog/v6/releases/6.0/Stage6_ID_Registry.json"
STAGE6_MIGRATION = DOCS / "catalog/v6/releases/6.0/Migration_to_Stage6.json"

THEOREM_SOURCE_SHA256 = "c7b997fb72d0b29f055346ef49750aa5b7340667d70f38a6bc3ade7eeb4ddd6b"
THEOREM_AUTHORITY_SHA256 = "9a9388c4df2b27fa051b451f4a3dc56afa6fe7dd147a5aaa1e7c28c76df77015"
THEOREM_ID_SET_SHA256 = "633616101ebbd3fa5dda8c1311c415e65cbf9013872e275305b6d938d72ed223"
STAGE5_CURRENT_SHA256 = "ef66a1da8baa6a9c27435cff83bcb9a5e382072d1c5e65150fc6a9265560f0bb"
STAGE5_CURRENT_AUTHORITY_SHA256 = "1d3a195fe1eb8a2cec9a8dcc109715cc9edf041733831d590e01e9f75b154f7e"
STAGE5_MANIFEST_AUTHORITY_SHA256 = "8f08b649ed49d3a3433ef531a326d95099367037ccae067677ab626ca35b9d16"
STRICT_SOURCE_SHA256 = "3d6668de8615e426a03c47b270edf3b5676e32080d78af13eca325fae418fc84"
STRICT_AUTHORITY_SHA256 = "3c682f3c6906c10b330f717c6de6e5d4be10690915fe8b6ae1e9c6743b6756f8"
STRICT_ID_SET_SHA256 = "adc64f7d4a1cc309bac6e93be9dbe481d7e21a6d6197fdc7f09889bfabc43521"
OPEN_SOURCE_SHA256 = "5ae017c6f9cf62809c5b881ed636822752c2c1d929593adf84277338550ad007"
RELEASE_MANIFEST_SHA256 = "a7e03126ceb24d3d5052c515fb79246823ef5cd1beae53209739aed8582c46cf"
RELEASE_ROOT_SHA256 = "ce490ed958240ae1cabc26c3f704ad20b4103e30ad8abfd44e9c3b722fa17877"
STAGE6_CURRENT_SHA256 = "689480df2bf5b7d1e3261cc9efd29dac90021af75f7f98fc50dde9cef35bb0c3"
STAGE6_CURRENT_AUTHORITY_SHA256 = "ee246e99182dbc97e80a42ce049445458da1a611c91b3f8dc47309551b34e8f5"
STAGE6_MANIFEST_SHA256 = "1fbf2ded0da52d0c33ba9014f2ac82c24e04b0fe5790b9306fc0ecd31c17a2d4"
STAGE6_MANIFEST_AUTHORITY_SHA256 = "0d31af0d97fdf0d040e549b7e2f88212650af628dd54217b4333a1dbac1bb6dc"
STAGE6_RELEASE_ROOT_SHA256 = "0709742a34087727f1ef4e64d8fb5fa5b1dc3661dfbf67a83c3b7b5f6cabca5b"
STAGE6_REGISTRY_SHA256 = "eb531fec1312927f8f7df6b5f21f5729ee96f2be86ddaa9af6c15165e58979ff"
STAGE6_REGISTRY_AUTHORITY_SHA256 = "da198be5b4b3acd43cad7049123b6942e22eecfe2c9b23e2d39fbe9161b47d0c"
STAGE6_MIGRATION_SHA256 = "80a85719f0c1e3b0ea057b2f5cc7f4381e4113b32a1a7907a7623b78f2d13eb6"
STAGE6_MIGRATION_AUTHORITY_SHA256 = "edcab45e40c86d25c5d4cc3572df2ab99e7bad3867ea8377bbb54f4f24b6bc85"
M0387_META = ROOT / "THM-M-0387/meta.json"
M0387_PROOF_UNITS = ROOT / "THM-M-0387/proof_units.json"
M0387_CURRENT_RECEIPT = ROOT / "THM-M-0387/receipts/current-validation.json"
M0387_CRITICAL_AUDIT = DOCS / "reviews/THM-M-0387_Critical_Audit_2026-08-10.md"
M0387_META_SHA256 = "b7fc660296f248d73d62cc2aaee6a2d36c3797e88d1d94a9d757f6384e9b90e2"
M0387_PROOF_UNITS_SHA256 = "e081c11ee8681350963275b3dd3ba7c819df5b85b28a8c01906e92d253b8a813"
M0387_CURRENT_RECEIPT_SHA256 = "fffb8c7e1c8e71c2c39fac4e4f322b9579af6a8b0e9fdb57885c8bbb9c92174e"
M0387_CRITICAL_AUDIT_SHA256 = "f692b6ef27af1a026c258d84c80d521fbdafe40b7064c2472087820be4b1728b"
CROUZEIX_PROMPT_REPOSITORY = "jinshanmu/CrouzeixConjecture"
CROUZEIX_PROMPT_COMMIT = "f9d5c8d39bece41ceedf6346ef50ad1fb393260e"
CROUZEIX_PROMPT_BLOB_SHA1 = "5b2705db56787157fadbfd9416522feb69b4ad95"
CROUZEIX_PROMPT_SHA256 = "0a0c3000b81efc4d9edc65ec3cd1d53df0d4e69b24bfee9fe0860301d853d6fc"
CROUZEIX_PROMPT_EXTRACTION = DOCS / "researches/Stage5_Crouzeix_Prompt_Extraction.md"
CROUZEIX_PROMPT_EXTRACTION_SHA256 = "14b652acfb374912350a30304cda0a7bda518a2cf1b50f75a18acfa2d10aa871"
CONJECTURE_POOL_CURRENT_SHA256 = "c48fa76ff7bf46b9ffd9fdb05d5b1f5c0fc5a1f26f4848c876d1e6fae79eea9b"
CONJECTURE_POOL_CURRENT_AUTHORITY_SHA256 = "aee07baeb701c3b377a0360182e148a4132e2d67ca5c61f83a7d4f9cb59c479d"
CONJECTURE_POOL_MANIFEST_SHA256 = "9e379aa55c6bb4a5f1c2897c8f9a5a9024a80135be399d622f42f12a3c207e66"
CONJECTURE_POOL_MANIFEST_AUTHORITY_SHA256 = "b9eb56d8d148f6da25d3ca8f63db2d92717a8211b7e916a81f702f87c386a143"
CONJECTURE_POOL_OCCURRENCES_SHA256 = "d3256351a80f1a5949e7c09dc521d84756006eec47938006a7d3a45e357b2241"
CONJECTURE_POOL_IDENTITIES_SHA256 = "b3416ceae5106cb2682ada5ce4b053836c37ac96f9aa44ec3d31b5d245db7f54"
CONJECTURE_RUNTIME_AUTHORITY_EPOCH = "stage5-conjecture-occurrence-pool-v2"
CONJECTURE_POOL_ID_SET_SHA256 = "61ce24a8dfbdb7cafceb9b7fdf9824064154b6d2b7cfdfb62c5bfb0b1bfb5e0f"
CONJECTURE_POOL_SOURCE_RECORD_SET_SHA256 = "368866db01969bd0635c25ef97a1d403a5bfc2a99040425353548f71c878e2b6"
CONJECTURE_POOL_SOURCE_ARCHIVE_SHA256 = "9e0493e5b67767f6636c5518d6bca7326b971dda54a6df237084c51151da2ead"
CONJECTURE_POOL_SOURCE_COMMIT = "357bcb1a1daf93917d42e8206ceaa55645729a09"
CONJECTURE_POOL_COUNT = 14865
CONJECTURE_STRICT_TARGET_COUNT = 1425
CONJECTURE_INTAKE_TARGET_COUNT = CONJECTURE_POOL_COUNT
CONJECTURE_TOTAL_TARGET_COUNT = CONJECTURE_STRICT_TARGET_COUNT + CONJECTURE_INTAKE_TARGET_COUNT

CHECKLIST_BEGIN = "<!-- STAGE5-PROOF-DEBT-EXECUTION-CHECKLIST:BEGIN -->"
CHECKLIST_END = "<!-- STAGE5-PROOF-DEBT-EXECUTION-CHECKLIST:END -->"
SPEC_BEGIN = "<!-- STAGE5-PROOF-DEBT-EXECUTION-SPEC:BEGIN -->"
SPEC_END = "<!-- STAGE5-PROOF-DEBT-EXECUTION-SPEC:END -->"
REQUIREMENTS_BEGIN = "<!-- STAGE5-PROOF-DEBT-REQUIREMENTS:BEGIN -->"
REQUIREMENTS_END = "<!-- STAGE5-PROOF-DEBT-REQUIREMENTS:END -->"
GANTT_META_BEGIN = "<!-- STAGE5-PROOF-DEBT-GANTT-METADATA:BEGIN -->"
GANTT_META_END = "<!-- STAGE5-PROOF-DEBT-GANTT-METADATA:END -->"
GANTT_INDEX_BEGIN = "<!-- STAGE5-PROOF-DEBT-GANTT-INDEX:BEGIN -->"
GANTT_INDEX_END = "<!-- STAGE5-PROOF-DEBT-GANTT-INDEX:END -->"

ROW_RE = re.compile(
    r"^- \[(?P<state>[ _x])\] `(?P<id>[A-Z0-9-]+)` "
    r"(?P<title>.+?) \| depends_on=(?P<depends>[^|]+?) "
    r"\| owned_paths=(?P<paths>[^|]+?) \| gate=(?P<gate>.+)$"
)
CHECKBOX_LINE_RE = re.compile(r"^- \[[ _x]\] ", re.MULTILINE)
RFC3339_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SAFE_COMPONENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,191}$")

BLUEPRINT_MARKER_PAIRS = (
    ("checklist", CHECKLIST_BEGIN, CHECKLIST_END),
    ("specification", SPEC_BEGIN, SPEC_END),
    ("requirements", REQUIREMENTS_BEGIN, REQUIREMENTS_END),
)
GANTT_MARKER_PAIRS = (
    ("metadata", GANTT_META_BEGIN, GANTT_META_END),
    ("index", GANTT_INDEX_BEGIN, GANTT_INDEX_END),
)


class BlueprintError(RuntimeError):
    """Fail-closed blueprint or projection error."""


def validate_marker_constants() -> None:
    document_markers = [
        marker
        for _, begin, end in BLUEPRINT_MARKER_PAIRS + GANTT_MARKER_PAIRS
        for marker in (begin, end)
    ]
    cron_markers = [
        THEOREM.cron_marker_begin,
        THEOREM.cron_marker_end,
        CONJECTURE.cron_marker_begin,
        CONJECTURE.cron_marker_end,
    ]
    if len(document_markers) != len(set(document_markers)):
        raise BlueprintError("document marker identities are not globally unique")
    if len(cron_markers) != len(set(cron_markers)):
        raise BlueprintError("theorem/conjecture cron marker identities overlap")
    if any("\n" in marker or "\r" in marker for marker in document_markers + cron_markers):
        raise BlueprintError("marker identity contains a line break")


def validate_marker_pairs(text: str, pairs: Iterable[tuple[str, str, str]], label: str) -> None:
    for name, begin, end in pairs:
        if text.count(begin) != 1 or text.count(end) != 1:
            raise BlueprintError(f"{label}: {name} marker identity/count drift")
        if text.index(begin) >= text.index(end):
            raise BlueprintError(f"{label}: {name} marker order drift")


@dataclass(frozen=True)
class Task:
    item_id: str
    title: str
    dependencies: tuple[str, ...]
    owned_paths: tuple[str, ...]
    gate: str
    state: str = " "

    def with_state(self, state: str) -> "Task":
        return Task(
            self.item_id,
            self.title,
            self.dependencies,
            self.owned_paths,
            self.gate,
            state,
        )


@dataclass(frozen=True)
class Program:
    kind: str
    blueprint: Path
    gantt: Path
    version: str
    schema: str
    task_prefix: str
    target_count: int
    phase_count: int
    runtime_root: str
    cron_marker_begin: str
    cron_marker_end: str


@dataclass(frozen=True)
class PreparedProgram:
    program: Program
    tasks: tuple[Task, ...]
    blueprint: bytes
    gantt: bytes
    expected_blueprint: FileExpectation | None
    expected_gantt: FileExpectation | None


@dataclass(frozen=True)
class FileExpectation:
    sha256: str
    stat_identity: dict[str, int]


THEOREM = Program(
    kind="theorem",
    blueprint=DOCS / "Stage5_Theorems_Blueprint.md",
    gantt=DOCS / "Stage5_Theorems_Gantt.md",
    version="stage5-theorem-proof-debt/2.0",
    schema="awesome-theorems/stage5-theorems-blueprint/2.0",
    task_prefix="S5THM",
    target_count=3500,
    phase_count=1,
    runtime_root=".ops/stage5-theorems-execution-v2",
    cron_marker_begin="# BEGIN AWESOME_THEOREMS_STAGE5_THEOREMS_EXECUTION_V2",
    cron_marker_end="# END AWESOME_THEOREMS_STAGE5_THEOREMS_EXECUTION_V2",
)

CONJECTURE = Program(
    kind="conjecture",
    blueprint=DOCS / "Stage5_Conjectures_Blueprint.md",
    gantt=DOCS / "Stage5_Conjectures_Gantt.md",
    version="stage5-conjecture-proof-debt/2.0",
    schema="awesome-theorems/stage5-conjectures-blueprint/2.0",
    task_prefix="S5CON",
    target_count=CONJECTURE_TOTAL_TARGET_COUNT,
    phase_count=1,
    runtime_root=".ops/stage5-conjectures-execution-v2",
    cron_marker_begin="# BEGIN AWESOME_THEOREMS_STAGE5_CONJECTURES_EXECUTION_V2",
    cron_marker_end="# END AWESOME_THEOREMS_STAGE5_CONJECTURES_EXECUTION_V2",
)

OBJECT_WORKER_V2_MIGRATION_RECEIPT = (
    DOCS
    / "evidence/stage5_shared_execution"
    / "one-object-one-goal-v1-to-v2-migration.json"
)
PROGRAM_ISOLATION_V3_MIGRATION_RECEIPT = (
    DOCS
    / "evidence/stage5_shared_execution/blueprint-migrations"
    / "S5PD-BLUEPRINT-MIGRATE-000001-program-isolation.json"
)


def program_isolation_migration_receipts() -> tuple[Path, ...]:
    root = PROGRAM_ISOLATION_V3_MIGRATION_RECEIPT.parent
    if not root.is_dir():
        return ()
    return tuple(sorted(
        path for path in root.glob("S5PD-BLUEPRINT-MIGRATE-*-program-isolation.json")
        if path.is_file() and not path.is_symlink()
    ))


def latest_program_isolation_migration_receipt() -> Path | None:
    receipts = program_isolation_migration_receipts()
    return receipts[-1] if receipts else None


def program_isolation_active(program: Program) -> bool:
    """Do not let canonical migration evidence weaken arbitrary fixture repos."""
    canonical_paths = {
        "theorem": (DOCS / "Stage5_Theorems_Blueprint.md", DOCS / "Stage5_Theorems_Gantt.md"),
        "conjecture": (DOCS / "Stage5_Conjectures_Blueprint.md", DOCS / "Stage5_Conjectures_Gantt.md"),
    }
    expected = canonical_paths.get(program.kind)
    return expected is not None and (program.blueprint, program.gantt) == expected and latest_program_isolation_migration_receipt() is not None


def next_program_isolation_migration_receipt() -> Path:
    root = PROGRAM_ISOLATION_V3_MIGRATION_RECEIPT.parent
    ordinals: list[int] = []
    if root.is_dir():
        for path in root.glob("S5PD-BLUEPRINT-MIGRATE-*.json"):
            match = re.search(r"MIGRATE-(\d+)-", path.name)
            if match:
                ordinals.append(int(match.group(1)))
    return root / f"S5PD-BLUEPRINT-MIGRATE-{max(ordinals, default=0) + 1:06d}-program-isolation.json"


def lifecycle_migration_receipts() -> tuple[Path, ...]:
    root = PROGRAM_ISOLATION_V3_MIGRATION_RECEIPT.parent
    if not root.is_dir():
        return ()
    return tuple(sorted(
        path for path in root.glob("S5PD-BLUEPRINT-MIGRATE-*-lifecycle.json")
        if path.is_file() and not path.is_symlink()
    ))


def next_lifecycle_migration_receipt() -> Path:
    root = PROGRAM_ISOLATION_V3_MIGRATION_RECEIPT.parent
    ordinals: list[int] = []
    if root.is_dir():
        for path in root.glob("S5PD-BLUEPRINT-MIGRATE-*.json"):
            match = re.search(r"MIGRATE-(\d+)-", path.name)
            if match:
                ordinals.append(int(match.group(1)))
    return root / f"S5PD-BLUEPRINT-MIGRATE-{max(ordinals, default=0) + 1:06d}-lifecycle.json"
LEGACY_V1_MIGRATION_AUTHORITIES = {
    "theorem": {
        "program": "stage5-theorem-proof-debt/1.0",
        "runtime_root": ".ops/stage5-theorems-execution-v1",
        "shared_runtime_root": ".ops/stage5-proof-debt-shared-v1",
        "blueprint_sha256": "5cb94720290319522b5f1d8341828ac2aaacb6404ce763dfeca69b9c45bf7806",
        "gantt_sha256": "757713ba55ce615ff48f4490399fe84a8fbd060f27201ab130075d436b1df01f",
        "row_count": 28075,
        "mathematical_row_count": 28000,
    },
    "conjecture": {
        "program": "stage5-conjecture-proof-debt/1.0",
        "runtime_root": ".ops/stage5-conjectures-execution-v1",
        "shared_runtime_root": ".ops/stage5-proof-debt-shared-v1",
        "blueprint_sha256": "c3dfec04aec441b31de19386908d214127364c4203b5bd8dbf3552794ee444cc",
        "gantt_sha256": "fb18cf9eb72ef11ec90bb7fd7b537e072b0ed51da872108d2c03ceaeea4aa7c4",
        "row_count": 15708,
        "mathematical_row_count": 15675,
    },
}

REVIEWED_PRISTINE_FORCE_PAIRS = {
    "theorem": {
        "blueprint_sha256": "9772e01ff6cd32e0b9886600c9c30eea59bb2d51bbe8f373ea56b1dfc6171236",
        "gantt_sha256": "719af334c4d8bee162d8074e79077e3e4f649ae37719a26be13bcfaf0d90bd51",
    },
    "conjecture": {
        "blueprint_sha256": "b3874efbf725278c02399977823e438f280e99b46d2bdd3ae77b59722bffe1ed",
        "gantt_sha256": "1b58f7695e983fc528880d79eeec6cb255c765dc05eac89a13e14f57155995f4",
    },
}
BOOTSTRAP_TRANSACTION_PREFIX = ".stage5-proof-debt-bootstrap-txn-"
CANONICAL_PYTHON = Path("/usr/bin/python3.12")
CANONICAL_CRONTAB = Path("/usr/bin/crontab")
CANONICAL_TMUX = Path("/usr/bin/tmux")
BOOT_COMMAND_TIMEOUT_SECONDS = 300
BOOT_COMMAND_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "PYTHONHASHSEED": "0",
}
BOOT_SANDBOX_PATH = ROOT / "scripts/stage5_boot_command_sandbox.py"
BOOT_SANDBOX_SHA256 = "646c7eab5ad810a46dd3ff2c2147eb422a998a570f8a22636a99e0952f0e441d"
BOOT_COMPILE_CHECK_PATH = ROOT / "scripts/stage5_boot_compile_check.py"
BOOT_COMPILE_CHECK_SHA256 = "00491bc4badccffaa7eddb60ec018e9ce4396bcacbb32e731452229b82f44dbd"
LEAN_PREFLIGHT_PATH = ROOT / "scripts/check_lean_environment.py"
LEAN_PREFLIGHT_SHA256 = "4f78ef89721f8dc7e15e640b22f1ea113b6b4f400a3e6e783bcda7077a9addd0"
CANONICAL_ELAN = Path("/home/sansha/.elan/bin/elan")
CANONICAL_ELAN_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
BOOT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@-]{0,199}$")
BOOT_SIGNATURE_RE = re.compile(r"^[0-9a-f]{128}$")
BOOT_HANDOFF_SCHEMA = "awesome-theorems/stage5-bootstrap-handoff/2.0"
BOOT_REVIEW_SCHEMA = "awesome-theorems/stage5-bootstrap-review/2.0"
BOOT_DECISION_SCHEMA = "awesome-theorems/stage5-bootstrap-review-decision/2.0"
BOOT_HANDOFF_ACCEPTANCE_SCHEMA = "awesome-theorems/stage5-bootstrap-handoff-acceptance/2.0"
BOOT_ACCEPTANCE_SCHEMA = "awesome-theorems/stage5-bootstrap-acceptance/2.0"
BOOT_ROLE_SCHEMA = "awesome-theorems/stage5-bootstrap-role-attestation/2.0"
BOOT_TRUST_ROOT_SCHEMA = "awesome-theorems/stage5-bootstrap-role-trust-root/2.0"
BOOT_CLAIM_SCHEMA = "awesome-theorems/stage5-bootstrap-claim-card/2.0"
BOOT_ROLE_TRUST_ROOT_NAME = "controller-bootstrap-role-trust-root.json"
BOOT_ROLE_TRUST_ROOT_SHA256: dict[str, str | None] = {
    "theorem": "303198bfede03b0331766b737094fc0005ecdd94144ee05d634a3bc54c19be6a",
    "conjecture": "abbbe600a310b6b74c7953a1fbc057f64705caa9c84523e6f1cfd77ed2e3a812",
}
# These are values for the checked-in operator-prompt fixtures only.  They are
# deliberately kept out of the execution specification and Blueprint: a
# controller must receive a complete prompt vector at invocation time.
THEOREM_PROMPT_CONCURRENCY = {
    "logical_claims": 24,
    "service_records": "not_applicable",
    "agent_executions": 24,
    "startup_reservations": 24,
    "launch_fanout_per_wave": 4,
    "live_transports": 24,
    "authenticated_goals": 24,
    "running_turns": 24,
    "outbound_request_starts_per_window": 24,
    "in_flight_requests": 24,
    "integration": 1,
    "validators": 4,
    "exact_path_conflicts": 0,
}
CONJECTURE_PROMPT_CONCURRENCY = {
    "logical_claims": 2,
    "service_records": "not_applicable",
    "agent_executions": 2,
    "startup_reservations": 2,
    "launch_fanout_per_wave": 2,
    "live_transports": 2,
    "authenticated_goals": 2,
    "running_turns": 2,
    "outbound_request_starts_per_window": 2,
    "in_flight_requests": 2,
    "integration": 1,
    "validators": 4,
    "exact_path_conflicts": 0,
}
CONCURRENCY_PROMPT_SCHEMA = "awesome-theorems/stage5-concurrency-prompt/2.0"
CONCURRENCY_DIMENSIONS = tuple(THEOREM_PROMPT_CONCURRENCY)
FROZEN_CODEX_MODEL = "gpt-5.6-sol"
CONJECTURE_FROZEN_CODEX_MODEL = "gpt-5.6-sol"
FROZEN_CODEX_REASONING_EFFORT = "ultra"
THEOREM_FROZEN_CODEX_SERVICE_TIER = "default"
CONJECTURE_FROZEN_CODEX_SERVICE_TIER = "default"
OPERATOR_GOAL_THREAD_ID = "01a00af8-9991-79e2-819b-f36effd4313d"
OPERATOR_GOAL_OBJECTIVE_SHA256 = "5fe47afd3a9bd1c2f03c67b97d6ec347a98535d83d1a15b78a31c3c108837bea"
OPERATOR_GOAL_TRUST_ROOT_SHA256 = "99afcd88bcb440d6f231f167e3f09198daf8837385ae9ad8770c4e29e9a8b20a"
CONJECTURE_OPERATOR_GOAL_THREAD_ID = "019fe8d5-f4f1-7820-af7a-b7a365cddf65"
CONJECTURE_OPERATOR_GOAL_OBJECTIVE_SHA256 = "157c73797eb2df07befd0e15efaaf4f9763b1ff64f81076891511a994d77a7ca"
CONJECTURE_OPERATOR_GOAL_TRUST_ROOT_SHA256 = "b565d0e27d59d71385fba95adbfd7ca307723b0ab1958289fead6d2e7fcd8277"
BOOT_ROLE_FIELDS = {
    "schema_version",
    "program",
    "role",
    "principal_id",
    "key_id",
    "principal_context",
    "claim_id",
    "run_id",
    "item_id",
    "manager_sha256",
    "source_bundle_sha256",
    "execution_spec_sha256",
    "observed_at",
    "signature_algorithm",
    "signed_payload_sha256",
    "signature",
    "authority_sha256",
}
BOOT_REVIEW_GATES = (
    "closed_workset_and_source_aliases",
    "generic_trust_zero_validator",
    "ongoing_blueprint_gantt_checker",
    "interactive_tmux_codex_controller",
    "operator_budget_and_program_coordinator_fail_closed",
    "mutation_and_crash_recovery_suite",
    "two_repository_portability",
    "scoped_stop_completion_cleanup",
)
BOOT_COMMANDS = {
    "theorem": (
        ("scripts/stage5_boot_compile_check.py", "scripts/check_stage5_theorem_claim.py"),
        ("scripts/stage5_boot_compile_check.py", "scripts/check_stage5_theorem_item.py"),
        ("scripts/stage5_boot_compile_check.py", "Docs/tools/check_stage5_theorems_blueprint.py"),
        ("scripts/stage5_boot_compile_check.py", "Docs/tools/generate_stage5_theorems_gantt.py"),
        ("scripts/stage5_boot_compile_check.py", "scripts/stage5_theorems_execution_cron_v2.py"),
        ("scripts/test_stage5_theorems_blueprint.py",),
        ("scripts/test_stage5_theorems_execution_cron_v2.py",),
    ),
    "conjecture": (
        ("scripts/stage5_boot_compile_check.py", "scripts/check_stage5_conjecture_claim.py"),
        ("scripts/stage5_boot_compile_check.py", "Docs/tools/check_stage5_conjectures_blueprint.py"),
        ("scripts/stage5_boot_compile_check.py", "Docs/tools/generate_stage5_conjectures_gantt.py"),
        ("scripts/stage5_boot_compile_check.py", "scripts/stage5_conjectures_execution_cron_v2.py"),
        ("scripts/stage5_conjectures_execution_cron_v2.py", "--validate-only"),
        ("scripts/test_stage5_conjecture_claim.py",),
        ("scripts/test_stage5_conjectures_blueprint.py",),
        ("scripts/test_stage5_conjectures_execution_cron_v2.py",),
    ),
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def manager_code_sha256() -> str:
    path = Path(__file__).resolve()
    if path != ROOT / "Docs/tools/manage_stage5_proof_debt_blueprints.py" or path.is_symlink():
        raise BlueprintError("BOOT acceptor code is not the canonical manager file")
    return sha256_bytes(path.read_bytes())


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def prompt_concurrency_values(program: Program) -> dict[str, int | str]:
    """Return only the checked-in prompt fixture, never an execution default."""
    values = THEOREM_PROMPT_CONCURRENCY if program.kind == "theorem" else CONJECTURE_PROMPT_CONCURRENCY
    return dict(values)


def concurrency_prompt_epoch(program: Program) -> str:
    return (
        "stage5-concurrency-prompt-2026-08-17-24-sol-default-subagents-4"
        if program.kind == "theorem"
        else "stage5-conjecture-concurrency-prompt-2026-08-16-sol-lifecycle-3"
    )


def concurrency_prompt_path(program: Program) -> str:
    return f"Docs/evidence/stage5_{program.kind}s/execution/concurrency-prompt.json"


def concurrency_prompt_object(
    program: Program,
    *,
    specification_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    # This is a checked-in operator fixture, not a controller fallback.  It
    # is intentionally complete so the execution controller can reject any
    # stale/partial artifact before it creates a runtime or reservation.
    thread_id, objective_sha256, _ = operator_goal_binding(program)
    spec_path = DOCS / "evidence" / f"stage5_{program.kind}s" / "execution-spec.json"
    if specification_override is not None:
        specification = specification_override
    elif spec_path.is_file() and not spec_path.is_symlink():
        # Bind the fixture to the exact currently authoritative spec bytes.
        # Recomputing spec_object() here would include a manager self-digest
        # that changes whenever this generator is repaired, making a prompt
        # claim a spec that is not yet on disk.
        specification = strict_json_loads(spec_path.read_bytes(), str(spec_path))
    else:
        specification = spec_object(program)
    body = {
        "schema_version": CONCURRENCY_PROMPT_SCHEMA,
        "program": program.version,
        "policy_epoch": concurrency_prompt_epoch(program),
        "execution_spec_sha256": sha256_bytes(canonical(specification)),
        "operator_identity": f"codex-user-goal:{thread_id}",
        "operator_goal_thread_id": thread_id,
        "operator_goal_objective_sha256": objective_sha256,
        "request_window_seconds": 120,
        "source": "explicit operator prompt fixture; not a controller or Blueprint default",
        "concurrency": prompt_concurrency_values(program),
        "execution_limits": {
            "generation_lifetime_seconds": 1209600,
            "model_input_tokens": 2000000,
            "model_output_tokens": 500000,
            "model_turns": "unbounded",
            "cpu_seconds": 1209600,
            "external_launches": 4,
        },
        "recovery": {
            "startup_attempts_per_generation": 1,
            "provider_attempts_per_request": 60,
            "repair_attempts_per_failure_identity": 3,
            "generation_replacements_per_work_item": 60,
            "backoff_initial_seconds": 60,
            "backoff_max_seconds": 3600,
            "backoff_multiplier": 2,
            "backoff_jitter_ratio": 0.2,
            "retry_after_precedence": "provider_retry_after_then_exponential",
            "breaker_failure_classes": ["http_429", "http_503", "provider_unavailable"],
            "breaker_scope": "provider",
            "breaker_failure_threshold": 3,
            "breaker_cooldown_seconds": 1800,
        },
    }
    return {**body, "authority_sha256": sha256_bytes(canonical(body))}


def concurrency_prompt_bytes(
    program: Program,
    *,
    specification_override: dict[str, Any] | None = None,
) -> bytes:
    """Return the exact bytes used by the checked-in prompt fixture."""
    return (
        json.dumps(
            concurrency_prompt_object(
                program, specification_override=specification_override,
            ),
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
    )


def concurrency_prompt_contract(program: Program) -> dict[str, Any]:
    return {
        "schema_version": CONCURRENCY_PROMPT_SCHEMA,
        "prompt_path": concurrency_prompt_path(program),
        "required_dimensions": list(CONCURRENCY_DIMENSIONS),
        "accepted_value_types": ["non_negative_integer", "not_applicable"],
        "value_source": "explicit_execution_prompt_only",
        "missing_policy": "fail_closed_before_materialization_or_launch",
        "unknown_dimension_policy": "fail_closed",
        "stale_prompt_policy": "fail_closed_when_policy_epoch_or_program_mismatches",
        "resolution": "requested_vector_is recorded verbatim; host/resource checks may only reduce it and must record each binding reason",
        "lane_generation_protocol": {
            "lane": "durable logical capacity slot bound to one immutable TARGET item",
            "generation": "fresh task root, private tmux server/socket/session, private CODEX_HOME, thread and exactly one /goal per admitted replacement",
            "replacement": "harvest and fence the old generation before reusing its lane; never reuse task roots, tmux identities, private homes or goals",
        },
        "request_policy": "one outstanding request per generation; rate and in-flight ceilings come from the same prompt vector",
        "prompt_digest": "controller records SHA-256 of exact prompt bytes in admission, Gantt and runtime snapshots",
        "execution_limits": {
            "generation_lifetime_seconds": 1209600,
            "model_input_tokens": 2000000,
            "model_output_tokens": 500000,
            "model_turns": "unbounded",
            "cpu_seconds": 1209600,
            "external_launches": 4,
        },
        "recovery": {
            "startup_attempts_per_generation": 1,
            "provider_attempts_per_request": 60,
            "repair_attempts_per_failure_identity": 3,
            "generation_replacements_per_work_item": 60,
            "backoff_initial_seconds": 60,
            "backoff_max_seconds": 3600,
            "backoff_multiplier": 2,
            "backoff_jitter_ratio": 0.2,
            "retry_after_precedence": "provider_retry_after_then_exponential",
            "breaker_failure_classes": ["http_429", "http_503", "provider_unavailable"],
            "breaker_scope": "provider",
            "breaker_failure_threshold": 3,
            "breaker_cooldown_seconds": 1800,
        },
        "lifecycle_policy": "goal lifetime is fourteen days; each stable work item admits one initial generation plus at most sixty non-overlapping replacement generations; turn count is unlimited, while token/CPU/launch ceilings remain explicit",
        "resolution": "requested_vector_is recorded verbatim; host/resource checks may only reduce it and must record each binding reason",
    }


def frozen_codex_service_tier(program: Program) -> str:
    return (
        THEOREM_FROZEN_CODEX_SERVICE_TIER
        if program.kind == "theorem"
        else CONJECTURE_FROZEN_CODEX_SERVICE_TIER
    )


def frozen_codex_model(program: Program) -> str:
    return FROZEN_CODEX_MODEL if program.kind == "theorem" else CONJECTURE_FROZEN_CODEX_MODEL


def operator_goal_binding(program: Program) -> tuple[str, str, str]:
    if program.kind == "theorem":
        return (
            OPERATOR_GOAL_THREAD_ID,
            OPERATOR_GOAL_OBJECTIVE_SHA256,
            OPERATOR_GOAL_TRUST_ROOT_SHA256,
        )
    return (
        CONJECTURE_OPERATOR_GOAL_THREAD_ID,
        CONJECTURE_OPERATOR_GOAL_OBJECTIVE_SHA256,
        CONJECTURE_OPERATOR_GOAL_TRUST_ROOT_SHA256,
    )


def operator_goal_trust_root_object(program: Program = THEOREM) -> dict[str, Any]:
    thread_id, objective_sha256, _ = operator_goal_binding(program)
    return {
        "schema_version": "awesome-theorems/stage5-operator-goal-trust-root/1.0",
        "authority_mode": "local_codex_active_goal_registry_binding",
        "operator_identity": f"codex-user-goal:{thread_id}",
        "thread_id": thread_id,
        "objective_sha256": objective_sha256,
        "verification": "controller requires the exact active local Codex goal thread/objective/status before activation and each launch; this is a pinned local operator instruction binding, not a cryptographic signature or price attestation",
        "renewal": "requires a new explicit user instruction and reviewed authority migration",
    }


def operator_budget_authority_object(
    program: Program = THEOREM,
    *,
    worker_launch_authorized: bool = False,
) -> dict[str, Any]:
    if not isinstance(worker_launch_authorized, bool):
        raise BlueprintError("worker launch authorization must be an explicit boolean")
    service_tier = frozen_codex_service_tier(program)
    thread_id, objective_sha256, trust_root_sha256 = operator_goal_binding(program)
    body = {
        "schema_version": "awesome-theorems/stage5-operator-budget-authority/1.0",
        "operator_identity": f"codex-user-goal:{thread_id}",
        "authority_mode": "local_codex_active_goal_registry_binding",
        "goal_thread_id": thread_id,
        "goal_objective_sha256": objective_sha256,
        "trust_root_sha256": trust_root_sha256,
        "issued_at": "2026-08-11T00:00:00Z",
        "expires_at": "2027-08-11T00:00:00Z",
        "billing_mode": "operator_goal_authorized_unknown_price",
        "billing_binding": {
            "provider": "sub2api",
            "model": frozen_codex_model(program),
            "reasoning_effort": FROZEN_CODEX_REASONING_EFFORT,
            "service_tier": service_tier,
            "monetary_price": "unknown_not_zero",
        },
            "program_allowances": {
            "stage5-theorem-proof-debt/2.0": {
                "model_input_tokens": 2000000000,
                "model_output_tokens": 500000000,
                "model_turns": "unbounded",
                "external_launches": 960,
                "wall_seconds": 145152000,
                "cpu_seconds": 145152000,
                "worker_launch_authorized": (
                    worker_launch_authorized if program.kind == "theorem" else False
                ),
            },
            "stage5-conjecture-proof-debt/2.0": {
                "worker_launch_authorized": False,
            },
        },
        "combined_allowances": {
            "model_input_tokens": 2000000000,
            "model_output_tokens": 500000000,
            "model_turns": "unbounded",
            "external_launches": 960,
            "wall_seconds": 145152000,
            "cpu_seconds": 145152000,
            "authenticated_live_goals": (
                prompt_concurrency_values(program)["authenticated_goals"]
                if program.kind == "theorem" else 0
            ),
        },
        "per_claim_maxima": {
            "model_input_tokens": 2000000,
            "model_output_tokens": 500000,
            "model_turns": "unbounded",
            "external_launches": 4,
            "wall_seconds": 1209600,
            "cpu_seconds": 1209600,
            "generation_lifetime_seconds": 1209600,
            "generation_replacements_per_work_item": 60,
        },
        "worker_launch_authorized": worker_launch_authorized,
        "concurrency_prompt_epoch": concurrency_prompt_epoch(program),
        "resolved_concurrency": prompt_concurrency_values(program),
        "concurrency_prompt_sha256": sha256_bytes(concurrency_prompt_bytes(program)),
        "reserve_policy": "reserve every per-claim worst case under the shared budget lease before launch; settle measured usage and never infer unknown monetary price as zero",
    }
    return {**body, "authority_sha256": sha256_bytes(canonical(body))}


def strict_json_loads(raw: bytes | str, label: str) -> Any:
    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise BlueprintError(f"{label}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    def reject_constant(value: str) -> Any:
        raise BlueprintError(f"{label}: non-finite JSON number {value}")

    try:
        return json.loads(
            raw,
            object_pairs_hook=pairs_hook,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BlueprintError(f"{label}: invalid JSON") from exc


def set_digest(values: Iterable[str]) -> str:
    return sha256_bytes(canonical(sorted(values)))


def read_bound_json(path: Path, expected_sha: str) -> dict[str, Any]:
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != expected_sha:
        raise BlueprintError(f"{path.relative_to(ROOT)} SHA drift: {observed}")
    value = strict_json_loads(raw, path.relative_to(ROOT).as_posix())
    if not isinstance(value, dict):
        raise BlueprintError(f"expected JSON object: {path}")
    return value


def validate_canonical_root() -> None:
    authority = sha256_bytes(
        canonical(
            {
                "canonical_repository_root": CANONICAL_ROOT.as_posix(),
                "relocation_policy": ROOT_RELOCATION_POLICY,
            }
        )
    )
    if authority != CANONICAL_ROOT_AUTHORITY_SHA256:
        raise BlueprintError("compiled canonical-root authority is internally inconsistent")
    # BOOT's Landlock runner executes the exact source bundle from a
    # content-addressed /tmp snapshot.  That is an intentionally bounded,
    # read-only relocation of the canonical tree; all normal controller and
    # worker processes must still use CANONICAL_ROOT exactly.
    boot_snapshot = os.environ.get("STAGE5_BOOT_SANDBOX") == "1" and os.environ.get("STAGE5_BOOT_CANONICAL_ROOT") == CANONICAL_ROOT.as_posix() and str(ROOT).startswith("/tmp/stage5-boot-snapshot-")
    if boot_snapshot:
        if not ROOT.is_dir() or ROOT.is_symlink() or ROOT.resolve(strict=True) != ROOT:
            raise BlueprintError("BOOT snapshot root is not a canonical real directory")
        return
    if (
        ROOT != CANONICAL_ROOT
        or not CANONICAL_ROOT.is_dir()
        or CANONICAL_ROOT.is_symlink()
        or CANONICAL_ROOT.resolve(strict=True) != CANONICAL_ROOT
    ):
        raise BlueprintError(
            f"repository root relocation requires a reviewed specification migration: "
            f"expected {CANONICAL_ROOT}, observed {ROOT}"
        )


@lru_cache(maxsize=1)
def validate_stage5_release_chain() -> None:
    validate_canonical_root()
    current = read_bound_json(STAGE5_CURRENT, STAGE5_CURRENT_SHA256)
    manifest = read_bound_json(STAGE5_MANIFEST, RELEASE_MANIFEST_SHA256)
    if (
        current.get("schema_version") != "awesome-theorems/stage5-current-release/5.6"
        or current.get("release") != "5.6"
        or current.get("manifest_path") != "releases/5.6/Release_Manifest.json"
        or current.get("manifest_sha256") != RELEASE_MANIFEST_SHA256
        or current.get("release_root_sha256") != RELEASE_ROOT_SHA256
        or current.get("authority_sha256") != STAGE5_CURRENT_AUTHORITY_SHA256
        or manifest.get("schema_version") != "awesome-theorems/stage5-release-manifest/5.6"
        or manifest.get("release") != "5.6"
        or manifest.get("release_root_sha256") != RELEASE_ROOT_SHA256
        or manifest.get("authority_sha256") != STAGE5_MANIFEST_AUTHORITY_SHA256
    ):
        raise BlueprintError("frozen Stage5 5.6 Current/manifest authority chain drift")
    counts = manifest.get("counts")
    if not isinstance(counts, dict) or (
        counts.get("cumulative_theorems") != 3500
        or counts.get("cumulative_open_claims") != 2025
        or counts.get("effective_strict_conjecture_credits") != 1425
    ):
        raise BlueprintError("frozen Stage5 5.6 manifest denominator drift")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or any(not isinstance(row, dict) for row in artifacts):
        raise BlueprintError("frozen Stage5 5.6 manifest artifacts are malformed")
    by_path = {row.get("path"): row for row in artifacts}
    if len(by_path) != len(artifacts):
        raise BlueprintError("frozen Stage5 5.6 manifest has duplicate artifact paths")
    required = {
        "Theorem_List.json": (THEOREM_SOURCE_SHA256, 3500),
        "Open_Claim_List.json": (OPEN_SOURCE_SHA256, 2025),
        "Strict_Conjecture_Ledger.json": (STRICT_SOURCE_SHA256, 1426),
    }
    for path, (digest, rows) in required.items():
        binding = by_path.get(path)
        if binding is None or binding.get("sha256") != digest or binding.get("row_count") != rows:
            raise BlueprintError(f"Stage5 manifest binding drift for {path}")


@lru_cache(maxsize=1)
def validate_m0387_negative_fixture() -> None:
    meta = read_bound_json(M0387_META, M0387_META_SHA256)
    proof_units = read_bound_json(M0387_PROOF_UNITS, M0387_PROOF_UNITS_SHA256)
    receipt = read_bound_json(M0387_CURRENT_RECEIPT, M0387_CURRENT_RECEIPT_SHA256)
    audit_raw = M0387_CRITICAL_AUDIT.read_bytes()
    if sha256_bytes(audit_raw) != M0387_CRITICAL_AUDIT_SHA256:
        raise BlueprintError("M0387 critical-audit negative fixture drift")
    coverage = proof_units.get("coverage_metrics")
    if (
        meta.get("id") != "THM-M-0387"
        or proof_units.get("theorem_id") != "THM-M-0387"
        or not isinstance(proof_units.get("nodes"), list)
        or len(proof_units["nodes"]) != 132
        or not isinstance(coverage, dict)
        or coverage.get("root_machine_closed") is not False
        or coverage.get("machine_closure")
        != {"numerator": 29, "denominator": 93, "percent": 31.18}
        or receipt.get("theorem_id") != "THM-M-0387"
        or receipt.get("status") != "passed"
    ):
        raise BlueprintError("M0387 negative-fixture semantics drift")


def source_bundle_object(program: Program) -> dict[str, Any]:
    validate_stage5_release_chain()
    validate_m0387_negative_fixture()
    if program.kind == "theorem":
        theorem_inventory()
    elif program.kind == "conjecture":
        strict_inventory()
        conjecture_occurrence_inventory()
        extraction_raw = CROUZEIX_PROMPT_EXTRACTION.read_bytes()
        if sha256_bytes(extraction_raw) != CROUZEIX_PROMPT_EXTRACTION_SHA256:
            raise BlueprintError("pinned Crouzeix prompt extraction drift")
    else:
        raise BlueprintError(f"unknown source-bundle program kind: {program.kind}")
    common: dict[str, Any] = {
        "canonical_repository_root": CANONICAL_ROOT.as_posix(),
        "canonical_root_authority_sha256": CANONICAL_ROOT_AUTHORITY_SHA256,
        "root_relocation_policy": ROOT_RELOCATION_POLICY,
        "stage5_current_sha256": STAGE5_CURRENT_SHA256,
        "stage5_current_authority_sha256": STAGE5_CURRENT_AUTHORITY_SHA256,
        "stage5_manifest_sha256": RELEASE_MANIFEST_SHA256,
        "stage5_manifest_authority_sha256": STAGE5_MANIFEST_AUTHORITY_SHA256,
        "stage5_release_root_sha256": RELEASE_ROOT_SHA256,
        "stage6_current_sha256": STAGE6_CURRENT_SHA256,
        "stage6_current_authority_sha256": STAGE6_CURRENT_AUTHORITY_SHA256,
        "stage6_manifest_sha256": STAGE6_MANIFEST_SHA256,
        "stage6_manifest_authority_sha256": STAGE6_MANIFEST_AUTHORITY_SHA256,
        "stage6_release_root_sha256": STAGE6_RELEASE_ROOT_SHA256,
        "stage6_registry_sha256": STAGE6_REGISTRY_SHA256,
        "stage6_registry_authority_sha256": STAGE6_REGISTRY_AUTHORITY_SHA256,
        "stage6_migration_sha256": STAGE6_MIGRATION_SHA256,
        "stage6_migration_authority_sha256": STAGE6_MIGRATION_AUTHORITY_SHA256,
        "m0387_negative_fixture_meta_sha256": M0387_META_SHA256,
        "m0387_negative_fixture_proof_units_sha256": M0387_PROOF_UNITS_SHA256,
        "m0387_negative_fixture_current_receipt_sha256": M0387_CURRENT_RECEIPT_SHA256,
        "m0387_negative_fixture_critical_audit_sha256": M0387_CRITICAL_AUDIT_SHA256,
    }
    if program.kind == "theorem":
        common.update(
            theorem_projection_sha256=THEOREM_SOURCE_SHA256,
            theorem_projection_authority_sha256=THEOREM_AUTHORITY_SHA256,
            theorem_id_set_sha256=THEOREM_ID_SET_SHA256,
        )
    else:
        common.update(
            strict_ledger_sha256=STRICT_SOURCE_SHA256,
            strict_ledger_authority_sha256=STRICT_AUTHORITY_SHA256,
            strict_id_set_sha256=STRICT_ID_SET_SHA256,
            open_projection_sha256=OPEN_SOURCE_SHA256,
            crouzeix_prompt_repository=CROUZEIX_PROMPT_REPOSITORY,
            crouzeix_prompt_commit=CROUZEIX_PROMPT_COMMIT,
            crouzeix_prompt_blob_sha1=CROUZEIX_PROMPT_BLOB_SHA1,
            crouzeix_prompt_sha256=CROUZEIX_PROMPT_SHA256,
            crouzeix_prompt_extraction_path=CROUZEIX_PROMPT_EXTRACTION.relative_to(ROOT).as_posix(),
            crouzeix_prompt_extraction_sha256=CROUZEIX_PROMPT_EXTRACTION_SHA256,
            conjecture_pool_current_sha256=CONJECTURE_POOL_CURRENT_SHA256,
            conjecture_pool_current_authority_sha256=CONJECTURE_POOL_CURRENT_AUTHORITY_SHA256,
            conjecture_pool_manifest_sha256=CONJECTURE_POOL_MANIFEST_SHA256,
            conjecture_pool_manifest_authority_sha256=CONJECTURE_POOL_MANIFEST_AUTHORITY_SHA256,
            conjecture_pool_occurrences_sha256=CONJECTURE_POOL_OCCURRENCES_SHA256,
            conjecture_pool_identity_registry_sha256=CONJECTURE_POOL_IDENTITIES_SHA256,
            conjecture_pool_id_set_sha256=CONJECTURE_POOL_ID_SET_SHA256,
            conjecture_pool_source_record_set_sha256=CONJECTURE_POOL_SOURCE_RECORD_SET_SHA256,
            conjecture_pool_source_archive_sha256=CONJECTURE_POOL_SOURCE_ARCHIVE_SHA256,
            conjecture_pool_source_commit=CONJECTURE_POOL_SOURCE_COMMIT,
            conjecture_pool_source_occurrence_count=CONJECTURE_POOL_COUNT,
            conjecture_pool_semantic_boundary="source occurrences only; no strict credit, Stage5 claim ID, retired renumbering alias or proof-target admission",
        )
    return common


def source_bundle_sha256(program: Program) -> str:
    return sha256_bytes(canonical(source_bundle_object(program)))


def claim_number(stage_claim_id: str) -> str:
    match = re.fullmatch(r"S5-CLM-(\d{8})", stage_claim_id)
    if match is None:
        raise BlueprintError(f"invalid Stage5 claim ID: {stage_claim_id}")
    return match.group(1)


@lru_cache(maxsize=1)
def stage6_aliases() -> dict[str, dict[str, Any]]:
    validate_stage5_release_chain()
    current = read_bound_json(STAGE6_CURRENT, STAGE6_CURRENT_SHA256)
    manifest = read_bound_json(STAGE6_MANIFEST, STAGE6_MANIFEST_SHA256)
    registry = read_bound_json(STAGE6_REGISTRY, STAGE6_REGISTRY_SHA256)
    migration = read_bound_json(STAGE6_MIGRATION, STAGE6_MIGRATION_SHA256)
    if (
        current.get("schema_version") != "awesome-theorems/stage6-current-release/1.0"
        or current.get("release") != "6.0"
        or current.get("manifest_path") != "releases/6.0/Migration_Manifest.json"
        or current.get("release_root_sha256") != STAGE6_RELEASE_ROOT_SHA256
        or current.get("manifest_sha256") != STAGE6_MANIFEST_SHA256
        or current.get("manifest_authority_sha256") != STAGE6_MANIFEST_AUTHORITY_SHA256
        or current.get("authority_sha256") != STAGE6_CURRENT_AUTHORITY_SHA256
        or manifest.get("schema_version") != "awesome-theorems/stage6-migration-manifest/1.0"
        or manifest.get("stage") != "Stage6"
        or manifest.get("authority_sha256") != STAGE6_MANIFEST_AUTHORITY_SHA256
        or manifest.get("final_migration") is not True
        or registry.get("authority_sha256") != STAGE6_REGISTRY_AUTHORITY_SHA256
        or migration.get("authority_sha256") != STAGE6_MIGRATION_AUTHORITY_SHA256
        or migration.get("stage6_registry_authority_sha256") != STAGE6_REGISTRY_AUTHORITY_SHA256
    ):
        raise BlueprintError("frozen the retired renumbering branch authority chain drift")
    counts = manifest.get("counts")
    if not isinstance(counts, dict) or counts.get("canonical_claims") != 9009:
        raise BlueprintError("Stage6 manifest claim denominator drift")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or any(not isinstance(row, dict) for row in artifacts):
        raise BlueprintError("Stage6 manifest artifacts are malformed")
    by_path = {row.get("path"): row for row in artifacts}
    if len(by_path) != len(artifacts):
        raise BlueprintError("Stage6 manifest has duplicate artifact paths")
    required_artifacts = {
        "Stage6_ID_Registry.json": (
            STAGE6_REGISTRY_SHA256,
            STAGE6_REGISTRY_AUTHORITY_SHA256,
            44815,
        ),
        "Migration_to_Stage6.json": (
            STAGE6_MIGRATION_SHA256,
            STAGE6_MIGRATION_AUTHORITY_SHA256,
            48100,
        ),
    }
    for path, (digest, authority, rows) in required_artifacts.items():
        binding = by_path.get(path)
        if (
            binding is None
            or binding.get("sha256") != digest
            or binding.get("authority_sha256") != authority
            or binding.get("row_count") != rows
        ):
            raise BlueprintError(f"Stage6 manifest binding drift for {path}")
    claims = registry.get("claims")
    if not isinstance(claims, list) or len(claims) != 9009:
        raise BlueprintError("Stage6 registry claim denominator drift")
    aliases: dict[str, dict[str, Any]] = {}
    seen_s6: set[str] = set()
    for row in claims:
        if not isinstance(row, dict):
            raise BlueprintError("Stage6 claim row is not an object")
        s5 = row.get("parent_s5_claim_id")
        s6_claim = row.get("stage6_claim_id")
        s6_variant = row.get("stage6_variant_id")
        parent_variant = row.get("parent_variant_id")
        resolution = row.get("current_resolution")
        if not all(isinstance(value, str) and value for value in (s5, s6_claim, s6_variant, parent_variant)):
            raise BlueprintError("Stage6 claim row lacks exact parent/current identities")
        if not isinstance(resolution, dict) or not isinstance(resolution.get("kind"), str):
            raise BlueprintError("Stage6 claim row lacks current-resolution semantics")
        if s5 in aliases or s6_claim in seen_s6 or row.get("lifecycle") != "current":
            raise BlueprintError("Stage6 claim mapping is not one-to-one current")
        aliases[s5] = {
            "stage6_claim_id": s6_claim,
            "stage6_variant_id": s6_variant,
            "parent_variant_id": parent_variant,
            "current_resolution_kind": resolution["kind"],
            "terminal_stage6_claim_ids": resolution.get("terminal_stage6_claim_ids"),
        }
        seen_s6.add(s6_claim)
    if len(aliases) != 9009:
        raise BlueprintError("retired renumbering alias mapping cardinality drift")
    return aliases


def validate_repo_path(value: str, item_id: str) -> None:
    path = PurePosixPath(value)
    if (
        not value
        or not path.parts
        or path.is_absolute()
        or value != path.as_posix()
        or ".." in path.parts
    ):
        raise BlueprintError(f"{item_id} has noncanonical owned path {value!r}")
    if path.parts[0] in {".git", ".ops"}:
        raise BlueprintError(f"{item_id} owns forbidden runtime/control path {value!r}")
    if any(char in value for char in "|`<>\\*?[]{}"):
        raise BlueprintError(f"{item_id} has unsafe owned path {value!r}")


def canonical_repo_relative_path(value: Any, label: str) -> tuple[str, Path]:
    """Resolve one exact repository-relative regular-file locator without ``..``."""
    if not isinstance(value, str):
        raise BlueprintError(f"{label}: path is not a string")
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or value != path.as_posix()
        or not path.parts
        or "." in path.parts
        or ".." in path.parts
        or any(not SAFE_COMPONENT_RE.fullmatch(part) for part in path.parts)
    ):
        raise BlueprintError(f"{label}: path is not strict repository-relative: {value!r}")
    resolved = ROOT / value
    validate_guard_path(resolved)
    return value, resolved


def canonical_task_relative_path(
    value: Any, task_root: Path, label: str, *, must_exist: bool = True
) -> tuple[str, Path]:
    if not isinstance(value, str):
        raise BlueprintError(f"{label}: path is not a string")
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or value != path.as_posix()
        or not path.parts
        or "." in path.parts
        or ".." in path.parts
        or any(not SAFE_COMPONENT_RE.fullmatch(part) for part in path.parts)
    ):
        raise BlueprintError(f"{label}: path is not strict task-relative: {value!r}")
    resolved = task_root / value
    current = task_root
    for part in path.parts[:-1]:
        current /= part
        if current.is_symlink() or not current.is_dir():
            raise BlueprintError(f"{label}: parent is not a real directory: {current}")
    if must_exist and (resolved.is_symlink() or not resolved.is_file()):
        raise BlueprintError(f"{label}: missing regular file: {resolved}")
    return value, resolved


def split_field(value: str, *, empty: str = "-") -> tuple[str, ...]:
    value = value.strip()
    if value == empty:
        return ()
    parts = tuple(part.strip() for part in value.split(","))
    if not parts or any(not part for part in parts) or len(parts) != len(set(parts)):
        raise BlueprintError(f"invalid list field {value!r}")
    return parts


def theorem_inventory() -> list[dict[str, Any]]:
    validate_stage5_release_chain()
    doc = read_bound_json(THEOREM_SOURCE, THEOREM_SOURCE_SHA256)
    records = doc.get("records")
    ids = doc.get("stage_claim_ids")
    if (
        doc.get("authority_sha256") != THEOREM_AUTHORITY_SHA256
        or doc.get("counts") != {"records": 3500}
        or not isinstance(records, list)
        or not isinstance(ids, list)
        or len(records) != 3500
        or ids != [row.get("stage_claim_id") for row in records]
        or len(set(ids)) != 3500
        or set_digest(ids) != THEOREM_ID_SET_SHA256
    ):
        raise BlueprintError("sealed theorem inventory invariants failed")
    aliases = stage6_aliases()
    for row in records:
        mapping = aliases.get(row["stage_claim_id"])
        if (
            mapping is None
            or mapping["parent_variant_id"] != row.get("variant_id")
            or mapping["current_resolution_kind"] != "current"
            or mapping["terminal_stage6_claim_ids"] != [mapping["stage6_claim_id"]]
        ):
            raise BlueprintError(f"theorem lacks frozen retired renumbering alias: {row['stage_claim_id']}")
    return records


def strict_inventory() -> list[dict[str, Any]]:
    validate_stage5_release_chain()
    strict = read_bound_json(STRICT_SOURCE, STRICT_SOURCE_SHA256)
    open_doc = read_bound_json(OPEN_SOURCE, OPEN_SOURCE_SHA256)
    credits = strict.get("strict_credits")
    records = open_doc.get("records")
    if (
        strict.get("authority_sha256") != STRICT_AUTHORITY_SHA256
        or not isinstance(credits, list)
        or len(credits) != 1425
        or not isinstance(records, list)
    ):
        raise BlueprintError("sealed strict-conjecture ledger invariants failed")
    ids = [row.get("stage_claim_id") for row in credits]
    if len(set(ids)) != 1425 or set_digest(ids) != STRICT_ID_SET_SHA256:
        raise BlueprintError("strict-conjecture member set drift")
    if "S5-CLM-00005311" in set(ids):
        raise BlueprintError("revoked strict credit entered the workset")
    by_id = {row.get("stage_claim_id"): row for row in records}
    if len(by_id) != len(records):
        raise BlueprintError("Open_Claim_List contains duplicate Stage5 IDs")
    aliases = stage6_aliases()
    joined: list[dict[str, Any]] = []
    for credit in credits:
        item_id = credit.get("stage_claim_id")
        record = by_id.get(item_id)
        if record is None:
            raise BlueprintError(f"strict credit lacks open record: {item_id}")
        expected_credit_fields = (
            {
                "stage_claim_id", "variant_id", "origin_release",
                "credit_source_branch", "semantic_key",
                "grants_strict_conjecture_credit", "evidence_sha256",
                "row_sha256",
            }
            if credit.get("origin_release") in {"5.0", "5.2"}
            else {
                "stage_claim_id", "variant_id", "semantic_key",
                "origin_release", "credit_source_branch", "evidence_sha256",
                "catalog_record_sha256", "statement_sha256",
                "curation_row_sha256", "source_row_sha256",
                "source_authority_file_sha256", "allocation_request_sha256",
                "grants_strict_conjecture_credit", "row_sha256",
            }
        )
        credit_body = dict(credit)
        row_sha256 = credit_body.pop("row_sha256", None)
        expected_semantic_key = record.get("semantic_key")
        if not isinstance(expected_semantic_key, str):
            expected_semantic_key = (
                "formal-conjectures-semantic/"
                + str(record.get("semantic_payload_sha256"))
            )
        if (
            set(credit) != expected_credit_fields
            or not isinstance(row_sha256, str)
            or sha256_bytes(canonical(credit_body)) != row_sha256
            or credit.get("grants_strict_conjecture_credit") is not True
            or credit.get("variant_id") != record.get("variant_id")
            or credit.get("origin_release") != record.get("origin_release")
            or credit.get("semantic_key") != expected_semantic_key
        ):
            raise BlueprintError(f"strict credit identity/seal drift: {item_id}")
        if record.get("current_claim_kind") != "conjecture" or record.get("material_status") != "open":
            raise BlueprintError(f"strict member has unexpected status: {item_id}")
        origin = credit["origin_release"]
        if origin in {"5.0", "5.2"}:
            if origin == "5.2":
                evidence_components = {
                    "record_sha256": sha256_bytes(canonical(record)),
                    "content_payload_sha256": str(record.get("content_payload_sha256")),
                    "source_payload_sha256": str(record.get("source_payload_sha256")),
                    "rights_payload_sha256": str(
                        (record.get("rights") or {}).get("rights_payload_sha256")
                    ),
                    "allocation_request_sha256": str(
                        (record.get("allocation") or {}).get("allocation_request_sha256")
                    ),
                }
                expected_branch = "origin_5_2_curated_latex_environment"
            else:
                evidence_components = {
                    "record_sha256": sha256_bytes(canonical(record)),
                    "content_payload_sha256": sha256_bytes(canonical({
                        "formal_statement": record.get("formal_statement"),
                        "mathematical_statement": record.get("mathematical_statement"),
                    })),
                    "source_payload_sha256": sha256_bytes(canonical({
                        "source_id": record.get("source_id"),
                        "locator": record.get("locator"),
                        "formal_statement": record.get("formal_statement"),
                        "provenance": record.get("provenance"),
                    })),
                    "rights_payload_sha256": sha256_bytes(
                        canonical(record.get("rights"))
                    ),
                    "allocation_request_sha256": str(
                        (record.get("allocation") or {}).get("allocation_request_sha256")
                    ),
                }
                expected_branch = "effective_parent_5_1_direct_prop"
            if (
                credit.get("credit_source_branch") != expected_branch
                or credit.get("evidence_sha256")
                != sha256_bytes(canonical(evidence_components))
            ):
                raise BlueprintError(f"strict credit evidence drift: {item_id}")
        elif origin == "5.5":
            source_locator = record.get("source_locator") or {}
            curator = record.get("curator_disposition") or {}
            if (
                credit.get("credit_source_branch")
                != f"origin_5_5_{(record.get('provenance') or {}).get('source_kind')}_reviewed_assertion"
                or credit.get("evidence_sha256") != record.get("content_payload_sha256")
                or credit.get("catalog_record_sha256") != record.get("catalog_record_sha256")
                or credit.get("statement_sha256")
                != (record.get("mathematical_statement") or {}).get("statement_sha256")
                or credit.get("curation_row_sha256") != curator.get("ledger_row_sha256")
                or credit.get("source_row_sha256") != source_locator.get("source_row_sha256")
                or credit.get("source_authority_file_sha256")
                != (source_locator.get("authority_receipt") or {}).get("file_sha256")
                or credit.get("allocation_request_sha256")
                != (record.get("allocation") or {}).get("allocation_request_sha256")
            ):
                raise BlueprintError(f"strict 5.5 credit evidence drift: {item_id}")
        else:
            raise BlueprintError(f"strict credit has unknown origin release: {item_id}")
        mapping = aliases.get(item_id)
        if (
            mapping is None
            or mapping["parent_variant_id"] != record.get("variant_id")
            or mapping["current_resolution_kind"] != "current"
            or mapping["terminal_stage6_claim_ids"] != [mapping["stage6_claim_id"]]
        ):
            raise BlueprintError(f"strict member lacks frozen retired renumbering alias: {item_id}")
        joined.append({"credit": credit, "record": record})
    return joined


@lru_cache(maxsize=1)
def conjecture_occurrence_inventory() -> list[dict[str, Any]]:
    """Load the full, non-credit-bearing ConjectureBench occurrence overlay."""
    current = read_bound_json(CONJECTURE_POOL_CURRENT, CONJECTURE_POOL_CURRENT_SHA256)
    manifest = read_bound_json(CONJECTURE_POOL_MANIFEST, CONJECTURE_POOL_MANIFEST_SHA256)
    if (
        current.get("schema_version") != "awesome-theorems/stage5-current-conjecture-pool/1.0"
        or current.get("pool_release") != "conjecturebench-357bcb1a-occurrences-v1"
        or current.get("manifest_path") != "conjecturebench-357bcb1a/Pool_Manifest.json"
        or current.get("manifest_sha256") != CONJECTURE_POOL_MANIFEST_SHA256
        or current.get("source_occurrence_denominator") != CONJECTURE_POOL_COUNT
        or current.get("base_stage5_release") != "5.6"
        or current.get("base_stage5_release_immutable") is not True
        or current.get("authority_sha256") != CONJECTURE_POOL_CURRENT_AUTHORITY_SHA256
    ):
        raise BlueprintError("Stage5 current conjecture-pool authority drift")
    counts = manifest.get("counts")
    boundary = manifest.get("semantic_boundary")
    artifacts = manifest.get("artifacts")
    source = manifest.get("source")
    if (
        manifest.get("schema_version") != "awesome-theorems/stage5-conjecture-pool-manifest/1.0"
        or manifest.get("pool_release") != current["pool_release"]
        or manifest.get("authority_sha256") != CONJECTURE_POOL_MANIFEST_AUTHORITY_SHA256
        or not isinstance(counts, dict)
        or counts.get("source_occurrences") != CONJECTURE_POOL_COUNT
        or counts.get("strict_credits_granted") != 0
        or counts.get("independently_verified_new_strict_identities") != 0
        or not isinstance(boundary, dict)
        or boundary.get("denominator_kind") != "source_occurrence_candidate_pool"
        or boundary.get("not_a_stage5_catalog_release") is not True
        or boundary.get("not_a_strict_conjecture_ledger") is not True
        or boundary.get("no_stage5_or_stage6_identity_allocation") is not True
        or not isinstance(artifacts, dict)
        or artifacts.get("pool_id_set_sha256") != CONJECTURE_POOL_ID_SET_SHA256
        or artifacts.get("source_record_set_sha256") != CONJECTURE_POOL_SOURCE_RECORD_SET_SHA256
        or not isinstance(source, dict)
        or source.get("commit") != CONJECTURE_POOL_SOURCE_COMMIT
        or source.get("archive_sha256") != CONJECTURE_POOL_SOURCE_ARCHIVE_SHA256
    ):
        raise BlueprintError("Stage5 conjecture-pool manifest boundary drift")
    occurrence_binding = artifacts.get("occurrences")
    identity_binding = artifacts.get("identity_registry")
    if (
        not isinstance(occurrence_binding, dict)
        or occurrence_binding.get("path") != CONJECTURE_POOL_OCCURRENCES.relative_to(ROOT).as_posix()
        or occurrence_binding.get("rows") != CONJECTURE_POOL_COUNT
        or occurrence_binding.get("sha256") != CONJECTURE_POOL_OCCURRENCES_SHA256
        or not isinstance(identity_binding, dict)
        or identity_binding.get("path") != CONJECTURE_POOL_IDENTITIES.relative_to(ROOT).as_posix()
        or identity_binding.get("rows") != CONJECTURE_POOL_COUNT
        or identity_binding.get("sha256") != CONJECTURE_POOL_IDENTITIES_SHA256
        or sha256_bytes(CONJECTURE_POOL_OCCURRENCES.read_bytes()) != CONJECTURE_POOL_OCCURRENCES_SHA256
        or sha256_bytes(CONJECTURE_POOL_IDENTITIES.read_bytes()) != CONJECTURE_POOL_IDENTITIES_SHA256
    ):
        raise BlueprintError("Stage5 conjecture-pool artifact binding drift")
    rows: list[dict[str, Any]] = []
    pool_ids: list[str] = []
    source_record_digests: list[str] = []
    for line_number, line in enumerate(CONJECTURE_POOL_OCCURRENCES.read_bytes().splitlines(), 1):
        row = strict_json_loads(line, f"conjecture occurrence line {line_number}")
        expected_pool_id = f"S5POOL-{line_number:08d}"
        if (
            not isinstance(row, dict)
            or row.get("pool_id") != expected_pool_id
            or row.get("stable_source_key")
            != f"conjecturebench/{row.get('kind')}/{row.get('source_native_id')}"
            or row.get("source_commit") != CONJECTURE_POOL_SOURCE_COMMIT
            or row.get("strict_credit") is not False
            or row.get("independent_current_open_verified") is not False
            or row.get("stage5_claim_id") is not None
            or row.get("stage6_alias") is not None
            or row.get("execution_admission") != "intake_status_rights_dedupe_only"
            or not isinstance(row.get("canonical_record_sha256"), str)
            or not SHA256_RE.fullmatch(row["canonical_record_sha256"])
        ):
            raise BlueprintError(f"invalid conjecture occurrence pool row: {expected_pool_id}")
        body = dict(row)
        authority = body.pop("authority_sha256", None)
        if not isinstance(authority, str) or sha256_bytes(canonical(body)) != authority:
            raise BlueprintError(f"conjecture occurrence seal drift: {expected_pool_id}")
        rows.append(row)
        pool_ids.append(expected_pool_id)
        source_record_digests.append(row["canonical_record_sha256"])
    if len(rows) != CONJECTURE_POOL_COUNT:
        raise BlueprintError("conjecture occurrence denominator drift")
    if (
        set_digest(pool_ids) != CONJECTURE_POOL_ID_SET_SHA256
        or set_digest(source_record_digests)
        != CONJECTURE_POOL_SOURCE_RECORD_SET_SHA256
    ):
        raise BlueprintError("conjecture occurrence ID/source-record set drift")
    identity_rows = CONJECTURE_POOL_IDENTITIES.read_bytes().splitlines()
    if len(identity_rows) != CONJECTURE_POOL_COUNT:
        raise BlueprintError("conjecture identity-review registry denominator drift")
    seen_stable_keys: set[str] = set()
    for line_number, (line, occurrence) in enumerate(zip(identity_rows, rows), 1):
        relation = strict_json_loads(line, f"conjecture identity relation line {line_number}")
        expected_pool_id = f"S5POOL-{line_number:08d}"
        stable_key = occurrence["stable_source_key"]
        if (
            not isinstance(relation, dict)
            or relation.get("schema_version")
            != "awesome-theorems/stage5-conjecture-identity-relation/1.0"
            or relation.get("pool_id") != expected_pool_id
            or relation.get("stable_source_key") != stable_key
            or relation.get("relation_state")
            != "pending_independent_identity_review"
            or relation.get("relation_kind") is not None
            or relation.get("canonical_identity_id") is not None
            or relation.get("evidence_sha256") is not None
            or relation.get("related_stage5_claim_ids") != []
            or relation.get("strict_promotion_authorized") is not False
            or stable_key in seen_stable_keys
        ):
            raise BlueprintError(
                f"invalid conjecture identity-review relation: {expected_pool_id}"
            )
        body = dict(relation)
        authority = body.pop("authority_sha256", None)
        if not isinstance(authority, str) or sha256_bytes(canonical(body)) != authority:
            raise BlueprintError(
                f"conjecture identity-review relation seal drift: {expected_pool_id}"
            )
        seen_stable_keys.add(stable_key)
    return rows


def theorem_cohort(row: dict[str, Any]) -> str:
    evidence = row.get("proof_evidence")
    if isinstance(evidence, dict):
        if evidence.get("formal_proof_state") != "kernel_checked_sorry_free" or evidence.get("uses_sorry") is not False:
            raise BlueprintError(f"unexpected mathlib proof state: {row.get('stage_claim_id')}")
        return "ML-KERNEL"
    formal = row.get("formal_statement")
    if not isinstance(formal, dict):
        raise BlueprintError(f"theorem lacks formal statement: {row.get('stage_claim_id')}")
    axioms = formal.get("axioms", [])
    return "FC-SORRY" if "sorryAx" in axioms else "FC-REPLAY"


def conjecture_cohort(joined: dict[str, Any]) -> str:
    origin = joined["record"].get("origin_release")
    return {"5.0": "FC-STATEMENT", "5.2": "OPENCONJECTURE", "5.5": "V55-RESEARCH"}.get(origin, "")


def conjecture_occurrence_cohort(row: dict[str, Any]) -> str:
    return {"curated": "CB-CURATED", "family": "CB-FAMILY", "catalog": "CB-CATALOG"}.get(str(row.get("kind")), "")


def global_tasks(program: Program) -> list[Task]:
    p = program.task_prefix
    kind_plural = f"{program.kind}s"
    evidence_root = f"Docs/evidence/stage5_{kind_plural}"
    checker_name = f"stage5_{program.kind}_claim"
    controller_name = f"stage5_{kind_plural}_execution_cron_v2"
    return [
        Task(
            f"{p}-BOOT-001",
            "isolated bootstrap preparation, independent validation and canonical-Master acceptance of the execution controller",
            (),
            (
                f"{evidence_root}/workset-5.6.json",
                f"{evidence_root}/workset-5.6-receipt.json",
                f"{evidence_root}/execution-spec.json",
                f"{evidence_root}/foundation-profiles.json",
                f"{evidence_root}/provider-registry.json",
                f"{evidence_root}/claim-card.schema.json",
                f"{evidence_root}/worker-result.schema.json",
                f"{evidence_root}/master-acceptance.schema.json",
                f"scripts/check_{checker_name}.py",
                *( ("scripts/check_stage5_theorem_item.py",) if program.kind == "theorem" else () ),
                f"scripts/test_{checker_name}.py",
                *( ("scripts/test_stage5_theorem_item.py",) if program.kind == "theorem" else () ),
                f"scripts/fixtures/{checker_name}",
                f"Docs/tools/check_stage5_{kind_plural}_blueprint.py",
                f"Docs/tools/generate_stage5_{kind_plural}_gantt.py",
                f"scripts/test_stage5_{kind_plural}_blueprint.py",
                f"scripts/{controller_name}.py",
                f"scripts/test_{controller_name}.py",
                *( (
                    "scripts/stage5_conjecture_handoff_transition.py",
                    "scripts/test_stage5_conjecture_handoff_transition.py",
                ) if program.kind == "conjecture" else () ),
        ),
            f"This is the sole pre-controller BOOT row and is never launched as a worker claim: an external or local bootstrap preparer authenticated by the program-specific pinned trust root reconstructs exactly {program.target_count} frozen execution members, distinguishing release identities from non-credit-bearing source occurrences and requiring retired renumbering aliases only where the member authority actually allocates them; it materializes the schemas/specification, validator, ongoing checker/Gantt generator/controller, then emits a signed `status=self_tested` provisional handoff. This canonical manager's narrow `--accept-boot-handoff` action independently replays the self-tests and atomically advances blank to underscore together with a manager-owned handoff-acceptance receipt binding the pre/post Blueprint/Gantt and complete input snapshot. Two identity-distinct signed reviewers and a distinct signed Master bind that receipt; `--accept-boot-review` then validates exact artifacts and atomically commits x, post-x Gantt and final acceptance receipt. BOOT asserts no Codex TUI, tmux process, thread or `/goal`. Direct blank-to-x is forbidden. Neither action launches workers or installs cron. Only afterward, with explicit operator activation/budget authority, may a Master internal action install the exact marker and separate activation receipt. Until then mathematical rows are unclaimable and this is a scaffold, not an activated controller.",
        )
    ]
def theorem_target_tasks(records: list[dict[str, Any]]) -> tuple[list[Task], dict[str, list[str]]]:
    tasks: list[Task] = []
    cohorts: dict[str, list[str]] = {"FC-SORRY": [], "FC-REPLAY": [], "ML-KERNEL": []}
    for row in sorted(records, key=lambda value: value["stage_claim_id"]):
        target = row["stage_claim_id"]
        number = claim_number(target)
        cohort = theorem_cohort(row)
        cohorts[cohort].append(target)
        dossier = f"Stage5_Theorem_Instances/{target}"
        lean = f"Formalizations/Lean/AwesomeTheorems/Stage5/Theorems/S5_CLM_{number}"
        tasks.append(
            Task(
                f"S5THM-{number}-TARGET",
                f"{target} complete theorem package [{cohort}] — one isolated tmux and one /goal",
                ("S5THM-BOOT-001",),
                (
                    f"{dossier}/intake.json",
                    f"{lean}/Statement.lean",
                    f"{dossier}/statement-crosswalk.json",
                    f"{dossier}/anchor-audit.json",
                    f"{dossier}/proof-units.json",
                    f"{dossier}/process-audit.md",
                    f"{lean}/Proof.lean",
                    f"{dossier}/machine-closure.json",
                    f"{dossier}/machine-checked-audit.md",
                    f"{dossier}/proof-outline.md",
                    f"{dossier}/full-study.md",
                    f"{dossier}/readability-review.json",
                    f"{lean}/Audit.lean",
                    f"{dossier}/build-validation.md",
                    f"{dossier}/receipts/current-validation.json",
                    f"{dossier}/README.md",
                    f"{dossier}/meta.json",
                    f"{dossier}/receipts/release-decision.json",
                ),
                "Exactly one logical TARGET owns this theorem, and it has at most one live worker generation. Every generation owns a fresh task root, task-local tmux server/socket/session, private writable CODEX_HOME, interactive Codex TUI process tree, thread and exactly one submitted /goal; generations never overlap and no generation may inspect another task root or claim another mathematical ID. The current active goal completes the target-local INTAKE, STATEMENT, ANCHOR, TREE, MACHINE, READABLE, VALIDATE and RELEASE sub-checklist. The durable handoff must bind the exact frozen record and retired renumbering alias; the Master-recomputed elaborated root expression and transitive non-foundation constant environment by provider declaration/type/body/source/revision hashes; a bidirectional crosswalk; content-addressed human and machine anchors; a complete typed proof/composition/provenance/trust/readability DAG; exact-root M0-L/W/P Lean closure without placeholders, unsafe injection, claim-specific axioms or unreviewed bodyless oracles; total injective node-to-fragment readable reconstruction with reverse coverage; clean cold from-source offline replay; semantic-substitution mutations; and a strict-dominance certificate over the pinned incomplete THM-M-0387 negative fixture. Local definitions, abbrevs, notation, syntax, macros, coercions, aliases or import substitutions may not shadow or reinterpret source symbols; text-identical theorem headers and self-attested hashes do not establish semantic identity. Distilled output removes duplication, never hypotheses, inference steps, outputs, formal anchors, downstream uses, exceptional cases or trust boundaries. Old phase or generation artifacts are usable only after controller harvest and explicit claim-local rematerialization; workers never read predecessor/sibling task roots directly. The canonical Master, outside the worker tmux, independently validates integrated bytes and alone advances underscore to x; only simultaneous exact semantic binding, M0, R0, empty H/M/R cut sets, current trace and strict dominance permit theorem_complete.",
            )
        )
    return tasks, cohorts


def conjecture_target_tasks(
    rows: list[dict[str, Any]],
    occurrences: list[dict[str, Any]] | None = None,
) -> tuple[list[Task], dict[str, list[str]]]:
    tasks: list[Task] = []
    cohorts: dict[str, list[str]] = {
        "FC-STATEMENT": [], "OPENCONJECTURE": [], "V55-RESEARCH": [],
        "CB-CURATED": [], "CB-FAMILY": [], "CB-CATALOG": [],
    }
    for joined in sorted(rows, key=lambda value: value["record"]["stage_claim_id"]):
        record = joined["record"]
        target = record["stage_claim_id"]
        number = claim_number(target)
        cohort = conjecture_cohort(joined)
        if cohort not in cohorts:
            raise BlueprintError(f"unknown conjecture cohort: {target}")
        cohorts[cohort].append(target)
        dossier = f"Stage5_Conjecture_Instances/{target}"
        lean = f"Formalizations/Lean/AwesomeTheorems/Stage5/Conjectures/S5_CLM_{number}"
        tasks.append(
            Task(
                f"S5CON-{number}-TARGET",
                f"{target} complete conjecture-resolution package [{cohort}] — one isolated tmux and one /goal",
                ("S5CON-BOOT-001",),
                (
                    f"{dossier}/intake.json",
                    f"{lean}/Statement.lean",
                    f"{dossier}/statement-crosswalk.json",
                    f"{dossier}/status-review.json",
                    f"{dossier}/frontier.json",
                    f"{dossier}/frontier.md",
                    f"{dossier}/process-audit.md",
                    f"{lean}/Exploration.lean",
                    f"{dossier}/research/attempt-001.json",
                    f"{dossier}/resolution-proof-units.json",
                    f"{dossier}/resolution-candidate-review.json",
                    f"{dossier}/human-resolution.md",
                    f"{dossier}/human-resolution-reviews.json",
                    f"{lean}/Proof.lean",
                    f"{dossier}/machine-closure.json",
                    f"{dossier}/machine-checked-audit.md",
                    f"{dossier}/resolution-outline.md",
                    f"{dossier}/full-study.md",
                    f"{dossier}/readability-review.json",
                    f"{lean}/Audit.lean",
                    f"{dossier}/build-validation.md",
                    f"{dossier}/receipts/current-validation.json",
                    f"{dossier}/README.md",
                    f"{dossier}/meta.json",
                    f"{dossier}/status-transition.json",
                    f"{dossier}/receipts/release-decision.json",
                ),
                "Exactly one logical TARGET owns this conjecture, and it has at most one live worker generation. Every generation owns a fresh task root, task-local tmux server/socket/session, private writable CODEX_HOME, interactive Codex TUI process tree, thread and exactly one submitted /goal; generations never overlap and no generation may inspect another task root or claim another mathematical ID. The current active goal completes the target-local INTAKE, STATEMENT, STATUS, FRONTIER, EXPLORE, RESOLUTION, HUMAN, LEAN, READABLE, VALIDATE and RELEASE sub-checklist. It must apply the claim-card conjecture proof-search protocol: maintain a durable registry of genuinely distinct mathematical approach families, preserve early independence, require concrete lemmas/constructions/equations/invariants/certificates/counterexamples, mark theorem-equivalent missing-lemma routes blocked, reopen only for a materially new mechanism, and adversarially audit every candidate for hidden hypotheses, polarity mismatch, circularity, equivalent reformulations, unsupported routine steps, invalid transitions and degenerate cases. The durable handoff must bind one sealed strict credit and retired renumbering alias; the exact Claim fingerprint and open baseline; a typed proof/refutation frontier; honestly executed positive-budget exploration; one immutable Claim or Not Claim resolution DAG with empty mapping, human and machine cut sets; a complete human proof or refutation; exact-polarity Lean root closure without placeholders, claim-specific axioms or unreviewed oracles; injective readable reconstruction; cold offline adversarial replay; and a provisional append-only status transition. Finite checks, special cases, reductions, failed routes and polished summaries remain unfinished checkpoints. Old phase or generation artifacts are usable only after controller harvest and explicit claim-local rematerialization; workers never read predecessor/sibling task roots directly. The canonical Master, outside the worker tmux, independently validates integrated bytes and alone advances underscore to x; if the exact claim remains open, TARGET remains unfinished.",
            )
        )
    for row in occurrences or []:
        pool_id = row["pool_id"]
        cohort = conjecture_occurrence_cohort(row)
        if cohort not in cohorts:
            raise BlueprintError(f"unknown conjecture occurrence cohort: {pool_id}")
        cohorts[cohort].append(pool_id)
        dossier = f"Stage5_Conjecture_Pool_Intake/{pool_id}"
        task_id = f"S5CON-POOL-{pool_id.removeprefix('S5POOL-')}-INTAKE"
        source_status = row.get("source_status")
        statement_state = row.get("statement_presence")
        tasks.append(
            Task(
                task_id,
                f"{pool_id} source-occurrence intake/adjudication [{cohort}; source={row['source_native_id']}; status={source_status}] — one isolated tmux and one /goal",
                ("S5CON-BOOT-001",),
                (
                    f"{dossier}/source-binding.json",
                    f"{dossier}/statement-exactification.json",
                    f"{dossier}/status-review.json",
                    f"{dossier}/rights-review.json",
                    f"{dossier}/importance-review.json",
                    f"{dossier}/identity-crosswalk.json",
                    f"{dossier}/adjudication.json",
                    f"{dossier}/process-audit.md",
                    f"{dossier}/README.md",
                    f"{dossier}/receipts/intake-decision.json",
                ),
                "Exactly one source occurrence owns this intake TARGET, and it has at most one live worker generation. Every generation owns a fresh task root, task-local tmux server/socket/session, private writable CODEX_HOME, interactive Codex TUI process tree, thread and exactly one submitted /goal; generations never overlap, no generation may inspect another task root, and no worker may claim another mathematical ID. This row binds the exact ConjectureBench record path/hash, source-native ID, dated source status, statement/pointer shape and rights class. It performs INTAKE, STATEMENT-EXACTIFICATION, STATUS, RIGHTS, IMPORTANCE, FULL-CATALOG-IDENTITY and ADJUDICATION only. The source occurrence is not a strict conjecture credit, does not inherit current-open truth from its source label, has no S5-CLM or retired renumbering alias, and cannot receive proof/refutation completion credit. A valid handoff must produce an independently sourced exact truth-apt Claim or parameterized frontier objective when possible; independently review current status and machine-proof evidence; preserve unanswered, answered, contested, placeholder and pointer states without relabeling; audit rights and attribution; and classify its relation to the existing catalog as exact_existing, equivalent, subsumed, special_case, same_family, new_identity, split_required, pointer_only, status_quarantine or rights_quarantine with concrete evidence. Known related IDs and family membership are leads, never automatic deduplication. If the occurrence is already answered, malformed, duplicate, low-importance, rights-blocked, or not truth-apt, accept that adjudication without creating a proof TARGET. If it is a new high/medium current-open semantic identity, this intake may only emit a promotion proposal for a separately reviewed append-only Stage5/Stage6 migration; it may not allocate IDs or mutate frozen 5.6/6.0. Source lookup, finite checks and polished summaries do not establish identity or status. The canonical Master, outside the worker tmux, independently validates the integrated intake bytes and alone advances underscore to x; intake x means adjudication complete, never conjecture proved/refuted.",
            )
        )
    return tasks, cohorts


def chunks(values: list[str], size: int = 50) -> Iterable[list[str]]:
    for index in range(0, len(values), size):
        yield values[index : index + size]


def terminal_tasks(program: Program, cohorts: dict[str, list[str]]) -> list[Task]:
    tasks: list[Task] = []
    shard_ids: list[str] = []
    cohort_codes = {
        "FC-SORRY": "FCS",
        "FC-REPLAY": "FCR",
        "ML-KERNEL": "MLK",
        "FC-STATEMENT": "FCS",
        "OPENCONJECTURE": "OPC",
        "V55-RESEARCH": "V55",
        "CB-CURATED": "CBC",
        "CB-FAMILY": "CBF",
        "CB-CATALOG": "CBX",
    }
    release_phase = "TARGET"
    for cohort in cohorts:
        values = sorted(cohorts[cohort])
        for ordinal, members in enumerate(chunks(values), start=1):
            shard_id = f"{program.task_prefix}-SHARD-{cohort_codes[cohort]}-{ordinal:03d}"
            shard_ids.append(shard_id)
            dependencies = tuple(
                (
                    f"{program.task_prefix}-POOL-{target.removeprefix('S5POOL-')}-INTAKE"
                    if target.startswith("S5POOL-")
                    else f"{program.task_prefix}-{claim_number(target)}-{release_phase}"
                )
                for target in members
            )
            membership_digest = set_digest(members)
            tasks.append(
                Task(
                    shard_id,
                    f"seal {cohort} release shard {ordinal:03d} ({len(members)} exact members)",
                    dependencies,
                    (f"Docs/evidence/stage5_{program.kind}s/shards/{cohort_codes[cohort]}-{ordinal:03d}.json",),
                    f"An isolated deterministic preparer reconstructs exactly the {len(members)} dependency IDs and member digest {membership_digest} and emits a content-addressed provisional shard. A distinct reviewer verifies every member receipt against current bytes and rejects missing, duplicate, cross-shard or reclassified credit; for CB intake cohorts the shard is JSON adjudication evidence and grants no mathematical/strict credit, while strict cohorts retain proof-resolution semantics. Only the Master integrates and accepts the typed shard.",
                )
            )
    kind_plural = f"{program.kind}s"
    aggregate_id = f"{program.task_prefix}-AGG-001"
    qa_id = f"{program.task_prefix}-QA-001"
    release_id = f"{program.task_prefix}-PROGRAM-RELEASE"
    tasks.extend(
        [
            Task(
                aggregate_id,
                f"serially integrate all accepted Stage5 {kind_plural} into deterministic Lean shard aggregators",
                tuple(shard_ids),
                (
                    f"Formalizations/Lean/AwesomeTheorems/Stage5/{kind_plural.capitalize()}.lean",
                    f"Docs/evidence/stage5_{kind_plural}/aggregate.json",
                ),
                (
                    f"An isolated deterministic preparer generates imports from the exact {program.target_count}-member accepted set, builds every shard/root with the pinned toolchain and emits a content-addressed provisional aggregate. A distinct reviewer proves no worker modified a shared aggregator or imported an unaccepted path; only the Master integrates it and binds declaration/member/body digests, without replacing per-claim evidence."
                    if program.kind == "theorem"
                    else f"An isolated deterministic preparer keeps two typed branches: Lean proof-resolution aggregation for exactly {CONJECTURE_STRICT_TARGET_COUNT} strict identities, and JSON intake-adjudication aggregation for exactly {CONJECTURE_POOL_COUNT} non-credit-bearing occurrences. It never imports intake rows into Lean proof roots or counts adjudication as strict completion. A distinct reviewer verifies both exact ID sets and only the Master binds the branch digests into the shared program aggregate."
                ),
            ),
            Task(
                qa_id,
                f"independently replay the complete {program.target_count}-member {program.kind} debt matrix",
                (aggregate_id,),
                (
                    f"scripts/check_stage5_{kind_plural}_program.py",
                    f"scripts/test_stage5_{kind_plural}_program.py",
                    f"Docs/evidence/stage5_{kind_plural}/program-acceptance.json",
                ),
                f"An independent checker reconstructs all {program.target_count} frozen execution-member IDs and each member-kind-specific completion algebra, receipt and aggregate binding from primary bytes, runs mutation suites and clean cold offline validation profiles where applicable, rejects denominator shrinkage, strict/intake conflation and stale projections, and reports separate ID sets rather than only counts; generator output, green extraction and Gantt state are not self-authentication.",
            ),
            Task(
                release_id,
                f"publish the terminal Stage5 {program.kind} proof-debt program decision",
                (qa_id,),
                (
                    f"Docs/reviews/Stage5_{kind_plural.capitalize()}_Proof_Debt_Final_Review.md",
                    f"Docs/evidence/stage5_{kind_plural}/execution/program-release-acceptance.json",
                ),
                f"An independent terminal preparer may emit a provisional final decision only after every other/ancestor row is accepted, all {program.target_count} member-kind-specific gates close, every durable queue is empty and repository gates pass. For conjectures this means exact proof closure for the strict branch and evidence-complete non-credit adjudication for the occurrence branch, never proof closure for every occurrence. A distinct reviewer binds one transaction ID plus the candidate post-x Blueprint, post-transition full-ID Gantt and prepared acceptance-receipt bytes; only then may the Master journal and atomically commit all three, advance underscore to x with program_complete=true and begin cleanup. Audits, bounded exploration, source assertions, percentages or unpublished drafts cannot satisfy this gate.",
            ),
        ]
    )
    return tasks


@lru_cache(maxsize=2)
def item_mode_records(program: Program) -> list[dict[str, Any]]:
    """Return the closed one-claim-per-checklist-item mode table."""
    p = program.task_prefix
    ordinary_transitions = [
        "not_done->handoff_waiting_master",
        "handoff_waiting_master->master_accepted",
        "handoff_waiting_master->not_done_after_rejection",
        "master_accepted->not_done_after_reviewed_invalidation",
    ]

    def record(
        mode_id: str,
        id_regex: str,
        phase: str,
        producer: str,
        transport: str,
        budget: str,
        *,
        bootstrap: bool = False,
    ) -> dict[str, Any]:
        return {
            "mode_id": mode_id,
            "id_regex": id_regex,
            "phase": phase,
            "producer": producer,
            "provisional_handoff_producer": f"{producer}_must_emit_content_addressed_provisional_handoff",
            "independent_reviewer": "canonical_master_validator_gate_outside_worker_transport",
            "master_acceptor": "canonical_master_only",
            "transport_applicability": transport,
            "execution_class": (
                "pre_controller_external_or_local_signed_principal"
                if bootstrap
                else (
                    "codex_tui_claim"
                    if transport.startswith("required_exactly_one_interactive")
                    else "canonical_master_internal_operation_not_a_worker_claim"
                )
            ),
            "reviewer_transport_applicability": (
                "each BOOT reviewer is an external or local principal authenticated by the program-specific pre-controller trust root; BOOT does not assert a Codex TUI, tmux process, thread, or /goal"
                if bootstrap
                else "no second worker claim, tmux, thread or /goal: independent review is a canonical-Master validator gate over the harvested handoff"
            ),
            "finite_budget_rule": budget,
            "allowed_state_transitions": ordinary_transitions,
            "pre_controller_exception": (
                "program-trust-root-authenticated external/local bootstrap handoff and independent review; no controller, runtime, tmux, process, thread, or Codex goal is claimed"
                if bootstrap
                else None
            ),
        }

    modes = [
        record(
            "BOOT",
            rf"{p}-BOOT-001",
            "BOOT",
            "isolated_bootstrap_preparer",
            "not_applicable_pre_controller_exception",
            "one finite bootstrap transaction with explicit deadline; never renewable",
            bootstrap=True,
        )
    ]
    shard_codes = "(?:FCS|FCR|MLK)" if program.kind == "theorem" else "(?:FCS|OPC|V55|CBC|CBF|CBX)"
    modes.append(
        record(
            "TARGET",
            rf"{p}-[0-9]{{8}}-TARGET",
            "TARGET",
            f"one_{program.kind}_one_goal_complete_package_worker",
            "required_exactly_one_interactive_task_local_tmux_codex_tui_goal",
            "one positive finite budget per generation; a healthy active goal may continue, but a terminal or fenced generation is fully retired before a fresh task root/thread/goal is admitted and generations never overlap",
        )
    )
    if program.kind == "conjecture":
        modes.append(
            record(
                "POOL-INTAKE",
                rf"{p}-POOL-[0-9]{{8}}-INTAKE",
                "POOL-INTAKE",
                "one_source_occurrence_one_goal_intake_adjudication_worker",
                "required_exactly_one_interactive_task_local_tmux_codex_tui_goal",
                "one positive finite budget per generation; adjudication completion grants no proof or strict credit and a terminal or fenced generation is fully retired before replacement",
            )
        )
    modes.extend(
        [
            record(
                "SHARD",
                rf"{p}-SHARD-{shard_codes}-[0-9]{{3}}",
                "SHARD",
                "isolated_deterministic_shard_preparer",
                "required_exactly_one_interactive_task_local_tmux_codex_tui_goal",
                "one positive finite deterministic shard-preparation claim; Master validation opens no reviewer worker",
            ),
            record(
                "AGG",
                rf"{p}-AGG-001",
                "AGG",
                "isolated_deterministic_aggregate_preparer",
                "required_exactly_one_interactive_task_local_tmux_codex_tui_goal",
                "one positive finite deterministic aggregate-preparation claim; Master validation opens no reviewer worker",
            ),
            record(
                "QA",
                rf"{p}-QA-001",
                "QA",
                "independent_full_program_validator",
                "required_exactly_one_interactive_task_local_tmux_codex_tui_goal",
                "one positive finite full-denominator validation claim; Master acceptance opens no reviewer worker",
            ),
            record(
                "PROGRAM-RELEASE",
                rf"{p}-PROGRAM-RELEASE",
                "PROGRAM-RELEASE",
                "independent_terminal_decision_preparer",
                "required_exactly_one_interactive_task_local_tmux_codex_tui_goal",
                "one positive finite terminal preparation claim before the Master three-output acceptance transaction",
            ),
        ]
    )
    return modes


def validate_item_mode_coverage(program: Program, tasks: list[Task]) -> None:
    modes = item_mode_records(program)
    mode_ids = [mode["mode_id"] for mode in modes]
    if len(mode_ids) != len(set(mode_ids)):
        raise BlueprintError(f"{program.kind}: duplicate item-mode IDs")
    for task in tasks:
        matches = [mode["mode_id"] for mode in modes if re.fullmatch(mode["id_regex"], task.item_id)]
        if len(matches) != 1:
            raise BlueprintError(
                f"{program.kind}: task {task.item_id} has {len(matches)} exact item modes {matches}"
            )


def expected_tasks(program: Program) -> list[Task]:
    tasks = global_tasks(program)
    if program.kind == "theorem":
        target_tasks, cohorts = theorem_target_tasks(theorem_inventory())
    else:
        target_tasks, cohorts = conjecture_target_tasks(
            strict_inventory(), conjecture_occurrence_inventory()
        )
    tasks.extend(target_tasks)
    tasks.extend(terminal_tasks(program, cohorts))
    validate_task_set(program, tasks, expected_initial=True)
    return tasks


def validate_task_set(program: Program, tasks: list[Task], *, expected_initial: bool = False, allow_legacy_execution_gate: bool = False) -> None:
    ids = [task.item_id for task in tasks]
    if len(ids) != len(set(ids)):
        raise BlueprintError(f"{program.kind}: duplicate task IDs")
    by_id = {task.item_id: task for task in tasks}
    target_re = re.compile(
        rf"^(?:{program.task_prefix}-[0-9]{{8}}-TARGET|"
        rf"{program.task_prefix}-POOL-[0-9]{{8}}-INTAKE)$"
    )
    targets = [task for task in tasks if target_re.fullmatch(task.item_id)]
    canonical_blueprint = program.version in {
        "stage5-theorem-proof-debt/2.0",
        "stage5-conjecture-proof-debt/2.0",
    }
    if (targets or canonical_blueprint) and len(targets) != program.target_count:
        raise BlueprintError(
            f"{program.kind}: expected exactly {program.target_count} execution-member rows, found {len(targets)}"
        )
    if program.kind == "conjecture" and canonical_blueprint:
        strict_ids = [
            task.item_id
            for task in tasks
            if re.fullmatch(r"S5CON-[0-9]{8}-TARGET", task.item_id)
        ]
        intake_ids = [
            task.item_id
            for task in tasks
            if re.fullmatch(r"S5CON-POOL-[0-9]{8}-INTAKE", task.item_id)
        ]
        expected_strict = [
            f"S5CON-{claim_number(entry['record']['stage_claim_id'])}-TARGET"
            for entry in strict_inventory()
        ]
        expected_intake = [
            f"S5CON-POOL-{index:08d}-INTAKE"
            for index in range(1, CONJECTURE_POOL_COUNT + 1)
        ]
        if strict_ids != expected_strict:
            raise BlueprintError(
                "conjecture: strict TARGET identity/order set differs from the sealed strict ledger"
            )
        if intake_ids != expected_intake:
            raise BlueprintError(
                "conjecture: occurrence INTAKE identity/order set differs from the sealed pool"
            )
    boot_id = f"{program.task_prefix}-BOOT-001"
    if canonical_blueprint:
        for target in targets:
            if target.dependencies != (boot_id,):
                raise BlueprintError(f"{target.item_id}: execution-member row must depend only on {boot_id}")
            required_gate_fragments = (
                "task-local tmux server/socket/session",
                "exactly one submitted /goal",
                "no generation may inspect another task root",
            )
            if program.kind == "theorem":
                required_gate_fragments += (
                    "transitive non-foundation constant environment",
                    "semantic-substitution mutations",
                    "strict-dominance certificate",
                    "Distilled output removes duplication",
                )
            if not allow_legacy_execution_gate and any(fragment not in target.gate for fragment in required_gate_fragments):
                raise BlueprintError(f"{target.item_id}: one-object/one-worker gate is incomplete")
    for task in tasks:
        if task.state not in {" ", "_", "x"}:
            raise BlueprintError(f"{task.item_id}: invalid state")
        if len(task.gate) < 80:
            raise BlueprintError(f"{task.item_id}: gate is too weak")
        for path in task.owned_paths:
            validate_repo_path(path, task.item_id)
        for dep in task.dependencies:
            if dep not in by_id or dep == task.item_id:
                raise BlueprintError(f"{task.item_id}: bad dependency {dep}")
        if task.state in {"_", "x"}:
            blockers = [dep for dep in task.dependencies if by_id[dep].state != "x"]
            if blockers:
                raise BlueprintError(f"{task.item_id}: advanced before dependencies {blockers[:5]}")
    paths: list[tuple[str, str]] = [
        (path, task.item_id) for task in tasks for path in task.owned_paths
    ]
    seen: dict[str, str] = {}
    for path, owner in paths:
        if path in seen:
            raise BlueprintError(f"owned path {path} has owners {seen[path]} and {owner}")
        seen[path] = owner
    for path in seen:
        parent = PurePosixPath(path).parent
        while parent != PurePosixPath("."):
            ancestor = parent.as_posix()
            if ancestor in seen:
                raise BlueprintError(f"owned-path prefix overlap: {ancestor} vs {path}")
            parent = parent.parent
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(item_id: str) -> None:
        if item_id in visiting:
            raise BlueprintError(f"dependency cycle at {item_id}")
        if item_id in visited:
            return
        visiting.add(item_id)
        for dep in by_id[item_id].dependencies:
            visit(dep)
        visiting.remove(item_id)
        visited.add(item_id)

    for item_id in ids:
        visit(item_id)
    release_id = f"{program.task_prefix}-PROGRAM-RELEASE"
    if release_id not in by_id:
        raise BlueprintError(f"{program.kind}: missing terminal release")
    ancestors: set[str] = set()

    def collect(item_id: str) -> None:
        for dep in by_id[item_id].dependencies:
            if dep not in ancestors:
                ancestors.add(dep)
                collect(dep)

    collect(release_id)
    if ancestors != set(ids) - {release_id}:
        missing = sorted(set(ids) - {release_id} - ancestors)
        raise BlueprintError(f"terminal release does not cover all tasks: {missing[:5]}")
    validate_item_mode_coverage(program, tasks)
    if expected_initial and any(task.state != " " for task in tasks):
        raise BlueprintError("bootstrap tasks must all start not-done")


def validate_cross_program_ownership(
    program_tasks: Iterable[tuple[Program, list[Task]]],
) -> None:
    owners: dict[str, str] = {}
    for program, tasks in program_tasks:
        for task in tasks:
            for path in task.owned_paths:
                owner = f"{program.kind}:{task.item_id}"
                if path in owners:
                    raise BlueprintError(
                        f"cross-program owned path {path} has owners {owners[path]} and {owner}"
                    )
                owners[path] = owner
    for path, owner in owners.items():
        parent = PurePosixPath(path).parent
        while parent != PurePosixPath("."):
            ancestor = parent.as_posix()
            if ancestor in owners:
                raise BlueprintError(
                    f"cross-program owned-path prefix overlap: {owners[ancestor]}:{ancestor} "
                    f"vs {owner}:{path}"
                )
            parent = parent.parent


def task_authority_sha256(task: Task) -> str:
    return sha256_bytes(
        canonical(
            {
                "item_id": task.item_id,
                "title": task.title,
                "dependencies": list(task.dependencies),
                "owned_paths": list(task.owned_paths),
                "gate": task.gate,
            }
        )
    )


def validate_state_evidence(
    program: Program,
    tasks: list[Task],
    *,
    allow_boot_transition: bool = False,
    allow_progress_cursor: bool = False,
) -> None:
    # A reviewed authority migration may need to rebind an already-running
    # cursor.  It still validates the complete immutable row/DAG contract;
    # this flag only permits reading the existing checkbox progress while the
    # migration transaction preserves every state byte-for-byte.
    if allow_progress_cursor:
        return
    advanced = [task.item_id for task in tasks if task.state != " "]
    boot_id = f"{program.task_prefix}-BOOT-001"
    if allow_boot_transition and (
        not advanced
        or advanced == [boot_id]
        and next(task for task in tasks if task.item_id == boot_id).state in {"_", "x"}
    ):
        return
    if advanced:
        raise BlueprintError(
            f"{program.kind}: bootstrap validator accepts only the pristine all-blank cursor; "
            "this canonical manager's narrow digest-bound BOOT acceptance actions alone perform BOOT blank-to-underscore-to-x, "
            "and the accepted BOOT-produced ongoing checker handles every later non-BOOT transition "
            f"(first advanced ID: {advanced[0]})"
        )


def marker_binding(label: str, begin: str, end: str) -> dict[str, Any]:
    begin_split = len(begin) // 2
    end_split = len(end) // 2
    return {
        "label": label,
        "begin_fragments": [begin[:begin_split], begin[begin_split:]],
        "end_fragments": [end[:end_split], end[end_split:]],
        "begin_sha256": sha256_bytes(begin.encode("utf-8")),
        "end_sha256": sha256_bytes(end.encode("utf-8")),
        "ordered_pair_sha256": sha256_bytes(canonical([begin, end])),
        "reconstruction": "concatenate each UTF-8 fragment array without a separator and verify its SHA-256",
    }


def program_coordination_authority(program: Program) -> dict[str, Any]:
    """Return coordination owned by one program, never by both programs."""
    root = runtime_execution_root(program)
    return {
        "schema_version": "awesome-theorems/stage5-program-coordinator/1.0",
        "program": program.version,
        "root": root,
        "isolation": "program-local; no theorem/conjecture shared coordinator, lease, ledger, or capacity pool",
        "lease_paths": {
            "admission": f"{root}/locks/admission.lock",
            "canonical_checkout_integration": f"{root}/locks/canonical-checkout-integration.lock",
            "operator_budget": f"{root}/locks/operator-budget.lock",
            "cleanup": f"{root}/locks/cleanup.lock",
            "exact_path_namespace": f"{root}/locks/owned-paths/<sha256-of-canonical-exact-path>.lock",
            "validator_namespace": f"{root}/locks/validators/validator-<slot>.lock",
        },
        "concurrency_prompt_contract": concurrency_prompt_contract(program),
        "operator_budget_authority_path": "Docs/evidence/stage5_shared_execution/operator-budget-v1.json",
        "cleanup_protocol": "program-local-v1",
    }


def runtime_execution_root(program: Program) -> str:
    """Return the current epoch namespace, leaving predecessor runtime intact."""

    return (
        f"{program.runtime_root}/epochs/{CONJECTURE_RUNTIME_AUTHORITY_EPOCH}"
        if program.kind == "conjecture"
        else program.runtime_root
    )


def conjecture_proof_search_prompt_contract() -> dict[str, Any]:
    """Return the Stage5-compatible core extracted from the pinned prompt.

    The upstream prompt used many agents.  Stage5 deliberately imports only
    its proof-search governance and executes it inside one long-lived TARGET
    goal, preserving the repository's no-child-agent accounting boundary.
    """
    return {
        "schema_version": "awesome-theorems/stage5-conjecture-proof-search-prompt/1.0",
        "source": {
            "repository": CROUZEIX_PROMPT_REPOSITORY,
            "commit": CROUZEIX_PROMPT_COMMIT,
            "blob_sha1": CROUZEIX_PROMPT_BLOB_SHA1,
            "file": "crouzeix_conjecture_prompt.txt",
            "file_sha256": CROUZEIX_PROMPT_SHA256,
            "extraction_path": CROUZEIX_PROMPT_EXTRACTION.relative_to(ROOT).as_posix(),
            "extraction_sha256": CROUZEIX_PROMPT_EXTRACTION_SHA256,
            "evidence_scope": "proof-search workflow input only; never mathematical correctness or completion evidence",
        },
        "execution_adaptation": {
            "worker_topology": "one TARGET, one current generation, one thread, one authenticated long-lived /goal",
            "upstream_multiagent_shape": "not imported",
            "route_parallelism": "conceptual approach families developed serially and independently inside the same goal",
            "child_agents": "forbidden",
            "collaboration_tools": "forbidden",
            "hidden_concurrency": "forbidden",
        },
        "resolution_roots": ["Claim", "Not Claim"],
        "approach_registry": {
            "required": True,
            "group_by": "mathematical mechanism, never superficial wording",
            "minimum_fields": [
                "family_id", "mechanism", "assumptions", "concrete_results",
                "exact_gap", "equivalence_to_root_risk", "state", "reopen_condition",
            ],
            "state_enum": ["live", "blocked", "refuted", "merged"],
            "durable_surfaces": [
                "frontier.json", "research/attempt-001.json", "process-audit.md",
                "resolution-proof-units.json", "resolution-candidate-review.json",
            ],
        },
        "search_loop": [
            "start with genuinely distinct formulations, invariants, reductions, algebraic/analytic/geometric/extremal/inductive mechanisms and falsification checks",
            "develop early families independently so a favored route does not collapse the portfolio",
            "require concrete lemmas, constructions, equations, invariants, certificates or counterexamples from every round",
            "synthesize mature families, adversarially challenge the strongest candidate, redirect effort and start a fresh round",
            "cross-pollinate only after independent routes expose their actual strengths and exact gaps",
        ],
        "blocked_route_policy": "an unproved missing lemma comparable in strength to the exact root is blocked, not near-complete; reopen only for a materially new mechanism, invariant or construction attacking that exact gap",
        "adversarial_audit": [
            "hidden hypotheses", "polarity mismatch", "circularity",
            "equivalent reformulation presented as progress", "unsupported routine step",
            "invalid sign/domain/limit/case transition", "degenerate and boundary cases",
            "human-to-Lean formalizability and trust boundary",
        ],
        "nonclosure_evidence": [
            "finite computation", "special case", "weakened claim", "added hypothesis",
            "reduction to an unproved theorem-strength lemma", "uncertified candidate counterexample",
            "failed search", "vague status report", "optimism", "polished summary",
        ],
        "completion_rule": "only a standalone exact-polarity human proof/refutation, adversarial audit, exact Lean root and all declared trust/validation gates may support closure",
        "unfinished_rule": "preserve the strongest rigorous frontier, failed-route certificates and exact remaining gap; keep the TARGET unresolved and never represent partial progress as completion",
        "short_goal_clause": "Apply the claim card's conjecture proof-search protocol: maintain a diverse approach-family registry, reject theorem-equivalent gaps, adversarially audit concrete candidates, and never claim closure without exact-polarity human and Lean completion.",
    }


def spec_object(program: Program) -> dict[str, Any]:
    validate_canonical_root()
    kind_plural = f"{program.kind}s"
    service_tier = frozen_codex_service_tier(program)
    operator_thread_id, operator_objective_sha256, operator_trust_root_sha256 = (
        operator_goal_binding(program)
    )
    program_authority = program_coordination_authority(program)
    controller_name = f"stage5_{kind_plural}_execution_cron_v2"
    execution_root = runtime_execution_root(program)
    (
        boot_handoff_relative,
        boot_handoff_acceptance_relative,
        boot_review_relative,
        boot_acceptance_relative,
    ) = boot_receipt_contract_paths(program)
    cron_command = (
        f"*/2 * * * * cd {CANONICAL_ROOT.as_posix()} && /usr/bin/python3 "
        f"{CANONICAL_ROOT.as_posix()}/scripts/{controller_name}.py --tick --concurrency-prompt "
        f"{CANONICAL_ROOT.as_posix()}/{concurrency_prompt_path(program)} >> "
        f"{CANONICAL_ROOT.as_posix()}/{execution_root}/logs/cron.log 2>&1"
    )
    specification = {
        "schema_version": "awesome-theorems/stage5-proof-debt-execution-spec/2.0",
        "program": program.version,
        "blueprint_schema": program.schema,
        "canonical_repository_root": CANONICAL_ROOT.as_posix(),
        "canonical_root_authority_sha256": CANONICAL_ROOT_AUTHORITY_SHA256,
        "root_relocation_policy": ROOT_RELOCATION_POLICY,
        "source_bundle": {
            "bindings": source_bundle_object(program),
            "sha256": source_bundle_sha256(program),
        },
        "authoritative_blueprint": program.blueprint.relative_to(ROOT).as_posix(),
        "gantt_projection": program.gantt.relative_to(ROOT).as_posix(),
        "checklist_parser": {
            "bootstrap_tool": "Docs/tools/manage_stage5_proof_debt_blueprints.py",
            "marker_binding": marker_binding("checklist", CHECKLIST_BEGIN, CHECKLIST_END),
            "row_grammar": "- [STATE] `ITEM-ID` title | depends_on=ID,ID-or-- | owned_paths=path,path-or-- | gate=verifiable clause",
            "states": ["not_done", "handoff_waiting_master", "master_accepted"],
            "stable_id_policy": "strict identities use exactly one immutable S5THM/S5CON-<8-digit-id>-TARGET row; non-credit-bearing conjecture occurrences use exactly one S5CON-POOL-<8-digit-pool-ordinal>-INTAKE row; internal phases never become worker claims or checklist rows",
            "bootstrap_boundary": "ordinary parse/check recognizes only the fixed pristine all-blank template; this manager's --accept-boot-handoff and --accept-boot-review are the sole narrow exceptions and perform only BOOT blank-to-underscore-to-x, after which the accepted ongoing checker/controller is mandatory for every non-BOOT transition or extension",
        },
        "bootstrap_acceptor": {
            "authority_path": "Docs/tools/manage_stage5_proof_debt_blueprints.py",
            "authority_sha256": manager_code_sha256(),
            "actions": ["--accept-boot-handoff", "--accept-boot-review"],
            "scope": "the only pre-controller state authority; accepts exactly one program (never --kind all), only the fixed BOOT-001 row, and never launches a worker or installs cron",
            "control_receipts": {
                "handoff": boot_handoff_relative,
                "handoff_acceptance": boot_handoff_acceptance_relative,
                "review": boot_review_relative,
                "acceptance": boot_acceptance_relative,
                "ownership": "handoff/review are immutable signed external inputs; the canonical manager owns both transition receipts, and atomically publishes handoff-acceptance with underscore and final acceptance with x",
            },
            "role_authentication": {
                "schema_version": BOOT_ROLE_SCHEMA,
                "trust_root": f"Docs/evidence/stage5_{kind_plural}/{BOOT_ROLE_TRUST_ROOT_NAME}",
                "trust_root_sha256": BOOT_ROLE_TRUST_ROOT_SHA256.get(program.kind),
                "trust_boundary": "external pre-controller TCB input, program-specific and pinned by reviewed manager bytes; null blocks BOOT until a reviewed manager/specification migration pins the exact digest",
                "signature_algorithm": "Ed25519",
                "producer": "external or local signed principal binding program/item/claim/run and exact manager/source/spec authority; no controller or TUI identity is asserted",
                "reviewers": "exactly two independently signed external/local decisions in principal-scoped immutable archives; neither path/digest/inode/principal/claim/run may be reused",
                "master": "a fourth external/local signed principal that authorizes review against the manager-owned handoff-acceptance receipt",
                "fail_closed": "a null/missing/malformed/untrusted signature, role/key/program/authority mismatch, receipt replay, or identity collision rejects before candidate commands execute",
            },
            "canonical_command_contract": {
                "python": CANONICAL_PYTHON.as_posix(),
                "crontab": CANONICAL_CRONTAB.as_posix(),
                "environment": BOOT_COMMAND_ENV,
                "commands": boot_command_spec(program),
                "mutation_boundary": "all source/manager/artifact/handoff/trust/review/decision bytes use the original CAS guards; commands are followed by complete rehash and a final precommit replay",
            },
            "handoff_transition": {
                "from": "not_done",
                "to": "handoff_waiting_master",
                "input": boot_handoff_relative,
                "requirements": "signed closed schema has status=self_tested and binds current blank Blueprint/Gantt, manager/spec/source/task digests, external/local producer, expected self-test result digest and every BOOT artifact; the manager independently replays self-tests and every file/tree is rehashed while cron/runtime/review/acceptance remain absent",
                "transaction": "compare-and-swap and rollback-safe atomic Blueprint, post-underscore Gantt and manager-owned handoff-acceptance receipt binding pre/post digests, replay results and complete input snapshot",
            },
            "review_transition": {
                "from": "handoff_waiting_master",
                "to": "master_accepted",
                "input": boot_review_relative,
                "output": boot_acceptance_relative,
                "requirements": "two identity-distinct passing reviewers, each distinct from producer and named Master, bind the exact manager-owned handoff-acceptance authority, artifact/controller/checker/test digests and every mandatory gate",
                "transaction": "precompute post-x Blueprint/Gantt and sealed acceptance receipt, then compare-and-swap all three through one rollback-safe manifest",
            },
            "recovery": "same repository-wide lock, source/artifact CAS guards, old/new digests, fsync journal and deterministic rollback/idempotent completion used by bootstrap output transactions",
            "postcondition": "BOOT=x still does not activate cron; the separately specified operator-authorized activation transaction may run afterward",
        },
        "runtime_root": program.runtime_root,
        "shared_runtime_root": None,
        "coordination_authority": program_authority,
        "task_root_shape": f"{execution_root}/tasks/<claim-id>/<run-id>",
        "mathematical_object_worker_protocol": {
            "bijection": f"one frozen {program.kind} execution-member ID equals one TARGET checklist item equals one claim identity equals one task-local tmux server/socket/session equals one private CODEX_HOME equals one Codex process tree equals one thread equals one active /goal",
            "claim_id_grammar": "<item-id>--worker; strict proof-resolution IDs end in -TARGET and source-occurrence adjudication IDs match S5CON-POOL-<8-digit>-INTAKE",
            "claim_identity": "<item-id>--worker/<run-id>",
            "task_root_shape": f"{execution_root}/tasks/<item-id>--worker/<run-id>",
            "lifetime": "the stable TARGET owns the complete mathematical object; exactly one fresh generation at a time works from intake through proof or refutation, readable reconstruction, validation and provisional release handoff",
            "generation_bijection": "one admitted generation equals one fresh task root equals one task-local tmux server/socket/session equals one private CODEX_HOME equals one process tree equals one thread equals exactly one submitted /goal",
            "generation_replacement": "a healthy active goal may continue under the same accounted caps; after terminal result, explicit stop, boundary violation or liveness failure, the old generation is fenced and stopped before a fresh run ID/root/home/thread/goal is admitted, with zero overlap",
            "internal_subchecklist": (
                ["INTAKE", "STATEMENT", "ANCHOR", "TREE", "MACHINE", "READABLE", "VALIDATE", "RELEASE"]
                if program.kind == "theorem"
                else ["INTAKE", "STATEMENT", "STATUS", "FRONTIER", "EXPLORE", "RESOLUTION", "HUMAN", "LEAN", "READABLE", "VALIDATE", "RELEASE"]
            ),
            "internal_progress": "target-local evidence only; internal stages are never scheduler claims, Blueprint rows, dependencies, tmux sessions, threads or goals",
            "no_second_id": "a TARGET worker may not claim, edit or opportunistically complete any second mathematical or source-occurrence ID",
            "repair": "continue only while the exact generation and active goal remain healthy and accounted; otherwise retire it completely and use one fresh nonoverlapping generation with one new /goal, never a second simultaneous worker for the object",
            "cross_task_access": "a generation may access only its own task root and individually materialized bootstrap inputs; any command, tool call, read or write naming a predecessor, sibling or other-program task root invalidates the generation and forbids harvest",
            "review": "independent validation is performed by the canonical Master/validator over the harvested immutable handoff and opens no reviewer worker, tmux, thread or /goal",
            "migration": "legacy phase handoffs may be copied only as target-local evidence; no legacy phase state alone advances TARGET",
            "master": "the canonical Master validates integrated bytes and alone advances underscore to x",
            "gantt_projection": "one monitoring row per TARGET with exactly one claim/run/owner/startup/live/running/handoff identity",
        },
        "theorem_acceptance_contract": (
            {
                "fixture_role": "THM-M-0387 is a pinned incomplete H1/M2/R0 negative fixture and minimum evidence shape, never a positive completion precedent",
                "strict_dominance": "every release passes all applicable fixture-shape predicates and strictly adds Master-recomputed semantic-environment identity plus semantic-substitution and cold-from-source replay evidence",
                "semantic_identity": "bind the elaborated root expression and every transitive non-foundation constant to pinned provider declaration/type/body/source/revision hashes; reject local definition, abbrev, notation, syntax, macro, coercion, namespace alias and import substitution shadowing",
                "machine_completion": "exact root M0-L/W/P, complete root-relevant proof/composition DAG, per-declaration type/body/dependency/axiom evidence, empty machine cut set and trust=0 cold offline replay",
                "readable_completion": "R0 means a total injective required-node-to-exact-fragment map and reverse ledger, independent conflict-checked review and empty readability cut set",
                "trace": "content-addressed frozen source, semantic environment, proof DAG, Lean object/read trace, mutation outcomes, readability decisions and canonical-Master release receipt; any authority change invalidates affected receipts",
                "distilled": "store generated inventories in structured evidence and eliminate prose duplication while retaining every hypothesis, inference, output, formal anchor, downstream use, exceptional case and trust boundary",
                "release_conjunction": "exact semantic binding and M0 and R0 and empty H/M/R cut sets and current trace and strict dominance; no proxy or self-attestation",
            }
            if program.kind == "theorem" else None
        ),
        "provisional_handoff_queue": f"{execution_root}/handoffs",
        "immutable_handoff_archive": f"Docs/evidence/stage5_{kind_plural}/execution/handoffs/<claim-id>/<baseline-sha256>/<patch-sha256>",
        "immutable_acceptance_archive": f"Docs/evidence/stage5_{kind_plural}/execution/acceptances/<item-id>/<baseline-sha256>/<integrated-tree-sha256>/<decision-sha256>.json",
        "nonacceptance_discovery_archive": f"Docs/evidence/stage5_{kind_plural}/execution/discoveries/<item-id>/<baseline-sha256>/<discovery-sha256>.json",
        "nonacceptance_discovery_rule": "a failed/self-tested closure or RESOLUTION attempt may emit a typed cut discovery without advancing blank to underscore: the controller harvests it, a distinct reviewer validates exact fingerprint/version/cut-family/node/type/evidence digests, and the Master only seals the content-addressed discovery receipt. It is explicitly nonacceptance evidence and grants no checkbox or math credit",
        "acceptance_archive_rule": "before any underscore-to-x write, the Master computes and digest-seals a receipt containing independent-review identities, handoff, baseline, integrated tree, task authority, validation outputs, decision and transition digests. Ordinary transitions publish that immutable receipt before x; PROGRAM-RELEASE stages its receipt in the same recovery manifest and atomically publishes it with the two post-x projections. Runtime ledgers reference exact path/SHA and cleanup preserves the archive",
        "integration_queue": f"{execution_root}/integration",
        "repair_queue": f"{execution_root}/repair",
        "checkpoint_queue": f"{execution_root}/checkpoints",
        "claim_ledger": f"{execution_root}/ledgers/claims.jsonl",
        "transition_ledger": f"{execution_root}/ledgers/transitions.jsonl",
        "admission_ledger": f"{execution_root}/ledgers/admission.jsonl",
        "durable_state": {
            "schema_version": "awesome-theorems/stage5-controller-durable-state/1.0",
            "record_contract": "each JSONL record has schema/version, program, monotone sequence, event ID/type, claim/run/item identities where applicable, RFC3339 instant, previous_record_sha256, canonical_record_sha256 and event-specific closed payload; duplicate sequence/event IDs or broken hash chain fail closed",
            "ledgers": {
                "claims": f"{execution_root}/ledgers/claims.jsonl",
                "launch_attempts": f"{execution_root}/ledgers/launch-attempts.jsonl",
                "harvested_handoffs": f"{execution_root}/ledgers/harvested-handoffs.jsonl",
                "integration_repair": f"{execution_root}/ledgers/integration-repair.jsonl",
                "released_claims_retired_processes": f"{execution_root}/ledgers/released-retired.jsonl",
                "route_decisions": f"{execution_root}/ledgers/route-decisions.jsonl",
                "admission_decisions": f"{execution_root}/ledgers/admission.jsonl",
                "state_transitions": f"{execution_root}/ledgers/transitions.jsonl",
                "scheduler_cursor": f"{execution_root}/ledgers/scheduler-cursor.jsonl",
                "cleanup": f"{execution_root}/ledgers/cleanup.jsonl",
            },
            "launch_recovery": "reservation/materialization/tmux/goal-pasted/goal-submitted/live events bind the task-local tmux pane PID/start time, socket/session, cwd, private CODEX_HOME, sole thread, sole active goal, completion token and claim-card hashes; restart authenticates and resumes or retires the exact attempt before any relaunch, so goal_submitted can never produce a duplicate /goal",
            "release_recovery": "harvest is durable before liveness prune; release binds retired tmux/PID descendants and immutable archive SHA; integration/repair cursor resumes only the exact item/baseline/handoff",
            "cleanup_recovery": "records preconditions, harvested/dispositioned queues, exact marker/process/socket/lock targets, each removal and post-cadence absence proof; restart is idempotent and never broad-kills",
            "boot_schemas": f"Docs/evidence/stage5_{kind_plural}/execution-spec.json defines closed event schemas; BOOT mutation tests cover truncation, duplicate/reorder, hash-chain break and crashes at every launch/harvest/integrate/release/cleanup event",
        },
        "scheduler_lock": f"{execution_root}/locks/scheduler.lock",
        "runtime_snapshot": f"{execution_root}/status/runtime-snapshot.json",
        "runtime_authority_epoch": (
            CONJECTURE_RUNTIME_AUTHORITY_EPOCH if program.kind == "conjecture" else None
        ),
        "status_surface": program.gantt.relative_to(ROOT).as_posix(),
        "worker_platform": "codex",
        "item_modes": item_mode_records(program),
        "worker_transport": "tmux_codex_tui",
        "goal_command": "/goal",
        "worker_lifecycle_mode": "lane_pool_bounded_generation",
        "worker_lifecycle_rule": "a lane is a durable logical capacity slot; each admitted generation has one fresh task root, private tmux server/socket/session, private CODEX_HOME, thread and /goal; terminal completion retires the generation, then the lane may be reused only after harvest and fencing",
        "process_isolation": "one_task_local_tmux_and_one_interactive_codex_process_tree_per_claim",
        "state_isolation": "one_private_writable_CODEX_HOME_per_claim",
        "worker_runtime_boundary": {
            "transport": "host interactive Codex TUI launched directly by task-local tmux",
            "tmux_topology": "one private tmux server/socket/session per claim; never multiple mathematical objects in windows or panes of one server",
            "cwd": "exact isolated task-local work root",
            "codex_home": "exact private writable task-local CODEX_HOME",
            "worker_container_transport": "forbidden",
            "task_root_access": "only the exact current task root plus individually declared materialized inputs; predecessor, sibling and other-program task roots are forbidden even read-only",
            "liveness": "authenticate tmux socket/session, pane PID/start time, process tree, cwd, private CODEX_HOME, exactly one private thread, exactly one active goal, frozen route and a clean current-session foreign-task-root audit",
        },
        "nested_agent_policy": {
            "enabled": program.kind == "theorem",
            "operator_authority": "the active theorem execution goal explicitly allows subagents",
            "capacity_rule": "every child independently consumes one agent execution, live transport, authenticated goal, running turn, outbound request, in-flight request and outstanding-request slot under the same prompt ceiling; parent plus children never exceed 24",
            "transport_rule": "every admitted child generation must use its own task-local tmux server/socket/session, private CODEX_HOME, interactive Codex TUI process, thread and exactly one submitted /goal; in-process or hidden child threads are forbidden",
            "identity_rule": "a child receives a distinct claim/run/execution identity and terminal result; it never claims a second mathematical TARGET or bypasses ownership",
            "disabled_feature_boundary": "Codex in-process multi-agent feature flags remain disabled because they cannot provide the independent tmux/request accounting required here; subagents are admitted only by the controller as first-class executions",
        },
        "forbidden_transports": [
            "codex_app_server",
            "app_server_json_rpc",
            "codex_exec",
            "shared_codex_daemon",
            "shared_tmux_server",
            "shared_writable_CODEX_HOME",
            "no_tmux_codex",
            "docker_worker_transport",
            "container_worker_transport",
        ],
        "route_policy": {
            "provider": "sub2api",
            "model": frozen_codex_model(program),
            "reasoning_effort": FROZEN_CODEX_REASONING_EFFORT,
            "service_tier": service_tier,
            "rule": "pass all three values explicitly to every interactive Codex TUI and authenticate the identical resolved route in the task-local registry before counting the claim live; installed defaults and silent substitution are forbidden",
        },
        "foundation_axiom_policy": {
            "schema_version": "awesome-theorems/stage5-foundation-profile/1.0",
            "registry": f"Docs/evidence/stage5_{kind_plural}/foundation-profiles.json",
            "profile_key": "<stage-claim-id>@<positive-profile-version>",
            "initial_authority": "BOOT-produced registry accepted by a reviewer independent of the profile authors and canonical Master",
            "required_closed_fields": [
                "stage_claim_id",
                "profile_version",
                "lean_toolchain_sha256",
                "provider_registry_sha256",
                "allowed_transitive_axiom_names",
                "allowed_bodyless_foundation_declarations",
                "per_name_justifications",
                "profile_authority_sha256",
            ],
            "per_claim_rule": "the observed transitive axiom set must equal the exact accepted set recorded by the target's reviewed versioned profile; no name is inherited from M0387 or a global folklore allowlist",
            "bodyless_exception": "only exact declarations individually named and justified in that target profile; no target proposition, mathematical fact, generated certificate oracle or claim-specific axiom is eligible",
            "migration": "any profile change requires an append-only reviewed Blueprint-version migration, a new positive profile version, preserved prior history and invalidation/reacceptance of every affected receipt",
        },
        "conjecture_resolution_identity_contract": (
            None
            if program.kind == "theorem"
            else {
                "schema_version": "awesome-theorems/stage5-conjecture-resolution-identity/1.0",
                "statement_fingerprint": {
                    "algorithm": "SHA-256 of canonical JSON",
                    "inputs": [
                        "exact Strict_Conjecture_Ledger credit bytes/hash",
                        "exact Open_Claim_List record/variant/source-context bytes/hash",
                        "Stage5 and one-to-one Stage6 identities",
                        "canonical Statement.lean Claim elaborated expression and tracked toolchain/provider pins",
                    ],
                    "recompute": "each phase and Master independently reconstructs from primary bytes; copied strings are not evidence",
                },
            "scope": "strict Stage5 proof-resolution TARGETs only; S5POOL occurrence-intake TARGETs use conjecture_occurrence_intake_contract and cannot claim resolution credit",
            "claim_orientation": "Claim",
                "baseline_material_status": "open",
                "resolution_polarity_enum": ["Claim", "Not Claim"],
                "terminal_lean_exact_type_digest": "SHA-256 of BOOT-validator canonical serialization of the fully elaborated Lean Expr: constructor tags, de Bruijn indices, explicit universe levels, constants with environment declaration hashes and normalized binder metadata under exact toolchain/environment hash; pretty-printer text is display-only and any metavariable/synthetic opaque placeholder is rejected",
                "resolution_dag": {
                    "closed_fields": ["version", "root_node_id", "nodes", "edges", "topological_order", "dag_sha256", "supersedes_version"],
                    "node_identity": "stable ID plus exact typed inputs/output/body/provider/provenance/trust hashes",
                    "edge_identity": "child, parent, composition declaration/type/body digest",
                    "cut_sets": ["mapping_cut_set", "candidate_human_cut_set", "candidate_machine_cut_set"],
                },
                "readability_receipt": "binds the identical accepted DAG/version/fingerprint/outcome polarity plus remaining_readability_cut_set=[], exact stable anchors and reviewer decisions; RESOLUTION never self-certifies readability",
                "status_event_chain": {
                    "event_kind_enum": ["resolve", "invalidate", "supersede"],
                    "resolve": "open -> proved|refuted; binds accepted resolution version/DAG/type/phase receipts",
                    "invalidate": "proved|refuted -> under_review; binds prior event, reason and exact invalidated receipt/DAG references while retaining all history",
                    "supersede": "under_review -> proved|refuted; binds the new accepted resolution version/DAG/type/phase receipts and superseded event",
                    "prior_event_sha256": "null only for the first resolve event; otherwise mandatory exact previous append-only event digest",
                    "effective_status": "derived from the last valid event plus RELEASE checkbox: only RELEASE=x with a terminal resolve/supersede is currently proved/refuted; blank/underscore or terminal invalidate is under_review and old resolution history grants no current credit",
                    "authority": "only canonical Master RELEASE acceptance/invalidation/supersession transactions append events; no worker rewrites or deletes status history",
                    "binding": "Statement fingerprint/open baseline, outcome polarity where applicable, accepted DAG/type/phase receipts and immutable STATUS baseline",
                },
                "cross_phase_equality": "RESOLUTION, HUMAN, LEAN, READABLE, VALIDATE and RELEASE receipts carry byte-equal fingerprint/outcome-polarity/DAG-root/version fields; STATUS carries the same fingerprint/open baseline but no authoritative outcome polarity",
                "master_rule": "recompute every field and digest from integrated primary bytes before acceptance; arbitrary equal strings, copied worker JSON or status labels never satisfy identity",
                "mandatory_mutations": ["source byte", "binder/domain", "Claim-to-Not-Claim", "outcome flip", "Lean exact type", "DAG root/node/edge", "cut-set deletion", "prior-event", "phase receipt mismatch"],
            }
        ),
        "conjecture_occurrence_intake_contract": (
            None
            if program.kind == "theorem"
            else {
                "schema_version": "awesome-theorems/stage5-conjecture-occurrence-intake/1.0",
                "source_occurrence_denominator": CONJECTURE_POOL_COUNT,
                "target_item_range": ["S5CON-POOL-00000001-INTAKE", "S5CON-POOL-00014865-INTAKE"],
                "pool_id_range": ["S5POOL-00000001", "S5POOL-00014865"],
                "authority": CONJECTURE_POOL_MANIFEST.relative_to(ROOT).as_posix(),
                "identity_registry": CONJECTURE_POOL_IDENTITIES.relative_to(ROOT).as_posix(),
                "semantic_boundary": "source occurrence and dated source status only; not a distinct strict identity, independent current-open verification, proof target, Stage5 claim ID or retired renumbering alias",
                "short_goal_clause": "Perform only the source-occurrence intake adjudication in the claim card; do not attempt a proof, claim current-open or strict status, allocate a Stage5/Stage6 identity, or grant mathematical resolution credit.",
                "internal_subchecklist": ["INTAKE", "STATEMENT-EXACTIFICATION", "STATUS", "RIGHTS", "IMPORTANCE", "FULL-CATALOG-IDENTITY", "ADJUDICATION"],
                "relation_kind_enum": ["exact_existing", "equivalent", "subsumed", "special_case", "same_family", "new_identity", "split_required", "pointer_only", "status_quarantine", "rights_quarantine"],
                "completion_rule": "Master-accepted evidence-complete adjudication; x never means mathematically proved/refuted and never grants catalog or strict credit",
                "promotion_rule": "only a separately reviewed append-only Stage5 catalog and retired renumbering alias migration may convert one accepted semantic identity into one proof-resolution TARGET; multiple occurrences never multiply workers or credit",
            }
        ),
        "concurrency_prompt_contract": concurrency_prompt_contract(program),
        "host_headroom_policy": "host observations may only reduce the explicit prompt vector; every reduction is recorded as a binding reason; no host headroom default is encoded here",
        "operator_budget_policy": {
            "durable_read_only_authority_file": "Docs/evidence/stage5_shared_execution/operator-budget-v1.json",
            "durable_trust_root_file": "Docs/evidence/stage5_shared_execution/operator-budget-trust-root-v1.json",
            "runtime_resolved_copy": f"{execution_root}/config/operator-budget.resolved.json",
            "cleanup_preserves_durable_authority": True,
            "authority_mode": "local_codex_active_goal_registry_binding",
            "operator_goal_thread_id": operator_thread_id,
            "operator_goal_objective_sha256": operator_objective_sha256,
            "initial_authority_sha256": None,
            "initial_trust_root_sha256": operator_trust_root_sha256,
            "initial_route_price_authority_sha256": None,
            "initial_state": "not_authorized_v2_requires_new_explicit_operator_goal_and_budget_authority",
            "worker_launch_authorized": False,
            "external_spend_authorized": False,
            "authorization_scope": "none initially; v1 goal/budget bindings are historical and cannot activate v2; a new explicit operator authority must accompany the complete concurrency prompt and may authorize only the prompt-resolved vector for this program on the frozen route",
            "finite_initial_allowances": {
                "program": program.version,
                "model_input_tokens": 2000000000,
                "model_output_tokens": 500000000,
                "model_turns": "unbounded",
                "external_launches": 960,
                "wall_seconds": 145152000,
                "cpu_seconds": 145152000,
                "per_claim_maxima": {
                    "model_input_tokens": 2000000,
                    "model_output_tokens": 500000,
                    "model_turns": "unbounded",
                    "external_launches": 4,
                    "wall_seconds": 1209600,
                    "cpu_seconds": 1209600,
                    "generation_lifetime_seconds": 1209600,
                    "generation_replacements_per_work_item": 60,
                },
            },
            "always_required_positive_finite_caps": [
                "model_input_tokens",
                "model_output_tokens",
                "external_launches",
                "wall_seconds",
                "cpu_seconds",
            ],
            "billing_mode": "operator_goal_authorized_unknown_price",
            "billing_contract": {
                "price_claim": "none: neither zero cost nor any invented monetary price is asserted",
                "authorization": "the active user-provided Codex goal explicitly requests this route and ceiling; activation and every launch must verify the exact local thread/objective remains active",
                "universal": "positive finite token, external-launch, wall-time and compute caps remain mandatory; model input/output turn count is explicitly unbounded by operator policy",
            },
            "required_authority_fields": [
                "operator_identity",
                "authority_mode",
                "goal_thread_id",
                "goal_objective_sha256",
                "trust_root_sha256",
                "issued_at",
                "expires_at",
                "billing_mode",
                "billing_binding",
                "program_allowances",
                "combined_allowances",
                "per_claim_maxima",
                "reserve_policy",
                "authority_sha256",
            ],
            "signature_contract": {
                "algorithm": "local Codex active-goal registry verification plus canonical SHA-256 sealing",
                "canonical_body": "canonical JSON of every closed authority field except authority_sha256",
                "authority_sha256": "SHA-256 of the exact canonical authority body",
                "trust_root_file": "Docs/evidence/stage5_shared_execution/operator-budget-trust-root-v1.json",
                "trust_activation": "the reviewed specification pins the exact local goal thread/objective trust-root SHA; controller activation and every launch independently read the local goals registry and require that exact goal to remain active",
                "nonclaim": "this local binding is not represented as an Ed25519 signature, monetary price attestation or unmetered-route claim",
            },
            "admission_rule": "fail closed when the exact active goal authority is absent, paused, cleared, expired, malformed, digest-mismatched, non-finite, non-positive for a required cap, insufficiently funded, or the exact route cannot be authenticated",
            "activation_rule": "after BOOT acceptance, materialize the canonical authority bound to this exact specification SHA; every tick verifies the pinned active goal, exact route and remaining finite balance under the shared budget lease before launch or external spend",
            "reservation_rule": "under the shared budget lease, reserve worst-case finite spend before admission and append the reservation with the claim/run identity and prior-ledger hash",
            "settlement_rule": "append measured tokens/turns/launches/time/compute and record monetary cost as unknown rather than zero; release only unused reservation; overrun stops the lane, grants no acceptance and requires new explicit operator authority",
            "renewal_rule": "no implicit, automatic, negative, NaN, infinite or self-authorized budget and no renewal merely because work remains difficult",
        },
        "program_coordination": {
            "authority": program_authority,
            "availability_rule": "this program fails closed if its own runtime, lease, or append-only ledger cannot be opened, locked, parsed, digest-verified and fsync-tested; it never waits on or reads the other program's runtime",
            "lease_identity": "program, item, claim, run, exact resource/path, holder pid/start time, nonce, acquired/expires instants and prior ledger hash",
            "release_rule": "release only the exact authenticated lease; expiry never grants acceptance and stale reclamation requires durable reconciliation evidence",
            "no_cross_program_pool": "theorem and conjecture have separate runtime roots, ledgers, budget reservations and two-goal caps; no combined total, shared coordinator or shared capacity admission exists",
        },
        "scheduler": {
            "cadence": "*/2 * * * *",
            "tick_budget_seconds": 100,
            "startup_deadline_seconds": 180,
            "claim_lease_seconds": 1209600,
            "generation_lifetime_seconds": 1209600,
            "generation_replacements_per_work_item": 60,
            "recovery_policy": {
                "backoff_initial_seconds": 60,
                "backoff_max_seconds": 3600,
                "backoff_multiplier": 2,
                "backoff_jitter_ratio": 0.2,
                "retry_after_precedence": "provider_retry_after_then_exponential",
                "breaker_failure_threshold": 3,
                "breaker_cooldown_seconds": 1800,
            },
            "lease_renewal": "only an authenticated exact-identity lane with a durable progress heartbeat may renew; expiry never grants completion and harvest precedes retirement",
            "repair_attempts_per_failure_identity": 3,
            "cron_marker_binding": marker_binding(
                f"{program.kind}-execution-cron",
                program.cron_marker_begin,
                program.cron_marker_end,
            ),
        },
        "controller_activation": {
            "preconditions": "BOOT=x through the one-time acceptance procedure, exact ongoing checker/controller digests accepted, shared embedded authority matched, and explicit operator activation plus positive finite budget/trust authority resolved",
            "action": "canonical-Master internal operation installs only the exact reviewed cron marker with compare-and-swap against current crontab and starts no worker directly",
            "exact_cron_command": cron_command,
            "exact_cron_command_sha256": sha256_bytes(cron_command.encode("utf-8")),
            "command_contract": {
                "schedule": "*/2 * * * *",
                "cwd": CANONICAL_ROOT.as_posix(),
                "argv": [
                    "/usr/bin/python3",
                    f"{CANONICAL_ROOT.as_posix()}/scripts/{controller_name}.py",
                    "--tick",
                ],
                "combined_log": f"{CANONICAL_ROOT.as_posix()}/{execution_root}/logs/cron.log",
                "forbidden": "extra shell commands, environment overrides, alternate transports, command substitution, unreviewed wrapper or log target",
            },
            "receipt": f"Docs/evidence/stage5_{kind_plural}/execution/controller-activation.json",
            "receipt_rule": "content-address and independently review pre/post crontab digests, exact marker/controller/spec/shared-authority/operator-authority hashes and activation instant; this is not BOOT-owned and cannot be written before BOOT=x",
            "initial_state": "not_activated",
        },
        "marker_namespace": {
            "blueprint_markers": {
                "checklist": marker_binding("checklist", CHECKLIST_BEGIN, CHECKLIST_END),
                "specification": marker_binding("specification", SPEC_BEGIN, SPEC_END),
                "requirements": marker_binding("requirements", REQUIREMENTS_BEGIN, REQUIREMENTS_END),
            },
            "gantt_markers": {
                "metadata": marker_binding("gantt-metadata", GANTT_META_BEGIN, GANTT_META_END),
                "index": marker_binding("gantt-index", GANTT_INDEX_BEGIN, GANTT_INDEX_END),
            },
            "cron_pairs": {
                "theorem": marker_binding(
                    "theorem-execution-cron",
                    THEOREM.cron_marker_begin,
                    THEOREM.cron_marker_end,
                ),
                "conjecture": marker_binding(
                    "conjecture-execution-cron",
                    CONJECTURE.cron_marker_begin,
                    CONJECTURE.cron_marker_end,
                ),
            },
            "uniqueness_rule": "Blueprint/Gantt marker pairs are intentionally shared schemas but are scoped to one named authoritative file and must occur exactly once there in order, with no orphan, nesting or duplicate; cron marker identities are globally unique across theorem/conjecture programs and installed cron state, with no cross-program reuse or pre-existing conflict",
        },
        "startup_state_machine": [
            "reserved",
            "materialized",
            "tmux_started",
            "goal_pasted",
            "goal_submitted",
            "live",
            "handoff_ready",
            "finished",
        ],
        "codex_home_bootstrap": {
            "allowed": ["required authentication credentials", "minimal selected provider/route configuration"],
            "forbidden": ["project trust history", "plugins", "marketplaces", "MCP servers", "prior threads", "prior goals", "logs", "SQLite registries"],
        },
        "launch_environment": {
            "unset": ["CODEX_CI", "CODEX_THREAD_ID", "CODEX_REMOTE_PAYLOAD"],
            "required": ["task-local CODEX_HOME", "task-local work cwd", "task-local tmux socket/session", "one interactive Codex process tree", "one thread", "one active /goal"],
            "forbidden": ["Docker or other container worker transport", "shared tmux server", "second thread", "second /goal", "second mathematical or source-occurrence ID"],
            "lock_fd_inheritance": "forbidden",
        },
        "artifact_policy": {
            "allowed": "exact checklist-owned repository paths, controller ledgers, content-addressed handoffs, validation logs and accepted receipts",
            "forbidden": "secrets, whole-repository copies, undeclared files, shared writable caches, symlink escapes and worker edits to authority/catalog/aggregators",
            "harvest_rule": "copy result and patch bytes into the immutable public archive keyed by claim, baseline and patch digest before liveness pruning or runtime deletion",
        },
        "task_materialization_validation": {
            "claim_root": "exact resolved task root must be a real controller-owned directory under the configured program runtime, with no symlink/mount escape and no writable ancestor shared with another claim",
            "file_provenance": "every materialized declared file records source path/hash, copy method and device/inode; hardlinks, reflinks, snapshots, mounts, archives, rsync/clone and whole-tree copies are forbidden even when inode differs; only fresh byte-copy of individually allowlisted files is valid",
            "immutable_metadata": "claim card/metadata bytes and authority hashes are frozen before materialization, checked before launch and rechecked at harvest; any mutation retires the claim without acceptance",
            "full_checkout_sentinels": [".git", "lake-manifest.json plus unrelated source tree", "catalog plus Docs plus scripts", "foreign Blueprint/runtime roots"],
            "baseline_checks": "before launch and harvest, rehash every read-only and writable baseline, verify all changed paths equal the exact owned-path allowlist, and reject untracked/out-of-scope bytes, symlink devices, alternate data streams and patch path escapes",
            "session_access_audit": "before liveness credit and harvest, scan the private current-generation session command/tool ledger; any predecessor, sibling or other-program task-root reference is a hard boundary violation, retires the generation and makes its result ineligible",
            "mandatory_mutations": ["hardlink", "reflink/provenance mismatch", "symlink", "mount", "claim metadata tamper", "full-checkout sentinel combination", "foreign task-root read/write/reference", "out-of-scope patch at harvest", "baseline changed after launch"],
        },
        "repository_discovery_snapshot": {
            "observed_at": "2026-08-10T14:20:00Z",
            "branch": "main",
            "origin": "https://github.com/weiyangzen/awesome_theorems.git",
            "dirty_paths_before_blueprint_generation": 67,
            "codex_cli": "codex-cli 0.147.0",
            "tmux": "tmux 3.4",
            "host": {
                "logical_cpus": 32,
                "memory_total_bytes": 98823827456,
                "memory_available_bytes": 68537380864,
                "swap_total_bytes": 8589930496,
                "disk_available_bytes": 2177149534208,
                "pid_limit": 348994,
                "processes_observed": 593,
                "usable_accelerators": 0,
                "accelerator_observation": "nvidia-smi installed but no communicating driver; no accelerator lane admitted",
            },
            "existing_external_cron_marker": "HARNESSFS_COMMUNITY_EXECUTION_V1",
            "existing_stage1_controller": "not reusable: current execution skill forbids its app-server transport surface",
            "boundary": "observational activation input, not a permanent capacity claim; every tick remeasures headroom and preserves unrelated cron/process state",
        },
        "ownership": {
            "canonical_checkout": "Master-only writes",
            "blueprint_checkboxes": "canonical Master only",
            "gantt": "atomic generated read-only projection",
            "workers": "task-local exact owned paths only; canonical checkout and Blueprint forbidden",
            "catalog_v5_v6": "read-only digest-bound input",
            "shared_aggregator": "serial Master-only",
            "shared_bootstrap_authority": "byte-identical authority object embedded in both Blueprints and both BOOT receipts; runtime CAS materialization only, no separate Docs owned_path",
        },
        "append_only_extensions": {
            "bootstrap_limit": "v2 contains exactly one strict TARGET row per mathematical identity and, for conjectures, one distinct POOL INTAKE row per pinned source occurrence; no target-scoped extension row is valid",
            "families": [],
            "target_local_append_only_rule": "proof units, conjecture exploration attempts, resolution supersessions and readability nodes remain TARGET-owned data inside the current generation; durable predecessor material must first be harvested and explicitly rematerialized as a declared target-local input, never read from an old task root, and these units never become checklist rows or simultaneous worker identities",
            "target_membership_rule": f"each of the sealed {program.target_count} execution members maps to exactly one member-kind-specific row and no arbitrary strict or pool ordinal is admitted",
            "ordinal_exhaustion_policy": "target-local ordinal grammars may be widened only by a Master-validated schema migration that preserves the stable TARGET identity; any worker replacement still uses a fresh nonoverlapping generation",
            "resolution_supersession_contract": (
                None
                if program.kind == "theorem"
                else {
                    "current_owned_path": "the TARGET-owned resolution-proof-units.json; replaceable only before TARGET acceptance or after reviewed TARGET x-to-blank invalidation with compare-and-swap",
                    "immutable_history": "before replacement, the controller copies exact old DAG bytes and receipt into the content-addressed immutable_acceptance_archive keyed by item/baseline/integrated-tree/decision digests; this archive is a controller acceptance surface, not an unowned worker artifact",
                    "acceptance_precondition": "mapping_cut_set=[], candidate_human_cut_set=[] and candidate_machine_cut_set=[] with exact fingerprint/outcome polarity inside the complete TARGET handoff",
                    "invalidation": "a later HUMAN/LEAN/READABLE/VALIDATE gap changes TARGET x to blank through reviewed invalidation, preserves the old version/receipt and resumes the same TARGET goal for correction",
                    "supersession": "new version is strictly increasing, binds supersedes_version and old/new DAG digests, and only a new Master-validated complete TARGET handoff may return TARGET to x; in-place accepted-DAG mutation is forbidden",
                }
            ),
            "row_requirements": "no target-scoped extension row is permitted; all internal work remains under the existing TARGET claim and exact owned paths",
            "migration_gate": "a Blueprint migration preserves the one-object-one-TARGET bijection, all unaffected states and predicates, and atomically records evidence-bound invalidations before any schema change",
            "forbidden": "target-scoped phase/extension rows, a second worker/goal for one object, runtime-only rows, renumbering, deletion, ID reuse, denominator shrinkage, accepted-DAG rewriting, dependency removal, predicate weakening or blank-to-x transition",
            "blueprint_migration_protocol": {
                "id_grammar": "S5PD-BLUEPRINT-MIGRATE-<000001..999999>",
                "receipt_path_grammar": "Docs/evidence/stage5_shared_execution/blueprint-migrations/S5PD-BLUEPRINT-MIGRATE-<ordinal>.json",
                "authority": "only BOOT's digest-bound ongoing checker may execute; isolated migration preparer, reviewer identity-distinct from preparer and Master, then canonical Master acceptance",
                "prepared_binding": "old Blueprint/Gantt/spec/DAG/source/shared-authority digests, every unaffected preserved state, exact affected x-to-blank invalidation set/reason/old receipts, added rows/owned paths/dependencies/budgets, strengthened predicates, new bytes/digests and prior migration receipt",
                "validation": "closed ID grammar and sealed-workset membership, DAG acyclicity/terminal ancestry, cross-program ownership and shared-lease exceptions, no old-byte/predicate weakening and all affected receipt invalidations",
                "commit": "journal the content-addressed receipt and compare-and-swap guards, then atomically replace every affected Blueprint with its same-prefix Gantt as one rollback-safe transaction; no one-file or runtime-only migration",
                "recovery": "transaction ID, old/new digests and receipt make restart deterministically roll back or idempotently finish before any controller admission",
            },
        },
        "provider_dependency_migration": {
            "id_grammar": "no worker checklist row; canonical-Master control transaction only",
            "authority": "canonical-Master migration validated outside mathematical worker transports",
            "provider_registry": f"Docs/evidence/stage5_{kind_plural}/provider-registry.json",
            "persistent_owned_path_grammar": f"Docs/evidence/stage5_{kind_plural}/dependency-migrations/<transaction-id>.json",
            "serial_shared_lease_targets": [
                "Formalizations/Lean/lakefile.lean",
                "Formalizations/Lean/lake-manifest.json",
                "Formalizations/Lean/lean-toolchain",
                f"Docs/evidence/stage5_{kind_plural}/provider-registry.json",
                f"Docs/evidence/stage5_{kind_plural}/foundation-profiles.json",
            ],
            "mutation_executor": "the predecessor-to-successor Blueprint migration is a canonical-Master control transaction, not a DEP-MIGRATE worker claim; it alone compare-and-swap edits the exact serial lease targets while atomically installing the successor authority",
            "ownership_rule": "the Master control transaction owns its unique receipt and exact shared dependency paths; mathematical TARGET workers never edit them",
            "cross_program_rule": "one globally unique migration receipt binds both affected program specifications; neither program resumes until Master validation succeeds",
            "downstream_rewire": "invalidate every affected TARGET plus aggregate, QA and program-release descendants; affected workers later resume their same goals under the new provider binding",
            "state_order": "atomically invalidate affected TARGET/aggregate descendants before root-file integration; after migration acceptance the same TARGET goals replay and reaccept, with no accepted row retaining an invalid environment",
            "pause_rule": "pause every theorem and conjecture lane whose dependency closure or validation environment may be affected before mutation and through reacceptance",
            "receipt_rule": "append the provider/version/body/license/SBOM/profile decision, preserve old provider history, invalidate all affected claim/profile/validation receipts and require their explicit replay and reacceptance",
        },
        "terminal_acceptance_transaction": {
            "precondition": "every ancestor of PROGRAM-RELEASE is accepted and all durable queues are empty; PROGRAM-RELEASE itself is still not accepted",
            "receipt_path": f"Docs/evidence/stage5_{kind_plural}/execution/program-release-acceptance.json",
            "journal_path": f"{execution_root}/transactions/program-release/<transaction-id>/manifest.json",
            "prepare": "freeze one transaction ID and exact bytes/digests for the post-transition Blueprint with PROGRAM-RELEASE=x, the Gantt projected from those post-transition bytes/final reconciled snapshot, and an acceptance receipt binding both digests, independent decisions and immutable-archive identity",
            "validate": "independent reviewer validates all three prepared byte strings, full ID coverage, program_complete=true and every source/spec/runtime/archive binding before any destination changes",
            "commit": "canonical Master writes a prepared fsync'd manifest containing old/new digests, then rollback-safely commits Blueprint, same-prefix Gantt and acceptance receipt as one three-output transaction and marks the manifest committed",
            "recovery": "on restart the exact transaction ID and old/new digests deterministically roll back all three or idempotently finish/archive a fully committed set; no state may treat post-x files without the matching receipt as accepted",
            "forbidden": "validating only the pre-transition Gantt, writing x before all three outputs are prepared, or exposing a durable one/two-file terminal state",
        },
        "claim_card_schema": f"Docs/evidence/stage5_{kind_plural}/claim-card.schema.json",
        "worker_result_schema": f"Docs/evidence/stage5_{kind_plural}/worker-result.schema.json",
        "master_acceptance_schema": f"Docs/evidence/stage5_{kind_plural}/master-acceptance.schema.json",
        "validation_profiles": [
            "inventory_and_identity",
            "exact_statement_semantics",
            *(
                [
                    "transitive_semantic_environment_and_no_shadowing",
                    "strict_dominance_over_m0387_negative_fixture",
                    "distilled_proof_sufficiency_and_nonduplication",
                ]
                if program.kind == "theorem" else []
            ),
            "pinned_lean4_trust0_build",
            "per_declaration_type_axiom_body_dependency",
            "proof_and_composition_graph",
            "human_math_and_readability",
            "cold_empty_build_offline_replay",
            "mutation_and_receipt_tamper",
            "full_program_projection_and_denominator",
        ],
        "cleanup": {
            "explicit_stop": "first copy every checksum-valid result and patch into the public immutable handoff archive and disposition every queue entry; then remove only this exact marker and controller-owned processes/runtime",
            "completion": "requires zero blank, zero underscore, empty handoff/integration/repair/checkpoint queues, passing repository gates, fresh Gantt and terminal program acceptance before scoped removal and absence receipt",
            "preserve": "canonical source, accepted artifacts, public immutable handoff/acceptance archives and final Gantt",
        },
        "git_policy": "preserve dirty canonical worktree; no reset stash checkout commit push or publication unless separately authorized",
        "skill_binding": {
            "package": "b3ehive execution-cron-builder 1.5.0+codex.20260811060051",
            "skill_sha256": "fa2207e9a48191f1492ab22b3a8b19fed5ebf22dc0f0448ea4fe610c94608f55",
            "execution_pattern_sha256": "df92db8b282edc3d364b953fa008c7a045abb54a620e877c399df32228a19637",
            "gate_rules_sha256": "b0eae1e59dbeb3b2de9bedb86831a7413ffd02cf220f3c2ba0b63bdb17d453bd",
        },
    }
    if program.kind == "conjecture":
        specification["conjecture_proof_search_prompt"] = conjecture_proof_search_prompt_contract()
    return specification


def source_chain_table() -> str:
    return f"""### Explicit pinned source-chain inventory

| Authority file | Exact file SHA-256 | Embedded authority/root binding |
|---|---|---|
| `Docs/catalog/v5/Current_Release.json` | `{STAGE5_CURRENT_SHA256}` | authority `{STAGE5_CURRENT_AUTHORITY_SHA256}`; release root `{RELEASE_ROOT_SHA256}` |
| `Docs/catalog/v5/releases/5.6/Release_Manifest.json` | `{RELEASE_MANIFEST_SHA256}` | authority `{STAGE5_MANIFEST_AUTHORITY_SHA256}`; release root `{RELEASE_ROOT_SHA256}` |
| `Docs/catalog/v6/Current_Release.json` | `{STAGE6_CURRENT_SHA256}` | authority `{STAGE6_CURRENT_AUTHORITY_SHA256}`; manifest `{STAGE6_MANIFEST_SHA256}`; release root `{STAGE6_RELEASE_ROOT_SHA256}` |
| `Docs/catalog/v6/releases/6.0/Migration_Manifest.json` | `{STAGE6_MANIFEST_SHA256}` | authority `{STAGE6_MANIFEST_AUTHORITY_SHA256}`; `final_migration=true` |
| `Docs/catalog/v6/releases/6.0/Stage6_ID_Registry.json` | `{STAGE6_REGISTRY_SHA256}` | authority `{STAGE6_REGISTRY_AUTHORITY_SHA256}` |
| `Docs/catalog/v6/releases/6.0/Migration_to_Stage6.json` | `{STAGE6_MIGRATION_SHA256}` | authority `{STAGE6_MIGRATION_AUTHORITY_SHA256}` |

The source bundle binds canonical root `{CANONICAL_ROOT}` under root authority `{CANONICAL_ROOT_AUTHORITY_SHA256}`. Relocation creates a new reviewed authority and cannot reinterpret receipts issued under this root."""


def conjecture_pool_source_table() -> str:
    return f"""### Conjecture-only source-occurrence overlay

| Authority file | Exact file SHA-256 | Boundary |
|---|---|---|
| `Docs/catalog/v5/pools/Current_Pool_Release.json` | `{CONJECTURE_POOL_CURRENT_SHA256}` | overlay authority `{CONJECTURE_POOL_CURRENT_AUTHORITY_SHA256}`; base release remains `5.6` |
| `Docs/catalog/v5/pools/conjecturebench-357bcb1a/Pool_Manifest.json` | `{CONJECTURE_POOL_MANIFEST_SHA256}` | authority `{CONJECTURE_POOL_MANIFEST_AUTHORITY_SHA256}`; source occurrences `14,865`; strict credits `0` |
| `Docs/catalog/v5/pools/conjecturebench-357bcb1a/Source_Occurrence_Pool.jsonl` | `{CONJECTURE_POOL_OCCURRENCES_SHA256}` | one sealed row per pinned occurrence |
| `Docs/catalog/v5/pools/conjecturebench-357bcb1a/Identity_Registry.jsonl` | `{CONJECTURE_POOL_IDENTITIES_SHA256}` | every identity relation initially pending; no automatic promotion |
"""


def program_inventory_section(program: Program) -> str:
    if program.kind == "theorem":
        return f"""## 2. Frozen denominator and present debt\n\n| Binding | Frozen value |\n|---|---|\n| Release | Stage5 `5.6`, root `{RELEASE_ROOT_SHA256}` |\n| Manifest SHA-256 | `{RELEASE_MANIFEST_SHA256}` |\n| Theorem projection SHA-256 | `{THEOREM_SOURCE_SHA256}` |\n| Theorem projection authority | `{THEOREM_AUTHORITY_SHA256}` |\n| Exact sorted S5-ID-set digest | `{THEOREM_ID_SET_SHA256}` |\n| Denominator | exactly **3,500** unique theorem records |\n| Current evidence cohorts | `ML-KERNEL=2,000`; `FC-REPLAY=131`; `FC-SORRY=1,369` |\n\nAll 3,500 have a Lean 4 formal type. The 2,000 mathlib records have pinned batch-level kernel/sorry-free evidence, but still owe per-declaration exact type, body, dependency, axiom, wrapper and receipt evidence. The 131 source-sorry-free Formal Conjectures rows remain `source_asserted_not_replayed`; the other 1,369 contain `sorryAx`. All 3,500 currently owe a THM-M-0387-grade, independently reviewed human-readable proof reconstruction. A docstring is statement metadata, not a proof.\n"""
    return f"""## 2. Frozen denominator and present debt\n\n| Binding | Frozen value |\n|---|---|\n| Base release | Stage5 `5.6`, root `{RELEASE_ROOT_SHA256}`; immutable and still the sole catalog release |\n| Manifest SHA-256 | `{RELEASE_MANIFEST_SHA256}` |\n| Strict ledger SHA-256 | `{STRICT_SOURCE_SHA256}` |\n| Strict ledger authority | `{STRICT_AUTHORITY_SHA256}` |\n| Exact sorted strict S5-ID-set digest | `{STRICT_ID_SET_SHA256}` |\n| Joined open projection SHA-256 | `{OPEN_SOURCE_SHA256}` |\n| Strict proof-resolution denominator | exactly **1,425** effective strict-conjecture credits |\n| Strict source cohorts | `FC-STATEMENT=400`; `OPENCONJECTURE=600`; `V55-RESEARCH=425` |\n| Conjecture occurrence overlay | ConjectureBench `{CONJECTURE_POOL_SOURCE_COMMIT}`; manifest `{CONJECTURE_POOL_MANIFEST_SHA256}` |\n| Occurrence intake denominator | exactly **14,865** source occurrences: `CB-CURATED=302`; `CB-FAMILY=9,342`; `CB-CATALOG=5,221` |\n| Source-observed upper bounds | not reported answered: **14,785**; active-labelled: **14,782**; neither is a strict/current-open denominator |\n| Total executable TARGET rows | exactly **16,290** = 1,425 strict resolution + 14,865 occurrence intake/adjudication |\n| Explicit non-credit boundary | overlay adds `0` strict credits, `0` S5-CLM IDs and `0` retired renumbering aliases |\n| Base exclusions | revoked `S5-CLM-00005311`; all 599 base-release `open_problem` rows |\n\nThe 1,425 strict identities retain their frozen proof/refutation boundary. The 14,865 overlay records are source occurrences from 302 curated records, 9,342 parameter-family instances and 5,221 extended-catalog entries; inclusion and source status are not independent verification. The overlay includes related records, placeholders, source pointers, contested/unclear rows and 80 records reported answered by their source. Those rows first owe exact statement/frontier, current-status, rights, importance and full-catalog identity adjudication. Intake acceptance never means proof, never grants strict credit and never mutates frozen Stage5 `5.6` or the retired renumbering branch; only a separately reviewed append-only catalog/alias migration may promote one semantic identity to one future proof TARGET.\n"""


def inventory_section(program: Program) -> str:
    program_section = program_inventory_section(program)
    heading = "## 2. Frozen denominator and present debt\n\n"
    if not program_section.startswith(heading):
        raise BlueprintError(f"{program.kind}: inventory heading drift")
    return (
        heading
        + source_chain_table()
        + ("\n\n" + conjecture_pool_source_table() if program.kind == "conjecture" else "")
        + "\n\n### Program-specific inventory\n\n"
        + program_section[len(heading) :]
    )


def debt_section(program: Program) -> str:
    if program.kind == "theorem":
        return """## 3. Debt axes and exact completion semantics\n\nThe following axes are independent and may never be inferred from checklist state:\n\n- `identity_exactness`: exact frozen claim, variant, source and retired renumbering alias binding.\n- `semantic_environment`: the elaborated root expression and every transitive non-foundation constant are bound to pinned provider declaration/type/body/source/revision hashes. Local declarations, notation, macros, coercions, namespace aliases or import substitutions may not shadow or reinterpret source symbols; a text-identical theorem header is not semantic evidence.\n- `human_source`: primary proof bytes and exact theorem/hypothesis crosswalk.\n- `machine_closure`: `M0-L` local body, `M0-W` pinned mathlib body through a local exact wrapper, or `M0-P` another pinned provider through a local exact wrapper.\n- `readability`: true `R0` only after complete anchored proof-DAG reconstruction and independent review.\n- `workflow`: blank, checksum-valid typed handoff or Master acceptance; never mathematical evidence. A terminal `/goal`, retired generation or exhausted execution limit changes transport/lifecycle state only and never proves theorem completion.\n\n`machine_complete` requires the Master to re-elaborate the exact unconditional root in the bound semantic environment, close every root-relevant proof/composition node, audit each declaration body/dependency/axiom and pass clean cold offline replay plus semantic-substitution mutations. `readable_complete` requires a total injective DAG-node-to-fragment map with reverse coverage and independent review. `theorem_complete` is their conjunction, zero H/M/R cut sets, a current validation trace and a strict-dominance certificate over the pinned THM-M-0387 negative fixture.\n\n`distilled` means removing duplication and generated inventory prose, not removing mathematics: each substantive node appears once and still states its inputs and hypotheses, inference, output, formal anchor, downstream use, exceptional cases and trust boundary. An audit, blocker, conditional implication, source claim, wrapper name, percentage, nonempty dossier or polished summary cannot substitute for this conjunction.\n"""
    return """## 3. Debt axes, outcomes and exact completion semantics\n\nStrict resolution targets record independent `catalog_binding`, `current_status_review`, `domain_classification`, `statement_exactness`, `human_resolution`, `machine_closure`, `readability`, `material_outcome` and workflow axes. Occurrence intake targets instead record exact source binding, statement/frontier exactification, status, rights, importance, semantic identity relation and adjudication; an intake row has no proof outcome and its x state means only evidence-complete adjudication. The only strict-resolution root outcomes are:\n\n| Outcome | Human debt | Machine debt | Resolution-readable debt | RELEASE |\n|---|---|---|---|---|\n| `proved` | independently accepted complete proof of exact `Claim` | checked Lean theorem `Claim` | reviewed final proof tree | may close only when all gates pass |\n| `refuted` | independently accepted complete refutation of exact `Claim` | checked Lean theorem `Not Claim`, preferably witness-to-negation | reviewed final refutation tree | may close only when all gates pass |\n| `open` | outstanding | root outstanding | frontier prose does not close resolution readability | must remain unfinished |\n\nA candidate, claimed solution, proof sketch, special case, finite verification, failed search, numerical/SMT/CAS observation, weakened theorem, added hypothesis, barrier or independence theorem remains open unless it composes to the exact permitted root outcome. A machine-found witness obtains refutation credit only after Lean checks that exact witness and derives `Not Claim`. An exploration item may be accepted when its precommitted bounded attempt is honestly complete; this never advances HUMAN, LEAN, READABLE, VALIDATE or RELEASE. Occurrence intake x likewise advances no HUMAN, LEAN, READABLE, VALIDATE or RELEASE proof-resolution axis and grants no catalog credit.\n"""


def m0387_section(program: Program) -> str:
    object_name = "theorem" if program.kind == "theorem" else "resolved conjecture"
    if program.kind != "theorem":
        return f"""## 4. THM-M-0387 floor and mandatory upgrades\n\n`THM-M-0387` supplies the minimum evidence *shape*: exact identity and statement, typed proof units, separate H/M/R debt, proof-body and trust boundaries, Lean 4 wrappers, exact-type and axiom probes, human-readable node reconstructions, structured validation and content-addressed receipts. Its exact meta/proof-unit/current-receipt/critical-audit bytes are pinned in the source bundle. It is not a positive completion fixture: its current root is `H1/M2/R0`, only `29/93` machine targets are closed, and `root_machine_closed=false`; the pinned critical audit rejects benchmark readiness.\n\nConsequently the validator uses it only as one negative conformance fixture: dossier presence and historical `R0` annotations cannot yield `{object_name}_complete`. Independent axis-isolation mutations also require exact M0 plus fake/shared/colliding R0 to fail readability and exact-looking roots through claim-specific axioms/bodyless oracles/unreviewed providers to fail machine closure. Every target must have exact root `M0-L/W/P`, per-declaration probes, injective stable node-to-fragment anchors with reverse coverage, current clean cold offline replay, mutations and independent Master release. FLT-specific node counts, branches and observed foundation names are instance facts, never universal constants; every target freezes its own reviewed profile.\n"""
    return """## 4. THM-M-0387 negative floor and strict-dominance gate\n\n`THM-M-0387` contributes a pinned negative fixture and evidence shape, not a completion precedent. Its current root is `H1/M2/R0`, only `29/93` machine targets are closed and `root_machine_closed=false`; the pinned critical audit rejects benchmark readiness. Copying its dossier layout, historic `R0`, prose volume or receipt style therefore grants no completion credit.\n\nEvery theorem release carries a machine-checkable strict-dominance certificate. It must (1) pass every evidence-shape check applicable to THM-M-0387, (2) close the exact root at `M0-L`, `M0-W` or reviewed `M0-P`, (3) have empty human, machine and readability cut sets, (4) add an independently recomputed elaborated-expression/transitive-semantic-environment lock, (5) pass cold from-source replay and semantic-substitution mutations, and (6) bind total injective readable reconstruction plus reverse coverage. At least the semantic-environment and adversarial-replay dimensions are strict additions over the fixture. Any absent, stale, self-attested or non-strict comparison fails closed.\n\nThe certificate compares predicates and content hashes, never page count or verbosity. Output remains distilled: machine inventories live in structured evidence, human surfaces avoid repetition, and no compression may elide a hypothesis, inference, output, formal anchor, downstream dependency, exceptional case or trust boundary. Instance-specific node counts, branches and foundation names are frozen per target, not copied from FLT.\n"""


def phase_section(program: Program) -> str:
    if program.kind == "theorem":
        return """## 5. Per-theorem one-worker execution boundary\n\nEvery frozen S5 theorem is physically instantiated below as exactly one stable `S5THM-<8-digit-id>-TARGET`. That TARGET is the durable theorem-work identity and survives every lane assignment, generation, process, thread, `/goal`, checkpoint and retry until canonical-Master acceptance. At any instant it has at most one worker generation. Every admitted generation has its own fresh task root, private tmux server/socket/session, private `CODEX_HOME`, interactive Codex process tree, thread and exactly one submitted `/goal`; no generation shares any of them, and no worker may inspect another task root or claim a second mathematical ID.\n\nInside the current generation, the worker maintains target-local progress through `INTAKE -> STATEMENT/ANCHOR -> TREE -> MACHINE -> READABLE -> VALIDATE -> RELEASE`. Those names are evidence sections, not Blueprint rows, scheduler claims, dependencies, tmux sessions, threads or goals. A healthy active goal may continue under the same generation. Goal state, generation state and theorem-work state are independent: a terminal `/goal`, expired generation, provider failure, controller restart or retired process is never `theorem_complete`. Before fencing or replacement, the controller must enter terminal-pending-disposition and content-address a typed complete or partial handoff/checkpoint. Only after that durable harvest may it stop the old transport and create a fresh nonoverlapping generation with a new run ID/root/home/thread/goal and one newly submitted `/goal`. Predecessor artifacts are usable only after controller harvest and explicit rematerialization into the new task; direct reads from old or sibling task roots are forbidden. Different TARGET rows depend only on BOOT, never on one another; only shard, aggregate, QA and program-release rows combine accepted targets.\n"""
    return f"""## 5. Per-member one-worker conjecture boundary

Every frozen strict conjecture is physically instantiated below as exactly one stable `S5CON-<8-digit-id>-TARGET`; every pinned source occurrence is separately instantiated as `S5CON-POOL-<8-digit-pool-ordinal>-INTAKE`. At any instant either row has at most one worker generation. Every admitted generation has its own fresh task root, private tmux server/socket/session, private `CODEX_HOME`, interactive Codex process tree, thread and exactly one submitted `/goal`; no generation shares any of them, and no worker may inspect another task root or claim a second mathematical or source-occurrence ID.

Inside a strict generation, the worker maintains target-local progress through `INTAKE -> STATEMENT -> STATUS -> FRONTIER -> EXPLORE -> RESOLUTION -> HUMAN/LEAN -> READABLE -> VALIDATE -> RELEASE`. Inside an occurrence generation it maintains `INTAKE -> STATEMENT-EXACTIFICATION -> STATUS -> RIGHTS -> IMPORTANCE -> FULL-CATALOG-IDENTITY -> ADJUDICATION`; it has no proof-resolution stage and cannot create proof credit. Those names are evidence sections, not Blueprint rows, scheduler claims, dependencies, tmux sessions, threads or goals. A healthy active goal may continue under the same generation. If it becomes terminal, fails liveness or violates isolation, the controller fully fences and stops it before creating a fresh nonoverlapping generation with a new run ID/root/home/thread/goal and one newly submitted `/goal`. Predecessor artifacts are usable only after controller harvest and explicit rematerialization into the new task; direct reads from old or sibling task roots are forbidden. Different strict and intake rows depend only on BOOT, never on one another; strict proof shards and intake-adjudication shards remain separate and join only at program QA.

### 5.1 Injected conjecture proof-search discipline

Every strict resolution TARGET claim card selects exactly the `strict_resolution_proof_search` branch of a closed `work_contract`. Its workflow source is pinned to `{CROUZEIX_PROMPT_REPOSITORY}` commit `{CROUZEIX_PROMPT_COMMIT}`, source SHA-256 `{CROUZEIX_PROMPT_SHA256}`, with the project-specific extraction at `{CROUZEIX_PROMPT_EXTRACTION.relative_to(ROOT).as_posix()}`. Every occurrence INTAKE instead selects exactly the disjoint `source_occurrence_intake` branch, which explicitly forbids proof work and carries no Crouzeix/Claim-or-Not-Claim protocol. The source is prompt-method evidence only, never evidence that any Stage5 conjecture or upstream candidate proof is mathematically correct.

Within the one authenticated long-lived `/goal`, the worker maintains a durable registry of genuinely distinct mathematical approach families; protects early routes from premature convergence; records concrete lemmas, constructions, equations, invariants, certificates or counterexamples and each exact gap; marks a theorem-equivalent missing-lemma route blocked; reopens it only for a materially new mechanism; keeps incompatible routes alive through multiple rounds; and repeatedly synthesizes, adversarially challenges, redirects and starts fresh rounds. Every resolution candidate is attacked for hidden hypotheses, polarity mismatch, circularity, equivalent reformulation, unsupported routine steps, invalid domain/sign/limit/case transitions, degenerate cases and Lean formalizability.

The original prompt's multi-agent topology, affirmative-only assumption, local path, web restrictions and refusal to report openness are not imported. Conceptual route diversity runs serially inside the same worker; collaboration tools, subagents, child threads and hidden request concurrency remain forbidden. Only a standalone exact `Claim` or `Not Claim` human derivation plus adversarial review, exact Lean root and all declared gates can close the TARGET. Finite checks, special cases, reductions, failed searches and polished summaries are truthful partial checkpoints only and never completion.
"""


def _legacy_base_protocol_sections(program: Program) -> str:
    service_tier = frozen_codex_service_tier(program)
    return f"""## 6. Checklist and authority protocol\n\nThis file is the sole requirements and checkbox authority. The only states are blank (not done), underscore (checksum-valid worker handoff harvested but not accepted), and `x` (canonical Master integrated and independently accepted). Blank and underscore both block dependency closure and completion. Workers never edit this Blueprint, its checkboxes, the canonical checkout, the Gantt, shared aggregators or catalog inputs. File existence, a worker success claim, an exit-zero command, generated prose or a catalog label never advances state.\n\nEvery checklist line freezes an immutable item ID, explicit dependencies, exact repository-relative owned paths and a verifiable gate. Dependencies must exist and be acyclic; advanced items require all direct dependencies accepted. Ownership rejects aliases, globs, absolute paths, `..`, runtime/control paths, duplicates and directory-prefix overlaps. Document order creates no dependency. The terminal PROGRAM-RELEASE ancestor closure must contain every other row.\n\n## 7. Isolation, claim cards and durable handoff\n\nEach generation root has the exact shape `{program.runtime_root}/tasks/<claim-id>/<run-id>/` with independent `work/`, `codex-home/`, `tmux.sock`, immutable `claim.json` and worker-owned `result.json`. Only declared writable paths and individually justified read-only bootstrap files are materialized with independent inodes; cloning, copying, rsyncing, reflinking, hardlinking, archiving, mounting or snapshotting the complete repository is forbidden. Credentials never enter task work. A generation may access its exact root and declared materialized inputs only. Reading or writing any predecessor, sibling or other-program task root is a hard boundary violation, invalidates the result and forces retirement.\n\nThe claim card binds specification/Blueprint/inventory digests, claim/run/item identities, stable lane and fresh generation IDs, the prompt epoch/digest and complete resolved concurrency vector. A result with `status=self_tested` truthfully binds changed paths, patch checksum, commands, exits and evidence. The controller audits the private current-session command/tool ledger for foreign task-root references before liveness credit and harvest, then content-addresses a valid result and patch before stopping the finished TUI. A healthy active generation may continue; otherwise the old tmux/process/root is fully fenced before one fresh nonoverlapping generation receives one new `/goal`.\n\n## 8. Codex transport, startup and liveness\n\nCodex execution is exactly one host task-local tmux server/socket/session, one ordinary interactive Codex TUI process tree, one private writable `CODEX_HOME`, one thread and exactly one authenticated active `/goal` per admitted generation. Docker and every other container worker transport are forbidden. The controller builds argv as an array and explicitly passes `-m {FROZEN_CODEX_MODEL}`, `model_reasoning_effort={FROZEN_CODEX_REASONING_EFFORT}`, `service_tier={service_tier}`, `features.goals=true`, both multi-agent flags false and a developer constraint forbidding collaboration tools, subagents and child threads. It pastes one short claim objective ending in a claim-specific completion token, observes that token in the real active composer, submits exactly once, and authenticates the tmux socket/session, pane PID/start time, process tree, exact cwd, private home, sole private thread, sole active goal, frozen route and clean foreign-task-root audit before counting a lane live.\n\nApp-server, controller JSON-RPC, `codex exec`, shared daemons, shared tmux, shared writable state, child threads, Docker/container workers, a second mathematical ID, cross-task-root access and no-tmux fallbacks are hard failures. A healthy `goal_submitted` lane with delayed registry writes stays starting until its bounded deadline and is promoted later without duplicate launch. Process-name counts and reservations are telemetry, not live goals.\n\n## 9. Prompt-bound scheduler, admission and integration\n\nA tick first parses and seals a complete operator concurrency prompt; a missing, partial, unknown, stale or environment-only vector fails closed before materialization, reservation or launch. Required dimensions include logical claims, service records or explicit `not_applicable`, agent executions, startup reservations, launch fanout per wave, live transports, authenticated goals, running turns, request starts per window, in-flight requests, integration, validators and exact-path conflicts. The prompt values are requested ceilings; host/resource checks may only reduce them and must record the binding reason.\n\nThe repository lease is held only for short validation, harvest, reconciliation, Blueprint/DAG state, reservation and final merge transactions. Slow preparation, TUI startup, model turns, network operations, Lean builds and integration validation run outside the lease; lock descriptors close before launch. A bounded admission pump launches independent claims in concurrent waves (fanout comes from the prompt) using an async/task-group/equivalent executor, isolates sibling failures and then merges durable results. A serial launch loop or a lock held across slow work is non-conforming. It repeatedly launches waves until the prompt-resolved target is full, the tick budget expires or a persisted dependency/conflict/startup/host/external/route/validator reason binds every missing slot. It always harvests first, retires and proves the exact old generation stopped second, and only then admits a replacement. Logical TARGETs, durable lanes, fresh generations, starting reservations, authenticated goals, running turns, request rate/in-flight, integration and validators are reported separately.\n\nThe Master integrates only dependency-ready, exact-path-conflict-safe immutable handoffs into the preserved dirty canonical tree, reruns item and repository gates, and alone advances underscore to `x`. Failure preserves the handoff and enters bounded repair without blocking unrelated work. Workers never modify the root Lake lock, toolchain or global aggregator; dependency changes require a separate serialized policy migration. Commit, push and external publication are disabled unless separately authorized.\n\n## 10. Lean 4 validation profile\n\nThe present reusable preflight is `python3 scripts/check_lean_environment.py`, binding Lean 4.29.0, Lake 5.0.0, mathlib `8a178386...` and the current manifest. The generic Stage5 validator does not yet exist and is a P0 checklist dependency. It must run literal structured recipes equivalent to:\n\n```text\npython3 scripts/check_lean_environment.py\ncd Formalizations/Lean\nelan run <tracked-toolchain> lake build +<exact-claim-module>\nelan run <tracked-toolchain> lake env lean --trust=0 <exact-Audit.lean>\n```\n\nEvery `Audit.lean` contains an exact-type example and a terminal structured axiom query. The checker strips comments/strings before rejecting placeholders, parses observed transitive axioms, freezes the exact accepted set, binds the real local or pinned provider body and proves provider use rather than trusting a wrapper. `lake env lean` exit zero, `checkdecls`, the existing M0387-specific lint and batch axiom unions are insufficient alone. Claim-local writable build state is isolated; dependency checkouts/caches are read-only, clean and hash-bound.\n\n## 11. Gantt and observability\n\n`{program.gantt.relative_to(ROOT).as_posix()}` is the mandatory same-prefix, generated read-only projection and never a second cursor. It includes a renderable Mermaid milestone, Blueprint/spec/inventory/runtime/prompt digests, generation time, state counts and exactly one monitoring row per checklist ID with dependencies, ownership, stable lane/fresh generation, startup/live/running/handoff/integration/repair, request metrics, planning and runtime blockers and timing. Unknown timing is visibly `unscheduled`; no dates are inferred from order or DAG depth. Atomic replacement occurs after final tick reconciliation. Missing, misnamed, stale, duplicate or incomplete projection fails a tick and completion.\n\n## 12. Stop, completion and cleanup\n\nExplicit stop first harvests and dispositions every eligible handoff, removes only this controller's exact cron marker, stops its task-local tmux servers and attributable descendants, preserves canonical and accepted artifacts, waits one cadence and proves absence without touching unrelated host processes or the existing HarnessFS cron. Boundary-violating results are never harvested as valid handoffs. Completion cleanup is stricter: all checklist rows accepted, all mathematical root debts closed, zero handoff/integration/repair/checkpoint backlog, all gates and the final Gantt fresh, and PROGRAM-RELEASE accepted. Cleanup is idempotent and records exact cron/process/socket/lock/runtime absence; PROGRAM-RELEASE remains a durable completion surface after runtime removal.\n\n## 13. Change and scope control\n\nThe frozen denominators cannot silently shrink. A source correction or mathematical reclassification requires an independently reviewed append-only catalog migration and an explicit Blueprint version migration; until authorized, the original target remains unfinished. Stable item IDs are never reused. New internal exploration attempts or proof units remain TARGET-local; they never create a second simultaneous worker. Any change to inventory, toolchain, dependency, axiom profile, semantic target, execution spec, validator, route or prompt policy invalidates affected receipts and reopens their gates.\n\nThe current Stage5 catalog and these Blueprints are local workspace artifacts: this document authorizes neither Git commit/push nor external publication.\n"""


def base_protocol_sections(program: Program) -> str:
    rendered = _legacy_base_protocol_sections(program)
    rendered = rendered.replace(
        f"`{program.runtime_root}/tasks/<claim-id>/<run-id>/`",
        f"`{runtime_execution_root(program)}/tasks/<claim-id>/<run-id>/`",
    )
    rendered = rendered.replace(
        f"`-m {FROZEN_CODEX_MODEL}`",
        f"`-m {frozen_codex_model(program)}`",
    )
    if program.kind == "theorem":
        rendered = rendered.replace(
            "both multi-agent flags false and a developer constraint forbidding "
            "collaboration tools, subagents and child threads",
            "both in-process multi-agent flags false; subagents are permitted only "
            "when the controller admits each child as a first-class execution with "
            "its own tmux/CODEX_HOME/thread/goal/result and charges it against the "
            "same global 24-execution and request ceilings",
        ).replace(
            "shared writable state, child threads, Docker/container workers",
            "shared writable state, hidden or in-process child threads, unaccounted "
            "subagents, Docker/container workers",
        )
    return rendered


def protocol_sections(program: Program) -> str:
    base = base_protocol_sections(program)
    execution_root = runtime_execution_root(program)
    anchor = (
        "\n\nThe current Stage5 catalog and these Blueprints are local workspace artifacts: "
        "this document authorizes neither Git commit/push nor external publication.\n"
    )
    if base.count(anchor) != 1:
        raise BlueprintError(f"{program.kind}: protocol addendum anchor drift")
    addendum = f"""

### 13.1 Program-local coordination, finite work and monotone migrations

This `{program.kind}` controller is a closed execution domain. Its runtime root, scheduler/admission leases, operator-budget reservations, request-rate ledger, exact-path locks, validator leases, handoffs, cleanup records and capacity counters live only under `{execution_root}`. The theorem controller and conjecture controller have separate roots and never read, lock, sum, replenish or wait on one another's state. A missing, unreadable, unsealable or inconsistent local surface blocks only this program; there is no cross-program capacity pool.

Fixed MACHINE/HUMAN/LEAN/RESOLUTION/READABLE rows are finite closure or review gates, not long-lived workers. New proof units, exploration attempts and readability nodes exist only as append-only stable extension rows with strictly positive operator-authorized finite budgets, ordinary durable underscore handoff, independent review and Master acceptance. This bootstrap parser accepts only the fixed v1 template; before any extension, BOOT's ongoing checker must be installed, independently accepted and digest-bound, then an independently reviewed Blueprint-version migration must add the row, exact ownership and dependencies and rewire terminal ancestry.

Every migration binds the prior Blueprint, specification and DAG as ancestor authorities. Legacy v1 phase IDs, rows and evidence remain immutable in the migration receipt and historical archives but are retired from the active v2 checklist; they are never reused, and no phase state is promoted into TARGET completion. Acceptance predicates may only be preserved or strengthened. Renumbering, ID reuse, denominator shrinkage, predicate weakening or rewriting an accepted resolution/proof DAG is forbidden. Provider changes are canonical-Master migrations outside mathematical workers, pause affected lanes under this program's local leases, exclusively own the exact root Lean dependency paths for the transaction, and invalidate then replay affected receipts. Target workers never alter root dependencies, and a migration never creates a second goal for a target.

The present Blueprint is only a one-time pristine scaffold authority and its Gantt is only a bootstrap projection. Neither file installs cron, activates a controller, creates runtime, authorizes worker launch or supplies operator budget. BOOT is the sole pre-controller exception: this canonical manager's narrow digest-bound handoff/review actions handle blank-to-underscore and underscore-to-x with atomic Gantt/receipt updates. The accepted ongoing checker handles every non-BOOT transition; direct blank-to-x is forbidden for every mode.

For PROGRAM-RELEASE, “all rows” means every other/ancestor row. The terminal preparer and independent reviewer validate the exact post-x Blueprint bytes and Gantt projected from those post-transition bytes before either destination changes; the Master commits both as one rollback-safe transaction. A pre-transition Gantt cannot authenticate terminal acceptance.
"""
    addendum = addendum.replace(
        "Fixed MACHINE/HUMAN/LEAN/RESOLUTION/READABLE rows are finite closure or review gates, not long-lived workers. New proof units, exploration attempts and readability nodes exist only as append-only stable extension rows with strictly positive operator-authorized finite budgets, ordinary durable underscore handoff, independent review and Master acceptance. This bootstrap parser accepts only the fixed v1 template; before any extension, BOOT's ongoing checker must be installed, independently accepted and digest-bound, then an independently reviewed Blueprint-version migration must add the row, exact ownership and dependencies and rewire terminal ancestry.",
        "MACHINE/HUMAN/LEAN/RESOLUTION/READABLE are target-local subchecks inside the mathematical object's sole stable TARGET, never separate rows or simultaneous workers. New proof units, exploration attempts and readability nodes remain append-only TARGET-owned data inside the current generation; durable predecessor material must be harvested and explicitly rematerialized rather than read from an old task root. They receive no separate checklist state, and the canonical Master validator reviews the harvested complete handoff without opening a second mathematical worker.",
    )
    lifecycle = ""
    if program.kind == "theorem":
        lifecycle = """

### 13.2 Theorem progress checkpoint, terminal disposition and recovery contract

The theorem work item, logical lane, concrete generation and authenticated `/goal` are four separate axes. The durable theorem item remains unfinished across all generation turnover. The Gantt and runtime projection must report `theorem_work_state`, `lane_state`, `generation_state`, `goal_state`, `handoff_kind`, latest checkpoint sequence/digest, terminal disposition, replacement lineage and current blocker separately; no one of those values may be inferred from another.

Every material progress checkpoint binds the exact TARGET and frozen semantic environment; the claim/specification/prompt/baseline digests; a monotone sequence; completed INTAKE/STATEMENT/ANCHOR/TREE/MACHINE/READABLE/VALIDATE/RELEASE facts with artifact hashes and validation outcomes; exact Lean goals and failed proof routes; current M/H/R cuts; the strongest verified machine closure; readable-proof debt; next safe action; blocker evidence; and consumed wall/token/turn/CPU/retry accounting. A checkpoint grants no mathematical or checkbox credit. A replacement receives only the latest checksum-valid harvested checkpoint through explicit claim-local rematerialization.

The closed theorem handoff taxonomy is `complete_candidate`, `machine_complete_reading_debt`, `proof_search_checkpoint`, `provider_retryable`, `validation_repair_required`, `proof_blocked_with_evidence` and `boundary_invalid`. Only `complete_candidate` may enter canonical-Master completion integration. `machine_complete_reading_debt` preserves exact M0 evidence and resumes at readability; `proof_search_checkpoint` preserves verified partial proof state; `provider_retryable` waits for the prompt-bound provider backoff/breaker policy; `validation_repair_required` resumes the exact failed validation identity; `proof_blocked_with_evidence` remains unfinished for operator/research review; and `boundary_invalid` grants no artifact credit beyond separately revalidated clean evidence. No partial class clears dependencies or becomes `x`.

A generation whose goal is terminal first enters `terminal_pending_disposition`. Retirement or replacement is forbidden until the canonical result/checkpoint emitter has produced a schema-valid manifest and the controller has harvested it durably; failure to emit is itself an unresolved recovery state, not permission to erase the task root. Worker completion, controller terminal salvage, synthetic activation tests, harvest parsing and Master preflight use one canonical schema/emitter contract so a worker cannot report a shape the controller rejects after the process disappears.

Concurrency and lifetime/recovery policy are independent. The successor lifecycle prompt must explicitly supply every Blueprint-selected concurrency dimension and every selected wall, input-token, output-token, model-turn, CPU, external-launch, failure-class retry, backoff and breaker value with units and scope. This Blueprint defines names, relations and theorem semantics only; it supplies no concurrency fallback. Missing, inferred, environment-only, stale or ambiguous prompt values fail before side effects. Generations admitted before this lifecycle migration keep their immutable claim-bound legacy values and may hand off normally, but their old values are never copied forward as defaults for a replacement.
"""
    return base.replace(anchor, addendum + lifecycle + anchor, 1)


def task_line(task: Task) -> str:
    deps = ",".join(task.dependencies) if task.dependencies else "-"
    paths = ",".join(task.owned_paths) if task.owned_paths else "-"
    return f"- [{task.state}] `{task.item_id}` {task.title} | depends_on={deps} | owned_paths={paths} | gate={task.gate}"


def tasks_with_boot_state(program: Program, tasks: list[Task], state: str) -> list[Task]:
    boot_id = f"{program.task_prefix}-BOOT-001"
    if state not in {"_", "x"}:
        raise BlueprintError("BOOT acceptor target state must be underscore or x")
    result = [task.with_state(state) if task.item_id == boot_id else task for task in tasks]
    validate_task_set(program, result)
    if [task.item_id for task in result if task.state != " "] != [boot_id]:
        raise BlueprintError("BOOT acceptor changed a non-BOOT task")
    return result


def rewrite_blueprint_states(
    program: Program, raw: bytes, current: list[Task], wanted: list[Task]
) -> bytes:
    text = raw.decode("utf-8")
    before, rest = text.split(CHECKLIST_BEGIN, 1)
    _, after = rest.split(CHECKLIST_END, 1)
    result = (
        before
        + CHECKLIST_BEGIN
        + "\n"
        + "\n".join(task_line(task) for task in wanted)
        + "\n"
        + CHECKLIST_END
        + after
    ).encode("utf-8")
    parsed = parse_blueprint(
        program,
        result,
        [task.with_state(" ") for task in current],
        allow_boot_transition=True,
    )
    if parsed != wanted:
        raise BlueprintError("BOOT state rewrite did not round-trip exactly")
    return result


def controller_validation_section() -> str:
    section = """## 14. Mandatory generated-controller validation

Before activation, adversarial tests must prove all of the following on isolated fixtures: validate-only creates no claim, tmux server or process; executable argv is interactive TUI and cannot resolve to app-server or `codex exec`; simultaneous claims have distinct task roots, sockets, sessions, process identities, homes, threads and goals; exactly one complete `/goal` is submitted per generation; only fully authenticated identities with a clean current-session foreign-task-root audit count live; delayed healthy registration promotes without relaunch; dead, mismatched or boundary-violating generations retire before replacement; harvest precedes prune and stops finished TUI servers; a boundary-violating result is never harvested; the scheduler lock is not inherited; every cap prevents lane `N+1`; with `N` eligible conflict-free claims and admitted headroom, one bounded admission pump reaches exactly `N` live lanes; and every underfill records its specific binding reason.

The tests must also prove exact terminal `Blueprint`-to-`Gantt` naming, one monitoring row per checklist ID, state-transition projection, stale source/spec/runtime rejection, atomic Gantt replacement after final merge, absence of fabricated timing, exact ownership and full-repository-copy rejection, worker inability to edit checkboxes or canonical files, safe continuation of only a healthy exact generation, fresh nonoverlapping replacement after retirement, rejection of predecessor/sibling/other-program task-root reads and writes, scoped stop and completion cleanup, and no effect on unrelated cron or host Codex processes. Producer and every phase-required reviewer must have distinct role claim IDs/roots/tmux/homes/threads/goals, launch only after immutable predecessor handoff where applicable, reserve/count separate budgets/caps, and appear as separate role objects in the ongoing Gantt; only producer harvest permits underscore and all required reviewer decisions plus Master recomputation permit x. Mathematical axis-isolation mutations must reject (a) an exact M0 machine root paired with self-labeled R0, shared unanchored prose or node-to-anchor collisions, and (b) an exact-looking root obtained through a claim-specific axiom, bodyless oracle or unreviewed provider, independently of M0387's compound M2 failure. Semantic-identity mutations must also reject text-identical theorem headers whose local environment redefines or shadows a source constant through `def`, `abbrev`, notation, syntax, macro, coercion, namespace alias or substituted imports—including real numbers changed to naturals, polynomials changed to lists and a substantive predicate changed to `True` or reflexivity. The checker recomputes the elaborated root and transitive non-foundation declaration/type/body/source/revision hashes from pinned providers; worker-supplied names or hashes are never self-authenticating. The positive suite must accept valid M0-L, M0-W and reviewed M0-P roots only when each has exact semantic identity, true R0, empty H/M/R cuts, a current trace and a strict-dominance certificate proving all applicable THM-M-0387 evidence-shape predicates plus the additional semantic-environment and cold-replay predicates. Readability requires an injective stable node-to-anchor mapping and a reverse anchor-to-exact-fragment ledger for every required DAG node; one generic fragment cannot cover multiple substantive nodes, and reviewer conflict checks include all prior authors/contributors. Distilled-output mutations delete each hypothesis, inference, output, formal anchor, downstream use, exceptional case and trust boundary in turn and must fail, while pure duplicate prose removal must preserve the evidence digest. Cold replay mutations include a shadowed stale target olean and assert an exact read trace proves every target/dependency object used was rebuilt or individually verified from bound sources; semantic failures exit nonzero with typed machine-resolvable source/node/receipt locators. Two unlike fixture repositories with different roots, blueprint names, IDs, languages, validators and route policies must show zero cross-project constants. Static scans fail executable forbidden transports, unexplained absolute or foreign paths and hidden fallback routes.
"""
    section = section.replace(
        "Producer and every phase-required reviewer must have distinct role claim IDs/roots/tmux/homes/threads/goals, launch only after immutable predecessor handoff where applicable, reserve/count separate budgets/caps, and appear as separate role objects in the ongoing Gantt; only producer harvest permits underscore and all required reviewer decisions plus Master recomputation permit x.",
        "For every mathematical TARGET, tests must prove a bijection among one frozen mathematical ID, one checklist row, one active claim root, one tmux server/socket/session, one private CODEX_HOME, one process tree, one thread and one active /goal; no internal phase or reviewer may create another worker identity, and the worker cannot touch a second mathematical ID. They must separately mutate theorem-work, lane, generation and goal states; prove terminal goal enters terminal_pending_disposition; reject retirement/replacement until a checksum-valid typed handoff or checkpoint is harvested; rematerialize the latest checkpoint without predecessor-root access; and prove complete_candidate, machine_complete_reading_debt, proof_search_checkpoint, provider_retryable, validation_repair_required, proof_blocked_with_evidence and boundary_invalid take distinct paths. Only complete_candidate is eligible for canonical-Master completion integration and x; every other kind remains dependency-blocking unfinished work. A synthetic completed-goal result must pass the same canonical emitter, harvest parser, schema and Master preflight used by a real worker.",
    )
    return section


def current_state_and_navigation(program: Program) -> str:
    plural = "Theorems" if program.kind == "theorem" else "Conjectures"
    if program.kind == "theorem":
        cohort_pattern = "FC-SORRY|FC-REPLAY|ML-KERNEL"
        example_id = "S5THM-00003485"
        shard_prefix = "S5THM-SHARD-"
    else:
        cohort_pattern = "FC-STATEMENT|OPENCONJECTURE|V55-RESEARCH|CB-CURATED|CB-FAMILY|CB-CATALOG"
        example_id = "S5CON-00003486"
        shard_prefix = "S5CON-SHARD-"
    blueprint = program.blueprint.relative_to(ROOT).as_posix()
    return f"""### Current-state matrix: what exists now versus execution deliverables

| Surface | Present in this bootstrap repository now | Produced only by accepted execution |
|---|---|---|
| Frozen catalog and release pins | yes: exact Stage5/Stage6 files, hashes, authorities and denominators in the pinned inventory below | no reinterpretation; changes require migration |
| Lean environment preflight | yes: `scripts/check_lean_environment.py` and tracked Lean/Lake pins | per-claim cold trust-zero validation receipts |
| Blueprint scaffold | yes: one-time pristine all-blank authority generated by this manager | BOOT alone uses this manager's narrow handoff/review acceptance actions; all non-BOOT transitions require its accepted ongoing checker |
| Gantt | yes: bootstrap all-unscheduled projection only | reconciled runtime, frontiers, blockers and final post-transition projection |
| Instance roots and Stage5 Lean roots | absent | per-target exact owned artifacts and Lean modules |
| Closed schemas and generic validators | absent | BOOT deliverables with independent acceptance |
| Ongoing checker/generator and controller | absent; this scaffold does not install or activate them | BOOT deliverables whose exact digests bind activation |
| Runtime, handoffs and ledgers | absent | controller-created only after accepted BOOT and operator budget authority |

### Cohort, shard and ID navigation

```bash
rg -n '{cohort_pattern}' {blueprint}
rg -n '{shard_prefix}' {blueprint}
rg -n '{example_id}-' {blueprint}
rg -n 'PROGRAM-RELEASE' {blueprint}
```

The first command locates cohort-tagged TARGET rows, the second shard seals, the third the sole TARGET for one concrete numeric ID shape, and the fourth the sole terminal row for the Stage5 {plural.lower()} program.
"""


def render_blueprint(program: Program, tasks: list[Task]) -> bytes:
    spec = spec_object(program)
    counts = Counter(task.state for task in tasks)
    title_kind = "Theorem" if program.kind == "theorem" else "Conjecture"
    mission = (
        "close machine-proof and human-readable proof debt for every frozen Stage5 theorem"
        if program.kind == "theorem"
        else "resolve every frozen strict conjecture and evidence-completely adjudicate every pinned source occurrence without converting occurrence count into strict credit"
    )
    member_label = (
        f"3,500 strict theorem TARGETs"
        if program.kind == "theorem"
        else f"{CONJECTURE_STRICT_TARGET_COUNT} strict conjecture TARGETs plus {CONJECTURE_POOL_COUNT} non-credit-bearing source-occurrence INTAKE rows"
    )
    header = f"""# Stage5 {title_kind} Proof-Debt Execution Blueprint\n\n> Document type: sole Stage5 {program.kind} proof-debt requirements and execution-checklist authority  \n> Blueprint version: `{program.version}`  \n> Authoritative path: `{program.blueprint.relative_to(ROOT).as_posix()}`  \n> Mandatory same-prefix Gantt: `{program.gantt.relative_to(ROOT).as_posix()}`  \n> Frozen execution members: `{program.target_count}`  \n> Member worker rows: exactly one member-kind-specific TARGET or INTAKE row per execution member  \n> Initial checklist items: `{len(tasks)}` (`blank={counts[' ']}`, `underscore={counts['_']}`, `accepted={counts['x']}`)  \n> Initial timing: all items unscheduled; no calendar estimate is inferred\n\n## 1. Mission and non-negotiable completion boundary\n\nThis program exists to {mission}. It is an execution authority, not a plan-only inventory and not a claim that the debts are already paid. Every strict mathematical target and, where declared, every source-occurrence intake member is physically enumerated exactly once in the checklist; aggregate counts, internal subphases, shards, aliases and variants never replace or multiply per-ID acceptance.\n\nOnly the canonical Master may accept work after integrating exact-path handoffs and rerunning the gates. The controller may keep making progress indefinitely, but it may declare program completion only at the terminal condition specified below. Difficulty, budget consumption, a bounded attempt, an audit, a blocker, or lack of a known route is never completion.\n\n{inventory_section(program)}\n{debt_section(program)}\n{m0387_section(program)}\n{phase_section(program)}\n{SPEC_BEGIN}\n```json\n{json.dumps(spec, ensure_ascii=False, sort_keys=True, indent=2)}\n```\n{SPEC_END}\n\n{protocol_sections(program)}\n{controller_validation_section()}\n## 15. Authoritative execution checklist\n\nThe region below is the only mutable task-state cursor. Every nonblank line inside it is one task row.\n\n{CHECKLIST_BEGIN}\n"""
    rendered_inventory = inventory_section(program)
    header = header.replace(
        "It is an execution authority, not a plan-only inventory and not a claim that the debts are already paid.",
        "It is an execution authority for requirements/checklist semantics only, not an activated controller, not a plan-only aggregate inventory and not a claim that the debts are already paid.",
        1,
    )
    header = header.replace(
        f"> Frozen execution members: `{program.target_count}`  ",
        f"> Frozen execution members: `{program.target_count}` ({member_label})  ",
        1,
    )
    inventory_anchor = "\n\n" + rendered_inventory
    if header.count(inventory_anchor) != 1:
        raise BlueprintError(f"{program.kind}: inventory insertion anchor drift")
    header = header.replace(
        inventory_anchor,
        "\n\n" + current_state_and_navigation(program) + "\n" + rendered_inventory,
        1,
    )
    header = header.replace(
        "\n## 14. Authoritative execution checklist\n",
        "\n" + controller_validation_section() + "\n## 15. Authoritative execution checklist\n",
    )
    header = header.replace(
        "## 1. Mission and non-negotiable completion boundary",
        REQUIREMENTS_BEGIN + "\n## 1. Mission and non-negotiable completion boundary",
        1,
    )
    header = header.replace(
        "\n## 15. Authoritative execution checklist\n",
        "\n" + REQUIREMENTS_END + "\n\n## 15. Authoritative execution checklist\n",
        1,
    )
    body = "\n".join(task_line(task) for task in tasks)
    footer = f"\n{CHECKLIST_END}\n"
    return (header + body + footer).encode("utf-8")


def parse_blueprint(
    program: Program,
    raw: bytes,
    expected: list[Task],
    *,
    allow_boot_transition: bool = False,
    allow_superseded_authority_for_invalidation: bool = False,
    allow_immutable_row_drift: bool = False,
    allow_progress_cursor: bool = False,
    allow_legacy_execution_gate: bool = False,
) -> list[Task]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise BlueprintError(f"{program.kind}: Blueprint is not UTF-8") from exc
    validate_marker_constants()
    validate_marker_pairs(text, BLUEPRINT_MARKER_PAIRS, f"{program.kind} Blueprint")
    for marker in (
        CHECKLIST_BEGIN,
        CHECKLIST_END,
        SPEC_BEGIN,
        SPEC_END,
        REQUIREMENTS_BEGIN,
        REQUIREMENTS_END,
    ):
        if text.count(marker) != 1:
            raise BlueprintError(f"{program.kind}: marker count drift for {marker}")
    before, rest = text.split(CHECKLIST_BEGIN, 1)
    region, after = rest.split(CHECKLIST_END, 1)
    if CHECKBOX_LINE_RE.search(before) or CHECKBOX_LINE_RE.search(after):
        raise BlueprintError(f"{program.kind}: checkbox outside authoritative region")
    parsed: list[Task] = []
    for line_number, line in enumerate(region.splitlines(), start=1):
        if not line:
            continue
        match = ROW_RE.fullmatch(line)
        if match is None:
            raise BlueprintError(f"{program.kind}: invalid checklist line {line_number}")
        dependencies = split_field(match.group("depends"))
        paths = split_field(match.group("paths"))
        parsed.append(
            Task(
                match.group("id"),
                match.group("title"),
                dependencies,
                paths,
                match.group("gate"),
                match.group("state"),
            )
        )
    if len(parsed) != len(expected):
        raise BlueprintError(f"{program.kind}: expected {len(expected)} rows, found {len(parsed)}")
    for actual, template in zip(parsed, expected):
        if (
            actual.item_id,
            actual.title,
            actual.dependencies,
            actual.owned_paths,
            actual.gate,
        ) != (
            template.item_id,
            template.title,
            template.dependencies,
            template.owned_paths,
            template.gate,
        ) and not allow_immutable_row_drift:
            raise BlueprintError(f"{program.kind}: immutable row drift at {template.item_id}")
    validate_task_set(program, parsed, allow_legacy_execution_gate=allow_legacy_execution_gate)
    normalized_text = (
        before
        + CHECKLIST_BEGIN
        + "\n"
        + "\n".join(task_line(task.with_state(" ")) for task in parsed)
        + "\n"
        + CHECKLIST_END
        + after
    )
    expected_text = render_blueprint(program, expected).decode("utf-8")
    if (
        not allow_superseded_authority_for_invalidation
        and not program_isolation_active(program)
        and normalized_text != expected_text
    ):
        raise BlueprintError(f"{program.kind}: immutable authority bytes drift outside checkbox states")
    expected_header = f"> Blueprint version: `{program.version}`"
    expected_authority = f"> Authoritative path: `{program.blueprint.relative_to(ROOT).as_posix()}`"
    expected_gantt = f"> Mandatory same-prefix Gantt: `{program.gantt.relative_to(ROOT).as_posix()}`"
    if any(text.count(value) != 1 for value in (expected_header, expected_authority, expected_gantt)):
        raise BlueprintError(f"{program.kind}: authority header drift")
    actual_requirements = text.split(REQUIREMENTS_BEGIN, 1)[1].split(REQUIREMENTS_END, 1)[0]
    expected_requirements = expected_text.split(REQUIREMENTS_BEGIN, 1)[1].split(REQUIREMENTS_END, 1)[0]
    if (
        not allow_superseded_authority_for_invalidation
        and not program_isolation_active(program)
        and actual_requirements != expected_requirements
    ):
        raise BlueprintError(f"{program.kind}: immutable requirements prose drift")
    spec_text = text.split(SPEC_BEGIN, 1)[1].split(SPEC_END, 1)[0]
    fenced = spec_text.strip()
    if not fenced.startswith("```json\n") or not fenced.endswith("\n```"):
        raise BlueprintError(f"{program.kind}: malformed spec fence")
    observed_spec = strict_json_loads(fenced[8:-4], f"{program.kind} execution specification")
    if not isinstance(observed_spec, dict):
        raise BlueprintError(f"{program.kind}: execution specification is not an object")
    if (
        not allow_superseded_authority_for_invalidation
        and not program_isolation_active(program)
        and observed_spec != spec_object(program)
    ):
        raise BlueprintError(f"{program.kind}: execution specification drift")
    validate_state_evidence(
        program,
        parsed,
        allow_boot_transition=allow_boot_transition,
        allow_progress_cursor=allow_progress_cursor,
    )
    return parsed


def state_name(state: str) -> str:
    return {" ": "not_done", "_": "handoff_waiting_master", "x": "master_accepted"}[state]


def runtime_snapshot(program: Program) -> tuple[dict[str, Any] | None, str | None]:
    program_root = ROOT / program.runtime_root
    shared_root = ROOT / SHARED_RUNTIME_ROOT
    path = program_root / "status/runtime-snapshot.json"
    observed = [candidate for candidate in (program_root, shared_root, path) if path_lexists(candidate)]
    if observed:
        raise BlueprintError(
            f"{program.kind}: bootstrap projection refuses all runtime input and any runtime/control surface "
            f"({observed[0].relative_to(ROOT)}); the accepted BOOT-produced checker/generator "
            "must replace this bootstrap tool"
        )
    return None, None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical_timestamp(value: Any, label: str) -> str:
    if not isinstance(value, str) or not RFC3339_RE.fullmatch(value):
        raise BlueprintError(f"{label} must be whole-second RFC3339 UTC")
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise BlueprintError(f"{label} is not a real UTC instant") from exc
    return value


def extract_generated_at(raw: bytes) -> str:
    text = raw.decode("utf-8")
    validate_marker_constants()
    validate_marker_pairs(text, GANTT_MARKER_PAIRS, "Gantt")
    if text.count(GANTT_META_BEGIN) != 1 or text.count(GANTT_META_END) != 1:
        raise BlueprintError("Gantt metadata markers missing")
    block = text.split(GANTT_META_BEGIN, 1)[1].split(GANTT_META_END, 1)[0].strip()
    if not block.startswith("```json\n") or not block.endswith("\n```"):
        raise BlueprintError("invalid Gantt metadata fence")
    metadata = strict_json_loads(block[8:-4], "Gantt metadata")
    if not isinstance(metadata, dict):
        raise BlueprintError("Gantt metadata is not an object")
    return canonical_timestamp(metadata.get("generated_at"), "Gantt generated_at")


def checklist_dag_object(tasks: list[Task]) -> list[dict[str, Any]]:
    return [
        {
            "item_id": task.item_id,
            "dependencies": list(task.dependencies),
            "owned_paths": list(task.owned_paths),
            "task_authority_sha256": task_authority_sha256(task),
        }
        for task in tasks
    ]


def task_mode(program: Program, task: Task) -> dict[str, Any]:
    matches = [
        mode for mode in item_mode_records(program) if re.fullmatch(mode["id_regex"], task.item_id)
    ]
    if len(matches) != 1:
        raise BlueprintError(f"{task.item_id}: cannot resolve exact mode")
    return matches[0]


def render_gantt(
    program: Program,
    blueprint_raw: bytes,
    tasks: list[Task],
    generated_at: str,
    *,
    prompt_override: bytes | None = None,
) -> bytes:
    canonical_timestamp(generated_at, "generated_at")
    text = blueprint_raw.decode("utf-8")
    spec_region = text.split(SPEC_BEGIN, 1)[1].split(SPEC_END, 1)[0].encode("utf-8")
    runtime, runtime_sha = runtime_snapshot(program)
    runtime_items = runtime.get("items", {}) if runtime else {}
    if not isinstance(runtime_items, dict):
        raise BlueprintError(f"{program.kind}: runtime items is not an object")
    unknown_runtime = sorted(set(runtime_items) - {task.item_id for task in tasks})
    if unknown_runtime:
        raise BlueprintError(f"{program.kind}: runtime snapshot has unknown IDs {unknown_runtime[:5]}")
    counts = Counter(state_name(task.state) for task in tasks)
    by_id = {task.item_id: task for task in tasks}
    ready = [
        task
        for task in tasks
        if task.state == " " and all(by_id[dep].state == "x" for dep in task.dependencies)
    ]
    implementation_frontier = [
        task.item_id
        for task in ready
        if task_mode(program, task)["phase"] not in {"VALIDATE", "QA", "PROGRAM-RELEASE"}
    ]
    validation_preparation_frontier = [
        task.item_id
        for task in ready
        if task_mode(program, task)["phase"] in {"VALIDATE", "QA", "PROGRAM-RELEASE"}
    ]
    integration_frontier = [
        task.item_id
        for task in tasks
        if task.state == "_" and all(by_id[dep].state == "x" for dep in task.dependencies)
    ]
    dependency_block_count = sum(
        any(by_id[dep].state != "x" for dep in task.dependencies)
        for task in tasks
        if task.state != "x"
    )
    runtime_block_kinds = Counter()
    for item in runtime_items.values():
        if not isinstance(item, dict):
            continue
        block = item.get("block")
        if isinstance(block, dict) and isinstance(block.get("kind"), str):
            runtime_block_kinds[block["kind"]] += 1
        elif isinstance(block, str) and block:
            runtime_block_kinds[block] += 1
    spec = spec_object(program)
    prompt_path = ROOT / concurrency_prompt_path(program)
    prompt: dict[str, Any] | None = None
    prompt_digest: str | None = None
    canonical_blueprint = DOCS / (
        "Stage5_Theorems_Blueprint.md"
        if program.kind == "theorem"
        else "Stage5_Conjectures_Blueprint.md"
    )
    if prompt_override is not None or (
        program.blueprint == canonical_blueprint
        and prompt_path.is_file()
        and not prompt_path.is_symlink()
    ):
        prompt_raw = prompt_override if prompt_override is not None else prompt_path.read_bytes()
        prompt_value = strict_json_loads(prompt_raw, f"{program.kind} concurrency prompt")
        if not isinstance(prompt_value, dict) or prompt_value.get("schema_version") != CONCURRENCY_PROMPT_SCHEMA or prompt_value.get("program") != program.version:
            raise BlueprintError(f"{program.kind}: concurrency prompt schema/program mismatch")
        prompt_body = dict(prompt_value)
        prompt_authority = prompt_body.pop("authority_sha256", None)
        if not isinstance(prompt_authority, str) or sha256_bytes(canonical(prompt_body)) != prompt_authority:
            raise BlueprintError(f"{program.kind}: concurrency prompt seal mismatch")
        vector = prompt_value.get("concurrency")
        if not isinstance(vector, dict) or set(vector) != set(CONCURRENCY_DIMENSIONS):
            raise BlueprintError(f"{program.kind}: concurrency prompt must provide the complete dimension vector")
        if prompt_value.get("execution_spec_sha256") != sha256_bytes(canonical(spec)):
            raise BlueprintError(f"{program.kind}: concurrency prompt execution-spec binding mismatch")
        prompt = prompt_value
        prompt_digest = sha256_bytes(prompt_raw)
    source_bundle = source_bundle_object(program)
    shared_snapshot = {
        "program_coordination_authority_sha256": sha256_bytes(canonical(spec["coordination_authority"])),
        "runtime_snapshot_sha256": None,
        "operator_budget_authority_sha256": None,
        "controller_state": "not_activated",
        "authenticated_live_goals": 0,
    }
    metadata = {
        "schema_version": "awesome-theorems/stage5-proof-debt-gantt/1.0",
        "program": program.version,
        "blueprint_path": program.blueprint.relative_to(ROOT).as_posix(),
        "gantt_path": program.gantt.relative_to(ROOT).as_posix(),
        "blueprint_sha256": sha256_bytes(blueprint_raw),
        "execution_spec_region_sha256": sha256_bytes(spec_region),
        "execution_specification_sha256": sha256_bytes(canonical(spec)),
        "source_bundle": source_bundle,
        "source_bundle_sha256": source_bundle_sha256(program),
        "checklist_dag_sha256": sha256_bytes(canonical(checklist_dag_object(tasks))),
        "checklist_state_sha256": sha256_bytes(
            canonical([[task.item_id, state_name(task.state)] for task in tasks])
        ),
        "runtime_snapshot_path": f"{runtime_execution_root(program)}/status/runtime-snapshot.json",
        "runtime_snapshot_sha256": runtime_sha,
        "runtime_snapshot_id": runtime.get("snapshot_id") if runtime else None,
        "generated_at": generated_at,
        "item_count": len(tasks),
        "target_count": program.target_count,
        "strict_resolution_target_count": (
            CONJECTURE_STRICT_TARGET_COUNT if program.kind == "conjecture" else program.target_count
        ),
        "source_occurrence_intake_count": (
            CONJECTURE_POOL_COUNT if program.kind == "conjecture" else 0
        ),
        "program_complete": all(task.state == "x" for task in tasks),
        "state_counts": {
            "not_done": counts["not_done"],
            "handoff_waiting_master": counts["handoff_waiting_master"],
            "master_accepted": counts["master_accepted"],
        },
        "frontiers": {
            "implementation": implementation_frontier,
            "validation_preparation": validation_preparation_frontier,
            "integration": integration_frontier,
        },
        "block_counts": {
            "dependency": dependency_block_count,
            "exact_path_conflict": runtime_block_kinds["exact_path_conflict"],
            "resource": runtime_block_kinds["resource"],
            "route": runtime_block_kinds["route"],
        },
        "capacity_saturation_underfill": {
            "scope": f"{program.kind}-only snapshot; theorem and conjecture runtimes are independent and must never be summed",
            "shared_snapshot_id": sha256_bytes(canonical(shared_snapshot)),
            "shared_snapshot": shared_snapshot,
            "controller_state": "not_activated",
            "concurrency_prompt_contract": spec["concurrency_prompt_contract"],
            "prompt_path": concurrency_prompt_path(program),
            "prompt_digest": prompt_digest,
            "requested_vector": prompt.get("concurrency") if prompt else None,
            "observed_usage": {
                "logical_claims": 0,
                "starting_lanes": 0,
                "authenticated_live_goals": 0,
                "running_turns": 0,
                "canonical_integrations": 0,
                "lean_build_validators": 0,
                "external_launches_this_wave": 0,
            },
            "saturated_dimensions": [],
            "underfill": {
                "authenticated_live_goal_slots": (
                    prompt["concurrency"].get("authenticated_goals") if prompt else None
                ),
                "binding_reasons": [
                    "BOOT_not_accepted",
                    "operator_budget_authority_not_materialized",
                    *( [] if prompt else ["concurrency_prompt_required"] ),
                ],
            },
            "ongoing_generator_contract": f"replace bootstrap constants with reconciled {program.kind}-local capacities, reservations, authenticated usage, saturation dimensions and one durable binding reason for every missing usable slot on each tick",
        },
        "bootstrap_limitation": "all-unscheduled source/DAG projection only; BOOT's independently accepted ongoing checker must replace this manager before any transition or runtime input",
        "schedule_basis": "recorded runtime timestamps only; all others unscheduled",
    }
    mermaid_generated_at = generated_at.removesuffix("Z")
    title = "Theorems" if program.kind == "theorem" else "Conjectures"
    lines = [
        f"# Stage5 {title} Proof-Debt Gantt and Complete Monitor",
        "",
        f"> Generated read-only projection of `{program.blueprint.relative_to(ROOT).as_posix()}`; the Blueprint is the sole checklist authority.",
        "",
        GANTT_META_BEGIN,
        "```json",
        json.dumps(metadata, ensure_ascii=False, sort_keys=True, indent=2),
        "```",
        GANTT_META_END,
        "",
        "## Renderable recorded timing",
        "",
        "The projection timestamp is not a task estimate. Only exact runtime timestamps may add task bars; every task lacking them remains in the complete unscheduled index below.",
        "",
        "```mermaid",
        "gantt",
        f"    title Stage5 {title} recorded projection timing",
        "    dateFormat YYYY-MM-DDTHH:mm:ss",
        "    axisFormat %Y-%m-%d %H:%M",
        "    section Projection",
        f"    Projection generated UTC :milestone, projection, {mermaid_generated_at}, 0s",
        "```",
        "",
        "## Complete monitoring index",
        "",
        "Every stable checklist ID occurs exactly once. Planning blockers come from unfinished Blueprint dependencies; runtime state is independently bound to the optional durable snapshot.",
        "",
        GANTT_INDEX_BEGIN,
        "| Item | State | Depends on | Owned paths | Claim | Run | Owner | Startup | Live | Running | Handoff | Integration | Repair | Planning blockers | Runtime block | Timing |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for task in tasks:
        rt = runtime_items.get(task.item_id)
        if rt is not None and not isinstance(rt, dict):
            raise BlueprintError(f"{task.item_id}: runtime item is not an object")
        rt = rt or {}
        blockers = [dep for dep in task.dependencies if by_id[dep].state != "x"]
        timing = rt.get("timing") or {
            "status": "unscheduled",
            "start": None,
            "end": None,
            "duration_seconds": None,
            "source": None,
        }
        cells: list[Any] = [
            task.item_id,
            state_name(task.state),
            list(task.dependencies),
            list(task.owned_paths),
            rt.get("claim_id"),
            rt.get("run_id"),
            rt.get("owner"),
            rt.get("startup"),
            rt.get("live"),
            rt.get("running"),
            rt.get("handoff"),
            rt.get("integration"),
            rt.get("repair"),
            blockers,
            rt.get("block"),
            timing,
        ]
        encoded = [json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) for value in cells]
        lines.append("| " + " | ".join(encoded) + " |")
    lines.extend([GANTT_INDEX_END, ""])
    result = ("\n".join(lines)).encode("utf-8")
    result_text = result.decode("utf-8")
    validate_marker_pairs(result_text, GANTT_MARKER_PAIRS, f"{program.kind} generated Gantt")
    if CHECKBOX_LINE_RE.search(result_text):
        raise BlueprintError(f"{program.kind}: generated Gantt contains a mutable checkbox")
    return result


def path_lexists(path: Path) -> bool:
    return os.path.lexists(os.fspath(path))


@contextmanager
def manager_mutation_lock() -> Iterator[None]:
    """Serialize every manager recovery/preflight/commit without creating state."""
    validate_canonical_root()
    descriptor = os.open(DOCS, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise BlueprintError("another Stage5 Blueprint manager mutation is active") from exc
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def validate_output_path(path: Path) -> None:
    validate_canonical_root()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as exc:
        raise BlueprintError(f"output escapes canonical repository: {path}") from exc
    if not relative.parts or relative.parts[0] != "Docs":
        raise BlueprintError(f"manager output is outside Docs: {relative}")
    current = ROOT
    for part in relative.parts[:-1]:
        current = current / part
        if not path_lexists(current):
            raise BlueprintError(f"output parent does not exist: {current}")
        if current.is_symlink() or not current.is_dir():
            raise BlueprintError(f"output parent is not a real directory: {current}")
    if path_lexists(path) and (path.is_symlink() or not path.is_file()):
        raise BlueprintError(f"output target is not a regular non-symlink file: {path}")
    if not os.access(path.parent, os.W_OK | os.X_OK):
        raise BlueprintError(f"output parent is not writable/searchable: {path.parent}")


def validate_guard_path(path: Path) -> None:
    validate_canonical_root()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as exc:
        raise BlueprintError(f"guard path escapes canonical repository: {path}") from exc
    if not relative.parts:
        raise BlueprintError("repository root cannot be a file guard")
    current = ROOT
    for part in relative.parts[:-1]:
        current = current / part
        if current.is_symlink() or not current.is_dir():
            raise BlueprintError(f"guard parent is not a real directory: {current}")
    if path_lexists(path) and (path.is_symlink() or not path.is_file()):
        raise BlueprintError(f"guard target is not a regular non-symlink file: {path}")


def file_expectation_from_descriptor(descriptor: int, label: str) -> FileExpectation:
    try:
        observed = os.fstat(descriptor)
        if not stat.S_ISREG(observed.st_mode):
            raise BlueprintError(f"expected regular file: {label}")
        digest = hashlib.sha256()
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
        after = os.fstat(descriptor)
        if (
            observed.st_dev,
            observed.st_ino,
            observed.st_size,
            observed.st_mtime_ns,
        ) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
            raise BlueprintError(f"file changed while hashing: {label}")
        return FileExpectation(
            digest.hexdigest(),
            {
                "device": observed.st_dev,
                "inode": observed.st_ino,
                "size": observed.st_size,
                "mtime_ns": observed.st_mtime_ns,
                "mode": stat.S_IMODE(observed.st_mode),
            },
        )
    except OSError as exc:
        raise BlueprintError(f"cannot inspect expected regular file: {label}") from exc


def regular_file_expectation(path: Path) -> FileExpectation | None:
    if not path_lexists(path):
        return None
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        descriptor = os.open(path, flags)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise BlueprintError(f"cannot open expected regular file without following links: {path}") from exc
    try:
        return file_expectation_from_descriptor(descriptor, os.fspath(path))
    finally:
        os.close(descriptor)


def regular_file_expectation_at(directory_fd: int, name: str, label: str) -> FileExpectation | None:
    validate_path_component(name, label)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        descriptor = os.open(name, flags, dir_fd=directory_fd)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise BlueprintError(
            f"cannot open expected regular file without following links: {label}"
        ) from exc
    try:
        return file_expectation_from_descriptor(descriptor, label)
    finally:
        os.close(descriptor)


def validate_file_expectation(path: Path, expected: FileExpectation | None) -> None:
    observed = regular_file_expectation(path)
    if observed != expected:
        raise BlueprintError(
            f"compare-and-swap guard failed for {path.relative_to(ROOT)}: "
            f"expected {expected.sha256 if expected else 'absent'}, "
            f"observed {observed.sha256 if observed else 'absent'}"
        )


def write_new_synced_file(path: Path, content: bytes, mode: int = 0o644) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb", closefd=False) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(descriptor)


def validate_path_component(name: str, label: str) -> None:
    if (
        not isinstance(name, str)
        or name in {"", ".", ".."}
        or "/" in name
        or "\x00" in name
    ):
        raise BlueprintError(f"unsafe path component for {label}: {name!r}")


def write_new_synced_file_at(
    directory_fd: int, name: str, content: bytes, mode: int, label: str
) -> None:
    validate_path_component(name, label)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0)
    descriptor = os.open(name, flags, mode, dir_fd=directory_fd)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb", closefd=False) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(descriptor)


def open_anchored_repository_directory(path: Path) -> int:
    """Open a real repository directory one component at a time without links."""
    try:
        relative = path.relative_to(ROOT)
    except ValueError as exc:
        raise BlueprintError(f"directory escapes canonical repository: {path}") from exc
    flags = (
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0)
    )
    descriptor = os.open(ROOT, flags)
    try:
        for part in relative.parts:
            validate_path_component(part, os.fspath(path))
            child = os.open(part, flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def directory_identity(descriptor: int) -> tuple[int, int]:
    observed = os.fstat(descriptor)
    if not stat.S_ISDIR(observed.st_mode):
        raise BlueprintError("anchored transaction path is no longer a directory")
    return observed.st_dev, observed.st_ino


def validate_directory_anchor(path: Path, descriptor: int) -> None:
    comparison = open_anchored_repository_directory(path)
    try:
        if directory_identity(comparison) != directory_identity(descriptor):
            raise BlueprintError(f"anchored directory identity drift: {path.relative_to(ROOT)}")
    finally:
        os.close(comparison)


_RENAME_NOREPLACE = 1
_LIBC = ctypes.CDLL(None, use_errno=True)
_RENAMEAT2 = getattr(_LIBC, "renameat2", None)
if _RENAMEAT2 is not None:
    _RENAMEAT2.argtypes = (
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    )
    _RENAMEAT2.restype = ctypes.c_int


def rename_noreplace_at(
    source_directory_fd: int,
    source_name: str,
    destination_directory_fd: int,
    destination_name: str,
) -> None:
    """Atomically move one anchored entry only when the destination is absent."""
    validate_path_component(source_name, "rename source")
    validate_path_component(destination_name, "rename destination")
    if _RENAMEAT2 is None:
        raise BlueprintError("renameat2(RENAME_NOREPLACE) is unavailable; unsafe fallback refused")
    ctypes.set_errno(0)
    result = _RENAMEAT2(
        source_directory_fd,
        os.fsencode(source_name),
        destination_directory_fd,
        os.fsencode(destination_name),
        _RENAME_NOREPLACE,
    )
    if result == 0:
        return
    error = ctypes.get_errno()
    if error in {errno.ENOSYS, errno.EINVAL, errno.EOPNOTSUPP}:
        raise BlueprintError(
            "renameat2(RENAME_NOREPLACE) is unsupported on this transaction surface; "
            "unsafe fallback refused"
        )
    raise OSError(error, os.strerror(error), destination_name)


def atomic_write(path: Path, content: bytes) -> None:
    """Safely replace one Docs file; multi-output commands use atomic_batch_write."""
    validate_output_path(path)
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temp_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        fsync_directory(path.parent)
    finally:
        if path_lexists(temporary):
            temporary.unlink()


# Retained as the independently tested single-output primitive; all authority
# transitions use atomic_batch_write so related Blueprint/Gantt/receipt bytes
# share one recovery manifest.


def transaction_manifest_path(transaction: Path) -> Path:
    return transaction / "manifest.json"


def write_transaction_manifest(transaction: Path, value: dict[str, Any]) -> None:
    target = transaction_manifest_path(transaction)
    temporary = transaction / "manifest.next"
    if path_lexists(temporary):
        raise BlueprintError(f"unexpected transaction manifest temporary: {temporary}")
    write_new_synced_file(temporary, canonical(value) + b"\n", 0o600)
    os.replace(temporary, target)
    fsync_directory(transaction)


def cleanup_transaction(transaction: Path) -> None:
    if transaction.parent != DOCS or not transaction.name.startswith(BOOTSTRAP_TRANSACTION_PREFIX):
        raise BlueprintError(f"refusing to clean unexpected transaction directory: {transaction}")
    allowed = re.compile(r"(?:manifest\.json|manifest\.next|new-[0-9]{2}\.bin|old-[0-9]{2}\.bin)")
    children = list(transaction.iterdir())
    for child in children:
        if not allowed.fullmatch(child.name):
            raise BlueprintError(f"refusing to delete unexpected transaction entry: {child}")
        if not (child.is_symlink() or child.is_file()):
            raise BlueprintError(f"refusing to delete non-file transaction entry: {child}")
    for child in sorted(children, key=lambda value: value.name == "manifest.json"):
        child.unlink()
    transaction.rmdir()
    fsync_directory(DOCS)


def transaction_allowed_destinations() -> set[str]:
    destinations = {
        path.relative_to(ROOT).as_posix()
        for program in (THEOREM, CONJECTURE)
        for path in (program.blueprint, program.gantt)
    }
    destinations.update(
        boot_receipt_paths(program)[3].relative_to(ROOT).as_posix()
        for program in (THEOREM, CONJECTURE)
    )
    destinations.update(
        boot_receipt_paths(program)[1].relative_to(ROOT).as_posix()
        for program in (THEOREM, CONJECTURE)
    )
    destinations.update(
        (DOCS / "evidence" / f"stage5_{program.kind}s" / "execution-spec.json")
        .relative_to(ROOT)
        .as_posix()
        for program in (THEOREM, CONJECTURE)
    )
    destinations.add(OBJECT_WORKER_V2_MIGRATION_RECEIPT.relative_to(ROOT).as_posix())
    destinations.update(
        path.relative_to(ROOT).as_posix()
        for path in program_isolation_migration_receipts()
    )
    destinations.add(next_program_isolation_migration_receipt().relative_to(ROOT).as_posix())
    destinations.update(
        path.relative_to(ROOT).as_posix()
        for path in lifecycle_migration_receipts()
    )
    destinations.add(next_lifecycle_migration_receipt().relative_to(ROOT).as_posix())
    destinations.update(
        path.relative_to(ROOT).as_posix()
        for path in conjecture_prompt_policy_migration_receipts()
    )
    destinations.add(next_conjecture_prompt_policy_migration_receipt().relative_to(ROOT).as_posix())
    destinations.add(
        (DOCS / "evidence/stage5_conjectures/pool-expansion-migration-v1.json")
        .relative_to(ROOT)
        .as_posix()
    )
    destinations.add(
        (DOCS / "evidence/stage5_conjectures/pool-expansion-correction-v2.json")
        .relative_to(ROOT)
        .as_posix()
    )
    destinations.add(
        (DOCS / "evidence/stage5_conjectures/pool-expansion-correction-v3.json")
        .relative_to(ROOT)
        .as_posix()
    )
    destinations.add(
        (DOCS / "evidence/stage5_conjectures/pool-expansion-correction-v4.json")
        .relative_to(ROOT)
        .as_posix()
    )
    destinations.add(
        (DOCS / "evidence/stage5_conjectures/pool-expansion-correction-v5.json")
        .relative_to(ROOT)
        .as_posix()
    )
    destinations.add(
        (DOCS / "evidence/stage5_conjectures/pool-expansion-correction-v6.json")
        .relative_to(ROOT)
        .as_posix()
    )
    destinations.add(
        (DOCS / "evidence/stage5_conjectures/pool-expansion-correction-v7.json")
        .relative_to(ROOT)
        .as_posix()
    )
    for filename in (
        "workset-5.6.json",
        "workset-5.6-receipt.json",
        "claim-card.schema.json",
        "worker-result.schema.json",
        "master-acceptance.schema.json",
        "foundation-profiles.json",
        "provider-registry.json",
        "execution/concurrency-prompt.json",
    ):
        destinations.add((DOCS / "evidence/stage5_conjectures" / filename).relative_to(ROOT).as_posix())
    return destinations


def transaction_destination_allowed(destination: Any, allowed: set[str]) -> bool:
    """Admit only exact static outputs or closed content-addressed receipt shapes."""
    if destination in allowed:
        return True
    if not isinstance(destination, str):
        return False
    return any(re.fullmatch(pattern, destination) is not None for pattern in (
        r"Docs/evidence/stage5_conjectures/execution/transitions/"
        r"S5CON-(?:[0-9]{8}-TARGET|POOL-[0-9]{8}-INTAKE)/[0-9a-f]{64}\.json",
        r"Docs/evidence/stage5_conjectures/execution/acceptances/"
        r"S5CON-(?:[0-9]{8}-TARGET|POOL-[0-9]{8}-INTAKE)/"
        r"[0-9a-f]{64}/[0-9a-f]{64}/[0-9a-f]{64}\.json",
    ))


def conjecture_item_owned_destinations(item_id: str) -> set[str]:
    """Return the exact immutable owned-path allowlist for one execution member."""
    if re.fullmatch(
        r"S5CON-(?:[0-9]{8}-TARGET|POOL-[0-9]{8}-INTAKE)", item_id
    ) is None:
        raise BlueprintError(f"unsupported conjecture integration item ID: {item_id!r}")
    matches = [task for task in expected_tasks(CONJECTURE) if task.item_id == item_id]
    if len(matches) != 1 or not matches[0].owned_paths:
        raise BlueprintError(f"conjecture integration ownership is missing: {item_id}")
    return set(matches[0].owned_paths)


def manifest_expectation(sha: Any, identity: Any, label: str) -> FileExpectation | None:
    if sha is None and identity is None:
        return None
    required = {"device", "inode", "size", "mtime_ns", "mode"}
    if (
        not isinstance(sha, str)
        or not SHA256_RE.fullmatch(sha)
        or not isinstance(identity, dict)
        or set(identity) != required
        or any(not isinstance(identity[key], int) or identity[key] < 0 for key in required)
    ):
        raise BlueprintError(f"invalid {label} file expectation")
    return FileExpectation(sha, identity)


def validate_transaction_manifest(
    transaction: Path,
    *,
    additional_allowed_destinations: set[str] | frozenset[str] = frozenset(),
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manifest_path = transaction_manifest_path(transaction)
    manifest = strict_json_loads(manifest_path.read_bytes(), "batch transaction manifest")
    if (
        not isinstance(manifest, dict)
        or set(manifest) != {"schema_version", "phase", "outputs"}
        or manifest.get("schema_version") != "awesome-theorems/stage5-output-transaction/1.1"
        or manifest.get("phase") not in {"staging", "prepared", "committed"}
        or not isinstance(manifest.get("outputs"), list)
        or not 1 <= len(manifest["outputs"]) <= 64
    ):
        raise BlueprintError(f"malformed batch transaction manifest: {transaction}")
    rows = manifest["outputs"]
    allowed_destinations = transaction_allowed_destinations() | set(additional_allowed_destinations)
    seen_destinations: set[str] = set()
    expected_names = {"manifest.json", "manifest.next"}
    required_row_keys = {
        "destination",
        "staged_name",
        "backup_name",
        "old_sha256",
        "old_stat",
        "new_sha256",
        "new_stat",
    }
    for index, row in enumerate(rows):
        staged_name = f"new-{index:02d}.bin"
        backup_name = f"old-{index:02d}.bin"
        if (
            not isinstance(row, dict)
            or set(row) != required_row_keys
            or not transaction_destination_allowed(row.get("destination"), allowed_destinations)
            or row.get("destination") in seen_destinations
            or row.get("staged_name") != staged_name
            or row.get("backup_name") != backup_name
            or not isinstance(row.get("new_sha256"), str)
            or not SHA256_RE.fullmatch(row["new_sha256"])
        ):
            raise BlueprintError(f"unsafe batch transaction row {index}: {transaction}")
        manifest_expectation(row.get("old_sha256"), row.get("old_stat"), "old")
        if row.get("new_stat") is not None:
            manifest_expectation(row["new_sha256"], row["new_stat"], "new")
        elif manifest["phase"] != "staging":
            raise BlueprintError(f"non-staging transaction lacks new stat identity: {transaction}")
        seen_destinations.add(row["destination"])
        expected_names.update((staged_name, backup_name))
    children = list(transaction.iterdir())
    for child in children:
        if child.name not in expected_names:
            raise BlueprintError(f"unexpected transaction entry: {child}")
        if not (child.is_file() and not child.is_symlink()):
            raise BlueprintError(f"transaction entry is not a regular file: {child}")
    return manifest, rows


@dataclass
class LiveTransactionRow:
    manifest: dict[str, Any]
    destination: Path
    destination_directory_fd: int
    destination_name: str
    old: FileExpectation | None
    new: FileExpectation | None = None
    stage_present: bool = False
    backup_present: bool = False
    captured: bool = False
    capture_verified: bool = False
    published: bool = False


@dataclass
class LiveTransaction:
    name: str
    path: Path
    docs_directory_fd: int
    transaction_directory_fd: int
    rows: list[LiveTransactionRow]
    manifest_expectation: FileExpectation | None = None
    phase: str = "staging"
    cleaned: bool = False


def create_live_transaction(
    docs_directory_fd: int, rows: list[LiveTransactionRow]
) -> LiveTransaction:
    flags = (
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0)
    )
    for _ in range(128):
        name = f"{BOOTSTRAP_TRANSACTION_PREFIX}{secrets.token_hex(16)}"
        try:
            os.mkdir(name, 0o700, dir_fd=docs_directory_fd)
        except FileExistsError:
            continue
        transaction_directory_fd = os.open(name, flags, dir_fd=docs_directory_fd)
        observed = os.fstat(transaction_directory_fd)
        bound = os.stat(name, dir_fd=docs_directory_fd, follow_symlinks=False)
        if (
            not stat.S_ISDIR(observed.st_mode)
            or (observed.st_dev, observed.st_ino) != (bound.st_dev, bound.st_ino)
            or observed.st_uid != os.geteuid()
            or stat.S_IMODE(observed.st_mode) != 0o700
            or os.listdir(transaction_directory_fd)
        ):
            os.close(transaction_directory_fd)
            raise BlueprintError("new output transaction directory identity drift")
        os.fsync(docs_directory_fd)
        return LiveTransaction(
            name,
            DOCS / name,
            docs_directory_fd,
            transaction_directory_fd,
            rows,
        )
    raise BlueprintError("cannot allocate a unique output transaction directory")


def write_live_transaction_manifest(live: LiveTransaction, value: dict[str, Any]) -> None:
    temporary_name = "manifest.next"
    target_name = "manifest.json"
    if regular_file_expectation_at(
        live.transaction_directory_fd,
        temporary_name,
        f"{live.path.relative_to(ROOT)}/{temporary_name}",
    ) is not None:
        raise BlueprintError(f"unexpected transaction manifest temporary: {live.path / temporary_name}")
    content = canonical(value) + b"\n"
    write_new_synced_file_at(
        live.transaction_directory_fd,
        temporary_name,
        content,
        0o600,
        f"{live.path.relative_to(ROOT)}/{temporary_name}",
    )
    os.replace(
        temporary_name,
        target_name,
        src_dir_fd=live.transaction_directory_fd,
        dst_dir_fd=live.transaction_directory_fd,
    )
    os.fsync(live.transaction_directory_fd)
    observed = regular_file_expectation_at(
        live.transaction_directory_fd,
        target_name,
        f"{live.path.relative_to(ROOT)}/{target_name}",
    )
    if observed is None or observed.sha256 != sha256_bytes(content):
        raise BlueprintError(f"transaction manifest verification failed: {live.path}")
    live.manifest_expectation = observed


def fsync_live_transaction_directories(live: LiveTransaction) -> None:
    for row in live.rows:
        os.fsync(row.destination_directory_fd)
    os.fsync(live.transaction_directory_fd)


def validate_live_destination(
    row: LiveTransactionRow, expected: FileExpectation | None
) -> None:
    observed = regular_file_expectation_at(
        row.destination_directory_fd,
        row.destination_name,
        row.destination.relative_to(ROOT).as_posix(),
    )
    if observed != expected:
        raise BlueprintError(
            f"compare-and-swap guard failed for {row.destination.relative_to(ROOT)}: "
            f"expected {expected.sha256 if expected else 'absent'}, "
            f"observed {observed.sha256 if observed else 'absent'}"
        )


def cleanup_live_transaction(live: LiveTransaction) -> None:
    if live.cleaned:
        return
    expected_entries: dict[str, FileExpectation] = {}
    if live.manifest_expectation is not None:
        expected_entries["manifest.json"] = live.manifest_expectation
    for row in live.rows:
        if row.stage_present:
            if row.new is None:
                raise BlueprintError("live transaction lost staged-output identity")
            expected_entries[row.manifest["staged_name"]] = row.new
        if row.backup_present:
            if row.old is None or not row.capture_verified:
                raise BlueprintError("refusing to clean an unverified transaction backup")
            expected_entries[row.manifest["backup_name"]] = row.old
    observed_names = set(os.listdir(live.transaction_directory_fd))
    if observed_names != set(expected_entries):
        raise BlueprintError(
            f"live output transaction entry drift; explicit operator recovery required: {live.path}"
        )
    for name, expected in expected_entries.items():
        observed = regular_file_expectation_at(
            live.transaction_directory_fd,
            name,
            f"{live.path.relative_to(ROOT)}/{name}",
        )
        if observed != expected:
            raise BlueprintError(
                f"live output transaction identity drift; explicit operator recovery required: "
                f"{live.path / name}"
            )
    for name in sorted(expected_entries, key=lambda value: value == "manifest.json"):
        os.unlink(name, dir_fd=live.transaction_directory_fd)
    os.fsync(live.transaction_directory_fd)
    observed_directory = os.fstat(live.transaction_directory_fd)
    try:
        bound_directory = os.stat(
            live.name, dir_fd=live.docs_directory_fd, follow_symlinks=False
        )
    except FileNotFoundError as exc:
        raise BlueprintError(
            f"live output transaction pathname disappeared; explicit operator recovery required: "
            f"{live.path}"
        ) from exc
    if (
        not stat.S_ISDIR(bound_directory.st_mode)
        or (bound_directory.st_dev, bound_directory.st_ino)
        != (observed_directory.st_dev, observed_directory.st_ino)
    ):
        raise BlueprintError(
            f"live output transaction pathname identity drift; explicit operator recovery required: "
            f"{live.path}"
        )
    os.rmdir(live.name, dir_fd=live.docs_directory_fd)
    os.fsync(live.docs_directory_fd)
    live.cleaned = True


def rollback_live_transaction(live: LiveTransaction) -> None:
    """Undo only mutations proved by this process's in-memory transaction state."""
    if live.phase == "committed":
        raise BlueprintError("refusing to roll back a committed live transaction")
    failures: list[str] = []
    for row in reversed(live.rows):
        row_failed = False
        if row.published:
            try:
                observed_destination = regular_file_expectation_at(
                    row.destination_directory_fd,
                    row.destination_name,
                    row.destination.relative_to(ROOT).as_posix(),
                )
                if observed_destination == row.new:
                    if row.stage_present or regular_file_expectation_at(
                        live.transaction_directory_fd,
                        row.manifest["staged_name"],
                        f"{live.path.relative_to(ROOT)}/{row.manifest['staged_name']}",
                    ) is not None:
                        raise BlueprintError("staged rollback slot is unexpectedly occupied")
                    rename_noreplace_at(
                        row.destination_directory_fd,
                        row.destination_name,
                        live.transaction_directory_fd,
                        row.manifest["staged_name"],
                    )
                    row.published = False
                    row.stage_present = True
                    observed_stage = regular_file_expectation_at(
                        live.transaction_directory_fd,
                        row.manifest["staged_name"],
                        f"{live.path.relative_to(ROOT)}/{row.manifest['staged_name']}",
                    )
                    if observed_stage != row.new:
                        raise BlueprintError("published output changed while being quarantined")
                elif observed_destination is None:
                    row.published = False
                else:
                    if row.stage_present or regular_file_expectation_at(
                        live.transaction_directory_fd,
                        row.manifest["staged_name"],
                        f"{live.path.relative_to(ROOT)}/{row.manifest['staged_name']}",
                    ) is not None:
                        raise BlueprintError(
                            "published destination has unknown concurrent bytes and no empty "
                            "quarantine slot"
                        )
                    rename_noreplace_at(
                        row.destination_directory_fd,
                        row.destination_name,
                        live.transaction_directory_fd,
                        row.manifest["staged_name"],
                    )
                    row.published = False
                    row.stage_present = True
                    failures.append(
                        f"{row.destination.relative_to(ROOT)}: published destination had "
                        "unknown concurrent bytes; bytes quarantined without overwrite"
                    )
            except BaseException as exc:
                failures.append(f"{row.destination.relative_to(ROOT)}: {exc}")
                row_failed = True
        if row.captured and not row_failed:
            try:
                if not row.capture_verified or row.old is None:
                    raise BlueprintError("captured destination backup was never verified")
                observed_backup = regular_file_expectation_at(
                    live.transaction_directory_fd,
                    row.manifest["backup_name"],
                    f"{live.path.relative_to(ROOT)}/{row.manifest['backup_name']}",
                )
                observed_destination = regular_file_expectation_at(
                    row.destination_directory_fd,
                    row.destination_name,
                    row.destination.relative_to(ROOT).as_posix(),
                )
                if observed_backup != row.old:
                    raise BlueprintError("trusted rollback backup identity drift")
                if observed_destination is not None:
                    raise BlueprintError("rollback destination is occupied")
                rename_noreplace_at(
                    live.transaction_directory_fd,
                    row.manifest["backup_name"],
                    row.destination_directory_fd,
                    row.destination_name,
                )
                row.backup_present = False
                row.captured = False
                validate_live_destination(row, row.old)
            except BaseException as exc:
                failures.append(f"{row.destination.relative_to(ROOT)}: {exc}")
                row_failed = True
        if not row_failed:
            try:
                validate_live_destination(row, row.old)
                validate_directory_anchor(row.destination.parent, row.destination_directory_fd)
            except BaseException as exc:
                failures.append(f"{row.destination.relative_to(ROOT)}: {exc}")
    try:
        fsync_live_transaction_directories(live)
    except BaseException as exc:
        failures.append(f"directory fsync: {exc}")
    if failures:
        raise BlueprintError(
            "safe automatic rollback stopped without overwriting unknown state; "
            f"journal retained at {live.path}: " + "; ".join(failures)
        )


def close_live_transaction(live: LiveTransaction) -> None:
    for row in live.rows:
        try:
            os.close(row.destination_directory_fd)
        except OSError:
            pass
    try:
        os.close(live.transaction_directory_fd)
    except OSError:
        pass
    try:
        os.close(live.docs_directory_fd)
    except OSError:
        pass


def recover_one_transaction(transaction: Path) -> None:
    del transaction
    raise BlueprintError(
        "path-based output transaction recovery is forbidden; "
        "explicit operator recovery is required"
    )


def recover_batch_transactions() -> None:
    validate_canonical_root()
    transaction_allowed_destinations()
    pending = sorted(DOCS.glob(f"{BOOTSTRAP_TRANSACTION_PREFIX}*"))
    if pending:
        raise BlueprintError(
            "untrusted/incomplete output transaction requires explicit operator recovery; "
            f"automatic replay is forbidden: {pending[0]}"
        )


def atomic_batch_write(
    outputs: list[tuple[Path, bytes]],
    *,
    expected_old: dict[Path, FileExpectation | None] | None = None,
    guards: dict[Path, FileExpectation | None] | None = None,
    precommit_validator: Any = None,
    additional_allowed_destinations: set[str] | frozenset[str] = frozenset(),
) -> None:
    if not outputs or len(outputs) > 64 or len({path for path, _ in outputs}) != len(outputs):
        raise BlueprintError("batch outputs must be nonempty and destination-unique")
    def validate_batch_destination(path: Path) -> None:
        try:
            relative = path.relative_to(ROOT).as_posix()
        except ValueError as exc:
            raise BlueprintError(f"batch output escapes repository: {path}") from exc
        if relative in additional_allowed_destinations:
            validate_guard_path(path)
            if not path.parent.is_dir() or path.parent.is_symlink():
                raise BlueprintError(f"batch output parent is not a real directory: {path.parent}")
            if not os.access(path.parent, os.W_OK | os.X_OK):
                raise BlueprintError(f"batch output parent is not writable/searchable: {path.parent}")
        else:
            validate_output_path(path)

    for path, _ in outputs:
        validate_batch_destination(path)
    allowed_destinations = transaction_allowed_destinations()
    for destination in additional_allowed_destinations:
        if (
            not isinstance(destination, str)
            or canonical_repo_relative_path(destination, "additional transaction destination")[0]
            != destination
            or not destination.startswith((
                "Stage5_Conjecture_Instances/",
                "Stage5_Conjecture_Pool_Intake/",
                "Formalizations/Lean/AwesomeTheorems/Stage5/Conjectures/",
            ))
        ):
            raise BlueprintError(f"unsafe additional transaction destination: {destination!r}")
    allowed_destinations.update(additional_allowed_destinations)
    for path, _ in outputs:
        destination = path.relative_to(ROOT).as_posix()
        if not transaction_destination_allowed(destination, allowed_destinations):
            raise BlueprintError(f"batch output destination is not allowlisted: {destination}")
    if expected_old is None:
        expected_old = {path: regular_file_expectation(path) for path, _ in outputs}
    if set(expected_old) != {path for path, _ in outputs}:
        raise BlueprintError("batch old-byte expectations do not cover exact outputs")
    guards = guards or {}
    for path, expectation in expected_old.items():
        validate_batch_destination(path)
        validate_file_expectation(path, expectation)
    for path, expectation in guards.items():
        validate_guard_path(path)
        validate_file_expectation(path, expectation)
    docs_directory_fd: int | None = None
    opened_rows: list[LiveTransactionRow] = []
    live: LiveTransaction | None = None
    try:
        docs_directory_fd = open_anchored_repository_directory(DOCS)
        for index, (path, content) in enumerate(outputs):
            staged_name = f"new-{index:02d}.bin"
            backup_name = f"old-{index:02d}.bin"
            old = expected_old[path]
            parent_fd = open_anchored_repository_directory(path.parent)
            opened_rows.append(
                LiveTransactionRow(
                    {
                    "destination": path.relative_to(ROOT).as_posix(),
                    "staged_name": staged_name,
                    "backup_name": backup_name,
                    "old_sha256": old.sha256 if old else None,
                    "old_stat": old.stat_identity if old else None,
                    "new_sha256": sha256_bytes(content),
                    "new_stat": None,
                    },
                    path,
                    parent_fd,
                    path.name,
                    old,
                )
            )
        live = create_live_transaction(docs_directory_fd, opened_rows)
        docs_directory_fd = None
        rows = [row.manifest for row in live.rows]
        manifest = {
            "schema_version": "awesome-theorems/stage5-output-transaction/1.1",
            "phase": "staging",
            "outputs": rows,
        }
        write_live_transaction_manifest(live, manifest)
        validate_transaction_manifest(
            live.path,
            additional_allowed_destinations=additional_allowed_destinations,
        )
        for row, (_, content) in zip(live.rows, outputs):
            write_new_synced_file_at(
                live.transaction_directory_fd,
                row.manifest["staged_name"],
                content,
                0o644,
                f"{live.path.relative_to(ROOT)}/{row.manifest['staged_name']}",
            )
            row.stage_present = True
            observed = regular_file_expectation_at(
                live.transaction_directory_fd,
                row.manifest["staged_name"],
                f"{live.path.relative_to(ROOT)}/{row.manifest['staged_name']}",
            )
            if observed is None or observed.sha256 != row.manifest["new_sha256"]:
                raise BlueprintError(f"staged output verification failed: {live.path}")
            row.new = observed
            row.manifest["new_stat"] = observed.stat_identity
        manifest["phase"] = "prepared"
        live.phase = "prepared"
        write_live_transaction_manifest(live, manifest)
        validate_transaction_manifest(
            live.path,
            additional_allowed_destinations=additional_allowed_destinations,
        )
        if precommit_validator is not None:
            precommit_validator()
        for path, expectation in {**expected_old, **guards}.items():
            validate_file_expectation(path, expectation)
        for row in live.rows:
            validate_directory_anchor(row.destination.parent, row.destination_directory_fd)
            if row.old is not None:
                rename_noreplace_at(
                    row.destination_directory_fd,
                    row.destination_name,
                    live.transaction_directory_fd,
                    row.manifest["backup_name"],
                )
                row.captured = True
                row.backup_present = True
                observed_backup = regular_file_expectation_at(
                    live.transaction_directory_fd,
                    row.manifest["backup_name"],
                    f"{live.path.relative_to(ROOT)}/{row.manifest['backup_name']}",
                )
                if observed_backup != row.old:
                    raise BlueprintError(
                        f"compare-and-swap captured unexpected bytes for "
                        f"{row.destination.relative_to(ROOT)}"
                    )
                row.capture_verified = True
        fsync_live_transaction_directories(live)
        for path, expectation in guards.items():
            validate_file_expectation(path, expectation)
        for row in live.rows:
            if row.new is None or not row.stage_present:
                raise BlueprintError("live transaction lost its staged output")
            rename_noreplace_at(
                live.transaction_directory_fd,
                row.manifest["staged_name"],
                row.destination_directory_fd,
                row.destination_name,
            )
            row.stage_present = False
            row.published = True
            validate_live_destination(row, row.new)
        fsync_live_transaction_directories(live)
        for path, expectation in guards.items():
            validate_file_expectation(path, expectation)
        for row in live.rows:
            validate_live_destination(row, row.new)
            validate_directory_anchor(row.destination.parent, row.destination_directory_fd)
            validate_file_expectation(row.destination, row.new)
        manifest["phase"] = "committed"
        write_live_transaction_manifest(live, manifest)
        validate_transaction_manifest(
            live.path,
            additional_allowed_destinations=additional_allowed_destinations,
        )
        live.phase = "committed"
        cleanup_live_transaction(live)
    except BaseException as original:
        if live is not None and not live.cleaned and live.phase != "committed":
            try:
                rollback_live_transaction(live)
                cleanup_live_transaction(live)
            except BaseException as rollback_error:
                raise BlueprintError(
                    f"batch mutation failed ({original}); {rollback_error}"
                ) from rollback_error
        raise
    finally:
        if live is not None:
            close_live_transaction(live)
        else:
            for row in opened_rows:
                try:
                    os.close(row.destination_directory_fd)
                except OSError:
                    pass
            if docs_directory_fd is not None:
                os.close(docs_directory_fd)


def select_programs(value: str) -> tuple[Program, ...]:
    if value == "all":
        return (THEOREM, CONJECTURE)
    return (THEOREM if value == "theorem" else CONJECTURE,)


def read_user_crontab() -> str:
    if CANONICAL_CRONTAB.is_symlink() or not CANONICAL_CRONTAB.is_file():
        raise BlueprintError("canonical crontab executable is unavailable")
    try:
        completed = subprocess.run(
            [CANONICAL_CRONTAB.as_posix(), "-l"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
            env=BOOT_COMMAND_ENV,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        raise BlueprintError("cannot establish existing cron marker state") from exc
    if completed.returncode == 0:
        return completed.stdout
    combined = (completed.stdout + "\n" + completed.stderr).lower()
    if completed.returncode == 1 and "no crontab for" in combined:
        return ""
    raise BlueprintError(f"cannot read existing user crontab (exit {completed.returncode})")


def sealed_boot_document(path: Path, required_fields: set[str], label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise BlueprintError(f"{label}: missing regular sealed document {path.relative_to(ROOT)}")
    value = strict_json_loads(path.read_bytes(), label)
    if not isinstance(value, dict) or set(value) != required_fields | {"authority_sha256"}:
        raise BlueprintError(f"{label}: closed fields differ")
    authority = value.get("authority_sha256")
    unsigned = dict(value)
    del unsigned["authority_sha256"]
    if (
        not isinstance(authority, str)
        or not SHA256_RE.fullmatch(authority)
        or sha256_bytes(canonical(unsigned)) != authority
    ):
        raise BlueprintError(f"{label}: canonical authority seal mismatch")
    return value


def process_start_ticks(pid: int) -> int | None:
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 1:
        return None
    try:
        raw = (Path("/proc") / str(pid) / "stat").read_text(encoding="utf-8")
        right = raw.rfind(")")
        if right < 0:
            return None
        return int(raw[right + 2 :].split()[19])
    except (OSError, ValueError, IndexError):
        return None


def process_effective_uid(pid: int) -> int | None:
    try:
        for line in (Path("/proc") / str(pid) / "status").read_text(encoding="utf-8").splitlines():
            if line.startswith("Uid:"):
                return int(line.split()[2])
    except (OSError, ValueError, IndexError):
        return None
    return None


def process_command(pid: int) -> list[str] | None:
    try:
        raw = (Path("/proc") / str(pid) / "cmdline").read_bytes()
        return [part.decode("utf-8") for part in raw.split(b"\0") if part]
    except (OSError, UnicodeDecodeError):
        return None


def process_environment_value(pid: int, name: str) -> str | None:
    try:
        raw = (Path("/proc") / str(pid) / "environ").read_bytes()
        prefix = name.encode("utf-8") + b"="
        matches = [part[len(prefix) :] for part in raw.split(b"\0") if part.startswith(prefix)]
        if len(matches) != 1:
            return None
        return matches[0].decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def regular_file_bytes(path: Path, label: str) -> tuple[bytes, FileExpectation]:
    expectation = regular_file_expectation(path)
    if expectation is None:
        raise BlueprintError(f"{label}: missing regular file")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        data = bytearray()
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            data.extend(chunk)
        after = os.fstat(descriptor)
        observed = FileExpectation(
            sha256_bytes(bytes(data)),
            {
                "device": after.st_dev,
                "inode": after.st_ino,
                "size": after.st_size,
                "mtime_ns": after.st_mtime_ns,
                "mode": stat.S_IMODE(after.st_mode),
            },
        )
        if observed != expectation:
            raise BlueprintError(f"{label}: changed while reading")
        return bytes(data), observed
    finally:
        os.close(descriptor)


def boot_evidence_root(program: Program) -> Path:
    return DOCS / "evidence" / f"stage5_{program.kind}s"


def boot_authority_epoch_root(program: Program) -> Path:
    """Return the append-only BOOT receipt namespace for this authority epoch.

    The theorem program keeps its published legacy namespace.  Conjecture pool
    successors must not overwrite or reinterpret historical BOOT receipts, so
    every successor runtime authority gets a disjoint receipt root.
    """

    if program.kind == "conjecture":
        return (
            boot_evidence_root(program)
            / "bootstrap"
            / "epochs"
            / CONJECTURE_RUNTIME_AUTHORITY_EPOCH
        )
    return boot_evidence_root(program)


def boot_review_archive_root(program: Program) -> Path:
    if program.kind == "conjecture":
        return boot_authority_epoch_root(program) / "reviews"
    return boot_evidence_root(program) / "bootstrap" / "reviews"


def boot_trust_root_path(program: Program) -> Path:
    return boot_evidence_root(program) / BOOT_ROLE_TRUST_ROOT_NAME


def boot_trust_keys(program: Program) -> tuple[dict[str, dict[str, Any]], FileExpectation]:
    path = boot_trust_root_path(program)
    raw, guard = regular_file_bytes(path, "BOOT role trust root")
    if set(BOOT_ROLE_TRUST_ROOT_SHA256) != {"theorem", "conjecture"}:
        raise BlueprintError("BOOT role trust-root pin map is malformed")
    expected_pin = BOOT_ROLE_TRUST_ROOT_SHA256.get(program.kind)
    if expected_pin is None or guard.sha256 != expected_pin:
        raise BlueprintError(
            f"BOOT {program.kind} role trust root is not pinned by this reviewed manager; "
            "this external pre-controller TCB remains blocked until a reviewed "
            "manager/specification migration freezes its exact program-specific SHA-256"
        )
    value = strict_json_loads(raw, "BOOT role trust root")
    if (
        not isinstance(value, dict)
        or set(value) != {"schema_version", "program", "signature_algorithm", "keys", "authority_sha256"}
        or value.get("schema_version") != BOOT_TRUST_ROOT_SCHEMA
        or value.get("program") != program.version
        or value.get("signature_algorithm") != "Ed25519"
        or not isinstance(value.get("keys"), list)
        or len(value["keys"]) < 4
    ):
        raise BlueprintError("BOOT role trust root is malformed")
    unsigned = dict(value)
    authority = unsigned.pop("authority_sha256")
    if not isinstance(authority, str) or sha256_bytes(canonical(unsigned)) != authority:
        raise BlueprintError("BOOT role trust-root authority mismatch")
    records: dict[str, dict[str, Any]] = {}
    principals: set[str] = set()
    public_keys: set[str] = set()
    for row in value["keys"]:
        if (
            not isinstance(row, dict)
            or set(row) != {"key_id", "principal_id", "allowed_role", "public_key_hex", "status"}
            or row.get("allowed_role") not in {"producer", "reviewer", "master"}
            or row.get("status") != "active"
            or not isinstance(row.get("key_id"), str)
            or not BOOT_ID_RE.fullmatch(row["key_id"])
            or not isinstance(row.get("principal_id"), str)
            or not BOOT_ID_RE.fullmatch(row["principal_id"])
            or not isinstance(row.get("public_key_hex"), str)
            or not re.fullmatch(r"[0-9a-f]{64}", row["public_key_hex"])
            or row["key_id"] in records
            or row["principal_id"] in principals
            or row["public_key_hex"] in public_keys
        ):
            raise BlueprintError("BOOT role trust root has malformed or duplicated key")
        records[row["key_id"]] = row
        principals.add(row["principal_id"])
        public_keys.add(row["public_key_hex"])
    if {row["allowed_role"] for row in records.values()} != {"producer", "reviewer", "master"}:
        raise BlueprintError("BOOT role trust root lacks every required role")
    return records, guard


def validate_signed_boot_document(
    value: dict[str, Any], fields: set[str], schema: str, label: str,
    trust_keys: dict[str, dict[str, Any]], expected_role: str,
) -> str:
    if set(value) != fields or value.get("schema_version") != schema:
        raise BlueprintError(f"{label}: closed fields/schema differ")
    key = trust_keys.get(value.get("key_id"))
    if (
        key is None
        or key["allowed_role"] != expected_role
        or value.get("role") != expected_role
        or value.get("principal_id") != key["principal_id"]
        or value.get("signature_algorithm") != "Ed25519"
        or not isinstance(value.get("signature"), str)
        or not BOOT_SIGNATURE_RE.fullmatch(value["signature"])
    ):
        raise BlueprintError(f"{label}: role/key identity is unauthenticated")
    unsigned = dict(value)
    authority = unsigned.pop("authority_sha256", None)
    signature = unsigned.pop("signature", None)
    signed_sha = unsigned.pop("signed_payload_sha256", None)
    payload = canonical(unsigned)
    if (
        not isinstance(authority, str)
        or sha256_bytes(canonical({**unsigned, "signed_payload_sha256": signed_sha, "signature": signature})) != authority
        or signed_sha != sha256_bytes(payload)
    ):
        raise BlueprintError(f"{label}: signed payload/authority mismatch")
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(key["public_key_hex"])).verify(
            bytes.fromhex(signature), payload
        )
    except (ValueError, InvalidSignature) as exc:
        raise BlueprintError(f"{label}: signature is invalid") from exc
    return key["principal_id"]


def validate_boot_claim_card(
    path: Path, expected_sha: str, *, program: Program, role: str, claim_id: str,
    run_id: str, item_id: str, task_root: str, work_root: str,
) -> FileExpectation:
    raw, guard = regular_file_bytes(path, "BOOT claim card")
    if guard.sha256 != expected_sha:
        raise BlueprintError("BOOT claim-card digest mismatch")
    value = strict_json_loads(raw, "BOOT claim card")
    required = {
        "schema_version", "program", "role", "claim_id", "run_id", "item_id",
        "task_root", "work_root", "canonical_repository_root", "canonical_write_policy",
        "manager_sha256", "source_bundle_sha256", "execution_spec_sha256",
    }
    if (
        not isinstance(value, dict)
        or set(value) != required
        or value.get("schema_version") != BOOT_CLAIM_SCHEMA
        or value.get("program") != program.version
        or value.get("role") != role
        or value.get("claim_id") != claim_id
        or value.get("run_id") != run_id
        or value.get("item_id") != item_id
        or value.get("task_root") != task_root
        or value.get("work_root") != work_root
        or value.get("canonical_repository_root") != CANONICAL_ROOT.as_posix()
        or value.get("canonical_write_policy") != "forbidden"
        or value.get("manager_sha256") != manager_code_sha256()
        or value.get("source_bundle_sha256") != source_bundle_sha256(program)
        or value.get("execution_spec_sha256") != sha256_bytes(canonical(spec_object(program)))
    ):
        raise BlueprintError("BOOT claim card does not bind the exact claim/root/authority")
    return guard


def validate_boot_role_attestation(
    value: Any, *, program: Program, expected_role: str,
    trust_keys: dict[str, dict[str, Any]], label: str,
) -> tuple[str, dict[Path, FileExpectation]]:
    if not isinstance(value, dict):
        raise BlueprintError(f"{label}: role attestation is not an object")
    principal = validate_signed_boot_document(
        value, BOOT_ROLE_FIELDS, BOOT_ROLE_SCHEMA, label, trust_keys, expected_role
    )
    for field in ("claim_id", "run_id", "item_id"):
        if not isinstance(value.get(field), str) or not BOOT_ID_RE.fullmatch(value[field]):
            raise BlueprintError(f"{label}: invalid {field}")
    boot_item = f"{program.task_prefix}-BOOT-001"
    if (
        value["item_id"] != boot_item
        or value.get("program") != program.version
        or value.get("principal_context") not in {"external", "local"}
        or value.get("manager_sha256") != manager_code_sha256()
        or value.get("source_bundle_sha256") != source_bundle_sha256(program)
        or value.get("execution_spec_sha256") != sha256_bytes(canonical(spec_object(program)))
    ):
        raise BlueprintError(f"{label}: pre-controller program/item/authority binding failed")
    canonical_timestamp(value.get("observed_at"), f"{label} observed_at")
    return principal, {}


def boot_artifact_snapshot(
    program: Program, tasks: list[Task]
) -> tuple[dict[str, str], dict[Path, FileExpectation]]:
    boot = next(task for task in tasks if task.item_id == f"{program.task_prefix}-BOOT-001")
    result: dict[str, str] = {}
    guards: dict[Path, FileExpectation] = {}
    seen_inodes: set[tuple[int, int]] = set()
    for relative in boot.owned_paths:
        validate_repo_path(relative, boot.item_id)
        path = ROOT / relative
        if path_lexists(path):
            if path.is_symlink():
                raise BlueprintError(f"BOOT artifact is a symlink: {relative}")
            if path.is_file():
                raw, expectation = regular_file_bytes(path, f"BOOT artifact {relative}")
                identity = (expectation.stat_identity["device"], expectation.stat_identity["inode"])
                if identity in seen_inodes or os.stat(path, follow_symlinks=False).st_nlink != 1:
                    raise BlueprintError(f"BOOT artifact is duplicated/hardlinked: {relative}")
                seen_inodes.add(identity)
                result[relative] = sha256_bytes(raw)
                guards[path] = expectation
            elif path.is_dir():
                rows = []
                for child in sorted(path.rglob("*")):
                    if child.is_symlink() or not child.is_file():
                        raise BlueprintError(f"BOOT artifact tree has unsafe entry: {child}")
                    raw, expectation = regular_file_bytes(child, f"BOOT artifact {child.relative_to(ROOT)}")
                    identity = (expectation.stat_identity["device"], expectation.stat_identity["inode"])
                    if identity in seen_inodes or os.stat(child, follow_symlinks=False).st_nlink != 1:
                        raise BlueprintError(f"BOOT artifact is duplicated/hardlinked: {child}")
                    seen_inodes.add(identity)
                    rows.append(
                        [child.relative_to(path).as_posix(), expectation.stat_identity["mode"], sha256_bytes(raw)]
                    )
                    guards[child] = expectation
                if not rows:
                    raise BlueprintError(f"BOOT artifact tree is empty: {relative}")
                result[relative] = sha256_bytes(canonical(rows))
            else:
                raise BlueprintError(f"BOOT artifact is not regular file/tree: {relative}")
        else:
            raise BlueprintError(f"BOOT artifact is missing: {relative}")
    execution_spec_path = (
        DOCS / "evidence" / f"stage5_{program.kind}s" / "execution-spec.json"
    )
    observed_spec = strict_json_loads(
        regular_file_bytes(execution_spec_path, f"{program.kind} BOOT execution-spec")[0],
        f"{program.kind} BOOT execution-spec",
    )
    if observed_spec != spec_object(program):
        raise BlueprintError("BOOT execution-spec.json is not the exact canonical specification")
    for suffix in ("claim-card.schema.json", "worker-result.schema.json", "master-acceptance.schema.json"):
        schema_path = execution_spec_path.parent / suffix
        schema_raw, schema_guard = regular_file_bytes(schema_path, f"BOOT {suffix}")
        guards[schema_path] = schema_guard
        schema = strict_json_loads(schema_raw, f"BOOT {suffix}")
        if (
            not isinstance(schema, dict)
            or set(schema) != {"$schema", "$id", "type", "additionalProperties", "required", "properties"}
            or not isinstance(schema.get("$schema"), str)
            or schema["type"] != "object"
            or schema.get("additionalProperties") is not False
            or not isinstance(schema.get("required"), list)
            or not isinstance(schema.get("properties"), dict)
            or not schema["required"]
            or set(schema["required"]) != set(schema["properties"])
            or not isinstance(schema.get("$id"), str)
            or program.kind not in schema["$id"]
        ):
            raise BlueprintError(f"BOOT schema is not closed: {suffix}")
    return result, guards


def boot_artifact_bindings(program: Program, tasks: list[Task]) -> dict[str, str]:
    return boot_artifact_snapshot(program, tasks)[0]


def boot_receipt_paths(program: Program) -> tuple[Path, Path, Path, Path]:
    return tuple(ROOT / relative for relative in boot_receipt_contract_paths(program))


def boot_receipt_contract_paths(program: Program) -> tuple[str, str, str, str]:
    """Return stable spec paths independently of testable receipt I/O hooks."""

    root = DOCS / "evidence" / f"stage5_{program.kind}s"
    if program.kind == "conjecture":
        root = (
            root
            / "bootstrap"
            / "epochs"
            / CONJECTURE_RUNTIME_AUTHORITY_EPOCH
        )
    return tuple(
        (root / filename).relative_to(ROOT).as_posix()
        for filename in (
            "controller-bootstrap-handoff.json",
            "controller-bootstrap-handoff-acceptance.json",
            "controller-bootstrap-review.json",
            "controller-bootstrap-acceptance.json",
        )
    )


BOOT_HANDOFF_FIELDS = {
    "schema_version", "role", "principal_id", "key_id", "signature_algorithm",
    "status", "program", "boot_item_id", "manager_sha256", "source_bundle_sha256",
    "execution_spec_sha256", "task_dag_sha256", "blueprint_sha256",
    "gantt_sha256", "boot_task_authority_sha256", "artifact_bindings",
    "command_spec_sha256", "expected_command_results_sha256", "producer_attestation",
    "signed_payload_sha256", "signature", "authority_sha256",
}
BOOT_HANDOFF_ACCEPTANCE_FIELDS = {
    "schema_version", "status", "program", "boot_item_id",
    "handoff_authority_sha256", "producer_principal_id", "input_snapshot",
    "command_spec_sha256", "command_results", "pre_blueprint_sha256",
    "pre_gantt_sha256", "post_blueprint_sha256", "post_gantt_sha256",
    "authority_sha256",
}
BOOT_DECISION_FIELDS = {
    "schema_version", "role", "principal_id", "key_id", "signature_algorithm",
    "program", "boot_item_id", "handoff_acceptance_authority_sha256", "artifact_bindings",
    "reviewer_attestation", "decision", "conflicts", "passed_gates",
    "command_spec_sha256", "signed_payload_sha256", "signature", "authority_sha256",
}
BOOT_REVIEW_FIELDS = {
    "schema_version", "program", "boot_item_id", "handoff_acceptance_authority_sha256",
    "producer_principal_id", "master_attestation", "reviewer_decisions",
    "passed_gates", "command_spec_sha256", "expected_command_results_sha256",
    "artifact_bindings", "role", "principal_id", "key_id", "signature_algorithm",
    "signed_payload_sha256", "signature", "authority_sha256",
}


def sealed_boot_receipt(path: Path, fields: set[str], schema: str, label: str) -> tuple[dict[str, Any], FileExpectation]:
    raw, guard = regular_file_bytes(path, label)
    value = strict_json_loads(raw, label)
    if not isinstance(value, dict) or set(value) != fields or value.get("schema_version") != schema:
        raise BlueprintError(f"{label}: closed fields/schema differ")
    authority = value.get("authority_sha256")
    unsigned = dict(value)
    del unsigned["authority_sha256"]
    if not isinstance(authority, str) or not SHA256_RE.fullmatch(authority) or sha256_bytes(canonical(unsigned)) != authority:
        raise BlueprintError(f"{label}: canonical authority seal mismatch")
    return value, guard


def boot_input_snapshot(
    program: Program,
    *,
    artifact_bindings: dict[str, str],
    source_guards: dict[Path, FileExpectation],
    manager_guard: FileExpectation,
    trust_guard: FileExpectation,
    handoff_path: Path,
    handoff_guard: FileExpectation,
) -> dict[str, Any]:
    """Build the complete digest-only BOOT transition input snapshot."""
    return {
        "schema_version": "awesome-theorems/stage5-bootstrap-input-snapshot/1.0",
        "program": program.version,
        "manager_sha256": manager_guard.sha256,
        "source_inputs": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": guard.sha256}
            for path, guard in sorted(source_guards.items(), key=lambda row: row[0].as_posix())
        ],
        "artifact_bindings": artifact_bindings,
        "trust_root_path": boot_trust_root_path(program).relative_to(ROOT).as_posix(),
        "trust_root_sha256": trust_guard.sha256,
        "handoff_path": handoff_path.relative_to(ROOT).as_posix(),
        "handoff_sha256": handoff_guard.sha256,
    }


def validate_role_uniqueness(attestations: list[dict[str, Any]], principals: list[str]) -> None:
    if len(principals) != len(set(principals)):
        raise BlueprintError("BOOT role principals are not identity-distinct")
    for field in ("claim_id", "run_id"):
        values = [value[field] for value in attestations]
        if len(values) != len(set(values)):
            raise BlueprintError(f"BOOT role {field} identities overlap")


def validate_decision_path(
    program: Program, relative: Any, *, principal: str, receipt_sha: str,
) -> tuple[Path, FileExpectation]:
    normalized, path = canonical_repo_relative_path(relative, "BOOT reviewer decision")
    expected_prefix = (
        boot_review_archive_root(program) / principal
    ).relative_to(ROOT).as_posix() + "/"
    if not normalized.startswith(expected_prefix) or normalized != f"{expected_prefix}{receipt_sha}.json":
        raise BlueprintError("BOOT reviewer decision path is outside its canonical principal archive")
    _, guard = regular_file_bytes(path, "BOOT reviewer decision")
    if guard.sha256 != receipt_sha:
        raise BlueprintError("BOOT reviewer decision receipt digest mismatch")
    return path, guard


def executable_python_ast_audit(program: Program) -> None:
    controller_path = ROOT / f"scripts/stage5_{program.kind}s_execution_cron_v2.py"
    try:
        tree = ast.parse(controller_path.read_text(encoding="utf-8"), filename=str(controller_path))
    except (OSError, SyntaxError) as exc:
        raise BlueprintError("BOOT controller cannot be parsed for transport audit") from exc
    forbidden_literals = {
        "exec", "app-server", "app_server", "--model", "--reasoning-effort",
        "codex exec", "codex app-server",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            normalized = " ".join(node.value.lower().split())
            if normalized in forbidden_literals:
                raise BlueprintError(f"BOOT controller contains forbidden executable transport literal: {node.value!r}")
        if isinstance(node, ast.Call):
            name = ""
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                # Attribute names such as re.compile are ordinary reviewed
                # library calls.  Only an explicit builtins.eval/exec/compile
                # is the dynamic-code surface this gate intends to forbid.
                if (
                    isinstance(node.func.value, ast.Name)
                    and node.func.value.id in {"builtins", "__builtins__"}
                ):
                    name = node.func.attr
            if name in {"eval", "exec", "compile"}:
                raise BlueprintError(f"BOOT controller uses dynamic executable construction: {name}")


def boot_command_spec(program: Program) -> list[dict[str, Any]]:
    python = CANONICAL_PYTHON.resolve(strict=True)
    if CANONICAL_PYTHON.is_symlink() or python != Path("/usr/bin/python3.12") or not os.access(python, os.X_OK):
        raise BlueprintError("canonical Python interpreter drift")
    return [
        {
            "command_id": f"{program.kind}-{index:02d}",
            "argv": [python.as_posix(), "-I", "-B", *tail],
            "timeout_seconds": BOOT_COMMAND_TIMEOUT_SECONDS,
            "transport": "systemd_transient_service_landlock_seccomp",
            "candidate_cwd": "content-addressed-read-only-snapshot-root",
            "candidate_environment": "env-i with private Landlock HOME/TMP/XDG",
            "network": "AF_INET/AF_INET6 denied",
            "complete_output_bytes_per_channel_max": 16777216,
            "sandbox_path": BOOT_SANDBOX_PATH.relative_to(ROOT).as_posix(),
            "sandbox_sha256": BOOT_SANDBOX_SHA256,
            "declared_snapshot_inputs": list(boot_sandbox_inputs(program)),
        }
        for index, tail in enumerate(BOOT_COMMANDS[program.kind], start=1)
    ]


def load_boot_sandbox() -> Any:
    if BOOT_SANDBOX_PATH.is_symlink() or not BOOT_SANDBOX_PATH.is_file():
        raise BlueprintError("BOOT sandbox implementation is unavailable")
    raw = BOOT_SANDBOX_PATH.read_bytes()
    if sha256_bytes(raw) != BOOT_SANDBOX_SHA256:
        raise BlueprintError("BOOT sandbox implementation digest drift")
    module_spec = importlib.util.spec_from_file_location(
        "stage5_boot_command_sandbox_reviewed", BOOT_SANDBOX_PATH
    )
    if module_spec is None or module_spec.loader is None:
        raise BlueprintError("BOOT sandbox module cannot be loaded")
    module = importlib.util.module_from_spec(module_spec)
    try:
        module_spec.loader.exec_module(module)
    except Exception as exc:
        raise BlueprintError("BOOT sandbox module import failed") from exc
    return module


def boot_sandbox_inputs(program: Program) -> tuple[str, ...]:
    # The command contract is part of the execution specification and is
    # rendered for tiny portability fixtures as well as the 3,500/1,425-row
    # canonical programs.  BOOT ownership is defined entirely by the single
    # global BOOT row; reconstructing the full mathematical inventory here
    # would make every spec render parse tens of megabytes of catalog data and
    # would implicitly couple the frozen command contract to scheduler work.
    boot_rows = global_tasks(program)
    if len(boot_rows) != 1 or boot_rows[0].item_id != f"{program.task_prefix}-BOOT-001":
        raise BlueprintError(f"{program.kind}: BOOT task contract drift")
    boot = boot_rows[0]
    paths = set(boot.owned_paths)
    paths.update(path.relative_to(ROOT).as_posix() for path in source_input_paths((program,)))
    paths.update({
        program.blueprint.relative_to(ROOT).as_posix(),
        program.gantt.relative_to(ROOT).as_posix(),
        # Claim/Blueprint validators dynamically load the canonical manager
        # from this repository-relative path.  BOOT executes them from a
        # content-addressed read-only snapshot, so the manager itself must be
        # an explicit snapshot input rather than an implicit host dependency.
        "Docs/tools/manage_stage5_proof_debt_blueprints.py",
        "scripts/check_lean_environment.py",
        "scripts/stage5_boot_compile_check.py",
        # The ongoing checker imports this exact closed-schema contract.  It is
        # a BOOT command input even though it is shared by both program kinds
        # and therefore is not owned by either program's BOOT row.
        "scripts/stage5_boot_schema_contract.py",
        concurrency_prompt_path(program),
        "Docs/evidence/stage5_shared_execution/operator-budget-v1.json",
        "Docs/evidence/stage5_shared_execution/operator-budget-trust-root-v1.json",
    })
    if (
        BOOT_COMPILE_CHECK_PATH.is_symlink()
        or not BOOT_COMPILE_CHECK_PATH.is_file()
        or sha256_bytes(BOOT_COMPILE_CHECK_PATH.read_bytes())
        != BOOT_COMPILE_CHECK_SHA256
    ):
        raise BlueprintError("BOOT read-only compile checker digest drift")
    return tuple(sorted(paths))


def boot_sandbox_plan(program: Program) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    sandbox = load_boot_sandbox()
    python = CANONICAL_PYTHON.resolve(strict=True)
    python_sha = sha256_bytes(python.read_bytes())
    manifest = sandbox.seal_snapshot_manifest(
        ROOT,
        boot_sandbox_inputs(program),
        executable_paths={python.as_posix(): python_sha},
    )
    commands = []
    for index, tail in enumerate(BOOT_COMMANDS[program.kind], start=1):
        commands.append(sandbox.make_command_spec(
            manifest,
            command_id=f"{program.kind}-{index:02d}",
            argv=[python.as_posix(), "-I", "-B", *tail],
            timeout_seconds=BOOT_COMMAND_TIMEOUT_SECONDS,
            conformance_id=sandbox.MANAGER_CONFORMANCE_ID,
        ))
    return manifest, commands


def run_boot_commands(program: Program) -> list[dict[str, Any]]:
    sandbox = load_boot_sandbox()
    manifest, commands = boot_sandbox_plan(program)
    try:
        suite = sandbox.run_suite(ROOT, manifest, commands)
    except sandbox.SandboxError as exc:
        raise BlueprintError(f"BOOT sandboxed authoritative command suite failed: {exc}") from exc
    raw_results = suite.get("commands")
    if not isinstance(raw_results, list) or len(raw_results) != len(commands):
        raise BlueprintError("BOOT sandbox command result cardinality differs")
    executable_python_ast_audit(program)
    # systemd unit names and wall-clock duration are intentionally unique to a
    # replay.  unittest also reports elapsed seconds in otherwise identical
    # output.  A producer cannot truthfully pre-bind a later independent replay
    # if those incidental values are part of the authority.  Keep the raw
    # result inside the sandbox's fail-closed execution boundary, but publish a
    # deterministic semantic projection that still binds the exact command,
    # snapshot, tools, sandbox policy, complete normalized transcripts, exit
    # status, timeout/overflow flags, and descendant cleanup proof.
    results: list[dict[str, Any]] = []
    for raw in raw_results:
        try:
            stdout = base64.b64decode(raw["stdout_base64"], validate=True).decode("utf-8")
            stderr = base64.b64decode(raw["stderr_base64"], validate=True).decode("utf-8")
        except (KeyError, ValueError, UnicodeDecodeError) as exc:
            raise BlueprintError("BOOT sandbox result transcript is malformed") from exc

        def normalize_transcript(value: str) -> str:
            value = value.replace("\r\n", "\n")
            return re.sub(
                r"(?m)^(Ran [0-9]+ tests?) in [0-9]+(?:\.[0-9]+)?s$",
                r"\1 in <elapsed>s",
                value,
            )

        result = {
            "schema_version": "awesome-theorems/stage5-boot-command-semantic-result/1.0",
            "command_id": raw.get("command_id"),
            "command_authority_sha256": raw.get("command_authority_sha256"),
            "argv": raw.get("argv"),
            "snapshot_manifest_sha256": raw.get("snapshot_manifest_sha256"),
            "tool_bindings_sha256": raw.get("tool_bindings_sha256"),
            "sandbox_policy_sha256": raw.get("sandbox_policy_sha256"),
            "conformance_id": raw.get("conformance_id"),
            "systemd_result": raw.get("systemd_result"),
            "exit_code": raw.get("exit_code"),
            "timed_out": raw.get("timed_out"),
            "output_overflow": raw.get("output_overflow"),
            "stdout_complete": raw.get("stdout_complete"),
            "stderr_complete": raw.get("stderr_complete"),
            "descendants_absent": raw.get("descendants_absent"),
            "stdout_normalized": normalize_transcript(stdout),
            "stderr_normalized": normalize_transcript(stderr),
        }
        if (
            result["systemd_result"] not in {"success", "unknown"}
            or result["exit_code"] != 0
            or result["timed_out"] is not False
            or result["output_overflow"] is not False
            or result["stdout_complete"] is not True
            or result["stderr_complete"] is not True
            or result["descendants_absent"] is not True
        ):
            raise BlueprintError("BOOT sandbox semantic result is not a clean pass")
        results.append(result)
    return results


def validate_boot_common(
    program: Program,
    expected: list[Task],
    blueprint_raw: bytes,
    tasks: list[Task],
    artifact_bindings: dict[str, str],
) -> dict[str, Any]:
    return {
        "program": program.version,
        "boot_item_id": f"{program.task_prefix}-BOOT-001",
        "manager_sha256": manager_code_sha256(),
        "source_bundle_sha256": source_bundle_sha256(program),
        "execution_spec_sha256": sha256_bytes(canonical(spec_object(program))),
        "task_dag_sha256": sha256_bytes(canonical(checklist_dag_object(expected))),
        "blueprint_sha256": sha256_bytes(blueprint_raw),
        "boot_task_authority_sha256": task_authority_sha256(expected[0]),
        "artifact_bindings": artifact_bindings,
    }


def validate_boot_runtime_absence(program: Program) -> None:
    paths = [(ROOT / SHARED_RUNTIME_ROOT, "shared runtime/control state")]
    if program.kind == "conjecture":
        paths.append((
            ROOT / runtime_execution_root(program),
            "current conjecture runtime authority epoch",
        ))
    else:
        paths.append((ROOT / program.runtime_root, f"{program.kind} runtime/control state"))
    for path, label in paths:
        if path_lexists(path):
            raise BlueprintError(f"BOOT acceptance refuses {label}")


def accept_boot(program: Program, *, review: bool) -> None:
    if program not in {THEOREM, CONJECTURE}:
        raise BlueprintError("BOOT acceptor is available only for canonical programs")
    # Recovery is serialized, but candidate validation commands never run while
    # holding the repository mutation lease.  The later commit reacquires the
    # lease and replays the complete CAS/snapshot boundary.
    with manager_mutation_lock():
        recover_batch_transactions()
    validate_bootstrap_cron_absence()
    validate_boot_runtime_absence(program)
    expected = expected_tasks(program)
    blueprint_raw, blueprint_guard = regular_file_bytes(program.blueprint, "BOOT Blueprint")
    gantt_raw, gantt_guard = regular_file_bytes(program.gantt, "BOOT Gantt")
    current = parse_blueprint(program, blueprint_raw, expected, allow_boot_transition=True)
    wanted_current = "_" if review else " "
    boot = next(task for task in current if task.item_id == f"{program.task_prefix}-BOOT-001")
    if boot.state != wanted_current or any(
        task.state != " " for task in current if task.item_id != boot.item_id
    ):
        raise BlueprintError(
            f"BOOT {'review' if review else 'handoff'} action requires BOOT={wanted_current!r} "
            "and every mathematical row blank"
        )
    artifact_bindings, artifact_guards = boot_artifact_snapshot(program, expected)
    source_guards = source_input_expectations((program,))
    manager_path = ROOT / "Docs/tools/manage_stage5_proof_debt_blueprints.py"
    manager_guard = regular_file_expectation(manager_path)
    if manager_guard is None or manager_guard.sha256 != manager_code_sha256():
        raise BlueprintError("BOOT manager changed while freezing inputs")
    trust_keys, trust_guard = boot_trust_keys(program)
    handoff_path, handoff_acceptance_path, review_path, acceptance_path = boot_receipt_paths(program)
    handoff, handoff_guard = sealed_boot_receipt(
        handoff_path, BOOT_HANDOFF_FIELDS, BOOT_HANDOFF_SCHEMA, "BOOT handoff"
    )
    producer_principal = validate_signed_boot_document(
        handoff, BOOT_HANDOFF_FIELDS, BOOT_HANDOFF_SCHEMA,
        "BOOT handoff", trust_keys, "producer",
    )
    producer_attestation = handoff.get("producer_attestation")
    attested_producer, producer_guards = validate_boot_role_attestation(
        producer_attestation, program=program, expected_role="producer",
        trust_keys=trust_keys, label="BOOT producer",
    )
    common = validate_boot_common(program, expected, blueprint_raw, current, artifact_bindings)
    command_spec_sha = sha256_bytes(canonical(boot_command_spec(program)))
    common_keys_without_blueprint = {
        "program", "boot_item_id", "manager_sha256", "source_bundle_sha256",
        "execution_spec_sha256", "task_dag_sha256", "boot_task_authority_sha256",
        "artifact_bindings",
    }
    if (
        producer_principal != attested_producer
        or handoff.get("principal_id") != producer_principal
        or handoff.get("status") != "self_tested"
        or handoff.get("command_spec_sha256") != command_spec_sha
        or not isinstance(handoff.get("expected_command_results_sha256"), str)
        or not SHA256_RE.fullmatch(handoff["expected_command_results_sha256"])
        or any(handoff.get(key) != common[key] for key in common_keys_without_blueprint)
    ):
        raise BlueprintError("BOOT handoff exact authority/status binding drift")
    common_guards: dict[Path, FileExpectation] = {
        **artifact_guards, **source_guards, **producer_guards,
        manager_path: manager_guard,
        boot_trust_root_path(program): trust_guard,
        handoff_path: handoff_guard,
    }
    input_snapshot = boot_input_snapshot(
        program,
        artifact_bindings=artifact_bindings,
        source_guards=source_guards,
        manager_guard=manager_guard,
        trust_guard=trust_guard,
        handoff_path=handoff_path,
        handoff_guard=handoff_guard,
    )

    if not review:
        if (
            handoff.get("blueprint_sha256") != sha256_bytes(blueprint_raw)
            or handoff.get("gantt_sha256") != sha256_bytes(gantt_raw)
        ):
            raise BlueprintError("BOOT handoff does not bind the current blank Blueprint/Gantt")
        if any(path_lexists(path) for path in (handoff_acceptance_path, review_path, acceptance_path)):
            raise BlueprintError("BOOT handoff-acceptance/review/final acceptance exists before handoff transition")
        # Deliberately outside manager_mutation_lock.
        command_results = run_boot_commands(program)
        if handoff["expected_command_results_sha256"] != sha256_bytes(canonical(command_results)):
            raise BlueprintError("BOOT producer self-test result binding failed")
        wanted = tasks_with_boot_state(program, current, "_")
        new_blueprint = rewrite_blueprint_states(program, blueprint_raw, current, wanted)
        new_gantt = render_gantt(program, new_blueprint, wanted, utc_now())
        handoff_acceptance_unsigned = {
            "schema_version": BOOT_HANDOFF_ACCEPTANCE_SCHEMA,
            "status": "self_tested",
            "program": program.version,
            "boot_item_id": boot.item_id,
            "handoff_authority_sha256": handoff["authority_sha256"],
            "producer_principal_id": producer_principal,
            "input_snapshot": input_snapshot,
            "command_spec_sha256": command_spec_sha,
            "command_results": command_results,
            "pre_blueprint_sha256": sha256_bytes(blueprint_raw),
            "pre_gantt_sha256": sha256_bytes(gantt_raw),
            "post_blueprint_sha256": sha256_bytes(new_blueprint),
            "post_gantt_sha256": sha256_bytes(new_gantt),
        }
        handoff_acceptance = dict(handoff_acceptance_unsigned)
        handoff_acceptance["authority_sha256"] = sha256_bytes(canonical(handoff_acceptance_unsigned))
        handoff_acceptance_bytes = json.dumps(
            handoff_acceptance, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False
        ).encode("utf-8") + b"\n"

        def handoff_precommit() -> None:
            validate_bootstrap_cron_absence()
            validate_boot_runtime_absence(program)
            validate_source_authorities_fresh((program,))
            bindings, fresh_artifacts = boot_artifact_snapshot(program, expected)
            if bindings != artifact_bindings or fresh_artifacts != artifact_guards:
                raise BlueprintError("BOOT artifacts changed before handoff commit")
            validate_boot_role_attestation(
                producer_attestation, program=program, expected_role="producer",
                trust_keys=trust_keys, label="BOOT producer precommit",
            )
            if any(path_lexists(path) for path in (handoff_acceptance_path, review_path, acceptance_path)):
                raise BlueprintError("BOOT control receipt appeared before handoff commit")

        with manager_mutation_lock():
            recover_batch_transactions()
            atomic_batch_write(
                [
                    (program.blueprint, new_blueprint),
                    (program.gantt, new_gantt),
                    (handoff_acceptance_path, handoff_acceptance_bytes),
                ],
                expected_old={
                    program.blueprint: blueprint_guard,
                    program.gantt: gantt_guard,
                    handoff_acceptance_path: None,
                },
                guards=common_guards,
                precommit_validator=handoff_precommit,
            )
        print(f"ACCEPTED BOOT handoff {program.kind} state=underscore status=self_tested")
        return

    handoff_acceptance, handoff_acceptance_guard = sealed_boot_receipt(
        handoff_acceptance_path,
        BOOT_HANDOFF_ACCEPTANCE_FIELDS,
        BOOT_HANDOFF_ACCEPTANCE_SCHEMA,
        "BOOT handoff acceptance",
    )
    if (
        handoff_acceptance.get("status") != "self_tested"
        or handoff_acceptance.get("program") != program.version
        or handoff_acceptance.get("boot_item_id") != boot.item_id
        or handoff_acceptance.get("handoff_authority_sha256") != handoff["authority_sha256"]
        or handoff_acceptance.get("producer_principal_id") != producer_principal
        or handoff_acceptance.get("input_snapshot") != input_snapshot
        or handoff_acceptance.get("command_spec_sha256") != command_spec_sha
        or sha256_bytes(canonical(handoff_acceptance.get("command_results")))
        != handoff["expected_command_results_sha256"]
        or handoff_acceptance.get("pre_blueprint_sha256") != handoff.get("blueprint_sha256")
        or handoff_acceptance.get("pre_gantt_sha256") != handoff.get("gantt_sha256")
        or handoff_acceptance.get("post_blueprint_sha256") != sha256_bytes(blueprint_raw)
        or handoff_acceptance.get("post_gantt_sha256") != sha256_bytes(gantt_raw)
    ):
        raise BlueprintError("BOOT handoff-acceptance chain or pre/post binding drift")
    if path_lexists(acceptance_path):
        raise BlueprintError("BOOT acceptance receipt already exists")
    review_doc, review_guard = sealed_boot_receipt(
        review_path, BOOT_REVIEW_FIELDS, BOOT_REVIEW_SCHEMA, "BOOT review"
    )
    review_principal = validate_signed_boot_document(
        review_doc, BOOT_REVIEW_FIELDS, BOOT_REVIEW_SCHEMA,
        "BOOT review", trust_keys, "master",
    )
    if (
        review_doc.get("program") != program.version
        or review_doc.get("boot_item_id") != boot.item_id
        or review_doc.get("handoff_acceptance_authority_sha256")
        != handoff_acceptance["authority_sha256"]
        or review_doc.get("producer_principal_id") != producer_principal
        or review_doc.get("artifact_bindings") != artifact_bindings
        or review_doc.get("passed_gates") != list(BOOT_REVIEW_GATES)
        or review_doc.get("command_spec_sha256") != command_spec_sha
        or not isinstance(review_doc.get("reviewer_decisions"), list)
        or len(review_doc["reviewer_decisions"]) != 2
    ):
        raise BlueprintError("BOOT review authority/gate binding failed")
    master_attestation = review_doc.get("master_attestation")
    master_principal, master_guards = validate_boot_role_attestation(
        master_attestation, program=program, expected_role="master",
        trust_keys=trust_keys, label="BOOT Master",
    )
    if review_principal != master_principal:
        raise BlueprintError("BOOT review is not signed by the authenticated Master")
    decision_paths: set[str] = set()
    decision_digests: set[str] = set()
    decision_inodes: set[tuple[int, int]] = set()
    reviewer_principals: list[str] = []
    reviewer_attestations: list[dict[str, Any]] = []
    decision_guards: dict[Path, FileExpectation] = {}
    reviewer_guards: dict[Path, FileExpectation] = {}
    for index, locator in enumerate(review_doc["reviewer_decisions"]):
        if (
            not isinstance(locator, dict)
            or set(locator) != {"principal_id", "path", "sha256"}
            or not isinstance(locator.get("principal_id"), str)
            or not BOOT_ID_RE.fullmatch(locator["principal_id"])
            or not isinstance(locator.get("sha256"), str)
            or not SHA256_RE.fullmatch(locator["sha256"])
        ):
            raise BlueprintError("BOOT reviewer decision locator is not closed")
        path, guard = validate_decision_path(
            program, locator["path"], principal=locator["principal_id"],
            receipt_sha=locator["sha256"],
        )
        inode = (guard.stat_identity["device"], guard.stat_identity["inode"])
        if locator["path"] in decision_paths or locator["sha256"] in decision_digests or inode in decision_inodes:
            raise BlueprintError("BOOT reviewer decision receipt is reused")
        decision_paths.add(locator["path"])
        decision_digests.add(locator["sha256"])
        decision_inodes.add(inode)
        decision, exact_guard = sealed_boot_receipt(
            path, BOOT_DECISION_FIELDS, BOOT_DECISION_SCHEMA, f"BOOT reviewer decision {index}"
        )
        principal = validate_signed_boot_document(
            decision, BOOT_DECISION_FIELDS, BOOT_DECISION_SCHEMA,
            f"BOOT reviewer decision {index}", trust_keys, "reviewer",
        )
        attestation = decision.get("reviewer_attestation")
        attested, role_guards = validate_boot_role_attestation(
            attestation, program=program, expected_role="reviewer",
            trust_keys=trust_keys, label=f"BOOT reviewer {index}",
        )
        if (
            principal != locator["principal_id"] or attested != principal
            or decision.get("program") != program.version
            or decision.get("boot_item_id") != boot.item_id
            or decision.get("handoff_acceptance_authority_sha256")
            != handoff_acceptance["authority_sha256"]
            or decision.get("artifact_bindings") != artifact_bindings
            or decision.get("decision") != "pass"
            or decision.get("conflicts") != []
            or decision.get("passed_gates") != list(BOOT_REVIEW_GATES)
            or decision.get("command_spec_sha256") != command_spec_sha
        ):
            raise BlueprintError("BOOT reviewer decision binding failed")
        reviewer_principals.append(principal)
        reviewer_attestations.append(attestation)
        decision_guards[path] = exact_guard
        reviewer_guards.update(role_guards)
    validate_role_uniqueness(
        [producer_attestation, *reviewer_attestations, master_attestation],
        [producer_principal, *reviewer_principals, master_principal],
    )
    # Deliberately outside manager_mutation_lock.
    executable_python_ast_audit(program)
    command_results = run_boot_commands(program)
    command_results_sha = sha256_bytes(canonical(command_results))
    if review_doc.get("expected_command_results_sha256") != command_results_sha:
        raise BlueprintError("BOOT review command-result binding failed")
    wanted = tasks_with_boot_state(program, current, "x")
    new_blueprint = rewrite_blueprint_states(program, blueprint_raw, current, wanted)
    new_gantt = render_gantt(program, new_blueprint, wanted, utc_now())
    acceptance_unsigned = {
        "schema_version": BOOT_ACCEPTANCE_SCHEMA,
        "program": program.version,
        "boot_item_id": boot.item_id,
        "manager_sha256": manager_guard.sha256,
        "source_bundle_sha256": source_bundle_sha256(program),
        "handoff_authority_sha256": handoff["authority_sha256"],
        "handoff_acceptance_authority_sha256": handoff_acceptance["authority_sha256"],
        "review_authority_sha256": review_doc["authority_sha256"],
        "producer_principal_id": producer_principal,
        "reviewer_principal_ids": reviewer_principals,
        "master_principal_id": master_principal,
        "artifact_bindings": artifact_bindings,
        "command_spec_sha256": command_spec_sha,
        "command_results": command_results,
        "post_blueprint_sha256": sha256_bytes(new_blueprint),
        "post_gantt_sha256": sha256_bytes(new_gantt),
        "cron_activated": False,
    }
    acceptance = dict(acceptance_unsigned)
    acceptance["authority_sha256"] = sha256_bytes(canonical(acceptance_unsigned))
    acceptance_bytes = json.dumps(
        acceptance, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False
    ).encode("utf-8") + b"\n"
    all_guards = {
        **common_guards, **master_guards, **decision_guards, **reviewer_guards,
        handoff_acceptance_path: handoff_acceptance_guard,
        review_path: review_guard,
    }

    def review_precommit() -> None:
        validate_bootstrap_cron_absence()
        validate_boot_runtime_absence(program)
        validate_source_authorities_fresh((program,))
        bindings, fresh_artifacts = boot_artifact_snapshot(program, expected)
        if bindings != artifact_bindings or fresh_artifacts != artifact_guards:
            raise BlueprintError("BOOT artifacts changed after command execution")
        for path, guard in all_guards.items():
            validate_file_expectation(path, guard)
        validate_role_uniqueness(
            [producer_attestation, *reviewer_attestations, master_attestation],
            [producer_principal, *reviewer_principals, master_principal],
        )
        validate_boot_role_attestation(
            master_attestation, program=program, expected_role="master",
            trust_keys=trust_keys, label="BOOT Master precommit",
        )
        if path_lexists(acceptance_path):
            raise BlueprintError("BOOT final acceptance appeared before review commit")

    with manager_mutation_lock():
        recover_batch_transactions()
        atomic_batch_write(
            [
                (program.blueprint, new_blueprint),
                (program.gantt, new_gantt),
                (acceptance_path, acceptance_bytes),
            ],
            expected_old={
                program.blueprint: blueprint_guard,
                program.gantt: gantt_guard,
                acceptance_path: None,
            },
            guards=all_guards,
            precommit_validator=review_precommit,
        )
    print(f"ACCEPTED BOOT review {program.kind} state=x cron_activated=false")


def validate_bootstrap_cron_absence() -> None:
    cron = read_user_crontab()
    for program in (THEOREM, CONJECTURE):
        begin_count = cron.count(program.cron_marker_begin)
        end_count = cron.count(program.cron_marker_end)
        if begin_count or end_count:
            raise BlueprintError(
                f"bootstrap forbidden with existing {program.kind} cron markers "
                f"(begin={begin_count}, end={end_count})"
            )


def validate_no_execution_history(program: Program, tasks: list[Task]) -> None:
    roots = [
        ROOT / program.runtime_root,
        DOCS / "evidence" / f"stage5_{program.kind}s",
        ROOT / f"Stage5_{'Theorem' if program.kind == 'theorem' else 'Conjecture'}_Instances",
        ROOT
        / "Formalizations/Lean/AwesomeTheorems/Stage5"
        / ("Theorems" if program.kind == "theorem" else "Conjectures"),
    ]
    for path in roots:
        if path_lexists(path):
            raise BlueprintError(
                f"{program.kind}: one-time bootstrap manager forbidden after execution/evidence surface exists: "
                f"{path.relative_to(ROOT)}"
            )
    for task in tasks:
        for owned in task.owned_paths:
            path = ROOT / owned
            if path_lexists(path):
                raise BlueprintError(
                    f"{program.kind}: owned execution artifact already exists: {owned}"
                )


def validate_shared_execution_history_absence() -> None:
    shared_evidence = DOCS / "evidence/stage5_shared_execution"
    if not path_lexists(shared_evidence):
        return
    if shared_evidence.is_symlink() or not shared_evidence.is_dir():
        raise BlueprintError("shared execution evidence root is not a real directory")
    allowed_operator_inputs = {
        shared_evidence / "operator-budget-v1.json",
        shared_evidence / "operator-budget-trust-root-v1.json",
        shared_evidence / "route-price-authority-v1.json",
        OBJECT_WORKER_V2_MIGRATION_RECEIPT,
    }
    migration_root = shared_evidence / "blueprint-migrations"

    def historical_migration(path: Path) -> bool:
        """Accept only immutable, sealed migration receipts as history.

        The bootstrap/check manager must reject live execution state, but a
        migration receipt is precisely the durable authority that explains
        why the current Blueprint/spec bytes are no longer pristine.  Earlier
        versions accidentally rejected this required audit trail wholesale.
        """
        if path.parent != migration_root or not re.fullmatch(
            r"S5PD-BLUEPRINT-MIGRATE-[0-9]{6}-(?:program-isolation|concurrency-prompt|lifecycle|conjecture-prompt-policy)\.json",
            path.name,
        ):
            return False
        try:
            value = strict_json_loads(path.read_bytes(), f"historical migration {path.name}")
        except (OSError, BlueprintError):
            return False
        if not isinstance(value, dict):
            return False
        authority = value.get("authority_sha256")
        body = dict(value)
        body.pop("authority_sha256", None)
        if not isinstance(authority, str) or not SHA256_RE.fullmatch(authority):
            return False
        if sha256_bytes(canonical(body)) != authority:
            return False
        expected_schema: dict[str, str | tuple[str, ...]] = {
            "program-isolation": "awesome-theorems/stage5-program-isolation-migration/1.0",
            "concurrency-prompt": (
                "awesome-theorems/stage5-concurrency-prompt-migration/1.0",
                "awesome-theorems/stage5-concurrency-prompt-migration/2.0",
            ),
            "lifecycle": "awesome-theorems/stage5-theorem-lifecycle-migration/1.0",
            "conjecture-prompt-policy": "awesome-theorems/stage5-conjecture-prompt-policy-migration/1.0",
        }
        suffix = next(
            candidate for candidate in ("program-isolation", "concurrency-prompt", "lifecycle", "conjecture-prompt-policy")
            if path.name.endswith(f"-{candidate}.json")
        )
        expected_id = (
            path.stem if suffix in {"concurrency-prompt", "lifecycle", "conjecture-prompt-policy"}
            else path.stem.removesuffix("-" + suffix)
        )
        schemas = expected_schema[suffix]
        schema_ok = value.get("schema_version") in schemas if isinstance(schemas, tuple) else value.get("schema_version") == schemas
        return schema_ok and value.get("migration_id") == expected_id
    for path in shared_evidence.rglob("*"):
        if path.is_dir() and not path.is_symlink():
            continue
        if (
            path not in allowed_operator_inputs
            and historical_migration(path)
        ):
            continue
        if path not in allowed_operator_inputs or path.is_symlink() or not path.is_file():
            raise BlueprintError(
                f"bootstrap manager refuses shared execution/history artifact: "
                f"{path.relative_to(ROOT)}"
            )


def parse_legacy_v1_blueprint(
    program: Program, raw: bytes
) -> tuple[dict[str, Any], Counter[str], list[str]]:
    """Read only the frozen v1 authority needed for the explicit v1-to-v2 migration."""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise BlueprintError(f"{program.kind}: legacy Blueprint is not UTF-8") from exc
    validate_marker_pairs(text, BLUEPRINT_MARKER_PAIRS, f"{program.kind} legacy Blueprint")
    specification_block = text.split(SPEC_BEGIN, 1)[1].split(SPEC_END, 1)[0].strip()
    if not specification_block.startswith("```json\n") or not specification_block.endswith("\n```"):
        raise BlueprintError(f"{program.kind}: malformed legacy specification")
    specification = strict_json_loads(
        specification_block[8:-4], f"{program.kind} legacy execution specification"
    )
    expected = LEGACY_V1_MIGRATION_AUTHORITIES[program.kind]
    for key in ("program", "runtime_root", "shared_runtime_root"):
        if not isinstance(specification, dict) or specification.get(key) != expected[key]:
            raise BlueprintError(f"{program.kind}: legacy {key} authority differs")
    rows: list[tuple[str, str]] = []
    checklist = text.split(CHECKLIST_BEGIN, 1)[1].split(CHECKLIST_END, 1)[0]
    for line in checklist.splitlines():
        if not line:
            continue
        match = ROW_RE.fullmatch(line)
        if match is None:
            raise BlueprintError(f"{program.kind}: malformed legacy checklist row")
        rows.append((match.group("id"), match.group("state")))
    if len(rows) != expected["row_count"] or len({item_id for item_id, _ in rows}) != len(rows):
        raise BlueprintError(f"{program.kind}: legacy checklist cardinality/identity differs")
    prefix = rf"^{program.task_prefix}-[0-9]{{8}}-"
    mathematical = [item_id for item_id, _ in rows if re.match(prefix, item_id)]
    if len(mathematical) != expected["mathematical_row_count"]:
        raise BlueprintError(f"{program.kind}: legacy mathematical row cardinality differs")
    return specification, Counter(state for _, state in rows), [
        item_id for item_id, state in rows if state != " "
    ]


def count_named_files(root: Path, name: str) -> int:
    if not path_lexists(root):
        return 0
    if root.is_symlink() or not root.is_dir():
        raise BlueprintError(f"migration evidence root is not a real directory: {root}")
    return sum(1 for path in root.rglob(name) if path.is_file() and not path.is_symlink())


def migration_history_summary(program: Program) -> dict[str, Any]:
    runtime_root = ROOT / LEGACY_V1_MIGRATION_AUTHORITIES[program.kind]["runtime_root"]
    handoff_root = (
        DOCS / "evidence" / f"stage5_{program.kind}s" / "execution" / "handoffs"
    )
    result_files: list[Path] = []
    for root in (runtime_root, handoff_root):
        if not path_lexists(root):
            continue
        if root.is_symlink() or not root.is_dir():
            raise BlueprintError(f"migration evidence root is not a real directory: {root}")
        result_files.extend(
            path for path in root.rglob("result.json")
            if path.is_file() and not path.is_symlink()
        )
    mathematical_ids: set[str] = set()
    item_ids: set[str] = set()
    for path in result_files:
        result = strict_json_loads(path.read_bytes(), path.relative_to(ROOT).as_posix())
        item_id = result.get("item_id") if isinstance(result, dict) else None
        if not isinstance(item_id, str):
            raise BlueprintError(f"migration result lacks item identity: {path}")
        item_ids.add(item_id)
        match = re.fullmatch(rf"{program.task_prefix}-([0-9]{{8}})-[A-Z0-9-]+", item_id)
        if match:
            mathematical_ids.add(match.group(1))
    top_level_handoff_directories = 0
    if path_lexists(handoff_root):
        top_level_handoff_directories = sum(
            1
            for child in handoff_root.iterdir()
            if child.is_dir() and not child.is_symlink()
        )
    return {
        "legacy_runtime_root": runtime_root.relative_to(ROOT).as_posix(),
        "legacy_runtime_preserved": path_lexists(runtime_root),
        "legacy_handoff_root": handoff_root.relative_to(ROOT).as_posix(),
        "legacy_handoff_root_preserved": path_lexists(handoff_root),
        "result_json_file_count": len(result_files),
        "distinct_legacy_item_id_count": len(item_ids),
        "distinct_mathematical_id_count": len(mathematical_ids),
        "top_level_handoff_directory_count": top_level_handoff_directories,
    }


def migrate_one_object_one_goal_blueprints(programs: tuple[Program, ...]) -> None:
    """Atomically retire v1 phase rows and install all-blank one-object v2 TARGETs."""
    if set(programs) != {THEOREM, CONJECTURE}:
        raise BlueprintError("one-object v2 migration must replace both programs together")
    with manager_mutation_lock():
        recover_batch_transactions()
        validate_bootstrap_cron_absence()
        if path_lexists(ROOT / SHARED_RUNTIME_ROOT):
            raise BlueprintError("v2 shared runtime exists; Blueprint migration is no longer pristine")
        for program in programs:
            if path_lexists(ROOT / program.runtime_root):
                raise BlueprintError(f"{program.kind}: v2 runtime already exists")
        if path_lexists(OBJECT_WORKER_V2_MIGRATION_RECEIPT):
            raise BlueprintError("one-object v2 migration receipt already exists")
        # This authority refresh changes only the theorem program.  The
        # independently governed conjecture Blueprint/spec/Gantt are copied
        # byte-for-byte and must not make a theorem route migration depend on
        # a concurrently published conjecture-pool pointer.
        source_guards = source_input_expectations((THEOREM,))
        old_guards: dict[Path, FileExpectation | None] = {}
        legacy_records: dict[str, Any] = {}
        new_outputs: list[tuple[Path, bytes]] = []
        generated_at = utc_now()
        task_sets: list[tuple[Program, list[Task]]] = []
        for program in programs:
            blueprint_guard = regular_file_expectation(program.blueprint)
            gantt_guard = regular_file_expectation(program.gantt)
            if blueprint_guard is None or gantt_guard is None:
                raise BlueprintError(f"{program.kind}: legacy Blueprint/Gantt pair is missing")
            expected = LEGACY_V1_MIGRATION_AUTHORITIES[program.kind]
            if (
                blueprint_guard.sha256 != expected["blueprint_sha256"]
                or gantt_guard.sha256 != expected["gantt_sha256"]
            ):
                raise BlueprintError(f"{program.kind}: legacy Blueprint/Gantt digest differs")
            old_blueprint = program.blueprint.read_bytes()
            old_gantt = program.gantt.read_bytes()
            _, states, advanced_ids = parse_legacy_v1_blueprint(program, old_blueprint)
            gantt_generated_at = extract_generated_at(old_gantt)
            tasks = expected_tasks(program)
            new_blueprint = render_blueprint(program, tasks)
            parsed = parse_blueprint(program, new_blueprint, tasks)
            new_gantt = render_gantt(program, new_blueprint, parsed, generated_at)
            task_sets.append((program, tasks))
            old_guards.update({program.blueprint: blueprint_guard, program.gantt: gantt_guard})
            new_outputs.extend(((program.blueprint, new_blueprint), (program.gantt, new_gantt)))
            legacy_records[program.kind] = {
                "program": expected["program"],
                "blueprint_path": program.blueprint.relative_to(ROOT).as_posix(),
                "blueprint_sha256": blueprint_guard.sha256,
                "gantt_path": program.gantt.relative_to(ROOT).as_posix(),
                "gantt_sha256": gantt_guard.sha256,
                "gantt_generated_at": gantt_generated_at,
                "checklist_item_count": expected["row_count"],
                "mathematical_phase_row_count": expected["mathematical_row_count"],
                "state_counts": {
                    "not_done": states[" "],
                    "handoff_waiting_master": states["_"],
                    "master_accepted": states["x"],
                },
                "advanced_item_ids": advanced_ids,
                "history": migration_history_summary(program),
                "v2_program": program.version,
                "v2_blueprint_sha256": sha256_bytes(new_blueprint),
                "v2_gantt_sha256": sha256_bytes(new_gantt),
                "v2_checklist_item_count": len(tasks),
                "v2_target_count": program.target_count,
                "v2_initial_state_counts": {
                    "not_done": len(tasks),
                    "handoff_waiting_master": 0,
                    "master_accepted": 0,
                },
            }
        validate_cross_program_ownership(task_sets)
        receipt_body = {
            "schema_version": "awesome-theorems/stage5-one-object-one-goal-migration/1.0",
            "migration_id": "stage5-one-object-one-goal-v1-to-v2",
            "generated_at": generated_at,
            "programs": legacy_records,
            "mapping": "one frozen mathematical ID -> one TARGET -> one task root -> one private tmux server/socket/session -> one private CODEX_HOME -> one Codex process tree -> one thread -> one active /goal",
            "state_policy": "all v2 TARGET, BOOT, shard, aggregate, QA and PROGRAM-RELEASE rows start not_done; no legacy phase x or underscore advances any v2 row",
            "evidence_policy": "legacy v1 runtime, result files, handoff archives, activation/BOOT receipts and accepted canonical artifacts are preserved byte-for-byte as historical target-local migration evidence only",
            "review_policy": "canonical Master/validator reviews a complete TARGET handoff without starting a reviewer worker, tmux, thread or goal",
            "runtime_policy": "Docker/container worker transport is forbidden; no v2 runtime, controller, cron, tmux or worker is created by this migration",
            "authority_inputs": {
                path.relative_to(ROOT).as_posix(): expectation.sha256
                for path, expectation in sorted(source_guards.items())
            },
        }
        receipt = {
            **receipt_body,
            "authority_sha256": sha256_bytes(canonical(receipt_body)),
        }
        receipt_bytes = json.dumps(
            receipt, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False
        ).encode("utf-8") + b"\n"
        receipt_guard = regular_file_expectation(OBJECT_WORKER_V2_MIGRATION_RECEIPT)
        if receipt_guard is not None:
            raise BlueprintError("one-object v2 migration receipt appeared concurrently")

        def final_migration_boundary() -> None:
            validate_bootstrap_cron_absence()
            validate_source_authorities_fresh(programs)
            if path_lexists(ROOT / SHARED_RUNTIME_ROOT):
                raise BlueprintError("v2 shared runtime appeared before migration commit")
            for program in programs:
                if path_lexists(ROOT / program.runtime_root):
                    raise BlueprintError(f"{program.kind}: v2 runtime appeared before migration commit")

        atomic_batch_write(
            [*new_outputs, (OBJECT_WORKER_V2_MIGRATION_RECEIPT, receipt_bytes)],
            expected_old={**old_guards, OBJECT_WORKER_V2_MIGRATION_RECEIPT: None},
            guards=source_guards,
            precommit_validator=final_migration_boundary,
        )
    for program, tasks in task_sets:
        print(
            f"MIGRATED {program.kind} rows={len(tasks)} targets={program.target_count} "
            "state=all_not_done worker=one_object_one_tmux_one_goal"
        )
    print(f"WROTE {OBJECT_WORKER_V2_MIGRATION_RECEIPT.relative_to(ROOT)}")


def migrate_program_isolation_v3(programs: tuple[Program, ...]) -> None:
    """Atomically install the program-local, tmux-only v3 execution surfaces.

    This is also the reviewed authority-refresh path for strengthened gates.
    Mathematical IDs, row ownership, dependencies and the one-object/one-goal
    bijection are preserved.  Theorem progress is deliberately invalidated
    when the acceptance predicate changes; stale BOOT or TARGET evidence may
    never survive by cursor preservation.  No runtime, cron or worker is
    created here.
    """
    if set(programs) != {THEOREM, CONJECTURE}:
        raise BlueprintError("program-isolation migration must update both Blueprints together")
    refresh_policy = (
        "the theorem program binds exactly 24 gpt-5.6-sol/ultra/default "
        "interactive tmux /goal executions; subagents are permitted only as "
        "first-class independently tmux-isolated and fully accounted executions "
        "inside the same 24-execution ceiling"
    )
    with manager_mutation_lock():
        recover_batch_transactions()
        validate_bootstrap_cron_absence()
        if path_lexists(ROOT / SHARED_RUNTIME_ROOT):
            raise BlueprintError("program-isolation migration refuses shared v2 runtime state")
        # The predecessor controller may leave a durable, fully harvested
        # runtime projection behind.  Migration must not consume that runtime
        # as authority (and must never run with live transports), so render a
        # clean projection from the preserved checklist cursor only.
        saved_runtime_snapshot = runtime_snapshot
        globals()["runtime_snapshot"] = lambda _program: (None, None)
        old_guards: dict[Path, FileExpectation | None] = {}
        outputs: list[tuple[Path, bytes]] = []
        records: dict[str, Any] = {}
        generated_at = utc_now()
        try:
          for program in programs:
            old_blueprint, old_bp_guard = regular_file_bytes(program.blueprint, f"{program.kind} Blueprint")
            old_gantt, old_gantt_guard = regular_file_bytes(program.gantt, f"{program.kind} Gantt")
            spec_path = DOCS / "evidence" / f"stage5_{program.kind}s" / "execution-spec.json"
            old_spec_raw, old_spec_guard = regular_file_bytes(
                spec_path, f"{program.kind} execution specification"
            )
            expected = expected_tasks(program)
            # Parse the predecessor only for row/DAG/ownership preservation;
            # its embedded v2 spec is intentionally the superseded authority.
            old_tasks = parse_blueprint(
                program, old_blueprint, expected,
                allow_boot_transition=True,
                allow_superseded_authority_for_invalidation=True,
                allow_immutable_row_drift=True,
                allow_progress_cursor=True,
                allow_legacy_execution_gate=True,
            )
            # A stricter theorem predicate invalidates all prior theorem
            # states, including BOOT: the previously accepted validator did
            # not enforce transitive semantic identity or strict dominance.
            # Conjecture gates are unaffected and preserve their cursor.
            state_by_id = {task.item_id: task.state for task in old_tasks}
            invalidated_item_ids = (
                [task.item_id for task in old_tasks if task.state != " "]
                if program.kind == "theorem" else []
            )
            if program.kind == "theorem":
                replacement_tasks = [task.with_state(" ") for task in expected]
                new_blueprint = render_blueprint(program, replacement_tasks)
                new_tasks = parse_blueprint(
                    program, new_blueprint, expected,
                    allow_boot_transition=True,
                    allow_superseded_authority_for_invalidation=True,
                    allow_immutable_row_drift=True,
                    allow_progress_cursor=True,
                )
                new_spec_object = spec_object(program)
                new_prompt = concurrency_prompt_bytes(
                    program, specification_override=new_spec_object,
                )
                new_gantt = render_gantt(
                    program, new_blueprint, new_tasks, generated_at,
                    prompt_override=new_prompt,
                )
                new_spec = json.dumps(
                    new_spec_object, ensure_ascii=False, sort_keys=True,
                    indent=2, allow_nan=False,
                ).encode("utf-8") + b"\n"
            else:
                # A theorem-only operator route/cap refresh must preserve the
                # independently governed conjecture program byte-for-byte.
                replacement_tasks = old_tasks
                new_blueprint = old_blueprint
                new_tasks = old_tasks
                new_gantt = old_gantt
                new_spec = old_spec_raw
            old_guards[program.blueprint] = old_bp_guard
            old_guards[program.gantt] = old_gantt_guard
            old_guards[spec_path] = old_spec_guard
            if program.kind == "theorem":
                prompt_path = ROOT / concurrency_prompt_path(program)
                _, prompt_guard = regular_file_bytes(
                    prompt_path, f"{program.kind} concurrency prompt",
                )
                old_guards[prompt_path] = prompt_guard
                outputs.extend((
                    (program.blueprint, new_blueprint),
                    (program.gantt, new_gantt),
                    (spec_path, new_spec),
                    (prompt_path, new_prompt),
                ))
            records[program.kind] = {
                "program": program.version,
                "blueprint_path": program.blueprint.relative_to(ROOT).as_posix(),
                "gantt_path": program.gantt.relative_to(ROOT).as_posix(),
                "old_blueprint_sha256": old_bp_guard.sha256,
                "old_gantt_sha256": old_gantt_guard.sha256,
                "new_blueprint_sha256": sha256_bytes(new_blueprint),
                "new_gantt_sha256": sha256_bytes(new_gantt),
                "row_count": len(old_tasks),
                "target_count": program.target_count,
                "old_state_counts": dict(Counter(state_name(task.state) for task in old_tasks)),
                "new_state_counts": dict(Counter(state_name(task.state) for task in new_tasks)),
                "invalidated_item_ids": invalidated_item_ids,
                "invalidation_reason": (
                    refresh_policy + "; the stronger Master-recomputed transitive "
                    "semantic identity, semantic-substitution mutations, strict "
                    "dominance over the incomplete THM-M-0387 negative fixture, "
                    "and distilled proof sufficiency remain mandatory"
                    if program.kind == "theorem" else None
                ),
                "old_spec_sha256": sha256_bytes(canonical(
                    strict_json_loads(old_blueprint.decode("utf-8").split(SPEC_BEGIN, 1)[1].split(SPEC_END, 1)[0].strip()[8:-4], "old spec")
                )),
                "new_spec_sha256": sha256_bytes(canonical(
                    spec_object(program) if program.kind == "theorem"
                    else strict_json_loads(old_spec_raw, "preserved conjecture spec")
                )),
                "execution_spec_file_sha256": sha256_bytes(new_spec),
                "bijection": "one mathematical object -> one TARGET -> one task-local tmux server/socket/session -> one private CODEX_HOME -> one thread -> one active /goal",
            }
        finally:
            globals()["runtime_snapshot"] = saved_runtime_snapshot
        receipt_path = next_program_isolation_migration_receipt()
        body = {
            "schema_version": "awesome-theorems/stage5-program-isolation-migration/1.0",
            "migration_id": receipt_path.stem.removesuffix("-program-isolation"),
            "generated_at": generated_at,
            "programs": records,
            "preserved": ["mathematical TARGET IDs", "TARGET dependencies", "owned paths", "DAG and terminal ancestry"],
            "state_policy": "the conjecture Blueprint, Gantt, execution spec and cursor are preserved byte-for-byte; every nonblank theorem state is invalidated under the refreshed theorem execution authority",
            "new_policy": refresh_policy + "; the conjecture program remains "
            "byte-identical; theorem completion still requires exact transitive "
            "semantic identity with no shadowing, M0, R0, empty H/M/R cuts, "
            "current cold replay and semantic mutations, and a strict-dominance "
            "certificate over the pinned incomplete THM-M-0387 negative fixture; "
            "distilled output removes duplication without removing mathematics",
            "runtime_policy": "no v2 runtime, controller, cron, tmux or worker is created by this migration",
        }
        receipt = dict(body)
        receipt["authority_sha256"] = sha256_bytes(canonical(body))
        receipt_bytes = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
        source_guards = source_input_expectations(programs)
        old_guards[receipt_path] = None
        def boundary() -> None:
            validate_bootstrap_cron_absence()
            if path_lexists(ROOT / SHARED_RUNTIME_ROOT):
                raise BlueprintError("shared v2 runtime appeared during program-isolation migration")
        atomic_batch_write(
            [*outputs, (receipt_path, receipt_bytes)],
            expected_old={
                path: old_guards[path]
                for path, _ in [*outputs, (receipt_path, receipt_bytes)]
            },
            guards=source_guards,
            precommit_validator=boundary,
        )
    print(f"MIGRATED program-local isolation for theorem+conjecture; receipt={receipt_path.relative_to(ROOT)}")


def next_concurrency_prompt_migration_receipt() -> Path:
    directory = DOCS / "evidence/stage5_shared_execution/blueprint-migrations"
    directory.mkdir(parents=True, exist_ok=True)
    candidates = sorted(directory.glob("S5PD-BLUEPRINT-MIGRATE-*-concurrency-prompt.json"))
    number = 1
    if candidates:
        numbers = [int(match.group(1)) for path in candidates if (match := re.search(r"MIGRATE-(\d+)-", path.name))]
        number = max(numbers, default=0) + 1
    return directory / f"S5PD-BLUEPRINT-MIGRATE-{number:06d}-concurrency-prompt.json"


def conjecture_prompt_policy_migration_receipts() -> tuple[Path, ...]:
    directory = DOCS / "evidence/stage5_shared_execution/blueprint-migrations"
    return tuple(sorted(directory.glob("S5PD-BLUEPRINT-MIGRATE-*-conjecture-prompt-policy.json")))


def next_conjecture_prompt_policy_migration_receipt() -> Path:
    directory = DOCS / "evidence/stage5_shared_execution/blueprint-migrations"
    ordinals: list[int] = []
    if directory.is_dir():
        for path in directory.glob("S5PD-BLUEPRINT-MIGRATE-*.json"):
            match = re.search(r"MIGRATE-(\d+)-", path.name)
            if match:
                ordinals.append(int(match.group(1)))
    return directory / f"S5PD-BLUEPRINT-MIGRATE-{max(ordinals, default=0) + 1:06d}-conjecture-prompt-policy.json"


@contextmanager
def theorem_scheduler_transition_guard() -> Iterator[None]:
    """Exclude one controller tick while publishing Blueprint authority bytes."""
    path = ROOT / ".ops/stage5-theorems-execution-v2.scheduler.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_RDWR | os.O_CREAT | getattr(os, "O_CLOEXEC", 0), 0o600)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise BlueprintError("theorem controller transition is active; retry lifecycle migration") from exc
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def _requirements_region(raw: bytes) -> bytes:
    text = raw.decode("utf-8")
    if text.count(REQUIREMENTS_BEGIN) != 1 or text.count(REQUIREMENTS_END) != 1:
        raise BlueprintError("theorem requirements markers differ")
    return text.split(REQUIREMENTS_BEGIN, 1)[1].split(REQUIREMENTS_END, 1)[0].encode("utf-8")


def _specification_region(raw: bytes) -> bytes:
    text = raw.decode("utf-8")
    if text.count(SPEC_BEGIN) != 1 or text.count(SPEC_END) != 1:
        raise BlueprintError("theorem execution-spec markers differ")
    return text.split(SPEC_BEGIN, 1)[1].split(SPEC_END, 1)[0].encode("utf-8")


def _replace_specification_region(raw: bytes, preserved: bytes) -> bytes:
    text = raw.decode("utf-8")
    before, rest = text.split(SPEC_BEGIN, 1)
    _, after = rest.split(SPEC_END, 1)
    return (before + SPEC_BEGIN).encode("utf-8") + preserved + (SPEC_END + after).encode("utf-8")


def _task_authority_projection(tasks: list[Task]) -> list[dict[str, Any]]:
    return [
        {
            "item_id": task.item_id,
            "title": task.title,
            "dependencies": list(task.dependencies),
            "owned_paths": list(task.owned_paths),
            "gate": task.gate,
        }
        for task in tasks
    ]


def _checklist_dag_projection(tasks: list[Task]) -> list[dict[str, Any]]:
    authorities = _task_authority_projection(tasks)
    return [
        {
            "item_id": task.item_id,
            "dependencies": list(task.dependencies),
            "owned_paths": list(task.owned_paths),
            "task_authority_sha256": sha256_bytes(canonical(authority)),
        }
        for task, authority in zip(tasks, authorities)
    ]


def _render_ongoing_theorem_gantt(blueprint: bytes) -> bytes:
    generator_path = DOCS / "tools/generate_stage5_theorems_gantt.py"
    module_spec = importlib.util.spec_from_file_location(
        "stage5_theorem_lifecycle_gantt_migration", generator_path
    )
    if module_spec is None or module_spec.loader is None:
        raise BlueprintError("ongoing theorem Gantt generator is unavailable")
    module = importlib.util.module_from_spec(module_spec)
    import sys
    sys.modules[module_spec.name] = module
    module_spec.loader.exec_module(module)
    descriptor, temporary = tempfile.mkstemp(prefix="stage5-theorem-lifecycle-", suffix=".md")
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(blueprint)
            stream.flush()
            os.fsync(stream.fileno())
        return module.render(blueprint_path=Path(temporary))
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def migrate_theorem_lifecycle_v5() -> None:
    """Strengthen theorem lifecycle semantics without interrupting live generations."""
    program = THEOREM
    state_path = ROOT / program.runtime_root / "state/controller-state.json"
    with theorem_scheduler_transition_guard(), manager_mutation_lock():
        recover_batch_transactions()
        blueprint_guard = regular_file_expectation(program.blueprint)
        gantt_guard = regular_file_expectation(program.gantt)
        state_guard = regular_file_expectation(state_path)
        if blueprint_guard is None or gantt_guard is None:
            raise BlueprintError("theorem Blueprint/Gantt is missing")
        old_blueprint = program.blueprint.read_bytes()
        old_gantt = program.gantt.read_bytes()
        expected = expected_tasks(program)
        current = parse_blueprint(
            program,
            old_blueprint,
            expected,
            allow_boot_transition=True,
            allow_superseded_authority_for_invalidation=True,
            allow_immutable_row_drift=True,
            allow_progress_cursor=True,
        )
        preserved_spec_region = _specification_region(old_blueprint)
        rendered = render_blueprint(program, current)
        new_blueprint = _replace_specification_region(rendered, preserved_spec_region)
        reparsed = parse_blueprint(
            program,
            new_blueprint,
            expected,
            allow_boot_transition=True,
            allow_superseded_authority_for_invalidation=True,
            allow_immutable_row_drift=True,
            allow_progress_cursor=True,
        )
        old_authority = _task_authority_projection(current)
        new_authority = _task_authority_projection(reparsed)
        if old_authority != new_authority:
            raise BlueprintError("lifecycle migration changed checklist task authority")
        if [task.state for task in current] != [task.state for task in reparsed]:
            raise BlueprintError("lifecycle migration changed checklist states")
        if _specification_region(new_blueprint) != preserved_spec_region:
            raise BlueprintError("lifecycle migration changed the embedded execution specification")
        new_gantt = _render_ongoing_theorem_gantt(new_blueprint)
        state_value: dict[str, Any] = {}
        if state_guard is not None:
            loaded = strict_json_loads(state_path.read_bytes(), "theorem controller state")
            if isinstance(loaded, dict):
                state_value = loaded
        active_generations = []
        for record in state_value.get("claims", {}).values() if isinstance(state_value.get("claims"), dict) else ():
            if not isinstance(record, dict) or record.get("status") not in {
                "reserved", "materialized", "tmux_started", "goal_pasted",
                "request_reserved", "submission_committed", "goal_submitted", "live",
                "generation_retire_required", "handoff_ready",
            }:
                continue
            claim_path = Path(str(record.get("task_root", ""))) / "claim.json"
            baseline_sha = None
            if claim_path.is_file() and not claim_path.is_symlink():
                claim = strict_json_loads(claim_path.read_bytes(), "active lifecycle claim")
                if isinstance(claim, dict):
                    baseline_sha = claim.get("baseline", {}).get("blueprint_sha256")
            active_generations.append({
                "item_id": record.get("item_id"),
                "generation_id": record.get("generation_id"),
                "status": record.get("status"),
                "baseline_blueprint_sha256": baseline_sha,
            })
        active_generations.sort(key=lambda row: (str(row["item_id"]), str(row["generation_id"])))
        receipt_path = next_lifecycle_migration_receipt()
        body = {
            "schema_version": "awesome-theorems/stage5-theorem-lifecycle-migration/1.0",
            "migration_id": receipt_path.stem,
            "generated_at": utc_now(),
            "program": program.version,
            "row_count": len(current),
            "target_count": program.target_count,
            "old_blueprint_sha256": sha256_bytes(old_blueprint),
            "new_blueprint_sha256": sha256_bytes(new_blueprint),
            "old_gantt_sha256": sha256_bytes(old_gantt),
            "new_gantt_sha256": sha256_bytes(new_gantt),
            "old_requirements_sha256": sha256_bytes(_requirements_region(old_blueprint)),
            "new_requirements_sha256": sha256_bytes(_requirements_region(new_blueprint)),
            "execution_spec_sha256": sha256_bytes(canonical(strict_json_loads(
                preserved_spec_region.decode("utf-8").strip()[8:-4], "preserved execution spec"
            ))),
            "checklist_task_authority_sha256": sha256_bytes(canonical(
                _checklist_dag_projection(current)
            )),
            "checklist_state_sha256": sha256_bytes(canonical([
                [task.item_id, state_name(task.state)] for task in current
            ])),
            "active_generations": active_generations,
            "active_generation_policy": "existing generations retain immutable claim baselines and may finish/handoff normally; no overlap, restart, goal resubmission or in-place baseline rewrite is authorized by this migration",
            "new_policy": "theorem work, lane, generation and goal states are independent; terminal generations require typed durable disposition/checkpoint before retirement; only complete_candidate is eligible for Master completion integration",
            "prompt_policy": "Blueprint contains no concurrency fallback; every successor prompt must explicitly supply all selected concurrency and lifecycle/recovery values",
            "preserved": [
                "mathematical TARGET IDs",
                "checklist states",
                "TARGET dependencies",
                "owned paths",
                "task gates",
                "embedded execution specification",
                "active generation claim baselines",
            ],
        }
        receipt = {**body, "authority_sha256": sha256_bytes(canonical(body))}
        receipt_bytes = json.dumps(
            receipt, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False
        ).encode("utf-8") + b"\n"
        atomic_batch_write(
            [
                (program.blueprint, new_blueprint),
                (program.gantt, new_gantt),
                (receipt_path, receipt_bytes),
            ],
            expected_old={
                program.blueprint: blueprint_guard,
                program.gantt: gantt_guard,
                receipt_path: None,
            },
            guards={state_path: state_guard} if state_guard is not None else {},
        )
    print(
        f"MIGRATED theorem lifecycle authority; receipt={receipt_path.relative_to(ROOT)} "
        f"active_generations_preserved={len(active_generations)}"
    )


def migrate_theorem_execution_prompt(
    *,
    confirm_concurrency: dict[str, Any] | None = None,
    authorize_worker_launch: bool = False,
) -> None:
    """CAS-refresh the theorem prompt and operator authority only.

    This narrow migration intentionally does not touch the conjecture
    Blueprint/spec, install cron, create runtime state, or start a worker.  A
    caller must provide the complete closed vector; no value is inferred.
    """
    if not isinstance(confirm_concurrency, dict):
        raise BlueprintError("theorem prompt migration requires an explicit complete concurrency object")
    expected = prompt_concurrency_values(THEOREM)
    if set(confirm_concurrency) == set(expected) | {"request_window_seconds"}:
        if confirm_concurrency.get("request_window_seconds") != 120:
            raise BlueprintError("confirmed request window differs from the reviewed 120-second window")
        confirm_vector = {key: confirm_concurrency[key] for key in expected}
    else:
        confirm_vector = confirm_concurrency
    if confirm_vector != expected:
        raise BlueprintError("confirmed concurrency object differs from the reviewed theorem vector")
    if not isinstance(authorize_worker_launch, bool):
        raise BlueprintError("worker launch authorization must be an explicit boolean")
    with theorem_scheduler_transition_guard(), manager_mutation_lock():
        recover_batch_transactions()
        active_generations: list[dict[str, Any]] = []
        runtime = ROOT / THEOREM.runtime_root
        if runtime.is_dir():
            state_path = runtime / "state/controller-state.json"
            if state_path.is_file() and not state_path.is_symlink():
                state = strict_json_loads(state_path.read_bytes(), "theorem runtime state")
                active_generations = [
                    {
                        "item_id": value.get("item_id"),
                        "generation_id": value.get("generation_id"),
                        "status": value.get("status"),
                        "prompt_digest": value.get("prompt_digest"),
                    }
                    for value in state.get("claims", {}).values()
                    if isinstance(value, dict) and value.get("status") in {
                        "reserved", "materialized", "tmux_started", "goal_pasted",
                        "request_reserved", "submission_committed", "goal_submitted", "live",
                    }
                ]
                active_generations.sort(key=lambda row: (
                    str(row["item_id"]), str(row["generation_id"]),
                ))
        blueprint_raw, blueprint_guard = regular_file_bytes(THEOREM.blueprint, "theorem Blueprint")
        gantt_raw, gantt_guard = regular_file_bytes(THEOREM.gantt, "theorem Gantt")
        spec_path = DOCS / "evidence/stage5_theorems/execution-spec.json"
        spec_raw, spec_guard = regular_file_bytes(spec_path, "theorem execution spec")
        prompt_path = ROOT / concurrency_prompt_path(THEOREM)
        authority_path = DOCS / "evidence/stage5_shared_execution/operator-budget-v1.json"
        trust_path = DOCS / "evidence/stage5_shared_execution/operator-budget-trust-root-v1.json"
        prompt_old, prompt_guard = regular_file_bytes(prompt_path, "theorem concurrency prompt")
        authority_old, authority_guard = regular_file_bytes(authority_path, "theorem operator authority")
        current_spec = strict_json_loads(spec_raw, "theorem execution spec")
        prompt = concurrency_prompt_object(THEOREM)
        prompt_bytes = concurrency_prompt_bytes(THEOREM)
        authority = operator_budget_authority_object(
            THEOREM, worker_launch_authorized=authorize_worker_launch,
        )
        authority_bytes = json.dumps(authority, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
        migration_path = next_concurrency_prompt_migration_receipt()
        body = {
            "schema_version": "awesome-theorems/stage5-concurrency-prompt-migration/2.0",
            "migration_id": migration_path.stem,
            "generated_at": utc_now(),
            "program": THEOREM.version,
            "pre": {
                "blueprint_sha256": sha256_bytes(blueprint_raw),
                "gantt_sha256": sha256_bytes(gantt_raw),
                "execution_spec_sha256": sha256_bytes(spec_raw),
                "prompt_sha256": sha256_bytes(prompt_old),
                "operator_authority_sha256": sha256_bytes(authority_old),
            },
            "post": {
                "blueprint_sha256": sha256_bytes(blueprint_raw),
                "gantt_sha256": sha256_bytes(gantt_raw),
                "execution_spec_sha256": sha256_bytes(spec_raw),
                "prompt_sha256": sha256_bytes(prompt_bytes),
                "operator_authority_sha256": sha256_bytes(authority_bytes),
                "policy_epoch": prompt["policy_epoch"],
                "concurrency": expected,
                "worker_launch_authorized": authorize_worker_launch,
            },
            "active_generations": active_generations,
            "active_generation_policy": "active generations retain immutable claim/prompt/spec baselines; only successor admissions bind the new prompt epoch, with no restart, overlap or second /goal",
            "scope": "theorem prompt/operator authority only; no runtime, cron, tmux, worker, conjecture or checklist mutation",
        }
        receipt = {**body, "authority_sha256": sha256_bytes(canonical(body))}
        receipt_bytes = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
        atomic_batch_write(
            [(prompt_path, prompt_bytes), (authority_path, authority_bytes), (migration_path, receipt_bytes)],
            expected_old={prompt_path: prompt_guard, authority_path: authority_guard, migration_path: None},
            guards={THEOREM.blueprint: blueprint_guard, THEOREM.gantt: gantt_guard, spec_path: spec_guard, trust_path: regular_file_expectation(trust_path)},
        )
    print(f"MIGRATED theorem prompt/operator authority; receipt={migration_path.relative_to(ROOT)}")


def replace_embedded_spec(blueprint_raw: bytes, specification: dict[str, Any]) -> bytes:
    text = blueprint_raw.decode("utf-8")
    if text.count(SPEC_BEGIN) != 1 or text.count(SPEC_END) != 1:
        raise BlueprintError("execution specification markers are not unique")
    before, tail = text.split(SPEC_BEGIN, 1)
    _, after = tail.split(SPEC_END, 1)
    block = f"\n```json\n{json.dumps(specification, ensure_ascii=False, sort_keys=True, indent=2)}\n```\n"
    return (before + SPEC_BEGIN + block + SPEC_END + after).encode("utf-8")


def migrate_concurrency_prompt_v4(programs: tuple[Program, ...]) -> None:
    """Install prompt-required vectors without resetting checklist progress."""
    if set(programs) != {THEOREM, CONJECTURE}:
        raise BlueprintError("concurrency-prompt migration must update both programs together")
    with manager_mutation_lock():
        recover_batch_transactions()
        validate_bootstrap_cron_absence()
        saved_runtime_snapshot = runtime_snapshot
        globals()["runtime_snapshot"] = lambda _program: (None, None)
        old_guards: dict[Path, FileExpectation | None] = {}
        outputs: list[tuple[Path, bytes]] = []
        records: dict[str, Any] = {}
        generated_at = utc_now()
        try:
            for program in programs:
                blueprint_raw, blueprint_guard = regular_file_bytes(program.blueprint, f"{program.kind} Blueprint")
                gantt_raw, gantt_guard = regular_file_bytes(program.gantt, f"{program.kind} Gantt")
                spec_path = DOCS / "evidence" / f"stage5_{program.kind}s" / "execution-spec.json"
                old_spec_raw, spec_guard = regular_file_bytes(spec_path, f"{program.kind} execution specification")
                expected = expected_tasks(program)
                tasks = parse_blueprint(
                    program, blueprint_raw, expected,
                    allow_boot_transition=True,
                    allow_superseded_authority_for_invalidation=True,
                    allow_immutable_row_drift=True,
                    allow_progress_cursor=True,
                    allow_legacy_execution_gate=True,
                )
                specification = spec_object(program)
                new_blueprint = replace_embedded_spec(blueprint_raw, specification)
                new_tasks = parse_blueprint(
                    program, new_blueprint, expected,
                    allow_boot_transition=True,
                    allow_superseded_authority_for_invalidation=True,
                    allow_immutable_row_drift=True,
                    allow_progress_cursor=True,
                )
                new_gantt = render_gantt(program, new_blueprint, new_tasks, generated_at)
                spec_bytes = json.dumps(specification, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False).encode("utf-8") + b"\n"
                prompt_path = ROOT / concurrency_prompt_path(program)
                prompt_bytes = json.dumps(concurrency_prompt_object(program), ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False).encode("utf-8") + b"\n"
                old_guards.update({program.blueprint: blueprint_guard, program.gantt: gantt_guard, spec_path: spec_guard, prompt_path: regular_file_expectation(prompt_path)})
                outputs.extend(((program.blueprint, new_blueprint), (program.gantt, new_gantt), (spec_path, spec_bytes), (prompt_path, prompt_bytes)))
                records[program.kind] = {
                    "program": program.version,
                    "old_blueprint_sha256": blueprint_guard.sha256,
                    "new_blueprint_sha256": sha256_bytes(new_blueprint),
                    "old_gantt_sha256": gantt_guard.sha256,
                    "new_gantt_sha256": sha256_bytes(new_gantt),
                    "old_spec_sha256": sha256_bytes(old_spec_raw),
                    "new_spec_sha256": sha256_bytes(spec_bytes),
                    "prompt_path": prompt_path.relative_to(ROOT).as_posix(),
                    "prompt_sha256": sha256_bytes(prompt_bytes),
                    "state_counts": dict(Counter(state_name(task.state) for task in tasks)),
                }
        finally:
            globals()["runtime_snapshot"] = saved_runtime_snapshot
        receipt_path = next_concurrency_prompt_migration_receipt()
        body = {
            "schema_version": "awesome-theorems/stage5-concurrency-prompt-migration/1.0",
            "migration_id": receipt_path.stem,
            "generated_at": generated_at,
            "programs": records,
            "policy": "Blueprints contain only the closed prompt contract; every numeric concurrency value is supplied by the explicit operator prompt fixture or a future prompt epoch, never by a skill/default/controller fallback",
            "lifecycle": "durable lanes own fresh nonoverlapping generations; old generations are harvested/fenced before lane reuse; parallel admission waves execute outside the scheduler lease",
            "scope": "Harness execution and Stage5 proof-debt Blueprint/spec/Gantt authorities only; no gateway/WebSocket behavior is changed",
        }
        receipt = {**body, "authority_sha256": sha256_bytes(canonical(body))}
        receipt_bytes = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
        old_guards[receipt_path] = None
        def boundary() -> None:
            validate_bootstrap_cron_absence()
            for program in programs:
                if path_lexists(ROOT / program.runtime_root):
                    snapshot = ROOT / program.runtime_root / "status/runtime-snapshot.json"
                    if snapshot.is_file():
                        value = strict_json_loads(snapshot.read_bytes(), f"{program.kind} runtime snapshot")
                        live = value.get("authenticated_live_goals", 0) if isinstance(value, dict) else 0
                        if live:
                            raise BlueprintError(f"{program.kind}: prompt migration refuses live generations")
        atomic_batch_write(
            [*outputs, (receipt_path, receipt_bytes)],
            expected_old=old_guards,
            guards=source_input_expectations(programs),
            precommit_validator=boundary,
        )
    print(f"MIGRATED prompt-required concurrency for theorem+conjecture; receipt={receipt_path.relative_to(ROOT)}")


def _render_ongoing_conjecture_gantt(
    blueprint: bytes, generated_at: str | None = None
) -> bytes:
    generator_path = DOCS / "tools/generate_stage5_conjectures_gantt.py"
    module_spec = importlib.util.spec_from_file_location(
        "stage5_conjecture_prompt_gantt_migration", generator_path
    )
    if module_spec is None or module_spec.loader is None:
        raise BlueprintError("ongoing conjecture Gantt generator is unavailable")
    module = importlib.util.module_from_spec(module_spec)
    import sys
    sys.modules[module_spec.name] = module
    module_spec.loader.exec_module(module)
    descriptor, temporary = tempfile.mkstemp(prefix="stage5-conjecture-prompt-", suffix=".md")
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(blueprint)
            stream.flush()
            os.fsync(stream.fileno())
        original = module.BLUEPRINT
        module.BLUEPRINT = Path(temporary)
        try:
            return module.render(generated_at)
        finally:
            module.BLUEPRINT = original
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


@contextmanager
def conjecture_scheduler_transition_guard() -> Iterator[None]:
    """Exclude conjecture controller admission while authority bytes change."""
    path = ROOT / ".ops/stage5-conjectures-execution-v2.scheduler.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_RDWR | os.O_CREAT | getattr(os, "O_CLOEXEC", 0), 0o600)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise BlueprintError("conjecture controller transition is active; retry prompt-policy migration") from exc
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def _conjecture_boot_data_bytes(
    blueprint: bytes, specification: dict[str, Any]
) -> dict[Path, bytes]:
    checker_path = DOCS / "tools/check_stage5_conjectures_blueprint.py"
    module_spec = importlib.util.spec_from_file_location(
        "stage5_conjecture_prompt_boot_data_migration", checker_path
    )
    if module_spec is None or module_spec.loader is None:
        raise BlueprintError("conjecture checker is unavailable")
    module = importlib.util.module_from_spec(module_spec)
    import sys
    sys.modules[module_spec.name] = module
    module_spec.loader.exec_module(module)
    descriptor, temporary = tempfile.mkstemp(prefix="stage5-conjecture-prompt-blueprint-", suffix=".md")
    original_blueprint = module.BLUEPRINT
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(blueprint)
            stream.flush()
            os.fsync(stream.fileno())
        module.BLUEPRINT = Path(temporary)
        captured = module.render_boot_data()
    finally:
        module.BLUEPRINT = original_blueprint
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
    expected_spec = json.dumps(
        specification, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False
    ).encode("utf-8") + b"\n"
    if captured.get(module.EXECUTION_SPEC) != expected_spec:
        raise BlueprintError("conjecture BOOT-data preparer produced a different execution specification")
    return captured


def migrate_conjecture_prompt_policy_v6() -> None:
    """Install the proof-search contract and invalidate weaker TARGET handoffs."""
    program = CONJECTURE
    with conjecture_scheduler_transition_guard(), manager_mutation_lock():
        recover_batch_transactions()
        blueprint_raw, blueprint_guard = regular_file_bytes(program.blueprint, "conjecture Blueprint")
        gantt_raw, gantt_guard = regular_file_bytes(program.gantt, "conjecture Gantt")
        expected = expected_tasks(program)
        current = parse_blueprint(
            program, blueprint_raw, expected,
            allow_boot_transition=True,
            allow_superseded_authority_for_invalidation=True,
            allow_immutable_row_drift=True,
            allow_progress_cursor=True,
            allow_legacy_execution_gate=True,
        )
        state_path = ROOT / program.runtime_root / "state/controller-state.json"
        active_generations: list[dict[str, Any]] = []
        if state_path.is_file() and not state_path.is_symlink():
            value = strict_json_loads(state_path.read_bytes(), "conjecture controller state")
            reservations = value.get("reservations", []) if isinstance(value, dict) else []
            if any(isinstance(row, dict) and row.get("status") == "reserved" for row in reservations):
                raise BlueprintError("conjecture prompt-policy migration refuses persisted reservations")
            claims = value.get("claims", {}) if isinstance(value, dict) else {}
            if isinstance(claims, dict):
                active_generations = [
                    {"item_id": item_id, "status": claim.get("status"), "run_id": claim.get("run_id")}
                    for item_id, claim in claims.items()
                    if isinstance(claim, dict) and claim.get("status") in {"materialized", "goal_submitted", "live"}
                ]
        if active_generations:
            raise BlueprintError("conjecture prompt-policy migration refuses active generations")
        invalidated = [
            task.item_id for task in current
            if task.item_id.endswith("-TARGET") and task.state != " "
        ]
        boot_id = "S5CON-BOOT-001"
        replacement = [
            template.with_state(
                " " if template.item_id in invalidated
                else next(task.state for task in current if task.item_id == template.item_id)
            )
            for template in expected
        ]
        if next(task.state for task in replacement if task.item_id == boot_id) != "x":
            raise BlueprintError("conjecture BOOT must remain accepted during prompt-policy migration")
        new_blueprint = render_blueprint(program, replacement)
        reparsed = parse_blueprint(
            program, new_blueprint, expected,
            allow_boot_transition=True,
            allow_superseded_authority_for_invalidation=True,
            allow_immutable_row_drift=True,
            allow_progress_cursor=True,
        )
        if [task.item_id for task in current] != [task.item_id for task in reparsed]:
            raise BlueprintError("conjecture prompt-policy migration changed item identities")
        specification = spec_object(program)
        boot_outputs = _conjecture_boot_data_bytes(new_blueprint, specification)
        prompt_path = ROOT / concurrency_prompt_path(program)
        # Build the explicit prompt against the successor spec rather than the
        # currently installed predecessor spec.
        spec_path = DOCS / "evidence/stage5_conjectures/execution-spec.json"
        spec_bytes = boot_outputs[spec_path]
        prompt_body = {
            "schema_version": CONCURRENCY_PROMPT_SCHEMA,
            "program": program.version,
            "policy_epoch": concurrency_prompt_epoch(program),
            "execution_spec_sha256": sha256_bytes(canonical(specification)),
            "operator_identity": f"codex-user-goal:{operator_goal_binding(program)[0]}",
            "operator_goal_thread_id": operator_goal_binding(program)[0],
            "operator_goal_objective_sha256": operator_goal_binding(program)[1],
            "request_window_seconds": 120,
            "source": "explicit operator prompt fixture; not a controller or Blueprint default",
            "concurrency": prompt_concurrency_values(program),
            "execution_limits": concurrency_prompt_contract(program)["execution_limits"],
            "recovery": concurrency_prompt_contract(program)["recovery"],
        }
        prompt_value = {**prompt_body, "authority_sha256": sha256_bytes(canonical(prompt_body))}
        prompt_bytes = json.dumps(prompt_value, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
        generated_at = utc_now()
        saved_runtime_snapshot = runtime_snapshot
        try:
            generator_path = DOCS / "tools/generate_stage5_conjectures_gantt.py"
            generator_spec = importlib.util.spec_from_file_location(
                "stage5_conjecture_prompt_runtime_snapshot", generator_path
            )
            if generator_spec is None or generator_spec.loader is None:
                raise BlueprintError("conjecture Gantt snapshot loader is unavailable")
            generator = importlib.util.module_from_spec(generator_spec)
            import sys
            sys.modules[generator_spec.name] = generator
            generator_spec.loader.exec_module(generator)
            globals()["runtime_snapshot"] = generator.snapshot_loader
            new_gantt = render_gantt(
                program, new_blueprint, reparsed, generated_at,
                prompt_override=prompt_bytes,
            )
        finally:
            globals()["runtime_snapshot"] = saved_runtime_snapshot
        evidence_paths = {
            path: raw for path, raw in boot_outputs.items()
            if path in {
                DOCS / "evidence/stage5_conjectures/workset-5.6.json",
                DOCS / "evidence/stage5_conjectures/workset-5.6-receipt.json",
                spec_path,
                DOCS / "evidence/stage5_conjectures/foundation-profiles.json",
                DOCS / "evidence/stage5_conjectures/provider-registry.json",
                DOCS / "evidence/stage5_conjectures/claim-card.schema.json",
                DOCS / "evidence/stage5_conjectures/worker-result.schema.json",
                DOCS / "evidence/stage5_conjectures/master-acceptance.schema.json",
            }
        }
        if len(evidence_paths) != 8:
            raise BlueprintError("conjecture BOOT-data successor output set is incomplete")
        integration_entries: list[dict[str, Any]] = []
        integration_root = ROOT / program.runtime_root / "integration"
        for path in sorted(integration_root.glob("*.json")) if integration_root.is_dir() else []:
            raw = path.read_bytes()
            value = strict_json_loads(raw, f"legacy integration entry {path.name}")
            item_id = value.get("item_id") if isinstance(value, dict) else None
            if item_id in {
                "S5CON-00003486-TARGET", "S5CON-00003487-TARGET",
                "S5CON-00003488-TARGET", "S5CON-00003490-TARGET",
                "S5CON-00003494-TARGET", "S5CON-00003498-TARGET",
                "S5CON-00003499-TARGET", "S5CON-00003500-TARGET",
            }:
                integration_entries.append({
                    "item_id": item_id,
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": sha256_bytes(raw),
                    "disposition": "historical_only_rejected_by_current_claim_validator",
                })
        receipt_path = next_conjecture_prompt_policy_migration_receipt()
        previous_receipts = conjecture_prompt_policy_migration_receipts()
        body = {
            "schema_version": "awesome-theorems/stage5-conjecture-prompt-policy-migration/1.0",
            "migration_id": receipt_path.stem,
            "generated_at": utc_now(),
            "program": program.version,
            "source": conjecture_proof_search_prompt_contract()["source"],
            "old_blueprint_sha256": blueprint_guard.sha256,
            "new_blueprint_sha256": sha256_bytes(new_blueprint),
            "old_gantt_sha256": gantt_guard.sha256,
            "new_gantt_sha256": sha256_bytes(new_gantt),
            "new_execution_spec_sha256": sha256_bytes(spec_bytes),
            "new_prompt_sha256": sha256_bytes(prompt_bytes),
            "artifact_sha256": {
                path.relative_to(ROOT).as_posix(): sha256_bytes(raw)
                for path, raw in sorted(evidence_paths.items(), key=lambda row: row[0].as_posix())
            },
            "code_sha256": {
                "manager": manager_code_sha256(),
                "checker": sha256_bytes((DOCS / "tools/check_stage5_conjectures_blueprint.py").read_bytes()),
                "gantt_generator": sha256_bytes((DOCS / "tools/generate_stage5_conjectures_gantt.py").read_bytes()),
                "controller": sha256_bytes((ROOT / "scripts/stage5_conjectures_execution_cron_v2.py").read_bytes()),
                "claim_validator": sha256_bytes((ROOT / "scripts/check_stage5_conjecture_claim.py").read_bytes()),
                "handoff_transition": sha256_bytes((ROOT / "scripts/stage5_conjecture_handoff_transition.py").read_bytes()),
            },
            "previous_prompt_policy_receipt": (
                {
                    "path": previous_receipts[-1].relative_to(ROOT).as_posix(),
                    "sha256": sha256_bytes(previous_receipts[-1].read_bytes()),
                }
                if previous_receipts else None
            ),
            "old_state_counts": dict(Counter(state_name(task.state) for task in current)),
            "new_state_counts": dict(Counter(state_name(task.state) for task in reparsed)),
            "invalidated_target_item_ids": invalidated,
            "invalidation_reason": "prior handoffs did not bind the new durable approach-family registry, theorem-equivalent-gap blocking, adversarial-audit and exact-closure contract",
            "preserved": ["mathematical TARGET IDs", "TARGET dependencies", "owned paths", "BOOT acceptance", "historical handoff archives"],
            "route": {"provider": "sub2api", "model": "gpt-5.6-sol", "reasoning_effort": "ultra", "service_tier": "default"},
            "runtime_policy": "no worker, tmux, goal, controller tick, cron or gateway/WebSocket behavior is launched or changed",
            "active_generations": active_generations,
            "legacy_integration_dispositions": integration_entries,
        }
        receipt = {**body, "authority_sha256": sha256_bytes(canonical(body))}
        receipt_bytes = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
        outputs = [
            (program.blueprint, new_blueprint),
            (program.gantt, new_gantt),
            *sorted(evidence_paths.items(), key=lambda row: row[0].as_posix()),
            (prompt_path, prompt_bytes),
            (receipt_path, receipt_bytes),
        ]
        expected_old = {path: regular_file_expectation(path) for path, _ in outputs}
        expected_old[receipt_path] = None
        def boundary() -> None:
            if state_path.is_file() and not state_path.is_symlink():
                state = strict_json_loads(state_path.read_bytes(), "conjecture controller state")
                reservations = state.get("reservations", []) if isinstance(state, dict) else []
                if any(isinstance(row, dict) and row.get("status") == "reserved" for row in reservations):
                    raise BlueprintError("conjecture reservation appeared during prompt-policy migration")
                claims = state.get("claims", {}) if isinstance(state, dict) else {}
                if any(
                    isinstance(claim, dict) and claim.get("status") in {"materialized", "goal_submitted", "live"}
                    for claim in claims.values()
                ):
                    raise BlueprintError("conjecture generation became active during prompt-policy migration")
        atomic_batch_write(
            outputs,
            expected_old=expected_old,
            guards=source_input_expectations((program,)),
            precommit_validator=boundary,
        )
    print(f"MIGRATED conjecture proof-search prompt policy; receipt={receipt_path.relative_to(ROOT)} invalidated={len(invalidated)}")


def validate_conjecture_prompt_policy_migration_receipt(
    tasks: list[Task], blueprint_raw: bytes, gantt_raw: bytes
) -> None:
    receipts = conjecture_prompt_policy_migration_receipts()
    if not receipts:
        raise BlueprintError("conjecture prompt-policy migration receipt is missing")
    path = receipts[-1]
    value = strict_json_loads(path.read_bytes(), "conjecture prompt-policy migration receipt")
    if not isinstance(value, dict):
        raise BlueprintError("conjecture prompt-policy migration receipt is malformed")
    authority = value.get("authority_sha256")
    body = dict(value); body.pop("authority_sha256", None)
    if (
        value.get("schema_version") != "awesome-theorems/stage5-conjecture-prompt-policy-migration/1.0"
        or value.get("migration_id") != path.stem
        or value.get("program") != CONJECTURE.version
        or not isinstance(authority, str)
        or sha256_bytes(canonical(body)) != authority
        or value.get("new_blueprint_sha256") != sha256_bytes(blueprint_raw)
        or value.get("new_gantt_sha256") != sha256_bytes(gantt_raw)
        or value.get("new_state_counts") != dict(Counter(state_name(task.state) for task in tasks))
        or value.get("route") != {"provider": "sub2api", "model": "gpt-5.6-sol", "reasoning_effort": "ultra", "service_tier": "default"}
        or value.get("source") != conjecture_proof_search_prompt_contract()["source"]
    ):
        raise BlueprintError("conjecture prompt-policy migration receipt binding differs")
    artifacts = value.get("artifact_sha256")
    code = value.get("code_sha256")
    expected_artifacts = {
        path.relative_to(ROOT).as_posix(): sha256_bytes(path.read_bytes())
        for path in (
            DOCS / "evidence/stage5_conjectures/workset-5.6.json",
            DOCS / "evidence/stage5_conjectures/workset-5.6-receipt.json",
            DOCS / "evidence/stage5_conjectures/execution-spec.json",
            DOCS / "evidence/stage5_conjectures/foundation-profiles.json",
            DOCS / "evidence/stage5_conjectures/provider-registry.json",
            DOCS / "evidence/stage5_conjectures/claim-card.schema.json",
            DOCS / "evidence/stage5_conjectures/worker-result.schema.json",
            DOCS / "evidence/stage5_conjectures/master-acceptance.schema.json",
        )
    }
    expected_code = {
        "manager": manager_code_sha256(),
        "checker": sha256_bytes((DOCS / "tools/check_stage5_conjectures_blueprint.py").read_bytes()),
        "gantt_generator": sha256_bytes((DOCS / "tools/generate_stage5_conjectures_gantt.py").read_bytes()),
        "controller": sha256_bytes((ROOT / "scripts/stage5_conjectures_execution_cron_v2.py").read_bytes()),
        "claim_validator": sha256_bytes((ROOT / "scripts/check_stage5_conjecture_claim.py").read_bytes()),
        "handoff_transition": sha256_bytes((ROOT / "scripts/stage5_conjecture_handoff_transition.py").read_bytes()),
    }
    prompt_path = ROOT / concurrency_prompt_path(CONJECTURE)
    spec_path = DOCS / "evidence/stage5_conjectures/execution-spec.json"
    if (
        artifacts != expected_artifacts
        or code != expected_code
        or value.get("new_execution_spec_sha256") != sha256_bytes(spec_path.read_bytes())
        or value.get("new_prompt_sha256") != sha256_bytes(prompt_path.read_bytes())
    ):
        raise BlueprintError("conjecture prompt-policy artifact/code binding differs")
    previous = value.get("previous_prompt_policy_receipt")
    if previous is not None:
        previous_path = ROOT / str(previous.get("path", ""))
        if (
            not previous_path.is_file() or previous_path.is_symlink()
            or sha256_bytes(previous_path.read_bytes()) != previous.get("sha256")
        ):
            raise BlueprintError("conjecture prompt-policy predecessor receipt differs")


def validate_one_object_v2_migration_receipt(
    program: Program, tasks: list[Task], blueprint_raw: bytes, gantt_raw: bytes
) -> None:
    if not OBJECT_WORKER_V2_MIGRATION_RECEIPT.is_file() or OBJECT_WORKER_V2_MIGRATION_RECEIPT.is_symlink():
        raise BlueprintError("one-object v2 migration receipt is missing")
    receipt = strict_json_loads(
        OBJECT_WORKER_V2_MIGRATION_RECEIPT.read_bytes(), "one-object v2 migration receipt"
    )
    if not isinstance(receipt, dict):
        raise BlueprintError("one-object v2 migration receipt is not an object")
    authority = receipt.get("authority_sha256")
    body = dict(receipt)
    body.pop("authority_sha256", None)
    if (
        receipt.get("schema_version")
        != "awesome-theorems/stage5-one-object-one-goal-migration/1.0"
        or not isinstance(authority, str)
        or not SHA256_RE.fullmatch(authority)
        or sha256_bytes(canonical(body)) != authority
    ):
        raise BlueprintError("one-object v2 migration receipt authority differs")
    record = receipt.get("programs", {}).get(program.kind)
    legacy = LEGACY_V1_MIGRATION_AUTHORITIES[program.kind]
    if not isinstance(record, dict):
        raise BlueprintError(f"{program.kind}: migration program record is missing")
    expected_fields = {
        "program": legacy["program"],
        "blueprint_sha256": legacy["blueprint_sha256"],
        "gantt_sha256": legacy["gantt_sha256"],
        "checklist_item_count": legacy["row_count"],
        "mathematical_phase_row_count": legacy["mathematical_row_count"],
        "v2_program": program.version,
        "v2_blueprint_sha256": sha256_bytes(blueprint_raw),
        "v2_checklist_item_count": len(tasks),
        "v2_target_count": program.target_count,
    }
    for key, expected in expected_fields.items():
        if record.get(key) != expected:
            raise BlueprintError(f"{program.kind}: migration receipt {key} differs")
    if not isinstance(record.get("v2_gantt_sha256"), str) or not SHA256_RE.fullmatch(
        record["v2_gantt_sha256"]
    ):
        raise BlueprintError(f"{program.kind}: initial v2 Gantt digest is malformed")
    if record.get("v2_initial_state_counts") != {
        "not_done": len(tasks),
        "handoff_waiting_master": 0,
        "master_accepted": 0,
    }:
        raise BlueprintError(f"{program.kind}: v2 initial migration state differs")
    if any(task.state != " " for task in tasks):
        raise BlueprintError(f"{program.kind}: migrated scaffold is no longer all blank")
    for path in (ROOT / program.runtime_root, ROOT / SHARED_RUNTIME_ROOT):
        if path_lexists(path):
            raise BlueprintError(
                f"{program.kind}: migrated scaffold check refuses v2 runtime surface "
                f"{path.relative_to(ROOT)}"
            )


def validate_program_isolation_migration_receipt(
    program: Program, tasks: list[Task], blueprint_raw: bytes, gantt_raw: bytes
) -> None:
    """Validate the narrow v2->v3 program-isolation migration receipt."""
    path = latest_program_isolation_migration_receipt()
    if path is None:
        return
    receipt = strict_json_loads(path.read_bytes(), "program-isolation migration receipt")
    if not isinstance(receipt, dict):
        raise BlueprintError("program-isolation migration receipt is not an object")
    authority = receipt.get("authority_sha256")
    body = dict(receipt)
    body.pop("authority_sha256", None)
    if (
        receipt.get("schema_version") != "awesome-theorems/stage5-program-isolation-migration/1.0"
        or not re.fullmatch(
            r"S5PD-BLUEPRINT-MIGRATE-[0-9]{6}", str(receipt.get("migration_id"))
        )
        or not isinstance(authority, str)
        or not SHA256_RE.fullmatch(authority)
        or sha256_bytes(canonical(body)) != authority
    ):
        raise BlueprintError("program-isolation migration receipt authority differs")
    record = receipt.get("programs", {}).get(program.kind)
    if not isinstance(record, dict):
        raise BlueprintError(f"{program.kind}: program-isolation migration record missing")
    current_sha = sha256_bytes(blueprint_raw)
    observed_counts = dict(Counter(state_name(task.state) for task in tasks))
    counts_match = record.get("new_state_counts") == observed_counts
    boot_post_transition = (
        program.kind == "theorem"
        and tasks
        and tasks[0].item_id == "S5THM-BOOT-001"
        and tasks[0].state in {"_", "x"}
        and all(task.state == " " for task in tasks[1:])
    )
    if (
        record.get("program") != program.version
        or record.get("row_count") != len(tasks)
        or record.get("target_count") != program.target_count
        or (not counts_match and not boot_post_transition)
    ):
        raise BlueprintError(f"{program.kind}: program-isolation migration binding differs")
    if record.get("new_blueprint_sha256") != current_sha:
        # BOOT acceptance is the first legal cursor transition after the
        # migration.  Bind the current bytes to its immutable acceptance
        # receipt instead of treating the migration predecessor digest as
        # stale authority.
        _, handoff_acceptance_path, _, acceptance_path = boot_receipt_paths(program)
        if (
            program.kind == "theorem"
            and not acceptance_path.is_file()
            and handoff_acceptance_path.is_file()
            and tasks[0].state == "_"
            and all(task.state == " " for task in tasks[1:])
        ):
            provisional = strict_json_loads(handoff_acceptance_path.read_bytes(), "BOOT handoff acceptance")
            if (
                provisional.get("program") == program.version
                and provisional.get("post_blueprint_sha256") == current_sha
                and provisional.get("post_gantt_sha256") == sha256_bytes(gantt_raw)
            ):
                return
        if (
            program.kind != "theorem"
            or not acceptance_path.is_file()
            or acceptance_path.is_symlink()
        ):
            raise BlueprintError(f"{program.kind}: post-migration Blueprint has no accepted transition receipt")
        acceptance = strict_json_loads(acceptance_path.read_bytes(), "BOOT acceptance")
        authority = acceptance.get("authority_sha256")
        unsigned = dict(acceptance)
        unsigned.pop("authority_sha256", None)
        if (
            not isinstance(authority, str)
            or sha256_bytes(canonical(unsigned)) != authority
            or acceptance.get("program") != program.version
            or acceptance.get("cron_activated") is not False
            or acceptance.get("post_blueprint_sha256") != current_sha
            or tasks[0].item_id != "S5THM-BOOT-001"
            or tasks[0].state != "x"
            or any(task.state != " " for task in tasks[1:])
        ):
            raise BlueprintError("post-migration theorem Blueprint is not bound by BOOT acceptance")
    if body.get("preserved") != [
        "mathematical TARGET IDs", "TARGET dependencies", "owned paths", "DAG and terminal ancestry"
    ]:
        raise BlueprintError("program-isolation migration preservation contract differs")


def source_input_paths(programs: Iterable[Program]) -> tuple[Path, ...]:
    selected = tuple(programs)
    paths = {
        STAGE5_CURRENT,
        STAGE5_MANIFEST,
        STAGE6_CURRENT,
        STAGE6_MANIFEST,
        STAGE6_REGISTRY,
        STAGE6_MIGRATION,
        M0387_META,
        M0387_PROOF_UNITS,
        M0387_CURRENT_RECEIPT,
        M0387_CRITICAL_AUDIT,
    }
    if any(program.kind == "theorem" for program in selected):
        paths.add(THEOREM_SOURCE)
    if any(program.kind == "conjecture" for program in selected):
        paths.update((
            STRICT_SOURCE, OPEN_SOURCE, CROUZEIX_PROMPT_EXTRACTION,
            CONJECTURE_POOL_CURRENT, CONJECTURE_POOL_MANIFEST,
            CONJECTURE_POOL_OCCURRENCES, CONJECTURE_POOL_IDENTITIES,
            DOCS / "catalog/v5/sources/conjecturebench-357bcb1a-full-source.tar.gz",
        ))
    return tuple(sorted(paths))


def source_input_expectations(programs: Iterable[Program]) -> dict[Path, FileExpectation]:
    result: dict[Path, FileExpectation] = {}
    for path in source_input_paths(programs):
        expectation = regular_file_expectation(path)
        if expectation is None:
            raise BlueprintError(f"missing pinned source input: {path.relative_to(ROOT)}")
        result[path] = expectation
    return result


def validate_source_authorities_fresh(programs: Iterable[Program]) -> None:
    validate_stage5_release_chain.cache_clear()
    validate_m0387_negative_fixture.cache_clear()
    stage6_aliases.cache_clear()
    conjecture_occurrence_inventory.cache_clear()
    for program in programs:
        source_bundle_object(program)


def validate_force_pair(
    program: Program, tasks: list[Task], force: bool
) -> tuple[FileExpectation | None, FileExpectation | None]:
    blueprint_exists = path_lexists(program.blueprint)
    gantt_exists = path_lexists(program.gantt)
    for path in (program.blueprint, program.gantt):
        validate_output_path(path)
    blueprint_expectation = regular_file_expectation(program.blueprint)
    gantt_expectation = regular_file_expectation(program.gantt)
    if not force:
        if blueprint_exists or gantt_exists:
            raise BlueprintError(
                f"refusing to overwrite existing {program.kind} Blueprint/Gantt without --force"
            )
        return None, None
    if not blueprint_exists:
        if gantt_exists:
            raise BlueprintError(f"{program.kind}: orphan Gantt cannot be force-replaced")
        return None, None
    blueprint_raw = program.blueprint.read_bytes()
    gantt_raw = program.gantt.read_bytes() if gantt_exists else None
    validate_file_expectation(program.blueprint, blueprint_expectation)
    validate_file_expectation(program.gantt, gantt_expectation)
    reviewed = REVIEWED_PRISTINE_FORCE_PAIRS[program.kind]
    if (
        gantt_raw is not None
        and sha256_bytes(blueprint_raw) == reviewed["blueprint_sha256"]
        and sha256_bytes(gantt_raw) == reviewed["gantt_sha256"]
    ):
        return blueprint_expectation, gantt_expectation
    parsed = parse_blueprint(program, blueprint_raw, tasks)
    if any(task.state != " " for task in parsed):
        raise BlueprintError(f"{program.kind}: forced Blueprint is not wholly blank")
    if gantt_raw is None:
        return blueprint_expectation, None
    generated_at = extract_generated_at(gantt_raw)
    canonical_gantt = render_gantt(program, blueprint_raw, parsed, generated_at)
    if gantt_raw != canonical_gantt:
        raise BlueprintError(
            f"{program.kind}: --force accepts only current canonical blank bytes or the "
            "explicit reviewed pristine legacy pair"
        )
    return blueprint_expectation, gantt_expectation


def prepare_bootstrap(programs: tuple[Program, ...], force: bool) -> list[PreparedProgram]:
    validate_canonical_root()
    validate_marker_constants()
    validate_bootstrap_cron_absence()
    validate_shared_execution_history_absence()
    if path_lexists(ROOT / SHARED_RUNTIME_ROOT):
        raise BlueprintError("bootstrap forbidden after shared coordinator/runtime exists")
    generated_at = utc_now()
    task_sets = [(program, expected_tasks(program)) for program in programs]
    validate_cross_program_ownership(task_sets)
    prepared: list[PreparedProgram] = []
    for program, tasks in task_sets:
        validate_no_execution_history(program, tasks)
        blueprint = render_blueprint(program, tasks)
        parsed = parse_blueprint(program, blueprint, tasks)
        gantt = render_gantt(program, blueprint, parsed, generated_at)
        expected_blueprint, expected_gantt = validate_force_pair(program, tasks, force)
        prepared.append(
            PreparedProgram(
                program,
                tuple(tasks),
                blueprint,
                gantt,
                expected_blueprint,
                expected_gantt,
            )
        )
    return prepared


def bootstrap_programs(programs: tuple[Program, ...], force: bool) -> None:
    with manager_mutation_lock():
        recover_batch_transactions()
        source_guards = source_input_expectations(programs)
        prepared = prepare_bootstrap(programs, force)
        for path, expectation in source_guards.items():
            validate_file_expectation(path, expectation)
        outputs = [
            output
            for item in prepared
            for output in (
                (item.program.blueprint, item.blueprint),
                (item.program.gantt, item.gantt),
            )
        ]
        expected_old = {
            path: expectation
            for item in prepared
            for path, expectation in (
                (item.program.blueprint, item.expected_blueprint),
                (item.program.gantt, item.expected_gantt),
            )
        }

        def final_bootstrap_boundary() -> None:
            validate_bootstrap_cron_absence()
            validate_shared_execution_history_absence()
            validate_source_authorities_fresh(programs)
            if path_lexists(ROOT / SHARED_RUNTIME_ROOT):
                raise BlueprintError("shared runtime appeared after bootstrap preflight")
            for item in prepared:
                validate_no_execution_history(item.program, list(item.tasks))

        atomic_batch_write(
            outputs,
            expected_old=expected_old,
            guards=source_guards,
            precommit_validator=final_bootstrap_boundary,
        )
    for item in prepared:
        print(f"WROTE {item.program.blueprint.relative_to(ROOT)} rows={len(item.tasks)}")
        print(f"WROTE {item.program.gantt.relative_to(ROOT)} rows={len(item.tasks)}")


def render_projections(programs: tuple[Program, ...]) -> None:
    with manager_mutation_lock():
        recover_batch_transactions()
        generated_at = utc_now()
        prepared: list[
            tuple[Program, list[Task], bytes, FileExpectation, FileExpectation | None]
        ] = []
        task_sets: list[tuple[Program, list[Task]]] = []
        validate_bootstrap_cron_absence()
        migrated = path_lexists(OBJECT_WORKER_V2_MIGRATION_RECEIPT)
        if not migrated:
            validate_shared_execution_history_absence()
        source_guards = source_input_expectations(programs)
        for program in programs:
            expected = expected_tasks(program)
            blueprint_expectation = regular_file_expectation(program.blueprint)
            if blueprint_expectation is None:
                raise BlueprintError(f"missing Blueprint: {program.blueprint}")
            gantt_expectation = regular_file_expectation(program.gantt)
            raw = program.blueprint.read_bytes()
            validate_file_expectation(program.blueprint, blueprint_expectation)
            tasks = parse_blueprint(
                program, raw, expected,
                allow_boot_transition=migrated,
                allow_superseded_authority_for_invalidation=migrated,
                allow_immutable_row_drift=migrated,
            )
            gantt = render_gantt(program, raw, tasks, generated_at)
            if migrated:
                for path in (ROOT / program.runtime_root, ROOT / SHARED_RUNTIME_ROOT):
                    if path_lexists(path):
                        raise BlueprintError(
                            f"{program.kind}: migration bootstrap renderer refuses v2 runtime"
                        )
            else:
                validate_no_execution_history(program, tasks)
            prepared.append(
                (program, tasks, gantt, blueprint_expectation, gantt_expectation)
            )
            task_sets.append((program, tasks))
        validate_cross_program_ownership(task_sets)

        def final_render_boundary() -> None:
            validate_bootstrap_cron_absence()
            if not migrated:
                validate_shared_execution_history_absence()
            validate_source_authorities_fresh(programs)
            for program, tasks, _, _, _ in prepared:
                runtime_snapshot(program)
                if not migrated:
                    validate_no_execution_history(program, tasks)

        atomic_batch_write(
            [(program.gantt, gantt) for program, _, gantt, _, _ in prepared],
            expected_old={program.gantt: old for program, _, _, _, old in prepared},
            guards={
                **source_guards,
                **{program.blueprint: guard for program, _, _, guard, _ in prepared},
            },
            precommit_validator=final_render_boundary,
        )
    for program, tasks, _, _, _ in prepared:
        print(f"WROTE {program.gantt.relative_to(ROOT)} rows={len(tasks)}")


def check(program: Program) -> None:
    validate_bootstrap_cron_absence()
    validate_shared_execution_history_absence()
    expected = expected_tasks(program)
    blueprint_raw = program.blueprint.read_bytes()
    prompt_policy_active = (
        program.kind == "conjecture"
        and bool(conjecture_prompt_policy_migration_receipts())
    )
    migrated = program_isolation_active(program) or prompt_policy_active
    tasks = parse_blueprint(
        program, blueprint_raw, expected,
        allow_boot_transition=migrated,
        allow_superseded_authority_for_invalidation=migrated,
        allow_immutable_row_drift=migrated,
        # Program-isolation migration is reviewed evidence that may preserve
        # an existing BOOT/worker cursor.  The canonical checker must validate
        # that cursor rather than treating preserved progress as bootstrap
        # drift; BOOT acceptance itself still uses its narrower transition
        # rules above.
        allow_progress_cursor=migrated,
    )
    gantt_raw = program.gantt.read_bytes()
    generated_at = extract_generated_at(gantt_raw)
    expected_gantt = (
        _render_ongoing_conjecture_gantt(blueprint_raw, generated_at)
        if prompt_policy_active else
        render_gantt(program, blueprint_raw, tasks, generated_at)
    )
    if gantt_raw != expected_gantt:
        raise BlueprintError(f"{program.kind}: Gantt is stale or noncanonical")
    if (
        path_lexists(OBJECT_WORKER_V2_MIGRATION_RECEIPT)
        and program.kind == "theorem"
        and program.blueprint == THEOREM.blueprint
        and not program_isolation_active(program)
    ):
        validate_one_object_v2_migration_receipt(
            program, tasks, blueprint_raw, gantt_raw
        )
    if prompt_policy_active:
        validate_conjecture_prompt_policy_migration_receipt(
            tasks, blueprint_raw, gantt_raw
        )
    elif program_isolation_active(program):
        validate_program_isolation_migration_receipt(
            program, tasks, blueprint_raw, gantt_raw
        )
    else:
        validate_no_execution_history(program, tasks)
    index_text = gantt_raw.decode("utf-8").split(GANTT_INDEX_BEGIN, 1)[1].split(GANTT_INDEX_END, 1)[0]
    indexed_ids = re.findall(r'^\| "([A-Z0-9-]+)" \|', index_text, re.MULTILINE)
    if indexed_ids != [task.item_id for task in tasks]:
        raise BlueprintError(f"{program.kind}: Gantt monitoring coverage/order drift")
    counts = Counter(state_name(task.state) for task in tasks)
    print(
        f"PASS {program.kind} blueprint rows={len(tasks)} targets={program.target_count} "
        f"blank={counts['not_done']} underscore={counts['handoff_waiting_master']} accepted={counts['master_accepted']}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--bootstrap", action="store_true", help="create initial Blueprints and Gantts")
    action.add_argument("--render", action="store_true", help="regenerate Gantts without editing Blueprints")
    action.add_argument("--check", action="store_true", help="validate Blueprints and byte-check Gantts")
    action.add_argument(
        "--migrate-one-object-v2",
        action="store_true",
        help="atomically replace the reviewed v1 phase authorities with all-blank one-object v2 TARGET authorities",
    )
    action.add_argument(
        "--migrate-program-isolation-v3",
        action="store_true",
        help="atomically replace the v2 shared-capacity execution spec with independent program-local tmux-only specs",
    )
    action.add_argument(
        "--migrate-concurrency-prompt-v4",
        action="store_true",
        help="preserve checklist progress while replacing Blueprint concurrency defaults with mandatory prompt contracts",
    )
    action.add_argument(
        "--migrate-theorem-prompt-authority",
        action="store_true",
        help="CAS-refresh the theorem prompt and operator authority from an explicit vector JSON",
    )
    action.add_argument(
        "--migrate-theorem-lifecycle-v5",
        action="store_true",
        help="atomically strengthen theorem goal/generation/work lifecycle and checkpoint semantics while preserving live claim baselines",
    )
    action.add_argument(
        "--migrate-conjecture-prompt-policy-v6",
        action="store_true",
        help="atomically install the Stage5 conjecture proof-search prompt contract and invalidate weaker TARGET handoffs",
    )
    action.add_argument(
        "--accept-boot-handoff",
        action="store_true",
        help="validate sealed BOOT artifacts and atomically advance only BOOT blank to underscore",
    )
    action.add_argument(
        "--accept-boot-review",
        action="store_true",
        help="validate independent BOOT review and atomically advance only BOOT underscore to x",
    )
    parser.add_argument("--kind", choices=("all", "theorem", "conjecture"), default="all")
    parser.add_argument(
        "--confirm-concurrency-json",
        type=Path,
        help="closed JSON object containing the explicitly confirmed theorem vector",
    )
    parser.add_argument(
        "--authorize-worker-launch",
        action="store_true",
        help="explicitly authorize theorem worker launch in the new authority",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace only a wholly blank pre-runtime Blueprint; never overwrites progress",
    )
    args = parser.parse_args()
    try:
        validate_canonical_root()
        validate_marker_constants()
        if args.force and not args.bootstrap:
            raise BlueprintError("--force is valid only with --bootstrap")
        programs = select_programs(args.kind)
        if args.migrate_one_object_v2 and args.kind != "all":
            raise BlueprintError("one-object v2 migration requires --kind all")
        if args.migrate_program_isolation_v3 and args.kind != "all":
            raise BlueprintError("program-isolation v3 migration requires --kind all")
        if args.migrate_concurrency_prompt_v4 and args.kind != "all":
            raise BlueprintError("concurrency-prompt v4 migration requires --kind all")
        if args.migrate_theorem_prompt_authority and args.kind != "theorem":
            raise BlueprintError("theorem prompt authority migration requires --kind theorem")
        if args.migrate_theorem_lifecycle_v5 and args.kind != "theorem":
            raise BlueprintError("theorem lifecycle v5 migration requires --kind theorem")
        if args.migrate_conjecture_prompt_policy_v6 and args.kind != "conjecture":
            raise BlueprintError("conjecture prompt policy v6 migration requires --kind conjecture")
        if (args.accept_boot_handoff or args.accept_boot_review) and len(programs) != 1:
            raise BlueprintError("BOOT acceptance requires --kind theorem or --kind conjecture")
        main_task_sets = [(program, expected_tasks(program)) for program in programs]
        validate_cross_program_ownership(main_task_sets)
        if args.bootstrap:
            bootstrap_programs(programs, args.force)
        elif args.migrate_one_object_v2:
            migrate_one_object_one_goal_blueprints(programs)
        elif args.migrate_program_isolation_v3:
            migrate_program_isolation_v3(programs)
        elif args.migrate_concurrency_prompt_v4:
            migrate_concurrency_prompt_v4(programs)
        elif args.migrate_theorem_prompt_authority:
            if args.confirm_concurrency_json is None:
                raise BlueprintError("--confirm-concurrency-json is required")
            confirmed = strict_json_loads(
                args.confirm_concurrency_json.read_bytes(),
                "confirmed theorem concurrency object",
            )
            migrate_theorem_execution_prompt(
                confirm_concurrency=confirmed,
                authorize_worker_launch=args.authorize_worker_launch,
            )
        elif args.migrate_theorem_lifecycle_v5:
            migrate_theorem_lifecycle_v5()
        elif args.migrate_conjecture_prompt_policy_v6:
            migrate_conjecture_prompt_policy_v6()
        elif args.render:
            render_projections(programs)
        elif args.accept_boot_handoff:
            accept_boot(programs[0], review=False)
        elif args.accept_boot_review:
            accept_boot(programs[0], review=True)
        else:
            with manager_mutation_lock():
                pending = list(DOCS.glob(f"{BOOTSTRAP_TRANSACTION_PREFIX}*"))
                if pending:
                    raise BlueprintError(
                        f"check refuses an incomplete output transaction: {pending[0]}"
                    )
                for program in programs:
                    check(program)
    except (BlueprintError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=__import__("sys").stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
