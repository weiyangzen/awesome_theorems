# Intake validation

Base revision: `3f994388953e417edafd54b069ab45d648619698`.

Validation date: `2026-07-12` (`Asia/Shanghai`). This covers target membership, dossier structure,
JSON integrity, and a narrow pinned Lean statement-vocabulary probe. The existing canonical `.lake`
artifacts were used read-only; no dependency update, build, clone, or fetch was run. The probe is not
the canonical theorem and provides no proof credit.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0510` | exit 0; rank 884, planned, legacy artifacts unaccepted, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0510/IntakeProbe.lean)` | exit 0; partition type/Fintype, `atTop`, `IsEquivalent`, and the real main-term expression elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0510/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0510/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0510 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0510` | exit 0; no output |

Known downstream gates remain intentionally open: exact primary-source formula/page and independent
review, canonical statement hash and mutations, discovery and obligation freezes, formal-anchor
audit, proof, trust and provenance closure, hermetic replay, and release acceptance. These prevent
theorem completion but do not invalidate a truthful `planned` intake.
