#!/usr/bin/env python3
"""Fail-closed source and provenance checks for S56-M-0319-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0319-PROOF"
THEOREM = "THM-M-0319"
TARGET_EXPRESSION_SHA256 = (
    "2e4dc02230de7a1c08fdf4a19ef0ec1da107297972dee0e85d893bdb33d6a514"
)
REGISTRY_DENOMINATOR_SHA256 = (
    "9d15b5eafa794b7f3cc1e83d4006447c90a75f8d8175bbaeb4b50fe8306ccee8"
)


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    value: dict[str, object] = {}
    for key, item in pairs:
        assert key not in value, ("duplicate JSON key", key)
        value[key] = item
    return value


def load(path: Path) -> dict:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
    )
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def strip_lean_comments_and_strings(source: str) -> str:
    """Erase nested comments, line comments, and string/char contents."""
    out: list[str] = []
    i = 0
    block_depth = 0
    in_string = False
    in_char = False
    escaped = False
    while i < len(source):
        pair = source[i:i + 2]
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


manifest = load(HERE / "vendor-manifest.json")
statement = load(HERE / "statement.json")
registry = load(HERE / "obligation-registry.json")
execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
receipt = load(HERE / "proof-receipt.json") if (HERE / "proof-receipt.json").exists() else None

item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item["theorem_id"] == THEOREM and item["execution_rank"] == 685
assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
assert item["depends_on"] == ["S56-M-0319-OBLIGATION_TREE"]
assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
predecessor = next(
    row for row in execution["items"] if row["id"] == "S56-M-0319-OBLIGATION_TREE"
)
assert predecessor["state"] == "[_]"

assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
    TARGET_EXPRESSION_SHA256
)
assert registry["root_obligation_id"] == "M0319-ROOT"
assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256

assert manifest["schema_version"] == "stage1-vendored-source-closure/1.0"
assert manifest["item_id"] == ITEM and manifest["theorem_id"] == THEOREM
assert manifest["license"]["spdx"] == "MIT"
assert manifest["license"]["sha256"] == sha256(HERE / "Vendor/LICENSE")
assert manifest["closure"]["module_count"] == len(manifest["files"]) == 3

actual_vendor_sources = {
    path.relative_to(HERE / "Vendor").as_posix()
    for path in (HERE / "Vendor").rglob("*.lean")
}
assert actual_vendor_sources == {row["path"] for row in manifest["files"]}
for row in manifest["files"]:
    path = HERE / "Vendor" / row["path"]
    assert sha256(path) == row["vendored_sha256"], row["path"]
    assert path.stat().st_size == row["vendored_bytes"], row["path"]

lean_files = [HERE / "Proof.lean"] + [
    HERE / "Vendor" / row["path"] for row in manifest["files"]
]
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
required_fragments = (
    "import Statement",
    "import Gametheory.Brouwer",
    "theorem exists_simplex_approximation",
    "hcompact.finite_cover_balls hdelta",
    "exists_continuous_sum_one_of_isOpen_isCompact",
    "obtain ⟨a, ha⟩ := Brouwer g hgcont",
    "theorem exactFixedPoint",
    "hcompact.exists_isMinOn",
    "theorem brouwerFixedPoint : BrouwerFixedPointTarget",
)
for fragment in required_fragments:
    assert fragment in proof, fragment
assert "THM_M_0318" not in proof
assert "harfe" not in proof.lower()

if receipt is not None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert receipt["base_revision"] == git("rev-parse", "HEAD")
    assert receipt["base_tree"] == git("rev-parse", "HEAD^{tree}")
    assert receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    assert receipt["proof_body"]["vendor_manifest_sha256"] == sha256(
        HERE / "vendor-manifest.json"
    )
    assert receipt["inputs"]["build_vendor_manifest_sha256"] == sha256(
        HERE / "build_vendor_manifest.py"
    )
    assert receipt["inputs"]["check_proof_py_sha256"] == sha256(
        HERE / "check_proof.py"
    )
    assert receipt["inputs"]["check_proof_sh_sha256"] == sha256(
        HERE / "check_proof.sh"
    )
    assert receipt["inputs"]["vendor_provenance_sha256"] == sha256(
        HERE / "VENDOR_PROVENANCE.md"
    )
    input_paths = {
        "blueprint_sha256": ROOT / "Docs/Stage1_Blueprint_rev-5.6.md",
        "execution_dag_sha256": ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "target_manifest_sha256": ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        "execution_skill_sha256": ROOT / "skills/execute-stage1-rev56/SKILL.md",
        "statement_sha256": HERE / "Statement.lean",
        "obligation_tree_sha256": HERE / "ObligationTree.lean",
        "obligation_registry_sha256": HERE / "obligation-registry.json",
        "typed_graphs_sha256": HERE / "typed-graphs.json",
        "anchor_audit_sha256": HERE / "anchor-audit.json",
        "lean_toolchain_sha256": ROOT / "Formalizations/Lean/lean-toolchain",
        "lake_manifest_sha256": ROOT / "Formalizations/Lean/lake-manifest.json",
    }
    for key, path in input_paths.items():
        assert receipt["inputs"][key] == sha256(path), key
    assert receipt["exact_declarations"] == [
        "Stage1Instances.THM_M_0319.exists_simplex_approximation",
        "Stage1Instances.THM_M_0319.hasApproximateFixedPoints",
        "Stage1Instances.THM_M_0319.exactFixedPoint",
        "Stage1Instances.THM_M_0319.brouwerFixedPoint",
    ]
    assert receipt["terminal_external_declarations"] == [
        "IndexedLOrder.Scarf",
        "IndexedLOrder.GiComponentStructure_holds",
        "Brouwer",
    ]
    assert receipt["validation_action"]["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["graph_reconciliation_pending"]["required"] is True
    assert receipt["structured_recipe"]["network_policy"].startswith(
        "no network operation required or observed"
    )
    assert receipt["result"]["root_kernel_inhabitant_observed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False

if "--require-receipt" in sys.argv:
    assert receipt is not None, "proof-receipt.json is required"

print(
    "PASS THM-M-0319 proof sources: exact target, MIT vendor closure, "
    "placeholder-free local bridge"
)
