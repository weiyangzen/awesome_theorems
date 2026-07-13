#!/usr/bin/env python3
"""Validate the replayable THM-M-0819 anchor-audit packet."""

from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0819-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0819"
BASE_REVISION = "27400857bccc93638c97e9c65859ddf5d5b5f4da"
BASE_TREE = "3762537e0e5ae46cd70b086da49a69e2fd7b275c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
INVENTORY_VERSION = "THM-M-0819-anchor-inventory/1"
CUTOFF = "2026-07-13T23:02:43+08:00"
EXPRESSION_SHA256 = "bdf0aa8f8adac4be9bf2080951be62eac168872b8c589a804ac8587c1878bb19"
STATEMENT_BUNDLE_SHA256 = "df437e79e306cbbdca0f9344a6a953a7f27886a197db7c614b995c846f8a2195"
STATEMENT_SHA256 = "c3e600a4a5c2b48686bf244915aea79972e4537a2d89120ad739018716056b52"
STATEMENT_JSON_SHA256 = "56d8c2af848287eab330da7497ad4fb5039a6305d4584e68415863cc6e0edf7c"
PROTOCOL_SHA256 = "de23ca5cc3a9908e672c70a6ae5e4b9e616836db091fe973ffee3f339428b04c"
ANCHOR_SHA256 = "23aaab376704c3bdae1e3ac1a590e222443768d64909e73160491bbec920efb1"
LEAN_OUTPUT_SHA256 = "d2e476abb93fd66df9a9dd804ef0b5cb68bdc64ec095351a3ebbaf3d873b510b"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
VLAD_REVISION = "f82f920f05a381bb1ce5e8903bde33e27f4365b6"
VLAD_SOURCE_SHA256 = "4bc86897588087f472b358830bba157b92994e2b0dd44c66805f57c29211c985"
VLAD_ARCHIVE_SHA256 = "5b0bcbb35a1f6939f1ac330144c1f32b38c1a1e5fc28304c985390030c362408"
VLAD_TOOLCHAIN_SHA256 = "53382cbe9b2e717af378843459403242cc24a3cc00865ffc644e7cd420a0f815"
VLAD_MANIFEST_SHA256 = "45eb015f8eb89e188406b4df626a9ed778c55251d36b59516adaaf7565fa026e"
VLAD_LICENSE_SHA256 = "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"
VLAD_CURRENT_PIN_OUTPUT_SHA256 = "01a36fd460bb5ef6f3761d026e1846e39755b9b8ec06f00b52a5bf76abd3d56e"
COQ_REVISION = "74c0cde97967149b7f44b775fabdc7d909760ebd"
COQ_SOURCE_SHA256 = "1ac4a43f82dde30132b7b9b730bde5495770b1129e502162ac0e8a7fce87115d"
INVENTORY_MEMBERS = {
    "M0819-C01-REPO-LOCAL-STATEMENT",
    "M0819-C02-REPO-LOCAL-NONCANDIDATES",
    "M0819-C03-MATHLIB-EXACT-TOPIC",
    "M0819-C04-MATHLIB-SUBSTRATE-AND-LOCATOR",
    "M0819-C05-MANIFEST-PINNED-EXTERNALS",
    "M0819-C06-VLAD-FINITE-EQUALITY",
    "M0819-C07-PUBLIC-SEARCH-BOUNDARY",
    "M0819-C08-COQ-FINITE-FORMALIZATION",
    "M0819-C09-HUMAN-SOURCE-BOUNDARY",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}
