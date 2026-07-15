# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `69662621a19907de342801b09124e8dfe3495e40`

Base tree: `fbfbc07e2045accdd0144baf892481a9bb6717f8`

Rechecked: `2026-07-15T18:53:46+08:00`

## Verdict

`blocked`. The exact frozen positive target is false, so no placeholder-free positive proof body
can truthfully inhabit it. The tracked `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

The proof item remains `[ ]`, with `root_closed=false` and `theorem_complete=false`. Its
obligation-tree prerequisite is only provisional `[_]`, pending master acceptance. No positive
proof body, receipt, provisional completion, audit completion, validation, release, theorem
completion, or master acceptance is claimed. Because the assigned phase is not genuinely
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Checked obstruction

The target assumes only `DifferentiableOn Real kappa (Set.Ioo a b)` while demanding a `C^3`
realizing curve. `curvature_is_contDiffOn_one` proves that the positive curvature of such a curve
must be `C^1` on the interval. The exact counterexample takes

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

This `kappa161` is differentiable everywhere and strictly positive on `(-1, 1)`, but its
derivative is zero at zero and `-1` along `1 / ((n + 1) * 2*pi)`, which tends to zero. Hence it is
not `C^1`, contradicting the regularity forced by the existence conclusion. This refutes only the
under-regularized frozen Lean proposition, not the classical theorem with source-faithful
coefficient regularity.

The negative declaration is a repo-local, kernel-checked body for the exact negation and an
`M0-L` candidate pending a node-specific receipt and master acceptance. It supplies no
positive-root credit. Rev-5.6 directs a refuted target to `H5` handling, so this report proposes
`H5/M5/R4` for authorized reconciliation. It does not rewrite the predecessor statement,
registry, graph, instance, or scheduler authority. The existing
`root_of_existence_and_uniqueness` is conditional composition: it assumes both open packages and
proves neither.

## Validation

All commands ran in this worker clone. The narrow Lean replay reused the automation-provided
pinned Lake closure without running `lake update`, `lake build`, dependency clone/fetch, checkout
repair, or any `.lake` mutation. Sources and oleans were copied or generated only under a
disposable `/tmp` directory and removed on exit. The untracked `Formalizations/Lean/.lake` symlink
points to the shared canonical cache, so this is warm-cache nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; lifecycle planned; theorem incomplete |
| assigned proof/prerequisite DAG query | 0 | proof `[ ]`, attempts 0; prerequisite `[_]`, attempts 1 |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...dadbe`; positive root remains open |
| `timeout --foreground --kill-after=5s 300 python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | canonical expression `c140d1d1...f82`; all four structural mutations killed |
| isolated `lake env which lean` plus direct Lean `--trust=0 -t0` replay below | 0 | statement and exact refutation elaborated; exact negation and source/output gates passed |
| refutation axiom and prohibited-construct scan | 0 | both key declarations use exactly `propext`, `Classical.choice`, and `Quot.sound`; zero prohibited matches |
| pinned package revision/tree/tracked-status checks | 0 | mathlib and flt-regular HEADs matched the manifest; both tracked worktrees were clean |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent because the positive proof phase is blocked |

The exact core replay, run from the repository root, was:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
LEAN_ROOT=$ROOT/Formalizations/Lean
TMP=$(mktemp -d /tmp/thm-m-0161-slot47-head69662621.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN=$(cd "$LEAN_ROOT" && env -u LEAN_PATH timeout 30 lake env which lean)
BASE_LEAN_PATH=$(cd "$LEAN_ROOT" && env -u LEAN_PATH timeout 30 lake env printenv LEAN_PATH)
cp "$TARGET/Statement.lean" "$TARGET/Counterexample.lean" "$TMP"/
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_LEAN_PATH" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
  "$TMP/Statement.lean" >"$TMP/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Counterexample.olean" \
  "$TMP/Counterexample.lean" >"$TMP/counterexample.out" 2>&1
```

After those commands, an executed Python parser read `Counterexample.lean` and
`counterexample.out`. It stripped comments, rejected `sorry`, `admit`, `sorryAx`, bodyless
declarations, unsafe/oracle constructs, Lean errors, and sorry warnings; required the exact
negation type; and required the exact allowed axiom set for `curvature_is_contDiffOn_one` and
`frozen_target_false`. Its exact body and the other small query/assertion commands are recorded in
the structured companion's `exact_command_appendix`. Lean printed version `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib was
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The temporary olean hashes were
`85d9e8d7...884e` for the statement and `ed0dbd7d...61ca` for the counterexample. The only
diagnostic was a non-failing `unnecessarySeqFocus` linter warning at `Counterexample.lean:70`.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first repair
the target with source-faithful `C^1` or stronger coefficient regularity, or replace the positive
item with an accepted counterexample or barrier target. A repaired target then needs a new
canonical expression fingerprint, an append-only obligation-registry and typed-graph version
delta, and fresh statement mutation testing, source review, anchor audit, obligation-tree
construction, and proof execution in dependency order.

This report is current-base negative evidence only. It does not satisfy `S56-M-0161-PROOF` and
supports no theorem-completion claim.
