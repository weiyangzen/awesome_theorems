# THM-M-1286 proof-phase recheck at current base

Item: `S56-M-1286-PROOF`

Intent: `prove`

Date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `18ff7447208231633bf2e01e8aad3111af56531a`

Base tree: `9ea9aab30253e72b62ef25c80e17b575356fb7b6`

## Verdict

`blocked`. The assigned proof phase cannot truthfully implement a proof body for the current
canonical target. Its prerequisite statement is not faithful to the intake's Euclidean
Schwarz-rearrangement claim.

`Statement.lean` defines `Euclidean n` as the ordinary function type `Fin n -> Real`. Mathlib equips
this type with the finite-product supremum norm, rather than the intended Euclidean `l2` norm.
Consequently `IsSymmetricDecreasing` is radial-antitone in `l-infinity` geometry and `eLpNorm g`
also integrates the supremum norm of gradient values. The existing placeholder-free
`ProofAudit.lean` supplies five kernel-checked diagnostic declarations: the Pi norm formula, a
two-coordinate discrepancy with `EuclideanSpace`, the exponent-one gradient-energy formula, and
the product/sup-metric ball-volume formula.

The positive proof architecture remains open independently of that mismatch.
`ObligationTree.exactTarget_of_packages` is conditional composition: it assumes both
`RearrangementConstruction` and `GradientEstimate`, so it implements neither analytic package and
does not close the root. Focused searches again found no compatible proof body in the repository or
the pinned mathlib revision. No weaker, conditional, anisotropic, quadratic-only, or differently
typed theorem was substituted.

The mismatch is mathematically substantive. At `n = 2`, `p = 1`, the diamond tent
`max(0, 1 - |x| - |y|)` is expected to have supremum-gradient energy `2`, while its
equimeasurable sup-radial cube tent has energy `2 * sqrt(2)`. This reverses the frozen inequality.
That calculation is blocker analysis only: a complete Lean refutation would itself require the
currently absent weak-derivative, rearrangement-uniqueness, and sharp integration infrastructure.
No kernel-checked `Not PolyaSzegoTarget` claim is made.

The first failed gate is exact canonical statement fidelity. Reopen `S56-M-1286-STATEMENT`, use a
measure-compatible Euclidean `l2` encoding, then rerun the statement transport/mutations, anchor
audit, obligation registry, typed graphs, and obligation-tree checks. Only after those dependent
artifacts are refrozen can proof work resume on the rearrangement construction and gradient
estimate, or integrate an immutable compatible Lean 4 proof.

The assigned item remains `[ ]`. This packet is durable blocker evidence, not a proof receipt. The
proof phase is not complete, so `.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation

All checks ran in this worker clone using the automation-provided read-only symlink to the canonical
pinned Lake artifacts. No `lake update`, `lake build`, dependency clone/fetch, network access, or
`.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; `planned`; hard-mathlib lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; positive root open at `M4`. |
| Isolated trust-zero Lean recipe below | 0 | `Statement.lean`, all five `ProofAudit` declarations, and conditional composition elaborated; three temporary oleans were produced. All six checked declarations reported exactly `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|unsafe|implemented_by|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| `rg -n -i 'equimeasur|symmetric.?decreasing.?rearrang|schwarz.?symm|schwarz.?rearrang|polya.?szego|pólya.?szegő' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1, expected | No semantic candidate in pinned mathlib. |
| `rg -n -i 'equimeasur|symmetric.?decreasing.?rearrang|schwarz.?symm|schwarz.?rearrang|polya.?szego|pólya.?szegő' Stage1_Instances Formalizations/Lean/AwesomeTheorems --glob '*.lean' --glob '!Stage1_Instances/THM-M-1286/**'` | 0 | Only neighboring `THM-M-1285` statement and conditional interfaces; no compatible terminal body. |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/proof-recheck-2026-07-14-head-18ff7447.json` | 0 | Structured current-base blocker is valid JSON. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1286/proof-recheck-2026-07-14-head-18ff7447.json` | 1, expected | The untracked JSON differs from `/dev/null`; no whitespace diagnostic. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1286/proof-recheck-2026-07-14-head-18ff7447.md` | 1, expected | The untracked Markdown differs from `/dev/null`; no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent because proof execution is blocked. |

The Lean replay wrote all compilation output to a disposable `/tmp` directory:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-head18ff7447.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN_ROOT="$ROOT/Formalizations/Lean"
BASE=$(cd "$LEAN_ROOT" && lake env printenv LEAN_PATH)
LEAN=$(cd "$LEAN_ROOT" && lake env which lean)
mkdir -p "$TMP/Stage1_Instances/THM-M-1286"
cp Stage1_Instances/THM-M-1286/Statement.lean \
  "$TMP/Stage1_Instances/THM-M-1286/Statement.lean"
cp Stage1_Instances/THM-M-1286/ProofAudit.lean "$TMP/ProofAudit.lean"
cp Stage1_Instances/THM-M-1286/ObligationTree.lean "$TMP/ObligationTree.lean"
cd "$TMP"
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE" timeout 180 "$LEAN" --trust=0 -t0 -R "$TMP" \
  -o "$TMP/Stage1_Instances/THM-M-1286/Statement.olean" \
  "$TMP/Stage1_Instances/THM-M-1286/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" timeout 180 "$LEAN" --trust=0 -t0 -R "$TMP" \
  -o "$TMP/ProofAudit.olean" "$TMP/ProofAudit.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" timeout 180 "$LEAN" --trust=0 -t0 -R "$TMP" \
  -o "$TMP/ObligationTree.olean" "$TMP/ObligationTree.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`); `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Status boundary

Lifecycle remains `planned`, and workers do not edit authoritative state. The intake and README
record `[H2, M4, R3]`, while the later typed graph records root human debt `H3`; this stale `H2/H3`
conflict also requires integration reconciliation. Integration review should reclassify the stale
`M4` candidate as `M5` for the demonstrated statement mismatch and reopen the statement node. No
audit completion, validation, release, master acceptance, or theorem completion is claimed.
