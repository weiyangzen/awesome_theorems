import «Stage1_Instances».«THM-M-1524».ObligationTree

/-!
# THM-M-1524 proof

This module closes the frozen Robertson and CCR components for the explicit
unbounded-observable interface in `Statement.lean`.
-/

noncomputable section

open scoped ComplexConjugate

namespace Stage1Instances.THM_M_1524

universe u

namespace Observable

variable {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

private theorem expectation_conj_eq (A : Observable H) (ψ : H)
    (hψ : ψ ∈ A.domain) (hA : A.IsSymmetric) :
    conj (A.expectation ψ hψ) = A.expectation ψ hψ := by
  unfold expectation
  calc
    conj (inner ℂ (A.apply ψ hψ) ψ) = inner ℂ ψ (A.apply ψ hψ) :=
      inner_conj_symm _ _
    _ = inner ℂ (A.apply ψ hψ) ψ := (hA ψ ψ hψ hψ).symm

private theorem centered_commutator_identity (A B : Observable H) (ψ : H)
    (hAψ : ψ ∈ A.domain) (hBψ : ψ ∈ B.domain)
    (hAB : B.apply ψ hBψ ∈ A.domain) (hBA : A.apply ψ hAψ ∈ B.domain)
    (hA : A.IsSymmetric) (hB : B.IsSymmetric) (hnorm : ‖ψ‖ = 1) :
    inner ℂ (A.commutatorApply B ψ hAψ hBψ hAB hBA) ψ =
      inner ℂ (B.apply ψ hBψ - B.expectation ψ hBψ • ψ)
          (A.apply ψ hAψ - A.expectation ψ hAψ • ψ) -
        inner ℂ (A.apply ψ hAψ - A.expectation ψ hAψ • ψ)
          (B.apply ψ hBψ - B.expectation ψ hBψ • ψ) := by
  have hψψ : inner ℂ ψ ψ = 1 := by
    rw [inner_self_eq_norm_sq_to_K, hnorm]
    norm_num
  have hAe := expectation_conj_eq A ψ hAψ hA
  have hBe := expectation_conj_eq B ψ hBψ hB
  have hAsymm := hA ψ ψ hAψ hAψ
  have hBsymm := hB ψ ψ hBψ hBψ
  rw [commutatorApply, inner_sub_left]
  rw [hA (B.apply ψ hBψ) ψ hAB hAψ, hB (A.apply ψ hAψ) ψ hBA hBψ]
  simp only [inner_sub_left, inner_sub_right, inner_smul_left, inner_smul_right]
  simp only [expectation] at hAe hBe ⊢
  rw [hψψ]
  simp only [mul_one]
  rw [hAe, hBe]
  rw [← hAsymm, ← hBsymm]
  ring

theorem robertson : RobertsonTarget.{u} := by
  intro H _ _ A B ψ hA hB hAB hBA hAself hBself hnorm
  let x := A.apply ψ hA - A.expectation ψ hA • ψ
  let y := B.apply ψ hB - B.expectation ψ hB • ψ
  have hid : inner ℂ (A.commutatorApply B ψ hA hB hAB hBA) ψ =
      inner ℂ y x - inner ℂ x y :=
    centered_commutator_identity A B ψ hA hB hAB hBA hAself.1 hBself.1 hnorm
  calc
    ‖inner ℂ (A.commutatorApply B ψ hA hB hAB hBA) ψ‖ / 2
        = ‖inner ℂ y x - inner ℂ x y‖ / 2 := by rw [hid]
    _ ≤ (‖inner ℂ y x‖ + ‖inner ℂ x y‖) / 2 :=
      div_le_div_of_nonneg_right (norm_sub_le _ _) (by norm_num)
    _ = ‖inner ℂ x y‖ := by
      rw [norm_inner_symm]
      ring
    _ ≤ ‖x‖ * ‖y‖ := norm_inner_le_norm x y
    _ = A.deviation ψ hA * B.deviation ψ hB := rfl

theorem heisenbergCCR (hrobertson : RobertsonTarget.{u}) : HeisenbergCCRTarget.{u} := by
  intro H _ _ Q P ψ hbar hQ hP hQP hPQ hQself hPself hhbar hnorm hCCR
  have hr := hrobertson H Q P ψ hQ hP hQP hPQ hQself hPself hnorm
  rw [hCCR ψ hQ hP hQP hPQ] at hr
  simpa [inner_smul_left, hnorm, abs_of_nonneg hhbar] using hr

end Observable

/-- Exact kernel-checked closure of the frozen two-component target. -/
theorem heisenberg_uncertainty : HeisenbergUncertaintyTarget.{u} :=
  ObligationTree.exactTarget_of_components Observable.robertson
    (Observable.heisenbergCCR Observable.robertson)

#print axioms Observable.robertson
#print axioms Observable.heisenbergCCR
#print axioms heisenberg_uncertainty

end Stage1Instances.THM_M_1524
