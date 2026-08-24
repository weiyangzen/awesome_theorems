#!/usr/bin/env python3
"""Aggregate completed human frontier reviews into formal Stage5.5 credit.

The input reviews deliberately grant no release credit.  This builder is the
single promotion point: it requires complete coverage of both frozen candidate
universes, rechecks every acceptance gate, deduplicates exact identities and
semantic keys across all batches, keeps the important-theorem quota disjoint,
and emits between 500 and 1,000 existing-parent frontier credits.  It creates
no theorem identities and does not mutate a release.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


REPO_ROOT = Path(__file__).resolve().parents[4]
V5 = REPO_ROOT / "Docs/catalog/v5"
REVIEW_DIR = V5 / "curation/frontier_theorem_reviews_v5_5"
CATALOG = V5 / "releases/5.4/Claim_Catalog.json"
MANIFEST = V5 / "releases/5.4/Release_Manifest.json"
IMPORTANT = V5 / "curation/theorem_quality_v5_5/mathlib-important-inventory-1000.json"
OUTPUT = V5 / "curation/Frontier_Theorem_Qualification_v5_5.json"
ERDOS_PRIMARY_QUEUE = V5 / "curation/erdos_parent_join_v5_5/resolved-theorem-max2-selected.jsonl"
ERDOS_SUPPLEMENTAL_QUEUE = V5 / "curation/erdos_parent_join_v5_5/resolved-theorem-supplemental.jsonl"
NONERDOS_PRIMARY_QUEUE = V5 / "curation/Frontier_Theorem_Candidate_Queue_v5_5.json"
NONERDOS_SUPPLEMENTAL_QUEUE = V5 / "curation/Frontier_Theorem_Supplemental_Candidate_Queue_v5_5.json"

PARENT_ROOT = "c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813"
PARENT_CATALOG_SHA = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
PARENT_MANIFEST_SHA = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
ERDOS_PRIMARY_QUEUE_SHA = "a65f8e9841dd415894cbfc5f032283fa05e4bd1161c6bd4c8a4ae3e9e0e64cae"
ERDOS_SUPPLEMENTAL_QUEUE_SHA = "6d31bf21d1182e3d1dd908fa27d552340fcb6169636541b04fbf26ea1a7e65a7"
NONERDOS_PRIMARY_QUEUE_SHA = "b3b28b81cfcd9fe4dbf002d2bb8d9bedaa8094656396e224abb5c6221530b2fc"
NONERDOS_SUPPLEMENTAL_QUEUE_SHA = "78c2d8e1e4068d59bf0471ecca9071fc139bb3300525df0aab8348718cbdc135"
MIN_CREDITS = 500
MAX_CREDITS = 1_000


class QualificationError(RuntimeError):
    pass


def reject_constant(token: str) -> None:
    raise QualificationError(f"non-finite JSON token is forbidden: {token}")


def closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return digest(canonical({key: item for key, item in value.items() if key not in omitted}))


def set_digest(values: Iterable[str]) -> str:
    return digest(canonical(sorted(values)))


def seal(value: Mapping[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result.pop("authority_sha256", None)
    result["authority_sha256"] = without(result, "authority_sha256")
    return result


def require(condition: bool, message: str) -> None:
    if not condition:
        raise QualificationError(message)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=closed_object,
        parse_constant=reject_constant,
    )
    require(isinstance(value, dict), f"{path} is not a JSON object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    payload = path.read_bytes()
    require(payload.endswith(b"\n"), f"{path} lacks terminal LF")
    rows: list[dict[str, Any]] = []
    for index, line in enumerate(payload.splitlines()):
        try:
            row = json.loads(
                line,
                object_pairs_hook=closed_object,
                parse_constant=reject_constant,
            )
        except json.JSONDecodeError as error:
            raise QualificationError(f"{path}:{index + 1}: invalid JSON: {error}") from error
        require(isinstance(row, dict), f"{path}:{index + 1} is not an object")
        # Review batches predate the unified qualification and intentionally
        # preserve their own deterministic key order.  Their exact file bytes
        # and per-row canonical digest are bound below; imposing this builder's
        # key order here would rewrite otherwise independently checked evidence.
        rows.append(row)
    return rows


def review_paths() -> list[Path]:
    paths = sorted(REVIEW_DIR.glob("*.jsonl"), key=lambda path: path.name.encode("utf-8"))
    require(paths, "no frontier review ledgers found")
    allowed_prefixes = ("erdos_", "nonerdos_")
    require(all(path.name.startswith(allowed_prefixes) for path in paths), "unexpected review JSONL")
    return paths


def all_pass(gates: Any) -> bool:
    if not isinstance(gates, dict) or not gates:
        return False
    for value in gates.values():
        if isinstance(value, bool):
            if value is not True:
                return False
        elif isinstance(value, dict):
            if value.get("pass") is True:
                continue
            if value.get("verdict") == "pass":
                continue
            return False
        else:
            return False
    return True


def candidate_identity(candidate: Mapping[str, Any], erdos: bool) -> tuple[Any, Any, Any]:
    if erdos:
        parent = candidate.get("parent")
        identity = candidate.get("identity")
        require(isinstance(parent, dict) and isinstance(identity, dict), "Erdos queue row identity malformed")
        return (
            parent.get("stage_claim_id"),
            parent.get("variant_id"),
            identity.get("semantic_identity_key"),
        )
    return candidate.get("stage_claim_id"), candidate.get("variant_id"), candidate.get("semantic_key")


def normalize(
    path: Path,
    line_index: int,
    row: Mapping[str, Any],
    queues: Mapping[str, Mapping[int, Mapping[str, Any]]],
) -> dict[str, Any]:
    erdos = path.name.startswith("erdos_")
    if erdos:
        identity = row.get("identity")
        source = row.get("source_binding")
        require(isinstance(identity, dict) and isinstance(source, dict), f"{path}:{line_index + 1} malformed")
        candidate_index = source.get("zero_based_row")
        stage_id = identity.get("stage_claim_id")
        variant_id = identity.get("variant_id")
        semantic = identity.get("semantic_identity_key")
        decision = row.get("decision")
        accepted = decision == "accept" and row.get("all_gates_pass") is True and all_pass(row.get("gates"))
        lane = "erdos_supplemental" if "supplemental" in path.name else "erdos_primary"
        credit = row.get("credit")
        require(
            isinstance(credit, dict)
            and credit.get("frontier_theorem_credit_granted") is False
            and credit.get("new_theorem_credit_granted") is False
            and credit.get("release_modified") is False,
            f"{path}:{line_index + 1} review credit boundary drifted",
        )
        if lane == "erdos_supplemental":
            candidate_index = row.get("supplemental_index", row.get("supplemental_rank", candidate_index))
        rights = row.get("rights_boundary")
        references = [
            value.get("evidence")
            for key, value in row.get("gates", {}).items()
            if key == "primary_resolution" and isinstance(value, dict)
        ]
    else:
        candidate_index = row.get("candidate_rank")
        stage_id = row.get("stage_claim_id")
        variant_id = row.get("variant_id")
        semantic = row.get("semantic_key")
        decision = row.get("decision")
        accepted = decision == "eligible_existing_frontier_credit" and all_pass(row.get("gates"))
        lane = "nonerdos_supplemental" if "supplemental" in path.name else "nonerdos_primary"
        require(row.get("grants_new_theorem_credit") is False, f"{path}:{line_index + 1} invents theorem credit")
        if lane == "nonerdos_supplemental":
            require(row.get("grants_frontier_credit") is False, f"{path}:{line_index + 1} supplemental self-grants formal credit")
            require(
                row.get("review_eligible_frontier_credit") is accepted,
                f"{path}:{line_index + 1} supplemental eligibility flag drifted",
            )
        else:
            require(
                row.get("grants_frontier_credit") is accepted,
                f"{path}:{line_index + 1} primary review eligibility flag drifted",
            )
        rights = {
            "review_finding": row.get("rights_finding"),
            "gate": row.get("gates", {}).get("rights"),
        }
        references = row.get("primary_references", row.get("primary_resolution_references", []))
    require(isinstance(candidate_index, int) and not isinstance(candidate_index, bool), f"{path}:{line_index + 1} index malformed")
    require(isinstance(stage_id, str) and stage_id.startswith("S5-CLM-"), f"{path}:{line_index + 1} S5 ID malformed")
    require(isinstance(variant_id, str) and variant_id.startswith("ATV-"), f"{path}:{line_index + 1} ATV ID malformed")
    require(isinstance(semantic, str) and semantic, f"{path}:{line_index + 1} semantic key missing")
    candidate = queues[lane].get(candidate_index)
    require(candidate is not None, f"{path}:{line_index + 1} has no frozen queue row")
    expected_sid, expected_atv, expected_semantic = candidate_identity(candidate, erdos)
    require(
        (stage_id, variant_id, semantic) == (expected_sid, expected_atv, expected_semantic),
        f"{path}:{line_index + 1} identity differs from frozen queue",
    )
    if erdos:
        source = row["source_binding"]
        if source.get("row_sha256") is not None:
            require(
                source.get("row_sha256") == digest(canonical(candidate)),
                f"{path}:{line_index + 1} frozen Erdos queue row hash mismatch",
            )
    else:
        declared_queue_sha = row.get("queue_row_sha256", row.get("source_row_sha256"))
        require(
            declared_queue_sha == candidate.get("row_sha256"),
            f"{path}:{line_index + 1} frozen non-Erdos queue row hash mismatch",
        )
    declared_hash = row.get("row_sha256", row.get("review_row_sha256"))
    if declared_hash is not None:
        field = "row_sha256" if "row_sha256" in row else "review_row_sha256"
        require(declared_hash == without(row, field), f"{path}:{line_index + 1} row hash stale")
    review_row_sha = digest(canonical(row))
    return {
        "lane": lane,
        "candidate_index": candidate_index,
        "stage_claim_id": stage_id,
        "variant_id": variant_id,
        "semantic_key": semantic,
        "decision": decision,
        "accepted": accepted,
        "all_gates_pass": all_pass(row.get("gates")) and (row.get("all_gates_pass", True) is True),
        "rights_evidence": rights,
        "primary_references": references,
        "review_binding": {
            "path": path.relative_to(REPO_ROOT).as_posix(),
            "file_sha256": sha_file(path),
            "line_number": line_index + 1,
            "review_row_sha256": review_row_sha,
        },
    }


def verify_coverage(rows: list[dict[str, Any]]) -> None:
    by_lane: dict[str, list[int]] = {}
    for row in rows:
        by_lane.setdefault(str(row["lane"]), []).append(int(row["candidate_index"]))
    expected = {
        "erdos_primary": set(range(379)),
        "erdos_supplemental": set(range(167)),
        "nonerdos_primary": set(range(1, 255)),
        "nonerdos_supplemental": set(range(255, 372)),
    }
    require(set(by_lane) == set(expected), f"frontier lanes incomplete: {sorted(by_lane)}")
    for lane, wanted in expected.items():
        observed = by_lane[lane]
        require(set(observed) == wanted and len(observed) == len(wanted), f"{lane} coverage differs")


def build() -> dict[str, Any]:
    require(sha_file(CATALOG) == PARENT_CATALOG_SHA, "parent catalog drifted")
    require(sha_file(MANIFEST) == PARENT_MANIFEST_SHA, "parent manifest drifted")
    catalog = load_json(CATALOG)
    manifest = load_json(MANIFEST)
    require(manifest.get("release_root_sha256") == PARENT_ROOT, "parent release root drifted")
    important = load_json(IMPORTANT)
    require(important.get("authority_sha256") == without(important, "authority_sha256"), "important authority stale")
    important_ids = {row["stage_claim_id"] for row in important.get("records", [])}
    require(len(important_ids) == 1_000, "important denominator drifted")
    parent_theorems = {
        row["stage_claim_id"]: row
        for row in catalog.get("records", [])
        if row.get("current_claim_kind") == "theorem" and row.get("material_status") == "proved"
    }
    require(len(parent_theorems) == 2_500, "parent theorem denominator drifted")

    require(sha_file(ERDOS_PRIMARY_QUEUE) == ERDOS_PRIMARY_QUEUE_SHA, "Erdos primary queue drifted")
    require(sha_file(ERDOS_SUPPLEMENTAL_QUEUE) == ERDOS_SUPPLEMENTAL_QUEUE_SHA, "Erdos supplemental queue drifted")
    require(sha_file(NONERDOS_PRIMARY_QUEUE) == NONERDOS_PRIMARY_QUEUE_SHA, "non-Erdos primary queue drifted")
    require(sha_file(NONERDOS_SUPPLEMENTAL_QUEUE) == NONERDOS_SUPPLEMENTAL_QUEUE_SHA, "non-Erdos supplemental queue drifted")
    erdos_primary_rows = load_jsonl(ERDOS_PRIMARY_QUEUE)
    erdos_supplemental_rows = load_jsonl(ERDOS_SUPPLEMENTAL_QUEUE)
    nonerdos_primary_document = load_json(NONERDOS_PRIMARY_QUEUE)
    nonerdos_supplemental_document = load_json(NONERDOS_SUPPLEMENTAL_QUEUE)
    nonerdos_primary_rows = nonerdos_primary_document.get("records")
    nonerdos_supplemental_rows = nonerdos_supplemental_document.get("records")
    require(isinstance(nonerdos_primary_rows, list) and len(nonerdos_primary_rows) == 254, "non-Erdos primary queue denominator drifted")
    require(isinstance(nonerdos_supplemental_rows, list) and len(nonerdos_supplemental_rows) == 117, "non-Erdos supplemental queue denominator drifted")
    require(len(erdos_primary_rows) == 379 and len(erdos_supplemental_rows) == 167, "Erdos queue denominator drifted")
    queues: dict[str, dict[int, Mapping[str, Any]]] = {
        "erdos_primary": {index: row for index, row in enumerate(erdos_primary_rows)},
        "erdos_supplemental": {index: row for index, row in enumerate(erdos_supplemental_rows)},
        "nonerdos_primary": {int(row["candidate_rank"]): row for row in nonerdos_primary_rows},
        "nonerdos_supplemental": {int(row["candidate_rank"]): row for row in nonerdos_supplemental_rows},
    }

    normalized: list[dict[str, Any]] = []
    inputs: list[dict[str, Any]] = []
    for path in review_paths():
        rows = load_jsonl(path)
        require(rows, f"empty frontier review: {path.name}")
        inputs.append(
            {
                "path": path.relative_to(REPO_ROOT).as_posix(),
                "file_sha256": sha_file(path),
                "size_bytes": path.stat().st_size,
                "rows": len(rows),
            }
        )
        normalized.extend(normalize(path, index, row, queues) for index, row in enumerate(rows))
    verify_coverage(normalized)

    accepted = [row for row in normalized if row["accepted"]]
    accepted.sort(
        key=lambda row: (
            {"erdos_primary": 0, "erdos_supplemental": 1, "nonerdos_primary": 2, "nonerdos_supplemental": 3}[row["lane"]],
            int(row["candidate_index"]),
            str(row["stage_claim_id"]),
        )
    )
    seen_stage: set[str] = set()
    seen_variant: set[str] = set()
    seen_semantic: set[str] = set()
    credits: list[dict[str, Any]] = []
    for source in accepted:
        sid = str(source["stage_claim_id"])
        atv = str(source["variant_id"])
        semantic = str(source["semantic_key"])
        require(sid in parent_theorems, f"accepted frontier identity is not a parent theorem: {sid}")
        require(sid not in important_ids, f"frontier quota double-counts important theorem: {sid}")
        require(sid not in seen_stage and atv not in seen_variant, f"frontier identity duplicate: {sid}")
        require(semantic not in seen_semantic, f"frontier semantic duplicate remains: {semantic}")
        row = {
            "accepted_rank": len(credits) + 1,
            "stage_claim_id": sid,
            "variant_id": atv,
            "semantic_key": semantic,
            "source_lane": source["lane"],
            "source_candidate_index": source["candidate_index"],
            "decision": "accept",
            "all_gates_pass": True,
            "rights_evidence": source["rights_evidence"],
            "primary_references": source["primary_references"],
            "review_binding": source["review_binding"],
            "grants_frontier_theorem_credit": True,
            "grants_new_theorem_identity_credit": False,
        }
        row["row_sha256"] = without(row, "row_sha256")
        credits.append(row)
        seen_stage.add(sid)
        seen_variant.add(atv)
        seen_semantic.add(semantic)
    require(MIN_CREDITS <= len(credits) <= MAX_CREDITS, f"accepted frontier count {len(credits)} misses gate")

    result = {
        "schema_version": "awesome-theorems/frontier-theorem-qualification/5.5",
        "review_as_of": "2026-08-10",
        "parent": {
            "release": "5.4",
            "release_root_sha256": PARENT_ROOT,
            "claim_catalog_sha256": PARENT_CATALOG_SHA,
            "release_manifest_sha256": PARENT_MANIFEST_SHA,
        },
        "scope": {
            "existing_parent_theorem_quality_credit_only": True,
            "creates_new_theorem_identities": False,
            "important_and_frontier_quota_sets_disjoint": True,
            "candidate_or_pending_rows_receive_credit": False,
        },
        "inputs": {
            "review_ledgers": inputs,
            "candidate_queues": [
                {"path": path.relative_to(REPO_ROOT).as_posix(), "file_sha256": sha_file(path), "rows": rows}
                for path, rows in (
                    (ERDOS_PRIMARY_QUEUE, 379),
                    (ERDOS_SUPPLEMENTAL_QUEUE, 167),
                    (NONERDOS_PRIMARY_QUEUE, 254),
                    (NONERDOS_SUPPLEMENTAL_QUEUE, 117),
                )
            ],
            "important_inventory": {
                "path": IMPORTANT.relative_to(REPO_ROOT).as_posix(),
                "file_sha256": sha_file(IMPORTANT),
                "authority_sha256": important["authority_sha256"],
                "rows": 1_000,
            },
        },
        "accepted_credits": credits,
        "counts": {
            "review_rows": len(normalized),
            "review_accepted_before_global_dedupe": len(accepted),
            "accepted_additional_frontier_theorems": len(credits),
            "accepted_distinct_important_landmarks": 1_000,
            "new_theorem_identity_credits": 0,
            "unsupported_importance_or_frontier_credit": 0,
            "pending_not_credited": sum(row["decision"] == "pending" for row in normalized),
            "rejected_not_credited": sum(row["decision"] == "reject" for row in normalized),
        },
        "set_digests": {
            "accepted_stage_claim_id_set_sha256": set_digest(row["stage_claim_id"] for row in credits),
            "accepted_variant_id_set_sha256": set_digest(row["variant_id"] for row in credits),
            "accepted_semantic_key_set_sha256": set_digest(row["semantic_key"] for row in credits),
            "accepted_row_sha256_set_sha256": set_digest(row["row_sha256"] for row in credits),
        },
    }
    return seal(result)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    document = build()
    payload = canonical(document) + b"\n"
    if args.check:
        require(args.output.is_file() and args.output.read_bytes() == payload, "frontier qualification missing or stale")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(payload)
    print(
        "PASS frontier theorem qualification "
        f"reviewed={document['counts']['review_rows']} "
        f"accepted={document['counts']['accepted_additional_frontier_theorems']} "
        f"authority={document['authority_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
