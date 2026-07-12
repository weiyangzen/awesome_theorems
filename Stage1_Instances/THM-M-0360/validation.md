# Intake validation

Validation date: 2026-07-12 (Asia/Shanghai). Base revision:
`396f523f7db5499e43d86728d9cfe073ac081dfa`.

The pre-existing worktree entry `?? Formalizations/Lean/.lake` is the canonical pinned artifact
link reused by this worker. It was not created, fetched, updated, or modified as part of the intake.
No other target path was edited.

| Command (from repository root unless shown) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and exactly 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0360` | 0 | rank 853, L0/rework required, planned, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0360/IntakeProbe.lean)` | 0 | pinned Lean elaborated the five discovery-only multiplier/Lp declarations |
| `python3 -m json.tool Stage1_Instances/THM-M-0360/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0360/task-dag.json` | 0 | valid JSON |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b\|unsafe' Stage1_Instances/THM-M-0360/IntakeProbe.lean` | 1 | expected no-match exit; no prohibited Lean token found |
| `git diff --check -- Stage1_Instances/THM-M-0360` | 0 | no whitespace error |

Pinned environment evidence: Lean `leanprover/lean4:v4.29.0`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`;
`FourierMultiplier.lean` SHA-256
`32cc67663b5b681c0a2295d66dc627d2b6bc9222f984d82efc8ba0c7d7e5a535`.

## Validation boundary

This validates the intake structure and availability of nearby pinned Lean APIs only. It does not
elaborate a Herz-Stein statement, because the repository metadata does not uniquely identify one.
The first failed later gate is exact primary-source selection and statement freeze. Consequently
there is no statement fingerprint, obligation registry, axiom audit of a proof body, H0/R0 credit,
audit completion, or theorem completion.
