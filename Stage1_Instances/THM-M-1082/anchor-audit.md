# Formal-anchor audit

Item: `S56-M-1082-ANCHOR_AUDIT`. Audit date: 2026-07-12.

## Exact pinned mathlib anchor

The Lake manifest and dependency worktree both identify mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. At that revision,
`Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def` defines
`ProbabilityTheory.IsGaussianProcess X P` as a one-field `Prop` structure whose field is exactly

```text
forall I : Finset T,
  HasGaussianLaw (fun omega => I.restrict (X . omega)) P
```

This is the frozen target's right-hand side, with the same universes, binders, typeclass
assumptions, measure, finite-index encoding, and inclusion of the empty finset. The upstream
definition source has SHA-256 `1dce719a...66cfb83`; its sole imported Gaussian-law definition has
SHA-256 `e5237228...091ab`. The definition entered mathlib in immutable commit
`09d61411b03a162bb9e3fc8afb8dea33e211a09f` (2026-01-27) and the audited source at the pin most
recently received a documentation-only edit in `88a2f718a08768772d7b2433fdd979be128f920c`.

The exact candidate is therefore a pinned mathlib definition plus a local checked two-way wrapper,
not an independently deep upstream theorem. `Statement.lean` and the independent
`AnchorAudit.lean` probe both construct the reverse direction with the public structure constructor
and obtain the forward direction with its public projection. Lean reports only mathlib's expected
`propext`, `Classical.choice`, and `Quot.sound` foundation profile for the audit probe, with no
custom axiom. This is an exact `M0-W` candidate for the later proof and trust gates; this phase inventories
it but does not promote proof, validation, release, or theorem-completion state.

`IsGaussianProcess.Basic` contains useful consequences such as `hasGaussianLaw_eval`,
`hasGaussianLaw_sum`, `of_isGaussianProcess`, `comp_right`, and `restrict`. None is needed to close
this definitional characterization, and none receives duplicate proof-body credit.

## External Lean 4 candidates

A bounded Sourcegraph search returned 100 matches in three repositories and hit its result limit.
Besides mathlib, it found `RemyDegenne/brownian-motion` at commit
`62df9fdf929642afcbc77e880135b468328b86c6` and `facebookresearch/atlas-lean` at commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50`. Both import mathlib's
`IsGaussianProcess` API and prove consequences or particular Brownian processes; neither supplies
a different terminal proof of the frozen definition-characterization equivalence.

The inspected brownian-motion module
`BrownianMotion/Gaussian/GaussianProcess.lean` has source SHA-256
`0a51f127...123dfe`, pins Lean `v4.31.0` and mathlib
`fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`, and contains covariance/independence consequences.
It is outside the local dependency closure and is strictly unnecessary for the exact root. The
Atlas source likewise uses mathlib's predicate in a Brownian-motion development rather than
replacing its definition. These are `M3` support-only discovery records, not integration candidates.

The Sourcegraph response is content-bound by SHA-256 `0f7e3fdd...fbde6`. A GitHub repository
metadata search for `"Gaussian process" Lean4` returned a complete zero-result response with
SHA-256 `08c082fd...2600b2`; this is only a bounded metadata search and is not a claim of global
absence. No dependency was cloned, fetched, updated, or added.

## Classification boundary

The formal anchor inventory is complete for this phase: the exact candidate is the pinned mathlib
structure definition already checked through a local wrapper, and the discovered external projects
only consume that API. Human primary-source pinpointing remains open, so this audit supplies no
`H0`. Obligation freezing, transitive trust/provenance closure, release-grade validation,
independent review, and both terminal decisions remain downstream work.

## Commands and results

All commands ran from this worker clone on 2026-07-12. Lean used the existing pinned `.lake`
artifacts; no dependency mutation or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1082/AnchorAudit.lean` | 0 | exact independent wrapper elaborated; axioms were `propext`, `Classical.choice`, and `Quot.sound` only |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1082/Statement.lean` | 0 | frozen canonical wrapper re-elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386...a95` |
| `rg -n 'IsGaussianProcess\|HasGaussianLaw' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | exact definition and related pinned APIs inventoried |
| Sourcegraph query `context:global (IsGaussianProcess OR "Gaussian process") lang:Lean count:100` | 0 | 100 bounded matches in mathlib, brownian-motion, and atlas-lean; result limit recorded |
| GitHub repository query `"Gaussian process" Lean4` | 0 | complete metadata response with zero repositories |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1082` | 0 | rank 524, planned, theorem incomplete |
