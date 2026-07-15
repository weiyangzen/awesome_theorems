# THM-M-1250 proof-phase recheck at current base

Item: `S56-M-1250-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `7505614b75de56cf10bbd196a4aaa0ca2a117064`

Base tree: `730e162a2133e4a077d764043b5e722c1f7feb39`

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen target.
The already present placeholder-free declaration

```text
Stage1Instances.THM_M_1250.Counterexample.not_schwartzSpaceCharacterization :
  Not Stage1Instances.THM_M_1250.SchwartzSpaceCharacterization
```

was replayed at the current base with the pinned Lean environment and trust
level zero.

The frozen `IsSchwartzFunction` uses an unscoped order in
`ContDiff Real top`. Lean elaborates it as `top : WithTop ENat`, mathlib's
analytic order `omega`. A `SchwartzMap` supplies regularity at
`(top : ENat) : WithTop ENat`, mathlib's smooth order `infinity`. The checked
counterexample bundles a nonzero compactly supported smooth bump as a
`SchwartzMap`. The frozen equivalence would make it analytic; analytic
uniqueness and compact support then force it to be zero, contradicting its
value at the origin.

This refutes the erroneous frozen analytic encoding only, not the classical
Schwartz-space characterization at smooth order `infinity`. Replacing the
order during this proof item would substitute a different theorem. The local
`reversePackage_from_frozen_conditions` theorem remains genuine partial work,
but `M1250-F-SMOOTH`, `M1250-F-PACKAGE`, and the positive root cannot close.

The required predecessor `S56-M-1250-OBLIGATION_TREE` is also only worker-
provisional `[_]`, not master-accepted `[x]`. No positive proof receipt, state
transition, audit completion, validation, release, or theorem completion is
claimed.

## Validation

No `lake update`, `lake build`, dependency clone/fetch/checkout, network
action, or `.lake` mutation was performed. The automation-provided `.lake`
symlink was reused read-only. The required root-project `lake env lean`
interface is now usable when the local `Statement.olean` prerequisite is
compiled into a disposable directory.

The exact current-base replay was:

```bash
set -u
root=$PWD
target=$root/Stage1_Instances/THM-M-1250
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d "$lean_root/.thm-m-1250-root-proof-7505614b-slot44.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Counterexample.lean" "$tmp/Counterexample.lean"
cd "$lean_root"
LEAN_NUM_THREADS=1 timeout 300 lake env lean --root="$lean_root" \
  --trust=0 -t0 -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" timeout 300 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  "$tmp/Counterexample.lean" >"$tmp/counterexample.log" 2>&1
```

Both invocations exited `0`. The exact refutation and its analytic-support
lemma reported axioms `[propext, Classical.choice, Quot.sound]`, with no
`sorryAx`. Evidence identities were:

| Output | SHA-256 | Bytes |
|---|---|---:|
| statement log | `2f7f47d31193d167181eab4606af44bc6d2ad6f1eac751581414659b479f5faa` | 3170 |
| counterexample log | `478b93b48893d7ff76281bafdb7c20ee9464a9758d85b4081a5fc788c5d67ed4` | 365 |

The temporary `Statement.olean` was used only to satisfy the local import and
was not retained or credited as deterministic evidence; compiled-output bytes
can vary with the disposable path.

A second disposable root-project replay substituted `ProofBlocker.lean` for
`Counterexample.lean`. It also exited `0`; its 2667-byte output had SHA-256
`535657cf2f2e5daab81470ec801591ae719f488b9f2032c49ff6b69fb18d896a`.
It printed the frozen order as `omega`, the structure order as `infinity`, and
the genuine reverse-package declaration. All three diagnostic theorems
reported only `[propext, Classical.choice, Quot.sound]`.

The pinned environment was Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The untracked canonical cache
symlink and disposable outputs make this nonrelease blocker evidence.

Other exact results:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1250` | 0 | rank 430; lifecycle planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1250/check_statement.py` | 0 | frozen expression hash and four structural mutation checks passed; this confirms identity, not truth |
| `python3 Stage1_Instances/THM-M-1250/check_anchor_audit.py` | 0 | immutable mathlib pin and source candidates matched; positive root remains open |
| `python3 Stage1_Instances/THM-M-1250/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed structurally; denominator `24c4c3e8...98bca`; root remains open M3 |
| prohibited-construct scan over owned Lean files | 1, expected | no prohibited proof escape matched |
| `git diff --check -- Stage1_Instances/THM-M-1250` | 0 | no scoped whitespace errors |
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
