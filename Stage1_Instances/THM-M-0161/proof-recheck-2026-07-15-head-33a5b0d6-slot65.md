# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `33a5b0d654c92a894e155f5385edaae684091bb0`

Base tree: `74ed89524afb3c118e31a7fce9b5763fee26b180`

Rechecked: `2026-07-15T13:03:43+08:00`

## Verdict

`blocked`. The exact frozen positive target cannot truthfully receive the requested proof body:
the repository-local `Counterexample.lean`, already tracked in the worker base, kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

The proof item remains `[ ]`. No positive proof body, proof receipt, provisional completion, audit
completion, validation, release, theorem completion, or master acceptance is claimed. The root
`.stage1-worker-selftest.json` is deliberately absent.

The frozen target assumes only `DifferentiableOn Real kappa (Ioo a b)` while requiring a `C^3`
realizing curve. `curvature_is_contDiffOn_one` proves that the positive realized curvature of every
such curve is `C^1`. The checked obstruction chooses

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

This curvature is differentiable everywhere and positive on the interval, but its derivative is
zero at zero and `-1` along `1 / ((n + 1) * 2*pi)`, a sequence tending to zero. Hence it is not
`C^1`, so the target's existence conjunct is false. This refutes only the under-regularized frozen
Lean encoding, not the classical theorem with source-faithful coefficient regularity.

The negative theorem is an `M0-L` body for the exact negation only and supplies no positive-root
proof credit. The appropriate proposed classification of the frozen target is `H5/M5/R4`.
Authoritative predecessor artifacts still contain historical vectors and a pre-refutation positive
obligation graph; this proof worker does not rewrite them. The prerequisite
`S56-M-0161-OBLIGATION_TREE` is still provisional `[_]`, not master-accepted `[x]`.

## Validation

The successful narrow replay used the pinned Lean `4.29.0` binary at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, pinned mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `--trust=0`, one thread, eight existing package
library directories, and disposable source copies and oleans under `/tmp`. No `lake update`, `lake
build`, clone, fetch, or explicit dependency repair was run. `lake env which lean` was invoked only
inside the already-present pinned mathlib subproject; the selected Lean binary then performed the
elaborations directly.

The automation-provided `Formalizations/Lean/.lake` is an untracked symlink to the shared canonical
cache. The root Lake project cannot resolve `HEAD` in its pre-existing incomplete `flt-regular`
checkout. Both the root `lake env lean` command and `check_statement.py` therefore timed out before
producing output in bounded probes; no repair or moving dependency fetch was attempted. The
successful direct replay is warm shared-cache, nonrelease blocker evidence, not a release receipt.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; theorem incomplete |
| assigned-item `jq` query | 0 | proof item `[ ]`, prerequisite `[_]`, attempts `0` |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations, 44 edges, denominator `48173f90...dadbe`; historical positive root open |
| `timeout 5 python3 Stage1_Instances/THM-M-0161/check_statement.py` | 124 | bounded root-Lake probe produced no output; incomplete `flt-regular` has no resolvable `HEAD` |
| `cd Formalizations/Lean && env -u LEAN_PATH timeout 5 lake env lean --version` | 124 | same bounded root-Lake missing-artifact blocker; no output and no repair attempted |
| isolated direct pinned-mathlib `--trust=0 -t0` recipe below | 0 | statement, exact refutation, and positive-candidate consistency probe elaborated |
| source, output, exact-type, and axiom checks in the recipe | 0 | zero prohibited matches; all three declarations use exactly `propext`, `Classical.choice`, and `Quot.sound` |
| mathlib revision and tracked-status checks | 0 | manifest pin matched and the mathlib tracked worktree was clean |

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
Lean (version 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740)
8a178386ffc0f5fef0b77738bb5449d50efeea95
LEAN_PATH_COMPONENTS=8
DIRECT_PINNED_TRUST_ZERO_REPLAY=PASS
```

The only diagnostic was a non-failing `unnecessarySeqFocus` linter warning at
`Counterexample.lean:70`; there was no Lean error or sorry warning.

Exact core replay, run from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
MATHLIB=$ROOT/Formalizations/Lean/.lake/packages/mathlib
TMP=$(mktemp -d /tmp/thm-m-0161-slot65.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET/Statement.lean" "$TARGET/Counterexample.lean" "$TMP"/
LEAN=$(cd "$MATHLIB" && env -u LEAN_PATH lake env which lean)
LIBS=$(find -L "$ROOT/Formalizations/Lean/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d ! -path '*/flt-regular/*' \
  -print | sort | paste -sd: -)
TOOLCHAIN=$(dirname "$(dirname "$LEAN")")/lib/lean

LEAN_NUM_THREADS=1 LEAN_PATH="$LIBS:$TOOLCHAIN" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
  "$TMP/Statement.lean" >"$TMP/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LIBS:$TOOLCHAIN" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Counterexample.olean" \
  "$TMP/Counterexample.lean" >"$TMP/counterexample.out" 2>&1
```

A temporary `ConsistencyProbe.lean` imported `Counterexample` and proved

```lean
theorem positive_candidate_implies_false
    (h : FundamentalTheoremOfSpaceCurvesTarget) : False :=
  frozen_target_false h
```

under the same trust-zero invocation. The executed recipe also parser-scanned comment-stripped
source for `sorry`, `admit`, `sorryAx`, bodyless declarations, unsafe/oracle mechanisms, and related
prohibited devices; checked Lean output for errors and sorry warnings; and required the exact
negation and exact three-axiom set for both key declarations and the consistency probe.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first require
`C^1` or stronger coefficient regularity, or replace the task with an accepted counterexample or
barrier target. A repaired target then requires a new canonical expression fingerprint, an
append-only obligation-registry and typed-graph version delta, and fresh mutation, source, anchor,
obligation-tree, and proof execution in dependency order.
