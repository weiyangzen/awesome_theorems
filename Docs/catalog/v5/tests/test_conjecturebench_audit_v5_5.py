#!/usr/bin/env python3
"""Black-box regression tests for the frozen ConjectureBench v5.5 audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[4]
TOOLS = REPO / "Docs/catalog/v5/tools"
CURATION_REL = Path("Docs/catalog/v5/curation/conjecturebench_v5_5")
CURATION = REPO / CURATION_REL
BUILDER = TOOLS / "build_conjecturebench_audit_v5_5.py"
CHECKER = TOOLS / "check_conjecturebench_audit_v5_5.py"

GENERATED = {
    "residual-review-190.jsonl": "022191ca07acac80873b0418af27b2f3d9e33374ea397bc07f5c8d61f25db585",
    "residual-review-validation.json": "867a21e7113f1ff5123b0646f041107fede23f876c00b7b986511bf13e4a40b9",
    "strict-review-ledger-302.jsonl": "4d13d77513ee7064fbe7bfa0cbd996cb491363afa17297a2a185cb1927407600",
    "final-audit-summary.json": "318e323f87dcf07450074a83492801a54fd1a33b2597004c4737722e2c6bec66",
}

SOURCE_FILES = [
    "Docs/catalog/v5/sources/conjecturebench-357bcb1a-source.tar.gz",
    "Docs/catalog/v5/sources/conjecturebench-357bcb1a-source-manifest.json",
    "Docs/catalog/v5/sources/conjecturebench-357bcb1a-curated-302.jsonl",
    "Docs/catalog/v5/sources/openconjecture-fa03d85-cc-by-real-conf090.jsonl",
    "Docs/catalog/v5/sources/oeis-conjectures-4c866362-all-conjectur-v2.jsonl",
]

RELEASE_FILES = [
    "Docs/catalog/v5/releases/5.4/Release_Manifest.json",
    "Docs/catalog/v5/releases/5.4/Claim_Catalog.json",
    "Docs/catalog/v5/releases/5.4/Strict_Conjecture_Ledger.json",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


class ConjectureBenchAuditTests(unittest.TestCase):
    maxDiff = None

    def run_tool(self, tool: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(tool), *args],
            cwd=REPO,
            text=True,
            capture_output=True,
            check=False,
        )

    def linked_workspace(self, root: Path) -> None:
        for source in CURATION.iterdir():
            if source.is_file():
                destination = root / source.relative_to(REPO)
                destination.parent.mkdir(parents=True, exist_ok=True)
                os.symlink(source, destination)
        for relative in SOURCE_FILES + RELEASE_FILES:
            source = REPO / relative
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(source, destination)

    def replace_link_with_copy(self, root: Path, relative: str) -> Path:
        destination = root / relative
        source = destination.resolve()
        destination.unlink()
        shutil.copyfile(source, destination)
        return destination

    def test_checker_replays_repository_audit(self) -> None:
        result = self.run_tool(CHECKER)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"overall_pass": true', result.stdout)
        summary = json.loads((CURATION / "final-audit-summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["outcome"]["accepted"], 0)

    def test_builder_is_byte_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "out"
            result = self.run_tool(BUILDER, "--write", "--output-dir", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            for name, expected in GENERATED.items():
                self.assertEqual(digest(output / name), expected, name)
                self.assertEqual((output / name).read_bytes(), (CURATION / name).read_bytes(), name)

    def test_ledger_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            self.linked_workspace(workspace)
            ledger = self.replace_link_with_copy(workspace, str(CURATION_REL / "strict-review-ledger-302.jsonl"))
            rows = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
            rows[0]["decision"] = "accept"
            ledger.write_bytes(b"".join(canonical(row) + b"\n" for row in rows))
            result = self.run_tool(CHECKER, "--workspace", str(workspace))
            self.assertNotEqual(result.returncode, 0)

    def test_protected_release_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            self.linked_workspace(workspace)
            manifest = self.replace_link_with_copy(workspace, RELEASE_FILES[0])
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["release"] = "5.4-mutated"
            manifest.write_bytes(canonical(payload) + b"\n")
            result = self.run_tool(CHECKER, "--workspace", str(workspace))
            self.assertNotEqual(result.returncode, 0)

    def test_curated_source_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            self.linked_workspace(workspace)
            relative = "Docs/catalog/v5/sources/conjecturebench-357bcb1a-curated-302.jsonl"
            source = self.replace_link_with_copy(workspace, relative)
            rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()]
            rows[0]["exact_statement"] = "mutated statement"
            source.write_bytes(b"".join(canonical(row) + b"\n" for row in rows))
            result = self.run_tool(CHECKER, "--workspace", str(workspace))
            self.assertNotEqual(result.returncode, 0)

    def test_official_artifacts_have_no_ephemeral_absolute_paths(self) -> None:
        names = [
            "review-residual-000-094.jsonl",
            "review-residual-095-189.jsonl",
            *GENERATED,
            "final-ledger-validation.json",
        ]
        for name in names:
            text = (CURATION / name).read_text(encoding="utf-8")
            self.assertNotIn("/tmp/", text, name)
            self.assertNotIn("/home/sansha/", text, name)


if __name__ == "__main__":
    unittest.main()
