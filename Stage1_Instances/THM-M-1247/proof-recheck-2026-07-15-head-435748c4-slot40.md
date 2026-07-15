# THM-M-1247 proof recheck at `435748c4` (slot40)

Item: `S56-M-1247-PROOF`

Theorem: `THM-M-1247`

Base revision: `435748c4550bad6c03c34931d309befe9658460d`

Base tree: `5354633764fc606c80fe66838d43b491165ea056`

Run date: `2026-07-15`

## Verdict

`blocked`. The proof phase is not complete, and no
`.stage1-worker-selftest.json` was emitted.

The tracked `Proof.lean` is placeholder-free and kernel-checks an inhabitant of
the frozen Lean proposition. It does not prove the canonical human Rellich
inequality selected by the intake. Two statement-mapping defects make its
admissible functions analytic functions on the finite Pi/sup-norm space rather
than arbitrary smooth functions on Euclidean `L2` space:

1. `ContDiff Real top` infers `top : WithTop ENat`, mathlib's analytic order
   `omega`; smooth infinity is `((top : ENat) : WithTop ENat)`.
2. `Euclidean n := Fin n -> Real` carries the ordinary finite Pi supremum norm;
   mathlib's `EuclideanSpace Real (Fin n)` is `PiLp 2` with the `L2` norm.

Support avoidance therefore makes the admitted analytic function vanish near
the origin, analytic uniqueness makes it identically zero, and simplification
closes only this malformed backend encoding. Blueprint sections 5/5.1 and 10.8
forbid proof credit for an unmapped or differently typed target.

The first failed gate remains the section 5.1 exact statement/source mapping
gate, proposed at `M1247-S-DOMAIN`. The frozen 13-obligation registry is
structurally valid but semantically stale. The predecessor
`S56-M-1247-OBLIGATION_TREE` is only `[_]`, not master-accepted.

## Current-Base Delta

The preceding current-style blocker packet was written against
`3ef7c6dff0c66bc8c02e842f4cea6b9936349094`. From that base to this base, the
only `THM-M-1247` additions are that packet's JSON and Markdown files. The
canonical statement, proof body, obligation tree, registry, typed graphs,
validation specs, anchor audit, target-manifest entry, and execution skill did
not change. Authority changes at HEAD concern unrelated targets; this proof
item remains `[ ]`, with `attempts: 0` and no children.

There were already 23 integrated `proof-recheck-*.json` files and 23 matching
Markdown companions before this packet. This exceeds the section 10.2 rule to
split an item after five unresolved execution ticks. The worker cannot edit the
master-owned DAG. The scheduler must stop redispatching this unchanged proof
item, reopen the statement phase, and create dependency-legal repair children.

## Validation

All credited Lean checks reused the automation-provided symlink to canonical
pinned artifacts. No update, build, clone, fetch, network request, or `.lake`
mutation was performed. Fresh working outputs were confined to a temporary
directory under `/tmp` and removed at command exit.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_statement.py` | 0 | Expression SHA-256 `4697dbba...5c90e`; all four recorded mutations killed. This checks the frozen encoding, not its human-claim mapping. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | Three pinned mathlib candidate families checked; exact external candidates `0`; terminal result open. |
| `python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | 13 obligations, 34 typed edges, denominator `9df3b5e9...79a590`; root open at `M3`, with six analytic obligations at `M4`. |
| Isolated pinned `lake env lean --trust=0` recipe below | 0 | Fresh `Statement.olean`, `Proof.lean`, and `ObligationTree.lean` elaborated; exact frozen type checked; axioms exactly `propext`, `Classical.choice`, `Quot.sound`. |
| `sed -n '104,118p' .../ContDiff/FTaylorSeries.lean` | 0 | Pinned mathlib distinguishes analytic `omega` from smooth `infinity`. |
| `sed -n '32,40p;96,120p' .../InnerProductSpace/PiL2.lean` | 0 | Pinned mathlib defines `EuclideanSpace` as `PiLp 2`. |
| `rg -n -i 'Rellich\|Hardy[-_ ]?Rellich\|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1, expected | No exact theorem candidate in readable pinned package sources. |
| Prohibited proof-token scan over `Statement.lean`, `Proof.lean`, and `ObligationTree.lean` | 1, expected | No `sorry`, `admit`, `sorryAx`, declared `axiom`, `unsafe`, or `opaque` token; not a transitive provenance audit. |
| `git diff --name-status 3ef7c6df..HEAD` over target semantic inputs, authorities, target manifest, and skill | 0 | Only the preceding target blocker pair and unrelated authority-state changes; no target semantic input, manifest entry, or skill change. |
| Count integrated `proof-recheck-*.json` files before this packet | 0 | `23`, beyond the mandatory five-tick split threshold. |
| JSON parse plus fail-closed packet identity/hash/state assertions | 0 | Base, hashes, paths, blocked state, scheduler escalation, and deliberate self-test absence agree. |
| `git diff --check` plus no-index whitespace checks for both new packet files | 0 diagnostics | No whitespace errors; no-index returns 1 only because each file is an addition. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false worker-completion packet exists. |

The successful narrow Lean replay was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
MATHLIB="$LEAN_ROOT/.lake/packages/mathlib"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-435748c4-slot40.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET"/{Statement,Proof,ObligationTree}.lean "$TMP/"
BASE_LEAN_PATH="$(find -L "$LEAN_ROOT/.lake/packages" -type d \
  -path '*/.lake/build/lib/lean' -print | LC_ALL=C sort | paste -sd:):\
$(readlink -f "$LEAN_ROOT/.lake")/build/lib/lean:\
$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
cd "$MATHLIB"
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
  --root="$TMP" -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
  --root="$TMP" "$TMP/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
  --root="$TMP" "$TMP/ObligationTree.lean"
```

The proof-specific output was:

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget : RellichInequalityTarget
'Stage1Instances.THM_M_1247.frozen_top_is_analytic_order' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.analytic_avoidance_eq_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.rellichInequalityTarget' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.root_of_coreRellichEstimate' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The expanded statement output contains `@Top.top (WithTop ENat)` together with
finite-Pi `@Pi.normedAddCommGroup` and `@Pi.normedSpace` instances, independently
confirming both mapping defects.

## Retry Condition

Do not dispatch `S56-M-1247-PROOF` unchanged again. Reopen
`S56-M-1247-STATEMENT` under an authorized assignment, use
`EuclideanSpace Real (Fin n)` and
`ContDiff Real ((top : ENat) : WithTop ENat)`, rerun exact-expression and four
mutation gates, then publish a versioned obligation-registry/typed-graph delta
and downstream invalidations. Split those repairs into dependency-legal child
tasks before resuming the genuine weighted integration-by-parts, sharp Hardy,
core-estimate, and transport proof.

## Status Boundary

This is current-base blocker and scheduler-escalation evidence under the owned
target path. It does not satisfy `S56-M-1247-PROOF`. The item remains `[ ]`;
there is no worker self-test, accepted receipt, audit-completion, validation,
release, or theorem-completion claim.
