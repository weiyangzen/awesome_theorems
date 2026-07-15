import Statement

/-!
# THM-M-0612 encoding sanity checks

These proofs rule out two vacuous routes through the frozen statement. They do
not prove the nonlinear radius obstruction or Gromov nonsqueezing.
-/

noncomputable section

namespace Stage1.THM_M_0612

universe u

theorem probe_standardForm_nondegenerate
    {Q : Type u} [Fintype Q]
    (v : PhaseSpace Q) (h : forall w, standardForm v w = 0) : v = 0 := by
  classical
  funext a
  cases a with
  | inl i =>
      have hi := h (Pi.single (Sum.inr i) 1)
      simpa [standardForm, Pi.single_apply, Finset.sum_ite_irrel] using hi
  | inr i =>
      have hi := h (Pi.single (Sum.inl i) 1)
      have hv : -v (Sum.inr i) = 0 := by
        simpa [standardForm, Pi.single_apply, Finset.sum_ite_irrel,
          Finset.sum_neg_distrib] using hi
      exact neg_eq_zero.mp hv

theorem probe_fderiv_injective
    {Q : Type u} [Fintype Q] {r : Real}
    {f : PhaseSpace Q -> PhaseSpace Q}
    (hf : IsSymplecticEmbeddingOnBall r f)
    {x : PhaseSpace Q} (hx : x ∈ ball r) :
    Function.Injective (fderiv Real f x) := by
  intro v w hvw
  apply sub_eq_zero.mp
  apply probe_standardForm_nondegenerate
  intro z
  have hform := hf.2.2 x hx (v - w) z
  rw [map_sub, hvw, sub_self] at hform
  simpa [standardForm] using hform.symm

#print axioms probe_standardForm_nondegenerate
#print axioms probe_fderiv_injective

end Stage1.THM_M_0612
