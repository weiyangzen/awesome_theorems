# THM-M-1286 proof-phase recheck at current base

Item: `S56-M-1286-PROOF`

Intent: `prove`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `3f555cfc0879cb7c42e83d6bcf7b9e3e09997e58`

Base tree: `e8837f7e0722548e2b35e901d9d974797097635e`

## Verdict

`blocked`; lifecycle remains `planned`, state remains `[ ]`, and the root remains open.

The first failed gate precedes proof implementation: exact canonical statement fidelity. In
`Statement.lean`, `Euclidean n` abbreviates `Fin n -> Real`. The installed Pi norm is the
coordinate supremum norm, not the Euclidean `l2` norm required by the intake's Schwarz
rearrangement claim. Consequently `IsSymmetricDecreasing`, metric balls, and the gradient
`eLpNorm` describe `l-infinity` geometry. The trust-zero declarations in `ProofAudit.lean` check
this mismatch: the frozen norm of `[1, -1]` is one, while its standard Euclidean norm squared is
two.

The obligation registry and typed graphs were frozen before this mismatch was found and therefore
cannot support proof execution. Their checked `exactTarget_of_packages` body only composes assumed
`RearrangementConstruction` and `GradientEstimate` packages. Neither package has an unconditional
body, and no compatible terminal body exists in the pinned mathlib or repository search surface.
Treating either package as a premise would violate the proof deliverable.

No statement, theorem body, dependency, registry, graph, or task state was changed. No weaker,
conditional, finite, anisotropic, or differently typed theorem was substituted. This packet is
current-base blocker evidence, not a proof receipt; `.stage1-worker-selftest.json` remains absent.

## Narrow validation

All Lean checks reused the automation-provided pinned Lake artifacts read-only. No `lake update`,
`lake build`, dependency clone/fetch, network access, or `.lake` mutation was performed. Compiled
output was isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; the recorded positive root remains open at `M4`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | `Statement.lean`, five diagnostic declarations in `ProofAudit.lean`, and conditional composition in `ObligationTree.lean` elaborated; three temporary oleans were produced. Every checked declaration reported exactly `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|unsafe|implemented_by|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| Focused semantic search in pinned mathlib | 1, expected | No equimeasurability, symmetric-decreasing/Schwarz rearrangement, or Polya-Szego candidate occurs. |
| Same search over repository Lean sources, excluding this target | 0 | Only THM-M-1285 statement and conditional interfaces occur; no compatible terminal body exists. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` and `HEAD^{tree}` | 0 | Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `sha256sum` over the recorded target inputs and Lake manifest | 0 | Every digest matched the structured packet. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is absent because the proof phase is blocked. |

Exact Lean replay from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-slot64-3f555cfc.XXXXXX)
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

Exact candidate searches from the repository root:

```bash
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
`c7d331ee...d20`; `typed-graphs.json` `9c225e12...7e2`; `anchor-audit.json`
`f05ca7a6...33c`; `validation-specs.json` `2ee56fb5...4e9a`; `lake-manifest.json`
`321626c8...2d81`.

## Retry condition

Reopen `S56-M-1286-STATEMENT`, replace the ordinary Pi type with a measure-compatible Euclidean
`l2` encoding, and rerun statement identity, transports, mutations, anchor audit, registry, typed
graphs, and obligation-tree gates. Then implement both analytic packages without placeholders, or
pin and exact-type-check an immutable compatible Lean 4 body.

## Status boundary

The current workflow cut set is `S56-M-1286-STATEMENT`; the stale positive proof graph instead
records `M1286-C-REARRANGE` and `M1286-L-GRADIENT`. The intake/README vector `[H2, M4, R3]` also
conflicts with the typed graph's root human debt `H3`; integration must reconcile that stale state.
No audit completion, validation, release, master acceptance, or theorem completion is claimed.
