#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0914-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0914"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0914-RELEASE"
THEOREM = "THM-M-0914"
BASE_REVISION = "c8b8f4f857647bcc095dc48e8c30390991351ab3"
BASE_TREE = "7a7e5a787c4d6e834f76a9787ee5e194074b1bc8"
EXPRESSION_SHA256 = "faef4a7f73219dc5b6178b8788978e21377c593ad84b845b4d49547218e6ae3b"
DENOMINATOR_SHA256 = "5a421bbbcc8afad0a1a35bb461a33c7712f8e2abd081706a36b4ccb4ce59f3ce"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "intake-receipt.json": "d97e3b20465c3d96efc775bfe86b1ffd87af3bf47ab5211d3193a3e2ef4a3858",
    "Statement.lean": "953cf5ba54e27cf08cce5a91880fd79d36f4b5aa7b92228bd27474a1399233db",
    "statement.json": "d7b6f9308f62afef5210ca8c01c17363cc0443ea5cb4a3261cdb9aa3c5ce646a",
    "statement-receipt.json": "969060307eea0b7b722a2e97e05d2c82d8683d29e3d9f8e30916baa808625e21",
    "anchor-audit.json": "3bad78f64fb4b2f28d4e1a032bb82c4c4fc4f528ee80781b1f5b227cf1bdca92",
    "anchor-audit-receipt.json": "be544ff8a040aa5592e84b4bf8817fda12eca406a327dd17f2d7ffcc5f238c76",
    "obligation-registry.json": "3379290c9bb2aa12cb9f2bd50d16174a5dbfefb1833bef961c394f8459c33d00",
    "obligation-tree-receipt.json": "f25ed59fad60242e4f7a26ae6d88921a3380269a5f1c76fcf80beccaaeaf5382",
    "typed-graphs.json": "05bacf88ed9a87e4cc5b796d0dae4944d57319ae890d67569e3e7bffccfdd5cc",
    "ObligationTree.lean": "b345e54fc0ee31fe58f76b8d15394dba7c090492eed94fad8468b6a79cc47272",
    "Proof.lean": "12f28163c757670e301e45282b6b5d02d50779c85fc5ce70109a7b3a9774bc8a",
    "proof-receipt.json": "15bbda352f967c3c2cfa32da8845be241db1d1bbcf448e225bef5e1deac28b78",
    "Validation.lean": "0a3b58a8f8e8b0edfa6b9c2bf85886912df366b941a757b16e721732c151824f",
    "check_validation.sh": "60d36f42e7dafde712fe1ee0d4d434908f69e29719062527c8c7d503e516ce2b",
    "validation-spec.json": "36a73bb2fcfbb5dc100845a74d7eb3db14091181d924f5a249a6aa224c283966",
    "validation-receipt.json": "4a923c65edd8c0d45f73c5996c8d660d70e339869aa55af8f2383ea737f3c6bf",
    "instance.json": "f073d38465200586aa998fc551211369cd62ecaf83503c09a67bab427af0f217",
    "task-dag.json": "ea3a86f9b7eef9f649cf32c7cedf21d728f347bc9d86a721d33e8e0c6244b7fe",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=600,
        check=False,
    )


