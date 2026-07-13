#!/usr/bin/env python3
"""Validate the immutable, locally checkable THM-M-0079 anchor ledger."""

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
ITEM_ID = "S56-M-0079-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0079"
BASE_REVISION = "250f9e73cbbb3ebd2da9d0cefff78f0ab8c0d056"
BASE_TREE = "b6e8138c58e31e82f8209cb70fbc0fb253f3654a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "bb109f77dcbd6884a4ac90b32230cc213c08f19df6bc797ad04afac1a10da553"
STATEMENT_SHA256 = "fdacf7f7c9a39400ce02e8d82e3ed2a3a66e33dcd57b553d9e01a1dd991878c5"
PROTOCOL_SHA256 = "195bb96e9077294ab58e87b0a37ad1cf819493a7b8c14f4ab7616e51fa99ddad"
ANCHOR_SHA256 = "ba8b20d91e110e1b4143f37907212498e8b94971e7f927c926fc3d6b2687d5ef"
LEAN_OUTPUT_SHA256 = "36905ff311d76a340662576b73c1970ba214e64360b6606235617071d2b7aa48"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/README.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
    f"Stage1_Instances/{THEOREM_ID}/instance.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_lines(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


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
    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1105
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1105
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    prerequisite = next(
        row for row in execution["items"] if row["id"] == "S56-M-0079-STATEMENT"
    )
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] in {"[ ]", "[_]"}
    assert prerequisite["state"] in {"[_]", "[x]"}
    assert item["depends_on"] == ["S56-M-0079-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256

    assert protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0"
    assert protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID
    assert protocol["inventory_version"] == audit["discovery_protocol"]["inventory_version"]
    assert protocol["saturation_claim"] is False
    assert sha256(HERE / "anchor-discovery-protocol.json") == PROTOCOL_SHA256
    assert audit["discovery_protocol"]["sha256"] == PROTOCOL_SHA256
    assert instance["discovery_protocol_hash"] == f"sha256:{PROTOCOL_SHA256}"

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]
    assert sha256(LEAN_ROOT / "lean-toolchain") == env["toolchain_file_sha256"]

    candidates = audit["candidates"]
    assert len(candidates) == 6
    assert {candidate["candidate_id"] for candidate in candidates} == {
        "M0079-C01-MATHLIB-DIRECT",
        "M0079-C02-MATHLIB-PROOF-SUBSTRATE",
        "M0079-C03-DWARN-LEAN3-HISTORICAL",
        "M0079-C04-DWARN-LEAN3-SECOND-HISTORICAL",
        "M0079-C05-MANIFEST-EXTERNAL-CLOSURE",
        "M0079-C06-PUBLIC-INDEX-RESULTS",
    }
    direct = next(c for c in candidates if c["candidate_id"] == "M0079-C01-MATHLIB-DIRECT")
    source = MATHLIB / direct["file"]
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["file_blob"] == output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB)
    assert direct["file_sha256"] == sha256(source)
    assert direct["source_region_sha256"] == sha256_lines(source, 313, 316)
    assert direct["declaration"] == "subgroupIsFreeOfIsFree"
    assert direct["candidate_classification"] == "M0-W"
    for name, revision in direct["historical_provenance"].items():
        if name.endswith("commit"):
            assert output(
                "git", "merge-base", "--is-ancestor", revision, MATHLIB_REVISION, cwd=MATHLIB
            ) == ""

    source_text = source.read_text(encoding="utf-8")
    for marker in (
        "instance actionGroupoidIsFree",
        "lemma endIsFree : IsFreeGroup (End (root' T))",
        "instance endIsFreeOfConnectedFree",
        "instance subgroupIsFreeOfIsFree",
        "IsFreeGroup.ofMulEquiv (endMulEquivSubgroup H)",
    ):
        assert marker in source_text, marker
    support = next(c for c in candidates if c["candidate_id"] == "M0079-C02-MATHLIB-PROOF-SUBSTRATE")
    assert support["candidate_classification"] == "M3_support_duplicate"
    historical = next(c for c in candidates if c["candidate_id"] == "M0079-C03-DWARN-LEAN3-HISTORICAL")
    historical2 = next(c for c in candidates if c["candidate_id"] == "M0079-C04-DWARN-LEAN3-SECOND-HISTORICAL")
    assert historical["revision"] == "99fb30c0bf321c651edbb7524101604cf0242ea1"
    assert historical["toolchain"] == "leanprover-community/lean:3.7.1"
    assert historical["candidate_classification"].startswith("M5_")
    assert historical2["revision"] == "e51a8c6511d374dc584698c7fa236a5be47e7dbe"
    assert historical2["toolchain"] == "Lean 3.27.0"
    assert historical2["candidate_classification"].startswith("M5_")

    adapter_path = HERE / "AnchorAudit.lean"
    adapter = adapter_path.read_text(encoding="utf-8")
    assert sha256(adapter_path) == ANCHOR_SHA256
    for marker in (
        "def ExactTarget : Prop",
        "forall (G : Type u) [Group G] [IsFreeGroup G]",
        "theorem exactTarget_mathlib_candidate : ExactTarget.{u}",
        "exact subgroupIsFreeOfIsFree H",
        "#print subgroupIsFreeOfIsFree",
        "#print axioms IsFreeGroupoid.SpanningTree.endIsFree",
        "#print sorries exactTarget_mathlib_candidate",
    ):
        assert marker in adapter, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(adapter))
    assert not forbidden.search(without_comments(source_text))

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("6/6 classified candidate groups")
    assert result["exact_candidate_located"] is True
    assert result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M0-W"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == [] and instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False

    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["classification"] == "M0-W"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    actual_changed = {
        line[3:]
        for line in subprocess.check_output(
            ["git", "status", "--short", "--untracked-files=all"],
            cwd=ROOT,
            text=True,
        ).splitlines()
    }
    assert actual_changed - {"Formalizations/Lean/.lake"} == CHANGED_PATHS
    assert set(instance["owned_artifacts"]) == {
        path.name for path in HERE.iterdir() if path.is_file()
    }

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0079/AnchorAudit.lean"],
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
    if normalized.count("propext, Classical.choice, Quot.sound") != 5:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected candidate axiom report")
    if lean.stdout.count("Declarations are sorry-free!") != 5:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected candidate placeholder report")
    if "theorem subgroupIsFreeOfIsFree" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("terminal proof-body print is missing")
    if "def Stage1Instances.THM_M_0079_AnchorAudit.ExactTarget.{u} : Prop" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("exact audit target was not printed")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0079; 6 candidate groups; exact pinned mathlib M0-W candidate; "
        "accepted root remains M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
