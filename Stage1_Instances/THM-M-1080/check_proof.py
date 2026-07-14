#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-1080-PROOF.

This checker intentionally does not elaborate Lean itself.  `check_proof.sh`
owns the isolated trust-zero replay; this file checks that its claimed sources,
frozen inputs, provisional receipt, dependency pins, and optional worker packet
remain mutually consistent.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ITEM = "S56-M-1080-PROOF"
THEOREM = "THM-M-1080"
BASE_REVISION = "fb0fd5be494d0813177dbdc959ec911d69a72015"
BASE_TREE = "f6d39faae5fb024a71ee786e7a6b017d335841cd"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
REGISTRY_DENOMINATOR_SHA256 = (
    "869c1a9abe79908244280909afaadc8e84b294df0d6b1e290b81e5363243df14"
)
CANONICAL_TARGET = "Stage1Instances.THM_M_1080.Statement"
CANONICAL_EXPRESSION_SHA256 = (
    "af69d1d82ed31033201ff05a06f14f6fe200307a16bd3538f34ab56d4fd0d350"
)
ALLOWED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]

PROVISIONAL_IDS = {
    "M1080-ROOT",
    "M1080-S-DEFINITIONS",
    "M1080-S-SCOPE",
    "M1080-S-BOUNDARY",
    "M1080-S-FOUNDATION",
    "M1080-N-INCREMENTS",
    "M1080-N-TELESCOPE",
    "M1080-C-EXPONENTIAL",
    "M1080-L-COND-HOEFFDING",
    "M1080-L-MGF-ITERATE",
    "M1080-L-MARKOV",
    "M1080-L-OPTIMIZE",
    "M1080-T-POSITIVE",
    "M1080-T-ZERO",
    "M1080-T-ASSEMBLE",
}

EXACT_DECLARATIONS = {
    "Stage1Instances.THM_M_1080.ObligationTree.azumaUpperTail_of_threshold_packages",
    "Stage1Instances.THM_M_1080.Proof.sum_increment_eq_sub",
    "Stage1Instances.THM_M_1080.Proof.exp_secant_bound",
    "Stage1Instances.THM_M_1080.Proof.condExp_exp_increment_le",
    "Stage1Instances.THM_M_1080.Proof.exp_endpoint_integrable",
    "Stage1Instances.THM_M_1080.Proof.exp_increment_sum_integral_le",
    "Stage1Instances.THM_M_1080.Proof.positiveThreshold",
    "Stage1Instances.THM_M_1080.Proof.zeroThreshold",
    "Stage1Instances.THM_M_1080.Proof.azumaUpperTail",
    "Stage1Instances.THM_M_1080.ExactRoot.positiveThresholdPackage",
    "Stage1Instances.THM_M_1080.ExactRoot.zeroThresholdPackage",
    "Stage1Instances.THM_M_1080.ExactRoot.azumaUpperTail_exact",
}

EXPECTED_BODY_MAP = {
    "M1080-ROOT": ["ExactRoot.azumaUpperTail_exact"],
    "M1080-S-DEFINITIONS": ["Proof.squaredBoundSum", "ExactRoot.azumaUpperTail_exact"],
    "M1080-S-SCOPE": ["ExactRoot.azumaUpperTail_exact"],
    "M1080-S-BOUNDARY": ["Proof.positiveThreshold", "Proof.zeroThreshold"],
    "M1080-S-FOUNDATION": [
        "trust-zero axiom reports for the exact root and supporting declarations"
    ],
    "M1080-N-INCREMENTS": [
        "Proof.condExp_exp_increment_le",
        "Proof.exp_increment_sum_integral_le",
    ],
    "M1080-N-TELESCOPE": ["Proof.sum_increment_eq_sub"],
    "M1080-C-EXPONENTIAL": [
        "Proof.exp_secant_bound",
        "Proof.exp_endpoint_integrable",
    ],
    "M1080-L-COND-HOEFFDING": ["Proof.condExp_exp_increment_le"],
    "M1080-L-MGF-ITERATE": ["Proof.exp_increment_sum_integral_le"],
    "M1080-L-MARKOV": ["Proof.positiveThreshold"],
    "M1080-L-OPTIMIZE": ["Proof.positiveThreshold"],
    "M1080-T-POSITIVE": [
        "Proof.positiveThreshold",
        "ExactRoot.positiveThresholdPackage",
    ],
    "M1080-T-ZERO": ["Proof.zeroThreshold", "ExactRoot.zeroThresholdPackage"],
    "M1080-T-ASSEMBLE": [
        "ObligationTree.azumaUpperTail_of_threshold_packages",
        "ExactRoot.azumaUpperTail_exact",
    ],
}

