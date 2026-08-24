#!/usr/bin/env python3
"""Black-box and structural tests for the frozen PutnamBench source universe."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile
import unittest
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[4]
TOOL_REL = Path("Docs/catalog/v5/tools/freeze_putnambench_source_v5_6.py")
OUTPUT_DIR_REL = Path("Docs/catalog/v5/curation/putnambench_v5_6")
INVENTORY_REL = OUTPUT_DIR_REL / "PutnamBench_Source_Inventory_v5_6.json"
PROBLEMS_REL = OUTPUT_DIR_REL / "PutnamBench_Source_Problems_v5_6.jsonl"
VARIANTS_REL = OUTPUT_DIR_REL / "PutnamBench_Formal_Variants_v5_6.jsonl"
FORMAL_ASSET_REL = OUTPUT_DIR_REL / "PutnamBench_Formal_Declaration_Asset_v5_6.jsonl"
FORBIDDEN_ARCHIVE_RELS = (
    Path("Docs/catalog/v5/sources/putnambench-dfb0a47a-source.tar.gz"),
    Path("Docs/catalog/v5/sources/putnambench-dfb0a47-source.tar.gz"),
)
ARCHIVE = Path("/tmp/at-benchmark-review/tars/putnam.tar.gz")
ARCHIVE_SHA256 = "843911c7eb432c0ce96ac1e6494f9675336a9be935884cd5b6de4575db042c30"
EXPECTED_AUTHORITY = "2cc7b0be42fb242a750d3eda12e1437fb7486c26a55bfef01ed76e32e1d31049"
EXPECTED_OUTPUT_SHA256 = {
    INVENTORY_REL: "f8407e1aefe39daea09bfa4f940533130139e2e6c65a2eff3e0688d68013ff95",
    PROBLEMS_REL: "85727d9216226b14be5bc52a2a7cf8aad11d3834ca10192acb4df1331631889d",
    VARIANTS_REL: "aae67f4250a7ff9132487b4a1af494697d7add32b9608dd44766fe516deb6dc4",
    FORMAL_ASSET_REL: "6431c652a888bf2dce1f9eb91692cc79f8bf986e613bc5658a43f5f770e7b563",
}
EXPECTED_MISMATCHES = {
    ("isabelle", "putnam_1980_b3", "putnam_1980_a3"),
    ("coq", "putnam_1968_a1", "putnam_1968_b1"),
    ("coq", "putnam_1970_b5", "putnam_1970_b5_solution"),
    ("coq", "putnam_1979_a6", "putnam_1979_b6"),
    ("coq", "putnam_1994_b3", "putnam_1993_b3"),
}


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def git_blob_sha1(payload: bytes) -> str:
    header = b"blob " + str(len(payload)).encode("ascii") + b"\0"
    return hashlib.sha1(header + payload).hexdigest()  # noqa: S324 - verifies Git identity.


def bound_bytes(payload: bytes, source_span: Mapping[str, int]) -> bytes:
    return payload[source_span["start_byte"] : source_span["end_byte_exclusive"]]


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    ignored = set(fields)
    return digest(canonical({key: item for key, item in value.items() if key not in ignored}))


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AssertionError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def reject_json_constant(value: str) -> Any:
    raise AssertionError(f"non-finite JSON number: {value}")


def strict_json_loads(payload: bytes) -> Any:
    return json.loads(
        payload.decode("utf-8", errors="strict"),
        object_pairs_hook=strict_object,
        parse_constant=reject_json_constant,
    )


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_bytes().splitlines(), start=1):
        value = strict_json_loads(line)
        if not isinstance(value, dict):
            raise AssertionError(f"non-object JSONL row at {path}:{line_number}")
        rows.append(value)
    return rows


def nested_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from nested_keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from nested_keys(item)


def nested_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from nested_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from nested_strings(item)


def independently_locate_formal(
    payload: bytes,
    language: str,
) -> tuple[str, tuple[int, int], tuple[int, int] | None, list[tuple[int, int]], tuple[int, int]]:
    declaration_patterns = {
        "lean4": re.compile(
            rb"(?m)^[ \t]*(?:(?:private|protected)[ \t]+)?"
            rb"(?P<kind>theorem|lemma)[ \t]+(?P<name>[A-Za-z_][A-Za-z0-9_']*)\b"
        ),
        "isabelle": re.compile(
            rb"(?m)^[ \t]*(?P<kind>theorem|lemma)[ \t]+"
            rb"(?P<name>[A-Za-z_][A-Za-z0-9_']*)[ \t]*:"
        ),
        "coq": re.compile(
            rb"(?mi)^[ \t]*(?P<kind>Theorem|Lemma|Proposition|Corollary|Fact|Remark)[ \t]+"
            rb"(?P<name>[A-Za-z_][A-Za-z0-9_']*)\b"
        ),
    }
    hole_patterns = {
        "lean4": re.compile(rb"\bsorry\b"),
        "isabelle": re.compile(rb"\bsorry\b"),
        "coq": re.compile(rb"\bAdmitted\s*\.", re.IGNORECASE),
    }
    declarations = list(declaration_patterns[language].finditer(payload))
    if len(declarations) != 1:
        raise AssertionError(f"independent declaration count drifted: {language}/{len(declarations)}")
    declaration = declarations[0]
    declaration_start = declaration.start("kind")
    holes = list(hole_patterns[language].finditer(payload))
    principal = [hole for hole in holes if hole.start() > declaration_start]
    if len(principal) != 1:
        raise AssertionError(f"independent principal-hole count drifted: {language}/{len(principal)}")
    principal_hole = principal[0]
    if language == "lean4":
        delimiters = list(re.finditer(rb":=", payload[declaration_start : principal_hole.start()]))
        if not delimiters:
            raise AssertionError("independent Lean delimiter missing")
        header_end = declaration_start + delimiters[-1].start()
        introducer = (header_end, principal_hole.start())
        if re.fullmatch(rb":=[ \t\r\n]*(?:by[ \t\r\n]*)?", payload[slice(*introducer)]) is None:
            raise AssertionError("independent Lean introducer drifted")
    elif language == "isabelle":
        header_end = principal_hole.start()
        introducer = None
    else:
        proofs = list(re.finditer(rb"\bProof\s*\.", payload[declaration_start : principal_hole.start()], re.IGNORECASE))
        if len(proofs) != 1:
            raise AssertionError(f"independent Coq Proof count drifted: {len(proofs)}")
        header_end = declaration_start + proofs[0].start()
        introducer = (header_end, principal_hole.start())
    return (
        declaration.group("name").decode("ascii"),
        (declaration_start, header_end),
        introducer,
        [(hole.start(), hole.end()) for hole in holes],
        (declaration_start, principal_hole.end()),
    )


class PutnamBenchSourceFreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = strict_json_loads((ROOT / INVENTORY_REL).read_bytes())
        cls.problems = load_jsonl(ROOT / PROBLEMS_REL)
        cls.variants = load_jsonl(ROOT / VARIANTS_REL)
        cls.formal_assets = load_jsonl(ROOT / FORMAL_ASSET_REL)

    def test_frozen_file_digests_and_authority(self) -> None:
        for relative in FORBIDDEN_ARCHIVE_RELS:
            self.assertFalse((ROOT / relative).exists(), relative.as_posix())
        for relative, expected in EXPECTED_OUTPUT_SHA256.items():
            self.assertEqual(digest((ROOT / relative).read_bytes()), expected, relative.as_posix())
        self.assertEqual(self.inventory["authority_sha256"], EXPECTED_AUTHORITY)
        self.assertEqual(
            self.inventory["authority_sha256"],
            hash_without(self.inventory, "authority_sha256"),
        )

    def test_exact_denominators_and_component_union(self) -> None:
        counts = self.inventory["counts"]
        self.assertEqual(len(self.problems), 675)
        self.assertEqual(len(self.variants), 1_724)
        self.assertEqual(len(self.formal_assets), 1_724)
        self.assertEqual(counts["informal_records"], 673)
        self.assertEqual(counts["formal_problem_key_union"], 674)
        self.assertEqual(counts["formal_variants_by_language"], {"lean4": 672, "isabelle": 640, "coq": 412})
        self.assertEqual(counts["proof_holes_by_language"], {"lean4": 1_018, "isabelle": 641, "coq": 412})
        self.assertEqual(
            self.inventory["known_anomalies"]["informal_only_problem_keys"],
            ["putnam_1997_a1"],
        )
        self.assertEqual(
            self.inventory["known_anomalies"]["formal_only_problem_keys"],
            ["putnam_1987_a3", "putnam_1996_a1"],
        )
        problem_keys = {row["problem_key"] for row in self.problems}
        formal_keys = {row["problem_key"] for row in self.variants}
        informal_keys = {row["problem_key"] for row in self.problems if row["informal_binding"] is not None}
        self.assertEqual(len(problem_keys), 675)
        self.assertEqual(len(formal_keys), 674)
        self.assertEqual(len(informal_keys), 673)
        self.assertEqual(informal_keys - formal_keys, {"putnam_1997_a1"})
        self.assertEqual(formal_keys - informal_keys, {"putnam_1987_a3", "putnam_1996_a1"})

    def test_every_row_is_sealed_and_informal_prose_is_not_embedded(self) -> None:
        forbidden_keys = {
            "informal_statement",
            "informal_solution",
            "statement_text",
            "solution_text",
            "exact_statement",
            "exact_solution",
        }
        for row in [*self.problems, *self.variants, *self.formal_assets]:
            self.assertEqual(row["row_sha256"], hash_without(row, "row_sha256"))
            self.assertFalse(forbidden_keys & set(nested_keys(row)))
        informal_rows = [row for row in self.problems if row["informal_binding"] is not None]
        self.assertEqual(len(informal_rows), 673)
        for row in informal_rows:
            binding = row["informal_binding"]
            self.assertFalse(binding["exact_statement_or_solution_text_embedded"])
            self.assertRegex(binding["statement_value_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(binding["solution_value_sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(binding["statement_pointer"].endswith("/informal_statement"))
            self.assertTrue(binding["solution_pointer"].endswith("/informal_solution"))

    def test_declaration_and_proof_hole_bindings_include_known_anomalies(self) -> None:
        mismatches = {
            (
                row["language"],
                row["problem_key"],
                row["principal_declaration"]["declared_name"],
            )
            for row in self.variants
            if not row["principal_declaration"]["name_matches_problem_key"]
        }
        self.assertEqual(mismatches, EXPECTED_MISMATCHES)
        for row in self.variants:
            declaration = row["principal_declaration"]
            principal_holes = [hole for hole in row["proof_holes"] if hole["is_principal_declaration_hole"]]
            self.assertEqual(len(principal_holes), 1)
            self.assertEqual(principal_holes[0]["hole_index"], declaration["principal_hole_index"])
            self.assertLess(
                declaration["header_span"]["start_byte"],
                declaration["header_span"]["end_byte_exclusive"],
            )
            self.assertLessEqual(
                declaration["header_span"]["end_byte_exclusive"],
                principal_holes[0]["span"]["start_byte"],
            )
            self.assertRegex(row["source_binding"]["file_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(declaration["header_sha256"], r"^[0-9a-f]{64}$")

    @unittest.skipUnless(ARCHIVE.is_file(), "operator-supplied pinned PutnamBench tar is not available")
    def test_external_archive_independently_replays_every_pointer_boundary_and_prose_exclusion(self) -> None:
        archive_path = ARCHIVE
        members: dict[str, tuple[bytes, str]] = {}
        with tarfile.open(archive_path, mode="r:gz") as archive:
            for member in archive.getmembers():
                if not member.isfile():
                    continue
                stream = archive.extractfile(member)
                self.assertIsNotNone(stream)
                assert stream is not None
                mode = "100755" if member.mode & 0o111 else "100644"
                members[member.name] = (stream.read(), mode)

        for row in self.problems:
            binding = row["informal_binding"]
            if binding is None:
                continue
            payload, git_mode = members[binding["archive_member_path"]]
            self.assertEqual(digest(payload), binding["file_sha256"])
            self.assertEqual(len(payload), binding["byte_length"])
            self.assertEqual(git_blob_sha1(payload), binding["git_blob_sha1"])
            self.assertEqual(git_mode, binding["git_mode"])
            raw_record = bound_bytes(payload, binding["record_span"])
            self.assertEqual(digest(raw_record), binding["record_raw_sha256"])
            record = strict_json_loads(raw_record)
            self.assertEqual(record["problem_name"], row["problem_key"])
            base_pointer = f"/{binding['record_index']}"
            self.assertEqual(binding["json_pointer"], base_pointer)
            self.assertEqual(binding["problem_name_pointer"], f"{base_pointer}/problem_name")
            self.assertEqual(binding["statement_pointer"], f"{base_pointer}/informal_statement")
            self.assertEqual(binding["solution_pointer"], f"{base_pointer}/informal_solution")
            self.assertEqual(binding["tags_pointer"], f"{base_pointer}/tags")
            self.assertEqual(digest(canonical(record)), binding["record_canonical_sha256"])
            self.assertEqual(digest(canonical(record["problem_name"])), binding["problem_name_value_sha256"])
            self.assertEqual(digest(canonical(record["informal_statement"])), binding["statement_value_sha256"])
            self.assertEqual(digest(canonical(record["informal_solution"])), binding["solution_value_sha256"])
            self.assertEqual(digest(canonical(record["tags"])), binding["tags_value_sha256"])
            self.assertEqual(len(record["tags"]), binding["tag_count"])

        assets_by_id = {row["variant_id"]: row for row in self.formal_assets}
        for row in self.variants:
            source = row["source_binding"]
            payload, git_mode = members[source["archive_member_path"]]
            self.assertEqual(digest(payload), source["file_sha256"])
            self.assertEqual(len(payload), source["byte_length"])
            self.assertEqual(git_blob_sha1(payload), source["git_blob_sha1"])
            self.assertEqual(git_mode, source["git_mode"])
            declaration = row["principal_declaration"]
            independently_declared_name, independent_header, independent_intro, independent_holes, independent_full = (
                independently_locate_formal(payload, row["language"])
            )
            self.assertEqual(independently_declared_name, declaration["declared_name"])
            self.assertEqual(
                independent_header,
                (declaration["header_span"]["start_byte"], declaration["header_span"]["end_byte_exclusive"]),
            )
            if independent_intro is None:
                self.assertIsNone(declaration["proof_introducer_binding"])
            else:
                intro_span = declaration["proof_introducer_binding"]["span"]
                self.assertEqual(independent_intro, (intro_span["start_byte"], intro_span["end_byte_exclusive"]))
            self.assertEqual(
                independent_holes,
                [(hole["span"]["start_byte"], hole["span"]["end_byte_exclusive"]) for hole in row["proof_holes"]],
            )
            self.assertEqual(
                independent_full,
                (
                    declaration["full_declaration_span"]["start_byte"],
                    declaration["full_declaration_span"]["end_byte_exclusive"],
                ),
            )
            header = bound_bytes(payload, declaration["header_span"])
            full_declaration = bound_bytes(payload, declaration["full_declaration_span"])
            self.assertEqual(digest(header), declaration["header_sha256"])
            self.assertEqual(digest(full_declaration), declaration["full_declaration_sha256"])
            self.assertIn(declaration["declared_name"].encode("ascii"), header)
            introducer = declaration["proof_introducer_binding"]
            if introducer is not None:
                self.assertEqual(digest(bound_bytes(payload, introducer["span"])), introducer["sha256"])
            for hole in row["proof_holes"]:
                self.assertEqual(digest(bound_bytes(payload, hole["span"])), hole["token_sha256"])
            principal = row["proof_holes"][declaration["principal_hole_index"]]
            self.assertTrue(principal["is_principal_declaration_hole"])
            self.assertTrue(full_declaration.endswith(bound_bytes(payload, principal["span"])))
            asset = assets_by_id[row["variant_id"]]
            self.assertEqual(asset["declaration_header"]["utf8"].encode("utf-8"), header)
            for asset_hole, source_hole in zip(asset["proof_holes"], row["proof_holes"], strict=True):
                token = bound_bytes(payload, source_hole["span"])
                self.assertEqual(asset_hole["token_utf8"].encode("utf-8"), token)
                self.assertEqual(token, b"Admitted." if row["language"] == "coq" else b"sorry")

        informal_payload = members[
            "PutnamBench-dfb0a47a1c1ec3a10f2a9acfdf41a2043920f33c/informal/putnam.json"
        ][0]
        informal_records = strict_json_loads(informal_payload)
        all_derived_string_values = "\n".join(
            text
            for document in [self.inventory, *self.problems, *self.variants, *self.formal_assets]
            for text in nested_strings(document)
        )
        for record in informal_records:
            self.assertNotIn(record["informal_statement"], all_derived_string_values)
            self.assertNotIn(record["informal_solution"], all_derived_string_values)

    def test_rights_are_scoped_and_do_not_inherit_to_informal_text(self) -> None:
        snapshot = self.inventory["source_snapshot"]
        self.assertFalse(snapshot["archive_embedded_in_repository"])
        self.assertFalse(snapshot["catalog_distributes_full_source_archive"])
        self.assertTrue(snapshot["operator_supplied_external_archive_required_for_full_replay"])
        self.assertEqual(snapshot["archive_sha256"], ARCHIVE_SHA256)
        rights = self.inventory["rights"]
        self.assertEqual(rights["lean4"]["license_expression"], "Apache-2.0")
        self.assertEqual(rights["isabelle"]["license_expression"], "Apache-2.0")
        self.assertEqual(rights["coq"]["license_expression"], "MIT")
        informal = rights["informal"]
        self.assertEqual(informal["license_expression"], "NOASSERTION")
        self.assertEqual(
            informal["informal_statement_permission_status"],
            "upstream_repository_readme_asserts_MAA_permission",
        )
        self.assertEqual(
            informal["informal_solution_permission_status"],
            "not_established_by_the_bound_README_assertion",
        )
        self.assertTrue(informal["permission_assertion_is_not_a_license"])
        self.assertFalse(informal["inherits_lean4_isabelle_or_coq_license"])
        self.assertFalse(informal["repository_root_license_file_present"])
        self.assertFalse(informal["informal_scoped_license_file_present"])
        self.assertFalse(informal["derived_problem_rows_embed_exact_statement_or_solution_text"])
        for language in ("lean4", "isabelle", "coq"):
            self.assertFalse(rights[language]["applies_to_informal_statements"])
            license_binding = rights[language]["license_binding"]
            self.assertEqual(
                digest(license_binding["license_text_utf8"].encode("utf-8")),
                license_binding["file_sha256"],
            )
        variants_by_id = {row["variant_id"]: row for row in self.variants}
        self.assertEqual({row["variant_id"] for row in self.formal_assets}, set(variants_by_id))
        for asset in self.formal_assets:
            variant = variants_by_id[asset["variant_id"]]
            self.assertEqual(asset["external_source_binding"], variant["source_binding"])
            self.assertEqual(asset["rights"]["rights_id"], variant["rights_id"])
            self.assertTrue(all(value is False for value in asset["exclusions"].values()))
            self.assertNotIn("/--", asset["declaration_header"]["utf8"])

    def test_cli_repository_only_check_passes_from_foreign_cwd(self) -> None:
        with tempfile.TemporaryDirectory(prefix="putnambench-foreign-cwd-") as temporary:
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / TOOL_REL),
                    "--check",
                    "--repo-root",
                    str(ROOT),
                ],
                cwd=temporary,
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "problems=675 informal=673 formal_variants=1724 formal_assets=1724 formal_keys=674",
            result.stdout,
        )

    @unittest.skipUnless(ARCHIVE.is_file(), "operator-supplied pinned PutnamBench tar is not available")
    def test_read_only_full_source_audit_passes(self) -> None:
        self.assertEqual(digest(ARCHIVE.read_bytes()), ARCHIVE_SHA256)
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / TOOL_REL),
                "--audit-source-archive",
                str(ARCHIVE),
                "--repo-root",
                str(ROOT),
            ],
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("AUDIT PASS", result.stdout)

    @unittest.skipUnless(ARCHIVE.is_file(), "operator-supplied pinned PutnamBench tar is not available")
    def test_external_archive_digest_mutation_fails_closed_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory(prefix="putnambench-bad-archive-") as temporary:
            bad_archive = Path(temporary) / "mutated.tar.gz"
            mutated = bytearray(ARCHIVE.read_bytes())
            mutated[-1] ^= 1
            bad_archive.write_bytes(mutated)
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / TOOL_REL),
                    "--audit-source-archive",
                    str(bad_archive),
                    "--repo-root",
                    str(ROOT),
                ],
                cwd=temporary,
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("archive SHA-256 drifted", result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_missing_external_archive_audit_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="putnambench-missing-external-") as temporary:
            missing = Path(temporary) / "missing.tar.gz"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / TOOL_REL),
                    "--audit-source-archive",
                    str(missing),
                    "--repo-root",
                    str(ROOT),
                ],
                cwd=temporary,
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("pinned archive is missing", result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_repository_only_check_rejects_accidental_full_archive_distribution(self) -> None:
        with tempfile.TemporaryDirectory(prefix="putnambench-forbidden-archive-") as temporary:
            repository_root = Path(temporary) / "repo"
            forbidden = repository_root / FORBIDDEN_ARCHIVE_RELS[0]
            forbidden.parent.mkdir(parents=True)
            forbidden.write_bytes(b"must not be distributed")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / TOOL_REL),
                    "--check",
                    "--repo-root",
                    str(repository_root),
                ],
                cwd=temporary,
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("full upstream archive must not be distributed", result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    @unittest.skipUnless(ARCHIVE.is_file(), "operator-supplied pinned PutnamBench tar is not available")
    def test_write_from_external_archive_then_repository_only_check_and_audit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="putnambench-external-write-") as temporary:
            repository_root = Path(temporary) / "repo"
            write_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / TOOL_REL),
                    "--write",
                    "--source-archive",
                    str(ARCHIVE),
                    "--repo-root",
                    str(repository_root),
                ],
                cwd=temporary,
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(write_result.returncode, 0, write_result.stdout + write_result.stderr)
            for relative in FORBIDDEN_ARCHIVE_RELS:
                self.assertFalse((repository_root / relative).exists())
            check_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / TOOL_REL),
                    "--check",
                    "--repo-root",
                    str(repository_root),
                ],
                cwd=temporary,
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(check_result.returncode, 0, check_result.stdout + check_result.stderr)
            audit_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / TOOL_REL),
                    "--audit-source-archive",
                    str(ARCHIVE),
                    "--repo-root",
                    str(repository_root),
                ],
                cwd=temporary,
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
        self.assertEqual(audit_result.returncode, 0, audit_result.stdout + audit_result.stderr)


if __name__ == "__main__":
    unittest.main()
