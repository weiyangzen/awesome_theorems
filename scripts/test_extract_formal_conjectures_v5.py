#!/usr/bin/env python3
"""Tests for the independent formal-conjectures Stage5 source extractor."""

from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
EXTRACTOR_PATH = ROOT / "Docs" / "tools" / "extract_formal_conjectures_v5.py"
PINNED_TARBALL = (
    ROOT
    / "Docs"
    / "catalog"
    / "v5"
    / "sources"
    / "formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz"
)

SPEC = importlib.util.spec_from_file_location(
    "extract_formal_conjectures_v5", EXTRACTOR_PATH
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load extractor at {EXTRACTOR_PATH}")
extractor = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = extractor
SPEC.loader.exec_module(extractor)


LICENSE = b"Apache License\nVersion 2.0, January 2004\n"
README = b"All other materials: Creative Commons Attribution 4.0 International License.\n"


SAMPLE = """import Zeta.Module
import Alpha.Module

namespace Outer
section Work
namespace Inner

/--
An open problem with a multiline docstring.
-/
@[category
  research open,
  AMS 5
    11]
theorem first (n : Nat) :
    let k := n
    answer(sorry) ↔ k = k := by
  sorry

/-- A named condition. -/
@[category textbook, AMS 3]
theorem assumptionA : True := by
  trivial

/-- A conditionally formalized solved result. -/
@[AMS 14]
@[category research solved,
  conditional formal_proof using lean4 at "https://example.test/proof" assuming assumptionA]
protected theorem second : True := by
  trivial

/-- A private textbook lemma whose string literal belongs to its statement. -/
@[category textbook, AMS 3]
private lemma third : "alpha" = "alpha" := by
  rfl

/-- This API declaration is outside the selected inventory. -/
@[category API, AMS 3]
lemma helper : True := by
  trivial

end Inner
end Work
end Outer
"""


def make_source_tree(base: Path, files: dict[str, str]) -> Path:
    root = base / f"formal-conjectures-{extractor.PINNED_COMMIT}"
    (root / "FormalConjectures").mkdir(parents=True)
    (root / "LICENSE").write_bytes(LICENSE)
    (root / "README.md").write_bytes(README)
    for relative, content in files.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return root


def make_tarball(source_root: Path, target: Path, *, prefix: str | None = None) -> Path:
    archive_prefix = prefix or source_root.name
    with tarfile.open(target, "w:gz", format=tarfile.PAX_FORMAT) as archive:
        for path in sorted(source_root.rglob("*")):
            if not path.is_file():
                continue
            data = path.read_bytes()
            relative = path.relative_to(source_root).as_posix()
            info = tarfile.TarInfo(f"{archive_prefix}/{relative}")
            info.size = len(data)
            info.mtime = 0
            info.mode = 0o644
            archive.addfile(info, io.BytesIO(data))
    return target


class ExtractFormalConjecturesV5Tests(unittest.TestCase):
    maxDiff = None

    def extract_tree(self, files: dict[str, str]) -> tuple[object, list[dict]]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = make_source_tree(Path(temporary.name), files)
        snapshot = extractor.load_snapshot(root)
        return snapshot, extractor.extract_snapshot(snapshot)

    def test_multiline_metadata_signature_namespace_and_comparison_fields(self) -> None:
        snapshot, records = self.extract_tree(
            {"FormalConjectures/Sample/Problem.lean": SAMPLE}
        )
        self.assertEqual(len(records), 4)
        by_name = {row["qualified_name"]: row for row in records}
        first = by_name["Outer.Inner.first"]
        self.assertEqual(first["theorem"], "Outer.Inner.first")
        self.assertEqual(first["category"], "research open")
        self.assertEqual(first["ams"], ["05", "11"])
        self.assertEqual(first["subjects"], ["5", "11"])
        self.assertEqual(first["declaration_kind"], "theorem")
        self.assertIn("multiline docstring", first["docstring"])
        self.assertTrue(first["docstring_raw"].startswith("/--"))
        self.assertIn("let k := n", first["declaration_statement"])
        self.assertNotIn(":= by", first["declaration_statement"])
        self.assertEqual(first["answerKinds"], ["Prop"])
        self.assertFalse(first["hasSorryFreeProof"])
        self.assertEqual(
            first["module_imports"], ["Alpha.Module", "Zeta.Module"]
        )
        self.assertEqual(first["source_commit"], extractor.PINNED_COMMIT)
        self.assertEqual(first["license"]["code_spdx"], "Apache-2.0")
        self.assertEqual(
            first["source_block_sha256"],
            extractor.sha256_bytes(first["source_block"].encode("utf-8")),
        )
        source_file = snapshot.source_files[0].data
        self.assertEqual(
            source_file[
                first["source_block_byte_start"]:
                first["source_block_byte_end_exclusive"]
            ],
            first["source_block"].encode("utf-8"),
        )

        second = by_name["Outer.Inner.second"]
        self.assertEqual(second["declaration_modifiers"], ["protected"])
        self.assertEqual(second["formalProofKind"], "lean4")
        self.assertEqual(second["formalProofLink"], "https://example.test/proof")
        self.assertEqual(second["proofConditions"], ["Outer.Inner.assumptionA"])
        self.assertTrue(second["hasSorryFreeProof"])
        self.assertTrue(second["formal_proofs"][0]["conditional"])

        third = by_name["Outer.Inner.third"]
        self.assertEqual(third["declaration_modifiers"], ["private"])
        self.assertIn('"alpha" = "alpha"', third["declaration_statement"])
        self.assertEqual(snapshot.commit, extractor.PINNED_COMMIT)

    def test_directory_and_tarball_produce_identical_records(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = make_source_tree(
                base, {"FormalConjectures/Sample/Problem.lean": SAMPLE}
            )
            tarball = make_tarball(root, base / "source.tar.gz")
            directory_snapshot = extractor.load_snapshot(root)
            tar_snapshot = extractor.load_snapshot(tarball)
            from_directory = extractor.extract_snapshot(directory_snapshot)
            from_tar = extractor.extract_snapshot(tar_snapshot)
            directory_without_transport = [
                {key: value for key, value in row.items() if key != "archive_member"}
                for row in from_directory
            ]
            tar_without_transport = [
                {key: value for key, value in row.items() if key != "archive_member"}
                for row in from_tar
            ]
            self.assertEqual(directory_without_transport, tar_without_transport)
            self.assertTrue(
                all(
                    row["archive_member"].startswith(root.name + "/FormalConjectures/")
                    for row in from_tar
                )
            )
            self.assertEqual(
                extractor.canonical_jsonl(directory_without_transport),
                extractor.canonical_jsonl(tar_without_transport),
            )

    def test_summary_reports_statement_duplicates_without_dropping_rows(self) -> None:
        text = """namespace Duplicate
/-- First spelling. -/
@[category textbook, AMS 3]
theorem first : True := by trivial
/-- Second spelling. -/
@[category textbook, AMS 3]
lemma second : True := by trivial
end Duplicate
"""
        snapshot, records = self.extract_tree(
            {"FormalConjectures/Duplicates.lean": text}
        )
        summary = extractor.extraction_summary(snapshot, records)
        self.assertEqual(summary["candidate_declarations"], 2)
        self.assertEqual(summary["unique_qualified_names"], 2)
        self.assertEqual(summary["unique_statement_hashes"], 1)
        self.assertEqual(summary["duplicate_statement_hash_groups"], 1)
        self.assertEqual(summary["duplicate_statement_declarations"], 2)

    def test_statement_hash_preserves_string_literals(self) -> None:
        text = """namespace Strings
/-- Alpha. -/
@[category textbook, AMS 3]
theorem alpha : "alpha" = "alpha" := by rfl
/-- Beta. -/
@[category textbook, AMS 3]
theorem beta : "beta" = "beta" := by rfl
end Strings
"""
        _snapshot, records = self.extract_tree(
            {"FormalConjectures/Strings.lean": text}
        )
        self.assertEqual(len({row["statement_sha256"] for row in records}), 2)

    def test_top_level_letI_assignments_do_not_truncate_signatures(self) -> None:
        text = """namespace LetIRegression
/-- The `k = 2` variant. -/
@[category research open, AMS 11]
theorem erdos_727_k_2 :
    letI k := 2
    answer(sorry) ↔ Set.Infinite {n : Nat | n + k = n + 2} := by
  sorry
/-- The `k = 1` variant. -/
@[category research solved, AMS 11]
theorem erdos_727_k_1 :
    letI k := 1
    answer(True) ↔ Set.Infinite {n : Nat | n + k = n + 1} := by
  sorry
/-- The square variant. -/
@[category research solved, AMS 12]
theorem erdos_477_square :
    letI f := fun n : Nat => n ^ 2
    ∀ n, f n = n ^ 2 := by
  sorry
/-- The cube variant. -/
@[category research open, AMS 12]
theorem erdos_477_cube :
    letI f := fun n : Nat => n ^ 3
    ∀ n, f n = n ^ 3 := by
  sorry
/-- A proof-valued local instance with nested tactic assignments. -/
@[category research solved, AMS 60]
theorem tactic_letI (p : Nat) :
    letI hp : p ≤ p := by
      have h : p ≤ p := by omega
      exact h
    p = p := by
  rfl
end LetIRegression
"""
        _snapshot, records = self.extract_tree(
            {"FormalConjectures/LetIRegression.lean": text}
        )
        by_name = {record["local_name"]: record for record in records}
        expected_fragments = {
            "erdos_727_k_2": ("answer(sorry) ↔", "Set.Infinite"),
            "erdos_727_k_1": ("answer(True) ↔", "Set.Infinite"),
            "erdos_477_square": ("∀ n", "f n = n ^ 2"),
            "erdos_477_cube": ("∀ n", "f n = n ^ 3"),
            "tactic_letI": ("have h : p ≤ p := by omega", "p = p"),
        }
        self.assertEqual(set(by_name), set(expected_fragments))
        for name, fragments in expected_fragments.items():
            statement = by_name[name]["statement"]
            self.assertIn("letI", statement)
            for fragment in fragments:
                self.assertIn(fragment, statement)
            self.assertFalse(statement.rstrip().endswith(":= by"))

    def assert_rejected(self, source_text: str, fragment: str) -> None:
        with self.assertRaisesRegex(extractor.ExtractionError, fragment):
            self.extract_tree({"FormalConjectures/Bad.lean": source_text})

    def test_empty_docstring_is_rejected(self) -> None:
        self.assert_rejected(
            "/--   -/\n@[category research open, AMS 11]\n"
            "theorem bad : True := by sorry\n",
            "empty docstring",
        )

    def test_missing_ams_is_rejected(self) -> None:
        self.assert_rejected(
            "/-- Has prose. -/\n@[category research open]\n"
            "theorem bad : True := by sorry\n",
            "no AMS classification",
        )

    def test_incomplete_declaration_is_rejected(self) -> None:
        self.assert_rejected(
            "/-- Has prose. -/\n@[category research open, AMS 11]\n"
            "theorem bad : True\n",
            "no complete top-level body separator",
        )

    def test_duplicate_qualified_name_is_rejected(self) -> None:
        declaration = (
            "namespace Same\n/-- Has prose. -/\n@[category textbook, AMS 3]\n"
            "theorem name : True := by trivial\nend Same\n"
        )
        with self.assertRaisesRegex(extractor.ExtractionError, "duplicate qualified"):
            self.extract_tree(
                {
                    "FormalConjectures/One.lean": declaration,
                    "FormalConjectures/Two.lean": declaration,
                }
            )

    def test_tarball_wrong_commit_root_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = make_source_tree(
                base, {"FormalConjectures/Sample/Problem.lean": SAMPLE}
            )
            tarball = make_tarball(root, base / "wrong.tar.gz", prefix="wrong-root")
            with self.assertRaisesRegex(extractor.ExtractionError, "pinned commit"):
                extractor.load_snapshot(tarball)

    def test_cli_summary_only_is_canonical_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = make_source_tree(
                base, {"FormalConjectures/Sample/Problem.lean": SAMPLE}
            )
            tarball = make_tarball(root, base / "source.tar.gz")
            result = subprocess.run(
                [sys.executable, str(EXTRACTOR_PATH), str(tarball), "--summary-only"],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(result.stdout)
            self.assertEqual(summary["candidate_declarations"], 4)
            self.assertEqual(result.stdout, extractor.canonical_json(summary) + "\n")

    @unittest.skipUnless(PINNED_TARBALL.is_file(), "pinned vendor tarball is unavailable")
    def test_pinned_snapshot_regression_counts(self) -> None:
        snapshot = extractor.load_snapshot(PINNED_TARBALL)
        records = extractor.extract_snapshot(snapshot)
        summary = extractor.extraction_summary(snapshot, records)
        self.assertEqual(summary["source_files_scanned"], 963)
        self.assertEqual(summary["source_files_with_records"], 948)
        self.assertEqual(summary["candidate_declarations"], 2778)
        self.assertEqual(summary["unique_qualified_names"], 2778)
        self.assertEqual(summary["unique_statement_hashes"], 2772)
        self.assertEqual(summary["duplicate_statement_hash_groups"], 3)
        self.assertEqual(summary["duplicate_statement_declarations"], 9)
        self.assertEqual(
            summary["category_counts"],
            {"research open": 1201, "research solved": 1419, "textbook": 158},
        )

        by_name = {record["qualified_name"]: record for record in records}
        exact_regressions = {
            "Erdos727.erdos_727.variants.k_1": ("letI k := 1", "answer(True) ↔"),
            "Erdos727.erdos_727.variants.k_2": ("letI k := 2", "answer(sorry) ↔"),
            "Erdos477.erdos_477.variants.S_sq": ("letI f := X ^ 2", "∀ A : Set ℤ"),
            "Erdos477.erdos_477.variants.X_pow_three": (
                "letI f := X ^ 3",
                "∀ A : Set ℤ",
            ),
        }
        for name, fragments in exact_regressions.items():
            statement = by_name[name]["statement"]
            for fragment in fragments:
                self.assertIn(fragment, statement)
            self.assertNotIn(":= by", statement)

        conjecture6_3 = by_name[
            "Arxiv.«0911.2077».arxiv.id0911_2077.conjecture6_3"
        ]["statement"]
        self.assertIn("PMF.binomial", conjecture6_3)
        self.assertTrue(conjecture6_3.rstrip().endswith(").toReal"))
        self.assertNotIn(").toReal := by", conjecture6_3)
        self.assertNotIn("\n  sorry", conjecture6_3)


if __name__ == "__main__":
    unittest.main()
