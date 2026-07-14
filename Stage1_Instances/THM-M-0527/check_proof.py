#!/usr/bin/env python3
"""Fail-closed proof-source, pin, evidence, and handoff checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0527-PROOF"
THEOREM = "THM-M-0527"
BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
STATEMENT_SHA256 = "00d2308cc4275b3ca7958961bc0ffc2c06651a64eff06773960f8aac94251327"
EXPRESSION_SHA256 = "4c7a7d4c54edb4a2d46091dda31f20a26664f005b20495012be1425dd625f55d"
DENOMINATOR_SHA256 = "3b54d00ce59d2dba93b119edf669c1bf39c3f402e5e0d7dcb7139f013f135df1"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_DECLARATIONS = {
    "locPathConnectedSpace_of_isLocalHomeomorph",
    "covering_locPathConnectedSpace",
    "comparisonLift",
    "inducedSubgroup_eq_of_isomorphic",
    "inducedMap_naturality",
    "inducedMap_surjective",
    "range_eq_of_comp_eq_of_surjective",
    "inducedSubgroup_eq_of_naturality",
    "inducedSubgroup_eq_of_isomorphic_via_naturality",
    "comparisonMaps_mutualInverse",
    "comparisonHomeomorph",
    "isomorphic_of_comparisonMaps",
    "isomorphic_of_inducedSubgroup_eq",
    "inducedSubgroup_eq_iff_isomorphic",
}
FIBER_IDS = [
    "M0527-FIB",
    "M0527-FIB-FWD",
    "M0527-FIB-LIFT-PQ",
    "M0527-FIB-LIFT-QP",
    "M0527-FIB-INVERSE",
    "M0527-FIB-HOME",
    "M0527-FIB-OVER",
    "M0527-FIB-REV",
    "M0527-FIB-REV-MAP",
    "M0527-FIB-REV-RANGE",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
    f"Stage1_Instances/{THEOREM}/proof-blocker.md",
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


def check_axiom_output(output_path: Path) -> None:
    output = output_path.read_text(encoding="utf-8")
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    reports = re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]", output, re.DOTALL)
    names = {name.rsplit(".", 1)[-1] for name, _ in reports}
    assert names == EXPECTED_DECLARATIONS, (names, EXPECTED_DECLARATIONS)
    for name, body in reports:
        actual = {item.strip() for item in body.split(",") if item.strip()}
        assert actual == allowed, f"unexpected axiom closure for {name}: {actual}"
    assert "sorryAx" not in output and "declaration uses 'sorry'" not in output
    assert "error:" not in output


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} PROOF_OUTPUT")
    check_axiom_output(Path(sys.argv[1]))

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
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 584
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0527-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0527-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    theorem_names = set(re.findall(r"^theorem\s+([A-Za-z0-9_]+)", proof, re.MULTILINE))
    def_names = set(re.findall(r"^noncomputable def\s+([A-Za-z0-9_]+)", proof, re.MULTILINE))
    assert theorem_names | def_names == EXPECTED_DECLARATIONS
    for fragment in (
        "existsUnique_continuousMap_lifts_of_range_le",
        "comparisonMaps_mutualInverse P Q",
        "inducedMap_naturality P Q",
        "range_eq_of_comp_eq_of_surjective",
        "inducedMap_surjective P Q",
        "inducedSubgroup_eq_iff_isomorphic",
    ):
        assert fragment in proof, fragment

    canonical = statement["canonical_formal_target"]
    assert canonical["statement_file_sha256"] == STATEMENT_SHA256
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0527-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    fingerprints = {
        row["obligation_id"]: row["statement_fingerprint"]
        for row in registry["obligations"] if row["obligation_id"] in FIBER_IDS
    }
    assert set(fingerprints) == set(FIBER_IDS)
    assert all(value.startswith("planned:v1:sha256:") for value in fingerprints.values())
    assert all(
        row["terminal_proof_body_id"] is None
        for row in registry["obligations"] if row["obligation_id"] in FIBER_IDS
    )
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["remaining_root_cut_set"] == [
        "M0527-EX-COVER", "M0527-EX-RANGE", "M0527-FIB"
    ]
    assert closure["theorem_complete"] is False
    assert "registry_denominator_sha256" not in graphs

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
    assert receipt["canonical_target_statement_sha256"] == STATEMENT_SHA256
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    receipt_names = {name.rsplit(".", 1)[-1] for name in receipt["exact_declarations"]}
    assert receipt_names == EXPECTED_DECLARATIONS
    assert receipt["supported_obligation_ids"] == []
    assert receipt["partial_progress_toward_obligation_ids"] == FIBER_IDS
    assert receipt["obligation_statement_fingerprints"] == fingerprints
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_validation_sha256", "proof-validation.md"),
        ("proof_blocker_json_sha256", "proof-blocker.json"),
        ("proof_blocker_md_sha256", "proof-blocker.md"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == ["M0527-EX-COVER", "M0527-EX-RANGE"]

    assert blocker["item_id"] == ITEM and blocker["theorem_id"] == THEOREM
    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["partial_progress_toward_obligation_ids"] == FIBER_IDS
    assert blocker["provisionally_closed_obligation_ids"] == []
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
    assert "claims zero complete frozen obligations" in validation
    assert "theorem_complete=false" in validation
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0527 partial proof phase: fiber-classification bodies checked")
    print("closed frozen obligations: none; root remains open M3")
    print("theorem_complete=false; accepted state unchanged")


if __name__ == "__main__":
    main()
