# Intake validation

Base revision: `cc46a50150dae27c90dca0938294d8da17db9109`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Since the source normalization and exact representation remain open, it does not
claim a canonical target, expression hash, mutation result, orthonormality, completeness, or proof.
The pre-existing canonical `.lake` symlink/artifacts were used read-only; no update, build, fetch,
or clone command was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0353` | exit 0; rank 846, planned, legacy artifacts unaccepted, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-0353/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0353/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0353/IntakeProbe.lean)` | exit 0; seven pinned Hermite-polynomial, `Lp`, measure, and Hilbert-basis API checks elaborated |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0353 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0353` | exit 0; no output |

Known downstream failures are intentionally open: primary-source selection and independent review,
normalization and boundary freeze, canonical statement elaboration and mutation tests, exhaustive
anchor audit, obligation registry, proof, hermetic replay, and release acceptance. They prevent
theorem completion but do not invalidate a truthful `planned` intake.
