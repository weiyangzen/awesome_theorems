#!/usr/bin/env python3
"""Validate the immutable, locally checkable THM-M-0030 anchor ledger."""

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
ITEM_ID = "S56-M-0030-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0030"
BASE_REVISION = "7e54c0fcaf9c0e53fa7afbbeb0a36218152f932c"
BASE_TREE = "80ece87e35401b07ba76abc36ea83440b5fa7f31"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "53389852e2c0875086c2c28cb4a60448670ee29145e13d86b4b1ad3e9df8861e"
STATEMENT_SHA256 = "737a2cf8a656d39617aecf8aa7d8b2bb3d5739807ea34f6e75dbb833f3c6978e"
PROTOCOL_SHA256 = "19dd018cf76446992cb59d3a46d054e71b65c37742a79a01e6fb3e7a81965fe2"
LEAN_OUTPUT_SHA256 = "b038ca1119581f32388d4740794a4611288c128729a43b19e12715ad4726b6c0"
BLUEPRINT_SHA256 = "47b6b1f8847369db69b034fa18d58a8edb0c857d7e4ec691436418cb5970c12a"
EXECUTION_SHA256 = "c62868b81cf74e4f695115f2bfd69d2fec5b944fa126e71ae09ea9f6fceeeb35"
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
    f"Stage1_Instances/{THEOREM_ID}/scope-map.md",
    f"Stage1_Instances/{THEOREM_ID}/source-statement-crosswalk.md",
    f"Stage1_Instances/{THEOREM_ID}/task-dag.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def normalize_generated_proofs(expression: str) -> str:
    expression = re.sub(r"@[A-Za-z0-9_'.]+\._proof_[0-9]+", "@<generated-proof>", expression)
    return " ".join(expression.split())


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert sha256(ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md") == BLUEPRINT_SHA256
    assert sha256(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json") == EXECUTION_SHA256
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1075
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID
    assert protocol["saturation_claim"] is False
    assert sha256(HERE / "discovery-protocol.json") == PROTOCOL_SHA256
    assert audit["discovery_protocol"]["sha256"] == PROTOCOL_SHA256

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1075
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0030-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    anchored = instance["anchor_audit"]
    assert anchored["item_id"] == ITEM_ID
    assert anchored["candidate_classification"] == "M0-W"
    assert anchored["candidate_evidence_level"] == "E2"
    assert anchored["candidate_master_accepted"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]
    lake_manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(package for package in lake_manifest["packages"] if package["name"] == "mathlib")
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert mathlib_pin["url"] == env["mathlib_remote"]
    assert len(lake_manifest["packages"]) == 11
    for package in lake_manifest["packages"]:
        directory_name = package["name"].strip("«»")
        package_path = LEAN_ROOT / ".lake" / "packages" / directory_name
        assert output("git", "rev-parse", "HEAD", cwd=package_path) == package["rev"]
        assert output("git", "status", "--short", cwd=package_path) == ""

    candidates = audit["candidates"]
    ids = [candidate["candidate_id"] for candidate in candidates]
    assert len(ids) == len(set(ids)) == 6
    direct = next(c for c in candidates if c["candidate_id"] == "M0030-C01-MATHLIB-EXACT")
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["file_blob"] == output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB)
    source_path = MATHLIB / direct["file"]
    assert sha256(source_path) == direct["file_sha256"]
    source_lines = source_path.read_bytes().splitlines(keepends=True)
    assert sha256_bytes(b"".join(source_lines[429:435])) == direct["body_sha256"]
    assert sha256_bytes(b"".join(source_lines[391:435])) == audit["proof_body_provenance"]["current_slice_sha256"]
    assert direct["declaration"] == "Ideal.iInf_pow_eq_bot_of_isLocalRing"
    assert direct["classification"] == "M0-W" and direct["evidence_level"] == "E2"

    source = source_path.read_text(encoding="utf-8")
    for marker in (
        "theorem Ideal.mem_iInf_smul_pow_eq_bot_iff",
        "theorem Ideal.iInf_pow_smul_eq_bot_of_le_jacobson",
        "theorem Ideal.iInf_pow_smul_eq_bot_of_isLocalRing",
        "theorem Ideal.iInf_pow_eq_bot_of_isLocalRing",
        "convert I.iInf_pow_smul_eq_bot_of_isLocalRing (M := R) h",
        "rw [smul_eq_mul, ← Ideal.one_eq_top, mul_one]",
    ):
        assert marker in source, marker
    scoped_body = without_comments("".join(source.splitlines(keepends=True)[391:435]))
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque|proof_wanted|implemented_by|extern)\b"
    )
    assert not forbidden.search(scoped_body)

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "forall {R : Type u} [CommRing R] [IsNoetherianRing R] [IsLocalRing R]",
        "theorem exactTarget_mathlib_candidate : ExactTarget",
        "exact Ideal.iInf_pow_eq_bot_of_isLocalRing I hI",
        "#print sorries Ideal.iInf_pow_eq_bot_of_isLocalRing",
        "#print axioms exactTarget_mathlib_candidate",
    ):
        assert marker in adapter, marker
    assert not forbidden.search(without_comments(adapter))

    external = audit["external_search"]
    assert external["sourcegraph_exact_declaration_query"]["result"].startswith(
        "done=true, skipped=[], 11 matches"
    )
    assert audit["discovery_protocol"]["saturation_claim"] is False
    assert next(c for c in candidates if c["candidate_id"] == "M0030-C05-ATLAS-CONSUMERS")[
        "classification"
    ] == "M3_external_consumers_only"
    assert next(c for c in candidates if c["candidate_id"] == "M0030-C06-FLT-CONSUMERS")[
        "classification"
    ] == "M3_external_consumers_only"

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("6/6 frozen candidates")
    assert result["exact_candidate_located"] is True
    assert result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M0-W"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["root_evidence_level"] == "E2"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is False and result["theorem_complete"] is False

    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["classification"] == "M0-W"
    assert receipt["candidate_result"]["evidence_level"] == "E2"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]

    actual_changed = {".stage1-worker-selftest.json"}
    status = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
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

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0030/AnchorAudit.lean"],
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
    if lean.stdout.count("Declarations are sorry-free!") != 3:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected sorry reports for the three audited declarations")
    for axiom in ("propext", "Classical.choice", "Quot.sound"):
        if lean.stdout.count(axiom) != 4:
            sys.stdout.write(lean.stdout)
            raise SystemExit(f"unexpected {axiom} report count")
    if "theorem Ideal.iInf_pow_eq_bot_of_isLocalRing" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("terminal transparent proof body was not printed")
    exact_target = re.search(
        r"def Stage1Instances\.THM_M_0030_AnchorAudit\.ExactTarget\.\{u\} : Prop :=\n"
        r"(?P<expression>.*)\Z",
        lean.stdout,
        re.DOTALL,
    )
    if exact_target is None:
        sys.stdout.write(lean.stdout)
        raise SystemExit("could not extract audit target expression")
    if normalize_generated_proofs(exact_target.group("expression")) != normalize_generated_proofs(
        formal["fully_explicit_expression"]
    ):
        sys.stdout.write(lean.stdout)
        raise SystemExit("audit target differs from frozen statement after generated-proof normalization")
    if sha256_bytes(lean.stdout.encode()) != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0030; 6 candidates classified; exact pinned mathlib wrapper M0-W/E2; "
        "accepted root remains M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
