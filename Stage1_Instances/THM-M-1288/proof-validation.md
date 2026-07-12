# THM-M-1288 proof-phase validation

Item: `S56-M-1288-PROOF`. Base revision:
`86b5fbdd7aeb66bbca3069f46c207c1d5f20790e`.

This proof phase adds real local proof bodies for three bounded parts of the
frozen tree: the elementary domain consequences (`M1288-S-DOMAIN`), the exact
pointwise and integral-expression gradient/Frechet transport
(`M1288-N-GRADIENT`), and the zero-function half of the exhaustive boundary
split (`M1288-B-BOUNDARY`). It also rechecks exact conditional composition.
The sharp analytic estimate and least-constant proof remain explicit package
arguments, so the root remains open and theorem completion is not claimed.

Validation ran from the worker clone on 2026-07-12. Existing canonical pinned
`.lake` artifacts were reused through the worker symlink. No update, build,
dependency clone, or fetch was run.

```text
cd Stage1_Instances/THM-M-1288
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o Statement.olean Statement.lean
  exit 0
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o ObligationTree.olean ObligationTree.lean
  exit 0
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
  exit 0
  every printed declaration depends only on:
    [propext, Classical.choice, Quot.sound]
rm -f Statement.olean ObligationTree.olean

python3 Stage1_Instances/THM-M-1288/check_proof.py
  exit 0: PASS; local bounded leaves closed, root remains conditional
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1288
  exit 0: rank 459, planned, theorem_complete false
python3 Stage1_Instances/THM-M-1288/check_obligation_tree.py
  exit 0: obligation tree and conditional composition valid
git diff --check -- Stage1_Instances/THM-M-1288 .stage1-worker-selftest.json
  exit 0; no output
```

No placeholder, new axiom, unsafe declaration, fake result, or substituted
target occurs in `Proof.lean`. The exact remaining machine cut set still
includes `M1288-N-ELPNORM`, `M1288-N-REARRANGEMENT`, `M1288-N-RADIAL`,
`M1288-L-WEIGHTED`, `M1288-L-GAMMA`, `M1288-C-EXTREMIZERS`, and
`M1288-L-LOWER-BOUND`, then the two package terminals and root composition.
Master acceptance remains required.
