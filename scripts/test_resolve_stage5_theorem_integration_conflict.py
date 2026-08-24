#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "stage5_theorem_conflict_resolver_test",
    SCRIPTS / "resolve_stage5_theorem_integration_conflict.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("resolver unavailable")
resolver = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(resolver)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


class ConflictResolverTests(unittest.TestCase):
    def fixture(self, root: Path) -> dict[str, Path]:
        ctl = resolver.controller
        runtime = root / ".ops/runtime"
        entry_path = runtime / "integration/A.json"
        queue = runtime / "handoffs/A/base/patch"
        canonical_path = root / "owned/A.txt"
        canonical_path.parent.mkdir(parents=True)
        canonical_path.write_bytes(b"old")
        artifact_path = root / "archive/new.txt"
        artifact_path.parent.mkdir(parents=True)
        artifact_path.write_bytes(b"new")
        manifest = ctl.seal(
            {
                "item_id": "A",
                "claim_id": "A--worker",
                "run_id": "r-new",
                "artifacts": [
                    {
                        "path": "owned/A.txt",
                        "archive_path": "archive/new.txt",
                        "sha256": sha(b"new"),
                        "size_bytes": 3,
                    }
                ],
            }
        )
        write_json(queue / "harvest-manifest.json", manifest)
        entry = ctl.seal(
            {
                "item_id": "A",
                "claim_id": "A--worker",
                "run_id": "r-new",
                "queue": ".ops/runtime/handoffs/A/base/patch",
            }
        )
        write_json(entry_path, entry)
        repair_path = runtime / "repair/A.json.repair.json"
        repair = ctl.seal(
            {
                "item_id": "A",
                "entry_sha256": sha(entry_path.read_bytes()),
                "reason": "canonical destination already exists: owned/A.txt",
            }
        )
        write_json(repair_path, repair)
        generation = root / ".ops/retired/tasks/A--worker/r-old"
        write_json(generation / "claim.json", {"item_id": "A", "run_id": "r-old"})
        old = generation / "work/owned/A.txt"
        old.parent.mkdir(parents=True)
        old.write_bytes(b"old")
        return {
            "runtime": runtime,
            "entry": entry_path,
            "canonical": canonical_path,
            "repair": repair_path,
            "generation": generation,
        }

    def settings(self, paths: dict[str, Path], root: Path):
        ctl = resolver.controller
        return (
            mock.patch.object(ctl, "ROOT", root),
            mock.patch.object(ctl, "RUNTIME", paths["runtime"]),
            mock.patch.object(ctl, "INTEGRATION_QUEUE", paths["runtime"] / "integration"),
            mock.patch.object(
                resolver,
                "SUPERSEDED_ROOT",
                root / "Docs/evidence/stage5_theorems/execution/superseded/canonical-conflicts",
            ),
        )

    def test_historical_provenance_requires_exact_bytes_and_item(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            generation = root / "r-old"
            write_json(generation / "claim.json", {"item_id": "A", "run_id": "r-old"})
            artifact = generation / "work/owned/A.txt"
            artifact.parent.mkdir(parents=True)
            artifact.write_bytes(b"old")
            conflicts = [{"path": "owned/A.txt", "sha256": sha(b"old")}]
            resolver._provenance_map(
                kind="historical_generation",
                source=generation,
                item_id="A",
                conflicts=conflicts,
            )
            artifact.write_bytes(b"drift")
            with self.assertRaisesRegex(Exception, "provenance differs"):
                resolver._provenance_map(
                    kind="historical_generation",
                    source=generation,
                    item_id="A",
                    conflicts=conflicts,
                )
            artifact.write_bytes(b"old")
            write_json(generation / "claim.json", {"item_id": "B", "run_id": "r-old"})
            with self.assertRaisesRegex(Exception, "claim item differs"):
                resolver._provenance_map(
                    kind="historical_generation",
                    source=generation,
                    item_id="A",
                    conflicts=conflicts,
                )

    def test_resolve_archives_before_removal_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = self.fixture(root)
            patches = self.settings(paths, root)
            with patches[0], patches[1], patches[2], patches[3]:
                first = resolver.resolve(
                    entry_path=paths["entry"],
                    provenance_kind="historical_generation",
                    provenance_path=paths["generation"],
                    reason="fixture orphan artifact",
                )
                self.assertFalse(paths["canonical"].exists())
                self.assertFalse(paths["repair"].exists())
                archived = root / first["archived_conflicts"][0]["archive_path"]
                self.assertEqual(archived.read_bytes(), b"old")
                # Simulate a crash after removing the canonical conflict and
                # active repair receipt but before the final completion write.
                completion = root / "Docs/evidence/stage5_theorems/execution/superseded/canonical-conflicts/A" / sha(paths["entry"].read_bytes()) / "completion.json"
                completion.unlink()
                second = resolver.resolve(
                    entry_path=paths["entry"],
                    provenance_kind="historical_generation",
                    provenance_path=paths["generation"],
                    reason="fixture orphan artifact",
                )
                self.assertEqual(first, second)

    def test_canonical_drift_and_symlink_fail_without_removal(self):
        for replacement in (b"drift", None):
            with self.subTest(replacement=replacement):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    paths = self.fixture(root)
                    if replacement is None:
                        paths["canonical"].unlink()
                        paths["canonical"].symlink_to(paths["generation"] / "work/owned/A.txt")
                    else:
                        paths["canonical"].write_bytes(replacement)
                    patches = self.settings(paths, root)
                    with patches[0], patches[1], patches[2], patches[3]:
                        with self.assertRaises(Exception):
                            resolver.resolve(
                                entry_path=paths["entry"],
                                provenance_kind="historical_generation",
                                provenance_path=paths["generation"],
                                reason="fixture",
                            )
                    self.assertTrue(paths["canonical"].exists() or paths["canonical"].is_symlink())
                    self.assertTrue(paths["repair"].is_file())


if __name__ == "__main__":
    unittest.main()
