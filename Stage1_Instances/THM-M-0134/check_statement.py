#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0134 statement evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0134"
ITEM_ID = "S56-M-0134-STATEMENT"
BASE_REVISION = "dae1951609072752d49d111bf00e78e4512f2d14"
BASE_TREE = "9d8cc27cc0e09489c78b0bdbdeb57b15c5840f13"
GRAPH_SHA256 = "3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
FAILED_GATE = "S02-EXACT-TARGET.exact_source_statement_identity_and_theorem_variant_selection"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0134/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0134/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0134/source-statement-crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0134/statement-receipt.json",
}
SEMANTIC = {
    "schema_version": "stage1-validator-semantic-result/1.0",
    "item_id": ITEM_ID,
    "theorem_id": THEOREM_ID,
    "phase": "statement",
    "status": "blocked",
    "verdict": "blocked",
    "phase_accepted": False,
    "audit_complete": False,
    "theorem_complete": False,
    "phase_predicate_proven": False,
    "first_failed_gate": FAILED_GATE,
    "open_obligations": 4,
    "stale_inputs": [],
    "blocked": True,
    "message": "The source does not identify one exact Burnside-Young proposition; the canonical Lean target and required statement mutations remain unavailable.",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def load(relative: str) -> dict:
    try:
        value = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {relative}: {exc}")
    if not isinstance(value, dict):
        fail(f"{relative} must contain one JSON object")
    return value


def sha256(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def check() -> None:
    manifest = load("Docs/Stage1_Targets_rev-5.6.json")
    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    record = load(ROLE_PATHS["statement_record"])
    receipt = load(ROLE_PATHS["phase_receipt"])
    ledger = load("Stage1_Instances/THM-M-0134/dependency-reuse-ledger.json")

    target = next(
        (row for row in manifest.get("targets", []) if row.get("theorem_id") == THEOREM_ID),
        None,
    )
    if not isinstance(target, dict) or target.get("execution_rank") != 50:
        fail("target manifest identity changed")
    if target.get("baseline") != "L0" or target.get("rework_required") is not True:
        fail("uniform L0 target boundary changed")
    if target.get("legacy_artifacts_accepted") is not False:
        fail("legacy artifact acceptance boundary changed")

    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.splitlines()
    actual_changed = {".stage1-worker-selftest.json"}
    for line in status:
        relative = line[3:]
        if relative == "Formalizations/Lean/.lake":
            continue
        if relative == ".stage1-worker-selftest.json":
            continue
        if not relative.startswith(f"Stage1_Instances/{THEOREM_ID}/"):
            fail(f"unexpected changed path outside worker ownership: {relative}")
        actual_changed.add(relative)

    node = next(
        (row for row in theorem_dag.get("theorems", []) if row.get("theorem_id") == THEOREM_ID),
        None,
    )
    if not isinstance(node, dict) or node.get("v2_execution_rank") != 284:
        fail("v2 theorem identity or rank changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency context changed")
    for field in (
        "direct_hard_parents",
        "transitive_hard_ancestors",
        "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
    ):
        if node.get(field) != []:
            fail(f"unexpected nonempty dependency context: {field}")

    if contract.get("schema_version") != "stage1-phase-acceptance-contracts/1.0":
        fail("phase acceptance contract schema changed")
    if sha256("Docs/Stage1_Phase_Acceptance_Contracts.json") != CONTRACT_SHA256:
        fail("phase acceptance contract bytes changed")
    phase_contract = next(
        (row for row in contract.get("phases", []) if row.get("phase") == "statement"),
        None,
    )
    if not isinstance(phase_contract, dict) or phase_contract.get("layer") != 1:
        fail("statement phase contract changed")
    selected_roles = {
        row.get("role"): row.get("path_candidates")
        for row in phase_contract.get("required_artifact_roles", [])
    }
    for role, relative in ROLE_PATHS.items():
        candidates = selected_roles.get(role)
        if not isinstance(candidates, list) or relative not in [
            value.format(theorem_id=THEOREM_ID) for value in candidates
        ]:
            fail(f"contract no longer selects {role}")
    candidates = [
        row.get("path_pattern") for row in phase_contract.get("validator_candidates", [])
    ]
    if candidates != [
        "Stage1_Instances/{theorem_id}/check_statement.py",
        "Stage1_Instances/{theorem_id}/check_statement_artifacts.py",
    ]:
        fail("statement validator candidates changed")
    if (HERE / "check_statement_artifacts.py").exists():
        fail("more than one statement validator candidate exists")

    expected_ledger = {
        "schema_version": "stage1-dependency-reuse-ledger/1.1",
        "consumer_theorem_id": THEOREM_ID,
        "observed_theorem_dag_sha256": GRAPH_SHA256,
        "dependency_context_sha256": CONTEXT_SHA256,
        "repository_revision": BASE_REVISION,
        "direct_parent_ids": [],
        "transitive_ancestor_ids": [],
        "hard_edge_ids": [],
        "reuse_hint_ids": [],
        "shared_group_ids": [],
        "inspections": [],
        "reuse_decisions": [],
        "unresolved_compatibility_obligations": [],
    }
    if ledger != expected_ledger:
        fail("empty dependency-reuse ledger is stale or incomplete")

    if record.get("schema_version") != "stage1-statement/1.0":
        fail("statement record schema changed")
    if record.get("item_id") != ITEM_ID or record.get("theorem_id") != THEOREM_ID:
        fail("statement record identity changed")
    for field in (
        "canonical_statement",
        "canonical_formal_target",
        "elaborated_expression_sha256",
        "environment_fingerprint_for_canonical_target",
    ):
        if record.get(field) is not None:
            fail(f"blocked record fabricates {field}")
    if record.get("statement_fingerprints") != [] or record.get("credited_transports") != []:
        fail("blocked record fabricates a fingerprint or transport")
    if record.get("minimal_imports_proven") is not False:
        fail("blocked record fabricates canonical import minimality")
    mutations = record.get("mutation_tests")
    required_mutations = {
        "removed_hypothesis",
        "changed_domain",
        "changed_binder_scope",
        "boundary_case",
    }
    if not isinstance(mutations, dict) or set(mutations) != required_mutations:
        fail("statement mutation inventory is incomplete")
    if set(mutations.values()) != {"not_executable_without_a_canonical_statement"}:
        fail("blocked mutation status changed")
    if record.get("first_failed_gate") != FAILED_GATE:
        fail("statement record first failed gate changed")
    if any(record.get(field) is not False for field in (
        "statement_elaborated",
        "phase_predicate_proven",
        "phase_accepted",
        "audit_complete",
        "theorem_complete",
    )):
        fail("statement record overstates acceptance or completion")

    lean_text = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    imports = re.findall(r"^import ([^\s]+)$", lean_text, re.MULTILINE)
    if imports != record.get("candidate_surface_probe", {}).get("direct_imports"):
        fail("candidate probe import record is stale")
    if not all(token in lean_text for token in (
        "#check Nat.Partition",
        "#check CandidateSymmetricGroup",
        "#check CandidateComplexRep",
        "#check Representation.IsIrreducible",
    )):
        fail("candidate object-vocabulary probe is incomplete")
    prohibited = re.compile(
        r"(?m)^\s*(axiom|constant|opaque|unsafe\s+(?:def|theorem)|theorem)\b|"
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide)\b"
    )
    if prohibited.search(lean_text):
        fail("statement probe contains a proof escape or theorem declaration")

    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    for phrase in (
        "Competing interpretations",
        "Required resolution",
        "not source-admitted",
        "supplies no H0",
    ):
        if phrase not in crosswalk:
            fail("source crosswalk omits the fail-closed boundary")

    required_receipt_fields = {
        pointer.removeprefix("/")
        for pointer in phase_contract.get("phase_receipt_required_fields", [])
        if isinstance(pointer, str) and pointer.count("/") == 1
    }
    if not required_receipt_fields <= set(receipt):
        fail("phase receipt lacks a contract-required field")
    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        fail("phase receipt schema changed")
    if receipt.get("item_id") != ITEM_ID or receipt.get("theorem_id") != THEOREM_ID:
        fail("phase receipt identity changed")
    if receipt.get("phase") != "statement" or receipt.get("intent") != "audit":
        fail("phase receipt phase or intent changed")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        fail("phase receipt base identity changed")
    if receipt.get("support_state") != "provisional_worker_selftest":
        fail("phase receipt support state changed")
    if receipt.get("proposed_state") != "[_]" or receipt.get("accepted") is not False:
        fail("worker receipt claims master acceptance")
    if receipt.get("verdict") != "blocked" or receipt.get("selftest_status") != "passed":
        fail("receipt no longer records a self-tested blocker")
    result = receipt.get("selftest_result")
    if not isinstance(result, dict) or result.get("exit_code") != 0:
        fail("receipt lacks a successful blocker self-test result")
    if not isinstance(result.get("commands"), list) or not result["commands"]:
        fail("receipt lacks exact self-test commands")
    if receipt.get("first_failed_gate") != FAILED_GATE:
        fail("receipt first failed gate changed")
    if receipt.get("statement_fingerprints") != []:
        fail("receipt fabricates a statement fingerprint")
    if receipt.get("mutation_tests") != mutations:
        fail("receipt and statement mutation boundaries disagree")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("receipt overstates a terminal decision")
    if receipt.get("semantic_result") != SEMANTIC:
        fail("receipt and validator semantic result disagree")

    packet = load(".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }:
        fail("worker packet field set changed")
    if packet.get("item_id") != ITEM_ID or packet.get("state") != "[_]":
        fail("worker packet identity or state changed")
    if packet.get("base_revision") != BASE_REVISION:
        fail("worker packet base revision changed")
    if packet.get("commands") != result.get("commands"):
        fail("worker packet and receipt command records disagree")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet and receipt known failures disagree")
    if set(packet.get("changed_paths", [])) != actual_changed:
        fail("worker packet changed paths do not match the Git delta")

    bindings = receipt.get("artifact_bindings")
    if not isinstance(bindings, dict) or set(bindings) != set(ROLE_PATHS):
        fail("receipt does not bind every contract-selected role")
    for role, relative in ROLE_PATHS.items():
        binding = bindings.get(role)
        if not isinstance(binding, dict):
            fail(f"missing artifact binding for {role}")
        if binding.get("role") != role or binding.get("path") != relative:
            fail(f"artifact binding identity changed for {role}")
        if role == "phase_receipt":
            if binding.get("sha256") is not None or binding.get("git_blob") is not None:
                fail("self-referential receipt binding must be scheduler-owned")
        elif binding.get("sha256") != sha256(relative) or binding.get("git_blob") != git_blob(relative):
            fail(f"artifact binding is stale for {role}")

    inputs = receipt.get("inputs")
    if not isinstance(inputs, dict):
        fail("receipt inputs are malformed")
    for name, relative in (
        ("dependency_reuse_ledger", "Stage1_Instances/THM-M-0134/dependency-reuse-ledger.json"),
        ("validator", "Stage1_Instances/THM-M-0134/check_statement.py"),
    ):
        binding = inputs.get(name)
        if not isinstance(binding, dict):
            fail(f"receipt lacks {name} binding")
        if binding.get("path") != relative or binding.get("sha256") != sha256(relative):
            fail(f"receipt {name} binding is stale")
        if binding.get("git_blob") != git_blob(relative):
            fail(f"receipt {name} Git blob is stale")

    for relative in {*ROLE_PATHS.values(), "Stage1_Instances/THM-M-0134/check_statement.py"}:
        data = (ROOT / relative).read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            fail(f"text artifact has a malformed byte boundary: {relative}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            fail(f"text artifact has trailing whitespace: {relative}")


def main() -> None:
    check()
    print(json.dumps(SEMANTIC, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
