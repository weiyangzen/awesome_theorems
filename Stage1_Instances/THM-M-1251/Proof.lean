import Mathlib.Analysis.Distribution.TemperedDistribution

/-!
# THM-M-1251 proof implementation

The selected statement uses mathlib's pointwise-convergence continuous dual.
Consequently its proof is the definitional expansion of the pinned
`TemperedDistribution` abbreviation; no analytic representation theorem or
strong-dual identification is needed.
-/

noncomputable section

open scoped SchwartzMap

universe u

namespace Stage1Instances.THM_M_1251.Proof

/-- The exact canonical proposition from `Statement.lean`. -/
def CanonicalTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E]
    [FiniteDimensional Real E],
      TemperedDistribution E Complex =
        (SchwartzMap E Complex →Lₚₜ[Complex] Complex)

/-- The pinned mathlib definition expands to the selected pointwise dual.
This is the unique terminal proof body for the machine proof route. -/
theorem importedDefinitionExpansion : CanonicalTarget.{u} := by
  intro E _ _ _
  rfl

/-- Exact root closure, kept separate to expose the frozen child-to-parent
composition boundary without duplicating proof credit. -/
theorem temperedDistributionsAreSchwartzDual : CanonicalTarget.{u} :=
  importedDefinitionExpansion

end Stage1Instances.THM_M_1251.Proof

#print axioms Stage1Instances.THM_M_1251.Proof.importedDefinitionExpansion
#print axioms Stage1Instances.THM_M_1251.Proof.temperedDistributionsAreSchwartzDual
