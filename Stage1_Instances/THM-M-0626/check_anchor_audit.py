#!/usr/bin/env python3
"""Validate the immutable, locally checkable THM-M-0626 anchor ledger."""

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
ITEM_ID = "S56-M-0626-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0626"
BASE_REVISION = "1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4"
BASE_TREE = "61214aa2a03c032134ddc4958b1df63df3430a85"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "5c32b45abf131975cd4673ca095ca1a8e0122e4104bf616a4afab09a03289231"
STATEMENT_SHA256 = "eb03b777ac803b993a4787a8b58bd3f8f132218bda961bec4b4d1445a88bcca6"
PROTOCOL_SHA256 = "efa0a992f3eef81af2e9b5df65d61aaa179f48ba4f71330744443a7650e4c4ef"
ANCHOR_SHA256 = "791df6f8ed5ce37e75b7a7f431de69e5a5e28587015f3726003e027da20ab76b"
LEAN_OUTPUT_SHA256 = "47b5e4d34dfcacc44c1fd60a331c76469e19fdbd2eae76eb9295c02099e99932"
MATHLIB_SOURCE = "Mathlib/Topology/Connected/Basic.lean"
MATHLIB_SOURCE_SHA256 = "929f0e1c789b8c0ed10c3164aa174e369b9b250317c525a8ad2f2dcca2a65e9c"
REGION_SHA256 = "346812463a258d99049e9ebb1c0f405bb97de0ebf9f432c92699d78bbfc06c9c"
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


