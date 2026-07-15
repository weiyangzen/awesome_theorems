# THM-M-1247 proof recheck at `51c2828e` (slot42)

Item: `S56-M-1247-PROOF`

Base revision: `51c2828e82ffb19860830f78b771f80e13ad7dff`

Base tree: `4655b8b40829513de6fb5661344b33fc7cd17cd1`

Run date: `2026-07-15T16:13:28+08:00`

## Verdict

`blocked`. The proof phase is not complete, so no
`.stage1-worker-selftest.json` was emitted.

The tracked `Proof.lean` is placeholder-free and kernel-checks an inhabitant of
the frozen Lean proposition. It cannot receive proof credit for the canonical
human Rellich inequality because the frozen proposition has two exact-statement
mapping defects:

1. `ContDiff Real top` infers `top : WithTop ENat`, mathlib's analytic order
   `omega`; smooth infinity is `((top : ENat) : WithTop ENat)`.
2. `Euclidean n := Fin n -> Real` carries the finite Pi supremum norm;
   `EuclideanSpace Real (Fin n)` is `PiLp 2` with the Euclidean `L2` norm.

Support avoidance makes every admitted analytic function vanish near the
origin. Analytic uniqueness then makes it identically zero, and simplification
closes only this malformed backend encoding. The first failed gate remains the
rev-5.6 section 5.1 exact statement/source-mapping gate, proposed at
`M1247-S-DOMAIN`.

The predecessor `S56-M-1247-OBLIGATION_TREE` is provisional `[_]`, not
master-accepted. Its 13-obligation registry remains structurally valid but is
semantically stale after the mismatch diagnosis. The conditional declaration
`root_of_coreRellichEstimate` still consumes an open `CoreRellichEstimate`
premise and supplies no missing analytic proof.

## Current-Base Delta

The prior target recheck was based at `3c2814a370c2fee02158ca79aa44a48e411c4d18`.
The only target-owned changes between that base and this base are that prior
recheck's JSON and Markdown companions. The statement, proof body, obligation
tree, registry, graphs, validation specs, anchor audit, target manifest entry,
proof-item state, and execution skill did not change. Authority changes concern
ten unrelated provisional task promotions.

There were 26 integrated `proof-recheck-*.json` files before this packet. This
is far beyond the section 10.2 rule requiring a split after five unresolved
ticks. The worker may not edit the master DAG. The scheduler must stop
redispatching this unchanged proof item, reopen the statement phase, and create
dependency-legal repair/proof children.

## Validation

All Lean checks read the automation-provided canonical pinned artifacts. No
update, build, clone, fetch, network request, or `.lake` mutation was performed.
Fresh outputs lived only in temporary directories under `/tmp` and were removed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_statement.py` | 0 | Expression SHA-256 `4697dbba...5c90e`; all four mutations killed. This validates only the frozen encoding. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | Three pinned mathlib candidate families checked; exact external candidates `0`; terminal result open. |
| `python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | 13 obligations, 34 typed edges, denominator `9df3b5e9...79a590`; root open at `M3`, with six analytic obligations at `M4`. |
| Isolated pinned `lake env lean --trust=0` recipe below | 0 | Fresh `Statement.olean`, `Proof.lean`, and `ObligationTree.lean` elaborated; exact frozen type checked; axioms exactly `propext`, `Classical.choice`, `Quot.sound`. |
| Independent read-only agent replay | 0 | Independently checked the same statement/proof route and axiom output; corroboration only, not release-independence credit. |
| `rg -n -i 'Rellich\|Hardy[-_ ]?Rellich\|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1, expected | No exact theorem candidate in readable pinned package Lean sources. |
| Prohibited proof-token scan over `Statement.lean`, `Proof.lean`, and `ObligationTree.lean` | 1, expected | No `sorry`, `admit`, `sorryAx`, declared `axiom`, `unsafe`, or `opaque`; this is not a transitive provenance audit. |
| Semantic/authority diff from `3c2814a3` to this base | 0 | Only the prior target blocker pair plus unrelated authority changes; no target semantic or governing-rule change. |
| Count integrated target proof-recheck JSON files before this packet | 0 | `26`, beyond the mandatory five-tick split threshold. |
| Packet JSON parse and target-scoped assertions | 0 | Current base, hashes, open-state boundary, and deliberate self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1247 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false worker-completion packet exists. |

The successful narrow Lean replay was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-51c2828e-slot42.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET"/{Statement,Proof,ObligationTree}.lean "$TMP/"
cd "$LEAN_ROOT"
BASE_LEAN_PATH=$(timeout --foreground --kill-after=5s 300s lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" "$TMP/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" "$TMP/ObligationTree.lean"
```

The proof-specific output was:

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget : RellichInequalityTarget
'Stage1Instances.THM_M_1247.frozen_top_is_analytic_order' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.analytic_avoidance_eq_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.rellichInequalityTarget' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.root_of_coreRellichEstimate' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The expanded root output contains `@Top.top (WithTop ENat)` together with
finite-Pi `@Pi.normedAddCommGroup` and `@Pi.normedSpace` instances, confirming
both mapping defects.

## Retry Condition

Do not dispatch `S56-M-1247-PROOF` unchanged again. Reopen
`S56-M-1247-STATEMENT` under an authorized assignment, use
`EuclideanSpace Real (Fin n)` and
`ContDiff Real ((top : ENat) : WithTop ENat)`, rerun exact-expression and
mutation gates, publish a versioned obligation-registry/typed-graph delta with
downstream invalidations, and split weighted integration by parts, derivative
Hardy, normalization, core estimate, and transport into dependency-legal child
tasks before resuming proof execution.

## Status Boundary

This is current-base blocker and scheduler-escalation evidence under the owned
target path. It does not satisfy `S56-M-1247-PROOF`. The item remains `[ ]`;
there is no worker self-test, accepted receipt, audit completion, validation,
release, or theorem-completion claim.
