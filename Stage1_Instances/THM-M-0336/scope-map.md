# Scope map

## Included topic boundary

- Injective von Neumann factors, once injectivity and the algebra presentation are source-fixed.
- Source-required hypotheses such as separable predual or countable decomposability.
- The exact Murray-von Neumann/Connes type branch selected by the source.
- The hyperfinite or other canonical model used in the selected classification statement.
- Existence, isomorphism, and uniqueness clauses actually asserted by the selected source result.
- Modular-flow or discrete-decomposition invariants only where the selected classification branch
  requires them.

## Ambiguities to resolve at statement freeze

The repository record does not determine which of these materially different roots it intends:

1. Uniqueness/classification of injective factors of type `II_1`.
2. The package covering cases `II_1`, `II_infinity`, and `III_lambda` for `lambda != 1` associated
   with Connes' 1976 paper.
3. A later combined statement about amenable/injective factors with separable predual, including
   cases not closed by that 1976 paper alone.
4. An equivalence such as injective iff amenable or injective iff hyperfinite, rather than the
   classification/uniqueness conclusion itself.
5. A result about general injective von Neumann algebras assembled by central decomposition rather
   than a factor theorem.

The statement phase must select an immutable source result and freeze the algebra representation,
factor predicate, injectivity definition, separability/countability assumptions, type parameter
and its range, canonical model, isomorphism notion, quantifier order, and all existence and
uniqueness clauses. It must explicitly handle the exceptional type-III parameters, non-factors,
the zero algebra, and nonseparable settings.

## Explicit exclusions

- Murray-von Neumann's general factor-type classification as a substitute.
- Connes' injective-factor/amenability equivalences as a substitute unless source selection shows
  that equivalence is the intended root.
- Later results that close additional type-III cases silently attributed to the 1976 source.
- Classification of arbitrary factors without the injectivity/amenability hypothesis.
- Classification of C-star algebras, subfactors, or their index values.
- Merely defining a predicate called `Injective` or assuming the desired isomorphism.
- The repository label `已验证` as proof or source-fidelity evidence.

No canonical Lean target is frozen at intake because the source record does not identify one exact
classification proposition.
