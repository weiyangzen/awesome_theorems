#!/usr/bin/env python3
"""Fail-closed semantic proof validator for S56-M-0554-PROOF."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0554"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0554-PROOF"
THEOREM = "THM-M-0554"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "2428583503c74afdba4210f063f54b4e98de9ac49461a634998fcc207662fb7b"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
DENOMINATOR_SHA256 = "3c72072a40a15d829c40df68b5fc121b74662a883799f7f7c277fa9c6ed8048b"
SHARED_GROUP = "SHARED-MODULE-50020b08cd4a5348"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_HASHES = {
    "Statement.lean": "8bd29893b87ad6991854c311ef1e80cab11f1fc0d6b63ab82e3bfeb1c5f89970",
    "Proof.lean": "d6f81c9852bdfc3ea1b416e674d80a322e48999852f79ec75f7817526f4cae1b",
    "obligation-registry.json": "b2087cf8eec22b4c63798aae57c8e8226038c1c45f596b1c4e728d1f465876e4",
    "typed-graphs.json": "c0682d4dc07391b140677635dd74c97e235f8bcefdbd71cf5ce45f87e706a013",
    "anchor-audit.json": "e53684e74b63c14e6fa105ab718e07e20a11ebe27378c937dcd02927bcc35cf6",
    "validation-specs.json": "362642d87cb4736b9180a71f1a5cc287fe6ac1c5570048e8beee6e48739f7467",
    "check_obligation_tree.py": "9c7725b6d8b7bdb642fb56df83a4bbbe8a4c77c245bfd271c330845d268f900a",
    "dependency-reuse-ledger.json": "81d33515532b45488c01d64ab0c1e9bb118da4f9370c776d32f27952e9bd6718",
}
EXPECTED_BLOBS = {
    "Statement.lean": "0c892d98e899a9e5b28864e7ece587c136f3420c",
    "Proof.lean": "17a879007f58baf459df5460fcdffe4803ecf88c",
    "obligation-registry.json": "fbf472638578ca982e495b2a860abbe38da89f52",
    "typed-graphs.json": "9c3fc7bcdc5341c321f64ab42a45ea00d03b7709",
    "anchor-audit.json": "7d52a8181232b239b0eb97d0fd349ea7cd5015af",
    "validation-specs.json": "62c7d324d12571399c6209af3dc92d534d2b2c27",
    "check_obligation_tree.py": "e3820e5be39396a7235717a98e07e3c10a5090b0",
    "dependency-reuse-ledger.json": "95239a257fa7fc666fb631c57b8b5534ae162caf",
}
SHARED_ARTIFACTS = {
    "Stage1_Instances/THM-M-0540/anchor-audit.json":
        "a96b1c0ff9588dec6d4de558a813f5370bf7f9d74abdadca013c089f2444c556",
    "Stage1_Instances/THM-M-0540/AnchorAudit.lean":
        "14a540e83633216eb7beb38a85aeb1a2bb1dcd141c1f40a2842fe5305ab217d9",
}
DECLARATIONS = [
    "Stage1.THM_M_0554.Proof.dataOfBranches",
    "Stage1.THM_M_0554.Proof.statementShapeOfBranches",
    "Stage1.THM_M_0554.Proof.statementOfBranchFamily",
]
PROVISIONAL_IDS = [
    "M0554-B-RECOMPOSE", "M0554-T-DATA", "M0554-T-INHABIT", "M0554-T-ROOT",
]
OPEN_IDS = {
    "M0554-ROOT", "M0554-S-EXACT", "M0554-S-THEORY", "M0554-S-CW",
    "M0554-S-DATA", "M0554-S-FOUNDATION", "M0554-N-SKELETON",
    "M0554-N-BIGRADE", "M0554-N-COEFFICIENT", "M0554-B-E2",
    "M0554-B-DIFFERENTIAL", "M0554-B-CONVERGENCE", "M0554-B-NATURALITY",
    "M0554-B-RECOMPOSE", "M0554-C-EXACT-COUPLE", "M0554-C-SPECTRAL",
    "M0554-C-E2-MODEL", "M0554-C-FILTRATION", "M0554-L-CELLULAR",
    "M0554-L-STABILIZATION", "M0554-L-STRONG", "M0554-X-SPECTRAL",
    "M0554-X-CW", "M0554-X-GENCOH", "M0554-X-GENCOH-PAIR",
    "M0554-X-GENCOH-EXCISION", "M0554-X-GENCOH-WEDGE", "M0554-X-SOURCE",
    "M0554-X-TCB", "M0554-T-DATA", "M0554-T-INHABIT", "M0554-T-ROOT",
}
PHASES = {
    "intake", "statement", "anchor_audit", "obligation_tree", "proof",
    "validation", "release",
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
    timeout: int = 300,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )


def checked_output(argv: list[str], *, cwd: Path = ROOT) -> str:
    result = run(argv, cwd=cwd)
    if result.returncode:
        raise ValueError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout.strip()


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
        item.strip() for item in match.group(1).replace("\n", "").split(",")
        if item.strip()
    }


def validate_ledger() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    expected_empty = {
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "inspections", "unresolved_compatibility_obligations",
    }
    if ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1":
        raise ValueError("dependency ledger schema mismatch")
    if ledger.get("consumer_theorem_id") != THEOREM:
        raise ValueError("dependency ledger consumer mismatch")
    if ledger.get("observed_theorem_dag_sha256") != GRAPH_SHA256:
        raise ValueError("dependency ledger graph binding is stale")
    if ledger.get("dependency_context_sha256") != CONTEXT_SHA256:
        raise ValueError("dependency ledger context binding is stale")
    if ledger.get("repository_revision") != BASE_REVISION:
        raise ValueError("dependency ledger repository binding is stale")
    for key in expected_empty:
        if ledger.get(key) != []:
            raise ValueError(f"dependency ledger {key} is not the audited empty closure")
    if ledger.get("shared_group_ids") != [SHARED_GROUP]:
        raise ValueError("dependency ledger shared-group context mismatch")
    if ledger.get("closure_audit") != {
        "parent_inspection_order": [],
        "inspected_parent_ids": [],
        "status": "empty_hard_parent_closure_inspected",
    }:
        raise ValueError("dependency ledger lacks the exact empty parent audit")
    decisions = ledger.get("reuse_decisions")
    if not isinstance(decisions, list) or len(decisions) != 1:
        raise ValueError("dependency ledger must decide the one shared group exactly once")
    decision = decisions[0]
    if decision.get("source_id") != SHARED_GROUP:
        raise ValueError("shared-group decision identity mismatch")
    if decision.get("provider_theorem_id") != "THM-M-0540":
        raise ValueError("shared-group inspected member mismatch")
    if decision.get("decision") != "not_applicable":
        raise ValueError("weak module co-mention was improperly credited as reuse")
    if decision.get("context_digest") != CONTEXT_SHA256:
        raise ValueError("shared-group decision context mismatch")
    if decision.get("inspected_member_artifacts") != SHARED_ARTIFACTS:
        raise ValueError("shared-group inspected artifact record mismatch")
    if not decision.get("non_reuse_reason"):
        raise ValueError("shared-group decision lacks a non-reuse reason")
    for relative, expected in SHARED_ARTIFACTS.items():
        if sha256(ROOT / relative) != expected:
            raise ValueError(f"shared-group artifact drifted: {relative}")


def lean_replay() -> None:
    if not (LEAN_ROOT / ".lake").exists():
        raise ValueError("pinned .lake artifacts are unavailable; fetching is forbidden")
    lean = Path(checked_output(["lake", "env", "which", "lean"], cwd=LEAN_ROOT))
    lake = Path(checked_output(["lake", "env", "which", "lake"], cwd=LEAN_ROOT))
    if sha256(lean) != LEAN_SHA256 or sha256(lake) != LAKE_SHA256:
        raise ValueError("pinned Lean or Lake executable digest mismatch")
    if LEAN_COMMIT not in checked_output([str(lean), "--version"], cwd=LEAN_ROOT):
        raise ValueError("pinned Lean executable identity mismatch")
    base_path = checked_output(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT)
    fixed_env = {
        **os.environ,
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "LEAN_PATH": base_path,
    }
    with tempfile.TemporaryDirectory(prefix="m0554-proof-", dir="/tmp") as raw:
        scratch = Path(raw)
        for name in ("Statement.lean", "Proof.lean"):
            (scratch / name).write_bytes((HERE / name).read_bytes())
        statement_result = run(
            [str(lean), "--trust=0", "-t0", f"--root={scratch}",
             "-o", str(scratch / "Statement.olean"), str(scratch / "Statement.lean")],
            cwd=LEAN_ROOT, env=fixed_env,
        )
        if statement_result.returncode:
            raise ValueError(f"trust-zero statement replay failed\n{statement_result.stdout}")
        proof_env = {**fixed_env, "LEAN_PATH": f"{scratch}:{base_path}"}
        proof_result = run(
            [str(lean), "--trust=0", "-t0", f"--root={scratch}",
             str(scratch / "Proof.lean")],
            cwd=LEAN_ROOT, env=proof_env,
        )
        if proof_result.returncode:
            raise ValueError(f"trust-zero proof replay failed\n{proof_result.stdout}")
        for declaration in DECLARATIONS:
            if printed_axioms(proof_result.stdout, declaration) != EXPECTED_AXIOMS:
                raise ValueError(f"unexpected axiom profile for {declaration}")
        if proof_result.stdout.count("Declarations are sorry-free!") != len(DECLARATIONS):
            raise ValueError("Lean did not confirm every claimed declaration sorry-free")


def verify() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION:
        raise ValueError("worker base revision drifted")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("worker base tree drifted")
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
            raise ValueError(f"owned input drifted: {name}")
        if git("hash-object", str(HERE / name)) != EXPECTED_BLOBS[name]:
            raise ValueError(f"owned input Git blob drifted: {name}")

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row.get("theorem_id") == THEOREM)
    if target.get("execution_rank") != 106 or target.get("lifecycle_mode") != "planned":
        raise ValueError("target manifest identity or lifecycle drifted")
    if target.get("theorem_complete") is not False:
        raise ValueError("target manifest unexpectedly claims theorem completion")

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    phase_items = {
        row["phase"]: row for row in execution["items"]
        if row.get("theorem_id") == THEOREM
    }
    if set(phase_items) != PHASES:
        raise ValueError("target lacks the exact seven phase items")
    proof_item = phase_items["proof"]
    if proof_item.get("state") != "[ ]" or proof_item.get("attempts") != 0:
        raise ValueError("proof item no longer matches the claimed open cursor")
    if proof_item.get("id") != ITEM:
        raise ValueError("proof phase item identity changed")
    if proof_item.get("depends_on") != ["S56-M-0554-OBLIGATION_TREE"]:
        raise ValueError("proof phase predecessor changed")
    if phase_items["obligation_tree"].get("state") != "[_]":
        raise ValueError("observed predecessor state changed")

    dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in dag["theorems"] if row.get("theorem_id") == THEOREM)
    if node.get("v2_execution_rank") != 322 or node.get("topological_layer") != 0:
        raise ValueError("exact v2 claim order changed")
    for key in ("direct_hard_parents", "transitive_hard_ancestors", "direct_reuse_hint_ids"):
        if node.get(key) != []:
            raise ValueError(f"unexpected dependency context in {key}")
    if node.get("shared_lemma_group_ids") != [SHARED_GROUP]:
        raise ValueError("shared-group context changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        raise ValueError("dependency context digest changed")
    validate_ledger()

    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    proofs = [row for row in contract.get("phases", []) if row.get("phase") == "proof"]
    if len(proofs) != 1 or proofs[0].get("intent") != "prove" or proofs[0].get("layer") != 4:
        raise ValueError("HEAD proof phase contract changed")
    candidates = proofs[0].get("validator_candidates")
    expected_candidates = [
        "Stage1_Instances/{theorem_id}/check_proof.py",
        "Stage1_Instances/{theorem_id}/check_proof.sh",
    ]
    if [row.get("path_pattern") for row in candidates] != expected_candidates:
        raise ValueError("proof validator candidate contract changed")
    existing = [
        pattern.format(theorem_id=THEOREM) for pattern in expected_candidates
        if (ROOT / pattern.format(theorem_id=THEOREM)).is_file()
    ]
    if existing != ["Stage1_Instances/THM-M-0554/check_proof.py"]:
        raise ValueError("proof validator selection is not exactly one HEAD candidate")

    receipt = load(HERE / "proof-receipt.json")
    required = {
        "schema_version", "receipt_id", "item_id", "theorem_id", "phase", "intent",
        "base_revision", "base_tree", "inputs", "support_state", "proposed_state",
        "accepted", "verdict", "selftest_status", "selftest_result", "known_failures",
        "first_failed_gate", "retry_condition", "status_boundary", "audit_complete",
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
    if receipt.get("support_state") != "provisional_worker_selftest":
        raise ValueError("proof receipt support state mismatch")
    if receipt.get("proposed_state") != "[_]" or receipt.get("accepted") is not False:
        raise ValueError("proof receipt improperly claims master acceptance")
    if receipt.get("verdict") != "blocked" or receipt.get("selftest_status") != "passed":
        raise ValueError("proof receipt does not preserve the self-tested blocker verdict")
    if receipt.get("selftest_result", {}).get("exit_code") != 0:
        raise ValueError("proof receipt self-test exit is not successful")
    commands = receipt.get("selftest_result", {}).get("commands")
    if not isinstance(commands, list) or not commands:
        raise ValueError("proof receipt lacks exact self-test commands")
    if receipt.get("canonical_target") != "Stage1.THM_M_0554.Statement":
        raise ValueError("proof receipt canonical target mismatch")
    if receipt.get("exact_declarations") != DECLARATIONS:
        raise ValueError("proof receipt exact declaration boundary mismatch")
    if receipt.get("closed_obligation_ids") != []:
        raise ValueError("proof receipt improperly closes a frozen obligation")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        raise ValueError("proof receipt overstates a terminal decision")
    expected_result = {
        "exit_code": 0,
        "semantic_verdict": "blocked",
        "phase_predicate_proven": False,
        "phase_accepted": False,
        "blocked": True,
        "audit_complete": False,
        "theorem_complete": False,
        "root_closed": False,
        "open_obligations": len(OPEN_IDS),
        "provisional_candidate_obligation_ids": PROVISIONAL_IDS,
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "placeholder_scan": "pass",
    }
    if receipt.get("result") != expected_result:
        raise ValueError("proof receipt semantic result mismatch")
    proof_sources = receipt.get("inputs", {}).get("proof_sources")
    if not isinstance(proof_sources, list) or len(proof_sources) != 1:
        raise ValueError("proof receipt must bind exactly one proof source")
    if proof_sources[0] != {
        "path": "Stage1_Instances/THM-M-0554/Proof.lean",
        "sha256": EXPECTED_HASHES["Proof.lean"],
        "git_blob": EXPECTED_BLOBS["Proof.lean"],
    }:
        raise ValueError("proof receipt source byte binding mismatch")
    bindings = receipt.get("input_bindings")
    if not isinstance(bindings, dict):
        raise ValueError("proof receipt lacks complete path bindings")
    for name, expected in EXPECTED_HASHES.items():
        binding = bindings.get(name)
        if not isinstance(binding, dict):
            raise ValueError(f"proof receipt lacks binding for {name}")
        if binding.get("path") != f"Stage1_Instances/THM-M-0554/{name}":
            raise ValueError(f"proof receipt path binding mismatch: {name}")
        if binding.get("sha256") != expected or binding.get("git_blob") != EXPECTED_BLOBS[name]:
            raise ValueError(f"proof receipt content binding mismatch: {name}")
    validator = HERE / "check_proof.py"
    validator_binding = bindings.get("check_proof.py")
    if not isinstance(validator_binding, dict):
        raise ValueError("proof receipt lacks validator binding")
    if validator_binding.get("path") != "Stage1_Instances/THM-M-0554/check_proof.py":
        raise ValueError("validator path binding mismatch")
    if validator_binding.get("sha256") != sha256(validator):
        raise ValueError("validator SHA-256 binding mismatch")
    if validator_binding.get("git_blob") != git("hash-object", str(validator)):
        raise ValueError("validator Git blob binding mismatch")

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
    if packet.get("commands") != commands:
        raise ValueError("worker packet and receipt command evidence disagree")
    if packet.get("known_failures") != receipt.get("known_failures"):
        raise ValueError("worker packet and receipt known failures disagree")
    expected_changed = {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0554/check_proof.py",
        "Stage1_Instances/THM-M-0554/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0554/proof-receipt.json",
        "Stage1_Instances/THM-M-0554/proof-validation.md",
    }
    if set(packet.get("changed_paths", [])) != expected_changed:
        raise ValueError("worker packet changed-path scope mismatch")
    status = run(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT,
    )
    if status.returncode:
        raise ValueError("cannot inspect worker worktree")
    actual_changed = {
        line[3:] for line in status.stdout.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    if actual_changed != expected_changed:
        raise ValueError("worktree delta escapes or omits the declared target scope")

    registry = load(HERE / "obligation-registry.json")
    rows = registry.get("obligations")
    if not isinstance(rows, list) or {row.get("obligation_id") for row in rows} != OPEN_IDS:
        raise ValueError("frozen obligation denominator identity changed")
    if registry.get("root_obligation_id") != "M0554-ROOT":
        raise ValueError("frozen root identity changed")
    if registry.get("denominator_sha256") != DENOMINATOR_SHA256:
        raise ValueError("frozen denominator digest changed")
    credited = {
        row.get("obligation_id"): row.get("terminal_proof_body_id") for row in rows
        if isinstance(row.get("terminal_proof_body_id"), str)
        and not row["terminal_proof_body_id"].startswith("missing:")
    }
    if credited != {
        "M0554-S-EXACT": "local:Stage1.THM_M_0554.statement_iff",
        "M0554-X-SPECTRAL":
            "mathlib:8a178386:CategoryTheory.E2CohomologicalSpectralSequence",
    }:
        raise ValueError("registry body inventory changed")
    closure = load(HERE / "typed-graphs.json").get("closure_boundary")
    if closure != {
        "closed_obligations": [],
        "root_machine_debt": "M4",
        "root_closed": False,
        "remaining_root_cut_set": [
            "M0554-X-GENCOH", "M0554-C-EXACT-COUPLE",
            "M0554-C-E2-MODEL", "M0554-L-STRONG",
        ],
        "composition_certificates_checked": [],
        "audit_complete": False,
        "theorem_complete": False,
    }:
        raise ValueError("typed graph closure boundary changed")

    for name in ("Statement.lean", "Proof.lean"):
        clean = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        if PROHIBITED.search(clean):
            raise ValueError(f"prohibited proof construct found in {name}")
    if git("rev-parse", "HEAD", cwd=MATHLIB) != MATHLIB_REVISION:
        raise ValueError("mathlib revision drifted")
    if git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) != MATHLIB_TREE:
        raise ValueError("mathlib tree drifted")
    if git("status", "--porcelain=v1", cwd=MATHLIB):
        raise ValueError("mathlib checkout is dirty")
    lean_replay()


def semantic_result(*, verified: bool, error: str | None = None) -> dict[str, Any]:
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
            "P04-KERNEL/S56-5.1-EXACT-TARGET-CONSISTENCY/M0554-S-DATA"
            if verified else "P01-ARTIFACTS"
        ),
        "open_obligations": len(OPEN_IDS),
        "stale_inputs": [],
        "blocked": verified,
        "message": (
            "Conditional branch composition replays at trust zero, but it assumes all four "
            "AHSS branch packages; the frozen source-unfaithful target has 32 open obligations."
            if verified else f"Proof blocker replay failed: {error}"
        ),
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
