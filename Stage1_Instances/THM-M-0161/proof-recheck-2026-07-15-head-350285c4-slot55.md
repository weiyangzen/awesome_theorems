# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `350285c48208616b6e3ad74154d9183d16523cfa`

Base tree: `c4edebc115ec954e4940ed5faaa3ffacd4e56091`

Rechecked: `2026-07-15T15:24:08+08:00`

## Verdict

`blocked`. The exact frozen positive target cannot receive a truthful proof body because the
repository-local `Counterexample.lean` kernel-checks the placeholder-free declaration

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

The proof item therefore remains `[ ]`. No positive proof receipt, provisional completion, audit
completion, validation, release, theorem completion, or master acceptance is claimed. The root
`.stage1-worker-selftest.json` is deliberately absent because the assigned positive proof phase is
not genuinely complete.

The target assumes only `DifferentiableOn Real kappa (Set.Ioo a b)` but demands a `C^3` realizing
curve. The checked obstruction chooses

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

This curvature is differentiable everywhere and positive on the interval. However,
`curvature_is_contDiffOn_one` proves that the positive curvature of every admitted `C^3` curve is
`C^1`. The derivative of `kappa161` is zero at zero and `-1` along
`1 / ((n + 1) * (2*pi))`, which tends to zero, so `kappa161` is not `C^1`. The existence conjunct
is false. This refutes the under-regularized Lean encoding, not the classical theorem with
source-faithful coefficient regularity.

The negative theorem is an `M0-L` body for the exact negation only and supplies no positive-root
credit. Rev-5.6 therefore requires an `H5` redirect. This packet proposes `H5/M5/R4` for authorized
reconciliation without changing predecessor statement, registry, graph, instance, or scheduler
authority. The existing graph still records `H3/M3/R4`, and `instance.json` records `H1/M4/R4`.
The historical positive cut remains `{M0161-T-EXISTENCE, M0161-T-UNIQUENESS}`. The conditional
`root_of_existence_and_uniqueness` assumes both packages and cannot close the root.

## Validation

All commands ran in this worker clone. The Lean replay used the existing pinned Lake closure,
created sources and oleans only under disposable `/tmp`, and invoked the resolved Lean binary with
`--trust=0 -t0`. No `lake update`, `lake build`, dependency clone/fetch, network access, checkout
repair, or `.lake` mutation was performed. The untracked `Formalizations/Lean/.lake` symlink points
to the canonical shared cache, so this is narrow nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; L0/rework-required; theorem incomplete |
| assigned-item DAG query | 0 | proof `[ ]`, attempts 0; prerequisite `[_]`, attempts 1 and pending master acceptance |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 edges passed; denominator `48173f90...dadbe`; positive root open |
| isolated trust-zero replay below | 0 | exact statement and refutation elaborated; exact negation, placeholder, output, and axiom gates passed |
| mathlib revision/tree/status checks | 0 | revision `8a178386...eea95`, tree `bdc39a31...c2b`, empty tracked status |
| source, authority, toolchain, manifest, and Lean binary hashes | 0 | all hashes in the JSON packet confirmed |
| `python3 -m json.tool` plus `jq` packet assertions | 0 | JSON parsed and critical blocked-state fields matched |
| wrapped new-file checks plus scoped `git diff --check` | 0 | both reports and the scoped delta had no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` plus temporary-source check | 0 | completion self-test absent and no checker `tmp*.lean` remained |

The replay printed:

```text
PROHIBITED_MATCH_COUNT=0
EXACT_NEGATION_TYPE=PASS
AXIOM_CLOSURE=propext,Classical.choice,Quot.sound
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
Lean (version 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740)
DIRECT_PINNED_TRUST_ZERO_REPLAY=PASS
```

The only diagnostic was the non-failing `unnecessarySeqFocus` linter warning at
`Counterexample.lean:70`. There was no Lean error, sorry warning, unsolved goal, or metavariable
diagnostic.

The core replay, run from the repository root, was:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
LEAN_ROOT=$ROOT/Formalizations/Lean
TMP=$(mktemp -d /tmp/thm-m-0161-slot55-replay.XXXXXX)
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

The output gate stripped comments, rejected `sorry`, `admit`, `sorryAx`, bodyless declarations,
unsafe/oracle constructs, Lean errors, sorry warnings, and unsolved goals, required the exact
negation type, and required exactly `propext`, `Classical.choice`, and `Quot.sound` for
`curvature_is_contDiffOn_one` and `frozen_target_false`. The trap removed all disposable files.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first repair
the target with source-faithful `C^1` or stronger coefficient regularity, or replace the positive
item with an accepted counterexample or barrier target. A repaired target then requires a new
canonical expression fingerprint, an append-only obligation-registry and typed-graph version delta,
and fresh statement mutation testing, source review, anchor audit, obligation-tree construction,
and proof execution in dependency order.

This is actionable blocker evidence, not proof completion.