def strip_lean_comments(source: str) -> str:
    """Remove nested Lean comments before the supplemental token scan."""
    result: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            result.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                result.append("\n")
            index += 1
        else:
            result.append(source[index])
            index += 1
    if depth:
        raise SystemExit("unterminated Lean block comment")
    return "".join(result)


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
    assert audit["execution_rank"] == 1320
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1320
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    prerequisite = next(
        row for row in execution["items"] if row["id"] == "S56-M-0626-STATEMENT"
    )
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] in {"[ ]", "[_]"}
    assert prerequisite["state"] in {"[_]", "[x]"}
    assert item["depends_on"] == ["S56-M-0626-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Audit mathlib and external Lean 4 candidates at immutable revisions."

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == audit["canonical_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256

    assert protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0"
    assert protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID
    assert protocol["inventory_version"] == audit["discovery_protocol"]["inventory_version"]
    assert protocol["saturation_claim"] is False
    assert set(protocol["inventory_members"]) == {
        "M0626-C01-MATHLIB-DIRECT",
        "M0626-C02-MATHLIB-SUBSTRATE",
        "M0626-C03-MATHLIB-NONSUBSTITUTES",
        "M0626-C04-FORMAL-CONJECTURES-DUPLICATE",
        "M0626-C05-MANIFEST-EXTERNAL-CLOSURE",
        "M0626-C06-PUBLIC-INDEX-RESULTS",
    }
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
    lake_manifest = load(LEAN_ROOT / "lake-manifest.json")
    manifest_revisions = {
        package["name"].strip("«»"): package["rev"]
        for package in lake_manifest["packages"]
    }
    for package_dir in (LEAN_ROOT / ".lake" / "packages").iterdir():
        if not (package_dir / ".git").exists():
            continue
        assert output("git", "rev-parse", "HEAD", cwd=package_dir) == manifest_revisions[package_dir.name]
        assert output("git", "status", "--short", cwd=package_dir) == ""

    candidates = audit["candidates"]
    assert len(candidates) == 6
    assert {candidate["candidate_id"] for candidate in candidates} == set(
        protocol["inventory_members"]
    )
    direct = next(c for c in candidates if c["candidate_id"] == "M0626-C01-MATHLIB-DIRECT")
    source = MATHLIB / direct["file"]
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["file"] == MATHLIB_SOURCE
    assert direct["file_blob"] == output("git", "rev-parse", f"HEAD:{MATHLIB_SOURCE}", cwd=MATHLIB)
    assert direct["file_sha256"] == sha256(source) == MATHLIB_SOURCE_SHA256
    assert direct["source_region_sha256"] == sha256_lines(source, 274, 297) == REGION_SHA256
    assert direct["declaration"] == "IsConnected.image"
    assert direct["candidate_classification"] == "M0-W"
    assert direct["evidence_level"] == "E2_worker_candidate_check"
    for name, revision in direct["historical_provenance"].items():
        if name.endswith("commit"):
            assert output(
                "git", "merge-base", "--is-ancestor", revision, MATHLIB_REVISION, cwd=MATHLIB
            ) == ""

    source_text = source.read_text(encoding="utf-8")
    for marker in (
        "protected theorem IsPreconnected.image",
        "continuousOn_iff'.1 hf",
        "protected theorem IsConnected.image",
        "image_nonempty.mpr H.nonempty",
        "H.isPreconnected.image f hf",
    ):
        assert marker in source_text, marker
    support = next(c for c in candidates if c["candidate_id"] == "M0626-C02-MATHLIB-SUBSTRATE")
    mismatch = next(c for c in candidates if c["candidate_id"] == "M0626-C03-MATHLIB-NONSUBSTITUTES")
    external = next(c for c in candidates if c["candidate_id"] == "M0626-C04-FORMAL-CONJECTURES-DUPLICATE")
    bounded = next(c for c in candidates if c["candidate_id"] == "M0626-C05-MANIFEST-EXTERNAL-CLOSURE")
    public = next(c for c in candidates if c["candidate_id"] == "M0626-C06-PUBLIC-INDEX-RESULTS")
    assert support["candidate_classification"] == "M3_support_duplicate"
    assert mismatch["candidate_classification"] == "M5_statement_mismatch"
    assert external["revision"] == "fdbea4653453a764aa7f952d3b45c93007356cc9"
    assert external["file_sha256"] == "fec0599bb2aed605ddded16b55fc06e0490202c3de98a457740d7c5b5ae0be41"
    assert external["candidate_classification"] == "M3_external_duplicate_wrapper"
    assert bounded["searched_lean_file_count"] == 668
    assert public["sourcegraph"]["response_sha256"] == "adb734a45ac635d6b3a53008f2cc14673cc7e134a27ca3ee91e016e0b0e027b0"
    assert public["github_code_search"]["result"].startswith("HTTP 401")
    assert public["grep_app"]["result"].startswith("HTTP 429")

    adapter_path = HERE / "AnchorAudit.lean"
    adapter = adapter_path.read_text(encoding="utf-8")
    assert sha256(adapter_path) == ANCHOR_SHA256
    for marker in (
        "def ExactTarget : Prop",
        "theorem exactTarget_mathlib_candidate : ExactTarget.{u, v}",
        "exact hs.image f hf.continuousOn",
        "#print IsPreconnected.image",
        "#print IsConnected.image",
        "#print sorries exactTarget_mathlib_candidate",
    ):
        assert marker in adapter, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(strip_lean_comments(adapter))
    assert not forbidden.search(strip_lean_comments(source_text))

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("6/6 classified candidate groups")
    assert result["exact_candidate_located"] is True
    assert result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["independent_external_lean4_terminal_body_found"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M0-W"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert audit["root_vector_before"] == audit["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == [] and instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False

    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "anchor_audit" and receipt["assigned_layer"] == 2
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["classification"] == "M0-W"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["anchor_file_sha256"] == sha256(adapter_path)
    assert receipt["anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    assert receipt["checker_sha256"] == sha256(Path(__file__))
    assert receipt["mathlib_source_sha256"] == sha256(source)
    assert receipt["mathlib_source_region_sha256"] == sha256_lines(source, 274, 297)
    for path_string, tagged_hash in receipt["source_inputs"].items():
        algorithm, expected = tagged_hash.split(":", 1)
        assert algorithm == "sha256"
        assert sha256(ROOT / path_string) == expected, f"source hash mismatch: {path_string}"
    for path_string, tagged_hash in receipt["public_projection_hashes"].items():
        algorithm, expected = tagged_hash.split(":", 1)
        assert algorithm == "sha256"
        assert sha256(ROOT / path_string) == expected, f"projection hash mismatch: {path_string}"

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
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0626/AnchorAudit.lean"],
        cwd=LEAN_ROOT,
        env={**dict(__import__("os").environ), "LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"},
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
        raise SystemExit("unexpected candidate axiom report")
    if lean.stdout.count("Declarations are sorry-free!") != 3:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected candidate placeholder report")
    if "protected theorem IsConnected.image" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("terminal proof-body print is missing")
    if "def Stage1Instances.THM_M_0626_AnchorAudit.ExactTarget.{u, v} : Prop" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("exact audit target was not printed")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0626; 6 candidate groups; exact pinned mathlib M0-W candidate; "
        "accepted root remains M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
