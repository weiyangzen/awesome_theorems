#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1003-VALIDATION."""

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


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables assertions")

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1003"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1003-VALIDATION"
THEOREM = "THM-M-1003"
BASE_REVISION = "d3d4bc991fae237427b8ac391bbe701dca8f2af2"
BASE_TREE = "51d54892f625b3b42e3b0c2c6b3c8e173c4ad166"
EXPRESSION_SHA256 = "ead76891696316502f96466e97e0ec725b72cb1f2dfdc6d8afa4e405e79b8e9f"
DENOMINATOR_SHA256 = "d44a39b4a9b24a0cce89719cf41820d368483961dc0c2c624423e82136092b3c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_RUNNER_STDOUT_SHA256 = "75d1d32294ae01be69a6154df22a848f40133c36b94356217ffcc4bdc9d7de1f"
EXPECTED_INPUTS = {
    "Statement.lean": "33888546fe909f442a3ddbb47135d7971bfd6d51c4b37daeed3a7b9d720e60ed",
    "ObligationTree.lean": "891b7db831e2de0589105d774a8a5d8f6af30d55e40e498b69dd05d1878d0873",
    "Proof.lean": "2f4c799b985e1f1e404a1d4ccc21669b0e0b58c0e852618d47822373ace8ec61",
    "Validation.lean": "3d21af2e60c1424281eac90e179a6725ebdcc664107b20d7b1851d489a6dbb8f",
    "intake.json": "62bdd19e0e2a8b4824040575c3de954de9db6b102a22d9b8aa987d8a25ee9ada",
    "statement.json": "791452c0e578d97bb79826e57345e4b594cf35d43982d8b98b18c171da52ea88",
    "anchor-audit.json": "e6d8203961305bb6ad6fe20d7dd4925358d99013f3d61240e22bb0787c8c9861",
    "obligation-registry.json": "52127d5da5984ceebefe4169198427c5bb26a24ca853ca0d7f7f8d38e79d942f",
    "typed-graphs.json": "0696933cb20b73c015376d2260be98fdab44576b02d35ff136fdfbf82e821c8d",
    "validation-specs.json": "4ee4e45cadd8e980458482705dc4c9db05d4a90ac1e691319168515eba8267db",
    "proof-receipt.json": "8286e4f01f61368ee41a41c6f05a35bc94581af00f70028f37c7a4db9989ba3f",
    "proof-validation.md": "e482e8748f39542951f6772ccf7fdb39932b303d5374b782fc0572935c30db17",
    "source_statement_crosswalk.md": "7f0898688eadad1e9809eb2ebf5bb27d8830892c8c3fcc1b5c53d691a344719e",
    "check_statement.py": "c75bf0b3e9b819511ac685c8f7116df7bdf80ff8c88f21780f75764924a7ebc5",
    "check_obligation_tree.py": "8023e2b87fbfc2d1f4afed654c44be4b3f8565f587c65bb5ac61251b8c04ddef",
    "check_proof.py": "d5cad1019f225857a0a646a267c9f05ed51e02a467225c83d95c574871e41354",
    "check_proof.sh": "6a2afe5e375becd88650b386cd1c281403f63c3217562492f2eb00b95cd1d5d6",
    "check_validation.sh": "e80bad423fef450c6eb38e0a5e23f0e57b10b600e2a6f1e162809335f8fd2b5a",
    "validation-spec.json": "cbee230289857cde2d5368b2c1cf716b3994ef558f32d07d5895f8c800a6583c",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
DIRECT_IMPORTS = {
    "Mathlib/Probability/Martingale/Convergence": (
        "68bc60388a2ae14add95c6c9f5654079c3371f5c",
        "de1d255ad82ed66e47c970e30d6e833445e0daf460861a103ec4a78d7c113765",
        "93d094ff1f1e083680be60dfa769443129ec28c34632962add797184101edc1f",
    ),
    "Mathlib/MeasureTheory/Function/ConditionalExpectation/CondJensen": (
        "53f435cfad4ea1abe76bed25f056cab4eb12b9b0",
        "470bca2817459705c7321a05f4792316a99fa422ade152b00a0667a1b18ef305",
        "3ae065396838a2ea8dae753c8a8ed6b4d736483060977742430b43452143be4c",
    ),
    "Mathlib/MeasureTheory/Function/LpSeminorm/CompareExp": (
        "859b622e81eb8505ddcac997734bc0885e70ecd2",
        "8c6d4d44000a460d380c2df4ddfa99cb2154e1c590f48d6bc70a9b644bdfb60c",
        "5d2c55f4efb6a841a49cbead01876f559f8fed1cd815ac8e97414c36938e1839",
    ),
    "Mathlib/MeasureTheory/Function/LpSeminorm/LpNorm": (
        "bc7236b725bc93131df93316e7841911686cef2f",
        "706a35af627c0ab2332765e81df84ab218be350ccc35ccdfd5515f99ad6213bb",
        "d6436f2f5a1faee0b50c4840669f9f0b6af0888e29bf347ac040b78886638bfa",
    ),
    "Mathlib/MeasureTheory/Function/SimpleFuncDenseLp": (
        "96154ab299529646b7fde2144095304885614dba",
        "67a5bc192e20cb8cd94f0ed098d5abd02acc9bfbdcc01a1acd58df84a2d10e92",
        "0b07f71ab85dde4af830cd61203e2fd396b9a0c3dcae62c12510e6a8f1224756",
    ),
    "Mathlib/MeasureTheory/Function/UniformIntegrable": (
        "13170b64e80156bdd54c8031e4a9e9720a0974a5",
        "501af1da201834a1540f5bee9fa4dfb6d096faa5768fff1c0d1813c9ab7b5b1c",
        "4da96ae5166e2f9ab20085603c956ced806ecc9a882830ebd55e9f097a58d789",
    ),
}
MACHINE_IDS = [
    "M1003-ROOT", "M1003-S-DEFINITIONS", "M1003-S-BOUNDARY",
    "M1003-S-FOUNDATION", "M1003-N-L1-BOUND", "M1003-B-ENDPOINTS",
    "M1003-C-LIMIT", "M1003-L-AE-LIMIT", "M1003-L-LIMIT-MEMLP",
    "M1003-L-COND-REP", "M1003-L-COND-APPROX", "M1003-T-CANDIDATE",
    "M1003-T-SAME-EXPONENT", "M1003-T-ASSEMBLE",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1003 narrow validation",
    "PASS kernel replay: exact statement, frozen composition, all proof declarations, root, and exact-type probe elaborated under network isolation at trust level zero",
    "PASS trust observation: checked declarations are transitively sorry-free and report exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, proof linkage, direct sources/blobs/oleans, clean mathlib pin, license, and tool identities agree",
    "PASS hygiene: parser-aware sorry checks and a supplemental comment-stripped prohibited-construct scan passed",
    "FAIL CLOSED authority/trust: proof lacks master acceptance; accepted foundation policy, complete transitive declaration/TCB/SBOM closure, H0, and R0 remain open",
    "FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or a deterministic release bundle",
    "FAIL CLOSED independent release: the exact-type probe shares this worker, checkout, proof body, kernel, and cache rather than a distinct signed verifier",
    "audit_complete=false; theorem_complete=false",
)
TIMEOUT_SECONDS = 900.0


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=TIMEOUT_SECONDS, check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).stdout.strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


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
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 283
    assert target["legacy_priority_slot"] == "S1-M-283"
    assert target["theorem_id"] == THEOREM
    assert target["baseline"] == "L0"
    assert target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == "hard_mathlib_anchor_and_wrapper"
    assert target["intake_score"] == 138
    assert target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 283,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-1003-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1003-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal == {
        "backend": "lean4",
        "module": "Stage1_Instances/THM-M-1003/Statement.lean",
        "declaration_or_expression": "Stage1Instances.THM_M_1003.LpMartingaleConvergenceTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "statement_file_sha256": EXPECTED_INPUTS["Statement.lean"],
    }
    assert intake["lifecycle_mode"] == "planned"
    assert intake["root_vector"] == {"human": "H3", "machine": "M3", "readability": "R3"}
    assert registry["root_obligation_id"] == "M1003-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["theorem_complete"] is False

    assert proof_receipt["item_id"] == "S56-M-1003-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["proof_graph_composition"]["all_required_proof_edges_consumed"] is True
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOMS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = re.sub(r"^#print sorries .*?$", "", source, flags=re.MULTILINE)
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    probe = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert "import Proof" in probe
    assert "theorem exactRootTypeProbe" in probe
    assert "assert_no_sorry Stage1Instances.THM_M_1003.Proof.target" in probe

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    for module, (blob, source_hash, olean_hash) in DIRECT_IMPORTS.items():
        assert git("rev-parse", f"HEAD:{module}.lean", cwd=MATHLIB) == blob
        assert sha256(MATHLIB / f"{module}.lean") == source_hash
        assert sha256(MATHLIB / ".lake/build/lib/lean" / f"{module}.olean") == olean_hash

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).stdout.strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).stdout.strip())
    python = Path(os.path.realpath(sys.executable))
    git_path = Path(os.path.realpath(shutil.which("git") or ""))
    bash_path = Path(os.path.realpath(shutil.which("bash") or ""))
    bwrap_path = Path(os.path.realpath(shutil.which("bwrap") or ""))
    assert LEAN_COMMIT in run([str(lean), "--version"]).stdout
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"]).stdout
    expected_tools = {
        lean: "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
        lake: "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
        python: "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
        git_path: "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
        bash_path: "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd",
        bwrap_path: "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
    }
    for tool, expected in expected_tools.items():
        assert tool.is_file() and sha256(tool) == expected, tool

    runner = run(["bash", str(HERE / "check_validation.sh")]).stdout
    assert hashlib.sha256(runner.encode()).hexdigest() == EXPECTED_RUNNER_STDOUT_SHA256
    assert runner.splitlines() == [
        "PASS THM-M-1003 network-isolated trust-zero kernel replay",
        "PASS exact proof/composition/type probe: propext, Classical.choice, Quot.sound",
        "PASS transitive sorry check: all proof declarations and exact-type probe are sorry-free",
    ]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["release_grade"] is False
    assert set(spec["covered_obligation_ids"]) == set(registry["frozen_denominators"]["inventory"])
    assert spec["allowed_observed_axioms"] == EXPECTED_AXIOMS

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1003-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["covered_obligation_ids"] == spec["covered_obligation_ids"]
    assert receipt["validated_declarations"] == spec["covered_declarations"]
    assert receipt["accepted_closed_obligation_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["inputs"]["worker_packet"] == sha256(ROOT / ".stage1-worker-selftest.json")
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_1003.LpMartingaleConvergenceTarget",
        "proof_declaration": "Stage1Instances.THM_M_1003.Proof.target",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    result = receipt["result"]
    assert result["kernel_replay"] == "provisional_pass"
    assert result["network_isolated_trust_zero_replay"] == "pass"
    assert result["observed_axioms"] == EXPECTED_AXIOMS
    assert result["transitive_sorry_check"] == "pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["foundation_and_complete_trust_closure"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["accepted_root_closed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["root_vector_before"] == {"H": "H3", "M": "M4", "R": "R3"}
    assert receipt["root_vector_after_worker_selftest"] == receipt["root_vector_before"]
    assert receipt["first_failed_gate"] == "dependency.S56-M-1003-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert set(receipt["changed_paths"]) == CHANGED_PATHS

    assert packet == {
        "item_id": ITEM,
        "changed_paths": receipt["changed_paths"],
        "commands": receipt["worker_commands"],
        "output_summary": "\n".join(SUMMARY_LINES),
        "base_revision": BASE_REVISION,
        "known_failures": receipt["known_failures"],
        "state": "[_]",
    }
    actual_changes = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        ("\n".join(SUMMARY_LINES) + "\n").encode()
    ).hexdigest()
    assert receipt["output_evidence"]["kernel_runner_stdout_sha256"] == EXPECTED_RUNNER_STDOUT_SHA256
    assert platform.system() == "Linux"

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
