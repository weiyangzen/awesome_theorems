#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1080-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1080"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1080-VALIDATION"
THEOREM = "THM-M-1080"
BASE_REVISION = "3f555cfc0879cb7c42e83d6bcf7b9e3e09997e58"
BASE_TREE = "e8837f7e0722548e2b35e901d9d974797097635e"
PROOF_BASE_REVISION = "fb0fd5be494d0813177dbdc959ec911d69a72015"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "af69d1d82ed31033201ff05a06f14f6fe200307a16bd3538f34ab56d4fd0d350"
DENOMINATOR_SHA256 = "869c1a9abe79908244280909afaadc8e84b294df0d6b1e290b81e5363243df14"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "7c70293edee7d3bfc79ea241f932241483285342ab400e10e8290782666ebda4",
    "AnchorAudit.lean": "895c71ad0a59764dcd797b898cd0da612f0431164066d7a2e8d21f58f7b96694",
    "anchor-audit.json": "6ca6e3bee4db7e77be06a0c1f775c43845b458e81d1ab68d8b1046a857b6a18a",
    "ObligationTree.lean": "ab7794789e88eb86ecf41a7a4356d0126dfde0298af4bf065a2bb0c4466c1d6d",
    "Proof.lean": "8332d6aaa5fc2fd24850bf24864ef2c600abfbb74e5468838df83c9f342d5e9e",
    "ExactRoot.lean": "c87fd2ffbfb88150e1c241ace9e45faaa9f9d25b84831b983b1616c41d5661f8",
    "proof-receipt.json": "5e1334dc3cc7545a3ec20637f7fbbdd724bfbe9c974a612331e26c519366ccfb",
    "statement.json": "362e192f9d4d6a66e4654fb716090fadf1a5f1afe36301d49c8a88b23430a4ed",
    "obligation-registry.json": "2238aecce213657fc484e2cb462d9bdb83d397e98bd753f1631ae6325d51f406",
    "typed-graphs.json": "7663e59aceb59ec263ce79dda260d2ce6be89dab7012cb204ffb015e52df6522",
    "validation-specs.json": "62c6c61b3b8f976b86211e08f6713512148452a1323b6be731d44812d2c0514a",
    "check_statement.py": "23018c19a7a8bdc25ebeb1e0bc667e9e09f3476fff0de54e3085a9d9ff158584",
    "check_obligation_tree.py": "85f5f1cabdd3ebc09a1c7e40db8f1ba0e04866a03f7dc01f84c57fb9223d8d63",
    "Validation.lean": "637eaeedb32d5b27622cdb0598fc618cbe81959565dcf03ecca823746845eca1",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
