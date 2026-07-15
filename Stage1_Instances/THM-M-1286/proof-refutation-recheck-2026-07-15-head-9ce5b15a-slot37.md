# THM-M-1286 proof-phase refutation recheck at `9ce5b15a`

Item: `S56-M-1286-PROOF`

Worker: Stage1 rev-5.6 slot37

Recorded: `2026-07-15T21:52:51+08:00` (`Asia/Shanghai`)

Base revision: `9ce5b15aaeafda7308c5b4d7b0eae998ab633650`

Base tree: `74e115f8418e0cbb135a1b0be01fb72c63904ba4`

Verdict: `blocked`

State: `[ ]`

Lifecycle: `planned -> planned`

Proof phase complete: `false`

Audit complete: `false`

Theorem complete: `false`

## Result

No positive proof body can truthfully be implemented for the exact frozen target. A fresh,
offline, trust-zero Lean replay checks the existing placeholder-free declaration
`Stage1Instances.THM_M_1286.Counterexample.not_polyaSzegoTarget` at exact type
`Not Stage1Instances.THM_M_1286.PolyaSzegoTarget`. Lean reports only `propext`,
`Classical.choice`, and `Quot.sound` for that refutation.

The checked counterexample specializes the target to `n = p = 1`, the nonnegative integrable
function `-log x` on `(0, 1)` transported to `Fin 1 -> Real`, and the zero gradient. In the frozen
predicate, `ContDiff Real top` denotes analytic regularity. Analytic uniqueness makes every
compactly supported test function zero, so `HasWeakGradient` is vacuous. Every positive
superlevel of the input nevertheless has positive finite measure. A pointwise real-valued
radial-antitone witness is bounded above by its value at zero, so its superlevel at
`uStar 0 + 1` is empty. Equimeasurability then contradicts the input's strictly positive
superlevel measure.

This refutes only the frozen Lean encoding, not a correctly formulated classical Polya-Szego
inequality. `ProofAudit.lean` independently checks a third encoding defect: the abbreviation
`Euclidean n := Fin n -> Real` carries the coordinate supremum norm rather than Euclidean `l2`.
The conditional declaration `ObligationTree.exactTarget_of_packages` assumes both positive proof
packages. Those premises cannot both be implemented in a consistent environment because their
composition would contradict the checked negation.

The first failed gate is exact canonical target consistency. The remaining actionable cut is the
predecessor `S56-M-1286-STATEMENT`, which must be repaired and refrozen before positive proof
execution. The assigned item's immediate prerequisite, `S56-M-1286-OBLIGATION_TREE`, remains only
worker-provisional `[_]`, not master-accepted, and its positive architecture is stale.

Since the preceding target packet at base `e6872c19`, no semantic target input, Lean source,
registry, graph, anchor audit, validation specification, toolchain file, or dependency lock has
changed. Current `HEAD` only integrates that preceding blocker packet under this target while
Blueprint/DAG authority advances. The proof item remains `[ ]`.

No Lean source, dependency lock, scheduler authority, or unrelated target was changed.
`.stage1-worker-selftest.json` is deliberately absent because the assigned positive proof phase is
not genuinely complete.

## Narrow Validation

All checks ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. Temporary
Lean objects were written only below `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch, checkout repair, network action, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; the stale positive root remains open `M4`. |
| Isolated `lake --offline env lean --trust=0 -t0` replay below | 0 | All four modules elaborated. `not_polyaSzegoTarget` has exact type `Not PolyaSzegoTarget`; inspected declarations report `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry\|admit\|axiom)\\b\|sorryAx\|unsafe\|implemented_by\|native_decide\|\\bextern\\b' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean `4.29.0`, commit `98dc76e3...740`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib revision `8a178386...e95`, tree `bdc39a31...b2b`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}` | 0 | Pinned dependency revision `56161b6e...a27`, tree `32c9eac...893`. |
| `git -C` both pinned packages `status --short` | 0 | Both package worktrees remained unmodified and clean. |
| `sha256sum` over the fourteen pinned/normative inputs listed in the JSON packet | 0 | All digests matched `source_hashes`. |
| `git diff --name-status e6872c19..HEAD` over the ten semantic target/toolchain inputs | 0 | No semantic input changed. |
| `python3 -m json.tool` plus target-scoped assertions on the adjacent JSON packet | 0 | The packet is valid JSON; all item, base, ownership, hash, refutation, blocked-state, dependency, and absent-self-test invariants passed. |
| Scoped `git diff --check`, plus no-index checks for both new packet files | 0 / 1 expected | No whitespace diagnostics; each no-index check returned only the expected new-file difference status. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test is absent because the proof phase is blocked. |

Exact Lean replay from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-slot37-9ce5b15a.XXXXXX)
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

## Retry Condition

Reopen `S56-M-1286-STATEMENT`: use measure-compatible Euclidean `l2` geometry, replace the outer
`top` analytic order with the intended smooth test class, and choose a rearrangement representation
that admits essentially unbounded finite-`p` inputs. Publish a new statement fingerprint and
refreeze every dependent statement, anchor, registry, graph, and obligation-tree artifact before
resuming positive proof execution, or explicitly redirect this instance to the checked
counterexample target.

## Status Boundary

This is fresh current-base, target-scoped, nonrelease refutation evidence. It does not satisfy
`S56-M-1286-PROOF`, proposes no worker-provisional completion or scheduler state, and supports no
audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance.
