# Anchor audit

Item: `S56-M-0600-ANCHOR_AUDIT`  
Base revision: `63728668acb87acd4bab7e755151dce89dc1eeb4`

## Frozen search boundary

The audited root is exactly `Stage1Instances.THM_M_0600.MorseLemmaTarget` from
`Statement.lean`, not a Hessian-diagonalization theorem, inverse function
theorem, minimum-only case, or Morse-theory consequence. The local environment
pins mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`
and Lean commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.

Repository-local Lean and the complete pinned mathlib source tree were searched
for the Morse lemma, nondegenerate critical points, Hessians, local normal
forms, quadratic forms, and relevant inverse/implicit-function APIs. No exact
declaration matching the frozen root was identified.

## Pinned mathlib candidates

| Module / declaration | Audited role | Root verdict |
|---|---|---|
| `Mathlib.LinearAlgebra.QuadraticForm.Real` / `QuadraticForm.equivalent_one_neg_one_weighted_sum_squared` | Sylvester diagonalization of a nondegenerate finite-dimensional real quadratic form with weights `-1` or `1` | ingredient only; no nonlinear local coordinates or equality for `f` |
| `Mathlib.LinearAlgebra.QuadraticForm.Signature` / `QuadraticForm.sigPos_add_sigNeg_add_radical` | dimension accounting for positive, negative, and radical parts | ingredient only; no local normal form |
| `Mathlib.Analysis.Calculus.InverseFunctionTheorem.ContDiff` / `ContDiffAt.to_localInverse` | smooth local inverse from an invertible derivative | ingredient only; generic analytic API |
| `Mathlib.Analysis.Calculus.ImplicitContDiff` / `ContDiffAt.contDiffAt_implicitFunction` | smooth implicit function | ingredient only; generic analytic API |

`AnchorAudit.lean` checks the exact types of the first three candidates against
the pinned build. Inspection of their source bodies shows ordinary theorem
proofs with no placeholder, new axiom, or unsafe declaration at these
terminal anchors. This is provenance for ingredients only: their transitive
closure and full trust surface are reserved for the later obligation and
validation phases.

## External Lean 4 search

On 2026-07-12, Sourcegraph global indexed-code queries were run with forks and
archives included for `MorseLemma`, `"Morse lemma"`,
`"nondegenerate critical point"`, `"Morse theory"`, `morse_lemma`, and
`morseLemma`, each restricted to Lean. Every query completed with
`matchCount: 0`. GitHub repository searches for combinations of Morse lemma,
Lean, and Lean 4 also returned zero repositories. Anonymous GitHub code search
was not available: the REST endpoint returned HTTP 401 and the web interface
required sign-in, so it is recorded as unavailable rather than credited.

This is bounded negative evidence, not a universal nonexistence claim. It does
not cover private, unindexed, or future repositories. Consequently there is no
external immutable candidate to inspect, pin, import, or assign proof credit.

## Classification

The vector remains `[H1, M4, R3]`. The exact target is a standard known human
theorem, but this audit found no exact Lean 4 closure. The current debt is
`formalization_debt`, not `repo_local_integration_debt`: no external machine
proof was found that awaits integration. The anchor-audit phase is complete and
self-tested; the Morse theorem is not proved, audit completion for the entire
dossier is not claimed, and no `M0` or theorem-completion state follows.

## Commands and results

All local commands ran inside this automation clone; Lean ran from
`Formalizations/Lean` using existing pinned Lake artifacts. No Lake update,
dependency fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure valid: 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | target manifest valid; ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0600` | 0 | rank 638, planned, hard-statement-first lane, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned mathlib/repository `rg` searches documented above | 0 | no exact Morse-lemma declaration; four ingredient families identified |
| six Sourcegraph queries documented above | 0 | each completed with `matchCount: 0` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0600/AnchorAudit.lean` | 0 | exact types of Sylvester, signature, and smooth-local-inverse ingredients elaborated |
| `git diff --check -- Stage1_Instances/THM-M-0600 .stage1-worker-selftest.json` | 0 | no whitespace errors |
