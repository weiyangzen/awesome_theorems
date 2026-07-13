#!/usr/bin/env python3
"""Fail-closed current-snapshot reconciliation for S56-M-1138-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1138"
ITEM = "S56-M-1138-RELEASE"
THEOREM = "THM-M-1138"
BASE_REVISION = "fcfd52dc69db3bf455310be55903278133a15a10"
BASE_TREE = "3580154b2d6b61f9bfee3079ce78939155de16ca"
VALIDATION_BASE_REVISION = "499a718cc7926abaf61e9721fe0d7485059403e6"
EXPRESSION_SHA256 = "7ae115564e67b7065344d9b323240a2694c3f1f1f01640d1b542dcc2152f4f5c"
DENOMINATOR_SHA256 = "a2093825a633069dc09fc9bf1597396052d7f9272bb33f44ace551aa7ba1ca49"
VALIDATION_RECEIPT_SHA256 = "f90c5b7cee68856ec3c2e09f4b190ccd0c457728c850609a889df456184a7ab5"
EXPECTED_INPUTS = {
    "Statement.lean": "a6a2c5d7cc38249b3d96a3f8037a68175db5d62eecec2790865086dce2747c5a",
    "ObligationTree.lean": "433c6beaaa9d7c5a74c8afe1f5337b38d4015ec3964988a2dea9b7dae938640d",
    "Proof.lean": "52105d067464dff747110a6fc147da9392adeddce2ca6fe61ddf70f37feef8f2",
    "statement.json": "4cc2e9671d8accc16d8453d2a72633e525b35932642916f47fd180db9d8c6032",
    "anchor-audit.json": "6fe67212ac3f2785d325aa1d33e6ec6c7ecdef613ad331c794330ee3063374b1",
    "obligation-registry.json": "a3fc025b941f6cfc039562e443bd41f5548bf1233e4f2181b3396b015f9a657e",
    "typed-graphs.json": "b66bd5f13ebfcc7b47c853872c615f235ca2cb5235fc641fa0ad778beb65dcdc",
    "proof-receipt.json": "88d6e0626a192c417c62f6970d31afa75a821b9786517672785bca233af1c3ff",
    "validation-spec.json": "a2ff017ba24f30683557b71a010a62274c1bae0a8e5cf400d96aa13582ffb278",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "137600294ac439439d734e5df712520b6018e0c50ec009fb608dd6a6bd83a352",
    "check_proof.sh": "079e4fc3b2a9a8f31d369dacbfcdd1e3341ddb55a02a3b5fd4ba62d197ca1365",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_EXECUTABLES = {
    "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "python3": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "bash": "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd",
    "bwrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "48a2aac3fab40f4b042c83cf6c525c45854392e891a44fb8992a3ad7ca215b88",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "c6c22454ebcfdd47a95a5a3e58e15ede0701fee836353d8723b5e720e029682c",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
WITHHELD_ROUTE_IDS = {
    "M1138-C-CLOSURE-MAXIMIZER",
    "M1138-B-MAXIMIZER-LOCATION",
    "M1138-L-INTERIOR-LOCAL",
    "M1138-L-CONNECTED-PROPAGATION",
    "M1138-L-CONTINUITY-EXTENSION",
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
    "PASS release inputs: current target, DAG dependency, receipts, graph, and hashes agree",
    "PASS current Lean observation: exact terminal package and root are sorry-free with expected axioms",
    "PASS fail-closed state: lifecycle planned; accepted root H1/M3/R3; accepted receipts 0",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional, unaccepted, and stale",
    "BLOCKED route, audit, immutable input, cold/offline, trust, and independent release gates",
    "verdict=blocked audit_complete=false theorem_complete=false",
)


if not __debug__:
    raise RuntimeError("release reconciliation requires Python assertions")


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key {key!r} in {path}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, expected_exit: int = 0) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=600,
        check=False,
    )
    assert result.returncode == expected_exit, (argv, result.returncode, result.stdout)
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).rstrip()


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, (declaration, output)
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 343
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1138-VALIDATION"
    )
    assert release_item["phase"] == "release" and release_item["layer"] == 6
    assert release_item["state"] == "[ ]" and release_item["attempts"] == 0
    assert release_item["depends_on"] == ["S56-M-1138-VALIDATION"]
    assert release_item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"input drifted: {name}"
    for name, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    lean_root = ROOT / "Formalizations" / "Lean"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(lean_root / name) == expected, f"tool input drifted: {name}"
    executables = {
        "lean": Path(run(["bash", "-lc", "cd Formalizations/Lean && lake env which lean"]).strip()),
        "python3": Path("/usr/bin/python3"),
        "bash": Path("/usr/bin/bash"),
        "bwrap": Path("/usr/bin/bwrap"),
    }
    for name, path in executables.items():
        assert path.is_file() and sha256(path) == EXPECTED_EXECUTABLES[name], name

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["accepted_receipt_ids"] == []
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-1138-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_base_revision"] == validation["base_revision"]
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is dependency["current_snapshot_replayable"] is False
    assert validation["base_revision"] == VALIDATION_BASE_REVISION

    assert statement["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "closed_obligations": ["M1138-S-DEFINITIONS", "M1138-T-ROOT-TRANSPORT"],
        "root_closed": False,
        "theorem_complete": False,
        "remaining_root_cut_set": ["M1138-T-BOUNDARY-MAX"],
        "root_machine_debt": "M3",
    }
    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is proof["content_addressed"] is False
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert set(proof["root_evidence"]["withheld_frozen_route_ids"]) == WITHHELD_ROUTE_IDS
    assert proof["root_evidence"]["foundation_credit_withheld"] is True
    assert validation["verdict"] == "blocked"
    assert validation["result"]["accepted_root_closed"] is False
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["result"]["accepted_closed_obligation_ids"] == []

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 600 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["depends_on"] == ["S56-M-1138-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["review_due"] and receipt["supersession_state"]
    assert receipt["revocation_state"] == "not_revoked" and receipt["incident_path"]
    assert receipt["invalidation_inputs"]
    assert receipt["validation_started_at"] <= receipt["validated_at"]
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["master_accepted"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["verdict"] == "blocked"
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["changed_paths"] == decision["changed_paths"]
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["dependency_receipt"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert receipt["dependency_receipt"]["current_snapshot_replayable"] is False
    assert receipt["input_bindings"][
        f"Stage1_Instances/{THEOREM}/release-spec.json"
    ] == sha256(HERE / "release-spec.json")
    for relative in (
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/check_release.py",
        f"Stage1_Instances/{THEOREM}/release-decision.json",
        f"Stage1_Instances/{THEOREM}/release-validation.md",
    ):
        assert relative in receipt["input_bindings"], relative
    for name, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / name) == expected, f"receipt input drifted: {name}"
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "covered_obligation_ids",
        "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert set(receipt["canonical_obligation_ids"]) == set(spec["reconciled_inventory_ids"])
    assert receipt["reconciled_inventory_ids"] == spec["reconciled_inventory_ids"]
    assert receipt["recipe"]["covered_obligation_ids"] == spec["covered_obligation_ids"]
    assert set(spec["covered_obligation_ids"]) < set(spec["reconciled_inventory_ids"])

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["next_failed_theorem_gate"]["gate_id"] == (
        "S56-M-1138-FROZEN-ROUTE-RECONCILIATION"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert result["accepted_remaining_root_cut_set"] == ["M1138-T-BOUNDARY-MAX"]
    receipt_result = receipt["result"]
    assert receipt_result["verdict"] == "blocked"
    assert receipt_result["lifecycle_before"] == receipt_result["lifecycle_after"] == "planned"
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["accepted_receipt_ids"] == []
    expected_stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["recipe"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout.encode("utf-8")
    ).hexdigest()
    assert receipt["recipe"]["raw_combined_log_sha256"].startswith("not retained:")
    assert "release-grade" in receipt["recipe"]["raw_log_retention_boundary"]

    reconciliation = decision["evidence_reconciliation"]
    for gate in (
        "validation_recipe_fresh_at_current_snapshot",
        "accepted_exact_root_kernel_closure",
        "frozen_perturbation_route_reconciled",
        "authoritative_graph_root_closed",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "accepted_foundation_policy",
        "complete_transitive_provenance_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[gate] is False, gate
    assert reconciliation["accepted_closed_obligation_ids"] == []
    cut_set = "\n".join(result["remaining_release_cut_set"])
    for fragment in (
        "S56-M-1138-VALIDATION",
        "perturbation-route",
        "M1138-S-FOUNDATION",
        "M1138-X-PROVENANCE",
        "M1138-X-SOURCE",
        "R0 node-anchored",
        "AUDIT-Z",
        "empty-cache network-denied cold build",
        "two signed attestations",
        "minimal verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in cut_set, fragment

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean"):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited proof mechanism in {name}"

    proof_output = run([
        "/usr/bin/bwrap",
        "--ro-bind", "/", "/",
        "--tmpfs", "/tmp",
        "--dev", "/dev",
        "--proc", "/proc",
        "--unshare-net",
        "--die-with-parent",
        "--chdir", str(ROOT),
        "/usr/bin/bash", f"Stage1_Instances/{THEOREM}/check_proof.sh",
    ])
    assert proof_output.count("Declarations are sorry-free!") == 2
    for declaration in (
        "Stage1Instances.THM_M_1138.Proof.boundaryMaximumPackage",
        "Stage1Instances.THM_M_1138.Proof.harmonicWeakMaximumPrinciple",
    ):
        assert printed_axioms(proof_output, declaration) == {
            "propext", "Classical.choice", "Quot.sound"
        }

    packet_path = ROOT / ".stage1-worker-selftest.json"
    if packet_path.exists():
        packet = load(packet_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == decision["known_failures"]
        status = git("status", "--short", "--untracked-files=all")
        actual_changes = {
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    for path in (
        HERE / "check_release.py",
        HERE / "release-decision.json",
        HERE / "release-receipt.json",
        HERE / "release-spec.json",
        HERE / "release-validation.md",
    ):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
