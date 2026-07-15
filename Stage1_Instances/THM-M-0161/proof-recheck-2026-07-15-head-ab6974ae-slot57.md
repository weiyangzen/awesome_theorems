# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `ab6974ae3bcabe677e7138ff057a7c005aac12d4`

Base tree: `c640af240d44f02c83a29dfa2f985f601a0dfcc2`

Rechecked: `2026-07-15T13:45:15+08:00`

## Verdict

`blocked`. A placeholder-free positive proof body cannot truthfully be implemented for the exact
frozen target. The tracked repo-local `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

Consequently any positive inhabitant of the target derives `False` in the same pinned environment.
The proof item remains `[ ]`. No positive proof body, proof receipt, provisional completion, audit
completion, validation, release, theorem completion, or master acceptance is claimed. Because the
assigned phase is not genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.

The frozen proposition assumes only `DifferentiableOn Real kappa (Ioo a b)` while requiring a
`C^3` realizing curve. `curvature_is_contDiffOn_one` proves that the positive realized curvature of
every such curve is `C^1`. The checked obstruction takes

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

This curvature is differentiable everywhere and positive on the interval, but its derivative is
zero at zero and `-1` along `1 / ((n + 1) * 2*pi)`, a sequence tending to zero. Thus it is not
`C^1`, contradicting the regularity forced by the target's existence conclusion. This refutes only
the under-regularized frozen Lean encoding, not the classical theorem with source-faithful
coefficient regularity.

The negative declaration is an `M0-L` body for the exact negation only and grants no positive-root
proof credit. The proposed classification for this frozen target is `H5/M5/R4`. This proof worker
does not rewrite the predecessor instance, registry, graph, or generated scheduler authority. The
historical obligation tree still exposes positive existence and uniqueness packages, and its
conditional composition theorem assumes both packages rather than proving them. Moreover, the
proof item's only prerequisite, `S56-M-0161-OBLIGATION_TREE`, remains provisional `[_]`, not
master-accepted `[x]`.

## Validation

All commands ran in this worker clone. The narrow successful replay used pinned Lean `4.29.0`
commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, pinned mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `lake env which lean` inside the existing mathlib
subproject, `--trust=0 -t0`, one thread, eight already-built package library directories, and
disposable sources and oleans under `/tmp`. It did not run `lake update`, `lake build`, a dependency
clone/fetch, checkout repair, or any other `.lake` mutation.

The automation-provided `Formalizations/Lean/.lake` is an untracked symlink to a shared canonical
cache. Bounded root-project probes timed out before producing output. The root cache's pre-existing
`flt-regular` checkout has no resolvable `HEAD`; it was not repaired or fetched. The successful
mathlib-subproject replay is warm shared-cache, nonrelease blocker evidence, not a release receipt.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; theorem incomplete |
| assigned-item JSON query | 0 | proof item `[ ]`, attempts `0`; prerequisite `[_]` |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations, 44 typed edges, denominator `48173f90...dadbe`; historical positive root open |
| `timeout 10 python3 Stage1_Instances/THM-M-0161/check_statement.py` | 124 | bounded root-Lake probe timed out without output; no dependency repair attempted |
| `cd Formalizations/Lean && env -u LEAN_PATH timeout 10 lake env lean --version` | 124 | same bounded root-project timeout |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 128 | fatal: ambiguous `HEAD`; the pre-existing dependency checkout has no resolvable revision |
| isolated pinned-mathlib trust-zero replay below | 0 | statement, exact refutation, and positive-candidate-implies-`False` probe elaborated |
| parser/output/exact-type/axiom gates in the replay | 0 | zero prohibited matches; exact negation passed; all three declarations use exactly the allowed axioms |
| mathlib revision/tree/tracked-status checks | 0 | manifest pin and tree matched; tracked mathlib worktree was clean |

The replay printed:

```text
PROHIBITED_MATCH_COUNT=0
EXACT_NEGATION_TYPE=PASS
AXIOM_CLOSURE=propext,Classical.choice,Quot.sound
POSITIVE_CANDIDATE_IMPLIES_FALSE=PASS
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
'Stage1Instances.THM_M_0161.positive_candidate_implies_false' depends on axioms:
  [propext, Classical.choice, Quot.sound]
LEAN_PATH_COMPONENTS=8
Lean (version 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740)
MATHLIB_HEAD=8a178386ffc0f5fef0b77738bb5449d50efeea95
MATHLIB_TREE=bdc39a3123201dae413a9d9be56ec242c19e5c2b
LEAN_BINARY_SHA256=3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf
PINNED_MATHLIB_LAKE_ENV_TRUST_ZERO_REPLAY=PASS
```

The only diagnostic was a non-failing `unnecessarySeqFocus` linter warning at
`Counterexample.lean:70`; there was no Lean error or sorry warning.

Exact core replay, run from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
LEAN_ROOT=$ROOT/Formalizations/Lean
MATHLIB=$LEAN_ROOT/.lake/packages/mathlib
TMP=$(mktemp -d /tmp/thm-m-0161-ab6974ae-slot57-replay.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET/Statement.lean" "$TARGET/Counterexample.lean" "$TMP"/
LEAN=$(cd "$MATHLIB" && env -u LEAN_PATH timeout 30 lake env which lean)
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
```

A temporary `ConsistencyProbe.lean` imported `Counterexample` and kernel-checked

```lean
theorem positive_candidate_implies_false
    (h : FundamentalTheoremOfSpaceCurvesTarget) : False :=
  frozen_target_false h
```

with the same direct pinned Lean invocation. The executed recipe stripped nested comments and
parser-scanned `Statement.lean` and `Counterexample.lean` for `sorry`, `admit`, `sorryAx`, axiom,
unsafe/oracle, extern, and related prohibited devices. It rejected Lean errors, sorry warnings, and
metavariable diagnostics; required the exact target negation; and required exactly `propext`,
`Classical.choice`, and `Quot.sound` for `curvature_is_contDiffOn_one`, `frozen_target_false`, and
the consistency probe. All disposable files were removed by the replay trap.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first require
`C^1` or stronger coefficient regularity, or replace the task with an accepted counterexample or
barrier target. A repaired target then requires a new canonical expression fingerprint, an
append-only obligation-registry and typed-graph version delta, and fresh mutation, source, anchor,
obligation-tree, and proof execution in dependency order.
