#!/usr/bin/env python3
"""Validate immutable local evidence for the THM-M-0958 anchor audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
THEOREM_ID = "THM-M-0958"
ITEM_ID = "S56-M-0958-ANCHOR_AUDIT"
BASE_REVISION = "f023dbc3411d83201065d1a1156d7406b81135d4"
BASE_TREE = "3b3a73ec19293a2a9b8d9c7e67f0d25da2a511b4"
EXPRESSION_SHA256 = "bc0d841038cdbcd4960581583c4ddfb7004d7ad38cf6432ab4803e9908f8f59c"
STATEMENT_SHA256 = "765d13f4b2fc0bc8bdf0a1211039b62ed6269148819857795aac0c7a42dc40e6"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROTOCOL_SHA256 = "4d70485827d3911c1394a2feb17635c6fc51331f3da6650693926011f8542351"
AUDIT_SHA256 = "eba38a4e3bb2530ffb45bc9560be6b667823a4b3ff9e19fdedc802fc6190224d"
ANCHOR_LEAN_SHA256 = "6c40ddacfa73884ae682c1dd32dbc41b4e809750b3f3ac9bf9bd82565afc6b05"
LEAN_OUTPUT_SHA256 = "29005d807865eb32c7af8c3db6641e142e7f0f338ead814ad87667d2ec49ac40"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}
FORBIDDEN_WORDS = tuple(
    "".join(chr(code) for code in codes)
    for codes in (
        (115, 111, 114, 114, 121),
        (97, 100, 109, 105, 116),
        (115, 111, 114, 114, 121, 65, 120),
        (97, 120, 105, 111, 109),
        (99, 111, 110, 115, 116, 97, 110, 116),
        (117, 110, 115, 97, 102, 101),
        (105, 109, 112, 108, 101, 109, 101, 110, 116, 101, 100, 95, 98, 121),
        (101, 120, 116, 101, 114, 110),
        (111, 112, 97, 113, 117, 101),
        (110, 97, 116, 105, 118, 101, 95, 100, 101, 99, 105, 100, 101),
        (114, 117, 110, 95, 116, 97, 99),
        (112, 114, 111, 111, 102, 95, 119, 97, 110, 116, 101, 100),
    )
)
FORBIDDEN = re.compile(r"\b(?:" + "|".join(FORBIDDEN_WORDS) + r")\b")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_comments_and_strings(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*", "", source)
    source = re.sub(r'"(?:\\.|[^"\\])*"', '""', source)
    return source


def validate_packet(receipt: dict) -> None:
    packet_path = ROOT / ".stage1-worker-selftest.json"
    assert packet_path.exists(), "final worker self-test packet is missing"
    packet = load(packet_path)
    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"] and packet["output_summary"]


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert protocol["schema_version"] == "stage1-anchor-discovery/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert audit["item_id"] == protocol["item_id"] == receipt["item_id"] == ITEM_ID
    assert audit["theorem_id"] == protocol["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert audit["base_revision"] == protocol["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == protocol["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert receipt["phase"] == "anchor_audit" and receipt["intent"] == "audit"
    assert receipt["dependency"] == "S56-M-0958-STATEMENT"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["acceptance_authority"] == "Stage1 integration lane"
    assert receipt["node_self_tested"] is True
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["typed_graph_changes"] == [] and receipt["composition_certificates"] == []
    candidate_result = receipt["candidate_result"]
    assert candidate_result["inventory_classified"] is True
    assert candidate_result["candidate_count"] == 7
    assert candidate_result["exact_elkin_candidate_located"] is False
    assert candidate_result["related_behrend_candidate_kernel_checked"] is True
    assert candidate_result["related_behrend_candidate_sorry_free"] is True
    assert candidate_result["related_behrend_statement_mismatch_checked"] is True
    assert candidate_result["related_behrend_exact_root_credit"] is False
    assert candidate_result["root_classification"] == "M3"
    assert candidate_result["master_accepted"] is False
    validate_packet(receipt)

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert target["execution_rank"] == audit["execution_rank"] == 1492
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    assert item["phase"] == "anchor_audit" and item["layer"] == 2 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0958-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256

    assert protocol["protocol_id"] == "S56-M-0958-ANCHOR-DISCOVERY-20260713-01"
    assert protocol["inventory_version"] == audit["inventory_version"]
    assert protocol["frozen_before_candidate_classification"] is True
    assert protocol["saturation_claim"] is False
    assert len(protocol["aliases"]) >= 12 and len(protocol["surfaces"]) >= 7
    assert sha256(HERE / "anchor-discovery-protocol.json") == PROTOCOL_SHA256
    assert audit["discovery_protocol_sha256"] == PROTOCOL_SHA256
    assert receipt["discovery_protocol_sha256"] == PROTOCOL_SHA256
    assert sha256(HERE / "anchor-audit.json") == AUDIT_SHA256
    assert sha256(HERE / "AnchorAudit.lean") == ANCHOR_LEAN_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]
    assert sha256(LEAN_ROOT / "lean-toolchain") == env["lean_toolchain_file_sha256"]
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    assert output("git", "rev-parse", "HEAD:LICENSE", cwd=MATHLIB) == env["mathlib_license_blob"]

    candidates = audit["candidates"]
    ids = [candidate["candidate_id"] for candidate in candidates]
    assert len(ids) == len(set(ids)) == 7
    assert ids == protocol["inventory_members"]
    behrend = next(c for c in candidates if c["candidate_id"] == "M0958-C02-MATHLIB-BEHREND-LOWER-BOUND")
    assert behrend["revision"] == MATHLIB_REVISION and behrend["tree"] == MATHLIB_TREE
    assert behrend["declaration"] == "Behrend.roth_lower_bound"
    assert behrend["candidate_classification"] == (
        "M0-W_for_nonidentical_behrend_target_no_elkin_root_credit"
    )
    source = MATHLIB / behrend["file"]
    assert sha256(source) == behrend["file_sha256"]
    assert output("git", "rev-parse", f"HEAD:{behrend['file']}", cwd=MATHLIB) == behrend["file_blob"]
    lines = source.read_bytes().splitlines(keepends=True)
    body = b"".join(lines[481:488])
    assert hashlib.sha256(body).hexdigest() == behrend["body_slice_sha256"]
    assert output(
        "git", "merge-base", "--is-ancestor", behrend["introduction_revision"], "HEAD", cwd=MATHLIB
    ) == ""
    assert output("git", "rev-parse", f"{behrend['introduction_revision']}^{{tree}}", cwd=MATHLIB) == behrend["introduction_tree"]

    defs = next(c for c in candidates if c["candidate_id"] == "M0958-C04-MATHLIB-DEFS-SUBSTRATE")
    defs_source = MATHLIB / defs["file"]
    assert sha256(defs_source) == defs["file_sha256"]
    assert output("git", "rev-parse", f"HEAD:{defs['file']}", cwd=MATHLIB) == defs["file_blob"]
    for text in (source.read_text(encoding="utf-8"), defs_source.read_text(encoding="utf-8")):
        assert not FORBIDDEN.search(without_comments_and_strings(text))

    anchor = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactElkinTarget : Prop",
        "def PinnedBehrendTarget : Prop",
        "theorem pinnedBehrendCandidate : PinnedBehrendTarget := by",
        "exact Behrend.roth_lower_bound",
        "#check_failure (rfl : ExactElkinTarget = PinnedBehrendTarget)",
        "assert_no_sorry Behrend.roth_lower_bound",
        "#print sorries Behrend.roth_lower_bound",
        "#print axioms Behrend.roth_lower_bound",
        "#print_anchor_closure",
    ):
        assert marker in anchor, marker
    assert not FORBIDDEN.search(without_comments_and_strings(anchor))

    formal_conjectures = next(c for c in candidates if c["candidate_id"] == "M0958-C06-FORMAL-CONJECTURES-RELATED-HITS")
    assert formal_conjectures["candidate_classification"] == "M5_unrelated_placeholder_statements"
    assert all(file["body"] == "by sorry" for file in formal_conjectures["files"])
    search = next(c for c in candidates if c["candidate_id"] == "M0958-C05-PUBLIC-INDEX-EXACT-QUERIES")
    assert len(search["queries"]) == 6
    assert all(query["response_sha256"] for query in search["queries"])

    decision = audit["inventory_decision"]
    assert decision["inventory_classified"] is True
    assert decision["source_boundary_coverage"].startswith("7/7")
    assert decision["exact_candidate_located"] is False
    assert decision["exact_candidate_kernel_probed"] is False
    assert decision["related_candidate_kernel_probed"] is True
    assert decision["candidate_accepted_by_master"] is False
    assert decision["root_machine_classification"] == "M3"
    expected_vector = {"H": "H1", "M": "M3", "R": "R4"}
    assert decision["authoritative_root_vector_before"] == expected_vector
    assert decision["authoritative_root_vector_after"] == expected_vector
    assert receipt["root_vector_before"] == expected_vector
    assert receipt["root_vector_after"] == expected_vector
    assert decision["kernel_closed_as_accepted_root"] is False
    assert audit["accepted_receipt_ids"] == []
    assert audit["audit_complete"] is receipt["audit_complete"] is False
    assert audit["theorem_complete"] is receipt["theorem_complete"] is False

    lean = subprocess.run(
        ["lake", "env", "lean", f"../../Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean"],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
        env={**os.environ, "LC_ALL": "C", "TZ": "UTC"},
    )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    if lean.stdout.count("Declarations are sorry-free!") != 3:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected transitive sorry report")
    normalized = re.sub(r"\s+", " ", lean.stdout)
    if normalized.count("depends on axioms: [propext, Classical.choice, Quot.sound]") != 3:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected axiom report")
    for marker in (
        "ANCHOR_CLOSURE declarations=28257 modules=1079",
        "ANCHOR_CLOSURE axioms=[propext, Classical.choice, Quot.sound]",
        "ANCHOR_CLOSURE bodyless_nonaxioms=[]",
        "ANCHOR_CLOSURE unsafe=[]",
    ):
        if marker not in lean.stdout:
            sys.stdout.write(lean.stdout)
            raise SystemExit(f"missing closure marker: {marker}")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    statement_source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    anchor_source = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    imports = "\n".join(
        line for line in (statement_source + "\n" + anchor_source).splitlines()
        if line.startswith("import ")
    )
    body = "\n".join(
        line for line in statement_source.splitlines() if not line.startswith("import ")
    )
    body += "\n" + "\n".join(
        line for line in anchor_source.splitlines() if not line.startswith("import ")
    )
    body += """

example :
    Stage1Instances.THM_M_0958.ElkinConstructionTarget =
      Stage1Instances.THM_M_0958_AnchorAudit.ExactElkinTarget := rfl
"""
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".lean", prefix="thm-m-0958-anchor-", delete=False
    ) as temporary:
        temporary.write(imports + "\n" + body)
        temporary_path = Path(temporary.name)
    try:
        identity = subprocess.run(
            ["lake", "env", "lean", str(temporary_path)],
            cwd=LEAN_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=240,
            check=False,
            env={**os.environ, "LC_ALL": "C", "TZ": "UTC"},
        )
        if identity.returncode:
            sys.stdout.write(identity.stdout)
            raise SystemExit("audit-local target is not definitionally identical to Statement.lean")
    finally:
        temporary_path.unlink(missing_ok=True)

    print(
        "check_anchor_audit: ok "
        "(THM-M-0958; 7 records; no exact Elkin candidate; related pinned Behrend body "
        "is sorry-free but mismatched; root H1/M3/R4; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
