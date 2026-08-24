#!/usr/bin/env python3
"""Independent read-only checker for non-Erdos frontier ranks 86--170."""

from __future__ import annotations

import hashlib
import json
import tarfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
QUEUE = ROOT / "Docs/catalog/v5/curation/Frontier_Theorem_Candidate_Queue_v5_5.json"
RELEASE = ROOT / "Docs/catalog/v5/releases/5.4/Claim_Catalog.json"
SOURCE = ROOT / "Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz"
LEDGER = ROOT / "Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5/nonerdos_086_170.jsonl"
SUMMARY = ROOT / "Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5/nonerdos_086_170.summary.json"
FIRST = 86
LAST = 170
QUEUE_SHA = "b3b28b81cfcd9fe4dbf002d2bb8d9bedaa8094656396e224abb5c6221530b2fc"
QUEUE_AUTHORITY = "375ca73546293f74fdc966209d4be0d184ad5e28273c70aecc7a12a601548133"
RELEASE_SHA = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
SOURCE_SHA = "51535f4755574d97672515a75b8b076065aba2c0d79631e99fa57719f484dcc8"
LICENSE_SHA = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"

ELIGIBLE = {
    87, 88, 90, 91, 92, 93, 95, 96, 99, 101, 102, 103, 104, 106, 108, 111,
    113, 114, 115, 116, 117, 118, 120, 121, 122, 123, 124, 125, 126, 128,
    130, 132, 133, 137, 138, 139, 140, 142, 143, 145, 147, 148, 149,
    151, 153, 155, 158, 161, 162, 164, 165, 166, 167,
}
PENDING = {94, 97, 98, 100, 107, 109, 112, 135, 141, 152, 156, 163}
REJECT = set(range(FIRST, LAST + 1)) - ELIGIBLE - PENDING


