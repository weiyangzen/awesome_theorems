#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1553-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1553"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1553-RELEASE"
THEOREM = "THM-M-1553"
BASE_REVISION = "8c4a58ee73da7fa8dce7a9f9bfcc0ec5fd713588"
BASE_TREE = "3fa6104e948efe18f95dcfc23e9d2bf7f3dad150"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "ef5d4bb909f3eba6d2a347e8bad055e3a4a08402beb725499259bb9bf1a9c3bc"
DENOMINATOR_SHA256 = "553f66664b7a640a7e299ac12a65bfcf668173fbfb556f179614ae1dd4fbfed1"
EXPECTED_INPUTS = {
    "Statement.lean": "d5e88315d8d721409648fd87cbdfa08d6774567e73218a24040f4bda13670c32",
    "ObligationTree.lean": "20678d4d4da4c2b395762568edcd44699f6cb888348f1300da168eb6d11cd031",
    "ProofLemmas.lean": "f7eaf88193e7d1af86e9871ff975344e4bb49d614714bb77dee5d4c48e3e6cb2",
    "Proof.lean": "a1f1de80b12de4d124157474193d1199f33a5a54e57e90fc123e5bc365dfd8ec",
    "Validation.lean": "549e596fa71279a1ebd9fbbd1d71ea4d1a71775dcf3df234d926ce3a17365c01",
    "instance.json": "8306ed1c117d782c96ae38220ecf6ec263123dc6b4ce5f0f6d074f7b0069c149",
    "task-dag.json": "8b6d1c1e7923d6f1353f46d9f84cc826bd47895f03df4ab4695c756da5a1104b",
    "statement.json": "1317dfdae0ce90254dbd71249e7c684db25fdb10a0c9323dd1689fa4d1075bcb",
    "anchor-audit.json": "dcaa52f18c97f048251edfca4bf39b65b4a938c0b84231dc02a683afdec6c123",
    "obligation-registry.json": "216b591a11f219bbf32aafcae6d580d21cc777cf7edd55ca4af4c1f3d47556fc",
    "typed-graphs.json": "4c522e9ca5de8746f483e4ec522ee619eb71fa6633fe7a98d0e278dd0e24489e",
    "proof-receipt.json": "e7f31fe00fc47c7c5128c65e7d7a1ba70eb0a96d512a4ee21887adf49c1bdf6a",
    "validation-spec.json": "3312845aa86b644ec246d713d352ae6d31b89da16f078490a3853be0ed943d72",
    "validation-receipt.json": "476aa7ed8f832850bf80ffb91a969ea5d3230d486fe6c7aab25d68ed8ffda12c",
    "check_validation.py": "df8294095674dd861545a968b927bc488a8885147bc1aae6dfad35d9035d7a4d",
    "check_validation.sh": "8cabc62bbf986f506f80a9c91a64ed69c40b19f2562d998e36d2870ec8cdd3f6",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MACHINE_IDS = [
    "M1553-ROOT", "M1553-S-CONTEXT", "M1553-N-HIROTA",
    "M1553-N-TRANSFORM", "M1553-L-REGULARITY", "M1553-L-LOG",
    "M1553-L-MIXED", "M1553-B-POLYNOMIAL", "M1553-T-ZERO",
    "M1553-T-ASSEMBLE", "M1553-S-BOUNDARY",
]
INVENTORY_IDS = MACHINE_IDS + [
    "M1553-X-SOURCE", "M1553-X-PROVENANCE", "M1553-X-TRUST",
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
    "PASS recorded current-turn Lean replay: exact roots are sorry-free with exactly propext, Classical.choice, and Quot.sound",
    "PASS fail-closed state: lifecycle planned; accepted root H3/M4/R4; accepted receipts 0",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted",
    "BLOCKED immutable input, cold/offline, source/readability, trust, and independent release gates",
    "verdict=blocked audit_complete=false theorem_complete=false",
)


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=240, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions (no -O/PYTHONOPTIMIZE)")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    graphs = load(HERE / "typed-graphs.json")
    registry = load(HERE / "obligation-registry.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 212
    assert target["lifecycle_mode"] == "planned"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1553-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 212,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1553-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]"
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-1553-VALIDATION"]

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["execution_rank"] == 212 and decision["intent"] == "release"
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]"
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-1553-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"], validation["receipt_id"],
    ]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 240 and spec["network_policy"] == "denied"
    assert "Bubblewrap with --unshare-net" in spec["network_enforcement"]
    assert "separately recorded current-turn run" in spec["network_enforcement"]
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["depends_on"] == ["S56-M-1553-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["verdict"] == "blocked"
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["current_turn_separately_replayed_obligation_ids"] == MACHINE_IDS
    assert receipt["accepted_receipt_ids"] == []
    for name, expected in receipt["input_bindings"].items():
        path = ROOT / name if name.startswith(".") or name.startswith("Stage1_") else LEAN_ROOT / name
        assert sha256(path) == expected, f"receipt input drifted: {name}"
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H3", "M4", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False and decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    receipt_result = receipt["result"]
    assert receipt_result["verdict"] == "blocked"
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == [
        "H3", "M4", "R4",
    ]
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["release_accepted"] is False
    assert receipt_result["accepted_receipt_ids"] == []
    assert receipt_result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt_result["next_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["changed_paths"] == decision["changed_paths"]

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H3", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False
    assert boundary["remaining_root_cut_set"] == ["M1553-B-POLYNOMIAL", "M1553-T-ZERO"]
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["result"]["root_machine_proof_body_present"] is True
    validation_result = validation["result"]
    assert validation_result["exact_root_kernel_replay"] == "provisional_pass"
    assert validation_result["accepted_root_machine_debt"] == "M3"
    assert validation_result["accepted_root_closed"] is False
    assert validation_result["hermetic_cold_offline_replay"] == "fail_closed"
    assert validation_result["independent_distinct_runner"] == "fail_closed"
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "accepted_exact_root_kernel_closure", "authoritative_graph_reconciled",
        "audit_z_accepted", "pinpoint_h0_review", "independent_r0_review",
        "complete_provenance_foundation_tcb_closure", "immutable_clean_release_input",
        "hermetic_cold_offline_replay", "sbom_license_archive_closure",
        "independent_clean_runner_attestations", "independently_implemented_minimal_verifier",
        "protected_ci_and_mutation_gates", "deterministic_release_bundle", "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["accepted_closed_obligations"] == []
    cut_set = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "S56-M-1553-VALIDATION", "H0 primary-source", "R0 node-anchored",
        "AUDIT-Z", "empty-cache network-denied cold build", "two signed attestations",
        "minimal release verifier", "deterministic content-addressed release bundle",
    ):
        assert fragment in cut_set, fragment

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "ProofLemmas.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = re.sub(r"^#print sorries .*?$", "", source, flags=re.MULTILINE)
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    # The current release turn already ran the narrow script successfully before
    # writing these artifacts. Bind that run to the integrated validation receipt;
    # the shared canonical cache is concurrently mutable infrastructure and is not
    # rerun here as if it were independent or release-grade evidence.
    assert validation["execution"]["exit_code"] == 0
    assert validation["result"]["network_isolated_lean_replay"] == "pass"
    assert validation["result"]["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound",
    ]
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(decision["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    replay_command = next(
        command for command in packet["commands"]
        if command["argv"] == ["bash", f"Stage1_Instances/{THEOREM}/check_validation.sh"]
    )
    assert replay_command["exit_code"] == 0
    assert replay_command["output_summary"] == (
        "Network-isolated temporary-directory Lean replay passed; exact proof and "
        "differential roots were sorry-free with exactly propext, Classical.choice, "
        "and Quot.sound."
    )
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H3, M4, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "This worker accepts no receipt", "release_grade=false",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
