#!/usr/bin/env python3
"""Prepare and finalize the 1,724-row Putnam formal-variant crosswalk.

Queue mode binds every frozen formalization file to its declaration metadata,
explicit filename/declaration anomalies, and any reviewed seed semantic keys
currently available.  It assigns no semantic disposition automatically.

Final mode requires the complete sealed 768-key seed crosswalk plus one manual,
zero-credit semantic-review disposition for every formal variant.  Exact
duplicate review rows are deduplicated; conflicts, omissions, inferred
filename mappings, or pending decisions fail closed.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any, Iterable, Mapping, Sequence


REPO = Path(__file__).resolve().parents[4]
TOOL_DIR = Path(__file__).resolve().parent
seed_spec = importlib.util.spec_from_file_location(
    "putnam_seed_crosswalk_dependency",
    TOOL_DIR / "build_putnam_seed_crosswalk_v5_6.py",
)
assert seed_spec is not None and seed_spec.loader is not None
seed = importlib.util.module_from_spec(seed_spec)
sys.modules[seed_spec.name] = seed
seed_spec.loader.exec_module(seed)

CURATION_REL = Path("Docs/catalog/v5/curation/putnambench_v5_6")
VARIANTS_REL = CURATION_REL / "PutnamBench_Formal_Variants_v5_6.jsonl"
ASSETS_REL = CURATION_REL / "PutnamBench_Formal_Declaration_Asset_v5_6.jsonl"
REVIEW_DIR_REL = CURATION_REL / "formal-variant-reviews"
QUEUE_REL = CURATION_REL / "formal-variant-crosswalk-review-queue.jsonl"
PROGRESS_REL = CURATION_REL / "formal-variant-crosswalk-progress.json"
CROSSWALK_REL = CURATION_REL / "formal-variant-crosswalk.jsonl"
SEED_CROSSWALK_REL = CURATION_REL / "seed-crosswalk.jsonl"

VARIANTS_SHA = "aae67f4250a7ff9132487b4a1af494697d7add32b9608dd44766fe516deb6dc4"
ASSETS_SHA = "6431c652a888bf2dce1f9eb91692cc79f8bf986e613bc5658a43f5f770e7b563"
EXPECTED_VARIANTS = 1_724
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

DISPOSITIONS = {
    "same_exact_claim_variant", "stronger_variant", "weaker_variant",
    "different_claim_variant", "wrong_problem_duplicate",
    "malformed_or_nonclaim_variant",
}
EXPECTED_ANOMALIES = {
    "putnambench::dfb0a47a1c1ec3a10f2a9acfdf41a2043920f33c::putnam_1968_a1::coq":
        (["coq_declared_name_mismatch"], "putnam_1968_b1", "putnam_1968_a1"),
    "putnambench::dfb0a47a1c1ec3a10f2a9acfdf41a2043920f33c::putnam_1970_b5::coq":
        (["coq_declared_name_mismatch"], "putnam_1970_b5_solution", "putnam_1970_b5"),
    "putnambench::dfb0a47a1c1ec3a10f2a9acfdf41a2043920f33c::putnam_1979_a6::coq":
        (["coq_declared_name_mismatch"], "putnam_1979_b6", "putnam_1979_a6"),
    "putnambench::dfb0a47a1c1ec3a10f2a9acfdf41a2043920f33c::putnam_1980_b3::isabelle":
        (["isabelle_declared_name_mismatch"], "putnam_1980_a3", "putnam_1980_b3"),
    "putnambench::dfb0a47a1c1ec3a10f2a9acfdf41a2043920f33c::putnam_1994_b3::coq":
        (["coq_declared_name_mismatch"], "putnam_1993_b3", "putnam_1994_b3"),
}

QUEUE_KEYS = {
    "schema_version", "variant_id", "source_variant_row_sha256",
    "source_problem_key", "language", "source_binding", "formal_declaration",
    "formal_asset_binding", "upstream_filename_declaration_anomalies",
    "declared_name_problem_key_candidate", "anomaly_requires_manual_mapping",
    "seed_review_state", "candidate_target_semantic_keys", "credit_boundary",
    "row_sha256",
}
REVIEW_KEYS = {
    "schema_version", "variant_id", "queue_row_sha256",
    "source_variant_row_sha256", "source_problem_key", "semantic_problem_key",
    "disposition", "target_semantic_keys", "statement_equivalence",
    "filename_declaration_review", "review", "candidate_only",
    "grants_catalog_entry", "grants_theorem_credit", "row_sha256",
}
EQUIVALENCE_KEYS = {
    "reviewed", "exact_statement_scope", "assumptions_preserved",
    "conclusion_preserved", "notes",
}
FILENAME_REVIEW_KEYS = {
    "reviewed", "source_anomaly_codes", "declared_name", "expected_name",
    "name_matches_problem_key", "semantic_mapping_inferred_from_filename",
    "finding",
}
REVIEW_META_KEYS = {
    "reviewer_id", "reviewed_as_of", "manual_statement_review",
    "manual_formal_variant_semantic_review",
    "manual_filename_declaration_anomaly_review", "notes",
}


class FormalCrosswalkError(RuntimeError):
    """The formal queue, review, or completeness contract failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FormalCrosswalkError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def hash_without(value: Mapping[str, Any], field: str) -> str:
    return digest(canonical({key: item for key, item in value.items() if key != field}))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in value, "row already sealed")
    value["row_sha256"] = hash_without(value, "row_sha256")
    return value


