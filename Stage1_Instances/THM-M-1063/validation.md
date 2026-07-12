# Intake validation

Base revision: `23e8c7fd5602b359d75252bd4e37074a071f0c68`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. There is no canonical Lean expression yet, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1063/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1063/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1063` | exit 0; rank 506, L0/rework_required, planned, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-1063 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures at intake: pinpoint primary-source inspection, canonical Lean elaboration, anchor
audit, obligation registry, proof, hermetic replay, and independent review remain open. They prevent
theorem completion but do not invalidate this fail-closed planned intake.

## Statement phase (2026-07-12)

The exact target in `DonskerTarget.lean` was checked in the pinned repository environment. This is
an elaboration receipt, not a proof receipt: the file defines the proposition and uses `#check`; it
does not declare a theorem, proof body, axiom, or placeholder.

| Command | Result |
|---|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1063/DonskerTarget.lean` | exit 0; exact target, direct expansion, and checked equivalence elaborated; printed `AwesomeTheorems.Stage1.THM_M_1063.DonskerInvariancePrinciple.{u_1, u_2} : Prop` |
| `rg -n -i 'brownian|wiener' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 1; no pinned mathlib declaration found |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-1063/DonskerTarget.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `de889c...a1847`, `651c8a...b1d2`, `321626...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1063` | exit 0; rank 506, L0/rework-required, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1063 .stage1-worker-selftest.json` | exit 0; no output |

Environment: repository base `205d13cfc35c45883410c569709a91cb34edce16`, Lean toolchain
`leanprover/lean4:v4.29.0`, mathlib pin `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
