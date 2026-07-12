import ObligationTree

namespace Stage1Instances.THM_M_1526

universe u

theorem paired_term
    {I : Type} {Psi : Type u}
    [Fintype I] [DecidableEq I] [AddCommGroup Psi] [Module Complex Psi]
    (D : FreeDiracData I Psi) (mu nu : I) :
    (D.gamma mu * D.deriv mu) * (D.gamma nu * D.deriv nu) +
        (D.gamma nu * D.deriv nu) * (D.gamma mu * D.deriv mu) =
      D.g mu nu • (D.deriv mu * D.deriv nu) +
        D.g nu mu • (D.deriv nu * D.deriv mu) := by
  have reorder (a b : I) :
      (D.gamma a * D.deriv a) * (D.gamma b * D.deriv b) =
        (D.gamma a * D.gamma b) * (D.deriv a * D.deriv b) := by
    rw [mul_assoc, ← mul_assoc (D.deriv a), ← D.gamma_deriv_commute b a]
    simp only [mul_assoc]
  by_cases h : mu = nu
  · subst nu
    rw [reorder]
    rw [D.clifford_diagonal]
    simp
  · rw [reorder, reorder]
    rw [D.deriv_commute nu mu]
    rw [← add_mul, D.clifford_offDiagonal mu nu (by simp [h])]
    rw [add_smul, add_mul]
    simp

theorem slash_square
    {I : Type} {Psi : Type u}
    [Fintype I] [DecidableEq I] [AddCommGroup Psi] [Module Complex Psi]
    (D : FreeDiracData I Psi) :
    slash D * slash D = kleinGordon D := by
  let A : SpinorOperator Psi := Finset.univ.sum fun mu =>
    Finset.univ.sum fun nu =>
      (D.gamma mu * D.deriv mu) * (D.gamma nu * D.deriv nu)
  let B : SpinorOperator Psi := Finset.univ.sum fun mu =>
    Finset.univ.sum fun nu => D.g mu nu • (D.deriv mu * D.deriv nu)
  have hpairs : A + A = B + B := by
    dsimp [A, B]
    conv_lhs =>
      rhs
      rw [Finset.sum_comm]
    conv_rhs =>
      rhs
      rw [Finset.sum_comm]
    simp only [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro mu _
    apply Finset.sum_congr rfl
    intro nu _
    exact paired_term D mu nu
  have hAB : A = B := by
    have h := congrArg (fun T : SpinorOperator Psi => (2 : Complex)⁻¹ • T) hpairs
    simpa [smul_add, ← add_smul] using h
  rw [slash, Finset.sum_mul]
  simp only [Finset.mul_sum]
  exact hAB

theorem freeDiracFactorization : FactorizationPackage.{u} := by
  intro I Psi _ _ _ _ D
  rw [sub_eq_add_neg]
  simp only [mul_add, add_mul]
  rw [slash_square]
  simp [pow_two, smul_smul, sub_eq_add_neg]

theorem freeDiracFactorizationTarget : FreeDiracFactorizationTarget.{u} :=
  root_of_factorization freeDiracFactorization

#print axioms paired_term
#print axioms slash_square
#print axioms freeDiracFactorization
#print axioms freeDiracFactorizationTarget

end Stage1Instances.THM_M_1526
