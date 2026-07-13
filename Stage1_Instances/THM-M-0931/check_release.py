#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0931-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0931"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0931-RELEASE"
THEOREM = "THM-M-0931"
BASE_REVISION = "c45f3c7090cb4adf616d45e5414985f956e807b2"
BASE_TREE = "da6f991c07f11e8608ddc090af9356558d64d360"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_DECLARATIONS = [
    "Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget",
    "Stage1Instances.THM_M_0931.Proof.erdosGinzburgZiv_via_frozen_composition",
    "Stage1Instances.THM_M_0931.Proof.erdosGinzburgZiv_direct",
    "Stage1Instances.THM_M_0931.Proof.erdosGinzburgZiv",
    "Stage1Instances.THM_M_0931.Validation.independentlyReconstructedErdosGinzburgZiv",
    "Int.erdos_ginzburg_ziv_multiset",
    "Int.erdos_ginzburg_ziv",
    "char_dvd_card_solutions_of_add_lt",
]
EXPRESSION_SHA256 = "b872e0de4aedbd0da8825d2c7dd9ecb30e01215131c61e73dc3050776711718a"
DENOMINATOR_SHA256 = "2b96d10afc8120ac78b0b3029f490c99406b9ea53a07ec3a933108354ae5cd6a"
VALIDATION_STDOUT_SHA256 = (
    "fc6cb44a5e47f577b1f168fde3af77a6da234d9f395e9e433fcb18c5d9df2d6b"
)
EXPECTED_INPUTS = {
    "Statement.lean": "d0e7e43d896a0625e87b3fac55319d5e999351c8f74cdda4e699d9360d651020",
    "ObligationTree.lean": "0e2e918e613f47fb6fefad481a9f7519bdda6a1a7c190ee3cae79280a6df4243",
    "Proof.lean": "01388ff60613831a83597b5647db19c08451a8b6fb1a574592fbadb658649f9f",
    "Validation.lean": "40a61533c3b46afdcf2577c2b278ee59055b62f7b141b15cf60253c80e35db59",
    "instance.json": "f5742b911dc2157ce3ab4d2a3d88bea08d34c5858c16b21bb25bf84e506bc6c2",
    "task-dag.json": "2d79adba8c7b7aa43e9e186888f81f05c568cfdcedd2e34b9cad62ec2eb58707",
    "statement.json": "84e0e15bc6545467b3ed6442dd33c07a9f471d550546c17ebc2adb9040fe1b4d",
    "obligation-registry.json": "ebdf51a2fd9bd2a724c38888e4b530d05398e2b441160922e8777f84ca71057a",
    "typed-graphs.json": "69a0d48b2697373ac9d708a548a0cd5765a0eda9df063b5e2c69924a558c7f2b",
    "proof-receipt.json": "b40d076951b9326b3fb3f04e173976b14d341a2d135afba745761fd0a2e9642d",
    "validation-spec.json": "be1472dcb9ba4ba9f573f9d4fa3cfd047813c057946ae24f6b3a09e303103a6f",
    "validation-receipt.json": "e179b7bb84efdc7be5d382b88662e84749fc6bd2148c7920f1eed5575459c1fe",
    "check_validation.py": "1315a497b8e05c62f6cb9e8bbb4d917004d5226711cc8de0b45ef3d00c5c33d4",
    "check_validation.sh": "04dd31d0f2b578a12a86d6c1b8ba2e29713b000a9c26d1b9205792e58591b93d",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "71a730375a1cdbb3a5b649b99603fcb242858098930cfe775b4dcf17959af441",
    "Docs/Stage1_Blueprint_rev-5.6.md": "0c47ebed000812e68becc418480cc51367a289235e76655764b4cea6096a97da",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
INVENTORY_IDS = [
    "M0931-ROOT",
    "M0931-S-INTERFACE",
    "M0931-S-BOUNDARY",
    "M0931-S-COUNT-TRANSPORT",
    "M0931-S-RESIDUE-TRANSPORT",
    "M0931-S-FOUNDATION",
    "M0931-T-ROOT-COMPOSE",
    "M0931-A-MULTISET-EGZ",
    "M0931-N-ENUMERATE",
    "M0931-L-INDEXED-EGZ",
    "M0931-B-INDUCTION",
    "M0931-B-ZERO",
    "M0931-B-ONE",
    "M0931-B-PRIME",
    "M0931-T-PRIME-CAST",
    "M0931-L-ZMOD-PRIME",
    "M0931-C-POLYNOMIALS",
    "M0931-L-DEGREE-BOUND",
    "M0931-X-CHEVALLEY-WARNING",
    "M0931-L-NONZERO-SOLUTION",
    "M0931-L-PRIME-CARD",
    "M0931-L-PRIME-SUM",
    "M0931-B-COMPOSITE",
    "M0931-C-DISJOINT-BLOCKS",
    "M0931-L-INNER-INDUCTION",
    "M0931-L-OUTER-INDUCTION",
    "M0931-T-COMPOSITE-ASSEMBLE",
    "M0931-X-SOURCE",
    "M0931-X-PROVENANCE",
    "M0931-X-TRUST",
    "M0931-X-READABLE",
    "M0931-X-WORKFLOW",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = (
    "PASS release inputs: target, DAG dependency, receipts, graph, and hashes agree",
    "PASS current Lean replay: exact roots are sorry-free with exactly propext, Classical.choice, and Quot.sound",
    "PASS fail-closed state: lifecycle planned; accepted root H1/M3/R4; accepted receipts 0",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted",
    "BLOCKED immutable input, cold/offline, source/readability, trust, and independent release gates",
    "verdict=blocked audit_complete=false theorem_complete=false",
)
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 600
EXPECTED_COMMANDS = [
    {
        "argv": ["python3", "Docs/tools/check_stage1_standard.py"],
        "cwd": ".",
        "exit_code": 0,
        "result": "15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed",
    },
    {
        "argv": ["python3", "scripts/stage1_target.py", "check"],
        "cwd": ".",
        "exit_code": 0,
        "result": "1546 unique targets with ranks 1 through 1546 passed",
    },
    {
        "argv": ["python3", "scripts/stage1_target.py", "show", THEOREM],
        "cwd": ".",
        "exit_code": 0,
        "result": "rank 1470 remains planned, L0/rework-required, and theorem-incomplete",
    },
    {
        "argv": ["bash", f"Stage1_Instances/{THEOREM}/check_validation.sh"],
        "cwd": ".",
        "exit_code": 0,
        "result": (
            "network-isolated exact proof and differential roots elaborated; "
            "twelve declarations were sorry-free with exactly the recorded axiom set"
        ),
    },
    {
        "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"],
        "cwd": ".",
        "exit_code": 0,
        "result": (
            "release authority, inputs, receipts, graph, narrow Lean evidence, "
            "and all fail-closed release gates reconciled"
        ),
    },
    {
        "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"],
        "cwd": ".",
        "env": {"PYTHONOPTIMIZE": "1"},
        "exit_code": 1,
        "result": "expected fail-closed rejection when Python assertions are disabled",
    },
    *[
        {
            "argv": ["python3", "-m", "json.tool", path],
            "cwd": ".",
            "exit_code": 0,
            "result": result,
        }
        for path, result in (
            (f"Stage1_Instances/{THEOREM}/release-spec.json", "release specification parsed as JSON"),
            (f"Stage1_Instances/{THEOREM}/release-decision.json", "release decision parsed as JSON"),
            (f"Stage1_Instances/{THEOREM}/release-receipt.json", "release receipt parsed as JSON"),
            (".stage1-worker-selftest.json", "worker packet parsed as JSON"),
        )
    ],
    {
        "argv": ["python3", "-m", "py_compile", f"Stage1_Instances/{THEOREM}/check_release.py"],
        "cwd": ".",
        "env": {"PYTHONPYCACHEPREFIX": "/tmp/stage1-thm-m-0931-release-pycache"},
        "exit_code": 0,
        "result": "release checker syntax compiled outside the repository",
    },
    {
        "argv": [
            "rg", "-n", "--glob", "*.lean",
            r"\b(sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
            r"^[[:space:]]*(axiom|constant|opaque|unsafe)\b",
            f"Stage1_Instances/{THEOREM}",
        ],
        "cwd": ".",
        "exit_code": 1,
        "result": (
            "raw auxiliary no-match scan over target Lean sources; the release checker "
            "separately performs the comment-stripped scan"
        ),
    },
    {
        "argv": [
            "git", "diff", "--check", "--", f"Stage1_Instances/{THEOREM}",
            ".stage1-worker-selftest.json",
        ],
        "cwd": ".",
        "exit_code": 0,
        "result": "no whitespace diagnostics",
    },
]


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    if remaining <= 0:
        raise RuntimeError("release recipe exceeded its total 600-second timeout")
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, (declaration, output)
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    graphs = load(HERE / "typed-graphs.json")
    registry = load(HERE / "obligation-registry.json")
    local_dag = load(HERE / "task-dag.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["intent"] == decision["phase"] == "release"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["intent"] == receipt["phase"] == "release"
    assert receipt["depends_on"] == ["S56-M-0931-VALIDATION"]

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 1470,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM,
        "name": "Erdős–Ginzburg–Ziv定理",
        "category": "组合数学 / 计数组合",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0931-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1470,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0931-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]"
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in local_dag["tasks"] if row["id"] == "S56-M-0931-VALIDATION"
    )
    assert local_release["state"] == local_validation["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-0931-VALIDATION"]
    assert local_dag["accepted_states"] == []

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    for name, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert receipt["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS
    expected_receipt_inputs = {
        **{
            f"Stage1_Instances/{THEOREM}/{name}": expected
            for name, expected in EXPECTED_INPUTS.items()
        },
        **{
            f"Formalizations/Lean/{name}": expected
            for name, expected in EXPECTED_TOOL_INPUTS.items()
        },
    }
    assert receipt["input_bindings"] == expected_receipt_inputs
    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"

    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["decision_support"] == receipt["support_state"]
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert receipt["accepted"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["master_acceptance"] == "pending_and_not_claimed"
    assert receipt["decision_id"] == decision["decision_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    checker_sha256 = sha256(Path(__file__))
    assert decision["release_checker_sha256"] == checker_sha256
    assert decision["release_recipe_id"] == spec["recipe_id"]
    release_bindings = receipt["release_artifact_bindings"]
    assert release_bindings == {
        f"Stage1_Instances/{THEOREM}/check_release.py": checker_sha256,
        f"Stage1_Instances/{THEOREM}/release-spec.json": sha256(HERE / "release-spec.json"),
        f"Stage1_Instances/{THEOREM}/release-decision.json": sha256(HERE / "release-decision.json"),
        f"Stage1_Instances/{THEOREM}/release-validation.md": sha256(HERE / "release-validation.md"),
    }
    assert receipt["binding_cycle_boundary"] == (
        "The receipt binds the upstream release specification, checker, decision, "
        "and readable handoff. It cannot bind its own bytes or the downstream worker "
        "packet; release_grade=false and content-addressed release evidence is not claimed."
    )

    dependency = decision["dependency"]
    assert dependency == {**receipt["dependency"], "worker_projection": "[_]"}
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0931-VALIDATION"
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
    assert spec["recipe_id"] == receipt["recipe"]["recipe_id"]
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 600 and spec["network_policy"] == "denied"
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_declarations"] == EXPECTED_DECLARATIONS
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact six-line PASS/BLOCKED release status summary",
    }]
    assert "Fail-closed release reconciliation" in spec["scope_boundary"]
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key

    result = decision["decision"]
    assert result["verdict"] == receipt["result"]["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    vector = {"H": "H1", "M": "M3", "R": "R4"}
    assert result["root_vector_before"] == result["root_vector_after"] == vector
    assert receipt["result"]["root_vector_before"] == vector
    assert receipt["result"]["root_vector_after"] == vector
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    receipt_result = receipt["result"]
    assert receipt_result["lifecycle_before"] == receipt_result["lifecycle_after"] == "planned"
    assert receipt_result["exit_code"] == 0
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["release_accepted"] is False
    assert receipt_result["accepted_receipt_ids"] == []
    assert receipt_result["accepted_closed_obligations"] == []
    assert set(receipt_result["observed_axioms"]) == EXPECTED_AXIOMS
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert receipt_result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt_result["first_failed_release_specific_gate"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert receipt_result["next_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["first_failed_gate"] == receipt_result["first_failed_gate"]
    assert receipt["first_failed_release_specific_gate"] == (
        receipt_result["first_failed_release_specific_gate"]
    )
    assert receipt["next_failed_release_gate"] == receipt_result["next_failed_release_gate"]
    assert "not release-grade evidence" in receipt["status_boundary"]
    semantic_output = "\n".join(SUMMARY_LINES) + "\n"
    semantic_output_sha256 = hashlib.sha256(semantic_output.encode("utf-8")).hexdigest()
    assert decision["release_output_sha256"] == semantic_output_sha256
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": semantic_output_sha256,
        "stdout_bytes": len(semantic_output.encode("utf-8")),
        "expected_line_count": len(SUMMARY_LINES),
        "exit_code": 0,
    }
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["retry_condition"] == decision["retry_condition"]
    assert receipt["changed_paths"] == decision["changed_paths"] == sorted(CHANGED_PATHS)

    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == vector
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["canonical_statement"] is None
    assert instance["canonical_formal_target"]["declaration_or_expression"] is None
    assert instance["obligation_registry_hash"] is None
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False
    assert boundary["accepted_root_machine_debt"] == "M3"
    assert boundary["accepted_closed_obligations"] == []
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert len(graphs["unverified_decomposition_plans"]) == 6

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["root_evidence"]["root_kernel_declaration_closed"] is True
    assert proof["root_evidence"]["accepted_root_closed"] is False
    assert proof["root_evidence"]["machine_debt_proposal"] == "M0-W"
    assert proof["root_evidence"]["unverified_internal_composition_count"] == 6
    validation_result = validation["result"]
    assert validation_result["root_kernel_replayed"] is True
    assert validation_result["differential_exact_root_replayed"] is True
    assert validation_result["accepted_root_closed"] is False
    assert validation_result["accepted_machine_debt"] == "M3"
    assert validation_result["hermetic_release_gate"] == "fail_closed"
    assert validation_result["independent_verification_gate"] == "fail_closed"
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "accepted_exact_root_m0_w_e1",
        "authoritative_instance_and_graph_reconciled",
        "internal_source_body_composition_certificates_complete",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_mutation_gates",
        "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["accepted_closed_obligations"] == []
    cut_set = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "S56-M-0931-VALIDATION",
        "six exact child-to-parent composition certificates",
        "H0 primary-source",
        "R0 node-anchored",
        "AUDIT-Z",
        "empty-cache network-denied cold build",
        "two signed attestations",
        "minimal release verifier",
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
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    lean_path = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lean_version = run([str(lean_path), "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    python_path = Path(shutil.which("python3") or "").resolve()
    git_path = Path(shutil.which("git") or "").resolve()
    bwrap_path = Path(shutil.which("bwrap") or "").resolve()
    environment = receipt["environment"]
    assert environment["lean_version"] == "4.29.0"
    assert environment["lean_commit"] == LEAN_COMMIT
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert sha256(lean_path) == environment["lean_executable_sha256"]
    assert sha256(python_path) == environment["python_executable_sha256"]
    assert sha256(git_path) == environment["git_executable_sha256"]
    assert sha256(bwrap_path) == environment["bubblewrap_executable_sha256"]
    replay = run(["bash", str(HERE / "check_validation.sh")])
    assert hashlib.sha256(replay.encode("utf-8")).hexdigest() == VALIDATION_STDOUT_SHA256
    proof_declarations = (
        "Int.erdos_ginzburg_ziv_multiset",
        "Int.erdos_ginzburg_ziv",
        "char_dvd_card_solutions_of_add_lt",
        "Stage1Instances.THM_M_0931.Proof.pinnedIndexedIntegerEGZ",
        "Stage1Instances.THM_M_0931.Proof.pinnedAtLeastCountAnchor",
        "Stage1Instances.THM_M_0931.Proof.atLeastCountAnchor_via_frozen_enumeration",
        "Stage1Instances.THM_M_0931.Proof.erdosGinzburgZiv_via_frozen_composition",
        "Stage1Instances.THM_M_0931.Proof.erdosGinzburgZiv_direct",
        "Stage1Instances.THM_M_0931.Proof.erdosGinzburgZiv",
    )
    differential_declarations = (
        "Int.erdos_ginzburg_ziv",
        "char_dvd_card_solutions_of_add_lt",
        "Stage1Instances.THM_M_0931.Validation.independentlyReconstructedErdosGinzburgZiv",
    )
    for declaration in proof_declarations + differential_declarations:
        assert printed_axioms(replay, declaration) == EXPECTED_AXIOMS, declaration
    assert replay.count("Declarations are sorry-free!") == 12
    assert "sorryAx" not in replay and "declaration uses 'sorry'" not in replay

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    assert packet["output_summary"] == list(SUMMARY_LINES)
    assert packet["commands"] == EXPECTED_COMMANDS
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "The verdict is `blocked`", "`[H1, M3, R4]`", "`AUDIT-Z`",
        "`THEOREM-Z`", "This worker accepts no receipt", "release_grade=false",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    assert environment["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
