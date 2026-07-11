# Source-statement crosswalk

## Candidate primary sources

- Joseph L. Doob, *Stochastic Processes*, Wiley (1953), the discrete-parameter martingale stopping
  results. This is the historical source candidate suggested by the repository's 1953 attribution;
  exact chapter, theorem, page, edition conventions, and errata have not yet been inspected.
- Joseph L. Doob, "Regularity properties of certain families of chance variables," *Transactions
  of the American Mathematical Society* 47 (1940), 455-486. This is a historical martingale source
  candidate, not yet verified as the source of the precise bounded two-stopping-time formulation.

These are discovery anchors only and do not establish `H0`. A stable scan/edition must be inspected
before the statement is represented as source-exact.

## Crosswalk

| Repository phrase | Intended component | Candidate Lean component | Intake status |
|---|---|---|---|
| "martingale expectation at stopping times" | equality of stopped expectations | `Martingale`, `Measure.integral`, `stoppedValue` | included; exact types open |
| stopping time | time observable from the filtration | `MeasureTheory.IsStoppingTime` | candidate API identified |
| ordered times | `tau <= pi` pointwise | function order on `Omega -> WithTop Nat` | included; source convention open |
| bounded | deterministic finite bound on the later time | `exists N, forall omega, pi omega <= N` | included; exact source hypothesis open |
| expectation | integral of the stopped real process | `mu[stoppedValue f tau]` | candidate encoding only |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_284.lean` imports mathlib optional-sampling and
optional-stopping modules and proposes the same bounded discrete equality. It is legacy discovery
material under the uniform L0 baseline: its declarations, imports, proof provenance, axioms, and
source fidelity receive no acceptance from this intake. The statement and anchor-audit phases must
recheck the pinned mathlib declarations and determine whether the equality has a genuine terminal
proof body rather than merely packaged assumptions or wrappers.

Before `H0`, an independent reviewer must verify the selected source theorem and definitions,
every hypothesis and boundary case, edition/errata status, and the complete source-to-Lean mapping.
