#!/usr/bin/env python3
"""Validate the immutable, locally replayable THM-M-0070 anchor inventory."""

from __future__ import annotations

import argparse
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
ITEM_ID = "S56-M-0070-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0070"
BASE_REVISION = "d266c6f5ce5732e1fccd687e2f9ce9aa2a0ed1fe"
BASE_TREE = "e77c8d6d5b41cb13d9d8acab2753ac37c4ebd6b4"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "51024e84c9b068a6de27ff2d3ba0f1e479c02dfd36d8072f3d243d46f3324c93"
STATEMENT_SHA256 = "9e1c126d56f87c1d7dee24d17b13c9c9822ffba13142e836ecbe2a85055a7dcf"
DISCOVERY_SHA256 = "0d2c5a8a59ecf044b0be46178d6a3e15c1d7246e8ba30d408d90fbb49457ff7b"
LEAN_OUTPUT_SHA256 = "37c22861db677c70be42128a310c241c848c90eca445cec850ae8d5b03337818"
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    audit = load(HERE / "anchor-audit.json")
    discovery = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(args.worker_packet) if args.worker_packet else None

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1101
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    if packet is not None:
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1101
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0070-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "anchor-discovery-protocol.json") == DISCOVERY_SHA256
    assert audit["discovery_protocol"]["sha256"] == DISCOVERY_SHA256
    assert discovery["committed_before_final_classification"] is True
    assert discovery["saturation_claim"] is False

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION and env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]

    interface = next(c for c in audit["candidates"] if c["candidate_id"] == "M0070-C01-MATHLIB-SOLVABILITY-INTERFACES")
    interface_file = MATHLIB / interface["file"]
    assert interface["revision"] == MATHLIB_REVISION and interface["tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", f"HEAD:{interface['file']}", cwd=MATHLIB) == interface["file_blob"]
    assert sha256(interface_file) == interface["file_sha256"]
    source = interface_file.read_text(encoding="utf-8")
    for marker in (
        "class IsSolvable : Prop where",
        "instance (priority := 100) CommGroup.isSolvable",
        "theorem solvable_of_ker_le_range",
        "theorem solvable_of_solvable_injective",
        "theorem solvable_of_surjective",
    ):
        assert marker in source, marker

    special = next(c for c in audit["candidates"] if c["candidate_id"] == "M0070-C02-MATHLIB-NEAR-SPECIAL-CLASSES")
    for record in special["source_records"]:
        path = MATHLIB / record["file"]
        assert output("git", "rev-parse", f"HEAD:{record['file']}", cwd=MATHLIB) == record["file_blob"]
        assert sha256(path) == record["file_sha256"]

    title = next(c for c in audit["candidates"] if c["candidate_id"] == "M0070-C03-MATHLIB-1000-TITLE")
    title_source = (MATHLIB / title["file"]).read_text(encoding="utf-8")
    assert title["file_blob"] == output("git", "rev-parse", f"HEAD:{title['file']}", cwd=MATHLIB)
    assert sha256(MATHLIB / title["file"]) == title["file_sha256"]
    assert "Q909517:\n  title: Feit–Thompson theorem\n\nQ913447:" in title_source

    external = next(c for c in audit["candidates"] if c["candidate_id"] == "M0070-C05-ODD-ORDER-LEAN-PLACEHOLDER")
    assert external["revision"] == "0f4a5daeaf6f26efd5af808ecd05e4744d8a2924"
    assert external["tree"] == "95e6964049e33a58cadf80851453d64ba48e7441"
    assert external["file_blob"] == "12cabbffd165b2554dd13d6986323eef7ab4b019"
    assert external["candidate_classification"] == "M5_exact_statement_placeholder_and_incompatible_pins"
    assert external["terminal_proof_body"] == "by sorry"
    assert external["mathlib_revision"] == "360da6fa66c1273b76b6b2d8c5666fd5ac2e3b56"

    coq = next(c for c in audit["candidates"] if c["candidate_id"] == "M0070-C06-MATHCOMP-ODD-ORDER-COQ")
    assert coq["revision"] == "6afa795b9018c64ab5c7cd2f9b3c9ab5dd45d93f"
    assert coq["formal_system"].startswith("Coq/Rocq")
    assert coq["candidate_classification"] == "M3_other_prover_exact_source_anchor"
    assert coq["evidence_level"] == "E3"

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "Odd (Nat.card G) -> IsSolvable G",
        "theorem exactTarget_iff_derivedSeries",
        "theorem commutative_special_case",
        "exact CommGroup.isSolvable",
        "#print axioms exactTarget_iff_derivedSeries",
    ):
        assert marker in adapter, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(adapter))

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("6/6")
    assert result["exact_lean_candidate_located"] is False
    assert result["exact_lean_placeholder_located"] is True
    assert result["interface_probe_kernel_checked"] is True
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M3"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is False and result["theorem_complete"] is False

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0070/AnchorAudit.lean"],
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
    if normalized.count("propext, Classical.choice, Quot.sound") != 3:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected interface axiom reports")
    if "def Stage1Instances.THM_M_0070_AnchorAudit.ExactTarget" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("exact target print is missing")
    if "sorry" in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("Lean output contains a proof placeholder")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("interface Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0070; 6 candidate groups; no exact Lean proof; "
        "exact external Lean placeholder M5; exact Coq source E3; "
        "root H1/M3/R4; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
