# Intake validation

Base revision: `bd0d227173ac95971603f633607751754850337e`.

Validation is limited to manifest consistency, dossier structure, JSON integrity, scoped intake
invariants, and a narrow pinned Lean API probe. No canonical expression, statement mutation,
formal anchor, proof, or theorem completion is claimed. The pre-existing canonical `.lake` link was
used read-only; no update, fetch, clone, or build was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0347` | exit 0; rank 840, planned, legacy artifacts unaccepted, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0347/IntakeProbe.lean)` | exit 0; seven pinned periodic-Fourier and uniform-convergence API checks elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0347/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0347/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0347 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0347` | exit 0; no output |

Known downstream failures are intentionally open: exact primary-source pinpoint and independent
review, all convention decisions, canonical target elaboration and mutation tests, obligation and
discovery freezes, anchor audit, proof, hermetic replay, and release acceptance. They prevent
theorem completion but do not invalidate a truthful `planned` intake.
