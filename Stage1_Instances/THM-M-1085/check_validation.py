#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1085-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1085"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1085-VALIDATION"
THEOREM = "THM-M-1085"
BASE_REVISION = "4ba3f2fd1e609b5958f24e0415eef9300da16924"
BASE_TREE = "6abc1f64758c17a59dad8c80ac44f238983dc720"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "2af285ae0bb208a80c325d1b8ba89cd273b83d01b2fef018b13e2feca9d43315"
DENOMINATOR_SHA256 = "c0367c009b2f628b52c7cf782f7785730d0207f7e90ec30afa47c1523a8a4dc4"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "ac7160af49ed699e13856c10d7a0aba637aaa5f76e30eb1ca943a9cbf3136a9d",
    "ObligationTree.lean": "f2d917824b406c3d871d3621d392a78200ff92d58172a96d934ea7e6ee0531b9",
    "AnchorAudit.lean": "07984d6f04ab3c4bb6dc67d0ac29889660e687a14202509d5b712b4b6c7deef8",
    "LawReduction.lean": "1a5394659dba9d5d1502494a636fdc71b47799322684d72f22cc1de07bfd6f96",
    "instance.json": "d22545c42fd51e6fe26041eb07911b6169c7f428586df53cbd5af4890f313da0",
    "task-dag.json": "6995b7e1899f142b319604fa2632e079428540bf7c9547c789462169d0db7472",
    "statement.json": "12da4e651eafb78d25193163da4a9138d05147d16d2faa9ac6f8215ff1259a1b",
    "anchor-audit.json": "33c82a2973972d046376847e801c23450509df3ff18f44c344e506db421dfe10",
    "obligation-registry.json": "0da7c6b059548a2a6c77db369d025695669c9be1ab452c63e9adf03426d2d355",
    "typed-graphs.json": "6f820c55b712708851b9595abbca0b6f1b5f289a2fc4b7a75abaea9f6f850a78",
    "check_statement.py": "3afaa68f36c75b3bd4fa5fa2dee824e46f202dcfbf80f4c382468e47745ffe79",
    "check_obligation_tree.py": "d238e01ed32e1c5c5a393aed0012c005fcd510683b1b33ce9d8a5adcc5eec4f0",
    "check_proof.py": "0e98d3eb12483d445967fd3ca558857e21cda252004ec957f402fd66a27a3130",
    "check_proof.sh": "71bd91e1baecbfa544ceb4d7985e1b1f1bcf3733c61b9106c661cab06a6e6d10",
    "proof-receipt.json": "c8a3d1875e7d7cd44324931a72fdc88ba3368077e9556848b0449293e4ae7be0",
    "proof-validation.md": "d4d8c3f30ebe753b45595f2461e052a44551316adeb59d2f07dbeca99e50a6b6",
    "proof-blocker.md": "6d5cf308a4224895808cf8d3e0456ae151b9ec4e09a6736693c678d88957e9e0",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
