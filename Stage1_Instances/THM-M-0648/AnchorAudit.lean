import Mathlib.ModelTheory.Satisfiability

/-!
# THM-M-0648 anchor audit probes

These checked applications repeat exactly the input and output shapes of the frozen target halves
and establish that the two declarations found in pinned mathlib inhabit them. This audit file does
not combine the halves into `CanonicalTarget` and does not claim the proof or release phases.
-/

namespace Stage1Instances.THM_M_0648

open Cardinal FirstOrder
open CategoryTheory

universe u v wM wK

theorem auditedDownwardCandidate (L : Language.{u, v}) (M : Type wM) [Nonempty M]
    [L.Structure M] (A : Set M) (kappa : Cardinal.{wK})
    (hInfinite : aleph0 <= kappa)
    (hA : Cardinal.lift.{wK} #A <= Cardinal.lift.{wM} kappa)
    (hL : Cardinal.lift.{wK} L.card <= Cardinal.lift.{max u v} kappa)
    (hM : Cardinal.lift.{wM} kappa <= Cardinal.lift.{wK} #M) :
    exists S : L.ElementarySubstructure M,
      A ⊆ S ∧ Cardinal.lift.{wK} #S = Cardinal.lift.{wM} kappa :=
  L.exists_elementarySubstructure_card_eq A kappa hInfinite hA hL hM

theorem auditedUpwardCandidate (L : Language.{u, v}) (M : Type wM) [L.Structure M]
    [Infinite M] (kappa : Cardinal.{wK})
    (hL : Cardinal.lift.{wK} L.card <= Cardinal.lift.{max u v} kappa)
    (hM : Cardinal.lift.{wK} #M <= Cardinal.lift.{wM} kappa) :
    exists N : Bundled L.Structure, Nonempty (M ↪ₑ[L] N) ∧ #N = kappa :=
  L.exists_elementaryEmbedding_card_eq_of_ge M kappa hL hM

end Stage1Instances.THM_M_0648

#print axioms FirstOrder.Language.exists_elementarySubstructure_card_eq
#print axioms FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge
#print axioms Stage1Instances.THM_M_0648.auditedDownwardCandidate
#print axioms Stage1Instances.THM_M_0648.auditedUpwardCandidate
