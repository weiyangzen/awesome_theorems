#!/usr/bin/env python3
"""Validate the locally replayable THM-M-0957 anchor-audit packet."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0957-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0957"
BASE_REVISION = "b243ebc0f9058ba5afafef8240b92c2dfb2edc6e"
BASE_TREE = "b4b092069141ac54ea1ab5a6ea946192a30ec78c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "e611db43ce6f3419553e3ebe0fe85a3ce89e4d3930b3842f5a09be8a7683d2ed"
STATEMENT_SHA256 = "b4bda6c926b0568d8b244623c12b4784651d55a9eb7df9d9ba3f512ed2cd9e46"
ANCHOR_PROBE_SHA256 = "d53ccd43676ecbea514eddd6ad4d225eff05516854091cee19f7e81cdd7e7dcd"
LEAN_OUTPUT_SHA256 = "782637a17d30fd6035a11f35e536d234400e4d4653ca80b9bd7f345845de2404"
DISCOVERY_SHA256 = "2f7789d1f4fd8f64ccf6ada594bd092f1bbfccc568916a2df7ed380ac6805c9b"
MATHLIB_SOURCE_SHA256 = "1f8c1813a75c722ee4d62d63185c53d0b52d27691e531c05e0ecb6c10c15cf65"
MATHLIB_SOURCE_BLOB = "7d3eb0e603040dcd72fe35e39c82f4d615b3e254"
MATHLIB_DEFS_SHA256 = "b325fb632a5398208995fa5beae71c47798086e588f98e46679aa81b923b28e3"
MATHLIB_DEFS_BLOB = "534177a2aa83fa462689226e248953fe38f2e1cc"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
MATHLIB_OLEAN_SHA256 = "620e1ce9b071dd2049ce734f4e58bc1e2bbdb6fb9bf9f6e17f1b39ad34bb720f"
SOURCE_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json":
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md":
        "eebd1b53e93f5cc4a8fc607f6f20e4a7c27b5271cd4b9276deccf19239a87cd8",
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "ba409ac34b332b91d46aad561739fb24b4946690af5860fce7e942a7ebaeeaf2",
    "skills/execute-stage1-rev56/SKILL.md":
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md":
        "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Formalizations/Lean/lean-toolchain":
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json":
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    f"Stage1_Instances/{THEOREM_ID}/Statement.lean": STATEMENT_SHA256,
    f"Stage1_Instances/{THEOREM_ID}/statement.json":
        "b70cb423c41c9d822b85696a57193ca0fc2dc26fe88b2a471bb68f6a9cb8dfab",
    f"Stage1_Instances/{THEOREM_ID}/statement-receipt.json":
        "bcccea3c146b6aec3b9332d6be59d6bc7b2fea497fc78a7008fe2e19a2057608",
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


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def without_comments_and_strings(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*", "", source)
    return re.sub(r'"(?:\\.|[^"\\])*"', '""', source)


def candidate(audit: dict, candidate_id: str) -> dict:
    return next(row for row in audit["candidates"] if row["candidate_id"] == candidate_id)


def canonical_expression() -> str:
    """Freshly serialize the canonical declaration using the statement phase's marker."""
    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    marker = "#print Stage1Instances.THM_M_0957.BehrendConstructionTarget"
    assert source.count(marker) == 1
    with tempfile.NamedTemporaryFile("w", suffix=".lean", encoding="utf-8", delete=False) as stream:
        stream.write(source)
        path = Path(stream.name)
    try:
        result = subprocess.run(
            ["lake", "env", "lean", str(path)], cwd=LEAN_ROOT, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180, check=False,
        )
    finally:
        path.unlink()
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    match = re.search(
        r"def Stage1Instances\.THM_M_0957\.BehrendConstructionTarget : Prop :=\n(?P<expression>.*)\Z",
        result.stdout, re.DOTALL,
    )
    if match is None:
        sys.stdout.write(result.stdout)
        raise SystemExit("could not serialize canonical statement")
    return match.group("expression").strip()


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
    assert audit["execution_rank"] == 1491
    assert audit["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is receipt["content_addressed"] is False
    assert receipt["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert receipt["verdict"] == "no_state_change"
    assert receipt["depends_on"] == ["S56-M-0957-STATEMENT"]
    assert receipt["first_failed_gate"] == (
        "dependency_ordered_master_acceptance_of_provisional_statement_prerequisite_and_anchor_audit"
    )
    assert receipt["accepted_receipt_ids"] == audit["accepted_receipt_ids"] == []
    assert set(receipt["changed_paths"]) == set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["item_id"] == ITEM_ID and packet["base_revision"] == BASE_REVISION
    assert packet["known_failures"] == receipt["known_failures"]
    assert receipt["source_inputs"] == {
        path: f"sha256:{digest}" for path, digest in SOURCE_INPUTS.items()
    }
    for path, digest in SOURCE_INPUTS.items():
        assert sha256(ROOT / path) == digest, f"stale source input: {path}"

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1491
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == 1491
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]" and item["depends_on"] == ["S56-M-0957-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    formal = statement["canonical_formal_target"]
    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert hashlib.sha256(canonical_expression().encode()).hexdigest() == EXPRESSION_SHA256
    assert sha256(HERE / "AnchorAudit.lean") == ANCHOR_PROBE_SHA256
    assert receipt["immutable_inputs"]["anchor_probe_sha256"] == ANCHOR_PROBE_SHA256

    assert sha256(HERE / "anchor-discovery-protocol.json") == DISCOVERY_SHA256
    discovery = audit["discovery_protocol"]
    assert discovery["sha256"] == DISCOVERY_SHA256
    assert discovery["inventory_version"] == protocol["inventory_version"]
    assert protocol["frozen_before_candidate_classification"] is True
    assert protocol["saturation_claim"] is discovery["saturation_claim"] is False
    candidate_ids = {row["candidate_id"] for row in audit["candidates"]}
    assert candidate_ids == set(protocol["inventory_members"])
    assert len(candidate_ids) == 7

    environment = audit["immutable_environment"]
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == environment["manifest_sha256"]
    assert sha256(LEAN_ROOT / "lean-toolchain") == environment["toolchain_file_sha256"]
    assert sha256(MATHLIB / "LICENSE") == environment["mathlib_license_sha256"] == MATHLIB_LICENSE_SHA256

    direct = candidate(audit, "M0957-C01-MATHLIB-TERMINAL-BOUNDS")
    source = MATHLIB / direct["file"]
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["file_blob"] == MATHLIB_SOURCE_BLOB
    assert output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB) == MATHLIB_SOURCE_BLOB
    assert sha256(source) == direct["file_sha256"] == MATHLIB_SOURCE_SHA256
    olean = MATHLIB / ".lake/build/lib/lean/Mathlib/Combinatorics/Additive/AP/Three/Behrend.olean"
    assert sha256(olean) == direct["compiled_olean_sha256"] == MATHLIB_OLEAN_SHA256
    assert direct["candidate_classification"] == "M5_statement_mismatch_root_candidate"
    assert direct["partial_family_classification"] == "M2_candidate_partial_restricted_family"
    assert direct["machine_probe"]["output_sha256"] == LEAN_OUTPUT_SHA256
    assert direct["machine_probe"]["reported_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert direct["machine_probe"]["transitive_declaration_closure_count"] == 28265
    assert direct["machine_probe"]["transitive_module_count"] == 1079
    assert direct["machine_probe"]["transitive_bodyless_nonaxioms"] == []
    assert direct["machine_probe"]["transitive_unsafe_declarations"] == []

    defs = MATHLIB / "Mathlib/Combinatorics/Additive/AP/Three/Defs.lean"
    assert output(
        "git", "rev-parse", "HEAD:Mathlib/Combinatorics/Additive/AP/Three/Defs.lean", cwd=MATHLIB
    ) == MATHLIB_DEFS_BLOB
    assert sha256(defs) == MATHLIB_DEFS_SHA256
    mathlib_source = source.read_text(encoding="utf-8")
    for marker in (
        "theorem threeAPFree_image_sphere",
        "theorem card_sphere_le_rothNumberNat",
        "theorem bound_aux (hd : d ≠ 0) (hn : 2 ≤ n)",
        "theorem roth_lower_bound_explicit (hN : 4096 ≤ N)",
        "theorem roth_lower_bound : (N : ℝ) * exp (-4 * √(log N)) ≤ rothNumberNat N",
    ):
        assert marker in mathlib_source, marker
    route = "\n".join(mathlib_source.splitlines()[180:489])
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|opaque|native_decide|implemented_by|extern)\b"
        r"|\bunsafe\s+(?:def|theorem|instance)\b"
    )
    assert forbidden.search(without_comments_and_strings(route)) is None

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "def MathlibExplicitTarget : Prop",
        "def MathlibAllNTarget : Prop",
        "theorem historicalConstantAtOne_lt_mathlibConstant",
        "theorem mathlibCandidate_restricted",
        "assert_no_sorry Behrend.roth_lower_bound_explicit",
        "assert_no_sorry mathlibCandidate_restricted",
        "#print_anchor_closure",
    ):
        assert marker in adapter, marker
    assert forbidden.search(without_comments_and_strings(adapter)) is None

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("7/7 frozen inventory candidates")
    assert result["exact_candidate_located"] is False
    assert result["partial_candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == (
        "M3_with_prospective_M2_partial_family_pending_obligation_freeze"
    )
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is result["theorem_complete"] is False
    before = {"H": "H1", "M": "M3", "R": "R3"}
    assert audit["root_vector_before"] == audit["accepted_root_vector_after"] == before
    assert receipt["root_vector_before"] == receipt["accepted_root_vector_after"] == before
    assert audit["root_candidate_vector_after"] == receipt["root_candidate_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }
    assert audit["audit_complete"] is receipt["audit_complete"] is False
    assert audit["theorem_complete"] is receipt["theorem_complete"] is False
    assert audit["gate_state"] == "worker_self_tested_pending_dependency_ordered_master_acceptance"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256

    lean_environment = os.environ.copy()
    lean_environment.update({"LC_ALL": "C", "TZ": "UTC"})
    lean = subprocess.run(
        ["lake", "env", "lean", "--trust=0", f"../../Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean"],
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
    if lean.stdout.count("Declarations are sorry-free!") != 9:
        sys.stdout.write(lean.stdout)
        raise SystemExit("expected nine machine-produced sorry-free reports")
    normalized = re.sub(r"\s+", " ", lean.stdout)
    axiom_reports = re.findall(r"depends on axioms: \[([^]]*)\]", normalized)
    if axiom_reports != ["propext, Classical.choice, Quot.sound"] * 9:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected candidate/adapter axiom report")
    for marker in (
        "Behrend.roth_lower_bound_explicit",
        "Behrend.roth_lower_bound",
        "ANCHOR_CLOSURE declarations=28265 modules=1079",
        "ANCHOR_CLOSURE axioms=[propext, Classical.choice, Quot.sound]",
        "ANCHOR_CLOSURE bodyless_nonaxioms=[]",
        "ANCHOR_CLOSURE unsafe=[]",
    ):
        if marker not in lean.stdout:
            sys.stdout.write(lean.stdout)
            raise SystemExit(f"missing Lean evidence marker: {marker}")
    if "sorryAx" in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("Lean output contains a proof placeholder")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0957; 7 candidates classified; no exact root candidate; "
        "prospective partial pinned mathlib family; root H1/M3/R3; "
        "audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
