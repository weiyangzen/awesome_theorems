# THM-M-0771 proof-phase validation

Item: `S56-M-0771-PROOF`. Base revision:
`5314165df54baa70993fddf08cc142a9739a74e0`.

## Implemented bodies

`Proof.lean` closes the frozen `M0771-L-WELLORDER-CONSTRUCTION` obligation
with the exact pinned `IsWellOrder.subtype_nonempty` witness. It then passes
that pointwise witness to the already checked `M0771-T-UNIVERSAL` composition,
proving the exact `WellOrderingTarget` from `Statement.lean`. The declarations
have no premises and report exactly `propext`, `Classical.choice`, and
`Quot.sound`.

This is proof-phase evidence only. It establishes a kernel-elaborated body for
the frozen machine root, but does not claim theorem completion. Human-source
and readable reconstruction closure, validation and release receipts, hermetic
replay, independent verification, and master acceptance remain open.

## Commands and results

Validation ran from the worker clone on 2026-07-12 (Asia/Shanghai). Existing
canonical pinned `.lake` artifacts were reused. No dependency update, build,
clone, fetch, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0771
  exit 0: rank 780, planned, L0/rework_required, theorem_complete=false

cd Stage1_Instances/THM-M-0771
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
  -o Statement.olean Statement.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
  -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
rm -f Statement.olean ObligationTree.olean
  exit 0: both proof declarations elaborated and each reports axioms
  [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0771/check_proof.py
  exit 0: exact proof fragments, frozen input hashes, receipt, and axiom
  disclosure passed

python3 Stage1_Instances/THM-M-0771/check_statement.py
  exit 0: exact statement and all four structural mutations passed

python3 Stage1_Instances/THM-M-0771/check_obligation_tree.py
  exit 0: frozen registry and typed obligation graphs passed

git diff --check -- Stage1_Instances/THM-M-0771 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The node-specific provisional receipt is `proof-receipt.json`. Only the
integration lane can accept it. The earlier frozen obligation-tree artifacts
truthfully remain a pre-proof snapshot and were not rewritten to imply master
acceptance or downstream validation.
