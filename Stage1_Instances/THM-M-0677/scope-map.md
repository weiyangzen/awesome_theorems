# Scope map

## Included topic boundary

- First-order structures and models of a theory.
- A source-specified minimality predicate on a model or structure.
- The exact property or characterization of such models named by the selected source.
- Any necessary hypotheses on the language, theory, cardinality, embeddings, or definability.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these materially different notions:

1. **Submodel minimality:** a model of `T` has no proper substructure that is also a model of `T`.
2. **Elementary minimality:** a model has no proper elementary substructure.
3. **Definability minimality:** every parameter-definable unary subset of the carrier is finite or
   cofinite (with conventions about parameters and finite carriers made explicit).
4. A theorem about existence, uniqueness, embeddings, cardinality, or another "property" of models
   satisfying one of those definitions.

The statement phase must inspect an immutable source and freeze one proposition, its ordered
binders, its exact notion of submodel or definability, and its conclusion. It must also decide empty
languages, finite carriers, empty or inconsistent theories, models without proper substructures,
and whether parameters are permitted.

## Explicit exclusions

- Prime models, atomic models, homogeneous models, and model companions as substitutes.
- Strong minimality as a substitute for minimality; quantification over elementary extensions or
  all elementarily equivalent structures changes the claim.
- The algebraic-geometry minimal model program or minimal models of arithmetic/set theory.
- A definition packaged as assumed data followed by a tautological projection.
- Any convenient theorem about substructures or definable sets absent a checked source crosswalk.
- The repository label `已验证` as evidence of a human or machine proof.

No canonical Lean target is frozen at intake because the source record does not identify one.
