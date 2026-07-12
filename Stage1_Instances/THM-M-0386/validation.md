# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`6f601f70dc531aafc2c0e73ea51db67cebeb3ad9`.

This validation covers manifest membership, dossier structure, JSON integrity, scoped intake
invariants, and a narrow pinned Lean API probe. Because the repository record does not identify a
unique proposition, no canonical target, expression hash, mutation result, source-proof status, or
proof is claimed. The pre-existing canonical `.lake` link/artifacts were used read-only; no update,
build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0386` | exit 0; rank 873, planned, legacy artifacts unaccepted, theorem_complete false |
| `rg -n -C 8 'THM-M-0386\|Elekes\|多项式在格点' Docs/researches Docs/Stage0_Blueprint.md Formalizations Stage1_Instances -g '!Stage1_Instances/THM-M-0386/**'` | exit 0; only repository metadata/gloss and a distinct Elekes sum-product entry were found; no theorem-specific formal artifact |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0386/IntakeProbe.lean)` | exit 0; six candidate polynomial/finite-grid APIs elaborated |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0386 -g '*.lean'` | exit 1, expected no-match result; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0386/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0386/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0386` | exit 0; no output |

Known downstream failures are intentionally open: immutable primary-source inspection and
independent review, exact statement and boundary selection, canonical Lean elaboration and mutation
tests, obligation/discovery freezes, anchor audit, proof, hermetic replay, and release acceptance.
They prevent theorem completion but do not invalidate this truthful `planned` intake.

