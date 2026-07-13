#!/usr/bin/env python3
"""Fail-closed source, pin, graph, receipt, and worker-packet checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


if not __debug__:
    raise SystemExit("check_proof.py must run without Python optimization")


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0821-PROOF"
THEOREM = "THM-M-0821"
BASE_REVISION = "5931467f7eefac7a6e57777cc3082e4a2edc03d4"
BASE_TREE = "45a10c953e5dc79c1eb9ae7d755ee84866717775"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TERMINAL_SOURCE_SHA256 = "b19d4cbe58af9422dc36864d1ad1eee717c264a90d94fd579d3c8305f0feb630"
TERMINAL_OLEAN_SHA256 = "d55fb20a47a998695477eb5503c15f4f3c2eafd82425c96e233245f814473f48"
STATEMENT_EXPRESSION_SHA256 = "8f5d05428a35e3b6f13947097ac52417ba900b3cf9b1b45c0bb173766c914d7c"
REGISTRY_DENOMINATOR_SHA256 = "4ea4814dfb5bf3db63946381630ecfa30114c54515612c9e385fa660b53bbc75"
EVIDENCE_IDS = [
    "M0821-ROOT",
    "M0821-T-ROOT-COMPOSE",
    "M0821-B-MAXIMUM",
    "M0821-T-ATTAIN",
    "M0821-C-MIDDLE-LAYER",
    "M0821-L-MIDDLE-ANTICHAIN",
    "M0821-C-MIDDLE-SIZED",
    "M0821-L-MIDDLE-CARD",
    "M0821-T-UPPER",
    "M0821-L-SPERNER-UPPER",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def run_lean() -> str:
    lean_root = ROOT / "Formalizations/Lean"
    lean_bin = subprocess.check_output(
        ["lake", "env", "which", "lean"], cwd=lean_root, text=True
    ).strip()
    lean_path = subprocess.check_output(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=lean_root, text=True
    ).strip()
    with tempfile.TemporaryDirectory(prefix="thm-m-0821-proof-") as temporary:
        for source, output_name, path_prefix in (
            (HERE / "Statement.lean", "Statement.olean", lean_path),
            (HERE / "ObligationTree.lean", "ObligationTree.olean", temporary + os.pathsep + lean_path),
        ):
            result = subprocess.run(
                [lean_bin, str(source), "-o", str(Path(temporary) / output_name)],
                cwd=ROOT,
                env=os.environ | {"LEAN_PATH": path_prefix},
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=180,
                check=False,
            )
            if result.returncode:
                sys.stdout.write(result.stdout)
                raise SystemExit(result.returncode)
        result = subprocess.run(
            [lean_bin, str(HERE / "Proof.lean")],
            cwd=ROOT,
            env=os.environ | {"LEAN_PATH": temporary + os.pathsep + lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def check_lean_output(lean_output: str) -> None:
    assert lean_output.count("Declarations are sorry-free!") >= 4
    expected_axioms = ["propext", "Classical.choice", "Quot.sound"]
    for declaration in (
        "IsAntichain.sperner",
        "Stage1Instances.THM_M_0821.Proof.middleLayerAttainment",
        "Stage1Instances.THM_M_0821.Proof.universalUpperBound",
        "Stage1Instances.THM_M_0821.Proof.spernerMaximum",
    ):
        match = re.search(
            re.escape(f"'{declaration}' depends on axioms:") + r"\s*\[([^]]*)\]",
            lean_output,
        )
        assert match is not None, declaration
        axioms = [name.strip() for name in match.group(1).split(",") if name.strip()]
        assert axioms == expected_axioms, (declaration, axioms)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1379
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["depends_on"] == ["S56-M-0821-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["state"] == "[ ]"
    assert item["deliverable"] == "Implement or pin/import the required proof bodies without placeholders."
    prerequisite = next(
        row for row in execution["items"] if row["id"] == "S56-M-0821-OBLIGATION_TREE"
    )
    assert prerequisite["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_dag["accepted_states"] == []
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|constant|opaque|unsafe)\b|"
        r"\b(?:implemented_by|native_decide)\b",
        re.MULTILINE,
    )
    assert prohibited.search(proof) is None
    for fragment in (
        "import ObligationTree",
        "theorem middleLayerAttainment",
        "attainment_of_middleLayer",
        "middleLayerAntichain_of_sized pinned_middleLayerSized",
        "pinned_middleLayerCardinality",
        "theorem universalUpperBound",
        "upperBound_of_sperner pinned_upperBound",
        "theorem spernerMaximum",
        "root_of_terminal <| compose_root <|",
        "maximumSplit_of_packages middleLayerAttainment universalUpperBound",
        "assert_no_sorry IsAntichain.sperner",
        "#print axioms spernerMaximum",
    ):
        assert fragment in proof, fragment
    lean_log_path = os.environ.get("THM_M_0821_LEAN_LOG")
    if lean_log_path:
        lean_output = Path(lean_log_path).read_text(encoding="utf-8")
    else:
        lean_output = run_lean()
    check_lean_output(lean_output)

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    terminal_source = mathlib / "Mathlib/Combinatorics/SetFamily/LYM.lean"
    terminal_olean = mathlib / ".lake/build/lib/lean/Mathlib/Combinatorics/SetFamily/LYM.olean"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    terminal_text = terminal_source.read_text(encoding="utf-8")
    for marker in (
        "theorem _root_.IsAntichain.sperner",
        "have : 0 < ((Fintype.card α).choose (Fintype.card α / 2) : ℚ≥0)",
        "choose_le_middle _ _",
        "lubell_yamamoto_meshalkin_inequality_sum_inv_choose h𝒜",
    ):
        assert marker in terminal_text
    assert prohibited.search(terminal_text) is None

    proof_edges = graphs["graphs"]["proof"]["edges"]
    children: dict[str, list[str]] = {}
    for edge in proof_edges:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = ["M0821-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(children.get(obligation, []))
    assert len(reachable) == 24
    assert set(EVIDENCE_IDS) <= reachable
    plans = graphs["unverified_decomposition_plans"]
    assert len(plans) == 8
    assert all(
        row["status"] == "source_body_decomposition_unverified_as_child_to_parent_composition"
        for row in plans
    )
    certificates = graphs["composition_certificates"]
    assert len(certificates) == 6
    assert {row["checked_declaration"] for row in certificates} == {
        "Stage1Instances.THM_M_0821_Obligations.root_of_terminal",
        "Stage1Instances.THM_M_0821_Obligations.compose_root",
        "Stage1Instances.THM_M_0821_Obligations.maximumSplit_of_packages",
        "Stage1Instances.THM_M_0821_Obligations.attainment_of_middleLayer",
        "Stage1Instances.THM_M_0821_Obligations.middleLayerAntichain_of_sized",
        "Stage1Instances.THM_M_0821_Obligations.upperBound_of_sperner",
    }

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert registry["status_observed_after_freeze"]["closed_obligations"] == []
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["theorem_complete"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"] == "S56-M-0821-PROOF-pinned-20260713T231725+0800"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["proof_body"]["terminal_source_sha256"] == TERMINAL_SOURCE_SHA256
    assert receipt["proof_body"]["terminal_olean_sha256"] == TERMINAL_OLEAN_SHA256
    assert receipt["content_addressed"] is False
    assert receipt["content_addressed_recipe_ids"] == []
    assert receipt["content_addressed_receipt_ids"] == []
    assert receipt["validator_inputs"]["check_proof_sha256"] == sha256(Path(__file__))
    assert receipt["validator_inputs"]["check_proof_sh_sha256"] == sha256(HERE / "check_proof.sh")
    assert receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
    assert receipt["inputs"]["obligation_tree_sha256"] == sha256(HERE / "ObligationTree.lean")
    assert receipt["inputs"]["obligation_registry_sha256"] == sha256(HERE / "obligation-registry.json")
    assert receipt["inputs"]["typed_graphs_sha256"] == sha256(HERE / "typed-graphs.json")
    assert receipt["exact_declarations"] == [
        "Stage1Instances.THM_M_0821.Proof.middleLayerAttainment",
        "Stage1Instances.THM_M_0821.Proof.universalUpperBound",
        "Stage1Instances.THM_M_0821.Proof.spernerMaximum",
    ]
    assert receipt["root_evidence"]["root_kernel_declaration_closed"] is True
    assert receipt["root_evidence"]["accepted_root_closed"] is False
    assert receipt["root_evidence"]["machine_debt_proposal"] == "M0-W"
    assert receipt["root_evidence"]["closed_obligation_ids"] == []
    assert receipt["root_evidence"]["exact_declaration_evidence_ids"] == EVIDENCE_IDS
    assert set(receipt["root_evidence"]["mapped_proof_graph_ids"]) == reachable
    assert receipt["root_evidence"]["mapped_proof_graph_id_count"] == len(reachable)
    assert receipt["root_evidence"]["internal_per_node_composition_credit"] is False
    assert receipt["root_evidence"]["unverified_internal_composition_count"] == len(plans)
    assert receipt["root_evidence"]["checked_composition_certificate_count"] == len(certificates)
    assert receipt["recipe"]["recipe_id"] == "VAL-M0821-PROOF-LEAN"
    assert receipt["recipe"]["cwd"] == "."
    assert receipt["recipe"]["argv"] == [
        "bash", "Stage1_Instances/THM-M-0821/check_proof.sh"
    ]
    assert receipt["recipe"]["network_policy"] == "denied"
    assert receipt["recipe"]["expected_exit"] == 0
    assert receipt["recipe"]["covered_ids"] == EVIDENCE_IDS
    assert receipt["result"]["exit_code"] == 0
    assert receipt["result"]["output_sha256"] == "0462d9eba0c69a3ec2ff79d3ced4906abdc4606692a2602b49cb39bb8eb6d619"
    assert receipt["result"]["output_bytes"] == 13145
    assert receipt["result"]["deterministic_repeat_count"] == 2
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["placeholder_scan"] == "pass"
    assert receipt["result"]["accepted_state_changed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    commands = packet["commands"]
    assert isinstance(commands, list) and len(commands) == 13
    command_by_name = {row["command"]: row for row in commands}
    assert command_by_name["bash Stage1_Instances/THM-M-0821/check_proof.sh"]["exit_code"] == 0
    assert command_by_name["python3 -B Stage1_Instances/THM-M-0821/check_proof.py"]["exit_code"] == 0
    assert command_by_name["python3 -B Stage1_Instances/THM-M-0821/check_obligation_tree.py"]["exit_code"] == 1
    assert command_by_name["PYTHONOPTIMIZE=1 python3 -B Stage1_Instances/THM-M-0821/check_proof.py"]["exit_code"] == 1
    assert all(set(row) == {"command", "exit_code", "result"} for row in commands)
    assert all(isinstance(row["result"], str) and row["result"] for row in commands)
    lake_link = ROOT / "Formalizations/Lean/.lake"
    assert lake_link.is_symlink()
    assert lake_link.resolve() == Path("/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake")
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    for relative in CHANGED_PATHS:
        path = ROOT / relative
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0821 proof phase: exact pinned root and frozen composition elaborate")
    print("provisional root proposal: M0-W; internal per-node composition credit withheld")
    print("theorem_complete=false")


if __name__ == "__main__":
    main()
