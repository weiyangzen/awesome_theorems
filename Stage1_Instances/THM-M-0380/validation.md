# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`6f601f70dc531aafc2c0e73ea51db67cebeb3ad9`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify an exact estimate, no canonical
target, expression hash, mutation result, or proof is claimed. The canonical `.lake` symlink was
used read-only; no dependency update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0380` | exit 0; rank 868, planned, legacy artifacts unaccepted, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0380/IntakeProbe.lean)` | exit 0; four Fourier/Schwartz API checks elaborated; no local-smoothing proposition asserted |
| `rg -n -i 'Sogge\|local smoothing\|cinematic curvature' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 1; expected no-match exit; no phrase-level theorem candidate found in pinned mathlib |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0380 -g '*.lean'` | exit 1; expected no-match exit; no prohibited placeholder or axiom in the intake probe |
| `python3 -m json.tool Stage1_Instances/THM-M-0380/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0380/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check --no-index /dev/null <each new text artifact>` | exit 1 for each new file because it is an addition; no whitespace-error diagnostics |

Known downstream failures are deliberately open: exact primary-source and errata inspection,
independent source review, canonical Lean elaboration and mutation tests, obligation/discovery
freezes, immutable anchor audit, proof, hermetic replay, and release acceptance. They prevent audit
and theorem completion but do not invalidate this truthful `planned` intake.
