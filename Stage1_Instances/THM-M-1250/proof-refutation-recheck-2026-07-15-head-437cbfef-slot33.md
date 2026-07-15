# THM-M-1250 proof-phase refutation recheck at `437cbfef` (slot33)

Item: `S56-M-1250-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `437cbfefc5829160dcb65d52dbe3c5458b187f3b`

Base tree: `849d1bfa7781d20a7428a64349372f2f43d94d2b`

## Verdict

`blocked`. No placeholder-free positive proof can inhabit the exact frozen
target. The tracked declaration

```text
Stage1Instances.THM_M_1250.Counterexample.not_schwartzSpaceCharacterization :
  Not Stage1Instances.THM_M_1250.SchwartzSpaceCharacterization
```

was freshly replayed at trust level zero. The proof-phase certificate

```text
Stage1Instances.THM_M_1250.not_refutedForwardPackage :
  Not Stage1Instances.THM_M_1250.RefutedForwardPackage
```

was replayed as well. It shows that the exact forward interface needed by the
frozen architecture cannot be supplied. Because `RefutedForwardPackage` is a
local duplicate rather than an imported registry declaration, the certificate
is negative evidence only and supplies no registry-closure credit.

In `Statement.lean`, the unscoped order in `ContDiff Real top f` elaborates as
`top : WithTop ENat`, mathlib's analytic order `omega`. A `SchwartzMap` instead
stores regularity at `(top : ENat) : WithTop ENat`, the smooth order
`infinity`. The counterexample bundles a nonzero compactly supported smooth
bump as a `SchwartzMap`. The frozen equivalence would make that bump analytic;
analytic uniqueness and compact support force it to be zero, contradicting its
value at the origin.

This refutes only the erroneous frozen analytic encoding, not the classical
Schwartz-space characterization. Replacing the order during this proof item
would substitute a differently typed theorem. The local theorem
`reversePackage_from_frozen_conditions` remains genuine partial progress, but
the authoritative registry has no accepted delta closing `M1250-R-PACKAGE`.
`M1250-T-ASSEMBLE` remains valid conditional composition.

The required predecessor `S56-M-1250-OBLIGATION_TREE` is only worker-
provisional `[_]`, not master-accepted `[x]`. This independently prevents
proof-item acceptance. The item therefore remains `[ ]`, and no proof receipt,
state transition, audit completion, validation result, release result, or
theorem completion is claimed.

## Validation

No `lake update`, `lake build`, dependency clone/fetch/checkout, network
action, or `.lake` mutation was performed. The automation-provided `.lake`
symlink was reused read-only. Lean outputs lived in a disposable directory
under `Formalizations/Lean` and were removed after replay.

The exact trust-zero recipe was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1250
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d "$lean_root/.thm-m-1250-proof-437cbfef-slot33.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
for f in Statement ProofBlocker Counterexample ProofRefutation; do
  cp "$target/$f.lean" "$tmp/$f.lean"
done
cd "$lean_root"
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" \
  timeout --foreground --kill-after=5s 600 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  -o "$tmp/ProofBlocker.olean" "$tmp/ProofBlocker.lean" \
  >"$tmp/proofblocker.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" \
  timeout --foreground --kill-after=5s 600 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  -o "$tmp/Counterexample.olean" "$tmp/Counterexample.lean" \
  >"$tmp/counterexample.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" \
  timeout --foreground --kill-after=5s 600 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  "$tmp/ProofRefutation.lean" >"$tmp/proofrefutation.log" 2>&1
```

All four invocations exited `0`. Both negations reported only
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
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The invoked Lean executable
SHA-256 was
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.
The untracked cache symlink makes this negative evidence nonrelease.

Other exact results:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1250` | 0 | rank 430; lifecycle planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1250/check_statement.py` | 0 | frozen expression hash and four structural mutations passed; identity only, not truth |
| `python3 Stage1_Instances/THM-M-1250/check_anchor_audit.py` | 0 | pinned mathlib candidates matched; positive root remains open |
| `python3 Stage1_Instances/THM-M-1250/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; root remains open M3 |
| prohibited-construct scan over owned Lean files | 1, expected | no prohibited proof escape matched |

There were 18 pre-existing ordinary proof-recheck JSON records and five
pre-existing refutation-recheck JSON records before this report. File count is not scheduler-tick
evidence. The authoritative DAG still records proof attempts as zero, so the
master must reconcile actual ticks and apply the five-unresolved-tick split or
redirect rule when warranted.

## Retry Condition

Do not retry this unchanged positive proof item. Reopen
`S56-M-1250-STATEMENT`, replace the ambiguous order with the intended
`((top : ENat) : WithTop ENat)`, and rerun expression identity, mutation,
anchor-audit, and versioned obligation-registry/typed-graph gates. All
invalidated prerequisites must then receive dependency-ordered master
acceptance before another positive proof attempt. Alternatively, the master
may explicitly redirect the work to a checked counterexample or barrier
target.

Because this proof phase is blocked rather than self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
