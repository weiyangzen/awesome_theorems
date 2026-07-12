# Intake validation record

Base revision: `82592a2cd69e194c41c57127bd211a94db5f3db4`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0605` | 0 | rank 643; planned; L0/rework-required; source status untrusted; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0605/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0605/task-dag.json >/dev/null` | 0 | open task DAG is valid JSON |
| `rg -n --glob '!validation.md' 'sorry\|admit\|sorryAx\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-0605` | 1 | no forbidden Lean proof-escape match; exit 1 is ripgrep's no-match result |
| `git diff --check -- Stage1_Instances/THM-M-0605 .stage1-worker-selftest.json` | 0 | no whitespace errors |

These are the smallest real checks for an intake-only node. This dossier adds
no Lean declaration, so `lake env lean` would not validate any claimed
expression or proof and is not represented as kernel evidence. Exact statement
elaboration, source inspection, anchor audit, proof, and all release checks are
open. No theorem completion is claimed.

The worktree already contained the untracked `Formalizations/Lean/.lake` path
at preflight. It was not created or modified by this item. Its presence makes
this a dirty, nonrelease run; this intake receipt remains provisional pending
master acceptance.
