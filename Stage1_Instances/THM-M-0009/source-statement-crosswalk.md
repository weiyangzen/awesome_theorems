# Source-statement crosswalk

## Primary-source candidates

- Henri Cartan and Samuel Eilenberg, *Homological Algebra*, Princeton University Press, 1956,
  Chapter III (derived functors and their exact sequences). Exact section, theorem, pages,
  assumptions, and errata require inspection against a stable edition.
- Charles A. Weibel, *An Introduction to Homological Algebra*, Cambridge University Press, 1994,
  sections 2.4 and 2.5 on derived functors and long exact sequences. Exact theorem/page anchors and
  edition-dependent numbering require inspection.

These are discovery anchors, not H0 evidence receipts.

## Crosswalk

| Metadata component | Source-level ambiguity | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "Ext functor" | first or second variable; modules or an abelian category | variance, universes, category instances, and `HasExt` assumptions differ | unresolved |
| "long exact sequence" | indexed sequence versus repeating finite exact windows | root conclusion may be a complex exactness predicate or quantified window exactness | unresolved |
| no short exact sequence shown | source may apply one of the derived-functor LES theorems | ordered objects, maps, and `ShortExact` witness must be frozen | blocking statement |
| no boundary cases | degree zero and shift convention unspecified | `n + 1` versus `1 + n`, and the initial Hom terms, need explicit treatment | unresolved |

## Existing Lean discovery boundary

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_102.lean` imports
`Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences` and proposes a conjunction of
`Abelian.Ext.covariantSequence_exact` and `Abelian.Ext.contravariantSequence_exact`. This is strong
evidence that the target is expressible in the pinned ecosystem, but it does not determine that the
two-branch conjunction is faithful to the unnamed source statement. It receives no accepted proof
credit at intake.

Before H0, an independent reviewer must inspect an immutable source copy, record exact theorem and
page anchors, definitions, assumptions and errata, and approve a node-by-node source-to-Lean map.
