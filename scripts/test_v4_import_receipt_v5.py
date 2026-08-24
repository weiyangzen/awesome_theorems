#!/usr/bin/env python3
"""Tests for the independent Stage4 -> Stage5 import receipt."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "Docs/tools/build_v4_import_receipt_v5.py"
RECEIPT_PATH = ROOT / "Docs/catalog/v5/V4_Import_Receipt_v5.json"
SPEC = importlib.util.spec_from_file_location("build_v4_import_receipt_v5", BUILDER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import the v4 import-receipt builder")
builder = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = builder
SPEC.loader.exec_module(builder)


class V4ImportReceiptV5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.actual_bytes = RECEIPT_PATH.read_bytes()
        cls.actual = json.loads(cls.actual_bytes.decode("utf-8"))
        cls.rebuilt = builder.build_receipt(ROOT)
        cls.expected_bytes = builder.receipt_bytes(cls.rebuilt)

    def test_receipt_is_current_canonical_json_and_correctly_sealed(self) -> None:
        self.assertEqual(self.actual_bytes, self.expected_bytes)
        self.assertTrue(self.actual_bytes.endswith(b"\n"))
        self.assertNotIn(b"\n", self.actual_bytes[:-1])
        self.assertEqual(
            self.actual["authority_sha256"], builder._artifact_authority(self.actual)
        )

    def test_real_stage4_denominators_are_directly_represented(self) -> None:
        counts = self.actual["counts"]
        self.assertEqual(counts["official_outputs"], 13)
        self.assertEqual(counts["official_json_outputs"], 10)
        self.assertEqual(counts["official_markdown_outputs"], 3)
        self.assertEqual(counts["authoritative_source_artifacts"], 17)
        self.assertEqual(counts["source_occurrences"], 3484)
        self.assertEqual(counts["atv_variants"], 3484)
        self.assertEqual(counts["stage_claim_mappings"], 3484)
        self.assertEqual(counts["baseline_carry"], 3338)
        self.assertEqual(counts["stage4_additions"], 146)
        self.assertEqual(counts["historical_thm_aliases"], 3262)
        self.assertEqual(counts["folded_occurrences"], 76)
        self.assertEqual(counts["redirects"], 8)
        self.assertEqual(counts["splits"], 4)

    def test_variant_stage_crosswalk_is_a_full_ordinal_bijection(self) -> None:
        rows = self.actual["identity_import"]["variant_stage_crosswalk"]
        self.assertEqual(len(rows), 3484)
        self.assertEqual(len({row["atv_id"] for row in rows}), 3484)
        self.assertEqual(len({row["s4_claim_id"] for row in rows}), 3484)
        for row in rows:
            ordinal = row["ordinal"]
            self.assertEqual(row["atv_id"], f"ATV-{ordinal:08d}")
            self.assertEqual(row["s4_claim_id"], f"S4-CLM-{ordinal:08d}")
        self.assertEqual(rows[0]["atv_id"], "ATV-00000001")
        self.assertEqual(rows[-1]["atv_id"], "ATV-00003484")

    def test_historical_aliases_are_explicit_and_never_rebound(self) -> None:
        rows = self.actual["identity_import"]["historical_thm_alias_crosswalk"]
        self.assertEqual(len(rows), 3262)
        self.assertEqual(len({row["thm_alias_id"] for row in rows}), 3262)
        self.assertTrue(all(row["rebound"] is False for row in rows))
        fermat = next(row for row in rows if row["thm_alias_id"] == "THM-M-0387")
        self.assertEqual(fermat["historical_atv_id"], "ATV-00000393")
        self.assertEqual(fermat["historical_s4_claim_id"], "S4-CLM-00000393")

    def test_redirect_and_split_rows_retain_no_inheritance_boundary(self) -> None:
        redirects = self.actual["identity_import"]["redirects"]
        splits = self.actual["identity_import"]["splits"]
        self.assertEqual(len(redirects), 8)
        self.assertEqual(len(splits), 4)
        self.assertTrue(
            all(
                row["default_child"] is None and row["evidence_inherited"] is False
                for row in redirects
            )
        )
        self.assertTrue(
            all(
                row["default_child"] is None
                and row["default_child_id"] is None
                and row["evidence_inherited"] is False
                for row in splits
            )
        )

    def test_every_bound_artifact_matches_current_bytes(self) -> None:
        for row in self.actual["official_outputs"]:
            payload = (ROOT / row["path"]).read_bytes()
            self.assertEqual(row["size_bytes"], len(payload))
            self.assertEqual(row["sha256"], builder.sha256_bytes(payload))
        for row in self.actual["authoritative_sources"]:
            payload = (ROOT / row["path"]).read_bytes()
            self.assertEqual(row["size_bytes"], len(payload))
            self.assertEqual(row["sha256"], builder.sha256_bytes(payload))

    def test_independent_checker_result_is_bound(self) -> None:
        check = self.actual["independent_checker"]
        self.assertEqual(check["status"], "passed")
        self.assertEqual(check["exit_code"], 0)
        self.assertEqual(
            check["argv"],
            ["python3", "scripts/check_claim_catalog_v4.py", "--require-complete"],
        )
        self.assertIn("PASS check_claim_catalog_v4 --require-complete", check["stdout"]["text_utf8"])
        self.assertEqual(check["stderr"]["size_bytes"], 0)

    def test_duplicate_json_keys_and_stale_authority_fail_closed(self) -> None:
        with self.assertRaises(builder.ImportReceiptError):
            builder.strict_json_bytes(b'{"x":1,"x":2}', "mutation.json")
        mutated = dict(self.actual)
        mutated["counts"] = dict(mutated["counts"])
        mutated["counts"]["atv_variants"] -= 1
        self.assertNotEqual(mutated["authority_sha256"], builder._artifact_authority(mutated))

    def test_cli_check_is_read_only_and_passes(self) -> None:
        before = RECEIPT_PATH.read_bytes()
        result = subprocess.run(
            [sys.executable, str(BUILDER_PATH), "--check"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PASS build_v4_import_receipt_v5 (checked)", result.stdout)
        self.assertEqual(RECEIPT_PATH.read_bytes(), before)

    def test_safe_path_rejects_escape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(builder.ImportReceiptError):
                builder._safe_repo_file(root, "../escape.json")


if __name__ == "__main__":
    unittest.main()