def set_digest(values: Iterable[str]) -> str:
    return digest(canonical(sorted(values)))


def encoded_json(value: Mapping[str, Any]) -> bytes:
    return canonical(value) + b"\n"


def encoded_jsonl(rows: Sequence[Mapping[str, Any]]) -> bytes:
    return b"".join(canonical(row) + b"\n" for row in rows)


def exact(value: Any, keys: set[str], label: str) -> Mapping[str, Any]:
    require(isinstance(value, dict), f"{label} is not an object")
    require(set(value) == keys, f"{label} closed schema drifted: missing={sorted(keys-set(value))} extra={sorted(set(value)-keys)}")
    return value


def nonempty(value: Any, label: str) -> str:
    require(isinstance(value, str) and value.strip() == value and value, f"{label} empty/malformed")
    return value


def load_frozen(repo_root: Path, relative: Path, rows: int, wanted_sha: str, label: str) -> tuple[list[dict[str, Any]], bytes]:
    result, payload = seed.load_jsonl(repo_root / relative, label)
    require(len(result) == rows and digest(payload) == wanted_sha, f"{label} frozen bytes/count drifted")
    for index, row in enumerate(result):
        require(row.get("row_sha256") == hash_without(row, "row_sha256"), f"{label} row seal drifted: {index}")
    return result, payload


def load_formal_sources(repo_root: Path) -> tuple[list[dict[str, Any]], dict[str, tuple[int, dict[str, Any]]]]:
    variants, _ = load_frozen(repo_root, VARIANTS_REL, EXPECTED_VARIANTS, VARIANTS_SHA, "formal variants")
    assets, _ = load_frozen(repo_root, ASSETS_REL, EXPECTED_VARIANTS, ASSETS_SHA, "formal declaration assets")
    asset_by_id = {str(row["variant_id"]): (index + 1, row) for index, row in enumerate(assets)}
    require(len(asset_by_id) == EXPECTED_VARIANTS, "formal asset IDs are not unique")
    observed_anomalies: dict[str, tuple[list[str], str, str]] = {}
    variant_ids: set[str] = set()
    for index, row in enumerate(variants):
        variant_id = nonempty(row.get("variant_id"), f"variant[{index}].variant_id")
        require(variant_id not in variant_ids, f"duplicate formal variant ID: {variant_id}")
        variant_ids.add(variant_id)
        asset = asset_by_id.get(variant_id, (None, None))[1]
        require(asset is not None and asset["problem_key"] == row["problem_key"] and asset["language"] == row["language"], f"formal variant/asset identity drifted: {variant_id}")
        require(asset["external_source_binding"] == row["source_binding"], f"formal variant/asset source drifted: {variant_id}")
        require(asset["declaration_header"]["sha256"] == row["principal_declaration"]["header_sha256"], f"formal variant/asset header drifted: {variant_id}")
        anomalies = row["anomaly_codes"]
        require(isinstance(anomalies, list), f"formal variant anomaly list malformed: {variant_id}")
        if anomalies:
            declaration = row["principal_declaration"]
            observed_anomalies[variant_id] = (
                anomalies, declaration["declared_name"], declaration["expected_name"]
            )
    require(observed_anomalies == EXPECTED_ANOMALIES, "explicit upstream filename/declaration anomaly set drifted")
    return variants, asset_by_id


