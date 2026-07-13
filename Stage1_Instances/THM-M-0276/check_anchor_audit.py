#!/usr/bin/env python3
"""Validate the locally replayable core of the THM-M-0276 anchor-audit packet."""

from __future__ import annotations

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
ITEM_ID = "S56-M-0276-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0276"
BASE_REVISION = "fcabbf1e0ad9507eebe91663bccabfa87d22813e"
BASE_TREE = "873e589c594454b7f263c7ed2342089a4d15e842"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "0cfb9796471903d081ad67551a3f9c2c3414cce1f7adbf79394d364a467c82fa"
NAMED_ROOT_SHA256 = "ec2954c0a55ee364e73f3b49407d1ef62ba1ff03807b1e53771181ef27f04d80"
STATEMENT_SHA256 = "ede62e0c7bbf3804f6a81c2f1115643048c69ced4750453af7e8ebd845c6aeea"
LEAN_OUTPUT_SHA256 = "a58da843bc1a208e3317a8333dcc5c120ff8b466d97cbb56727505f5819e04fb"
DISCOVERY_SHA256 = "d5f2cb54bd2d44214bf6a21b454bbcc59f3059b2f7450b3c51a7a8312f20bb57"
MATHLIB_SOURCE_SHA256 = "b046e38a239014c32e2313b4a216edd89198e57351d9c6068a3de7811680bf6c"
MATHLIB_SOURCE_BLOB = "8d4361a5bdf07bb8b7e2214ee59340f9931422bd"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
SOURCE_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json":
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md":
        "8607034eed9f13cd5759de5cd2bc4d41d34a1ed073e6ab07c4b6b3689edde46d",
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "d342e206b1372121057707b034f58b10e2dca2cb3a8468577219af0050dc2f53",
    "skills/execute-stage1-rev56/SKILL.md":
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain":
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json":
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    f"Stage1_Instances/{THEOREM_ID}/Statement.lean": STATEMENT_SHA256,
}
ATLAS_REVISION = "34ffed396f376454c1a9b297f3fd74c5c801fb50"
ATLAS_SOURCE_SHA256 = "4e754597f07d99a417822c61d77090ab08b8b3c799c67f633a6aef59dbbdff80"
OPTLIB_REVISION = "03124b75df1422afed0a96e370f0e258589650ba"
OPTLIB_SOURCE_SHA256 = "bbf6fe54cc1d0b9f7901051cf5f05f88f7d57da85a5f55bcc7957be602d31db7"
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


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*", "", source)
    return re.sub(r'"(?:\\.|[^"\\])*"', '""', source)


