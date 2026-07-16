#!/usr/bin/env python3
"""Focused crash-recovery tests for the Stage1 integration WAL.

These tests intentionally live outside the main scheduler test module so WAL
hardening and lane-allocation work can proceed independently.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


MODULE_PATH = Path(__file__).with_name("stage1_execution_cron.py")
SPEC = importlib.util.spec_from_file_location("stage1_execution_recovery_under_test", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
cron = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = cron
SPEC.loader.exec_module(cron)


REAL_ROOT = MODULE_PATH.parents[1]
CHILD_MODE = "--stage1-recovery-child"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def configure_child_scheduler(root: Path) -> None:
    """Point every mutable scheduler surface at one disposable repository."""

    docs = root / "Docs"
    runtime = root / ".cron" / "stage1-v2-app-server"
    cron.ROOT = root
    cron.DOCS = docs
    cron.BLUEPRINT = docs / "Stage1_Blueprint_v2.md"
    cron.ASSURANCE_BLUEPRINT = docs / "Stage1_Blueprint_rev-5.6.md"
    cron.TARGETS = docs / "Stage1_Targets_rev-5.6.json"
    cron.DAG = docs / "Stage1_Execution_DAG_rev-5.6.json"
    cron.THEOREM_DAG_V2 = docs / "Stage1_Theorem_DAG_v2.json"
    cron.PHASE_ACCEPTANCE_CONTRACTS = docs / "Stage1_Phase_Acceptance_Contracts.json"
    cron.LEGACY_RUNTIME = root / ".cron" / "stage1-rev56"
    cron.RUNTIME = runtime
    # Recovery and checkpoint children must never observe or alter the real
    # operator pause marker. Their control paths are absent fixture paths.
    control = root / ".test-control"
    cron.PAUSE_FILE = control / "PAUSED"
    cron.LEGACY_PAUSE_FILE = control / "LEGACY_PAUSED"
    cron.theorem_dag_v2.cache_clear()


def kill_self() -> None:
    os.kill(os.getpid(), signal.SIGKILL)
    raise AssertionError("SIGKILL unexpectedly returned")


def publication_crash_child(root: Path, kill_after: str) -> None:
    """Perform the real durable publication prefix, then die without cleanup."""

    configure_child_scheduler(root)
    runtime = cron.RUNTIME
    todo = cron.DOCS / "todos_20260716.md"
    pending = runtime / "pending_checkpoint.json"
    queue = runtime / "integration_queue.json"
    transaction = cron.FileTransaction(runtime / "integration_wal.json")

    # Production integration snapshots all shared state surfaces before the
    # first mutation. Preserve that ordering so each kill leaves a complete WAL.
    for path in (
        cron.BLUEPRINT,
        cron.DAG,
        cron.THEOREM_DAG_V2,
        runtime / "claims.json",
        queue,
        pending,
        todo,
    ):
        transaction.snapshot(path)

    receipt_bytes = b'{"schema_version":"stage1-master-phase-acceptance/1.0"}\n'
    receipt_digest = hashlib.sha256(receipt_bytes).hexdigest()
    receipt = (
        root
        / "Stage1_Instances"
        / "THM-M-0001"
        / "master-acceptance"
        / "intake"
        / f"{receipt_digest}.json"
    )
    transaction.snapshot(receipt)
    transaction.ensure_parent(receipt)
    cron.durable_write_bytes(receipt, receipt_bytes)
    if kill_after == "receipt":
        kill_self()

    cron.atomic_write(cron.BLUEPRINT, "interrupted authoritative blueprint\n")
    if kill_after == "ssot":
        kill_self()

    cron.atomic_write(cron.DAG, '{"interrupted":"execution-dag"}\n')
    if kill_after == "execution_dag":
        kill_self()

    cron.atomic_write(cron.THEOREM_DAG_V2, '{"interrupted":"theorem-dag"}\n')
    if kill_after == "theorem_dag":
        kill_self()

    cron.save_claims([{"item_id": "S56-M-0001-INTAKE", "status": "master_accepted"}])
    if kill_after == "claims":
        kill_self()

    cron.atomic_write(queue, '{"master_accepted":["S56-M-0001-INTAKE"]}\n')
    cron.atomic_write(todo, "interrupted daily projection\n")
    cron.atomic_write(
        pending,
        json.dumps(
            {
                "schema_version": "stage1-pending-checkpoint/1.0",
                "base_revision": cron.run(["git", "rev-parse", "HEAD"]).stdout.strip(),
                "state": "integrated_uncommitted",
                "paths": [
                    {
                        "path": path.relative_to(root).as_posix(),
                        "sha256": sha256(path),
                        "mode": "100644",
                    }
                    for path in (
                        receipt,
                        cron.BLUEPRINT,
                        cron.DAG,
                        cron.THEOREM_DAG_V2,
                    )
                ],
            },
            indent=2,
        )
        + "\n",
    )
    if kill_after == "pending_checkpoint":
        kill_self()
    raise AssertionError(f"unknown publication killpoint: {kill_after}")


def publication_recovery_child(root: Path) -> None:
    configure_child_scheduler(root)
    cron.recover_integration_wal()


def checkpoint_child(root: Path, operation: str) -> None:
    """Crash or resume one real local commit/push checkpoint transaction."""

    configure_child_scheduler(root)
    pending = cron.RUNTIME / "pending_checkpoint.json"
    if operation == "recover":
        if pending.exists():
            cron.checkpoint_integration()
        return

    real_run = cron.run
    real_atomic_write = cron.atomic_write

    def crash_run(command: list[str], **kwargs):
        result = real_run(command, **kwargs)
        if operation == "after_commit" and command[:2] == ["git", "commit"]:
            kill_self()
        if operation == "after_push" and command[:2] == ["git", "push"]:
            kill_self()
        return result

    def crash_atomic_write(path: Path, text: str) -> None:
        real_atomic_write(path, text)
        if operation != "after_committed_manifest" or Path(path) != pending:
            return
        try:
            state = json.loads(text).get("state")
        except json.JSONDecodeError:
            return
        if state == "committed_unpushed":
            kill_self()

    cron.run = crash_run
    cron.atomic_write = crash_atomic_write
    cron.checkpoint_integration()
    raise AssertionError(f"checkpoint killpoint did not fire: {operation}")


def recovery_child_main(arguments: list[str]) -> None:
    if len(arguments) != 3:
        raise SystemExit("recovery child expects ACTION ROOT KILLPOINT")
    action, root_text, killpoint = arguments
    root = Path(root_text).resolve()
    temporary_root = Path(tempfile.gettempdir()).resolve()
    if (
        root == REAL_ROOT.resolve()
        or not root.is_relative_to(temporary_root)
        or not (root / ".stage1-recovery-fixture").is_file()
    ):
        raise SystemExit("refusing recovery child outside a marked temporary repository")
    if action == "publication-crash":
        publication_crash_child(root, killpoint)
    elif action == "publication-recover":
        publication_recovery_child(root)
    elif action == "checkpoint":
        checkpoint_child(root, killpoint)
    else:
        raise SystemExit(f"unknown recovery child action: {action}")


class RealRuntimeIsolationMixin:
    """Prove each subprocess test leaves the operator runtime untouched."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.real_runtime_claims = REAL_ROOT / ".cron" / "stage1-v2-app-server" / "claims.json"
        cls.real_legacy_claims = REAL_ROOT / ".cron" / "stage1-rev56" / "claims.json"
        cls.real_current_pause = REAL_ROOT / ".cron" / "stage1-v2-app-server" / "PAUSED"
        cls.real_pause = REAL_ROOT / ".cron" / "stage1-rev56" / "PAUSED"
        cls.real_runtime_hashes = {
            path: sha256(path) if path.is_file() else None
            for path in (
                cls.real_runtime_claims,
                cls.real_legacy_claims,
                cls.real_current_pause,
                cls.real_pause,
            )
        }

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            for path, before in cls.real_runtime_hashes.items():
                after = sha256(path) if path.is_file() else None
                if after != before:
                    raise AssertionError(f"real Stage1 runtime changed across test class: {path}")
        finally:
            super().tearDownClass()

    def assert_real_runtime_unchanged(self) -> None:
        for path, before in self.real_runtime_hashes.items():
            after = sha256(path) if path.is_file() else None
            self.assertEqual(after, before, f"real Stage1 runtime changed: {path}")

    def tearDown(self) -> None:
        self.assert_real_runtime_unchanged()
        super().tearDown()


