#!/usr/bin/env python3
"""Independent checker for supplemental review ranks 1--59."""

from __future__ import annotations

import hashlib
import json
import tarfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
QUEUE = ROOT / "Docs/catalog/v5/curation/Frontier_Theorem_Supplemental_Candidate_Queue_v5_5.json"
PRIMARY = ROOT / "Docs/catalog/v5/curation/Frontier_Theorem_Candidate_Queue_v5_5.json"
RELEASE = ROOT / "Docs/catalog/v5/releases/5.4/Claim_Catalog.json"
SOURCE = ROOT / "Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz"
LEDGER = ROOT / "Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5/nonerdos_supplemental_001_059.jsonl"
SUMMARY = ROOT / "Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5/nonerdos_supplemental_001_059_summary.json"
QUEUE_SHA = "78c2d8e1e4068d59bf0471ecca9071fc139bb3300525df0aab8348718cbdc135"
QUEUE_AUTHORITY = "d382e4c9b6851150257fea50ab597051b6258085a24b04d43e517a81094c547c"
PRIMARY_SHA = "b3b28b81cfcd9fe4dbf002d2bb8d9bedaa8094656396e224abb5c6221530b2fc"
RELEASE_SHA = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
SOURCE_SHA = "51535f4755574d97672515a75b8b076065aba2c0d79631e99fa57719f484dcc8"
LICENSE_SHA = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
ELIGIBLE = {255, 256, 258, 259, 260, 261, 262, 263, 264, 265, 267, 268, 269, 272, 273, 274, 275, 284, 286, 289, 299, 306, 308, 309}
PENDING = {266, 276, 293, 295, 296, 311}
REJECT = set(range(255, 314)) - ELIGIBLE - PENDING


