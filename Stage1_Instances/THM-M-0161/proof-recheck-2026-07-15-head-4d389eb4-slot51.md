# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `4d389eb47e043f6f44925a418baee0d034f764ba`

Base tree: `64faabd76665273032b8cb1554b90655b5c94256`

Rechecked: `2026-07-15T17:08:39+08:00`

## Verdict

`blocked`. No positive proof body can truthfully inhabit the exact frozen target. The already
tracked, placeholder-free `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

The proof item remains `[ ]`. No source, statement, registry, graph, scheduler state, proof body,
or unrelated target was changed. Because the assigned positive phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.

The target asks every differentiable positive curvature to be realized by a `C^3` curve. The
checked obstruction uses

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

`kappa161` is differentiable and positive on the interval, but its derivative is zero at zero and
`-1` along `1 / ((n + 1) * 2*pi)`, a sequence tending to zero. Hence it is not `C^1`. In contrast,
`curvature_is_contDiffOn_one` proves that the positive curvature of any admitted `C^3` realization
is `C^1`. The existence conjunct is therefore false; uniqueness is immaterial. This refutes only
the under-regularized Lean encoding, not the classical theorem with source-faithful coefficient
regularity.

The negative declaration is `M0-L` for the exact negation only and supplies no positive-root proof
credit. Under the rev-5.6 `H5` rule, ordinary proof execution must stop pending an authorized
corrected statement, counterexample target, or barrier target. This report proposes `H5/M5/R4` for
master reconciliation but does not rewrite predecessor authority. The instance still records
`H1/M4/R4`, while the typed graph records `H3/M3/R4` at its root.

The historical positive cut remains `{M0161-T-EXISTENCE, M0161-T-UNIQUENESS}`.
`root_of_existence_and_uniqueness` assumes those packages and therefore cannot close either one.
The prerequisite `S56-M-0161-OBLIGATION_TREE` is also only provisional `[_]`, not accepted `[x]`.

## Validation

All commands ran in this worker clone. Lean checks reused the existing pinned Lake closure without
mutating it. The worker `.lake` entry is an automation-provided symlink to a shared warm cache, so
these are narrow nonrelease blocker checks, not release evidence. No `lake update`, `lake build`,
dependency clone/fetch, or checkout repair was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; theorem incomplete |
| assigned-item DAG query | 0 | proof `[ ]`, attempts 0; prerequisite `[_]`, attempts 1 |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...dadbe`; positive root open |
| `python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | exact expression `c140d1d1...7f82`; all four structural mutations killed |
| preliminary disposable consistency-probe invocation | 1 | Lean rejected a `/tmp` input outside the mistakenly retained repository `--root`; no theorem result was claimed, and the invocation was corrected to `--root="$TMP"` |
| isolated trust-zero replay below | 0 | statement, exact refutation, and a positive-candidate-implies-`False` probe elaborated |
| source, type, axiom, and output gates | 0 | no prohibited construct or Lean error/sorry warning; exact negation passed; declarations use exactly `propext`, `Classical.choice`, and `Quot.sound` |
| mathlib and `flt-regular` revision/tree/status checks | 0 | pinned revisions recorded and both tracked dependency worktrees clean |
| independent second-agent trust-zero replay | 0 | exact negation and the same axiom closure independently confirmed in a separate disposable directory |
| `python3 -m json.tool` plus blocker-field/hash assertions | 0 | structured report is valid JSON and its frozen input hashes and fail-closed fields match |
| new-file and scoped `git diff --check` | 0 | both fresh artifacts and the complete owned-path delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent because the positive phase is blocked |

The core replay copied `Statement.lean` and `Counterexample.lean` into a disposable `/tmp`
directory, resolved the existing environment with `lake env which lean` and `lake env printenv
LEAN_PATH`, and ran:

```bash
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_PATH" \
  timeout --foreground --kill-after=5s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_PATH" \
  timeout --foreground --kill-after=5s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Counterexample.olean" "$TMP/Counterexample.lean"
```

A disposable `Consistency.lean` imported `Counterexample` and checked

```lean
theorem consistency_probe
    (h : FundamentalTheoremOfSpaceCurvesTarget) : False :=
  frozen_target_false h
```

under the same `--trust=0 -t0` invocation. The replay printed Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, exact negation, consistency probe, and the allowed
axiom closure. The sole diagnostic was the known non-failing `unnecessarySeqFocus` linter warning
at `Counterexample.lean:70`.

This pair is additive current-base revalidation. It repeats already integrated negative mathematics
against a newer repository base whose target source hashes and relevant DAG projections are
unchanged. It is neither a new proof body nor a blanket supersession of prior or accepted evidence.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first require
`C^1` or stronger curvature regularity (or otherwise exclude the checked counterexample without
assuming the conclusion), or redirect the item to a counterexample/barrier target. Any repair needs
a new target fingerprint, append-only registry and typed-graph version delta, and fresh statement,
source, anchor, obligation-tree, and proof work in dependency order.

This is actionable blocker evidence, not proof completion.
