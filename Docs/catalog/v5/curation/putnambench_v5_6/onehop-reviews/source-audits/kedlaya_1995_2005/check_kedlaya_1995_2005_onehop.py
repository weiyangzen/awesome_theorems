#!/usr/bin/env python3
"""Independent, read-only verifier for the Kedlaya 1995--2005 one-hop audit.

The checker never imports or invokes the generator.  It binds every reviewed
row to the external link-only source snapshot by file and line-span SHA-256,
rebuilds all field/count/credit invariants, and verifies the semantic-audit
decision receipt against the final independently written statements.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ARTIFACT = HERE / "kedlaya_1995_2005_onehop_relations.json"
RECEIPT = HERE / "receipt.json"
SOURCE_ROOT = Path(os.environ.get("KEDLAYA_SOURCE_ROOT", "/tmp/putnam-kedlaya-solutions-1995-2025"))
EXPECTED_YEARS = range(1995, 2006)
EXPECTED_TOP_KEYS = {
    "schema_version",
    "scope",
    "counts",
    "verbatim_source_text_stored",
    "edges",
}
EXPECTED_EDGE_KEYS = {
    "schema_version",
    "candidate_key",
    "problem_key",
    "problem_id",
    "edge_class",
    "relation_type",
    "proposed_relation_type",
    "target_kind",
    "target_identity_key",
    "independent_summary",
    "target",
    "source_locator",
    "source_role",
    "disposition",
    "review_status",
    "reason_code",
    "evidence",
    "catalog_credit",
    "theorem_identity_credit",
    "grants_release_entry",
    "grants_theorem_identity_credit",
    "accepted_rationale",
    "copyright_boundary",
    "row_sha256",
}
EXPECTED_TARGET_KEYS = {
    "kind",
    "claim_kind",
    "material_status",
    "normalized_label",
    "independently_written_statement",
    "statement_sha256",
    "parent_5_5_exact_join",
}
EXPECTED_LOCATOR_KEYS = {
    "source_id",
    "path",
    "url",
    "line_start",
    "line_end",
    "file_sha256",
    "span_sha256",
}
EXPECTED_COUNTS = {
    "accepted_edges": 132,
    "accepted_theorem_claim_targets": 132,
    "accepted_open_claim_targets": 0,
    "accepted_conjecture_claim_targets": 0,
    "candidate_edges": 0,
    "covered_problems": 132,
    "catalog_credit_granted": 0,
    "theorem_identity_credit_granted": 0,
}
BANNED_PAYLOAD_KEYS = {
    "quote",
    "quotes",
    "snippet",
    "snippets",
    "trigger",
    "trigger_text",
    "source_text",
    "excerpt",
    "verbatim_text",
}


def sha256(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def canonical_sha(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(raw)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def recursive_keys(value: object):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from recursive_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from recursive_keys(nested)


def item_sections(raw: bytes) -> dict[str, tuple[int, int]]:
    lines = raw.decode("utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for line_number, line in enumerate(lines, 1):
        match = re.search(r"\\item\[([ABab])(?:--)?([1-6])\]", line)
        if match:
            starts.append((line_number, (match.group(1) + match.group(2)).lower()))
    require(len(starts) == 12, "source file does not contain the expected 12 problem sections")
    return {
        label: (start, starts[index + 1][0] - 1 if index + 1 < len(starts) else len(lines))
        for index, (start, label) in enumerate(starts)
    }


def main() -> int:
    require(ARTIFACT.is_file(), f"artifact missing: {ARTIFACT}")
    require(RECEIPT.is_file(), f"receipt missing: {RECEIPT}")
    require(SOURCE_ROOT.is_dir(), f"link-only source snapshot missing: {SOURCE_ROOT}")

    artifact_bytes = ARTIFACT.read_bytes()
    artifact = json.loads(artifact_bytes)
    receipt = json.loads(RECEIPT.read_bytes())
    require(set(artifact) == EXPECTED_TOP_KEYS, f"artifact top-level fields mismatch: {sorted(artifact)}")
    require(artifact.get("schema_version") == "putnam-onehop-v1", "artifact schema mismatch")
    require(artifact.get("scope") == {"years": [1995, 2005], "currently_reviewed_years": [1995, 2005]}, "scope mismatch")
    require(artifact.get("verbatim_source_text_stored") is False, "top-level source-text flag is not false")
    require(artifact.get("counts") == EXPECTED_COUNTS, "declared artifact counts mismatch")

    checker_path = Path(__file__).resolve()
    require(receipt.get("artifact") == ARTIFACT.name, "receipt artifact name mismatch")
    require(receipt.get("artifact_sha256") == sha256(artifact_bytes), "receipt artifact SHA-256 mismatch")
    require(receipt.get("checker") == checker_path.name, "receipt checker name mismatch")
    require(receipt.get("checker_sha256") == sha256(checker_path.read_bytes()), "receipt checker SHA-256 mismatch")
    require(receipt.get("counts") == EXPECTED_COUNTS, "receipt counts mismatch")
    require(receipt.get("source_text_stored") is False, "receipt source-text flag is not false")

    edges = artifact.get("edges")
    require(isinstance(edges, list), "edges is not a list")
    require(len(edges) == 132, f"edge count is {len(edges)}, expected 132")
    expected_ids = {
        f"putnam_{year}_{side}{number}"
        for year in EXPECTED_YEARS
        for side in ("a", "b")
        for number in range(1, 7)
    }
    ids = [edge.get("problem_id") for edge in edges]
    require(set(ids) == expected_ids and len(set(ids)) == 132, "problem universe/count mismatch")
    require(len({edge.get("candidate_key") for edge in edges}) == 132, "candidate keys are not unique")
    require(len({edge.get("target_identity_key") for edge in edges}) == 132, "target keys are not unique")
    require(Counter(int(pid.split("_")[1]) for pid in ids) == Counter({year: 12 for year in EXPECTED_YEARS}), "year coverage mismatch")

    present_banned = BANNED_PAYLOAD_KEYS.intersection(recursive_keys(artifact))
    require(not present_banned, f"verbatim-bearing payload keys found: {sorted(present_banned)}")

    source_files: dict[str, str] = {}
    section_cache: dict[str, dict[str, tuple[int, int]]] = {}
    statement_by_id: dict[str, str] = {}
    span_by_id: dict[str, str] = {}
    for position, edge in enumerate(edges):
        pid = edge.get("problem_id", "?")
        prefix = f"edge[{position}]/{pid}"
        require(set(edge) == EXPECTED_EDGE_KEYS, f"{prefix}: edge fields mismatch")
        require(edge["schema_version"] == "awesome-theorems/kedlaya-putnam-onehop-review/5.6", f"{prefix}: row schema")
        require(edge["candidate_key"] == f"kedlaya-onehop/{pid}/01-primary-key-proposition", f"{prefix}: candidate key")
        require(edge["problem_key"] == pid, f"{prefix}: problem key")
        require(edge["edge_class"] == "onehop_relation", f"{prefix}: edge class")
        require(edge["relation_type"] == "direct_key_proposition", f"{prefix}: relation type")
        require(edge["proposed_relation_type"] == "standard_solution_uses", f"{prefix}: proposed relation type")
        require(edge["target_kind"] == "local_lemma", f"{prefix}: target kind")
        require(edge["source_role"] == "secondary_unofficial_solution", f"{prefix}: source role")
        require(edge["disposition"] == "accepted_edge" and edge["review_status"] == "accepted", f"{prefix}: disposition/status")
        require(edge["reason_code"] == "reviewed_direct_proposition_relation", f"{prefix}: reason code")
        require(edge["catalog_credit"] == 0 and edge["theorem_identity_credit"] == 0, f"{prefix}: nonzero identity credit")
        require(edge["grants_release_entry"] is False and edge["grants_theorem_identity_credit"] is False, f"{prefix}: credit grant flag")

        summary = edge["independent_summary"]
        require(isinstance(summary, str) and len(summary.strip()) >= 30, f"{prefix}: missing/short independent statement")
        target = edge["target"]
        require(set(target) == EXPECTED_TARGET_KEYS, f"{prefix}: target fields mismatch")
        require(target["kind"] == "claim" and target["claim_kind"] == "theorem" and target["material_status"] == "proved", f"{prefix}: target classification")
        require(target["normalized_label"] == f"key solution proposition for {pid}", f"{prefix}: normalized label")
        require(target["independently_written_statement"] == summary, f"{prefix}: statement aliases disagree")
        require(target["statement_sha256"] == sha256(summary), f"{prefix}: statement SHA-256")
        join = target["parent_5_5_exact_join"]
        require(set(join) == {"status", "stage_claim_id", "variant_id", "basis"}, f"{prefix}: exact-join fields")
        require(join["status"] == "no_exact_match_established" and join["stage_claim_id"] is None and join["variant_id"] is None, f"{prefix}: exact-join result")
        require(isinstance(join["basis"], str) and join["basis"].strip(), f"{prefix}: exact-join basis")

        evidence = edge["evidence"]
        require(set(evidence) == {"proof_step_use_verified", "proposition_level", "relation_assertion_origin", "source_wording_redistributed", "verbatim_source_text_stored"}, f"{prefix}: evidence fields")
        require(evidence["proof_step_use_verified"] is True and evidence["proposition_level"] is True, f"{prefix}: proof-step review")
        require(evidence["relation_assertion_origin"] == "independently_written_reviewed_statement", f"{prefix}: relation origin")
        require(evidence["source_wording_redistributed"] is False and evidence["verbatim_source_text_stored"] is False, f"{prefix}: evidence rights flags")
        boundary = edge["copyright_boundary"]
        require(set(boundary) == {"verbatim_source_text_stored", "summary_is_independent_paraphrase", "source_text_reconstruction_material_stored"}, f"{prefix}: rights fields")
        require(boundary == {"verbatim_source_text_stored": False, "summary_is_independent_paraphrase": True, "source_text_reconstruction_material_stored": False}, f"{prefix}: rights boundary")
        require(isinstance(edge["accepted_rationale"], str) and edge["accepted_rationale"].strip(), f"{prefix}: empty rationale")

        locator = edge["source_locator"]
        require(set(locator) == EXPECTED_LOCATOR_KEYS, f"{prefix}: locator fields mismatch")
        year = int(pid.split("_")[1])
        label = pid.rsplit("_", 1)[1]
        filename = f"{year}s.tex"
        require(locator["source_id"] == f"kedlaya-putnam-archive/{year}/{label.upper()}", f"{prefix}: source id")
        require(locator["path"] == filename, f"{prefix}: source filename")
        require(locator["url"] == f"https://kskedlaya.org/putnam-archive/{filename}", f"{prefix}: source URL")
        source_path = SOURCE_ROOT / filename
        require(source_path.is_file(), f"{prefix}: source file missing")
        raw = source_path.read_bytes()
        file_digest = sha256(raw)
        source_files[filename] = file_digest
        require(locator["file_sha256"] == file_digest, f"{prefix}: source file SHA-256")
        lines = raw.splitlines(keepends=True)
        start, end = locator["line_start"], locator["line_end"]
        require(type(start) is int and type(end) is int and 1 <= start <= end <= len(lines), f"{prefix}: line bounds")
        span_digest = sha256(b"".join(lines[start - 1 : end]))
        require(locator["span_sha256"] == span_digest, f"{prefix}: source span SHA-256")
        if filename not in section_cache:
            section_cache[filename] = item_sections(raw)
        require(label in section_cache[filename], f"{prefix}: missing source section")
        section_start, section_end = section_cache[filename][label]
        require(section_start <= start <= end <= section_end, f"{prefix}: span outside problem section")
        require(edge["target_identity_key"] == f"local:{pid}:{span_digest}", f"{prefix}: target identity key")

        unhashed = dict(edge)
        row_digest = unhashed.pop("row_sha256")
        require(row_digest == canonical_sha(unhashed), f"{prefix}: row SHA-256")
        statement_by_id[pid] = target["statement_sha256"]
        span_by_id[pid] = span_digest

    require(receipt.get("source_files_sha256") == dict(sorted(source_files.items())), "receipt source-file digests mismatch")
    manifest = SOURCE_ROOT / "SHA256SUMS"
    require(manifest.is_file(), f"source hash manifest missing: {manifest}")
    require(receipt.get("source_manifest_sha256") == sha256(manifest.read_bytes()), "receipt source-manifest SHA-256 mismatch")

    audit = receipt.get("semantic_second_pass")
    require(isinstance(audit, dict), "semantic second-pass receipt missing")
    require(audit.get("reviewed_rows") == 132 and audit.get("unreviewed_rows") == 0, "semantic review coverage mismatch")
    require(audit.get("post_revision_approved_rows") == 132, "not all final rows are approved")
    bindings = audit.get("decision_bindings")
    require(isinstance(bindings, list) and len(bindings) == 132, "semantic decision bindings mismatch")
    binding_ids = [binding.get("problem_id") for binding in bindings]
    require(set(binding_ids) == expected_ids and len(set(binding_ids)) == 132, "semantic decision universe mismatch")
    decisions = Counter()
    for binding in bindings:
        pid = binding["problem_id"]
        require(set(binding) == {"problem_id", "second_pass_decision", "final_statement_sha256", "source_span_sha256"}, f"semantic binding fields: {pid}")
        decision = binding["second_pass_decision"]
        require(decision in {"OK", "CHANGE"}, f"invalid semantic decision: {pid}")
        require(binding["final_statement_sha256"] == statement_by_id[pid], f"semantic statement binding: {pid}")
        require(binding["source_span_sha256"] == span_by_id[pid], f"semantic span binding: {pid}")
        decisions[decision] += 1
    change_ids = sorted(binding["problem_id"] for binding in bindings if binding["second_pass_decision"] == "CHANGE")
    require(audit.get("initial_ok_rows") == decisions["OK"], "semantic OK count mismatch")
    require(audit.get("initial_change_rows") == decisions["CHANGE"], "semantic CHANGE count mismatch")
    require(audit.get("change_problem_ids") == change_ids, "semantic CHANGE ID list mismatch")
    require(decisions["OK"] + decisions["CHANGE"] == 132, "semantic decision total mismatch")
    shards = audit.get("review_shards")
    require(isinstance(shards, list) and len(shards) == 2, "semantic review shards mismatch")
    expected_shard_years = ([1995, 2001], [2002, 2005])
    expected_shard_sizes = (84, 48)
    for shard, years, size in zip(shards, expected_shard_years, expected_shard_sizes):
        require(shard.get("years") == years and shard.get("reviewed_rows") == size, f"semantic shard scope mismatch: {years}")
        shard_changes = sorted(pid for pid in change_ids if years[0] <= int(pid.split("_")[1]) <= years[1])
        require(shard.get("change_problem_ids") == shard_changes, f"semantic shard CHANGE IDs mismatch: {years}")
        require(shard.get("initial_change_rows") == len(shard_changes), f"semantic shard CHANGE count mismatch: {years}")
        require(shard.get("initial_ok_rows") == size - len(shard_changes), f"semantic shard OK count mismatch: {years}")

    invariants = receipt.get("invariants")
    require(isinstance(invariants, dict) and invariants, "receipt invariants missing")
    require(all(value is True for value in invariants.values()), "receipt contains a false invariant")

    print(
        "PASS kedlaya_1995_2005_onehop "
        f"artifact_sha256={sha256(artifact_bytes)} "
        f"edges={len(edges)} covered_problems={len(set(ids))} "
        f"semantic_ok={decisions['OK']} semantic_change={decisions['CHANGE']} "
        "pending=0 rejected=0 catalog_credit=0 theorem_identity_credit=0 source_text_stored=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
