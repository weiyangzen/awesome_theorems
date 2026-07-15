# THM-M-1286 proof-phase refutation recheck

Item: `S56-M-1286-PROOF`

Intent: `prove`

Recorded: `2026-07-15T18:49:23+08:00` (`Asia/Shanghai`)

Base revision: `cb7809d0317a837cb067c0d3fe417c84f167b350`

Base tree: `312398b9378990dd26dbd22392237586d5ed1916`

## Verdict

`blocked`. A positive proof body cannot truthfully be implemented for the exact frozen target:
`Counterexample.lean` contains the placeholder-free theorem
`Stage1Instances.THM_M_1286.Counterexample.not_polyaSzegoTarget` with exact type
`Not PolyaSzegoTarget`. The current trust-zero, offline Lean replay elaborated it and reported only
`propext`, `Classical.choice`, and `Quot.sound`.

The counterexample specializes the target to `n = 1`, `p = 1`, zero gradient, and the integrable
nonnegative function `-log x` on `(0, 1)`. In the frozen statement, `ContDiff Real top` resolves to
analytic rather than smooth C-infinity regularity. Every compactly supported analytic test function
is zero, so `HasWeakGradient` becomes vacuous. Every pointwise real-valued radial-antitone proposed
rearrangement is bounded above by its value at zero, while the log spike has a positive-measure
superlevel above every positive threshold. Equimeasurability therefore gives a contradiction at
threshold `uStar 0 + 1`.

This refutes the frozen Lean encoding, not the classical Polya-Szego theorem. The encoding also uses
the ordinary Pi supremum norm on `Fin n -> Real`, rather than Euclidean `l2` geometry. Proof work may
not repair or substitute the statement during this phase. The conditional declaration
`ObligationTree.exactTarget_of_packages` gives no positive proof credit: its two premises cannot both
be implemented in the current consistent environment because their composition would contradict
the checked negation.

The first failed gate is exact canonical target consistency. The actionable remaining cut is the
predecessor `S56-M-1286-STATEMENT`, not the stale positive package cut. The prerequisite obligation
tree is only worker-provisional, the proof item remains `[ ]`, and no completion self-test is
permitted.

## Narrow validation

All Lean checks reused the automation-provided pinned Lake artifacts read-only. No `lake update`,
`lake build`, dependency clone/fetch, network action, or `.lake` mutation was performed. Generated
oleans were isolated below `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed structurally; denominator `e586a1f...ddaa4`; the stale positive root remains open `M4`. |
| Isolated `lake --offline env lean --trust=0 -t0` replay below | 0 | `Statement.lean` and `Counterexample.lean` elaborated to 67,392-byte and 218,384-byte oleans with SHA-256 `3e7524...c0b` and `7d1b1d...a9c1`. `not_polyaSzegoTarget` has exact type `Not PolyaSzegoTarget` and reports `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|unsafe|implemented_by|native_decide|extern\\b' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean `4.29.0`, commit `98dc76e3...40`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib revision `8a178386...95`, tree `bdc39a31...b2b`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}` | 0 | Pinned dependency revision `56161b6e...a27`, tree `32c9eace...893`. |
| `git -C` both pinned packages `status --short` | 0 | Both package worktrees remained unmodified. |
| `sha256sum` over the nine pinned inputs in the JSON packet | 0 | All digests matched `source_hashes`. |
| `python3 -m json.tool` on the adjacent JSON packet | 0 | Structured blocker packet is valid JSON. |
| Target-scoped semantic assertions over the JSON packet | 0 | Item, theorem, base, ownership, blocked verdict, refuted/open root, incomplete proof/theorem, and absent-self-test boundaries passed. |
| Scoped `git diff --check` and `git diff --no-index --check /dev/null` on both new files | 0 / 1, expected | The tracked check passed; each no-index check produced only the expected new-file difference status and no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test is absent because the positive proof phase is blocked. |

Exact Lean replay from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-slot10-cb7809d0.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/Stage1_Instances/THM-M-1286"
cd "$ROOT/Formalizations/Lean"
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=10s 600 \
  lake --offline env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/Stage1_Instances/THM-M-1286/Statement.olean" \
  ../../Stage1_Instances/THM-M-1286/Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP" timeout --foreground --kill-after=10s 600 \
  lake --offline env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/Stage1_Instances/THM-M-1286/Counterexample.olean" \
  ../../Stage1_Instances/THM-M-1286/Counterexample.lean
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

## Retry condition

Reopen `S56-M-1286-STATEMENT`: use measure-compatible Euclidean `l2` geometry, replace analytic
order `top`/`omega` with the intended smooth C-infinity order, and choose a rearrangement
representation that admits essentially unbounded finite-`p` inputs. Publish a new statement
fingerprint, then refreeze transports, mutations, anchor audit, registry, typed graphs, and
obligation tree in dependency order before resuming proof execution. Alternatively, explicitly
redirect execution to the checked counterexample target.

## Status boundary

Lifecycle remains `planned`; no authoritative debt vector or scheduler state changed. This is fresh
current-base, target-scoped, nonrelease refutation evidence. It does not satisfy
`S56-M-1286-PROOF` and claims no positive proof completion, audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance. No `.stage1-worker-selftest.json` is
written because the assigned positive proof phase is not self-tested complete.
