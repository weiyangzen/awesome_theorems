import Statement

/-!
# THM-M-0652 independent validation probe

This module reconstructs the two proof-phase boundary results directly from
the frozen definitions. It does not import `Proof.lean` or
`ObligationTree.lean`, and it deliberately does not assert the general Craig
interpolation root.
-/

open FirstOrder

namespace Stage1Instances.THM_M_0652.Validation

universe u v

/-- Independent reconstruction when the antecedent vocabulary is common. -/
theorem independent_antecedent_boundary {L : Language.{u, v}}
    {phi psi : L.Sentence} (hEntails : SentenceEntails phi psi)
    (hVocab : VocabularySubset phi psi) :
    exists theta : L.Sentence, IsInterpolant phi psi theta := by
  refine ⟨phi, ⟨?_, ?_, hEntails⟩⟩
  · exact ⟨fun _ h => h, hVocab⟩
  · intro M _ _ hphi
    exact hphi

/-- Independent reconstruction when the consequent vocabulary is common. -/
theorem independent_consequent_boundary {L : Language.{u, v}}
    {phi psi : L.Sentence} (hEntails : SentenceEntails phi psi)
    (hVocab : VocabularySubset psi phi) :
    exists theta : L.Sentence, IsInterpolant phi psi theta := by
  refine ⟨psi, ⟨?_, hEntails, ?_⟩⟩
  · exact ⟨hVocab, fun _ h => h⟩
  · intro M _ _ hpsi
    exact hpsi

#print axioms independent_antecedent_boundary
#print axioms independent_consequent_boundary

end Stage1Instances.THM_M_0652.Validation
