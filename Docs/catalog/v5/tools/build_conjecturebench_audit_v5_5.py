#!/usr/bin/env python3
"""Deterministically build the repository-owned ConjectureBench v5.5 audit.

The generated ledger is a conservative candidate audit, not a release update:
no row is accepted and no strict-conjecture credit is granted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
CURATION_REL = Path("Docs/catalog/v5/curation/conjecturebench_v5_5")
CURATION_DEFAULT = REPO_ROOT / CURATION_REL

INPUTS = {
    "source_archive": (Path("Docs/catalog/v5/sources/conjecturebench-357bcb1a-source.tar.gz"), "9f598326e7d83011630d77eb0ef309aabd4112eb803a7debe0ec6076937912fe"),
    "source_manifest": (Path("Docs/catalog/v5/sources/conjecturebench-357bcb1a-source-manifest.json"), "b1337e5f7455d680c42fa55ac4a141b573fe5d044137cca101faf5a8eae7263b"),
    "source_asset": (Path("Docs/catalog/v5/sources/conjecturebench-357bcb1a-curated-302.jsonl"), "0efbd15dec93a9499644db5324c63ee02631732a295ce583ab7229e4e2e6291a"),
    "mechanical_screen": (CURATION_REL / "mechanical-screen.jsonl", "380c9064f95ebd0a6078eeb6614a2c7f109fe380c70c31cba1571aab8c411559"),
    "parent_relations": (CURATION_REL / "parent-stable-identity-relations.jsonl", "02a57dcb208aca531270d6bedad170b510a96a0de1845c85edc773ef231ac763"),
    "parent_exclusions": (CURATION_REL / "parent-exact-and-status-drift-exclusions.jsonl", "f1c1ce17f65793d4b9400cab60464e5d826b6d4776552c483c2be60c452dc4ab"),
    "residual_candidates": (CURATION_REL / "remaining-manual-semantic-review.jsonl", "8ee48b0d1e5d67315a74321980067faca715ee35b1009fea3a521f4144c5787e"),
    "review_a": (CURATION_REL / "review-residual-000-094.jsonl", "27d1e8a5dadb51db3b3fb66851b5b7a2b0d3076f70934c38906ef608b64ce1c8"),
    "review_b": (CURATION_REL / "review-residual-095-189.jsonl", "4c57a9ecf46ff1a992af91b2ee086230a4335b9ac201364a4450cc5fec1440a5"),
    "status_drift": (CURATION_REL / "status-drift-2026-08-10.jsonl", "a5b4b0219f4fe1d622d6977c3a74dd6af488f61e242d830015c5dddb1a4956a4"),
    "parent_catalog": (Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json"), "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"),
    "parent_ledger": (Path("Docs/catalog/v5/releases/5.4/Strict_Conjecture_Ledger.json"), "52ba1ccf06462741bcc48028fb121e5e30d1e7b56128cfeb910dc56a2e1a83a3"),
    "release_manifest": (Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json"), "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"),
    "openconjecture": (Path("Docs/catalog/v5/sources/openconjecture-fa03d85-cc-by-real-conf090.jsonl"), "8a698e3af53ca0605a2a8ecd2e3a9944ad84157440a86f3c319effaf9792c6ce"),
    "oeis_all_conjectur": (Path("Docs/catalog/v5/sources/oeis-conjectures-4c866362-all-conjectur-v2.jsonl"), "18da1f5881f0410f2c38dc8362271b536db11c4509d58812942a11981181ec3d"),
}

GENERATED_NAMES = {
    "residual_reviews": "residual-review-190.jsonl",
    "residual_validation": "residual-review-validation.json",
    "ledger": "strict-review-ledger-302.jsonl",
    "summary": "final-audit-summary.json",
}

SOURCE_COMMIT = "357bcb1a1daf93917d42e8206ceaa55645729a09"
SOURCE_TREE = "ce1e057720604415124e20cf4c24486a4fd8cd30"


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    if any(not isinstance(row, dict) for row in rows):
        raise RuntimeError(f"non-object JSONL row: {path}")
    return rows


def base_pending(source: dict[str, Any], screen: dict[str, Any]) -> dict[str, Any]:
    status = source["source_status_observation"]
    contested = status["state"] == "status-contested"
    reason = "source_status_contested" if contested else "needs_independent_status_review"
    basis = (
        source["record"]["status_observation"].get("note")
        if contested
        else "ConjectureBench marks the status evidence as needs-independent-review; no strict admission gate may inherit an open finding from that label."
    )
    return {
        "schema_version": "conjecturebench-strict-review-v1",
        "cb_id": source["cb_id"],
        "decision": "pending",
        "reason_code": reason,
        "exact_claim_text": source["exact_statement"],
        "truth_apt": True,
        "context_complete": True,
        "source_asserted_open_as_of_record": status["state"] == "open",
        "current_open_as_of_2026_08_10": None,
        "importance_tier": "not_assessed",
        "importance_basis": "Deferred until the independent source/status gate is complete.",
        "duplicate_targets": [],
        "review_basis": basis,
        "source_review": "record_replayed_at_pinned_commit; independent status/source review incomplete",
        "rights_review": "pending_source_specific_review",
        "status_drift_evidence": None,
        "acceptance_evidence_complete": False,
        "grants_strict_conjecture_credit": False,
        "pending_gates": [
            "independent_current_open_status_cutoff_replay",
            "high_or_medium_importance",
            "source_specific_release_summary_and_attribution",
            "comprehensive_semantic_dedupe",
        ],
        "mechanical_screen": screen,
    }


def explicit_duplicate(source: dict[str, Any], screen: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "conjecturebench-strict-review-v1",
        "cb_id": source["cb_id"],
        "decision": "reject",
        "reason_code": "explicit_source_duplicate",
        "exact_claim_text": source["exact_statement"],
        "truth_apt": True,
        "context_complete": True,
        "source_asserted_open_as_of_record": True,
        "current_open_as_of_2026_08_10": None,
        "importance_tier": "not_assessed",
        "importance_basis": "Not assessed because explicit duplicate exclusion is prior.",
        "duplicate_targets": [f"conjecturebench/{source['duplicate_of']}"],
        "review_basis": "The pinned source record explicitly supplies duplicate_of.",
        "source_review": "record_replayed_at_pinned_commit",
        "rights_review": "not_required_after_prior_rejection",
        "status_drift_evidence": None,
        "acceptance_evidence_complete": False,
        "grants_strict_conjecture_credit": False,
        "pending_gates": [],
        "mechanical_screen": screen,
    }


def parent_exclusion(
    source: dict[str, Any], screen: dict[str, Any], evidence: list[dict[str, Any]], drift: dict[str, Any] | None
) -> dict[str, Any]:
    solved = any(row["exclusion_type"] == "status_drift_parent_now_solved" for row in evidence)
    targets = sorted({f"parent/{row['parent_stage_claim_id']}" for row in evidence})
    if solved:
        reason = "not_currently_open_parent_source_reports_solved"
        basis = (
            drift["relation_basis"] if drift is not None else
            "The stable upstream conjecture identity is explicitly theorem/proved in the pinned parent status snapshot."
        )
        status_evidence: dict[str, Any] | None = drift
    else:
        reason = "exact_parent_formal_declaration_duplicate"
        basis = (
            "The pinned Formal benchmark and parent use the same member path and declaration name, and their theorem/lemma declaration text is byte-identical after removing only the benchmark category attribute. This proves exact surface-form identity; it does not claim cross-revision kernel-expression equality."
        )
        status_evidence = None
    return {
        "schema_version": "conjecturebench-strict-review-v1",
        "cb_id": source["cb_id"],
        "decision": "reject",
        "reason_code": reason,
        "exact_claim_text": source["exact_statement"],
        "truth_apt": True,
        "context_complete": True,
        "source_asserted_open_as_of_record": True,
        "current_open_as_of_2026_08_10": False if solved else None,
        "importance_tier": "not_assessed",
        "importance_basis": "Not assessed because parent/status exclusion is prior.",
        "duplicate_targets": targets if not solved else [],
        "review_basis": basis,
        "source_review": "pinned ConjectureBench record and Formal-parent evidence replayed",
        "rights_review": "not_required_after_prior_rejection",
        "status_drift_evidence": status_evidence,
        "acceptance_evidence_complete": False,
        "grants_strict_conjecture_credit": False,
        "pending_gates": [],
        "mechanical_screen": screen,
        "parent_exclusion_evidence": evidence,
    }


def jsonl_bytes(rows: list[dict[str, Any]]) -> bytes:
    return b"".join(canonical(row) + b"\n" for row in rows)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def logical_path(name: str) -> str:
    return INPUTS[name][0].as_posix()


def merge_residual_reviews(
    candidates: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    review_a: list[dict[str, Any]],
    review_b: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], bytes, bytes]:
    if len(candidates) != 190:
        raise RuntimeError(f"residual candidate count mismatch: {len(candidates)}")
    source_by_id = {row["cb_id"]: row for row in sources}
    reviews = review_a + review_b
    indexed: list[tuple[int, dict[str, Any]]] = []
    for row in reviews:
        index = row.get("input_index", row.get("residual_index"))
        if type(index) is not int or not 0 <= index < len(candidates):
            raise RuntimeError(f"invalid residual index: {index!r}")
        indexed.append((index, row))
    indexed.sort(key=lambda item: item[0])
    if [index for index, _ in indexed] != list(range(190)):
        raise RuntimeError("residual review coverage is not exactly 0..189")

    ordered: list[dict[str, Any]] = []
    for index, row in indexed:
        candidate = candidates[index]
        cb_id = candidate["id"]
        source = source_by_id.get(cb_id)
        if source is None:
            raise RuntimeError(f"{cb_id}: source record missing")
        if row.get("cb_id") != cb_id:
            raise RuntimeError(f"{cb_id}: residual index/ID mismatch")
        if row.get("exact_claim_text") != candidate.get("statement") or row.get("exact_claim_text") != source.get("exact_statement"):
            raise RuntimeError(f"{cb_id}: residual exact-text mismatch")
        if row.get("input_sha256") != INPUTS["residual_candidates"][1]:
            raise RuntimeError(f"{cb_id}: residual input hash mismatch")
        if row.get("input_record_sha256") != sha256_bytes(canonical(candidate)):
            raise RuntimeError(f"{cb_id}: residual record hash mismatch")
        if row.get("decision") not in {"pending", "reject"}:
            raise RuntimeError(f"{cb_id}: acceptance is not authorized")
        if row.get("acceptance_evidence_complete") is not False or row.get("grants_strict_conjecture_credit") is not False:
            raise RuntimeError(f"{cb_id}: nonaccept grants acceptance or credit")
        if row.get("status_drift_evidence") is not None and not isinstance(row.get("status_drift_evidence"), dict):
            raise RuntimeError(f"{cb_id}: status drift evidence is not object/null")
        targets = row.get("duplicate_targets")
        if not isinstance(targets, list) or any(not isinstance(value, str) for value in targets):
            raise RuntimeError(f"{cb_id}: invalid duplicate targets")
        if targets and row.get("decision") != "reject":
            raise RuntimeError(f"{cb_id}: known duplicate is not rejected")
        if row.get("decision") == "pending" and targets:
            raise RuntimeError(f"{cb_id}: pending row carries duplicate targets")
        if row.get("current_open_as_of_2026_08_10") is False and row.get("decision") != "reject":
            raise RuntimeError(f"{cb_id}: non-open row is not rejected")
        encoded = canonical(row).decode("utf-8")
        if "/tmp/" in encoded or "/home/sansha/" in encoded:
            raise RuntimeError(f"{cb_id}: nonportable absolute path in review")
        ordered.append(row)

    decisions = Counter(row["decision"] for row in ordered)
    if decisions != Counter({"pending": 138, "reject": 52}):
        raise RuntimeError(f"unexpected residual decisions: {decisions}")
    payload = jsonl_bytes(ordered)
    receipt = {
        "schema_version": "conjecturebench-residual-review-consolidation-v2",
        "overall_pass": True,
        "issues": [],
        "inputs": {
            name: {"path": logical_path(name), "sha256": INPUTS[name][1]}
            for name in ("residual_candidates", "source_asset", "parent_catalog", "parent_ledger", "openconjecture", "oeis_all_conjectur")
        },
        "review_files": [
            {"path": logical_path("review_a"), "sha256": INPUTS["review_a"][1], "rows": len(review_a)},
            {"path": logical_path("review_b"), "sha256": INPUTS["review_b"][1], "rows": len(review_b)},
        ],
        "coverage": {
            "candidate_rows": len(candidates),
            "review_rows": len(ordered),
            "unique_review_indices": len(indexed),
            "exact_0_through_189": True,
        },
        "counts": {
            "decisions": dict(sorted(decisions.items())),
            "reason_codes": dict(sorted(Counter(row["reason_code"] for row in ordered).items())),
            "importance_tiers": dict(sorted(Counter(row["importance_tier"] for row in ordered).items())),
            "accepted": 0,
            "strict_credits_granted": 0,
        },
        "merged_output": {
            "path": (CURATION_REL / GENERATED_NAMES["residual_reviews"]).as_posix(),
            "sha256": sha256_bytes(payload),
            "rows": len(ordered),
        },
        "boundary": (
            "The 190 inputs are a conservative upper-bound queue after mechanical and exact Formal-parent exclusions. "
            "Rows remain non-credit unless every exact-source, current-status, high/medium-importance, source-specific-rights, "
            "atomicity, and comprehensive semantic-dedupe gate is independently evidenced."
        ),
    }
    receipt_bytes = canonical(receipt) + b"\n"
    return ordered, payload, receipt_bytes


def build(workspace: Path) -> dict[str, bytes]:
    paths = {name: workspace / relative for name, (relative, _) in INPUTS.items()}
    for name, path in paths.items():
        if not path.is_file():
            raise RuntimeError(f"missing pinned input {name}: {path}")
        observed = sha256(path)
        if observed != INPUTS[name][1]:
            raise RuntimeError(f"{name} hash mismatch: {observed}")

    sources = load_jsonl(paths["source_asset"])
    screens = load_jsonl(paths["mechanical_screen"])
    candidates = load_jsonl(paths["residual_candidates"])
    review_a = load_jsonl(paths["review_a"])
    review_b = load_jsonl(paths["review_b"])
    residual, residual_payload, residual_receipt = merge_residual_reviews(candidates, sources, review_a, review_b)
    exclusions = load_jsonl(paths["parent_exclusions"])
    drifts = load_jsonl(paths["status_drift"])
    source_by_id = {row["cb_id"]: row for row in sources}
    screen_by_id = {row["cb_id"]: row for row in screens}
    residual_by_id = {row["cb_id"]: row for row in residual}
    drift_by_id = {row["cb_id"]: row for row in drifts}
    exclusions_by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in exclusions:
        exclusions_by_id[row["cb_id"]].append(row)

    expected_ids = [f"cb-{index:04d}" for index in range(1, 303)]
    if [row["cb_id"] for row in sources] != expected_ids or [row["cb_id"] for row in screens] != expected_ids:
        raise RuntimeError("source/screen coverage or order mismatch")
    partitions = {
        "residual_review": set(residual_by_id),
        "parent_exclusion": set(exclusions_by_id),
        "explicit_source_duplicate": {
            row["cb_id"] for row in screens if row["mechanical_disposition"] == "explicit_source_duplicate"
        },
        "mechanical_status_quarantine": {
            row["cb_id"] for row in screens
            if row["mechanical_disposition"] in {"source_status_contested", "needs_independent_status_review"}
        },
    }
    for name_a, ids_a in partitions.items():
        for name_b, ids_b in partitions.items():
            if name_a < name_b and ids_a & ids_b:
                raise RuntimeError(f"partition overlap {name_a}/{name_b}: {sorted(ids_a & ids_b)}")
    union = set().union(*partitions.values())
    if union != set(expected_ids) or {key: len(value) for key, value in partitions.items()} != {
        "residual_review": 190,
        "parent_exclusion": 70,
        "explicit_source_duplicate": 2,
        "mechanical_status_quarantine": 40,
    }:
        raise RuntimeError("final partition coverage/count mismatch")

    rows: list[dict[str, Any]] = []
    for cb_id in expected_ids:
        source = source_by_id[cb_id]
        screen = screen_by_id[cb_id]
        if cb_id in residual_by_id:
            row = dict(residual_by_id[cb_id])
            partition = "residual_review"
        elif cb_id in exclusions_by_id:
            row = parent_exclusion(source, screen, exclusions_by_id[cb_id], drift_by_id.get(cb_id))
            partition = "parent_exclusion"
        elif cb_id in partitions["explicit_source_duplicate"]:
            row = explicit_duplicate(source, screen)
            partition = "explicit_source_duplicate"
        else:
            row = base_pending(source, screen)
            partition = "mechanical_status_quarantine"
        if row["exact_claim_text"] != source["exact_statement"]:
            raise RuntimeError(f"{cb_id}: final exact claim mismatch")
        if row["decision"] != "accept":
            if row["acceptance_evidence_complete"] is not False or row["grants_strict_conjecture_credit"] is not False:
                raise RuntimeError(f"{cb_id}: nonaccept grants credit")
        row["final_audit_partition"] = partition
        row["source_commit"] = SOURCE_COMMIT
        row["source_tree_sha1"] = SOURCE_TREE
        row["source_record_key"] = source["source_record_key"]
        row["source_record_raw_sha256"] = source["record_raw_sha256"]
        row["source_status_observation"] = source["source_status_observation"]
        row["rights_boundary"] = source["rights"]
        row["final_row_payload_sha256"] = hashlib.sha256(
            canonical({key: value for key, value in row.items() if key != "final_row_payload_sha256"})
        ).hexdigest()
        rows.append(row)

    decisions = Counter(row["decision"] for row in rows)
    partitions_count = Counter(row["final_audit_partition"] for row in rows)
    reasons = Counter(row["reason_code"] for row in rows)
    accepted = [row for row in rows if row["decision"] == "accept"]
    credits = [row for row in rows if row["grants_strict_conjecture_credit"]]
    if decisions != Counter({"pending": 178, "reject": 124}) or accepted or credits:
        raise RuntimeError(f"unexpected final outcome: {decisions}, accepted={len(accepted)}, credits={len(credits)}")

    ledger_payload = jsonl_bytes(rows)
    fixed_inputs = {
        name: {"path": relative.as_posix(), "sha256": expected}
        for name, (relative, expected) in INPUTS.items()
    }
    summary = {
        "schema_version": "conjecturebench-final-strict-audit-v1",
        "audit_cutoff_date": "2026-08-10",
        "source_commit": SOURCE_COMMIT,
        "source_tree_sha1": SOURCE_TREE,
        "inputs": fixed_inputs,
        "generated_artifacts": {
            "residual_reviews": {
                "path": (CURATION_REL / GENERATED_NAMES["residual_reviews"]).as_posix(),
                "rows": len(residual),
                "sha256": sha256_bytes(residual_payload),
                "size_bytes": len(residual_payload),
            },
            "residual_validation": {
                "path": (CURATION_REL / GENERATED_NAMES["residual_validation"]).as_posix(),
                "sha256": sha256_bytes(residual_receipt),
                "size_bytes": len(residual_receipt),
            },
        },
        "coverage": {
            "source_records": len(sources),
            "final_review_rows": len(rows),
            "exact_cb_0001_through_cb_0302": [row["cb_id"] for row in rows] == expected_ids,
            "partitions": dict(sorted(partitions_count.items())),
        },
        "outcome": {
            "decisions": dict(sorted(decisions.items())),
            "reason_codes": dict(sorted(reasons.items())),
            "accepted": len(accepted),
            "strict_credits_granted": len(credits),
            "release_entries_added": 0,
        },
        "ledger": {
            "path": (CURATION_REL / GENERATED_NAMES["ledger"]).as_posix(),
            "rows": len(rows),
            "sha256": sha256_bytes(ledger_payload),
            "size_bytes": len(ledger_payload),
        },
        "boundary": [
            "No candidate is automatically accepted.",
            "Acceptance requires a complete atomic proposition, high or medium importance, an exact pinned source, independently verified current-open evidence, source-specific rights and attribution, and comprehensive semantic deduplication.",
            "Source-recorded status observations and dates are preserved; later cutoff drift is recorded separately in status_drift_evidence.",
            "The defensible residual upper bound is 190 candidates; earlier bounds of 161, 162, and 172 are withdrawn because stable path and declaration name alone did not prove exact proposition identity.",
            "The 138 residual candidates and 40 mechanically quarantined records remain pending, not rejected or accepted.",
            "The 124 rejects comprise 2 explicit source duplicates, 70 parent/status exclusions, and 52 residual semantic/atomicity/status exclusions.",
            "The exact parent-duplicate test compares byte-identical Lean surface declarations after removing only the benchmark category attribute; it does not claim equality of fully elaborated kernel expressions across dependency revisions.",
            "Strict acceptance remains zero because no residual row has a complete independently authored release summary/attribution packet plus comprehensive current-status and proposition-level dedupe evidence.",
            "The parent release 5.4 is an input only and is not modified by this audit.",
        ],
    }
    summary_payload = canonical(summary) + b"\n"
    outputs = {
        GENERATED_NAMES["residual_reviews"]: residual_payload,
        GENERATED_NAMES["residual_validation"]: residual_receipt,
        GENERATED_NAMES["ledger"]: ledger_payload,
        GENERATED_NAMES["summary"]: summary_payload,
    }
    for name, payload in outputs.items():
        decoded = payload.decode("utf-8")
        if "/tmp/" in decoded or "/home/sansha/" in decoded:
            raise RuntimeError(f"generated artifact contains a nonportable absolute path: {name}")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=REPO_ROOT)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--write", action="store_true", help="write deterministic outputs; otherwise compare existing bytes")
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    output = args.output_dir.resolve() if args.output_dir else workspace / CURATION_REL
    outputs = build(workspace)
    if args.write:
        output.mkdir(parents=True, exist_ok=True)
        for name, payload in outputs.items():
            (output / name).write_bytes(payload)
    else:
        for name, payload in outputs.items():
            path = output / name
            if not path.is_file() or path.read_bytes() != payload:
                raise RuntimeError(f"generated artifact mismatch: {path}")
    result = {
        "mode": "write" if args.write else "check",
        "output_dir": CURATION_REL.as_posix() if output == workspace / CURATION_REL else str(output),
        "artifacts": {
            name: {"sha256": sha256_bytes(payload), "size_bytes": len(payload)}
            for name, payload in sorted(outputs.items())
        },
        "outcome": {"pending": 178, "reject": 124, "accepted": 0, "strict_credit": 0},
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
