#!/usr/bin/env python3
"""Validate the bounded, immutable THM-M-0814 anchor inventory."""

from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0814-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0814"
BASE_REVISION = "46a0f2a3ea74765a0467c489264b838ffbb70675"
BASE_TREE = "7b1b5269d7da840fd086da731d6f92903c209c35"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "f9fc7813f437ebcd4b2b7327373dd76134d651c1624d2a06f689e84ec571a21e"
STATEMENT_SHA256 = "e2493ef46f9bdd5c8d0b30069efaf27b7ad0f69781d4c4c7317b94a63a06755b"
STATEMENT_JSON_SHA256 = "ed7b955159e8bc250fe051cc69ad5b067c7f0901a3a401e0ae4890414adda4b0"
PROTOCOL_SHA256 = "3752eccca8af840e91778f287ca9a5dd32b0a7a46f20889b7ebd465a8b3b9b40"
ANCHOR_SHA256 = "e852f11560a1ec8ab115d6991ba4cad0528d6ebe52fd7a96149bf85e3dc656c2"
LEAN_OUTPUT_SHA256 = "b03b1756e0866b4c33daebfb0cd1835d1c726b8ffa602c4d85332d23f21559e9"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
ATLAS_REVISION = "34ffed396f376454c1a9b297f3fd74c5c801fb50"
ATLAS_SOURCE_SHA256 = "548d67576de93163edafe40fc0de829b7a05d3fcaacdcedd8e08c6dd14c7261e"
ATLAS_SUPPORT_SHA256 = "960d7755cdea6595421964ef29cd487636bae2cbc6929bb5b419cf06cddb6ce8"
INVENTORY_VERSION = "THM-M-0814-anchor-inventory/2"
CUTOFF = "2026-07-13T22:12:00+08:00"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/README.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
    f"Stage1_Instances/{THEOREM_ID}/external-anchor-snapshot.json",
    f"Stage1_Instances/{THEOREM_ID}/instance.json",
}
INVENTORY_MEMBERS = {
    "M0814-C01-REPO-LOCAL-EXACT-STATEMENT",
    "M0814-C02-REPO-LOCAL-NONSUBSTITUTES",
    "M0814-C03-MATHLIB-EXACT-TOPIC",
    "M0814-C04-MATHLIB-SUPPORT-AND-NONSUBSTITUTES",
    "M0814-C05-MANIFEST-PINNED-EXTERNALS",
    "M0814-C06-PUBLIC-LEAN4-RESULTS",
    "M0814-C07-FORMAL-CONJECTURES",
    "M0814-C08-HISTORICAL-LEAN3-RESULTS",
    "M0814-C09-HUMAN-SOURCE-BOUNDARY",
    "M0814-C10-CLRS-LEAN-PARTIAL",
    "M0814-C11-ZETAGON-HISTORICAL-LEAN3",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def strip_lean_comments(source: str) -> str:
    result: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            result.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                result.append("\n")
            index += 1
        else:
            result.append(source[index])
            index += 1
    if depth:
        raise SystemExit("unterminated Lean block comment")
    return "".join(result)


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    external = load(HERE / "external-anchor-snapshot.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    target_manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    lake_manifest = load(LEAN_ROOT / "lake-manifest.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1373
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in target_manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1373
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    prerequisite = next(
        row for row in execution["items"] if row["id"] == "S56-M-0814-STATEMENT"
    )
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] in {"[ ]", "[_]"}
    assert prerequisite["state"] in {"[_]", "[x]"}
    assert item["depends_on"] == ["S56-M-0814-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Audit mathlib and external Lean 4 candidates at immutable revisions."

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "statement.json") == STATEMENT_JSON_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == audit["canonical_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256

    assert protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0"
    assert protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID
    assert protocol["base_revision"] == BASE_REVISION
    assert protocol["inventory_version"] == audit["inventory_version"] == INVENTORY_VERSION
    assert protocol["frozen_at"] == protocol["cutoff"] == audit["cutoff"] == CUTOFF
    assert audit["discovery_protocol"]["frozen_at"] == CUTOFF
    assert audit["discovery_protocol"]["cutoff"] == CUTOFF
    assert protocol["predecessor_inventory"] == {
        "inventory_version": "THM-M-0814-anchor-inventory/1",
        "cutoff": "2026-07-13T20:43:00+08:00",
        "protocol_sha256": "fa344e254f0bb75fb8c5623cc3ee46d8e380c554b016cfc79baf09a585993ae8",
        "supersession_reason": (
            "Two concrete immutable leads observed after the version-1 cutoff were appended and "
            "classified in version 2."
        ),
    }
    assert protocol["saturation_claim"] is False
    assert set(protocol["inventory_members"]) == INVENTORY_MEMBERS
    assert sha256(HERE / "anchor-discovery-protocol.json") == PROTOCOL_SHA256
    assert instance["discovery_protocol_hash"] == f"sha256:{PROTOCOL_SHA256}"
    assert {candidate["candidate_id"] for candidate in audit["candidates"]} == INVENTORY_MEMBERS

    environment = audit["immutable_environment"]
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    manifest_revisions = {
        package["name"].strip("«»"): package["rev"] for package in lake_manifest["packages"]
    }
    pinned = next(c for c in audit["candidates"] if c["candidate_id"].endswith("PINNED-EXTERNALS"))
    assert pinned["revisions"] == manifest_revisions
    assert pinned["searched_lean_file_count"] == 9676
    for package_dir in (LEAN_ROOT / ".lake" / "packages").iterdir():
        if not (package_dir / ".git").exists():
            continue
        assert output("git", "rev-parse", "HEAD", cwd=package_dir) == manifest_revisions[package_dir.name]
        assert output("git", "status", "--short", cwd=package_dir) == ""

    exact = next(c for c in audit["candidates"] if c["candidate_id"].endswith("EXACT-STATEMENT"))
    assert exact["classification"] == "M3_exact_statement_only"
    mathlib_exact = next(c for c in audit["candidates"] if c["candidate_id"].endswith("EXACT-TOPIC"))
    assert mathlib_exact["searched_library_lean_file_count"] == 7871
    assert mathlib_exact["classification"] == "no_exact_candidate"
    public = next(c for c in audit["candidates"] if c["candidate_id"].endswith("PUBLIC-LEAN4-RESULTS"))
    atlas = public["atlas_candidate"]
    assert atlas["revision"] == ATLAS_REVISION
    assert atlas["declaration"] == "NetworkFlow.max_flow_min_cut"
    assert atlas["classification"] == "M3_external_support_only"
    assert atlas["evidence_level"] == "no_root_E_tier_nonexact_checked_support"
    assert {row["classification"] for row in public["placeholder_blocked_projects"]} == {"M5"}
    formal_conjectures = next(
        c for c in audit["candidates"] if c["candidate_id"].endswith("FORMAL-CONJECTURES")
    )
    assert formal_conjectures["recursive_tree_entry_count"] == 1204
    assert formal_conjectures["recursive_tree_truncated"] is False
    clrs = next(c for c in audit["candidates"] if c["candidate_id"].endswith("CLRS-LEAN-PARTIAL"))
    assert clrs["project"] == "TankTechnology/CLRS-Lean"
    assert clrs["revision"] == "4fc689e2aa705703fc946eb4c26a5bb544d9f604"
    assert clrs["declaration"] == "CLRS.Chapter26.Flow.eq_cutCapacity_implies_maximal"
    clrs_source_type = (
        "{V : Type*} -> [Fintype V] -> [DecidableEq V] -> {G : FlowNetwork V} -> "
        "(phi : Flow V G) -> (S : Finset V) -> G.s in S -> G.t notin S -> "
        "phi.value = Finset.sum S (fun u => Finset.sum (S complement) "
        "(fun v => G.c u v)) -> Flow.isMaximal phi"
    )
    assert clrs["source_type"] == clrs_source_type
    assert "not elaborated locally" in clrs["source_type_status"]
    assert clrs["source_sha256"] == "6b5769df350e184fbb294ab04ddd01b3993795dffe2d08be0b64ad073152ca4c"
    assert clrs["support_source_sha256"] == "5add59ce29de71225d86d61ed951ff45ab5662f5196672415352a14d73dffe11"
    assert clrs["toolchain"] == "leanprover/lean4:v4.32.0-rc1"
    assert clrs["mathlib_revision"] == "360da6fa66c1273b76b6b2d8c5666fd5ac2e3b56"
    assert clrs["classification"] == "M3_nonexact_partial_support"
    assert clrs["evidence_level"] == "no_root_E_tier_support_only"
    zetagon = next(
        c for c in audit["candidates"] if c["candidate_id"].endswith("ZETAGON-HISTORICAL-LEAN3")
    )
    assert zetagon["project"] == "Zetagon/maxflow-mincut"
    assert zetagon["revision"] == "15f69893f60b07f55df161a567d272e2956a1741"
    assert zetagon["declaration"] == "maxflow_mincut"
    assert zetagon["source_type"].startswith(
        "{V : Type*} -> [fintype V] -> (rsn : residual_network V)"
    )
    assert "not elaborated locally" in zetagon["source_type_status"]
    assert zetagon["source_sha256"] == "2d5232751d8d22b303334c1a073c189ecd0ad616d7b86db6999a4d4a0b5767a6"
    assert zetagon["toolchain"] == "Lean 3.43.0"
    assert zetagon["mathlib_revision"] == "ad49768532540f77b87e78601821bc95f06d9546"
    assert zetagon["classification"] == "M5_wrong_backend_and_placeholders"
    assert zetagon["evidence_level"] == "no_E_tier_wrong_backend_and_placeholders"
    assert "17 active sorry" in zetagon["placeholder_and_trust_status"]

    assert external["schema_version"] == "stage1-external-anchor-snapshot/1.0"
    assert external["item_id"] == ITEM_ID and external["theorem_id"] == THEOREM_ID
    assert external["inventory_version"] == INVENTORY_VERSION
    assert external["captured_at"] == CUTOFF
    assert "inventory version 2" in external["capture_time_scope"]
    assert len(external["candidates"]) == 5
    externals = {row["candidate_id"]: row for row in external["candidates"]}
    ext_atlas = externals["M0814-EXT-ATLAS"]
    assert ext_atlas["revision"] == ATLAS_REVISION
    assert ext_atlas["source_sha256"] == ATLAS_SOURCE_SHA256
    assert ext_atlas["support_source_sha256"] == ATLAS_SUPPORT_SHA256
    assert ext_atlas["git_tree_hash"] == "c12fe2315fe475d70a4fcee81d6b731f853373ab"
    assert ext_atlas["recursive_tree_truncated"] is False
    assert ext_atlas["classification"] == "M3_external_support_only"
    assert ext_atlas["evidence_level"] == "no_root_E_tier_nonexact_checked_support"
    assert externals["M0814-EXT-GITLAB-LEAN4"]["classification"] == "M5_placeholder_blocked"
    assert externals["M0814-EXT-HISTORICAL-LEAN3"]["classification"] == "M5_wrong_backend_and_placeholders"
    ext_clrs = externals["M0814-EXT-CLRS-LEAN-PARTIAL"]
    assert ext_clrs["revision"] == clrs["revision"]
    assert ext_clrs["source_sha256"] == clrs["source_sha256"]
    assert ext_clrs["support_source_sha256"] == clrs["support_source_sha256"]
    assert ext_clrs["toolchain"] == clrs["toolchain"]
    assert ext_clrs["mathlib_revision"] == clrs["mathlib_revision"]
    assert ext_clrs["classification"] == clrs["classification"]
    assert ext_clrs["evidence_level"] == clrs["evidence_level"]
    assert ext_clrs["source_type"] == clrs["source_type"]
    assert ext_clrs["source_type_status"] == clrs["source_type_status"]
    ext_zetagon = externals["M0814-EXT-ZETAGON-LEAN3"]
    assert ext_zetagon["revision"] == zetagon["revision"]
    assert ext_zetagon["source_sha256"] == zetagon["source_sha256"]
    assert ext_zetagon["toolchain"] == zetagon["toolchain"]
    assert ext_zetagon["mathlib_revision"] == zetagon["mathlib_revision"]
    assert ext_zetagon["classification"] == zetagon["classification"]
    assert ext_zetagon["evidence_level"] == zetagon["evidence_level"]
    assert ext_zetagon["source_type"] == zetagon["source_type"]
    assert ext_zetagon["source_type_status"] == zetagon["source_type_status"]

    public_results = public["public_query_results"]
    public_hashes = {
        digest
        for row in public_results
        for digest in (
            row["response_sha256"]
            if isinstance(row["response_sha256"], list)
            else [row["response_sha256"]]
        )
    }
    assert public_hashes == {
        "85a7c7043e251af8b23ac8aecb083711f879486e48ce5ce61af7d07b61bf01df",
        "d81bedcde1b99488224c3c4aa0d132582355698f891e0be59d88ab8371fac615",
        "f6b58e0e07dba2112e4150baeae1710e6933a2df9210203c45637ccf60daa767",
        "7bfef330c6b0861fbd4633f356fb0ea78e4bee30a310263f9e3b103676c273e1",
        "85c19a8e842b06db68016918813017b46ea0f08d27310965a5ee23e05a7b8850",
        "08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2",
        "2855f82f682040661af68682e3981bd03966f6f4f52f158277419e1b192d2333",
        "1db366a292a73aaa6963398fe4e4bdb2b42e9b7a2d745a0878210569945e386e",
        "6ad861fca678f4ae31517a142f8eada4c8cfa62a1327bdd74d6bed2e52dd5017",
        "917f5454065139cc85c9b53fb4ed890303149b34c682ed5574cde71ccdf742b2",
        "d34a0c1091ce05f032d9168e47c15b2420c88270230c93b73c847455637a1bd6",
        "2d69697c0aae28a8724b7eca7948e6b2cb0d221e3c02db8f6a0b6028f17f02b5",
        "dcb56d33590b5058026a7948641557fd02710d51ed2ff6d49ff113f663eaa3d0",
    }

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"] == (
        "11/11 frozen groups semantically classified; prescribed per-query "
        "timestamp/status/count evidence incomplete"
    )
    assert result["exact_statement_candidate_located"] is True
    assert result["exact_proof_candidate_located"] is False
    assert result["credible_nonexact_lean4_candidate_located"] is True
    assert result["candidate_kernel_checked_for_own_statement"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["independent_exact_external_lean4_terminal_body_found"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["strongest_exact_root_machine_debt_after"] == "M3"
    assert result["root_evidence_level"] == "E3_from_exact_statement_only; no proof-candidate E tier"
    assert result["discovery_protocol_evidence_complete"] is False
    assert "per-query observation timestamps" in result["discovery_protocol_evidence_blocker"]
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert audit["root_vector_before"] == audit["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == [] and instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert set(instance["owned_artifacts"]) == {
        path.name for path in HERE.iterdir() if path.is_file()
    }

    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "anchor_audit" and receipt["assigned_layer"] == 2
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert validated_at >= datetime.fromisoformat(CUTOFF)
    assert validated_at <= datetime.now(timezone.utc).astimezone() + timedelta(seconds=5)
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["root_classification"] == "M3"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert any("per-query observation timestamps" in row for row in receipt["known_failures"])
    assert receipt["accepted_receipt_ids"] == []
    assert not any(re.search(r"<[^>]+>", row["command"]) for row in receipt["commands_and_results"])
    for path_string, tagged_hash in receipt["source_inputs"].items():
        algorithm, expected = tagged_hash.split(":", 1)
        assert algorithm == "sha256"
        assert sha256(ROOT / path_string) == expected, f"source hash mismatch: {path_string}"

    anchor_path = HERE / "AnchorAudit.lean"
    anchor_source = anchor_path.read_text(encoding="utf-8")
    assert sha256(anchor_path) == ANCHOR_SHA256
    for marker in (
        "def ExactTarget",
        "(HasTerminals : forall",
        "(Flow : forall",
        "#check Graph.IsLink",
        "#check Graph.IsLink.edge_mem",
        "#check Finsupp.sum",
        "#check Real.toNNReal",
        "#check IsCompact.exists_isMinOn",
        "#print ExactTarget",
    ):
        assert marker in anchor_source, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(strip_lean_comments(anchor_source))

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    actual_changed = {
        line[3:]
        for line in subprocess.check_output(
            ["git", "status", "--short", "--untracked-files=all"],
            cwd=ROOT,
            text=True,
        ).splitlines()
    }
    assert actual_changed - {"Formalizations/Lean/.lake"} == CHANGED_PATHS

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0814/AnchorAudit.lean"],
        cwd=LEAN_ROOT,
        env={**os.environ, "LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"},
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    if "def Stage1Instances.THM_M_0814_AnchorAudit.ExactTarget" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("audit target print is missing")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("anchor-audit Lean output changed")

    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    print(
        "check_anchor_audit: ok "
        "(THM-M-0814; 11 candidate groups; Atlas conditional directed support only; "
        "exact root remains M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
