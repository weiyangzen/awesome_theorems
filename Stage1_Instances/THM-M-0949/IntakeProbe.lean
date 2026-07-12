import Mathlib.Combinatorics.HalesJewett
import Mathlib.Data.Finset.Density
import Mathlib.Data.Real.Basic

/-!
# THM-M-0949 discovery-only intake probe

These checks authenticate pinned combinatorial-line, ordinary Hales-Jewett, and finite-density
interfaces adjacent to a future density Hales-Jewett encoding. `CandidateTargetShape` checks only
that the source-guided binder shape can be expressed. It is a definition of a proposition, not a
theorem declaration, proof, canonical target, or statement-gate fingerprint.
-/

open Combinatorics

#check Combinatorics.Line
#check Combinatorics.Line.proper
#check Combinatorics.Line.IsMono
#check Combinatorics.Line.exists_mono_in_high_dimension
#check Finset.dens
#check Finset.dens_eq_card_div_card

namespace Stage1.THM_M_0949.Intake

/-- Candidate binder shape only; the statement phase must source-review and freeze its conventions. -/
def CandidateTargetShape : Prop :=
  forall k : Nat, 0 < k -> forall delta : Real, 0 < delta ->
    exists N : Nat, 0 < N /\ forall n : Nat, N <= n ->
      forall A : Finset (Fin n -> Fin k), delta <= (A.dens : Real) ->
        exists l : Combinatorics.Line (Fin k) (Fin n), forall a : Fin k, l a ∈ A

#check CandidateTargetShape

end Stage1.THM_M_0949.Intake