TOOL_HASHES = {
    "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "lake": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
    "python": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "git": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
    "bash": "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd",
    "bubblewrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
}
MATHLIB_ARTIFACTS = {
    "Mathlib/Probability/Moments/SubGaussian.lean": "1261993867efbddb6781a6ce9d0855335fab6891f819062ac83b8d9f6d94c440",
    ".lake/build/lib/lean/Mathlib/Probability/Moments/SubGaussian.olean": "063f83b186bfdee9417f4eccd88160425c87debf5cfdf8bc829d277ed761497b",
    "LICENSE": "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1",
}
PROVISIONALLY_CLOSED_IDS = {
    "M1080-ROOT", "M1080-S-DEFINITIONS", "M1080-S-SCOPE", "M1080-S-BOUNDARY",
    "M1080-S-FOUNDATION", "M1080-N-INCREMENTS", "M1080-N-TELESCOPE",
    "M1080-C-EXPONENTIAL", "M1080-L-COND-HOEFFDING", "M1080-L-MGF-ITERATE",
    "M1080-L-MARKOV", "M1080-L-OPTIMIZE", "M1080-T-POSITIVE",
    "M1080-T-ZERO", "M1080-T-ASSEMBLE",
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
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate key {key!r} in {path}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
        timeout: int = 1200) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_axioms(output: str, declaration: str) -> None:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)]",
        output, re.DOTALL,
    )
    assert match is not None, (declaration, output)
    observed = {part.strip() for part in match.group(1).split(",")}
    assert observed == EXPECTED_AXIOMS, (declaration, observed)


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
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
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 522,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-1080-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    proof_item = next(row for row in execution["items"] if row["id"] == "S56-M-1080-PROOF")
    assert proof_item["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-1080-PROOF"]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-1080-VALIDATION-narrow-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 1800
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert set(spec["covered_obligation_ids"]) == PROVISIONALLY_CLOSED_IDS

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_1080.Statement"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["proof_body"]["exact_root_sha256"] == EXPECTED_INPUTS["ExactRoot.lean"]
    assert set(proof_receipt["provisionally_closed_proof_obligation_ids"]) == PROVISIONALLY_CLOSED_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["accepted"] is False
    assert git("merge-base", PROOF_BASE_REVISION, BASE_REVISION) == PROOF_BASE_REVISION
    changed_since_proof_base = set(git(
        "diff", "--name-only", f"{PROOF_BASE_REVISION}..{BASE_REVISION}", "--", str(HERE)
    ).splitlines())
    assert changed_since_proof_base == {
        f"Stage1_Instances/{THEOREM}/ExactRoot.lean",
        f"Stage1_Instances/{THEOREM}/Proof.lean",
        f"Stage1_Instances/{THEOREM}/check_proof.py",
        f"Stage1_Instances/{THEOREM}/check_proof.sh",
        f"Stage1_Instances/{THEOREM}/proof-receipt.json",
        f"Stage1_Instances/{THEOREM}/proof-validation.md",
    }
    assert instance["lifecycle"] == "planned"
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == ["M1080-T-ASSEMBLE"]
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b", re.MULTILINE,
    )
    for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "ExactRoot.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    for forbidden in ("import ObligationTree", "import ExactRoot", "azumaUpperTail_exact", "azumaUpperTail_of_threshold_packages"):
        assert forbidden not in differential, forbidden
    assert "using Proof.azumaUpperTail" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert git("rev-parse", "HEAD:Mathlib/Probability/Moments/SubGaussian.lean", cwd=MATHLIB) == "ac725ac480d72031e932c719b3e3fad92e860cc3"
    for relative, expected in MATHLIB_ARTIFACTS.items():
        assert sha256(MATHLIB / relative) == expected, relative
    assert anchor["mathlib"]["revision"] == MATHLIB_REVISION
    assert anchor["mathlib"]["source_sha256"] == MATHLIB_ARTIFACTS["Mathlib/Probability/Moments/SubGaussian.lean"]

    bwrap = Path(os.path.realpath(shutil.which("bwrap") or ""))
    git_path = Path(os.path.realpath(shutil.which("git") or ""))
    bash = Path(os.path.realpath(shutil.which("bash") or ""))
    python = Path(os.path.realpath(sys.executable))
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    tools = {"lean": lean, "lake": lake, "python": python, "git": git_path, "bash": bash, "bubblewrap": bwrap}
    for name, path in tools.items():
        assert path.is_file() and sha256(path) == TOOL_HASHES[name], (name, path)
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()

    with tempfile.TemporaryDirectory(prefix="stage1-m1080-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "ExactRoot.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--setenv", "HOME", "/tmp/stage1-m1080-no-home",
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
            "--chdir", str(tmp),
        ]
        def lean_run(module: str, *, sibling_path: bool = False, output: bool = True) -> str:
            path = f"{tmp}:{lean_path}" if sibling_path else lean_path
            argv = base + ["--setenv", "LEAN_PATH", path, str(lean), "--trust=0", "-t0"]
            if output:
                argv += ["-o", f"{Path(module).stem}.olean"]
            argv += [module]
            return run(argv, timeout=1200)

        statement_output = lean_run("Statement.lean")
        anchor_output = lean_run("AnchorAudit.lean", output=False)
        obligation_output = lean_run("ObligationTree.lean")
        proof_output = lean_run("Proof.lean")
        exact_output = lean_run("ExactRoot.lean", sibling_path=True)
        validation_output = lean_run("Validation.lean", sibling_path=True, output=False)

    assert "AzumaUpperTail" in statement_output and "MutationPositiveThresholdOnly" in statement_output
    anchor_declarations = (
        "ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF",
        "ProbabilityTheory.HasSubgaussianMGF.sum_of_hasCondSubgaussianMGF",
        "ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero",
        "Stage1Instances.THM_M_1080.mathlibConditionalSubgaussianCandidate",
    )
    for declaration in anchor_declarations:
        assert_axioms(anchor_output, declaration)
    assert_axioms(obligation_output, "Stage1Instances.THM_M_1080.ObligationTree.azumaUpperTail_of_threshold_packages")
    proof_declarations = (
        "sum_increment_eq_sub", "exp_secant_bound", "condExp_exp_increment_le",
        "exp_endpoint_integrable", "exp_increment_sum_integral_le", "positiveThreshold",
        "zeroThreshold", "azumaUpperTail",
    )
    for declaration in proof_declarations:
        assert_axioms(proof_output, f"Stage1Instances.THM_M_1080.Proof.{declaration}")
    exact_declarations = ("positiveThresholdPackage", "zeroThresholdPackage", "azumaUpperTail_exact")
    for declaration in exact_declarations:
        assert_axioms(exact_output, f"Stage1Instances.THM_M_1080.ExactRoot.{declaration}")
    assert_axioms(validation_output, "Stage1Instances.THM_M_1080.Proof.azumaUpperTail")
    assert_axioms(validation_output, "Stage1Instances.THM_M_1080.Validation.directExactRoot")
    assert "declaration uses 'sorry'" not in validation_output
    assert "VALIDATION_CLOSURE declarations=" in validation_output
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in validation_output
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in validation_output
    assert "VALIDATION_CLOSURE unsafe=[]" in validation_output
    all_output = anchor_output + obligation_output + proof_output + exact_output + validation_output
    assert "sorryAx" not in all_output and "declaration uses 'sorry'" not in all_output

    statement_check = run(["python3", "-B", str(HERE / "check_statement.py")])
    assert EXPRESSION_SHA256 in statement_check and "mutation distinction: ok" in statement_check
    # The frozen tree checker predates Validation.lean and scans every sibling .lean file for the
    # substring "sorry", including comments and `assert_no_sorry`. Its structural assertions are
    # reproduced above; do not weaken or rewrite that historical phase checker here.

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["release_grade"] is receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["target"] == {
        "canonical_declaration": "Stage1Instances.THM_M_1080.Statement",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    for name, path in tools.items():
        assert receipt["environment"][f"{name}_executable_sha256"] == sha256(path)
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.machine()}"
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "network_enforcement", "expected_exit", "expected_outputs", "covered_obligation_ids",
        "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key]
    result = receipt["result"]
    assert result["exact_root_kernel_closed"] is True
    assert result["observed_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_closed_obligations"] == []
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["same_worker_differential_exact_type_bridge"] == "pass"
    for gate in (
        "dependency_master_acceptance_gate", "complete_provenance_gate", "complete_tcb_gate",
        "hermetic_cold_reproduction_gate", "independent_distinct_runner_gate",
    ):
        assert result[gate] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1080-PROOF.master_acceptance"
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
    status = git("status", "--porcelain=v1", "--untracked-files=all", "--", str(HERE), str(ROOT / ".stage1-worker-selftest.json"))
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for path in (HERE / "validation-receipt.json", HERE / "validation-phase.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("PASS THM-M-1080 narrow validation: exact root and differential exact-type bridge kernel-check under network isolation")
    print("PASS trust observation: 18 local/anchor declarations are sorry-free with the selected classical trio")
    print("PASS pinned provenance subset: target, denominator, source/olean/license, toolchain, mathlib revision/tree/remote, and clean dependency agree")
    print("OPEN accepted state: PROOF remains provisional; accepted H2/M3/R3 and zero accepted obligations remain")
    print("BLOCKED release gates: shared warm cache, incomplete provenance/TCB, and no distinct signed independent verifier")


if __name__ == "__main__":
    main()
