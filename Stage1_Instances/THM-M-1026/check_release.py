#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1026-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1026"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1026-RELEASE"
THEOREM = "THM-M-1026"
BASE_REVISION = "bb2a1ec294938a22b88699da0d30ced721d8ee7b"
BASE_TREE = "d8d58ab94c83274db18efd3af989171acb898759"
VALIDATION_BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
VALIDATION_RECEIPT_SHA256 = (
    "d4eccd827ace2b4b5beef68b6c64697f4da02e0b500de317440750bffc70c569"
)
EXPRESSION_SHA256 = "e39476697d12d054b84ab39c07251418d449ba5ea094c2bb37df9850c7caff93"
DENOMINATOR_SHA256 = "e74cb65a6278468b7696e4ce10a93ccbe318c57ff57bf51b541680529880f3b2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
ALL_OBLIGATIONS = [
    "M1026-ROOT",
    "M1026-S-DEFINITIONS",
    "M1026-S-BOUNDARIES",
    "M1026-S-FOUNDATION",
    "M1026-N-WEAK-CHARFUN",
    "M1026-B-NECESSITY",
    "M1026-C-BLOCK-DECOMPOSITION",
    "M1026-L-LIMIT-COMPARISON",
    "M1026-T-NECESSITY",
    "M1026-B-CONVERSE",
    "M1026-C-STABLE-WITNESS",
    "M1026-L-CONSTANT-WEAK-LIMIT",
    "M1026-T-CONVERSE",
    "M1026-T-BRANCH-MERGE",
    "M1026-X-CHARFUN-PROVENANCE",
    "M1026-X-SOURCE",
]
EXPECTED_DECLARATIONS = {
    "Stage1Instances.THM_M_1026.ObligationTree.root_of_directions",
    "Stage1Instances.THM_M_1026.Proof.stable_normalizers",
    "Stage1Instances.THM_M_1026.Proof.weaklyConverges_of_eventually_eq",
    "Stage1Instances.THM_M_1026.Proof.converseTerminal",
    "Stage1Instances.THM_M_1026.Validation.independentlyReconstructedStableNormalizers",
    "Stage1Instances.THM_M_1026.Validation.independentlyReconstructedWeakLimit",
    "Stage1Instances.THM_M_1026.Validation.independentlyReconstructedConverse",
    "Stage1Instances.THM_M_1026.Validation.independentlyReconstructedConditionalRoot",
}
EXPECTED_INPUTS = {
    "README.md": "1ed87da6db5453c8a1521b151063ab525684f4ee727ab4639c4951df1c57c944",
    "intake.json": "cd9bbb711c138dbd588b7477b6b78bdd7ab844fac849f474355e8790caee616a",
    "task-dag.json": "85ca9fc57a7bf1addbcf852bc72e4cb7f4348401481451530ddd373a033e697b",
    "Statement.lean": "f70d267d426daf28a4fbf912fa4215c5f27095a347fe714d83a4cd31eb605e8b",
    "statement.json": "7501509afc67633c57b3eb26c937efa4f885d092d1f4c7df63a54dec1b4f7157",
    "source-statement-crosswalk.md": "5b907273e87ef09171d336294d5e70a492a95879ac62053482ed2c757ad46d34",
    "anchor-audit.json": "c410a4e19149d6919ea6ef539c52585c26dfc3d5cc825d712f35fc57d36d42b8",
    "obligation-registry.json": "35ab2cdaf9fe3175eef9871a78cee8f7c27d98f94087c80a868e132d9c83f415",
    "typed-graphs.json": "f5cf4765e0825cb911fcb46f449ee0abd1264881c058ba9815567cadf82667d6",
    "ObligationTree.lean": "3429c56a3a6acaae51ca5858970e5337acbe5e312a32c4fe4cb42a4ea4bd19ed",
    "Proof.lean": "fb6670299962b85b1fd46f56b2511c8e872ff906bee9e032eb707bde0fbd2830",
    "proof-phase.json": "3c2681c2fb8c75159dfc303ec27a6713fa5df01a8a06376b004306eab1c6f72b",
    "proof-blocker.json": "dfbcbe46ca62d94eed5ff584cefda474f38a2467344d59d8243fed0230e1d1c8",
    "proof-receipt.json": "23a90245dc4abf2385ff612746bfc58ae3fce18a34aa9f47f2862efec28a04db",
    "Validation.lean": "e731491f6697d5d1946afa3ffe92c9f98e21a4e95317152eefed8a40c6e81830",
    "validation-spec.json": "08b55b57e7fb2511c18399db3bf90cb482cb8da345f523175cf51e8d97dfbb8e",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-phase.md": "8a7f393d11783392e44b29ec579fb1e7f4da9e2d1dd00493070755e6e374cdb2",
    "check_validation.py": "40257fc82481f68b4cc673acf617d10f7799c577d960d4c3c8a3c947af5ff5f9",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "53c09b6b05a2caa909ee27a0d9aace9846e73c702e2182fe8ebfd6b2f6e35728",
    "Docs/Stage1_Blueprint_rev-5.6.md": "bde68f38bfb3597acfe7213927c77b4e75a6b2975f3e54e8c5f52ee5787e0438",
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
    timeout: int = 900,
) -> str:
    try:
        completed = subprocess.run(
            argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as error:
        fail(f"command timed out: {argv!r}\n{error.stdout or ''}")
    require(
        completed.returncode == 0,
        f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}",
    )
    return completed.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).strip()


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
    require(depth == 0, "unterminated Lean block comment")
    return "".join(output)


