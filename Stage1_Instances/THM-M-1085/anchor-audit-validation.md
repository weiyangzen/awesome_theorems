# Anchor-audit validation record

Item: `S56-M-1085-ANCHOR_AUDIT`  
Base revision: `7fade6ac1192f68266bd22be9fb2c754785b0727`  
Search cutoff: `2026-07-12T04:08:26Z`

## Result

The exact frozen target was not found. The closest pinned mathlib artifacts provide joint-Gaussian
definitions, characteristic-function facts, and finite-dimensional process projections, but no
theorem whose conclusion compares lower-tail probabilities under an off-diagonal covariance order.
The exact-candidate inventory is therefore empty and current machine debt is `M4`. This is a bounded
negative audit, not evidence that no Lean formalization exists anywhere.

Pinned mathlib is `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, tag `v4.29.0`). The relevant source hashes are
`ad92ad1a...f5192` for `HasGaussianLaw/Basic.lean` and `1dce719a...f83` for
`IsGaussianProcess/Def.lean`; the Lake manifest hash is `321626c8...2d81`.

## Exact commands and results

All Lean commands ran from `Formalizations/Lean` against the existing pinned `.lake` environment.
No dependency update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `git -C .lake/packages/mathlib grep -n -i -E 'slepian|gaussian (comparison|inequality)|normal comparison' 8a178386ffc0f5fef0b77738bb5449d50efeea95 -- 'Mathlib/*.lean' 'Mathlib/**/*.lean'` | 1 | zero matches |
| `git -C .lake/packages/flt-regular grep -n -i -E 'slepian|gaussian (comparison|inequality)|normal comparison' 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27 -- '*.lean' '**/*.lean'` | 1 | zero matches |
| three Sourcegraph stream searches over global Lean, with `archived:yes fork:yes` | 0 each | exhaustive `matchCount: 0`, `skipped: []` for `Slepian`, `"Gaussian comparison"`, and `covariance Gaussian comparison` |
| four GitHub repository-search API queries | 0 each | `total_count: 0`, `incomplete_results: false` |
| GitHub unauthenticated code-search API for `Slepian language:Lean` | 22 (`curl`) | HTTP 403; access limitation, not counted as negative evidence |
| `lake env lean ../../Stage1_Instances/THM-M-1085/AnchorAudit.lean` | 0 | closest APIs elaborated; axiom output recorded in `anchor-audit.json` |
| `python3 -m json.tool ../../Stage1_Instances/THM-M-1085/anchor-audit.json` | 0 | valid JSON |
| `python3 ../../Stage1_Instances/THM-M-1085/check_statement.py` | 0 | frozen target unchanged; expression SHA-256 `2af285ae...d43315` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1085` | 0 | rank 527, `L0/rework_required`, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1085 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Boundary

This phase does not claim a proof, `M0`, `M1`, `H0`, audit completion, or theorem completion. The
next task must construct the obligation tree without pretending that the supporting Gaussian APIs
close any comparison step. Master acceptance remains required.
