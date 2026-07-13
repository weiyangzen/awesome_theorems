#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1055-VALIDATION."""

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


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1055"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1055-VALIDATION"
THEOREM = "THM-M-1055"
BASE_REVISION = "67b1bf1758649d2be86775230c7d4bfe117ade2b"
BASE_TREE = "5f872831428a9d9805e61aad3868be443c29cef2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPRESSION_SHA256 = "8d7956f1f5f46ae435293eef17df7881f26d9c18fad6ac54c870e232cdb26181"
DENOMINATOR_SHA256 = "cb67895834a856b780f44cbcf8c3de106f574f5035d3003486181876fd382d06"
UPSTREAM_REVISION = "ed3fa6b8a30594eeb791160563942ba115581aa0"
UPSTREAM_ARCHIVE_SHA256 = "3c0ef177500430ab55950061cfd73991347f5336b5b3d5032ffe46ac56009a52"
EXPECTED_INPUTS = {
    "Statement.lean": "a4caeaa6d5e09ea935d38a9b8e202854a43d430fe365368e78e2027d49dc2625",
    "AnchorAudit.lean": "ad160b9d5d0beb7f1f866348173adb90d0d5ccbdb565ba5a5fd42e4358693075",
    "anchor-audit.json": "5654da75c72cc37c28ceb3e90dd393233e9cec9bb9788a59143c5d515ab72723",
    "statement.json": "64a7980cfce101b4f4b7a264c9cfe7ae5ae7d81ce18104e95770bf7b7bb70c46",
    "ObligationTree.lean": "75b73aeebcb73409794ffb0d7ac6f122288d8d28028fcf9d0b26ecdb88737db1",
    "obligation-registry.json": "7ff29f11d10bb462a6566d281aa5a4692eb4b7bd0ca0970ff77309e46c511905",
    "typed-graphs.json": "03a4eb677e478b6f97bb1fbd0d16a0134ab8a8b7e6e10f65e118a8d1995ec152",
    "validation-specs.json": "09b9e90025d3b5c1251b62c1c85c36eccbb26289b7753344eb4a42c5c34ecc2c",
    "instance.json": "5cdb721404fdddfac463a29374519c253fd2065a8ccdf25d1e23ee9f907786c4",
    "task-dag.json": "a2758c5fb91d5f9732f904f575205e4f88d83de872dbed9900ce75aaa74dac78",
    "Proof.lean": "25af658d03f196715fa99272c03d10e47afcf26c278766bc9c8d28c665008437",
    "proof-receipt.json": "ed13cb10e80920937a3cc6b106ba9260e272712c629852a85971089bc786046d",
    "External/MaximalErgodic.lean": "b310154abc8a2407785ddc42dc3c1d4a1e45643cca47c9a2ff77fda7999298d4",
    "External/Birkhoff.lean": "de397519e3d49a8362270695ee860365ee1f6b41fd1d13829562d0cf752c0f12",
    "LICENSE.external": "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30",
    "Validation.lean": "b082ab02013818d97b6373ccfb63eae275b8fb4a0b5d9c163dfb2dce839de117",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
MACHINE_IDS = {
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
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=900,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_axioms(output: str, declaration: str) -> None:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, (declaration, output)
    observed = {part.strip() for part in match.group(1).split(",")}
    assert observed == EXPECTED_AXIOMS, (declaration, observed)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 247,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1055-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    proof_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1055-PROOF"
    )
    assert proof_item["state"] == "[_]" and proof_item["attempts"] == 1
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task == {
        "id": ITEM,
        "depends_on": ["S56-M-1055-PROOF"],
        "state": "open",
    }

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert set(spec["covered_obligation_ids"]) == MACHINE_IDS

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    formal = statement["canonical_formal_target"]
    assert formal == {
        "backend": "lean4",
        "module": f"Stage1_Instances/{THEOREM}/Statement.lean",
        "declaration_or_expression": (
            "Stage1Instances.THM_M_1055.BirkhoffErgodicTarget"
        ),
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "statement_file_sha256": EXPECTED_INPUTS["Statement.lean"],
    }
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert set(registry["frozen_denominators"]["required_machine"]) == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["upstream"]["revision"] == UPSTREAM_REVISION
    assert proof_receipt["upstream"]["archive_sha256"] == UPSTREAM_ARCHIVE_SHA256
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["frozen_graph_closed"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["frozen_proof_graph_cut_set"] == [
        "M1055-A-EXTERNAL-INTEGRATION"
    ]
    assert proof_receipt["result"]["axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["remaining_root_cut_set"] == ["M1055-T-INVARIANT-LIMIT"]
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    external_node = next(
        node for node in graphs["nodes"]
        if node["obligation_id"] == "M1055-A-EXTERNAL-INTEGRATION"
    )
    assert "lua-vr/pointwise-birkhoff@fc06094c" in external_node["formal_target"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    source_names = (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
        "External/MaximalErgodic.lean", "External/Birkhoff.lean", "Validation.lean",
    )
    for name in source_names:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = (HERE / "Validation.lean").read_text(encoding="utf-8")
    for forbidden in (
        "import Proof", "import ObligationTree", "birkhoffErgodicTarget",
        "root_of_invariantLimitPackage", "invariantLimitPackage_proof",
    ):
        assert forbidden not in differential, forbidden
    assert "ErgodicTheory.tendsto_birkhoffAverage_ae_integral hT hf" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    bwrap = Path(shutil.which("bwrap") or "")
    assert bwrap.is_file(), "bubblewrap is required for network-denied Lean replay"
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()

    with tempfile.TemporaryDirectory(prefix="m1055-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in (
            "Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean",
        ):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        for name in ("MaximalErgodic.lean", "Birkhoff.lean"):
            (tmp / name).write_bytes((HERE / "External" / name).read_bytes())
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--setenv", "LANG", "C.UTF-8", "--setenv",
            "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC", "--chdir", str(tmp),
        ]
        statement_output = run(base + [
            "--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0",
            "-o", "Statement.olean", "Statement.lean",
        ])
        module_env = ["--setenv", "LEAN_PATH", f"{tmp}:{lean_path}"]
        obligation_output = run(base + module_env + [
            str(lean), "--trust=0", "-o", "ObligationTree.olean",
            "ObligationTree.lean",
        ])
        maximal_output = run(base + module_env + [
            str(lean), "--trust=0", "-o", "MaximalErgodic.olean",
            "MaximalErgodic.lean",
        ])
        birkhoff_output = run(base + module_env + [
            str(lean), "--trust=0", "-o", "Birkhoff.olean", "Birkhoff.lean",
        ])
        proof_output = run(base + module_env + [
            str(lean), "--trust=0", "Proof.lean",
        ])
        validation_output = run(base + module_env + [
            str(lean), "--trust=0", "Validation.lean",
        ])

    assert "BirkhoffErgodicTarget" in statement_output
    assert "sorryAx" not in (
        obligation_output + maximal_output + birkhoff_output + proof_output
        + validation_output
    )
    proof_declarations = (
        "ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg",
        "ErgodicTheory.condExp_invariants_comp",
        "ErgodicTheory.ae_tendsto_orbit_div_atTop_zero",
        "ErgodicTheory.tendsto_birkhoffAverage_ae",
        "ErgodicTheory.tendsto_birkhoffAverage_ae_integral",
        "Stage1Instances.THM_M_1055.invariantLimitPackage_proof",
        "Stage1Instances.THM_M_1055.birkhoffErgodicTarget",
    )
    for declaration in proof_declarations:
        assert_axioms(proof_output, declaration)
    validation_declarations = (
        "ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg",
        "ErgodicTheory.tendsto_birkhoffAverage_ae",
        "ErgodicTheory.tendsto_birkhoffAverage_ae_integral",
        "Stage1Instances.THM_M_1055.Validation.differentialBirkhoffErgodicTarget",
    )
    for declaration in validation_declarations:
        assert_axioms(validation_output, declaration)
    assert proof_output.count("Declarations are sorry-free!") == 5
    assert validation_output.count("Declarations are sorry-free!") == 4

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["release_grade"] is receipt["accepted"] is False
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["validation-spec.json"] == sha256(
        HERE / "validation-spec.json"
    )
    assert receipt["inputs"]["check_validation.py"] == sha256(
        HERE / "check_validation.py"
    )
    assert receipt["target"] == {
        "canonical_declaration": (
            "Stage1Instances.THM_M_1055.BirkhoffErgodicTarget"
        ),
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
        "exact_statement_delta": "none",
    }
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["python_executable_sha256"] == sha256(Path(sys.executable).resolve())
    assert environment["git_executable_sha256"] == sha256(
        Path(shutil.which("git") or "").resolve()
    )
    assert environment["bash_executable_sha256"] == sha256(
        Path(shutil.which("bash") or "").resolve()
    )
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap.resolve())
    assert environment["platform"] == f"{platform.system()} {platform.machine()}"
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    provenance = receipt["provenance"]
    assert provenance["upstream_revision"] == UPSTREAM_REVISION
    assert provenance["upstream_archive_sha256"] == UPSTREAM_ARCHIVE_SHA256
    assert provenance["maximal_ergodic_port_sha256"] == EXPECTED_INPUTS[
        "External/MaximalErgodic.lean"
    ]
    assert provenance["birkhoff_port_sha256"] == EXPECTED_INPUTS[
        "External/Birkhoff.lean"
    ]
    assert provenance["license_sha256"] == EXPECTED_INPUTS["LICENSE.external"]
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key]
    result = receipt["result"]
    assert result["exact_root_kernel_closed"] is True
    assert result["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert result["accepted_root_machine_debt"] == "M4"
    assert result["accepted_closed_obligations"] == []
    assert result["frozen_graph_closed"] is False
    assert result["network_isolated_trust_zero_lean_replay"] == "pass"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["accepted_foundation_tcb_gate"] == "fail_closed"
    assert result["complete_provenance_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == (
        "dependency.S56-M-1055-PROOF.master_acceptance"
    )
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    required_packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet) == required_packet_fields
    assert set(receipt["changed_paths"]) == set(packet["changed_paths"]) == CHANGED_PATHS
    assert receipt["commands"] == packet["commands"]
    assert receipt["output_summary"] == packet["output_summary"]
    assert receipt["known_failures"] == packet["known_failures"]
    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (HERE / "validation-receipt.json", HERE / "validation-phase.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("PASS THM-M-1055 narrow validation")
    print("PASS network-isolated trust-zero kernel replay: exact target, frozen composition, both ported analytic modules, proof root, and differential root elaborated")
    print("PASS trust observation: seven proof declarations and four validation declarations report exactly propext, Classical.choice, and Quot.sound")
    print("PASS local provenance: source hashes, port delta, license, and clean pinned mathlib identity agree")
    print("OPEN authority: PROOF is provisional and the frozen external route disagrees; accepted root remains H2/M4/R4 with zero accepted obligations")
    print("BLOCKED release gates: warm shared cache, unaccepted foundation/TCB, incomplete transitive provenance/SBOM, and no distinct signed independent verifier")
    print("audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
