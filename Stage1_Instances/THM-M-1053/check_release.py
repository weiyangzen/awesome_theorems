#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1053-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1053"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1053-RELEASE"
THEOREM = "THM-M-1053"
BASE_REVISION = "d3d4bc991fae237427b8ac391bbe701dca8f2af2"
BASE_TREE = "51d54892f625b3b42e3b0c2c6b3c8e173c4ad166"
EXPRESSION_SHA256 = "f4b06a49160cd083fa4cf1bb3b1ddfe1453dbcb1e521ff2c09ba5d3753a2e562"
DENOMINATOR_SHA256 = "125e28fed0cbce9e0cbffea0da90b047c35a770c90d3be2a82a42319b8606005"
PROOF_RECEIPT_SHA256 = "ca51b92704687406b5d5799220ec4f77665ab8b8afad8b7243bda290b6949b2d"
VALIDATION_RECEIPT_SHA256 = "4480223d344bf8611e94f5df1f10ed013d72a2c50f16c1009cc1175fa3ce1d1b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_VECTOR = {"H": "H2", "M": "M1", "R": "R4"}
GRAPH_CUT = ["M1053-T-GENERAL", "M1053-L-ERGODIC-IDENTIFICATION"]
CORRECTION_CUT = [
    "M1053-L-DENSE-CLASS.route-reconciliation",
    "M1053-L-ERGODIC-IDENTIFICATION.corrected-target",
]
LEAN_SOURCES = (
    "Statement.lean",
    "ObligationTree.lean",
    "MaximalErgodic.lean",
    "Birkhoff.lean",
    "Proof.lean",
    "Validation.lean",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}
SUMMARY_LINES = (
    "PASS S56-M-1053-RELEASE negative reconciliation",
    "PASS pinned trust-zero network-isolated replay: exact root and differential root elaborate sorry-free",
    "PASS observed axioms: propext, Classical.choice, Quot.sound",
    "BLOCKED dependency: S56-M-1053-VALIDATION is provisional and not master-accepted",
    "BLOCKED assurance: graph/H0/R0/trust/cold-offline/independent-verifier/bundle gates remain open",
    "verdict=blocked lifecycle=planned root_vector=H2/M1/R4 audit_complete=false theorem_complete=false",
)
STARTED = time.monotonic()
TIMEOUT_SECONDS = 900.0


if sys.flags.optimize:
    raise SystemExit("release check failed: Python optimization disables assertions")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    if remaining <= 0:
        raise TimeoutError("release recipe exceeded its 900-second wall-clock bound")
    completed = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            f"release check failed ({completed.returncode}): {argv!r}\n{completed.stdout}"
        )
    return completed.stdout


