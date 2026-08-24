#!/usr/bin/env python3
"""Independent validator for the non-Erdos ranks 1--85 review.

This file intentionally does not import the builder. Expected decisions, source
authorities, canonicalization, source-slice checks, and receipt checks are
implemented independently so replay and mutation tests can detect drift.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tarfile
from collections import Counter
from pathlib import Path
from typing import Any


ALLOWED_DECISIONS = {"eligible_existing_frontier_credit", "pending", "reject"}
EXPECTED_ELIGIBLE = {
    1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    21, 22, 23, 24, 26, 27, 28, 29, 31, 33, 39, 40,
    48, 53, 54, 57, 58, 61, 65, 67, 68, 70, 71, 75,
    78, 80, 81, 84,
}
EXPECTED_REJECT = {19, 34, 55, 59, 62, 64, 69, 73, 74, 77, 79, 82}
EXPECTED_PENDING = set(range(1, 86)) - EXPECTED_ELIGIBLE - EXPECTED_REJECT
EXPECTED_DUPLICATES = {59: 57, 74: 75, 79: 80}

QUEUE_REL = Path("Docs/catalog/v5/curation/Frontier_Theorem_Candidate_Queue_v5_5.json")
PARENT_REL = Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json")
MANIFEST_REL = Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json")
QUEUE_FILE_SHA256 = "b3b28b81cfcd9fe4dbf002d2bb8d9bedaa8094656396e224abb5c6221530b2fc"
QUEUE_AUTHORITY_SHA256 = "375ca73546293f74fdc966209d4be0d184ad5e28273c70aecc7a12a601548133"
PARENT_SHA256 = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
MANIFEST_SHA256 = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
RELEASE_ROOT_SHA256 = "c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813"
SOURCE_COMMIT = "2270d31e8dd611521f979de6d86da364930b7669"
SOURCE_ARCHIVE_SHA256 = "51535f4755574d97672515a75b8b076065aba2c0d79631e99fa57719f484dcc8"
LICENSE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
EXPECTED_JSONL_SHA256 = "a07d59318c6eb150fa475b4c654e0aa811d23d6e3e7fb68d9e7edd24748295f5"
EXPECTED_RECEIPT_AUTHORITY_SHA256 = "89ce6d5713c6a218146a072a21340f8a37d47bc49bc1fabbf1d6003bd237e687"


class ValidationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(1 << 20)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def digest_set(items: list[Any]) -> str:
    return digest_bytes(canonical_bytes(sorted(set(items))))


def expected_decision(rank: int) -> str:
    if rank in EXPECTED_ELIGIBLE:
        return "eligible_existing_frontier_credit"
    if rank in EXPECTED_REJECT:
        return "reject"
    return "pending"


def validate(args: argparse.Namespace) -> dict[str, Any]:
    repo = args.repo_root.resolve()
    review_dir = repo / "Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5"
    source_archive = (args.source_archive or (repo / "Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz")).resolve()
    jsonl_path = (args.jsonl or (review_dir / "nonerdos_001_085.jsonl")).resolve()
    receipt_path = (args.receipt or (review_dir / "nonerdos_001_085_summary.json")).resolve()

    queue_path = repo / QUEUE_REL
    parent_path = repo / PARENT_REL
    manifest_path = repo / MANIFEST_REL
    require(digest_file(queue_path) == QUEUE_FILE_SHA256, "queue file hash mismatch")
    require(digest_file(parent_path) == PARENT_SHA256, "parent catalog hash mismatch")
    require(digest_file(manifest_path) == MANIFEST_SHA256, "parent manifest hash mismatch")
    require(digest_file(source_archive) == SOURCE_ARCHIVE_SHA256, "source archive hash mismatch")

    queue = json.loads(queue_path.read_text(encoding="utf-8"))
    parent = json.loads(parent_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(queue.get("authority_sha256") == QUEUE_AUTHORITY_SHA256, "queue authority literal mismatch")
    queue_without_authority = dict(queue)
    queue_without_authority.pop("authority_sha256", None)
    require(digest_bytes(canonical_bytes(queue_without_authority)) == QUEUE_AUTHORITY_SHA256,
            "queue canonical authority mismatch")
    require(manifest.get("release_root_sha256") == RELEASE_ROOT_SHA256, "release root mismatch")
    require(queue["inputs"]["formal_conjectures_commit"] == SOURCE_COMMIT, "source commit mismatch")
    with tarfile.open(source_archive, "r:gz") as archive:
        source_members = {}
        license_bytes = None
        for member_info in archive.getmembers():
            if not member_info.isfile():
                continue
            member_file = archive.extractfile(member_info)
            require(member_file is not None, f"cannot read source member {member_info.name}")
            data = member_file.read()
            parts = Path(member_info.name).parts
            relative = Path(*parts[1:]).as_posix() if len(parts) > 1 else parts[0]
            source_members[relative] = data
            if relative == "LICENSE":
                license_bytes = data
        require(license_bytes is not None and digest_bytes(license_bytes) == LICENSE_SHA256,
                "source license hash mismatch")

    jsonl_bytes = jsonl_path.read_bytes()
    require(digest_bytes(jsonl_bytes) == EXPECTED_JSONL_SHA256, "review JSONL fixed authority mismatch")
    require(jsonl_bytes.endswith(b"\n"), "JSONL must be LF terminated")
    raw_lines = jsonl_bytes.splitlines()
    require(len(raw_lines) == 85, f"expected 85 JSONL rows, got {len(raw_lines)}")
    rows = [json.loads(line) for line in raw_lines]
    require([r.get("candidate_rank") for r in rows] == list(range(1, 86)), "rank order/coverage mismatch")
    require([r.get("review_index") for r in rows] == list(range(85)), "review index order/coverage mismatch")

    selected_queue = queue["records"][:85]
    require([q["candidate_rank"] for q in selected_queue] == list(range(1, 86)), "queue prefix ranks drifted")
    queue_semantic_counts = Counter(q["semantic_key"] for q in selected_queue)
    parent_normalized_counts = Counter(
        rec.get("dedupe", {}).get("normalized_statement_sha256")
        for rec in parent["records"]
        if rec.get("dedupe", {}).get("normalized_statement_sha256")
    )
    parent_by_variant = {rec["variant_id"]: rec for rec in parent["records"]}

    seen_review_hashes: list[str] = []
    referenced_assets: dict[str, dict[str, Any]] = {}
    decision_counts: Counter[str] = Counter()
    for queue_row, row in zip(selected_queue, rows):
        rank = queue_row["candidate_rank"]
        require(row.get("schema_version") == "awesome-theorems/frontier-existing-credit-review/5.5",
                f"rank {rank}: schema mismatch")
        require(row.get("review_as_of") == "2026-08-10", f"rank {rank}: review date mismatch")
        require(row.get("review_batch") == "nonerdos-001-085", f"rank {rank}: batch mismatch")
        require(row.get("decision") in ALLOWED_DECISIONS, f"rank {rank}: forbidden decision")
        require(row["decision"] == expected_decision(rank), f"rank {rank}: unexpected decision")
        decision_counts[row["decision"]] += 1

        queue_core = dict(queue_row)
        queue_row_hash = queue_core.pop("row_sha256")
        require(digest_bytes(canonical_bytes(queue_core)) == queue_row_hash, f"rank {rank}: queue row hash invalid")
        for key in ("candidate_rank", "stage_claim_id", "variant_id", "family_id", "semantic_key", "display_name"):
            require(row.get(key) == queue_row.get(key), f"rank {rank}: {key} does not match queue")
        require(row.get("source_row_sha256") == queue_row_hash, f"rank {rank}: source row binding mismatch")

        loc = queue_row["source_locator"]
        source_data = source_members[loc["member_path"]]
        require(digest_bytes(source_data) == loc["file_sha256"], f"rank {rank}: source member hash mismatch")
        source_slice = source_data[loc["byte_start"]:loc["byte_end_exclusive"]]
        require(digest_bytes(source_slice) == loc["raw_block_sha256"], f"rank {rank}: source slice hash mismatch")
        binding = row.get("source_slice_binding", {})
        for key in ("member_path", "file_sha256", "byte_start", "byte_end_exclusive", "raw_block_sha256"):
            require(binding.get(key) == loc.get(key), f"rank {rank}: source slice binding {key} mismatch")
        require(binding.get("source_commit") == SOURCE_COMMIT, f"rank {rank}: source binding commit mismatch")
        require(binding.get("source_archive_sha256") == SOURCE_ARCHIVE_SHA256,
                f"rank {rank}: source archive binding mismatch")

        normalized = row["semantic_key"].split("/", 1)[1]
        require(queue_semantic_counts[row["semantic_key"]] == 1, f"rank {rank}: nonunique batch semantic key")
        require(parent_normalized_counts[normalized] == 1, f"rank {rank}: parent occurrence count is not one")
        require(row["dedupe_finding"]["exact_batch_occurrences"] == 1, f"rank {rank}: bad batch count claim")
        require(row["dedupe_finding"]["exact_parent_occurrences"] == 1, f"rank {rank}: bad parent count claim")
        parent_rec = parent_by_variant.get(row["variant_id"])
        require(parent_rec is not None, f"rank {rank}: parent variant missing")
        require(parent_rec["stage_claim_id"] == row["stage_claim_id"], f"rank {rank}: parent claim mismatch")
        pb = row.get("parent_binding", {})
        require(pb.get("parent_catalog_sha256") == PARENT_SHA256, f"rank {rank}: parent SHA binding mismatch")
        require(pb.get("parent_record_canonical_sha256") == digest_bytes(canonical_bytes(parent_rec)),
                f"rank {rank}: parent record canonical hash mismatch")

        require(row.get("grants_new_theorem_credit") is False, f"rank {rank}: new theorem credit forbidden")
        expected_frontier = rank in EXPECTED_ELIGIBLE
        require(row.get("grants_frontier_credit") is expected_frontier, f"rank {rank}: frontier credit mismatch")
        gates = row.get("gates")
        require(isinstance(gates, dict), f"rank {rank}: gates missing")
        required_gate_names = {
            "complete_proved_theorem_statement", "primary_resolution_reference_fixed",
            "scope_matches_reference", "documented_open_problem_or_frontier_main_result",
            "proved_status_verified_as_of_2026_08_10", "rights_review_complete_for_existing_credit",
            "semantic_dedupe_complete", "semantic_dedupe_passed",
        }
        require(set(gates) == required_gate_names, f"rank {rank}: gate schema mismatch")
        require(all(isinstance(v, bool) for v in gates.values()), f"rank {rank}: nonboolean gate")
        refs = row.get("primary_resolution_references")
        require(isinstance(refs, list), f"rank {rank}: references must be an array")
        if expected_frontier:
            require(all(gates.values()), f"rank {rank}: eligible row has failed gate")
            require(len(refs) >= 1, f"rank {rank}: eligible row has no fixed primary reference")
            require("all_eligibility_gates_passed" in row.get("reason_codes", []),
                    f"rank {rank}: eligible reason code missing")
        else:
            require(row.get("grants_frontier_credit") is False, f"rank {rank}: noneligible credit true")
        require(gates["rights_review_complete_for_existing_credit"] is True,
                f"rank {rank}: rights review not recorded")
        require("not independently cleared" in row.get("rights_finding", ""),
                f"rank {rank}: source-specific rights limitation omitted")

        duplicate_of = EXPECTED_DUPLICATES.get(rank)
        dd = row["dedupe_finding"]
        require(dd.get("conceptual_duplicate_of_candidate_rank") == duplicate_of,
                f"rank {rank}: conceptual duplicate binding mismatch")
        require(dd.get("distinct_for_frontier_credit") is (duplicate_of is None),
                f"rank {rank}: distinctness mismatch")
        require(gates["semantic_dedupe_complete"] is True, f"rank {rank}: dedupe not completed")
        require(gates["semantic_dedupe_passed"] is (duplicate_of is None),
                f"rank {rank}: dedupe pass mismatch")
        if duplicate_of is not None:
            require(row["decision"] == "reject", f"rank {rank}: duplicate not rejected")
            require(duplicate_of in EXPECTED_ELIGIBLE, f"rank {rank}: selected duplicate representative is not eligible")

        for ref in refs:
            require(ref.get("role", "").startswith("primary_resolution"), f"rank {rank}: bad reference role")
            if ref.get("kind") == "immutable_bibliographic_locator":
                require(rank in {1, 3} and ref.get("identifier_scheme") == "doi", f"rank {rank}: unfixed locator")
                require(ref.get("fixed_in_source_row_sha256") == queue_row_hash,
                        f"rank {rank}: DOI is not bound to queue row")
                continue
            asset_key = ref.get("asset_key")
            expected_hash = ref.get("external_snapshot_sha256")
            locator = ref.get("locator")
            require(isinstance(asset_key, str) and asset_key, f"rank {rank}: external asset key missing")
            require(isinstance(expected_hash, str) and len(expected_hash) == 64 and
                    all(char in "0123456789abcdef" for char in expected_hash),
                    f"rank {rank}: external snapshot SHA-256 invalid")
            require(isinstance(locator, str) and locator.startswith("https://"),
                    f"rank {rank}: stable external locator missing")
            require(ref.get("artifact_path") is None, f"rank {rank}: third-party evidence must not be redistributed")
            require(ref.get("redistribution_status") == "evidence_bytes_not_redistributed",
                    f"rank {rank}: external evidence redistribution status missing")
            if ref.get("kind") == "fixed_formal_proof":
                marker = ref.get("target_marker")
                require(isinstance(marker, str) and marker, f"rank {rank}: formal target marker absent")
                require("raw.githubusercontent.com" in locator,
                        f"rank {rank}: formal proof locator is not immutable raw GitHub content")
                require(ref.get("target_proof_sorry_free") is True,
                        f"rank {rank}: target formal proof not recorded closed")
            inventory_entry = {
                "asset_key": asset_key,
                "kind": ref["kind"],
                "locator": locator,
                "external_snapshot_sha256": expected_hash,
                "artifact_path": None,
                "redistribution_status": "evidence_bytes_not_redistributed",
            }
            previous = referenced_assets.setdefault(asset_key, inventory_entry)
            require(previous == inventory_entry, f"rank {rank}: conflicting external asset metadata")

        row_core = dict(row)
        recorded_row_hash = row_core.pop("review_row_sha256", None)
        computed_row_hash = digest_bytes(canonical_bytes(row_core))
        require(recorded_row_hash == computed_row_hash, f"rank {rank}: review row hash mismatch")
        require(canonical_bytes(row) == raw_lines[rank - 1], f"rank {rank}: JSONL line is not canonical")
        seen_review_hashes.append(recorded_row_hash)

    require(decision_counts == Counter({
        "eligible_existing_frontier_credit": 41, "pending": 32, "reject": 12,
    }), f"decision counts mismatch: {decision_counts}")

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt_core = dict(receipt)
    recorded_authority = receipt_core.pop("receipt_authority_sha256", None)
    require(recorded_authority == digest_bytes(canonical_bytes(receipt_core)), "receipt authority hash mismatch")
    require(recorded_authority == EXPECTED_RECEIPT_AUTHORITY_SHA256, "receipt fixed authority mismatch")
    require(receipt.get("schema_version") == "awesome-theorems/frontier-existing-credit-review-receipt/5.5",
            "receipt schema mismatch")
    require(receipt.get("review_batch") == "nonerdos-001-085", "receipt batch mismatch")
    require(receipt.get("review_as_of") == "2026-08-10", "receipt date mismatch")
    inp = receipt["inputs"]
    expected_inputs = {
        "queue_file_sha256": QUEUE_FILE_SHA256,
        "queue_authority_sha256": QUEUE_AUTHORITY_SHA256,
        "parent_catalog_sha256": PARENT_SHA256,
        "parent_manifest_sha256": MANIFEST_SHA256,
        "parent_release_root_sha256": RELEASE_ROOT_SHA256,
        "formal_conjectures_commit": SOURCE_COMMIT,
        "source_archive_sha256": SOURCE_ARCHIVE_SHA256,
        "source_license_sha256": LICENSE_SHA256,
    }
    for key, value in expected_inputs.items():
        require(inp.get(key) == value, f"receipt input {key} mismatch")
    require(receipt["credit_policy"]["automatic_credit"] is False, "automatic credit forbidden")
    require(receipt["credit_policy"]["all_grants_new_theorem_credit"] is False,
            "receipt new-credit policy mismatch")
    require(receipt["credit_policy"]["release_or_queue_modified"] is False,
            "receipt mutation policy mismatch")
    counts = receipt["counts"]
    require(counts == {
        "review_rows": 85,
        "eligible_existing_frontier_credit": 41,
        "pending": 32,
        "reject": 12,
        "grants_frontier_credit": 41,
        "grants_new_theorem_credit": 0,
    }, "receipt counts mismatch")
    out = receipt["output"]
    require(out.get("jsonl_file") == jsonl_path.name, "receipt JSONL filename mismatch")
    require(out.get("jsonl_sha256") == digest_bytes(jsonl_bytes), "receipt JSONL hash mismatch")
    expected_output_digests = {
        "review_row_sha256_set_sha256": digest_set(seen_review_hashes),
        "candidate_rank_set_sha256": digest_set([r["candidate_rank"] for r in rows]),
        "stage_claim_id_set_sha256": digest_set([r["stage_claim_id"] for r in rows]),
        "variant_id_set_sha256": digest_set([r["variant_id"] for r in rows]),
        "semantic_key_set_sha256": digest_set([r["semantic_key"] for r in rows]),
        "eligible_variant_id_set_sha256": digest_set([r["variant_id"] for r in rows if r["grants_frontier_credit"]]),
        "eligible_semantic_key_set_sha256": digest_set([r["semantic_key"] for r in rows if r["grants_frontier_credit"]]),
        "decision_vector_sha256": digest_bytes(canonical_bytes([[r["candidate_rank"], r["decision"]] for r in rows])),
    }
    for key, value in expected_output_digests.items():
        require(out.get(key) == value, f"receipt output digest {key} mismatch")

    receipt_assets = inp.get("fixed_evidence_assets")
    require(isinstance(receipt_assets, list), "receipt evidence inventory missing")
    inventory = {x["asset_key"]: x for x in receipt_assets}
    require(inventory == referenced_assets, "receipt evidence inventory does not equal referenced assets")
    require(inp.get("external_evidence_bytes_redistributed") is False,
            "receipt must forbid redistribution of external evidence bytes")
    expected_asset_set = digest_set([
        f"{key}:{item['external_snapshot_sha256']}:{item['locator']}"
        for key, item in sorted(inventory.items())
    ])
    require(inp.get("fixed_evidence_asset_set_sha256") == expected_asset_set,
            "receipt evidence set digest mismatch")

    return {
        "status": "valid",
        "review_rows": 85,
        "eligible_existing_frontier_credit": 41,
        "pending": 32,
        "reject": 12,
        "grants_new_theorem_credit": 0,
        "jsonl_sha256": digest_bytes(jsonl_bytes),
        "receipt_authority_sha256": recorded_authority,
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[4])
    p.add_argument("--source-archive", type=Path, default=None)
    p.add_argument("--jsonl", type=Path, default=None)
    p.add_argument("--receipt", type=Path, default=None)
    return p.parse_args()


if __name__ == "__main__":
    try:
        result = validate(parse_args())
    except (ValidationError, AssertionError, KeyError, ValueError, OSError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
