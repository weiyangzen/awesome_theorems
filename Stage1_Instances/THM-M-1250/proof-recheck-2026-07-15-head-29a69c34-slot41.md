# THM-M-1250 proof-phase recheck at current base

Item: `S56-M-1250-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `29a69c34f06bf3444399287853ea7806767d0944`

Base tree: `de0efce35b6fcc6f851b9c2e643d61ec49d831e0`

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen target.
The existing placeholder-free declaration

```text
Stage1Instances.THM_M_1250.Counterexample.not_schwartzSpaceCharacterization :
  Not Stage1Instances.THM_M_1250.SchwartzSpaceCharacterization
```

was replayed at the current base with pinned Lean and trust level zero.

The frozen `IsSchwartzFunction` uses `ContDiff Real top` without fixing the
order type. Lean elaborates that `top` as `top : WithTop ENat`, mathlib's
analytic order `omega`. A `SchwartzMap` supplies regularity at
`(top : ENat) : WithTop ENat`, mathlib's smooth order `infinity`. The checked
counterexample bundles a nonzero compactly supported smooth bump as a
`SchwartzMap`. The frozen equivalence would make it analytic; analytic
uniqueness and compact support then force it to be zero, contradicting its
value at the origin.

This refutes only the erroneous frozen analytic encoding, not the classical
Schwartz-space characterization at smooth order `infinity`. Changing the
order during this proof item would substitute a different theorem. The
existing `reversePackage_from_frozen_conditions` theorem is valid partial
work, but `M1250-F-SMOOTH`, `M1250-F-PACKAGE`, and the positive root cannot
close.

The required predecessor `S56-M-1250-OBLIGATION_TREE` is also only worker-
provisional `[_]`, not master-accepted `[x]`. No proof receipt, state
transition, audit completion, validation, release, or theorem completion is
claimed.

## Validation

No `lake update`, `lake build`, dependency clone/fetch/checkout, network
action, or `.lake` mutation was performed. The automation-provided canonical
`.lake` symlink was reused read-only. Fresh copies of the three Lean modules
were compiled in a disposable directory, which was removed afterward:

```bash
set -u
root=$PWD
target=$root/Stage1_Instances/THM-M-1250
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d "$lean_root/.thm-m-1250-root-proof-29a69c34-slot41.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Counterexample.lean" "$tmp/Counterexample.lean"
cp "$target/ProofBlocker.lean" "$tmp/ProofBlocker.lean"
cd "$lean_root"
LEAN_NUM_THREADS=1 timeout 300 lake env lean --root="$lean_root" \
  --trust=0 -t0 -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" timeout 300 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  "$tmp/Counterexample.lean" >"$tmp/counterexample.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" timeout 300 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  "$tmp/ProofBlocker.lean" >"$tmp/proofblocker.log" 2>&1
```

All three invocations exited `0`. The exact target negation, analytic-support
lemma, order witnesses, and reverse-package theorem reported only
`[propext, Classical.choice, Quot.sound]`, with no `sorryAx`. The logs were:

| Output | SHA-256 | Bytes |
|---|---|---:|
| statement | `2f7f47d31193d167181eab4606af44bc6d2ad6f1eac751581414659b479f5faa` | 3170 |
| counterexample | `478b93b48893d7ff76281bafdb7c20ee9464a9758d85b4081a5fc788c5d67ed4` | 365 |
| proof blocker | `535657cf2f2e5daab81470ec801591ae719f488b9f2032c49ff6b69fb18d896a` | 2667 |

The pinned environment was Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The untracked cache symlink and
disposable outputs make this current negative evidence nonrelease.

Other exact results:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1250` | 0 | rank 430; lifecycle planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1250/check_statement.py` | 0 | frozen expression hash and four structural mutations passed; this confirms identity, not truth |
| `python3 Stage1_Instances/THM-M-1250/check_anchor_audit.py` | 0 | immutable mathlib pin/worktree/source candidates matched; positive root remains open |
| `python3 Stage1_Instances/THM-M-1250/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; denominator `24c4c3e8...98bca`; root remains open M3 |
| prohibited-construct scan over owned Lean files | 1, expected | no prohibited proof escape matched |
| blocker JSON/source-hash/invariant checks and `git diff --check` | 0 | structured evidence parsed, hashes and blocked/no-selftest invariants passed, and both new files had no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is deliberately absent |

## Retry condition

Reopen `S56-M-1250-STATEMENT`, replace the ambiguous order by the intended
`((top : ENat) : WithTop ENat)`, and rerun expression identity, mutation,
anchor-audit, and versioned obligation-registry/typed-graph gates. Those
invalidated prerequisites must receive master acceptance before another proof
attempt. The remaining workflow cut set is `S56-M-1250-STATEMENT`.

Because this positive proof phase is blocked rather than self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent and this item remains
`[ ]`.
