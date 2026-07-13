#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, blocker, and packet checks for THM-M-1143."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
from datetime import datetime


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1143-PROOF"
THEOREM = "THM-M-1143"
BASE_REVISION = "3bb4cb3ae15dff8b48c93242019edec3bf858e48"
BASE_TREE = "8e911f5a101bd92eb0951794fa0d9a3c0c3a2ddc"
EXPRESSION_SHA256 = "e05a7b951bf36aedbc370a3f6ad2950c86b63b4d3a8af1d0e031290b62701610"
DENOMINATOR_SHA256 = "af64903cdbdaa77c2ffcbbbf20f444870b91f6e032643c3994d35d2688c20eb7"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
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


def tracked_patch_sha256() -> str:
    patch = subprocess.check_output(
        [
            "git",
            "diff",
            "--binary",
            "--",
            f"Stage1_Instances/{THEOREM}/Proof.lean",
            f"Stage1_Instances/{THEOREM}/proof-validation.md",
        ],
        cwd=ROOT,
    )
    return hashlib.sha256(patch).hexdigest()


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 348
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-1143-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1143-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_dag["accepted_states"] == []

    source_without_assertions = proof.replace("assert_no_sorry", "")
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    assert prohibited.search(source_without_assertions) is None
    for fragment in (
        "import ObligationTree",
        "theorem exists_uniform_abs_bound",
        "theorem exists_nonnegative_uniform_abs_bound",
        "def InteriorGradientEstimatePackage",
        "theorem continuousLinearMap_eq_zero_of_norm_le_div",
        "theorem vanishingDerivativePackage_of_interiorGradientEstimate",
        "theorem zeroDerivativeConstantPackage : ZeroDerivativeConstantPackage",
        "theorem root_of_interiorGradientEstimate",
        "assert_no_sorry root_of_interiorGradientEstimate",
        "#print axioms root_of_interiorGradientEstimate",
    ):
        assert fragment in proof, fragment

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    assert statement["printed_expression_sha256"] == EXPRESSION_SHA256
    assert statement["declaration"] == (
        "Stage1Instances.THM_M_1143.BoundedHarmonicIsConstant"
    )
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M1143-ROOT"
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["remaining_root_cut_set"] == [
        "M1143-T-VANISH",
        "M1143-L-CONSTANT",
    ]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    receipt_bound_files = {
        "Proof.lean",
        "Statement.lean",
        "ObligationTree.lean",
        "obligation-registry.json",
        "typed-graphs.json",
        "anchor-audit.json",
        "validation-specs.json",
        "check_proof.py",
        "check_proof.sh",
        "proof-blocker.json",
        "proof-validation.md",
    }
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_blocker_sha256", "proof-blocker.json"),
        ("proof_validation_sha256", "proof-validation.md"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename)
    assert receipt["nonrelease_worktree"]["tracked_patch_sha256"] == tracked_patch_sha256()
    symlink = ROOT / "Formalizations/Lean/.lake"
    assert symlink.is_symlink()
    assert receipt["nonrelease_worktree"]["pre_existing_untracked_path"] == (
        "Formalizations/Lean/.lake"
    )
    assert receipt["nonrelease_worktree"]["pre_existing_symlink_target"] == str(
        symlink.readlink()
    )
    assert receipt["nonrelease_worktree"]["untracked_input_sha256"] == {
        f"Stage1_Instances/{THEOREM}/check_proof.py": sha256(HERE / "check_proof.py"),
        f"Stage1_Instances/{THEOREM}/check_proof.sh": sha256(HERE / "check_proof.sh"),
        f"Stage1_Instances/{THEOREM}/proof-blocker.json": sha256(HERE / "proof-blocker.json"),
    }
    assert receipt["recipe"]["argv"] == [
        "bash",
        f"Stage1_Instances/{THEOREM}/check_proof.sh",
    ]
    assert receipt["recipe"]["timeout_seconds"] == 600
    assert receipt["recipe"]["lean_step_timeout_seconds"] == 180
    assert receipt["recipe"]["network_policy"].startswith("denied")
    assert re.fullmatch(r"[0-9a-f]{64}", receipt["result"]["output_sha256"])
    assert receipt["result"]["output_bytes"] > 0
    started = datetime.fromisoformat(receipt["validation_started_at"])
    ended = datetime.fromisoformat(receipt["validation_ended_at"])
    validated = datetime.fromisoformat(receipt["validated_at"])
    assert started <= ended <= validated
    assert receipt["closed_obligation_ids"] == []
    assert receipt["remaining_root_cut_set"] == ["M1143-T-VANISH"]
    assert receipt["first_unavailable_substantive_leaf"] == "M1143-L-GRADIENT"
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt_bound_files <= set(receipt["freshness"]["invalidation_inputs"])

    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["proof_body_added"] is True
    assert blocker["closed_obligation_ids"] == []
    assert blocker["remaining_root_cut_set"] == ["M1143-T-VANISH"]
    assert blocker["first_unavailable_substantive_leaf"] == "M1143-L-GRADIENT"
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    assert datetime.fromisoformat(blocker["recorded_at"]) <= validated

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "M1143-L-GRADIENT" in validation
    assert "does not claim theorem completion" in validation
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1143 partial proof phase: normalization, limit, and calculus bodies checked")
    print("closed frozen obligations: none; planned fingerprints await master reconciliation")
    print("root closure: open (M3) at M1143-T-VANISH; theorem_complete=false")


if __name__ == "__main__":
    main()
