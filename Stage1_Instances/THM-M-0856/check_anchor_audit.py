#!/usr/bin/env python3
"""Validate the immutable, target-owned THM-M-0856 anchor audit."""

from __future__ import annotations

import argparse
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
ITEM_ID = "S56-M-0856-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0856"
RANK = 1410
BASE_REVISION = "72e9e8092182121a6794921f61fcc9cae22f726d"
BASE_TREE = "0d6c1fdf06d1573c256af331c6b198e5a787af43"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_FILE = "Mathlib/Combinatorics/SimpleGraph/Tutte.lean"
MATHLIB_FILE_BLOB = "4b7931e61e4dd6a3aae37fcecf698ddc238fbc4e"
MATHLIB_FILE_SHA256 = "47072b914aa564222ef8013092c38fa62227fea8230e308cc3eb5f11afcdffc3"
ORIGIN_REVISION = "358193a686dedec6d9d4d69374d1bdd6ecad9b25"
EXPRESSION_SHA256 = "5364250d1d4e132aaf1d5ce8ad5425369546963189991202f49b2fcf65095bae"
STATEMENT_SHA256 = "cd7ec3e97a02ccc24578de4431a1a8ebf0e9572f9616b271b67f145d72fbedce"
ANCHOR_SHA256 = "9a3ab433c46f869933eb1a493b83a6faff86d7391dfeac48ca8d7d380c0a127b"
PROTOCOL_SHA256 = "cd31403c675b2428eaddd14594b94943931899419dd4b259df5b796953c72d94"
LEAN_OUTPUT_SHA256 = "d1fd4f1e7b868f300491e4aa438688aa1b8b48cb4e1b749873d2207dd99e5f13"
ATLAS_SHA256 = "646cf222f850c459be5e6670223444516e1e8a325463282a436949c64a907efe"
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


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert b"\x00" not in data and (not data or data.endswith(b"\n")), path
    for number, line in enumerate(data.splitlines(), 1):
        assert line == line.rstrip(b" \t"), f"{path}:{number}: trailing whitespace"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["normative_profile"] == "machine-theorem-assurance/1.0"
    assert audit["item_id"] == receipt["item_id"] == protocol["item_id"] == ITEM_ID
    assert audit["theorem_id"] == receipt["theorem_id"] == protocol["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == RANK
    assert audit["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == RANK
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    statement_item = next(row for row in execution["items"] if row["id"] == "S56-M-0856-STATEMENT")
    assert statement_item["state"] == "[_]"
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert (item["phase"], item["layer"], item["state"]) == ("anchor_audit", 2, "[ ]")
    assert item["depends_on"] == ["S56-M-0856-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert protocol["saturation_claim"] is False
    assert protocol["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert sha256(HERE / "anchor-discovery-protocol.json") == PROTOCOL_SHA256
    assert audit["discovery_protocol_sha256"] == PROTOCOL_SHA256
    assert "public discovery preceded" in audit["protocol_timing_boundary"]
    public_searches = [row for row in audit["search_results"] if row["surface"] not in {
        "repo-local Lean source", "pinned mathlib source and installed packages"
    }]
    assert all("observed_at" in row or "observed_at_values" in row for row in public_searches)

    canonical = audit["canonical_target"]
    assert canonical["declaration"] == "Stage1Instances.THM_M_0856.TutteOneFactorTarget"
    assert canonical["expression_sha256"] == EXPRESSION_SHA256
    assert canonical["statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == canonical["declaration"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION and env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert output("git", "describe", "--tags", "--exact-match", "HEAD", cwd=MATHLIB) == "v4.29.0"
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["lake_manifest_sha256"]
    assert sha256(LEAN_ROOT / "lean-toolchain") == env["lean_toolchain_file_sha256"]
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]

    terminal = next(c for c in audit["candidates"] if c["candidate_id"] == "M0856-C02-PINNED-MATHLIB-TUTTE")
    assert terminal["revision"] == MATHLIB_REVISION and terminal["tree"] == MATHLIB_TREE
    assert terminal["file_blob"] == MATHLIB_FILE_BLOB
    assert output("git", "rev-parse", f"HEAD:{MATHLIB_FILE}", cwd=MATHLIB) == MATHLIB_FILE_BLOB
    terminal_path = MATHLIB / MATHLIB_FILE
    assert sha256(terminal_path) == terminal["file_sha256"] == MATHLIB_FILE_SHA256
    assert output("git", "merge-base", "--is-ancestor", ORIGIN_REVISION, MATHLIB_REVISION, cwd=MATHLIB) == ""
    assert terminal["declaration"] == "SimpleGraph.tutte"
    assert terminal["local_adapter"].endswith("exactTarget_mathlib_candidate")
    assert terminal["candidate_classification"] == "M3"
    assert terminal["eligible_route_shape_after_E1"] == "M0-W"
    assert terminal["evidence_level"] == "node_local_below_E1"
    assert terminal["machine_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert terminal["kernel_checked"] is True and terminal["accepted"] is False

    source = terminal_path.read_text(encoding="utf-8")
    for marker in (
        "def IsTutteViolator",
        "lemma not_isTutteViolator_of_isPerfectMatching",
        "theorem IsTutteViolator.empty",
        "lemma exists_isTutteViolator",
        "theorem tutte :",
        "exact exists_isTutteViolator h (Nat.not_odd_iff_even.mp hvOdd)",
    ):
        assert marker in source, marker
    anchor = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    assert sha256(HERE / "AnchorAudit.lean") == ANCHOR_SHA256
    for marker in (
        "def ExactTarget.{v} : Prop",
        "theorem exactTarget_mathlib_candidate : ExactTarget",
        "SimpleGraph.tutte (G := G)",
        "#print SimpleGraph.tutte",
        "#print sorries SimpleGraph.tutte",
        "#print axioms exactTarget_mathlib_candidate",
    ):
        assert marker in anchor, marker
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe|extern|implemented_by|native_decide)\b"
    )
    assert not forbidden.search(without_comments(anchor))
    assert not forbidden.search(without_comments(source))

    candidate_ids = {candidate["candidate_id"] for candidate in audit["candidates"]}
    assert candidate_ids == {
        "M0856-C01-LOCAL-STATEMENT",
        "M0856-C02-PINNED-MATHLIB-TUTTE",
        "M0856-C03-PINNED-MATHLIB-DIRECTIONS",
        "M0856-C04-ATLAS-DUPLICATE-WRAPPER",
        "M0856-C05-FORMAL-CONJECTURES-SUPPORT",
        "M0856-C06-CROSS-TARGET-PROBE",
    }
    assert all(candidate["candidate_classification"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"} for candidate in audit["candidates"])
    atlas = next(c for c in audit["candidates"] if c["candidate_id"] == "M0856-C04-ATLAS-DUPLICATE-WRAPPER")
    assert atlas["revision"] == "34ffed396f376454c1a9b297f3fd74c5c801fb50"
    assert atlas["tree"] == "c12fe2315fe475d70a4fcee81d6b731f853373ab"
    assert atlas["file_blob"] == "0e32e4b4c7b7ef3c721b1ffbd9b2661aad947b42"
    assert atlas["tree_truncated"] is False and atlas["tree_entries"] == 2860
    assert atlas["file_sha256"] == ATLAS_SHA256
    assert atlas["candidate_classification"] == "M3"
    assert atlas["integration_decision"].startswith("Do not integrate")
    assert "No independent Tutte terminal proof body" in atlas["body_provenance"]
    assert "SimpleGraph.tutte terminal" in atlas["body_provenance"]

    metrics = audit["inventory_metrics"]
    assert metrics["candidate_ids"] == metrics["classified_candidate_ids"]
    formal_conjectures = next(
        c for c in audit["candidates"]
        if c["candidate_id"] == "M0856-C05-FORMAL-CONJECTURES-SUPPORT"
    )
    assert formal_conjectures["tree"] == "40d17fde4b874af651386e646081f453377ea020"
    assert formal_conjectures["tree_truncated"] is False
    assert formal_conjectures["file_blob"] == "8c5c1c73bdb79d8055ad2e36a560b1b8e746fd78"
    assert formal_conjectures["file_sha256"] == (
        "c7d3ecd6e13b82ea8daa6c1fc0156c5371e8e5e774dc496bb81d2c184a39ac24"
    )
    assert formal_conjectures["disposition"] == "support_only_not_root_candidate"
    assert metrics["inventory_classification"] == "6/6"
    assert len(metrics["distinct_exact_terminal_body_ids"]) == 1
    assert metrics["exhaustive_discovery_claim"] is False and metrics["root_closure"] is False
    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["exact_candidate_located"] is True and result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["candidate_route_classification"] == "M3"
    assert result["eligible_route_shape_after_E1"] == "M0-W"
    assert result["root_machine_debt_before"] == result["root_machine_candidate_after"] == "M3"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["root_candidate_vector_after"] == result["accepted_root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert audit["audit_complete"] is False and audit["theorem_complete"] is False
    assert audit["accepted_receipt_ids"] == []
    provenance = audit["provenance_packet"]
    assert provenance["terminal_declaration"] == "SimpleGraph.tutte"
    assert "unfolds TutteOneFactorTarget" in provenance["canonical_identity_check"]
    assert provenance["transitive_trust_closure_hash"] is None

    lean = run_lean(HERE / "AnchorAudit.lean")
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    normalized = re.sub(r"\s+", " ", lean.stdout)
    expected_axioms = "[propext, Classical.choice, Quot.sound]"
    if normalized.count(expected_axioms) != 4:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected terminal, branch, or adapter axiom report")
    if lean.stdout.count("Declarations are sorry-free!") != 2:
        sys.stdout.write(lean.stdout)
        raise SystemExit("terminal or adapter sorry report changed")
    if "theorem SimpleGraph.tutte" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("terminal proof body was not printed")
    if "sorryAx" in lean.stdout or "declaration uses 'sorry'" in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("Lean output reports a proof placeholder")
    assert hashlib.sha256(lean.stdout.encode()).hexdigest() == LEAN_OUTPUT_SHA256

    statement_source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    statement_without_import = statement_source.replace(
        "import Mathlib.Combinatorics.SimpleGraph.Matching\n", "", 1
    )
    anchor_without_import = anchor.replace("import Mathlib.Combinatorics.SimpleGraph.Tutte\n", "", 1)
    combined = (
        "import Mathlib.Combinatorics.SimpleGraph.Tutte\n\n"
        + statement_without_import
        + "\n"
        + anchor_without_import
        + """

namespace Stage1Instances.THM_M_0856.CombinedAnchorCheck

universe u

theorem canonicalTarget_iff_auditTarget :
    Stage1Instances.THM_M_0856.TutteOneFactorTarget.{u} <->
      Stage1Instances.THM_M_0856.AnchorAudit.ExactTarget.{u} := by
  simp only [Stage1Instances.THM_M_0856.TutteOneFactorTarget,
    Stage1Instances.THM_M_0856.OddComponentCondition,
    Stage1Instances.THM_M_0856.AnchorAudit.ExactTarget]

theorem canonicalTarget_of_auditCandidate :
    Stage1Instances.THM_M_0856.TutteOneFactorTarget :=
  Stage1Instances.THM_M_0856.AnchorAudit.exactTarget_mathlib_candidate

#print sorries canonicalTarget_of_auditCandidate
#print axioms canonicalTarget_iff_auditTarget
#print axioms canonicalTarget_of_auditCandidate

end Stage1Instances.THM_M_0856.CombinedAnchorCheck
"""
    )
    with tempfile.TemporaryDirectory(prefix="thm-m-0856-anchor-") as directory:
        path = Path(directory) / "CombinedAnchorCheck.lean"
        path.write_text(combined, encoding="utf-8")
        identity = run_lean(path)
    if identity.returncode:
        sys.stdout.write(identity.stdout)
        raise SystemExit(identity.returncode)
    identity_normalized = re.sub(r"\s+", " ", identity.stdout)
    if identity_normalized.count(expected_axioms) < 6:
        sys.stdout.write(identity.stdout)
        raise SystemExit("combined canonical identity/candidate axiom checks are missing")
    if "sorryAx" in identity.stdout or "declaration uses 'sorry'" in identity.stdout:
        sys.stdout.write(identity.stdout)
        raise SystemExit("combined canonical check reports a proof placeholder")

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["artifact_hashes"] == {
        "AnchorAudit.lean": f"sha256:{sha256(HERE / 'AnchorAudit.lean')}",
        "anchor-audit.json": f"sha256:{sha256(HERE / 'anchor-audit.json')}",
        "anchor-audit-validation.md": f"sha256:{sha256(HERE / 'anchor-audit-validation.md')}",
        "anchor-discovery-protocol.json": (
            f"sha256:{sha256(HERE / 'anchor-discovery-protocol.json')}"
        ),
        "check_anchor_audit.py": f"sha256:{sha256(Path(__file__))}",
    }
    assert receipt["immutable_inputs"]["discovery_protocol_sha256"] == PROTOCOL_SHA256
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

    if args.worker_packet:
        packet = load(args.worker_packet)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary", "base_revision",
            "known_failures", "state",
        }
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        check_text_file(ROOT / relative)

    print(
        "check_anchor_audit: ok "
        "(THM-M-0856; 6 candidates; exact pinned mathlib M0-W-shaped route kernel-checked; "
        "evidence below E1; accepted root M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
