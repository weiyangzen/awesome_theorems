# THM-M-1250 proof-phase recheck at current base

Item: `S56-M-1250-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `ab6974ae3bcabe677e7138ff057a7c005aac12d4`

Base tree: `c640af240d44f02c83a29dfa2f985f601a0dfcc2`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen
target. The already integrated, placeholder-free declaration

```text
Stage1Instances.THM_M_1250.Counterexample.not_schwartzSpaceCharacterization :
  Not Stage1Instances.THM_M_1250.SchwartzSpaceCharacterization
```

was replayed against the current pinned Lean closure at trust level zero.
`Statement.lean` writes `ContDiff Real top f` without fixing the order type,
so `top` elaborates as the analytic order `omega : WithTop ENat`. A
`SchwartzMap` supplies only the infinitely differentiable order
`infinity = (top : ENat)` coerced into `WithTop ENat`.

The countertheorem constructs a nonzero compactly supported smooth function
on `Fin 1 -> Real`, maps it into `Complex`, and bundles it as a
`SchwartzMap`. The frozen characterization would make this function analytic.
Analytic uniqueness and compact support would then force it to be zero,
contradicting its value at the origin.

This refutes only the erroneous frozen analytic encoding, not the classical
Schwartz-space characterization at smooth order `infinity`. Changing the
order during this proof item would substitute a different theorem. The
existing reverse-package implementation is valid partial work, but the
positive forward package and root remain impossible.

The required predecessor `S56-M-1250-OBLIGATION_TREE` is only worker-
provisional `[_]`, not master-accepted `[x]`. Independently, its positive
route is semantically invalidated at `M1250-F-SMOOTH`. No positive proof body,
proof receipt, state transition, audit completion, validation, release, or
theorem completion is claimed.

## Validation

No `lake update`, `lake build`, dependency clone/fetch/checkout, network
action, or `.lake` mutation was performed. The automation-provided `.lake`
symlink was reused read-only.

The required root-project interface was attempted first:

```text
cd Formalizations/Lean &&
timeout 300 lake env lean --trust=0 \
  ../../Stage1_Instances/THM-M-1250/Counterexample.lean
```

It did not reach Lean output and was manually interrupted after more than 120
seconds. A separate read-only `git rev-parse HEAD` probe in the pre-existing
`flt-regular` package checkout exited nonzero with `unknown revision`, so the
root Lake environment cannot complete dependency configuration. This is an
environment blocker, not proof evidence, and the cache was left untouched.

The smallest available real check used `lake env lean` from the intact pinned
mathlib subproject. `LEAN_PATH` was assembled read-only from the eight existing
package build directories. Fresh temporary copies of `Statement.lean` and
`Counterexample.lean` were compiled at trust level zero and removed afterward:

```bash
set -u
root=$PWD
target=$root/Stage1_Instances/THM-M-1250
lean_root=$root/Formalizations/Lean
mathlib=$lean_root/.lake/packages/mathlib
lean_path=$(find -L "$lean_root/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd:)
tmp=$(mktemp -d "$lean_root/.thm-m-1250-proof-ab6974ae-slot38.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Counterexample.lean" "$tmp/Counterexample.lean"
(
  cd "$mathlib"
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
    lake env lean --root="$lean_root" --trust=0 -t0 \
      -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
      >"$tmp/statement.log" 2>&1
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
    lake env lean --root="$lean_root" --trust=0 -t0 \
      "$tmp/Counterexample.lean" >"$tmp/counterexample.log" 2>&1
  cat "$tmp/counterexample.log"
)
```

The recipe exited `0`. The exact negation and the analytic-support lemma both
reported only `[propext, Classical.choice, Quot.sound]`, with no `sorryAx`.
The output hashes were:

| Output | SHA-256 |
|---|---|
| statement log | `2f7f47d31193d167181eab4606af44bc6d2ad6f1eac751581414659b479f5faa` |
| countertheorem log | `478b93b48893d7ff76281bafdb7c20ee9464a9758d85b4081a5fc788c5d67ed4` |
| temporary `Statement.olean` | `fae43cdd079db016584860a07381679fe8e9d5a10755556308322fa98b88fa91` |

Other exact results:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1250` | 0 | rank 430; planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1250/check_anchor_audit.py` | 0 | immutable mathlib pin and source candidates matched; positive root remains open |
| `python3 Stage1_Instances/THM-M-1250/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed structurally; denominator `24c4c3e8...98bca`; root remains open M3 |
| `python3 Stage1_Instances/THM-M-1250/check_statement.py` | interrupted | root-Lake-dependent checker produced no result after more than 60 seconds; no statement-validation credit claimed |
| prohibited-construct scan over owned Lean files | 1, expected | no prohibited proof device or declaration matched |
| blocker artifact JSON/invariant and new-file whitespace checks | 0 | structured current-base record and blocked/no-selftest invariants passed; both new files had no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is deliberately absent |

The pinned environment was Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The untracked cache symlink and
broken root Lake route make this nonrelease negative evidence.

## Retry Condition

Ordinary positive proof work may resume only after authorized statement repair
replaces the ambiguous regularity order by
`((top : ENat) : WithTop ENat)`, followed by a new statement fingerprint,
mutation checks, anchor audit, versioned obligation registry and typed graphs,
and dependency-order master acceptance. The pinned `flt-regular` checkout must
also be restored without fetching a moving dependency before required root-
project validation.

Because the assigned positive proof phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`. This file is current-base blocker evidence, not a proof receipt.
