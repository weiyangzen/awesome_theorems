import Mathlib.Combinatorics.SetFamily.KruskalKatona
import Mathlib.Data.Finset.Slice

/-!
# THM-M-0964 discovery-only intake probe

This file checks pinned finite-set vocabulary and elaborates a source-guided candidate proposition
shape for a later Hilton-Milner statement. `CandidateTargetShape` is only a definition of a
proposition. It is not the canonical target, a theorem, or a proof.
-/

#check Set.Intersecting
#check Set.Sized
#check Set.sInter
#check Finset.powersetCard
#check Finset.card_powersetCard
#check Finset.erdos_ko_rado
#check Nat.choose

namespace Stage1.THM_M_0964.Intake

/--
Candidate bound-only shape from immutable secondary restatements. The statement phase must review
the primary theorem, endpoint conventions, and whether equality classification belongs to the root.
-/
def CandidateTargetShape : Prop :=
  forall n k : Nat, 2 <= k -> 2 * k < n ->
    forall F : Finset (Finset (Fin n)),
      (F : Set (Finset (Fin n))).Sized k ->
      (F : Set (Finset (Fin n))).Intersecting ->
      Set.sInter (((fun A : Finset (Fin n) => (A : Set (Fin n))) ''
        (F : Set (Finset (Fin n))))) = (∅ : Set (Fin n)) ->
      F.card <= (n - 1).choose (k - 1) - (n - k - 1).choose (k - 1) + 1

#check CandidateTargetShape

end Stage1.THM_M_0964.Intake
