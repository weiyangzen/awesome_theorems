# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `d6616cc60ad980c635f22ef840e9c5db2ebcab50`

Base tree: `d6f3c3aedec26191f09878fd6eb1fec666adf318`

Rechecked: `2026-07-15T17:48:33+08:00`

## Verdict

`blocked`. A placeholder-free positive proof cannot truthfully inhabit the exact frozen target.
The tracked `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

No positive proof body, proof receipt, provisional completion, audit completion, validation,
release, theorem completion, or master acceptance is claimed. The proof item remains `[ ]`, with
`root_closed=false` and `theorem_complete=false`. The obligation-tree prerequisite is only
provisional `[_]`, not master accepted `[x]`. Because the assigned positive proof phase is not
genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.

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
the frozen typed graph records `H3/M3/R4`, and the existing
`root_of_existence_and_uniqueness` consumes assumed existence and uniqueness packages and is only
conditional composition.

## Validation

All commands ran in this worker clone. Checks reused the existing pinned Lake closure. No `lake
update`, `lake build`, dependency clone/fetch, or other `.lake` mutation was performed. The exact
trust-zero replay wrote its oleans and command outputs only under a disposable `/tmp` directory and
removed them on exit. The pre-existing untracked `Formalizations/Lean/.lake` symlink points to the
canonical shared cache, so this is narrow warm-cache, nonrelease blocker evidence. The tracked
mathlib worktree remained clean.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; theorem incomplete |
| current-base assigned-item DAG query | 0 | obligation-tree predecessor `[_]`, attempts 1; proof item `[ ]`, attempts 0 |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...dadbe`; historical positive root remains open |
| `timeout 300 python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | canonical expression `c140d1d1...f82`; all four structural mutations killed; pinned mathlib revision matched |
| isolated pinned Lake-environment trust-zero replay below | 0 | statement and exact refutation elaborated with disposable oleans; exact negation, source scan, output scan, and axiom gates passed |
| mathlib revision/tree/tracked-status checks | 0 | revision `8a178386...eea95`, tree `bdc39a31...a95`, and empty tracked status |
| `python3 -m json.tool Stage1_Instances/THM-M-0161/proof-recheck-2026-07-15-head-d6616cc6-slot59.json >/dev/null` | 0 | fresh blocker packet is valid JSON |
| wrapped new-file and scoped `git diff --check` commands | 0 | both fresh reports and the complete scoped delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent because the positive proof phase is blocked |

The replay printed Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and:

```text
PROHIBITED_MATCH_COUNT=0
EXACT_NEGATION_TYPE=PASS
AXIOM_CLOSURE=propext,Classical.choice,Quot.sound
LEAN_PATH_COMPONENTS=13
MATHLIB_HEAD=8a178386ffc0f5fef0b77738bb5449d50efeea95
MATHLIB_TREE=bdc39a3123201dae413a9d9be56ec242c19e5c2b
PINNED_LAKE_ENV_TRUST_ZERO_REPLAY=PASS
```

`#print axioms` reported exactly `propext`, `Classical.choice`, and `Quot.sound` for both
`curvature_is_contDiffOn_one` and `frozen_target_false`. The only diagnostic was a non-failing
`unnecessarySeqFocus` linter warning at `Counterexample.lean:70`. There was no Lean error, sorry
warning, unsolved goal, or prohibited proof construct.

Exact core replay, run from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
LEAN_ROOT=$ROOT/Formalizations/Lean
TMP=$(mktemp -d /tmp/thm-m-0161-d6616cc6-slot59-replay.XXXXXX)
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

The executed parser stripped comments, rejected `sorry`, `admit`, `sorryAx`, bodyless/unsafe/oracle
constructs, Lean errors, sorry warnings, and unsolved goals, required the exact negation type, and
required exactly the three recorded axioms for both key declarations. It then checked Lean and
mathlib revision/tree identities and required an empty tracked mathlib status. The full parser is
captured in the worker command transcript; all disposable files were removed by the trap.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first repair
the target with source-faithful `C^1` or stronger coefficient regularity, or replace the positive
item with an accepted counterexample or barrier target. A repaired target then needs a new canonical
expression fingerprint, append-only obligation-registry and typed-graph version deltas, and fresh
statement mutation testing, source review, anchor audit, obligation-tree construction, and proof
execution in dependency order.

This report is current-base negative evidence only. It does not satisfy `S56-M-0161-PROOF` and
supports no theorem-completion claim.
