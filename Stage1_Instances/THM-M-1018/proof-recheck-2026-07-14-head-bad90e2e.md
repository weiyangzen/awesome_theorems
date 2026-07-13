# THM-M-1018 proof recheck at `bad90e2e`

Item: `S56-M-1018-PROOF`

Date: `2026-07-14T03:53:58+08:00`

Base revision: `bad90e2e2479d376609447202eb4f437789d0d11`

Base tree: `df3ade7b4d06057f8aac33369c3d69bd391aa05a`

## Verdict

`blocked`. The exact proof phase remains open. No unconditional Lean proof body exists in the
owned dossier for `Stage1Instances.THM_M_1018.LevyInversionTarget`, and this current-base recheck
found no eligible theorem in the pinned dependency closure to import or wrap. The root vector
therefore remains `[H2, M3, R4]`; `root_closed=false`, `theorem_complete=false`, and the item remains
`[ ]`.

The remaining root cut is `M1018-T-ANALYTIC`, the fixed-data Levy interval-inversion theorem. The
existing `ObligationTree.root_compose` is only a checked conditional composition: it returns an
analytic premise supplied by its caller and does not construct that premise. The first unavailable
frozen proof package is `M1018-L-DIRICHLET`. Pinned mathlib contains no evaluation of the symmetric
improper sine integral with the normalization and endpoint values required by the selected sharp
cutoff kernel.

Pinned mathlib's nearest characteristic-function result is `integral_charFun_Icc`. It proves the
unweighted finite identity
`integral (-r..r) (charFun mu) = 2*r * integral (sinc (r*x)) dmu`; it does not prove the weighted
endpoint-kernel limit. The available Fourier inversion theorem additionally assumes an integrable
density and an integrable Fourier transform, so it cannot be substituted for this theorem about an
arbitrary probability measure. Focused scans found neither an exact Levy interval-inversion theorem
nor a sharp Dirichlet sine-integral limit in the pinned source tree.

Closing the frozen root requires placeholder-free implementations of `M1018-C-APPROX`,
`M1018-N-FUBINI`, `M1018-N-SCALE`, `M1018-B-POSITION`, `M1018-L-DIRICHLET`,
`M1018-L-INTEGRAL-LIMIT`, `M1018-L-ENDPOINTS`, and `M1018-T-ANALYTIC`. In particular, the
finite-measure limit passage must not use false uniform domination. Assuming this analytic package,
returning the conditional composer, or replacing the target with uniqueness or density Fourier
inversion would violate the proof-body gate.

No `sorry`, axiom, placeholder, unsafe injection, broadened theorem, or substituted theorem was
introduced. Because the assigned positive proof phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All checks ran in the worker clone and reused the automation-provided canonical pinned `.lake`
artifacts read-only. No `lake update`, `lake build`, dependency clone or fetch, or `.lake` mutation
was performed. Discovery queries used GitHub's repository and code-search endpoints only: the
repository search returned zero results and code search returned HTTP 401. No remote source or
dependency was fetched, these queries receive no proof credit, and `network_used=true` is recorded
in the structured blocker. The untracked `.lake` link makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1018` | 0 | Rank 494; planned hard-mathlib-anchor-and-wrapper lane; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1018/check_obligation_tree.py` | 0 | 17 obligations and 34 typed edges passed; denominator `c5662da4...d6c2`; root and fixed-data analytic theorem remain open M3 |
| isolated temporary-copy `lake env lean --trust=0` replay | 0 | `Statement.lean`, `AnchorAudit.lean`, and `ObligationTree.lean` elaborated; `root_compose` reported exactly `propext`, `Classical.choice`, and `Quot.sound` |
| exact pinned mathlib Levy-inversion scan recorded below | 1 | Expected no-match exit; no exact interval-inversion anchor was found |
| focused pinned Dirichlet/sine-integral/Fourier-interval scan recorded below | 0 | Only unrelated finite trigonometric integrals, periodic Fourier coefficients, or noise matched; no required sharp improper-integral limit was found |
| GitHub repository and code-search discovery | mixed | Repository search returned `total_count: 0`; unauthenticated code search returned HTTP 401; no source or dependency was fetched |
| scoped prohibited-construct scan recorded below | 1 | Expected no-match exit for `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `opaque`, `constant`, `extern`, `implemented_by`, and `native_decide` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `python3 -m json.tool ...; blocker invariant assertions` | 0 | The structured current-base blocker parsed and its identity, base, blocked/open flags, empty receipts/body locations, root cut, changed paths, and absent completion self-test agreed |
| scoped new-file whitespace checks for this JSON and Markdown pair | 0 aggregate | Each file differed from `/dev/null` as expected and emitted no whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test is deliberately absent because the proof item is incomplete |

The isolated Lean replay copied the three owned modules to
`/tmp/thm-m-1018-proof-slot77.<random>`, compiled `Statement.lean` to a disposable olean, placed the
temporary directory before the pinned `LEAN_PATH` for `ObligationTree.lean`, and removed the
directory on exit. Source fingerprints remained unchanged: `Statement.lean`
`88009a0b...fdd7`, `ObligationTree.lean` `2df4f358...055e`, registry `14938dc0...fb95`, typed
graphs `0ab51094...fba2`, anchor audit `44e089c4...ee99`, and validation specifications
`92681bbd...49e9`. The toolchain and Lake-manifest SHA-256 values are
`651c8acc...b1d2` and `321626c8...2d81`.

The exact isolated replay command was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1018
tmp=$(mktemp -d /tmp/thm-m-1018-proof-slot77.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$target/AnchorAudit.lean" "$tmp/AnchorAudit.lean"
cd "$tmp"
LEAN_PATH="$lean_path" "$lean" --trust=0 -o Statement.olean Statement.lean
LEAN_PATH="$lean_path" "$lean" --trust=0 AnchorAudit.lean
LEAN_PATH=".:$lean_path" "$lean" --trust=0 ObligationTree.lean
```

The exact pinned scans were:

```bash
rg -ni --glob '*.lean' \
  'levy.*inversion|lévy.*inversion|lévy.*inversion|inversion.*levy|inversion.*lévy|inversion.*lévy|charFun.*Ioc|Ioc.*charFun' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib

rg -n -i --glob '*.lean' \
  'dirichlet.*integral|integral.*sin.*/|integral.*sin.*inv|sin.*integral.*pi|tendsto.*sinc|integral_sinc|sinc.*integral|fourier.*(Ioc|Icc|interval|indicator)|(Ioc|Icc|interval|indicator).*fourier' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib | head -200
```

The exact prohibited-construct scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|^[[:space:]]*(?:opaque|constant|extern)[[:space:]]' \
  Stage1_Instances/THM-M-1018 --glob '*.lean'
```

## Retry Condition

Resume after a placeholder-free implementation of the frozen analytic packages above, or after an
immutable compatible Lean 4 terminal proof is present in the pinned closure and can pass exact-type,
terminal-body, provenance, placeholder, axiom, composition, and trust checks without changing the
target or dependency lock.

This owned artifact is current-base blocker evidence, not a proof receipt. It does not satisfy
`S56-M-1018-PROOF`, propose an item-state transition, or support audit completion, validation,
release, theorem completion, receipt acceptance, or master acceptance.
