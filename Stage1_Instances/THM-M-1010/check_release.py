#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1010-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1010"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1010-RELEASE"
THEOREM = "THM-M-1010"
BASE_REVISION = "43f55bb87aa8883be277a6660f49c6f8ba647082"
BASE_TREE = "8e624c67ebaa9cd00a352276e1fca6d17c18e0b9"
VALIDATION_BASE_REVISION = "fd995645725ec3633e4da7e6d759deb14f530861"
EXPRESSION_SHA256 = "f5f12340fa49d0be0eed038c99c47c921017284447b4a73f4b096e085e800d18"
DENOMINATOR_SHA256 = "8cf08f666cc9a074319f3cd4a905f2f94deedbe62f344fb3554399f3f5d16016"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
ALL_OBLIGATIONS = [
    "M1010-ROOT", "M1010-S-DEFINITIONS", "M1010-S-DOMAIN",
    "M1010-S-BOUNDARY", "M1010-S-FOUNDATION", "M1010-N-PARTITIONS",
    "M1010-C-INTERVAL", "M1010-C-COUPLING", "M1010-L-MEASURABLE",
    "M1010-L-LAWS", "M1010-L-AE-STABILIZE",
    "M1010-L-METRIC-CONVERGENCE", "M1010-T-ASSEMBLE",
    "M1010-X-SOURCE", "M1010-X-PROVENANCE",
]
OPEN_ROOT_CUT = [
    "M1010-N-PARTITIONS", "M1010-C-INTERVAL", "M1010-L-MEASURABLE",
    "M1010-L-LAWS", "M1010-L-AE-STABILIZE",
]
REPLAY_DECLARATIONS = [
    "Stage1Instances.THM_M_1010.exists_common_space_exact_marginals",
    "Stage1Instances.THM_M_1010.representation_of_constant_laws",
    "Stage1Instances.THM_M_1010.target_for_constant_sequence",
    "Stage1Instances.THM_M_1010.ObligationTree.target_of_couplingPackage",
]
RECONCILED_INPUTS = {
    "intake.json": "240164e6be84d6c5e9c84d5ececae3e5faae64abf48e6cd04a0a0653fb395669",
    "README.md": "57b242a89e5b5b72060e31c7df7f46db98b595cdda6a683ee63fd47064471c7f",
    "source_statement_crosswalk.md": "1a77c2b328bf4f935ae32368a40c7652829ddcbc3687fc008c22503d3222d31d",
    "Statement.lean": "79eada2911ea773a8fffd02d59d67f49c1e43cb091c7510d563afeed57994f94",
    "statement.json": "6c9cc2af8cc6c80be42d5a4d3acc7c4995f1664f428be6daf4dcd317424b5cc8",
    "anchor_audit.json": "fa466dc83c1678d016a346dc095b22cfaab3921a65ea33dbaa386cab3ffc0cea",
    "obligation-registry.json": "4b40bc6a126f1e76f43a83c5c77610fd1d0bf7c6ab4d83ed5a4cf61eb5dae7e4",
    "typed-graphs.json": "142369c75e6b0eae8d7ad7248210866727b6c9b33d800cb86e3b8776cd9b6afd",
    "task-dag.json": "eb2823f75fc1865b4f73a8f08ec6c50e9a92a4dcaf18c37a8dafdd201e821e4b",
    "ObligationTree.lean": "a52bc1afbf854c891abacb7da1acc8f074351b3f8f88e1676a7e0b54b6f5d6d6",
    "Proof.lean": "e652a54085931d125e1fa5ea7c73329fc46728c5e673a29e264af65914f79ca5",
    "proof-receipt.json": "3f4ccf395ddf5a73b5e4787dcdd41cf1cd1a388eb9893e08e02bd3fb286f63b1",
    "proof-validation.md": "8d202034070dd0c8785687467d662adf523b2c6018bb0bea68db07a4081fb150",
    "check_proof.sh": "0792f4c273a910ef5fe562bd00f62cfd016745f662bc882d86ebbf4769c0ba80",
    "Validation.lean": "1797a5735f1cd6ed8cbc25ab41afa1f490da572d3ac6b904e9d68f154fe2978e",
    "validation-spec.json": "8061311e491ab3572dc7d097cf76b55eb3ec8c313f8b35f489875b6abdecee4d",
    "validation-receipt.json": "7c1dd6049751cc4fa423f6701a5d80a60189a2a7502fafecc1a7ea9807a54a7a",
    "validation-blocker.json": "5627136104f5cf68516c7fe3e200de3edc340f7554eeca988be98c8392e5b06f",
    "validation-phase.md": "5b409b9e5e25b0ad2a8da0bba0f4d30e4b7b0d1419e6c7093aac6b3e2d5ed05b",
    "check_validation.py": "a9e132998bf09d6051c1c8bf772833ed1b99026944d74fcd41d9f5f000ec309e",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "766c3bf75d97610b12a4f9cde8e66025aaf797bf202ce7b4b5a8636974fefb07",
    "Docs/Stage1_Blueprint_rev-5.6.md": "36d906d91c931d074038112ab5eb971b88930b78d3938847442e97560f02357c",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = [
    "PASS release inputs: target, DAG, receipts, registry, graph, and hashes agree",
    "PASS current narrow Lean replay: exact statement, conditional composer, and three partial bodies checked under trust zero",
    "PASS fail-closed authority: planned H1/M3/R3; five-node root cut; accepted receipts 0",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional, nonrelease, and unaccepted",
    "BLOCKED exact root, AUDIT-Z, trust/provenance, cold/offline, and independent release gates",
    "verdict=blocked audit_complete=false theorem_complete=false",
]


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900, expected_exit: int = 0,
) -> str:
    try:
        result = subprocess.run(
            argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as error:
        fail(f"command timed out: {argv!r}\n{error.stdout or ''}")
    require(
        result.returncode == expected_exit,
        f"command exited {result.returncode}, expected {expected_exit}: {argv!r}\n{result.stdout}",
    )
    return result.stdout


def controlled_env() -> dict[str, str]:
    path = os.environ.get("PATH")
    home = os.environ.get("HOME")
    require(bool(path) and bool(home), "PATH or HOME is unavailable")
    return {
        "PATH": path or "", "HOME": home or "", "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_NUM_THREADS": "1",
        "PYTHONOPTIMIZE": "0",
    }


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, env=controlled_env(), timeout=60).strip()


