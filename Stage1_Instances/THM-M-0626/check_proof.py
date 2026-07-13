#!/usr/bin/env python3
"""Fail-closed source, graph, pin, receipt, and packet checks for THM-M-0626 proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0626-PROOF"
THEOREM = "THM-M-0626"
BASE_REVISION = "72e9e8092182121a6794921f61fcc9cae22f726d"
BASE_TREE = "0d6c1fdf06d1573c256af331c6b198e5a787af43"
EXPRESSION_SHA256 = "5c32b45abf131975cd4673ca095ca1a8e0122e4104bf616a4afab09a03289231"
DENOMINATOR_SHA256 = "9c6e54699269263a82e13f7b771daf802103b4a4e0114d1c6a76a98918487270"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_SOURCE = Path("Mathlib/Topology/Connected/Basic.lean")
MATHLIB_SOURCE_BLOB = "d3fdb9332b203fe7bb9e932a5136c7c6c9824f82"
MATHLIB_SOURCE_SHA256 = "929f0e1c789b8c0ed10c3164aa174e369b9b250317c525a8ad2f2dcca2a65e9c"
MATHLIB_BODY_SHA256 = "52cd1c84042b3e3cce16ea0209bf323e7d976bcf1b4f4b2cba629345711b4d9e"
PROVISIONAL_IDS = [
    "M0626-ROOT",
    "M0626-S-GLOBAL-LOCAL",
    "M0626-N-IMAGE-COVER-TO-SOURCE",
    "M0626-N-SEPARATION-GOAL",
    "M0626-C-RELATIVE-PREIMAGES",
    "M0626-N-WITNESS-PULLBACK",
    "M0626-L-SOURCE-INTERSECTION",
    "M0626-T-INTERSECTION-PUSHFORWARD",
    "M0626-L-IMAGE-PRECONNECTED",
    "M0626-L-IMAGE-NONEMPTY",
    "M0626-A-ISCONNECTED-IMAGE",
    "M0626-T-LOCAL-COMPOSE",
    "M0626-T-ASSEMBLE",
]
OPEN_MACHINE_IDS = [
    "M0626-S-INTERFACE",
    "M0626-S-CONNECTEDNESS",
    "M0626-S-BOUNDARY",
    "M0626-S-FOUNDATION",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1320,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-0626-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import ObligationTree",
        "theorem relativePreimages : RelativePreimagePackage.{u, v}",
        "theorem imageCoverPullback : ImageCoverPullbackPackage.{u, v}",
        "theorem imageHitPullback : ImageHitPullbackPackage.{u, v}",
        "theorem sourceIntersection : SourceIntersectionPackage.{u}",
        "theorem intersectionPushforward : IntersectionPushforwardPackage.{u, v}",
        "separationEngine_of_components relativePreimages imageCoverPullback imageHitPullback",
        "imagePreconnected_of_separationEngine separationEngine",
        "localConnectedImage_of_components imageNonempty imagePreconnected",
        "theorem localConnectedImage_mathlib : LocalConnectedImagePackage.{u, v}",
        "exact hs.image f hf",
        "root_of_localConnectedImage globalToLocalContinuity localConnectedImage_mathlib",
        "root_of_localConnectedImage globalToLocalContinuity localConnectedImage_components",
        "exactAssembly_of_packages globalToLocalContinuity localConnectedImage_mathlib",
        "#print sorries connectedImage_via_components",
        "#print axioms connectedImage_via_exactAssembly",
    ):
        assert marker in proof, marker

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0626.ConnectedImageTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0626-ROOT"
    assert set(PROVISIONAL_IDS + OPEN_MACHINE_IDS) == set(
        registry["frozen_denominators"]["required_machine"]
    )

    proof_pairs = {
        (edge["from"], edge["to"])
        for edge in graphs["graphs"]["proof"]["edges"]
        if edge["type"] == "proof_requires"
    }
    assert {
        ("M0626-ROOT", "M0626-T-ASSEMBLE"),
        ("M0626-T-ASSEMBLE", "M0626-S-GLOBAL-LOCAL"),
        ("M0626-T-ASSEMBLE", "M0626-A-ISCONNECTED-IMAGE"),
    } <= proof_pairs

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["provisionally_closed_proof_obligation_ids"] == PROVISIONAL_IDS
    assert receipt["required_machine_open_ids"] == OPEN_MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename)
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False

    obligation_by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    for evidence in receipt["provisional_obligation_evidence"]:
        assert evidence["obligation_id"] in PROVISIONAL_IDS
        assert evidence["statement_fingerprint"] == obligation_by_id[
            evidence["obligation_id"]
        ]["statement_fingerprint"]
        assert evidence["declarations"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    source = mathlib / MATHLIB_SOURCE
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""
    assert git_output("rev-parse", f"HEAD:{MATHLIB_SOURCE}", cwd=mathlib) == MATHLIB_SOURCE_BLOB
    assert sha256(source) == MATHLIB_SOURCE_SHA256
    lines = source.read_bytes().splitlines(keepends=True)
    assert hashlib.sha256(b"".join(lines[272:297])).hexdigest() == MATHLIB_BODY_SHA256
    terminal = without_comments(b"".join(lines[272:297]).decode("utf-8"))
    assert prohibited.search(terminal) is None
    for marker in (
        "protected theorem IsPreconnected.image",
        "continuousOn_iff'.1 hf",
        "protected theorem IsConnected.image",
        "image_nonempty.mpr H.nonempty",
        "H.isPreconnected.image f hf",
    ):
        assert marker in terminal, marker

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git_output("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim theorem completion" in validation
    assert "M0-W" in validation and "M0626-S-FOUNDATION" in validation
    for path in (
        proof_path,
        HERE / "check_proof.py",
        HERE / "check_proof.sh",
        HERE / "proof-receipt.json",
        HERE / "proof-validation.md",
        ROOT / ".stage1-worker-selftest.json",
    ):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print(
        "PASS THM-M-0626 proof phase: exact pinned root and full component reconstruction checked"
    )
    print("accepted state unchanged; proof proposal is provisional pending master acceptance")


if __name__ == "__main__":
    main()
