# THM-M-1286 proof-phase recheck at current base

Item: `S56-M-1286-PROOF`

Intent: `prove`

Date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `40801f373a9b0443cc58ff8ec365fb5b75c8b8c3`

Base tree: `f3b8367a9ec13bd00b783bc4367d64003ffcde28`

## Verdict

`blocked`. No unconditional proof body or compatible pinned import closes the exact root. More
fundamentally, proof execution found that the frozen Lean target is not faithful to the intake's
Euclidean Schwarz-rearrangement claim.

`Statement.lean` defines `Euclidean n` as the ordinary function type `Fin n -> Real`. Mathlib gives
that type the finite-product supremum norm. Therefore `IsSymmetricDecreasing` is radial-antitone in
the `l-infinity` metric, and `eLpNorm g` integrates the same supremum norm of the weak-gradient
vector. This differs from the intended Euclidean `l2` geometry. The new placeholder-free
`ProofAudit.lean` checks the norm formula, a concrete two-coordinate discrepancy, the exponent-one
energy formula, and the product/sup-metric ball-volume formula at trust level zero.

The mathematical risk is substantive, not cosmetic. For `n = 2`, `p = 1`, the diamond tent
`max(0, 1 - |x| - |y|)` has supremum-gradient energy `2`, while its equimeasurable
sup-radial-antitone cube tent has energy `2 * sqrt(2)`. This reverses the requested inequality.
That calculation is recorded only as blocker analysis: formalizing the complete counterexample
would itself require the currently absent weak-derivative, rearrangement-uniqueness, and sharp
energy packages. No kernel-checked `Not PolyaSzegoTarget` claim is made.

The earlier immediate positive cut set, `M1286-C-REARRANGE` and `M1286-L-GRADIENT`, also remains
unimplemented. `ObligationTree.exactTarget_of_packages` consumes those packages as assumptions and
is only conditional composition. No weaker, conditional, anisotropic, or differently encoded
theorem was substituted. The item remains `[ ]`; no self-test manifest is written.
The recorded debt vector remains `[H2, M4, R3]` because this proof worker does not edit authoritative
state; the integration lane should decide whether the explicit statement-mismatch diagnosis warrants
an `M5` reclassification when reopening the statement node.

## Validation

All completed checks ran in this worker clone against the existing pinned Lake artifacts. The
automation-provided `.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network access, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; planned hard-mathlib lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; the positive root remains open `M4` |
| Isolated trust-zero Lean recipe below | 0 | Exact statement and all five `ProofAudit` declarations elaborated; every audit declaration reports exactly `[propext, Classical.choice, Quot.sound]` |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|unsafe|implemented_by|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct in any owned Lean source |
| `rg -n -i 'rearrang\|equimeasur\|schwarz.*symm\|polya.?szego\|pólya.?szegő' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Finite-sum rearrangement and unrelated textual hits only; no Schwarz rearrangement or compatible terminal body |
| `rg -n -i 'rearrang\|equimeasur\|schwarz.*symm\|polya.?szego\|pólya.?szegő' Stage1_Instances Formalizations/Lean/AwesomeTheorems --glob '*.lean' --glob '!Stage1_Instances/THM-M-1286/**'` | 0 | THM-M-1285 statement/interfaces and an unrelated conditional spherical contract; no compatible terminal body |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/proof-recheck-2026-07-14-head-40801f37.json` | 0 | Structured current-base blocker is valid JSON |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1286/ProofAudit.lean` | 1, expected | Untracked file differs from `/dev/null`; no whitespace diagnostics |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1286/proof-recheck-2026-07-14-head-40801f37.json` | 1, expected | Untracked file differs from `/dev/null`; no whitespace diagnostics |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1286/proof-recheck-2026-07-14-head-40801f37.md` | 1, expected | Untracked file differs from `/dev/null`; no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent |

The exact Lean recipe writes all compiled output to a disposable directory:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-audit.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN_ROOT="$ROOT/Formalizations/Lean"
BASE=$(cd "$LEAN_ROOT" && lake env printenv LEAN_PATH)
LEAN=$(cd "$LEAN_ROOT" && lake env which lean)
mkdir -p "$TMP/Stage1_Instances/THM-M-1286"
cp Stage1_Instances/THM-M-1286/Statement.lean \
  "$TMP/Stage1_Instances/THM-M-1286/Statement.lean"
cp Stage1_Instances/THM-M-1286/ProofAudit.lean "$TMP/ProofAudit.lean"
cd "$TMP"
LEAN_PATH="$BASE" "$LEAN" --trust=0 -t0 -R "$TMP" \
  -o "$TMP/Stage1_Instances/THM-M-1286/Statement.olean" \
  "$TMP/Stage1_Instances/THM-M-1286/Statement.lean"
LEAN_PATH="$TMP:$BASE" "$LEAN" --trust=0 -t0 -R "$TMP" \
  -o "$TMP/ProofAudit.olean" "$TMP/ProofAudit.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry Condition

The first failed gate is exact canonical statement fidelity. Reopen `S56-M-1286-STATEMENT`, replace
the ordinary Pi type with a measure-compatible Euclidean `l2` encoding, and rerun statement,
transport, mutation, anchor, registry, and obligation-tree gates. Only then resume the missing
rearrangement-construction and gradient-estimate formalization, or integrate an immutable compatible
Lean 4 proof without changing the dependency lock.

This packet is proof-phase blocker evidence, not a proof receipt. It does not satisfy the assigned
proof item or claim audit completion, validation, release, master acceptance, or theorem completion.
