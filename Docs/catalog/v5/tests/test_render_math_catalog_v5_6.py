"""Mutation and rendering tests for the Stage5 5.6 readable catalog."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys
import unittest

from Docs.catalog.v5.tools import render_math_catalog_v5_6 as renderer


class RenderMathCatalogV56Tests(unittest.TestCase):
    """Exercise the renderer's authenticated seams without copying the release."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[4]
        # The expensive, complete authority load and render are shared by the
        # unit tests.  The CLI test below is intentionally the only independent
        # end-to-end replay.
        cls.bundle = renderer.load_release(cls.root)
        cls.rendered = renderer.render_documents(cls.bundle)

        cls.legacy = next(
            row for row in cls.bundle.catalog_records if row["origin_release"] == "5.0"
        )
        cls.openconjecture = next(
            row for row in cls.bundle.catalog_records if row["origin_release"] == "5.2"
        )
        cls.mathlib = next(
            row for row in cls.bundle.catalog_records if row["origin_release"] == "5.6"
        )
        cls.oeis = next(
            row
            for row in cls.bundle.catalog_records
            if row["source_id"] == "SRC-MATH-V5-5-OEIS"
        )
        cls.open_problem_garden = next(
            row
            for row in cls.bundle.catalog_records
            if row["source_id"] == "SRC-MATH-V5-5-OPEN-PROBLEM-GARDEN"
        )

    @staticmethod
    def _reseal(document: dict[str, object]) -> dict[str, object]:
        result = dict(document)
        result["authority_sha256"] = renderer._hash_without(result, "authority_sha256")
        return result

    @staticmethod
    def _with_right(record: dict[str, object], field: str, value: object) -> dict[str, object]:
        result = dict(record)
        rights = dict(record["rights"])
        rights[field] = value
        result["rights"] = rights
        return result

    def test_real_release_renders_all_exact_projections(self) -> None:
        self.assertEqual(tuple(self.rendered), renderer.OUTPUT_FILES)
        self.assertEqual(len(self.bundle.theorem_ids), 3_500)
        self.assertEqual(len(self.bundle.open_ids), 2_025)
        self.assertEqual(len(self.bundle.strict_ids), 1_425)
        root_marker = (
            "sha256:" + self.bundle.manifest["release_root_sha256"]
        ).encode("ascii")
        for name in renderer.OUTPUT_FILES:
            with self.subTest(name=name):
                self.assertTrue(self.rendered[name].endswith(b"\n"))
                self.assertIn(root_marker, self.rendered[name])
        self.assertTrue(renderer.check_readable(self.bundle, self.rendered))

    def test_manifest_seal_and_release_root_mutations_are_rejected(self) -> None:
        stale_seal = dict(self.bundle.manifest)
        stale_seal["authority_sha256"] = "0" * 64
        with self.assertRaisesRegex(renderer.RenderError, "authority seal is stale"):
            renderer.validate_manifest(stale_seal)

        stale_root = dict(self.bundle.manifest)
        stale_root["release_root_sha256"] = "f" * 64
        stale_root = self._reseal(stale_root)
        with self.assertRaisesRegex(renderer.RenderError, "release root does not recompute"):
            renderer.validate_manifest(stale_root)

    def test_projection_id_and_copied_record_mutations_are_rejected(self) -> None:
        path = self.root / renderer.RELEASE_REL / renderer.OPEN_NAME
        official = renderer.parse_document_bytes(path.read_bytes(), renderer.OPEN_NAME)
        self.assertEqual(
            renderer.validate_projection(
                renderer.OPEN_NAME,
                official,
                self.bundle.catalog_records,
                bucket="open",
            ),
            self.bundle.open_ids,
        )

        bad_ids = dict(official)
        bad_ids["stage_claim_ids"] = list(official["stage_claim_ids"])
        bad_ids["stage_claim_ids"][0], bad_ids["stage_claim_ids"][1] = (
            bad_ids["stage_claim_ids"][1],
            bad_ids["stage_claim_ids"][0],
        )
        bad_ids = self._reseal(bad_ids)
        with self.assertRaisesRegex(renderer.RenderError, "IDs do not exactly match"):
            renderer.validate_projection(
                renderer.OPEN_NAME,
                bad_ids,
                self.bundle.catalog_records,
                bucket="open",
            )

        bad_record = dict(official)
        bad_record["records"] = list(official["records"])
        first = dict(bad_record["records"][0])
        first["display_name"] = str(first["display_name"]) + " mutated"
        bad_record["records"][0] = first
        bad_record = self._reseal(bad_record)
        with self.assertRaisesRegex(renderer.RenderError, "exact ordered catalog predicate"):
            renderer.validate_projection(
                renderer.OPEN_NAME,
                bad_record,
                self.bundle.catalog_records,
                bucket="open",
            )

    def test_strict_credit_rejects_false_flag_and_open_problem(self) -> None:
        stage_id = self.bundle.strict_ids[0]
        credit = self.bundle.strict_credit_by_id[stage_id]
        record = self.bundle.catalog_index[stage_id]

        false_flag = dict(credit)
        false_flag["grants_strict_conjecture_credit"] = False
        false_flag["row_sha256"] = renderer._hash_without(false_flag, "row_sha256")
        with self.assertRaisesRegex(renderer.RenderError, "active open conjecture"):
            renderer.validate_strict_credit(false_flag, record)

        open_problem = dict(record)
        open_problem["current_claim_kind"] = "open_problem"
        with self.assertRaisesRegex(renderer.RenderError, "active open conjecture"):
            renderer.validate_strict_credit(credit, open_problem)

    def test_statement_rights_allow_known_branches_and_fail_closed(self) -> None:
        allowed = (
            (
                "legacy Apache formal type",
                self.legacy,
                self.legacy["formal_statement"].get("declaration_type")
                or self.legacy["formal_statement"]["formal_type"],
            ),
            (
                "OpenConjecture CC-BY text",
                self.openconjecture,
                self.openconjecture["mathematical_statement"]["body_tex"],
            ),
            (
                "mathlib Apache formal type",
                self.mathlib,
                self.mathlib["formal_statement"]["formal_type"],
            ),
            (
                "reviewed OEIS assertion",
                self.oeis,
                self.oeis["mathematical_statement"]["exact_claim_text"],
            ),
            (
                "independent Open Problem Garden summary",
                self.open_problem_garden,
                self.open_problem_garden["mathematical_statement"]["semantic_summary"],
            ),
        )
        for label, record, expected in allowed:
            with self.subTest(label=label):
                self.assertEqual(renderer.statement_view(record).text, expected)

        denied = (
            (
                "legacy license drift",
                self._with_right(self.legacy, "formal_code_terms", "Proprietary"),
            ),
            (
                "withheld OpenConjecture text",
                self._with_right(self.openconjecture, "text_withheld", True),
            ),
            (
                "mathlib docstring license drift",
                self._with_right(self.mathlib, "docstring_terms", "unknown"),
            ),
            (
                "uncleared reviewed statement",
                self._with_right(
                    self.oeis, "cleared_for_catalog_metadata_and_statement", False
                ),
            ),
            (
                "Open Problem Garden source wording enabled",
                self._with_right(
                    self.open_problem_garden, "source_wording_redistributed", True
                ),
            ),
        )
        for label, record in denied:
            with self.subTest(label=label):
                with self.assertRaises(renderer.RenderError):
                    renderer.statement_view(record)

    def test_open_problem_garden_exact_source_wording_is_not_rendered(self) -> None:
        sentinel = "DO-NOT-RENDER-OPG-EXACT-SOURCE-WORDING"
        record = dict(self.open_problem_garden)
        statement = dict(record["mathematical_statement"])
        statement["exact_claim_text"] = sentinel
        record["mathematical_statement"] = statement

        view = renderer.statement_view(record)
        markdown = renderer._record_markdown(record, view)
        self.assertEqual(view.text, statement["semantic_summary"])
        self.assertNotIn(sentinel, view.text)
        self.assertNotIn(sentinel, markdown)

    def test_dynamic_fence_and_display_name_block_header_injection(self) -> None:
        injected_statement = "before\n```\n## S5-CLM-99999999\n`````\nafter"
        fenced = renderer._fenced(injected_statement, "lean")
        lines = fenced.splitlines()
        opening = re.fullmatch(r"(`+)lean", lines[0])
        self.assertIsNotNone(opening)
        self.assertGreater(len(opening.group(1)), 5)
        self.assertEqual(lines[-1], opening.group(1))
        self.assertIn(injected_statement, fenced)

        record = dict(self.mathlib)
        record["display_name"] = "safe name\n## S5-CLM-99999999 `forged`"
        markdown = renderer._record_markdown(
            record, renderer.statement_view(self.mathlib)
        )
        headings = re.findall(r"^## (S5-CLM-[0-9]{8})(?:\s|$)", markdown, re.MULTILINE)
        self.assertEqual(headings, [self.mathlib["stage_claim_id"]])

    def test_real_cli_check_is_read_only(self) -> None:
        readable = self.root / renderer.READABLE_REL
        before = {
            name: (
                (readable / name).stat().st_ino,
                (readable / name).stat().st_mtime_ns,
                (readable / name).stat().st_size,
            )
            for name in renderer.OUTPUT_FILES
        }
        result = subprocess.run(
            [
                sys.executable,
                str(Path(renderer.__file__).resolve()),
                "--repo-root",
                str(self.root),
                "--check",
            ],
            cwd=self.root.parent,
            text=True,
            capture_output=True,
            check=False,
            timeout=120,
        )
        after = {
            name: (
                (readable / name).stat().st_ino,
                (readable / name).stat().st_mtime_ns,
                (readable / name).stat().st_size,
            )
            for name in renderer.OUTPUT_FILES
        }
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS Stage5 readable projections 5.6", result.stdout)
        self.assertEqual(result.stderr, "")
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
