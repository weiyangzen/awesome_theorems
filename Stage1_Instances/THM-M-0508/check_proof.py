#!/usr/bin/env python3
"""Fail-closed source and evidence checks for S56-M-0508-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0508-PROOF"
THEOREM = "THM-M-0508"
BASE_REVISION = "8714972d4cf7ae256a92b9e35032c9df1bf5745c"
BASE_TREE = "080d14e14102a733c6992aa0644e3c65d755e91b"
DENOMINATOR_SHA256 = "79ff122b736335e90938cf7304db0b680dc23531e4d12d4b8c987d0ddc953bc2"
EXPRESSION_SHA256 = "54ddaa6fe49c75368fd333adae9bc7ab50a9542516ef24d73fb5e43f0c1ac5fb"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
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
    value = json.loads(path.read_text(encoding="utf-8"))
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
    instance = load(HERE / "instance.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    # Base identity is receipt provenance. Integration changes HEAD, so replay
    # requires that base to remain in history rather than requiring HEAD equal it.
    assert git("show", "-s", "--format=%T", BASE_REVISION) == BASE_TREE
    subprocess.check_call(
        ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"],
        cwd=ROOT,
    )
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 882
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["state"] in {"[ ]", "[_]", "[x]"}
    assert item["depends_on"] == ["S56-M-0508-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"]
        if row["id"] == "S56-M-0508-OBLIGATION_TREE"
    )
    assert predecessor["state"] in {"[_]", "[x]"}

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import Statement",
        "import ObligationTree",
        "theorem vinogradovThreePrimesTarget_iff_eventualPositiveRepresentationCount",
        "theorem vinogradovThreePrimesTarget_of_eventualPositiveRepresentationCount",
        "ObligationTree.representationCount_pos_iff",
        "#print sorries vinogradovThreePrimesTarget_iff_eventualPositiveRepresentationCount",
        "#print sorries vinogradovThreePrimesTarget_of_eventualPositiveRepresentationCount",
    ):
        assert marker in proof, marker
    assert "theorem vinogradovThreePrimesTarget_proof" not in proof

    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert instance["canonical_formal_target"]["elaborated_expression_hash"] == (
        f"sha256:{EXPRESSION_SHA256}"
    )
    closure = graphs["closure_boundary"]
    assert closure["root_machine_debt"] == "M4"
    assert closure["root_closed"] is False
    assert closure["theorem_complete"] is False
    assert closure["first_open_cut_set"] == [
        "M0508-N-FOURIER",
        "M0508-B-ARCS",
        "M0508-L-MAJOR",
        "M0508-L-SINGULAR",
        "M0508-L-MINOR",
    ]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["canonical_statement_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["supported_obligation_ids"] == []
    assert receipt["partial_progress_toward_obligation_ids"] == []
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["proof_body"]["classification"] == "local_proof_body_partial_interface"
    assert receipt["proof_body"]["local_roles"] == ["composition", "composition"]
    assert receipt["proof_body"]["terminal_declarations"] == receipt["exact_declarations"]
    assert receipt["proof_body"]["transitive_trust_closure"]["axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("instance_sha256", "instance.json"),
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
    result = receipt["result"]
    assert result["root_kernel_closed"] is False
    assert result["root_closed"] is False
    assert result["audit_complete"] is False
    assert result["theorem_complete"] is False
    assert receipt["audit_complete"] is False
    assert receipt["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == closure["first_open_cut_set"]
    recipe = receipt["recipe"]
    assert recipe["argv"] == ["bash", f"Stage1_Instances/{THEOREM}/check_proof.sh"]
    assert recipe["network_policy"] == "denied"
    assert recipe["network_enforcement"].startswith("not OS-enforced")
    assert recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == []
    assert recipe["covered_declarations"] == receipt["exact_declarations"]

    assert blocker["proof_body_added"] is True
    assert blocker["partial_proof_receipt_id"] == receipt["receipt_id"]
    assert blocker["statement_sha256"] == sha256(HERE / "Statement.lean")
    assert blocker["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert blocker["obligation_tree_sha256"] == sha256(HERE / "ObligationTree.lean")
    assert blocker["obligation_registry_sha256"] == sha256(HERE / "obligation-registry.json")
    assert blocker["typed_graphs_sha256"] == sha256(HERE / "typed-graphs.json")
    assert blocker["anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    assert blocker["partial_progress_toward_obligation_ids"] == []
    assert blocker["root_closed"] is False
    assert blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.exists():
        packet = load(selftest_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]
        status = subprocess.check_output(
            ["git", "status", "--short", "--untracked-files=all"],
            cwd=ROOT,
            text=True,
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

    print("PASS THM-M-0508 proof evidence: hashes, pin, scope, and open-root boundary agree")


if __name__ == "__main__":
    main()
