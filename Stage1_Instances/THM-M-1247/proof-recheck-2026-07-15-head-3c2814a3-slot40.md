# THM-M-1247 proof recheck at `3c2814a3` (slot40)

Item: `S56-M-1247-PROOF`

Theorem: `THM-M-1247`

Base revision: `3c2814a370c2fee02158ca79aa44a48e411c4d18`

Base tree: `e1bd7e27bd922b779322c089410a471b6a1535f0`

Run date: `2026-07-15`

## Verdict

`blocked`. The proof phase is not complete, and no
`.stage1-worker-selftest.json` was emitted.

The tracked `Proof.lean` is placeholder-free and kernel-checks an inhabitant of
the frozen Lean proposition. It does not prove the canonical human Rellich
inequality selected by the intake. Two statement-mapping defects make the
admissible functions analytic functions on the finite Pi/sup-norm space rather
than arbitrary smooth functions on Euclidean `L2` space:

1. `ContDiff Real top` infers `top : WithTop ENat`, mathlib's analytic order
   `omega`; smooth infinity is `((top : ENat) : WithTop ENat)`.
2. `Euclidean n := Fin n -> Real` carries the ordinary finite Pi supremum norm;
   mathlib's `EuclideanSpace Real (Fin n)` is `PiLp 2` with the `L2` norm.

Support avoidance therefore makes the admitted analytic function vanish near
the origin, analytic uniqueness makes it identically zero, and simplification
closes only this malformed backend encoding. Rev-5.6 exact-statement and
statement/source-mapping gates forbid canonical proof credit.

The first failed gate remains the section 5.1 exact statement/source mapping
gate, proposed at `M1247-S-DOMAIN`. The frozen 13-obligation registry is
structurally valid but semantically stale. The predecessor
`S56-M-1247-OBLIGATION_TREE` is only `[_]`, not master-accepted.

## Current-Base Delta

The preceding current-style blocker packet was written against
`9d3f687e9bf0fe3120397744332e909472c52dfd`. From that base to this base, the
only `THM-M-1247` additions are that packet's JSON and Markdown files. The
canonical statement, proof body, obligation tree, registry, typed graphs,
validation specs, anchor audit, target-manifest entry, and execution skill did
not change. Authority changes promote four unrelated items. This proof item
remains `[ ]`, with `attempts: 0` and no children.

There were already 25 integrated `proof-recheck-*.json` files and 25 matching
Markdown companions before this packet, plus the initial blocker pair. This is
five times the section 10.2 threshold requiring a split after five unresolved
ticks. The worker cannot edit the master-owned DAG. The scheduler must stop
redispatching this unchanged proof item, reopen the statement phase, and create
dependency-legal repair children.

`THM-M-1246` now provides provisional repo-local ordinary Hardy proof
substrate. It is not an exact Rellich theorem, shares the stale analytic
regularity encoding, is outside this item's owned path, and neither repairs
this target's statement nor closes its weighted derivative Hardy and singular
integration-by-parts obligations. It therefore does not change the blocked
verdict.

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
| `rg -n -i 'Rellich\|Hardy[-_ ]?Rellich\|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1, expected | No exact theorem candidate in readable pinned package sources. |
| Prohibited proof-token scan over `Statement.lean`, `Proof.lean`, and `ObligationTree.lean` | 1, expected | No `sorry`, `admit`, `sorryAx`, declared `axiom`, `unsafe`, or `opaque` token; not a transitive provenance audit. |
| `git diff --name-status 9d3f687e9bf0fe3120397744332e909472c52dfd..HEAD` over target semantic inputs, authorities, manifest, and skill | 0 | Only the preceding target blocker pair plus unrelated evidence/state changes; no target semantic input or governing-rule change. |
| Count integrated `proof-recheck-*.json` files before this packet | 0 | `25`, five times the mandatory split threshold. |
| `python3 -m json.tool Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-3c2814a3-slot40.json >/dev/null` | 0 | Blocker packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1247 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics in the owned path or self-test path. |
| `git diff --no-index --check /dev/null <new-packet-file>` for each companion | 1, expected | Addition-only exit, with no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false worker-completion packet exists. |

The successful narrow Lean replay was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-3c2814a3-slot40.XXXXXX)
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

The expanded statement output contains `@Top.top (WithTop ENat)` together with
finite-Pi `@Pi.normedAddCommGroup` and `@Pi.normedSpace` instances,
independently confirming both mapping defects.

## Retry Condition

Do not dispatch `S56-M-1247-PROOF` unchanged again. Reopen
`S56-M-1247-STATEMENT` under an authorized assignment, use
`EuclideanSpace Real (Fin n)` and
`ContDiff Real ((top : ENat) : WithTop ENat)`, rerun exact-expression and four
mutation gates, then publish a versioned obligation-registry/typed-graph delta
and downstream invalidations. Audit any reused `THM-M-1246` theorem as an
explicit dependency and split the genuine weighted integration-by-parts,
weighted derivative Hardy, normalization, core-estimate, and transport work
into dependency-legal child tasks before resuming proof execution.

## Status Boundary

This is current-base blocker and scheduler-escalation evidence under the owned
target path. It does not satisfy `S56-M-1247-PROOF`. The item remains `[ ]`;
there is no worker self-test, accepted receipt, audit-completion, validation,
release, or theorem-completion claim.
