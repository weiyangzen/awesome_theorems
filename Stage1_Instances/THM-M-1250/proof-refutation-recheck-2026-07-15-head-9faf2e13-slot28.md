# THM-M-1250 proof-phase refutation recheck at `9faf2e13` (slot28)

Item: `S56-M-1250-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `9faf2e13566ce7ad1047f54337157387eaed48bf`

Base tree: `438505eefd23e6c86d2100b87e98212be6fd8675`

## Verdict

`blocked`. A positive proof body cannot inhabit the exact frozen target. The
tracked, placeholder-free declaration

```text
Stage1Instances.THM_M_1250.Counterexample.not_schwartzSpaceCharacterization :
  Not Stage1Instances.THM_M_1250.SchwartzSpaceCharacterization
```

was freshly replayed at trust level zero. The proof-phase certificate

```text
Stage1Instances.THM_M_1250.not_refutedForwardPackage :
  Not Stage1Instances.THM_M_1250.RefutedForwardPackage
```

was replayed as well. `RefutedForwardPackage` is the same proposition as the
registry's `ForwardPackage`, but it is locally restated rather than treated as
an accepted registry update. The certificate is negative evidence only; it
does not close a positive obligation.

The source of the contradiction is the frozen statement. `Statement.lean`
uses `ContDiff Real top f` without fixing the order type, so Lean elaborates
`top` as `top : WithTop ENat`, mathlib's analytic order `omega`. A
`SchwartzMap` supplies regularity at
`(top : ENat) : WithTop ENat`, mathlib's smooth order `infinity`. The checked
counterexample bundles a nonzero compactly supported smooth bump as a
`SchwartzMap`; the frozen equivalence would make it analytic, and analytic
uniqueness plus compact support would then make it zero, contradicting its
value at the origin.

This refutes only the erroneous analytic encoding, not the classical
Schwartz-space characterization at smooth order `infinity`. Correcting the
order in this proof item would substitute a different theorem. The local
`reversePackage_from_frozen_conditions` proof remains genuine partial work,
but no append-only registry delta or accepted receipt closes
`M1250-R-PACKAGE`. The authoritative root cut remains
`M1250-F-PACKAGE` and `M1250-R-PACKAGE`.

The required predecessor `S56-M-1250-OBLIGATION_TREE` is only worker-
provisional `[_]`, not master-accepted `[x]`. This independently prevents
proof-item acceptance. The assigned item stays `[ ]`; no proof receipt, state
transition, audit completion, validation, release, or theorem completion is
claimed.

## Validation

No `lake update`, `lake build`, dependency clone/fetch/checkout, network
action, or `.lake` mutation was performed. The automation-provided `.lake`
symlink was reused read-only. Lean outputs were produced in a fresh disposable
directory below `Formalizations/Lean` and removed after the replay.

The trust-zero recipe was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1250
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d "$lean_root/.thm-m-1250-proof-9faf2e13-slot28.XXXXXX")
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
  lower=$(printf '%s' "$f" | tr '[:upper:]' '[:lower:]')
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" \
    timeout --foreground --kill-after=5s 600 \
    lake env lean --root="$lean_root" --trust=0 -t0 \
    -o "$tmp/$f.olean" "$tmp/$f.lean" \
    >"$tmp/$lower.log" 2>&1
done
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" \
  timeout --foreground --kill-after=5s 600 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  "$tmp/ProofRefutation.lean" >"$tmp/proofrefutation.log" 2>&1
```

All four Lean invocations exited `0`. The exact target negation, order
witnesses, reverse package, and forward-package impossibility certificate
reported only `[propext, Classical.choice, Quot.sound]`, with no `sorryAx`.

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
The untracked automation cache symlink makes this negative evidence
nonrelease.

Other exact results:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1250` | 0 | rank 430; lifecycle planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1250/check_statement.py` | 0 | expression hash and four structural mutations passed; identity only, not truth |
| `python3 Stage1_Instances/THM-M-1250/check_anchor_audit.py` | 0 | immutable pin/worktree/source candidates matched; positive root remains open |
| `python3 Stage1_Instances/THM-M-1250/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; denominator `24c4c3e8...98bca`; root remains open M3 |
| prohibited-construct scan over the owned Lean sources | 1, expected | no prohibited proof escape matched |

There were 18 ordinary proof-recheck JSON records and two refutation-recheck
JSON records before this run. Record count is not scheduler-tick evidence; the
authoritative DAG still records attempts as zero. The master must reconcile
actual execution ticks and apply the five-unresolved-tick split or redirect
rule when warranted.

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
