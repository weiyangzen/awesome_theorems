# THM-M-1286 proof-phase recheck at `ab6974ae`

Item: `S56-M-1286-PROOF`

Recorded: `2026-07-15T13:39:53+08:00` (`Asia/Shanghai`)

Base revision: `ab6974ae3bcabe677e7138ff057a7c005aac12d4`

Base tree: `c640af240d44f02c83a29dfa2f985f601a0dfcc2`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen target. The tracked,
placeholder-free declaration

```lean
theorem Stage1Instances.THM_M_1286.Counterexample.not_polyaSzegoTarget :
    Not Stage1Instances.THM_M_1286.PolyaSzegoTarget
```

kernel-checks at trust level zero against a freshly elaborated `Statement.olean`. The positive item
therefore remains `[ ]`; this packet is blocker evidence, not a positive proof receipt.

The refutation specializes the target to `n = p = 1`. The input is `-log x` on `(0, 1)`, extended
by zero and transported to `Fin 1 -> Real`, with zero as its proposed weak gradient. It is
nonnegative and integrable, and every positive superlevel has finite, strictly positive measure.
In the frozen API, `ContDiff Real top` denotes analytic rather than merely smooth regularity.
Analytic uniqueness forces compactly supported test functions to be zero, making
`HasWeakGradient` vacuous. Every pointwise real-valued `IsSymmetricDecreasing` witness is bounded
above by its value at zero, so its superlevel at `uStar 0 + 1` is empty. Equimeasurability with the
unbounded input then gives a contradiction.

This refutes only the current Lean encoding, not the classical Polya-Szego theorem. The encoding
also uses `Euclidean n := Fin n -> Real`, whose norm is the coordinate supremum norm rather than
Euclidean `l2`; `ProofAudit.lean` checks that mismatch. Finally,
`ObligationTree.exactTarget_of_packages` is only a conditional composition theorem. Its
`RearrangementConstruction` and `GradientEstimate` premises cannot both be implemented in a
consistent environment because their composition would contradict the checked refutation.

No Lean source, frozen predecessor artifact, dependency lock, scheduler authority, self-test
manifest, or unrelated target was changed. The bounded `lake env` probe automatically refreshed the
empty shared `flt-regular/.git/FETCH_HEAD` before timing out. This Git-metadata side effect is
disclosed, excluded from proof evidence, and was not repaired or hidden. `.stage1-worker-selftest.json`
is deliberately absent because the requested positive proof phase is not genuinely complete.

## Failed Gate And Retry

The first failed gate is exact canonical target consistency: trust-zero Lean proves
`Not PolyaSzegoTarget`. The remaining root cut is `S56-M-1286-STATEMENT`, not the stale positive
analytic package cut. Rev-5.6 classifies a refuted target and statement mismatch as a blocker; this
worker records evidence for integration review but changes no authoritative debt vector or state.

Retry only after an authorized statement-phase repair:

- use measure-compatible Euclidean `l2` geometry;
- use the intended smooth compactly supported test class rather than analytic `top`;
- represent rearrangements so essentially unbounded finite-`p` inputs are not forced to have a
  globally bounded pointwise real-valued representative;
- publish a new statement fingerprint and refreeze transports, mutations, anchor audit, registry,
  typed graphs, and obligation tree in dependency order; and
- restore the exact pinned `flt-regular` artifact before the prescribed `lake env lean` replay.

## Narrow Validation

All credited checks used this worker clone and existing pinned sources/artifacts. No `lake update`,
`lake build`, dependency clone/fetch, network action, or manual `.lake` repair was run. Successful
Lean output was confined to a fresh `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; stale positive root remains open `M4`. |
| Bounded isolated `lake env lean --trust=0 -t0` statement replay | 124 | Timed out after 60 seconds without output; the existing pinned `flt-regular` package has no resolvable `HEAD`; no dependency repair followed. |
| Direct pinned Lean 4.29.0 `--trust=0 -t0` replay below | 0 | `Statement.lean` and `Counterexample.lean` elaborated to 67,392-byte and 218,384-byte oleans. `not_polyaSzegoTarget` had exact type `Not PolyaSzegoTarget` and axioms `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|unsafe|implemented_by|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| Direct pinned toolchain `lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...40`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib revision `8a178386...95`, tree `bdc39a31...b2b`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}` | 128, expected blocker | Pinned package directory has no resolvable `HEAD`; no dependency mutation was attempted. |
| `sha256sum` over the nine pinned inputs listed below | 0 | All digests matched the structured packet. |

The smallest successful supporting replay used the pinned toolchain binary and only existing
compiled pinned libraries:

```bash
set -euo pipefail
ROOT=$PWD
LEAN=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
TMP=$(mktemp -d /tmp/thm-m-1286-ab6974ae-slot52.XXXXXX)
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
  -R "$ROOT" -o "$TMP/Stage1_Instances/THM-M-1286/Counterexample.olean" \
  "$ROOT/Stage1_Instances/THM-M-1286/Counterexample.lean"
```

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

## Status Boundary

Lifecycle remains `planned`; no authoritative vector or scheduler state was changed. This is
current-base, target-scoped, nonrelease proof-blocker evidence. It does not satisfy
`S56-M-1286-PROOF` and claims no positive proof completion, audit completion, validation, release,
master acceptance, or theorem completion.
