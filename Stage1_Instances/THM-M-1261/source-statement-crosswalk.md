# Source-statement crosswalk

## Source boundary

The repository research row says only "Lars Hormander, 1971" and "a tool for solving hyperbolic
equations." A relevant primary source is Lars Hormander, "Fourier integral operators. I", *Acta
Mathematica* 127 (1971), 79-183, DOI `10.1007/BF02392052`. That paper develops the calculus and
applications, but the metadata does not identify a numbered theorem. The paper is therefore a
candidate source family, not an H0 statement anchor.

## Crosswalk

| Metadata component | Source component to locate | Required Lean component | Intake status |
|---|---|---|---|
| "Fourier integral operator" | exact definition of phase, amplitude, order, and equivalence | concrete oscillatory-integral operator and well-definedness predicates | family located; exact definitions open |
| attributed to Hormander, 1971 | numbered theorem in the cited paper or a justified replacement source | exact declaration/expression with source revision | bibliographic candidate only |
| "solving hyperbolic equations" | specific parametrix or solution-operator theorem and its PDE hypotheses | operator equation, initial data, remainder, and regularity conclusion | exact claim open |
| canonical geometry | source canonical relation and nondegeneracy assumptions | typed cotangent/canonical-relation data | open |
| analytic conclusion | exact local/global and modulo-smoothing qualification | quantified spaces, orders, constants, and equality notion | open |

Later work must inspect an authoritative copy, record a stable file hash and page/theorem pinpoint,
check corrections/errata, and map every premise row by row. A modern monograph may clarify
definitions but cannot silently replace the primary theorem. No Lean declaration or proof-body
candidate is credited at intake, and no H0 or machine closure is claimed.
