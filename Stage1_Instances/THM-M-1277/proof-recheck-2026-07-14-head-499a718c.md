# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `499a718cc7926abaf61e9721fe0d7485059403e6`

Base tree: `ed2a23c0266f4d921ad97562392226015eee80be`

## Verdict

`blocked`. The exact frozen target has no legal positive proof body because it
is false. The tracked placeholder-free declaration

```text
Stage1Rev56.THMM1277.not_statement :
  Not Stage1Rev56.THMM1277.Statement
```

kernel-checks at trust level zero against a freshly emitted
`Statement.olean`.

The failure is in `SmoothCompactIn`. Its `ContDiff Real top` order is
mathlib's analytic order `omega`, not smooth order `infinity`, which is the
coerced top of `ENat`. Analytic uniqueness makes every compactly supported
approximant identically zero. Therefore `ZeroBoundarySobolev` forces its
scalar field to vanish almost everywhere and every admissible exponential
integral equals `volume Omega`, for every exponent. On the bounded open unit
ball, the supercritical clause with `C = volume Omega` then requires
`volume Omega < volume Omega`.

This refutes only the frozen Lean encoding, not the mathematical
Moser-Trudinger theorem. Correcting the target during this proof item would be
an illegal substitution. The dossier's recorded vector remains
`[H1, M3, R3]`; `M5` is only the proposed machine diagnosis for the exact
statement mismatch. No obligation, proof receipt, audit completion, or
theorem completion is claimed.

The statement prerequisite also lacks the required normalized elaborated-
expression fingerprint and the required mutation-test evidence. The existing
positive obligation registry and typed graphs predate the refutation. Their
structural validator still reports an open `M3` root, but the checked
conditional branch composer cannot supply the false sharpness premise.

## Validation

All successful Lean checks used the existing pinned artifacts read-only. The
Lake wrapper could not resolve the environment because another manifest
dependency in the shared canonical cache was incomplete, and resolution would
have attempted a prohibited dependency fetch. The narrow check therefore
invoked the same pinned Lean 4.29.0 binary directly with `LEAN_PATH` assembled
from existing `.lake/**/.lake/build/lib/lean` directories. No `lake update`,
`lake build`, dependency clone/fetch, network access, or `.lake` mutation was
performed by this run. The untracked `Formalizations/Lean/.lake` symlink also
makes this nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1277` | 0 | Rank 328; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | `PASS`: 24 obligations and 48 typed edges; denominator `e17739e...f60575`; stale positive root open `M3` |
| Direct pinned-Lean temporary-olean recipe below | 0 | `Statement : Prop` and `not_statement : Not Statement` elaborated at trust level zero; every printed axiom set was exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe)\b' Stage1_Instances/THM-M-1277 --glob '*.lean'` | 1, expected | No prohibited proof placeholder, declared axiom, generated placeholder constant, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1277/proof-recheck-2026-07-14-head-499a718c.json >/dev/null` | 0 | This current-base structured blocker is valid JSON |
| `test ! -e .stage1-worker-selftest.json` | 0 | No positive proof self-test manifest was written |
| `git diff --no-index --check /dev/null <new-artifact>` for each current-base JSON/Markdown artifact | 1 per added file, expected | Both commands produced empty diagnostic output, so neither artifact has a whitespace error |

Exact direct Lean recipe, run from the workspace root:

```bash
set -u
ROOT=$PWD
LEAN_ROOT="$ROOT/Formalizations/Lean"
TARGET="$ROOT/Stage1_Instances/THM-M-1277"
TMP=$(mktemp -d /tmp/thm-m-1277-proof-499a718c.XXXXXX)
LEAN="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
BASE=$(find "$LEAN_ROOT/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd: -)
BASE="$BASE:$LEAN_ROOT/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE" timeout 300 "$LEAN" \
  --trust=0 -t0 --root="$ROOT" -o "$TMP/Statement.olean" \
  "$TARGET/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" timeout 300 "$LEAN" \
  --trust=0 -t0 --root="$ROOT" "$TARGET/Proof.lean"
rm -rf "$TMP"
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

The fresh output hashes were `84f541c0...59e63` for `Statement.olean`,
`593f08c4...fb3a8` for statement output, and `2f47380b...0d9c8` for proof
output.

## Retry condition

The first failed gate is exact canonical statement correctness. Reopen
`S56-M-1277-STATEMENT`, use the intended smooth order unambiguously as
`((top : ENat) : WithTop ENat)` (scoped notation `infinity`), rerun exact-
expression identity and mutation tests, and publish a versioned obligation
registry, typed graphs, and validation specifications for the new fingerprint
before another proof attempt.

The remaining root cut set is `S56-M-1277-STATEMENT`. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
