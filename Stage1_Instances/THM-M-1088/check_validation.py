#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1088-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1088"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1088-VALIDATION"
THEOREM = "THM-M-1088"
BASE_REVISION = "9584b263a758e0dbab59344389554570dcf2e535"
BASE_TREE = "d4ea7039d087ff41783f81c4f1b35c2817dd6a1b"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
REGISTRY_DENOMINATOR = "56fb1860d804859c9580000d4f003ce8ad997dea3f9e40aca50d5b1efe921f3d"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUT_HASHES = {
    "Statement.lean": "907c7a7e9cefced10649e3de0b3230e78bf852484b93caf02b6f40ff9920e1c7",
    "ObligationTree.lean": "3a84b1dddb7d61e43fda96574732531f49c6aac353b35e17de80a1ed056a5939",
    "Proof.lean": "77e8587590de79fa2f58029f1bdcddda1d61c6e2461740508be252f754ed21c5",
    "Validation.lean": "b2bef1c81f2544d69b4be7268da3504e45e43a58fb7239d7044fbb39c72f4d75",
    "anchor-audit.md": "d19940bb5a7ad055c1a1a6a2f95ce3570be4e1833b9e769a5234f32070ce8086",
    "source-statement-crosswalk.md": "956e15c97c92706871cdf30d131e0ebde9e57128a171c8f39f4b0c970ff16acf",
    "obligation-registry.json": "ea7883a01a2ed602fa365888a2c836a64a6dacd1d404e38aa98818e5ecded495",
    "typed-graphs.json": "737f489744cc0342a47d05549aa9acf45f3fe21e6a0451cd2301298050b05069",
    "proof-receipt.json": "fc9dc7a73c59ca8785cee48cd012b43600f9878e5b679dda9c034ef34d45f2c1",
    "proof-blocker.json": "ad74bc238c86bc7dc7485024c228472c03c8a25eb564592aecd3480b3b79c1fe",
    "proof-validation.md": "c2a92c10951ce860645449bf3f4f45f6bb16c926f3b1312561055d12a27bfb10",
}
MATHLIB_SOURCE_HASHES = {
    "Mathlib/Probability/Distributions/Gaussian/IsGaussianProcess/Basic.lean": (
        "b324daeb7f5868696e257f603b1eed66e72228890bdc32c251f838f7c08421b3"
    ),
    "Mathlib/Probability/Moments/SubGaussian.lean": (
        "1261993867efbddb6781a6ce9d0855335fab6891f819062ac83b8d9f6d94c440"
    ),
}
MATHLIB_OLEAN_HASHES = {
    ".lake/build/lib/lean/Mathlib/Probability/Distributions/Gaussian/IsGaussianProcess/Basic.olean": (
        "1b6d9f0530fc05deed850214607c75e822dc19bc0f1929eb75961dd9511180ed"
    ),
    ".lake/build/lib/lean/Mathlib/Probability/Moments/SubGaussian.olean": (
        "063f83b186bfdee9417f4eccd88160425c87debf5cfdf8bc829d277ed761497b"
    ),
}
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_1088.Proof.coordinate_hasSubgaussianMGF",
    "Stage1Instances.THM_M_1088.Proof.zeroTailBound_of_isGaussianProcess",
    "Stage1Instances.THM_M_1088.Proof.upperTailBound_of_hasSubgaussianMGF",
    "Stage1Instances.THM_M_1088.Proof.upperTailBound_of_process_hasSubgaussianMGF",
)
VALIDATION_DECLARATIONS = (
    "Stage1Instances.THM_M_1088.Validation.coordinate_hasSubgaussianMGF",
    "Stage1Instances.THM_M_1088.Validation.zeroTailBound_of_isGaussianProcess",
    "Stage1Instances.THM_M_1088.Validation.strictUpperTail_of_hasSubgaussianMGF",
    "Stage1Instances.THM_M_1088.Validation.processUpperTail_of_supremumMGF",
)
ARCHITECTURAL_ROOT_CUT = ["M1088-T-ENGINE"]
PROOF_EXECUTION_CUT = [
    "M1088-L-FINITE-CONCENTRATION",
    "M1088-L-COVARIANCE",
    "M1088-L-MEAN-LIMIT",
    "M1088-L-PROBABILITY-LIMIT",
    "M1088-T-ENGINE",
]
FIRST_THEOREM_GATE = (
    "M1088-L-FINITE-CONCENTRATION: no placeholder-free sharp sub-Gaussian MGF "
    "theorem for a finite Gaussian maximum exists in the pinned closure"
)
RECIPE_PATH = "/usr/bin:/bin"
RECIPE_ARGV = [
    "/usr/bin/bwrap",
    "--ro-bind", "/", "/",
    "--dev", "/dev",
    "--proc", "/proc",
    "--tmpfs", "/tmp",
    "--unshare-net",
    "--die-with-parent",
    "--clearenv",
    "--setenv", "HOME", "/tmp",
    "--setenv", "PATH", RECIPE_PATH,
    "--setenv", "LANG", "C.UTF-8",
    "--setenv", "LC_ALL", "C.UTF-8",
    "--setenv", "TZ", "UTC",
    "--setenv", "LEAN_NUM_THREADS", "1",
    "/usr/bin/python3", "-I", "-B",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}

