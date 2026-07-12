# THM-M-0322 proof-phase validation

## Implemented proof

`Proof.lean` closes the exact target frozen in `Statement.lean`. It imports the
frozen composition module, proves the reverse inclusion from pinned mathlib's
`closure_convexHull_extremePoints`, and combines it with the already checked
forward inclusion through `root_of_inclusions`. Thus the proof exposes both
directions while its terminal mathematical body remains the exact theorem at
mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for the new
declarations. The proof source has no `sorry`, `admit`, `sorryAx`, new axiom, or
unsafe declaration. This is provisional proof-node evidence pending master
acceptance. Validation, release, H0, R0, hermetic replay, and independent
verification remain open, so this receipt does not claim theorem completion.

## Commands and exact results

Commands ran from base revision
`3d8dd27e4ff1200a2d9c8daaa9cae8072eca6241` on 2026-07-12. No update, build,
clone, fetch, network access, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: check_stage1_standard: ok (15 assurance groups, 41 legacy rows,
  300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0: stage1_target: ok (1546 unique targets, ranks 1..1546, all
  L0/rework_required)

python3 scripts/stage1_target.py show THM-M-0322
  exit 0: execution rank 819; planned; theorem_complete=false

bash Stage1_Instances/THM-M-0322/check_proof.sh
  exit 0: Statement.lean, ObligationTree.lean, and Proof.lean elaborated in an
  isolated temporary olean directory; hullExtreme_subset,
  root_of_inclusions, hullExtreme_superset, and kreinMilmanTarget_proof each
  reported [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0322/check_obligation_tree.py
  exit 0: PASS THM-M-0322 obligation tree: 19 obligations, 38 typed edges;
  frozen denominator d98f83a7242eccacc32e330ba44ed8c7a259e6f6df76e4959c89d26628d981a3

python3 Stage1_Instances/THM-M-0322/check_proof.py
  exit 0: PASS THM-M-0322 proof phase: pinned proof body closes the exact machine root

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0322/Proof.lean
  exit 1 with empty output: expected clean scan

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95
```
