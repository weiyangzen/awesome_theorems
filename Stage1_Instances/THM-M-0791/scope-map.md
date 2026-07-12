# Scope map

## Included topic boundary

- A source-selected definition or characterization of a Woodin cardinal.
- The exact property, equivalence, existence statement, or consequence named by that source.
- The chosen set-theory foundation and representation of cardinals, ordinals, rank segments,
  subsets/functions, elementary embeddings, critical points, closure, and strongness/extenders.
- Every quantifier and restriction on ordinals, sets, functions, transitive models, and embeddings.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different possible targets:

1. a definition using functions on the cardinal and closure points with a suitable elementary
   embedding;
2. a definition using, for every subset of the cardinal, cardinals below it that are strong for
   that subset;
3. an equivalence between standard characterizations;
4. an existence, reflection, stationary-set, determinacy, or consistency-strength consequence.

The statement phase must locate an immutable source and freeze one proposition, ordered binders,
the exact Woodin convention, ambient theory, embedding domains/codomains, critical point and closure
requirements, and conclusion. It must also decide whether zero/small cardinals are ruled out by
hypothesis or definition, how universe levels encode proper-class language, whether embeddings are
sets or metatheoretic objects, and whether the claim is conditional on the existence of a Woodin
cardinal rather than asserting one exists.

## Explicit exclusions

- Measurable, strong, supercompact, huge, inaccessible, or other large cardinals as substitutes.
- A theorem merely about regular or inaccessible cardinals because mathlib has those APIs.
- Assuming a predicate named `IsWoodin` and returning the assumption or a definitional projection.
- An assertion that a Woodin cardinal exists unless the selected source statement asserts existence.
- Determinacy or inner-model consequences without their exact hypotheses and source crosswalk.
- Informal equivalence of characterizations without checked transports in the selected foundation.
- The repository label `已验证` as human-proof or machine-proof evidence.

No canonical Lean target is frozen at intake because the source record identifies no proposition.
