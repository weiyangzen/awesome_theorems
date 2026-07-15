#!/usr/bin/env python3
"""Fail-closed source, graph, receipt, packet, and kernel checks for this proof node."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0890-PROOF"
THEOREM = "THM-M-0890"
ROOT_ID = "M0890-ROOT"
BASE_REVISION = "20808d65f53d8801e78f061504b93bb7efd49489"
BASE_TREE = "a5bf33a278a7a285878c89177838ae1a0dcc9990"
EXPRESSION_SHA256 = "512ebe658ca83b7fb4bb3d3565122d065e3bc6e589898b4f3cf74ab2e12ea54d"
DENOMINATOR_SHA256 = "259c6e160437f0fc2646c6f1e302441c3e129c6d3e70346d04438ea3f7a45169"
PROOF_SHA256 = "b41705e275a454f9412a05b8f09b5be8701ff989840c7be216629824a5b08e68"
LEAN_OUTPUT_SHA256 = "1feb46c6727f181724eb22479f0345d5a36682b795841eb89c07983539cd9d59"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_INPUT_HASHES = {
    "Statement.lean": "beb6cbe0437f78f26188cc3ed1ebe82bed84d2a07f1f8ea1abd78468740a787f",
    "statement.json": "dd9b94824f9f5e3a4f8627da05c132a69fcd18cdf476a11046d253ec4d78be21",
    "ObligationTree.lean": "6959e302e3676c172f1db7003014b56e153057f367ecaebb3b8c81a86bf27ff2",
    "obligation-registry.json": "079b565a392e4e81e291e3bed8b45d4b6b77e51668a733bce7435b8c89857110",
    "typed-graphs.json": "8c9906787a3fe386d98ddef9442904ce43f63eeead34c15a4f17ca664eaf0903",
    "anchor-audit.json": "b922f69cb16eed05e8f29f281460a928e787619a7c7f4c923ea312a1bf098549",
    "validation-specs.json": "45f9587856a82ef19ffac2e21f180c67dc3a16d00ee9518638b74f9fb21675ed",
    "task-dag.json": "8540d20add89f3528bbf1d69969025828862dd3043d30eeae2f4db8890dd74c7",
    "instance.json": "030d142bc502f89b768709136ebac408d8fe02d2d779de272291944c0ada8101",
}
INPUT_RECEIPT_KEYS = {
    "Statement.lean": "statement_sha256",
    "statement.json": "statement_json_sha256",
    "ObligationTree.lean": "obligation_tree_sha256",
    "obligation-registry.json": "obligation_registry_sha256",
    "typed-graphs.json": "typed_graphs_sha256",
    "anchor-audit.json": "anchor_audit_sha256",
    "validation-specs.json": "validation_specs_sha256",
    "task-dag.json": "task_dag_sha256",
    "instance.json": "instance_json_sha256",
}
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
DECLARATIONS = (
    "leastAdjacencyEigenvalue_le_eigenvalue",
    "leastAdjacencyEigenvalue_neg",
    "denominatorPositive_proof",
    "shiftedAdjacency_posSemidef",
    "independentSet_adjacency_quadratic_zero",
    "independentSet_characteristic_norm",
    "regular_adjacency_mulVec_one",
    "independentSet_adjacency_one",
    "one_dotProduct_one_real",
    "centered_shifted_quadratic",
    "independentSet_scalar_nonnegative",
    "indepNum_pos",
    "maximumIndependentSetEstimate_proof",
    "divisionFreeInequality_proof",
    "ratioAssembly_proof",
    "hoffmanRatioBound_proof",
)
EXACT_EVIDENCE_IDS = [
    "M0890-ROOT",
    "M0890-N-MAX-WITNESS",
    "M0890-N-DENOMINATOR",
    "M0890-T-DIVISION-FREE",
    "M0890-T-ASSEMBLE",
]
PLAN_PARENTS = {
    "M0890-N-DENOMINATOR",
    "M0890-L-LEAST-NEGATIVE",
    "M0890-L-SCALAR-ESTIMATE",
    "M0890-L-QUADRATIC-EVAL",
    "M0890-L-PSD-PRINCIPAL",
    "M0890-T-RESTRICTED-FORM",
    "M0890-C-PRINCIPAL",
    "M0890-L-HOFFMAN-PSD",
    "M0890-L-COMMON-EIGENBASIS",
    "M0890-B-ALPHA-POSITIVE",
}
MAPPED_IDS = [
    "M0890-ROOT", "M0890-S-TARGET", "M0890-S-LEAST",
    "M0890-S-INDEPENDENCE", "M0890-S-BOUNDARY", "M0890-S-TRANSPORT",
    "M0890-S-FOUNDATION", "M0890-N-MAX-WITNESS", "M0890-N-LEAST-MIN",
    "M0890-L-LEAST-NEGATIVE", "M0890-N-DENOMINATOR",
    "M0890-L-REGULAR-ONES", "M0890-L-ONES-ORTHOGONAL",
    "M0890-C-HOFFMAN-MATRIX", "M0890-L-COMMON-EIGENBASIS",
    "M0890-L-HOFFMAN-PSD", "M0890-C-PRINCIPAL", "M0890-L-PSD-PRINCIPAL",
    "M0890-L-INDEPENDENT-ZERO", "M0890-T-RESTRICTED-FORM",
    "M0890-C-ONES-VECTOR", "M0890-L-QUADRATIC-EVAL",
    "M0890-B-ALPHA-POSITIVE", "M0890-L-SCALAR-ESTIMATE",
    "M0890-T-DIVISION-FREE", "M0890-T-ASSEMBLE",
]
PROOF_REACHABLE_IDS = [
    "M0890-ROOT", "M0890-T-ASSEMBLE", "M0890-N-DENOMINATOR",
    "M0890-L-LEAST-NEGATIVE", "M0890-N-LEAST-MIN", "M0890-L-REGULAR-ONES",
    "M0890-S-BOUNDARY", "M0890-T-DIVISION-FREE", "M0890-N-MAX-WITNESS",
    "M0890-L-SCALAR-ESTIMATE", "M0890-L-QUADRATIC-EVAL",
    "M0890-L-PSD-PRINCIPAL", "M0890-L-HOFFMAN-PSD",
    "M0890-C-HOFFMAN-MATRIX", "M0890-L-COMMON-EIGENBASIS",
    "M0890-L-ONES-ORTHOGONAL", "M0890-C-PRINCIPAL",
    "M0890-T-RESTRICTED-FORM", "M0890-L-INDEPENDENT-ZERO",
    "M0890-C-ONES-VECTOR", "M0890-B-ALPHA-POSITIVE",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}

if not __debug__:
    raise SystemExit("THM-M-0890 proof checker requires assertions; do not use python -O")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
    value: dict[str, object] = {}
    for key, item in pairs:
        assert key not in value, f"duplicate JSON key: {key}"
        value[key] = item
    return value


def load(path: Path) -> dict:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def check_text(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, f"invalid byte: {path}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def check_source() -> None:
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, digest in EXPECTED_INPUT_HASHES.items():
        assert sha256(HERE / name) == digest, f"prerequisite changed: {name}"
    assert sha256(HERE / "Proof.lean") == PROOF_SHA256
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert sha256(LEAN_ROOT / "lean-toolchain") == (
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    )
    assert sha256(LEAN_ROOT / "lake-manifest.json") == (
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
    )

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1440,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-0890-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0890-OBLIGATION_TREE"
    )
    assert predecessor["state"] in {"[_]", "[x]"}
    task_dag = load(HERE / "task-dag.json")
    local_item = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_item["state"] == "open" and local_item["evidence_ids"] == []
    assert task_dag["accepted_states"] == []

    source = (HERE / "Proof.lean").read_text(encoding="utf-8")
    code = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    code = re.sub(r"--.*", "", code)
    code = re.sub(
        r"^.*(?:assert_no_sorry|#print sorries).*$", "", code, flags=re.MULTILINE
    )
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|extern|native_decide|proof_wanted)\b|"
        r"^\s*(?:axiom|constant|unsafe|opaque)\b",
        re.MULTILINE,
    )
    assert forbidden.search(code) is None
    assert "import ObligationTree" in source
    assert "theorem hoffmanRatioBound_proof : HoffmanRatioBoundTarget.{u}" in source
    assert "root_of_ratio_assembly ratioAssembly_proof" in source
    for name in DECLARATIONS:
        assert re.search(rf"^theorem {name}\b", source, re.MULTILINE), name
        assert f"assert_no_sorry {name}" in source
        assert f"#print axioms {name}" in source


def check_graph_and_receipt() -> None:
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    receipt = load(HERE / "proof-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    formal_target = statement["canonical_formal_target"]
    assert formal_target["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0890.HoffmanRatioBoundTarget"
    )
    assert formal_target["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal_target["statement_file_sha256"] == EXPECTED_INPUT_HASHES["Statement.lean"]
    assert instance["theorem_id"] == THEOREM
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert registry["registry_id"] == "THM-M-0890-OBLIGATIONS-v1"
    assert registry["registry_version"] == 1
    assert registry["root_obligation_id"] == ROOT_ID
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MAPPED_IDS
    assert len(registry["obligations"]) == 33
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []

    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["root_node_id"] == f"{THEOREM}-ROOT"
    assert {node["obligation_id"] for node in graphs["nodes"]} >= set(MAPPED_IDS)
    boundary = graphs["closure_boundary"]
    assert boundary["closed_obligations"] == []
    assert boundary["root_closed"] is False
    assert boundary["accepted_root_machine_debt"] == "M3"
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    plans = graphs["unverified_decomposition_plans"]
    assert len(plans) == 10
    plan_ids = [plan["plan_id"] for plan in plans]
    plan_parents = [plan["parent_obligation_id"] for plan in plans]
    assert len(plan_ids) == len(set(plan_ids)) == 10
    assert len(plan_parents) == len(set(plan_parents)) == 10
    assert set(plan_parents) == PLAN_PARENTS
    assert set(plan_ids) == {f"DECOMP-{parent}" for parent in PLAN_PARENTS}
    assert all(
        plan["status"]
        == "source_body_decomposition_unverified_as_child_to_parent_composition"
        for plan in plans
    )

    children: dict[str, list[str]] = {}
    for edge in graphs["graphs"]["proof"]["edges"]:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: list[str] = []

    def visit(identifier: str) -> None:
        if identifier in reachable:
            return
        reachable.append(identifier)
        for child in children.get(identifier, []):
            visit(child)

    visit(ROOT_ID)
    assert reachable == PROOF_REACHABLE_IDS
    assert set(reachable) <= set(MAPPED_IDS)

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["execution_rank"] == 1440 and receipt["phase"] == "proof"
    assert receipt["intent"] == "prove"
    assert receipt["depends_on"] == ["S56-M-0890-OBLIGATION_TREE"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["canonical_declaration"] == (
        "Stage1Instances.THM_M_0890.HoffmanRatioBoundTarget"
    )
    assert receipt["exact_root_declaration"] == (
        "Stage1Instances.THM_M_0890_Proof.hoffmanRatioBound_proof"
    )
    assert receipt["registry_id"] == registry["registry_id"]
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    assert receipt["proof_body"]["terminal_body_id"] == f"sha256:{PROOF_SHA256}"
    assert receipt["exact_declaration_evidence_ids"] == EXACT_EVIDENCE_IDS
    assert receipt["mapped_proof_graph_id_count"] == len(MAPPED_IDS)
    assert receipt["mapped_proof_graph_ids"] == MAPPED_IDS
    assert receipt["proof_reachable_id_count"] == len(PROOF_REACHABLE_IDS)
    assert receipt["proof_reachable_ids"] == PROOF_REACHABLE_IDS
    assert receipt["closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["internal_per_node_composition_credit"] is False
    assert receipt["unverified_internal_composition_count"] == len(plans)
    for name, key in INPUT_RECEIPT_KEYS.items():
        assert receipt["inputs"][key] == sha256(HERE / name), key
    assert receipt["inputs"]["proof_validation_md_sha256"] == sha256(
        HERE / "proof-validation.md"
    )
    assert receipt["inputs"]["lean_toolchain_sha256"] == sha256(
        LEAN_ROOT / "lean-toolchain"
    )
    assert receipt["inputs"]["lake_manifest_sha256"] == sha256(
        LEAN_ROOT / "lake-manifest.json"
    )

    recipe = receipt["recipe"]
    assert set(recipe) == {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    }
    assert recipe["cwd"] == "." and recipe["env_allowlist"] == {}
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["recipe_id"] == "S56-M-0890-PROOF-isolated-trust-zero-v1"
    assert recipe["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_proof.py", "--run-lean"
    ]
    assert recipe["timeout_seconds"] == 900
    assert len(recipe["expected_outputs"]) == 1
    assert recipe["covered_obligation_ids"] == EXACT_EVIDENCE_IDS
    assert len(recipe["covered_declarations"]) == len(DECLARATIONS)
    assert recipe["covered_declarations"] == receipt["exact_declarations"]

    result = receipt["result"]
    assert result["exit_code"] == 0 and result["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert set(result["axioms"]) == EXPECTED_AXIOMS
    assert result["placeholder_scan"] == "pass"
    assert result["root_kernel_closed"] is True
    assert result["accepted_root_closed"] is False
    assert result["machine_debt_proposal"] == "M0-L"
    assert result["accepted_state_changed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["root_vector_before"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert receipt["root_vector_after_proposed"] == {"H": "H1", "M": "M0-L", "R": "R4"}
    assert receipt["root_vector_after_worker_selftest"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["first_failed_downstream_gate"].startswith("S56-M-0890-VALIDATION:")
    assert "Provisional proof-node evidence only" in receipt["status_boundary"]
    assert receipt["accepted_receipt_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS

    packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet) == packet_fields
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"] and packet["output_summary"]
    assert "unaccepted M0-L root proposal" in packet["output_summary"]
    assert "theorem_complete=false" in packet["output_summary"]
    command_rows = packet["commands"]
    assert all(
        set(row) == {"command", "exit_code", "result"}
        and isinstance(row["exit_code"], int)
        and row["command"]
        and row["result"]
        for row in command_rows
    )
    exits = {row["command"]: row["exit_code"] for row in command_rows}
    stale = f"python3 -B Stage1_Instances/{THEOREM}/check_obligation_tree.py"
    assert exits[stale] == 1
    assert all(code == 0 for command, code in exits.items() if command != stale)
    for required in (
        "python3 Docs/tools/check_stage1_standard.py",
        "python3 scripts/stage1_target.py check",
        f"python3 scripts/stage1_target.py show {THEOREM}",
        f"python3 -B Stage1_Instances/{THEOREM}/check_proof.py",
        f"python3 -B Stage1_Instances/{THEOREM}/check_proof.py --run-lean",
    ):
        assert exits[required] == 0

    status = output(
        "git", "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        check_text(ROOT / relative)
    for path in (HERE / "proof-receipt.json", HERE / "proof-validation.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text


def run_lean() -> str:
    lean_bin = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    env = {
        **os.environ,
        "LEAN_PATH": lean_path,
        "LEAN_NUM_THREADS": "1",
        "LC_ALL": "C",
        "LANG": "C",
        "NO_COLOR": "1",
    }
    with tempfile.TemporaryDirectory(prefix="thm-m-0890-proof-") as temporary:
        temp = Path(temporary)
        commands = (
            ([lean_bin, "--trust=0", "-t0", "-o", str(temp / "Statement.olean"), "Statement.lean"], env),
            ([lean_bin, "--trust=0", "-t0", "-o", str(temp / "ObligationTree.olean"), "ObligationTree.lean"], {**env, "LEAN_PATH": f"{temp}:{lean_path}"}),
            ([lean_bin, "--trust=0", "-t0", "-o", str(temp / "Proof.olean"), "Proof.lean"], {**env, "LEAN_PATH": f"{temp}:{lean_path}"}),
        )
        combined = ""
        for argv, command_env in commands:
            result = subprocess.run(
                argv,
                cwd=HERE,
                env=command_env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=300,
                check=False,
            )
            combined += result.stdout
            if result.returncode:
                sys.stdout.write(combined)
                raise SystemExit(result.returncode)
    assert "Declarations are sorry-free!" in combined
    assert "sorryAx" not in combined and "error:" not in combined
    for name in DECLARATIONS:
        prefix = f"THM_M_0890_Proof.{name}' depends on axioms: ["
        assert combined.count(prefix) == 1
        start = combined.index(prefix) + len(prefix)
        end = combined.index("]", start)
        axioms = {
            part.strip() for part in combined[start:end].replace("\n", "").split(",")
        }
        assert axioms == EXPECTED_AXIOMS
    return combined


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-lean", action="store_true")
    args = parser.parse_args()
    check_source()
    check_graph_and_receipt()
    print(
        "PASS THM-M-0890 proof packet: exact M0-L root proposal, "
        "26 mapped required-machine IDs, 10 uncredited decomposition plans"
    )
    if args.run_lean:
        lean_output = run_lean()
        digest = hashlib.sha256(lean_output.encode()).hexdigest()
        assert digest == LEAN_OUTPUT_SHA256
        print(
            "PASS THM-M-0890 Lean --trust=0: "
            f"16 clean axiom reports; output sha256 {digest}"
        )


if __name__ == "__main__":
    main()
