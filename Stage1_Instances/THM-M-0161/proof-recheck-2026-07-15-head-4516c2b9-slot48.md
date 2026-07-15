# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `4516c2b9d9dfa14a5f8b09da31e54e91718a6cf0`

Base tree: `e7886f0e6704a1d2e56c136d2316207cced14abd`

Rechecked: `2026-07-15T20:45:49+08:00`

## Verdict

`blocked`. A placeholder-free positive proof body cannot truthfully inhabit the exact frozen
target. The tracked [Counterexample.lean](Counterexample.lean) kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

The same trust-zero replay checked

```lean
theorem positive_candidate_implies_false
    (h : FundamentalTheoremOfSpaceCurvesTarget) : False :=
  frozen_target_false h
```

Thus accepting a positive proof of the unchanged target would accept `False` in the pinned
environment. No positive proof body, proof receipt, provisional completion, audit completion,
validation, release, theorem completion, or master acceptance is claimed. The item remains `[ ]`,
with `root_closed=false` and `theorem_complete=false`. Its obligation-tree prerequisite is only
provisional `[_]`. Because this positive proof phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Checked obstruction

The target assumes only `DifferentiableOn Real kappa (Set.Ioo a b)` while demanding a `C^3`
realizing curve. `curvature_is_contDiffOn_one` proves that the positive curvature of any such curve
must be `C^1` on the interval. The checked counterexample uses

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

This `kappa161` is differentiable everywhere and strictly positive on `(-1,1)`, but its derivative
is zero at zero and `-1` along `1 / ((n + 1) * 2*pi)`, which tends to zero. It is therefore not
`C^1`, contradicting the regularity forced by the target's existence conclusion. This refutes only
the under-regularized Lean proposition, not the classical theorem with source-faithful coefficient
regularity.

The negative declaration is a repo-local, kernel-checked body for the exact negation only. It gives
no positive-root credit. Rev-5.6 section 3 requires an `H5` redirect for a refuted target, so this
packet proposes `H5/M5/R4` for authorized reconciliation. It does not rewrite the predecessor
statement, registry, graph, instance, or scheduler authority. The existing
`root_of_existence_and_uniqueness` is conditional composition: it assumes both positive packages
and proves neither.

## Validation

All commands ran in this worker clone. The replay reused the automation-provided pinned Lake
closure without running `lake update`, `lake build`, dependency clone/fetch, checkout repair, or
other `.lake` mutation. Generated oleans and the consistency probe existed only in a disposable
`/tmp` directory and were removed by the trap. The untracked `Formalizations/Lean/.lake` symlink
points to the canonical shared cache, so this is narrow, warm-cache, nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; theorem incomplete |
| assigned proof/prerequisite DAG query | 0 | proof item `[ ]`, attempts 0; obligation-tree prerequisite `[_]`, attempts 1 |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...dadbe`; positive root remains open |
| `timeout --foreground --kill-after=5s 300 python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | canonical expression `c140d1d1...f82`; all four structural mutations killed; mathlib pin matched |
| isolated pinned Lake-environment trust-zero replay below | 0 | statement, exact refutation, and positive-candidate-implies-`False` probe elaborated |
| replay source/output/type/axiom gates | 0 | zero prohibited matches; exact negation passed; all three declarations use exactly `propext`, `Classical.choice`, and `Quot.sound` |
| mathlib and flt-regular revision/tree/status checks | 0 | both manifest revisions matched and both tracked dependency worktrees were clean |
| `python3 -m json.tool Stage1_Instances/THM-M-0161/proof-recheck-2026-07-15-head-4516c2b9-slot48.json >/dev/null` | 0 | fresh current-base blocker packet is valid JSON |
| wrapped new-file/scoped `git diff --check`, JSON semantic assertions, and prohibited-source scan | 0 | both reports have no whitespace errors; blocker/state booleans and source-policy assertions passed |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent because the positive proof phase is blocked |

The replay printed Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and:

```text
PROHIBITED_MATCH_COUNT=0
EXACT_NEGATION_TYPE=PASS
AXIOM_CLOSURE=propext,Classical.choice,Quot.sound
POSITIVE_CANDIDATE_IMPLIES_FALSE=PASS
LEAN_PATH_COMPONENTS=13
MATHLIB_HEAD=8a178386ffc0f5fef0b77738bb5449d50efeea95
MATHLIB_TREE=bdc39a3123201dae413a9d9be56ec242c19e5c2b
FLT_REGULAR_HEAD=56161b6eb5281fbfe9c38f2bcec0f429ebc11a27
PINNED_LAKE_ENV_TRUST_ZERO_REPLAY=PASS
```

`#print axioms` reported exactly `propext`, `Classical.choice`, and `Quot.sound` for
`curvature_is_contDiffOn_one`, `frozen_target_false`, and the consistency probe. The only diagnostic
was a non-failing `unnecessarySeqFocus` linter warning at `Counterexample.lean:70`. There was no
Lean error, sorry warning, unsolved goal, or metavariable diagnostic.

Exact core replay, run from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
LEAN_ROOT=$ROOT/Formalizations/Lean
TMP=$(mktemp -d /tmp/thm-m-0161-4516c2b9-slot48-replay.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN=$(cd "$LEAN_ROOT" && env -u LEAN_PATH timeout 30 lake env which lean)
PINNED_LEAN_PATH=$(cd "$LEAN_ROOT" && env -u LEAN_PATH timeout 30 lake env printenv LEAN_PATH)

test "$(sha256sum "$TARGET/Statement.lean" | cut -d' ' -f1)" = \
  82f74a6f99d1b81fe3dac43628a6d5d7dd0f88a323d42b0d21c300bb92a43060
test "$(sha256sum "$TARGET/Counterexample.lean" | cut -d' ' -f1)" = \
  2f306383c91022b4767de275a59be8fbb987da4d765f2d72e632a83d34f710f9

LEAN_NUM_THREADS=1 LEAN_PATH="$PINNED_LEAN_PATH" timeout 300 \
  "$LEAN" --trust=0 -t0 -R "$TARGET" -o "$TMP/Statement.olean" \
  "$TARGET/Statement.lean" >"$TMP/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$PINNED_LEAN_PATH" timeout 300 \
  "$LEAN" --trust=0 -t0 -R "$TARGET" -o "$TMP/Counterexample.olean" \
  "$TARGET/Counterexample.lean" >"$TMP/counterexample.out" 2>&1
```

A temporary `ConsistencyProbe.lean` imported `Counterexample`, defined the exact probe shown above,
and was elaborated with the same direct pinned Lean invocation. The executed parser stripped nested
comments; rejected `sorry`, `admit`, `sorryAx`, bodyless/unsafe/oracle constructs, Lean errors,
sorry warnings, unsolved goals, and metavariable diagnostics; required the exact negation type; and
required exactly the three recorded axioms for all three declarations. The trap removed every
disposable file.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first repair
the target with source-faithful `C^1` or stronger coefficient regularity, or replace the positive
item with an accepted counterexample or barrier target. A repaired target then needs a new canonical
expression fingerprint, an append-only obligation-registry and typed-graph version delta, and fresh
statement mutation testing, source review, anchor audit, obligation-tree construction, and proof
execution in dependency order.

This report is current-base negative evidence only. It does not satisfy `S56-M-0161-PROOF` and
supports no theorem-completion claim.
