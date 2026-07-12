# THM-M-1522 anchor audit

Item: `S56-M-1522-ANCHOR_AUDIT`. Audit date: 2026-07-12. Worker base:
`4161921b2a43484a498bcf39900c1c468bc4174e`.

## Verdict

The pinned local mathlib has the Birkhoff-average object model, ergodicity APIs,
almost-everywhere transport, and a Hilbert-space mean-ergodic theorem, but no
terminal pointwise Birkhoff declaration matching the frozen target. The exact
repo-local root therefore remains open.

`lua-vr/pointwise-birkhoff@fc06094ca0506d8d74eba8b45b34882ce5930bf4`
is a credible external Lean 4 candidate. Its two top-level declarations prove
convergence to an invariant conditional expectation. It is nevertheless only
an upstream anchor here: it has not been imported or checked in this Lake
closure, uses Lean 4.20.0-rc5 and mathlib
`83f3832c6cfeecbc8d16b0248c98346956a7f0e5`, and still needs a checked bridge
from `invCondexp` to the constant `integral mu f` under ergodicity. The truthful
classification is `M3`, with no theorem-completion credit.

## Candidate ledger

| Surface | Immutable identity | Assessment |
|---|---|---|
| Repo-local `S1_M_247.lean` | repository base plus SHA-256 `57a019...77d9c` | Statement shapes and prior audit metadata only; it explicitly denies terminal closure |
| mathlib4 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` | `birkhoffSum`, `birkhoffAverage`, preservation/ergodicity, a.e. transport, and mean-ergodic support; no exact pointwise root |
| `lua-vr/pointwise-birkhoff` | `fc06094ca0506d8d74eba8b45b34882ce5930bf4`; top-level source SHA-256 `34cd25...e156` | Relevant upstream proof, but unchecked locally and conclusion requires an adapter |

The local mathlib git tree was clean at the manifest revision. `AnchorAudit.lean`
kernel-checks the supporting declaration names and the two immutable revision
labels. It contains no assumed proof of the target.

## Search boundary

The audit searched repo-local artifacts and the complete pinned local
`Mathlib/**/*.lean` tree using Birkhoff, pointwise-ergodic, convergence, and
conditional-expectation aliases. It also inspected immutable raw upstream
metadata for the known external candidate. GitHub's recursive-tree API returned
HTTP 403, and raw access was intermittent, so this is bounded evidence over the
named surfaces rather than an exhaustive public-code nonexistence claim. No
dependency was cloned, fetched, updated, or added to `.lake`.

## Validation receipt

Exact commands and results from this worker run:

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned tree clean |
| `rg -n 'theorem (birkhoff\|.*tendsto.*birkhoff)\|def (birkhoff\|.*tendsto.*birkhoff)' Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 0 | only definitions/support and mean-ergodic/fixed-point convergence; no exact root |
| `curl` immutable raw upstream `BirkhoffErgodicThm.lean` piped to `sha256sum` | 0 | `34cd25528e31e3eacf9bdd1089b57d799ae339a0d6512a4a2713668c96bee156` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1522/AnchorAudit.lean` | 0 | pinned metadata checks and eight supporting declaration names elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-1522/anchor-audit.json` | 0 | structured audit parsed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-1522` | 0 | rank 190, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1522 .stage1-worker-selftest.json` | 0 | no whitespace errors |