def source_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if not in_string and source.startswith("/-", index):
            depth += 1
            output.extend("  ")
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            output.extend("  ")
            index += 2
        elif depth:
            output.append("\n" if source[index] == "\n" else " ")
            index += 1
        elif not in_string and source.startswith("--", index):
            end = source.find("\n", index)
            end = len(source) if end < 0 else end
            output.extend(" " * (end - index))
            index = end
        elif source[index] == '"':
            in_string = not in_string
            output.append(" ")
            index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if source[index] == "\n" else " ")
                index += 1
        else:
            output.append(source[index])
            index += 1
    require(depth == 0 and not in_string, "unterminated Lean comment or string")
    return "".join(output)


def axiom_reports(output: str) -> dict[str, list[str]]:
    matches = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL)
    return {
        name: [part.strip() for part in raw.split(",") if part.strip()]
        for name, raw in matches
    }


def current_kernel_replay() -> tuple[str, dict[str, str]]:
    """Replay the current nonroot declarations in a network-isolated temp tree."""

    env = controlled_env()
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=env).strip())
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=env,
    ).strip()
    version = run([str(lean), "--version"], env=env, timeout=60)
    require("4.29.0" in version and "98dc76e3c0a9b856c9b98726b713fb04fab16740" in version,
            "unexpected Lean executable")

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m1010-release-") as tmp_name:
        tmp = Path(tmp_name).resolve()
        module_dir = tmp / "Stage1_Instances" / THEOREM
        module_dir.mkdir(parents=True)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (module_dir / name).write_bytes((HERE / name).read_bytes())
        (tmp / "home").mkdir()
        replay_env = env.copy()
        replay_env["HOME"] = str(tmp / "home")
        base = [str(lean), "--trust=0", "-t0", "-R", str(tmp)]
        outputs["Statement.lean"] = run(base + [
            "-o", str(module_dir / "Statement.olean"), str(module_dir / "Statement.lean"),
        ], cwd=tmp, env={**replay_env, "LEAN_PATH": lean_path})
        module_path = f"{tmp}:{lean_path}"
        outputs["ObligationTree.lean"] = run(base + [
            "-o", str(module_dir / "ObligationTree.olean"), str(module_dir / "ObligationTree.lean"),
        ], cwd=tmp, env={**replay_env, "LEAN_PATH": module_path})
        outputs["Proof.lean"] = run(base + [
            "-o", str(module_dir / "Proof.olean"), str(module_dir / "Proof.lean"),
        ], cwd=tmp, env={**replay_env, "LEAN_PATH": module_path})
        outputs["Validation.lean"] = run(base + [
            str(module_dir / "Validation.lean"),
        ], cwd=tmp, env={**replay_env, "LEAN_PATH": module_path})

    proof_reports = axiom_reports(outputs["Proof.lean"])
    validation_reports = axiom_reports(outputs["Validation.lean"])
    require(set(proof_reports) == set(REPLAY_DECLARATIONS[:3]), "proof axiom coverage drifted")
    require(set(validation_reports) == set(REPLAY_DECLARATIONS), "validation axiom coverage drifted")
    for reports in (proof_reports, validation_reports):
        for declaration, axioms in reports.items():
            require(axioms == EXPECTED_AXIOMS, f"axiom closure drifted: {declaration}")
    combined = "\n".join(outputs.values())
    require(outputs["Validation.lean"].count("Declarations are sorry-free!") == 4,
            "validation sorry checks did not all pass")
    require("declaration uses 'sorry'" not in combined and "sorryAx" not in combined,
            "Lean replay observed a placeholder")
    require(all("error:" not in output for output in outputs.values()),
            "Lean replay observed an error")
    closure = re.search(
        r"VALIDATION_CLOSURE roots=(\d+) declarations=(\d+) modules=(\d+)",
        outputs["Validation.lean"],
    )
    require(closure is not None and closure.group(1) == "4", "validation closure drifted")
    require("VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["Validation.lean"],
            "bodyless nonaxiom found")
    require("VALIDATION_CLOSURE unsafe=[]" in outputs["Validation.lean"],
            "unsafe declaration found")
    return combined, outputs


