import Statement
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Topology.Order.Compact

/-!
# THM-M-1271 differential validation probes

This module imports only the frozen statement. It independently reconstructs
the geometric barrier and the conditional analytic-to-root adapter already
present in the proof phase. The Palais-Smale sequence construction remains an
explicit premise, so this module is not a proof of the mountain-pass target.

These declarations are same-workspace differential evidence, not the distinct
independent-runner attestation required for release.
-/

namespace Stage1Instances.THM_M_1271.Validation

open Filter Set

universe u

variable {X : Type u} [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X]

omit [NormedSpace ℝ X] [CompleteSpace X] in
/-- Direct reconstruction of the sphere-crossing argument from the frozen path
predicate, without importing the proof implementation. -/
theorem directAdmissiblePath_meets_sphere {e : X} {rho : ℝ} {gamma : ℝ → X}
    (hgamma : IsAdmissiblePath e gamma) (hrho : 0 < rho) (he : rho < ‖e‖) :
    ∃ t ∈ Icc (0 : ℝ) 1, ‖gamma t‖ = rho := by
  have hnorm : ContinuousOn (fun t : ℝ ↦ ‖gamma t‖) (Icc 0 1) :=
    continuous_norm.comp_continuousOn hgamma.1
  have hrange := intermediate_value_Icc (show (0 : ℝ) ≤ 1 by norm_num) hnorm
  have hrho_mem : rho ∈ Icc (‖gamma 0‖) (‖gamma 1‖) := by
    rw [hgamma.2.1, hgamma.2.2, norm_zero]
    exact ⟨hrho.le, he.le⟩
  rcases hrange hrho_mem with ⟨t, ht, hteq⟩
  exact ⟨t, ht, hteq⟩

omit [CompleteSpace X] in
/-- Direct reconstruction of the lower bound for a single admissible path. -/
theorem directAlpha_le_pathHeight {Phi : X → ℝ} {rho alpha : ℝ} {e : X}
    {gamma : ℝ → X} (hC1 : ContDiff ℝ 1 Phi)
    (hgamma : IsAdmissiblePath e gamma) (hrho : 0 < rho) (he : rho < ‖e‖)
    (hsphere : ∀ x : X, ‖x‖ = rho → alpha ≤ Phi x) :
    alpha ≤ PathHeight Phi gamma := by
  obtain ⟨t, ht, ht_norm⟩ := directAdmissiblePath_meets_sphere hgamma hrho he
  have hmem : Phi (gamma t) ∈ {r : ℝ | ∃ s ∈ Icc (0 : ℝ) 1, r = Phi (gamma s)} :=
    ⟨t, ht, rfl⟩
  have hcompact : IsCompact (Phi '' (gamma '' Icc (0 : ℝ) 1)) :=
    ((isCompact_Icc.image_of_continuousOn hgamma.1).image_of_continuousOn
      hC1.continuous.continuousOn)
  have hbdd : BddAbove {r : ℝ | ∃ s ∈ Icc (0 : ℝ) 1, r = Phi (gamma s)} := by
    have heq : {r : ℝ | ∃ s ∈ Icc (0 : ℝ) 1, r = Phi (gamma s)} =
        Phi '' (gamma '' Icc (0 : ℝ) 1) := by
      ext r
      constructor
      · rintro ⟨s, hs, rfl⟩
        exact ⟨gamma s, ⟨s, hs, rfl⟩, rfl⟩
      · rintro ⟨x, ⟨s, hs, rfl⟩, rfl⟩
        exact ⟨s, hs, rfl⟩
    rw [heq]
    exact hcompact.bddAbove
  exact (hsphere (gamma t) ht_norm).trans (le_csSup hbdd hmem)

/-- Direct geometric barrier at the exact frozen minimax level. -/
theorem directAlpha_le_mountainPassLevel {Phi : X → ℝ} {rho alpha : ℝ} {e : X}
    (hC1 : ContDiff ℝ 1 Phi) (hrho : 0 < rho)
    (hsphere : ∀ x : X, ‖x‖ = rho → alpha ≤ Phi x) (he : rho < ‖e‖) :
    alpha ≤ MountainPassLevel Phi e := by
  have hline : IsAdmissiblePath e (fun t : ℝ ↦ t • e) := by
    refine ⟨(continuous_id.smul continuous_const).continuousOn, ?_, ?_⟩
    · simp
    · simp
  rw [MountainPassLevel]
  apply le_csInf
  · exact ⟨PathHeight Phi (fun t : ℝ ↦ t • e), (fun t : ℝ ↦ t • e), hline, rfl⟩
  · rintro c ⟨gamma, hgamma, rfl⟩
    exact directAlpha_le_pathHeight hC1 hgamma hrho he hsphere

/-- Independent check of the final adapter. The analytic critical-point
package is deliberately retained as an exact premise. -/
theorem directConditionalRoot
    (critical : ∀ (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X]
      [CompleteSpace X] (Phi : X → ℝ) (rho alpha : ℝ) (e : X),
      ContDiff ℝ 1 Phi → PalaisSmale Phi → Phi 0 = 0 → 0 < rho → 0 < alpha →
      (∀ x : X, ‖x‖ = rho → alpha ≤ Phi x) → rho < ‖e‖ → Phi e ≤ 0 →
      ∃ x : X, fderiv ℝ Phi x = 0 ∧ Phi x = MountainPassLevel Phi e) :
    MountainPassTarget.{u} := by
  intro X _group _space _complete Phi rho alpha e hC1 hPS hzero hrho halpha
    hsphere he hout
  obtain ⟨x, hxcrit, hxvalue⟩ :=
    critical X Phi rho alpha e hC1 hPS hzero hrho halpha hsphere he hout
  exact ⟨x, hxcrit, hxvalue, directAlpha_le_mountainPassLevel hC1 hrho hsphere he⟩

#print axioms directAdmissiblePath_meets_sphere
#print axioms directAlpha_le_pathHeight
#print axioms directAlpha_le_mountainPassLevel
#print axioms directConditionalRoot

end Stage1Instances.THM_M_1271.Validation
