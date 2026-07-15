#!/usr/bin/env python3
"""Fail-closed source and evidence checks for S56-M-0958-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0958-PROOF"
THEOREM = "THM-M-0958"
BASE_REVISION = "435748c4550bad6c03c34931d309befe9658460d"
BASE_TREE = "5354633764fc606c80fe66838d43b491165ea056"
DENOMINATOR_SHA256 = "a66280599ad67d6daac4bea5c3e08484e1b6c1aa0d75223a5d3aaf428c383e5b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
PARTIAL_PROGRESS_IDS = [
    "M0958-C-DIGIT-EMBED",
    "M0958-L-DIGIT-INJECTIVE",
    "M0958-L-NO-CARRY",
    "M0958-L-PROGRESSION-FREE",
    "M0958-L-EMBED-RANGE",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate key in {path}: {key}"
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

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1492
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0958-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["deliverable"] == "Implement or pin/import the required proof bodies without placeholders."

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|proof_wanted)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "theorem map_injOn_digit_box",
        "theorem map_image_threeAPFree",
        "theorem map_image_lt_pow",
        "theorem oneBasedDigitImage_subset",
        "theorem oneBasedDigitImage_progressionFree",
        "structure DigitEmbeddingPackage",
        "theorem digitEmbeddingPackage_checked",
        "#print axioms digitEmbeddingPackage_checked",
    ):
        assert marker in proof, marker
    assert "theorem elkinConstruction" not in proof
    assert "theorem proof : ElkinConstructionTarget" not in proof

    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    observed = registry["status_observed_after_freeze"]
    assert observed["accepted_closed_obligations"] == []
    assert observed["accepted_root_machine_debt"] == "M3"
    closure = graphs["closure_boundary"]
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["accepted_closed_obligations"] == []
    assert closure["minimal_open_machine_proof_cut_sets"] == [["M0958-T-WITNESS"]]
    assert closure["theorem_complete"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["supported_obligation_ids"] == []
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS_IDS
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["exact_declarations"] == [
        "Stage1Instances.THM_M_0958.Proof.map_injOn_digit_box",
        "Stage1Instances.THM_M_0958.Proof.map_add_eq",
        "Stage1Instances.THM_M_0958.Proof.map_image_threeAPFree",
        "Stage1Instances.THM_M_0958.Proof.card_map_image",
        "Stage1Instances.THM_M_0958.Proof.map_image_lt_pow",
        "Stage1Instances.THM_M_0958.Proof.oneBasedDigitImage_subset",
        "Stage1Instances.THM_M_0958.Proof.card_oneBasedDigitImage",
        "Stage1Instances.THM_M_0958.Proof.oneBasedDigitImage_progressionFree",
        "Stage1Instances.THM_M_0958.Proof.digitEmbeddingPackage_checked",
    ]
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_validation_sha256", "proof-validation.md"),
        ("proof_blocker_sha256", "proof-blocker.json"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == ["M0958-T-WITNESS"]
    recipe = receipt["recipe"]
    assert recipe["recipe_id"] == "S56-M-0958-PROOF-RECIPE-v1"
    assert recipe["cwd"] == "."
    assert recipe["argv"] == ["bash", f"Stage1_Instances/{THEOREM}/check_proof.sh"]
    assert recipe["network"] == "not_used" and recipe["covered_declarations"] == 9
    assert recipe["covered_ids"] == []

    assert blocker["proof_body_added"] is True
    assert blocker["partial_proof_receipt_id"] == receipt["receipt_id"]
    assert blocker["supported_obligation_ids"] == []
    assert blocker["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS_IDS
    assert blocker["root_closed"] is False and blocker["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "zero frozen obligations are claimed closed" in validation
    assert "not theorem completion" in validation
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0958 proof evidence: local radix bodies, hashes, pin, scope, and open root agree")


if __name__ == "__main__":
    main()
