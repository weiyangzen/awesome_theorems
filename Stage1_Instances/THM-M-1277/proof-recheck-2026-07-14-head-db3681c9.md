# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `db3681c9e2616e7be7e8b5fde7fe48c77d6df6fe`

Base tree: `03ebac35e51f1236b49c6a3110b748d45c6c2682`

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen target.
The existing placeholder-free declaration

```text
Stage1Rev56.THMM1277.not_statement :
  Not Stage1Rev56.THMM1277.Statement
```

kernel-checks again at trust level zero against a freshly elaborated
`Statement.olean`.

The failure is in `SmoothCompactIn`: its `ContDiff Real top` order is
mathlib's analytic order `omega`, not smooth order `infinity`. Analytic
uniqueness forces every compactly supported approximant to be identically
zero. Hence `ZeroBoundarySobolev` forces its scalar field to vanish almost
everywhere and every admissible exponential integral equals `volume Omega`.
On the bounded open unit ball, the supercritical clause with
`C = volume Omega` then requires `volume Omega < volume Omega`.

This refutes the frozen Lean encoding, not the mathematical
Moser-Trudinger theorem. Correcting or broadening the target during this
proof item would be an illegal substitution. The recorded dossier vector
remains `[H1, M3, R3]`; `M5` is only the proposed machine diagnosis for this
exact statement mismatch. The positive obligation registry and typed graphs
predate the refutation and are stale even though their structural validator
passes. No obligation, proof receipt, audit completion, or theorem
completion is claimed.

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
| Fresh temporary-olean Lean recipe below | 0 | `Statement : Prop` and `not_statement : Not Statement` elaborated at trust level zero; the module prints only `propext`, `Classical.choice`, and `Quot.sound` for each declaration |
| Independent read-only worker replay of the same recipe | 0 | Independently confirmed the exact countertheorem at this base and the same source hashes |
| `rg -n '\\b(sorry\|admit\|sorryAx)\\b\|^[[:space:]]*(axiom\|unsafe)\\b' Stage1_Instances/THM-M-1277 --glob '*.lean'` | 1, expected | No prohibited proof placeholder, declared axiom, generated placeholder constant, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1277/proof-blocker.json >/dev/null` | 0 | The structured blocker is valid JSON |
| `lake env lean --version` (from `Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
set -euo pipefail
TMP=$(mktemp -d /tmp/thm-m-1277-proof-db3681c9.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
BASE=$(lake env printenv LEAN_PATH)
lake env lean --trust=0 -t0 --root=../.. \
  -o "$TMP/Statement.olean" \
  ../../Stage1_Instances/THM-M-1277/Statement.lean
LEAN_PATH="$TMP:$BASE" lake env lean --trust=0 -t0 --root=../.. \
  ../../Stage1_Instances/THM-M-1277/Proof.lean
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

## Retry condition

The first failed gate is exact canonical statement correctness. Reopen
`S56-M-1277-STATEMENT`, spell the intended smooth order unambiguously as
`((top : ENat) : WithTop ENat)` (scoped notation `infinity`), rerun statement
identity and mutation gates, and publish a versioned obligation registry,
typed graphs, and validation specifications for the changed fingerprint
before another proof attempt.

The remaining root cut set is `S56-M-1277-STATEMENT`. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
