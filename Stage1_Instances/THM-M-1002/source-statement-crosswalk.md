# Source-statement crosswalk

## Candidate primary sources

- J. L. Doob, *Stochastic Processes*, Wiley (1953), the martingale convergence results in the
  martingale chapter. This is the historical primary monograph candidate. Exact theorem number,
  page, edition wording, hypotheses, and errata have not yet been inspected.
- J. L. Doob, "Regularity properties of certain families of chance variables," *Transactions of
  the American Mathematical Society* 47 (1940), 455-486. This is a historical primary-paper
  candidate whose precise relationship to the named modern theorem still requires inspection.

These anchors establish neither `H0` nor exact statement fidelity. A stable scan/edition and an
independent review are required downstream.

## Crosswalk

| Repository/source phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "Doob martingale convergence theorem" | classical discrete-time convergence family | explicit theorem proposition, not a package field | family fixed; exact source row open |
| "upper and lower martingales" | supermartingale and submartingale branches | `Supermartingale` / `Submartingale` over a filtration | included; terminology transport open |
| one-sided boundedness | uniform bound on positive/negative parts | integral/expectation of positive or negative part | exact convention open |
| convergence | pointwise convergence outside a null set | `∀ᵐ ω ∂μ, Tendsto ... atTop ...` | intended encoding identified |
| finite limit | real-valued terminal random variable | measurable/integrable limit or `Filtration.limitProcess` | exact conclusion open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_282.lean` imports
`Mathlib.Probability.Martingale.Convergence` and contains a checked historical wrapper around
`MeasureTheory.Submartingale.ae_tendsto_limitProcess`, plus a supermartingale transport by
negation. Its statement assumes a uniform `eLpNorm`-one bound and targets mathlib's
`Filtration.limitProcess`. That is valuable candidate evidence, but it is potentially stronger
than the classical one-sided source hypothesis and has not passed rev-5.6 exact-statement,
provenance, freshness, or receipt gates. It therefore supplies no accepted intake proof credit.

Before `H0`, an independent reviewer must verify edition, theorem/page, all assumptions, terminology,
errata, and every source-to-Lean row. Before any `M0` claim, the exact chosen expression and checked
transports must be elaborated against the pinned environment.
