#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, blocker, and packet checks for THM-M-1010."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1010-PROOF"
THEOREM = "THM-M-1010"
BASE_REVISION = "ff3db6d51326417873f49c410421f8f3e13be993"
BASE_TREE = "9160a80a3e3588fd96fcd79323230668cc7d3df1"
STATEMENT_EXPRESSION = "f5f12340fa49d0be0eed038c99c47c921017284447b4a73f4b096e085e800d18"
DENOMINATOR_SHA256 = "8cf08f666cc9a074319f3cd4a905f2f94deedbe62f344fb3554399f3f5d16016"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
HAS_LAW_EXISTS_BLOB = "a0bb5807d52562981ecfdb0cd36abc92a02ea29b"
PROOF_SHA256 = "e652a54085931d125e1fa5ea7c73329fc46728c5e673a29e264af65914f79ca5"
PARTIAL_PROGRESS_IDS = [
    "M1010-C-COUPLING",
    "M1010-L-MEASURABLE",
    "M1010-L-LAWS",
]
FINGERPRINTS = {
    "M1010-C-COUPLING": "planned:v1:sha256:2114a36c3d644a0caaeded1c046d68e144464a1dee753c173b995907d132f995",
    "M1010-L-MEASURABLE": "planned:v1:sha256:2d0f0df4db060e183c5340f10f0907286200b0bcafcad3cf663e1bd9cd3aeae5",
    "M1010-L-LAWS": "planned:v1:sha256:48bbe4b5868e42bd8e992678c28a4e442b759c40bbe2d691f30e564801f436d3",
}
REMAINING_CUT = [
    "M1010-N-PARTITIONS",
    "M1010-C-INTERVAL",
    "M1010-L-MEASURABLE",
    "M1010-L-LAWS",
    "M1010-L-AE-STABILIZE",
]
BLOCKER_JSON = "proof-blocker-2026-07-15-head-ff3db6d5-slot39.json"
BLOCKER_MD = "proof-blocker-2026-07-15-head-ff3db6d5-slot39.md"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/{BLOCKER_JSON}",
    f"Stage1_Instances/{THEOREM}/{BLOCKER_MD}",
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
    blocker = load(HERE / BLOCKER_JSON)
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 290
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-1010-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1010-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern|external)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    declared = set(re.findall(r"^theorem\s+([A-Za-z0-9_]+)", proof, re.MULTILINE))
    assert declared == {
        "exists_common_space_exact_marginals",
        "representation_of_constant_laws",
        "target_for_constant_sequence",
    }
    for fragment in (
        "structure CommonMarginalData",
        "@Measurable sample S sampleMeasurable",
        "@HasLaw sample S sampleMeasurable",
        "exists_hasLaw_indepFun (fun _ : Option Nat => S) law",
        "#print axioms exists_common_space_exact_marginals",
    ):
        assert fragment in proof, fragment
    assert "theorem Target" not in proof and "theorem CouplingPackage" not in proof
    assert sha256(proof_path) == PROOF_SHA256

    assert statement["elaborated_expression_sha256"] == STATEMENT_EXPRESSION
    assert registry["root_obligation_id"] == "M1010-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    for obligation_id in PARTIAL_PROGRESS_IDS:
        assert by_id[obligation_id]["statement_fingerprint"] == FINGERPRINTS[obligation_id]
        assert by_id[obligation_id]["terminal_proof_body_id"] is None
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [
        "M1010-S-DEFINITIONS",
        "M1010-S-DOMAIN",
        "M1010-T-ASSEMBLE",
    ]
    assert closure["root_closed"] is closure["audit_complete"] is False
    assert closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == REMAINING_CUT

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    assert git("rev-parse", "HEAD:Mathlib/Probability/HasLawExists.lean", cwd=mathlib) == (
        HAS_LAW_EXISTS_BLOB
    )

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == PROOF_SHA256
    assert receipt["proof_body"]["upstream_source_blob"] == HAS_LAW_EXISTS_BLOB
    assert receipt["exact_declarations_added"] == [
        "Stage1Instances.THM_M_1010.exists_common_space_exact_marginals"
    ]
    assert receipt["supported_obligation_ids"] == []
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS_IDS
    assert receipt["obligation_statement_fingerprints"] == FINGERPRINTS
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor_audit.json"),
        ("task_dag_sha256", "task-dag.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_validation_sha256", "proof-validation.md"),
        ("proof_blocker_json_sha256", BLOCKER_JSON),
        ("proof_blocker_md_sha256", BLOCKER_MD),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["partial_declarations_kernel_closed"] is True
    assert receipt["result"]["proof_phase_complete"] is False
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == REMAINING_CUT

    assert blocker["item_id"] == ITEM and blocker["theorem_id"] == THEOREM
    assert blocker["base_revision"] == BASE_REVISION and blocker["base_tree"] == BASE_TREE
    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["verdict"] == "no_state_change" and blocker["state"] == "[_]"
    assert blocker["proof_body_added"] is blocker["partial_bodies_self_tested"] is True
    assert blocker["proof_phase_complete"] is False
    assert blocker["closed_obligations_added"] == []
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    assert blocker["remaining_root_cut_set"] == REMAINING_CUT
    assert blocker["selftest_manifest_written"] is True

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
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "receipt claims zero new\nfrozen obligations closed" in validation
    assert "proof_phase_complete=false" in validation
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1010 partial proof phase: one new common-marginals body checked")
    print("closed frozen obligations added: none; root remains open M3")
    print("proof_phase_complete=false; theorem_complete=false; accepted state unchanged")


if __name__ == "__main__":
    main()
