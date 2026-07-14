#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1029-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1029"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1029-RELEASE"
THEOREM = "THM-M-1029"
BASE_REVISION = "17ab2f2e1cfc0f8fe952eef85bcb0c0163f3ac97"
BASE_TREE = "2562e0eb38e93c12bd3f592a28fdc040278351f3"
VALIDATION_BASE_REVISION = "2d334dfd1443fdb9dbdf08b9d53d6c67399ec7af"
VALIDATION_RECEIPT_SHA256 = (
    "a3a0eedf2fb9d4209a6089de6eaf99225885c0e99b9aeaa84b15f6640de9e86d"
)
EXPRESSION_SHA256 = "f3e443377f8cac2eba62a6ebcf6f05ce5bd453f3075d9de573641856e21331b2"
DENOMINATOR_SHA256 = "f5ba78d2ff64231db87b356cdf2827f4d9173387c0a387c3acfbddad19cf0fb4"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
ALL_OBLIGATIONS = [
    "M1029-ROOT",
    "M1029-S-DEFINITIONS",
    "M1029-S-BOUNDARY",
    "M1029-S-FOUNDATION",
    "M1029-N-QUADRATIC-VARIATION",
    "M1029-C-EXPONENTIAL",
    "M1029-L-EXPONENTIAL-MARTINGALE",
    "M1029-L-CONDITIONAL-CHARACTERISTIC",
    "M1029-L-GAUSSIAN-LAW",
    "M1029-L-INDEPENDENCE",
    "M1029-T-INCREMENTS",
    "M1029-T-ASSEMBLE",
    "M1029-X-SOURCE",
    "M1029-X-PROVENANCE",
]
EXPECTED_PROOF_DECLARATIONS = {
    "Stage1Instances.THM_M_1029.Proof.bracketCompensated_deterministicTime_eq",
    "Stage1Instances.THM_M_1029.Proof.deterministicTimeProcess_continuousPaths",
    "Stage1Instances.THM_M_1029.Proof.deterministicTimeProcess_monotonePaths",
    "Stage1Instances.THM_M_1029.Proof.deterministicTimeProcess_startsAtZero",
    "Stage1Instances.THM_M_1029.Proof.bracketCompensated_martingale_of_quadratic",
    "Stage1Instances.THM_M_1029.Proof.quadraticCompensated_stronglyAdapted",
    "Stage1Instances.THM_M_1029.Proof.square_stronglyAdapted",
    "Stage1Instances.THM_M_1029.Proof.deterministicTime_stronglyAdapted_of_martingales",
    "Stage1Instances.THM_M_1029.Proof.quadratic_coordinate_integrable",
    "Stage1Instances.THM_M_1029.Proof.coordinate_memLp_two",
    "Stage1Instances.THM_M_1029.Proof.increment_memLp_two",
    "Stage1Instances.THM_M_1029.Proof.increment_square_integrable",
    "Stage1Instances.THM_M_1029.Proof.increment_condExp_eq_zero",
    "Stage1Instances.THM_M_1029.Proof.increment_condExp_sq",
    "Stage1Instances.THM_M_1029.Proof.integral_process_eq_zero",
    "Stage1Instances.THM_M_1029.Proof.integral_process_sq_eq_time",
    "Stage1Instances.THM_M_1029.Proof.variance_process_eq_time",
    "Stage1Instances.THM_M_1029.Proof.zeroElapsedIncrement",
    "Stage1Instances.THM_M_1029.Proof.hasLaw_gaussianReal_of_charFun",
    "Stage1Instances.THM_M_1029.Proof.hasLaw_gaussianReal_zero",
    "Stage1Instances.THM_M_1029.Proof.incrementLawPackage_of_components",
    "Stage1Instances.THM_M_1029.Proof.incrementLawPackage_of_strict",
    "Stage1Instances.THM_M_1029.Proof.root_of_assumedIncrementComponents",
}
EXPECTED_INPUTS = {
    "README.md": "cee1e0ed8e2f8d3a3f5c6e6ed45ba18ec60112009c7ffbc9bc5aedb037fbb05c",
    "instance.json": "39593519d1198e5d47a017d44bed1f1fd86da2174cb131a64a99bdec7d05c691",
    "task-dag.json": "93526986ec3962d8aec295bfa382b54955e09b21d78cb48543adbfcc3b50ed61",
    "Statement.lean": "ae6a30cd8ba78423f8d4577bb1c6e9e047cc7c8f10e5a2ba8b6d500337f06782",
    "statement.json": "32d7ae2323df43130a91e511a65b2d31cb5aed42518bdcc8deea12dd8c5d7400",
    "source-statement-crosswalk.md": "a80cffb80a92717b2f4122562651b389ed8dcd664561e4ef190a6b4775a53227",
    "anchor-audit.json": "0d281883b5c2d62c07d485fd5e9c606ccff04d233d97293dcedd04c1c956573b",
    "obligation-registry.json": "22a9b3af299a84aecefdc49c60ca96a261a8c37157e6d1f15ae0cddcba577053",
    "typed-graphs.json": "96fe778b583d0c3d5e4e4b8936428b2a0f928736aa0c4032722e199b9e22e774",
    "ObligationTree.lean": "9298952a961d60af29ff4fe28ce1600174837a08e1addbfd51f06da678678453",
    "Proof.lean": "d1b7395e0a5206f4c655e1c9b226036d786eb24d7c09b5f43340cf3c17bdebc6",
    "proof-blocker-2026-07-14.json": "97e42234b676ad3f729f22a9fb7fddf3d8b7d8deb28bd943bd3ab12ccb4051a8",
    "proof-receipt.json": "c6de98f9443838002fbd4606561cd67dff76d6fe16ab3b473dc2a185e8574aed",
    "Validation.lean": "1abd510ed8795c6b21615830f0a6183860d1cda083a287c5fa245ac67643427e",
    "validation-spec.json": "83cd80185e2969756875ce31e1d843e509f80d5aea4fb3b0608f729f34c72812",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-phase.md": "e18abd86858d0db96008cf3b12348c5e7a111c6257c53343dbf996e4c6ed3333",
    "check_validation.py": "34ecbc06f1f6f225fa4f341f0fa00232759e9be4fbbd493781f247fbb528388b",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "53b2ab23cb33a8866e0eb67263e1ac70a188f81550342fd4c1f53bc6511723ea",
    "Docs/Stage1_Blueprint_rev-5.6.md": "500db6985d8f1e2b39f57564a02f3b571ffe068222077e1d42e5218d0bfc3ac0",
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
    """Replay only the existing partial declarations in a fresh network-isolated target dir."""

    bwrap = shutil.which("bwrap")
    require(bwrap is not None, "bubblewrap is unavailable")
    fixed_env = os.environ.copy()
    fixed_env.update({
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC",
        "LEAN_NUM_THREADS": "1", "PYTHONOPTIMIZE": "0",
    })
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env).strip())
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env,
    ).strip()
    version = run([str(lean), "--version"], env=fixed_env, timeout=60)
    require("4.29.0" in version, "unexpected Lean version")

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m1029-release-") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base = [
            bwrap, "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--setenv", "HOME", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]
        outputs["Statement.lean"] = run(base + [
            "--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0", "-t0",
            "-o", "Statement.olean", "Statement.lean",
        ], env=fixed_env)
        module_path = f"{tmp}:{lean_path}"
        outputs["ObligationTree.lean"] = run(base + [
            "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
            "-o", "ObligationTree.olean", "ObligationTree.lean",
        ], env=fixed_env)
        outputs["Proof.lean"] = run(base + [
            "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
            "Proof.lean",
        ], env=fixed_env)
        outputs["Validation.lean"] = run(base + [
            "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
            "Validation.lean",
        ], env=fixed_env)

    tree_reports = axiom_reports(outputs["ObligationTree.lean"])
    require(tree_reports == {
        "Stage1Instances.THM_M_1029.root_of_incrementLawPackage": EXPECTED_AXIOMS,
    }, "conditional composition axiom report drifted")
    proof_reports = axiom_reports(outputs["Proof.lean"])
    require(set(proof_reports) == EXPECTED_PROOF_DECLARATIONS,
            "partial proof declaration coverage drifted")
    require(all(value == EXPECTED_AXIOMS for value in proof_reports.values()),
            "partial proof axiom profile drifted")
    validation_reports = axiom_reports(outputs["Validation.lean"])
    require(validation_reports == {
        "Stage1Instances.THM_M_1029.Validation.exactRootOfDirectStrictIncrementLaw": EXPECTED_AXIOMS,
    }, "differential conditional adapter axiom report drifted")
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
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker-2026-07-14.json")
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
    require(target["execution_rank"] == 222, "execution rank drifted")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "uniform L0 baseline drifted")
    require(target["lifecycle_mode"] == "planned", "target lifecycle drifted")
    require(target["legacy_artifacts_accepted"] is False, "legacy evidence became accepted")
    require(target["theorem_complete"] is False, "manifest claims theorem completion")

    items = {row["id"]: row for row in execution["items"]}
    require(items[ITEM] == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 222,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1029-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }, "release execution item drifted")
    require(items["S56-M-1029-VALIDATION"]["state"] == "[_]",
            "validation dependency is no longer worker-provisional")

    require(instance["lifecycle"] == "planned", "instance lifecycle drifted")
    require(instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"},
            "instance root vector drifted")
    require(instance["audit_complete"] is instance["theorem_complete"] is False,
            "instance claims a terminal decision")
    require(instance["accepted_proof_state"] == [], "instance has accepted proof state")
    require(task_dag["accepted_states"] == [], "local task DAG has accepted states")
    require(all(row["state"] == "open" for row in task_dag["tasks"]),
            "local task DAG was silently reconciled")
    formal = statement["canonical_formal_target"]
    require(formal["elaborated_expression_sha256"] == EXPRESSION_SHA256,
            "canonical expression drifted")
    require(statement["statement_elaborated"] is True, "statement lost elaboration")
    require(statement["theorem_proved"] is statement["theorem_complete"] is False,
            "statement claims proof completion")
    require(anchor["audit_complete"] is anchor["theorem_complete"] is False,
            "anchor audit claims terminal completion")

    require(registry["denominator_sha256"] == DENOMINATOR_SHA256,
            "registry denominator drifted")
    require([row["obligation_id"] for row in registry["obligations"]] == ALL_OBLIGATIONS,
            "obligation inventory drifted")
    require(graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256,
            "graph/registry denominator mismatch")
    require({row["obligation_id"] for row in graphs["nodes"]} == set(ALL_OBLIGATIONS),
            "typed graph obligation universe drifted")
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1029-ROOT")
    require((root_node["human_debt"], root_node["machine_debt"], root_node["readability_debt"])
            == ("H2", "M3", "R4"), "typed graph root vector drifted")
    boundary = graphs["closure_boundary"]
    require(boundary["root_closed"] is False, "typed graph claims root closure")
    require(boundary["audit_complete"] is boundary["theorem_complete"] is False,
            "typed graph claims terminal completion")
    require(boundary["remaining_root_cut_set"] == ["M1029-T-INCREMENTS"],
            "typed graph root cut drifted")
    require(graphs["graphs"]["evidence"]["edges"] == [], "evidence graph is not empty")

    require(proof["support_state"] == "provisional_worker_selftest",
            "proof support boundary drifted")
    require(proof["accepted"] is False and proof["closed_obligation_ids"] == [],
            "proof receipt claims accepted closure")
    require(proof["result"]["root_closed"] is False,
            "proof receipt claims root closure")
    require(proof["result"]["theorem_complete"] is False,
            "proof receipt claims theorem completion")
    require(proof["remaining_root_cut_set"] == ["M1029-T-INCREMENTS"],
            "proof root cut drifted")
    require(blocker["closed_obligation_ids"] == [], "blocker claims a closed obligation")
    require(blocker["root_closed"] is blocker["theorem_complete"] is False,
            "blocker claims completion")

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
    require(validation["result"]["root_machine_debt"] == "M3",
            "validation root debt drifted")
    require(validation["result"]["remaining_root_cut_set"] == ["M1029-T-INCREMENTS"],
            "validation root cut drifted")
    require(validation["result"]["audit_complete"] is False
            and validation["result"]["theorem_complete"] is False,
            "validation claims terminal completion")

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
    require(decision["root_vector"] == {
        "before": {"H": "H2", "M": "M3", "R": "R4"},
        "after": {"H": "H2", "M": "M3", "R": "R4"},
    }, "release changed the authoritative root vector")
    require(decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }, "terminal decisions do not fail closed")
    require(decision["first_failed_gate"]["gate_id"] ==
            "S56-10.2-DEPENDENCY-ACCEPTANCE", "first node gate drifted")
    require(decision["first_failed_theorem_gate"]["gate_id"] ==
            "proof.root_kernel_closure.M1029-T-INCREMENTS",
            "first theorem gate drifted")
    require(decision["first_failed_release_gate"]["gate_id"] ==
            "S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE",
            "first assurance gate drifted")
    require(decision["first_failed_reproduction_gate"]["gate_id"] ==
            "S56-10.6-HERMETIC-COLD-BUILD", "first reproduction gate drifted")
    require(decision["remaining_root_cut_set"] == ["M1029-T-INCREMENTS"],
            "decision mathematical root cut drifted")
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
    require(decision["evidence_reconciliation"]["current_partial_kernel_replay"] ==
            "pass_as_provisional_network_isolated_warm_cache_evidence",
            "current partial replay classification drifted")
    require(decision["evidence_reconciliation"]["predecessor_recipe_freshness"] ==
            "fail_closed_phase_bound_to_old_head_dag_state_and_worker_packet",
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
    expected_env = {
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "PYTHONOPTIMIZE": "0",
        "PATH": "explicitly_variable; must resolve python3, git, lake, and bwrap; exact invoked executable digests are recorded where material to the partial Lean replay",
    }
    require(spec["env_allowlist"] == expected_env,
            "release recipe environment contract drifted")
    require(spec["network_enforcement"].startswith("Every Lean invocation runs with --trust=0"),
            "release network-enforcement description drifted")
    require(spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy":
            "contains verdict=blocked audit_complete=false theorem_complete=false",
    }], "release expected-output contract drifted")
    require(set(spec["covered_declarations"]) == {
        "Stage1Instances.THM_M_1029.root_of_incrementLawPackage",
        *EXPECTED_PROOF_DECLARATIONS,
        "Stage1Instances.THM_M_1029.Validation.exactRootOfDirectStrictIncrementLaw",
    }, "release declaration coverage drifted")
    require(len(spec["covered_declarations"]) == 25,
            "release declaration coverage contains duplicates")
    require(spec["scope_boundary"].startswith("Reconciles the frozen 14-obligation inventory"),
            "release recipe scope boundary drifted")

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
        require(receipt["recipe"][key] == spec[key],
                f"receipt/spec recipe mismatch: {key}")
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
        ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
        ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"],
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
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            "receipt command exit-code ledger drifted")
    require(recorded_commands[4]["classification"] == "expected_freshness_failure",
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
        "python3 scripts/stage1_target.py show THM-M-1029",
        "python3 -B Stage1_Instances/THM-M-1029/check_obligation_tree.py",
        "python3 -B Stage1_Instances/THM-M-1029/check_validation.py",
        "python3 -B Stage1_Instances/THM-M-1029/check_release.py",
        "python3 -m json.tool Stage1_Instances/THM-M-1029/release-spec.json",
        "python3 -m json.tool Stage1_Instances/THM-M-1029/release-decision.json",
        "python3 -m json.tool Stage1_Instances/THM-M-1029/release-receipt.json",
        "python3 -m json.tool .stage1-worker-selftest.json",
        "PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1029-release-pycache python3 -m py_compile Stage1_Instances/THM-M-1029/check_release.py",
        "git diff --check -- Stage1_Instances/THM-M-1029 .stage1-worker-selftest.json",
    ], "worker packet command ledger drifted")
    for fragment in (
        "verdict blocked", "planned", "H2/M3/R4", "accepted receipts are empty",
        "M1029-T-INCREMENTS remains open", "audit_complete=false",
        "theorem_complete=false",
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
    for marker in (
        "def GaussianIncrementLawPackage : Prop",
        "def IncrementIndependencePackage : Prop",
        "def StrictIncrementLawPackage : Prop",
        "(gaussian : GaussianIncrementLawPackage.{u})",
        "(independent : IncrementIndependencePackage.{u})",
    ):
        require(marker in proof_source, f"conditional proof boundary drifted: {marker}")

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
    lake_path = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
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
    require(receipt["current_kernel_replay"]["stdout_sha256"] ==
            hashlib.sha256(replay_output.encode("utf-8")).hexdigest(),
            "current replay output hash drifted")
    require(receipt["current_kernel_replay"]["stdout_bytes"] ==
            len(replay_output.encode("utf-8")), "current replay byte count drifted")
    require(receipt["current_kernel_replay"]["axiom_report_count"] == 25,
            "receipt axiom report count drifted")
    require(set(receipt["current_kernel_replay"]["module_stdout_sha256"]) == set(outputs),
            "receipt module output inventory drifted")
    for name, output in outputs.items():
        require(receipt["current_kernel_replay"]["module_stdout_sha256"][name] ==
                hashlib.sha256(output.encode("utf-8")).hexdigest(),
                f"receipt module output hash drifted: {name}")

    public = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H2, M3, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "release_grade=false", "accepts no receipt", "M1029-T-INCREMENTS",
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

    require(receipt["environment"]["platform"] == f"{platform.system()} {platform.machine()}",
            "receipt platform drifted")
    print("PASS release inputs: target, DAG, archived receipts, registry, graphs, and hashes agree")
    print("PASS current partial Lean replay: 25 trust-zero reports; conditional interfaces stay premises")
    print("PASS fail-closed state: lifecycle planned; root H2/M3/R4; accepted receipts 0")
    print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted")
    print("BLOCKED proof.root_kernel_closure.M1029-T-INCREMENTS")
    print("BLOCKED release trust, cold/offline, independent-verifier, and bundle gates")
    print("verdict=blocked audit_complete=false theorem_complete=false")


if __name__ == "__main__":
    main()
