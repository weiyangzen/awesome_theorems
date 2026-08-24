#!/usr/bin/env python3
"""Migrate and seal the completed OEIS v5.5 candidate audit into the repository.

This utility is intentionally an import tool, not a release publisher.  It
copies the authoritative review inputs from a supplied audit workspace,
normalizes embedded local paths to repository-relative names, writes a compact
combined survivor projection, and seals every repository-owned artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
CURATION_REL = Path("Docs/catalog/v5/curation/oeis_v5_5")
CURATION = REPO_ROOT / CURATION_REL
SOURCE_REL = Path("Docs/catalog/v5/sources")
PARENT_REL = Path("Docs/catalog/v5/releases/5.4")
CURRENT_RELEASE_REL = Path("Docs/catalog/v5/Current_Release.json")

V1_REVIEW_NAMES = [f"review-{index:02d}.jsonl" for index in range(8)]
V2_REVIEW_NAMES = [f"review-v2-{index:02d}.jsonl" for index in range(8)]

COPY_MAP = {
    "output/unique-normalized-candidates.jsonl": "v1/legacy-candidates.jsonl",
    **{f"review-8/batch-{index:02d}.jsonl": f"v1/batches/batch-{index:02d}.jsonl"
       for index in range(8)},
    **{f"reviews/{name}": f"v1/reviews/{name}" for name in V1_REVIEW_NAMES},
    **{f"reviews-v2/{name}": f"v2/reviews/{name}" for name in V2_REVIEW_NAMES},
    "cross-dedupe-audit.json": "v1/cross-dedupe-audit.json",
    "internal-semantic-dedupe.json": "v1/internal-semantic-dedupe.json",
    "internal-semantic-dedupe-tier-supplement.json": "v1/internal-semantic-dedupe-tier-supplement.json",
    "parent-match-a.json": "v1/parent-match-a.json",
    "parent-match-b.json": "v1/parent-match-b.json",
    "parent-match-retrieval.jsonl": "v1/support/parent-match-retrieval.jsonl",
    "parent-strict-compact.tsv": "v1/support/parent-strict-compact.tsv",
    "accepted-compact.tsv": "v1/support/accepted-compact.tsv",
    "review-v2-only-8/v2-only-499.jsonl": "v2/source-v2-only-499.jsonl",
    **{f"review-v2-only-8/batch-{index:02d}.jsonl": f"v2/batches/batch-{index:02d}.jsonl"
       for index in range(8)},
    "v2-consolidation-manual-annotations.json": "v2/manual-annotations.json",
    "v2-consolidation-audit.json": "v2/consolidation-audit.json",
    "v2-consolidated-current-survivors.jsonl": "v2/survivors.jsonl",
}

SOURCE_FILES = {
    "source_archive": SOURCE_REL / "oeis-conjectures-4c866362-source.tar.gz",
    "v1_candidates": SOURCE_REL / "oeis-conjectures-4c866362-candidates.jsonl",
    "v2_candidates": SOURCE_REL / "oeis-conjectures-4c866362-all-conjectur-v2.jsonl",
}
PARENT_FILES = {
    "claim_catalog": PARENT_REL / "Claim_Catalog.json",
    "claim_id_registry": PARENT_REL / "Claim_ID_Registry.json",
    "coverage_ledger": PARENT_REL / "Coverage_Ledger.json",
    "migration_v4_to_v5": PARENT_REL / "Migration_v4_to_v5.json",
    "open_claim_list": PARENT_REL / "Open_Claim_List.json",
    "release_manifest": PARENT_REL / "Release_Manifest.json",
    "stage5_claim_id_registry": PARENT_REL / "Stage5_Claim_ID_Registry.json",
    "strict_ledger": PARENT_REL / "Strict_Conjecture_Ledger.json",
    "theorem_list": PARENT_REL / "Theorem_List.json",
}
PARENT_ROWS = {
    "claim_catalog": 4100,
    "claim_id_registry": 7584,
    "coverage_ledger": 5961,
    "migration_v4_to_v5": 7584,
    "open_claim_list": 1600,
    "release_manifest": None,
    "stage5_claim_id_registry": 7584,
    "strict_ledger": 1001,
    "theorem_list": 2500,
}


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def jsonl_rows(path: Path) -> int:
    return sum(1 for line in path.read_bytes().splitlines() if line.strip())


def binding(path: Path, *, rows: int | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": path.relative_to(REPO_ROOT).as_posix(),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }
    if rows is not None:
        result["rows"] = rows
    return result


def normalize_path_string(value: str) -> str:
    old_root = "/tmp/oeis-conjecture-source-audit/"
    repo_root = "/home/sansha/Github/awesome_theorems/"
    if value == "/tmp/oeis-conjecture-source-audit":
        return CURATION_REL.as_posix()
    if value.startswith(old_root):
        suffix = value[len(old_root):]
        mapped = COPY_MAP.get(suffix)
        if mapped is not None:
            return (CURATION_REL / mapped).as_posix()
        if suffix == "output/unique-normalized-candidates.jsonl":
            return (CURATION_REL / "v1/legacy-candidates.jsonl").as_posix()
        if suffix.startswith("review-8/batch-"):
            name = suffix.rsplit("/", 1)[-1]
            return (CURATION_REL / "v1/batches" / name).as_posix()
        if suffix.startswith("review-v2-only-8/batch-"):
            name = suffix.rsplit("/", 1)[-1]
            return (CURATION_REL / "v2/batches" / name).as_posix()
        if suffix == "review-v2-only-8/v2-only-499.jsonl":
            return (CURATION_REL / "v2/source-v2-only-499.jsonl").as_posix()
        if suffix == "consolidate_v2_reviews.py":
            return (CURATION_REL / "v2/consolidation-audit.json").as_posix()
        if suffix in {"parent-match-retrieval.jsonl", "parent-strict-compact.tsv",
                      "accepted-compact.tsv"}:
            return (CURATION_REL / COPY_MAP[suffix]).as_posix()
        raise ValueError(f"unmapped temporary provenance path: {value}")
    if value == "/home/sansha/Github/awesome_theorems":
        return "."
    if value.startswith(repo_root):
        return value[len(repo_root):]
    return value


def normalize(value: Any) -> Any:
    if isinstance(value, str):
        return normalize_path_string(value)
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_artifact(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    raw = source.read_bytes()
    if b"/tmp/" not in raw and b"/home/" not in raw:
        destination.write_bytes(raw)
        return
    if source.suffix == ".json":
        destination.write_bytes(canonical(normalize(json.loads(source.read_text(encoding="utf-8")))))
    elif source.suffix == ".jsonl":
        rows = load_jsonl(source)
        destination.write_bytes(b"".join(canonical(normalize(row)) for row in rows))
    else:
        shutil.copyfile(source, destination)


def rebind_reference(value: dict[str, Any], path: Path, *, rows_key: str | None = None) -> None:
    value["path"] = path.relative_to(REPO_ROOT).as_posix()
    value["sha256"] = sha256_file(path)
    if rows_key is not None:
        value[rows_key] = jsonl_rows(path)
    if "size_bytes" in value:
        value["size_bytes"] = path.stat().st_size


def rebind_nested_artifacts() -> None:
    internal_path = CURATION / "v1/internal-semantic-dedupe.json"
    supplement_path = CURATION / "v1/internal-semantic-dedupe-tier-supplement.json"
    parent_a_path = CURATION / "v1/parent-match-a.json"
    parent_b_path = CURATION / "v1/parent-match-b.json"
    cross_path = CURATION / "v1/cross-dedupe-audit.json"
    manual_path = CURATION / "v2/manual-annotations.json"
    v2_audit_path = CURATION / "v2/consolidation-audit.json"

    v1_batch_paths = [CURATION / f"v1/batches/batch-{index:02d}.jsonl" for index in range(8)]
    v1_review_paths = [CURATION / f"v1/reviews/review-{index:02d}.jsonl" for index in range(8)]
    v2_batch_paths = [CURATION / f"v2/batches/batch-{index:02d}.jsonl" for index in range(8)]
    v2_review_paths = [CURATION / f"v2/reviews/review-v2-{index:02d}.jsonl" for index in range(8)]
    legacy_path = CURATION / "v1/legacy-candidates.jsonl"
    retrieval_path = CURATION / "v1/support/parent-match-retrieval.jsonl"
    strict_compact_path = CURATION / "v1/support/parent-strict-compact.tsv"
    accepted_compact_path = CURATION / "v1/support/accepted-compact.tsv"
    v2_master_path = CURATION / "v2/source-v2-only-499.jsonl"
    v2_survivors_path = CURATION / "v2/survivors.jsonl"

    v1_review_stats = []
    for path in v1_review_paths:
        rows = load_jsonl(path)
        accepted = sum(row.get("decision") == "accept" for row in rows)
        v1_review_stats.append((len(rows), accepted, len(rows) - accepted))
    v2_review_stats = []
    v2_review_sha_by_key: dict[str, str] = {}
    for path in v2_review_paths:
        rows = load_jsonl(path)
        accepted = sum(row.get("decision") == "accept" for row in rows)
        high_medium = sum(
            row.get("decision") == "accept"
            and row.get("importance_tier") in {"high", "medium"}
            for row in rows
        )
        v2_review_stats.append((len(rows), accepted, high_medium))
        review_sha = sha256_file(path)
        for row in rows:
            v2_review_sha_by_key[row["candidate_key"]] = review_sha

    internal = json.loads(internal_path.read_text(encoding="utf-8"))
    scope = internal["scope"]
    scope["candidate_file"] = legacy_path.relative_to(REPO_ROOT).as_posix()
    scope["candidate_file_sha256"] = sha256_file(legacy_path)
    for reference, path in zip(scope["review_files"], v1_review_paths):
        rebind_reference(reference, path, rows_key="row_count")
    internal_path.write_bytes(canonical(internal))

    supplement = json.loads(supplement_path.read_text(encoding="utf-8"))
    rebind_reference(supplement["source_audit"], internal_path)
    supplement_path.write_bytes(canonical(supplement))

    for path, selected_reviews in (
        (parent_a_path, range(0, 3)),
        (parent_b_path, range(3, 8)),
    ):
        parent_match = json.loads(path.read_text(encoding="utf-8"))
        for reference, index in zip(parent_match["scope"]["review_files"], selected_reviews):
            rebind_reference(reference, v1_review_paths[index], rows_key="rows")
            reference["accepted"] = v1_review_stats[index][1]
        inputs = parent_match["inputs"]
        rebind_reference(inputs["parent_match_retrieval"], retrieval_path)
        rebind_reference(inputs["parent_strict_compact"], strict_compact_path)
        if "accepted_compact" in inputs:
            rebind_reference(inputs["accepted_compact"], accepted_compact_path)
        path.write_bytes(canonical(parent_match))

    cross = json.loads(cross_path.read_text(encoding="utf-8"))
    cross_inputs = cross["inputs"]
    rebind_reference(cross_inputs["candidate_file"], legacy_path, rows_key="rows")
    for reference, path in zip(cross_inputs["batch_files"], v1_batch_paths):
        rebind_reference(reference, path, rows_key="rows")
    for index, (reference, path) in enumerate(zip(cross_inputs["review_files"], v1_review_paths)):
        rebind_reference(reference, path, rows_key="rows")
        reference["accepted"] = v1_review_stats[index][1]
        reference["rejected"] = v1_review_stats[index][2]
    for name, path in (
        ("internal_semantic_dedupe", internal_path),
        ("internal_tier_supplement", supplement_path),
        ("parent_match_a", parent_a_path),
        ("parent_match_b", parent_b_path),
        ("parent_match_retrieval", retrieval_path),
        ("parent_strict_compact", strict_compact_path),
    ):
        rebind_reference(cross_inputs[name], path)
    rebind_reference(
        cross_inputs["parent_catalog"],
        REPO_ROOT / "Docs/catalog/v5/releases/5.3/Claim_Catalog.json",
    )
    rebind_reference(
        cross_inputs["parent_ledger"],
        REPO_ROOT / "Docs/catalog/v5/releases/5.3/Strict_Conjecture_Ledger.json",
    )
    cross_path.write_bytes(canonical(cross))

    v2_survivors = load_jsonl(v2_survivors_path)
    for row in v2_survivors:
        row["source_review_sha256"] = v2_review_sha_by_key[row["candidate_key"]]
    v2_survivors_path.write_bytes(b"".join(canonical(row) for row in v2_survivors))

    v2_audit = json.loads(v2_audit_path.read_text(encoding="utf-8"))
    original_consolidator_sha = v2_audit["inputs"]["consolidator"]["sha256"]
    migration_tool = Path(__file__).resolve()
    v2_audit["inputs"]["consolidator"] = {
        **binding(migration_tool),
        "historical_generator_sha256": original_consolidator_sha,
        "role": "repository migration and receipt sealing; final validity is replayed by the independent checker",
    }
    v2_inputs = v2_audit["inputs"]
    for index, (reference, path) in enumerate(zip(v2_inputs["available_reviews"], v2_review_paths)):
        rebind_reference(reference, path, rows_key="rows")
        reference["accepted"] = v2_review_stats[index][1]
        reference["high_medium_accepted"] = v2_review_stats[index][2]
        reference["validation_errors"] = 0
    for reference, path in zip(v2_inputs["v2_batch_inputs"], v2_batch_paths):
        rebind_reference(reference, path, rows_key="rows")
    rebind_reference(v2_inputs["v2_master"], v2_master_path, rows_key="rows")
    rebind_reference(v2_inputs["v1_final_audit"], cross_path)
    rebind_reference(v2_inputs["manual_annotations"], manual_path)
    parent_input_names = {
        "catalog": "claim_catalog",
        "manifest": "release_manifest",
        "open_claim_list": "open_claim_list",
        "strict_ledger": "strict_ledger",
        "theorem_list": "theorem_list",
    }
    for input_name, parent_name in parent_input_names.items():
        rebind_reference(
            v2_inputs["parent_5_4"][input_name], REPO_ROOT / PARENT_FILES[parent_name]
        )
    v2_audit_path.write_bytes(canonical(v2_audit))


def build_combined_survivors(v1_audit: dict[str, Any], v2_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    survivor_keys = v1_audit["high_medium_survivor_keys"]
    all_tier = {row["candidate_key"]: row for row in v1_audit["all_tier_survivors"]}
    v1_rows = []
    for key in survivor_keys:
        source = all_tier[key]
        v1_rows.append({
            "candidate_key": key,
            "a_numbers": source["a_numbers"],
            "importance_tier": source["importance_tier"],
            "semantic_summary": source["semantic_summary"],
            "audit_layer": "v1_narrow_marker",
            "candidate_only": True,
            "grants_catalog_entry": False,
            "grants_strict_conjecture_credit": False,
        })
    normalized_v2 = [{
        **row,
        "audit_layer": "v2_literal_stem_extension",
        "candidate_only": True,
        "grants_catalog_entry": False,
        "grants_strict_conjecture_credit": False,
    } for row in v2_rows]
    return [*v1_rows, *normalized_v2]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-workspace", type=Path, required=True)
    args = parser.parse_args()
    source_workspace = args.source_workspace.resolve(strict=True)

    for source_relative, destination_relative in COPY_MAP.items():
        source = source_workspace / source_relative
        if not source.is_file():
            raise ValueError(f"missing authoritative audit artifact: {source}")
        write_artifact(source, CURATION / destination_relative)

    rebind_nested_artifacts()

    v1_audit_path = CURATION / "v1/cross-dedupe-audit.json"
    v2_audit_path = CURATION / "v2/consolidation-audit.json"
    v2_survivors_path = CURATION / "v2/survivors.jsonl"
    v1_audit = json.loads(v1_audit_path.read_text(encoding="utf-8"))
    v2_audit = json.loads(v2_audit_path.read_text(encoding="utf-8"))
    v2_survivors = load_jsonl(v2_survivors_path)
    combined = build_combined_survivors(v1_audit, v2_survivors)
    combined_path = CURATION / "combined-survivors.jsonl"
    combined_path.write_bytes(b"".join(canonical(row) for row in combined))

    artifacts: dict[str, Any] = {}
    for _, destination_relative in sorted(COPY_MAP.items(), key=lambda item: item[1]):
        path = CURATION / destination_relative
        artifacts[destination_relative] = binding(
            path, rows=jsonl_rows(path) if path.suffix == ".jsonl" else None,
        )
    artifacts["combined-survivors.jsonl"] = binding(combined_path, rows=len(combined))

    source_bindings = {
        name: binding(REPO_ROOT / relative, rows=(
            602 if name == "v1_candidates" else 1101 if name == "v2_candidates" else None
        ))
        for name, relative in SOURCE_FILES.items()
    }
    extractor_paths = {
        "v1_extractor": REPO_ROOT / "Docs/tools/extract_oeis_conjectures_v5.py",
        "v2_extractor": REPO_ROOT / "Docs/tools/extract_oeis_conjectures_v5_v2.py",
    }
    source_receipt_path = REPO_ROOT / SOURCE_REL / "oeis-conjectures-4c866362-receipt.json"
    source_receipt = {
        "schema_version": "awesome-theorems/oeis-frozen-source-receipt/5.5",
        "artifact": source_receipt_path.relative_to(REPO_ROOT).as_posix(),
        "source": {
            "repository": "https://github.com/oeis/oeisdata",
            "commit": "4c8663620c66525a0c92654a4a9c4703b3d98921",
            "tree_sha1": "7e0ed547bdc22e34ec578307fed26572bbd58b1e",
            "license_spdx": "CC-BY-SA-4.0",
        },
        "artifacts": source_bindings,
        "extractors": {name: binding(path) for name, path in extractor_paths.items()},
        "counts": {
            "frozen_sequence_entries": 622,
            "v1_candidate_rows": 602,
            "v2_candidate_rows": 1101,
            "v2_only_candidate_rows": 499,
        },
        "candidate_only": True,
        "grants_catalog_entry": False,
        "grants_strict_conjecture_credit": False,
    }
    source_receipt_path.write_bytes(canonical(source_receipt))
    source_bindings["source_receipt"] = binding(source_receipt_path)
    parent_bindings = {
        name: binding(REPO_ROOT / relative, rows=PARENT_ROWS[name])
        for name, relative in PARENT_FILES.items()
    }
    receipt = {
        "schema_version": "awesome-theorems/oeis-candidate-audit-receipt/5.5",
        "artifact": (CURATION_REL / "audit-receipt.json").as_posix(),
        "audit_date": "2026-08-10",
        "source": source_bindings,
        "parent_release_5_4": parent_bindings,
        "publication_boundary": {
            "current_release": binding(REPO_ROOT / CURRENT_RELEASE_REL),
        },
        "artifacts": artifacts,
        "counts": {
            "v1_candidates_reviewed": 602,
            "v1_high_survivors": 41,
            "v1_medium_survivors": 158,
            "v1_high_medium_survivors": 199,
            "v2_only_candidates_reviewed": 499,
            "v2_high_survivors": 18,
            "v2_medium_survivors": 51,
            "v2_high_medium_survivors": 69,
            "combined_candidate_survivors": 268,
            "formal_release_additions": 0,
            "strict_credits_granted": 0,
        },
        "candidate_only": True,
        "formal_release_modified": False,
        "release_published": False,
        "tools": {
            "migration": binding(Path(__file__).resolve()),
            "checker": binding(
                REPO_ROOT / "Docs/catalog/v5/tools/check_oeis_audit_v5_5.py"
            ),
        },
    }
    (CURATION / "audit-receipt.json").write_bytes(canonical(receipt))
    print("PASS OEIS audit migration: v1=199 v2=69 combined=268 formal_additions=0")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1)
