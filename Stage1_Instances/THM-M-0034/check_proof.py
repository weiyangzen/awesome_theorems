#!/usr/bin/env python3
"""Fail-closed source, provenance, kernel, and receipt checks for THM-M-0034."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations/Lean"
ITEM = "S56-M-0034-PROOF"
THEOREM = "THM-M-0034"
BASE_REVISION = "6ac589f0d8c5a9eeb726a1a05def7f9467ea2e2d"
BASE_TREE = "9e8c2b617c489611e447b350a4b4cf4aeff15f39"
TARGET_EXPRESSION_SHA256 = (
    "d80cc9860ed5a53c81a0851b4dc8e702aa5a23d448f373ae6d68ed0c9b5604b1"
)
REGISTRY_DENOMINATOR_SHA256 = (
    "0f1fd6b2f8450f934acd51372109d93d3b86bfc9ecaac8fe0f58bc566d7fb090"
)
UPSTREAM_REVISION = "51ed173b17b274e61f759556ab3e1c090267d1bd"
UPSTREAM_TREE = "264c487a24b2158bf8432459fd0b1e326acdf1eb"
UPSTREAM_ARCHIVE_SHA256 = (
    "ad8bd7662861ddf984f6c244f3b1d3eabbe4b0fd9b33f51dd85e2918d737babf"
)
SELECTED_EXTERNAL_REVISION = "e8d85a6f6fa210ba0be12bd02aa22009699f0c35"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LAKE_MANIFEST_SHA256 = (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)
LICENSE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
EXPECTED_BUILD_ORDER = [
    "Stage1_Instances.THM-M-0034.Vendor.QuillenSuslin.UnimodularVector.BivariatePolynomial",
    "Stage1_Instances.THM-M-0034.Vendor.QuillenSuslin.UnimodularVector.SuslinMonicPolynomialThm",
    "Stage1_Instances.THM-M-0034.Vendor.QuillenSuslin.UnimodularVector.Basic",
    "Stage1_Instances.THM-M-0034.Vendor.QuillenSuslin.UnimodularVector.PID",
    "Stage1_Instances.THM-M-0034.Vendor.QuillenSuslin.FiniteFreeResolution.Basic",
    "Stage1_Instances.THM-M-0034.Vendor.QuillenSuslin.FiniteFreeResolution.Polynomial",
    "Stage1_Instances.THM-M-0034.Vendor.QuillenSuslin.FiniteFreeResolution.StablyFree",
    "Stage1_Instances.THM-M-0034.Vendor.QuillenSuslin.MainTheorem",
]
FROZEN_PROOF_EDGES = {
    ("M0034-ROOT", "proof_requires", "M0034-T-ROOT"),
    ("M0034-T-ROOT", "composes", "M0034-ROOT"),
    ("M0034-T-ROOT", "proof_requires", "M0034-T-ADAPTER"),
    ("M0034-T-ADAPTER", "composes", "M0034-T-ROOT"),
    ("M0034-T-ADAPTER", "proof_requires", "M0034-X-EXTERNAL-BODY"),
    ("M0034-X-EXTERNAL-BODY", "composes", "M0034-T-ADAPTER"),
}
ALLOWED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]


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


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def strip_lean_comments_and_strings(source: str) -> str:
    """Erase nested comments, line comments, and string/character contents."""
    out: list[str] = []
    index = 0
    block_depth = 0
    in_string = False
    in_char = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if block_depth:
            if pair == "/-":
                block_depth += 1
                out.extend("  ")
                index += 2
            elif pair == "-/":
                block_depth -= 1
                out.extend("  ")
                index += 2
            else:
                out.append("\n" if char == "\n" else " ")
                index += 1
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
            index += 1
            continue
        if pair == "/-":
            block_depth = 1
            out.extend("  ")
            index += 2
        elif pair == "--":
            newline = source.find("\n", index)
            if newline < 0:
                out.extend(" " * (len(source) - index))
                index = len(source)
            else:
                out.extend(" " * (newline - index))
                index = newline
        elif char == '"':
            in_string = True
            out.append(" ")
            index += 1
        elif char == "'" and index + 2 < len(source) and source[index + 2] == "'":
            in_char = True
            out.append(" ")
            index += 1
        else:
            out.append(char)
            index += 1
    assert block_depth == 0 and not in_string and not in_char
    return "".join(out)


def run_checked(command: list[str], timeout: int) -> bytes:
    result = subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    assert result.returncode == 0, (
        command,
        result.returncode,
        result.stdout.decode("utf-8", errors="replace"),
    )
    return result.stdout


def main() -> None:
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    manifest = load(HERE / "vendor-manifest.json")
    receipt = load(HERE / "proof-receipt.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1078,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-0034-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"]
        if row["id"] == "S56-M-0034-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0034.QuillenSuslinTarget"
    )
    assert formal["elaborated_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["root_obligation_id"] == "M0034-ROOT"
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["selected_external_revision"] == SELECTED_EXTERNAL_REVISION
    assert registry["selected_external_revision"] != UPSTREAM_REVISION
    assert registry["proof_body_aliases"]["mbkybky.QuillenSuslin.quillenSuslin"] == (
        "alternative_body_no_selected_credit"
    )
    alternative = next(
        row for row in registry["obligations"]
        if row["obligation_id"] == "M0034-X-ALT-PID"
    )
    assert alternative["machine_eligibility"] == "informational"
    assert alternative["terminal_proof_body_id"] is None
    proof_edges = {
        (edge["from"], edge["type"], edge["to"])
        for edge in graphs["graphs"]["proof"]["edges"]
    }
    assert proof_edges == FROZEN_PROOF_EDGES
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["accepted_closed_obligations"] == []

    assert manifest["schema_version"] == "stage1-vendored-source-closure/1.0"
    assert manifest["item_id"] == ITEM and manifest["theorem_id"] == THEOREM
    assert manifest["upstream"]["project"] == "mbkybky/QuillenSuslin"
    assert manifest["upstream"]["revision"] == UPSTREAM_REVISION
    assert manifest["upstream"]["source_tree"] == UPSTREAM_TREE
    assert manifest["upstream"]["source_archive_sha256"] == UPSTREAM_ARCHIVE_SHA256
    assert manifest["target_environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert manifest["target_environment"]["mathlib_tree"] == MATHLIB_TREE
    assert manifest["license"]["spdx"] == "Apache-2.0"
    assert manifest["license"]["sha256"] == LICENSE_SHA256
    assert manifest["license"]["standard_text_supplied_locally"] is True
    assert manifest["license"]["copied_from_upstream_archive"] is False
    assert manifest["build_order"] == EXPECTED_BUILD_ORDER
    assert manifest["closure"]["module_count"] == len(manifest["files"]) == 8
    assert manifest["closure"]["internal_import_edges"] == 7
    assert manifest["closure"]["vendored_bytes"] == 260645
    assert manifest["closure"]["vendored_lines"] == 5079
    for key in ("semantic_diff_sha256", "normalized_compatibility_patch_sha256"):
        assert re.fullmatch(r"[0-9a-f]{64}", manifest["closure"][key]), key
    assert manifest["closure"]["semantic_diff_sha256"] == (
        "372acc2ec8f1f0921b9ffe63fda67f4ec40487840d8379af091a7297047d0d19"
    )
    assert manifest["closure"]["normalized_compatibility_patch_sha256"] == (
        "c76174fb78f391ceb00fc57df79829ef3af99c0dc43b477f444c61085ed02fe3"
    )

    vendor_root = HERE / "Vendor"
    actual_vendor_sources = {
        path.relative_to(vendor_root).as_posix()
        for path in vendor_root.rglob("*.lean")
    }
    expected_vendor_sources = {row["path"] for row in manifest["files"]}
    assert actual_vendor_sources == expected_vendor_sources
    actual_vendor_files = {
        path.relative_to(vendor_root).as_posix()
        for path in vendor_root.rglob("*") if path.is_file()
    }
    assert actual_vendor_files == expected_vendor_sources | {"LICENSE"}
    assert sha256(vendor_root / "LICENSE") == LICENSE_SHA256
    for row in manifest["files"]:
        path = vendor_root / row["path"]
        source = path.read_text(encoding="utf-8")
        assert sha256(path) == row["vendored_sha256"], row["path"]
        assert path.stat().st_size == row["vendored_bytes"], row["path"]
        assert re.fullmatch(r"[0-9a-f]{64}", row["upstream_sha256"]), row["path"]
        assert (
            "Released under Apache 2.0 license as described in the file LICENSE."
            in source[:512]
        ), row["path"]
        assert source.count("/- Port notice:") == int(row["modified"]), row["path"]
        assert bool(row["compatibility_operations"]) is row["modified"], row["path"]

    import_pattern = re.compile(
        r"^import «Stage1_Instances»\.«THM-M-0034»\.Vendor\."
        r"(QuillenSuslin\.[A-Za-z0-9_.]+)$",
        re.MULTILINE,
    )
    imports: dict[str, list[str]] = {}
    for relative in expected_vendor_sources:
        source = (vendor_root / relative).read_text(encoding="utf-8")
        imports[relative] = [
            module.replace(".", "/") + ".lean"
            for module in import_pattern.findall(source)
        ]
    assert sum(map(len, imports.values())) == 7
    assert {
        imported for values in imports.values() for imported in values
    } <= expected_vendor_sources
    reachable = {"QuillenSuslin/MainTheorem.lean"}
    pending = list(reachable)
    while pending:
        for imported in imports[pending.pop()]:
            if imported not in reachable:
                reachable.add(imported)
                pending.append(imported)
    assert reachable == expected_vendor_sources

    lean_paths = [HERE / "Proof.lean", HERE / "ProofAudit.lean"] + [
        vendor_root / row["path"] for row in manifest["files"]
    ]
    prohibited = re.compile(
        r"#exit\b|\b(sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    for path in lean_paths:
        stripped = strip_lean_comments_and_strings(path.read_text(encoding="utf-8"))
        match = prohibited.search(stripped)
        assert match is None, (path, match.group(0) if match else None)

    proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
    for marker in (
        "import «Stage1_Instances».«THM-M-0034».Statement",
        "import «Stage1_Instances».«THM-M-0034».Vendor.QuillenSuslin.MainTheorem",
        "theorem quillenSuslinTarget : QuillenSuslinTarget.{u, v} := by",
        "exact quillenSuslin k (Fin n) P",
        "#print sorries quillenSuslinTarget",
        "#print axioms quillenSuslinTarget",
    ):
        assert marker in proof, marker
    audit = (HERE / "ProofAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "assert_no_sorry quillenSuslin",
        "assert_no_sorry Stage1Instances.THM_M_0034.quillenSuslinTarget",
        "#print axioms Stage1Instances.THM_M_0034.quillenSuslinTarget",
    ):
        assert marker in audit, marker

    provenance = (HERE / "PORT_PROVENANCE.md").read_text(encoding="utf-8")
    assert UPSTREAM_REVISION in provenance and UPSTREAM_TREE in provenance
    assert UPSTREAM_ARCHIVE_SHA256 in provenance
    assert "not represented as a byte copy from the upstream archive" in provenance
    for row in manifest["files"]:
        for value in (row["path"], row["upstream_sha256"], row["vendored_sha256"]):
            assert value in provenance, value
    for key in ("semantic_diff_sha256", "normalized_compatibility_patch_sha256"):
        assert manifest["closure"][key] in provenance, key

    mathlib = LEAN_ROOT / ".lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256
    assert (LEAN_ROOT / ".lake").is_symlink()

    vendor_output = run_checked(
        [sys.executable, "-B", str(HERE / "build_vendor_manifest.py")], 120
    )
    assert b"PASS THM-M-0034 vendor closure" in vendor_output
    proof_output = run_checked(["bash", str(HERE / "check_proof.sh")], 1800)
    expected_output = (
        b"PASS THM-M-0034 isolated proof elaboration "
        b"(8 vendored modules, --trust=0 -t0)\n"
    )
    assert proof_output == expected_output, proof_output.decode("utf-8", errors="replace")
    assert not list(HERE.rglob("*.olean"))
    assert not list(HERE.rglob("*.ilean"))

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert receipt["exact_statement_delta"] == "none"
    assert receipt["kernel_inhabited_obligation_ids_observed"] == ["M0034-ROOT"]
    assert receipt["closed_obligation_ids_proposed"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["graph_reconciliation_pending"]["required"] is True
    assert receipt["graph_reconciliation_pending"]["frozen_selected_revision"] == (
        SELECTED_EXTERNAL_REVISION
    )
    assert receipt["graph_reconciliation_pending"]["observed_alternate_revision"] == (
        UPSTREAM_REVISION
    )
    assert receipt["frozen_proof_graph_cut_set"] == ["M0034-X-EXTERNAL-BODY"]
    assert receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    assert receipt["proof_body"]["proof_audit_sha256"] == sha256(
        HERE / "ProofAudit.lean"
    )
    assert receipt["proof_body"]["vendor_manifest_sha256"] == sha256(
        HERE / "vendor-manifest.json"
    )
    assert receipt["proof_body"]["upstream_revision"] == UPSTREAM_REVISION
    assert receipt["proof_body"]["upstream_tree"] == UPSTREAM_TREE
    assert receipt["proof_body"]["upstream_archive_sha256"] == UPSTREAM_ARCHIVE_SHA256
    assert receipt["proof_body"]["vendored_module_count"] == 8
    assert receipt["proof_body"]["vendored_source_bytes"] == 260645
    assert receipt["proof_body"]["license_sha256"] == LICENSE_SHA256
    assert receipt["proof_body"]["normalized_compatibility_patch_sha256"] == (
        manifest["closure"]["normalized_compatibility_patch_sha256"]
    )
    assert receipt["proof_body"]["semantic_diff_sha256"] == (
        manifest["closure"]["semantic_diff_sha256"]
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
        "proof_sha256": HERE / "Proof.lean",
        "proof_audit_sha256": HERE / "ProofAudit.lean",
        "vendor_manifest_sha256": HERE / "vendor-manifest.json",
        "build_vendor_manifest_sha256": HERE / "build_vendor_manifest.py",
        "check_proof_py_sha256": Path(__file__),
        "check_proof_sh_sha256": HERE / "check_proof.sh",
        "port_provenance_sha256": HERE / "PORT_PROVENANCE.md",
        "proof_validation_sha256": HERE / "proof-validation.md",
        "lean_toolchain_sha256": LEAN_ROOT / "lean-toolchain",
        "lake_manifest_sha256": LEAN_ROOT / "lake-manifest.json",
    }
    for key, path in input_paths.items():
        assert receipt["inputs"][key] == sha256(path), key
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["environment"]["validation_trust_level"] == 0
    assert receipt["validation_action"]["exit_code"] == 0
    assert receipt["validation_action"]["stdout_bytes"] == len(proof_output)
    assert receipt["validation_action"]["stdout_sha256"] == digest(proof_output)
    assert receipt["validation_action"]["observed_axioms"] == ALLOWED_AXIOMS
    result = receipt["result"]
    assert result["root_kernel_inhabitant_observed"] is True
    assert result["frozen_graph_closed"] is False
    assert result["accepted_root_closed"] is False
    assert result["audit_complete"] is False
    assert result["theorem_complete"] is False
    assert receipt["root_vector_before"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}

    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    )
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
        and not line[3:].startswith("Formalizations/Lean/.lake/")
    }
    expected_changes = set(receipt["changed_paths"])
    packet_path = ROOT / ".stage1-worker-selftest.json"
    if packet_path.exists():
        packet = load(packet_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == expected_changes
        assert packet["known_failures"] == receipt["known_failures"]
        assert actual_changes == expected_changes
    else:
        assert expected_changes == actual_changes | {".stage1-worker-selftest.json"}
    assert all(
        path == ".stage1-worker-selftest.json"
        or path.startswith(f"Stage1_Instances/{THEOREM}/")
        for path in actual_changes
    )

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    for marker in (
        "exact-root kernel inhabitant",
        "frozen proof graph remains open",
        "theorem_complete=false",
        "registry v2 or append-only route delta",
    ):
        assert marker in validation, marker
    for path in (
        Path(__file__), HERE / "proof-receipt.json", HERE / "proof-validation.md"
    ):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\x00" not in data, path
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path

    print(
        "PASS THM-M-0034 proof phase: exact PID-route root kernel inhabitant checked"
    )
    print(f"proof output sha256: {digest(proof_output)}")
    print(
        "accepted closure unchanged; frozen graph route reconciliation remains pending"
    )


if __name__ == "__main__":
    main()
