# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Recheck date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `3bb4cb3ae15dff8b48c93242019edec3bf858e48`

Base tree: `8e911f5a101bd92eb0951794fa0d9a3c0c3a2ddc`

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen target.
The tracked placeholder-free declaration

```text
Stage1Rev56.THMM1277.not_statement :
  Not Stage1Rev56.THMM1277.Statement
```

kernel-checks again at trust level zero. The frozen definition
`SmoothCompactIn` uses `ContDiff Real top`; at this inferred type, `top` is
mathlib's analytic order `omega`, not the smooth order `infinity`. Analytic
uniqueness therefore makes every compactly supported approximant identically
zero. The selected completion forces every admissible scalar field to vanish
almost everywhere, so every exponential integral equals `volume Omega`.
Applying the supercritical conjunct on the bounded open unit ball with
`C = volume Omega` then requires `volume Omega < volume Omega`.

This refutes the frozen formal encoding, not the mathematical
Moser-Trudinger theorem. A corrected statement cannot be substituted during
this proof item. The positive obligation tree is consequently stale: its
conditional branch composer does not produce the impossible sharpness
premise. The item remains `[ ]`; no proof receipt, accepted obligation,
audit-completion, validation, release, or theorem-completion claim is made.
The dossier's recorded vector remains `[H1, M3, R3]`, with `M5` the proposed
machine diagnosis for this exact-target mismatch.

## Failed Gate And Retry

The first failed gate is exact canonical statement correctness. Reopen
`S56-M-1277-STATEMENT` and spell the intended smooth order unambiguously as
`((top : ENat) : WithTop ENat)` (scoped notation `infinity`). Then re-run the
statement identity and mutation gates and publish a versioned obligation
registry, graphs, and validation specifications for the new statement
fingerprint before retrying proof execution.

The actionable remaining cut set is therefore `S56-M-1277-STATEMENT`, not the
stale positive endpoint and sharpness packages.

## Validation

All checks ran in this worker clone using the existing pinned Lake closure.
No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation
was performed. The automation-provided untracked `Formalizations/Lean/.lake`
symlink makes this nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1277` | 0 | Rank 328; planned lifecycle; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | The frozen 24-obligation, 48-edge projection is structurally valid but still reports its pre-refutation positive root as open `M3`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | Exact statement and refutation elaborated; `not_statement : Not Statement`; every printed axiom set was exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| scoped forbidden-token scan of every owned `*.lean` file | 1 | No prohibited placeholder, declared axiom, generated placeholder constant, or unsafe declaration; exit 1 is ripgrep's no-match result. |
| `python3 -m json.tool Stage1_Instances/THM-M-1277/proof-blocker.json >/dev/null` | 0 | The structured blocker is valid JSON. |
| `timeout 30 lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
set -euo pipefail
TMP=$(mktemp -d /tmp/thm-m-1277-proof-recheck.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
BASE=$(lake env printenv LEAN_PATH)
lake env lean --trust=0 -t0 --root=../.. \
  -o "$TMP/Statement.olean" \
  ../../Stage1_Instances/THM-M-1277/Statement.lean
LEAN_PATH="$TMP:$BASE" lake env lean --trust=0 -t0 --root=../.. \
  ../../Stage1_Instances/THM-M-1277/Proof.lean
```

The input SHA-256 values at this base are: statement
`2b1ddca1ed6abcee99139bfa66e2fc931a543368814b456d50b555a44250f839`,
refutation body
`0ba87510e9549f78ff033bf1dba28657856c748474bef7143a776204ca950d86`,
registry
`aa8ec448e49d03b87ea9afe610a3285318b2c377e68c0dd77ab854a4813abeec`,
typed graphs
`fdcc8a995fc5cbc5b20d14d8fa3d4b6bb657d3d57ca40c0ddc6271cbc00e53f0`,
validation specifications
`2eba2d5cbaaab2abf3664aaf30b7b776f75fc6273788a7f6a16238458142342b`,
and Lake manifest
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

This is durable blocker evidence, not a proof receipt, and accepted receipt IDs
remain empty. Because the assigned positive proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` is deliberately
absent.
