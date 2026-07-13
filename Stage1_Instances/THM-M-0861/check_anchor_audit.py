#!/usr/bin/env python3
"""Validate the bounded immutable THM-M-0861 formal-anchor inventory."""

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
ITEM_ID = "S56-M-0861-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0861"
BASE_REVISION = "9c75282d42a7ef447d885d1d56997a79418bcd8a"
BASE_TREE = "cc5285432a02107fadffb68c698690d1b98ac5f2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "4e7919ed3b44379a42d69ef88cfb5e512248eccfe755392723cb6769c4f8e197"
STATEMENT_SHA256 = "a6ce9ee3edd720d38fa9306324e38b48d5f0430a8b9513b9207e7808ea1b380d"
PROTOCOL_SHA256 = "a7813bbe56a888df8ffe12465725f494f55084a6498529a6444db0b672a1a253"
ANCHOR_LEAN_SHA256 = "d109f2336caa28e017313e05572986ec1e1e2311d267b486789fb240552628e6"
LEAN_OUTPUT_SHA256 = "015cf7091d852e2453c600ea0f5d4ab6c5c4785f9707584b32401fcb3a6bec9d"
MATHLIB_FILES = {
    "Mathlib/Combinatorics/Graph/Basic.lean":
        ("72ae0789f49228ac2fb458a9bf7da842d0638190",
         "dc3f9c7793f8de09261868afeb7e1d8804914b90b1fc4615feb139f2452dd2b9"),
    "Mathlib/Combinatorics/SimpleGraph/Bipartite.lean":
        ("7263d4c6eed57420f67b01639947965ec952d74c",
         "5402f4cd073b757a9d1bd127cbbca9f9a2b0750c8c9edb7e2361df32312acf3f"),
    "Mathlib/Combinatorics/SimpleGraph/EdgeLabeling.lean":
        ("2b6c7b330727ccc5de9ab88dbcc71737697cff80",
         "6f0181a9b0a003bd703d81f609d5e30779d5543aa31dfc32f4b15c6e6c51b3f9"),
    "Mathlib/Combinatorics/SimpleGraph/LineGraph.lean":
        ("786371783f21afc25193d940fb6655c6f196d58c",
         "8d938aa393a544cb7f20fe34176ec005702363991f978f7ccb394c7276ab401f"),
    "Mathlib/Combinatorics/SimpleGraph/Coloring.lean":
        ("8d32158848f9f8d4c34cfdf49bd66fd5604adae1",
         "42c4c6ac9c763df08f33a9fc4cf329e19908dacc630be771a547fcb583f7be56"),
    "Mathlib/Combinatorics/SimpleGraph/Finite.lean":
        ("a111f858a1b79cae5c68eaa94bfdf104c50063cf",
         "968b2c58d0e77e91c69815bf1ed5e3fafa7302eaebc08139d9fdbb323ad910e8"),
    "Mathlib/Combinatorics/SimpleGraph/Hall.lean":
        ("6bd653c1e0cec51aadbd460e67919d9499226f97",
         "e7ffa1e4de6af950973d02725efd8d2bbbb015e2f05b4b45a52148244a2a5f5e"),
    "Mathlib/Combinatorics/Hall/Basic.lean":
        ("5cda9c0e906803f10f1f50b916d564ebb443ac95",
         "dab48f10ac7d10b7190b88f8b7e2447b55be1af098358a9f5318d66c675b2382"),
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def candidate(audit: dict, candidate_id: str) -> dict:
    return next(c for c in audit["candidates"] if c["candidate_id"] == candidate_id)


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1415
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1415
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0861-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256

    assert protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0"
    assert protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID
    assert protocol["protocol_id"] == audit["discovery_protocol"]["protocol_id"]
    assert protocol["saturation_claim"] is False
    assert sha256(HERE / "anchor-discovery-protocol.json") == PROTOCOL_SHA256
    assert audit["discovery_protocol"]["sha256"] == PROTOCOL_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["lake_manifest_sha256"]
    assert sha256(LEAN_ROOT / "lean-toolchain") == env["lean_toolchain_file_sha256"]
    for path, (blob, digest) in MATHLIB_FILES.items():
        source = MATHLIB / path
        assert output("git", "rev-parse", f"HEAD:{path}", cwd=MATHLIB) == blob
        assert sha256(source) == digest

    candidate_ids = {c["candidate_id"] for c in audit["candidates"]}
    assert len(audit["candidates"]) == len(candidate_ids) == 7
    assert candidate_ids == {
        "M0861-C01-REPO-LOCAL-STATEMENT",
        "M0861-C02-MATHLIB-MULTIGRAPH-SUBSTRATE",
        "M0861-C03-MATHLIB-SIMPLEGRAPH-COLORING-SUBSTRATE",
        "M0861-C04-MATHLIB-HALL-SUBSTRATE",
        "M0861-C05-FORMAL-CONJECTURES-EDGE-PARTITION",
        "M0861-C06-ATLAS-KONIG-MATCHING-NONSUBSTITUTE",
        "M0861-C07-MATHLIB-PR33032-MATCHING-NONSUBSTITUTE",
    }
    assert candidate(audit, "M0861-C01-REPO-LOCAL-STATEMENT")["candidate_classification"] == "M3_statement_only"
    assert candidate(audit, "M0861-C02-MATHLIB-MULTIGRAPH-SUBSTRATE")["candidate_classification"] == "M3_substrate_only"
    assert candidate(audit, "M0861-C03-MATHLIB-SIMPLEGRAPH-COLORING-SUBSTRATE")["candidate_classification"] == "M3_substrate_only"
    assert candidate(audit, "M0861-C04-MATHLIB-HALL-SUBSTRATE")["candidate_classification"] == "M3_support_only"
    formal_conjectures = candidate(audit, "M0861-C05-FORMAL-CONJECTURES-EDGE-PARTITION")
    assert formal_conjectures["revision"] == "b2e608fc52d765510915a244bb69b1a2741acc3c"
    assert formal_conjectures["tree"] == "40d17fde4b874af651386e646081f453377ea020"
    assert formal_conjectures["file_blob"] == "ffbc91afd929294affd17f90fe3f78ef45414d4c"
    assert formal_conjectures["file_sha256"] == "bb210a857d62dd09f8f14aaf87b37bb8ac88cc0d6c35d9e871f159c5e5714147"
    assert formal_conjectures["candidate_classification"] == "M3_mismatched_interface_only"
    atlas = candidate(audit, "M0861-C06-ATLAS-KONIG-MATCHING-NONSUBSTITUTE")
    assert atlas["revision"] == "34ffed396f376454c1a9b297f3fd74c5c801fb50"
    assert atlas["tree"] == "c12fe2315fe475d70a4fcee81d6b731f853373ab"
    assert atlas["file_blob"] == "21b72693bd00726262cab7d5faddc44aea8c07dd"
    assert atlas["file_sha256"] == "15aac02e02d67d36d1ff8ec0cda4a73c8bb6270ae88deb2f8519bdb0c99855d1"
    assert atlas["transitive_placeholder"]["token"] == "sorry"
    assert "sorryAx" in atlas["machine_axioms"]
    assert atlas["candidate_classification"] == "M5_wrong_theorem_and_placeholder"
    pull_request = candidate(audit, "M0861-C07-MATHLIB-PR33032-MATCHING-NONSUBSTITUTE")
    assert pull_request["revision"] == "6cfc4b1f77aef6f7f70f8f733cefa8eafc5a3497"
    assert pull_request["tree"] == "a94eee877a43b09cc0748e862fffe774de606ff1"
    assert pull_request["candidate_classification"] == "M5_statement_mismatch"
    assert {entry["blob"] for entry in pull_request["files"]} == {
        "4bdc03b6c00cd2e0c3857c11fd4de72372892b06",
        "a59c3026476e2c3edb37db2750ea4f3a6fd9ab61",
        "31c555ba2999061756069512fc638719c11d078b",
    }

    edge_labeling = (MATHLIB / "Mathlib/Combinatorics/SimpleGraph/EdgeLabeling.lean").read_text()
    assert "we reserve that terminology for labelings where incident edges cannot share a\nlabel" in edge_labeling
    assert output(
        "git", "merge-base", "--is-ancestor",
        "5010acf37f7bd8866facb77a3b2ad5be17f2510a", MATHLIB_REVISION,
        cwd=MATHLIB,
    ) == ""
    assert output(
        "git", "merge-base", "--is-ancestor",
        "921b8d39f71a5c813b526f38e4033417d40b4c3d", MATHLIB_REVISION,
        cwd=MATHLIB,
    ) == ""

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("7/7 frozen candidate groups classified")
    assert result["exact_candidate_located"] is False
    assert result["exact_candidate_kernel_checked"] is False
    assert result["substrate_candidates_kernel_checked"] is True
    assert result["independent_external_exact_terminal_body_found"] is False
    assert result["eligible_external_integration_debt"] is False
    assert result["candidate_accepted_by_master"] is False
    assert result["authoritative_root_machine_debt_before"] == "M4"
    assert result["root_machine_candidate_after"] == "M3"
    assert result["authoritative_root_machine_debt_after"] == "M4"
    assert result["candidate_root_evidence_level"] == "E3"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert audit["audit_complete"] is False and audit["theorem_complete"] is False
    assert audit["accepted_receipt_ids"] == []

    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "anchor_audit" and receipt["intent"] == "audit"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []

    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["state"] == "[_]" and packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]

    adapter_path = HERE / "AnchorAudit.lean"
    adapter = adapter_path.read_text(encoding="utf-8")
    assert sha256(adapter_path) == ANCHOR_LEAN_SHA256
    for marker in (
        "def ExactTarget : Prop",
        "IsBipartite G -> HasChromaticIndex G (maxDegree G vertexFinite)",
        "#check SimpleGraph.EdgeLabeling",
        "#check SimpleGraph.chromaticNumber",
        "#check SimpleGraph.exists_isPerfectMatching_of_forall_ncard_le",
        "#check_failure (SimpleGraph.lineGraph_adj_iff_exists : ExactTarget.{u, v})",
        "#print sorries SimpleGraph.exists_isPerfectMatching_of_forall_ncard_le",
    ):
        assert marker in adapter, marker
    stripped_adapter = without_comments(adapter)
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe|opaque)[ \t]", re.MULTILINE)
    # `#print sorries` is an audit command, not a placeholder declaration.
    stripped_adapter = re.sub(r"^#print sorries .*?$", "", stripped_adapter, flags=re.MULTILINE)
    assert not forbidden.search(stripped_adapter)

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0861/AnchorAudit.lean"],
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
    assert lean.stdout.count("Type mismatch") == 2
    assert lean.stdout.count("Declarations are sorry-free!") == 3
    assert lean.stdout.count("depends on axioms: [propext, Classical.choice, Quot.sound]") == 3
    assert "def Stage1Instances.THM_M_0861_AnchorAudit.ExactTarget.{u, v} : Prop" in lean.stdout
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("anchor Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0861; 7 candidate groups; no exact Lean body; pinned substrate M3/E3; "
        "candidate root H1/M3/R4; authoritative root remains H1/M4/R4; "
        "audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
