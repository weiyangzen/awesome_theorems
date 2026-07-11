# Source-statement crosswalk

## Candidate primary sources

- Paul Levy, *Theorie de l'addition des variables aleatoires* (1937), historical primary monograph
  candidate. Exact edition, theorem/page, hypotheses, and errata have not been inspected.
- Patrick Billingsley, *Convergence of Probability Measures*, modern textbook candidate for the
  weak-convergence formulation. Exact edition, theorem/page, wording, and errata remain open.

These are discovery anchors, not H0 evidence. A later source audit must inspect a stable edition and
record the theorem verbatim enough to distinguish the known-limit equivalence from the stronger
existence form.

## Crosswalk

| Repository phrase | Frozen mathematical meaning | Expected Lean component | Intake status |
|---|---|---|---|
| "characteristic functions converge" | pointwise convergence at every frequency | `charFun`, `Tendsto`, `atTop` | included; exact coercions open |
| "weak convergence" | convergence of probability measures to specified `mu0` | topology on `ProbabilityMeasure E` | included; topology audit open |
| "Levy continuity theorem" | known-limit iff, not arbitrary-limit construction | `Iff` between the two convergence claims | frozen intent |
| finite-dimensional real domain | Euclidean-style Fourier pairing | real inner product and finite-dimensional instances | included; binder order open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_291.lean` imports
`Mathlib.MeasureTheory.Measure.LevyConvergence` and records the candidate declaration
`MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun`. It also clearly separates the
stronger arbitrary-limit existence statement. Under rev-5.6 the file is discovery input only: its
exact type, imports, axiom profile, pinned revision, and wrapper must be rechecked and accepted in
later phases.

Before H0, an independent reviewer must verify the chosen source edition, theorem/page, definitions
of weak convergence and characteristic function, all domain assumptions, normalization/sign
conventions, and errata, then approve the row-by-row mapping.
