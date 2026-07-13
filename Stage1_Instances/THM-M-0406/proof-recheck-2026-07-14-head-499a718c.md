# THM-M-0406 proof-phase recheck at current base

Item: `S56-M-0406-PROOF`
Recheck date: 2026-07-14 (Asia/Shanghai)
Base revision: `499a718cc7926abaf61e9721fe0d7485059403e6`
Base tree: `ed2a23c0266f4d921ad97562392226015eee80be`

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
proposition. The existing placeholder-free declaration

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (Stage1Instances.THMM0406.CorvajaZannierTheoremOne.{0, 0} (k := Rat))
```

is a kernel-checked countermodel. It sets `boundaryDivisor := Fin 4`, selects
all four divisors, uses unit weights and intersection numbers, makes every
geometric and boundary premise true, and sets `curve := Empty`. A proof of the
root would therefore produce an inhabitant of `Empty`.

This refutes the frozen abstract encoding, not the mathematical
Corvaja--Zannier theorem. `SurfaceData` does not intrinsically connect its
scheme, point, divisor, curve, or predicate fields. Adding a curve-existence
premise, changing `SurfaceData`, or proving a realizable specialization would
change the assigned target. `SurfaceDegeneracyEngine` in
`ObligationTree.lean` is definitionally the same refutable proposition, so its
conditional adapters provide no positive proof credit.

No proof body or receipt was added, no obligation was closed, and the proof
item remains `[ ]`. The debt vector remains `[H1, M5, R3]` and
`.stage1-worker-selftest.json` is deliberately absent.

## Failed gate and retry

The first failed gate is `M0406-S-DEFINITIONS` / exact-target consistency. The
remaining root cut set is `M0406-S-DEFINITIONS` and `M0406-ROOT`.

Retry only after reopening statement and obligation-tree gates, replacing the
disconnected abstract interface with a source-faithful proposition whose
intrinsic, noncircular semantics rule out this model, and freezing a new exact
expression fingerprint and obligation registry. Merely assuming
`Nonempty X.curve` or the desired output is not a source-faithful repair.

## Validation

All source edits were scoped to this worker clone. No `lake update`,
`lake build`, or explicit dependency clone/fetch command was run. However, an
early `lake env printenv LEAN_PATH` invocation unexpectedly started Lake
dependency provisioning and a `git fetch` for `flt-regular`. It was terminated
immediately, but the shared canonical package directory was left as an
incomplete Git checkout without a resolvable `HEAD`. No repair or further
fetch was attempted. The anchor-audit pin check therefore failed closed.

A direct use of the already pinned Lean binary and existing compiled module
paths still elaborated `Statement.lean` and `Proof.lean` at trust level zero.
The accidental network/package mutation and dirty `.lake` symlink make this
nonrelease blocker evidence, not theorem validation.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | 14 obligations and 26 typed edges passed; denominator `46deb9e...d90a7`; predecessor root open M4. |
| `python3 Stage1_Instances/THM-M-0406/check_anchor_audit.py` | 1 | Failed closed because the shared canonical `flt-regular` checkout had no resolvable `HEAD`; no repair or subsequent fetch was attempted. |
| `cd Formalizations/Lean && lake env printenv LEAN_PATH` | terminated | Unexpectedly started Lake provisioning and a `git fetch` for `flt-regular`; terminated with no output accepted and no subsequent repair/fetch. |
| Direct pinned `lean --trust=0` recipe below | 0 | The exact statement and countermodel elaborated. Both declarations reported `[propext, Classical.choice, Quot.sound]`; statement/proof output SHA-256 values were `0f59d348...385b` and `942b7cc7...a1f8`. |
| `~/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Revision `8a178386...ea95`; tree `bdc39a31...e5c2b`. |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*axiom\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0406 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited construct occurs in the owned Lean sources. |
| `python3 -m json.tool Stage1_Instances/THM-M-0406/proof-recheck-2026-07-14-head-499a718c.json >/dev/null` | 0 | The current-base structured blocker record parsed. |
| `git diff --no-index --check /dev/null <each new owned artifact>; test $? -eq 1` | 0 | No whitespace errors; both expected no-index difference statuses were exactly 1. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion manifest exists because the proof phase is incomplete. |

The direct replay used the pinned Lean 4.29.0 binary and constructed
`LEAN_PATH` only from already present compiled module directories:

```bash
set -euo pipefail
root=$PWD
lean=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
base=$(find "$root/Formalizations/Lean/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -printf '%p:' | sed 's/:$//')
base="$base:$root/Formalizations/Lean/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
tmp=$(mktemp -d /tmp/thm-m-0406-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cd Stage1_Instances/THM-M-0406
LEAN_NUM_THREADS=1 LEAN_PATH="$base" "$lean" --trust=0 -t0 \
  -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base" "$lean" --trust=0 -t0 Proof.lean
```

The current source SHA-256 values are:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `9d6e2a94131455eedcee2ae75765746958988f23f6398cc5c4ea3fbc193258ec` |
| `ObligationTree.lean` | `bbcd4865cc660a210b104c50e19d5ca66055dacdab07182f6d4693c096f3f02c` |
| `Proof.lean` | `afeb346ab8f1ff9e41b87395744faa7a352509d28ef842f10f18a3ec00874aaf` |
| `obligation-registry.json` | `90d988ef727c9f1cbe99cfffb73c21b05f32f6d0b61a2177b624217cfb4612b6` |
| `typed-graphs.json` | `f4da55995c5413f92314904e9687721153b52e7d1d1e1e27fe551f0d7333da17` |
| `anchor-audit.json` | `8e0f84a533e183b8b70ef48955d9fa2dc8dbf39274f4345c600c8f2c143cfd21` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |

This uniquely named current-base report is durable blocker evidence only.
