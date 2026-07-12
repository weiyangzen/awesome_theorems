# Scope map

## Included topic boundary

- First-order languages, structures, theories, and models.
- Cardinality existence or comparison for models, structures, elementary substructures, or
  elementary extensions, once an exact source chooses among them.
- All language-cardinality, infinitude, nonemptiness, containment, and cardinal-bound hypotheses
  required by that chosen statement.
- The exact elementary relationship and cardinal equality or inequality in the conclusion.

## Ambiguities to resolve at statement freeze

The literal phrase "cardinality of infinite models" is compatible with materially different claims:

1. Upward Loewenheim-Skolem: an infinite structure has an elementary extension of a specified
   larger cardinality, subject to language and model bounds.
2. Downward Loewenheim-Skolem: a structure has a smaller elementary substructure containing a
   specified set, subject to lower and upper cardinal bounds.
3. A combined theorem selecting an elementary embedding direction for every admissible infinite
   cardinal.
4. Existence of an elementarily equivalent structure, or existence of a model of the same theory,
   of a specified cardinality.
5. Only an arbitrarily-large-model consequence, which is weaker than exact cardinal equality.

The statement phase must use an immutable source to freeze one of these, its ordered binders,
universe lifts, hypotheses, exact conclusion, and boundary cases.

## Explicit exclusions

- Treating adjacent repository targets `THM-M-0646`, `THM-M-0647`, or `THM-M-0648` as the source
  statement for this target.
- Replacing elementary equivalence by isomorphism, mere equicardinality, or satisfaction of an
  unrelated theory.
- Dropping bounds involving `aleph_0`, the language cardinality, the source model, or a contained
  parameter set.
- Substituting compactness, completeness, categoricity, or the Skolem paradox.
- Crediting the inventory label `已验证`, a `#check`, or an imported theorem name as proof evidence.

No canonical Lean target is frozen at intake because the source record does not identify one.

