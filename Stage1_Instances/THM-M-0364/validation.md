# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`ded29702119d0d4880db9fcf1d0a6560a89058fd`.

This validation covers target membership, dossier structure, JSON integrity, official
bibliographic identification, and a narrow pinned Lean API probe. Since the repository record does
not contain the source theorem's hypotheses, no canonical target, expression hash, mutation result,
formal anchor, or proof is claimed. The existing canonical `.lake` link/artifacts were used
read-only; no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0364` | exit 0; rank 856, planned, legacy artifacts unaccepted, theorem_complete false |
| `rg -n -C 18 'T1 theorem\|L2 boundedness of singular integral operators\|David.*Journe' Docs/researches Docs -g '*.md' -g '*.json'` | exit 0; repository source, Stage0 projection, manifest, and generated projection agree on the sparse metadata |
| `curl -L -s --max-time 30 https://annals.math.princeton.edu/1984/120-2/p07` with metadata field extraction | exit 0; official page identifies David/Journe, title, volume 120 (1984), pages 371-397, DOI 10.2307/2006946; no abstract/theorem text |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0364/IntakeProbe.lean)` | exit 0; five generic measure/Lp/continuous-operator APIs elaborated |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0364 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0364/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0364/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; target IDs, planned lifecycle, empty accepted states, open downstream tasks, and false terminal flags agree |
| `git diff --check -- Stage1_Instances/THM-M-0364` | exit 0; no whitespace errors |

Known downstream gates remain intentionally open: immutable primary theorem passage and independent
review; exact statement and boundary freeze; Lean elaboration and mutations; obligation/discovery
freezes; formal-anchor audit; proof, trust and provenance closure; hermetic replay; and release
acceptance. They prevent theorem completion but do not invalidate this truthful `planned` intake.