SOURCE_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json":
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md":
        "23beea005fc66bf5f7c8409ef0d9c1467b9b5a835f3dcd82c7364a44038adfd0",
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "68dac5e13eb0d76db27455b0270e8715f0a5b76e8053d9bbeeb1595fb40e5b99",
    "skills/execute-stage1-rev56/SKILL.md":
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain":
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json":
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    f"Stage1_Instances/{THEOREM_ID}/Statement.lean": STATEMENT_SHA256,
    f"Stage1_Instances/{THEOREM_ID}/statement.json": STATEMENT_JSON_SHA256,
}
MATHLIB_FILES = {
    "Mathlib/Order/Antichain.lean": (
        "65126484292f6fdc68c80f96fcd537a85a9378dd",
        "d124c384df09f812df642ddffa03acf2cf12d45e307f839dc7d91efb41ef677d",
    ),
    "Mathlib/Order/Height.lean": (
        "248a84a984a85e5867d816055d67a8c39bd02bf3",
        "800a7db6f57477f80b6d58f753cd25f107b9a979aec5fc05ff2fc02999517425",
    ),
    "Mathlib/Order/Preorder/Chain.lean": (
        "79192e03cfc5ff64bbc4a5b423bea42561de6b1b",
        "e376f326b56f65f92c5aa2873959dc600265f60c1fd99d64d0aad5a2d02f895e",
    ),
    "docs/1000.yaml": (
        "3e681315f501e3487e117071b1ec8710e7d95176",
        "12792e25ca081fb16c149223f9920c0dff1214ebe5e46b026e15829862a0130c",
    ),
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def candidate(audit: dict, candidate_id: str) -> dict:
    return next(row for row in audit["candidates"] if row["candidate_id"] == candidate_id)


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*", "", source)
    return re.sub(r'"(?:\\.|[^"\\])*"', '""', source)


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    if not data.endswith(b"\n"):
        raise SystemExit(f"missing final newline: {path}")
    if b"\r" in data or b"\x00" in data:
        raise SystemExit(f"invalid byte in {path}")
    if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
        raise SystemExit(f"trailing whitespace in {path}")


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert audit["item_id"] == protocol["item_id"] == receipt["item_id"] == ITEM_ID
    assert audit["theorem_id"] == protocol["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1377
    assert audit["base_revision"] == protocol["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == protocol["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1377
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0819-STATEMENT")
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]" and predecessor["state"] == "[_]"
    assert item["depends_on"] == ["S56-M-0819-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_bundle_sha256"] == STATEMENT_BUNDLE_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == audit["canonical_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_bundle_sha256"] == STATEMENT_BUNDLE_SHA256
    assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "statement.json") == STATEMENT_JSON_SHA256

    assert protocol["inventory_version"] == audit["inventory_version"] == INVENTORY_VERSION
    assert protocol["frozen_at"] == protocol["cutoff"] == audit["cutoff"] == CUTOFF
    assert protocol["saturation_claim"] is False
    assert set(protocol["inventory_members"]) == INVENTORY_MEMBERS
    assert {row["candidate_id"] for row in audit["candidates"]} == INVENTORY_MEMBERS
    assert sha256(HERE / "anchor-discovery-protocol.json") == PROTOCOL_SHA256

    environment = audit["immutable_environment"]
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == environment["mathlib_license_sha256"] == MATHLIB_LICENSE_SHA256
    for path, (blob, digest) in MATHLIB_FILES.items():
        assert output("git", "rev-parse", f"HEAD:{path}", cwd=MATHLIB) == blob
        assert sha256(MATHLIB / path) == digest

    local = candidate(audit, "M0819-C01-REPO-LOCAL-STATEMENT")
    assert local["candidate_classification"] == "M3_exact_statement_only"
    assert local["evidence_level"] == "E3" and local["terminal_proof_body"] is None
    repo_negative = candidate(audit, "M0819-C02-REPO-LOCAL-NONCANDIDATES")
    assert repo_negative["searched_tracked_lean_file_count"] == 2461
    mathlib_exact = candidate(audit, "M0819-C03-MATHLIB-EXACT-TOPIC")
    assert mathlib_exact["searched_library_lean_file_count"] == 7871
    assert mathlib_exact["candidate_classification"] == "no_exact_candidate"
    pinned = candidate(audit, "M0819-C05-MANIFEST-PINNED-EXTERNALS")
    assert pinned["searched_lean_file_count"] == 9676

    vlad = candidate(audit, "M0819-C06-VLAD-FINITE-EQUALITY")
    assert vlad["revision"] == VLAD_REVISION
    assert vlad["file_sha256"] == VLAD_SOURCE_SHA256
    assert vlad["archive_sha256"] == VLAD_ARCHIVE_SHA256
    assert "all 13 regular files" in vlad["archive_tree_reconstruction_scope"]
    assert vlad["original_toolchain_sha256"] == VLAD_TOOLCHAIN_SHA256
    assert vlad["original_lake_manifest_sha256"] == VLAD_MANIFEST_SHA256
    assert vlad["license_sha256"] == VLAD_LICENSE_SHA256
    assert vlad["original_mathlib_revision"] == "3234d21e85d1c08e42db46555be77bc3a051a61b"
    assert vlad["declaration"] == "minChainPartition_eq_antichainWidth"
    assert vlad["candidate_classification"] == "M5_scope_mismatch_and_current_pin_failure"
    assert vlad["evidence_level"] == "no_root_E_tier_nonexact_related_candidate"
    assert vlad["current_pin_check"]["exit"] == 1
    assert vlad["current_pin_check"]["output_sha256"] == VLAD_CURRENT_PIN_OUTPUT_SHA256
    assert len(vlad["current_pin_check"]["failures"]) == 3
    assert any("arbitrary carrier" in row for row in vlad["unclosed_statement_bridges"])
    assert any("sorryAx" in row for row in vlad["current_pin_check"]["machine_axiom_output"])

    coq = candidate(audit, "M0819-C08-COQ-FINITE-FORMALIZATION")
    assert coq["revision"] == COQ_REVISION and coq["file_sha256"] == COQ_SOURCE_SHA256
    assert coq["candidate_classification"] == "M5_wrong_backend_and_finite_scope"

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("9/9")
    assert result["exact_statement_candidate_located"] is True
    assert result["exact_proof_candidate_located"] is False
    assert result["candidate_kernel_checked_under_repository_pin"] is False
    assert result["root_machine_debt_before"] == result["strongest_exact_root_machine_debt_after"] == "M3"
    assert result["root_evidence_level"] == (
        "E3 exact-statement evidence only; the nonexact external candidate receives no root E tier"
    )
    assert result["discovery_protocol_evidence_complete"] is False
    assert "per-query ledger" in result["discovery_protocol_evidence_blocker"]
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is result["theorem_complete"] is False
    expected_vector = {"H": "H1", "M": "M3", "R": "R3"}
    assert audit["root_vector_before"] == audit["root_vector_after"] == expected_vector

    assert receipt["phase"] == "anchor_audit" and receipt["assigned_layer"] == 2
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert set(receipt["changed_paths"]) == set(packet["changed_paths"]) == CHANGED_PATHS
    assert receipt["known_failures"] == packet["known_failures"] == audit["known_failures"]
    assert receipt["accepted_receipt_ids"] == audit["accepted_receipt_ids"] == []
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == expected_vector
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["anchor_source_sha256"] == ANCHOR_SHA256
    assert receipt["discovery_protocol_sha256"] == PROTOCOL_SHA256
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["base_revision"] == BASE_REVISION
    for path, digest in SOURCE_INPUTS.items():
        assert receipt["source_inputs"][path] == f"sha256:{digest}"
        assert sha256(ROOT / path) == digest

    actual_changed = {
        line[3:]
        for line in output("git", "status", "--short", "--untracked-files=all").splitlines()
    }
    assert actual_changed - {"Formalizations/Lean/.lake"} == CHANGED_PATHS

    anchor = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    assert sha256(HERE / "AnchorAudit.lean") == ANCHOR_SHA256
    for marker in (
        "def HasExactly",
        "def IsDependent",
        "def IsDisjointChainDecomposition",
        "def ExactTarget",
        "#check IsChain",
        "#check IsAntichain",
        "#check Set.chainHeight",
        "#print ExactTarget",
    ):
        assert marker in anchor, marker
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe|native_decide|implemented_by|extern)\b"
    )
    assert forbidden.search(without_comments(anchor)) is None

    lean_environment = os.environ.copy()
    lean_environment.update({"LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"})
    lean = subprocess.run(
        ["lake", "env", "lean", f"../../Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean"],
        cwd=LEAN_ROOT,
        env=lean_environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    for marker in (
        "IsChain.",
        "IsAntichain.",
        "Set.chainHeight.",
        "Set.exists_eq_chainHeight_of_finite.",
        "def Stage1Instances.THM_M_0819_AnchorAudit.ExactTarget",
    ):
        if marker not in lean.stdout:
            sys.stdout.write(lean.stdout)
            raise SystemExit(f"missing Lean evidence marker: {marker}")
    if "sorryAx" in lean.stdout or hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("anchor Lean output changed or contains recovery holes")

    for relative in CHANGED_PATHS:
        check_text_file(ROOT / relative)
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    print(
        "check_anchor_audit: ok "
        "(THM-M-0819; 9/9 bounded groups classified; exact root remains M3; "
        "finite external candidate is M5 and supplies no proof credit)"
    )


if __name__ == "__main__":
    main()
