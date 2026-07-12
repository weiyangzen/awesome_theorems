# Intake validation

Item: `S56-M-0385-INTAKE`  
Base revision: `6f601f70dc531aafc2c0e73ea51db67cebeb3ad9`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

This validation covers manifest membership, dossier structure, JSON integrity, source-record
discovery, and a narrow pinned Lean API probe. Because the repository wording does not select one
proposition, no canonical target, expression hash, mutation result, proof, or theorem completion is
claimed. The pre-existing canonical `.lake` link and artifacts were used read-only; no dependency
update, build, fetch, or clone was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0385` | 0 | rank 872; planned; no accepted legacy artifact; theorem_complete false |
| `git rev-parse HEAD` | 0 | `6f601f70dc531aafc2c0e73ea51db67cebeb3ad9` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `rg -n -i 'THM-M-0385\|Bourgain\u548c\u79ef\|\u548c\u96c6\u4e0e\u79ef\u96c6\u7684\u5927\u5c0f\u5173\u7cfb' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json` | 0 | found only the topic gloss and open Stage0 fields for this target; a separate adjacent record shares the gloss |
| `python3 -m json.tool Stage1_Instances/THM-M-0385/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0385/task-dag.json` | 0 | valid JSON |
| scoped Python assertions over the instance, DAG, and owned file set | 0 | `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0385/IntakeProbe.lean)` | 0 | eight real/prime-field finite sumset, product-set, and cardinality expressions elaborated |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0385 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0385` | 0 | no output |

Known downstream failures are deliberately open: exact source selection and independent review,
canonical statement elaboration and mutation tests, formal-candidate audit, obligation registry,
proof, hermetic replay, and release acceptance. These prevent theorem completion but do not
invalidate this truthful `planned` intake.
