# Source-statement crosswalk

| Claim component | Human source anchor | Lean target surface | Intake assessment |
|---|---|---|---|
| Abstract variational principle on a complete metric space | I. Ekeland, *On the variational principle*, Journal of Mathematical Analysis and Applications 47 (1974), 324-353, DOI `10.1016/0022-247X(74)90025-0` | Future canonical root declaration | Primary paper identified, but theorem/page wording, assumptions, and errata have not yet been checked against a fixed copy: `H1` |
| Lower semicontinuity, lower boundedness/properness, and approximate-minimizer premise | Same primary paper; exact numbered result and notation require source audit | Candidate predicates from mathlib topology and `EReal` APIs | Each assumption is in scope; no Lean spelling or semantic equivalence is credited |
| Witness improves the input and remains within the prescribed radius | Same primary result, under the chosen two-parameter convention | Existential witness with value and distance conjuncts | Intended content frozen; strictness, constants, and extended-real coercions remain statement-phase work |
| Strict perturbed-minimality inequality against every other point | Same primary result | Universal inequality involving `(epsilon / lambda) * dist v w` | Intended content frozen, but orientation and arithmetic codomain must be checked from the source |
| Real-valued and one-parameter variants | Standard later presentations; no secondary edition accepted yet | Possible checked specializations/transports | Discovery candidates only |
| Caristi-type formulation | Related variational/fixed-point theorem family | Possible theorem-family bridge | Not part of the exact root and not assumed equivalent without a checked transport |

The generated Stage1 prose says only “existence of approximate minimizers.” That phrase is too weak
to serve as the canonical theorem: it omits completeness, lower semicontinuity, lower boundedness or
properness, the input approximation, localization, and the strict perturbation inequality. This
intake therefore preserves the full conventional two-parameter theorem family while leaving exact
constant and codomain choices open rather than silently broadening or weakening the source result.

Primary-source discovery locator (not an immutable evidence receipt):

- <https://doi.org/10.1016/0022-247X(74)90025-0>

No `H0` claim is made. The source audit must obtain a fixed edition, record the numbered theorem and
page, map every premise and conclusion conjunct, check later corrections or errata, and receive an
independent review. The statement phase must then select the exact codomain, inspect available
mathlib declarations, elaborate the ordered binders, serialize the normalized expression, and test
mutations of completeness, lower semicontinuity, positivity, approximation, and strictness.
