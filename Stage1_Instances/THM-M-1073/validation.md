# Intake validation record

Base revision: `23e8c7fd5602b359d75252bd4e37074a071f0c68`.

Validation is limited to repository/manifest consistency, dossier structure, fail-closed intake
invariants, and whitespace. No Lean elaboration is possible because the source supplies no eligible
proposition, and no kernel-proof result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1073` | 0 | rank 515; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1073/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1073/task-dag.json >/dev/null` | 0 | open task DAG is valid JSON |
| scoped intake assertion command below | 0 | printed `intake invariant check: ok`; ID/schema/lifecycle/source blocker/no-proof invariants hold |
| `git diff --check -- Stage1_Instances/THM-M-1073 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The scoped assertion command is:

```bash
python3 -c 'import json; p="Stage1_Instances/THM-M-1073/intake.json"; d=json.load(open(p)); t=json.load(open("Stage1_Instances/THM-M-1073/task-dag.json")); assert d["schema_version"] == "stage1-instance/5.6.0"; assert d["item_id"] == "S56-M-1073-INTAKE"; assert d["theorem_id"] == "THM-M-1073"; assert d["lifecycle_mode"] == "planned"; assert d["canonical_statement"] is None; assert d["canonical_formal_target"]["gate_state"] == "blocked_missing_exact_human_statement"; assert d["accepted_proof_state"] == []; assert d["theorem_complete"] is False; assert t["accepted_states"] == []; assert [x["id"] for x in t["tasks"]] == ["S56-M-1073-STATEMENT", "S56-M-1073-ANCHOR_AUDIT", "S56-M-1073-OBLIGATION_TREE", "S56-M-1073-PROOF", "S56-M-1073-VALIDATION", "S56-M-1073-RELEASE"]; assert all(x["state"] == "open" for x in t["tasks"]); print("intake invariant check: ok")'
```

Master acceptance and every dependent phase remain outstanding. The exact-statement recovery
condition is documented in the dossier rather than hidden by a substituted theorem.
