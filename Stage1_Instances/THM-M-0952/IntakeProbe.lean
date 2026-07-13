import Mathlib.Algebra.Group.Pointwise.Finset.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-!
# THM-M-0952 discovery-only intake probe

These checks authenticate pinned finite real sumset, product-set, cardinality, maximum, and real
power interfaces adjacent to a future Elekes statement. `CandidateTargetShape` checks only that a
source-guided binder shape can be expressed. It is a definition of a proposition, not a theorem,
proof, canonical target, or statement-gate fingerprint.
-/

open scoped Pointwise

noncomputable section

local instance : DecidableEq Real := Classical.decEq Real

variable (A : Finset Real)

#check A + A
#check A * A
#check (A + A).card
#check (A * A).card
#check max (A + A).card (A * A).card
#check Real.rpow

namespace Stage1.THM_M_0952.Intake

/-- Candidate binder shape only; the statement phase must source-review and freeze its conventions. -/
def CandidateTargetShape : Prop :=
  exists c : Real, 0 < c /\ forall A : Finset Real,
    (forall a : Real, a ∈ A -> a != 0) ->
      c * Real.rpow (A.card : Real) (5 / 4 : Real) <=
        (max (A + A).card (A * A).card : Real)

#check CandidateTargetShape

end Stage1.THM_M_0952.Intake