def axiom_reports(output: str) -> dict[str, list[str]]:
    matches = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL)
    return {
        name: [part.strip() for part in raw.split(",") if part.strip()]
        for name, raw in matches
    }


def current_kernel_replay() -> tuple[str, dict[str, str]]:
    """Replay only the existing converse and conditional declarations."""

    bwrap = shutil.which("bwrap")
    require(bwrap is not None, "bubblewrap is unavailable")
    fixed_env = os.environ.copy()
    fixed_env.update({
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "PYTHONOPTIMIZE": "0",
    })
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env).strip())
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env,
    ).strip()
    version = run([str(lean), "--version"], env=fixed_env, timeout=60)
    require("4.29.0" in version and "98dc76e3" in version, "unexpected Lean version")

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m1026-release-") as tmp_name:
        tmp = Path(tmp_name).resolve()
        (tmp / "home").mkdir()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base = [
            bwrap,
            "--ro-bind", "/", "/",
            "--bind", str(tmp), str(tmp),
            "--dev", "/dev",
            "--proc", "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--clearenv",
            "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1",
            "--chdir", str(tmp),
        ]
        outputs["Statement.lean"] = run(base + [
            "--setenv", "LEAN_PATH", lean_path,
            str(lean), "--trust=0", "-t0", "-o", "Statement.olean", "Statement.lean",
        ], env=fixed_env)
        module_path = f"{tmp}:{lean_path}"
        outputs["ObligationTree.lean"] = run(base + [
            "--setenv", "LEAN_PATH", module_path,
            str(lean), "--trust=0", "-t0", "-o", "ObligationTree.olean", "ObligationTree.lean",
        ], env=fixed_env)
        outputs["Proof.lean"] = run(base + [
            "--setenv", "LEAN_PATH", module_path,
            str(lean), "--trust=0", "-t0", "Proof.lean",
        ], env=fixed_env)
        outputs["Validation.lean"] = run(base + [
            "--setenv", "LEAN_PATH", module_path,
            str(lean), "--trust=0", "-t0", "Validation.lean",
        ], env=fixed_env)

    reports: dict[str, list[str]] = {}
    for output in outputs.values():
        reports.update(axiom_reports(output))
    require(set(reports) == EXPECTED_DECLARATIONS, "release declaration coverage drifted")
    require(all(value == EXPECTED_AXIOMS for value in reports.values()),
            "partial proof axiom profile drifted")
    combined = "".join(outputs.values())
    require("error:" not in combined and "sorryAx" not in combined,
            "Lean replay observed an error or placeholder axiom")
    return combined, outputs


