#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1055-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1055"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1055-RELEASE"
THEOREM = "THM-M-1055"
BASE_REVISION = "958a8abe91875e70c6b46520fa67f2196173944b"
BASE_TREE = "74102362c673fa27361249b1eeee4109d0feb845"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
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
    "Statement.lean": "a4caeaa6d5e09ea935d38a9b8e202854a43d430fe365368e78e2027d49dc2625",
    "AnchorAudit.lean": "ad160b9d5d0beb7f1f866348173adb90d0d5ccbdb565ba5a5fd42e4358693075",
    "ObligationTree.lean": "75b73aeebcb73409794ffb0d7ac6f122288d8d28028fcf9d0b26ecdb88737db1",
    "Proof.lean": "25af658d03f196715fa99272c03d10e47afcf26c278766bc9c8d28c665008437",
    "Validation.lean": "b082ab02013818d97b6373ccfb63eae275b8fb4a0b5d9c163dfb2dce839de117",
    "External/MaximalErgodic.lean": "b310154abc8a2407785ddc42dc3c1d4a1e45643cca47c9a2ff77fda7999298d4",
    "External/Birkhoff.lean": "de397519e3d49a8362270695ee860365ee1f6b41fd1d13829562d0cf752c0f12",
    "LICENSE.external": "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30",
    "instance.json": "5cdb721404fdddfac463a29374519c253fd2065a8ccdf25d1e23ee9f907786c4",
    "task-dag.json": "a2758c5fb91d5f9732f904f575205e4f88d83de872dbed9900ce75aaa74dac78",
    "statement.json": "64a7980cfce101b4f4b7a264c9cfe7ae5ae7d81ce18104e95770bf7b7bb70c46",
    "anchor-audit.json": "5654da75c72cc37c28ceb3e90dd393233e9cec9bb9788a59143c5d515ab72723",
    "obligation-registry.json": "7ff29f11d10bb462a6566d281aa5a4692eb4b7bd0ca0970ff77309e46c511905",
    "typed-graphs.json": "03a4eb677e478b6f97bb1fbd0d16a0134ab8a8b7e6e10f65e118a8d1995ec152",
    "proof-receipt.json": "ed13cb10e80920937a3cc6b106ba9260e272712c629852a85971089bc786046d",
    "validation-receipt.json": "69ffee75099fb8040f9ffc8e3b9b642bf6c5598a00180361d030c5e7ec262fb2",
    "validation-spec.json": "7248858fdad87dd1c678742cd58f0a3be764aea17a37629bb1bb8482d7ece358",
    "check_validation.py": "453de772783cfd4250e03e901f4da8390062ac40ec8fca48df8fb4b7fd606f4c",
    "check_proof.sh": "c941cfe644a277c34803ace37c7f5d0f64cedb7b9a5df715d088d64a0abf4349",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
