#!/usr/bin/env python3
"""Fail closed over the THM-M-0115 bounded immutable anchor inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
INSTANCE = Path(__file__).resolve().parent
LEAN_DIR = ROOT / "Formalizations" / "Lean"
PACKAGES = LEAN_DIR / ".lake" / "packages"
AUDIT_PATH = INSTANCE / "anchor-audit.json"
PROTOCOL_PATH = INSTANCE / "anchor-discovery-protocol.json"
PROBE_PATH = INSTANCE / "AnchorAudit.lean"
RECEIPT_PATH = INSTANCE / "anchor-audit-receipt.json"
EXTERNAL_SNAPSHOT_PATH = INSTANCE / "external-anchor-snapshot.json"
ITEM_ID = "S56-M-0115-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0115"
BASE_REVISION = "c4715a2babbead02e04d70708c3ebc58c75a1942"
BASE_TREE = "28cd40da86c57dea61aed02b4965f80699894bd3"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "eada246ab2968c378c5b6c31c2ffd84c10873d9206b499457c451ae3848c160e"
STATEMENT_SHA256 = "26648a8514a0a9240c831132918c9ad0f735eb7accce33f2287a45961394d538"
ATLAS_REVISION = "34ffed396f376454c1a9b297f3fd74c5c801fb50"
ATLAS_SOURCE_SHA256 = "2ade6a4b32dd2b2960bf6a9993921308591b9fe95aec61407f9f89bea554f450"
FORBIDDEN_PROBE = re.compile(
    r"(^|[^A-Za-z_])(sorry|admit|sorryAx|axiom|constant|opaque|unsafe|"
    r"implemented_by|native_decide)([^A-Za-z_]|$)"
)


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.STDOUT
    ).strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    audit = load(AUDIT_PATH)
    protocol = load(PROTOCOL_PATH)
    external_snapshot = load(EXTERNAL_SNAPSHOT_PATH)
    statement = load(INSTANCE / "statement.json")
    statement_receipt = load(INSTANCE / "statement-receipt.json")
    manifest = load(LEAN_DIR / "lake-manifest.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    require(audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID,
            "audit identity changed")
    require(protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID,
            "protocol identity changed")
    require(audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE,
            "audit base changed")
    require(git("rev-parse", "HEAD") == BASE_REVISION, "worker base revision changed")
    require(git("rev-parse", "HEAD^{tree}") == BASE_TREE, "worker base tree changed")

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    require(item["theorem_id"] == THEOREM_ID and item["phase"] == "anchor_audit",
            "authoritative DAG identity changed")
    require(item["layer"] == 2 and item["depends_on"] == ["S56-M-0115-STATEMENT"],
            "authoritative DAG dependency changed")
    require(item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"],
            "authoritative ownership changed")

    formal = statement["canonical_formal_target"]
    require(formal["declaration_or_expression"] ==
            "Stage1Instances.THMM0115.GrothendieckRiemannRochExpandedTarget",
            "canonical declaration changed")
    require(formal["elaborated_expression_sha256"] == EXPRESSION_SHA256,
            "canonical expression changed")
    require(formal["statement_file_sha256"] == STATEMENT_SHA256,
            "statement record source hash changed")
    require(sha256(INSTANCE / "Statement.lean") == STATEMENT_SHA256,
            "statement source changed")
    require(statement_receipt["statement_fingerprints"] ==
            [f"sha256:{EXPRESSION_SHA256}"], "statement receipt changed")

    mathlib_package = next(p for p in manifest["packages"] if p["name"] == "mathlib")
    require(mathlib_package["rev"] == MATHLIB_REVISION, "manifest mathlib pin changed")
    mathlib = (PACKAGES / "mathlib").resolve()
    require(git("-C", str(mathlib), "rev-parse", "HEAD") == MATHLIB_REVISION,
            "materialized mathlib HEAD changed")
    require(git("-C", str(mathlib), "rev-parse", "HEAD^{tree}") == MATHLIB_TREE,
            "materialized mathlib tree changed")
    require(git("-C", str(mathlib), "status", "--short", "--untracked-files=no") == "",
            "materialized mathlib tracked worktree is dirty")

    env = audit["immutable_environment"]
    require(env["mathlib_revision"] == MATHLIB_REVISION and
            env["mathlib_tree"] == MATHLIB_TREE, "audit mathlib pin changed")
    require(env["manifest_sha256"] == sha256(LEAN_DIR / "lake-manifest.json"),
            "manifest digest changed")
    require(env["mathlib_license_sha256"] == sha256(mathlib / "LICENSE"),
            "mathlib license digest changed")

    expected_blobs = {
        "Mathlib/AlgebraicGeometry/Scheme.lean": "7651e2471b43dc23566ee935fb154c962825e8c6",
        "Mathlib/AlgebraicGeometry/Over.lean": "f50323f4db34de85e495a00635b08159c2efce6c",
        "Mathlib/AlgebraicGeometry/Morphisms/Proper.lean": "5eb5c0e0c9b90cd948b02b820e9c7351629187b2",
        "Mathlib/AlgebraicGeometry/Morphisms/Smooth.lean": "7b0d9e9958838fda8439b972b5bbd11ecbdde160",
        "Mathlib/AlgebraicGeometry/QuasiAffine.lean": "285a35af48be7901de378e9783aed7190bb8007d",
        "Mathlib/AlgebraicGeometry/Modules/Sheaf.lean": "8361d3a6527fc20115db196f8535168105e3af61",
        "Mathlib/AlgebraicGeometry/Modules/Tilde.lean": "58acd4d6baa4bfe97cf8b8f7b98fe6a71a65beb6",
        "Mathlib/CategoryTheory/Sites/SheafCohomology/Basic.lean": "fd348ffcea30facc9341994693411e8165a3d36f",
        "Mathlib/Algebra/Homology/DerivedCategory/HomologySequence.lean": "153b2dca2e2317b4a123b02d61187fae0fb41a1d",
        "Mathlib/GroupTheory/MonoidLocalization/GrothendieckGroup.lean": "80dafe76c8b08b70a3ac7be381306afc4c5468fc",
    }
    for path, expected in expected_blobs.items():
        actual = git("-C", str(mathlib), "rev-parse", f"HEAD:{path}")
        require(actual == expected, f"mathlib source blob changed: {path}")

    candidate_ids = [row["candidate_id"] for row in audit["candidates"]]
    require(candidate_ids == protocol["inventory_member_ids"],
            "protocol/audit inventory order or membership changed")
    require(len(candidate_ids) == len(set(candidate_ids)) == 9,
            "candidate inventory is not a nine-row bijection")
    classifications = {row["candidate_id"]: row["classification"]
                       for row in audit["candidates"]}
    require(classifications["M0115-C01-REPO-CANONICAL-STATEMENT"] ==
            "M3_exact_statement_only", "canonical candidate misclassified")
    require(classifications["M0115-C06-ATLAS-GRR-PLACEHOLDER"] ==
            "M5_direct_placeholder_and_statement_mismatch",
            "Atlas placeholder candidate misclassified")
    require(all("M0" not in value and "M1" not in value
                for value in classifications.values()),
            "inventory unexpectedly claims an integrable or closed candidate")

    legacy = ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_023.lean"
    require(git("rev-parse", "HEAD:Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_023.lean") ==
            "9247109bfe38c3e5053d6c6c82d1649f082c555e", "legacy blob changed")
    require(sha256(legacy) ==
            "f9d66d89d0c2cfd180ea177a41d7c4815104446ce33c81c80ef453517d0ec0d8",
            "legacy source digest changed")

    probe = PROBE_PATH.read_text(encoding="utf-8")
    require(FORBIDDEN_PROBE.search(probe) is None,
            "prohibited Lean construct in target-owned anchor probe")
    checked_names = set(re.findall(r"^#check (.+)$", probe, re.MULTILINE))
    expected_checks = {
        "Scheme", "Scheme.Spec", "Scheme.Over", "Scheme.Hom.IsOver",
        "Scheme.Hom.isOver_iff", "@IsProper", "@Smooth", "Scheme.IsQuasiAffine",
        "Scheme.Modules", "Scheme.Modules.pushforward", "Scheme.Modules.pullback",
        "Scheme.Modules.pullbackPushforwardAdjunction", "SheafOfModules.IsQuasicoherent",
        "tilde", "CategoryTheory.Sheaf.H", "CategoryTheory.Sheaf.cohomologyFunctor",
        "DerivedCategory", "DerivedCategory.homologyFunctor", "Algebra.GrothendieckGroup",
    }
    require(expected_checks <= checked_names,
            f"missing probe names: {sorted(expected_checks - checked_names)}")
    require("#check Algebra.GrothendieckGroup" in probe,
            "missing generic group-completion probe")
    require("#print axioms tildeIsQuasicoherent" in probe,
            "missing support-wrapper axiom probe")

    atlas = next(row for row in audit["candidates"]
                 if row["candidate_id"] == "M0115-C06-ATLAS-GRR-PLACEHOLDER")
    require(atlas["revision"] == ATLAS_REVISION, "Atlas revision changed")
    snapshot_atlas = external_snapshot["atlas_grr"]
    require(snapshot_atlas["revision"] == ATLAS_REVISION and
            snapshot_atlas["source_sha256"] == ATLAS_SOURCE_SHA256,
            "Atlas content-addressed observation changed")
    require("by sorry" in snapshot_atlas["terminal_body_excerpt"],
            "Atlas direct proof-gap observation changed")
    require("grothendieck_riemann_roch" in
            snapshot_atlas["downstream_dependency_excerpt"],
            "Atlas downstream placeholder observation changed")
    require(snapshot_atlas["toolchain"] == "leanprover/lean4:v4.29.0" and
            snapshot_atlas["mathlib_revision"] == MATHLIB_REVISION,
            "Atlas recorded environment changed")
    require(snapshot_atlas["source_sha256"] == atlas["file_sha256"] and
            snapshot_atlas["license_sha256"] == atlas["license_sha256"],
            "Atlas audit/snapshot crosswalk changed")
    sourcegraph = external_snapshot["sourcegraph_observations"]
    require(len(sourcegraph) == 4 and all(row["done"] is True for row in sourcegraph),
            "bounded Sourcegraph snapshot changed")
    declaration_search = next(row for row in sourcegraph
                              if row["query"].startswith("GrothendieckRiemannRoch"))
    require(declaration_search["match_count"] == 2 and
            {row["revision"] for row in declaration_search["matches"]} ==
            {ATLAS_REVISION}, "Sourcegraph Atlas-only observation changed")

    decision = audit["root_decision"]
    require(decision["classification_before"] == "M3" and
            decision["classification_after_proposed"] == "M3",
            "root machine classification changed")
    require(decision["kernel_closed"] is False and
            decision["repo_local_integration_debt"] is False and
            decision["integration_tasks"] == [], "root decision overclaims closure or debt")
    require(audit["root_vector_before"] == audit["root_vector_after_proposed"] ==
            {"human": "H4", "machine": "M3", "readability": "R4"},
            "root vector changed without evidence")
    require(audit["theorem_proved"] is False and audit["audit_complete"] is False and
            audit["theorem_complete"] is False and audit["accepted_receipt_ids"] == [],
            "audit overclaims terminal state")

    if RECEIPT_PATH.exists():
        receipt = load(RECEIPT_PATH)
        require(receipt["item_id"] == ITEM_ID and receipt["accepted"] is False and
                receipt["proposed_state"] == "[_]", "provisional receipt changed")
        require(receipt["audit_complete"] is False and
                receipt["theorem_complete"] is False, "receipt overclaims completion")
        expected_changed = {
            ".stage1-worker-selftest.json",
            f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
            f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
            f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
            f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
            f"Stage1_Instances/{THEOREM_ID}/anchor-audit.md",
            f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
            f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
            f"Stage1_Instances/{THEOREM_ID}/external-anchor-snapshot.json",
        }
        require(set(receipt["changed_paths"]) == expected_changed,
                "receipt changed-path inventory changed")
        hashes = receipt["output_hashes"]
        for filename in (
            "AnchorAudit.lean", "anchor-discovery-protocol.json", "anchor-audit.json",
            "anchor-audit.md", "check_anchor_audit.py", "external-anchor-snapshot.json",
        ):
            require(hashes[filename] == sha256(INSTANCE / filename),
                    f"receipt output hash is stale: {filename}")

    payload = {
        "atlas_direct_placeholder": True,
        "candidate_rows_classified": len(candidate_ids),
        "canonical_expression_sha256": EXPRESSION_SHA256,
        "mathlib_revision": MATHLIB_REVISION,
        "probe_sha256": sha256(PROBE_PATH),
        "root_machine_classification": "M3",
        "theorem_complete": False,
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
