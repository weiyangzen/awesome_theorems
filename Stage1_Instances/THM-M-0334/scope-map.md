# Scope map

## Included topic boundary

- Von Neumann algebras in a source-specified abstract or concrete presentation.
- The projection comparison relation and finiteness/proper-infiniteness notions required by the
  selected source.
- Factors, their centers, and the exact type-I/type-II/type-III partition named by the source.
- Any source-required refinements such as `I_n`, `I_infinity`, `II_1`, or `II_infinity`.
- If explicitly selected, decomposition of a general von Neumann algebra into central type
  summands, including the precise existence and uniqueness statement.

## Ambiguities to resolve at statement freeze

The repository record does not determine which of these materially different roots it intends:

1. Every factor lies in exactly one of types I, II, and III, defined through its projections.
2. The refined classification of factors into `I_n`, `I_infinity`, `II_1`, `II_infinity`, and III.
3. A central decomposition theorem for arbitrary von Neumann algebras into type summands or factors.
4. A historical package containing definitions and several classification results rather than one
   proposition.

The statement phase must pin a source passage and freeze the algebra presentation, factor
hypothesis, projection-equivalence definition, exact type predicates, quantifier order,
exhaustiveness/exclusivity or decomposition conclusion, and all separability or sigma-finiteness
assumptions. It must also decide the zero algebra, zero Hilbert space, finite-dimensional factors,
and whether isomorphism, spatial equivalence, or central decomposition equivalence is intended.

## Explicit exclusions

- Connes' classification of injective/amenable factors as a substitute.
- Classification of type-III factors by modular invariants as a substitute.
- Classification of finite-dimensional C-star algebras, AW-star algebras, or general operator
  algebras as a substitute.
- The von Neumann bicommutant theorem, despite its nearby subject matter.
- Merely defining type predicates and proving a tautological disjunction from an assumed type tag.
- The repository label `已验证` as proof or source-fidelity evidence.

No canonical Lean target is frozen at intake because the source record does not identify one exact
classification proposition.
