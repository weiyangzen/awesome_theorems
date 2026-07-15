# THM-M-0161 proof-phase recheck at base 6bf9ee93

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Rechecked: `2026-07-16T04:51:15+08:00`

## Verdict

`blocked`. A placeholder-free positive proof cannot truthfully inhabit the exact frozen target. The
tracked `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

No positive proof body, proof receipt, provisional completion, audit completion, validation,
release, theorem completion, or master acceptance is claimed. The proof item remains `[ ]`, with
`root_closed=false` and `theorem_complete=false`. Its obligation-tree prerequisite is only
provisional `[_]`, not master accepted `[x]`. Because this positive proof phase is not genuinely
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Dependency Context

The required schema-1.1 ledger was created before proof execution and binds graph digest
`73e99d22...40eca`, context digest `0151ccc2...116`, and this exact base revision. The v2 node has no
hard parent, transitive ancestor, hard edge, or direct reuse hint. All three weak shared-module
groups were nevertheless inspected and decided:

| Group | Inspected member | Decision | Boundary |
|---|---|---|---|
| `SHARED-MODULE-015f6388efc48e5f` | `THM-M-1332` | `not_applicable` | Picard-Lindelof local existence is only a supporting ODE interface, and the member has no canonical root or accepted proof body |
| `SHARED-MODULE-afda69317376545a` | `THM-M-1332` | `not_applicable` | Gronwall uniqueness is only an ODE ingredient and not the prescribed-invariants existence or rigid-motion theorem |
| `SHARED-MODULE-c42df17c4a3d5abc` | `THM-M-0162` | `not_applicable` | Cross-product algebra and pointwise Frenet-Serret identities do not construct or uniquely characterize the required curve |

The repository's exact ledger validator passed with zero hard-parent inspections, exactly three
decisions, no accepted reuse, and no unresolved compatibility obligations. These nonblocking hints
supply no checkbox or proof credit.

## Checked Obstruction

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
credit. Rev-5.6 requires an `H5` redirect when the exact target is refuted. This packet therefore
proposes `H5/M5/R4` for authorized reconciliation but does not rewrite the predecessor statement,
instance, registry, typed graphs, or task-state authority.

## Validation

All commands ran in this worker clone. The existing pinned Lake closure was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
trust-zero replay copied source and wrote oleans only under a disposable `/tmp` directory. The
pre-existing untracked `Formalizations/Lean/.lake` symlink points to the canonical shared cache, so
this is narrow warm-cache, nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | current rev-5.6 standard checks passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 before artifacts; 1 after | pre-edit graph passed; post-artifact deterministic inventory sees the new blocker JSON, which only the master may reconcile |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique L0/rework-required targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; theorem incomplete |
| exact repository ledger validator | 0 | `DEPENDENCY_REUSE_LEDGER_VALID=PASS`; zero inspections; three decisions |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations, 44 typed edges, denominator `48173f90...dadbe`; predecessor positive root open |
| `python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | canonical expression `c140d1d1...7f82` and all four structural mutations passed |
| isolated direct pinned trust-zero replay below | 0 | exact negation, axiom closure, source scan, and output scan passed |
| mathlib and `flt-regular` revision/tree/status checks | 0 | both pins matched and both tracked dependency worktrees were clean |
| `python3 scripts/stage1_execution_cron.py --validate-only --workers 0` | 1 | stopped at the same checked-in versus freshly generated evidence-inventory difference; no semantic dependency context changed |

The post-artifact aggregate failure is fail-closed and retained here rather than hidden. The graph
generator correctly excludes `dependency-reuse-ledger.json` from shared-group discovery, so the
recorded graph/context digests remain stable, but its general `structured_json_files` inventory also
lists every blocker JSON. Adding the required target-owned blocker therefore makes a fresh projection
inventory differ from the checked-in authority. This worker is prohibited from editing or
regenerating `Docs/Stage1_Theorem_DAG_v2.json`; the integration lane must reconcile that derived
inventory after preserving the blocker.

The successful isolated replay, run from the repository root, was:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
LEAN_ROOT=$ROOT/Formalizations/Lean
LEAN=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
TMP=$(mktemp -d /tmp/thm-m-0161-6bf9ee93-slot44-replay.XXXXXX)
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
cp "$TARGET/Statement.lean" "$TARGET/Counterexample.lean" "$TMP/"
LIBS=$(find -L "$LEAN_ROOT/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd: -)
TOOLCHAIN=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean

LEAN_NUM_THREADS=1 LEAN_PATH="$LIBS:$TOOLCHAIN" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
  "$TMP/Statement.lean" >"$TMP/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LIBS:$TOOLCHAIN" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Counterexample.olean" \
  "$TMP/Counterexample.lean" >"$TMP/counterexample.out" 2>&1
```

A parser stripped comments, rejected `sorry`, `admit`, `sorryAx`, bodyless/unsafe/oracle
constructs, Lean errors, sorry warnings, and unsolved goals, required the exact negation type, and
required exactly the three recorded axioms for both key declarations. It printed:

```text
PROHIBITED_MATCH_COUNT=0
EXACT_NEGATION_TYPE=PASS
AXIOM_CLOSURE=propext,Classical.choice,Quot.sound
Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740
MATHLIB_HEAD=8a178386ffc0f5fef0b77738bb5449d50efeea95
MATHLIB_TREE=bdc39a3123201dae413a9d9be56ec242c19e5c2b
DIRECT_PINNED_TRUST_ZERO_REPLAY=PASS
```

The only diagnostic was a non-failing `unnecessarySeqFocus` linter warning at
`Counterexample.lean:70`. There was no Lean error, sorry warning, unsolved goal, or prohibited proof
construct.

## Retry Condition

Do not retry the unchanged positive root. Authorized source and statement review must first repair
the coefficient regularity to `C^1` or stronger, or replace the task with an accepted
counterexample/barrier target. A corrected target then needs a new canonical fingerprint, an
append-only obligation-registry and typed-graph version delta, and fresh statement mutation, source,
anchor, obligation-tree, and proof execution in dependency order.

This is current-base negative evidence only. It does not satisfy `S56-M-0161-PROOF` and supports no
theorem-completion claim.
