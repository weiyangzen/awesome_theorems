# Source-statement crosswalk

## Candidate primary source

Jonathan Pila and Alex Wilkie, "The rational points of a definable set," *Duke Mathematical
Journal* **133** (2006), no. 3, 591-616, DOI `10.1215/S0012-7094-06-13336-7`. This is the primary
paper associated with the named theorem. A stable scan must still be inspected to record the exact
theorem number, pages, wording, referenced definitions, and errata before the claim is frozen.

This bibliographic record is a discovery anchor, not an immutable receipt and not an `H0` claim.

## Crosswalk

| Metadata/source component | Mathematical role | Required Lean object | Intake disposition |
|---|---|---|---|
| o-minimal expansion of the real field | controls definable sets and tame geometry | language/structure, real-field expansion, o-minimality, parameter policy | included; exact binders open |
| definable `X` in affine `n`-space | set whose rational points are counted | definable subset of `Fin n -> Real` (or source-faithful equivalent) | included; encoding open |
| `X_alg` | union of connected positive-dimensional semialgebraic subsets | semialgebraic connectedness, dimension, union construction | included; definition must be copied exactly |
| rational points of height at most `T` | finite counting set | rational embedding, height, finite set/cardinality | included; convention open |
| for every positive `epsilon` | subpolynomial exponent | positive real exponent and ordered quantifier | included; domain open |
| constant depending on `X` and `epsilon` | uniformity boundary | explicit existential constant before the height quantifier | included; exact dependencies open |
| `N(X - X_alg,T) <= c T^epsilon` | root conclusion | numeric count and real-power inequality | intended root; threshold/inequality open |

## Existing Lean discovery boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_087.lean` provides useful names for rational
points and lists missing API families. It explicitly says its `StatementShape` is not terminal.
More importantly, `PilaWilkieArityBoundary.subpolynomialBound` is an arbitrary predicate supplied
by the existential boundary package, so the declaration does not encode the quantitative source
conclusion. It receives no exact-statement or proof credit under rev-5.6.

Before `H0`, reviewers must record a pinpoint stable source, map all referenced definitions and
assumptions, check published corrections/errata, reconstruct the human proof node-by-node, and
independently approve the crosswalk.
