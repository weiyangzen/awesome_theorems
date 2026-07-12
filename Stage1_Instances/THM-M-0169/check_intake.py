#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

intake = json.loads((HERE / "intake.json").read_text())
dag = json.loads((HERE / "task-dag.json").read_text())
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())

entries = targets["targets"] if isinstance(targets, dict) else targets
target = next(row for row in entries if row["theorem_id"] == "THM-M-0169")
assert target["execution_rank"] == 666
assert target["baseline"] == "L0" and target["rework_required"] is True
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

assert intake["schema_version"] == "stage1-instance/5.6.0"
assert intake["item_id"] == "S56-M-0169-INTAKE"
assert intake["theorem_id"] == dag["theorem_id"] == "THM-M-0169"
assert intake["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
assert intake["canonical_formal_target"]["elaborated_expression_hash"] is None
assert intake["canonical_formal_target"]["environment_fingerprint"] is None
assert intake["obligation_registry_hash"] is None
assert intake["theorem_complete"] is dag["theorem_complete"] is False
assert dag["accepted_tasks"] == []
assert all(task["state"] == "open" for task in dag["tasks"])

task_ids = {task["id"] for task in dag["tasks"]}
for task in dag["tasks"]:
    assert set(task["depends_on"]) <= task_ids

for relative in intake["public_merge_targets"]:
    assert relative.startswith("Stage1_Instances/THM-M-0169/")
    assert (ROOT / relative).is_file()

for name in ("README.md", "source_statement_crosswalk.md"):
    text = (HERE / name).read_text()
    assert "theorem_complete" in text or "theorem-completion" in text

print("check_intake: ok (THM-M-0169 planned, 9 open tasks, no accepted proof state)")
