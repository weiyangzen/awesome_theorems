#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, and claim checks for THM-M-0957 proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0957-PROOF"
THEOREM = "THM-M-0957"
BASE_REVISION = "8714972d4cf7ae256a92b9e35032c9df1bf5745c"
BASE_TREE = "080d14e14102a733c6992aa0644e3c65d755e91b"
EXPRESSION_SHA256 = "e611db43ce6f3419553e3ebe0fe85a3ce89e4d3930b3842f5a09be8a7683d2ed"
REGISTRY_DENOMINATOR = "84f7eaea7de3659e4324dc64f7849fde4024dd057d4d320c879b0b59dd692a63"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
BEHREND_SHA256 = "1f8c1813a75c722ee4d62d63185c53d0b52d27691e531c05e0ecb6c10c15cf65"
PROOF_IDS = [
    "M0957-ROOT",
    "M0957-T-ASSEMBLE",
    "M0957-T-CONSTRUCTION",
    "M0957-T-SHARP-PARAMETERS",
    "M0957-N-INCLUSIVE-INDEX",
    "M0957-T-PARAM-ADMISSIBLE",
    "M0957-L-AMBIENT-FIT",
    "M0957-T-SHARP-ESTIMATE",
    "M0957-N-SHARP-DIMENSION",
    "M0957-L-RADIX-NONZERO",
    "M0957-N-RPOW-EXP",
    "M0957-T-RATIO-ASYMPTOTIC",
    "M0957-T-PROXY-ASYMPTOTIC",
    "M0957-L-RADIX-FLOOR",
    "M0957-L-OPTIMAL-EXPONENT",
    "M0957-L-PROXY-LOG",
    "M0957-L-RECIPROCAL-LOSS",
    "M0957-L-LINEAR-LOSS",
    "M0957-L-SUBLEADING-LOSS",
    "M0957-L-PROXY-RPOW-IDENTITY",
    "M0957-L-PROXY-SLACK",
    "M0957-L-RECIPROCAL-CORE",
    "M0957-L-LINEAR-CEILING",
    "M0957-L-LINEAR-INCREMENT",
    "M0957-L-DIMENSION-SLACK",
    "M0957-L-LOG-DIMENSION",
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
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def proof_reachable(graphs: dict) -> list[str]:
    children: dict[str, list[str]] = {}
    for edge in graphs["graphs"]["proof"]["edges"]:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    result: list[str] = []
    queue = ["M0957-ROOT"]
    while queue:
        node = queue.pop(0)
        if node in result:
            continue
        result.append(node)
        queue.extend(children.get(node, []))
    return result


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    receipt = load(HERE / "proof-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1491
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0957-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    without_comments = re.sub(r"/-.*?-/", "", proof, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    assert prohibited.search(without_comments) is None
    markers = (
        "import ObligationTree",
        "import Statement",
        "theorem dimensionControl_proof : DimensionControlPackage",
        "theorem proxySlackAbsorption_proof : ProxySlackAbsorptionPackage",
        "theorem linearIncrementAbsorption_proof : LinearIncrementAbsorptionPackage",
        "theorem dimensionSlack_proof : DimensionSlackPackage",
        "theorem logDimensionLoss_proof : LogDimensionLossPackage",
        "theorem quantitativeConstruction_installed : QuantitativeConstructionPackage",
        "theorem exactAssembly_proof : ExactAssembly",
        "theorem exactRoot_proof : Root",
        "theorem behrendConstructionTarget_proof :",
        "Stage1Instances.THM_M_0957.BehrendConstructionTarget :=",
        "#print sorries behrendConstructionTarget_proof",
        "#print axioms behrendConstructionTarget_proof",
    )
    for marker in markers:
        assert marker in proof, marker

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR
    assert graphs["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
    records = {row["obligation_id"]: row for row in registry["obligations"]}
    assert proof_reachable(graphs) == PROOF_IDS
    assert set(PROOF_IDS) <= records.keys()

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    assert sha256(mathlib / "Mathlib/Combinatorics/Additive/AP/Three/Behrend.lean") == BEHREND_SHA256

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["closed_obligation_ids"] == PROOF_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["recipe"]["covered_ids"] == PROOF_IDS
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), filename
    fingerprints = receipt["obligation_statement_fingerprints"]
    for obligation_id in PROOF_IDS:
        assert fingerprints[obligation_id] == records[obligation_id]["statement_fingerprint"]

    assert not (HERE / "proof-blocker.json").exists()
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "exact root" in validation and "kernel-closed" in validation
    assert "does not claim theorem completion" in validation
    assert "M0-L" in validation
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0957 proof phase: exact root closes the frozen machine route")
    print("root kernel closure: true; accepted root closure: false; theorem_complete=false")


if __name__ == "__main__":
    main()
