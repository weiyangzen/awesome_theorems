#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1119-RELEASE."""

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
ITEM = "S56-M-1119-RELEASE"
THEOREM = "THM-M-1119"
BASE_REVISION = "78df0e1ce628d7e18e48441678ad85f9552d1b77"
BASE_TREE = "f6355c949fed70817ee3929831406a4b454a0977"
EXPRESSION_SHA256 = "c457bb8081bc2dc5dfdaca2c724ea34eab89491a80e87e78ab2a31fa16c5cf6e"
DENOMINATOR_SHA256 = "fa2c6bc00cb54723662b9dd9796c6b2d04a61865670ed8a15560655429ecbb3c"
PROOF_RECEIPT_SHA256 = "e976e1869ea6ff93e867be58709bd9935941b953bb99ff56e183dddfaba9fce4"
VALIDATION_RECEIPT_SHA256 = "3ce259b1b1d02602be7381964cff33eda8d02ed4d529619d3fd1e4b1e4bb2e64"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_CUT = ["M1119-T-SUBCRITICAL", "M1119-T-SUPERCRITICAL"]
PARTIAL_IDS = ["M1119-S-DEFINITIONS", "M1119-S-BOUNDARY", "M1119-N-MONOTONE"]
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
UPSTREAM_INPUTS = {
    "README.md": "6662ec40ebb819daeddc4d198c0505dff86d53703710cb82a91f29cab5fbb010",
    "instance.json": "5f0c2f37a7ee84203b561647260665fab8d1b36bbf540ca4e216714f0a09d75f",
    "scope-map.md": "712ef7db97efe2e205ddcb533c978c5e45d08b33d414365588b22f3baf971079",
    "source-statement-crosswalk.md": "3a6e9eab5c81d32d34c595b8c8a084b3c7d39f96c76f6369b8cbf7d608026aa5",
    "task-dag.json": "d9a45816c199122ef4740ae5f0f0f2c43bf2a8792abcceeb3e15e8bbf6c68465",
    "statement.json": "f1d5c2a4934a95357b5f081334b243744d287c8a3ecd3b5108cac8dfd1389f2e",
    "anchor-audit.json": "500174fb30ba9488e294e616c60a71204d5855781a7cbbc33740cbcab1125723",
    "obligation-registry.json": "a3a097dc5a79e99538d11b337f170307b456b7f1b493e27e6ea857f7c356b42c",
    "typed-graphs.json": "34080853d80041ae752080c71879ec715e520ef74ef9dbd4fac4de5b30d49604",
    "Statement.lean": "f020e5b38de3a85f6efa0272c98271c1fe49aa2194e21918342a23b58a4e3b86",
    "AnchorAudit.lean": "316d446fb228d97ade1752d3095ece9eb5517d3cdd79f612aaef1783a06f773c",
    "ObligationTree.lean": "ff16eff998fa1e9e4403957f9fc834017d1db317ee910dbb099b769b40b46483",
    "Proof.lean": "f20a21a4783a61350b40e54ad2e45d9660b648d0684009a595077fda7fa0b242",
    "Validation.lean": "7c8744f242fa02ef7c4160241bbf42d1012aada27ff4ad4d1f7d2b525ed472cf",
    "proof-blocker-current.json": "3881527c43bf1b5d4841f20c190130af17742b927058b1555046c9915d7594c6",
    "proof-receipt.json": PROOF_RECEIPT_SHA256,
    "validation-spec.json": "4a716956ba27a57cfdadd70d37db3db5c8633406f7623eef9c28d4a9139ac82b",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "8271d8888746f2ec98638b8ad1bd1865b4ac6cf9c327c17835ea4ff6317c6a92",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "03ab7dd8432c56191e227b2bcf4bea0eb8a54a4b31e5c755a9170e287c68392f",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "72332e44119bdf3b08934766aa909dbce9c4d5547b385cd5dd18990f44a6c616",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}
SUMMARY_LINES = (
    "PASS release reconciliation: current authority and historical receipt inputs are hash-bound",
    "PASS current narrow Lean replay: statement, conditional composer, 13 partial bodies, and 2 differential probes",
    "OPEN exact root: neither one-half threshold inequality is inhabited; accepted obligations remain empty",
    "BLOCKED AUDIT-Z: authority, source/readability review, typed evidence, provenance, and public state are unreconciled",
    "BLOCKED THEOREM-Z: dependency acceptance, root M0, cold/offline, SBOM, independence, bundle, and master gates fail",
)
STARTED = time.monotonic()
TIMEOUT = 900.0


