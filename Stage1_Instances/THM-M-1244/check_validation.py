#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1244-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import time


if not __debug__:
    raise SystemExit("check_validation.py must run without Python optimization")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1244"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1244-VALIDATION"
THEOREM = "THM-M-1244"
BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
UPSTREAM_REVISION = "7b82b1323c80f0c21ca449fd12e1c24315ae9782"
EXPRESSION_SHA256 = "eeff335a47ceaf9d469f25e1570640f17008c1f38d8173499a5429e7ab6397b3"
DENOMINATOR_SHA256 = "edecb957b6903682647ae02dbfff3d6bdd693e6ddf2decd18721fdcae702c297"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "f1507845f649ea0881f77178c58ac681851c127e26c0dd42cce92b38f48d441b",
    "ObligationTree.lean": "1ce196b7f6f6d77565ae290c12f1b33ac2b1cdd63084e1aa2dbce560722aa2d5",
    "Proof.lean": "787fa20226032f9e80ee13a633dfeab6c6aaf2a6d04d30a3319a2d8d56c9cb8d",
    "ProofAudit.lean": "a285c69aa7175479c603d8c24d69b829e4aef5886d0e61301ed69272034fc1f7",
    "Validation.lean": "c32b1b113aa8b2889369b1b2f94a78bca6c14344d9b91659fdf6f9f8a3d6c7fa",
    "statement.json": "40c235b0fcc33b49169fc18eb8992c0e4aa7c684709f74711dab99f16b0d0e84",
    "anchor_audit.json": "e5773083e9187011d8fe2e8e928ab6e34dea15d582d669774241c076876e1d2b",
    "obligation-registry.json": "bbf8a6a8990b8d468da92cbcd048f66ca66185747adc8932e09f2931d477911f",
    "typed-graphs.json": "7bc58e69698479b0bb80f6af24f38b056f69376a725dea90e6642fe21a5d866f",
    "proof-receipt.json": "42b078de85cbf52d01e7c6b8a75a1858439f3433c982018ca60820351ee4e248",
    "check_proof.py": "d18254d30512a05684065e7f655b739f928e6b7bfc66506221e908ea343d1d03",
    "PORT_PROVENANCE.md": "18353ff34e52543eee89d8dd6acf4b0f317c1f6c68eea8b44c859aa70f0ce1c8",
    "LICENSE": "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30",
    "check_validation.sh": "281285b46eccd63abf12556e86be998bb9d9a00212f6feb3c781d73b5ddd7308",
    "validation-spec.json": "c5b3c6a0c2ca031689db449e1c64cc5744845eee31443f4a19ee4efc9d385af0",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_TOOL_HASHES = {
    "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "lake": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
    "python": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "git": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
    "bwrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
}
SELECTED_MATHLIB = {
    "Mathlib/Probability/Distributions/Gaussian/Real.lean": {
        "blob": "f5795fbfb92475879b67b0ee8577687575a82258",
        "source_sha256": "f5321db08f0156c5a12e15986d2ced9108183c907e3082d2566da8ef8da931a8",
        "olean_sha256": "b5894530bc315c897142ff650c774ed5ee3180b1df45690021fdd830e6e82ea4",
    },
    "Mathlib/MeasureTheory/Integral/Prod.lean": {
        "blob": "184104dac5a7787740bde1cd69a420699274b81a",
        "source_sha256": "3f695c14e45e3e97e28df9e90bd6db4d0283ced3db5572c67ca67f4297f0e1f9",
        "olean_sha256": "b1f35a43087bc11266b472ffc0784d801d2a5c3457bea8102cbd5fbc87005ee2",
    },
    "Mathlib/Analysis/Calculus/FDeriv/Pi.lean": {
        "blob": "2e72516986f5a0ad0352f14b29cbf8b5da48edda",
        "source_sha256": "8d125b8e54c4b30c3212ce41ba2ca12161f1200e70feaf2bc18f190532f4cf78",
        "olean_sha256": "a700c39cd2517df1038196759fd2ea8611fba0687da48ffd0e7d1144bcc2c164",
    },
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/ProofAudit.lean",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1244 narrow validation",
    "PASS network-isolated trust-zero replay: exact statement, composition, vendored terminal, proof root, and no-Proof-module reconstruction elaborated",
    "PASS hygiene: kernel recursive sorry checks and comment-stripped prohibited-construct scan passed",
    "PASS trust observation: all seven checked declarations stay within propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, upstream pin, clean mathlib pin/tree/remote, selected source/olean hashes, license, and tools agree",
    "FAIL CLOSED authority/state: proof is provisional and the frozen graph remains M4/open pending master reconciliation",
    "FAIL CLOSED hermetic/trust: shared warm .lake is not an empty-cache offline replay or complete transitive TCB/SBOM bundle",
    "FAIL CLOSED independence/readability/source: same-worker replay is not independent verification; H0 and R0 reviews remain open",
    "audit_complete=false; theorem_complete=false",
)
STARTED = time.monotonic()
TIMEOUT_SECONDS = 2400.0


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(result, dict), path
    return result


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 2400-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
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
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 425 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 425,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1244-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1244-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "closed_obligations": ["M1244-T-ASSEMBLE"],
        "root_closed": False,
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": ["M1244-L-UPSTREAM", "M1244-L-INTEGRAL"],
        "composition_certificates": [
            "Stage1Instances.THM_M_1244.gaussianLogSobolevTarget_of_packages"
        ],
        "reason": "The conditional final composition is checked, but neither analytic package has a proof body.",
    }

    assert proof_receipt["item_id"] == "S56-M-1244-PROOF"
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["proof_body"]["origin"]["revision"] == UPSTREAM_REVISION
    assert proof_receipt["required_machine_open_ids"] == [
        "M1244-S-DEFS", "M1244-S-DOMAIN", "M1244-S-BOUNDARY", "M1244-S-FOUNDATION"
    ]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    lean_paths = [
        HERE / "Statement.lean", HERE / "ObligationTree.lean", HERE / "Proof.lean",
        HERE / "ProofAudit.lean", HERE / "Validation.lean", *(HERE / "SLT").rglob("*.lean"),
    ]
    for path in lean_paths:
        source = code_without_comments(path.read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {path}"
    validation_header = (HERE / "Validation.lean").read_text(encoding="utf-8").split("/-!", 1)[0]
    assert "import Proof" not in validation_header
    validation_code = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    for forbidden in ("coordinateLogSobolevPackage", "coordinateToOperatorEnergyPackage", "gaussianLogSobolev :"):
        assert forbidden not in validation_code, forbidden
    assert "independentlyReconstructedGaussianLogSobolev" in validation_code
    assert "assert_no_sorry independentlyReconstructedGaussianLogSobolev" in validation_code

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    for source_name, expected in SELECTED_MATHLIB.items():
        source = MATHLIB / source_name
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / source_name.replace(".lean", ".olean")
        assert git("rev-parse", f"HEAD:{source_name}", cwd=MATHLIB) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
    assert sha256(MATHLIB / "LICENSE") == "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    python = Path(os.path.realpath(os.sys.executable))
    git_path = Path(os.path.realpath(shutil.which("git") or ""))
    bwrap = Path(os.path.realpath(shutil.which("bwrap") or ""))
    tools = {"lean": lean, "lake": lake, "python": python, "git": git_path, "bwrap": bwrap}
    for name, path in tools.items():
        assert path.is_file() and sha256(path) == EXPECTED_TOOL_HASHES[name], (name, path)
    lean_version = run([str(lean), "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], cwd=LEAN_ROOT)

    runner_output = run(["bash", str(HERE / "check_validation.sh")])
    runner_bytes = runner_output.encode("utf-8")
    assert hashlib.sha256(runner_bytes).hexdigest() == receipt["result"]["kernel_output_sha256"]
    assert len(runner_bytes) == receipt["result"]["kernel_output_bytes"]
    assert runner_output.count("Declarations are sorry-free!") == 7
    assert "PASS axiom profile: seven checked declarations" in runner_output
    assert "sorryAx" not in runner_output and "declaration uses 'sorry'" not in runner_output

    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    for source_name, expected in SELECTED_MATHLIB.items():
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / source_name.replace(".lean", ".olean")
        assert sha256(MATHLIB / source_name) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["timeout_seconds"] == 2400
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["env_allowlist"] == {}
    assert len(spec["covered_obligation_ids"]) == len(set(spec["covered_obligation_ids"]))
    assert len(spec["covered_declarations"]) == 7
    for field in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations", "scope_boundary",
    ):
        assert receipt["recipe"][field] == spec[field], field

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["inputs"] == {**EXPECTED_INPUTS, "check_validation.py": sha256(Path(__file__).resolve())}
    assert receipt["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert receipt["result"]["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert receipt["result"]["axiom_report_count"] == 7
    assert receipt["result"]["placeholder_and_unsafe_scan"] == "pass"
    assert receipt["result"]["proof_master_acceptance"] == "fail_closed"
    assert receipt["result"]["typed_state_and_architecture_reconciliation"] == "fail_closed"
    assert receipt["result"]["complete_provenance_and_tcb"] == "fail_closed"
    assert receipt["result"]["hermetic_cold_offline_replay"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["root_vector_before"] == {"human": "H1", "machine": "M4", "readability": "R3"}
    assert receipt["root_vector_after_worker_selftest"] == {
        "human": "H1", "machine": "M4_with_provisional_exact_root_replay", "readability": "R3"
    }
    assert receipt["first_failed_gate"] == "dependency.S56-M-1244-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert set(receipt["changed_paths"]) == CHANGED_PATHS

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands_and_exit_codes"]
    assert packet["output_summary"] == list(SUMMARY_LINES)
    summary_bytes = ("\n".join(packet["output_summary"]) + "\n").encode("utf-8")
    expected_output = spec["expected_outputs"][0]
    assert hashlib.sha256(summary_bytes).hexdigest() == expected_output["semantic_sha256"]
    assert len(summary_bytes) == expected_output["bytes"]
    assert packet["known_failures"] == receipt["known_failures"]

    public_text = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("validation-phase.md", "validation-receipt.json")
    )
    assert "/home/" not in public_text and ".cron/" not in public_text
    assert '"theorem_complete": true' not in public_text
    status_lines = set(
        git(
            "status", "--porcelain=v1", "-uall", "--",
            f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
            "Formalizations/Lean/.lake",
        ).splitlines()
    )
    required_status = {f"?? {path}" for path in CHANGED_PATHS}
    assert required_status <= status_lines, (status_lines, required_status)
    allowed_extra = {
        "?? Formalizations/Lean/.lake",
        "?? Stage1_Instances/THM-M-1244/tmpkjvxwv_v.lean",
    }
    assert status_lines <= required_status | allowed_extra, status_lines
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    assert platform.system() == "Linux"
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
