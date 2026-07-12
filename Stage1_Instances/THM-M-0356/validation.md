# Intake validation

Base revision: `396f523f7db5499e43d86728d9cfe073ac081dfa`.

This record covers target membership, dossier structure, intake invariants, and a narrow pinned Lean
API probe. The probe receives no statement or proof credit. Existing canonical `.lake` artifacts
were reused read-only; no update, fetch, clone, dependency build, or other `.lake` mutation was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0356` | exit 0; rank 849, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0356/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0356/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| initial `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0356/IntakeProbe.lean)` with direct `Mathlib.Topology.CompactSupport` import | exit 1; the pinned cache lacked that module's `.olean`; the unnecessary direct import was removed rather than building or mutating `.lake` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0356/IntakeProbe.lean)` | exit 0; seven compact-support, Lp, orthonormality, and basis API checks elaborated |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0356 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0356 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are intentionally open: primary-source passage inspection and independent
review, theorem and convention freeze, canonical target elaboration and mutations, anchor audit,
obligation registry, proof, hermetic replay, and release acceptance. They prevent theorem completion
but not a truthful `planned` intake.
