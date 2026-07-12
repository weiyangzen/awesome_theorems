# Intake validation

Base revision: `2ff2721a0184cf5f856054cb7d46b10dbc703f5a`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean prerequisite-API probe. Since the machine model and source formulation are not selected, the
probe is not a canonical target and supplies no statement or proof credit. The canonical `.lake`
artifacts were used read-only; no update, build, clone, fetch, or dependency mutation was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0707` | exit 0; rank 748, L0/rework_required, planned, legacy artifacts unaccepted, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | exit 0; Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0707/IntakeProbe.lean` | exit 0; all six pinned partial-recursive-code API checks elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0707/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0707/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant)[[:space:]]' Stage1_Instances/THM-M-0707 -g '*.lean'` followed by an expected-no-match assertion | exit 0; `rg` returned 1 as expected, so the owned Lean source contains none of the prohibited tokens |
| `git diff --check -- Stage1_Instances/THM-M-0707` | exit 0; no output |

Known downstream failures are intentionally open: immutable source selection and review, canonical
statement elaboration and mutations, checked transport between machine models, discovery and
obligation freezes, full anchor/provenance audit, proof, hermetic replay, and independent release
review. They block theorem completion but do not invalidate a truthful `planned` intake.
