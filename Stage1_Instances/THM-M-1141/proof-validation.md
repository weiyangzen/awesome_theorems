# THM-M-1141 proof-phase validation

Item: `S56-M-1141-PROOF`. Base revision:
`24c7a19c1a6033b0aed791e0127a3b3e3564a7b0`.

This proof phase adds real local proof bodies for `M1141-L-POSITIVE` and
`M1141-L-PROPAGATE`. The first derives positive, nonzero denominators on `K`.
The second defines typed finite comparison chains, proves multiplication of
symmetric comparison constants, and proves the endpoint bound `A ^ k` by
induction. The conditional ratio composition is rechecked. This does not prove
the local analytic Harnack estimate or `UniformValueComparison`, and does not
claim root or theorem completion.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no update, build, dependency clone, or fetch was run.

```text
cd Stage1_Instances/THM-M-1141
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o Statement.olean Statement.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
  exit 0
  positive_denominators_on_compact depends on axioms:
    [propext, Classical.choice, Quot.sound]
  ComparisonChain.endpoint depends on axioms:
    [propext, Classical.choice, Quot.sound]
  harnackInequality_of_analytic_package depends on axioms:
    [propext, Classical.choice, Quot.sound]
rm -f Statement.olean ObligationTree.olean

python3 Stage1_Instances/THM-M-1141/check_proof.py
  exit 0
  PASS THM-M-1141 proof phase: positivity and finite-chain propagation packages closed; analytic uniform comparison remains open

python3 Stage1_Instances/THM-M-1141/check_obligation_tree.py
  exit 0
  PASS THM-M-1141 obligation tree: 11 obligations, 67 typed edges

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1141
  exit 0; rank 346, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-1141 .stage1-worker-selftest.json
  exit 0; no output
```

No placeholder, bodyless axiom declaration, unsafe declaration, oracle, or
substituted target is present. The remaining machine cut set starts with
`M1141-L-LOCAL`, then the compact cover and connected-chain constructions and
the uniform assembly. The root remains `M3`; master acceptance is still
required.
