import Mathlib.ModelTheory.Ultraproducts

/-!
# THM-M-0673: exact sentence form of Los's theorem

This module freezes and tests the statement boundary only. It does not provide
an independent proof of Los's theorem.
-/

namespace Stage1Instances.THM_M_0673

open Filter FirstOrder

universe u v w x

/-- The exact intake-selected sentence form of Los's theorem. -/
def LosSentenceTarget : Prop :=
  ∀ (I : Type u) (M : I → Type v) (U : Ultrafilter I)
    (L : Language.{w, x}) [∀ i, L.Structure (M i)] [∀ i, Nonempty (M i)]
    (phi : L.Sentence),
      (U : Filter I).Product M ⊨ phi ↔ ∀ᶠ i : I in U, M i ⊨ phi

/-- A direct spelling of the type family exposed by mathlib's
`FirstOrder.Language.Ultraproduct.sentence_realize`. -/
def PinnedMathlibSentenceShape : Prop :=
  ∀ (I : Type u) (M : I → Type v) (U : Ultrafilter I)
    (L : Language.{w, x}) [∀ i, L.Structure (M i)] [∀ i, Nonempty (M i)]
    (phi : L.Sentence),
      (U : Filter I).Product M ⊨ phi ↔ ∀ᶠ i : I in (U : Filter I), M i ⊨ phi

/-- Checked transport between the canonical target and the direct pinned shape. -/
theorem losSentenceTarget_iff_pinnedMathlibSentenceShape :
    LosSentenceTarget.{u, v, w, x} ↔ PinnedMathlibSentenceShape.{u, v, w, x} :=
  Iff.rfl

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedFactorNonempty : Prop :=
  ∀ (I : Type u) (M : I → Type v) (U : Ultrafilter I)
    (L : Language.{w, x}) [∀ i, L.Structure (M i)] (phi : L.Sentence),
      (U : Filter I).Product M ⊨ phi ↔ ∀ᶠ i : I in U, M i ⊨ phi

def mutationIndexDomainNat : Prop :=
  ∀ (M : Nat → Type v) (U : Ultrafilter Nat)
    (L : Language.{w, x}) [∀ i, L.Structure (M i)] [∀ i, Nonempty (M i)]
    (phi : L.Sentence),
      (U : Filter Nat).Product M ⊨ phi ↔ ∀ᶠ i : Nat in U, M i ⊨ phi

def mutationExistsSentence : Prop :=
  ∀ (I : Type u) (M : I → Type v) (U : Ultrafilter I)
    (L : Language.{w, x}) [∀ i, L.Structure (M i)] [∀ i, Nonempty (M i)],
    ∃ phi : L.Sentence,
      (U : Filter I).Product M ⊨ phi ↔ ∀ᶠ i : I in U, M i ⊨ phi

def mutationPrincipalUltrafiltersOnly : Prop :=
  ∀ (I : Type u) (M : I → Type v) (center : I)
    (L : Language.{w, x}) [∀ i, L.Structure (M i)] [∀ i, Nonempty (M i)]
    (phi : L.Sentence),
      ((pure center : Ultrafilter I) : Filter I).Product M ⊨ phi ↔
        ∀ᶠ i : I in (pure center : Ultrafilter I), M i ⊨ phi

/-- The canonical statement includes the principal-ultrafilter boundary. -/
theorem principal_boundary
    (I : Type u) (M : I → Type v) (center : I)
    (L : Language.{w, x}) [∀ i, L.Structure (M i)] [∀ i, Nonempty (M i)]
    (phi : L.Sentence) :
    ((pure center : Ultrafilter I) : Filter I).Product M ⊨ phi ↔
      ∀ᶠ i : I in (pure center : Ultrafilter I), M i ⊨ phi :=
  FirstOrder.Language.Ultraproduct.sentence_realize phi

end Stage1Instances.THM_M_0673

set_option pp.explicit true in
#print Stage1Instances.THM_M_0673.LosSentenceTarget
