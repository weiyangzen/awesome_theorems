# Source-statement crosswalk

## Candidate primary sources

- Norbert Wiener, "Differential-Space", *Journal of Mathematics and Physics* 2 (1923), 131-174,
  is the historical construction/source candidate. Exact theorem numbering, wording, and the
  extent of its differentiability result have not yet been inspected.
- Peter Morters and Yuval Peres, *Brownian Motion*, Cambridge University Press (2010), chapters on
  Brownian paths, is a modern rigorous source candidate. Exact theorem/page, edition wording, and
  errata remain to be inspected.

These references are discovery anchors only, not `H0` evidence. The statement phase must select an
inspectable edition and cross-check every hypothesis and quantifier.

## Crosswalk

| Repository phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Wiener process" | standard real Brownian process | concrete process plus probability measure and Brownian-law predicate | included; representation open |
| "continuous" | sample path continuity on nonnegative time | `ContinuousOn` or continuity on an intrinsic time subtype | included; version convention open |
| "nowhere differentiable" | failure of a finite derivative at every time | likely `¬ DifferentiableWithinAt ℝ` on the time domain | included; endpoint/source convention open |
| "almost surely" | one or two probability-one path events | `∀ᵐ ω ∂P, ...` and event measurability as required | included; event combination open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_221.lean` records relevant pinned-mathlib APIs,
including Gaussian processes, independent increments, Kolmogorov moment conditions, and a proposed
`Set.Ici 0`/`DifferentiableWithinAt` encoding. Its `WienerPathRegularityConclusion` stores the
terminal path properties as fields, so projections from it are not a proof of the source theorem.
Its claims about missing or external APIs must be repeated against immutable revisions in the
anchor-audit phase.

Before `H0`, an independent reviewer must verify the selected source's edition, theorem/page,
definitions, assumptions, modification convention, endpoint semantics, and errata, then approve a
row-by-row source-to-Lean mapping.
