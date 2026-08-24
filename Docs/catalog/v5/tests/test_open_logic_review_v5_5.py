from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[4]
CHECKER = ROOT / "Docs/catalog/v5/tools/check_open_logic_review_v5_5.py"
AUDIT = ROOT / "Docs/catalog/v5/curation/open_logic_v5_5"
SOURCE = ROOT / "Docs/catalog/v5/sources/open-logic-problems-479fe770-source.tar.gz"


class OpenLogicReviewTests(unittest.TestCase):
    def run_checker(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(CHECKER), *arguments],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_pristine_review_replays(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("accepted=4", result.stdout)

    def test_checker_has_no_separate_generator_import(self):
        source = CHECKER.read_text(encoding="utf-8")
        self.assertNotIn("import validate_open_logic_review", source)
        self.assertNotIn("import build_open_logic", source)

    def test_resealed_decision_mutation_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            audit = Path(directory) / "audit"
            shutil.copytree(AUDIT, audit)
            jsonl = audit / "open-logic-review.jsonl"
            rows = [json.loads(line) for line in jsonl.read_text(encoding="utf-8").splitlines()]
            rows[1]["decision"] = "reject"
            rows[1]["grants_strict_conjecture_credit"] = False
            payload = b"".join(
                (json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
                for row in rows
            )
            jsonl.write_bytes(payload)
            digest = hashlib.sha256(payload).hexdigest()
            (audit / "open-logic-review.sha256").write_text(f"{digest}  open-logic-review.jsonl\n", encoding="utf-8")
            counts_path = audit / "open-logic-review.count.json"
            counts = json.loads(counts_path.read_text(encoding="utf-8"))
            counts["artifact_sha256"] = digest
            counts["counts"]["accepted"] -= 1
            counts["counts"]["rejected"] += 1
            counts["counts"]["grants_strict_conjecture_credit"] -= 1
            counts["accepted_problem_ids"].remove(2)
            counts["rejected_problem_ids"].append(2)
            counts["rejected_problem_ids"].sort()
            counts_path.write_text(json.dumps(counts, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
            result = self.run_checker("--audit-dir", str(audit))
            self.assertNotEqual(result.returncode, 0)

    def test_mutated_source_archive_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "source.tar.gz"
            payload = bytearray(SOURCE.read_bytes())
            payload[-1] ^= 1
            archive.write_bytes(payload)
            result = self.run_checker("--source-archive", str(archive))
            self.assertNotEqual(result.returncode, 0)

    def test_missing_parent_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_checker("--workspace", directory)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
