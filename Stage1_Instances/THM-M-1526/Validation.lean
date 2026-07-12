import Statement

/-!
# THM-M-1526 independent local validation probe

This module reconstructs the exact frozen target without importing the proof
or obligation-composition modules. It is a same-runner differential check, not
an independent release attestation.
-/

namespace Stage1Instances.THM_M_1526.Validation

open Stage1Instances.THM_M_1526

universe u

theorem independentPairedTerm
    {I : Type} {Psi : Type u}
    [Fintype I] [DecidableEq I] [AddCommGroup Psi] [Module Complex Psi]
    (D : FreeDiracData I Psi) (mu nu : I) :
    (D.gamma mu * D.deriv mu) * (D.gamma nu * D.deriv nu) +
        (D.gamma nu * D.deriv nu) * (D.gamma mu * D.deriv mu) =
      D.g mu nu • (D.deriv mu * D.deriv nu) +
        D.g nu mu • (D.deriv nu * D.deriv mu) := by
  have moveDerivatives (a b : I) :
      (D.gamma a * D.deriv a) * (D.gamma b * D.deriv b) =
        (D.gamma a * D.gamma b) * (D.deriv a * D.deriv b) := by
    rw [mul_assoc, ← mul_assoc (D.deriv a), ← D.gamma_deriv_commute b a]
    simp only [mul_assoc]
  rcases eq_or_ne mu nu with rfl | hne
  · rw [moveDerivatives, D.clifford_diagonal]
    simp
  · rw [moveDerivatives, moveDerivatives, D.deriv_commute nu mu]
    rw [← add_mul, D.clifford_offDiagonal mu nu (by simpa using hne)]
    rw [add_smul, add_mul]
    simp

theorem independentSlashSquare
    {I : Type} {Psi : Type u}
    [Fintype I] [DecidableEq I] [AddCommGroup Psi] [Module Complex Psi]
    (D : FreeDiracData I Psi) :
    slash D * slash D = kleinGordon D := by
  let lhs : SpinorOperator Psi := Finset.univ.sum fun mu =>
    Finset.univ.sum fun nu =>
      (D.gamma mu * D.deriv mu) * (D.gamma nu * D.deriv nu)
  let rhs : SpinorOperator Psi := Finset.univ.sum fun mu =>
    Finset.univ.sum fun nu => D.g mu nu • (D.deriv mu * D.deriv nu)
  have doubled : lhs + lhs = rhs + rhs := by
    dsimp [lhs, rhs]
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
    exact independentPairedTerm D mu nu
  have equal : lhs = rhs := by
    have scaled := congrArg
      (fun T : SpinorOperator Psi => (2 : Complex)⁻¹ • T) doubled
    simpa [smul_add, ← add_smul] using scaled
  rw [slash, Finset.sum_mul]
  simp only [Finset.mul_sum]
  exact equal

theorem independentFreeDiracFactorizationTarget :
    FreeDiracFactorizationTarget.{u} := by
  intro I Psi _ _ _ _ D
  have factorization :
      (slash D + D.mass • (1 : SpinorOperator Psi)) *
          (slash D - D.mass • (1 : SpinorOperator Psi)) =
        kleinGordon D - D.mass ^ 2 • (1 : SpinorOperator Psi) := by
    rw [sub_eq_add_neg]
    simp only [mul_add, add_mul]
    rw [independentSlashSquare]
    simp [pow_two, smul_smul, sub_eq_add_neg]
  refine ⟨factorization, ?_⟩
  intro psi killed
  rw [← factorization]
  change (slash D + D.mass • (1 : SpinorOperator Psi))
    ((slash D - D.mass • (1 : SpinorOperator Psi)) psi) = 0
  rw [killed]
  exact map_zero _

#print axioms independentPairedTerm
#print axioms independentSlashSquare
#print axioms independentFreeDiracFactorizationTarget

end Stage1Instances.THM_M_1526.Validation