def candidate_seed_semantics(collection: Mapping[str, Any]) -> dict[str, list[str]]:
    return {
        key: [str(target["semantic_key"]) for target in entry["targets"]]
        for key, entry in collection["selected"].items()
    }


def declared_problem_candidate(name: str) -> str | None:
    return name if seed.PROBLEM_RE.fullmatch(name) else None


def build_queue(repo_root: Path) -> tuple[list[dict[str, Any]], Mapping[str, Any]]:
    variants, asset_by_id = load_formal_sources(repo_root)
    collection = seed.collect_reviews(repo_root)
    semantics_by_problem = candidate_seed_semantics(collection)
    rows: list[dict[str, Any]] = []
    for index, variant in enumerate(variants):
        variant_id = str(variant["variant_id"])
        declaration = variant["principal_declaration"]
        asset_line, asset = asset_by_id[variant_id]
        problem_key = str(variant["problem_key"])
        anomalies = list(variant["anomaly_codes"])
        target_options = semantics_by_problem.get(problem_key, [])
        row = {
            "schema_version": "awesome-theorems/putnam-formal-variant-review-candidate/5.6",
            "variant_id": variant_id,
            "source_variant_row_sha256": variant["row_sha256"],
            "source_problem_key": problem_key,
            "language": variant["language"],
            "source_binding": {
                "path": VARIANTS_REL.as_posix(),
                "file_sha256": VARIANTS_SHA,
                "line_number": index + 1,
                "row_sha256": variant["row_sha256"],
            },
            "formal_declaration": {
                "upstream_relative_path": variant["source_binding"]["upstream_relative_path"],
                "source_file_sha256": variant["source_binding"]["file_sha256"],
                "kind": declaration["kind"],
                "declared_name": declaration["declared_name"],
                "expected_name": declaration["expected_name"],
                "name_matches_problem_key": declaration["name_matches_problem_key"],
                "header_sha256": declaration["header_sha256"],
                "full_declaration_sha256": declaration["full_declaration_sha256"],
                "source_proof_state": declaration["source_proof_state"],
            },
            "formal_asset_binding": {
                "path": ASSETS_REL.as_posix(),
                "file_sha256": ASSETS_SHA,
                "line_number": asset_line,
                "row_sha256": asset["row_sha256"],
                "rights_id": asset["rights"]["rights_id"],
                "license_expression": asset["rights"]["license_expression"],
            },
            "upstream_filename_declaration_anomalies": anomalies,
            "declared_name_problem_key_candidate": declared_problem_candidate(declaration["declared_name"]),
            "anomaly_requires_manual_mapping": bool(anomalies),
            "seed_review_state": "reviewed_semantic_targets_available" if target_options else "seed_review_missing",
            "candidate_target_semantic_keys": target_options,
            "credit_boundary": {
                "candidate_only": True,
                "formal_variant_grants_catalog_entry": False,
                "formal_variant_grants_theorem_credit": False,
                "proof_hole_is_not_proof_evidence": True,
                "filename_or_declaration_name_does_not_determine_semantic_mapping": True,
            },
        }
        rows.append(seal(row))
    require(len(rows) == EXPECTED_VARIANTS, "formal review queue denominator drifted")
    return rows, collection


