# THM-M-1286 proof-phase refutation recheck at `62a4768e`

Item: `S56-M-1286-PROOF`

Worker: Stage1 rev-5.6 slot46

Base revision: `62a4768eab1bedaed6d970d504e1788c021f47a9`

Base tree: `fc154c2bea683094c1a662e67edba530547f5270`

Verdict: `blocked`

State: `[ ]`

Lifecycle: `planned -> planned`

Proof phase complete: `false`

Audit complete: `false`

Theorem complete: `false`

## Result

No positive proof body can truthfully be implemented for the frozen target. Trust-zero Lean in the
current pinned environment checks
`Stage1Instances.THM_M_1286.Counterexample.not_polyaSzegoTarget` at the exact type
`Not Stage1Instances.THM_M_1286.PolyaSzegoTarget`. The declaration reports only `propext`,
`Classical.choice`, and `Quot.sound`.

The counterexample specializes the target to `n = 1` and `p = 1`, with the integrable nonnegative
function `-log x` on `(0, 1)` transported to `Fin 1 -> Real` and the zero gradient. The target's
`ContDiff Real top` tests are analytic, not merely smooth. Analytic uniqueness forces every
compactly supported test function to vanish, so the frozen `HasWeakGradient` predicate is vacuous.
Every positive superlevel of the log spike nevertheless has positive finite measure. A pointwise
real-valued radial-decreasing witness is bounded above by its value at zero, making its superlevel
at `uStar 0 + 1` empty and contradicting equimeasurability.

This refutes the frozen Lean encoding, not a correctly formulated classical Polya-Szego theorem.
The encoding independently uses `Euclidean n := Fin n -> Real`, whose norm is the coordinate
supremum norm instead of Euclidean `l2`; `ProofAudit.lean` checks that mismatch. The positive
composition theorem `ObligationTree.exactTarget_of_packages` only consumes
`RearrangementConstruction` and `GradientEstimate`. Those premises cannot both be implemented in a
consistent environment because their checked composition would contradict the exact refutation.

The first failed gate is exact canonical target consistency. The actionable cut is the predecessor
`S56-M-1286-STATEMENT`, not the stale positive analytic-package cut. The obligation-tree predecessor
is also only worker-provisional (`[_]`), not master-accepted. This proof worker changes neither
predecessor artifacts nor authoritative state.

No Lean source, dependency lock, scheduler authority, or unrelated target was changed.
`.stage1-worker-selftest.json` is deliberately absent because the assigned positive proof phase is
not genuinely complete.

## Narrow Validation

All checks ran in this worker clone. The automation-provided `Formalizations/Lean/.lake` link was
treated as read-only and reused the canonical pinned artifacts. Temporary Lean objects were written
only below `/tmp` and removed. No `lake update`, `lake build`, dependency clone/fetch, network
action, checkout repair, or dependency mutation was performed.

The run started from a clean tracked tree and clean owned path. The pre-existing untracked `.lake`
link points to the scheduler's canonical pinned cache; it is recorded as a nonrelease input boundary,
not as a file created or modified by this worker. The structured packet also binds the current
blueprint, manifest, DAG, execution skill, guidelines, Lean binary, target sources, and dependency
pins by digest or immutable revision/tree identity.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed structurally; denominator `e586a1f...ddaa4`; the stale positive root is recorded open `M4`. |
| Isolated `lake --offline env lean --trust=0 -t0` replay below | 0 | `Statement.lean` and `Counterexample.lean` elaborated to 67,392-byte and 218,384-byte oleans with SHA-256 `3e7524...c0b` and `7d1b1d...a9c1`. `not_polyaSzegoTarget` has exact type `Not PolyaSzegoTarget` and reports `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|unsafe\|implemented_by\|native_decide\|extern\b' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean `4.29.0`, commit `98dc76e3...40`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib revision `8a178386...95`, tree `bdc39a31...b2b`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}` | 0 | Pinned dependency revision `56161b6e...a27`, tree `32c9eace...893`. |
| `git -C` both pinned packages `status --short` | 0 | Both package worktrees remained unmodified. |
| Scoped `git diff --quiet f53223e6..HEAD` over the frozen target inputs and Lean manifest | 0 | Statement, refutation, diagnostics, obligation artifacts, audit/specification inputs, and dependency lock are unchanged since the latest integrated checked packet. |
| `sha256sum` over the nine pinned inputs listed below | 0 | All digests matched the structured packet. |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/proof-refutation-recheck-2026-07-15-head-62a4768e-slot46.json` | 0 | The structured current-base blocker packet is valid JSON. |
| Target-scoped semantic assertions over the JSON packet | 0 | Item, theorem, base, ownership, blocked verdict, open/refuted root, incomplete proof/theorem, and absent-self-test boundaries passed. |
| Scoped `git diff --check` and `git diff --no-index --check /dev/null` on both new files | 0 / 1, expected | The tracked check passed; each no-index check reported only the expected new-file difference and no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test is absent because the positive proof phase is blocked. |

Exact Lean replay from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-slot46-62a4768e.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/Stage1_Instances/THM-M-1286"
cd "$ROOT/Formalizations/Lean"
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s \
  lake --offline env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/Stage1_Instances/THM-M-1286/Statement.olean" \
  ../../Stage1_Instances/THM-M-1286/Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP" timeout --foreground --kill-after=5s 300s \
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

## Retry Condition

Reopen `S56-M-1286-STATEMENT`: use measure-compatible Euclidean `l2` geometry, the intended smooth
compactly supported test class, and a rearrangement representation that admits essentially
unbounded finite-`p` inputs. Publish a new statement fingerprint and refreeze the statement,
transports, mutations, anchor audit, registry, typed graphs, and obligation tree in dependency order
before resuming proof execution. Alternatively, explicitly redirect execution to the checked
counterexample target.

## Status Boundary

Lifecycle remains `planned`; no authoritative debt vector or scheduler state was changed. This is
fresh current-base, target-scoped, nonrelease refutation evidence. It does not satisfy
`S56-M-1286-PROOF` and claims no positive proof completion, audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
