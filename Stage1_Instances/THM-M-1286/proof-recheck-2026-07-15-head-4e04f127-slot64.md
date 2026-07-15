# THM-M-1286 proof-phase execution at current base

Item: `S56-M-1286-PROOF`

Intent: `prove`

Recorded: `2026-07-15T08:45:27+08:00` (`Asia/Shanghai`)

Base revision: `4e04f1277aeb8c718b61049fd1af49b0ab00d882`

Base tree: `a1940b2f3482ac73691d8a22cc1925e3c75e438f`

## Verdict

`blocked`. Proof execution found and kernel-checked a contradiction to the exact frozen positive
target. `Counterexample.lean` proves:

```lean
theorem Stage1Instances.THM_M_1286.Counterexample.not_polyaSzegoTarget :
    Not Stage1Instances.THM_M_1286.PolyaSzegoTarget
```

Therefore no proof body for `PolyaSzegoTarget` can be added consistently, and the assigned positive
proof item cannot be completed. The item remains `[ ]`; this packet is blocker and refutation
evidence, not a positive proof receipt.

The refutation uses the exact target at `n = p = 1`. Let `u` be `-log x` on `(0, 1)`, zero outside,
transported to `Fin 1 -> Real`. It is nonnegative and integrable, its positive superlevel sets have
finite measure, and every positive superlevel has strictly positive measure. The target's
`HasWeakGradient` assumption is vacuous: in this frozen API, `ContDiff Real top` means analytic,
not smooth, and an analytic compactly supported test function is identically zero. Hence the zero
vector field is an admissible weak gradient.

Any witness satisfying the frozen pointwise `IsSymmetricDecreasing` predicate is bounded above by
its value at zero. Taking `t = uStar 0 + 1` makes its strict superlevel empty. Equimeasurability then
says the corresponding strict superlevel of `u` has measure zero, contradicting the checked
positive-measure result. This refutes the exact formal statement without relying on the previously
identified `l-infinity` versus Euclidean-`l2` mismatch.

The positive architecture remains only conditional: `ObligationTree.exactTarget_of_packages`
assumes `RearrangementConstruction` and `GradientEstimate`. A theorem premise cannot override a
kernel-checked refutation of the root. The neighboring M1285 construction is differently typed and
its `ENNReal` codomain can represent an infinite value at the origin; transporting it to the
M1286 real-valued pointwise interface is exactly where the contradiction appears.

No `.stage1-worker-selftest.json` was written because the requested positive proof phase is not
self-tested as complete. The prerequisite obligation-tree item also remains worker-provisional
rather than master-accepted.

## Narrow validation

All Lean checks reused the automation-provided pinned Lake artifacts read-only. No `lake update`,
`lake build`, dependency clone/fetch, network access, or `.lake` mutation was performed. Compiled
output was isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; the stale positive root remains recorded open at `M4`. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean` and `Counterexample.lean` | 0 | The exact target and refutation elaborated; olean sizes were 67392 and 218384 bytes. `not_polyaSzegoTarget` reported exactly `[propext, Classical.choice, Quot.sound]`. |
| Isolated `lake env lean --trust=0 -t0` replay of `ProofAudit.lean` and `ObligationTree.lean` | 0 | Five statement diagnostics and conditional composition elaborated; all declarations reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry\|admit\|axiom)\\b\|sorryAx\|unsafe\|implemented_by\|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `sha256sum` over the nine pinned inputs named below | 0 | Every digest matched the structured packet. |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/proof-recheck-2026-07-15-head-4e04f127-slot64.json` | 0 | The structured current-base blocker is valid JSON. |
| `git diff --check` plus `git diff --no-index --check /dev/null` for the three new files | 0 / 1, expected | No whitespace diagnostics; no-index returned difference status for each new file. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test is absent because the positive proof phase is blocked. |

Exact refutation replay from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-counterexample.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/Stage1_Instances/THM-M-1286"
cd "$ROOT/Formalizations/Lean"
LEAN_NUM_THREADS=1 timeout 180 lake env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/Stage1_Instances/THM-M-1286/Statement.olean" \
  ../../Stage1_Instances/THM-M-1286/Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP" timeout 180 lake env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/Counterexample.olean" \
  ../../Stage1_Instances/THM-M-1286/Counterexample.lean
```

Pinned input SHA-256 values:

- `Statement.lean`: `ef428b6d6fbb5a05b9112291cd5e113ff02d58776a03b2765837bd3ddc2039bb`
- `Counterexample.lean`: `dd227181174b72d4aafd614313499c35f6b930056879764b311a479f06f1f0a6`
- `ProofAudit.lean`: `09152048ca2a69b790f9bd1ab8db0e8bf533d7d5873b05d571b64647a1b647a9`
- `ObligationTree.lean`: `31690c4c88849ca069648df8cbc72aaec44ce139e83a9fabda1b5b26093a4d6b`
- `obligation-registry.json`: `c7d331ee666db5ca093880b051d0959395d35735bb2c337dfd7d5c7a91215d20`
- `typed-graphs.json`: `9c225e12b3cb6db6f264b360a5e7c6d418d837efe3214909d5cbd9a664a987e2`
- `anchor-audit.json`: `f05ca7a660c1ba2d5ca1fa359cde5338eaded9355c84795294d1a48e745bd33c`
- `validation-specs.json`: `2ee56fb5cadf7df96cc8d0ba96b6fbacec5cfc7861f2114a6608b444aec44e9a`
- `Formalizations/Lean/lake-manifest.json`: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`

## Retry condition

Reopen `S56-M-1286-STATEMENT`. Besides replacing the Pi/sup-norm space with a
measure-compatible Euclidean `l2` encoding and replacing analytic tests with the intended smooth
order, repair the rearrangement codomain or regularity boundary so essentially unbounded Sobolev
inputs are representable without requiring a finite pointwise value at the origin. Then rerun
statement identity, transports, mutations, anchor audit, registry, typed graphs, and
obligation-tree gates before any positive proof work resumes.

## Status boundary

Lifecycle remains `planned`; no authoritative vector or scheduler state was changed. The fresh
kernel result establishes an exact-statement contradiction and warrants integration review of an
`M5` classification plus invalidation/refreeze of statement-dependent artifacts. No positive proof
completion, audit completion, validation, release, master acceptance, or theorem completion is
claimed.
