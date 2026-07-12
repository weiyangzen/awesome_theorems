# THM-M-0982 proof-phase validation

Item: `S56-M-0982-PROOF`. Base revision:
`5e4c113b5fdd950714aacb1c46886e07431e3cd5`.

`Proof.lean` imports the exact target frozen by `Statement.lean` and closes both
branches. Continuity from below applies the pinned mathlib union theorem.
Continuity from above explicitly converts measurability to null measurability
and obtains a finite member from the probability-measure instance before
applying the pinned intersection theorem. The two bodies compose into the
exact `ProbabilityContinuityTarget` conjunction.

Validation ran from the worker clone on 2026-07-12. The existing canonical
pinned `.lake` artifacts were reused; no update, build, dependency clone, or
fetch was run. The temporary local `Statement.olean` was removed afterward.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0982
  exit 0: rank 262, planned, L0/rework_required, theorem_complete false

python3 Stage1_Instances/THM-M-0982/check_proof.py
  exit 0: PASS THM-M-0982 proof phase: exact frozen target has a
  placeholder-free proof body

cd Stage1_Instances/THM-M-0982
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
  -o Statement.olean Statement.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
  exit 0
  continuityFromBelow depends on axioms:
    [propext, Classical.choice, Quot.sound]
  continuityFromAbove depends on axioms:
    [propext, Classical.choice, Quot.sound]
  probabilityContinuity depends on axioms:
    [propext, Classical.choice, Quot.sound]
rm -f Statement.olean

python3 Stage1_Instances/THM-M-0982/check_obligation_tree.py
  exit 0: 11 frozen obligations and 23 typed edges passed; the recorded
  denominator is e7e587af7868a029493fd68e95b913630d7c0225f2b50d52b5afe10e8008456b

git diff --check -- Stage1_Instances/THM-M-0982 .stage1-worker-selftest.json
  exit 0; no output
```

No `sorry`, `admit`, axiom declaration, unsafe declaration, placeholder, or
substituted target is present. This self-tests proof integration only. The
separate validation and release nodes, human-source acceptance, readable
reconstruction, hermetic replay, and independent review remain open, so
theorem completion is not claimed. Master acceptance is still required.
