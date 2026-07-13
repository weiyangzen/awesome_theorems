#!/usr/bin/env python3
"""Fail-closed source, pin, graph, and receipt checks for S56-M-0912-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0912-PROOF"
THEOREM = "THM-M-0912"
BASE_REVISION = "5931467f7eefac7a6e57777cc3082e4a2edc03d4"
BASE_TREE = "45a10c953e5dc79c1eb9ae7d755ee84866717775"
EXPRESSION_SHA256 = "b322549a05e57fbf466b60eb8ff89f4a08c6ee3b68ea5bf3ff3bf86d99521776"
DENOMINATOR_SHA256 = "c66f1840e6d1bcc7b0a64f7ecdc24ee2f13adc10098ca8467cd238c649f7432b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
BASIC_SOURCE = Path("Mathlib/Data/Nat/Choose/Basic.lean")
BASIC_BLOB = "15a5c95dae82b6fc0ae14eebe85215f89853f7ee"
BASIC_SHA256 = "b3c40f47d39427428d70518b48adaaf16d3622698b32406fa7745749f1387170"
BASIC_OLEAN_SHA256 = "057f7b9cc9a9d24c4d1e2d7fcdec76cf6909fd0ee0439bbe59c25a823efcbf10"
PROOF_IDS = [
    "M0912-ROOT",
    "M0912-T-ROOT-COMPOSE",
    "M0912-N-POSITIVE-ROW",
    "M0912-T-PREDECESSOR-COMPOSE",
    "M0912-L-CHOOSE-SUCC-RIGHT",
    "M0912-L-POSITIVE-COLUMN-REINDEX",
    "M0912-N-SUMMAND-ORDER",
]
PREDECESSOR_INTERFACE_IDS = [
    "M0912-S-INTERFACE",
    "M0912-S-BOUNDARY",
    "M0912-S-TRANSPORTS",
]
OPEN_MACHINE_IDS = [
    "M0912-S-FOUNDATION",
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
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


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

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1454,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-0912-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import Statement",
        "import ObligationTree",
        "theorem positiveColumnReindex_proof : PositiveColumnReindex := by",
        "exact Nat.exists_eq_add_of_le' hn",
        "theorem chooseSuccRight_proof : ChooseSuccRightAnchor := by",
        "exact Nat.choose_succ_right m k hm",
        "theorem predecessorRecurrence_from_frozen_children :",
        "predecessorRecurrence_of_chooseSuccRight_and_reindex",
        "theorem predecessorRecurrence_pinned : PredecessorRecurrenceAnchor := by",
        "exact Nat.choose_eq_choose_pred_add hm hn",
        "root_of_bridges_and_predecessorAnchor positiveRowBridge_checked",
        "theorem pascalIdentityTarget_proof : PascalIdentityTarget :=",
        "theorem pascalIdentityTarget_via_frozen_children : PascalIdentityTarget :=",
        "assert_no_sorry pascalIdentityTarget_proof",
        "#print axioms pascalIdentityTarget_proof",
    ):
        assert marker in proof, marker

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0912-ROOT"
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    required_machine = registry["frozen_denominators"]["required_machine"]
    assert set(required_machine) == set(
        PROOF_IDS + PREDECESSOR_INTERFACE_IDS + OPEN_MACHINE_IDS
    )

    proof_edges = graphs["graphs"]["proof"]["edges"]
    children: dict[str, list[str]] = {}
    for edge in proof_edges:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = ["M0912-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(children.get(obligation, []))
    assert reachable == set(PROOF_IDS)

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["provisionally_closed_proof_obligation_ids"] == PROOF_IDS
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
    assert receipt["result"]["axioms"] == ["propext"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["recipe"]["output_sha256"] == (
        "c992e4e246af412dc7a18bf35e90239c8c91607c7905916109f87a42e27f2726"
    )
    assert receipt["predecessor_replay_observations"] == [
        {
            "command": "python3 -B Stage1_Instances/THM-M-0912/check_intake.py",
            "exit_code": 1,
            "result": "historical intake checker hardcodes its intake-plus-statement file set and rejects already-integrated anchor, obligation-tree, and proof files",
        },
        {
            "command": "python3 -B Stage1_Instances/THM-M-0912/check_statement.py",
            "exit_code": 1,
            "result": "historical statement checker expects authoritative statement state [ ], while the current base records the predecessor worker state [_]",
        },
        {
            "command": "python3 -B Stage1_Instances/THM-M-0912/check_anchor_audit.py",
            "exit_code": 1,
            "result": "historical anchor checker requires its original base revision rather than the current proof worker base",
        },
    ]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""
    source = mathlib / BASIC_SOURCE
    olean = mathlib / ".lake/build/lib/lean" / BASIC_SOURCE.with_suffix(".olean")
    assert git_output("rev-parse", f"HEAD:{BASIC_SOURCE}", cwd=mathlib) == BASIC_BLOB
    assert sha256(source) == BASIC_SHA256 and sha256(olean) == BASIC_OLEAN_SHA256
    basic_text = source.read_text(encoding="utf-8")
    for marker in (
        "def choose :",
        "theorem choose_succ_right",
        "theorem choose_eq_choose_pred_add",
        "Nat.exists_eq_add_of_le'",
        "Nat.add_one_sub_one",
    ):
        assert marker in basic_text
    assert prohibited.search(without_comments(basic_text)) is None

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git_output("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim theorem completion" in validation
    assert "M0-W" in validation and "M0912-S-FOUNDATION" in validation
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

    print("PASS THM-M-0912 proof phase: exact frozen root and every proof-graph child close")


if __name__ == "__main__":
    main()
