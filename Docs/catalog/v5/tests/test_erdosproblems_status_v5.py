from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[4]
CHECKER_PATH = ROOT / "Docs/catalog/v5/tools/check_erdosproblems_status_v5.py"
SNAPSHOT = ROOT / "Docs/catalog/v5/sources/erdosproblems-status-af90db96.json"
ARCHIVE = ROOT / "Docs/catalog/v5/sources/erdosproblems-af90db96-source.tar.gz"

spec = importlib.util.spec_from_file_location("independent_erdos_status_checker", CHECKER_PATH)
assert spec and spec.loader
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def reseal(document):
    for row in document["records"]:
        row["row_sha256"] = hashlib.sha256(canonical({key: value for key, value in row.items() if key != "row_sha256"})).hexdigest()
    document["set_digests"]["row_sha256_set_sha256"] = hashlib.sha256(canonical(sorted(row["row_sha256"] for row in document["records"]))).hexdigest()
    document["authority_sha256"] = hashlib.sha256(canonical({key: value for key, value in document.items() if key != "authority_sha256"})).hexdigest()


class ErdosProblemsStatusSnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pristine = json.loads(SNAPSHOT.read_text(encoding="utf-8"))

    def check_mutation(self, document):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "snapshot.json"
            path.write_bytes(canonical(document) + b"\n")
            with self.assertRaises(checker.CheckError):
                checker.check(path, ARCHIVE)

    def test_pristine_independent_replay_passes(self):
        result = checker.check(SNAPSHOT, ARCHIVE)
        self.assertEqual(result["records"], 1217)

    def test_checker_does_not_import_generator(self):
        source = CHECKER_PATH.read_text(encoding="utf-8")
        self.assertNotIn("pin_erdosproblems_status_v5", source)

    def test_resealed_status_mutation_is_rejected(self):
        document = copy.deepcopy(self.pristine)
        document["records"][0]["status"]["state"] = "proved"
        reseal(document)
        self.check_mutation(document)

    def test_resealed_credit_boundary_mutation_is_rejected(self):
        document = copy.deepcopy(self.pristine)
        document["evidence_boundary"]["status_metadata_alone_grants_theorem_or_conjecture_credit"] = True
        reseal(document)
        self.check_mutation(document)

    def test_resealed_count_mutation_is_rejected(self):
        document = copy.deepcopy(self.pristine)
        document["counts"]["records"] = 1218
        reseal(document)
        self.check_mutation(document)

    def test_mutated_archive_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "source.tar.gz"
            payload = bytearray(ARCHIVE.read_bytes())
            payload[-1] ^= 1
            archive.write_bytes(payload)
            with self.assertRaises(checker.CheckError):
                checker.check(SNAPSHOT, archive)


if __name__ == "__main__":
    unittest.main()
