#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0822-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


if not __debug__:
    raise SystemExit("check_release.py must run without Python optimization")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0822"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0822-RELEASE"
THEOREM = "THM-M-0822"
BASE_REVISION = "86da50a0693b7d557e5f3bb2c72d42525956526f"
BASE_TREE = "e2c87c9dc7ec274bc22013bc1159aff46bae12aa"
EXPRESSION_SHA256 = "646e9860afcf5efd962b6f69c9c2825220f23418d05f7675490b783e63afe209"
DENOMINATOR_SHA256 = "40ff944c9434231f2656a60ff306e27b69ef6fe302df8dc1bd56f89d314a8f15"
VALIDATION_RECEIPT_SHA256 = "670c21381395479ce69951bf27273b0fdb772f592ca77d5b41fa04fb58c3544e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M0822-ROOT",
    "M0822-S-TARGET",
    "M0822-S-BOUNDARY",
    "M0822-S-FOUNDATION",
    "M0822-T-ASSEMBLE",
    "M0822-T-ATTAINMENT",
    "M0822-C-STAR",
    "M0822-L-STAR-IMAGE",
    "M0822-L-STAR-INTERSECTING",
    "M0822-L-STAR-SIZED",
    "M0822-L-STAR-CARD",
    "M0822-L-GROUND-ELEMENT",
    "M0822-T-UPPER-ADAPTER",
    "M0822-T-MATHLIB-EKR",
    "M0822-B-RZERO",
    "M0822-C-COMPLEMENTS",
    "M0822-L-SHADOW-DISJOINT",
    "M0822-L-COMPLEMENT-CARD",
    "M0822-L-COMPLEMENT-SIZED",
    "M0822-L-KK-LOVASZ",
    "M0822-L-BINOMIAL-CONTRADICTION",
    "M0822-L-SLICE-CARD",
    "M0822-X-SOURCE",
    "M0822-X-PROVENANCE",
    "M0822-X-TRUST",
    "M0822-X-READABLE",
    "M0822-X-WORKFLOW",
]
MACHINE_IDS = [
    "M0822-ROOT",
    "M0822-T-ASSEMBLE",
    "M0822-T-ATTAINMENT",
    "M0822-C-STAR",
    "M0822-L-STAR-IMAGE",
    "M0822-L-STAR-INTERSECTING",
    "M0822-L-STAR-SIZED",
    "M0822-L-STAR-CARD",
    "M0822-L-GROUND-ELEMENT",
    "M0822-T-UPPER-ADAPTER",
    "M0822-T-MATHLIB-EKR",
]
COMPOSITION_DECLARATIONS = {
    "M0822-ROOT": "Stage1Instances.THM_M_0822.ObligationTree.rootOfExactAssembly",
    "M0822-T-ASSEMBLE": "Stage1Instances.THM_M_0822.ObligationTree.composeRoot",
    "M0822-T-ATTAINMENT": (
        "Stage1Instances.THM_M_0822.ObligationTree.attainment_of_starPackages"
    ),
    "M0822-C-STAR": (
        "Stage1Instances.THM_M_0822.ObligationTree.starConstruction_of_groundElement"
    ),
    "M0822-L-STAR-CARD": (
        "Stage1Instances.THM_M_0822.ObligationTree.starCard_of_image"
    ),
    "M0822-T-UPPER-ADAPTER": (
        "Stage1Instances.THM_M_0822.ObligationTree.upperBound_of_mathlibTerminal"
    ),
}
EXPECTED_INPUTS = {
    "Statement.lean": "b91d0fce7cd10a12585860b11af519cbe7496f555d04a751d5b4b6309309582d",
    "ObligationTree.lean": "2a1b89b25537b105eaba06fcf100fe6811b1f29470282ae24c469f4467322696",
    "Proof.lean": "1fe64b97e021ac3a3a817bf6d24af075ecdf5f7a61fc056b773d2bfc9e74cb01",
    "Validation.lean": "9654759e0988696850a6f0acd1db06ebef3a04a4895731125086032b49e3e72b",
    "instance.json": "76eb233e115a86db5d5916e4be794485273bc5a13f0714bda5ce9994dd2447d8",
    "task-dag.json": "7ee08eb684996c3f46a8f3c4bf2b066199a5a42faff56ec7975d066e6a5212b4",
    "statement.json": "07c9d2c949841df151a02d23b5bb568a64f299e8728910961070c93acec82b42",
    "anchor-audit.json": "380c1d6f3e10084bc82f24fca8a881a12fdc4794885b2e3f1ff7b5fd7985afee",
    "obligation-registry.json": "57d38c8d20bc4c8615707d52c7e30b18f0976af68cb1eed0a95a2e88de82e716",
    "typed-graphs.json": "2b4ad3930023606c4f25a07fa2c8c11908d396de19c54d4f116914e921a742e5",
    "proof-receipt.json": "a66afe73f88e58648a6fb6987a04aa82b8a30b0bff2adff3519ae065d98056c3",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-spec.json": "c5530e11c0c853b8939a8c3e33c65e457a3159084a3d04ef4876173d78bad439",
    "check_validation.sh": "58cd905918469d957423723ecddf2a3f10900897f8824108fcc9201673416a75",
    "source-statement-crosswalk.md": "b5aed58947ebbc75218aaea5c79e08a6285475bfb529134629937b965fdd52be",
}
EXPECTED_AUTHORITIES = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "84f0ce6372cd229a4336adbd5b4c23a1143788b31c5a536620b0468198f0d89d",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0eccdc572f7eeec6e0d3e0e318049acb3a8720b9cfdb07d2336b121b9401716f",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, authorities, and hashes agree",
    "PASS narrow Lean replay: exact maximum-value root is sorry-free at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED audit: accepted H1/M3/R4 stays open with no accepted receipt or obligation",
    "BLOCKED release assurance: clean cold/offline bundle, TCB/SBOM, and independent verifier are absent",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]


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
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).strip()


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    spec = load(HERE / "release-spec.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1380 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1380,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0822-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0822-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0822-VALIDATION"]

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in EXPECTED_AUTHORITIES.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0822.ErdosKoRadoMaximumTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert anchor["canonical_target"]["expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0822-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert len(registry["obligations"]) == len(INVENTORY_IDS) == 27
    assert len(graphs["composition_certificates"]) == 6
    assert {
        row["parent_obligation_id"]: row["declaration"]
        for row in graphs["composition_certificates"]
    } == COMPOSITION_DECLARATIONS
    assert graphs["unverified_decomposition_plans"] == []

    vector = {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == vector
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    # Release records rather than mutates this stale predecessor-owned merge inventory.
    assert not any("Proof.lean" in path for path in instance["public_merge_targets"])
    assert not any("Validation.lean" in path for path in instance["owned_artifacts"])

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert validation["receipt_id"] == decision["dependency"]["receipt_id"]
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["accepted_closed_obligation_ids"] == []
    assert validation["accepted_receipt_ids"] == []
    assert validation["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert validation["result"]["accepted_root_machine_debt"] == "M3"
    assert validation["result"]["accepted_root_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == "dependency.S56-M-0822-PROOF.master_acceptance"
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256

    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert receipt["accepted"] is receipt["content_addressed_release_evidence"] is False
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert set(decision["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert decision["known_failures"] == receipt["known_failures"]
    assert decision["root_vector"]["before"] == decision["root_vector"]["after"] == vector
    assert decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == vector
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-0822-VALIDATION.master_acceptance"
    )
    assert receipt["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["first_failed_dependency_gate"] == (
        "dependency.S56-M-0822-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    for gate in (
        "authoritative_instance_task_registry_graph_reconciliation",
        "node_specific_proof_and_composition_acceptance",
        "accepted_h0_primary_source_review",
        "independently_reviewed_r0_reconstruction",
        "accepted_foundation_and_complete_transitive_tcb",
        "complete_provenance_sbom_and_license_archive",
        "immutable_clean_cold_offline_reproduction",
        "deterministic_content_addressed_release_bundle",
        "distinct_signed_independent_runners",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_mutation_gates",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][gate] == "missing", gate

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == receipt["recipe"]["recipe_id"]
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "--unshare-net" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert set(receipt["release_artifacts"]) == {
        "check_release.py", "release-decision.json", "release-spec.json",
        "release-validation.md",
    }
    for name, expected in receipt["release_artifacts"].items():
        assert sha256(HERE / name) == expected, f"release artifact drifted: {name}"

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
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    replay = run(["bash", str(HERE / "check_validation.sh")])
    assert len(replay.encode("utf-8")) == 7921
    assert hashlib.sha256(replay.encode("utf-8")).hexdigest() == (
        "2de5d4df63c14cbafe24afac9f36d6f5bb1a37644e8b921ccc4f7bf363e686c4"
    )
    assert replay.count("Declarations are sorry-free!") == 14
    assert "declaration uses 'sorry'" not in replay
    assert "sorryAx" not in replay and "error:" not in replay
    root_declaration = "Stage1Instances.THM_M_0822.Proof.erdosKoRadoMaximum"
    assert printed_axioms(replay, "Finset.erdos_ko_rado") == EXPECTED_AXIOMS
    assert printed_axioms(replay, root_declaration) == EXPECTED_AXIOMS

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["output_summary"] == "\n".join(SUMMARY_LINES)
    assert packet["known_failures"] == decision["known_failures"]
    assert receipt["commands"] == packet["commands"]
    assert receipt["output_summary"] == SUMMARY_LINES
    assert all(
        set(row) == {"command", "exit_code", "result"}
        and isinstance(row["exit_code"], int)
        and isinstance(row["result"], str)
        and row["result"]
        for row in packet["commands"]
    )
    command_results = {row["command"]: row["exit_code"] for row in packet["commands"]}
    assert command_results[f"bash Stage1_Instances/{THEOREM}/check_validation.sh"] == 0
    assert command_results[
        f"python3 -I -B Stage1_Instances/{THEOREM}/check_release.py"
    ] == 0
    assert command_results[
        f"python3 -O -I -B Stage1_Instances/{THEOREM}/check_release.py"
    ] == 1

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H1, M3, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "This worker accepts no receipt", "release_grade=false",
    ):
        assert fragment in handoff, fragment
    for path in (
        HERE / "release-decision.json",
        HERE / "release-receipt.json",
        HERE / "release-validation.md",
    ):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
