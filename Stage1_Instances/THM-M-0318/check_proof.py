#!/usr/bin/env python3
"""Fail-closed source, provenance, and receipt checks for S56-M-0318-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0318-PROOF"
THEOREM = "THM-M-0318"
BASE_REVISION = "557b928b377b386864527c9fb4831d45857837aa"
BASE_TREE = "e677879a6eb4cb9d6795ba1bd78726af06ab9465"
TARGET_EXPRESSION_SHA256 = (
    "2605ac76f3d50dddcc135d3094639fbed3de58a10b26a8f9eeb504101e556b5f"
)
INVENTORY_SHA256 = (
    "57d77a8fccc8308a704f1185c92057a17791da515e45325179aa81d000376f87"
)
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
UPSTREAM_REVISION = "c02205edf347ad45f0d62db85497598ba2c4291e"
UPSTREAM_TREE = "5dda2d10fdd4a0db1aba85f1fa1a7acc509f80e4"
UPSTREAM_ARCHIVE_SHA256 = (
    "8591fadd6737d75b921eee27dc9d85d5d9f040a83ad7dcb2d81dc208754c04cd"
)
COMPATIBILITY_PATCH_SHA256 = (
    "39fff43f92e646d6365f6279fd565d0d2d7b873f0922a1df9165f880a36b8790"
)
PROOF_OBLIGATION_IDS = [
    "M0318-ROOT",
    "M0318-C",
    "M0318-C-NET",
    "M0318-C-MAP",
    "M0318-B-BROUWER",
    "M0318-L-APPROX",
    "M0318-L-LIMIT",
    "M0318-L-CONT",
    "M0318-T-COMPOSE",
]


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


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


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
receipt = load(HERE / "proof-receipt.json")
statement = load(HERE / "statement.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
packet = load(ROOT / ".stage1-worker-selftest.json")

assert git("rev-parse", "HEAD") == BASE_REVISION
assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item["theorem_id"] == THEOREM and item["execution_rank"] == 684
assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
assert item["depends_on"] == ["S56-M-0318-OBLIGATION_TREE"]
assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
predecessor = next(
    row for row in execution["items"] if row["id"] == "S56-M-0318-OBLIGATION_TREE"
)
assert predecessor["state"] == "[_]"

assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
    TARGET_EXPRESSION_SHA256
)
assert registry["root_obligation_id"] == "M0318-ROOT"
assert registry["frozen_denominators"]["inventory_sha256"] == INVENTORY_SHA256
assert graphs["theorem_complete"] is False

assert manifest["schema_version"] == "stage1-vendored-source-closure/1.0"
assert manifest["item_id"] == receipt["item_id"] == ITEM
assert manifest["theorem_id"] == receipt["theorem_id"] == THEOREM
assert manifest["upstream"]["revision"] == UPSTREAM_REVISION
assert manifest["upstream"]["source_tree"] == UPSTREAM_TREE
assert manifest["upstream"]["source_archive_sha256"] == UPSTREAM_ARCHIVE_SHA256
assert manifest["closure"]["normalized_compatibility_patch_sha256"] == (
    COMPATIBILITY_PATCH_SHA256
)
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
    "import ObligationTree",
    "import Gametheory.Brouwer",
    "theorem exists_simplex_approximation",
    "hcompact.finite_cover_balls hdelta",
    "exists_continuous_sum_one_of_isOpen_isCompact",
    "obtain ⟨a, ha⟩ := Brouwer g hgcont",
    "theorem approximationEngine : ApproximationEngine.{u}",
    "theorem compactLimitEngine : CompactLimitEngine.{u}",
    "compose_schauder approximationEngine compactLimitEngine",
    "theorem schauderFixedPoint : SchauderFixedPointTarget.{u}",
)
for fragment in required_fragments:
    assert fragment in proof, fragment
declarations = (
    "IndexedLOrder.Scarf",
    "IndexedLOrder.GiComponentStructure_holds",
    "Brouwer",
    "Stage1Instances.THM_M_0318.exists_simplex_approximation",
    "Stage1Instances.THM_M_0318.hasApproximateFixedPoints",
    "Stage1Instances.THM_M_0318.approximationEngine",
    "Stage1Instances.THM_M_0318.compactLimitEngine",
    "Stage1Instances.THM_M_0318.exactSchauderTarget",
    "Stage1Instances.THM_M_0318.schauderFixedPoint",
)
for declaration in declarations:
    assert f"assert_no_sorry {declaration}" in proof
    assert f"#print sorries {declaration}" in proof
    assert f"#print axioms {declaration}" in proof

assert receipt["schema_version"] == "stage1-node-receipt/1.0"
assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
assert receipt["base_tree"] == BASE_TREE
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
assert receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION_SHA256
assert receipt["registry_inventory_sha256"] == INVENTORY_SHA256
assert receipt["covered_obligation_ids"] == PROOF_OBLIGATION_IDS
assert receipt["kernel_inhabited_obligation_ids_observed"] == PROOF_OBLIGATION_IDS
assert receipt["closed_obligation_ids_proposed"] == []
assert receipt["accepted_closed_obligation_ids"] == []
assert receipt["closure_candidate_after_master_reconciliation"] == PROOF_OBLIGATION_IDS
assert receipt["accepted_receipt_ids"] == []
assert receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
assert receipt["proof_body"]["vendor_manifest_sha256"] == sha256(
    HERE / "vendor-manifest.json"
)
for key, filename in (
    ("statement_sha256", "Statement.lean"),
    ("obligation_tree_sha256", "ObligationTree.lean"),
    ("obligation_registry_sha256", "obligation-registry.json"),
    ("typed_graphs_sha256", "typed-graphs.json"),
    ("anchor_audit_sha256", "anchor-audit.json"),
    ("build_vendor_manifest_sha256", "build_vendor_manifest.py"),
    ("check_proof_py_sha256", "check_proof.py"),
    ("check_proof_sh_sha256", "check_proof.sh"),
    ("proof_validation_sha256", "proof-validation.md"),
    ("vendor_provenance_sha256", "VENDOR_PROVENANCE.md"),
):
    assert receipt["inputs"][key] == sha256(HERE / filename), key
assert receipt["inputs"]["lake_manifest_sha256"] == sha256(
    ROOT / "Formalizations/Lean/lake-manifest.json"
)
assert receipt["inputs"]["lean_toolchain_sha256"] == sha256(
    ROOT / "Formalizations/Lean/lean-toolchain"
)
assert receipt["result"]["root_kernel_inhabitant_observed"] is True
assert receipt["result"]["accepted_root_closed"] is False
assert receipt["result"]["audit_complete"] is False
assert receipt["result"]["theorem_complete"] is False
assert receipt["validation_action"]["observed_axioms"] == [
    "propext", "Classical.choice", "Quot.sound"
]
assert re.fullmatch(r"[0-9a-f]{64}", receipt["validation_action"]["stdout_sha256"])
assert receipt["validation_action"]["stdout_sha256"] == (
    receipt["validation_action"]["log_sha256"]
)

mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
assert git("status", "--porcelain=v1", cwd=mathlib) == ""

assert set(packet) == {
    "item_id", "changed_paths", "commands", "output_summary",
    "base_revision", "known_failures", "state",
}
assert packet["item_id"] == ITEM and packet["state"] == "[_]"
assert packet["changed_paths"] == receipt["changed_paths"]
assert packet["known_failures"] == receipt["known_failures"]
status = subprocess.check_output(
    ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
)
actual_changes = {
    line[3:]
    for line in status.splitlines()
    if line[3:] != "Formalizations/Lean/.lake"
}
assert actual_changes == set(packet["changed_paths"]), (
    actual_changes,
    set(packet["changed_paths"]),
)

for relative in receipt["changed_paths"]:
    if relative == ".stage1-worker-selftest.json":
        continue
    data = (ROOT / relative).read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

print("PASS THM-M-0318 proof phase: exact pinned-external Schauder root checked")
print(f"proof source sha256: {sha256(HERE / 'Proof.lean')}")
print("accepted state unchanged; graph reconciliation and validation remain pending")
