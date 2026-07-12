#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0474-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0474"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0474-RELEASE"
THEOREM = "THM-M-0474"
BASE_REVISION = "2cf42e232e732b5d915dc077d91524b386861821"
BASE_TREE = "f37ffb23dda888fedd3da7b2d7a8bbceaee21d44"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "5475969fd23513d3b98134a6aaa747675a32a899f38be773a23cb330f2f590e8"
DENOMINATOR_SHA256 = "28dd518db2fe79a5006cbeb3fdd51b379f67cf388960c3f5fafdf2a7ad8b6a9e"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
GRAPH_CUT = [
    "M0474-L-NAT",
    "M0474-X-SOURCE",
    "M0474-S-FOUNDATION",
    "M0474-X-PROVENANCE",
    "M0474-X-READABLE",
    "M0474-X-WORKFLOW",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/instance.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
}


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(f"{name} is not a JSON object")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    try:
        completed = subprocess.run(
            argv,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=150,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        fail(f"command timed out: {argv!r}\n{error.stdout or ''}")
    if completed.returncode:
        fail(f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}")
    return completed.stdout


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def axiom_reports(output: str) -> list[set[str]]:
    blocks = re.findall(r"depends on axioms: \[(.*?)\]", output, flags=re.DOTALL)
    return [
        {name.strip() for name in block.split(",") if name.strip()}
        for block in blocks
    ]


def main() -> None:
    spec = load("release-spec.json")
    decision = load("release-decision.json")
    receipt = load("release-receipt.json")
    instance = load("instance.json")
    statement = load("statement.json")
    registry = load("obligation-registry.json")
    graphs = load("typed-graphs.json")
    proof = load("proof-receipt.json")
    validation = load("validation-receipt.json")
    dag = load("task-dag.json")
    selftest = json.loads(
        (ROOT / ".stage1-worker-selftest.json").read_text(encoding="utf-8")
    )
    targets = json.loads(
        (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
    )
    execution = json.loads(
        (ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(encoding="utf-8")
    )

    target = next(
        (entry for entry in targets["targets"] if entry["theorem_id"] == THEOREM), None
    )
    if target is None or target["execution_rank"] != 938:
        fail("target membership or rank drifted")
    if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
        fail("target authority no longer supports the blocked decision")
    item = next((row for row in execution["items"] if row["id"] == ITEM), None)
    if item is None:
        fail("release execution item is absent")
    expected_item_fields = {
        "theorem_id": THEOREM,
        "execution_rank": 938,
        "phase": "release",
        "layer": 6,
        "depends_on": ["S56-M-0474-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "children": [],
    }
    for key, value in expected_item_fields.items():
        if item.get(key) != value:
            fail(f"release execution item drifted at {key}")
    if item["state"] not in {"[ ]", "[_]"}:
        fail("a worker release check cannot consume accepted or invalid item state")
    authority_inputs = {
        "Docs/Stage1_Targets_rev-5.6.json": targets,
        "Docs/Stage1_Execution_DAG_rev-5.6.json": execution,
    }
    for relative, value in authority_inputs.items():
        if digest(ROOT / relative) != receipt["authority_inputs"][relative]:
            fail(f"release authority input drifted: {relative}")

    local_release = next(task for task in dag["tasks"] if task["id"] == ITEM)
    local_validation = next(
        task for task in dag["tasks"] if task["id"] == "S56-M-0474-VALIDATION"
    )
    if local_release["state"] != "open" or local_validation["state"] != "open":
        fail("local task authority no longer records an open dependency and release")
    if dag["accepted_states"]:
        fail("local task authority unexpectedly contains accepted state")
    if digest(HERE / "task-dag.json") != receipt["authority_inputs"]["task-dag.json"]:
        fail("local task authority input drifted")

    if spec["item_id"] != decision["item_id"] or decision["item_id"] != receipt["item_id"]:
        fail("release item identity mismatch")
    if spec["theorem_id"] != decision["theorem_id"] or decision["theorem_id"] != THEOREM:
        fail("release theorem identity mismatch")
    if decision["base_revision"] != receipt["base_revision"] or decision["base_revision"] != BASE_REVISION:
        fail("base revision mismatch")
    if decision["base_tree"] != receipt["base_tree"] or decision["base_tree"] != BASE_TREE:
        fail("base tree mismatch")
    if decision["decision_support"] != receipt["support_state"]:
        fail("release support classification mismatch")
    if receipt["support_state"] != "provisional_worker_selftest":
        fail("release evidence must remain provisional")
    if decision["release_grade"] is not False or receipt["release_grade"] is not False:
        fail("same-worker warm-cache evidence cannot be release grade")
    for name, expected in receipt["inputs"].items():
        if digest(HERE / name) != expected:
            fail(f"release receipt input drifted: {name}")
    if receipt["decision_id"] != decision["decision_id"]:
        fail("release receipt does not identify the reconciled decision")
    if receipt["canonical_target_expression_sha256"] != EXPRESSION_SHA256:
        fail("release receipt target fingerprint drifted")
    if receipt["registry_denominator_sha256"] != DENOMINATOR_SHA256:
        fail("release receipt registry fingerprint drifted")
    if receipt["changed_paths"] != sorted(CHANGED_PATHS):
        fail("release receipt changed paths are incomplete or out of canonical order")
    if receipt["master_acceptance"] != "pending_and_not_claimed":
        fail("release receipt falsely reports master acceptance")
    if receipt["owner"] != "Stage1 integration lane":
        fail("release receipt owner drifted")
    receipt_result = receipt["result"]
    if receipt_result["exit_code"] != 0 or receipt_result["verdict"] != "blocked":
        fail("release receipt result or verdict drifted")
    if receipt_result["authoritative_root_state"] != "H1/M3/R4_open":
        fail("release receipt authoritative root state drifted")
    if receipt_result["audit_complete"] is not False or receipt_result["theorem_complete"] is not False:
        fail("release receipt falsely reports a terminal decision")
    if receipt_result["audit_z"] != "fail_closed" or receipt_result["theorem_z"] != "fail_closed":
        fail("release receipt falsely reports AUDIT-Z or THEOREM-Z")
    for gate in (
        "dependency_master_acceptance",
        "hermetic_release_gate",
        "supply_chain_gate",
        "independent_verification_gate",
        "deterministic_bundle_gate",
    ):
        if receipt_result[gate] != "fail_closed":
            fail(f"release receipt silently cleared gate: {gate}")
    if receipt_result["master_acceptance_gate"] != "pending":
        fail("release receipt master gate drifted")
    if receipt["first_failed_gate"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
        fail("release receipt does not preserve the first failed gate")
    if receipt["known_failures"] != decision["known_failures"]:
        fail("release receipt and decision failure ledgers disagree")
    if receipt["retry_condition"] != decision["retry_condition"]:
        fail("release receipt and decision retry conditions disagree")
    if receipt["invalidation_inputs"] != decision["invalidation_inputs"]:
        fail("release receipt and decision invalidation inputs disagree")
    if receipt["freshness"]["review_due"] != decision["freshness"]["review_due"]:
        fail("release receipt and decision review due dates disagree")
    if receipt["freshness"]["revocation_state"] != decision["freshness"]["revocation_state"]:
        fail("release receipt and decision revocation states disagree")
    if receipt["freshness"]["incident_path"] != decision["freshness"]["incident_path"]:
        fail("release receipt and decision incident paths disagree")
    if not receipt["status_boundary"].startswith("Self-tested negative release reconciliation"):
        fail("release receipt status boundary drifted")
    snapshot = receipt["nonrelease_snapshot_binding"]
    if snapshot["base_revision"] != BASE_REVISION or snapshot["base_tree"] != BASE_TREE:
        fail("nonrelease snapshot base identity drifted")
    if set(snapshot["tracked_changed_paths"] + snapshot["untracked_owned_paths"]) != CHANGED_PATHS:
        fail("nonrelease snapshot path classification is incomplete")
    if snapshot["preexisting_untracked_paths"] != ["Formalizations/Lean/.lake"]:
        fail("pre-existing automation artifact classification drifted")

    expected_selftest_keys = {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    if set(selftest) != expected_selftest_keys:
        fail("worker self-test schema drifted")
    if selftest["item_id"] != ITEM or selftest["state"] != "[_]":
        fail("wrong self-test item or provisional state")
    if selftest["base_revision"] != BASE_REVISION:
        fail("self-test base revision mismatch")
    if set(selftest["changed_paths"]) != CHANGED_PATHS:
        fail("self-test changed paths are incomplete or overbroad")
    if not selftest["commands"] or not selftest["output_summary"].startswith("PASS:"):
        fail("self-test command/result summary is absent")
    if selftest["known_failures"] != decision["known_failures"]:
        fail("self-test and decision failure ledgers disagree")
    handoff_inputs = {
        ".stage1-worker-selftest.json": ROOT / ".stage1-worker-selftest.json",
        "README.md": HERE / "README.md",
        "instance.json": HERE / "instance.json",
        "release-phase.md": HERE / "release-phase.md",
    }
    for name, path in handoff_inputs.items():
        if digest(path) != receipt["handoff_input_hashes"][name]:
            fail(f"release handoff input drifted: {name}")

    if spec["argv"] != ["python3", f"Stage1_Instances/{THEOREM}/check_release.py"]:
        fail("release recipe argv drifted")
    if spec["cwd"] != "." or spec["network_policy"] != "denied":
        fail("release recipe working directory or network policy drifted")
    if spec["timeout_seconds"] != 180 or spec["expected_exit"] != 0:
        fail("release recipe bound drifted")
    if {item["obligation_id"] for item in registry["obligations"]} != set(
        spec["covered_obligation_ids"]
    ):
        fail("release recipe does not cover the frozen registry")

    for name, expected in decision["reconciled_inputs"].items():
        if digest(HERE / name) != expected:
            fail(f"reconciled input drifted: {name}")
    if decision["dependency"]["receipt_sha256"] != digest(HERE / "validation-receipt.json"):
        fail("validation dependency receipt hash drifted")
    if decision["dependency"]["receipt_id"] != validation["receipt_id"]:
        fail("validation dependency receipt identity drifted")
    if decision["dependency"]["item_id"] != validation["item_id"]:
        fail("validation dependency item identity drifted")
    if validation["support_state"] != "provisional_worker_selftest":
        fail("validation evidence is not provisional as reconciled")
    if validation["release_grade"] is not False or decision["dependency"]["master_accepted"] is not False:
        fail("validation dependency was falsely represented as accepted/release-grade")

    vector = {"H": "H1", "M": "M3", "R": "R4"}
    if instance["lifecycle"] != instance["lifecycle_mode"] or instance["lifecycle"] != "planned":
        fail("instance lifecycle drifted")
    if instance["root_vector"] != vector:
        fail("instance root vector drifted")
    if instance["accepted_receipt_ids"] or instance["accepted_proof_state"]:
        fail("instance unexpectedly contains accepted proof state")
    if instance["audit_complete"] is not False or instance["theorem_complete"] is not False:
        fail("instance unexpectedly claims a terminal decision")
    if statement["canonical_formal_target"]["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        fail("canonical target expression drifted")
    if registry["denominator_sha256"] != DENOMINATOR_SHA256:
        fail("obligation denominator drifted")
    closure = graphs["closure_boundary"]
    if closure["root_closed"] is not False or closure["root_machine_debt"] != "M3":
        fail("authoritative graph no longer supports the blocked decision")
    if closure["audit_complete"] is not False or closure["theorem_complete"] is not False:
        fail("authoritative graph unexpectedly claims a terminal decision")
    if closure["remaining_root_cut_set"] != GRAPH_CUT:
        fail("authoritative graph cut set drifted")
    if decision["authoritative_graph_remaining_root_cut_set"] != GRAPH_CUT:
        fail("release decision does not preserve the graph cut set")

    if proof["accepted"] is not False or proof["support_state"] != "provisional_worker_selftest":
        fail("proof receipt support state drifted")
    if proof["result"]["root_closed"] is not True:
        fail("release decision lost the provisional exact-root evidence")
    if proof["result"]["theorem_complete"] is not False:
        fail("proof receipt overstates theorem completion")
    validation_result = validation["result"]
    if validation_result["proof_dependency_master_accepted"] is not False:
        fail("validation receipt falsely reports dependency acceptance")
    if validation_result["authoritative_graph_root_closed"] is not False:
        fail("validation receipt contradicts authoritative graph state")
    if validation_result["hermetic_release_gate"] != "fail_closed":
        fail("validation receipt silently cleared the hermetic gate")
    if validation_result["independent_distinct_runner_gate"] != "fail_closed":
        fail("validation receipt silently cleared the independent gate")

    if decision["verdict"] != "blocked":
        fail("open release gates require a blocked verdict")
    if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
        fail("blocked worker release must not advance lifecycle")
    if decision["root_vector_before"] != vector or decision["root_vector_after"] != vector:
        fail("release decision silently changed the accepted root vector")
    if decision["audit_complete"] is not False or decision["theorem_complete"] is not False:
        fail("release decision falsely reports AUDIT-Z or THEOREM-Z")
    if decision["release_accepted"] is not False or decision["accepted_receipt_ids"]:
        fail("worker release decision falsely reports acceptance")
    if decision["first_failed_gate"]["gate_id"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
        fail("release decision does not identify the first failed gate")

    reconciliation = decision["evidence_reconciliation"]
    required_false_gates = (
        "authoritative_graph_reconciled",
        "accepted_root_m0_e1",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "accepted_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_offline_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    )
    for gate in required_false_gates:
        if reconciliation[gate] is not False:
            fail(f"release gate was silently cleared: {gate}")
    cut = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "master acceptance",
        "M0-W/E1",
        "H0 primary-source",
        "R0 structured reconstruction",
        "empty-cache network-denied cold build",
        "SBOM",
        "two signed attestations",
        "minimal release verifier",
        "protected CI",
        "deterministic content-addressed release bundle",
    ):
        if fragment not in cut:
            fail(f"release cut set omits {fragment!r}")

    toolchain_sha = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    manifest_sha = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
    if digest(LEAN_ROOT / "lean-toolchain") != toolchain_sha:
        fail("Lean toolchain file drifted")
    if digest(LEAN_ROOT / "lake-manifest.json") != manifest_sha:
        fail("dependency manifest drifted")
    env = os.environ.copy()
    env.update(spec["env_allowlist"])
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=env).strip()
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=env).strip())
    if digest(lean) != LEAN_SHA256:
        fail("Lean executable digest drifted")
    version = run([str(lean), "--version"], cwd=LEAN_ROOT, env=env)
    if "4.29.0" not in version or LEAN_COMMIT not in version:
        fail("Lean version drifted")
    if not MATHLIB.resolve().is_dir():
        fail("canonical pinned mathlib artifact is missing")
    if run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() != MATHLIB_REVISION:
        fail("mathlib revision drifted")
    if run(["git", "rev-parse", "HEAD^{tree}"], cwd=MATHLIB).strip() != MATHLIB_TREE:
        fail("mathlib tree drifted")
    if run(["git", "status", "--porcelain=v1"], cwd=MATHLIB):
        fail("mathlib dependency worktree is dirty before replay")

    source_hashes = {
        "Mathlib/FieldTheory/Finite/Basic.lean": "808bb4eddb8a4b48785e4430f944fe0827c96842dffa0c08cd21b5659bd85d44",
        "Mathlib/GroupTheory/OrderOfElement.lean": "42bef2580b87cd0fa6367cd2d57d30fb25fce373576a856cc84d27dad23fae23",
        "Mathlib/Data/Nat/Totient.lean": "bc3be754c653d34785636ed734355fc5e976719b4eddf3cb7f37175265f1c20f",
    }
    olean_hashes = {
        "Mathlib/FieldTheory/Finite/Basic.olean": "4cede73b3c7f85692307990d9cdaf819b5ac61dc50272e31586b7899d9f32119",
        "Mathlib/GroupTheory/OrderOfElement.olean": "33d0d5970b2ec79349ee6335e9f76842ff648e8594994ddd3da18ca8941c2858",
        "Mathlib/Data/Nat/Totient.olean": "e0f0c983aed45dd95fab75f06773eb7afe69f7ed1769071234b476a778bf69c6",
    }
    for relative, expected in source_hashes.items():
        if digest(MATHLIB / relative) != expected:
            fail(f"pinned mathlib source drifted: {relative}")
    for relative, expected in olean_hashes.items():
        if digest(MATHLIB / ".lake/build/lib/lean" / relative) != expected:
            fail(f"pinned mathlib olean drifted: {relative}")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(?:axiom|unsafe)\b",
        re.MULTILINE,
    )
    lean_files = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    for name in lean_files:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        if prohibited.search(source):
            fail(f"prohibited Lean mechanism in {name}")

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m0474-release-", dir=LEAN_ROOT) as tmp_name:
        tmp = Path(tmp_name)
        for name in lean_files:
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base_env = env.copy()
        base_env["LEAN_PATH"] = lean_path
        outputs["Statement.lean"] = run(
            [str(lean), "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
            cwd=LEAN_ROOT,
            env=base_env,
        )
        module_env = base_env.copy()
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        outputs["ObligationTree.lean"] = run(
            [str(lean), "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
            cwd=LEAN_ROOT,
            env=module_env,
        )
        outputs["Proof.lean"] = run(
            [str(lean), str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=module_env
        )
        outputs["Validation.lean"] = run(
            [str(lean), str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=module_env
        )

    if outputs["Statement.lean"].count("Type mismatch") != 4:
        fail("statement mutation checks did not produce four expected rejections")
    proof_reports = axiom_reports(outputs["Proof.lean"])
    validation_reports = axiom_reports(outputs["Validation.lean"])
    if len(proof_reports) != 18 or not all(report <= EXPECTED_AXIOMS for report in proof_reports):
        fail("proof axiom reports drifted")
    if len(validation_reports) != 3 or not all(report == EXPECTED_AXIOMS for report in validation_reports):
        fail("differential validation axiom reports drifted")
    if outputs["Proof.lean"].count("Declarations are sorry-free!") != 18:
        fail("proof sorry-free report count drifted")
    if outputs["Validation.lean"].count("Declarations are sorry-free!") != 3:
        fail("differential validation sorry-free report count drifted")
    combined = "".join(outputs.values())
    if "declaration uses 'sorry'" in combined or "sorryAx" in combined:
        fail("Lean replay reported a placeholder")
    if run(["git", "status", "--porcelain=v1"], cwd=MATHLIB):
        fail("mathlib dependency worktree changed during replay")

    if set(instance["owned_artifacts"]) != {path.name for path in HERE.iterdir() if path.is_file()}:
        fail("owned artifact inventory is stale")
    status = run(["git", "status", "--short", "--untracked-files=all"])
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    if actual_changed != CHANGED_PATHS:
        fail("actual changed paths do not match the release handoff")
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            fail(f"noncanonical text encoding or terminator: {path.name}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            fail(f"trailing whitespace in {path.name}")

    semantic_output = "\n".join(
        (
            (
                "PASS S56-M-0474-RELEASE: exact statement, direct root, frozen composition, "
                "and totient route kernel-replayed"
            ),
            (
                "PASS provisional trust observation: 18 proof and 3 differential declarations "
                "are sorry-free with allowed axiom subsets"
            ),
            (
                "PASS reconciliation: immutable input hashes, pinned dependency tree, graph cut, "
                "receipts, and unchanged authority agree"
            ),
            "BLOCKED first gate: S56-10.2-DEPENDENCY-ACCEPTANCE",
            (
                "BLOCKED release gates: H0/R0/trust, cold offline replay, supply chain, "
                "independent verification, deterministic bundle, and master acceptance"
            ),
            (
                "VERDICT blocked: lifecycle planned; root H1/M3/R4; audit_complete=false; "
                "theorem_complete=false; accepted_receipts=0"
            ),
        )
    )
    if receipt["result"]["semantic_output_sha256"] != hashlib.sha256(
        semantic_output.encode("utf-8")
    ).hexdigest():
        fail("release receipt semantic output hash drifted")
    print(semantic_output)


if __name__ == "__main__":
    main()
