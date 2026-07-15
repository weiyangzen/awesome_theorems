#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, blocker, and packet checks for THM-M-1060."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1060-PROOF"
THEOREM = "THM-M-1060"
BASE_REVISION = "48fb6596b1844f4183c411142415d872ff21e842"
BASE_TREE = "eb8dfff0e90b5ce5b11ac2096777060d62874064"
STATEMENT_SHA256 = "d2bfdc20fcb2cd7c3de27588917dad689056d73e05880814590ab1e3c604581a"
REGISTRY_SHA256 = "cb01f4a60e1dc76401a13d41c7fc14a38e391e6d15325827dff178788f2add05"
GRAPHS_SHA256 = "f707b692bd77c98f1aa435c51165a83f539fdb1bb96a2d765f47746c95814cb9"
PROOF_SHA256 = "9d5626f018862f239c79cdc49b2917abc23565d81fb8c8b8dc7aee6cbedf2069"
CHECK_SH_SHA256 = "356f7b432ae01d6b35b130543ce83d826772fce007ca705d0df8b105ae804531"
DENOMINATOR_SHA256 = "32d2df11f1dd7faa40b53ee0ae86fc93d52317f80c4d3e9c1f8bcbe00b2a3f74"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PARTIAL_ID = "M1060-N-WIENER"
PARTIAL_FINGERPRINT = (
    "planned:v1:sha256:4beb7a80c6c6465ec15dc4165162fe4a89d9b61f584edcbeee2abaab23879625"
)
REMAINING_CUT = [
    "M1060-L-GAUSSIAN",
    "M1060-L-MODULUS",
    "M1060-L-EXP-EQUIV",
    "M1060-L-RATE-ID",
    "M1060-L-RATE-LSC",
    "M1060-L-SUBLEVEL-BOUND",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-blocker-2026-07-15-head-48fb6596.json",
    f"Stage1_Instances/{THEOREM}/proof-blocker-2026-07-15-head-48fb6596.md",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
}
NEW_DECLARATIONS = [
    "Stage1Instances.THM_M_1060.oneTimeVarianceAndLaw",
    "Stage1Instances.THM_M_1060.oneTimeLaw",
    "Stage1Instances.THM_M_1060.isGaussianProcess_of_isWienerMeasure",
]


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
    blocker = load(HERE / "proof-blocker-2026-07-15-head-48fb6596.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 503
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-1060-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1060-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    declared = set(re.findall(r"^theorem\s+([A-Za-z0-9_]+)", proof, re.MULTILINE))
    assert declared == {
        "measurableEvaluationLinear",
        "continuousScale",
        "isProbabilityMeasure_of_isWienerMeasure",
        "zeroTimeVarianceAndLaw",
        "zeroTimeLaw",
        "oneTimeVarianceAndLaw",
        "oneTimeLaw",
        "isGaussianProcess_of_isWienerMeasure",
    }
    for marker in (
        "oneTimeVarianceAndLaw",
        "oneTimeLaw",
        "isGaussianProcess_of_isWienerMeasure",
        "ProbabilityTheory.isGaussian_of_map_eq_gaussianReal",
        "#print axioms isGaussianProcess_of_isWienerMeasure",
    ):
        assert marker in proof, marker
    assert "SchilderTarget" not in without_comments(proof)

    assert sha256(proof_path) == PROOF_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "obligation-registry.json") == REGISTRY_SHA256
    assert sha256(HERE / "typed-graphs.json") == GRAPHS_SHA256
    assert sha256(HERE / "check_proof.sh") == CHECK_SH_SHA256
    assert registry["root_obligation_id"] == "M1060-ROOT"
    computed_denominator = hashlib.sha256(
        json.dumps(registry["frozen_denominators"], sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert computed_denominator == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    assert by_id[PARTIAL_ID]["statement_fingerprint"] == PARTIAL_FINGERPRINT
    assert by_id[PARTIAL_ID]["terminal_proof_body_id"] is None
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["root_closed"] is closure["audit_complete"] is False
    assert closure["theorem_complete"] is False
    assert closure["root_machine_debt"] == "M4"
    assert closure["remaining_root_cut_set"] == REMAINING_CUT
    assert instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}

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
    assert receipt["canonical_target"] == "Stage1Instances.THM_M_1060.SchilderTarget"
    assert receipt["canonical_target_statement_sha256"] == STATEMENT_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == PROOF_SHA256
    assert receipt["exact_declarations_added"] == NEW_DECLARATIONS
    assert receipt["supported_obligation_ids"] == []
    assert receipt["partial_progress_toward_obligation_ids"] == [PARTIAL_ID]
    assert receipt["obligation_statement_fingerprints"] == {
        PARTIAL_ID: PARTIAL_FINGERPRINT
    }
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
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
    assert blocker["frozen_implementation_cut_set"] == REMAINING_CUT
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

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1060 partial proof phase: three new local bodies and evidence checked")
    print("closed frozen obligations: none; root remains open M4")
    print("proof_phase_complete=false; theorem_complete=false; accepted state unchanged")


if __name__ == "__main__":
    main()