if not __debug__:
    raise RuntimeError("validation requires Python assertions")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).rstrip()


def untracked_patch_sha256(path: Path) -> str:
    relative = path.relative_to(ROOT)
    result = subprocess.run(
        ["git", "diff", "--no-index", "--binary", "/dev/null", str(relative)],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert result.returncode == 1 and result.stderr == b"", path
    return hashlib.sha256(result.stdout).hexdigest()


def source_without_comments(source: str) -> str:
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


def reported_axioms(output: str, declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    assert output.count(no_axioms) + len(matches) == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


spec = load(HERE / "validation-spec.json")
instance = load(HERE / "instance.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
proof_receipt = load(HERE / "proof-receipt.json")
proof_blocker = load(HERE / "proof-blocker.json")
targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
receipt_path = HERE / "validation-receipt.json"
receipt = load(receipt_path) if receipt_path.exists() else None
verify_receipt = os.environ.get("STAGE1_SKIP_RECEIPT_CHECK") != "1"

assert git("rev-parse", "HEAD") == BASE_REVISION
assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
assert target["execution_rank"] == 530 and target["baseline"] == "L0"
assert target["lifecycle_mode"] == "planned" and target["rework_required"] is True
assert target["legacy_artifacts_accepted"] is target["theorem_complete"] is False
item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item == {
    "id": ITEM,
    "theorem_id": THEOREM,
    "execution_rank": 530,
    "phase": "validation",
    "layer": 5,
    "state": "[ ]",
    "depends_on": ["S56-M-1088-PROOF"],
    "owned_paths": [f"Stage1_Instances/{THEOREM}"],
    "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1088-PROOF")
assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

assert spec["schema_version"] == "stage1-validation-spec/1.0"
assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
assert spec["argv"] == RECIPE_ARGV
assert spec["cwd"] == "." and spec["network_policy"] == "denied"
assert spec["env_allowlist"] == {
    "HOME": "/tmp",
    "PATH": RECIPE_PATH,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}
assert spec["expected_exit"] == 0 and spec["timeout_seconds"] == 900
assert spec["covered_obligation_ids"] == []
assert len(spec["observed_open_state_obligation_ids"]) == 19
assert set(spec["observed_open_state_obligation_ids"]) == set(
    registry["frozen_denominators"]["inventory"]
)
assert len(spec["covered_declarations"]) == len(set(spec["covered_declarations"])) == 11

for name, expected in EXPECTED_INPUT_HASHES.items():
    assert sha256(HERE / name) == expected, f"bound validation input changed: {name}"
assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
assert registry["root_obligation_id"] == "M1088-ROOT"
assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
assert registry["status_observed_after_freeze"] == {
    "provisionally_checked_interfaces": ["M1088-T-ASSEMBLE"],
    "closed_obligations": [],
    "root_machine_debt": "M3",
}
closure = graphs["closure_boundary"]
assert closure["closed_obligations"] == []
assert closure["remaining_root_cut_set"] == ARCHITECTURAL_ROOT_CUT
assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
assert graphs["graphs"]["evidence"]["edges"] == []
assert instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
assert instance["accepted_proof_state"] == []
assert instance["audit_complete"] is instance["theorem_complete"] is False
assert proof_receipt["accepted"] is False and proof_receipt["proposed_state"] == "[_]"
assert proof_receipt["provisionally_closed_obligation_ids"] == []
assert proof_receipt["accepted_closed_obligation_ids"] == []
assert proof_receipt["result"]["root_kernel_closed"] is False
assert proof_receipt["result"]["audit_complete"] is proof_receipt["result"]["theorem_complete"] is False
assert proof_receipt["remaining_root_cut_set"] == PROOF_EXECUTION_CUT
assert proof_receipt["first_failed_gate"] == FIRST_THEOREM_GATE
assert proof_blocker["root_closed"] is proof_blocker["audit_complete"] is proof_blocker["theorem_complete"] is False
assert proof_blocker["provisionally_closed_obligation_ids"] == []

for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
    path = ROOT / relative
    if not path.exists() and not verify_receipt:
        continue
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

lean_files = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
all_source = "\n".join(
    source_without_comments((HERE / name).read_text(encoding="utf-8")) for name in lean_files
)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|public|noncomputable|local|scoped|partial)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe|extern)\b",
    re.MULTILINE,
)
assert prohibited.search(all_source) is None
validation_source = source_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
assert "import Proof" not in validation_source and "import ObligationTree" not in validation_source
assert "target_of_upperTailEngine" not in validation_source and "UpperTailEngine" not in validation_source
assert "(hmgf : ProbabilityTheory.HasSubgaussianMGF" in validation_source
assert re.search(r"^theorem[ \t]+BorellTISTarget(?:[ \t:(]|$)", all_source, re.MULTILINE) is None

