# THM-M-1250 proof blocker handoff at `cf0d919f` (slot33)

Item: `S56-M-1250-PROOF`

Intent: `prove`

Recorded: `2026-07-15T23:45:19+08:00` (`Asia/Shanghai`)

Base revision: `cf0d919f2dfc00f3f777e9319188dec0f644d159`

Base tree: `993e3e180c52396b1dd8c970410284d8c3e5bf8d`

## Verdict

`blocked`. A positive proof cannot inhabit the exact frozen target. The
tracked, placeholder-free theorem

```text
Stage1Instances.THM_M_1250.Counterexample.not_schwartzSpaceCharacterization :
  Not Stage1Instances.THM_M_1250.SchwartzSpaceCharacterization
```

was freshly replayed at trust level zero. `Statement.lean` writes
`ContDiff Real top f` without fixing the order type, so Lean elaborates it as
`top : WithTop ENat`, mathlib's analytic order `omega`. A `SchwartzMap`
instead stores regularity at `(top : ENat) : WithTop ENat`, the smooth order
`infinity`. A nonzero compactly supported smooth bump is therefore a
`SchwartzMap` but cannot satisfy the frozen analytic conjunct.

This run adds an unambiguous target-local interface module and proves

```text
Stage1Instances.THM_M_1250.not_m1250ForwardPackage :
  Not Stage1Instances.THM_M_1250.M1250ForwardPackage
```

by composing an assumed exact forward package with the already checked local
reverse package and the exact root composition, then applying the canonical
countertheorem. This is a real negative proof body, not positive root closure.
It avoids the repository's generic `ObligationTree` module-name collision and
binds the impossibility certificate directly to the exact interface spelled
by `M1250-F-PACKAGE`.

The checked counterexample refutes only the erroneous frozen analytic
encoding, not the classical Schwartz-space theorem at smooth order
`infinity`. Correcting the order here would substitute a different theorem.
The required predecessor `S56-M-1250-OBLIGATION_TREE` is also only
worker-provisional `[_]`, not master-accepted `[x]`. The proof item therefore
remains `[ ]`; no success self-test or completion receipt is emitted.

## Lean Evidence

No `lake update`, `lake build`, dependency clone/fetch/checkout, network
action, or `.lake` mutation was performed. The automation-provided canonical
`.lake` symlink was reused read-only. All Lean outputs were written beneath a
fresh disposable directory in `Formalizations/Lean` and removed after replay.

The exact trust-zero recipe was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1250
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d "$lean_root/.thm-m-1250-final-cf0d919f-slot33.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
for f in Statement ProofBlocker Counterexample M1250ObligationTree M1250ProofRefutation; do
  cp "$target/$f.lean" "$tmp/$f.lean"
done
cd "$lean_root"
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.log" 2>&1
export LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}"
for f in ProofBlocker Counterexample M1250ObligationTree; do
  LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600 \
    lake env lean --root="$lean_root" --trust=0 -t0 \
    -o "$tmp/$f.olean" "$tmp/$f.lean" \
    >"$tmp/$f.log" 2>&1
done
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600 \
  lake env lean --root="$lean_root" --trust=0 -t0 \
  "$tmp/M1250ProofRefutation.lean" \
  >"$tmp/M1250ProofRefutation.log" 2>&1
```

All five invocations exited `0`. The countertheorem and canonical forward-
package negation both reported only
`[propext, Classical.choice, Quot.sound]`, with no `sorryAx`.

| Output | SHA-256 | Bytes |
|---|---|---:|
| statement log | `2f7f47d31193d167181eab4606af44bc6d2ad6f1eac751581414659b479f5faa` | 3170 |
| proof-blocker log | `535657cf2f2e5daab81470ec801591ae719f488b9f2032c49ff6b69fb18d896a` | 2667 |
| countertheorem log | `478b93b48893d7ff76281bafdb7c20ee9464a9758d85b4081a5fc788c5d67ed4` | 365 |
| interface log | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| forward-package negation log | `c381cdbee0efb5d74115de513ba879183804c1a5179f1658edd74c978ebc571d` | 187 |

The pinned environment was Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, with executable SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.
Mathlib was revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

Other exact results:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1250` | 0 | rank 430; planned lifecycle; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1250/check_statement.py` | 0 | expression hash and four mutations passed; identity only, not truth |
| `python3 Stage1_Instances/THM-M-1250/check_anchor_audit.py` | 0 | pinned mathlib candidates matched; root remains open |
| `python3 Stage1_Instances/THM-M-1250/check_obligation_tree.py` | 0 | 15 obligations and 30 edges passed; root remains open M3 |
| prohibited-construct scan over owned Lean files | 1, expected | no prohibited proof escape matched |

## Retry Condition

Reopen `S56-M-1250-STATEMENT`, replace the ambiguous order by the intended
`((top : ENat) : WithTop ENat)`, and regenerate the statement fingerprint,
mutations, anchor audit, obligation registry, and typed graphs. All invalidated
prerequisites must then receive dependency-ordered master acceptance before a
positive proof attempt. Alternatively, redirect this work explicitly to a
counterexample/barrier target.

Because this positive proof phase is blocked rather than self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
