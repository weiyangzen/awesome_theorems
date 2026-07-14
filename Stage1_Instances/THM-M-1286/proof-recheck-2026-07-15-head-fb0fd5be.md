# THM-M-1286 proof-phase recheck at current base

Item: `S56-M-1286-PROOF`

Intent: `prove`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `fb0fd5be494d0813177dbdc959ec911d69a72015`

Base tree: `f6d39faae5fb024a71ee786e7a6b017d335841cd`

## Verdict

`blocked`. This current-base replay cannot truthfully add an unconditional proof body for
`Stage1Instances.THM_M_1286.PolyaSzegoTarget`. The first failed gate is exact canonical statement
fidelity, so neither of the still-open analytic packages can receive proof credit.

`Statement.lean` defines `Euclidean n` as the ordinary Pi type `Fin n -> Real`. Its installed norm
is the finite-product supremum norm, not the Euclidean `l2` norm in the intake's Schwarz
rearrangement claim. Consequently `IsSymmetricDecreasing` is radial-antitone in `l-infinity`
geometry, and the weak-gradient `eLpNorm` comparison uses the same supremum norm. The existing
placeholder-free `ProofAudit.lean` kernel-checks the Pi norm formula, the discrepancy for
coordinates `(1, -1)`, the exponent-one energy integrand, and the cube/product ball-volume formula.

This is a statement mismatch, not a missing notation change. The earlier blocker analysis gives a
two-dimensional, exponent-one diamond-tent calculation that reverses the requested inequality in
the frozen geometry. It is not a kernel proof of `Not PolyaSzegoTarget`; formalizing that
counterexample would itself require absent weak-derivative, rearrangement-uniqueness, and exact
integration infrastructure.

The positive architecture is also open. `ObligationTree.exactTarget_of_packages` assumes
`RearrangementConstruction` and `GradientEstimate`; it implements neither premise. Focused searches
found no compatible terminal body in the repository or pinned mathlib. The nearby THM-M-1285 files
contain only statement and conditional-interface material. No weaker, conditional, anisotropic,
quadratic-only, or differently typed result was substituted.

The item remains `[ ]`. No proof source or completion self-test manifest was written. This packet is
current-base blocker evidence, not a proof receipt.

## Narrow validation

All Lean checks reused the automation-provided pinned Lake artifacts read-only. No `lake update`,
`lake build`, dependency clone/fetch, network access, or `.lake` mutation was performed. Compiled
output was isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; recorded root remains open at `M4`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | `Statement.lean`, five diagnostic declarations in `ProofAudit.lean`, and conditional composition in `ObligationTree.lean` elaborated; three temporary oleans were produced. Every checked declaration reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|unsafe|implemented_by|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| Focused semantic search in pinned mathlib | 1, expected | No `equimeasur`, symmetric-decreasing/Schwarz rearrangement, or Pólya-Szegő candidate occurs. |
| Same search over repository Lean sources, excluding this target | 0 | Only THM-M-1285 statement and conditional interfaces; no compatible terminal body. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/proof-recheck-2026-07-15-head-fb0fd5be.json` | 0 | Structured current-base blocker is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1286` | 0 | No tracked whitespace error. No-index checks below cover the two new files. |
| `git diff --no-index --check /dev/null` against each new packet file | 1, expected | Each untracked file differs from `/dev/null`; neither command emitted a whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is absent because the proof phase is blocked. |

Exact Lean replay from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-slot53-fb0fd5be.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/Stage1_Instances/THM-M-1286"
cd "$ROOT/Formalizations/Lean"
LEAN_NUM_THREADS=1 timeout 180 lake env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/Stage1_Instances/THM-M-1286/Statement.olean" \
  ../../Stage1_Instances/THM-M-1286/Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP" timeout 180 lake env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/ProofAudit.olean" \
  ../../Stage1_Instances/THM-M-1286/ProofAudit.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP" timeout 180 lake env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/ObligationTree.olean" \
  ../../Stage1_Instances/THM-M-1286/ObligationTree.lean
```

Exact placeholder and candidate searches, run from the repository root:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide' \
  Stage1_Instances/THM-M-1286 --glob '*.lean'
rg -n -i \
  'equimeasur|symmetric.?decreasing.?rearrang|schwarz.?symm|schwarz.?rearrang|polya.?szego|pólya.?szegő' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'
rg -n -i \
  'equimeasur|symmetric.?decreasing.?rearrang|schwarz.?symm|schwarz.?rearrang|polya.?szego|pólya.?szegő' \
  Stage1_Instances Formalizations/Lean/AwesomeTheorems --glob '*.lean' \
  --glob '!Stage1_Instances/THM-M-1286/**'
```

Pinned input SHA-256 values: `Statement.lean` `ef428b6d...9bb`; `ObligationTree.lean`
`31690c4c...4d6b`; `ProofAudit.lean` `09152048...47a9`; `obligation-registry.json`
`c7d331ee...d20`; `typed-graphs.json` `9c225e12...7e2`; `lake-manifest.json`
`321626c8...2d81`.

## Retry condition

Reopen `S56-M-1286-STATEMENT`, replace the ordinary Pi type with a measure-compatible Euclidean
`l2` encoding, and rerun statement identity/transports/mutations, anchor audit, registry, typed
graphs, and obligation-tree gates. Then implement both analytic packages without placeholders, or
pin and exact-type-check an immutable compatible Lean 4 body.

## Status boundary

Lifecycle remains `planned`. The intake/README vector `[H2, M4, R3]` conflicts with the typed
graph's root human debt `H3`; integration must reconcile that stale state and should review an `M5`
classification for the checked statement mismatch. No audit completion, validation, release,
master acceptance, or theorem completion is claimed.