def main() -> None:
    require(not sys.flags.optimize, "optimized Python disables fail-closed checks")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor_audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    tasks = load(HERE / "task-dag.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    require(git("rev-parse", "HEAD") == BASE_REVISION, "base revision drifted")
    require(git("rev-parse", "HEAD^{tree}") == BASE_TREE, "base tree drifted")
    run(["git", "merge-base", "--is-ancestor", VALIDATION_BASE_REVISION, BASE_REVISION],
        env=controlled_env(), timeout=60)
    for name, expected in RECONCILED_INPUTS.items():
        require(digest(HERE / name) == expected, f"reconciled input drifted: {name}")
    for name, expected in AUTHORITY_INPUTS.items():
        require(digest(ROOT / name) == expected, f"authority input drifted: {name}")
    require(decision["reconciled_inputs"] == RECONCILED_INPUTS,
            "decision input ledger drifted")
    require(decision["authority_inputs"] == AUTHORITY_INPUTS,
            "decision authority ledger drifted")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    require(target == {
        "execution_rank": 290, "legacy_priority_slot": "S1-M-290",
        "theorem_id": THEOREM, "name": "Skorokhod表示定理",
        "category": "概率论与随机过程 / 概率论基础", "source_status_untrusted": "已验证",
        "baseline": "L0", "rework_required": True, "legacy_artifacts_accepted": False,
        "target_lane": "hard_mathlib_anchor_and_wrapper", "intake_score": 138,
        "lifecycle_mode": "planned", "theorem_complete": False,
    }, "target authority drifted")
    items = {row["id"]: row for row in execution["items"]}
    require(items[ITEM] == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 290,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1010-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }, "release execution item drifted")
    require(items["S56-M-1010-VALIDATION"]["state"] == "[_]"
            and items["S56-M-1010-VALIDATION"]["attempts"] == 1,
            "validation dependency is not worker-provisional")

    vector = {"H": "H1", "M": "M3", "R": "R3"}
    require(intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False,
            "intake lifecycle drifted")
    require(intake["root_vector"] == {
        "human": "H1", "machine": "M3", "readability": "R3",
    }, "intake root vector drifted")
    require(statement["elaborated_expression_sha256"] == EXPRESSION_SHA256,
            "canonical expression drifted")
    require(statement["theorem_complete"] is False, "statement claims completion")
    require(anchor["exact_root_candidate"] is None and anchor["theorem_complete"] is False,
            "anchor audit claims an exact root")
    require(registry["root_obligation_id"] == "M1010-ROOT"
            and registry["denominator_sha256"] == DENOMINATOR_SHA256,
            "registry identity drifted")
    require(registry["frozen_denominators"]["inventory"] == ALL_OBLIGATIONS,
            "obligation inventory drifted")
    require(graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256,
            "graph/registry denominator mismatch")
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1010-ROOT")
    require({"H": root["human_debt"], "M": root["machine_debt"],
             "R": root["readability_debt"]} == vector, "graph vector drifted")
    require(root["evidence_ids"] == [], "root gained accepted evidence")
    closure = graphs["closure_boundary"]
    require(closure["root_closed"] is closure["audit_complete"] is False
            and closure["theorem_complete"] is False, "graph claims terminal closure")
    require(closure["remaining_root_cut_set"] == OPEN_ROOT_CUT,
            "root cut drifted")
    require(tasks["tasks"][-1]["state"] == "open", "proof task is not open")

    require(proof["support_state"] == "provisional_worker_selftest"
            and proof["accepted"] is False, "proof became accepted")
    require(proof["accepted_closed_obligation_ids"] == []
            and proof["result"]["root_kernel_closed"] is False
            and proof["result"]["theorem_complete"] is False,
            "proof claims root completion")
    require(validation["support_state"] == "provisional_worker_selftest"
            and validation["accepted"] is validation["release_grade"] is False,
            "validation became accepted or release grade")
    require(validation["base_revision"] == VALIDATION_BASE_REVISION,
            "validation base drifted")
    require(validation["accepted_closed_obligation_ids"] == []
            and validation["result"]["root_kernel_closed"] is False
            and validation["result"]["audit_complete"] is False
            and validation["result"]["theorem_complete"] is False,
            "validation claims terminal closure")

    require(decision["schema_version"] == "stage1-release-decision/1.0",
            "decision schema drifted")
    require(decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM,
            "decision identity drifted")
    require(decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE,
            "decision base drifted")
    require(decision["decision_support"] == "provisional_worker_selftest"
            and decision["proposed_state"] == "[_]", "decision support drifted")
    require(decision["verdict"] == "blocked" and decision["release_accepted"] is False,
            "release verdict is not blocked")
    require(decision["lifecycle_before"] == decision["lifecycle_after"] == "planned",
            "blocked release advanced lifecycle")
    require(decision["accepted_receipt_ids"] == []
            and decision["accepted_closed_obligation_ids"] == [],
            "worker accepted evidence")
    require(decision["root_vector"]["authoritative_before"] == ["H1", "M3", "R3"]
            and decision["root_vector"]["authoritative_after"] == ["H1", "M3", "R3"],
            "release silently changed the root vector")
    require(decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked",
    }, "terminal decisions are not fail closed")
    require(decision["first_failed_gate"]["gate_id"]
            == "S56-10.2-DEPENDENCY-ACCEPTANCE", "first workflow gate drifted")
    require(decision["first_failed_theorem_gate"]["gate_id"]
            == "M1010-N-PARTITIONS", "first theorem gate drifted")
    require(decision["first_failed_release_gate"]["gate_id"]
            == "S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE",
            "first release assurance gate drifted")
    require(decision["first_failed_reproduction_gate"]["gate_id"]
            == "S56-10.6-HERMETIC-COLD-BUILD", "first reproduction gate drifted")
    require(decision["remaining_root_cut_set"] == OPEN_ROOT_CUT,
            "decision root cut drifted")
    for key in (
        "validation_dependency_master_accepted", "predecessor_recipe_current",
        "exact_root_kernel_closed", "authoritative_graph_reconciled",
        "audit_inventory_complete_and_accepted", "pinpoint_h0_and_independent_source_review",
        "independent_r0_review", "accepted_foundation_policy",
        "complete_transitive_provenance_foundation_tcb", "immutable_clean_release_input",
        "hermetic_cold_offline_replay", "sbom_license_offline_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "protected_ci_and_required_adversarial_gates",
        "deterministic_content_addressed_release_bundle", "master_acceptance",
    ):
        require(decision["evidence_reconciliation"][key] is False,
                f"release cleared {key}")

    replay = decision["predecessor_recipe_replay"]
    require(replay["exit_code"] == 1
            and replay["classification"] == "expected_freshness_failure"
            and replay["result"] == "blocked_before_lean_replay",
            "stale predecessor recipe was hidden")
    validation_source = (HERE / "check_validation.py").read_text(encoding="utf-8")
    require(f'BASE_REVISION = "{VALIDATION_BASE_REVISION}"' in validation_source,
            "predecessor base binding drifted")
    require('"state": "[ ]"' in validation_source and '"attempts": 0' in validation_source,
            "predecessor old DAG binding drifted")

    require(spec["schema_version"] == "stage1-validation-recipe/1.0",
            "release spec schema drifted")
    require(spec["item_id"] == receipt["item_id"] == ITEM
            and spec["theorem_id"] == receipt["theorem_id"] == THEOREM,
            "spec/receipt identity drifted")
    require(spec["argv"] == [
        "bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
        "--tmpfs", "/tmp", "--unshare-net", "--die-with-parent",
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
    ], "release recipe argv drifted")
    require(spec["cwd"] == "." and spec["network_policy"] == "denied"
            and spec["timeout_seconds"] == 900 and spec["expected_exit"] == 0,
            "release recipe contract drifted")
    require(spec["covered_obligation_ids"] == ALL_OBLIGATIONS,
            "release recipe misses a frozen obligation")
    require(spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"],
            "release recipe misses a terminal decision")

    require(receipt["schema_version"] == "stage1-node-receipt/1.0",
            "receipt schema drifted")
    require(receipt["support_state"] == "provisional_worker_selftest"
            and receipt["proposed_state"] == "[_]", "receipt support drifted")
    require(receipt["accepted"] is receipt["release_grade"] is False
            and receipt["master_accepted"] is False, "receipt claims acceptance")
    require(receipt["recipe"] == {**spec, "observed_exit": 0},
            "receipt recipe drifted")
    require(receipt["dependency"] == decision["dependency"],
            "dependency ledgers disagree")
    require(receipt["known_failures"] == decision["known_failures"],
            "failure ledgers disagree")
    require(set(receipt["changed_paths"]) == CHANGED_PATHS,
            "receipt changed-path ledger drifted")
    require(receipt["decision_sha256"] == digest(HERE / "release-decision.json"),
            "receipt decision hash drifted")
    require(receipt["release_spec_sha256"] == digest(HERE / "release-spec.json"),
            "receipt spec hash drifted")
    require(receipt["checker_sha256"] == digest(HERE / "check_release.py"),
            "receipt checker hash drifted")
    require(receipt["public_projection_sha256"] == digest(HERE / "release-validation.md"),
            "receipt projection hash drifted")
    require(receipt["canonical_target"]["elaborated_expression_sha256"]
            == EXPRESSION_SHA256 and receipt["canonical_target"]
            ["registry_denominator_sha256"] == DENOMINATOR_SHA256,
            "receipt canonical target drifted")
    require(receipt["canonical_obligation_ids"] == ALL_OBLIGATIONS,
            "receipt obligation list drifted")
    require(receipt["result"]["verdict"] == "blocked"
            and receipt["result"]["audit_complete"] is False
            and receipt["result"]["theorem_complete"] is False,
            "receipt result is not the negative verdict")
    require(receipt["result"]["accepted_receipt_ids"] == []
            and receipt["result"]["accepted_closed_obligation_ids"] == [],
            "receipt result accepts evidence")
    require(receipt["result"]["remaining_root_cut_set"] == OPEN_ROOT_CUT,
            "receipt root cut drifted")
    for name, expected in receipt["inputs"].items():
        require(digest(ROOT / name) == expected, f"receipt input drifted: {name}")

    require(MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable")
    require(git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
            "mathlib revision drifted")
    require(git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
            "mathlib tree drifted")
    require(git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == "",
            "pinned mathlib worktree is dirty")
    replay_output, outputs = current_kernel_replay()
    current = receipt["current_kernel_replay"]
    require(current["stdout_sha256"] == hashlib.sha256(replay_output.encode()).hexdigest(),
            "current replay output hash drifted")
    require(current["stdout_bytes"] == len(replay_output.encode()),
            "current replay byte count drifted")
    require(current["axiom_report_count"] == 8
            and current["observed_axioms"] == EXPECTED_AXIOMS,
            "current replay axiom ledger drifted")
    require(set(current["module_stdout_sha256"]) == set(outputs),
            "current replay module ledger drifted")
    for name, output in outputs.items():
        require(current["module_stdout_sha256"][name]
                == hashlib.sha256(output.encode()).hexdigest(),
                f"current replay module output drifted: {name}")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        require(prohibited.search(source_without_comments_and_strings(
            (HERE / name).read_text(encoding="utf-8"))) is None,
            f"prohibited Lean mechanism in {name}")
    proof_source = source_without_comments_and_strings((HERE / "Proof.lean").read_text())
    require(not re.search(r"^theorem\s+(?:Target|CouplingPackage)\b", proof_source, re.MULTILINE),
            "proof source silently added a root declaration")

    require(set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }, "worker packet schema drifted")
    require(packet["item_id"] == ITEM and packet["state"] == "[_]"
            and packet["base_revision"] == BASE_REVISION, "worker packet identity drifted")
    require(set(packet["changed_paths"]) == CHANGED_PATHS,
            "worker changed-path ledger drifted")
    require(packet["known_failures"] == decision["known_failures"],
            "worker/decision failure ledger differs")
    require(packet["output_summary"] == SUMMARY_LINES,
            "worker output summary drifted")

    actual_changes = {
        line[3:] for line in git(
            "status", "--porcelain=v1", "--untracked-files=all", "--",
            f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
        ).splitlines() if line
    }
    require(actual_changes == CHANGED_PATHS, "actual scoped changes differ from handoff")
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        require(data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data,
                f"text hygiene failed: {relative}")
        require(all(not line.endswith((b" ", b"\t")) for line in data.splitlines()),
                f"trailing whitespace: {relative}")
    for relative in (
        f"Stage1_Instances/{THEOREM}/release-decision.json",
        f"Stage1_Instances/{THEOREM}/release-receipt.json",
        f"Stage1_Instances/{THEOREM}/release-validation.md",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        require("/home/" not in text and ".cron/" not in text,
                f"private absolute path leaked: {relative}")
        require("theorem_complete=true" not in text,
                f"completion claim leaked: {relative}")

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
