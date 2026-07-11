# Intake validation

Base revision: `65062914df38e17a7b33d43f303feb92974e31b5`.

Commands were run from the repository root on 2026-07-12 (Asia/Shanghai). Validation is limited to
manifest consistency, dossier structure, scoped intake invariants, JSON syntax, and whitespace.
There is no canonical Lean expression, so no elaboration or kernel result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1076/intake.json >/dev/null` | 0 | Structured intake parsed as JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1076/task-dag.json >/dev/null` | 0 | Open task DAG parsed as JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | Passed: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1076` | 0 | Confirmed rank 518, planned lifecycle, L0/rework-required, unaccepted legacy artifacts, and theorem incomplete |
| scoped Python dossier assertions | 0 | `intake invariant check: ok`; exact file set, IDs, rank, lifecycle, ambiguity gate, empty accepted state, false completion flags, DAG order, and open downstream nodes checked |
| `rg -n '\bsorry\b\|\baxiom\b\|\bplaceholder\b\|THM-M-0387' Stage1_Instances/THM-M-1076 --glob '!validation.md'` | 1 | No prohibited proof token or copied fixture ID; exit 1 is the expected no-match result |
| `git diff --check -- Stage1_Instances/THM-M-1076 .stage1-worker-selftest.json` | 0 | No whitespace errors |

Known downstream failures are exact source identification, canonical Lean elaboration, formal
anchor audit, obligation registry, proof, hermetic replay, and independent review. They prevent
theorem completion but do not invalidate a fail-closed planned intake.
