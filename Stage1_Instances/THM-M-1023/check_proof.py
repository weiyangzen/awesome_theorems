#!/usr/bin/env python3
"""Fail-closed source, provenance, and receipt checks for S56-M-1023-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1023-PROOF"
THEOREM = "THM-M-1023"
BASE = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
MATHLIB_REV = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
UPSTREAM_REV = "93b635fba23398bfb1f0db8d220f88172f6900b6"
UPSTREAM_ARCHIVE_SHA256 = "585b9255907bc5db4c44f010acf98f7a9d608eea1d845b93f6938ff2437e4621"
UPSTREAM_ARCHIVE_URL = (
    "https://api.github.com/repos/slink/LeanLevy/tarball/"
    "93b635fba23398bfb1f0db8d220f88172f6900b6"
)
TARGET_EXPRESSION_SHA256 = (
    "f84253c83a8c31d9b77246bc0b3eef7715b0d0a04b707bb91cd5c329fdde1a2f"
)
UPSTREAM_MANIFEST_SHA256 = (
    "addd91a5dfdc2d6eef6b10bdd220914d4d49d266d2ff5e4f76fbe4ba0a1c6a92"
)
UPSTREAM_CONCAT_SHA256 = (
    "74e551bd8ffae5aefe530b1fd15912940ecd6dfe74eb1ff23c011a5909e7aa9e"
)


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    value = {}
    for key, item in pairs:
        assert key not in value, ("duplicate JSON key", key)
        value[key] = item
    return value


def load(path: Path) -> dict:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
    )
    assert isinstance(value, dict)
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

assert manifest["schema_version"] == "stage1-vendored-source-closure/1.0"
assert receipt["schema_version"] == "stage1-node-receipt/1.0"
assert manifest["item_id"] == receipt["item_id"] == ITEM
assert manifest["theorem_id"] == receipt["theorem_id"] == THEOREM
assert manifest["upstream"]["revision"] == UPSTREAM_REV
assert manifest["upstream"]["source_archive_url"] == UPSTREAM_ARCHIVE_URL
assert manifest["upstream"]["source_archive_sha256"] == UPSTREAM_ARCHIVE_SHA256
assert manifest["upstream"]["upstream_toolchain"] == "leanprover/lean4:v4.29.0-rc3"
assert manifest["upstream"]["upstream_mathlib_revision"] == (
    "8e096f85f9401f2c359b6708199c0402a980d921"
)
assert manifest["compatibility"]["target_mathlib_revision"] == MATHLIB_REV
assert manifest["compatibility"]["normalized_patch_sha256"] == (
    "ee3fcdea45ff454fe2aab4886881136af66070659c91a4b010a37964d95d3c84"
)
assert manifest["closure"]["upstream_manifest_sha256"] == UPSTREAM_MANIFEST_SHA256
assert manifest["closure"]["upstream_concat_sha256"] == UPSTREAM_CONCAT_SHA256
assert len(manifest["files"]) == 20
assert manifest["closure"]["module_count"] == 20
assert manifest["closure"]["vendored_bytes"] == 727852
assert manifest["closure"]["line_count"] == 13536
assert manifest["license"]["sha256"] == sha(HERE / "Vendor/LICENSE")

actual_vendor_sources = {
    path.relative_to(HERE / "Vendor").as_posix()
    for path in (HERE / "Vendor").rglob("*.lean")
}
assert actual_vendor_sources == {row["path"] for row in manifest["files"]}
actual_vendor_files = {
    path.relative_to(HERE / "Vendor").as_posix()
    for path in (HERE / "Vendor").rglob("*") if path.is_file()
}
assert actual_vendor_files == actual_vendor_sources | {"LICENSE"}
assert manifest["license"] == {
    "spdx": "MIT",
    "path": "Vendor/LICENSE",
    "sha256": "9ccb61ce372d47010507d876144053d40f49203851663956ae8c46e469dbfe79",
}

upstream_concat = hashlib.sha256()
upstream_lines: list[bytes] = []
vendored_concat = hashlib.sha256()
for row in manifest["files"]:
    path = HERE / "Vendor" / row["path"]
    assert path.is_file(), row["path"]
    assert sha(path) == row["vendored_sha256"], row["path"]
    assert path.stat().st_size == row["vendored_bytes"], row["path"]
    data = path.read_bytes()
    vendored_concat.update(data)
    if row["compatibility_transform"] is None:
        assert row["upstream_sha256"] == row["vendored_sha256"]
        upstream_data = data
    else:
        old = row["compatibility_transform"]["from"].encode()
        new = row["compatibility_transform"]["to"].encode()
        assert data.count(new) == 1, row["path"]
        upstream_data = data.replace(new, old)
        assert sha(path) != row["upstream_sha256"]
    assert hashlib.sha256(upstream_data).hexdigest() == row["upstream_sha256"]
    upstream_concat.update(upstream_data)
    upstream_lines.append(
        f"{row['upstream_sha256']}  {row['path']}\n".encode("utf-8")
    )

assert upstream_concat.hexdigest() == manifest["closure"]["upstream_concat_sha256"]
assert vendored_concat.hexdigest() == manifest["closure"]["vendored_concat_sha256"]
assert hashlib.sha256(b"".join(upstream_lines)).hexdigest() == (
    manifest["closure"]["upstream_manifest_sha256"]
)

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
for required in (
    "import Statement",
    "import LeanLevy.Levy.LevyKhintchineUniqueness",
    "theorem infinitelyDivisibleIffLevyKhintchine :",
    "InfinitelyDivisibleIffLevyKhintchine := by",
    "#print sorries infinitelyDivisibleIffLevyKhintchine",
    "#print axioms infinitelyDivisibleIffLevyKhintchine",
):
    assert required in proof, required
for declaration in (
    "ProbabilityTheory.levyKhintchine_representation",
    "ProbabilityTheory.levyKhintchine_converse",
    "ProbabilityTheory.existsUnique_levyKhintchineTriple",
):
    assert f"#print sorries {declaration}" in proof
    assert f"#print axioms {declaration}" in proof

assert registry["root_obligation_id"] == "M1023-ROOT"
assert registry["denominator_sha256"] == (
    "d4c7d2a1d47477fc812ed85f49f768034a99424755d90cb4de202a112a80c825"
)
assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == sha(HERE / "anchor-audit.json")
assert graphs["closure_boundary"]["root_closed"] is False

item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item["theorem_id"] == THEOREM
assert item["phase"] == "proof" and item["layer"] == 4
assert item["state"] in {"[ ]", "[_]"}
assert item["depends_on"] == ["S56-M-1023-OBLIGATION_TREE"]
assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

assert receipt["item_id"] == ITEM and receipt["base_revision"] == BASE
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
assert receipt["canonical_target"] == (
    "Stage1Instances.THM_M_1023.InfinitelyDivisibleIffLevyKhintchine"
)
assert receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION_SHA256
assert receipt["covered_obligation_ids"] == ["M1023-ROOT"]
assert receipt["kernel_inhabited_obligation_ids_observed"] == ["M1023-ROOT"]
assert receipt["closed_obligation_ids_proposed"] == []
assert receipt["accepted_closed_obligation_ids"] == []
assert receipt["closure_candidate_after_master_reconciliation"] == ["M1023-ROOT"]
assert receipt["accepted_receipt_ids"] == []
assert receipt["graph_reconciliation_pending"]["unreconciled_obligation_ids"]
assert receipt["proof_body"]["source_sha256"] == sha(HERE / "Proof.lean")
assert receipt["inputs"]["check_proof_py_sha256"] == sha(Path(__file__))
assert receipt["inputs"]["statement_sha256"] == sha(HERE / "Statement.lean")
assert receipt["inputs"]["obligation_tree_sha256"] == sha(HERE / "ObligationTree.lean")
assert receipt["inputs"]["obligation_registry_sha256"] == sha(
    HERE / "obligation-registry.json"
)
assert receipt["inputs"]["typed_graphs_sha256"] == sha(HERE / "typed-graphs.json")
assert receipt["inputs"]["anchor_audit_sha256"] == sha(HERE / "anchor-audit.json")
assert receipt["inputs"]["check_proof_sh_sha256"] == sha(HERE / "check_proof.sh")
assert receipt["inputs"]["build_vendor_manifest_sha256"] == sha(
    HERE / "build_vendor_manifest.py"
)
assert receipt["inputs"]["proof_validation_sha256"] == sha(HERE / "proof-validation.md")
assert receipt["inputs"]["lake_manifest_sha256"] == sha(
    ROOT / "Formalizations/Lean/lake-manifest.json"
)
assert receipt["inputs"]["lean_toolchain_sha256"] == sha(
    ROOT / "Formalizations/Lean/lean-toolchain"
)
assert receipt["proof_body"]["vendor_manifest_sha256"] == sha(HERE / "vendor-manifest.json")
assert receipt["proof_body"]["upstream_revision"] == UPSTREAM_REV
assert receipt["proof_body"]["upstream_archive_url"] == UPSTREAM_ARCHIVE_URL
assert receipt["proof_body"]["upstream_archive_sha256"] == UPSTREAM_ARCHIVE_SHA256
assert receipt["proof_body"]["vendored_module_count"] == 20
assert receipt["proof_body"]["license_sha256"] == sha(HERE / "Vendor/LICENSE")
assert receipt["result"]["root_kernel_inhabitant_observed"] is True
assert receipt["result"]["accepted_root_closed"] is False
assert receipt["result"]["theorem_complete"] is False
assert re.fullmatch(r"[0-9a-f]{64}", receipt["validation_action"]["stdout_sha256"])
assert receipt["validation_action"]["log_sha256"] == (
    receipt["validation_action"]["stdout_sha256"]
)
assert subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
).strip() == BASE
assert subprocess.check_output(
    ["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True
).strip() == receipt["base_tree"]

mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "rev-parse", "HEAD"], text=True
).strip() == MATHLIB_REV
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "rev-parse", "HEAD^{tree}"], text=True
).strip() == MATHLIB_TREE
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "status", "--short"], text=True
) == ""

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    selftest = load(selftest_path)
    assert set(selftest) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
    assert selftest["base_revision"] == BASE
    assert selftest["changed_paths"] == receipt["changed_paths"]
    assert selftest["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changes = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == set(selftest["changed_paths"]), (
        actual_changes,
        set(selftest["changed_paths"]),
    )

print("PASS THM-M-1023 proof phase: exact pinned-external root checked")
print(f"proof source sha256: {sha(HERE / 'Proof.lean')}")
print("accepted state unchanged; M0-P proposal is pending master acceptance")
