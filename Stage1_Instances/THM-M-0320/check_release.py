#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0320-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


if not __debug__:
    raise SystemExit("release validation requires Python assertions")

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0320"
ITEM = "S56-M-0320-RELEASE"
THEOREM = "THM-M-0320"
BASE_REVISION = "7505614b75de56cf10bbd196a4aaa0ca2a117064"
BASE_TREE = "730e162a2133e4a077d764043b5e722c1f7feb39"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
DENOMINATOR_SHA256 = (
    "b513af2baba56c289271260eadeeaea0c1df46090f3728123c0395b955b0b974"
)
PROOF_RECEIPT_SHA256 = (
    "e9b7f89884744a08f12b8bcdf3d7a05ac2d1f0bf6e05f5a66f4fced8dd06968e"
)
VALIDATION_RECEIPT_SHA256 = (
    "307d5fff9f9945ee920fbc8e89f6a74a59ad7ec459fe9756e8249f6f792322bf"
)
INVENTORY_IDS = [
    "M0320-ROOT",
    "M0320-S-STATEMENT",
    "M0320-S-FOUNDATION",
    "M0320-T-COMPACT",
    "M0320-T-GRAPH",
    "M0320-C-CORE",
    "M0320-T-SUBTYPE",
    "M0320-T-ASSEMBLE",
    "M0320-X-SOURCE",
    "M0320-X-PROVENANCE",
]
FROZEN_OPEN_CUT = ["M0320-T-GRAPH", "M0320-C-CORE"]
PROVISIONAL_KERNEL_IDS = [
    "M0320-ROOT",
    "M0320-T-COMPACT",
    "M0320-T-GRAPH",
    "M0320-C-CORE",
    "M0320-T-ASSEMBLE",
]
EXPECTED_INPUTS = {
    "README.md": "5a63be21dddc121d2a773b13f449c76c0e53e04b6025717e7dd9cd0f02d86bbc",
    "instance.json": "8bc23a5d11b991f57015090215d049ad3d8dff5b55173777a6c09e1ccd7af789",
    "task-dag.json": "839f9714363fda9a8153c32efe0824008e9732d891b71897c52cf4bb45470746",
    "Statement.lean": "3faa541aa99857bcbebb808f0d49a077377d20ab5b73144bbb5eedd5e93f04df",
    "ObligationTree.lean": "88050f777a447ba3dd2f78dd9069bce14667567647197b6c5b24febbfddb84e2",
    "GraphBridgeProof.lean": "efbabf2c2418c4f068970871a5837071c742da274256d85e2081d5613c49e033",
    "BrouwerSource.lean": "164011f052a69a85b961cfaafccffe87f94ad99de916429850d5da320dbe65e9",
    "Proof.lean": "5c5545ee48cb84f046a112569b156f88637963e67965a244337db1ecb5c83c22",
    "Validation.lean": "e666cd52d7f2a20c23ee3eec47d7423126a23012555f622acb0a26e4658a92ba",
    "TrustAudit.lean": "6d3e0dfae9f31520416938e955cc87ee3c4820f1d45039204fb07eeb21247e6f",
    "anchor-audit.json": "d53cbbccadba992b4e292ca3b759d9cc9d28a1e044aea3dea5a29843adb1c736",
    "obligation-registry.json": "1d83900afadc0effc677f1f4ad40ad0da96b6a8fba25911ee7c5488759622c13",
    "typed-graphs.json": "5bda34edf918402375545fd36aff0d03843f5cb62b16fa6692993f7544ddedc1",
    "source-statement-crosswalk.md": "8edc3d26d7bca899a9b0464f8e00071eb7ef04b0f9f192d50a703e463dcd2d5e",
    "proof-receipt.json": PROOF_RECEIPT_SHA256,
    "validation-spec.json": "50483badd5261ca4923a9f7a2af0b87bad07efb1be56a4473856d60731889b02",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "fe04e1784c7677c82932521eddb5c2e7a98c1c100fd919f4dfb5af8a8a1f1ade",
    "validation-phase.md": "88443a47a38d906942929545832b3714b2c865c105f700179b64339323b3e155",
    "check_proof.sh": "1d72151118a17e0cf3c15bd0f768a855263640020ae514bb4448e5aa3ff50556",
}
EXPECTED_AUTHORITY = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "e3c2c7d8f509cfa6f7494bd5390f5134e428adaaa122a9467d342bbea71d3281",
    "Docs/Stage1_Blueprint_rev-5.6.md": "72f71ee0c8570e5e9b60b2af2cf28095cbe35b51ab38ba7ca41309d69c57d06a",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_RELEASE = {
    "release-spec.json": "2cf4f67f936e4a9723cc20c0b87bc079265bec3de3d6f3c3f7c206bfc4613c56",
    "release-decision.json": "adecc73bab583234c334256af93dbad6e99c3e4aca9ce225bfa05e82d88d0271",
    "release-validation.md": "72bc0d59165429c53df4ae98313c86d72cecbeec506db40db622fb52dc5a41fa",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = (
    "PASS release reconciliation: authority, target inputs, and prior receipts are hash-bound",
    "PASS exact verdict: provisional kernel root observed but no accepted closure is inferred",
    "BLOCKED dependency.S56-M-0320-VALIDATION.master_acceptance",
    "BLOCKED AUDIT-Z and THEOREM-Z; accepted root remains H1/M4/R4",
    "BLOCKED immutable cold release, distinct verification, and deterministic bundle gates",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
)
VALIDATION_PROBE_COMMAND = (
    "timeout 30 /usr/bin/bwrap --ro-bind / / --dev /dev --proc /proc "
    "--tmpfs /tmp --unshare-net --die-with-parent --setenv LANG C.UTF-8 "
    "--setenv LC_ALL C.UTF-8 --setenv TZ UTC --setenv LEAN_NUM_THREADS 1 "
    "--setenv STAGE1_SKIP_RECEIPT_CHECK 1 --setenv STAGE1_OUTER_NETWORK_ISOLATED 1 "
    "/usr/bin/python3 -I -B Stage1_Instances/THM-M-0320/check_validation.py --probe"
)
PROOF_COMMAND = "timeout 300 bash Stage1_Instances/THM-M-0320/check_proof.sh"
JSON_COMMAND = (
    "for f in Stage1_Instances/THM-M-0320/release-spec.json "
    "Stage1_Instances/THM-M-0320/release-decision.json "
    "Stage1_Instances/THM-M-0320/release-receipt.json .stage1-worker-selftest.json; "
    "do python3 -m json.tool $f >/dev/null || exit; done"
)


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


def run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=60, check=False,
    )


