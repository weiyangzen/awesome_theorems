# THM-M-1286 proof-phase recheck at current base

Item: `S56-M-1286-PROOF`

Date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `ed9e08c4aa5d18cb58fa54e74867f38999a92a14`

Base tree: `41384c2a54f3f02cffd5aa5c92555706fc748659`

## Verdict

`blocked`. There is no unconditional proof body or compatible pinned import for the exact frozen
root. More fundamentally, the statement does not encode the Euclidean Schwarz-rearrangement claim
selected by intake.

`Statement.lean` abbreviates `Euclidean n` as the ordinary function type `Fin n -> Real`. Mathlib
gives that type the finite-product supremum norm. Consequently `IsSymmetricDecreasing` is radial in
the `l-infinity` metric, metric balls are cubes, and `eLpNorm g` integrates the supremum norm of the
weak-gradient vector. The intended Polya-Szego inequality instead uses Euclidean `l2` geometry.

The placeholder-free `ProofAudit.lean` checks this mismatch in the pinned kernel: it proves the
finite-Pi norm formula, computes norm one for coordinates `(1,-1)`, computes squared norm two for
the same coordinates in `EuclideanSpace`, exposes the exponent-one gradient-energy integrand, and
checks the product/sup-metric ball-volume formula. Every diagnostic declaration elaborated at trust
level zero with exactly `propext`, `Classical.choice`, and `Quot.sound` in its axiom report.

This mismatch is substantive. For `n = 2`, `p = 1`, the diamond tent
`max(0, 1 - |x| - |y|)` has supremum-gradient energy `2`, while its equimeasurable sup-radial cube
tent has energy `2 * sqrt(2)`, reversing the requested direction. That calculation is blocker
analysis, not a formal refutation: no kernel-checked `Not PolyaSzegoTarget` is claimed.

Even after statement repair, the prior positive cut set remains open. The local theorem
`ObligationTree.exactTarget_of_packages` merely composes `RearrangementConstruction` and
`GradientEstimate` premises into the root; it proves neither premise. No weaker, conditional,
anisotropic, or differently encoded theorem was substituted.

The recorded vector remains `[H2, M4, R3]` because this worker does not edit authoritative state.
The integration lane should reopen `S56-M-1286-STATEMENT` and decide whether the mismatch warrants
`M5`. The proof item remains `[ ]`, and `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All checks used the existing pinned Lake closure read-only. No `lake update`, `lake build`,
dependency clone/fetch, network operation, or `.lake` mutation was performed. Lean output went to
disposable directories under `/tmp` and was removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | `PASS`: 18 obligations and 23 typed edges; denominator `e586a1f...ddaa4`; recorded positive root open `M4` |
| Isolated trust-zero Lean replay below | 0 | Statement, conditional composition, and five diagnostic bodies elaborated; every printed axiom set was `[propext, Classical.choice, Quot.sound]` |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|unsafe\|implemented_by\|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct in any owned Lean source |
| Scoped candidate searches in pinned mathlib and repository Lean sources | 0 | Finite-sum rearrangement, THM-M-1285 interfaces, and an unrelated spherical contract only; no compatible terminal proof body |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/proof-recheck-2026-07-14-head-ed9e08c4.json >/dev/null` | 0 | This fresh structured blocker is valid JSON |
| Scoped `git diff --check` plus no-index checks for both new files | 0 | No whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent |

Exact Lean replay, run from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-slot64.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN_ROOT="$ROOT/Formalizations/Lean"
BASE=$(cd "$LEAN_ROOT" && lake env printenv LEAN_PATH)
LEAN=$(cd "$LEAN_ROOT" && lake env which lean)
mkdir -p "$TMP/Stage1_Instances/THM-M-1286"
cp Stage1_Instances/THM-M-1286/Statement.lean \
  "$TMP/Stage1_Instances/THM-M-1286/Statement.lean"
cp Stage1_Instances/THM-M-1286/ObligationTree.lean "$TMP/ObligationTree.lean"
cp Stage1_Instances/THM-M-1286/ProofAudit.lean "$TMP/ProofAudit.lean"
cd "$TMP"
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE" "$LEAN" --trust=0 -t0 -R "$TMP" \
  -o "$TMP/Stage1_Instances/THM-M-1286/Statement.olean" \
  "$TMP/Stage1_Instances/THM-M-1286/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" "$LEAN" --trust=0 -t0 -R "$TMP" \
  -o "$TMP/ObligationTree.olean" "$TMP/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" "$LEAN" --trust=0 -t0 -R "$TMP" \
  -o "$TMP/ProofAudit.olean" "$TMP/ProofAudit.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry Condition

Reopen `S56-M-1286-STATEMENT`, replace the ordinary Pi type with a measure-compatible Euclidean
`l2` encoding, and rerun exact target identity, transport, mutation, anchor, registry, and
obligation-tree gates. Then implement both analytic packages without placeholders or integrate an
immutable compatible Lean 4 proof.

This packet is fresh proof-phase blocker evidence, not a proof receipt. It does not satisfy the
assigned proof item or claim audit completion, theorem completion, validation, release, independent
verification, or master acceptance.
