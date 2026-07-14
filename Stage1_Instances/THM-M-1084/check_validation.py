#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1084-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1084"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1084-VALIDATION"
THEOREM = "THM-M-1084"
BASE_REVISION = "2b8b16b4ca4c9ff610215bd8306fdb3f751f5345"
BASE_TREE = "e9c3bddf01615e3a25aac732152cb0975f38f0eb"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "25bdfe85eaaa67694f865e6af60c240b013b2fbcd9acfb2949e5abdb0b34ca99"
DENOMINATOR_SHA256 = "a2bf7a0e46b0ca64f3ce1259043f8e1f7c85975bb4762a9e2a5256709555111a"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "75ce1fe27d00a5b5f42d0fe6bfc961e9e836145cb2f608faab5ddb122ba98222",
    "ObligationTree.lean": "8868690697aeac26a40f48b5abb88a5859c632b3eadbc7e63666e427f35aabc6",
    "GaussianMGFBridge.lean": "721c0fcae4dbcaf106382d7ac01b5239d29aec941502bc9c59ccdf24d4576142",
    "CoveringNets.lean": "aab49b3768a09f6db7f4925495e6d3113c3c25d3a2bce274bb393079e027a32f",
    "instance.json": "6610ef0b1862fafd446b143754fb3e32d835d95a581a17ad1938ed8a04503103",
    "task-dag.json": "d5bf4d607b7bb9283438bbe1b47a79ab6857a4f77f3fe828eac1f4ca3b0754cb",
    "statement.json": "ea2e93a4d5e878331376aec2724eba0d57a8727e9674e55fb941a110f4cbbe42",
    "anchor-audit.json": "7e0e035b4a1a97db174b53d939eec6e946d29339f6c425c03c236bfdbe609976",
    "obligation-registry.json": "1c447a6f1691e586160ba324c732072ad9604643e2edd7ee3d8fd7a3b4396117",
    "typed-graphs.json": "38c06677202fa48a54df6b892b4d0790dbf5867b20fec188fe69ff864a0e46ef",
    "validation-specs.json": "611468f38da58b304f10c984fdfe2a59e428db7122c2456b804ba1a0f4673195",
    "proof-attempt.json": "e2120e7140102367186e2e252dd4609d818c4c7194d60b687efcd20725dc26f1",
    "proof-receipt.json": "8f3217aee237783ed970490ee03c91a355590c6f7236e6e1b0ccb4bc4779c677",
    "check_proof.sh": "c0b001323fd93eedce4f23c8f326b70b84557449362a424a714e6d2ed2c39d42",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
