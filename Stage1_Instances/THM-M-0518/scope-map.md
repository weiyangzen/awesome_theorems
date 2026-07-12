# Scope map

## Included claim

- Domain: elliptic curves over `Q`, represented only after choosing a faithful Lean object boundary.
- Hypothesis: global semistability, conventionally good or multiplicative reduction at every finite
  place; its precise model-independence and minimal-model formulation must follow the source audit.
- Conclusion: genuine modularity, with a weight-two modular form/newform and the exact level,
  conductor, coefficient, normalization, and compatibility relation required by the source.
- Isomorphism invariance and transport between an elliptic curve and a Weierstrass model.

## Decisions required at statement freeze

1. Choose mathlib's representation of elliptic curves over `Q` and state the required nonsingularity
   without confusing a proposition argument with the `IsElliptic` typeclass.
2. Define global semistability over all finite places. The local mathlib disjunction `HasGoodReduction
   R W` or `HasMultiplicativeReduction R W` is an ingredient, not the global hypothesis.
3. Select the exact meaning of "modular" used in Wiles's paper and encode every substantive field.
   A structure containing arbitrary compatibility propositions would make existence vacuous and is
   forbidden.
4. Freeze conductor/level conventions, normalized eigenform/newform conditions, coefficient field,
   L-series or Galois-representation compatibility, and all transports between equivalent forms.
5. Check source definitions, Theorem 0.4's dependencies, the companion Taylor-Wiles correction,
   and relevant errata before claiming `H0`.

## Explicit exclusions

- The later theorem that every elliptic curve over `Q` is modular.
- A modularity-lifting theorem for a Galois representation substituted for the stated elliptic-curve
  theorem; such results may become proof-tree bridges only after an exact crosswalk.
- Curves over arbitrary number fields or only a special conductor/residual branch.
- Local semistability at one DVR in place of semistability at every finite place.
- Equality of names, unconstrained witness fields, or a proposition assumed as a hypothesis.
- The repository labels `已验证` and `形式化状态: 已验证` as source or machine-proof evidence.
- Legacy `S1_M_049` statement-shape definitions as an accepted rev-5.6 target or proof.
