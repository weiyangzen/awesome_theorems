# Intake validation record

Base revision: `056367be3b1cb2e101200085ec5a5fdff670d16b`.

The worktree already contained modifications to the generated blueprint and execution DAG. They
are outside this item's owned path and were neither edited nor used as acceptance evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1263` | 0 | rank 440; `planned`; theorem incomplete; lane `hard_mathlib_anchor_and_wrapper` |
| `python3 -m json.tool Stage1_Instances/THM-M-1263/intake.json >/dev/null` | 0 | intake JSON parsed successfully |
| `rg -n "sorry\|admit\|axiom\|placeholder\|fake result" Stage1_Instances/THM-M-1263 \|\| true` | 0 | only documentary uses of “axiom” describing future validation; no Lean proof or placeholder exists |
| `git diff --check -- Stage1_Instances/THM-M-1263` | 0 | no whitespace errors |

No Lean compilation is claimed: intake intentionally has no exact formal expression or Lean module.
The exact-statement gate remains open, so this receipt self-tests only the planned intake deliverable.
