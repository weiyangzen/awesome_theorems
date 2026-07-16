#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0109 statement evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0109"
ITEM_ID = "S56-M-0109-STATEMENT"
BASE_REVISION = "778c2db4855d48868391ea236f702e592067e798"
BASE_TREE = "27abf0ec82dad50561a14d1db471126fb7ac8665"
GRAPH_SHA256 = "9db2a7cc29bf218211004677abe45ce1742f597405c2d879675dbc66542c4c8b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
FAILED_GATE = "S02-EXACT-TARGET.exact_source_identity_and_canonical_claim"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0109/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0109/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0109/source-statement-crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0109/statement-receipt.json",
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
    "message": (
        "The repository name and coordinate-ring gloss do not identify one exact "
        "proposition; the canonical Lean target and four required statement "
        "mutations remain unavailable."
    ),
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


def authoritative_item() -> dict:
    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    pattern = re.compile(
        r"^- \[ \] `S56-M-0109-STATEMENT` / `THM-M-0109` / `statement`: "
        r"Elaborate the exact Lean 4 target with the minimal pinned imports\. "
        r"\{attempts=0\}\n"
        r"  Depends: `S56-M-0109-INTAKE`\. Owned paths: "
        r"`Stage1_Instances/THM-M-0109`\. Gate: rev-5\.6 node-specific "
        r"receipt and master acceptance\.$",
        re.MULTILINE,
    )
    if len(pattern.findall(blueprint)) != 1:
        fail("sole task-state authority no longer has the exact open statement row")
    predecessor = re.compile(
        r"^- \[_\] `S56-M-0109-INTAKE` / `THM-M-0109` / `intake`: .*"
        r"\{attempts=1\}$",
        re.MULTILINE,
    )
    if len(predecessor.findall(blueprint)) != 1:
        fail("sole task-state authority predecessor state changed")

    execution = load("Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(
        (row for row in execution.get("items", []) if row.get("id") == ITEM_ID),
        None,
    )
    if not isinstance(item, dict):
        fail("assigned statement item disappeared")
    expected = {
        "theorem_id": THEOREM_ID,
        "execution_rank": 33,
        "phase": "statement",
        "layer": 1,
        "state": "[ ]",
        "depends_on": ["S56-M-0109-INTAKE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM_ID}"],
    }
    for field, value in expected.items():
        if item.get(field) != value:
            fail(f"authoritative statement field changed: {field}")
    return item


def check_authorities() -> dict:
    manifest = load("Docs/Stage1_Targets_rev-5.6.json")
    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")

    target = next(
        (row for row in manifest.get("targets", []) if row.get("theorem_id") == THEOREM_ID),
        None,
    )
    if not isinstance(target, dict) or target.get("execution_rank") != 33:
        fail("target manifest identity changed")
    if target.get("baseline") != "L0" or target.get("rework_required") is not True:
        fail("uniform L0 target boundary changed")
    if target.get("legacy_artifacts_accepted") is not False:
        fail("legacy artifact acceptance boundary changed")

    authoritative_item()

    node = next(
        (row for row in theorem_dag.get("theorems", []) if row.get("theorem_id") == THEOREM_ID),
        None,
    )
    if not isinstance(node, dict) or node.get("v2_execution_rank") != 268:
        fail("v2 theorem identity or rank changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency context changed")
    if node.get("phase_states", {}).get("intake") != "[_]":
        fail("intake predecessor state changed")
    if node.get("phase_states", {}).get("statement") != "[ ]":
        fail("statement phase state changed")
    for field in (
        "direct_hard_parents",
        "transitive_hard_ancestors",
        "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
    ):
        if node.get(field) != []:
            fail(f"unexpected nonempty dependency context: {field}")
    if sha256("Docs/Stage1_Theorem_DAG_v2.json") != GRAPH_SHA256:
        fail("theorem DAG bytes changed")

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
        expanded = [value.format(theorem_id=THEOREM_ID) for value in candidates or []]
        if relative not in expanded:
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
    return phase_contract


