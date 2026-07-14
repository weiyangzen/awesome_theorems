#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1011-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1011"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1011-RELEASE"
THEOREM = "THM-M-1011"
BASE_REVISION = "605d8c2f2b4e46bcc0762f51a012db1ac610e1ee"
BASE_TREE = "426435f32f2e6a4594f78e816ed8790671784225"
VALIDATION_BASE_REVISION = "e6c4d56e017f77b02752e6c1325f0298dfb7f4d4"
EXPRESSION_SHA256 = "5711575e18ff4a1eecd2ce047a29817d876a6e44cb86c724b476414314f9e812"
DENOMINATOR_SHA256 = "3dd41addcf34fd9ca7d89e9d2231337be0e01df77f497acdcefff743020bdd90"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
ALL_OBLIGATIONS = [
    "M1011-ROOT", "M1011-S-DEFINITIONS", "M1011-S-DOMAIN",
    "M1011-S-BOUNDARY", "M1011-S-TRANSPORT", "M1011-S-FOUNDATION",
    "M1011-N-SEPARATION", "M1011-B-TIGHT-COMPACT",
    "M1011-B-COMPACT-TIGHT", "M1011-L-PROKHOROV",
    "M1011-L-COMPACT-TIGHT", "M1011-T-ASSEMBLE", "M1011-X-SOURCE",
    "M1011-X-PROVENANCE",
]
REQUIRED_MACHINE = ALL_OBLIGATIONS[:12]
EXPECTED_INPUTS = {
    "instance.json": "f18c2b855027894e744ad8be6d0fd3d196f03380a24644931326c6dd82dfdaa1",
    "task-dag.json": "02e641a97aefbc84bf91c654c2040adfbee84ca7bd0b7079606f64b4d6291a6e",
    "README.md": "def4e8fc02ecb9042adf3761138794ec60d04637994c25ab9cc671741109c22d",
    "source-statement-crosswalk.md": "29fa181b560e3b6abdd36017d1c5da3ac16ef1e5c16bcaa98fdb540103cf12b6",
    "Statement.lean": "6bf24878f5041dc4aa1e7365b8a0c2b5c7d8fb65fe5ee389597081a8c9511d66",
    "statement.json": "fcffa9db59e116f36201c498e7c0fb4af581c1c04b7f8f3d0fe6b4aa6616e5ab",
    "AnchorAudit.lean": "383ae02d191eef2d24e9d0b0fd3794494995ea863fff0ee73ba26e7fe88a3a95",
    "anchor-audit.json": "7d75a5b6a347a8d2f23627346953cc5747b119960b4d7d1e5b114f8b506a93a2",
    "ObligationTree.lean": "4395f2cb5f788f3fd9ae19fabfd97659d4edeef88eafb952f1a80f03d2c17c9d",
    "obligation-registry.json": "e427e1638975db782747232bd2dcd9382df41424df592d94035dec05b31aaa40",
    "typed-graphs.json": "38b9505f9643c6a2bac4fd8f65d4723d031cfb18a26d905197bfd4d833819895",
    "validation-specs.json": "ed6f75283414aeb3da94d5f68e403d40e1c4cb1b629bcdec80e0722276dec8a1",
    "Proof.lean": "f8b6582c52e409df8fbace88d59fe8300efc018f07a40bf8f10a43aad75413ed",
    "proof-receipt.json": "24edab9ea39e96f373cc9e473b80fb7d7d0ae7ad0fe2d1899585f0ad2d3ef7f7",
    "Validation.lean": "5691ce8857744903f5184b5aa3483666732c4265c7c1466a30e03c2112d0ca85",
    "validation-spec.json": "edc8d2361b70d05c97f0469f67fe3f696be9dda5c7172222b396799ee9b8e256",
    "validation-receipt.json": "7fd5963bcdba7d5aaf1b9dbcfa1114fa2949259d77d8e5890e3af1fab03db9db",
    "validation-phase.md": "f61bafc003d0f9044c2fdd963330edaa62c56ce93a5b050e72813a7b4aca2cd1",
    "check_validation.py": "b0d0b094ec3a8584afe9d19471d690179a76f0557a367d8de43043f1757b9e71",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "c9ee8ef50b7d8b62b146b33fb78bd15b586e30e3f1799468d53c859e6b1c2b96",
    "Docs/Stage1_Blueprint_rev-5.6.md": "36b29c5b7327456390b945ed1df4534e86289295cce5cf4740e84dec4b6f9478",
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
    timeout: int = 900, expected_exit: int = 0,
) -> str:
    try:
        completed = subprocess.run(
            argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as error:
        fail(f"command timed out: {argv!r}\n{error.stdout or ''}")
    require(
        completed.returncode == expected_exit,
        f"command exited {completed.returncode}, expected {expected_exit}: {argv!r}\n"
        f"{completed.stdout}",
    )
    return completed.stdout


def controlled_env() -> dict[str, str]:
    """Minimal outer recipe environment; Lean subprocesses add fixed replay variables."""

    path = os.environ.get("PATH")
    require(path is not None and path != "", "PATH is unavailable")
    return {
        "PATH": path,
        "HOME": str(Path.home()),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "PYTHONOPTIMIZE": "0",
    }


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, env=controlled_env(), timeout=60).strip()


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
    """Replay current exact roots in a fresh, network-isolated target directory."""

    fixed_env = controlled_env()
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env).strip())
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env,
    ).strip()
    require("4.29.0" in run([str(lean), "--version"], env=fixed_env, timeout=60),
            "unexpected Lean version")

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m1011-release-") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        (tmp / "home").mkdir()
        base = [str(lean), "--trust=0", "-t0", "--root", str(tmp)]
        lean_env = fixed_env.copy()
        lean_env["HOME"] = str(tmp / "home")
        outputs["Statement.lean"] = run(base + [
            "-o", "Statement.olean", "Statement.lean",
        ], cwd=tmp, env={**lean_env, "LEAN_PATH": lean_path})
        module_path = f"{tmp}:{lean_path}"
        outputs["ObligationTree.lean"] = run(base + [
            "-o", "ObligationTree.olean", "ObligationTree.lean",
        ], cwd=tmp, env={**lean_env, "LEAN_PATH": module_path})
        outputs["Proof.lean"] = run(base + [
            "Proof.lean",
        ], cwd=tmp, env={**lean_env, "LEAN_PATH": module_path})
        outputs["Validation.lean"] = run(base + [
            "Validation.lean",
        ], cwd=tmp, env={**lean_env, "LEAN_PATH": module_path})

    require(axiom_reports(outputs["Proof.lean"]) == {
        "Stage1Instances.THM_M_1011.Proof.canonical": EXPECTED_AXIOMS,
    }, "proof root axiom report drifted")
    validation_reports = axiom_reports(outputs["Validation.lean"])
    require(
        validation_reports.get(
            "Stage1Instances.THM_M_1011.Validation.independentlyReconstructedCanonical"
        ) == EXPECTED_AXIOMS,
        "differential root axiom report drifted",
    )
    forward = next(
        (value for name, value in validation_reports.items()
         if name.endswith("isCompact_closure_of_isTightMeasureSet")), None,
    )
    reverse = next(
        (value for name, value in validation_reports.items()
         if name.endswith("isTightMeasureSet_of_isCompact_closure")), None,
    )
    require(forward == EXPECTED_AXIOMS, "forward mathlib body axiom report drifted")
    require(reverse == EXPECTED_AXIOMS, "reverse mathlib body axiom report drifted")
    require(len(validation_reports) == 3, "unexpected differential axiom report count")
    combined = "".join(outputs.values())
    require("Declarations are sorry-free!" in outputs["Validation.lean"],
            "differential sorry check did not pass")
    require("declaration uses 'sorry'" not in combined and "sorryAx" not in combined
            and "error:" not in combined, "Lean replay observed a placeholder or error")
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
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    require(git("rev-parse", "HEAD") == BASE_REVISION, "base revision drifted")
    require(git("rev-parse", "HEAD^{tree}") == BASE_TREE, "base tree drifted")
    require(run(["git", "merge-base", "--is-ancestor", VALIDATION_BASE_REVISION,
                 BASE_REVISION], env=controlled_env()) == "",
            "validation base is not an ancestor")
    for name, expected in EXPECTED_INPUTS.items():
        require(digest(HERE / name) == expected, f"reconciled input drifted: {name}")
    require(decision["reconciled_inputs"] == EXPECTED_INPUTS, "decision input map drifted")
    for name, expected in AUTHORITY_INPUTS.items():
        require(digest(ROOT / name) == expected, f"authority input drifted: {name}")
    require(decision["authority_inputs"] == AUTHORITY_INPUTS, "decision authority map drifted")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    require(target["execution_rank"] == 260, "execution rank drifted")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "uniform L0 baseline drifted")
    require(target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False,
            "target authority advanced")
    require(target["legacy_artifacts_accepted"] is False, "legacy evidence became accepted")

    items = {row["id"]: row for row in execution["items"]}
    require(items[ITEM] == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 260,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1011-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }, "release execution item drifted")
    require(items["S56-M-1011-VALIDATION"]["state"] == "[_]"
            and items["S56-M-1011-VALIDATION"]["attempts"] == 1,
            "validation dependency is not worker-provisional")

    planned_vector = {"H": "H1", "M": "M5", "R": "R4"}
    require(instance["lifecycle"] == "planned" and instance["root_vector"] == planned_vector,
            "instance planned state drifted")
    require(instance["accepted_proof_state"] == [], "instance has accepted proof state")
    require(instance["audit_complete"] is instance["theorem_complete"] is False,
            "instance claims a terminal decision")
    require(task_dag["lifecycle"] == "planned" and task_dag["accepted_states"] == [],
            "local task authority advanced")
    require(all(row["state"] == "open" for row in task_dag["tasks"]),
            "local task DAG was silently reconciled")
    require(statement["canonical_formal_target"]["elaborated_expression_sha256"]
            == EXPRESSION_SHA256, "canonical expression drifted")
    require(statement["statement_elaborated"] is True
            and statement["theorem_complete"] is False, "statement boundary drifted")
    require(anchor["audit_complete"] is anchor["theorem_complete"] is False,
            "anchor audit claims terminal completion")

    require(registry["denominator_sha256"] == DENOMINATOR_SHA256,
            "registry denominator drifted")
    require(registry["frozen_denominators"]["inventory"] == ALL_OBLIGATIONS,
            "obligation inventory drifted")
    require(registry["frozen_denominators"]["required_machine"] == REQUIRED_MACHINE,
            "machine denominator drifted")
    require(graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256,
            "graph/registry denominator mismatch")
    root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1011-ROOT")
    require((root["human_debt"], root["machine_debt"], root["readability_debt"])
            == ("H1", "M5", "R4"), "typed graph root vector drifted")
    require(root["evidence_ids"] == [], "typed graph root gained accepted evidence")
    boundary = graphs["closure_boundary"]
    require(boundary["root_closed"] is False and boundary["root_machine_debt"] == "M5"
            and boundary["theorem_complete"] is False, "frozen graph claims closure")
    require(boundary["remaining_root_cut_set"] == ["M1011-N-SEPARATION"],
            "frozen machine cut drifted")

    require(proof["support_state"] == "provisional_worker_selftest"
            and proof["accepted"] is False, "proof support boundary drifted")
    require(proof["result"]["root_kernel_closed"] is True
            and proof["result"]["frozen_graph_closed"] is False,
            "proof/graph distinction drifted")
    require(proof["accepted_closed_obligation_ids"] == []
            and proof["result"]["theorem_complete"] is False,
            "proof receipt claims accepted completion")
    require(validation["support_state"] == "provisional_worker_selftest"
            and validation["accepted"] is validation["release_grade"] is False,
            "validation became accepted or release grade")
    require(validation["base_revision"] == VALIDATION_BASE_REVISION,
            "validation base identity drifted")
    require(validation["accepted_closed_obligation_ids"] == []
            and validation["result"]["accepted_root_closed"] is False,
            "validation claims accepted closure")
    require(validation["result"]["audit_complete"] is False
            and validation["result"]["theorem_complete"] is False,
            "validation claims terminal completion")

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
    require(decision["root_vector"]["authoritative_before"] == ["H1", "M5", "R4"]
            and decision["root_vector"]["authoritative_after"] == ["H1", "M5", "R4"],
            "release silently changed the vector")
    require(decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked",
    }, "terminal decisions are not fail closed")
    require(decision["first_failed_gate"]["gate_id"]
            == "S56-10.2-DEPENDENCY-ACCEPTANCE", "first node gate drifted")
    require(decision["first_failed_theorem_gate"]["gate_id"]
            == "M1011-ARCHITECTURE-RECONCILIATION", "first theorem gate drifted")
    require(decision["first_failed_release_gate"]["gate_id"]
            == "S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE",
            "first release assurance gate drifted")
    require(decision["first_failed_reproduction_gate"]["gate_id"]
            == "S56-10.6-HERMETIC-COLD-BUILD", "first reproduction gate drifted")
    require(decision["authoritative_remaining_machine_cut_set"]
            == ["M1011-N-SEPARATION"], "decision machine cut drifted")
    for key in (
        "validation_dependency_master_accepted", "predecessor_recipe_current",
        "authoritative_graph_reconciled", "structured_state_fresh",
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
        "--tmpfs", "/tmp",
        "--unshare-net", "--die-with-parent", "python3", "-B",
        f"Stage1_Instances/{THEOREM}/check_release.py",
    ], "release recipe argv drifted")
    require(spec["cwd"] == "." and spec["network_policy"] == "denied"
            and spec["timeout_seconds"] == 900 and spec["expected_exit"] == 0,
            "release recipe contract drifted")
    require(spec["covered_obligation_ids"] == ALL_OBLIGATIONS,
            "release recipe misses a frozen obligation")
    require(receipt["schema_version"] == "stage1-node-receipt/1.0",
            "receipt schema drifted")
    require(receipt["normative_profile"] == "machine-theorem-assurance/1.0",
            "receipt normative profile drifted")
    require(receipt["owner"] == "S56-M-1011-RELEASE worker slot1"
            and receipt["validated_at"] == "2026-07-15T02:18:21+08:00",
            "receipt owner/time identity drifted")
    require(receipt["support_state"] == "provisional_worker_selftest"
            and receipt["proposed_state"] == "[_]", "receipt support drifted")
    require(receipt["accepted"] is receipt["release_grade"] is False
            and receipt["master_accepted"] is False, "receipt claims acceptance")
    for key in (
        "schema_version", "recipe_id", "item_id", "theorem_id", "cwd", "argv",
        "env_allowlist", "timeout_seconds", "network_policy", "network_enforcement",
        "environment_enforcement", "expected_exit", "expected_outputs", "covered_obligation_ids",
        "covered_declarations", "scope_boundary",
    ):
        require(receipt["recipe"][key] == spec[key], f"receipt recipe drifted: {key}")
    require(receipt["recipe"]["observed_exit"] == 0,
            "receipt recipe observed exit drifted")
    require(receipt["dependency"] == decision["dependency"], "dependency ledgers disagree")
    require(receipt["known_failures"] == decision["known_failures"],
            "failure ledgers disagree")
    require(set(receipt["changed_paths"]) == CHANGED_PATHS,
            "receipt changed-path ledger drifted")
    for name, expected in receipt["inputs"].items():
        require(digest(ROOT / name) == expected, f"receipt input drifted: {name}")
    require(receipt["authority_inputs"] == AUTHORITY_INPUTS,
            "receipt authority ledger drifted")
    require(receipt["decision_sha256"] == digest(HERE / "release-decision.json"),
            "receipt decision hash drifted")
    require(receipt["release_spec_sha256"] == digest(HERE / "release-spec.json"),
            "receipt spec hash drifted")
    require(receipt["checker_sha256"] == digest(HERE / "check_release.py"),
            "receipt checker hash drifted")
    require(receipt["public_projection_sha256"] == digest(HERE / "release-validation.md"),
            "receipt projection hash drifted")
    require(receipt["result"]["verdict"] == "blocked"
            and receipt["result"]["audit_complete"] is False
            and receipt["result"]["theorem_complete"] is False,
            "receipt result is not the negative verdict")
    require(receipt["result"]["accepted_receipt_ids"] == [],
            "receipt accepts evidence")
    require(receipt["result"]["accepted_closed_obligation_ids"] == [],
            "receipt accepts obligation closure")
    require(receipt["result"]["authoritative_remaining_machine_cut_set"]
            == ["M1011-N-SEPARATION"], "receipt machine cut drifted")
    require(receipt["canonical_target"]["elaborated_expression_sha256"]
            == EXPRESSION_SHA256 and receipt["canonical_target"]
            ["registry_denominator_sha256"] == DENOMINATOR_SHA256,
            "receipt canonical target drifted")
    require(receipt["canonical_obligation_ids"] == ALL_OBLIGATIONS,
            "receipt canonical obligation list drifted")
    require(receipt["kernel_replayed_declarations"] == [
        "Stage1Instances.THM_M_1011.Proof.canonical",
        "Stage1Instances.THM_M_1011.Validation.independentlyReconstructedCanonical",
        "MeasureTheory.isCompact_closure_of_isTightMeasureSet",
        "MeasureTheory.isTightMeasureSet_of_isCompact_closure",
    ], "receipt replay declaration list drifted")
    require(receipt["commands_and_results"] == [
        {
            "cwd": ".", "argv": ["python3", "Docs/tools/check_stage1_standard.py"],
            "exit_code": 0,
            "result": "15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed",
        },
        {
            "cwd": ".", "argv": ["python3", "scripts/stage1_target.py", "check"],
            "exit_code": 0,
            "result": "1546 unique ordered targets at ranks 1 through 1546 passed",
        },
        {
            "cwd": ".", "argv": ["python3", "scripts/stage1_target.py", "show", THEOREM],
            "exit_code": 0,
            "result": "rank 260 remains planned, L0/rework_required, theorem_complete false",
        },
        {
            "cwd": ".", "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
            "exit_code": 0,
            "result": "14 obligations and 35 typed edges passed; frozen root remains open M5 at M1011-N-SEPARATION",
        },
        {
            "cwd": ".", "argv": ["python3", f"Stage1_Instances/{THEOREM}/check_proof.py"],
            "exit_code": 1, "classification": "expected_phase_packet_failure",
            "result": "static proof source, receipt, and hash checks reached the packet boundary; the proof-phase checker then correctly rejected the release-phase root packet (this command performed no Lean subprocess replay)",
        },
        {
            "cwd": ".", "argv": ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"],
            "exit_code": 1, "classification": "expected_freshness_failure",
            "result": "phase-bound predecessor checker stopped before Lean because its base and DAG assertions are stale",
        },
        {
            "cwd": ".", "argv": [
                "bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
                "--tmpfs", "/tmp",
                "--unshare-net", "--die-with-parent", "python3", "-B",
                f"Stage1_Instances/{THEOREM}/check_release.py",
            ],
            "exit_code": 0,
            "result": "current authority, hashes, network-isolated exact-root replay, and blocked terminal decisions passed",
        },
    ], "receipt command ledger drifted")
    handoff = receipt["worker_handoff"]
    require(handoff["exact_statements_added_or_changed"] == []
            and handoff["debt_vector_change_proposed"].startswith("none;"),
            "worker handoff overstates source or vector changes")
    require(handoff["typed_graph_changes"] == []
            and handoff["composition_certificates_changed"] == [],
            "worker handoff claims graph or composition edits")
    require(set(handoff["change_impact_set"]) == {
        ITEM, "S56-M-1011-VALIDATION freshness classification",
    }, "worker handoff impact set drifted")
    dirty = receipt["nonrelease_dirty_input_evidence"]
    require(dirty["tracked_patch_scope"] == []
            and dirty["tracked_patch_sha256"]
            == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "nonrelease tracked patch boundary drifted")
    for name, expected in dirty["untracked_input_hashes"].items():
        require(digest(ROOT / name) == expected,
                f"nonrelease untracked input drifted: {name}")

    require(set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }, "worker packet schema drifted")
    require(packet["item_id"] == ITEM and packet["state"] == "[_]"
            and packet["base_revision"] == BASE_REVISION, "worker packet identity drifted")
    require(set(packet["changed_paths"]) == CHANGED_PATHS, "changed-path ledger drifted")
    require(packet["known_failures"] == decision["known_failures"],
            "worker/decision failure ledger differs")
    blocked = [row for row in packet["commands"] if row.get("expected") == "blocked"]
    require(len(blocked) == 2 and all(row["exit_code"] == 1 for row in blocked),
            "worker packet predecessor blockers drifted")
    require({row.get("classification") for row in blocked} == {
        "expected_phase_packet_failure", "expected_freshness_failure",
    }, "worker packet blocker classifications drifted")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
                 "Proof.lean", "Validation.lean"):
        require(prohibited.search(code_without_comments(
            (HERE / name).read_text(encoding="utf-8"))) is None,
            f"prohibited Lean mechanism in {name}")

    require(MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable")
    require(git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
            "mathlib revision drifted")
    require(git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
            "mathlib tree drifted")
    require(git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == "",
            "pinned mathlib worktree is dirty before replay")
    replay_output, outputs = current_kernel_replay()
    current = receipt["current_kernel_replay"]
    require(current["stdout_sha256"] == hashlib.sha256(replay_output.encode()).hexdigest(),
            "current replay output hash drifted")
    require(current["stdout_bytes"] == len(replay_output.encode()),
            "current replay byte count drifted")
    require(current["axiom_report_count"] == 4,
            "current replay axiom report count drifted")
    require(current["observed_axioms"] == EXPECTED_AXIOMS,
            "receipt observed axiom list drifted")
    require(set(current["module_stdout_sha256"]) == set(outputs),
            "current replay module ledger drifted")
    for name, output in outputs.items():
        require(current["module_stdout_sha256"][name]
                == hashlib.sha256(output.encode()).hexdigest(),
                f"current replay module output drifted: {name}")
    environment = receipt["environment"]
    require(environment["platform"] == "Linux 7.0.0-27-generic x86_64",
            "receipt platform drifted")
    require(environment["lean_toolchain"] == "leanprover/lean4:v4.29.0"
            and environment["lean_commit"]
            == "98dc76e3c0a9b856c9b98726b713fb04fab16740",
            "receipt Lean identity drifted")
    require(environment["lean_executable_sha256"]
            == digest(Path(run(["lake", "env", "which", "lean"],
                               cwd=LEAN_ROOT, env=controlled_env()).strip())),
            "receipt Lean executable digest drifted")
    require(environment["lake_executable_sha256"]
            == digest(Path(run(["lake", "env", "which", "lake"],
                               cwd=LEAN_ROOT, env=controlled_env()).strip())),
            "receipt Lake executable digest drifted")
    require(environment["python_executable_sha256"]
            == digest(Path(os.path.realpath(sys.executable))),
            "receipt Python executable digest drifted")
    git_path = Path(os.path.realpath(shutil.which("git") or ""))
    bwrap_path = Path(os.path.realpath(shutil.which("bwrap") or ""))
    require(environment["git_executable_sha256"] == digest(git_path),
            "receipt Git executable digest drifted")
    require(environment["bubblewrap_executable_sha256"] == digest(bwrap_path),
            "receipt bubblewrap executable digest drifted")
    require(environment["mathlib_revision"] == MATHLIB_REVISION
            and environment["mathlib_tree"] == MATHLIB_TREE,
            "receipt mathlib identity drifted")
    require(git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == "",
            "pinned mathlib worktree changed during replay")

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

    print("PASS release inputs: target, DAG, receipts, registry, graph, and hashes agree")
    print("PASS current narrow Lean replay: exact proof and differential roots; four trust-zero reports")
    print("PASS fail-closed authority: planned H1/M5/R4; frozen cut M1011-N-SEPARATION; accepted receipts 0")
    print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional, stale, and unaccepted")
    print("BLOCKED graph reconciliation, AUDIT-Z, trust, cold/offline, and independent release gates")
    print("verdict=blocked audit_complete=false theorem_complete=false")


if __name__ == "__main__":
    main()
