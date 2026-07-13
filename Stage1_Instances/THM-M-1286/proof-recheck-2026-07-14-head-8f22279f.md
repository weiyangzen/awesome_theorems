# THM-M-1286 proof-phase recheck at current base

Item: `S56-M-1286-PROOF`

Intent: `prove`

Date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `8f22279fd1216cdfb5676c758e6bdb08e0ba3e01`

Base tree: `d2e9e68da52ecfcfe15a9c48ac2262400e602667`

## Verdict

`blocked`. This current-base replay confirms that no unconditional proof body or compatible pinned
import closes `Stage1Instances.THM_M_1286.PolyaSzegoTarget`. More importantly, the prerequisite
statement is not faithful to the intake's Euclidean Schwarz-rearrangement claim.

`Statement.lean` abbreviates `Euclidean n` as the ordinary Pi type `Fin n -> Real`. Its norm is the
coordinate supremum norm, not the intended Euclidean `l2` norm. Consequently both radial
monotonicity and the weak-gradient `eLpNorm` comparison use `l-infinity` geometry. The existing
placeholder-free `ProofAudit.lean` establishes this mismatch with five kernel-checked declarations:
the Pi norm formula, a two-coordinate norm discrepancy, the exponent-one energy formula, and the
product/sup-metric ball-volume formula.

`ObligationTree.exactTarget_of_packages` remains conditional on `RearrangementConstruction` and
`GradientEstimate`; it supplies neither premise and therefore is not a root proof. The positive
architecture checker still reports both packages open at `M4`, and repository/pinned-mathlib search
still finds no compatible terminal body. No weaker, conditional, anisotropic, or differently typed
theorem was substituted.

The item remains `[ ]`. This packet records a repeated hard blocker at a fresh immutable base; it is
not completion evidence. Because the proof phase is not self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All checks ran in this worker clone using the existing pinned Lake artifacts. The automation-provided
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency clone/fetch, network
access, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; planned hard-mathlib lane; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; root remains open `M4` |
| Isolated trust-zero Lean recipe below | 0 | `Statement.lean`, all five `ProofAudit` declarations, and conditional composition elaborated; axiom reports were exactly `[propext, Classical.choice, Quot.sound]` |
| `rg -n --pcre2 '\\b(?:sorry\|admit\|axiom)\\b\|sorryAx\|unsafe\|implemented_by\|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct in owned Lean source |
| `rg -n -i 'rearrang\|equimeasur\|schwarz.*symm\|polya.?szego\|pólya.?szegő' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Only finite-sum rearrangement and unrelated textual hits; no compatible Schwarz-rearrangement body |
| Same search over `Stage1_Instances` and `Formalizations/Lean/AwesomeTheorems`, excluding this target | 0 | THM-M-1285 statement/interfaces and an unrelated conditional spherical contract only |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/proof-recheck-2026-07-14-head-8f22279f.json` | 0 | Structured current-base blocker is valid JSON |
| `git diff --no-index --check /dev/null` against each new packet file | 1, expected | Both files differ from `/dev/null`; neither command emitted a whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent because the proof phase is blocked |

The exact Lean replay wrote all compiled output to a disposable `/tmp` directory:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-current.XXXXXX)
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
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry Condition

Reopen `S56-M-1286-STATEMENT`, replace the ordinary Pi type with a measure-compatible Euclidean
`l2` encoding, and rerun statement, transport, mutation, anchor, registry, and obligation-tree
gates. Only after that correction should proof work implement the rearrangement-construction and
gradient-estimate packages without placeholders, or pin an immutable compatible Lean 4 proof.

This is proof-phase blocker evidence, not a proof receipt. It does not satisfy the assigned proof
item or claim audit completion, validation, release, master acceptance, or theorem completion.
