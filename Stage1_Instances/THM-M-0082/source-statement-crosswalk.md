# Source-statement crosswalk

## Candidate primary sources

- Peter J. Freyd, *Abelian Categories: An Introduction to the Theory of Functors*, Harper & Row
  (1964). This is a historical primary monograph candidate for the general adjoint functor theorem;
  the exact theorem/page, hypotheses, and errata have not yet been inspected.
- Saunders Mac Lane, *Categories for the Working Mathematician*, second edition, Springer (1998),
  the adjoints chapter's adjoint-functor-theorem section. This is a stable modern source candidate,
  but its exact theorem/page and size conventions still require inspection.

These are discovery anchors, not `H0` evidence. Anchor audit must select a stable edition and record
a pinpoint statement, proof, assumptions, definitions, and errata.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "adjoint functor theorem" | Freyd's general existence theorem | right-adjoint predicate for `G` | included; exact encoding open |
| complete domain | limits used in the construction | `HasLimits` with explicit size | included; universes open |
| preserves limits | continuity hypothesis on `G` | `PreservesLimitsOfSize` | included; size match open |
| solution set | small weakly initial family in each comma category | `SolutionSetCondition` | included; definition audit open |
| right adjoint | existence of a left adjoint to `G` | `G.IsRightAdjoint` or exhibited `F ⊣ G` | included; canonical conclusion open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_135.lean` imports
`Mathlib.CategoryTheory.Adjunction.AdjointFunctorTheorems` and names
`isRightAdjoint_of_preservesLimits_of_solutionSetCondition`. This strongly identifies a candidate
formal target, but the legacy file is explicitly unaccepted by the manifest. Later phases must
inspect the pinned mathlib source and exact declaration type, elaborate a canonical target, check
the terminal body and axioms, and establish source fidelity. The legacy special-theorem and
homological wrappers do not broaden the included claim.

Before `H0`, an independent reviewer must approve the edition/theorem/page, terminology, every
assumption, size convention, proof boundary, errata search, and row-by-row source-to-Lean mapping.
