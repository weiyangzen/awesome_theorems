#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1057-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1057"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1057-RELEASE"
THEOREM = "THM-M-1057"
BASE_REVISION = "a82f55b39af066976bbf2e4bef9948f55430dd9d"
BASE_TREE = "82443ce17bd24cc5c65cc8c50c72405653e65192"
EXPRESSION_SHA256 = "aebaaa6256cc5cb252ff4662647955a625f2ff6f1311dbcea1c04463ab3c03af"
DENOMINATOR_SHA256 = "080ff4e9ec6298847c52b7135ca47d9d57aecd0797d2ff1acd6161aaf1b0f67c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
VALIDATION_RECEIPT_ID = "S56-M-1057-VALIDATION-narrow-20260714T034615+0800"
PROOF_RECEIPT_ID = "S56-M-1057-PROOF-local-20260714T015200+0800"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_EXECUTABLES = {
    "lean_executable_sha256": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "lake_executable_sha256": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
    "python_executable_sha256": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "git_executable_sha256": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
    "bash_executable_sha256": "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd",
    "bubblewrap_executable_sha256": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
}
EXPECTED_INPUTS = {
    "intake.json": "dcf46b92aac91ff380ff49e9926dcb92bb6a6b915ab9a706c6d576d7f13e36d1",
    "Statement.lean": "bdd8ad8026b13ec9de27a63aac9874e88d29e8f57a9d5dcf0380d3f14eb61073",
    "statement.json": "7548489e0797f7d8ce20cade71c22e584f10205ca4f6f84697ab59751e20a5c0",
    "AnchorAudit.lean": "e56fab6de687822f640d476029b379a251261183dbec818e924d1a0ea19be1f1",
    "anchor-audit.json": "14b523ec4f5e2c1b918a0c1a0fcbe12fffaf46fe185333f277356472a2829003",
    "ObligationTree.lean": "637c86f449f9d6e0180a93cae59672f1ecbffe9fd06c216065adc1c3e4adfd7a",
    "obligation-registry.json": "71394c3b69dd4b8970849416d502072fdc3fb7775d8ee92fdddf1fb5cf97ace0",
    "typed-graphs.json": "b9d95e5ec6c81f9196c72f175c45d3f426696871c45234fe0dd7ed7b8f1e3c96",
    "validation-specs.json": "b971c17b17d85e1700e57ec99b27d8dcd89ed82a1980c846d0ff6ea924d9320b",
    "MaximalErgodic.lean": "1e6ecd26fe2f3587f292e82e41b3bc7e61f5110cf4be6e3a5e4bc53a8a45c6d5",
    "Birkhoff.lean": "0bb4ef8cc491100c54c8966ba31c44ac86661117b1e1eac8498564bc5384f789",
    "KingmanFekete.lean": "4112aaeb5043c7bc5e659c62ef8f58b5f563ebfe94fae9eb3ad0c9bcbcf3749a",
    "KingmanDerriennic.lean": "1bd9754dcc2f957084804a9b7136e0a378bd9abc7e857a77b86857298934340a",
    "KingmanCompanion.lean": "231b552e488d9b693edfaf1b461e612901698e205227db2fc579a4d4d54f9f2a",
    "KingmanBlockSqueeze.lean": "3e26d917b00133917ea10788c8e54542cff61c8d03c7afd6c8138f60720ba567",
    "KingmanCore.lean": "fb2fad9b2c30386476fa67b9db71eda07880823d902f183f9eab2a915a5a4d82",
    "KingmanMeans.lean": "96fc4065af56f39ca17602238a31d6de108d0d0bf3db6fd490c1a5a2b8e6cc52",
    "Proof.lean": "235eb7cbbc9a3bb6fa7f4f651de1d260dc1e89b2d40471fac8f82757b32278ec",
    "proof-receipt.json": "d49b270822bab040d3455afbb40b552d9bf90b682083cfc015e0df11c15b5d32",
    "Validation.lean": "f0be52b702f13ba0cb38d15e0e3a3366c6e70d14899cab64ca9cb3a35b55e942",
    "validation-spec.json": "e7da3cc084a5ece111542516af992b8c7abab3ef1f5fdc6fe54c2d336a5fd18c",
    "validation-receipt.json": "f266604127afbfb28f66c85f52b2a643a3b68610f22643db4bc8d68e48d87c2a",
    "check_validation.py": "c9247633e8403aa061ecdbf9f4beec3a12da0a180eac71cf443e580a12a130e8",
    "check_validation.sh": "76d84f62b74c9fc7532855f0cdd7686f1f332d2c78891f8995eb412b3cb3fea8",
    "source_statement_crosswalk.md": "5c4eaf9050d57f9f7348b46bee63a269f136f6ca2e465cb973d55644aadd62b0",
    "PORT_PROVENANCE.md": "7620ed425654a3fd729fcda38c8994a98db7e9e60944355a52c78f2cee4c17db",
    "LICENSE": "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
INVENTORY_IDS = [
    "M1057-ROOT", "M1057-S-DEFINITIONS", "M1057-S-BOUNDARY",
    "M1057-S-FOUNDATION", "M1057-N-EXPECTATION-SUBADDITIVE",
    "M1057-L-FEKETE", "M1057-C-BLOCK-DECOMPOSITION",
    "M1057-L-MAXIMAL-INEQUALITY", "M1057-L-AE-CONVERGENCE",
    "M1057-L-INVARIANCE", "M1057-L-ERGODIC-IDENTIFICATION",
    "M1057-T-LIMIT-PACKAGE", "M1057-T-ASSEMBLE", "M1057-X-SOURCE",
    "M1057-X-PROVENANCE",
]
MACHINE_IDS = INVENTORY_IDS[:13]
KERNEL_REPLAYED_IDS = [
    "M1057-ROOT", "M1057-T-LIMIT-PACKAGE", "M1057-T-ASSEMBLE",
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
    "PASS current Lean replay: exact root is sorry-free with exactly propext, Classical.choice, and Quot.sound",
    "PASS fail-closed state: lifecycle planned; accepted root H1/M3/R3; accepted receipts 0",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted",
    "BLOCKED provenance authority, audit, immutable input, cold/offline, trust, and independent release gates",
    "verdict=blocked audit_complete=false theorem_complete=false",
)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate key {key!r} in {path}"
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 900) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
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
    output: list[str] = []
    depth = 0
    index = 0
    while index < len(source):
        if source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            index += 1
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


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
        raise RuntimeError("release checker requires Python assertions (no -O)")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    graphs = load(HERE / "typed-graphs.json")
    registry = load(HERE / "obligation-registry.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 249
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"]
        if row["id"] == "S56-M-1057-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 249,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1057-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert intake["root_vector"] == {
        "human": "H1", "machine": "M3", "readability": "R3"
    }
    assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False and boundary["root_machine_debt"] == "M3"
    assert boundary["minimal_open_cut"] == ["M1057-T-LIMIT-PACKAGE"]
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False

    assert proof["receipt_id"] == PROOF_RECEIPT_ID
    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False and proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert validation["receipt_id"] == VALIDATION_RECEIPT_ID
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["first_failed_gate"] == (
        "dependency.S56-M-1057-PROOF.master_acceptance"
    )
    assert validation["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert validation["result"]["accepted_root_vector"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }
    assert validation["result"]["accepted_closed_obligations"] == []
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["provenance"][
        "complete_transitive_declaration_and_source_origin_closure"
    ] is False
    assert anchor["external_lean4_search"]["immutable_candidate_revisions"] == []
    assert anchor["classification"]["machine_status"] == "not_repo_local_closed"
    assert proof["proof_body"]["origin"]["revision"] == (
        "ed3fa6b8a30594eeb791160563942ba115581aa0"
    )
    analytic_ids = set(proof["provisionally_closed_proof_obligation_ids"]) - {
        "M1057-ROOT", "M1057-T-ASSEMBLE"
    }
    body_ids = {
        row["obligation_id"]: row["terminal_proof_body_id"]
        for row in registry["obligations"]
    }
    assert all(body_ids[node] is None for node in analytic_ids)
    assert all(
        not node["evidence_ids"] and node["provenance_id"] == "none"
        for node in graphs["nodes"] if node["obligation_id"] in analytic_ids
    )

    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["execution_rank"] == 249 and decision["intent"] == "release"
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["decision_support"] == receipt["support_state"] == (
        "provisional_worker_selftest"
    )
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_base_revision"] == validation["base_revision"]
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert decision["provisional_receipt_ids_inspected"] == [
        PROOF_RECEIPT_ID, VALIDATION_RECEIPT_ID
    ]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-1057-RELEASE-negative-reconciliation-v1"
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 900 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0 and spec["covered_obligation_ids"] == INVENTORY_IDS
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key

    result = decision["decision"]
    assert result["verdict"] == receipt["result"]["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == [
        "H1", "M3", "R3"
    ]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == (
        "S56-10.2-DEPENDENCY-ACCEPTANCE"
    )
    assert result["first_failed_theorem_gate"]["gate_id"] == (
        "M1057-X-PROVENANCE-AUTHORITY-RECONCILIATION"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["kernel_replayed_obligation_ids"] == KERNEL_REPLAYED_IDS
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["remaining_root_cut_set"] == result["remaining_root_cut_set"]

    for key in (
        "accepted_exact_root_kernel_closure", "proof_master_acceptance",
        "anchor_candidate_inventory_reconciled",
        "node_specific_proof_body_mapping_reconciled",
        "authoritative_graph_reconciled", "audit_z_accepted",
        "pinpoint_h0_review", "independent_r0_review",
        "accepted_foundation_policy", "complete_transitive_provenance_tcb_closure",
        "immutable_clean_release_input", "hermetic_cold_offline_replay",
        "sbom_license_archive_closure", "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_mutation_gates", "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    lean_names = (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
        "MaximalErgodic.lean", "Birkhoff.lean", "KingmanFekete.lean",
        "KingmanDerriennic.lean", "KingmanCompanion.lean",
        "KingmanBlockSqueeze.lean", "KingmanCore.lean", "KingmanMeans.lean",
        "Proof.lean", "Validation.lean",
    )
    for name in lean_names:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    replay = run(["bash", f"Stage1_Instances/{THEOREM}/check_validation.sh"])
    declarations = (
        "Stage1Instances.THM_M_1057.root_of_pointwiseLimitPackage",
        "ErgodicTheory.tendsto_kingman_ergodic_means",
        "Stage1Instances.THM_M_1057.pointwiseLimitPackage",
        "Stage1Instances.THM_M_1057.kingmanTarget",
    )
    for declaration in declarations:
        assert printed_axioms(replay, declaration) == EXPECTED_AXIOMS, declaration
    assert replay.count("Declarations are sorry-free!") == 11
    assert "declaration uses 'sorry'" not in replay and "error:" not in replay

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    receipt_commands = {
        (tuple(row["argv"]), row["exit_code"]) for row in receipt["commands"]
    }
    packet_commands = {
        (tuple(row["argv"]), row["exit_code"]) for row in packet["commands"]
    }
    assert receipt_commands <= packet_commands
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    expected_bindings = {
        *(f"Stage1_Instances/{THEOREM}/{name}" for name in EXPECTED_INPUTS),
        f"Stage1_Instances/{THEOREM}/release-spec.json",
        f"Stage1_Instances/{THEOREM}/release-decision.json",
        f"Stage1_Instances/{THEOREM}/release-validation.md",
        f"Stage1_Instances/{THEOREM}/check_release.py",
        ".stage1-worker-selftest.json",
        *EXPECTED_TOOL_INPUTS,
    }
    assert set(receipt["input_bindings"]) == expected_bindings
    for name, expected in receipt["input_bindings"].items():
        path = ROOT / name if name.startswith((".", "Stage1_")) else LEAN_ROOT / name
        assert sha256(path) == expected, f"release input drifted: {name}"
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    for key, expected in EXPECTED_EXECUTABLES.items():
        assert receipt["environment"][key] == expected

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H1, M3, R3]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "This worker accepts no", "`release_grade=false`",
    ):
        assert fragment in handoff, fragment

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
