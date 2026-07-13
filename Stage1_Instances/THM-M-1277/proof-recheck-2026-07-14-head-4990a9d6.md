# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `4990a9d6fa09beb7747e6822c6543c6123ca7504`

Base tree: `b74497bc09c004757aa3974f3bb0622d77e20106`

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen target
because that target is false. The tracked, placeholder-free declaration

```text
Stage1Rev56.THMM1277.not_statement :
  Not Stage1Rev56.THMM1277.Statement
```

kernel-checks at trust level zero against a freshly emitted
`Statement.olean`.

The defect is in `SmoothCompactIn`. Its `ContDiff Real top` order is inferred
as `WithTop ENat`, whose `top` is mathlib's analytic order `omega`; it is not
the smooth order `infinity`, which is the coerced top of `ENat`. Analytic
uniqueness makes every compactly supported approximant identically zero.
Consequently `ZeroBoundarySobolev` forces every admitted scalar field to
vanish almost everywhere, and every admissible exponential integral equals
`volume Omega`, independently of the exponent. On the bounded open unit ball,
the supercritical clause with `C = volume Omega` then requires
`volume Omega < volume Omega`.

This refutes only the frozen Lean encoding, not the mathematical
Moser-Trudinger theorem. Correcting or broadening the statement during this
proof item would be an illegal substitution. The recorded dossier vector
remains `[H1, M3, R3]`; `M5` is only the proposed machine diagnosis for the
exact statement mismatch. No obligation, proof receipt, audit completion, or
theorem completion is claimed.

The positive obligation registry and typed graphs predate the refutation.
Their structural validator still reports an open `M3` root, but their
conditional composition cannot supply the false sharpness premise.

## Validation

All checks ran in this worker clone using the existing pinned Lake closure.
No `lake update`, `lake build`, dependency clone/fetch, network access, or
`.lake` mutation was performed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1277` | 0 | Rank 328; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | `PASS`: 24 obligations and 48 typed edges; denominator `e17739e...f60575`; stale positive root open `M3` |
| Fresh temporary-olean Lean recipe below | 0 | `Statement : Prop` and `not_statement : Not Statement` elaborated at trust level zero; every printed axiom set was exactly `propext`, `Classical.choice`, and `Quot.sound` |
| Independent read-only review and fresh replay | 0 | A separate worker confirmed the exact countertheorem and refutation chain; its fresh replay reproduced the same three-axiom report and output hashes |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe)\b' Stage1_Instances/THM-M-1277 --glob '*.lean'` | 1, expected | No prohibited proof placeholder, declared axiom, generated placeholder constant, or unsafe declaration |
| `lake env lean --version` (from `Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-1277/proof-recheck-2026-07-14-head-4990a9d6.json >/dev/null` | 0 | This current-base structured blocker is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1277` | 0 | No whitespace errors in tracked owned-path changes; the two new artifacts require the explicit checks below |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1277/proof-recheck-2026-07-14-head-4990a9d6.json` | 1, expected | Added-file status with no whitespace diagnostic |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1277/proof-recheck-2026-07-14-head-4990a9d6.md` | 1, expected | Added-file status with no whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | No positive proof self-test manifest was written |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
set -u
TMP=$(mktemp -d /tmp/thm-m-1277-proof-4990a9d6-slot54.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
BASE=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 --root=../.. \
  -o "$TMP/Statement.olean" \
  ../../Stage1_Instances/THM-M-1277/Statement.lean \
  >"$TMP/statement.log" 2>&1
s=$?
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" timeout 300 lake env lean \
  --trust=0 -t0 --root=../.. \
  ../../Stage1_Instances/THM-M-1277/Proof.lean \
  >"$TMP/proof.log" 2>&1
p=$?
printf 'statement_exit=%s proof_exit=%s\n' "$s" "$p"
printf '%s\n' '--- statement output ---'
cat "$TMP/statement.log"
printf '%s\n' '--- proof output ---'
cat "$TMP/proof.log"
printf '%s\n' '--- output sha256 ---'
sha256sum "$TMP/statement.log" "$TMP/proof.log"
exit "$((s || p))"
```

The fresh statement and proof output SHA-256 values were respectively
`593f08c48172c08e242b8073f6550e2d3f100806c26d98d9ddb387dc8a1fb3a8`
and `2f47380b9e5a682199aa7e433ad923111d99b9612a1d9bb3a050fa4f8c10d9c8`.
The checked input SHA-256 values are:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `2b1ddca1ed6abcee99139bfa66e2fc931a543368814b456d50b555a44250f839` |
| `Proof.lean` | `0ba87510e9549f78ff033bf1dba28657856c748474bef7143a776204ca950d86` |
| `obligation-registry.json` | `aa8ec448e49d03b87ea9afe610a3285318b2c377e68c0dd77ab854a4813abeec` |
| `typed-graphs.json` | `fdcc8a995fc5cbc5b20d14d8fa3d4b6bb657d3d57ca40c0ddc6271cbc00e53f0` |
| `validation-specs.json` | `2eba2d5cbaaab2abf3664aaf30b7b776f75fc6273788a7f6a16238458142342b` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |

## Retry condition

The first failed gate is exact canonical statement correctness. Reopen
`S56-M-1277-STATEMENT`, spell the intended smooth order unambiguously as
`((top : ENat) : WithTop ENat)` (scoped notation `infinity`), rerun exact
statement identity and mutation gates, and publish a versioned obligation
registry, typed graphs, and validation specifications for the changed
fingerprint before another proof attempt.

The remaining root cut set is `S56-M-1277-STATEMENT`. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
