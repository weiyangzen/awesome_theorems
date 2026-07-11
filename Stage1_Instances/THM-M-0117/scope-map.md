# Scope map

## Included root claim

- Domain: compact complex manifolds; the exact smoothness, connectedness, irreducibility, and dimension conventions remain to be recovered from a primary source.
- Hypothesis: the manifold is Moishezon, conventionally expressed by maximal algebraic dimension; its exact meromorphic-function-field definition must be frozen later.
- Conclusion: existence of a projective algebraic variety bimeromorphic to the analytic manifold.
- Comparison data: the eventual target must specify analytification and the precise bimeromorphic relation between analytic spaces; mere existence of an unrelated projective variety is insufficient.

## Decisions left to the statement node

- Resolve the primary-source wording and whether “Moishezon theorem” here denotes the bimeromorphic algebraic-model theorem or a projectivity theorem with an additional Kähler hypothesis.
- Select exact Lean representations of complex manifolds/analytic spaces, meromorphic functions, algebraic dimension, projective varieties, analytification, and bimeromorphisms.
- Freeze ordered binders, universes, typeclass hypotheses, minimal imports, environment fingerprint, and foundation/TCB profiles.
- Cover dimension-zero, empty/nonempty, disconnected, singular-versus-manifold, and reducible boundary conventions.
- Mutation-test compactness, maximal algebraic dimension, projectivity, and the direction and strength of the comparison relation.

## Explicit exclusions

- “Moishezon plus Kähler implies projective” as a silent substitute for the frozen root.
- Kodaira embedding, Chow's theorem, GAGA, or algebraic reduction alone as the root theorem.
- A scheme-side projectivity/properness wrapper lacking the analytic-to-algebraic comparison.
- The legacy `S1_M_037.lean` predicate shapes and metadata as accepted rev-5.6 statement or proof evidence.

These boundaries prevent a nearby projectivity theorem or a checkable algebraic special case from replacing the requested algebraicity claim.