if sys.flags.optimize:
    raise SystemExit("release check failed: Python optimization disables assertions")


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    remaining = TIMEOUT - (time.monotonic() - STARTED)
    if remaining <= 0:
        raise TimeoutError("release recipe exceeded its wall-clock bound")
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=remaining, check=False,
    )
    if check and result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).stdout.strip()


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


def current_changed_paths() -> set[str]:
    status = git("status", "--short", "--untracked-files=all")
    return {line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"}


def main() -> None:
    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    receipt = load(HERE / "release-receipt.json")
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 559 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    release_node = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_node = next(
        row for row in execution["items"] if row["id"] == "S56-M-1119-VALIDATION"
    )
    assert release_node["state"] == "[ ]" and release_node["attempts"] == 0
    assert release_node["depends_on"] == ["S56-M-1119-VALIDATION"]
    assert release_node["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert validation_node["state"] == "[_]" and validation_node["attempts"] == 1

    for name, expected in UPSTREAM_INPUTS.items():
        assert sha256(HERE / name) == expected, name
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, name
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, name

    assert instance["lifecycle"] == tasks["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == tasks["accepted_states"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    local_tasks = {row["id"]: row for row in tasks["tasks"]}
    assert local_tasks["S56-M-1119-VALIDATION"]["state"] == "open"
    assert local_tasks[ITEM]["state"] == "open"
    assert statement["statement_elaborated"] is True
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert anchor["audit_complete"] is True
    assert "only the bounded formal-anchor inventory" in anchor["status_boundary"]
    assert anchor["root_machine_classification"] == "M4"
    assert anchor["theorem_complete"] is False

    ids = registry["frozen_denominators"]["inventory"]
    assert len(ids) == len(set(ids)) == 15
    assert registry["root_obligation_id"] == "M1119-ROOT"
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert {node["obligation_id"] for node in graphs["nodes"]} == set(ids)
    assert all(not node["evidence_ids"] and node["provenance_id"] == "none" for node in graphs["nodes"])
    assert set(graphs["graphs"]) == {"proof", "provenance", "trust", "documentation", "workflow"}
    composer = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1119-T-COMPOSE")
    assert composer["machine_debt"] == "M0-L" and composer["evidence_ids"] == []
    composition_inputs = {
        edge["source"] for edge in graphs["graphs"]["proof"]
        if edge["edge_type"] == "composes" and edge["target"] == "M1119-T-COMPOSE"
    }
    assert composition_inputs == set(ROOT_CUT)

    assert sha256(HERE / "proof-receipt.json") == PROOF_RECEIPT_SHA256
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert proof["support_state"] == validation["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is validation["accepted"] is False
    assert proof["supported_obligation_ids"] == proof["accepted_closed_obligation_ids"] == []
    assert proof["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof["result"]["root_kernel_closed"] is False
    assert validation["release_grade"] is validation["content_addressed_release_evidence"] is False
    assert validation["result"]["supported_obligation_ids"] == []
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_closed"] is validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["accepted_receipt_ids"] == []
    assert validation["remaining_root_cut_set"] == ROOT_CUT
    assert validation["hermeticity"]["decision"] == "fail_closed_nonrelease_warm_cache_replay"
    assert validation["independent_validation"]["decision"] == "fail_closed"

    validation_checker = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert 'BASE_REVISION = "3d3099d0d4002093cf89da97132bdf954605810b"' in validation_checker
    assert 'packet_path = ROOT / ".stage1-worker-selftest.json"' in validation_checker
    stale_validation = run(
        ["/usr/bin/python3", "-B", str(HERE / "check_validation.py")], check=False
    )
    assert stale_validation.returncode != 0
    assert "AssertionError" in stale_validation.stdout

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
        "Validation.lean",
    ):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, name
    validation_code = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert "import Proof" not in validation_code and "import ObligationTree" not in validation_code

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
    toolchain_bin = account_home / ".elan/toolchains/leanprover--lean4---v4.29.0/bin"
    lean = toolchain_bin / "lean"
    lake = toolchain_bin / "lake"
    assert sha256(lean) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(lake) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT).stdout
    fixed_env = {
        "HOME": "/tmp",
        "PATH": f"{toolchain_bin}:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    lean_path = run(
        [str(lake), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env
    ).stdout.strip()
    tmp = Path(tempfile.mkdtemp(prefix="stage1-m1119-release-", dir="/tmp"))
    try:
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()

        def isolated_lean(args: list[str], *, module_path: bool = False) -> str:
            env = dict(fixed_env)
            env["HOME"] = "/tmp/work/home"
            env["LEAN_PATH"] = f"/tmp/work:{lean_path}" if module_path else lean_path
            argv = [
                "/usr/bin/bwrap", "--ro-bind", "/", "/", "--dev", "/dev",
                "--proc", "/proc", "--tmpfs", "/tmp", "--unshare-net",
                "--die-with-parent", "--bind", str(tmp), "/tmp/work",
                "--chdir", "/tmp/work",
                "--clearenv",
            ]
            for key, value in env.items():
                argv += ["--setenv", key, value]
            argv += [str(lean), "--trust=0", "-j1", "-t0", *args]
            return run(argv).stdout

        statement_output = isolated_lean(["-o", "Statement.olean", "Statement.lean"])
        tree_output = isolated_lean(
            ["-o", "ObligationTree.olean", "ObligationTree.lean"], module_path=True
        )
        proof_output = isolated_lean(["Proof.lean"], module_path=True)
        validation_output = isolated_lean(["Validation.lean"], module_path=True)
    finally:
        shutil.rmtree(tmp)

    all_output = statement_output + tree_output + proof_output + validation_output
    assert "error:" not in all_output and "sorryAx" not in all_output
    assert "declaration uses 'sorry'" not in all_output
    assert reported_axioms(
        tree_output, "Stage1Instances.THM_M_1119.kestenTarget_of_threshold_bounds"
    ) == EXPECTED_AXIOMS
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    for declaration in DIFFERENTIAL_DECLARATIONS:
        assert reported_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    assert validation_output.count("Declarations are sorry-free!") == 2

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "/usr/bin/python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["timeout_seconds"] == 900 and spec["covered_obligation_ids"] == []
    assert spec["inspected_obligation_ids"] == ids
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["verdict"] == "blocked" and decision["release_grade"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector_before"] == decision["root_vector_after"] == instance["root_vector"]
    assert decision["audit_complete"] is decision["theorem_complete"] is False
    assert decision["release_accepted"] is False and decision["accepted_receipt_ids"] == []
    assert decision["terminal_decisions"] == {"audit_z": "blocked", "theorem_z": "blocked"}
    assert decision["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert decision["dependency"]["accepted"] is decision["dependency"]["master_accepted"] is False
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_mathematical_gate"]["gate_id"] == (
        "M1119-N-MONOTONE-AND-THRESHOLD-ROOT-CLOSURE"
    )
    assert decision["remaining_root_cut_set"] == ROOT_CUT
    for key in (
        "validation_recipe_fresh_at_integrated_head", "dependency_master_accepted",
        "authoritative_state_reconciled", "accepted_root_m0", "audit_z_accepted",
        "pinpoint_h0_source_review", "independent_r0_review",
        "complete_provenance_foundation_tcb_closure", "immutable_clean_release_input",
        "hermetic_cold_empty_cache_offline_replay", "complete_sbom_license_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "protected_ci_and_adversarial_gates", "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["master_acceptance"] is False
    assert receipt["dependency_receipt"]["sha256"] == VALIDATION_RECEIPT_SHA256
    for name, expected in receipt["upstream_input_bindings"].items():
        assert name in UPSTREAM_INPUTS and expected == sha256(HERE / name), name
    for name, expected in receipt["authority_input_bindings"].items():
        assert name in AUTHORITY_INPUTS and expected == sha256(ROOT / name), name
    for name, expected in receipt["tool_input_bindings"].items():
        assert name in TOOL_INPUTS and expected == sha256(LEAN_ROOT / name), name
    for name in ("release-decision.json", "release-spec.json", "check_release.py", "release-phase.md"):
        assert receipt["release_input_bindings"][name] == sha256(HERE / name), name
    assert receipt["recipe"] == spec
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["root_vector_before"] == receipt["result"]["root_vector_after"] == instance["root_vector"]
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["release_accepted"] is False
    assert receipt["result"]["accepted_receipt_ids"] == []
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
    assert receipt["output_evidence"] == {
        "stream": "stdout",
        "sha256": hashlib.sha256(expected_stdout).hexdigest(),
        "bytes": len(expected_stdout),
        "line_count": len(SUMMARY_LINES),
        "exit_code": 0,
        "classification": "provisional nonrelease negative-decision evidence",
    }

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"] == decision["known_failures"]
    assert packet["commands"] == receipt["worker_command_ledger"]
    assert packet["output_summary"] == receipt["worker_output_summary"]
    assert current_changed_paths() == CHANGED_PATHS
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
