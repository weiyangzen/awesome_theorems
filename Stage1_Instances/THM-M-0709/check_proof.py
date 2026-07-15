#!/usr/bin/env python3
"""Fail-closed evidence checks for the THM-M-0709 partial proof phase."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0709-PROOF"
THEOREM = "THM-M-0709"
BASE_REVISION = "4ba3f2fd1e609b5958f24e0415eef9300da16924"
BASE_TREE = "6abc1f64758c17a59dad8c80ac44f238983dc720"
EXPRESSION_SHA256 = "5d375802e054a1c87b9fe6c8c24b728e9bcf8bfa20025ebe987d461545926d03"
DENOMINATOR_SHA256 = "f3731049c66ed6cf5e4687115b723249d54dae577f83859e130b76911f519b38"
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


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 750
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0709-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0709-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import Mathlib.Computability.Reduce",
        "import Statement",
        "theorem not_computablePred_of_manyOneReducible",
        "ComputablePred.computable_of_manyOneReducible hred htarget",
        "theorem haltingPredicate_not_computable",
        "ComputablePred.halting_problem input",
        "theorem postCorrespondenceUndecidable_of_haltingReduction",
        "hred : HaltingPredicate input ≤₀ HasSolution",
        "#print sorries ComputablePred.halting_problem",
        "#print axioms ComputablePred.halting_problem",
    ):
        assert marker in proof, marker
    assert "theorem postCorrespondenceUndecidable :" not in proof

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0709.PostCorrespondenceUndecidable"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    computed_denominator = hashlib.sha256(
        json.dumps(registry["obligations"], sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert computed_denominator == DENOMINATOR_SHA256
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    expected_fingerprints = {
        obligation_id: by_id[obligation_id]["statement_fingerprint"]
        for obligation_id in ("M0709-N-HALTING", "M0709-T-UNDECIDABLE", "M0709-ROOT")
    }
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["root_machine_classification"] == "M3"
    assert graphs["closure_boundary"]["theorem_complete"] is False

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
    assert receipt["obligation_statement_fingerprints"] == expected_fingerprints
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["provisionally_closed_obligation_ids"] == ["M0709-N-HALTING"]
    assert receipt["partial_progress_toward_obligation_ids"] == [
        "M0709-T-UNDECIDABLE", "M0709-ROOT"
    ]
    assert receipt["accepted_closed_obligation_ids"] == []
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False

    assert blocker["item_id"] == ITEM and blocker["theorem_id"] == THEOREM
    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["provisionally_closed_obligation_ids"] == ["M0709-N-HALTING"]
    assert blocker["partial_progress_toward_obligation_ids"] == [
        "M0709-T-UNDECIDABLE", "M0709-ROOT"
    ]
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    assert blocker["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    expected_sources = {
        "Mathlib/Computability/Halting.lean": (
            "0834371356762db805d37208b9cf8a1fc0efd217",
            "c2a073a05c631e7fc957577a66025e9ac36dac741f9aa865e0f053b17f0c85de",
        ),
        "Mathlib/Computability/Reduce.lean": (
            "aa5487c021cfdb4c7644efdd30ec5eb9dc0775bb",
            "30513e477c461fdce1518542f4dc16085f1d98ab47ba2bfbc28d5b741b18e556",
        ),
    }
    for path, (blob, digest) in expected_sources.items():
        assert git("rev-parse", f"HEAD:{path}", cwd=mathlib) == blob
        assert sha256(mathlib / path) == digest

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git(
        "status", "--short", "--untracked-files=all", "--",
        f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
    )
    actual_changes = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "not an\nunconditional root proof" in validation
    assert "remains M3" in validation
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0709 partial proof: pinned halting leaf and terminal transfer checked")
    print("root closure: open (M3); halting-to-binary-PCP reduction remains unimplemented")
    print("theorem_complete=false; accepted state unchanged")


if __name__ == "__main__":
    main()
