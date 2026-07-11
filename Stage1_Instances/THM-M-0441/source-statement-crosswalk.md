# Source-statement crosswalk

## Candidate primary source

Jonathan Pila and Alex Wilkie, "The rational points of a definable set," *Duke Mathematical
Journal* **133** (2006), no. 3, 591-616, DOI `10.1215/S0012-7094-06-13336-7`. This is the primary
paper associated with the named theorem. The MIMS repository copy, dated 2005-10-10, was inspected
at SHA-256 `81071938707150caedbcc640cdd426ca8f2ca98bc016aac2dde054d9d45f4d2f`.
The frozen root is Theorem 1.8 (first version), using Definitions 1.3 and 1.5.

This pinpoint supports statement selection but is not an `H0` proof/source-audit claim; errata,
proof-node reconstruction, and independent source review remain downstream.

## Crosswalk

| Metadata/source component | Mathematical role | Required Lean object | Intake disposition |
|---|---|---|---|
| o-minimal expansion of the real field | controls definable sets and tame geometry | `IsOMinimalExpansion L`: contains ring-definable sets and unary definable sets have finite frontier | frozen and elaborated |
| definable `X` in affine `n`-space | set whose rational points are counted | `(Set.univ : Set Real).Definable L X` | frozen and elaborated |
| `X_alg` | union of connected positive-dimensional semialgebraic subsets | `algebraicPart X`; positive dimension encoded by nontriviality for connected semialgebraic sets | frozen and elaborated |
| rational points of height at most `T` | finite counting set | `max |num| den` coordinate height and `Set.ncard` after explicit finiteness | Definition 1.3 frozen |
| for every positive `epsilon` | subpolynomial exponent | `epsilon : Real`, `0 < epsilon` | frozen |
| constant depending on `X` and `epsilon` | uniformity boundary | `exists c : Real, 0 < c`, inside `X, epsilon` and before `T` | frozen |
| `N(X - X_alg,T) <= c T^epsilon` | root conclusion | finite slice and real-power inequality for every natural `T >= 1` | Theorem 1.8 frozen |

## Existing Lean discovery boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_087.lean` provides useful names for rational
points and lists missing API families. It explicitly says its `StatementShape` is not terminal.
More importantly, `PilaWilkieArityBoundary.subpolynomialBound` is an arbitrary predicate supplied
by the existential boundary package, so the declaration does not encode the quantitative source
conclusion. It receives no exact-statement or proof credit under rev-5.6.

Before `H0`, reviewers must still check published corrections/errata, reconstruct the human proof
node-by-node, and independently approve this crosswalk.