INVENTORY_IDS = [
    "M1055-ROOT",
    "M1055-S-DEFINITIONS",
    "M1055-S-BOUNDARY",
    "M1055-S-FOUNDATION",
    "M1055-A-EXTERNAL-INTEGRATION",
    "M1055-L-POINTWISE-LIMIT",
    "M1055-L-LIMIT-MEASURABLE",
    "M1055-L-LIMIT-INVARIANT",
    "M1055-L-ERGODIC-CONSTANCY",
    "M1055-L-INTEGRAL-IDENTIFICATION",
    "M1055-T-INVARIANT-LIMIT",
    "M1055-T-ASSEMBLE",
    "M1055-X-SOURCE",
    "M1055-X-PROVENANCE",
]
MACHINE_IDS = INVENTORY_IDS[:12]
KERNEL_REPLAYED_IDS = [
    "M1055-ROOT",
    "M1055-T-INVARIANT-LIMIT",
    "M1055-T-ASSEMBLE",
]
EXPECTED_PACKET_OUTPUT_SUMMARY = (
    "The release phase self-tested a truthful negative reconciliation. Current "
    "narrow Lean evidence confirms a sorry-free exact Birkhoff root with exactly "
    "propext, Classical.choice, and Quot.sound, but validation remains provisional "
    "and unaccepted, the frozen external route and authoritative graph are "
    "unreconciled, and H0/R0, foundation/TCB/provenance, clean cold offline, "
    "independent-verifier, CI, deterministic-bundle, and master gates remain open. "
    "Lifecycle stays planned, accepted root H2/M4/R4, audit_complete=false, and "
    "theorem_complete=false."
)
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
    "PASS fail-closed state: lifecycle planned; accepted root H2/M4/R4; accepted receipts 0",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted",
    "BLOCKED route, audit, immutable input, cold/offline, trust, and independent release gates",
    "verdict=blocked audit_complete=false theorem_complete=false",
)
EXPECTED_STDOUT_SHA256 = "19266ec83c8001869e26aaa11125c8cfbe73455bacdf8918d8ab37626b1d0518"


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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> str:
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
        raise RuntimeError("release checker requires Python assertions (no -O)")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    graphs = load(HERE / "typed-graphs.json")
    registry = load(HERE / "obligation-registry.json")
    local_dag = load(HERE / "task-dag.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 247
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"]
        if row["id"] == "S56-M-1055-VALIDATION"
    )
    assert release_item["theorem_id"] == THEOREM
    assert release_item["execution_rank"] == 247
    assert release_item["phase"] == "release" and release_item["layer"] == 6
    assert release_item["state"] in {"[ ]", "[_]"}
    assert release_item["attempts"] in {0, 1}
    assert (release_item["state"] == "[ ]") == (release_item["attempts"] == 0)
    assert release_item["depends_on"] == ["S56-M-1055-VALIDATION"]
    assert release_item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert release_item["deliverable"] == (
        "Reconcile evidence and decide the exact theorem-completion verdict."
    )
    assert release_item["completion_gate"] == (
        "rev-5.6 node-specific receipt and master acceptance"
    )
    assert release_item["children"] == []
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-1055-VALIDATION"]
    assert local_dag["accepted_states"] == []

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["execution_rank"] == 247 and decision["intent"] == "release"
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]"
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-1055-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_base_revision"] == validation["base_revision"]
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"], validation["receipt_id"]
    ]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 600 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["kernel_replayed_obligation_ids"] == KERNEL_REPLAYED_IDS

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["depends_on"] == ["S56-M-1055-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["verdict"] == "blocked"
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["kernel_replayed_obligation_ids"] == KERNEL_REPLAYED_IDS
    assert receipt["accepted_receipt_ids"] == []
    environment = receipt["environment"]
    for key, expected in EXPECTED_EXECUTABLES.items():
        assert environment[key] == expected
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
    assert result["root_vector_before"] == result["root_vector_after"] == [
        "H2", "M4", "R4"
    ]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == (
        "S56-10.2-DEPENDENCY-ACCEPTANCE"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    receipt_result = receipt["result"]
    assert receipt_result["verdict"] == "blocked"
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == [
        "H2", "M4", "R4"
    ]
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["accepted_receipt_ids"] == []
    expected_stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert hashlib.sha256(expected_stdout.encode("utf-8")).hexdigest() == (
        EXPECTED_STDOUT_SHA256
    )
    assert receipt["output_evidence"] == {
        "expected_line_count": 6,
        "exit_code": 0,
        "stdout_sha256": EXPECTED_STDOUT_SHA256,
    }

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["remaining_root_cut_set"] == ["M1055-T-INVARIANT-LIMIT"]
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["frozen_graph_closed"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["frozen_proof_graph_cut_set"] == ["M1055-A-EXTERNAL-INTEGRATION"]
    assert proof["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    validation_result = validation["result"]
    assert validation_result["exact_root_kernel_closed"] is True
    assert validation_result["frozen_graph_closed"] is False
    assert validation_result["accepted_root_machine_debt"] == "M4"
    assert validation_result["accepted_closed_obligations"] == []
    assert validation_result["hermetic_release_gate"] == "fail_closed"
    assert validation_result["independent_distinct_runner_gate"] == "fail_closed"
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False
    assert validation["provenance"]["complete_transitive_declaration_and_source_origin_closure"] is False
    assert "lua-vr/pointwise-birkhoff@fc06094c" in validation["provenance"]["frozen_route"]
    assert validation["provenance"]["upstream_revision"] == (
        "ed3fa6b8a30594eeb791160563942ba115581aa0"
    )

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "validation_recipe_fresh_at_integrated_base",
        "accepted_exact_root_kernel_closure",
        "frozen_external_route_reconciled",
        "authoritative_graph_reconciled",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "accepted_foundation_policy",
        "complete_transitive_provenance_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_mutation_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["accepted_closed_obligations"] == []
    cut_set = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "S56-M-1055-VALIDATION",
        "M1055-A-EXTERNAL-INTEGRATION",
        "M1055-S-FOUNDATION",
        "M1055-X-PROVENANCE",
        "M1055-X-SOURCE",
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
    lean_names = (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
        "Validation.lean", "External/MaximalErgodic.lean", "External/Birkhoff.lean",
    )
    for name in lean_names:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap is required for network-denied replay"
    lean_path = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake_path = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean = Path(lean_path)
    lake = Path(lake_path)
    executables = {
        "lean_executable_sha256": lean,
        "lake_executable_sha256": lake,
        "python_executable_sha256": Path(sys.executable).resolve(),
        "git_executable_sha256": Path(shutil.which("git") or "").resolve(),
        "bash_executable_sha256": Path(shutil.which("bash") or "").resolve(),
        "bubblewrap_executable_sha256": Path(bwrap).resolve(),
    }
    for key, path in executables.items():
        assert sha256(path) == EXPECTED_EXECUTABLES[key], (key, path)
    with tempfile.TemporaryDirectory(prefix="m1055-release-replay-", dir="/tmp") as tmp:
        replay = run([
            bwrap,
            "--ro-bind", "/", "/",
            "--dev", "/dev",
            "--proc", "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--bind", str(LEAN_ROOT), str(LEAN_ROOT),
            "--bind", tmp, tmp,
            "--setenv", "TMPDIR", tmp,
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--chdir", str(ROOT),
            "bash", str(HERE / "check_proof.sh"),
        ])
    declarations = (
        "ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg",
        "ErgodicTheory.condExp_invariants_comp",
        "ErgodicTheory.ae_tendsto_orbit_div_atTop_zero",
        "ErgodicTheory.tendsto_birkhoffAverage_ae",
        "ErgodicTheory.tendsto_birkhoffAverage_ae_integral",
        "Stage1Instances.THM_M_1055.invariantLimitPackage_proof",
        "Stage1Instances.THM_M_1055.birkhoffErgodicTarget",
    )
    for declaration in declarations:
        assert printed_axioms(replay, declaration) == EXPECTED_AXIOMS, declaration
    assert replay.count("Declarations are sorry-free!") == 5
    assert "sorryAx" not in replay and "declaration uses 'sorry'" not in replay

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    assert packet["output_summary"] == EXPECTED_PACKET_OUTPUT_SUMMARY
    packet_results = {
        (tuple(row["argv"]), row["exit_code"])
        for row in packet["commands"]
    }
    for row in receipt["commands"]:
        assert (tuple(row["argv"]), row["exit_code"]) in packet_results
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["changed_paths"] == decision["changed_paths"] == packet["changed_paths"]
    status = git("status", "--short", "--untracked-files=all")
    assert not list(LEAN_ROOT.glob(".m1055-proof.*")), "stale proof replay directory"
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H2, M4, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "worker accepts no receipt", "`release_grade=false`",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