class SubprocessCrashTestCase(RealRuntimeIsolationMixin, unittest.TestCase):
    def run_child(
        self,
        root: Path,
        action: str,
        killpoint: str,
        *,
        expect_sigkill: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(MODULE_PATH.with_name(Path(__file__).name)), CHILD_MODE, action, str(root), killpoint],
            cwd=REAL_ROOT,
            text=True,
            capture_output=True,
            timeout=30,
        )
        if expect_sigkill:
            self.assertEqual(
                result.returncode,
                -signal.SIGKILL,
                f"child did not die at {killpoint}: stdout={result.stdout!r} stderr={result.stderr!r}",
            )
        elif result.returncode:
            self.fail(
                f"child failed ({action}/{killpoint}): "
                f"stdout={result.stdout!r} stderr={result.stderr!r}"
            )
        return result


class IntegrationWalRecoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        self.root.mkdir()
        (self.root / ".stage1-recovery-fixture").write_text("temporary test repo\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "recovery@example.invalid"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Recovery Tests"],
            cwd=self.root,
            check=True,
        )
        self.docs = self.root / "Docs"
        self.runtime = self.root / ".cron" / "stage1-v2-app-server"
        self.docs.mkdir()
        self.runtime.mkdir(parents=True)
        self.blueprint = self.docs / "Stage1_Blueprint_v2.md"
        self.blueprint.write_text("old blueprint\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=self.root, check=True)
        self.head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=self.root, text=True
        ).strip()
        self.wal = self.runtime / "integration_wal.json"

    def patch_scheduler(self):
        return (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "DOCS", self.docs),
            mock.patch.object(cron, "BLUEPRINT", self.blueprint),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(cron, "theorem_dag_v2", mock.Mock(cache_clear=mock.Mock())),
        )

    def write_wal(self, rows: list[dict[str, object]]) -> None:
        self.wal.write_text(
            json.dumps(
                {
                    "schema_version": "stage1-integration-wal/1.0",
                    "state": "prepared",
                    "base_revision": self.head,
                    "files": rows,
                    "created_dirs": [],
                }
            )
            + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def file_row(relative: str, payload: bytes) -> dict[str, object]:
        return {
            "path": relative,
            "kind": "file",
            "mode": 0o644,
            "payload_hex": payload.hex(),
        }

    def test_late_malformed_row_is_rejected_before_any_recovery_mutation(self) -> None:
        """All rows must validate before recovery touches the first destination."""

        old = self.blueprint.read_bytes()
        self.blueprint.write_text("interrupted blueprint\n", encoding="utf-8")
        self.write_wal(
            [
                {
                    "path": "Docs/Stage1_Execution_DAG_rev-5.6.json",
                    "kind": "file",
                    "mode": 0o644,
                    "payload_hex": "not-hex",
                },
                # Recovery walks in reverse.  A validator that validates only
                # as it mutates will restore this valid row before discovering
                # the earlier malformed row.
                self.file_row("Docs/Stage1_Blueprint_v2.md", old),
            ]
        )
        patches = self.patch_scheduler()
        with patches[0], patches[1], patches[2], patches[3], patches[4]:
            with self.assertRaisesRegex(SystemExit, "payload is malformed"):
                cron.recover_integration_wal()
        self.assertEqual(self.blueprint.read_text(), "interrupted blueprint\n")
        self.assertTrue(self.wal.is_file())

    def test_recovery_interruption_can_be_retried_to_the_same_fixed_point(self) -> None:
        first = self.blueprint
        second = self.docs / "Stage1_Execution_DAG_rev-5.6.json"
        second.write_text("old dag\n", encoding="utf-8")
        old_first = first.read_bytes()
        old_second = second.read_bytes()
        first.write_text("interrupted blueprint\n", encoding="utf-8")
        second.write_text("interrupted dag\n", encoding="utf-8")
        self.write_wal(
            [
                self.file_row("Docs/Stage1_Blueprint_v2.md", old_first),
                self.file_row("Docs/Stage1_Execution_DAG_rev-5.6.json", old_second),
            ]
        )
        real_write = cron.durable_write_bytes
        writes = 0

        def fail_after_one_write(path: Path, data: bytes) -> None:
            nonlocal writes
            real_write(path, data)
            writes += 1
            if writes == 1:
                raise OSError("injected recovery interruption")

        patches = self.patch_scheduler()
        with patches[0], patches[1], patches[2], patches[3], patches[4], mock.patch.object(
            cron, "durable_write_bytes", side_effect=fail_after_one_write
        ):
            with self.assertRaises(OSError):
                cron.recover_integration_wal()
        self.assertTrue(self.wal.is_file())

        patches = self.patch_scheduler()
        with patches[0], patches[1], patches[2], patches[3], patches[4]:
            cron.recover_integration_wal()
            cron.recover_integration_wal()
        self.assertEqual(first.read_bytes(), old_first)
        self.assertEqual(second.read_bytes(), old_second)
        self.assertFalse(self.wal.exists())

    def test_replay_and_semantic_acceptance_files_are_recoverable(self) -> None:
        claim_id = "20260716T120000Z-abcdef123456"
        replay_relative = (
            f"{self.runtime.relative_to(self.root).as_posix()}/replay-results/{claim_id}.json"
        )
        semantic_relative = (
            f"{self.runtime.relative_to(self.root).as_posix()}/semantic-decisions/{claim_id}.json"
        )
        replay = self.root / replay_relative
        semantic = self.root / semantic_relative
        replay.parent.mkdir(parents=True)
        semantic.parent.mkdir(parents=True)
        replay.write_text('{"interrupted":true}\n', encoding="utf-8")
        semantic.write_text('{"interrupted":true}\n', encoding="utf-8")
        self.write_wal(
            [
                {"path": replay_relative, "kind": "missing", "mode": None},
                {"path": semantic_relative, "kind": "missing", "mode": None},
            ]
        )
        patches = self.patch_scheduler()
        with patches[0], patches[1], patches[2], patches[3], patches[4]:
            cron.recover_integration_wal()
        self.assertFalse(replay.exists())
        self.assertFalse(semantic.exists())
        self.assertFalse(self.wal.exists())

    def test_durable_pending_boundary_survives_after_wal_commit(self) -> None:
        """Once rollback WAL is removed, an exact pending checkpoint must remain."""

        pending = self.runtime / "pending_checkpoint.json"
        transaction = cron.FileTransaction(self.wal)
        patches = self.patch_scheduler()
        with patches[0], patches[1], patches[2], patches[3], patches[4]:
            transaction.snapshot(pending)
            cron.atomic_write(
                pending,
                json.dumps(
                    {
                        "schema_version": "stage1-pending-checkpoint/1.0",
                        "base_revision": self.head,
                        "state": "integrated_uncommitted",
                        "paths": [
                            {
                                "path": "Docs/Stage1_Blueprint_v2.md",
                                "sha256": "0" * 64,
                                "mode": "100644",
                            }
                        ],
                    }
                )
                + "\n",
            )
            transaction.commit()
        self.assertFalse(self.wal.exists())
        self.assertTrue(pending.is_file())
        self.assertEqual(json.loads(pending.read_text())["state"], "integrated_uncommitted")


class SubprocessPublicationRecoveryTests(SubprocessCrashTestCase):
    KILLPOINTS = (
        "receipt",
        "ssot",
        "execution_dag",
        "theorem_dag",
        "claims",
        "pending_checkpoint",
    )

    def make_fixture(self, sandbox: Path) -> tuple[Path, dict[str, bytes | None]]:
        root = sandbox / "repo"
        root.mkdir()
        (root / ".stage1-recovery-fixture").write_text("temporary test repo\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "recovery@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Recovery Tests"], cwd=root, check=True)
        docs = root / "Docs"
        runtime = root / ".cron" / "stage1-v2-app-server"
        docs.mkdir()
        runtime.mkdir(parents=True)
        originals = {
            "Docs/Stage1_Blueprint_v2.md": b"authoritative blueprint before integration\n",
            "Docs/Stage1_Execution_DAG_rev-5.6.json": b'{"state":"execution-before"}\n',
            "Docs/Stage1_Theorem_DAG_v2.json": b'{"state":"theorem-before"}\n',
            ".cron/stage1-v2-app-server/claims.json": b'{"claims":[{"status":"before"}]}\n',
            ".cron/stage1-v2-app-server/integration_queue.json": b'{"queued":["before"]}\n',
            ".cron/stage1-v2-app-server/pending_checkpoint.json": None,
            "Docs/todos_20260716.md": b"daily projection before integration\n",
        }
        for relative, payload in originals.items():
            if payload is None:
                continue
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        subprocess.run(
            [
                "git",
                "add",
                ".stage1-recovery-fixture",
                "Docs/Stage1_Blueprint_v2.md",
                "Docs/Stage1_Execution_DAG_rev-5.6.json",
                "Docs/Stage1_Theorem_DAG_v2.json",
                "Docs/todos_20260716.md",
                ".cron/stage1-v2-app-server/claims.json",
                ".cron/stage1-v2-app-server/integration_queue.json",
            ],
            cwd=root,
            check=True,
        )
        subprocess.run(["git", "commit", "-qm", "base"], cwd=root, check=True)
        return root, originals

    def assert_fixed_point(self, root: Path, originals: dict[str, bytes | None]) -> None:
        for relative, payload in originals.items():
            path = root / relative
            if payload is None:
                self.assertFalse(path.exists(), relative)
            else:
                self.assertEqual(path.read_bytes(), payload, relative)
        self.assertFalse((root / ".cron" / "stage1-v2-app-server" / "integration_wal.json").exists())
        self.assertFalse((root / "Stage1_Instances").exists())
        self.assertEqual(
            subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True).strip(),
            "",
        )

    def test_real_sigkill_publication_matrix_recovers_exact_fixed_point(self) -> None:
        for killpoint in self.KILLPOINTS:
            with self.subTest(killpoint=killpoint), tempfile.TemporaryDirectory() as directory:
                root, originals = self.make_fixture(Path(directory))
                base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
                self.run_child(root, "publication-crash", killpoint, expect_sigkill=True)
                wal = root / ".cron" / "stage1-v2-app-server" / "integration_wal.json"
                self.assertTrue(wal.is_file())
                self.assertEqual(
                    subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
                    base,
                )
                self.run_child(root, "publication-recover", "recover")
                self.assert_fixed_point(root, originals)
                # A new process must observe the same fixed point when recovery
                # is retried after the journal has already been consumed.
                self.run_child(root, "publication-recover", "recover-again")
                self.assert_fixed_point(root, originals)

    def test_child_refuses_the_real_repository(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(Path(__file__)),
                CHILD_MODE,
                "publication-crash",
                str(REAL_ROOT),
                "claims",
            ],
            cwd=REAL_ROOT,
            text=True,
            capture_output=True,
            timeout=10,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("refusing recovery child", result.stderr)


class SubprocessCheckpointRecoveryTests(SubprocessCrashTestCase):
    KILLPOINTS = ("after_commit", "after_committed_manifest", "after_push")
    RELATIVE = "Stage1_Instances/THM-M-0001/evidence.txt"

    def make_fixture(self, sandbox: Path) -> tuple[Path, Path, str]:
        root = sandbox / "repo"
        remote = sandbox / "origin.git"
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
        subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
        (root / ".stage1-recovery-fixture").write_text("temporary test repo\n", encoding="utf-8")
        subprocess.run(["git", "config", "user.email", "recovery@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Recovery Tests"], cwd=root, check=True)
        target = root / self.RELATIVE
        target.parent.mkdir(parents=True)
        target.write_text("base evidence\n", encoding="utf-8")
        subprocess.run(
            ["git", "add", ".stage1-recovery-fixture", self.RELATIVE],
            cwd=root,
            check=True,
        )
        subprocess.run(["git", "commit", "-qm", "base"], cwd=root, check=True)
        subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=root, check=True)
        subprocess.run(["git", "push", "-qu", "origin", "main"], cwd=root, check=True)
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
        target.write_text("integrated evidence\n", encoding="utf-8")
        runtime = root / ".cron" / "stage1-v2-app-server"
        runtime.mkdir(parents=True)
        pending = {
            "schema_version": "stage1-pending-checkpoint/1.0",
            "base_revision": base,
            "state": "integrated_uncommitted",
            "paths": [
                {"path": self.RELATIVE, "sha256": sha256(target), "mode": "100644"}
            ],
            "created_at": "2026-07-16T00:00:00+00:00",
        }
        (runtime / "pending_checkpoint.json").write_text(json.dumps(pending) + "\n", encoding="utf-8")
        return root, remote, base

    @staticmethod
    def remote_main(remote: Path) -> str:
        return subprocess.check_output(
            ["git", "--git-dir", str(remote), "rev-parse", "refs/heads/main"],
            text=True,
        ).strip()

    def test_real_sigkill_checkpoint_matrix_recovers_commit_and_push(self) -> None:
        for killpoint in self.KILLPOINTS:
            with self.subTest(killpoint=killpoint), tempfile.TemporaryDirectory() as directory:
                root, remote, base = self.make_fixture(Path(directory))
                self.run_child(root, "checkpoint", killpoint, expect_sigkill=True)
                committed = subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=root, text=True
                ).strip()
                self.assertNotEqual(committed, base)
                self.assertEqual(
                    subprocess.check_output(
                        ["git", "diff", "--name-only", base, committed], cwd=root, text=True
                    ).splitlines(),
                    [self.RELATIVE],
                )
                pending_path = root / ".cron" / "stage1-v2-app-server" / "pending_checkpoint.json"
                pending = json.loads(pending_path.read_text(encoding="utf-8"))
                if killpoint == "after_commit":
                    self.assertEqual(pending["state"], "integrated_uncommitted")
                    self.assertEqual(self.remote_main(remote), base)
                elif killpoint == "after_committed_manifest":
                    self.assertEqual(pending["state"], "committed_unpushed")
                    self.assertEqual(pending["commit_revision"], committed)
                    self.assertEqual(self.remote_main(remote), base)
                else:
                    self.assertEqual(pending["state"], "committed_unpushed")
                    self.assertEqual(self.remote_main(remote), committed)

                self.run_child(root, "checkpoint", "recover")
                self.assertFalse(pending_path.exists())
                self.assertEqual(self.remote_main(remote), committed)
                self.assertEqual(
                    subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
                    committed,
                )
                self.assertEqual((root / self.RELATIVE).read_text(encoding="utf-8"), "integrated evidence\n")
                self.assertEqual(
                    subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True).strip(),
                    "",
                )
                self.run_child(root, "checkpoint", "recover")
                self.assertEqual(self.remote_main(remote), committed)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == CHILD_MODE:
        recovery_child_main(sys.argv[2:])
    else:
        unittest.main()
