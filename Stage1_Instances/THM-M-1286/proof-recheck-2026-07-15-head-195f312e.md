# THM-M-1286 proof-phase recheck at current base

Item: `S56-M-1286-PROOF`

Intent: `prove`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `195f312e0164390d672a8e6642dd1242dd7bbe8d`

Base tree: `f12d8c8e0368a8142da0ceeb2c931a087157f49c`

## Verdict

`blocked`. No unconditional proof body can truthfully be added for the current canonical target.
The first failed gate is exact canonical statement fidelity, before either open analytic package can
receive proof credit.

`Statement.lean` abbreviates `Euclidean n` as the ordinary Pi type `Fin n -> Real`. Its installed
norm is the finite-product supremum norm, not the Euclidean `l2` norm selected by the intake's
Schwarz-rearrangement claim. Thus `IsSymmetricDecreasing` is radial-antitone in `l-infinity`
geometry and the weak-gradient energy also uses the supremum norm. The placeholder-free
`ProofAudit.lean` kernel-checks the Pi norm formula, the discrepancy at coordinates `(1, -1)`, the
exponent-one energy integrand, and the product/cube ball-volume formula.

This is a mathematical encoding mismatch, not a notation issue. Prior blocker analysis gives an
`n = 2`, `p = 1` diamond-tent example whose input supremum-gradient energy is `2`, while its
equimeasurable sup-radial cube tent has energy `2 * sqrt 2`, reversing the requested inequality.
That analysis is not a kernel proof of `Not PolyaSzegoTarget`: formalizing the weak derivatives,
rearrangement uniqueness, and exact integrals would itself require missing infrastructure.

The positive architecture remains open as well. `ObligationTree.exactTarget_of_packages` assumes
`RearrangementConstruction` and `GradientEstimate`; it implements neither premise. Focused searches
found no compatible terminal body in the repository or pinned mathlib. The neighboring
`THM-M-1285` files contain only statement, elementary profile lemmas, and conditional interfaces.
No weaker, conditional, anisotropic, quadratic-only, or differently typed result was substituted.

The item remains `[ ]`. No proof source or completion self-test manifest was written. This packet is
current-base blocker evidence, not a proof receipt.

## Narrow validation

All Lean checks reused the automation-provided symlink to the canonical pinned Lake artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch, network access, or `.lake`
mutation was performed. Compiled output was isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; recorded positive root remains open at `M4`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | `Statement.lean`, five diagnostic declarations in `ProofAudit.lean`, and conditional composition in `ObligationTree.lean` elaborated; three temporary oleans were produced. Every checked declaration reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry\|admit\|axiom)\\b\|sorryAx\|unsafe\|implemented_by\|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| Focused semantic search in pinned mathlib | 1, expected | No equimeasurability, symmetric-decreasing/Schwarz rearrangement, or Polya-Szego candidate occurs. |
| Same search over repository Lean sources, excluding this target | 0 | Only neighboring `THM-M-1285` statement, elementary profile lemmas, and conditional interfaces; no compatible terminal body. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/proof-recheck-2026-07-15-head-195f312e.json` | 0 | Structured current-base blocker is valid JSON. |
| `git diff --check` and no-index checks for this packet | 0 / 1, expected | No whitespace diagnostic; each no-index check reports the expected new-file difference. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is absent because the proof phase is blocked. |

Exact Lean replay, run from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-slot64.XXXXXX)
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

The generated olean sizes were 67,392, 100,776, and 77,176 bytes. Pinned inputs include
`Statement.lean` SHA-256 `ef428b6d...9bb`, `ProofAudit.lean` `09152048...47a9`,
`ObligationTree.lean` `31690c4c...4d6b`, and `lake-manifest.json` `321626c8...2d81`.

## Retry condition

Reopen `S56-M-1286-STATEMENT`, replace the ordinary Pi type with a measure-compatible Euclidean
`l2` encoding, and rerun statement identity/transports/mutations, anchor audit, registry, typed
graphs, and obligation-tree gates. Then implement both analytic packages without placeholders or
pin and exact-type-check an immutable compatible Lean 4 body.

## Status boundary

Lifecycle remains `planned`. The dossier's intake/README vector `[H2, M4, R3]` conflicts with the
typed graph's root `[H3, M4, R3]`; integration must reconcile that stale state and should consider
`M5` for the checked statement mismatch. No audit completion, validation, release, master
acceptance, or theorem completion is claimed.
