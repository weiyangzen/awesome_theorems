#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, blocker, and worker-packet checks for THM-M-0814."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0814-PROOF"
THEOREM = "THM-M-0814"
BASE_REVISION = "b62c08f262435e44a30ad3fc88a4712e3954afc7"
BASE_TREE = "f7374dcf5690374a2e9e5d13ac124b34c7ecfab1"
STATEMENT_EXPRESSION = "f9fc7813f437ebcd4b2b7327373dd76134d651c1624d2a06f689e84ec571a21e"
DENOMINATOR_SHA256 = "f0ff554fe8facfa66bbdcbe9f036f7de20ebbe738b1d2cc9b4c06a899d673d7b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROVISIONALLY_CLOSED_IDS = ["M0814-L-WEAK-DUALITY"]
PARTIAL_PROGRESS_IDS = ["M0814-B-NO-CHAIN"]
REMAINING_MACHINE_CUT = ["M0814-L-MAX-ATTAIN", "M0814-T-EQUAL-CUT"]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/instance.json",
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


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1373
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0814-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0814-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for fragment in (
        "theorem weakDuality_proof : WeakDuality",
        "Finsupp.sum_finsetSum_comm",
        "theorem noChain_case",
        "letI : IsEmpty (Chain G source sink)",
        "theorem cutCertificate_of_equalCut",
        "theorem root_of_maximalFlowAttainment_and_equalCut",
        "assert_no_sorry weakDuality_proof",
        "#print axioms root_of_maximalFlowAttainment_and_equalCut",
    ):
        assert fragment in proof, fragment

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
        STATEMENT_EXPRESSION
    )
    expected_artifacts = build_obligation_artifacts.build()
    for filename, expected in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"),
        expected_artifacts,
    ):
        encoded = (json.dumps(expected, indent=2, ensure_ascii=True) + "\n").encode()
        assert (HERE / filename).read_bytes() == encoded, f"stale generated artifact: {filename}"
    assert registry["root_obligation_id"] == "M0814-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    for obligation_id in PROVISIONALLY_CLOSED_IDS + PARTIAL_PROGRESS_IDS:
        assert by_id[obligation_id]["statement_fingerprint"].startswith("planned:v1:sha256:")
        assert by_id[obligation_id]["terminal_proof_body_id"] is None
    assert graphs["closure_boundary"]["closed_obligations"] == []
    assert graphs["closure_boundary"]["root_closed"] is False
    assert instance["accepted_proof_state"] == []
    assert instance["accepted_receipt_ids"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM}/{name}" for name in actual_files
    }

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
    assert receipt["owner"] == "Stage1 integration lane"
    assert receipt["review_due"]
    assert receipt["supersession_state"]
    assert receipt["revocation_state"] == "not-accepted"
    assert receipt["incident_path"]
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["provisionally_closed_obligation_ids"] == PROVISIONALLY_CLOSED_IDS
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["remaining_machine_root_cut_set"] == REMAINING_MACHINE_CUT
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_validation_sha256", "proof-validation.md"),
        ("proof_blocker_sha256", "proof-blocker.json"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    nonrelease = receipt["nonrelease_evidence_boundary"]
    assert nonrelease["repository_dirty"] is True
    assert nonrelease["content_addressed_receipt_id"] is False
    assert "not release evidence" in nonrelease["classification"]
    recipe = receipt["recipe"]
    assert recipe["cwd"] == "."
    assert recipe["argv"] == ["bash", f"Stage1_Instances/{THEOREM}/check_proof.sh"]
    assert recipe["env_allowlist"] == {
        "LC_ALL": "C inside Lean invocations",
        "LANG": "C inside Lean invocations",
        "NO_COLOR": "1 inside Lean invocations",
        "LEAN_NUM_THREADS": "1 inside Lean invocations",
        "LEAN_PATH": (
            "derived by lake env from the pinned manifest, with the fresh temporary "
            "directory prepended after Statement elaboration"
        ),
    }
    assert recipe["timeout_seconds"] == 300
    assert recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0
    assert isinstance(recipe["expected_outputs"], list) and recipe["expected_outputs"]
    assert recipe["covered_obligation_ids"] == PROVISIONALLY_CLOSED_IDS
    assert recipe["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS_IDS

    assert blocker["item_id"] == ITEM and blocker["theorem_id"] == THEOREM
    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["provisionally_closed_obligation_ids"] == PROVISIONALLY_CLOSED_IDS
    assert blocker["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS_IDS
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
    assert "root remains open" in validation
    assert "theorem_complete=false" in validation
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0814 partial proof phase: weak duality and no-chain branch checked")
    print("accepted state unchanged; root remains open at M3")
    print("theorem_complete=false")


if __name__ == "__main__":
    main()
