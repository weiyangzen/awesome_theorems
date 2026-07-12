# Intake validation

Base revision: `2ff2721a0184cf5f856054cb7d46b10dbc703f5a`.

Validation date: `2026-07-12` (`Asia/Shanghai`). This validation covers target membership, dossier
structure, JSON integrity, source-record discovery, and a narrow pinned Lean relation-API probe.
The pre-existing canonical `.lake` link and artifacts were used read-only; no update, build, clone,
or fetch was run. The probe is not a lambda-calculus statement or proof.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0705` | 0 | rank 746; planned; legacy artifacts unaccepted; theorem_complete false |
| `rg -n -C 8 'THM-M-0705|Church-Rosser' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | repository gloss and open Stage0 fields located |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0705/IntakeProbe.lean)` | 0 | all six generic relation API checks elaborated; no lambda-calculus theorem asserted |
| `python3 -m json.tool Stage1_Instances/THM-M-0705/instance.json` | 0 | intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0705/task-dag.json` | 0 | open DAG JSON is syntactically valid |
| scoped Python intake assertions | 0 | `intake invariant check: ok`; planned lifecycle, open tasks, and empty acceptance state agree |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0705 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0705` | 0 | no output |

Known downstream work is intentionally open: primary-source inspection and independent review,
canonical statement elaboration and mutation tests, anchor and provenance audit, frozen obligation
graphs, proof, trust closure, hermetic replay, readable reconstruction, and release acceptance. These
prevent theorem completion but do not invalidate a truthful self-tested `planned` intake.
