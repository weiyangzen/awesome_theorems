# THM-M-1247 proof-phase recheck at current base

Item: `S56-M-1247-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Verdict

`blocked`. The existing placeholder-free declaration

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget :
  Stage1Instances.THM_M_1247.RellichInequalityTarget
```

kernel-checks at trust level zero, but only because the frozen Lean target is
not the intended classical Rellich inequality. The source claim requires
arbitrary smooth compactly supported functions on Euclidean space. Instead,
`Statement.lean` gives `ContDiff Real top` the inferred order `WithTop ENat`;
its `top` is mathlib's analytic order `omega`, not smooth order `infinity`.
Support avoidance then supplies a neighborhood of zero on which the function
vanishes, and analytic uniqueness forces the function to vanish everywhere.
The checked root follows by simplifying both integrals to zero.

There is a second independent mismatch: the abbreviation `Fin n -> Real`
uses mathlib's Pi sup norm. It is not `EuclideanSpace Real (Fin n)` with the
Euclidean L2 norm used by the classical radial weight. Thus the local body is
durable diagnostic evidence for a malformed backend encoding, not proof
credit for the canonical human theorem. Correcting the target during this
proof item would be an illegal substitution.

The accepted dossier vector remains `[H1, M3, R3]`; `M5` is only the proposed
machine diagnosis for the statement mismatch. The positive obligation
registry and graphs are stale with respect to that diagnosis, despite their
structural validator passing. No proof receipt, obligation closure, audit
completion, or theorem completion is claimed.

## Validation

Checks ran in this worker clone using only the existing pinned Lean and Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, network
access, or `.lake` mutation was performed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1247/check_statement.py` | interrupted | This legacy checker invokes five concurrent `lake env lean` elaborations; it was stopped without credit during system-wide Lean saturation. The narrower raw-Lean recipe below directly elaborated the unchanged target and proof. |
| `python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | interrupted | This upstream audit re-elaboration was stopped without credit during system-wide Lean saturation; no anchor-audit result is needed or claimed by this blocker recheck. |
| `python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | `PASS`: 13 obligations and 34 typed edges; denominator `9df3b5e...79a590`; stale positive root open at M3 |
| Fresh temporary-olean raw Lean recipe below | 0 | `rellichInequalityTarget : RellichInequalityTarget` elaborated at trust level zero; all three proof declarations report only `propext`, `Classical.choice`, and `Quot.sound` |
| Independent read-only worker replay of the same proof | 0 | Independently confirmed the exact-encoding body and the same axiom closure |
| `rg -n '\\b(sorry|admit|sorryAx)\\b|^[[:space:]]*(axiom|unsafe|opaque)[[:space:]]' Stage1_Instances/THM-M-1247/{Statement,Proof}.lean` | 1, expected | No prohibited placeholder, declared axiom, unsafe declaration, or opaque body |
| `python3 -m json.tool Stage1_Instances/THM-M-1247/proof-recheck-2026-07-15-head-a1a7e939.json >/dev/null` | 0 | Current-base blocker packet is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1247` | 0 | No whitespace errors in the owned path |

Exact successful Lean recipe (temporary files are removed afterward):

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
LEAN="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
TMP=$(mktemp -d /tmp/thm-m-1247-proof.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET"/{Statement,Proof}.lean "$TMP/"
BASE_LEAN_PATH="$(find -L "$LEAN_ROOT/.lake/packages" -type d \
  -path '*/.lake/build/lib/lean' -print | paste -sd:):\
$(readlink -f "$LEAN_ROOT/.lake")/build/lib/lean:\
$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_LEAN_PATH" timeout 180 \
  "$LEAN" --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" timeout 180 \
  "$LEAN" --trust=0 -t0 --root="$TMP" "$TMP/Proof.lean"
```

Checked input SHA-256 values:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `0fb5f4ddca16a5e9d99f692b17ad86ca55955835fc5aa3d2c063798fc06bf266` |
| `Proof.lean` | `36cbbc887a33bd3a58fac5d6285a8cee0b44f5458a247057acbec589b52852fb` |
| `obligation-registry.json` | `1c7cdcd995877c5a4244c9385967df45078356b3ec5a0fafa07ffb65f7f2d557` |
| `typed-graphs.json` | `641b0143331a5e4917fee477c1bfd29bcd11b69d6ae67471d164b51ecd28526a` |
| `validation-specs.json` | `5a69307e8af773a1196d38e11e68fc0f491db0eaac2b478e0f8cf950055504c1` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |

## Retry condition

The first failed gate is exact canonical statement correctness. Reopen
`S56-M-1247-STATEMENT`, replace the domain with
`EuclideanSpace Real (Fin n)`, spell smoothness unambiguously as
`ContDiff Real ((top : ENat) : WithTop ENat)`, and rerun exact-statement and
mutation gates. Then publish a versioned registry/graph delta and downstream
invalidations before another proof attempt.

The remaining root cut set is `S56-M-1247-STATEMENT`. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
