#!/usr/bin/env python3
"""Fail-closed source, pin, graph, and receipt checks for S56-M-1003-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1003-PROOF"
THEOREM = "THM-M-1003"
BASE_REVISION = "bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad"
BASE_TREE = "ca999baf360c6ce2440bbc2c01aeb8d519269a90"
EXPRESSION_SHA256 = "ead76891696316502f96466e97e0ec725b72cb1f2dfdc6d8afa4e405e79b8e9f"
DENOMINATOR_SHA256 = "d44a39b4a9b24a0cce89719cf41820d368483961dc0c2c624423e82136092b3c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROOF_IDS = [
    "M1003-ROOT",
    "M1003-N-L1-BOUND",
    "M1003-B-ENDPOINTS",
    "M1003-C-LIMIT",
    "M1003-L-AE-LIMIT",
    "M1003-L-LIMIT-MEMLP",
    "M1003-L-COND-REP",
    "M1003-L-COND-APPROX",
    "M1003-T-CANDIDATE",
    "M1003-T-SAME-EXPONENT",
    "M1003-T-ASSEMBLE",
]
ASSURANCE_IDS_DEFERRED_FROM_PROOF_RECEIPT = ["M1003-S-FOUNDATION"]
INFORMATIONAL_ASSURANCE_OPEN_IDS = ["M1003-X-PROVENANCE"]
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
    assert isinstance(value, dict), path
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
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 283
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-1003-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import ObligationTree",
        "theorem eLpNorm_condExp_le",
        "theorem memLpTendstoCondExp",
        "theorem uniformL1Bound",
        "theorem limitCandidate",
        "theorem candidatePackage",
        "theorem uniformL1UI",
        "theorem sameExponentNormCanonical",
        "D.martingale.ae_eq_condExp_limitProcess (uniformL1UI D)",
        "theorem sameExponentPackage",
        "theorem target : LpMartingaleConvergenceTarget.{u}",
        "root_of_limit_packages candidatePackage sameExponentPackage",
        "#print sorries target",
        "#print axioms target",
    ):
        assert marker in proof, marker

    required_machine = registry["frozen_denominators"]["required_machine"]
    assert required_machine == [
        "M1003-ROOT",
        "M1003-S-DEFINITIONS",
        "M1003-S-BOUNDARY",
        "M1003-S-FOUNDATION",
        "M1003-N-L1-BOUND",
        "M1003-B-ENDPOINTS",
        "M1003-C-LIMIT",
        "M1003-L-AE-LIMIT",
        "M1003-L-LIMIT-MEMLP",
        "M1003-L-COND-REP",
        "M1003-L-COND-APPROX",
        "M1003-T-CANDIDATE",
        "M1003-T-SAME-EXPONENT",
        "M1003-T-ASSEMBLE",
    ]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M1003-ROOT"
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1003.LpMartingaleConvergenceTarget"
    )
    proof_pairs = {
        (edge["from"], edge["to"])
        for edge in graphs["graphs"]["proof"]["edges"]
        if edge["type"] == "proof_requires"
    }
    assert proof_pairs == {
        ("M1003-ROOT", "M1003-T-ASSEMBLE"),
        ("M1003-T-ASSEMBLE", "M1003-T-CANDIDATE"),
        ("M1003-T-ASSEMBLE", "M1003-T-SAME-EXPONENT"),
        ("M1003-T-CANDIDATE", "M1003-C-LIMIT"),
        ("M1003-T-CANDIDATE", "M1003-L-AE-LIMIT"),
        ("M1003-T-CANDIDATE", "M1003-L-LIMIT-MEMLP"),
        ("M1003-L-AE-LIMIT", "M1003-N-L1-BOUND"),
        ("M1003-T-SAME-EXPONENT", "M1003-L-COND-REP"),
        ("M1003-T-SAME-EXPONENT", "M1003-L-COND-APPROX"),
        ("M1003-L-COND-REP", "M1003-T-CANDIDATE"),
        ("M1003-L-COND-APPROX", "M1003-L-COND-REP"),
        ("M1003-L-COND-APPROX", "M1003-L-LIMIT-MEMLP"),
        ("M1003-L-COND-APPROX", "M1003-B-ENDPOINTS"),
    }

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["provisionally_closed_proof_obligation_ids"] == PROOF_IDS
    assert receipt["assurance_ids_deferred_from_proof_receipt"] == (
        ASSURANCE_IDS_DEFERRED_FROM_PROOF_RECEIPT
    )
    assert receipt["informational_assurance_open_ids"] == INFORMATIONAL_ASSURANCE_OPEN_IDS
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
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename)
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["proof_graph_composition"]["all_required_proof_edges_consumed"] is True
    evidence = {
        row["obligation_id"]: row for row in receipt["provisional_obligation_evidence"]
    }
    assert list(evidence) == PROOF_IDS
    assert all(row["declarations"] for row in evidence.values())

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git_output("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim\ntheorem completion" in validation
    assert "M0-L" in validation and "foundation/TCB" in validation
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

    print("PASS THM-M-1003 proof phase: exact frozen root closes through all proof-graph children")


if __name__ == "__main__":
    main()
