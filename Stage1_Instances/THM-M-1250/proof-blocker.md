# THM-M-1250 proof-phase blocker

Item: `S56-M-1250-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `8c045f3d21e3e747c39dd266f581367b08bddd8b`

## First failed gate

The exact frozen statement cannot be discharged by the frozen
`SchwartzMap.smooth'` projection route. In `Statement.lean`, the unscoped
expression

```lean
ContDiff Real top f
```

elaborates at order `top : WithTop ENat`. The mathlib structure field instead
has order `up (top : ENat) : WithTop ENat`. These are different orders: the
frozen target asks for the strictly stronger analytic regularity condition,
whereas a Schwartz map is defined to be smooth to every finite order.

The attempted exact forward body failed with:

```text
Application type mismatch: phi.smooth' has type
  ContDiff Real (up top) phi.toFun
but is expected to have type
  ContDiff Real top phi
```

The reverse mismatch goes in the usable direction. `ProofBlocker.lean`
contains the genuine unconditional theorem
`reversePackage_from_frozen_conditions`, which weakens the stronger frozen
smoothness premise with `ContDiff.of_le` and constructs the bundled map. It
also freezes both smoothness propositions explicitly in
`FrozenSmoothnessMismatch`. No forward package or canonical root is asserted.

## Retry condition

Return the target to the statement phase and replace the ambiguous order by
the intended explicit order
`(↑(⊤ : ENat) : WithTop ENat)` (equivalently the correctly scoped
`C^infinity` notation), then rerun statement fingerprinting, mutation tests,
anchor audit, and obligation-tree freeze before proof execution. That is a
statement change and is outside this proof worker's ownership of the assigned
phase; silently making it here would substitute a different theorem.

## Validation

All commands ran in the worker clone. The pinned canonical `.lake` symlink was
reused without update, build, fetch, clone, network access, or mutation.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1250
  exit 0: rank 430, planned, theorem_complete=false

Disposable trust-zero compilation of Statement.lean and ProofBlocker.lean
with the pinned Lean executable and Lake-derived
LEAN_PATH
  exit 0: the explicit mismatch probe and reverse-package theorem elaborated;
  reversePackage_from_frozen_conditions reported only propext,
  Classical.choice, and Quot.sound

Disposable trust-zero compilation of the exact attempted forward and reverse
field proof
  exit 1: both ContDiff order mismatches above were reported; generated
  declarations contained sorryAx and therefore received no proof credit

python3 Stage1_Instances/THM-M-1250/check_obligation_tree.py
  exit 0: frozen 15-obligation/30-edge architecture remains structurally valid
  and its forward/reverse root cut remains open

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe|opaque)[[:space:]]' \
  Stage1_Instances/THM-M-1250/ProofBlocker.lean
  exit 1 with empty output: no prohibited proof device

git diff --check -- Stage1_Instances/THM-M-1250
  exit 0: no whitespace errors
```

## Status boundary

Verdict: `blocked`. No self-test manifest or node-specific proof receipt is
emitted because the assigned proof phase is not genuinely self-tested as
complete. The reverse package is local progress only; `M1250-F-PACKAGE` and
the exact root remain open. Accepted state, audit completion, theorem
completion, validation, release, and master acceptance are unchanged.
