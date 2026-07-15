# THM-M-0346 proof recheck at current base

Item: `S56-M-0346-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T16:13:31+08:00`

Base revision: `9db995936e3354d71e109c055e31b9e9588569c5`

Base tree: `12006c9a7309e04bbf337d2b19dc0eeae3c9b265`

## Verdict

`blocked`. The assigned proof phase remains `[ ]`; no completion self-test is issued.

The exact target is `Stage1.THM_M_0346.CarlesonTarget`: every complex `L^2` function on the
period-one additive circle has its inclusive symmetric Fourier partial sums converge to the
canonical `Lp` representative almost everywhere. The existing `Proof.lean` supplies real,
placeholder-free bodies for the representative certificate, period and exponent side conditions,
the exact dossier-local cutoff equality, an upstream-shaped specialization adapter, and
conditional almost-everywhere composition. A trust-zero replay checks all six bodies.

This does not prove `RawCarlesonHunt`. In particular,
`carlesonTarget_of_rawCarlesonHunt : RawCarlesonHunt -> CarlesonTarget` is a conditional adapter,
not a proof of its premise or the root. The actual external `partialFourierSum'` definition is not
imported, so the local reconstruction of its cutoff is not an upstream integration receipt.

The first failed gate is `M0346-L-CARLESON-HUNT`. The pinned package closure has neither a
Carleson package nor declarations named `carleson_hunt` or `partialFourierSum'`. Pinned mathlib's
`hasSum_fourier_series_L2` gives convergence in the `Lp` topology, not pointwise or
almost-everywhere convergence. Its pointwise theorem assumes a continuous function with summable
Fourier coefficients and cannot replace the arbitrary-`L^2` target.

The audited upstream history supplies no compatible proof body. Its sole Lean `v4.29.0` revision,
`306ae5b29300771aece1aa39f0a939183cc59486`, pins a different mathlib revision and defines
`carleson_hunt := sorry`. The first source-complete body at
`d422163115553c400bb93b6b3b0d50313b7a9f25` requires Lean `v4.30.0-rc2` and mathlib
`1a4917a18b30ea1333c195e597067fe044ac9176`; this repository is pinned to Lean `v4.29.0` and
mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The task forbids fetching or mutating
`.lake`, and no new compatible artifact is present at this base.

## Narrow evidence

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. Temporary
Lean objects were created below `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch, network request, external checkout, source import, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1,546 unique ordered targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0346` | 0 | Rank 839; lifecycle planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0346/check_obligation_tree.py` | 0 | Eleven obligations and 24 typed edges passed; denominator `1ff60884ffc043439ab5a7b812bc9f2e8133e9d1eb8d130330d43f2709439c8c5`; root open at M3. |
| `cd Formalizations/Lean && timeout 240 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0346/Statement.lean` | 0 | The exact canonical target elaborated under the pinned project environment. |
| Temporary isolated `lake env lean --trust=0 -t0` replay of copied `Statement.lean` and `Proof.lean` | 0 | The target and all six local declarations elaborated; every declaration was sorry-free and reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n --pcre2 '(?m)^\s*(?:axiom\|constant\|opaque)\b\|\b(?:sorry\|admit\|sorryAx\|unsafe\|extern\|implemented_by\|native_decide)\b' Stage1_Instances/THM-M-0346/{Statement,Proof,ObligationTree}.lean` | 1 | Expected no-match exit; no prohibited mechanism occurred in the owned Lean sources. |
| `find -L Formalizations/Lean/.lake/packages -maxdepth 1 -mindepth 1 -type d -printf '%f\\n' \| sort \| rg -i '^carleson$'` | 1 | Expected no-match exit; no pinned Carleson package exists. |
| `rg -n --glob '*.lean' 'theorem\s+carleson_hunt\b\|def\s+partialFourierSum.' Formalizations/Lean Stage1_Instances/THM-M-0346` | 1 | Expected no-match exit; the actual upstream theorem and API are absent. |
| `rg -n 'theorem hasSum_fourier_series_L2\|theorem has_pointwise_sum_fourier_series_of_summable\|theorem hasSum_fourier_series_of_summable' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Fourier/AddCircle.lean` | 0 | Located only the non-closing topology-valued and stronger-hypothesis mathlib results. |
| `git diff --name-status 6ac589f0d8c5a9eeb726a1a05def7f9467ea2e2d..HEAD --` over the canonical proof, registry, graph, anchor, pin, manifest, and execution-skill inputs | 0 | Empty output; only prior blocker evidence was integrated after the last recheck. |
| `cd Formalizations/Lean && timeout 30 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3`; the pinned environment is available. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent because the proof phase is incomplete. |

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
