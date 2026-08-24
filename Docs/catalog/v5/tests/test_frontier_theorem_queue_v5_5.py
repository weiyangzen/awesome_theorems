from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[4]
CHECKER_PATH = ROOT / "Docs/catalog/v5/tools/check_frontier_theorem_queue_v5_5.py"
QUEUE = ROOT / "Docs/catalog/v5/curation/Frontier_Theorem_Candidate_Queue_v5_5.json"
spec = importlib.util.spec_from_file_location("frontier_queue_checker", CHECKER_PATH)
assert spec and spec.loader
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def reseal(document):
    for row in document["records"]:
        row["row_sha256"] = hashlib.sha256(canonical({key: value for key, value in row.items() if key != "row_sha256"})).hexdigest()
    document["set_digests"]["s5_id_set_sha256"] = hashlib.sha256(canonical(sorted(row["stage_claim_id"] for row in document["records"]))).hexdigest()
    document["set_digests"]["semantic_key_set_sha256"] = hashlib.sha256(canonical(sorted(row["semantic_key"] for row in document["records"]))).hexdigest()
    document["set_digests"]["row_sha256_set_sha256"] = hashlib.sha256(canonical(sorted(row["row_sha256"] for row in document["records"]))).hexdigest()
    document["authority_sha256"] = hashlib.sha256(canonical({key: value for key, value in document.items() if key != "authority_sha256"})).hexdigest()


class FrontierTheoremQueueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads(QUEUE.read_text(encoding="utf-8"))

    def mutated_fails(self, document):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "queue.json"
            path.write_bytes(canonical(document) + b"\n")
            with self.assertRaises(checker.CheckError):
                checker.check(path)

    def test_pristine_queue_passes(self):
        self.assertEqual(checker.check(QUEUE)["rows"], 254)

    def test_checker_does_not_import_builder(self):
        self.assertNotIn("build_frontier_theorem_queue_v5_5", CHECKER_PATH.read_text(encoding="utf-8"))

    def test_resealed_frontier_credit_is_rejected(self):
        document = copy.deepcopy(self.document)
        document["records"][0]["review_state"]["grants_frontier_credit"] = True
        document["records"][0]["review_state"]["disposition"] = "accepted"
        document["counts"]["accepted_frontier_credits"] = 1
        reseal(document)
        self.mutated_fails(document)

    def test_resealed_source_binding_is_rejected(self):
        document = copy.deepcopy(self.document)
        document["records"][0]["source_member_path"] = document["records"][1]["source_member_path"]
        reseal(document)
        self.mutated_fails(document)

    def test_resealed_selection_swap_is_rejected(self):
        document = copy.deepcopy(self.document)
        document["records"][0], document["records"][1] = document["records"][1], document["records"][0]
        document["records"][0]["candidate_rank"] = 1
        document["records"][1]["candidate_rank"] = 2
        reseal(document)
        self.mutated_fails(document)


if __name__ == "__main__":
    unittest.main()
