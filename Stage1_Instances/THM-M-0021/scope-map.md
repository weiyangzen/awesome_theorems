# Scope map

## Preserved theorem family

The repository phrase preserves only the following family-level content:

- the varying objects are algebraic number fields;
- the subject is asymptotic behavior involving their class numbers; and
- the historical label is the Brauer-Siegel theorem.

A common modern formulation studies the logarithm of the product of the class number and regulator
relative to a logarithmic discriminant scale along a family of number fields. This is a scope
locator only. It is not adopted as the canonical statement, because neither that product nor the
necessary family hypotheses occur in the repository source.

## Decisions required at statement freeze

The dependent statement phase must select an immutable authoritative passage and freeze all of the
following proposition-changing choices:

1. Whether the theorem quantifies over an explicit sequence, a directed family, or an arbitrary
   family of number fields satisfying an asymptotic predicate.
2. The number-field carrier and isomorphism convention, and whether fields must be normal, Galois,
   or satisfy another restriction.
3. Whether degrees are fixed, bounded, or allowed to grow, and the exact degree-versus-discriminant
   hypothesis.
4. The discriminant invariant, absolute value, square-root or root-discriminant normalization, and
   the proof that every logarithmic denominator is defined and eventually nonzero.
5. Whether the numerator is the class number alone, the product of class number and regulator, a
   logarithm of that product, or a source-defined equivalent expression.
6. Whether the conclusion is a limit, asymptotic equivalence, pair of bounds, or another quantified
   estimate, including the codomain, coercions, filter, and normalization.
7. All boundary cases: the rational field, repeated or isomorphic fields, bounded discriminant,
   degree one, empty or finite families, and zero/one values before logarithms.
8. The exact ordered binders, hypotheses, conclusion, alternate encodings, logical principles, and
   checked transports between any credited variants.

## Explicit exclusions

- A fixed-field class-number formula, class-number finiteness, or positivity result as a substitute
  for an asymptotic theorem over varying fields.
- Asymptotic counting of ideals of bounded norm in one fixed number field. Pinned mathlib's
  `NumberField.Ideal.tendsto_norm_le_div_atTop` is of this kind and is not Brauer-Siegel.
- Dirichlet's analytic class-number formula by itself, even though it exposes class number,
  regulator, and discriminant ingredients.
- A special family such as quadratic, cyclotomic, CM, normal, or fixed-degree fields unless the
  selected source makes that exact family canonical or a checked transport is supplied.
- A statement assuming the desired limiting relation, bounds, or asymptotic equivalence as a
  hypothesis or structure field.
- An estimate for class number alone if the source theorem controls the class-number/regulator
  product, or conversely.
- The catalog label `已验证`, the duplicated inventory entry, adjacent API availability, or a
  bounded name search as source, statement, or proof evidence.

No canonical Lean proposition is frozen at intake. Later formalization must expose the actual
family, growth predicate, invariants, logarithms, and filter rather than weakening or broadening the
source-selected theorem.
