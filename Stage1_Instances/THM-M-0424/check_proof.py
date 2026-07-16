#!/usr/bin/env python3
"""Fail-closed semantic proof validator for S56-M-0424-PROOF."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0424"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0424-PROOF"
THEOREM = "THM-M-0424"
BASE_REVISION = "2dc5a410b68eff806858fd6ed0cb33d57f6209f7"
BASE_TREE = "841bdd6114e7436cff4a3a1ff248fc1e884a9ddc"
GRAPH_SHA256 = "3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa"
CONTEXT_SHA256 = "f6c5258e1d42d3812d7d616b9a9135ed71401872573195920e5bf8aa56d99683"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
FLR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
FLR_TREE = "32c9eace926573a9981787ae97643e520353c893"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
STATEMENT_EXPRESSION_SHA256 = "62cfee70820b2f8bc4e924505b8984993322f623109868957b726b3446fc3aa8"
DENOMINATOR_SHA256 = "83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_HASHES = {
    "Statement.lean": "e6ee85656ac5bf9576546f2d56ab6e9ff20eb85452be4a9be4ea6a06a55ae7e9",
    "ObligationTree.lean": "f5a825653aabeb9365b86ab7c1c91a2291291258a5ba7131cab2027127ec10cb",
    "UniverseCounterexample-2026-07-14-head-5753c6ed.lean":
        "2b7580c0ccb344736e3643522f4b96b0efeb66db4d310b90cb0745a2dad9e5e8",
    "obligation-registry.json": "2886ccb997b40e63b7bee6241954eaca770db39a71ce9a701af890f600a0f6f5",
    "typed-graphs.json": "079c3176794bd6caf665cd0bcac2cb14fcf8b6a1c99a39256728d5fb16df69cd",
    "anchor-audit.json": "7b2941e9728a1a0913168ae4ae336bdfd009d53181bc9f5f537d591c3b9adc60",
    "validation-specs.json": "2fea3704a2dd481c07801e4456d378d6b7096c17da8630cc11bf78c872fca4cc",
}
PROOF_RECEIPT_INPUT_HASHES = {
    **EXPECTED_HASHES,
    "dependency-reuse-ledger.json":
        "f98d1a49362c5b83874e23358dbca0009bd3c02ac53482e759fad6b2e61bc7f2",
}
SHARED_GROUPS = [
    "SHARED-MODULE-1e1e801c1afdcc1f",
    "SHARED-MODULE-6e79d52d6da9de82",
    "SHARED-MODULE-d1f653e354a315e1",
]
SHARED_PROVIDERS = {
    "SHARED-MODULE-1e1e801c1afdcc1f": (
        "THM-M-0039",
        {
            "Stage1_Instances/THM-M-0039/IntakeProbe.lean":
                "d7c4c9e201164f66fc3ef4aac7cdbf7830f1aded53a4236a6ca6b9ef6f56aed7",
            "Stage1_Instances/THM-M-0039/instance.json":
                "84e7922423ede59acfe79bde5bb7b75e742aa782d039d732a92826fc7c671786",
        },
    ),
    "SHARED-MODULE-6e79d52d6da9de82": (
        "THM-M-0037",
        {
            "Stage1_Instances/THM-M-0037/IntakeProbe.lean":
                "9693c4ec79ad5df88504f187819dd0857954d1c9d9ec43630d1b9e0b9ce32bf6",
            "Stage1_Instances/THM-M-0037/instance.json":
                "732f8a2df1df5ac8323ec93e01232c8d1d3109c9aee771a4dc3b9b6fc1e437cd",
        },
    ),
    "SHARED-MODULE-d1f653e354a315e1": (
        "THM-M-0038",
        {
            "Stage1_Instances/THM-M-0038/IntakeProbe.lean":
                "ceac8a1ffaa8adafb317a912413a5939bacd18a88fe7362072a9a6fd07bf81ec",
            "Stage1_Instances/THM-M-0038/instance.json":
                "26e2a46f2a0fd38d0a4ad2c204b1bcaae47b188cde8d01414c788279f88852f9",
        },
    ),
}
PHASES = {
    "intake", "statement", "anchor_audit", "obligation_tree", "proof",
    "validation", "release",
}
OPEN_IDS = {
    "M0424-ROOT", "M0424-S-TARGET", "M0424-S-BOUNDARY",
    "M0424-S-FOUNDATION", "M0424-C-TENSOR-ALG", "M0424-C-TENSOR-CSA",
    "M0424-C-TENSOR-CONGR", "M0424-C-ONE", "M0424-C-OPPOSITE",
    "M0424-L-DESCENT", "M0424-L-ASSOC", "M0424-L-COMM",
    "M0424-L-UNIT", "M0424-L-INVERSE", "M0424-T-LAWDATA",
    "M0424-T-COMPOSE", "M0424-X-SOURCE", "M0424-X-PROVENANCE",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    re.MULTILINE,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return value


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 180,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )


def checked_output(
    argv: list[str], *, cwd: Path = ROOT, preserve_whitespace: bool = False,
) -> str:
    result = run(argv, cwd=cwd)
    if result.returncode:
        raise ValueError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout if preserve_whitespace else result.stdout.strip()


def git(*argv: str, cwd: Path = ROOT) -> str:
    return checked_output(["git", *argv], cwd=cwd)


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if depth:
            if source.startswith("/-", index):
                depth += 1
                index += 2
            elif source.startswith("-/", index):
                depth -= 1
                index += 2
            else:
                index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                index += 2
            elif source[index] == '"':
                in_string = False
                index += 1
            else:
                index += 1
        elif source.startswith("/-", index):
            depth = 1
            index += 2
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        elif source[index] == '"':
            in_string = True
            index += 1
        else:
            output.append(source[index])
            index += 1
    if depth or in_string:
        raise ValueError("unterminated Lean comment or string")
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output,
        re.DOTALL,
    )
    if match is None:
        raise ValueError(f"missing axiom report for {declaration}")
    return {
        item.strip()
        for item in match.group(1).replace("\n", "").split(",")
        if item.strip()
    }


def validate_ledger() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    if ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1":
        raise ValueError("dependency ledger schema mismatch")
    if ledger.get("consumer_theorem_id") != THEOREM:
        raise ValueError("dependency ledger theorem mismatch")
    if ledger.get("observed_theorem_dag_sha256") != GRAPH_SHA256:
        raise ValueError("dependency ledger graph binding is stale")
    if ledger.get("dependency_context_sha256") != CONTEXT_SHA256:
        raise ValueError("dependency ledger context binding is stale")
    if ledger.get("repository_revision") != BASE_REVISION:
        raise ValueError("dependency ledger repository binding is stale")
    for key in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "inspections", "unresolved_compatibility_obligations",
    ):
        if ledger.get(key) != []:
            raise ValueError(f"dependency ledger field {key} is not the audited empty closure")
    if ledger.get("shared_group_ids") != SHARED_GROUPS:
        raise ValueError("dependency ledger shared-group context is incomplete")
    closure = ledger.get("closure_audit")
    if not isinstance(closure, dict) or closure.get("parent_inspection_order") != []:
        raise ValueError("dependency ledger lacks the exact empty parent inspection order")
    if closure.get("inspected_parent_ids") != []:
        raise ValueError("dependency ledger invents a hard-parent inspection")
    if closure.get("status") != "empty_hard_parent_closure_inspected":
        raise ValueError("dependency ledger does not record the empty closure audit")
    decisions = ledger.get("reuse_decisions")
    if not isinstance(decisions, list) or len(decisions) != len(SHARED_GROUPS):
        raise ValueError("dependency ledger does not decide every shared group exactly once")
    if [row.get("source_id") for row in decisions] != SHARED_GROUPS:
        raise ValueError("dependency ledger shared-group decision order changed")
    for row in decisions:
        source_id = row["source_id"]
        provider, artifacts = SHARED_PROVIDERS[source_id]
        if row.get("provider_theorem_id") != provider or row.get("decision") != "not_applicable":
            raise ValueError("shared-module hint was improperly credited as proof reuse")
        if row.get("context_digest") != CONTEXT_SHA256 or not row.get("non_reuse_reason"):
            raise ValueError("shared-module decision lacks context or non-reuse reason")
        if row.get("inspected_member_artifacts") != artifacts:
            raise ValueError("shared-module inspected artifact set changed")
        for relative, expected in artifacts.items():
            if sha256(ROOT / relative) != expected:
                raise ValueError(f"shared-module inspected artifact drifted: {relative}")


def replay_counterexample() -> None:
    lean = Path(checked_output(["lake", "env", "which", "lean"], cwd=LEAN_ROOT))
    lake = Path(checked_output(["lake", "env", "which", "lake"], cwd=LEAN_ROOT))
    if sha256(lean) != LEAN_SHA256 or sha256(lake) != LAKE_SHA256:
        raise ValueError("pinned Lean or Lake executable digest mismatch")
    if LEAN_COMMIT not in checked_output([str(lean), "--version"], cwd=LEAN_ROOT):
        raise ValueError("pinned Lean executable identity mismatch")
    base_path = checked_output(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT)
    fixed_env = {
        **os.environ,
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "LEAN_PATH": base_path,
    }
    with tempfile.TemporaryDirectory(prefix="m0424-proof-", dir="/tmp") as raw:
        scratch = Path(raw)
        statement = scratch / "Statement.lean"
        counterexample = scratch / "Counterexample.lean"
        statement.write_bytes((HERE / "Statement.lean").read_bytes())
        counterexample.write_bytes(
            (HERE / "UniverseCounterexample-2026-07-14-head-5753c6ed.lean").read_bytes()
        )
        statement_output = run(
            [str(lean), "--trust=0", "--root", str(scratch), "-o",
             str(scratch / "Statement.olean"), str(statement)],
            cwd=LEAN_ROOT,
            env=fixed_env,
        )
        if statement_output.returncode:
            raise ValueError(f"statement replay failed\n{statement_output.stdout}")
        local_env = {**fixed_env, "LEAN_PATH": f"{scratch}:{base_path}"}
        counter_output = run(
            [str(lean), "--trust=0", "--root", str(scratch), "-o",
             str(scratch / "Counterexample.olean"), str(counterexample)],
            cwd=LEAN_ROOT,
            env=local_env,
        )
        if counter_output.returncode:
            raise ValueError(f"counterexample replay failed\n{counter_output.stdout}")
        if hashlib.sha256(statement_output.stdout.encode()).hexdigest() != (
            "efa2ea0ea05ce852276dd67e3abe1c6f3c705670f8c435bebcf57be1456b4e51"
        ):
            raise ValueError("statement replay output drifted")
        if hashlib.sha256(counter_output.stdout.encode()).hexdigest() != (
            "c309037999d6b2be51e46f3e5a1e3ce8f67255764f213671c71f0df4696e8dcb"
        ):
            raise ValueError("counterexample replay output drifted")
        if sha256(scratch / "Statement.olean") != (
            "3cf07b674053f73ba89b4b05c86e12c87cece6b588f3ee71ff389db747a1c2c2"
        ):
            raise ValueError("statement compiled object drifted")
        for declaration in (
            "Stage1Instances.THM_M_0424.UniverseCounterexample.small_of_one_rep_equiv",
            "Stage1Instances.THM_M_0424.UniverseCounterexample.no_small_base_representative",
            "Stage1Instances.THM_M_0424.UniverseCounterexample.no_law_data_at_unrelated_universes",
            "Stage1Instances.THM_M_0424.UniverseCounterexample.not_brauerGroupStatement",
        ):
            if printed_axioms(counter_output.stdout, declaration) != EXPECTED_AXIOMS:
                raise ValueError(f"unexpected axiom profile for {declaration}")
        if "this : ¬BrauerGroupStatement" not in counter_output.stdout:
            raise ValueError("counterexample did not recheck the negated exact target")


def verify() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION or git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("worker base revision or tree drifted")
    if sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") != GRAPH_SHA256:
        raise ValueError("theorem DAG digest drifted")
    if sha256(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") != CONTRACT_SHA256:
        raise ValueError("phase contract digest drifted")
    if sha256(LEAN_ROOT / "lean-toolchain") != TOOLCHAIN_SHA256:
        raise ValueError("Lean toolchain file drifted")
    if sha256(LEAN_ROOT / "lake-manifest.json") != MANIFEST_SHA256:
        raise ValueError("Lake manifest drifted")
    for name, expected in EXPECTED_HASHES.items():
        if sha256(HERE / name) != expected:
            raise ValueError(f"owned frozen input drifted: {name}")

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row.get("theorem_id") == THEOREM)
    if target.get("execution_rank") != 78 or target.get("lifecycle_mode") != "planned":
        raise ValueError("target manifest identity or lifecycle drifted")
    if target.get("theorem_complete") is not False:
        raise ValueError("target manifest unexpectedly claims theorem completion")

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    phase_items = {
        row["phase"]: row for row in execution["items"]
        if row.get("theorem_id") == THEOREM
    }
    if set(phase_items) != PHASES:
        raise ValueError("target does not have the exact seven phase items")
    if phase_items["proof"].get("state") != "[ ]" or phase_items["proof"].get("attempts") != 0:
        raise ValueError("proof item no longer matches the claimed open state")
    if phase_items["proof"].get("depends_on") != ["S56-M-0424-OBLIGATION_TREE"]:
        raise ValueError("proof prerequisite identity changed")
    if phase_items["obligation_tree"].get("state") != "[_]":
        raise ValueError("proof prerequisite observation changed")

    theorem_dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM)
    if node.get("v2_execution_rank") != 304 or node.get("topological_layer") != 0:
        raise ValueError("v2 claim order changed")
    for field in ("direct_hard_parents", "transitive_hard_ancestors", "direct_reuse_hint_ids"):
        if node.get(field) != []:
            raise ValueError(f"unexpected dependency context in {field}")
    if node.get("shared_lemma_group_ids") != SHARED_GROUPS:
        raise ValueError("shared-group context changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        raise ValueError("dependency context digest changed")
    validate_ledger()

    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    proof_contracts = [
        row for row in contract.get("phases", [])
        if isinstance(row, dict) and row.get("phase") == "proof"
    ]
    if len(proof_contracts) != 1:
        raise ValueError("HEAD phase contract lacks exactly one proof row")
    proof_contract = proof_contracts[0]
    if proof_contract.get("intent") != "prove" or proof_contract.get("layer") != 4:
        raise ValueError("proof phase contract intent or layer changed")
    roles = {
        row.get("role"): row
        for row in proof_contract.get("required_artifact_roles", [])
        if isinstance(row, dict)
    }
    if set(roles) != {
        "dependency_reuse_ledger", "proof_sources", "provider_material",
        "phase_receipt",
    }:
        raise ValueError("proof phase artifact roles changed")
    candidates = proof_contract.get("validator_candidates")
    if [row.get("path_pattern") for row in candidates] != [
        "Stage1_Instances/{theorem_id}/check_proof.py",
        "Stage1_Instances/{theorem_id}/check_proof.sh",
    ]:
        raise ValueError("proof validator candidate contract changed")
    existing_candidates = [
        pattern.format(theorem_id=THEOREM)
        for pattern in (row["path_pattern"] for row in candidates)
        if (ROOT / pattern.format(theorem_id=THEOREM)).is_file()
    ]
    if existing_candidates != ["Stage1_Instances/THM-M-0424/check_proof.py"]:
        raise ValueError("proof validator candidate selection is not exact")

    receipt = load(HERE / "proof-receipt.json")
    required_receipt_fields = {
        "schema_version", "receipt_id", "item_id", "theorem_id", "phase",
        "intent", "base_revision", "base_tree", "inputs", "support_state",
        "proposed_state", "accepted", "verdict", "selftest_status",
        "selftest_result", "known_failures", "first_failed_gate",
        "retry_condition", "status_boundary", "audit_complete",
        "theorem_complete", "invalidation_inputs", "canonical_target",
        "exact_declarations", "closed_obligation_ids", "proof_body", "result",
    }
    if not required_receipt_fields <= set(receipt):
        raise ValueError("proof receipt lacks a contract-required field")
    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        raise ValueError("proof receipt schema mismatch")
    if receipt.get("item_id") != ITEM or receipt.get("theorem_id") != THEOREM:
        raise ValueError("proof receipt identity mismatch")
    if receipt.get("phase") != "proof" or receipt.get("intent") != "prove":
        raise ValueError("proof receipt phase or intent mismatch")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        raise ValueError("proof receipt base binding mismatch")
    if receipt.get("support_state") != "provisional_worker_selftest":
        raise ValueError("proof receipt support state mismatch")
    if receipt.get("proposed_state") != "[_]" or receipt.get("accepted") is not False:
        raise ValueError("proof receipt improperly claims master acceptance")
    if receipt.get("verdict") != "blocked" or receipt.get("selftest_status") != "passed":
        raise ValueError("proof receipt does not preserve the self-tested blocked verdict")
    if receipt.get("selftest_result", {}).get("exit_code") != 0:
        raise ValueError("proof receipt self-test exit is not successful")
    if not receipt.get("selftest_result", {}).get("commands"):
        raise ValueError("proof receipt lacks exact self-test commands")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }:
        raise ValueError("worker self-test packet schema mismatch")
    if packet.get("item_id") != ITEM or packet.get("state") != "[_]":
        raise ValueError("worker self-test packet identity or state mismatch")
    if packet.get("base_revision") != BASE_REVISION:
        raise ValueError("worker self-test packet base mismatch")
    if packet.get("commands") != receipt.get("selftest_result", {}).get("commands"):
        raise ValueError("worker packet and receipt command evidence disagree")
    if packet.get("known_failures") != receipt.get("known_failures"):
        raise ValueError("worker packet and receipt known failures disagree")
    expected_changed = {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0424/check_proof.py",
        "Stage1_Instances/THM-M-0424/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0424/proof-receipt.json",
        "Stage1_Instances/THM-M-0424/proof-validation.md",
    }
    if set(packet.get("changed_paths", [])) != expected_changed:
        raise ValueError("worker self-test packet changed-path scope mismatch")
    status = checked_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        preserve_whitespace=True,
    )
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    if actual_changed != expected_changed:
        raise ValueError("worktree delta escapes or omits the declared target scope")
    if receipt.get("canonical_target") != (
        "Stage1Instances.THM_M_0424.BrauerGroupStatement"
    ):
        raise ValueError("proof receipt canonical target mismatch")
    if receipt.get("exact_declarations") != [
        "Stage1Instances.THM_M_0424.UniverseCounterexample.not_brauerGroupStatement"
    ]:
        raise ValueError("proof receipt exact declaration boundary mismatch")
    if receipt.get("closed_obligation_ids") != []:
        raise ValueError("proof receipt improperly closes a frozen obligation")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        raise ValueError("proof receipt overstates a terminal decision")
    if receipt.get("result") != {
        "exit_code": 0,
        "semantic_verdict": "blocked",
        "phase_predicate_proven": False,
        "phase_accepted": False,
        "blocked": True,
        "audit_complete": False,
        "theorem_complete": False,
        "root_closed": False,
        "open_obligations": len(OPEN_IDS),
    }:
        raise ValueError("proof receipt semantic result mismatch")
    proof_sources = receipt.get("inputs", {}).get("proof_sources")
    if not isinstance(proof_sources, list) or len(proof_sources) != 1:
        raise ValueError("proof receipt must bind exactly one negative proof source")
    source_binding = proof_sources[0]
    if source_binding.get("path") != (
        "Stage1_Instances/THM-M-0424/UniverseCounterexample-2026-07-14-head-5753c6ed.lean"
    ):
        raise ValueError("proof receipt source path mismatch")
    if source_binding.get("sha256") != EXPECTED_HASHES[
        "UniverseCounterexample-2026-07-14-head-5753c6ed.lean"
    ] or source_binding.get("git_blob") != "1624ed83e6215131c57f4f9ba35dd8766679eaa1":
        raise ValueError("proof receipt source byte binding mismatch")
    input_bindings = receipt.get("input_bindings")
    if not isinstance(input_bindings, dict):
        raise ValueError("proof receipt lacks complete input bindings")
    for name, expected in PROOF_RECEIPT_INPUT_HASHES.items():
        binding = input_bindings.get(name)
        path = HERE / name
        if not isinstance(binding, dict) or binding.get("sha256") != expected:
            raise ValueError(f"proof receipt input binding mismatch: {name}")
        if binding.get("git_blob") != git("hash-object", str(path)):
            raise ValueError(f"proof receipt Git blob binding mismatch: {name}")
    validator_binding = input_bindings.get("check_proof.py")
    validator_path = HERE / "check_proof.py"
    if not isinstance(validator_binding, dict):
        raise ValueError("proof receipt lacks the proof validator binding")
    if validator_binding.get("sha256") != sha256(validator_path):
        raise ValueError("proof receipt validator SHA-256 binding mismatch")
    if validator_binding.get("git_blob") != git("hash-object", str(validator_path)):
        raise ValueError("proof receipt validator Git blob binding mismatch")

    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    rows = registry.get("obligations")
    if not isinstance(rows, list) or {row.get("obligation_id") for row in rows} != OPEN_IDS:
        raise ValueError("frozen obligation denominator identity changed")
    if registry.get("root_obligation_id") != "M0424-ROOT":
        raise ValueError("frozen root identity changed")
    if registry.get("denominator_sha256") != DENOMINATOR_SHA256:
        raise ValueError("frozen obligation denominator digest changed")
    if any(row.get("body") is not None for row in rows):
        raise ValueError("registry unexpectedly records a terminal proof body")
    closure = graphs.get("closure_boundary")
    if not isinstance(closure, dict) or closure.get("root_closed") is not False:
        raise ValueError("typed graph unexpectedly closes the root")
    if closure.get("distinct_terminal_proof_bodies") != []:
        raise ValueError("typed graph unexpectedly credits a terminal proof body")

    for name in (
        "Statement.lean", "ObligationTree.lean",
        "UniverseCounterexample-2026-07-14-head-5753c6ed.lean",
    ):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        if PROHIBITED.search(source):
            raise ValueError(f"prohibited proof construct found in {name}")

    if git("rev-parse", "HEAD", cwd=MATHLIB) != MATHLIB_REVISION:
        raise ValueError("mathlib revision drifted")
    if git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) != MATHLIB_TREE:
        raise ValueError("mathlib tree drifted")
    if git("status", "--porcelain=v1", cwd=MATHLIB) != "":
        raise ValueError("mathlib checkout is dirty")
    flr = LEAN_ROOT / ".lake" / "packages" / "flt-regular"
    if git("rev-parse", "HEAD", cwd=flr) != FLR_REVISION:
        raise ValueError("flt-regular revision drifted")
    if git("rev-parse", "HEAD^{tree}", cwd=flr) != FLR_TREE:
        raise ValueError("flt-regular tree drifted")
    if git("status", "--porcelain=v1", cwd=flr) != "":
        raise ValueError("flt-regular checkout is dirty")
    defs = (MATHLIB / "Mathlib/Algebra/BrauerGroup/Defs.lean").read_text(encoding="utf-8")
    if "Prove that the Brauer group is an abelian group" not in defs:
        raise ValueError("pinned Brauer-group implementation boundary changed")
    replay_counterexample()


def semantic_result(*, verified: bool, error: str | None = None) -> dict[str, Any]:
    message = (
        "The frozen target is refuted by the checked {1,0} universe specialization; "
        "zero frozen obligations are closed and the proof phase remains blocked."
        if verified else f"Proof blocker replay failed: {error}"
    )
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "proof",
        "status": "blocked" if verified else "failed",
        "verdict": "blocked" if verified else "repair_required",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": (
            "P04-KERNEL/S56-5.1-EXACT-TARGET-CONSISTENCY/M0424-S-BOUNDARY"
            if verified else "P01-ARTIFACTS"
        ),
        "open_obligations": len(OPEN_IDS),
        "stale_inputs": [],
        "blocked": verified,
        "message": message,
    }


def main() -> int:
    try:
        verify()
    except Exception as exc:
        result = semantic_result(verified=False, error=str(exc))
        code = 1
    else:
        result = semantic_result(verified=True)
        code = 0
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
