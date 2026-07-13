# THM-M-1553 proof-phase validation

Item: `S56-M-1553-PROOF`. Base revision:
`bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`.

## Implemented proof

`ProofLemmas.lean` proves the required multivariable regularity, mixed-partial
commutation, exact Hirota-sum expansions, and logarithm/exponential derivative
identities through the orders used by the target. `Proof.lean` then normalizes
the bilinear equation, for `L = log tau`, to

```text
L_xxxx + 6 * L_xx^2 + L_xt = 0.
```

Positivity supplies `tau = exp L` and justifies cancelling `exp(L)^2`.
Differentiating the normalized identity in `x` gives

```text
L_xxxxx + 12 * L_xx * L_xxx + L_xxt = 0,
```

which is exactly half the KdV residual of `u = 2 * L_xx`. The checked
composition declaration `hirotaKdVTarget_proof` has the literal frozen type
`HirotaKdVTarget`; there is no added premise, weakened hypothesis, changed
sign, omitted Hirota term, or soliton-family substitution.

## Commands and results

Validation ran in the worker clone on 2026-07-14 (Asia/Shanghai). Existing
canonical pinned Lake artifacts were reused through the automation-provided
symlink. No `lake update`, `lake build`, dependency fetch, clone, or `.lake`
mutation was run.

```text
bash Stage1_Instances/THM-M-1553/check_proof.sh
  exit 0
  Declarations are sorry-free! (three declarations)
  logarithmic_bilinear_identity axioms: [propext, Classical.choice, Quot.sound]
  logDerivativeBridge axioms: [propext, Classical.choice, Quot.sound]
  hirotaKdVTarget_proof axioms: [propext, Classical.choice, Quot.sound]
  PASS exact frozen machine root has a local body

python3 Stage1_Instances/THM-M-1553/check_obligation_tree.py
  exit 0: 14 frozen obligations and typed edges passed; the freeze artifact
  retains its truthful pre-proof open boundary pending master reconciliation

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1553
  exit 0: rank 212, planned, theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-1553/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both JSON documents parsed

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1553-proof-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1553/check_proof.py
  exit 0: checker syntax compiled outside the repository

rg prohibited proof devices in Proof.lean and ProofLemmas.lean
  exit 1 with empty output: expected no-match pass

git diff --check -- Stage1_Instances/THM-M-1553 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

This is proof-phase worker evidence only. The node-specific provisional
receipt is `proof-receipt.json`. Master acceptance, source/readability closure,
validation, hermetic and independent replay, release, and theorem completion
remain separate open gates.