EXPECTED_CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-1080/ExactRoot.lean",
    "Stage1_Instances/THM-M-1080/Proof.lean",
    "Stage1_Instances/THM-M-1080/check_proof.py",
    "Stage1_Instances/THM-M-1080/check_proof.sh",
    "Stage1_Instances/THM-M-1080/proof-receipt.json",
    "Stage1_Instances/THM-M-1080/proof-validation.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL THM-M-1080 proof check: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def command(*argv: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        fail(
            f"command failed ({result.returncode}): {' '.join(argv)}\n"
            f"{result.stdout}{result.stderr}"
        )
    return result.stdout


def locate() -> tuple[Path, Path]:
    script_parent = Path(__file__).resolve().parent
    if (script_parent / "Proof.lean").is_file():
        target = script_parent
        root = target.parents[1]
    else:
        root_text = command("git", "rev-parse", "--show-toplevel", cwd=Path.cwd()).strip()
        root = Path(root_text).resolve()
        target = root / "Stage1_Instances" / THEOREM
    require(target.is_dir(), f"missing target directory: {target}")
    return root, target


def sha256(path: Path) -> str:
    require(path.is_file(), f"missing required file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load JSON object {path}: {error}")
    require(isinstance(value, dict), f"JSON root is not an object: {path}")
    return value


def lean_code_without_comments_or_strings(source: str) -> str:
    """Remove nested Lean comments and string contents before token scanning."""

    output: list[str] = []
    index = 0
    block_depth = 0
    line_comment = False
    in_string = False
    escaped = False
    while index < len(source):
        pair = source[index : index + 2]
        char = source[index]
        if line_comment:
            if char == "\n":
                line_comment = False
                output.append("\n")
            else:
                output.append(" ")
            index += 1
            continue
        if block_depth:
            if pair == "/-":
                block_depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                block_depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
            continue
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            output.append("\n" if char == "\n" else " ")
            index += 1
            continue
        if pair == "--":
            line_comment = True
            output.extend("  ")
            index += 2
        elif pair == "/-":
            block_depth = 1
            output.extend("  ")
            index += 2
        elif char == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    require(block_depth == 0, "unterminated block comment in Lean source")
    require(not in_string, "unterminated string in Lean source")
    return "".join(output)