def cb(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def without(value: dict, key: str) -> dict:
    return {name: item for name, item in value.items() if name != key}


def safe_path(value: str) -> Path:
    path = Path(value)
    assert not path.is_absolute() and ".." not in path.parts
    resolved = (ROOT / path).resolve()
    assert resolved.is_relative_to(ROOT.resolve())
    return resolved


def main() -> None:
    assert not (ELIGIBLE & PENDING or ELIGIBLE & REJECT or PENDING & REJECT)
    assert ELIGIBLE | PENDING | REJECT == set(range(FIRST, LAST + 1))
    queue_data = QUEUE.read_bytes()
    release_data = RELEASE.read_bytes()
    source_data = SOURCE.read_bytes()
    ledger_data = LEDGER.read_bytes()
    summary = json.loads(SUMMARY.read_bytes())
    assert sha(queue_data) == summary["inputs"]["queue_sha256"] == QUEUE_SHA
    assert sha(release_data) == summary["inputs"]["release_5_4_claim_catalog_sha256"] == RELEASE_SHA
    assert sha(source_data) == summary["inputs"]["source_archive_sha256"] == SOURCE_SHA
    assert summary["inputs"]["source_license_sha256"] == LICENSE_SHA
    queue = json.loads(queue_data)
    release = json.loads(release_data)
    assert queue["authority_sha256"] == summary["inputs"]["queue_authority_sha256"] == QUEUE_AUTHORITY
    assert summary["rank_range"] == {"first": FIRST, "last": LAST, "inclusive": True, "expected_rows": 85}
    for key in ("queue_path", "release_5_4_claim_catalog_path", "source_archive_path"):
        safe_path(summary["inputs"][key])
    assert safe_path(summary["output"]["ledger_path"]) == LEDGER.resolve()
    for path_key, hash_key in (("builder_path", "builder_sha256"), ("checker_path", "checker_sha256")):
        artifact = safe_path(summary["validation"][path_key])
        assert sha(artifact.read_bytes()) == summary["validation"][hash_key]

    lines = ledger_data.splitlines()
    assert ledger_data.endswith(b"\n") and len(lines) == 85
    rows = [json.loads(line) for line in lines]
    assert [row["candidate_rank"] for row in rows] == list(range(FIRST, LAST + 1))
    candidates = {row["candidate_rank"]: row for row in queue["records"] if FIRST <= row["candidate_rank"] <= LAST}
    release_by_stage = {row["stage_claim_id"]: row for row in release["records"]}

    archive_prefix = "formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669/"
    with tarfile.open(SOURCE, "r:gz") as tf:
        assert sha(tf.extractfile(archive_prefix + "LICENSE").read()) == LICENSE_SHA
        for candidate in candidates.values():
            assert sha(cb(without(candidate, "row_sha256"))) == candidate["row_sha256"]
            member = tf.extractfile(archive_prefix + candidate["source_member_path"]).read()
            assert sha(member) == candidate["source_locator"]["file_sha256"]
            assert b"Licensed under the Apache License, Version 2.0" in member[:800]

    gate_names = {
        "complete_proved_statement", "primary_reference", "scope_match",
        "current_proved_status", "frontier_or_documented_resolution", "rights",
        "semantic_dedupe",
    }
    reference_names = {
        "kind", "identifier", "url", "title", "version", "published_at",
        "updated_at", "artifact_path", "artifact_sha256", "verification",
    }
    for row in rows:
        rank = row["candidate_rank"]
        candidate = candidates[rank]
        parent = release_by_stage[row["stage_claim_id"]]
        assert row["schema_version"] == "awesome-theorems/frontier-theorem-human-review/5.5"
        assert row["reviewed_as_of"] == "2026-08-10"
        for key in ("stage_claim_id", "variant_id", "family_id", "display_name", "semantic_key"):
            assert row[key] == candidate[key]
        assert row["queue_row_sha256"] == candidate["row_sha256"]
        assert parent["formal_type_sha256"] == candidate["formal_type_sha256"]
        assert parent["dedupe"]["normalized_statement_sha256"] == candidate["semantic_key"].split("/", 1)[1]
        expected = "eligible_existing_frontier_credit" if rank in ELIGIBLE else "pending" if rank in PENDING else "reject"
        assert row["decision"] == expected
        assert set(row["gates"]) == gate_names
        assert all(type(gate["pass"]) is bool and isinstance(gate["evidence"], list) and gate["evidence"] for gate in row["gates"].values())
        all_pass = all(gate["pass"] for gate in row["gates"].values())
        assert all_pass == (rank in ELIGIBLE)
        assert row["gates"]["rights"]["pass"] is True
        assert row["grants_frontier_credit"] is all_pass
        assert row["grants_new_theorem_credit"] is False
        assert (row["frontier_credit_key"] is not None) == all_pass
        if all_pass:
            assert row["primary_references"] and row["reason_codes"][0] == "all_review_gates_pass"
        else:
            assert any(not gate["pass"] for gate in row["gates"].values())
        for reference in row["primary_references"]:
            assert set(reference) == reference_names
            assert reference["identifier"] and reference["url"] and reference["title"] and reference["verification"]
        assert sha(cb(without(row, "row_sha256"))) == row["row_sha256"]

    keys = [row["frontier_credit_key"] for row in rows if row["frontier_credit_key"]]
    assert len(keys) == len(set(keys))
    counts = Counter(row["decision"] for row in rows)
    assert summary["counts"] == {
        "eligible_existing_frontier_credit": counts["eligible_existing_frontier_credit"],
        "pending": counts["pending"],
        "reject": counts["reject"],
        "review_rows": 85,
        "review_eligible_frontier_keys": len(keys),
        "formal_release_frontier_credits_granted": 0,
        "new_theorem_credits_granted": 0,
    }
    assert summary["output"]["ledger_rows"] == 85
    assert summary["output"]["ledger_bytes"] == len(ledger_data)
    assert summary["output"]["ledger_sha256"] == sha(ledger_data)
    expected_digests = {
        "ordered_queue_row_sha256_chain": sha(cb([row["queue_row_sha256"] for row in rows])),
        "ordered_review_row_sha256_chain": sha(cb([row["row_sha256"] for row in rows])),
        "semantic_key_set_sha256": sha(cb(sorted({row["semantic_key"] for row in rows}))),
        "frontier_credit_key_set_sha256": sha(cb(sorted(keys))),
        "eligible_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "eligible_existing_frontier_credit"))),
        "pending_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "pending"))),
        "reject_rank_set_sha256": sha(cb(sorted(row["candidate_rank"] for row in rows if row["decision"] == "reject"))),
    }
    assert summary["set_digests"] == expected_digests
    assert summary["invariants"]["formal_release_modified"] is False
    assert summary["invariants"]["review_alone_grants_release_credit"] is False
    assert summary["invariants"]["eligible_rows_grant_new_theorem_credit"] is False
    assert summary["cross_batch_findings"]["canonical_stronger_rank"] == 102
    assert summary["cross_batch_findings"]["subsumed_candidate_rank"] == 191
    assert summary["cross_batch_findings"]["shakan_canonical_general_rank"] == 329
    assert summary["cross_batch_findings"]["shakan_subsumed_primary_rank"] == 136
    assert summary["validation"]["status"] == "checker_bound; independent read-only checker required and run after generation"
    assert sha(cb(without(summary, "authority_sha256"))) == summary["authority_sha256"]
    print(f"PASS frontier nonerdos 086-170 rows=85 eligible={counts['eligible_existing_frontier_credit']} pending={counts['pending']} reject={counts['reject']} authority={summary['authority_sha256']}")


if __name__ == "__main__":
    main()
