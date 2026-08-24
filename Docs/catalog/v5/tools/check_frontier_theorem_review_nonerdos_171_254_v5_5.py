#!/usr/bin/env python3
"""Independent read-only checker for non-Erdos frontier ranks 171--254."""

from __future__ import annotations

import hashlib
import json
import tarfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
QUEUE = ROOT / "Docs/catalog/v5/curation/Frontier_Theorem_Candidate_Queue_v5_5.json"
RELEASE = ROOT / "Docs/catalog/v5/releases/5.4/Claim_Catalog.json"
LEDGER = ROOT / "Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5/nonerdos_171_254.jsonl"
SUMMARY = ROOT / "Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5/nonerdos_171_254_summary.json"
SOURCE = ROOT / "Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz"
FIRST = 171
LAST = 254
QUEUE_SHA = "b3b28b81cfcd9fe4dbf002d2bb8d9bedaa8094656396e224abb5c6221530b2fc"
QUEUE_AUTHORITY = "375ca73546293f74fdc966209d4be0d184ad5e28273c70aecc7a12a601548133"
RELEASE_SHA = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
SOURCE_SHA = "51535f4755574d97672515a75b8b076065aba2c0d79631e99fa57719f484dcc8"
LICENSE_SHA = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
ELIGIBLE_RANKS = {
    171, 172, 177, 179, 180, 182, 183, 184, 185, 186, 187, 188, 190, 191,
    192, 193, 195, 197, 198, 201, 202, 204, 205, 206, 207, 214, 215, 216,
    217, 218, 220, 221, 222, 224, 225, 227, 228, 229, 231, 232, 234, 236,
    238, 241, 242, 247, 249, 250, 251, 253,
}
PENDING_RANKS = {175, 181, 196, 208, 210, 211, 212, 219, 226, 233, 243, 244, 246, 248}
REJECT_RANKS = set(range(FIRST, LAST + 1)) - ELIGIBLE_RANKS - PENDING_RANKS
EXPECTED_FALSE_GATES = {
    173: {"complete_proved_statement", "scope_match"},
    174: {"scope_match", "current_proved_status"},
    176: {"frontier_or_documented_resolution"},
    178: {"complete_proved_statement", "scope_match", "current_proved_status"},
    189: {"primary_reference", "frontier_or_documented_resolution"},
    194: {"frontier_or_documented_resolution"},
    199: {"semantic_dedupe"},
    200: {"frontier_or_documented_resolution"},
    203: {"frontier_or_documented_resolution"},
    209: {"primary_reference", "frontier_or_documented_resolution"},
    213: {"primary_reference", "frontier_or_documented_resolution"},
    223: {"primary_reference", "frontier_or_documented_resolution"},
    230: {"frontier_or_documented_resolution"},
    235: {"primary_reference", "frontier_or_documented_resolution"},
    237: {"scope_match", "current_proved_status"},
    239: {"scope_match", "current_proved_status"},
    240: {"scope_match", "current_proved_status"},
    245: {"primary_reference", "frontier_or_documented_resolution"},
    252: {"semantic_dedupe"},
    254: {"complete_proved_statement", "scope_match", "semantic_dedupe"},
}


