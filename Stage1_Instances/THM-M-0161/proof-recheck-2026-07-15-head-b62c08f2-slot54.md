# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `b62c08f262435e44a30ad3fc88a4712e3954afc7`

Base tree: `f7374dcf5690374a2e9e5d13ac124b34c7ecfab1`

Rechecked: `2026-07-15` (`Asia/Shanghai`)

## Verdict

`blocked`. A placeholder-free positive proof body cannot truthfully inhabit the exact frozen
target. The tracked [Counterexample.lean](Counterexample.lean) kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

The same trust-zero replay also checked the consistency probe

```lean
theorem positive_candidate_implies_false
    (h : FundamentalTheoremOfSpaceCurvesTarget) : False :=
  frozen_target_false h
```

Thus accepting a positive proof of the unchanged target would accept `False` in the pinned
environment. No positive body, proof receipt, provisional completion, audit completion,
validation, release, theorem completion, or master acceptance is claimed. The proof item remains
`[ ]`, with `root_closed=false` and `theorem_complete=false`. Because the assigned positive proof
phase is not genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.

## Checked obstruction

The frozen target assumes only `DifferentiableOn Real kappa (Set.Ioo a b)` while demanding a
`C^3` realizing curve. `curvature_is_contDiffOn_one` proves that a positive prescribed curvature
realized by such a curve must be `C^1` on the interval. The checked counterexample uses

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

This `kappa161` is differentiable everywhere and strictly positive on `(-1,1)`, but its derivative
is zero at zero and `-1` along `1 / ((n + 1) * 2*pi)`, which tends to zero. It is therefore not
`C^1`, contradicting the regularity forced by the target's existence conclusion. This refutes the
under-regularized Lean proposition only, not the classical theorem with source-faithful
coefficient regularity.

The negative declaration is an `M0-L` body for the exact negation only and gives no positive-root
credit. Rev-5.6 section 3 requires an `H5` redirect when the exact target is refuted, so this packet
proposes `H5/M5/R4` for authorized reconciliation. It does not rewrite predecessor statement,
registry, graph, instance, or scheduler authority. The frozen graph still records `H3/M3/R4`, the
intake instance records `H1/M4/R4`, and the only prerequisite remains provisional `[_]`. The
existing `root_of_existence_and_uniqueness` consumes assumed existence and uniqueness packages and
therefore is conditional composition, not a positive proof.

## Validation

All commands ran in this worker clone. The exact replay reused the automation-provided pinned Lake
closure without running `lake update`, `lake build`, dependency clone/fetch, checkout repair, or
other `.lake` mutation. Sources and generated oleans lived only in a disposable `/tmp` directory.
The replay used `lake env which lean` from the pinned mathlib project, then invoked that Lean binary
directly with `--trust=0 -t0`, one thread, and the already-built package libraries. The untracked
`Formalizations/Lean/.lake` symlink points to the canonical shared cache, so this is deliberately
narrow, warm-cache, nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; lifecycle planned; theorem incomplete |
| assigned-item DAG query | 0 | proof item `[ ]`, attempts 0; obligation-tree prerequisite `[_]`, attempts 1 |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...dadbe`; positive root remains open |
| `timeout 300 python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | canonical expression `c140d1d1...f82`; all four structural mutations killed |
| isolated pinned-mathlib trust-zero replay below | 0 | statement, exact refutation, and positive-candidate-implies-`False` probe elaborated |
| replay source/output/type/axiom gates | 0 | no prohibited construct; exact negation passed; all three declarations use exactly `propext`, `Classical.choice`, and `Quot.sound` |
| mathlib revision/tree/tracked-status checks | 0 | manifest pin `8a178386...eea95`, tree `bdc39a31...a95`, and empty tracked status confirmed |
| input JSON parse and SHA-256 checks | 0 | registry, typed graph, and anchor audit parsed; frozen input hashes matched this packet |
| `python3 -m json.tool Stage1_Instances/THM-M-0161/proof-recheck-2026-07-15-head-b62c08f2-slot54.json >/dev/null` | 0 | fresh blocker packet is valid JSON |
| wrapped `git diff --no-index --check` for both new reports plus scoped `git diff --check` | 0 | both new artifacts and the complete scoped delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent because the positive proof phase is blocked |

The replay printed Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and:

```text
PROHIBITED_MATCH_COUNT=0
EXACT_NEGATION_TYPE=PASS
AXIOM_CLOSURE=propext,Classical.choice,Quot.sound
POSITIVE_CANDIDATE_IMPLIES_FALSE=PASS
LEAN_PATH_COMPONENTS=9
MATHLIB_HEAD=8a178386ffc0f5fef0b77738bb5449d50efeea95
MATHLIB_TREE=bdc39a3123201dae413a9d9be56ec242c19e5c2b
PINNED_MATHLIB_LAKE_ENV_TRUST_ZERO_REPLAY=PASS
```

The only diagnostic was a non-failing `unnecessarySeqFocus` linter warning at
`Counterexample.lean:70`. There was no Lean error, sorry warning, unsolved goal, or metavariable
diagnostic.

Exact core replay, run from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
LEAN_ROOT=$ROOT/Formalizations/Lean
MATHLIB=$LEAN_ROOT/.lake/packages/mathlib
TMP=$(mktemp -d /tmp/thm-m-0161-b62c08f2-slot54-replay.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET/Statement.lean" "$TARGET/Counterexample.lean" "$TMP"/
LEAN=$(cd "$MATHLIB" && env -u LEAN_PATH timeout 30 lake env which lean)
LIBS=$(find -L "$LEAN_ROOT/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d ! -path '*/flt-regular/*' \
  -print | LC_ALL=C sort | paste -sd: -)
TOOLCHAIN=$(dirname "$(dirname "$LEAN")")/lib/lean

LEAN_NUM_THREADS=1 LEAN_PATH="$LIBS:$TOOLCHAIN" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
  "$TMP/Statement.lean" >"$TMP/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LIBS:$TOOLCHAIN" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Counterexample.olean" \
  "$TMP/Counterexample.lean" >"$TMP/counterexample.out" 2>&1
```

A temporary `ConsistencyProbe.lean` imported `Counterexample`, defined the exact probe shown above,
and was elaborated with the same direct pinned-Lean invocation. The executed parser stripped nested
comments, rejected `sorry`, `admit`, `sorryAx`, bodyless/unsafe/oracle constructs, Lean errors,
sorry warnings, unsolved goals, and metavariable diagnostics, required the exact negation type, and
required exactly the three allowed axioms for `curvature_is_contDiffOn_one`,
`frozen_target_false`, and `positive_candidate_implies_false`. All disposable files were removed by
the trap.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first repair
the target with source-faithful `C^1` or stronger coefficient regularity, or replace the positive
item with an accepted counterexample or barrier target. A repaired target then needs a new canonical
expression fingerprint, an append-only obligation-registry and typed-graph version delta, and fresh
statement mutation testing, source review, anchor audit, obligation-tree construction, and proof
execution in dependency order.
