import FormalConjectures.ErdosProblems.«1»

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace AwesomeTheorems.Stage5.S5_CLM_00003549

/-- The concrete set `{3, 6, 11, 12, 13}` is a five-element sum-distinct set in `Icc 1 13`. -/
theorem witness_at_thirteen :
    ∃ A, Erdos1.IsSumDistinctSet A 13 ∧ A.card = 5 := by
  refine ⟨{3, 6, 11, 12, 13}, ?_⟩
  decide

/-- No five-element sum-distinct set can be contained in `Icc 1 12`.

This is a closed finite decision: every candidate is a subset of the twelve-element interval,
and all of its powerset sums are evaluated by the generated decision procedure.
-/
theorem no_witness_at_twelve :
    ¬ ∃ A, Erdos1.IsSumDistinctSet A 12 ∧ A.card = 5 := by
  intro h
  rcases h with ⟨A, hA, hcard⟩
  have hexhaust :
      ((Finset.Icc 1 12).powerset.filter fun B =>
        B.card = 5 ∧
        (fun (⟨S, _⟩ : B.powerset) => S.sum id).Injective) = ∅ := by
    set_option maxRecDepth 100000 in
      set_option maxHeartbeats 0 in
        decide
  have hmem : A ∈ (Finset.Icc 1 12).powerset.filter fun B =>
      B.card = 5 ∧
        (fun (⟨S, _⟩ : B.powerset) => S.sum id).Injective := by
    simp only [Finset.mem_filter, Finset.mem_powerset]
    exact ⟨hA.1, hcard, hA.2⟩
  rw [hexhaust] at hmem
  simp at hmem

/-- Any five-element sum-distinct set has ambient upper endpoint at least thirteen. -/
theorem lower_bound_thirteen {N : ℕ}
    (h : ∃ A, Erdos1.IsSumDistinctSet A N ∧ A.card = 5) : 13 ≤ N := by
  by_contra hn
  have hN : N ≤ 12 := by omega
  rcases h with ⟨A, hA, hcard⟩
  apply no_witness_at_twelve
  refine ⟨A, ?_, hcard⟩
  refine ⟨?_, hA.2⟩
  intro x hx
  have hx' := hA.1 hx
  simp only [Finset.mem_Icc] at hx' ⊢
  exact ⟨hx'.1, hx'.2.trans hN⟩

/-- Independent trust-zero closure of the frozen statement; the provider proof body is unused. -/
theorem proof_root :
    IsLeast {N | ∃ A, Erdos1.IsSumDistinctSet A N ∧ A.card = 5} 13 := by
  constructor
  · exact witness_at_thirteen
  · intro N hN
    exact lower_bound_thirteen hN

/-- An active reference to the frozen provider declaration, used only for exact-type transport. -/
theorem provider_type_transport :
    type_of% Erdos1.erdos_1.variants.least_N_5 := by
  exact proof_root

end AwesomeTheorems.Stage5.S5_CLM_00003549