def cb(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def without(obj: dict, key: str) -> dict:
    return {k: v for k, v in obj.items() if k != key}


def safe_repo_path(value: str) -> Path:
    path = Path(value)
    assert not path.is_absolute() and ".." not in path.parts
    resolved = (ROOT / path).resolve()
    assert resolved.is_relative_to(ROOT.resolve())
    return resolved


def main() -> None:
    queue_bytes = QUEUE.read_bytes()
    release_bytes = RELEASE.read_bytes()
    ledger_bytes = LEDGER.read_bytes()
    summary_bytes = SUMMARY.read_bytes()
    summary = json.loads(summary_bytes)
    assert sha(queue_bytes) == summary["inputs"]["queue_sha256"] == QUEUE_SHA
    assert sha(release_bytes) == summary["inputs"]["release_5_4_claim_catalog_sha256"] == RELEASE_SHA
    assert sha(SOURCE.read_bytes()) == summary["inputs"]["source_archive_sha256"] == SOURCE_SHA
    assert summary["inputs"]["source_license_sha256"] == LICENSE_SHA
    queue = json.loads(queue_bytes)
    assert queue["authority_sha256"] == summary["inputs"]["queue_authority_sha256"] == QUEUE_AUTHORITY
    assert summary["rank_range"] == {"first": FIRST, "last": LAST, "inclusive": True, "expected_rows": LAST - FIRST + 1}
    for key in ("queue_path", "release_5_4_claim_catalog_path", "source_archive_path"):
        safe_repo_path(summary["inputs"][key])
    for key in ("ledger_path",):
        safe_repo_path(summary["output"][key])
    for path_key, hash_key in (("builder_path", "builder_sha256"), ("checker_path", "checker_sha256"), ("test_path", "test_sha256")):
        artifact = safe_repo_path(summary["validation"][path_key])
        assert sha(artifact.read_bytes()) == summary["validation"][hash_key]
    lines = ledger_bytes.splitlines()
    assert ledger_bytes.endswith(b"\n") and len(lines) == LAST - FIRST + 1
    rows = [json.loads(line) for line in lines]
    assert [r["candidate_rank"] for r in rows] == list(range(FIRST, LAST + 1))
    candidates = {r["candidate_rank"]: r for r in queue["records"] if FIRST <= r["candidate_rank"] <= LAST}
    archive_prefix = "formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669/"
    with tarfile.open(SOURCE, "r:gz") as tf:
        license_data = tf.extractfile(archive_prefix + "LICENSE").read()
        assert sha(license_data) == LICENSE_SHA
        for candidate in candidates.values():
            queue_payload = without(candidate, "row_sha256")
            assert sha(cb(queue_payload)) == candidate["row_sha256"]
            member_data = tf.extractfile(archive_prefix + candidate["source_member_path"]).read()
            assert sha(member_data) == candidate["source_locator"]["file_sha256"]
            assert b"Licensed under the Apache License, Version 2.0" in member_data[:800]
    allowed_decisions = {"eligible_existing_frontier_credit", "pending", "reject"}
    expected_gate_names = {
        "complete_proved_statement", "primary_reference", "scope_match",
        "current_proved_status", "frontier_or_documented_resolution", "rights",
        "semantic_dedupe",
    }
    for row in rows:
        rank = row["candidate_rank"]
        candidate = candidates[rank]
        assert row["schema_version"] == "awesome-theorems/frontier-theorem-human-review/5.5"
        assert row["decision"] in allowed_decisions
        assert row["stage_claim_id"] == candidate["stage_claim_id"]
        assert row["variant_id"] == candidate["variant_id"]
        assert row["family_id"] == candidate["family_id"]
        assert row["display_name"] == candidate["display_name"]
        assert row["queue_row_sha256"] == candidate["row_sha256"]
        assert row["semantic_key"] == candidate["semantic_key"]
        assert set(row["gates"]) == expected_gate_names
        assert all(type(g["pass"]) is bool and isinstance(g["evidence"], list) and g["evidence"] for g in row["gates"].values())
        all_pass = all(g["pass"] for g in row["gates"].values())
        expected_decision = (
            "eligible_existing_frontier_credit" if rank in ELIGIBLE_RANKS
            else "pending" if rank in PENDING_RANKS else "reject"
        )
        assert row["decision"] == expected_decision
        false_gates = {name for name, value in row["gates"].items() if not value["pass"]}
        if rank in ELIGIBLE_RANKS:
            assert not false_gates and row["reason_codes"] == ["all_review_gates_pass"]
        elif rank in PENDING_RANKS:
            assert false_gates == {"primary_reference", "scope_match", "current_proved_status", "frontier_or_documented_resolution"}
            assert row["reason_codes"] == ["insufficient_independent_primary_evidence"]
        else:
            assert false_gates == EXPECTED_FALSE_GATES[rank]
        assert (row["decision"] == "eligible_existing_frontier_credit") == all_pass
        assert row["grants_frontier_credit"] is all_pass
        assert row["grants_new_theorem_credit"] is False
        assert (row["frontier_credit_key"] is not None) == all_pass
        assert sha(cb(without(row, "row_sha256"))) == row["row_sha256"]
        for primary in row["primary_references"]:
            assert set(primary) == {"kind", "identifier", "url", "title", "version", "published_at", "updated_at", "artifact_path", "artifact_sha256", "verification"}
            assert primary["identifier"] and primary["url"] and primary["title"] and primary["verification"]
    keys = [r["frontier_credit_key"] for r in rows if r["frontier_credit_key"]]
    assert len(keys) == len(set(keys))
    counts = Counter(r["decision"] for r in rows)
    assert summary["counts"]["eligible_existing_frontier_credit"] == counts["eligible_existing_frontier_credit"]
    assert summary["counts"]["pending"] == counts["pending"]
    assert summary["counts"]["reject"] == counts["reject"]
    assert summary["counts"]["review_rows"] == len(rows)
    assert summary["counts"]["formal_release_frontier_credits_granted"] == 0
    assert summary["counts"]["new_theorem_credits_granted"] == 0
    assert sha(ledger_bytes) == summary["output"]["ledger_sha256"]
    assert len(ledger_bytes) == summary["output"]["ledger_bytes"]
    expected_digests = {
        "ordered_queue_row_sha256_chain": sha(cb([r["queue_row_sha256"] for r in rows])),
        "ordered_review_row_sha256_chain": sha(cb([r["row_sha256"] for r in rows])),
        "semantic_key_set_sha256": sha(cb(sorted({r["semantic_key"] for r in rows}))),
        "frontier_credit_key_set_sha256": sha(cb(sorted(keys))),
        "eligible_rank_set_sha256": sha(cb(sorted(r["candidate_rank"] for r in rows if r["decision"] == "eligible_existing_frontier_credit"))),
        "pending_rank_set_sha256": sha(cb(sorted(r["candidate_rank"] for r in rows if r["decision"] == "pending"))),
        "reject_rank_set_sha256": sha(cb(sorted(r["candidate_rank"] for r in rows if r["decision"] == "reject"))),
    }
    assert summary["set_digests"] == expected_digests
    assert summary["invariants"]["formal_release_modified"] is False
    assert summary["invariants"]["review_alone_grants_release_credit"] is False
    assert summary["validation"]["status"] == "checker_bound; independent read-only checker required and run after generation"
    assert sha(cb(without(summary, "authority_sha256"))) == summary["authority_sha256"]
    print(f"PASS frontier nonerdos 171-254 rows={len(rows)} eligible={counts['eligible_existing_frontier_credit']} pending={counts['pending']} reject={counts['reject']} authority={summary['authority_sha256']}")


if __name__ == "__main__":
    main()
