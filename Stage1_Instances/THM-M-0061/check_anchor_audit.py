#!/usr/bin/env python3
"""Validate the immutable, locally checkable THM-M-0061 anchor ledger."""

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
AUDIT_PATH = HERE / "anchor-audit.json"
ITEM_ID = "S56-M-0061-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0061"
BASE_REVISION = "eb9c2192f79a480deff66d2c0f8e31032bcc2d9f"
BASE_TREE = "57b76c2fceacd8819b0ec8b9abcd42cfcc74b8e2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "adff72e9052ea17e3b6e4349c23028f35f4b8e3c610ea5f9f3b4fc02fe136836"
STATEMENT_SHA256 = "386d2d25cc7fe5f55f26438e1bc749eb5953e251b48591d3e47247b733bfdc7d"
LEAN_OUTPUT_SHA256 = "ea79a8bfbb29bf0771525dc77e39821179355c5518b546d23d6113d43fe200dc"
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
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1093
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["classification"] == "M0-W"
    assert receipt["candidate_result"]["evidence_level"] == "E2"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    if packet is not None:
        expected_fields = {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert set(packet) == expected_fields
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1093
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0061-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]
    assert sha256(LEAN_ROOT / "lean-toolchain") == env["toolchain_file_sha256"]

    direct = next(c for c in audit["candidates"] if c["candidate_id"] == "M0061-C01-MATHLIB-DIRECT")
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["file_blob"] == output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB)
    assert sha256(MATHLIB / direct["file"]) == direct["file_sha256"]
    assert direct["declaration"] == "Subgroup.card_subgroup_dvd_card"
    assert direct["candidate_classification"] == "M0-W"
    assert direct["evidence_level"] == "E2"
    for name, revision in direct["historical_provenance"].items():
        if name.endswith("commit"):
            assert output("git", "merge-base", "--is-ancestor", revision, MATHLIB_REVISION, cwd=MATHLIB) == ""

    card_source = (MATHLIB / direct["file"]).read_text(encoding="utf-8")
    for marker in (
        "public import Mathlib.GroupTheory.Coset.Basic",
        "public import Mathlib.SetTheory.Cardinal.Finite",
        "assert_not_exists Field",
        "theorem card_eq_card_quotient_mul_card_subgroup (s : Subgroup α)",
        "rw [← Nat.card_prod]; exact Nat.card_congr Subgroup.groupEquivQuotientProdSubgroup",
        "theorem card_subgroup_dvd_card (s : Subgroup α) : Nat.card s ∣ Nat.card α := by",
        "classical simp [card_eq_card_quotient_mul_card_subgroup s, @dvd_mul_left ℕ]",
    ):
        assert marker in card_source, marker
    assert sha256(MATHLIB / "Mathlib/GroupTheory/Coset/Basic.lean") == receipt["immutable_inputs"]["mathlib_basic_source_sha256"]
    assert sha256(MATHLIB / "Mathlib/SetTheory/Cardinal/Finite.lean") == receipt["immutable_inputs"]["mathlib_cardinal_finite_source_sha256"]

    support = next(c for c in audit["candidates"] if c["candidate_id"] == "M0061-C02-MATHLIB-PRODUCT-IDENTITY")
    additive = next(c for c in audit["candidates"] if c["candidate_id"] == "M0061-C03-MATHLIB-ADDITIVE")
    external = next(c for c in audit["candidates"] if c["candidate_id"] == "M0061-C04-MANIFEST-EXTERNAL-CLOSURE")
    public = next(c for c in audit["candidates"] if c["candidate_id"] == "M0061-C05-PUBLIC-GROUP-THEORY-REPOSITORIES")
    assert support["candidate_classification"] == "M3_support_duplicate"
    assert additive["candidate_classification"] == "M3_domain_mismatch_duplicate"
    assert external["candidate_classification"] == "M4_no_candidate_located"
    assert public["candidate_classification"] == "M4_no_candidate_located"
    assert len(public["immutable_revisions"]) == 2

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "forall (G : Type u) [Group G] [Finite G] (H : Subgroup G)",
        "theorem exactTarget_mathlib_candidate : ExactTarget.{u}",
        "exact Subgroup.card_subgroup_dvd_card H",
        "#print Subgroup.card_subgroup_dvd_card",
        "#print Subgroup.card_eq_card_quotient_mul_card_subgroup",
        "#print axioms AddSubgroup.card_addSubgroup_dvd_card",
        "#print axioms exactTarget_mathlib_candidate",
    ):
        assert marker in adapter, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(adapter))
    assert not forbidden.search(without_comments(card_source))

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("5/5 classified candidates")
    assert result["exact_candidate_located"] is True
    assert result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M0-W"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["root_evidence_level"] == "E2"
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert audit["discovery_protocol"]["saturation_claim"] is False

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0061/AnchorAudit.lean"],
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
    if normalized.count("propext, Classical.choice, Quot.sound") != 4:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected candidate axiom report")
    if "theorem Subgroup.card_subgroup_dvd_card" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate proof-body print is missing")
    if "theorem Subgroup.card_eq_card_quotient_mul_card_subgroup" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("direct bridge proof-body print is missing")
    if "sorry" in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("Lean output contains a proof placeholder")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0061; 5 candidates; exact pinned mathlib wrapper M0-W/E2; "
        "accepted root remains M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
