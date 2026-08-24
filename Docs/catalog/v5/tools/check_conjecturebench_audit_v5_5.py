#!/usr/bin/env python3
"""Independently validate the repository-owned ConjectureBench v5.5 audit."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[4]
CURATION_REL = Path("Docs/catalog/v5/curation/conjecturebench_v5_5")
SOURCE_PREFIX = "conjecturebench-357bcb1a/"
SOURCE_COMMIT = "357bcb1a1daf93917d42e8206ceaa55645729a09"
SOURCE_TREE = "ce1e057720604415124e20cf4c24486a4fd8cd30"
EXPECTED_IDS = [f"cb-{number:04d}" for number in range(1, 303)]
EXPECTED_PARTITIONS = {
    "explicit_source_duplicate": 2,
    "mechanical_status_quarantine": 40,
    "parent_exclusion": 70,
    "residual_review": 190,
}
EXPECTED_DECISIONS = {"pending": 178, "reject": 124}

FIXED = {
    "source_archive": (Path("Docs/catalog/v5/sources/conjecturebench-357bcb1a-source.tar.gz"), "9f598326e7d83011630d77eb0ef309aabd4112eb803a7debe0ec6076937912fe"),
    "source_manifest": (Path("Docs/catalog/v5/sources/conjecturebench-357bcb1a-source-manifest.json"), "b1337e5f7455d680c42fa55ac4a141b573fe5d044137cca101faf5a8eae7263b"),
    "source_asset": (Path("Docs/catalog/v5/sources/conjecturebench-357bcb1a-curated-302.jsonl"), "0efbd15dec93a9499644db5324c63ee02631732a295ce583ab7229e4e2e6291a"),
    "mechanical_screen": (CURATION_REL / "mechanical-screen.jsonl", "380c9064f95ebd0a6078eeb6614a2c7f109fe380c70c31cba1571aab8c411559"),
    "parent_relations": (CURATION_REL / "parent-stable-identity-relations.jsonl", "02a57dcb208aca531270d6bedad170b510a96a0de1845c85edc773ef231ac763"),
    "parent_exclusions": (CURATION_REL / "parent-exact-and-status-drift-exclusions.jsonl", "f1c1ce17f65793d4b9400cab60464e5d826b6d4776552c483c2be60c452dc4ab"),
    "residual_candidates": (CURATION_REL / "remaining-manual-semantic-review.jsonl", "8ee48b0d1e5d67315a74321980067faca715ee35b1009fea3a521f4144c5787e"),
    "review_a": (CURATION_REL / "review-residual-000-094.jsonl", "27d1e8a5dadb51db3b3fb66851b5b7a2b0d3076f70934c38906ef608b64ce1c8"),
    "review_b": (CURATION_REL / "review-residual-095-189.jsonl", "4c57a9ecf46ff1a992af91b2ee086230a4335b9ac201364a4450cc5fec1440a5"),
    "residual_reviews": (CURATION_REL / "residual-review-190.jsonl", "022191ca07acac80873b0418af27b2f3d9e33374ea397bc07f5c8d61f25db585"),
    "residual_validation": (CURATION_REL / "residual-review-validation.json", "867a21e7113f1ff5123b0646f041107fede23f876c00b7b986511bf13e4a40b9"),
    "status_drift": (CURATION_REL / "status-drift-2026-08-10.jsonl", "a5b4b0219f4fe1d622d6977c3a74dd6af488f61e242d830015c5dddb1a4956a4"),
    "ledger": (CURATION_REL / "strict-review-ledger-302.jsonl", "4d13d77513ee7064fbe7bfa0cbd996cb491363afa17297a2a185cb1927407600"),
    "summary": (CURATION_REL / "final-audit-summary.json", "318e323f87dcf07450074a83492801a54fd1a33b2597004c4737722e2c6bec66"),
    "parent_catalog": (Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json"), "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"),
    "parent_ledger": (Path("Docs/catalog/v5/releases/5.4/Strict_Conjecture_Ledger.json"), "52ba1ccf06462741bcc48028fb121e5e30d1e7b56128cfeb910dc56a2e1a83a3"),
    "release_manifest": (Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json"), "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"),
    "openconjecture": (Path("Docs/catalog/v5/sources/openconjecture-fa03d85-cc-by-real-conf090.jsonl"), "8a698e3af53ca0605a2a8ecd2e3a9944ad84157440a86f3c319effaf9792c6ce"),
    "oeis_all_conjectur": (Path("Docs/catalog/v5/sources/oeis-conjectures-4c866362-all-conjectur-v2.jsonl"), "18da1f5881f0410f2c38dc8362271b536db11c4509d58812942a11981181ec3d"),
}

BUILDER_INPUTS = {
    "source_archive", "source_manifest", "source_asset", "mechanical_screen",
    "parent_relations", "parent_exclusions", "residual_candidates", "review_a",
    "review_b", "status_drift", "parent_catalog", "parent_ledger",
    "release_manifest", "openconjecture", "oeis_all_conjectur",
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


class Audit:
    def __init__(self) -> None:
        self.checks = 0
        self.issues: list[str] = []

    def check(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.issues.append(message)

    def equal(self, observed: Any, expected: Any, label: str) -> None:
        self.checks += 1
        if observed != expected:
            self.issues.append(f"{label}: observed={observed!r}, expected={expected!r}")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path, audit: Audit, *, canonical_lines: bool = True) -> list[dict[str, Any]]:
    raw = path.read_bytes()
    audit.check(raw.endswith(b"\n"), f"{path}: missing final newline")
    lines = raw.splitlines()
    audit.check(all(line.strip() for line in lines), f"{path}: blank JSONL line")
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(lines, 1):
        value = json.loads(line)
        audit.check(isinstance(value, dict), f"{path}:{number}: row is not an object")
        if not isinstance(value, dict):
            continue
        if canonical_lines:
            audit.equal(line, canonical(value), f"{path}:{number}: noncanonical JSON")
        rows.append(value)
    return rows


def unique_map(rows: Iterable[dict[str, Any]], key: str, audit: Audit, label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        audit.check(isinstance(value, str), f"{label}: non-string {key}")
        if isinstance(value, str):
            audit.check(value not in result, f"{label}: duplicate {key} {value}")
            result[value] = row
    return result


def safe_tar_name(name: str) -> bool:
    path = PurePosixPath(name)
    in_prefix = name == SOURCE_PREFIX.rstrip("/") or name.startswith(SOURCE_PREFIX)
    return not path.is_absolute() and ".." not in path.parts and in_prefix


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", "--workspace", dest="workspace", type=Path, default=REPO_ROOT)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    report_path = args.report.resolve() if args.report else workspace / CURATION_REL / "final-ledger-validation.json"
    paths = {name: workspace / relative for name, (relative, _) in FIXED.items()}
    audit = Audit()
    input_meta: dict[str, dict[str, Any]] = {}
    for name, path in paths.items():
        if not path.is_file():
            audit.check(False, f"missing pinned input {name}: {path}")
            continue
        observed = sha256_file(path)
        input_meta[name] = {"path": FIXED[name][0].as_posix(), "sha256": observed}
        audit.equal(observed, FIXED[name][1], f"pinned input {name}")
    if any(not path.is_file() for path in paths.values()):
        for issue in audit.issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 1

    sources = load_jsonl(paths["source_asset"], audit)
    screens = load_jsonl(paths["mechanical_screen"], audit)
    relations = load_jsonl(paths["parent_relations"], audit)
    exclusions = load_jsonl(paths["parent_exclusions"], audit)
    candidates = load_jsonl(paths["residual_candidates"], audit)
    review_a = load_jsonl(paths["review_a"], audit)
    review_b = load_jsonl(paths["review_b"], audit)
    residual = load_jsonl(paths["residual_reviews"], audit)
    drifts = load_jsonl(paths["status_drift"], audit)
    ledger = load_jsonl(paths["ledger"], audit)
    openconjecture = load_jsonl(paths["openconjecture"], audit)
    oeis_rows = load_jsonl(paths["oeis_all_conjectur"], audit)
    source_manifest = load_json(paths["source_manifest"])
    residual_receipt = load_json(paths["residual_validation"])
    summary = load_json(paths["summary"])
    parent_catalog = load_json(paths["parent_catalog"])
    parent_ledger = load_json(paths["parent_ledger"])
    release_manifest = load_json(paths["release_manifest"])

    audit.equal([row.get("cb_id") for row in sources], EXPECTED_IDS, "source coverage/order")
    audit.equal([row.get("cb_id") for row in screens], EXPECTED_IDS, "screen coverage/order")
    audit.equal([row.get("cb_id") for row in ledger], EXPECTED_IDS, "ledger coverage/order")
    source_by_id = unique_map(sources, "cb_id", audit, "source")
    screen_by_id = unique_map(screens, "cb_id", audit, "screen")
    ledger_by_id = unique_map(ledger, "cb_id", audit, "ledger")

    # Replay all 302 exact source records and rights evidence from the fixed archive.
    expected_files = {
        SOURCE_PREFIX + "CITATION.cff",
        SOURCE_PREFIX + "LICENSE-DATA",
        SOURCE_PREFIX + "NOTICE",
        SOURCE_PREFIX + "problems/conjectures/README.md",
        *{SOURCE_PREFIX + f"problems/conjectures/{cb_id}.json" for cb_id in EXPECTED_IDS},
    }
    archived: dict[str, bytes] = {}
    with tarfile.open(paths["source_archive"], "r:gz") as archive:
        members = archive.getmembers()
        audit.check(all(safe_tar_name(member.name) for member in members), "unsafe source archive member")
        for member in members:
            if member.isfile():
                handle = archive.extractfile(member)
                audit.check(handle is not None, f"unreadable source archive member {member.name}")
                if handle is not None:
                    audit.check(member.name not in archived, f"duplicate source archive member {member.name}")
                    archived[member.name] = handle.read()
    audit.equal(set(archived), expected_files, "source archive file set")
    audit.equal(len(archived), 306, "source archive file count")
    audit.equal(source_manifest.get("schema_version"), "awesome-theorems/conjecturebench-fixed-source/1", "source manifest schema")
    audit.equal(source_manifest.get("source", {}).get("commit"), SOURCE_COMMIT, "source manifest commit")
    audit.equal(source_manifest.get("source", {}).get("tree_sha1"), SOURCE_TREE, "source manifest tree")
    audit.equal(source_manifest.get("archive", {}).get("sha256"), FIXED["source_archive"][1], "source manifest archive hash")
    audit.equal(source_manifest.get("curated_source", {}).get("sha256"), FIXED["source_asset"][1], "source manifest curated hash")
    rights_hashes = source_manifest.get("rights", {}).get("evidence", {})
    for name in ("CITATION.cff", "LICENSE-DATA", "NOTICE"):
        audit.equal(sha256_bytes(archived[SOURCE_PREFIX + name]), rights_hashes.get(name), f"rights member {name}")
    audit.equal(source_manifest.get("rights", {}).get("bespoke_record_layer_license_spdx"), "CC-BY-4.0", "record-layer license")
    audit.equal(source_manifest.get("rights", {}).get("upstream_rights_not_inherited"), True, "upstream rights boundary")

    for cb_id in EXPECTED_IDS:
        source = source_by_id[cb_id]
        record_path = source.get("record_path")
        audit.equal(record_path, f"problems/conjectures/{cb_id}.json", f"{cb_id}: record path")
        raw = archived.get(SOURCE_PREFIX + str(record_path), b"")
        parsed = json.loads(raw)
        statement = source.get("exact_statement")
        audit.equal(source.get("source_snapshot", {}).get("commit"), SOURCE_COMMIT, f"{cb_id}: source commit")
        audit.equal(source.get("source_snapshot", {}).get("tree_sha1"), SOURCE_TREE, f"{cb_id}: source tree")
        audit.equal(source.get("source_record_key"), f"conjecturebench/{cb_id}@{SOURCE_COMMIT}", f"{cb_id}: source key")
        audit.equal(source.get("record"), parsed, f"{cb_id}: parsed source record")
        audit.equal(source.get("record_raw_sha256"), sha256_bytes(raw), f"{cb_id}: raw SHA-256")
        audit.equal(source.get("record_raw_size_bytes"), len(raw), f"{cb_id}: raw size")
        audit.equal(source.get("record_blob_sha1"), git_blob_sha1(raw), f"{cb_id}: Git blob SHA-1")
        audit.equal(source.get("record_canonical_sha256"), sha256_bytes(canonical(parsed)), f"{cb_id}: canonical SHA-256")
        audit.equal(statement, parsed.get("statement"), f"{cb_id}: exact statement")
        if isinstance(statement, str):
            audit.equal(source.get("exact_statement_sha256"), sha256_bytes(statement.encode()), f"{cb_id}: statement SHA-256")
        audit.equal(source.get("duplicate_of"), parsed.get("duplicate_of"), f"{cb_id}: duplicate_of")
        observed = source.get("source_status_observation", {})
        recorded = parsed.get("status_observation", {})
        for field in ("state", "evidence_state", "as_of"):
            audit.equal(observed.get(field), recorded.get(field), f"{cb_id}: recorded status {field}")
        audit.equal(observed.get("preserved_not_rolled_forward"), True, f"{cb_id}: status preservation")
        audit.equal(observed.get("current_status_requires_separate_cutoff_review"), True, f"{cb_id}: separate cutoff boundary")

        screen = screen_by_id[cb_id]
        duplicate = source.get("duplicate_of")
        state = observed.get("state")
        evidence = observed.get("evidence_state")
        disposition = (
            "explicit_source_duplicate" if duplicate is not None else
            "source_status_contested" if state == "status-contested" else
            "needs_independent_status_review" if evidence == "needs-independent-review" else
            "semantic_review_candidate"
        )
        audit.equal(screen.get("mechanical_disposition"), disposition, f"{cb_id}: mechanical disposition")
        audit.equal(screen.get("source_record_key"), source.get("source_record_key"), f"{cb_id}: screen source key")
        audit.equal(screen.get("source_as_of"), observed.get("as_of"), f"{cb_id}: screen status date")
        audit.equal(screen.get("explicit_duplicate_target"), duplicate, f"{cb_id}: screen duplicate target")
        audit.equal(screen.get("accepted"), False, f"{cb_id}: mechanical acceptance")
        audit.equal(screen.get("strict_credit_granted"), False, f"{cb_id}: mechanical credit")

    # Reconstruct and validate the reviewed residual queue independently.
    audit.equal(len(candidates), 190, "residual candidate count")
    audit.equal(len(review_a), 95, "review A count")
    audit.equal(len(review_b), 95, "review B count")
    combined = sorted(review_a + review_b, key=lambda row: row.get("input_index", row.get("residual_index")))
    audit.equal([row.get("input_index", row.get("residual_index")) for row in combined], list(range(190)), "review index coverage")
    audit.equal(combined, residual, "merged residual payload")
    audit.equal([row.get("cb_id") for row in residual], [row.get("id") for row in candidates], "residual ID/order join")
    residual_by_id = unique_map(residual, "cb_id", audit, "residual")
    for index, (candidate, review) in enumerate(zip(candidates, residual, strict=True)):
        cb_id = review.get("cb_id")
        audit.equal(review.get("input_index"), index, f"{cb_id}: input index")
        audit.equal(review.get("residual_index"), index, f"{cb_id}: residual index")
        audit.equal(review.get("input_sha256"), FIXED["residual_candidates"][1], f"{cb_id}: residual input hash")
        audit.equal(review.get("input_record_sha256"), sha256_bytes(canonical(candidate)), f"{cb_id}: residual record hash")
        audit.equal(review.get("exact_claim_text"), candidate.get("statement"), f"{cb_id}: residual exact text")
        audit.equal(review.get("exact_claim_text"), source_by_id.get(str(cb_id), {}).get("exact_statement"), f"{cb_id}: residual/source text")
        audit.check(review.get("decision") in {"pending", "reject"}, f"{cb_id}: forbidden residual decision")
        audit.equal(review.get("acceptance_evidence_complete"), False, f"{cb_id}: residual acceptance flag")
        audit.equal(review.get("grants_strict_conjecture_credit"), False, f"{cb_id}: residual credit flag")
        audit.check("/tmp/" not in canonical(review).decode() and "/home/sansha/" not in canonical(review).decode(), f"{cb_id}: nonportable review path")
    audit.equal(Counter(row.get("decision") for row in residual), Counter({"pending": 138, "reject": 52}), "residual decisions")

    audit.equal(residual_receipt.get("schema_version"), "conjecturebench-residual-review-consolidation-v2", "residual receipt schema")
    audit.equal(residual_receipt.get("overall_pass"), True, "residual receipt pass")
    audit.equal(residual_receipt.get("merged_output", {}).get("sha256"), FIXED["residual_reviews"][1], "residual receipt hash")
    audit.equal(residual_receipt.get("merged_output", {}).get("rows"), 190, "residual receipt rows")
    audit.equal(residual_receipt.get("counts", {}).get("decisions"), {"pending": 138, "reject": 52}, "residual receipt decisions")
    audit.equal(residual_receipt.get("counts", {}).get("accepted"), 0, "residual receipt accepted")
    audit.equal(residual_receipt.get("counts", {}).get("strict_credits_granted"), 0, "residual receipt credits")
    receipt_names = {"residual_candidates", "source_asset", "parent_catalog", "parent_ledger", "openconjecture", "oeis_all_conjectur"}
    audit.equal(set(residual_receipt.get("inputs", {})), receipt_names, "residual receipt input set")
    for name in receipt_names:
        entry = residual_receipt.get("inputs", {}).get(name, {})
        audit.equal(entry.get("path"), FIXED[name][0].as_posix(), f"residual receipt path {name}")
        audit.equal(entry.get("sha256"), FIXED[name][1], f"residual receipt hash {name}")

    # Parent exact-declaration and later status-drift exclusions.
    audit.equal(len(relations), 97, "stable identity relation count")
    audit.equal(len({row.get("cb_id") for row in relations}), 88, "stable identity CB-ID count")
    exclusions_by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in exclusions:
        exclusions_by_id[str(row.get("cb_id"))].append(row)
    drift_by_id = unique_map(drifts, "cb_id", audit, "status drift")
    audit.equal(len(exclusions), 79, "parent exclusion evidence count")
    audit.equal(len(exclusions_by_id), 70, "parent exclusion CB-ID count")
    audit.equal(Counter(row.get("exclusion_type") for row in exclusions), Counter({"exact_parent_formal_declaration_text": 76, "status_drift_parent_now_solved": 3}), "parent exclusion types")
    audit.equal(set(drift_by_id), {"cb-0267", "cb-0269", "cb-0271"}, "solved drift IDs")

    partitions = {
        "residual_review": set(residual_by_id),
        "parent_exclusion": set(exclusions_by_id),
        "explicit_source_duplicate": {row["cb_id"] for row in screens if row.get("mechanical_disposition") == "explicit_source_duplicate"},
        "mechanical_status_quarantine": {row["cb_id"] for row in screens if row.get("mechanical_disposition") in {"source_status_contested", "needs_independent_status_review"}},
    }
    for left, left_ids in partitions.items():
        for right, right_ids in partitions.items():
            if left < right:
                audit.equal(left_ids & right_ids, set(), f"partition overlap {left}/{right}")
    audit.equal(set().union(*partitions.values()), set(EXPECTED_IDS), "partition union")
    audit.equal({name: len(ids) for name, ids in partitions.items()}, EXPECTED_PARTITIONS, "partition counts")

    catalog_by_id = unique_map(parent_catalog.get("records", []), "stage_claim_id", audit, "parent catalog")
    strict_by_id = unique_map(parent_ledger.get("strict_credits", []), "stage_claim_id", audit, "parent strict ledger")
    audit.equal(parent_catalog.get("release"), "5.4", "parent catalog release")
    audit.equal(parent_ledger.get("release"), "5.4", "parent ledger release")
    audit.equal(release_manifest.get("release"), "5.4", "release manifest release")
    for evidence in exclusions:
        cb_id = evidence.get("cb_id")
        parent_id = evidence.get("parent_stage_claim_id")
        parent = catalog_by_id.get(parent_id, {})
        audit.check(bool(parent), f"{cb_id}: missing parent target {parent_id}")
        joins = {
            "parent_variant_id": "variant_id", "parent_display_name": "display_name",
            "parent_origin_release": "origin_release", "parent_current_claim_kind": "current_claim_kind",
            "parent_material_status": "material_status", "parent_raw_status": "raw_status",
            "parent_formal_declaration_sha256": "formal_declaration_sha256",
            "parent_formal_declaration_text": "formal_declaration", "parent_formal_docstring": "formal_docstring",
            "parent_status_detail": "status_detail",
        }
        for evidence_field, parent_field in joins.items():
            audit.equal(evidence.get(evidence_field), parent.get(parent_field), f"{cb_id}/{parent_id}: {evidence_field}")
        audit.equal(evidence.get("parent_is_effective_strict_credit"), parent_id in strict_by_id, f"{cb_id}/{parent_id}: strict join")
        if evidence.get("exclusion_type") == "exact_parent_formal_declaration_text":
            audit.equal(evidence.get("declaration_text_byte_equal"), True, f"{cb_id}/{parent_id}: declaration equality")
            audit.equal(evidence.get("benchmark_declaration_text"), evidence.get("parent_formal_declaration_text"), f"{cb_id}/{parent_id}: declaration text")
        else:
            audit.equal(parent.get("material_status"), "proved", f"{cb_id}/{parent_id}: solved status")
    for cb_id, drift in drift_by_id.items():
        source = source_by_id[cb_id]
        audit.equal(drift.get("exact_cb_statement"), source.get("exact_statement"), f"{cb_id}: drift exact text")
        audit.equal(drift.get("cb_recorded_status"), source.get("source_status_observation"), f"{cb_id}: preserved recorded status")
        audit.equal(drift.get("current_open_admission"), False, f"{cb_id}: current-open rejection")
        audit.equal(drift.get("strict_credit_granted"), False, f"{cb_id}: drift credit")

    # Final row joins, provenance, decisions, and generated partitions.
    for cb_id in EXPECTED_IDS:
        row = ledger_by_id[cb_id]
        source = source_by_id[cb_id]
        screen = screen_by_id[cb_id]
        partition = next(name for name, ids in partitions.items() if cb_id in ids)
        audit.equal(row.get("final_audit_partition"), partition, f"{cb_id}: final partition")
        audit.equal(row.get("exact_claim_text"), source.get("exact_statement"), f"{cb_id}: final text")
        audit.equal(row.get("source_record_key"), source.get("source_record_key"), f"{cb_id}: final source key")
        audit.equal(row.get("source_record_raw_sha256"), source.get("record_raw_sha256"), f"{cb_id}: final raw hash")
        audit.equal(row.get("source_commit"), SOURCE_COMMIT, f"{cb_id}: final commit")
        audit.equal(row.get("source_tree_sha1"), SOURCE_TREE, f"{cb_id}: final tree")
        audit.equal(row.get("source_status_observation"), source.get("source_status_observation"), f"{cb_id}: final recorded status")
        audit.equal(row.get("rights_boundary"), source.get("rights"), f"{cb_id}: final rights")
        payload = {key: value for key, value in row.items() if key != "final_row_payload_sha256"}
        audit.equal(row.get("final_row_payload_sha256"), sha256_bytes(canonical(payload)), f"{cb_id}: payload hash")
        audit.equal(row.get("acceptance_evidence_complete"), False, f"{cb_id}: acceptance evidence")
        audit.equal(row.get("grants_strict_conjecture_credit"), False, f"{cb_id}: strict credit")
        if partition == "residual_review":
            normalized = {"source_commit", "source_tree_sha1", "source_record_key", "source_record_raw_sha256", "final_audit_partition", "source_status_observation", "rights_boundary", "final_row_payload_sha256"}
            audit.equal({key: value for key, value in row.items() if key not in normalized}, {key: value for key, value in residual_by_id[cb_id].items() if key not in normalized}, f"{cb_id}: residual payload retained")
        else:
            audit.equal(row.get("mechanical_screen"), screen, f"{cb_id}: embedded screen")
        if partition == "parent_exclusion":
            evidence = exclusions_by_id[cb_id]
            solved = any(item.get("exclusion_type") == "status_drift_parent_now_solved" for item in evidence)
            audit.equal(row.get("decision"), "reject", f"{cb_id}: parent decision")
            audit.equal(row.get("duplicate_targets"), [] if solved else sorted({f"parent/{item['parent_stage_claim_id']}" for item in evidence}), f"{cb_id}: parent targets")
            audit.equal(row.get("status_drift_evidence"), drift_by_id.get(cb_id) if solved else None, f"{cb_id}: final drift")
            audit.equal(row.get("parent_exclusion_evidence"), evidence, f"{cb_id}: final parent evidence")
        elif partition == "explicit_source_duplicate":
            audit.equal(row.get("decision"), "reject", f"{cb_id}: explicit duplicate decision")
            audit.equal(row.get("duplicate_targets"), [f"conjecturebench/{source['duplicate_of']}"], f"{cb_id}: explicit target")
        elif partition == "mechanical_status_quarantine":
            audit.equal(row.get("decision"), "pending", f"{cb_id}: quarantine decision")
            audit.equal(row.get("duplicate_targets"), [], f"{cb_id}: quarantine targets")
        audit.check(row.get("decision") in {"pending", "reject"}, f"{cb_id}: forbidden decision")
        if row.get("decision") == "pending":
            audit.equal(row.get("duplicate_targets"), [], f"{cb_id}: pending duplicate target")

    decisions = Counter(row.get("decision") for row in ledger)
    partition_counts = Counter(row.get("final_audit_partition") for row in ledger)
    reasons = Counter(row.get("reason_code") for row in ledger)
    audit.equal(dict(decisions), EXPECTED_DECISIONS, "final decisions")
    audit.equal(dict(partition_counts), EXPECTED_PARTITIONS, "final partitions")
    audit.equal(sum(row.get("decision") == "accept" for row in ledger), 0, "accepted count")
    audit.equal(sum(row.get("grants_strict_conjecture_credit") is True for row in ledger), 0, "credit count")

    # Every semantic duplicate target must resolve to a pinned evidence corpus.
    open_ids = {str(row.get("id")) for row in openconjecture}
    audit.equal(len(open_ids), len(openconjecture), "OpenConjecture unique IDs")
    oeis_refs: dict[str, set[str]] = defaultdict(set)
    oeis_key_counts: Counter[str] = Counter()
    for item in oeis_rows:
        key = item.get("candidate_key")
        if isinstance(key, str):
            oeis_key_counts[key] += 1
            for location in item.get("locations", []):
                number = location.get("a_number") if isinstance(location, dict) else None
                if isinstance(number, str):
                    oeis_refs[key].add(number)
    all_targets: list[tuple[str, str]] = []
    for row in ledger:
        targets = row.get("duplicate_targets")
        audit.check(isinstance(targets, list), f"{row.get('cb_id')}: duplicate_targets type")
        if isinstance(targets, list):
            audit.equal(len(targets), len(set(targets)), f"{row.get('cb_id')}: repeated target")
            all_targets.extend((str(row.get("cb_id")), target) for target in targets if isinstance(target, str))
    namespace_counts: Counter[str] = Counter()
    for cb_id, target in all_targets:
        if re.fullmatch(r"(?:parent/)?S5-CLM-\d{8}", target):
            namespace_counts["parent"] += 1
            audit.check(target.removeprefix("parent/") in catalog_by_id, f"{cb_id}: unresolved parent target {target}")
        elif re.fullmatch(r"conjecturebench/cb-\d{4}", target):
            namespace_counts["conjecturebench"] += 1
            target_id = target.removeprefix("conjecturebench/")
            audit.check(target_id in source_by_id and target_id != cb_id, f"{cb_id}: unresolved/self CB target {target}")
        elif re.fullmatch(r"openconjecture/\d+", target):
            namespace_counts["openconjecture"] += 1
            audit.check(target.split("/", 1)[1] in open_ids, f"{cb_id}: unresolved OpenConjecture target {target}")
        elif re.fullmatch(r"oeis-normalized/[0-9a-f]{64}", target):
            namespace_counts["oeis-normalized"] += 1
            audit.equal(oeis_key_counts[target], 1, f"{cb_id}: normalized OEIS target {target}")
        elif re.fullmatch(r"oeis/A\d{6}/[0-9a-f]{8}", target):
            namespace_counts["oeis"] += 1
            _, number, prefix = target.split("/")
            matches = [key for key, numbers in oeis_refs.items() if key.removeprefix("oeis-normalized/").startswith(prefix) and number in numbers]
            audit.equal(len(matches), 1, f"{cb_id}: short OEIS target {target}")
        else:
            audit.check(False, f"{cb_id}: unknown duplicate target {target!r}")

    # Recompute the final summary and enforce the audit boundary text.
    audit.equal(summary.get("schema_version"), "conjecturebench-final-strict-audit-v1", "summary schema")
    audit.equal(summary.get("audit_cutoff_date"), "2026-08-10", "summary cutoff")
    audit.equal(summary.get("source_commit"), SOURCE_COMMIT, "summary commit")
    audit.equal(summary.get("source_tree_sha1"), SOURCE_TREE, "summary tree")
    audit.equal(set(summary.get("inputs", {})), BUILDER_INPUTS, "summary input set")
    for name in BUILDER_INPUTS:
        entry = summary.get("inputs", {}).get(name, {})
        audit.equal(entry.get("path"), FIXED[name][0].as_posix(), f"summary path {name}")
        audit.equal(entry.get("sha256"), FIXED[name][1], f"summary hash {name}")
    generated = summary.get("generated_artifacts", {})
    for name in ("residual_reviews", "residual_validation"):
        audit.equal(generated.get(name, {}).get("path"), FIXED[name][0].as_posix(), f"summary generated path {name}")
        audit.equal(generated.get(name, {}).get("sha256"), FIXED[name][1], f"summary generated hash {name}")
        audit.equal(generated.get(name, {}).get("size_bytes"), paths[name].stat().st_size, f"summary generated size {name}")
    coverage = summary.get("coverage", {})
    audit.equal(coverage.get("source_records"), 302, "summary source rows")
    audit.equal(coverage.get("final_review_rows"), 302, "summary ledger rows")
    audit.equal(coverage.get("partitions"), dict(sorted(partition_counts.items())), "summary partitions")
    outcome = summary.get("outcome", {})
    audit.equal(outcome.get("decisions"), dict(sorted(decisions.items())), "summary decisions")
    audit.equal(outcome.get("reason_codes"), dict(sorted(reasons.items())), "summary reasons")
    audit.equal(outcome.get("accepted"), 0, "summary accepted")
    audit.equal(outcome.get("strict_credits_granted"), 0, "summary credits")
    audit.equal(outcome.get("release_entries_added"), 0, "summary release additions")
    audit.equal(summary.get("ledger", {}).get("path"), FIXED["ledger"][0].as_posix(), "summary ledger path")
    audit.equal(summary.get("ledger", {}).get("sha256"), FIXED["ledger"][1], "summary ledger hash")
    audit.equal(summary.get("ledger", {}).get("rows"), 302, "summary ledger count")
    audit.equal(summary.get("ledger", {}).get("size_bytes"), paths["ledger"].stat().st_size, "summary ledger size")
    boundary = summary.get("boundary", [])
    audit.check(any("No candidate is automatically accepted" in item for item in boundary), "missing no-auto-accept boundary")
    audit.check(any("complete atomic proposition" in item and "high or medium importance" in item and "source-specific rights" in item and "semantic deduplication" in item for item in boundary), "missing strict admission gates")
    audit.check(any("status observations and dates are preserved" in item and "drift is recorded separately" in item for item in boundary), "missing status-date boundary")
    audit.check(any("residual upper bound is 190" in item and "161, 162, and 172 are withdrawn" in item for item in boundary), "missing corrected upper bound")
    audit.check(any("parent release 5.4" in item and "not modified" in item for item in boundary), "missing protected-release boundary")
    audit.equal(paths["summary"].read_bytes(), canonical(summary) + b"\n", "canonical summary")

    for name in ("review_a", "review_b", "residual_reviews", "residual_validation", "ledger", "summary", "source_manifest"):
        text = paths[name].read_text(encoding="utf-8")
        audit.check("/tmp/" not in text and "/home/sansha/" not in text, f"nonportable path in {name}")

    # Fail closed if any pinned file changed while it was being reviewed.
    for name, path in paths.items():
        audit.equal(sha256_file(path), input_meta[name]["sha256"], f"stable input during validation {name}")

    report = {
        "schema_version": "awesome-theorems/conjecturebench-final-ledger-validation/1",
        "overall_pass": not audit.issues,
        "checks_performed": audit.checks,
        "issues": audit.issues,
        "source": {
            "archive_replayed": True,
            "commit": SOURCE_COMMIT,
            "tree_sha1": SOURCE_TREE,
            "records_replayed": len(sources),
            "archive_sha256": FIXED["source_archive"][1],
        },
        "inputs": input_meta,
        "coverage": {"ids_in_exact_order": [row.get("cb_id") for row in ledger] == EXPECTED_IDS, "partitions": dict(sorted(partition_counts.items()))},
        "outcome": {"decisions": dict(sorted(decisions.items())), "accepted": 0, "strict_credits_granted": 0},
        "duplicate_targets": {"total": len(all_targets), "namespaces": dict(sorted(namespace_counts.items())), "all_resolved": not any("target" in issue.lower() for issue in audit.issues)},
        "duplicate_evidence_scope": {
            "oeis_source_path": FIXED["oeis_all_conjectur"][0].as_posix(),
            "oeis_source_sha256": FIXED["oeis_all_conjectur"][1],
            "boundary": "Target existence is replayed from the pinned OEIS source asset; proposition equivalence remains a recorded human-review judgment and does not create acceptance.",
        },
        "ledger": {"path": FIXED["ledger"][0].as_posix(), "rows": len(ledger), "sha256": FIXED["ledger"][1], "size_bytes": paths["ledger"].stat().st_size},
        "summary": {"path": FIXED["summary"][0].as_posix(), "sha256": FIXED["summary"][1], "size_bytes": paths["summary"].stat().st_size},
        "protected_release_5_4": {
            "manifest_sha256": FIXED["release_manifest"][1],
            "catalog_sha256": FIXED["parent_catalog"][1],
            "strict_ledger_sha256": FIXED["parent_ledger"][1],
            "release_entries_added": 0,
        },
    }
    report_payload = canonical(report) + b"\n"
    if args.write_report:
        if audit.issues:
            print("refusing to overwrite the validation report after failed checks", file=sys.stderr)
        else:
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_bytes(report_payload)
    else:
        audit.check(report_path.is_file(), f"missing validation report: {report_path}")
        if report_path.is_file():
            audit.equal(report_path.read_bytes(), report_payload, "validation report determinism")

    result = {
        "overall_pass": not audit.issues,
        "checks_performed": audit.checks,
        "issue_count": len(audit.issues),
        "report": (CURATION_REL / "final-ledger-validation.json").as_posix(),
        "report_sha256": sha256_bytes(report_payload),
    }
    print(json.dumps(result, indent=2))
    if audit.issues:
        for issue in audit.issues[:50]:
            print(f"ERROR: {issue}", file=sys.stderr)
        if len(audit.issues) > 50:
            print(f"ERROR: {len(audit.issues) - 50} additional issues omitted", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
