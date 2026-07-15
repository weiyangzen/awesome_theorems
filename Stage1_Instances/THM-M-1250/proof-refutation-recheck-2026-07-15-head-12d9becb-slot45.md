# THM-M-1250 proof-phase refutation recheck at `12d9becb` (slot45)

Item: `S56-M-1250-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `12d9becb170c3ef83e7aed51d1b3eed2a1940379`

Base tree: `6e6e70064d410f5e13419c450a6383278f17ed44`

## Verdict

`blocked`. A positive Lean proof cannot inhabit the exact frozen target. The
tracked, placeholder-free declaration

```text
Stage1Instances.THM_M_1250.Counterexample.not_schwartzSpaceCharacterization :
  Not Stage1Instances.THM_M_1250.SchwartzSpaceCharacterization
```

was replayed at trust level zero. The proof-phase certificate

```text
Stage1Instances.THM_M_1250.not_refutedForwardPackage :
  Not Stage1Instances.THM_M_1250.RefutedForwardPackage
```

was also replayed. `RefutedForwardPackage` duplicates the exact proposition
spelled by the registry's `ForwardPackage`; because it does not import that
declaration or publish an accepted registry delta, this check supplies a
negative certificate but no positive proof or registry-closure credit.

`Statement.lean` writes `ContDiff Real top f` without fixing the order type.
Lean elaborates it as `top : WithTop ENat`, mathlib's analytic order `omega`.
A `SchwartzMap` supplies regularity at
`(top : ENat) : WithTop ENat`, mathlib's smooth order `infinity`. The checked
counterexample bundles a nonzero compactly supported smooth bump as a
`SchwartzMap`. The frozen equivalence would make it analytic; analytic
uniqueness and compact support then force it to be zero, contradicting its
value at the origin.

Pinned mathlib corroborates every boundary: `ContDiff/Defs.lean` lines 90-92
distinguish `infinity` from `omega`, lines 1159-1167 identify `ContDiff omega`
with analytic regularity, `SchwartzSpace/Basic.lean` lines 72-78 define
`SchwartzMap.smooth'` at order `infinity`, and
`Analytic/Uniqueness.lean` lines 230-237 provide the identity principle.

This refutes only the erroneous frozen analytic encoding, not the classical
Schwartz-space characterization at smooth order `infinity`. Replacing the
order during this proof item would substitute a different theorem. The local
`reversePackage_from_frozen_conditions` theorem remains genuine progress, but
the version-1 registry has no delta or accepted receipt closing
`M1250-R-PACKAGE`. Its authoritative root cut therefore remains both
`M1250-F-PACKAGE` and `M1250-R-PACKAGE`. The checked
`M1250-T-ASSEMBLE` theorem remains valid conditional composition; it is not
itself refuted.

The required predecessor `S56-M-1250-OBLIGATION_TREE` is only worker-
provisional `[_]`, not master-accepted `[x]`. This independently prevents
proof-item acceptance. The assigned item stays `[ ]`, and no proof receipt,
state transition, audit completion, validation, release, or theorem
completion is claimed.

## Validation

No `lake update`, `lake build`, dependency clone/fetch/checkout, network
action, or `.lake` mutation was performed. The automation-provided `.lake`
symlink was reused read-only. All Lean outputs were created below
`Formalizations/Lean` in disposable directories and removed after each run.

The trust-zero replay recipe was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1250
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d "$lean_root/.thm-m-1250-proof-12d9becb-slot45.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
for f in Statement Counterexample ProofBlocker ProofRefutation; do
  cp "$target/$f.lean" "$tmp/$f.lean"
done
cd "$lean_root"
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.log" 2>&1
for f in ProofBlocker Counterexample; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" \
    timeout --foreground --kill-after=5s 600 \
    lake env lean --root="$lean_root" --trust=0 -t0 \
    -o "$tmp/$f.olean" "$tmp/$f.lean" \
    >"$tmp/${f,,}.log" 2>&1
done
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" \
  timeout --foreground --kill-after=5s 600 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  "$tmp/ProofRefutation.lean" >"$tmp/proofrefutation.log" 2>&1
```

All four invocations exited `0`. The exact target negation and forward-package
impossibility certificate reported only
`[propext, Classical.choice, Quot.sound]`, with no `sorryAx`.

| Output | SHA-256 | Bytes |
|---|---|---:|
| statement log | `2f7f47d31193d167181eab4606af44bc6d2ad6f1eac751581414659b479f5faa` | 3170 |
| proof-blocker log | `535657cf2f2e5daab81470ec801591ae719f488b9f2032c49ff6b69fb18d896a` | 2667 |
| countertheorem log | `478b93b48893d7ff76281bafdb7c20ee9464a9758d85b4081a5fc788c5d67ed4` | 365 |
| proof-refutation log | `2ccc1339ca05d191d6900b175614d156b57e2176e11c09f05194452434eeb175` | 220 |

The pinned environment was Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The Lean executable hash was
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.
The untracked cache symlink and disposable outputs make this negative evidence
nonrelease.

Other exact results:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1250` | 0 | rank 430; lifecycle planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1250/check_statement.py` | 0 | frozen expression hash and four structural mutations passed; identity only, not truth |
| `python3 Stage1_Instances/THM-M-1250/check_anchor_audit.py` | 0 | immutable mathlib pin/worktree/source candidates matched; positive root remains open |
| `python3 Stage1_Instances/THM-M-1250/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; denominator `24c4c3e8...98bca`; root remains open M3 |
| prohibited-construct scan over the four credited Lean files | 1, expected | no prohibited proof escape matched |
| JSON, base/hash/invariant, and changed-file whitespace checks | 0 | current-base blocked evidence and no-selftest invariants passed |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent |

There were 18 pre-existing ordinary proof-recheck JSON records and one
pre-existing refutation-recheck JSON record. File count is not scheduler-tick
evidence. The authoritative DAG still records proof attempts as zero, so the
master must reconcile actual ticks and apply the five-unresolved-tick split or
redirect rule when warranted.

## Retry Condition

Reopen `S56-M-1250-STATEMENT`, replace the ambiguous order by the intended
`((top : ENat) : WithTop ENat)`, and rerun expression identity, mutation,
anchor-audit, and versioned obligation-registry/typed-graph gates. All
invalidated prerequisites must receive dependency-ordered master acceptance
before another positive proof attempt. Alternatively, explicitly redirect the
work to a checked counterexample or barrier target.

Because this positive proof phase is blocked rather than self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent and this item remains
`[ ]`.
