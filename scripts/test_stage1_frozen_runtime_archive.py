#!/usr/bin/env python3
"""Focused tests for content-addressing a paused Stage1 runtime."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


MODULE = Path(__file__).with_name("stage1_frozen_runtime_archive.py")
SPEC = importlib.util.spec_from_file_location("stage1_frozen_runtime_archive_under_test", MODULE)
assert SPEC is not None and SPEC.loader is not None
archive = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = archive
SPEC.loader.exec_module(archive)


def run(cwd: Path, *argv: str) -> str:
    result = subprocess.run(argv, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode:
        raise AssertionError(result.stderr or result.stdout)
    return result.stdout.strip()


class FrozenArchiveTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        run(self.root, "git", "init", "-b", "main")
        run(self.root, "git", "config", "user.email", "test@example.invalid")
        run(self.root, "git", "config", "user.name", "Stage1 Test")
        (self.root / "Docs").mkdir()
        (self.root / "Docs/Stage1_Blueprint_v2.md").write_text("- [_] frozen\n")
        run(self.root, "git", "add", ".")
        run(self.root, "git", "commit", "-m", "base")
        self.runtime = self.root / ".cron/stage1-v2-app-server"
        (self.runtime / "workers").mkdir(parents=True)
        (self.root / ".cron/stage1-rev56").mkdir(parents=True)
        (self.runtime / "PAUSED").write_text("paused\n")
        (self.root / ".cron/stage1-rev56/PAUSED").write_text("paused\n")

    def clone(self, slot: int) -> Path:
        workspace = self.runtime / "workers" / f"slot{slot}"
        run(self.root, "git", "clone", str(self.root), str(workspace))
        return workspace

    def write_claims(self, claims: list[dict[str, object]]) -> None:
        (self.runtime / "claims.json").write_text(json.dumps({"claims": claims}) + "\n")

    def claim(self, slot: int) -> dict[str, object]:
        return {
            "claim_id": f"20260716T120000Z-{slot:012x}",
            "item_id": f"S56-M-{slot:04d}-INTAKE",
            "theorem_id": f"THM-M-{slot:04d}",
            "slot": slot,
            "status": "live",
            "owned_paths": [f"Stage1_Instances/THM-M-{slot:04d}"],
            "workspace": str(self.runtime / "workers" / f"slot{slot}"),
        }

    def test_archive_is_deterministic_and_captures_binary_and_symlink(self) -> None:
        workspace = self.clone(1)
        owned = workspace / "Stage1_Instances/THM-M-0001"
        owned.mkdir(parents=True)
        (owned / "data.bin").write_bytes(b"\x00\xffpayload")
        (workspace / "Formalizations/Lean").mkdir(parents=True)
        (workspace / "Formalizations/Lean/.lake").symlink_to("/readonly/toolchain")
        (workspace / "outside.txt").write_text("mismatch\n")
        claim = self.claim(1)
        self.write_claims([claim])

        first, deltas = archive.build_archive(self.root, self.runtime)
        second, repeated = archive.build_archive(self.root, self.runtime)
        self.assertEqual(first, second)
        self.assertEqual(deltas, repeated)
        row = deltas[0]
        self.assertEqual(row["workspace_state"], "dirty")
        self.assertEqual(row["claim_metadata_state"], "internally_consistent")
        self.assertEqual(row["out_of_claim_changed_paths"], ["outside.txt"])
        self.assertEqual(row["scheduler_infrastructure_paths"], ["Formalizations/Lean/.lake"])
        entries = {entry["path"]: entry for entry in row["untracked_entries"]}
        self.assertEqual(entries["Formalizations/Lean/.lake"]["kind"], "symlink")
        self.assertEqual(entries["Stage1_Instances/THM-M-0001/data.bin"]["size"], 9)
        unhashed = dict(row)
        digest = unhashed.pop("archive_sha256")
        self.assertEqual(digest, archive.sha256_bytes(archive.canonical_json(unhashed)))

        path = archive.write_archive(self.runtime, first, deltas)
        self.assertTrue(path.is_file())
        self.assertEqual(archive.write_archive(self.runtime, first, deltas), path)
        self.assertEqual(json.loads((self.runtime / "claims.json").read_text())["claims"], [claim])

    def test_missing_workspace_is_bound_without_inventing_evidence(self) -> None:
        self.write_claims([self.claim(2)])
        manifest, deltas = archive.build_archive(self.root, self.runtime)
        self.assertEqual(deltas[0]["workspace_state"], "missing")
        self.assertEqual(deltas[0]["untracked_entries"], [])
        self.assertEqual(manifest["workspace_archives"][0]["archive_sha256"], deltas[0]["archive_sha256"])

    def test_archive_requires_both_pause_markers(self) -> None:
        self.write_claims([])
        (self.runtime / "PAUSED").unlink()
        with self.assertRaisesRegex(archive.ArchiveError, "pause markers"):
            archive.build_archive(self.root, self.runtime)

    def test_noncanonical_claim_workspace_is_rejected(self) -> None:
        claim = self.claim(1)
        claim["workspace"] = str(self.root)
        self.write_claims([claim])
        with self.assertRaisesRegex(archive.ArchiveError, "canonical slot"):
            archive.build_archive(self.root, self.runtime)

    def test_retirement_requires_exact_archive_and_preserves_workspaces(self) -> None:
        workspace = self.clone(1)
        owned = workspace / "Stage1_Instances/THM-M-0001"
        owned.mkdir(parents=True)
        (owned / "evidence.json").write_text('{"theorem_id":"THM-M-0001"}\n')
        claim = self.claim(1)
        self.write_claims([claim])
        manifest, deltas = archive.build_archive(self.root, self.runtime)
        archive.write_archive(self.runtime, manifest, deltas)
        retirement = archive.retire_archived_claims(
            self.root, self.runtime, manifest, deltas
        )
        self.assertTrue(retirement.is_file())
        ledger = json.loads((self.runtime / "claims.json").read_text())
        self.assertEqual(ledger["claims"], [])
        self.assertEqual(
            ledger["retired_archive_manifest_sha256"], manifest["manifest_sha256"]
        )
        self.assertTrue(workspace.is_dir())
        self.assertTrue((self.runtime / "PAUSED").is_file())
        self.assertTrue((self.root / ".cron/stage1-rev56/PAUSED").is_file())

    def test_retirement_refuses_changed_claim_ledger(self) -> None:
        self.write_claims([self.claim(1)])
        manifest, deltas = archive.build_archive(self.root, self.runtime)
        archive.write_archive(self.runtime, manifest, deltas)
        self.write_claims([])
        with self.assertRaisesRegex(archive.ArchiveError, "changed"):
            archive.retire_archived_claims(self.root, self.runtime, manifest, deltas)


if __name__ == "__main__":
    unittest.main()
