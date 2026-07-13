#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0043-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0043"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0043-RELEASE"
THEOREM = "THM-M-0043"
BASE_REVISION = "59c86ca38b16fe4d3901ba66530aae4df0e881b0"
BASE_TREE = "2b8fc12c558d4fe807d7b4ac4b2c9a127002338e"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "a46ee23911b8027aa5de93149fd781def441429e386cb9181fc2064b2898557a"
DENOMINATOR_SHA256 = "1a92339af83640c1cf5d8853722d8c381b11a9d4139c4cb251cea3781d5b2af8"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
UNCERTIFIED_ID = "M0043-T-OPERATOR-DECOMP"
GRAPH_CUT = [
    "M0043-T-CONJUGATED-DIAGONAL",
    "M0043-X-SOURCE",
    "M0043-S-FOUNDATION",
    "M0043-X-PROVENANCE",
    "M0043-X-EVIDENCE",
    "M0043-X-TRUST",
    "M0043-X-READABLE",
    "M0043-X-WORKFLOW",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
}


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(f"{path} is not a JSON object")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
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


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def axiom_reports(output: str) -> list[set[str]]:
    blocks = re.findall(r"depends on axioms: \[(.*?)]", output, flags=re.DOTALL)
    return [
        {name.strip() for name in block.split(",") if name.strip()}
        for block in blocks
    ]