def main() -> None:
    require(not sys.flags.optimize, "optimized Python disables fail-closed assertions")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    intake = load(HERE / "intake.json")
    task_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_phase = load(HERE / "proof-phase.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    require(git("rev-parse", "HEAD") == BASE_REVISION, "base revision drifted")
    require(git("rev-parse", "HEAD^{tree}") == BASE_TREE, "base tree drifted")
    require(
        run(["git", "merge-base", "--is-ancestor", VALIDATION_BASE_REVISION, BASE_REVISION]) == "",
        "validation base is not an ancestor of the release base",
    )
    for name, expected in EXPECTED_INPUTS.items():
        require(digest(HERE / name) == expected, f"reconciled input drifted: {name}")
    require(decision["reconciled_inputs"] == EXPECTED_INPUTS, "decision input map drifted")
    for name, expected in AUTHORITY_INPUTS.items():
        require(digest(ROOT / name) == expected, f"authority input drifted: {name}")
    require(decision["authority_inputs"] == AUTHORITY_INPUTS, "decision authority map drifted")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    require(target["execution_rank"] == 502, "execution rank drifted")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "uniform L0 baseline drifted")
    require(target["lifecycle_mode"] == "planned", "target lifecycle drifted")
    require(target["legacy_artifacts_accepted"] is False, "legacy evidence became accepted")
    require(target["theorem_complete"] is False, "manifest claims theorem completion")

    items = {row["id"]: row for row in execution["items"]}
    require(items[ITEM] == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 502,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1026-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }, "release execution item drifted")
    require(items["S56-M-1026-VALIDATION"]["state"] == "[_]",
            "validation dependency is no longer worker-provisional")

    require(intake["lifecycle_mode"] == "planned", "intake lifecycle drifted")
    require(intake["audit_complete"] is intake["theorem_complete"] is False,
            "intake claims a terminal decision")
    require(task_dag["theorem_id"] == THEOREM, "local task DAG identity drifted")
    require(not any(row["state"] == "accepted" for row in task_dag["tasks"]),
            "local task DAG has accepted state")
    formal = statement["canonical_formal_target"]
    require(formal["elaborated_expression_sha256"] == EXPRESSION_SHA256,
            "canonical expression drifted")
    require(statement["statement_elaborated"] is True, "statement lost elaboration")
    require(statement["theorem_proved"] is statement["theorem_complete"] is False,
            "statement claims proof completion")
    require(anchor["theorem_proved"] is anchor["theorem_complete"] is False,
            "anchor audit claims proof completion")

    require(registry["denominator_sha256"] == DENOMINATOR_SHA256,
            "registry denominator drifted")
    require([row["obligation_id"] for row in registry["obligations"]] == ALL_OBLIGATIONS,
            "obligation inventory drifted")
    require(graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256,
            "graph/registry denominator mismatch")
    require({row["obligation_id"] for row in graphs["nodes"]} == set(ALL_OBLIGATIONS),
            "typed graph obligation universe drifted")
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1026-ROOT")
    require((root_node["human_debt"], root_node["machine_debt"], root_node["readability_debt"])
            == ("H2", "M3", "R4"), "typed graph root vector drifted")
    boundary = graphs["closure_boundary"]
    require(boundary["root_closed"] is boundary["theorem_complete"] is False,
            "typed graph claims root or theorem closure")
    require(boundary["remaining_root_cut_set"] == [
        "M1026-T-NECESSITY", "M1026-T-CONVERSE",
    ], "typed graph root cut drifted")

    require(proof_phase["remaining_root_cut_set"] == ["M1026-T-NECESSITY"],
            "proof phase root cut drifted")
    require(proof_phase["root_closed"] is proof_phase["theorem_complete"] is False,
            "proof phase claims completion")
    require(proof["support_state"] == "provisional_worker_selftest",
            "proof support boundary drifted")
    require(proof["accepted"] is False and proof["root_closed"] is False,
            "proof receipt claims accepted root closure")
    require(proof["result"]["theorem_complete"] is False,
            "proof receipt claims theorem completion")
    require(proof["remaining_root_cut_set"] == ["M1026-T-NECESSITY"],
            "proof root cut drifted")
    require(blocker["first_failed_gate"] == "M1026-C-BLOCK-DECOMPOSITION",
            "proof blocker drifted")
    require(blocker["root_closed"] is blocker["theorem_complete"] is False,
            "proof blocker claims completion")

    require(digest(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256,
            "validation receipt bytes drifted")
    require(validation["base_revision"] == VALIDATION_BASE_REVISION,
            "validation receipt base drifted")
    require(validation["support_state"] == "provisional_worker_selftest",
            "validation support boundary drifted")
    require(validation["accepted"] is False and validation["release_grade"] is False,
            "validation became accepted or release grade")
    require(validation["result"]["root_kernel_closed"] is False,
            "validation claims root closure")
    require(validation["result"]["audit_complete"] is False
            and validation["result"]["theorem_complete"] is False,
            "validation claims terminal completion")
    require(validation["first_failed_theorem_gate"] ==
            "proof.root_kernel_closure.M1026-T-NECESSITY",
            "validation theorem boundary drifted")

    require(decision["schema_version"] == "stage1-release-decision/1.0",
            "release decision schema drifted")
    require(decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM,
            "release decision identity drifted")
    require(decision["intent"] == "release" and decision["verdict"] == "blocked",
            "release intent or verdict drifted")
    require(decision["release_grade"] is decision["release_accepted"] is False,
            "release decision claims release grade")
    require(decision["base_revision"] == BASE_REVISION
            and decision["base_tree"] == BASE_TREE, "decision base drifted")
    require(decision["lifecycle_before"] == decision["lifecycle_after"] == "planned",
            "blocked release advanced lifecycle")
    require(decision["accepted_receipt_ids"] == [], "worker accepted a receipt")
    require(decision["root_vector"]["before"] ==
            decision["root_vector"]["after"] == {"H": "H2", "M": "M3", "R": "R4"},
            "release changed the authoritative root vector")
    require(decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }, "terminal decisions do not fail closed")
    require(decision["first_failed_gate"]["gate_id"] ==
            "S56-10.2-DEPENDENCY-ACCEPTANCE", "first node gate drifted")
    require(decision["first_failed_theorem_gate"]["gate_id"] ==
            "proof.root_kernel_closure.M1026-T-NECESSITY",
            "first theorem gate drifted")
    require(decision["first_failed_release_gate"]["gate_id"] ==
            "S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE",
            "first assurance gate drifted")
    require(decision["first_failed_reproduction_gate"]["gate_id"] ==
            "S56-10.6-HERMETIC-COLD-BUILD", "first reproduction gate drifted")
    require(decision["authoritative_remaining_root_cut_set"] == [
        "M1026-T-NECESSITY", "M1026-T-CONVERSE",
    ], "decision authoritative root cut drifted")
    require(decision["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256,
            "decision dependency receipt hash drifted")
    require(decision["dependency"]["master_accepted"] is False,
            "decision claims dependency master acceptance")
    require(decision["dependency"]["receipt_id"] == validation["receipt_id"],
            "decision names wrong dependency receipt")
    for key in (
        "validation_dependency_master_accepted",
        "exact_root_kernel_closed",
        "accepted_foundation_profile",
        "complete_transitive_provenance_and_tcb",
        "pinpoint_h0_and_independent_source_review",
        "independent_r0_review",
        "audit_z_accepted",
        "immutable_clean_release_input",
        "hermetic_empty_cache_cold_offline_replay",
        "complete_sbom_license_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    ):
        require(decision["evidence_reconciliation"][key] is False,
                f"release silently cleared {key}")
    require(decision["evidence_reconciliation"]["predecessor_recipe_freshness"] ==
            "fail_closed_phase_bound_to_historical_head_and_worker_packet",
            "stale predecessor recipe was hidden")

    require(spec["schema_version"] == "stage1-validation-recipe/1.0",
            "release recipe schema drifted")
    require(spec["item_id"] == receipt["item_id"] == ITEM,
            "release recipe/receipt item drifted")
    require(spec["theorem_id"] == receipt["theorem_id"] == THEOREM,
            "release recipe/receipt theorem drifted")
    require(spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
    ], "release argv drifted")
    require(spec["cwd"] == "." and spec["network_policy"] == "denied",
            "release recipe policy drifted")
    require(spec["timeout_seconds"] == 900 and spec["expected_exit"] == 0,
            "release recipe resource contract drifted")
    require(spec["covered_obligation_ids"] == ALL_OBLIGATIONS,
            "release recipe does not cover the frozen inventory")
    require(set(spec["covered_declarations"]) == EXPECTED_DECLARATIONS,
            "release declaration inventory drifted")

    require(receipt["schema_version"] == "stage1-node-receipt/1.0",
            "release receipt schema drifted")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE,
            "release receipt base drifted")
    require(receipt["support_state"] == "provisional_worker_selftest",
            "release receipt support drifted")
    require(receipt["accepted"] is False and receipt["release_grade"] is False,
            "release receipt claims acceptance")
    require(receipt["master_accepted"] is False, "worker claims master acceptance")
    require(receipt["decision_id"] == decision["decision_id"], "receipt names wrong decision")
    require(receipt["decision_sha256"] == digest(HERE / "release-decision.json"),
            "release decision hash drifted")
    require(receipt["release_spec_sha256"] == digest(HERE / "release-spec.json"),
            "release spec hash drifted")
    require(receipt["checker_sha256"] == digest(HERE / "check_release.py"),
            "release checker hash drifted")
    require(receipt["public_projection_sha256"] == digest(HERE / "release-validation.md"),
            "release projection hash drifted")
    require(receipt["dependency"] == decision["dependency"], "dependency ledgers disagree")
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations", "scope_boundary",
    ):
        require(receipt["recipe"][key] == spec[key], f"receipt/spec mismatch: {key}")
    require(receipt["known_failures"] == decision["known_failures"],
            "failure ledgers disagree")
    require(set(receipt["changed_paths"]) == CHANGED_PATHS,
            "release receipt changed paths drifted")
    require(receipt["result"]["verdict"] == "blocked", "receipt verdict drifted")
    require(receipt["result"]["audit_complete"] is False
            and receipt["result"]["theorem_complete"] is False,
            "receipt claims terminal completion")

    expected_recorded_argv = [
        ["python3", "Docs/tools/check_stage1_standard.py"],
        ["python3", "scripts/stage1_target.py", "check"],
        ["python3", "scripts/stage1_target.py", "show", THEOREM],
        ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_statement.py"],
        ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
        ["bash", f"Stage1_Instances/{THEOREM}/check_proof.sh"],
        ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"],
        ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"],
        ["python3", "-m", "json.tool", f"Stage1_Instances/{THEOREM}/release-spec.json"],
        ["python3", "-m", "json.tool", f"Stage1_Instances/{THEOREM}/release-decision.json"],
        ["python3", "-m", "json.tool", f"Stage1_Instances/{THEOREM}/release-receipt.json"],
        ["python3", "-m", "json.tool", ".stage1-worker-selftest.json"],
        ["python3", "-m", "py_compile", f"Stage1_Instances/{THEOREM}/check_release.py"],
        ["git", "diff", "--check", "--", f"Stage1_Instances/{THEOREM}",
         ".stage1-worker-selftest.json"],
    ]
    recorded_commands = receipt["commands_and_results"]
    require([row["argv"] for row in recorded_commands] == expected_recorded_argv,
            "receipt command argv ledger drifted")
    require([row["exit_code"] for row in recorded_commands] ==
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            "receipt command exit-code ledger drifted")
    require(recorded_commands[6]["classification"] == "expected_freshness_failure",
            "predecessor freshness failure classification drifted")

    require(packet["item_id"] == ITEM and packet["state"] == "[_]",
            "worker packet identity/state drifted")
    require(packet["base_revision"] == BASE_REVISION, "worker packet base drifted")
    require(set(packet["changed_paths"]) == CHANGED_PATHS,
            "worker packet changed paths drifted")
    require(packet["known_failures"] == decision["known_failures"],
            "worker packet failure ledger drifted")
    require(packet["commands"] == [
        "python3 Docs/tools/check_stage1_standard.py",
        "python3 scripts/stage1_target.py check",
        "python3 scripts/stage1_target.py show THM-M-1026",
        "python3 -B Stage1_Instances/THM-M-1026/check_statement.py",
        "python3 -B Stage1_Instances/THM-M-1026/check_obligation_tree.py",
        "bash Stage1_Instances/THM-M-1026/check_proof.sh",
        "python3 -I -B Stage1_Instances/THM-M-1026/check_validation.py",
        "python3 -B Stage1_Instances/THM-M-1026/check_release.py",
        "python3 -m json.tool Stage1_Instances/THM-M-1026/release-spec.json",
        "python3 -m json.tool Stage1_Instances/THM-M-1026/release-decision.json",
        "python3 -m json.tool Stage1_Instances/THM-M-1026/release-receipt.json",
        "python3 -m json.tool .stage1-worker-selftest.json",
        "PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1026-release-pycache python3 -m py_compile Stage1_Instances/THM-M-1026/check_release.py",
        "git diff --check -- Stage1_Instances/THM-M-1026 .stage1-worker-selftest.json",
    ], "worker packet command ledger drifted")
    for fragment in (
        "verdict blocked", "planned", "H2/M3/R4", "accepted receipts are empty",
        "M1026-T-NECESSITY remains open", "audit_complete=false", "theorem_complete=false",
    ):
        require(fragment in packet["output_summary"],
                f"worker output summary omits {fragment!r}")
    actual_changes = {
        line[3:] for line in git(
            "status", "--porcelain=v1", "--untracked-files=all", "--",
            f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
        ).splitlines() if line
    }
    require(actual_changes == CHANGED_PATHS,
            f"actual scoped changes differ from handoff: {sorted(actual_changes)}")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        require(prohibited.search(source) is None, f"prohibited Lean construct in {name}")
    proof_source = code_without_comments((HERE / "Proof.lean").read_text(encoding="utf-8"))
    validation_source = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    require("necessity half" in (HERE / "Proof.lean").read_text(encoding="utf-8"),
            "proof source no longer discloses open necessity")
    require("theorem converseTerminal" in proof_source, "converse body is missing")
    require("(necessity :" in validation_source, "conditional validation premise is hidden")
    require("import Proof" not in validation_source,
            "differential validation unexpectedly imports Proof")

    require(MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable")
    require(git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
            "mathlib revision drifted")
    require(git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
            "mathlib tree drifted")
    require(git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE,
            "mathlib remote drifted")
    require(git("status", "--porcelain=v1", cwd=MATHLIB) == "",
            "mathlib worktree is dirty before replay")
    lean_path = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake_path = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lake"
    require(receipt["environment"]["lean_executable_sha256"] == digest(lean_path),
            "Lean executable digest drifted")
    require(receipt["environment"]["lake_executable_sha256"] == digest(lake_path),
            "Lake executable digest drifted")
    bwrap_path = shutil.which("bwrap")
    require(bwrap_path is not None, "bubblewrap is unavailable")
    require(receipt["environment"]["bubblewrap_executable_sha256"] ==
            digest(Path(bwrap_path)), "bubblewrap executable digest drifted")
    require(receipt["environment"]["python"] ==
            f"CPython {platform.python_version()}", "Python version drifted")
    require(receipt["environment"]["python_executable_sha256"] ==
            digest(Path(sys.executable)), "Python executable digest drifted")
    git_path = shutil.which("git")
    require(git_path is not None, "git is unavailable")
    require(receipt["environment"]["git"] == run([git_path, "--version"]).strip(),
            "git version drifted")
    require(receipt["environment"]["git_executable_sha256"] == digest(Path(git_path)),
            "git executable digest drifted")
    replay_output, outputs = current_kernel_replay()
    require(git("status", "--porcelain=v1", cwd=MATHLIB) == "",
            "mathlib worktree changed during replay")
    replay_hash = hashlib.sha256(replay_output.encode("utf-8")).hexdigest()
    replay_bytes = len(replay_output.encode("utf-8"))
    if receipt["current_kernel_replay"]["stdout_sha256"] != replay_hash:
        print(json.dumps({
            "stdout_sha256": replay_hash,
            "stdout_bytes": replay_bytes,
            "module_stdout_sha256": {
                name: hashlib.sha256(output.encode("utf-8")).hexdigest()
                for name, output in outputs.items()
            },
            "module_stdout_bytes": {
                name: len(output.encode("utf-8")) for name, output in outputs.items()
            },
        }, sort_keys=True))
        fail("current replay output hash drifted")
    require(receipt["current_kernel_replay"]["stdout_bytes"] == replay_bytes,
            "current replay byte count drifted")
    require(receipt["current_kernel_replay"]["axiom_report_count"] == 8,
            "receipt axiom report count drifted")
    require(set(receipt["current_kernel_replay"]["module_stdout_sha256"]) == set(outputs),
            "receipt module output inventory drifted")
    for name, output in outputs.items():
        require(receipt["current_kernel_replay"]["module_stdout_sha256"][name] ==
                hashlib.sha256(output.encode("utf-8")).hexdigest(),
                f"receipt module output hash drifted: {name}")
        require(receipt["current_kernel_replay"]["module_stdout_bytes"][name] ==
                len(output.encode("utf-8")), f"receipt module byte count drifted: {name}")

    public = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H2, M3, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "release_grade=false", "accepts no receipt", "M1026-T-NECESSITY",
    ):
        require(fragment in public, f"release projection omits {fragment!r}")
    require("/home/" not in public and ".cron/" not in public,
            "public release projection exposes a private worker path")
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        require(data.endswith(b"\n"), f"missing final newline: {relative}")
        require(b"\r" not in data and b"\x00" not in data,
                f"invalid byte in {relative}")
        require(all(not line.endswith((b" ", b"\t")) for line in data.splitlines()),
                f"trailing whitespace in {relative}")

    require(receipt["environment"]["platform"] ==
            f"{platform.system()} {platform.machine()}", "receipt platform drifted")
    print("PASS release inputs: target, DAG, predecessor receipts, registry, graphs, and hashes agree")
    print("PASS current partial Lean replay: eight trust-zero reports; necessity stays an explicit premise")
    print("PASS fail-closed state: lifecycle planned; root H2/M3/R4; accepted receipts 0")
    print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted")
    print("BLOCKED proof.root_kernel_closure.M1026-T-NECESSITY")
    print("BLOCKED release trust, cold/offline, independent-verifier, and bundle gates")
    print("verdict=blocked audit_complete=false theorem_complete=false")


if __name__ == "__main__":
    main()
