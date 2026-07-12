# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`).  
Base revision: `fc8e70dc8b3df070bf824de575d4a369542a621f`.

This validation covers target membership, dossier structure, JSON integrity, source discovery, and
a narrow pinned Lean API probe. Because the repository sources do not identify one exact
proposition, no canonical target, expression hash, mutation result, anchor result, or proof is
claimed. The pre-existing canonical `.lake` link and artifacts were used read-only; no update,
build, fetch, or clone was run. The untracked `.lake` link was already present at preflight and is
outside this target's owned path, so this is nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0331` | 0 | rank 824; planned; legacy artifacts unaccepted; theorem_complete false |
| `git status --short` | 0 | preflight showed only the pre-existing untracked `Formalizations/Lean/.lake` link |
| `rg -n -i 'THM-M-0331\|斯通定理\|单参数酉群与自伴算子\|酉群与自伴算符的指数关系' Docs/researches/math_theorems.md Docs/researches/physics_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json` | 0 | located the two topic glosses, Stage0 open fields, and selected manifest record |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| bounded `rg` Stone/unitary/self-adjoint search under pinned `Mathlib` | 0 | found other Stone-named theorems but no declaration identified as the one-parameter unitary-group theorem; discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0331/IntakeProbe.lean)` | 0 | eight partial-operator, self-adjoint, unitary, and continuity API checks elaborated |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0331 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom in the Lean probe |
| `python3 -m json.tool Stage1_Instances/THM-M-0331/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0331/task-dag.json` | 0 | valid JSON |
| scoped Python intake assertions | 0 | manifest/DAG identity, planned lifecycle, null target, empty accepted states, open downstream tasks, and artifact inventory passed |
| `git diff --check -- Stage1_Instances/THM-M-0331 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Known downstream failures are intentionally open: immutable exact source selection and independent
review; direction, convention, and boundary decisions; canonical statement elaboration and
mutation tests; obligation and discovery freezes; formal-anchor audit; proof and composition;
hermetic replay; and release acceptance. These prevent audit and theorem completion but do not
invalidate a truthful self-tested `planned` intake.

