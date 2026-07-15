# THM-M-1286 proof refutation recheck at `43f55bb8`

Item: `S56-M-1286-PROOF`

Intent: `prove`

Recorded: `2026-07-15T17:42:44+08:00` (`Asia/Shanghai`)

Base revision: `43f55bb87aa8883be277a6660f49c6f8ba647082`

Base tree: `8e624c67ebaa9cd00a352276e1fca6d17c18e0b9`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen target. The tracked,
placeholder-free declaration

```lean
theorem Stage1Instances.THM_M_1286.Counterexample.not_polyaSzegoTarget :
    Not Stage1Instances.THM_M_1286.PolyaSzegoTarget
```

was replayed from source at this base with `lake env lean --trust=0 -t0`. Lean checked its exact
type and reported only `[propext, Classical.choice, Quot.sound]`. The assigned positive proof item
therefore remains `[ ]`; this packet is blocker evidence, not a proof receipt.

The refutation specializes the target to `n = p = 1`. Its input is `-log x` on `(0, 1)`, extended
by zero and transported to `Fin 1 -> Real`, with zero as the alleged weak gradient. The function is
nonnegative and integrable, and each positive superlevel has finite, strictly positive measure. In
the frozen API, `ContDiff Real top` is analytic rather than merely smooth. Analytic uniqueness
forces every compactly supported test function to vanish, so `HasWeakGradient` is vacuous. But a
pointwise real-valued `IsSymmetricDecreasing` witness is bounded above by its value at zero. Its
superlevel at `uStar 0 + 1` is empty, contradicting equimeasurability with the log spike.

This refutes the frozen Lean encoding, not a correctly formulated classical Polya-Szego theorem.
The encoding independently uses `Euclidean n := Fin n -> Real`, whose norm is the coordinate
supremum norm instead of Euclidean `l2`; `ProofAudit.lean` checks that fidelity defect. The positive
composition theorem `ObligationTree.exactTarget_of_packages` only consumes
`RearrangementConstruction` and `GradientEstimate`. Those premises cannot both be implemented in a
consistent environment because their checked composition would contradict the exact refutation.

The first failed gate is exact canonical target consistency. The actionable cut is the predecessor
`S56-M-1286-STATEMENT`, not the stale positive package cut. The prerequisite obligation-tree item
is also only worker-provisional (`[_]`), not master-accepted, so the assigned node is not yet
dependency-legal for master acceptance. This proof worker changes neither predecessor artifacts nor
authoritative state.

No Lean source, dependency lock, scheduler authority, or unrelated target was changed.
`.stage1-worker-selftest.json` is deliberately absent because the assigned positive proof phase is
not genuinely complete.

## Narrow validation

All checks ran in this worker clone. The automation-provided `Formalizations/Lean/.lake` symlink was
treated as read-only and reused the canonical pinned artifacts. Temporary Lean objects were written
only below `/tmp` and removed. No `lake update`, `lake build`, dependency clone/fetch, network
action, checkout repair, or dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed structurally; denominator `e586a1f...ddaa4`; the stale positive root is recorded open `M4`. |
| Isolated `lake env lean --trust=0 -t0` replay below | 0 | All four modules elaborated. `not_polyaSzegoTarget` has exact type `Not PolyaSzegoTarget`; the checked declarations report `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry\|admit\|axiom)\\b\|sorryAx\|unsafe\|implemented_by\|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean `4.29.0`, commit `98dc76e3...40`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib revision `8a178386...95`, tree `bdc39a31...b2b`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}` | 0 | Pinned dependency revision `56161b6e...a27`, tree `32c9eace...893`. |
| `git -C` both pinned packages `diff --quiet` | 0 | Both package worktrees remained unmodified. |
| `sha256sum` over the nine pinned inputs listed below | 0 | All digests matched the structured packet. |

Exact Lean replay from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-slot41-43f55bb8.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/Stage1_Instances/THM-M-1286"
cd "$ROOT/Formalizations/Lean"
LEAN_NUM_THREADS=1 timeout --foreground 300 lake env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/Stage1_Instances/THM-M-1286/Statement.olean" \
  ../../Stage1_Instances/THM-M-1286/Statement.lean
for src in Counterexample ProofAudit ObligationTree; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$TMP" timeout --foreground 300 \
    lake env lean --trust=0 -t0 -R ../.. \
    -o "$TMP/Stage1_Instances/THM-M-1286/$src.olean" \
    ../../Stage1_Instances/THM-M-1286/$src.lean
done
```

The generated olean sizes were 67,392 bytes for `Statement`, 218,384 for `Counterexample`,
100,776 for `ProofAudit`, and 77,176 for `ObligationTree`.

Pinned input SHA-256 values:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `ef428b6d6fbb5a05b9112291cd5e113ff02d58776a03b2765837bd3ddc2039bb` |
| `Counterexample.lean` | `dd227181174b72d4aafd614313499c35f6b930056879764b311a479f06f1f0a6` |
| `ProofAudit.lean` | `09152048ca2a69b790f9bd1ab8db0e8bf533d7d5873b05d571b64647a1b647a9` |
| `ObligationTree.lean` | `31690c4c88849ca069648df8cbc72aaec44ce139e83a9fabda1b5b26093a4d6b` |
| `obligation-registry.json` | `c7d331ee666db5ca093880b051d0959395d35735bb2c337dfd7d5c7a91215d20` |
| `typed-graphs.json` | `9c225e12b3cb6db6f264b360a5e7c6d418d837efe3214909d5cbd9a664a987e2` |
| `anchor-audit.json` | `f05ca7a660c1ba2d5ca1fa359cde5338eaded9355c84795294d1a48e745bd33c` |
| `validation-specs.json` | `2ee56fb5cadf7df96cc8d0ba96b6fbacec5cfc7861f2114a6608b444aec44e9a` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |

## Retry condition

Reopen `S56-M-1286-STATEMENT`: use measure-compatible Euclidean `l2` geometry, spell the intended
smooth order rather than `top`/analytic order, and choose a rearrangement representation that admits
essentially unbounded finite-`p` inputs. Publish a new statement fingerprint and refreeze every
dependent statement, anchor, registry, graph, and obligation-tree artifact before resuming positive
proof execution, or explicitly redirect this instance to the checked counterexample target.

## Status boundary

This is fresh current-base, target-scoped, nonrelease refutation evidence. It does not satisfy
`S56-M-1286-PROOF`, proposes no worker-provisional completion or scheduler state, and supports no
audit completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
