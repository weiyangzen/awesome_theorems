# Scope map

## Included subject boundary

- Regular arithmetic surfaces: two-dimensional arithmetic schemes, typically fibred over the
  spectrum of the ring of integers of a number field, with the exact regularity, properness, and
  flatness hypotheses to be taken from the selected source theorem.
- Divisors equipped with archimedean/Green-function data and their intersection pairing.
- The finite-place algebraic intersection contribution together with the infinite-place analytic
  contribution, only in the normalization used by the selected source.
- A single theorem within this boundary, to be chosen and frozen during the statement phase.

## Statement decisions still open

The repository phrase is not proposition-shaped. Source inspection must select one numbered result
and freeze the base number field, surface hypotheses, divisor equivalence relation, Green-function
regularity, normalization, codomain, symmetry or bilinearity claims, and degenerate cases. It must
also distinguish an existence/well-definedness theorem from later consequences such as an
arithmetic Hodge index theorem or an adjunction formula.

## Explicit exclusions

- Treating the entire subject "Arakelov theory" as one theorem.
- Substituting the arithmetic Hodge index theorem, Faltings height, Arakelov--Zhang inequalities,
  or intersection theory on higher-dimensional arithmetic varieties without source evidence.
- An abstract Lean structure that assumes an intersection pairing as a field.
- Using the manifest's untrusted "verified" label as mathematical or machine-proof evidence.

The next phase must stop rather than elaborate a broadened or guessed target if source inspection
does not uniquely resolve the intended result.