def checked(argv: list[str], *, cwd: Path = ROOT) -> str:
    result = run(argv, cwd=cwd)
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return checked(["git", *args], cwd=cwd).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    instance = load(HERE / "instance.json")
    graphs = load(HERE / "typed-graphs.json")
    local_dag = load(HERE / "task-dag.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1456
    assert target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    assert target["baseline"] == "L0" and target["rework_required"] is True

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"]
        if row["id"] == "S56-M-0914-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1456,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0914-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in local_dag["tasks"]
        if row["id"] == "S56-M-0914-VALIDATION"
    )
    assert local_release["state"] == local_validation["state"] == "open"
    assert local_release["evidence_ids"] == local_validation["evidence_ids"] == []
    assert local_dag["accepted_states"] == []

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0914-ROOT"

    dependency = decision["dependency"]
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["intent"] == "release"
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["release_grade"] is decision["content_addressed"] is False
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0914-VALIDATION"
    assert dependency["generated_projection"] == "[_]"
    assert dependency["target_local_state"] == "open"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["content_addressed"] is validation["content_addressed"] is False
    assert dependency["master_accepted"] is False and validation["accepted"] is False
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 600 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert "warm" in spec["network_enforcement"] and "not section 10.6" in spec["network_enforcement"]
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["depends_on"] == ["S56-M-0914-VALIDATION"]
    assert receipt["verdict"] == "blocked" and receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed"] is receipt["master_accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["dependency_receipt"] == dependency
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
        "scope_boundary",
    ):
        assert receipt["recipe"][key] == spec[key]

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M3", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    receipt_result = receipt["result"]
    assert receipt_result["exit_code"] == 0 and receipt_result["verdict"] == "blocked"
    assert receipt_result["lifecycle_before"] == receipt_result["lifecycle_after"] == "planned"
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == ["H1", "M3", "R4"]
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["audit_z"] == receipt_result["theorem_z"] == "blocked"
    assert receipt_result["accepted_receipt_ids"] == receipt_result["accepted_closed_obligations"] == []
    assert receipt_result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt_result["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert set(receipt_result["observed_axioms"]) == EXPECTED_AXIOMS
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["changed_paths"] == decision["changed_paths"]

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "accepted_exact_root_kernel_closure",
        "generated_and_target_local_state_reconciled",
        "authoritative_graph_reconciled",
        "audit_z_accepted",
        "audit_inventory_complete_and_reconciled",
        "pinpoint_h0_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["accepted_closed_obligations"] == []
    assert set(reconciliation["observed_axioms"]) == EXPECTED_AXIOMS

    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False and boundary["root_machine_debt"] == "M3"
    assert boundary["accepted_closed_obligations"] == []
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    for obligation in (
        "M0914-X-SOURCE", "M0914-S-FOUNDATION", "M0914-X-PROVENANCE",
        "M0914-X-TRUST", "M0914-X-READABLE", "M0914-X-WORKFLOW",
    ):
        assert obligation in boundary["remaining_root_cut_set"]

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    validation_result = validation["result"]
    assert validation["verdict"] == "blocked" and validation["accepted"] is False
    assert validation_result["root_kernel_replayed"] is True
    assert validation_result["differential_exact_root_replayed"] is True
    assert validation_result["accepted_root_closed"] is False
    assert validation_result["hermetic_release_gate"] == "fail_closed"
    assert validation_result["independent_verification_gate"] == "fail_closed"
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False

    cut_set = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "master acceptance", "target-local all-open", "graph and debt reconciliation",
        "AUDIT-Z", "H0 primary-source", "R0 structured reconstruction",
        "transitive declaration", "empty-cache network-denied cold build", "SBOM",
        "two signed attestations", "minimal release verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in cut_set, fragment

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        assert prohibited.search(without_comments((HERE / name).read_text(encoding="utf-8"))) is None

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    replay = checked(["bash", f"Stage1_Instances/{THEOREM}/check_validation.sh"])
    assert replay == (
        "PASS THM-M-0914 network-isolated validation: exact proof and differential "
        "roots replayed; 15 declarations sorry-free; axioms within propext, "
        "Classical.choice, Quot.sound; closure has no unsafe or bodyless nonaxioms\n"
    )

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(decision["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"]
    release_command = next(
        row for row in packet["commands"] if row["argv"][-1] == f"Stage1_Instances/{THEOREM}/check_release.py"
    )
    assert release_command["exit_code"] == 0
    historical = next(
        row for row in packet["commands"] if row["argv"][-1] == f"Stage1_Instances/{THEOREM}/check_validation.py"
    )
    assert historical["exit_code"] == 1 and "phase-bound" in historical["result"]

    status = checked(["git", "status", "--short", "--untracked-files=all"])
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    handoff = " ".join((HERE / "release-validation.md").read_text(encoding="utf-8").split())
    for fragment in (
        "`blocked`", "`[H1, M3, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "release_grade=false", "This worker accepts no receipt",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS release inputs: target, DAG dependency, receipts, graph, and hashes agree")
    print("PASS current Lean replay: exact root and differential route are sorry-free; axioms within allowed profile")
    print("PASS fail-closed state: lifecycle planned; accepted root H1/M3/R4; accepted receipts 0")
    print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted")
    print("BLOCKED S56-10.6-HERMETIC-COLD-BUILD and independent release gates")
    print("verdict=blocked audit_complete=false theorem_complete=false")


if __name__ == "__main__":
    main()
