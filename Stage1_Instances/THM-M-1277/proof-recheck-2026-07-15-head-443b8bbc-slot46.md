# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. The exact frozen target has no legal positive proof body because it
is false. The tracked, placeholder-free declaration

```text
Stage1Rev56.THMM1277.not_statement :
  Not Stage1Rev56.THMM1277.Statement
```

freshly kernel-checks at trust level zero against a freshly emitted
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
an illegal substitution. The dossier's recorded vector remains
`[H1, M3, R3]`; `M5` is only the proposed diagnosis of the exact statement
mismatch. No obligation, positive proof receipt, audit completion, validation,
release, or theorem completion is claimed.

The assigned node's prerequisite `S56-M-1277-OBLIGATION_TREE` is still
provisional `[_]`, not master-accepted `[x]`. The statement record also lacks
the required normalized elaborated-expression fingerprint and mutation-test
evidence. In addition, `scope-map.md` says nonemptiness is unnecessary while
the formal target, statement record, and README require it because sharpness
is false on the empty domain. The stale positive obligation graph has 24
obligations and 48 typed edges and reports an open `M3` root; its conditional
branch composer cannot supply the false sharpness premise.

## Validation

The worker first attempted the required `lake env lean` path against the
shared dependency cache. It failed before Lean started because
`flt-regular` had `HEAD = refs/heads/.invalid`. After that invocation, the
checkout was newly initialized and its `FETCH_HEAD` changed repeatedly while
other automation processes were also invoking Lake against the same cache, so
mutation attribution cannot be isolated. This worker did not explicitly run
`lake update`, `lake build`, `git clone`, `git fetch`, or `git checkout`,
stopped using Lake after the failure, and did not attempt a repair.

As narrowly scoped corroboration, the same pinned Lean 4.29.0 executable was
run with `LEAN_PATH` assembled read-only from the already present package build
directories. That fresh trust-zero replay succeeded and reproduced the prior
tracked output hashes exactly. Because it did not pass through `lake env lean`,
it is blocker corroboration, not the required pinned release receipt.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1277` | 0 | Rank 328; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | `PASS`: 24 obligations and 48 typed edges; denominator `e17739e...f60575`; stale positive root open `M3` |
| Required fresh `lake env lean` recipe | 1 | Lake stopped before Lean: `flt-regular: could not resolve 'HEAD' to a commit` |
| Read-only fallback fresh-olean recipe below | 0 | `Statement : Prop` and `not_statement : Not Statement` elaborated at trust level zero; every printed axiom set was exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe)\b' Stage1_Instances/THM-M-1277 --glob '*.lean'` | 1, expected | No prohibited proof placeholder, declared axiom, generated placeholder constant, or unsafe declaration |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{commit} HEAD^{tree}` | 0 | Pinned mathlib `8a178386...eea95`, tree `bdc39a31...2c19e5c2b` |
| `test ! -e .stage1-worker-selftest.json` | 0 | No positive proof self-test manifest was written |

The required attempt, run from the workspace root, was:

```bash
set -u
ROOT=$PWD
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/thm-m-1277-proof-443b8bbc.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cd "$LEAN_ROOT"
BASE=$(timeout 60 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 \
  --root=../.. -o "$TMP/Statement.olean" \
  ../../Stage1_Instances/THM-M-1277/Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" timeout 300 lake env lean \
  --trust=0 -t0 --root=../.. \
  ../../Stage1_Instances/THM-M-1277/Proof.lean
```

The read-only fallback used the pinned toolchain and existing build products:

```bash
set -u
ROOT=$PWD
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/thm-m-1277-proof-direct-443b8bbc.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cd "$LEAN_ROOT"
PATHS="$PWD/.lake/build/lib/lean"
for d in "$PWD"/.lake/packages/*/.lake/build/lib/lean; do
  test -d "$d" && PATHS="$PATHS:$d"
done
LEAN_NUM_THREADS=1 LEAN_PATH="$PATHS" timeout 300 lean --trust=0 -t0 \
  --root=../.. -o "$TMP/Statement.olean" \
  ../../Stage1_Instances/THM-M-1277/Statement.lean \
  >"$TMP/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$PATHS" timeout 300 lean --trust=0 -t0 \
  --root=../.. ../../Stage1_Instances/THM-M-1277/Proof.lean \
  >"$TMP/proof.out" 2>&1
sha256sum "$TMP/Statement.olean" "$TMP/statement.out" "$TMP/proof.out"
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
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |

The fresh output hashes were
`84f541c01763ee25facdce4cfc28cc3380e52a5f55d9c3c295c0cefe99159e63`
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
attempt. Separately restore the pinned `flt-regular` checkout so that the
required `lake env lean` recipe can be replayed without fetching a moving
dependency.

The remaining root cut set is `S56-M-1277-STATEMENT`. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
