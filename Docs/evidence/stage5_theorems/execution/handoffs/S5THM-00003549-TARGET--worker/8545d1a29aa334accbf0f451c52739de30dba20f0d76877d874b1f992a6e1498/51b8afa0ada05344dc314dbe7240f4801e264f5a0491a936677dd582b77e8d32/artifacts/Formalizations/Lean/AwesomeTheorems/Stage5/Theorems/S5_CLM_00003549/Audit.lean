import FormalConjectures.ErdosProblems.«1»

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace AwesomeTheorems.Stage5.S5_CLM_00003549

/-- Audit-local replay of the finite witness. -/
theorem audit_witness_at_thirteen :
    ∃ A, Erdos1.IsSumDistinctSet A 13 ∧ A.card = 5 := by
  refine ⟨{3, 6, 11, 12, 13}, ?_⟩
  decide

/-- Audit-local replay of the exhaustive finite obstruction below thirteen. -/
theorem audit_no_witness_at_twelve :
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

/-- Audit-local replay of the monotonic lower-bound step. -/
theorem audit_lower_bound_thirteen {N : ℕ}
    (h : ∃ A, Erdos1.IsSumDistinctSet A N ∧ A.card = 5) : 13 ≤ N := by
  by_contra hn
  have hN : N ≤ 12 := by omega
  rcases h with ⟨A, hA, hcard⟩
  apply audit_no_witness_at_twelve
  refine ⟨A, ?_, hcard⟩
  refine ⟨?_, hA.2⟩
  intro x hx
  have hx' := hA.1 hx
  simp only [Finset.mem_Icc] at hx' ⊢
  exact ⟨hx'.1, hx'.2.trans hN⟩

/-- Exact claim-owned root, rebuilt here so Audit.lean is a cold standalone replay. -/
theorem machine_root :
    IsLeast {N | ∃ A, Erdos1.IsSumDistinctSet A N ∧ A.card = 5} 13 := by
  constructor
  · exact audit_witness_at_thirteen
  · intro N hN
    exact audit_lower_bound_thirteen hN

/-- Kernel-checkable exact-type witness required by the provider route. -/
example : type_of% Erdos1.erdos_1.variants.least_N_5 := AwesomeTheorems.Stage5.S5_CLM_00003549.machine_root

/-- Reversed exact-type transport remains definitionally the same proposition. -/
example
    (h : type_of% Erdos1.erdos_1.variants.least_N_5) :
    IsLeast {N | ∃ A, Erdos1.IsSumDistinctSet A N ∧ A.card = 5} 13 := by
  exact h

#print axioms AwesomeTheorems.Stage5.S5_CLM_00003549.machine_root

end AwesomeTheorems.Stage5.S5_CLM_00003549
