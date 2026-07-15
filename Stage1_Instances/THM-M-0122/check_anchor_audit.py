#!/usr/bin/env python3
"""Fail closed over the THM-M-0122 bounded immutable anchor inventory."""

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
ITEM_ID = "S56-M-0122-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0122"
BASE_REVISION = "6bf9ee93a322e7d25cf9249226222095f95d1cff"
BASE_TREE = "24acf86e69ab2e6fca9480c6269b6429874ba295"
GRAPH_SHA256 = "73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
EXPRESSION_SHA256 = "f3e5f585b30ab9543bc47551d0d91c695523bace26fdb5484869add319ef7dac"
STATEMENT_SHA256 = "824c2d9410bbf3117fa6340e4259f9a3a7df6ff892c4b7cc6dad94a03ab437e8"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ATLAS_REVISION = "34ffed396f376454c1a9b297f3fd74c5c801fb50"
ATLAS_SOURCE_SHA256 = "b5aca9ae03c178c908fdf0e28d4dd8672643b16390b25e9b9771882726ed8f01"
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
        raise SystemExit(f"anchor audit check failed: {message}")


def main() -> None:
    audit = load(INSTANCE / "anchor-audit.json")
    protocol = load(INSTANCE / "anchor-discovery-protocol.json")
    snapshot = load(INSTANCE / "external-anchor-snapshot.json")
    ledger = load(INSTANCE / "dependency-reuse-ledger.json")
    statement = load(INSTANCE / "statement.json")
    statement_receipt = load(INSTANCE / "statement-receipt.json")
    manifest = load(LEAN_DIR / "lake-manifest.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    theorem_dag_path = ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json"
    theorem_dag = load(theorem_dag_path)

    require(audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID,
            "audit identity changed")
    require(protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID,
            "protocol identity changed")
    require(snapshot["item_id"] == ITEM_ID and snapshot["theorem_id"] == THEOREM_ID,
            "snapshot identity changed")
    require(audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE,
            "audit base changed")
    require(git("rev-parse", "HEAD") == BASE_REVISION, "worker base revision changed")
    require(git("rev-parse", "HEAD^{tree}") == BASE_TREE, "worker base tree changed")

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    require(item["theorem_id"] == THEOREM_ID and item["phase"] == "anchor_audit",
            "authoritative task identity changed")
    require(item["layer"] == 2 and item["state"] == "[ ]" and
            item["depends_on"] == ["S56-M-0122-STATEMENT"],
            "authoritative task state or dependency changed")
    require(item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"],
            "authoritative ownership changed")

    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    require(sha256(theorem_dag_path) == GRAPH_SHA256, "theorem DAG digest changed")
    require(node["dependency_context_sha256"] == CONTEXT_SHA256,
            "target dependency context changed")
    require(node["direct_hard_parents"] == [] and
            node["transitive_hard_ancestors"] == [] and
            node["direct_reuse_hint_ids"] == [] and
            node["shared_lemma_group_ids"] == [], "authoritative empty closure changed")
    expected_empty = (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "inspections", "reuse_decisions",
        "unresolved_compatibility_obligations",
    )
    require(ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1" and
            ledger["consumer_theorem_id"] == THEOREM_ID, "ledger identity changed")
    require(ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256 and
            ledger["dependency_context_sha256"] == CONTEXT_SHA256 and
            ledger["repository_revision"] == BASE_REVISION, "ledger binding changed")
    require(all(ledger[field] == [] for field in expected_empty),
            "empty v2 context is not recorded exactly")

    formal = statement["canonical_formal_target"]
    require(formal["declaration_or_expression"] ==
            "Stage1Instances.THMM0122.FaltingsTarget", "canonical declaration changed")
    require(formal["elaborated_expression_sha256"] == EXPRESSION_SHA256,
            "canonical expression changed")
    require(formal["statement_file_sha256"] == STATEMENT_SHA256 and
            sha256(INSTANCE / "Statement.lean") == STATEMENT_SHA256,
            "canonical statement source changed")
    require(statement_receipt["statement_fingerprints"] ==
            [f"sha256:{EXPRESSION_SHA256}"], "statement receipt fingerprint changed")

    mathlib_package = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    require(mathlib_package["rev"] == MATHLIB_REVISION, "manifest mathlib pin changed")
    mathlib = (PACKAGES / "mathlib").resolve()
    require(git("-C", str(mathlib), "rev-parse", "HEAD") == MATHLIB_REVISION,
            "materialized mathlib revision changed")
    require(git("-C", str(mathlib), "rev-parse", "HEAD^{tree}") == MATHLIB_TREE,
            "materialized mathlib tree changed")
    require(git("-C", str(mathlib), "status", "--short", "--untracked-files=no") == "",
            "materialized mathlib tracked worktree is dirty")
    require(audit["immutable_environment"]["lake_manifest_sha256"] ==
            sha256(LEAN_DIR / "lake-manifest.json"), "Lake manifest digest changed")
    require(audit["immutable_environment"]["mathlib_license_sha256"] ==
            sha256(mathlib / "LICENSE"), "mathlib license digest changed")

    geometry = next(row for row in audit["candidates"]
                    if row["candidate_id"] == "M0122-C04-MATHLIB-GEOMETRY-SUBSTRATE")
    arithmetic = next(row for row in audit["candidates"]
                      if row["candidate_id"] == "M0122-C05-MATHLIB-ARITHMETIC-SUBSTRATE")
    for relative, expected in {**geometry["source_sha256"],
                               **arithmetic["source_sha256"]}.items():
        require(sha256(mathlib / relative) == expected,
                f"pinned mathlib source changed: {relative}")
    docs = next(row for row in audit["candidates"]
                if row["candidate_id"] == "M0122-C06-MATHLIB-DOCUMENTATION-ROW")
    require(sha256(mathlib / "docs/1000.yaml") == docs["source_sha256"],
            "mathlib documentation snapshot changed")
    doc_text = (mathlib / "docs/1000.yaml").read_text(encoding="utf-8")
    row = doc_text[doc_text.index("Q240950:"):doc_text.index("Q241868:")]
    require("title: Faltings's theorem" in row and "decl:" not in row and
            "decls:" not in row, "Faltings documentation row gained a declaration")

    package_search = subprocess.run(
        ["rg", "-n", "-i",
         "Faltings|MordellConjecture|Mordell conjecture|FaltingsTheorem|faltings_theorem",
         str(PACKAGES), "-g", "*.lean", "-g", "*.md", "-g", "*.yaml", "-g", "*.json"],
        text=True, capture_output=True,
    )
    require(package_search.returncode == 0 and
            package_search.stdout.strip().endswith(
                "mathlib/docs/1000.yaml:249:  title: Faltings's theorem"),
            "pinned package closure gained or lost a Faltings/Mordell source match")

    candidate_ids = [row["candidate_id"] for row in audit["candidates"]]
    require(candidate_ids == protocol["inventory_member_ids"],
            "protocol/audit inventory order or membership changed")
    require(len(candidate_ids) == len(set(candidate_ids)) == 8,
            "candidate inventory is not an eight-row bijection")
    require(all(row["exact_root_closed"] is False for row in audit["candidates"]),
            "a candidate unexpectedly claims root closure")
    require(all(not row["classification"].startswith(("M0", "M1"))
                for row in audit["candidates"]),
            "inventory unexpectedly credits a kernel-closed candidate")
    require(sha256(ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_041.lean") ==
            "d1faf74ef45845b9aa741df83a8e2390ec21217b8063c7a87be6e72f1fca30d5",
            "legacy discovery source changed")
    require(sha256(ROOT / "Stage1_Instances/THM-M-0395/Statement.lean") ==
            "de1bfb399ccec48a224e867c55f6eab12589e458949d6d409260be65f0920ba6",
            "same-claim statement source changed")
    require(sha256(ROOT / "Stage1_Instances/THM-M-0395/Proof.lean") ==
            "1c0139a56ce605ecf2ff09231f91a78ca777a0733711a480adc429400517d643",
            "same-claim partial proof source changed")

    atlas = snapshot["atlas_faltings"]
    atlas_candidate = next(row for row in audit["candidates"]
                           if row["candidate_id"] == "M0122-C07-ATLAS-FALTINGS-PLACEHOLDER")
    require(atlas["revision"] == atlas_candidate["revision"] == ATLAS_REVISION,
            "Atlas revision changed")
    require(atlas["source_sha256"] == atlas_candidate["file_sha256"] ==
            ATLAS_SOURCE_SHA256, "Atlas source digest changed")
    require(atlas["toolchain"] == "leanprover/lean4:v4.29.0" and
            atlas["mathlib_revision"] == MATHLIB_REVISION,
            "Atlas environment observation changed")
    require("by sorry" in atlas["terminal_body_excerpt"] and
            atlas_candidate["classification"] ==
            "M5_direct_placeholder_and_material_statement_mismatch",
            "Atlas direct placeholder boundary changed")
    require(atlas["license_sha256"] == atlas_candidate["license_sha256"],
            "Atlas license binding changed")
    sourcegraph = snapshot["sourcegraph_observations"]
    require(len(sourcegraph) == 4 and all(row["done"] is True for row in sourcegraph),
            "bounded Sourcegraph observations changed")
    require(sourcegraph[0]["repositories_count"] == 1 and
            {row["repository"] for row in sourcegraph[0]["matches"]} ==
            {"github.com/facebookresearch/atlas-lean"},
            "bounded Faltings search no longer records Atlas only")

    probe = (INSTANCE / "AnchorAudit.lean").read_text(encoding="utf-8")
    require(FORBIDDEN_PROBE.search(probe) is None,
            "prohibited Lean construct in target-owned anchor probe")
    expected_checks = {
        "NumberField", "Scheme", "SmoothOfRelativeDimension", "geometrically", "IsClosedImmersion",
        "Proj.toSpecZero", "CategoryTheory.Sheaf.H", "Northcott.finite_le",
        "AddCommGroup.fg_of_descent'",
    }
    checked = set(re.findall(r"^#check (.+)$", probe, re.MULTILINE))
    require(expected_checks <= checked, f"missing Lean probes: {sorted(expected_checks - checked)}")
    require("#print axioms checked_northcott_sublevel" in probe,
            "missing target-owned support axiom probe")

    coverage = audit["classification_coverage"]
    require(coverage == {
        "classified": 8,
        "inventory_size": 8,
        "complete_for_inventory_version": True,
        "discovery_saturation_claimed": False,
        "external_exact_proof_candidate_found": False,
    }, "classification boundary changed")
    decision = audit["root_decision"]
    require(decision["classification_before"] == decision["classification_after_proposed"] ==
            "M3" and decision["kernel_closed"] is False and
            decision["repo_local_integration_debt"] is False,
            "root decision overclaims closure or integration debt")
    require(audit["root_vector_before"] == audit["root_vector_after_proposed"] ==
            {"human": "H4", "machine": "M3", "readability": "R3"},
            "root vector changed without evidence")
    require(audit["inventory_complete"] is True and audit["theorem_proved"] is False and
            audit["audit_complete"] is False and audit["theorem_complete"] is False and
            audit["accepted_receipt_ids"] == [], "audit overclaims terminal state")

    receipt_path = INSTANCE / "anchor-audit-receipt.json"
    if receipt_path.exists():
        receipt = load(receipt_path)
        require(receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID and
                receipt["proposed_state"] == "[_]" and receipt["accepted"] is False,
                "provisional receipt identity or authority changed")
        require(receipt["audit_complete"] is False and
                receipt["theorem_complete"] is False,
                "provisional receipt overclaims completion")
        for filename, expected in receipt["output_hashes"].items():
            if not filename.endswith((".lean", ".json", ".py")):
                continue
            output = INSTANCE / filename
            if output == receipt_path:
                continue
            require(sha256(output) == expected,
                    f"receipt output hash is stale: {filename}")

    payload = {
        "atlas_direct_placeholder": True,
        "candidate_rows_classified": len(candidate_ids),
        "canonical_expression_sha256": EXPRESSION_SHA256,
        "dependency_context_sha256": CONTEXT_SHA256,
        "mathlib_revision": MATHLIB_REVISION,
        "root_machine_classification": "M3",
        "theorem_complete": False,
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
