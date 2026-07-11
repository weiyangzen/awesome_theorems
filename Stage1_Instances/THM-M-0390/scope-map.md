# Scope map

## Included claim

The intended root is the positive-natural-number theorem
`x^p + 1 = y^q -> (x,p,y,q) = (2,3,3,2)`, under the four strict hypotheses
`1 < x`, `1 < y`, `1 < p`, and `1 < q`. Equivalently, `8` and `9` are the unique consecutive
nontrivial positive perfect powers, oriented from the smaller to the larger number.

The statement phase must freeze binder order, the `Nat` domain, exponentiation parsing, conjunction
association in the conclusion, and checked transports between the equation and pair formulations.
It must mutation-test removal of each strict bound, reversal of orientation, and the boundary values
zero and one.

## Degenerate cases

Allowing base `1` or exponent `1` makes the claim false or changes its meaning, so all four lower
bounds are essential. Natural numbers avoid signed-base duplicates; an integer formulation is not
interchangeable without absolute-value and parity conditions. The theorem concerns values that are
consecutive, not merely perfect-power representations of a preselected pair.

## Explicit exclusions

- Catalan numbers, Catalan generating functions, and polynomial Fermat-Catalan theorems.
- A witness-only theorem that merely checks `2^3 + 1 = 3^2`.
- Fixed exponent, bounded-search, or finite-grid special cases as the root theorem.
- Integer, rational, complex, or abstract-monoid generalizations.
- A formulation that assumes uniqueness or the desired tuple in a hypothesis.
- The legacy `S1_M_004.lean` declarations as accepted rev-5.6 evidence.

Human mathematical closure is known, but repo-local Lean closure is not accepted. The initial debt
classification is `formalization_debt`, subject to the later immutable upstream audit.