def load_manual_reviews(repo_root: Path, queue_by_id: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    directory = repo_root / REVIEW_DIR_REL
    paths = sorted(directory.glob("*.jsonl")) if directory.is_dir() else []
    occurrences: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for path in paths:
        rows, _payload = seed.load_jsonl(path, f"formal review {path.name}")
        for index, row in enumerate(rows):
            exact(row, REVIEW_KEYS, f"{path.name}:{index+1}")
            require(row["schema_version"] == "awesome-theorems/putnam-formal-variant-semantic-review/5.6" and row["row_sha256"] == hash_without(row, "row_sha256"), f"formal review schema/seal drifted: {path.name}:{index+1}")
            variant_id = nonempty(row["variant_id"], f"formal review {path.name}:{index+1}.variant_id")
            queue = queue_by_id.get(variant_id)
            require(queue is not None, f"formal review names unknown variant: {variant_id}")
            require(row["queue_row_sha256"] == queue["row_sha256"] and row["source_variant_row_sha256"] == queue["source_variant_row_sha256"] and row["source_problem_key"] == queue["source_problem_key"], f"formal review source/queue binding drifted: {variant_id}")
            require(row["disposition"] in DISPOSITIONS, f"formal review disposition invalid: {variant_id}")
            targets = row["target_semantic_keys"]
            require(isinstance(targets, list) and targets == sorted(set(targets)), f"formal review target list malformed: {variant_id}")
            equivalence = exact(row["statement_equivalence"], EQUIVALENCE_KEYS, f"formal review equivalence: {variant_id}")
            require(equivalence["reviewed"] is True and all(isinstance(equivalence[key], bool) for key in ("exact_statement_scope", "assumptions_preserved", "conclusion_preserved")) and isinstance(equivalence["notes"], str), f"formal equivalence review malformed: {variant_id}")
            if row["disposition"] == "same_exact_claim_variant":
                require(equivalence["exact_statement_scope"] is True and equivalence["assumptions_preserved"] is True and equivalence["conclusion_preserved"] is True, f"same-exact formal review equivalence gates fail: {variant_id}")
            filename = exact(row["filename_declaration_review"], FILENAME_REVIEW_KEYS, f"formal filename review: {variant_id}")
            declaration = queue["formal_declaration"]
            require(filename["reviewed"] is True and filename["source_anomaly_codes"] == queue["upstream_filename_declaration_anomalies"] and filename["declared_name"] == declaration["declared_name"] and filename["expected_name"] == declaration["expected_name"] and filename["name_matches_problem_key"] == declaration["name_matches_problem_key"], f"formal filename anomaly binding drifted: {variant_id}")
            require(filename["semantic_mapping_inferred_from_filename"] is False and isinstance(filename["finding"], str) and filename["finding"], f"formal filename review inferred mapping or lacks finding: {variant_id}")
            review = exact(row["review"], REVIEW_META_KEYS, f"formal review metadata: {variant_id}")
            require(isinstance(review["reviewed_as_of"], str) and DATE_RE.fullmatch(review["reviewed_as_of"]), f"formal review date invalid: {variant_id}")
            require(nonempty(review["reviewer_id"], f"formal reviewer: {variant_id}") and review["manual_statement_review"] is True and review["manual_formal_variant_semantic_review"] is True and review["manual_filename_declaration_anomaly_review"] is True and isinstance(review["notes"], str), f"formal manual review gates fail: {variant_id}")
            require(row["candidate_only"] is True and row["grants_catalog_entry"] is False and row["grants_theorem_credit"] is False, f"formal review credit boundary drifted: {variant_id}")
            occurrences[variant_id].append(row)
    result: dict[str, dict[str, Any]] = {}
    for variant_id, rows in occurrences.items():
        require(all(row == rows[0] for row in rows), f"conflicting duplicate formal reviews: {variant_id}")
        result[variant_id] = rows[0]
    return result


def final_seed_semantics(repo_root: Path) -> dict[str, set[str]]:
    collection = seed.collect_reviews(repo_root)
    rows = seed.build_crosswalk_rows(repo_root, collection)
    payload = seed.encoded_jsonl(rows)
    path = repo_root / SEED_CROSSWALK_REL
    require(path.is_file() and path.read_bytes() == payload, "complete seed crosswalk is absent or differs from reviewed source rows")
    return {
        str(row["problem_key"]): {str(target["semantic_key"]) for target in row["targets"]}
        for row in rows
    }


def build_final_rows(repo_root: Path, queue: Sequence[Mapping[str, Any]], reviews: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    queue_by_id = {str(row["variant_id"]): row for row in queue}
    require(len(reviews) == EXPECTED_VARIANTS and set(reviews) == set(queue_by_id), f"formal review denominator incomplete: reviewed={len(reviews)}/1724 missing={EXPECTED_VARIANTS-len(reviews)}")
    semantics = final_seed_semantics(repo_root)
    all_semantics = set().union(*semantics.values())
    rows: list[dict[str, Any]] = []
    for queue_row in queue:
        variant_id = str(queue_row["variant_id"])
        review = reviews[variant_id]
        semantic_problem = review["semantic_problem_key"]
        require(semantic_problem in semantics, f"formal review maps outside full seed grid: {variant_id}")
        targets = review["target_semantic_keys"]
        if review["disposition"] == "malformed_or_nonclaim_variant":
            require(not targets, f"malformed formal review targets benchmark semantics: {variant_id}")
        else:
            require(targets and set(targets) <= semantics[semantic_problem] and set(targets) <= all_semantics, f"formal review targets wrong seed semantics: {variant_id}")
        final = {
            "schema_version": "awesome-theorems/putnambench-formal-crosswalk-row/5.6",
            "variant_id": variant_id,
            "source_variant_row_sha256": queue_row["source_variant_row_sha256"],
            "source_problem_key": queue_row["source_problem_key"],
            "semantic_problem_key": semantic_problem,
            "disposition": review["disposition"],
            "target_semantic_keys": list(targets),
            "statement_equivalence": copy.deepcopy(review["statement_equivalence"]),
            "review": copy.deepcopy(review["review"]),
        }
        rows.append(seal(final))
    return rows


def build_progress(repo_root: Path, queue: Sequence[Mapping[str, Any]], collection: Mapping[str, Any], reviews: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    variant_ids = {str(row["variant_id"]) for row in queue}
    missing_reviews = sorted(variant_ids - set(reviews))
    languages = Counter(str(row["language"]) for row in queue)
    anomalies = [row for row in queue if row["upstream_filename_declaration_anomalies"]]
    reviewed_seed_variants = sum(row["seed_review_state"] == "reviewed_semantic_targets_available" for row in queue)
    seed_complete = len(collection["selected"]) == 768
    progress: dict[str, Any] = {
        "schema_version": "awesome-theorems/putnam-formal-variant-crosswalk-progress/5.6",
        "as_of": "2026-08-10",
        "inputs": {
            "formal_variants": {"path": VARIANTS_REL.as_posix(), "rows": 1724, "sha256": VARIANTS_SHA},
            "formal_declaration_assets": {"path": ASSETS_REL.as_posix(), "rows": 1724, "sha256": ASSETS_SHA},
            "seed_crosswalk_progress_authority_sha256": seed.build_progress(repo_root, collection)["authority_sha256"],
            "manual_formal_review_directory": REVIEW_DIR_REL.as_posix(),
        },
        "counts": {
            "formal_variant_rows": 1724,
            "formal_variants_by_language": dict(sorted(languages.items())),
            "explicit_upstream_filename_declaration_anomalies": len(anomalies),
            "variants_with_reviewed_seed_semantic_options": reviewed_seed_variants,
            "variants_waiting_for_seed_review": 1724 - reviewed_seed_variants,
            "manual_formal_variant_reviews": len(reviews),
            "missing_manual_formal_variant_reviews": len(missing_reviews),
            "catalog_entries_granted": 0,
            "theorem_credits_granted": 0,
        },
        "explicit_anomalies": [
            {
                "variant_id": row["variant_id"],
                "source_problem_key": row["source_problem_key"],
                "language": row["language"],
                "anomaly_codes": row["upstream_filename_declaration_anomalies"],
                "declared_name": row["formal_declaration"]["declared_name"],
                "expected_name": row["formal_declaration"]["expected_name"],
                "declared_name_problem_key_candidate": row["declared_name_problem_key_candidate"],
                "semantic_mapping_inferred": False,
            }
            for row in anomalies
        ],
        "missing_review_variant_ids": missing_reviews,
        "set_digests": {
            "formal_variant_id_set_sha256": set_digest(variant_ids),
            "queue_row_sha256_set_sha256": set_digest(str(row["row_sha256"]) for row in queue),
            "manual_review_variant_id_set_sha256": set_digest(reviews),
            "explicit_anomaly_variant_id_set_sha256": set_digest(str(row["variant_id"]) for row in anomalies),
        },
        "gates": {
            "all_1724_frozen_variants_bound": True,
            "five_upstream_filename_declaration_anomalies_explicit": len(anomalies) == 5,
            "no_semantic_mapping_inferred_from_filename_or_declaration_name": True,
            "complete_768_seed_crosswalk_present": seed_complete and (repo_root / SEED_CROSSWALK_REL).is_file(),
            "all_1724_manual_semantic_reviews_present": not missing_reviews,
            "formal_variant_crosswalk_write_authorized": seed_complete and (repo_root / SEED_CROSSWALK_REL).is_file() and not missing_reviews,
        },
        "publication_boundary": {
            "queue_and_progress_only": True,
            "formal_variants_grant_catalog_credit": False,
            "proof_holes_grant_proof_credit": False,
            "missing_reviews_fabricated": False,
        },
        "findings": [
            *([] if seed_complete else [f"incomplete seed review denominator: {len(collection['selected'])}/768"]),
            *([] if not missing_reviews else [f"incomplete formal semantic review denominator: {len(reviews)}/1724"]),
        ],
    }
    progress["authority_sha256"] = hash_without(progress, "authority_sha256")
    return progress


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fchmod(stream.fileno(), 0o644)
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def run(args: argparse.Namespace) -> int:
    repo_root = args.repo_root.resolve()
    queue, collection = build_queue(repo_root)
    queue_by_id = {str(row["variant_id"]): row for row in queue}
    reviews = load_manual_reviews(repo_root, queue_by_id)
    progress = build_progress(repo_root, queue, collection, reviews)
    queue_payload = encoded_jsonl(queue)
    progress_payload = encoded_json(progress)
    if args.write_queue:
        atomic_write(repo_root / QUEUE_REL, queue_payload)
        atomic_write(repo_root / PROGRESS_REL, progress_payload)
        action = "WROTE QUEUE"
    elif args.check_queue:
        require((repo_root / QUEUE_REL).is_file() and (repo_root / QUEUE_REL).read_bytes() == queue_payload, "formal queue bytes drifted")
        require((repo_root / PROGRESS_REL).is_file() and (repo_root / PROGRESS_REL).read_bytes() == progress_payload, "formal progress bytes drifted")
        action = "PASS QUEUE"
    else:
        rows = build_final_rows(repo_root, queue, reviews)
        payload = encoded_jsonl(rows)
        if args.write_crosswalk:
            atomic_write(repo_root / CROSSWALK_REL, payload)
            action = "WROTE CROSSWALK"
        else:
            require((repo_root / CROSSWALK_REL).is_file() and (repo_root / CROSSWALK_REL).read_bytes() == payload, "formal crosswalk bytes drifted")
            action = "PASS CROSSWALK"
    print(
        f"{action} variants=1724 seed_options={progress['counts']['variants_with_reviewed_seed_semantic_options']} "
        f"manual_reviews={len(reviews)}/1724 anomalies=5 "
        f"authority={progress['authority_sha256']}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-queue", action="store_true")
    mode.add_argument("--check-queue", action="store_true")
    mode.add_argument("--write-crosswalk", action="store_true")
    mode.add_argument("--check-crosswalk", action="store_true")
    parser.add_argument("--repo-root", type=Path, default=REPO)
    args = parser.parse_args()
    try:
        return run(args)
    except (FormalCrosswalkError, seed.CrosswalkError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"FAIL Putnam formal-variant crosswalk: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