def candidate(audit: dict, candidate_id: str) -> dict:
    return next(row for row in audit["candidates"] if row["candidate_id"] == candidate_id)


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
    assert audit["execution_rank"] == 1282
    assert audit["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is receipt["content_addressed"] is False
    assert receipt["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert receipt["verdict"] == "no_state_change"
    assert receipt["depends_on"] == ["S56-M-0276-STATEMENT"]
    assert receipt["first_failed_gate"] == (
        "master_acceptance_of_provisional_statement_prerequisite_and_anchor_audit"
    )
    assert receipt["accepted_receipt_ids"] == audit["accepted_receipt_ids"] == []
    assert set(receipt["changed_paths"]) == set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["item_id"] == ITEM_ID and packet["base_revision"] == BASE_REVISION
    assert packet["known_failures"] == receipt["known_failures"]
    assert any(
        "not retained in this provisional packet" in failure
        for failure in receipt["known_failures"]
    )
    assert receipt["source_inputs"] == {
        path: f"sha256:{digest}" for path, digest in SOURCE_INPUTS.items()
    }
    for path, digest in SOURCE_INPUTS.items():
        assert sha256(ROOT / path) == digest, f"stale source input: {path}"

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1282
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == 1282
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]" and item["depends_on"] == ["S56-M-0276-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    formal = statement["canonical_formal_target"]
    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_named_root_expression_sha256"] == NAMED_ROOT_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["named_root_expression_sha256"] == NAMED_ROOT_SHA256
    assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean") == STATEMENT_SHA256

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

    direct = candidate(audit, "M0276-C01-MATHLIB-DIRECT")
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["file_blob"] == MATHLIB_SOURCE_BLOB
    assert output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB) == MATHLIB_SOURCE_BLOB
    assert sha256(MATHLIB / direct["file"]) == direct["file_sha256"] == MATHLIB_SOURCE_SHA256
    assert direct["declaration"] == "ContinuousLinearMap.isOpenMap"
    assert direct["local_adapter"].endswith("exactTarget_mathlib_candidate")
    assert direct["candidate_classification"] == "M1" and direct["evidence_level"] == "E2"
    assert direct["principal_direct_proof_dependencies"] == [
        "ContinuousLinearMap.exists_preimage_norm_le",
        "Metric.isOpen_iff",
        "Set.mem_image_of_mem",
        "ContinuousLinearMap.map_add",
    ]
    assert direct["machine_probe"]["output_sha256"] == LEAN_OUTPUT_SHA256
    assert direct["machine_probe"]["reported_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert direct["machine_probe"]["transitive_declaration_closure_count"] == 17187
    assert direct["machine_probe"]["transitive_module_count"] == 654
    assert direct["machine_probe"]["transitive_bodyless_nonaxioms"] == []
    assert direct["machine_probe"]["transitive_unsafe_declarations"] == []

    history = direct["historical_provenance"]
    for prefix in ("lean4_port", "semilinear_generalization"):
        revision = history[f"{prefix}_commit"]
        assert history[f"{prefix}_tree"] == output("git", "rev-parse", f"{revision}^{{tree}}", cwd=MATHLIB)
        assert output("git", "merge-base", "--is-ancestor", revision, MATHLIB_REVISION, cwd=MATHLIB) == ""

    mathlib_source = (MATHLIB / direct["file"]).read_text(encoding="utf-8")
    for marker in (
        "theorem exists_approx_preimage_norm_le (surj : Surjective f)",
        "⋃ n : ℕ, closure (f '' ball 0 n) = Set.univ",
        "nonempty_interior_of_iUnion_of_closed",
        "theorem exists_preimage_norm_le (surj : Surjective f)",
        "obtain ⟨C, C0, hC⟩ := exists_approx_preimage_norm_le f surj",
        "protected theorem isOpenMap (surj : Surjective f) : IsOpenMap f",
        "rcases exists_preimage_norm_le f surj with ⟨C, Cpos, hC⟩",
        "theorem isQuotientMap (surj : Surjective f) : IsQuotientMap f",
    ):
        assert marker in mathlib_source, marker
    visible_route = "\n".join(mathlib_source.splitlines()[78:252])
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque|native_decide|implemented_by|extern)\b"
    )
    assert forbidden.search(without_comments(visible_route)) is None

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "def ExpandedExactTarget : Prop",
        "theorem exactTarget_iff_expandedExactTarget",
        "theorem exactTarget_mathlib_candidate : ExactTarget",
        "exact ContinuousLinearMap.isOpenMap f hf",
        "assert_no_sorry ContinuousLinearMap.isOpenMap",
        "assert_no_sorry exactTarget_mathlib_candidate",
        "#print_anchor_closure",
    ):
        assert marker in adapter, marker
    assert forbidden.search(without_comments(adapter)) is None

    atlas = candidate(audit, "M0276-C04-ATLAS-WRAPPER")
    assert atlas["revision"] == ATLAS_REVISION and atlas["file_sha256"] == ATLAS_SOURCE_SHA256
    assert atlas["terminal_proof_body_id"] == "M0276-C01-MATHLIB-DIRECT"
    assert atlas["mathlib_revision"] == MATHLIB_REVISION
    assert atlas["machine_probe"]["exit"] == 0 and atlas["machine_probe"]["sorry_free"] is True
    assert atlas["candidate_classification"] == "M3_external_duplicate_wrapper"

    optlib = candidate(audit, "M0276-C05-OPTLIB-CONSUMER")
    assert optlib["revision"] == OPTLIB_REVISION
    assert optlib["file_sha256"] == OPTLIB_SOURCE_SHA256
    assert optlib["lake_manifest_sha256"] == "9f0b1865306f7c59320334bbabc8c9ca98a555696616e8d0c2d66c54fc9515f7"
    assert optlib["mathlib_revision"] == "d7317655e2826dc1f1de9a0c138db2775c4bb841"
    assert optlib["candidate_classification"] == "M5_statement_mismatch_consumer"

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("7/7 classified candidates")
    assert result["exact_candidate_located"] is result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M1"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["root_evidence_level"] == "E2"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is result["theorem_complete"] is False
    before = {"H": "H2", "M": "M3", "R": "R4"}
    assert audit["root_vector_before"] == audit["accepted_root_vector_after"] == before
    assert receipt["root_vector_before"] == receipt["accepted_root_vector_after"] == before
    assert audit["root_candidate_vector_after"] == receipt["root_candidate_vector_after"] == {
        "H": "H2", "M": "M1", "R": "R4"
    }
    assert audit["audit_complete"] is receipt["audit_complete"] is False
    assert audit["theorem_complete"] is receipt["theorem_complete"] is False
    assert audit["gate_state"] == "worker_self_tested_pending_master_acceptance"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256

    lean_environment = os.environ.copy()
    lean_environment.update({"LC_ALL": "C", "TZ": "UTC"})
    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0276/AnchorAudit.lean"],
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
    if lean.stdout.count("Declarations are sorry-free!") != 4:
        sys.stdout.write(lean.stdout)
        raise SystemExit("expected four machine-produced sorry-free reports")
    normalized = re.sub(r"\s+", " ", lean.stdout)
    axiom_reports = re.findall(r"depends on axioms: \[([^]]*)\]", normalized)
    if axiom_reports != ["propext, Classical.choice, Quot.sound"] * 4:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected terminal/helper/adapter axiom report")
    for marker in (
        "protected theorem ContinuousLinearMap.isOpenMap",
        "ANCHOR_CLOSURE declarations=17187 modules=654",
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
    expanded = re.search(
        r"def Stage1Instances\.THM_M_0276_AnchorAudit\.ExpandedExactTarget\.\{u, v\} : Prop :=\n"
        r"(?P<expression>.*)\Z",
        lean.stdout,
        re.DOTALL,
    )
    if expanded is None:
        sys.stdout.write(lean.stdout)
        raise SystemExit("could not extract the audit target's explicit expanded expression")
    if sha256_bytes(expanded.group("expression").strip().encode()) != EXPRESSION_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("audit target does not match the frozen expression fingerprint")
    if sha256_bytes(lean.stdout.encode()) != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0276; 7 candidates classified; exact pinned mathlib candidate M1/E2; "
        "accepted root remains H2/M3/R4; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
