#!/usr/bin/env python3
"""Fail-closed scope and evidence checks for the THM-M-0510 proof contribution."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0510-PROOF"
THEOREM = "THM-M-0510"
BASE_REVISION = "7505614b75de56cf10bbd196a4aaa0ca2a117064"
BASE_TREE = "730e162a2133e4a077d764043b5e722c1f7feb39"
STATEMENT_SHA256 = "2bdbd9447b9917305ecb72e4268f14effd74ea12a55a2f9aa620fe1d497bd049"
REGISTRY_SHA256 = "678c26527bb23c368a7db74bc1aa6ac71e5ef479f8e0e54926fb288a2bde36b2"
GRAPHS_SHA256 = "98caff1f27cb7c1562624cde98867d64aa6c9387aa4af427cf3b7164e937987a"
DENOMINATOR_SHA256 = "59e9147cc46427b6fc6a114cf81f7a5710c3441cf3a9ef2a74b1690f08f167dd"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
OBLIGATION = "M0510-N-EULER-PRODUCT"
FINGERPRINT = "planned:v1:sha256:831a1ed9d493aa01d83532c6a1543fd546c3774247ba40030c635b2e80b68c30"
REMAINING_CUT = [
    "M0510-N-COEFFICIENT",
    "M0510-C-CONTOUR",
    "M0510-L-MODULAR",
    "M0510-L-MINOR-BOUND",
    "M0510-X-SOURCE",
    "M0510-X-FOUNDATION",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
    f"Stage1_Instances/{THEOREM}/proof-execution.md",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
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
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 884
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-0510-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0510-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    declared = set(re.findall(r"^(?:@\[simp\]\s*)?theorem\s+([A-Za-z0-9_]+)", proof, re.MULTILINE))
    assert declared == {
        "coeff_ordinaryPartitionSeries",
        "geometricFactor_mul_oneSub",
        "hasProd_ordinaryPartitionSeries_geometric",
        "ordinaryPartitionSeries_eq_geometricProduct",
        "ordinaryPartitionSeries_mul_eulerProduct",
    }
    for marker in (
        "Nat.Partition.hasProd_powerSeriesMk_card_restricted",
        "tsum_pow_mul_one_sub_of_constantCoeff_eq_zero",
        "multipliable_one_sub_X_pow",
        "#print axioms ordinaryPartitionSeries_mul_eulerProduct",
    ):
        assert marker in proof, marker
    assert "HardyRamanujanAsymptoticTarget := by" not in proof

    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "obligation-registry.json") == REGISTRY_SHA256
    assert sha256(HERE / "typed-graphs.json") == GRAPHS_SHA256
    assert registry["root_obligation_id"] == "M0510-ROOT"
    computed_denominator = hashlib.sha256(
        json.dumps(registry["obligations"], sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert computed_denominator == DENOMINATOR_SHA256
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    assert by_id[OBLIGATION]["statement_fingerprint"] == FINGERPRINT
    assert by_id[OBLIGATION]["terminal_proof_body_id"] is None
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["theorem_complete"] is False
    assert closure["root_machine_classification"] == "M3"
    assert closure["first_open_cut"][0] == OBLIGATION

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["canonical_target"] == "Stage1Instances.THM_M_0510.HardyRamanujanAsymptoticTarget"
    assert receipt["canonical_target_statement_sha256"] == STATEMENT_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["supported_obligation_ids"] == [OBLIGATION]
    assert receipt["partial_progress_toward_obligation_ids"] == []
    assert receipt["obligation_statement_fingerprints"] == {OBLIGATION: FINGERPRINT}
    assert receipt["provisionally_closed_obligation_ids"] == [OBLIGATION]
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["proof_phase_complete"] is False
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == REMAINING_CUT
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("anchor_audit_sha256", "AnchorAudit.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_execution_sha256", "proof-execution.md"),
        ("proof_blocker_sha256", "proof-blocker.json"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["inputs"]["lean_toolchain_sha256"] == sha256(
        ROOT / "Formalizations/Lean/lean-toolchain"
    )
    assert receipt["inputs"]["lake_manifest_sha256"] == sha256(
        ROOT / "Formalizations/Lean/lake-manifest.json"
    )

    assert blocker["item_id"] == ITEM and blocker["theorem_id"] == THEOREM
    assert blocker["base_revision"] == BASE_REVISION and blocker["base_tree"] == BASE_TREE
    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["verdict"] == "no_state_change"
    assert blocker["proof_body_added"] is blocker["partial_bodies_self_tested"] is True
    assert blocker["proof_phase_complete"] is False
    assert blocker["provisionally_closed_obligation_ids"] == [OBLIGATION]
    assert blocker["accepted_closed_obligation_ids"] == []
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    assert blocker["remaining_root_cut_set"] == REMAINING_CUT
    assert blocker["first_failed_gate"].startswith("M0510-N-COEFFICIENT:")
    assert blocker["selftest_manifest_written"] is True

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
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

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0510 proof phase: Euler-product normalization evidence checked")
    print("provisionally closed obligation: M0510-N-EULER-PRODUCT")
    print("root remains open M3; theorem_complete=false")


if __name__ == "__main__":
    main()
