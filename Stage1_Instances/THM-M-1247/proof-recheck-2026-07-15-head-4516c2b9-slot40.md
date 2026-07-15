# THM-M-1247 proof recheck at `4516c2b9` (slot40)

Item: `S56-M-1247-PROOF`

Base revision: `4516c2b9d9dfa14a5f8b09da31e54e91718a6cf0`

Base tree: `e7886f0e6704a1d2e56c136d2316207cced14abd`

Run date: `2026-07-15T20:47:50+08:00`

## Verdict

`blocked`. The assigned proof phase is not genuinely complete, so no
`.stage1-worker-selftest.json` was emitted.

The tracked placeholder-free declaration

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget :
  Stage1Instances.THM_M_1247.RellichInequalityTarget
```

re-elaborates at trust level zero, but it proves only the malformed frozen
Lean encoding, not the canonical classical Rellich inequality. There are two
independent exact-statement defects:

1. `ContDiff Real top` infers `top : WithTop ENat`, which mathlib defines as
   analytic order `omega`; smooth infinity is
   `((top : ENat) : WithTop ENat)`.
2. `Euclidean n := Fin n -> Real` has the finite Pi supremum norm. The
   classical radial weight requires `EuclideanSpace Real (Fin n)`, mathlib's
   `PiLp 2` Euclidean L2 norm.

Support avoidance makes each function admitted by the analytic encoding zero
near the origin. Analytic uniqueness then makes it identically zero, and the
encoded inequality reduces to `0 <= 0`. This is kernel-checked diagnostic
evidence, but rev-5.6 exact-statement and backend-to-source mapping gates
forbid treating it as proof credit for the canonical claim.

The structurally valid obligation registry is semantically stale. Its
conditional `root_of_coreRellichEstimate` still consumes an open
`CoreRellichEstimate`, while the analytic-vacuity proof bypasses the frozen
weighted integration-by-parts/Hardy architecture rather than composing its
required children. The prerequisite `S56-M-1247-OBLIGATION_TREE` is only
`[_]`, not master-accepted.

The source boundary is independently open: the crosswalk records DOI
`10.1007/PL00004387`, whereas the cited Davies-Hinz article at volume 227,
pages 511-523 is `10.1007/PL00004389`. No exact Rellich or Hardy-Rellich
declaration was found in the readable pinned package source closure.

## Current-Base Delta And Escalation

Since the preceding recheck base `a1ba351e42fd9eefe315119ef09c0b958358bb8e`,
the target gained only that recheck's JSON and Markdown companions. Two
unrelated validation items were promoted in the master-owned authority files.
The THM-M-1247 statement, proof, obligation registry, typed graphs, anchor
audit, manifest entry, task states, and execution skill did not change.

There were 38 integrated `proof-recheck-*.json` reports before this packet,
but the master-owned proof item still records zero attempts and no children.
Packet count is not itself an authoritative execution-tick count. The master
must reconcile these reports and apply the rev-5.6 section 10.2 split rule if
at least five are unresolved ticks rather than dispatching the same oversized
item unchanged again.

## Validation

All Lean checks reused the existing pinned Lake sources and compiled
artifacts. No update, build, clone, fetch, network access, or `.lake` mutation
was performed. Fresh output was confined to a temporary `/tmp` directory and
removed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_statement.py` | 0 | Expression SHA-256 `4697dbba...5c90e`; all four recorded structural mutations killed. This checks the frozen encoding, not its human-claim mapping. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | Three pinned mathlib candidate families checked; exact external candidates `0`; terminal result open. |
| `python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | 13 obligations, 34 typed edges, denominator `9df3b5e9...79a590`; root open at `M3`, with six analytic obligations at `M4`. |
| Isolated pinned `lake env lean --trust=0` recipe below | 0 | Fresh `Statement.olean`, `Proof.olean`, and `ObligationTree.olean` elaborated; exact frozen type checked; axioms exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n -i 'Rellich\|Hardy[-_ ]?Rellich\|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1, expected | No exact theorem candidate in readable pinned package sources. |
| Prohibited proof-token scan over `Statement.lean`, `Proof.lean`, and `ObligationTree.lean` | 1, expected | No `sorry`, `admit`, `sorryAx`, declared `axiom`, `unsafe`, or `opaque` token; not a transitive provenance audit. |
| `git diff --name-status a1ba351e42fd9eefe315119ef09c0b958358bb8e..HEAD` over target and governing surfaces | 0 | Only the preceding target blocker pair plus two unrelated authority promotions; no target semantic or task-state change. |
| Count integrated `proof-recheck-*.json` files before this packet | 0 | `38`; no assertion that packet count equals execution ticks. |
| `python3 -m json.tool Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-4516c2b9-slot40.json >/dev/null` | 0 | Current-base blocker packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1247 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics in tracked owned-path changes or the self-test path. |
| `git diff --no-index --check /dev/null <new-packet-file>` for each companion | 1, expected | Addition-only diff exit for each file, with no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false completion packet exists. |

The narrow kernel replay was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
MATHLIB="$LEAN_ROOT/.lake/packages/mathlib"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-4516c2b9-slot40.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET"/{Statement,Proof,ObligationTree}.lean "$TMP"/
BASE_LEAN_PATH="$(find -L "$LEAN_ROOT/.lake/packages" -type d \
  -path '*/.lake/build/lib/lean' -print | LC_ALL=C sort | paste -sd:):\
$(readlink -f "$LEAN_ROOT/.lake")/build/lib/lean:\
$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
cd "$MATHLIB"
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Proof.olean" "$TMP/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/ObligationTree.olean" "$TMP/ObligationTree.lean"
```

Proof-specific output:

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget : RellichInequalityTarget
'Stage1Instances.THM_M_1247.frozen_top_is_analytic_order' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.analytic_avoidance_eq_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.rellichInequalityTarget' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.root_of_coreRellichEstimate' depends on axioms: [propext, Classical.choice, Quot.sound]
STATEMENT_EXIT=0
PROOF_EXIT=0
OBLIGATION_TREE_EXIT=0
```

The printed target contains `@Top.top (WithTop ENat)` together with finite-Pi
`@Pi.normedAddCommGroup` and `@Pi.normedSpace` instances, independently
confirming both mapping defects.

## Retry Condition

Reopen `S56-M-1247-STATEMENT` under an authorized assignment. Replace the
domain with `EuclideanSpace Real (Fin n)` and analytic `top` with smooth
`((top : ENat) : WithTop ENat)`, then rerun exact-expression and mutation
gates and publish a versioned registry/graph delta with downstream
invalidations. Correct the source DOI under the appropriate source/statement
task. After that, implement the weighted integration-by-parts, sharp Hardy,
normalization, core-estimate, and transport obligations as dependency-legal
children if the master confirms the five-tick split threshold.

## Status Boundary

This is current-base blocker and scheduler-escalation evidence only. It does
not satisfy `S56-M-1247-PROOF`; the item remains `[ ]`. No proof receipt,
canonical root closure, audit completion, validation, release, or theorem
completion is claimed.
