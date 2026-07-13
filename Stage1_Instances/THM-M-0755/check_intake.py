#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0755"
BASE = "d05520867fab3367a9b61b9544c3e12241204f54"
BASE_TREE = "fb2cfc62077d5b53e9938632cd6361dd60872067"
MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


target_data = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
targets = target_data if isinstance(target_data, list) else target_data["targets"]
target = next(item for item in targets if item["theorem_id"] == "THM-M-0755")

execution_data = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
execution_items = execution_data if isinstance(execution_data, list) else execution_data["items"]
authoritative = [item for item in execution_items if item["theorem_id"] == "THM-M-0755"]

instance = load(OWNED / "instance.json")
dag = load(OWNED / "task-dag.json")
receipt = load(OWNED / "intake-receipt.json")

assert target == {
    "execution_rank": 1341,
    "legacy_priority_slot": None,
    "theorem_id": "THM-M-0755",
    "name": "解析层次",
    "category": "数理逻辑 / 递归论",
    "source_status_untrusted": "已验证",
    "baseline": "L0",
    "rework_required": True,
    "legacy_artifacts_accepted": False,
    "target_lane": "hard_statement_first_partial_verification",
    "intake_score": 86,
    "lifecycle_mode": "planned",
    "theorem_complete": False,
}
assert len(authoritative) == 7
assert authoritative[0]["id"] == "S56-M-0755-INTAKE"
assert authoritative[0]["depends_on"] == []
assert authoritative[0]["owned_paths"] == ["Stage1_Instances/THM-M-0755"]
assert authoritative[0]["deliverable"] == (
    "Create the theorem dossier, scope map, and source-statement crosswalk."
)

assert target["execution_rank"] == instance["execution_rank"] == 1341
assert target["baseline"] == instance["baseline"] == "L0"
assert target["rework_required"] is instance["rework_required"] is True
assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == "THM-M-0755"
assert instance["item_id"] == receipt["item_id"] == "S56-M-0755-INTAKE"
assert (
    instance["lifecycle_mode"]
    == instance["lifecycle"]
    == dag["lifecycle_mode"]
    == dag["lifecycle"]
    == "planned"
)
assert dag["theorem_complete"] is False
assert instance["intent"] == "intake"
assert instance["canonical_statement"] is None
assert instance["canonical_claim"] is None
assert instance["canonical_formal_target"]["module"] is None
assert instance["canonical_formal_target"]["declaration_or_expression"] is None
assert instance["canonical_formal_target"]["elaborated_expression_hash"] is None
assert instance["canonical_formal_target"]["environment_fingerprint"] is None
assert instance["quantifiers"] == instance["ordered_binders"] == []
assert instance["hypotheses"] == instance["alternate_encodings"] == []
assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
assert instance["audit_complete"] is False and instance["theorem_complete"] is False
assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
assert dag["accepted_states"] == []

expected_ids = [item["id"] for item in authoritative[1:]]
assert [task["id"] for task in dag["tasks"]] == expected_ids
for task, source in zip(dag["tasks"], authoritative[1:]):
    for key in (
        "id",
        "theorem_id",
        "execution_rank",
        "phase",
        "layer",
        "depends_on",
        "owned_paths",
        "deliverable",
        "completion_gate",
    ):
        assert task[key] == source[key], f"DAG mismatch for {task['id']} field {key}"
    assert task["state"] == "open"

owned_files = sorted(path.name for path in OWNED.iterdir() if path.is_file())
assert sorted(instance["owned_artifacts"]) == owned_files
hashed_files = [name for name in owned_files if name != "intake-receipt.json"]
assert sorted(receipt["untracked_owned_artifact_sha256"]) == sorted(hashed_files)
for name in hashed_files:
    assert receipt["untracked_owned_artifact_sha256"][name] == sha256(OWNED / name), (
        f"owned artifact hash mismatch: {name}"
    )

for path in OWNED.iterdir():
    if not path.is_file():
        continue
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path.name}"
    assert b"\r" not in data, f"non-LF newline: {path.name}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path.name}"
    )

probe = (OWNED / "IntakeProbe.lean").read_text(encoding="utf-8")
prohibited = re.compile(
    r"\b(sorry|admit|sorryAx)\b|^\s*(axiom|opaque|constant|unsafe)\s+", re.MULTILINE
)
assert not prohibited.search(probe), "prohibited Lean construct in IntakeProbe.lean"
assert "theorem " not in probe and "lemma " not in probe
assert "This file does not select, state, or prove the target" in probe

source_text = (ROOT / "Docs" / "researches" / "math_theorems.md").read_text(encoding="utf-8")
source_block = """**解析层次**
- 提出者: Stephen Kleene
- 时间: 1955
- 陈述: 解析集合的层次
- 重要性: 高
- 形式化状态: 已验证
"""
assert source_text.count(source_block) == 1
stage0_text = (ROOT / "Docs" / "Stage0_Blueprint.md").read_text(encoding="utf-8")
assert "- [ ] THM-M-0755 解析层次\n  - 定理内容: 解析集合的层次" in stage0_text

assert receipt["base_revision"] == instance["source_revisions"]["repository_base"] == BASE
assert receipt["base_tree"] == instance["source_revisions"]["repository_base_tree"] == BASE_TREE
assert instance["source_revisions"]["mathlib"] == MATHLIB
assert instance["source_revisions"]["mathlib_tree"] == MATHLIB_TREE
assert receipt["selftest_result"] == "pass"
assert receipt["accepted"] is receipt["content_addressed"] is False
assert receipt["covered_node_ids"] == ["S56-M-0755-INTAKE"]
assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
assert receipt["worker_input_hashes"]["lake_symlink_target_sha256"] == (
    "e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826"
)

print("intake invariant check: ok")
