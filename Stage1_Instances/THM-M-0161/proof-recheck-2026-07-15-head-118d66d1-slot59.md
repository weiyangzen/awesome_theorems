# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `118d66d1986768cd9a00e661ccf6447c26a53efb`

Base tree: `e31babc8fcb7426673e5d6c0a4a884af2cd737e8`

Rechecked: `2026-07-15T18:00:37+08:00`

## Verdict

`blocked`. A placeholder-free positive proof cannot truthfully inhabit the exact frozen target.
The tracked `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

No positive proof body, proof receipt, provisional completion, audit completion, validation,
release, theorem completion, or master acceptance is claimed. The proof item remains `[ ]`, with
`root_closed=false` and `theorem_complete=false`. Its obligation-tree prerequisite is only
provisional `[_]`, not master accepted `[x]`. Because this positive proof phase is not genuinely
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Checked obstruction

The frozen target assumes only `DifferentiableOn Real kappa (Ioo a b)` while requiring a `C^3`
realizing curve. `curvature_is_contDiffOn_one` proves that a positive prescribed curvature realized
by such a curve must be `C^1` on the interval. The checked counterexample uses

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

This `kappa161` is differentiable everywhere and strictly positive on `(-1,1)`, but its derivative
is zero at zero and `-1` along `1 / ((n + 1) * 2*pi)`, which tends to zero. It is therefore not
`C^1`, contradicting the regularity forced by the target's existence conclusion. This refutes the
under-regularized Lean proposition only, not the classical theorem with source-faithful coefficient
regularity.

The negative declaration is an `M0-L` body for the exact negation only and gives no positive-root
credit. Rev-5.6 section 3 requires an `H5` redirect when the exact target is refuted, so this packet
proposes `H5/M5/R4` for authorized reconciliation. It does not rewrite predecessor statement,
instance, registry, graph, or task-state authority. The intake instance still records `H1/M4/R4`,
the frozen typed graph records `H3/M3/R4`, and `root_of_existence_and_uniqueness` only composes
assumed existence and uniqueness packages.

## Validation

All commands ran in this worker clone. Checks reused the existing pinned Lake closure. No `lake
update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The exact
trust-zero replay copied sources and wrote oleans only under a disposable `/tmp` directory, which
was removed on exit. The pre-existing untracked `Formalizations/Lean/.lake` symlink points to the
canonical shared cache, so this is narrow warm-cache, nonrelease blocker evidence. The tracked
mathlib worktree remained clean.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; theorem incomplete |
| current-base assigned-item DAG query | 0 | obligation-tree predecessor `[_]`, attempts 1; proof item `[ ]`, attempts 0 |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...dadbe`; historical positive root remains open |
| `timeout 300 python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | canonical expression `c140d1d1...7f82` and all four structural mutation tests passed |
| isolated pinned Lake-environment trust-zero replay below | 0 | statement and exact refutation elaborated with disposable oleans; exact negation, source scan, output scan, and axiom gates passed |
| independent subagent trust-zero replay | 0 | exact negation and the same axiom closure independently confirmed in a separate disposable directory |
| mathlib and `flt-regular` revision/tree/tracked-status checks | 0 | pinned revisions and trees matched; both tracked dependency worktrees were clean |
| structured report, hash, changed-path, and whitespace checks | 0 | the JSON packet parsed; frozen inputs and fail-closed fields matched; both fresh files and scoped delta passed `git diff --check` |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the positive proof phase is blocked |

The replay printed Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and:

```text
PROHIBITED_MATCH_COUNT=0
EXACT_NEGATION_TYPE=PASS
AXIOM_CLOSURE=propext,Classical.choice,Quot.sound
MATHLIB_HEAD=8a178386ffc0f5fef0b77738bb5449d50efeea95
MATHLIB_TREE=bdc39a3123201dae413a9d9be56ec242c19e5c2b
PINNED_LAKE_ENV_TRUST_ZERO_REPLAY=PASS
```

`#print axioms` reported exactly `propext`, `Classical.choice`, and `Quot.sound` for both
`curvature_is_contDiffOn_one` and `frozen_target_false`. The only diagnostic was a non-failing
`unnecessarySeqFocus` linter warning at `Counterexample.lean:70`. There was no Lean error, sorry
warning, unsolved goal, or prohibited proof construct.

The core replay, run from the repository root, was:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
LEAN_ROOT=$ROOT/Formalizations/Lean
TMP=$(mktemp -d /tmp/thm-m-0161-118d66d1-slot59-replay.XXXXXX)
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
cp "$TARGET/Statement.lean" "$TARGET/Counterexample.lean" "$TMP/"
LEAN=$(cd "$LEAN_ROOT" && env -u LEAN_PATH timeout 30 lake env which lean)
PINNED_LEAN_PATH=$(cd "$LEAN_ROOT" && env -u LEAN_PATH timeout 30 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$PINNED_LEAN_PATH" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
  "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$PINNED_LEAN_PATH" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Counterexample.olean" \
  "$TMP/Counterexample.lean"
```

A parser stripped comments, rejected `sorry`, `admit`, `sorryAx`, bodyless/unsafe/oracle
constructs, Lean errors, sorry warnings, and unsolved goals, required the exact negation type, and
required exactly the three recorded axioms for both key declarations. It then checked the Lean and
dependency identities and required clean tracked dependency worktrees. All disposable files were
removed by the trap.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first repair
the target with source-faithful `C^1` or stronger coefficient regularity, or replace the positive
item with an accepted counterexample or barrier target. A repaired target then needs a new canonical
expression fingerprint, append-only obligation-registry and typed-graph version deltas, and fresh
statement mutation testing, source review, anchor audit, obligation-tree construction, and proof
execution in dependency order.

This report is current-base negative evidence only. It does not satisfy `S56-M-0161-PROOF` and
supports no theorem-completion claim.
