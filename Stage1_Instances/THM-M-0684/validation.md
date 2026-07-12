# Intake validation

Base revision: `d4da54fa4b81642d3c351d58820f005903bbe09e`.

This record covers manifest membership, dossier structure, JSON integrity, source discovery, and a
narrow pinned Lean API probe. Since the repository gloss is not an exact proposition, it claims no
canonical target, expression hash, mutation result, or proof. The canonical `.lake` symlink and
existing pinned artifacts were used read-only; no update, build, clone, or fetch was run.

The exact validation commands and results are recorded below. Known downstream open gates are
source selection and independent review, exact statement elaboration and mutations,
obligation/discovery freezes, anchor audit, proof, hermetic replay, and release acceptance. These
prevent theorem completion but do not invalidate a truthful `planned` intake.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0684` | exit 0; rank 725, planned, legacy artifacts unaccepted, theorem_complete false |
| `rg -n -C 4 '第二不完备性定理\|哥德尔第二不完全性定理\|系统不能证明自身一致性\|一致形式系统不能证明自身一致性' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | exit 0; found the two underspecified source glosses and open Stage0 fields |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0684/IntakeProbe.lean)` | exit 0; language, sentence, theory, and bounded-formula encoding APIs elaborated |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0684 -g '*.lean'` | exit 1 as expected for no matches; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0684/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0684/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0684` | exit 0; no output |
