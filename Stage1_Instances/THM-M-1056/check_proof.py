#!/usr/bin/env python3
"""Fail-closed source, provenance, and receipt checks for S56-M-1056-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


if not __debug__:
    raise SystemExit("check_proof.py must not run with assertions disabled")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1056-PROOF"
THEOREM = "THM-M-1056"
BASE_REVISION = "118d66d1986768cd9a00e661ccf6447c26a53efb"
BASE_TREE = "e31babc8fcb7426673e5d6c0a4a884af2cd737e8"
TARGET_EXPRESSION_SHA256 = (
    "8e1a96a304ce3dd43838f934406d58ac3594b9d34c6e1617461abc17e65d403b"
)
REGISTRY_DENOMINATOR_SHA256 = (
    "5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828"
)
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
WRAPPER_MODULES = (
    "CoordinateBridge.lean",
    "IntegrabilityBridge.lean",
    "CocycleBridge.lean",
    "GrowthBridge.lean",
    "ExternalInvoke.lean",
    "ConditionalWrapper.lean",
    "M1056ProjectionBridge.lean",
    "ConcreteProjectionPackage.lean",
    "Proof.lean",
)


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        assert key not in value, ("duplicate JSON key", key)
        value[key] = item
    return value


def load(path: Path) -> dict[str, object]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
    )
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def strip_lean_comments_and_strings(source: str) -> str:
    """Erase nested comments, line comments, and string/character contents."""
    out: list[str] = []
    i = 0
    block_depth = 0
    in_string = False
    in_char = False
    escaped = False
    while i < len(source):
        pair = source[i : i + 2]
        char = source[i]
        if block_depth:
            if pair == "/-":
                block_depth += 1
                out.extend("  ")
                i += 2
            elif pair == "-/":
                block_depth -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if char == "\n" else " ")
                i += 1
            continue
        if in_string or in_char:
            out.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif in_string and char == '"':
                in_string = False
            elif in_char and char == "'":
                in_char = False
            i += 1
            continue
        if pair == "/-":
            block_depth = 1
            out.extend("  ")
            i += 2
        elif pair == "--":
            end = source.find("\n", i)
            if end == -1:
                out.extend(" " * (len(source) - i))
                i = len(source)
            else:
                out.extend(" " * (end - i))
                i = end
        elif char == '"':
            in_string = True
            out.append(" ")
            i += 1
        elif char == "'" and i + 2 < len(source) and source[i + 2] == "'":
            in_char = True
            out.append(" ")
            i += 1
        else:
            out.append(char)
            i += 1
    assert block_depth == 0 and not in_string and not in_char
    return "".join(out)


statement = load(HERE / "statement.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
manifest = load(HERE / "vendor-manifest.json")
execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
receipt_path = HERE / "proof-receipt.json"
receipt = load(receipt_path) if receipt_path.exists() else None

assert git("rev-parse", "HEAD") == BASE_REVISION
assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item["theorem_id"] == THEOREM and item["execution_rank"] == 248
assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
assert item["depends_on"] == ["S56-M-1056-OBLIGATION_TREE"]
assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
predecessor = next(
    row for row in execution["items"]
    if row["id"] == "S56-M-1056-OBLIGATION_TREE"
)
assert predecessor["state"] == "[_]"

formal_target = statement["canonical_formal_target"]
assert formal_target["declaration_or_expression"] == (
    "Stage1Instances.THM_M_1056.OseledetsMultiplicativeErgodicTarget"
)
assert formal_target["elaborated_expression_sha256"] == TARGET_EXPRESSION_SHA256
assert formal_target["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert registry["root_obligation_id"] == "M1056-ROOT"
assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == sha256(
    HERE / "anchor-audit.json"
)
assert len(registry["obligations"]) == 19
assert graphs["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["remaining_root_cut_set"] == ["M1056-T-CORE"]

assert manifest["schema_version"] == "stage1-vendored-source-closure/1.0"
assert manifest["item_id"] == ITEM and manifest["theorem_id"] == THEOREM
assert manifest["upstream"]["revision"] == (
    "ed3fa6b8a30594eeb791160563942ba115581aa0"
)
assert manifest["upstream"]["source_archive_sha256"] == (
    "3c0ef177500430ab55950061cfd73991347f5336b5b3d5032ffe46ac56009a52"
)
assert manifest["target_environment"]["mathlib_revision"] == MATHLIB_REVISION
assert manifest["target_environment"]["mathlib_tree"] == MATHLIB_TREE
assert manifest["license"]["spdx"] == "Apache-2.0"
assert manifest["license"]["sha256"] == sha256(
    HERE / "External/Oseledets/LICENSE"
)
assert manifest["terminal"]["declaration"] == "ErgodicTheory.oseledets_splitting"
assert manifest["closure"] == {
    "module_count": 62,
    "vendored_bytes": 1504769,
    "vendored_lines": 27472,
    "source_only": True,
    "stored_olean_count": 0,
    "stored_log_count": 0,
}
subprocess.run(
    [sys.executable, str(HERE / "check_vendor.py")],
    cwd=ROOT,
    check=True,
)

vendor_sources = [
    HERE / "External/Oseledets" / row["path"] for row in manifest["files"]
]
lean_files = [HERE / "Statement.lean"] + [HERE / name for name in WRAPPER_MODULES]
lean_files.extend(vendor_sources)
assert len(lean_files) == 72
for path in lean_files:
    stripped = strip_lean_comments_and_strings(path.read_text(encoding="utf-8"))
    forbidden = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    match = forbidden.search(stripped)
    assert match is None, (path, match.group(0) if match else None)

proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
for fragment in (
    "import ConcreteProjectionPackage",
    "theorem oseledetsMultiplicativeErgodic :",
    "OseledetsMultiplicativeErgodicTarget.{u, v} :=",
    "oseledets_multiplicative_ergodic_target",
    "theorem oseledetsMultiplicativeErgodicTarget :",
    "#print sorries oseledetsMultiplicativeErgodic",
    "#print axioms oseledetsMultiplicativeErgodic",
):
    assert fragment in proof, fragment

imports = {
    name: [
        line.removeprefix("import ")
        for line in (HERE / name).read_text(encoding="utf-8").splitlines()
        if line.startswith("import ")
    ]
    for name in WRAPPER_MODULES
}
assert imports["IntegrabilityBridge.lean"][0] == "CoordinateBridge"
assert imports["CocycleBridge.lean"][0] == "IntegrabilityBridge"
assert imports["GrowthBridge.lean"][0] == "CocycleBridge"
assert imports["ExternalInvoke.lean"] == [
    "GrowthBridge", "ErgodicTheory.TwoSided.SplittingAssembly"
]
assert imports["ConditionalWrapper.lean"] == ["ExternalInvoke", "Statement"]
assert imports["ConcreteProjectionPackage.lean"] == [
    "ConditionalWrapper", "M1056ProjectionBridge"
]
assert imports["Proof.lean"] == ["ConcreteProjectionPackage"]

if receipt is not None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "proof" and receipt["intent"] == "prove"
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert receipt["kernel_inhabited_obligation_ids_observed"] == ["M1056-ROOT"]
    assert receipt["closed_obligation_ids_proposed"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["closure_candidate_after_master_reconciliation"] == [
        "M1056-ROOT"
    ]
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["graph_reconciliation_pending"]["required"] is True
    assert receipt["proof_body"]["root_source_sha256"] == sha256(HERE / "Proof.lean")
    assert receipt["proof_body"]["vendor_manifest_sha256"] == sha256(
        HERE / "vendor-manifest.json"
    )
    wrapper_hashes = receipt["proof_body"]["wrapper_source_sha256"]
    assert wrapper_hashes == {name: sha256(HERE / name) for name in WRAPPER_MODULES}
    expected_inputs = {
        "blueprint_sha256": ROOT / "Docs/Stage1_Blueprint_rev-5.6.md",
        "execution_dag_sha256": ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "target_manifest_sha256": ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        "execution_skill_sha256": ROOT / "skills/execute-stage1-rev56/SKILL.md",
        "statement_sha256": HERE / "Statement.lean",
        "obligation_tree_sha256": HERE / "ObligationTree.lean",
        "obligation_registry_sha256": HERE / "obligation-registry.json",
        "typed_graphs_sha256": HERE / "typed-graphs.json",
        "anchor_audit_sha256": HERE / "anchor-audit.json",
        "vendor_manifest_sha256": HERE / "vendor-manifest.json",
        "check_vendor_py_sha256": HERE / "check_vendor.py",
        "vendor_provenance_sha256": HERE / "VENDOR_PROVENANCE.md",
        "check_proof_py_sha256": HERE / "check_proof.py",
        "check_proof_sh_sha256": HERE / "check_proof.sh",
        "proof_validation_sha256": HERE / "proof-validation.md",
        "readme_sha256": HERE / "README.md",
        "lean_toolchain_sha256": ROOT / "Formalizations/Lean/lean-toolchain",
        "lake_manifest_sha256": ROOT / "Formalizations/Lean/lake-manifest.json",
    }
    for key, path in expected_inputs.items():
        assert receipt["inputs"][key] == sha256(path), key
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["environment"]["validation_trust_level"] == 0
    assert receipt["validation_action"]["exit_code"] == 0
    assert receipt["validation_action"]["external_module_count"] == 62
    assert receipt["validation_action"]["target_module_count"] == 10
    assert receipt["validation_action"]["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["validation_action"]["all_inspected_sorry_free"] is True
    assert receipt["historical_olean_ledger_replay"]["matched"] == 61
    assert receipt["historical_olean_ledger_replay"]["mismatched"] == 1
    assert receipt["result"] == {
        "root_kernel_inhabitant_observed": True,
        "accepted_root_closed": False,
        "accepted_state_changed": False,
        "audit_complete": False,
        "theorem_complete": False,
        "machine_debt_proposal": (
            "exact-root M0-L/M0-P candidate after graph/provenance "
            "reconciliation and master acceptance"
        ),
    }
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }

if "--require-receipt" in sys.argv:
    assert receipt is not None, "proof-receipt.json is required"

print(
    "PASS THM-M-1056 proof packet: exact root, 62-module Apache-2.0 "
    "source closure, placeholder-free coordinate/projection bridge"
)
