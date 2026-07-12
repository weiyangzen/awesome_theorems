# Scope map

## Included topic boundary

- A source-selected cardinal `kappa` and a precise rank-initial structure based on `V_kappa`.
- A source-selected formula hierarchy, normally indexed by finite `m` and `n`, with explicit
  first- and higher-order variable sorts.
- Reflection of truth with permitted parameters from `V_kappa` to some `V_alpha`, `alpha < kappa`.
- The exact property, implication, or characterization actually named by the selected source.

## Ambiguities to resolve at statement freeze

The repository record does not choose among these non-interchangeable targets:

1. `Pi^m_n`-indescribability for fixed `m` and `n`.
2. `Sigma^m_n`-indescribability or a convention under which it is paired with a Pi level.
3. Total indescribability, quantifying over a collection of complexity levels.
4. A characterization at a particular level, such as a weak-compactness/reflection equivalence,
   with all required cardinal hypotheses.
5. An existence, consistency-strength, stationary-set, ideal, or preservation theorem about
   indescribable cardinals rather than the reflection definition itself.

The statement phase must freeze the source's syntax convention, satisfaction relation, language,
parameters, ambient foundation, ordered binders, hypotheses, conclusion, and boundary cases. It
must also distinguish a proposition asserting that a supplied cardinal is indescribable from any
claim that such a cardinal exists.

## Explicit exclusions

- Inaccessible, Mahlo, weakly compact, Ramsey, or measurable cardinal facts as substitutes.
- A convenient theorem about `Cardinal.IsInaccessible`; it is only a nearby encoding ingredient.
- A definition packaged as assumed data followed by a tautological field projection.
- Conflating one fixed `Pi^m_n` level with total indescribability.
- Treating meta-level Lean propositions as an object-language satisfaction predicate without a
  checked semantics bridge.
- Treating the repository label `已验证` as human-source or kernel-proof evidence.

No canonical Lean target is frozen at intake because the source record identifies no proposition.
