#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-1430"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


target_data = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
targets = target_data if isinstance(target_data, list) else target_data["targets"]
target = next(item for item in targets if item["theorem_id"] == "THM-M-1430")
instance = load(OWNED / "instance.json")
dag = load(OWNED / "task-dag.json")
receipt = load(OWNED / "intake-receipt.json")

assert target["execution_rank"] == instance["execution_rank"] == 928
assert target["baseline"] == instance["baseline"] == "L0"
assert target["rework_required"] is instance["rework_required"] is True
assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
assert target["theorem_complete"] is instance["theorem_complete"] is False
assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == "THM-M-1430"
assert instance["item_id"] == receipt["item_id"] == "S56-M-1430-INTAKE"
assert instance["lifecycle_mode"] == instance["lifecycle"] == dag["lifecycle"] == "planned"
assert instance["intent"] == "intake"
assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
assert instance["canonical_formal_target"]["declaration_or_expression"] is None
assert instance["canonical_formal_target"]["elaborated_expression_hash"] is None
assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
assert instance["audit_complete"] is False and instance["theorem_complete"] is False
assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
assert dag["accepted_states"] == []

expected_tasks = [
    ("S56-M-1430-STATEMENT", ["S56-M-1430-INTAKE"]),
    ("S56-M-1430-ANCHOR_AUDIT", ["S56-M-1430-STATEMENT"]),
    ("S56-M-1430-OBLIGATION_TREE", ["S56-M-1430-ANCHOR_AUDIT"]),
    ("S56-M-1430-PROOF", ["S56-M-1430-OBLIGATION_TREE"]),
    ("S56-M-1430-VALIDATION", ["S56-M-1430-PROOF"]),
    ("S56-M-1430-RELEASE", ["S56-M-1430-VALIDATION"]),
]
assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
assert all(task["state"] == "open" for task in dag["tasks"])

owned_files = sorted(path.name for path in OWNED.iterdir() if path.is_file())
assert sorted(instance["owned_artifacts"]) == owned_files
hashed_files = [name for name in owned_files if name != "intake-receipt.json"]
assert sorted(receipt["untracked_owned_artifact_sha256"]) == sorted(hashed_files)
for name in hashed_files:
    digest = hashlib.sha256((OWNED / name).read_bytes()).hexdigest()
    assert receipt["untracked_owned_artifact_sha256"][name] == digest, (
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

base = "ffe94ac84965dc19f4923f88b7566072ddee37ae"
assert receipt["base_revision"] == base
assert instance["source_revisions"]["repository_base"] == base
assert instance["source_revisions"]["repository_base_tree"] == (
    "876a17f277d84dcf06ca672e5cd351edaa294495"
)
assert instance["source_revisions"]["mathlib"] == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert instance["source_revisions"]["lean_toolchain_file_sha256"] == (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
assert instance["source_revisions"]["lake_manifest_sha256"] == (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)
assert receipt["selftest_result"] == "pass" and receipt["accepted"] is False
assert receipt["content_addressed"] is False
assert receipt["covered_node_ids"] == ["S56-M-1430-INTAKE"]
assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
assert receipt["worker_input_hashes"]["lake_symlink_target_sha256"] == (
    "e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826"
)

print("intake invariant check: ok")
