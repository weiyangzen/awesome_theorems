# THM-M-1056 proof recheck (slot 59)

Item: `S56-M-1056-PROOF`

Base revision: `d1d1b6abb3bf227c43ebb3ce0513779bc96d6294`

Base tree: `c8009994d3b72ece76326dd39eaf0262255cb6a1`

Attempt date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`. No proof body was added, no frozen obligation was closed, and no
state change or receipt is proposed. The root remains `[H1, M3, R3]`, and
`.stage1-worker-selftest.json` is deliberately absent because the assigned
proof phase is not self-tested complete.

## First failed proof gate

The first failed gate remains `M1056-T-CORE`: there is no placeholder-free
inhabitant of `OseledetsCorePackage` in the repository or pinned dependency
closure. That package is definitionally the complete universal target, so
`root_of_oseledetsCorePackage` is conditional composition rather than a proof.
`SanityInstance.lean` closes only the one-point identity specialization.

The immutable candidate
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`
contains a substantive Euclidean matrix/submodule splitting theorem. It does
not supply the target's arbitrary-fiber coordinate and integrability
transports or its strongly measurable oblique component projections, their
algebra, equivariance, count positivity, and growth transport. Importing the
candidate alone would therefore substitute a narrower theorem.

A scratch port outside the repository continued through modules 11--16 of the
candidate's 62-module closure and stopped at module 17,
`ErgodicTheory.Lyapunov.ForwardMeasurable`, line 53:33. Lean could not synthesize
the `StarHomClass` instance used by `Matrix.toEuclideanCLM`. No scratch compile
process remains. This compatibility failure precedes, and does not remove, the
exact-target transport work above.

## Dependency-cache incident

The automation-provided `.lake` path is a symlink to the scheduler's shared
canonical cache. An initial `lake env lean --version` probe failed before Lean
with:

```text
error: .../Formalizations/Lean/.lake/packages/flt-regular: could not resolve
'HEAD' to a commit; the repository may be corrupt, so you may need to remove
it and try again
```

