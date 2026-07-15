#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, blocker, and packet checks for THM-M-1063."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1063-PROOF"
THEOREM = "THM-M-1063"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
STATEMENT_SHA256 = "de889c475bd663395eb9385627686109c645ba3446ee513c4019cf82f00a1847"
REGISTRY_SHA256 = "7886d9ce4b1552493476e336bfb5cc1b7537debe8249e61989cdeec86a85d5e8"
GRAPHS_SHA256 = "e63f2ce6eab9bc6fa942b6e1a412ab0b07063fcc978676daf125779c6a0875b5"
DENOMINATOR_SHA256 = "a55c3e289a005535836506a2ce233e3dbb5fa0a7b84717b38c221583d26a7703"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PARTIAL_IDS = ["M1063-N-STANDARDIZE", "M1063-X-SCALAR-CLT"]
FINGERPRINTS = {
    "M1063-N-STANDARDIZE":
        "planned:v1:sha256:c999ced1f79fb8c04da716e2aec8c5544156494af098559a3d8c5296c15d7d7a",
    "M1063-X-SCALAR-CLT":
        "planned:v1:sha256:067b4a734132ce8d686eb7ed8f4fd81dfe021715cca2a6dba013fa11bc088ed6",
}
REMAINING_CUT = [
    "M1063-L-CLT",
    "M1063-L-MODULUS",
    "M1063-L-ASCOLI",
    "M1063-L-PROKHOROV",
    "M1063-L-LAW-UNIQUE",
    "M1063-T-API",
]
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


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 506
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-1063-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1063-OBLIGATION_TREE"
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
        "standardizedIncrement_package",
        "scalarPartialSums_tendstoInDistribution",
    }
    for marker in (
        "def standardizedIncrement",
        "hIndep.comp",
        "variance_const_mul",
        "tendstoInDistribution_inv_sqrt_mul_sum",
        "#print axioms standardizedIncrement_package",
        "#print axioms scalarPartialSums_tendstoInDistribution",
    ):
        assert marker in proof, marker
    assert "DonskerInvariancePrinciple" not in proof

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "AwesomeTheorems.Stage1.THM_M_1063.DonskerInvariancePrinciple"
    )
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "DonskerTarget.lean") == STATEMENT_SHA256
    assert sha256(HERE / "obligation-registry.json") == REGISTRY_SHA256
    assert sha256(HERE / "typed-graphs.json") == GRAPHS_SHA256
    assert registry["root_obligation_id"] == "M1063-ROOT"
    computed_denominator = hashlib.sha256(
        json.dumps(
            registry["frozen_denominators"], sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()
    assert computed_denominator == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    assert by_id["M1063-ROOT"]["statement_fingerprint"] == (
        "lean-expression-sha256:"
        "a5bb2e2443661e20f8342ed0dba6b7f7ef5f5ce445bc2d5bbdf19ef5ce842c81"
    )
    for obligation_id in PARTIAL_IDS:
        assert by_id[obligation_id]["statement_fingerprint"] == FINGERPRINTS[obligation_id]
        assert by_id[obligation_id]["terminal_proof_body_id"] is None
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
    assert receipt["canonical_target"] == formal["declaration_or_expression"]
    assert receipt["canonical_target_statement_sha256"] == STATEMENT_SHA256
    assert receipt["canonical_target_expression_sha256"] == (
        "a5bb2e2443661e20f8342ed0dba6b7f7ef5f5ce445bc2d5bbdf19ef5ce842c81"
    )
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["exact_declarations"] == [
        "AwesomeTheorems.Stage1.THM_M_1063.Proof.standardizedIncrement_package",
        "AwesomeTheorems.Stage1.THM_M_1063.Proof.scalarPartialSums_tendstoInDistribution",
    ]
    assert receipt["supported_obligation_ids"] == []
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert receipt["obligation_statement_fingerprints"] == FINGERPRINTS
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["proof_phase_complete"] is False
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == REMAINING_CUT
    for key, filename in (
        ("donsker_target_sha256", "DonskerTarget.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("anchor_audit_lean_sha256", "AnchorAudit.lean"),
        ("anchor_audit_md_sha256", "anchor-audit.md"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_validation_sha256", "proof-validation.md"),
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
    assert blocker["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert blocker["provisionally_closed_obligation_ids"] == []
    assert blocker["accepted_closed_obligation_ids"] == []
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    assert blocker["remaining_root_cut_set"] == REMAINING_CUT
    assert blocker["first_failed_gate"].startswith("M1063-C-PATH / M1063-C-MEAS:")
    assert blocker["intake_root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
    assert blocker["frozen_graph_root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
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
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "claims zero entire frozen obligations closed" in validation
    assert "theorem_complete=false" in validation
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1063 partial proof phase: two local bodies and evidence checked")
    print("closed frozen obligations: none; root remains open M4")
    print("theorem_complete=false; accepted state unchanged")


if __name__ == "__main__":
    main()
