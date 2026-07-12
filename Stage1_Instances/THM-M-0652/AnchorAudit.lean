import Mathlib.ModelTheory.Equivalence

/-!
# THM-M-0652 anchor probes

These checks inventory the pinned first-order infrastructure. None of the
declarations below is a Craig interpolation theorem.
-/

open FirstOrder
open FirstOrder.Language

namespace Stage1Instances.THM_M_0652.AnchorAudit

universe u v

#check Language
#check Language.Sentence
#check Language.LHom.onSentence
#check Language.LHom.realize_onSentence
#check Language.Theory.isSatisfiable_iff_isFinitelySatisfiable
#check Language.Theory.ModelType

/-- The pinned compactness theorem is supporting infrastructure, not root closure. -/
theorem compactness_support {L : Language.{u, v}} (T : L.Theory) :
    T.IsSatisfiable ↔ T.IsFinitelySatisfiable :=
  Theory.isSatisfiable_iff_isFinitelySatisfiable

/-- The pinned language-map semantics is supporting infrastructure. -/
theorem language_map_support {L L' : Language.{u, v}} (M : Type (max u v))
    [L.Structure M] [L'.Structure M] (g : L →ᴸ L') [g.IsExpansionOn M]
    (phi : L.Sentence) :
    M ⊨ g.onSentence phi ↔ M ⊨ phi :=
  g.realize_onSentence M phi

#print axioms compactness_support
#print axioms language_map_support

end Stage1Instances.THM_M_0652.AnchorAudit
