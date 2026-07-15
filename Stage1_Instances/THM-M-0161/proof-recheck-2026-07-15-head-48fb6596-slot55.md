# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `48fb6596b1844f4183c411142415d872ff21e842`

Base tree: `eb8dfff0e90b5ce5b11ac2096777060d62874064`

Rechecked: `2026-07-15T15:01:27+08:00`

## Verdict

`blocked`. The exact frozen positive target cannot receive a truthful proof body because the
repository-local, already tracked `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

The positive proof item remains `[ ]`. No positive proof body, proof receipt, provisional
completion, audit completion, validation, release, theorem completion, or master acceptance is
claimed. The root `.stage1-worker-selftest.json` is deliberately absent.

The frozen target assumes only `DifferentiableOn Real kappa (Ioo a b)` while requiring a `C^3`
realizing curve. The checked obstruction uses

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

This curvature is differentiable everywhere and positive on the interval. However,
`curvature_is_contDiffOn_one` proves that every positive curvature realized by a `C^3` curve is
`C^1`, while the derivative of `kappa161` is zero at zero and `-1` along
`1 / ((n + 1) * 2*pi)`, which tends to zero. Thus `kappa161` is not `C^1`, and the target's
existence conjunct is false. This refutes only the under-regularized frozen Lean encoding, not the
classical theorem with source-faithful coefficient regularity.

The negative theorem is an `M0-L` body for the exact negation only and supplies no positive-root
proof credit. Rev-5.6 section 3 requires an `H5` redirect for a refuted target, so this packet
proposes `H5/M5/R4` for authorized reconciliation. It does not rewrite predecessor statement,
registry, graph, instance, or scheduler authority. The historical positive registry still has the
open cut `{M0161-T-EXISTENCE, M0161-T-UNIQUENESS}`, and the prerequisite
`S56-M-0161-OBLIGATION_TREE` remains provisional `[_]` rather than master-accepted `[x]`.
The existing `root_of_existence_and_uniqueness` assumes both packages and is conditional
composition, not positive closure.

## Validation

All commands ran in this worker clone. The exact replay reused the automation-provided pinned Lake
closure without running `lake update`, `lake build`, dependency clone/fetch, checkout repair, or
other `.lake` mutation. Sources and oleans existed only in a disposable `/tmp` directory. The
replay resolved Lean with `lake env which lean` in the pinned mathlib subproject and then invoked
that binary directly with `--trust=0 -t0`, one thread, and nine existing library-path components.
The untracked `Formalizations/Lean/.lake` symlink is a shared warm cache, so this is narrow
nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; lifecycle planned; theorem incomplete |
| assigned-item DAG query | 0 | proof item `[ ]`, attempts 0; obligation-tree prerequisite `[_]`, attempts 1 |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...dadbe`; positive root remains open |
| `timeout 300 python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | canonical expression `c140d1d1...7f82`; all four structural mutations killed |
| isolated pinned-mathlib trust-zero replay below | 0 | statement, exact refutation, and positive-candidate-implies-`False` probe elaborated |
| replay source/output/type/axiom gates | 0 | no prohibited construct; exact negation passed; all three declarations use exactly `propext`, `Classical.choice`, and `Quot.sound` |
| mathlib revision/tree/tracked-status checks | 0 | manifest pin `8a178386...eea95`, tree `bdc39a31...c2b`, and empty tracked status confirmed |
| `python3 -m json.tool` plus packet-field assertions | 0 | fresh blocker packet parsed and its critical fields matched |
| wrapped new-file and scoped `git diff --check` commands | 0 | both reports and the complete scoped worker delta had no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent because the positive proof phase is blocked |

The successful replay printed:

```text
PROHIBITED_MATCH_COUNT=0
EXACT_NEGATION_TYPE=PASS
AXIOM_CLOSURE=propext,Classical.choice,Quot.sound
POSITIVE_CANDIDATE_IMPLIES_FALSE=PASS
Lean (version 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740)
LEAN_PATH_COMPONENTS=9
DIRECT_PINNED_TRUST_ZERO_REPLAY=PASS
```

The only diagnostic was a non-failing `unnecessarySeqFocus` linter warning at
`Counterexample.lean:70`. There was no Lean error, sorry warning, unsolved goal, or metavariable
diagnostic. Two preliminary report-side parser revisions exited `1` after the Lean elaborations
because their regular expressions did not recognize Lean's compact `negation` and probe output;
the corrected exact-type gates above passed without changing any theorem source or dependency.

Exact core replay, run from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
LEAN_ROOT=$ROOT/Formalizations/Lean
MATHLIB=$LEAN_ROOT/.lake/packages/mathlib
TMP=$(mktemp -d /tmp/thm-m-0161-slot55-finalreplay.XXXXXX)
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

A temporary `ConsistencyProbe.lean` imported `Counterexample` and checked

```lean
theorem positive_candidate_implies_false
    (h : FundamentalTheoremOfSpaceCurvesTarget) : False :=
  frozen_target_false h
```

under the same trust-zero invocation. The executed gate stripped comments, rejected `sorry`,
`admit`, `sorryAx`, bodyless declarations, unsafe/oracle constructs, Lean errors, sorry warnings,
and unsolved goals, required the exact negation and probe types, and required exactly the three
allowed axioms for `curvature_is_contDiffOn_one`, `frozen_target_false`, and the probe. The trap
removed every disposable file.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first repair
the target with source-faithful `C^1` or stronger coefficient regularity, or replace the positive
item with an accepted counterexample or barrier target. A repaired target then needs a new
canonical expression fingerprint, an append-only obligation-registry and typed-graph version
delta, and fresh statement mutation testing, source review, anchor audit, obligation-tree
construction, and proof execution in dependency order.

Because the positive proof phase is blocked rather than genuinely self-tested,
`.stage1-worker-selftest.json` remains absent. This packet is actionable blocker evidence, not proof
completion.
