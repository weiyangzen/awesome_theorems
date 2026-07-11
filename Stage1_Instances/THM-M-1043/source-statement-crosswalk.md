# Source-statement crosswalk

## Candidate primary sources

- Mark Kac, "On distributions of certain Wiener functionals," *Transactions of the American
  Mathematical Society* 65 (1949), 1-13. This is a historical primary paper candidate for the
  Wiener-functional/heat-equation form. The precise displayed formula, assumptions, and errata
  have not yet been inspected from a stable scan.
- Bernt Oksendal, *Stochastic Differential Equations: An Introduction with Applications*, sixth
  edition, Springer (2003), section 8.2 (the Feynman-Kac formula). This is a modern source candidate
  for an SDE/generator statement; exact theorem numbering, wording, hypotheses, and errata remain
  to be verified against the edition.

These citations are discovery anchors, not `H0` evidence. The statement phase must select and
inspect one exact theorem, and must not silently merge the broader modern formula with Kac's
historical special case.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "probabilistic representation of a PDE" | solution equals a path expectation | equality between a concrete PDE solution and integral under a path law | included; exact expression open |
| diffusion and generator | Markov process associated to the differential operator | process/SDE law and a checked generator relation | included; object model open |
| killing potential | exponential of the negative time integral of `V` | measurable path integral, exponential, and integrability | included; sign frozen only after source selection |
| source term | accumulated inhomogeneous forcing along the path | time integral with the correct discount factor | included; convention open |
| terminal payoff | boundary value at the finite horizon | evaluation of `g` at terminal state, possibly stopped | included; domain/exit behavior open |
| sufficiently regular solution | classical PDE and uniqueness hypotheses | derivative, measurability, boundedness, and uniqueness predicates | included; exact hypotheses open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_236.lean` records useful candidate conventions and
mathlib kernel/integration discovery. Its `FeynmanKacData.probabilisticRepresentation` and related
well-formedness facts are assumed fields rather than a construction of the path expectation, and
the module says it does not prove Feynman-Kac. It therefore supplies neither an exact source
statement nor terminal proof closure. Its upstream API observations must be repeated at the pinned
revision during anchor audit.

Before `H0`, an independent reviewer must verify edition, theorem/page or formula anchor,
definitions, hypotheses, time/sign conventions, boundary cases, and errata, then approve a
row-by-row source-to-Lean mapping.
