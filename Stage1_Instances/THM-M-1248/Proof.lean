import ObligationTree
import Mathlib.Analysis.Analytic.Uniqueness

/-!
# THM-M-1248 proof execution

This module closes the exact frozen Lean target. The statement's unqualified
`ContDiff Real top` order is analytic (`omega`), rather than smooth
(`infinity`). Thus compact support forces every admitted test function to be
zero. This proof is exact for the frozen proposition, but it exposes a
source-fidelity defect and is not evidence for the intended CKN theorem.
-/

namespace Stage1Instances.THM_M_1248

open MeasureTheory Set Filter

/-- The endpoint/interior split forced by the frozen bounds `0 <= a <= 1`. -/
theorem admissible_parameter_split
    {n : Nat} {p q r alpha beta gamma sigma a : Real}
    (hadm : AdmissibleParameters n p q r alpha beta gamma sigma a) :
    a = 0 ∨ a = 1 ∨ (0 < a ∧ a < 1) := by
  rcases hadm with ⟨_, _, _, _, ha0, ha1, _⟩
  rcases eq_or_lt_of_le ha0 with rfl | ha0
  · exact Or.inl rfl
  rcases eq_or_lt_of_le ha1 with rfl | ha1
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inr ⟨ha0, ha1⟩)

/-- At the `a = 0` endpoint, admissibility forces the target and lower-order
weights and exponents to agree. -/
theorem admissible_a_zero_forces_lower_order_parameters
    {n : Nat} {p q r alpha beta gamma sigma : Real}
    (hadm : AdmissibleParameters n p q r alpha beta gamma sigma 0) :
    gamma = beta /\ r = q := by
  rcases hadm with
    ⟨_, _, _, _, _, _, _, _, _, hgamma, hscale, _, _⟩
  norm_num at hgamma hscale
  subst gamma
  have hrqInv : r⁻¹ = q⁻¹ := by
    linarith [hscale]
  exact ⟨rfl, inv_injective hrqInv⟩

/-- The exact Caffarelli-Kohn-Nirenberg estimate at the lower-order endpoint
`a = 0`.  Here the admissibility equations reduce the estimate to reflexivity,
with constant `C = 1`. -/
theorem caffarelliKohnNirenberg_a_zero
    {n : Nat} {p q r alpha beta gamma sigma : Real}
    (hadm : AdmissibleParameters n p q r alpha beta gamma sigma 0) :
    ∃ C : Real, 0 < C ∧
      ∀ u : EuclideanSpace Real (Fin n) -> Real,
        ContDiff Real ⊤ u -> HasCompactSupport u ->
        weightedLp r gamma u ≤
          C * (weightedDerivativeLp p alpha u) ^ (0 : Real) *
            (weightedLp q beta u) ^ (1 - (0 : Real)) := by
  obtain ⟨hgamma, hrq⟩ :=
    admissible_a_zero_forces_lower_order_parameters hadm
  subst gamma
  subst r
  refine ⟨1, by norm_num, ?_⟩
  intro u _ _
  simp

/-- A compactly supported function admitted by the frozen statement is zero.
The critical point is that its unqualified `top` differentiability order
elaborates to the analytic order `omega`. -/
theorem compactlySupported_analytic_eq_zero
    {n : Nat} (hn : 0 < n)
    (u : EuclideanSpace Real (Fin n) -> Real)
    (hu : ContDiff Real ⊤ u) (hcomp : HasCompactSupport u) :
    u = 0 := by
  letI : Nonempty (Fin n) := ⟨⟨0, hn⟩⟩
  letI : NoncompactSpace (EuclideanSpace Real (Fin n)) :=
    RealNormedSpace.noncompactSpace _
  have hproper : tsupport u ≠ Set.univ := hcomp.ne_univ
  obtain ⟨z, hz⟩ := (Set.ne_univ_iff_exists_notMem (tsupport u)).mp hproper
  exact (hu.analyticOnNhd (s := Set.univ)).eq_of_eventuallyEq
    analyticOnNhd_const (notMem_tsupport_iff_eventuallyEq.mp hz)

/-- A premise-free proof of the exact frozen Lean target. It is vacuous with
respect to nonzero test functions because the statement accidentally requires
analytic compactly supported functions. -/
theorem caffarelliKohnNirenbergTarget : CaffarelliKohnNirenbergTarget := by
  intro n p q r alpha beta gamma sigma a hadm
  have hn := hadm.1
  have hr := hadm.2.2.2.1
  refine ⟨1, by norm_num, ?_⟩
  intro u hu hcomp
  have hu0 : u = 0 := compactlySupported_analytic_eq_zero hn u hu hcomp
  subst u
  have hlhs : weightedLp r gamma
      (0 : EuclideanSpace Real (Fin n) -> Real) = 0 := by
    simp [weightedLp, Real.zero_rpow hr.ne', inv_ne_zero hr.ne']
  rw [hlhs]
  exact mul_nonneg
    (mul_nonneg zero_le_one
      (Real.rpow_nonneg (by
        apply Real.rpow_nonneg
        apply integral_nonneg
        intro x
        exact Real.rpow_nonneg
          (mul_nonneg (Real.rpow_nonneg (norm_nonneg x) alpha) (norm_nonneg _)) p) a))
    (Real.rpow_nonneg (by
      apply Real.rpow_nonneg
      apply integral_nonneg
      intro x
      exact Real.rpow_nonneg
        (mul_nonneg (Real.rpow_nonneg (norm_nonneg x) beta) (abs_nonneg _)) q) (1 - a))

#print axioms admissible_parameter_split
#print axioms admissible_a_zero_forces_lower_order_parameters
#print axioms caffarelliKohnNirenberg_a_zero
#print axioms compactlySupported_analytic_eq_zero
#print axioms caffarelliKohnNirenbergTarget
#print sorries admissible_parameter_split
#print sorries admissible_a_zero_forces_lower_order_parameters
#print sorries caffarelliKohnNirenberg_a_zero
#print sorries compactlySupported_analytic_eq_zero
#print sorries caffarelliKohnNirenbergTarget

end Stage1Instances.THM_M_1248
