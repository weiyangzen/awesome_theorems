import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.Analysis.Normed.Module.FiniteDimension

/-!
# THM-M-0120 conditional obligation composition

This module checks the final logical assembly chosen by the frozen tree. All
substantive cone-theorem packages remain explicit premises.
-/

namespace Stage1Instances.THMM0120.ObligationTree

universe uN

/-- The four independent output packages for one fixed indexed family compose
to the same dependent existential/conjunction shape used by
`ConeTheoremData.Conclusion`. This supplies no geometric premise. -/
theorem conclusion_of_packages
    {N : Type uN} [NormedAddCommGroup N] [NormedSpace Real N]
    (moriCone : Set N) (canonicalPairing : N →ₗ[Real] Real)
    (ι : Type) (countable : Countable ι) (ray : ι → Set N)
    (RayPackage : ι → Prop) (InDecomposition : N → Prop)
    (Contraction : ι → Prop)
    (rayPackage : ∀ i, RayPackage i)
    (decomposition : ∀ z, z ∈ moriCone ↔ InDecomposition z)
    (localFiniteness : ∀ ε : Real, 0 < ε →
      {i | ∃ z ∈ ray i, ‖z‖ = 1 ∧ canonicalPairing z ≤ -ε}.Finite)
    (contractions : ∀ i, Contraction i) :
    ∃ (j : Type) (_ : Countable j) (selectedRay : j → Set N),
      (∀ i, RayPackage i) ∧
      (∀ z, z ∈ moriCone ↔ InDecomposition z) ∧
      (∀ ε : Real, 0 < ε →
        {i | ∃ z ∈ selectedRay i, ‖z‖ = 1 ∧ canonicalPairing z ≤ -ε}.Finite) ∧
      ∀ i, Contraction i := by
  exact ⟨ι, countable, ray, rayPackage, decomposition, localFiniteness, contractions⟩

#print axioms conclusion_of_packages

end Stage1Instances.THMM0120.ObligationTree
