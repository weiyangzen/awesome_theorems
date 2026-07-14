#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1119-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1119"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1119-VALIDATION"
THEOREM = "THM-M-1119"
BASE_REVISION = "3d3099d0d4002093cf89da97132bdf954605810b"
BASE_TREE = "17ea0daeddceb9742a5df33c247d624d2842c520"
EXPRESSION_SHA256 = "c457bb8081bc2dc5dfdaca2c724ea34eab89491a80e87e78ab2a31fa16c5cf6e"
DENOMINATOR_SHA256 = "fa2c6bc00cb54723662b9dd9796c6b2d04a61865670ed8a15560655429ecbb3c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
REMAINING_ROOT_CUT = ["M1119-T-SUBCRITICAL", "M1119-T-SUPERCRITICAL"]
PARTIAL_IDS = ["M1119-S-DEFINITIONS", "M1119-S-BOUNDARY", "M1119-N-MONOTONE"]
EXPECTED_INPUTS = {
    "Statement.lean": "f020e5b38de3a85f6efa0272c98271c1fe49aa2194e21918342a23b58a4e3b86",
    "AnchorAudit.lean": "316d446fb228d97ade1752d3095ece9eb5517d3cdd79f612aaef1783a06f773c",
    "ObligationTree.lean": "ff16eff998fa1e9e4403957f9fc834017d1db317ee910dbb099b769b40b46483",
    "Proof.lean": "f20a21a4783a61350b40e54ad2e45d9660b648d0684009a595077fda7fa0b242",
    "statement.json": "f1d5c2a4934a95357b5f081334b243744d287c8a3ecd3b5108cac8dfd1389f2e",
    "anchor-audit.json": "500174fb30ba9488e294e616c60a71204d5855781a7cbbc33740cbcab1125723",
    "obligation-registry.json": "a3a097dc5a79e99538d11b337f170307b456b7f1b493e27e6ea857f7c356b42c",
    "typed-graphs.json": "34080853d80041ae752080c71879ec715e520ef74ef9dbd4fac4de5b30d49604",
    "proof-receipt.json": "e976e1869ea6ff93e867be58709bd9935941b953bb99ff56e183dddfaba9fce4",
    "proof-blocker-current.json": "3881527c43bf1b5d4841f20c190130af17742b927058b1555046c9915d7594c6",
    "proof-validation.md": "12075d97f18b594a6e001f0f254132637df4de75d6af189b53c407b49da715ed",
    "source-statement-crosswalk.md": "3a6e9eab5c81d32d34c595b8c8a084b3c7d39f96c76f6369b8cbf7d608026aa5",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_1119.openGraph_adj_of_open",
    "Stage1Instances.THM_M_1119.openGraph_mono",
    "Stage1Instances.THM_M_1119.originInInfiniteCluster_mono",
    "Stage1Instances.THM_M_1119.openGraph_reachable_of_walk",
    "Stage1Instances.THM_M_1119.measurable_openGraph_reachable",
    "Stage1Instances.THM_M_1119.measurable_originInInfiniteCluster",
    "Stage1Instances.THM_M_1119.bondMeasure_one_eq_dirac",
    "Stage1Instances.THM_M_1119.originInInfiniteCluster_allOpen",
    "Stage1Instances.THM_M_1119.one_mem_positiveParameters",
    "Stage1Instances.THM_M_1119.criticalProbability_le_one",
    "Stage1Instances.THM_M_1119.bondMeasure_zero_eq_dirac",
    "Stage1Instances.THM_M_1119.percolationProbability_zero",
    "Stage1Instances.THM_M_1119.zero_not_mem_positiveParameters",
)
DIFFERENTIAL_DECLARATIONS = (
    "Stage1Instances.THM_M_1119.Validation.differentialOpenGraphMono",
    "Stage1Instances.THM_M_1119.Validation.differentialBondMeasureZeroEqDirac",
)
SUMMARY_LINES = (
    "PASS THM-M-1119 network-isolated trust-zero replay of the frozen statement, conditional composer, and 13 partial proof declarations",
    "PASS differential validation: two no-proof-import elementary probes elaborate and are sorry-free",
    "PASS observed trust: all checked declarations use only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen local hashes and clean pinned mathlib revision, tree, origin, and license agree",
    "OPEN exact root: neither one-half threshold inequality is inhabited; zero frozen obligations are closed",
    "BLOCKED release gates: proof dependency/root closure, complete provenance/TCB, cold empty-cache replay, and distinct-runner verification",
)
RECIPE_ARGV = [
    "/usr/bin/bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
    "--tmpfs", "/tmp", "--unshare-net", "--die-with-parent", "--clearenv",
    "--setenv", "HOME", "/tmp", "--setenv", "PATH", "/usr/bin:/bin",
    "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
    "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
    "/usr/bin/python3", "-I", "-B",
    "Stage1_Instances/THM-M-1119/check_validation.py",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-1119/Validation.lean",
    "Stage1_Instances/THM-M-1119/check_validation.py",
    "Stage1_Instances/THM-M-1119/validation-phase.md",
    "Stage1_Instances/THM-M-1119/validation-receipt.json",
    "Stage1_Instances/THM-M-1119/validation-spec.json",
}
STARTED = time.monotonic()
TIMEOUT = 1200.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables assertions")


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


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    remaining = TIMEOUT - (time.monotonic() - STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its wall-clock bound")
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=remaining, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
    while index < len(source):
        if source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            index += 1
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL)
    matches = pattern.findall(output)
    assert len(matches) == 1, declaration
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def expected_changed_paths() -> set[str]:
    status = run(["/usr/bin/git", "status", "--short", "--untracked-files=all"])
    return {line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"}


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    instance = load(HERE / "instance.json")
    anchor = load(HERE / "anchor-audit.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker-current.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    receipt_path = HERE / "validation-receipt.json"
    receipt = load(receipt_path) if receipt_path.exists() else None
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = load(packet_path) if packet_path.exists() else None
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 559 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 559,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1119-PROOF"],
        "owned_paths": ["Stage1_Instances/THM-M-1119"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1119-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    assert registry["root_obligation_id"] == "M1119-ROOT"
    obligations = registry["obligations"]
    assert len(obligations) == 15 and len({row[0] for row in obligations}) == 15
    assert registry["frozen_denominators"]["inventory"] == [row[0] for row in obligations]
    root_row = next(row for row in obligations if row[0] == "M1119-ROOT")
    assert root_row[7] == f"lean-expression-sha256:{EXPRESSION_SHA256}"
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert {node["obligation_id"] for node in graphs["nodes"]} == {row[0] for row in obligations}
    assert all(not node["evidence_ids"] for node in graphs["nodes"])
    composition = {
        edge["source"] for edge in graphs["graphs"]["proof"]
        if edge["edge_type"] == "composes" and edge["target"] == "M1119-T-COMPOSE"
    }
    assert composition == set(REMAINING_ROOT_CUT)
    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert anchor["root_machine_classification"] == "M4"
    assert anchor["theorem_proved"] is anchor["theorem_complete"] is False
    assert proof_receipt["item_id"] == "S56-M-1119-PROOF"
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["root_closed"] is blocker["theorem_complete"] is False
    assert blocker["remaining_root_cut_set"] == REMAINING_ROOT_CUT

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        assert prohibited.search(code_without_comments((HERE / name).read_text(encoding="utf-8"))) is None, name
    validation_code = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert "import Proof" not in validation_code and "import ObligationTree" not in validation_code
    for declaration in ("differentialOpenGraphMono", "differentialBondMeasureZeroEqDirac"):
        assert f"assert_no_sorry {declaration}" in validation_code

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["argv"] == RECIPE_ARGV
    assert spec["env_allowlist"] == {
        "HOME": "/tmp", "PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_NUM_THREADS": "1",
    }
    assert spec["timeout_seconds"] == 1200 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0 and spec["covered_obligation_ids"] == []
    assert spec["validated_partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    expected_covered = {
        "Stage1Instances.THM_M_1119.KestenTarget",
        "Stage1Instances.THM_M_1119.kestenTarget_iff_expandedTarget",
        "Stage1Instances.THM_M_1119.kestenTarget_of_threshold_bounds",
        *PROOF_DECLARATIONS,
        *DIFFERENTIAL_DECLARATIONS,
    }
    assert set(spec["covered_declarations"]) == expected_covered
    assert len(spec["covered_declarations"]) == len(expected_covered)

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    account_home = Path(pwd.getpwuid(os.getuid()).pw_dir)
    toolchain_bin = account_home / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin"
    lean = toolchain_bin / "lean"
    lake = toolchain_bin / "lake"
    assert sha256(lean) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(lake) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(Path("/usr/bin/python3")) == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    assert sha256(Path("/usr/bin/git")) == "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
    assert sha256(Path("/usr/bin/bwrap")) == "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
    assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], cwd=LEAN_ROOT)
    fixed_env = {
        "HOME": "/tmp",
        "PATH": f"{toolchain_bin}:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    lean_path = run([str(lake), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env).strip()

    tmp = Path(tempfile.mkdtemp(prefix="stage1-m1119-validation-", dir="/tmp"))
    try:
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()

        def isolated_lean(args: list[str], *, module_path: bool = False) -> str:
            env = dict(fixed_env)
            env["HOME"] = str(tmp / "home")
            env["LEAN_PATH"] = f"{tmp}:{lean_path}" if module_path else lean_path
            return run([str(lean), "--trust=0", "-j1", "-t0", *args], cwd=tmp, env=env)

        statement_output = isolated_lean(["-o", "Statement.olean", "Statement.lean"])
        tree_output = isolated_lean(["-o", "ObligationTree.olean", "ObligationTree.lean"], module_path=True)
        proof_output = isolated_lean(["Proof.lean"], module_path=True)
        validation_output = isolated_lean(["Validation.lean"], module_path=True)
    finally:
        shutil.rmtree(tmp)

    assert "error:" not in statement_output + tree_output + proof_output + validation_output
    assert reported_axioms(
        tree_output, "Stage1Instances.THM_M_1119.kestenTarget_of_threshold_bounds"
    ) == EXPECTED_AXIOMS
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    for declaration in DIFFERENTIAL_DECLARATIONS:
        assert reported_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    assert validation_output.count("Declarations are sorry-free!") == 2
    all_output = tree_output + proof_output + validation_output
    assert "declaration uses 'sorry'" not in all_output and "sorryAx" not in all_output

    assert receipt is not None and packet is not None
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1119-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_1119.KestenTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
        "exact_statement_delta": "none",
    }
    repository_state = receipt["repository_state"]
    assert repository_state["base_revision"] == BASE_REVISION
    assert repository_state["base_tree"] == BASE_TREE
    assert repository_state["initial_tracked_patch_sha256"] == hashlib.sha256(b"").hexdigest()
    link_text = os.readlink(LEAN_ROOT / ".lake").encode("utf-8")
    assert repository_state["preexisting_untracked_input_link_text_sha256"] == (
        hashlib.sha256(link_text).hexdigest()
    )
    assert repository_state["accepted_state_changed"] is False
    assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validator_sha256"] == sha256(Path(__file__).resolve())
    assert receipt["inputs"]["validation_probe_sha256"] == sha256(HERE / "Validation.lean")
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["recipe"] == spec
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
    assert receipt["output_evidence"] == {
        "stream": "stdout",
        "sha256": hashlib.sha256(expected_stdout).hexdigest(),
        "bytes": len(expected_stdout),
        "line_count": len(SUMMARY_LINES),
        "exit_code": 0,
        "archive_classification": (
            "nonrelease semantic log digest; transient raw log is not a release archive"
        ),
    }
    assert receipt["trust"]["trust_level"] == 0
    assert receipt["trust"]["validated_existing_declarations"] == 14
    assert receipt["trust"]["differential_declarations"] == list(DIFFERENTIAL_DECLARATIONS)
    assert receipt["trust"]["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["trust"]["accepted_foundation_profile"] is False
    assert receipt["trust"]["complete_transitive_trust_closure"] is False
    environment = receipt["environment"]
    assert environment["lean_commit"] == LEAN_COMMIT
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["bubblewrap_executable_sha256"] == sha256(Path("/usr/bin/bwrap"))
    assert environment["python_executable_sha256"] == sha256(Path("/usr/bin/python3"))
    assert environment["git_executable_sha256"] == sha256(Path("/usr/bin/git"))
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_origin"] == MATHLIB_REMOTE
    assert environment["mathlib_license_sha256"] == MATHLIB_LICENSE_SHA256
    assert environment["mathlib_source_clean"] is True
    assert receipt["provenance"]["proof_dependency_master_accepted"] is False
    assert receipt["provenance"]["complete_terminal_body_import_dependency_source_and_tcb_closure"] is False
    assert receipt["provenance"]["root_provenance_closure"] == "open"
    assert receipt["hermeticity"]["decision"] == "fail_closed_nonrelease_warm_cache_replay"
    assert receipt["hermeticity"]["fresh_clean_checkout"] is False
    assert receipt["hermeticity"]["empty_user_package_and_build_caches"] is False
    assert receipt["hermeticity"]["cold_dependency_rebuild"] is False
    assert receipt["independent_validation"]["decision"] == "fail_closed"
    for key in (
        "distinct_verifier_identity", "independently_provisioned_clean_runner",
        "independent_writable_cache", "second_signed_attestation",
        "independently_implemented_minimal_release_verifier",
    ):
        assert receipt["independent_validation"][key] is False
    result = receipt["result"]
    assert result["validated_partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert result["supported_obligation_ids"] == []
    assert result["provisionally_closed_obligation_ids"] == []
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_closed"] is result["root_kernel_closed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["root_vector_before"] == result["root_vector_after"] == {
        "H": "H2", "M": "M4", "R": "R4"
    }
    assert result["debt_vector_change_proposed"] is False
    assert result["accepted_state_changed"] is False
    for key in (
        "complete_transitive_provenance_gate", "complete_transitive_tcb_gate",
        "hermetic_release_gate", "independent_verification_gate",
    ):
        assert result[key] == "fail_closed"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["first_failed_gate"] == (
        "dependency.S56-M-1119-PROOF.master_acceptance_and_M1119-N-MONOTONE.root_closure"
    )
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    assert receipt["first_failed_mathematical_gate"] == (
        "M1119-N-MONOTONE: no parameter coupling or critical-infimum reduction reaches "
        "either exact one-half threshold inequality"
    )
    assert receipt["remaining_root_cut_set"] == REMAINING_ROOT_CUT
    assert receipt["known_failures"] == packet["known_failures"]
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["output_summary"] == receipt["worker_output_summary"]
    assert packet["commands"] == receipt["worker_command_ledger"]
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert len(packet["changed_paths"]) == len(CHANGED_PATHS)
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert len(receipt["changed_paths"]) == len(CHANGED_PATHS)
    assert expected_changed_paths() == CHANGED_PATHS

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
