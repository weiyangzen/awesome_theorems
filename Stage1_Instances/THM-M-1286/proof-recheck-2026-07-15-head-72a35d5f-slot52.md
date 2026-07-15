# THM-M-1286 proof-phase recheck at current base

Item: `S56-M-1286-PROOF`

Intent: `prove`

Recorded: `2026-07-15T08:20:46+08:00` (`Asia/Shanghai`)

Base revision: `72a35d5f64e32233c0bc77a57e47bd078475ad74`

Base tree: `a80eb91ed5629dee62d031e78bc87b509cf8e6eb`

## Verdict

`blocked`. No unconditional proof body can truthfully be added for the current canonical target.
The first failed gate is exact statement fidelity, before either open analytic package can receive
proof credit.

`Statement.lean` defines `Euclidean n` as the ordinary Pi type `Fin n -> Real`. Its installed norm
is the finite-product supremum norm, rather than the Euclidean `l2` norm in the intake's classical
Schwarz-rearrangement claim. Therefore `IsSymmetricDecreasing` is radial-antitone in `l-infinity`
geometry, and the vector-valued weak-gradient energy also uses the supremum norm.
`ProofAudit.lean` supplies placeholder-free kernel certificates for the Pi norm formula, the norm
discrepancy at coordinates `(1, -1)`, the exponent-one energy integrand, and the product/cube ball
volume formula.

This is a mathematical encoding mismatch, not a notation issue. Prior analysis gives an `n = 2`,
`p = 1` diamond-tent calculation whose input supremum-gradient energy is `2`, while its expected
equimeasurable sup-radial cube tent has energy `2 * sqrt 2`, reversing the frozen inequality.
Formalizing the representative's uniqueness is itself missing work, so this calculation is blocker
analysis rather than a kernel proof of `Not PolyaSzegoTarget`.

The positive proof architecture is also open. The checked body
`ObligationTree.exactTarget_of_packages` assumes `RearrangementConstruction` and
`GradientEstimate`; it implements neither premise. A focused search found no compatible terminal
body in pinned mathlib. The adjacent THM-M-1285 target now has a placeholder-free Schwarz
construction, but its correctly typed Euclidean-space witness does not supply the weak-gradient
estimate, and its proposition cannot close this differently typed target. No weaker, conditional,
anisotropic, quadratic-only, or differently typed theorem was substituted.

The assigned item remains `[ ]`. No proof source or `.stage1-worker-selftest.json` was written.
This packet is current-base blocker evidence, not a proof receipt.

## Narrow validation

All Lean checks reused the automation-provided pinned Lake artifacts read-only. No `lake update`,
`lake build`, dependency clone/fetch, network access, or `.lake` mutation was performed. Compiled
output was isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; the recorded root remains open at `M4`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | `Statement.lean`, five diagnostic bodies in `ProofAudit.lean`, and conditional composition in `ObligationTree.lean` elaborated; olean sizes were 67392, 100776, and 77176 bytes. All six checked declarations reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry\|admit\|axiom)\\b\|sorryAx\|unsafe\|implemented_by\|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| Focused semantic search in pinned mathlib and repository Lean sources | 1 / 0 | No pinned-mathlib body; the repository search found THM-M-1285's differently typed construction but no compatible gradient estimate or terminal body. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `sha256sum` over the eight pinned inputs named below | 0 | Every digest matched the structured packet. |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/proof-recheck-2026-07-15-head-72a35d5f-slot52.json` | 0 | The current-base structured blocker is valid JSON. |
| `git diff --check` plus `git diff --no-index --check /dev/null` for both new packet files | 0 / 1, expected | No whitespace diagnostics; no-index returned difference status for each new file. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test is absent because the proof phase is blocked. |

Exact Lean replay from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-slot52-72a35d5f.XXXXXX)
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

Pinned input SHA-256 values:

- `Statement.lean`: `ef428b6d6fbb5a05b9112291cd5e113ff02d58776a03b2765837bd3ddc2039bb`
- `ProofAudit.lean`: `09152048ca2a69b790f9bd1ab8db0e8bf533d7d5873b05d571b64647a1b647a9`
- `ObligationTree.lean`: `31690c4c88849ca069648df8cbc72aaec44ce139e83a9fabda1b5b26093a4d6b`
- `obligation-registry.json`: `c7d331ee666db5ca093880b051d0959395d35735bb2c337dfd7d5c7a91215d20`
- `typed-graphs.json`: `9c225e12b3cb6db6f264b360a5e7c6d418d837efe3214909d5cbd9a664a987e2`
- `anchor-audit.json`: `f05ca7a660c1ba2d5ca1fa359cde5338eaded9355c84795294d1a48e745bd33c`
- `validation-specs.json`: `2ee56fb5cadf7df96cc8d0ba96b6fbacec5cfc7861f2114a6608b444aec44e9a`
- `Formalizations/Lean/lake-manifest.json`: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`

## Retry condition

Reopen `S56-M-1286-STATEMENT`, replace the ordinary Pi type with a measure-compatible Euclidean
`l2` encoding, and rerun statement identity/transports/mutations, anchor audit, registry, typed
graphs, and obligation-tree gates. Then implement both analytic packages without placeholders, or
pin and exact-type-check an immutable compatible Lean 4 body.

## Status boundary

Lifecycle remains `planned`, and the root vector remains `[H2, M4, R3]` in the intake/README. The
typed graph records stale `H3`, and the checked mismatch warrants integration review of an `M5`
classification; this proof worker changes neither authority. No audit completion, proof-phase
completion, validation, release, master acceptance, or theorem completion is claimed.
