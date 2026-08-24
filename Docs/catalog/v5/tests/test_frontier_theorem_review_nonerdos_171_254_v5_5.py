#!/usr/bin/env python3
"""Black-box and adversarial tests for the 171--254 review checker."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHECKER_REL = Path("Docs/catalog/v5/tools/check_frontier_theorem_review_nonerdos_171_254_v5_5.py")
BUILDER_REL = Path("Docs/catalog/v5/tools/build_frontier_theorem_review_nonerdos_171_254_v5_5.py")
TEST_REL = Path("Docs/catalog/v5/tests/test_frontier_theorem_review_nonerdos_171_254_v5_5.py")
QUEUE_REL = Path("Docs/catalog/v5/curation/Frontier_Theorem_Candidate_Queue_v5_5.json")
RELEASE_REL = Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json")
SOURCE_REL = Path("Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz")
LEDGER_REL = Path("Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5/nonerdos_171_254.jsonl")
SUMMARY_REL = Path("Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5/nonerdos_171_254_summary.json")


def cb(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_checker(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(root / CHECKER_REL)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def make_mirror(root: Path) -> None:
    immutable = (CHECKER_REL, BUILDER_REL, TEST_REL, QUEUE_REL, RELEASE_REL, SOURCE_REL)
    mutable = (LEDGER_REL, SUMMARY_REL)
    for rel in immutable + mutable:
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if rel in immutable:
            os.link(ROOT / rel, target)
        else:
            shutil.copy2(ROOT / rel, target)


def reseal_summary(root: Path, rows: list[dict]) -> None:
    ledger_bytes = b"".join(cb(row) + b"\n" for row in rows)
    (root / LEDGER_REL).write_bytes(ledger_bytes)
    summary = json.loads((root / SUMMARY_REL).read_text(encoding="utf-8"))
    decisions = {name: sum(row["decision"] == name for row in rows) for name in ("eligible_existing_frontier_credit", "pending", "reject")}
    keys = sorted(row["frontier_credit_key"] for row in rows if row["frontier_credit_key"])
    summary["output"].update({"ledger_sha256": sha(ledger_bytes), "ledger_bytes": len(ledger_bytes), "ledger_rows": len(rows)})
    summary["counts"].update(decisions)
    summary["counts"]["review_eligible_frontier_keys"] = len(keys)
    summary["set_digests"] = {
        "ordered_queue_row_sha256_chain": sha(cb([row["queue_row_sha256"] for row in rows])),
        "ordered_review_row_sha256_chain": sha(cb([row["row_sha256"] for row in rows])),
        "semantic_key_set_sha256": sha(cb(sorted({row["semantic_key"] for row in rows}))),
        "frontier_credit_key_set_sha256": sha(cb(keys)),
        "eligible_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "eligible_existing_frontier_credit"))),
        "pending_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "pending"))),
        "reject_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "reject"))),
    }
    summary.pop("authority_sha256", None)
    summary["authority_sha256"] = sha(cb(summary))
    (root / SUMMARY_REL).write_bytes(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n")


def test_pristine_checker_passes() -> None:
    result = run_checker(ROOT)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS frontier nonerdos 171-254 rows=84 eligible=50 pending=14 reject=20" in result.stdout


def test_outer_resealed_wrong_credit_escalation_is_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="frontier-review-171-254-") as directory:
        mirror = Path(directory)
        make_mirror(mirror)
        rows = [json.loads(line) for line in (mirror / LEDGER_REL).read_text(encoding="utf-8").splitlines()]
        row = next(item for item in rows if item["candidate_rank"] == 173)
        for value in row["gates"].values():
            value["pass"] = True
        row["decision"] = "eligible_existing_frontier_credit"
        row["reason_codes"] = ["all_review_gates_pass"]
        row["grants_frontier_credit"] = True
        row["frontier_credit_key"] = "frontier-resolution-sha256/" + "0" * 64
        row.pop("row_sha256")
        row["row_sha256"] = sha(cb(row))
        reseal_summary(mirror, rows)
        result = run_checker(mirror)
        assert result.returncode != 0


if __name__ == "__main__":
    test_pristine_checker_passes()
    test_outer_resealed_wrong_credit_escalation_is_rejected()
    print("PASS tests frontier nonerdos 171-254")
