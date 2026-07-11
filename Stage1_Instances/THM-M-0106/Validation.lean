import Statement
import Mathlib.RingTheory.NoetherNormalization

/-!
# THM-M-0106 independent validation probe

This module reconstructs the frozen target through the checked statement
transport.  It deliberately does not import or invoke `Proof.lean`.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

namespace Stage1Instances.THM_M_0106.Validation

universe u

/-- An independently written exact-target probe.  The proof first establishes
the historical affine-Spec encoding, then uses the statement module's checked
equivalence instead of repeating the proof-phase affine-space construction. -/
theorem noetherNormalization_independent_probe :
    NoetherNormalizationTarget.{u} := by
  apply target_iff_pinnedAffineSpecCandidateShape.mpr
  intro k R _ _ _ _ _
  obtain ⟨s, g, hg, hfinite⟩ := exists_finite_inj_algHom_of_fg k R
  refine ⟨s, g, hg, hfinite, ?_⟩
  rw [AlgebraicGeometry.IsFinite.SpecMap_iff]
  exact hfinite

#check noetherNormalization_independent_probe
#print axioms noetherNormalization_independent_probe

end Stage1Instances.THM_M_0106.Validation
