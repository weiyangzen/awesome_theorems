#!/usr/bin/env python3
"""Fail-closed source, pin, graph, and receipt checks for S56-M-0030-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0030-PROOF"
THEOREM = "THM-M-0030"
BASE_REVISION = "ebd5f75831296a8a35e7b33013b964f2baf31bb9"
BASE_TREE = "d1e4bc83c803eefcd9898aac57352265a29f0658"
EXPRESSION_SHA256 = "53389852e2c0875086c2c28cb4a60448670ee29145e13d86b4b1ad3e9df8861e"
DENOMINATOR_SHA256 = "2c8a394f62ce23e20c104f25129c82e7966b24cc2ac991a50f9d7a68ce1c6a45"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_SOURCE_SHA256 = "b161e2c4ce77f1224648467573dd4ba4c0ebc1ed734118e70df4cb39b33b1a72"
MATHLIB_SOURCE_BLOB = "c4fc3737f1859f1e22d387b199b46fe32d5f5093"
MATHLIB_BODY_SHA256 = "bed35e82de1fe7cbabba8e7db71f6c1d606c5b76547a3740c93089490775bf49"
CLOSED_IDS = [
    "M0030-ROOT",
    "M0030-X-MATHLIB-BODY",
    "M0030-N-FINITE-MODULE",
    "M0030-N-JACOBSON",
    "M0030-N-LOCAL-CONTAINMENT",
    "M0030-L-PROPER-MAXIMAL",
    "M0030-L-MAXIMAL-JACOBSON",
    "M0030-L-JACOBSON-UNIT",
    "M0030-X-JACOBSON-UNIT-SOURCE",
    "M0030-N-FIXEDPOINT-IFF",
    "M0030-T-FIXEDPOINT-COMPOSE",
    "M0030-B-FIXEDPOINT-FORWARD",
    "M0030-B-FIXEDPOINT-BACKWARD",
]
SOURCE_MAPPED_IDS = [
    "M0030-C-INFIMUM-SUBMODULE",
    "M0030-C-STABLE-INTERSECTION",
    "M0030-L-STABILIZATION-INDEX",
    "M0030-T-STABILITY-EVALUATE",
    "M0030-L-FG-NAKAYAMA",
    "M0030-L-POWER-INDUCTION",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip() == BASE_REVISION
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True
    ).strip() == BASE_TREE

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1075
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0030-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import ObligationTree",
        "theorem exactMathlibAnchor : ExactMathlibAnchor.{u}",
        "Ideal.iInf_pow_eq_bot_of_isLocalRing I hI",
        "theorem fixedPointCharacterization : FixedPointCharacterizationTarget.{u, v}",
        "Ideal.mem_iInf_smul_pow_eq_bot_iff I x",
        "theorem jacobsonIntersection_via_frozen_composition",
        "theorem finiteModuleIntersection_via_frozen_composition",
        "theorem exactMathlibAnchor_via_frozen_composition",
        "theorem krullIntersection_direct : KrullIntersectionTarget.{u}",
        "theorem krullIntersection_via_pinned_anchor",
        "theorem krullIntersection_via_frozen_composition",
        "#print sorries Ideal.iInf_pow_eq_bot_of_isLocalRing",
        "#print axioms krullIntersection_via_frozen_composition",
    ):
        assert marker in proof, marker

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["closed_obligation_ids"] == CLOSED_IDS
    assert receipt["source_mapped_not_individually_closed_ids"] == SOURCE_MAPPED_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["proof_body"]["terminal_body_sha256"] == MATHLIB_BODY_SHA256
    assert receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
    assert receipt["inputs"]["obligation_tree_sha256"] == sha256(
        HERE / "ObligationTree.lean"
    )
    assert receipt["inputs"]["obligation_registry_sha256"] == sha256(
        HERE / "obligation-registry.json"
    )
    assert receipt["inputs"]["typed_graphs_sha256"] == sha256(
        HERE / "typed-graphs.json"
    )
    assert receipt["inputs"]["anchor_audit_sha256"] == sha256(
        HERE / "anchor-audit.json"
    )
    assert receipt["inputs"]["validation_specs_sha256"] == sha256(
        HERE / "validation-specs.json"
    )
    assert receipt["inputs"]["check_proof_sh_sha256"] == sha256(
        HERE / "check_proof.sh"
    )
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["theorem_complete"] is False

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0030.KrullIntersectionTarget"
    )
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0030-ROOT"
    registry_rows = {row["obligation_id"]: row for row in registry["obligations"]}
    node_evidence = receipt["provisional_obligation_evidence"]
    assert [row["obligation_id"] for row in node_evidence] == CLOSED_IDS
    for row in node_evidence:
        assert row["statement_fingerprint"] == registry_rows[row["obligation_id"]][
            "statement_fingerprint"
        ]
        assert row["local_role"] and row["declarations"]
    required_machine = registry["frozen_denominators"]["required_machine"]
    architecture_ids = {row for row in required_machine if not row.startswith("M0030-S-")}
    assert architecture_ids == set(CLOSED_IDS + SOURCE_MAPPED_IDS)
    assert receipt["recipe"]["covered_obligation_ids"] == CLOSED_IDS
    assert receipt["recipe"]["recipe_id"] == "S56-M-0030-PROOF-LEAN"
    assert receipt["recipe"]["env_allowlist"] == {}
    assert receipt["recipe"]["network_policy"] == "denied"
    assert receipt["recipe"]["expected_exit"] == 0

    proof_pairs = {
        (edge["from"], edge["to"])
        for edge in graphs["graphs"]["proof"]["edges"]
        if edge["type"] == "proof_requires"
    }
    assert proof_pairs == {
        ("M0030-ROOT", "M0030-X-MATHLIB-BODY"),
        ("M0030-X-MATHLIB-BODY", "M0030-N-FINITE-MODULE"),
        ("M0030-N-FINITE-MODULE", "M0030-N-JACOBSON"),
        ("M0030-N-FINITE-MODULE", "M0030-N-LOCAL-CONTAINMENT"),
        ("M0030-N-LOCAL-CONTAINMENT", "M0030-L-PROPER-MAXIMAL"),
        ("M0030-N-LOCAL-CONTAINMENT", "M0030-L-MAXIMAL-JACOBSON"),
        ("M0030-N-JACOBSON", "M0030-N-FIXEDPOINT-IFF"),
        ("M0030-N-JACOBSON", "M0030-L-JACOBSON-UNIT"),
        ("M0030-L-JACOBSON-UNIT", "M0030-X-JACOBSON-UNIT-SOURCE"),
    }

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    source_rel = Path("Mathlib/RingTheory/Filtration.lean")
    source = mathlib / source_rel
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, text=True
    ).strip() == MATHLIB_REVISION
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True
    ).strip() == MATHLIB_TREE
    assert subprocess.check_output(
        ["git", "rev-parse", f"HEAD:{source_rel}"], cwd=mathlib, text=True
    ).strip() == MATHLIB_SOURCE_BLOB
    assert not subprocess.check_output(
        ["git", "status", "--porcelain=v1"], cwd=mathlib, text=True
    ).strip()
    assert sha256(source) == MATHLIB_SOURCE_SHA256
    source_lines = source.read_bytes().splitlines(keepends=True)
    assert hashlib.sha256(b"".join(source_lines[429:435])).hexdigest() == (
        MATHLIB_BODY_SHA256
    )
    source_text = source.read_text(encoding="utf-8")
    start = source_text.index("theorem Ideal.mem_iInf_smul_pow_eq_bot_iff")
    end = source_text.index("theorem Ideal.isIdempotentElem_iff_eq_bot_or_top_of_isLocalRing")
    terminal_route = without_comments(source_text[start:end])
    assert prohibited.search(terminal_route) is None
    for marker in (
        "Submodule.exists_mem_and_smul_eq_self_of_fg_of_le_smul",
        "Ideal.mem_iInf_smul_pow_eq_bot_iff",
        "isUnit_of_sub_one_mem_jacobson_bot",
        "(le_maximalIdeal h).trans (maximalIdeal_le_jacobson _)",
        "convert I.iInf_pow_smul_eq_bot_of_isLocalRing (M := R) h",
        "rw [smul_eq_mul, ← Ideal.one_eq_top, mul_one]",
    ):
        assert marker in terminal_route, marker

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim theorem completion" in validation
    assert "M0-W" in validation and "M0030-S-FOUNDATION" in validation
    for path in (
        proof_path,
        HERE / "check_proof.py",
        HERE / "check_proof.sh",
        HERE / "proof-receipt.json",
        HERE / "proof-validation.md",
        ROOT / ".stage1-worker-selftest.json",
    ):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0030 proof phase: exact pinned Krull root and proof route are kernel-closed")


if __name__ == "__main__":
    main()
