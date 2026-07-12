# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`e9d545372b66f73be63271b2fb408ef134d1d6f7`.

This validation covers manifest membership, dossier structure, JSON integrity, prohibited-token
screening, and a narrow pinned Lean API probe. Because the repository record does not identify a
proposition, no canonical target, expression hash, mutation result, or proof is claimed. The
pre-existing shared canonical `.lake` link/artifacts were used read-only; no update, build, fetch,
or clone was run. The worktree already reported `?? Formalizations/Lean/.lake` at preflight, so this
is nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0516` | 0 | rank 890; planned; legacy artifacts unaccepted; theorem_complete false |
| `git status --short` | 0 | pre-existing `?? Formalizations/Lean/.lake`; no target dossier existed |
| `rg -n -i 'THM-M-0516\|岩泽理论\|分圆域的p-adic L-函数' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | only topic metadata and explicitly open Stage0 fields identify the target |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0516/IntakeProbe.lean)` | 0 | all six pinned API checks elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0516/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0516/task-dag.json` | 0 | valid JSON |
| scoped Python intake assertions | 0 | `intake invariant check: ok` |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0516 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0516` | 0 | no output |

Known downstream failures remain intentionally open: exact primary-source selection and
independent review, canonical statement elaboration and mutation tests, obligation/discovery
freezes, formal-anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem
completion but do not invalidate a truthful `planned` intake.
