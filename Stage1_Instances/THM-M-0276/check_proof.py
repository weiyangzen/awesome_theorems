#!/usr/bin/env python3
"""Fail-closed source, pin, graph-boundary, receipt, and Lean checks for proof phase."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0276-PROOF"
THEOREM = "THM-M-0276"
BASE_REVISION = "5931467f7eefac7a6e57777cc3082e4a2edc03d4"
BASE_TREE = "45a10c953e5dc79c1eb9ae7d755ee84866717775"
EXPRESSION_SHA256 = "0cfb9796471903d081ad67551a3f9c2c3414cce1f7adbf79394d364a467c82fa"
DENOMINATOR_SHA256 = "1437a03a1fa4badc07b730dd8fb72bc6e2783c1205a2d842479b573cfde710c8"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
BANACH_SOURCE = MATHLIB / "Mathlib/Analysis/Normed/Operator/Banach.lean"
BANACH_SHA256 = "b046e38a239014c32e2313b4a216edd89198e57351d9c6068a3de7811680bf6c"
BANACH_BLOB = "8d4361a5bdf07bb8b7e2214ee59340f9931422bd"
BANACH_OLEAN = (
    MATHLIB
    / ".lake/build/lib/lean/Mathlib/Analysis/Normed/Operator/Banach.olean"
)
BANACH_OLEAN_SHA256 = "3a1f5d8a584421c9878fdd8401429e3b44847122efd4e944fd7e9d2133528224"
EXPECTED_INPUT_HASHES = {
    "Statement.lean": "ede62e0c7bbf3804f6a81c2f1115643048c69ced4750453af7e8ebd845c6aeea",
    "ObligationTree.lean": "e5757cdf296ba2c12b52658dd7e8231decf8de61a0ff97718139b7a864ab2a76",
    "obligation-registry.json": "0a5df1dbb570e1ec995f609e6e75e6fe0e1e33e306f7f180eeb3a2a139647004",
    "typed-graphs.json": "853fc1e01fe0abc25bc0d8ab82a2b1013562b21a7d277215930fa86359ed4ea3",
    "anchor-audit.json": "d84027b9f12d99c5617d719f7ce48bb1b34917a90414f476589e53c17934b906",
    "validation-specs.json": "18d146c8cfa420b914fa2970987bc1fda939f4060af27d57bcc501840f494bd0",
}
INPUT_RECEIPT_KEYS = {
    "Statement.lean": "statement_lean_sha256",
    "ObligationTree.lean": "obligationtree_lean_sha256",
    "obligation-registry.json": "obligation_registry_json_sha256",
    "typed-graphs.json": "typed_graphs_json_sha256",
    "anchor-audit.json": "anchor_audit_json_sha256",
    "validation-specs.json": "validation_specs_json_sha256",
}
DECLARATIONS = (
    "pinnedApproximatePreimage",
    "pinnedExactPreimage",
    "pinnedOpenMap",
    "pinnedMathlibTerminal",
    "realOpenMapping",
    "complexOpenMapping",
    "banachOpenMapping_direct",
    "banachOpenMapping_via_frozen_composition",
    "expandedBanachOpenMapping",
)
UPSTREAM_DECLARATIONS = (
    "ContinuousLinearMap.exists_approx_preimage_norm_le",
    "ContinuousLinearMap.exists_preimage_norm_le",
    "ContinuousLinearMap.isOpenMap",
)
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MAPPED_IDS = [
    "M0276-ROOT",
    "M0276-N-SAME-FIELD",
    "M0276-T-ASSEMBLE",
    "M0276-T-ADAPTER",
    "M0276-T-UPSTREAM",
    "M0276-B-REAL",
    "M0276-B-COMPLEX",
    "M0276-T-ISOPENMAP",
    "M0276-L-LOCAL-OPEN-BALL",
    "M0276-L-EXACT-PREIMAGE",
    "M0276-C-APPROX-SELECTION",
    "M0276-L-RESIDUAL-GEOMETRIC",
    "M0276-L-SUMMABLE-SERIES",
    "M0276-L-TELESCOPE",
    "M0276-L-LIMIT-IMAGE",
    "M0276-L-APPROX-PREIMAGE",
    "M0276-C-BAIRE-COVER",
    "M0276-L-BAIRE-INTERIOR",
    "M0276-L-RESCALE-SHELL",
    "M0276-C-CLOSURE-PAIR",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
    assert isinstance(value, dict), path
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    task_dag = load(HERE / "task-dag.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1282
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0276-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_item = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_item["state"] == "open" and task_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for declaration in DECLARATIONS:
        assert re.search(rf"^theorem {declaration}\b", proof, re.MULTILINE), declaration
        assert f"assert_no_sorry {declaration}" in proof
        assert f"#print sorries {declaration}" in proof
        assert f"#print axioms {declaration}" in proof
    for declaration in UPSTREAM_DECLARATIONS:
        assert f"assert_no_sorry {declaration}" in proof
        assert f"#print sorries {declaration}" in proof
        assert f"#print axioms {declaration}" in proof
    for marker in (
        "import Statement",
        "import ObligationTree",
        "ContinuousLinearMap.exists_approx_preimage_norm_le f surj",
        "ContinuousLinearMap.exists_preimage_norm_le f surj",
        "ContinuousLinearMap.isOpenMap f surj",
        "Stage1Instances.THM_M_0276_Obligations.compose_root",
        "Stage1Instances.THM_M_0276_Obligations.terminal_adapter pinnedMathlibTerminal",
        "banachOpenMappingTarget_iff_expandedOpenMappingTarget.mp",
    ):
        assert marker in proof, marker

    for name, expected in EXPECTED_INPUT_HASHES.items():
        assert sha256(HERE / name) == expected, f"prerequisite changed: {name}"
    assert registry["root_obligation_id"] == "M0276-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert len(registry["obligations"]) == 29
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["root_node_id"] == "M0276-ROOT"
    assert len(graphs["unverified_decomposition_plans"]) == 14
    assert graphs["closure_boundary"]["closed_obligations"] == []
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["accepted_root_machine_debt"] == "M3"
    assert graphs["closure_boundary"]["theorem_complete"] is False
    reachable = set()
    children: dict[str, list[str]] = {}
    for edge in graphs["graphs"]["proof"]["edges"]:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])

    def visit(identifier: str) -> None:
        if identifier in reachable:
            return
        reachable.add(identifier)
        for child in children.get(identifier, []):
            visit(child)

    visit("M0276-ROOT")
    assert list(reachable) and reachable == set(MAPPED_IDS)

    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert git(
        "rev-parse", "HEAD:Mathlib/Analysis/Normed/Operator/Banach.lean", cwd=MATHLIB
    ) == BANACH_BLOB
    assert sha256(BANACH_SOURCE) == BANACH_SHA256
    assert sha256(BANACH_OLEAN) == BANACH_OLEAN_SHA256
    source_lines = BANACH_SOURCE.read_bytes().splitlines(keepends=True)
    body_hashes = {
        "approximate_preimage": hashlib.sha256(b"".join(source_lines[84:153])).hexdigest(),
        "exact_preimage": hashlib.sha256(b"".join(source_lines[159:225])).hexdigest(),
        "open_map": hashlib.sha256(b"".join(source_lines[226:248])).hexdigest(),
    }
    assert body_hashes == receipt["proof_body"]["terminal_body_sha256"]

    run = subprocess.run(
        ["bash", f"Stage1_Instances/{THEOREM}/check_proof.sh"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=180,
    )
    if run.returncode:
        print(run.stdout, end="")
        raise SystemExit(run.returncode)
    assert "PASS THM-M-0276 Lean proof" in run.stdout
    assert "sorryAx" not in run.stdout and "error:" not in run.stdout
    for declaration in UPSTREAM_DECLARATIONS:
        assert f"'{declaration}' depends on axioms:" in run.stdout
    for declaration in DECLARATIONS:
        qualified = f"Stage1Instances.THM_M_0276.Proof.{declaration}"
        assert f"'{qualified}' depends on axioms:" in run.stdout
    reported = set(re.findall(r"(?:propext|Classical\.choice|Quot\.sound|sorryAx)", run.stdout))
    assert reported == ALLOWED_AXIOMS

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["inputs"]["check_proof_sh_sha256"] == sha256(HERE / "check_proof.sh")
    for name, key in INPUT_RECEIPT_KEYS.items():
        assert receipt["inputs"][key] == sha256(HERE / name), key
    root = receipt["root_evidence"]
    assert root["root_kernel_declaration_closed"] is True
    assert root["accepted_root_closed"] is False
    assert root["machine_debt_proposal"] == "M0-W"
    assert root["closed_obligation_ids"] == root["accepted_closed_obligation_ids"] == []
    assert root["mapped_proof_graph_id_count"] == len(MAPPED_IDS)
    assert root["mapped_proof_graph_ids"] == MAPPED_IDS
    assert root["internal_per_node_composition_credit"] is False
    assert root["unverified_internal_composition_count"] == 14
    assert set(receipt["result"]["axioms"]) == ALLOWED_AXIOMS
    assert receipt["result"]["accepted_state_changed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["debt_vector"]["accepted_before"] == {
        "H": "H2", "M": "M3", "R": "R4"
    }
    assert receipt["debt_vector"]["accepted_after_worker_selftest"] == {
        "H": "H2", "M": "M3", "R": "R4"
    }
    assert set(receipt["changed_paths"]) == CHANGED_PATHS

    required_packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet) == required_packet_fields
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]

    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS
    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "not acceptance or\ntheorem completion" in validation
    assert "M0-W" in validation and "Fourteen" in validation
    for relative in CHANGED_PATHS:
        path = ROOT / relative
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for path in (HERE / "proof-receipt.json", HERE / "proof-validation.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    print(
        "PASS THM-M-0276 proof packet: exact pinned M0-W root proposal, "
        "20 mapped proof IDs, 14 uncredited internal composition plans, theorem_complete=false"
    )


if __name__ == "__main__":
    main()
