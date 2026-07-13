import Mathlib.Data.Finset.Powerset

/-!
# THM-M-0963 discovery-only intake probe

These checks authenticate finite-family, pairwise-intersection, powerset-cardinality, and
binomial interfaces adjacent to a future Ray-Chaudhuri-Wilson statement. `CandidateTargetShape`
only checks that the secondary-source binder shape is expressible. It is a definition of a
proposition, not a theorem, proof, canonical target, or statement-gate fingerprint.
-/

#check Set.Pairwise
#check Finset.inter_subset_left
#check Finset.card_le_card
#check Finset.powersetCard
#check Finset.mem_powersetCard
#check Finset.card_powersetCard
#check Nat.choose

namespace Stage1.THM_M_0963.Intake

/-- Candidate binder shape only; the statement phase must primary-source-review all conventions. -/
def CandidateTargetShape : Prop :=
  forall n k s : Nat, 0 < s -> s <= k -> k <= n ->
    forall L : Finset Nat, L.card = s ->
      forall F : Finset (Finset (Fin n)),
        (forall A, A ∈ F -> A.card = k) ->
        (F : Set (Finset (Fin n))).Pairwise (fun A B => (A ∩ B).card ∈ L) ->
          F.card <= n.choose s

#check CandidateTargetShape

end Stage1.THM_M_0963.Intake
