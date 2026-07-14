#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0559-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import time


if not __debug__:
    raise SystemExit("check_release.py must run without Python optimization")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0559"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-0559-RELEASE"
THEOREM = "THM-M-0559"
BASE_REVISION = "a9274bb02f984e5c74d2c97339044c6db8eb14f9"
BASE_TREE = "c72a5af07dd4ab3f7088c516c74235e794a6de09"
STATEMENT_SHA256 = "f6db49c559ac718c96eb566d83e69748ae2d3fd0a1e95396465cbfa1e7328f1c"
STATEMENT_RECORD_SHA256 = "6d7925c9f37f5b2506f403b1fbda81a200e1e37edac1579a6c8bac1c0a4da1a4"
STATEMENT_OUTPUT_SHA256 = "ceed321b7234e4250269966bf4c6583e6f62b9305361da2ec910973e62c083be"
STATEMENT_OUTPUT_BYTES = 465
DENOMINATOR_SHA256 = "040c9f0d06a8432b0cf5768d43391f143d820754686514252ce484f53d3446fc"
PROOF_RECEIPT_SHA256 = "aba8729230ab01409ce50e61980fab266b0875aaf3adb11141d4b78d3279ec86"
VALIDATION_RECEIPT_SHA256 = "362cadbb071cd54accea1c024d3915b981ebb24b16de48beb401048bb63207dd"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_VECTOR = {"H": "H3", "M": "M4", "R": "R4"}
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
CUT = ["M0559-N-COMPONENTS", "M0559-T-FORWARD"]
LEAN_MODULES = ("Statement.lean", "Proof.lean", "Validation.lean")
SUMMARY_LINES = (
    "PASS S56-M-0559-RELEASE negative reconciliation",
    "PASS recorded pinned trust-zero checks: statement and partial component package elaborate sorry-free",
    "PASS observed axioms: propext, Classical.choice, Quot.sound",
    "BLOCKED dependency: S56-M-0559-VALIDATION is provisional, accepted=false, and not master-accepted",
    "BLOCKED assurance: exact root, AUDIT-Z, H0/R0, trust/provenance, cold/offline, independent-verifier, and bundle gates remain open",
    "verdict=blocked lifecycle=planned root_vector=H3/M4/R4 audit_complete=false theorem_complete=false",
)
EXPECTED_INPUTS = {
    "instance.json": "9230796550017250686ffc137f97e087936358a6cf82ef718b735001476f181e",
    "task-dag.json": "f21cda9d050bdceaf17e018d98b6da79edb0c5b346ba5ab46f616059fc22aa71",
    "statement.json": STATEMENT_RECORD_SHA256,
    "Statement.lean": STATEMENT_SHA256,
    "obligation-registry.json": "9a07086c9d49e00ff8100e18064d50578d253f5c6f6976cce5ae1e186bf6b9b6",
    "typed-graphs.json": "5cd995d027f4dd1dc5c54e7d6c0bf0c29985a50ab1a9701d21daa967fea2c411",
    "ObligationTree.lean": "471cea10d3c2d18632dbd7aafcb13e63fa7876eefef7e86359a7d2b1b1b6985c",
    "Proof.lean": "f0b1ec9ac606a8943e2aaaf711f2704caf628a33532d71709b0ff370f454b660",
    "Validation.lean": "fed617a1585f602720fab7065ffd9fc0fab8455557e08a965a5f98d5f87ebe84",
    "proof-receipt.json": PROOF_RECEIPT_SHA256,
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "source-statement-crosswalk.md": "7b818de32e06143405946b9fbf53658cd7e3a92b91386accb45979df0b942359",
    "README.md": "103d4dbe042194e34151b8d3123764a2c9bdec28bc9b7c6c3f55d7c0beeb5dd1",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "4f5335b6a1724a2856bb155e3147debd858e7fc1cf07d4b70c757e6515f5dd23",
    "Docs/Stage1_Blueprint_rev-5.6.md": "770174567b83623a839cf4f9a68c1a78524d516ecd1bc18e17c64130a48052e5",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
RELEASE_FILES = (
    "release-spec.json",
    "release-decision.json",
    "release-receipt.json",
    "release-phase.md",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    *{f"Stage1_Instances/{THEOREM}/{name}" for name in RELEASE_FILES},
    f"Stage1_Instances/{THEOREM}/check_release.py",
}
STARTED = time.monotonic()
TIMEOUT_SECONDS = 600.0


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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 180) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    assert remaining > 0, "release recipe exceeded its 600-second wall-clock bound"
    completed = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=min(timeout, remaining),
        check=False,
    )
    assert completed.returncode == 0, (argv, completed.returncode, completed.stdout)
    return completed.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        pair = source[index : index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                index += 2
            elif pair == "-/":
                depth -= 1
                index += 2
            else:
                index += 1
            continue
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if pair == "/-":
            depth = 1
            index += 2
        elif pair == "--":
            newline = source.find("\n", index + 2)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        else:
            output.append(char)
            if char == '"':
                in_string = True
            index += 1
    assert depth == 0 and not in_string
    return "".join(output)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    receipt = load(HERE / "release-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, name
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, name

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 607 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    release_node = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_node = next(
        row for row in execution["items"] if row["id"] == "S56-M-0559-VALIDATION"
    )
    assert release_node["phase"] == "release" and release_node["layer"] == 6
    assert release_node["state"] == "[ ]" and release_node["attempts"] == 0
    assert release_node["depends_on"] == ["S56-M-0559-VALIDATION"]
    assert release_node["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert validation_node["state"] == "[_]" and validation_node["attempts"] >= 1
    local_release = next(row for row in tasks["tasks"] if row["id"] == ITEM)
    assert local_release == {
        "id": ITEM,
        "depends_on": ["S56-M-0559-VALIDATION"],
        "state": "open",
    }

    assert instance["lifecycle"] == tasks["lifecycle"] == "planned"
    assert instance["root_vector"] == EXPECTED_VECTOR
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == [] and tasks["accepted_states"] == []
    assert all(row["state"] == "open" for row in tasks["tasks"])
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert statement["canonical_declaration"] == "Stage1Instances.THM_M_0559.WhiteheadTarget"
    assert statement["source_sha256"] == STATEMENT_SHA256
    assert statement["proof_claimed"] is statement["theorem_complete"] is False

    assert registry["root_obligation_id"] == "M0559-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert len(registry["obligations"]) == 18
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["remaining_root_cut_set"] == CUT
    assert closure["root_machine_debt"] == "M4"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M0559-ROOT")
    assert root_node["machine_debt"] == "M4" and root_node["evidence_ids"] == []
    assert root_node["source_crosswalk_id"] == "primary-source-node-map-pending"
    assert root_node["provenance_id"] == "none"

    assert sha256(HERE / "proof-receipt.json") == PROOF_RECEIPT_SHA256
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert proof["support_state"] == validation["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is validation["accepted"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert validation["verdict"] == "blocked" and validation["release_grade"] is False
    assert validation["content_addressed_release_evidence"] is False
    assert validation["accepted_receipt_ids"] == []
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["accepted_root_machine_debt"] == "M4"
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == "dependency.S56-M-0559-PROOF.master_acceptance"
    assert validation["remaining_root_cut_set"] == CUT

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["verdict"] == "blocked" and decision["release_grade"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector_before"] == decision["root_vector_after"] == EXPECTED_VECTOR
    assert decision["audit_complete"] is decision["theorem_complete"] is False
    assert decision["terminal_decisions"] == {
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }
    assert decision["release_accepted"] is False and decision["accepted_receipt_ids"] == []
    assert decision["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert decision["dependency"]["accepted"] is False
    assert decision["dependency"]["master_accepted"] is False
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_open_theorem_gate"]["gate_id"] == "M0559-N-COMPONENTS-KERNEL-CLOSURE"
    assert decision["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert decision["remaining_root_cut_set"] == CUT
    replay = decision["historical_validation_recipe_replay"]
    assert replay["attempted"] is True and replay["exit_code"] == 1
    assert replay["classification"] == "not_currently_replayable_nonrelease_historical_receipt"
    assert replay["first_error"] == "historical base revision mismatch at current HEAD"
    assert replay["base_revision"] == validation["base_revision"]
    assert replay["current_revision"] == BASE_REVISION
    for key, value in decision["evidence_reconciliation"].items():
        if key.endswith("_accepted") or key.endswith("_closure") or key in {
            "authoritative_instance_reconciled",
            "immutable_clean_release_input",
            "cold_empty_cache_offline_replay",
            "sbom_license_offline_archive_closure",
            "two_independent_signed_runner_attestations",
            "independently_implemented_minimal_release_verifier",
            "protected_ci_and_adversarial_gates",
            "deterministic_content_addressed_release_bundle",
            "master_acceptance",
        }:
            assert value is False, key

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "no_network_operation"
    assert "does not provision a network namespace" in spec["network_enforcement"]
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b|\bextern[ \t]+",
        flags=re.MULTILINE,
    )
    for name in LEAN_MODULES:
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = source.replace("#print sorries", "")
        assert prohibited.search(source) is None, name

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["master_acceptance"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["canonical_target"]["statement_source_sha256"] == STATEMENT_SHA256
    assert receipt["canonical_target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["recipe"] == spec
    assert receipt["inputs"]["release-spec.json"] == sha256(HERE / "release-spec.json")
    assert receipt["inputs"]["release-decision.json"] == sha256(HERE / "release-decision.json")
    assert receipt["inputs"]["check_release.py"] == sha256(HERE / "check_release.py")
    assert receipt["inputs"]["release-phase.md"] == sha256(HERE / "release-phase.md")
    result = receipt["result"]
    assert result["exit_code"] == 0 and result["verdict"] == "blocked"
    assert result["accepted_root_vector_before"] == result["accepted_root_vector_after"] == EXPECTED_VECTOR
    assert result["fresh_narrow_kernel_replay"] == "provisional_pass_recorded_before_release_checker"
    assert set(result["observed_axioms"]) == EXPECTED_AXIOMS
    assert result["accepted_root_closed"] is result["audit_complete"] is result["theorem_complete"] is False
    assert result["accepted_receipt_ids"] == []
    stdout_bytes = ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
    assert result["semantic_output_sha256"] == hashlib.sha256(stdout_bytes).hexdigest()
    assert result["stdout_bytes"] == len(stdout_bytes)
    assert result["statement_output_sha256"] == STATEMENT_OUTPUT_SHA256
    assert result["proof_output_sha256"] == validation["result"]["proof_output_sha256"]
    assert result["differential_output_sha256"] == validation["result"]["differential_output_sha256"]

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"] == decision["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    status_rows = [line for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"]
    assert {line[3:] for line in status_rows} == CHANGED_PATHS, status_rows
    assert all(line.startswith("?? ") for line in status_rows), status_rows
    assert git("diff", "--", str(HERE), str(ROOT / ".stage1-worker-selftest.json")) == ""
    assert git("diff", "--cached", "--", str(HERE), str(ROOT / ".stage1-worker-selftest.json")) == ""
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for name in RELEASE_FILES:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
