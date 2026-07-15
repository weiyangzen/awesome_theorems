#!/usr/bin/env python3
"""Validate the immutable, locally checkable THM-M-0673 anchor ledger."""

from __future__ import annotations

import argparse
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
ITEM_ID = "S56-M-0673-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0673"
BASE_REVISION = "fc1568a2997ca815b767b8cc172f3d4d339bf3b9"
BASE_TREE = "635319193989301e577a430446e682952c51c538"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "3b541698da0e2b40d0cef5ea0f03ebd62538d330293e4e393ce053e000906cba"
STATEMENT_SHA256 = "131cab45507a3d3c7249d02f52f8cfbaf9d7b1c004a542e24f1bdb36be9ca424"
ANCHOR_LEAN_SHA256 = "c6c7355a3b81161df13a6afb979d54f0672068849c1cfc16850ac465d6c920d9"
PROTOCOL_SHA256 = "4dd179537f27c66505e8ad73e318c217fa35a1e4480122e98bf20748713d5ba7"
LEAN_OUTPUT_SHA256 = "660406097522f9a4bdfa24d5ba671c63a981e55e325a91c25dd301bddf451134"
MATHLIB_SOURCE_SHA256 = "ba32a045647e55dee5bc5b4534ede125eb6cc7bef523aec77dea5e980dfacd54"
MATHLIB_SOURCE_BLOB = "8c436697c7c071261251d3369b70e3882d46673a"
MATHLIB_OLEAN_SHA256 = "1ee005283e38f3d6a64eb931f3452702a4a9ba33e2fc850ef48cf665008e2865"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/README.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
    f"Stage1_Instances/{THEOREM_ID}/discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/instance.json",
    f"Stage1_Instances/{THEOREM_ID}/task-dag.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def run(*args: str, cwd: Path = ROOT, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
        env={**__import__("os").environ, "LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"},
    )


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise SystemExit(f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def without_comments_and_strings(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*", "", source)
    return re.sub(r'"(?:\\.|[^"\\])*"', '""', source)


def candidate(audit: dict, candidate_id: str) -> dict:
    return next(row for row in audit["candidates"] if row["candidate_id"] == candidate_id)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(args.worker_packet) if args.worker_packet else None

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 717
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 717
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0673-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert sha256(HERE / "discovery-protocol.json") == PROTOCOL_SHA256
    assert audit["discovery_protocol"]["sha256"] == PROTOCOL_SHA256
    assert protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID
    assert protocol["inventory_version"] == audit["inventory_version"]
    assert protocol["saturation_claim"] is audit["discovery_protocol"]["saturation_claim"] is False
    candidate_ids = [row["candidate_id"] for row in audit["candidates"]]
    assert len(candidate_ids) == len(set(candidate_ids)) == 6
    assert set(candidate_ids) == set(protocol["inventory_members"])

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "AnchorAudit.lean") == ANCHOR_LEAN_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0673.LosSentenceTarget"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False

    environment = audit["immutable_environment"]
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == environment["license_sha256"] == MATHLIB_LICENSE_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == environment["manifest_sha256"]
    assert sha256(LEAN_ROOT / "lean-toolchain") == environment["toolchain_file_sha256"]
    lake_manifest = load(LEAN_ROOT / "lake-manifest.json")
    assert len(lake_manifest["packages"]) == 11
    for package in lake_manifest["packages"]:
        directory = LEAN_ROOT / ".lake" / "packages" / package["name"].strip("«»")
        assert output("git", "rev-parse", "HEAD", cwd=directory) == package["rev"]
        assert output("git", "status", "--short", cwd=directory) == ""

    direct = candidate(audit, "M0673-C01-MATHLIB-EXACT")
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["file_blob"] == MATHLIB_SOURCE_BLOB
    assert output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB) == MATHLIB_SOURCE_BLOB
    source_path = MATHLIB / direct["file"]
    assert sha256(source_path) == direct["file_sha256"] == MATHLIB_SOURCE_SHA256
    source_lines = source_path.read_bytes().splitlines(keepends=True)
    assert sha256_bytes(b"".join(source_lines[151:158])) == direct["body_sha256"]
    assert sha256_bytes(b"".join(source_lines[145:150])) == candidate(
        audit, "M0673-C02-MATHLIB-FORMULA-BRIDGE"
    )["body_sha256"]
    assert sha256_bytes(b"".join(source_lines[93:144])) == candidate(
        audit, "M0673-C03-MATHLIB-BOUNDED-FORMULA-TERMINAL"
    )["body_sha256"]
    olean = MATHLIB / ".lake/build/lib/lean/Mathlib/ModelTheory/Ultraproducts.olean"
    assert olean.is_file() and olean.stat().st_size == environment["compiled_module_bytes"]
    assert sha256(olean) == environment["compiled_module_sha256"] == MATHLIB_OLEAN_SHA256
    assert direct["classification"] == "M0-W_candidate"
    assert direct["evidence_level"] == "E2_nonrelease_worker_probe"

    source = source_path.read_text(encoding="utf-8")
    for marker in (
        "theorem boundedFormula_realize_cast",
        "theorem realize_formula_cast",
        "theorem sentence_realize",
        "Classical.epsilon fun m : M a",
        "rw [← realize_formula_cast φ, iff_eq_eq]",
    ):
        assert marker in source, marker
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|extern|proof_wanted|native_decide)\b|"
        r"^\s*(?:axiom|constant|unsafe|opaque)\b",
        re.MULTILINE,
    )
    assert forbidden.search(without_comments_and_strings("".join(source.splitlines(True)[93:158]))) is None

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "theorem exactTarget_mathlib_candidate",
        "exact FirstOrder.Language.Ultraproduct.sentence_realize phi",
        "assert_no_sorry FirstOrder.Language.Ultraproduct.sentence_realize",
        "#print axioms exactTarget_mathlib_candidate",
        "NameSet.transitivelyUsedConstants",
        "ANCHOR_CLOSURE bodyless_nonaxioms=",
        "ANCHOR_CLOSURE unsafe=",
    ):
        assert marker in adapter, marker
    adapter_code = without_comments_and_strings(adapter)
    adapter_code = re.sub(r"^.*(?:assert_no_sorry|#print sorries).*$", "", adapter_code, flags=re.MULTILINE)
    assert forbidden.search(adapter_code) is None

    probe = direct["machine_probe"]
    assert probe["output_sha256"] == LEAN_OUTPUT_SHA256
    assert probe["reported_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert probe["transitive_declaration_closure_count"] == 5075
    assert probe["transitive_module_count"] == 190
    assert probe["transitive_bodyless_nonaxioms"] == []
    assert probe["transitive_unsafe_declarations"] == []

    foundation = candidate(audit, "M0673-C05-FOUNDATION-MISMATCH")
    assert foundation["classification"] == "M5_statement_and_integration_mismatch"
    assert foundation["file_blob"] == "bf156dcc0034dc5b1c1368d5a17f3d55e2a9507b"
    assert foundation["file_sha256"] == "dd0b42abd4e248585b22449828b8742908359d0cb81e0b0c505cccb927d631a6"
    assert "equality-free" in foundation["statement_mismatch"]
    assert "raw dependent-function" in foundation["statement_mismatch"]
    assert candidate(audit, "M0673-C06-MATHLIB3-HISTORICAL")["classification"].startswith("M3_")

    provenance = audit["proof_body_provenance"]
    assert provenance["local_role"] == "wrapper"
    assert provenance["terminal_declaration"] == direct["terminal_declaration"]
    assert provenance["transitive_trust_closure_hash"] is None
    port = provenance["historical_lineage"]
    assert port["lean4_port_tree"] == output(
        "git", "rev-parse", f"{port['lean4_port_commit']}^{{tree}}", cwd=MATHLIB
    )
    historic = subprocess.check_output(
        ["git", "show", f"{port['lean4_port_commit']}:{direct['file']}"], cwd=MATHLIB
    )
    assert sha256_bytes(historic) == port["lean4_port_source_sha256"]
    assert run(
        "git", "merge-base", "--is-ancestor", port["lean4_port_commit"], MATHLIB_REVISION,
        cwd=MATHLIB,
    ).returncode == 0

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("6/6 frozen candidates")
    assert result["exact_candidate_located"] is True
    assert result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M0-W"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["root_evidence_level"] == "E2_nonrelease_worker_probe"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is False and result["theorem_complete"] is False

    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["statement_fingerprints"] == [f"sha256:{EXPRESSION_SHA256}"]
    assert receipt["anchor_audit_lean_sha256"] == f"sha256:{ANCHOR_LEAN_SHA256}"
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["candidate_result"]["classification"] == "M0-W_candidate"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["candidate_result"]["bodyless_nonaxioms"] == []
    assert receipt["candidate_result"]["unsafe_declarations"] == []
    assert receipt["root_vector_before"] == receipt["accepted_root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4",
    }
    assert receipt["root_candidate_vector_after"] == {"H": "H1", "M": "M0-W", "R": "R4"}
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False

    if packet is not None:
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]

        actual_changed = {".stage1-worker-selftest.json"}
        status = subprocess.check_output(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT, text=True
        )
        for line in status.splitlines():
            path = line[3:]
            if path == "Formalizations/Lean/.lake":
                continue
            if path != ".stage1-worker-selftest.json" and not path.startswith(
                f"Stage1_Instances/{THEOREM_ID}/"
            ):
                raise SystemExit(f"changed path outside worker ownership: {path}")
            actual_changed.add(path)
        assert actual_changed == CHANGED_PATHS

    lean = run(
        "lake", "env", "lean", "--trust=0",
        "../../Stage1_Instances/THM-M-0673/AnchorAudit.lean", cwd=LEAN_ROOT,
    )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    if lean.stdout.count("Declarations are sorry-free!") != 4:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected sorry reports")
    for expected in (
        "ANCHOR_CLOSURE declarations=5075 modules=190",
        "ANCHOR_CLOSURE axioms=[propext, Classical.choice, Quot.sound]",
        "ANCHOR_CLOSURE bodyless_nonaxioms=[]",
        "ANCHOR_CLOSURE unsafe=[]",
    ):
        if expected not in lean.stdout:
            sys.stdout.write(lean.stdout)
            raise SystemExit(f"missing Lean closure report: {expected}")
    if sha256_bytes(lean.stdout.encode()) != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0673; 6 candidates classified; exact pinned mathlib M0-W candidate/E2; "
        "accepted root remains M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
