# THM-M-1241 anchor-audit validation

Item: `S56-M-1241-ANCHOR_AUDIT`

The pinned mathlib candidate module elaborates locally. Its five nearby declarations are genuine
kernel-checked special cases, but none has the canonical statement type. In particular, none covers
arbitrary `m,j,q,r,a`, the product of two powered norms, infinity endpoints, coordinate-derivative
maxima, and both of Nirenberg's printed exceptions. No wrapper or theorem completion is claimed.

## Immutable anchors

| Surface | Immutable identity |
|---|---|
| worker base | `ad0567008a38fc8c39deda009ab34e4ca9910f46` |
| Lean | `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| mathlib | commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| candidate source | `Mathlib/Analysis/FunctionalSpaces/SobolevInequality.lean`, last source commit `d0a53972acfb6b7d9de9fcf09c19073c990177f6` |

## Exact validation

All commands ran from the worker clone unless a `cwd` is stated.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 targets accepted |
| `python3 scripts/stage1_target.py check` | 0 | unique ranks 1..1546, uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | rank 422; planned; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'gagliardo\|nirenberg\|interpolation inequal\|interpolation.*sobolev\|sobolev.*interpolation' Formalizations/Lean/.lake/packages -g '*.lean' -g 'README*' -g 'lake-manifest.json'` | 0 | only pinned mathlib's `SobolevInequality.lean` matched |
| `rg -n '\bsorry\b\|\badmit\b\|\baxiom\b\|\bunsafe\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/FunctionalSpaces/SobolevInequality.lean` | 1 | expected negative search: no forbidden token |
| `lake env lean ../../Stage1_Instances/THM-M-1241/AnchorAudit.lean` (`cwd=Formalizations/Lean`) | 0 | all five declarations elaborated; every `#print axioms` reported `[propext, Classical.choice, Quot.sound]` |
| `python3 -m json.tool Stage1_Instances/THM-M-1241/anchor-audit.json` | 0 | structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1241 .stage1-worker-selftest.json` | 0 | no whitespace errors |

External discovery on 2026-07-12 used GitHub's unauthenticated repository API. Queries for
`"Gagliardo-Nirenberg" Lean` and `"SobolevInequality.lean"` each returned `total_count: 0`.
GitHub code search returned HTTP 403 and grep.app returned HTTP 429. Therefore this audit makes a
truthful negative finding for the locally pinned closure and the completed public repository
queries, but does not pretend that rate-limited public code search was exhaustive.

Verdict: anchor audit self-tested; exact candidate absent; root remains open with formalization
debt. Master acceptance is still required, and neither audit completion nor theorem completion is
asserted.
