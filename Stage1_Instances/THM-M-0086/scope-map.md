# Scope map

## Included claim branches

- Embedding branch: a small abelian category and a full, faithful, exact functor into a category of
  modules over a ring. The statement phase must fix the exact smallness convention, universes,
  handedness of modules, and whether exactness is encoded directly or by preservation of finite
  limits and finite colimits.
- Injective branch: a complete abelian category with enough injectives and a separator/generator
  has an injective coseparator/cogenerator.
- Dual branch: a cocomplete abelian category with enough projectives and a
  coseparator/cogenerator has a projective separator/generator.

## Boundary decisions

Primary-source inspection must decide whether the last two branches genuinely belong to the named
repository theorem. It must also freeze local smallness versus universe-smallness, ring versus
small preadditive target, left/right module convention, exactness language, binder order, and all
completeness assumptions. Degenerate categories are not silently excluded.

## Explicit exclusions

- The general adjoint functor theorem, Freyd's incompleteness theorem, or the special adjoint
  functor theorem as a substitute.
- A faithful but not full or exact representation.
- A generator result with completeness, enough-injective/projective, or separator assumptions
  removed.
- Treating the existing wrapper or a mathlib theorem name as source fidelity or rev-5.6 acceptance.

The statement phase may formalize a conjunction only after source audit justifies the package;
otherwise it must preserve distinct typed roots and record their relation to the repository label.
