# Source-statement crosswalk

## Candidate source boundary

The repository metadata attributes the theorem family to Paul Levy and Aleksandr Khinchin in 1934,
but provides no title, edition, theorem number, page, source text, assumptions, or errata record.
That is historical discovery metadata, not H0 evidence. The statement/anchor audit must inspect an
immutable primary source or explicitly justify an authoritative edition that states the intended
process version, rather than importing a familiar modern formula from memory.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Levy-Khinchin representation" | one exact characteristic-exponent formula | a fully elaborated expression using one convention | family frozen; formula and source pinpoint open |
| "Levy process" | zero start, stationary independent increments, and selected continuity condition | concrete process, law, filtration, and increment predicates | included; API and binder order open |
| "characteristic function" | expectation/Fourier transform of the time-`t` marginal | measurable complex exponential and integral against the law | included; Fourier sign open |
| exponential time dependence | marginal convolution-semigroup identity | equality to `exp (t * psi u)` for the selected time and scalar types | included; logarithm-free formulation preferred but not fixed |
| drift/Gaussian/jump data | characteristic triplet and Levy measure | scalar parameters, measure predicate, compensated integral | included; normalization and uniqueness open |
| converse | valid triplet produces a Levy process or convolution semigroup | existence construction with all process hypotheses | source-dependent; not claimed or discarded at intake |

## Normalization hazards

Fourier signs, the factor multiplying the Gaussian quadratic term, and choices such as
`x * 1_{|x| <= 1}` versus other truncation functions alter the displayed exponent and drift. These
forms are not definitionally interchangeable. The source audit must map every term, assumption, and
boundary case row by row; any alternate encoding needs a checked Lean transport.

The current human status is provisional `H2`: the named family and claim components are identified,
but exact edition/theorem/page, assumptions, referenced definitions, errata, and independent review
are absent. No repository-local or external formal declaration is credited by this intake.
