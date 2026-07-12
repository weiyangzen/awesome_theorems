# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` identifies the theorem as the Poisson integral formula, attributes
it to Simeon Poisson (1820), and summarizes it as the solution of the Dirichlet problem on a disk.
`Docs/Stage0_Blueprint.md` repeats that metadata. These are intake provenance, not primary-source or
`H0` evidence, and their untrusted "verified" label provides no machine-proof credit.

## Candidate mathematical sources

- Simeon-Denis Poisson's 1820-era work is the historical attribution to investigate. The exact
  publication, edition, theorem location, notation, and assumptions have not yet been inspected.
- A stable modern complex-analysis or potential-theory edition containing the disk Dirichlet theorem
  must be selected for an exact theorem/page crosswalk if the historical source does not state the
  modern continuous-boundary formulation.

No exact theorem/page or errata claim is made at intake. These candidates cannot support `H0` until
the statement phase records a stable edition and an independent review.

## Crosswalk

| Repository phrase | Frozen mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Poisson integral formula" | Poisson-kernel boundary integral | `Real.circleAverage (poissonKernel c w • g) c R` | frozen |
| "on a disk" | open disk, closed disk, boundary circle, `R > 0` | `ball c R`, `closedBall c R`, `sphere c R` | frozen |
| "Dirichlet problem" | prescribed continuous boundary trace | `ContinuousOn g (sphere c R)` and `EqOn u g (sphere c R)` | frozen |
| "solution" | constructed extension with analytic properties | existential `u`, `HarmonicOnNhd`, closure continuity | frozen |
| interior formula | kernel integral evaluates the extension | equality at every `w ∈ ball c R` | frozen |

The repository metadata is too terse to decide a different classical variant. The statement phase
therefore follows the fuller human scope frozen by the accepted intake dependency. This is an exact
Lean target decision, not H0: the historical/modern primary-source pinpoint and independent review
remain open.

## Lean discovery boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_144.lean`, for the distinct target `THM-M-1154`,
imports `Mathlib.Analysis.Complex.Harmonic.Poisson` and checks the adjacent theorem
`HarmonicOnNhd.circleAverage_poissonKernel_smul`. It also records a disk Dirichlet special-case shape,
but explicitly leaves construction, harmonicity, closure continuity, and boundary trace open. It is
therefore discovery input only. The anchor audit must inspect declarations and terminal bodies at the
pinned revision and may not turn this adjacent result into closure of THM-M-1148.

Before `H0`, an independent reviewer must verify the chosen source's edition, theorem/page,
definitions, all assumptions, normalization, limiting argument, uniqueness scope, and errata, then
approve a row-by-row mapping to the exact Lean expression.
