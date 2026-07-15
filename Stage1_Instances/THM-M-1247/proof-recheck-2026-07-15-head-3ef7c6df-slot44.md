# THM-M-1247 proof-phase recheck at `3ef7c6df` (slot44)

Item: `S56-M-1247-PROOF`

Date: `2026-07-15T15:07:50+08:00` (`Asia/Shanghai`)

Base revision: `3ef7c6dff0c66bc8c02e842f4cea6b9936349094`

Base tree: `58db6c40c0fa9186c4a56a022a6a37d1c2be551b`

## Verdict

`blocked`. No canonical proof body can truthfully be implemented from the
assigned inputs. The existing placeholder-free declaration

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget :
  Stage1Instances.THM_M_1247.RellichInequalityTarget
```

re-elaborates at trust level zero, but it proves a malformed backend encoding,
not the canonical Rellich inequality. It therefore receives no proof credit.

The human claim quantifies over arbitrary smooth compactly supported functions
on Euclidean `L2` space. In `Statement.lean`, `ContDiff Real top` instead
infers `top : WithTop ENat`, definitionally mathlib's analytic order `omega`.
Support avoidance gives a neighborhood of the origin where such an analytic
function vanishes, and analytic uniqueness makes it zero everywhere. Both
sides of the encoded inequality then simplify to zero. Independently,
`Euclidean n := Fin n -> Real` has the finite Pi supremum norm rather than the
`L2` norm of `EuclideanSpace Real (Fin n)`.

This violates the rev-5.6 section 5 backend-to-canonical mapping gate. A
proof-only worker may not silently repair the statement or substitute the
degenerate encoded proposition. `M1247-S-DOMAIN` is the first proposed
invalidated obligation. The structurally valid registry and graph remain
stale, while the substantive `IBP`, `HARDY`, weights, boundary, domain, and
Laplacian obligations remain open.

The required predecessor `S56-M-1247-OBLIGATION_TREE` is still provisional
`[_]`, not master-accepted. The root vector remains `[H1, M3, R3]`; `M5` is
only the proposed machine diagnosis. No proof receipt, state transition, audit
completion, validation, release, or theorem completion is claimed.
`.stage1-worker-selftest.json` is deliberately absent because this phase is
not genuinely complete.

## Current-Base Delta

Since the preceding recheck at `ec3b52a2`, the base added that blocker pair and
unrelated target integrations. There was no change to the THM-M-1247 statement,
proof, obligation registry, typed graph, validation specifications, anchor
audit, target manifest entry, proof-item state, or execution skill.

There are now 22 integrated proof-blocker report pairs for this target. The
authoritative item still records zero attempts and no children. The report
count is not treated as authoritative execution-tick state, but repeated
unchanged dispatch has exceeded the standard's five-tick split threshold.
This worker cannot edit the DAG or create a statement-phase child.

## Validation

All credited Lean checks read the pinned package sources and compiled
artifacts. Temporary Lean outputs were created under `/tmp` and removed. No
update, build, dependency clone/fetch, or `.lake` mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_statement.py` | 0 | Expression SHA-256 `4697dbba...5c90e`; all four recorded structural mutations killed. This confirms the frozen expression, not canonical source fidelity. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | Three pinned mathlib candidate families checked; zero exact external candidates; terminal result open. |
| `python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | 13 obligations, 34 typed edges, denominator `9df3b5e...79a590`; root open at M3. |
| Isolated pinned `lake env lean --trust=0` recipe below | 0 | Fresh statement, proof, and conditional composition elaborated. |
| `sed -n '104,118p' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Calculus/ContDiff/FTaylorSeries.lean` | 0 | Pinned mathlib defines analytic `omega` as `top : WithTop ENat` and smooth `infinity` as `((top : ENat) : WithTop ENat)`. |
| `sed -n '32,40p;96,120p' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/PiL2.lean` | 0 | Pinned mathlib defines `EuclideanSpace` as `PiLp 2`, with the L2 norm. |
| `rg -n -i 'Rellich|Hardy[-_ ]?Rellich|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1, expected | No exact candidate in the readable pinned source closure. |
| `rg -n '\b(sorry|admit|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe\|opaque)[[:space:]]' Stage1_Instances/THM-M-1247/{Statement,Proof,ObligationTree}.lean` | 1, expected | No prohibited lexical match; this is not a transitive provenance audit. |
| `git diff --check -- Stage1_Instances/THM-M-1247` plus `git diff --no-index --check /dev/null` for each new blocker file | 0 diagnostics | No whitespace errors in the tracked owned path or either new file; each no-index command returns 1 only because the file is an addition. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false completion packet exists. |

The successful narrow Lean replay was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
MATHLIB="$LEAN_ROOT/.lake/packages/mathlib"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-3ef7c6df-slot44.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET"/{Statement,Proof,ObligationTree}.lean "$TMP/"
BASE_LEAN_PATH="$(find -L "$LEAN_ROOT/.lake/packages" -type d \
  -path '*/.lake/build/lib/lean' -print | LC_ALL=C sort | paste -sd:):\
$(readlink -f "$LEAN_ROOT/.lake")/build/lib/lean:\
$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
cd "$MATHLIB"
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_LEAN_PATH" timeout 300 \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" timeout 300 \
  lake env lean --trust=0 -t0 --root="$TMP" "$TMP/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" timeout 300 \
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

The expanded statement output contains `@Top.top (WithTop ENat)` and finite-Pi
`@Pi.normedAddCommGroup`/`@Pi.normedSpace` instances, confirming both defects.

The structured companion is validated with `python3 -m json.tool` and a
fail-closed assertion recipe binding item/base identity, hashes, open-state
fields, changed paths, and deliberate self-test absence.

## Retry Condition

Reopen `S56-M-1247-STATEMENT` under an authorized assignment. Use
`EuclideanSpace Real (Fin n)` and
`ContDiff Real ((top : ENat) : WithTop ENat)`, rerun exact-statement and
mutation gates, then publish a versioned registry/graph delta with downstream
invalidations before another proof attempt. Do not dispatch this proof item
unchanged again.

## Status Boundary

This is current-base blocker evidence under the owned target path. It does not
satisfy `S56-M-1247-PROOF`. The item remains `[ ]`, and no worker self-test or
accepted receipt exists.
