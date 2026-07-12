# THM-M-0708 proof-phase validation

## Implemented proof

`Proof.lean` adopts the immutable mathlib declaration `ComputablePred.rice` audited in the preceding
phase. `riceBridge` supplies the exact `RiceBridge` interface frozen by the obligation tree, and
`riceTheorem` passes that body to `root_of_riceBridge`. The independent declaration
`riceTheorem_direct` checks the same exact root without the intermediate composition theorem.

All three declarations elaborate without `sorry`, `admit`, `sorryAx`, a new axiom, or an unsafe
declaration. Lean reports only `propext`, `Classical.choice`, and `Quot.sound`. This is provisional
proof-node evidence pending master acceptance. The downstream validation and release gates remain
separate, so theorem completion is not claimed.

## Commands and results

Commands ran from base revision `ed278d07d4b1fbd48887625b78d32141bebc9441` on 2026-07-12
(receipt timestamp `2026-07-12T08:11:22Z`).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0708
  exit 0: execution rank 749; planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0708/check_obligation_tree.py
  exit 0: 13 obligations and 30 typed edges passed; the frozen pre-proof
  snapshot truthfully remains open M3 pending proof-phase bridge adoption

python3 Stage1_Instances/THM-M-0708/check_proof.py
  exit 0: exact declarations, pinned body, frozen composition route, and
  prohibited-token scan passed

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0708/check_proof.sh
  exit 0: isolated ObligationTree and Proof elaboration passed; the frozen
  composition theorem and all three proof declarations report only propext,
  Classical.choice, and Quot.sound

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95

git diff --check -- Stage1_Instances/THM-M-0708
  exit 0: no whitespace errors
```

No `lake update`, `lake build`, clone, fetch, network access, or mutation of `.lake` was performed.
The check script uses a temporary directory and removes its generated `.olean` file on exit.