A later observation found a new shared checkout whose reflog records a clone
from its GitHub origin followed by checkout at the pinned revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` at 03:13:58 +08:00. The process
that performed that transition and whether it used the network are unknown;
the resulting Lake environment is nonrelease evidence and is not credited as
a stable validation result.

This slot did not issue `lake update`, `lake build`, dependency clone, or
dependency fetch and did not intentionally modify `.lake`. The narrow Lean
replay instead used the installed pinned Lean 4.29 binary and the already-built
canonical package artifacts through an explicit read-only `LEAN_PATH`.

## Fresh commands and exact results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique ordered targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; lifecycle `planned`; `rework_required: true`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | The frozen 19-obligation, 49-edge graph passed; denominator `5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828`; root open M3 and core M4. |
| `cd Formalizations/Lean && lake env lean --version` | 1 | Shared-cache failure: `packages/flt-regular` could not resolve `HEAD`; not credited. |
| `/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| Copy `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` to a fresh `/tmp` directory; run the pinned Lean binary with `LEAN_NUM_THREADS=1`, explicit canonical package `LEAN_PATH`, `--trust=0 -t0`, and fresh output oleans; remove the directory | 0 | All three modules elaborated. Only unused-variable warnings occurred. `#print axioms` reported `[propext, Classical.choice, Quot.sound]` for the conditional composer and sanity conclusion. The temporary oleans had SHA-256 `c55d17a...f64db`, `a75c5008...7f0e`, and `ff4de13c...8b7`; all were removed. |
| Scratch compile modules 11--62 of the cached immutable external closure with pinned Lean, `--trust=0`, and `LEAN_NUM_THREADS=1` | 1 | Modules 11--16 elaborated; first failure was module 17 at `ForwardMeasurable.lean:53:33`, missing a `StarHomClass` instance for `Matrix.toEuclideanCLM`. |
| `rg -n '^\\s*(sorry|admit|axiom)(\\s|$)|sorryAx|^\\s*unsafe\\s' Stage1_Instances/THM-M-1056 -g '*.lean'` | 1 | Expected no-match exit; no prohibited Lean declaration token occurs. |
| `rg -n -i '(^|[^A-Za-z])(oseledets|multiplicative ergodic|kingman)([^A-Za-z]|$)' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Expected no-match exit; pinned mathlib has no named terminal Oseledets or Kingman declaration. |

The structured JSON parse, blocker invariants, new-file whitespace checks, and
self-test absence passed as final handoff checks; they are not circularly
recorded as already-run evidence inside the packet they validate.

The direct replay used the installed Lean binary and the already-built project,
mathlib, Batteries, Qq, Aesop, ProofWidgets, ImportGraph, LeanSearchClient, and
Plausible library directories in `LEAN_PATH`, with the temporary directory
prepended only for dependent imports. It did not include `flt-regular`, whose
build artifact was absent. The external scratch archive SHA-256 was
`3c0ef177500430ab55950061cfd73991347f5336b5b3d5032ffe46ac56009a52`;
the failure log SHA-256 was
`a0b3479608292f364adeeb57dd8cb113107f28d914341baa797a9a2a744f9757`.

Exact direct replay recipe, run from the worker root:

```bash
set -euo pipefail
ROOT=$PWD
LEAN="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
BASE="$ROOT/Formalizations/Lean/.lake/packages/batteries/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/Qq/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/aesop/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/proofwidgets/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/importGraph/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/plausible/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/packages/mathlib/.lake/build/lib/lean:$ROOT/Formalizations/Lean/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
TMP=$(mktemp -d /tmp/thm-m-1056-direct-final.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp Stage1_Instances/THM-M-1056/Statement.lean "$TMP/Statement.lean"
cp Stage1_Instances/THM-M-1056/ObligationTree.lean "$TMP/ObligationTree.lean"
cp Stage1_Instances/THM-M-1056/SanityInstance.lean "$TMP/SanityInstance.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE" "$LEAN" --trust=0 -t0 -R "$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" "$LEAN" --trust=0 -t0 -R "$TMP" \
  -o "$TMP/ObligationTree.olean" "$TMP/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" "$LEAN" --trust=0 -t0 -R "$TMP" \
  -o "$TMP/SanityInstance.olean" "$TMP/SanityInstance.lean"
```

Exact external-closure loop, run from `Formalizations/Lean` after modules
1--10 had been checked in the same scratch tree:

```bash
LEAN=$(ELAN_TOOLCHAIN=$(cat lean-toolchain) elan which lean)
LP=/tmp/m1056-closure-compile.FFeoWc:$(cat /tmp/leanpath.manual)
: > /tmp/m1056-next.log
for n in $(seq 11 62); do
  mod=$(sed -n "${n}p" /tmp/m1056-closure-compile.FFeoWc/order.txt)
  file="/tmp/m1056-closure-compile.FFeoWc/${mod//.//}.lean"
  out="/tmp/m1056-closure-compile.FFeoWc/${mod//.//}.olean"
  printf '[%02d/62] %s\n' "$n" "$mod" | tee -a /tmp/m1056-next.log
  LEAN_PATH="$LP" LEAN_NUM_THREADS=1 "$LEAN" --trust=0 \
    --root=/tmp/m1056-closure-compile.FFeoWc -o "$out" "$file" \
    >> /tmp/m1056-next.log 2>&1 || {
      rc=$?
      printf 'FIRST_FAILURE index=%02d rc=%d file=%s\n' "$n" "$rc" "$file" \
        | tee -a /tmp/m1056-next.log
      exit "$rc"
    }
done
```

## Retry condition

Resume after placeholder-free implementations of the frozen core packages
exist, or after the immutable external development is compatibly ported with
kernel-checked coordinate, integrability, measurable-oblique-projection,
equivariance, growth, exact-type, provenance, and trust transports. A stable
pinned dependency cache is also required for ordinary `lake env lean` replay.

## Status boundary

This is a proof-phase blocker record, not a proof receipt. The minimal open root
cut remains `M1056-T-CORE`; theorem completion is false, and the item cannot
truthfully receive `[_]`.
