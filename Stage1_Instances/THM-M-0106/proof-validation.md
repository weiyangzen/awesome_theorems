# THM-M-0106 proof-phase validation

Item: `S56-M-0106-PROOF`. Base revision:
`5f9b9aa5be620b78a09a5b1b2fd877e0c9051251`.

## Implemented body

`Proof.lean` proves the exact frozen `NoetherNormalizationTarget`. It invokes
the pinned mathlib theorem `exists_finite_inj_algHom_of_fg`, retains its
injective finite algebra map, and constructs the required affine-space
morphism with the frozen `affineSpaceMorphism`. `IsFinite.SpecMap_iff` and
postcomposition by `AffineSpace.SpecIso.inv` prove finiteness; simplification
proves the required morphism equation. There is no premise on the theorem and
no `sorry`, local axiom declaration, unsafe declaration, substituted target,
or new dependency.

This is proof-phase evidence only. It closes the frozen root at the level of a
kernel-elaborated proof body, but does not claim theorem completion: source and
readability review, validation and release receipts, hermetic replay,
independent verification, and master acceptance remain open.

## Commands and results

Validation ran from the worker clone on 2026-07-12 (Asia/Shanghai). The
existing canonical pinned `.lake` artifacts were reused. No dependency update,
build, clone, or fetch was run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0106
  exit 0: rank 30, planned, L0/rework_required, theorem_complete=false

cd Stage1_Instances/THM-M-0106
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
  -o Statement.olean Statement.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
rm -f Statement.olean
  exit 0: noetherNormalization_proof has the exact frozen type and reports
  axioms [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0106/check_proof.py
  exit 0: exact unconditional proof body and required pinned bridges passed

python3 Stage1_Instances/THM-M-0106/check_statement.py
  exit 0: expression SHA-256 4980834b63da78609158f944b53234d72089e2bfaacb348461de2651aa671209;
  all four structural mutations distinguished

python3 Stage1_Instances/THM-M-0106/check_anchor_audit.py
  exit 0: audit expression definitionally matches the frozen target and the
  pinned candidate closure elaborates

python3 Stage1_Instances/THM-M-0106/check_obligation_tree.py
  exit 0: 18 frozen obligations and 39 typed edges passed; this earlier
  freeze artifact truthfully retains its pre-proof open boundary

git diff --check -- Stage1_Instances/THM-M-0106 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The node-specific receipt is `proof-receipt.json`. Its support state is
provisional worker self-test; only the integration lane can accept it.
