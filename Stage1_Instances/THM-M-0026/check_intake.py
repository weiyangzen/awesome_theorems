#!/usr/bin/env python3
"""Fail-closed structural checker for the THM-M-0026 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0026"
ITEM_ID = "S56-M-0026-INTAKE"
BASE_REVISION = "d750776142c633e42858cebfc67c5c2664d419d7"
BASE_TREE = "7e62c62f1939b5cb668e56590b709f71f6e676b5"
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
}
TASKS = [
    f"S56-M-0026-{phase}"
    for phase in ("STATEMENT", "ANCHOR_AUDIT", "OBLIGATION_TREE", "PROOF", "VALIDATION", "RELEASE")
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load_json(path)
    assert packet["item_id"] == ITEM_ID
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] and packet["output_summary"]
    required_commands = {
        "python3 Docs/tools/check_stage1_standard.py",
        "python3 scripts/stage1_target.py check",
        "python3 scripts/stage1_target.py show THM-M-0026",
        "cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0026/IntakeProbe.lean",
        "python3 -B Stage1_Instances/THM-M-0026/check_intake.py --worker-packet .stage1-worker-selftest.json",
        "git diff --check -- Stage1_Instances/THM-M-0026 .stage1-worker-selftest.json",
    }
    assert required_commands <= set(packet["commands"])
    assert packet["known_failures"] == receipt["known_failures"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")

    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    targets = manifest["targets"] if isinstance(manifest, dict) else manifest
    target = next(row for row in targets if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1071
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    assert target["legacy_artifacts_accepted"] is False

    execution = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    nodes = execution["nodes"] if "nodes" in execution else execution["items"]
    authoritative = next(node for node in nodes if node["id"] == ITEM_ID)
    assert authoritative["theorem_id"] == THEOREM_ID
    assert authoritative["phase"] == "intake" and authoritative["depends_on"] == []
    assert authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert authoritative["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    assert formal["module"] is formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_hash"] is formal["environment_fingerprint"] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == instance["hypotheses"] == []
    assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    tasks = dag["tasks"]
    assert [task["id"] for task in tasks] == TASKS
    assert all(task["state"] == "open" for task in tasks)
    assert tasks[0]["depends_on"] == [ITEM_ID]
    assert all(tasks[i]["depends_on"] == [tasks[i - 1]["id"]] for i in range(1, len(tasks)))
    assert [task["layer"] for task in tasks] == list(range(1, 7))
    assert [task["phase"] for task in tasks] == [
        "statement", "anchor_audit", "obligation_tree", "proof", "validation", "release"
    ]
    for task in tasks:
        assert task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] and task["required_evidence"]
        assert task["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"
    assert dag["accepted_states"] == [] and dag["theorem_complete"] is False
    assert dag["audit_complete"] is False
    assert all(task["evidence_ids"] == [] for task in tasks)

    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["debt_vector_proposed"] == instance["root_vector"]
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == []
    assert receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["content_addressed_recipe_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert receipt["remaining_root_cut_set"] == TASKS
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["known_failures"] and receipt["selftest_result"] == "pass"

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_files == set(instance["owned_artifacts"]) == OWNED_FILES
    expected_paths = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_paths
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }

    for relative, tagged in receipt["source_inputs"].items():
        assert tagged == f"sha256:{sha256(ROOT / relative)}", f"stale source input: {relative}"
    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION and revisions["repository_base_tree"] == BASE_TREE
    assert receipt["worker_input_hashes"]["mathlib_revision"] == revisions["mathlib"]
    assert receipt["worker_input_hashes"]["mathlib_tree"] == revisions["mathlib_tree"]
    assert receipt["worker_input_hashes"]["mathlib_nullstellensatz_sha256"] == revisions["mathlib_nullstellensatz_sha256"]
    assert receipt["worker_input_hashes"]["lean_toolchain"] == f"sha256:{revisions['lean_toolchain_file_sha256']}"
    assert receipt["worker_input_hashes"]["lake_manifest"] == f"sha256:{revisions['lake_manifest_sha256']}"

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**希尔伯特零点定理**" in catalog
    assert "- 陈述: 代数闭域上多项式环的极大理想与代数集点的对应" in catalog
    module = ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/RingTheory/Nullstellensatz.lean"
    assert sha256(module) == revisions["mathlib_nullstellensatz_sha256"]
    module_text = module.read_text(encoding="utf-8")
    for declaration in (
        "eq_vanishingIdeal_singleton_of_isMaximal",
        "isMaximal_iff_eq_vanishingIdeal_singleton",
        "vanishingIdeal_zeroLocus_eq_radical",
    ):
        assert declaration in module_text

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in ("README.md", "instance.json", "intake-receipt.json", "scope-map.md", "source-statement-crosswalk.md", "task-dag.json", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("dossier invariant check: ok (THM-M-0026 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
