# THM-M-0346 proof recheck at current base

Item: `S56-M-0346-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T18:15:55+08:00`

Base revision: `97cd9c492d95baa9b55d2d8b341844107f07e686`

Base tree: `bdd31de5f2fcd38078e4b5793b400a8105a3b8ba`

## Verdict

`blocked`. The assigned proof phase remains `[ ]`; no completion self-test is issued.

The exact target is `Stage1.THM_M_0346.CarlesonTarget`: every complex `L^2` function on the
period-one additive circle has its inclusive symmetric Fourier partial sums converge to the
canonical `Lp` representative almost everywhere. Existing `Proof.lean` has six real,
placeholder-free bodies for the representative certificate, period and exponent side conditions,
an upstream-shaped specialization adapter, the exact dossier-local cutoff equality, and
conditional almost-everywhere composition. A trust-zero isolated replay checks all six bodies.

This does not prove `RawCarlesonHunt`. In particular,
`carlesonTarget_of_rawCarlesonHunt : RawCarlesonHunt -> CarlesonTarget` is conditional and does not
close its premise or the root. The dossier-local `upstreamPartialFourierSum` reconstruction is not
an integration receipt for the absent external `partialFourierSum'` declaration.

The first failed gate is `M0346-L-CARLESON-HUNT`. The pinned dependency closure contains neither a
Carleson package nor source or compiled declarations for `carleson_hunt` and
`partialFourierSum'`. Pinned mathlib's `hasSum_fourier_series_L2` proves convergence in the `Lp`
topology, not pointwise or almost-everywhere convergence. Its pointwise theorem assumes a
continuous function with summable Fourier coefficients, so it cannot replace the arbitrary-`L^2`
target.

The read-only upstream-history cache still contains no compatible body. Tag `v4.29.0` resolves to
`306ae5b29300771aece1aa39f0a939183cc59486`, pins mathlib
`f1a99cc3d4b62bff01325ac228882baadea934af`, and defines `carleson_hunt := sorry`. The first audited
source-complete body, `d422163115553c400bb93b6b3b0d50313b7a9f25`, requires Lean
`v4.30.0-rc2` and mathlib `1a4917a18b30ea1333c195e597067fe044ac9176`. No one of the 970
cached upstream revisions uses this repository's mathlib pin
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The task forbids dependency fetching and `.lake`
mutation, and no compatible artifact is present at this base.

## Narrow evidence

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. Temporary
Lean objects were confined to `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch, network request, external checkout, source import, or `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1,546 unique ordered targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0346` | 0 | Rank 839; lifecycle planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0346/check_obligation_tree.py` | 0 | Eleven obligations and 24 typed edges passed; denominator `1ff60884fc043439ab5a7b812bc9f2e8133e9d1eb8d130330d43f2709439c8c5`; root open at M3. |
| `cd Formalizations/Lean && timeout 240 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0346/Statement.lean` | 0 | The exact canonical target elaborated under the pinned project environment. |
| Isolated replay of copied `Statement.lean` and `Proof.lean` with the Lean binary and `LEAN_PATH` obtained through existing `lake env`, using `--trust=0 -t0` | 0 | The target and all six local declarations elaborated; all were sorry-free and reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n --pcre2 '(?m)^\s*(?:axiom\|constant\|opaque)\b\|\b(?:sorry\|admit\|sorryAx\|unsafe\|extern\|implemented_by\|native_decide)\b' Stage1_Instances/THM-M-0346/{Statement,Proof,ObligationTree}.lean` | 1 | Expected no-match exit; no prohibited mechanism occurred in the owned Lean sources. |
| `find -L Formalizations/Lean/.lake/packages -maxdepth 1 -mindepth 1 -type d -printf '%f\n' \| sort \| rg -i '^carleson$'` | 1 | Expected no-match exit; no pinned Carleson package exists. |
| `rg -n --glob '*.lean' 'theorem\s+carleson_hunt\b\|def\s+partialFourierSum.' Formalizations/Lean Stage1_Instances/THM-M-0346` | 1 | Expected no-match exit; the actual upstream theorem and API are absent. |
| Scoped search under pinned `packages` and `build` for `Carleson/Classical/CarlesonHunt.{olean,ilean,ir}` | 0 | Empty output; no compiled Carleson-Hunt artifact exists. |
| `rg -n -C 8 'theorem hasSum_fourier_series_L2\|theorem has_pointwise_sum_fourier_series_of_summable\|theorem hasSum_fourier_series_of_summable' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Fourier/AddCircle.lean` | 0 | Located only the non-closing topology-valued and stronger-hypothesis results. |
| `git diff --name-status f53223e6746df4856b00068d3e8723264dfd044a..HEAD --` over canonical proof, registry, graph, anchor, pin, manifest, and execution-skill inputs | 0 | Empty output; no scoped proof source or pin changed since the preceding recheck base. |
| Read-only `git show`, `git grep`, and `rev-list` over all 970 revisions in `/tmp/carleson-inspect` | 0 | The Lean 4.29.0 body is `sorry`; the first source-complete body has incompatible pins; no revision matches the repository mathlib pin. |
| `cd Formalizations/Lean && timeout 120 lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3`; the pinned environment is available. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent because the proof phase is incomplete. |
| JSON parse, blocker-invariant assertions, and `git diff --check` over this owned pair | 0 | The record parsed, all blocked/open/no-selftest invariants held, and the diff had no whitespace errors. |

Source SHA-256 values are `a2af9f8bfdb524a60b3fc3d2e3eaaa064d8e70063d90e25a5134c79ae0bc4a4d`
for `Statement.lean` and `690e35222ca644aaf708ba0ab2ffc5d886b60209d46511edea6bfc1a60fbb81d`
for `Proof.lean`. Temporary object SHA-256 values were
`a349e94179235a765512cd39fca2fd50f09a0fb20009d0ad55155d2677906b82` and
`b7dd98fcb48d359df7bc92c1bea086896383aa08053f76772eb2852df44d2c91`.

## Boundary and retry condition

Lifecycle stays `planned`; the frozen root stays `[H3, M3, R4]`. The remaining root cut is
`M0346-C-REPRESENTATIVE`, `M0346-N-NORMALIZATION`, `M0346-N-CUTOFF`,
`M0346-L-CARLESON-HUNT`, and `M0346-T-AE-REP`. `audit_complete=false` and
`theorem_complete=false`. This record changes no scheduler state, accepts no receipt, and supports
no proof-completion, validation, release, audit-completion, theorem-completion, or master-acceptance
claim.

Resume after the integration lane provides an immutable, license-reviewed, placeholder-free
Carleson package compatible with the repository pins, or after a deliberate repository-wide pin
migration. Then import the actual theorem, check the exact external partial-sum transport, audit
its transitive terminal bodies and axioms, and compose the exact root. Until then,
`.stage1-worker-selftest.json` must remain absent.