PARTIAL_DECLARATIONS = (
    "measurableSet_belowAllRange",
    "measurableSet_belowAllEuclidean",
    "coordinate_hasGaussianLaw",
    "coordinate_integrable",
    "isProbabilityMeasure_of_hasGaussianLaw",
    "pushforward_hasLaw",
    "map_apply_belowAllRange",
    "map_toLp_apply_belowAllEuclidean",
    "integral_coordinate_map",
    "covariance_coordinate_map",
    "covarianceMatrix_eq",
    "covarianceMatrix_posSemidef",
    "covarianceMatrix_diag_eq",
    "covarianceMatrix_offdiag_le",
    "covarianceMatrix_order_data",
    "integral_toLp_map_eq_zero",
    "covarianceBilin_map_eq_multivariateGaussian",
    "gaussian_law_eq_multivariateGaussian",
    "belowAll_eq_multivariateGaussian",
    "slepianTarget_of_law",
)
DIFFERENTIAL_DECLARATIONS = (
    "Stage1Instances.THM_M_1085.Validation.independentlyReconstructedMapBelowAll",
    "Stage1Instances.THM_M_1085.Validation.independentlyReconstructedCovarianceOrder",
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
    timeout: int = 1500,
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
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 527 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 527,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1085-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1085-PROOF"
    )
    assert predecessor["state"] == "[_]"
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-1085-PROOF"]

    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M4"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    expected_cut = [
        "M1085-N-LAWS", "M1085-C-INTERPOLATION",
        "M1085-L-INTERPOLATION-ID", "M1085-L-MIXED-SIGN", "M1085-L-LIMIT",
    ]
    assert closure["remaining_root_cut_set"] == expected_cut

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1085.SlepianTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == "M1085-ROOT"
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert anchor["exact_candidates"] == [] and anchor["machine_debt"] == "M4"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == expected_cut

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    lean_files = (
        "Statement.lean", "ObligationTree.lean", "AnchorAudit.lean",
        "LawReduction.lean", "Validation.lean",
    )
    for name in lean_files:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    proof_source = code_without_comments(
        (HERE / "LawReduction.lean").read_text(encoding="utf-8")
    )
    assert "def LawSlepianTarget : Prop" in proof_source
    assert re.search(r"(?:theorem|def)\s+lawSlepianTarget\b", proof_source) is None
    validation_source = code_without_comments(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    for forbidden in ("SlepianTarget", "LawSlepianTarget", "slepianTarget_of_law"):
        assert forbidden not in validation_source, forbidden

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
    base_lean_path = run(
        ["env", "-u", "LEAN_PATH", "lake", "env", "printenv", "LEAN_PATH"],
        cwd=LEAN_ROOT,
    ).strip()

    with tempfile.TemporaryDirectory(prefix="stage1-m1085-validation-") as tmp_name:
        tmp = Path(tmp_name)
        module_dir = tmp / "Stage1_Instances" / THEOREM
        module_dir.mkdir(parents=True)
        for name in lean_files:
            (module_dir / name).write_bytes((HERE / name).read_bytes())
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
                [lean, "--trust=0", "-t0", "-R", str(tmp), "-o",
                 str(module_dir / "Statement.olean"), str(module_dir / "Statement.lean")],
                cwd=tmp,
                env={**common_env, "LEAN_PATH": base_lean_path},
            )
            local_path = f"{tmp}:{base_lean_path}"
            obligation_out = network_isolated(
                bwrap,
                [lean, "--trust=0", "-t0", "-R", str(tmp),
                 str(module_dir / "ObligationTree.lean")],
                cwd=tmp,
                env={**common_env, "LEAN_PATH": local_path},
            )
            anchor_out = network_isolated(
                bwrap,
                [lean, "--trust=0", "-t0", "-R", str(tmp),
                 str(module_dir / "AnchorAudit.lean")],
                cwd=tmp,
                env={**common_env, "LEAN_PATH": local_path},
            )
            proof_out = network_isolated(
                bwrap,
                [lean, "--trust=0", "-t0", "-R", str(tmp), "-o",
                 str(module_dir / "LawReduction.olean"),
                 str(module_dir / "LawReduction.lean")],
                cwd=tmp,
                env={**common_env, "LEAN_PATH": local_path},
            )
            validation_out = network_isolated(
                bwrap,
                [lean, "--trust=0", "-t0", "-R", str(tmp),
                 str(module_dir / "Validation.lean")],
                cwd=tmp,
                env={**common_env, "LEAN_PATH": local_path},
            )
        finally:
            os.umask(old_umask)

    assert "SlepianTarget" in statement_out
    assert "slepianTarget_of_pointwise" in obligation_out
    assert "HasGaussianLaw" in anchor_out and "IsGaussianProcess" in anchor_out
    proof_namespace = "Stage1Instances.THM_M_1085.Proof."
    for short_name in PARTIAL_DECLARATIONS:
        declaration = proof_namespace + short_name
        assert printed_axioms(proof_out, declaration) <= ALLOWED_AXIOMS
    assert proof_out.count("Declarations are sorry-free!") == len(PARTIAL_DECLARATIONS)
    for declaration in DIFFERENTIAL_DECLARATIONS:
        assert printed_axioms(validation_out, declaration) <= ALLOWED_AXIOMS
    assert validation_out.count("Declarations are sorry-free!") == len(
        DIFFERENTIAL_DECLARATIONS
    )
    for output in (statement_out, obligation_out, anchor_out, proof_out, validation_out):
        assert "sorryAx" not in output and "declaration uses 'sorry'" not in output
        assert "error:" not in output

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 1500
    assert spec["network_policy"] == "denied"
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert spec["expected_exit"] == 0

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1085-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["release_grade"] is False
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_1085.SlepianTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    for name in (
        "Validation.lean", "check_validation.py", "validation-phase.md",
        "validation-spec.json",
    ):
        assert receipt["inputs"][name] == sha256(HERE / name), name
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
    assert result["partial_proof_replay"] == "pass_no_closed_frozen_obligation"
    assert result["same_worker_differential_partial_replay"] == "pass"
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["observed_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["root_kernel_closed"] is False
    assert result["accepted_root_closed"] is False
    assert result["root_machine_debt"] == "M4"
    assert result["remaining_root_cut_set"] == expected_cut
    assert result["complete_trust_and_provenance_closure"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1085-PROOF.master_acceptance"
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

    print("PASS THM-M-1085 narrow validation")
    print("PASS network-isolated kernel replay: exact statement, conditional interfaces, twenty partial declarations, and two differential probes elaborated")
    print("PASS trust observation: checked declarations are sorry-free and use only propext, Classical.choice, and Quot.sound")
    print("PASS selected provenance: frozen local hashes and clean pinned mathlib revision/tree/remote agree")
    print("FAIL CLOSED root: LawSlepianTarget is uninhabited and the five-node frozen cut set remains open at M4")
    print("FAIL CLOSED authority/trust: proof master acceptance and complete transitive foundation, provenance, and TCB closure remain open")
    print("FAIL CLOSED hermetic release: shared warm .lake is not a clean empty-cache cold offline replay")
    print("FAIL CLOSED independent release: same-worker differential checks are not a distinct signed verifier")
    print("audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
