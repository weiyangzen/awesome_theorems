import Statement

/-!
# THM-M-0652 conditional obligation composition

This module checks the interfaces between semantic completeness, syntactic
interpolation, and soundness.  All three mathematical packages remain explicit
premises; no Craig interpolation proof is asserted here.
-/

open FirstOrder

namespace Stage1Instances.THM_M_0652

universe u v

/-- A still-unimplemented derivability relation for the selected first-order calculus. -/
abbrev DerivationRelation :=
  {L : Language.{u, v}} -> L.Sentence -> L.Sentence -> Prop

/-- The semantic-to-syntactic completeness bridge required by the proof route. -/
def SemanticCompleteness (derives : DerivationRelation.{u, v}) : Prop :=
  forall {L : Language.{u, v}} {phi psi : L.Sentence},
    SentenceEntails phi psi -> derives phi psi

/-- The Maehara/cut-elimination output, including the exact common vocabulary condition. -/
def SyntacticInterpolation (derives : DerivationRelation.{u, v}) : Prop :=
  forall {L : Language.{u, v}} {phi psi : L.Sentence},
    derives phi psi -> exists theta : L.Sentence,
      UsesOnlyCommonVocabulary theta phi psi /\ derives phi theta /\ derives theta psi

/-- Soundness for both derivability legs returned by interpolation extraction. -/
def DerivationSoundness (derives : DerivationRelation.{u, v}) : Prop :=
  forall {L : Language.{u, v}} {phi psi : L.Sentence},
    derives phi psi -> SentenceEntails phi psi

/-- Checked child-to-root composition for the frozen proof architecture. -/
theorem statement_of_calculus_packages
    (derives : DerivationRelation.{u, v})
    (complete : SemanticCompleteness derives)
    (interpolate : SyntacticInterpolation derives)
    (sound : DerivationSoundness derives) :
    Statement.{u, v} := by
  intro L phi psi hEntails
  obtain ⟨theta, hCommon, hLeft, hRight⟩ := interpolate (complete hEntails)
  exact ⟨theta, hCommon, sound hLeft, sound hRight⟩

#print axioms statement_of_calculus_packages

end Stage1Instances.THM_M_0652
