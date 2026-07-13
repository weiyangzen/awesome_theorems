#!/usr/bin/env python3
"""Validate the immutable, bounded THM-M-0034 anchor inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0034-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0034"
BASE_REVISION = "75ab5edd624df749325d391b41b669f8d72774b2"
BASE_TREE = "26562e2b8168d91a92a8164c9d8f0fc55178836e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "d80cc9860ed5a53c81a0851b4dc8e702aa5a23d448f373ae6d68ed0c9b5604b1"
STATEMENT_SHA256 = "cfdfeabe825f5b7936905cee310c2306dba8b18a4b25281fb09c7d10719b79e8"
LEAN_OUTPUT_SHA256 = "4e496fba18af17d5ac823408da9019eda983c5e72fb922fd12fcd12fa575a6f3"
ANCHOR_FILE_SHA256 = "85ddef200d365bbedd4753c94ae54ccd17d8b1a075a5b8d514b3cb49f47ddea2"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1078 and audit["phase"] == "anchor_audit"
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1078
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0034-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert statement["canonical_formal_target"]["statement_file_sha256"] == STATEMENT_SHA256
    assert audit["canonical_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "AnchorAudit.lean") == ANCHOR_FILE_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]

    assert protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID
    assert protocol["inventory_version"] == audit["discovery_protocol"]["inventory_version"]
    assert protocol["canonical_expression_sha256"] == EXPRESSION_SHA256
    assert protocol["saturation_claim_planned"] is False
    assert audit["discovery_protocol"]["frozen_before_candidate_classification"] is True
    assert audit["discovery_protocol"]["saturation_claim"] is False

    candidates = {candidate["candidate_id"]: candidate for candidate in audit["candidates"]}
    assert set(candidates) == {
        "M0034-C01-MATHLIB-SUPPORT",
        "M0034-C02-EDMUND-EXACT",
        "M0034-C03-MBKYBKY-PID",
        "M0034-C04-ATLAS-NAME-COLLISION",
        "M0034-C05-FORMAL-CONJECTURES-NEGATIVE",
    }
    support = candidates["M0034-C01-MATHLIB-SUPPORT"]
    assert support["candidate_classification"] == "M3_support_only"
    assert support["tracked_mathlib_lean_files_searched"] == 7871
    for file, blob in support["source_blobs"].items():
        assert output("git", "rev-parse", f"HEAD:{file}", cwd=MATHLIB) == blob
        assert sha256(MATHLIB / file) == support["source_sha256"][file]

    exact = candidates["M0034-C02-EDMUND-EXACT"]
    assert exact["revision"] == "e8d85a6f6fa210ba0be12bd02aa22009699f0c35"
    assert exact["archive_sha256"] == "6072221d080e634f0a9775518855557fce0495cf4004848e4cb57dda4aa7e6d2"
    assert exact["declaration"] == "QuillenSuslin.quillenSuslin"
    assert exact["file_blob"] == "65b21ef0969d7dc5401baa66eda5b0260567a7b4"
    assert exact["file_sha256"] == "15496d2272b3d481d0158a0c18cf4444d03376dc24edd085d797f29b4317cd4c"
    assert exact["toolchain"] == "leanprover/lean4:v4.29.0"
    assert exact["mathlib_revision"] == MATHLIB_REVISION
    assert exact["production_lean_files"] == 76
    assert "0 sorry, 0 #exit, 0 native_decide, 0 axiom" in exact["placeholder_audit"]
    assert exact["license"].startswith("unknown")
    assert exact["candidate_classification"] == "M3_exact_formal_source_anchor"
    assert exact["evidence_level"] == "E3"

    pid = candidates["M0034-C03-MBKYBKY-PID"]
    assert pid["revision"] == "51ed173b17b274e61f759556ab3e1c090267d1bd"
    assert pid["tree"] == "264c487a24b2158bf8432459fd0b1e326acdf1eb"
    assert pid["file_blob"] == "2694d34f828fc5e60608cff60fba7058d69a56ea"
    assert pid["candidate_classification"] == "M1_external_kernel_closure_incompatible_pin"
    assert "completed successfully" in pid["upstream_ci"]
    collision = candidates["M0034-C04-ATLAS-NAME-COLLISION"]
    assert collision["terminal_proof_body"] == "by sorry"
    assert collision["candidate_classification"] == "M5_statement_mismatch_and_placeholder"
    assert candidates["M0034-C05-FORMAL-CONJECTURES-NEGATIVE"]["candidate_classification"] == "no_candidate"

    assert len(audit["external_searches"]) == 10
    assert any("HTTP 401" in row["result"] for row in audit["external_searches"])
    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("5/5 candidate records classified")
    assert result["exact_external_source_candidate_located"] is True
    assert result["external_kernel_closure_candidate_located"] is True
    assert result["eligible_repo_local_integration_debt"] is True
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_debt_candidate_after"] == "M1"
    assert result["root_machine_debt_accepted_after"] == "M3"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert audit["audit_complete"] is False and audit["theorem_complete"] is False

    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["anchor_probe_file_sha256"] == ANCHOR_FILE_SHA256
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["candidate_result"]["classified_records"] == 5
    assert receipt["candidate_result"]["exact_external_source_candidate_found"] is True
    assert receipt["candidate_result"]["external_kernel_closure_candidate_found"] is True
    assert receipt["candidate_result"]["candidate_root_classification"] == "M1"
    assert receipt["candidate_result"]["accepted_root_classification"] == "M3"
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False

    required_packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet) == required_packet_fields
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]

    probe = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "def ExternalFieldCandidate : Prop",
        "theorem externalFieldCandidate_implies_exact",
        "def ExternalPIDCandidate : Prop",
        "theorem externalPIDCandidate_implies_exact",
        "#check Module.Flat.of_projective",
        "#check Module.free_of_flat_of_isLocalRing",
        "#check (inferInstance : Module.Flat",
        "#check_failure (inferInstance : Module.Free",
        "#print axioms externalPIDCandidate_implies_exact",
        "#print ExactTarget",
    ):
        assert marker in probe, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(probe))

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0034/AnchorAudit.lean"],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    required_output = (
        "inferInstance : Module.Flat (MvPolynomial (Fin n) k) P",
        "failed to synthesize instance of type class\n  Module.Free (MvPolynomial (Fin n) k) P",
        "'Stage1Instances.THM_M_0034_AnchorAudit.externalPIDCandidate_implies_exact' depends on axioms",
        "'Stage1Instances.THM_M_0034_AnchorAudit.externalFieldCandidate_implies_exact' depends on axioms",
        "def Stage1Instances.THM_M_0034_AnchorAudit.ExactTarget.{u, v} : Prop",
    )
    for marker in required_output:
        if marker not in lean.stdout:
            sys.stdout.write(lean.stdout)
            raise SystemExit(f"missing Lean evidence: {marker}")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("anchor probe output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0034; 5 classified records; exact E3 source plus provisional M1 older-pin candidate; "
        "accepted root M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
