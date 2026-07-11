# THM-M-0003 proof-phase validation

## Implemented proof

`Proof.lean` imports the exact proposition frozen in `Statement.lean`. The
canonical `snakeLemma` wrapper applies the pinned mathlib declaration
`ShortComplex.SnakeInput.snake_lemma`. A second exact-target declaration passes
the four pinned segment bodies `L₀_exact`, `L₁'_exact`, `L₂'_exact`, and
`L₃_exact` through the already frozen `ObligationTree.root_compose` certificate.
Thus the wrapper checks both the exact root type and the frozen child-to-parent
architecture rather than relying only on a nearby theorem name.

No `sorry`, `admit`, new axiom, unsafe declaration, broadened hypothesis, or
substituted conclusion occurs in the proof artifact. Lean reports only
`propext`, `Classical.choice`, and `Quot.sound`. This is provisional proof-node
evidence pending master acceptance; downstream validation and release are not
claimed, and the theorem is not claimed complete.

## Commands and results

Commands ran from base revision
`ae68d10d70accbf26b8c8c53097b02a2ae2fa561` on 2026-07-12 local time.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0003
  exit 0: execution rank 98; planned; theorem_complete=false

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0003/check_proof.sh
  exit 0: isolated Statement, ObligationTree, and Proof elaboration passed;
  both exact-root declarations report propext, Classical.choice, Quot.sound

python3 Stage1_Instances/THM-M-0003/check_proof.py
  exit 0: exact declarations, pinned bodies, hashes, and prohibited-token scan passed

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95
```

No update, build, clone, fetch, or mutation of `.lake` was performed. Temporary
`.olean` files were isolated and removed by the validation script.
