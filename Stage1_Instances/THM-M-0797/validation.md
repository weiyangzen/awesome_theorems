# Intake validation

Base revision: `1c5adf59c0f8176526cb4c9fb281b3ff340c9eeb`.

Validation date: `2026-07-12` (`Asia/Shanghai`). This validation covers manifest membership,
dossier structure, JSON integrity, scoped intake invariants, and a narrow pinned Lean API probe.
Because the repository record does not identify a proposition, no canonical target, expression
hash, mutation result, diamond predicate, constructible-universe theorem, or proof is claimed. The
pre-existing canonical `.lake` artifacts were consumed read-only; no update, build, fetch, or clone
was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0797` | exit 0; rank 801, planned, legacy artifacts unaccepted, theorem_complete false |
| `rg -n -C 8 'THM-M-0797\|钻石原理' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json` | exit 0; only topic-level repository metadata and Stage0 open fields identify the target |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0797/IntakeProbe.lean)` | exit 0; seven nearby ordinal, closedness, and unboundedness API expressions elaborated |
| `rg -n -i 'diamond\|stationary\|\bclub\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib/SetTheory -g '*.lean'` | exit 0; sole match is a `club sets` TODO comment in `Ordinal/FixedPoint.lean`, with no diamond/stationary declaration located |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0797 -g '*.lean'` | exit 1 as expected for no matches; no prohibited placeholder or axiom occurs in the Lean probe |
| `python3 -m json.tool Stage1_Instances/THM-M-0797/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0797/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0797 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream gates intentionally remain open: primary-source selection and independent review,
selection of the exact diamond variant and foundation/model conventions, canonical statement
elaboration and mutation tests, discovery and obligation freezes, formal-anchor audit, proof,
hermetic replay, and release acceptance. They prevent theorem completion but do not invalidate a
truthful `planned` intake.
