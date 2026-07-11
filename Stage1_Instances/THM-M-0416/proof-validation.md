# THM-M-0416 proof-phase validation

Item: `S56-M-0416-PROOF`. Base revision:
`108284d893a06f2c566f9a7958581e78cbb50d02`.

`Proof.lean` integrates real pinned proof bodies for all four mathematical
packages in the frozen obligation tree. The exact root declaration is composed
with `root_of_packages`; it is not a broadened or substituted theorem.

Validation ran in the worker clone on 2026-07-12. The existing pinned `.lake`
artifacts were reused. No update, build, clone, fetch, or `.lake` mutation was
performed.

```text
cd Stage1_Instances/THM-M-0416
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
  -o Statement.olean Statement.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
  -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
  exit 0
  all five proof declarations depend only on:
    [propext, Classical.choice, Quot.sound]
rm -f Statement.olean ObligationTree.olean

python3 Stage1_Instances/THM-M-0416/check_proof.py
  exit 0: four frozen packages and exact root integrated

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0416
  exit 0: rank 71, planned, theorem_complete false

git diff --check -- Stage1_Instances/THM-M-0416 .stage1-worker-selftest.json
  exit 0; no output
```

The proof-phase machine root cut set is empty. This is not a theorem-completion
claim: provenance, trust, hermetic replay, independent validation, human source
and readability review, release, and master acceptance remain separate gates.
