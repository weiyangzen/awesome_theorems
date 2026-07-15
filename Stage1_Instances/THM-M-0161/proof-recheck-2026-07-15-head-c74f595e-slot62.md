# THM-M-0161 current-base proof blocker

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `c74f595e99fe574f4619307c859ec20986bb2297`

Base tree: `b27451453ff7d1e87d296c6634bd270799c666d9`

Rechecked: `2026-07-15T12:11:08+08:00`

## Verdict

`blocked`. The exact frozen positive target is false, so no placeholder-free positive proof body
can truthfully satisfy this item. The already tracked `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

The frozen statement assumes only `DifferentiableOn Real kappa (Ioo a b)` but requires a `C^3`
realizing curve. Every such realization with positive prescribed curvature forces that curvature
to be `C^1`. The checked counterexample uses

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

Here `kappa161` is differentiable everywhere and positive on the interval, but its derivative is
zero at zero and `-1` along `1 / ((n + 1) * 2*pi)`, which tends to zero. Thus it is not `C^1` and
cannot be the curvature of a curve promised by the target. A temporary Lean probe also checked
that any inhabitant of the positive target, combined with `frozen_target_false`, proves `False`.

The negative theorem is a repo-local `M0-L` body for the exact negation only. It provides no
positive-root proof credit. Under rev-5.6 section 3.1 this proposes `H5/M5` for the frozen
under-regularized proposition and redirects work to statement repair, a counterexample target, or
a barrier target. It does not refute the classical theorem with source-faithful regularity.

The proof item remains `[ ]`. No positive proof body, proof receipt, provisional completion, audit
completion, validation, release, theorem completion, or master acceptance is claimed. This proof
worker also leaves the predecessor statement, obligation registry, typed graph, and scheduler
state unchanged.

## Validation

All checks ran from this worker clone. The successful narrow replay used Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, pinned mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `--trust=0`, one thread, and only existing compiled
libraries. Statement, counterexample, probe, logs, and oleans were copied or created in a disposable
`/tmp` directory and removed. No `lake update`, `lake build`, clone, fetch, checkout repair, or other
`.lake` mutation was performed.

The automation-provided `Formalizations/Lean/.lake` is an untracked symlink to a shared canonical
cache. The root project cannot currently resolve `HEAD` in its pre-existing incomplete
`flt-regular` checkout, so both `check_statement.py` and root-project `lake env lean` fail before
target elaboration. This missing pinned artifact is recorded as a blocker rather than fetched. For
the successful narrow replay, the pinned mathlib subproject supplied `lake env lean` and its
already-built dependency closure. This is warm, shared-cache, nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations, 44 edges, denominator `48173f90...dadbe`; historical positive root open |
| `python3 Stage1_Instances/THM-M-0161/check_statement.py` | 1 | root Lake project could not resolve the incomplete `flt-regular` checkout; no repair attempted |
| `cd Formalizations/Lean && env -u LEAN_PATH timeout 30 lake env lean --version` | 1 | same missing-artifact blocker before Lean execution |
| `cd Formalizations/Lean/.lake/packages/mathlib && env -u LEAN_PATH timeout 30 lake env lean --version` | 0 | pinned Lean 4.29.0 was available |
| isolated pinned-mathlib `lake env lean --trust=0 -t0` recipe below | 0 | statement, refutation, and consistency probe elaborated; exact type, axioms, and prohibited-device gates passed |
| mathlib revision and clean-status checks | 0 | manifest pin matched and its tracked worktree status was empty |
| structured JSON and scoped whitespace checks | 0 | blocker record valid; both fresh reports and the complete scoped worker delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion manifest deliberately absent |

The replay printed:

```text
PROHIBITED_MATCH_COUNT=0
AXIOM_EXACT_TYPE_AND_CONSISTENCY_PROBE=PASS
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
'Stage1Instances.THM_M_0161.curvature_is_contDiffOn_one' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_0161.frozen_target_false' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_0161.positive_candidate_implies_false' depends on axioms:
  [propext, Classical.choice, Quot.sound]
PINNED_MATHLIB_LAKE_ENV_TRUST_ZERO_REPLAY=PASS
```

The only diagnostic was a non-failing `unnecessarySeqFocus` linter warning at
`Counterexample.lean:70`. The source/output gate found no `sorry`, `admit`, `sorryAx`, bodyless
declaration, unsafe/oracle device, or Lean error.

Exact replay recipe, run from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
LEAN_ROOT=$ROOT/Formalizations/Lean
TMP=$(mktemp -d /tmp/thm-m-0161-slot62.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET/Statement.lean" "$TARGET/Counterexample.lean" "$TMP"/
LEAN=$(cd "$LEAN_ROOT/.lake/packages/mathlib" && \
  env -u LEAN_PATH timeout 30 lake env which lean)
LIBS=$(find -L "$LEAN_ROOT/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d ! -path '*/flt-regular/*' \
  -print | sort | paste -sd: -)
TOOLCHAIN=$(dirname "$(dirname "$LEAN")")/lib/lean

LEAN_NUM_THREADS=1 LEAN_PATH="$LIBS:$TOOLCHAIN" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
  "$TMP/Statement.lean" >"$TMP/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LIBS:$TOOLCHAIN" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Counterexample.olean" \
  "$TMP/Counterexample.lean" >"$TMP/counterexample.out" 2>&1

printf '%s\n' \
  'import Counterexample' \
  'namespace Stage1Instances.THM_M_0161' \
  'theorem positive_candidate_implies_false' \
  '    (h : FundamentalTheoremOfSpaceCurvesTarget) : False :=' \
  '  frozen_target_false h' \
  '#print axioms positive_candidate_implies_false' \
  'end Stage1Instances.THM_M_0161' >"$TMP/ConsistencyProbe.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LIBS:$TOOLCHAIN" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/ConsistencyProbe.olean" \
  "$TMP/ConsistencyProbe.lean" >"$TMP/probe.out" 2>&1
```

The executed recipe then parser-scanned the comment-stripped counterexample source, required the
exact negation and exact three-axiom set for both key declarations and the consistency probe, and
rejected prohibited source/output markers. The structured JSON sibling records the source hashes,
environment hashes, exact outputs, and command results.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first require
`C^1` or stronger coefficient regularity, or replace the task with an accepted counterexample or
barrier target. A repaired target then needs a new canonical expression fingerprint, an append-only
obligation-registry and typed-graph version delta, and fresh mutation, source, anchor, tree, and
proof execution in dependency order.

Because the assigned positive proof phase is blocked rather than genuinely self-tested,
`.stage1-worker-selftest.json` is deliberately absent.
