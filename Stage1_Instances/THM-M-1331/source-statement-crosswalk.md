# Source-statement crosswalk

## Repository provenance

`Docs/researches/math_theorems.md:9712-9717` is the only repository source record. It gives the
title, Cauchy/Picard attribution, year 1890, the Chinese gloss `Lipschitz条件下解的存在唯一性`,
importance `高`, and status `已验证`. All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; they contain no citation.

`Docs/Stage0_Blueprint.md:36210-36234` projects that record as `THM-M-1331` and explicitly marks the
precise definitions, premises, proof route, equivalent statements, axioms, and formal artifact as
open. Neither file is a primary mathematical source. The verified label supplies no `H0` or
machine-proof credit.

## Primary-source status

No immutable primary edition, theorem or page locator, definition chain, exact transcription,
translation review, errata search, or independent reviewer is present in the repository or accepted
by this intake. The Cauchy/Picard attribution and 1890 date are discovery metadata only. A later
source audit must select and hash an edition, record the exact theorem and incorporated definitions,
and crosswalk every premise and conclusion below. Familiar historical naming is not a substitute.

## Claim crosswalk

| Catalogue component | Mathematical choice still required | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| solutions | scalar equation, finite-dimensional system, or Banach-valued curve; solution regularity | `Real -> E`, `HasDerivAt` or `HasDerivWithinAt`, or an integral equation | family identified; domain and predicate open |
| Lipschitz condition | local/global, state/time variable, uniform constant, region, and range restriction | `LipschitzOnWith`/`LipschitzWith` for `f t` on a ball or source set | essential hypothesis named; exact scope open |
| existence | initial data, interval, continuity and bound assumptions, and one/two-sided endpoint behavior | `IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt` is an adjacent candidate | candidate API only; no exact source match or proof credit |
| uniqueness | class of eligible solutions, common domain, local/global equality, and range membership | `ODE_solution_unique_of_mem_Icc` or `_eventually` are adjacent candidates | separate API with conventions that must be composed and mapped |
| 1890/Cauchy/Picard | historical work and exact version intended | no Lean component | bibliographic lead only |
| verified | claimed prior formal status | none | explicitly untrusted under rev-5.6 |

## Pinned Lean discovery boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.ODE.PicardLindelof` defines `IsPicardLindelof`. Its assumptions include a
time-dependent vector field on a normed complete real space, a state-Lipschitz condition on a
closed ball, continuity in time, a uniform norm bound, and an interval-radius inequality. Its
`exists_eq_forall_mem_Icc_hasDerivWithinAt` theorem supplies existence in differential form.

Uniqueness is separate in `Mathlib.Analysis.ODE.Gronwall`, including
`ODE_solution_unique_of_mem_Icc` and `ODE_solution_unique_of_eventually`. A source-faithful combined
existence-and-uniqueness root would need a checked bridge aligning interval, derivative, continuity,
and range conventions. `IntakeProbe.lean` authenticates only these names and types in the pinned
environment. This is `M3` interface discovery, not a selected target, formal-anchor audit, terminal
proof-body audit, or `M0` result.

## Neighbor and non-substitution check

The catalogue immediately follows this item with `THM-M-1332`, the Picard-Lindelof theorem. That
record says only "existence and uniqueness of ODE solutions" and cites Picard/Lindelof in 1894.
No primary-source evidence currently proves that the two IDs denote distinct propositions. The
statement phase must record an approved distinction, alias, or correction before either target may
claim an overlapping formal root.

Existence under continuity alone is the separate Peano theorem and cannot replace the Lipschitz
claim. Conversely, Gronwall uniqueness alone cannot establish existence. A global theorem cannot
be inferred from local Lipschitz data without additional source-specified hypotheses.

Before `H0`, an independent reviewer must verify the immutable source, theorem/page, definitions,
all assumptions, conclusion, historical attribution, translation, errata, and the identity boundary
with `THM-M-1332`. Before any machine-completion claim, the exact combined Lean target and bridge
must pass the statement, provenance, trust, composition, and release gates.
