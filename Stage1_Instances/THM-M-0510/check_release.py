#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0510-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0510"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0510-RELEASE"
THEOREM = "THM-M-0510"
BASE_REVISION = "19eddccb8988b4da9e007b60f4a25b6806877160"
BASE_TREE = "1b5d55ad37802063bf31881e5e06faa0410bf21c"
EXPRESSION_SHA256 = "9c84bc6acd929a60f87942f0ae5647b0430b9164e35249e561bccecc0cb91b41"
DENOMINATOR_SHA256 = "59e9147cc46427b6fc6a114cf81f7a5710c3441cf3a9ef2a74b1690f08f167dd"
VALIDATION_RECEIPT_SHA256 = "88d72bdbd33f1f0761a380da25c1d0a4e11446ac91642e548aed6bad3acfbf2a"
PROOF_RECEIPT_SHA256 = "9d1955568997cfb937c59fb273ee586128f216fbecbb2e2fc4ef799fcf3f3edd"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
VECTOR = {"H": "H2", "M": "M3", "R": "R4"}
INVENTORY_IDS = [
    "M0510-ROOT",
    "M0510-S-ENCODING",
    "M0510-S-BOUNDARY",
    "M0510-N-EULER-PRODUCT",
    "M0510-N-COEFFICIENT",
    "M0510-C-CONTOUR",
    "M0510-B-ARC-SPLIT",
    "M0510-L-MODULAR",
    "M0510-L-MAJOR-LOCAL",
    "M0510-L-MAJOR-INTEGRAL",
    "M0510-L-MAJOR-ASYMPTOTIC",
    "M0510-L-MINOR-BOUND",
    "M0510-T-RECOMBINE",
    "M0510-T-ASYMPTOTIC",
    "M0510-X-SOURCE",
    "M0510-X-FOUNDATION",
    "M0510-X-PROVENANCE",
]
AUTHORITY_CUT = [
    "M0510-N-EULER-PRODUCT",
    "M0510-N-COEFFICIENT",
    "M0510-C-CONTOUR",
    "M0510-L-MODULAR",
    "M0510-L-MINOR-BOUND",
    "M0510-X-SOURCE",
    "M0510-X-FOUNDATION",
]
PROVISIONAL_CUT = [
    "M0510-N-COEFFICIENT",
    "M0510-C-CONTOUR",
    "M0510-L-MODULAR",
    "M0510-L-MINOR-BOUND",
    "M0510-X-SOURCE",
    "M0510-X-FOUNDATION",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
EVIDENCE_INPUTS = {
    "Statement.lean": "2bdbd9447b9917305ecb72e4268f14effd74ea12a55a2f9aa620fe1d497bd049",
    "ObligationTree.lean": "d75993a57087ceae4d2b80873e991794f87957d30f75950329b9d40a0f08982b",
    "Proof.lean": "4ec8e571d3f2565b81f48161f5e1dfb41ece0d37d7a04a6ccf473fb29d1e47fa",
    "Validation.lean": "9829b209a05559b99682eb1f1a41b19868357bf3a7bd676689abd68578313992",
    "instance.json": "3cbb9f3af2cd6e6bdfc360c1ad1e8bf82448af929738b42c72ae4b6a175a112c",
    "task-dag.json": "93cc5ee64b19679f3658854795097c0b25a9fcddf0b114b1e48e7748c073cec8",
    "statement.json": "1a5f4b03a9cc2bdcec1cd7691d2007f689dd88b291e68efebb7a45e676284c8a",
    "anchor-audit.json": "ec5b4e099f3ee3859390accceb8caf7cbb1d1a48c7b53ecf7b94bd8e8410c6c2",
    "obligation-registry.json": "678c26527bb23c368a7db74bc1aa6ac71e5ef479f8e0e54926fb288a2bde36b2",
    "typed-graphs.json": "98caff1f27cb7c1562624cde98867d64aa6c9387aa4af427cf3b7164e937987a",
    "proof-receipt.json": PROOF_RECEIPT_SHA256,
    "proof-blocker.json": "0373983c17ce362ff5de94d13b65259c2f81395cca8f223f5c6b31f29824234c",
    "validation-phase-spec.json": "ed7659a0dd30c935290c13ce9e9b0ccb3399cd8c1abc8ea4cd1832ec544bd893",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "7c88219d651533b5eeb71d124dceb755cf1f625a5a50dbd7bf44c8967a19fb08",
    "scope-map.md": "50730c98dc04b194c4d56b53a86eafac54c93ac8542986850139cda67e3f2ef2",
    "source-statement-crosswalk.md": "8baf54d69ca4479a493972ab1d5a836aaf526537122d045d6b5d34cf61010a98",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "97cea6374ca54395177bc40eaf5d1308358029bf49e7696d110f981f9bd41a52",
    "Docs/Stage1_Blueprint_rev-5.6.md": "d56ba1caab9c71e28c94c6a0ea45560cd08dbfffc0d32a2cbbe1c115d527fabd",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}


if not __debug__:
    raise RuntimeError("release checker requires Python assertions")


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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


def git(*args: str, cwd: Path = ROOT) -> str:
    completed = run(["/usr/bin/git", *args], cwd=cwd)
    assert completed.returncode == 0, completed.stdout
    return completed.stdout.strip()


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


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in EVIDENCE_INPUTS.items():
        assert sha256(HERE / name) == expected, f"evidence input drifted: {name}"
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 884
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0510-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 884,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0510-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    assert validation_item["depends_on"] == ["S56-M-0510-PROOF"]

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert tasks["lifecycle"] == "planned" and tasks["accepted_states"] == []
    local_tasks = {row["id"]: row for row in tasks["tasks"]}
    assert local_tasks["S56-M-0510-VALIDATION"]["state"] == "open"
    assert local_tasks[ITEM]["state"] == "open"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0510.HardyRamanujanAsymptoticTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EVIDENCE_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0510-ROOT"
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    computed_denominator = hashlib.sha256(
        json.dumps(registry["obligations"], sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert computed_denominator == DENOMINATOR_SHA256
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["theorem_complete"] is False
    assert closure["root_machine_classification"] == "M3"
    assert closure["first_open_cut"] == AUTHORITY_CUT
    by_id = {node["obligation_id"]: node for node in graphs["nodes"]}
    assert by_id["M0510-N-EULER-PRODUCT"]["machine_debt"] == "M4"
    assert by_id["M0510-N-EULER-PRODUCT"]["evidence_ids"] == []
    assert by_id["M0510-T-ASYMPTOTIC"]["machine_debt"] == "M0-L"

    tree = source_without_comments((HERE / "ObligationTree.lean").read_text(encoding="utf-8"))
    assert re.search(
        r"def FinalAsymptoticPackage\s*:\s*Prop\s*:=\s*HardyRamanujanAsymptoticTarget",
        tree,
    )
    assert re.search(
        r"theorem root_of_finalAsymptotic\s*\(h\s*:\s*FinalAsymptoticPackage\)\s*:\s*HardyRamanujanAsymptoticTarget\s*:=\s*by\s*exact h",
        tree,
    )
    assert "A tautological theorem assuming the asymptotic formula as a hypothesis." in (
        HERE / "scope-map.md"
    ).read_text(encoding="utf-8")

    assert sha256(HERE / "proof-receipt.json") == PROOF_RECEIPT_SHA256
    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False and proof["verdict"] == "no_state_change"
    assert proof["result"]["proof_phase_complete"] is False
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert proof["provisionally_closed_obligation_ids"] == ["M0510-N-EULER-PRODUCT"]
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["remaining_root_cut_set"] == PROVISIONAL_CUT

    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["accepted_receipt_ids"] == []
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_closed"] is validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["result"]["structured_terminal_transport_gate"] == "fail_closed_semantic_mismatch"
    assert validation["result"]["hermetic_release_gate"] == "fail_closed"
    assert validation["result"]["independent_distinct_runner_gate"] == "fail_closed"
    validation_checker = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert 'BASE_REVISION = "472dc79eb4d406a6707691193fbe3ab58d0f0cc4"' in validation_checker
    stale = run(
        ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py", "--probe"],
        timeout=60,
    )
    assert stale.returncode != 0
    assert "AssertionError" in stale.stdout

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == decision["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == decision["theorem_id"] == THEOREM
    assert spec["recipe_id"] == decision["release_recipe_id"]
    assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
            "covered_obligation_ids", "covered_declarations", "covered_decisions", "scope_boundary",
        )
    }

    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["decision_support"] == receipt["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert receipt["accepted"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["master_acceptance"] is False
    assert decision["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert decision["dependency"]["master_accepted"] is False
    assert receipt["dependency_receipt"]["sha256"] == VALIDATION_RECEIPT_SHA256
    assert receipt["dependency_receipt"]["master_accepted"] is False

    assert decision["verdict"] == receipt["result"]["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector_before"] == decision["root_vector_after"] == VECTOR
    assert receipt["result"]["root_vector_before"] == receipt["result"]["root_vector_after"] == VECTOR
    assert decision["audit_complete"] is decision["theorem_complete"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert decision["release_accepted"] is receipt["result"]["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert decision["first_failed_gate"]["gate_id"] == "dependency.S56-M-0510-VALIDATION.master_acceptance"
    assert decision["first_failed_theorem_gate"]["gate_id"] == "M0510-N-COEFFICIENT.kernel_closure"
    assert decision["first_failed_release_gate"]["gate_id"] == "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    assert decision["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert decision["authoritative_graph_first_open_cut"] == AUTHORITY_CUT
    assert decision["provisional_post_proof_remaining_root_cut_set"] == PROVISIONAL_CUT
    assert receipt["remaining_root_cut_set"] == PROVISIONAL_CUT

    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["accepted_closed_obligation_ids"] == []
    for key in (
        "exact_root_kernel_closure",
        "audit_inventory_reconciliation",
        "human_source_h0_acceptance",
        "readability_r0_acceptance",
        "complete_transitive_provenance_foundation_tcb",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] == "missing", key
    remaining = "\n".join(decision["remaining_theorem_completion_gates"])
    for fragment in (
        "stale M0-L terminal-transport claim",
        "coefficient extraction",
        "AUDIT-Z",
        "H0 pinpoint",
        "R0 node-specific",
        "empty-cache network-denied cold build",
        "two signed attestations",
        "minimal release verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in remaining, fragment

    assert receipt["evidence_inputs"] == EVIDENCE_INPUTS
    assert receipt["authority_inputs"] == AUTHORITY_INPUTS
    assert receipt["tool_inputs"] == TOOL_INPUTS
    assert decision["reconciled_inputs"] == EVIDENCE_INPUTS
    assert decision["authority_inputs"] == AUTHORITY_INPUTS
    assert receipt["release_artifact_inputs"]["release-spec.json"] == sha256(HERE / "release-spec.json")
    assert receipt["release_artifact_inputs"]["release-decision.json"] == sha256(HERE / "release-decision.json")
    assert receipt["release_artifact_inputs"]["release-validation.md"] == sha256(HERE / "release-validation.md")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|run_tac|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        assert prohibited.search(source_without_comments((HERE / name).read_text(encoding="utf-8"))) is None

    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert mathlib.is_dir()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""

    replay = run(["bash", f"Stage1_Instances/{THEOREM}/check_proof.sh"])
    assert replay.returncode == 0, replay.stdout
    reports = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", replay.stdout, re.DOTALL)
    assert len(reports) == 5
    for _, raw in reports:
        assert {name.strip() for name in raw.split(",") if name.strip()} == EXPECTED_AXIOMS
    assert "PASS THM-M-0510 trust-zero replay" in replay.stdout
    assert "first remaining machine gate: M0510-N-COEFFICIENT" in replay.stdout
    assert "root remains open M3; theorem_complete=false" in replay.stdout
    assert "sorryAx" not in replay.stdout
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]

    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, sorted(actual_changed)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("PASS S56-M-0510-RELEASE negative reconciliation")
    print("verdict=blocked lifecycle=planned root_vector=H2/M3/R4")
    print("root_closed=false audit_complete=false theorem_complete=false")
    print("first_failed_gate=dependency.S56-M-0510-VALIDATION.master_acceptance")
    print("first_theorem_gate=M0510-N-COEFFICIENT.kernel_closure")
    print("release_gates=immutable-clean-input,cold-offline,independent-verifier,bundle")


if __name__ == "__main__":
    main()