PARTIAL_DECLARATIONS = (
    "Stage1Instances.THM_M_1084.Proof.hasSubgaussianMGF_of_hasGaussianLaw_of_integral_eq_zero",
    "Stage1Instances.THM_M_1084.Proof.increment_mgf_eq_dist_sq",
    "Stage1Instances.THM_M_1084.Proof.increment_hasSubgaussianMGF",
    "Stage1Instances.THM_M_1084.Proof.gaussianIncrementMGFPackage",
    "Stage1Instances.THM_M_1084.Proof.exists_openBallCover",
    "Stage1Instances.THM_M_1084.Proof.exists_minimal_openBallCover",
    "Stage1Instances.THM_M_1084.Proof.coveringNumber_pos",
)
DIFFERENTIAL_DECLARATIONS = (
    "Stage1Instances.THM_M_1084.Validation.independentlyReconstructedGaussianIncrementMGFPackage",
    "Stage1Instances.THM_M_1084.Validation.independentlyReconstructedCoveringNumberPos",
)
COMPOSITION_DECLARATION = (
    "Stage1Instances.THM_M_1084.root_of_integrability_and_entropy_packages"
)
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
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 900,
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert output.count(no_axioms) + (match is not None) == 1, declaration
    if match is None:
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def network_isolated(
    bwrap: str,
    argv: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
) -> str:
    fixed_env = dict(env)
    fixed_env["PWD"] = str(cwd)
    command = [
        bwrap,
        "--unshare-net",
        "--dev-bind", "/", "/",
        "--proc", "/proc",
        "--chdir", str(cwd),
        "--",
        "env", "-i",
        *[f"{key}={value}" for key, value in sorted(fixed_env.items())],
        *argv,
    ]
    return run(command, cwd=cwd)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_attempt = load(HERE / "proof-attempt.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 526 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 526,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1084-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1084-PROOF"
    )
    assert predecessor["state"] == "[_]"
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-1084-PROOF"]

    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["remaining_root_cut_set"] == [
        "M1084-T-INTEGRABLE", "M1084-T-ENTROPY"
    ]
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1084.DudleyEntropyBoundTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == "M1084-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert frozen_specs["item_id"] == "S56-M-1084-OBLIGATION_TREE"
    assert proof_attempt["root_machine_state"] == "M3"
    assert proof_attempt["provisionally_closed_obligations"] == [
        "M1084-N-GAUSSIAN-MGF"
    ]
    assert proof_receipt["accepted"] is False
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == closure["remaining_root_cut_set"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    lean_files = (
        "Statement.lean", "ObligationTree.lean", "GaussianMGFBridge.lean",
        "CoveringNets.lean", "Validation.lean",
    )
    for name in lean_files:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    validation_source = code_without_comments(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    for forbidden in (
        "DudleyEntropyBoundTarget",
        "SupremumIntegrabilityPackage",
        "EntropyInequalityPackage",
        "root_of_integrability_and_entropy_packages",
    ):
        assert forbidden not in validation_source, forbidden
    assert "independentlyReconstructedGaussianIncrementMGFPackage" in validation_source
    assert "independentlyReconstructedCoveringNumberPos" in validation_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == (
        "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
    )

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    lake_version = run(["lake", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in lake_version
    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap unavailable for the denied-network recipe"
    python = Path(os.path.realpath(os.sys.executable))
    git_path = shutil.which("git")
    assert git_path is not None
    base_lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()

    with tempfile.TemporaryDirectory(prefix="stage1-m1084-validation-") as tmp_name:
        tmp = Path(tmp_name)
        for name in lean_files:
            (tmp / name).write_bytes((HERE / name).read_bytes())
        common_env = {
            "HOME": os.environ.get("HOME", "/nonexistent"),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "LEAN_NUM_THREADS": "1",
            "PATH": os.environ.get("PATH", ""),
            "TZ": "UTC",
        }
        os.chmod(tmp, 0o700)
        old_umask = os.umask(0o022)
        try:
            statement_out = network_isolated(
                bwrap,
                [lean, "--trust=0", "-o", str(tmp / "Statement.olean"), "Statement.lean"],
                cwd=tmp,
                env={**common_env, "LEAN_PATH": base_lean_path},
            )
            local_path = f"{tmp}:{base_lean_path}"
            obligation_out = network_isolated(
                bwrap,
                [lean, "--trust=0", "ObligationTree.lean"],
                cwd=tmp,
                env={**common_env, "LEAN_PATH": local_path},
            )
            mgf_out = network_isolated(
                bwrap,
                [lean, "--trust=0", "-o", str(tmp / "GaussianMGFBridge.olean"),
                 "GaussianMGFBridge.lean"],
                cwd=tmp,
                env={**common_env, "LEAN_PATH": local_path},
            )
            nets_out = network_isolated(
                bwrap,
                [lean, "--trust=0", "-o", str(tmp / "CoveringNets.olean"),
                 "CoveringNets.lean"],
                cwd=tmp,
                env={**common_env, "LEAN_PATH": local_path},
            )
            validation_out = network_isolated(
                bwrap,
                [lean, "--trust=0", "Validation.lean"],
                cwd=tmp,
                env={**common_env, "LEAN_PATH": local_path},
            )
        finally:
            os.umask(old_umask)

    assert "DudleyEntropyBoundTarget" in statement_out
    assert printed_axioms(obligation_out, COMPOSITION_DECLARATION) <= ALLOWED_AXIOMS
    assert "sorryAx" not in obligation_out and "declaration uses 'sorry'" not in obligation_out
    combined_partial = mgf_out + nets_out
    for declaration in PARTIAL_DECLARATIONS:
        assert printed_axioms(combined_partial, declaration) <= ALLOWED_AXIOMS
    assert combined_partial.count("Declarations are sorry-free!") == len(PARTIAL_DECLARATIONS)
    for declaration in DIFFERENTIAL_DECLARATIONS:
        assert printed_axioms(validation_out, declaration) <= ALLOWED_AXIOMS
    assert validation_out.count("Declarations are sorry-free!") == len(
        DIFFERENTIAL_DECLARATIONS
    )
    for output in (obligation_out, combined_partial, validation_out):
        assert "sorryAx" not in output and "declaration uses 'sorry'" not in output
        assert "error:" not in output

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied"
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert spec["expected_exit"] == 0

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1084-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_1084.DudleyEntropyBoundTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["Validation.lean"] == sha256(HERE / "Validation.lean")
    assert receipt["inputs"]["check_validation.py"] == sha256(
        HERE / "check_validation.py"
    )
    assert receipt["inputs"]["validation-phase.md"] == sha256(
        HERE / "validation-phase.md"
    )
    assert receipt["inputs"]["validation-spec.json"] == sha256(
        HERE / "validation-spec.json"
    )
    assert receipt["inputs"]["worker_packet"] == sha256(
        ROOT / ".stage1-worker-selftest.json"
    )
    environment = receipt["environment"]
    assert environment["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert environment["lean_executable_sha256"] == sha256(Path(lean))
    assert environment["lake_executable_sha256"] == sha256(Path(lake))
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(
        Path(os.path.realpath(git_path))
    )
    assert environment["bubblewrap_executable_sha256"] == sha256(
        Path(os.path.realpath(bwrap))
    )
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_remote"] == MATHLIB_REMOTE
    assert environment["mathlib_license_sha256"] == sha256(MATHLIB / "LICENSE")
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    result = receipt["result"]
    assert result["exact_statement_replay"] == "pass"
    assert result["conditional_composition_replay"] == "pass_not_root_closure"
    assert result["partial_proof_replay"] == "pass"
    assert result["same_worker_differential_partial_replay"] == "pass"
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["observed_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["root_kernel_closed"] is False
    assert result["accepted_root_closed"] is False
    assert result["root_machine_debt"] == "M3"
    assert result["remaining_root_cut_set"] == closure["remaining_root_cut_set"]
    assert result["complete_trust_and_provenance_closure"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1084-PROOF.master_acceptance"
    assert receipt["first_failed_mathematical_gate"] == "proof.root_kernel_closure"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("PASS THM-M-1084 narrow validation")
    print("PASS network-isolated kernel replay: exact statement, conditional composition, and nine partial/differential declarations elaborated")
    print("PASS trust observation: checked declarations are sorry-free and use only propext, Classical.choice, and Quot.sound")
    print("PASS selected provenance: frozen local hashes and clean pinned mathlib revision/tree/remote agree")
    print("FAIL CLOSED root: both terminal Dudley packages remain unproved at M3")
    print("FAIL CLOSED authority/trust: proof master acceptance and complete transitive foundation, provenance, and TCB closure remain open")
    print("FAIL CLOSED hermetic release: shared warm .lake is not a clean empty-cache cold offline replay")
    print("FAIL CLOSED independent release: same-worker differential checks are not a distinct signed verifier")
    print("audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