def check_lean_sources(target: Path) -> None:
    proof_path = target / "Proof.lean"
    exact_path = target / "ExactRoot.lean"
    proof = proof_path.read_text(encoding="utf-8")
    exact = exact_path.read_text(encoding="utf-8")

    import re

    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(?:axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    for path, source in ((proof_path, proof), (exact_path, exact)):
        code = lean_code_without_comments_or_strings(source)
        match = forbidden.search(code)
        require(match is None, f"prohibited Lean construct in {path.name}: {match and match.group(0)!r}")

    proof_markers = (
        "theorem exp_secant_bound",
        "theorem sum_increment_eq_sub",
        "theorem condExp_exp_increment_le",
        "C + r * Y omega",
        "condExp_add",
        "condExp_smul",
        "theorem exp_endpoint_integrable",
        "theorem exp_increment_sum_integral_le",
        "condExp_mul_of_stronglyMeasurable_left",
        "theorem positiveThreshold",
        "by_cases hS0 : S = 0",
        "ProbabilityTheory.measure_ge_le_exp_mul_mgf",
        "theorem zeroThreshold",
        "theorem azumaUpperTail",
        "#print axioms condExp_exp_increment_le",
        "#print axioms exp_increment_sum_integral_le",
        "#print axioms azumaUpperTail",
    )
    exact_markers = (
        "import Statement",
        "import ObligationTree",
        "import Proof",
        "theorem positiveThresholdPackage",
        "ObligationTree.PositiveThresholdPackage",
        "Proof.positiveThreshold",
        "theorem zeroThresholdPackage",
        "ObligationTree.ZeroThresholdPackage",
        "Proof.zeroThreshold",
        "theorem azumaUpperTail_exact",
        "Stage1Instances.THM_M_1080.Statement",
        "ObligationTree.azumaUpperTail_of_threshold_packages",
        "#print axioms azumaUpperTail_exact",
    )
    for marker in proof_markers:
        require(marker in proof, f"Proof.lean missing marker: {marker}")
    for marker in exact_markers:
        require(marker in exact, f"ExactRoot.lean missing marker: {marker}")

    shell = (target / "check_proof.sh").read_text(encoding="utf-8")
    for marker in (
        "set -euo pipefail",
        "lake env which lean",
        "lake env printenv LEAN_PATH",
        "LEAN_NUM_THREADS=1",
        "--trust=0",
        "Statement.olean",
        "ObligationTree.olean",
        "Proof.olean",
        "ExactRoot.olean",
        "azumaUpperTail_exact",
        "check_proof.py",
    ):
        require(marker in shell, f"check_proof.sh missing fail-closed marker: {marker}")
    forbidden_shell = re.compile(
        r"\blake[ \t]+(?:update|build|upgrade|clean)\b|"
        r"\bgit[ \t]+(?:clone|fetch|pull|submodule[ \t]+update)\b|"
        r"\b(?:curl|wget|ssh|scp|rsync)[ \t]+"
    )
    match = forbidden_shell.search(shell)
    require(match is None, f"mutable/network operation in check_proof.sh: {match and match.group(0)!r}")

    validation = (target / "proof-validation.md").read_text(encoding="utf-8")
    for marker in (
        ITEM,
        BASE_REVISION,
        "azumaUpperTail_exact",
        "propext",
        "Classical.choice",
        "Quot.sound",
        "master acceptance",
        "theorem completion",
    ):
        require(marker.lower() in validation.lower(),
                f"proof-validation.md missing evidence/boundary marker: {marker}")


def check_frozen_inputs(root: Path, target: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    statement = load_object(target / "statement.json")
    registry = load_object(target / "obligation-registry.json")
    graphs = load_object(target / "typed-graphs.json")
    execution = load_object(root / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    formal = statement.get("canonical_formal_target")
    require(isinstance(formal, dict), "statement canonical_formal_target is absent")
    require(formal.get("declaration_or_expression") == CANONICAL_TARGET, "canonical target drift")
    require(
        formal.get("elaborated_expression_sha256") == CANONICAL_EXPRESSION_SHA256,
        "canonical expression fingerprint drift",
    )
    require(
        formal.get("statement_file_sha256") == sha256(target / "Statement.lean"),
        "statement metadata/source hash mismatch",
    )

    require(registry.get("root_obligation_id") == "M1080-ROOT", "registry root drift")
    require(
        registry.get("denominator_sha256") == REGISTRY_DENOMINATOR_SHA256,
        "registry denominator drift",
    )
    require(
        registry.get("frozen_against_statement_sha256") == sha256(target / "Statement.lean"),
        "registry statement freeze mismatch",
    )
    require(
        registry.get("frozen_against_anchor_audit_sha256") == sha256(target / "anchor-audit.json"),
        "registry anchor freeze mismatch",
    )
    denominators = registry.get("frozen_denominators")
    require(isinstance(denominators, dict), "registry frozen denominator payload missing")
    require(
        set(denominators.get("required_machine", [])) == PROVISIONAL_IDS,
        "required-machine denominator differs from the 15 proof obligations",
    )
    frozen_status = registry.get("status_observed_after_freeze")
    require(isinstance(frozen_status, dict), "registry frozen status missing")
    require(
        frozen_status.get("closed_obligations") == ["M1080-T-ASSEMBLE"],
        "worker rewrote or drifted frozen pre-proof closure",
    )
    require(frozen_status.get("root_machine_debt") == "M3", "frozen root debt drift")

    closure = graphs.get("closure_boundary")
    require(isinstance(closure, dict), "typed-graph closure boundary missing")
    require(closure.get("closed_obligations") == ["M1080-T-ASSEMBLE"], "typed closure drift")
    require(closure.get("root_closed") is False, "frozen typed graph improperly closes root")
    require(closure.get("theorem_complete") is False, "frozen typed graph claims completion")
    require(graphs.get("registry_denominator_sha256") == REGISTRY_DENOMINATOR_SHA256,
            "typed graph denominator mismatch")

    items = execution.get("items")
    require(isinstance(items, list), "execution DAG items missing")
    matching = [row for row in items if isinstance(row, dict) and row.get("id") == ITEM]
    require(len(matching) == 1, "execution DAG proof item missing or duplicated")
    item = matching[0]
    require(item.get("theorem_id") == THEOREM, "execution theorem mismatch")
    require(item.get("phase") == "proof" and item.get("layer") == 4, "execution phase/layer drift")
    require(item.get("state") in {"[ ]", "[_]"}, "worker observed invalid authoritative state")
    require(item.get("depends_on") == ["S56-M-1080-OBLIGATION_TREE"], "proof dependency drift")
    require(item.get("owned_paths") == [f"Stage1_Instances/{THEOREM}"], "ownership drift")

    # Proof workers must leave these architecture/authority artifacts untouched.
    frozen_paths = (
        "Statement.lean",
        "ObligationTree.lean",
        "obligation-registry.json",
        "typed-graphs.json",
        "validation-specs.json",
        "anchor-audit.json",
    )
    for name in frozen_paths:
        result = subprocess.run(
            ["git", "diff", "--quiet", "--", str((target / name).relative_to(root))],
            cwd=root,
            check=False,
        )
        require(result.returncode == 0, f"frozen input was modified: {name}")
    return statement, registry


def check_receipt(root: Path, target: Path, registry: dict[str, Any]) -> dict[str, Any]:
    receipt = load_object(target / "proof-receipt.json")
    require(receipt.get("schema_version") == "stage1-node-receipt/1.0", "receipt schema drift")
    require(
        receipt.get("receipt_id") == "S56-M-1080-PROOF-WORKER-20260715",
        "receipt ID mismatch",
    )
    require(receipt.get("item_id") == ITEM and receipt.get("theorem_id") == THEOREM,
            "receipt identity mismatch")
    require(receipt.get("phase") == "proof", "receipt phase mismatch")
    require(receipt.get("intent") == "prove", "receipt intent mismatch")
    require(receipt.get("base_revision") == BASE_REVISION, "receipt base revision mismatch")
    require(receipt.get("base_tree") == BASE_TREE, "receipt base tree mismatch")
    require(receipt.get("support_state") == "provisional_worker_selftest", "receipt support state")
    require(receipt.get("proposed_state") == "[_]", "receipt proposal is not [_]")
    require(receipt.get("accepted") is False, "worker receipt cannot be accepted")
    require(receipt.get("canonical_target") == CANONICAL_TARGET, "receipt canonical target drift")
    require(
        receipt.get("canonical_target_expression_sha256") == CANONICAL_EXPRESSION_SHA256,
        "receipt canonical expression hash drift",
    )
    require(
        receipt.get("registry_denominator_sha256") == REGISTRY_DENOMINATOR_SHA256,
        "receipt denominator mismatch",
    )
    require(set(receipt.get("exact_declarations", [])) == EXACT_DECLARATIONS,
            "receipt exact-declaration inventory mismatch")
    require(
        set(receipt.get("provisionally_closed_proof_obligation_ids", [])) == PROVISIONAL_IDS,
        "receipt provisional proof-closure set mismatch",
    )
    require(receipt.get("accepted_closed_obligation_ids") == [],
            "worker receipt claims accepted obligation closure")
    require(receipt.get("changed_paths") == EXPECTED_CHANGED_PATHS,
            "receipt changed_paths is not the exact scoped inventory")

    body = receipt.get("proof_body")
    require(isinstance(body, dict), "receipt proof_body missing")
    require(body.get("source") == f"Stage1_Instances/{THEOREM}/Proof.lean",
            "receipt Proof source path mismatch")
    require(body.get("source_sha256") == sha256(target / "Proof.lean"),
            "receipt Proof source hash mismatch")
    require(body.get("exact_root_source") == f"Stage1_Instances/{THEOREM}/ExactRoot.lean",
            "receipt exact-root source path mismatch")
    require(body.get("exact_root_sha256") == sha256(target / "ExactRoot.lean"),
            "receipt exact-root source hash mismatch")
    require(
        body.get("terminal_declaration") ==
        "Stage1Instances.THM_M_1080.ExactRoot.azumaUpperTail_exact",
        "receipt terminal declaration mismatch",
    )

    body_map = receipt.get("obligation_body_map")
    require(isinstance(body_map, dict), "receipt obligation_body_map missing")
    require(body_map == EXPECTED_BODY_MAP, "receipt obligation/body witness map drift")

    inputs = receipt.get("inputs")
    require(isinstance(inputs, dict), "receipt input hashes missing")
    input_files = {
        "statement_sha256": "Statement.lean",
        "obligation_tree_sha256": "ObligationTree.lean",
        "obligation_registry_sha256": "obligation-registry.json",
        "typed_graphs_sha256": "typed-graphs.json",
        "validation_specs_sha256": "validation-specs.json",
        "anchor_audit_sha256": "anchor-audit.json",
        "check_proof_sh_sha256": "check_proof.sh",
        "check_proof_py_sha256": "check_proof.py",
        "proof_validation_sha256": "proof-validation.md",
    }
    for key, name in input_files.items():
        require(inputs.get(key) == sha256(target / name), f"receipt input hash mismatch: {name}")

    environment = receipt.get("environment")
    require(isinstance(environment, dict), "receipt environment missing")
    require(environment.get("mathlib_revision") == MATHLIB_REVISION, "receipt mathlib revision")
    require(environment.get("mathlib_tree") == MATHLIB_TREE, "receipt mathlib tree")
    require(environment.get("lean_executable_sha256") == LEAN_EXECUTABLE_SHA256,
            "receipt Lean executable hash")
    require(environment.get("lean_toolchain_file_sha256") == LEAN_TOOLCHAIN_SHA256,
            "receipt toolchain-file hash")
    require(environment.get("lake_manifest_sha256") == LAKE_MANIFEST_SHA256,
            "receipt manifest hash")

    result = receipt.get("result")
    require(isinstance(result, dict), "receipt result missing")
    require(result.get("exit_code") == 0, "receipt replay did not exit zero")
    require(result.get("axioms") == ALLOWED_AXIOMS, "receipt axiom set mismatch")
    require(result.get("root_kernel_closed") is True, "receipt does not kernel-close exact root")
    require(result.get("accepted_root_closed") is False, "receipt claims accepted root closure")
    require(result.get("audit_complete") is False, "proof receipt claims audit completion")
    require(result.get("theorem_complete") is False, "proof receipt claims theorem completion")

    before = receipt.get("root_vector_before")
    proposed = receipt.get("root_vector_proposed")
    accepted = receipt.get("root_vector_accepted")
    require(before == {"H": "H2", "M": "M3", "R": "R3"}, "receipt prior vector drift")
    require(proposed == {"H": "H2", "M": "M0-L", "R": "R3"}, "receipt proposal drift")
    require(accepted == before, "worker receipt changed accepted debt vector")
    require(receipt.get("accepted_receipt_ids") == [], "worker claims an accepted receipt")
    require(receipt.get("content_addressed_receipt_ids") == [],
            "mutable worker receipt claims content-addressed acceptance")
    require(receipt.get("revocation_state") == "unaccepted_current_worker_evidence",
            "receipt revocation/support state drift")
    require(isinstance(receipt.get("invalidation_inputs"), list)
            and receipt["invalidation_inputs"], "receipt invalidation inputs missing")

    failures = receipt.get("known_failures")
    require(isinstance(failures, list) and all(isinstance(x, str) for x in failures) and failures,
            "receipt known_failures missing")
    failure_text = " ".join(failures).lower()
    for term in (
        "master acceptance",
        "frozen",
        "source",
        "readability",
        "provenance",
        "hermetic",
        "independent",
        "validation",
        "release",
        "theorem completion",
    ):
        require(term in failure_text, f"receipt failure boundary omits {term!r}")

    require(registry.get("status_observed_after_freeze", {}).get("root_machine_debt") == "M3",
            "receipt check observed rewritten frozen status")
    return receipt


def check_environment(root: Path, receipt: dict[str, Any]) -> None:
    lean_dir = root / "Formalizations" / "Lean"
    mathlib = lean_dir / ".lake" / "packages" / "mathlib"
    require(mathlib.is_dir(), "canonical pinned mathlib artifact is missing")
    require(command("git", "-C", str(mathlib), "rev-parse", "HEAD").strip() == MATHLIB_REVISION,
            "installed mathlib revision drift")
    require(command("git", "-C", str(mathlib), "rev-parse", "HEAD^{tree}").strip() == MATHLIB_TREE,
            "installed mathlib tree drift")
    require(command("git", "-C", str(mathlib), "status", "--short") == "",
            "installed mathlib worktree is dirty")
    require(sha256(lean_dir / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256,
            "Lean toolchain file drift")
    require(sha256(lean_dir / "lake-manifest.json") == LAKE_MANIFEST_SHA256,
            "Lake manifest drift")
    lean = Path(command("lake", "env", "which", "lean", cwd=lean_dir).strip())
    require(sha256(lean) == LEAN_EXECUTABLE_SHA256, "Lean executable drift")

    recipe = receipt.get("recipe")
    require(isinstance(recipe, dict), "receipt recipe missing")
    argv = recipe.get("argv")
    require(argv == ["bash", f"Stage1_Instances/{THEOREM}/check_proof.sh"],
            "receipt replay command drift")
    require(recipe.get("mutable_dependency_operations") is False,
            "receipt permits mutable dependency operations")


def check_worker_packet(root: Path, receipt: dict[str, Any]) -> None:
    packet_path = root / ".stage1-worker-selftest.json"
    require(packet_path.is_file(), "required worker self-test packet is missing")
    packet = load_object(packet_path)
    require(set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }, "worker packet keys mismatch")
    require(packet.get("item_id") == ITEM and packet.get("state") == "[_]",
            "worker packet identity/state mismatch")
    require(packet.get("base_revision") == BASE_REVISION, "worker packet base mismatch")
    require(packet.get("changed_paths") == EXPECTED_CHANGED_PATHS,
            "worker packet changed_paths mismatch")
    require(packet.get("known_failures") == receipt.get("known_failures"),
            "worker packet failure boundary differs from receipt")
    commands = packet.get("commands")
    require(isinstance(commands, list) and commands, "worker packet commands missing")
    for row in commands:
        require(isinstance(row, dict) and set(row) == {"command", "exit_code", "result"},
                "worker packet command row schema mismatch")
        require(isinstance(row["command"], str) and row["command"],
                "worker packet command is empty")
        require(row["exit_code"] == 0, "worker packet records a failed final command")
        require(isinstance(row["result"], str) and row["result"],
                "worker packet command result is empty")
    require(isinstance(packet.get("output_summary"), str) and packet["output_summary"],
            "worker packet output summary missing")

    status = command(
        "git", "status", "--short", "--untracked-files=all", cwd=root
    )
    actual: set[str] = set()
    for line in status.splitlines():
        require(len(line) >= 4, f"unparseable git status line: {line!r}")
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path == "Formalizations/Lean/.lake":
            continue
        actual.add(path)
    require(actual == set(EXPECTED_CHANGED_PATHS),
            f"scoped changed paths differ: actual={sorted(actual)!r}")


def main() -> None:
    root, target = locate()
    require(command("git", "rev-parse", "HEAD", cwd=root).strip() == BASE_REVISION,
            "workspace HEAD differs from receipt base")
    require(command("git", "rev-parse", "HEAD^{tree}", cwd=root).strip() == BASE_TREE,
            "workspace base tree differs from receipt base")
    check_lean_sources(target)
    _, registry = check_frozen_inputs(root, target)
    receipt = check_receipt(root, target, registry)
    check_environment(root, receipt)
    check_worker_packet(root, receipt)

    print("PASS THM-M-1080 proof packet: exact arbitrary-space Azuma root is kernel-closed")
    print(f"Proof.lean sha256: {sha256(target / 'Proof.lean')}")
    print(f"ExactRoot.lean sha256: {sha256(target / 'ExactRoot.lean')}")
    print("accepted state unchanged; provisional proof awaits master acceptance and validation")


if __name__ == "__main__":
    main()
