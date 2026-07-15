# THM-M-0161 proof hard-stop

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `d1933ff69a2dc943cd3203497ab9cf9fe79f4e58`

Base tree: `8eca89518ce485e51886ee61d92b6251d0df7dc7`

Recorded: `2026-07-15T15:50:47+08:00`

## Verdict

`blocked`. Ordinary positive-root execution must stop because the exact frozen proposition has a
placeholder-free, kernel-checked refutation. The item remains `[ ]`; this packet claims no proof
completion, audit completion, validation, release, theorem completion, or master acceptance.

`Statement.lean` assumes only `DifferentiableOn` prescribed curvature while requiring a realizing
curve to be `ContDiffOn Real 3`. `Counterexample.lean` proves that every positive curvature realized
by such a curve is `ContDiffOn Real 1`, then uses

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

The prescribed curvature is differentiable and positive on the interval but not `C^1` at zero.
Lean therefore checks the exact declaration

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not Stage1Instances.THM_M_0161.FundamentalTheoremOfSpaceCurvesTarget
```

This is an `M0-L` body for the exact negation only. It supplies no positive-root proof credit and
does not refute the classical theorem with source-faithful coefficient regularity. Any proposed
positive inhabitant would yield `False` by applying `frozen_target_false`.

The independent dependency gate also remains closed: `S56-M-0161-OBLIGATION_TREE` is only `[_]`,
pending master acceptance. Its checked final theorem conditionally assumes complete existence and
uniqueness packages; it proves neither package and cannot be substituted for the requested root.

The tracked dossier already contains repeated current-base rechecks of the same obstruction. Under
the five-tick split rule, scheduling another unchanged positive proof attempt is not a valid retry.
This packet records the current-base hard stop rather than duplicating a proof body or modifying
predecessor authority.

## Validation

All checks reused the automation-provided pinned `.lake` closure. No `lake update`, `lake build`,
dependency clone/fetch, checkout, or `.lake` mutation was performed. The worker clone's `.lake` is
an untracked symlink to the shared canonical cache, so the Lean replay is narrow nonrelease blocker
evidence rather than a hermetic release receipt.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | Rank 660, planned, L0/rework_required, theorem incomplete |
| assigned-item `jq` query | 0 | Proof `[ ]`, attempts 0; obligation-tree prerequisite `[_]`, attempts 1 |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations, 44 typed edges, open M3 root |
| `timeout 300 python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | Canonical expression `c140d1d...f82`; four mutations killed; pinned mathlib revision matched |
| isolated `lake env lean --trust=0 -t0` replay below | 0 | Statement and exact refutation elaborated; both key axiom reports were exactly `propext`, `Classical.choice`, `Quot.sound` |
| prohibited-construct scan of comment-stripped `Counterexample.lean` | 0 | No prohibited proof device or bodyless declaration match |
| pinned mathlib revision/tree and tracked-status checks | 0 | Revision `8a178386...95`, tree `bdc39a31...c2b`, tracked status empty |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent |

The successful narrow Lean replay was run from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-0161
LEAN_ROOT=$ROOT/Formalizations/Lean
TMP=$(mktemp -d /tmp/thm-m-0161-slot55.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET/Statement.lean" "$TARGET/Counterexample.lean" "$TMP"/
(
  cd "$LEAN_ROOT"
  timeout 300 lake env lean --trust=0 -t0 --root="$TMP" \
    -o "$TMP/Statement.olean" "$TMP/Statement.lean"
  LEAN_PATH="$TMP" timeout 300 lake env lean --trust=0 -t0 --root="$TMP" \
    -o "$TMP/Counterexample.olean" "$TMP/Counterexample.lean"
)
```

Lean 4 was version `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
The only diagnostic was the non-failing `unnecessarySeqFocus` linter warning at
`Counterexample.lean:70`.

## Retry condition

Do not retry the unchanged positive target. Redirect to authorized source and statement review,
then either strengthen the coefficient hypothesis to a source-faithful `C^1` or stronger condition,
or replace the item with an accepted counterexample/barrier target. Any repaired target requires a
new canonical expression fingerprint, an append-only obligation-registry and typed-graph version,
and fresh statement, source, anchor, obligation-tree, and proof phases in dependency order.

Because the assigned positive proof phase is blocked rather than genuinely self-tested,
`.stage1-worker-selftest.json` is deliberately absent.
