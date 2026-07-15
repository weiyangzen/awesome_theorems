# THM-M-1286 proof-phase recheck at current base

Item: `S56-M-1286-PROOF`

Intent: `prove`

Recorded: `2026-07-15T11:44:34+08:00` (`Asia/Shanghai`)

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. The current base contains a placeholder-free Lean refutation of the exact frozen
positive target:

```lean
theorem Stage1Instances.THM_M_1286.Counterexample.not_polyaSzegoTarget :
    Not Stage1Instances.THM_M_1286.PolyaSzegoTarget
```

Consequently no consistent proof body for `PolyaSzegoTarget` can satisfy this assigned positive
proof item. The item remains `[ ]`; this packet is current-base blocker evidence, not a positive
proof receipt.

The refutation specializes the target to `n = p = 1`. Its input is `-log x` on `(0, 1)`, extended
by zero and transported to `Fin 1 -> Real`, with zero proposed weak gradient. It is nonnegative and
integrable, all positive superlevels are finite, and every positive superlevel has strictly positive
measure. In the frozen API, `ContDiff Real top` is analytic rather than merely smooth, so a compactly
supported test function is zero and `HasWeakGradient` is vacuous. Any pointwise real-valued
`IsSymmetricDecreasing` witness is bounded above by its value at zero. At threshold
`uStar 0 + 1`, its superlevel is empty, contradicting equimeasurability with the unbounded input.

This contradiction is independent of the additional fidelity defect already checked by
`ProofAudit.lean`: `Euclidean n := Fin n -> Real` has the coordinate supremum norm, not Euclidean
`l2` geometry. The positive architecture is also only conditional.
`ObligationTree.exactTarget_of_packages` assumes `RearrangementConstruction` and
`GradientEstimate`; in a consistent environment those premises cannot both be implemented because
their checked composition would contradict `not_polyaSzegoTarget`.

No statement, proof source, registry, graph, tracked dependency lock/source, or scheduler state was
intentionally changed. The failed Lake discovery did touch the shared `.lake` target as detailed
below. No `.stage1-worker-selftest.json` was written because the requested positive proof phase is
not self-tested as complete.

## Narrow validation

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; stale positive root remains open at `M4`. |
| Direct pinned Lean 4.29.0 trust-zero replay described below | 0 | `Statement.lean` and `Counterexample.lean` elaborated; olean sizes 67392 and 218384 bytes. `not_polyaSzegoTarget` reported exactly `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry\|admit\|axiom)\\b\|sorryAx\|unsafe\|implemented_by\|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| `lake env lean --version` from `Formalizations/Lean` | 1 | Lake failed before invoking Lean: pinned package `flt-regular` could not resolve `HEAD` and its automatic materialization attempt exited through Git 128. This is not valid Lake evidence. |
| Direct pinned toolchain binary `lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `sha256sum` over the nine pinned inputs named below | 0 | Every digest matched this packet. |
| `python3 -m json.tool` on this packet | 0 | Structured blocker artifact is valid JSON. |
| `git diff --check` and no-index checks on both packet files | 0 / 1, expected | No whitespace diagnostics; no-index returned the expected difference status for each new file. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is absent because the positive proof phase is blocked. |

The smallest successful replay used the pinned Lean binary and only the existing compiled
mathlib/dependency libraries. It did not use the network, build dependencies, or write into
`.lake`; all compilation output was isolated under `/tmp` and removed:

```bash
set -euo pipefail
ROOT=$PWD
LEAN=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
TMP=$(mktemp -d /tmp/thm-m-1286-slot54-direct.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/Stage1_Instances/THM-M-1286"
BASE="$ROOT/Formalizations/Lean/.lake/packages/mathlib/.lake/build/lib/lean"
for p in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible; do
  d="$ROOT/Formalizations/Lean/.lake/packages/$p/.lake/build/lib/lean"
  test ! -d "$d" || BASE="$BASE:$d"
done
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE" timeout --foreground 300 "$LEAN" --trust=0 -t0 \
  -R "$ROOT" -o "$TMP/Stage1_Instances/THM-M-1286/Statement.olean" \
  "$ROOT/Stage1_Instances/THM-M-1286/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" timeout --foreground 300 "$LEAN" --trust=0 -t0 \
  -R "$ROOT" -o "$TMP/Counterexample.olean" \
  "$ROOT/Stage1_Instances/THM-M-1286/Counterexample.lean"
```

The prescribed `lake env lean` replay could not be run because the canonical pinned
`flt-regular` worktree was missing/incomplete. A read-only inspection call to `lake env which lean`
triggered Lake's own attempted package materialization before failing; the shared `.lake` therefore
cannot support hermetic evidence for this run. No `lake update`, `lake build`, explicit clone/fetch,
or manual dependency repair was run. This packet records the failed attempt rather than presenting
the direct-binary replay as a substitute for the later validation/release gates.

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

Reopen `S56-M-1286-STATEMENT`. Repair the Euclidean norm, use the intended smooth-test order rather
than analytic `top`, and repair the rearrangement codomain/regularity boundary so essentially
unbounded finite-`p` inputs are representable. Then rerun statement identity, transports,
mutations, anchor audit, registry, typed graphs, and obligation-tree gates before positive proof
work resumes. The automation environment must also restore the exact pinned `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` artifact before a prescribed `lake env lean` replay.

## Status boundary

Lifecycle remains `planned`; no authoritative vector or scheduler state was changed. This
current-base proof blocker supports integration review of an `M5` exact-target classification and
refreeze of all statement-dependent artifacts. It does not satisfy `S56-M-1286-PROOF` and claims no
positive proof completion, audit completion, validation, release, master acceptance, or theorem
completion.
