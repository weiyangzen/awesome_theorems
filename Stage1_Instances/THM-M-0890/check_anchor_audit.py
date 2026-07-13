#!/usr/bin/env python3
"""Fail-closed checker for the THM-M-0890 rev-5.6 anchor audit."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0890-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0890"
BASE_REVISION = "a1c9974d7fb28cd680e6494b968544bf801a93a2"
BASE_TREE = "1fa287bc821355aca2ca9e3ce107830a3eb58e64"
TARGET_SHA256 = "512ebe658ca83b7fb4bb3d3565122d065e3bc6e589898b4f3cf74ab2e12ea54d"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{name} must contain a JSON object")
    return value


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_lean(name: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(HERE / name)],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=180,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    audit = load("anchor-audit.json")
    protocol = load("anchor-discovery-protocol.json")
    receipt = load("anchor-audit-receipt.json")

    assert audit["item_id"] == protocol["item_id"] == receipt["item_id"] == ITEM_ID
    assert audit["theorem_id"] == protocol["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert audit["base_revision"] == protocol["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == protocol["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert audit["canonical_target"]["expression_sha256"] == TARGET_SHA256
    assert protocol["canonical_expression_sha256"] == receipt["canonical_target_expression_sha256"] == TARGET_SHA256
    assert audit["inventory_version"] == protocol["inventory_version"] == receipt["inventory_version"]
    assert audit["discovery_protocol"]["frozen_before_candidate_classification"] is True
    assert audit["discovery_protocol"]["saturation_claim"] is False
    assert protocol["saturation_claim_planned"] is False

    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""

    manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
    mathlib = next(package for package in manifest["packages"] if package["name"] == "mathlib")
    assert mathlib["rev"] == audit["immutable_environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert audit["immutable_environment"]["mathlib_tree"] == MATHLIB_TREE

    statement = load("statement.json")
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == TARGET_SHA256
    assert sha256(HERE / "Statement.lean") == audit["canonical_target"]["statement_file_sha256"]

    candidates = {row["candidate_id"]: row for row in audit["candidates"]}
    assert set(candidates) == {
        "M0890-C01-LOCAL-STATEMENT",
        "M0890-C02-MATHLIB-SUBSTRATE",
        "M0890-C03-ATLAS-SPECTRAL-GRAPH-ADJACENCY",
        "M0890-C04-FORMAL-CONJECTURES-GRAPH-DEFINITIONS",
        "M0890-C05-PUBLIC-INDEX-INVENTORY",
    }
    assert candidates["M0890-C01-LOCAL-STATEMENT"]["candidate_classification"] == "M3_exact_statement_only"
    assert candidates["M0890-C02-MATHLIB-SUBSTRATE"]["candidate_classification"] == "M3_support_only"
    assert candidates["M0890-C03-ATLAS-SPECTRAL-GRAPH-ADJACENCY"]["candidate_classification"] == "M5_statement_mismatch_and_placeholders"
    assert candidates["M0890-C04-FORMAL-CONJECTURES-GRAPH-DEFINITIONS"]["candidate_classification"] == "M3_related_definitions_only"
    assert candidates["M0890-C05-PUBLIC-INDEX-INVENTORY"]["candidate_classification"] == "no_formal_candidate"

    for record in candidates["M0890-C02-MATHLIB-SUBSTRATE"]["source_records"]:
        path = MATHLIB / record["file"]
        assert sha256(path) == record["sha256"]
        assert output("git", "hash-object", record["file"], cwd=MATHLIB) == record["blob"]

    result = audit["audit_result"]
    expected_vector = {"H": "H1", "M": "M3", "R": "R4"}
    assert result["inventory_classified"] is True
    assert result["exact_external_source_candidate_found"] is False
    assert result["external_kernel_closure_candidate_found"] is False
    assert result["eligible_repo_local_integration_debt"] is False
    assert result["root_vector_before"] == result["root_vector_candidate_after"] == result["root_vector_accepted_after"] == expected_vector
    assert result["node_self_tested"] is True
    assert result["gate_state"] == "self_tested_pending_master_acceptance"
    assert audit["audit_complete"] is result["audit_complete"] is receipt["audit_complete"] is False
    assert audit["theorem_complete"] is result["theorem_complete"] is receipt["theorem_complete"] is False
    assert receipt["accepted"] is False and receipt["accepted_receipt_ids"] == []
    for relative, tagged in receipt["artifact_hashes"].items():
        if relative in {".stage1-worker-selftest.json", "Stage1_Instances/THM-M-0890/anchor-audit-receipt.json"}:
            continue
        assert tagged == f"sha256:{sha256(ROOT / relative)}"

    source = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b")
    without_comments = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    assert forbidden.search(without_comments) is None
    for declaration in receipt["checked_declarations"]:
        assert declaration in source

    lean = run_lean("AnchorAudit.lean")
    if lean.returncode:
        print(lean.stdout, end="")
        raise SystemExit(lean.returncode)
    assert hashlib.sha256(lean.stdout.encode()).hexdigest() == receipt["lean_output_sha256"]
    reports = re.findall(r"depends on axioms: \[(.*?)\]", lean.stdout)
    assert len(reports) == 8
    assert all({value.strip() for value in report.split(",")} == EXPECTED_AXIOMS for report in reports)
    assert "sorryAx" not in lean.stdout

    item = next(
        row for row in json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(encoding="utf-8"))["items"]
        if row["id"] == ITEM_ID
    )
    assert (item["theorem_id"], item["phase"], item["layer"]) == (THEOREM_ID, "anchor_audit", 2)
    assert item["depends_on"] == ["S56-M-0890-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    if args.worker_packet is not None:
        packet = json.loads(args.worker_packet.read_text(encoding="utf-8"))
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
        assert packet["known_failures"] == receipt["known_failures"] == audit["known_failures"]
        assert packet["commands"] == receipt["commands_and_results"]

    print(
        "anchor audit verified: 5/5 candidate groups classified; exact root M3; "
        "pinned support checked; no proof or theorem completion"
    )


if __name__ == "__main__":
    main()