manifest = load(LEAN_ROOT / "lake-manifest.json")
mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir(), "pinned mathlib artifact is unavailable"
assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
for name, expected in MATHLIB_SOURCE_HASHES.items():
    assert sha256(mathlib / name) == expected, f"changed pinned mathlib source: {name}"
for name, expected in MATHLIB_OLEAN_HASHES.items():
    assert sha256(mathlib / name) == expected, f"changed pinned compiled artifact: {name}"

account_home = Path(pwd.getpwuid(os.getuid()).pw_dir)
toolchain_bin = account_home / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin"
lean = toolchain_bin / "lean"
lake = toolchain_bin / "lake"
bwrap = Path(shutil.which("bwrap") or "")
assert lean.is_file() and lake.is_file() and bwrap.is_file()
assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
assert bwrap == Path("/usr/bin/bwrap") and sha256(bwrap) == BWRAP_SHA256
assert sha256(Path("/usr/bin/python3")) == PYTHON_SHA256
fixed_env = {
    "HOME": os.environ["HOME"],
    "PATH": f"{toolchain_bin}:/usr/bin:/bin",
    "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}
assert {key: os.environ[key] for key in spec["env_allowlist"]} == spec["env_allowlist"]
assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT, env=fixed_env, timeout=120)
lean_path = run([str(lake), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env, timeout=180).strip()

tmp = Path(tempfile.mkdtemp(prefix="stage1-m1088-validation-", dir="/tmp"))
try:
    for name in lean_files:
        shutil.copy2(HERE / name, tmp / name)
    (tmp / "home").mkdir()

    def isolated_lean(args: list[str], *, module_path: bool = False) -> str:
        path = f"{tmp}:{lean_path}" if module_path else lean_path
        return run(
            [str(lake), "env", "lean", "--trust=0", "-t0", "--root", str(tmp), *args],
            cwd=tmp,
            env={**fixed_env, "HOME": str(tmp / "home"), "LEAN_PATH": path},
        )

    statement_output = isolated_lean(["-o", "Statement.olean", "Statement.lean"])
    obligation_output = isolated_lean(
        ["-o", "ObligationTree.olean", "ObligationTree.lean"], module_path=True
    )
    proof_output = isolated_lean(["Proof.lean"], module_path=True)
    validation_output = isolated_lean(["Validation.lean"], module_path=True)
finally:
    shutil.rmtree(tmp)

composition = "Stage1Instances.THM_M_1088.ObligationTree.target_of_upperTailEngine"
assert reported_axioms(obligation_output, composition) == EXPECTED_AXIOMS
for declaration in PROOF_DECLARATIONS:
    assert reported_axioms(proof_output, declaration) == EXPECTED_AXIOMS
for declaration in VALIDATION_DECLARATIONS:
    assert reported_axioms(validation_output, declaration) == EXPECTED_AXIOMS
assert validation_output.count("Declarations are sorry-free!") == len(VALIDATION_DECLARATIONS)
combined_output = "\n".join((statement_output, obligation_output, proof_output, validation_output))
assert "sorryAx" not in combined_output
assert "declaration uses 'sorry'" not in combined_output
assert "error:" not in combined_output

if receipt is not None and verify_receipt:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["verdict"] == "blocked"
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_statement_sha256"] == EXPECTED_INPUT_HASHES["Statement.lean"]
    assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
    assert receipt["canonical_expression_fingerprint"]["status"] == (
        "fail_closed_missing_canonical_serialization_hash"
    )
    assert receipt["inputs"]["lean_toolchain_sha256"] == TOOLCHAIN_SHA256
    assert receipt["inputs"]["lake_manifest_sha256"] == MANIFEST_SHA256
    assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validator_sha256"] == sha256(Path(__file__).resolve())
    for key, name in (
        ("validation_probe_sha256", "Validation.lean"),
        ("statement_source_sha256", "Statement.lean"),
        ("obligation_tree_source_sha256", "ObligationTree.lean"),
        ("proof_source_sha256", "Proof.lean"),
        ("anchor_audit_sha256", "anchor-audit.md"),
        ("source_crosswalk_sha256", "source-statement-crosswalk.md"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("proof_receipt_sha256", "proof-receipt.json"),
        ("proof_blocker_sha256", "proof-blocker.json"),
        ("proof_validation_sha256", "proof-validation.md"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / name), key
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations",
        )
    }
    assert receipt["recipe"]["covered_obligation_ids"] == []
    result = receipt["result"]
    expected_stdout = [
        "PASS THM-M-1088 network-isolated trust-zero narrow validation",
        "PASS exact statement, conditional composition, four partial proof declarations, and four same-route separate-module declarations replayed",
        "PASS nine axiom reports list exactly propext, Classical.choice, and Quot.sound; all separate-module declarations are sorry-free",
        "PASS frozen hashes and selected clean pinned mathlib provenance; zero frozen obligations closed",
        "OPEN M1088-T-ENGINE/root at M3; proof acceptance, complete provenance/TCB, cold-offline hermetic, and distinct-runner gates fail closed",
    ]
    assert result["recorded_stdout"] == expected_stdout
    assert result["recorded_stdout_sha256"] == hashlib.sha256(
        ("\n".join(expected_stdout) + "\n").encode()
    ).hexdigest()
    assert result["supported_obligation_ids"] == []
    assert result["provisionally_closed_obligation_ids"] == []
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_kernel_closed"] is False
    assert result["root_vector_before"] == result["root_vector_after"] == {
        "H": "H2", "M": "M3", "R": "R4"
    }
    assert result["architectural_remaining_root_cut_set"] == ARCHITECTURAL_ROOT_CUT
    assert result["proof_execution_remaining_root_cut_set"] == PROOF_EXECUTION_CUT
    assert result["complete_transitive_provenance_gate"] == "fail_closed"
    assert result["complete_transitive_tcb_gate"] == "fail_closed"
    assert result["hermetic_cold_offline_gate"] == "fail_closed"
    assert result["independent_verification_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["accepted_state_changed"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1088-PROOF.master_acceptance"
    assert receipt["first_failed_theorem_gate"] == FIRST_THEOREM_GATE
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    worktree = receipt["worktree_state"]
    assert worktree["worker_worktree_reference"] == ".cron/stage1-rev56/workers/slot18"
    tracked_patch = subprocess.run(
        ["git", "diff", "--binary", "--", str(HERE)],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    assert tracked_patch.stderr == b""
    assert worktree["base_target_patch_sha256"] == hashlib.sha256(
        tracked_patch.stdout
    ).hexdigest()
    assert worktree["validation_probe_untracked_patch_sha256"] == untracked_patch_sha256(
        HERE / "Validation.lean"
    )
    assert worktree["validator_untracked_patch_sha256"] == untracked_patch_sha256(
        HERE / "check_validation.py"
    )
    assert worktree["validation_spec_untracked_patch_sha256"] == untracked_patch_sha256(
        HERE / "validation-spec.json"
    )
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == LEAN_SHA256
    assert environment["lake_executable_sha256"] == LAKE_SHA256
    assert environment["python_executable_sha256"] == PYTHON_SHA256
    assert environment["bubblewrap_executable_sha256"] == BWRAP_SHA256
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_remote"] == MATHLIB_REMOTE
    assert environment["mathlib_license_sha256"] == MATHLIB_LICENSE_SHA256
    assert environment["gaussian_basic_source_sha256"] == MATHLIB_SOURCE_HASHES[
        "Mathlib/Probability/Distributions/Gaussian/IsGaussianProcess/Basic.lean"
    ]
    assert environment["gaussian_basic_olean_sha256"] == MATHLIB_OLEAN_HASHES[
        ".lake/build/lib/lean/Mathlib/Probability/Distributions/Gaussian/IsGaussianProcess/Basic.olean"
    ]
    assert environment["subgaussian_source_sha256"] == MATHLIB_SOURCE_HASHES[
        "Mathlib/Probability/Moments/SubGaussian.lean"
    ]
    assert environment["subgaussian_olean_sha256"] == MATHLIB_OLEAN_HASHES[
        ".lake/build/lib/lean/Mathlib/Probability/Moments/SubGaussian.olean"
    ]
    assert environment["umask"] == "inherited_nonrelease_input; not fixed by the recipe"
    assert environment["memory_bound"] == "not enforced; nonrelease limitation"
    assert environment["disk_bound"] == "not enforced; nonrelease limitation"
    trust = receipt["trust"]
    assert set(trust["machine_reported_axioms"]) == EXPECTED_AXIOMS
    assert len(trust["machine_reported_axioms"]) == len(EXPECTED_AXIOMS)
    assert trust["axiom_report_count"] == 9
    assert trust["accepted_foundation_profile"] is False
    assert trust["complete_transitive_declaration_closure"] is False
    assert trust["complete_transitive_tcb_inventory"] is False
    provenance = receipt["provenance"]
    assert provenance["selected_direct_provenance"] == "pass"
    assert provenance["complete_transitive_declaration_and_source_origin_closure"] is False
    assert provenance["root_terminal_proof_body_present"] is False
    assert provenance["root_provenance_closure"] == "open"
    handoff = receipt["worker_handoff"]
    assert handoff["reported_nodes"] == [
        ITEM, "M1088-ROOT", "M1088-T-ENGINE", "M1088-T-ASSEMBLE",
        "M1088-X-PROVENANCE", "M1088-X-TRUST",
    ]
    assert handoff["exact_statements_added_or_changed"] == []
    assert handoff["typed_graph_changes"] == []
    assert handoff["debt_vector_change"] == "none: H2/M3/R4 -> H2/M3/R4"
    assert handoff["source_revisions"] == {
        "repository_base": BASE_REVISION,
        "mathlib": MATHLIB_REVISION,
    }
    hermeticity = receipt["hermeticity"]
    assert hermeticity["decision"] == "fail_closed_nonrelease_warm_cache_replay"
    assert hermeticity["empty_user_package_build_caches"] is False
    assert hermeticity["clean_checkout"] is hermeticity["offline_archive_restoration"] is False
    independence = receipt["independent_validation"]
    assert independence["decision"] == "fail_closed"
    for key in (
        "distinct_runner", "distinct_verifier_identity", "independent_dependency_cache",
        "second_signed_attestation", "independently_implemented_release_verifier",
    ):
        assert independence[key] is False, key
    assert receipt["validation_started_at"] < receipt["validation_ended_at"]
    assert receipt["validated_at"] == receipt["validation_ended_at"]

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    packet = load(selftest_path)
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    if receipt is not None and verify_receipt:
        assert packet["commands"] == receipt["commands"]
        assert packet["output_summary"] == receipt["output_summary"]
        assert packet["known_failures"] == receipt["known_failures"]
    actual_changes = {
        line[3:] for line in run(
            ["git", "status", "--short", "--untracked-files=all"]
        ).splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

print("PASS THM-M-1088 network-isolated trust-zero narrow validation")
print("PASS exact statement, conditional composition, four partial proof declarations, and four same-route separate-module declarations replayed")
print("PASS nine axiom reports list exactly propext, Classical.choice, and Quot.sound; all separate-module declarations are sorry-free")
print("PASS frozen hashes and selected clean pinned mathlib provenance; zero frozen obligations closed")
print("OPEN M1088-T-ENGINE/root at M3; proof acceptance, complete provenance/TCB, cold-offline hermetic, and distinct-runner gates fail closed")
