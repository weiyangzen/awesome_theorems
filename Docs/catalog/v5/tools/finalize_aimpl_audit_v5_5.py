#!/usr/bin/env python3
"""Validate and seal the AimPL per-record review and cross-dedupe audit."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_DIR = REPO_ROOT / "Docs/catalog/v5/sources/aimpl"
CURATION_DIR = REPO_ROOT / "Docs/catalog/v5/curation/aimpl_v5_5"
TOOLS_DIR = REPO_ROOT / "Docs/catalog/v5/tools"
PARENT_DIR = REPO_ROOT / "Docs/catalog/v5/releases/5.4"
SCHEMA = "awesome-theorems/aimpl-strict-conjecture-review/1"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def binding(path: Path, *, row_count: int | None = None) -> dict[str, object]:
    result: dict[str, object] = {
        "path": path.relative_to(REPO_ROOT).as_posix(),
        "sha256": digest(path),
        "size_bytes": path.stat().st_size,
    }
    if row_count is not None:
        result["rows"] = row_count
    return result


# These are reviewed relationships, not score-triggered decisions.
RELATIONSHIPS: dict[int, dict[str, list[dict]]] = {
    20: {"parent_5_4": [{
        "id": "ATV-00005370", "relation": "related_not_equivalent",
        "basis": "The parent is Sidorenko's graph homomorphism-density conjecture; AimPL is a 3-uniform 3-partite hypergraph copy-count analogue.",
    }]},
    23: {
        "parent_5_4": [{
            "id": "ATV-00003655", "relation": "excluded_source_component_equivalent",
            "basis": "AimPL item (1) is equivalent to the parent Erdos1082.parts.i claim, so the review deliberately selects only item (2) and grants no credit to item (1).",
        }],
        "conjecturebench": [{
            "id": "cb-0135", "relation": "excluded_source_component_overlap",
            "basis": "AimPL item (1), which the review excludes, is the global-distance component of cb-0135; the accepted AimPL item (2) is the distinct isosceles-triangle claim.",
        }],
    },
    28: {"parent_5_4": [{
        "id": "ATV-00006351", "relation": "shared_attribution_name_not_equivalent",
        "basis": "Both are attributed to Sokal, but the parent concerns coefficientwise Hankel total positivity of GKP row polynomials, whereas AimPL concerns zeros of P_n(z,w).",
    }]},
    30: {"parent_5_4": [{
        "id": "ATV-00005841", "relation": "related_not_equivalent",
        "basis": "The parent record proves the 2/7 lower-bound construction; AimPL conjectures equality pi(K4^-)=2/7, which also requires the matching upper bound.",
    }]},
    31: {"aimpl_batch": [{
        "id": "aimpl/32", "relation": "special_case_not_equivalent",
        "basis": "Candidate 31 is the m=4 instance of candidate 32's all-m complete-3-graph formula; the two have different truth conditions.",
    }]},
    32: {"aimpl_batch": [{
        "id": "aimpl/31", "relation": "generalization_not_equivalent",
        "basis": "Candidate 32 implies candidate 31 at m=4 but is not implied by it.",
    }]},
    34: {"aimpl_batch": [{
        "id": "aimpl/35", "relation": "same_family_not_equivalent",
        "basis": "The forbidden hypergraphs C5^3 and C5^- are different and have different asserted densities.",
    }]},
    35: {"aimpl_batch": [{
        "id": "aimpl/34", "relation": "same_family_not_equivalent",
        "basis": "The forbidden hypergraphs C5^- and C5^3 are different and have different asserted densities.",
    }]},
    36: {"aimpl_batch": [{
        "id": "aimpl/37", "relation": "related_extremal_model_not_equivalent",
        "basis": "Both concern Ruzsa-Szemeredi-type sparse configurations, but their quantified structures and conclusions differ.",
    }]},
    37: {"aimpl_batch": [{
        "id": "aimpl/36", "relation": "related_extremal_model_not_equivalent",
        "basis": "The matching-union crossing-configuration claim is not the f^r(n,p,s) statement.",
    }]},
    38: {"aimpl_batch": [{
        "id": "aimpl/36", "relation": "related_extremal_model_not_equivalent",
        "basis": "The source itself calls the graph copy-union conjecture related; it is not semantically equivalent to the hypergraph f^r claim.",
    }]},
    40: {"aimpl_batch": [{
        "id": "aimpl/41", "relation": "parity_variant_not_equivalent",
        "basis": "Even-color and odd-color asymptotic subsequences are logically distinct variants.",
    }]},
    41: {"aimpl_batch": [{
        "id": "aimpl/40", "relation": "parity_variant_not_equivalent",
        "basis": "Odd-color and even-color asymptotic subsequences are logically distinct variants.",
    }]},
    45: {"aimpl_batch": [{
        "id": "aimpl/46", "relation": "named_family_not_equivalent",
        "basis": "The restricted Bareket domain maximization and triangular positive/negative-parameter extremizers are different claims.",
    }]},
    46: {"aimpl_batch": [{
        "id": "aimpl/45", "relation": "named_family_not_equivalent",
        "basis": "The discrete triangle claim is not equivalent to the simply-connected-domain Bareket restriction.",
    }]},
    55: {
        "conjecturebench": [{
            "id": "cb-0088", "relation": "component_overlap",
            "basis": "The AimPL inequality component is Log-Brunn-Minkowski; AimPL additionally prints an equality characterization absent from cb-0088.",
        }],
        "aimpl_batch": [{
            "id": "aimpl/56", "relation": "special_case_not_equivalent",
            "basis": "Candidate 55 is the p=0/logarithmic case within candidate 56's p>=0 family, with an extra equality clause.",
        }],
    },
    56: {
        "conjecturebench": [{
            "id": "cb-0088", "relation": "overlap_at_parameter_value_not_equivalent",
            "basis": "The p=0 specialization overlaps Log-Brunn-Minkowski, but the all-p statement is strictly stronger.",
        }],
        "aimpl_batch": [{
            "id": "aimpl/55", "relation": "generalization_not_equivalent",
            "basis": "The all-p statement contains the logarithmic p=0 case but is not equivalent to it.",
        }],
    },
}


def build() -> tuple[bytes, bytes, bytes]:
    candidates_path = SOURCE_DIR / "candidates.jsonl"
    review_paths = [CURATION_DIR / "review-a.jsonl", CURATION_DIR / "review-b.jsonl"]
    retrieval_path = CURATION_DIR / "cross-dedupe-retrieval.jsonl"
    retrieval_summary_path = CURATION_DIR / "cross-dedupe-retrieval-summary.json"
    manifest_path = SOURCE_DIR / "source-manifest.json"
    asset_receipt_path = SOURCE_DIR / "asset-receipt.json"
    source_asset_path = SOURCE_DIR / "aimpl-source-snapshot.tar.gz"
    crosscheck_cb_path = CURATION_DIR / "crosscheck-conjecturebench-302.jsonl"
    crosscheck_oeis_path = CURATION_DIR / "crosscheck-oeis-602.jsonl"
    parent_catalog_path = PARENT_DIR / "Claim_Catalog.json"
    parent_manifest_path = PARENT_DIR / "Release_Manifest.json"
    for path in [
        candidates_path, *review_paths, retrieval_path, retrieval_summary_path,
        manifest_path, asset_receipt_path, source_asset_path, crosscheck_cb_path,
        crosscheck_oeis_path, parent_catalog_path, parent_manifest_path,
    ]:
        if not path.exists():
            raise ValueError(f"missing required audit input: {path}")
    candidates = load_jsonl(candidates_path)
    reviews = [row for path in review_paths for row in load_jsonl(path)]
    retrieval = load_jsonl(retrieval_path)
    if [row["candidate_index"] for row in candidates] != list(range(1, 60)):
        raise ValueError("candidate indices are not exactly 1..59")
    reviews.sort(key=lambda row: row["candidate_index"])
    if [row["candidate_index"] for row in reviews] != list(range(1, 60)):
        raise ValueError("review coverage is not exactly once for indices 1..59")
    if [row["candidate_index"] for row in retrieval] != list(range(1, 60)):
        raise ValueError("retrieval coverage is not exactly 1..59")
    retrieval_by_index = {row["candidate_index"]: row for row in retrieval}
    output = []
    for candidate, review in zip(candidates, reviews):
        index = candidate["candidate_index"]
        if review.get("candidate_key") != candidate["candidate_key"]:
            raise ValueError(f"candidate key mismatch at {index}")
        decision = review.get("decision")
        if decision not in {"accept", "reject", "pending"}:
            raise ValueError(f"invalid decision at {index}")
        if decision == "accept":
            if review.get("tier") not in {"high", "medium"}:
                raise ValueError(f"accepted row lacks high/medium tier at {index}")
            exact = review.get("exact_claim_html")
            if not isinstance(exact, str) or exact not in candidate["exact_source"]["body_html"]:
                raise ValueError(f"accepted exact claim is not a literal body substring at {index}")
            if not all(review.get(field) is True for field in
                       ("truth_apt", "context_complete", "source_asserted_open")):
                raise ValueError(f"accepted row fails strict boolean gate at {index}")
        else:
            if review.get("tier") != "none" or review.get("exact_claim_html") is not None:
                raise ValueError(f"non-accepted row improperly has tier/claim at {index}")
        relation_map = RELATIONSHIPS.get(index, {})
        retrieval_row = retrieval_by_index[index]
        top_retrieval = {
            corpus: [{"id": x["id"], "score": x["score"], "label": x.get("label")}
                     for x in retrieval_row["top_matches"][corpus][:5]]
            for corpus in ("parent_5_4", "conjecturebench", "oeis", "aimpl_batch")
        }
        cross = {
            "manual_verdict": (
                "component_overlap_present_no_duplicate_credit"
                if any("component_overlap" in rel["relation"]
                       for rels in relation_map.values() for rel in rels)
                else "semantic_unique_with_any_listed_relations_non_equivalent"
            ),
            "parent_5_4": relation_map.get("parent_5_4", []),
            "conjecturebench": relation_map.get("conjecturebench", []),
            "oeis": relation_map.get("oeis", []),
            "aimpl_batch": relation_map.get("aimpl_batch", []),
            "top_lexical_retrieval_reviewed": top_retrieval,
            "retrieval_scores_are_not_verdicts": True,
        }
        output.append({
            "schema_version": SCHEMA,
            "candidate_index": index,
            "candidate_key": candidate["candidate_key"],
            "source_record_key": candidate["source_record_key"],
            "source_url": candidate["source_snapshot"]["source_url"],
            "source_sha256": candidate["source_snapshot"]["source_sha256"],
            "initial_review": review,
            "cross_dedupe": cross,
            "final_decision": decision,
            "final_tier": review["tier"],
            "candidate_only": True,
            "strict_credit_granted": False,
        })
    ledger_bytes = b"".join(canonical(row) for row in output)
    counts = Counter(row["final_decision"] for row in output)
    tiers = Counter(row["final_tier"] for row in output if row["final_decision"] == "accept")
    reason_counts = Counter(row["initial_review"]["reason_code"] for row in output)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    summary = {
        "schema_version": SCHEMA,
        "artifact": "Docs/catalog/v5/curation/aimpl_v5_5/review-summary.json",
        "audit_cutoff_utc": manifest["created_at_utc"],
        "counts": {
            "mechanical_explicit_tag_candidates": len(candidates),
            "reviewed_exactly_once": len(output),
            "accepted_high": tiers["high"],
            "accepted_medium": tiers["medium"],
            "accepted_total": counts["accept"],
            "reject": counts["reject"],
            "pending": counts["pending"],
            "cross_source_component_overlaps": sum(
                row["cross_dedupe"]["manual_verdict"] == "component_overlap_present_no_duplicate_credit"
                for row in output
            ),
            "strict_credits_granted": 0,
        },
        "reason_counts": dict(sorted(reason_counts.items())),
        "source_scope": manifest["counts"],
        "source_date": {
            "snapshot_cutoff_utc": manifest["created_at_utc"],
            "upstream_last_modified_exposed": False,
            "policy": manifest["source"]["source_date_policy"],
        },
        "rights_and_citation": {
            "license_spdx": "CC-BY-SA-3.0",
            "license_url": "http://creativecommons.org/licenses/by-sa/3.0/",
            "verified_root_pages": manifest["counts"]["root_pages"],
            "verified_section_pages": manifest["counts"]["section_pages"],
            "citation_pattern": manifest["source"]["citation_pattern"],
            "share_alike_required_for_adapted_source_text": True,
        },
        "cross_dedupe_scope": {
            "parent_5_4_records": 4100,
            "oeis_candidates": 602,
            "conjecturebench_records": 302,
            "aimpl_batch_candidates": 59,
            "policy": "lexical retrieval plus per-record manual semantic comparison; related non-equivalent variants do not collapse",
        },
        "admission_boundary": {
            "candidate_only": True,
            "formal_release_modified": False,
            "accepted_rows_are_not_formal_additions": True,
            "strict_credit_granted": 0,
        },
        "inputs": {
            "candidates": binding(candidates_path, row_count=len(candidates)),
            "source_manifest": binding(manifest_path),
            "source_asset_receipt": binding(asset_receipt_path),
            "review_a": binding(review_paths[0], row_count=30),
            "review_b": binding(review_paths[1], row_count=29),
            "cross_dedupe_retrieval": binding(retrieval_path, row_count=len(retrieval)),
            "cross_dedupe_retrieval_summary": binding(retrieval_summary_path),
        },
        "review_ledger_sha256": hashlib.sha256(ledger_bytes).hexdigest(),
    }
    summary_bytes = canonical(summary)
    scripts = [
        TOOLS_DIR / "extract_aimpl_conjectures_v5_5.py",
        TOOLS_DIR / "build_aimpl_review_b_v5_5.py",
        TOOLS_DIR / "build_aimpl_cross_dedupe_v5_5.py",
        TOOLS_DIR / "finalize_aimpl_audit_v5_5.py",
        TOOLS_DIR / "check_aimpl_audit_v5_5.py",
    ]
    ledger_path = CURATION_DIR / "review-ledger.jsonl"
    summary_path = CURATION_DIR / "review-summary.json"
    ledger_binding = {
        "path": ledger_path.relative_to(REPO_ROOT).as_posix(),
        "sha256": hashlib.sha256(ledger_bytes).hexdigest(),
        "size_bytes": len(ledger_bytes),
        "rows": len(output),
    }
    summary_binding = {
        "path": summary_path.relative_to(REPO_ROOT).as_posix(),
        "sha256": hashlib.sha256(summary_bytes).hexdigest(),
        "size_bytes": len(summary_bytes),
    }
    receipt = {
        "schema_version": SCHEMA,
        "artifact": "Docs/catalog/v5/curation/aimpl_v5_5/audit-receipt.json",
        "audit_cutoff_utc": manifest["created_at_utc"],
        "artifacts": {
            "source_asset": binding(source_asset_path),
            "source_manifest": binding(manifest_path),
            "source_asset_receipt": binding(asset_receipt_path),
            "candidates": binding(candidates_path, row_count=len(candidates)),
            "review_a": binding(review_paths[0], row_count=30),
            "review_b": binding(review_paths[1], row_count=29),
            "crosscheck_conjecturebench": binding(crosscheck_cb_path, row_count=302),
            "crosscheck_oeis": binding(crosscheck_oeis_path, row_count=602),
            "cross_dedupe_retrieval": binding(retrieval_path, row_count=len(retrieval)),
            "cross_dedupe_retrieval_summary": binding(retrieval_summary_path),
            "review_ledger": ledger_binding,
            "review_summary": summary_binding,
        },
        "parent_release_inputs": {
            "claim_catalog": binding(parent_catalog_path, row_count=4100),
            "release_manifest": binding(parent_manifest_path),
        },
        "scripts": {
            path.relative_to(REPO_ROOT).as_posix(): digest(path)
            for path in scripts
        },
        "formal_release_modified": False,
        "strict_credits_granted": 0,
    }
    return ledger_bytes, summary_bytes, canonical(receipt)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    ledger, summary, receipt = build()
    outputs = {
        CURATION_DIR / "review-ledger.jsonl": ledger,
        CURATION_DIR / "review-summary.json": summary,
        CURATION_DIR / "audit-receipt.json": receipt,
    }
    if args.check:
        for path, expected in outputs.items():
            if not path.exists() or path.read_bytes() != expected:
                raise ValueError(f"generated audit artifact drift: {path}")
    else:
        for path, data in outputs.items():
            path.write_bytes(data)
    counts = json.loads(summary)["counts"]
    print(f"PASS final audit: high={counts['accepted_high']} medium={counts['accepted_medium']} "
          f"reject={counts['reject']} pending={counts['pending']} strict_credit=0")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
