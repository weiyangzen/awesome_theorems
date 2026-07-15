# THM-M-1247 proof-phase recheck at `1f996d0b` (slot42)

Item: `S56-M-1247-PROOF`

Date: `2026-07-15T13:11:52+08:00` (`Asia/Shanghai`)

Base revision: `1f996d0ba7939acd26bf231689a91751d276bb8c`

Base tree: `ae0448c57d503bd89b62f8f4b753e689abe77e83`

## Verdict

`blocked`. This is a base-refresh blocker report, not a new proof
implementation. Since the prior slot42 recheck at `63a9ed9c`, no canonical
statement, proof body, obligation registry, typed graph, target authority, or
task state changed. The base advanced by integrating that prior blocker pair.

The existing placeholder-free declaration

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget :
  Stage1Instances.THM_M_1247.RellichInequalityTarget
```

re-elaborates at trust level zero, but it closes only a malformed frozen Lean
encoding. It cannot receive proof credit for the canonical Rellich inequality.

The intended claim quantifies over arbitrary smooth compactly supported
functions on Euclidean space. In `Statement.lean`, `ContDiff Real top` instead
infers `top : WithTop ENat`, definitionally mathlib's analytic order `omega`.
Support avoidance gives a neighborhood of the origin where the analytic
function vanishes. Analytic uniqueness then makes it zero everywhere, so both
sides of the encoded inequality simplify to zero.

Independently, `Euclidean n := Fin n -> Real` has the finite Pi supremum norm,
not the Euclidean L2 norm of `EuclideanSpace Real (Fin n)`. The checked body is
therefore diagnostic evidence for a statement mismatch, not a proof of the
selected source theorem.

The dossier vector stays `[H1, M3, R3]`; `M5` is only the proposed machine
diagnosis. The structurally valid registry and graphs are stale after this
diagnosis. The required `S56-M-1247-OBLIGATION_TREE` predecessor remains
provisional `[_]`, not master-accepted. No proof receipt, state transition,
audit completion, validation completion, release, or theorem completion is
claimed. `.stage1-worker-selftest.json` is deliberately absent because the
assigned proof phase is not genuinely complete.

## Delta And Escalation

The authoritative DAG still records the proof item as `[ ]` with zero attempts.
There are separately 17 integrated proof-blocker report pairs. That report
count is not asserted to be 17 authoritative execution ticks, but the repeated
unchanged dispatch warrants integration-lane review against the section 10.2
five-tick split rule. This worker is not authorized to edit the DAG or create
children. The proof item should not be dispatched unchanged again.

The first failed gate is the Stage1 rev-5.6 section 5.1 exact Lean statement
gate; `M1247-S-DOMAIN` is the proposed first invalidated obligation. The first
repair task is `S56-M-1247-STATEMENT`. Repairing that predecessor inside this
proof-only assignment would substitute the frozen target and invalidate the
anchor and obligation-tree inputs.

Retry only after an authorized statement-phase repair uses
`EuclideanSpace Real (Fin n)` and
`ContDiff Real ((top : ENat) : WithTop ENat)`, reruns the exact-statement and
mutation gates, and publishes a versioned registry/graph delta with downstream
invalidations. Separately, an authorized cache-management lane must restore the
complete immutable Lake closure: the pinned `flt-regular` package has no
resolvable `HEAD`. This worker did not repair, update, build, clone, or fetch a
dependency.

## Validation

All credited Lean checks read existing pinned sources and compiled artifacts.
Generated Lean output was confined to a fresh `/tmp` directory and removed.
The automation-provided untracked `.lake` symlink makes this nonrelease
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before this report | 0 | Only the automation-provided `?? Formalizations/Lean/.lake` symlink was present; the owned target path was clean. |
| `python3 Stage1_Instances/THM-M-1247/check_statement.py` | 1 | Root Lake resolution failed before Lean because pinned `flt-regular` has no resolvable `HEAD`; no statement-pass credit is claimed. |
| `python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 1 | Failed at the same preexisting Lake dependency defect; no anchor-audit pass credit is claimed. |
| `python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | `PASS`: 13 obligations and 34 typed edges; denominator `9df3b5e...79a590`; root open at M3. |
| Isolated pinned mathlib `lake env lean --trust=0` recipe below | 0 | Fresh `Statement.olean`, `Proof.lean`, and `ObligationTree.lean` elaborated; the exact frozen root and conditional composition checked. |
| Independent isolated statement/proof replay by a task agent | 0 | A separate agent derived and repeated the fresh trust-zero checks with the same proof and axiom output; corroboration only, not release independence. |
| `sed -n '88,125p' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Calculus/ContDiff/FTaylorSeries.lean` | 0 | Pinned mathlib defines analytic `omega` as `top : WithTop ENat` and smooth infinity as `((top : ENat) : WithTop ENat)`. |
| `sed -n '32,40p;96,120p' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/PiL2.lean` | 0 | Pinned mathlib defines `EuclideanSpace` as `PiLp 2`, with the L2 norm. |
| `rg -n -i 'Rellich\|Hardy[-_ ]?Rellich\|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean' --glob '!flt-regular/**'` | 1, expected | No matching Lean source in the readable pinned package closure. |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe\|opaque)[[:space:]]' Stage1_Instances/THM-M-1247/{Statement,Proof}.lean` | 1, expected | No lexical match; this does not replace a transitive provenance scan. |
| `cd Formalizations/Lean && timeout 180 lake env printenv LEAN_PATH` | 1 | Confirmed the preexisting `flt-regular` `HEAD` blocker without mutating `.lake`. |
| `git diff --name-status 63a9ed9c..HEAD -- <target-and-authority-paths>` | 0 | Only the preceding slot42 blocker pair was added; no target source, authority, registry, graph, or task state changed. |
| `python3 -m json.tool <new-json> >/dev/null` plus current-base packet assertions | 0 | JSON syntax, base/tree identity, source and authority hashes, tracked prior-report count, blocker booleans, changed-path existence, and deliberate self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1247` | 0 | No whitespace errors in the owned target delta. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The successful isolated Lean recipe was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
MATHLIB="$ROOT/Formalizations/Lean/.lake/packages/mathlib"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-1f996d0b-slot42.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET"/{Statement,Proof,ObligationTree}.lean "$TMP/"
cd "$MATHLIB"
TOOLCHAIN_PATH=$(timeout 180 lake env printenv LEAN_PATH)
BASE_LEAN_PATH="$ROOT/Formalizations/Lean/.lake/packages/Cli/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/batteries/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/Qq/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/aesop/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/proofwidgets/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/importGraph/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/plausible/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/mathlib/.lake/build/lib/lean:${TOOLCHAIN_PATH##*:}"
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_LEAN_PATH" timeout 180 \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" timeout 180 \
  lake env lean --trust=0 -t0 --root="$TMP" "$TMP/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" timeout 180 \
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

## Status Boundary

This is current-base blocker evidence under the owned target path. It is not a
positive proof receipt and does not satisfy `S56-M-1247-PROOF`. The assigned
item remains `[ ]`; no accepted receipt ID or worker self-test manifest exists.
