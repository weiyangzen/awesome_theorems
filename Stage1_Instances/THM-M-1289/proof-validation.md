# THM-M-1289 proof-phase validation

Item: `S56-M-1289-PROOF`. Base revision:
`14963a4fe0de015a5205ea2978fd0bf8fdc09b55`.

`Proof.lean` supplies real local bodies for strict positivity and infinite Frechet smoothness of the
exact frozen bubble. Positivity follows from `n >= 3`, positive scale, and the positive squared
denominator. Smoothness uses the smooth squared norm on a real inner-product space, nonvanishing of
the positive denominator, division, and real powers away from zero. The new conditional composition
removes these two premises but retains the exact PDE, critical function-norm, gradient-norm, and
sharp-extremal components. Thus the root and theorem are not claimed closed.

## Commands and results

Commands ran on 2026-07-12 inside this worker clone. The existing canonical pinned `.lake`
artifacts were reused; no update, build, dependency clone, fetch, or `.lake` mutation was run.

```text
cd Stage1_Instances/THM-M-1289
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
  -o Statement.olean Statement.lean
  exit 0; the four intentional check_failure mutation diagnostics appeared

LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
  -o ObligationTree.olean ObligationTree.lean
  exit 0; conditional composition axioms: propext, Classical.choice, Quot.sound

LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
  exit 0; bubble_pos, contDiff_bubble, and conditional root composition each report only
  propext, Classical.choice, Quot.sound

python3 Stage1_Instances/THM-M-1289/check_obligation_tree.py
  exit 0; frozen 20-node registry and typed graphs passed

python3 Docs/tools/check_stage1_standard.py
  exit 0; rev-5.6 standard and 1546-target coverage passed

python3 scripts/stage1_target.py check
  exit 0; 1546 unique uniform-L0 targets passed

python3 scripts/stage1_target.py show THM-M-1289
  exit 0; rank 460, planned, theorem_complete false

rg -n "\\b(sorry|axiom|admit|unsafe)\\b" Stage1_Instances/THM-M-1289/Proof.lean
  exit 1 with no output; no forbidden marker occurred

git diff --check -- Stage1_Instances/THM-M-1289 .stage1-worker-selftest.json
  exit 0; no whitespace errors
```

The temporary `Statement.olean` and `ObligationTree.olean` were removed after validation. The
pre-existing untracked worker `.lake` link makes this nonrelease evidence. Master acceptance and
the later validation/release nodes remain required.
