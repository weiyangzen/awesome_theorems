import Mathlib.ModelTheory.Semantics

/-!
# THM-M-0652: Craig's first-order interpolation theorem

This module freezes the sentence-level semantic statement in one ambient
first-order language.  The interpolant's nonlogical symbols are required to
occur in both endpoint sentences; equality and the logical connectives are
logical symbols and therefore need no support entry.
-/

open FirstOrder
open FirstOrder.Language

namespace Stage1Instances.THM_M_0652

universe u v w

/-- The function and relation symbols allowed in a first-order expression. -/
structure SymbolSupport (L : Language.{u, v}) : Type (max (u + 1) (v + 1)) where
  functions : (n : Nat) -> Set (L.Functions n)
  relations : (n : Nat) -> Set (L.Relations n)

/-- Every function symbol in a term belongs to the specified support. -/
def TermSupported {L : Language.{u, v}} {alpha : Type w} (S : SymbolSupport L) :
    L.Term alpha -> Prop
  | .var _ => True
  | .func f ts => f ∈ S.functions _ ∧ ∀ i, TermSupported S (ts i)

/-- Every nonlogical symbol in a bounded formula belongs to the specified support. -/
def BoundedFormulaSupported {L : Language.{u, v}} {alpha : Type w}
    (S : SymbolSupport L) : ∀ {n : Nat}, L.BoundedFormula alpha n -> Prop
  | _, .falsum => True
  | _, .equal t₁ t₂ => TermSupported S t₁ ∧ TermSupported S t₂
  | _, .rel R ts => R ∈ S.relations _ ∧ ∀ i, TermSupported S (ts i)
  | _, .imp phi psi => BoundedFormulaSupported S phi ∧ BoundedFormulaSupported S psi
  | _, .all phi => BoundedFormulaSupported S phi

/-- Sentence-level specialization of syntactic support. -/
abbrev SentenceSupported {L : Language.{u, v}} (S : SymbolSupport L)
    (phi : L.Sentence) : Prop :=
  BoundedFormulaSupported S phi

/--
All nonlogical symbols of `theta` occur in `phi`.  Quantification over every
support makes this an exact occurrence-subset condition, rather than a choice
of a possibly oversized support.
-/
def VocabularySubset {L : Language.{u, v}} (theta phi : L.Sentence) : Prop :=
  ∀ S : SymbolSupport L, SentenceSupported S phi -> SentenceSupported S theta

/-- `theta` uses only symbols common to the two endpoint sentences. -/
def UsesOnlyCommonVocabulary {L : Language.{u, v}}
    (theta phi psi : L.Sentence) : Prop :=
  VocabularySubset theta phi ∧ VocabularySubset theta psi

/-- Empty-theory semantic consequence between sentences. -/
def SentenceEntails {L : Language.{u, v}} (phi psi : L.Sentence) : Prop :=
  ∀ ⦃M : Type (max u v)⦄ [Nonempty M] [L.Structure M], M ⊨ phi -> M ⊨ psi

/-- A sentence is a Craig interpolant between `phi` and `psi`. -/
def IsInterpolant {L : Language.{u, v}}
    (phi psi theta : L.Sentence) : Prop :=
  UsesOnlyCommonVocabulary theta phi psi ∧
    SentenceEntails phi theta ∧ SentenceEntails theta psi

/--
Craig's interpolation theorem, in its classical first-order, semantic,
sentence-level form.
-/
def Statement : Prop :=
  ∀ (L : Language.{u, v}) (phi psi : L.Sentence),
    SentenceEntails phi psi -> ∃ theta : L.Sentence, IsInterpolant phi psi theta

/-- Checked transparent expansion of the canonical target. -/
theorem statement_iff :
    Statement.{u, v} ↔
      ∀ (L : Language.{u, v}) (phi psi : L.Sentence),
        SentenceEntails phi psi ->
          ∃ theta : L.Sentence,
            UsesOnlyCommonVocabulary theta phi psi ∧
              SentenceEntails phi theta ∧ SentenceEntails theta psi :=
  Iff.rfl

/-! Boundary probes: the target admits the empty language and arbitrary endpoint sentences. -/

example (hStatement : Statement.{0, 0}) (phi psi : Language.empty.Sentence)
    (h : SentenceEntails phi psi) :
    ∃ theta : Language.empty.Sentence, IsInterpolant phi psi theta := by
  exact hStatement Language.empty phi psi h

example (hStatement : Statement.{u, v}) (L : Language.{u, v}) (phi psi : L.Sentence)
    (h : SentenceEntails phi psi) :
    ∃ theta : L.Sentence,
      VocabularySubset theta phi ∧ VocabularySubset theta psi ∧
        SentenceEntails phi theta ∧ SentenceEntails theta psi := by
  obtain ⟨theta, hCommon, hLeft, hRight⟩ := hStatement L phi psi h
  exact ⟨theta, hCommon.1, hCommon.2, hLeft, hRight⟩

/-! Definitional-identity mutation probes. Each weakened or reversed target must be rejected. -/

/--
error: Type mismatch
  Iff.rfl
has type
  ?m.3 ↔ ?m.3
but is expected to have type
  Statement ↔ ∀ (L : Language) (phi psi : L.Sentence), ∃ theta, IsInterpolant phi psi theta
-/
#guard_msgs in
example :
    Statement.{u, v} ↔
      ∀ (L : Language.{u, v}) (phi psi : L.Sentence),
        ∃ theta : L.Sentence, IsInterpolant phi psi theta :=
  Iff.rfl

/--
error: Type mismatch
  Iff.rfl
has type
  ?m.5 ↔ ?m.5
but is expected to have type
  Statement ↔
    ∀ (L : Language) (phi psi : L.Sentence),
      SentenceEntails phi psi → ∃ theta, SentenceEntails phi theta ∧ SentenceEntails theta psi
-/
#guard_msgs in
example :
    Statement.{u, v} ↔
      ∀ (L : Language.{u, v}) (phi psi : L.Sentence),
        SentenceEntails phi psi ->
          ∃ theta : L.Sentence, SentenceEntails phi theta ∧ SentenceEntails theta psi :=
  Iff.rfl

/--
error: Type mismatch
  Iff.rfl
has type
  ?m.6 ↔ ?m.6
but is expected to have type
  Statement ↔
    ∀ (L : Language) (phi psi : L.Sentence),
      SentenceEntails phi psi →
        ∃ theta, UsesOnlyCommonVocabulary theta phi psi ∧ SentenceEntails phi theta ∧ SentenceEntails psi theta
-/
#guard_msgs in
example :
    Statement.{u, v} ↔
      ∀ (L : Language.{u, v}) (phi psi : L.Sentence),
        SentenceEntails phi psi ->
          ∃ theta : L.Sentence,
            UsesOnlyCommonVocabulary theta phi psi ∧
              SentenceEntails phi theta ∧ SentenceEntails psi theta :=
  Iff.rfl

end Stage1Instances.THM_M_0652

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0652.Statement

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0652.statement_iff

#print axioms Stage1Instances.THM_M_0652.statement_iff
