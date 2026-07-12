/-!
# THM-M-0464 independent validation probes

This fragment is elaborated after `Statement.lean` and `ObligationTree.lean`.  It independently
reconstructs two proof-phase boundary results without importing or invoking `Proof.lean`.
-/

namespace AwesomeTheorems.THM_M_0464.Validation

open Set

theorem independent_countingConclusion_empty {n : ℕ} {epsilon : ℝ} :
    ObligationTree.CountingConclusion n (∅ : Set (Fin n → ℝ)) epsilon := by
  refine ⟨0, fun T _hT => ?_⟩
  have hrp : rationalPoints ((∅ : Set (Fin n → ℝ)) \ algebraicPart ∅) T = ∅ := by
    ext q
    simp [rationalPoints]
  rw [hrp]
  simp

theorem independent_countingConclusion_of_semialgebraic_connected
    {n : ℕ} {X : Set (Fin n → ℝ)} {epsilon : ℝ}
    (hsa : IsSemialgebraic X) (hconn : IsConnected X) (hnss : ¬X.Subsingleton) :
    ObligationTree.CountingConclusion n X epsilon := by
  have hsubset : X ⊆ algebraicPart X := by
    intro x hx
    rw [algebraicPart]
    exact mem_sUnion_of_mem hx ⟨subset_rfl, hsa, hconn, hnss⟩
  refine ⟨0, fun T _hT => ?_⟩
  have hrp : rationalPoints (X \ algebraicPart X) T = ∅ := by
    rw [diff_eq_empty.mpr hsubset]
    ext q
    simp [rationalPoints]
  rw [hrp]
  simp

#print axioms independent_countingConclusion_empty
#print axioms independent_countingConclusion_of_semialgebraic_connected

end AwesomeTheorems.THM_M_0464.Validation
