#!/usr/bin/env python3
"""Validate the immutable, target-owned THM-M-0741 anchor audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
AUDIT_PATH = HERE / "anchor-audit.json"
ITEM_ID = "S56-M-0741-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0741"
RANK = 1329
BASE_REVISION = "561d83df037004ceb2259292d7c63be930b40391"
BASE_TREE = "6eb02475bf5a70139d60615c924b31c930efc2bb"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_FILE_BLOB = "0834371356762db805d37208b9cf8a1fc0efd217"
EXPRESSION_SHA256 = "1a96ad274a14ef0c7285734258d28a7ff6e49febe1470bfbb957d757a92e718c"
STATEMENT_SHA256 = "79e8f14fa5219760ef0fa3b26c95ebe40916f0ed2881a6491fce36944398d4c7"
ANCHOR_SHA256 = "c88e2e959eb7aecf19c6b3fd6a214817480143e2ebeba096250cd0d33b1dbdff"
LEAN_OUTPUT_SHA256 = "fab3027faad883fb79d137cf92097c7df793687d00e0b4253bfbdeee71596ba5"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
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


def main() -> None:
    audit = load(AUDIT_PATH)
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = load(packet_path) if packet_path.exists() else None

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["normative_profile"] == "machine-theorem-assurance/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == RANK
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert output("git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD") == ""

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == RANK
    assert target["name"] == "\u505c\u673a\u95ee\u9898" and target["category"] == "\u6570\u7406\u903b\u8f91 / \u9012\u5f52\u8bba"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    statement_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0741-STATEMENT"
    )
    assert statement_item["state"] == "[_]"
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0741-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0741.HaltingProblemUndecidable"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "AnchorAudit.lean") == ANCHOR_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]

    terminal = next(
        candidate
        for candidate in audit["candidates"]
        if candidate["candidate_id"] == "M0741-C02-MATHLIB-FIXED-INPUT"
    )
    assert terminal["revision"] == MATHLIB_REVISION and terminal["tree"] == MATHLIB_TREE
    assert terminal["file_blob"] == MATHLIB_FILE_BLOB
    assert output("git", "rev-parse", f"HEAD:{terminal['file']}", cwd=MATHLIB) == MATHLIB_FILE_BLOB
    terminal_source = MATHLIB / terminal["file"]
    assert sha256(terminal_source) == terminal["file_sha256"]
    assert terminal["declaration"] == "ComputablePred.halting_problem"
    assert terminal["local_adapter"].endswith("exactTarget_of_pinnedMathlibAnchor")
    assert terminal["candidate_classification"] == "M3"
    assert terminal["eligible_route_shape_after_E1"] == "M0-W"
    assert terminal["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert output(
        "git", "merge-base", "--is-ancestor", terminal["historical_provenance"]["lean4_port_commit"],
        MATHLIB_REVISION, cwd=MATHLIB
    ) == ""

    source = terminal_source.read_text(encoding="utf-8")
    for marker in (
        "theorem rice (C : Set (\u2115 \u2192. \u2115))",
        "theorem halting_problem (n) : \u00acComputablePred fun c => (eval c n).Dom",
        "| h => rice { f | (f n).Dom } h Nat.Partrec.zero Nat.Partrec.none trivial",
    ):
        assert marker in source, marker
    terminal_region = source[source.index("theorem rice "):source.index("-- Post's theorem")]
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(terminal_region))

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "Not (ComputablePred fun programInput : Code × Nat =>",
        "theorem exactTarget_of_pinnedMathlibAnchor : ExactTarget",
        "apply ComputablePred.halting_problem 0",
        "pairComputable.comp (Computable.id.pair (Computable.const 0))",
        "#print ComputablePred.halting_problem",
        "#print axioms exactTarget_of_pinnedMathlibAnchor",
    ):
        assert marker in adapter, marker
    assert not forbidden.search(without_comments(adapter))

    adjacent = next(
        candidate
        for candidate in audit["candidates"]
        if candidate["candidate_id"] == "M0741-C03-MATHLIB-ADJACENT"
    )
    assert {declaration["name"] for declaration in adjacent["declarations"]} == {
        "ComputablePred.halting_problem_re",
        "ComputablePred.halting_problem_not_re",
        "ComputablePred.rice",
    }
    assert all(declaration["type"] and declaration["role"] for declaration in adjacent["declarations"])
    assert adjacent["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert "machine #print axioms" in adjacent["placeholder_bodyless_unsafe_oracle_status"]

    duplicate = next(
        candidate
        for candidate in audit["candidates"]
        if candidate["candidate_id"] == "M0741-C04-REPO-DUPLICATE-FAMILY"
    )
    assert duplicate["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert duplicate["disposition"] == "cross_target_discovery_lead_only"

    external = next(
        candidate
        for candidate in audit["candidates"]
        if candidate["candidate_id"] == "M0741-C05-FOUNDATION-COMMENTED"
    )
    assert external["revision"] == "c28942b7d9d0df41ee5b736602c3f27b8643532c"
    assert external["tree"] == "c9261b0eb941962daa02a999b1d67bb4ecfd0e21"
    assert external["source_archive_sha256"] == (
        "477e62680d4fe1d2629fc652c39b55bf04ee38eb76afe85c5c2341f05e935975"
    )
    assert external["file_sha256"] == (
        "c1198082f4806bf803cc813d41cdcedb31470940bc6400fe68e1b26efc7b6fe4"
    )
    assert external["candidate_classification"] == "M5"
    assert "statement mismatch" in external["blocker"]
    assert "comment" in external["placeholder_bodyless_unsafe_oracle_status"]
    assert "sorry" in external["placeholder_bodyless_unsafe_oracle_status"]

    searches = audit["external_searches"]
    assert len(searches) == 8
    assert all(search.get("result") and search.get("immutability_boundary") for search in searches)
    response_hashes = {
        search["response_sha256"] for search in searches if "response_sha256" in search
    }
    assert response_hashes == {
        "19ea6474c58f3025ce2e1aaabab50c330921c008639efc4099bcebb60e7f85e3",
        "f4423b5ede1ee69ffcdcb94a61aad9c5b398c072d086b8d0d7f974dd5218a782",
        "0872ba0b9cc5b36d6092103119871e7e1b4ef5da051176546a0d59e953481496",
        "cf453664473c940c73660a149cc2f6bae64fbb67b40afae9a7b5f52f86cf8f6d",
        "1db366a292a73aaa6963398fe4e4bdb2b42e9b7a2d745a0878210569945e386e",
        "477e62680d4fe1d2629fc652c39b55bf04ee38eb76afe85c5c2341f05e935975",
    }
    grep_search = next(search for search in searches if search["surface"] == "grep.app code search")
    assert set(grep_search["response_sha256_values"]) == {
        "cb991ea2af7df20afc24f1654561e33b7b78746124984bd5361d7704b61ea915",
        "725dd29c1255def706659bc07f8947efa948e1e91833579860dd4e6bd2f9668b",
    }
    assert audit["discovery_protocol"]["saturation_claim"] is False
    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("5/5")
    assert result["exact_candidate_located"] is True
    assert result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["candidate_route_classification"] == "M3"
    assert result["eligible_route_shape_after_E1"] == "M0-W"
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M3"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["root_candidate_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }
    assert result["accepted_root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    provenance = audit["provenance_packet"]
    assert provenance["terminal_declaration"] == "ComputablePred.halting_problem 0"
    assert "Iff.rfl" in provenance["canonical_identity_check"]
    assert provenance["transitive_trust_closure_hash"] is None
    assert audit["known_limitations"]

    classifications = {candidate["candidate_classification"] for candidate in audit["candidates"]}
    assert classifications <= {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    prior_files = set(load(HERE / "instance.json")["owned_artifacts"])
    anchor_files = {
        "AnchorAudit.lean",
        "anchor-audit-receipt.json",
        "anchor-audit-validation.md",
        "anchor-audit.json",
        "check_anchor_audit.py",
    }
    assert prior_files | anchor_files <= actual_files

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"].startswith("worker_self_tested_anchor_inventory")
    assert receipt["supersession_state"] and receipt["review_due"]
    assert receipt["incident_path"] and receipt["invalidation_inputs"]
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["classification"] == "M3"
    assert receipt["candidate_result"]["eligible_route_shape_after_E1"] == "M0-W"
    assert receipt["candidate_result"]["evidence_level"] == "node_local_below_E1"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["content_addressed_recipe_or_receipt_ids"] == []
    impact = receipt["ownership_and_change_impact"]
    assert impact["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert impact["change_impact_set"] == [ITEM_ID]
    assert impact["cross_target_credit"] == []
    recipes = {recipe["recipe_id"]: recipe for recipe in receipt["structured_validation_recipes"]}
    lean_recipe = recipes["S56-M-0741-ANCHOR-AUDIT-LEAN"]
    ledger_recipe = recipes["S56-M-0741-ANCHOR-AUDIT-LEDGER"]
    assert not any("CombinedAudit" in name for name in lean_recipe["covered_declarations"])
    assert {
        "Stage1Instances.THM_M_0741_CombinedAudit.canonicalTarget_iff_auditTarget",
        "Stage1Instances.THM_M_0741_CombinedAudit.canonicalTarget_of_auditCandidate",
    } <= set(ledger_recipe["covered_declarations"])

    if packet is not None:
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
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]
        assert isinstance(packet["commands"], list) and packet["commands"]
        assert isinstance(packet["output_summary"], str) and packet["output_summary"]

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0741/AnchorAudit.lean"],
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
    normalized = re.sub(r"\s+", " ", lean.stdout)
    expected_axioms = "[propext, Classical.choice, Quot.sound]"
    if normalized.count(expected_axioms) != 2:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected terminal or adapter axiom report")
    if "theorem ComputablePred.halting_problem" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("terminal proof body was not printed")
    if "sorry" in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("Lean output contains a proof placeholder")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    anchor_without_import = adapter.replace("import Mathlib.Computability.Halting\n", "", 1)
    combined = (
        (HERE / "Statement.lean").read_text(encoding="utf-8")
        + "\n"
        + anchor_without_import
        + """

