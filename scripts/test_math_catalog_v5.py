#!/usr/bin/env python3
"""Positive, mutation, and determinism tests for the Stage5 math releases."""

from __future__ import annotations

import ast
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check_math_catalog_v5.py"
GENERATOR_PATH = ROOT / "Docs" / "tools" / "generate_math_catalog_v5.py"

SPEC = importlib.util.spec_from_file_location("check_math_catalog_v5", CHECKER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import independent Stage5 checker")
checker_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker_module
SPEC.loader.exec_module(checker_module)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def tree_snapshot(path: Path) -> dict[str, tuple[str, int, int, int]]:
    result: dict[str, tuple[str, int, int, int]] = {}
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        stat = item.stat()
        result[str(item.relative_to(path))] = (
            checker_module.sha256_file(item),
            stat.st_size,
            stat.st_mtime_ns,
            stat.st_ino,
        )
    return result


class MathCatalogV5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = load_json(ROOT / checker_module.CONTRACT_PATH)
        cls.schema = load_json(ROOT / checker_module.SCHEMA_PATH)
        cls.source_registry = load_json(ROOT / checker_module.SOURCE_REGISTRY_PATH)
        cls.v4_registry = load_json(ROOT / checker_module.V4_REGISTRY_PATH)
        cls.parent_ids = {
            row["variant_id"] for row in cls.v4_registry["variants"]
        }
        cls.documents = {
            release: {
                checker_module.MANIFEST_NAME: load_json(
                    ROOT
                    / checker_module.release_dir(release)
                    / checker_module.MANIFEST_NAME
                ),
                **{
                    name: load_json(
                        ROOT / checker_module.release_dir(release) / name
                    )
                    for name in checker_module.RELEASE_FILES
                },
            }
            for release in checker_module.RELEASES
        }
        source_checker = checker_module.Checker(ROOT)
        cls.sources = checker_module.check_source_registry(
            source_checker, cls.source_registry
        )
        if source_checker.errors:
            raise AssertionError("invalid source registry: " + "; ".join(source_checker.errors))
        cls.candidates = checker_module.rebuild_formal_candidates(
            source_checker, cls.sources
        )

    def test_static_independent_checker_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CHECKER_PATH)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PASS check_math_catalog_v5", result.stdout)

    def test_static_checker_imports_no_generator_or_extractor(self) -> None:
        tree = ast.parse(CHECKER_PATH.read_text(encoding="utf-8"))
        imported: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.append(node.module or "")
        forbidden = [name for name in imported if "generat" in name or "extract" in name]
        self.assertEqual(forbidden, [])

    def test_independent_tar_extraction_count_and_digest_are_pinned(self) -> None:
        self.assertEqual(
            len(self.candidates), checker_module.PINNED_CANDIDATE_COUNT
        )
        jsonl = b"".join(
            checker_module.canonical_json_bytes(row) + b"\n"
            for row in self.candidates
        )
        self.assertEqual(
            checker_module.sha256_bytes(jsonl),
            checker_module.PINNED_EXTRACTION_JSONL_SHA256,
        )

    def test_exact_thresholds_parent_universe_and_append_only_ids(self) -> None:
        self.assertEqual(
            self.parent_ids,
            {f"ATV-{value:08d}" for value in range(1, 3485)},
        )
        result_sets: dict[str, set[str]] = {}
        for release in checker_module.RELEASES:
            records = checker_module.artifact_rows(
                self.documents[release]["Claim_Catalog.json"]
            )
            origin = [row for row in records if checker_module.origin_release(row) == release]
            theorems = {
                checker_module.record_variant_id(row)
                for row in origin
                if checker_module.is_quota_theorem(row)
            }
            open_claims = {
                checker_module.record_variant_id(row)
                for row in origin
                if checker_module.is_quota_open_claim(row)
            }
            self.assertGreaterEqual(
                len(theorems), checker_module.MINIMUMS[release]["theorem"]
            )
            self.assertGreaterEqual(
                len(open_claims), checker_module.MINIMUMS[release]["open"]
            )
            ids = set(
                checker_module.registry_variant_ids(
                    self.documents[release]["Claim_ID_Registry.json"]
                )
            )
            suffix = checker_module.expected_suffix(
                ids - self.parent_ids, checker_module.FIRST_STAGE5_ORDINAL
            )
            self.assertTrue(suffix)
            result_sets[release] = ids
        self.assertTrue(result_sets["5.0"] <= result_sets["5.1"])

    def test_atv_s5_bijection_has_equal_ordinals(self) -> None:
        for release in checker_module.RELEASES:
            rows = checker_module.artifact_rows(
                self.documents[release]["Stage5_Claim_ID_Registry.json"]
            )
            pairs = [
                (
                    checker_module.record_variant_id(row),
                    checker_module.record_stage_id(row),
                )
                for row in rows
            ]
            self.assertEqual(len(pairs), len({atv for atv, _ in pairs}))
            self.assertEqual(len(pairs), len({stage for _, stage in pairs}))
            for atv, stage in pairs:
                self.assertIsNotNone(atv)
                self.assertIsNotNone(stage)
                assert atv is not None and stage is not None
                self.assertEqual(
                    checker_module.ordinal(atv, checker_module.ATV_RE),
                    checker_module.ordinal(stage, checker_module.S5_RE),
                )

    def test_manifest_roots_and_s51_parent_are_byte_bound(self) -> None:
        roots: dict[str, str] = {}
        for release in checker_module.RELEASES:
            inventory = checker_module.release_inventory(ROOT, release)
            roots[release] = checker_module.release_root_sha256(inventory)
            manifest = self.documents[release][checker_module.MANIFEST_NAME]
            self.assertEqual(manifest["release_root_sha256"], roots[release])
            by_path = {row["path"]: row for row in manifest["artifacts"]}
            self.assertEqual(set(by_path), set(checker_module.RELEASE_FILES))
            for row in inventory:
                self.assertEqual(by_path[row["path"]]["sha256"], row["sha256"])
                self.assertEqual(
                    by_path[row["path"]]["size_bytes"], row["size_bytes"]
                )
                self.assertEqual(
                    by_path[row["path"]]["row_count"],
                    checker_module.artifact_row_count(
                        row["path"], self.documents[release][row["path"]]
                    ),
                )
        child = self.documents["5.1"][checker_module.MANIFEST_NAME]
        self.assertEqual(
            child.get("parent_release"),
            "5.0",
        )
        self.assertEqual(
            child.get("parent_release_root_sha256"),
            roots["5.0"],
        )

    def test_coverage_candidate_and_msc_sets_are_explicit(self) -> None:
        for release in checker_module.RELEASES:
            ledger = self.documents[release]["Coverage_Ledger.json"]
            candidates = ledger["candidate_dispositions"]
            msc_rows = ledger["msc_coverage"]
            self.assertEqual(len(candidates), checker_module.PINNED_CANDIDATE_COUNT)
            self.assertEqual(
                [row["msc_top_class"] for row in msc_rows],
                self.contract["msc_coverage_policy"]["top_level_classes"],
            )
            self.assertEqual(len(msc_rows), 63)
            audit = checker_module.Checker(ROOT)
            checker_module.check_coverage_ledger(
                audit,
                release,
                ledger,
                {
                    row["variant_id"]: row
                    for row in checker_module.artifact_rows(
                        self.documents[release]["Claim_Catalog.json"]
                    )
                },
                self.contract,
                self.sources,
                self.candidates,
            )
            self.assertEqual(audit.errors, [])

    def test_semantic_and_raw_source_hashes_recompute(self) -> None:
        audit = checker_module.Checker(ROOT)
        for release in checker_module.RELEASES:
            records = checker_module.artifact_rows(
                self.documents[release]["Claim_Catalog.json"]
            )
            for row in records:
                if checker_module.origin_release(row) != release:
                    continue
                self.assertEqual(
                    row["statement_sha256"],
                    checker_module.statement_digest(row["statement"]),
                )
                self.assertEqual(
                    row["mathematical_statement"]["statement_sha256"],
                    row["statement_sha256"],
                )
                self.assertEqual(
                    {
                        key: value
                        for key, value in row["mathematical_statement"].items()
                        if key != "statement_sha256"
                    },
                    row["statement"],
                )
                self.assertEqual(
                    row["dedupe"]["normalized_statement_sha256"],
                    checker_module.contextual_statement_sha256(row),
                )
                source = self.sources[row["source_id"]]
                block = checker_module.locator_payload(
                    audit, source, row["locator"], row["variant_id"]
                )
                text = block.decode("utf-8")
                self.assertIn(row["formal_declaration"], text)
                self.assertIn(row["formal_docstring"], text)

    def test_manifest_count_spoof_is_rejected(self) -> None:
        release = "5.0"
        catalog = dict(self.documents[release]["Claim_Catalog.json"])
        catalog["counts"] = dict(catalog.get("counts", {}))
        catalog["counts"]["origin_theorems"] = 10_000_000
        audit = checker_module.Checker(ROOT)
        checker_module.check_declared_catalog_counts(
            audit,
            release,
            catalog,
            checker_module.artifact_rows(catalog),
        )
        self.assertTrue(any("not recomputed truth" in error for error in audit.errors))

    def test_projection_excludes_lemma_from_theorem_credit(self) -> None:
        release = "5.0"
        row = copy.deepcopy(
            next(
                row
                for row in checker_module.artifact_rows(
                    self.documents[release]["Claim_Catalog.json"]
                )
                if checker_module.is_quota_theorem(row)
            )
        )
        row["declaration_kind"] = "lemma"
        row["formal_statement"]["declaration_kind"] = "lemma"
        self.assertTrue(checker_module.is_theorem(row))
        self.assertFalse(checker_module.is_quota_theorem(row))

    def test_contextual_duplicate_keys_are_rejected(self) -> None:
        release = "5.0"
        records = [
            row
            for row in checker_module.artifact_rows(
                self.documents[release]["Claim_Catalog.json"]
            )
            if checker_module.origin_release(row) == release
        ]
        self.assertGreaterEqual(len(records), 2)
        left = dict(records[0])
        right = dict(records[1])
        for key in (
            "source_id",
            "qualified_name",
            "module",
            "namespace",
            "formal_declaration",
        ):
            right[key] = left[key]
        right["dedupe"] = dict(right["dedupe"])
        right["dedupe"]["source_statement_sha256"] = left["dedupe"][
            "source_statement_sha256"
        ]
        right["dedupe"]["normalized_statement_sha256"] = left["dedupe"][
            "normalized_statement_sha256"
        ]
        audit = checker_module.Checker(ROOT)
        checker_module.check_quota_duplicates(audit, release, [left, right])
        self.assertGreaterEqual(len(audit.errors), 3)

    def test_same_surface_text_in_distinct_context_is_not_duplicate(self) -> None:
        release = "5.0"
        row = next(
            row
            for row in checker_module.artifact_rows(
                self.documents[release]["Claim_Catalog.json"]
            )
            if checker_module.origin_release(row) == release
        )
        left = copy.deepcopy(row)
        right = copy.deepcopy(row)
        right["variant_id"] = "ATV-99999999"
        right["source_id"] = left["source_id"]
        right["qualified_name"] = left["qualified_name"] + ".ContextB"
        right["module"] = left["module"] + ".ContextB"
        right["namespace"] = left["namespace"] + ".ContextB"
        right["formal_declaration"] = left["formal_declaration"]
        right["dedupe"]["normalized_statement_sha256"] = (
            checker_module.contextual_statement_sha256(right)
        )
        audit = checker_module.Checker(ROOT)
        checker_module.check_quota_duplicates(audit, release, [left, right])
        self.assertEqual(audit.errors, [])

    def test_wrong_status_breaks_exact_projection(self) -> None:
        release = "5.1"
        catalog_rows = checker_module.artifact_rows(
            self.documents[release]["Claim_Catalog.json"]
        )
        by_atv = {
            row["variant_id"]: row for row in catalog_rows
        }
        victim_id = next(
            row["variant_id"]
            for row in catalog_rows
            if checker_module.origin_release(row) == release
            and checker_module.is_quota_theorem(row)
        )
        mutated = dict(by_atv)
        victim = dict(mutated[victim_id])
        victim["material_status"] = "open"
        mutated[victim_id] = victim
        stage_by_atv = {
            row["variant_id"]: row["stage_claim_id"]
            for row in checker_module.artifact_rows(
                self.documents[release]["Stage5_Claim_ID_Registry.json"]
            )
        }
        audit = checker_module.Checker(ROOT)
        checker_module.check_projections(
            audit,
            release,
            self.documents[release],
            mutated,
            stage_by_atv,
        )
        self.assertTrue(any("theorem projection" in error for error in audit.errors))

    def test_historical_migration_drift_is_rejected(self) -> None:
        release = "5.0"
        documents = dict(self.documents[release])
        migration = dict(documents["Migration_v4_to_v5.json"])
        rows = list(checker_module.artifact_rows(migration))
        rows[0] = dict(rows[0])
        target_key = next(
            key
            for key in ("variant_id", "target_variant_id", "atv_id")
            if key in rows[0]
        )
        rows[0][target_key] = "ATV-99999999"
        row_field = next(
            key
            for key in ("migrations", "records", "rows")
            if isinstance(migration.get(key), list)
        )
        migration[row_field] = rows
        documents["Migration_v4_to_v5.json"] = migration
        catalog_ids = {
            row["variant_id"]
            for row in checker_module.artifact_rows(documents["Claim_Catalog.json"])
        }
        audit = checker_module.Checker(ROOT)
        checker_module.check_numbering_and_migration(
            audit, release, documents, catalog_ids, self.parent_ids
        )
        self.assertTrue(
            any(
                "rebinds" in error or "outside the release ATV/S5 registry" in error
                for error in audit.errors
            )
        )

    def test_statement_and_raw_block_hash_tampering_are_rejected(self) -> None:
        release = "5.0"
        row = next(
            row
            for row in checker_module.artifact_rows(
                self.documents[release]["Claim_Catalog.json"]
            )
            if checker_module.origin_release(row) == release
        )
        semantic = dict(row)
        semantic["statement"] = {"tampered": True}
        audit = checker_module.Checker(ROOT)
        checker_module.check_record_content(
            audit,
            release,
            [semantic],
            self.contract,
            self.sources,
            self.candidates,
        )
        self.assertTrue(any("statement hash" in error for error in audit.errors))

        raw = dict(row)
        raw["locator"] = dict(raw["locator"])
        raw["locator"]["raw_block_sha256"] = "0" * 64
        audit = checker_module.Checker(ROOT)
        checker_module.check_record_content(
            audit,
            release,
            [raw],
            self.contract,
            self.sources,
            self.candidates,
        )
        self.assertTrue(any("raw block hash" in error for error in audit.errors))

    def test_swapped_source_status_and_category_are_rejected(self) -> None:
        release = "5.0"
        rows = [
            row
            for row in checker_module.artifact_rows(
                self.documents[release]["Claim_Catalog.json"]
            )
            if checker_module.origin_release(row) == release
        ]
        theorem = copy.deepcopy(
            next(row for row in rows if row["raw_category"] != "research open")
        )
        open_claim = copy.deepcopy(
            next(
                row
                for row in rows
                if row["raw_category"] == "research open"
                and row["claim_kind"] == "conjecture"
            )
        )
        for field in (
            "raw_category",
            "raw_status",
            "category",
            "material_status",
        ):
            theorem[field], open_claim[field] = open_claim[field], theorem[field]
        audit = checker_module.Checker(ROOT)
        checker_module.check_record_content(
            audit,
            release,
            [theorem, open_claim],
            self.contract,
            self.sources,
            self.candidates,
        )
        self.assertTrue(
            any("independently parsed source" in error for error in audit.errors),
            audit.errors,
        )

    def test_forged_noncredit_candidate_is_rejected(self) -> None:
        release = "5.0"
        ledger = copy.deepcopy(self.documents[release]["Coverage_Ledger.json"])
        victim = next(
            row
            for row in ledger["candidate_dispositions"]
            if row["disposition"] == "pointer_noncredit"
        )
        victim["candidate_key"] = (
            "formal-conjectures:FormalConjectures/Forged.lean#Forged.claim"
        )
        victim["qualified_name"] = "Forged.claim"
        victim["source_statement_sha256"] = "1" * 64
        victim["normalized_statement_sha256"] = "2" * 64
        victim["evidence_locator_sha256"] = "3" * 64
        catalog_by_atv = {
            row["variant_id"]: row
            for row in checker_module.artifact_rows(
                self.documents[release]["Claim_Catalog.json"]
            )
        }
        audit = checker_module.Checker(ROOT)
        checker_module.check_coverage_ledger(
            audit,
            release,
            ledger,
            catalog_by_atv,
            self.contract,
            self.sources,
            self.candidates,
        )
        self.assertTrue(
            any(
                "source universe" in error or "forged or unknown" in error
                for error in audit.errors
            ),
            audit.errors,
        )

    def test_known_noncredit_candidate_field_forgery_is_rejected(self) -> None:
        release = "5.1"
        catalog_by_atv = {
            row["variant_id"]: row
            for row in checker_module.artifact_rows(
                self.documents[release]["Claim_Catalog.json"]
            )
        }
        mutations = (
            ("pointer_noncredit", "disposition", "excluded_by_source_policy"),
            ("pointer_noncredit", "reason_code", "forged_reason"),
            ("pointer_noncredit", "source_statement_sha256", "4" * 64),
            ("pointer_noncredit", "evidence_locator_sha256", "5" * 64),
            ("duplicate_noncredit", "duplicate_of_variant_id", "ATV-00000001"),
        )
        for disposition, field, forged_value in mutations:
            with self.subTest(field=field):
                ledger = copy.deepcopy(
                    self.documents[release]["Coverage_Ledger.json"]
                )
                victim = next(
                    row
                    for row in ledger["candidate_dispositions"]
                    if row["disposition"] == disposition
                )
                victim[field] = forged_value
                audit = checker_module.Checker(ROOT)
                checker_module.check_coverage_ledger(
                    audit,
                    release,
                    ledger,
                    catalog_by_atv,
                    self.contract,
                    self.sources,
                    self.candidates,
                )
                self.assertTrue(
                    any(
                        "independently rebuilt candidate/disposition truth"
                        in error
                        for error in audit.errors
                    ),
                    audit.errors,
                )

    def test_allocated_candidate_ordinal_swap_is_rejected(self) -> None:
        release = "5.0"
        rows = checker_module.artifact_rows(
            self.documents[release]["Claim_Catalog.json"]
        )
        left, right = copy.deepcopy(rows[0]), copy.deepcopy(rows[1])
        for field in (
            "occurrence_id",
            "family_id",
            "sense_id",
            "variant_id",
            "stage_claim_id",
        ):
            left[field], right[field] = right[field], left[field]
        left["allocation"]["transaction_id"], right["allocation"][
            "transaction_id"
        ] = (
            right["allocation"]["transaction_id"],
            left["allocation"]["transaction_id"],
        )
        audit = checker_module.Checker(ROOT)
        checker_module.check_record_content(
            audit,
            release,
            [left, right],
            self.contract,
            self.sources,
            self.candidates,
        )
        self.assertTrue(
            any("candidate/ordinal binding" in error for error in audit.errors),
            audit.errors,
        )

    def test_source_rights_inflation_is_rejected(self) -> None:
        release = "5.0"
        row = copy.deepcopy(
            checker_module.artifact_rows(
                self.documents[release]["Claim_Catalog.json"]
            )[0]
        )
        row["rights"].update(
            {
                "docstring_terms": "Apache-2.0",
                "status": "cleared",
                "not_independently_cleared": False,
                "attribution": ["forged"],
            }
        )
        audit = checker_module.Checker(ROOT)
        checker_module.check_record_content(
            audit,
            release,
            [row],
            self.contract,
            self.sources,
            self.candidates,
        )
        self.assertTrue(
            any("rights differ" in error for error in audit.errors),
            audit.errors,
        )

    def test_manifest_hash_and_root_tampering_are_rejected(self) -> None:
        release = "5.0"
        for mutation in ("artifact", "root"):
            manifest = copy.deepcopy(
                self.documents[release][checker_module.MANIFEST_NAME]
            )
            if mutation == "artifact":
                manifest["artifacts"][0]["sha256"] = "0" * 64
            else:
                manifest["release_root_sha256"] = "0" * 64
            audit = checker_module.Checker(ROOT)
            checker_module.check_manifest(
                audit, release, manifest, self.documents[release]
            )
            self.assertTrue(audit.errors, mutation)

    def test_two_generator_checks_are_identical_and_read_only(self) -> None:
        self.assertTrue(GENERATOR_PATH.is_file(), GENERATOR_PATH)
        release_root = ROOT / checker_module.V5_ROOT / "releases"
        before = tree_snapshot(release_root)
        outputs: list[str] = []
        for _ in range(2):
            result = subprocess.run(
                [sys.executable, str(GENERATOR_PATH), "--check"],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout)
            outputs.append(result.stdout)
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(tree_snapshot(release_root), before)


if __name__ == "__main__":
    unittest.main()
