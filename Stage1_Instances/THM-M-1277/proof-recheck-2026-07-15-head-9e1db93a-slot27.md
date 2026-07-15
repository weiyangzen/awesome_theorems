# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `9e1db93a3c4b869cc7c1f8ac99b6c1b12cb4c82c`

Base tree: `0499e20448fdcec5b57b47cc034570b35aab32a1`

## Verdict

`blocked`. The exact frozen target cannot have a legal positive proof body: it
is false. The tracked, placeholder-free declaration

```text
Stage1Rev56.THMM1277.not_statement :
  Not Stage1Rev56.THMM1277.Statement
```

kernel-checks at trust level zero against a freshly emitted
`Statement.olean`.

The defect is in `SmoothCompactIn`. Its `ContDiff Real top` order is mathlib's
analytic order `omega`, not smooth order `infinity`, which is the coerced top
of `ENat`. Analytic uniqueness makes every compactly supported approximant
identically zero. Consequently `ZeroBoundarySobolev` forces its scalar field
to vanish almost everywhere, and every admissible exponential integral equals
`volume Omega` for every exponent. On the bounded open unit ball, the
supercritical clause with `C = volume Omega` then requires
`volume Omega < volume Omega`.

This refutes only the frozen Lean encoding, not the mathematical
Moser-Trudinger theorem. Correcting the target during this proof item would be
an illegal theorem substitution. The dossier's recorded vector remains
`[H1, M3, R3]`; `M5` is only the proposed machine diagnosis for this exact
statement mismatch. No obligation, positive proof receipt, audit completion,
or theorem completion is claimed.

The assigned proof node's prerequisite `S56-M-1277-OBLIGATION_TREE` is still
provisional `[_]`, not master-accepted `[x]`. The statement record also lacks
the required normalized elaborated-expression fingerprint and mutation-test
evidence. In addition, `scope-map.md` says nonemptiness is unnecessary while
the formal target, statement record, and README require it because sharpness
is false on the empty domain. The existing positive obligation registry and
typed graphs predate the refutation. Their validator reports an open `M3`
root; its conditional branch composer cannot supply the false sharpness
premise.

## Validation

All successful Lean checks reused only the existing pinned toolchain and
precompiled dependency artifacts. No `lake update`, `lake build`, dependency
clone/fetch, network access, or `.lake` mutation occurred. The
automation-provided untracked `Formalizations/Lean/.lake` symlink makes this
nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1277` | 0 | Rank 328; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | `PASS`: 24 obligations and 48 typed edges; denominator `e17739e...f60575`; stale positive root open `M3` |
| Fresh temporary-olean recipe below | 0 | `Statement : Prop` and `not_statement : Not Statement` elaborated at trust level zero; all 13 printed axiom sets were exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `timeout 60 lake env lean --version` from `Formalizations/Lean` | 1 | Root Lake resolution failed before Lean because the existing pinned `flt-regular` package has no resolvable `HEAD`; the cache was not repaired or fetched |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe)\b' Stage1_Instances/THM-M-1277 --glob '*.lean'` | 1, expected | No prohibited proof placeholder, declared axiom, generated placeholder constant, or unsafe declaration |
| `lake env lean --version` from the pinned mathlib package | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{commit} HEAD^{tree}` | 0 | Pinned mathlib `8a178386...eea95`, tree `bdc39a31...2c19e5c2b` |
| `test ! -e .stage1-worker-selftest.json` | 0 | No positive proof self-test manifest was written |

The narrow replay ran from the workspace root. It uses `lake env` from the
pinned mathlib package, whose manifest is internally resolvable, and supplies
an explicit `LEAN_PATH` assembled from the already-present root dependency
outputs. This bypasses only the broken unrelated `flt-regular` package
resolution; it neither writes nor rebuilds dependencies.

```bash
set -euo pipefail
ROOT=$PWD
TARGET="$ROOT/Stage1_Instances/THM-M-1277"
LEAN_ROOT="$ROOT/Formalizations/Lean"
MATHLIB="$LEAN_ROOT/.lake/packages/mathlib"
TMP=$(mktemp -d /tmp/thm-m-1277-lake-env.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET/Statement.lean" "$TARGET/Proof.lean" "$TMP"/
TOOLCHAIN_LIB="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
MANUAL_LEAN_PATH=$(find -L "$LEAN_ROOT/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d ! -path '*/flt-regular/*' \
  -print | sort -u | paste -sd: -)
MANUAL_LEAN_PATH="$MANUAL_LEAN_PATH:$TOOLCHAIN_LIB"
cd "$MATHLIB"
LEAN_NUM_THREADS=1 timeout 300 lake env env \
  LEAN_PATH="$MANUAL_LEAN_PATH" lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 timeout 300 lake env env \
  LEAN_PATH="$TMP:$MANUAL_LEAN_PATH" lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Proof.olean" "$TMP/Proof.lean"
```

The checked input SHA-256 values are:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `2b1ddca1ed6abcee99139bfa66e2fc931a543368814b456d50b555a44250f839` |
| `Proof.lean` | `0ba87510e9549f78ff033bf1dba28657856c748474bef7143a776204ca950d86` |
| `obligation-registry.json` | `aa8ec448e49d03b87ea9afe610a3285318b2c377e68c0dd77ab854a4813abeec` |
| `typed-graphs.json` | `fdcc8a995fc5cbc5b20d14d8fa3d4b6bb657d3d57ca40c0ddc6271cbc00e53f0` |
| `validation-specs.json` | `2eba2d5cbaaab2abf3664aaf30b7b776f75fc6273788a7f6a16238458142342b` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |

The fresh output hashes were
`6f184999ed81c69800d9f91cd3c969557853b7ff370c05fdd6790cd31de4e65a`
for `Statement.olean`,
`593f08c48172c08e242b8073f6550e2d3f100806c26d98d9ddb387dc8a1fb3a8`
for statement output, and
`2f47380b9e5a682199aa7e433ad923111d99b9612a1d9bb3a050fa4f8c10d9c8`
for proof output. The temporary directory was removed.

## Retry condition

The first failed gate is exact canonical statement correctness. Reopen
`S56-M-1277-STATEMENT`, use the intended smooth order unambiguously as
`((top : ENat) : WithTop ENat)` (scoped notation `infinity`), reconcile the
nonempty-domain scope text, rerun exact-expression identity and mutation
tests, and publish a versioned obligation registry, typed graphs, and
validation specifications for the new fingerprint before another proof
attempt. Restore the pinned `flt-regular` artifact separately before requiring
root-package Lake replay; do not fetch a moving revision.

The remaining root cut set is `S56-M-1277-STATEMENT`. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
