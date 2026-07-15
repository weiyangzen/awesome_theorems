#!/usr/bin/env python3
"""Fail-closed source, provenance, and packet checks for S56-M-0353-PROOF."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0353-PROOF"
THEOREM = "THM-M-0353"
BASE_REVISION = "48fb6596b1844f4183c411142415d872ff21e842"
BASE_TREE = "eb8dfff0e90b5ce5b11ac2096777060d62874064"

VENDOR_PATH = HERE / "Vendor/GaussianField/HermiteFunctions.lean"
LICENSE_PATH = HERE / "Vendor/LICENSE"
UPSTREAM_REPOSITORY = "mrdouglasny/gaussian-field"
UPSTREAM_REVISION = "d63a28568a75d99f6cb27af1f888a49a69855a66"
UPSTREAM_TREE = "7b2c1a97a992cacee49dcbd347a9d78d59fdc383"
UPSTREAM_PATH = "SchwartzNuclear/HermiteFunctions.lean"
UPSTREAM_BLOB = "077d911f5e26a11199bc0756f50a803a58490807"
UPSTREAM_SOURCE_SHA256 = "e25548a1e042a61b340e24931dc05fd49bcaa6cf1daf68c335859df58d3b3d49"
UPSTREAM_ARCHIVE_SHA256 = "3d0504de255e7684f9f7badebff98dcb05619dfe180dbfa56d55c94bcdc4961c"
LICENSE_SHA256 = "2d3b806e6fd270f11819d0f797f721747adb0d497760e1b9053b6cd1fae4cf54"
VENDOR_MANIFEST_SHA256 = "7fb077d8c7a26522e65b3c9237d8500be15be4ffc55cee8e0ba68f3b24a5ab7c"
VENDOR_PROVENANCE_SHA256 = "94d06437c58c3ff5a364001b50c53ae9ce1001525021c0dfef2eb7b22f5ea700"
BUILD_VENDOR_MANIFEST_SHA256 = "4af810edb20cc4e4916fe9c41a5bdcc87d6fde14215e041f7eaeb8833efc7c59"
CHECK_PROOF_SH_SHA256 = "1726c71d35d2dfd586e35acc95451eb4822df40dae392a9c8140c6b99b7fcabf"
PROOF_EXECUTION_SHA256 = "2d41b9f5d56a891093fbe31d0aa66ef62e462a2cf84c87f4097e215518ce2567"
PROOF_VALIDATION_SHA256 = "308f01ce1d528494234585eba92398735b5c046d42a0ff1b2deff7aeead0c68c"
LEGACY_VALIDATION_SHA256 = "3fcfdcfec915790974d8253a768eee862fffbd0679668d9fed7cdd1574e4aa40"

MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"

STATEMENT_SHA256 = "58416bc39074209c0d725fce0a9c0dbf09725d847e2be24a77ebaa73527e2d99"
OBLIGATION_TREE_SHA256 = "fdd4f947aea690c1cdbfaeb1dcbff9ded6476267163c31c28f85d0792ab0dfbc"
REGISTRY_SHA256 = "e87ac0a8bd1d6e1816f8816ec85d08e94686230e6afd00d294eca8f732bd6376"
GRAPHS_SHA256 = "868cdcbd5d6c2e049b21c8138016a96a0fdd1ba7e9eceba8ce5685032c3fc329"
ANCHOR_AUDIT_SHA256 = "468b16881b49a74d5b868a3b8600b5d5b8be2c923024056e9432a2497ec7ebfe"
TASK_DAG_SHA256 = "f663ea0e3293ca14da37e4f1339f81df3ba582d3d9ed1573dae89d3eee608a8e"
DENOMINATOR_SHA256 = "4516c92f499b2c9dfc0c2097d27d1a7eb177a4965b00d4b1dcf38456d8efd0f0"
CANONICAL_TARGET = "Stage1Instances.THM_M_0353.HermiteCompletenessTarget"

PROOF_MACHINE_IDS = {
    "M0353-ROOT",
    "M0353-T-ASSEMBLE",
    "M0353-P-MEMLP",
    "M0353-P-BASIS",
    "M0353-C-LP-VECTORS",
    "M0353-L-ORTHONORMAL",
    "M0353-L-DENSE",
    "M0353-C-HILBERT-BASIS",
    "M0353-L-GAUSSIAN-ORTH",
    "M0353-L-POLY-DENSE",
    "M0353-T-MEASURE",
    "M0353-S-NORMALIZATION",
    "M0353-X-HERMITE-POLY",
}
ASSURANCE_IDS = {"M0353-X-SOURCE", "M0353-X-TRUST", "M0353-X-PROVENANCE"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"expected JSON object: {path}"
    return value


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def owned_changed_paths(*, include_selftest: bool) -> set[str]:
    """Compute only this worker's owned Git delta, without parsing porcelain paths."""
    owner = f"Stage1_Instances/{THEOREM}"
    tracked = git_output("diff", "--name-only", "HEAD", "--", owner).splitlines()
    untracked = git_output(
        "ls-files", "--others", "--exclude-standard", "--", owner
    ).splitlines()
    changed = set(tracked) | set(untracked)
    if include_selftest and (ROOT / ".stage1-worker-selftest.json").is_file():
        changed.add(".stage1-worker-selftest.json")
    assert all(path.startswith(f"{owner}/") for path in changed if not path.startswith("."))
    return changed


