#!/usr/bin/env python3
"""Fail-closed source, pin, graph, receipt, and packet checks for M0914 proof."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0914-PROOF"
THEOREM = "THM-M-0914"
BASE_REVISION = "9f2a15ae074a155a719c4b743df26f1e993312da"
BASE_TREE = "f86e49cf644956699ddb4e82c561101847086c5f"
EXPRESSION_SHA256 = "faef4a7f73219dc5b6178b8788978e21377c593ad84b845b4d49547218e6ae3b"
DENOMINATOR_SHA256 = "5a421bbbcc8afad0a1a35bb461a33c7712f8e2abd081706a36b4ccb4ce59f3ce"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PIGEONHOLE_SOURCE = Path("Mathlib/Data/Fintype/Pigeonhole.lean")
PIGEONHOLE_BLOB = "19ebeb40518e099dc572d5b3b627ce2f62c0745a"
PIGEONHOLE_SHA256 = "fa4604d2b1ae480f910e6000ca8814a632299082b48a14f598314303b68cc582"
PIGEONHOLE_OLEAN_SHA256 = "0d557d94dc54047f6c54aa3c94785d859a4f3738e6bf98d3b42257ee6bb36931"
PIGEONHOLE_BODY_SHA256 = "d84d5bc0b4c083cfdfb02001f2def9855531a4c250dbc855132fd9064669eb2f"
CARD_SOURCE = Path("Mathlib/Data/Finset/Card.lean")
CARD_BLOB = "d1c2c1e36ea9028aa27c4724c2c9d76afd9af35b"
CARD_SHA256 = "5566f2afb81cb80e2aa7349d8b04214f3667d84e4b81d965f85714ec5a8f0e27"
CARD_OLEAN_SHA256 = "b8504bc80578476685d30420a182799a2e385bde6c35299494034e828767023d"
CARD_BOUND_BODY_SHA256 = "11c401a65812e6d18a01c623ba3ce05b5ac7a4e707a007cfee8a013613e84b1e"
FINSET_BODY_SHA256 = "c88e185f9515ef671655ee204e5526c49887f3a23a56b99a0d849074cdcb9707"
PROOF_IDS = [
    "M0914-ROOT",
    "M0914-T-ROOT-COMPOSE",
    "M0914-N-FIN-CARD-INEQUALITY",
    "M0914-A-FINTYPE-WRAPPER",
    "M0914-N-FIN-CARD-IDENTITY",
    "M0914-N-SUCCESSOR-LT",
    "M0914-L-FINSET-COLLISION",
    "M0914-N-UNIV-MAPS-TO",
    "M0914-L-CARD-INJON-BOUND",
    "M0914-L-NO-COLLISION-INJON",
]
INTERFACE_IDS = [
    "M0914-S-INTERFACE",
    "M0914-S-BOUNDARY",
    "M0914-S-BOX-TRANSPORT",
]
OPEN_MACHINE_IDS = ["M0914-S-FOUNDATION"]
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
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def body_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1 : last])).hexdigest()


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

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1456,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-0914-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import Statement",
        "import ObligationTree",
        "theorem cardInjOnBound_pinned : FinsetCardInjOnBound := by",
        "exact Finset.card_le_card_of_injOn f hMaps hInj",
        "theorem finsetCollision_pinned : FinsetCollisionPackage := by",
        "exact Finset.exists_ne_map_eq_of_card_lt_of_maps_to hcard hMaps",
        "finsetCollisionPackage_of_cardBound_and_noCollision",
        "theorem fintypeWrapper_pinned : FintypeCollisionPackage := by",
        "exact Fintype.exists_ne_map_eq_of_card_lt f hcard",
        "fintypePackage_of_finsetPackage finsetCollision_from_frozen_children",
        "root_of_fintypePackage fintypeWrapper_pinned cardFinPackage",
        "theorem pigeonholeTarget_proof : PigeonholeTarget :=",
        "theorem pigeonholeTarget_via_frozen_children : PigeonholeTarget :=",
        "assert_no_sorry pigeonholeTarget_proof",
        "#print axioms pigeonholeTarget_proof",
    ):
        assert marker in proof, marker

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0914-ROOT"
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    required_machine = registry["frozen_denominators"]["required_machine"]
    assert set(required_machine) == set(PROOF_IDS + INTERFACE_IDS + OPEN_MACHINE_IDS)

    proof_edges = graphs["graphs"]["proof"]["edges"]
    children: dict[str, list[str]] = {}
    for edge in proof_edges:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: list[str] = []
    pending = ["M0914-ROOT"]
    while pending:
        obligation = pending.pop(0)
        if obligation in reachable:
            continue
        reachable.append(obligation)
        pending.extend(children.get(obligation, []))
    assert reachable == PROOF_IDS

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["provisionally_closed_proof_obligation_ids"] == PROOF_IDS
    assert receipt["predecessor_interface_ids_not_reclaimed"] == INTERFACE_IDS
    assert receipt["required_machine_open_ids"] == OPEN_MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    fingerprints = {
        row["obligation_id"]: row["statement_fingerprint"]
        for row in registry["obligations"]
        if row["obligation_id"] in PROOF_IDS
    }
    assert receipt["statement_fingerprints"] == fingerprints
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename)
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    pigeonhole = mathlib / PIGEONHOLE_SOURCE
    card = mathlib / CARD_SOURCE
    assert git("rev-parse", f"HEAD:{PIGEONHOLE_SOURCE}", cwd=mathlib) == PIGEONHOLE_BLOB
    assert git("rev-parse", f"HEAD:{CARD_SOURCE}", cwd=mathlib) == CARD_BLOB
    assert sha256(pigeonhole) == PIGEONHOLE_SHA256
    assert sha256(card) == CARD_SHA256
    assert sha256(mathlib / ".lake/build/lib/lean" / PIGEONHOLE_SOURCE.with_suffix(".olean")) == PIGEONHOLE_OLEAN_SHA256
    assert sha256(mathlib / ".lake/build/lib/lean" / CARD_SOURCE.with_suffix(".olean")) == CARD_OLEAN_SHA256
    assert body_sha256(pigeonhole, 46, 49) == PIGEONHOLE_BODY_SHA256
    assert body_sha256(card, 413, 418) == CARD_BOUND_BODY_SHA256
    assert body_sha256(card, 442, 449) == FINSET_BODY_SHA256

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"] and all(
        isinstance(command["argv"], list)
        and isinstance(command["exit_code"], int)
        and command["result"]
        for command in packet["commands"]
    )
    assert "Pending" not in packet["output_summary"]
    assert "not accepted state or theorem completion" in packet["output_summary"]

    actual_changes = {
        line[3:]
        for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS
    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim theorem completion" in validation
    assert "M0-W" in validation and "M0914-S-FOUNDATION" in validation
    for path in [ROOT / name for name in CHANGED_PATHS]:
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0914 proof phase: exact frozen root and every proof-graph child close")


if __name__ == "__main__":
    main()
