# Scope map

## Included theorem family

- Weak compactness in functional analysis, with the weak topology made explicit.
- The source-selected `L^1` family or source-selected bounded linear operator formulation.
- Uniform integrability, weak compactness, and every measure, boundedness, closure, or operator
  hypothesis actually used by the selected equivalence.
- Both directions only if the exact source states an equivalence.

## Decisions required at statement freeze

The statement phase must select and inspect one immutable source passage. It must freeze whether the
root concerns relatively weakly compact subsets of `L^1`, weak sequential compactness, or weakly
compact operators; real or complex scalars; the measure-space assumptions; the `L^1` construction;
the exact uniform-integrability convention; whether boundedness or closure is separate; domain and
codomain assumptions for an operator version; and whether compactness concerns an image, its weak
closure, the unit ball, sequences, or nets. Null measure, finite families, zero spaces, and the zero
operator must be treated explicitly.

## Explicit exclusions

- The Dunford-Pettis property of a Banach space as a substitute for the named theorem.
- The claim that weakly compact operators are completely continuous unless an exact source selects
  that formulation and supplies its domains and sequence/topology conventions.
- Ordinary norm-compact operators (`IsCompactOperator` with the norm topology) as a substitute for
  weak compactness.
- Uniform integrability alone, or a one-way supporting lemma, as the full equivalence.
- A finite-dimensional special case, a martingale convergence theorem, or Vitali convergence.
- A structure carrying the desired criterion as an assumed field.
- The repository label `已验证` as human-source or kernel evidence.

No canonical Lean target is frozen during intake. The checked APIs are only encoding ingredients.
