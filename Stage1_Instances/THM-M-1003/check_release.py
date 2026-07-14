#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1003-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


if not __debug__ or sys.flags.optimize:
    raise RuntimeError("release checker requires Python assertions")

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1003"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1003-RELEASE"
THEOREM = "THM-M-1003"
BASE_REVISION = "df73b636b3b854e8f045eff38bac636559fcbd23"
BASE_TREE = "05ae7157bcd52673b3ebf1a150e348500c1b55e4"
VALIDATION_BASE = "d3d4bc991fae237427b8ac391bbe701dca8f2af2"
EXPRESSION_SHA256 = "ead76891696316502f96466e97e0ec725b72cb1f2dfdc6d8afa4e405e79b8e9f"
DENOMINATOR_SHA256 = "d44a39b4a9b24a0cce89719cf41820d368483961dc0c2c624423e82136092b3c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_REPLAY = [
    "PASS THM-M-1003 network-isolated trust-zero kernel replay",
    "PASS exact proof/composition/type probe: propext, Classical.choice, Quot.sound",
    "PASS transitive sorry check: all proof declarations and exact-type probe are sorry-free",
]
SUMMARY_LINES = [
    "PASS S56-M-1003-RELEASE truthful negative reconciliation",
    "PASS exact frozen root/composition/type probe replayed under network isolation and trust zero",
    "PASS all proof declarations sorry-free; axioms exactly propext, Classical.choice, Quot.sound",
    "BLOCKED dependency.S56-M-1003-VALIDATION.master_acceptance",
    "BLOCKED H0/R0, foundation, complete provenance/TCB/SBOM, and authoritative reconciliation",
    "BLOCKED S56-10.6-HERMETIC-COLD-BUILD and independent verification",
    "AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]",
]
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


def load(path: Path) -> dict:
    def no_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

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


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def source_without_comments(source: str) -> str:
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
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = re.sub(r"^#print sorries .*?$", "", source, flags=re.MULTILINE)
        assert prohibited.search(source) is None, name


def actual_changed_paths() -> set[str]:
    status = git("status", "--short", "--untracked-files=all")
    return {line[3:] for line in status.splitlines()}


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation_spec = load(HERE / "validation-spec.json")
    validation = load(HERE / "validation-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"]
        if row["id"] == "S56-M-1003-VALIDATION"
    )
    assert target["execution_rank"] == release_item["execution_rank"] == 283
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 283,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1003-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    for name, expected in decision["reconciled_inputs"].items():
        assert sha256(HERE / name) == expected, f"target input drifted: {name}"
    for name, expected in decision["authority_inputs"].items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"

    assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False
    assert intake["root_vector"] == {
        "human": "H3", "machine": "M3", "readability": "R3"
    }
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1003.LpMartingaleConvergenceTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M1003-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    inventory = registry["frozen_denominators"]["inventory"]
    assert spec["covered_obligation_ids"] == inventory
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is False
    assert closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == [
        "M1003-T-CANDIDATE", "M1003-T-SAME-EXPONENT"
    ]
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1003-ROOT")
    assert [root["human_debt"], root["machine_debt"], root["readability_debt"]] == [
        "H3", "M4", "R3"
    ]
    assert root["evidence_ids"] == []

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False and proof["content_addressed"] is False
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert set(proof["result"]["axioms"]) == EXPECTED_AXIOMS
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["theorem_complete"] is False

    assert validation["item_id"] == validation_item["id"]
    assert validation["receipt_id"] == decision["dependency"]["receipt_id"]
    assert sha256(HERE / "validation-receipt.json") == decision["dependency"]["receipt_sha256"]
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["content_addressed_release_evidence"] is False
    assert validation["accepted_receipt_ids"] == []
    assert validation["result"]["root_kernel_closed_locally"] is True
    assert validation["result"]["accepted_root_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == (
        "dependency.S56-M-1003-PROOF.master_acceptance"
    )

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["recorded_recipe_current_snapshot_replayable"] is False

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    vector = {"H": "H3", "M": "M4", "R": "R3"}
    assert result["root_vector_before"] == result["root_vector_after"] == vector
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_gate"]["dependency_gate_id"] == (
        "dependency.S56-M-1003-VALIDATION.master_acceptance"
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

    reconciliation = decision["evidence_reconciliation"]
    false_gates = (
        "validation_recorded_recipe_current_snapshot_replayable",
        "accepted_exact_root_m0_l_e0",
        "authoritative_graph_fresh_after_proof",
        "authoritative_graph_root_closed",
        "authoritative_state_reconciled",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "accepted_foundation_profile",
        "complete_transitive_provenance_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    )
    assert all(reconciliation[gate] is False for gate in false_gates)
    assert reconciliation["accepted_closed_obligation_ids"] == []
    cut = "\n".join(result["remaining_release_cut_set"])
    for fragment in (
        "S56-M-1003-VALIDATION", "graph", "AUDIT-Z", "H0 pinpoint", "R0 node-anchored",
        "transitive declaration", "empty-cache network-denied cold build", "SBOM",
        "two signed attestations", "minimal release verifier",
        "deterministic content-addressed release bundle", "THEOREM-Z",
    ):
        assert fragment in cut, fragment

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied"
    assert spec["network_policy_enforced"] is False and spec["expected_exit"] == 0

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-1003-VALIDATION"]
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["master_accepted"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["verdict"] == "blocked"
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["canonical_obligation_ids"] == inventory
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["known_failures"] == decision["known_failures"]
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["result"]["root_vector_before"] == receipt["result"][
        "root_vector_after"
    ] == vector
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["accepted_receipt_ids"] == []
    assert receipt["dependency_receipt"]["receipt_sha256"] == sha256(
        HERE / "validation-receipt.json"
    )
    assert receipt["freshness"]["review_due"] and receipt["invalidation_inputs"]

    assert MATHLIB.is_dir() and (LEAN_ROOT / ".lake").is_symlink()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--short", cwd=MATHLIB) == ""
    assert_source_hygiene()

    assert validation_spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    validation_checker = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert VALIDATION_BASE in validation_checker
    assert '.stage1-worker-selftest.json' in validation_checker
    stale = run(validation_spec["argv"], timeout=120)
    assert stale.returncode != 0, "snapshot-bound validation recipe unexpectedly passed"
    assert "assert git(\"rev-parse\", \"HEAD\") == BASE_REVISION" in stale.stdout
    assert "AssertionError" in stale.stdout

    replay = run(["bash", f"Stage1_Instances/{THEOREM}/check_validation.sh"])
    assert replay.returncode == 0, replay.stdout
    assert replay.stdout.splitlines() == EXPECTED_REPLAY

    expected_stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["recipe"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout.encode("utf-8")
    ).hexdigest()
    assert receipt["recipe"]["raw_combined_log_sha256"] is None

    assert packet == {
        "item_id": ITEM,
        "changed_paths": receipt["changed_paths"],
        "commands": receipt["worker_commands"],
        "output_summary": "\n".join(SUMMARY_LINES),
        "base_revision": BASE_REVISION,
        "known_failures": receipt["known_failures"],
        "state": "[_]",
    }
    assert actual_changed_paths() == CHANGED_PATHS | {"Formalizations/Lean/.lake"}
    for path in CHANGED_PATHS:
        assert_text_hygiene(ROOT / path)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
