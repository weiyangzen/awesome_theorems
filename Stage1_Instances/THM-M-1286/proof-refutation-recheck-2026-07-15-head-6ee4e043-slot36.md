# THM-M-1286 proof-phase refutation recheck at `6ee4e043`

Item: `S56-M-1286-PROOF`

Worker: Stage1 rev-5.6 slot36

Base revision: `6ee4e043011799c8a8d6f7f5a2b68dd5fb819679`

Base tree: `8e7811b64a8ad5298ec20aa3f40898f299dce655`

Verdict: `blocked`

State: `[ ]`

Lifecycle: `planned -> planned`

Proof phase complete: `false`

Audit complete: `false`

Theorem complete: `false`

## Result

No positive proof body can truthfully be implemented for the frozen target. A current-base,
trust-zero Lean replay checks
`Stage1Instances.THM_M_1286.Counterexample.not_polyaSzegoTarget` at exact type
`Not Stage1Instances.THM_M_1286.PolyaSzegoTarget`. Its machine-reported axioms are only `propext`,
`Classical.choice`, and `Quot.sound`.

The checked counterexample takes `n = p = 1`, the nonnegative integrable function `-log x` on
`(0, 1)` transported to `Fin 1 -> Real`, and the zero gradient. In the frozen predicate,
`ContDiff Real top` is analytic regularity. Analytic uniqueness makes every compactly supported test
function zero, so `HasWeakGradient` is vacuous. Every positive superlevel of the input has positive
finite measure. By contrast, a pointwise real-valued symmetric-decreasing witness is bounded above
by its value at zero, making its superlevel at `uStar 0 + 1` empty. This contradicts
equimeasurability.

This refutes the frozen Lean encoding, not the correctly formulated classical Polya-Szego theorem.
`ProofAudit.lean` independently checks that the frozen `Euclidean n := Fin n -> Real` uses the
coordinate supremum norm instead of Euclidean `l2`. The conditional theorem
`ObligationTree.exactTarget_of_packages` merely assumes both positive analytic packages. Those
premises cannot both be implemented consistently because their composition would contradict the
checked negation.

The first failed gate is exact canonical target consistency. The remaining cut is the predecessor
`S56-M-1286-STATEMENT`, which must be repaired and refrozen before positive proof work resumes. The
assigned proof item's obligation-tree prerequisite also remains worker-provisional `[_]`, not
master-accepted. No predecessor artifact or authoritative state is changed here.

Since the prior slot36 packet at base `69f012f9`, no semantic target input, Lean source, registry,
graph, anchor audit, validation specification, toolchain, or dependency lock has changed. Prior
blocker evidence was integrated and Blueprint/DAG authority advanced, but the predecessor remains
`[_]` and this item remains `[ ]`.

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
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; positive root remains open `M4`. |
| Isolated `lake --offline env lean --trust=0 -t0` replay below | 0 | All four modules elaborated. `not_polyaSzegoTarget` has exact type `Not PolyaSzegoTarget`; inspected declarations report only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n --pcre2` prohibited-pattern scan over owned Lean source | 1, expected | No `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `extern` occurs. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean `4.29.0`, commit `98dc76e3...40`; Lake `5.0.0-src+98dc76e`. |
| Pinned package revision/tree and status checks | 0 | Mathlib `8a178386...95` / `bdc39a31...b2b`; flt-regular `56161b6e...a27` / `32c9eac...893`; both package worktrees stayed clean. |
| `sha256sum` over fifteen packet inputs | 0 | All hashes matched the structured packet. |
| Base delta from `69f012f9..HEAD` | 0 | Only prior blocker pairs were added under this target; authority changed without target repair or acceptance. |
| JSON syntax and target-scoped invariant checks | 0 | Item, base, ownership, exact negation, blocked state, incomplete-proof boundary, authority state, and absent-self-test invariants passed. |
| Scoped whitespace checks | 0 / 1, expected | No diagnostics; no-index returned only the expected new-file difference status. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test remains absent because the proof phase is blocked. |

Exact Lean replay from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-slot36-6ee4e043.XXXXXX)
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

Generated objects:

| Output | Bytes | SHA-256 |
|---|---:|---|
| `Statement.olean` | 67,392 | `3e7524cff9894071eac21c8dfcf6a8437663d4dfba5edbc52b8747075bb10c0b` |
| `Counterexample.olean` | 218,384 | `7d1b1dc2c45dfd3817979900e72c5389b33e481f1e27b24fcfe982e20f1ca9c1` |
| `ProofAudit.olean` | 100,776 | `320fb198abc6bd4b9ed89f5706f40a38912b5e9cdf5405b84444a53f946a0b5c` |
| `ObligationTree.olean` | 77,176 | `f8ac6ed41d32adb97136a09d7a5f3f0009bdc7c0dc1c6ddef2cba163c463aa86` |

## Retry Condition

Reopen `S56-M-1286-STATEMENT`: use measure-compatible Euclidean `l2` geometry, the intended smooth
compactly supported test class, and a rearrangement representation admitting essentially unbounded
finite-`p` inputs. Publish a new statement fingerprint and refreeze every dependent statement,
anchor, registry, graph, and obligation-tree artifact before resuming proof execution. The other
valid route is an explicit scheduler redirection to the checked counterexample target.

## Status Boundary

Lifecycle remains `planned`; no authoritative vector or scheduler state changed. This is fresh,
current-base, target-scoped nonrelease refutation evidence. It does not satisfy
`S56-M-1286-PROOF` and claims no positive proof completion, audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
