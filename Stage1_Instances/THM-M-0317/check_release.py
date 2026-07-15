#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0317-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0317"
ITEM = "S56-M-0317-RELEASE"
THEOREM = "THM-M-0317"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
EXPECTED_INPUTS = {
    "Statement.lean": "94c90b4b7a6dda1083b80b80907264b91e89cf5f2a6cb285e06a161be238dff2",
    "AnchorAudit.lean": "28dddd57894ba0be163dad8a8704e3c807c11d9474e773cdadbac00eb306f11d",
    "ObligationTree.lean": "bba7554df1b27f64cb8a69a0237cdd3b151cbec8b0d49fdfcb2f501b7bae2624",
    "Proof.lean": "da908a598cfd7e18c53fae440f4491b062d6ecd0605903b7fe924bee6a87b216",
    "Validation.lean": "ead54431497749917bc7d8d78798a3829c153461b72a289dc78e3ae0896bd427",
    "instance.json": "592cba93934fa28e3b10e6324087193146fe61f9df5a6f888ba90a03e1ea81d5",
    "task-dag.json": "ae08abf3c8883e09e808a173c5de148560b27df48f032b44b5cbf051c368b27f",
    "anchor-audit.json": "c6bf134e9ab189197b67330111f68f963fbd0d0e2e1de153bd4063f9069b6c39",
    "obligation-registry.json": "d67f99adec35a52a547b9ba1b49187613dcd27dfd2746754dc4a0539abbdbbde",
    "typed-graphs.json": "4d8c4f814cc065dc81a5bf90a357a57fc5d7ff3271350901acca64fcd19879a0",
    "validation-specs.json": "1782500c10182512d428735e5df4f2c48184776458ff2a99e9fdf33a1e113300",
    "proof-receipt.json": "b36ca8d96a61b198b6283ce02e21d656826c89ec3a5fbd62b5eb12be20309f02",
    "proof-blocker.json": "edc0c51dac45c1b5d91241f5f75446db07f521f2d4d9338ef910d1d12d617a81",
    "validation-spec.json": "aba447e77de8a95cff4c9a2d59eab98b3078cbb029687c5e2f77635f2a222ee0",
    "validation-receipt.json": "0e3e066e752396d4743e337cd2e2df4b3ad5a242d2539ee63f1da994eda9baf3",
    "check_validation.py": "9608a82a9d507fd1502feaa94dc80d7d312627378d1f6fb3ccc6c7bc1e559404",
    "source-statement-crosswalk.md": "b4f9a2dfe294ee41f230c9d4bd84fc17d58d9c080e9903da5a51206ff56f292a",
}
INVENTORY_IDS = [
    "M0317-ROOT", "M0317-S-DEFINITIONS", "M0317-S-DOMAINS",
    "M0317-S-BOUNDARY", "M0317-S-FOUNDATION", "M0317-N-NEIGHBORHOODS",
    "M0317-C-FINITE-COVER", "M0317-C-PARTITION", "M0317-C-FINITE-MAP",
    "M0317-L-BROUWER", "M0317-L-APPROX-FIXED", "M0317-L-COMPACT-LIMIT",
    "M0317-T-APPROX", "M0317-T-LIMIT", "M0317-T-ASSEMBLE",
    "M0317-X-SOURCE", "M0317-X-PROVENANCE",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
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


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    instance = load(HERE / "instance.json")
    graphs = load(HERE / "typed-graphs.json")
    registry = load(HERE / "obligation-registry.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 683
    assert target["lifecycle_mode"] == "planned"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0317-VALIDATION"
    )
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 683,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0317-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-0317-VALIDATION"]

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"

    assert decision["item_id"] == receipt["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["execution_rank"] == 683 and decision["intent"] == "release"
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["decision_support"] == receipt["support_state"] == (
        "provisional_worker_selftest"
    )
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0317-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"], validation["receipt_id"]
    ]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-B", str(HERE.relative_to(ROOT) / "check_release.py")]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 180 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert decision["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["depends_on"] == ["S56-M-0317-VALIDATION"]
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["verdict"] == "blocked"
    assert receipt["accepted_receipt_ids"] == decision["accepted_receipt_ids"] == []
    expected_bindings = {
        f"Stage1_Instances/{THEOREM}/{name}": expected
        for name, expected in (
            ("Statement.lean", EXPECTED_INPUTS["Statement.lean"]),
            ("Proof.lean", EXPECTED_INPUTS["Proof.lean"]),
            ("Validation.lean", EXPECTED_INPUTS["Validation.lean"]),
            ("instance.json", EXPECTED_INPUTS["instance.json"]),
            ("task-dag.json", EXPECTED_INPUTS["task-dag.json"]),
            ("obligation-registry.json", EXPECTED_INPUTS["obligation-registry.json"]),
            ("typed-graphs.json", EXPECTED_INPUTS["typed-graphs.json"]),
            ("proof-receipt.json", EXPECTED_INPUTS["proof-receipt.json"]),
            ("proof-blocker.json", EXPECTED_INPUTS["proof-blocker.json"]),
            ("validation-spec.json", EXPECTED_INPUTS["validation-spec.json"]),
            ("validation-receipt.json", EXPECTED_INPUTS["validation-receipt.json"]),
            ("source-statement-crosswalk.md", EXPECTED_INPUTS["source-statement-crosswalk.md"]),
            ("release-spec.json", "442815cd59ad35c0e883d2d3ba6a2aacf3bd2ced44be3a730917225a73fdc7f6"),
            ("release-decision.json", "cec8d435d53bd4d1b92b64d26b7be61b4f602b146656ef8fe612d3a9f8be7eeb"),
            ("release-validation.md", "0ea50a4e4c3a54c21e903a2d733a716e439fb182e22539f99672314ea3be07b5"),
            ("check_release.py", "informational:self-referential-validator-binding-checked-by-worker-diff"),
        )
    }
    assert set(receipt["input_bindings"]) == set(expected_bindings)
    for relative, expected in receipt["input_bindings"].items():
        if relative.endswith("/check_release.py"):
            continue
        assert sha256(ROOT / relative) == expected, f"receipt binding drifted: {relative}"
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations",
        )
    }

    result = decision["decision"]
    assert result["verdict"] == receipt["result"]["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == [
        "H1", "M4", "R4"
    ]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["next_failed_theorem_gate"]["gate_id"] == "proof.root_kernel_closure"
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert result["authoritative_remaining_root_cut_set"] == [
        "M0317-T-APPROX", "M0317-T-LIMIT"
    ]
    assert result["post_provisional_validation_mathematical_cut_set"] == [
        "M0317-T-APPROX"
    ]

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is False
    assert closure["theorem_complete"] is False
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["result"]["root_closed"] is proof["result"]["theorem_complete"] is False
    assert blocker["first_failed_gate"].startswith("M0317-T-APPROX")
    assert blocker["root_closed"] is blocker["theorem_complete"] is False
    validation_result = validation["result"]
    assert validation_result["root_closed"] is validation_result["root_kernel_closed"] is False
    assert validation_result["remaining_root_cut_set"] == ["M0317-T-APPROX"]
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False
    assert validation_result["hermetic_release_gate"] == "fail_closed"
    assert validation_result["independent_verification_gate"] == "fail_closed"

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "accepted_exact_root_kernel_closure", "approximation_package_body_present",
        "authoritative_graph_reconciled", "audit_z_accepted", "pinpoint_h0_review",
        "independent_r0_review", "accepted_foundation_profile",
        "complete_provenance_trust_and_tcb_closure", "immutable_clean_release_input",
        "hermetic_cold_offline_replay", "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier", "protected_ci_and_mutation_gates",
        "deterministic_release_bundle", "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    cut = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "S56-M-0317-VALIDATION", "M0317-T-APPROX", "M0317-X-SOURCE",
        "R0 structured", "empty-cache network-denied cold build",
        "two signed attestations", "minimal release verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in cut, fragment

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    actual = {
        line[3:] for line in git(
            "status", "--short", "--untracked-files=all", "--",
            str(HERE.relative_to(ROOT)), ".stage1-worker-selftest.json",
        ).splitlines()
    }
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H1, M4, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "This worker accepts no receipt", "`release_grade=false`",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("PASS S56-M-0317-RELEASE reconciliation")
    print("verdict=blocked lifecycle=planned accepted_root_vector=H1/M4/R4")
    print("audit_complete=false theorem_complete=false accepted_receipts=0")
    print("first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
    print("next_failed_theorem_gate=proof.root_kernel_closure:M0317-T-APPROX")


if __name__ == "__main__":
    main()
