# THM-M-1250 proof-phase refutation recheck at `aef94f39` (slot26)

Item: `S56-M-1250-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `aef94f39853f9222e48f83b2358a6822aafd3c50`

Base tree: `8c42e198fdbcc36b0f5cc0f865e0961715a35c17`

## Verdict

`blocked`. No positive Lean proof can inhabit the exact frozen proposition.
The existing placeholder-free declaration

```text
Stage1Instances.THM_M_1250.Counterexample.not_schwartzSpaceCharacterization :
  Not Stage1Instances.THM_M_1250.SchwartzSpaceCharacterization
```

was replayed at trust level zero on this base. The proof-phase certificate

```text
Stage1Instances.THM_M_1250.not_refutedForwardPackage :
  Not Stage1Instances.THM_M_1250.RefutedForwardPackage
```

was replayed as well. `RefutedForwardPackage` has the exact proposition written
by the registry's `ForwardPackage`; it remains a local diagnostic duplicate,
not a registry-closing import or an accepted registry delta.

`Statement.lean` writes `ContDiff Real top f` without fixing the order type.
Lean elaborates it as `top : WithTop ENat`, mathlib's analytic order `omega`.
A `SchwartzMap` supplies regularity at
`(top : ENat) : WithTop ENat`, mathlib's smooth order `infinity`. The checked
counterexample bundles a nonzero compactly supported smooth bump as a
`SchwartzMap`. The frozen equivalence would make it analytic; analytic
uniqueness plus compact support then forces it to be zero, contradicting its
value at the origin.

This refutes only the erroneous frozen analytic encoding, not the classical
Schwartz-space characterization at smooth order `infinity`. Repairing the
order inside this proof item would substitute a different theorem, which the
rev-5.6 proof gate forbids. The local
`reversePackage_from_frozen_conditions` declaration is genuine partial
progress, but the frozen registry contains no accepted delta that closes
`M1250-R-PACKAGE`. The root cut remains `M1250-F-PACKAGE` and
`M1250-R-PACKAGE`; `M1250-T-ASSEMBLE` remains only conditional composition.

The required predecessor `S56-M-1250-OBLIGATION_TREE` is worker-provisional
`[_]`, not master-accepted `[x]`. This independently blocks proof-item
acceptance. The item therefore stays `[ ]`; no proof receipt, state transition,
audit completion, validation/release result, or theorem completion is claimed.

## Validation

No `lake update`, `lake build`, dependency clone/fetch/checkout, network action,
or `.lake` mutation was performed. The automation-provided `.lake` symlink was
reused read-only. Lean outputs lived in a disposable directory under
`Formalizations/Lean` and were deleted on exit.

The narrow trust-zero replay was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1250
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d "$lean_root/.thm-m-1250-proof-aef94f39-slot26.XXXXXX")
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

The replay ran from `2026-07-15T20:21:21+08:00` through
`2026-07-15T20:22:26+08:00`. All four invocations exited `0`. The exact target
negation and forward-package impossibility certificate reported only
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
The automation-provided untracked cache symlink makes this negative evidence
nonrelease.

Other exact results:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1250` | 0 | rank 430; lifecycle planned; theorem incomplete |
| `timeout --foreground --kill-after=5s 300 python3 Stage1_Instances/THM-M-1250/check_statement.py` | 0 | frozen expression hash and four structural mutations passed; identity only, not truth |
| `python3 Stage1_Instances/THM-M-1250/check_anchor_audit.py` | 0 | immutable mathlib pin/worktree/source candidates matched; positive root remains open |
| `python3 Stage1_Instances/THM-M-1250/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; denominator `24c4c3e8...98bca`; root remains open M3 |
| prohibited-construct scan over the four credited Lean files | 1, expected | no prohibited proof escape matched |

## Retry Condition

Reopen `S56-M-1250-STATEMENT`, replace the ambiguous order by the intended
`((top : ENat) : WithTop ENat)`, and publish fresh expression, mutation,
anchor-audit, obligation-registry, and typed-graph artifacts. Every invalidated
prerequisite must then receive dependency-ordered master acceptance before a
new positive proof attempt. Alternatively, explicitly redirect the target to
a checked counterexample or barrier theorem.

Because this proof phase is blocked rather than self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent and this item remains
`[ ]`.
