#!/usr/bin/env python3
"""Fail-closed checks for the THM-M-0338 partial proof packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0338-PROOF"
THEOREM = "THM-M-0338"
BASE_REVISION = "b8c0a0c119a82ef435e23f9ff85bfd783db95736"
BASE_TREE = "831576eb7d1273d01e99653d36b616e99e85dc0f"
EXPRESSION_SHA256 = "c0c479c898a7b418bd4d82ad05d7514edfcc885cfd9a5487fb1a4ac5ffc37868"
DENOMINATOR_SHA256 = "e53a0b15267ae38e68bb1b727edd51b52d0b60c8f244fd912fc2153c2a0cca6e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROVISIONALLY_CLOSED_IDS = ["M0338-E-EXTENSION"]
CHECKED_DECLARATIONS = [
    "Stage1.THM_M_0338.extension_exists_for_state",
    "Stage1.THM_M_0338.extension_exists_for_kadison_singer_input",
]
REMAINING_MACHINE_CUT = [
    "M0338-KS-PAVING",
    "M0338-W-MSS",
    "M0338-X-SOURCE",
    "M0338-X-FOUNDATION",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation-v2.md",
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


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 831
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0338-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0338-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import ObligationTree",
        "riesz_extension",
        "neg_algebraMap_norm_le_self",
        "PositiveLinearMap.mk₀",
        "theorem extension_exists_for_state",
        "ExtensionExists diagonal phi",
        "assert_no_sorry extension_exists_for_state",
        "#print axioms extension_exists_for_state",
        "theorem extension_exists_for_kadison_singer_input",
        "assert_no_sorry extension_exists_for_kadison_singer_input",
        "#print axioms extension_exists_for_kadison_singer_input",
    ):
        assert marker in proof, marker
    assert "theorem KadisonSingerStatement" not in proof
    assert "theorem root" not in proof

    formal = instance["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1.THM_M_0338.KadisonSingerStatement"
    assert formal["elaborated_expression_hash"] == f"sha256:{EXPRESSION_SHA256}"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    computed = hashlib.sha256(
        json.dumps(registry["obligations"], sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert computed == DENOMINATOR_SHA256
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    extension = by_id["M0338-E-EXTENSION"]
    assert extension["statement_fingerprint"] == (
        "planned:v1:sha256:081a0055ad30375e20d4fe4ccc76b72f61bc34d6af94302f2205211783d681e9"
    )
    assert extension["terminal_proof_body_id"] is None
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["root_machine_classification"] == "M3"
    assert graphs["closure_boundary"]["theorem_complete"] is False
    assert instance["accepted_proof_state"] == []
    assert instance["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["exact_declarations"] == CHECKED_DECLARATIONS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["provisionally_closed_obligation_ids"] == PROVISIONALLY_CLOSED_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["provisional_remaining_machine_cut"] == REMAINING_MACHINE_CUT
    assert receipt["authoritative_graph_open_cut_unchanged"] == graphs["closure_boundary"]["open_cut_set"]
    assert receipt["recipe"]["covered_obligation_ids"] == PROVISIONALLY_CLOSED_IDS
    assert receipt["recipe"]["covered_declarations"] == CHECKED_DECLARATIONS
    binding = receipt["obligation_bindings"]
    assert binding == [
        {
            "obligation_id": "M0338-E-EXTENSION",
            "registry_statement_fingerprint": extension["statement_fingerprint"],
            "registry_formal_target": "Stage1.THM_M_0338.ExtensionExists",
            "implementation_declaration": (
                "Stage1.THM_M_0338.extension_exists_for_kadison_singer_input"
            ),
            "binding_basis": (
                "The contextual wrapper retains the frozen Hilbert basis, diagonal "
                "matrix-coefficient, state, and purity inputs verbatim and concludes the exact "
                "ExtensionExists interface. It delegates to the stronger unconditional theorem, "
                "which needs none of the extra inputs, without changing the required conclusion."
            ),
            "acceptance_state": "provisional_worker_selftest_pending_master_reconciliation",
        }
    ]
    assert receipt["proof_body"]["terminal_declaration"] == CHECKED_DECLARATIONS[0]
    assert receipt["proof_body"]["contextual_wrapper"] == CHECKED_DECLARATIONS[1]
    assert receipt["proof_body"]["terminal_body_count"] == 1
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_validation_sha256", "proof-validation-v2.md"),
        ("proof_blocker_sha256", "proof-blocker.json"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False

    assert blocker["item_id"] == ITEM and blocker["theorem_id"] == THEOREM
    assert blocker["base_revision"] == BASE_REVISION and blocker["base_tree"] == BASE_TREE
    assert blocker["partial_proof_receipt_id"] == receipt["receipt_id"]
    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["proof_body_added"] is True
    assert blocker["implemented_bodies"] == {
        CHECKED_DECLARATIONS[0]: (
            "Unconditional terminal ExtensionExists body. It restricts a state to the "
            "self-adjoint real subspace, applies M. Riesz extension using the order unit "
            "||y|| * 1, complexifies the positive real functional, and proves positivity, "
            "normalization, and exact restriction."
        ),
        CHECKED_DECLARATIONS[1]: (
            "Exact frozen-input wrapper retaining the basis, diagonal-characterization, and "
            "purity hypotheses. It delegates to extension_exists_for_state and receives no "
            "second terminal-body credit."
        ),
    }
    assert blocker["provisionally_closed_obligation_ids"] == PROVISIONALLY_CLOSED_IDS
    assert blocker["accepted_closed_obligation_ids"] == []
    assert blocker["remaining_machine_root_cut_set"] == REMAINING_MACHINE_CUT
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    validation = (HERE / "proof-validation-v2.md").read_text(encoding="utf-8")
    assert "M0338-E-EXTENSION" in validation
    assert "root remains open" in validation
    assert "theorem_complete=false" in validation
    assert sha256(proof_path) in validation
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), relative

    print("PASS THM-M-0338 partial proof: extension existence checked")
    print("provisional obligation closure: M0338-E-EXTENSION; master reconciliation pending")
    print("accepted closure: none; root remains open M3; theorem_complete=false")


if __name__ == "__main__":
    main()