def cb(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def without(value: dict, key: str) -> dict:
    return {name: item for name, item in value.items() if name != key}


def safe(value: str) -> Path:
    path = Path(value)
    assert not path.is_absolute() and ".." not in path.parts
    resolved = (ROOT / path).resolve()
    assert resolved.is_relative_to(ROOT.resolve())
    return resolved


def main() -> None:
    assert ELIGIBLE | PENDING | REJECT == set(range(255, 314))
    assert not (ELIGIBLE & PENDING or ELIGIBLE & REJECT or PENDING & REJECT)
    assert sha(QUEUE.read_bytes()) == QUEUE_SHA and sha(PRIMARY.read_bytes()) == PRIMARY_SHA
    assert sha(RELEASE.read_bytes()) == RELEASE_SHA and sha(SOURCE.read_bytes()) == SOURCE_SHA
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert queue["authority_sha256"] == QUEUE_AUTHORITY
    candidates = [row for row in queue["records"] if 1 <= row["supplemental_rank"] <= 59]
    candidate_by_rank = {row["candidate_rank"]: row for row in candidates}
    release_by_stage = {row["stage_claim_id"]: row for row in release["records"]}
    assert [row["supplemental_rank"] for row in candidates] == list(range(1, 60))
    assert [row["candidate_rank"] for row in candidates] == list(range(255, 314))
    assert summary["rank_range"] == {"supplemental_first": 1, "supplemental_last": 59, "candidate_first": 255, "candidate_last": 313, "inclusive": True, "expected_rows": 59}
    assert summary["inputs"]["supplemental_queue_sha256"] == QUEUE_SHA
    assert summary["inputs"]["supplemental_queue_authority_sha256"] == QUEUE_AUTHORITY
    assert summary["inputs"]["primary_queue_sha256"] == PRIMARY_SHA
    assert summary["inputs"]["release_5_4_claim_catalog_sha256"] == RELEASE_SHA
    assert summary["inputs"]["source_archive_sha256"] == SOURCE_SHA
    assert summary["inputs"]["source_license_sha256"] == LICENSE_SHA
    for section, keys in (("inputs", ("supplemental_queue_path", "primary_queue_path", "release_5_4_claim_catalog_path", "source_archive_path")), ("output", ("ledger_path",))):
        for key in keys:
            safe(summary[section][key])
    for path_key, hash_key in (("builder_path", "builder_sha256"), ("checker_path", "checker_sha256")):
        artifact = safe(summary["validation"][path_key])
        assert sha(artifact.read_bytes()) == summary["validation"][hash_key]
    ledger_data = LEDGER.read_bytes()
    rows = [json.loads(line) for line in ledger_data.splitlines()]
    assert ledger_data.endswith(b"\n") and len(rows) == 59
    assert [row["candidate_rank"] for row in rows] == list(range(255, 314))
    assert [row["supplemental_rank"] for row in rows] == list(range(1, 60))
    archive_prefix = "formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669/"
    with tarfile.open(SOURCE, "r:gz") as tf:
        assert sha(tf.extractfile(archive_prefix + "LICENSE").read()) == LICENSE_SHA
        for candidate in candidates:
            assert sha(cb(without(candidate, "row_sha256"))) == candidate["row_sha256"]
            data = tf.extractfile(archive_prefix + candidate["source_member_path"]).read()
            assert sha(data) == candidate["source_locator"]["file_sha256"]
            assert b"Licensed under the Apache License, Version 2.0" in data[:800]
    gate_names = {"complete_proved_statement", "primary_reference", "scope_match", "current_proved_status", "frontier_or_documented_resolution", "rights", "semantic_dedupe"}
    ref_names = {"kind", "identifier", "url", "title", "version", "published_at", "updated_at", "artifact_path", "artifact_sha256", "verification"}
    for row in rows:
        rank = row["candidate_rank"]
        candidate = candidate_by_rank[rank]
        parent = release_by_stage[row["stage_claim_id"]]
        assert row["schema_version"] == "awesome-theorems/frontier-theorem-human-review/5.5"
        for key in ("candidate_rank", "supplemental_rank", "stage_claim_id", "variant_id", "family_id", "display_name", "semantic_key"):
            assert row[key] == candidate[key]
        assert row["queue_row_sha256"] == candidate["row_sha256"]
        assert parent["formal_type_sha256"] == candidate["formal_type_sha256"]
        expected = "eligible_existing_frontier_credit" if rank in ELIGIBLE else "pending" if rank in PENDING else "reject"
        assert row["decision"] == expected
        assert set(row["gates"]) == gate_names
        assert all(type(value["pass"]) is bool and value["evidence"] for value in row["gates"].values())
        all_pass = all(value["pass"] for value in row["gates"].values())
        assert all_pass == (rank in ELIGIBLE)
        assert row["review_eligible_frontier_credit"] is all_pass
        assert row["grants_frontier_credit"] is False and row["grants_new_theorem_credit"] is False
        assert (row["frontier_credit_key"] is not None) == all_pass
        if all_pass:
            assert row["primary_references"] and row["reason_codes"][0] == "all_review_gates_pass"
        for reference in row["primary_references"]:
            assert set(reference) == ref_names and reference["identifier"] and reference["url"] and reference["title"] and reference["verification"]
        assert sha(cb(without(row, "row_sha256"))) == row["row_sha256"]
    counts = Counter(row["decision"] for row in rows)
    keys = [row["frontier_credit_key"] for row in rows if row["frontier_credit_key"]]
    assert len(keys) == len(set(keys))
    assert summary["counts"] == {"eligible_existing_frontier_credit": counts["eligible_existing_frontier_credit"], "pending": counts["pending"], "reject": counts["reject"], "review_rows": 59, "review_eligible_frontier_keys": len(keys), "formal_release_frontier_credits_granted": 0, "new_theorem_credits_granted": 0}
    assert summary["output"]["ledger_rows"] == 59 and summary["output"]["ledger_bytes"] == len(ledger_data) and summary["output"]["ledger_sha256"] == sha(ledger_data)
    expected_digests = {
        "ordered_queue_row_sha256_chain": sha(cb([row["queue_row_sha256"] for row in rows])),
        "ordered_review_row_sha256_chain": sha(cb([row["row_sha256"] for row in rows])),
        "semantic_key_set_sha256": sha(cb(sorted({row["semantic_key"] for row in rows}))),
        "frontier_credit_key_set_sha256": sha(cb(sorted(keys))),
        "eligible_candidate_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "eligible_existing_frontier_credit"))),
        "pending_candidate_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "pending"))),
        "reject_candidate_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "reject"))),
    }
    assert summary["set_digests"] == expected_digests
    assert summary["invariants"]["formal_release_modified"] is False
    assert summary["invariants"]["all_rows_grant_frontier_credit_false"] is True
    assert summary["invariants"]["all_rows_grant_new_theorem_credit_false"] is True
    assert sha(cb(without(summary, "authority_sha256"))) == summary["authority_sha256"]
    print(f"PASS supplemental review 001-059 rows=59 eligible={counts['eligible_existing_frontier_credit']} pending={counts['pending']} reject={counts['reject']} authority={summary['authority_sha256']}")


if __name__ == "__main__":
    main()
