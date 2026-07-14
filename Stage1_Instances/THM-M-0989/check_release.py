#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0989-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0989"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0989-RELEASE"
THEOREM = "THM-M-0989"
BASE_REVISION = "d9006cb9119e9419f99f143c24edb5b15d0569d8"
BASE_TREE = "496fab16aa95efde99cc3dc2e71b90779d34248b"
VALIDATION_BASE = "64ac616628d97140f9ca64eff0298e51d7f4e9ff"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
DENOMINATOR = "c5d0b41c35c0759e11055611925021d6c2e38fc251da666e8f3afe238eccdc15"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
SUMMARY_LINES = (
    "PASS S56-M-0989-RELEASE truthful negative reconciliation",
    "PASS exact frozen statement/root and same-worker final composition replayed",
    "PASS 25 axiom reports; five sorry-free reports; closure 53251/1748 clean",
    "BLOCKED dependency.S56-M-0989-VALIDATION.master_acceptance",
    "BLOCKED stale canonical fingerprint, graph, public vector, H0/R0, provenance/TCB",
    "BLOCKED S56-10.6-HERMETIC-COLD-BUILD and independent verification",
    "AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUBPROCESS_ENV = {
    "HOME": os.environ.get("HOME", ""),
    "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
    "LANG": "C",
    "LC_ALL": "C",
    "NO_COLOR": "1",
    "TZ": "UTC",
}

if not __debug__:
    raise RuntimeError("release checker requires Python assertions")


def load(path: Path) -> dict:
    def no_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates
    )
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 600
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        env=SUBPROCESS_ENV,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


