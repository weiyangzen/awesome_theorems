/-!
# THM-M-0464 proof execution

This fragment is elaborated after `Statement.lean` and `ObligationTree.lean`.  It closes the
set-theoretic algebraic-part and degenerate counting leaves without assuming Pila-Wilkie or any of
its open analytic/geometric packages.
-/

namespace AwesomeTheorems.THM_M_0464.Proof

open Set

theorem subset_algebraicPart_of_semialgebraic_connected
    {n : ℕ} {X : Set (Fin n → ℝ)}
    (hsa : IsSemialgebraic X) (hconn : IsConnected X) (hnss : ¬X.Subsingleton) :
    X ⊆ algebraicPart X := by
  intro x hx
  rw [algebraicPart]
  exact mem_sUnion_of_mem hx ⟨subset_rfl, hsa, hconn, hnss⟩

theorem algebraicPart_subset {n : ℕ} (X : Set (Fin n → ℝ)) :
    algebraicPart X ⊆ X := by
  intro x hx
  rw [algebraicPart] at hx
  obtain ⟨s, hs, hxs⟩ := mem_sUnion.mp hx
  exact hs.1 hxs

theorem algebraicPart_mono {n : ℕ} {X Y : Set (Fin n → ℝ)} (hXY : X ⊆ Y) :
    algebraicPart X ⊆ algebraicPart Y := by
  intro x hx
  rw [algebraicPart] at hx ⊢
  obtain ⟨s, hs, hxs⟩ := mem_sUnion.mp hx
  exact mem_sUnion_of_mem hxs ⟨hs.1.trans hXY, hs.2⟩

theorem rationalPoints_mono {n : ℕ} {X Y : Set (Fin n → ℝ)} (hXY : X ⊆ Y) (T : ℕ) :
    rationalPoints X T ⊆ rationalPoints Y T := by
  intro q hq
  exact ⟨hXY hq.1, hq.2⟩

theorem countingConclusion_of_diff_eq_empty
    {n : ℕ} {X : Set (Fin n → ℝ)} {epsilon : ℝ}
    (h : X \ algebraicPart X = ∅) :
    ObligationTree.CountingConclusion n X epsilon := by
  refine ⟨0, fun T _hT => ?_⟩
  have hrp : rationalPoints (X \ algebraicPart X) T = ∅ := by
    rw [h]
    ext q
    simp [rationalPoints]
  rw [hrp]
  simp

theorem countingConclusion_of_semialgebraic_connected
    {n : ℕ} {X : Set (Fin n → ℝ)} {epsilon : ℝ}
    (hsa : IsSemialgebraic X) (hconn : IsConnected X) (hnss : ¬X.Subsingleton) :
    ObligationTree.CountingConclusion n X epsilon := by
  apply countingConclusion_of_diff_eq_empty
  exact diff_eq_empty.mpr (subset_algebraicPart_of_semialgebraic_connected hsa hconn hnss)

theorem countingConclusion_empty {n : ℕ} {epsilon : ℝ} :
    ObligationTree.CountingConclusion n (∅ : Set (Fin n → ℝ)) epsilon := by
  apply countingConclusion_of_diff_eq_empty
  exact diff_eq_empty.mpr (empty_subset _)

#print axioms subset_algebraicPart_of_semialgebraic_connected
#print axioms algebraicPart_subset
#print axioms algebraicPart_mono
#print axioms rationalPoints_mono
#print axioms countingConclusion_of_diff_eq_empty
#print axioms countingConclusion_of_semialgebraic_connected
#print axioms countingConclusion_empty

end AwesomeTheorems.THM_M_0464.Proof
