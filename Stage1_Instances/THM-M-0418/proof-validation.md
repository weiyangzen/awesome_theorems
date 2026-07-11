# THM-M-0418 proof-phase validation

Item: `S56-M-0418-PROOF`. Base revision:
`4ee3e13d2f3ae78d194a8c9963de58c34b134a3c`.

`Proof.lean` proves the exact frozen `MinkowskiIdealClassBound` proposition by
applying the audited terminal declaration
`NumberField.exists_ideal_in_class_of_norm_le` from pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It also checks composition into
the literal pinned-source shape. The wrapper is repo-local; the single proof
body remains upstream and is not counted twice.

Validation ran on 2026-07-11 UTC using the canonical pinned `.lake` artifacts.
No update, build, clone, fetch, network access, or `.lake` mutation was run.

```text
cd Stage1_Instances/THM-M-0418
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o Statement.olean Statement.lean
  exit 0; one expected unused-variable mutation-fixture linter warning

LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
  exit 0; terminal, exact target, and source-shape transport each report:
    [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0418/check_proof.py
  exit 0: exact adapter and transport present; prohibited-source scan passed

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0418
  exit 0: rank 73, planned, theorem_complete false

python3 -m json.tool Stage1_Instances/THM-M-0418/proof-receipt.json
  exit 0

git diff --check -- Stage1_Instances/THM-M-0418 .stage1-worker-selftest.json
  exit 0; no output
```

Machine root closure is established provisionally for this proof node. This
does not establish theorem completion: H0 source acceptance, R0 readable
reconstruction, hermetic validation, independent verification, master
acceptance, and release remain later gates.
