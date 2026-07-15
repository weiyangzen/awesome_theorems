# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `accbdd6582656e7810e6e388651cc8dfc47b707b`

Base tree: `99d4c26098e653f4b8426fe2bb1d62cc228c421f`

Rechecked: `2026-07-15T13:23:53+08:00`

## Verdict

`blocked`. The requested placeholder-free positive proof body cannot truthfully be implemented for
the exact frozen target. The tracked repo-local `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

The proof item remains `[ ]`. No positive proof body, proof receipt, provisional completion, audit
completion, validation, release, theorem completion, or master acceptance is claimed. Because this
phase is not genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.

The frozen proposition assumes only `DifferentiableOn Real kappa (Ioo a b)` but requires a `C^3`
realizing curve. `curvature_is_contDiffOn_one` proves that the positive realized curvature of every
such curve is `C^1`. The checked obstruction takes

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

This curvature is differentiable everywhere and positive on the interval, but its derivative is
zero at zero and `-1` along `1 / ((n + 1) * 2*pi)`, a sequence tending to zero. It is therefore not
`C^1`, contradicting the regularity forced by the existence conclusion. This refutes only the
under-regularized frozen Lean encoding, not the classical fundamental theorem with source-faithful
coefficient regularity.

The negative declaration is an `M0-L` body for the exact negation only. It grants no positive-root
proof credit. The appropriate proposed classification for the frozen target is `H5/M5/R4`, while
the predecessor instance and typed graph retain historical vectors and a pre-refutation positive
architecture. This proof worker does not rewrite those predecessor authorities. In addition, the
only prerequisite, `S56-M-0161-OBLIGATION_TREE`, remains provisional `[_]`, not master-accepted
`[x]`.

## Validation

All commands ran from this worker clone. The successful narrow replay used pinned Lean `4.29.0`
commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, pinned mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `lake env lean --trust=0 -t0` inside the existing
mathlib subproject, one thread, eight already-built package library directories, and disposable
source copies and oleans under `/tmp`. No `lake update`, `lake build`, dependency clone/fetch,
checkout repair, or other `.lake` mutation was performed.

The automation-provided `Formalizations/Lean/.lake` is an untracked symlink to a shared canonical
cache. The root project cannot resolve `HEAD` in its pre-existing incomplete `flt-regular`
checkout, so both the root `lake env lean` check and `check_statement.py` fail before target
elaboration. The dependency was not repaired or fetched. The successful mathlib-subproject replay
is warm shared-cache, nonrelease blocker evidence, not a release receipt.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; theorem incomplete |
| assigned-item `jq` query | 0 | proof item `[ ]`, attempts `0`; prerequisite `[_]` |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations, 44 typed edges, denominator `48173f90...dadbe`; historical positive root open |
| `timeout 5 python3 Stage1_Instances/THM-M-0161/check_statement.py` | 1 | root Lake reported that incomplete `flt-regular` could not resolve `HEAD`; no repair attempted |
| `cd Formalizations/Lean && env -u LEAN_PATH timeout 5 lake env lean --version` | 1 | same missing-artifact blocker before Lean execution |
| pinned-mathlib `lake env lean --trust=0 -t0` replay below | 0 | statement, exact refutation, and positive-candidate-implies-False probe elaborated |
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
8a178386ffc0f5fef0b77738bb5449d50efeea95
PINNED_MATHLIB_LAKE_ENV_TRUST_ZERO_REPLAY=PASS
```

The only diagnostic was a non-failing `unnecessarySeqFocus` linter warning at
`Counterexample.lean:70`; there was no Lean error or sorry warning.

Exact core replay:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
MATHLIB=$ROOT/Formalizations/Lean/.lake/packages/mathlib
TMP=$(mktemp -d /tmp/thm-m-0161-accbdd65-slot65.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET/Statement.lean" "$TARGET/Counterexample.lean" "$TMP"/
LIBS=$(find -L "$ROOT/Formalizations/Lean/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d ! -path '*/flt-regular/*' \
  -print | sort | paste -sd: -)

(
  cd "$MATHLIB"
  LEAN_NUM_THREADS=1 LEAN_PATH="$LIBS" timeout 300 \
    lake env lean --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
    "$TMP/Statement.lean"
)
(
  cd "$MATHLIB"
  LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LIBS" timeout 300 \
    lake env lean --trust=0 -t0 --root="$TMP" -o "$TMP/Counterexample.olean" \
    "$TMP/Counterexample.lean"
)
```

A temporary `ConsistencyProbe.lean` imported `Counterexample` and kernel-checked

```lean
theorem positive_candidate_implies_false
    (h : FundamentalTheoremOfSpaceCurvesTarget) : False :=
  frozen_target_false h
```

with the same pinned `lake env lean --trust=0 -t0` invocation. The executed recipe stripped
comments and parser-scanned `Statement.lean` and `Counterexample.lean` for `sorry`, `admit`,
`sorryAx`, bodyless declarations, unsafe/oracle constructs, and related prohibited devices. It
also rejected Lean errors and sorry warnings, required the exact negation, and required exactly
`propext`, `Classical.choice`, and `Quot.sound` for `curvature_is_contDiffOn_one`,
`frozen_target_false`, and the consistency probe.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first require
`C^1` or stronger coefficient regularity, or replace the task with an accepted counterexample or
barrier target. A repaired target then requires a new canonical expression fingerprint, an
append-only obligation-registry and typed-graph version delta, and fresh mutation, source, anchor,
obligation-tree, and proof execution in dependency order.
