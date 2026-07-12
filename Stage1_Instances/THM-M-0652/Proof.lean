import ObligationTree

/-!
# THM-M-0652 proof-phase admissions

This module implements the elementary semantic and vocabulary leaves available
from the frozen statement.  It also checks two genuine boundary constructions:
an endpoint itself is an interpolant when its vocabulary is already common.

The first-order completeness, cut-elimination, and Maehara extraction packages
remain open.  No unconditional proof of `Statement` is asserted here.
-/

open FirstOrder

namespace Stage1Instances.THM_M_0652

universe u v

/-- Syntactic vocabulary inclusion is reflexive. -/
theorem vocabularySubset_refl {L : Language.{u, v}} (phi : L.Sentence) :
    VocabularySubset phi phi := by
  intro S hphi
  exact hphi

/-- Syntactic vocabulary inclusion composes. -/
theorem vocabularySubset_trans {L : Language.{u, v}} {chi theta phi : L.Sentence}
    (hchiTheta : VocabularySubset chi theta)
    (hthetaPhi : VocabularySubset theta phi) :
    VocabularySubset chi phi := by
  intro S hphi
  exact hchiTheta S (hthetaPhi S hphi)

/-- Empty-theory semantic consequence is reflexive. -/
theorem sentenceEntails_refl {L : Language.{u, v}} (phi : L.Sentence) :
    SentenceEntails phi phi := by
  intro M _ _ hphi
  exact hphi

/-- Empty-theory semantic consequence composes. -/
theorem sentenceEntails_trans {L : Language.{u, v}} {phi theta psi : L.Sentence}
    (hphiTheta : SentenceEntails phi theta)
    (hthetaPsi : SentenceEntails theta psi) :
    SentenceEntails phi psi := by
  intro M _ _ hphi
  exact hthetaPsi (hphiTheta hphi)

/-- The antecedent is an interpolant when all of its symbols occur in the consequent. -/
theorem antecedent_isInterpolant {L : Language.{u, v}} {phi psi : L.Sentence}
    (hEntails : SentenceEntails phi psi)
    (hVocab : VocabularySubset phi psi) :
    IsInterpolant phi psi phi := by
  exact ⟨⟨vocabularySubset_refl phi, hVocab⟩,
    sentenceEntails_refl phi, hEntails⟩

/-- The consequent is an interpolant when all of its symbols occur in the antecedent. -/
theorem consequent_isInterpolant {L : Language.{u, v}} {phi psi : L.Sentence}
    (hEntails : SentenceEntails phi psi)
    (hVocab : VocabularySubset psi phi) :
    IsInterpolant phi psi psi := by
  exact ⟨⟨hVocab, vocabularySubset_refl psi⟩,
    hEntails, sentenceEntails_refl psi⟩

/-- Exact interpolation closure for the antecedent-vocabulary boundary case. -/
theorem interpolation_of_antecedent_vocabulary {L : Language.{u, v}}
    {phi psi : L.Sentence} (hEntails : SentenceEntails phi psi)
    (hVocab : VocabularySubset phi psi) :
    ∃ theta : L.Sentence, IsInterpolant phi psi theta :=
  ⟨phi, antecedent_isInterpolant hEntails hVocab⟩

/-- Exact interpolation closure for the consequent-vocabulary boundary case. -/
theorem interpolation_of_consequent_vocabulary {L : Language.{u, v}}
    {phi psi : L.Sentence} (hEntails : SentenceEntails phi psi)
    (hVocab : VocabularySubset psi phi) :
    ∃ theta : L.Sentence, IsInterpolant phi psi theta :=
  ⟨psi, consequent_isInterpolant hEntails hVocab⟩

end Stage1Instances.THM_M_0652

#print axioms Stage1Instances.THM_M_0652.vocabularySubset_refl
#print axioms Stage1Instances.THM_M_0652.vocabularySubset_trans
#print axioms Stage1Instances.THM_M_0652.sentenceEntails_refl
#print axioms Stage1Instances.THM_M_0652.sentenceEntails_trans
#print axioms Stage1Instances.THM_M_0652.antecedent_isInterpolant
#print axioms Stage1Instances.THM_M_0652.consequent_isInterpolant
#print axioms Stage1Instances.THM_M_0652.interpolation_of_antecedent_vocabulary
#print axioms Stage1Instances.THM_M_0652.interpolation_of_consequent_vocabulary
