# THM-M-0452 proof-phase validation

Item: `S56-M-0452-PROOF`. Base revision:
`15209c0db1b16388f976ffb2244cadfdd6f3866d`.

## Implemented proof bodies

`Proof.lean` closes the frozen `M0452-D-WELLDEFINED` and
`M0452-D-POSITIVE` branch. It proves that a supplied `PolarizationCore`
vanishes on torsion in either argument, descends it with two checked
`QuotientAddGroup.lift` applications, and proves diagonal positive
definiteness using the exact `diagonal_kernel` field. It also supplies
`quotientPairingCoreTarget_of_polarization`, so `QuotientPairingCoreTarget`
no longer needs to be an independent open construction.

The file deliberately does not construct `CanonicalHeightCore` or
`PolarizationCore`. Thus `M0452-H-LIMIT` and `M0452-P-ASSEMBLE` remain the
honest root cut, and the exact `NeronTatePairingTarget` remains unproved.

## Exact validation

Validation ran in the worker clone on 2026-07-12. It reused the canonical
pinned Lake artifacts and did not update, build, clone, or fetch dependencies.

```text
LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_DEPS=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0452
LEAN_PATH="$LEAN_DEPS" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_DEPS" "$LEAN_BIN" -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$LEAN_DEPS" "$LEAN_BIN" Proof.lean
rm -f Statement.olean ObligationTree.olean
  exit 0
  quotientPairingCoreOfPolarization depends on axioms:
    [propext, Classical.choice, Quot.sound]
  quotientPairingCoreTarget_of_polarization depends on axioms:
    [propext, Classical.choice, Quot.sound]
```

The final validation also ran the Stage1 standard and target-manifest checks,
the frozen obligation-tree checker, prohibited-token hygiene over all target
Lean files, JSON parsing of the existing structured artifacts, and scoped
`git diff --check`. Exact command outcomes are recorded in the worker
self-test receipt.

Status boundary: this proof phase supplies real kernel-elaborated bodies for
the quotient branch only. It does not alter the frozen registry or checklist,
claim accepted receipts, close the height/polarization branches, complete the
later validation/release phases, or claim theorem completion.
