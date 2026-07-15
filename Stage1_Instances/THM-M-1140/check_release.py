#!/usr/bin/env python3
"""Fail-closed current-snapshot reconciliation for S56-M-1140-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1140"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
FLT_REGULAR = LEAN_ROOT / ".lake" / "packages" / "flt-regular"

ITEM = "S56-M-1140-RELEASE"
THEOREM = "THM-M-1140"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
EXPRESSION_SHA256 = "541e5716657e39b56e24f220a7118beecc0fc4f2a196312b7f278af92302b3b4"
DENOMINATOR_SHA256 = "355cbcf3b25f5e8ac67d3d814a268744dbe8ba8ae8afaec651199e64d6520bee"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
FLT_REGULAR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"

EXPECTED_INPUTS = {
    "Statement.lean": "c0f7ef8b8c003598b09d5984804630ca3d47bfde472c7748e5ee2035e6ef418a",
    "AnchorAudit.lean": "a7d1d721a0013aee621e42c56100b94bbbb29b1c4475197228691a52abb96bce",
    "ObligationTree.lean": "ed5fb3a36f248104c0f66458270fc362233a1634b46586cb33b2f006bc9f504b",
    "Proof.lean": "998609dc7186a333fbf3ae6220e6b7f63bd1b5c22995af1bd752a9d2d7de98ae",
    "Validation.lean": "c18f1f895224b991c5f11acee5edade11cd11af8a1d2fbcc3618bb09cb82241e",
    "intake.json": "7dbdd20f4813f3b6e63c397482b485336630512eb154a57644caa8ea464a092d",
    "statement.json": "57a7ddf69672b1b2bfb5be53d0752572c9b07b5915b7205da399e4b714ec1379",
    "anchor-audit.json": "7f37819dc454ae67b7e0363ea50d85ac378b377bda58806f1b2eeff1fd1ffdfc",
    "obligation-registry.json": "14dc0bf5e61a29063a530b3510c6b59f21be8d989c94ac2c13d31af481c90826",
    "typed-graphs.json": "6e99d7b827544e1cd78a882a84a8bd28fb8e1eaa66d33f49feec55b21d2b7477",
    "validation-specs.json": "bf0ff6ca61da45ca67a600a756b68505ddee03f06f79b71185f9b82b0c31b20b",
    "proof-receipt.json": "4f2f07e773b2ef59ea2cb01584d40d463a14384e3dcc22f7024f50a9bc880fbd",
    "validation-spec.json": "08bdd99c41d3d73698f791169ce83b6ada56e97b7d359415ccfe30b2bdecf20d",
    "validation-receipt.json": "4bbfe93b4ff2d0af175ad3f0823b00906366baed8cb1c53ce8bd2f06a10f053e",
    "check_validation.py": "53f60f04e6b854234a56d54afbb6a6c6e7417e5ccb665a469c4ed433b0de02ee",
    "check_proof.py": "24aa62e71c607c38b899c9f8645f5dcd8dc7af13926955182d5af7004297b3f4",
    "check_proof.sh": "fbff95b1fb7389eab5475a402599d566230ffa8d0e5ef2890024c0895b7979df",
    "check_obligation_tree.py": "3732b765719ef76bcc407d4e0737f4e841d0f42515dd3ee14b610069d2f5cb5a",
    "source_statement_crosswalk.md": "289b8dfa399c540fd4f8440fb2108c30b3f4127ec7a3a91b613899d72d546e70",
    "README.md": "bf253ea778e732c85564fae35dde37d2ce5b7a1ac989adf6e2f79b03b6768bfc",
    "validation-phase.md": "07eb9d8a0a322152761e5bd488489465d661fa5c26def88ab3e16be81c77ee31",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "c09f9f713bdbc820559e41e1e1840423d60cc2af666aeaf5f3c88587de77f161",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0bb2f433832fe71156aa46c0828102ec3fb61a00dec81fae129c2826a59f63ca",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lakefile.lean": "43259bbc1b42b1574b78c8584753029dc5e118c0a0e752ac0a5bad9004b4dcda",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
INVENTORY_IDS = [
    "M1140-ROOT", "M1140-S-DEFINITIONS", "M1140-S-DOMAIN",
    "M1140-S-BOUNDARY", "M1140-S-FOUNDATION", "M1140-N-MAX-LEVEL",
    "M1140-L-MEAN-VALUE", "M1140-L-CONTINUITY", "M1140-L-LEVEL-CLOSED",
    "M1140-L-LEVEL-OPEN", "M1140-L-CONNECTED", "M1140-T-LOCAL-PACKAGE",
    "M1140-T-PROPAGATION-PACKAGE", "M1140-T-ASSEMBLE", "M1140-X-SOURCE",
    "M1140-X-PROVENANCE",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = (
    "PASS release reconciliation: manifest, DAG, statement, frozen inventory, receipts, and hashes agree",
    "PASS current structural checks: 16 obligations and 36 typed edges; accepted root remains H2/M3/R3",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional, unaccepted, and nonrelease-grade",
    "BLOCKED freshness: validation is snapshot-bound and the pinned flt-regular worktree HEAD is unresolved",
    "BLOCKED audit and release: architecture, H0/R0, TCB/SBOM, cold offline, independent, and bundle gates remain open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key {key!r} in {path}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, expected_exit: int = 0) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=180, check=False,
    )
    assert result.returncode == expected_exit, (argv, result.returncode, result.stdout)
    return result.stdout


def git(*args: str, cwd: Path = ROOT, expected_exit: int = 0) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, expected_exit=expected_exit).rstrip()


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    if sys.flags.optimize:
        raise RuntimeError("release reconciliation requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 345, "legacy_priority_slot": None, "theorem_id": THEOREM,
        "name": "强极值原理", "category": "微分方程 / 偏微分方程",
        "source_status_untrusted": "已验证", "baseline": "L0",
        "rework_required": True, "legacy_artifacts_accepted": False,
        "target_lane": "hard_mathlib_anchor_and_wrapper", "intake_score": 142,
        "lifecycle_mode": "planned", "theorem_complete": False,
    }
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1140-VALIDATION"
    )
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 345,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1140-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"release input drifted: {name}"
    for name, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    canonical = statement["canonical_formal_target"]
    assert canonical["declaration"] == (
        "Stage1Instances.THM_M_1140.HarmonicStrongMaximumPrinciple"
    )
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert canonical["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1140-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == [
        "M1140-T-LOCAL-PACKAGE", "M1140-T-PROPAGATION-PACKAGE",
    ]
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1140-ROOT")
    assert root_node["human_debt"] == "H2"
    assert root_node["machine_debt"] == "M3"
    assert root_node["readability_debt"] == "R3"
    assert root_node["evidence_ids"] == []
    assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False

    assert validation["item_id"] == validation_item["id"]
    assert validation["receipt_id"] == decision["dependency"]["receipt_id"]
    assert decision["dependency"]["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["content_addressed"] is False and validation["verdict"] == "blocked"
    assert validation["accepted_receipt_ids"] == []
    assert validation["accepted_closed_obligation_ids"] == []
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == "dependency.S56-M-1140-PROOF.master_acceptance"
    assert validation["first_failed_node_specific_gate"] == (
        "S56-M-1140-VALIDATION-FROZEN-ARCHITECTURE-RECONCILIATION"
    )
    assert validation["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False and proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["result"]["theorem_complete"] is False

    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["decision_support"] == receipt["support_state"] == (
        "provisional_worker_selftest"
    )
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    dependency = decision["dependency"]
    assert dependency["item_id"] == "S56-M-1140-VALIDATION"
    assert dependency["worker_projection"] == "[_]"
    assert dependency["master_accepted"] is False
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["content_addressed"] is validation["content_addressed"] is False
    assert dependency["receipt_base_revision"] == validation["base_revision"]
    assert dependency["current_snapshot_replayable"] is False

    result = decision["decision"]
    assert result["verdict"] == receipt["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == {
        "H": "H2", "M": "M3", "R": "R3",
    }
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["master_accepted"] is receipt["content_addressed_release_evidence"] is False
    receipt_result = receipt["result"]
    assert receipt_result["verdict"] == "blocked"
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == {
        "H": "H2", "M": "M3", "R": "R3",
    }
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["argv"] == [
        "/usr/bin/bwrap", "--ro-bind", "/", "/", "--dev", "/dev",
        "--proc", "/proc", "--tmpfs", "/tmp", "--unshare-net", "--die-with-parent",
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
    ]
    assert spec["timeout_seconds"] == 180 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0 and spec["reconciled_inventory_ids"] == INVENTORY_IDS
    assert spec["covered_obligation_ids"] == ["M1140-ROOT", "M1140-T-ASSEMBLE"]
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "reconciled_inventory_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key

    for key in (
        "accepted_exact_root_kernel_closure", "authoritative_graph_reconciled",
        "audit_z_accepted", "pinpoint_h0_review", "independent_r0_review",
        "accepted_foundation_policy", "complete_transitive_provenance_tcb_closure",
        "immutable_clean_release_input", "hermetic_cold_offline_replay",
        "sbom_license_archive_closure", "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier", "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key
    cut_set = "\n".join(result["remaining_release_cut_set"])
    for fragment in (
        "S56-M-1140-VALIDATION", "Gaussian-barrier", "M1140-S-FOUNDATION",
        "M1140-X-PROVENANCE", "M1140-X-SOURCE", "R0", "AUDIT-Z",
        "empty-cache network-denied cold build", "SBOM", "two signed attestations",
        "minimal verifier", "deterministic content-addressed release bundle",
    ):
        assert fragment in cut_set, fragment

    standard = run(["/usr/bin/python3", "Docs/tools/check_stage1_standard.py"])
    assert "check_stage1_standard: ok" in standard and "1546 uniform-L0" in standard
    target_check = run(["/usr/bin/python3", "scripts/stage1_target.py", "check"])
    assert "stage1_target: ok" in target_check and "1546 unique targets" in target_check
    target_show = run([
        "/usr/bin/python3", "scripts/stage1_target.py", "show", THEOREM,
    ])
    shown = json.loads(target_show)
    assert shown == target
    structural = run([
        "/usr/bin/python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py",
    ])
    assert "PASS THM-M-1140 obligation tree: 16 obligations, 36 typed edges" in structural
    proof_metadata = run([
        "/usr/bin/python3", "-B", f"Stage1_Instances/{THEOREM}/check_proof.py",
    ], expected_exit=1)
    assert "AssertionError" in proof_metadata
    assert packet["item_id"] == ITEM

    validation_replay = run([
        "/usr/bin/python3", "-I", "-B",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
    ], expected_exit=1)
    assert "AssertionError" in validation_replay
    assert validation["base_revision"] != BASE_REVISION

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    flt_entry = next(row for row in manifest["packages"] if row["name"] == "«flt-regular»")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert flt_entry["rev"] == flt_entry["inputRev"] == FLT_REGULAR_REVISION
    assert MATHLIB.resolve().is_dir() and FLT_REGULAR.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    flt_head = git("rev-parse", "HEAD", cwd=FLT_REGULAR, expected_exit=128)
    assert "unknown revision or path" in flt_head
    assert (FLT_REGULAR / ".git" / "HEAD").read_text(encoding="utf-8") == (
        "ref: refs/heads/.invalid\n"
    )
    assert git("cat-file", "-e", f"{FLT_REGULAR_REVISION}^{{commit}}", cwd=FLT_REGULAR) == ""
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT, expected_exit=1)
    assert (
        "could not resolve 'HEAD' to a commit" in lean_version
        or "external command 'git' exited with code 255" in lean_version
    )
    proof_replay = run(["/usr/bin/bash", str(HERE / "check_proof.sh")], expected_exit=1)
    assert (
        "could not resolve 'HEAD' to a commit" in proof_replay
        or "external command 'git' exited with code 255" in proof_replay
    )

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        assert prohibited.search(source_without_comments((HERE / name).read_text())) is None, name

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert set(decision["changed_paths"]) == CHANGED_PATHS
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == decision["output_summary"]
    assert packet["output_summary"] == receipt["output_summary"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    assert os.path.islink(LEAN_ROOT / ".lake")
    assert os.readlink(LEAN_ROOT / ".lake") == (
        "/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake"
    )
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    expected_stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["recipe_output"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout.encode("utf-8")
    ).hexdigest()
    assert receipt["recipe_output"]["stdout_bytes"] == len(expected_stdout.encode("utf-8"))
    print(expected_stdout, end="")


if __name__ == "__main__":
    main()
