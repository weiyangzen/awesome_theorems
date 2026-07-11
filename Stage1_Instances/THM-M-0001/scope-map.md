# Scope map

## Included mathematical claim

The metadata sentence `短正合列诱导长正合同调序列` is read narrowly as the standard homological
algebra theorem: a degreewise short exact sequence of chain complexes

`0 -> A -> B -> C -> 0`

induces connecting maps `H_n(C) -> H_(n-1)(A)`, and the induced homology maps and connecting maps
form an exact sequence continuing through every degree. Naturality of the connecting maps is part
of the conventional construction but must be separately represented if the selected source or
formal encoding includes it.

The intended Lean domain is homological complexes in an abelian category, with explicit universes,
index type, complex shape, short-complex object, short-exactness hypothesis, adjacent indices, and
the relevant homology objects and morphisms. The statement phase must decide whether the canonical
root is an indexed exact-sequence object, exactness of every consecutive triple, or a checked family
of finite windows. That encoding choice may not weaken the continuing long-sequence claim.

## Boundary cases to freeze

- Arbitrary abelian category versus modules in an abelian category.
- Homological versus cohomological grading, including the direction and sign of the connecting map.
- Bounded and unbounded complexes and endpoints, if the index shape has endpoints.
- Exactness as image-equals-kernel versus mathlib's categorical `ShortComplex.Exact` formulation.
- Whether naturality is in the root statement or a separate root-relevant obligation.

## Explicit exclusions

- A single six-term window presented as the entire unbounded long exact sequence without a checked
  universal quantifier or assembly argument.
- Only the zero-composition identities, without exactness at every consecutive term.
- A specialized group-(co)homology sequence substituted for the general chain-complex theorem.
- The derived-category triangle sequence unless a checked transport to the short-exact-complex claim
  is supplied.
- Legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_096.lean` as accepted rev-5.6 evidence.

The later statement phase owns the exact expression, minimal imports, environment fingerprint,
alternate transports, and required hypothesis/domain/binder/boundary mutations.
