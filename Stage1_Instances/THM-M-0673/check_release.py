#!/usr/bin/env python3
"""Fail-closed current-snapshot check for S56-M-0673-RELEASE."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0673-RELEASE"
THEOREM = "THM-M-0673"
BASE_REVISION = "88a5a5c6fe6bac0d813a74ca20fa553eaf2a6d68"
BASE_TREE = "a0a75048a918a3bf566c3dbcf6b4352c3b2ee8e4"
TARGET_EXPRESSION = "3b541698da0e2b40d0cef5ea0f03ebd62538d330293e4e393ce053e000906cba"
DENOMINATOR = "4266ee40d8be778685c48d8781aab55dd6d57301e7d9ded13523ea4353c58fe6"
REGISTRY_SEMANTIC = "aefa3236248ea7500e3dd48e01e953f978f8425c78ac11103364ce9cabce3e77"
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
GRAPH_CUT = [
    "M0673-A-BOUNDED",
    "M0673-S-FOUNDATION",
    "M0673-X-SOURCE",
    "M0673-X-PROVENANCE",
    "M0673-X-TRUST",
    "M0673-X-READABLE",
    "M0673-X-WORKFLOW",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
INPUT_HASHES = {
    "instance.json": "c24eb53d67563203d997de2a068bda05cbef1aa56ab76826c6e93455b4798029",
    "task-dag.json": "d8b945e35ab6f159a9833aef12417ab66dcf4ccb7e9e284360381c6196ce27a7",
    "statement.json": "81468c229e682d4a3490c4275caa5dcbbc55b598a48d5e93bab1ae9b2016170e",
    "Statement.lean": "131cab45507a3d3c7249d02f52f8cfbaf9d7b1c004a542e24f1bdb36be9ca424",
    "obligation-registry.json": "2c5af493b744470bfcf09feb9fb4c13bbdff20ed434799b0d2c34e6db8fbfbb0",
    "typed-graphs.json": "7bd03ea0943661d43a4c02c0b711998f50a786bbb744412ba7cc4d557ce581fb",
    "Proof.lean": "cacb2a7f66bdeca3823b154e31d6a891d89a1751e78cf4cb73d20ef5b61a28fa",
    "proof-receipt.json": "b9e7a86f93d0ebf46860fb20207e480463639b9202b81ece262a875d5ea51f62",
    "Validation.lean": "faa7e299b8a90bef6fe554a3b15659c944bcfedd47e12f90d9fe42725e9122a3",
    "validation-spec.json": "a9ed7c9ddc61f9fb00ba0cd5497d7b4c49d85fc7c1511583a0c73d1a835974e8",
    "validation-receipt.json": "2c65d7746e51d9e9a8e44ed6565895110d6fc78441e50c6c2b59b848a9b36743",
}
AUTHORITY_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "9562a9b560c2175fd8a67556e8efbc62f4afaaf5a1ab30c0157399d54e2b6142",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "2c886a07ec06e5a70e9e7924a8543ef0226e19615f851c2ad00f51b1f012c2a6",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
SUMMARY_LINES = [
    "PASS release inputs: current base, target authority, canonical target, registry, graph, and provisional receipts agree",
    "PASS provisional kernel evidence: current trust-zero Lean replay is recorded without promoting the accepted root",
    "BLOCKED dependency: S56-M-0673-VALIDATION is provisional, blocked, unaccepted, and non-release-grade",
    "BLOCKED terminal gates: AUDIT-Z=false and THEOREM-Z=false; accepted root remains H1/M3/R4 and open",
    "BLOCKED release assurance: clean cold offline replay, H0/R0, complete trust/supply chain, independent verifier, deterministic bundle, and master acceptance are absent",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def git(*args: str) -> str:
    return subprocess.check_output(
        ["/usr/bin/git", *args], cwd=ROOT, text=True
    ).strip()


def actual_changed_paths() -> set[str]:
    status = subprocess.check_output(
        ["/usr/bin/git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    )
    return {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main(worker_packet: Path) -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    local_tasks = load(HERE / "task-dag.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(worker_packet)

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 717
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 717,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0673-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0673-VALIDATION"
    )
    assert predecessor["state"] == "[_]"
    assert local_tasks["accepted_states"] == []
    assert next(row for row in local_tasks["tasks"] if row["id"] == ITEM)["state"] == "open"

    for name, expected in INPUT_HASHES.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in AUTHORITY_HASHES.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    assert decision["reconciled_inputs"] == INPUT_HASHES
    assert decision["authority_inputs"] == AUTHORITY_HASHES

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == TARGET_EXPRESSION
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR
    assert registry["registry_sha256"] == graphs["registry_sha256"] == REGISTRY_SEMANTIC
    assert decision["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_0673.LosSentenceTarget",
        "expression_sha256": TARGET_EXPRESSION,
        "registry_denominator_sha256": DENOMINATOR,
        "registry_semantic_sha256": REGISTRY_SEMANTIC,
    }

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    boundary = graphs["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == []
    assert boundary["root_closed"] is False and boundary["root_machine_debt"] == "M3"
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["remaining_root_cut_set"] == GRAPH_CUT

    assert validation["receipt_id"] == decision["dependency"]["receipt_id"]
    assert sha256(HERE / "validation-receipt.json") == decision["dependency"]["receipt_sha256"]
    assert validation["item_id"] == "S56-M-0673-VALIDATION"
    assert validation["verdict"] == "blocked" and validation["accepted"] is False
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["release_grade"] is False
    assert validation["accepted_receipt_ids"] == []
    assert validation["first_failed_gate"] == "dependency.S56-M-0673-PROOF.master_acceptance"
    assert validation["result"]["root_kernel_inhabitant_observed"] is True
    assert validation["result"]["accepted_root_closed"] is False
    assert proof["result"]["root_kernel_inhabitant_observed"] is True
    assert proof["accepted"] is False and proof["accepted_receipt_ids"] == []

    assert decision["item_id"] == receipt["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert decision["root_vector"]["accepted_before"] == ["H1", "M3", "R4"]
    assert decision["root_vector"]["accepted_after"] == ["H1", "M3", "R4"]
    assert decision["authoritative_graph_cut"] == GRAPH_CUT
    terminal = decision["terminal_decisions"]
    assert terminal == receipt["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }
    assert decision["first_failed_gate"]["gate_id"] == (
        "dependency.S56-M-0673-VALIDATION.master_acceptance"
    )
    assert receipt["first_failed_gate"] == decision["first_failed_gate"]["gate_id"]
    assert receipt["first_failed_intrinsic_release_gate"] == "hermetic.immutable_clean_input"
    assert receipt["authoritative_graph_cut"] == GRAPH_CUT
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_receipt"] is False
    assert receipt["result"]["accepted_state_changed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False

    required_fragments = (
        "master acceptance of S56-M-0673-VALIDATION",
        "M0673-S-FOUNDATION",
        "M0673-X-SOURCE",
        "M0673-X-PROVENANCE",
        "M0673-X-TRUST",
        "M0673-X-READABLE",
        "M0673-X-WORKFLOW",
        "empty-cache cold network-denied build",
        "independently implemented minimal verifier",
        "deterministic bundle",
    )
    cut = "\n".join(decision["remaining_root_cut_set"])
    for fragment in required_fragments:
        assert fragment in cut, f"release cut omits {fragment!r}"
    for key in (
        "accepted_foundation_profile",
        "human_source_acceptance",
        "readability_acceptance",
        "current_snapshot_obligation_recipe_replay",
        "hermetic_release_reproduction",
        "supply_chain_closure",
        "independent_release_verification",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key].startswith("missing"), key

    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B",
        f"Stage1_Instances/{THEOREM}/check_release.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert receipt["artifact_hashes"] == {
        "release-spec.json": sha256(HERE / "release-spec.json"),
        "release-decision.json": sha256(HERE / "release-decision.json"),
        "release-validation.md": sha256(HERE / "release-validation.md"),
    }
    assert receipt["dependency_receipt"] == {
        "receipt_id": validation["receipt_id"],
        "sha256": sha256(HERE / "validation-receipt.json"),
        "accepted": False,
        "release_grade": False,
        "verdict": "blocked",
    }

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == SUMMARY_LINES
    assert packet["commands"]
    actual = actual_changed_paths()
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == actual == CHANGED_PATHS
    for relative in actual:
        assert_text_hygiene(ROOT / relative)

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path, required=True)
    args = parser.parse_args()
    main((ROOT / args.worker_packet).resolve())
