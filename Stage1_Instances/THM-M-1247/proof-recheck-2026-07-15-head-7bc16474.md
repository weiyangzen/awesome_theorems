# THM-M-1247 proof-phase recheck at `7bc16474`

Item: `S56-M-1247-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `7bc16474ba6a97ad369a618990b1ffbec170db3c`

Base tree: `d911a4fe236f270edbd1521a474442e0de79c6b3`

## Verdict

`blocked`. The tracked placeholder-free declaration

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
the analytic function is zero; analytic uniqueness then makes it zero
everywhere, and both sides of the frozen inequality simplify to zero.

Independently, `Euclidean n := Fin n -> Real` uses mathlib's finite Pi
supremum norm. It is not `EuclideanSpace Real (Fin n)`, which is `PiLp 2` with
the Euclidean L2 norm required by the radial Rellich weight. The checked body
therefore provides diagnostic evidence for the statement mismatch, not a
proof of a broadened, repaired, or substituted theorem.

The accepted dossier vector remains `[H1, M3, R3]`; `M5` is only the proposed
machine diagnosis. The existing registry and graphs remain structurally
valid but stale relative to this diagnosis. No proof receipt, state
transition, audit completion, validation completion, release, or theorem
completion is claimed. `.stage1-worker-selftest.json` is deliberately absent
because the assigned positive proof phase is not genuinely complete.

## Failed Gate

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M1247-S-DOMAIN`. The remaining root cut is
`S56-M-1247-STATEMENT`. Correcting the statement in this proof-only item would
be an unauthorized substitution and would invalidate the frozen downstream
artifacts.

Retry only after an authorized statement-phase repair uses
`EuclideanSpace Real (Fin n)` and
`ContDiff Real ((top : ENat) : WithTop ENat)`, reruns the statement and
mutation gates, and publishes a versioned registry/graph delta with downstream
invalidations before a new proof attempt.

## Validation

All credited checks ran in this worker clone against the existing pinned Lean
and Lake artifacts. No `lake update`, `lake build`, dependency clone/fetch,
network action, or other `.lake` mutation was performed. Generated Lean
output was confined to a fresh `/tmp` directory and removed afterward. The
automation-provided untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short` before this report | 0 | Only the automation-provided `?? Formalizations/Lean/.lake` symlink was present; the owned target path was clean. |
| `python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | `PASS`: 13 obligations and 34 typed edges; denominator `9df3b5e...79a590`; root open at M3 with six analytic obligations at M4. |
| Isolated pinned `lake env lean --trust=0` recipe below | 0 | Fresh `Statement.olean` plus `Proof.lean` elaborated. The root has the exact frozen type; all three proof declarations report exactly `[propext, Classical.choice, Quot.sound]`. |
| Independent read-only worker replay of the same Lean recipe | 0 | Independently confirmed the exact-encoding proof at trust level zero and the same statement/proof hashes. |
| `rg -n '\\b(sorry|admit|sorryAx)\\b|^[[:space:]]*(axiom|unsafe|opaque)[[:space:]]' Stage1_Instances/THM-M-1247/{Statement,Proof}.lean` | 1 | Expected no-match: no prohibited placeholder or declaration token occurs in the checked Lean files. |
| `python3 -m json.tool Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-7bc16474.json >/dev/null` plus the invariant recipe below | 0 | Current-base blocker fields, source hashes, open-state boundary, and deliberate self-test absence agree. |
| `git diff --check` plus explicit new-file checks | 0 | No whitespace errors in the owned changes. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean recipe was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-7bc16474.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET"/{Statement,Proof}.lean "$TMP/"
cd "$LEAN_ROOT"
BASE_LEAN_PATH=$(timeout 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_LEAN_PATH" timeout 180 \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" timeout 180 \
  lake env lean --trust=0 -t0 --root="$TMP" "$TMP/Proof.lean"
```

Checked input SHA-256 values:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `0fb5f4ddca16a5e9d99f692b17ad86ca55955835fc5aa3d2c063798fc06bf266` |
| `Proof.lean` | `36cbbc887a33bd3a58fac5d6285a8cee0b44f5458a247057acbec589b52852fb` |
| `ObligationTree.lean` | `e585d34ea74c1c6fa32eb7dc933e81ab9121626a86d3856be4ddd8a699ea49ac` |
| `obligation-registry.json` | `1c7cdcd995877c5a4244c9385967df45078356b3ec5a0fafa07ffb65f7f2d557` |
| `typed-graphs.json` | `641b0143331a5e4917fee477c1bfd29bcd11b69d6ae67471d164b51ecd28526a` |
| `validation-specs.json` | `5a69307e8af773a1196d38e11e68fc0f491db0eaac2b478e0f8cf950055504c1` |
| `anchor-audit.json` | `ddae20cc0997c2f867e70d16b5855c96d7f51bb41654f6393a7a8ff13d4c4350` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |

This is durable current-base blocker evidence, not a proof receipt. It changes
no Lean source, frozen predecessor artifact, scheduler authority, dependency
artifact, or unrelated target.
