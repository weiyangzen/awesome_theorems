#!/usr/bin/env python3
"""Fail-closed validation for the THM-M-0110 immutable anchor inventory."""

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
ITEM_ID = "S56-M-0110-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0110"
BASE_REVISION = "88a5a5c6fe6bac0d813a74ca20fa553eaf2a6d68"
BASE_TREE = "a0a75048a918a3bf566c3dbcf6b4352c3b2ee8e4"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "d0a9a0e873dd388aa37c0bcc77fce1fc38bae5911851a87570b94f50c80eecc6"
STATEMENT_SHA256 = "81e89341fc571e588c47c8984d71779fd4b90b2cd55ae70c3392c742655574dd"
PROTOCOL_SHA256 = "c947bac0403fdf50d9e1b3a24c1f628883a7447303d4e97a43766bb97a0fd462"
INVENTORY_SHA256 = "ebc44cef5ee0a085db29688e3f4f5579cbe79d0869ea14e8b475c119e6f75c66"
ANCHOR_SHA256 = "405d5f58177ea4f30e09dbb65eb3bc9ba772deb6dbe35d7d6667dda83ac4413c"
LEAN_OUTPUT_SHA256 = "02f052caab4e0fa3d04af48166e949edff1ae2d5e1b6c03f901b9621b5b8f460"
LEGACY_SHA256 = "e9e6b6d9c7df8c60b81cf6be6229be075988d237c50db0efc6a8d6cca7585232"
LEGACY_BLOB = "efb8630cc5f0b0598db2702a7d4f7b83bd1dcaae"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/README.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}
MATHLIB_SOURCES = {
    "Mathlib/AlgebraicGeometry/Modules/Sheaf.lean": (
        "8361d3a6527fc20115db196f8535168105e3af61",
        "39ad16dcfaafa9f6d6d8c3546f4fbd59153a1e25255c7ab80c98d4dcb0bcd762",
    ),
    "Mathlib/CategoryTheory/Sites/SheafCohomology/Basic.lean": (
        "fd348ffcea30facc9341994693411e8165a3d36f",
        "8765b1daa9cca22fe316be0619f110f8fff814ae1bb7a70c42f9cfbc4ba8a6f8",
    ),
    "Mathlib/Algebra/Homology/DerivedCategory/Ext/EnoughInjectives.lean": (
        "73eebed8565229496b750c83bcfe2d7905538b7c",
        "f1ddb65d3cc441f1aee9519a9acabe73164d78d539760c8fee4959970a6709a0",
    ),
    "Mathlib/AlgebraicGeometry/ProjectiveSpectrum/Proper.lean": (
        "50b0f2ffba58356c79a538871d87f33ff261063c",
        "139bce062cba8697ddd2fcb4ed211d4aac02297005412901c7ddbf4b02e3c57b",
    ),
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


def prohibited_pattern() -> re.Pattern[str]:
    terms = tuple("".join(parts) for parts in (
        ("sor", "ry"), ("ad", "mit"), ("sor", "ry", "Ax"),
        ("ax", "iom"), ("un", "safe"), ("op", "aque"),
    ))
    return re.compile(r"\b(?:" + "|".join(terms) + r")\b")


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    manifest = load(LEAN_ROOT / "lake-manifest.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == receipt["item_id"] == protocol["item_id"] == ITEM_ID
    assert audit["theorem_id"] == receipt["theorem_id"] == protocol["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 34 and audit["phase"] == "anchor_audit"
    assert audit["base_revision"] == receipt["base_revision"] == protocol["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD^{commit}") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 34
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert (item["theorem_id"], item["phase"], item["layer"]) == (THEOREM_ID, "anchor_audit", 2)
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0110-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert audit["audited_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert audit["audited_target"]["statement_file_sha256"] == STATEMENT_SHA256
    assert protocol["canonical_expression_sha256"] == EXPRESSION_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "anchor-discovery-protocol.json") == PROTOCOL_SHA256
    assert sha256(HERE / "anchor-audit.json") == INVENTORY_SHA256
    assert sha256(HERE / "AnchorAudit.lean") == ANCHOR_SHA256

    packages = {row["name"]: row for row in manifest["packages"]}
    assert packages["mathlib"]["rev"] == MATHLIB_REVISION
    assert audit["immutable_environment"]["manifest_sha256"] == sha256(LEAN_ROOT / "lake-manifest.json")
    assert output("git", "rev-parse", "HEAD^{commit}", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == audit["immutable_environment"]["mathlib_license_sha256"]
    for source, (blob, digest) in MATHLIB_SOURCES.items():
        assert output("git", "rev-parse", f"HEAD:{source}", cwd=MATHLIB) == blob
        assert sha256(MATHLIB / source) == digest

    legacy = ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_034.lean"
    assert output("git", "rev-parse", "HEAD:Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_034.lean") == LEGACY_BLOB
    assert sha256(legacy) == LEGACY_SHA256
    legacy_text = legacy.read_text(encoding="utf-8")
    assert "def StatementShape : Prop" in legacy_text
    assert "def c008ExactExternalKodairaVanishingFound : Bool := false" in legacy_text

    assert protocol["inventory_version"] == audit["discovery_protocol"]["inventory_version"]
    assert protocol["inventory_version"] == receipt["candidate_result"]["inventory_version"]
    assert protocol["saturation_claim_planned"] is False
    assert audit["discovery_protocol"]["saturation_claim"] is False
    candidates = {row["candidate_id"]: row for row in audit["candidates"]}
    assert set(candidates) == set(protocol["inventory_member_ids"])
    assert len(candidates) == receipt["candidate_result"]["classified_records"] == 8
    assert len(audit["human_source_metadata"]) == receipt["candidate_result"]["source_metadata_records"] == 2
    assert candidates["M0110-C01-REPO-LEGACY-SHAPE"]["classification"] == "M3_nonexact_statement_shape"
    assert candidates["M0110-C02-MATHLIB-SHEAF-H"]["classification"] == "M3_exact_carrier_only"
    assert candidates["M0110-C03-MATHLIB-ZERO-SHEAF"]["classification"] == "M3_stronger_premise_near_anchor"
    assert candidates["M0110-C04-MATHLIB-INJECTIVE-EXT"]["classification"] == "M3_stronger_premise_near_anchor"
    assert candidates["M0110-C05-MATHLIB-PROJ-PROPER"]["classification"] == "M3_geometric_substrate_only"
    atlas = candidates["M0110-C06-ATLAS-KODAIRA-NAME-MATCHES"]
    assert atlas["revision"] == "34ffed396f376454c1a9b297f3fd74c5c801fb50"
    assert atlas["tree"] == "c12fe2315fe475d70a4fcee81d6b731f853373ab"
    assert atlas["file_sha256"] == "be356467d0adad4914b14bb9b25d1d3347576b6b3411141130d31347126ae37c"
    assert len(atlas["adjacent_algebraic_geometry_files"]) == 7
    assert atlas["classification"] == "M5_statement_mismatch_and_placeholders"
    physlib = candidates["M0110-C07-PHYSLIB-KODAIRA-FIBERS"]
    assert physlib["revision"] == "851e49a321d5a8dad4da23583da422f569c53cb4"
    assert physlib["classification"] == "M5_name_collision_and_statement_mismatch"
    assert candidates["M0110-C08-FORMAL-CONJECTURES-NEGATIVE"]["classification"] == "no_candidate"

    root = audit["root_decision"]
    assert root["inventory_classified"] is True
    assert root["exact_mathlib_terminal_candidate_found"] is False
    assert root["exact_external_terminal_candidate_found"] is False
    assert root["external_kernel_closure_candidate_found"] is False
    assert root["eligible_repo_local_integration_debt"] is False
    assert root["classification_before"] == root["classification_after_proposed"] == "M3"
    assert root["kernel_closed"] is False
    assert "do not constrain" in root["first_failed_gate"]
    assert audit["root_vector_before"] == audit["root_vector_after_proposed"]
    assert audit["node_self_tested"] is True
    assert audit["audit_complete"] is False and audit["theorem_complete"] is False
    assert audit["accepted_receipt_ids"] == []

    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["artifact_sha256"]["anchor_probe"] == ANCHOR_SHA256
    assert receipt["artifact_sha256"]["anchor_probe_output"] == LEAN_OUTPUT_SHA256
    assert receipt["artifact_sha256"]["discovery_protocol"] == PROTOCOL_SHA256
    assert receipt["artifact_sha256"]["anchor_inventory"] == INVENTORY_SHA256
    assert receipt["root_vector_before"] == receipt["root_vector_after_proposed"] == audit["root_vector_after_proposed"]
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []

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
        "abbrev AuditedCohomology",
        "theorem subsingletonCohomology_of_isZero",
        "#check CategoryTheory.Sheaf.H",
        "#check CategoryTheory.Sheaf.subsingleton_H_of_isZero",
        "#check CategoryTheory.Abelian.Ext.subsingleton_of_injective",
        "IsProper (Proj.toSpecZero",
        "#print axioms subsingletonCohomology_of_isZero",
    ):
        assert marker in probe, marker
    forbidden = prohibited_pattern()
    assert forbidden.search(without_comments(probe)) is None

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0110/AnchorAudit.lean"],
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
        "CategoryTheory.Sheaf.subsingleton_H_of_isZero",
        "CategoryTheory.Abelian.Ext.subsingleton_of_injective",
        "Stage1Instances.THMM0110.AnchorAudit.subsingletonCohomology_of_isZero",
        "IsZero ((SheafOfModules.toSheaf D.X.ringCatSheaf).obj D.KTensorL)",
        "depends on axioms: [propext, Classical.choice, Quot.sound]",
    )
    for marker in required_output:
        if marker not in lean.stdout:
            sys.stdout.write(lean.stdout)
            raise SystemExit(f"missing Lean evidence: {marker}")
    if "sorryAx" in lean.stdout:
        raise SystemExit("unexpected sorryAx in anchor probe")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("anchor probe output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0110; 8 classified candidates; 2 source metadata records; "
        "no exact terminal candidate; accepted root M3; audit_complete=false; "
        "theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
