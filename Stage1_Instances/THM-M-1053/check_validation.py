#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1053-VALIDATION."""

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
ITEM = "S56-M-1053-VALIDATION"
THEOREM = "THM-M-1053"
BASE_REVISION = "a3c20fd2f4da1879baa00bd5455573c49d4b2fa0"
BASE_TREE = "2ae6946f2b059449025558b6033de33c332412ee"
EXPRESSION_SHA256 = "f4b06a49160cd083fa4cf1bb3b1ddfe1453dbcb1e521ff2c09ba5d3753a2e562"
DENOMINATOR_SHA256 = "125e28fed0cbce9e0cbffea0da90b047c35a770c90d3be2a82a42319b8606005"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
UPSTREAM_REVISION = "ed3fa6b8a30594eeb791160563942ba115581aa0"
UPSTREAM_ARCHIVE_SHA256 = "3c0ef177500430ab55950061cfd73991347f5336b5b3d5032ffe46ac56009a52"
UPSTREAM_MAXIMAL_SHA256 = "6b9c40bd0e8d7238919283ad8666d0563d780a3b31eeb67d0ca66aae821817cc"
UPSTREAM_BIRKHOFF_SHA256 = "bed8d81c6eb7f0ba74548255779dad7c3dc4e75ecf7ad935e1c68ef6fcb6ea6a"
LICENSE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
EXPECTED_INPUTS = {
    "Statement.lean": "0beae61d530145f227f6657484cf04f6e847d604164cb6683c8aee94aeb01427",
    "AnchorAudit.lean": "923ad6bcec3f2c00cce422765403852795b45cbbb7e9edf455d0b60712857a00",
    "anchor-audit.json": "baf2b7785821f7142b951bdd7307e2d2d47ba2fefb086a9ec4544b1317d0b831",
    "statement.json": "0989ab7f51afdf593013d9d20aa00d6104ef1f1ac47cec208f816fc7b1352016",
    "ObligationTree.lean": "98ffaf435760f36440c117615de363b81c1f9ad8e859d0bc4b201e73bd9e3345",
    "obligation-registry.json": "f16e88a56975ab2487cd36077bef1719dd27f0031c71453510665f1aea8c4b17",
    "typed-graphs.json": "a98e9c030b90131e73f695a8bd12727b9857ce163631ac33c580084d7a47ba88",
    "validation-specs.json": "84ee161824e70b3ff338c6a047d94c163ade03c6002f0ac94cb9fcb4fd7f57e2",
    "instance.json": "317f4da95c8321252b01a9c11d6d6c05d6fbbba70db57db9be1e7f44d5b10c34",
    "task-dag.json": "6a82f68e8efca9a0a8851ab83e7f5ecf6437a6deb3671d8d784effd0cd9b597a",
    "Proof.lean": "830f2a5ae481a3ee3e7994b21b94f75c86b15001ecb95d0fee3ded3feabf8656",
    "proof-receipt.json": "ca51b92704687406b5d5799220ec4f77665ab8b8afad8b7243bda290b6949b2d",
    "MaximalErgodic.lean": "af39bb1048599b97b58f4a982cc7de8a379b2f54597d0c3aba08ca476b01924d",
    "Birkhoff.lean": "d78b7eaa868ed59d8ed852649d309fd4388630b99e1c3498b09e34ade5e74f06",
    "LICENSE": LICENSE_SHA256,
    "PORT_PROVENANCE.md": "e44791cde325bec53878d54731eedd10736f394607a4c73890d2002181048a3b",
    "Validation.lean": "5643cb24e200b46cf97c0288c30d9d7161b0a24307c90c3d27b204d07a7d0d2f",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
VALIDATION_INPUTS = {
    "validation-spec.json": "a9d4865414b9c84e044fd6c22194d42d9e96ee697994c97858a7d32189ee5c99",
}
MACHINE_IDS = [
    "M1053-ROOT", "M1053-S-DEFINITIONS", "M1053-S-BOUNDARY",
    "M1053-S-FOUNDATION", "M1053-N-AVERAGE", "M1053-L-MAXIMAL",
    "M1053-L-DENSE-CLASS", "M1053-L-AE-CONVERGENCE",
    "M1053-L-LIMIT-INTEGRABLE", "M1053-L-LIMIT-INVARIANT",
    "M1053-T-GENERAL", "M1053-L-ERGODIC-IDENTIFICATION",
    "M1053-T-ASSEMBLE", "M1053-X-EXTERNAL",
]
COVERED_IDS = MACHINE_IDS + ["M1053-X-SOURCE", "M1053-X-PROVENANCE"]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1053 narrow validation",
    "PASS network-isolated trust-zero kernel replay: exact root, ported bodies, proof route, and differential route elaborated",
    "PASS trust observation: checked declarations are sorry-free and report exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: port reconstruction, license, frozen hashes, clean mathlib pin, and tool identities agree",
    "FAIL CLOSED authority and graph: proof lacks master acceptance; frozen dense-class route is unrealized and identification package is refuted",
    "FAIL CLOSED foundation/trust/provenance: accepted policy, complete transitive closure, TCB inventory, and SBOM remain open",
    "FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or deterministic bundle",
    "FAIL CLOSED independent release: the differential proof used this worker, checkout, kernel, and cache, not a distinct signed verifier",
    "audit_complete=false; theorem_complete=false",
)
STARTED = time.monotonic()
TIMEOUT_SECONDS = 900.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables assertions")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 900-second wall-clock bound")
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=remaining, check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
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
        output, re.DOTALL,
    )
    assert match is not None, declaration
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


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
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 245 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 245,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-1053-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1053-PROOF"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task == {
        "id": ITEM, "depends_on": ["S56-M-1053-PROOF"], "state": "open"
    }

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    for name, expected in VALIDATION_INPUTS.items():
        assert sha256(HERE / name) == expected, f"changed validation input: {name}"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1.THM_M_1053.StatementShape"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == "M1053-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == [
        "M1053-T-GENERAL", "M1053-L-ERGODIC-IDENTIFICATION"
    ]
    assert proof_receipt["item_id"] == "S56-M-1053-PROOF"
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["proof_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["frozen_graph_closed"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["frozen_proof_graph_cut_set"] == [
        "M1053-L-DENSE-CLASS", "M1053-L-ERGODIC-IDENTIFICATION"
    ]
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOM_LIST
    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H2", "M": "M1", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    lean_sources = (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
        "MaximalErgodic.lean", "Birkhoff.lean", "Proof.lean", "Validation.lean",
    )
    for name in lean_sources:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = re.sub(r"^#print sorries .*?$", "", source, flags=re.MULTILINE)
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = code_without_comments((HERE / "Validation.lean").read_text())
    for forbidden in (
        "import Proof", "import ObligationTree", "statementShape_proof",
        "generalInvariantLimitPackage_proof", "statementShape_of_packages",
    ):
        assert forbidden not in differential, forbidden
    assert "theorem differentialStatementShape" in differential
    assert "assert_no_sorry differentialStatementShape" in differential

    assert sha256(HERE / "LICENSE") == LICENSE_SHA256
    port_maximal = (HERE / "MaximalErgodic.lean").read_bytes()
    port_birkhoff = (HERE / "Birkhoff.lean").read_bytes()
    maximal_notice = (
        b"/-\nPort note: this file is modified from\n"
        + f"`marcmorningstar/lean4-ergodic-theory@{UPSTREAM_REVISION}`.\n".encode()
        + b"The sole compatibility change is the pinned-mathlib spelling\n"
        + b"`integrable_finset_sum`; see `PORT_PROVENANCE.md`.\n-/\n"
    )
    birkhoff_notice = (
        b"/-\nPort note: this file is modified from\n"
        + f"`marcmorningstar/lean4-ergodic-theory@{UPSTREAM_REVISION}`.\n".encode()
        + b"Only the sibling module import below is target-local; see `PORT_PROVENANCE.md`.\n-/\n"
    )
    assert port_maximal.count(maximal_notice) == 1
    assert port_birkhoff.count(birkhoff_notice) == 1
    reconstructed_maximal = port_maximal.replace(maximal_notice, b"", 1).replace(
        b"integrable_finset_sum", b"integrable_finsetSum", 1
    )
    reconstructed_birkhoff = port_birkhoff.replace(birkhoff_notice, b"", 1).replace(
        b"import MaximalErgodic", b"import ErgodicTheory.Ergodic.MaximalErgodic", 1
    )
    assert sha256_bytes(reconstructed_maximal) == UPSTREAM_MAXIMAL_SHA256
    assert sha256_bytes(reconstructed_birkhoff) == UPSTREAM_BIRKHOFF_SHA256

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    lake_version = run(["lake", "env", "lake", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in lake_version
    python = Path(os.path.realpath(sys.executable))
    git_path = Path(os.path.realpath(shutil.which("git") or ""))
    bash = Path(os.path.realpath(shutil.which("bash") or ""))
    bwrap = Path(os.path.realpath(shutil.which("bwrap") or ""))
    assert bwrap.is_file(), "bubblewrap is required for network-denied replay"
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()

    with tempfile.TemporaryDirectory(prefix="m1053-validation-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        for source_name in (
            "Statement.lean", "ObligationTree.lean", "MaximalErgodic.lean",
            "Birkhoff.lean", "Proof.lean", "Validation.lean",
        ):
            (tmp / source_name).write_bytes((HERE / source_name).read_bytes())
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

    assert "Stage1.THM_M_1053.StatementShape" in statement_output
    assert "sorryAx" not in (
        obligation_output + maximal_output + birkhoff_output
        + proof_output + validation_output
    )
    proof_declarations = (
        "ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg",
        "ErgodicTheory.tendsto_birkhoffAverage_ae",
        "ErgodicTheory.tendsto_birkhoffAverage_ae_integral",
        "Stage1.THM_M_1053.generalInvariantLimitPackage_proof",
        "Stage1.THM_M_1053.statementShape_proof",
        "Stage1.THM_M_1053.not_ergodicLimitIdentificationPackage",
    )
    for declaration in proof_declarations:
        assert printed_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    validation_declarations = (
        "ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg",
        "ErgodicTheory.tendsto_birkhoffAverage_ae",
        "ErgodicTheory.tendsto_birkhoffAverage_ae_integral",
        "Stage1.THM_M_1053.Validation.differentialStatementShape",
    )
    for declaration in validation_declarations:
        assert printed_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    assert proof_output.count("Declarations are sorry-free!") == 6
    assert validation_output.count("Declarations are sorry-free!") == 4

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "--unshare-net" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == COVERED_IDS
    assert "M1053-S-FOUNDATION" in spec["covered_obligation_ids"]
    assert "M1053-X-PROVENANCE" in spec["covered_obligation_ids"]
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact nine-line PASS/FAIL-CLOSED status summary",
    }]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1053-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["covered_obligation_ids"] == COVERED_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    for input_name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][input_name] == expected, input_name
    for input_name, expected in VALIDATION_INPUTS.items():
        assert receipt["inputs"][input_name] == expected, input_name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["worktree_state"]["preexisting_untracked_link_target_sha256"] == (
        sha256_bytes(os.readlink(LEAN_ROOT / ".lake").encode())
    )
    canonical = receipt["canonical_target"]
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert canonical["registry_denominator_sha256"] == DENOMINATOR_SHA256
    environment = receipt["environment"]
    assert environment["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_path)
    assert environment["bash_executable_sha256"] == sha256(bash)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    result = receipt["result"]
    assert result["exact_root_kernel_replay"] == "provisional_pass"
    assert result["differential_exact_root_replay"] == "provisional_pass_same_worker"
    assert result["observed_axioms"] == EXPECTED_AXIOM_LIST
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["selected_provenance"] == "pass"
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["frozen_graph_closed"] is False
    assert result["frozen_graph_cut_set"] == [
        "M1053-L-DENSE-CLASS", "M1053-L-ERGODIC-IDENTIFICATION"
    ]
    assert result["accepted_root_machine_debt"] == "M1"
    assert result["accepted_root_closed"] is False
    assert result["foundation_and_complete_trust_closure"] == "fail_closed"
    assert result["complete_provenance_closure"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1053-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    notes = (HERE / "validation-phase.md").read_text(encoding="utf-8")
    assert "same-worker differential" in notes
    assert "empty-cache cold bootstrap" in notes
    assert "theorem completion remain false" in notes
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (HERE / "validation-receipt.json", HERE / "validation-phase.md"):
        public_text = path.read_text(encoding="utf-8")
        assert "/home/" not in public_text and ".cron/" not in public_text
        assert "theorem_complete=true" not in public_text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
