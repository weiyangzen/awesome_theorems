#!/usr/bin/env python3
"""Fail-closed semantic validator for S56-M-0583-PROOF."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0583"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0583-PROOF"
THEOREM = "THM-M-0583"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "cdf6c9f8de36e769dba3868e130e3dbcced7e1e38e0429fb4b3a728c4b787aff"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
TARGET_EXPRESSION_SHA256 = (
    "8ba8ef3cba0ad739c717ad8f42d40c221ff7a2cdcf79f7098709a60bd7a7ebce"
)
DENOMINATOR_SHA256 = (
    "910aad119639e1751b6f8c0ad6d04f98a030acdc0e00c951cd46f6efff18cccd"
)
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_POINCARE_SHA256 = (
    "4b9c454dac5fb68da0ff0bac0efe9e5d4ce17c87b9892ff63343c42e761bb8cf"
)
EXPECTED_HASHES = {
    "Statement.lean": "ce7668cd0bd07aaf54ed7d60bb9eb74253b6ab48ab97e38c12d1446d99eec6d8",
    "ObligationTree.lean": "c94f747e03bfce01c35a1c3e571230b6c2153bb721701ee85cd36a1100b00076",
    "ProofBlockerProbe.lean": "dd2897ba5f2eac92a0e6a36eee55877fb30837e22bb186f57a6e3b906df29744",
    "anchor-audit.json": "0921114daab79180db4817dcf6ab1f6957ac9eede62497e4406b72538f750396",
    "obligation-registry.json": "1db09a273d7c989f950c0c346a6317b84d593f784d4027b82d51a4c0e37c9ef2",
    "typed-graphs.json": "69eb81febc06de38ef6eb8ff23ada7ef6a2c3d0192f027bdbcb2601055690bef",
    "task-dag.json": "7f8ccd6bb0e9ebfaf8556513b0aebb60771d493eb218adfb7e6bc22352fcf25a",
    "proof-blocker.json": "dcc906e809458e2e433cfe534977ea2762c3a368a628c0af90b1276df4b20a2b",
    "dependency-reuse-ledger.json": "9f228d8023163cb7657db02f5e1706714facc172a56f1c053b145e8aa27dc084",
}
SHARED_GROUP = "SHARED-MODULE-b3a9d89c683d7166"
SHARED_PROVIDER = "THM-M-0586"
SHARED_ARTIFACTS = {
    "Stage1_Instances/THM-M-0586/Statement.lean":
        "326186c55d4b7abcefbd6f3c3e2813e8f0271bcbfc266ae937b6e7f220b42b49",
    "Stage1_Instances/THM-M-0586/anchor-audit.json":
        "c9f7de88584d686d18d9b8b17e182dc39e4ded67ebf28580958b00cb61ce894e",
    "Stage1_Instances/THM-M-0586/proof-blocker.json":
        "c339d819f420e3b0f1017b7ac47c45e2c4578bf0f324b287bc5528de7e151822",
}
OPEN_IDS = {
    "M0583-ROOT",
    "M0583-S-ENCODING",
    "M0583-H-SOURCE-CROSSWALK",
    "M0583-R-HOMOTOPY-DATA",
    "M0583-C-TOPOLOGICAL-MODEL",
    "M0583-L-DISK-EMBEDDING",
    "M0583-L-SURGERY",
    "M0583-L-S-COBORDISM",
    "M0583-C-HOMEOMORPHISM",
    "M0583-X-FREEDMAN-CORE",
    "M0583-T-EXACT-ADAPTER",
    "M0583-C-ROOT-COMPOSITION",
    "M0583-X-PROVENANCE",
    "M0583-S-FOUNDATION",
    "M0583-D-READABLE",
    "M0583-E-VALIDATION",
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
    result = run(argv, cwd=cwd, timeout=30)
    if result.returncode:
        raise ValueError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout.strip()


def git(*argv: str, cwd: Path = ROOT) -> str:
    return checked_output(["git", *argv], cwd=cwd)


def source_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string:
            output.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif pair == "/-":
            depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            newline = source.find("\n", index)
            if newline < 0:
                output.extend(" " * (len(source) - index))
                index = len(source)
            else:
                output.extend(" " * (newline - index))
                index = newline
        elif char == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
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
        value.strip()
        for value in match.group(1).replace("\n", "").split(",")
        if value.strip()
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
            raise ValueError(f"dependency ledger field {key} is not the empty closure")
    if ledger.get("shared_group_ids") != [SHARED_GROUP]:
        raise ValueError("dependency ledger shared group changed")
    closure = ledger.get("closure_audit")
    if not isinstance(closure, dict):
        raise ValueError("dependency ledger lacks closure audit")
    if closure.get("parent_inspection_order") != [] or closure.get("inspected_parent_ids") != []:
        raise ValueError("dependency ledger invents a hard-parent inspection")
    if closure.get("expected_inspection_count") != 0 or closure.get("actual_inspection_count") != 0:
        raise ValueError("dependency ledger empty-closure count changed")
    if closure.get("status") != "empty_hard_parent_closure_inspected":
        raise ValueError("dependency ledger empty closure is not audited")
    decisions = ledger.get("reuse_decisions")
    if not isinstance(decisions, list) or len(decisions) != 1:
        raise ValueError("dependency ledger must decide the shared group exactly once")
    decision = decisions[0]
    if (
        decision.get("source_id") != SHARED_GROUP
        or decision.get("provider_theorem_id") != SHARED_PROVIDER
        or decision.get("decision") != "not_applicable"
        or decision.get("context_digest") != CONTEXT_SHA256
        or decision.get("provider_proof_state") != "[ ]"
        or not decision.get("non_reuse_reason")
    ):
        raise ValueError("shared-group non-reuse decision changed")
    if decision.get("inspected_artifact_digests") != SHARED_ARTIFACTS:
        raise ValueError("shared-group inspected artifact set changed")
    for relative, expected in SHARED_ARTIFACTS.items():
        if sha256(ROOT / relative) != expected:
            raise ValueError(f"shared-group artifact drifted: {relative}")


def lean_replay() -> None:
    if not LEAN_ROOT.joinpath(".lake").exists():
        raise ValueError("pinned .lake artifacts are unavailable; fetching is forbidden")
    if git("rev-parse", "HEAD", cwd=MATHLIB) != MATHLIB_REVISION:
        raise ValueError("pinned mathlib revision drifted")
    if git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) != MATHLIB_TREE:
        raise ValueError("pinned mathlib tree drifted")
    if git("status", "--porcelain=v1", cwd=MATHLIB):
        raise ValueError("pinned mathlib worktree is dirty")
    poincare = MATHLIB / "Mathlib" / "Geometry" / "Manifold" / "PoincareConjecture.lean"
    if sha256(poincare) != MATHLIB_POINCARE_SHA256:
        raise ValueError("pinned Poincare source drifted")
    source = poincare.read_text(encoding="utf-8")
    if "proof_wanted ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere" not in source:
        raise ValueError("pinned Poincare proof-wanted boundary changed")

    lean = Path(checked_output(["lake", "env", "which", "lean"], cwd=LEAN_ROOT))
    base_path = checked_output(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT)
    fixed_env = {
        **os.environ,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "LEAN_PATH": base_path,
    }
    with tempfile.TemporaryDirectory(prefix="m0583-proof-", dir="/tmp") as raw:
        scratch = Path(raw)
        outputs: dict[str, str] = {}
        for name in ("Statement.lean", "ObligationTree.lean", "ProofBlockerProbe.lean"):
            (scratch / name).write_bytes((HERE / name).read_bytes())
            result = run(
                [str(lean), "--trust=0", "-t0", "--root", str(scratch),
                 str(scratch / name)],
                cwd=LEAN_ROOT,
                env=fixed_env,
            )
            if result.returncode:
                raise ValueError(f"trust-zero replay failed for {name}\n{result.stdout}")
            outputs[name] = result.stdout
        if printed_axioms(
            outputs["ObligationTree.lean"],
            "Stage1Instances.THM_M_0583.ObligationTree.canonicalRoot_of_freedmanTopologicalCore",
        ) != {"propext", "Classical.choice", "Quot.sound"}:
            raise ValueError("conditional adapter axiom profile changed")
        if printed_axioms(
            outputs["ProofBlockerProbe.lean"],
            "Stage1Instances.THM_M_0583.proofPhaseCore_iff_canonicalRoot",
        ) != {"propext", "Classical.choice", "Quot.sound"}:
            raise ValueError("diagnostic equivalence axiom profile changed")


def verify() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION or git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("worker base revision or tree drifted")
    if sha256(ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json") != GRAPH_SHA256:
        raise ValueError("authoritative theorem DAG drifted")
    if sha256(ROOT / "Docs" / "Stage1_Phase_Acceptance_Contracts.json") != CONTRACT_SHA256:
        raise ValueError("phase acceptance contract drifted")
    if sha256(LEAN_ROOT / "lean-toolchain") != TOOLCHAIN_SHA256:
        raise ValueError("Lean toolchain file drifted")
    if sha256(LEAN_ROOT / "lake-manifest.json") != MANIFEST_SHA256:
        raise ValueError("Lake manifest drifted")
    for name, expected in EXPECTED_HASHES.items():
        if sha256(HERE / name) != expected:
            raise ValueError(f"owned frozen input drifted: {name}")

    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row.get("theorem_id") == THEOREM)
    if target.get("execution_rank") != 116 or target.get("lifecycle_mode") != "planned":
        raise ValueError("target manifest identity or lifecycle drifted")
    if target.get("theorem_complete") is not False:
        raise ValueError("target manifest unexpectedly claims theorem completion")

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    phase_items = {
        row["phase"]: row for row in execution["items"]
        if row.get("theorem_id") == THEOREM
    }
    if set(phase_items) != PHASES:
        raise ValueError("target does not have the exact seven phase items")
    if phase_items["proof"].get("state") != "[ ]" or phase_items["proof"].get("attempts") != 0:
        raise ValueError("proof item no longer matches the assigned open state")
    if phase_items["proof"].get("depends_on") != ["S56-M-0583-OBLIGATION_TREE"]:
        raise ValueError("proof prerequisite identity changed")
    if phase_items["obligation_tree"].get("state") != "[_]":
        raise ValueError("proof prerequisite observation changed")

    theorem_dag = load(ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json")
    node = next(row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM)
    if node.get("v2_execution_rank") != 332 or node.get("topological_layer") != 0:
        raise ValueError("v2 claim order changed")
    for field in ("direct_hard_parents", "transitive_hard_ancestors", "direct_reuse_hint_ids"):
        if node.get(field) != []:
            raise ValueError(f"unexpected dependency context in {field}")
    if node.get("shared_lemma_group_ids") != [SHARED_GROUP]:
        raise ValueError("shared-group context changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        raise ValueError("dependency context digest changed")
    validate_ledger()

    registry = load(HERE / "obligation-registry.json")
    rows = registry.get("obligations")
    if not isinstance(rows, list) or {row.get("obligation_id") for row in rows} != OPEN_IDS:
        raise ValueError("frozen obligation denominator identity changed")
    if registry.get("denominator_sha256") != DENOMINATOR_SHA256:
        raise ValueError("frozen obligation denominator digest changed")
    if registry.get("status_observed_after_freeze", {}).get("closed_obligations") != []:
        raise ValueError("frozen registry unexpectedly records closed obligations")
    if any(row.get("terminal_proof_body_id") is not None for row in rows):
        raise ValueError("frozen registry unexpectedly records a terminal proof body")
    graphs = load(HERE / "typed-graphs.json")
    closure = graphs.get("closure_boundary")
    if not isinstance(closure, dict) or closure.get("closed_obligations") != []:
        raise ValueError("typed graph unexpectedly credits proof closure")
    if closure.get("theorem_complete") is not False:
        raise ValueError("typed graph unexpectedly claims theorem completion")

    statement = load(HERE / "statement.json")
    if statement["canonical_formal_target"]["elaborated_expression_sha256"] != TARGET_EXPRESSION_SHA256:
        raise ValueError("canonical target fingerprint drifted")
    blocker = load(HERE / "proof-blocker.json")
    if blocker.get("proof_body_added") is not False or blocker.get("root_closed") is not False:
        raise ValueError("proof blocker incorrectly records a proof body")
    if blocker.get("first_failed_gate", "").split(":", 1)[0] != "M0583-X-FREEDMAN-CORE":
        raise ValueError("proof blocker first failed gate changed")

    for name in ("Statement.lean", "ObligationTree.lean", "ProofBlockerProbe.lean"):
        source = source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        if PROHIBITED.search(source):
            raise ValueError(f"prohibited proof or trust construct found in {name}")

    contract = load(ROOT / "Docs" / "Stage1_Phase_Acceptance_Contracts.json")
    proof_contracts = [row for row in contract["phases"] if row.get("phase") == "proof"]
    if len(proof_contracts) != 1:
        raise ValueError("HEAD phase contract lacks exactly one proof row")
    candidates = proof_contracts[0].get("validator_candidates")
    if [row.get("path_pattern") for row in candidates] != [
        "Stage1_Instances/{theorem_id}/check_proof.py",
        "Stage1_Instances/{theorem_id}/check_proof.sh",
    ]:
        raise ValueError("proof validator candidate contract changed")
    existing = [
        row["path_pattern"].format(theorem_id=THEOREM)
        for row in candidates
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM)).is_file()
    ]
    if existing != ["Stage1_Instances/THM-M-0583/check_proof.py"]:
        raise ValueError("proof validator candidate selection is not exact")

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
    if (receipt.get("item_id"), receipt.get("theorem_id"), receipt.get("phase"), receipt.get("intent")) != (
        ITEM, THEOREM, "proof", "prove",
    ):
        raise ValueError("proof receipt identity changed")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        raise ValueError("proof receipt base binding changed")
    if receipt.get("support_state") != "provisional_worker_selftest" or receipt.get("proposed_state") != "[_]":
        raise ValueError("proof receipt worker support state changed")
    if receipt.get("accepted") is not False or receipt.get("verdict") != "blocked":
        raise ValueError("proof receipt overstates acceptance")
    if receipt.get("selftest_status") != "passed" or receipt.get("selftest_result", {}).get("exit_code") != 0:
        raise ValueError("proof receipt self-test did not pass")
    if not receipt.get("selftest_result", {}).get("commands"):
        raise ValueError("proof receipt has no exact self-test commands")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        raise ValueError("proof receipt crosses a terminal boundary")
    if receipt.get("closed_obligation_ids") != [] or receipt.get("exact_declarations") != []:
        raise ValueError("blocked proof receipt improperly claims proof closure")
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
        raise ValueError("proof receipt semantic result changed")
    proof_sources = receipt.get("inputs", {}).get("proof_sources")
    if not isinstance(proof_sources, list) or len(proof_sources) != 1:
        raise ValueError("proof receipt must bind the blocker probe as its proof source")
    source_binding = proof_sources[0]
    if source_binding.get("path") != "Stage1_Instances/THM-M-0583/ProofBlockerProbe.lean":
        raise ValueError("proof receipt source path changed")
    if source_binding.get("sha256") != EXPECTED_HASHES["ProofBlockerProbe.lean"]:
        raise ValueError("proof receipt source SHA-256 changed")
    if source_binding.get("git_blob") != git("hash-object", str(HERE / "ProofBlockerProbe.lean")):
        raise ValueError("proof receipt source Git blob changed")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id", "changed_paths", "commands", "output_summary", "base_revision",
        "known_failures", "state",
    }:
        raise ValueError("worker self-test packet schema changed")
    if packet.get("item_id") != ITEM or packet.get("state") != "[_]":
        raise ValueError("worker self-test packet identity changed")
    if packet.get("base_revision") != BASE_REVISION:
        raise ValueError("worker self-test packet base changed")
    if packet.get("commands") != receipt.get("selftest_result", {}).get("commands"):
        raise ValueError("worker packet and receipt commands disagree")
    if packet.get("known_failures") != receipt.get("known_failures"):
        raise ValueError("worker packet and receipt failures disagree")
    expected_changed = {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0583/check_proof.py",
        "Stage1_Instances/THM-M-0583/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0583/proof-receipt.json",
        "Stage1_Instances/THM-M-0583/proof-validation.md",
    }
    if set(packet.get("changed_paths", [])) != expected_changed:
        raise ValueError("worker self-test changed-path scope changed")
    status = run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=ROOT,
        timeout=30,
    )
    if status.returncode:
        raise ValueError("cannot inspect the worker worktree delta")
    records = [value for value in status.stdout.split("\0") if value]
    actual_changed = set()
    for record in records:
        path = record[3:]
        if path == "Formalizations/Lean/.lake" or path.startswith("Formalizations/Lean/.lake/"):
            continue
        actual_changed.add(path)
    if actual_changed != expected_changed:
        raise ValueError("worktree delta escapes or omits the declared target scope")
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
            "P04-KERNEL/M0583-X-FREEDMAN-CORE" if verified else "P01-ARTIFACTS"
        ),
        "open_obligations": len(OPEN_IDS),
        "stale_inputs": [],
        "blocked": verified,
        "message": (
            "No eligible retained proof body inhabits the exact four-dimensional "
            "topological Poincare target; all 16 frozen obligations remain open."
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
