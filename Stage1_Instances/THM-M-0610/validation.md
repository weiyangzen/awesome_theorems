# Intake validation record

Base revision: `15c189e825a13df6978f1010a5e2e9a7ddb27692`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0610` | 0 | rank 647; planned; L0/rework-required; source status untrusted; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0610/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0610/task-dag.json >/dev/null` | 0 | open task DAG is valid JSON |
| `jq -e '.item_id == "S56-M-0610-INTAKE" and .theorem_id == "THM-M-0610" and .execution_rank == 647 and .lifecycle_mode == "planned" and .theorem_complete == false and .audit_complete == false and .canonical_formal_target.gate_state == "open_pending_statement_and_source_disambiguation"' Stage1_Instances/THM-M-0610/intake.json >/dev/null` | 0 | identity, rank, lifecycle, open statement gate, and noncompletion boundary agree |
| `jq -e '.theorem_id == "THM-M-0610" and .lifecycle == "planned" and (.accepted_states \| length == 0) and ([.tasks[].state] \| all(. == "open"))' Stage1_Instances/THM-M-0610/task-dag.json >/dev/null` | 0 | every dependent phase is open and no state is accepted |
| `rg -n --glob '!validation.md' 'sorry\|admit\|sorryAx\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-0610` | 1 | no forbidden proof-escape match; exit 1 is ripgrep's no-match result |
| `git diff --check -- Stage1_Instances/THM-M-0610 .stage1-worker-selftest.json` | 0 | no whitespace errors |

These are the smallest real checks for an intake-only node. This dossier adds
no Lean declaration, so `lake env lean` would not validate any claimed
expression or proof and is not represented as kernel evidence. Exact statement
elaboration, source inspection, anchor discovery, proof, and every release
gate remain open. No theorem completion is claimed.

The worktree already contained the untracked `Formalizations/Lean/.lake` path
at preflight. It was neither created nor modified by this item. Its presence
makes the run dirty and nonrelease; the intake packet remains provisional until
the integration lane independently verifies it and issues master acceptance.
