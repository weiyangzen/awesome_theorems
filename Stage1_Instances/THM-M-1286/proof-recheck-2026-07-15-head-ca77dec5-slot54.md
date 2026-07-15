# THM-M-1286 proof-phase recheck at current base

Item: `S56-M-1286-PROOF`

Intent: `prove`

Recorded: `2026-07-15T12:01:10+08:00` (`Asia/Shanghai`)

Base revision: `ca77dec5478e55c429f8f55a078eeef45356771b`

Base tree: `bb9cc1b79fee7404df2dd6eef0eea47f998059f1`

## Verdict

`blocked`. The exact frozen positive target cannot consistently receive the requested proof body:
the owned source already contains a placeholder-free Lean proof of its negation.

```lean
theorem Stage1Instances.THM_M_1286.Counterexample.not_polyaSzegoTarget :
    Not Stage1Instances.THM_M_1286.PolyaSzegoTarget
```

The refutation specializes the target to `n = p = 1`. Its input is `-log x` on `(0, 1)`, extended
by zero and transported to `Fin 1 -> Real`, with zero proposed weak gradient. It is nonnegative and
integrable; every positive superlevel is finite and strictly positive. In the frozen definition,
`ContDiff Real top` means analytic, so every compactly supported test function is zero and
`HasWeakGradient` is vacuous. Any pointwise real-valued `IsSymmetricDecreasing` witness is bounded
above by its value at zero. Its superlevel at `uStar 0 + 1` is therefore empty, contradicting
equimeasurability with the unbounded input.

The positive obligation architecture is only conditional:
`ObligationTree.exactTarget_of_packages` assumes both `RearrangementConstruction` and
`GradientEstimate`. These premises cannot both be implemented in a consistent environment because
their checked composition would contradict `not_polyaSzegoTarget`. Independently,
`ProofAudit.lean` checks that the frozen `Euclidean n := Fin n -> Real` has the coordinate supremum
norm rather than Euclidean `l2` geometry.

No positive proof source, statement, registry, graph, dependency lock, checklist, or scheduler state
was changed. No `.stage1-worker-selftest.json` was written because this positive proof phase is not
complete.

## Narrow validation

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed structurally; denominator `e586a1f...ddaa4`; the stale positive root is recorded open at `M4`. |
| Direct pinned Lean 4.29.0 `--trust=0 -t0` replay described below | 0 | `Statement.lean` and `Counterexample.lean` elaborated; olean sizes 67392 and 218384 bytes. `not_polyaSzegoTarget` has exact type `Not PolyaSzegoTarget` and reports `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry\|admit\|axiom)\\b\|sorryAx\|unsafe\|implemented_by\|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited proof construct occurs in owned Lean source. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib revision `8a178386...95`, tree `bdc39a31...b2b`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 128, expected blocker | The pinned package directory has no resolvable `HEAD`; no fetch, clone, update, build, or repair was attempted. |
| Direct pinned toolchain `lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `sha256sum` over the nine pinned inputs listed below | 0 | All digests matched the values recorded here. |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/proof-recheck-2026-07-15-head-ca77dec5-slot54.json` | 0 | Structured blocker packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1286` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is absent because the positive proof phase is blocked. |

The successful replay used only the pinned Lean binary and existing compiled pinned libraries. It
wrote oleans under a fresh `/tmp` directory and removed them on exit; it did not invoke Lake or
mutate `.lake`.

```bash
set -euo pipefail
ROOT=$PWD
LEAN=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
TMP=$(mktemp -d /tmp/thm-m-1286-slot54-ca77dec.XXXXXX)
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

Reopen `S56-M-1286-STATEMENT`: use Euclidean `l2` geometry, the intended smooth-test order rather
than analytic `top`, and a rearrangement representation that permits essentially unbounded
finite-`p` inputs. Then refreeze and rerun statement identity, mutations, anchor audit, obligation
registry, typed graphs, and obligation-tree gates before resuming positive proof work. Prescribed
`lake env lean` replay additionally requires the existing pinned `flt-regular` artifact at
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` to be restored externally.

## Status boundary

This is current-base, target-scoped blocker evidence. It does not satisfy
`S56-M-1286-PROOF`, does not propose worker-provisional completion, and claims no theorem
completion, validation, release, or master acceptance.
