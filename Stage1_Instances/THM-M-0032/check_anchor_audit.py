#!/usr/bin/env python3
"""Validate the immutable, bounded THM-M-0032 anchor inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0032-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0032"
BASE_REVISION = "4ecdda4863162748b3ee70bc4ec842789418145d"
BASE_TREE = "aace54662cd5e9ca38472011f41afdbffdedfa04"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "199d16d669438ea6e1cd556adbc4a9475805acf048379e01ae1a1f75f453a8d8"
STATEMENT_SHA256 = "5391ab5cef4895413e28fcabe5a3e23e7b93aeea643c1fbae991223c34c07f3a"
LEAN_OUTPUT_SHA256 = "8d3b1018d6ad7a7fc5dd1cdcfdb53ad9a83146347c8d7a9a82e128f937c9968f"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.md",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
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


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    target_manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1076 and audit["phase"] == "anchor_audit"
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in target_manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1076
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0032-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert audit["canonical_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]

    candidates = {candidate["candidate_id"]: candidate for candidate in audit["candidates"]}
    assert set(candidates) == {
        "M0032-C01-MATHLIB-SUPPORT",
        "M0032-C02-ATLAS-ADMITTED",
        "M0032-C03-ATLAS-DUPLICATE-ADMITTED",
        "M0032-C04-REGULAR-LOCAL-RINGS-PARTIAL",
        "M0032-C05-FORMAL-CONJECTURES-NEGATIVE",
    }
    support = candidates["M0032-C01-MATHLIB-SUPPORT"]
    assert support["candidate_classification"] == "M3_support_only"
    for file, blob in support["source_blobs"].items():
        assert output("git", "rev-parse", f"HEAD:{file}", cwd=MATHLIB) == blob

    regular_defs = (MATHLIB / "Mathlib/RingTheory/RegularLocalRing/Defs.lean").read_text()
    assert "class IsRegularLocalRing" in regular_defs
    assert "[IsLocalRing R] [IsDomain R] [IsPrincipalIdealRing R] : IsRegularLocalRing R" in regular_defs
    assert "UniqueFactorizationMonoid" not in regular_defs
    kaplansky = (MATHLIB / "Mathlib/RingTheory/UniqueFactorizationDomain/Kaplansky.lean").read_text()
    assert "public theorem iff_exists_prime_mem_of_isPrime" in kaplansky
    pid = (MATHLIB / "Mathlib/RingTheory/PrincipalIdealDomain.lean").read_text()
    assert "to_uniqueFactorizationMonoid : UniqueFactorizationMonoid R" in pid

    atlas = candidates["M0032-C02-ATLAS-ADMITTED"]
    duplicate = candidates["M0032-C03-ATLAS-DUPLICATE-ADMITTED"]
    assert atlas["revision"] == "34ffed396f376454c1a9b297f3fd74c5c801fb50"
    assert atlas["tree"] == "c12fe2315fe475d70a4fcee81d6b731f853373ab"
    assert atlas["terminal_proof_body"] == "by sorry"
    assert atlas["placeholder_count_in_file"] == 3
    assert atlas["candidate_classification"] == "M5_placeholder"
    assert "[IsDomain R]" in atlas["type"]
    assert duplicate["terminal_proof_body"] == "by sorry"
    assert duplicate["candidate_classification"] == "M5_placeholder_duplicate"
    assert atlas["file_sha256"] == "15b91d6faa1295bfb06e62f01d032fd39de265a05fb592842037f7aab7f107c8"
    assert duplicate["file_sha256"] == "6b09c9bb15e8137100657a980dca5325deb9c865a35791b1bcb7de543c9fc035"

    partial = candidates["M0032-C04-REGULAR-LOCAL-RINGS-PARTIAL"]
    assert partial["revision"] == "ea5a55ef4d5ce3618aea38376981c5a5eb33b7f0"
    assert partial["tree"] == "f0f6a6c02898b1eeeedf78acda7b2dc05d484195"
    assert partial["terminal_target_found"] is False
    assert partial["candidate_classification"] == "M3_partial_support"
    assert partial["file_sha256"] == "90ed0a20076cfbcec091023fab50b1e6e447626d684fe311308c3b6632d69a90"
    negative = candidates["M0032-C05-FORMAL-CONJECTURES-NEGATIVE"]
    assert negative["tree_entry_count"] == 1204
    assert negative["candidate_classification"] == "no_candidate"

    searches = {row["surface"] + ":" + row["query"]: row for row in audit["external_searches"]}
    assert len(searches) == 7
    assert any("HTTP 401" in row["result"] for row in searches.values())
    assert any("HTTP 503" in row["result"] for row in searches.values())
    assert audit["discovery_protocol"]["frozen_before_candidate_classification"] is True
    assert audit["discovery_protocol"]["saturation_claim"] is False

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("5/5 candidate records classified")
    assert result["exact_placeholder_free_candidate_located"] is False
    assert result["external_terminal_proof_found"] is False
    assert result["eligible_repo_local_integration_debt"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_debt_after"] == "M3"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert audit["theorem_complete"] is False

    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["candidate_result"]["classified_records"] == 5
    assert receipt["candidate_result"]["exact_placeholder_free_candidate_found"] is False
    assert receipt["candidate_result"]["accepted_root_classification"] == "M3"
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False

    required_packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet) == required_packet_fields
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]

    probe = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "forall (R : Type u) [CommRing R] [IsRegularLocalRing R]",
        "#check UniqueFactorizationMonoid.iff_exists_prime_mem_of_isPrime",
        "#check IsPrincipalIdealRing.of_prime_ne_bot",
        "#check PrincipalIdealRing.to_uniqueFactorizationMonoid",
        "#check_failure (inferInstance : UniqueFactorizationMonoid R)",
        "#print ExactTarget",
    ):
        assert marker in probe, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(probe))

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0032/AnchorAudit.lean"],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    if "failed to synthesize instance of type class\n  UniqueFactorizationMonoid R" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("expected negative synthesis evidence is missing")
    if "def Stage1Instances.THM_M_0032_AnchorAudit.ExactTarget.{u} : Prop" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("exact target print is missing")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("anchor probe output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0032; 5 classified records; no eligible terminal proof; "
        "root remains M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