def main() -> None:
    spec = load(HERE / "release-spec.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    local_dag = load(HERE / "task-dag.json")
    selftest = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    if git("rev-parse", "HEAD") != BASE_REVISION or git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository base revision or tree drifted")
    target = next((row for row in targets["targets"] if row["theorem_id"] == THEOREM), None)
    if target is None or target["execution_rank"] != 1083:
        fail("target membership or execution rank drifted")
    if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
        fail("target authority no longer supports the blocked decision")

    release_item = next((row for row in execution["items"] if row["id"] == ITEM), None)
    validation_item = next(
        (row for row in execution["items"] if row["id"] == "S56-M-0043-VALIDATION"), None
    )
    expected_release_fields = {
        "theorem_id": THEOREM,
        "execution_rank": 1083,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0043-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    if release_item is None:
        fail("release item is absent from the execution DAG")
    for key, expected in expected_release_fields.items():
        if release_item.get(key) != expected:
            fail(f"release execution item drifted at {key}")
    if validation_item is None or validation_item["state"] != "[_]":
        fail("validation dependency is not the expected provisional worker projection")

    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in local_dag["tasks"] if row["id"] == "S56-M-0043-VALIDATION"
    )
    if local_release["state"] != "open" or local_validation["state"] != "open":
        fail("local task authority no longer records open validation and release items")
    if local_dag["accepted_states"]:
        fail("local task authority unexpectedly contains accepted state")

    if spec["item_id"] != decision["item_id"] or decision["item_id"] != receipt["item_id"]:
        fail("release item identity mismatch")
    if spec["theorem_id"] != decision["theorem_id"] or decision["theorem_id"] != THEOREM:
        fail("release theorem identity mismatch")
    if decision["base_revision"] != receipt["base_revision"] or receipt["base_revision"] != BASE_REVISION:
        fail("base revision mismatch")
    if decision["base_tree"] != receipt["base_tree"] or receipt["base_tree"] != BASE_TREE:
        fail("base tree mismatch")
    if decision["decision_support"] != receipt["support_state"]:
        fail("release support classification mismatch")
    if decision["release_grade"] is not False or receipt["release_grade"] is not False:
        fail("warm same-worker evidence cannot be release grade")
    if receipt["decision_id"] != decision["decision_id"]:
        fail("release receipt identifies the wrong decision")
    if receipt["master_acceptance"] != "pending_and_not_claimed":
        fail("release receipt falsely reports master acceptance")
    if receipt["canonical_target_expression_sha256"] != EXPRESSION_SHA256:
        fail("release receipt target fingerprint drifted")
    if receipt["registry_denominator_sha256"] != DENOMINATOR_SHA256:
        fail("release receipt registry fingerprint drifted")
    for name, expected in receipt["inputs"].items():
        if digest(HERE / name) != expected:
            fail(f"release receipt input drifted: {name}")
    authority_paths = {
        "Docs/Stage1_Targets_rev-5.6.json": ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        "Docs/Stage1_Execution_DAG_rev-5.6.json": ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "task-dag.json": HERE / "task-dag.json",
    }
    for name, path in authority_paths.items():
        if receipt["authority_inputs"][name] != digest(path):
            fail(f"release authority input drifted: {name}")

    for name, expected in decision["reconciled_inputs"].items():
        if digest(HERE / name) != expected:
            fail(f"reconciled input drifted: {name}")
    dependency = decision["dependency"]
    if dependency["receipt_sha256"] != digest(HERE / "validation-receipt.json"):
        fail("validation receipt dependency hash drifted")
    if dependency["receipt_id"] != validation["receipt_id"]:
        fail("validation receipt dependency identity drifted")
    if dependency["master_accepted"] is not False:
        fail("release decision falsely represents validation as master-accepted")
    if validation["support_state"] != "provisional_worker_selftest":
        fail("validation receipt support state drifted")
    if validation["release_grade"] is not False or validation["accepted"] is not False:
        fail("validation receipt was falsely represented as accepted or release-grade")

    vector = {"H": "H1", "M": "M3", "R": "R4"}
    if instance["lifecycle"] != "planned" or instance["lifecycle_mode"] != "planned":
        fail("authoritative instance lifecycle drifted")
    if instance["root_vector"] != vector:
        fail("authoritative instance vector drifted")
    if instance["accepted_receipt_ids"] or instance["accepted_proof_state"]:
        fail("authoritative instance unexpectedly contains accepted proof state")
    if instance["audit_complete"] is not False or instance["theorem_complete"] is not False:
        fail("authoritative instance unexpectedly claims terminal completion")
    if statement["canonical_formal_target"]["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        fail("canonical expression fingerprint drifted")
    if registry["denominator_sha256"] != DENOMINATOR_SHA256:
        fail("frozen denominator drifted")
    closure = graphs["closure_boundary"]
    if closure["root_closed"] is not False or closure["root_machine_debt"] != "M3":
        fail("authoritative graph no longer supports the blocked decision")
    if closure["accepted_closed_obligations"]:
        fail("authoritative graph unexpectedly contains accepted closure")
    if closure["audit_complete"] is not False or closure["theorem_complete"] is not False:
        fail("authoritative graph unexpectedly claims terminal completion")
    if closure["remaining_root_cut_set"] != GRAPH_CUT:
        fail("authoritative graph cut set drifted")

    if proof["support_state"] != "provisional_worker_selftest" or proof["accepted"] is not False:
        fail("proof receipt support state drifted")
    if proof["result"]["root_kernel_closed"] is not True:
        fail("provisional exact-root proof evidence was lost")
    certified_ids: set[str] = set()
    for certificate in proof["composition_certificates"]:
        certified_ids.add(certificate["parent"])
        certified_ids.update(certificate["children"])
    if set(proof["closed_obligation_ids"]) - certified_ids != {UNCERTIFIED_ID}:
        fail("proof receipt certificate gap changed")
    result = validation["result"]
    if result["exact_root_kernel_closed_locally"] is not True:
        fail("validation receipt no longer reports the provisional exact root")
    if result["accepted_root_closed"] is not False:
        fail("validation receipt falsely reports accepted root closure")
    if result["uncertified_claimed_proof_obligation_ids"] != [UNCERTIFIED_ID]:
        fail("validation no longer preserves the proof certificate gap")
    if len(result["locally_validated_obligation_ids"]) != 22:
        fail("validation local coverage count drifted")
    for gate in (
        "hermetic_release_gate",
        "complete_transitive_trust_and_provenance_gate",
        "independent_distinct_runner_gate",
    ):
        if result[gate] != "fail_closed":
            fail(f"validation receipt silently cleared {gate}")

    if decision["verdict"] != "blocked" or decision["release_accepted"] is not False:
        fail("open release gates require a blocked decision")
    if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
        fail("blocked release decision must not advance lifecycle")
    if decision["root_vector_before"] != vector or decision["root_vector_after"] != vector:
        fail("blocked release decision silently changed the accepted vector")
    if decision["audit_complete"] is not False or decision["theorem_complete"] is not False:
        fail("release decision falsely reports AUDIT-Z or THEOREM-Z")
    if decision["accepted_receipt_ids"]:
        fail("worker release decision falsely reports accepted receipts")
    if decision["first_failed_gate"]["gate_id"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
        fail("release decision lost the first failed gate")
    if decision["authoritative_graph_remaining_root_cut_set"] != GRAPH_CUT:
        fail("release decision lost the authoritative graph cut set")
    if decision["known_failures"] != receipt["known_failures"]:
        fail("release decision and receipt failure ledgers disagree")
    if decision["retry_condition"] != receipt["retry_condition"]:
        fail("release decision and receipt retry conditions disagree")
    if decision["invalidation_inputs"] != receipt["invalidation_inputs"]:
        fail("release decision and receipt invalidation inputs disagree")

    expected_selftest_keys = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    if set(selftest) != expected_selftest_keys:
        fail("worker self-test schema drifted")
    if selftest["item_id"] != ITEM or selftest["state"] != "[_]":
        fail("wrong worker self-test item or provisional state")
    if selftest["base_revision"] != BASE_REVISION:
        fail("worker self-test base revision drifted")
    if set(selftest["changed_paths"]) != CHANGED_PATHS:
        fail("worker self-test changed paths drifted")
    if selftest["known_failures"] != decision["known_failures"]:
        fail("worker self-test and decision failure ledgers disagree")
    if receipt["changed_paths"] != sorted(CHANGED_PATHS):
        fail("release receipt changed paths are incomplete or unsorted")

    expected_argv = ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    if spec["argv"] != expected_argv or receipt["recipe"]["argv"] != expected_argv:
        fail("release recipe argv drifted")
    if spec["cwd"] != "." or spec["network_policy"] != "denied":
        fail("release recipe cwd or network policy drifted")
    if spec["timeout_seconds"] != 180 or spec["expected_exit"] != 0:
        fail("release recipe resource or exit contract drifted")
    if {row["obligation_id"] for row in registry["obligations"]} != set(spec["covered_obligation_ids"]):
        fail("release recipe does not cover the frozen obligation registry")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    lean_names = ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    for name in lean_names:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        if prohibited.search(source):
            fail(f"prohibited Lean construct in {name}")

    if not MATHLIB.resolve().is_dir():
        fail("pinned mathlib artifact is unavailable")
    if git("rev-parse", "HEAD", cwd=MATHLIB) != MATHLIB_REVISION:
        fail("mathlib revision drifted")
    if git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) != MATHLIB_TREE:
        fail("mathlib tree drifted")
    if git("status", "--porcelain=v1", cwd=MATHLIB):
        fail("pinned mathlib worktree is dirty")
    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    if digest(Path(lean)) != LEAN_SHA256:
        fail("Lean executable identity drifted")
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    if "4.29.0" not in lean_version or LEAN_COMMIT not in lean_version:
        fail("Lean version drifted")

    base_env = os.environ.copy()
    base_env.update({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})
    with tempfile.TemporaryDirectory(prefix="m0043-release-") as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        statement_env = base_env.copy()
        statement_env["LEAN_PATH"] = lean_path
        run([lean, "-t", "0", "-o", "Statement.olean", "Statement.lean"], cwd=tmp, env=statement_env)
        module_env = base_env.copy()
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        obligation_output = run(
            [lean, "-t", "0", "-o", "ObligationTree.olean", "ObligationTree.lean"],
            cwd=tmp,
            env=module_env,
        )
        proof_output = run([lean, "-t", "0", "Proof.lean"], cwd=tmp, env=module_env)
        validation_output = run([lean, "-t", "0", "Validation.lean"], cwd=tmp, env=module_env)

    all_axioms = axiom_reports(obligation_output + proof_output + validation_output)
    if len(all_axioms) != 6 or any(report != EXPECTED_AXIOMS for report in all_axioms):
        fail(f"unexpected axiom reports: {all_axioms}")
    if proof_output.count("Declarations are sorry-free!") != 3:
        fail("proof sorry-free report count drifted")
    if validation_output.count("Declarations are sorry-free!") != 2:
        fail("differential sorry-free report count drifted")
    if "sorryAx" in obligation_output + proof_output + validation_output:
        fail("Lean output contains sorryAx")

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    if actual_changes != CHANGED_PATHS:
        fail(f"changed paths drifted: {sorted(actual_changes)}")
    for path in [HERE / name for name in (
        "release-spec.json", "release-decision.json", "check_release.py",
        "release-receipt.json", "release-phase.md",
    )] + [ROOT / ".stage1-worker-selftest.json"]:
        data = path.read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            fail(f"invalid text encoding or terminator: {path}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            fail(f"trailing whitespace: {path}")

    if receipt["environment"]["platform"] != f"{platform.system()} {platform.release()} {platform.machine()}":
        fail("release receipt platform drifted")
    if git("status", "--porcelain=v1", cwd=MATHLIB):
        fail("pinned mathlib worktree changed during replay")

    print("PASS provisional kernel: exact root and duplicate route replay at Lean trust level zero")
    print("PASS reconciliation: accepted authority remains planned H1/M3/R4 with root open")
    print("GAP proof evidence: M0043-T-OPERATOR-DECOMP lacks a composition-certificate mapping")
    print("BLOCKED release: validation is unaccepted; H0/R0, hermetic, supply-chain, and independent gates remain open")
    print("VERDICT blocked: lifecycle planned; audit_complete=false; theorem_complete=false; accepted_receipts=0")


if __name__ == "__main__":
    main()