def check_ledger() -> None:
    ledger = load("Stage1_Instances/THM-M-0109/dependency-reuse-ledger.json")
    expected = {
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
    if ledger != expected:
        fail("empty dependency-reuse ledger is stale or incomplete")


def check_statement_boundary() -> dict:
    record = load(ROLE_PATHS["statement_record"])
    if record.get("schema_version") != "stage1-statement/1.0":
        fail("statement record schema changed")
    if record.get("item_id") != ITEM_ID or record.get("theorem_id") != THEOREM_ID:
        fail("statement record identity changed")
    if record.get("canonical_claim_status") != (
        "blocked_source_identity_and_exact_claim_unresolved"
    ):
        fail("statement ambiguity is no longer explicit")
    if record.get("canonical_statement") is not None:
        fail("a canonical mathematical statement was invented")
    formal = record.get("canonical_formal_target")
    if not isinstance(formal, dict):
        fail("canonical formal target boundary is malformed")
    if formal.get("module") != ROLE_PATHS["statement_source"]:
        fail("statement source path changed")
    for field in (
        "declaration_or_expression",
        "elaborated_expression_sha256",
        "environment_fingerprint",
    ):
        if formal.get(field) is not None:
            fail(f"blocked record fabricates {field}")
    if record.get("direct_imports") != [] or record.get("minimal_imports_proven") is not False:
        fail("blocked record fabricates canonical import minimality")
    if record.get("statement_fingerprints") != [] or record.get("credited_transports") != []:
        fail("blocked record fabricates a fingerprint or transport")

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
    if any(
        record.get(field) is not False
        for field in (
            "statement_elaborated",
            "phase_predicate_proven",
            "phase_accepted",
            "audit_complete",
            "theorem_complete",
        )
    ):
        fail("statement record overstates acceptance or completion")

    dependency = record.get("dependency_context")
    if not isinstance(dependency, dict):
        fail("statement dependency context is malformed")
    for field in (
        "parent_inspection_order",
        "direct_parent_ids",
        "transitive_ancestor_ids",
        "hard_edge_ids",
        "reuse_hint_ids",
        "shared_group_ids",
    ):
        if dependency.get(field) != []:
            fail(f"statement dependency closure changed: {field}")
    if dependency.get("provider_acceptance_inherited") is not False:
        fail("statement record transfers provider acceptance")

    lean_text = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    if re.findall(r"^import ([^\s]+)$", lean_text, re.MULTILINE):
        fail("declaration-free statement boundary unexpectedly imports a module")
    prohibited = re.compile(
        r"(?m)^\s*(?:def|abbrev|structure|class|inductive|axiom|constant|opaque|"
        r"unsafe\s+(?:def|theorem)|theorem|example)\b|"
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b"
    )
    if prohibited.search(lean_text):
        fail("statement boundary contains a declaration or proof escape")
    for phrase in (
        "intentionally declaration-free",
        "not a canonical target",
        "No canonical declaration is emitted",
    ):
        if phrase not in lean_text:
            fail("Lean statement boundary omits its non-credit status")

    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    for phrase in (
        "Scheme-theoretic Chow's",
        "coordinate-ring",
        "Required resolution",
        "no exact-statement",
    ):
        if phrase not in crosswalk:
            fail("source crosswalk omits the fail-closed boundary")
    repository_source = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    if "周炜良引理" not in repository_source or "代数簇的坐标环性质" not in repository_source:
        fail("repository source record changed")
    legacy = ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_033.lean"
    if hashlib.sha256(legacy.read_bytes()).hexdigest() != (
        "4b4e66cfbc43f85647f9081d81d4b524f77bc49fcebec27d9cb9a511288d4242"
    ):
        fail("legacy discovery source changed")
    return mutations


def check_receipt(phase_contract: dict, mutations: dict) -> None:
    receipt = load(ROLE_PATHS["phase_receipt"])
    top_level_required = {
        pointer.removeprefix("/")
        for pointer in phase_contract.get("phase_receipt_required_fields", [])
        if isinstance(pointer, str) and pointer.count("/") == 1
    }
    if not top_level_required <= set(receipt):
        fail("phase receipt lacks a contract-required field")
    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        fail("phase receipt schema changed")
    if receipt.get("item_id") != ITEM_ID or receipt.get("theorem_id") != THEOREM_ID:
        fail("phase receipt identity changed")
    if receipt.get("phase") != "statement" or receipt.get("intent") != "audit":
        fail("phase receipt phase or intent changed")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        fail("phase receipt base identity changed")
    if receipt.get("claim_order") != {
        "v2_execution_rank": 268,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        fail("receipt claim order changed")
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

    expected_changed = {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0109/Statement.lean",
        "Stage1_Instances/THM-M-0109/check_statement.py",
        "Stage1_Instances/THM-M-0109/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0109/source-statement-crosswalk.md",
        "Stage1_Instances/THM-M-0109/statement-receipt.json",
        "Stage1_Instances/THM-M-0109/statement.json",
    }
    if set(packet.get("changed_paths", [])) != expected_changed:
        fail("worker packet changed-path inventory changed")
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.splitlines()
    actual_changed: set[str] = set()
    for line in status:
        relative = line[3:]
        if relative == "Formalizations/Lean/.lake":
            continue
        if relative != ".stage1-worker-selftest.json" and not relative.startswith(
            f"Stage1_Instances/{THEOREM_ID}/"
        ):
            fail(f"unexpected changed path outside worker ownership: {relative}")
        actual_changed.add(relative)
    if actual_changed != expected_changed:
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
    if inputs.get("parent_inspection_order") != []:
        fail("receipt parent inspection order changed")
    if inputs.get("provider_acceptance_inherited") is not False:
        fail("receipt transfers provider acceptance")
    for name, relative in (
        ("dependency_reuse_ledger", "Stage1_Instances/THM-M-0109/dependency-reuse-ledger.json"),
        ("validator", "Stage1_Instances/THM-M-0109/check_statement.py"),
    ):
        binding = inputs.get(name)
        if not isinstance(binding, dict):
            fail(f"receipt lacks {name} binding")
        if binding.get("path") != relative or binding.get("sha256") != sha256(relative):
            fail(f"receipt {name} binding is stale")
        if binding.get("git_blob") != git_blob(relative):
            fail(f"receipt {name} Git blob is stale")


def check_text_boundaries() -> None:
    selected = set(ROLE_PATHS.values()) | {
        "Stage1_Instances/THM-M-0109/check_statement.py",
        "Stage1_Instances/THM-M-0109/dependency-reuse-ledger.json",
    }
    for relative in selected:
        data = (ROOT / relative).read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            fail(f"text artifact has a malformed byte boundary: {relative}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            fail(f"text artifact has trailing whitespace: {relative}")


def main() -> None:
    phase_contract = check_authorities()
    check_ledger()
    mutations = check_statement_boundary()
    check_receipt(phase_contract, mutations)
    check_text_boundaries()
    print(json.dumps(SEMANTIC, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
