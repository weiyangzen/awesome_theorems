# Anchor audit record

Item: `S56-M-1058-ANCHOR_AUDIT`  
Base revision: `14b3498b20eaa72406a51b89bb3c409701a8c903`  
Audit date: 2026-07-12

## Result

The immutable local candidate is mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It provides the exact substrate
used by the frozen statement: probability measures and their measure coercion,
extended-real `limsup`/`liminf`, lower semicontinuity, and `ENNReal.log` with
`log 0 = bot`. `AnchorAudit.lean` checks these APIs against the pinned package.

No terminal `LargeDeviationPrinciple`, probabilistic Cramer theorem, Sanov
theorem, Gartner-Ellis theorem, Varadhan lemma, rate-function API, or Laplace
principle was located in the complete pinned mathlib source tree or the other
pinned Lake package sources. Cramer hits are matrix Cramer's rule and are not
probability candidates. `ProbabilityMeasure.limsup_measure_closed_le_of_tendsto`
in `Mathlib.MeasureTheory.Measure.Portmanteau` is a weak-convergence closed-set
inequality without logarithmic scaling or a rate function, so it is not a
terminal or near-exact LDP candidate.

The historical local `S1_M_250.lean` is also not terminal evidence. Its
`largeDeviationPrinciple_of_obligations` merely projects upper and lower LDP
bounds already supplied in `LargeDeviationProofObligations`, and its data uses
an abstract extended logarithm rather than the frozen statement's direct
`ENNReal.log`. It remains discovery material only.

External repository search found no exact LDP candidate. A repository titled
`gibbs-variational` appeared for a Varadhan query, but its advertised
Donsker-Varadhan variational principle is a different claim; it was not
broadened into this target. Unauthenticated GitHub code search was rate-limited,
so it yields no evidence. The older immutable negative search of
`uw-math-ai/central_limit_theorem` at
`0ed57e943d642eaa95fe547780024b9e3a0dfbdf` is retained only as a rejected,
irrelevant candidate; no dependency was fetched or changed.

The node conclusion is therefore `M3 / formalization_debt`, not
`repo_local_integration_debt`: no exact external proof body exists among the
verified candidates that could presently be pinned/imported/checked. This
completes the bounded anchor audit, not the theorem. Proof, trust, provenance,
hermetic validation, and release gates remain open.

## Commands and results

All package inspection was read-only. No `lake update`, build, clone, fetch, or
change beneath `.lake` was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1058` | 0 | rank 250, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i --glob '*.lean' 'large.?deviation\|LargeDeviation\|Cram[eé]r\|Sanov\|Varadhan\|GartnerEllis\|Gärtner.Ellis\|LaplacePrinciple\|RateFunction' Formalizations/Lean/.lake/packages` | 0 | no relevant probability/LDP declaration; only unrelated matrix Cramer and cone-author hits |
| `lake env lean ../../Stage1_Instances/THM-M-1058/AnchorAudit.lean` (from `Formalizations/Lean`) | 0 | all six pinned substrate probes elaborated |
| `lake env lean ../../Stage1_Instances/THM-M-1058/Statement.lean` (from `Formalizations/Lean`) | 0 | frozen target and direct-expansion transport elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-1058/anchor-audit.json >/dev/null` | 0 | structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1058` | 0 | no whitespace errors |
