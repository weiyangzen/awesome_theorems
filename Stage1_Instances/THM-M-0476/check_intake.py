#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0476 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0476"
ITEM_ID = "S56-M-0476-INTAKE"
RANK = 1357
BASE_REVISION = "67d32ab26aba14b674ae8a1b919e6935812190c3"
BASE_TREE = "8a1d264cf3331992fbbc3a4fffca285af0b88929"
STATEMENT_BASE_REVISION = "be8701e88e791545c16a262edd1909486d5cef4b"
STATEMENT_BASE_TREE = "78b0a751473bf6d71f453a6aad18b130268a3428"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
OWNED_FILES = {
    "README.md",
    "instance.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "task-dag.json",
    "IntakeProbe.lean",
    "check_intake.py",
    "validation.md",
    "intake-receipt.json",
    "Statement.lean",
    "check_statement.py",
    "statement.json",
    "statement-receipt.json",
    "statement-validation.md",
    "AnchorAudit.lean",
    "anchor-audit-receipt.json",
    "anchor-audit-validation.md",
    "anchor-audit.json",
    "anchor-discovery-protocol.json",
    "check_anchor_audit.py",
    "ObligationTree.lean",
    "build_obligation_artifacts.py",
    "check_obligation_tree.py",
    "obligation-registry.json",
    "typed-graphs.json",
    "validation-specs.json",
    "obligation-tree.md",
    "obligation-tree-validation.md",
    "obligation-tree-receipt.json",
    "lean-elaboration-evidence.json",
    "Proof.lean",
    "check_proof.py",
    "check_proof.sh",
    "proof-receipt.json",
    "proof-validation.md",
}
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
SOURCE_HASH_FIELDS = {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
    "mathlib_wilson_sha256":
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/Wilson.lean",
}
HISTORICAL_WORKFLOW_HASHES = {
    "authoritative_blueprint_sha256":
        "201ff7722835a8360e3400c6f173b1e6684462b46ce5ed02e6b37ba51baf81bb",
    "execution_dag_sha256":
        "0e2192895bfd08136cf7d965e1c9d942ff0d040568b72552bc7869c5801b41fb",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["verdict"] == "no_state_change"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["content_addressed_recipe_ids"] == []
    assert packet["content_addressed_receipt_ids"] == []
    assert packet["proof_body_locations"] == []
    assert packet["canonical_obligation_ids"] == []
    assert packet["statement_fingerprints"] == []
    assert packet["typed_graph_changes"] == []
    assert packet["composition_certificates"] == []
    assert packet["audit_complete"] is packet["theorem_complete"] is False
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "威尔逊定理"
    assert target["category"] == instance["category"] == "数论 / 初等数论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[_]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] and instance["canonical_claim"]
    formal = instance["canonical_formal_target"]
    assert formal["module"] == f"Stage1_Instances/{THEOREM_ID}/Statement.lean"
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0476.WilsonTheoremTarget"
    )
    assert formal["elaborated_expression_hash"] == (
        "sha256:ee76edb160426d3e8d95b11bfedca7febcfe915f50007e042875c922ebc8a4ac"
    )
    assert formal["environment_fingerprint"]
    assert formal["declaration_candidates"] == [
        "ZMod.wilsons_lemma",
        "ZMod.prod_Ico_one_prime",
        "Nat.prime_iff_fac_equiv_neg_one",
    ]
    assert instance["quantifiers"] == ["p : Nat"]
    assert instance["ordered_binders"] == ["p : Nat", "hp : p.Prime"]
    assert instance["hypotheses"] == ["hp : p.Prime"]
    assert instance["alternate_encodings"] == [{
        "target": "forall (p : Nat) [Fact p.Prime], ((p - 1)! : ZMod p) = -1",
        "relationship": "iff",
        "checked_witness": "Stage1Instances.THM_M_0476.wilsonTheoremTarget_iff_factTarget",
    }]
    assert instance["excluded_degenerate_cases"]
    assert instance["obligation_registry_hash"] == (
        "sha256:032993303cc2c963a4b3256c95a03989cf24cd0462baed03cbfe16055c58fbbf"
    )
    assert instance["discovery_protocol_hash"] == (
        "sha256:2069bfed989cf0d0f8198d6e0a30a99dd84f0ea3442e5765040ea98f5cdac042"
    )
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == STATEMENT_BASE_REVISION
    assert revisions["repository_base_tree"] == STATEMENT_BASE_TREE
    assert revisions["intake_evidence_base"] == BASE_REVISION
    assert revisions["intake_evidence_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    source_commit = revisions["repository_source_record_commit"]
    assert git("rev-parse", f"{source_commit}:Docs/researches/math_theorems.md") == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        current_hash = sha256(ROOT / relative)
        if field in {"authoritative_blueprint_sha256", "execution_dag_sha256"}:
            assert revisions[field] == HISTORICAL_WORKFLOW_HASHES[field]
            assert revisions[field] != current_hash
        else:
            assert revisions[field] == current_hash, f"stale source hash: {field}"
    catalog_lines = "".join(
        (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8").splitlines(keepends=True)[3496:3502]
    )
    stage0_lines = "".join(
        (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8").splitlines(keepends=True)[13054:13080]
    )
    assert hashlib.sha256(catalog_lines.encode()).hexdigest() == revisions["repository_record_excerpt_sha256"]
    assert hashlib.sha256(stage0_lines.encode()).hexdigest() == revisions["stage0_excerpt_sha256"]
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("rev-parse", "HEAD:Mathlib/NumberTheory/Wilson.lean", cwd=mathlib) == revisions["mathlib_wilson_blob"]
    assert not git("status", "--short", cwd=mathlib), "pinned mathlib source is dirty"

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0476-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["authoritative_state"] in {"[ ]", "[_]"}
        assert task["authoritative_state"] == authoritative["state"] or (
            task["authoritative_state"] == "[ ]" and authoritative["state"] == "[_]"
        )
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**威尔逊定理**") == 1
    assert "- 提出者: John Wilson" in catalog
    assert "- 时间: 1770" in catalog
    assert "- 陈述: (p-1)! ≡ -1 (mod p)" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0476 威尔逊定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0474", "THM-M-0475", "THM-M-0477", "THM-M-0899"
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    intake_owned_files = OWNED_FILES - {
        "Statement.lean",
        "check_statement.py",
        "statement.json",
        "statement-receipt.json",
        "statement-validation.md",
        "AnchorAudit.lean",
        "anchor-audit-receipt.json",
        "anchor-audit-validation.md",
        "anchor-audit.json",
        "anchor-discovery-protocol.json",
        "check_anchor_audit.py",
        "ObligationTree.lean",
        "build_obligation_artifacts.py",
        "check_obligation_tree.py",
        "obligation-registry.json",
        "typed-graphs.json",
        "validation-specs.json",
        "obligation-tree.md",
        "obligation-tree-validation.md",
        "obligation-tree-receipt.json",
        "lean-elaboration-evidence.json",
        "Proof.lean",
        "check_proof.py",
        "check_proof.sh",
        "proof-receipt.json",
        "proof-validation.md",
    }
    assert set(receipt["changed_paths"]) == {
        ".stage1-worker-selftest.json",
        *{f"Stage1_Instances/{THEOREM_ID}/{name}" for name in intake_owned_files},
    }
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["phase"] == "intake" and receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["change_impact_set"] == [ITEM_ID]
    assert receipt["content_addressed_recipe_ids"] == []
    assert receipt["content_addressed_receipt_ids"] == []
    assert receipt["structured_validation_recipes"]
    superseded_intake_projection_hashes = {
        f"Stage1_Instances/{THEOREM_ID}/{name}"
        for name in {
            "README.md", "check_intake.py", "instance.json", "scope-map.md",
            "source-statement-crosswalk.md", "task-dag.json", "validation.md",
        }
    }
    for relative, expected in receipt["owned_artifact_sha256"].items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        elif relative in superseded_intake_projection_hashes:
            continue
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    lean_result = subprocess.run(
        ["lake", "env", "lean", f"../../Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    assert lean_result.returncode == 0, lean_result.stdout
    assert hashlib.sha256(lean_result.stdout.encode()).hexdigest() == receipt["lean_probe_stdout_sha256"]

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )
    for name in ("README.md", "instance.json", "intake-receipt.json", "scope-map.md",
                 "source-statement-crosswalk.md", "task-dag.json", "validation.md",
                 "statement.json", "statement-receipt.json", "statement-validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet:
        check_worker_packet(args.worker_packet, receipt)
    print("intake invariant check: ok (THM-M-0476 planned; expanded statement dossier; H1/M3/R4)")


if __name__ == "__main__":
    main()
