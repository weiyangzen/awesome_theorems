#!/usr/bin/env python3
"""Fail-closed structural checker for the THM-M-0029 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0029"
ITEM_ID = "S56-M-0029-INTAKE"
BASE_REVISION = "936bf2b9e968abd3b79b5b36d32f2f2bff648c7e"
BASE_TREE = "8c9d3261b0ba9a81deb5bfc19a335a02cb80f962"
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
    f"S56-M-0029-{phase}"
    for phase in ("STATEMENT", "ANCHOR_AUDIT", "OBLIGATION_TREE", "PROOF", "VALIDATION", "RELEASE")
]
SOURCE_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "001dd6c3c6ccc1b1910f0c51201f534f9e37c29df4f5d09a894f1cf30aa116eb",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "203319f482338106f0e568a85379df8a0434a560b7778b2a7137621df00af3d3",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/RingTheory/Finiteness/Nakayama.lean": "fb87e5542271068bf673438aee9fe14d2534fbaef4088298131908c9f4e12524",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/RingTheory/Nakayama.lean": "e4eca230b16af2c1513b64b13591d41b90718005ffcac8b0f3bfaa7f2f570328",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load_json(path)
    assert packet["item_id"] == ITEM_ID
    assert packet["theorem_id"] == THEOREM_ID
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] and packet["output_summary"]
    required_commands = {
        "python3 Docs/tools/check_stage1_standard.py",
        "python3 scripts/stage1_target.py check",
        "python3 scripts/stage1_target.py show THM-M-0029",
        "cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0029/IntakeProbe.lean",
        "python3 -B Stage1_Instances/THM-M-0029/check_intake.py --worker-packet .stage1-worker-selftest.json",
        "git diff --check -- Stage1_Instances/THM-M-0029 .stage1-worker-selftest.json",
    }
    assert required_commands <= set(packet["commands"])
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["audit_complete"] is packet["theorem_complete"] is False


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
    assert target["execution_rank"] == 1074
    assert target["name"] == "中山引理" and target["category"] == "代数学 / 环论"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    assert target["legacy_priority_slot"] is None and target["legacy_artifacts_accepted"] is False

    execution = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    nodes = execution["nodes"] if "nodes" in execution else execution["items"]
    authoritative = next(node for node in nodes if node["id"] == ITEM_ID)
    assert authoritative["theorem_id"] == THEOREM_ID
    assert authoritative["phase"] == "intake" and authoritative["depends_on"] == []
    assert authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert authoritative["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    assert formal["module"] is formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_hash"] is formal["environment_fingerprint"] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == instance["hypotheses"] == []
    assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["source_revisions"]["primary_candidate_pdf_sha256"] == (
        receipt["worker_input_hashes"]["primary_candidate_pdf_sha256"]
    )

    candidate_declarations = set(formal["candidate_declarations"])
    for name in (
        "Submodule.exists_sub_one_mem_and_smul_eq_zero_of_fg_of_le_smul",
        "Submodule.eq_bot_of_le_smul_of_le_jacobson_bot",
        "Submodule.smul_le_of_le_smul_of_le_jacobson_bot",
        "Submodule.exists_injOn_mkQ_image_span_eq_of_span_eq_map_mkQ_of_le_jacobson_bot",
    ):
        assert name in candidate_declarations

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
        assert task["evidence_ids"] == []
    assert dag["accepted_states"] == []
    assert dag["audit_complete"] is dag["theorem_complete"] is False

    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["debt_vector_proposed"] == instance["root_vector"]
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["content_addressed_recipe_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert receipt["remaining_root_cut_set"] == TASKS
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["known_failures"] and receipt["selftest_result"] == "pass"
    assert receipt["axiom_and_placeholder_result"]["command_exit_code"] == 1

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_files == set(instance["owned_artifacts"]) == OWNED_FILES
    expected_paths = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_paths
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }

    for relative, expected in SOURCE_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"stale source input: {relative}"
        assert receipt["source_inputs"][relative] == f"sha256:{expected}"
    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert revisions["repository_base_tree"] == BASE_TREE
    assert revisions["mathlib"] == receipt["worker_input_hashes"]["mathlib_revision"]
    assert revisions["mathlib_tree"] == receipt["worker_input_hashes"]["mathlib_tree"]
    assert revisions["mathlib_finiteness_nakayama_sha256"] == SOURCE_INPUTS[
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/RingTheory/Finiteness/Nakayama.lean"
    ]
    assert revisions["mathlib_nakayama_sha256"] == SOURCE_INPUTS[
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/RingTheory/Nakayama.lean"
    ]

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**中山引理**" in catalog and "- 陈述: 关于模的生成元的引理" in catalog
    mathlib_text = (
        ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/RingTheory/Nakayama.lean"
    ).read_text(encoding="utf-8")
    for declaration in (
        "eq_bot_of_le_smul_of_le_jacobson_bot",
        "smul_le_of_le_smul_of_le_jacobson_bot",
        "exists_injOn_mkQ_image_span_eq_of_span_eq_map_mkQ_of_le_jacobson_bot",
    ):
        assert declaration in mathlib_text

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in (
        "README.md", "instance.json", "intake-receipt.json", "scope-map.md",
        "source-statement-crosswalk.md", "task-dag.json", "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-0029 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
