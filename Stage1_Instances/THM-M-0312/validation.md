# Intake validation

Base revision: `9b651a1d3f6c41876f66c5933991b6cbaceeb70d`.

Validation covers target membership, dossier structure, JSON integrity, and a narrow pinned Lean API
probe. It does not claim exact statement identity or proof closure. The worker clone's pre-existing
canonical `.lake` link and artifacts were used read-only; no update, build, fetch, or clone ran.

Commands were run from the repository root on 2026-07-12 unless a subshell is shown.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0312` | exit 0; rank 814, planned, legacy artifacts unaccepted, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0312/IntakeProbe.lean)` | exit 0; all three pinned Banach-Steinhaus declaration candidates and their full public types elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0312/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0312/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` for identity, planned lifecycle, L0 baseline, empty accepted states, false terminal flags, open ordered DAG, and artifact presence |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0312 -g '*.lean'` | exit 1, expected no-match result; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0312` | exit 0; no output |

Known downstream gates remain intentionally open: exact expression serialization and mutations,
primary-source and errata audit, independent review, obligation/discovery freezes, formal-candidate
provenance and trust audit, proof-state acceptance, hermetic replay, and release. These prevent
theorem completion but do not invalidate a truthful `planned` intake.
