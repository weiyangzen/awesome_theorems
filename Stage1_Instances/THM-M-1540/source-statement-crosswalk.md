# Source-statement crosswalk

## Primary source candidate

Roger Penrose, "Twistor Algebra," *Journal of Mathematical Physics* **8** (1967), 345-366,
DOI `10.1063/1.1705200`. This is the historical source matching the repository's 1967 attribution.
The bibliographic identification is an intake anchor only: the exact numbered result, page span,
definitions, assumptions, and errata have not yet been inspected and therefore do not establish
`H0`.

For terminology and theorem discovery, Roger Penrose and Wolfgang Rindler, *Spinors and Space-Time,
Volume 2: Spinor and Twistor Methods in Space-Time Geometry*, Cambridge University Press (1986), is
a secondary candidate. It cannot replace row-by-row verification against the chosen primary result.

## Crosswalk

| Repository phrase | Scoped mathematical content | Required Lean object | Intake status |
|---|---|---|---|
| "twistor theory" | classical flat-space incidence geometry | explicit finite-dimensional complex vector and projective spaces | narrowed; definitions open |
| "spacetime" | complexified conformal compactification of Minkowski space | concrete quotient/Grassmannian or equivalent model | included; encoding open |
| "twistor" | nonzero twistor modulo complex scaling | projectivization with nonzero condition | included; convention open |
| "description" | point/projective-line correspondence | two maps plus inverse or a typed equivalence | intended; exact strength open |
| incidence | spinorial incidence equation | typed linear/bilinear equation | included; indices and sign open |
| real spacetime | fixed/reality-compatible locus | conjugation and Hermitian reality condition | source-dependent, not yet frozen |

## Fidelity gate

The legacy phrase is too broad to elaborate truthfully. Before `H0` or statement acceptance, an
independent reviewer must verify the primary edition, exact theorem/page, surrounding definitions,
all hypotheses, direction of correspondence, boundary cases, and errata. The resulting source rows
must map one-to-one to Lean binders and hypotheses. A nearby projective-geometry theorem or a
definition of the incidence relation is not an acceptable substitute.

