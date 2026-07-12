# Intake validation

Base revision: `32404187d6cee70b44ae90adf8d0d765752e5149`.

Validation date: `2026-07-12` (`Asia/Shanghai`). This validation covers manifest membership,
dossier structure, JSON integrity, and a narrow pinned Lean API probe. Because the repository record
does not identify a proposition, no canonical target, expression hash, mutation result, Woodin
predicate, or proof is claimed. The pre-existing canonical `.lake` link and artifacts were used
read-only; no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0791` | exit 0; rank 796, planned, legacy artifacts unaccepted, theorem_complete false |
| `rg -n -C 8 'THM-M-0791\|伍丁基数' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json` | exit 0; only topic-level repository metadata and Stage0 open fields identify the target |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0791/IntakeProbe.lean)` | exit 0; six nearby cardinal/ZFC APIs elaborated |
| `rg -n -i 'woodin' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 1; expected no-match exit in the bounded pinned-mathlib search |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0791 -g '*.lean'` | exit 1; expected no-match exit, so no prohibited placeholder or axiom occurs in the Lean probe |
| `python3 -m json.tool Stage1_Instances/THM-M-0791/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0791/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0791` | exit 0; no output |

Known downstream failures are intentionally open: primary-source selection and independent review,
canonical statement elaboration and mutation tests, obligation and discovery freezes, formal-anchor
audit, proof, hermetic replay, and release acceptance. They prevent theorem completion but do not
invalidate a truthful `planned` intake.
