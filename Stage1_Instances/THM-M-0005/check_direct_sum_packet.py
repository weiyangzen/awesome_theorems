#!/usr/bin/env python3
"""Fail-closed packet checks for THM-M-0005 direct-sum proof progress."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0005-PROOF"
THEOREM = "THM-M-0005"
BASE_REVISION = "5bb515438bd0e1d53584e5243c5d434dfde7158e"
BASE_TREE = "8055b8d863f0978f110a628ab3ccc7ab1e146b12"
EXPRESSION_SHA256 = "f6396a70702a8bb45dbbb267ebd3ba10aae4f4db28cf25355f8fcd7bb607ddd4"
DENOMINATOR_SHA256 = "563eac891739af1e2468c4fd23e7465013f9e5791e069a03e22ccdf67119a762"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/ProofDirectSum20260715Head5bb51543Slot21.lean",
    f"Stage1_Instances/{THEOREM}/check_direct_sum_packet.py",
    f"Stage1_Instances/{THEOREM}/check_direct_sum_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-direct-sum-receipt-20260715-head-5bb51543-slot21.json",
    f"Stage1_Instances/{THEOREM}/proof-direct-sum-validation-20260715-head-5bb51543-slot21.md",
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
    proof_path = HERE / "ProofDirectSum20260715Head5bb51543Slot21.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-direct-sum-receipt-20260715-head-5bb51543-slot21.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    intake = load(HERE / "intake.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 100
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0005-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0005-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    declarations = re.findall(r"^#print axioms\s+(\S+)\s*$", proof, re.MULTILINE)
    assert len(declarations) == len(set(declarations)) == 8
    for fragment in (
        "def torDegreesSuccEquivTensorDegrees",
        "theorem torDegrees_zero_empty",
        "theorem torTerm_zero_isZero",
        "def torTermSuccIso",
        "theorem torTermSuccIso_hom_ι",
        "theorem torTermSuccIso_inv_ι",
    ):
        assert fragment in proof, fragment

    assert intake["canonical_formal_target"]["elaborated_expression_hash"] == (
        f"sha256:{EXPRESSION_SHA256}"
    )
    assert registry["root_obligation_id"] == "M0005-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    assert by_id["M0005-DIRECT-SUM"]["statement_fingerprint"] == (
        "sha256:08b00cd4b84b6426db825334735d28882e22f89502a7219292ed6a9512d62faa"
    )

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
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["inputs"]["statement_sha256"] == sha256(HERE / "KunnethStatement.lean")
    assert receipt["inputs"]["obligation_registry_sha256"] == sha256(
        HERE / "obligation-registry.json"
    )
    assert receipt["inputs"]["typed_graphs_sha256"] == sha256(HERE / "typed-graphs.json")
    assert receipt["inputs"]["check_direct_sum_packet_py_sha256"] == sha256(
        HERE / "check_direct_sum_packet.py"
    )
    assert receipt["inputs"]["check_direct_sum_proof_sh_sha256"] == sha256(
        HERE / "check_direct_sum_proof.sh"
    )
    assert receipt["supported_obligation_ids"] == []
    assert receipt["partial_progress_toward_obligation_ids"] == ["M0005-DIRECT-SUM"]
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["recipe"]["argv"] == [
        "bash",
        "Stage1_Instances/THM-M-0005/check_direct_sum_proof.sh",
    ]
    assert receipt["authoritative_graph_open_cut_set_unchanged"] == graphs[
        "closure_boundary"
    ]["remaining_root_cut_set"]

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

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0005 direct-sum proof packet: source, pins, and evidence checked")
    print("provisional closures: none; root remains open M3; theorem_complete=false")


if __name__ == "__main__":
    main()
