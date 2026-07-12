# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`e9252b1cfdc99a094324c8a10d260769df2eca15`.

This validation covers manifest membership, planned dossier invariants, source extraction, JSON
integrity, and a narrow pinned Lean elliptic-curve API probe. It does not validate an exact Lean
statement or proof. The canonical `.lake` link/artifacts were used read-only; no update, build,
clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0519` | 0 | rank 892; planned; legacy artifacts unaccepted; theorem_complete false |
| `sha256sum /tmp/bcdt.pdf` | 0 | primary paper PDF hash `1e34130e55a0ef39d7ef2566cc7d518e2b69048dece36328a0b6530e92044cf2` |
| `pdftotext -f 1 -l 5 -layout /tmp/bcdt.pdf -` | 0 | printed pages 843-847 contain Theorem A, the six equivalent definitions, and initial proof split |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0519/IntakeProbe.lean)` | 0 | four API checks and the nonsingularity witness example elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0519/instance.json` | 0 | JSON valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0519/task-dag.json` | 0 | JSON valid |
| scoped Python intake assertions | 0 | `intake invariant check: ok` |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0519 -g '*.lean'` | 1 | expected no-match exit; no placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0519` | 0 | no output |

Known downstream failures remain open by design: canonical modularity encoding, expression hash,
mutation tests, complete primary-source/errata review, obligation and discovery freezes, formal
anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem completion but
do not invalidate this truthful `planned` intake.
