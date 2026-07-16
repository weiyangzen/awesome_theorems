#!/usr/bin/env python3
"""Fail-closed semantic validator for S56-M-0110-PROOF."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0110"
ITEM = "S56-M-0110-PROOF"
THEOREM = "THM-M-0110"
BASE_REVISION = "307c34d30fc3763c82a944a142ae922b48ff18aa"
BASE_TREE = "ef45ba442c71959db78ad146a023bcf32946a53f"
GRAPH_SHA256 = "8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47"
CONTEXT_SHA256 = "4f60e4c0e01ec4cc069fbe1a7601aabdc8f2acf1df3e4c917e09e4235cec640b"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
TARGET_SHA256 = "d0a9a0e873dd388aa37c0bcc77fce1fc38bae5911851a87570b94f50c80eecc6"
REGISTRY_DENOMINATOR = "153eb5eb51ad4419b8eed1a637a24ff66c7690442339b4fefebb327dc20c2cba"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
STATEMENT_OLEAN_SHA256 = "801714acbf5a066898fb023ed7a2c21ccb76d6f2380c4d614c69320073a47421"
PROOF_OLEAN_SHA256 = "52a98788887ac65c9937a0af3e456e6f72865aa178b10f6c10fefc94e73984eb"
SHARED_GROUPS = ["SHARED-MODULE-735a79718fe89f59"]
EXACT_DECLARATIONS = [
    "Stage1Instances.THMM0110.Proof.kodairaVanishingTarget_of_vanishing"
]
EXPECTED_INPUT_HASHES = {
    "Statement.lean": "81e89341fc571e588c47c8984d71779fd4b90b2cd55ae70c3392c742655574dd",
    "ObligationTree.lean": "50a046419ce96d6a25617ebffe90579ecf4381c10d56491d0690f83584f0f712",
    "Proof.lean": "518f89a4591b6261d27a946f3d99517b09cc45bdbb6d76c51c475a90792abb16",
    "anchor-audit.json": "ebc44cef5ee0a085db29688e3f4f5579cbe79d0869ea14e8b475c119e6f75c66",
    "obligation-registry.json": "83e751a0cc3082103f622e35ece193535b59b758befaf606e6798a9ff7fee107",
    "typed-graphs.json": "9f18edd9d801b70d9272543df3ee5c8091b9aa147ede3b8c3cbbeaf5a96e110b",
    "validation-specs.json": "c7f008f81a03fdbb193b934b2f2a2789657fdbc65dfc5c3911053ba84e975bd0",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)


class ValidationError(RuntimeError):
    pass


def fail(message: str) -> NoReturn:
    raise ValidationError(message)


def load(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            if key in value:
                fail(f"duplicate JSON key {key!r} in {path.relative_to(ROOT)}")
            value[key] = child
        return value

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
        )
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {path.relative_to(ROOT)}: {error}")
    if not isinstance(value, dict):
        fail(f"expected JSON object in {path.relative_to(ROOT)}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*argv: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=cwd, capture_output=True, text=True, timeout=30
    )
    if result.returncode:
        fail(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def strip_comments_and_strings(source: str) -> str:
    out: list[str] = []
    index = 0
    depth = 0
    quoted = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                out.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                out.extend("  ")
                index += 2
            else:
                out.append("\n" if char == "\n" else " ")
                index += 1
        elif quoted:
            out.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            index += 1
        elif pair == "/-":
            depth = 1
            out.extend("  ")
            index += 2
        elif pair == "--":
            end = source.find("\n", index)
            if end == -1:
                out.extend(" " * (len(source) - index))
                index = len(source)
            else:
                out.extend(" " * (end - index))
                index = end
        elif char == '"':
            quoted = True
            out.append(" ")
            index += 1
        else:
            out.append(char)
            index += 1
    if depth or quoted:
        fail("unterminated comment or string in Lean source")
    return "".join(out)


def run_checked(argv: list[str], *, cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=240
    )
    if result.returncode:
        fail(f"command failed ({' '.join(argv)}): {result.stdout}{result.stderr}")
    return result


def lean_replay() -> tuple[str, str, str]:
    lean_root = ROOT / "Formalizations" / "Lean"
    lake = lean_root / ".lake"
    if not lake.exists():
        fail("pinned .lake artifacts are unavailable; dependency fetching is forbidden")
    mathlib = lake / "packages" / "mathlib"
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        fail("pinned mathlib revision changed")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        fail("pinned mathlib tree changed")
    if git("status", "--porcelain=v1", cwd=mathlib):
        fail("pinned mathlib worktree is dirty")

    lake_bin = Path.home() / ".elan" / "bin" / "lake"
    if not lake_bin.is_file():
        fail("pinned Lake launcher is unavailable")
    base_env = {
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "NO_COLOR": "1",
        "LEAN_NUM_THREADS": "1",
        "PATH": (
            str(lake_bin.parent) + ":" + str(Path(sys.executable).parent)
            + ":/usr/local/bin:/usr/bin:/bin"
        ),
        "HOME": str(Path.home()),
    }
    path_result = run_checked(
        [str(lake_bin), "env", "printenv", "LEAN_PATH"],
        cwd=lean_root,
        env=base_env,
    )
    lean_path = path_result.stdout.strip()
    with tempfile.TemporaryDirectory(prefix="thm-m-0110-proof-") as raw_tmp:
        tmp = Path(raw_tmp)
        for name in ("Statement.lean", "Proof.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        statement_result = run_checked(
            [
                str(lake_bin), "env", "lean", "--trust=0", "-t0",
                f"--root={tmp}", str(tmp / "Statement.lean"),
                "-o", str(tmp / "Statement.olean"),
            ],
            cwd=lean_root,
            env=base_env,
        )
        local_env = {**base_env, "LEAN_PATH": f"{tmp}:{lean_path}"}
        proof_result = run_checked(
            [
                str(lake_bin), "env", "lean", "--trust=0", "-t0",
                f"--root={tmp}", str(tmp / "Proof.lean"),
                "-o", str(tmp / "Proof.olean"),
            ],
            cwd=lean_root,
            env=local_env,
        )
        statement_hash = digest(tmp / "Statement.olean")
        proof_hash = digest(tmp / "Proof.olean")
    return statement_result.stdout + statement_result.stderr, proof_result.stdout + proof_result.stderr, statement_hash + ":" + proof_hash


def verify_authorities() -> tuple[dict[str, Any], dict[str, Any]]:
    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("repository HEAD differs from the claimed worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository tree differs from the claimed worker base")
    for relative, expected in {
        "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
        "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    }.items():
        if digest(ROOT / relative) != expected:
            fail(f"authority input changed: {relative}")

    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row.get("theorem_id") == THEOREM)
    if target.get("execution_rank") != 34 or target.get("theorem_complete") is not False:
        fail("target membership, rank, or completion boundary changed")

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM)
    if item != {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 34,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-0110-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }:
        fail("authoritative proof item changed")
    predecessor = next(
        row for row in execution["items"]
        if row.get("id") == "S56-M-0110-OBLIGATION_TREE"
    )
    if predecessor.get("state") != "[_]":
        fail("observed prerequisite state changed")

    theorem_dag = load(ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json")
    node = next(row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM)
    if node.get("v2_execution_rank") != 269 or node.get("topological_layer") != 0:
        fail("v2 execution order changed")
    if node.get("phase_states", {}).get("proof") != "[ ]":
        fail("v2 proof state changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency context changed")
    if node.get("direct_hard_parents") != [] or node.get("transitive_hard_ancestors") != []:
        fail("hard-parent closure is no longer empty")
    if node.get("direct_reuse_hint_ids") != []:
        fail("reuse-hint closure is no longer empty")
    if node.get("shared_lemma_group_ids") != SHARED_GROUPS:
        fail("shared-group context changed")

    contract = load(ROOT / "Docs" / "Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row.get("phase") == "proof")
    if phase.get("layer") != 4 or phase.get("intent") != "prove":
        fail("proof phase contract changed")
    if [row.get("path_pattern") for row in phase["validator_candidates"]] != [
        "Stage1_Instances/{theorem_id}/check_proof.py",
        "Stage1_Instances/{theorem_id}/check_proof.sh",
    ]:
        fail("proof validator candidates changed")
    if (HERE / "check_proof.sh").exists():
        fail("proof validator selection is ambiguous")
    return node, phase


def verify_ledger() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    for field, expected in (
        ("schema_version", "stage1-dependency-reuse-ledger/1.1"),
        ("consumer_theorem_id", THEOREM),
        ("observed_theorem_dag_sha256", GRAPH_SHA256),
        ("dependency_context_sha256", CONTEXT_SHA256),
        ("repository_revision", BASE_REVISION),
    ):
        if ledger.get(field) != expected:
            fail(f"dependency ledger field {field} changed")
    for field in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "inspections", "unresolved_compatibility_obligations",
    ):
        if ledger.get(field) != []:
            fail(f"dependency ledger field {field} is no longer empty")
    if ledger.get("shared_group_ids") != SHARED_GROUPS:
        fail("dependency ledger shared groups changed")
    decisions = ledger.get("reuse_decisions")
    if not isinstance(decisions, list) or [row.get("source_id") for row in decisions] != SHARED_GROUPS:
        fail("dependency ledger shared-group decisions are incomplete")
    decision = decisions[0]
    if decision.get("decision") != "not_applicable":
        fail("dependency ledger invents accepted reuse")
    if decision.get("provider_theorem_id") != "THM-M-0118":
        fail("dependency ledger shared-group provider changed")
    if decision.get("context_digest") != CONTEXT_SHA256 or not decision.get("non_reuse_reason"):
        fail("dependency ledger weak-group decision is unbound")
    if decision.get("provider_acceptance_inherited") is not False:
        fail("dependency ledger inherits provider acceptance")
    for relative, expected in decision.get("inspected_member_artifacts", {}).items():
        if digest(ROOT / relative) != expected:
            fail(f"inspected weak-group artifact changed: {relative}")
    audit = ledger.get("closure_audit", {})
    if audit.get("parent_inspection_order") != [] or audit.get("inspected_parent_ids") != []:
        fail("parent inspection order is not the authoritative empty closure")
    if audit.get("expected_parent_inspection_count") != 0 or audit.get("actual_parent_inspection_count") != 0:
        fail("empty parent inspection count changed")
    if audit.get("claim_order") != {
        "v2_execution_rank": 269,
        "phase_layer": 4,
        "phase_item_id": ITEM,
    }:
        fail("dependency ledger claim order changed")


def verify_sources_and_receipt(phase: dict[str, Any]) -> dict[str, Any]:
    for name, expected in EXPECTED_INPUT_HASHES.items():
        if digest(HERE / name) != expected:
            fail(f"proof input changed: {name}")
    statement = load(HERE / "statement.json")
    if statement.get("canonical_formal_target", {}).get("elaborated_expression_sha256") != TARGET_SHA256:
        fail("canonical target fingerprint changed")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    if registry.get("root_obligation_id") != "M0110-ROOT":
        fail("obligation root changed")
    if registry.get("denominator_sha256") != REGISTRY_DENOMINATOR:
        fail("obligation denominator changed")
    if graphs.get("registry_denominator_sha256") != REGISTRY_DENOMINATOR:
        fail("typed-graph denominator changed")
    if len(registry.get("obligations", [])) != 23:
        fail("obligation count changed")
    boundary = graphs.get("closure_boundary", {})
    if boundary.get("root_closed") is not False:
        fail("typed graph falsely closes the root")
    if boundary.get("minimal_open_proof_cut_set") != [
        "M0110-S-SEMANTIC", "M0110-T-VANISHING"
    ]:
        fail("typed graph root cut set changed")

    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        source = (HERE / name).read_text(encoding="utf-8")
        if PROHIBITED.search(strip_comments_and_strings(source)):
            fail(f"prohibited proof or trust construct in {name}")
    proof_source = (HERE / "Proof.lean").read_text(encoding="utf-8")
    for marker in (
        "theorem kodairaVanishingTarget_of_vanishing",
        "KodairaVanishingTarget.{u} := by",
        "exact vanishing k D hD",
        "#print sorries kodairaVanishingTarget_of_vanishing",
        "#print axioms kodairaVanishingTarget_of_vanishing",
    ):
        if marker not in proof_source:
            fail(f"conditional assembly body is missing marker: {marker}")

    receipt = load(HERE / "proof-receipt.json")
    required_fields = {
        pointer.split("/")[-1]
        for pointer in phase.get("phase_receipt_required_fields", [])
        if pointer.count("/") == 1
    }
    if not required_fields <= set(receipt):
        fail("proof receipt omits contract-required fields")
    for field, expected in (
        ("schema_version", "stage1-node-receipt/1.0"),
        ("item_id", ITEM),
        ("theorem_id", THEOREM),
        ("phase", "proof"),
        ("intent", "prove"),
        ("base_revision", BASE_REVISION),
        ("base_tree", BASE_TREE),
        ("support_state", "provisional_worker_selftest"),
        ("proposed_state", "[_]"),
        ("verdict", "blocked"),
    ):
        if receipt.get(field) != expected:
            fail(f"proof receipt field {field} changed")
    if receipt.get("accepted") is not False or phase.get("raw_blocked_can_close_phase") is not False:
        fail("blocked proof receipt overstates acceptance")
    if receipt.get("selftest_status") != "passed":
        fail("proof receipt self-test is not passing")
    commands = receipt.get("selftest_result", {}).get("commands")
    if not isinstance(commands, list) or not commands:
        fail("proof receipt lacks exact self-test commands")
    if receipt.get("selftest_result", {}).get("exit_code") != 0:
        fail("proof receipt self-test exit changed")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("proof receipt crosses a terminal boundary")
    if receipt.get("canonical_target") != "Stage1Instances.THMM0110.KodairaVanishingTarget":
        fail("canonical target identity changed")
    if receipt.get("exact_declarations") != EXACT_DECLARATIONS:
        fail("exact declaration inventory changed")
    if receipt.get("closed_obligation_ids") != ["M0110-T-ASSEMBLE"]:
        fail("conditional assembly obligation inventory changed")
    if receipt.get("accepted_closed_obligation_ids") != []:
        fail("proof receipt invents accepted obligation closure")
    if receipt.get("remaining_root_cut_set") != [
        "M0110-S-SEMANTIC", "M0110-T-VANISHING"
    ]:
        fail("proof receipt root cut set changed")
    body = receipt.get("proof_body", {})
    if body.get("source") != f"Stage1_Instances/{THEOREM}/Proof.lean":
        fail("proof body source path changed")
    if body.get("source_sha256") != digest(HERE / "Proof.lean"):
        fail("proof body source binding changed")
    if body.get("root_kernel_closed") is not False:
        fail("proof body falsely closes the root")

    inputs = receipt.get("inputs", {})
    if "provider_material" in inputs:
        fail("proof receipt claims provider material despite no reuse")
    expected_bindings = {
        "proof_sources": [{
            "path": f"Stage1_Instances/{THEOREM}/Proof.lean",
            "sha256": digest(HERE / "Proof.lean"),
            "git_blob": git("hash-object", "--no-filters", f"Stage1_Instances/{THEOREM}/Proof.lean"),
        }],
        "dependency_reuse_ledger": {
            "path": f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
            "sha256": digest(HERE / "dependency-reuse-ledger.json"),
            "git_blob": git("hash-object", "--no-filters", f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json"),
        },
        "proof_blocker": {
            "path": f"Stage1_Instances/{THEOREM}/proof-blocker.json",
            "sha256": digest(HERE / "proof-blocker.json"),
            "git_blob": git("hash-object", "--no-filters", f"Stage1_Instances/{THEOREM}/proof-blocker.json"),
        },
        "proof_validation": {
            "path": f"Stage1_Instances/{THEOREM}/proof-validation.md",
            "sha256": digest(HERE / "proof-validation.md"),
            "git_blob": git("hash-object", "--no-filters", f"Stage1_Instances/{THEOREM}/proof-validation.md"),
        },
    }
    for field, expected in expected_bindings.items():
        if inputs.get(field) != expected:
            fail(f"proof receipt input binding changed: {field}")
    validator_binding = inputs.get("validator_candidate")
    if validator_binding != {
        "path": f"Stage1_Instances/{THEOREM}/check_proof.py",
        "sha256": digest(HERE / "check_proof.py"),
        "git_blob": git("hash-object", "--no-filters", f"Stage1_Instances/{THEOREM}/check_proof.py"),
        "existed_at_base": False,
        "current_claim_selection_eligible": False,
    }:
        fail("proof receipt validator binding changed")
    result = receipt.get("result", {})
    expected_result_fields = {
        "exit_code": 0,
        "semantic_verdict": "blocked",
        "phase_predicate_proven": False,
        "phase_accepted": False,
        "blocked": True,
        "root_kernel_closed": False,
        "accepted_closed_obligation_ids": [],
        "provisionally_closed_obligation_ids": ["M0110-T-ASSEMBLE"],
        "open_obligations": 16,
        "observed_axioms": ["propext", "Classical.choice", "Quot.sound"],
        "placeholder_scan": "pass",
        "stale_inputs": [],
        "audit_complete": False,
        "theorem_complete": False,
        "statement_olean_sha256": STATEMENT_OLEAN_SHA256,
        "proof_olean_sha256": PROOF_OLEAN_SHA256,
    }
    if result != expected_result_fields:
        fail("proof receipt result changed")
    return receipt


def verify_worker_packet(receipt: dict[str, Any]) -> None:
    packet = load(ROOT / ".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }:
        fail("worker packet fields changed")
    if packet.get("item_id") != ITEM or packet.get("state") != "[_]":
        fail("worker packet identity or state changed")
    if packet.get("base_revision") != BASE_REVISION:
        fail("worker packet base changed")
    if set(packet.get("changed_paths", [])) != CHANGED_PATHS:
        fail("worker packet changed-path inventory is incomplete")
    if packet.get("commands") != receipt.get("selftest_result", {}).get("commands"):
        fail("worker packet commands disagree with proof receipt")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet failures disagree with proof receipt")
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    if actual_changed != CHANGED_PATHS:
        fail(f"worktree delta disagrees with worker packet: {sorted(actual_changed)}")
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            fail(f"invalid text encoding or final newline: {relative}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            fail(f"trailing whitespace: {relative}")


def verify() -> None:
    _, phase = verify_authorities()
    verify_ledger()
    receipt = verify_sources_and_receipt(phase)
    verify_worker_packet(receipt)
    _, lean_output, olean_hashes = lean_replay()
    if olean_hashes != f"{STATEMENT_OLEAN_SHA256}:{PROOF_OLEAN_SHA256}":
        fail("trust-zero Lean output hashes changed")
    axiom_match = re.search(
        r"'Stage1Instances\.THMM0110\.Proof\."
        r"kodairaVanishingTarget_of_vanishing' depends on axioms: "
        r"\[(?P<axioms>.*?)\]",
        lean_output,
        flags=re.DOTALL,
    )
    if axiom_match is None:
        fail("missing conditional assembly axiom report")
    observed_axioms = set(
        re.findall(r"[A-Za-z][A-Za-z0-9_.]*", axiom_match.group("axioms"))
    )
    if observed_axioms != {"propext", "Classical.choice", "Quot.sound"}:
        fail("unexpected conditional assembly axiom profile")
    if "Declarations are sorry-free!" not in lean_output:
        fail("missing machine-derived no-sorry report")


def semantic_result(*, passed: bool, message: str) -> dict[str, Any]:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "proof",
        "status": "blocked" if passed else "failed",
        "verdict": "blocked" if passed else "repair_required",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": (
            "P04-KERNEL/M0110-T-VANISHING" if passed else "P01-ARTIFACTS"
        ),
        "open_obligations": 16,
        "stale_inputs": [],
        "blocked": passed,
        "message": message,
    }


def main() -> None:
    try:
        verify()
    except (AssertionError, KeyError, OSError, RuntimeError, ValueError) as error:
        result = semantic_result(
            passed=False, message=f"proof evidence replay failed: {error}"
        )
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    result = semantic_result(
        passed=True,
        message=(
            "The empty hard-parent closure, sole weak shared group, conditional "
            "assembly body, source hygiene, and trust-zero Lean replay passed; "
            "semantic transport and premise-free Kodaira vanishing remain open."
        ),
    )
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
