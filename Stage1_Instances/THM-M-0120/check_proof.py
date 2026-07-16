#!/usr/bin/env python3
"""Fail-closed semantic proof validator for S56-M-0120-PROOF."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0120"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-0120-PROOF"
THEOREM = "THM-M-0120"
BASE_REVISION = "307c34d30fc3763c82a944a142ae922b48ff18aa"
BASE_TREE = "ef45ba442c71959db78ad146a023bcf32946a53f"
GRAPH_SHA256 = "8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
BLUEPRINT_SHA256 = "2a5bc7d397e03969aac1a9f8f21b437152b8ef63ef453055acf67857ced628b5"
ASSURANCE_SHA256 = "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8"
TARGETS_SHA256 = "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
EXECUTION_DAG_SHA256 = "fe70128eba4e3878fbc58625bc7f602be4020e5e2edd6b94b134436568086d65"
SKILL_SHA256 = "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454"

TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"

STATEMENT_EXPRESSION_SHA256 = "074d45c3dfbf6dd24905ebee7f18835fd37ba1fc7acae6a1f41ec5c6f2d88cfd"
DENOMINATOR_SHA256 = "69152b161a10b5ce6099fb09c48320330d6d35f63a11411ad14ccb84963081b1"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

EXPECTED_HASHES = {
    "Statement.lean": "69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b",
    "ObligationTree.lean": "21d9aca576307bdcf2f2fe8d5e06c3a56008b44b9534391d3bbb8926e1693035",
    "Proof.lean": "e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab",
    "obligation-registry.json": "cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d",
    "typed-graphs.json": "9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f",
    "anchor-audit.json": "71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d",
    "validation-specs.json": "69323c530f4a15676cb6c791df8cf8769d5d01820578bef2bcbb737413d07771",
    "statement.json": "a5f28a9cfdf8797940fc41f9411183ee373b53c6a26c57866825ea1619c78777",
    "instance.json": "d8648f6d44a701c3dd540e1256e2b3442ccc1da837f81aedcf89d824ef4ce2ae",
    "dependency-reuse-ledger.json": "0a04bc44bda77cd5036f6e626faa75b7d462ae307f8e191662e2ef2860714928",
}

OPEN_IDS = {
    "M0120-ROOT", "M0120-T", "M0120-S", "M0120-S-DATA",
    "M0120-S-DEFS", "M0120-S-BOUNDARY", "M0120-S-TRANSPORT",
    "M0120-X", "M0120-X-KLT", "M0120-X-N1", "M0120-X-INT",
    "M0120-D", "M0120-D-RAYS", "M0120-D-NEG", "M0120-D-RAT",
    "M0120-D-SUM", "M0120-F", "M0120-F-COMPACT", "M0120-C",
    "M0120-C-EXIST", "M0120-C-CURVES", "M0120-C-UNIV",
    "M0120-P", "M0120-V", "M0120-R",
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
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
    if not isinstance(value, dict):
        raise ValueError(f"expected one JSON object in {path}")
    return value


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 240,
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


def validate_authorities() -> None:
    authority_hashes = {
        "Docs/Stage1_Blueprint_v2.md": BLUEPRINT_SHA256,
        "Docs/Stage1_Blueprint_rev-5.6.md": ASSURANCE_SHA256,
        "Docs/Stage1_Targets_rev-5.6.json": TARGETS_SHA256,
        "Docs/Stage1_Execution_DAG_rev-5.6.json": EXECUTION_DAG_SHA256,
        "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
        "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
        "skills/execute-stage1-rev56/SKILL.md": SKILL_SHA256,
    }
    for relative, expected in authority_hashes.items():
        if sha256(ROOT / relative) != expected:
            raise ValueError(f"authority drifted: {relative}")

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row.get("theorem_id") == THEOREM)
    if target.get("execution_rank") != 39 or target.get("lifecycle_mode") != "planned":
        raise ValueError("target manifest identity or lifecycle drifted")
    if target.get("baseline") != "L0" or target.get("rework_required") is not True:
        raise ValueError("target assurance baseline drifted")
    if target.get("theorem_complete") is not False:
        raise ValueError("target manifest unexpectedly claims theorem completion")

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    phase_items = {
        row["phase"]: row for row in execution["items"]
        if row.get("theorem_id") == THEOREM
    }
    if set(phase_items) != {
        "intake", "statement", "anchor_audit", "obligation_tree",
        "proof", "validation", "release",
    }:
        raise ValueError("target no longer has exactly seven phase items")
    proof_item = phase_items["proof"]
    if proof_item.get("id") != ITEM or proof_item.get("state") != "[ ]":
        raise ValueError("proof task-state authority no longer matches the claim")
    if proof_item.get("attempts") != 0 or proof_item.get("children") != []:
        raise ValueError("proof attempt or child state changed")
    if proof_item.get("depends_on") != ["S56-M-0120-OBLIGATION_TREE"]:
        raise ValueError("proof predecessor identity changed")
    if phase_items["obligation_tree"].get("state") != "[_]":
        raise ValueError("proof predecessor observation changed")

    theorem_dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM)
    if node.get("v2_execution_rank") != 273 or node.get("topological_layer") != 0:
        raise ValueError("v2 claim order changed")
    for field in (
        "direct_hard_parents", "transitive_hard_ancestors",
        "direct_reuse_hint_ids", "shared_lemma_group_ids",
    ):
        if node.get(field) != []:
            raise ValueError(f"unexpected dependency context in {field}")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        raise ValueError("dependency context digest drifted")

    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    rows = [row for row in contract["phases"] if row.get("phase") == "proof"]
    if len(rows) != 1:
        raise ValueError("phase contract does not contain exactly one proof contract")
    phase = rows[0]
    if phase.get("layer") != 4 or phase.get("intent") != "prove":
        raise ValueError("proof contract claim order or intent changed")
    if phase.get("raw_blocked_can_close_phase") is not False:
        raise ValueError("proof contract negative-result boundary changed")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        raise ValueError("proof contract negative finding policy changed")
    if [gate.get("gate_id") for gate in phase.get("semantic_gates", [])] != [
        "P01-ARTIFACTS", "P02-CONTEXT", "P03-REUSE", "P04-KERNEL",
        "P05-HYGIENE", "P06-COMPOSITION",
    ]:
        raise ValueError("proof semantic gate set changed")
    candidates = phase.get("validator_candidates", [])
    if [row.get("path_pattern") for row in candidates] != [
        "Stage1_Instances/{theorem_id}/check_proof.py",
        "Stage1_Instances/{theorem_id}/check_proof.sh",
    ]:
        raise ValueError("proof validator candidates changed")
    existing = [
        pattern.format(theorem_id=THEOREM)
        for pattern in (row["path_pattern"] for row in candidates)
        if (ROOT / pattern.format(theorem_id=THEOREM)).is_file()
    ]
    if existing != ["Stage1_Instances/THM-M-0120/check_proof.py"]:
        raise ValueError("proof validator candidate selection is ambiguous")


def validate_ledger() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    if ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1":
        raise ValueError("dependency ledger schema mismatch")
    if ledger.get("consumer_theorem_id") != THEOREM:
        raise ValueError("dependency ledger owner mismatch")
    if ledger.get("observed_theorem_dag_sha256") != GRAPH_SHA256:
        raise ValueError("dependency ledger graph binding is stale")
    if ledger.get("dependency_context_sha256") != CONTEXT_SHA256:
        raise ValueError("dependency ledger context binding is stale")
    if ledger.get("repository_revision") != BASE_REVISION:
        raise ValueError("dependency ledger repository binding is stale")
    for key in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "inspections", "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        if ledger.get(key) != []:
            raise ValueError(f"dependency ledger field {key} is not the exact empty context")
    if ledger.get("claim_order") != {
        "v2_execution_rank": 273,
        "phase_layer": 4,
        "phase_item_id": ITEM,
    }:
        raise ValueError("dependency ledger claim order is stale")
    audit = ledger.get("closure_audit")
    if not isinstance(audit, dict):
        raise ValueError("dependency ledger lacks a closure audit")
    if audit.get("parent_inspection_order") != [] or audit.get("inspected_parent_ids") != []:
        raise ValueError("dependency ledger invents or omits a parent inspection")
    if audit.get("inspection_count") != 0:
        raise ValueError("dependency ledger empty inspection count is wrong")
    if audit.get("status") != "empty_declared_context_inspected":
        raise ValueError("dependency ledger does not affirm the empty closure audit")


def validate_receipt_and_packet() -> None:
    receipt = load(HERE / "proof-receipt.json")
    required = {
        "schema_version", "receipt_id", "item_id", "theorem_id", "phase",
        "intent", "base_revision", "base_tree", "inputs", "support_state",
        "proposed_state", "accepted", "verdict", "selftest_status",
        "selftest_result", "known_failures", "first_failed_gate",
        "retry_condition", "status_boundary", "audit_complete",
        "theorem_complete", "invalidation_inputs", "canonical_target",
        "exact_declarations", "closed_obligation_ids", "proof_body", "result",
    }
    if not required <= set(receipt):
        raise ValueError("proof receipt lacks a contract-required field")
    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        raise ValueError("proof receipt schema mismatch")
    if receipt.get("item_id") != ITEM or receipt.get("theorem_id") != THEOREM:
        raise ValueError("proof receipt identity mismatch")
    if receipt.get("phase") != "proof" or receipt.get("intent") != "prove":
        raise ValueError("proof receipt phase or intent mismatch")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        raise ValueError("proof receipt base binding mismatch")
    if receipt.get("support_state") != "provisional_worker_selftest_blocked":
        raise ValueError("proof receipt support-state boundary mismatch")
    if receipt.get("proposed_state") != "[_]" or receipt.get("accepted") is not False:
        raise ValueError("proof receipt improperly claims master acceptance")
    if receipt.get("verdict") != "blocked" or receipt.get("selftest_status") != "passed":
        raise ValueError("proof receipt does not preserve the self-tested blocker verdict")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        raise ValueError("proof receipt overstates a terminal decision")
    if receipt.get("canonical_target") != "Stage1Instances.THMM0120.MoriConeTheoremTarget":
        raise ValueError("proof receipt canonical target mismatch")
    if receipt.get("exact_declarations") != [
        "Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget"
    ]:
        raise ValueError("proof receipt declaration boundary mismatch")
    if receipt.get("closed_obligation_ids") != []:
        raise ValueError("proof receipt improperly closes an obligation")
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
    proof_body = receipt.get("proof_body")
    if not isinstance(proof_body, dict):
        raise ValueError("proof receipt lacks a proof-body boundary")
    if proof_body.get("positive_root_body") is not False:
        raise ValueError("proof receipt improperly claims a positive root body")
    if proof_body.get("terminal_proof_body_id") is not None:
        raise ValueError("proof receipt credits a terminal proof body")

    proof_sources = receipt.get("inputs", {}).get("proof_sources")
    if not isinstance(proof_sources, list) or len(proof_sources) != 1:
        raise ValueError("proof receipt must bind exactly one negative proof source")
    source = proof_sources[0]
    if source.get("path") != "Stage1_Instances/THM-M-0120/Proof.lean":
        raise ValueError("proof source path mismatch")
    if source.get("sha256") != EXPECTED_HASHES["Proof.lean"]:
        raise ValueError("proof source SHA-256 mismatch")
    if source.get("git_blob") != git("hash-object", str(HERE / "Proof.lean")):
        raise ValueError("proof source Git blob mismatch")
    if receipt.get("inputs", {}).get("provider_material") != []:
        raise ValueError("receipt invents provider material")
    context = receipt.get("dependency_context")
    if not isinstance(context, dict):
        raise ValueError("receipt lacks dependency context")
    for key in (
        "parent_inspection_order", "inspected_parent_ids", "direct_parent_ids",
        "transitive_ancestor_ids", "hard_edge_ids", "reuse_hint_ids",
        "shared_group_ids", "reused_declaration_ids",
    ):
        if context.get(key) != []:
            raise ValueError(f"receipt dependency field {key} is not empty")
    if context.get("provider_acceptance_inherited") is not False:
        raise ValueError("receipt inherits provider acceptance")

    bindings = receipt.get("input_bindings")
    if not isinstance(bindings, dict):
        raise ValueError("proof receipt lacks complete input bindings")
    for name, expected in EXPECTED_HASHES.items():
        binding = bindings.get(name)
        path = HERE / name
        if not isinstance(binding, dict) or binding.get("sha256") != expected:
            raise ValueError(f"proof receipt SHA-256 binding mismatch: {name}")
        if binding.get("git_blob") != git("hash-object", str(path)):
            raise ValueError(f"proof receipt Git blob binding mismatch: {name}")
    validator = bindings.get("check_proof.py")
    validator_path = HERE / "check_proof.py"
    if not isinstance(validator, dict):
        raise ValueError("receipt lacks validator binding")
    if validator.get("sha256") != sha256(validator_path):
        raise ValueError("receipt validator SHA-256 binding mismatch")
    if validator.get("git_blob") != git("hash-object", str(validator_path)):
        raise ValueError("receipt validator Git blob binding mismatch")

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
        raise ValueError("worker packet and proof receipt commands disagree")
    if packet.get("known_failures") != receipt.get("known_failures"):
        raise ValueError("worker packet and proof receipt failures disagree")
    expected_changed = {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0120/check_proof.py",
        "Stage1_Instances/THM-M-0120/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0120/proof-receipt.json",
        "Stage1_Instances/THM-M-0120/proof-validation.md",
    }
    if set(packet.get("changed_paths", [])) != expected_changed:
        raise ValueError("worker packet changed-path scope mismatch")
    status = checked_output(
        ["git", "status", "--short", "--untracked-files=all"],
        preserve_whitespace=True,
    )
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    if actual_changed != expected_changed:
        raise ValueError("worktree delta escapes or omits the declared target scope")


def validate_frozen_architecture() -> None:
    for name, expected in EXPECTED_HASHES.items():
        if sha256(HERE / name) != expected:
            raise ValueError(f"owned frozen input drifted: {name}")

    statement = load(HERE / "statement.json")
    formal = statement.get("canonical_formal_target", {})
    if formal.get("declaration_or_expression") != (
        "Stage1Instances.THMM0120.MoriConeTheoremTarget"
    ):
        raise ValueError("frozen statement declaration changed")
    if formal.get("elaborated_expression_sha256") != STATEMENT_EXPRESSION_SHA256:
        raise ValueError("frozen statement expression changed")
    if statement.get("theorem_proved") is not False or statement.get("theorem_complete") is not False:
        raise ValueError("statement record unexpectedly claims closure")

    registry = load(HERE / "obligation-registry.json")
    rows = registry.get("obligations")
    if not isinstance(rows, list) or {row.get("obligation_id") for row in rows} != OPEN_IDS:
        raise ValueError("frozen obligation denominator identity changed")
    if registry.get("root_obligation_id") != "M0120-ROOT":
        raise ValueError("frozen root identity changed")
    if registry.get("denominator_sha256") != DENOMINATOR_SHA256:
        raise ValueError("frozen obligation denominator digest changed")
    if any(row.get("terminal_proof_body_id") is not None for row in rows):
        raise ValueError("registry unexpectedly credits a terminal proof body")

    graphs = load(HERE / "typed-graphs.json")
    closure = graphs.get("closure_boundary")
    if not isinstance(closure, dict) or closure.get("root_closed") is not False:
        raise ValueError("typed graph unexpectedly closes the root")
    if closure.get("closed_obligations") != [] or closure.get("theorem_complete") is not False:
        raise ValueError("typed graph unexpectedly credits theorem closure")

    audit = load(HERE / "anchor-audit.json")
    decision = audit.get("root_decision")
    if not isinstance(decision, dict) or decision.get("kernel_closed") is not False:
        raise ValueError("anchor audit unexpectedly reports kernel closure")
    if decision.get("exact_external_candidate_found") is not False:
        raise ValueError("anchor audit unexpectedly reports an external proof")

    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        if PROHIBITED.search(source):
            raise ValueError(f"prohibited proof construct found in {name}")


def replay_countermodel() -> None:
    if sha256(LEAN_ROOT / "lean-toolchain") != TOOLCHAIN_SHA256:
        raise ValueError("Lean toolchain file drifted")
    if sha256(LEAN_ROOT / "lake-manifest.json") != MANIFEST_SHA256:
        raise ValueError("Lake manifest drifted")
    lean = Path(checked_output(["lake", "env", "which", "lean"], cwd=LEAN_ROOT))
    lake = Path(checked_output(["lake", "env", "which", "lake"], cwd=LEAN_ROOT))
    if sha256(lean) != LEAN_SHA256 or sha256(lake) != LAKE_SHA256:
        raise ValueError("pinned Lean or Lake executable digest mismatch")
    if LEAN_COMMIT not in checked_output([str(lean), "--version"], cwd=LEAN_ROOT):
        raise ValueError("pinned Lean executable identity mismatch")
    if git("rev-parse", "HEAD", cwd=MATHLIB) != MATHLIB_REVISION:
        raise ValueError("mathlib revision drifted")
    if git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) != MATHLIB_TREE:
        raise ValueError("mathlib tree drifted")
    if git("status", "--porcelain=v1", cwd=MATHLIB) != "":
        raise ValueError("mathlib checkout is dirty")

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
    with tempfile.TemporaryDirectory(prefix="m0120-proof-", dir="/tmp") as raw:
        scratch = Path(raw)
        statement = scratch / "Statement.lean"
        proof = scratch / "Proof.lean"
        statement.write_bytes((HERE / "Statement.lean").read_bytes())
        proof.write_bytes((HERE / "Proof.lean").read_bytes())
        statement_result = run(
            [str(lean), "--trust=0", "--root", str(scratch), "-o",
             str(scratch / "Statement.olean"), str(statement)],
            cwd=LEAN_ROOT,
            env=fixed_env,
        )
        if statement_result.returncode:
            raise ValueError(f"statement replay failed\n{statement_result.stdout}")
        proof_result = run(
            [str(lean), "--trust=0", "--root", str(scratch), "-o",
             str(scratch / "Proof.olean"), str(proof)],
            cwd=LEAN_ROOT,
            env={**fixed_env, "LEAN_PATH": f"{scratch}:{base_path}"},
        )
        if proof_result.returncode:
            raise ValueError(f"countermodel replay failed\n{proof_result.stdout}")
        if hashlib.sha256(statement_result.stdout.encode()).hexdigest() != (
            "227b41b022b670d99a326070af16b3007dbf438d19f8e7d4745d7afc57370ab4"
        ):
            raise ValueError("statement replay output drifted")
        if hashlib.sha256(proof_result.stdout.encode()).hexdigest() != (
            "3898551895c04d36d276ee78335df8d097d382c9f85862d62a5b4224334412f0"
        ):
            raise ValueError("countermodel replay output drifted")
        if sha256(scratch / "Statement.olean") != (
            "f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16"
        ):
            raise ValueError("statement compiled object drifted")
        if sha256(scratch / "Proof.olean") != (
            "cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec"
        ):
            raise ValueError("countermodel compiled object drifted")
        declaration = "Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget"
        if printed_axioms(proof_result.stdout, declaration) != EXPECTED_AXIOMS:
            raise ValueError("countermodel axiom profile changed")


def verify() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION or git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("worker base revision or tree drifted")
    validate_authorities()
    validate_ledger()
    validate_frozen_architecture()
    replay_countermodel()
    validate_receipt_and_packet()


def semantic_result(*, verified: bool, error: str | None = None) -> dict[str, Any]:
    message = (
        "The trust-zero countermodel refutes the frozen {0,0,0,0} target; "
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
            "P04-KERNEL/S56-5.1-EXACT-TARGET-CONSISTENCY/M0120-S-DATA/M0120-S-BOUNDARY"
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
