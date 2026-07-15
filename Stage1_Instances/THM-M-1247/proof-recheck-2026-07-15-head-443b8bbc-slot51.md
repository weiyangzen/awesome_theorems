# THM-M-1247 proof-phase recheck at `443b8bbc` (slot51)

Item: `S56-M-1247-PROOF`

Date: `2026-07-15T11:39:28+08:00` (`Asia/Shanghai`)

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. The existing placeholder-free declaration

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget :
  Stage1Instances.THM_M_1247.RellichInequalityTarget
```

re-elaborates at trust level zero, but it closes only a malformed frozen Lean
encoding. It cannot receive proof credit for the canonical Rellich inequality.

The source claim requires arbitrary smooth compactly supported functions on
Euclidean space. In `Statement.lean`, however, `ContDiff Real top` infers
`top : WithTop ENat`, mathlib's analytic order `omega`, rather than smooth
order `infinity`. Support avoidance gives a neighborhood of the origin where
the analytic function is zero. Analytic uniqueness then makes it zero
everywhere, and both sides of the frozen inequality simplify to zero.

Independently, `Euclidean n := Fin n -> Real` uses the finite Pi supremum norm,
not `EuclideanSpace Real (Fin n)`, which is `PiLp 2` with the Euclidean L2 norm
required by the radial Rellich weight. The checked body is diagnostic evidence
for a statement mismatch, not a proof of a repaired or substituted theorem.

The recorded dossier vector remains `[H1, M3, R3]`; `M5` is only the proposed
machine diagnosis. The registry and graphs remain structurally valid but stale
relative to this diagnosis. The required `S56-M-1247-OBLIGATION_TREE`
predecessor is also provisional at `[_]`, not master-accepted. No proof receipt,
state transition, audit completion, validation completion, release, or theorem
completion is claimed. `.stage1-worker-selftest.json` is deliberately absent
because the assigned positive proof phase is not genuinely complete.

## Failed Gate

The first failed gate is the Stage1 rev-5.6 section 5.1 exact Lean statement
gate; `M1247-S-DOMAIN` is the proposed first invalidated obligation. The first
repair task is `S56-M-1247-STATEMENT`. A repaired statement would also require
refreshing `S56-M-1247-ANCHOR_AUDIT` and `S56-M-1247-OBLIGATION_TREE`.
Correcting those inputs in this proof-only assignment would be an unauthorized
substitution and would invalidate their frozen fingerprints.

Retry only after an authorized statement-phase repair uses
`EuclideanSpace Real (Fin n)` and
`ContDiff Real ((top : ENat) : WithTop ENat)`, reruns statement and mutation
gates, and publishes a versioned registry/graph delta with downstream
invalidations. Separately, an authorized cache-management lane must restore the
complete immutable Lake closure: the automation-provided canonical
`flt-regular` checkout currently has `.git/HEAD` pointing to
`refs/heads/.invalid`. This worker did not repair, update, clone, or fetch it.

## Validation

All credited checks ran in this worker clone using existing pinned sources and
compiled artifacts. No `lake update`, `lake build`, dependency clone/fetch,
network action, or other `.lake` mutation was performed. Lean outputs were
confined to fresh `/tmp` directories; checker-created transient files were
removed. The automation-provided untracked `.lake` symlink makes this
nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1247/check_statement.py` | 1 | Root Lake resolution failed before Lean because `flt-regular` has invalid `HEAD`; no statement-pass credit is claimed. |
| `python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 1 | Failed at the same preexisting Lake dependency defect; no anchor-audit pass is claimed. |
| `python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | `PASS`: 13 obligations and 34 typed edges; denominator `9df3b5e...79a590`; root open at M3 with six analytic obligations at M4. |
| Root-project isolated `lake env lean --trust=0` recipe | 1 | Failed before Lean: `flt-regular: could not resolve 'HEAD' to a commit`. The dependency was not repaired or fetched. |
| Pinned mathlib `lake env lean --trust=0` recipe below | 0 | Fresh `Statement.olean` and `Proof.lean` elaborated; the exact frozen root and all three proof declarations checked. |
| Direct pinned Lean 4.29.0 replay with canonical package paths | 0 | Independently repeated the same elaboration and axiom output. |
| Two independent task-agent replays | 0, 0 | Both agents independently derived and checked the same frozen-target proof. This is corroboration, not release-independence credit. |
| `rg -n '\\b(sorry\|admit\|sorryAx)\\b\|^[[:space:]]*(axiom\|unsafe\|opaque)[[:space:]]' Stage1_Instances/THM-M-1247/{Statement,Proof}.lean` | 1, expected | No lexical match; this is not a transitive provenance scan. |
| `python3 -m json.tool <blocker.json>` plus packet/source-hash assertions | 0 | Current-base identity, input hashes, open-state boundary, dependency status, and environment blocker agree. |
| `git diff --check -- Stage1_Instances/THM-M-1247` | 0 | No whitespace errors in tracked owned changes. |
| `git diff --no-index --check /dev/null <new-file>` | 1, expected | Each report is an added-file diff and emits no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The successful pinned `lake env lean` recipe was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
MATHLIB="$ROOT/Formalizations/Lean/.lake/packages/mathlib"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-443b8bbc-slot51.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET"/{Statement,Proof}.lean "$TMP/"
cd "$MATHLIB"
TOOLCHAIN_PATH=$(timeout 180 lake env printenv LEAN_PATH)
BASE_LEAN_PATH="$ROOT/Formalizations/Lean/.lake/packages/Cli/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/batteries/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/Qq/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/aesop/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/proofwidgets/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/importGraph/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/plausible/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/mathlib/.lake/build/lib/lean:${TOOLCHAIN_PATH##*:}"
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_LEAN_PATH" timeout 180 \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" timeout 180 \
  lake env lean --trust=0 -t0 --root="$TMP" "$TMP/Proof.lean"
```

The proof-specific output was:

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget : RellichInequalityTarget
'Stage1Instances.THM_M_1247.frozen_top_is_analytic_order' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.analytic_avoidance_eq_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.rellichInequalityTarget' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The expanded statement output contains `@Top.top (WithTop ENat)` and the
finite-Pi `@Pi.normedAddCommGroup`/`@Pi.normedSpace` instances, confirming both
encoding mismatches.

## Status Boundary

This is current-base blocker evidence under the owned target path. It is not a
positive proof receipt and does not satisfy `S56-M-1247-PROOF`. The assigned
item remains `[ ]`; no accepted receipt ID or worker self-test manifest exists.
