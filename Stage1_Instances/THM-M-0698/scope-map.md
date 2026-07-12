# Scope map

## Included claim

- Arbitrary many-sorted first-order languages and theories of closed formulas.
- Semantic satisfiability by a nonempty structure modeling every sentence in the theory.
- Finite satisfiability quantified over every finite set of sentences contained in the theory.
- Both implications: restriction of a model proves the easy direction; compactness supplies a model
  from the finite-subtheory hypothesis.

## Binder and representation decisions

The intended mathematical binders are `L`, then `T`, with no countability, finiteness, consistency,
cardinality, or syntactic-derivability hypothesis. The pinned candidate uses mathlib's
`FirstOrder.Language`, `Language.Theory` (sets of sentences), `Theory.IsSatisfiable`, and
`Theory.IsFinitelySatisfiable`. Its satisfiability definition requires a nonempty model. The formal
statement phase must freeze the precise universe parameters, implicit binders, normalized kernel
expression, imports, and logical profile rather than relying on this prose rendering.

## Boundary cases

- The empty theory and the empty finite subtheory are included.
- A finite theory is included; choosing the whole theory recovers its satisfiability.
- Languages may have empty function or relation symbol families.
- Empty carrier structures are excluded by the nonempty-model convention.
- No fixed carrier cardinality is asserted.

## Explicit exclusions

- Propositional compactness, topological compactness, compactness of a proof calculus, or weak
  compactness of cardinals as substitutes.
- The consequence form alone (`T models phi` iff a finite subtheory models `phi`) unless connected
  to the canonical satisfiability form by a checked transport.
- Only the hard implication, or a countable/finite-language specialization, as the whole theorem.
- Syntactic consistency in place of finite semantic satisfiability without a checked completeness
  bridge and exact source crosswalk.
- An abstract hypothesis that already supplies compactness, a bodyless declaration, or an assumed
  model packaged as input.
- The inventory label `已验证` or the existence of a mathlib theorem name as acceptance evidence.

