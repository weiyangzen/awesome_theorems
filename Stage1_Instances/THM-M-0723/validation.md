# Intake validation

Base revision: `d19d83e12b57432e75cbb1c35f4577d5b0645cf9`.

This validation covers manifest membership, dossier structure, JSON integrity, source discovery,
and a narrow pinned Lean API probe. Because the repository record does not identify a proposition,
no canonical target, expression hash, mutation result, or proof is claimed. The canonical `.lake`
link and artifacts were used read-only; no update, build, clone, or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0723` | exit 0; rank 760, planned, legacy artifacts unaccepted, theorem_complete false |
| `rg -n -C 18 'THM-M-0723\|多项式层次\|复杂性类的层次结构' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | exit 0; only topic metadata plus open Stage0 fields found |
| `python3 -m json.tool Stage1_Instances/THM-M-0723/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0723/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; planned lifecycle, empty accepted state, open downstream DAG, and false terminal flags confirmed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0723/IntakeProbe.lean)` | exit 0; pinned language carrier and basic API elaborated under Lean 4.29.0 |
| `rg -n -i 'polynomial hierarchy\|PolynomialHierarchy\|ComplexityClass' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 1; expected no-match result in bounded pinned-mathlib search |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0723 -g '*.lean'` | exit 1; expected no-match result; no prohibited Lean placeholder or axiom |
| `git diff --check -- Stage1_Instances/THM-M-0723` | exit 0; no output |

Known downstream gates intentionally remain open: pinpoint source selection and independent review,
canonical statement elaboration and mutations, obligation/discovery freezes, anchor audit, proof,
trust and composition checks, hermetic replay, and release acceptance. They prevent theorem
completion but do not invalidate this truthful `planned` intake.