def nested_get(value: dict[str, Any], *paths: tuple[str, ...]) -> Any:
    """Return the first present nested field, allowing stable receipt layout variants."""
    for path in paths:
        current: Any = value
        for key in path:
            if not isinstance(current, dict) or key not in current:
                break
            current = current[key]
        else:
            return current
    return None


def lean_code(source: str) -> str:
    """Blank Lean comments and literals while preserving newlines and token separation.

    Lean block comments nest. Raw strings have the form `r###"..."###`; ordinary
    strings and character literals support escapes. Keeping newlines lets the
    prohibited-declaration check retain its line-start semantics.
    """

    out = list(source)
    n = len(source)
    i = 0

    def blank(start: int, end: int) -> None:
        for index in range(start, end):
            if out[index] not in "\r\n":
                out[index] = " "

    while i < n:
        if source.startswith("--", i):
            end = source.find("\n", i + 2)
            if end < 0:
                end = n
            blank(i, end)
            i = end
            continue
        if source.startswith("/-", i):
            start = i
            depth = 1
            i += 2
            while i < n and depth:
                if source.startswith("/-", i):
                    depth += 1
                    i += 2
                elif source.startswith("-/", i):
                    depth -= 1
                    i += 2
                else:
                    i += 1
            assert depth == 0, "unterminated Lean block comment"
            blank(start, i)
            continue

        raw = re.match(r'r(#+)?"', source[i:])
        if raw:
            start = i
            hashes = raw.group(1) or ""
            i += raw.end()
            end_marker = '"' + hashes
            end = source.find(end_marker, i)
            assert end >= 0, "unterminated Lean raw string"
            i = end + len(end_marker)
            blank(start, i)
            continue

        is_char_start = source[i] == "'" and (
            i == 0 or not (source[i - 1].isalnum() or source[i - 1] in "_'?!")
        )
        if source[i] == '"' or is_char_start:
            start = i
            quote = source[i]
            i += 1
            escaped = False
            while i < n:
                char = source[i]
                i += 1
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == quote:
                    break
            else:
                raise AssertionError(f"unterminated Lean {quote} literal")
            blank(start, i)
            continue
        i += 1

    return "".join(out)


def assert_no_prohibited_source(path: Path) -> None:
    code = lean_code(path.read_text(encoding="utf-8"))
    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
        r"^[ \t]*(axiom|constant|opaque|unsafe)[ \t]+",
        re.MULTILINE,
    )
    match = prohibited.search(code)
    assert match is None, f"prohibited executable construct in {path}: {match.group(0)!r}"


def assert_markers(source: str, markers: tuple[str, ...], label: str) -> None:
    for marker in markers:
        assert marker in source, f"missing {label} marker: {marker}"