def git(*args: str) -> str:
    result = run(["git", *args])
    assert result.returncode == 0, result.stdout
    return result.stdout.strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, name
    for name, expected in EXPECTED_AUTHORITY.items():
        assert sha256(ROOT / name) == expected, name
    for name, expected in EXPECTED_RELEASE.items():
        assert sha256(HERE / name) == expected, name

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 686 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item["state"] == "[ ]"
    assert release_item["depends_on"] == ["S56-M-0320-VALIDATION"]
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0320-VALIDATION"
    )
    assert validation_item["state"] == "[_]"

    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert decision["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["phase"] == receipt["phase"] == "release"
    assert decision["intent"] == receipt["intent"] == "release"
    assert decision["depends_on"] == receipt["depends_on"] == ["S56-M-0320-VALIDATION"]
    assert decision["execution_rank"] == receipt["execution_rank"] == 686

    assert instance["lifecycle"] == tasks["lifecycle"] == "planned"
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == tasks["accepted_states"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert next(row for row in tasks["tasks"] if row["id"].endswith("-VALIDATION"))["state"] == "open"
    assert next(row for row in tasks["tasks"] if row["id"].endswith("-RELEASE"))["state"] == "open"

    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    boundary = graphs["closure_boundary"]
    assert boundary["remaining_root_cut_set"] == FROZEN_OPEN_CUT
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False

    assert proof["receipt_id"] == decision["provisional_receipt_ids_inspected"][0]
    assert proof["accepted"] is False and proof["accepted_receipt_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["theorem_complete"] is False
    assert "M0320-T-SUBTYPE" in proof["kernel_inhabited_obligation_ids_observed"]
    assert validation["receipt_id"] == decision["provisional_receipt_ids_inspected"][1]
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation.get("accepted_receipt_ids", []) == []
    assert validation["result"]["provisionally_observed_kernel_inhabited_obligation_ids"] == PROVISIONAL_KERNEL_IDS
    assert validation["result"]["unreconciled_architecture_obligation_ids"] == ["M0320-T-SUBTYPE"]
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == "dependency.S56-M-0320-PROOF.master_acceptance"

    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["decision_id"] == receipt["decision_id"] == receipt["receipt_id"]
    assert "20260715T144500+0800" in decision["decision_id"]
    assert decision["decided_at"] == receipt["validated_at"] == "2026-07-15T14:45:00+08:00"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector"]["accepted_before"] == ROOT_VECTOR
    assert decision["root_vector"]["accepted_after"] == ROOT_VECTOR
    assert decision["canonical_target"] == receipt["canonical_target"]
    assert decision["canonical_target"]["source_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert decision["canonical_target"]["accepted_elaborated_expression_sha256"] is None
    assert decision["canonical_target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert decision["accepted_receipt_ids"] == decision["accepted_closed_obligation_ids"] == []
    assert decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
        "release_accepted": False,
    }
    assert decision["authoritative_remaining_root_cut_set"] == FROZEN_OPEN_CUT
    assert decision["unreconciled_architecture_obligation_ids"] == ["M0320-T-SUBTYPE"]
    assert decision["first_failed_gate"]["node_gate"] == (
        "dependency.S56-M-0320-VALIDATION.master_acceptance"
    )
    assert receipt["accepted"] is receipt["master_accepted"] is False
    assert receipt["release_grade"] is receipt["release_accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert receipt["dependency"] == decision["dependency"]
    assert receipt["dependency"] == {
        "item_id": "S56-M-0320-VALIDATION",
        "scheduler_projection": "[_]",
        "receipt_id": validation["receipt_id"],
        "receipt_sha256": VALIDATION_RECEIPT_SHA256,
        "support_state": "provisional_worker_selftest",
        "accepted": False,
        "release_grade": False,
        "master_accepted": False,
        "verdict": "blocked",
    }
    assert receipt["decision_sha256"] == sha256(HERE / "release-decision.json")
    assert receipt["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["public_projection_sha256"] == sha256(HERE / "release-validation.md")
    assert receipt["checker_sha256"] == sha256(HERE / "check_release.py")
    assert receipt["accepted_receipt_ids"] == receipt["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["root_vector_before"] == ROOT_VECTOR
    assert receipt["result"]["root_vector_after"] == ROOT_VECTOR
    assert receipt["result"]["accepted_receipt_ids"] == []
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["authoritative_remaining_root_cut_set"] == FROZEN_OPEN_CUT
    assert receipt["result"]["unreconciled_architecture_obligation_ids"] == ["M0320-T-SUBTYPE"]
    assert receipt["result"]["first_failed_gate"] == (
        "dependency.S56-M-0320-VALIDATION.master_acceptance"
    )
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    expected_stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["execution"]["checker_stdout_sha256"] == hashlib.sha256(
        expected_stdout.encode()
    ).hexdigest()
    assert receipt["execution"]["checker_stdout_bytes"] == len(expected_stdout.encode())
    assert receipt["known_failures"] == decision["known_failures"] == packet["known_failures"]

    for path, expected in receipt["input_bindings"].items():
        assert expected == sha256(ROOT / path), path
    expected_binding_paths = {
        *(f"Stage1_Instances/{THEOREM}/{name}" for name in EXPECTED_INPUTS),
        *EXPECTED_AUTHORITY,
    }
    assert set(receipt["input_bindings"]) == expected_binding_paths

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["network_policy"] == "denied_not_required"
    assert spec["expected_exit"] == 0 and spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == receipt["proposed_state"] == decision["proposed_state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert "verdict is blocked" in packet["output_summary"]
    assert "audit_complete=false" in packet["output_summary"]
    assert "theorem_complete=false" in packet["output_summary"]
    assert set(packet["changed_paths"]) == set(receipt["repository_state"]["changed_paths"]) == CHANGED_PATHS
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    command_records = receipt["commands_and_exit_codes"]
    assert any(
        row["command"] == VALIDATION_PROBE_COMMAND and row["exit_code"] == 1
        for row in command_records
    )
    proof_records = [row for row in command_records if row["command"] == PROOF_COMMAND]
    assert [(row["attempt"], row["exit_code"]) for row in proof_records] == [(1, 1), (2, 124)]
    assert any(
        row["command"] == JSON_COMMAND and row["exit_code"] == 0
        for row in command_records
    )
    assert packet["commands"].count(PROOF_COMMAND) == 2
    assert VALIDATION_PROBE_COMMAND in packet["commands"]
    assert JSON_COMMAND in packet["commands"]

    actual = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
    }
    actual.discard("Formalizations/Lean/.lake")
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    assert (ROOT / "Formalizations/Lean/.lake").is_symlink()

    proof_source = (HERE / "Proof.lean").read_text(encoding="utf-8")
    assert re.search(
        r"theorem\s+kakutaniFixedPoint\s*:\s*KakutaniFixedPointTarget\s*:=",
        proof_source,
    )
    assert "root_of_closedGraph_packages closedGraphKakutaniCore" in proof_source
    assert "upperHemicontinuityClosedGraphBridge" in proof_source
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES), flush=True)


if __name__ == "__main__":
    main()
