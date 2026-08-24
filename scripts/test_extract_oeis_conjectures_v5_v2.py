#!/usr/bin/env python3
"""Tests for the all-``conjectur``-within-pinned-622 OEIS source layer."""

from __future__ import annotations

from collections import Counter
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
EXTRACTOR_PATH = ROOT / "Docs/tools/extract_oeis_conjectures_v5_v2.py"

SPEC = importlib.util.spec_from_file_location(
    "extract_oeis_conjectures_v5_v2", EXTRACTOR_PATH
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load extractor at {EXTRACTOR_PATH}")
extractor = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = extractor
SPEC.loader.exec_module(extractor)


def ascii_lower(text: str) -> str:
    """Independent oracle spelling; do not reuse the extractor regex."""

    return "".join(
        chr(ord(character) + 32) if "A" <= character <= "Z" else character
        for character in text
    )


def location_key(location: dict[str, object]) -> tuple[object, ...]:
    return (
        location["a_number"],
        location["field"],
        location["line_number"],
        location["original_text"],
    )


class ExtractOeisConjecturesV5V2Tests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = extractor.load_source_archive()
        cls.v1_rows = extractor.load_v1_candidate_rows()
        cls.result = extractor.extract_candidates(cls.bundle, cls.v1_rows)
        cls.asset_bytes = extractor.DEFAULT_CANDIDATE_ASSET.read_bytes()
        cls.rows = extractor.load_candidate_asset(
            extractor.DEFAULT_CANDIDATE_ASSET,
            bundle=cls.bundle,
            v1_rows=cls.v1_rows,
        )

    def temporary_asset(self, payload: bytes) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "candidates.jsonl"
        path.write_bytes(payload)
        return path

    def assert_replay_rejects(self, rows: list[dict[str, object]]) -> None:
        path = self.temporary_asset(extractor.encode_candidates(rows))
        with self.assertRaisesRegex(
            extractor.ExtractionError,
            "candidate rows do not replay from the pinned source",
        ):
            extractor.load_candidate_asset(
                path,
                bundle=self.bundle,
                v1_rows=self.v1_rows,
                enforce_asset_lock=False,
            )

    def test_vendored_digest_size_rows_and_exact_replay(self) -> None:
        self.assertEqual(len(self.asset_bytes), 3_733_739)
        self.assertEqual(
            extractor.sha256_bytes(self.asset_bytes),
            "18da1f5881f0410f2c38dc8362271b536db11c4509d58812942a11981181ec3d",
        )
        self.assertEqual(len(self.rows), 1_101)
        self.assertEqual(self.rows, list(self.result.candidates))
        self.assertEqual(
            self.asset_bytes, extractor.encode_candidates(self.result.candidates)
        )
        self.assertEqual(
            self.result.summary["candidate_asset_sha256"],
            extractor.CANDIDATE_ASSET_SHA256,
        )

    def test_independent_field_line_oracle_matches_every_location_once(self) -> None:
        expected: list[tuple[object, ...]] = []
        excluded: list[tuple[object, ...]] = []
        field_counts: Counter[str] = Counter()
        stem_matches = 0
        entries: set[str] = set()
        for entry in self.bundle.entries:
            for field in entry.fields:
                lowered = ascii_lower(field.text)
                if "conjectur" not in lowered:
                    continue
                key = (entry.a_number, field.field, field.line_number, field.text)
                if field.field in {"%N", "%C", "%F"}:
                    expected.append(key)
                    field_counts[field.field] += 1
                    stem_matches += lowered.count("conjectur")
                    entries.add(entry.a_number)
                else:
                    excluded.append(key)

        observed = [
            location_key(location)
            for row in self.rows
            for location in row["locations"]
        ]
        self.assertEqual(sorted(observed), sorted(expected))
        self.assertEqual(len(observed), len(set(observed)))
        self.assertEqual(len(observed), 1_141)
        self.assertEqual(stem_matches, 1_304)
        self.assertEqual(len(entries), 611)
        self.assertEqual(dict(sorted(field_counts.items())), {"%C": 875, "%F": 220, "%N": 46})
        self.assertTrue(
            any(key[0] == "A029889" and key[1] == "%Y" for key in excluded)
        )
        self.assertFalse(any(key[0] == "A029889" for key in observed))

    def test_occurrence_group_and_normalization_counts_are_not_claim_counts(self) -> None:
        self.assertEqual(sum(row["occurrence_count"] for row in self.rows), 1_141)
        self.assertEqual(
            sum(
                location["literal_stem_match_count"]
                for row in self.rows
                for location in row["locations"]
            ),
            1_304,
        )
        group_sizes = Counter(row["occurrence_count"] for row in self.rows)
        self.assertEqual(group_sizes, Counter({1: 1078, 2: 12, 3: 7, 4: 2, 5: 2}))
        self.assertEqual(sum(group_sizes[size] for size in group_sizes if size > 1), 23)
        self.assertEqual(
            sum((size - 1) * count for size, count in group_sizes.items()), 40
        )
        self.assertEqual(
            len(
                {
                    location["original_text"]
                    for row in self.rows
                    for location in row["locations"]
                }
            ),
            1_104,
        )
        for row in self.rows:
            self.assertIs(
                row["dedupe_boundary"]["semantic_deduplication_performed"], False
            )
            self.assertIs(
                row["dedupe_boundary"]["normalized_key_is_not_semantic_identity"],
                True,
            )
            self.assertIs(
                row["discovery_boundary"]["archive_population_is_not_oeis_complete"],
                True,
            )

    def test_case_stem_headings_and_multiple_hits_are_retained_as_lines(self) -> None:
        locations = [
            location for row in self.rows for location in row["locations"]
        ]
        self.assertTrue(
            any(location["original_text"].strip() == "Conjecture:" for location in locations)
        )
        uppercase = [
            location
            for location in locations
            if "CONJECTURE:" in location["original_text"]
        ]
        self.assertTrue(uppercase)
        seven = [
            location
            for location in locations
            if location["literal_stem_match_count"] == 7
        ]
        self.assertEqual(len(seven), 1)
        self.assertEqual(
            (seven[0]["a_number"], seven[0]["field"], seven[0]["line_number"]),
            ("A087207", "%C", 11),
        )

    def test_resolution_language_is_retained_as_a_nonexhaustive_hint(self) -> None:
        locations = [
            location for row in self.rows for location in row["locations"]
        ]
        risk = [
            location
            for location in locations
            if location["review_hints"]["possible_resolution_language"]
        ]
        self.assertEqual(len(risk), 68)
        self.assertEqual(len({location_key(location) for location in risk}), 68)
        self.assertEqual(
            sum(
                row["review_hint_location_counts"]["possible_resolution_language"]
                for row in self.rows
            ),
            68,
        )
        for location in risk:
            self.assertIs(location["review_hints"]["retained_regardless_of_hints"], True)
            self.assertIs(location["review_hints"]["hints_are_non_dispositive"], True)
            self.assertIs(location["review_hints"]["hints_are_nonexhaustive"], True)

        by_position = {
            (location["a_number"], location["field"], location["line_number"]): location
            for location in locations
        }
        for position in (
            ("A002496", "%C", 6),
            ("A065706", "%C", 7),
            ("A083844", "%C", 6),
            ("A224363", "%C", 6),
        ):
            self.assertTrue(
                by_position[position]["review_hints"]["possible_resolution_language"]
            )
            self.assertTrue(
                by_position[position]["review_hints"]["possible_unresolved_language"]
            )

        # These resolved-looking lines are also retained.  Their false legacy
        # hint demonstrates why the hint is explicitly nonexhaustive and is not
        # an open/closed adjudication.
        for position in (("A108411", "%C", 8), ("A212198", "%C", 8)):
            self.assertIn(position, by_position)
            self.assertFalse(
                by_position[position]["review_hints"]["possible_resolution_language"]
            )

    def test_v1_locations_are_a_strict_subset_and_no_v1_key_is_lost(self) -> None:
        legacy_result = extractor.v1.extract_candidates(self.bundle)
        legacy_locations = {
            (
                row["a_number"],
                row["field"],
                row["line_number"],
                row["original_text"],
            )
            for row in legacy_result.occurrences
        }
        legacy_locations.update(
            (
                row["a_number"],
                row["field"],
                row["line_number"],
                row["original_text"],
            )
            for row in legacy_result.quarantined
        )
        v2_locations = {
            location_key(location)
            for row in self.rows
            for location in row["locations"]
        }
        flagged_legacy_locations = {
            location_key(location)
            for row in self.rows
            for location in row["locations"]
            if location["legacy_v1_discovery"]["narrow_marker_matched"]
        }
        self.assertEqual(len(legacy_locations), 665)
        self.assertEqual(flagged_legacy_locations, legacy_locations)
        self.assertTrue(legacy_locations < v2_locations)
        self.assertEqual(len(v2_locations - legacy_locations), 476)

        v1_keys = {row["candidate_key"] for row in self.v1_rows}
        v2_keys = {row["candidate_key"] for row in self.rows}
        self.assertEqual(len(v1_keys), 602)
        self.assertEqual(len(v2_keys), 1_101)
        self.assertEqual(len(v1_keys & v2_keys), 602)
        self.assertEqual(len(v2_keys - v1_keys), 499)
        self.assertEqual(len(v1_keys - v2_keys), 0)
        self.assertEqual(
            extractor.sha256_bytes(extractor.canonical_json_bytes(sorted(v2_keys))),
            "5c28cb9863046900fe865aa76fddf2d1d65ef326dccea7c6f0ba28a11b30300a",
        )

    def test_every_row_is_review_only_and_grants_no_credit(self) -> None:
        normalized = [row["normalized_text"] for row in self.rows]
        self.assertEqual(normalized, sorted(normalized))
        self.assertEqual(
            len({row["candidate_key"] for row in self.rows}), len(self.rows)
        )
        for row in self.rows:
            self.assertIs(row["candidate_only"], True)
            self.assertIs(row["grants_catalog_entry"], False)
            self.assertIs(row["grants_strict_conjecture_credit"], False)
            self.assertEqual(
                row["candidate_key"],
                f"oeis-normalized/{extractor.sha256_bytes(row['normalized_text'].encode('utf-8'))}",
            )
            self.assertEqual(
                row["normalized_text_sha256"], row["candidate_key"].split("/", 1)[1]
            )
            self.assertEqual(row["occurrence_count"], len(row["locations"]))
            self.assertEqual(
                row["a_number_count"],
                len({location["a_number"] for location in row["locations"]}),
            )
            self.assertEqual(
                row["status_boundary"]["current_open_status"],
                "not_independently_reviewed",
            )
            self.assertEqual(
                row["status_boundary"]["atomicity_status"],
                "not_independently_reviewed",
            )

    def test_lock_off_loader_rejects_canonical_schema_and_order_tampering(self) -> None:
        mutations: dict[str, object] = {}

        rows = copy.deepcopy(self.rows)
        rows[0]["grants_strict_conjecture_credit"] = True
        mutations["grant"] = rows

        rows = copy.deepcopy(self.rows)
        del rows[0]["locations"][0]["review_hints"]
        mutations["missing_hint"] = rows

        rows = copy.deepcopy(self.rows)
        rows[0]["locations"][0]["field"] = "%Y"
        mutations["wrong_field"] = rows

        rows = copy.deepcopy(self.rows)
        rows[0]["locations"][0]["original_text"] = "no lexical marker remains"
        mutations["wrong_original"] = rows

        rows = copy.deepcopy(self.rows)
        rows[0]["occurrence_count"] += 1
        mutations["wrong_count"] = rows

        rows = copy.deepcopy(self.rows)
        rows[0]["candidate_key"] = "oeis-normalized/" + "0" * 64
        mutations["wrong_key"] = rows

        rows = copy.deepcopy(self.rows)
        rows[0]["normalized_text_sha256"] = "0" * 64
        mutations["wrong_hash"] = rows

        rows = copy.deepcopy(self.rows)
        rows[0]["locations"].append(copy.deepcopy(rows[0]["locations"][0]))
        mutations["duplicate_location"] = rows

        rows = copy.deepcopy(self.rows)
        rows[0], rows[1] = rows[1], rows[0]
        mutations["wrong_order"] = rows

        for label, mutated in mutations.items():
            with self.subTest(label=label):
                self.assert_replay_rejects(mutated)

    def test_noncanonical_json_and_missing_final_lf_are_rejected(self) -> None:
        lines = self.asset_bytes.splitlines()
        first = json.loads(lines[0])
        lines[0] = json.dumps(first, ensure_ascii=False).encode("utf-8")
        path = self.temporary_asset(b"\n".join(lines) + b"\n")
        with self.assertRaisesRegex(extractor.ExtractionError, "not canonical"):
            extractor.load_candidate_asset(
                path,
                bundle=self.bundle,
                v1_rows=self.v1_rows,
                enforce_asset_lock=False,
            )

        path = self.temporary_asset(self.asset_bytes[:-1])
        with self.assertRaisesRegex(extractor.ExtractionError, "lacks one final LF"):
            extractor.load_candidate_asset(
                path,
                bundle=self.bundle,
                v1_rows=self.v1_rows,
                enforce_asset_lock=False,
            )

    def test_cli_check_and_summary(self) -> None:
        checked = subprocess.run(
            [sys.executable, str(EXTRACTOR_PATH), "--check"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            checked.stdout.strip(),
            "PASS extract_oeis_conjectures_v5_v2 occurrences=1141 "
            "candidates=1101 v1_intersection=602 v2_only=499",
        )
        summary = subprocess.run(
            [sys.executable, str(EXTRACTOR_PATH), "--summary-only"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(json.loads(summary.stdout), self.result.summary)
        boundary = self.result.summary["discovery_boundary"]
        self.assertIs(boundary["archive_population_is_not_oeis_complete"], True)
        self.assertIs(boundary["scan_complete_within_pinned_archive_and_fields"], True)
        self.assertIs(
            self.result.summary["status_boundary"][
                "candidate_asset_grants_strict_conjecture_credit"
            ],
            False,
        )


if __name__ == "__main__":
    unittest.main()
