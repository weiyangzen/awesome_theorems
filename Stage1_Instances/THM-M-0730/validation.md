# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`d19d83e12b57432e75cbb1c35f4577d5b0645cf9`.

This validation covers manifest membership, dossier structure, scoped invariants, and a narrow
pinned Lean API probe. Because the repository record does not identify a proposition, no canonical
target, expression hash, mutation result, source acceptance, or proof is claimed. The pre-existing
canonical `.lake` link/artifacts were used read-only; no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0730` | exit 0; rank 767, planned, legacy artifacts unaccepted, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0730/IntakeProbe.lean)` | exit 0; all seven general graph/finite/rational API checks elaborated; no canonical theorem asserted |
| `python3 -m json.tool Stage1_Instances/THM-M-0730/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0730/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0730 -g '*.lean'` | exit 1 as expected for no matches; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0730` | exit 0; no output |

Known downstream failures are intentionally open: exact primary-source inspection and independent
review, selection of gap amplification versus the PCP consequence, parameter and boundary freeze,
canonical statement elaboration and mutation tests, obligation/discovery freezes, anchor audit,
proof, hermetic replay, and release acceptance. They prevent theorem completion but do not
invalidate a truthful `planned` intake.
