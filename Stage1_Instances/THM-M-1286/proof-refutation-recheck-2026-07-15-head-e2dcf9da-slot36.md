# THM-M-1286 proof-phase refutation recheck at `e2dcf9da`

Item: `S56-M-1286-PROOF`

Worker: Stage1 rev-5.6 slot36

Base revision: `e2dcf9dac5876bb5b659eb8185d8de16d53b3ff4`

Base tree: `62cdca59e6cd4e6cccbe8cfafdeb54d3874052ac`

Verdict: `blocked`

State: `[ ]`

Lifecycle: `planned -> planned`

Proof phase complete: `false`

Audit complete: `false`

Theorem complete: `false`

## Result

No positive proof body can truthfully be implemented for the frozen target. A current-base,
offline, trust-zero Lean replay checks
`Stage1Instances.THM_M_1286.Counterexample.not_polyaSzegoTarget` at exact type
`Not Stage1Instances.THM_M_1286.PolyaSzegoTarget`. Lean reports only `propext`,
`Classical.choice`, and `Quot.sound` for that declaration.

The checked counterexample takes `n = p = 1`, the nonnegative integrable function `-log x` on
`(0, 1)` transported to `Fin 1 -> Real`, and the zero gradient. In the frozen predicate,
`ContDiff Real top` denotes analytic regularity. Analytic uniqueness makes every compactly
supported test function zero, so `HasWeakGradient` is vacuous. Every positive superlevel of the
input has positive finite measure. A pointwise real-valued symmetric-decreasing witness, however,
is bounded above by its value at zero, making its superlevel at `uStar 0 + 1` empty. This
contradicts equimeasurability.

This refutes the frozen Lean encoding, not a correctly formulated classical Polya-Szego theorem.
`ProofAudit.lean` separately checks that the frozen `Euclidean n := Fin n -> Real` uses the
coordinate supremum norm rather than Euclidean `l2`. The conditional theorem
`ObligationTree.exactTarget_of_packages` assumes both positive proof packages. Those premises
cannot both be implemented in a consistent environment because their composition would contradict
the checked negation.

The first failed gate is exact canonical target consistency. The remaining cut is the predecessor
`S56-M-1286-STATEMENT`, which must be repaired and refrozen before positive proof execution. The
assigned item's obligation-tree prerequisite remains worker-provisional `[_]`, not master-accepted.
No predecessor artifact or authoritative state is changed here.

Since the prior slot36 packet at base `6ee4e043`, no semantic target input, Lean source, registry,
graph, anchor audit, validation specification, toolchain, or dependency lock has changed. The prior
packet was integrated and the Blueprint/DAG authority advanced, but the predecessor remains `[_]`
and this item remains `[ ]`.

No Lean source, dependency lock, scheduler authority, or unrelated target was changed.
`.stage1-worker-selftest.json` is deliberately absent because the assigned positive proof phase is
not genuinely complete.

## Narrow Validation

All checks ran in this worker clone. The automation-provided `Formalizations/Lean/.lake` link was
reused read-only. Temporary Lean objects were written only below `/tmp` and removed. No `lake
update`, `lake build`, dependency clone/fetch, checkout repair, network action, or `.lake` mutation
was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; the stale positive root remains open `M4`. |
| Isolated `lake --offline env lean --trust=0 -t0` replay below | 0 | All four modules elaborated. `not_polyaSzegoTarget` has exact type `Not PolyaSzegoTarget`; inspected declarations report `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|unsafe|implemented_by|native_decide|\\bextern\\b' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean `4.29.0`, commit `98dc76e3...40`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib revision `8a178386...95`, tree `bdc39a31...b2b`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}` | 0 | Pinned dependency revision `56161b6e...a27`, tree `32c9eace...893`. |
| `git -C` both pinned packages `diff --quiet` | 0 | Both package worktrees remained unmodified. |
| `sha256sum` over the ten pinned inputs listed below | 0 | All digests matched the structured packet. |
| `git diff --name-status 6ee4e043..HEAD` over semantic target inputs | 0 | No semantic target input changed; only the earlier slot36 blocker pair was added under this target, while Blueprint/DAG authority advanced. |
| `python3 -m json.tool` plus target-scoped assertions on the structured packet | 0 | JSON and item/base/ownership/refutation/state/self-test invariants passed. |
| Scoped `git diff --check`, plus no-index checks for both new packet files | 0 / 1 expected | No whitespace diagnostics; each no-index check returned only the expected new-file difference status. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test is absent because the proof phase is blocked. |

Exact Lean replay from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-slot36-e2dcf9dac.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/Stage1_Instances/THM-M-1286"
cd "$ROOT/Formalizations/Lean"
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s \
  lake --offline env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/Stage1_Instances/THM-M-1286/Statement.olean" \
  ../../Stage1_Instances/THM-M-1286/Statement.lean
for src in Counterexample ProofAudit ObligationTree; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$TMP" timeout --foreground --kill-after=5s 300s \
    lake --offline env lean --trust=0 -t0 -R ../.. \
    -o "$TMP/Stage1_Instances/THM-M-1286/$src.olean" \
    "../../Stage1_Instances/THM-M-1286/$src.lean"
done
```

The generated olean sizes and SHA-256 values were:

| Module | Bytes | SHA-256 |
|---|---:|---|
| `Statement` | 67,392 | `3e7524cff9894071eac21c8dfcf6a8437663d4dfba5edbc52b8747075bb10c0b` |
| `Counterexample` | 218,384 | `7d1b1dc2c45dfd3817979900e72c5389b33e481f1e27b24fcfe982e20f1ca9c1` |
| `ProofAudit` | 100,776 | `320fb198abc6bd4b9ed89f5706f40a38912b5e9cdf5405b84444a53f946a0b5c` |
| `ObligationTree` | 77,176 | `f8ac6ed41d32adb97136a09d7a5f3f0009bdc7c0dc1c6ddef2cba163c463aa86` |

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
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |

## Retry Condition

Reopen `S56-M-1286-STATEMENT`: use measure-compatible Euclidean `l2` geometry, replace the outer
`top`/analytic order with scoped `∞` for the intended smooth class, and choose a rearrangement
representation that admits essentially unbounded finite-`p` inputs. Publish a new statement
fingerprint and refreeze every dependent statement, anchor, registry, graph, and obligation-tree
artifact before resuming positive proof execution, or explicitly redirect this instance to the
checked counterexample target.

## Status Boundary

This is fresh current-base, target-scoped, nonrelease refutation evidence. It does not satisfy
`S56-M-1286-PROOF`, proposes no worker-provisional completion or scheduler state, and supports no
audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance.
