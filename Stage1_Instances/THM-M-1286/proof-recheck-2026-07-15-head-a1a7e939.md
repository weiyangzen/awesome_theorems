# THM-M-1286 proof-phase recheck at current base

Item: `S56-M-1286-PROOF`

Intent: `prove`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Verdict

`blocked`. The proof phase cannot truthfully add an unconditional proof body for the current
canonical target. The first failed gate is exact canonical statement fidelity, before either open
analytic proof package can receive credit.

`Statement.lean` abbreviates `Euclidean n` as the ordinary function type `Fin n -> Real`. Mathlib
equips that type with the finite-product supremum norm, not the Euclidean `l2` norm selected by the
intake's Schwarz-rearrangement claim. Therefore `IsSymmetricDecreasing` is radial-antitone in
`l-infinity` geometry, while the gradient energy uses the same supremum norm. The existing
placeholder-free `ProofAudit.lean` kernel-checks the Pi norm formula, a two-coordinate discrepancy
with `EuclideanSpace`, the exponent-one gradient integrand, and the product/cube ball-volume
formula.

This is substantive rather than a cosmetic encoding issue. For `n = 2`, `p = 1`, the diamond-tent
example analyzed in the prior proof packets has input supremum-gradient energy `2`, while its
equimeasurable sup-radial cube tent has energy `2 * sqrt 2`, reversing the requested direction.
That is blocker analysis, not a kernel proof of `Not PolyaSzegoTarget`: formalizing its weak
derivatives, rearrangement uniqueness, and sharp integrals would itself require missing analysis.

The positive architecture also remains open. `ObligationTree.exactTarget_of_packages` assumes
`RearrangementConstruction` and `GradientEstimate`; it implements neither premise and hence does
not close the root. Current repository and pinned-mathlib searches found no compatible terminal
body. The closest pinned results provide layer-cake, ball-volume, integration-by-parts, or Sobolev
infrastructure only. No weaker, conditional, anisotropic, quadratic-only, or differently typed
theorem was substituted.

The item remains `[ ]`. No proof source or completion self-test manifest was written. This packet
is fresh, current-base blocker evidence and is not a proof receipt.

## Narrow validation

All checks ran in this worker clone against the automation-provided read-only symlink to the
canonical pinned Lake artifacts. No `lake update`, `lake build`, dependency clone/fetch, network
access, or `.lake` mutation was performed. Lean output was isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; recorded positive root remains open at `M4`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | `Statement.lean`, five diagnostic declarations in `ProofAudit.lean`, and conditional composition in `ObligationTree.lean` elaborated; three temporary oleans were produced. Every checked declaration reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| `rg -n -i 'equimeasur|symmetric.?decreasing.?rearrang|schwarz.?symm|schwarz.?rearrang|polya.?szego|pólya.?szegő' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1, expected | No semantic proof candidate occurs in pinned mathlib. |
| Same semantic search over repository Lean sources, excluding this target | 0 | Only neighboring `THM-M-1285` statement and conditional interfaces; no compatible terminal body. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/proof-recheck-2026-07-15-head-a1a7e939.json` | 0 | Structured current-base blocker is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1286/proof-recheck-2026-07-15-head-a1a7e939.{json,md}` | 0 | No tracked whitespace errors. |
| `git diff --no-index --check /dev/null` against each new packet file | 1, expected | Each untracked file differs from `/dev/null`; neither check emitted a whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is absent because the proof phase is blocked. |

Exact Lean replay, run from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-slot53-lakeenv.XXXXXX)
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

Pinned inputs: `Statement.lean` SHA-256 `ef428b6d...9bb`; `ObligationTree.lean`
`31690c4c...4d6b`; `ProofAudit.lean` `09152048...47a9`; `lake-manifest.json`
`321626c8...2d81`.

## Retry condition

Reopen `S56-M-1286-STATEMENT`, replace the ordinary Pi type with a measure-compatible Euclidean
`l2` encoding, and rerun statement identity/transports/mutations, anchor audit, registry, typed
graphs, and obligation-tree gates. Then implement both analytic packages without placeholders or
pin and exact-type-check an immutable compatible Lean 4 body.

## Status boundary

Lifecycle remains `planned`. The dossier's intake/README vector `[H2, M4, R3]` conflicts with the
typed graph's root `[H3, M4, R3]`; this worker preserves authoritative state and asks integration to
reconcile it. Integration should also consider `M5` for the demonstrated statement mismatch. No
audit completion, validation, release, master acceptance, or theorem completion is claimed.