def check_vendor_manifest() -> dict[str, Any]:
    """Recompute the canonical vendor manifest in memory and compare exact bytes.

    Importing the target-local builder is safe here: its module body defines pure
    helpers only, and `build_manifest` reads and hashes files without writing.
    """
    builder_path = HERE / "build_vendor_manifest.py"
    manifest_path = HERE / "vendor-manifest.json"
    assert sha256(builder_path) == BUILD_VENDOR_MANIFEST_SHA256
    assert sha256(manifest_path) == VENDOR_MANIFEST_SHA256
    assert sha256(HERE / "VENDOR_PROVENANCE.md") == VENDOR_PROVENANCE_SHA256

    spec = importlib.util.spec_from_file_location("m0353_build_vendor_manifest", builder_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rebuilt = module.build_manifest()
    rendered = (json.dumps(rebuilt, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    assert manifest_path.read_bytes() == rendered, "vendor-manifest.json is noncanonical"

    manifest = load_json(manifest_path)
    assert manifest["schema_version"] == "stage1-vendored-source-closure/1.0"
    assert manifest["item_id"] == ITEM and manifest["theorem_id"] == THEOREM
    upstream = manifest["upstream"]
    assert upstream["project"] == UPSTREAM_REPOSITORY
    assert upstream["canonical_remote"] == f"https://github.com/{UPSTREAM_REPOSITORY}.git"
    assert upstream["revision"] == UPSTREAM_REVISION
    assert upstream["source_tree"] == UPSTREAM_TREE
    assert upstream["source_archive_sha256"] == UPSTREAM_ARCHIVE_SHA256
    assert upstream["toolchain"]["value"] == "leanprover/lean4:v4.30.0"
    assert upstream["lake_manifest"]["mathlib_revision"] == (
        "c5ea00351c28e24afc9f0f84379aa41082b1188f"
    )

    environment = manifest["target_environment"]
    assert environment["toolchain_sha256"] == TOOLCHAIN_SHA256
    assert environment["lake_manifest_sha256"] == LAKE_MANIFEST_SHA256
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert manifest["license"] == {
        "spdx": "Apache-2.0",
        "upstream_path": "LICENSE",
        "vendored_path": "Vendor/LICENSE",
        "git_blob_sha1": "94f474d4d34ef439ac1bb0f1961d5cc9e9096c7e",
        "sha256": LICENSE_SHA256,
        "bytes": 774,
        "lines": 17,
        "verbatim": True,
    }
    assert manifest["compatibility"] == {
        "source_transform_count": 0,
        "normalized_patch_sha256": hashlib.sha256(b"").hexdigest(),
        "semantic_scope": "none; source and license are byte-identical upstream copies",
        "path_relocation_only": True,
    }
    assert manifest["build_order"] == ["Vendor.GaussianField.HermiteFunctions"]
    assert len(manifest["files"]) == 1
    source = manifest["files"][0]
    assert source["upstream_path"] == UPSTREAM_PATH
    assert source["vendored_path"] == "Vendor/GaussianField/HermiteFunctions.lean"
    assert source["git_blob_sha1"] == UPSTREAM_BLOB
    assert source["upstream_sha256"] == source["vendored_sha256"] == UPSTREAM_SOURCE_SHA256
    assert source["bytes"] == VENDOR_PATH.stat().st_size == 99106
    assert source["lines"] == len(VENDOR_PATH.read_bytes().splitlines()) == 1859
    assert source["verbatim"] is True and source["compatibility_operations"] == []
    closure = manifest["closure"]
    assert closure["module_count"] == 1 and closure["source_bytes"] == 99106
    assert closure["external_dependencies"] == ["Mathlib"]
    assert closure["terminal_declarations"] == [
        "hermiteFunction_memLp", "hermiteFunction_orthonormal", "hermiteFunction_complete"
    ]
    return manifest


def check_sources() -> None:
    proof_path = HERE / "Proof.lean"
    assert sha256(VENDOR_PATH) == UPSTREAM_SOURCE_SHA256
    assert git_output("hash-object", str(VENDOR_PATH)) == UPSTREAM_BLOB
    assert sha256(LICENSE_PATH) == LICENSE_SHA256
    for path in (proof_path, VENDOR_PATH):
        assert_no_prohibited_source(path)

    vendor = VENDOR_PATH.read_text(encoding="utf-8")
    proof = proof_path.read_text(encoding="utf-8")
    assert_markers(
        vendor,
        (
            "Released under Apache 2.0 license as described in the file LICENSE.",
            "def hermiteFunctionNormConst (n : ℕ) : ℝ :=",
            "def hermiteFunction (n : ℕ) (x : ℝ) : ℝ :=",
            "theorem hermiteFunction_memLp (n : ℕ) :",
            "theorem hermiteFunction_orthonormal :",
            "private theorem hermiteFunction_complete_proof :",
            "theorem hermiteFunction_complete :",
            "hermiteFunction_complete_proof",
        ),
        "vendor",
    )
    assert_markers(
        proof,
        (
            "import ObligationTree",
            "import Vendor.GaussianField.HermiteFunctions",
            "import Mathlib.Util.AssertNoSorry",
            "import Mathlib.Util.PrintSorries",
            "theorem realHermiteNormalization_eq (n : Nat)",
            "theorem target_hermiteFunction_eq_ofReal (n : Nat) (x : Real)",
            "theorem target_hermiteFunction_memLp (n : Nat)",
            "theorem targetHermiteLp_orthonormal : Orthonormal Complex targetHermiteLp",
            "theorem targetHermiteLp_span_orthogonal_eq_bot",
            "HilbertBasis.mkOfOrthogonalEqBot",
            "theorem hermiteMemLpPackage_proof : HermiteMemLpPackage",
            "theorem hermiteBasisPackage_proof : HermiteBasisPackage",
            "theorem hermiteCompletenessTarget_proof : HermiteCompletenessTarget",
            "root_of_hermite_packages",
        ),
        "proof",
    )
    inspected = (
        "_root_.hermiteFunction_memLp",
        "_root_.hermiteFunction_orthonormal",
        "_root_.hermiteFunction_complete",
        "hermiteMemLpPackage_proof",
        "hermiteBasisPackage_proof",
        "hermiteCompletenessTarget_proof",
    )
    for declaration in inspected:
        assert f"assert_no_sorry {declaration}" in proof
        assert f"#print sorries {declaration}" in proof
        assert f"#print axioms {declaration}" in proof


def check_frozen_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    expected_hashes = {
        HERE / "Statement.lean": STATEMENT_SHA256,
        HERE / "ObligationTree.lean": OBLIGATION_TREE_SHA256,
        HERE / "obligation-registry.json": REGISTRY_SHA256,
        HERE / "typed-graphs.json": GRAPHS_SHA256,
        HERE / "anchor-audit.json": ANCHOR_AUDIT_SHA256,
        HERE / "task-dag.json": TASK_DAG_SHA256,
        LEAN_ROOT / "lean-toolchain": TOOLCHAIN_SHA256,
        LEAN_ROOT / "lake-manifest.json": LAKE_MANIFEST_SHA256,
    }
    for path, expected in expected_hashes.items():
        assert sha256(path) == expected, f"frozen input changed: {path}"

    execution = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM
    assert item["execution_rank"] == 846 and item["phase"] == "proof" and item["layer"] == 4
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0353-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    task_dag = load_json(HERE / "task-dag.json")
    task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert task["depends_on"] == item["depends_on"] and task["state"] == "open"
    assert task_dag["accepted_states"] == []

    registry = load_json(HERE / "obligation-registry.json")
    graphs = load_json(HERE / "typed-graphs.json")
    assert registry["theorem_id"] == THEOREM and graphs["theorem_id"] == THEOREM
    assert registry["root_obligation_id"] == "M0353-ROOT"
    assert graphs["root_node_id"] == "M0353-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert registry["frozen_against_anchor_audit_sha256"] == ANCHOR_AUDIT_SHA256

    registry_ids = {row["obligation_id"] for row in registry["obligations"]}
    graph_nodes = {row["obligation_id"] for row in graphs["nodes"]}
    assert registry_ids == graph_nodes == PROOF_MACHINE_IDS | ASSURANCE_IDS
    assert set(registry["frozen_denominators"]["required_machine"]) == (
        PROOF_MACHINE_IDS | {"M0353-X-TRUST"}
    )
    assert set(graphs["graphs"]) == {
        "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"
    }
    all_edge_ids: set[str] = set()
    for graph in graphs["graphs"].values():
        for edge in graph["edges"]:
            assert edge["from"] in registry_ids and edge["to"] in registry_ids
            assert edge["edge_id"] not in all_edge_ids
            all_edge_ids.add(edge["edge_id"])
    proof_edges = graphs["graphs"]["proof"]["edges"]
    reciprocal = {edge["edge_id"] for edge in proof_edges}
    assert all(edge.get("reciprocal_edge_id") in reciprocal for edge in proof_edges)
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "theorem_complete": False,
        "minimal_open_root_cut": ["M0353-P-MEMLP", "M0353-P-BASIS"],
    }
    return registry, graphs


def check_environment() -> None:
    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    mathlib = LEAN_ROOT / ".lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""
    lean = Path(
        subprocess.check_output(
            ["lake", "env", "which", "lean"], cwd=LEAN_ROOT, text=True
        ).strip()
    )
    assert lean.is_file() and sha256(lean) == LEAN_EXECUTABLE_SHA256


def check_receipt(registry: dict[str, Any], manifest: dict[str, Any]) -> None:
    receipt_path = HERE / "proof-receipt.json"
    if not receipt_path.exists():
        return
    receipt = load_json(receipt_path)
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt.get("phase", "proof") == "proof"
    assert receipt["base_revision"] == BASE_REVISION
    if "base_tree" in receipt:
        assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt.get("canonical_target", CANONICAL_TARGET) == CANONICAL_TARGET
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256

    inputs = receipt["inputs"]
    expected_inputs = (
        ("statement_sha256", STATEMENT_SHA256),
        ("obligation_tree_sha256", OBLIGATION_TREE_SHA256),
        ("obligation_registry_sha256", REGISTRY_SHA256),
        ("typed_graphs_sha256", GRAPHS_SHA256),
        ("anchor_audit_sha256", ANCHOR_AUDIT_SHA256),
        ("vendor_manifest_sha256", VENDOR_MANIFEST_SHA256),
        ("vendor_provenance_sha256", VENDOR_PROVENANCE_SHA256),
        ("build_vendor_manifest_py_sha256", BUILD_VENDOR_MANIFEST_SHA256),
        ("check_proof_sh_sha256", CHECK_PROOF_SH_SHA256),
        ("proof_execution_sha256", PROOF_EXECUTION_SHA256),
        ("proof_validation_sha256", PROOF_VALIDATION_SHA256),
        ("validation_sha256", LEGACY_VALIDATION_SHA256),
    )
    for key, expected in expected_inputs:
        assert inputs[key] == expected, key

    proof_body = receipt["proof_body"]
    assert nested_get(
        proof_body, ("source_sha256",), ("proof_sha256",), ("local_adapter_sha256",)
    ) == sha256(HERE / "Proof.lean")
    assert nested_get(
        proof_body, ("vendored_source_sha256",), ("vendor_source_sha256",)
    ) == UPSTREAM_SOURCE_SHA256
    assert nested_get(
        proof_body, ("upstream_repository",), ("vendor", "upstream_repository")
    ) == UPSTREAM_REPOSITORY
    assert nested_get(
        proof_body, ("upstream_revision",), ("vendor", "upstream_revision")
    ) == UPSTREAM_REVISION
    assert nested_get(proof_body, ("upstream_tree",), ("vendor", "upstream_tree")) == UPSTREAM_TREE
    assert nested_get(proof_body, ("upstream_path",), ("vendor", "upstream_path")) == UPSTREAM_PATH
    assert nested_get(
        proof_body, ("upstream_blob",), ("upstream_git_blob",), ("vendor", "upstream_blob")
    ) == UPSTREAM_BLOB
    archive = nested_get(
        proof_body, ("upstream_archive_sha256",), ("vendor", "upstream_archive_sha256")
    )
    assert archive == UPSTREAM_ARCHIVE_SHA256
    assert nested_get(proof_body, ("license",), ("vendor", "license")) == "Apache-2.0"
    assert nested_get(
        proof_body, ("license_sha256",), ("vendor", "license_sha256")
    ) == LICENSE_SHA256
    manifest_hash = nested_get(
        proof_body, ("vendor_manifest_sha256",), ("vendor", "manifest_sha256")
    )
    if manifest_hash is not None:
        assert manifest_hash == VENDOR_MANIFEST_SHA256
    source_count = nested_get(
        proof_body, ("vendored_module_count",), ("vendor", "module_count")
    )
    if source_count is not None:
        assert source_count == manifest["closure"]["module_count"] == 1

    result = receipt["result"]
    assert result["exit_code"] == 0 and result["root_kernel_closed"] is True
    assert result.get("accepted_root_closed", False) is False
    assert result["theorem_complete"] is False
    assert result["axioms"] == ["propext", "Classical.choice", "Quot.sound"]

    registry_ids = {row["obligation_id"] for row in registry["obligations"]}
    proposed = set(
        receipt.get("provisionally_closed_obligation_ids", receipt.get("covered_obligation_ids", []))
    )
    accepted = set(receipt.get("accepted_closed_obligation_ids", []))
    assert proposed <= registry_ids and accepted == set()
    fingerprints = receipt.get("obligation_statement_fingerprints", {})
    if fingerprints:
        expected = {row["obligation_id"]: row["statement_fingerprint"] for row in registry["obligations"]}
        assert set(fingerprints) <= registry_ids
        assert all(expected[key] == value for key, value in fingerprints.items())

    packet_path = ROOT / ".stage1-worker-selftest.json"
    if packet_path.exists():
        packet = load_json(packet_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["known_failures"] == receipt["known_failures"]
        assert isinstance(packet["commands"], list) and packet["commands"]
        assert isinstance(packet["output_summary"], str) and packet["output_summary"]
        actual_changes = owned_changed_paths(include_selftest=True)
        assert actual_changes == set(packet["changed_paths"]), (
            actual_changes, set(packet["changed_paths"])
        )
    else:
        assert set(receipt["changed_paths"]) == owned_changed_paths(include_selftest=False) | {
            ".stage1-worker-selftest.json"
        }


def lexer_selftest() -> None:
    sample = r'''
/- outer sorry /- nested axiom fake : False -/ admit -/
def apostrophe' : String := "sorry axiom unsafe"
def doubleApostrophe'' : Nat := 0
def question?' : Nat := 0
def bang!' : Nat := 0
def character : Char := '\''
def raw : String := r##"opaque extern native_decide"##
theorem clean : True := by trivial
'''
    code = lean_code(sample)
    assert "outer sorry" not in code and "nested axiom" not in code
    for identifier in ("apostrophe'", "doubleApostrophe''", "question?'", "bang!'"):
        assert identifier in code
    assert "theorem clean" in code
    assert "opaque extern native_decide" not in code

    for forbidden in (
        "theorem bad : True := by sorry\n",
        "axiom bad : False\n",
        "unsafe def bad : Nat := 0\n",
        "def bad : Nat := by native_decide\n",
    ):
        code = lean_code(forbidden)
        assert re.search(
            r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
            r"^[ \t]*(axiom|constant|opaque|unsafe)[ \t]+",
            code,
            re.MULTILINE,
        )


def main() -> None:
    lexer_selftest()
    check_environment()
    manifest = check_vendor_manifest()
    check_sources()
    registry, _ = check_frozen_inputs()
    check_receipt(registry, manifest)
    print("PASS THM-M-0353 proof source, provenance, frozen graph, and pin checks")
    print(f"vendor source sha256: {sha256(VENDOR_PATH)}; upstream blob: {UPSTREAM_BLOB}")
    print("accepted state unchanged; proof evidence remains provisional pending master acceptance")


if __name__ == "__main__":
    main()