namespace Stage1Instances.THM_M_0741_CombinedAudit

theorem canonicalTarget_iff_auditTarget :
    Stage1Instances.THM_M_0741.HaltingProblemUndecidable <->
      Stage1Instances.THM_M_0741_AnchorAudit.ExactTarget :=
  Iff.rfl

theorem canonicalTarget_of_auditCandidate :
    Stage1Instances.THM_M_0741.HaltingProblemUndecidable :=
  Stage1Instances.THM_M_0741_AnchorAudit.exactTarget_of_pinnedMathlibAnchor

#print axioms canonicalTarget_iff_auditTarget
#print axioms canonicalTarget_of_auditCandidate

end Stage1Instances.THM_M_0741_CombinedAudit
"""
    )
    with tempfile.TemporaryDirectory(prefix="thm-m-0741-anchor-") as directory:
        combined_path = Path(directory) / "CombinedAudit.lean"
        combined_path.write_text(combined, encoding="utf-8")
        identity = subprocess.run(
            ["lake", "env", "lean", str(combined_path)],
            cwd=LEAN_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
    if identity.returncode:
        sys.stdout.write(identity.stdout)
        raise SystemExit(identity.returncode)
    identity_normalized = re.sub(r"\s+", " ", identity.stdout)
    if identity_normalized.count(expected_axioms) < 4:
        sys.stdout.write(identity.stdout)
        raise SystemExit("combined canonical identity/candidate axiom checks are missing")
    if "sorryAx" in identity.stdout:
        sys.stdout.write(identity.stdout)
        raise SystemExit("combined canonical check depends on a proof placeholder")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0741; 5 candidates; exact pinned mathlib M0-W-shaped route kernel-checked; "
        "evidence below E1; accepted root M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
