# THM-M-0161 current-base proof hard-stop

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `fc1568a2997ca815b767b8cc172f3d4d339bf3b9`

Base tree: `635319193989301e577a430446e682952c51c538`

Recorded: `2026-07-15T16:07:44+08:00`

## Verdict

`blocked`. The exact frozen positive proposition cannot receive a truthful proof body because its
placeholder-free exact negation is already kernel checked. The proof item remains `[ ]`; this
packet claims no positive proof receipt, provisional completion, audit completion, validation,
release, theorem completion, or master acceptance.

`Statement.lean` assumes only `DifferentiableOn` prescribed curvature while requiring a realizing
curve to be `ContDiffOn Real 3`. `Counterexample.lean` proves every positive curvature realized by
such a curve is `ContDiffOn Real 1`, and then chooses

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

This prescribed curvature is differentiable and positive on the interval, but it is not `C^1` at
zero. Lean checks the exact declaration

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not Stage1Instances.THM_M_0161.FundamentalTheoremOfSpaceCurvesTarget
```

This body is `M0-L` evidence for the exact negation only. It gives no positive-root proof credit
and does not refute the classical theorem with source-faithful coefficient regularity. Any positive
candidate for the frozen target would immediately prove `False` by applying
`frozen_target_false`.

The workflow dependency also remains unaccepted: `S56-M-0161-OBLIGATION_TREE` is `[_]`, pending
master acceptance. Its final Lean theorem conditionally assumes the complete existence and
uniqueness packages and proves neither, so it cannot substitute for the requested root. The
tracked dossier contains repeated rechecks of this same obstruction; another unchanged positive
proof attempt is not a valid retry.

## Validation

All commands reused the automation-provided pinned `.lake` closure. No `lake update`, `lake build`,
dependency clone/fetch, checkout, or `.lake` mutation was performed. The worker clone's `.lake` is
an untracked symlink to the shared canonical cache, so the Lean replay is narrow nonrelease blocker
evidence, not a hermetic release receipt.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; L0/rework-required; theorem incomplete |
| assigned-item DAG query | 0 | proof `[ ]`, attempts 0; prerequisite `[_]`, attempts 1 |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 edges passed; positive root open |
| `timeout 300 python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | canonical expression `c140d1d...f82`; four mutations killed |
| isolated direct Lean `--trust=0 -t0` replay below | 0 | statement and exact negation elaborated; exact type and axiom reports passed |
| prohibited-construct scan of `Counterexample.lean` | 0 | no prohibited proof device or bodyless declaration match |
| pinned mathlib revision/tree and tracked-status checks | 0 | revision `8a178386...eea95`, tree `bdc39a31...c2b`, tracked status empty |
| JSON parse, packet assertions, and exact changed-path comparison | 0 | blocked-state fields parsed and both owned changes matched |
| wrapped new-file checks and scoped `git diff --check` | 0 | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent |

The successful narrow replay, run from the repository root, was:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
LEAN_ROOT=$ROOT/Formalizations/Lean
TMP=$(mktemp -d /tmp/thm-m-0161-slot55-headfc1568a2.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN=$(cd "$LEAN_ROOT" && env -u LEAN_PATH timeout 30 lake env which lean)
BASE_LEAN_PATH=$(cd "$LEAN_ROOT" && env -u LEAN_PATH timeout 30 lake env printenv LEAN_PATH)
cp "$TARGET/Statement.lean" "$TARGET/Counterexample.lean" "$TMP"/
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_LEAN_PATH" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
  "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" timeout 300 \
  "$LEAN" --trust=0 -t0 --root="$TMP" -o "$TMP/Counterexample.olean" \
  "$TMP/Counterexample.lean"
```

Lean printed the exact negation and reported exactly `propext`, `Classical.choice`, and
`Quot.sound` for both `curvature_is_contDiffOn_one` and `frozen_target_false`. The temporary
`Statement.olean` hash was `85d9e8d7...4884e`; the temporary `Counterexample.olean` hash was
`ed0dbd7d...bd61ca`. The only diagnostic was the non-failing `unnecessarySeqFocus` linter warning
at `Counterexample.lean:70`; there was no Lean error, sorry warning, unsolved goal, or metavariable
diagnostic. The trap removed the disposable files.

## Retry Condition

Do not retry the unchanged positive target. Redirect to authorized source and statement review,
then strengthen the coefficient hypothesis to a source-faithful `C^1` or stronger condition, or
replace the item with an accepted counterexample/barrier target. Any repaired target needs a new
canonical expression fingerprint, an append-only obligation-registry and typed-graph version, and
fresh statement, source, anchor, obligation-tree, and proof phases in dependency order.

Because the assigned positive proof phase is blocked rather than genuinely self-tested,
`.stage1-worker-selftest.json` is deliberately absent.
