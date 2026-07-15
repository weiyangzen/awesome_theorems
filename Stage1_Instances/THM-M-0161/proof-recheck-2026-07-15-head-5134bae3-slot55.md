# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `5134bae303d5f5104698e8c96d7af4c26306eb47`

Base tree: `54e4bd2793df37c5451b86659fbd95a83504c25a`

Rechecked: `2026-07-15T16:33:09+08:00`

## Verdict

`blocked`. The exact frozen positive target cannot truthfully receive the requested proof body.
The already tracked, placeholder-free `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

The proof item remains `[ ]`. No positive proof body, proof receipt, provisional completion, audit
completion, validation, release, theorem completion, or master acceptance is claimed. Because the
assigned phase is not genuinely complete, the root `.stage1-worker-selftest.json` is deliberately
absent.

The frozen target assumes only `DifferentiableOn Real kappa (Ioo a b)` while requiring a `C^3`
realizing curve. The checked obstruction chooses

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

This curvature is differentiable everywhere and positive on the interval, but its derivative is
zero at zero and `-1` along `1 / ((n + 1) * 2*pi)`, which tends to zero. Therefore it is not `C^1`.
Meanwhile, `curvature_is_contDiffOn_one` proves that every positive curvature realized by an
admitted `C^3` curve is `C^1`. Thus the target's existence conjunct is false. This refutes only the
under-regularized frozen Lean encoding, not the classical theorem with source-faithful coefficient
regularity.

The negative declaration is an `M0-L` body for the exact negation only. It gives no positive-root
proof credit. Rev-5.6 section 3.1 requires ordinary proof execution of an `H5` target to stop and
redirect to an authorized corrected statement, counterexample, or barrier target. This packet
proposes `H5/M5/R4` for later authoritative reconciliation; it does not change predecessor state,
the frozen registry, the typed graph, or the scheduler.

The historical positive cut remains `{M0161-T-EXISTENCE, M0161-T-UNIQUENESS}`. The checked theorem
`root_of_existence_and_uniqueness` merely assumes those complete packages and composes them, so it
cannot provide positive closure. In addition, the prerequisite `S56-M-0161-OBLIGATION_TREE` is
provisional `[_]`, not master-accepted `[x]`.

## Validation

All commands ran in this worker clone. The Lean checks used the existing pinned Lake environment,
Lean `4.29.0`, `--trust=0`, one thread, and disposable sources and oleans under `/tmp`. No `lake
update`, `lake build`, dependency clone/fetch, checkout repair, or other `.lake` mutation was run.
The worker's `.lake` path is an automation-provided symlink to a shared warm cache, so this is
narrow nonrelease blocker evidence, not a release receipt.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; theorem incomplete |
| assigned-item DAG query | 0 | proof `[ ]`, attempts 0; prerequisite `[_]`, attempts 1 |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...dadbe`; historical positive root open |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | exact expression `c140d1d1...7f82`; all four structural mutations killed |
| final concurrent rerun of that statement checker | terminated | a later resource-contended duplicate exceeded the tool-call wait; its child was stopped and its temporary source removed; it is not claimed as evidence |
| isolated `lake env lean --trust=0 -t0` replay below | 0 | statement, exact refutation, conditional composition, and a positive-candidate-implies-`False` probe elaborated |
| exact-type, axiom, and prohibited-output gates | 0 | exact negation passed; zero prohibited output matches; key declarations use exactly `propext`, `Classical.choice`, and `Quot.sound` |
| mathlib and `flt-regular` revision/tree/status checks | 0 | manifest pins matched and both tracked worktrees were clean |
| `git diff --check` and JSON assertions | 0 | the blocker packet and complete scoped delta passed |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent because the positive proof phase is blocked |

The core replay copied `Statement.lean`, `Counterexample.lean`, and `ObligationTree.lean` to a
disposable directory, resolved the existing environment with `lake env printenv LEAN_PATH`, and
ran:

```bash
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Counterexample.olean" "$TMP/Counterexample.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/ObligationTree.olean" "$TMP/ObligationTree.lean"
```

A separate disposable `ConsistencyProbe.lean` imported `Counterexample` and kernel-checked

```lean
theorem positive_candidate_implies_false
    (h : FundamentalTheoremOfSpaceCurvesTarget) : False :=
  frozen_target_false h
```

under the same trust-zero invocation. The replay printed the exact negation and reported only
`propext`, `Classical.choice`, and `Quot.sound` for `curvature_is_contDiffOn_one`,
`frozen_target_false`, `root_of_existence_and_uniqueness`, and the consistency probe. The only
diagnostic was a non-failing `unnecessarySeqFocus` linter warning at `Counterexample.lean:70`; there
was no Lean error or sorry warning.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first repair
the target with source-faithful `C^1` or stronger coefficient regularity, or replace the positive
item with an accepted counterexample or barrier target. A repaired target then requires a new
canonical expression fingerprint, an append-only registry and typed-graph version delta, and fresh
statement, source, anchor, obligation-tree, and proof work in dependency order.

This is actionable blocker evidence, not proof completion.