def run_isolated(argv: list[str]) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    if remaining <= 0:
        raise TimeoutError("release recipe exceeded its 900-second wall-clock bound")
    completed = subprocess.run(
        argv,
        cwd="/",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            f"isolated Lean check failed ({completed.returncode}): "
            f"{argv!r}\n{completed.stdout}"
        )
    return completed.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, declaration
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    receipt = load(HERE / "release-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 245
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    release_node = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_node = next(
        row for row in execution["items"] if row["id"] == "S56-M-1053-VALIDATION"
    )
    assert release_node["phase"] == "release" and release_node["layer"] == 6
    assert release_node["state"] == "[ ]" and release_node["attempts"] == 0
    assert release_node["depends_on"] == ["S56-M-1053-VALIDATION"]
    assert validation_node["state"] == "[_]" and validation_node["attempts"] == 1
    local_release = next(row for row in tasks["tasks"] if row["id"] == ITEM)
    assert local_release == {
        "id": ITEM,
        "depends_on": ["S56-M-1053-VALIDATION"],
        "state": "open",
    }

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == EXPECTED_VECTOR
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == []
    assert tasks["lifecycle"] == "planned" and tasks["accepted_states"] == []
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["remaining_root_cut_set"] == GRAPH_CUT

    assert sha256(HERE / "proof-receipt.json") == PROOF_RECEIPT_SHA256
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert proof["support_state"] == validation["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is validation["accepted"] is False
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["frozen_graph_closed"] is False
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["frozen_proof_graph_cut_set"] == [
        "M1053-L-DENSE-CLASS",
        "M1053-L-ERGODIC-IDENTIFICATION",
    ]
    assert validation["release_grade"] is False
    assert validation["content_addressed_release_evidence"] is False
    assert validation["accepted_closed_obligation_ids"] == []
    validation_result = validation["result"]
    assert validation_result["exact_root_kernel_replay"] == "provisional_pass"
    assert validation_result["differential_exact_root_replay"] == "provisional_pass_same_worker"
    assert validation_result["accepted_root_vector"] == EXPECTED_VECTOR
    assert validation_result["accepted_root_machine_debt"] == "M1"
    assert validation_result["accepted_root_closed"] is False
    assert validation_result["frozen_graph_cut_set"] == [
        "M1053-L-DENSE-CLASS",
        "M1053-L-ERGODIC-IDENTIFICATION",
    ]
    assert validation_result["foundation_and_complete_trust_closure"] == "fail_closed"
    assert validation_result["complete_provenance_closure"] == "fail_closed"
    assert validation_result["hermetic_cold_offline_replay"] == "fail_closed"
    assert validation_result["independent_distinct_runner"] == "fail_closed"
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["verdict"] == "blocked" and decision["release_grade"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector_before"] == decision["root_vector_after"] == EXPECTED_VECTOR
    assert decision["audit_complete"] is decision["theorem_complete"] is False
    assert decision["release_accepted"] is False and decision["accepted_receipt_ids"] == []
    assert decision["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert decision["dependency"]["master_accepted"] is False
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert decision["authoritative_graph_remaining_root_cut_set"] == GRAPH_CUT
    assert decision["proof_evidence_graph_correction_cut_set"] == CORRECTION_CUT
    assert decision["evidence_reconciliation"]["canonical_expression_sha256"] == EXPRESSION_SHA256
    assert decision["evidence_reconciliation"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    for key in (
        "authoritative_graph_reconciled",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "accepted_foundation_provenance_and_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_and_offline_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle",
        "public_projection_reconciled",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key
    cut_text = "\n".join(decision["remaining_theorem_completion_gates"])
    for fragment in (
        "master acceptance",
        "registry v2 or append-only correction",
        "instance, README, scope, and source-crosswalk reconciliation",
        "H0 pinpoint primary-source",
        "R0 structured reconstruction",
        "transitive declaration",
        "empty-cache network-denied cold build",
        "SBOM and license",
        "two agreeing signed attestations",
        "minimal release verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in cut_text, fragment

    for name, expected in decision["reconciled_inputs"].items():
        assert sha256(HERE / name) == expected, name
    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3",
        "-I",
        "-B",
        f"Stage1_Instances/{THEOREM}/check_release.py",
    ]
    assert spec["network_policy"] == "denied" and spec["timeout_seconds"] == 900
    assert "--unshare-net" in spec["network_enforcement"]
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in LEAN_SOURCES:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = re.sub(r"^#print sorries .*?$", "", source, flags=re.MULTILINE)
        assert prohibited.search(source) is None, name

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    bwrap = Path(os.path.realpath(shutil.which("bwrap") or ""))
    assert lean.is_file() and bwrap.is_file()
    with tempfile.TemporaryDirectory(prefix="m1053-release-", dir="/tmp") as name:
        temporary = Path(name).resolve()
        for source_name in LEAN_SOURCES:
            (temporary / source_name).write_bytes((HERE / source_name).read_bytes())
        base = [
            str(bwrap),
            "--ro-bind",
            "/",
            "/",
            "--bind",
            str(temporary),
            str(temporary),
            "--dev",
            "/dev",
            "--proc",
            "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--setenv",
            "LANG",
            "C.UTF-8",
            "--setenv",
            "LC_ALL",
            "C.UTF-8",
            "--setenv",
            "TZ",
            "UTC",
            "--chdir",
            str(temporary),
        ]
        statement_output = run_isolated(
            base
            + [
                "--setenv",
                "LEAN_PATH",
                lean_path,
                str(lean),
                "--trust=0",
                "-o",
                "Statement.olean",
                "Statement.lean",
            ]
        )
        module_path = f"{temporary}:{lean_path}"
        outputs: dict[str, str] = {}
        for module in ("ObligationTree",):
            outputs[module] = run_isolated(
                base
                + [
                    "--setenv",
                    "LEAN_PATH",
                    module_path,
                    str(lean),
                    "--trust=0",
                    "-o",
                    f"{module}.olean",
                    f"{module}.lean",
                ]
            )
        outputs["MaximalErgodic"] = run_isolated(
            base
            + [
                "--setenv",
                "LEAN_PATH",
                lean_path,
                str(lean),
                "--trust=0",
                "-o",
                "MaximalErgodic.olean",
                "MaximalErgodic.lean",
            ]
        )
        outputs["Birkhoff"] = run_isolated(
            base
            + [
                "--setenv",
                "LEAN_PATH",
                module_path,
                str(lean),
                "--trust=0",
                "-o",
                "Birkhoff.olean",
                "Birkhoff.lean",
            ]
        )
        proof_output = run_isolated(
            base
            + [
                "--setenv",
                "LEAN_PATH",
                module_path,
                str(lean),
                "--trust=0",
                "Proof.lean",
            ]
        )
        validation_output = run_isolated(
            base
            + [
                "--setenv",
                "LEAN_PATH",
                module_path,
                str(lean),
                "--trust=0",
                "Validation.lean",
            ]
        )

    assert "Stage1.THM_M_1053.StatementShape" in statement_output, statement_output
    combined = "".join(outputs.values()) + proof_output + validation_output
    assert "sorryAx" not in combined, combined
    proof_declarations = (
        "ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg",
        "ErgodicTheory.tendsto_birkhoffAverage_ae",
        "ErgodicTheory.tendsto_birkhoffAverage_ae_integral",
        "Stage1.THM_M_1053.generalInvariantLimitPackage_proof",
        "Stage1.THM_M_1053.statementShape_proof",
        "Stage1.THM_M_1053.not_ergodicLimitIdentificationPackage",
    )
    for declaration in proof_declarations:
        assert printed_axioms(proof_output, declaration) == EXPECTED_AXIOMS, proof_output
    validation_declarations = (
        "ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg",
        "ErgodicTheory.tendsto_birkhoffAverage_ae",
        "ErgodicTheory.tendsto_birkhoffAverage_ae_integral",
        "Stage1.THM_M_1053.Validation.differentialStatementShape",
    )
    for declaration in validation_declarations:
        assert printed_axioms(validation_output, declaration) == EXPECTED_AXIOMS, validation_output
    assert proof_output.count("Declarations are sorry-free!") == 6, proof_output
    assert validation_output.count("Declarations are sorry-free!") == 4, validation_output

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-1053-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["accepted_receipt_ids"] == []
    assert receipt["result"]["observed_axioms"] == [
        "propext",
        "Classical.choice",
        "Quot.sound",
    ]
    for input_name in (
        "release-decision.json",
        "release-spec.json",
        "check_release.py",
        "release-phase.md",
    ):
        assert receipt["inputs"][input_name] == sha256(HERE / input_name), input_name
    assert receipt["inputs"]["proof-receipt.json"] == PROOF_RECEIPT_SHA256
    assert receipt["inputs"]["validation-receipt.json"] == VALIDATION_RECEIPT_SHA256
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]" and set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (
        HERE / "release-decision.json",
        HERE / "release-receipt.json",
        HERE / "release-phase.md",
    ):
        public_text = path.read_text(encoding="utf-8")
        assert "/home/" not in public_text and ".cron/" not in public_text
        assert "theorem_complete=true" not in public_text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
