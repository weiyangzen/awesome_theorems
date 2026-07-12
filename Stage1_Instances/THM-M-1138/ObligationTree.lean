import Statement

/-!
# THM-M-1138 conditional obligation composition

This module checks only the final composition boundary of the frozen proof
architecture. The analytic maximum-principle package remains an explicit
premise; no proof of that package is asserted here.
-/

namespace Stage1Instances.THM_M_1138

/-- The terminal analytic package has exactly the canonical conclusion. Its
internal obligations are recorded separately in the frozen registry. -/
def BoundaryMaximumPackage : Prop :=
  forall (n : Nat) (U : Set (Space n)) (u : Space n -> Real),
    0 < n -> U.Nonempty -> IsOpen U -> IsConnected U -> Bornology.IsBounded U ->
    InnerProductSpace.HarmonicContOnCl u U ->
    exists y, y ∈ frontier U ∧ forall x, x ∈ closure U -> u x <= u y

/-- Checked transport from the terminal analytic package to the exact public
root. The premise is deliberately not manufactured in this phase. -/
theorem root_of_boundaryMaximumPackage
    (terminal : BoundaryMaximumPackage) : HarmonicWeakMaximumPrinciple := by
  exact terminal

#print axioms root_of_boundaryMaximumPackage

end Stage1Instances.THM_M_1138