def run_ok(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> str:
    result = run(argv, cwd=cwd, timeout=timeout)
    assert result.returncode == 0, (argv, result.returncode, result.stdout)
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run_ok(["git", *args], cwd=cwd).strip()


def without_lean_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        char = source[index]
        pair = source[index:index + 2]
        if depth:
            if pair == "/-":
                depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif pair == "/-":
            depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            while index < len(source) and source[index] != "\n":
                output.append(" ")
                index += 1
        else:
            output.append(char)
            if char == '"':
                in_string = True
            index += 1
    assert depth == 0 and not in_string
    return "".join(output)


def assert_source_hygiene() -> None:
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean",
        "AnchorAudit.lean",
        "ObligationTree.lean",
        "Proof.lean",
        "ProdExp.lean",
        "CharFunBound.lean",
        "LindebergArray.lean",
        "Validation.lean",
    ):
        source = without_lean_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, name


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def changed_paths() -> set[str]:
    status = git("status", "--short", "--untracked-files=all")
    return {line[3:] for line in status.splitlines()}


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    intake = load(HERE / "intake.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation_spec = load(HERE / "validation-spec.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"]
        if row["id"] == "S56-M-0989-VALIDATION"
    )
    assert target["execution_rank"] == release_item["execution_rank"] == 269
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    assert release_item["phase"] == "release" and release_item["layer"] == 6
    assert release_item["state"] == "[ ]" and release_item["attempts"] == 0
    assert release_item["depends_on"] == [validation_item["id"]]
    assert release_item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    for name, expected in decision["reconciled_inputs"].items():
        assert sha256(HERE / name) == expected, f"target input drifted: {name}"
    for name, expected in decision["authority_inputs"].items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in receipt["input_bindings"].items():
        if name in {
            ".stage1-worker-selftest.json",
            f"Stage1_Instances/{THEOREM}/release-decision.json",
            f"Stage1_Instances/{THEOREM}/release-spec.json",
            f"Stage1_Instances/{THEOREM}/release-validation.md",
        }:
            assert expected == "excluded: provisional packet surface not hash-bound"
            continue
        assert sha256(ROOT / name) == expected, f"receipt input drifted: {name}"

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["execution_rank"] == 269 and decision["intent"] == "release"
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == validation_item["id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_base_revision"] == validation["base_revision"] == VALIDATION_BASE
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["content_addressed_release_evidence"] is False
    assert validation["content_addressed_release_evidence"] is False
    assert validation["verdict"] == "blocked"
    assert validation["first_failed_gate"] == (
        "dependency.S56-M-0989-PROOF.master_acceptance"
    )

    assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False
    assert intake["canonical_formal_target"]["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0989.Statement"
    )
    assert intake["canonical_formal_target"]["elaborated_expression_hash"] is None
    assert intake["root_vector"] == {
        "human": "H2", "machine": "M3", "readability": "R3"
    }
    assert registry["root_obligation_id"] == "M0989-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR
    assert graphs["registry_denominator_sha256"] == DENOMINATOR
    assert registry["frozen_denominators"]["inventory"] == spec[
        "reconciled_inventory_ids"
    ]
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == [
        "M0989-S-MEAS", "M0989-T-CHARFUN"
    ]
    root_node = next(
        node for node in graphs["nodes"] if node["obligation_id"] == "M0989-ROOT"
    )
    assert [
        root_node["human_debt"], root_node["machine_debt"],
        root_node["readability_debt"],
    ] == ["H2", "M3", "R4"]
    assert root_node["evidence_ids"] == []
    assert proof["support_state"] == validation["support_state"]
    assert proof["accepted"] is False
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["result"]["axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert validation["result"]["root_closed_locally"] is True
    assert validation["result"]["accepted_root_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["accepted_closed_obligation_ids"] == []

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "."
    assert spec["env_allowlist"] == {
        "HOME": "inherited only for pinned elan/lake discovery",
        "PATH": "inherited only for pinned Lean/Lake, Python, Git, Bash, and Bubblewrap discovery",
        "LANG": "C",
        "LC_ALL": "C",
        "NO_COLOR": "1",
        "TZ": "UTC",
    }
    assert spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied"
    assert spec["network_policy_enforced"] is False
    assert spec["network_enforcement"].startswith(
        "The outer Python reconciliation performs only local"
    )
    assert spec["expected_exit"] == 0
    assert spec["expected_outputs"] == [
        {
            "path_or_stream": "stdout",
            "semantic_hash_policy": "exact seven-line PASS/BLOCKED release-decision summary",
        }
    ]
    assert set(spec["covered_obligation_ids"]) < set(spec["reconciled_inventory_ids"])
    assert receipt["recipe"]["recipe_id"] == spec["recipe_id"]
    for key in (
        "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "network_policy_enforced",
        "expected_exit", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0989-VALIDATION"]
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["master_accepted"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["verdict"] == "blocked"
    assert receipt["canonical_target"] == "Stage1Instances.THM_M_0989.Statement"
    assert receipt["canonical_target_expression_sha256"] is None
    assert receipt["registry_denominator_sha256"] == DENOMINATOR
    assert receipt["canonical_obligation_ids"] == spec["reconciled_inventory_ids"]
    assert receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["self_hash_boundary"].startswith(
        "The receipt excludes four provisional packet surfaces"
    )
    assert receipt["dependency_receipt"]["receipt_sha256"] == sha256(
        HERE / "validation-receipt.json"
    )
    assert receipt["dependency_receipt"]["master_accepted"] is False
    assert receipt["freshness"]["review_due"] and receipt["invalidation_inputs"]
    environment = receipt["environment"]
    assert environment["platform"] == "Linux 7.0.0-27-generic x86_64"
    assert environment["lean_toolchain"] == "leanprover/lean4:v4.29.0"
    assert environment["lean_commit"] == (
        "98dc76e3c0a9b856c9b98726b713fb04fab16740"
    )
    lean = Path(run_ok(["bash", "-lc", "cd Formalizations/Lean && lake env which lean"]).strip())
    assert sha256(lean) == environment["lean_executable_sha256"]
    assert sha256(Path("/usr/bin/python3")) == environment["python_executable_sha256"]
    assert sha256(Path("/usr/bin/bash")) == environment["bash_executable_sha256"]
    assert sha256(Path("/usr/bin/bwrap")) == environment["bubblewrap_executable_sha256"]
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["network_used"] is False
    assert environment["release_classification"] == "nonrelease worker evidence"

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == {
        "H": "H2", "M": "M3", "R": "R4"
    }
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_gate"]["dependency_gate_id"] == (
        "dependency.S56-M-0989-VALIDATION.master_acceptance"
    )
    assert result["nested_validation_first_failed_gate"]["gate_id"] == validation[
        "first_failed_gate"
    ]
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert result["authoritative_graph_remaining_cut_set"] == closure[
        "remaining_root_cut_set"
    ]
    receipt_result = receipt["result"]
    assert receipt_result["verdict"] == "blocked"
    assert receipt_result["lifecycle_before"] == receipt_result["lifecycle_after"] == (
        "planned"
    )
    assert receipt_result["root_vector_before"] == receipt_result[
        "root_vector_after"
    ] == {"H": "H2", "M": "M3", "R": "R4"}
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["accepted_receipt_ids"] == []

    reconciliation = decision["evidence_reconciliation"]
    for gate in (
        "validation_recorded_recipe_fresh_at_current_snapshot",
        "accepted_exact_root_kernel_closure",
        "authoritative_graph_fresh_after_proof",
        "authoritative_graph_root_closed",
        "public_root_vector_reconciled",
        "canonical_expression_fingerprint_present",
        "source_variant_fidelity_accepted",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "accepted_foundation_policy",
        "complete_transitive_provenance_tcb_closure",
        "immutable_clean_release_input",
        "whole_recipe_network_denial",
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
        "S56-M-0989-VALIDATION", "graph", "canonical elaborated-expression",
        "AUDIT-Z", "H0 pinpoint", "R0 node-anchored", "transitive declaration",
        "empty-cache network-denied cold build", "SBOM", "two signed attestations",
        "minimal release verifier", "deterministic content-addressed release bundle",
        "THEOREM-Z",
    ):
        assert fragment in cut_set, fragment

    assert validation_spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    checker_source = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert VALIDATION_BASE in checker_source
    assert '.stage1-worker-selftest.json' in checker_source
    stale = run(validation_spec["argv"], timeout=120)
    assert stale.returncode != 0, "snapshot-bound validation recipe unexpectedly passed"
    assert "assert git(\"rev-parse\", \"HEAD\") == BASE_REVISION" in stale.stdout
    assert "AssertionError" in stale.stdout

    assert MATHLIB.is_dir() and (LEAN_ROOT / ".lake").is_symlink()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--short", cwd=MATHLIB) == ""
    assert_source_hygiene()
    replay = run(["bash", f"Stage1_Instances/{THEOREM}/check_validation.sh"])
    assert replay.returncode == 0, replay.stdout
    assert replay.stdout.count("Declarations are sorry-free!") == 5
    axiom_reports = re.findall(
        r"depends on axioms:\s*\[(.*?)]", replay.stdout, flags=re.DOTALL
    )
    assert len(axiom_reports) == 25, len(axiom_reports)
    for report in axiom_reports:
        assert {part.strip() for part in report.split(",") if part.strip()} == (
            EXPECTED_AXIOMS
        )
    for marker in (
        "VALIDATION_CLOSURE declarations=53251 modules=1748",
        "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]",
        "VALIDATION_CLOSURE bodyless_nonaxioms=[]",
        "VALIDATION_CLOSURE unsafe=[]",
        "PASS THM-M-0989 network-isolated validation",
    ):
        assert marker in replay.stdout, marker

    expected_stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["recipe"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout.encode("utf-8")
    ).hexdigest()
    assert receipt["recipe"]["raw_combined_log_sha256"] is None
    assert "release-grade" in receipt["recipe"]["raw_log_retention_boundary"]

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    assert all(
        isinstance(command, dict)
        and isinstance(command.get("argv"), list)
        and isinstance(command.get("exit_code"), int)
        for command in packet["commands"]
    )
    assert changed_paths() == CHANGED_PATHS | {"Formalizations/Lean/.lake"}

    for path in (
        ROOT / ".stage1-worker-selftest.json",
        HERE / "check_release.py",
        HERE / "release-decision.json",
        HERE / "release-receipt.json",
        HERE / "release-spec.json",
        HERE / "release-validation.md",
    ):
        assert_text_hygiene(path)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
