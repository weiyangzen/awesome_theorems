# THM-M-1250 proof-phase refutation recheck at `4c1d50aa` (slot44)

Item: `S56-M-1250-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `4c1d50aa6552eb6ec56338a663a5dff79a4ae2e3`

Base tree: `e38ee217e0bb768c5c915905d1d0b04fc89e25f2`

## Verdict

`blocked`. No positive Lean proof can inhabit the exact frozen target. The
tracked, placeholder-free declaration

```text
Stage1Instances.THM_M_1250.Counterexample.not_schwartzSpaceCharacterization :
  Not Stage1Instances.THM_M_1250.SchwartzSpaceCharacterization
```

was replayed at trust level zero. This proof-phase run also adds the checked
certificate

```text
Stage1Instances.THM_M_1250.not_refutedForwardPackage :
  Not Stage1Instances.THM_M_1250.RefutedForwardPackage
```

where `RefutedForwardPackage` is the exact proposition spelled by the frozen
registry's `M1250-F-PACKAGE` interface. The certificate composes any assumed
forward package with the already checked reverse package, obtains the exact
canonical characterization, and contradicts the countertheorem. It has no
placeholder and reports only `propext`, `Classical.choice`, and `Quot.sound`.

The frozen `IsSchwartzFunction` uses an unscoped order in
`ContDiff Real top`. Lean elaborates it as `top : WithTop ENat`, mathlib's
analytic order `omega`. A `SchwartzMap` supplies regularity at
`(top : ENat) : WithTop ENat`, mathlib's smooth order `infinity`. The checked
counterexample bundles a nonzero compactly supported smooth bump as a
`SchwartzMap`. The frozen equivalence would make it analytic; analytic
uniqueness and compact support then force it to be zero, contradicting its
value at the origin.

This refutes only the erroneous frozen analytic encoding, not the classical
Schwartz-space characterization at smooth order `infinity`. Replacing the
order during this proof item would substitute a different theorem. The local
`reversePackage_from_frozen_conditions` theorem remains genuine partial work,
but `M1250-F-SMOOTH`, `M1250-F-PACKAGE`, and the positive root cannot close.

The required predecessor `S56-M-1250-OBLIGATION_TREE` is also only worker-
provisional `[_]`, not master-accepted `[x]`. The assigned proof item therefore
remains `[ ]`. No positive proof receipt, state transition, audit completion,
validation, release, or theorem completion is claimed.

## Validation

No `lake update`, `lake build`, dependency clone/fetch/checkout, network
action, or `.lake` mutation was performed. The automation-provided `.lake`
symlink was reused read-only. Lean outputs were created in a disposable
directory below `Formalizations/Lean` and removed after the check.

The exact trust-zero replay was:

```bash
set -u
root=$PWD
target=$root/Stage1_Instances/THM-M-1250
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d "$lean_root/.thm-m-1250-proof-refutation-4c1d50aa-slot44.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
for f in Statement.lean ProofBlocker.lean Counterexample.lean ProofRefutation.lean; do
  cp "$target/$f" "$tmp/$f"
done
cd "$lean_root"
LEAN_NUM_THREADS=1 timeout 300 lake env lean --root="$lean_root" \
  --trust=0 -t0 -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" timeout 300 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  -o "$tmp/ProofBlocker.olean" "$tmp/ProofBlocker.lean" \
  >"$tmp/proofblocker.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" timeout 300 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  -o "$tmp/Counterexample.olean" "$tmp/Counterexample.lean" \
  >"$tmp/counterexample.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" timeout 300 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  "$tmp/ProofRefutation.lean" >"$tmp/refutation.log" 2>&1
```

All four invocations exited `0`. Evidence identities were:

| Output | SHA-256 | Bytes |
|---|---|---:|
| statement log | `2f7f47d31193d167181eab4606af44bc6d2ad6f1eac751581414659b479f5faa` | 3170 |
| proof-blocker log | `535657cf2f2e5daab81470ec801591ae719f488b9f2032c49ff6b69fb18d896a` | 2667 |
| countertheorem log | `478b93b48893d7ff76281bafdb7c20ee9464a9758d85b4081a5fc788c5d67ed4` | 365 |
| proof-refutation log | `2ccc1339ca05d191d6900b175614d156b57e2176e11c09f05194452434eeb175` | 220 |

The pinned environment was Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`).

Other exact results:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1250` | 0 | rank 430; lifecycle planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1250/check_statement.py` | 0 | frozen expression hash and four structural mutation checks passed; identity only, not truth |
| `python3 Stage1_Instances/THM-M-1250/check_anchor_audit.py` | 0 | immutable pin and source candidates matched; positive root remains open |
| `python3 Stage1_Instances/THM-M-1250/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; root remains open M3 |
| prohibited-construct scan over owned Lean files | 1, expected | no prohibited proof escape matched |

`ProofRefutation.lean` has SHA-256
`a5705c64924d8599e0783382650f96d8e262bd78f512bb80b813249a0b0a0272`.
The structural registry denominator remains
`24c4c3e89df76e28bfa658401de1edd90d5000ad1897f89d2495a071bb098bca`.

There were 18 pre-existing `proof-recheck-*.json` records. File count is not
scheduler-tick evidence; the master must reconcile actual ticks and apply the
five-unresolved-tick split rule. The authoritative DAG still records attempts
as zero.

## Retry Condition

Reopen `S56-M-1250-STATEMENT`, replace the ambiguous order by the intended
`((top : ENat) : WithTop ENat)`, and rerun expression identity, mutation,
anchor-audit, and versioned obligation-registry/typed-graph gates. Those
invalidated prerequisites must receive master acceptance before another
positive proof attempt. Alternatively, the master may explicitly redirect to
a checked counterexample/barrier target. The remaining workflow cut set is
`S56-M-1250-STATEMENT`.

Because this positive proof phase is blocked rather than self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
