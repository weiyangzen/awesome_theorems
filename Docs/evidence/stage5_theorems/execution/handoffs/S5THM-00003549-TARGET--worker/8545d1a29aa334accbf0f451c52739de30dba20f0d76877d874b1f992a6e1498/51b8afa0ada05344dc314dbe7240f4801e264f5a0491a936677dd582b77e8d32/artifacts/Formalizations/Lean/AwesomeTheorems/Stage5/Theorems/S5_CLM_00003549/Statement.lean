import FormalConjectures.ErdosProblems.«1»

namespace AwesomeTheorems.Stage5.S5_CLM_00003549

/-- Active source-to-target transport against the exact frozen declaration. -/
theorem source_to_target
    (h : type_of% Erdos1.erdos_1.variants.least_N_5) :
    IsLeast {N | ∃ A, Erdos1.IsSumDistinctSet A N ∧ A.card = 5} 13 := by
  exact h

/-- Active target-to-source transport against the exact frozen declaration. -/
theorem target_to_source
    (h : IsLeast {N | ∃ A, Erdos1.IsSumDistinctSet A N ∧ A.card = 5} 13) :
    type_of% Erdos1.erdos_1.variants.least_N_5 := by
  exact h

/-- The source and claim-local statement surfaces elaborate to the same proposition. -/
theorem statement_equivalence :
    (type_of% Erdos1.erdos_1.variants.least_N_5) ↔
      IsLeast {N | ∃ A, Erdos1.IsSumDistinctSet A N ∧ A.card = 5} 13 := by
  rfl

end AwesomeTheorems.Stage5.S5_CLM_00003549
