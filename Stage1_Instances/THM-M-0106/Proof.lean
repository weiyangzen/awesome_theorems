import Statement
import Mathlib.RingTheory.NoetherNormalization

/-!
# THM-M-0106 proof-phase body

This module pins mathlib's Noether-normalization theorem and supplies the
checked affine-space bridge required by the frozen target.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

namespace Stage1Instances.THM_M_0106

universe u

/-- The exact frozen Noether-normalization target, closed by the pinned
mathlib algebraic theorem and the standard affine `Spec` equivalence. -/
theorem noetherNormalization_proof : NoetherNormalizationTarget.{u} := by
  intro k R _ _ _ _ _
  obtain ⟨s, g, hg, hfinite⟩ := exists_finite_inj_algHom_of_fg k R
  refine ⟨s, g, hg, hfinite, affineSpaceMorphism g, ?_, ?_⟩
  · have hspec : IsFinite (Spec.map (CommRingCat.ofHom g.toRingHom)) := by
      rw [AlgebraicGeometry.IsFinite.SpecMap_iff]
      exact hfinite
    exact MorphismProperty.RespectsIso.postcomp (P := @IsFinite)
      (AlgebraicGeometry.AffineSpace.SpecIso (Fin s) (CommRingCat.of k)).inv
      (Spec.map (CommRingCat.ofHom g.toRingHom)) hspec
  · simp [affineSpaceMorphism]

#check noetherNormalization_proof
#print axioms noetherNormalization_proof

end Stage1Instances.THM_M_0106
